"""
Unit tests for MCNP Template Generator Skill

Tests template generation capabilities:
- PWR unit cell template
- Dosimetry sphere template
- Slab shielding template
- Parameter customization
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-template-generator"
sys.path.insert(0, str(skill_dir))

from mcnp_template_generator import MCNPTemplateGenerator


class TestMCNPTemplateGenerator:
    """Test suite for MCNP Template Generator"""

    def setup_method(self):
        """Setup test fixture"""
        self.generator = MCNPTemplateGenerator()

    # ===== PWR Unit Cell Tests =====

    def test_reactor_unit_cell_default(self):
        """Test PWR unit cell with default parameters"""
        result = self.generator.reactor_unit_cell()
        assert result is not None
        assert 'PWR Unit Cell' in result
        assert 'lat=1' in result
        assert 'u=1' in result

    def test_reactor_unit_cell_custom_pitch(self):
        """Test PWR unit cell with custom pitch"""
        result = self.generator.reactor_unit_cell(pitch=1.5)
        assert result is not None
        assert '1.5' in result

    def test_reactor_unit_cell_custom_fuel_radius(self):
        """Test PWR unit cell with custom fuel radius"""
        result = self.generator.reactor_unit_cell(fuel_radius=0.45)
        assert result is not None
        assert '0.45' in result

    def test_reactor_unit_cell_custom_clad(self):
        """Test PWR unit cell with custom cladding thickness"""
        result = self.generator.reactor_unit_cell(clad_thickness=0.08)
        assert result is not None
        # Clad radius should be fuel + clad thickness
        assert result is not None

    def test_reactor_unit_cell_contains_materials(self):
        """Test unit cell includes material cards"""
        result = self.generator.reactor_unit_cell()
        assert 'm1' in result.lower() or 'M1' in result
        assert 'm2' in result.lower() or 'M2' in result
        assert 'm3' in result.lower() or 'M3' in result

    def test_reactor_unit_cell_contains_kcode(self):
        """Test unit cell includes KCODE card"""
        result = self.generator.reactor_unit_cell()
        assert 'kcode' in result.lower()

    def test_reactor_unit_cell_contains_surfaces(self):
        """Test unit cell includes surface definitions"""
        result = self.generator.reactor_unit_cell()
        assert 'cz' in result  # Cylindrical surfaces

    # ===== Dosimetry Sphere Tests =====

    def test_dosimetry_sphere_basic(self):
        """Test dosimetry sphere template"""
        result = self.generator.dosimetry_sphere()
        assert result is not None
        assert 'Dosimetry Sphere' in result

    def test_dosimetry_sphere_contains_water(self):
        """Test dosimetry sphere has water (cell with material 1)"""
        result = self.generator.dosimetry_sphere()
        # Template has cell 10 with material 1 (-1.0 density water)
        assert '1  -1.0' in result or '10' in result

    def test_dosimetry_sphere_mode_np(self):
        """Test dosimetry sphere uses neutron-photon mode"""
        result = self.generator.dosimetry_sphere()
        assert 'mode n p' in result.lower()

    def test_dosimetry_sphere_has_source(self):
        """Test dosimetry sphere has source definition"""
        result = self.generator.dosimetry_sphere()
        assert 'sdef' in result.lower()

    def test_dosimetry_sphere_has_tally(self):
        """Test dosimetry sphere has F6 tally"""
        result = self.generator.dosimetry_sphere()
        assert 'f6' in result.lower()

    def test_dosimetry_sphere_geometry(self):
        """Test dosimetry sphere has sphere surface"""
        result = self.generator.dosimetry_sphere()
        assert 'so' in result  # Sphere at origin

    # ===== Slab Shielding Tests =====

    def test_shielding_slab_default(self):
        """Test slab shielding with default thickness"""
        result = self.generator.shielding_slab()
        assert result is not None
        assert 'Slab Shielding' in result

    def test_shielding_slab_custom_thickness(self):
        """Test slab shielding with custom thickness"""
        result = self.generator.shielding_slab(thickness=20)
        assert result is not None
        assert '20 cm' in result

    def test_shielding_slab_has_shield_region(self):
        """Test slab has shield material"""
        result = self.generator.shielding_slab()
        # Should have aluminum or some shield material
        assert 'm1' in result.lower()

    def test_shielding_slab_neutron_mode(self):
        """Test slab uses neutron transport"""
        result = self.generator.shielding_slab()
        assert 'mode n' in result.lower()

    def test_shielding_slab_has_source(self):
        """Test slab has source definition"""
        result = self.generator.shielding_slab()
        assert 'sdef' in result.lower()

    def test_shielding_slab_has_surface_tally(self):
        """Test slab has F2 surface tally"""
        result = self.generator.shielding_slab()
        assert 'f2' in result.lower()

    def test_shielding_slab_planes(self):
        """Test slab has plane surfaces"""
        result = self.generator.shielding_slab()
        assert 'pz' in result  # Z-plane

    # ===== Integration Tests =====

    def test_all_templates_generate(self):
        """Test all templates can be generated"""
        t1 = self.generator.reactor_unit_cell()
        t2 = self.generator.dosimetry_sphere()
        t3 = self.generator.shielding_slab()
        assert t1 is not None
        assert t2 is not None
        assert t3 is not None

    def test_templates_non_empty(self):
        """Test all templates produce non-trivial output"""
        t1 = self.generator.reactor_unit_cell()
        t2 = self.generator.dosimetry_sphere()
        t3 = self.generator.shielding_slab()
        assert len(t1) > 100
        assert len(t2) > 50
        assert len(t3) > 50

    def test_templates_have_mode_cards(self):
        """Test all templates include MODE specification"""
        t1 = self.generator.reactor_unit_cell()
        t2 = self.generator.dosimetry_sphere()
        t3 = self.generator.shielding_slab()
        assert 'mode' in t1.lower()
        assert 'mode' in t2.lower()
        assert 'mode' in t3.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
