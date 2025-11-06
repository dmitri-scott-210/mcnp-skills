#!/usr/bin/env python3
"""
Mesh Visualizer for MCNP6 Mesh Tallies

Purpose: Visualize mesh geometry and overlay on MCNP geometry for validation.
Author: MCNP Skills Project
Version: 1.0.0

Usage:
    python mesh_visualizer.py meshtal.xdmf --slice Z 0
    python mesh_visualizer.py --fmesh-card input.i --tally 4
"""

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from typing import Optional, Tuple, List

try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False
    print("Warning: h5py not available. HDF5 visualization disabled.")


class MeshVisualizer:
    """Visualize MCNP mesh tallies."""

    def __init__(self):
        self.mesh_data = None
        self.mesh_type = None

    def load_xdmf(self, xdmf_file: str):
        """
        Load mesh data from XDMF/HDF5 file.

        Args:
            xdmf_file: Path to meshtal.xdmf file
        """
        if not HAS_H5PY:
            raise ImportError("h5py required for XDMF visualization")

        # XDMF is XML metadata; actual data in HDF5
        h5_file = xdmf_file.replace('.xdmf', '.h5')

        with h5py.File(h5_file, 'r') as f:
            # Load mesh geometry
            if 'mesh' in f:
                self.mesh_data = {
                    'vertices': f['mesh']['vertices'][:],
                    'connectivity': f['mesh']['connectivity'][:]
                }
            # Load tally data if present
            tallies = [k for k in f.keys() if k.startswith('tally_')]
            if tallies:
                tally = tallies[0]
                self.mesh_data['values'] = f[tally]['values'][:]
                self.mesh_data['errors'] = f[tally]['errors'][:]

        self.mesh_type = 'UM'  # Unstructured mesh

    def parse_fmesh_card(self, input_file: str, tally_number: int):
        """
        Parse FMESH card from MCNP input file.

        Args:
            input_file: Path to MCNP input file
            tally_number: FMESH tally number to parse
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Find FMESH card
        fmesh_lines = []
        in_fmesh = False

        for line in lines:
            line = line.strip()
            if line.startswith(f'FMESH{tally_number}:'):
                in_fmesh = True
                fmesh_lines.append(line)
            elif in_fmesh:
                if line.startswith('c ') or line.startswith('c') and len(line) == 1:
                    continue
                elif line.startswith('FMESH') or line.startswith('F') or line.startswith('M'):
                    break
                else:
                    fmesh_lines.append(line)

        # Parse FMESH specification
        fmesh_str = ' '.join(fmesh_lines)

        # Extract geometry type
        if 'GEOM=XYZ' in fmesh_str:
            self.mesh_type = 'XYZ'
        elif 'GEOM=RZT' in fmesh_str:
            self.mesh_type = 'RZT'
        else:
            raise ValueError("Could not determine mesh geometry type")

        # Parse origin
        origin_idx = fmesh_str.find('ORIGIN=')
        if origin_idx >= 0:
            origin_str = fmesh_str[origin_idx+7:].split()[0:3]
            origin = [float(x) for x in origin_str]
        else:
            origin = [0, 0, 0]

        # Parse mesh boundaries
        def parse_mesh_spec(keyword):
            idx = fmesh_str.find(keyword + '=')
            if idx < 0:
                return []
            vals_str = fmesh_str[idx+len(keyword)+1:].split()
            vals = []
            for v in vals_str:
                try:
                    vals.append(float(v))
                except ValueError:
                    break
            return vals

        imesh = parse_mesh_spec('IMESH')
        jmesh = parse_mesh_spec('JMESH')
        kmesh = parse_mesh_spec('KMESH')

        self.mesh_data = {
            'geometry': self.mesh_type,
            'origin': origin,
            'imesh': imesh,
            'jmesh': jmesh,
            'kmesh': kmesh
        }

    def plot_2d_slice(self, plane: str = 'XY', position: float = 0.0,
                      output_file: Optional[str] = None):
        """
        Plot 2D slice of mesh.

        Args:
            plane: Slice plane ('XY', 'XZ', 'YZ')
            position: Position along third axis
            output_file: Output file path (if None, show interactive)
        """
        if self.mesh_data is None:
            raise ValueError("No mesh data loaded")

        fig, ax = plt.subplots(figsize=(10, 8))

        if self.mesh_type == 'XYZ':
            self._plot_cartesian_slice(ax, plane, position)
        elif self.mesh_type == 'RZT':
            self._plot_cylindrical_slice(ax)
        elif self.mesh_type == 'UM':
            self._plot_um_slice(ax, plane, position)

        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'MCNP Mesh Tally - {plane} Slice at {position}')

        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"Plot saved to {output_file}")
        else:
            plt.show()

    def _plot_cartesian_slice(self, ax, plane: str, position: float):
        """Plot Cartesian (XYZ) mesh slice."""
        origin = self.mesh_data['origin']
        imesh = self.mesh_data['imesh']
        jmesh = self.mesh_data['jmesh']
        kmesh = self.mesh_data['kmesh']

        # Determine which axes to plot
        if plane == 'XY':
            x_bounds = [origin[0]] + imesh
            y_bounds = [origin[1]] + jmesh
            xlabel, ylabel = 'X (cm)', 'Y (cm)'
        elif plane == 'XZ':
            x_bounds = [origin[0]] + imesh
            y_bounds = [origin[2]] + kmesh
            xlabel, ylabel = 'X (cm)', 'Z (cm)'
        elif plane == 'YZ':
            x_bounds = [origin[1]] + jmesh
            y_bounds = [origin[2]] + kmesh
            xlabel, ylabel = 'Y (cm)', 'Z (cm)'
        else:
            raise ValueError(f"Invalid plane {plane}")

        # Draw mesh grid
        for x in x_bounds:
            ax.axvline(x, color='blue', linewidth=0.5, alpha=0.7)
        for y in y_bounds:
            ax.axhline(y, color='blue', linewidth=0.5, alpha=0.7)

        # Draw bounding box
        x_min, x_max = x_bounds[0], x_bounds[-1]
        y_min, y_max = y_bounds[0], y_bounds[-1]

        rect = Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                         fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(x_min - 5, x_max + 5)
        ax.set_ylim(y_min - 5, y_max + 5)

    def _plot_cylindrical_slice(self, ax):
        """Plot cylindrical (RZT) mesh in R-Z plane."""
        origin = self.mesh_data['origin']
        imesh = self.mesh_data.get('imesh', [])  # Radial
        jmesh = self.mesh_data.get('jmesh', [])  # Axial

        if not imesh or not jmesh:
            ax.text(0.5, 0.5, 'No mesh data to plot', ha='center', va='center')
            return

        # R-Z plot (cylindrical cross-section)
        r_bounds = [0] + imesh
        z_bounds = [origin[2]] + jmesh

        # Draw radial lines
        for r in r_bounds:
            ax.axvline(r, color='blue', linewidth=0.5, alpha=0.7)
            ax.axvline(-r, color='blue', linewidth=0.5, alpha=0.7)

        # Draw axial lines
        for z in z_bounds:
            ax.axhline(z, color='blue', linewidth=0.5, alpha=0.7)

        ax.set_xlabel('R (cm)')
        ax.set_ylabel('Z (cm)')
        ax.set_xlim(-r_bounds[-1] * 1.1, r_bounds[-1] * 1.1)
        ax.set_ylim(z_bounds[0] - 5, z_bounds[-1] + 5)

    def _plot_um_slice(self, ax, plane: str, position: float):
        """Plot unstructured mesh slice."""
        if 'vertices' not in self.mesh_data:
            ax.text(0.5, 0.5, 'UM data not loaded', ha='center', va='center')
            return

        vertices = self.mesh_data['vertices']

        # Determine which axes to plot
        if plane == 'XY':
            coords = vertices[:, :2]
            xlabel, ylabel = 'X (cm)', 'Y (cm)'
        elif plane == 'XZ':
            coords = vertices[:, [0, 2]]
            xlabel, ylabel = 'X (cm)', 'Z (cm)'
        elif plane == 'YZ':
            coords = vertices[:, [1, 2]]
            xlabel, ylabel = 'Y (cm)', 'Z (cm)'
        else:
            raise ValueError(f"Invalid plane {plane}")

        # Plot vertices
        ax.scatter(coords[:, 0], coords[:, 1], c='blue', s=1, alpha=0.5)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    def print_summary(self):
        """Print mesh summary statistics."""
        if self.mesh_data is None:
            print("No mesh data loaded")
            return

        print("\n" + "="*60)
        print("MESH SUMMARY")
        print("="*60)

        print(f"Mesh Type: {self.mesh_type}")

        if self.mesh_type in ['XYZ', 'RZT']:
            origin = self.mesh_data.get('origin', [0, 0, 0])
            print(f"Origin: ({origin[0]:.2f}, {origin[1]:.2f}, {origin[2]:.2f})")

            imesh = self.mesh_data.get('imesh', [])
            jmesh = self.mesh_data.get('jmesh', [])
            kmesh = self.mesh_data.get('kmesh', [])

            print(f"I-direction boundaries: {len(imesh)}")
            print(f"J-direction boundaries: {len(jmesh)}")
            print(f"K-direction boundaries: {len(kmesh)}")

        elif self.mesh_type == 'UM':
            n_vertices = len(self.mesh_data.get('vertices', []))
            n_elements = len(self.mesh_data.get('connectivity', []))
            print(f"Vertices: {n_vertices:,}")
            print(f"Elements: {n_elements:,}")

        print("="*60 + "\n")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description='Visualize MCNP mesh tallies')

    parser.add_argument('input', type=str, nargs='?',
                        help='Input file (meshtal.xdmf or input.i)')
    parser.add_argument('--fmesh-card', type=str,
                        help='MCNP input file with FMESH card')
    parser.add_argument('--tally', type=int, default=4,
                        help='FMESH tally number')
    parser.add_argument('--slice', type=str, choices=['XY', 'XZ', 'YZ'], default='XY',
                        help='Slice plane')
    parser.add_argument('--position', type=float, default=0.0,
                        help='Slice position along third axis')
    parser.add_argument('--output', type=str,
                        help='Output file path (PNG, PDF, etc.)')
    parser.add_argument('--summary', action='store_true',
                        help='Print mesh summary only (no plot)')

    args = parser.parse_args()

    vis = MeshVisualizer()

    # Load mesh data
    if args.input:
        if args.input.endswith('.xdmf'):
            vis.load_xdmf(args.input)
        elif args.input.endswith('.i') or args.input.endswith('.inp'):
            vis.parse_fmesh_card(args.input, args.tally)
        else:
            print("Error: Unknown file type. Use .xdmf or .i/.inp")
            sys.exit(1)
    elif args.fmesh_card:
        vis.parse_fmesh_card(args.fmesh_card, args.tally)
    else:
        parser.print_help()
        sys.exit(1)

    # Print summary
    vis.print_summary()

    # Plot
    if not args.summary:
        vis.plot_2d_slice(args.slice, args.position, args.output)


if __name__ == '__main__':
    main()
