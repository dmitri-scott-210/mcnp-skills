"""
Unit tests for MCNP Input Validator Skill

Tests validation logic for MCNP input files:
- Block structure validation
- Cross-reference checking
- Importance card validation
- Material definition checking
- Tally specification validation
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-input-validator"
sys.path.insert(0, str(skill_dir))

from mcnp_input_validator import MCNPInputValidator


class TestMCNPInputValidator:
    """Test suite for MCNP Input Validator"""

    def setup_method(self):
        """Setup test fixture"""
        self.validator = MCNPInputValidator()

    # ===== Helper Methods =====

    def create_temp_input(self, content: str) -> str:
        """Create temporary MCNP input file"""
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.inp', delete=False)
        temp.write(content)
        temp.close()
        return temp.name

    # ===== Block Structure Tests =====

    def test_validate_simple_valid_input(self):
        """Test validation of simple valid input"""
        content = """simple - test problem
1 0 -1 imp:n=1
2 0 1 imp:n=0

1 so 5.0

sdef pos=0 0 0 erg=14.1
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Simple valid input should pass validation"
        assert len(result['errors']) == 0, "No errors should be found"
        Path(temp_file).unlink()  # Clean up

    def test_validate_missing_cell_block(self):
        """Test detection of missing cell block"""
        content = """test

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Missing cell block should fail validation"
        assert any('cell' in err.lower() for err in result['errors']), \
            "Error should mention missing cells"
        Path(temp_file).unlink()

    def test_validate_missing_surface_block(self):
        """Test detection of missing surface block"""
        content = """test
1 0 -1 imp:n=1

"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Missing surface block should fail validation"
        assert any('surface' in err.lower() for err in result['errors']), \
            "Error should mention missing surfaces"
        Path(temp_file).unlink()

    def test_validate_missing_data_cards(self):
        """Test warning for minimal data cards"""
        content = """test
1 0 -1 imp:n=1

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        # Should be valid with minimal data cards
        assert result['valid'] is True, "Minimal data cards should pass validation"
        # Check that we get warnings about missing material or importance
        assert 'warnings' in result
        Path(temp_file).unlink()

    # ===== Cross-Reference Tests =====

    def test_validate_undefined_surface_reference(self):
        """Test detection of undefined surface reference"""
        content = """test - undefined surface
1 0 -1 -2 imp:n=1

1 so 5.0
$ Surface 2 is referenced but not defined

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Undefined surface should fail validation"
        assert any('undefined surface' in err.lower() for err in result['errors']), \
            "Error should mention undefined surface"
        Path(temp_file).unlink()

    def test_validate_all_surfaces_defined(self):
        """Test validation passes when all surfaces are defined"""
        content = """test - all surfaces defined
1 0 -1 -2 imp:n=1

1 so 5.0
2 pz 10.0

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "All defined surfaces should pass validation"
        Path(temp_file).unlink()

    # ===== Importance Tests =====

    def test_validate_missing_importance_cards(self):
        """Test warning for missing importance cards"""
        content = """test - no importance
1 0 -1

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Missing importance is warning, not error"
        assert any('importance' in warn.lower() for warn in result['warnings']), \
            "Warning should mention missing importance"
        Path(temp_file).unlink()

    def test_validate_zero_importance_warning(self):
        """Test warning for zero importance cells"""
        content = """test - zero importance
1 0 -1 imp:n=1
2 0 1 imp:n=0

1 so 5.0

sdef
imp:n 1 0
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Zero importance is valid but warnable"
        assert any('zero importance' in warn.lower() for warn in result['warnings']), \
            "Warning should mention zero importance"
        Path(temp_file).unlink()

    # ===== Material Tests =====

    def test_validate_undefined_material(self):
        """Test detection of undefined material reference"""
        content = """test - undefined material
1 999 -1.0 -1 imp:n=1
$ Material 999 not defined

1 so 5.0

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Undefined material should fail validation"
        assert any('undefined material' in err.lower() for err in result['errors']), \
            "Error should mention undefined material"
        Path(temp_file).unlink()

    def test_validate_defined_materials(self):
        """Test validation passes when materials are defined"""
        content = """test - material defined
1 1 -2.7 -1 imp:n=1

1 so 5.0

sdef
m1 13027 1.0  $ Aluminum
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Defined materials should pass validation"
        Path(temp_file).unlink()

    def test_validate_void_cells_no_material(self):
        """Test void cells (material 0) don't require material cards"""
        content = """test - void cells
1 0 -1 imp:n=1
2 1 -2.7 1 -2 imp:n=1

1 so 5.0
2 so 10.0

sdef
m1 13027 1.0
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Void cells should not require materials"
        Path(temp_file).unlink()

    # ===== Tally Tests =====

    def test_validate_duplicate_tally_error(self):
        """Test detection of duplicate tally definitions"""
        content = """test - duplicate tally
1 0 -1 imp:n=1

1 so 5.0

sdef
f1:n 1
f1:p 1
$ Same tally number for different particles - not allowed
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Duplicate tally should fail validation"
        assert any('tally' in err.lower() and 'multiple' in err.lower()
                   for err in result['errors']), \
            "Error should mention duplicate tally"
        Path(temp_file).unlink()

    def test_validate_unique_tallies(self):
        """Test validation passes with unique tally numbers"""
        content = """test - unique tallies
1 0 -1 imp:n=1

1 so 5.0

sdef
f1:n 1
f2:n 1
f4:n 1
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Unique tallies should pass validation"
        Path(temp_file).unlink()

    # ===== Recommendation Tests =====

    def test_validate_complex_geometry_recommendation(self):
        """Test recommendation for complex geometry (>10 cells)"""
        # Create input with >10 cells
        cells = "\n".join([f"{i} 0 -{i} imp:n=1" for i in range(1, 12)])
        surfaces = "\n".join([f"{i} so {i*5}" for i in range(1, 12)])

        content = f"""test - complex geometry
{cells}

{surfaces}

sdef
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert any('geometry plotting' in rec.lower()
                   for rec in result['recommendations']), \
            "Should recommend geometry plotting for complex geometry"
        Path(temp_file).unlink()

    # ===== Integration Tests =====

    def test_validate_realistic_sphere_problem(self):
        """Test validation of realistic sphere problem"""
        content = """Godiva sphere problem
10 1 0.04921 -1 imp:n=1      $ HEU sphere
20 0 1 imp:n=0               $ Void

1 so 8.7407                  $ Sphere radius (cm)

sdef pos=0 0 0 erg=d1
si1 l 2.0                    $ 2 MeV neutron
m1 92235.80c 0.9346          $ U-235
   92238.80c 0.0654          $ U-238
kcode 10000 1.0 50 250       $ Criticality
ksrc 0 0 0                   $ Initial source
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Realistic problem should pass validation"
        assert len(result['errors']) == 0, "No errors in valid problem"
        Path(temp_file).unlink()

    def test_validate_shielding_problem(self):
        """Test validation of shielding problem with tallies"""
        content = """Simple shielding problem
10 1 -2.7 -1 imp:n=1         $ Aluminum shield
20 0 1 imp:n=0               $ Void

1 so 10.0                    $ Shield sphere

sdef pos=0 0 0 erg=14.1      $ 14.1 MeV point source
m1 13027 1.0                 $ Aluminum
f2:n 1                       $ Surface flux
f4:n 10                      $ Cell flux
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is True, "Shielding problem should pass validation"
        Path(temp_file).unlink()

    def test_validate_multiple_errors(self):
        """Test detection of multiple errors in one input"""
        content = """test - multiple errors
1 999 -1.0 -1 -99 imp:n=1    $ Undefined material and surface
2 1 -2.7 1 imp:n=1

1 so 5.0

sdef
m1 13027 1.0
f1:n 1
f1:p 1                        $ Duplicate tally
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Multiple errors should fail validation"
        assert len(result['errors']) >= 2, "Should detect multiple errors"
        assert any('material' in err.lower() for err in result['errors'])
        assert any('surface' in err.lower() for err in result['errors'])
        Path(temp_file).unlink()

    # ===== Edge Case Tests =====

    def test_validate_empty_input(self):
        """Test validation of empty input"""
        content = ""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Empty input should fail validation"
        Path(temp_file).unlink()

    def test_validate_comment_only_input(self):
        """Test validation of input with only comments"""
        content = """c This is a comment
c Another comment
c More comments
"""
        temp_file = self.create_temp_input(content)
        result = self.validator.validate_file(temp_file)

        assert result['valid'] is False, "Comment-only input should fail validation"
        Path(temp_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
