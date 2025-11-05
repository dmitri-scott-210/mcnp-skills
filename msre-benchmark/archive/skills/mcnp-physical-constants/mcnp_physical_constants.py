"""MCNP Physical Constants (Skill 30) - Nuclear constants calculator"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.unit_conversions import UnitConverter

class MCNPPhysicalConstants:
    def __init__(self):
        self.uc = UnitConverter()
    
    def get_avogadro(self) -> float:
        return self.uc.AVOGADRO
    
    def get_speed_of_light(self) -> float:
        return self.uc.C_LIGHT
    
    def barn_to_cm2(self, barn: float) -> float:
        return self.uc.barn_to_cm2(barn)
    
    def temperature_to_energy(self, temp_k: float) -> float:
        """Convert temperature to kT energy in MeV"""
        return self.uc.temperature_to_energy(temp_k)
    
    def energy_to_temperature(self, energy_mev: float) -> float:
        """Convert energy to temperature"""
        return self.uc.energy_to_temperature(energy_mev)
    
    def calculate_number_density(self, density_g_cm3: float, atomic_weight: float) -> float:
        """Calculate number density (atoms/cm3)"""
        return (density_g_cm3 * self.uc.AVOGADRO) / atomic_weight
    
    def print_constants(self):
        """Print common constants"""
        print("MCNP Physical Constants")
        print("="*50)
        print(f"Avogadro's number: {self.uc.AVOGADRO:.6e} /mol")
        print(f"Speed of light: {self.uc.C_LIGHT:.6e} cm/s")
        print(f"1 barn = {self.uc.BARN:.6e} cm²")
        print(f"Boltzmann constant: 8.617333e-5 eV/K")
