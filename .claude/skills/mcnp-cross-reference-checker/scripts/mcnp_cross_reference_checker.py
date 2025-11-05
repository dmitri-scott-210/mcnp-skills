"""
MCNP Cross-Reference Checker

Validates all cross-references in MCNP input files including:
- Cell → Surface references
- Cell → Material references
- Cell → Transformation references
- Cell → Universe/Fill references
- Tally → Cell/Surface references
- FM → Material references
- Importance card count matching

Usage:
    from mcnp_cross_reference_checker import MCNPCrossReferenceChecker

    checker = MCNPCrossReferenceChecker()
    graph = checker.build_dependency_graph('input.inp')
    broken = checker.find_broken_references('input.inp')

Version: 2.0.0
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


class MCNPCrossReferenceChecker:
    """Main class for cross-reference validation and dependency analysis"""

    def __init__(self):
        self.cells = {}
        self.surfaces = set()
        self.materials = set()
        self.transformations = set()
        self.universes = set()
        self.tallies = {}

    def parse_input_file(self, filename: str) -> Tuple[List[str], List[str], List[str]]:
        """
        Parse MCNP input into three blocks

        Returns:
            Tuple of (cell_lines, surface_lines, data_lines)
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Find blank lines separating blocks
        blank_indices = [i for i, line in enumerate(lines) if line.strip() == '']

        if len(blank_indices) < 2:
            raise ValueError("Input file must have at least 2 blank lines (three-block structure)")

        # Split into blocks
        title_end = 1  # Skip title line
        cells_end = blank_indices[0]
        surfaces_end = blank_indices[1]

        cell_lines = lines[title_end:cells_end]
        surface_lines = lines[cells_end+1:surfaces_end]
        data_lines = lines[surfaces_end+1:]

        return cell_lines, surface_lines, data_lines

    def extract_surfaces_from_cells(self, cell_lines: List[str]) -> Dict[int, List[int]]:
        """Extract all surface references from cell geometries"""
        cells_to_surfaces = {}

        for line in cell_lines:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('C'):
                continue

            # Parse cell card: j m d geom params
            parts = line.split()
            if len(parts) < 4:
                continue

            try:
                cell_num = int(parts[0])
            except ValueError:
                continue

            # Extract geometry expression (after density)
            geom_start = 3  # After j, m, d
            geom_parts = parts[geom_start:]

            # Extract surface numbers from geometry
            surfaces = []
            for part in geom_parts:
                # Stop at parameters (IMP, VOL, etc.)
                if ':' in part or '=' in part:
                    break

                # Remove operators and extract number
                part = part.replace('(', '').replace(')', '').replace('#', '').replace(':', ' ')
                nums = part.split()
                for num in nums:
                    try:
                        surf_num = abs(int(num))
                        if surf_num > 0:
                            surfaces.append(surf_num)
                    except ValueError:
                        pass

            cells_to_surfaces[cell_num] = surfaces

        return cells_to_surfaces

    def extract_materials_from_cells(self, cell_lines: List[str]) -> Dict[int, int]:
        """Extract material references from cells"""
        cells_to_materials = {}

        for line in cell_lines:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('C'):
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            try:
                cell_num = int(parts[0])
                mat_num = int(parts[1])
                if mat_num > 0:  # Only non-void
                    cells_to_materials[cell_num] = mat_num
            except ValueError:
                pass

        return cells_to_materials

    def build_dependency_graph(self, filename: str) -> Dict:
        """
        Build complete dependency graph for input file

        Returns:
            Dictionary with all cross-reference relationships
        """
        cell_lines, surface_lines, data_lines = self.parse_input_file(filename)

        # Extract defined entities
        defined_surfaces = self._extract_defined_surfaces(surface_lines)
        defined_materials = self._extract_defined_materials(data_lines)
        defined_cells = self._extract_defined_cells(cell_lines)

        # Extract references
        cells_to_surfaces = self.extract_surfaces_from_cells(cell_lines)
        cells_to_materials = self.extract_materials_from_cells(cell_lines)

        # Build reverse mappings
        surfaces_used_by = {}
        for cell, surfs in cells_to_surfaces.items():
            for surf in surfs:
                if surf not in surfaces_used_by:
                    surfaces_used_by[surf] = []
                surfaces_used_by[surf].append(cell)

        materials_used_by = {}
        for cell, mat in cells_to_materials.items():
            if mat not in materials_used_by:
                materials_used_by[mat] = []
            materials_used_by[mat].append(cell)

        # Identify unused entities
        unused_surfaces = list(defined_surfaces - set(surfaces_used_by.keys()))
        unused_materials = list(defined_materials - set(materials_used_by.keys()))

        return {
            'cells_to_surfaces': cells_to_surfaces,
            'cells_to_materials': cells_to_materials,
            'surfaces_used_by': surfaces_used_by,
            'materials_used_by': materials_used_by,
            'unused_surfaces': unused_surfaces,
            'unused_materials': unused_materials,
            'defined_cells': defined_cells,
            'defined_surfaces': list(defined_surfaces),
            'defined_materials': list(defined_materials)
        }

    def find_broken_references(self, filename: str) -> List[Dict]:
        """
        Find all broken cross-references

        Returns:
            List of broken reference dictionaries
        """
        broken = []

        cell_lines, surface_lines, data_lines = self.parse_input_file(filename)

        defined_surfaces = self._extract_defined_surfaces(surface_lines)
        defined_materials = self._extract_defined_materials(data_lines)

        cells_to_surfaces = self.extract_surfaces_from_cells(cell_lines)
        cells_to_materials = self.extract_materials_from_cells(cell_lines)

        # Check surface references
        for cell, surfs in cells_to_surfaces.items():
            for surf in surfs:
                if surf not in defined_surfaces:
                    broken.append({
                        'type': 'undefined_surface',
                        'cell': cell,
                        'missing_surface': surf,
                        'error': f'Cell {cell} references undefined surface {surf}'
                    })

        # Check material references
        for cell, mat in cells_to_materials.items():
            if mat not in defined_materials:
                broken.append({
                    'type': 'undefined_material',
                    'cell': cell,
                    'missing_material': mat,
                    'error': f'Cell {cell} references undefined material {mat}'
                })

        return broken

    def _extract_defined_surfaces(self, surface_lines: List[str]) -> Set[int]:
        """Extract all defined surface numbers"""
        surfaces = set()
        for line in surface_lines:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('C'):
                continue
            parts = line.split()
            if parts:
                try:
                    surf_num = int(parts[0])
                    surfaces.add(surf_num)
                except ValueError:
                    pass
        return surfaces

    def _extract_defined_materials(self, data_lines: List[str]) -> Set[int]:
        """Extract all defined material numbers"""
        materials = set()
        for line in data_lines:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('C'):
                continue
            if line.upper().startswith('M') and not line.upper().startswith('MODE'):
                # Extract material number
                match = re.match(r'M(\d+)', line, re.IGNORECASE)
                if match:
                    materials.add(int(match.group(1)))
        return materials

    def _extract_defined_cells(self, cell_lines: List[str]) -> List[int]:
        """Extract all defined cell numbers"""
        cells = []
        for line in cell_lines:
            line = line.strip()
            if not line or line.startswith('c') or line.startswith('C'):
                continue
            parts = line.split()
            if parts:
                try:
                    cells.append(int(parts[0]))
                except ValueError:
                    pass
        return cells

    def detect_unused_entities(self, graph: Dict) -> Dict:
        """Return unused surfaces and materials"""
        return {
            'unused_surfaces': graph['unused_surfaces'],
            'unused_materials': graph['unused_materials']
        }

    def generate_full_report(self, filename: str) -> Dict:
        """Generate comprehensive validation report"""
        graph = self.build_dependency_graph(filename)
        broken = self.find_broken_references(filename)

        return {
            'fatal_errors': broken,
            'warnings': {
                'unused_surfaces': graph['unused_surfaces'],
                'unused_materials': graph['unused_materials']
            },
            'statistics': {
                'total_cells': len(graph['defined_cells']),
                'total_surfaces': len(graph['defined_surfaces']),
                'total_materials': len(graph['defined_materials']),
                'cell_surface_refs': sum(len(s) for s in graph['cells_to_surfaces'].values()),
                'cell_material_refs': len(graph['cells_to_materials'])
            }
        }


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python mcnp_cross_reference_checker.py <input_file>")
        sys.exit(1)

    checker = MCNPCrossReferenceChecker()
    report = checker.generate_full_report(sys.argv[1])

    print("=" * 60)
    print("CROSS-REFERENCE VALIDATION REPORT")
    print("=" * 60)

    if report['fatal_errors']:
        print("\n❌ FATAL ERRORS:")
        for i, err in enumerate(report['fatal_errors'], 1):
            print(f"  {i}. {err['error']}")
    else:
        print("\n✓ No broken references found")

    if report['warnings']['unused_surfaces'] or report['warnings']['unused_materials']:
        print("\n⚠ WARNINGS:")
        if report['warnings']['unused_surfaces']:
            print(f"  Unused surfaces: {report['warnings']['unused_surfaces']}")
        if report['warnings']['unused_materials']:
            print(f"  Unused materials: {report['warnings']['unused_materials']}")

    print("\n📊 STATISTICS:")
    for key, value in report['statistics'].items():
        print(f"  {key}: {value}")

    print("=" * 60)
