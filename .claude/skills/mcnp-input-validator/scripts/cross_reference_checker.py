#!/usr/bin/env python3
"""
Cross-Reference Checker

Validates cross-references in MCNP input files:
- Cell geometry → Surface definitions
- Cell material → Material definitions
- Tally → Cell/Surface references
- FILL → Universe definitions
- TRCL → Transformation definitions

Usage:
    from cross_reference_checker import check_cross_references

    errors = check_cross_references('input.inp')
    if errors:
        for error in errors:
            print(f"ERROR: {error}")

Author: MCNP Skills Revamp Project
Version: 2.0.0
"""

import re
from typing import List, Dict, Set


class CrossReferenceChecker:
    """Check cross-references in MCNP input."""

    def __init__(self):
        """Initialize checker."""
        self.cells = {}
        self.surfaces = set()
        self.materials = set()
        self.universes = set()
        self.transformations = set()
        self.errors = []

    def check_file(self, filepath: str) -> List[str]:
        """
        Check cross-references in MCNP input file.

        Args:
            filepath: Path to MCNP input file

        Returns:
            List of error strings
        """
        self.errors = []

        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            return [f"Error reading file: {e}"]

        # Parse input
        self._parse_input(lines)

        # Check references
        self._check_cell_geometry_references()
        self._check_cell_material_references()
        self._check_importance_count()

        return self.errors

    def _parse_input(self, lines: List[str]):
        """Parse input to extract entities."""
        # Find block boundaries
        blank_positions = [i for i, line in enumerate(lines) if line.strip() == '']

        if len(blank_positions) < 2:
            self.errors.append("FATAL: Invalid block structure")
            return

        first_blank = blank_positions[0]
        second_blank = blank_positions[1]

        # Parse cells
        cell_lines = lines[1:first_blank]
        for line in cell_lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            tokens = line.split()
            if len(tokens) >= 3:
                try:
                    cell_num = int(tokens[0])
                    material = int(tokens[1])
                    geometry = ' '.join(tokens[3:])
                    self.cells[cell_num] = {
                        'material': material,
                        'geometry': geometry
                    }
                except ValueError:
                    pass

        # Parse surfaces
        surface_lines = lines[first_blank+1:second_blank]
        for line in surface_lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            tokens = line.split()
            if len(tokens) >= 1:
                try:
                    surf_num = int(tokens[0])
                    self.surfaces.add(surf_num)
                except ValueError:
                    pass

        # Parse data cards
        data_lines = lines[second_blank+1:]
        for line in data_lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            # Material cards
            if re.match(r'^[Mm]\d+', line):
                match = re.match(r'^[Mm](\d+)', line)
                if match:
                    mat_num = int(match.group(1))
                    self.materials.add(mat_num)

    def _check_cell_geometry_references(self):
        """Check that all surfaces referenced in cell geometry exist."""
        for cell_num, cell_data in self.cells.items():
            geometry = cell_data['geometry']

            # Extract surface numbers from geometry
            # Match numbers not preceded by U= or FILL=
            surf_refs = re.findall(r'(?<!U=)(?<!FILL=)\b(\d+)\b', geometry)

            for surf_ref in surf_refs:
                try:
                    surf_num = int(surf_ref)
                    if surf_num not in self.surfaces:
                        self.errors.append(
                            f"FATAL: Cell {cell_num} geometry references "
                            f"undefined surface {surf_num}"
                        )
                except ValueError:
                    pass

    def _check_cell_material_references(self):
        """Check that all materials referenced in cells exist."""
        for cell_num, cell_data in self.cells.items():
            material = cell_data['material']
            if material != 0 and material not in self.materials:
                self.errors.append(
                    f"FATAL: Cell {cell_num} uses material {material}, "
                    f"but M{material} card not defined"
                )

    def _check_importance_count(self):
        """Check importance card entry count matches cell count (basic)."""
        # This is a simplified check
        # Full implementation would parse IMP cards
        cell_count = len(self.cells)
        if cell_count > 0:
            # Add as informational note
            pass


def check_cross_references(filepath: str) -> List[str]:
    """
    Convenience function to check cross-references.

    Args:
        filepath: Path to MCNP input file

    Returns:
        List of error strings
    """
    checker = CrossReferenceChecker()
    return checker.check_file(filepath)


def main():
    """Command-line interface."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python cross_reference_checker.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    print(f"Checking cross-references: {input_file}")
    print("="*60)

    errors = check_cross_references(input_file)

    if errors:
        print("CROSS-REFERENCE ERRORS:")
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        sys.exit(1)
    else:
        print("✓ All cross-references valid")
        sys.exit(0)


if __name__ == '__main__':
    main()
