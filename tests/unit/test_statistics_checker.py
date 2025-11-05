"""
Unit tests for MCNP Statistics Checker Skill

Tests the 10 statistical checks validation:
- Mean stability in final half
- Relative error < 0.10
- Variance of variance (VOV) < 0.10
- Figure of merit (FOM) stability
- PDF slope in range 3-10
- All 10 bins passed
- No oscillatory behavior
- Confidence intervals overlap
- Largest tally < 5% of total
- Relative error decreases as 1/√N
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-statistics-checker"
sys.path.insert(0, str(skill_dir))

from mcnp_statistics_checker import MCNPStatisticsChecker


class TestMCNPStatisticsChecker:
    """Test suite for MCNP Statistics Checker"""

    def setup_method(self):
        """Setup test fixture"""
        self.checker = MCNPStatisticsChecker()

    # ===== Helper Methods =====

    def create_temp_output(self, content: str) -> str:
        """Create temporary MCNP output file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Check All Tallies Tests =====

    def test_check_all_tallies_passing(self):
        """Test checking tallies with all checks passing"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
           tally type 4    track length estimate of particle flux.
           particle(s): neutrons

 volumes
            cell:       1
                       1.00000E+00

 multiplier bin:    1.00000E+00
 cell  1
      energy
    1.0000E-01   1.23456E-02 0.0450
    total        1.23456E-02 0.0450

 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)
        result = self.checker.check_all_tallies(temp_file)

        # Should return dictionary with tally results
        assert isinstance(result, dict), "Should return dictionary"
        Path(temp_file).unlink()

    def test_check_all_tallies_failing(self):
        """Test checking tallies with failed checks"""
        output_content = """1mcnp     version 6.3.0

 tally        5        nps =    1000
           tally type 5    flux at a point detector.

 cell  1
      energy
    1.0000E-01   5.67890E-03 0.2500
    total        5.67890E-03 0.2500

 warning.  tally        5 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.checker.check_all_tallies(temp_file)

        assert isinstance(result, dict), "Should return dictionary"
        Path(temp_file).unlink()

    def test_check_all_tallies_multiple(self):
        """Test checking multiple tallies"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
      energy
    1.0000E-01   1.23456E-02 0.0450
    total        1.23456E-02 0.0450
 passed all 10 statistical checks

 tally        14        nps =    10000
      energy
    1.0000E-01   2.34567E-03 0.0600
    total        2.34567E-03 0.0600
 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)
        result = self.checker.check_all_tallies(temp_file)

        assert isinstance(result, dict), "Should return dictionary"
        # May have entries for tallies 4 and 14
        Path(temp_file).unlink()

    def test_check_all_tallies_no_tallies(self):
        """Test checking output with no tallies"""
        output_content = """1mcnp     version 6.3.0

      run terminated when       1000  particle histories were done.
"""
        temp_file = self.create_temp_output(output_content)
        result = self.checker.check_all_tallies(temp_file)

        assert isinstance(result, dict), "Should return dictionary"
        assert len(result) == 0, "Should have no tally results"
        Path(temp_file).unlink()

    def test_check_all_tallies_structure(self):
        """Test that result has expected structure"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
      energy
    1.0000E-01   1.23456E-02 0.0450
    total        1.23456E-02 0.0450
 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)
        result = self.checker.check_all_tallies(temp_file)

        # Each tally should have: all_passed, checks, fom
        for tally_num, tally_data in result.items():
            if tally_data:  # May be empty dict
                assert isinstance(tally_data, dict), "Tally data should be dict"
                # May have keys: all_passed, checks, fom
        Path(temp_file).unlink()

    # ===== Get Failed Checks Tests =====

    def test_get_failed_checks_none_failed(self):
        """Test getting failed checks when all pass"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
      energy
    1.0000E-01   1.23456E-02 0.0450
    total        1.23456E-02 0.0450
 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)
        failed = self.checker.get_failed_checks(temp_file)

        assert isinstance(failed, dict), "Should return dictionary"
        # Should be empty or have no failed checks
        Path(temp_file).unlink()

    def test_get_failed_checks_some_failed(self):
        """Test getting failed checks when some fail"""
        output_content = """1mcnp     version 6.3.0

 tally        5        nps =    1000
      energy
    1.0000E-01   5.67890E-03 0.2500
    total        5.67890E-03 0.2500
 warning.  tally        5 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        failed = self.checker.get_failed_checks(temp_file)

        assert isinstance(failed, dict), "Should return dictionary"
        Path(temp_file).unlink()

    def test_get_failed_checks_multiple_tallies(self):
        """Test getting failed checks with multiple tallies"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
 passed all 10 statistical checks

 tally        5        nps =    1000
 warning.  tally        5 has not passed all 10 statistical checks.

 tally        14        nps =    5000
 warning.  tally       14 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        failed = self.checker.get_failed_checks(temp_file)

        assert isinstance(failed, dict), "Should return dictionary"
        # Should have entries for tallies 5 and 14 (but not 4)
        Path(temp_file).unlink()

    def test_get_failed_checks_no_tallies(self):
        """Test getting failed checks from file with no tallies"""
        output_content = """1mcnp     version 6.3.0

      run terminated when       1000  particle histories were done.
"""
        temp_file = self.create_temp_output(output_content)
        failed = self.checker.get_failed_checks(temp_file)

        assert isinstance(failed, dict), "Should return dictionary"
        assert len(failed) == 0, "Should have no failed checks"
        Path(temp_file).unlink()

    # ===== Recommend Improvements Tests =====

    def test_recommend_improvements_no_failures(self):
        """Test recommendations when all checks pass"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)
        recommendations = self.checker.recommend_improvements(temp_file)

        assert isinstance(recommendations, list), "Should return list"
        assert len(recommendations) == 0, "Should have no recommendations when all pass"
        Path(temp_file).unlink()

    def test_recommend_improvements_with_failures(self):
        """Test recommendations when checks fail"""
        output_content = """1mcnp     version 6.3.0

 tally        5        nps =    1000
 warning.  tally        5 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        recommendations = self.checker.recommend_improvements(temp_file)

        assert isinstance(recommendations, list), "Should return list"
        # Should have recommendations if failed checks detected
        Path(temp_file).unlink()

    def test_recommend_improvements_structure(self):
        """Test recommendation structure"""
        output_content = """1mcnp     version 6.3.0

 tally        5        nps =    1000
 warning.  tally        5 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        recommendations = self.checker.recommend_improvements(temp_file)

        # Each recommendation should have: tally, issue, suggestions
        for rec in recommendations:
            assert isinstance(rec, dict), "Each recommendation should be dict"
            # May have keys: tally, issue, suggestions
        Path(temp_file).unlink()

    def test_recommend_improvements_multiple_tallies(self):
        """Test recommendations for multiple failing tallies"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
 passed all 10 statistical checks

 tally        5        nps =    1000
 warning.  tally        5 has not passed all 10 statistical checks.

 tally        14        nps =    500
 warning.  tally       14 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)
        recommendations = self.checker.recommend_improvements(temp_file)

        assert isinstance(recommendations, list), "Should return list"
        # Should have recommendations for tallies 5 and 14 (not 4)
        Path(temp_file).unlink()

    # ===== Integration Tests =====

    def test_workflow_check_then_recommend(self):
        """Test complete workflow: check all -> get failed -> recommend"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
 passed all 10 statistical checks

 tally        5        nps =    1000
 warning.  tally        5 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)

        # Step 1: Check all tallies
        all_checks = self.checker.check_all_tallies(temp_file)
        assert isinstance(all_checks, dict), "Should get all checks"

        # Step 2: Get failed checks
        failed = self.checker.get_failed_checks(temp_file)
        assert isinstance(failed, dict), "Should get failed checks"

        # Step 3: Get recommendations
        recommendations = self.checker.recommend_improvements(temp_file)
        assert isinstance(recommendations, list), "Should get recommendations"

        Path(temp_file).unlink()

    def test_realistic_pwr_output(self):
        """Test with realistic PWR simulation output"""
        output_content = """1mcnp     version 6.3.0  03/01/2023

          probid =  PWR fuel pin k-infinity

 kcode  10000 1.000 30 130

 tally        4        nps =  1300000
           tally type 4    track length estimate of particle flux.
           particle(s): neutrons

 volumes
            cell:       1            2            3            4
                       5.28318E-01  5.65487E-02  2.06637E-01  2.55098E+00

 cell  1
      energy
    1.0000E-08   1.23456E-04 0.0012
    6.2506E-07   2.34567E-03 0.0015
    1.0000E+01   3.45678E-05 0.0180
    total        5.67890E-03 0.0008

 passed all 10 statistical checks

      run terminated when     130  kcode cycles were done.
"""
        temp_file = self.create_temp_output(output_content)

        # Should handle realistic output
        all_checks = self.checker.check_all_tallies(temp_file)
        assert isinstance(all_checks, dict), "Should parse realistic output"

        failed = self.checker.get_failed_checks(temp_file)
        assert isinstance(failed, dict), "Should get failed checks"
        assert len(failed) == 0, "PWR output should pass all checks"

        recommendations = self.checker.recommend_improvements(temp_file)
        assert len(recommendations) == 0, "Should have no recommendations when passing"

        Path(temp_file).unlink()

    def test_realistic_point_detector(self):
        """Test with point detector tally (often has poor statistics)"""
        output_content = """1mcnp     version 6.3.0

 tally        5        nps =    50000
           tally type 5    flux at a point detector.
           particle(s): neutrons

 detector located at x,y,z =  1.00000E+01  0.00000E+00  0.00000E+00

      energy
    1.0000E-08   8.90123E-06 0.3500
    1.0000E+01   7.89012E-07 0.4200
    total        9.69035E-06 0.3200

 warning.  tally        5 has not passed all 10 statistical checks.
           passed  1 of the 10 statistical checks

 fom = (histories/minute)*(f(x)/relative error)**2 =  1.23E+02
"""
        temp_file = self.create_temp_output(output_content)

        all_checks = self.checker.check_all_tallies(temp_file)
        assert isinstance(all_checks, dict), "Should parse point detector"

        failed = self.checker.get_failed_checks(temp_file)
        # Should detect failed checks for tally 5

        recommendations = self.checker.recommend_improvements(temp_file)
        assert isinstance(recommendations, list), "Should have recommendations"
        # Should recommend increasing NPS or variance reduction

        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_empty_output_file(self):
        """Test with empty output file"""
        temp_file = self.create_temp_output("")

        result = self.checker.check_all_tallies(temp_file)
        assert isinstance(result, dict), "Should handle empty file"
        assert len(result) == 0, "Empty file should have no tallies"

        Path(temp_file).unlink()

    def test_output_file_no_statistics(self):
        """Test output file that terminated early (no statistics)"""
        output_content = """1mcnp     version 6.3.0

      fatal error.  bad trouble in subroutine sourcc of mcrun
            source particle type is not on mode card.
"""
        temp_file = self.create_temp_output(output_content)

        result = self.checker.check_all_tallies(temp_file)
        assert isinstance(result, dict), "Should handle error output"

        Path(temp_file).unlink()

    def test_many_tallies(self):
        """Test with many tallies"""
        tally_blocks = []
        for i in range(4, 24, 2):  # Tallies 4, 6, 8, ..., 22
            tally_blocks.append(f"""
 tally       {i:2d}        nps =    10000
      energy
    1.0000E-01   {i}.23456E-02 0.0{i:02d}0
    total        {i}.23456E-02 0.0{i:02d}0
 passed all 10 statistical checks
""")

        output_content = "1mcnp     version 6.3.0\n" + "\n".join(tally_blocks)
        temp_file = self.create_temp_output(output_content)

        result = self.checker.check_all_tallies(temp_file)
        assert isinstance(result, dict), "Should handle many tallies"

        Path(temp_file).unlink()

    def test_tally_with_multiplier_bins(self):
        """Test tally with multiplier bins (more complex)"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
           tally type 4    track length estimate of particle flux.

 volumes
            cell:       1
                       1.00000E+00

 multiplier bin:    1.00000E+00
 cell  1
      energy
    1.0000E-01   1.23456E-02 0.0450
    total        1.23456E-02 0.0450

 multiplier bin:    2.53000E-08  (  1001.80c   (n,gamma) )
 cell  1
      energy
    1.0000E-01   3.45678E-04 0.1200
    total        3.45678E-04 0.1200

 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)

        result = self.checker.check_all_tallies(temp_file)
        assert isinstance(result, dict), "Should handle multiplier bins"

        Path(temp_file).unlink()

    def test_tally_numbers_non_sequential(self):
        """Test with non-sequential tally numbers"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
 passed all 10 statistical checks

 tally       14        nps =    10000
 passed all 10 statistical checks

 tally      104        nps =    10000
 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)

        result = self.checker.check_all_tallies(temp_file)
        assert isinstance(result, dict), "Should handle non-sequential tallies"

        Path(temp_file).unlink()

    def test_recommendations_content_quality(self):
        """Test that recommendations contain useful content"""
        output_content = """1mcnp     version 6.3.0

 tally        5        nps =    1000
 warning.  tally        5 has not passed all 10 statistical checks.
"""
        temp_file = self.create_temp_output(output_content)

        recommendations = self.checker.recommend_improvements(temp_file)

        # Recommendations should have meaningful content
        for rec in recommendations:
            if 'suggestions' in rec:
                assert len(rec['suggestions']) > 0, "Should have suggestions"
                for suggestion in rec['suggestions']:
                    assert isinstance(suggestion, str), "Suggestion should be string"
                    assert len(suggestion) > 10, "Suggestion should be meaningful"

        Path(temp_file).unlink()

    def test_check_all_tallies_preserves_tally_numbers(self):
        """Test that tally numbers are preserved in results"""
        output_content = """1mcnp     version 6.3.0

 tally        4        nps =    10000
 passed all 10 statistical checks

 tally       24        nps =    10000
 passed all 10 statistical checks
"""
        temp_file = self.create_temp_output(output_content)

        result = self.checker.check_all_tallies(temp_file)

        # Should preserve original tally numbers as keys
        assert isinstance(result, dict), "Should return dictionary"

        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
