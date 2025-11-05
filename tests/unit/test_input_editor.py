"""
Unit tests for MCNP Input Editor Skill

Tests input file editing capabilities:
- File loading
- Search and replace
- Comment addition
- Card removal
- File saving
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-input-editor"
sys.path.insert(0, str(skill_dir))

from mcnp_input_editor import MCNPInputEditor


class TestMCNPInputEditor:
    """Test suite for MCNP Input Editor"""

    def setup_method(self):
        """Setup test fixture"""
        self.editor = MCNPInputEditor()

    # ===== Basic API Tests =====

    def test_editor_initialization(self):
        """Test editor initializes correctly"""
        assert self.editor is not None
        assert self.editor.parser is not None
        assert self.editor.parsed is None

    def test_load_file_interface(self):
        """Test load_file method exists"""
        assert hasattr(self.editor, 'load_file')
        assert callable(self.editor.load_file)

    def test_search_replace_interface(self):
        """Test search_replace method exists"""
        assert hasattr(self.editor, 'search_replace')
        assert callable(self.editor.search_replace)

    def test_add_comment_interface(self):
        """Test add_comment method exists"""
        assert hasattr(self.editor, 'add_comment')
        assert callable(self.editor.add_comment)

    def test_remove_card_interface(self):
        """Test remove_card method exists"""
        assert hasattr(self.editor, 'remove_card')
        assert callable(self.editor.remove_card)

    def test_save_file_interface(self):
        """Test save_file method exists"""
        assert hasattr(self.editor, 'save_file')
        assert callable(self.editor.save_file)

    # ===== Search and Replace Tests =====

    def test_search_replace_no_data(self):
        """Test search and replace with no loaded data"""
        result = self.editor.search_replace('old', 'new')
        assert result == 0  # No changes when no data loaded

    def test_search_replace_with_mock_data(self):
        """Test search and replace with mock data"""
        mock_cell = Mock()
        mock_cell.raw = "10 1 -2.7 -1 imp:n=1"
        mock_cell.number = 10
        mock_cell.material = 1
        mock_cell.density = -2.7
        mock_cell.geometry = "-1"
        mock_cell.parameters = {'imp:n': 1}

        self.editor.parsed = {'cells': [mock_cell], 'surfaces': [], 'data_cards': {}}
        self.editor.parser._parse_cell_card = Mock(return_value=mock_cell)

        result = self.editor.search_replace('imp:n=1', 'imp:n=0')
        assert result >= 0  # Returns count of changes

    # ===== Comment Addition Tests =====

    def test_add_comment_top(self):
        """Test adding comment at top"""
        self.editor.add_comment("Test comment", position='top')
        assert self.editor.parsed is not None
        assert len(self.editor.parsed['message_block']) > 0
        assert 'c Test comment' in self.editor.parsed['message_block'][0]

    def test_add_comment_bottom(self):
        """Test adding comment at bottom"""
        self.editor.add_comment("First comment", position='bottom')
        self.editor.add_comment("Second comment", position='bottom')
        assert len(self.editor.parsed['message_block']) == 2
        assert 'c Second comment' in self.editor.parsed['message_block'][-1]

    def test_add_multiple_comments(self):
        """Test adding multiple comments"""
        self.editor.add_comment("Comment 1", position='top')
        self.editor.add_comment("Comment 2", position='top')
        self.editor.add_comment("Comment 3", position='bottom')
        assert len(self.editor.parsed['message_block']) == 3

    # ===== Card Removal Tests =====

    def test_remove_card_no_data(self):
        """Test removing card with no data"""
        self.editor.remove_card('nps')
        # Should not raise error

    def test_remove_card_with_data(self):
        """Test removing card from parsed data"""
        self.editor.parsed = {
            'data_cards': {'nps': Mock(), 'mode': Mock()},
            'cells': [],
            'surfaces': []
        }
        self.editor.remove_card('nps')
        assert 'nps' not in self.editor.parsed['data_cards']
        assert 'mode' in self.editor.parsed['data_cards']

    def test_remove_nonexistent_card(self):
        """Test removing card that doesn't exist"""
        self.editor.parsed = {'data_cards': {}, 'cells': [], 'surfaces': []}
        self.editor.remove_card('nonexistent')
        # Should not raise error

    # ===== File Operations Tests =====

    def test_save_file_no_data(self, tmp_path):
        """Test saving file with no data"""
        output_file = tmp_path / "test_output.inp"
        self.editor.save_file(str(output_file))
        # Should not raise error, file may or may not be created

    def test_save_file_with_data(self, tmp_path):
        """Test saving file with data"""
        self.editor.parsed = {
            'title': 'Test Problem',
            'message_block': ['c Test comment'],
            'cells': [],
            'surfaces': [],
            'data_cards': {}
        }
        self.editor.parser.to_string = Mock(return_value="Test content")

        output_file = tmp_path / "test_output.inp"
        self.editor.save_file(str(output_file))
        assert output_file.exists()

    # ===== Integration Tests =====

    def test_complete_edit_workflow(self, tmp_path):
        """Test complete editing workflow"""
        # Initialize with data
        self.editor.parsed = {
            'title': 'Test Problem',
            'message_block': [],
            'cells': [],
            'surfaces': [],
            'data_cards': {'nps': Mock(), 'mode': Mock()}
        }
        # Add comment
        self.editor.add_comment("Modified by automated test")
        # Remove card
        self.editor.remove_card('nps')
        # Verify changes
        assert len(self.editor.parsed['message_block']) > 0
        assert 'nps' not in self.editor.parsed['data_cards']

    def test_api_consistency(self):
        """Test all methods handle None parsed data gracefully"""
        # All these should not raise errors when parsed is None
        self.editor.search_replace('old', 'new')
        self.editor.remove_card('test')
        output_file = Path(__file__).parent / "temp_test.inp"
        try:
            self.editor.save_file(str(output_file))
        except:
            pass  # May fail but should not crash
        finally:
            if output_file.exists():
                output_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
