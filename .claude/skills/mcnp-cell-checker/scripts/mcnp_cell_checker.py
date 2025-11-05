#!/usr/bin/env python3
"""
MCNP Cell Checker - Main Validation Class

Validates MCNP cell cards for universe, lattice, and fill correctness.

Usage:
    from mcnp_cell_checker import MCNPCellChecker

    checker = MCNPCellChecker()
    results = checker.check_cells('input.inp')

    if results['valid']:
        print("✓ All cell cards validated")
    else:
        print(f"✗ Found {len(results['errors'])} errors")
"""

import sys
import os
from pathlib import Path

# Add skill directory to path for imports
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from scripts.universe_validator import UniverseValidator
from scripts.lattice_validator import LatticeValidator
from scripts.dependency_tree_builder import DependencyTreeBuilder


class MCNPCellChecker:
    """Main cell card validation class"""

    def __init__(self):
        self.universe_validator = UniverseValidator()
        self.lattice_validator = LatticeValidator()
        self.tree_builder = DependencyTreeBuilder()

    def check_cells(self, input_file):
        """
        Comprehensive cell card validation

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict with keys:
                - 'valid': bool
                - 'errors': list of error messages
                - 'warnings': list of warning messages
                - 'info': list of informational messages
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }

        print(f"Validating cell cards in: {input_file}")
        print("=" * 70)

        # Step 1: Universe references
        print("\n[1/5] Checking universe references...")
        universe_results = self.universe_validator.validate_universes(input_file)

        if universe_results['undefined']:
            results['valid'] = False
            for u in universe_results['undefined']:
                results['errors'].append(
                    f"Universe {u} referenced in FILL but not defined with u={u}"
                )
        else:
            results['info'].append(
                f"All {len(universe_results['used'])} universe references valid"
            )

        unused = set(universe_results['defined']) - set(universe_results['used'])
        if unused:
            results['warnings'].append(f"Unused universe definitions: {unused}")

        # Step 2: Lattice types
        print("\n[2/5] Validating lattice specifications...")
        lattice_results = self.lattice_validator.validate_lattices(input_file)

        for cell_num, result in lattice_results.items():
            if result['errors']:
                results['valid'] = False
                results['errors'].extend(result['errors'])

        if not lattice_results:
            results['info'].append("No lattice cells found")
        else:
            results['info'].append(f"{len(lattice_results)} lattice cells validated")

        # Step 3: Fill array dimensions
        print("\n[3/5] Checking fill array dimensions...")
        fill_results = self.lattice_validator.check_fill_dimensions(input_file)

        for cell_num, result in fill_results.items():
            if result['expected_size'] != result['actual_size']:
                results['valid'] = False
                results['errors'].append(
                    f"Cell {cell_num}: Fill array size mismatch - "
                    f"expected {result['expected_size']}, found {result['actual_size']}"
                )

        # Step 4: Universe dependency tree
        print("\n[4/5] Building universe dependency tree...")
        tree_results = self.tree_builder.build_universe_tree(input_file)

        if tree_results['circular_refs']:
            results['valid'] = False
            for cycle in tree_results['circular_refs']:
                results['errors'].append(
                    f"Circular universe reference: {' → '.join(map(str, cycle))}"
                )

        if tree_results['max_depth'] > 10:
            results['warnings'].append(
                f"Deep nesting detected: {tree_results['max_depth']} levels "
                "(may impact performance)"
            )

        results['info'].append(f"Max universe nesting: {tree_results['max_depth']} levels")

        # Step 5: Lattice boundaries
        print("\n[5/5] Checking lattice boundary surfaces...")
        boundary_results = self.lattice_validator.check_lattice_boundaries(input_file)

        for cell_num, result in boundary_results.items():
            if not result['appropriate']:
                results['warnings'].extend(result['recommendations'])

        # Final summary
        print("\n" + "=" * 70)
        if results['valid']:
            print("✓ CELL VALIDATION PASSED")
        else:
            print("✗ CELL VALIDATION FAILED")
            print(f"  Errors: {len(results['errors'])}")

        if results['warnings']:
            print(f"  Warnings: {len(results['warnings'])}")

        print("=" * 70)

        return results


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python mcnp_cell_checker.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)

    checker = MCNPCellChecker()
    results = checker.check_cells(input_file)

    # Print errors
    if results['errors']:
        print("\n❌ ERRORS:")
        for err in results['errors']:
            print(f"  • {err}")

    # Print warnings
    if results['warnings']:
        print("\n⚠ WARNINGS:")
        for warn in results['warnings']:
            print(f"  • {warn}")

    # Print info
    if results['info']:
        print("\n📝 INFO:")
        for info in results['info']:
            print(f"  • {info}")

    # Exit with appropriate code
    sys.exit(0 if results['valid'] else 1)


if __name__ == "__main__":
    main()
