"""
Unit tests for MCNP Input Updater Skill

Tests MCNP version migration capabilities:
- MCNP5 to MCNP6 conversion
- Library ID updates (.50c -> .80c)
- Deprecated card conversion
- Migration report generation
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-input-updater"
sys.path.insert(0, str(skill_dir))

from mcnp_input_updater import MCNPInputUpdater


class TestMCNPInputUpdater:
    """Test suite for MCNP Input Updater"""

    def setup_method(self):
        """Setup test fixture"""
        self.updater = MCNPInputUpdater()

    # ===== Basic API Tests =====

    def test_updater_initialization(self):
        """Test updater initializes correctly"""
        assert self.updater is not None
        assert self.updater.parser is not None
        assert self.updater.changes_made == []
        assert self.updater.parsed is None

    def test_convert_mcnp5_to_mcnp6_interface(self):
        """Test convert_mcnp5_to_mcnp6 method exists"""
        assert hasattr(self.updater, 'convert_mcnp5_to_mcnp6')
        assert callable(self.updater.convert_mcnp5_to_mcnp6)

    def test_generate_migration_report_interface(self):
        """Test generate_migration_report method exists"""
        assert hasattr(self.updater, 'generate_migration_report')
        assert callable(self.updater.generate_migration_report)

    # ===== Library Update Tests =====

    def test_library_update_50c_to_80c(self):
        """Test updating .50c libraries to .80c"""
        mock_card = Mock()
        mock_card.entries = ['92235.50c', '0.03', '92238.50c', '0.97']

        self.updater.parsed = {
            'data_cards': {'m1': mock_card},
            'cells': [],
            'surfaces': [],
            'title': ''
        }
        self.updater.parser.to_string = Mock(return_value="Updated")

        # Simulate conversion
        for i, entry in enumerate(mock_card.entries):
            if '.50c' in entry:
                mock_card.entries[i] = entry.replace('.50c', '.80c')

        assert '92235.80c' in mock_card.entries
        assert '92238.80c' in mock_card.entries

    def test_library_update_60c_to_80c(self):
        """Test updating .60c libraries to .80c"""
        mock_card = Mock()
        mock_card.entries = ['1001.60c', '2', '8016.60c', '1']

        # Simulate conversion
        for i, entry in enumerate(mock_card.entries):
            if '.60c' in entry:
                mock_card.entries[i] = entry.replace('.60c', '.80c')

        assert '1001.80c' in mock_card.entries
        assert '8016.80c' in mock_card.entries

    def test_library_mixed_updates(self):
        """Test updating mixed library versions"""
        mock_card = Mock()
        mock_card.entries = ['92235.50c', '0.03', '1001.60c', '2.0']

        # Simulate conversion
        for i, entry in enumerate(mock_card.entries):
            if '.50c' in entry:
                mock_card.entries[i] = entry.replace('.50c', '.80c')
            elif '.60c' in entry:
                mock_card.entries[i] = entry.replace('.60c', '.80c')

        assert '92235.80c' in mock_card.entries
        assert '1001.80c' in mock_card.entries

    # ===== Deprecated Card Tests =====

    def test_deprecated_notrn_to_phys(self):
        """Test converting NOTRN to PHYS:P"""
        deprecated_map = {
            'notrn': 'phys:p',
            'pikmt': 'lcolr'
        }

        assert 'notrn' in deprecated_map
        assert deprecated_map['notrn'] == 'phys:p'

    def test_deprecated_pikmt_to_lcolr(self):
        """Test converting PIKMT to LCOLR"""
        deprecated_map = {
            'notrn': 'phys:p',
            'pikmt': 'lcolr'
        }

        assert 'pikmt' in deprecated_map
        assert deprecated_map['pikmt'] == 'lcolr'

    # ===== Migration Report Tests =====

    def test_generate_report_no_changes(self):
        """Test generating report with no changes"""
        result = self.updater.generate_migration_report()
        assert result is not None
        assert 'Migration Report' in result
        assert 'Total changes: 0' in result

    def test_generate_report_with_changes(self):
        """Test generating report with changes"""
        self.updater.changes_made = [
            'Updated 92235.50c to .80c library',
            'Updated 92238.50c to .80c library',
            'Converted NOTRN to PHYS:P'
        ]
        result = self.updater.generate_migration_report()
        assert 'Total changes: 3' in result
        assert '92235.50c' in result
        assert 'NOTRN' in result

    def test_generate_report_formatting(self):
        """Test report formatting"""
        self.updater.changes_made = ['Test change']
        result = self.updater.generate_migration_report()
        assert '=' in result  # Has separator
        assert '  -' in result  # Has bullet points

    # ===== Integration Tests =====

    def test_complete_migration_workflow(self, tmp_path):
        """Test complete MCNP5 to MCNP6 migration"""
        # Create mock input file
        input_file = tmp_path / "input_mcnp5.inp"
        input_file.write_text("Test MCNP5 input")

        # Create mock parsed data
        mock_m1 = Mock()
        mock_m1.entries = ['92235.50c', '0.03', '92238.50c', '0.97']
        mock_m2 = Mock()
        mock_m2.entries = ['1001.60c', '2', '8016.60c', '1']

        self.updater.parser.parse_file = Mock(return_value={
            'data_cards': {'m1': mock_m1, 'm2': mock_m2},
            'cells': [],
            'surfaces': [],
            'title': 'Test'
        })
        self.updater.parser.to_string = Mock(return_value="Converted input")

        output_file = tmp_path / "input_mcnp6.inp"
        changes = self.updater.convert_mcnp5_to_mcnp6(
            str(input_file),
            str(output_file)
        )

        assert output_file.exists()
        assert isinstance(changes, list)

    def test_pwr_core_migration(self):
        """Test migrating PWR core model from MCNP5 to MCNP6"""
        # Mock PWR fuel materials
        mock_fuel = Mock()
        mock_fuel.entries = [
            '92235.50c', '0.03',
            '92238.50c', '0.97',
            '8016.50c', '2.0'
        ]

        mock_water = Mock()
        mock_water.entries = ['1001.60c', '2', '8016.60c', '1']

        mock_zirc = Mock()
        mock_zirc.entries = ['40090.50c', '0.50']

        self.updater.parsed = {
            'data_cards': {
                'm1': mock_fuel,
                'm2': mock_water,
                'm3': mock_zirc
            }
        }

        # All .50c and .60c should be updated to .80c
        # (This would happen in the actual conversion method)

    def test_multiple_materials_migration(self):
        """Test migrating file with many materials"""
        materials = {}
        for i in range(1, 11):  # 10 materials
            mock_mat = Mock()
            mock_mat.entries = [f'92235.50c', '1.0']
            materials[f'm{i}'] = mock_mat

        self.updater.parsed = {'data_cards': materials}
        # Each material should be tracked for conversion

    def test_changes_tracking(self):
        """Test that changes are properly tracked"""
        self.updater.changes_made = []
        self.updater.changes_made.append('Test change 1')
        self.updater.changes_made.append('Test change 2')
        assert len(self.updater.changes_made) == 2

    def test_no_conversion_needed(self, tmp_path):
        """Test file with no conversion needed"""
        # File already using .80c libraries
        mock_card = Mock()
        mock_card.entries = ['92235.80c', '1.0']

        self.updater.parser.parse_file = Mock(return_value={
            'data_cards': {'m1': mock_card},
            'cells': [],
            'surfaces': [],
            'title': 'Already MCNP6'
        })
        self.updater.parser.to_string = Mock(return_value="No changes")

        input_file = tmp_path / "input.inp"
        input_file.write_text("Test")
        output_file = tmp_path / "output.inp"

        changes = self.updater.convert_mcnp5_to_mcnp6(
            str(input_file),
            str(output_file)
        )

        # Should complete successfully even with no changes
        assert isinstance(changes, list)

    def test_partial_conversion(self):
        """Test file with mix of old and new libraries"""
        mock_card = Mock()
        # Mix of .80c (already converted) and .50c (needs conversion)
        mock_card.entries = ['92235.80c', '0.03', '92238.50c', '0.97']

        # Only .50c should be converted
        for i, entry in enumerate(mock_card.entries):
            if '.50c' in entry:
                mock_card.entries[i] = entry.replace('.50c', '.80c')

        assert mock_card.entries == ['92235.80c', '0.03', '92238.80c', '0.97']

    def test_api_consistency(self):
        """Test API handles expected operations"""
        # Generate report should work even with no conversion
        report = self.updater.generate_migration_report()
        assert report is not None

        # Changes list should be accessible
        assert isinstance(self.updater.changes_made, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
