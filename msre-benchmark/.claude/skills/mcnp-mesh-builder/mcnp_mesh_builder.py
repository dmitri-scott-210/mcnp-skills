"""
MCNP Mesh Builder (Skill 23) - FMESH and TMESH superimposed mesh tallies

Based on MCNP6.3 Chapter 5.9.18 - Mesh Tallies:
- FMESH: Rectangular (xyz), cylindrical (cyl, rzt) superimposed mesh
- TMESH: MCNPX-style mesh tallies (RMESH, CMESH, SMESH)
- OUT formats: IJ, CF, COL, CUV, XDMF (HDF5 for ParaView/VisIt)
- Energy binning: EMESH/EINTS for energy-resolved tallies
- Time binning: Available with TMESH

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md: ADVANCED OPERATIONS section
- Chapter 5.9.18: FMESH and TMESH cards
- Appendix D.4: XDMF mesh output format
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from typing import List, Tuple, Optional

class MCNPMeshBuilder:
    """
    Build MCNP mesh tallies for spatial distributions

    Capabilities:
    - Rectangular (xyz) mesh tallies
    - Cylindrical (cyl, rzt) mesh tallies
    - Energy binning
    - XDMF output for visualization
    - Unstructured mesh embedding
    """

    def __init__(self):
        self.mesh_tallies = []

    def add_rectangular_mesh(self, tally_num: int, particle: str,
                            origin: Tuple[float, float, float],
                            imesh: List[float], jmesh: List[float], kmesh: List[float],
                            iints: List[int], jints: List[int], kints: List[int],
                            emesh: Optional[List[float]] = None,
                            eints: Optional[List[int]] = None,
                            out_format: str = 'xdmf') -> str:
        """
        Add rectangular FMESH tally (xyz geometry)

        Args:
            tally_num: Tally number (e.g., 104 for FMESH104)
            particle: Particle type (n, p, e, etc.)
            origin: (x, y, z) origin of mesh
            imesh: X-direction mesh boundaries
            jmesh: Y-direction mesh boundaries
            kmesh: Z-direction mesh boundaries
            iints: Number of intervals between imesh boundaries
            jints: Number of intervals between jmesh boundaries
            kints: Number of intervals between kmesh boundaries
            emesh: Energy boundaries (optional)
            eints: Energy intervals (optional)
            out_format: Output format (xdmf, ij, cf, col, cuv)

        Returns:
            FMESH card string

        Example:
            imesh=[10, 20], iints=[5] creates 5 bins from 10 to 20 cm
        """
        if len(imesh) != len(iints):
            raise ValueError(f"imesh length {len(imesh)} must equal iints length {len(iints)}")
        if len(jmesh) != len(jints):
            raise ValueError(f"jmesh length {len(jmesh)} must equal jints length {len(jints)}")
        if len(kmesh) != len(kints):
            raise ValueError(f"kmesh length {len(kmesh)} must equal kints length {len(kints)}")

        card = f"fmesh{tally_num}:{particle}"
        card += f" geom=xyz origin={origin[0]} {origin[1]} {origin[2]}"
        card += f" imesh=" + " ".join(map(str, imesh))
        card += f" iints=" + " ".join(map(str, iints))
        card += f" jmesh=" + " ".join(map(str, jmesh))
        card += f" jints=" + " ".join(map(str, jints))
        card += f" kmesh=" + " ".join(map(str, kmesh))
        card += f" kints=" + " ".join(map(str, kints))

        # Add energy binning if specified
        if emesh and eints:
            card += f" emesh=" + " ".join(map(str, emesh))
            card += f" eints=" + " ".join(map(str, eints))

        # Add output format
        card += f" out={out_format}"

        self.mesh_tallies.append(card)
        return card

    def add_cylindrical_mesh(self, tally_num: int, particle: str,
                            origin: Tuple[float, float, float],
                            axis: Tuple[float, float, float],
                            vec: Tuple[float, float, float],
                            rmesh: List[float], zmesh: List[float],
                            rints: List[int], zints: List[int],
                            geometry: str = 'cyl',
                            out_format: str = 'xdmf') -> str:
        """
        Add cylindrical FMESH tally (cyl or rzt geometry)

        Args:
            tally_num: Tally number
            particle: Particle type
            origin: (x, y, z) origin (base of cylinder)
            axis: (ax, ay, az) cylinder axis direction
            vec: (vx, vy, vz) reference vector (defines theta=0)
            rmesh: Radial boundaries
            zmesh: Axial (z) boundaries
            rints: Radial intervals
            zints: Axial intervals
            geometry: 'cyl' (r,theta,z) or 'rzt' (r,z,theta)
            out_format: Output format

        Returns:
            FMESH card string
        """
        card = f"fmesh{tally_num}:{particle}"
        card += f" geom={geometry}"
        card += f" origin={origin[0]} {origin[1]} {origin[2]}"
        card += f" axs={axis[0]} {axis[1]} {axis[2]}"
        card += f" vec={vec[0]} {vec[1]} {vec[2]}"
        card += f" imesh=" + " ".join(map(str, rmesh))  # i = radial
        card += f" iints=" + " ".join(map(str, rints))
        card += f" kmesh=" + " ".join(map(str, zmesh))  # k = axial
        card += f" kints=" + " ".join(map(str, zints))
        card += f" out={out_format}"

        self.mesh_tallies.append(card)
        return card

    def add_tmesh(self, mesh_num: int, particle: str, mesh_type: str,
                 cora: List[float], corb: List[float], corc: List[float],
                 ergsh: Optional[List[float]] = None) -> str:
        """
        Add TMESH tally (MCNPX-style mesh)

        Args:
            mesh_num: Mesh tally number (1, 11, 21, etc.)
            particle: Particle type
            mesh_type: 'rmesh' (rectangular), 'cmesh' (cylindrical), 'smesh' (spherical)
            cora, corb, corc: Coordinate boundaries
            ergsh: Energy boundaries (optional)

        Returns:
            TMESH block string

        TMESH Types:
            Type 1 (n=1,11,21,...): Track-averaged flux
            Type 2 (n=2,12,22,...): Source point data
            Type 3 (n=3,13,23,...): Energy deposition
            Type 4 (n=4,14,24,...): DXTRAN contributions
        """
        lines = ["tmesh"]
        lines.append(f"  {mesh_type}{mesh_num}:{particle}")
        lines.append(f"    cora{mesh_num} " + " ".join(map(str, cora)))
        lines.append(f"    corb{mesh_num} " + " ".join(map(str, corb)))
        lines.append(f"    corc{mesh_num} " + " ".join(map(str, corc)))

        if ergsh:
            lines.append(f"    ergsh{mesh_num} " + " ".join(map(str, ergsh)))

        lines.append("endmd")

        tmesh_block = "\n".join(lines)
        self.mesh_tallies.append(tmesh_block)
        return tmesh_block

    def add_unstructured_mesh(self, mesh_file: str, background_cell: int,
                             mesh_format: str = 'abaqus') -> str:
        """
        Add unstructured mesh embedding

        Args:
            mesh_file: Path to mesh file (ABAQUS .inp format)
            background_cell: Cell number where mesh is embedded
            mesh_format: Mesh file format (default 'abaqus')

        Returns:
            EMBED/EMBEE card string
        """
        lines = [
            f"embed {mesh_file}",
            f"embee 1 {background_cell}"
        ]
        embed_block = "\n".join(lines)
        self.mesh_tallies.append(embed_block)
        return embed_block

    def estimate_mesh_size(self, nx: int, ny: int, nz: int,
                          ne: int = 1, stat_target: float = 0.05) -> dict:
        """
        Estimate particles needed for mesh tally statistics

        Args:
            nx, ny, nz: Number of spatial bins
            ne: Number of energy bins
            stat_target: Target relative error (default 0.05 = 5%)

        Returns:
            Dict with particle estimate and recommendations
        """
        total_bins = nx * ny * nz * ne
        particles_per_bin = int((1.0 / stat_target) ** 2)  # From R² ~ 1/N
        total_particles = total_bins * particles_per_bin

        return {
            'total_bins': total_bins,
            'particles_per_bin': particles_per_bin,
            'total_particles_needed': total_particles,
            'recommendation': f"Run {total_particles:,} particles for {stat_target*100}% relative error"
        }

    def generate_cards(self) -> str:
        """Generate all mesh tally cards"""
        lines = ["c Mesh Tally Cards"]
        lines.extend(self.mesh_tallies)
        return "\n".join(lines)
