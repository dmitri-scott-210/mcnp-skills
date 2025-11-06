#!/usr/bin/env python3
"""
MCNP Library Checker

Check availability of isotopes in MCNP cross-section libraries (xsdir file).

Usage:
    # Check single ZAID
    python library_checker.py --zaid "92235.80c"

    # Check multiple ZAIDs
    python library_checker.py --file input.i

    # Search for available isotopes
    python library_checker.py --search "U-"
"""

import sys
import os
import argparse
import re


class XsdirChecker:
    """MCNP xsdir file checker"""

    def __init__(self, datapath=None):
        """
        Initialize checker

        Args:
            datapath: Path to MCNP data directory (default: $DATAPATH env var)
        """
        if datapath is None:
            datapath = os.environ.get('DATAPATH')

        if not datapath:
            raise ValueError("DATAPATH not set. Set environment variable or provide path.")

        self.datapath = datapath
        self.xsdir_path = os.path.join(datapath, 'xsdir')

        if not os.path.exists(self.xsdir_path):
            raise FileNotFoundError(f"xsdir file not found: {self.xsdir_path}")

        # Cache of available ZAIDs
        self._zaids = None

    def load_xsdir(self):
        """Load xsdir file and cache ZAIDs"""
        if self._zaids is not None:
            return

        self._zaids = {}

        with open(self.xsdir_path, 'r', encoding='utf-8', errors='ignore') as f:
            in_directory = False

            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('c '):
                    continue

                # Check for section markers
                if line.lower() == 'directory':
                    in_directory = True
                    continue
                elif line.lower() in ['thermal', 'photoatomic', 'photoelectron', 'dosimetry']:
                    in_directory = False

                if in_directory:
                    # Parse ZAID entry
                    parts = line.split()
                    if len(parts) >= 3:
                        zaid = parts[0]
                        try:
                            aw = float(parts[1])
                            filename = parts[2]
                            self._zaids[zaid] = {'aw': aw, 'filename': filename}
                        except ValueError:
                            continue

    def check_zaid(self, zaid):
        """
        Check if ZAID available in xsdir

        Args:
            zaid: ZAID string (e.g., '92235.80c')

        Returns:
            dict with availability info or None
        """
        self.load_xsdir()

        if zaid in self._zaids:
            return {
                'zaid': zaid,
                'available': True,
                'atomic_weight': self._zaids[zaid]['aw'],
                'filename': self._zaids[zaid]['filename']
            }
        else:
            return {
                'zaid': zaid,
                'available': False
            }

    def search_zaids(self, pattern):
        """
        Search for ZAIDs matching pattern

        Args:
            pattern: Regex pattern or substring

        Returns:
            list of matching ZAIDs
        """
        self.load_xsdir()

        matches = []
        for zaid in self._zaids:
            if re.search(pattern, zaid, re.IGNORECASE):
                matches.append(zaid)

        return sorted(matches)

    def get_all_zaids(self):
        """Get list of all available ZAIDs"""
        self.load_xsdir()
        return sorted(self._zaids.keys())

    def check_input_file(self, input_file):
        """
        Check all ZAIDs in MCNP input file

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict with results
        """
        # Extract ZAIDs from input file
        zaids_found = set()
        zaid_pattern = r'\b(\d{1,3}\d{3}\.\d{2}[a-z])\b'

        with open(input_file, 'r') as f:
            for line in f:
                # Skip comment lines
                if line.strip().startswith('c ') or line.strip().startswith('C '):
                    continue

                # Find ZAIDs in line
                matches = re.findall(zaid_pattern, line, re.IGNORECASE)
                zaids_found.update(matches)

        # Check each ZAID
        results = {
            'total': len(zaids_found),
            'available': [],
            'missing': [],
        }

        for zaid in sorted(zaids_found):
            info = self.check_zaid(zaid)
            if info['available']:
                results['available'].append(zaid)
            else:
                results['missing'].append(zaid)

        return results


def interactive_mode(checker):
    """Interactive library checking mode"""
    print("=" * 60)
    print("MCNP Library Checker - Interactive Mode")
    print("=" * 60)
    print(f"xsdir: {checker.xsdir_path}")
    print("\nCommands:")
    print("  check <ZAID>     - Check if ZAID available")
    print("  search <pattern> - Search for ZAIDs")
    print("  list <element>   - List isotopes of element (e.g., 'list U')")
    print("  stats            - Show library statistics")
    print("  help             - Show this help")
    print("  quit, exit       - Exit program")
    print()

    while True:
        try:
            cmd = input("library> ").strip()

            if not cmd:
                continue

            if cmd.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if cmd.lower() == 'help':
                print("\nAvailable commands:")
                print("  check 92235.80c    → Check if U-235 available")
                print("  search 92          → Search for all uranium isotopes")
                print("  list U             → List U isotopes")
                print("  stats              → Show statistics")
                continue

            parts = cmd.split(None, 1)
            command = parts[0].lower()

            if command == 'check':
                if len(parts) < 2:
                    print("ERROR: check requires a ZAID")
                    continue

                zaid = parts[1]
                info = checker.check_zaid(zaid)

                print(f"\nZAID: {info['zaid']}")
                if info['available']:
                    print("Status: AVAILABLE ✓")
                    print(f"Atomic weight: {info['atomic_weight']:.5f} amu")
                    print(f"File: {info['filename']}")
                else:
                    print("Status: NOT FOUND ✗")

            elif command == 'search':
                if len(parts) < 2:
                    print("ERROR: search requires a pattern")
                    continue

                pattern = parts[1]
                matches = checker.search_zaids(pattern)

                if matches:
                    print(f"\nFound {len(matches)} matches for '{pattern}':")
                    for i, zaid in enumerate(matches[:50], 1):  # Limit to 50
                        print(f"  {i:3d}. {zaid}")
                    if len(matches) > 50:
                        print(f"  ... ({len(matches) - 50} more)")
                else:
                    print(f"No matches found for '{pattern}'")

            elif command == 'list':
                if len(parts) < 2:
                    print("ERROR: list requires an element symbol")
                    continue

                element = parts[1].upper()
                # Map element symbol to Z
                element_map = {
                    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                    'Fe': 26, 'Ni': 28, 'Cu': 29, 'Zr': 40, 'Pb': 82, 'U': 92, 'Pu': 94
                }

                if element in element_map:
                    z = element_map[element]
                    pattern = f"^{z}\\d{{3}}\\.\\d{{2}}[a-z]$"
                    matches = checker.search_zaids(pattern)

                    if matches:
                        print(f"\nIsotopes of {element} (Z={z}):")
                        for zaid in matches:
                            print(f"  {zaid}")
                    else:
                        print(f"No isotopes found for {element}")
                else:
                    print(f"ERROR: Unknown element '{element}'")

            elif command == 'stats':
                checker.load_xsdir()
                all_zaids = checker.get_all_zaids()
                total = len(all_zaids)

                # Count by library type
                types = {}
                for zaid in all_zaids:
                    lib_type = zaid[-1]
                    types[lib_type] = types.get(lib_type, 0) + 1

                print(f"\nLibrary Statistics:")
                print(f"Total ZAIDs: {total}")
                print("\nBy library type:")
                for lib_type in sorted(types.keys()):
                    print(f"  .??{lib_type}: {types[lib_type]:4d}")

            else:
                print(f"ERROR: Unknown command '{command}'")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Library Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check single ZAID
  python library_checker.py --zaid "92235.80c"

  # Check all ZAIDs in input file
  python library_checker.py --file input.i

  # Search for uranium isotopes
  python library_checker.py --search "^92"

  # Interactive mode (default)
  python library_checker.py

Environment:
  DATAPATH: Path to MCNP data directory containing xsdir file
        """
    )

    parser.add_argument('--datapath', help='Path to MCNP data directory')
    parser.add_argument('--zaid', help='ZAID to check')
    parser.add_argument('--file', help='MCNP input file to check')
    parser.add_argument('--search', help='Search pattern for ZAIDs')
    parser.add_argument('--list-all', action='store_true', help='List all available ZAIDs')

    args = parser.parse_args()

    try:
        checker = XsdirChecker(datapath=args.datapath)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        print("\nPlease set DATAPATH environment variable or use --datapath option")
        sys.exit(1)

    # Command-line mode
    if args.zaid:
        info = checker.check_zaid(args.zaid)
        print(f"ZAID: {info['zaid']}")
        if info['available']:
            print("Status: AVAILABLE ✓")
            print(f"Atomic weight: {info['atomic_weight']:.5f} amu")
            print(f"File: {info['filename']}")
            sys.exit(0)
        else:
            print("Status: NOT FOUND ✗")
            sys.exit(1)

    elif args.file:
        if not os.path.exists(args.file):
            print(f"ERROR: Input file not found: {args.file}")
            sys.exit(1)

        results = checker.check_input_file(args.file)

        print(f"Input file: {args.file}")
        print(f"Total ZAIDs found: {results['total']}")
        print(f"Available: {len(results['available'])}")
        print(f"Missing: {len(results['missing'])}")

        if results['missing']:
            print("\nMissing ZAIDs:")
            for zaid in results['missing']:
                print(f"  ✗ {zaid}")
            sys.exit(1)
        else:
            print("\nAll ZAIDs are available ✓")
            sys.exit(0)

    elif args.search:
        matches = checker.search_zaids(args.search)
        if matches:
            print(f"Found {len(matches)} matches:")
            for zaid in matches:
                print(f"  {zaid}")
        else:
            print(f"No matches found for '{args.search}'")
        sys.exit(0)

    elif args.list_all:
        all_zaids = checker.get_all_zaids()
        print(f"Total ZAIDs: {len(all_zaids)}")
        for zaid in all_zaids:
            print(zaid)
        sys.exit(0)

    else:
        # Interactive mode (default)
        interactive_mode(checker)


if __name__ == '__main__':
    main()
