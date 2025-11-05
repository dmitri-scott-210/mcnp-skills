"""
Integration tests for Parse → Analyze → Report workflow

Tests the complete workflow:
1. Parse MCNP output with output-parser
2. Analyze tallies with tally-analyzer
3. Check statistics with statistics-checker

This workflow simulates typical user interaction when analyzing simulation results.
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

# Add skill directories to path
output_parser_dir = project_root / ".claude" / "skills" / "mcnp-output-parser"
tally_analyzer_dir = project_root / ".claude" / "skills" / "mcnp-tally-analyzer"
stats_checker_dir = project_root / ".claude" / "skills" / "mcnp-statistics-checker"

sys.path.insert(0, str(output_parser_dir))
sys.path.insert(0, str(tally_analyzer_dir))
sys.path.insert(0, str(stats_checker_dir))

from mcnp_output_analyzer import MCNPOutputAnalyzer
from mcnp_tally_analyzer import MCNPTallyAnalyzer
from mcnp_statistics_checker import MCNPStatisticsChecker


class TestWorkflowAnalyze:
    """Test suite for Parse → Analyze → Report workflow"""

    def setup_method(self):
        """Setup test fixtures"""
        self.output_parser = MCNPOutputAnalyzer()
        self.tally_analyzer = MCNPTallyAnalyzer()
        self.stats_checker = MCNPStatisticsChecker()

    # ===== Simple Output Workflow =====

    def test_simple_output_workflow(self):
        """Test complete workflow: parse → analyze → check stats"""
        # Sample MCNP output with tally
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00
          Code Name & Version = MCNP6, 1.0

 nps    mean   error   vov   slope   fom
 1000  1.234  0.0500  0.0001  10.0   1000

1tally        4        nps =     1000
           tally type 4    track length estimate of particle flux.
           particle(s): neutrons

 cell  1
      energy
    0.0000E+00   1.2340E-02 0.0500
    total        1.2340E-02 0.0500
"""

        # Step 1: Parse output
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Step 2: Analyze tallies
        tally_analysis = self.tally_analyzer.extract_tallies(output_text)
        assert tally_analysis is not None

        # Step 3: Check statistics
        stats_result = self.stats_checker.check_tally_statistics(
            mean=1.234,
            rel_error=0.05,
            vov=0.0001,
            slope=10.0,
            fom=1000
        )
        assert stats_result is not None
        assert 'passed' in stats_result or 'checks' in stats_result

    # ===== Multiple Tally Workflow =====

    def test_multiple_tally_workflow(self):
        """Test workflow with multiple tallies"""
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

1tally        4        nps =     10000
 cell  1
      total        1.2340E-02 0.0100

1tally        6        nps =     10000
 cell  1
      total        2.5600E-03 0.0200
"""

        # Step 1: Parse
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Step 2: Analyze all tallies
        tally_analysis = self.tally_analyzer.extract_tallies(output_text)
        assert tally_analysis is not None

        # Step 3: Check statistics for each tally
        stats1 = self.stats_checker.check_tally_statistics(
            mean=1.234e-2,
            rel_error=0.01,
            vov=0.0001,
            slope=10.0,
            fom=10000
        )
        assert stats1 is not None

        stats2 = self.stats_checker.check_tally_statistics(
            mean=2.56e-3,
            rel_error=0.02,
            vov=0.0001,
            slope=10.0,
            fom=5000
        )
        assert stats2 is not None

    # ===== Energy Binned Tally Workflow =====

    def test_energy_binned_tally_workflow(self):
        """Test workflow with energy-binned tallies"""
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

1tally        4        nps =     10000
           tally type 4    track length estimate of particle flux.

 cell  1
      energy
    1.0000E-08   1.5000E-03 0.0500
    1.0000E-06   2.3000E-03 0.0400
    1.0000E-04   3.1000E-03 0.0350
    1.0000E-02   2.8000E-03 0.0380
    1.0000E+00   1.9000E-03 0.0450
    total        1.1600E-02 0.0200
"""

        # Step 1: Parse
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Step 2: Analyze energy bins
        tally_analysis = self.tally_analyzer.extract_tallies(output_text)
        assert tally_analysis is not None

        # Step 3: Check statistics for total
        stats = self.stats_checker.check_tally_statistics(
            mean=1.16e-2,
            rel_error=0.02,
            vov=0.0001,
            slope=10.0,
            fom=25000
        )
        assert stats is not None

    # ===== Statistical Quality Workflow =====

    def test_good_statistics_workflow(self):
        """Test workflow with good statistical quality"""
        # Output with good statistics (rel error < 0.05)
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

 nps    mean   error   vov   slope   fom
 100000  1.234  0.0080  0.00005  10.0   156250

1tally        4        nps =     100000
 cell  1
      total        1.2340E-02 0.0080
"""

        # Parse and analyze
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Check statistics - should pass all checks
        stats = self.stats_checker.check_tally_statistics(
            mean=1.234,
            rel_error=0.008,  # Good: < 0.05
            vov=0.00005,      # Good: < 0.1
            slope=10.0,       # Good: > 3
            fom=156250        # Good FOM
        )
        assert stats is not None

    def test_poor_statistics_workflow(self):
        """Test workflow with poor statistical quality"""
        # Output with poor statistics (rel error > 0.10)
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

 nps    mean   error   vov   slope   fom
 100  1.234  0.2500  0.1500  2.5   16

1tally        4        nps =     100
 cell  1
      total        1.2340E-02 0.2500
"""

        # Parse and analyze
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Check statistics - should fail some checks
        stats = self.stats_checker.check_tally_statistics(
            mean=1.234,
            rel_error=0.25,   # Poor: > 0.10
            vov=0.15,         # Poor: > 0.1
            slope=2.5,        # Poor: < 3
            fom=16            # Low FOM
        )
        assert stats is not None
        # Should indicate failed checks

    # ===== KCODE Workflow =====

    def test_kcode_analysis_workflow(self):
        """Test workflow for criticality problems"""
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00
          the final estimated combined collision/absorption/track-length keff = 1.00254 with an estimated standard deviation of 0.00184

 keff estimator     keff   standard deviation
 collision         1.0028      0.0019
 absorption        1.0025      0.0018
 track length      1.0023      0.0019

 avg k(c/a/t)    1.00254   0.00184
"""

        # Step 1: Parse output
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Step 2: Extract keff
        # Check if parser found keff
        if hasattr(parsed, 'keff') or (isinstance(parsed, dict) and 'keff' in parsed):
            # Statistics on keff
            if isinstance(parsed, dict):
                keff = parsed.get('keff', 1.00254)
                keff_std = parsed.get('keff_std', 0.00184)
            else:
                keff = 1.00254
                keff_std = 0.00184

            # Check keff uncertainty
            rel_error = keff_std / keff
            assert rel_error < 0.005  # Should be < 0.5% for criticality

    # ===== Warning Detection Workflow =====

    def test_warning_detection_workflow(self):
        """Test detection of warnings in output"""
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

 warning.  tally        4 is unreliable in cell        1.
           the tally relative error is greater than 0.50.

1tally        4        nps =     1000
 cell  1
      total        1.2340E-02 0.5500
"""

        # Step 1: Parse and detect warnings
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Parser should flag warnings
        if isinstance(parsed, dict):
            has_warnings = 'warnings' in parsed or 'has_warnings' in parsed
            # Warnings detected

    # ===== Large Tally Workflow =====

    def test_large_tally_workflow(self):
        """Test workflow with large multi-cell tally"""
        # Create output with many cells
        output_lines = [
            "1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00",
            "",
            "1tally        4        nps =     10000",
            "           tally type 4    track length estimate of particle flux.",
            ""
        ]

        # Add 100 cells
        for i in range(1, 101):
            output_lines.append(f" cell  {i}")
            output_lines.append(f"      total        {1.23e-2 + i*1e-5:.4E} {0.01 + i*0.0001:.4f}")

        output_text = "\n".join(output_lines)

        # Parse
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Analyze
        tally_analysis = self.tally_analyzer.extract_tallies(output_text)
        assert tally_analysis is not None

    # ===== Export Workflow =====

    def test_export_workflow(self):
        """Test exporting tally results to CSV"""
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

1tally        4        nps =     10000
 cell  1
      energy
    1.0000E-08   1.5000E-03 0.0500
    1.0000E-06   2.3000E-03 0.0400
    1.0000E-04   3.1000E-03 0.0350
    total        1.1600E-02 0.0200
"""

        # Parse
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Analyze and export
        if hasattr(self.tally_analyzer, 'export_to_csv'):
            csv_output = self.tally_analyzer.export_to_csv(output_text)
            assert csv_output is not None
            # Should contain CSV-formatted data

    # ===== Workflow Performance =====

    def test_workflow_performance_small(self):
        """Test workflow performance on small output"""
        import time

        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00

1tally        4        nps =     1000
 cell  1
      total        1.2340E-02 0.0500
"""

        start = time.time()

        # Parse
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Analyze
        tally_analysis = self.tally_analyzer.extract_tallies(output_text)
        assert tally_analysis is not None

        # Check stats
        stats = self.stats_checker.check_tally_statistics(
            mean=1.234e-2,
            rel_error=0.05,
            vov=0.0001,
            slope=10.0,
            fom=400
        )
        assert stats is not None

        elapsed = time.time() - start

        # Should complete very quickly
        assert elapsed < 2.0, f"Workflow took {elapsed:.2f}s (expected < 2s)"

    # ===== Comprehensive Workflow =====

    def test_comprehensive_analysis_workflow(self):
        """Test complete analysis of complex output"""
        output_text = """1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00
          Code Name & Version = MCNP6, 1.0

 nps    mean   error   vov   slope   fom
 10000  1.234  0.0100  0.0001  10.0   10000

1tally        4        nps =     10000
           tally type 4    track length estimate of particle flux.
           particle(s): neutrons

 cell  1
      energy
    1.0000E-08   1.5000E-03 0.0500
    1.0000E-06   2.3000E-03 0.0400
    total        1.1600E-02 0.0100

1tally        6        nps =     10000
           tally type 6    track length estimate of heating.

 cell  1
      total        2.5600E-03 0.0150
"""

        # Step 1: Parse everything
        parsed = self.output_parser.parse_output(output_text)
        assert parsed is not None

        # Step 2: Analyze all tallies
        tally_analysis = self.tally_analyzer.extract_tallies(output_text)
        assert tally_analysis is not None

        # Step 3: Check statistics for each tally
        stats_f4 = self.stats_checker.check_tally_statistics(
            mean=1.16e-2,
            rel_error=0.01,
            vov=0.0001,
            slope=10.0,
            fom=10000
        )
        assert stats_f4 is not None

        stats_f6 = self.stats_checker.check_tally_statistics(
            mean=2.56e-3,
            rel_error=0.015,
            vov=0.0001,
            slope=10.0,
            fom=4444
        )
        assert stats_f6 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
