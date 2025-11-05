#!/usr/bin/env python3
"""
MCNP Input Structure Validator

Pre-MCNP validation script that checks input file structure and common
formatting errors before running MCNP. Catches issues that cause fatal errors.

Usage:
    python validate_input_structure.py input.i
    python validate_input_structure.py input.i --verbose

Requirements:
    Python 3.8+
    No external dependencies (uses standard library only)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


class ValidationError:
    """Represents a validation error with severity and location."""

    def __init__(self, severity: str, line_num: int, message: str, suggestion: str = ""):
        self.severity = severity  # ERROR, WARNING, INFO
        self.line_num = line_num
        self.message = message
        self.suggestion = suggestion

    def __str__(self) -> str:
        result = f"[{self.severity}] Line {self.line_num}: {self.message}"
        if self.suggestion:
            result += f"\n  → Suggestion: {self.suggestion}"
        return result


def check_three_block_structure(lines: List[str]) -> List[ValidationError]:
    """Check for proper three-block structure with blank line separators."""
    errors = []

    # Skip title and comments to find first cell card
    first_cell_line = None
    first_surface_line = None
    first_data_line = None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip comments and blank lines
        if not stripped or stripped.startswith('c ') or stripped.startswith('C '):
            continue

        # Check if it's a cell card (starts with number)
        if first_cell_line is None and re.match(r'^\d', stripped):
            first_cell_line = i

        # Check for surface cards (number + surface type)
        elif first_surface_line is None and re.match(r'^\d+\s+(SO|S|SX|SY|SZ|PX|PY|PZ|P|CX|CY|CZ|C/X|C/Y|C/Z)', stripped, re.IGNORECASE):
            first_surface_line = i

        # Check for data cards (starts with letter)
        elif first_data_line is None and re.match(r'^[A-Za-z]', stripped):
            first_data_line = i

    # Check blank line after cells
    if first_cell_line and first_surface_line:
        # Check if there's a blank line between cells and surfaces
        has_blank = False
        for i in range(first_cell_line, first_surface_line):
            if not lines[i-1].strip():
                has_blank = True
                break

        if not has_blank:
            errors.append(ValidationError(
                "ERROR", first_surface_line,
                "Missing blank line between cell cards and surface cards",
                "Add a blank line after the last cell card"
            ))

    # Check blank line after surfaces
    if first_surface_line and first_data_line:
        has_blank = False
        for i in range(first_surface_line, first_data_line):
            if not lines[i-1].strip():
                has_blank = True
                break

        if not has_blank:
            errors.append(ValidationError(
                "ERROR", first_data_line,
                "Missing blank line between surface cards and data cards",
                "Add a blank line after the last surface card"
            ))

    # Check blank line at end of file
    if lines and lines[-1].strip():
        errors.append(ValidationError(
            "ERROR", len(lines),
            "Missing blank line at end of file",
            "Add a blank line as the last line of the file"
        ))

    return errors


def check_tabs(lines: List[str]) -> List[ValidationError]:
    """Check for tab characters (MCNP treats tabs as single spaces)."""
    errors = []

    for i, line in enumerate(lines, 1):
        if '\t' in line:
            errors.append(ValidationError(
                "ERROR", i,
                "Tab character found (MCNP treats tabs as single spaces)",
                "Replace tabs with spaces (configure editor: 'Insert spaces for tabs')"
            ))

    return errors


def check_mode_card_first(lines: List[str]) -> List[ValidationError]:
    """Check that MODE card is first data card."""
    errors = []

    first_data_card = None
    first_data_line = None
    mode_line = None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip comments and blank lines
        if not stripped or stripped.startswith('c ') or stripped.startswith('C ') or stripped.startswith('$'):
            continue

        # Check if it's a data card (starts with letter, not number)
        if re.match(r'^[A-Za-z]', stripped):
            if first_data_card is None:
                first_data_card = stripped.split()[0].upper()
                first_data_line = i

            if stripped.upper().startswith('MODE'):
                mode_line = i
                break

    if first_data_card and mode_line:
        if first_data_card != 'MODE':
            errors.append(ValidationError(
                "ERROR", first_data_line,
                f"MODE card must be first data card (found {first_data_card} first)",
                "Move MODE card before all other data cards"
            ))

    return errors


def check_particle_designators(lines: List[str]) -> List[ValidationError]:
    """Check for missing particle designators on cards that require them."""
    errors = []

    # Cards that require particle designators
    requires_designator = ['F1', 'F2', 'F4', 'F5', 'F6', 'F7', 'F8',
                           'IMP', 'PHYS', 'CUT', 'ELPT']

    for i, line in enumerate(lines, 1):
        stripped = line.strip().upper()

        # Skip comments
        if not stripped or stripped.startswith('C ') or stripped.startswith('$'):
            continue

        # Check each card type
        for card in requires_designator:
            # Match card name at start of line
            if re.match(rf'^{card}[^:]*\s', stripped):
                # Check if it has particle designator (:N, :P, :E, etc.)
                if ':' not in stripped.split()[0]:
                    errors.append(ValidationError(
                        "WARNING", i,
                        f"{card} card may need particle designator (:N, :P, :E, etc.)",
                        f"Add particle designator: {card}:N (for neutrons)"
                    ))

    return errors


def check_continuation_lines(lines: List[str]) -> List[ValidationError]:
    """Check for improperly formatted continuation lines."""
    errors = []

    for i, line in enumerate(lines, 1):
        # Skip blank lines and comments
        if not line.strip() or line.strip().startswith('c ') or line.strip().startswith('C '):
            continue

        # Check if line starts without 5 spaces and isn't a card name
        # (likely an improper continuation)
        if line and line[0] not in [' ', 'c', 'C', '$'] and not re.match(r'^[A-Za-z0-9*]', line[0]):
            errors.append(ValidationError(
                "WARNING", i,
                "Possible improper continuation line (not 5+ spaces or card name)",
                "Start continuation lines with 5+ spaces, use &, or repeat card name"
            ))

    return errors


def check_comment_format(lines: List[str]) -> List[ValidationError]:
    """Check for comment formatting issues."""
    errors = []

    for i, line in enumerate(lines, 1):
        # Check for 'C' or 'c' in columns 1-5 without space
        if len(line) > 1 and line[0] in ['c', 'C'] and line[1] != ' ':
            errors.append(ValidationError(
                "WARNING", i,
                "Comment card 'C' should be followed by space in column 6",
                "Add space after 'C': 'C This is a comment'"
            ))

    return errors


def check_line_length(lines: List[str]) -> List[ValidationError]:
    """Check for excessively long lines."""
    errors = []

    for i, line in enumerate(lines, 1):
        if len(line) > 128:
            errors.append(ValidationError(
                "WARNING", i,
                f"Line exceeds 128 characters ({len(line)} chars)",
                "MCNP supports up to 128 characters; consider splitting line"
            ))

    return errors


def validate_input_file(input_file: Path, verbose: bool = False) -> Tuple[List[ValidationError], bool]:
    """Validate MCNP input file structure.

    Returns:
        Tuple of (errors_list, passed_validation)
    """
    if not input_file.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        return [], False

    # Read file
    with open(input_file, 'r', errors='ignore') as f:
        lines = f.readlines()

    if not lines:
        print(f"Error: File is empty: {input_file}", file=sys.stderr)
        return [], False

    # Run all checks
    all_errors = []
    all_errors.extend(check_three_block_structure(lines))
    all_errors.extend(check_tabs(lines))
    all_errors.extend(check_mode_card_first(lines))
    all_errors.extend(check_particle_designators(lines))
    all_errors.extend(check_continuation_lines(lines))
    all_errors.extend(check_comment_format(lines))
    all_errors.extend(check_line_length(lines))

    # Sort by line number
    all_errors.sort(key=lambda e: (e.line_num, e.severity))

    # Check if validation passed (no errors, warnings are okay)
    has_errors = any(e.severity == "ERROR" for e in all_errors)
    passed = not has_errors

    return all_errors, passed


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate MCNP input file structure before running MCNP',
        epilog='Exit codes: 0=passed, 1=errors found, 2=file error'
    )
    parser.add_argument('input_file', type=Path,
                        help='MCNP input file to validate')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all checks including INFO messages')

    args = parser.parse_args()

    print(f"Validating: {args.input_file}")
    print("="*70)

    errors, passed = validate_input_file(args.input_file, args.verbose)

    if not errors:
        print("✓ No issues found - input structure looks good!")
        print("\nRecommended next steps:")
        print(f"  1. Plot geometry: mcnp6 inp={args.input_file} ip")
        print(f"  2. Run simulation: mcnp6 inp={args.input_file}")
        return 0

    # Print errors
    error_count = sum(1 for e in errors if e.severity == "ERROR")
    warning_count = sum(1 for e in errors if e.severity == "WARNING")

    for error in errors:
        if error.severity == "INFO" and not args.verbose:
            continue
        print(error)
        print()

    # Summary
    print("="*70)
    if passed:
        print(f"✓ PASSED with {warning_count} warning(s)")
        print("\nWarnings should be reviewed but won't prevent MCNP from running.")
        print("\nRecommended next steps:")
        print(f"  1. Review warnings above")
        print(f"  2. Plot geometry: mcnp6 inp={args.input_file} ip")
        print(f"  3. Run simulation: mcnp6 inp={args.input_file}")
        return 0
    else:
        print(f"✗ FAILED with {error_count} error(s), {warning_count} warning(s)")
        print("\nErrors must be fixed before running MCNP.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
