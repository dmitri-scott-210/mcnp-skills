"""
Test suite for Category A: Input Creation Skills (6 skills)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path to import from .claude/skills/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from new .claude/skills/ structure
from claude.skills.mcnp_input_builder.mcnp_input_generator import MCNPInputGenerator
from claude.skills.mcnp_geometry_builder.mcnp_geometry_builder import MCNPGeometryBuilder
from claude.skills.mcnp_material_builder.mcnp_material_builder import MCNPMaterialBuilder
from claude.skills.mcnp_source_builder.mcnp_source_builder import MCNPSourceBuilder
from claude.skills.mcnp_tally_builder.mcnp_tally_builder import MCNPTallyBuilder
from claude.skills.mcnp_template_generator.mcnp_template_generator import MCNPTemplateGenerator

class TestMCNPInputGenerator:
    
    def test_generate_simple_sphere(self):
        """Test generating simple sphere problem"""
        gen = MCNPInputGenerator()
        result = gen.generate_simple_problem(
            geometry_type='sphere',
            radius=5.0,
            material_z=92,
            source_energy=14.1
        )
        
        assert 'so' in result.lower()
        assert 'imp:n' in result.lower()
        assert 'sdef' in result.lower()
    
    def test_generate_slab_shield(self):
        """Test generating slab shielding problem"""
        gen = MCNPInputGenerator()
        result = gen._generate_slab_shield(
            thickness=10.0,
            material_z=82,
            source_energy=1.0
        )
        
        assert 'px' in result.lower() or 'pz' in result.lower()
        assert 'm1' in result.lower()
    
    def test_generate_criticality(self):
        """Test generating KCODE problem"""
        gen = MCNPInputGenerator()
        result = gen._generate_criticality(
            geometry_type='sphere',
            radius=8.0,
            material='u235'
        )
        
        assert 'kcode' in result.lower()
        assert 'ksrc' in result.lower()

class TestMCNPGeometryBuilder:
    
    def test_add_sphere(self):
        """Test adding sphere surface"""
        builder = MCNPGeometryBuilder()
        builder.add_sphere(1, 0, 0, 0, 5.0)
        
        result = builder.generate_input()
        assert '1 so 5.0' in result or '1 s 0 0 0 5.0' in result
    
    def test_add_cylinder(self):
        """Test adding cylinder"""
        builder = MCNPGeometryBuilder()
        builder.add_cylinder(2, 'z', 0, 0, 3.0)
        
        result = builder.generate_input()
        assert 'cz' in result.lower()
    
    def test_add_cell_with_geometry(self):
        """Test adding cell with CSG expression"""
        builder = MCNPGeometryBuilder()
        builder.add_sphere(1, 0, 0, 0, 5.0)
        builder.add_cell(10, 1, -19.1, '-1', importance_n=1)
        
        result = builder.generate_input()
        assert '10' in result
        assert '-19.1' in result
        assert 'imp:n=1' in result.lower()

class TestMCNPMaterialBuilder:
    
    def test_add_element(self):
        """Test adding natural element"""
        builder = MCNPMaterialBuilder()
        builder.add_material(1)
        builder.add_element(1, 'Fe', fraction=-7.87, fraction_type='mass')
        
        result = builder.generate_cards()
        assert 'm1' in result.lower()
        assert '26000' in result or 'fe' in result.lower()
    
    def test_add_compound(self):
        """Test adding compound (H2O)"""
        builder = MCNPMaterialBuilder()
        builder.add_material(2)
        builder.add_compound(2, 'H2O', density_g_cm3=1.0)
        
        result = builder.generate_cards()
        assert 'm2' in result.lower()
        assert '1001' in result or '1000' in result
        assert '8016' in result or '8000' in result
    
    def test_add_isotope_with_library(self):
        """Test adding specific isotope with cross-section library"""
        builder = MCNPMaterialBuilder()
        builder.add_material(3)
        builder.add_isotope(3, 92235, fraction=-1.0, library='80c')
        
        result = builder.generate_cards()
        assert '92235.80c' in result

class TestMCNPSourceBuilder:
    
    def test_point_source(self):
        """Test point source at origin"""
        builder = MCNPSourceBuilder()
        builder.set_position(0, 0, 0)
        builder.set_energy(14.1)
        
        result = builder.generate_sdef()
        assert 'sdef' in result.lower()
        assert 'pos=0 0 0' in result.lower()
        assert 'erg=14.1' in result.lower()
    
    def test_energy_distribution(self):
        """Test energy distribution"""
        builder = MCNPSourceBuilder()
        builder.set_energy_distribution([0.1, 1.0, 10.0], [0.0, 0.5, 1.0])
        
        result = builder.generate_sdef()
        assert 'si' in result.lower()
        assert 'sp' in result.lower()
    
    def test_criticality_source(self):
        """Test KCODE source"""
        builder = MCNPSourceBuilder()
        result = builder.generate_criticality_source(
            n_per_cycle=1000,
            n_skip=30,
            n_total=130
        )
        
        assert 'kcode' in result.lower()
        assert '1000' in result
        assert '30' in result

class TestMCNPTallyBuilder:
    
    def test_surface_current(self):
        """Test F1 surface current tally"""
        builder = MCNPTallyBuilder()
        builder.add_surface_current([1, 2], particle='n')
        
        result = builder.generate_tallies()
        assert 'f1:n' in result.lower()
    
    def test_cell_flux(self):
        """Test F4 cell flux tally"""
        builder = MCNPTallyBuilder()
        builder.add_cell_flux([10, 20], particle='n')
        
        result = builder.generate_tallies()
        assert 'f4:n' in result.lower()
    
    def test_energy_bins(self):
        """Test adding energy bins"""
        builder = MCNPTallyBuilder()
        builder.add_surface_current([1], particle='n')
        builder.add_energy_bins(1, [0.01, 0.1, 1.0, 10.0])
        
        result = builder.generate_tallies()
        assert 'e1' in result.lower()
        assert '0.01' in result

class TestMCNPTemplateGenerator:
    
    def test_reactor_unit_cell(self):
        """Test reactor unit cell template"""
        result = MCNPTemplateGenerator.reactor_unit_cell(
            fuel_radius=0.4,
            clad_thickness=0.05,
            pitch=1.26
        )
        
        assert 'lat=1' in result.lower()
        assert 'cz' in result.lower()
    
    def test_dosimetry_sphere(self):
        """Test dosimetry sphere template"""
        result = MCNPTemplateGenerator.dosimetry_sphere(
            radius=30.0,
            source_energy=14.1
        )
        
        assert 'so' in result.lower()
        assert 'sdef' in result.lower()
        assert 'f4' in result.lower() or 'f2' in result.lower()
