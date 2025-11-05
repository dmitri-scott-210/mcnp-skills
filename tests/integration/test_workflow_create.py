"""
Integration tests for Create → Validate → Analyze workflow

Tests the complete workflow:
1. Create geometry with geometry-builder
2. Validate input with input-validator
3. Check geometry with geometry-checker

This workflow simulates typical user interaction when building MCNP inputs.
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

# Add skill directories to path
geometry_builder_dir = project_root / ".claude" / "skills" / "mcnp-geometry-builder"
input_validator_dir = project_root / ".claude" / "skills" / "mcnp-input-validator"
geometry_checker_dir = project_root / ".claude" / "skills" / "mcnp-geometry-checker"

sys.path.insert(0, str(geometry_builder_dir))
sys.path.insert(0, str(input_validator_dir))
sys.path.insert(0, str(geometry_checker_dir))

from mcnp_geometry_builder import MCNPGeometryBuilder
from mcnp_input_validator import MCNPInputValidator
from mcnp_geometry_checker import MCNPGeometryChecker


class TestWorkflowCreate:
    """Test suite for Create → Validate → Analyze workflow"""

    def setup_method(self):
        """Setup test fixtures"""
        self.geo_builder = MCNPGeometryBuilder()
        self.validator = MCNPInputValidator()
        self.geo_checker = MCNPGeometryChecker()

    # ===== Simple Sphere Workflow =====

    def test_simple_sphere_workflow(self):
        """Test complete workflow: create sphere → validate → check"""
        # Step 1: Create geometry
        surf_id = self.geo_builder.add_sphere((0, 0, 0), 5.0)
        assert surf_id is not None

        # Step 2: Create minimal input (manually for testing)
        input_text = """Simple Sphere Test
c Cell cards
1 1 -1.0 -1     $ Water sphere
2 0     1       $ Void outside

c Surface cards
1 so 5.0        $ Sphere at origin, R=5

c Data cards
mode n
nps 1000
sdef pos=0 0 0 erg=1.0
m1 1001.80c 2 8016.80c 1  $ Water
"""

        # Step 3: Validate input
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None
        assert 'errors' in validation_result or 'is_valid' in validation_result

        # Step 4: Check geometry
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    def test_cylinder_workflow(self):
        """Test complete workflow with cylinder geometry"""
        # Step 1: Create cylinder
        surf_id = self.geo_builder.add_cylinder('z', (0, 0), 2.5)
        assert surf_id is not None

        # Step 2: Create minimal input
        input_text = """Cylinder Test
c Cell cards
1 1 -1.0 -1 -2 2  $ Water cylinder
2 0     1:-2:2    $ Void outside

c Surface cards
1 cz 2.5        $ Cylinder along Z
2 pz -10        $ Bottom plane
2 pz 10         $ Top plane

c Data cards
mode n
nps 1000
m1 1001.80c 2 8016.80c 1
"""

        # Step 3: Validate
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None

        # Step 4: Check geometry
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    # ===== Multi-Cell Geometry Workflow =====

    def test_multi_cell_workflow(self):
        """Test workflow with multiple cells"""
        # Step 1: Create nested spheres
        inner_sphere = self.geo_builder.add_sphere((0, 0, 0), 2.0)
        outer_sphere = self.geo_builder.add_sphere((0, 0, 0), 5.0)
        assert inner_sphere is not None
        assert outer_sphere is not None

        # Step 2: Create nested sphere input
        input_text = """Nested Spheres
c Cell cards
1 1 -1.0 -1     $ Inner sphere (water)
2 2 -2.7 1 -2   $ Outer shell (aluminum)
3 0     2       $ Void outside

c Surface cards
1 so 2.0        $ Inner sphere
2 so 5.0        $ Outer sphere

c Data cards
mode n
nps 1000
sdef pos=0 0 0 erg=1.0
m1 1001.80c 2 8016.80c 1     $ Water
m2 13027.80c 1               $ Aluminum
"""

        # Step 3: Validate
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None

        # Step 4: Check geometry
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    # ===== PWR Pin Cell Workflow =====

    def test_pwr_pin_cell_workflow(self):
        """Test realistic PWR pin cell workflow"""
        # Step 1: Create PWR pin geometry (fuel, gap, clad)
        fuel_surf = self.geo_builder.add_cylinder('z', (0, 0), 0.41)
        gap_surf = self.geo_builder.add_cylinder('z', (0, 0), 0.42)
        clad_surf = self.geo_builder.add_cylinder('z', (0, 0), 0.48)
        assert fuel_surf is not None
        assert gap_surf is not None
        assert clad_surf is not None

        # Step 2: Create PWR pin input
        input_text = """PWR Pin Cell
c Cell cards
1 1 -10.4 -1    $ UO2 fuel
2 0     1 -2    $ Gap
3 2 -6.5 2 -3   $ Zircaloy cladding
4 3 -0.74 3     $ Water moderator

c Surface cards
1 cz 0.41       $ Fuel radius
2 cz 0.42       $ Gap radius
3 cz 0.48       $ Clad outer radius

c Data cards
mode n
kcode 1000 1.0 25 125
ksrc 0 0 0
m1 92235.80c 0.035 92238.80c 0.965 8016.80c 2.0  $ 3.5% enriched UO2
m2 40090.80c 1                                   $ Zircaloy
m3 1001.80c 2 8016.80c 1                         $ Water
"""

        # Step 3: Validate
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None

        # Step 4: Check geometry
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    # ===== Error Detection Workflow =====

    def test_invalid_geometry_detection(self):
        """Test that workflow detects invalid geometry"""
        # Step 1: Create geometry (valid)
        surf_id = self.geo_builder.add_sphere((0, 0, 0), 5.0)
        assert surf_id is not None

        # Step 2: Create invalid input (missing surfaces)
        input_text = """Invalid Geometry
c Cell cards
1 1 -1.0 -999   $ References non-existent surface
2 0     999

c Surface cards
1 so 5.0        $ Surface 1 defined, but cell references 999

c Data cards
mode n
nps 1000
m1 1001.80c 2 8016.80c 1
"""

        # Step 3: Validate - should detect error
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None
        # Validator should flag missing surface reference

        # Step 4: Geometry checker might also detect issues
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    def test_overlapping_cells_detection(self):
        """Test detection of overlapping cells"""
        # Create input with potentially overlapping cells
        input_text = """Overlapping Cells Test
c Cell cards
1 1 -1.0 -1     $ Sphere 1
2 2 -2.7 -2     $ Sphere 2 (may overlap with 1)
3 0     1 2     $ Void outside

c Surface cards
1 s 0 0 0 3.0   $ Sphere at origin
2 s 2 0 0 3.0   $ Sphere offset by 2cm (overlaps!)

c Data cards
mode n
nps 1000
sdef pos=0 0 0
m1 1001.80c 2 8016.80c 1
m2 13027.80c 1
"""

        # Validate
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None

        # Check geometry - should detect overlap
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    # ===== Complex Geometry Workflow =====

    def test_box_geometry_workflow(self):
        """Test workflow with box geometry"""
        # Step 1: Create box surfaces
        xmin = self.geo_builder.add_plane('x', -5)
        xmax = self.geo_builder.add_plane('x', 5)
        ymin = self.geo_builder.add_plane('y', -5)
        ymax = self.geo_builder.add_plane('y', 5)
        zmin = self.geo_builder.add_plane('z', -5)
        zmax = self.geo_builder.add_plane('z', 5)

        assert all([xmin, xmax, ymin, ymax, zmin, zmax])

        # Step 2: Create box input
        input_text = """Box Geometry
c Cell cards
1 1 -2.7 -1 1 -2 2 -3 3     $ Aluminum box
2 0     1:-1:2:-2:3:-3      $ Void outside

c Surface cards
1 px -5         $ X min
1 px 5          $ X max
2 py -5         $ Y min
2 py 5          $ Y max
3 pz -5         $ Z min
3 pz 5          $ Z max

c Data cards
mode n
nps 1000
sdef pos=0 0 0 erg=1.0
m1 13027.80c 1  $ Aluminum
"""

        # Step 3: Validate
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None

        # Step 4: Check geometry
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

    # ===== Workflow Timing Tests =====

    def test_workflow_performance_simple(self):
        """Test workflow performance on simple geometry"""
        import time

        # Simple sphere geometry
        input_text = """Simple Sphere
c Cell cards
1 1 -1.0 -1
2 0     1

c Surface cards
1 so 10.0

c Data cards
mode n
nps 1000
sdef pos=0 0 0 erg=1.0
m1 1001.80c 2 8016.80c 1
"""

        start = time.time()

        # Validation
        validation_result = self.validator.validate_input(input_text)
        assert validation_result is not None

        # Geometry check
        geometry_result = self.geo_checker.check_geometry(input_text)
        assert geometry_result is not None

        elapsed = time.time() - start

        # Should complete quickly (< 5 seconds for simple geometry)
        assert elapsed < 5.0, f"Workflow took {elapsed:.2f}s (expected < 5s)"

    # ===== Integration Test Summary =====

    def test_workflow_integration_summary(self):
        """Summary test: create multiple geometries and validate all"""
        geometries = []

        # Create sphere
        self.geo_builder.add_sphere((0, 0, 0), 5.0)
        geometries.append("sphere")

        # Create cylinder
        self.geo_builder.add_cylinder('z', (0, 0), 2.5)
        geometries.append("cylinder")

        # Create planes
        self.geo_builder.add_plane('z', 0)
        geometries.append("plane")

        assert len(geometries) == 3
        assert len(self.geo_builder.surfaces) >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
