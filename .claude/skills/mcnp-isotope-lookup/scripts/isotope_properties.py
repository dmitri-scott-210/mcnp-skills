#!/usr/bin/env python3
"""
MCNP Isotope Properties Tool

Lookup atomic masses, natural abundances, and decay data for isotopes.

Usage:
    # Interactive mode
    python isotope_properties.py

    # Command-line examples
    python isotope_properties.py --isotope "U-235"
    python isotope_properties.py --element "Cl" --abundance
    python isotope_properties.py --mass "Fe-56"
"""

import sys
import argparse


class IsotopeDatabase:
    """Database of isotope properties"""

    # Atomic masses (amu) - selected common isotopes
    ATOMIC_MASSES = {
        # Light elements
        (1, 1): 1.00782503, (1, 2): 2.01410178, (1, 3): 3.01604928,
        (2, 3): 3.01602932, (2, 4): 4.00260325,
        (3, 6): 6.01512289, (3, 7): 7.01600344,
        (4, 9): 9.01218307,
        (5, 10): 10.01293697, (5, 11): 11.00930546,
        (6, 12): 12.00000000, (6, 13): 13.00335484,
        (7, 14): 14.00307400, (7, 15): 15.00010890,
        (8, 16): 15.99491462, (8, 17): 16.99913176, (8, 18): 17.99915961,
        (9, 19): 18.99840316,
        (11, 23): 22.98976928,
        (13, 27): 26.98153853,
        (14, 28): 27.97692654, (14, 29): 28.97649466, (14, 30): 29.97377013,
        (15, 31): 30.97376200,
        (17, 35): 34.96885272, (17, 37): 36.96590262,

        # Structural materials
        (26, 54): 53.93960900, (26, 56): 55.93493750, (26, 57): 56.93539400, (26, 58): 57.93327560,
        (28, 58): 57.93534290, (28, 60): 59.93078640, (28, 61): 60.93105600, (28, 62): 61.92834510, (28, 64): 63.92796600,
        (29, 63): 62.92959750, (29, 65): 64.92778950,
        (40, 90): 89.90470440, (40, 91): 90.90564580, (40, 92): 91.90504080, (40, 94): 93.90631520, (40, 96): 95.90827340,

        # Heavy metals
        (82, 204): 203.97304400, (82, 206): 205.97446530, (82, 207): 206.97589690, (82, 208): 207.97665210,
        (83, 209): 208.98039870,
        (74, 180): 179.94671080, (74, 182): 181.94820420, (74, 183): 182.95022300, (74, 184): 183.95093120, (74, 186): 185.95436410,

        # Actinides
        (92, 233): 233.03963520, (92, 234): 234.04095210, (92, 235): 235.04393010, (92, 238): 238.05078820,
        (93, 237): 237.04817340,
        (94, 238): 238.04955990, (94, 239): 239.05216340, (94, 240): 240.05381350, (94, 241): 241.05685150, (94, 242): 242.05874260,
        (95, 241): 241.05682910, (95, 243): 243.06138110,
        (96, 244): 244.06275230,
        (98, 252): 252.08162700,
    }

    # Natural abundances (fraction) - selected elements
    NATURAL_ABUNDANCES = {
        1: {1: 0.999885, 2: 0.000115},  # Hydrogen
        5: {10: 0.199, 11: 0.801},      # Boron
        6: {12: 0.9893, 13: 0.0107},    # Carbon
        7: {14: 0.99636, 15: 0.00364},  # Nitrogen
        8: {16: 0.99757, 17: 0.00038, 18: 0.00205},  # Oxygen
        17: {35: 0.7576, 37: 0.2424},   # Chlorine
        26: {54: 0.05845, 56: 0.91754, 57: 0.02119, 58: 0.00282},  # Iron
        28: {58: 0.68077, 60: 0.26223, 61: 0.01140, 62: 0.03634, 64: 0.00926},  # Nickel
        29: {63: 0.6915, 65: 0.3085},   # Copper
        40: {90: 0.5145, 91: 0.1122, 92: 0.1715, 94: 0.1738, 96: 0.0280},  # Zirconium
        82: {204: 0.014, 206: 0.241, 207: 0.221, 208: 0.524},  # Lead
        92: {234: 0.000054, 235: 0.007204, 238: 0.992742},  # Uranium (natural)
    }

    # Average atomic masses (amu) for natural elements
    AVERAGE_MASSES = {
        1: 1.008, 2: 4.003, 3: 6.94, 4: 9.012, 5: 10.81, 6: 12.011, 7: 14.007, 8: 15.999,
        9: 18.998, 10: 20.180, 11: 22.990, 12: 24.305, 13: 26.982, 14: 28.085, 15: 30.974,
        16: 32.06, 17: 35.45, 18: 39.948, 19: 39.098, 20: 40.078, 26: 55.845, 28: 58.693,
        29: 63.546, 40: 91.224, 42: 95.95, 47: 107.868, 48: 112.414, 74: 183.84, 82: 207.2,
        83: 208.980, 92: 238.029,
    }

    # Half-lives (seconds) - selected radioactive isotopes
    HALF_LIVES = {
        (1, 3): 3.888e8,        # H-3 (12.3 yr)
        (27, 60): 1.663e8,      # Co-60 (5.27 yr)
        (38, 90): 9.08e8,       # Sr-90 (28.8 yr)
        (43, 99): 6.65e12,      # Tc-99 (211,000 yr)
        (55, 137): 9.51e8,      # Cs-137 (30.2 yr)
        (92, 235): 2.22e16,     # U-235 (7.04e8 yr)
        (92, 238): 1.41e17,     # U-238 (4.47e9 yr)
        (94, 239): 7.60e11,     # Pu-239 (24,110 yr)
        (95, 241): 1.36e10,     # Am-241 (432 yr)
    }

    # Element symbols
    SYMBOLS = {
        1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
        11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca',
        21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn',
        40: 'Zr', 42: 'Mo', 47: 'Ag', 48: 'Cd', 74: 'W', 82: 'Pb', 83: 'Bi', 92: 'U', 93: 'Np', 94: 'Pu',
        95: 'Am', 96: 'Cm', 98: 'Cf',
    }

    SYMBOL_TO_Z = {v: k for k, v in SYMBOLS.items()}


class IsotopeLookup:
    """Isotope property lookup tool"""

    def __init__(self):
        self.db = IsotopeDatabase()

    def get_atomic_mass(self, z, a=None):
        """Get atomic mass (amu)"""
        if a is None:
            # Return average mass for element
            return self.db.AVERAGE_MASSES.get(z)
        else:
            # Return specific isotope mass
            return self.db.ATOMIC_MASSES.get((z, a))

    def get_natural_abundance(self, z):
        """Get natural isotopic composition"""
        return self.db.NATURAL_ABUNDANCES.get(z)

    def get_half_life(self, z, a):
        """Get half-life (seconds)"""
        return self.db.HALF_LIVES.get((z, a))

    def calculate_average_mass(self, z):
        """Calculate average atomic mass from abundances"""
        abundances = self.get_natural_abundance(z)
        if not abundances:
            return None

        avg_mass = 0.0
        for a, frac in abundances.items():
            mass = self.get_atomic_mass(z, a)
            if mass:
                avg_mass += frac * mass

        return avg_mass


def interactive_mode():
    """Interactive isotope lookup mode"""
    lookup = IsotopeLookup()

    print("=" * 60)
    print("MCNP Isotope Properties Tool - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  mass <isotope>       - Get atomic mass (e.g., 'mass U-235')")
    print("  abundance <element>  - Get natural abundances (e.g., 'abundance Cl')")
    print("  halflife <isotope>   - Get half-life (e.g., 'halflife Co-60')")
    print("  average <element>    - Calculate average mass (e.g., 'average Fe')")
    print("  help                 - Show this help")
    print("  quit, exit           - Exit program")
    print()

    while True:
        try:
            cmd = input("isotope> ").strip()

            if not cmd:
                continue

            if cmd.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if cmd.lower() == 'help':
                print("\nAvailable commands:")
                print("  mass U-235          → Get atomic mass")
                print("  abundance Cl        → Get natural isotopic composition")
                print("  halflife Co-60      → Get radioactive half-life")
                print("  average Fe          → Calculate average atomic mass")
                continue

            parts = cmd.split(None, 1)
            if len(parts) < 2:
                print("ERROR: Command requires an argument")
                continue

            command, arg = parts[0].lower(), parts[1]

            # Parse isotope or element
            import re
            match = re.match(r'^([A-Z][a-z]?)-?(\d+)?$', arg, re.IGNORECASE)
            if not match:
                print(f"ERROR: Could not parse '{arg}'")
                continue

            symbol = match.group(1).capitalize()
            if len(symbol) == 2:
                symbol = symbol[0] + symbol[1].lower()

            if symbol not in lookup.db.SYMBOL_TO_Z:
                print(f"ERROR: Unknown element '{symbol}'")
                continue

            z = lookup.db.SYMBOL_TO_Z[symbol]
            a = int(match.group(2)) if match.group(2) else None

            if command == 'mass':
                if a is None:
                    mass = lookup.get_atomic_mass(z)
                    print(f"\nElement: {symbol} (Z={z})")
                    print(f"Average atomic mass: {mass:.3f} amu")
                else:
                    mass = lookup.get_atomic_mass(z, a)
                    if mass:
                        print(f"\nIsotope: {symbol}-{a} (Z={z}, A={a})")
                        print(f"Atomic mass: {mass:.8f} amu")
                    else:
                        print(f"ERROR: Mass data not available for {symbol}-{a}")

            elif command == 'abundance':
                abundances = lookup.get_natural_abundance(z)
                if abundances:
                    print(f"\nElement: {symbol} (Z={z})")
                    print("Natural isotopic composition:")
                    total = 0.0
                    for a_val, frac in sorted(abundances.items()):
                        print(f"  {symbol}-{a_val}: {frac*100:.4f}% ({frac:.6f})")
                        total += frac
                    print(f"Total: {total:.6f}")
                else:
                    print(f"No natural abundance data for {symbol}")

            elif command == 'halflife':
                if a is None:
                    print("ERROR: Half-life requires specific isotope (e.g., Co-60)")
                    continue

                t_half = lookup.get_half_life(z, a)
                if t_half:
                    print(f"\nIsotope: {symbol}-{a}")
                    print(f"Half-life: {t_half:.3e} seconds")
                    # Convert to human-readable units
                    if t_half > 3.156e7:
                        print(f"          {t_half/3.156e7:.2f} years")
                    elif t_half > 86400:
                        print(f"          {t_half/86400:.2f} days")
                    elif t_half > 3600:
                        print(f"          {t_half/3600:.2f} hours")
                else:
                    print(f"ERROR: Half-life data not available for {symbol}-{a}")

            elif command == 'average':
                avg_mass = lookup.calculate_average_mass(z)
                if avg_mass:
                    print(f"\nElement: {symbol} (Z={z})")
                    print(f"Calculated average mass: {avg_mass:.4f} amu")

                    abundances = lookup.get_natural_abundance(z)
                    print("\nCalculation:")
                    for a_val, frac in sorted(abundances.items()):
                        mass = lookup.get_atomic_mass(z, a_val)
                        contribution = frac * mass
                        print(f"  {symbol}-{a_val}: {frac:.6f} × {mass:.6f} = {contribution:.6f}")
                else:
                    print(f"Cannot calculate average mass for {symbol}")

            else:
                print(f"ERROR: Unknown command '{command}'")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Isotope Properties Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get atomic mass
  python isotope_properties.py --isotope "U-235"
  python isotope_properties.py --mass "Fe-56"

  # Get natural abundances
  python isotope_properties.py --element "Cl" --abundance

  # Get half-life
  python isotope_properties.py --isotope "Co-60" --halflife

  # Interactive mode (default)
  python isotope_properties.py
        """
    )

    parser.add_argument('--isotope', help='Isotope (e.g., U-235)')
    parser.add_argument('--element', help='Element symbol (e.g., Cl)')
    parser.add_argument('--mass', help='Get atomic mass')
    parser.add_argument('--abundance', action='store_true', help='Get natural abundances')
    parser.add_argument('--halflife', action='store_true', help='Get half-life')
    parser.add_argument('--average', action='store_true', help='Calculate average mass')

    args = parser.parse_args()
    lookup = IsotopeLookup()

    # Command-line mode
    if args.mass or args.isotope:
        isotope_str = args.mass or args.isotope
        import re
        match = re.match(r'^([A-Z][a-z]?)-?(\d+)?$', isotope_str, re.IGNORECASE)
        if match:
            symbol = match.group(1).capitalize()
            if len(symbol) == 2:
                symbol = symbol[0] + symbol[1].lower()
            a = int(match.group(2)) if match.group(2) else None

            if symbol in lookup.db.SYMBOL_TO_Z:
                z = lookup.db.SYMBOL_TO_Z[symbol]
                if a:
                    mass = lookup.get_atomic_mass(z, a)
                    if mass:
                        print(f"Isotope: {symbol}-{a}")
                        print(f"Atomic mass: {mass:.8f} amu")
                    else:
                        print(f"ERROR: Mass data not available for {symbol}-{a}")
                        sys.exit(1)
                else:
                    mass = lookup.get_atomic_mass(z)
                    print(f"Element: {symbol}")
                    print(f"Average atomic mass: {mass:.3f} amu")
            else:
                print(f"ERROR: Unknown element '{symbol}'")
                sys.exit(1)
        else:
            print(f"ERROR: Could not parse '{isotope_str}'")
            sys.exit(1)

    elif args.element and args.abundance:
        symbol = args.element.capitalize()
        if len(symbol) == 2:
            symbol = symbol[0] + symbol[1].lower()

        if symbol in lookup.db.SYMBOL_TO_Z:
            z = lookup.db.SYMBOL_TO_Z[symbol]
            abundances = lookup.get_natural_abundance(z)
            if abundances:
                print(f"Element: {symbol} (Z={z})")
                print("Natural isotopic composition:")
                for a, frac in sorted(abundances.items()):
                    print(f"  {symbol}-{a}: {frac*100:.4f}% ({frac:.6f})")
            else:
                print(f"No natural abundance data for {symbol}")
                sys.exit(1)
        else:
            print(f"ERROR: Unknown element '{symbol}'")
            sys.exit(1)

    else:
        # Interactive mode (default)
        interactive_mode()


if __name__ == '__main__':
    main()
