#!/usr/bin/env python3
"""
MCNP Volume Calculator

Calculates cell volumes after scaling operations and updates VOL parameters.

Usage:
    python volume_calculator.py input.i --scale 1.5
    python volume_calculator.py input.i --scale-xyz 2.0 1.0 1.5
    python volume_calculator.py input.i --update-volumes

Output:
    - Volume calculations for simple geometries
    - Updated input file with corrected VOL parameters
"""

import sys
import argparse
import re
import math

class VolumeCalculator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.cells = {}
        self.surfaces = {}

    def parse_input(self):
        """Parse MCNP input to extract cells and surfaces"""
        with open(self.input_file, 'r') as f:
            lines = f.readlines()

        # Find blank lines (block separators)
        blank_indices = [i for i, line in enumerate(lines) if line.strip() == '']

        if len(blank_indices) < 2:
            print("WARNING: Could not identify three-block structure")
            return

        # Parse cells
        cell_start = 1
        cell_end = blank_indices[0]
        self._parse_cells(lines[cell_start:cell_end])

        # Parse surfaces
        surf_start = blank_indices[0] + 1
        surf_end = blank_indices[1]
        self._parse_surfaces(lines[surf_start:surf_end])

    def _parse_cells(self, lines):
        """Extract cell definitions with current VOL parameters"""
        for line in lines:
            if line.strip().startswith('c'):
                continue
            if not line.strip():
                continue

            # Look for VOL parameter
            vol_match = re.search(r'VOL[=\s]+([\d.eE+-]+)', line, re.IGNORECASE)
            cell_match = re.match(r'^\s*(\d+)', line)

            if cell_match:
                cell_num = int(cell_match.group(1))
                current_vol = float(vol_match.group(1)) if vol_match else None

                self.cells[cell_num] = {
                    'line': line,
                    'current_vol': current_vol
                }

    def _parse_surfaces(self, lines):
        """Extract surface definitions for volume calculation"""
        for line in lines:
            if line.strip().startswith('c'):
                continue
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            try:
                surf_num = int(parts[0])
            except ValueError:
                continue

            # Check for TR number
            tr_num = None
            surf_type_idx = 1
            if len(parts) > 2:
                try:
                    potential_tr = int(parts[1])
                    tr_num = potential_tr
                    surf_type_idx = 2
                except ValueError:
                    pass

            surf_type = parts[surf_type_idx] if surf_type_idx < len(parts) else 'UNKNOWN'
            params = parts[surf_type_idx+1:] if surf_type_idx+1 < len(parts) else []

            self.surfaces[surf_num] = {
                'type': surf_type.upper(),
                'params': params
            }

    def calculate_simple_volumes(self):
        """Calculate volumes for simple geometries"""
        volumes = {}

        for surf_num, surf in self.surfaces.items():
            surf_type = surf['type']
            params = surf['params']

            try:
                if surf_type == 'SO':
                    # Sphere at origin: V = 4/3 π R³
                    R = float(params[0])
                    V = (4/3) * math.pi * R**3
                    volumes[surf_num] = ('SO', R, V)

                elif surf_type == 'S':
                    # General sphere: V = 4/3 π R³
                    R = float(params[3])
                    V = (4/3) * math.pi * R**3
                    volumes[surf_num] = ('S', R, V)

                elif surf_type == 'RPP':
                    # Rectangular parallelepiped
                    xmin, xmax = float(params[0]), float(params[1])
                    ymin, ymax = float(params[2]), float(params[3])
                    zmin, zmax = float(params[4]), float(params[5])
                    V = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)
                    volumes[surf_num] = ('RPP', (xmax-xmin, ymax-ymin, zmax-zmin), V)

                elif surf_type in ['CX', 'CY', 'CZ']:
                    # Infinite cylinder (cannot calculate without bounds)
                    pass

                elif surf_type == 'RCC':
                    # Right circular cylinder
                    vx, vy, vz = float(params[3]), float(params[4]), float(params[5])
                    R = float(params[6])
                    height = math.sqrt(vx**2 + vy**2 + vz**2)
                    V = math.pi * R**2 * height
                    volumes[surf_num] = ('RCC', (R, height), V)

            except (ValueError, IndexError):
                continue

        return volumes

    def apply_scaling(self, scale_factor, scale_xyz=None):
        """Apply scaling factor to volumes"""
        if scale_xyz:
            fx, fy, fz = scale_xyz
            volume_scale = fx * fy * fz
        else:
            volume_scale = scale_factor ** 3

        scaled_volumes = {}
        volumes = self.calculate_simple_volumes()

        for surf_num, (surf_type, dims, V) in volumes.items():
            V_scaled = V * volume_scale
            scaled_volumes[surf_num] = V_scaled

        return scaled_volumes

    def print_volume_report(self, scale_factor=None, scale_xyz=None):
        """Print volume calculation report"""
        print("=" * 60)
        print("MCNP Volume Calculator Report")
        print("=" * 60)

        volumes = self.calculate_simple_volumes()

        if not volumes:
            print("\nNo simple volumes could be calculated.")
            print("(Complex geometries require MCNP volume calculation)")
            return

        print(f"\nFound {len(volumes)} calculable surfaces")

        if scale_factor or scale_xyz:
            if scale_xyz:
                fx, fy, fz = scale_xyz
                print(f"\nScaling: fx={fx}, fy={fy}, fz={fz}")
                print(f"Volume scale factor: {fx * fy * fz:.4f}")
            else:
                print(f"\nUniform scaling: {scale_factor}")
                print(f"Volume scale factor: {scale_factor**3:.4f}")

            scaled_volumes = self.apply_scaling(scale_factor, scale_xyz)

            print("\n" + "-" * 60)
            print("SURFACE VOLUMES (Original → Scaled)")
            print("-" * 60)

            for surf_num in sorted(volumes.keys()):
                surf_type, dims, V_orig = volumes[surf_num]
                V_scaled = scaled_volumes[surf_num]

                print(f"Surface {surf_num} ({surf_type}):")
                print(f"  Original: {V_orig:.2f} cm³")
                print(f"  Scaled:   {V_scaled:.2f} cm³")

        else:
            print("\n" + "-" * 60)
            print("SURFACE VOLUMES (Original)")
            print("-" * 60)

            for surf_num in sorted(volumes.keys()):
                surf_type, dims, V = volumes[surf_num]
                print(f"Surface {surf_num} ({surf_type}): {V:.2f} cm³")

        # Check against cell VOL parameters
        print("\n" + "-" * 60)
        print("CELL VOL PARAMETER COMPARISON")
        print("-" * 60)

        for cell_num, cell_info in sorted(self.cells.items()):
            if cell_info['current_vol']:
                print(f"Cell {cell_num}: VOL={cell_info['current_vol']:.2f} cm³")

def main():
    parser = argparse.ArgumentParser(description='MCNP Volume Calculator')
    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--scale', type=float, help='Uniform scale factor')
    parser.add_argument('--scale-xyz', nargs=3, type=float, metavar=('FX', 'FY', 'FZ'),
                       help='Non-uniform scale factors')
    parser.add_argument('--update-volumes', action='store_true',
                       help='Update VOL parameters in input file (NOT YET IMPLEMENTED)')

    args = parser.parse_args()

    calculator = VolumeCalculator(args.input_file)
    calculator.parse_input()

    if args.update_volumes:
        print("ERROR: --update-volumes not yet implemented")
        print("Use output values to manually update VOL parameters")
        sys.exit(1)

    calculator.print_volume_report(args.scale, args.scale_xyz)

    if args.scale or args.scale_xyz:
        print("\n" + "=" * 60)
        print("RECOMMENDATION")
        print("=" * 60)
        print("\nUpdate cell VOL parameters with scaled values shown above.")
        print("Manual update required for accuracy.")

if __name__ == '__main__':
    main()
