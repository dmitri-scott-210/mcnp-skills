"""
Unit tests for MCNP Unit Converter Skill

Tests all conversion methods in mcnp-unit-converter skill:
- Length conversions (cm, mm, m, inch)
- Energy conversions (eV, keV, MeV, GeV)
- Density conversions (g/cm³ to atoms/b-cm)
"""
import pytest
import sys
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-unit-converter"
sys.path.insert(0, str(skill_dir))

from mcnp_unit_converter import MCNPUnitConverterSkill


class TestMCNPUnitConverterSkill:
    """Test suite for MCNP Unit Converter Skill"""

    def setup_method(self):
        """Setup test fixture - create converter instance"""
        self.converter = MCNPUnitConverterSkill()

    # ===== Length Conversion Tests =====

    def test_convert_length_cm_to_m(self):
        """Test conversion from centimeters to meters"""
        result = self.converter.convert_length(100.0, 'cm', 'm')
        assert abs(result - 1.0) < 1e-10, "100 cm should equal 1 m"

    def test_convert_length_m_to_cm(self):
        """Test conversion from meters to centimeters"""
        result = self.converter.convert_length(1.0, 'm', 'cm')
        assert abs(result - 100.0) < 1e-10, "1 m should equal 100 cm"

    def test_convert_length_cm_to_mm(self):
        """Test conversion from centimeters to millimeters"""
        result = self.converter.convert_length(1.0, 'cm', 'mm')
        assert abs(result - 10.0) < 1e-10, "1 cm should equal 10 mm"

    def test_convert_length_inch_to_cm(self):
        """Test conversion from inches to centimeters"""
        result = self.converter.convert_length(1.0, 'inch', 'cm')
        assert abs(result - 2.54) < 1e-10, "1 inch should equal 2.54 cm"

    def test_convert_length_same_unit(self):
        """Test conversion when units are the same"""
        result = self.converter.convert_length(42.0, 'cm', 'cm')
        assert abs(result - 42.0) < 1e-10, "Same unit conversion should return original value"

    def test_convert_length_zero(self):
        """Test conversion of zero length"""
        result = self.converter.convert_length(0.0, 'cm', 'm')
        assert abs(result - 0.0) < 1e-10, "Zero length should convert to zero"

    def test_convert_length_negative(self):
        """Test conversion of negative length (for relative distances)"""
        result = self.converter.convert_length(-100.0, 'cm', 'm')
        assert abs(result - (-1.0)) < 1e-10, "Negative lengths should convert correctly"

    # ===== Energy Conversion Tests =====

    def test_convert_energy_eV_to_MeV(self):
        """Test conversion from eV to MeV"""
        result = self.converter.convert_energy(1e6, 'eV', 'MeV')
        assert abs(result - 1.0) < 1e-10, "1e6 eV should equal 1 MeV"

    def test_convert_energy_MeV_to_eV(self):
        """Test conversion from MeV to eV"""
        result = self.converter.convert_energy(1.0, 'MeV', 'eV')
        assert abs(result - 1e6) < 1e-3, "1 MeV should equal 1e6 eV"

    def test_convert_energy_keV_to_MeV(self):
        """Test conversion from keV to MeV"""
        result = self.converter.convert_energy(1000.0, 'keV', 'MeV')
        assert abs(result - 1.0) < 1e-10, "1000 keV should equal 1 MeV"

    def test_convert_energy_MeV_to_GeV(self):
        """Test conversion from MeV to GeV"""
        result = self.converter.convert_energy(1000.0, 'MeV', 'GeV')
        assert abs(result - 1.0) < 1e-10, "1000 MeV should equal 1 GeV"

    def test_convert_energy_thermal_neutron(self):
        """Test conversion for thermal neutron energy (0.0253 eV)"""
        result = self.converter.convert_energy(0.0253, 'eV', 'MeV')
        expected = 0.0253 / 1e6
        assert abs(result - expected) < 1e-12, "Thermal neutron energy conversion"

    def test_convert_energy_fusion_DT(self):
        """Test conversion for D-T fusion neutron (14.1 MeV)"""
        result = self.converter.convert_energy(14.1, 'MeV', 'keV')
        assert abs(result - 14100.0) < 1e-6, "D-T fusion neutron energy"

    def test_convert_energy_zero(self):
        """Test conversion of zero energy"""
        result = self.converter.convert_energy(0.0, 'eV', 'MeV')
        assert abs(result - 0.0) < 1e-10, "Zero energy should convert to zero"

    # ===== Density Conversion Tests =====

    def test_density_g_to_atoms_water(self):
        """Test density conversion for water (1 g/cm³)"""
        # Water: H2O, molecular weight = 18.015 g/mol
        result = self.converter.density_g_to_atoms(1.0, 18.015)
        expected = 0.0334  # atoms/b-cm
        assert abs(result - expected) < 0.001, "Water density conversion"

    def test_density_g_to_atoms_aluminum(self):
        """Test density conversion for aluminum (2.7 g/cm³)"""
        # Aluminum: atomic weight = 26.982 g/mol
        result = self.converter.density_g_to_atoms(2.7, 26.982)
        expected = 0.0603  # atoms/b-cm
        assert abs(result - expected) < 0.001, "Aluminum density conversion"

    def test_density_g_to_atoms_uranium(self):
        """Test density conversion for uranium metal (19.1 g/cm³)"""
        # Uranium: atomic weight = 238.03 g/mol
        result = self.converter.density_g_to_atoms(19.1, 238.03)
        expected = 0.0483  # atoms/b-cm
        assert abs(result - expected) < 0.001, "Uranium density conversion"

    def test_density_g_to_atoms_UO2_fuel(self):
        """Test density conversion for UO2 fuel (10.2 g/cm³)"""
        # UO2: molecular weight = 270.03 g/mol
        result = self.converter.density_g_to_atoms(10.2, 270.03)
        expected = 0.0227  # atoms/b-cm
        assert abs(result - expected) < 0.001, "UO2 fuel density conversion"

    def test_density_g_to_atoms_air(self):
        """Test density conversion for air at STP (0.001205 g/cm³)"""
        # Air (approximate): molecular weight ≈ 29 g/mol
        result = self.converter.density_g_to_atoms(0.001205, 29.0)
        expected = 2.5e-5  # atoms/b-cm (very dilute)
        assert abs(result - expected) < 1e-6, "Air density conversion"

    def test_density_g_to_atoms_zero(self):
        """Test density conversion for zero density (void)"""
        result = self.converter.density_g_to_atoms(0.0, 1.0)
        assert abs(result - 0.0) < 1e-10, "Zero density should convert to zero"

    # ===== Integration Tests =====

    def test_roundtrip_length_conversion(self):
        """Test round-trip length conversion (cm → m → cm)"""
        original = 123.45
        step1 = self.converter.convert_length(original, 'cm', 'm')
        step2 = self.converter.convert_length(step1, 'm', 'cm')
        assert abs(step2 - original) < 1e-10, "Round-trip conversion should preserve value"

    def test_roundtrip_energy_conversion(self):
        """Test round-trip energy conversion (MeV → eV → MeV)"""
        original = 14.1
        step1 = self.converter.convert_energy(original, 'MeV', 'eV')
        step2 = self.converter.convert_energy(step1, 'eV', 'MeV')
        assert abs(step2 - original) < 1e-6, "Round-trip conversion should preserve value"

    def test_multiple_length_conversions(self):
        """Test chain of length conversions (cm → mm → m → cm)"""
        original = 100.0  # cm
        mm = self.converter.convert_length(original, 'cm', 'mm')
        assert abs(mm - 1000.0) < 1e-10

        m = self.converter.convert_length(mm, 'mm', 'm')
        assert abs(m - 1.0) < 1e-10

        back_to_cm = self.converter.convert_length(m, 'm', 'cm')
        assert abs(back_to_cm - original) < 1e-10

    # ===== Edge Case Tests =====

    def test_invalid_length_unit(self):
        """Test error handling for invalid length unit"""
        with pytest.raises(KeyError):
            self.converter.convert_length(100.0, 'cm', 'invalid_unit')

    def test_invalid_energy_unit(self):
        """Test error handling for invalid energy unit"""
        with pytest.raises(KeyError):
            self.converter.convert_energy(1.0, 'MeV', 'invalid_unit')

    def test_density_invalid_atomic_weight(self):
        """Test density conversion with invalid (zero) atomic weight"""
        with pytest.raises(ZeroDivisionError):
            self.converter.density_g_to_atoms(1.0, 0.0)

    def test_very_large_number_conversion(self):
        """Test conversion with very large numbers"""
        large = 1e30
        result = self.converter.convert_length(large, 'cm', 'm')
        assert abs(result - (large / 100.0)) < 1e20

    def test_very_small_number_conversion(self):
        """Test conversion with very small numbers"""
        small = 1e-30
        result = self.converter.convert_length(small, 'cm', 'm')
        assert abs(result - (small / 100.0)) < 1e-40

    # ===== MCNP-Specific Application Tests =====

    def test_mcnp_unit_cell_dimensions(self):
        """Test conversion for typical PWR unit cell pitch (1.26 cm)"""
        pitch_cm = 1.26
        pitch_m = self.converter.convert_length(pitch_cm, 'cm', 'm')
        assert abs(pitch_m - 0.0126) < 1e-10, "PWR unit cell pitch conversion"

    def test_mcnp_fuel_pin_radius(self):
        """Test conversion for typical fuel pin radius (0.41 cm → mm)"""
        radius_cm = 0.41
        radius_mm = self.converter.convert_length(radius_cm, 'cm', 'mm')
        assert abs(radius_mm - 4.1) < 1e-10, "Fuel pin radius conversion"

    def test_mcnp_thermal_energy_conversion(self):
        """Test thermal energy at room temperature (293.6 K → MeV)"""
        # kT at 293.6 K ≈ 0.0253 eV
        thermal_eV = 0.0253
        thermal_MeV = self.converter.convert_energy(thermal_eV, 'eV', 'MeV')
        assert abs(thermal_MeV - 2.53e-8) < 1e-10, "Thermal energy conversion"

    def test_mcnp_fission_energy_range(self):
        """Test typical fission neutron energy range (0.1 - 10 MeV)"""
        low_MeV = 0.1
        high_MeV = 10.0

        low_eV = self.converter.convert_energy(low_MeV, 'MeV', 'eV')
        high_eV = self.converter.convert_energy(high_MeV, 'MeV', 'eV')

        assert abs(low_eV - 1e5) < 1.0
        assert abs(high_eV - 1e7) < 10.0

    # ===== Reference Method Tests =====

    def test_print_reference_no_error(self):
        """Test that print_reference method runs without errors"""
        try:
            self.converter.print_reference()
        except Exception as e:
            pytest.fail(f"print_reference() raised {type(e).__name__}: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
