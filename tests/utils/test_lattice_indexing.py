"""
Test suite for utils/lattice_indexing.py
"""
import pytest
from utils.lattice_indexing import HexLattice, RectLattice

class TestHexLattice:
    
    def test_ring_position_conversion(self):
        """Test converting ring/position to i,j coordinates"""
        lattice = HexLattice()
        
        # Center element is ring 0, position 0
        i, j = lattice.ring_position_to_ij(0, 0)
        assert i == 0 and j == 0
        
        # Ring 1 has 6 elements
        ring1_coords = [lattice.ring_position_to_ij(1, p) for p in range(6)]
        assert len(ring1_coords) == 6
    
    def test_ij_to_xy(self):
        """Test converting i,j to x,y physical coordinates"""
        lattice = HexLattice(pitch=1.0)
        
        x, y = lattice.ij_to_xy(0, 0)
        assert abs(x) < 1e-10 and abs(y) < 1e-10
        
        x, y = lattice.ij_to_xy(1, 0)
        assert abs(x - 1.0) < 1e-10
    
    def test_get_ring_elements(self):
        """Test getting all elements in a ring"""
        lattice = HexLattice()
        
        ring0 = lattice.get_ring_elements(0)
        assert len(ring0) == 1
        
        ring1 = lattice.get_ring_elements(1)
        assert len(ring1) == 6
        
        ring2 = lattice.get_ring_elements(2)
        assert len(ring2) == 12

class TestRectLattice:
    
    def test_ijk_to_xyz(self):
        """Test 3D rectangular lattice indexing"""
        lattice = RectLattice(pitch_x=1.0, pitch_y=1.0, pitch_z=1.0)
        
        x, y, z = lattice.ijk_to_xyz(0, 0, 0)
        assert abs(x) < 1e-10 and abs(y) < 1e-10 and abs(z) < 1e-10
        
        x, y, z = lattice.ijk_to_xyz(2, 3, 1)
        assert abs(x - 2.0) < 1e-10
        assert abs(y - 3.0) < 1e-10
        assert abs(z - 1.0) < 1e-10
