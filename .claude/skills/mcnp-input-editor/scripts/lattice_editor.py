#!/usr/bin/env python3
"""
Lattice Editor for MCNP Inputs

Safely edit lattice fill arrays while preserving dimension constraints.

CRITICAL: Lattice fill arrays have EXACT dimension requirements.
fill=-7:7 -7:7 0:0 requires (7-(-7)+1)×(7-(-7)+1)×(0-0+1) = 15×15×1 = 225 elements!

Usage:
    python lattice_editor.py input.i --cell 200 --replace-universe 100 101
    python lattice_editor.py input.i --cell 200 --validate
    python lattice_editor.py input.i --cell 300 --expand-k -15:15 -16:16 --fill-pattern "100 2R 200 26R 100 2R"

Author: MCNP Skills Project
Version: 3.0.0
"""

import re
import sys
import argparse
from pathlib import Path


class LatticeEditor:
    """Edit MCNP lattice cells safely"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.lines = []
        self.lattice_cells = {}

        if not self.file_path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        with open(self.file_path, 'r') as f:
            self.lines = f.readlines()

        self._parse_lattices()

    def _parse_lattices(self):
        """Find all lattice cells in file"""
        in_cells = True  # Assume we start in cells block
        current_cell = None
        current_cell_lines = []

        for i, line in enumerate(self.lines):
            # Skip comments and blank lines
            if line.strip().startswith('c') or line.strip().startswith('C'):
                continue

            # Detect blank line (section separator)
            if re.match(r'^\s*$', line):
                in_cells = False  # After first blank, no longer in cells
                continue

            # Look for LAT= parameter in cells block
            if in_cells or 'lat=' in line.lower() or 'lat =' in line.lower():
                # Check if this line starts a new cell (starts with number)
                cell_match = re.match(r'^\s*(\d+)\s', line)

                if cell_match:
                    # Save previous cell if it was a lattice
                    if current_cell is not None and any('lat=' in l.lower() for l in [cl[1] for cl in current_cell_lines]):
                        self._process_lattice_cell(current_cell, current_cell_lines)

                    # Start new cell
                    current_cell = int(cell_match.group(1))
                    current_cell_lines = [(i, line)]
                elif current_cell is not None:
                    # Continuation line (starts with spaces or &)
                    if line.startswith('     ') or line.lstrip().startswith('&'):
                        current_cell_lines.append((i, line))
                    else:
                        # End of current cell
                        if any('lat=' in l.lower() for l in [cl[1] for cl in current_cell_lines]):
                            self._process_lattice_cell(current_cell, current_cell_lines)
                        current_cell = None
                        current_cell_lines = []

        # Process last cell if lattice
        if current_cell is not None and any('lat=' in l.lower() for l in [cl[1] for cl in current_cell_lines]):
            self._process_lattice_cell(current_cell, current_cell_lines)

    def _process_lattice_cell(self, cell_num, cell_lines):
        """Process a lattice cell and extract fill array"""
        # Find fill array (may span multiple lines)
        fill_lines = self._extract_fill_array(cell_lines)

        self.lattice_cells[cell_num] = {
            'cell_lines': cell_lines,
            'fill_lines': fill_lines
        }

    def _extract_fill_array(self, cell_lines):
        """Extract complete fill array from cell lines"""
        fill_lines = []
        in_fill = False

        for line_num, line in cell_lines:
            # Look for fill= start
            if 'fill=' in line.lower():
                in_fill = True
                fill_lines.append((line_num, line))
                continue

            # If in fill, include continuation lines
            if in_fill:
                # Check for continuation (starts with spaces or &)
                if line.startswith('     ') or line.lstrip().startswith('&'):
                    fill_lines.append((line_num, line))
                else:
                    break  # End of fill array

        return fill_lines

    def replace_universe(self, cell_num, old_u, new_u, validate=True):
        """
        Replace all instances of universe old_u with new_u in lattice

        Args:
            cell_num: Lattice cell number
            old_u: Universe number to replace
            new_u: New universe number
            validate: Validate element count after replacement

        Returns:
            bool: True if successful
        """
        if cell_num not in self.lattice_cells:
            print(f"ERROR: Cell {cell_num} is not a lattice cell")
            print(f"Available lattice cells: {list(self.lattice_cells.keys())}")
            return False

        lattice = self.lattice_cells[cell_num]
        fill_lines = lattice['fill_lines']

        # Replace in fill array
        replacements = 0
        for line_num, line in fill_lines:
            # Use word boundaries to avoid partial matches
            # Replace "100" but not "1001" or "2100"
            pattern = r'\b' + str(old_u) + r'\b'
            new_line = re.sub(pattern, str(new_u), line)

            if new_line != line:
                self.lines[line_num] = new_line
                replacements += 1

        print(f"Replaced universe {old_u} → {new_u} in cell {cell_num}: {replacements} line(s) modified")

        if validate:
            return self.validate_lattice(cell_num)

        return True

    def validate_lattice(self, cell_num):
        """
        Validate that lattice dimensions match element count

        Returns:
            bool: True if valid, False otherwise
        """
        if cell_num not in self.lattice_cells:
            print(f"ERROR: Cell {cell_num} is not a lattice cell")
            return False

        lattice = self.lattice_cells[cell_num]
        cell_lines = lattice['cell_lines']

        # Extract fill dimensions from cell card
        # Pattern: fill=IMIN:IMAX JMIN:JMAX KMIN:KMAX
        cell_text = ''.join([line for _, line in cell_lines])
        fill_match = re.search(r'fill\s*=\s*(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)',
                              cell_text, re.IGNORECASE)

        if not fill_match:
            print(f"ERROR: Could not parse fill dimensions for cell {cell_num}")
            return False

        imin, imax, jmin, jmax, kmin, kmax = map(int, fill_match.groups())

        # Calculate required elements
        i_count = imax - imin + 1
        j_count = jmax - jmin + 1
        k_count = kmax - kmin + 1
        required_elements = i_count * j_count * k_count

        # Count actual elements in fill array
        fill_text = ""
        for _, line in lattice['fill_lines']:
            fill_text += line

        # Remove 'fill=...' part, keep only universe numbers
        fill_text = re.sub(r'fill\s*=\s*-?\d+:-?\d+\s+-?\d+:-?\d+\s+-?\d+:-?\d+\s*', '', fill_text, flags=re.IGNORECASE)

        # Expand repeat notation (nR → n+1 copies)
        fill_text = self._expand_repeat_notation(fill_text)

        # Count universe numbers
        universe_numbers = re.findall(r'\b\d+\b', fill_text)
        actual_elements = len(universe_numbers)

        # Validate
        if actual_elements != required_elements:
            print(f"ERROR: Dimension mismatch in cell {cell_num}")
            print(f"  Dimensions: {imin}:{imax} {jmin}:{jmax} {kmin}:{kmax}")
            print(f"  Required elements: {i_count} × {j_count} × {k_count} = {required_elements}")
            print(f"  Actual elements: {actual_elements}")
            print(f"  Difference: {actual_elements - required_elements}")
            return False

        print(f"✓ Cell {cell_num}: {actual_elements} elements matches {i_count}×{j_count}×{k_count}")
        return True

    def _expand_repeat_notation(self, text):
        """
        Expand repeat notation: '100 2R' → '100 100 100'

        CRITICAL: nR means n+1 total copies!
        - 2R means 3 copies (original + 2 repeats)
        - 24R means 25 copies
        """
        def expand_match(match):
            universe = match.group(1)
            repeat_count = int(match.group(2))
            # nR = n+1 copies (original + n repeats)
            return ' '.join([universe] * (repeat_count + 1))

        # Match: universe_number whitespace repeat_countR
        # Example: "100 2R" → expand_match captures universe=100, repeat_count=2
        pattern = r'(\d+)\s+(\d+)[Rr]'
        expanded = re.sub(pattern, expand_match, text, flags=re.IGNORECASE)

        return expanded

    def list_lattices(self):
        """List all lattice cells found in file"""
        if not self.lattice_cells:
            print("No lattice cells found in file")
            return

        print(f"\nLattice cells in {self.file_path}:")
        print(f"{'='*70}")
        for cell_num in sorted(self.lattice_cells.keys()):
            lattice = self.lattice_cells[cell_num]
            cell_lines = lattice['cell_lines']
            cell_text = ''.join([line for _, line in cell_lines])

            # Extract LAT type
            lat_match = re.search(r'lat\s*=\s*(\d+)', cell_text, re.IGNORECASE)
            lat_type = lat_match.group(1) if lat_match else "?"

            # Extract fill dimensions
            fill_match = re.search(r'fill\s*=\s*(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)',
                                  cell_text, re.IGNORECASE)
            if fill_match:
                imin, imax, jmin, jmax, kmin, kmax = map(int, fill_match.groups())
                i_count = imax - imin + 1
                j_count = jmax - jmin + 1
                k_count = kmax - kmin + 1
                required = i_count * j_count * k_count

                lat_name = "rectangular" if lat_type == "1" else "hexagonal" if lat_type == "2" else "unknown"

                print(f"Cell {cell_num}: LAT={lat_type} ({lat_name})")
                print(f"  Dimensions: {imin}:{imax} {jmin}:{jmax} {kmin}:{kmax}")
                print(f"  Required elements: {i_count}×{j_count}×{k_count} = {required}")
            else:
                print(f"Cell {cell_num}: LAT={lat_type}")
                print(f"  Could not parse fill dimensions")
            print()

    def save(self, output_path=None):
        """Save edited file"""
        if output_path is None:
            output_path = self.file_path

        # Create backup
        backup_path = str(self.file_path) + '.bak'
        with open(backup_path, 'w') as f:
            with open(self.file_path, 'r') as orig:
                f.write(orig.read())

        with open(output_path, 'w') as f:
            f.writelines(self.lines)

        print(f"Saved to: {output_path}")
        print(f"Backup: {backup_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Edit MCNP lattice cells safely',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # List all lattice cells in file
  python lattice_editor.py input.i --list

  # Replace universe 100 with 101 in cell 200
  python lattice_editor.py input.i --cell 200 --replace-universe 100 101

  # Validate lattice dimensions
  python lattice_editor.py input.i --cell 200 --validate

  # Replace and validate
  python lattice_editor.py input.i --cell 200 --replace-universe 100 101 --output modified.i

CRITICAL NOTES:
  - Lattice dimensions MUST match element count EXACTLY
  - Repeat notation: nR = n+1 copies (2R = 3 copies, 24R = 25 copies)
  - For LAT=1 (rectangular): RPP must contain N × pitch
  - For LAT=2 (hexagonal): RHP must contain N × (R×√3)
  - Always validate after editing with --validate
        '''
    )

    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--cell', type=int, help='Lattice cell number to edit')
    parser.add_argument('--replace-universe', nargs=2, metavar=('OLD', 'NEW'), type=int,
                       help='Replace universe OLD with NEW')
    parser.add_argument('--validate', action='store_true', help='Validate lattice after editing')
    parser.add_argument('--list', action='store_true', help='List all lattice cells')
    parser.add_argument('--output', help='Output file (default: overwrite input)')

    args = parser.parse_args()

    try:
        editor = LatticeEditor(args.input_file)

        # List mode
        if args.list:
            editor.list_lattices()
            return 0

        # Validate mode
        if args.validate and args.cell:
            if editor.validate_lattice(args.cell):
                return 0
            else:
                return 1

        # Replace mode
        if args.replace_universe:
            if not args.cell:
                print("ERROR: --cell required when using --replace-universe")
                return 1

            old_u, new_u = args.replace_universe
            success = editor.replace_universe(args.cell, old_u, new_u, validate=True)

            if success:
                editor.save(args.output)
                return 0
            else:
                print("Editing failed, file not saved")
                return 1

        # No operation specified
        print("No operation specified. Use --help for usage.")
        print("Tip: Use --list to see lattice cells in file")
        return 1

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
