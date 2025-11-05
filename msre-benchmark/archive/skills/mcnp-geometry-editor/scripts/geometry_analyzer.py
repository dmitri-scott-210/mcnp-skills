#!/usr/bin/env python3
"""
MCNP Geometry Analyzer

Parses MCNP input files and analyzes geometry structure.
Identifies surfaces, cells, transformations, and relationships.

Usage:
    python geometry_analyzer.py input.i

Output:
    - List of all surfaces with types and parameters
    - List of all cells with material assignments
    - Transformation cards detected
    - Lattice structures identified
    - Bounding box calculations
"""

import re
import sys
from typing import Dict, List, Tuple

class MCNPGeometryAnalyzer:
    def __init__(self, filename: str):
        self.filename = filename
        self.surfaces = {}
        self.cells = {}
        self.transformations = {}
        self.lattices = {}
        self.title = ""

    def parse_input(self):
        """Parse MCNP input file into structured data"""
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        # Identify blocks
        self.title = lines[0].strip() if lines else ""

        # Find blank lines (block separators)
        blank_indices = [i for i, line in enumerate(lines) if line.strip() == '']

        if len(blank_indices) < 2:
            print("WARNING: Expected 2 blank lines (block separators), found", len(blank_indices))

        # Parse cells block
        cell_start = 1
        cell_end = blank_indices[0] if blank_indices else len(lines)
        self._parse_cells(lines[cell_start:cell_end])

        # Parse surfaces block
        if len(blank_indices) >= 1:
            surf_start = blank_indices[0] + 1
            surf_end = blank_indices[1] if len(blank_indices) >= 2 else len(lines)
            self._parse_surfaces(lines[surf_start:surf_end])

        # Parse data block
        if len(blank_indices) >= 2:
            data_start = blank_indices[1] + 1
            self._parse_data(lines[data_start:])

    def _parse_cells(self, lines: List[str]):
        """Parse cell cards"""
        for line in lines:
            if line.strip().startswith('c'):
                continue  # Skip comments
            if not line.strip():
                continue

            # Cell format: cell_num mat density geometry params
            match = re.match(r'^\s*(\d+)\s+(\d+|-?\d+)\s+([-+]?\d+\.?\d*[eE]?[-+]?\d*)', line)
            if match:
                cell_num = int(match.group(1))
                mat_num = int(match.group(2))
                density = float(match.group(3))

                # Check for LAT (lattice)
                is_lattice = 'LAT' in line.upper()

                # Check for FILL
                has_fill = 'FILL' in line.upper()

                # Check for TRCL
                trcl_match = re.search(r'TRCL[=\s]+(\d+)', line, re.IGNORECASE)
                trcl = int(trcl_match.group(1)) if trcl_match else None

                self.cells[cell_num] = {
                    'material': mat_num,
                    'density': density,
                    'is_lattice': is_lattice,
                    'has_fill': has_fill,
                    'trcl': trcl,
                    'line': line.strip()
                }

                if is_lattice:
                    self.lattices[cell_num] = line.strip()

    def _parse_surfaces(self, lines: List[str]):
        """Parse surface cards"""
        for line in lines:
            if line.strip().startswith('c'):
                continue
            if not line.strip():
                continue

            # Surface format: surf_num [TR_num] surf_type parameters
            parts = line.split()
            if len(parts) < 2:
                continue

            try:
                surf_num = int(parts[0])
            except ValueError:
                continue

            # Check if next is TR number or surface type
            tr_num = None
            surf_type_idx = 1

            if len(parts) > 2:
                try:
                    potential_tr = int(parts[1])
                    tr_num = potential_tr
                    surf_type_idx = 2
                except ValueError:
                    pass

            surf_type = parts[surf_type_idx] if surf_type_idx < len(parts) else 'UNKNOWN'
            params = parts[surf_type_idx+1:] if surf_type_idx+1 < len(parts) else []

            self.surfaces[surf_num] = {
                'type': surf_type,
                'tr': tr_num,
                'parameters': params,
                'line': line.strip()
            }

    def _parse_data(self, lines: List[str]):
        """Parse data cards, looking for TR cards"""
        for line in lines:
            if line.strip().startswith('*TR') or line.strip().startswith('TR'):
                # Transformation card
                match = re.match(r'^\*?TR(\d+)', line, re.IGNORECASE)
                if match:
                    tr_num = int(match.group(1))
                    self.transformations[tr_num] = line.strip()

    def print_summary(self):
        """Print analysis summary"""
        print("=" * 60)
        print(f"MCNP Geometry Analysis: {self.filename}")
        print("=" * 60)
        print(f"\nTitle: {self.title}\n")

        print(f"Cells: {len(self.cells)}")
        print(f"Surfaces: {len(self.surfaces)}")
        print(f"Transformations: {len(self.transformations)}")
        print(f"Lattices: {len(self.lattices)}")

        print("\n" + "-" * 60)
        print("CELLS")
        print("-" * 60)
        for cell_num in sorted(self.cells.keys()):
            cell = self.cells[cell_num]
            print(f"Cell {cell_num}: mat={cell['material']}, rho={cell['density']}", end="")
            if cell['is_lattice']:
                print(" [LATTICE]", end="")
            if cell['has_fill']:
                print(" [FILL]", end="")
            if cell['trcl']:
                print(f" [TRCL={cell['trcl']}]", end="")
            print()

        print("\n" + "-" * 60)
        print("SURFACES")
        print("-" * 60)
        for surf_num in sorted(self.surfaces.keys()):
            surf = self.surfaces[surf_num]
            print(f"Surface {surf_num}: {surf['type']}", end="")
            if surf['tr']:
                print(f" [TR={surf['tr']}]", end="")
            print(f" params={' '.join(surf['parameters'])}")

        if self.transformations:
            print("\n" + "-" * 60)
            print("TRANSFORMATIONS")
            print("-" * 60)
            for tr_num in sorted(self.transformations.keys()):
                print(f"TR{tr_num}: {self.transformations[tr_num]}")

        if self.lattices:
            print("\n" + "-" * 60)
            print("LATTICE STRUCTURES")
            print("-" * 60)
            for cell_num in sorted(self.lattices.keys()):
                print(f"Cell {cell_num} (lattice):")
                print(f"  {self.lattices[cell_num]}")

    def get_surface_types(self) -> Dict[str, int]:
        """Count surface types"""
        types = {}
        for surf in self.surfaces.values():
            surf_type = surf['type']
            types[surf_type] = types.get(surf_type, 0) + 1
        return types

    def get_bounding_box_estimate(self) -> Tuple[float, float, float, float, float, float]:
        """Estimate bounding box from simple surfaces"""
        xmin, xmax = float('inf'), float('-inf')
        ymin, ymax = float('inf'), float('-inf')
        zmin, zmax = float('inf'), float('-inf')

        for surf in self.surfaces.values():
            surf_type = surf['type'].upper()
            params = surf['parameters']

            try:
                if surf_type == 'PX' and len(params) >= 1:
                    x = float(params[0])
                    xmin, xmax = min(xmin, x), max(xmax, x)
                elif surf_type == 'PY' and len(params) >= 1:
                    y = float(params[0])
                    ymin, ymax = min(ymin, y), max(ymax, y)
                elif surf_type == 'PZ' and len(params) >= 1:
                    z = float(params[0])
                    zmin, zmax = min(zmin, z), max(zmax, z)
                elif surf_type == 'RPP' and len(params) >= 6:
                    xmin = min(xmin, float(params[0]))
                    xmax = max(xmax, float(params[1]))
                    ymin = min(ymin, float(params[2]))
                    ymax = max(ymax, float(params[3]))
                    zmin = min(zmin, float(params[4]))
                    zmax = max(zmax, float(params[5]))
            except (ValueError, IndexError):
                continue

        return (xmin, xmax, ymin, ymax, zmin, zmax)

def main():
    if len(sys.argv) < 2:
        print("Usage: python geometry_analyzer.py input.i")
        sys.exit(1)

    filename = sys.argv[1]

    analyzer = MCNPGeometryAnalyzer(filename)
    analyzer.parse_input()
    analyzer.print_summary()

    print("\n" + "-" * 60)
    print("SURFACE TYPE DISTRIBUTION")
    print("-" * 60)
    types = analyzer.get_surface_types()
    for surf_type, count in sorted(types.items()):
        print(f"{surf_type}: {count}")

    print("\n" + "-" * 60)
    print("BOUNDING BOX ESTIMATE")
    print("-" * 60)
    bbox = analyzer.get_bounding_box_estimate()
    if all(x != float('inf') and x != float('-inf') for x in bbox):
        print(f"X: [{bbox[0]:.2f}, {bbox[1]:.2f}]")
        print(f"Y: [{bbox[2]:.2f}, {bbox[3]:.2f}]")
        print(f"Z: [{bbox[4]:.2f}, {bbox[5]:.2f}]")
    else:
        print("Could not determine bounding box from available surfaces")

if __name__ == '__main__':
    main()
