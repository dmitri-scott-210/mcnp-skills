"""
Integration tests for Large File Handling

Tests performance on files of different sizes:
- Baseline: 1,000 lines (<1s)
- Typical Reactor: 5,000 lines (<5s)
- HFIR Benchmark: 10,000+ lines (<10s)

This validates that skills can handle realistic large MCNP inputs efficiently.
"""
import pytest
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

# Add skill directories to path
input_validator_dir = project_root / ".claude" / "skills" / "mcnp-input-validator"
geometry_checker_dir = project_root / ".claude" / "skills" / "mcnp-geometry-checker"
output_parser_dir = project_root / ".claude" / "skills" / "mcnp-output-parser"

sys.path.insert(0, str(input_validator_dir))
sys.path.insert(0, str(geometry_checker_dir))
sys.path.insert(0, str(output_parser_dir))

from mcnp_input_validator import MCNPInputValidator
from mcnp_geometry_checker import MCNPGeometryChecker
from mcnp_output_analyzer import MCNPOutputAnalyzer


class TestLargeFiles:
    """Test suite for large file handling performance"""

    def setup_method(self):
        """Setup test fixtures"""
        self.validator = MCNPInputValidator()
        self.geo_checker = MCNPGeometryChecker()
        self.output_parser = MCNPOutputAnalyzer()

    # ===== Helper Methods =====

    def generate_large_input(self, n_cells, n_surfaces, n_materials):
        """Generate large MCNP input for testing"""
        lines = ["Large MCNP Input Test", "c Cell cards"]

        # Generate cells
        for i in range(1, n_cells + 1):
            mat = (i % n_materials) + 1
            surf = i
            density = -1.0 - (i * 0.01)
            lines.append(f"{i} {mat} {density} -{surf}")

        # Void cell
        lines.append(f"{n_cells + 1} 0 {n_cells}")

        lines.append("")
        lines.append("c Surface cards")

        # Generate surfaces (concentric spheres)
        for i in range(1, n_surfaces + 1):
            radius = 1.0 + (i * 0.5)
            lines.append(f"{i} so {radius:.2f}")

        lines.append("")
        lines.append("c Data cards")
        lines.append("mode n")
        lines.append("nps 10000")
        lines.append("sdef pos=0 0 0 erg=1.0")

        # Generate materials
        for i in range(1, n_materials + 1):
            lines.append(f"m{i} 1001.80c 2 8016.80c 1  $ Water-like material {i}")

        return "\n".join(lines)

    def generate_large_output(self, n_tallies, n_bins):
        """Generate large MCNP output for testing"""
        lines = [
            "1mcnp     version 6     ld=06/06/13                     10/31/25 12:00:00",
            "          Code Name & Version = MCNP6, 1.0",
            ""
        ]

        # Generate multiple tallies
        for tally in range(1, n_tallies + 1):
            tally_num = tally * 4  # F4, F8, F12, etc.
            lines.append(f"1tally  {tally_num:6}        nps =     100000")
            lines.append("           tally type 4    track length estimate of particle flux.")
            lines.append("")
            lines.append(" cell  1")
            lines.append("      energy")

            # Generate energy bins
            energy = 1.0e-8
            for i in range(n_bins):
                value = 1.23e-3 * (1 + i * 0.1)
                error = 0.01 + (i * 0.001)
                lines.append(f"    {energy:.4E}   {value:.4E} {error:.4f}")
                energy *= 10

            # Total
            total = 1.23e-2
            total_error = 0.005
            lines.append(f"    total        {total:.4E} {total_error:.4f}")
            lines.append("")

        return "\n".join(lines)

    # ===== Baseline Tests (1,000 lines) =====

    def test_baseline_input_validation(self):
        """Test validation on 1,000 line input (<1s target)"""
        # Generate ~1,000 line input (100 cells, 100 surfaces, 10 materials)
        input_text = self.generate_large_input(n_cells=100, n_surfaces=100, n_materials=10)
        line_count = len(input_text.split('\n'))
        assert 900 <= line_count <= 1100, f"Expected ~1000 lines, got {line_count}"

        # Validate with timing
        start = time.time()
        result = self.validator.validate_input(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 1.0, f"Baseline validation took {elapsed:.2f}s (target: <1s)"

    def test_baseline_geometry_check(self):
        """Test geometry check on 1,000 line input (<1s target)"""
        input_text = self.generate_large_input(n_cells=100, n_surfaces=100, n_materials=10)

        start = time.time()
        result = self.geo_checker.check_geometry(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 1.0, f"Baseline geometry check took {elapsed:.2f}s (target: <1s)"

    def test_baseline_output_parsing(self):
        """Test output parsing on 1,000 line output (<1s target)"""
        # Generate ~1,000 line output (10 tallies, 20 bins each)
        output_text = self.generate_large_output(n_tallies=10, n_bins=20)
        line_count = len(output_text.split('\n'))
        assert 900 <= line_count <= 1100, f"Expected ~1000 lines, got {line_count}"

        start = time.time()
        result = self.output_parser.parse_output(output_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 1.0, f"Baseline output parsing took {elapsed:.2f}s (target: <1s)"

    # ===== Typical Reactor Tests (5,000 lines) =====

    def test_typical_input_validation(self):
        """Test validation on 5,000 line input (<5s target)"""
        # Generate ~5,000 line input (500 cells, 500 surfaces, 50 materials)
        input_text = self.generate_large_input(n_cells=500, n_surfaces=500, n_materials=50)
        line_count = len(input_text.split('\n'))
        assert 4500 <= line_count <= 5500, f"Expected ~5000 lines, got {line_count}"

        start = time.time()
        result = self.validator.validate_input(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 5.0, f"Typical validation took {elapsed:.2f}s (target: <5s)"

    def test_typical_geometry_check(self):
        """Test geometry check on 5,000 line input (<5s target)"""
        input_text = self.generate_large_input(n_cells=500, n_surfaces=500, n_materials=50)

        start = time.time()
        result = self.geo_checker.check_geometry(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 5.0, f"Typical geometry check took {elapsed:.2f}s (target: <5s)"

    def test_typical_output_parsing(self):
        """Test output parsing on 5,000 line output (<5s target)"""
        # Generate ~5,000 line output (50 tallies, 20 bins each)
        output_text = self.generate_large_output(n_tallies=50, n_bins=20)
        line_count = len(output_text.split('\n'))
        assert 4500 <= line_count <= 5500, f"Expected ~5000 lines, got {line_count}"

        start = time.time()
        result = self.output_parser.parse_output(output_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 5.0, f"Typical output parsing took {elapsed:.2f}s (target: <5s)"

    # ===== HFIR Benchmark Tests (10,000+ lines) =====

    def test_hfir_input_validation(self):
        """Test validation on 10,000+ line input (<10s target)"""
        # Generate ~10,000 line input (1000 cells, 1000 surfaces, 100 materials)
        input_text = self.generate_large_input(n_cells=1000, n_surfaces=1000, n_materials=100)
        line_count = len(input_text.split('\n'))
        assert line_count >= 10000, f"Expected >=10000 lines, got {line_count}"

        start = time.time()
        result = self.validator.validate_input(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 10.0, f"HFIR validation took {elapsed:.2f}s (target: <10s)"

    def test_hfir_geometry_check(self):
        """Test geometry check on 10,000+ line input (<10s target)"""
        input_text = self.generate_large_input(n_cells=1000, n_surfaces=1000, n_materials=100)

        start = time.time()
        result = self.geo_checker.check_geometry(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 10.0, f"HFIR geometry check took {elapsed:.2f}s (target: <10s)"

    def test_hfir_output_parsing(self):
        """Test output parsing on 10,000+ line output (<10s target)"""
        # Generate ~10,000 line output (100 tallies, 20 bins each)
        output_text = self.generate_large_output(n_tallies=100, n_bins=20)
        line_count = len(output_text.split('\n'))
        assert line_count >= 10000, f"Expected >=10000 lines, got {line_count}"

        start = time.time()
        result = self.output_parser.parse_output(output_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 10.0, f"HFIR output parsing took {elapsed:.2f}s (target: <10s)"

    # ===== Memory Tests =====

    def test_memory_usage_large_input(self):
        """Test memory usage stays reasonable for large inputs"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        # Generate and process large input
        input_text = self.generate_large_input(n_cells=1000, n_surfaces=1000, n_materials=100)
        result = self.validator.validate_input(input_text)
        assert result is not None

        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_used = mem_after - mem_before

        # Should use less than 500MB for this operation
        assert mem_used < 500, f"Memory usage {mem_used:.1f}MB exceeds 500MB limit"

    # ===== Scalability Tests =====

    def test_scalability_linear(self):
        """Test that performance scales approximately linearly"""
        times = []

        # Test at 100, 500, 1000 cells
        for n_cells in [100, 500, 1000]:
            input_text = self.generate_large_input(n_cells=n_cells, n_surfaces=n_cells, n_materials=10)

            start = time.time()
            result = self.validator.validate_input(input_text)
            elapsed = time.time() - start

            assert result is not None
            times.append((n_cells, elapsed))

        # Check that time doesn't explode (not O(n^2) or worse)
        # If 1000 cells takes more than 15x the time of 100 cells, something's wrong
        time_100 = times[0][1]
        time_1000 = times[2][1]

        if time_100 > 0.01:  # Only check if baseline is measurable
            ratio = time_1000 / time_100
            assert ratio < 20, f"Performance degradation too severe: {ratio:.1f}x for 10x size increase"

    # ===== Stress Tests =====

    def test_stress_many_materials(self):
        """Test handling many materials"""
        # 100 cells, 100 surfaces, 500 materials
        input_text = self.generate_large_input(n_cells=100, n_surfaces=100, n_materials=500)

        start = time.time()
        result = self.validator.validate_input(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 2.0, f"Many materials test took {elapsed:.2f}s (target: <2s)"

    def test_stress_deep_nesting(self):
        """Test handling deep cell nesting"""
        # Create input with nested universes (simulated)
        lines = ["Deep Nesting Test"]
        lines.append("c Cell cards")

        # Create 50 levels of nesting
        for i in range(1, 51):
            lines.append(f"{i} 1 -1.0 -{i} u={i} fill={i+1}")

        lines.append("51 1 -1.0 -51 u=51")  # Innermost cell

        lines.append("")
        lines.append("c Surface cards")
        for i in range(1, 52):
            lines.append(f"{i} so {i * 0.5}")

        lines.append("")
        lines.append("c Data cards")
        lines.append("mode n")
        lines.append("nps 1000")
        lines.append("m1 1001.80c 2 8016.80c 1")

        input_text = "\n".join(lines)

        start = time.time()
        result = self.validator.validate_input(input_text)
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 2.0, f"Deep nesting test took {elapsed:.2f}s (target: <2s)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
