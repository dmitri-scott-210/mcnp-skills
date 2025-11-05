"""
MCNP Unit Converter (Skill 27) - Convert between unit systems

MCNP units:
- Length: cm
- Energy: MeV
- Time: shakes (10⁻⁸ s)
- Temperature: MeV (TMP card)
- Density: g/cm³ (negative) or atoms/(b-cm)×10²⁴ (positive)
- Cross sections: barns
- Activity: Ci, Bq

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md: Units Summary
- Chapter 4: Input Description (units specification)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.unit_conversions import UnitConverter, LengthUnit, EnergyUnit, DensityUnit, ActivityUnit, DoseUnit

class MCNPUnitConverterSkill:
    def __init__(self):
        self.uc = UnitConverter()
    
    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        units = {'cm': LengthUnit.CM, 'mm': LengthUnit.MM, 'm': LengthUnit.M, 'inch': LengthUnit.INCH}
        return self.uc.convert_length(value, units[from_unit], units[to_unit])
    
    def convert_energy(self, value: float, from_unit: str, to_unit: str) -> float:
        units = {'MeV': EnergyUnit.MEV, 'eV': EnergyUnit.EV, 'keV': EnergyUnit.KEV, 'GeV': EnergyUnit.GEV}
        return self.uc.convert_energy(value, units[from_unit], units[to_unit])
    
    def density_g_to_atoms(self, density_g_cm3: float, atomic_weight: float) -> float:
        return self.uc.density_g_cm3_to_atoms_b_cm(density_g_cm3, atomic_weight)
    
    def print_reference(self):
        self.uc.print_conversion_table()
