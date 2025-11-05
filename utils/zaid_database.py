"""
MCNP6 ZAID Database
Isotope and nuclear data lookup utilities
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Isotope:
    """Represents an isotope"""
    z: int  # Atomic number
    a: int  # Mass number (0 for natural element)
    symbol: str
    name: str
    atomic_weight: float
    natural_abundance: float = 0.0  # Fraction (0-1)


@dataclass
class ZAID:
    """Represents an MCNP ZAID (ZZZAAA.nnX format)"""
    z: int  # Atomic number (ZZZ)
    a: int  # Mass number (AAA, 0 = natural)
    library_id: str  # Library identifier (e.g., "80c", "31c")
    
    def __str__(self):
        """Convert to ZAID string format"""
        zzzaaa = self.z * 1000 + self.a
        return f"{zzzaaa}.{self.library_id}"
    
    @classmethod
    def from_string(cls, zaid_str: str) -> 'ZAID':
        """Parse ZAID from string like '92235.80c'"""
        parts = zaid_str.split('.')
        zzzaaa = int(parts[0])
        library_id = parts[1] if len(parts) > 1 else "80c"
        
        z = zzzaaa // 1000
        a = zzzaaa % 1000
        
        return cls(z=z, a=a, library_id=library_id)


class ZAIDDatabase:
    """
    ZAID database for isotope lookup and cross-section library management
    """
    
    # Element symbols (atomic number → symbol)
    ELEMENTS = {
        1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
        9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S',
        17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr',
        25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge',
        33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr',
        41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd',
        49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba',
        57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd',
        65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf',
        73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg',
        81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra',
        89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm',
        97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm'
    }
    
    # Atomic weights (natural isotopic composition)
    ATOMIC_WEIGHTS = {
        1: 1.008, 2: 4.003, 3: 6.941, 4: 9.012, 5: 10.81, 6: 12.01, 7: 14.01, 8: 16.00,
        9: 19.00, 10: 20.18, 11: 22.99, 12: 24.31, 13: 26.98, 14: 28.09, 15: 30.97, 16: 32.07,
        17: 35.45, 18: 39.95, 19: 39.10, 20: 40.08, 21: 44.96, 22: 47.87, 23: 50.94, 24: 52.00,
        25: 54.94, 26: 55.85, 27: 58.93, 28: 58.69, 29: 63.55, 30: 65.38, 31: 69.72, 32: 72.63,
        33: 74.92, 34: 78.97, 35: 79.90, 36: 83.80, 37: 85.47, 38: 87.62, 39: 88.91, 40: 91.22,
        41: 92.91, 42: 95.95, 43: 98.0, 44: 101.1, 45: 102.9, 46: 106.4, 47: 107.9, 48: 112.4,
        49: 114.8, 50: 118.7, 51: 121.8, 52: 127.6, 53: 126.9, 54: 131.3, 55: 132.9, 56: 137.3,
        57: 138.9, 58: 140.1, 59: 140.9, 60: 144.2, 61: 145.0, 62: 150.4, 63: 152.0, 64: 157.3,
        65: 158.9, 66: 162.5, 67: 164.9, 68: 167.3, 69: 168.9, 70: 173.0, 71: 175.0, 72: 178.5,
        73: 180.9, 74: 183.8, 75: 186.2, 76: 190.2, 77: 192.2, 78: 195.1, 79: 197.0, 80: 200.6,
        81: 204.4, 82: 207.2, 83: 209.0, 84: 209.0, 85: 210.0, 86: 222.0, 87: 223.0, 88: 226.0,
        89: 227.0, 90: 232.0, 91: 231.0, 92: 238.0, 93: 237.0, 94: 244.0, 95: 243.0, 96: 247.0,
        97: 247.0, 98: 251.0, 99: 252.0, 100: 257.0
    }
    
    # Temperature mapping (Kelvin) for library suffixes
    LIBRARY_TEMPERATURES = {
        # ENDF/B-VIII.0 (lib80x) - 7 temperatures
        '00c': 293.6,   # Room temperature
        '01c': 600.0,
        '02c': 900.0,
        '03c': 1200.0,
        '04c': 2500.0,
        '05c': 0.1,     # Nearly 0K
        '06c': 250.0,
        # ENDF/B-VII.1 (endf71x) - 4 temperatures
        '80c': 293.6,   # Room temperature
        '81c': 600.0,
        '82c': 900.0,
        '83c': 1200.0,
        # ENDF/B-VII.0 (endf70) - 3 temperatures
        '70c': 293.6,   # Room temperature
        '71c': 600.0,
        '72c': 900.0,
        # ENDF/B-VI (endf60) - Multiple temperatures
        '60c': 293.6,   # Room temperature
        '61c': 600.0,
        '62c': 900.0,
        '63c': 1200.0,
        '64c': 1500.0,
        '65c': 1800.0,
        '66c': 2100.0,
        # ENDF/B-V - Legacy temperatures
        '50c': 293.6,
        '51c': 600.0,
        '52c': 900.0,
        '53c': 1200.0
    }

    # Common library identifiers with descriptions
    LIBRARY_IDS = {
        # ========== ENDF/B-VIII.0 (lib80x) - Latest ==========
        '00c': 'ENDF/B-VIII.0 neutron @ 293.6K (20.5°C)',
        '01c': 'ENDF/B-VIII.0 neutron @ 600K (327°C)',
        '02c': 'ENDF/B-VIII.0 neutron @ 900K (627°C)',
        '03c': 'ENDF/B-VIII.0 neutron @ 1200K (927°C)',
        '04c': 'ENDF/B-VIII.0 neutron @ 2500K (2227°C)',
        '05c': 'ENDF/B-VIII.0 neutron @ 0.1K (-273°C)',
        '06c': 'ENDF/B-VIII.0 neutron @ 250K (-23°C)',

        # ========== ENDF/B-VII.1 (endf71x) ==========
        '80c': 'ENDF/B-VII.1 neutron @ 293.6K (20.5°C)',
        '81c': 'ENDF/B-VII.1 neutron @ 600K (327°C)',
        '82c': 'ENDF/B-VII.1 neutron @ 900K (627°C)',
        '83c': 'ENDF/B-VII.1 neutron @ 1200K (927°C)',

        # ========== ENDF/B-VII.0 (endf70) ==========
        '70c': 'ENDF/B-VII.0 neutron @ 293.6K (20.5°C)',
        '71c': 'ENDF/B-VII.0 neutron @ 600K (327°C)',
        '72c': 'ENDF/B-VII.0 neutron @ 900K (627°C)',

        # ========== ENDF/B-VI (endf60) ==========
        '60c': 'ENDF/B-VI neutron @ 293.6K (20.5°C)',
        '61c': 'ENDF/B-VI neutron @ 600K (327°C)',
        '62c': 'ENDF/B-VI neutron @ 900K (627°C)',
        '63c': 'ENDF/B-VI neutron @ 1200K (927°C)',
        '64c': 'ENDF/B-VI neutron @ 1500K (1227°C)',
        '65c': 'ENDF/B-VI neutron @ 1800K (1527°C)',
        '66c': 'ENDF/B-VI neutron @ 2100K (1827°C)',

        # ========== ENDF/B-V (Legacy) ==========
        '50c': 'ENDF/B-V neutron @ 293.6K (20.5°C)',
        '51c': 'ENDF/B-V neutron @ 600K (327°C)',
        '52c': 'ENDF/B-V neutron @ 900K (627°C)',
        '53c': 'ENDF/B-V neutron @ 1200K (927°C)',

        # ========== Thermal Scattering S(α,β) ==========
        '20t': 'ENDF/B-VII.1 S(α,β) thermal scattering',
        '21t': 'ENDF/B-VII.1 S(α,β) @ elevated temp',
        '22t': 'ENDF/B-VII.1 S(α,β) @ high temp',
        '10t': 'ENDF/B-VI S(α,β) thermal scattering',
        '11t': 'ENDF/B-VI S(α,β) @ elevated temp',
        '01t': 'Legacy S(α,β) thermal scattering',

        # ========== Photon Libraries ==========
        '04p': 'MCPLIB04 photon (ENDF/B-VI based)',
        '03p': 'MCPLIB03 photon (older)',
        '84p': 'ENDF/B-VII.1 photon',
        '80p': 'ENDF/B-VIII.0 photon',

        # ========== Electron Libraries ==========
        '03e': 'EL03 electron library',
        '01e': 'EL01 electron library (older)',

        # ========== Proton Libraries ==========
        '70h': 'ENDF70PROT proton (LA150)',
        '66h': 'LA150H proton @ 293.6K',
        '67h': 'LA150H proton @ 600K',

        # ========== Dosimetry ==========
        '30y': 'ENDF/B-VI dosimetry cross sections',
        '31y': 'ENDF/B-VI dosimetry (variant)',

        # ========== Multi-group ==========
        '30g': 'MGXSNP 30-group neutron',
        '42g': 'MGXSNP 42-group coupled n-p',

        # ========== Other Particles ==========
        '66d': 'Deuteron library',
        '66t': 'Triton library',
        '66s': 'He-3 library',
        '66a': 'Alpha particle library',
        '66g': 'Light ion library'
    }

    # Common thermal scattering materials (ZAID format uses element Z=0)
    THERMAL_SCATTERING_MATERIALS = {
        'lwtr': 'Light water H2O',
        'hwtr': 'Heavy water D2O',
        'grph': 'Graphite',
        'poly': 'Polyethylene',
        'benz': 'Benzene',
        'zrh': 'Zirconium hydride',
        'be': 'Beryllium metal',
        'beo': 'Beryllium oxide',
        'graph': 'Reactor grade graphite',
        'uO2': 'Uranium dioxide'
    }
    
    def __init__(self):
        self.available_zaids: Dict[str, List[str]] = {}  # ZAID base → list of library IDs
    
    def symbol_to_z(self, symbol: str) -> Optional[int]:
        """Convert element symbol to atomic number"""
        symbol_upper = symbol.upper()
        for z, sym in self.ELEMENTS.items():
            if sym.upper() == symbol_upper:
                return z
        return None
    
    def z_to_symbol(self, z: int) -> Optional[str]:
        """Convert atomic number to element symbol"""
        return self.ELEMENTS.get(z)
    
    def get_atomic_weight(self, z: int, a: int = 0) -> float:
        """
        Get atomic weight
        
        Args:
            z: Atomic number
            a: Mass number (0 for natural composition)
        
        Returns:
            Atomic weight in g/mol
        """
        if a == 0:
            # Natural composition
            return self.ATOMIC_WEIGHTS.get(z, 0.0)
        else:
            # Specific isotope - approximate as mass number
            return float(a)
    
    def create_zaid(self, z: int, a: int = 0, library_id: str = "80c") -> ZAID:
        """
        Create ZAID from components
        
        Args:
            z: Atomic number
            a: Mass number (0 for natural)
            library_id: Library identifier
        
        Returns:
            ZAID object
        """
        return ZAID(z=z, a=a, library_id=library_id)
    
    def parse_isotope_name(self, name: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Parse isotope name to (Z, A)
        
        Examples:
            "U-235" → (92, 235)
            "H-1" → (1, 1)
            "Al" → (13, 0)  # Natural
        
        Returns:
            (z, a) tuple or (None, None) if invalid
        """
        # Try format: Symbol-Mass (e.g., U-235, H-1)
        match = re.match(r'([A-Za-z]+)-(\d+)', name)
        if match:
            symbol = match.group(1)
            a = int(match.group(2))
            z = self.symbol_to_z(symbol)
            return (z, a)
        
        # Try just symbol (natural composition)
        z = self.symbol_to_z(name)
        if z:
            return (z, 0)
        
        return (None, None)
    
    def isotope_to_zaid(self, name: str, library_id: str = "80c") -> Optional[ZAID]:
        """
        Convert isotope name to ZAID
        
        Args:
            name: Isotope name (e.g., "U-235", "Al")
            library_id: Library identifier
        
        Returns:
            ZAID object or None if invalid
        """
        z, a = self.parse_isotope_name(name)
        if z is not None:
            return self.create_zaid(z, a, library_id)
        return None
    
    def zaid_to_name(self, zaid: ZAID) -> str:
        """Convert ZAID to human-readable name"""
        symbol = self.z_to_symbol(zaid.z)
        if not symbol:
            return f"Unknown-{zaid.z}"
        
        if zaid.a == 0:
            return symbol  # Natural composition
        else:
            return f"{symbol}-{zaid.a}"
    
    def expand_natural_element(self, z: int, library_id: str = "80c") -> List[Tuple[ZAID, float]]:
        """
        Expand natural element into isotopes with abundances
        
        This is a simplified version. Full implementation would have complete
        natural abundance data for all elements.
        
        Returns:
            List of (ZAID, abundance) tuples
        """
        # Common natural isotopic compositions (simplified)
        natural_compositions = {
            1: [(1, 0.999885), (2, 0.000115)],  # H: H-1, H-2 (deuterium)
            6: [(12, 0.9893), (13, 0.0107)],    # C: C-12, C-13
            8: [(16, 0.9976), (17, 0.0004), (18, 0.0020)],  # O: O-16, O-17, O-18
            13: [(27, 1.0)],  # Al: Al-27 (monoisotopic)
            92: [(234, 0.000054), (235, 0.00720), (238, 0.992746)]  # U: U-234, U-235, U-238
        }
        
        if z not in natural_compositions:
            # Default: use natural element (ZZZAAA = ZZZ000)
            return [(ZAID(z=z, a=0, library_id=library_id), 1.0)]
        
        result = []
        for a, abundance in natural_compositions[z]:
            zaid = ZAID(z=z, a=a, library_id=library_id)
            result.append((zaid, abundance))
        
        return result
    
    def get_library_description(self, library_id: str) -> str:
        """Get description of library identifier"""
        return self.LIBRARY_IDS.get(library_id, f"Unknown library: {library_id}")
    
    def get_library_temperature(self, library_id: str) -> Optional[float]:
        """
        Get temperature in Kelvin for a library ID

        Args:
            library_id: Library identifier (e.g., '00c', '80c')

        Returns:
            Temperature in Kelvin or None if not temperature-dependent
        """
        return self.LIBRARY_TEMPERATURES.get(library_id)

    def find_libraries_at_temperature(self, temperature_k: float, tolerance: float = 5.0,
                                      endf_version: str = 'VIII.0') -> List[str]:
        """
        Find library IDs at a specific temperature

        Args:
            temperature_k: Target temperature in Kelvin
            tolerance: Temperature tolerance in Kelvin
            endf_version: ENDF version ('VIII.0', 'VII.1', 'VII.0', 'VI')

        Returns:
            List of library IDs matching criteria
        """
        results = []

        # Determine which libraries to search based on ENDF version
        if endf_version == 'VIII.0':
            search_libs = ['00c', '01c', '02c', '03c', '04c', '05c', '06c']
        elif endf_version == 'VII.1':
            search_libs = ['80c', '81c', '82c', '83c']
        elif endf_version == 'VII.0':
            search_libs = ['70c', '71c', '72c']
        elif endf_version == 'VI':
            search_libs = ['60c', '61c', '62c', '63c', '64c', '65c', '66c']
        elif endf_version == 'V':
            search_libs = ['50c', '51c', '52c', '53c']
        else:
            search_libs = list(self.LIBRARY_TEMPERATURES.keys())

        for lib_id in search_libs:
            lib_temp = self.LIBRARY_TEMPERATURES.get(lib_id)
            if lib_temp and abs(lib_temp - temperature_k) <= tolerance:
                results.append(lib_id)

        return results

    def recommend_library(self, z: int, a: int, particle: str = 'n',
                          temperature_k: float = 293.6) -> str:
        """
        Recommend library identifier for isotope and particle type

        Args:
            z: Atomic number
            a: Mass number
            particle: Particle type ('n', 'p', 'e', 'h', etc.)
            temperature_k: Target temperature in Kelvin (default 293.6K = room temp)

        Returns:
            Recommended library ID
        """
        if particle == 'n':
            # Neutron libraries - use latest ENDF/B-VIII.0
            libs = self.find_libraries_at_temperature(temperature_k, tolerance=10.0, endf_version='VIII.0')
            if libs:
                return libs[0]
            return '00c'  # ENDF/B-VIII.0 @ 293.6K (latest, room temp)
        elif particle == 'p':
            return '04p'  # MCPLIB04 photon library
        elif particle == 'e':
            return '03e'  # EL03 electron library
        elif particle == 'h':
            return '70h'  # Proton library (LA150)
        elif particle == 'd':
            return '66d'  # Deuteron
        elif particle == 't':
            return '66t'  # Triton
        elif particle == 's':
            return '66s'  # He-3
        elif particle == 'a':
            return '66a'  # Alpha
        else:
            return '00c'  # Default to latest neutron
    
    def parse_xsdir(self, xsdir_path: str):
        """
        Parse xsdir file to find available ZAIDs
        
        Args:
            xsdir_path: Path to xsdir or xsdir_mcnp6.1 file
        """
        if not os.path.exists(xsdir_path):
            return
        
        try:
            with open(xsdir_path, 'r') as f:
                for line in f:
                    # Skip comments and headers
                    if line.startswith('#') or line.strip() == '':
                        continue
                    
                    # ZAID entries typically start with the ZAID
                    parts = line.split()
                    if parts:
                        zaid_str = parts[0]
                        # Check if it looks like a ZAID
                        if '.' in zaid_str:
                            base = zaid_str.split('.')[0]
                            lib_id = zaid_str.split('.')[1]
                            
                            if base not in self.available_zaids:
                                self.available_zaids[base] = []
                            if lib_id not in self.available_zaids[base]:
                                self.available_zaids[base].append(lib_id)
        except Exception as e:
            print(f"Error parsing xsdir: {e}")
    
    def is_zaid_available(self, zaid: ZAID) -> bool:
        """Check if ZAID is available in loaded xsdir"""
        base = str(zaid.z * 1000 + zaid.a)
        if base in self.available_zaids:
            return zaid.library_id in self.available_zaids[base]
        return False


if __name__ == "__main__":
    # Test ZAID database
    db = ZAIDDatabase()
    
    # Test 1: Symbol to Z
    print("=== Element Lookup ===")
    z = db.symbol_to_z('U')
    print(f"U → Z = {z}")
    symbol = db.z_to_symbol(92)
    print(f"Z = 92 → {symbol}")
    
    # Test 2: Parse isotope names
    print("\n=== Isotope Parsing ===")
    isotopes = ['U-235', 'H-1', 'Al', 'Pu-239']
    for iso in isotopes:
        z, a = db.parse_isotope_name(iso)
        if z:
            zaid = db.isotope_to_zaid(iso)
            print(f"{iso:10s} → Z={z:3d}, A={a:3d} → ZAID: {zaid}")
    
    # Test 3: Atomic weights
    print("\n=== Atomic Weights ===")
    print(f"Natural aluminum: {db.get_atomic_weight(13, 0):.3f} g/mol")
    print(f"U-235: {db.get_atomic_weight(92, 235):.1f} g/mol")
    
    # Test 4: Natural element expansion
    print("\n=== Natural Element Expansion ===")
    hydrogen = db.expand_natural_element(1)
    print("Hydrogen isotopes:")
    for zaid, abundance in hydrogen:
        name = db.zaid_to_name(zaid)
        print(f"  {name:8s} ({zaid}): {abundance*100:.4f}%")
    
    # Test 5: Library recommendations
    print("\n=== Library Recommendations ===")
    for particle in ['n', 'p', 'e']:
        lib = db.recommend_library(92, 235, particle)
        desc = db.get_library_description(lib)
        print(f"Particle {particle}: {lib} - {desc}")
