"""
Unit tests for MCNP Warning Analyzer Skill

Tests warning analysis and categorization capabilities:
- Warning detection from output files
- Warning categorization (geometry, material, tally, source, other)
- Warning prioritization
- Multiple warning handling
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-warning-analyzer"
sys.path.insert(0, str(skill_dir))

from mcnp_warning_analyzer import MCNPWarningAnalyzer


class TestMCNPWarningAnalyzer:
    """Test suite for MCNP Warning Analyzer"""

    def setup_method(self):
        """Setup test fixture"""
        self.analyzer = MCNPWarningAnalyzer()

    # ===== Helper Methods =====

    def create_temp_output(self, content: str) -> str:
        """Create temporary MCNP output file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Warning Detection Tests =====

    def test_analyze_geometry_warning(self):
        """Test detection of geometry warning"""
        output_content = """
1mcnp     version 6.3.0

 warning.  cell      100 is not used.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        # Should detect at least one warning
        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings > 0, "Should detect warning"
        Path(temp_file).unlink()

    def test_analyze_material_warning(self):
        """Test detection of material warning"""
        output_content = """
 warning.  material        1 has been set to a conductor.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings > 0, "Should detect material warning"
        Path(temp_file).unlink()

    def test_analyze_tally_warning(self):
        """Test detection of tally warning"""
        output_content = """
 warning.  tally        5 needs more than 1000 histories.
 warning.  tally has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings >= 2, "Should detect both tally warnings"
        Path(temp_file).unlink()

    def test_analyze_source_warning(self):
        """Test detection of source warning"""
        output_content = """
 warning.  source energy is outside the range of cross section data.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings > 0, "Should detect source warning"
        Path(temp_file).unlink()

    def test_analyze_no_warnings(self):
        """Test output with no warnings"""
        output_content = """
1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings == 0, "Should detect no warnings"
        Path(temp_file).unlink()

    # ===== Warning Categorization Tests =====

    def test_categorization_structure(self):
        """Test that result has all expected categories"""
        output_content = """
 warning.  test warning
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        # Check all expected categories exist
        expected_categories = ['geometry', 'material', 'tally', 'source', 'other']
        for cat in expected_categories:
            assert cat in result, f"Category '{cat}' should exist in result"

        Path(temp_file).unlink()

    def test_multiple_warnings_same_category(self):
        """Test handling multiple warnings of same category"""
        output_content = """
 warning.  cell      100 is not used.
 warning.  cell      200 is not used.
 warning.  surface   50 is not used.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        # Should have multiple warnings captured
        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings >= 3, "Should capture all warnings"
        Path(temp_file).unlink()

    def test_mixed_category_warnings(self):
        """Test warnings from multiple categories"""
        output_content = """
 warning.  cell      100 is not used.
 warning.  material        1 has been set to a conductor.
 warning.  tally        5 needs more than 1000 histories.
 warning.  source energy is outside cross section range.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings >= 4, "Should detect warnings from multiple categories"
        Path(temp_file).unlink()

    # ===== Warning Prioritization Tests =====

    def test_prioritize_empty_warnings(self):
        """Test prioritization of empty warning dict"""
        warnings = {'geometry': [], 'material': [], 'tally': [], 'source': [], 'other': []}
        prioritized = self.analyzer.prioritize_warnings(warnings)

        assert isinstance(prioritized, list), "Should return a list"
        assert len(prioritized) == 0, "Empty warnings should produce empty list"

    def test_prioritize_single_warning(self):
        """Test prioritization of single warning"""
        warnings = {
            'geometry': [],
            'material': [],
            'tally': ['tally 5 has poor statistics'],
            'source': [],
            'other': []
        }
        prioritized = self.analyzer.prioritize_warnings(warnings)

        assert len(prioritized) == 1, "Should have one prioritized warning"
        assert prioritized[0]['category'] == 'tally'
        assert 'tally 5' in prioritized[0]['message']

    def test_prioritize_multiple_warnings_order(self):
        """Test that prioritization follows correct order"""
        warnings = {
            'geometry': ['geometry warning 1'],
            'material': ['material warning 1'],
            'tally': ['tally warning 1'],
            'source': ['source warning 1'],
            'other': ['other warning 1']
        }
        prioritized = self.analyzer.prioritize_warnings(warnings)

        assert len(prioritized) == 5, "Should have all 5 warnings"

        # Check order: geometry, material, source, tally, other
        categories = [w['category'] for w in prioritized]
        expected_order = ['geometry', 'material', 'source', 'tally', 'other']
        assert categories == expected_order, f"Order should be {expected_order}"

    def test_prioritize_preserves_messages(self):
        """Test that prioritization preserves warning messages"""
        test_message = "cell 100 is not used"
        warnings = {
            'geometry': [test_message],
            'material': [],
            'tally': [],
            'source': [],
            'other': []
        }
        prioritized = self.analyzer.prioritize_warnings(warnings)

        assert prioritized[0]['message'] == test_message, "Message should be preserved"

    # ===== Integration Tests =====

    def test_analyze_and_prioritize_workflow(self):
        """Test complete workflow: analyze then prioritize"""
        output_content = """
1mcnp     version 6.3.0

 warning.  cell      100 is not used.
 warning.  material        1 has been set to a conductor.
 warning.  tally        5 needs more than 1000 histories.
"""
        temp_file = self.create_temp_output(output_content)

        # Step 1: Analyze
        warnings = self.analyzer.analyze_warnings(temp_file)

        # Step 2: Prioritize
        prioritized = self.analyzer.prioritize_warnings(warnings)

        assert len(prioritized) >= 3, "Should have at least 3 warnings"
        assert all('category' in w and 'message' in w for w in prioritized), \
            "Each warning should have category and message"

        Path(temp_file).unlink()

    def test_realistic_warning_output(self):
        """Test with realistic MCNP warning output"""
        output_content = """1mcnp     version 6.3.0  03/01/2023

          probid =  test problem

 comment.  total nubar used if fissionable isotopes are present.

 warning.  material        1 is used in a problem with fissionable material.
           the material is treated as a conductor.

 warning.  cell      999 has importance=0 but volume>0.
           this cell will be a true void.

 warning.  tally       14 has not passed all 10 statistical checks.

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(output_content)
        warnings = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in warnings.values())
        assert total_warnings >= 3, "Should detect multiple realistic warnings"
        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_analyze_empty_file(self):
        """Test analysis of empty file"""
        temp_file = self.create_temp_output("")
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings == 0, "Empty file should have no warnings"
        Path(temp_file).unlink()

    def test_analyze_warning_case_insensitive(self):
        """Test that 'Warning' vs 'warning' vs 'WARNING' all detected"""
        output_content = """
 Warning.  test 1
 warning.  test 2
 WARNING.  test 3
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings >= 3, "Should detect warnings regardless of case"
        Path(temp_file).unlink()

    def test_analyze_partial_warning_keyword(self):
        """Test that 'warning' substring is detected"""
        output_content = """
 subwarning.  test message
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        # 'warning' in 'subwarning' should match
        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings > 0, "Should detect warning substring"
        Path(temp_file).unlink()

    def test_prioritize_multiple_same_category(self):
        """Test prioritization with multiple warnings in same category"""
        warnings = {
            'geometry': ['warning 1', 'warning 2', 'warning 3'],
            'material': [],
            'tally': [],
            'source': [],
            'other': []
        }
        prioritized = self.analyzer.prioritize_warnings(warnings)

        assert len(prioritized) == 3, "Should have 3 warnings"
        assert all(w['category'] == 'geometry' for w in prioritized), \
            "All should be geometry category"

    def test_analyze_non_ascii_warnings(self):
        """Test handling of non-ASCII characters in warnings"""
        output_content = """
 warning.  cell café has special characters
 warning.  résumé of warnings
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        # Should handle without crashing
        assert result is not None, "Should handle non-ASCII characters"
        Path(temp_file).unlink()

    def test_analyze_very_long_warning(self):
        """Test handling of very long warning messages"""
        long_warning = " warning.  " + "x" * 10000
        output_content = f"""
{long_warning}
"""
        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings > 0, "Should handle very long warnings"
        Path(temp_file).unlink()

    # ===== Multiple Warning Tests =====

    def test_analyze_hundreds_of_warnings(self):
        """Test handling of many warnings (stress test)"""
        warnings_list = [f" warning.  test warning {i}" for i in range(100)]
        output_content = "\n".join(warnings_list)

        temp_file = self.create_temp_output(output_content)
        result = self.analyzer.analyze_warnings(temp_file)

        total_warnings = sum(len(warns) for warns in result.values())
        assert total_warnings == 100, "Should capture all 100 warnings"
        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
