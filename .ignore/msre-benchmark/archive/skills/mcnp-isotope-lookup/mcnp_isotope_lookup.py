"""MCNP Isotope Lookup (Skill 28) - ZAID lookup and atomic data"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.zaid_database import ZAIDDatabase

class MCNPIsotopeLookup:
    def __init__(self):
        self.db = ZAIDDatabase()
    
    def lookup_zaid(self, isotope_name: str, library: str = '80c') -> str:
        zaid = self.db.isotope_to_zaid(isotope_name, library)
        return str(zaid) if zaid else None
    
    def get_atomic_weight(self, element: str) -> float:
        z = self.db.symbol_to_z(element)
        return self.db.get_atomic_weight(z, 0) if z else 0.0
    
    def expand_natural_element(self, element: str, library: str = '80c') -> list:
        z = self.db.symbol_to_z(element)
        if z:
            return self.db.expand_natural_element(z, library)
        return []
    
    def recommend_library(self, isotope: str, particle: str = 'n') -> str:
        z, a = self.db.parse_isotope_name(isotope)
        if z:
            return self.db.recommend_library(z, a, particle)
        return '80c'
