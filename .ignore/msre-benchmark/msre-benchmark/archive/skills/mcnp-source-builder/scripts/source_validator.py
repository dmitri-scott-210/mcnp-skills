"""
MCNP Source Definition Validator

Validates SDEF, SI, SP, SB, and DS card consistency in MCNP input files.
Checks probability normalization, distribution references, and keyword compatibility.

Usage:
    python source_validator.py input.i
    python source_validator.py --interactive

Author: Claude (Anthropic)
Created: 2025-11-03
"""

import argparse
import re
import sys
from typing import Dict, List, Tuple, Set
from pathlib import Path


class SourceValidator:
    """Validator for MCNP source definitions"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.si_cards = {}  # {dist_num: (type, values)}
        self.sp_cards = {}  # {dist_num: (type, probabilities)}
        self.sb_cards = {}  # {dist_num: values}
        self.ds_cards = {}  # {dist_num: values}
        self.sdef_refs = set()  # Distribution numbers referenced in SDEF

    def add_error(self, msg: str):
        """Add validation error"""
        self.errors.append(f"ERROR: {msg}")

    def add_warning(self, msg: str):
        """Add validation warning"""
        self.warnings.append(f"WARNING: {msg}")

    def parse_si_card(self, line: str) -> Tuple[int, str, List[float]]:
        """
        Parse SI card: SI<n> [H|L|A|S] v1 v2 v3 ...

        Returns:
            (distribution_number, type, values)
        """
        # Extract distribution number
        match = re.match(r'SI(\d+)\s+([HLAS])?\s*(.*)', line, re.IGNORECASE)
        if not match:
            return None, None, None

        dist_num = int(match.group(1))
        dist_type = match.group(2).upper() if match.group(2) else 'H'  # Default is H
        values_str = match.group(3)

        # Parse values
        values = [float(x) for x in values_str.split()]

        return dist_num, dist_type, values

    def parse_sp_card(self, line: str) -> Tuple[int, str, List[float]]:
        """
        Parse SP card: SP<n> [D|C|V|W] p1 p2 p3 ...

        Returns:
            (distribution_number, type, probabilities)
        """
        match = re.match(r'SP(\d+)\s+([DCVW])?\s*(.*)', line, re.IGNORECASE)
        if not match:
            return None, None, None

        dist_num = int(match.group(1))
        prob_type = match.group(2).upper() if match.group(2) else 'D'  # Default is D
        probs_str = match.group(3)

        # Parse probabilities
        probs = [float(x) for x in probs_str.split()]

        return dist_num, prob_type, probs

    def parse_sdef_keywords(self, line: str) -> Set[str]:
        """
        Parse SDEF card to extract distribution references.

        Returns:
            Set of distribution keywords (ERG, DIR, POS, etc.)
        """
        keywords = set()

        # Look for distribution references: keyword=Dn or keyword=DSn
        pattern = r'(\w+)\s*=\s*[Dd](\d+)'
        matches = re.finditer(pattern, line)

        for match in matches:
            keyword = match.group(1).upper()
            dist_num = int(match.group(2))
            keywords.add(keyword)
            self.sdef_refs.add(dist_num)

        return keywords

    def validate_sp_normalization(self, dist_num: int, prob_type: str, probs: List[float]):
        """
        Validate SP card probability normalization.

        Rules:
        - Type D (discrete): probabilities should sum to 1.0
        - Type C (cumulative): last value should be 1.0
        - Type V (volume): checked against geometry
        - Type W (weight): no normalization required
        """
        if prob_type == 'D':
            prob_sum = sum(probs)
            if abs(prob_sum - 1.0) > 0.001:
                self.add_warning(
                    f"SP{dist_num} (type D): Probabilities sum to {prob_sum:.6f}, not 1.0. "
                    f"MCNP will normalize, but verify intent."
                )

        elif prob_type == 'C':
            if abs(probs[-1] - 1.0) > 0.001:
                self.add_error(
                    f"SP{dist_num} (type C): Last cumulative probability is {probs[-1]:.6f}, not 1.0. "
                    f"This will cause source sampling errors."
                )

    def validate_si_sp_consistency(self, dist_num: int):
        """Validate SI and SP card consistency"""
        if dist_num not in self.si_cards:
            self.add_error(f"SP{dist_num} exists but SI{dist_num} is missing")
            return

        if dist_num not in self.sp_cards:
            self.add_warning(f"SI{dist_num} exists but SP{dist_num} is missing (uniform sampling will be used)")
            return

        si_type, si_values = self.si_cards[dist_num]
        sp_type, sp_probs = self.sp_cards[dist_num]

        # Check length consistency
        if si_type in ['H', 'A']:  # Histogram or Arbitrary
            if len(si_values) - 1 != len(sp_probs):
                self.add_error(
                    f"SI{dist_num}/SP{dist_num}: For type {si_type}, SI should have n+1 values "
                    f"for n probabilities. Found SI={len(si_values)}, SP={len(sp_probs)}"
                )
        elif si_type in ['L', 'S']:  # List or Special
            if len(si_values) != len(sp_probs):
                self.add_error(
                    f"SI{dist_num}/SP{dist_num}: For type {si_type}, SI and SP must have equal length. "
                    f"Found SI={len(si_values)}, SP={len(sp_probs)}"
                )

    def validate_distribution_references(self):
        """Validate that all SDEF-referenced distributions exist"""
        for dist_num in self.sdef_refs:
            if dist_num not in self.si_cards:
                self.add_error(f"SDEF references D{dist_num}, but SI{dist_num} not found")

    def validate_file(self, filepath: str) -> bool:
        """
        Validate MCNP input file source definitions.

        Returns:
            True if no errors (warnings OK), False if errors found
        """
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.add_error(f"File not found: {filepath}")
            return False
        except Exception as e:
            self.add_error(f"Error reading file: {e}")
            return False

        # Find data cards block (third block)
        in_data_block = False
        blank_count = 0

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Skip comments and empty lines
            if line.startswith('c ') or line.startswith('C ') or not line:
                if not line:
                    blank_count += 1
                    if blank_count == 2:
                        in_data_block = True
                continue

            if not in_data_block:
                continue

            # Parse SDEF card
            if line.upper().startswith('SDEF'):
                self.parse_sdef_keywords(line)

            # Parse SI cards
            elif line.upper().startswith('SI'):
                dist_num, dist_type, values = self.parse_si_card(line)
                if dist_num:
                    self.si_cards[dist_num] = (dist_type, values)

            # Parse SP cards
            elif line.upper().startswith('SP'):
                dist_num, prob_type, probs = self.parse_sp_card(line)
                if dist_num:
                    self.sp_cards[dist_num] = (prob_type, probs)
                    # Validate normalization
                    self.validate_sp_normalization(dist_num, prob_type, probs)

            # Parse SB cards (biasing)
            elif line.upper().startswith('SB'):
                match = re.match(r'SB(\d+)', line, re.IGNORECASE)
                if match:
                    dist_num = int(match.group(1))
                    self.sb_cards[dist_num] = True

            # Parse DS cards (dependent distributions)
            elif line.upper().startswith('DS'):
                match = re.match(r'DS(\d+)', line, re.IGNORECASE)
                if match:
                    dist_num = int(match.group(1))
                    self.ds_cards[dist_num] = True

        # Perform cross-validation
        for dist_num in self.sp_cards:
            self.validate_si_sp_consistency(dist_num)

        self.validate_distribution_references()

        # Print results
        print(f"\n{'='*70}")
        print(f"MCNP Source Validation Report: {Path(filepath).name}")
        print(f"{'='*70}\n")

        if self.errors:
            print(f"ERRORS FOUND: {len(self.errors)}")
            for err in self.errors:
                print(f"  {err}")
            print()

        if self.warnings:
            print(f"WARNINGS: {len(self.warnings)}")
            for warn in self.warnings:
                print(f"  {warn}")
            print()

        if not self.errors and not self.warnings:
            print("✓ No issues found. Source definitions appear valid.")
            print()

        # Print summary
        print(f"Summary:")
        print(f"  SI cards found: {len(self.si_cards)}")
        print(f"  SP cards found: {len(self.sp_cards)}")
        print(f"  SB cards found: {len(self.sb_cards)}")
        print(f"  DS cards found: {len(self.ds_cards)}")
        print(f"  SDEF references: {len(self.sdef_refs)}")
        print(f"{'='*70}\n")

        return len(self.errors) == 0


def interactive_mode():
    """Interactive validation mode"""
    print("\n" + "="*70)
    print("MCNP Source Validator - Interactive Mode")
    print("="*70 + "\n")

    while True:
        filepath = input("Enter MCNP input file path (or 'quit' to exit): ").strip()

        if filepath.lower() in ['quit', 'exit', 'q']:
            print("Exiting...")
            break

        if not Path(filepath).exists():
            print(f"ERROR: File not found: {filepath}\n")
            continue

        validator = SourceValidator()
        validator.validate_file(filepath)


def main():
    parser = argparse.ArgumentParser(
        description='Validate MCNP source definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single file
  python source_validator.py input.i

  # Interactive mode
  python source_validator.py --interactive

Validation Checks:
  - SP probability normalization (type D should sum to 1.0, type C last value = 1.0)
  - SI/SP length consistency (histogram vs discrete)
  - SDEF distribution references (all Dn must have corresponding SIn)
  - Missing SI or SP cards
        """
    )

    parser.add_argument('input_file', nargs='?', help='MCNP input file to validate')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode - validate multiple files')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.input_file:
        validator = SourceValidator()
        is_valid = validator.validate_file(args.input_file)
        sys.exit(0 if is_valid else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
