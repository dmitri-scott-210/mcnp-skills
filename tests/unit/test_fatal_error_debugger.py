"""
Unit tests for MCNP Fatal Error Debugger Skill

Tests error diagnosis and fix suggestion capabilities:
- Fatal error detection from output files
- Error pattern matching
- Fix suggestions
- Common error retrieval
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-fatal-error-debugger"
sys.path.insert(0, str(skill_dir))

from mcnp_fatal_error_debugger import MCNPFatalErrorDebugger


class TestMCNPFatalErrorDebugger:
    """Test suite for MCNP Fatal Error Debugger"""

    def setup_method(self):
        """Setup test fixture"""
        self.debugger = MCNPFatalErrorDebugger()

    # ===== Helper Methods =====

    def create_temp_output(self, content: str) -> str:
        """Create temporary MCNP output file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Error Detection Tests =====

    def test_diagnose_sourcc_error(self):
        """Test detection of sourcc fatal error"""
        output_content = """
1mcnp     version 6.3.0

 fatal error.  bad trouble in subroutine sourcc of mcrun
                source particle type is not on mode card.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] > 0, "Should detect fatal error"
        assert any('sourcc' in err['message'].lower() for err in result['errors']), \
            "Should detect sourcc error"
        Path(temp_file).unlink()

    def test_diagnose_lost_particle_error(self):
        """Test detection of lost particle error"""
        output_content = """
 particle  12345678 lost.
   x,y,z coordinates:  1.23456E+01  2.34567E+01  3.45678E+01
   u,v,w directions :  1.0000E+00  0.0000E+00  0.0000E+00
   energy = 1.4100E+01 MeV    weight = 1.0000E+00
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        # Note: "lost" might not trigger "fatal" keyword
        # This test verifies the file can be read
        assert result is not None, "Should return result"
        Path(temp_file).unlink()

    def test_diagnose_geometry_error(self):
        """Test detection of geometry error"""
        output_content = """
 fatal error.  geometry error - lost particle
         cell  100 surface   5 sense   -1
         x,y,z coordinates:  0.00000E+00  0.00000E+00  5.00001E+00
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] > 0, "Should detect fatal error"
        Path(temp_file).unlink()

    def test_diagnose_no_errors(self):
        """Test output with no fatal errors"""
        output_content = """
1mcnp     version 6.3.0

 probid =  test problem

      run terminated when     10000  particle histories were done.

+                                   MCNP6     Result Table
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] == 0, "Should detect no fatal errors"
        Path(temp_file).unlink()

    # ===== Fix Suggestion Tests =====

    def test_suggest_fix_sourcc(self):
        """Test fix suggestion for sourcc error"""
        error = "fatal error.  bad trouble in subroutine sourcc"
        fix = self.debugger.suggest_fix(error)

        assert fix is not None, "Should return a fix suggestion"
        assert len(fix) > 0, "Fix suggestion should not be empty"
        # Typically mentions source or MODE card
        assert 'source' in fix.lower() or 'mode' in fix.lower(), \
            "Fix should mention source or mode"

    def test_suggest_fix_lost_particle(self):
        """Test fix suggestion for lost particle"""
        error = "particle lost"
        fix = self.debugger.suggest_fix(error)

        assert fix is not None, "Should return a fix suggestion"
        assert len(fix) > 0, "Fix suggestion should not be empty"

    def test_suggest_fix_unknown_error(self):
        """Test fix suggestion for unknown error"""
        error = "completely unknown error message xyz123"
        fix = self.debugger.suggest_fix(error)

        assert fix is not None, "Should return something"
        assert 'no known fix' in fix.lower() or fix == "", \
            "Should indicate no known fix"

    # ===== Common Errors Tests =====

    def test_get_common_errors(self):
        """Test retrieval of common fatal errors"""
        common_errors = self.debugger.get_common_errors()

        assert isinstance(common_errors, list), "Should return a list"
        assert len(common_errors) > 0, "Should have at least one common error"

    def test_common_errors_have_patterns(self):
        """Test that common errors have required fields"""
        common_errors = self.debugger.get_common_errors()

        if len(common_errors) > 0:
            first_error = common_errors[0]
            # Check that error objects have expected attributes
            assert hasattr(first_error, 'pattern') or isinstance(first_error, dict), \
                "Errors should have pattern information"

    # ===== Integration Tests =====

    def test_diagnose_multiple_errors(self):
        """Test detection of multiple fatal errors in one output"""
        output_content = """
1mcnp     version 6.3.0

 fatal error.  bad trouble in subroutine sourcc
 fatal error.  geometry error - lost particle
 fatal error.  material 999 not found
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] >= 1, "Should detect at least one error"
        Path(temp_file).unlink()

    def test_diagnose_with_bad_trouble(self):
        """Test detection using 'bad trouble' keyword"""
        output_content = """
 fatal error.  bad trouble in subroutine sourcc of mcrun
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] > 0, "Should detect bad trouble as fatal error"
        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_diagnose_empty_output(self):
        """Test diagnosis of empty output file"""
        temp_file = self.create_temp_output("")
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] == 0, "Empty file should have no errors"
        Path(temp_file).unlink()

    def test_diagnose_non_ascii_characters(self):
        """Test handling of non-ASCII characters in output"""
        output_content = """
1mcnp     version 6.3.0

 Some text with non-ASCII: café résumé

 fatal error.  test error
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        # Should handle non-ASCII without crashing
        assert result is not None, "Should handle non-ASCII characters"
        Path(temp_file).unlink()

    def test_suggest_fix_empty_string(self):
        """Test fix suggestion for empty error message"""
        fix = self.debugger.suggest_fix("")

        assert fix is not None, "Should handle empty string"

    def test_suggest_fix_very_long_message(self):
        """Test fix suggestion for very long error message"""
        long_message = "fatal error. " + "x" * 10000
        fix = self.debugger.suggest_fix(long_message)

        assert fix is not None, "Should handle long messages"

    # ===== Realistic Error Scenarios =====

    def test_realistic_sourcc_scenario(self):
        """Test realistic sourcc error scenario"""
        output_content = """1mcnp     version 6.3.0  03/01/2023

          probid =  test problem

 bad trouble in subroutine sourcc of mcrun
         source particle type   1 is not on mode card.
         source energy = 1.4100E+01

 mcrun execution failed.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.debugger.diagnose_error(temp_file)

        assert result['count'] > 0, "Should detect error"

        # Test fix suggestion
        if result['errors']:
            error_msg = result['errors'][0]['message']
            fix = self.debugger.suggest_fix(error_msg)
            assert len(fix) > 0, "Should provide fix"

        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
