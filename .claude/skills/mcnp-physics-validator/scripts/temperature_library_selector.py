"""
MCNP Temperature-Dependent S(α,β) Library Selector

Helps select appropriate thermal scattering libraries based on operating temperature.
Critical for accurate thermal neutron physics in reactors.

Temperature mismatch can cause:
- Wrong thermal neutron spectrum
- Incorrect reactivity calculations
- Benchmark validation failures
"""

from typing import Tuple, Dict, List

class TemperatureLibrarySelector:
    """Select appropriate thermal scattering libraries for operating temperatures"""

    # Graphite library temperature ranges (K)
    GRAPHITE_LIBRARIES = {
        'grph.10t': {
            'temp_nominal': 296,
            'temp_min': 0,
            'temp_max': 400,
            'celsius': 23,
            'description': 'Room temperature (cold critical)',
            'applications': ['Cold critical experiments', 'Zero-power tests', 'Room temperature benchmarks']
        },
        'grph.18t': {
            'temp_nominal': 600,
            'temp_min': 400,
            'temp_max': 700,
            'celsius': 327,
            'description': 'HTGR operating (most common)',
            'applications': ['HTGR operating conditions', 'Fast reactor reflectors', 'Standard operating temp']
        },
        'grph.22t': {
            'temp_nominal': 800,
            'temp_min': 700,
            'temp_max': 900,
            'celsius': 527,
            'description': 'High-temperature HTGR',
            'applications': ['High-temp HTGR designs', 'Advanced gas reactors']
        },
        'grph.24t': {
            'temp_nominal': 1000,
            'temp_min': 900,
            'temp_max': 1100,
            'celsius': 727,
            'description': 'VHTR operating',
            'applications': ['Very High Temperature Reactors', 'VHTR operating conditions']
        },
        'grph.26t': {
            'temp_nominal': 1200,
            'temp_min': 1100,
            'temp_max': 1400,
            'celsius': 927,
            'description': 'VHTR accident',
            'applications': ['VHTR accident scenarios', 'High-temperature transients']
        },
        'grph.28t': {
            'temp_nominal': 1600,
            'temp_min': 1400,
            'temp_max': 1800,
            'celsius': 1327,
            'description': 'Severe accident',
            'applications': ['Severe accident analysis', 'Core melt scenarios']
        },
        'grph.30t': {
            'temp_nominal': 2000,
            'temp_min': 1800,
            'temp_max': 3000,
            'celsius': 1727,
            'description': 'Extreme accident',
            'applications': ['Extreme accident conditions', 'Maximum credible temperatures']
        },
    }

    # Water library temperature ranges
    WATER_LIBRARIES = {
        'lwtr.10t': {
            'temp_nominal': 294,
            'temp_min': 0,
            'temp_max': 310,
            'celsius': 21,
            'description': 'Room temperature',
            'applications': ['Cold critical', 'Research reactor pools', 'Room temp experiments']
        },
        'lwtr.11t': {
            'temp_nominal': 325,
            'temp_min': 310,
            'temp_max': 337,
            'celsius': 52,
            'description': 'PWR cold leg (~52°C)',
            'applications': ['PWR cold leg', 'Common PWR operating']
        },
        'lwtr.13t': {
            'temp_nominal': 350,
            'temp_min': 337,
            'temp_max': 375,
            'celsius': 77,
            'description': 'PWR average (~77°C)',
            'applications': ['PWR average temperature', 'Most common PWR library']
        },
        'lwtr.14t': {
            'temp_nominal': 400,
            'temp_min': 375,
            'temp_max': 450,
            'celsius': 127,
            'description': 'PWR hot leg (~127°C)',
            'applications': ['PWR hot leg', 'High-temp LWR']
        },
        'lwtr.16t': {
            'temp_nominal': 500,
            'temp_min': 450,
            'temp_max': 650,
            'celsius': 227,
            'description': 'Supercritical water',
            'applications': ['Supercritical water reactors', 'Advanced LWR']
        },
        'lwtr.20t': {
            'temp_nominal': 800,
            'temp_min': 650,
            'temp_max': 1000,
            'celsius': 527,
            'description': 'Steam/BWR',
            'applications': ['Steam conditions', 'BWR', 'High-temperature water']
        },
    }

    # Heavy water libraries
    HEAVY_WATER_LIBRARIES = {
        'hwtr.10t': {
            'temp_nominal': 294,
            'temp_min': 0,
            'temp_max': 310,
            'celsius': 21,
            'description': 'Room temperature',
            'applications': ['Cold critical', 'Zero-power CANDU']
        },
        'hwtr.11t': {
            'temp_nominal': 325,
            'temp_min': 310,
            'temp_max': 400,
            'celsius': 52,
            'description': 'CANDU operating (~52°C)',
            'applications': ['CANDU operating', 'Heavy water research reactors']
        },
    }

    # Other libraries (temperature-independent or single temperature)
    OTHER_LIBRARIES = {
        'be.01t': {
            'temp_nominal': 296,
            'material': 'Beryllium metal',
            'description': 'Beryllium reflector/moderator',
            'applications': ['Beryllium reflectors', 'Be moderators', 'Test reactors']
        },
        'poly.10t': {
            'temp_nominal': 296,
            'material': 'Polyethylene (CH₂)ₙ',
            'description': 'Polyethylene shielding',
            'applications': ['Neutron shielding', 'Neutron sources', 'Shielding calculations']
        },
    }

    def select_graphite_library(self, temperature_K: float) -> Tuple[str, Dict]:
        """
        Select appropriate graphite library for temperature

        Args:
            temperature_K: Operating temperature in Kelvin

        Returns:
            (library_name, library_info)
        """
        for lib_name, lib_info in self.GRAPHITE_LIBRARIES.items():
            if lib_info['temp_min'] <= temperature_K < lib_info['temp_max']:
                return lib_name, lib_info

        # If beyond range, return highest
        return 'grph.30t', self.GRAPHITE_LIBRARIES['grph.30t']

    def select_water_library(self, temperature_K: float) -> Tuple[str, Dict]:
        """Select appropriate light water library for temperature"""
        for lib_name, lib_info in self.WATER_LIBRARIES.items():
            if lib_info['temp_min'] <= temperature_K < lib_info['temp_max']:
                return lib_name, lib_info

        # If beyond range, return highest
        return 'lwtr.20t', self.WATER_LIBRARIES['lwtr.20t']

    def select_heavy_water_library(self, temperature_K: float) -> Tuple[str, Dict]:
        """Select appropriate heavy water library for temperature"""
        for lib_name, lib_info in self.HEAVY_WATER_LIBRARIES.items():
            if lib_info['temp_min'] <= temperature_K < lib_info['temp_max']:
                return lib_name, lib_info

        # If beyond range, return highest
        return 'hwtr.11t', self.HEAVY_WATER_LIBRARIES['hwtr.11t']

    def celsius_to_kelvin(self, celsius: float) -> float:
        """Convert Celsius to Kelvin"""
        return celsius + 273.15

    def kelvin_to_celsius(self, kelvin: float) -> float:
        """Convert Kelvin to Celsius"""
        return kelvin - 273.15

    def generate_recommendations(self, reactor_type: str, operating_temp_K: float) -> Dict:
        """
        Generate comprehensive library recommendations for reactor type

        Args:
            reactor_type: 'HTGR', 'PWR', 'BWR', 'CANDU', etc.
            operating_temp_K: Operating temperature in Kelvin

        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'reactor_type': reactor_type,
            'operating_temp_K': operating_temp_K,
            'operating_temp_C': self.kelvin_to_celsius(operating_temp_K),
            'libraries': []
        }

        if reactor_type.upper() in ['HTGR', 'VHTR', 'AGR', 'MAGNOX', 'RBMK']:
            # Graphite-moderated reactor
            lib_name, lib_info = self.select_graphite_library(operating_temp_K)
            recommendations['libraries'].append({
                'material': 'Graphite moderator/reflector',
                'library': lib_name,
                'temperature_nominal': lib_info['temp_nominal'],
                'temperature_range': f"{lib_info['temp_min']}-{lib_info['temp_max']} K",
                'description': lib_info['description'],
                'example': f"mt1 {lib_name}  $ {lib_info['description']}"
            })

        elif reactor_type.upper() in ['PWR', 'BWR', 'LWR']:
            # Light water reactor
            lib_name, lib_info = self.select_water_library(operating_temp_K)
            recommendations['libraries'].append({
                'material': 'Light water moderator',
                'library': lib_name,
                'temperature_nominal': lib_info['temp_nominal'],
                'temperature_range': f"{lib_info['temp_min']}-{lib_info['temp_max']} K",
                'description': lib_info['description'],
                'example': f"mt2 {lib_name}  $ {lib_info['description']}"
            })

        elif reactor_type.upper() in ['CANDU', 'HWR']:
            # Heavy water reactor
            lib_name, lib_info = self.select_heavy_water_library(operating_temp_K)
            recommendations['libraries'].append({
                'material': 'Heavy water moderator',
                'library': lib_name,
                'temperature_nominal': lib_info['temp_nominal'],
                'temperature_range': f"{lib_info['temp_min']}-{lib_info['temp_max']} K",
                'description': lib_info['description'],
                'example': f"mt3 {lib_name}  $ {lib_info['description']}"
            })

        return recommendations

    def print_library_table(self, material_type: str = 'all'):
        """Print formatted table of available libraries"""

        if material_type.lower() in ['graphite', 'all']:
            print("\n" + "=" * 80)
            print("GRAPHITE THERMAL SCATTERING LIBRARIES")
            print("=" * 80)
            print(f"{'Library':<12} {'Temp (K)':<10} {'Temp (°C)':<10} {'Description':<40}")
            print("-" * 80)
            for lib, info in self.GRAPHITE_LIBRARIES.items():
                print(f"{lib:<12} {info['temp_nominal']:<10} {info['celsius']:<10} {info['description']:<40}")

        if material_type.lower() in ['water', 'all']:
            print("\n" + "=" * 80)
            print("LIGHT WATER THERMAL SCATTERING LIBRARIES")
            print("=" * 80)
            print(f"{'Library':<12} {'Temp (K)':<10} {'Temp (°C)':<10} {'Description':<40}")
            print("-" * 80)
            for lib, info in self.WATER_LIBRARIES.items():
                print(f"{lib:<12} {info['temp_nominal']:<10} {info['celsius']:<10} {info['description']:<40}")

        if material_type.lower() in ['heavy_water', 'all']:
            print("\n" + "=" * 80)
            print("HEAVY WATER THERMAL SCATTERING LIBRARIES")
            print("=" * 80)
            print(f"{'Library':<12} {'Temp (K)':<10} {'Temp (°C)':<10} {'Description':<40}")
            print("-" * 80)
            for lib, info in self.HEAVY_WATER_LIBRARIES.items():
                print(f"{lib:<12} {info['temp_nominal']:<10} {info['celsius']:<10} {info['description']:<40}")


# Example usage and test cases
if __name__ == "__main__":
    selector = TemperatureLibrarySelector()

    print("=" * 80)
    print("TEMPERATURE-DEPENDENT S(α,β) LIBRARY SELECTOR")
    print("=" * 80)

    # Test 1: HTGR at 600K
    print("\nTest 1: HTGR at 600K")
    print("-" * 80)
    lib, info = selector.select_graphite_library(600)
    print(f"Recommended library: {lib}")
    print(f"Nominal temperature: {info['temp_nominal']}K ({info['celsius']}°C)")
    print(f"Description: {info['description']}")
    print(f"Applications: {', '.join(info['applications'])}")

    # Test 2: PWR at 350K
    print("\nTest 2: PWR at 350K")
    print("-" * 80)
    lib, info = selector.select_water_library(350)
    print(f"Recommended library: {lib}")
    print(f"Nominal temperature: {info['temp_nominal']}K ({info['celsius']}°C)")
    print(f"Description: {info['description']}")
    print(f"Applications: {', '.join(info['applications'])}")

    # Test 3: Complete recommendations for HTGR
    print("\nTest 3: Complete Recommendations for HTGR at 600K")
    print("-" * 80)
    recommendations = selector.generate_recommendations('HTGR', 600)
    print(f"Reactor type: {recommendations['reactor_type']}")
    print(f"Operating temperature: {recommendations['operating_temp_K']}K ({recommendations['operating_temp_C']:.1f}°C)")
    print("\nRecommended libraries:")
    for lib_rec in recommendations['libraries']:
        print(f"  • {lib_rec['material']}")
        print(f"    Library: {lib_rec['library']}")
        print(f"    Nominal temp: {lib_rec['temperature_nominal']}K")
        print(f"    Range: {lib_rec['temperature_range']}")
        print(f"    Example: {lib_rec['example']}")

    # Test 4: Display all library tables
    print("\n" + "=" * 80)
    print("ALL AVAILABLE THERMAL SCATTERING LIBRARIES")
    selector.print_library_table('all')

    # Test 5: Temperature conversion
    print("\n" + "=" * 80)
    print("TEMPERATURE CONVERSIONS")
    print("=" * 80)
    test_temps_c = [23, 300, 600, 1000]
    print(f"{'Celsius':<15} {'Kelvin':<15} {'Recommended Graphite Library':<30}")
    print("-" * 80)
    for temp_c in test_temps_c:
        temp_k = selector.celsius_to_kelvin(temp_c)
        lib, _ = selector.select_graphite_library(temp_k)
        print(f"{temp_c:<15} {temp_k:<15.1f} {lib:<30}")
