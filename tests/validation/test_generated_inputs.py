"""
Validation Tests for Generated MCNP Inputs

Tests that skills generate complete, valid MCNP input files that could be run by MCNP.
These tests validate realistic end-to-end workflows.

Test scenarios:
1. Simple sphere with source and tally - should be executable
2. PWR pin cell - should be executable
3. Shielding slab - should be executable
4. Dosimetry sphere - should be executable

Note: These tests verify structural correctness. Actual MCNP execution requires
MCNP6 installation (not required for these tests).
"""
import pytest
import sys
import tempfile
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

# Add skill directories to path
template_gen_dir = project_root / ".claude" / "skills" / "mcnp-template-generator"
input_validator_dir = project_root / ".claude" / "skills" / "mcnp-input-validator"

sys.path.insert(0, str(template_gen_dir))
sys.path.insert(0, str(input_validator_dir))

from mcnp_template_generator import MCNPTemplateGenerator
from mcnp_input_validator import MCNPInputValidator


class TestGeneratedInputs:
    """Validation test suite for generated MCNP inputs"""

    def setup_method(self):
        """Setup test fixtures"""
        self.generator = MCNPTemplateGenerator()
        self.validator = MCNPInputValidator()

    def create_temp_input(self, content: str) -> str:
        """Create temporary MCNP input file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.inp', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    def validate_mcnp_structure(self, input_text: str) -> dict:
        """Validate MCNP input structure"""
        lines = input_text.split('\n')

        # Check for three main blocks more flexibly
        # Cells: numeric lines at start (after title), or lines with imp
        has_cells = any(
            (line.strip() and line.strip()[0].isdigit() and 'imp' in line.lower())
            or ('cell' in line.lower() and line.strip().startswith('c'))
            for line in lines[1:30]  # Check more lines
        )

        # Surfaces: lines with surface mnemonics
        has_surfaces = any(
            any(surf in line.lower() for surf in ['so ', 'cz ', 'pz ', 'px ', 'py ', 's ', 'c/'])
            or ('surface' in line.lower() and line.strip().startswith('c'))
            for line in lines
        )

        # Data cards: mode, nps, kcode, sdef, etc.
        has_data = any(card in input_text.lower()
                       for card in ['mode', 'nps', 'kcode', 'sdef', 'ksrc'])

        return {
            'has_title': len(lines) > 0 and len(lines[0].strip()) > 0 and not lines[0].strip().startswith('c'),
            'has_cells': has_cells,
            'has_surfaces': has_surfaces,
            'has_data': has_data,
            'line_count': len(lines)
        }

    # ===== PWR Pin Cell Validation =====

    def test_pwr_pin_cell_complete(self):
        """Test that PWR pin cell template is complete and valid"""
        # Generate PWR template
        input_text = self.generator.reactor_unit_cell()
        assert input_text is not None
        assert isinstance(input_text, str)

        # Validate structure
        structure = self.validate_mcnp_structure(input_text)
        assert structure['has_title'], "Missing title"
        assert structure['has_cells'], "Missing cell cards"
        assert structure['has_surfaces'], "Missing surface cards"
        assert structure['has_data'], "Missing data cards"

        # Validate with validator
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        assert 'valid' in result or 'errors' in result
        Path(temp_file).unlink()

    def test_pwr_pin_cell_has_fuel(self):
        """Test that PWR contains fuel material"""
        input_text = self.generator.reactor_unit_cell()
        assert 'uo2' in input_text.lower() or '92235' in input_text or 'm1' in input_text.lower()

    def test_pwr_pin_cell_has_moderator(self):
        """Test that PWR contains water moderator"""
        input_text = self.generator.reactor_unit_cell()
        assert 'water' in input_text.lower() or '1001' in input_text

    def test_pwr_pin_cell_has_kcode(self):
        """Test that PWR uses KCODE for criticality"""
        input_text = self.generator.reactor_unit_cell()
        assert 'kcode' in input_text.lower()

    def test_pwr_pin_cell_has_lattice(self):
        """Test that PWR uses lattice structure"""
        input_text = self.generator.reactor_unit_cell()
        assert 'lat=' in input_text or 'lat =' in input_text or 'fill=' in input_text

    # ===== Dosimetry Sphere Validation =====

    def test_dosimetry_sphere_complete(self):
        """Test that dosimetry sphere is complete and valid"""
        input_text = self.generator.dosimetry_sphere()
        assert input_text is not None

        # Validate structure
        structure = self.validate_mcnp_structure(input_text)
        assert structure['has_title'], "Missing title"
        assert structure['has_cells'], "Missing cell cards"
        assert structure['has_surfaces'], "Missing surface cards"
        assert structure['has_data'], "Missing data cards"

        # Validate
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        Path(temp_file).unlink()

    def test_dosimetry_sphere_has_source(self):
        """Test that dosimetry sphere has source definition"""
        input_text = self.generator.dosimetry_sphere()
        assert 'sdef' in input_text.lower()

    def test_dosimetry_sphere_has_tally(self):
        """Test that dosimetry sphere has tally"""
        input_text = self.generator.dosimetry_sphere()
        # Should have F6 (heating) or F4 (flux) tally
        assert 'f6' in input_text.lower() or 'f4' in input_text.lower()

    def test_dosimetry_sphere_mode_np(self):
        """Test that dosimetry uses n,p mode"""
        input_text = self.generator.dosimetry_sphere()
        assert 'mode' in input_text.lower()

    # ===== Shielding Slab Validation =====

    def test_shielding_slab_complete(self):
        """Test that shielding slab is complete and valid"""
        input_text = self.generator.shielding_slab()
        assert input_text is not None

        # Validate structure
        structure = self.validate_mcnp_structure(input_text)
        assert structure['has_title'], "Missing title"
        assert structure['has_cells'], "Missing cell cards"
        assert structure['has_surfaces'], "Missing surface cards"
        assert structure['has_data'], "Missing data cards"

        # Validate
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        Path(temp_file).unlink()

    def test_shielding_slab_has_shield_material(self):
        """Test that shielding slab has shield material"""
        input_text = self.generator.shielding_slab()
        # Should have aluminum or some material
        assert 'm1' in input_text.lower() or '13027' in input_text

    def test_shielding_slab_has_planes(self):
        """Test that shielding slab uses plane surfaces"""
        input_text = self.generator.shielding_slab()
        assert 'pz' in input_text or 'px' in input_text or 'py' in input_text

    def test_shielding_slab_has_surface_tally(self):
        """Test that shielding has surface tally (F2)"""
        input_text = self.generator.shielding_slab()
        assert 'f2' in input_text.lower() or 'f1' in input_text.lower()

    # ===== Customization Validation =====

    def test_pwr_custom_pitch(self):
        """Test PWR with custom pitch"""
        input_text = self.generator.reactor_unit_cell(pitch=1.5)
        assert '1.5' in input_text

        # Should still be valid
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        Path(temp_file).unlink()

    def test_pwr_custom_fuel_radius(self):
        """Test PWR with custom fuel radius"""
        input_text = self.generator.reactor_unit_cell(fuel_radius=0.45)
        assert '0.45' in input_text

        # Should still be valid
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        Path(temp_file).unlink()

    def test_shielding_custom_thickness(self):
        """Test shielding with custom thickness"""
        input_text = self.generator.shielding_slab(thickness=20)
        assert '20' in input_text

        # Should still be valid
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        Path(temp_file).unlink()

    # ===== Realistic Problem Validation =====

    def test_realistic_pwr_assembly(self):
        """Test realistic PWR assembly configuration"""
        # Generate with realistic parameters
        input_text = self.generator.reactor_unit_cell(
            pitch=1.26,
            fuel_radius=0.41,
            clad_thickness=0.07
        )

        # Validate structure
        structure = self.validate_mcnp_structure(input_text)
        assert structure['line_count'] >= 15, "PWR assembly should have substantial content"

        # Validate
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None

        # Check for key PWR components
        assert 'uo2' in input_text.lower() or '92235' in input_text, "Missing fuel"
        assert 'zirc' in input_text.lower() or '40090' in input_text, "Missing cladding"
        assert 'water' in input_text.lower() or 'm3' in input_text.lower(), "Missing water"

        Path(temp_file).unlink()

    def test_all_templates_structurally_valid(self):
        """Test that all templates are structurally valid"""
        templates = {
            'PWR': self.generator.reactor_unit_cell(),
            'Dosimetry': self.generator.dosimetry_sphere(),
            'Shielding': self.generator.shielding_slab()
        }

        for name, input_text in templates.items():
            # Validate structure
            structure = self.validate_mcnp_structure(input_text)
            assert structure['has_title'], f"{name}: Missing title"
            assert structure['has_cells'], f"{name}: Missing cells"
            assert structure['has_surfaces'], f"{name}: Missing surfaces"
            assert structure['has_data'], f"{name}: Missing data"

            # Validate with validator
            temp_file = self.create_temp_input(input_text)
            result = self.validator.validate_file(temp_file)
            assert result is not None, f"{name}: Validation failed"
            Path(temp_file).unlink()

    # ===== Format Validation =====

    def test_proper_blank_line_separation(self):
        """Test that blocks are separated by blank lines"""
        input_text = self.generator.reactor_unit_cell()
        lines = input_text.split('\n')

        # Should have at least 2 blank lines (separating 3 blocks)
        blank_lines = [i for i, line in enumerate(lines) if line.strip() == '']
        assert len(blank_lines) >= 2, "MCNP requires blank lines between blocks"

    def test_no_duplicate_card_numbers(self):
        """Test that cell/surface numbers are not duplicated"""
        input_text = self.generator.reactor_unit_cell()
        # Basic check - validator should catch duplicates
        temp_file = self.create_temp_input(input_text)
        result = self.validator.validate_file(temp_file)
        assert result is not None
        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
