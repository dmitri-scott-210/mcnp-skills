#!/usr/bin/env python3
"""
MCNP Unit Converter - Interactive Conversion Tool

Standalone utility for converting between different unit systems for MCNP simulations.
Handles energy, length, density, temperature, cross sections, activity, mass, angle, and time conversions.

Usage:
    python unit_converter.py                    # Interactive mode
    python unit_converter.py --help             # Show help
    python unit_converter.py energy 14.1 keV MeV  # Command line conversion

Author: MCNP Skills Project
License: MIT
"""

import sys
import argparse
import math

# Physical constants (CODATA 2018)
CONSTANTS = {
    'c': 2.99792458e8,           # Speed of light (m/s)
    'N_A': 6.02214076e23,         # Avogadro's number (mol⁻¹)
    'k_B': 8.617333262e-11,       # Boltzmann constant (MeV/K)
    'k_B_eV': 8.617333262e-5,     # Boltzmann constant (eV/K)
    'amu_g': 1.66053906660e-24,   # Atomic mass unit (g)
    'amu_MeV': 931.494102,        # Atomic mass unit (MeV/c²)
    'eV_J': 1.602176634e-19,      # Electron volt (J)
    'barn_cm2': 1e-24,            # Barn (cm²)
    'Ci_Bq': 3.7e10,              # Curie (Bq)
    'shake_s': 1e-8,              # Shake (s)
}

class UnitConverter:
    """MCNP unit conversion engine"""

    def __init__(self):
        self.conversions_performed = []

    # ==================== ENERGY CONVERSIONS ====================

    def convert_energy(self, value, from_unit, to_unit):
        """Convert energy between MeV, eV, keV, GeV, J"""
        # Convert to MeV first
        to_MeV = {
            'MeV': 1.0,
            'eV': 1e-6,
            'keV': 1e-3,
            'GeV': 1e3,
            'J': 1.0 / (CONSTANTS['eV_J'] * 1e6),  # J to MeV
        }

        if from_unit not in to_MeV:
            raise ValueError(f"Unknown energy unit: {from_unit}")
        if to_unit not in to_MeV:
            raise ValueError(f"Unknown energy unit: {to_unit}")

        # Convert: value -> MeV -> target unit
        value_MeV = value * to_MeV[from_unit]
        result = value_MeV / to_MeV[to_unit]

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== LENGTH CONVERSIONS ====================

    def convert_length(self, value, from_unit, to_unit):
        """Convert length between cm, m, mm, inch, Angstrom"""
        # Convert to cm first
        to_cm = {
            'cm': 1.0,
            'm': 100.0,
            'mm': 0.1,
            'inch': 2.54,
            'Angstrom': 1e-8,
            'A': 1e-8,
        }

        if from_unit not in to_cm:
            raise ValueError(f"Unknown length unit: {from_unit}")
        if to_unit not in to_cm:
            raise ValueError(f"Unknown length unit: {to_unit}")

        # Convert: value -> cm -> target unit
        value_cm = value * to_cm[from_unit]
        result = value_cm / to_cm[to_unit]

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== DENSITY CONVERSIONS ====================

    def convert_density(self, value, from_unit, to_unit, atomic_weight=None):
        """Convert density between g/cm³, kg/m³, atom/b-cm"""
        if from_unit == 'g/cm3' and to_unit == 'kg/m3':
            result = value * 1000.0
        elif from_unit == 'kg/m3' and to_unit == 'g/cm3':
            result = value / 1000.0
        elif from_unit == 'g/cm3' and to_unit == 'atom/b-cm':
            if atomic_weight is None:
                raise ValueError("Atomic weight required for g/cm³ to atom/b-cm conversion")
            result = (value * CONSTANTS['N_A']) / (atomic_weight * 1e24)
        elif from_unit == 'atom/b-cm' and to_unit == 'g/cm3':
            if atomic_weight is None:
                raise ValueError("Atomic weight required for atom/b-cm to g/cm³ conversion")
            result = (value * atomic_weight * 1e24) / CONSTANTS['N_A']
        else:
            raise ValueError(f"Unsupported density conversion: {from_unit} to {to_unit}")

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== TEMPERATURE CONVERSIONS ====================

    def convert_temperature(self, value, from_unit, to_unit):
        """Convert temperature between K, °C, °F, MeV, eV"""
        # Convert to Kelvin first
        if from_unit == 'K':
            value_K = value
        elif from_unit == 'C':
            value_K = value + 273.15
        elif from_unit == 'F':
            value_K = (value - 32) * 5/9 + 273.15
        elif from_unit == 'MeV':
            value_K = value / CONSTANTS['k_B']
        elif from_unit == 'eV':
            value_K = value / CONSTANTS['k_B_eV']
        else:
            raise ValueError(f"Unknown temperature unit: {from_unit}")

        # Convert from Kelvin to target
        if to_unit == 'K':
            result = value_K
        elif to_unit == 'C':
            result = value_K - 273.15
        elif to_unit == 'F':
            result = (value_K - 273.15) * 9/5 + 32
        elif to_unit == 'MeV':
            result = value_K * CONSTANTS['k_B']
        elif to_unit == 'eV':
            result = value_K * CONSTANTS['k_B_eV']
        else:
            raise ValueError(f"Unknown temperature unit: {to_unit}")

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== CROSS SECTION CONVERSIONS ====================

    def convert_cross_section(self, value, from_unit, to_unit):
        """Convert cross section between barn, mb, cm²"""
        # Convert to barns first
        to_barn = {
            'barn': 1.0,
            'b': 1.0,
            'mb': 1e-3,
            'millibarn': 1e-3,
            'cm2': 1e24,
        }

        if from_unit not in to_barn:
            raise ValueError(f"Unknown cross section unit: {from_unit}")
        if to_unit not in to_barn:
            raise ValueError(f"Unknown cross section unit: {to_unit}")

        # Convert: value -> barn -> target unit
        value_barn = value * to_barn[from_unit]
        result = value_barn / to_barn[to_unit]

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== ACTIVITY CONVERSIONS ====================

    def convert_activity(self, value, from_unit, to_unit):
        """Convert activity between Bq, Ci, mCi, μCi, dps"""
        # Convert to Bq first
        to_Bq = {
            'Bq': 1.0,
            'dps': 1.0,
            'Ci': CONSTANTS['Ci_Bq'],
            'mCi': CONSTANTS['Ci_Bq'] * 1e-3,
            'uCi': CONSTANTS['Ci_Bq'] * 1e-6,
            'microCi': CONSTANTS['Ci_Bq'] * 1e-6,
        }

        if from_unit not in to_Bq:
            raise ValueError(f"Unknown activity unit: {from_unit}")
        if to_unit not in to_Bq:
            raise ValueError(f"Unknown activity unit: {to_unit}")

        # Convert: value -> Bq -> target unit
        value_Bq = value * to_Bq[from_unit]
        result = value_Bq / to_Bq[to_unit]

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== MASS CONVERSIONS ====================

    def convert_mass(self, value, from_unit, to_unit):
        """Convert mass between g, kg, amu, MeV/c²"""
        # Convert to grams first
        to_g = {
            'g': 1.0,
            'kg': 1000.0,
            'amu': CONSTANTS['amu_g'],
        }

        if from_unit == 'MeV/c2':
            # MeV/c² to grams
            value_amu = value / CONSTANTS['amu_MeV']
            value_g = value_amu * CONSTANTS['amu_g']
        elif from_unit in to_g:
            value_g = value * to_g[from_unit]
        else:
            raise ValueError(f"Unknown mass unit: {from_unit}")

        # Convert from grams to target
        if to_unit == 'g':
            result = value_g
        elif to_unit == 'kg':
            result = value_g / 1000.0
        elif to_unit == 'amu':
            result = value_g / CONSTANTS['amu_g']
        elif to_unit == 'MeV/c2':
            value_amu = value_g / CONSTANTS['amu_g']
            result = value_amu * CONSTANTS['amu_MeV']
        else:
            raise ValueError(f"Unknown mass unit: {to_unit}")

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== TIME CONVERSIONS ====================

    def convert_time(self, value, from_unit, to_unit):
        """Convert time between s, ms, μs, ns, shakes"""
        # Convert to seconds first
        to_s = {
            's': 1.0,
            'ms': 1e-3,
            'us': 1e-6,
            'microsecond': 1e-6,
            'ns': 1e-9,
            'nanosecond': 1e-9,
            'shake': CONSTANTS['shake_s'],
        }

        if from_unit not in to_s:
            raise ValueError(f"Unknown time unit: {from_unit}")
        if to_unit not in to_s:
            raise ValueError(f"Unknown time unit: {to_unit}")

        # Convert: value -> seconds -> target unit
        value_s = value * to_s[from_unit]
        result = value_s / to_s[to_unit]

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    # ==================== ANGLE CONVERSIONS ====================

    def convert_angle(self, value, from_unit, to_unit):
        """Convert angle between degrees, radians"""
        if from_unit == 'deg' and to_unit == 'rad':
            result = value * math.pi / 180.0
        elif from_unit == 'rad' and to_unit == 'deg':
            result = value * 180.0 / math.pi
        elif from_unit == to_unit:
            result = value
        else:
            raise ValueError(f"Unsupported angle conversion: {from_unit} to {to_unit}")

        self._log_conversion(value, from_unit, result, to_unit)
        return result

    def angle_to_cosine(self, angle_deg):
        """Convert angle in degrees to direction cosine"""
        angle_rad = angle_deg * math.pi / 180.0
        return math.cos(angle_rad)

    # ==================== UTILITY FUNCTIONS ====================

    def _log_conversion(self, value_from, unit_from, value_to, unit_to):
        """Log conversion for history"""
        self.conversions_performed.append({
            'from': (value_from, unit_from),
            'to': (value_to, unit_to)
        })

    def print_history(self):
        """Print conversion history"""
        if not self.conversions_performed:
            print("No conversions performed yet.")
            return

        print("\n" + "="*60)
        print("CONVERSION HISTORY")
        print("="*60)
        for i, conv in enumerate(self.conversions_performed, 1):
            from_val, from_unit = conv['from']
            to_val, to_unit = conv['to']
            print(f"{i}. {from_val} {from_unit} = {to_val:.6g} {to_unit}")
        print("="*60 + "\n")


def interactive_mode():
    """Run interactive conversion session"""
    converter = UnitConverter()

    print("\n" + "="*60)
    print(" "*15 + "MCNP UNIT CONVERTER")
    print("="*60)
    print("Supported conversions:")
    print("  1. Energy:       MeV, eV, keV, GeV, J")
    print("  2. Length:       cm, m, mm, inch, Angstrom")
    print("  3. Density:      g/cm³, kg/m³, atom/b-cm")
    print("  4. Temperature:  K, °C, °F, MeV, eV")
    print("  5. Cross section: barn, mb, cm²")
    print("  6. Activity:     Bq, Ci, mCi, μCi, dps")
    print("  7. Mass:         g, kg, amu, MeV/c²")
    print("  8. Time:         s, ms, μs, ns, shake")
    print("  9. Angle:        deg, rad, cosine")
    print("\nType 'help' for detailed info, 'history' to see past conversions, 'quit' to exit")
    print("="*60 + "\n")

    while True:
        try:
            cmd = input("Enter conversion type (or 'quit'): ").strip().lower()

            if cmd in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if cmd == 'history':
                converter.print_history()
                continue

            if cmd == 'help':
                print_help()
                continue

            # Get conversion parameters
            if cmd in ['energy', '1']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (MeV, eV, keV, GeV, J): ").strip()
                to_unit = input("To unit (MeV, eV, keV, GeV, J): ").strip()
                result = converter.convert_energy(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['length', '2']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (cm, m, mm, inch, Angstrom): ").strip()
                to_unit = input("To unit (cm, m, mm, inch, Angstrom): ").strip()
                result = converter.convert_length(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['density', '3']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (g/cm3, kg/m3, atom/b-cm): ").strip()
                to_unit = input("To unit (g/cm3, kg/m3, atom/b-cm): ").strip()

                if 'atom' in from_unit or 'atom' in to_unit:
                    atomic_weight = float(input("Enter atomic weight (g/mol): "))
                    result = converter.convert_density(value, from_unit, to_unit, atomic_weight)
                else:
                    result = converter.convert_density(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['temperature', '4']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (K, C, F, MeV, eV): ").strip()
                to_unit = input("To unit (K, C, F, MeV, eV): ").strip()
                result = converter.convert_temperature(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['cross', 'crosssection', '5']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (barn, mb, cm2): ").strip()
                to_unit = input("To unit (barn, mb, cm2): ").strip()
                result = converter.convert_cross_section(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['activity', '6']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (Bq, Ci, mCi, uCi, dps): ").strip()
                to_unit = input("To unit (Bq, Ci, mCi, uCi, dps): ").strip()
                result = converter.convert_activity(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['mass', '7']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (g, kg, amu, MeV/c2): ").strip()
                to_unit = input("To unit (g, kg, amu, MeV/c2): ").strip()
                result = converter.convert_mass(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['time', '8']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (s, ms, us, ns, shake): ").strip()
                to_unit = input("To unit (s, ms, us, ns, shake): ").strip()
                result = converter.convert_time(value, from_unit, to_unit)
                print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit}\n")

            elif cmd in ['angle', '9']:
                value = float(input("Enter value: "))
                from_unit = input("From unit (deg, rad): ").strip()
                to_unit_input = input("To unit (deg, rad, cosine): ").strip()

                if to_unit_input == 'cosine':
                    # Convert to degrees first if needed
                    if from_unit == 'rad':
                        angle_deg = value * 180.0 / math.pi
                    else:
                        angle_deg = value
                    result = converter.angle_to_cosine(angle_deg)
                    print(f"\n✓ {value} {from_unit} → cos({angle_deg:.2f}°) = {result:.6g}\n")
                else:
                    result = converter.convert_angle(value, from_unit, to_unit_input)
                    print(f"\n✓ {value} {from_unit} = {result:.6g} {to_unit_input}\n")

            else:
                print(f"Unknown command: {cmd}. Type 'help' for assistance.\n")

        except ValueError as e:
            print(f"\n✗ Error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}\n")


def print_help():
    """Print detailed help information"""
    help_text = """
MCNP UNIT CONVERTER - HELP

COMMAND LINE USAGE:
    python unit_converter.py <type> <value> <from_unit> <to_unit> [atomic_weight]

EXAMPLES:
    python unit_converter.py energy 14.1 keV MeV
    python unit_converter.py length 2.5 m cm
    python unit_converter.py density 2.7 g/cm3 atom/b-cm 26.982
    python unit_converter.py temperature 500 C K
    python unit_converter.py activity 10 mCi Bq

INTERACTIVE MODE:
    python unit_converter.py

    Then follow the prompts for conversion type and values.

MCNP STANDARD UNITS:
    - Energy:        MeV (mega-electron volts)
    - Length:        cm (centimeters)
    - Density:       g/cm³ (negative) or atom/b-cm (positive)
    - Temperature:   MeV or K (Kelvin on TMP card)
    - Cross section: barn (10⁻²⁴ cm²)
    - Time:          shake (10⁻⁸ seconds)
    - Mass:          amu (atomic mass units)
    - Activity:      Bq (Becquerel) or Ci (Curie)

PHYSICAL CONSTANTS:
    c   = 2.998×10⁸ m/s        (speed of light)
    N_A = 6.022×10²³ mol⁻¹     (Avogadro's number)
    k_B = 8.617×10⁻¹¹ MeV/K    (Boltzmann constant)
    1 amu = 931.494 MeV/c²     (atomic mass unit)
    1 barn = 10⁻²⁴ cm²         (cross section unit)
    1 Ci = 3.7×10¹⁰ Bq         (activity unit)

For more information, see SKILL.md in the mcnp-unit-converter directory.
"""
    print(help_text)


def command_line_mode(args):
    """Run single conversion from command line"""
    converter = UnitConverter()

    try:
        conv_type = args.type.lower()
        value = args.value
        from_unit = args.from_unit
        to_unit = args.to_unit

        if conv_type == 'energy':
            result = converter.convert_energy(value, from_unit, to_unit)
        elif conv_type == 'length':
            result = converter.convert_length(value, from_unit, to_unit)
        elif conv_type == 'density':
            if args.atomic_weight is None:
                if 'atom' in from_unit or 'atom' in to_unit:
                    print("Error: Atomic weight required for density conversions involving atom/b-cm")
                    sys.exit(1)
                result = converter.convert_density(value, from_unit, to_unit)
            else:
                result = converter.convert_density(value, from_unit, to_unit, args.atomic_weight)
        elif conv_type == 'temperature':
            result = converter.convert_temperature(value, from_unit, to_unit)
        elif conv_type == 'cross_section':
            result = converter.convert_cross_section(value, from_unit, to_unit)
        elif conv_type == 'activity':
            result = converter.convert_activity(value, from_unit, to_unit)
        elif conv_type == 'mass':
            result = converter.convert_mass(value, from_unit, to_unit)
        elif conv_type == 'time':
            result = converter.convert_time(value, from_unit, to_unit)
        elif conv_type == 'angle':
            if to_unit == 'cosine':
                if from_unit == 'rad':
                    angle_deg = value * 180.0 / math.pi
                else:
                    angle_deg = value
                result = converter.angle_to_cosine(angle_deg)
                print(f"{value} {from_unit} → cos({angle_deg:.2f}°) = {result:.6g}")
                return
            else:
                result = converter.convert_angle(value, from_unit, to_unit)
        else:
            print(f"Unknown conversion type: {conv_type}")
            sys.exit(1)

        print(f"{value} {from_unit} = {result:.6g} {to_unit}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='MCNP Unit Converter - Convert between different unit systems',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python unit_converter.py                                # Interactive mode
    python unit_converter.py energy 14.1 keV MeV            # Convert 14.1 keV to MeV
    python unit_converter.py length 2.5 m cm                # Convert 2.5 m to cm
    python unit_converter.py density 2.7 g/cm3 atom/b-cm 26.982  # Al density with atomic weight
    python unit_converter.py temperature 500 C K            # Convert 500°C to Kelvin
    python unit_converter.py activity 10 mCi Bq             # Convert 10 mCi to Becquerels

For MCNP standard units and more information, see SKILL.md
        """
    )

    parser.add_argument('type', nargs='?', help='Conversion type (energy, length, density, etc.)')
    parser.add_argument('value', nargs='?', type=float, help='Value to convert')
    parser.add_argument('from_unit', nargs='?', help='Source unit')
    parser.add_argument('to_unit', nargs='?', help='Target unit')
    parser.add_argument('atomic_weight', nargs='?', type=float, help='Atomic weight (for density conversions)')
    parser.add_argument('--help-detailed', action='store_true', help='Show detailed help')

    args = parser.parse_args()

    if args.help_detailed:
        print_help()
    elif args.type is None:
        # Interactive mode
        interactive_mode()
    else:
        # Command line mode
        command_line_mode(args)


if __name__ == '__main__':
    main()
