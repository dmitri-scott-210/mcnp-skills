#!/usr/bin/env python3
"""
MCNP ZAID and Library Validator

Purpose: Validate ZAID format, check library availability in xsdir, and verify
         material card consistency.

Features:
  - ZAID format validation (ZZZAAA.nnX)
  - xsdir availability checking
  - Library consistency checking across materials
  - Generate warnings for missing or inconsistent data
  - Material card validator

Usage:
  python zaid_library_validator.py [input_file]
  python zaid_library_validator.py --zaid 92235.80c
  python zaid_library_validator.py --interactive

Author: MCNP Material Builder Skill
Version: 1.0
Date: 2025-11-03
"""

import sys
import re
import os
from typing import List, Tuple, Dict, Set, Optional
from pathlib import Path


class ZAIDValidator:
    """Validator for MCNP ZAID format and library availability."""

    # ZAID format regex patterns
    ZAID_PATTERN_FULL = re.compile(r'^(\d{1,3})(\d{3})\.(\d{2})([a-z])$', re.IGNORECASE)
    ZAID_PATTERN_SHORT = re.compile(r'^(\d{1,3})(\d{3})$')
    ZAID_PATTERN_SYMBOL = re.compile(r'^([A-Z][a-z]?)-(\d+)(m?)$', re.IGNORECASE)

    # Particle type designators
    PARTICLE_TYPES = {
        'c': 'continuous-energy neutron',
        't': 'thermal S(alpha,beta)',
        'p': 'photoatomic',
        'u': 'photonuclear',
        'e': 'electron',
        'h': 'proton',
        'd': 'deuteron',
        's': 'helion (He-3)',
        'a': 'alpha',
        'g': 'photon',
    }

    def __init__(self, xsdir_path: Optional[str] = None):
        """
        Initialize validator.

        Args:
            xsdir_path: Path to xsdir file. If None, uses $DATAPATH/xsdir.
        """
        self.xsdir_path = xsdir_path or self._find_xsdir()
        self.available_zaids: Set[str] = set()

        if self.xsdir_path and os.path.exists(self.xsdir_path):
            self._load_xsdir()

    def _find_xsdir(self) -> Optional[str]:
        """Find xsdir file from DATAPATH environment variable."""
        datapath = os.getenv('DATAPATH')
        if datapath:
            xsdir_file = os.path.join(datapath, 'xsdir')
            if os.path.exists(xsdir_file):
                return xsdir_file

        # Try common locations
        common_paths = [
            '/usr/local/MCNP_DATA/xsdir',
            '/opt/mcnp/data/xsdir',
            'C:/MCNP_DATA/xsdir',
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def _load_xsdir(self):
        """Load available ZAIDs from xsdir file."""
        try:
            with open(self.xsdir_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(('c', 'C', '#')):
                        parts = line.split()
                        if parts:
                            zaid = parts[0]
                            self.available_zaids.add(zaid.lower())
        except Exception as e:
            print(f"Warning: Could not load xsdir: {e}", file=sys.stderr)

    def validate_zaid_format(self, zaid: str) -> Tuple[bool, str]:
        """
        Validate ZAID format.

        Args:
            zaid: ZAID string to validate

        Returns:
            (is_valid, message)

        Examples:
            >>> validator.validate_zaid_format("92235.80c")
            (True, "Valid full ZAID: Z=92, A=235, lib=80, particle=c (continuous-energy neutron)")
        """
        zaid = zaid.strip()

        # Try full format (ZZZAAA.nnX)
        match = self.ZAID_PATTERN_FULL.match(zaid)
        if match:
            Z, A, lib, particle = match.groups()
            Z_int = int(Z)
            A_int = int(A)

            if not (1 <= Z_int <= 118):
                return (False, f"Invalid atomic number Z={Z_int} (must be 1-118)")

            particle_desc = self.PARTICLE_TYPES.get(particle.lower(), "unknown")
            msg = f"Valid full ZAID: Z={Z_int}, A={A_int}, lib={lib}, particle={particle} ({particle_desc})"
            return (True, msg)

        # Try short format (ZZZAAA)
        match = self.ZAID_PATTERN_SHORT.match(zaid)
        if match:
            Z, A = match.groups()
            Z_int = int(Z)
            A_int = int(A)

            if not (1 <= Z_int <= 118):
                return (False, f"Invalid atomic number Z={Z_int} (must be 1-118)")

            msg = f"Valid short ZAID: Z={Z_int}, A={A_int} (library will be determined by xLIB or M0)"
            return (True, msg)

        # Try symbol format (H-1, Ag-110m)
        match = self.ZAID_PATTERN_SYMBOL.match(zaid)
        if match:
            symbol, mass, metastable = match.groups()
            msg = f"Valid symbol ZAID: {symbol}-{mass}{metastable} (modern format)"
            return (True, msg)

        return (False, f"Invalid ZAID format: '{zaid}'")

    def check_availability(self, zaid: str) -> Tuple[bool, str]:
        """
        Check if ZAID is available in xsdir.

        Args:
            zaid: ZAID string to check

        Returns:
            (is_available, message)
        """
        if not self.available_zaids:
            return (False, "xsdir not loaded")

        zaid_lower = zaid.strip().lower()

        if zaid_lower in self.available_zaids:
            return (True, f"ZAID '{zaid}' found in xsdir")

        # Try without library suffix
        zaid_base = zaid.split('.')[0]
        matches = [z for z in self.available_zaids if z.startswith(zaid_base)]

        if matches:
            return (False, f"ZAID '{zaid}' not found, but similar: {', '.join(matches[:5])}")
        else:
            return (False, f"ZAID '{zaid}' not found in xsdir")

    def validate_material_card(self, m_card_line: str) -> Dict[str, any]:
        """
        Validate M card line from MCNP input.

        Args:
            m_card_line: M card text (can be multi-line with & continuation)

        Returns:
            Dictionary with validation results
        """
        result = {
            'material_num': None,
            'zaids': [],
            'fractions': [],
            'keywords': {},
            'errors': [],
            'warnings': [],
        }

        # Extract material number
        m_match = re.match(r'^M(\d+)\s+', m_card_line, re.IGNORECASE)
        if not m_match:
            result['errors'].append("Invalid M card format (no material number found)")
            return result

        result['material_num'] = int(m_match.group(1))

        # Remove comment
        if '$' in m_card_line:
            m_card_line = m_card_line.split('$')[0]

        # Parse tokens
        tokens = m_card_line[m_match.end():].split()

        i = 0
        fraction_sign = None
        while i < len(tokens):
            token = tokens[i]

            # Check for keywords
            if '=' in token or token.upper() in ['NLIB', 'PLIB', 'ELIB', 'GAS', 'ESTEP', 'HSTEP']:
                if '=' in token:
                    key, val = token.split('=', 1)
                    result['keywords'][key.upper()] = val
                else:
                    # Next token is value
                    if i + 1 < len(tokens):
                        result['keywords'][token.upper()] = tokens[i + 1]
                        i += 1
                i += 1
                continue

            # Check for ZAID
            if i + 1 < len(tokens):
                zaid = token
                try:
                    fraction = float(tokens[i + 1])

                    result['zaids'].append(zaid)
                    result['fractions'].append(fraction)

                    # Check fraction sign consistency
                    if fraction_sign is None:
                        fraction_sign = "atomic" if fraction > 0 else "weight"
                    else:
                        current_sign = "atomic" if fraction > 0 else "weight"
                        if current_sign != fraction_sign:
                            result['errors'].append(
                                f"Mixed fraction types: {fraction_sign} and {current_sign}"
                            )

                    # Validate ZAID format
                    valid, msg = self.validate_zaid_format(zaid)
                    if not valid:
                        result['errors'].append(f"ZAID '{zaid}': {msg}")

                    # Check availability
                    if self.available_zaids:
                        avail, msg = self.check_availability(zaid)
                        if not avail:
                            result['warnings'].append(f"ZAID '{zaid}': {msg}")

                    i += 2
                except ValueError:
                    result['errors'].append(f"Expected fraction after ZAID '{zaid}'")
                    i += 1
            else:
                result['errors'].append(f"ZAID '{token}' missing fraction")
                i += 1

        # Check fraction sum for weight fractions
        if fraction_sign == "weight":
            total = sum(result['fractions'])
            if abs(total + 1.0) > 0.01:
                result['warnings'].append(
                    f"Weight fractions sum to {total:.4f} (should be -1.0)"
                )

        return result


def validate_input_file(input_file: str) -> Dict[str, List]:
    """
    Validate all M cards in MCNP input file.

    Args:
        input_file: Path to MCNP input file

    Returns:
        Dictionary with validation results for all materials
    """
    validator = ZAIDValidator()
    results = {'materials': [], 'summary': {'errors': 0, 'warnings': 0}}

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Find M cards (can span multiple lines with &)
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.upper().startswith('M') and not line.upper().startswith('MODE'):
            # Collect continuation lines
            m_card = line
            while m_card.rstrip().endswith('&'):
                i += 1
                if i < len(lines):
                    m_card = m_card.rstrip('&\n') + ' ' + lines[i].strip()
                else:
                    break

            # Validate
            result = validator.validate_material_card(m_card)
            results['materials'].append(result)

            if result['errors']:
                results['summary']['errors'] += len(result['errors'])
            if result['warnings']:
                results['summary']['warnings'] += len(result['warnings'])

        i += 1

    return results


def print_validation_results(results: Dict):
    """Print validation results in readable format."""
    print("=" * 70)
    print("MCNP Material Card Validation Results")
    print("=" * 70)
    print()

    for mat_result in results['materials']:
        mat_num = mat_result['material_num']
        print(f"Material {mat_num}:")
        print(f"  ZAIDs: {', '.join(mat_result['zaids'])}")
        print(f"  Fractions: {', '.join(f'{f:.4g}' for f in mat_result['fractions'])}")

        if mat_result['keywords']:
            print(f"  Keywords: {mat_result['keywords']}")

        if mat_result['errors']:
            print(f"  ❌ ERRORS:")
            for err in mat_result['errors']:
                print(f"     - {err}")

        if mat_result['warnings']:
            print(f"  ⚠️  WARNINGS:")
            for warn in mat_result['warnings']:
                print(f"     - {warn}")

        if not mat_result['errors'] and not mat_result['warnings']:
            print(f"  ✅ Valid")

        print()

    print("-" * 70)
    print(f"Summary: {results['summary']['errors']} errors, {results['summary']['warnings']} warnings")
    print("=" * 70)


def interactive_mode():
    """Interactive ZAID validator."""
    validator = ZAIDValidator()

    print("=" * 70)
    print("MCNP ZAID and Library Validator (Interactive Mode)")
    print("=" * 70)
    print(f"xsdir loaded: {'Yes' if validator.available_zaids else 'No'}")
    print()

    while True:
        zaid = input("Enter ZAID to validate (or 'quit' to exit): ").strip()

        if zaid.lower() == 'quit':
            break

        # Validate format
        valid, msg = validator.validate_zaid_format(zaid)
        print(f"Format: {'✅' if valid else '❌'} {msg}")

        # Check availability
        if valid and validator.available_zaids:
            avail, msg = validator.check_availability(zaid)
            print(f"Availability: {'✅' if avail else '⚠️'} {msg}")

        print()


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print(__doc__)
        sys.exit(0)

    if sys.argv[1] == "--interactive":
        interactive_mode()
    elif sys.argv[1] == "--zaid":
        if len(sys.argv) < 3:
            print("Error: --zaid requires a ZAID argument")
            sys.exit(1)

        validator = ZAIDValidator()
        zaid = sys.argv[2]

        valid, msg = validator.validate_zaid_format(zaid)
        print(f"Format: {msg}")

        if valid and validator.available_zaids:
            avail, msg = validator.check_availability(zaid)
            print(f"Availability: {msg}")

    else:
        # Validate input file
        input_file = sys.argv[1]

        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found")
            sys.exit(1)

        results = validate_input_file(input_file)
        print_validation_results(results)

        if results['summary']['errors'] > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
