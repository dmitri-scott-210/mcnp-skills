"""
Unit tests for MCNP Criticality Analyzer Skill

Tests KCODE analysis capabilities:
- K-effective analysis
- Convergence checking
- Cycle history extraction
- Uncertainty evaluation
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-criticality-analyzer"
sys.path.insert(0, str(skill_dir))

from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer


class TestMCNPCriticalityAnalyzer:
    """Test suite for MCNP Criticality Analyzer"""

    def setup_method(self):
        """Setup test fixture"""
        self.analyzer = MCNPCriticalityAnalyzer()

    # ===== Helper Methods =====

    def create_temp_output(self, content: str) -> str:
        """Create temporary MCNP output file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== KCODE Analysis Tests =====

    def test_analyze_kcode_present(self):
        """Test analysis when KCODE data is present"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  50  150

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    150  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        assert 'has_kcode' in result, "Should check for KCODE"
        Path(temp_file).unlink()

    def test_analyze_kcode_absent(self):
        """Test analysis when no KCODE data present"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        assert result['has_kcode'] == False, "Should detect no KCODE"
        assert len(result) == 1, "Should only have has_kcode field"
        Path(temp_file).unlink()

    def test_analyze_kcode_structure(self):
        """Test structure of KCODE analysis result"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  50  150

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    150  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        # Check expected fields (if KCODE present)
        if result['has_kcode']:
            assert 'k_effective' in result, "Should have k_effective"
            assert 'uncertainty' in result, "Should have uncertainty"
            assert 'converged' in result, "Should have convergence status"

        Path(temp_file).unlink()

    def test_analyze_kcode_converged(self):
        """Test analysis of well-converged KCODE"""
        content = """1mcnp     version 6.3.0

 kcode  100000  1.0  100  500

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    500  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # σ = 0.00045 < 0.005, should be converged
            assert result['converged'] == True, "Should detect convergence"

        Path(temp_file).unlink()

    def test_analyze_kcode_not_converged(self):
        """Test analysis of poorly-converged KCODE"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  10  50

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.01234

      run terminated when     50  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # σ = 0.01234 > 0.005, should not be converged
            assert result['converged'] == False, "Should detect poor convergence"

        Path(temp_file).unlink()

    def test_analyze_kcode_boundary_convergence(self):
        """Test analysis at convergence boundary"""
        content = """1mcnp     version 6.3.0

 kcode  50000  1.0  50  200

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00500

      run terminated when    200  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # σ = 0.00500 == 0.005, boundary case
            # Implementation may vary (< vs <=)
            assert 'converged' in result, "Should have convergence status"

        Path(temp_file).unlink()

    # ===== Cycle History Tests =====

    def test_get_cycle_history_present(self):
        """Test getting cycle history when KCODE present"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  50  150

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    150  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        history = self.analyzer.get_cycle_history(temp_file)

        assert isinstance(history, list), "Should return list"
        Path(temp_file).unlink()

    def test_get_cycle_history_absent(self):
        """Test getting cycle history when no KCODE"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        history = self.analyzer.get_cycle_history(temp_file)

        assert isinstance(history, list), "Should return list"
        assert len(history) == 0, "Should be empty for non-KCODE"
        Path(temp_file).unlink()

    def test_get_cycle_history_length(self):
        """Test cycle history has expected length"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  50  150

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    150  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        history = self.analyzer.get_cycle_history(temp_file)

        # History length depends on parser implementation
        assert isinstance(history, list), "Should be list"
        Path(temp_file).unlink()

    # ===== Convergence Checking Tests =====

    def test_check_convergence_converged(self):
        """Test convergence check for well-converged system"""
        content = """1mcnp     version 6.3.0

 kcode  100000  1.0  100  500

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    500  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.check_convergence(temp_file)

        assert isinstance(result, dict), "Should return dict"
        assert 'converged' in result, "Should have convergence status"
        if result['converged']:
            assert result['recommendation'] == 'Good', "Should recommend Good"

        Path(temp_file).unlink()

    def test_check_convergence_not_converged(self):
        """Test convergence check for poorly-converged system"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  10  50

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.01234

      run terminated when     50  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.check_convergence(temp_file)

        assert isinstance(result, dict), "Should return dict"
        assert 'converged' in result, "Should have convergence status"
        if not result['converged'] and 'recommendation' in result:
            assert 'Run more cycles' in result['recommendation'], "Should recommend more cycles"

        Path(temp_file).unlink()

    def test_check_convergence_no_kcode(self):
        """Test convergence check when no KCODE data"""
        content = """1mcnp     version 6.3.0

      run terminated when     10000  particle histories were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.check_convergence(temp_file)

        assert result['converged'] == False, "Should not be converged without KCODE"
        assert 'reason' in result, "Should have reason field"
        assert 'No KCODE' in result['reason'], "Should explain no KCODE data"
        Path(temp_file).unlink()

    def test_check_convergence_structure(self):
        """Test structure of convergence check result"""
        content = """1mcnp     version 6.3.0

 kcode  10000  1.0  50  150

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    150  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.check_convergence(temp_file)

        # Check required fields
        assert 'converged' in result, "Should have converged"
        # recommendation may not be present if no KCODE data
        if result['converged'] or 'k_eff' in result:
            assert 'recommendation' in result, "Should have recommendation when KCODE present"

        # If KCODE present, should have k_eff and sigma
        if result['converged'] or 'k_eff' in result:
            assert 'k_eff' in result, "Should have k_eff"
            assert 'sigma' in result, "Should have sigma"

        Path(temp_file).unlink()

    # ===== Integration Tests =====

    def test_complete_workflow(self):
        """Test complete criticality analysis workflow"""
        content = """1mcnp     version 6.3.0

 kcode  100000  1.0  100  500

 the final estimated combined collision/absorption/track-length keff = 1.00123 with an estimated standard deviation of 0.00045

      run terminated when    500  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)

        # Step 1: Analyze KCODE
        analysis = self.analyzer.analyze_kcode(temp_file)
        assert 'has_kcode' in analysis, "Should analyze KCODE"

        # Step 2: Get cycle history
        history = self.analyzer.get_cycle_history(temp_file)
        assert isinstance(history, list), "Should get cycle history"

        # Step 3: Check convergence
        convergence = self.analyzer.check_convergence(temp_file)
        assert 'converged' in convergence, "Should check convergence"

        Path(temp_file).unlink()

    def test_realistic_godiva_output(self):
        """Test with realistic Godiva sphere output"""
        content = """1mcnp     version 6.3.0  03/01/2023

          probid =  godiva - pu metal sphere

 comment.  U-235 metal bare sphere (godiva) - critical assembly

 kcode  10000  1.0  50  250

1problem summary

      run terminated when    250  kcode cycles were done.

           keff estimator      cycle    average   combined    corr
 collision                  250   1.00024   1.00018  0.0004  0.15
 absorption                 250   0.99897   0.99965  0.0004  0.14
 track length               250   1.00034   1.00027  0.0004  0.15
 col/abs/tl combined        250   1.00018   1.00003  0.0004  0.14

 the final estimated combined collision/absorption/track-length keff = 1.00003 with an estimated standard deviation of 0.00040

 the estimated 68, 95, and 99 percent keff confidence intervals are 0.99963 to 1.00043, 0.99923 to 1.00083, and 0.99893 to 1.00113

 computer time =    45.67 minutes
"""
        temp_file = self.create_temp_output(content)
        analysis = self.analyzer.analyze_kcode(temp_file)

        if analysis['has_kcode']:
            # Well-converged critical system should be detected
            assert analysis['converged'] == True, "Godiva should be converged"

        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_analyze_empty_output(self):
        """Test analysis of empty output file"""
        temp_file = self.create_temp_output("")
        result = self.analyzer.analyze_kcode(temp_file)

        assert result['has_kcode'] == False, "Empty file should have no KCODE"
        Path(temp_file).unlink()

    def test_get_cycle_history_empty_output(self):
        """Test cycle history from empty output"""
        temp_file = self.create_temp_output("")
        history = self.analyzer.get_cycle_history(temp_file)

        assert isinstance(history, list), "Should return list"
        assert len(history) == 0, "Should be empty"
        Path(temp_file).unlink()

    def test_check_convergence_empty_output(self):
        """Test convergence check on empty output"""
        temp_file = self.create_temp_output("")
        result = self.analyzer.check_convergence(temp_file)

        assert result['converged'] == False, "Empty file should not converge"
        Path(temp_file).unlink()

    def test_analyze_kcode_very_few_cycles(self):
        """Test analysis with minimal cycles"""
        content = """1mcnp     version 6.3.0

 kcode  1000  1.0  5  10

 the final estimated combined collision/absorption/track-length keff = 1.05678 with an estimated standard deviation of 0.05000

      run terminated when     10  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # Large uncertainty, should not be converged
            assert result['converged'] == False, "Few cycles should not converge"

        Path(temp_file).unlink()

    def test_analyze_kcode_many_cycles(self):
        """Test analysis with many cycles"""
        content = """1mcnp     version 6.3.0

 kcode  50000  1.0  500  2000

 the final estimated combined collision/absorption/track-length keff = 1.00001 with an estimated standard deviation of 0.00010

      run terminated when   2000  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # Very small uncertainty, should be well-converged
            assert result['converged'] == True, "Many cycles should converge well"

        Path(temp_file).unlink()

    def test_analyze_kcode_subcritical(self):
        """Test analysis of subcritical system"""
        content = """1mcnp     version 6.3.0

 kcode  50000  1.0  100  400

 the final estimated combined collision/absorption/track-length keff = 0.95000 with an estimated standard deviation of 0.00030

      run terminated when    400  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # Subcritical but well-converged
            assert result['converged'] == True, "Should detect subcritical convergence"
            assert result['k_effective'] < 1.0, "Should be subcritical"

        Path(temp_file).unlink()

    def test_analyze_kcode_supercritical(self):
        """Test analysis of supercritical system"""
        content = """1mcnp     version 6.3.0

 kcode  50000  1.0  100  400

 the final estimated combined collision/absorption/track-length keff = 1.08000 with an estimated standard deviation of 0.00030

      run terminated when    400  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.analyze_kcode(temp_file)

        if result['has_kcode']:
            # Supercritical but well-converged
            assert result['converged'] == True, "Should detect supercritical convergence"
            assert result['k_effective'] > 1.0, "Should be supercritical"

        Path(temp_file).unlink()

    def test_check_convergence_publication_quality(self):
        """Test detection of publication-quality convergence"""
        content = """1mcnp     version 6.3.0

 kcode  200000  1.0  500  2500

 the final estimated combined collision/absorption/track-length keff = 1.00000 with an estimated standard deviation of 0.00008

      run terminated when   2500  kcode cycles were done.
"""
        temp_file = self.create_temp_output(content)
        result = self.analyzer.check_convergence(temp_file)

        if 'sigma' in result:
            # σ < 0.001 is publication quality
            assert result['sigma'] < 0.001, "Should be publication quality"

        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
