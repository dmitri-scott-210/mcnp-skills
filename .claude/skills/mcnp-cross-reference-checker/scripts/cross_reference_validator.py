#!/usr/bin/env python3
"""
MCNP Cross-Reference Validator
Validates cell → surface, cell → material, and cell → universe references
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

class MCNPValidator:
    """
    Main validation class for MCNP cross-references
    """

    def __init__(self, input_file: str):
        self.input_file = input_file
        self.cells = {}
        self.surfaces = set()
        self.materials = set()
        self.universes = set()
        self.errors = []
        self.warnings = []

    def parse_input(self):
        """Parse MCNP input file into structured data"""
        with open(self.input_file) as f:
            lines = f.readlines()

        # Split into blocks
        cells_block = []
        surfaces_block = []
        data_block = []

        current_block = cells_block
        blank_count = 0

        for line_num, line in enumerate(lines, 1):
            # Skip pure comment lines
            if line.strip().startswith(('c ', 'C ', 'c\t', 'C\t')):
                continue

            # Detect blank line
            if line.strip() == '':
                blank_count += 1
                if blank_count == 1:
                    current_block = surfaces_block
                elif blank_count == 2:
                    current_block = data_block
                continue

            current_block.append((line_num, line))

        # Parse each block
        self._parse_cells(cells_block)
        self._parse_surfaces(surfaces_block)
        self._parse_materials(data_block)

    def _parse_cells(self, cells_block):
        """Extract cell information"""
        for line_num, line in cells_block:
            # Remove inline comments
            if '$' in line:
                line = line.split('$')[0]

            parts = line.split()
            if len(parts) < 3:
                continue

            try:
                cell_id = int(parts[0])
                material_id = int(parts[1])

                # Extract surfaces from geometry
                surfaces = self._extract_surfaces(line)

                # Extract universe if present
                universe = self._extract_universe(line)

                # Extract fill if present
                fill = self._extract_fill(line)

                self.cells[cell_id] = {
                    'line': line_num,
                    'material': material_id,
                    'surfaces': surfaces,
                    'universe': universe,
                    'fill': fill,
                    'text': line.strip()
                }

                if universe is not None:
                    self.universes.add(universe)

            except (ValueError, IndexError):
                continue

    def _extract_surfaces(self, cell_line: str) -> List[int]:
        """Extract surface IDs from cell Boolean expression"""
        # Remove cell ID, material, density
        parts = cell_line.split()
        if len(parts) < 4:
            return []

        # Geometry starts at 4th position
        geometry = ' '.join(parts[3:])

        # Remove options (u=, imp=, vol=, fill=, etc.)
        geometry = re.split(r'\s+(u=|imp:|vol=|fill=|lat=)', geometry)[0]

        # Extract all surface IDs (numbers with optional +/-)
        matches = re.findall(r'[+-]?\d+', geometry)

        # Convert to absolute values (remove signs), convert to int
        surface_ids = [abs(int(m)) for m in matches if m]

        # Remove duplicates
        return list(set(surface_ids))

    def _extract_universe(self, cell_line: str) -> int:
        """Extract universe ID from u= specification"""
        match = re.search(r'\bu=(\d+)', cell_line)
        if match:
            return int(match.group(1))
        return None

    def _extract_fill(self, cell_line: str) -> List[int]:
        """Extract universe ID(s) from fill= specification"""
        match = re.search(r'\bfill=([^\s]+)', cell_line)
        if not match:
            return None

        fill_str = match.group(1)

        # Check if it's a simple fill (single number) or lattice fill
        if fill_str.isdigit():
            return [int(fill_str)]

        # For lattice fill, would need to parse full array
        # Simplified: extract all numbers from fill specification
        numbers = re.findall(r'\d+', fill_str)
        return [int(n) for n in numbers]

    def _parse_surfaces(self, surfaces_block):
        """Extract surface IDs"""
        for line_num, line in surfaces_block:
            if '$' in line:
                line = line.split('$')[0]

            parts = line.split()
            if len(parts) < 2:
                continue

            # Check if line starts with asterisk (reflecting surface)
            if parts[0].startswith('*'):
                surf_id_str = parts[0][1:]
            else:
                surf_id_str = parts[0]

            try:
                surf_id = int(surf_id_str)
                self.surfaces.add(surf_id)
            except ValueError:
                continue

    def _parse_materials(self, data_block):
        """Extract material IDs"""
        for line_num, line in data_block:
            if '$' in line:
                line = line.split('$')[0]

            # Material cards start with 'm' or 'M'
            if line.strip().lower().startswith('m'):
                # Extract material number
                match = re.match(r'[mM](\d+)', line.strip())
                if match:
                    mat_id = int(match.group(1))
                    self.materials.add(mat_id)

    def validate_cell_surfaces(self):
        """Check that all surfaces referenced by cells are defined"""
        for cell_id, cell_data in self.cells.items():
            for surf_id in cell_data['surfaces']:
                if surf_id not in self.surfaces:
                    self.errors.append({
                        'type': 'undefined_surface',
                        'cell_id': cell_id,
                        'surface_id': surf_id,
                        'line': cell_data['line'],
                        'message': f"Cell {cell_id} references undefined surface {surf_id}"
                    })

    def validate_cell_materials(self):
        """Check that all materials referenced by cells are defined"""
        for cell_id, cell_data in self.cells.items():
            material_id = cell_data['material']

            # Skip void cells (material 0)
            if material_id == 0:
                continue

            if material_id not in self.materials:
                self.errors.append({
                    'type': 'undefined_material',
                    'cell_id': cell_id,
                    'material_id': material_id,
                    'line': cell_data['line'],
                    'message': f"Cell {cell_id} references undefined material {material_id}"
                })

    def validate_universes(self):
        """Check that all filled universes are declared"""
        filled_universes = set()

        for cell_id, cell_data in self.cells.items():
            if cell_data['fill']:
                filled_universes.update(cell_data['fill'])

        for u_id in filled_universes:
            if u_id not in self.universes and u_id != 0:
                self.errors.append({
                    'type': 'undefined_universe',
                    'universe_id': u_id,
                    'message': f"Universe {u_id} is filled but not declared (no cells with u={u_id})"
                })

    def detect_circular_universes(self):
        """Detect circular universe references"""
        # Build fill graph
        fill_graph = {}
        for cell_id, cell_data in self.cells.items():
            parent_u = cell_data['universe'] if cell_data['universe'] else 0

            if parent_u not in fill_graph:
                fill_graph[parent_u] = []

            if cell_data['fill']:
                fill_graph[parent_u].extend(cell_data['fill'])

        # DFS cycle detection
        def has_cycle(node, visited, rec_stack, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            cycles_found = []

            for neighbor in fill_graph.get(node, []):
                if neighbor not in visited:
                    cycles_found.extend(has_cycle(neighbor, visited, rec_stack, path[:]))
                elif neighbor in rec_stack:
                    # Cycle found
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles_found.append(cycle)

            rec_stack.remove(node)
            return cycles_found

        visited = set()
        all_cycles = []

        for universe in fill_graph:
            if universe not in visited:
                cycles = has_cycle(universe, visited, set(), [])
                for cycle in cycles:
                    self.errors.append({
                        'type': 'circular_universe',
                        'cycle': cycle,
                        'message': f"Circular universe reference: {' → '.join(map(str, cycle))}"
                    })

    def check_duplicates(self):
        """Check for duplicate entity IDs"""
        # Check duplicate cell IDs (already unique in dict, but track line numbers)
        cell_lines = {}
        for cell_id, cell_data in self.cells.items():
            if cell_id not in cell_lines:
                cell_lines[cell_id] = []
            cell_lines[cell_id].append(cell_data['line'])

        for cell_id, lines in cell_lines.items():
            if len(lines) > 1:
                self.errors.append({
                    'type': 'duplicate_cell',
                    'cell_id': cell_id,
                    'lines': lines,
                    'message': f"Duplicate cell ID {cell_id} at lines {lines}"
                })

    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("=" * 70)
        report.append("MCNP CROSS-REFERENCE VALIDATION REPORT")
        report.append(f"File: {self.input_file}")
        report.append("=" * 70)
        report.append("")

        # Section 1: Fatal Errors
        report.append("SECTION 1: FATAL ERRORS")
        report.append("-" * 70)
        if self.errors:
            for i, error in enumerate(self.errors, 1):
                report.append(f"[{i}] {error['message']}")
                if 'line' in error:
                    report.append(f"    Location: Line {error['line']}")
                report.append("")
        else:
            report.append("✓ No fatal errors detected")
            report.append("")

        # Section 2: Warnings
        report.append("SECTION 2: WARNINGS")
        report.append("-" * 70)
        if self.warnings:
            for i, warning in enumerate(self.warnings, 1):
                report.append(f"[{i}] {warning['message']}")
                report.append("")
        else:
            report.append("✓ No warnings")
            report.append("")

        # Section 3: Statistics
        report.append("SECTION 3: STATISTICS")
        report.append("-" * 70)
        report.append(f"Total cells:     {len(self.cells)}")
        report.append(f"Total surfaces:  {len(self.surfaces)}")
        report.append(f"Total materials: {len(self.materials)}")
        report.append(f"Total universes: {len(self.universes)}")
        report.append("")

        # Section 4: Summary
        report.append("SECTION 4: SUMMARY")
        report.append("-" * 70)
        if self.errors:
            report.append(f"❌ VALIDATION FAILED: {len(self.errors)} fatal error(s)")
            report.append("   Input file will NOT run successfully in MCNP")
        else:
            report.append("✅ VALIDATION PASSED")
            report.append("   No fatal cross-reference errors detected")
        report.append("")
        report.append("=" * 70)

        return "\n".join(report)

    def validate(self) -> bool:
        """Run all validation checks"""
        self.parse_input()

        self.validate_cell_surfaces()
        self.validate_cell_materials()
        self.validate_universes()
        self.detect_circular_universes()
        self.check_duplicates()

        return len(self.errors) == 0


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python cross_reference_validator.py <mcnp_input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not Path(input_file).exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)

    print(f"Validating {input_file}...")
    print()

    validator = MCNPValidator(input_file)
    passed = validator.validate()

    report = validator.generate_report()
    print(report)

    # Write report to file
    report_file = Path(input_file).stem + "_validation_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"Report saved to: {report_file}")

    # Exit code: 0 = pass, 1 = fail
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
