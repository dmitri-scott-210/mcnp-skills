"""
Integration tests - End-to-end workflows
"""
import pytest
from skills.input_creation.mcnp_input_generator import MCNPInputGenerator
from skills.validation.mcnp_input_validator import MCNPInputValidator
from skills.input_editing.mcnp_geometry_editor import MCNPGeometryEditor
from skills.output_analysis.mcnp_tally_analyzer import MCNPTallyAnalyzer

class TestEndToEndWorkflows:
    
    def test_create_validate_workflow(self):
        """Test: Create input → Validate"""
        # Step 1: Create input
        generator = MCNPInputGenerator()
        input_text = generator.generate_simple_problem(
            geometry_type='sphere',
            radius=5.0,
            material_z=92,
            source_energy=14.1
        )
        
        # Step 2: Validate
        validator = MCNPInputValidator()
        result = validator.validate_string(input_text)
        
        assert result['is_valid'] is True
    
    def test_create_edit_validate_workflow(self):
        """Test: Create → Edit → Validate"""
        # Step 1: Create
        generator = MCNPInputGenerator()
        input_text = generator.generate_simple_problem(
            geometry_type='sphere',
            radius=5.0,
            material_z=82,
            source_energy=1.0
        )
        
        # Step 2: Edit geometry
        editor = MCNPGeometryEditor()
        editor.load_string(input_text)
        editor.modify_cell_parameter(1, density=-11.34)  # Change to lead density
        modified = editor.get_modified_input()
        
        # Step 3: Validate
        validator = MCNPInputValidator()
        result = validator.validate_string(modified)
        
        assert result['is_valid'] is True
    
    def test_full_problem_lifecycle(self):
        """Test complete problem lifecycle"""
        from skills.input_creation.mcnp_geometry_builder import MCNPGeometryBuilder
        from skills.input_creation.mcnp_material_builder import MCNPMaterialBuilder
        from skills.input_creation.mcnp_source_builder import MCNPSourceBuilder
        from skills.input_creation.mcnp_tally_builder import MCNPTallyBuilder
        
        # 1. Build geometry
        geom = MCNPGeometryBuilder()
        geom.add_sphere(1, 0, 0, 0, 5.0)
        geom.add_sphere(2, 0, 0, 0, 10.0)
        geom.add_cell(10, 1, -7.87, '-1', importance_n=1)
        geom.add_cell(20, 2, -1.0, '1 -2', importance_n=1)
        geom.add_cell(30, 0, 0, '2', importance_n=0)
        
        # 2. Build materials
        mat = MCNPMaterialBuilder()
        mat.add_material(1)
        mat.add_element(1, 'Fe', -7.87, 'mass')
        mat.add_material(2)
        mat.add_compound(2, 'H2O', density_g_cm3=1.0)
        
        # 3. Build source
        source = MCNPSourceBuilder()
        source.set_position(0, 0, 0)
        source.set_energy(14.1)
        
        # 4. Build tallies
        tally = MCNPTallyBuilder()
        tally.add_cell_flux([10, 20], particle='n')
        tally.add_energy_bins(4, [0.01, 0.1, 1.0, 10.0])
        
        # 5. Combine into full input
        full_input = f"""Full problem test
{geom.generate_input()}

{mat.generate_cards()}
{source.generate_sdef()}
mode n
nps 10000
{tally.generate_tallies()}
"""
        
        # 6. Validate
        validator = MCNPInputValidator()
        result = validator.validate_string(full_input)
        
        assert result is not None
    
    def test_analyze_existing_file(self, tal01_input):
        """Test analyzing existing input file"""
        from parsers.input_parser import MCNPInputParser
        from skills.validation.mcnp_geometry_checker import MCNPGeometryChecker
        
        # 1. Parse
        parser = MCNPInputParser()
        parsed = parser.parse_string(tal01_input)
        
        assert len(parsed['cells']) >= 3
        
        # 2. Check geometry
        checker = MCNPGeometryChecker()
        geom_result = checker.check_geometry_string(tal01_input)
        
        assert 'surfaces' in geom_result
        
        # 3. Generate plots
        plots = checker.generate_plot_commands(tal01_input)
        assert len(plots) > 0
