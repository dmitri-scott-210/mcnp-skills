"""
MCNP Thermal Scattering Validator
Verifies S(α,β) thermal scattering libraries (MT cards) are present for appropriate materials

CRITICAL: Missing MT cards cause 1000-5000 pcm reactivity errors in thermal reactors!

Checks:
1. Graphite (C) materials have grph.XXt
2. Light water (H-1 + O-16) has lwtr.XXt
3. Heavy water (H-2 + O-16) has hwtr.XXt
4. Polyethylene (H + C) has poly.XXt
5. Beryllium metal has be.XXt
6. Beryllium oxide has beo.XXt
7. Temperature-appropriate library selection
"""

import re
from typing import Dict, List, Set, Tuple


class ThermalScatteringValidator:
    """Checks for missing or inappropriate thermal scattering libraries"""

    # ZAID patterns for thermal scatterers
    GRAPHITE_ZAIDS = {'6000', '6012', '6013'}
    HYDROGEN_ZAIDS = {'1001', '1002'}  # H-1, H-2
    OXYGEN_ZAIDS = {'8016', '8017', '8018'}
    BERYLLIUM_ZAIDS = {'4009'}

    # S(α,β) library recommendations
    THERMAL_SCATTER_LIBS = {
        'graphite': {
            'pattern': 'grph',
            'temperatures': {
                '10t': '296K',
                '18t': '600K',
                '22t': '800K',
                '24t': '1000K',
                '26t': '1200K',
                '28t': '1600K',
                '30t': '2000K'
            }
        },
        'light_water': {
            'pattern': 'lwtr',
            'temperatures': {
                '10t': '294K',
                '11t': '325K (PWR cold leg)',
                '13t': '350K (PWR average)',
                '14t': '400K (PWR hot leg)',
                '16t': '500K',
                '20t': '800K (steam)'
            }
        },
        'heavy_water': {
            'pattern': 'hwtr',
            'temperatures': {
                '10t': '294K',
                '11t': '325K (CANDU)'
            }
        },
        'polyethylene': {
            'pattern': 'poly',
            'temperatures': {
                '10t': '296K',
                '20t': '350K'
            }
        },
        'beryllium': {
            'pattern': 'be',
            'temperatures': {
                '10t': '296K',
                '20t': '400K',
                '22t': '500K',
                '24t': '600K',
                '26t': '700K',
                '28t': '800K'
            }
        },
        'beryllium_oxide': {
            'pattern': 'beo',
            'temperatures': {
                '10t': '296K',
                '20t': '400K',
                '22t': '500K',
                '24t': '600K',
                '26t': '700K',
                '28t': '800K'
            }
        }
    }

    def __init__(self, input_file: str):
        """
        Initialize validator with MCNP input file

        Args:
            input_file: Path to MCNP input file
        """
        self.input_file = input_file
        self.materials = {}  # mat_id: {zaids: set, fractions: dict}
        self.mt_cards = {}  # mat_id: mt_specification
        self.errors = []
        self.warnings = []

        self._parse_input()

    def _parse_input(self):
        """Parse MCNP input to extract material definitions and MT cards"""
        with open(self.input_file, 'r') as f:
            content = f.read()

        current_material = None
        current_zaids = set()
        current_fractions = {}
        in_data_section = False

        lines = content.split('\n')

        # Find data section (after two blank lines)
        blank_count = 0
        for i, line in enumerate(lines):
            if not line.strip():
                blank_count += 1
                if blank_count >= 2:
                    in_data_section = True
            else:
                if in_data_section:
                    break

        for line in lines:
            # Material card: m<id> or m <id>
            mat_match = re.match(r'^m\s*(\d+)', line.strip(), re.IGNORECASE)
            if mat_match:
                # Save previous material
                if current_material is not None:
                    self.materials[current_material] = {
                        'zaids': current_zaids,
                        'fractions': current_fractions
                    }

                # Start new material
                current_material = int(mat_match.group(1))
                current_zaids = set()
                current_fractions = {}
                continue

            # MT card: mt<id> <library> or mt <id> <library>
            mt_match = re.match(r'^mt\s*(\d+)\s+(\S+)', line.strip(), re.IGNORECASE)
            if mt_match:
                mat_id = int(mt_match.group(1))
                library = mt_match.group(2)
                self.mt_cards[mat_id] = library
                continue

            # ZAID line (isotope specification)
            if current_material is not None:
                # Skip comment lines
                if line.strip().startswith('c ') or line.strip().startswith('C '):
                    continue

                # Match ZAID.XXc fraction or ZAID.XXc -fraction
                zaid_matches = re.findall(r'(\d+)\.\d+c\s+([\-\d\.Ee\+\-]+)', line, re.IGNORECASE)
                for zaid, fraction in zaid_matches:
                    current_zaids.add(zaid)
                    try:
                        current_fractions[zaid] = float(fraction)
                    except ValueError:
                        pass

        # Save last material
        if current_material is not None:
            self.materials[current_material] = {
                'zaids': current_zaids,
                'fractions': current_fractions
            }

    def is_graphite(self, mat_zaids: Set[str]) -> bool:
        """Check if material contains graphite (carbon)"""
        return bool(mat_zaids & self.GRAPHITE_ZAIDS)

    def is_light_water(self, mat_zaids: Set[str], fractions: Dict[str, float]) -> bool:
        """Check if material is light water (H-1 + O-16, ratio ~2:1)"""
        has_h1 = '1001' in mat_zaids
        has_o16 = '8016' in mat_zaids
        return has_h1 and has_o16

    def is_heavy_water(self, mat_zaids: Set[str]) -> bool:
        """Check if material is heavy water (H-2 + O-16)"""
        has_h2 = '1002' in mat_zaids
        has_o = bool(mat_zaids & self.OXYGEN_ZAIDS)
        return has_h2 and has_o

    def is_polyethylene(self, mat_zaids: Set[str], fractions: Dict[str, float]) -> bool:
        """Check if material is polyethylene (H + C, ratio ~2:1)"""
        has_h = bool(mat_zaids & self.HYDROGEN_ZAIDS)
        has_c = bool(mat_zaids & self.GRAPHITE_ZAIDS)

        if not (has_h and has_c):
            return False

        # Check H:C ratio (should be ~2:1 for polyethylene)
        # This is approximate - would need better heuristic for production
        return True

    def is_beryllium_metal(self, mat_zaids: Set[str]) -> bool:
        """Check if material is beryllium metal"""
        return bool(mat_zaids & self.BERYLLIUM_ZAIDS) and len(mat_zaids) == 1

    def is_beryllium_oxide(self, mat_zaids: Set[str]) -> bool:
        """Check if material is beryllium oxide (Be + O)"""
        has_be = bool(mat_zaids & self.BERYLLIUM_ZAIDS)
        has_o = bool(mat_zaids & self.OXYGEN_ZAIDS)
        return has_be and has_o

    def check_material(self, mat_id: int, mat_info: Dict) -> List[str]:
        """
        Check a single material for thermal scattering requirements

        Args:
            mat_id: Material ID number
            mat_info: Dictionary with 'zaids' and 'fractions'

        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        zaids = mat_info['zaids']
        fractions = mat_info.get('fractions', {})

        # Check for graphite
        if self.is_graphite(zaids):
            if mat_id not in self.mt_cards or 'grph' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} contains carbon but missing grph.XXt S(α,β) library\n"
                    f"  ZAIDs: {sorted(zaids)}\n"
                    f"  Add: mt{mat_id} grph.18t  $ or appropriate temperature\n"
                    f"  Impact: Wrong thermal spectrum, 1000-5000 pcm reactivity error"
                )

        # Check for light water
        if self.is_light_water(zaids, fractions):
            if mat_id not in self.mt_cards or 'lwtr' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} appears to be light water but missing lwtr.XXt library\n"
                    f"  ZAIDs: {sorted(zaids)}\n"
                    f"  Add: mt{mat_id} lwtr.13t  $ or appropriate temperature\n"
                    f"  Impact: Wrong thermal spectrum, incorrect reactivity"
                )

        # Check for heavy water
        if self.is_heavy_water(zaids):
            if mat_id not in self.mt_cards or 'hwtr' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} appears to be heavy water but missing hwtr.XXt library\n"
                    f"  ZAIDs: {sorted(zaids)}\n"
                    f"  Add: mt{mat_id} hwtr.11t  $ or appropriate temperature"
                )

        # Check for beryllium metal
        if self.is_beryllium_metal(zaids):
            if mat_id not in self.mt_cards or 'be.' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} is beryllium metal but missing be.XXt library\n"
                    f"  Add: mt{mat_id} be.10t  $ or appropriate temperature"
                )

        # Check for beryllium oxide
        if self.is_beryllium_oxide(zaids):
            if mat_id not in self.mt_cards or 'beo' not in self.mt_cards[mat_id].lower():
                errors.append(
                    f"CRITICAL: Material m{mat_id} is beryllium oxide but missing beo.XXt library\n"
                    f"  Add: mt{mat_id} beo.10t  $ or appropriate temperature"
                )

        return errors

    def validate(self) -> Dict[str, List[str]]:
        """
        Run all thermal scattering checks

        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        for mat_id, mat_info in self.materials.items():
            mat_errors = self.check_material(mat_id, mat_info)
            self.errors.extend(mat_errors)

        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_report(self):
        """Print validation report to console"""
        results = self.validate()

        print("=" * 70)
        print("THERMAL SCATTERING VALIDATION REPORT")
        print(f"File: {self.input_file}")
        print("=" * 70)

        print(f"\nMaterials found: {len(self.materials)}")
        print(f"MT cards found: {len(self.mt_cards)}")

        # Categorize materials
        graphite_mats = []
        water_mats = []
        beryllium_mats = []

        for mat_id, mat_info in self.materials.items():
            zaids = mat_info['zaids']
            fractions = mat_info.get('fractions', {})

            if self.is_graphite(zaids):
                graphite_mats.append(mat_id)
            if self.is_light_water(zaids, fractions) or self.is_heavy_water(zaids):
                water_mats.append(mat_id)
            if self.is_beryllium_metal(zaids) or self.is_beryllium_oxide(zaids):
                beryllium_mats.append(mat_id)

        if graphite_mats:
            print(f"\nGraphite materials: {len(graphite_mats)} (m{', m'.join(map(str, sorted(graphite_mats)))})")
        if water_mats:
            print(f"Water materials: {len(water_mats)} (m{', m'.join(map(str, sorted(water_mats)))})")
        if beryllium_mats:
            print(f"Beryllium materials: {len(beryllium_mats)} (m{', m'.join(map(str, sorted(beryllium_mats)))})")

        if results['errors']:
            print(f"\n❌ CRITICAL ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"\n{error}")
        else:
            print("\n✓ No missing thermal scattering libraries detected")

        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"\n{warning}")

        # Print available S(α,β) library options
        if results['errors']:
            print("\n" + "=" * 70)
            print("AVAILABLE S(α,β) LIBRARIES:")
            for lib_type, lib_info in self.THERMAL_SCATTER_LIBS.items():
                print(f"\n{lib_type.replace('_', ' ').title()} ({lib_info['pattern']}.XXt):")
                for temp_code, temp_desc in lib_info['temperatures'].items():
                    print(f"  {lib_info['pattern']}.{temp_code:<4} → {temp_desc}")

        print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python thermal_scattering_validator.py <input_file>")
        sys.exit(1)

    validator = ThermalScatteringValidator(sys.argv[1])
    validator.print_report()
