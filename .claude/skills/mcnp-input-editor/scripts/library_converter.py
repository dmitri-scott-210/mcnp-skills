#!/usr/bin/env python3
"""
MCNP Library Converter

Convert ZAID cross-section library identifiers between ENDF versions
(e.g., .70c → .80c for ENDF/B-VII.0 to ENDF/B-VIII.0).

Usage:
    python library_converter.py input.i --old 70c --new 80c
    python library_converter.py input.i --old 70c --new 80c --check-availability

Author: MCNP Skills Project
Version: 2.0.0
"""

import argparse
import re
import sys
from pathlib import Path


class LibraryConverter:
    """Convert ZAID cross-section libraries"""

    def __init__(self, filename):
        self.filename = Path(filename)
        self.lines = []

        if not self.filename.exists():
            raise FileNotFoundError(f"{filename} not found")

        self.load()

    def load(self):
        """Load input file"""
        with open(self.filename, 'r') as f:
            self.lines = f.readlines()

    def save(self, output_filename=None):
        """Save modified file"""
        filename = output_filename or self.filename
        with open(filename, 'w') as f:
            f.writelines(self.lines)
        print(f"Saved to {filename}")

    def convert_library(self, old_lib, new_lib, preview=False):
        """Convert all ZAID library identifiers

        Args:
            old_lib: Old library identifier (e.g., '70c')
            new_lib: New library identifier (e.g., '80c')
            preview: If True, show changes without applying

        Returns: Tuple (number of changes, list of unique ZAIDs changed)
        """
        # Pattern to match ZAID.XXc format
        pattern = re.compile(rf'(\d{{4,6}})\.{re.escape(old_lib)}')

        count = 0
        zaids_changed = set()
        modified_lines = []

        for i, line in enumerate(self.lines):
            matches = pattern.findall(line)
            if matches:
                zaids_changed.update(matches)
                new_line = pattern.sub(rf'\1.{new_lib}', line)
                count += len(matches)

                if preview:
                    print(f"Line {i+1}:")
                    print(f"  Before: {line.rstrip()}")
                    print(f"  After:  {new_line.rstrip()}")

                modified_lines.append(new_line)
            else:
                modified_lines.append(line)

        if not preview:
            self.lines = modified_lines
            print(f"Converted {count} ZAID(s) from .{old_lib} to .{new_lib}")
            print(f"Unique isotopes affected: {len(zaids_changed)}")
        else:
            print(f"\nPreview: {count} conversion(s) would be made")
            print(f"Unique isotopes: {len(zaids_changed)}")
            print("Run without --preview to apply changes")

        return count, sorted(zaids_changed)

    def convert_selective(self, old_lib, new_lib, zaid_list, preview=False):
        """Convert only specific ZAIDs

        Args:
            old_lib: Old library identifier
            new_lib: New library identifier
            zaid_list: List of ZAID numbers to convert (e.g., ['1001', '92235'])
            preview: If True, show changes without applying

        Returns: Number of changes made
        """
        count = 0
        modified_lines = []

        for zaid in zaid_list:
            pattern = re.compile(rf'{zaid}\.{re.escape(old_lib)}')
            for i, line in enumerate(self.lines):
                if pattern.search(line):
                    if preview:
                        new_line = pattern.sub(f'{zaid}.{new_lib}', line)
                        print(f"Line {i+1} ({zaid}):")
                        print(f"  Before: {line.rstrip()}")
                        print(f"  After:  {new_line.rstrip()}")
                    else:
                        self.lines[i] = pattern.sub(f'{zaid}.{new_lib}', line)
                    count += 1

        if preview:
            print(f"\nPREVIEW: {count} specific ZAID conversion(s) would be made")
            print("Run without --preview to apply changes")
        else:
            print(f"Converted {count} specific ZAID(s)")

        return count

    def check_thermal_libraries(self):
        """Check for thermal scattering MT cards that may need updating

        Returns: List of MT cards found
        """
        mt_cards = []
        pattern = re.compile(r'^MT\d+\s+(\S+)')

        for line in self.lines:
            match = pattern.match(line.strip())
            if match:
                mt_cards.append(match.group(1))

        if mt_cards:
            print("\nThermal scattering libraries found:")
            for mt in mt_cards:
                print(f"  {mt}")
            print("\nNote: Verify these are compatible with new cross-section library")
        else:
            print("\nNo thermal scattering (MT) cards found")

        return mt_cards

    def list_all_zaids(self):
        """List all ZAIDs in file

        Returns: Dict {ZAID: library}
        """
        pattern = re.compile(r'(\d{4,6})\.(\d{2,3}[cp])')
        zaids = {}

        for line in self.lines:
            matches = pattern.findall(line)
            for zaid, lib in matches:
                if zaid not in zaids:
                    zaids[zaid] = set()
                zaids[zaid].add(lib)

        return zaids


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Cross-Section Library Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all .70c to .80c
  python library_converter.py input.i --old 70c --new 80c

  # Preview changes without applying
  python library_converter.py input.i --old 70c --new 80c --preview

  # Convert only specific isotopes
  python library_converter.py input.i --old 70c --new 80c --zaids 1001 8016 92235

  # List all ZAIDs in file
  python library_converter.py input.i --list

  # Check thermal scattering libraries
  python library_converter.py input.i --check-mt

Cross-Section Libraries:
  .70c - ENDF/B-VII.0 (continuous energy neutron)
  .80c - ENDF/B-VIII.0 (continuous energy neutron)
  .31c - ENDF/B-VI.8 (continuous energy neutron)
  .24c - ENDF/B-VI (continuous energy neutron)

  Note: Verify library availability in your MCNP xsdir file before converting.
        """)

    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--output', '-o', help='Output filename (default: overwrite)')
    parser.add_argument('--old', help='Old library identifier (e.g., 70c)')
    parser.add_argument('--new', help='New library identifier (e.g., 80c)')
    parser.add_argument('--zaids', nargs='+', help='Specific ZAIDs to convert (optional)')
    parser.add_argument('--preview', action='store_true',
                        help='Preview changes without applying')
    parser.add_argument('--list', action='store_true',
                        help='List all ZAIDs in file')
    parser.add_argument('--check-mt', action='store_true',
                        help='Check thermal scattering (MT) cards')

    args = parser.parse_args()

    try:
        converter = LibraryConverter(args.input_file)

        # List mode
        if args.list:
            zaids = converter.list_all_zaids()
            print("\nZAIDs found in input file:")
            for zaid in sorted(zaids.keys()):
                libs = ', '.join(sorted(zaids[zaid]))
                # Decode ZAID (simplified)
                try:
                    z = int(zaid[:-3])
                    a = int(zaid[-3:])
                    print(f"  {zaid} (Z={z}, A={a}): {libs}")
                except:
                    print(f"  {zaid}: {libs}")
            return 0

        # Check MT cards
        if args.check_mt:
            converter.check_thermal_libraries()
            return 0

        # Convert mode
        if args.old and args.new:
            # Selective conversion
            if args.zaids:
                converter.convert_selective(args.old, args.new, args.zaids, preview=args.preview)
            # Full conversion
            else:
                converter.convert_library(args.old, args.new, args.preview)

            # Check MT cards after conversion
            if not args.preview:
                print()
                converter.check_thermal_libraries()
                converter.save(args.output)

            return 0

        # No operation
        print("No operation specified. Use --help for usage.")
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
