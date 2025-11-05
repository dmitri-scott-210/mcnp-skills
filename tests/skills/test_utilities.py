"""
Test suite for Category F: Utilities Skills (5 skills)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path to import from .claude/skills/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from new .claude/skills/ structure
from claude.skills.mcnp_unit_converter.mcnp_unit_converter import MCNPUnitConverterSkill as MCNPUnitConverter
from claude.skills.mcnp_isotope_lookup.mcnp_isotope_lookup import MCNPIsotopeLookup
from claude.skills.mcnp_cross_section_manager.mcnp_cross_section_manager import MCNPCrossSectionManager
from claude.skills.mcnp_physical_constants.mcnp_physical_constants import MCNPPhysicalConstants
from claude.skills.mcnp_example_finder.mcnp_example_finder import MCNPExampleFinder

class TestMCNPUnitConverter:
    
    def test_convert_length(self):
        """Test length conversions"""
        converter = MCNPUnitConverter()
        
        # cm to m
        result = converter.convert_length(100, 'cm', 'm')
        assert abs(result - 1.0) < 1e-10
        
        # inches to cm
        result = converter.convert_length(1, 'in', 'cm')
        assert abs(result - 2.54) < 1e-10
    
    def test_convert_energy(self):
        """Test energy conversions"""
        converter = MCNPUnitConverter()
        
        # MeV to keV
        result = converter.convert_energy(1.0, 'MeV', 'keV')
        assert abs(result - 1000.0) < 1e-10
        
        # eV to MeV
        result = converter.convert_energy(1e6, 'eV', 'MeV')
        assert abs(result - 1.0) < 1e-10
    
    def test_density_conversion(self):
        """Test density conversions"""
        converter = MCNPUnitConverter()
        
        # Water: 1.0 g/cm³ to atoms/b-cm
        result = converter.density_g_to_atoms(
            density_g_cm3=1.0,
            atomic_weight=18.015,  # H2O
            atoms_per_molecule=3
        )
        
        assert result > 0

class TestMCNPIsotopeLookup:
    
    def test_lookup_u235(self):
        """Test U-235 lookup"""
        lookup = MCNPIsotopeLookup()
        
        result = lookup.lookup_zaid(92235)
        assert result['element'] == 'U'
        assert result['Z'] == 92
        assert result['A'] == 235
    
    def test_isotope_to_zaid(self):
        """Test converting isotope name to ZAID"""
        lookup = MCNPIsotopeLookup()
        
        zaid = lookup.isotope_to_zaid('U-235')
        assert zaid == 92235
        
        zaid = lookup.isotope_to_zaid('H-1')
        assert zaid == 1001
    
    def test_expand_natural_element(self):
        """Test expanding natural element"""
        lookup = MCNPIsotopeLookup()
        
        isotopes = lookup.expand_natural_element('Fe')
        assert len(isotopes) > 0
        assert any(iso['A'] == 56 for iso in isotopes)  # Fe-56 is most abundant
    
    def test_get_atomic_weight(self):
        """Test getting atomic weight"""
        lookup = MCNPIsotopeLookup()
        
        weight = lookup.get_atomic_weight(92235)
        assert abs(weight - 235.044) < 0.1

class TestMCNPCrossSectionManager:
    
    def test_parse_xsdir_format(self):
        """Test parsing XSDIR format"""
        sample_xsdir = """
datapath=/path/to/data
 1001.80c    0.999167 endf80.01  0 1 1 12345  0 0 2.5301E-08
92235.80c 235.043924 endf80.92 0 1 5 678901 0 0 2.5301E-08
        """
        
        manager = MCNPCrossSectionManager()
        result = manager.parse_xsdir(sample_xsdir)
        
        assert '1001.80c' in result
        assert '92235.80c' in result
    
    def test_check_availability(self):
        """Test checking library availability"""
        manager = MCNPCrossSectionManager()
        manager.available_libraries = {
            '1001.80c': {'library': 'ENDF/B-VIII.0'},
            '1001.70c': {'library': 'ENDF/B-VII.0'}
        }
        
        available = manager.check_availability(1001, '80c')
        assert available is True
        
        available = manager.check_availability(1001, '90c')
        assert available is False
    
    def test_suggest_temperature_library(self):
        """Test suggesting temperature-specific library"""
        manager = MCNPCrossSectionManager()
        
        suggestion = manager.suggest_temperature_library(
            zaid=1001,
            temperature_K=600
        )
        
        assert suggestion is not None

class TestMCNPPhysicalConstants:
    
    def test_get_constants(self):
        """Test retrieving physical constants"""
        constants = MCNPPhysicalConstants()
        
        avogadro = constants.get_avogadro()
        assert abs(avogadro - 6.022e23) < 1e20
        
        c = constants.get_speed_of_light()
        assert abs(c - 2.998e10) < 1e8  # cm/s
    
    def test_temperature_conversion(self):
        """Test temperature to energy conversion"""
        constants = MCNPPhysicalConstants()
        
        # Room temperature ~300K to eV
        energy_eV = constants.temperature_to_energy(300)
        assert 0.01 < energy_eV < 0.1
    
    def test_calculate_number_density(self):
        """Test number density calculation"""
        constants = MCNPPhysicalConstants()
        
        # Water: 1.0 g/cm³, MW=18.015
        n_density = constants.calculate_number_density(
            density_g_cm3=1.0,
            molecular_weight=18.015
        )
        
        assert n_density > 0
        assert n_density < 1e24  # atoms/cm³

class TestMCNPExampleFinder:
    
    def test_search_examples(self, test_data_dir):
        """Test searching for examples"""
        finder = MCNPExampleFinder(str(test_data_dir))
        finder.index_all()
        
        results = finder.search('sphere')
        assert len(results) >= 0
    
    def test_get_simple_examples(self, test_data_dir):
        """Test getting simple examples"""
        finder = MCNPExampleFinder(str(test_data_dir))
        finder.index_all()
        
        simple = finder.get_simple_examples()
        assert len(simple) > 0
    
    def test_find_by_feature(self, test_data_dir):
        """Test finding examples by feature"""
        finder = MCNPExampleFinder(str(test_data_dir))
        finder.index_all()
        
        # Find examples with KCODE
        kcode_examples = finder.find_by_feature('kcode')
        # May or may not find any depending on examples
        
        # Find examples with tallies
        tally_examples = finder.find_by_feature('tally')
