#!/usr/bin/env python3
"""
Block Structure Validator

Specialized validator for MCNP three-block input structure.
Verifies:
- Exactly 2 blank lines separating blocks
- Title card present
- Three blocks present (cells, surfaces, data)
- No blank lines within blocks

Usage:
    from block_structure_validator import validate_block_structure

    errors = validate_block_structure('input.inp')
    if errors:
        for error in errors:
            print(f"ERROR: {error}")

Author: MCNP Skills Revamp Project
Version: 2.0.0
"""

from typing import List, Tuple


def validate_block_structure(filepath: str) -> List[str]:
    """
    Validate MCNP input file block structure.

    Args:
        filepath: Path to MCNP input file

    Returns:
        List of error strings (empty if valid)
    """
    errors = []

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [f"File not found: {filepath}"]
    except Exception as e:
        return [f"Error reading file: {e}"]

    # Check for blank lines
    blank_line_numbers = []
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            blank_line_numbers.append(i)

    blank_count = len(blank_line_numbers)

    # Check for exactly 2 blank lines
    if blank_count < 2:
        errors.append(
            f"FATAL: Missing blank line separator(s). "
            f"Expected 2, found {blank_count}. "
            f"Add blank line after Cell Cards and after Surface Cards blocks."
        )
        return errors
    elif blank_count > 2:
        errors.append(
            f"FATAL: Extra blank lines detected. "
            f"Expected 2, found {blank_count} at lines {blank_line_numbers}. "
            f"Remove blank lines within blocks."
        )

    # Check title card
    if not lines[0].strip():
        errors.append("FATAL: Title card missing (first line is blank)")

    # Check three blocks
    if blank_count >= 2:
        first_blank_idx = blank_line_numbers[0] - 1  # Convert to 0-indexed
        second_blank_idx = blank_line_numbers[1] - 1

        # Cell block
        cell_block = lines[1:first_blank_idx]
        if not _has_content(cell_block):
            errors.append("FATAL: Cell Cards block is empty")

        # Surface block
        surface_block = lines[first_blank_idx+1:second_blank_idx]
        if not _has_content(surface_block):
            errors.append("FATAL: Surface Cards block is empty")

        # Data block
        data_block = lines[second_blank_idx+1:]
        if not _has_content(data_block):
            errors.append("FATAL: Data Cards block is empty")

    return errors


def _has_content(lines: List[str]) -> bool:
    """
    Check if block has non-comment content.

    Args:
        lines: List of lines in block

    Returns:
        True if block has content, False if empty or only comments
    """
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('c'):
            return True
    return False


def get_block_boundaries(filepath: str) -> Tuple[int, int, int]:
    """
    Get line numbers of block boundaries.

    Args:
        filepath: Path to MCNP input file

    Returns:
        Tuple of (first_blank_line, second_blank_line, total_lines)
        Returns (0, 0, 0) if structure invalid
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except Exception:
        return (0, 0, 0)

    blank_lines = []
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            blank_lines.append(i)

    if len(blank_lines) < 2:
        return (0, 0, 0)

    return (blank_lines[0], blank_lines[1], len(lines))


def main():
    """Command-line interface."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python block_structure_validator.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    print(f"Validating block structure: {input_file}")
    print("="*60)

    errors = validate_block_structure(input_file)

    if errors:
        print("BLOCK STRUCTURE ERRORS:")
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        sys.exit(1)
    else:
        print("✓ Block structure valid")
        boundaries = get_block_boundaries(input_file)
        print(f"\nBlock boundaries:")
        print(f"  Cell Cards:    Lines 1-{boundaries[0]-1}")
        print(f"  Surface Cards: Lines {boundaries[0]+1}-{boundaries[1]-1}")
        print(f"  Data Cards:    Lines {boundaries[1]+1}-{boundaries[2]}")
        sys.exit(0)


if __name__ == '__main__':
    main()
