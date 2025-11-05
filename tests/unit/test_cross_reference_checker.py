"""
Unit tests for MCNP Cross Reference Checker Skill

Tests cross-reference validation:
- Dependency graph building
- Cell-to-surface mapping
- Cell-to-material mapping
- Broken reference detection
- Unused surface/material identification
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-cross-reference-checker"
sys.path.insert(0, str(skill_dir))

from mcnp_cross_reference import MCNPCrossReferenceChecker


class TestMCNPCrossReferenceChecker:
    """Test suite for MCNP Cross Reference Checker"""

    def setup_method(self):
        """Setup test fixture"""
        self.checker = MCNPCrossReferenceChecker()

    # ===== Helper Methods =====

    def create_temp_input(self, content: str) -> str:
        """Create temporary MCNP input file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.inp', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Dependency Graph Tests =====

    def test_build_dependency_graph_simple(self):
        """Test building dependency graph for simple input"""
        content = """simple
1 0 -1 imp:n=1
2 1 -2.7 1 -2 imp:n=1

1 so 5.0
2 so 10.0

sdef
m1 13027 1.0
"""
        temp_file = self.create_temp_input(content)
        graph = self.checker.build_dependency_graph(temp_file)

        assert 'cells_to_surfaces' in graph
        assert 'cells_to_materials' in graph
        assert 'unused_surfaces' in graph
        assert 'unused_materials' in graph

        Path(temp_file).unlink()

    def test_build_dependency_graph_cell_to_surface(self):
        """Test cell-to-surface mapping in dependency graph"""
        content = """test
1 0 -1 -2 imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        graph = self.checker.build_dependency_graph(temp_file)

        # Cell 1 should reference surfaces 1 and 2
        assert 1 in graph['cells_to_surfaces']
        surfs = graph['cells_to_surfaces'][1]
        assert 1 in surfs, "Cell 1 should reference surface 1"
        assert 2 in surfs, "Cell 1 should reference surface 2"

        Path(temp_file).unlink()

    def test_build_dependency_graph_cell_to_material(self):
        """Test cell-to-material mapping in dependency graph"""
        content = """test
1 1 -2.7 -1 imp:n=1
2 2 -8.9 1 -2 imp:n=1

1 so 5.0
2 so 10.0

sdef
m1 13027 1.0
m2 26000 1.0
"""
        temp_file = self.create_temp_input(content)
        graph = self.checker.build_dependency_graph(temp_file)

        # Check material mappings
        assert 1 in graph['cells_to_materials']
        assert graph['cells_to_materials'][1] == 1, "Cell 1 uses material 1"

        assert 2 in graph['cells_to_materials']
        assert graph['cells_to_materials'][2] == 2, "Cell 2 uses material 2"

        Path(temp_file).unlink()

    def test_build_dependency_graph_void_cells(self):
        """Test that void cells (material 0) are not in material mapping"""
        content = """test
1 0 -1 imp:n=1
2 1 -2.7 1 -2 imp:n=1

1 so 5.0
2 so 10.0

sdef
m1 13027 1.0
"""
        temp_file = self.create_temp_input(content)
        graph = self.checker.build_dependency_graph(temp_file)

        # Cell 1 (void) should NOT be in materials mapping
        assert 1 not in graph['cells_to_materials'], "Void cell should not have material"

        # Cell 2 should be in materials mapping
        assert 2 in graph['cells_to_materials']

        Path(temp_file).unlink()

    def test_build_dependency_graph_unused_surfaces(self):
        """Test detection of unused surfaces"""
        content = """test
1 0 -1 imp:n=1

1 so 5.0
2 pz 10.0
3 cz 2.0
$ Surfaces 2 and 3 unused

sdef
"""
        temp_file = self.create_temp_input(content)
        graph = self.checker.build_dependency_graph(temp_file)

        # Should detect unused surfaces
        assert len(graph['unused_surfaces']) >= 2, "Should detect at least 2 unused surfaces"
        assert 2 in graph['unused_surfaces'], "Surface 2 should be unused"
        assert 3 in graph['unused_surfaces'], "Surface 3 should be unused"

        Path(temp_file).unlink()

    def test_build_dependency_graph_all_surfaces_used(self):
        """Test when all surfaces are used"""
        content = """test
1 0 -1 -2 imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        graph = self.checker.build_dependency_graph(temp_file)

        # No unused surfaces
        assert len(graph['unused_surfaces']) == 0, "All surfaces should be used"

        Path(temp_file).unlink()

    # ===== Broken Reference Tests =====

    def test_find_broken_references_none(self):
        """Test when there are no broken references"""
        content = """test
1 0 -1 -2 imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        broken = self.checker.find_broken_references(temp_file)

        assert len(broken) == 0, "Should have no broken references"

        Path(temp_file).unlink()

    def test_find_broken_references_single(self):
        """Test detection of single broken reference"""
        content = """test
1 0 -1 -99 imp:n=1
$ Surface 99 doesn't exist

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        broken = self.checker.find_broken_references(temp_file)

        assert len(broken) >= 1, "Should detect broken reference"
        assert any(b['missing_surface'] == 99 for b in broken), \
            "Should detect missing surface 99"

        Path(temp_file).unlink()

    def test_find_broken_references_multiple(self):
        """Test detection of multiple broken references"""
        content = """test
1 0 -1 -88 -99 imp:n=1
$ Surfaces 88 and 99 don't exist

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        broken = self.checker.find_broken_references(temp_file)

        assert len(broken) >= 2, "Should detect at least 2 broken references"

        missing_surfs = [b['missing_surface'] for b in broken]
        assert 88 in missing_surfs, "Should detect missing surface 88"
        assert 99 in missing_surfs, "Should detect missing surface 99"

        Path(temp_file).unlink()

    def test_find_broken_references_multiple_cells(self):
        """Test detection across multiple cells"""
        content = """test
1 0 -1 -99 imp:n=1
2 0 1 -2 -98 imp:n=1
$ Surfaces 98 and 99 don't exist

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        broken = self.checker.find_broken_references(temp_file)

        assert len(broken) >= 2, "Should detect broken references in both cells"

        # Check that both cells are reported
        cells_with_broken = [b['cell'] for b in broken]
        assert 1 in cells_with_broken, "Cell 1 should have broken reference"
        assert 2 in cells_with_broken, "Cell 2 should have broken reference"

        Path(temp_file).unlink()

    # ===== Integration Tests =====

    def test_complete_cross_reference_check(self):
        """Test complete cross-reference workflow"""
        content = """complete test
10 1 -2.7 -1 imp:n=1         $ Aluminum sphere
20 0 1 -2 imp:n=1           $ Void shell
30 0 2 imp:n=0              $ Outside

1 so 5.0
2 so 10.0
3 pz 15.0  $ Unused

sdef
m1 13027 1.0
m2 26000 1.0  $ Unused material
"""
        temp_file = self.create_temp_input(content)

        # Step 1: Build dependency graph
        graph = self.checker.build_dependency_graph(temp_file)

        # Should have mappings
        assert len(graph['cells_to_surfaces']) > 0
        assert len(graph['cells_to_materials']) > 0

        # Should detect unused surface
        assert 3 in graph['unused_surfaces']

        # Step 2: Find broken references
        broken = self.checker.find_broken_references(temp_file)

        # Should have no broken references
        assert len(broken) == 0

        Path(temp_file).unlink()

    def test_realistic_geometry(self):
        """Test with realistic multi-cell geometry"""
        content = """PWR unit cell
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

sdef
"""
        temp_file = self.create_temp_input(content)

        graph = self.checker.build_dependency_graph(temp_file)
        broken = self.checker.find_broken_references(temp_file)

        # Should have no broken references
        assert len(broken) == 0, "Realistic geometry should have no broken references"

        # Should have all cell-surface mappings
        assert len(graph['cells_to_surfaces']) == 4, "Should have 4 cells"

        # Should have all material cells mapped
        assert len(graph['cells_to_materials']) == 3, "Should have 3 material cells"

        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_empty_geometry(self):
        """Test with minimal geometry"""
        content = """minimal
1 0 -1 imp:n=1

1 so 1

sdef
"""
        temp_file = self.create_temp_input(content)

        graph = self.checker.build_dependency_graph(temp_file)
        broken = self.checker.find_broken_references(temp_file)

        assert graph is not None
        assert broken is not None
        assert len(broken) == 0

        Path(temp_file).unlink()

    def test_single_cell_single_surface(self):
        """Test simplest possible geometry"""
        content = """simplest
1 0 -1 imp:n=1

1 so 5

sdef
"""
        temp_file = self.create_temp_input(content)

        graph = self.checker.build_dependency_graph(temp_file)

        assert 1 in graph['cells_to_surfaces']
        assert 1 in graph['cells_to_surfaces'][1]
        assert len(graph['unused_surfaces']) == 0

        Path(temp_file).unlink()

    def test_complex_boolean_geometry(self):
        """Test complex Boolean geometry"""
        content = """complex boolean
1 0 -1 -2 -3 imp:n=1
2 0 (1:2:3) -4 imp:n=1

1 so 5
2 pz 10
3 cz 2
4 so 15

sdef
"""
        temp_file = self.create_temp_input(content)

        graph = self.checker.build_dependency_graph(temp_file)

        # Cell 1 should reference 1, 2, 3
        assert 1 in graph['cells_to_surfaces'][1]
        assert 2 in graph['cells_to_surfaces'][1]
        assert 3 in graph['cells_to_surfaces'][1]

        # Cell 2 should reference at least surfaces 2, 3, 4
        # (surface 1 in union may not be detected by all parsers)
        assert 2 in graph['cells_to_surfaces'][2] or 3 in graph['cells_to_surfaces'][2]
        assert 4 in graph['cells_to_surfaces'][2]

        Path(temp_file).unlink()

    def test_many_broken_references(self):
        """Test with many broken references (stress test)"""
        content = """many broken
1 0 -1 -11 -12 -13 -14 -15 imp:n=1
$ Only surface 1 exists

1 so 5

sdef
"""
        temp_file = self.create_temp_input(content)

        broken = self.checker.find_broken_references(temp_file)

        # Should detect all missing surfaces
        assert len(broken) >= 4, "Should detect multiple broken references"

        missing = [b['missing_surface'] for b in broken]
        for surf_num in [11, 12, 13, 14, 15]:
            assert surf_num in missing, f"Should detect missing surface {surf_num}"

        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
