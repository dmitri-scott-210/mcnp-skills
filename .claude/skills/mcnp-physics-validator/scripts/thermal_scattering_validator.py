"""
Comprehensive Thermal Scattering Validator for MCNP
Detects missing S(α,β) cards - CRITICAL for thermal systems

Based on AGR-1 Material Card Analysis findings:
- Missing graphite MT cards cause 1000-5000 pcm reactivity errors
- Production models have been found with ~50 missing MT cards
- MCNP doesn't warn - runs without error but produces wrong results
"""

import re
from typing import Dict, List, Tuple, Optional

class ThermalScatteringValidator:
    """Validate thermal scattering (MT) cards in MCNP inputs"""

    # Temperature ranges for library selection
    GRAPHITE_TEMPS = {
        'grph.10t': (0, 400, 296, 'Room temperature (cold critical)'),
        'grph.18t': (400, 700, 600, 'HTGR operating (most common)'),
        'grph.22t': (700, 900, 800, 'High-temperature HTGR'),
        'grph.24t': (900, 1100, 1000, 'VHTR operating'),
        'grph.26t': (1100, 1400, 1200, 'VHTR accident'),
        'grph.28t': (1400, 1800, 1600, 'Severe accident'),
        'grph.30t': (1800, 3000, 2000, 'Extreme accident'),
    }

    WATER_TEMPS = {
        'lwtr.10t': (0, 310, 294, 'Room temperature'),
        'lwtr.11t': (310, 337, 325, 'PWR cold leg (~52°C)'),
        'lwtr.13t': (337, 375, 350, 'PWR average (~77°C)'),
        'lwtr.14t': (375, 450, 400, 'PWR hot leg (~127°C)'),
        'lwtr.16t': (450, 650, 500, 'Supercritical water'),
        'lwtr.20t': (650, 1000, 800, 'Steam/BWR'),
    }

    HEAVY_WATER_TEMPS = {
        'hwtr.10t': (0, 310, 294, 'Room temperature'),
        'hwtr.11t': (310, 400, 325, 'CANDU operating (~52°C)'),
    }

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self, materials: Dict, mt_cards: Dict, mode: str,
                 operating_temp: Optional[float] = None) -> Dict:
        """
        Main validation method

        Args:
            materials: {mat_id: {zaid: fraction}}
            mt_cards: {mat_id: [library1, library2, ...]}
            mode: MODE card string (e.g., 'N P')
            operating_temp: Operating temperature in Kelvin (optional)

        Returns:
            {'errors': [...], 'warnings': [...], 'info': [...]}
        """
        self.errors = []
        self.warnings = []
        self.info = []

        if 'N' not in mode.upper():
            self.info.append({
                'type': 'NO_NEUTRON_TRANSPORT',
                'message': 'MODE does not include neutrons - thermal scattering not needed'
            })
            return self._format_results()

        for mat_id, composition in materials.items():
            self._validate_material(mat_id, composition, mt_cards.get(mat_id, []),
                                   operating_temp)

        return self._format_results()

    def _validate_material(self, mat_id: str, composition: Dict,
                          mt_libs: List[str], operating_temp: Optional[float]):
        """Validate single material"""

        # Detect material type
        has_carbon = self._has_isotope(composition, ['6000', '6012', '6013'])
        has_hydrogen = self._has_isotope(composition, ['1001'])
        has_deuterium = self._has_isotope(composition, ['1002'])
        has_oxygen = self._has_isotope(composition, ['8016', '8017', '8018'])
        has_beryllium = self._has_isotope(composition, ['4009'])

        # Check graphite
        if has_carbon:
            self._check_graphite(mat_id, composition, mt_libs, operating_temp)

        # Check light water
        if has_hydrogen and has_oxygen and not has_deuterium:
            self._check_water(mat_id, mt_libs, operating_temp)

        # Check heavy water
        if has_deuterium and has_oxygen:
            self._check_heavy_water(mat_id, mt_libs, operating_temp)

        # Check beryllium
        if has_beryllium:
            self._check_beryllium(mat_id, mt_libs)

        # Check polyethylene (C + H)
        if has_carbon and has_hydrogen and not has_oxygen:
            self._check_polyethylene(mat_id, mt_libs)

    def _check_graphite(self, mat_id: str, composition: Dict, mt_libs: List[str],
                       operating_temp: Optional[float]):
        """Validate graphite thermal scattering"""

        # Check if this is fuel (contains U or Pu) - may not need MT card
        has_fuel = self._has_isotope(composition, ['92', '94'])

        has_grph = any('grph' in lib.lower() for lib in mt_libs)

        if not has_grph:
            # For fuel materials, this might be UCO kernel - make it a warning
            if has_fuel:
                self.warnings.append({
                    'material': mat_id,
                    'type': 'MISSING_GRAPHITE_THERMAL_SCATTERING_IN_FUEL',
                    'severity': 'WARNING',
                    'message': f'Material m{mat_id} contains both graphite and fuel',
                    'impact': 'If this is UCO kernel, no MT needed. If graphite matrix, MT required.',
                    'recommendation': f'Add "mt{mat_id} grph.18t" if this is graphite matrix/moderator',
                })
            else:
                self.errors.append({
                    'material': mat_id,
                    'type': 'MISSING_GRAPHITE_THERMAL_SCATTERING',
                    'severity': 'CRITICAL',
                    'message': f'Material m{mat_id} contains graphite but NO MT card with grph.XXt',
                    'impact': 'Wrong thermal neutron spectrum, reactivity error 1000-5000 pcm',
                    'fix': f'Add "mt{mat_id} grph.18t" (or appropriate temperature library)',
                    'reference': 'AGR1_Material_Card_Analysis.md - Missing graphite S(α,β)'
                })
        elif operating_temp:
            # Check if temperature is appropriate
            current_lib = [lib for lib in mt_libs if 'grph' in lib.lower()][0]
            recommended = self._select_graphite_library(operating_temp)

            if current_lib != recommended:
                self.warnings.append({
                    'material': mat_id,
                    'type': 'SUBOPTIMAL_GRAPHITE_TEMPERATURE',
                    'severity': 'WARNING',
                    'current_library': current_lib,
                    'recommended_library': recommended,
                    'operating_temp': operating_temp,
                    'message': f'Material m{mat_id} uses {current_lib} but operating temp is {operating_temp}K',
                    'recommendation': f'Consider changing to {recommended} for better accuracy'
                })

    def _check_water(self, mat_id: str, mt_libs: List[str],
                    operating_temp: Optional[float]):
        """Validate light water thermal scattering"""

        has_lwtr = any('lwtr' in lib.lower() for lib in mt_libs)

        if not has_lwtr:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_WATER_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} is light water but NO MT card with lwtr.XXt',
                'impact': 'Inaccurate thermal neutron treatment, reactivity error 500-2000 pcm',
                'fix': f'Add "mt{mat_id} lwtr.13t" (or appropriate temperature library)',
                'reference': 'Thermal scattering validation requirements'
            })
        elif operating_temp:
            current_lib = [lib for lib in mt_libs if 'lwtr' in lib.lower()][0]
            recommended = self._select_water_library(operating_temp)

            if current_lib != recommended:
                self.warnings.append({
                    'material': mat_id,
                    'type': 'SUBOPTIMAL_WATER_TEMPERATURE',
                    'severity': 'WARNING',
                    'current_library': current_lib,
                    'recommended_library': recommended,
                    'operating_temp': operating_temp,
                    'message': f'Material m{mat_id} uses {current_lib} but operating temp is {operating_temp}K'
                })

    def _check_heavy_water(self, mat_id: str, mt_libs: List[str],
                          operating_temp: Optional[float]):
        """Validate heavy water thermal scattering"""

        has_hwtr = any('hwtr' in lib.lower() for lib in mt_libs)

        if not has_hwtr:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_HEAVY_WATER_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} is heavy water but NO MT card with hwtr.XXt',
                'impact': 'Wrong D2O physics, reactivity error 800-3000 pcm',
                'fix': f'Add "mt{mat_id} hwtr.11t"'
            })

    def _check_beryllium(self, mat_id: str, mt_libs: List[str]):
        """Validate beryllium thermal scattering"""

        has_be = any('be.' in lib.lower() for lib in mt_libs)

        if not has_be:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_BERYLLIUM_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} contains beryllium but NO MT card with be.01t',
                'impact': 'Wrong reflector physics, reactivity error 200-1000 pcm',
                'fix': f'Add "mt{mat_id} be.01t"',
                'note': f'If mixed with H2O, need BOTH: mt{mat_id} lwtr.XXt be.01t'
            })

    def _check_polyethylene(self, mat_id: str, mt_libs: List[str]):
        """Validate polyethylene thermal scattering"""

        has_poly = any('poly' in lib.lower() for lib in mt_libs)

        if not has_poly:
            self.warnings.append({
                'material': mat_id,
                'type': 'MISSING_POLYETHYLENE_THERMAL_SCATTERING',
                'severity': 'WARNING',
                'message': f'Material m{mat_id} appears to be polyethylene but NO MT card with poly.XXt',
                'recommendation': f'Add "mt{mat_id} poly.10t" for better accuracy',
                'impact': 'Moderate accuracy loss in shielding calculations'
            })

    def _select_graphite_library(self, temp_K: float) -> str:
        """Select appropriate graphite library for temperature"""
        for lib, (t_min, t_max, t_nominal, desc) in self.GRAPHITE_TEMPS.items():
            if t_min <= temp_K < t_max:
                return lib
        return 'grph.30t'  # Highest available

    def _select_water_library(self, temp_K: float) -> str:
        """Select appropriate water library for temperature"""
        for lib, (t_min, t_max, t_nominal, desc) in self.WATER_TEMPS.items():
            if t_min <= temp_K < t_max:
                return lib
        return 'lwtr.20t'  # Highest available

    def _has_isotope(self, composition: Dict, zaid_patterns: List[str]) -> bool:
        """Check if material contains any of the specified ZAIDs"""
        for zaid_pattern in zaid_patterns:
            for zaid in composition.keys():
                # Extract element number from ZAID
                zaid_str = str(zaid)
                if '.' in zaid_str:
                    zaid_str = zaid_str.split('.')[0]

                if zaid_str.startswith(zaid_pattern):
                    return True
        return False

    def _format_results(self) -> Dict:
        """Format validation results"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'summary': {
                'critical_errors': len(self.errors),
                'warnings': len(self.warnings),
                'passed': len(self.errors) == 0
            }
        }


# Example usage and test cases
if __name__ == "__main__":
    validator = ThermalScatteringValidator()

    # Test 1: Missing graphite MT card (CRITICAL ERROR)
    print("=" * 60)
    print("Test 1: Missing Graphite Thermal Scattering (AGR-1 Pattern)")
    print("=" * 60)
    materials = {
        '9040': {  # Graphite spacer
            '6012.00c': 0.989,
            '6013.00c': 0.011
        }
    }
    mt_cards = {}  # NO MT CARD!

    result = validator.validate(materials, mt_cards, 'N', operating_temp=600)
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   Material: m{err['material']}")
            print(f"   Message: {err['message']}")
            print(f"   Impact: {err['impact']}")
            print(f"   Fix: {err['fix']}")

    # Test 2: Correct graphite with MT card
    print("\n" + "=" * 60)
    print("Test 2: Correct Graphite with MT Card")
    print("=" * 60)
    materials = {
        '9040': {
            '6012.00c': 0.989,
            '6013.00c': 0.011
        }
    }
    mt_cards = {'9040': ['grph.18t']}  # CORRECT!

    result = validator.validate(materials, mt_cards, 'N', operating_temp=600)
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    print(f"Passed: {result['summary']['passed']}")

    # Test 3: Wrong temperature library
    print("\n" + "=" * 60)
    print("Test 3: Suboptimal Temperature Library")
    print("=" * 60)
    materials = {
        '9040': {
            '6012.00c': 0.989,
            '6013.00c': 0.011
        }
    }
    mt_cards = {'9040': ['grph.10t']}  # Room temp for 600K reactor!

    result = validator.validate(materials, mt_cards, 'N', operating_temp=600)
    print(f"\nWarnings: {result['summary']['warnings']}")
    if result['warnings']:
        for warn in result['warnings']:
            print(f"\n⚠ {warn['type']}")
            print(f"   Current: {warn['current_library']}")
            print(f"   Recommended: {warn['recommended_library']}")
            print(f"   Operating Temp: {warn['operating_temp']}K")

    # Test 4: Mixed Be + H2O (needs BOTH)
    print("\n" + "=" * 60)
    print("Test 4: Mixed Beryllium + Water")
    print("=" * 60)
    materials = {
        '14': {
            '1001.70c': 0.01,
            '8016.70c': 0.005,
            '4009.60c': 0.98
        }
    }
    mt_cards = {'14': ['lwtr.10t']}  # Missing be.01t!

    result = validator.validate(materials, mt_cards, 'N')
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   {err['message']}")
            print(f"   Fix: {err['fix']}")
            if 'note' in err:
                print(f"   Note: {err['note']}")

    # Test 5: Missing water MT card
    print("\n" + "=" * 60)
    print("Test 5: Missing Water Thermal Scattering")
    print("=" * 60)
    materials = {
        '1': {
            '1001.70c': 2.0,
            '8016.70c': 1.0
        }
    }
    mt_cards = {}  # NO MT CARD!

    result = validator.validate(materials, mt_cards, 'N')
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   {err['message']}")
            print(f"   Fix: {err['fix']}")

    print("\n" + "=" * 60)
    print("VALIDATION TESTS COMPLETE")
    print("=" * 60)
