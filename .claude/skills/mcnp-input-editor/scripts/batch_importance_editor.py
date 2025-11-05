#!/usr/bin/env python3
"""
MCNP Batch Importance Editor

Systematically change importance values across cell cards with
smart handling of graveyard cells and pattern-based selection.

Usage:
    python batch_importance_editor.py input.i --set-all 1
    python batch_importance_editor.py input.i --old 2 --new 1
    python batch_importance_editor.py input.i --by-material 1:1 2:2 3:4

Author: MCNP Skills Project
Version: 2.0.0
"""

import argparse
import re
import sys
from pathlib import Path


class ImportanceEditor:
    """Batch editor for neutron importance values"""

    def __init__(self, filename):
        self.filename = Path(filename)
        self.lines = []
        self.cell_block_start = 0
        self.surface_block_start = 0

        if not self.filename.exists():
            raise FileNotFoundError(f"{filename} not found")

        self.load()

    def load(self):
        """Load input file and find cell block"""
        with open(self.filename, 'r') as f:
            self.lines = f.readlines()

        blank_count = 0
        for i, line in enumerate(self.lines):
            if line.strip() == '':
                blank_count += 1
                if blank_count == 1:
                    self.surface_block_start = i
                    break

        self.cell_block_start = 1  # After title

    def save(self, output_filename=None):
        """Save modified file"""
        filename = output_filename or self.filename
        with open(filename, 'w') as f:
            f.writelines(self.lines)
        print(f"Saved to {filename}")

    def set_all_importances(self, new_imp, exclude_zero=True, particle='N'):
        """Set all importance values to same value

        Args:
            new_imp: New importance value
            exclude_zero: If True, skip IMP:N=0 cells (graveyard)
            particle: Particle type ('N', 'P', 'E', etc.)

        Returns: Number of cells modified
        """
        pattern = re.compile(rf'IMP:{particle}=(\d+)')
        count = 0

        for i in range(self.cell_block_start, self.surface_block_start):
            match = pattern.search(self.lines[i])
            if match:
                old_value = int(match.group(1))

                # Skip if excluding zero and value is zero
                if exclude_zero and old_value == 0:
                    continue

                # Replace
                self.lines[i] = pattern.sub(f'IMP:{particle}={new_imp}', self.lines[i])
                count += 1

        print(f"Set IMP:{particle}={new_imp} for {count} cell(s)")
        if exclude_zero:
            print("(Graveyard cells with IMP:N=0 unchanged)")

        return count

    def change_importance(self, old_imp, new_imp, particle='N'):
        """Change specific importance value

        Args:
            old_imp: Old importance value to find
            new_imp: New importance value to set
            particle: Particle type

        Returns: Number of cells modified
        """
        pattern = f'IMP:{particle}={old_imp}'
        replacement = f'IMP:{particle}={new_imp}'
        count = 0

        for i in range(self.cell_block_start, self.surface_block_start):
            if pattern in self.lines[i]:
                self.lines[i] = self.lines[i].replace(pattern, replacement)
                count += 1

        print(f"Changed {count} cell(s): IMP:{particle}={old_imp} → {new_imp}")
        return count

    def set_by_material(self, material_importance_map, particle='N'):
        """Set importance based on material number

        Args:
            material_importance_map: Dict {material_num: importance_value}
            particle: Particle type

        Returns: Number of cells modified
        """
        count = 0

        for i in range(self.cell_block_start, self.surface_block_start):
            parts = self.lines[i].split()
            if len(parts) < 2:
                continue

            # Check if cell card
            if not parts[0].isdigit():
                continue

            # Get material number
            try:
                mat_num = int(parts[1])
            except ValueError:
                continue

            # Check if material is in map
            if mat_num in material_importance_map:
                new_imp = material_importance_map[mat_num]

                # Update or add IMP parameter
                pattern = re.compile(rf'IMP:{particle}=\d+')
                if pattern.search(self.lines[i]):
                    self.lines[i] = pattern.sub(f'IMP:{particle}={new_imp}', self.lines[i])
                else:
                    # Add IMP parameter
                    self.lines[i] = self.lines[i].rstrip() + f'  IMP:{particle}={new_imp}\n'

                count += 1

        print(f"Set importances for {count} cell(s) by material")
        return count

    def preview_changes(self, show_all=False):
        """Preview importance distribution

        Args:
            show_all: If True, show all cells. If False, show summary.
        """
        importance_counts = {}

        for i in range(self.cell_block_start, self.surface_block_start):
            match = re.search(r'IMP:N=(\d+)', self.lines[i])
            if match:
                imp_value = int(match.group(1))
                importance_counts[imp_value] = importance_counts.get(imp_value, 0) + 1

                if show_all:
                    parts = self.lines[i].split()
                    if len(parts) > 0:
                        cell_num = parts[0]
                        print(f"Cell {cell_num}: IMP:N={imp_value}")

        # Summary
        print("\nImportance Distribution:")
        for imp in sorted(importance_counts.keys()):
            print(f"  IMP:N={imp}: {importance_counts[imp]} cell(s)")

        return importance_counts


def main():
    parser = argparse.ArgumentParser(
        description='Batch MCNP Importance Editor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Set all importances to 1 (except graveyard)
  python batch_importance_editor.py input.i --set-all 1

  # Change all IMP:N=2 to IMP:N=1
  python batch_importance_editor.py input.i --old 2 --new 1

  # Set importances by material: mat 1→imp 1, mat 2→imp 2, mat 10→imp 4
  python batch_importance_editor.py input.i --by-material 1:1 2:2 10:4

  # Preview current importance distribution
  python batch_importance_editor.py input.i --preview

  # Include graveyard cells in changes
  python batch_importance_editor.py input.i --set-all 1 --include-zero
        """)

    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--output', '-o', help='Output filename (default: overwrite)')
    parser.add_argument('--set-all', type=int, metavar='IMP',
                        help='Set all importances to this value')
    parser.add_argument('--old', type=int, help='Old importance value to change')
    parser.add_argument('--new', type=int, help='New importance value')
    parser.add_argument('--by-material', nargs='+', metavar='MAT:IMP',
                        help='Set importance by material (e.g., 1:1 2:2 3:4)')
    parser.add_argument('--particle', default='N', help='Particle type (default: N)')
    parser.add_argument('--include-zero', action='store_true',
                        help='Include IMP:N=0 cells (graveyard) in changes')
    parser.add_argument('--preview', action='store_true',
                        help='Preview current importance distribution')

    args = parser.parse_args()

    try:
        editor = ImportanceEditor(args.input_file)

        # Preview mode
        if args.preview:
            editor.preview_changes(show_all=False)
            return 0

        # Set all importances
        if args.set_all is not None:
            editor.set_all_importances(args.set_all,
                                       exclude_zero=not args.include_zero,
                                       particle=args.particle)
            editor.save(args.output)
            return 0

        # Change specific value
        if args.old is not None:
            if args.new is None:
                print("Error: --new required with --old")
                return 1
            editor.change_importance(args.old, args.new, args.particle)
            editor.save(args.output)
            return 0

        # Set by material
        if args.by_material:
            mat_imp_map = {}
            for pair in args.by_material:
                try:
                    mat, imp = pair.split(':')
                    mat_imp_map[int(mat)] = int(imp)
                except ValueError:
                    print(f"Error: Invalid format '{pair}'. Use MAT:IMP (e.g., 1:2)")
                    return 1

            editor.set_by_material(mat_imp_map, args.particle)
            editor.save(args.output)
            return 0

        # No operation specified
        print("No operation specified. Use --help for usage.")
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
