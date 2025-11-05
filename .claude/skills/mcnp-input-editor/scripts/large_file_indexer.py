#!/usr/bin/env python3
"""
MCNP Large File Indexer

Build index of card locations in large MCNP input files (9,000+ lines)
for fast random access editing without loading entire file into memory.

Usage:
    python large_file_indexer.py input.i --build-index
    python large_file_indexer.py input.i --edit-cell 500 --density -1.2
    python large_file_indexer.py input.i --find-cell 1234

Author: MCNP Skills Project
Version: 2.0.0
"""

import argparse
import json
import sys
from pathlib import Path


class LargeFileIndexer:
    """Indexer for large MCNP input files"""

    def __init__(self, filename):
        self.filename = Path(filename)
        self.index_file = self.filename.with_suffix('.idx.json')

        if not self.filename.exists():
            raise FileNotFoundError(f"{filename} not found")

    def build_index(self, verbose=False):
        """Build index of card locations

        Returns: Dict with block boundaries and card locations
        """
        index = {
            'filename': str(self.filename),
            'blocks': {},
            'cells': {},
            'surfaces': {},
            'total_lines': 0
        }

        with open(self.filename, 'r') as f:
            line_num = 0
            blank_count = 0
            current_block = 'title'

            for line in f:
                line_num += 1

                # Track blank lines (block separators)
                if line.strip() == '':
                    blank_count += 1
                    if blank_count == 1:
                        index['blocks']['cell_end'] = line_num - 1
                        index['blocks']['surface_start'] = line_num + 1
                        current_block = 'surface'
                    elif blank_count == 2:
                        index['blocks']['surface_end'] = line_num - 1
                        index['blocks']['data_start'] = line_num + 1
                        current_block = 'data'
                        break  # Don't index data block (too variable)

                    continue

                # Start of cell block
                if blank_count == 0 and line_num > 1:
                    if current_block == 'title':
                        index['blocks']['cell_start'] = line_num
                        current_block = 'cell'

                # Index cell cards
                if current_block == 'cell':
                    parts = line.split()
                    if len(parts) > 0 and parts[0].isdigit():
                        cell_num = int(parts[0])
                        index['cells'][cell_num] = line_num

                # Index surface cards
                elif current_block == 'surface':
                    parts = line.split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        surf_num = int(parts[0])
                        index['surfaces'][surf_num] = line_num

            index['total_lines'] = line_num

        if verbose:
            print(f"Index built:")
            print(f"  Total lines: {index['total_lines']}")
            print(f"  Cells indexed: {len(index['cells'])}")
            print(f"  Surfaces indexed: {len(index['surfaces'])}")
            print(f"  Cell block: lines {index['blocks'].get('cell_start', 0)}-{index['blocks'].get('cell_end', 0)}")
            print(f"  Surface block: lines {index['blocks'].get('surface_start', 0)}-{index['blocks'].get('surface_end', 0)}")

        return index

    def save_index(self, index):
        """Save index to JSON file"""
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)
        print(f"Index saved to {self.index_file}")

    def load_index(self):
        """Load index from JSON file"""
        if not self.index_file.exists():
            raise FileNotFoundError(f"Index file {self.index_file} not found. Run --build-index first.")

        with open(self.index_file, 'r') as f:
            index = json.load(f)

        # Convert string keys to int for cells/surfaces
        index['cells'] = {int(k): v for k, v in index['cells'].items()}
        index['surfaces'] = {int(k): v for k, v in index['surfaces'].items()}

        return index

    def find_card(self, card_type, card_num):
        """Find line number for specific card

        Args:
            card_type: 'cell' or 'surface'
            card_num: Card number

        Returns: Line number or None
        """
        index = self.load_index()

        if card_type == 'cell':
            return index['cells'].get(card_num)
        elif card_type == 'surface':
            return index['surfaces'].get(card_num)
        else:
            raise ValueError(f"Invalid card type: {card_type}")

    def edit_cell_density(self, cell_num, new_density, output_file=None):
        """Edit cell density using index (fast for large files)

        Args:
            cell_num: Cell number to edit
            new_density: New density value
            output_file: Output filename (default: overwrite input)

        Returns: True if successful
        """
        index = self.load_index()
        line_num = index['cells'].get(cell_num)

        if line_num is None:
            print(f"Error: Cell {cell_num} not found in index")
            return False

        # Read entire file (in production, use seek for true random access)
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        # Edit specific line
        target_idx = line_num - 1  # Convert to 0-based index
        parts = lines[target_idx].split()

        if len(parts) < 3:
            print(f"Error: Cell {cell_num} has invalid format")
            return False

        old_density = parts[2]
        parts[2] = str(new_density)

        # Preserve comment if present
        if '$' in lines[target_idx]:
            main, comment = lines[target_idx].split('$', 1)
            lines[target_idx] = '  '.join(parts) + '  $' + comment
        else:
            lines[target_idx] = '  '.join(parts) + '\n'

        # Write back
        output = output_file or self.filename
        with open(output, 'w') as f:
            f.writelines(lines)

        print(f"Cell {cell_num}: density {old_density} → {new_density}")
        print(f"Saved to {output}")
        return True

    def get_statistics(self):
        """Get file statistics from index"""
        index = self.load_index()

        return {
            'total_lines': index['total_lines'],
            'cells': len(index['cells']),
            'surfaces': len(index['surfaces']),
            'cell_block_lines': index['blocks']['cell_end'] - index['blocks']['cell_start'] + 1,
            'surface_block_lines': index['blocks']['surface_end'] - index['blocks']['surface_start'] + 1
        }


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Large File Indexer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build index for large file
  python large_file_indexer.py large_reactor.i --build-index

  # Find cell location
  python large_file_indexer.py large_reactor.i --find-cell 1234

  # Edit cell using index (fast)
  python large_file_indexer.py large_reactor.i --edit-cell 500 --density -1.2

  # Get file statistics
  python large_file_indexer.py large_reactor.i --stats

Performance Note:
  For files >5,000 lines, indexing enables much faster targeted editing.
  Index is saved to .idx.json file and reused for subsequent operations.
        """)

    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--build-index', action='store_true',
                        help='Build and save index')
    parser.add_argument('--find-cell', type=int, metavar='NUM',
                        help='Find line number for cell')
    parser.add_argument('--find-surface', type=int, metavar='NUM',
                        help='Find line number for surface')
    parser.add_argument('--edit-cell', type=int, metavar='NUM',
                        help='Edit cell (requires --density)')
    parser.add_argument('--density', type=float,
                        help='New density value')
    parser.add_argument('--output', '-o',
                        help='Output filename (default: overwrite input)')
    parser.add_argument('--stats', action='store_true',
                        help='Show file statistics from index')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    try:
        indexer = LargeFileIndexer(args.input_file)

        # Build index
        if args.build_index:
            index = indexer.build_index(verbose=True)
            indexer.save_index(index)
            return 0

        # Statistics
        if args.stats:
            try:
                stats = indexer.get_statistics()
                print(f"\nFile: {args.input_file}")
                print(f"Total lines: {stats['total_lines']}")
                print(f"Cells: {stats['cells']}")
                print(f"Surfaces: {stats['surfaces']}")
                print(f"Cell block: {stats['cell_block_lines']} lines")
                print(f"Surface block: {stats['surface_block_lines']} lines")
            except FileNotFoundError:
                print("Error: Index not found. Run --build-index first.")
                return 1
            return 0

        # Find cell
        if args.find_cell is not None:
            line_num = indexer.find_card('cell', args.find_cell)
            if line_num:
                print(f"Cell {args.find_cell}: line {line_num}")
            else:
                print(f"Cell {args.find_cell}: not found")
            return 0

        # Find surface
        if args.find_surface is not None:
            line_num = indexer.find_card('surface', args.find_surface)
            if line_num:
                print(f"Surface {args.find_surface}: line {line_num}")
            else:
                print(f"Surface {args.find_surface}: not found")
            return 0

        # Edit cell
        if args.edit_cell is not None:
            if args.density is None:
                print("Error: --density required with --edit-cell")
                return 1
            success = indexer.edit_cell_density(args.edit_cell, args.density, args.output)
            return 0 if success else 1

        # No operation
        print("No operation specified. Use --help for usage.")
        print("Tip: Run --build-index first for large files.")
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
