"""
Unit tests for MCNP Transform Editor Skill

Tests transformation editing capabilities:
- Translation creation
- Rotation creation
- TR card generation
- Transformation application to cells
- Plot command generation
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-transform-editor"
sys.path.insert(0, str(skill_dir))

from mcnp_transform_editor import MCNPTransformEditor


class TestMCNPTransformEditor:
    """Test suite for MCNP Transform Editor"""

    def setup_method(self):
        """Setup test fixture"""
        self.editor = MCNPTransformEditor()

    # ===== Basic API Tests =====

    def test_editor_initialization(self):
        """Test editor initializes correctly"""
        assert self.editor is not None
        assert self.editor.parser is not None
        assert self.editor.transformations == {}
        assert self.editor.parsed is None

    def test_create_translation_interface(self):
        """Test create_translation method exists"""
        assert hasattr(self.editor, 'create_translation')
        assert callable(self.editor.create_translation)

    def test_create_rotation_interface(self):
        """Test create_rotation method exists"""
        assert hasattr(self.editor, 'create_rotation')
        assert callable(self.editor.create_rotation)

    def test_apply_to_cell_interface(self):
        """Test apply_to_cell method exists"""
        assert hasattr(self.editor, 'apply_to_cell')
        assert callable(self.editor.apply_to_cell)

    def test_generate_tr_cards_interface(self):
        """Test generate_tr_cards method exists"""
        assert hasattr(self.editor, 'generate_tr_cards')
        assert callable(self.editor.generate_tr_cards)

    def test_generate_plot_command_interface(self):
        """Test generate_plot_command method exists"""
        assert hasattr(self.editor, 'generate_plot_command')
        assert callable(self.editor.generate_plot_command)

    # ===== Translation Tests =====

    def test_create_translation_simple(self):
        """Test creating simple translation"""
        result = self.editor.create_translation(1, 10.0, 0.0, 0.0)
        assert result is not None
        assert 1 in self.editor.transformations

    def test_create_translation_3d(self):
        """Test creating 3D translation"""
        result = self.editor.create_translation(2, 5.0, 10.0, 15.0)
        assert result is not None
        assert 2 in self.editor.transformations

    def test_create_multiple_translations(self):
        """Test creating multiple translations"""
        self.editor.create_translation(1, 10.0, 0.0, 0.0)
        self.editor.create_translation(2, 0.0, 10.0, 0.0)
        self.editor.create_translation(3, 0.0, 0.0, 10.0)
        assert len(self.editor.transformations) == 3

    def test_translation_negative_values(self):
        """Test translation with negative values"""
        result = self.editor.create_translation(1, -10.0, -5.0, -2.5)
        assert result is not None

    # ===== Rotation Tests =====

    def test_create_rotation_x_axis(self):
        """Test creating rotation around X-axis"""
        result = self.editor.create_rotation(10, 'x', 90.0)
        assert result is not None
        assert 10 in self.editor.transformations

    def test_create_rotation_y_axis(self):
        """Test creating rotation around Y-axis"""
        result = self.editor.create_rotation(11, 'y', 45.0)
        assert result is not None
        assert 11 in self.editor.transformations

    def test_create_rotation_z_axis(self):
        """Test creating rotation around Z-axis"""
        result = self.editor.create_rotation(12, 'z', 180.0)
        assert result is not None
        assert 12 in self.editor.transformations

    def test_rotation_case_insensitive(self):
        """Test rotation axis is case-insensitive"""
        result1 = self.editor.create_rotation(20, 'X', 90.0)
        result2 = self.editor.create_rotation(21, 'Y', 90.0)
        result3 = self.editor.create_rotation(22, 'Z', 90.0)
        assert all([result1, result2, result3])

    def test_rotation_various_angles(self):
        """Test rotations with various angles"""
        angles = [0.0, 30.0, 45.0, 90.0, 180.0, 270.0, 360.0]
        for i, angle in enumerate(angles):
            result = self.editor.create_rotation(30 + i, 'z', angle)
            assert result is not None

    # ===== Apply to Cell Tests =====

    def test_apply_to_cell_no_data(self):
        """Test applying transformation with no data"""
        self.editor.apply_to_cell(10, 1)
        # Should not raise error

    def test_apply_to_cell_with_data(self):
        """Test applying transformation to cell"""
        mock_cell = Mock()
        mock_cell.number = 10
        mock_cell.parameters = {}

        self.editor.parsed = {'cells': [mock_cell]}
        self.editor.apply_to_cell(10, 1)
        assert mock_cell.parameters['trcl'] == 1

    def test_apply_to_nonexistent_cell(self):
        """Test applying transformation to nonexistent cell"""
        mock_cell = Mock()
        mock_cell.number = 10
        mock_cell.parameters = {}

        self.editor.parsed = {'cells': [mock_cell]}
        self.editor.apply_to_cell(999, 1)
        # Should not raise error or modify existing cell
        assert 'trcl' not in mock_cell.parameters

    # ===== TR Card Generation Tests =====

    def test_generate_tr_cards_empty(self):
        """Test generating TR cards with no transformations"""
        result = self.editor.generate_tr_cards()
        assert result == []

    def test_generate_tr_cards_single(self):
        """Test generating TR cards with one transformation"""
        self.editor.create_translation(1, 10.0, 0.0, 0.0)
        result = self.editor.generate_tr_cards()
        assert len(result) == 1

    def test_generate_tr_cards_multiple(self):
        """Test generating TR cards with multiple transformations"""
        self.editor.create_translation(1, 10.0, 0.0, 0.0)
        self.editor.create_rotation(2, 'z', 90.0)
        self.editor.create_translation(3, 0.0, 10.0, 0.0)
        result = self.editor.generate_tr_cards()
        assert len(result) == 3

    def test_generate_tr_cards_sorted(self):
        """Test TR cards are sorted by number"""
        self.editor.create_translation(3, 10.0, 0.0, 0.0)
        self.editor.create_translation(1, 10.0, 0.0, 0.0)
        self.editor.create_translation(2, 10.0, 0.0, 0.0)
        result = self.editor.generate_tr_cards()
        # Cards should be in order 1, 2, 3
        assert len(result) == 3

    # ===== Plot Command Tests =====

    def test_generate_plot_command_basic(self):
        """Test generating basic plot command"""
        result = self.editor.generate_plot_command(
            origin=(0, 0, 0),
            basis='xy',
            extent=(10, 10)
        )
        assert result is not None
        assert 'plot' in result
        assert 'origin=' in result
        assert 'basis=' in result
        assert 'extent=' in result

    def test_generate_plot_command_custom_origin(self):
        """Test plot command with custom origin"""
        result = self.editor.generate_plot_command(
            origin=(10, 20, 30),
            basis='xz',
            extent=(50, 50)
        )
        assert '10' in result
        assert '20' in result
        assert '30' in result

    def test_generate_plot_command_different_bases(self):
        """Test plot command with different basis planes"""
        bases = ['xy', 'xz', 'yz']
        for basis in bases:
            result = self.editor.generate_plot_command(
                origin=(0, 0, 0),
                basis=basis,
                extent=(10, 10)
            )
            assert basis in result

    # ===== Integration Tests =====

    def test_complete_transformation_workflow(self):
        """Test complete transformation workflow"""
        # Create transformations
        tr1 = self.editor.create_translation(1, 10.0, 0.0, 0.0)
        tr2 = self.editor.create_rotation(2, 'z', 90.0)

        # Generate TR cards
        cards = self.editor.generate_tr_cards()
        assert len(cards) == 2

        # Generate plot command
        plot = self.editor.generate_plot_command((0, 0, 0), 'xy', (20, 20))
        assert plot is not None

    def test_pwr_assembly_transformation(self):
        """Test PWR assembly grid transformation"""
        # Create translations for 17x17 grid
        pitch = 1.26  # cm
        for i in range(3):
            for j in range(3):
                tr_num = i * 3 + j + 1
                self.editor.create_translation(
                    tr_num,
                    i * pitch,
                    j * pitch,
                    0.0
                )
        assert len(self.editor.transformations) == 9

    def test_rotation_translation_combined(self):
        """Test combining rotation and translation"""
        # Common pattern: rotate then translate
        self.editor.create_rotation(10, 'z', 45.0)
        self.editor.create_translation(11, 10.0, 10.0, 0.0)

        cards = self.editor.generate_tr_cards()
        assert len(cards) == 2

    def test_file_save_with_data(self, tmp_path):
        """Test saving file with transformations"""
        self.editor.parsed = {
            'title': 'Test',
            'cells': [],
            'surfaces': [],
            'data_cards': {}
        }
        self.editor.parser.to_string = Mock(return_value="Test content")

        output_file = tmp_path / "test_transform.inp"
        self.editor.save_file(str(output_file))
        assert output_file.exists()

    def test_api_consistency(self):
        """Test all methods handle expected inputs"""
        # Create various transformations
        self.editor.create_translation(1, 0.0, 0.0, 0.0)
        self.editor.create_rotation(2, 'x', 0.0)
        self.editor.apply_to_cell(1, 1)
        cards = self.editor.generate_tr_cards()
        plot = self.editor.generate_plot_command((0, 0, 0), 'xy', (1, 1))

        assert len(cards) == 2
        assert plot is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
