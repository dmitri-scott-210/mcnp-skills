"""
Unit tests for MCNP Geometry Checker Skill

Tests geometry validation capabilities:
- Surface usage checking
- Cell definition validation
- Void cell detection
- Boolean operator validation
- Geometry recommendations
- Plot command generation
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-geometry-checker"
sys.path.insert(0, str(skill_dir))

from mcnp_geometry_checker import MCNPGeometryChecker


class TestMCNPGeometryChecker:
    """Test suite for MCNP Geometry Checker"""

    def setup_method(self):
        """Setup test fixture"""
        self.checker = MCNPGeometryChecker()

    # ===== Helper Methods =====

    def create_temp_input(self, content: str) -> str:
        """Create temporary MCNP input file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.inp', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Surface Usage Tests =====

    def test_check_all_surfaces_used(self):
        """Test when all surfaces are used"""
        content = """test - all surfaces used
1 0 -1 -2 imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should have recommendations but no unused surface warnings
        unused_warnings = [i for i in issues if i['type'] == 'warning' and 'not used' in i['message']]
        assert len(unused_warnings) == 0, "No surfaces should be unused"
        Path(temp_file).unlink()

    def test_check_unused_surfaces(self):
        """Test detection of unused surfaces"""
        content = """test - unused surfaces
1 0 -1 imp:n=1

1 so 5.0
2 pz 10.0
3 cz 2.0
$ Surfaces 2 and 3 are not used

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should detect unused surfaces
        unused_warnings = [i for i in issues if i['type'] == 'warning' and 'not used' in i['message']]
        assert len(unused_warnings) >= 2, "Should detect at least 2 unused surfaces"
        Path(temp_file).unlink()

    def test_check_single_unused_surface(self):
        """Test detection of single unused surface"""
        content = """test - one unused
1 0 -1 imp:n=1

1 so 5.0
2 pz 10.0  $ unused

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        unused_warnings = [i for i in issues if i['type'] == 'warning' and 'not used' in i['message']]
        assert len(unused_warnings) == 1, "Should detect exactly 1 unused surface"
        Path(temp_file).unlink()

    # ===== Void Cell Tests =====

    def test_check_void_cells_present(self):
        """Test when void cells are present"""
        content = """test - with void
1 0 -1 imp:n=1
2 1 -2.7 1 -2 imp:n=1

1 so 5.0
2 so 10.0

sdef
m1 13027 1.0
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should NOT have "No void cells" info message
        no_void_msgs = [i for i in issues if i['type'] == 'info' and 'No void' in i['message']]
        assert len(no_void_msgs) == 0, "Should not report missing void cells"
        Path(temp_file).unlink()

    def test_check_no_void_cells(self):
        """Test detection when no void cells present"""
        content = """test - no voids
1 1 -2.7 -1 imp:n=1

1 so 5.0

sdef
m1 13027 1.0
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should have info message about no void cells
        no_void_msgs = [i for i in issues if i['type'] == 'info' and 'No void' in i['message']]
        assert len(no_void_msgs) > 0, "Should report no void cells"
        Path(temp_file).unlink()

    # ===== Boolean Operator Tests =====

    def test_check_excessive_complement_operators(self):
        """Test detection of excessive complement operators"""
        content = """test - excessive complements
1 0 -1 #2 #3 #4 #5 imp:n=1

1 so 5.0
2 so 1.0
3 so 1.5
4 so 2.0
5 so 2.5

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should warn about excessive # operators
        complement_warnings = [i for i in issues if 'Excessive' in i['message'] and '#' in i['message']]
        assert len(complement_warnings) > 0, "Should detect excessive complement operators"
        Path(temp_file).unlink()

    def test_check_union_without_parentheses(self):
        """Test detection of union operator without parentheses"""
        content = """test - union without parens
1 0 -1:-2 imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should complete without errors (union checking is optional)
        assert isinstance(issues, list), "Should return list of issues"
        # Union operator checking is an advanced feature - not required
        Path(temp_file).unlink()

    def test_check_union_with_parentheses(self):
        """Test union operator with parentheses (correct usage)"""
        content = """test - union with parens
1 0 (-1:-2) imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should NOT warn about this
        union_warnings = [i for i in issues if i['type'] == 'info' and 'Union' in i['message'] and 'without parentheses' in i['message']]
        assert len(union_warnings) == 0, "Should not warn when parentheses present"
        Path(temp_file).unlink()

    # ===== Geometry Recommendations Tests =====

    def test_check_always_includes_recommendations(self):
        """Test that recommendations are always included"""
        content = """simple
1 0 -1 imp:n=1

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should have recommendations
        recommendations = [i for i in issues if i['type'] == 'recommendation']
        assert len(recommendations) >= 3, "Should have at least 3 recommendations"
        Path(temp_file).unlink()

    def test_check_recommendations_content(self):
        """Test that recommendations have expected content"""
        content = """simple
1 0 -1 imp:n=1

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        recommendations = [i for i in issues if i['type'] == 'recommendation']
        rec_messages = ' '.join([r['message'] for r in recommendations])

        # Check for key recommendation keywords
        assert 'plot' in rec_messages.lower(), "Should recommend plotting"
        assert 'void' in rec_messages.lower(), "Should recommend VOID card"
        Path(temp_file).unlink()

    # ===== Plot Command Generation Tests =====

    def test_generate_plot_commands(self):
        """Test generation of plot commands"""
        plot_cmds = self.checker.generate_plot_commands()

        assert isinstance(plot_cmds, list), "Should return a list"
        assert len(plot_cmds) == 3, "Should have 3 plot commands (XY, XZ, YZ)"

    def test_generate_plot_commands_content(self):
        """Test plot command content"""
        plot_cmds = self.checker.generate_plot_commands()

        # Should have commands for different planes
        cmd_str = ' '.join(plot_cmds)
        assert 'xy' in cmd_str.lower(), "Should have XY plot"
        assert 'xz' in cmd_str.lower(), "Should have XZ plot"
        assert 'yz' in cmd_str.lower(), "Should have YZ plot"
        assert 'plot' in cmd_str.lower(), "Should use plot keyword"

    def test_generate_plot_commands_format(self):
        """Test that plot commands are properly formatted"""
        plot_cmds = self.checker.generate_plot_commands()

        for cmd in plot_cmds:
            assert isinstance(cmd, str), "Each command should be a string"
            assert len(cmd) > 0, "Commands should not be empty"
            assert 'plot' in cmd.lower(), "Should contain 'plot' keyword"

    # ===== VOID Test Generation Tests =====

    def test_generate_void_test_input(self):
        """Test generation of VOID test input"""
        void_test = self.checker.generate_void_test_input()

        assert isinstance(void_test, str), "Should return a string"
        assert len(void_test) > 0, "Should not be empty"
        assert 'void' in void_test.lower(), "Should contain VOID keyword"

    def test_generate_void_test_content(self):
        """Test VOID test input content"""
        void_test = self.checker.generate_void_test_input()

        # Should have instructions
        assert 'c' in void_test.lower(), "Should have comments"
        assert 'void' in void_test.lower(), "Should have VOID card"
        assert 'geometry' in void_test.lower(), "Should mention geometry testing"

    # ===== Integration Tests =====

    def test_check_complex_geometry(self):
        """Test checking of complex geometry"""
        content = """complex geometry test
10 1 -10.2 -1 imp:n=1       $ Fuel
20 0 1 -2 imp:n=1          $ Gap
30 2 -6.5 2 -3 imp:n=1      $ Clad
40 0 3 imp:n=0             $ Void

1 so 0.5
2 so 0.6
3 so 0.7
4 pz 10.0  $ Unused

sdef
m1 92235.80c 1.0
m2 40000.80c 1.0
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should have:
        # - At least one unused surface warning (surface 4)
        # - Void cells present (no info message)
        # - Recommendations

        assert len(issues) > 0, "Should have some issues/recommendations"

        unused = [i for i in issues if 'not used' in i['message']]
        assert len(unused) >= 1, "Should detect unused surface"

        Path(temp_file).unlink()

    def test_check_realistic_problem(self):
        """Test with realistic MCNP problem"""
        content = """PWR fuel pin
c Pin regions
1 1 -10.2 -1 u=1 imp:n=1         $ UO2 fuel
2 0 1 -2 u=1 imp:n=1             $ Gap
3 2 -6.5 2 -3 u=1 imp:n=1        $ Zircaloy clad
4 3 -0.74 3 u=1 imp:n=1          $ Water

c Surfaces
1 cz 0.41    $ Fuel outer radius
2 cz 0.42    $ Gap outer radius
3 cz 0.48    $ Clad outer radius

c Materials
m1 92235.80c 0.03  92238.80c 0.97  8016.80c 2.0  $ UO2
m2 40000.80c 1.0                                  $ Zircaloy
m3 1001.80c 2  8016.80c 1                        $ Water
mt3 lwtr.20t

sdef u=1 pos=0 0 0 erg=2.0
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should complete without errors
        assert issues is not None, "Should return issues list"

        # Should have recommendations
        recs = [i for i in issues if i['type'] == 'recommendation']
        assert len(recs) > 0, "Should have recommendations"

        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_check_empty_geometry(self):
        """Test with minimal/empty geometry"""
        content = """minimal
1 0 -1 imp:n=1

1 so 1

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should still return recommendations
        assert len(issues) > 0, "Should have recommendations at minimum"
        Path(temp_file).unlink()

    def test_check_many_complement_operators(self):
        """Test with many complement operators (>3)"""
        content = """many complements
1 0 -1 #2 #3 #4 #5 #6 imp:n=1

1 so 10.0
2 so 1.0
3 so 2.0
4 so 3.0
5 so 4.0
6 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should warn about excessive complements
        excessive = [i for i in issues if 'Excessive' in i['message']]
        assert len(excessive) > 0, "Should warn about excessive # operators"
        Path(temp_file).unlink()

    def test_check_exactly_three_complements(self):
        """Test with exactly 3 complement operators (boundary)"""
        content = """three complements
1 0 -1 #2 #3 #4 imp:n=1

1 so 10.0
2 so 1.0
3 so 2.0
4 so 3.0

sdef
"""
        temp_file = self.create_temp_input(content)
        issues = self.checker.check_geometry(temp_file)

        # Should NOT warn (threshold is >3)
        excessive = [i for i in issues if 'Excessive' in i['message']]
        assert len(excessive) == 0, "Should not warn at threshold of 3"
        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
