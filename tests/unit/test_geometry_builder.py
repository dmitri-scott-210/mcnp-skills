"""
Unit tests for MCNP Geometry Builder Skill

Tests geometry construction capabilities:
- Surface creation (sphere, cylinder, plane, box)
- Cell definition with materials
- Geometry string generation
- Complete geometry assembly
"""
import pytest
import sys
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-geometry-builder"
sys.path.insert(0, str(skill_dir))

from mcnp_geometry_builder import MCNPGeometryBuilder


class TestMCNPGeometryBuilder:
    """Test suite for MCNP Geometry Builder"""

    def setup_method(self):
        """Setup test fixture"""
        self.builder = MCNPGeometryBuilder()

    # ===== Surface Creation Tests =====

    def test_add_sphere_centered(self):
        """Test adding centered sphere"""
        surf_num = self.builder.add_sphere(1, 0, 0, 0, 5.0)
        assert surf_num == 1
        assert len(self.builder.surfaces) == 1
        assert "so 5.0" in self.builder.surfaces[0]

    def test_add_sphere_offset(self):
        """Test adding offset sphere"""
        surf_num = self.builder.add_sphere(1, 1.0, 2.0, 3.0, 5.0)
        assert surf_num == 1
        assert "s 1.0 2.0 3.0 5.0" in self.builder.surfaces[0]

    def test_add_cylinder_z_axis(self):
        """Test adding cylinder along z-axis"""
        surf_num = self.builder.add_cylinder('z', (0.0, 0.0), 2.0)
        assert surf_num > 0
        assert len(self.builder.surfaces) == 1
        assert "c/z" in self.builder.surfaces[0]

    def test_add_plane(self):
        """Test adding plane"""
        surf_num = self.builder.add_plane('z', 10.0)
        assert surf_num > 0
        assert "pz 10.0" in self.builder.surfaces[0]

    def test_add_box(self):
        """Test adding box"""
        surf_num = self.builder.add_box(-5, 5, -5, 5, 0, 10)
        assert surf_num > 0
        assert "rpp" in self.builder.surfaces[0]

    # ===== Cell Creation Tests =====

    def test_add_cell_with_material(self):
        """Test adding cell with material"""
        cell_num = self.builder.add_cell(1, 1, -2.7, "-1")
        assert cell_num == 1
        assert len(self.builder.cells) == 1

    def test_add_cell_void(self):
        """Test adding void cell"""
        cell_num = self.builder.add_cell(1, 0, 0, "-1")
        assert cell_num == 1
        assert len(self.builder.cells) == 1

    # ===== Integration Tests =====

    def test_complete_sphere_geometry(self):
        """Test complete sphere geometry"""
        # Add surfaces
        s1 = self.builder.add_sphere(1, 0, 0, 0, 5.0)
        s2 = self.builder.add_sphere(2, 0, 0, 0, 10.0)

        # Add cells
        self.builder.add_cell(1, 1, -2.7, f"-{s1}", imp_n=1)
        self.builder.add_cell(2, 0, 0, f"{s1} -{s2}", imp_n=1)

        assert len(self.builder.surfaces) == 2
        assert len(self.builder.cells) == 2

    def test_pwr_pin_cell_geometry(self):
        """Test realistic PWR pin cell geometry"""
        # Fuel, gap, clad radii
        self.builder.add_cylinder('z', (0, 0), 0.41)
        self.builder.add_cylinder('z', (0, 0), 0.42)
        self.builder.add_cylinder('z', (0, 0), 0.48)

        assert len(self.builder.surfaces) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
