"""
MCNP6 Lattice Indexing Utilities
Handle hexagonal (LAT=1) and rectangular (LAT=2) lattice indexing
"""

import math
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass


@dataclass
class LatticeElement:
    """Represents a single lattice element"""
    i: int  # First index
    j: int  # Second index
    k: int  # Third index (for 3D lattices)
    universe: int  # Universe number filling this element
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # Physical position


class HexLattice:
    """
    Hexagonal lattice (LAT=1) indexing utilities
    
    MCNP hexagonal lattices use a unique indexing scheme based on rings.
    Ring 0 is the center element.
    Ring N contains 6N elements arranged hexagonally.
    """
    
    def __init__(self, pitch: float = 1.0, origin: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        """
        Initialize hexagonal lattice
        
        Args:
            pitch: Distance between adjacent hex centers
            origin: Origin position of lattice
        """
        self.pitch = pitch
        self.origin = origin
    
    @staticmethod
    def ring_position_to_ij(ring: int, position: int) -> Tuple[int, int]:
        """
        Convert (ring, position) to (i, j) indices
        
        Ring 0: (0, 0)
        Ring 1: positions 0-5
        Ring 2: positions 0-11
        etc.
        
        Args:
            ring: Ring number (0 = center, 1 = first ring, etc.)
            position: Position within ring (0 to 6*ring-1)
        
        Returns:
            (i, j) tuple
        """
        if ring == 0:
            return (0, 0)
        
        # Starting position for each side of the hexagon
        positions_per_side = ring
        side = position // positions_per_side
        pos_in_side = position % positions_per_side
        
        # Hexagonal directions (6 sides)
        # Side 0: +i direction
        # Side 1: +j, -i direction
        # Side 2: +j direction
        # Side 3: -i direction
        # Side 4: -j, +i direction
        # Side 5: -j direction
        
        if side == 0:  # Right side
            i = ring
            j = pos_in_side
        elif side == 1:  # Upper right
            i = ring - pos_in_side - 1
            j = ring
        elif side == 2:  # Upper left
            i = -pos_in_side - 1
            j = ring - pos_in_side - 1
        elif side == 3:  # Left side
            i = -ring
            j = -pos_in_side - 1
        elif side == 4:  # Lower left
            i = -ring + pos_in_side + 1
            j = -ring
        else:  # side == 5, Lower right
            i = pos_in_side + 1
            j = -ring + pos_in_side + 1
        
        return (i, j)
    
    @staticmethod
    def ij_to_ring_position(i: int, j: int) -> Tuple[int, int]:
        """
        Convert (i, j) indices to (ring, position)
        
        Args:
            i, j: Hexagonal lattice indices
        
        Returns:
            (ring, position) tuple
        """
        if i == 0 and j == 0:
            return (0, 0)
        
        # Ring number is maximum of abs(i), abs(j), abs(i+j)
        ring = max(abs(i), abs(j), abs(i + j))
        
        # Determine which side and position
        if i == ring and j >= 0:  # Side 0: right
            position = j
        elif j == ring and i <= 0:  # Side 1: upper right
            position = ring + (ring - i - 1)
        elif i + j == -ring and i < 0:  # Side 2: upper left
            position = 2 * ring + (-i - 1)
        elif i == -ring and j <= 0:  # Side 3: left
            position = 3 * ring + (-j - 1)
        elif j == -ring and i >= 0:  # Side 4: lower left
            position = 4 * ring + (i - 1)
        else:  # Side 5: lower right (i + j == ring and i > 0)
            position = 5 * ring + (j + ring - 1)
        
        return (ring, position)
    
    def ij_to_xy(self, i: int, j: int) -> Tuple[float, float]:
        """
        Convert (i, j) indices to (x, y) physical coordinates
        
        Args:
            i, j: Hexagonal lattice indices
        
        Returns:
            (x, y) coordinates in cm
        """
        # Hexagonal lattice geometry
        # x direction: pitch spacing
        # y direction: pitch * sqrt(3)/2 spacing, offset by i/2
        x = self.pitch * (i + 0.5 * j) + self.origin[0]
        y = self.pitch * (math.sqrt(3) / 2.0) * j + self.origin[1]
        
        return (x, y)
    
    def xy_to_ij(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert (x, y) coordinates to nearest (i, j) indices
        
        Args:
            x, y: Physical coordinates
        
        Returns:
            (i, j) indices of nearest hex
        """
        # Remove origin offset
        x = x - self.origin[0]
        y = y - self.origin[1]
        
        # Convert to fractional coordinates
        j_frac = y / (self.pitch * math.sqrt(3) / 2.0)
        i_frac = (x / self.pitch) - 0.5 * j_frac
        
        # Round to nearest integer
        i = round(i_frac)
        j = round(j_frac)
        
        return (i, j)
    
    def get_ring_elements(self, ring: int) -> List[Tuple[int, int]]:
        """
        Get all (i, j) indices for a given ring
        
        Args:
            ring: Ring number
        
        Returns:
            List of (i, j) tuples
        """
        if ring == 0:
            return [(0, 0)]
        
        elements = []
        num_positions = 6 * ring
        
        for pos in range(num_positions):
            i, j = self.ring_position_to_ij(ring, pos)
            elements.append((i, j))
        
        return elements
    
    def get_all_elements_up_to_ring(self, max_ring: int) -> List[Tuple[int, int]]:
        """Get all elements from ring 0 to max_ring"""
        elements = []
        for ring in range(max_ring + 1):
            elements.extend(self.get_ring_elements(ring))
        return elements
    
    @staticmethod
    def count_elements_in_ring(ring: int) -> int:
        """Count number of elements in a ring"""
        if ring == 0:
            return 1
        return 6 * ring
    
    @staticmethod
    def count_elements_up_to_ring(max_ring: int) -> int:
        """Count total elements from ring 0 to max_ring"""
        if max_ring == 0:
            return 1
        return 1 + 3 * max_ring * (max_ring + 1)


class RectLattice:
    """
    Rectangular lattice (LAT=2) indexing utilities
    """
    
    def __init__(self, pitch_x: float = 1.0, pitch_y: float = 1.0, pitch_z: float = 1.0,
                 origin: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        """
        Initialize rectangular lattice
        
        Args:
            pitch_x, pitch_y, pitch_z: Pitch in each direction
            origin: Origin position of lattice
        """
        self.pitch_x = pitch_x
        self.pitch_y = pitch_y
        self.pitch_z = pitch_z
        self.origin = origin
    
    def ijk_to_xyz(self, i: int, j: int, k: int = 0) -> Tuple[float, float, float]:
        """
        Convert (i, j, k) indices to (x, y, z) coordinates
        
        Args:
            i, j, k: Rectangular lattice indices
        
        Returns:
            (x, y, z) coordinates
        """
        x = self.pitch_x * i + self.origin[0]
        y = self.pitch_y * j + self.origin[1]
        z = self.pitch_z * k + self.origin[2]
        
        return (x, y, z)
    
    def xyz_to_ijk(self, x: float, y: float, z: float = 0.0) -> Tuple[int, int, int]:
        """
        Convert (x, y, z) coordinates to nearest (i, j, k) indices
        
        Args:
            x, y, z: Physical coordinates
        
        Returns:
            (i, j, k) indices
        """
        i = round((x - self.origin[0]) / self.pitch_x)
        j = round((y - self.origin[1]) / self.pitch_y)
        k = round((z - self.origin[2]) / self.pitch_z)
        
        return (i, j, k)
    
    def get_neighbors(self, i: int, j: int, k: int = 0, include_diagonals: bool = False) -> List[Tuple[int, int, int]]:
        """
        Get neighboring lattice elements
        
        Args:
            i, j, k: Center element indices
            include_diagonals: Include diagonal neighbors
        
        Returns:
            List of neighbor (i, j, k) tuples
        """
        neighbors = [
            (i+1, j, k), (i-1, j, k),
            (i, j+1, k), (i, j-1, k),
            (i, j, k+1), (i, j, k-1)
        ]
        
        if include_diagonals:
            # Add 2D diagonal neighbors
            neighbors.extend([
                (i+1, j+1, k), (i+1, j-1, k),
                (i-1, j+1, k), (i-1, j-1, k)
            ])
            # Add 3D diagonal neighbors
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di != 0 or dj != 0:
                        neighbors.extend([
                            (i+di, j+dj, k+1),
                            (i+di, j+dj, k-1)
                        ])
        
        return neighbors
    
    @staticmethod
    def parse_fill_array(fill_string: str, dims: Tuple[int, int, int]) -> Dict[Tuple[int, int, int], int]:
        """
        Parse FILL array specification
        
        Args:
            fill_string: FILL array data (space-separated universe numbers)
            dims: Lattice dimensions (nx, ny, nz)
        
        Returns:
            Dictionary mapping (i, j, k) to universe number
        """
        universes = [int(u) for u in fill_string.split()]
        fill_map = {}
        
        nx, ny, nz = dims
        idx = 0
        
        # MCNP FILL order: z varies fastest, then y, then x
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if idx < len(universes):
                        fill_map[(i, j, k)] = universes[idx]
                        idx += 1
        
        return fill_map


if __name__ == "__main__":
    # Test hexagonal lattice
    print("=== Hexagonal Lattice Tests ===")
    hex_lat = HexLattice(pitch=1.26)
    
    print(f"\nRing 0: {hex_lat.get_ring_elements(0)}")
    print(f"Ring 1 (6 elements): {hex_lat.get_ring_elements(1)}")
    print(f"Ring 2 (12 elements): {hex_lat.get_ring_elements(2)}")
    
    print(f"\nTotal elements up to ring 3: {hex_lat.count_elements_up_to_ring(3)}")
    
    # Test conversions
    ring, pos = 2, 5
    i, j = hex_lat.ring_position_to_ij(ring, pos)
    print(f"\nRing {ring}, Position {pos} → (i, j) = ({i}, {j})")
    
    ring_back, pos_back = hex_lat.ij_to_ring_position(i, j)
    print(f"(i, j) = ({i}, {j}) → Ring {ring_back}, Position {pos_back}")
    
    x, y = hex_lat.ij_to_xy(i, j)
    print(f"(i, j) = ({i}, {j}) → (x, y) = ({x:.3f}, {y:.3f}) cm")
    
    # Test rectangular lattice
    print("\n=== Rectangular Lattice Tests ===")
    rect_lat = RectLattice(pitch_x=1.0, pitch_y=1.0, pitch_z=1.0)
    
    i, j, k = 5, 3, 2
    x, y, z = rect_lat.ijk_to_xyz(i, j, k)
    print(f"(i, j, k) = ({i}, {j}, {k}) → (x, y, z) = ({x}, {y}, {z})")
    
    neighbors = rect_lat.get_neighbors(5, 5, 5)
    print(f"\nNeighbors of (5, 5, 5): {len(neighbors)} elements")
