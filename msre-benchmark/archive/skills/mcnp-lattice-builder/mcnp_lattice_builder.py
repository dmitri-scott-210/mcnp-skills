"""
MCNP Lattice Builder (Skill 24) - Rectangular and hexagonal lattices with FILL

Based on MCNP6.3 Chapter 5.5 - Repeated Structures:
- LAT=1: Hexahedral (rectangular) lattice with [i,j,k] indexing
- LAT=2: Hexagonal prism lattice with ring/position indexing
- U card: Universe number (0-99,999,999)
- FILL card: Fill cell with universe or lattice array
- TRCL: Cell transformation for rotation/translation

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md: ADVANCED OPERATIONS section
- Chapter 5.5: Cell Parameters (U, FILL, LAT, TRCL)
- Chapter 10.1: Geometry Examples (lattice examples)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from typing import List, Tuple, Dict, Optional
from utils.lattice_indexing import HexLattice, RectLattice

class MCNPLatticeBuilder:
    """
    Build MCNP lattice structures with repeated universes

    Capabilities:
    - Rectangular lattices (LAT=1) with [i,j,k] indexing
    - Hexagonal lattices (LAT=2) with ring/position indexing
    - Simple FILL (single universe in cell)
    - Array FILL (universe array for lattice)
    """

    def __init__(self):
        self.lattice_cells = []
        self.universe_defs = {}  # Track defined universes

    def create_rectangular_lattice(self, cell_num: int, nx: int, ny: int, nz: int,
                                   universe_array: List[int],
                                   universe_num: int = 99,
                                   material: int = 0,
                                   geometry: str = "-1") -> str:
        """
        Create hexahedral (rectangular) lattice LAT=1

        Format: FILL=imin:imax jmin:jmax kmin:kmax universe_list
        Indexing: [i,j,k] where i varies fastest

        Args:
            cell_num: Cell number for lattice
            nx, ny, nz: Number of lattice elements in each direction
            universe_array: Flat list of universe numbers (length = nx*ny*nz)
            universe_num: Universe number for this lattice cell
            material: Material number (0 for lattice cell)
            geometry: Geometry specification

        Returns:
            MCNP cell card string
        """
        if len(universe_array) != nx * ny * nz:
            raise ValueError(f"Universe array length {len(universe_array)} != nx*ny*nz = {nx*ny*nz}")

        # Build cell card with LAT=1
        cell_str = f"{cell_num} {material} {geometry} lat=1 u={universe_num} imp:n=1"
        cell_str += f" fill=0:{nx-1} 0:{ny-1} 0:{nz-1}"

        # Add universe array (i varies fastest, then j, then k)
        for univ in universe_array:
            cell_str += f" {univ}"

        self.lattice_cells.append(cell_str)
        self.universe_defs[universe_num] = 'rectangular_lattice'
        return cell_str

    def create_hexagonal_lattice(self, cell_num: int, pitch: float, n_rings: int,
                                 universe_map: Dict[Tuple[int, int], int],
                                 universe_num: int = 99,
                                 material: int = 0,
                                 geometry: str = "-1") -> str:
        """
        Create hexagonal prism lattice LAT=2

        Format: FILL=universe_list (ordered by ring 0, then ring 1 positions, etc.)
        Indexing: Ring/position - (0,0) center, then 6 positions in ring 1, etc.

        Args:
            cell_num: Cell number for lattice
            pitch: Hexagonal pitch (distance between centers)
            n_rings: Number of hexagonal rings (0=center only, 1=center+6, etc.)
            universe_map: Dict mapping (ring, position) -> universe_number
            universe_num: Universe number for this lattice cell

        Returns:
            MCNP cell card string
        """
        hex_lat = HexLattice(pitch=pitch)
        elements = hex_lat.get_all_elements_up_to_ring(n_rings)

        fill_nums = []
        for ring, pos in elements:
            univ = universe_map.get((ring, pos), 0)
            fill_nums.append(str(univ))

        # Build cell card with LAT=2
        cell_str = f"{cell_num} {material} {geometry} lat=2 u={universe_num} imp:n=1 fill="
        cell_str += " ".join(fill_nums)

        self.lattice_cells.append(cell_str)
        self.universe_defs[universe_num] = 'hexagonal_lattice'
        return cell_str

    def create_simple_fill(self, cell_num: int, material: int, geometry: str,
                          fill_universe: int, **params) -> str:
        """
        Create cell filled with single universe (non-lattice)

        Format: j m geom FILL=n
        Used for nesting one universe inside another
        """
        cell_str = f"{cell_num} {material} {geometry} fill={fill_universe}"

        for key, val in params.items():
            if key == 'importance_n':
                cell_str += f" imp:n={val}"
            elif key == 'transformation':
                cell_str += f" trcl={val}"
            else:
                cell_str += f" {key}={val}"

        self.lattice_cells.append(cell_str)
        return cell_str
    
    def generate_cards(self) -> str:
        return "\n".join(["c Lattice Cells"] + self.lattice_cells)
