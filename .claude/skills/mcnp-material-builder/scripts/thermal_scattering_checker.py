#!/usr/bin/env python3
"""
MCNP Thermal Scattering Checker

Validates that materials requiring S(alpha,beta) treatment have MT cards.

CRITICAL CHECK: Detects missing graphite MT cards (common professional model error)

Usage:
    python thermal_scattering_checker.py input.i
    python thermal_scattering_checker.py --verbose input.i

Author: MCNP Skills System
Version: 1.0
Created: 2025-11-08
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Elements that REQUIRE thermal scattering in thermal systems
THERMAL_SCATTERING_ELEMENTS = {
    '1': 'H',   # Hydrogen
    '2': 'He',  # Helium (sometimes)
    '4': 'Be',  # Beryllium
    '6': 'C',   # Carbon (GRAPHITE - CRITICAL!)
    '8': 'O',   # Oxygen (in water, BeO)
}

# S(alpha,beta) table patterns
SALPHABETA_TABLES = {
    'H-H2O': 'Hydrogen in water',
    'H-CH2': 'Hydrogen in polyethylene',
    'H-BENZ': 'Hydrogen in benzene',
    'H-ZRH': 'Hydrogen in zirconium hydride',
    'D-D2O': 'Deuterium in heavy water',
    'C-GRPH': 'Carbon in graphite',
    'Be-MET': 'Beryllium metal',
    'Be-BEO': 'Beryllium in BeO',
    'O-BEO': 'Oxygen in BeO',
    'LWTR': 'Light water (old format)',
    'HWTR': 'Heavy water (old format)',
    'POLY': 'Polyethylene (old format)',
    'GRPH': 'Graphite (old format)',
    'BE': 'Beryllium (old format)',
}


class MaterialCard:
    """Represents an MCNP material card"""

    def __init__(self, material_number: str):
        self.number = material_number
        self.isotopes: List[Tuple[str, str, str]] = []  # (ZAID, fraction, library)
        self.has_mt_card = False
        self.mt_tables: List[str] = []
        self.tmp_temperature = None
        self.elements_present: Set[str] = set()

    def add_isotope(self, zaid: str, fraction: str):
        """Add isotope to material composition"""
        # Extract Z, A, library
        match = re.match(r'(\d+)(\d{3})\.?(\d*\w*)?', zaid)
        if match:
            z = str(int(match.group(1)))  # Atomic number
            a = match.group(2)  # Mass number (000 for natural)
            lib = match.group(3) if match.group(3) else ''
            self.isotopes.append((f"{z}{a}", fraction, lib))
            self.elements_present.add(z)

    def needs_thermal_scattering(self) -> bool:
        """Check if material contains elements requiring S(alpha,beta)"""
        return bool(self.elements_present & THERMAL_SCATTERING_ELEMENTS.keys())

    def get_elements_needing_mt(self) -> List[str]:
        """Return list of element symbols that need MT cards"""
        return [THERMAL_SCATTERING_ELEMENTS[z] for z in
                self.elements_present & THERMAL_SCATTERING_ELEMENTS.keys()]


def parse_mcnp_input(filename: str) -> Tuple[Dict[str, MaterialCard], Dict[str, float]]:
    """
    Parse MCNP input file for material and MT cards

    Returns:
        materials: Dict of material number → MaterialCard
        tmp_cards: Dict of material number → temperature (MeV)
    """
    materials = {}
    tmp_cards = {}

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Track which block we're in
    in_data_block = False
    current_material = None
    current_card_type = None
    continuation_lines = []

    for line in lines:
        # Strip comments
        if 'c ' == line[:2].lower() and line[1] == ' ':
            continue

        # Handle line continuation
        stripped = line.rstrip()
        if stripped and stripped[-1] == '&':
            continuation_lines.append(stripped[:-1])
            continue
        else:
            if continuation_lines:
                full_line = ''.join(continuation_lines) + stripped
                continuation_lines = []
            else:
                full_line = stripped

        # Skip blank lines
        if not full_line.strip():
            current_material = None
            current_card_type = None
            continue

        # Check for data block start (first blank line after cell cards)
        # Simple heuristic: data cards start with known keywords
        if full_line.strip() and full_line[0] not in ['c', 'C', ' ']:
            in_data_block = True

        # Parse M cards (material composition)
        m_match = re.match(r'^[mM](\d+)\s+', full_line)
        if m_match:
            mat_num = m_match.group(1)
            if mat_num not in materials:
                materials[mat_num] = MaterialCard(mat_num)
            current_material = mat_num
            current_card_type = 'M'

            # Parse isotopes on this line
            remainder = full_line[m_match.end():]
            parse_material_isotopes(materials[mat_num], remainder)
            continue

        # Parse MT cards (thermal scattering)
        mt_match = re.match(r'^[mM][tT](\d+)\s+', full_line)
        if mt_match:
            mat_num = mt_match.group(1)
            if mat_num in materials:
                materials[mat_num].has_mt_card = True
                remainder = full_line[mt_match.end():]
                tables = remainder.split()
                materials[mat_num].mt_tables.extend(tables)
            current_card_type = 'MT'
            continue

        # Parse TMP cards (temperature)
        tmp_match = re.match(r'^[tT][mM][pP](\d+)\s+(\S+)', full_line)
        if tmp_match:
            mat_num = tmp_match.group(1)
            temp_mev = float(tmp_match.group(2))
            tmp_cards[mat_num] = temp_mev
            current_card_type = 'TMP'
            continue

        # Continuation of current card
        if current_material and current_card_type == 'M':
            parse_material_isotopes(materials[current_material], full_line)

    return materials, tmp_cards


def parse_material_isotopes(material: MaterialCard, line: str):
    """Extract ZAID and fraction pairs from material card line"""
    tokens = line.split()
    i = 0
    while i < len(tokens) - 1:
        zaid = tokens[i]
        fraction = tokens[i + 1]
        # Check if it looks like a ZAID (number with optional .nnX)
        if re.match(r'\d+\.?\d*\w*', zaid) and re.match(r'-?\d+\.?\d*[eE]?[+-]?\d*', fraction):
            material.add_isotope(zaid, fraction)
            i += 2
        else:
            i += 1


def temperature_from_mev(temp_mev: float) -> float:
    """Convert temperature from MeV to Kelvin"""
    # T [K] = T [MeV] / 8.617e-11
    return temp_mev / 8.617e-11


def check_mt_temperature_match(mt_table: str, tmp_kelvin: float) -> Tuple[bool, str]:
    """
    Check if MT table temperature matches TMP card temperature

    Returns:
        (matches, message)
    """
    # Extract temperature from table name (approximate)
    temp_map = {
        '40': (293, 296),    # Room temp
        '41': (323, 400),    # Warm
        '42': (373, 500),    # Elevated
        '43': (423, 600),    # Operating
        '44': (473, 700),    # High
        '45': (523, 800),    # Very high
        '46': (573, 1000),   # VHTR
        '47': (623, 1200),   # Extreme
        '48': (800, 1600),   # Accident
        '49': (1000, 2000),  # Maximum
    }

    # Extract nn from table name (e.g., C-GRPH.43t → 43, GRPH.47T → 47)
    match = re.search(r'\.(\d{2})[tT]', mt_table)
    if match:
        code = match.group(1)
        if code in temp_map:
            t_min, t_max = temp_map[code]
            if t_min <= tmp_kelvin <= t_max:
                return True, f"Temperature match OK ({tmp_kelvin:.0f}K within {t_min}-{t_max}K range)"
            else:
                return False, f"MISMATCH: TMP={tmp_kelvin:.0f}K, but MT table is for {t_min}-{t_max}K"

    return None, "Cannot determine MT table temperature"


def main():
    parser = argparse.ArgumentParser(
        description='Check MCNP input for missing thermal scattering (MT) cards'
    )
    parser.add_argument('input_file', help='MCNP input file to check')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed information for all materials')
    parser.add_argument('--critical-only', action='store_true',
                        help='Only report critical errors (missing MT cards)')

    args = parser.parse_args()

    if not Path(args.input_file).exists():
        print(f"ERROR: File '{args.input_file}' not found!")
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print(f"MCNP Thermal Scattering Checker")
    print(f"{'=' * 70}")
    print(f"Input file: {args.input_file}\n")

    # Parse input file
    materials, tmp_cards = parse_mcnp_input(args.input_file)

    if not materials:
        print("WARNING: No material cards found in input file!")
        sys.exit(0)

    print(f"Found {len(materials)} material(s)\n")

    # Check each material
    errors = []
    warnings = []
    ok_count = 0

    for mat_num in sorted(materials.keys(), key=lambda x: int(x)):
        material = materials[mat_num]

        # Skip materials that don't need thermal scattering
        if not material.needs_thermal_scattering():
            if args.verbose:
                print(f"Material M{mat_num}: No thermal scattering elements present")
            continue

        # Material needs S(alpha,beta) treatment
        elements_needing_mt = material.get_elements_needing_mt()

        # CRITICAL: Check for graphite
        has_carbon = '6' in material.elements_present
        has_hydrogen = '1' in material.elements_present

        if not material.has_mt_card:
            # CRITICAL ERROR
            error_msg = (
                f"Material M{mat_num}: MISSING MT CARD!\n"
                f"  Contains: {', '.join(elements_needing_mt)}\n"
                f"  Impact: Free-gas scattering instead of molecular binding\n"
            )

            if has_carbon:
                error_msg += (
                    f"  **CRITICAL**: Graphite detected - reactivity error 1000-5000 pcm likely!\n"
                    f"  FIX: Add MT{mat_num}  C-GRPH.43t (or appropriate temperature)\n"
                )
            elif has_hydrogen:
                error_msg += (
                    f"  FIX: Add MT{mat_num}  H-H2O.40t (or H-CH2.40t, etc.)\n"
                )

            errors.append(error_msg)
            print(f"❌ {error_msg}")

        else:
            # MT card present - check details
            print(f"✅ Material M{mat_num}: MT card present")
            print(f"   Contains: {', '.join(elements_needing_mt)}")
            print(f"   MT tables: {', '.join(material.mt_tables)}")

            # Check temperature match if TMP card present
            if mat_num in tmp_cards:
                tmp_kelvin = temperature_from_mev(tmp_cards[mat_num])
                print(f"   TMP{mat_num} = {tmp_cards[mat_num]:.2e} MeV ({tmp_kelvin:.0f} K)")

                for table in material.mt_tables:
                    match, msg = check_mt_temperature_match(table, tmp_kelvin)
                    if match is True:
                        print(f"   ✅ {msg}")
                    elif match is False:
                        warn_msg = f"Material M{mat_num}: {msg}"
                        warnings.append(warn_msg)
                        print(f"   ⚠️  {msg}")

            ok_count += 1
            print()

    # Summary
    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total materials checked: {len([m for m in materials.values() if m.needs_thermal_scattering()])}")
    print(f"✅ Correct MT cards: {ok_count}")
    print(f"❌ Missing MT cards: {len(errors)}")
    print(f"⚠️  Warnings: {len(warnings)}")

    if errors:
        print(f"\n{'=' * 70}")
        print(f"CRITICAL ERRORS (must fix before running)")
        print(f"{'=' * 70}")
        for error in errors:
            print(error)

    if warnings and not args.critical_only:
        print(f"\n{'=' * 70}")
        print(f"WARNINGS (check carefully)")
        print(f"{'=' * 70}")
        for warning in warnings:
            print(f"⚠️  {warning}")

    # Exit code
    if errors:
        print(f"\n❌ FAILED: {len(errors)} critical error(s) found")
        print(f"   Fix missing MT cards before running MCNP!")
        sys.exit(1)
    elif warnings:
        print(f"\n⚠️  PASSED with warnings: Review temperature mismatches")
        sys.exit(0)
    else:
        print(f"\n✅ PASSED: All thermal scattering requirements met")
        sys.exit(0)


if __name__ == '__main__':
    main()
