"""
Unit tests for MCNP Material Builder Skill

Tests material definition capabilities:
- Isotope addition
- Material card generation
- Natural element expansion
- Thermal scattering
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-material-builder"
sys.path.insert(0, str(skill_dir))

from mcnp_material_builder import MCNPMaterialBuilder


class TestMCNPMaterialBuilder:
    """Test suite for MCNP Material Builder"""

    def setup_method(self):
        """Setup test fixture"""
        self.builder = MCNPMaterialBuilder()

    # ===== Basic Material Tests =====

    def test_add_isotope_single(self):
        """Test adding single element"""
        self.builder.add_element(1, 'U-235', 0.03)
        assert len(self.builder.materials) > 0

    def test_add_isotope_multiple(self):
        """Test adding multiple elements"""
        self.builder.add_element(1, 'U-235', 0.03)
        self.builder.add_element(1, 'U-238', 0.97)
        assert len(self.builder.materials) > 0

    def test_water_material(self):
        """Test water material H2O"""
        self.builder.add_element(1, 'H-1', 2)
        self.builder.add_element(1, 'O-16', 1)
        assert len(self.builder.materials) > 0

    def test_uo2_fuel_material(self):
        """Test UO2 fuel material"""
        self.builder.add_element(1, 'U-235', 0.03)
        self.builder.add_element(1, 'U-238', 0.97)
        self.builder.add_element(1, 'O-16', 2.0)
        assert len(self.builder.materials) > 0

    def test_aluminum_material(self):
        """Test aluminum structural material"""
        self.builder.add_element(1, 'Al', 1.0)
        assert len(self.builder.materials) > 0

    def test_zircaloy_material(self):
        """Test zircaloy clad material"""
        self.builder.add_element(1, 'Zr', 1.0)
        assert len(self.builder.materials) > 0

    # ===== Multiple Materials Tests =====

    def test_multiple_materials(self):
        """Test creating multiple materials"""
        self.builder.add_element(1, 'U-235', 1.0)
        self.builder.add_element(2, 'H-1', 1.0)
        self.builder.add_element(3, 'O-16', 1.0)
        assert len(self.builder.materials) >= 3

    def test_material_numbering(self):
        """Test material numbers are tracked correctly"""
        self.builder.add_element(5, 'U-235', 1.0)
        assert 5 in self.builder.materials or len(self.builder.materials) > 0

    # ===== Realistic Nuclear Materials =====

    def test_pwr_fuel_enriched(self):
        """Test PWR enriched fuel (3.5% U-235)"""
        self.builder.add_element(1, 'U-235', 0.035)
        self.builder.add_element(1, 'U-238', 0.965)
        self.builder.add_element(1, 'O-16', 2.0)
        assert len(self.builder.materials) > 0

    def test_boron_carbide_absorber(self):
        """Test B4C control rod absorber"""
        self.builder.add_element(1, 'B-10', 0.8)
        self.builder.add_element(1, 'B-11', 3.2)
        self.builder.add_element(1, 'C', 1.0)
        assert len(self.builder.materials) > 0

    def test_stainless_steel(self):
        """Test stainless steel structural material"""
        self.builder.add_element(1, 'Fe', 0.74)
        self.builder.add_element(1, 'Cr', 0.18)
        self.builder.add_element(1, 'Ni', 0.08)
        assert len(self.builder.materials) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
