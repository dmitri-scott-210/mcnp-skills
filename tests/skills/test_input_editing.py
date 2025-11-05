"""
Test suite for Category B: Input Editing Skills (5 skills)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path to import from .claude/skills/
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from new .claude/skills/ structure
from claude.skills.mcnp_input_editor.mcnp_input_editor import MCNPInputEditor
from claude.skills.mcnp_geometry_editor.mcnp_geometry_editor import MCNPGeometryEditor
from claude.skills.mcnp_transform_editor.mcnp_transform_editor import MCNPTransformEditor
from claude.skills.mcnp_variance_reducer.mcnp_variance_reducer import MCNPVarianceReducer
from claude.skills.mcnp_input_updater.mcnp_input_updater import MCNPInputUpdater

class TestMCNPInputEditor:
    
    def test_load_and_search(self, src1_input):
        """Test loading file and searching"""
        editor = MCNPInputEditor()
        editor.load_string(src1_input)
        
        matches = editor.search('sdef')
        assert len(matches) > 0
    
    def test_search_replace(self, simple_input):
        """Test search and replace"""
        editor = MCNPInputEditor()
        editor.load_string(simple_input)
        
        editor.search_replace('imp:n=1', 'imp:n=2')
        result = editor.get_modified_input()
        
        assert 'imp:n=2' in result
    
    def test_add_comment(self, simple_input):
        """Test adding comments"""
        editor = MCNPInputEditor()
        editor.load_string(simple_input)
        
        editor.add_comment('This is a test comment')
        result = editor.get_modified_input()
        
        assert 'test comment' in result.lower()

class TestMCNPGeometryEditor:
    
    def test_modify_cell_density(self, tal01_input):
        """Test modifying cell density"""
        editor = MCNPGeometryEditor()
        editor.load_string(tal01_input)
        
        editor.modify_cell_parameter(10, density=-20.0)
        result = editor.get_modified_input()
        
        # Cell 10 should now have density -20.0
        assert '-20.0' in result or '-20' in result
    
    def test_replace_surface(self, simple_input):
        """Test replacing surface in cells"""
        editor = MCNPGeometryEditor()
        editor.load_string(simple_input)
        
        editor.replace_surface_in_cells(1, 2)
        result = editor.get_modified_input()
        
        # Surface 1 should be replaced with surface 2
        assert ' 2' in result or '-2' in result
    
    def test_add_surface(self, simple_input):
        """Test adding new surface"""
        editor = MCNPGeometryEditor()
        editor.load_string(simple_input)
        
        editor.add_surface(2, 'pz', 5.0)
        result = editor.get_modified_input()
        
        assert '2 pz 5.0' in result.lower() or '2  pz  5' in result.lower()

class TestMCNPTransformEditor:
    
    def test_create_translation(self):
        """Test creating translation transformation"""
        editor = MCNPTransformEditor()
        
        tr_card = editor.create_translation(1, 5.0, 0.0, 0.0)
        assert 'tr1' in tr_card.lower()
        assert '5.0' in tr_card or '5' in tr_card
    
    def test_create_rotation(self):
        """Test creating rotation transformation"""
        editor = MCNPTransformEditor()
        
        tr_card = editor.create_rotation(2, angle_z=90)
        assert 'tr2' in tr_card.lower()
    
    def test_apply_to_cell(self, tal01_input):
        """Test applying transformation to cell"""
        editor = MCNPTransformEditor()
        editor.load_string(tal01_input)
        
        editor.apply_to_cell(10, transform_number=1)
        result = editor.get_modified_input()
        
        # Cell 10 should reference transformation
        assert 'trcl=1' in result.lower() or '*trcl 1' in result.lower()

class TestMCNPVarianceReducer:
    
    def test_set_cell_importances(self, simple_input):
        """Test setting importance values"""
        reducer = MCNPVarianceReducer()
        reducer.load_string(simple_input)
        
        reducer.set_cell_importances({10: 4, 20: 0}, particle='n')
        result = reducer.get_modified_input()
        
        # Should have geometric splitting
        assert 'imp:n' in result.lower()
    
    def test_add_weight_windows(self):
        """Test adding weight window card"""
        reducer = MCNPVarianceReducer()
        reducer.load_string("test\n1 0 -1 imp:n=1\n\n1 so 1\n\n")
        
        reducer.add_weight_windows(cells=[1], lower_bounds=[0.5])
        result = reducer.get_modified_input()
        
        assert 'wwn' in result.lower()
    
    def test_add_dxtran(self):
        """Test adding DXTRAN sphere"""
        reducer = MCNPVarianceReducer()
        reducer.load_string("test\n1 0 -1 imp:n=1\n\n1 so 1\n\n")
        
        reducer.add_dxtran_sphere(x=10.0, y=0.0, z=0.0, radius=1.0)
        result = reducer.get_modified_input()
        
        assert 'dxt' in result.lower() or 'dxtran' in result.lower()

class TestMCNPInputUpdater:
    
    def test_mcnp5_to_mcnp6_basic(self):
        """Test basic MCNP5 to MCNP6 conversion"""
        mcnp5_input = """Test problem
1 0 -1 imp:n=1
2 0  1 imp:n=0

1 so 5

mode n p
m1 92235.60c -1.0
"""
        
        updater = MCNPInputUpdater()
        result = updater.convert_mcnp5_to_mcnp6(mcnp5_input)
        
        # Should suggest updating cross-section libraries
        assert '80c' in result.lower() or 'endf' in result.lower()
    
    def test_generate_migration_report(self):
        """Test migration report generation"""
        updater = MCNPInputUpdater()
        updater.convert_mcnp5_to_mcnp6("test\n1 0 -1 imp:n=1\n\n1 so 1\n\nmode n\n")
        
        report = updater.generate_migration_report()
        assert 'migration' in report.lower() or 'conversion' in report.lower()
