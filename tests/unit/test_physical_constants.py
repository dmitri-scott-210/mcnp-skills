"""
Unit tests for MCNP Physical Constants Skill

Tests physical constants and conversions:
- Fundamental constants retrieval
- Unit conversions (barn to cm², etc.)
- Temperature-energy conversions
- Number density calculations
"""
import pytest
import sys
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-physical-constants"
sys.path.insert(0, str(skill_dir))

from mcnp_physical_constants import MCNPPhysicalConstants


class TestMCNPPhysicalConstants:
    """Test suite for MCNP Physical Constants"""

    def setup_method(self):
        """Setup test fixture"""
        self.constants = MCNPPhysicalConstants()

    # ===== Fundamental Constants Tests =====

    def test_get_avogadro(self):
        """Test Avogadro's number retrieval"""
        avogadro = self.constants.get_avogadro()

        assert isinstance(avogadro, float), "Should return float"
        assert avogadro > 0, "Should be positive"
        assert 6.0e23 < avogadro < 6.1e23, "Should be ~6.022e23"

    def test_get_speed_of_light(self):
        """Test speed of light retrieval"""
        c = self.constants.get_speed_of_light()

        assert isinstance(c, float), "Should return float"
        assert c > 0, "Should be positive"
        assert 2.99e10 < c < 3.00e10, "Should be ~2.998e10 cm/s"

    def test_avogadro_precision(self):
        """Test Avogadro's number has correct precision"""
        avogadro = self.constants.get_avogadro()

        # NIST value: 6.02214076e23
        assert 6.02e23 < avogadro < 6.03e23, "Should match NIST value"

    def test_speed_of_light_precision(self):
        """Test speed of light has correct precision"""
        c = self.constants.get_speed_of_light()

        # c = 2.99792458e10 cm/s
        assert 2.997e10 < c < 2.999e10, "Should match known value"

    # ===== Barn Conversion Tests =====

    def test_barn_to_cm2_single_barn(self):
        """Test conversion of 1 barn to cm²"""
        result = self.constants.barn_to_cm2(1.0)

        assert isinstance(result, float), "Should return float"
        # 1 barn = 1e-24 cm²
        assert 0.9e-24 < result < 1.1e-24, "Should be ~1e-24 cm²"

    def test_barn_to_cm2_zero(self):
        """Test conversion of zero barns"""
        result = self.constants.barn_to_cm2(0.0)

        assert result == 0.0, "Zero barns should be zero cm²"

    def test_barn_to_cm2_large_value(self):
        """Test conversion of large barn value"""
        result = self.constants.barn_to_cm2(1000.0)

        assert result > 0, "Should be positive"
        assert 0.9e-21 < result < 1.1e-21, "Should be ~1e-21 cm²"

    def test_barn_to_cm2_small_value(self):
        """Test conversion of small barn value"""
        result = self.constants.barn_to_cm2(0.001)

        assert result > 0, "Should be positive"
        assert 0.9e-27 < result < 1.1e-27, "Should be ~1e-27 cm²"

    def test_barn_to_cm2_negative(self):
        """Test conversion of negative barn value"""
        result = self.constants.barn_to_cm2(-5.0)

        # Physical meaning unclear, but should handle mathematically
        assert result < 0, "Should preserve sign"

    # ===== Temperature-Energy Conversion Tests =====

    def test_temperature_to_energy_room_temp(self):
        """Test conversion of room temperature to energy"""
        # Room temp: ~293 K
        energy = self.constants.temperature_to_energy(293.0)

        assert isinstance(energy, float), "Should return float"
        assert energy > 0, "Should be positive"
        # kT at 293 K ≈ 0.0253 eV = 2.53e-8 MeV
        assert 2.0e-8 < energy < 3.0e-8, "Should be ~2.5e-8 MeV"

    def test_temperature_to_energy_zero_kelvin(self):
        """Test conversion at absolute zero"""
        energy = self.constants.temperature_to_energy(0.0)

        assert energy == 0.0, "Zero K should give zero energy"

    def test_temperature_to_energy_high_temp(self):
        """Test conversion at high temperature"""
        # 1000 K
        energy = self.constants.temperature_to_energy(1000.0)

        assert energy > 0, "Should be positive"
        # kT at 1000 K ≈ 0.0862 eV = 8.62e-8 MeV
        assert 8.0e-8 < energy < 9.0e-8, "Should be ~8.6e-8 MeV"

    def test_energy_to_temperature_room_energy(self):
        """Test conversion of room temperature energy to T"""
        # kT at 293 K ≈ 2.53e-8 MeV
        temp = self.constants.energy_to_temperature(2.53e-8)

        assert isinstance(temp, float), "Should return float"
        assert temp > 0, "Should be positive"
        assert 280 < temp < 300, "Should be ~293 K"

    def test_energy_to_temperature_zero_energy(self):
        """Test conversion of zero energy"""
        temp = self.constants.energy_to_temperature(0.0)

        assert temp == 0.0, "Zero energy should give zero K"

    def test_energy_to_temperature_high_energy(self):
        """Test conversion of high energy"""
        # kT at 1000 K ≈ 8.62e-8 MeV
        temp = self.constants.energy_to_temperature(8.62e-8)

        assert temp > 0, "Should be positive"
        assert 980 < temp < 1020, "Should be ~1000 K"

    def test_temperature_energy_roundtrip(self):
        """Test roundtrip conversion T→E→T"""
        original_temp = 500.0
        energy = self.constants.temperature_to_energy(original_temp)
        final_temp = self.constants.energy_to_temperature(energy)

        # Should recover original temperature
        assert abs(final_temp - original_temp) < 1.0, "Roundtrip should preserve value"

    # ===== Number Density Calculation Tests =====

    def test_calculate_number_density_water(self):
        """Test number density calculation for water"""
        # Water: ρ = 1.0 g/cm³, MW = 18 g/mol
        density = self.constants.calculate_number_density(1.0, 18.0)

        assert isinstance(density, float), "Should return float"
        assert density > 0, "Should be positive"
        # N = (1.0 * 6.022e23) / 18 ≈ 3.35e22 atoms/cm³
        assert 3.0e22 < density < 3.5e22, "Water density should be ~3.35e22"

    def test_calculate_number_density_aluminum(self):
        """Test number density calculation for aluminum"""
        # Al: ρ = 2.7 g/cm³, MW = 26.982 g/mol
        density = self.constants.calculate_number_density(2.7, 26.982)

        assert density > 0, "Should be positive"
        # N ≈ 6.03e22 atoms/cm³
        assert 5.9e22 < density < 6.1e22, "Al density should be ~6.0e22"

    def test_calculate_number_density_uranium(self):
        """Test number density calculation for uranium"""
        # U metal: ρ = 19.1 g/cm³, MW = 238.03 g/mol
        density = self.constants.calculate_number_density(19.1, 238.03)

        assert density > 0, "Should be positive"
        # N ≈ 4.83e22 atoms/cm³
        assert 4.7e22 < density < 4.9e22, "U density should be ~4.8e22"

    def test_calculate_number_density_zero_density(self):
        """Test number density with zero material density"""
        density = self.constants.calculate_number_density(0.0, 1.0)

        assert density == 0.0, "Zero density should give zero number density"

    def test_calculate_number_density_air(self):
        """Test number density for low-density material (air)"""
        # Air at STP: ~0.001225 g/cm³, MW ≈ 29 g/mol
        density = self.constants.calculate_number_density(0.001225, 29.0)

        assert density > 0, "Should be positive"
        # Very low density
        assert density < 1e21, "Air should have low number density"

    def test_calculate_number_density_heavy_material(self):
        """Test number density for heavy material"""
        # Lead: ρ = 11.34 g/cm³, MW = 207.2 g/mol
        density = self.constants.calculate_number_density(11.34, 207.2)

        assert density > 0, "Should be positive"
        # N ≈ 3.3e22 atoms/cm³
        assert 3.2e22 < density < 3.4e22, "Pb density should be ~3.3e22"

    # ===== Integration Tests =====

    def test_complete_workflow_water_molecule(self):
        """Test complete workflow for water molecule analysis"""
        # Step 1: Get Avogadro's number
        avogadro = self.constants.get_avogadro()
        assert avogadro > 0, "Should get Avogadro's number"

        # Step 2: Calculate H₂O number density
        water_density = self.constants.calculate_number_density(1.0, 18.0)
        assert water_density > 0, "Should calculate water density"

        # Step 3: Convert temperature to energy
        room_temp_energy = self.constants.temperature_to_energy(293.6)
        assert room_temp_energy > 0, "Should convert temperature"

        # All operations successful
        assert True, "Complete workflow executed"

    def test_complete_workflow_cross_section(self):
        """Test complete workflow for cross-section analysis"""
        # Step 1: Get constants
        avogadro = self.constants.get_avogadro()
        c_light = self.constants.get_speed_of_light()

        # Step 2: Convert barn to cm²
        cross_section_cm2 = self.constants.barn_to_cm2(10.0)
        assert cross_section_cm2 > 0, "Should convert cross section"

        # Step 3: Calculate macroscopic cross-section
        # Σ = N * σ
        n_density = self.constants.calculate_number_density(1.0, 18.0)
        macro_xs = n_density * cross_section_cm2

        assert macro_xs > 0, "Should calculate macroscopic XS"

    # ===== Print Constants Test =====

    def test_print_constants_no_error(self):
        """Test that print_constants executes without error"""
        # Should not raise exception
        try:
            self.constants.print_constants()
            success = True
        except Exception:
            success = False

        assert success, "print_constants should execute without error"

    # ===== Edge Case Tests =====

    def test_barn_to_cm2_very_large(self):
        """Test barn conversion with very large value"""
        result = self.constants.barn_to_cm2(1e10)

        assert result > 0, "Should handle large values"

    def test_barn_to_cm2_very_small(self):
        """Test barn conversion with very small value"""
        result = self.constants.barn_to_cm2(1e-10)

        assert result > 0, "Should handle small values"

    def test_temperature_to_energy_cryogenic(self):
        """Test temperature conversion at cryogenic temperatures"""
        # Liquid nitrogen: 77 K
        energy = self.constants.temperature_to_energy(77.0)

        assert energy > 0, "Should handle cryogenic temperatures"
        # kT at 77 K ≈ 6.64e-9 MeV
        assert 6.0e-9 < energy < 7.0e-9, "Should be ~6.6e-9 MeV"

    def test_temperature_to_energy_very_high(self):
        """Test temperature conversion at very high temperature"""
        # Fusion plasma: ~10,000 K
        energy = self.constants.temperature_to_energy(10000.0)

        assert energy > 0, "Should handle high temperatures"
        # kT at 10000 K ≈ 8.62e-7 MeV
        assert 8.0e-7 < energy < 9.0e-7, "Should be ~8.6e-7 MeV"

    def test_energy_to_temperature_negative_energy(self):
        """Test temperature from negative energy (unphysical)"""
        # Should handle mathematically even if unphysical
        temp = self.constants.energy_to_temperature(-1.0e-8)

        # Depends on implementation - may return negative or error
        assert isinstance(temp, float), "Should return float"

    def test_calculate_number_density_very_light_isotope(self):
        """Test number density with very light isotope"""
        # Deuterium: MW ≈ 2 g/mol
        density = self.constants.calculate_number_density(1.0, 2.0)

        assert density > 0, "Should handle light isotopes"
        # N = (1.0 * 6.022e23) / 2 ≈ 3.01e23
        assert 2.9e23 < density < 3.1e23, "Should be ~3.0e23"

    def test_calculate_number_density_very_heavy_isotope(self):
        """Test number density with very heavy isotope"""
        # Uranium-238: MW = 238 g/mol
        density = self.constants.calculate_number_density(19.1, 238.0)

        assert density > 0, "Should handle heavy isotopes"

    # ===== Realistic Application Tests =====

    def test_thermal_neutron_energy(self):
        """Test calculation of thermal neutron energy"""
        # Thermal neutrons at 293.6 K
        thermal_energy = self.constants.temperature_to_energy(293.6)

        # 0.0253 eV = 2.53e-8 MeV
        assert 2.5e-8 < thermal_energy < 2.6e-8, "Should match thermal energy"

    def test_pwr_fuel_temperature(self):
        """Test PWR fuel operating temperature"""
        # PWR fuel centerline: ~1200 K
        energy = self.constants.temperature_to_energy(1200.0)

        assert energy > 0, "Should calculate PWR fuel energy"
        # kT at 1200 K ≈ 1.03e-7 MeV
        assert 1.0e-7 < energy < 1.1e-7, "Should be ~1.0e-7 MeV"

    def test_uo2_number_density(self):
        """Test UO₂ fuel number density calculation"""
        # UO₂: ρ = 10.2 g/cm³, MW = 270 g/mol
        density = self.constants.calculate_number_density(10.2, 270.0)

        assert density > 0, "Should calculate UO₂ density"
        # N ≈ 2.27e22 molecules/cm³
        assert 2.2e22 < density < 2.3e22, "Should be ~2.27e22"

    def test_boron_carbide_absorber(self):
        """Test B₄C absorber number density"""
        # B₄C: ρ = 2.52 g/cm³, MW = 55.26 g/mol
        density = self.constants.calculate_number_density(2.52, 55.26)

        assert density > 0, "Should calculate B₄C density"
        # N ≈ 2.75e22 molecules/cm³
        assert 2.7e22 < density < 2.8e22, "Should be ~2.75e22"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
