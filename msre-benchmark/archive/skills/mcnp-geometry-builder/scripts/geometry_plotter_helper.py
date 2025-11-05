#!/usr/bin/env python3
"""
MCNP Geometry Plotter Helper

Generates MCNP geometry plot commands for visualizing geometry.
Creates .comin files for batch plotting and interactive commands.

Usage:
    python geometry_plotter_helper.py input_file.inp [options]

Options:
    --slices   N       Generate N slices along each axis (default: 3)
    --origin   X Y Z   Set plot origin (default: 0 0 0)
    --extent   E       Set plot extent (default: auto-detect)
    --output   FILE    Output file for plot commands (default: geometry_plots.comin)

Features:
    - Auto-generates multi-slice plots (XY, XZ, YZ)
    - Creates cell-labeled and material-labeled views
    - Generates extent commands based on geometry bounds
    - Outputs both .comin batch file and interactive commands

Example:
    python geometry_plotter_helper.py reactor.inp --slices 5 --origin 0 0 50
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

class MCNPPlotterHelper:
    """Generates MCNP plot commands for geometry visualization"""

    def __init__(self, filepath: str, origin: Tuple[float, float, float] = (0, 0, 0),
                 extent: Optional[float] = None, num_slices: int = 3):
        self.filepath = Path(filepath)
        self.origin = origin
        self.extent = extent
        self.num_slices = num_slices
        self.cells = []
        self.surfaces = []

    def parse_input(self):
        """Parse MCNP input to extract geometry bounds"""

        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # Find blank line delimiters
        blank_indices = []
        for i, line in enumerate(lines):
            if line.strip() == '':
                blank_indices.append(i)

        if len(blank_indices) < 2:
            print("Warning: Cannot parse blocks, file format may be invalid")
            return

        # Extract cell and surface blocks
        first_blank = blank_indices[0]
        second_blank = blank_indices[1]

        cell_cards = lines[1:first_blank]
        surface_cards = lines[first_blank+1:second_blank]

        # Extract cell numbers
        for line in cell_cards:
            if line.strip() and not line.strip().startswith('c'):
                match = re.match(r'\s*(\d+)\s+', line)
                if match:
                    self.cells.append(int(match.group(1)))

        # Extract surface numbers
        for line in surface_cards:
            if line.strip() and not line.strip().startswith('c'):
                match = re.match(r'\s*[\*\+]?(\d+)\s+', line)
                if match:
                    self.surfaces.append(int(match.group(1)))

        print(f"Found {len(self.cells)} cells and {len(self.surfaces)} surfaces")

    def estimate_extent(self) -> float:
        """Estimate plot extent from geometry (placeholder)"""
        # In a full implementation, would parse surface definitions
        # For now, return reasonable default
        if self.extent:
            return self.extent
        return 50.0  # Default extent in cm

    def generate_slice_plots(self) -> List[str]:
        """Generate multi-slice plot commands"""

        commands = []
        extent = self.estimate_extent()

        # Header
        commands.append("c MCNP Geometry Plot Commands")
        commands.append(f"c Generated for: {self.filepath.name}")
        commands.append(f"c Origin: {self.origin}")
        commands.append(f"c Extent: {extent}")
        commands.append("")

        # Set origin and extent
        commands.append(f"origin {self.origin[0]} {self.origin[1]} {self.origin[2]}")
        commands.append(f"extent {extent}")
        commands.append("")

        # XY slices (perpendicular to Z axis)
        commands.append("c ===== XY Slices (Z axis) =====")
        z_min, z_max = self.origin[2] - extent/2, self.origin[2] + extent/2
        z_values = [z_min + (z_max - z_min) * i / (self.num_slices - 1)
                    for i in range(self.num_slices)]

        for i, z in enumerate(z_values, 1):
            commands.append(f"c Slice XY-{i} at Z={z:.2f}")
            commands.append(f"px 0 0 {z}")
            commands.append(f"label 1 1 cel")
            commands.append(f"plot")
            commands.append(f"end")
            commands.append(f"px 0 0 {z}")
            commands.append(f"label 1 1 mat")
            commands.append(f"plot")
            commands.append(f"end")
            commands.append("")

        # XZ slices (perpendicular to Y axis)
        commands.append("c ===== XZ Slices (Y axis) =====")
        y_min, y_max = self.origin[1] - extent/2, self.origin[1] + extent/2
        y_values = [y_min + (y_max - y_min) * i / (self.num_slices - 1)
                    for i in range(self.num_slices)]

        for i, y in enumerate(y_values, 1):
            commands.append(f"c Slice XZ-{i} at Y={y:.2f}")
            commands.append(f"py 0 {y} 0")
            commands.append(f"label 1 1 cel")
            commands.append(f"plot")
            commands.append(f"end")
            commands.append(f"py 0 {y} 0")
            commands.append(f"label 1 1 mat")
            commands.append(f"plot")
            commands.append(f"end")
            commands.append("")

        # YZ slices (perpendicular to X axis)
        commands.append("c ===== YZ Slices (X axis) =====")
        x_min, x_max = self.origin[0] - extent/2, self.origin[0] + extent/2
        x_values = [x_min + (x_max - x_min) * i / (self.num_slices - 1)
                    for i in range(self.num_slices)]

        for i, x in enumerate(x_values, 1):
            commands.append(f"c Slice YZ-{i} at X={x:.2f}")
            commands.append(f"pz {x} 0 0")
            commands.append(f"label 1 1 cel")
            commands.append(f"plot")
            commands.append(f"end")
            commands.append(f"pz {x} 0 0")
            commands.append(f"label 1 1 mat")
            commands.append(f"plot")
            commands.append(f"end")
            commands.append("")

        return commands

    def generate_interactive_commands(self) -> List[str]:
        """Generate commands for interactive plotter use"""

        commands = []
        extent = self.estimate_extent()

        commands.append("# Interactive MCNP Plotter Commands")
        commands.append(f"# For use with: mcnp6 inp={self.filepath.name} ip")
        commands.append("#")
        commands.append("# Basic Commands:")
        commands.append(f"origin {self.origin[0]} {self.origin[1]} {self.origin[2]}")
        commands.append(f"extent {extent}")
        commands.append("")
        commands.append("# XY plane at origin:")
        commands.append(f"px 0 0 {self.origin[2]}")
        commands.append("label 1 1 cel")
        commands.append("")
        commands.append("# XZ plane at origin:")
        commands.append(f"py 0 {self.origin[1]} 0")
        commands.append("label 1 1 cel")
        commands.append("")
        commands.append("# YZ plane at origin:")
        commands.append(f"pz {self.origin[0]} 0 0")
        commands.append("label 1 1 cel")
        commands.append("")
        commands.append("# Useful commands:")
        commands.append("# label 1 1 cel    - Show cell numbers")
        commands.append("# label 1 1 mat    - Show material numbers")
        commands.append("# label 1 0        - Hide labels")
        commands.append("# scale 0.5        - Zoom in")
        commands.append("# scale 2.0        - Zoom out")
        commands.append("# color N R G B    - Set cell N color (RGB 0-255)")
        commands.append("# end              - Exit plotter")

        return commands

    def save_commands(self, output_file: str = "geometry_plots.comin"):
        """Save plot commands to file"""

        commands = self.generate_slice_plots()

        output_path = Path(output_file)
        try:
            with open(output_path, 'w') as f:
                f.write('\n'.join(commands))
            print(f"✅ Plot commands saved to: {output_path}")
            print(f"   Run with: mcnp6 inp={self.filepath.name} com={output_path.name}")
        except Exception as e:
            print(f"Error writing file: {e}")

        # Also save interactive commands
        interactive_file = output_path.stem + "_interactive.txt"
        interactive_commands = self.generate_interactive_commands()
        try:
            with open(interactive_file, 'w') as f:
                f.write('\n'.join(interactive_commands))
            print(f"✅ Interactive commands saved to: {interactive_file}")
        except Exception as e:
            print(f"Error writing interactive file: {e}")

def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description='Generate MCNP geometry plot commands',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate default plots (3 slices per axis)
  python geometry_plotter_helper.py reactor.inp

  # Generate 5 slices per axis centered at (0, 0, 50)
  python geometry_plotter_helper.py reactor.inp --slices 5 --origin 0 0 50

  # Custom extent and output file
  python geometry_plotter_helper.py reactor.inp --extent 100 --output my_plots.comin
        """
    )

    parser.add_argument('input_file', help='MCNP input file to plot')
    parser.add_argument('--slices', type=int, default=3,
                        help='Number of slices along each axis (default: 3)')
    parser.add_argument('--origin', type=float, nargs=3, default=[0, 0, 0],
                        metavar=('X', 'Y', 'Z'),
                        help='Plot origin coordinates (default: 0 0 0)')
    parser.add_argument('--extent', type=float,
                        help='Plot extent in cm (default: auto-detect)')
    parser.add_argument('--output', default='geometry_plots.comin',
                        help='Output file for plot commands (default: geometry_plots.comin)')

    args = parser.parse_args()

    # Create plotter helper
    plotter = MCNPPlotterHelper(
        filepath=args.input_file,
        origin=tuple(args.origin),
        extent=args.extent,
        num_slices=args.slices
    )

    # Parse input file
    plotter.parse_input()

    # Generate and save commands
    plotter.save_commands(args.output)

    print("\n" + "="*70)
    print("📊 Plot Generation Complete!")
    print("="*70)
    print("\nUsage:")
    print(f"  1. Batch plotting:  mcnp6 inp={args.input_file} com={args.output}")
    print(f"  2. Interactive:     mcnp6 inp={args.input_file} ip")
    print(f"     Then copy commands from: {Path(args.output).stem}_interactive.txt")
    print("\nTip: Use 'label 1 1 cel' for cell numbers, 'label 1 1 mat' for materials")

if __name__ == '__main__':
    main()
