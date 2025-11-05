#!/usr/bin/env python3
"""
Fill Array Validator

Standalone tool for validating MCNP fill array dimensions.
Checks that array sizes match lattice declarations.

Usage:
    python fill_array_validator.py input.inp
"""

import sys
from mcnp_cell_checker import MCNPCellChecker


def validate_fill_arrays(input_file):
    """
    Validate all fill arrays in input file

    Args:
        input_file: Path to MCNP input file

    Returns:
        True if all arrays valid, False otherwise
    """
    checker = MCNPCellChecker()
    fill_check = checker.check_fill_dimensions(input_file)

    if not fill_check:
        print("No fill arrays found in input file")
        return True

    print(f"{'='*70}")
    print(f"Fill Array Validation: {input_file}")
    print(f"{'='*70}\n")

    all_valid = True

    for cell_num in sorted(fill_check.keys()):
        result = fill_check[cell_num]

        print(f"Cell {cell_num}:")
        print(f"  Declaration: {result['declaration']}")

        i_size, j_size, k_size = result['dimensions']
        print(f"  Dimensions: {i_size} × {j_size} × {k_size}")
        print(f"  Expected: {result['expected_size']} values")
        print(f"  Actual: {result['actual_size']} values")

        if result['valid']:
            print("  Status: ✓ Correct size\n")
        else:
            all_valid = False
            diff = result['actual_size'] - result['expected_size']
            print(f"  Status: ✗ Size mismatch ({diff:+d})")

            if diff < 0:
                print(f"  ERROR: Missing {-diff} values")
            else:
                print(f"  ERROR: Extra {diff} values")
            print()

        # Show universe composition
        if result['valid']:
            array_values = result['array_values']
            unique_universes = sorted(set(array_values) - {0})

            if unique_universes:
                print(f"  Universe composition:")
                for u in unique_universes:
                    count = array_values.count(u)
                    percentage = (count / len(array_values)) * 100
                    print(f"    u={u}: {count:3d} times ({percentage:5.1f}%)")
                print()

    # Summary
    print("=" * 70)
    if all_valid:
        print(f"✓ ALL FILL ARRAYS VALID ({len(fill_check)} arrays)")
    else:
        invalid_count = sum(1 for r in fill_check.values() if not r['valid'])
        print(f"✗ {invalid_count} OF {len(fill_check)} ARRAYS HAVE ERRORS")
    print("=" * 70)

    return all_valid


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python fill_array_validator.py input.inp")
        print("\nValidates fill array dimensions in MCNP input files")
        print("Checks that array sizes match lattice declarations")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        if validate_fill_arrays(input_file):
            sys.exit(0)
        else:
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
