#!/usr/bin/env python3
"""
MCNP Library Finder

Find available cross-section libraries for isotopes and suggest alternatives
when specific libraries are not available.

Usage:
    # Interactive mode
    python library_finder.py

    # Command-line examples
    python library_finder.py --isotope "U-235"
    python library_finder.py --isotope "Pb" --library "80c"
    python library_finder.py --element 92
    python library_finder.py --recommend "92235.70c"
"""

import sys
import os
import argparse
import re
from collections import defaultdict


# Element data
ELEMENTS = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
    'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
    'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22,
    'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29,
    'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36,
    'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42, 'Tc': 43,
    'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50,
    'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57,
    'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64,
    'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71,
    'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78,
    'Au': 79, 'Hg': 80, 'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85,
    'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91, 'U': 92,
    'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99,
    'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103
}

Z_TO_SYMBOL = {v: k for k, v in ELEMENTS.items()}


class LibraryFinder:
    """Find and recommend MCNP cross-section libraries"""

    def __init__(self, xsdir_path=None):
        """
        Initialize library finder

        Args:
            xsdir_path: Path to xsdir file (default: $DATAPATH/xsdir)
        """
        if xsdir_path is None:
            datapath = os.environ.get('DATAPATH')
            if not datapath:
                raise ValueError("DATAPATH not set. Set environment variable or provide xsdir_path.")
            xsdir_path = os.path.join(datapath, 'xsdir')

        if not os.path.exists(xsdir_path):
            raise FileNotFoundError(f"xsdir file not found: {xsdir_path}")

        self.xsdir_path = xsdir_path
        self._zaids = None

    def load_xsdir(self):
        """Load and cache xsdir ZAIDs"""
        if self._zaids is not None:
            return

        self._zaids = set()

        with open(self.xsdir_path, 'r', encoding='utf-8', errors='ignore') as f:
            in_directory = False

            for line in f:
                line = line.strip()

                if not line or line.startswith('c '):
                    continue

                line_lower = line.lower()
                if line_lower == 'directory':
                    in_directory = True
                    continue
                elif line_lower in ['thermal', 'photoatomic', 'photoelectron', 'dosimetry']:
                    in_directory = False

                if in_directory:
                    parts = line.split()
                    if len(parts) >= 1:
                        self._zaids.add(parts[0].lower())

    def parse_isotope(self, isotope_str):
        """
        Parse isotope string (e.g., 'U-235', 'Pb', 'H-1')

        Returns: (symbol, z, mass_number) or None
        """
        isotope_str = isotope_str.strip()

        # Match patterns
        patterns = [
            r'^([A-Z][a-z]?)-?(\d+)$',  # U-235 or U235
            r'^([A-Z][a-z]?)$',          # Pb (natural)
        ]

        for pattern in patterns:
            match = re.match(pattern, isotope_str, re.IGNORECASE)
            if match:
                symbol = match.group(1).capitalize()
                if len(symbol) == 2:
                    symbol = symbol[0] + symbol[1].lower()

                if symbol not in ELEMENTS:
                    return None

                z = ELEMENTS[symbol]
                mass_number = int(match.group(2)) if len(match.groups()) > 1 else None

                return symbol, z, mass_number

        return None

    def parse_zaid(self, zaid_str):
        """
        Parse ZAID string

        Returns: (z, a, library_num, library_type) or None
        """
        pattern = r'^(\d{1,3})(\d{3})\.(\d{2})([a-z])$'
        match = re.match(pattern, zaid_str, re.IGNORECASE)

        if match:
            return (
                int(match.group(1)),
                int(match.group(2)),
                match.group(3),
                match.group(4).lower()
            )

        return None

    def find_isotope_libraries(self, isotope_str):
        """
        Find all available libraries for an isotope

        Args:
            isotope_str: Isotope string (e.g., 'U-235', 'Pb')

        Returns:
            dict with available libraries
        """
        self.load_xsdir()

        parsed = self.parse_isotope(isotope_str)
        if not parsed:
            return None

        symbol, z, mass_number = parsed
        a = mass_number if mass_number is not None else 0

        # Build ZAID prefix
        zaid_prefix = f"{z}{a:03d}."

        # Find all matching ZAIDs
        matches = defaultdict(list)
        for zaid in self._zaids:
            if zaid.startswith(zaid_prefix):
                # Extract library info
                parts = zaid.split('.')
                if len(parts) == 2:
                    lib_suffix = parts[1]
                    lib_num = lib_suffix[:2]
                    lib_type = lib_suffix[2]
                    matches[lib_type].append(lib_suffix)

        return {
            'symbol': symbol,
            'z': z,
            'a': a,
            'isotope': f"{symbol}-{a}" if a > 0 else f"{symbol} (natural)",
            'libraries': dict(matches)
        }

    def find_element_libraries(self, z):
        """
        Find all isotopes and libraries for an element

        Args:
            z: Atomic number

        Returns:
            dict with isotope libraries
        """
        self.load_xsdir()

        if z not in Z_TO_SYMBOL:
            return None

        symbol = Z_TO_SYMBOL[z]

        # Find all isotopes of this element
        isotopes = defaultdict(lambda: defaultdict(list))

        for zaid in self._zaids:
            parsed = self.parse_zaid(zaid)
            if parsed and parsed[0] == z:
                z_val, a_val, lib_num, lib_type = parsed
                isotopes[a_val][lib_type].append(f"{lib_num}{lib_type}")

        return {
            'symbol': symbol,
            'z': z,
            'isotopes': dict(isotopes)
        }

    def check_zaid(self, zaid):
        """
        Check if ZAID is available in xsdir

        Returns: bool
        """
        self.load_xsdir()
        return zaid.lower() in self._zaids

    def recommend_alternative(self, zaid):
        """
        Recommend alternative library if ZAID not available

        Args:
            zaid: ZAID string (e.g., '92235.70c')

        Returns:
            dict with recommendations
        """
        self.load_xsdir()

        parsed = self.parse_zaid(zaid)
        if not parsed:
            return {'error': 'Invalid ZAID format'}

        z, a, lib_num, lib_type = parsed

        recommendations = {
            'requested': zaid,
            'available': self.check_zaid(zaid),
            'alternatives': []
        }

        if recommendations['available']:
            return recommendations

        # Strategy 1: Try different library versions (same type)
        for alt_lib in ['80', '81', '82', '83', '84', '70', '71', '66']:
            alt_zaid = f"{z}{a:03d}.{alt_lib}{lib_type}"
            if self.check_zaid(alt_zaid):
                recommendations['alternatives'].append({
                    'zaid': alt_zaid,
                    'reason': f'Alternative library version (.{alt_lib}{lib_type})',
                    'priority': 1
                })

        # Strategy 2: Try natural element (if specific isotope not found)
        if a > 0:
            natural_zaid = f"{z}000.{lib_num}{lib_type}"
            if self.check_zaid(natural_zaid):
                symbol = Z_TO_SYMBOL.get(z, f"Z={z}")
                recommendations['alternatives'].append({
                    'zaid': natural_zaid,
                    'reason': f'Natural {symbol} mix (includes all isotopes)',
                    'priority': 2
                })

        # Strategy 3: Try other library types
        for alt_type in ['c', 'd']:
            if alt_type != lib_type:
                alt_zaid = f"{z}{a:03d}.{lib_num}{alt_type}"
                if self.check_zaid(alt_zaid):
                    recommendations['alternatives'].append({
                        'zaid': alt_zaid,
                        'reason': f'Different library type (.{alt_type})',
                        'priority': 3
                    })

        # Sort by priority
        recommendations['alternatives'].sort(key=lambda x: x['priority'])

        return recommendations


def interactive_mode(finder):
    """Interactive library finding mode"""
    print("=" * 70)
    print("MCNP Library Finder - Interactive Mode")
    print("=" * 70)
    print(f"xsdir: {finder.xsdir_path}")
    print("\nCommands:")
    print("  isotope <name>     - Find libraries for isotope (e.g., 'isotope U-235')")
    print("  element <Z>        - Find all isotopes of element (e.g., 'element 92')")
    print("  check <ZAID>       - Check if ZAID available")
    print("  recommend <ZAID>   - Get alternative recommendations")
    print("  help               - Show this help")
    print("  quit, exit         - Exit program")
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
                print("  isotope U-235       → Find all U-235 libraries")
                print("  element 92          → Find all uranium isotopes")
                print("  check 92235.80c     → Check if available")
                print("  recommend 92235.70c → Get alternatives if missing")
                continue

            parts = cmd.split(None, 1)
            if len(parts) < 2:
                print("ERROR: Command requires an argument")
                continue

            command, arg = parts[0].lower(), parts[1]

            if command == 'isotope':
                result = finder.find_isotope_libraries(arg)

                if result:
                    print(f"\nIsotope: {result['isotope']} (Z={result['z']})")
                    print(f"Available libraries:")

                    if result['libraries']:
                        for lib_type, libs in sorted(result['libraries'].items()):
                            type_name = {
                                'c': 'Continuous energy',
                                't': 'Thermal scattering',
                                'p': 'Photoatomic',
                                'e': 'Photoelectron',
                                'd': 'Discrete energy'
                            }.get(lib_type, f'Type {lib_type}')

                            print(f"\n  {type_name} (.??{lib_type}):")
                            for lib in sorted(libs):
                                zaid = f"{result['z']}{result['a']:03d}.{lib}"
                                print(f"    {zaid}")
                    else:
                        print("  No libraries found")
                else:
                    print(f"ERROR: Could not parse isotope '{arg}'")

            elif command == 'element':
                try:
                    z = int(arg)
                except ValueError:
                    print(f"ERROR: Invalid atomic number '{arg}'")
                    continue

                result = finder.find_element_libraries(z)

                if result:
                    print(f"\nElement: {result['symbol']} (Z={result['z']})")
                    print(f"Isotopes found: {len(result['isotopes'])}")

                    for a in sorted(result['isotopes'].keys()):
                        iso_name = f"{result['symbol']}-{a}" if a > 0 else f"{result['symbol']} (natural)"
                        print(f"\n  {iso_name}:")

                        for lib_type, libs in sorted(result['isotopes'][a].items()):
                            libs_str = ', '.join(sorted(libs))
                            print(f"    .??{lib_type}: {libs_str}")
                else:
                    print(f"ERROR: Unknown element Z={arg}")

            elif command == 'check':
                available = finder.check_zaid(arg)

                print(f"\nZAID: {arg}")
                if available:
                    print("Status: AVAILABLE ✓")
                else:
                    print("Status: NOT FOUND ✗")
                    print("\nUse 'recommend' command to find alternatives")

            elif command == 'recommend':
                result = finder.recommend_alternative(arg)

                if 'error' in result:
                    print(f"ERROR: {result['error']}")
                    continue

                print(f"\nRequested: {result['requested']}")
                if result['available']:
                    print("Status: AVAILABLE ✓")
                else:
                    print("Status: NOT FOUND ✗")

                    if result['alternatives']:
                        print("\nRecommended alternatives:")
                        for i, alt in enumerate(result['alternatives'], 1):
                            print(f"  {i}. {alt['zaid']}")
                            print(f"     Reason: {alt['reason']}")
                    else:
                        print("\nNo alternatives found")
                        print("Consider:")
                        print("  - Using natural element mix (ZZZAAA → ZZZ000)")
                        print("  - Different library version (.70c, .66c)")
                        print("  - Omitting isotope if minor contributor")

            else:
                print(f"ERROR: Unknown command '{command}'")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Library Finder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find libraries for U-235
  python library_finder.py --isotope "U-235"

  # Find all uranium isotopes
  python library_finder.py --element 92

  # Check if ZAID available
  python library_finder.py --check "92235.80c"

  # Get recommendations for missing library
  python library_finder.py --recommend "92235.70c"

  # Interactive mode (default)
  python library_finder.py

Environment:
  DATAPATH: Path to MCNP data directory containing xsdir file
        """
    )

    parser.add_argument('--xsdir', help='Path to xsdir file')
    parser.add_argument('--isotope', help='Find libraries for isotope (e.g., U-235)')
    parser.add_argument('--element', type=int, help='Find all isotopes of element (Z)')
    parser.add_argument('--check', help='Check if ZAID available')
    parser.add_argument('--recommend', help='Get alternatives for ZAID')

    args = parser.parse_args()

    try:
        finder = LibraryFinder(xsdir_path=args.xsdir)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        print("\nPlease set DATAPATH environment variable or use --xsdir option")
        sys.exit(1)

    # Command-line mode
    if args.isotope:
        result = finder.find_isotope_libraries(args.isotope)
        if result:
            print(f"Isotope: {result['isotope']} (Z={result['z']})")
            if result['libraries']:
                print("Available libraries:")
                for lib_type, libs in sorted(result['libraries'].items()):
                    print(f"  .??{lib_type}: {', '.join(sorted(libs))}")
            else:
                print("No libraries found")
            sys.exit(0)
        else:
            print(f"ERROR: Could not parse isotope '{args.isotope}'")
            sys.exit(1)

    elif args.element is not None:
        result = finder.find_element_libraries(args.element)
        if result:
            print(f"Element: {result['symbol']} (Z={result['z']})")
            print(f"Isotopes: {len(result['isotopes'])}")
            for a in sorted(result['isotopes'].keys()):
                iso = f"{result['symbol']}-{a}" if a > 0 else "natural"
                libs = ', '.join(result['isotopes'][a].keys())
                print(f"  {iso}: {libs}")
            sys.exit(0)
        else:
            print(f"ERROR: Unknown element Z={args.element}")
            sys.exit(1)

    elif args.check:
        available = finder.check_zaid(args.check)
        print(f"ZAID: {args.check}")
        if available:
            print("Status: AVAILABLE ✓")
            sys.exit(0)
        else:
            print("Status: NOT FOUND ✗")
            sys.exit(1)

    elif args.recommend:
        result = finder.recommend_alternative(args.recommend)
        if 'error' in result:
            print(f"ERROR: {result['error']}")
            sys.exit(1)

        print(f"Requested: {result['requested']}")
        if result['available']:
            print("Status: AVAILABLE ✓")
            sys.exit(0)
        else:
            print("Status: NOT FOUND ✗")
            if result['alternatives']:
                print("\nAlternatives:")
                for alt in result['alternatives']:
                    print(f"  {alt['zaid']} - {alt['reason']}")
            sys.exit(1)

    else:
        # Interactive mode (default)
        interactive_mode(finder)


if __name__ == '__main__':
    main()
