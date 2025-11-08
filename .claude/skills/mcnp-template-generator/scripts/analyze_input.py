"""
MCNP Input Analyzer for Template Conversion
Identifies sections suitable for parameterization
"""

import re
import argparse
from collections import defaultdict


def analyze_mcnp_input(filename):
    """
    Analyze MCNP input to identify candidate template variables.

    Args:
        filename: Path to MCNP input file

    Returns:
        dict with analysis results
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Identify block boundaries
    blocks = identify_blocks(lines)

    # Analyze each block
    cell_analysis = analyze_cells(lines, blocks['cells'])
    surface_analysis = analyze_surfaces(lines, blocks['surfaces'])
    data_analysis = analyze_data(lines, blocks['data'])

    # Identify repeated patterns
    patterns = find_repeated_patterns(lines)

    # Generate recommendations
    recommendations = generate_recommendations(
        cell_analysis, surface_analysis, data_analysis, patterns
    )

    return {
        'blocks': blocks,
        'cell_analysis': cell_analysis,
        'surface_analysis': surface_analysis,
        'data_analysis': data_analysis,
        'patterns': patterns,
        'recommendations': recommendations
    }


def identify_blocks(lines):
    """Identify cell, surface, and data block boundaries."""
    blocks = {'cells': [], 'surfaces': [], 'data': []}

    current_block = 'cells'
    blank_count = 0

    for i, line in enumerate(lines):
        # Detect block transitions (blank line)
        if line.strip() == '':
            blank_count += 1
            if blank_count == 1 and current_block == 'cells':
                current_block = 'surfaces'
            elif blank_count == 2 and current_block == 'surfaces':
                current_block = 'data'
        else:
            blank_count = 0

        blocks[current_block].append(i)

    return blocks


def analyze_cells(lines, cell_indices):
    """Analyze cell block for parameterization candidates."""
    cells = []

    for i in cell_indices:
        line = lines[i].strip()
        if not line or line.startswith('c'):
            continue

        # Parse cell card
        parts = line.split()
        if len(parts) < 3:
            continue

        cell_num = parts[0]
        mat_num = parts[1]
        density = parts[2] if parts[1] != '0' else None

        cells.append({
            'line': i,
            'cell_num': cell_num,
            'mat_num': mat_num,
            'density': density,
            'universe': extract_universe(line)
        })

    # Identify patterns
    universe_groups = defaultdict(list)
    for cell in cells:
        if cell['universe']:
            universe_groups[cell['universe']].append(cell)

    return {
        'total_cells': len(cells),
        'universe_groups': dict(universe_groups),
        'material_variants': count_material_variants(cells)
    }


def analyze_surfaces(lines, surface_indices):
    """Analyze surface block for parameterization candidates."""
    surfaces = []

    for i in surface_indices:
        line = lines[i].strip()
        if not line or line.startswith('c'):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        surf_num = parts[0]
        surf_type = parts[1]

        surfaces.append({
            'line': i,
            'surf_num': surf_num,
            'surf_type': surf_type
        })

    return {
        'total_surfaces': len(surfaces),
        'surface_types': count_surface_types(surfaces)
    }


def analyze_data(lines, data_indices):
    """Analyze data block for parameterization candidates."""
    materials = []
    current_material = None

    for i in data_indices:
        line = lines[i].strip()

        # Material card start
        if line.startswith('m') and not line.startswith('mt'):
            mat_match = re.match(r'm(\d+)', line, re.IGNORECASE)
            if mat_match:
                current_material = {
                    'line': i,
                    'mat_num': mat_match.group(1),
                    'isotopes': []
                }
                materials.append(current_material)

        # Isotope line
        elif current_material and not line.startswith('c'):
            isotope_match = re.findall(r'(\d+\.\d+c)\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', line)
            current_material['isotopes'].extend(isotope_match)

    return {
        'total_materials': len(materials),
        'materials': materials
    }


def find_repeated_patterns(lines):
    """Identify repeated multi-line patterns (candidate for loops/templates)."""
    # Look for repeated cell definitions (similar structure)
    patterns = []

    # Example: Find repeated lattice fill patterns
    fill_pattern = re.compile(r'fill=(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)')

    for i, line in enumerate(lines):
        match = fill_pattern.search(line)
        if match:
            patterns.append({
                'line': i,
                'type': 'fill_array',
                'bounds': match.groups()
            })

    return patterns


def count_material_variants(cells):
    """Count how many different materials are used."""
    materials = set(cell['mat_num'] for cell in cells if cell['mat_num'] != '0')
    return len(materials)


def count_surface_types(surfaces):
    """Count surface types."""
    types = defaultdict(int)
    for surf in surfaces:
        types[surf['surf_type']] += 1
    return dict(types)


def extract_universe(line):
    """Extract universe number from cell card."""
    match = re.search(r'u=(\d+)', line, re.IGNORECASE)
    return match.group(1) if match else None


def generate_recommendations(cell_analysis, surface_analysis, data_analysis, patterns):
    """Generate template variable recommendations."""
    recommendations = []

    # Recommend lattice fill arrays as template variables
    if patterns:
        recommendations.append({
            'type': 'fill_array',
            'variable_name': 'lattice_fills',
            'reason': f'Found {len(patterns)} lattice fill arrays',
            'benefit': 'Can vary lattice contents programmatically'
        })

    # Recommend universe groups as template variables
    if len(cell_analysis['universe_groups']) > 5:
        recommendations.append({
            'type': 'universe_cells',
            'variable_name': 'assembly_cells',
            'reason': f'Found {len(cell_analysis["universe_groups"])} universe groups',
            'benefit': 'Can swap assembly types easily'
        })

    # Recommend material variations
    if cell_analysis['material_variants'] > 20:
        recommendations.append({
            'type': 'materials',
            'variable_name': 'fuel_materials',
            'reason': f'Found {cell_analysis["material_variants"]} material definitions',
            'benefit': 'Can vary compositions for burnup or enrichment studies'
        })

    return recommendations


def print_report(analysis):
    """Print analysis report."""
    print("=" * 70)
    print("MCNP INPUT ANALYSIS FOR TEMPLATE CONVERSION")
    print("=" * 70)

    print(f"\n📊 BLOCK STRUCTURE")
    print(f"  Cell block:    lines 1-{len(analysis['blocks']['cells'])}")
    print(f"  Surface block: lines {len(analysis['blocks']['cells'])+1}-"
          f"{len(analysis['blocks']['cells'])+len(analysis['blocks']['surfaces'])}")
    print(f"  Data block:    lines {len(analysis['blocks']['cells'])+len(analysis['blocks']['surfaces'])+1}-end")

    print(f"\n📐 CELL ANALYSIS")
    print(f"  Total cells: {analysis['cell_analysis']['total_cells']}")
    print(f"  Universe groups: {len(analysis['cell_analysis']['universe_groups'])}")
    print(f"  Material variants: {analysis['cell_analysis']['material_variants']}")

    print(f"\n🔷 SURFACE ANALYSIS")
    print(f"  Total surfaces: {analysis['surface_analysis']['total_surfaces']}")
    print(f"  Surface types:")
    for surf_type, count in analysis['surface_analysis']['surface_types'].items():
        print(f"    {surf_type}: {count}")

    print(f"\n⚛️  DATA ANALYSIS")
    print(f"  Total materials: {analysis['data_analysis']['total_materials']}")

    print(f"\n🔁 REPEATED PATTERNS")
    print(f"  Lattice fill arrays: {len(analysis['patterns'])}")

    print(f"\n💡 RECOMMENDATIONS FOR TEMPLATE VARIABLES")
    if analysis['recommendations']:
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"\n  {i}. Template Variable: {{{{ {rec['variable_name']} }}}}")
            print(f"     Type: {rec['type']}")
            print(f"     Reason: {rec['reason']}")
            print(f"     Benefit: {rec['benefit']}")
    else:
        print("  No strong candidates found. Input may be too simple for templating.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analyze MCNP input for template conversion'
    )
    parser.add_argument('input_file', help='MCNP input file to analyze')
    args = parser.parse_args()

    analysis = analyze_mcnp_input(args.input_file)
    print_report(analysis)
