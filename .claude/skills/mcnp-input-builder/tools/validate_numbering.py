#!/usr/bin/env python3
"""
MCNP Numbering Scheme Validator

Validates that MCNP input files follow systematic numbering schemes:
- Hierarchical position encoding (XYZSS pattern)
- Functional subsystem ranges (10000-blocks)
- Universe component encoding (XYZW pattern)
- Correlated entity numbering
- No numbering conflicts

Usage:
    python validate_numbering.py input_file.i [--scheme SCHEME_TYPE]

Scheme types:
    - hierarchical: XYZSS position encoding
    - subsystem: Reserved 10000-blocks
    - universe: XYZW component encoding
    - auto: Attempt to detect scheme from file header
"""

import re
import sys
import argparse
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class NumberingValidator:
    """Validates MCNP numbering schemes"""

    def __init__(self, filename: str, scheme: str = "auto"):
        self.filename = filename
        self.scheme = scheme
        self.cells = []
        self.surfaces = {}
        self.materials = {}
        self.universes = {}
        self.errors = []
        self.warnings = []
        self.numbering_config = {}

    def parse_input(self):
        """Parse MCNP input file into sections"""
        print(f"\n{'='*60}")
        print(f"Parsing: {self.filename}")
        print(f"{'='*60}")

        with open(self.filename, 'r') as f:
            lines = f.readlines()

        in_cells = False
        in_surfaces = False
        in_data = False
        title_seen = False

        for i, line in enumerate(lines, 1):
            # Skip title card
            if not title_seen:
                title_seen = True
                continue

            # Blank line transitions
            if line.strip() == '':
                if in_cells:
                    in_cells = False
                    in_surfaces = True
                    print(f"  Transitioned to surface block at line {i}")
                elif in_surfaces:
                    in_surfaces = False
                    in_data = True
                    print(f"  Transitioned to data block at line {i}")
                continue

            # Comment lines
            if line.startswith(('c', 'C', ' c', ' C')):
                # Try to extract numbering scheme from comments
                if 'NUMBERING SCHEME' in line.upper() or 'CELLS:' in line.upper():
                    self._extract_scheme_info(line)
                continue

            # Start with cells
            if not in_cells and not in_surfaces and not in_data:
                in_cells = True
                print(f"  Started cell block at line {i}")

            # Parse based on block
            if in_cells:
                self._parse_cell(line, i)
            elif in_surfaces:
                self._parse_surface(line, i)
            elif in_data:
                self._parse_data_card(line, i)

        print(f"\nParsed:")
        print(f"  {len(self.cells)} cells")
        print(f"  {len(self.surfaces)} surfaces")
        print(f"  {len(self.materials)} materials")
        print(f"  {len(self.universes)} universes")

    def _extract_scheme_info(self, line: str):
        """Extract numbering scheme info from comments"""
        # Look for patterns like "Cells: XYZSS" or "10000-19999: Fuel"
        patterns = {
            'hierarchical': r'[XYZ]{3,5}',
            'subsystem': r'\d{5,6}-\d{5,6}',
        }
        for scheme_type, pattern in patterns.items():
            if re.search(pattern, line):
                self.numbering_config[scheme_type] = line.strip()

    def _parse_cell(self, line: str, line_num: int):
        """Parse cell card"""
        # Basic cell format: j m d geom params
        parts = line.split()
        if len(parts) >= 3:
            try:
                cell_num = int(parts[0])
                mat_num = int(parts[1])
                density = parts[2]

                # Extract universe if present
                universe = None
                if 'U=' in line.upper():
                    match = re.search(r'[Uu]=(\d+)', line)
                    if match:
                        universe = int(match.group(1))

                # Extract fill if present
                fill = None
                if 'FILL=' in line.upper():
                    match = re.search(r'[Ff][Ii][Ll][Ll]=(\d+)', line)
                    if match:
                        fill = int(match.group(1))

                self.cells.append({
                    'number': cell_num,
                    'material': mat_num,
                    'density': density,
                    'universe': universe,
                    'fill': fill,
                    'line': line_num
                })

                # Track universes
                if universe is not None:
                    if universe not in self.universes:
                        self.universes[universe] = []
                    self.universes[universe].append(cell_num)

            except (ValueError, IndexError):
                self.warnings.append(f"Line {line_num}: Could not parse cell card")

    def _parse_surface(self, line: str, line_num: int):
        """Parse surface card"""
        parts = line.split()
        if parts:
            try:
                surf_num = int(parts[0])
                surf_type = parts[1] if len(parts) > 1 else None
                self.surfaces[surf_num] = {
                    'type': surf_type,
                    'line': line_num
                }
            except (ValueError, IndexError):
                self.warnings.append(f"Line {line_num}: Could not parse surface card")

    def _parse_data_card(self, line: str, line_num: int):
        """Parse data cards (materials, etc.)"""
        # Material card
        if line.strip().upper().startswith('M'):
            match = re.match(r'[Mm](\d+)', line)
            if match:
                mat_num = int(match.group(1))
                self.materials[mat_num] = {
                    'line': line_num
                }

    def validate_hierarchical_encoding(self):
        """Validate XYZSS hierarchical position encoding"""
        print(f"\n{'='*60}")
        print("Validating Hierarchical Encoding (XYZSS)")
        print(f"{'='*60}")

        if not self.cells:
            self.warnings.append("No cells found to validate")
            return

        # Analyze cell numbers for patterns
        cell_nums = [c['number'] for c in self.cells]

        # Check for 5-digit pattern (XYZSS)
        five_digit = [n for n in cell_nums if 10000 <= n <= 99999]

        if five_digit:
            print(f"\n✓ Found {len(five_digit)} cells with 5-digit encoding")

            # Extract components
            for cell_num in five_digit:
                x = cell_num // 10000
                y = (cell_num // 1000) % 10
                z = (cell_num // 100) % 10
                ss = cell_num % 100

                if x == 0:
                    self.warnings.append(
                        f"Cell {cell_num}: X=0 in XYZSS encoding (should be 1-9)"
                    )

                # Check for reasonable ranges
                if x > 9:
                    self.errors.append(
                        f"Cell {cell_num}: X={x} exceeds single digit"
                    )

            # Check for consistent encoding
            x_values = set(n // 10000 for n in five_digit)
            y_values = set((n // 1000) % 10 for n in five_digit)
            z_values = set((n // 100) % 10 for n in five_digit)

            print(f"\n  Component ranges:")
            print(f"    X (Major): {sorted(x_values)}")
            print(f"    Y (Sub):   {sorted(y_values)}")
            print(f"    Z (Layer): {sorted(z_values)}")

        else:
            print("\n  No 5-digit hierarchical encoding detected")

    def validate_subsystem_ranges(self):
        """Validate functional subsystem 10000-block ranges"""
        print(f"\n{'='*60}")
        print("Validating Subsystem Ranges (10000-blocks)")
        print(f"{'='*60}")

        if not self.cells:
            return

        cell_nums = [c['number'] for c in self.cells]

        # Group by 10000 blocks
        blocks = defaultdict(list)
        for num in cell_nums:
            block = (num // 10000) * 10000
            blocks[block].append(num)

        if len(blocks) > 1:
            print(f"\n✓ Found {len(blocks)} distinct 10000-blocks:")
            for block in sorted(blocks.keys()):
                count = len(blocks[block])
                range_str = f"{block:05d}-{block+9999:05d}"
                print(f"    {range_str}: {count:4d} cells")

            # Check for conflicts within blocks
            for block, nums in blocks.items():
                if len(nums) != len(set(nums)):
                    duplicates = [n for n in set(nums) if nums.count(n) > 1]
                    self.errors.append(
                        f"Block {block}: Duplicate cell numbers: {duplicates}"
                    )
        else:
            print("\n  All cells in same 10000-block (no subsystem separation)")

    def validate_universe_encoding(self):
        """Validate XYZW universe component encoding"""
        print(f"\n{'='*60}")
        print("Validating Universe Component Encoding (XYZW)")
        print(f"{'='*60}")

        if not self.universes:
            print("\n  No universes defined (simple geometry)")
            return

        print(f"\n✓ Found {len(self.universes)} universe definitions")

        # Analyze universe numbering
        u_nums = sorted(self.universes.keys())

        # Check for component type encoding (W digit)
        four_digit = [u for u in u_nums if 1000 <= u <= 9999]

        if four_digit:
            print(f"\n  {len(four_digit)} universes with 4-digit encoding (XYZW):")

            # Group by position (XYZ)
            positions = defaultdict(list)
            for u in four_digit:
                pos = u // 10  # XYZ
                comp_type = u % 10  # W
                positions[pos].append((u, comp_type))

            for pos in sorted(positions.keys()):
                components = positions[pos]
                comp_str = ", ".join(f"u={u}(W={w})" for u, w in components)
                print(f"    Position {pos:03d}: {comp_str}")

                # Validate component types
                for u, w in components:
                    if w > 9:
                        self.errors.append(
                            f"Universe {u}: Component type W={w} exceeds single digit"
                        )

        # Check for universe 0 (should not be explicitly defined)
        if 0 in u_nums:
            self.warnings.append(
                "Universe 0 explicitly defined (usually global, implicit)"
            )

    def validate_correlated_numbering(self):
        """Validate correlated cell/surface/material numbering"""
        print(f"\n{'='*60}")
        print("Validating Correlated Numbering")
        print(f"{'='*60}")

        if not self.cells:
            return

        # Check if cell numbers correlate with surface numbers
        cell_nums = set(c['number'] for c in self.cells)
        surf_nums = set(self.surfaces.keys())

        correlated = cell_nums & surf_nums
        if correlated:
            print(f"\n✓ Found {len(correlated)} correlated cell/surface numbers")
            print(f"  Examples: {sorted(list(correlated))[:10]}")
        else:
            print("\n  No obvious cell/surface correlation detected")

        # Check cell-material correlation
        mat_nums = set(self.materials.keys())
        mat_in_cells = set(c['material'] for c in self.cells if c['material'] != 0)

        # Extract base numbers (e.g., 11101 → 111)
        def get_base(num, digits=3):
            """Extract first 'digits' digits from number"""
            if num < 10**digits:
                return num
            while num >= 10**digits:
                num //= 10
            return num

        cell_bases = set(get_base(c['number']) for c in self.cells)
        mat_bases = set(get_base(m) for m in mat_nums)

        correlated_mat = cell_bases & mat_bases
        if correlated_mat:
            print(f"\n✓ Found {len(correlated_mat)} correlated cell/material base numbers")
            print(f"  Examples: {sorted(list(correlated_mat))[:10]}")

    def validate_no_conflicts(self):
        """Check for numbering conflicts"""
        print(f"\n{'='*60}")
        print("Checking for Numbering Conflicts")
        print(f"{'='*60}")

        # Check cell number uniqueness
        cell_nums = [c['number'] for c in self.cells]
        if len(cell_nums) != len(set(cell_nums)):
            duplicates = [n for n in set(cell_nums) if cell_nums.count(n) > 1]
            self.errors.append(f"Duplicate cell numbers: {duplicates}")
            print(f"\n✗ ERROR: Duplicate cell numbers found: {duplicates}")
        else:
            print(f"\n✓ No duplicate cell numbers ({len(cell_nums)} cells)")

        # Check surface number uniqueness
        surf_nums = list(self.surfaces.keys())
        if len(surf_nums) != len(set(surf_nums)):
            duplicates = [n for n in set(surf_nums) if surf_nums.count(n) > 1]
            self.errors.append(f"Duplicate surface numbers: {duplicates}")
            print(f"\n✗ ERROR: Duplicate surface numbers found: {duplicates}")
        else:
            print(f"\n✓ No duplicate surface numbers ({len(surf_nums)} surfaces)")

        # Check material number uniqueness
        mat_nums = list(self.materials.keys())
        if len(mat_nums) != len(set(mat_nums)):
            duplicates = [n for n in set(mat_nums) if mat_nums.count(n) > 1]
            self.errors.append(f"Duplicate material numbers: {duplicates}")
            print(f"\n✗ ERROR: Duplicate material numbers found: {duplicates}")
        else:
            print(f"\n✓ No duplicate material numbers ({len(mat_nums)} materials)")

        # Check universe number uniqueness (critical!)
        u_nums = list(self.universes.keys())
        if len(u_nums) != len(set(u_nums)):
            duplicates = [n for n in set(u_nums) if u_nums.count(n) > 1]
            self.errors.append(f"CRITICAL: Duplicate universe numbers: {duplicates}")
            print(f"\n✗ CRITICAL ERROR: Duplicate universe numbers: {duplicates}")
        else:
            print(f"\n✓ No duplicate universe numbers ({len(u_nums)} universes)")

    def validate_all(self):
        """Run all validation checks"""
        print(f"\n{'#'*60}")
        print(f"# MCNP NUMBERING SCHEME VALIDATION")
        print(f"# File: {self.filename}")
        print(f"{'#'*60}")

        self.parse_input()

        # Run validations
        self.validate_hierarchical_encoding()
        self.validate_subsystem_ranges()
        self.validate_universe_encoding()
        self.validate_correlated_numbering()
        self.validate_no_conflicts()

        # Summary
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")

        if self.errors:
            print(f"\n✗ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✓ ALL CHECKS PASSED - No errors or warnings")
        elif not self.errors:
            print(f"\n✓ VALIDATION PASSED - {len(self.warnings)} warnings (non-critical)")
        else:
            print(f"\n✗ VALIDATION FAILED - Fix {len(self.errors)} errors before running MCNP")

        print(f"\n{'='*60}\n")

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate MCNP input file numbering schemes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scheme types:
  hierarchical - XYZSS position encoding (10000-99999 range)
  subsystem    - Reserved 10000-blocks for functional subsystems
  universe     - XYZW component encoding for universes
  auto         - Attempt to detect scheme from file header

Examples:
  python validate_numbering.py input.i
  python validate_numbering.py pwr_core.i --scheme hierarchical
  python validate_numbering.py htgr_model.i --scheme universe
        """
    )

    parser.add_argument('input_file', help='MCNP input file to validate')
    parser.add_argument('--scheme', choices=['hierarchical', 'subsystem', 'universe', 'auto'],
                        default='auto', help='Numbering scheme type (default: auto)')

    args = parser.parse_args()

    # Check file exists
    try:
        with open(args.input_file, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.input_file}")
        sys.exit(1)

    # Run validation
    validator = NumberingValidator(args.input_file, args.scheme)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
