"""
MCNP6 Unit Conversions
Handle conversions between different unit systems for MCNP calculations
"""

from typing import Dict, Optional
from enum import Enum


class LengthUnit(Enum):
    CM = "cm"
    MM = "mm"
    M = "m"
    INCH = "inch"
    FOOT = "foot"


class EnergyUnit(Enum):
    MEV = "MeV"
    EV = "eV"
    KEV = "keV"
    GEV = "GeV"
    JOULE = "J"


class DensityUnit(Enum):
    G_CM3 = "g/cm³"
    KG_M3 = "kg/m³"
    LBM_FT3 = "lbm/ft³"
    ATOMS_B_CM = "atoms/b-cm"


class ActivityUnit(Enum):
    CURIE = "Ci"
    BECQUEREL = "Bq"
    MILLICURIE = "mCi"
    MICROCURIE = "µCi"


class DoseUnit(Enum):
    REM = "rem"
    SIEVERT = "Sv"
    MILLIREM = "mrem"
    MILLISIEVERT = "mSv"
    GRAY = "Gy"
    RAD = "rad"


class UnitConverter:
    """
    Comprehensive unit conversion for MCNP calculations
    """
    
    # Physical constants
    AVOGADRO = 6.02214076e23  # particles/mol
    C_LIGHT = 2.99792458e10    # cm/s
    EV_TO_JOULE = 1.602176634e-19
    BARN = 1e-24               # cm²
    
    # Conversion factors to MCNP default units
    LENGTH_TO_CM = {
        LengthUnit.CM: 1.0,
        LengthUnit.MM: 0.1,
        LengthUnit.M: 100.0,
        LengthUnit.INCH: 2.54,
        LengthUnit.FOOT: 30.48
    }
    
    ENERGY_TO_MEV = {
        EnergyUnit.MEV: 1.0,
        EnergyUnit.EV: 1e-6,
        EnergyUnit.KEV: 1e-3,
        EnergyUnit.GEV: 1e3,
        EnergyUnit.JOULE: 1.0 / (1.602176634e-13)  # J to MeV
    }
    
    ACTIVITY_TO_CURIE = {
        ActivityUnit.CURIE: 1.0,
        ActivityUnit.BECQUEREL: 1.0 / 3.7e10,
        ActivityUnit.MILLICURIE: 1e-3,
        ActivityUnit.MICROCURIE: 1e-6
    }
    
    DOSE_CONVERSION = {
        DoseUnit.REM: 1.0,
        DoseUnit.SIEVERT: 100.0,      # 1 Sv = 100 rem
        DoseUnit.MILLIREM: 1e-3,
        DoseUnit.MILLISIEVERT: 0.1,   # 1 mSv = 0.1 rem
        DoseUnit.GRAY: 100.0,         # 1 Gy = 100 rad
        DoseUnit.RAD: 1.0
    }
    
    @classmethod
    def convert_length(cls, value: float, from_unit: LengthUnit, to_unit: LengthUnit) -> float:
        """Convert length between units"""
        cm_value = value * cls.LENGTH_TO_CM[from_unit]
        return cm_value / cls.LENGTH_TO_CM[to_unit]
    
    @classmethod
    def convert_energy(cls, value: float, from_unit: EnergyUnit, to_unit: EnergyUnit) -> float:
        """Convert energy between units"""
        mev_value = value * cls.ENERGY_TO_MEV[from_unit]
        return mev_value / cls.ENERGY_TO_MEV[to_unit]
    
    @classmethod
    def convert_activity(cls, value: float, from_unit: ActivityUnit, to_unit: ActivityUnit) -> float:
        """Convert activity between units"""
        ci_value = value * cls.ACTIVITY_TO_CURIE[from_unit]
        return ci_value / cls.ACTIVITY_TO_CURIE[to_unit]
    
    @classmethod
    def convert_dose(cls, value: float, from_unit: DoseUnit, to_unit: DoseUnit) -> float:
        """Convert dose between units"""
        rem_value = value * cls.DOSE_CONVERSION[from_unit]
        return rem_value / cls.DOSE_CONVERSION[to_unit]
    
    @classmethod
    def density_g_cm3_to_atoms_b_cm(cls, density_g_cm3: float, atomic_weight: float) -> float:
        """
        Convert density from g/cm³ to atoms/b-cm
        
        Args:
            density_g_cm3: Density in g/cm³
            atomic_weight: Atomic or molecular weight in g/mol
        
        Returns:
            Density in atoms/b-cm (negative value for MCNP)
        """
        atoms_per_cm3 = (density_g_cm3 * cls.AVOGADRO) / atomic_weight
        atoms_per_b_cm = atoms_per_cm3 * cls.BARN
        return atoms_per_b_cm
    
    @classmethod
    def atoms_b_cm_to_density_g_cm3(cls, atoms_b_cm: float, atomic_weight: float) -> float:
        """
        Convert density from atoms/b-cm to g/cm³
        
        Args:
            atoms_b_cm: Atomic density in atoms/b-cm
            atomic_weight: Atomic or molecular weight in g/mol
        
        Returns:
            Density in g/cm³
        """
        atoms_per_cm3 = atoms_b_cm / cls.BARN
        density_g_cm3 = (atoms_per_cm3 * atomic_weight) / cls.AVOGADRO
        return density_g_cm3
    
    @classmethod
    def temperature_to_energy(cls, temp_kelvin: float) -> float:
        """
        Convert temperature to energy (kT) in MeV
        Boltzmann constant k = 8.617333e-5 eV/K
        
        Args:
            temp_kelvin: Temperature in Kelvin
        
        Returns:
            Energy in MeV
        """
        k_boltzmann_ev = 8.617333e-5  # eV/K
        energy_ev = k_boltzmann_ev * temp_kelvin
        return energy_ev * 1e-6  # Convert to MeV
    
    @classmethod
    def energy_to_temperature(cls, energy_mev: float) -> float:
        """
        Convert energy (MeV) to temperature (K)
        
        Args:
            energy_mev: Energy in MeV
        
        Returns:
            Temperature in Kelvin
        """
        k_boltzmann_ev = 8.617333e-5  # eV/K
        energy_ev = energy_mev * 1e6
        return energy_ev / k_boltzmann_ev
    
    @classmethod
    def barn_to_cm2(cls, barn: float) -> float:
        """Convert barn to cm²"""
        return barn * cls.BARN
    
    @classmethod
    def cm2_to_barn(cls, cm2: float) -> float:
        """Convert cm² to barn"""
        return cm2 / cls.BARN
    
    @classmethod
    def mev_to_wavelength_cm(cls, energy_mev: float) -> float:
        """
        Convert photon energy to wavelength
        λ = hc/E
        """
        h_planck = 4.135667696e-21  # MeV·s
        wavelength_cm = (h_planck * cls.C_LIGHT) / energy_mev
        return wavelength_cm
    
    @classmethod
    def wavelength_cm_to_mev(cls, wavelength_cm: float) -> float:
        """Convert wavelength to photon energy"""
        h_planck = 4.135667696e-21  # MeV·s
        energy_mev = (h_planck * cls.C_LIGHT) / wavelength_cm
        return energy_mev
    
    @classmethod
    def flux_to_dose_rate(cls, flux: float, dose_conversion_factor: float) -> float:
        """
        Convert particle flux to dose rate
        
        Args:
            flux: Particle flux (particles/cm²/s)
            dose_conversion_factor: Dose conversion factor (rem·cm²)
        
        Returns:
            Dose rate (rem/hr)
        """
        dose_rate_rem_s = flux * dose_conversion_factor
        dose_rate_rem_hr = dose_rate_rem_s * 3600
        return dose_rate_rem_hr
    
    @classmethod
    def print_conversion_table(cls):
        """Print a quick reference table of common conversions"""
        print("=" * 60)
        print("MCNP Unit Conversion Quick Reference")
        print("=" * 60)
        
        print("\nLength conversions to cm:")
        for unit, factor in cls.LENGTH_TO_CM.items():
            print(f"  1 {unit.value:6s} = {factor:10.4f} cm")
        
        print("\nEnergy conversions to MeV:")
        for unit, factor in cls.ENERGY_TO_MEV.items():
            print(f"  1 {unit.value:6s} = {factor:10.6e} MeV")
        
        print("\nPhysical constants:")
        print(f"  Avogadro's number: {cls.AVOGADRO:.6e} particles/mol")
        print(f"  1 barn = {cls.BARN:.6e} cm²")
        print(f"  c (light speed) = {cls.C_LIGHT:.6e} cm/s")
        
        print("\nExample density conversion (water at 1 g/cm³, MW=18):")
        atoms_b_cm = cls.density_g_cm3_to_atoms_b_cm(1.0, 18.0)
        print(f"  1.0 g/cm³ = {atoms_b_cm:.6e} atoms/b-cm")
        print(f"  MCNP density input: -{atoms_b_cm:.6e}")
        
        print("=" * 60)


if __name__ == "__main__":
    # Test conversions
    uc = UnitConverter()
    
    # Test length
    inches = uc.convert_length(10.0, LengthUnit.CM, LengthUnit.INCH)
    print(f"10 cm = {inches:.3f} inches")
    
    # Test energy
    kev = uc.convert_energy(14.1, EnergyUnit.MEV, EnergyUnit.KEV)
    print(f"14.1 MeV = {kev:.1f} keV")
    
    # Test density
    aluminum_atoms_b_cm = uc.density_g_cm3_to_atoms_b_cm(2.7, 26.982)
    print(f"Aluminum 2.7 g/cm³ = {aluminum_atoms_b_cm:.6e} atoms/b-cm")
    
    # Print reference table
    print()
    uc.print_conversion_table()
