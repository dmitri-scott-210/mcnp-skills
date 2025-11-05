"""
Unit tests for MCNP Geometry Editor Skill

Tests geometry editing capabilities:
- Cell parameter modification
- Surface replacement in cells
- Surface addition
- Surface removal
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-geometry-editor"
sys.path.insert(0, str(skill_dir))

from mcnp_geometry_editor import MCNPGeometryEditor


class TestMCNPGeometryEditor:
    """Test suite for MCNP Geometry Editor"""

    def setup_method(self):
        """Setup test fixture"""
        self.editor = MCNPGeometryEditor()

    # ===== Basic API Tests =====

    def test_editor_initialization(self):
        """Test editor initializes correctly"""
        assert self.editor is not None
        assert self.editor.parser is not None
        assert self.editor.geom_eval is not None
        assert self.editor.parsed is None

    def test_load_file_interface(self):
        """Test load_file method exists"""
        assert hasattr(self.editor, 'load_file')
        assert callable(self.editor.load_file)

    def test_modify_cell_parameter_interface(self):
        """Test modify_cell_parameter method exists"""
        assert hasattr(self.editor, 'modify_cell_parameter')
        assert callable(self.editor.modify_cell_parameter)

    def test_replace_surface_interface(self):
        """Test replace_surface_in_cells method exists"""
        assert hasattr(self.editor, 'replace_surface_in_cells')
        assert callable(self.editor.replace_surface_in_cells)

    def test_add_surface_interface(self):
        """Test add_surface method exists"""
        assert hasattr(self.editor, 'add_surface')
        assert callable(self.editor.add_surface)

    def test_remove_surface_interface(self):
        """Test remove_surface method exists"""
        assert hasattr(self.editor, 'remove_surface')
        assert callable(self.editor.remove_surface)

    # ===== Cell Parameter Modification Tests =====

    def test_modify_cell_parameter_no_data(self):
        """Test modifying cell parameter with no data"""
        self.editor.modify_cell_parameter(10, 'imp:n', 0)
        # Should not raise error

    def test_modify_cell_parameter_with_data(self):
        """Test modifying cell parameter with mock data"""
        mock_cell = Mock()
        mock_cell.number = 10
        mock_cell.parameters = {'imp:n': 1}

        self.editor.parsed = {'cells': [mock_cell], 'surfaces': [], 'data_cards': {}}
        self.editor.modify_cell_parameter(10, 'imp:n', 0)
        assert mock_cell.parameters['imp:n'] == 0

    def test_modify_nonexistent_cell(self):
        """Test modifying cell that doesn't exist"""
        mock_cell = Mock()
        mock_cell.number = 10
        mock_cell.parameters = {}

        self.editor.parsed = {'cells': [mock_cell], 'surfaces': []}
        self.editor.modify_cell_parameter(999, 'imp:n', 0)
        # Should not raise error

    # ===== Surface Replacement Tests =====

    def test_replace_surface_no_data(self):
        """Test replacing surface with no data"""
        self.editor.replace_surface_in_cells(1, 2)
        # Should not raise error

    def test_replace_surface_with_data(self):
        """Test replacing surface in cells"""
        mock_cell = Mock()
        mock_cell.geometry = "-1 2 -3"

        self.editor.parsed = {'cells': [mock_cell], 'surfaces': []}
        self.editor.geom_eval.substitute_surface = Mock(return_value="-2 2 -3")

        self.editor.replace_surface_in_cells(1, 2)
        self.editor.geom_eval.substitute_surface.assert_called_once()

    # ===== Surface Addition Tests =====

    def test_add_surface_no_data(self):
        """Test adding surface with no data"""
        result = self.editor.add_surface('so', [5.0])
        assert result == -1  # Returns -1 when no data

    def test_add_surface_sphere(self):
        """Test adding sphere surface"""
        self.editor.parsed = {'surfaces': [], 'cells': []}
        result = self.editor.add_surface('so', [5.0])
        assert result == 1  # First surface number
        assert len(self.editor.parsed['surfaces']) == 1

    def test_add_surface_plane(self):
        """Test adding plane surface"""
        self.editor.parsed = {'surfaces': [], 'cells': []}
        result = self.editor.add_surface('pz', [10.0])
        assert result > 0
        assert len(self.editor.parsed['surfaces']) == 1

    def test_add_multiple_surfaces(self):
        """Test adding multiple surfaces"""
        self.editor.parsed = {'surfaces': [], 'cells': []}
        surf1 = self.editor.add_surface('so', [5.0])
        surf2 = self.editor.add_surface('pz', [10.0])
        assert surf2 > surf1
        assert len(self.editor.parsed['surfaces']) == 2

    def test_add_surface_numbering(self):
        """Test surface numbering is sequential"""
        mock_surf1 = Mock()
        mock_surf1.number = 5

        self.editor.parsed = {'surfaces': [mock_surf1], 'cells': []}
        result = self.editor.add_surface('so', [5.0])
        assert result == 6  # Next after 5

    # ===== Surface Removal Tests =====

    def test_remove_surface_no_data(self):
        """Test removing surface with no data"""
        self.editor.remove_surface(1)
        # Should not raise error

    def test_remove_surface_with_data(self):
        """Test removing surface from list"""
        mock_surf1 = Mock()
        mock_surf1.number = 1
        mock_surf2 = Mock()
        mock_surf2.number = 2

        self.editor.parsed = {'surfaces': [mock_surf1, mock_surf2], 'cells': []}
        self.editor.remove_surface(1)
        assert len(self.editor.parsed['surfaces']) == 1
        assert self.editor.parsed['surfaces'][0].number == 2

    def test_remove_nonexistent_surface(self):
        """Test removing surface that doesn't exist"""
        mock_surf = Mock()
        mock_surf.number = 1

        self.editor.parsed = {'surfaces': [mock_surf], 'cells': []}
        self.editor.remove_surface(999)
        assert len(self.editor.parsed['surfaces']) == 1

    # ===== File Operations Tests =====

    def test_save_file_with_data(self, tmp_path):
        """Test saving file with data"""
        self.editor.parsed = {
            'title': 'Test',
            'cells': [],
            'surfaces': [],
            'data_cards': {}
        }
        self.editor.parser.to_string = Mock(return_value="Test content")

        output_file = tmp_path / "test_geom.inp"
        self.editor.save_file(str(output_file))
        assert output_file.exists()

    # ===== Integration Tests =====

    def test_complete_geometry_edit(self):
        """Test complete geometry editing workflow"""
        # Initialize
        self.editor.parsed = {'surfaces': [], 'cells': [], 'data_cards': {}}

        # Add surfaces
        s1 = self.editor.add_surface('so', [5.0])
        s2 = self.editor.add_surface('so', [10.0])
        assert len(self.editor.parsed['surfaces']) == 2

        # Remove one surface
        self.editor.remove_surface(s1)
        assert len(self.editor.parsed['surfaces']) == 1

    def test_pwr_pin_geometry_editing(self):
        """Test editing PWR pin cell geometry"""
        self.editor.parsed = {'surfaces': [], 'cells': []}

        # Add fuel, gap, clad surfaces
        fuel_surf = self.editor.add_surface('cz', [0.41])
        gap_surf = self.editor.add_surface('cz', [0.42])
        clad_surf = self.editor.add_surface('cz', [0.48])

        assert fuel_surf < gap_surf < clad_surf
        assert len(self.editor.parsed['surfaces']) == 3

    def test_api_consistency(self):
        """Test all methods handle None parsed data gracefully"""
        # All these should not raise errors when parsed is None
        self.editor.modify_cell_parameter(1, 'imp:n', 0)
        self.editor.replace_surface_in_cells(1, 2)
        self.editor.remove_surface(1)
        result = self.editor.add_surface('so', [5.0])
        assert result == -1  # Correctly returns -1 for no data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
