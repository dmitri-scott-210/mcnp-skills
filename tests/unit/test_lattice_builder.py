"""
Unit tests for MCNP Lattice Builder Skill

Tests lattice construction capabilities:
- Rectangular lattices (LAT=1)
- Hexagonal lattices (LAT=2)
- Simple FILL operations
- Universe array handling
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-lattice-builder"
sys.path.insert(0, str(skill_dir))

from mcnp_lattice_builder import MCNPLatticeBuilder


class TestMCNPLatticeBuilder:
    """Test suite for MCNP Lattice Builder"""

    def setup_method(self):
        """Setup test fixture"""
        self.builder = MCNPLatticeBuilder()

    # ===== Rectangular Lattice Tests =====

    def test_rectangular_lattice_2x2x1(self):
        """Test 2x2x1 rectangular lattice"""
        universe_array = [1, 2, 3, 4]  # 2x2x1
        result = self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=universe_array
        )
        assert result is not None
        assert 'lat=1' in result
        assert '0:1' in result  # nx-1
        assert '0:1' in result  # ny-1

    def test_rectangular_lattice_3x3x3(self):
        """Test 3x3x3 rectangular lattice"""
        universe_array = [1] * 27  # 3x3x3 = 27
        result = self.builder.create_rectangular_lattice(
            cell_num=20, nx=3, ny=3, nz=3,
            universe_array=universe_array
        )
        assert result is not None
        assert 'lat=1' in result
        assert '0:2' in result  # 3-1=2

    def test_rectangular_lattice_custom_universe(self):
        """Test rectangular lattice with custom universe number"""
        universe_array = [1, 2, 3, 4]
        result = self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=universe_array,
            universe_num=50
        )
        assert result is not None
        assert 'u=50' in result

    def test_rectangular_lattice_wrong_array_size(self):
        """Test rectangular lattice with incorrect array size"""
        universe_array = [1, 2, 3]  # Wrong size for 2x2x1
        with pytest.raises(ValueError):
            self.builder.create_rectangular_lattice(
                cell_num=10, nx=2, ny=2, nz=1,
                universe_array=universe_array
            )

    def test_rectangular_lattice_contains_universes(self):
        """Test rectangular lattice contains all universes"""
        universe_array = [5, 6, 7, 8]
        result = self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=universe_array
        )
        assert '5' in result
        assert '6' in result
        assert '7' in result
        assert '8' in result

    def test_rectangular_lattice_importance(self):
        """Test rectangular lattice has importance"""
        universe_array = [1, 2, 3, 4]
        result = self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=universe_array
        )
        assert 'imp:n=1' in result

    # ===== Hexagonal Lattice Tests =====

    def test_hexagonal_lattice_single_element(self):
        """Test hexagonal lattice with center only (0 rings)"""
        universe_map = {(0, 0): 1}  # Center element
        result = self.builder.create_hexagonal_lattice(
            cell_num=30, pitch=1.26, n_rings=0,
            universe_map=universe_map
        )
        assert result is not None
        assert 'lat=2' in result

    def test_hexagonal_lattice_one_ring(self):
        """Test hexagonal lattice with 1 ring (7 elements total)"""
        universe_map = {
            (0, 0): 1,  # Center
            (1, 0): 2, (1, 1): 2, (1, 2): 2,
            (1, 3): 2, (1, 4): 2, (1, 5): 2
        }
        result = self.builder.create_hexagonal_lattice(
            cell_num=30, pitch=1.26, n_rings=1,
            universe_map=universe_map
        )
        assert result is not None
        assert 'lat=2' in result

    def test_hexagonal_lattice_custom_universe(self):
        """Test hexagonal lattice with custom universe number"""
        universe_map = {(0, 0): 1}
        result = self.builder.create_hexagonal_lattice(
            cell_num=30, pitch=1.26, n_rings=0,
            universe_map=universe_map,
            universe_num=75
        )
        assert 'u=75' in result

    def test_hexagonal_lattice_pwr_assembly(self):
        """Test hexagonal lattice for PWR assembly (17x17 approximation)"""
        # Simple test with center + 1 ring
        universe_map = {(0, 0): 1}
        for pos in range(6):
            universe_map[(1, pos)] = 2
        result = self.builder.create_hexagonal_lattice(
            cell_num=40, pitch=1.26, n_rings=1,
            universe_map=universe_map
        )
        assert result is not None
        assert 'lat=2' in result

    # ===== Simple FILL Tests =====

    def test_simple_fill_basic(self):
        """Test simple FILL with single universe"""
        result = self.builder.create_simple_fill(
            cell_num=50, material=0, geometry="-10",
            fill_universe=5
        )
        assert result is not None
        assert 'fill=5' in result

    def test_simple_fill_with_importance(self):
        """Test simple FILL with importance parameter"""
        result = self.builder.create_simple_fill(
            cell_num=50, material=0, geometry="-10",
            fill_universe=5,
            importance_n=1
        )
        assert 'imp:n=1' in result

    def test_simple_fill_with_transformation(self):
        """Test simple FILL with transformation"""
        result = self.builder.create_simple_fill(
            cell_num=50, material=0, geometry="-10",
            fill_universe=5,
            transformation=10
        )
        assert 'trcl=10' in result

    def test_simple_fill_multiple_params(self):
        """Test simple FILL with multiple parameters"""
        result = self.builder.create_simple_fill(
            cell_num=50, material=0, geometry="-10",
            fill_universe=5,
            importance_n=1,
            transformation=10
        )
        assert 'fill=5' in result
        assert 'imp:n=1' in result
        assert 'trcl=10' in result

    # ===== Card Generation Tests =====

    def test_generate_cards_empty(self):
        """Test generate_cards with no lattices"""
        result = self.builder.generate_cards()
        assert result is not None
        assert 'Lattice Cells' in result

    def test_generate_cards_single_lattice(self):
        """Test generate_cards with one lattice"""
        self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=[1, 2, 3, 4]
        )
        result = self.builder.generate_cards()
        assert 'Lattice Cells' in result
        assert 'lat=1' in result

    def test_generate_cards_multiple_lattices(self):
        """Test generate_cards with multiple lattices"""
        self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=[1, 2, 3, 4]
        )
        self.builder.create_simple_fill(
            cell_num=20, material=0, geometry="-20",
            fill_universe=99
        )
        result = self.builder.generate_cards()
        assert 'lat=1' in result
        assert 'fill=99' in result

    # ===== Universe Tracking Tests =====

    def test_universe_tracking_rectangular(self):
        """Test universe tracking for rectangular lattice"""
        self.builder.create_rectangular_lattice(
            cell_num=10, nx=2, ny=2, nz=1,
            universe_array=[1, 2, 3, 4],
            universe_num=99
        )
        assert 99 in self.builder.universe_defs
        assert self.builder.universe_defs[99] == 'rectangular_lattice'

    def test_universe_tracking_hexagonal(self):
        """Test universe tracking for hexagonal lattice"""
        universe_map = {(0, 0): 1}
        self.builder.create_hexagonal_lattice(
            cell_num=30, pitch=1.26, n_rings=0,
            universe_map=universe_map,
            universe_num=88
        )
        assert 88 in self.builder.universe_defs
        assert self.builder.universe_defs[88] == 'hexagonal_lattice'

    # ===== Integration Tests =====

    def test_pwr_fuel_assembly_lattice(self):
        """Test realistic PWR fuel assembly lattice"""
        # 17x17 lattice with guide tubes
        universe_array = []
        for i in range(17*17*1):
            if i % 17 == 8 or i // 17 == 8:  # Guide tube positions
                universe_array.append(2)
            else:
                universe_array.append(1)

        result = self.builder.create_rectangular_lattice(
            cell_num=100, nx=17, ny=17, nz=1,
            universe_array=universe_array
        )
        assert result is not None
        assert 'lat=1' in result
        assert '0:16' in result  # 17-1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
