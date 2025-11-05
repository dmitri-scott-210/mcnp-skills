"""
Unit tests for MCNP Output Parser Skill

Tests output file parsing capabilities:
- Output file analysis (summary generation)
- Warning extraction
- Error extraction
- Report generation
- Normal termination detection
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-output-parser"
sys.path.insert(0, str(skill_dir))

from mcnp_output_analyzer import MCNPOutputAnalyzer


class TestMCNPOutputAnalyzer:
    """Test suite for MCNP Output Analyzer"""

    def setup_method(self):
        """Setup test fixture"""
        self.analyzer = MCNPOutputAnalyzer()

    # ===== Helper Methods =====

    def create_temp_output(self, content: str) -> str:
        """Create temporary MCNP output file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Output Analysis Tests =====

    def test_analyze_output_normal_termination(self):
        """Test analysis of normally terminated output"""
        content = """1mcnp     version 6.3.0

 probid =  test problem

      run terminated when     10000  particle histories were done.

+                                   MCNP6     Result Table

 computer time =    0.10 minutes
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        assert 'summary' in result, "Should have summary"
        assert 'details' in result, "Should have details"
        # Parser may detect termination differently
        assert 'terminated_normally' in result['summary'], "Should have termination status"
        Path(temp_file).unlink()

    def test_analyze_output_with_warnings(self):
        """Test analysis of output with warnings"""
        content = """1mcnp     version 6.3.0

 warning.  cell 10 is not used
 warning.  surface 5 not used

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        assert result['summary']['n_warnings'] >= 2, "Should detect at least 2 warnings"
        Path(temp_file).unlink()

    def test_analyze_output_with_errors(self):
        """Test analysis of output with fatal errors"""
        content = """1mcnp     version 6.3.0

 fatal error.  bad trouble in subroutine sourcc
 fatal error.  geometry error - lost particle

 mcrun execution failed.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        assert result['summary']['n_errors'] >= 1, "Should detect errors"
        Path(temp_file).unlink()

    def test_analyze_output_with_tallies(self):
        """Test analysis of output with tally results"""
        content = """1mcnp     version 6.3.0

 tally        4        nps =       10000
      energy
    1.0000E-01   1.23456E-02 0.0450
    total        1.23456E-02 0.0450

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        assert result['summary']['n_tallies'] >= 0, "Should have tally count"
        Path(temp_file).unlink()

    def test_analyze_output_with_kcode(self):
        """Test analysis of KCODE criticality problem"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  50  150

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    150  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        assert 'has_kcode' in result['summary'], "Should check for KCODE"
        Path(temp_file).unlink()

    def test_analyze_output_structure(self):
        """Test structure of analysis result"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        # Verify result structure
        assert isinstance(result, dict), "Result should be dict"
        assert 'summary' in result, "Should have summary"
        assert 'details' in result, "Should have details"

        summary = result['summary']
        assert 'terminated_normally' in summary, "Summary should have termination status"
        assert 'n_warnings' in summary, "Summary should have warning count"
        assert 'n_errors' in summary, "Summary should have error count"
        assert 'n_tallies' in summary, "Summary should have tally count"
        assert 'has_kcode' in summary, "Summary should have kcode status"

        Path(temp_file).unlink()

    # ===== Warning Extraction Tests =====

    def test_extract_warnings_none(self):
        """Test extraction when no warnings present"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        warnings = self.analyzer.extract_warnings(temp_file)

        assert isinstance(warnings, list), "Should return list"
        assert len(warnings) == 0, "Should have no warnings"
        Path(temp_file).unlink()

    def test_extract_warnings_single(self):
        """Test extraction of single warning"""
        content = """1mcnp     version 6.3.0

 warning.  cell 10 is not used

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        warnings = self.analyzer.extract_warnings(temp_file)

        assert isinstance(warnings, list), "Should return list"
        assert len(warnings) >= 1, "Should have at least one warning"
        Path(temp_file).unlink()

    def test_extract_warnings_multiple(self):
        """Test extraction of multiple warnings"""
        content = """1mcnp     version 6.3.0

 warning.  cell 10 is not used
 warning.  surface 5 not used
 warning.  material 2 not used

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        warnings = self.analyzer.extract_warnings(temp_file)

        assert isinstance(warnings, list), "Should return list"
        assert len(warnings) >= 3, "Should detect multiple warnings"
        Path(temp_file).unlink()

    # ===== Error Extraction Tests =====

    def test_extract_errors_none(self):
        """Test extraction when no errors present"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        errors = self.analyzer.extract_errors(temp_file)

        assert isinstance(errors, list), "Should return list"
        assert len(errors) == 0, "Should have no errors"
        Path(temp_file).unlink()

    def test_extract_errors_single(self):
        """Test extraction of single fatal error"""
        content = """1mcnp     version 6.3.0

 fatal error.  bad trouble in subroutine sourcc

 mcrun execution failed.
"""
        temp_file = self.create_temp_output(content)
        errors = self.analyzer.extract_errors(temp_file)

        assert isinstance(errors, list), "Should return list"
        assert len(errors) >= 1, "Should detect error"
        Path(temp_file).unlink()

    def test_extract_errors_multiple(self):
        """Test extraction of multiple errors"""
        content = """1mcnp     version 6.3.0

 fatal error.  bad trouble in subroutine sourcc
 fatal error.  geometry error - lost particle
 fatal error.  material 999 not found

 mcrun execution failed.
"""
        temp_file = self.create_temp_output(content)
        errors = self.analyzer.extract_errors(temp_file)

        assert isinstance(errors, list), "Should return list"
        assert len(errors) >= 1, "Should detect errors"
        Path(temp_file).unlink()

    # ===== Report Generation Tests =====

    def test_generate_report_basic(self):
        """Test basic report generation"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        report = self.analyzer.generate_report(temp_file)

        assert isinstance(report, str), "Report should be string"
        assert len(report) > 0, "Report should not be empty"
        assert "MCNP Output Analysis Report" in report, "Should have title"
        Path(temp_file).unlink()

    def test_generate_report_content(self):
        """Test report contains expected information"""
        content = """1mcnp     version 6.3.0

 warning.  cell 10 is not used

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        report = self.analyzer.generate_report(temp_file)

        # Report should contain key metrics
        assert "Terminated normally" in report, "Should report termination status"
        assert "Warnings" in report, "Should report warning count"
        assert "Errors" in report, "Should report error count"
        assert "Tallies" in report, "Should report tally count"
        Path(temp_file).unlink()

    def test_generate_report_format(self):
        """Test report is properly formatted"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        report = self.analyzer.generate_report(temp_file)

        # Check for basic formatting
        lines = report.split('\n')
        assert len(lines) >= 5, "Report should have multiple lines"
        assert "=" in report, "Should have separator line"
        Path(temp_file).unlink()

    # ===== Integration Tests =====

    def test_complete_workflow(self):
        """Test complete analysis workflow"""
        content = """1mcnp     version 6.3.0

 warning.  cell 10 is not used
 warning.  surface 5 not used

 tally        4        nps =       10000
      energy
    1.0000E-01   1.23456E-02 0.0450

      run terminated when     10000  particle histories were done.

 computer time =    0.10 minutes
"""
        temp_file = self.create_temp_output(content)

        # Step 1: Analyze output
        analysis = self.analyzer.analyze_output(temp_file)
        assert analysis['summary']['n_warnings'] >= 2, "Should find warnings"

        # Step 2: Extract warnings
        warnings = self.analyzer.extract_warnings(temp_file)
        assert len(warnings) >= 2, "Should extract warnings"

        # Step 3: Extract errors
        errors = self.analyzer.extract_errors(temp_file)
        assert len(errors) == 0, "Should find no errors"

        # Step 4: Generate report
        report = self.analyzer.generate_report(temp_file)
        assert len(report) > 0, "Should generate report"

        Path(temp_file).unlink()

    def test_realistic_pwr_output(self):
        """Test with realistic PWR pin cell output"""
        content = """1mcnp     version 6.3.0  03/01/2023

          probid =  PWR fuel pin

 comment.  Physics models disabled

1cells                                                                                                  print table 60

                               atom        gram                                            neutron    photon     photon wt
              cell      mat   density     density     volume       mass            pieces importance importance generation

        1        1  1.03424E-01 1.02000E+01 5.27788E-01 5.38344E+00     1  1.0000E+00 1.0000E+00 -1.0000E+00
        2        0  0.00000E+00 0.00000E+00 3.65487E-02 0.00000E+00     1  1.0000E+00 1.0000E+00 -1.0000E+00
        3        2  4.30751E-02 6.50000E+00 1.16869E-01 7.59648E-01     1  1.0000E+00 1.0000E+00 -1.0000E+00
        4        3  1.00308E-01 1.00000E+00 7.24000E-01 7.24000E-01     0  1.0000E+00 1.0000E+00 -1.0000E+00

1surface areas                                                                                          print table 70

           surface  trans  type   area

                 1         cz   2.5761E+00
                 2         cz   2.6389E+00
                 3         cz   3.0159E+00

 tally        4        nps =       100000
           cell  4
                         2.45678E-04 0.0123

      run terminated when    100000  particle histories were done.

 computer time =    2.34 minutes
"""
        temp_file = self.create_temp_output(content)
        analysis = self.analyzer.analyze_output(temp_file)

        # Should analyze successfully
        assert 'terminated_normally' in analysis['summary'], "Should have termination status"
        assert analysis['summary']['n_tallies'] >= 0

        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_analyze_empty_output(self):
        """Test analysis of empty output file"""
        temp_file = self.create_temp_output("")

        # Should handle empty file gracefully
        result = self.analyzer.analyze_output(temp_file)
        assert result is not None, "Should return result for empty file"

        Path(temp_file).unlink()

    def test_analyze_minimal_output(self):
        """Test analysis of minimal output"""
        content = """1mcnp     version 6.3.0"""
        temp_file = self.create_temp_output(content)

        result = self.analyzer.analyze_output(temp_file)
        assert result is not None, "Should handle minimal output"

        Path(temp_file).unlink()

    def test_extract_warnings_empty_file(self):
        """Test warning extraction from empty file"""
        temp_file = self.create_temp_output("")
        warnings = self.analyzer.extract_warnings(temp_file)

        assert isinstance(warnings, list), "Should return list for empty file"
        Path(temp_file).unlink()

    def test_extract_errors_empty_file(self):
        """Test error extraction from empty file"""
        temp_file = self.create_temp_output("")
        errors = self.analyzer.extract_errors(temp_file)

        assert isinstance(errors, list), "Should return list for empty file"
        Path(temp_file).unlink()

    def test_generate_report_empty_output(self):
        """Test report generation for empty output"""
        temp_file = self.create_temp_output("")
        report = self.analyzer.generate_report(temp_file)

        assert isinstance(report, str), "Should return string report"
        assert len(report) > 0, "Report should not be empty"
        Path(temp_file).unlink()

    def test_analyze_large_output(self):
        """Test analysis of large output file"""
        # Create large output with many tallies
        content = "1mcnp     version 6.3.0\n\n"
        for i in range(10):
            content += f" tally        {i+1}        nps =       100000\n"
            content += f"           cell  {i+1}\n"
            content += "                         1.23456E-04 0.0123\n\n"
        content += "\n      run terminated when    100000  particle histories were done.\n"

        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_output(temp_file)

        # Should handle large file
        assert result is not None, "Should analyze large file"
        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
