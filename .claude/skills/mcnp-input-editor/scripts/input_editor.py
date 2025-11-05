#!/usr/bin/env python3
"""
MCNP Input Editor

General-purpose MCNP input file editor with find/replace, batch editing,
and structure-preserving modifications.

Usage:
    python input_editor.py input.i --find "IMP:N=2" --replace "IMP:N=1"
    python input_editor.py input.i --cell 100 --density -1.2
    python input_editor.py input.i --validate

Author: MCNP Skills Project
Version: 2.0.0
"""

import argparse
import re
import sys
from pathlib import Path


class MCNPInputEditor:
    """MCNP input file editor with structure preservation"""

    def __init__(self, filename):
        self.filename = Path(filename)
        self.lines = []
        self.cell_block_start = 0
        self.surface_block_start = 0
        self.data_block_start = 0
        self.title_line = ""

        if not self.filename.exists():
            raise FileNotFoundError(f"{filename} not found")

        self.load()

    def load(self):
        """Load MCNP input file and index block locations"""
        with open(self.filename, 'r') as f:
            self.lines = f.readlines()

        if not self.lines:
            raise ValueError("Empty input file")

        self.title_line = self.lines[0]

        # Find block boundaries (marked by blank lines)
        blank_count = 0
        for i, line in enumerate(self.lines):
            if line.strip() == '':
                blank_count += 1
                if blank_count == 1:
                    self.surface_block_start = i + 1
                elif blank_count == 2:
                    self.data_block_start = i + 1
                    break

        self.cell_block_start = 1  # After title

    def save(self, output_filename=None):
        """Save modified input file"""
        filename = output_filename or self.filename
        with open(filename, 'w') as f:
            f.writelines(self.lines)
        print(f"Saved to {filename}")

    def find_cell(self, cell_num):
        """Find line number for specific cell

        Returns: Line index or None if not found
        """
        for i in range(self.cell_block_start, self.surface_block_start - 1):
            if i >= len(self.lines):
                break
            parts = self.lines[i].split()
            if len(parts) > 0 and parts[0] == str(cell_num):
                return i
        return None

    def edit_cell_density(self, cell_num, new_density):
        """Change density of specific cell

        Args:
            cell_num: Cell number to modify
            new_density: New density value

        Returns: True if successful, False otherwise
        """
        line_idx = self.find_cell(cell_num)
        if line_idx is None:
            print(f"Error: Cell {cell_num} not found")
            return False

        parts = self.lines[line_idx].split()
        if len(parts) < 3:
            print(f"Error: Cell {cell_num} has invalid format")
            return False

        old_density = parts[2]
        parts[2] = str(new_density)

        # Preserve inline comment if present
        if '$' in self.lines[line_idx]:
            main, comment = self.lines[line_idx].split('$', 1)
            self.lines[line_idx] = '  '.join(parts) + '  $' + comment
        else:
            self.lines[line_idx] = '  '.join(parts) + '\n'

        print(f"Cell {cell_num}: density {old_density} → {new_density}")
        return True

    def batch_find_replace(self, find_pattern, replace_text, regex=False, preview=False):
        """Find and replace across entire file

        Args:
            find_pattern: Text or regex pattern to find
            replace_text: Replacement text
            regex: True to use regex, False for literal
            preview: True to show changes without applying

        Returns: Number of replacements made
        """
        count = 0
        modified_lines = []

        for i, line in enumerate(self.lines):
            if regex:
                new_line, n = re.subn(find_pattern, replace_text, line)
            else:
                if find_pattern in line:
                    new_line = line.replace(find_pattern, replace_text)
                    n = 1
                else:
                    new_line = line
                    n = 0

            if n > 0:
                count += n
                if preview:
                    print(f"Line {i+1}:")
                    print(f"  Before: {line.rstrip()}")
                    print(f"  After:  {new_line.rstrip()}")

            modified_lines.append(new_line)

        if not preview:
            self.lines = modified_lines
            print(f"Replaced {count} occurrence(s)")
        else:
            print(f"\nPreview: {count} replacement(s) would be made")
            print("Run without --preview to apply changes")

        return count

    def batch_importance_change(self, old_imp, new_imp, exclude_zero=True):
        """Change all importance values

        Args:
            old_imp: Old importance value
            new_imp: New importance value
            exclude_zero: If True, skip IMP:N=0 (graveyard)

        Returns: Number of changes made
        """
        pattern = f'IMP:N={old_imp}'
        replacement = f'IMP:N={new_imp}'

        if exclude_zero and old_imp == 0:
            print("Warning: Not changing IMP:N=0 (graveyard cells)")
            return 0

        count = 0
        for i in range(self.cell_block_start, self.surface_block_start - 1):
            if i >= len(self.lines):
                break

            if pattern in self.lines[i]:
                self.lines[i] = self.lines[i].replace(pattern, replacement)
                count += 1

        print(f"Changed {count} cell(s): IMP:N={old_imp} → IMP:N={new_imp}")
        return count

    def validate_structure(self):
        """Validate three-block structure

        Returns: List of errors (empty if valid)
        """
        errors = []

        # Check for exactly 2 blank lines
        blank_lines = [i for i, line in enumerate(self.lines) if line.strip() == '']
        if len(blank_lines) < 2:
            errors.append("Missing blank line separators (need exactly 2)")

        # Check title exists
        if not self.title_line or self.title_line.strip() == '':
            errors.append("Missing title line")

        # Check blocks exist
        if self.surface_block_start == 0:
            errors.append("Surface block not found")
        if self.data_block_start == 0:
            errors.append("Data block not found")

        # Validate cell cards
        for i in range(self.cell_block_start, self.surface_block_start - 1):
            if i >= len(self.lines):
                break
            parts = self.lines[i].split()
            if len(parts) >= 3:
                if not parts[0].isdigit():
                    errors.append(f"Line {i+1}: Invalid cell number")
                if not (parts[1].isdigit() or parts[1] == '0'):
                    errors.append(f"Line {i+1}: Invalid material number")

        if errors:
            print("Validation errors found:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✓ Input file structure valid")

        return errors

    def get_statistics(self):
        """Get file statistics"""
        stats = {
            'total_lines': len(self.lines),
            'cell_count': 0,
            'surface_count': 0,
            'material_count': 0
        }

        # Count cells
        for i in range(self.cell_block_start, self.surface_block_start - 1):
            if i >= len(self.lines):
                break
            parts = self.lines[i].split()
            if len(parts) > 0 and parts[0].isdigit():
                stats['cell_count'] += 1

        # Count surfaces
        for i in range(self.surface_block_start, self.data_block_start - 1):
            if i >= len(self.lines):
                break
            parts = self.lines[i].split()
            if len(parts) > 0 and parts[0].isdigit():
                stats['surface_count'] += 1

        # Count materials
        for i in range(self.data_block_start, len(self.lines)):
            line = self.lines[i].strip()
            if line.startswith('M') and not line.startswith('MODE'):
                parts = line.split()
                if len(parts) > 0 and parts[0][1:].isdigit():
                    stats['material_count'] += 1

        return stats


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Input File Editor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Change cell 100 density
  python input_editor.py input.i --cell 100 --density -1.2

  # Batch find/replace
  python input_editor.py input.i --find "IMP:N=2" --replace "IMP:N=1"

  # Regex replace (ZAID library update)
  python input_editor.py input.i --find "\\.70c" --replace ".80c" --regex

  # Preview changes without applying
  python input_editor.py input.i --find "IMP:N=2" --replace "IMP:N=1" --preview

  # Validate file structure
  python input_editor.py input.i --validate

  # Get file statistics
  python input_editor.py input.i --stats
        """)

    parser.add_argument('input_file', help='MCNP input file to edit')
    parser.add_argument('--output', '-o', help='Output filename (default: overwrite input)')
    parser.add_argument('--cell', type=int, help='Cell number to edit')
    parser.add_argument('--density', type=float, help='New density for cell')
    parser.add_argument('--find', help='Text to find')
    parser.add_argument('--replace', help='Replacement text')
    parser.add_argument('--regex', action='store_true', help='Use regex for find/replace')
    parser.add_argument('--preview', action='store_true', help='Preview changes without applying')
    parser.add_argument('--validate', action='store_true', help='Validate file structure')
    parser.add_argument('--stats', action='store_true', help='Show file statistics')

    args = parser.parse_args()

    try:
        editor = MCNPInputEditor(args.input_file)

        # Statistics mode
        if args.stats:
            stats = editor.get_statistics()
            print(f"\nFile: {args.input_file}")
            print(f"Total lines: {stats['total_lines']}")
            print(f"Cells: {stats['cell_count']}")
            print(f"Surfaces: {stats['surface_count']}")
            print(f"Materials: {stats['material_count']}")
            return 0

        # Validation mode
        if args.validate:
            errors = editor.validate_structure()
            return 0 if not errors else 1

        # Edit cell density
        if args.cell is not None:
            if args.density is None:
                print("Error: --density required with --cell")
                return 1
            editor.edit_cell_density(args.cell, args.density)
            editor.save(args.output)
            return 0

        # Find/replace
        if args.find is not None:
            if args.replace is None:
                print("Error: --replace required with --find")
                return 1
            editor.batch_find_replace(args.find, args.replace, args.regex, args.preview)
            if not args.preview:
                editor.save(args.output)
            return 0

        # No operation specified
        print("No operation specified. Use --help for usage information.")
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
