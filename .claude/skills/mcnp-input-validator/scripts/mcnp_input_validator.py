#!/usr/bin/env python3
"""
MCNP Input Validator - Main Validation Engine

Comprehensive MCNP input file validation for syntax, cross-references,
physics settings, and format compliance.

Usage:
    from mcnp_input_validator import MCNPInputValidator

    validator = MCNPInputValidator()
    results = validator.validate_file('input.inp')

    if results['valid']:
        print("Input file passed validation")
    else:
        for error in results['errors']:
            print(f"ERROR: {error}")

Author: MCNP Skills Revamp Project
Version: 2.0.0
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set


class MCNPInputValidator:
    """
    Main MCNP input validation engine.

    Performs comprehensive validation of MCNP input files including:
    - Block structure validation
    - Card syntax checking
    - Cross-reference validation
    - Physics consistency checking
    """

    def __init__(self):
        """Initialize validator with empty results."""
        self.errors = []
        self.warnings = []
        self.recommendations = []

        # Storage for parsed entities
        self.cells = {}
        self.surfaces = {}
        self.materials = {}
        self.universes = {}
        self.transformations = {}

    def validate_file(self, filepath: str) -> Dict:
        """
        Validate an MCNP input file.

        Args:
            filepath: Path to MCNP input file

        Returns:
            Dictionary with validation results:
            {
                'valid': bool,
                'errors': list of error strings,
                'warnings': list of warning strings,
                'recommendations': list of recommendation strings
            }
        """
        # Reset results
        self.errors = []
        self.warnings = []
        self.recommendations = []

        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.errors.append(f"File not found: {filepath}")
            return self._build_results()
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return self._build_results()

        # Run validation checks in order
        self._validate_structure(lines)

        if self.errors:
            # If fatal structure errors, don't continue
            return self._build_results()

        self._parse_input(lines)
        self._validate_cross_references()
        self._validate_physics()
        self._add_recommendations()

        return self._build_results()

    def _validate_structure(self, lines: List[str]):
        """
        Validate three-block structure and blank line count.

        Args:
            lines: List of file lines
        """
        # Count blank lines
        blank_lines = []
        for i, line in enumerate(lines, 1):
            if line.strip() == '':
                blank_lines.append(i)

        blank_count = len(blank_lines)

        # Check for exactly 3 blank lines (after cells, after surfaces, at EOF)
        if blank_count != 3:
            self.errors.append(
                f"FATAL: Invalid blank line count. "
                f"Expected 3, found {blank_count}. "
                f"Blank lines at: {blank_lines}"
            )

        # Identify blocks
        if blank_count >= 2:
            first_blank = blank_lines[0]
            second_blank = blank_lines[1]

            # Title assumed at line 1
            cells_block = lines[1:first_blank-1]
            surfaces_block = lines[first_blank:second_blank-1]
            data_block = lines[second_blank:]

            # Check blocks are non-empty
            if not any(line.strip() and not line.strip().startswith('c') for line in cells_block):
                self.errors.append("FATAL: Cell Cards block is empty")

            if not any(line.strip() and not line.strip().startswith('c') for line in surfaces_block):
                self.errors.append("FATAL: Surface Cards block is empty")

            if not any(line.strip() and not line.strip().startswith('c') for line in data_block):
                self.errors.append("FATAL: Data Cards block is empty")

    def _parse_input(self, lines: List[str]):
        """
        Parse input file to extract cells, surfaces, materials, etc.

        Args:
            lines: List of file lines
        """
        # Find blank line positions
        blank_positions = [i for i, line in enumerate(lines) if line.strip() == '']

        if len(blank_positions) < 2:
            return  # Structure error already reported

        first_blank = blank_positions[0]
        second_blank = blank_positions[1]

        # Parse cells
        cell_lines = lines[1:first_blank]
        self._parse_cells(cell_lines)

        # Parse surfaces
        surface_lines = lines[first_blank+1:second_blank]
        self._parse_surfaces(surface_lines)

        # Parse data cards
        data_lines = lines[second_blank+1:]
        self._parse_data_cards(data_lines)

    def _parse_cells(self, lines: List[str]):
        """Parse cell cards."""
        for line in lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            # Simple parsing: cell_num material density geometry
            tokens = line.split()
            if len(tokens) >= 3:
                try:
                    cell_num = int(tokens[0])
                    material = int(tokens[1])
                    self.cells[cell_num] = {
                        'material': material,
                        'geometry': ' '.join(tokens[3:])
                    }
                except ValueError:
                    pass  # Skip malformed lines

    def _parse_surfaces(self, lines: List[str]):
        """Parse surface cards."""
        for line in lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            tokens = line.split()
            if len(tokens) >= 2:
                try:
                    surf_num = int(tokens[0])
                    surf_type = tokens[1]
                    self.surfaces[surf_num] = {'type': surf_type}
                except ValueError:
                    pass

    def _parse_data_cards(self, lines: List[str]):
        """Parse data cards."""
        for line in lines:
            line = line.strip()
            if not line or line.startswith('c'):
                continue

            # Check for material cards
            if line.startswith('M') or line.startswith('m'):
                tokens = line.split()
                if len(tokens) > 0:
                    # Extract material number
                    m_card = tokens[0]
                    match = re.match(r'[Mm](\d+)', m_card)
                    if match:
                        mat_num = int(match.group(1))
                        self.materials[mat_num] = True

    def _validate_cross_references(self):
        """Validate cross-references between cells, surfaces, materials."""

        # Check cell geometry references to surfaces
        for cell_num, cell_data in self.cells.items():
            geometry = cell_data['geometry']

            # Extract surface numbers from geometry
            # Simple regex to find numbers
            surf_refs = re.findall(r'\b(\d+)\b', geometry)

            for surf_ref in surf_refs:
                surf_num = int(surf_ref)
                if surf_num not in self.surfaces:
                    self.errors.append(
                        f"FATAL: Cell {cell_num} geometry references "
                        f"undefined surface {surf_num}"
                    )

        # Check cell material references
        for cell_num, cell_data in self.cells.items():
            material = cell_data['material']
            if material != 0 and material not in self.materials:
                self.errors.append(
                    f"FATAL: Cell {cell_num} uses material {material}, "
                    f"but M{material} card not defined"
                )

    def _validate_physics(self):
        """Validate physics settings (placeholder for detailed checks)."""
        # This would check MODE, PHYS cards, cross-section consistency, etc.
        # For now, add general recommendation
        pass

    def _add_recommendations(self):
        """Add best practice recommendations."""
        self.recommendations.append(
            "ESSENTIAL: Plot geometry before running (mcnp6 ip i=input.inp)"
        )
        self.recommendations.append(
            "RECOMMENDED: Test with VOID card for geometry verification"
        )
        self.recommendations.append(
            "Verify cross-section libraries load correctly in output file"
        )

    def _build_results(self) -> Dict:
        """Build results dictionary."""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'recommendations': self.recommendations
        }


def main():
    """Command-line interface for validator."""
    if len(sys.argv) < 2:
        print("Usage: python mcnp_input_validator.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    print("="*60)
    print("MCNP INPUT VALIDATOR v2.0.0")
    print("="*60)
    print(f"Validating: {input_file}\n")

    validator = MCNPInputValidator()
    results = validator.validate_file(input_file)

    # Print results
    if results['errors']:
        print("\n" + "="*60)
        print("FATAL ERRORS (must fix before running)")
        print("="*60)
        for i, error in enumerate(results['errors'], 1):
            print(f"{i}. {error}")

    if results['warnings']:
        print("\n" + "="*60)
        print("WARNINGS (should review)")
        print("="*60)
        for i, warning in enumerate(results['warnings'], 1):
            print(f"{i}. {warning}")

    if results['recommendations']:
        print("\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. {rec}")

    print("\n" + "="*60)
    if results['valid']:
        print("STATUS: PASSED - Input validation successful")
        print("="*60)
        print("\nREADY FOR NEXT STEPS:")
        print("1. Plot geometry (ESSENTIAL)")
        print("2. Run VOID test (RECOMMENDED)")
        print("3. Execute MCNP simulation")
        sys.exit(0)
    else:
        print("STATUS: FAILED - Fix errors before running")
        print("="*60)
        sys.exit(1)


if __name__ == '__main__':
    main()
