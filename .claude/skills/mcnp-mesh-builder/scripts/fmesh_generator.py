#!/usr/bin/env python3
"""
FMESH Card Generator for MCNP6

Purpose: Programmatically generate FMESH cards with automatic binning optimization.
Author: MCNP Skills Project
Version: 1.0.0

Usage:
    python fmesh_generator.py --geometry XYZ --origin 0 0 0 --extent 100 100 100 --bins 20 20 20
"""

import argparse
import sys
import numpy as np
from typing import List, Tuple, Optional


class FMESHGenerator:
    """Generate FMESH card specifications for MCNP6."""

    def __init__(self, tally_number: int = 4, particle: str = 'N'):
        """
        Initialize FMESH generator.

        Args:
            tally_number: FMESH tally number (must end in 4)
            particle: Particle type (N, P, E, etc.)
        """
        if tally_number % 10 != 4:
            raise ValueError("FMESH tally number must end in 4 (e.g., 4, 14, 24)")

        self.tally_number = tally_number
        self.particle = particle
        self.geometry = None
        self.origin = None
        self.mesh_spec = {}
        self.energy_bins = None
        self.time_bins = None
        self.output_format = 'xdmf'
        self.algorithm = 'fast_hist'

    def set_cartesian(self, origin: Tuple[float, float, float],
                      x_bounds: List[float], x_bins: List[int],
                      y_bounds: List[float], y_bins: List[int],
                      z_bounds: List[float], z_bins: List[int]):
        """
        Set Cartesian (XYZ) geometry.

        Args:
            origin: (x0, y0, z0) mesh origin
            x_bounds: X-direction mesh boundaries [x1, x2, ..., xn]
            x_bins: Number of intervals in each X segment [i1, i2, ..., in]
            y_bounds: Y-direction mesh boundaries
            y_bins: Number of intervals in each Y segment
            z_bounds: Z-direction mesh boundaries
            z_bins: Number of intervals in each Z segment
        """
        self.geometry = 'XYZ'
        self.origin = origin
        self.mesh_spec = {
            'IMESH': x_bounds,
            'IINTS': x_bins,
            'JMESH': y_bounds,
            'JINTS': y_bins,
            'KMESH': z_bounds,
            'KINTS': z_bins
        }

    def set_cylindrical(self, origin: Tuple[float, float, float],
                        axis: Tuple[float, float, float],
                        vec: Tuple[float, float, float],
                        r_bounds: List[float], r_bins: List[int],
                        z_bounds: List[float], z_bins: List[int],
                        theta_bounds: List[float], theta_bins: List[int]):
        """
        Set cylindrical (RZT) geometry.

        Args:
            origin: (x0, y0, z0) axis origin
            axis: (ux, uy, uz) axis direction vector
            vec: (vx, vy, vz) reference vector for theta=0
            r_bounds: Radial mesh boundaries [r1, r2, ..., rn]
            r_bins: Number of intervals in each R segment
            z_bounds: Axial mesh boundaries
            z_bins: Number of intervals in each Z segment
            theta_bounds: Azimuthal mesh boundaries (degrees) [θ1, θ2, ..., θn]
            theta_bins: Number of intervals in each θ segment
        """
        self.geometry = 'RZT'
        self.origin = origin
        self.mesh_spec = {
            'AXS': axis,
            'VEC': vec,
            'IMESH': r_bounds,
            'IINTS': r_bins,
            'JMESH': z_bounds,
            'JINTS': z_bins,
            'KMESH': theta_bounds,
            'KINTS': theta_bins
        }

    def set_energy_bins(self, energies: List[float]):
        """
        Set energy bin boundaries (MeV).

        Args:
            energies: Energy boundaries [e1, e2, ..., en]
        """
        self.energy_bins = energies

    def set_time_bins(self, times: List[float]):
        """
        Set time bin boundaries (shakes, 1e-8 s).

        Args:
            times: Time boundaries [t1, t2, ..., tn]
        """
        self.time_bins = times

    def set_output(self, fmt: str = 'xdmf'):
        """
        Set output format.

        Args:
            fmt: Output format ('xdmf', 'col', 'ij', 'ik', 'jk', 'none')
        """
        valid_formats = ['xdmf', 'col', 'ij', 'ik', 'jk', 'none']
        if fmt not in valid_formats:
            raise ValueError(f"Invalid format {fmt}. Must be one of {valid_formats}")
        self.output_format = fmt

    def set_algorithm(self, alg: str = 'fast_hist'):
        """
        Set mesh tally algorithm.

        Args:
            alg: Algorithm ('fast_hist', 'hist', 'batch', 'rma_batch')
        """
        valid_algs = ['fast_hist', 'hist', 'batch', 'rma_batch']
        if alg not in valid_algs:
            raise ValueError(f"Invalid algorithm {alg}. Must be one of {valid_algs}")
        self.algorithm = alg

    def generate(self) -> str:
        """
        Generate FMESH card string.

        Returns:
            FMESH card as string
        """
        if self.geometry is None:
            raise ValueError("Geometry not set. Use set_cartesian() or set_cylindrical()")

        lines = []

        # Header line
        lines.append(f"FMESH{self.tally_number}:{self.particle} GEOM={self.geometry}")

        # Origin
        origin_str = f"          ORIGIN={self.origin[0]} {self.origin[1]} {self.origin[2]}"
        lines.append(origin_str)

        # Axis and vector for RZT
        if self.geometry == 'RZT':
            ax = self.mesh_spec['AXS']
            vec = self.mesh_spec['VEC']
            lines.append(f"          AXS={ax[0]} {ax[1]} {ax[2]}")
            lines.append(f"          VEC={vec[0]} {vec[1]} {vec[2]}")

        # Mesh boundaries and intervals
        for coord, bounds_key, ints_key in [
            ('I', 'IMESH', 'IINTS'),
            ('J', 'JMESH', 'JINTS'),
            ('K', 'KMESH', 'KINTS')
        ]:
            bounds = self.mesh_spec[bounds_key]
            ints = self.mesh_spec[ints_key]

            # Format bounds (handle long lists with continuation)
            bounds_str = " ".join(str(b) for b in bounds)
            ints_str = " ".join(str(i) for i in ints)

            lines.append(f"          {bounds_key}={bounds_str}  {ints_key}={ints_str}")

        # Energy bins
        if self.energy_bins:
            e_str = " ".join(str(e) for e in self.energy_bins)
            lines.append(f"          EMESH={e_str}")

        # Time bins
        if self.time_bins:
            t_str = " ".join(str(t) for t in self.time_bins)
            lines.append(f"          TMESH={t_str}")

        # Output format
        lines.append(f"          OUT={self.output_format}")

        # Algorithm (if not default)
        if self.algorithm != 'fast_hist':
            lines.append(f"          MSHMF={self.algorithm}")

        return "\n".join(lines)

    def calculate_bins(self) -> int:
        """Calculate total number of bins."""
        if self.geometry is None:
            return 0

        i_bins = sum(self.mesh_spec['IINTS'])
        j_bins = sum(self.mesh_spec['JINTS'])
        k_bins = sum(self.mesh_spec['KINTS'])

        total = i_bins * j_bins * k_bins

        if self.energy_bins:
            total *= (len(self.energy_bins) - 1)

        if self.time_bins:
            total *= (len(self.time_bins) - 1)

        return total


def create_uniform_cartesian(origin: Tuple[float, float, float],
                              extent: Tuple[float, float, float],
                              bins: Tuple[int, int, int],
                              tally_number: int = 4,
                              particle: str = 'N') -> str:
    """
    Create uniform Cartesian mesh.

    Args:
        origin: (x0, y0, z0) corner of mesh
        extent: (x_size, y_size, z_size) mesh dimensions
        bins: (nx, ny, nz) number of bins in each direction
        tally_number: FMESH tally number
        particle: Particle type

    Returns:
        FMESH card string
    """
    gen = FMESHGenerator(tally_number, particle)

    x_end = origin[0] + extent[0]
    y_end = origin[1] + extent[1]
    z_end = origin[2] + extent[2]

    gen.set_cartesian(
        origin=origin,
        x_bounds=[x_end], x_bins=[bins[0]],
        y_bounds=[y_end], y_bins=[bins[1]],
        z_bounds=[z_end], z_bins=[bins[2]]
    )

    return gen.generate()


def create_logarithmic_radial(origin: Tuple[float, float, float],
                               r_min: float, r_max: float, r_bins: int,
                               z_min: float, z_max: float, z_bins: int,
                               tally_number: int = 14,
                               particle: str = 'N') -> str:
    """
    Create cylindrical mesh with logarithmic radial binning.

    Args:
        origin: (x0, y0, z0) axis origin
        r_min: Minimum radius
        r_max: Maximum radius
        r_bins: Number of radial bins
        z_min: Minimum Z
        z_max: Maximum Z
        z_bins: Number of axial bins
        tally_number: FMESH tally number
        particle: Particle type

    Returns:
        FMESH card string
    """
    gen = FMESHGenerator(tally_number, particle)

    # Logarithmic radial spacing
    r_bounds = np.logspace(np.log10(r_min), np.log10(r_max), r_bins + 1)[1:]
    r_intervals = [1] * r_bins

    # Uniform axial spacing
    z_bounds = [z_max]
    z_intervals = [z_bins]

    # Full azimuth
    theta_bounds = [360]
    theta_intervals = [36]

    gen.set_cylindrical(
        origin=origin,
        axis=(0, 0, 1),
        vec=(1, 0, 0),
        r_bounds=r_bounds.tolist(),
        r_bins=r_intervals,
        z_bounds=z_bounds,
        z_bins=z_intervals,
        theta_bounds=theta_bounds,
        theta_bins=theta_intervals
    )

    return gen.generate()


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description='Generate FMESH cards for MCNP6')

    parser.add_argument('--geometry', choices=['XYZ', 'RZT'], default='XYZ',
                        help='Mesh geometry type')
    parser.add_argument('--origin', nargs=3, type=float, default=[0, 0, 0],
                        help='Mesh origin (x0 y0 z0)')
    parser.add_argument('--extent', nargs=3, type=float, required=True,
                        help='Mesh extent (x_size y_size z_size) for XYZ')
    parser.add_argument('--bins', nargs=3, type=int, default=[20, 20, 20],
                        help='Number of bins (nx ny nz)')
    parser.add_argument('--tally', type=int, default=4,
                        help='Tally number (must end in 4)')
    parser.add_argument('--particle', type=str, default='N',
                        help='Particle type (N, P, E, etc.)')
    parser.add_argument('--energy', nargs='+', type=float,
                        help='Energy bin boundaries (MeV)')
    parser.add_argument('--output', type=str, default='xdmf',
                        choices=['xdmf', 'col', 'ij', 'ik', 'jk', 'none'],
                        help='Output format')

    args = parser.parse_args()

    if args.geometry == 'XYZ':
        card = create_uniform_cartesian(
            origin=tuple(args.origin),
            extent=tuple(args.extent),
            bins=tuple(args.bins),
            tally_number=args.tally,
            particle=args.particle
        )
    else:
        # RZT example (simplified)
        card = create_logarithmic_radial(
            origin=tuple(args.origin),
            r_min=0.1,
            r_max=args.extent[0],
            r_bins=args.bins[0],
            z_min=args.origin[2],
            z_max=args.origin[2] + args.extent[2],
            z_bins=args.bins[2],
            tally_number=args.tally,
            particle=args.particle
        )

    print(card)
    print()

    # Calculate total bins
    gen = FMESHGenerator(args.tally, args.particle)
    if args.geometry == 'XYZ':
        gen.set_cartesian(
            tuple(args.origin),
            [args.origin[0] + args.extent[0]], [args.bins[0]],
            [args.origin[1] + args.extent[1]], [args.bins[1]],
            [args.origin[2] + args.extent[2]], [args.bins[2]]
        )

    if args.energy:
        gen.set_energy_bins(args.energy)

    total_bins = gen.calculate_bins()
    print(f"c Total bins: {total_bins:,}")


if __name__ == '__main__':
    main()
