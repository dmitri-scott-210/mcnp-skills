# Validation Algorithms
## Detailed Pseudocode for Cross-Reference Checking

## Algorithm 1: Parse MCNP Input File

```python
def parse_mcnp_input(filename):
    """
    Parse MCNP input into structured data

    Returns:
        dict with keys: cells, surfaces, materials, data_cards
    """
    with open(filename) as f:
        lines = f.readlines()

    # MCNP input structure: cells, blank, surfaces, blank, data cards
    blocks = split_into_blocks(lines)

    cells = parse_cells_block(blocks['cells'])
    surfaces = parse_surfaces_block(blocks['surfaces'])
    materials = parse_materials_block(blocks['data'])

    return {
        'cells': cells,
        'surfaces': surfaces,
        'materials': materials,
        'filename': filename
    }

def split_into_blocks(lines):
    """
    Split input into cells, surfaces, data blocks
    Blocks separated by blank lines
    """
    blocks = {'cells': [], 'surfaces': [], 'data': []}
    current_block = 'cells'
    blank_count = 0

    for line in lines:
        # Skip comments
        if line.strip().startswith('c ') or line.strip().startswith('C '):
            continue

        # Detect blank line (block separator)
        if line.strip() == '':
            blank_count += 1
            if blank_count == 1:
                current_block = 'surfaces'
            elif blank_count == 2:
                current_block = 'data'
            continue

        blocks[current_block].append(line)

    return blocks
```

## Algorithm 2: Extract Surface References from Cell

```python
import re

def extract_surfaces_from_cell(cell_line):
    """
    Parse cell Boolean expression to extract surface IDs

    Args:
        cell_line: String like "100 1 -8.0  -500 501 -502"

    Returns:
        List of surface IDs (as integers)
    """
    # Remove cell ID, material ID, density
    parts = cell_line.split()

    # Skip first 3 entries (cell, material, density)
    geometry_part = ' '.join(parts[3:])

    # Remove options (u=, imp=, vol=, etc.)
    geometry_part = re.split(r'\s+(u=|imp:|vol=|fill=)', geometry_part)[0]

    # Extract all numbers (surface IDs)
    # Pattern: optional +/-, digits
    surface_pattern = r'[+-]?\d+'
    matches = re.findall(surface_pattern, geometry_part)

    # Convert to integers, remove signs
    surface_ids = [abs(int(m)) for m in matches]

    # Remove duplicates, sort
    return sorted(set(surface_ids))

# Example:
# cell_line = "60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110 imp:n=1"
# extract_surfaces_from_cell(cell_line)
# → [29, 53, 74, 100, 110, 1111, 1118]
```

## Algorithm 3: Detect Void Cell Type

```python
def classify_void_cell(cell_line):
    """
    Determine type of void cell (material 0)

    Returns:
        "material" - has non-zero material
        "lattice" - void with lat= specification
        "fill" - void with fill= specification
        "true_void" - void with no special specification
    """
    parts = cell_line.split()
    material_id = int(parts[1])

    if material_id != 0:
        return "material"

    # Material is 0 - check for lat= or fill=
    if 'lat=' in cell_line or 'lat =' in cell_line:
        return "lattice"
    elif 'fill=' in cell_line or 'fill =' in cell_line:
        return "fill"
    else:
        return "true_void"
```

## Algorithm 4: Validate Cell → Surface References

```python
def validate_cell_surfaces(cells, surfaces):
    """
    Check that all surfaces referenced by cells are defined

    Returns:
        List of errors
    """
    errors = []

    # Build set of defined surfaces
    defined_surfaces = set(surfaces.keys())

    for cell_id, cell_data in cells.items():
        referenced_surfaces = cell_data['surfaces']

        for surf_id in referenced_surfaces:
            if surf_id not in defined_surfaces:
                errors.append({
                    'type': 'undefined_surface',
                    'cell_id': cell_id,
                    'surface_id': surf_id,
                    'line': cell_data['line_number'],
                    'cell_line': cell_data['text']
                })

    return errors
```

## Algorithm 5: Validate Cell → Material References

```python
def validate_cell_materials(cells, materials):
    """
    Check that all materials referenced by cells are defined
    Properly handles void cells

    Returns:
        List of errors
    """
    errors = []

    # Build set of defined materials
    defined_materials = set(materials.keys())

    for cell_id, cell_data in cells.items():
        material_id = cell_data['material']
        cell_type = classify_void_cell(cell_data['text'])

        # Skip void cells (material 0)
        if cell_type in ['lattice', 'fill', 'true_void']:
            continue

        # Non-void cell - check if material defined
        if material_id not in defined_materials:
            errors.append({
                'type': 'undefined_material',
                'cell_id': cell_id,
                'material_id': material_id,
                'line': cell_data['line_number'],
                'cell_line': cell_data['text']
            })

    return errors
```

## Algorithm 6: Build Universe Fill Graph

```python
def build_universe_fill_graph(cells):
    """
    Build directed graph of universe fill relationships

    Returns:
        dict: {universe_id: [list of universes it fills with]}
    """
    fill_graph = {}
    universe_declarations = set()

    for cell_id, cell_data in cells.items():
        # Check if cell declares a universe
        if 'universe' in cell_data:
            u_id = cell_data['universe']
            universe_declarations.add(u_id)
            if u_id not in fill_graph:
                fill_graph[u_id] = []

        # Check if cell fills with universe(s)
        if 'fill' in cell_data:
            parent_u = cell_data.get('universe', 0)  # Default to 0 if not specified
            fill_ids = cell_data['fill']  # Can be single ID or list (lattice)

            if not isinstance(fill_ids, list):
                fill_ids = [fill_ids]

            if parent_u not in fill_graph:
                fill_graph[parent_u] = []

            fill_graph[parent_u].extend(fill_ids)

    return fill_graph, universe_declarations
```

## Algorithm 7: Detect Circular Universe References

```python
def detect_circular_universes(fill_graph):
    """
    Detect cycles in universe fill graph using DFS

    Returns:
        List of cycles (each cycle is a list of universe IDs)
    """
    def dfs_cycle(node, visited, rec_stack, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        cycles_found = []

        for neighbor in fill_graph.get(node, []):
            if neighbor not in visited:
                cycles_found.extend(dfs_cycle(neighbor, visited, rec_stack, path[:]))
            elif neighbor in rec_stack:
                # Cycle detected! Extract cycle from path
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles_found.append(cycle)

        rec_stack.remove(node)
        return cycles_found

    visited = set()
    all_cycles = []

    for universe in fill_graph:
        if universe not in visited:
            cycles = dfs_cycle(universe, visited, set(), [])
            all_cycles.extend(cycles)

    return all_cycles
```

## Algorithm 8: Validate Lattice Fill Arrays

```python
def validate_lattice_fill(cell_data):
    """
    Check that lattice fill array has correct number of elements

    Args:
        cell_data: Dict with 'fill_bounds' and 'fill_array'

    Returns:
        Error dict if mismatch, None if OK
    """
    bounds = cell_data['fill_bounds']  # e.g., "-7:7 -7:7 0:0"
    fill_array = cell_data['fill_array']  # List of universe IDs

    # Parse bounds
    ranges = bounds.split()
    i_range = ranges[0].split(':')
    j_range = ranges[1].split(':')
    k_range = ranges[2].split(':')

    i_min, i_max = int(i_range[0]), int(i_range[1])
    j_min, j_max = int(j_range[0]), int(j_range[1])
    k_min, k_max = int(k_range[0]), int(k_range[1])

    # Calculate expected elements
    expected = (i_max - i_min + 1) * (j_max - j_min + 1) * (k_max - k_min + 1)

    # Expand repeat notation in fill_array
    expanded_array = expand_repeat_notation(fill_array)
    actual = len(expanded_array)

    if expected != actual:
        return {
            'type': 'lattice_size_mismatch',
            'cell_id': cell_data['cell_id'],
            'expected': expected,
            'actual': actual,
            'bounds': bounds,
            'breakdown': f"({i_max}-{i_min}+1) × ({j_max}-{j_min}+1) × ({k_max}-{k_min}+1)"
        }

    return None  # OK

def expand_repeat_notation(fill_array):
    """
    Expand MCNP repeat notation (nR) to full array

    Example:
        ["100", "2R", "200", "24R"] → [100, 100, 100, 200, 200, ... (25 times)]
    """
    expanded = []
    i = 0
    while i < len(fill_array):
        element = fill_array[i]

        if element.endswith('R'):
            # Repeat notation: previous element repeated n+1 times total
            n = int(element[:-1])
            prev_element = expanded[-1]
            for _ in range(n):
                expanded.append(prev_element)
        else:
            # Normal element
            expanded.append(int(element))

        i += 1

    return expanded
```

## Algorithm 9: Detect Duplicate IDs

```python
def detect_duplicates(entity_dict):
    """
    Find duplicate IDs in cells, surfaces, materials, or universes

    Args:
        entity_dict: {id: {'line_number': N, ...}}

    Returns:
        List of duplicate errors
    """
    # Group by ID
    id_locations = {}
    for entity_id, data in entity_dict.items():
        if entity_id not in id_locations:
            id_locations[entity_id] = []
        id_locations[entity_id].append(data['line_number'])

    # Find duplicates
    duplicates = []
    for entity_id, locations in id_locations.items():
        if len(locations) > 1:
            duplicates.append({
                'id': entity_id,
                'locations': locations
            })

    return duplicates
```

## Algorithm 10: Generate Validation Report

```python
def generate_validation_report(errors, warnings, info):
    """
    Create formatted validation report

    Args:
        errors: List of fatal error dicts
        warnings: List of warning dicts
        info: Dict with informational statistics

    Returns:
        Formatted report string
    """
    report = []

    # Header
    report.append("=" * 70)
    report.append("MCNP CROSS-REFERENCE VALIDATION REPORT")
    report.append(f"File: {info['filename']}")
    report.append("=" * 70)
    report.append("")

    # Section 1: Fatal Errors
    report.append("SECTION 1: FATAL ERRORS")
    report.append("-" * 70)
    if errors:
        for i, error in enumerate(errors, 1):
            report.append(f"[{i}] {format_error(error)}")
            report.append("")
    else:
        report.append("✓ No fatal errors detected")
        report.append("")

    # Section 2: Warnings
    report.append("SECTION 2: WARNINGS")
    report.append("-" * 70)
    if warnings:
        for i, warning in enumerate(warnings, 1):
            report.append(f"[{i}] {format_warning(warning)}")
            report.append("")
    else:
        report.append("✓ No warnings")
        report.append("")

    # Section 3: Informational
    report.append("SECTION 3: STATISTICS")
    report.append("-" * 70)
    report.append(f"Total cells:     {info['num_cells']}")
    report.append(f"Total surfaces:  {info['num_surfaces']}")
    report.append(f"Total materials: {info['num_materials']}")
    report.append(f"Total universes: {info['num_universes']}")
    report.append("")

    # Section 4: Summary
    report.append("SECTION 4: SUMMARY")
    report.append("-" * 70)
    if errors:
        report.append(f"❌ VALIDATION FAILED: {len(errors)} fatal error(s)")
    else:
        report.append("✅ VALIDATION PASSED")
    report.append("")

    return "\n".join(report)

def format_error(error):
    """Format individual error for report"""
    if error['type'] == 'undefined_surface':
        return (
            f"UNDEFINED SURFACE\n"
            f"  Cell: {error['cell_id']} (line {error['line']})\n"
            f"  Surface: {error['surface_id']} (not defined)\n"
            f"  Context: {error['cell_line']}"
        )
    elif error['type'] == 'undefined_material':
        return (
            f"UNDEFINED MATERIAL\n"
            f"  Cell: {error['cell_id']} (line {error['line']})\n"
            f"  Material: {error['material_id']} (not defined)\n"
            f"  Context: {error['cell_line']}"
        )
    elif error['type'] == 'circular_universe':
        cycle_str = " → ".join(map(str, error['cycle']))
        return (
            f"CIRCULAR UNIVERSE REFERENCE\n"
            f"  Cycle: {cycle_str}"
        )
    elif error['type'] == 'lattice_size_mismatch':
        return (
            f"LATTICE ARRAY SIZE MISMATCH\n"
            f"  Cell: {error['cell_id']}\n"
            f"  Expected: {error['expected']} elements\n"
            f"  Actual: {error['actual']} elements\n"
            f"  Bounds: {error['bounds']}\n"
            f"  Calculation: {error['breakdown']}"
        )
    else:
        return f"UNKNOWN ERROR: {error}"
```

## Complete Validation Workflow

```python
def validate_mcnp_input(filename):
    """
    Main validation function - orchestrates all checks
    """
    # Step 1: Parse input
    parsed = parse_mcnp_input(filename)

    # Step 2: Run all validation checks
    errors = []
    warnings = []

    # Check 1: Cell → Surface
    errors.extend(validate_cell_surfaces(parsed['cells'], parsed['surfaces']))

    # Check 2: Cell → Material
    errors.extend(validate_cell_materials(parsed['cells'], parsed['materials']))

    # Check 3: Universe fill graph
    fill_graph, universe_decls = build_universe_fill_graph(parsed['cells'])

    # Check 4: Circular references
    cycles = detect_circular_universes(fill_graph)
    for cycle in cycles:
        errors.append({'type': 'circular_universe', 'cycle': cycle})

    # Check 5: Undefined universes
    for parent_u, filled_univs in fill_graph.items():
        for u in filled_univs:
            if u not in universe_decls and u != 0:
                errors.append({'type': 'undefined_universe', 'universe_id': u})

    # Check 6: Lattice arrays
    for cell_id, cell_data in parsed['cells'].items():
        if 'lattice' in cell_data:
            lattice_error = validate_lattice_fill(cell_data)
            if lattice_error:
                errors.append(lattice_error)

    # Check 7: Duplicate IDs
    for entity_type in ['cells', 'surfaces', 'materials']:
        dups = detect_duplicates(parsed[entity_type])
        for dup in dups:
            errors.append({'type': f'duplicate_{entity_type}', **dup})

    # Step 3: Gather statistics
    info = {
        'filename': filename,
        'num_cells': len(parsed['cells']),
        'num_surfaces': len(parsed['surfaces']),
        'num_materials': len(parsed['materials']),
        'num_universes': len(universe_decls)
    }

    # Step 4: Generate report
    report = generate_validation_report(errors, warnings, info)

    return {
        'passed': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'report': report
    }
```
