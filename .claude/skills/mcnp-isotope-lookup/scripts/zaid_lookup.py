#!/usr/bin/env python3
"""
MCNP ZAID Lookup Tool

Interactive and command-line tool for converting element names and isotopes
to MCNP ZAID format and vice versa.

Usage:
    # Interactive mode
    python zaid_lookup.py

    # Command-line examples
    python zaid_lookup.py --isotope "U-235" --library "80c"
    python zaid_lookup.py --element "Pb"
    python zaid_lookup.py --zaid "92235.80c"
"""

import sys
import argparse
import re


class ElementData:
    """Periodic table data"""

    # Element symbol to atomic number mapping
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
        'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105,
        'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111,
        'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117,
        'Og': 118
    }

    # Reverse mapping
    Z_TO_SYMBOL = {v: k for k, v in ELEMENTS.items()}

    # Element full names
    ELEMENT_NAMES = {
        'H': 'Hydrogen', 'He': 'Helium', 'Li': 'Lithium', 'Be': 'Beryllium',
        'B': 'Boron', 'C': 'Carbon', 'N': 'Nitrogen', 'O': 'Oxygen',
        'F': 'Fluorine', 'Ne': 'Neon', 'Na': 'Sodium', 'Mg': 'Magnesium',
        'Al': 'Aluminum', 'Si': 'Silicon', 'P': 'Phosphorus', 'S': 'Sulfur',
        'Cl': 'Chlorine', 'Ar': 'Argon', 'K': 'Potassium', 'Ca': 'Calcium',
        'Fe': 'Iron', 'Ni': 'Nickel', 'Cu': 'Copper', 'Zn': 'Zinc', 'Zr': 'Zirconium',
        'Ag': 'Silver', 'Cd': 'Cadmium', 'W': 'Tungsten', 'Pb': 'Lead',
        'Bi': 'Bismuth', 'U': 'Uranium', 'Pu': 'Plutonium', 'Am': 'Americium',
        'Cm': 'Curium', 'Cf': 'Californium'
    }


class ZAIDLookup:
    """MCNP ZAID lookup and conversion tool"""

    def __init__(self):
        self.elements = ElementData()

    def parse_isotope(self, isotope_str):
        """
        Parse isotope string (e.g., 'U-235', 'H-1', 'Pb')

        Returns: (symbol, mass_number) or None
        """
        isotope_str = isotope_str.strip()

        # Match patterns like "U-235", "H2", "Pb", etc.
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

                mass_number = match.group(2) if len(match.groups()) > 1 else None
                if mass_number:
                    mass_number = int(mass_number)

                # Validate element
                if symbol not in self.elements.ELEMENTS:
                    return None

                return symbol, mass_number

        return None

    def isotope_to_zaid(self, isotope_str, library='80c'):
        """
        Convert isotope string to ZAID

        Args:
            isotope_str: Isotope string (e.g., 'U-235', 'Pb')
            library: Library suffix (default '80c')

        Returns: ZAID string or None
        """
        result = self.parse_isotope(isotope_str)
        if not result:
            return None

        symbol, mass_number = result
        z = self.elements.ELEMENTS[symbol]

        if mass_number is None:
            # Natural element
            zaid_num = f"{z}000"
        else:
            # Specific isotope
            zaid_num = f"{z}{mass_number:03d}"

        return f"{zaid_num}.{library}"

    def zaid_to_isotope(self, zaid_str):
        """
        Parse ZAID string and return isotope information

        Args:
            zaid_str: ZAID string (e.g., '92235.80c')

        Returns: dict with Z, A, library, symbol, name
        """
        # Pattern: ZZZAAA.nnX
        pattern = r'^(\d{1,3})(\d{3})\.(\d{2})([a-z])$'
        match = re.match(pattern, zaid_str)

        if not match:
            return None

        z = int(match.group(1))
        a = int(match.group(2))
        lib_num = match.group(3)
        lib_type = match.group(4)

        if z not in self.elements.Z_TO_SYMBOL:
            return None

        symbol = self.elements.Z_TO_SYMBOL[z]
        name = self.elements.ELEMENT_NAMES.get(symbol, symbol)

        if a == 0:
            isotope_name = f"{symbol} (natural)"
        else:
            isotope_name = f"{symbol}-{a}"

        return {
            'Z': z,
            'A': a,
            'library_num': lib_num,
            'library_type': lib_type,
            'library': f"{lib_num}{lib_type}",
            'symbol': symbol,
            'element_name': name,
            'isotope_name': isotope_name,
            'zaid': zaid_str
        }

    def validate_zaid(self, zaid_str):
        """
        Validate ZAID format

        Returns: (valid: bool, message: str)
        """
        pattern = r'^(\d{1,3})(\d{3})\.(\d{2})([a-z])$'
        match = re.match(pattern, zaid_str)

        if not match:
            return False, "Invalid ZAID format (expected ZZZAAA.nnX)"

        z = int(match.group(1))
        a = int(match.group(2))
        lib_type = match.group(4)

        if z < 1 or z > 118:
            return False, f"Invalid atomic number Z={z} (must be 1-118)"

        if a < 0 or a > 300:
            return False, f"Invalid mass number A={a}"

        valid_types = ['c', 'd', 'p', 'e', 't', 'h', 'm', 'y', 'u', 'v']
        if lib_type not in valid_types:
            return False, f"Unknown library type '{lib_type}'"

        return True, "Valid ZAID"


def interactive_mode():
    """Interactive ZAID lookup mode"""
    lookup = ZAIDLookup()

    print("=" * 60)
    print("MCNP ZAID Lookup Tool - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  isotope <name>    - Convert isotope to ZAID (e.g., 'isotope U-235')")
    print("  zaid <ZAID>       - Parse ZAID (e.g., 'zaid 92235.80c')")
    print("  element <symbol>  - Get natural element ZAID (e.g., 'element Pb')")
    print("  validate <ZAID>   - Validate ZAID format")
    print("  help              - Show this help")
    print("  quit, exit        - Exit program")
    print()

    while True:
        try:
            cmd = input("lookup> ").strip()

            if not cmd:
                continue

            if cmd.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if cmd.lower() == 'help':
                print("\nAvailable commands:")
                print("  isotope U-235       → Get ZAID for U-235")
                print("  zaid 92235.80c      → Parse ZAID")
                print("  element Pb          → Get natural element ZAID")
                print("  validate 92235.80c  → Validate format")
                continue

            parts = cmd.split(None, 1)
            if len(parts) < 2:
                print("ERROR: Command requires an argument")
                continue

            command, arg = parts[0].lower(), parts[1]

            if command == 'isotope':
                zaid = lookup.isotope_to_zaid(arg)
                if zaid:
                    info = lookup.zaid_to_isotope(zaid)
                    print(f"\nIsotope: {arg}")
                    print(f"ZAID: {zaid}")
                    print(f"Element: {info['element_name']} (Z={info['Z']})")
                    print(f"Library: {info['library']}")
                else:
                    print(f"ERROR: Could not parse isotope '{arg}'")

            elif command == 'zaid':
                info = lookup.zaid_to_isotope(arg)
                if info:
                    print(f"\nZAID: {info['zaid']}")
                    print(f"Isotope: {info['isotope_name']}")
                    print(f"Element: {info['element_name']} (Z={info['Z']})")
                    print(f"Mass number: A={info['A']}")
                    print(f"Library: {info['library']}")
                else:
                    print(f"ERROR: Invalid ZAID '{arg}'")

            elif command == 'element':
                zaid = lookup.isotope_to_zaid(arg)
                if zaid:
                    info = lookup.zaid_to_isotope(zaid)
                    print(f"\nElement: {info['element_name']}")
                    print(f"Natural ZAID: {zaid}")
                    print(f"Z = {info['Z']}")
                else:
                    print(f"ERROR: Unknown element '{arg}'")

            elif command == 'validate':
                valid, msg = lookup.validate_zaid(arg)
                print(f"\nZAID: {arg}")
                print(f"Status: {msg}")
                if valid:
                    info = lookup.zaid_to_isotope(arg)
                    print(f"Isotope: {info['isotope_name']}")

            else:
                print(f"ERROR: Unknown command '{command}'")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='MCNP ZAID Lookup Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert isotope to ZAID
  python zaid_lookup.py --isotope "U-235" --library "80c"
  python zaid_lookup.py --isotope "Pb"

  # Parse ZAID
  python zaid_lookup.py --zaid "92235.80c"

  # Validate ZAID
  python zaid_lookup.py --validate "92235.80c"

  # Interactive mode (default)
  python zaid_lookup.py
        """
    )

    parser.add_argument('--isotope', help='Isotope to convert (e.g., U-235, Pb)')
    parser.add_argument('--library', default='80c', help='Library suffix (default: 80c)')
    parser.add_argument('--zaid', help='ZAID to parse (e.g., 92235.80c)')
    parser.add_argument('--validate', help='ZAID to validate')
    parser.add_argument('--element', help='Element symbol (get natural ZAID)')

    args = parser.parse_args()
    lookup = ZAIDLookup()

    # Command-line mode
    if args.isotope:
        zaid = lookup.isotope_to_zaid(args.isotope, args.library)
        if zaid:
            info = lookup.zaid_to_isotope(zaid)
            print(f"Isotope: {args.isotope}")
            print(f"ZAID: {zaid}")
            print(f"Element: {info['element_name']} (Z={info['Z']})")
            if info['A'] == 0:
                print("Type: Natural element mix")
            else:
                print(f"Mass number: A={info['A']}")
        else:
            print(f"ERROR: Could not parse isotope '{args.isotope}'")
            sys.exit(1)

    elif args.zaid:
        info = lookup.zaid_to_isotope(args.zaid)
        if info:
            print(f"ZAID: {info['zaid']}")
            print(f"Isotope: {info['isotope_name']}")
            print(f"Element: {info['element_name']}")
            print(f"Atomic number: Z = {info['Z']}")
            print(f"Mass number: A = {info['A']}")
            print(f"Library: {info['library']}")
        else:
            print(f"ERROR: Invalid ZAID '{args.zaid}'")
            sys.exit(1)

    elif args.validate:
        valid, msg = lookup.validate_zaid(args.validate)
        print(f"ZAID: {args.validate}")
        print(f"Status: {msg}")
        if valid:
            info = lookup.zaid_to_isotope(args.validate)
            print(f"Isotope: {info['isotope_name']}")
        sys.exit(0 if valid else 1)

    elif args.element:
        zaid = lookup.isotope_to_zaid(args.element, args.library)
        if zaid:
            info = lookup.zaid_to_isotope(zaid)
            print(f"Element: {info['element_name']}")
            print(f"Natural ZAID: {zaid}")
            print(f"Atomic number: Z = {info['Z']}")
        else:
            print(f"ERROR: Unknown element '{args.element}'")
            sys.exit(1)

    else:
        # Interactive mode (default)
        interactive_mode()


if __name__ == '__main__':
    main()
