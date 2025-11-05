#!/usr/bin/env python3
"""
Pre-Run Cell Validation Script

Comprehensive cell card validation before MCNP execution.
Runs all 5 validation procedures and reports results.

Usage:
    python validate_cells_prerun.py input.inp

Exit codes:
    0 - All validations passed
    1 - Validation failures detected
"""

import sys
from mcnp_cell_checker import MCNPCellChecker


def validate_cell_cards(input_file):
    """
    Complete cell card validation workflow

    Args:
        input_file: Path to MCNP input file

    Returns:
        True if all validations passed, False otherwise
    """
    print(f"{'='*70}")
    print(f"MCNP Cell Card Validation: {input_file}")
    print(f"{'='*70}")

    checker = MCNPCellChecker()

    # Step 1: Universe references
    print("\n[1/5] Checking universe references...")
    universe_check = checker.validate_universes(input_file)

    if universe_check['undefined']:
        print("  ❌ FATAL: Undefined universe references")
        for u in universe_check['undefined']:
            print(f"     Universe {u} referenced in FILL but not defined")
        return False
    else:
        defined_count = len(universe_check['defined'])
        used_count = len(universe_check['used'])
        print(f"  ✓ All {used_count} universe references valid")
        print(f"    {defined_count} universes defined")

    # Check for unused universes
    unused = set(universe_check['defined']) - set(universe_check['used'])
    if unused:
        print(f"  ⚠ WARNING: {len(unused)} unused universes: {sorted(unused)}")

    # Step 2: Lattice specifications
    print("\n[2/5] Validating lattice specifications...")
    lattice_results = checker.validate_lattices(input_file)

    if not lattice_results:
        print("  ℹ No lattice cells found")
    else:
        lattice_errors = []
        for cell_num, result in lattice_results.items():
            if result['errors']:
                lattice_errors.extend(
                    [f"Cell {cell_num}: {err}" for err in result['errors']]
                )

        if lattice_errors:
            print(f"  ❌ FATAL: {len(lattice_errors)} lattice errors")
            for err in lattice_errors:
                print(f"     {err}")
            return False
        else:
            print(f"  ✓ All {len(lattice_results)} lattice cells valid")

    # Step 3: Fill array dimensions
    print("\n[3/5] Checking fill array dimensions...")
    fill_check = checker.check_fill_dimensions(input_file)

    if not fill_check:
        print("  ℹ No fill arrays found")
    else:
        dimension_errors = []
        for cell_num, result in fill_check.items():
            if not result['valid']:
                diff = result['actual_size'] - result['expected_size']
                dimension_errors.append(
                    f"Cell {cell_num}: Expected {result['expected_size']} "
                    f"values, found {result['actual_size']} ({diff:+d})"
                )

        if dimension_errors:
            print(f"  ❌ FATAL: {len(dimension_errors)} dimension mismatches")
            for err in dimension_errors:
                print(f"     {err}")
            return False
        else:
            print(f"  ✓ All {len(fill_check)} fill arrays have correct dimensions")

    # Step 4: Universe dependency tree
    print("\n[4/5] Building universe dependency tree...")
    tree = checker.build_universe_tree(input_file)

    if tree['circular_refs']:
        print("  ❌ FATAL: Circular universe references detected")
        for cycle in tree['circular_refs']:
            print(f"     {' → '.join(map(str, cycle))}")
        return False
    else:
        print(f"  ✓ No circular references")
        print(f"    Maximum nesting depth: {tree['max_depth']} levels")

    # Performance warnings
    if tree['max_depth'] > 10:
        print(f"  ⚠ WARNING: Deep nesting ({tree['max_depth']} levels)")
        print("     Performance impact expected")
        print("     Consider optimization strategies")
    elif tree['max_depth'] > 7:
        print(f"  ℹ Nesting depth ({tree['max_depth']} levels) is acceptable")
        print("    Consider negative universe optimization for levels 3+")

    # Check for unreachable universes
    if tree['unreachable']:
        print(f"  ⚠ WARNING: {len(tree['unreachable'])} unreachable universes")
        print(f"     {tree['unreachable']}")

    # Step 5: Lattice boundary surfaces
    print("\n[5/5] Checking lattice boundary surfaces...")
    boundary_check = checker.check_lattice_boundaries(input_file)

    if not boundary_check:
        print("  ℹ No lattice cells to check")
    else:
        boundary_warnings = []
        for cell_num, result in boundary_check.items():
            if not result['appropriate']:
                for rec in result['recommendations']:
                    boundary_warnings.append(f"Cell {cell_num}: {rec}")

        if boundary_warnings:
            print(f"  ⚠ {len(boundary_warnings)} boundary recommendations:")
            # Show first 3
            for warn in boundary_warnings[:3]:
                print(f"     {warn}")
            if len(boundary_warnings) > 3:
                print(f"     ... and {len(boundary_warnings) - 3} more")
        else:
            print(f"  ✓ All {len(boundary_check)} lattice boundaries appropriate")

    # Final summary
    print(f"\n{'='*70}")
    print("✓ CELL VALIDATION PASSED")
    print(f"{'='*70}")
    print("\nSummary:")
    print(f"  • {len(universe_check['defined'])} universes defined")
    print(f"  • {len(lattice_results)} lattice cells")
    if fill_check:
        print(f"  • {len(fill_check)} fill arrays")
    print(f"  • {tree['max_depth']} levels of nesting")
    print(f"\nReady for MCNP execution:")
    print(f"  mcnp6 i={input_file}")
    print(f"{'='*70}")

    return True


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate_cells_prerun.py input.inp")
        print("\nValidates MCNP cell cards before execution:")
        print("  - Universe references (U/FILL)")
        print("  - Lattice specifications (LAT=1 or LAT=2)")
        print("  - Fill array dimensions")
        print("  - Universe dependency hierarchy")
        print("  - Lattice boundary surfaces")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        if validate_cell_cards(input_file):
            print(f"\n✓ Ready to run MCNP")
            sys.exit(0)
        else:
            print(f"\n✗ Fix cell card errors before running MCNP")
            sys.exit(1)
    except FileNotFoundError:
        print(f"\n✗ Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during validation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
