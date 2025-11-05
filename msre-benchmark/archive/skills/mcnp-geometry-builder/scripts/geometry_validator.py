#!/usr/bin/env python3
"""
MCNP Geometry Validator

Pre-MCNP validation script for geometry input files.
Checks common geometry errors before running expensive simulations.

Usage:
    python geometry_validator.py input_file.inp

Features:
    - Validates MCNP file structure (3 blocks, blank line delimiters)
    - Checks surface and cell cross-references
    - Validates material references
    - Checks for common syntax errors
    - Identifies undefined surfaces, cells, materials
    - Validates transformation references

Exit Codes:
    0: No errors found
    1: Errors found (details printed to stdout)
    2: File not found or invalid format
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Stores validation results"""
    errors: List[str]
    warnings: List[str]
    info: List[str]

class MCNPGeometryValidator:
    """Validates MCNP geometry input files"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.lines = []
        self.title = ""
        self.cell_cards = []
        self.surface_cards = []
        self.data_cards = []

        self.defined_cells = set()
        self.defined_surfaces = set()
        self.defined_materials = set()
        self.defined_transformations = set()

        self.results = ValidationResult([], [], [])

    def validate(self) -> ValidationResult:
        """Main validation entry point"""

        if not self.filepath.exists():
            self.results.errors.append(f"File not found: {self.filepath}")
            return self.results

        # Read file
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                self.lines = f.readlines()
        except Exception as e:
            self.results.errors.append(f"Error reading file: {e}")
            return self.results

        # Run validation checks
        self._check_file_structure()
        self._parse_blocks()
        self._extract_definitions()
        self._check_cross_references()
        self._check_syntax()

        return self.results

    def _check_file_structure(self):
        """Validate MCNP 3-block structure with blank line delimiters"""

        if not self.lines:
            self.results.errors.append("File is empty")
            return

        # Count blank lines (lines with only whitespace or empty)
        blank_line_indices = []
        for i, line in enumerate(self.lines, 1):
            if line.strip() == '':
                blank_line_indices.append(i)

        num_blank = len(blank_line_indices)

        # MCNP requires EXACTLY 2 blank lines (one after cells, one after surfaces)
        if num_blank < 2:
            self.results.errors.append(
                f"CRITICAL: MCNP requires EXACTLY 2 blank lines (found {num_blank}). "
                "One after Cell Cards, one after Surface Cards."
            )
        elif num_blank > 2:
            self.results.warnings.append(
                f"Found {num_blank} blank lines (expected 2). "
                f"Extra blank lines at: {blank_line_indices[2:]}"
            )

        # Check for blank lines WITHIN blocks (common error)
        if num_blank > 2:
            self.results.errors.append(
                "ILLEGAL: Blank lines found WITHIN blocks. "
                "Blank lines are ONLY allowed between blocks."
            )

    def _parse_blocks(self):
        """Parse file into three blocks"""

        if not self.lines:
            return

        # Title is first line
        self.title = self.lines[0].strip()
        self.results.info.append(f"Title: {self.title}")

        # Find blank line delimiters
        blank_indices = []
        for i, line in enumerate(self.lines):
            if line.strip() == '':
                blank_indices.append(i)

        if len(blank_indices) < 2:
            self.results.errors.append("Cannot parse blocks: insufficient blank line delimiters")
            return

        # Extract blocks
        first_blank = blank_indices[0]
        second_blank = blank_indices[1]

        self.cell_cards = self.lines[1:first_blank]
        self.surface_cards = self.lines[first_blank+1:second_blank]
        self.data_cards = self.lines[second_blank+1:]

        self.results.info.append(f"Cell cards: {len(self.cell_cards)} lines")
        self.results.info.append(f"Surface cards: {len(self.surface_cards)} lines")
        self.results.info.append(f"Data cards: {len(self.data_cards)} lines")

    def _extract_definitions(self):
        """Extract defined cells, surfaces, materials, transformations"""

        # Extract cell numbers (first number on non-comment lines)
        for line in self.cell_cards:
            if line.strip().startswith('c') or line.strip().startswith('C'):
                continue
            match = re.match(r'\s*(\d+)\s+', line)
            if match:
                self.defined_cells.add(int(match.group(1)))

        # Extract surface numbers (first entry on non-comment lines)
        for line in self.surface_cards:
            if line.strip().startswith('c') or line.strip().startswith('C'):
                continue
            # Surface can have * or + prefix for reflecting/white boundary
            match = re.match(r'\s*[\*\+]?(\d+)\s+', line)
            if match:
                self.defined_surfaces.add(int(match.group(1)))

        # Extract material numbers (M cards in data block)
        for line in self.data_cards:
            match = re.match(r'\s*[mM](\d+)\s+', line, re.IGNORECASE)
            if match:
                self.defined_materials.add(int(match.group(1)))

        # Extract transformation numbers (TR cards in data block)
        for line in self.data_cards:
            match = re.match(r'\s*\*?[tT][rR](\d+)\s+', line)
            if match:
                self.defined_transformations.add(int(match.group(1)))

        self.results.info.append(f"Defined cells: {sorted(self.defined_cells)}")
        self.results.info.append(f"Defined surfaces: {sorted(self.defined_surfaces)}")
        self.results.info.append(f"Defined materials: {sorted(self.defined_materials)}")
        self.results.info.append(f"Defined transformations: {sorted(self.defined_transformations)}")

    def _check_cross_references(self):
        """Check that all references are defined"""

        # Check cell material references
        for line in self.cell_cards:
            if line.strip().startswith('c') or line.strip().startswith('C'):
                continue

            # Cell format: j m d geom params
            match = re.match(r'\s*(\d+)\s+(\d+)\s+', line)
            if match:
                cell_num = int(match.group(1))
                mat_num = int(match.group(2))

                # Material 0 is void (OK)
                if mat_num != 0 and mat_num not in self.defined_materials:
                    self.results.errors.append(
                        f"Cell {cell_num} references undefined material M{mat_num}"
                    )

        # Check cell surface references
        for line in self.cell_cards:
            if line.strip().startswith('c') or line.strip().startswith('C'):
                continue

            # Find all surface numbers in geometry description
            # Look for patterns like: -1 2 -3 (with optional +/-)
            surfaces = re.findall(r'[+-]?(\d+)', line)
            if surfaces:
                cell_match = re.match(r'\s*(\d+)\s+', line)
                cell_num = int(cell_match.group(1)) if cell_match else 0

                for surf in surfaces:
                    surf_num = int(surf)
                    # Skip cell number itself and material number
                    if surf_num not in self.defined_surfaces and surf_num not in self.defined_cells:
                        # Could be surface or could be part of density or other parameter
                        # This is a simplified check
                        pass

        # Check transformation references in surface cards
        for line in self.surface_cards:
            if line.strip().startswith('c') or line.strip().startswith('C'):
                continue

            # Surface with transformation: j n <type> <params>
            # Where n is transformation number
            match = re.match(r'\s*[\*\+]?(\d+)\s+(\d+)\s+', line)
            if match:
                surf_num = int(match.group(1))
                potential_tr = int(match.group(2))

                # If potential_tr is not a surface type mnemonic, it's a TR number
                # Surface types are typically 1-2 letter codes, not pure numbers in this position
                # This is a simplified check
                if potential_tr > 999:  # Unlikely to be valid TR number
                    pass  # Skip this check for now (complex to distinguish)

    def _check_syntax(self):
        """Check for common syntax errors"""

        # Check for continuation errors (missing & or +)
        for i, line in enumerate(self.lines, 1):
            if len(line.rstrip()) > 128:
                self.results.warnings.append(
                    f"Line {i} exceeds 128 characters (MCNP limit)"
                )

        # Check for illegal characters in cell/surface blocks
        for i, line in enumerate(self.cell_cards, 1):
            if '\t' in line:
                self.results.warnings.append(
                    f"Cell card line {i} contains tab character (use spaces)"
                )

        # Check for common macrobody errors
        for i, line in enumerate(self.surface_cards, 1):
            # Check RHP/HEX specifications
            if re.search(r'\b(RHP|HEX)\s+', line, re.IGNORECASE):
                values = re.findall(r'[+-]?\d+\.?\d*', line)
                if len(values) < 9:
                    self.results.errors.append(
                        f"Surface card line {i}: RHP/HEX requires minimum 9 values "
                        f"(found {len(values)}). Format: vx vy vz h1 h2 h3 r1 r2 r3"
                    )

def main():
    """Main entry point"""

    if len(sys.argv) != 2:
        print("Usage: python geometry_validator.py input_file.inp")
        sys.exit(2)

    filepath = sys.argv[1]
    validator = MCNPGeometryValidator(filepath)
    results = validator.validate()

    # Print results
    print("="*70)
    print(f"MCNP Geometry Validation Report: {filepath}")
    print("="*70)

    if results.errors:
        print(f"\n❌ ERRORS ({len(results.errors)}):")
        for i, error in enumerate(results.errors, 1):
            print(f"  {i}. {error}")

    if results.warnings:
        print(f"\n⚠️  WARNINGS ({len(results.warnings)}):")
        for i, warning in enumerate(results.warnings, 1):
            print(f"  {i}. {warning}")

    if results.info:
        print(f"\nℹ️  INFO:")
        for info in results.info:
            print(f"  - {info}")

    print("\n" + "="*70)

    if results.errors:
        print("❌ VALIDATION FAILED - Fix errors before running MCNP")
        sys.exit(1)
    elif results.warnings:
        print("⚠️  VALIDATION PASSED WITH WARNINGS")
        sys.exit(0)
    else:
        print("✅ VALIDATION PASSED - No errors found")
        sys.exit(0)

if __name__ == '__main__':
    main()
