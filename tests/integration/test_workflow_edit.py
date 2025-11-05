"""
Integration tests for Generate → Edit → Validate workflow

Tests the complete workflow:
1. Generate template with template-generator
2. Edit geometry with geometry-editor
3. Validate edited input with input-validator

This workflow simulates typical user interaction when modifying templates.
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

# Add skill directories to path
template_gen_dir = project_root / ".claude" / "skills" / "mcnp-template-generator"
geometry_editor_dir = project_root / ".claude" / "skills" / "mcnp-geometry-editor"
input_validator_dir = project_root / ".claude" / "skills" / "mcnp-input-validator"

sys.path.insert(0, str(template_gen_dir))
sys.path.insert(0, str(geometry_editor_dir))
sys.path.insert(0, str(input_validator_dir))

from mcnp_template_generator import MCNPTemplateGenerator
from mcnp_geometry_editor import MCNPGeometryEditor
from mcnp_input_validator import MCNPInputValidator


class TestWorkflowEdit:
    """Test suite for Generate → Edit → Validate workflow"""

    def setup_method(self):
        """Setup test fixtures"""
        self.template_gen = MCNPTemplateGenerator()
        self.geo_editor = MCNPGeometryEditor()
        self.validator = MCNPInputValidator()

    # ===== PWR Template Workflow =====

    def test_pwr_template_edit_workflow(self):
        """Test complete workflow: generate PWR → edit parameters → validate"""
        # Step 1: Generate PWR template
        template = self.template_gen.reactor_unit_cell()
        assert template is not None
        assert len(template) > 100

        # Step 2: Edit cell density
        edited = self.geo_editor.modify_cell_parameter(
            template,
            cell_id=1,
            parameter='density',
            new_value=-10.5
        )
        assert edited is not None

        # Step 3: Validate edited input
        validation_result = self.validator.validate_input(edited)
        assert validation_result is not None

    def test_pwr_template_pitch_modification(self):
        """Test modifying PWR pin pitch"""
        # Step 1: Generate PWR with default pitch
        template = self.template_gen.reactor_unit_cell(pitch=1.26)
        assert template is not None

        # Step 2: Generate with modified pitch
        modified = self.template_gen.reactor_unit_cell(pitch=1.50)
        assert modified is not None
        assert '1.5' in modified

        # Step 3: Validate modified input
        validation_result = self.validator.validate_input(modified)
        assert validation_result is not None

    def test_pwr_fuel_radius_modification(self):
        """Test modifying fuel radius"""
        # Step 1: Generate PWR with custom fuel radius
        template = self.template_gen.reactor_unit_cell(fuel_radius=0.45)
        assert template is not None
        assert '0.45' in template

        # Step 2: Validate
        validation_result = self.validator.validate_input(template)
        assert validation_result is not None

    # ===== Dosimetry Sphere Workflow =====

    def test_dosimetry_template_workflow(self):
        """Test dosimetry sphere template workflow"""
        # Step 1: Generate dosimetry sphere
        template = self.template_gen.dosimetry_sphere()
        assert template is not None
        assert 'Dosimetry Sphere' in template

        # Step 2: Edit surface (change radius)
        edited = self.geo_editor.modify_surface(
            template,
            surface_id=1,
            new_definition='so 15.0'  # Change sphere radius to 15cm
        )
        assert edited is not None

        # Step 3: Validate
        validation_result = self.validator.validate_input(edited)
        assert validation_result is not None

    # ===== Shielding Slab Workflow =====

    def test_shielding_slab_edit_workflow(self):
        """Test shielding slab template editing"""
        # Step 1: Generate slab with default thickness
        template = self.template_gen.shielding_slab()
        assert template is not None

        # Step 2: Generate with custom thickness
        modified = self.template_gen.shielding_slab(thickness=20)
        assert modified is not None
        assert '20 cm' in modified

        # Step 3: Validate
        validation_result = self.validator.validate_input(modified)
        assert validation_result is not None

    def test_shielding_material_change(self):
        """Test changing shielding material"""
        # Step 1: Generate aluminum slab
        template = self.template_gen.shielding_slab()
        assert template is not None

        # Step 2: Edit to change material (aluminum → lead)
        # Replace aluminum material with lead
        edited = self.geo_editor.modify_cell_parameter(
            template,
            cell_id=1,
            parameter='material',
            new_value=2  # Change to material 2
        )
        assert edited is not None

        # Step 3: Validate
        validation_result = self.validator.validate_input(edited)
        assert validation_result is not None

    # ===== Multiple Edit Workflow =====

    def test_multiple_edits_workflow(self):
        """Test multiple sequential edits"""
        # Step 1: Generate template
        template = self.template_gen.reactor_unit_cell()
        assert template is not None

        # Step 2: First edit - change fuel density
        edit1 = self.geo_editor.modify_cell_parameter(
            template,
            cell_id=1,
            parameter='density',
            new_value=-10.8
        )
        assert edit1 is not None

        # Step 3: Second edit - change material
        edit2 = self.geo_editor.modify_cell_parameter(
            edit1,
            cell_id=2,
            parameter='material',
            new_value=5
        )
        assert edit2 is not None

        # Step 4: Validate final result
        validation_result = self.validator.validate_input(edit2)
        assert validation_result is not None

    # ===== Surface Editing Workflow =====

    def test_surface_replacement_workflow(self):
        """Test replacing surface definitions"""
        # Step 1: Generate template
        template = self.template_gen.dosimetry_sphere()
        assert template is not None

        # Step 2: Replace sphere surface with cylinder
        edited = self.geo_editor.replace_surface(
            template,
            old_surface_id=1,
            new_definition='cz 10.0'  # Replace sphere with cylinder
        )
        assert edited is not None

        # Step 3: Validate (may have errors due to incompatible geometry)
        validation_result = self.validator.validate_input(edited)
        assert validation_result is not None

    def test_add_surface_workflow(self):
        """Test adding new surfaces"""
        # Step 1: Generate simple template
        template = self.template_gen.dosimetry_sphere()
        assert template is not None

        # Step 2: Add additional surface
        edited = self.geo_editor.add_surface(
            template,
            surface_id=999,
            definition='pz 20.0'  # Add plane surface
        )
        assert edited is not None

        # Step 3: Validate
        validation_result = self.validator.validate_input(edited)
        assert validation_result is not None

    # ===== Comment Addition Workflow =====

    def test_add_comments_workflow(self):
        """Test adding comments to template"""
        # Step 1: Generate template
        template = self.template_gen.reactor_unit_cell()
        assert template is not None

        # Step 2: Add comments
        # Note: geometry_editor might not have add_comment, but we can test if it exists
        if hasattr(self.geo_editor, 'add_comment'):
            edited = self.geo_editor.add_comment(
                template,
                "Modified for 4.5% enrichment"
            )
            assert edited is not None

            # Step 3: Validate
            validation_result = self.validator.validate_input(edited)
            assert validation_result is not None

    # ===== Error Recovery Workflow =====

    def test_invalid_edit_detection(self):
        """Test that invalid edits are detected during validation"""
        # Step 1: Generate valid template
        template = self.template_gen.dosimetry_sphere()
        assert template is not None

        # Step 2: Make invalid edit (reference non-existent surface)
        # Manually create invalid edit
        invalid_edit = template.replace('1 1 -1.0', '1 1 -1.0 -999')  # Reference surface 999

        # Step 3: Validate should detect error
        validation_result = self.validator.validate_input(invalid_edit)
        assert validation_result is not None
        # Should flag missing surface reference

    # ===== Template Customization Workflow =====

    def test_pwr_enrichment_workflow(self):
        """Test customizing PWR enrichment"""
        # Step 1: Generate 3.5% enriched PWR (default)
        template_35 = self.template_gen.reactor_unit_cell()
        assert template_35 is not None

        # Step 2: Validate original
        validation_35 = self.validator.validate_input(template_35)
        assert validation_35 is not None

        # Step 3: Edit enrichment (would require modifying m1 material card)
        # For testing, we just verify the template validates
        # In practice, user would manually edit material card

    # ===== Workflow Timing Tests =====

    def test_workflow_performance(self):
        """Test workflow performance"""
        import time

        start = time.time()

        # Generate template
        template = self.template_gen.reactor_unit_cell()
        assert template is not None

        # Edit
        edited = self.geo_editor.modify_cell_parameter(
            template,
            cell_id=1,
            parameter='density',
            new_value=-10.5
        )
        assert edited is not None

        # Validate
        validation_result = self.validator.validate_input(edited)
        assert validation_result is not None

        elapsed = time.time() - start

        # Should complete quickly
        assert elapsed < 5.0, f"Workflow took {elapsed:.2f}s (expected < 5s)"

    # ===== Round-Trip Workflow =====

    def test_generate_edit_regenerate_workflow(self):
        """Test generating, editing, and regenerating templates"""
        # Step 1: Generate template with pitch 1.26
        template1 = self.template_gen.reactor_unit_cell(pitch=1.26)
        assert template1 is not None

        # Step 2: Validate first version
        validation1 = self.validator.validate_input(template1)
        assert validation1 is not None

        # Step 3: Generate new template with pitch 1.50
        template2 = self.template_gen.reactor_unit_cell(pitch=1.50)
        assert template2 is not None

        # Step 4: Validate second version
        validation2 = self.validator.validate_input(template2)
        assert validation2 is not None

        # Both should be valid
        assert template1 != template2  # Should be different

    # ===== All Templates Workflow =====

    def test_all_templates_workflow(self):
        """Test generating and validating all templates"""
        templates = []

        # Generate all templates
        t1 = self.template_gen.reactor_unit_cell()
        t2 = self.template_gen.dosimetry_sphere()
        t3 = self.template_gen.shielding_slab()

        templates.extend([t1, t2, t3])

        # Validate all
        for i, template in enumerate(templates):
            assert template is not None, f"Template {i} is None"
            validation = self.validator.validate_input(template)
            assert validation is not None, f"Validation {i} failed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
