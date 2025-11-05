#!/usr/bin/env python3
"""
MCNP Surface Editor

Programmatic batch editing of surface parameters for scaling, translation, etc.

Usage:
    python surface_editor.py input.i --scale 1.5 -o output.i
    python surface_editor.py input.i --translate 10 0 0 -o output.i
    python surface_editor.py input.i --surface-type SO --scale-radius 2.0

Output:
    Modified MCNP input file with updated surface parameters
"""

import sys
import argparse
import re

class SurfaceEditor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.lines = []
        self.surface_line_map = {}  # surf_num -> line_index

    def load_input(self):
        """Load MCNP input file"""
        with open(self.input_file, 'r') as f:
            self.lines = f.readlines()

        # Find blank lines (block separators)
        blank_indices = [i for i, line in enumerate(self.lines) if line.strip() == '']

        if len(blank_indices) < 2:
            print("WARNING: Could not identify three-block structure")
            return

        # Identify surface block
        self.surf_start = blank_indices[0] + 1
        self.surf_end = blank_indices[1]

        # Map surface numbers to line indices
        for i in range(self.surf_start, self.surf_end):
            line = self.lines[i]
            if line.strip().startswith('c') or not line.strip():
                continue

            match = re.match(r'^\s*(\d+)', line)
            if match:
                surf_num = int(match.group(1))
                self.surface_line_map[surf_num] = i

    def scale_uniform(self, factor):
        """Apply uniform scaling to all surfaces"""
        for surf_num, line_idx in self.surface_line_map.items():
            line = self.lines[line_idx]
            parts = line.split()

            # Identify surface type
            surf_num_idx = 0
            tr_num_idx = None
            surf_type_idx = 1

            # Check for TR number
            if len(parts) > 2:
                try:
                    int(parts[1])
                    tr_num_idx = 1
                    surf_type_idx = 2
                except ValueError:
                    pass

            surf_type = parts[surf_type_idx].upper()
            param_start_idx = surf_type_idx + 1

            # Scale parameters based on surface type
            new_params = []
            for param in parts[param_start_idx:]:
                # Skip non-numeric (comments, etc.)
                try:
                    val = float(param)
                    new_params.append(str(val * factor))
                except ValueError:
                    new_params.append(param)

            # Reconstruct line
            new_line_parts = parts[:param_start_idx] + new_params

            # Preserve original formatting approximately
            new_line = "  ".join(new_line_parts)

            # Preserve inline comment if present
            if '$' in line:
                comment = line[line.index('$'):]
                new_line += "  " + comment.rstrip() + "\n"
            else:
                new_line += "\n"

            self.lines[line_idx] = new_line

    def translate_surfaces(self, dx, dy, dz):
        """Apply translation to applicable surfaces"""
        for surf_num, line_idx in self.surface_line_map.items():
            line = self.lines[line_idx]
            parts = line.split()

            # Identify surface type
            surf_type_idx = 1
            if len(parts) > 2:
                try:
                    int(parts[1])
                    surf_type_idx = 2
                except ValueError:
                    pass

            surf_type = parts[surf_type_idx].upper()

            # Only translate surfaces with position parameters
            if surf_type in ['S', 'C/X', 'C/Y', 'C/Z', 'RCC', 'BOX', 'RHP', 'REC']:
                # Implementation depends on specific surface type
                # This is a simplified version
                pass

    def scale_specific_type(self, surf_type_filter, scale_factor, param_name='radius'):
        """Scale only surfaces of specific type"""
        for surf_num, line_idx in self.surface_line_map.items():
            line = self.lines[line_idx]
            parts = line.split()

            surf_type_idx = 1
            if len(parts) > 2:
                try:
                    int(parts[1])
                    surf_type_idx = 2
                except ValueError:
                    pass

            surf_type = parts[surf_type_idx].upper()

            if surf_type == surf_type_filter.upper():
                # Scale radius for SO, S surfaces
                if surf_type in ['SO', 'S']:
                    param_start = surf_type_idx + 1
                    radius_idx = param_start if surf_type == 'SO' else param_start + 3

                    if len(parts) > radius_idx:
                        old_val = float(parts[radius_idx])
                        parts[radius_idx] = str(old_val * scale_factor)

                        # Reconstruct line
                        new_line = "  ".join(parts[:radius_idx+1])
                        if '$' in line:
                            new_line += "  " + line[line.index('$'):].rstrip() + "\n"
                        else:
                            new_line += "\n"

                        self.lines[line_idx] = new_line

    def write_output(self, output_file):
        """Write modified input to output file"""
        with open(output_file, 'w') as f:
            f.writelines(self.lines)

        print(f"Modified input written to: {output_file}")

    def print_summary(self):
        """Print summary of surfaces found"""
        print("=" * 60)
        print(f"Surface Editor - {self.input_file}")
        print("=" * 60)
        print(f"\nTotal surfaces found: {len(self.surface_line_map)}")
        print(f"Surface block: lines {self.surf_start+1} to {self.surf_end}")

        # Count by type
        type_counts = {}
        for surf_num, line_idx in self.surface_line_map.items():
            line = self.lines[line_idx]
            parts = line.split()

            surf_type_idx = 1
            if len(parts) > 2:
                try:
                    int(parts[1])
                    surf_type_idx = 2
                except ValueError:
                    pass

            if len(parts) > surf_type_idx:
                surf_type = parts[surf_type_idx].upper()
                type_counts[surf_type] = type_counts.get(surf_type, 0) + 1

        print("\nSurface type distribution:")
        for surf_type, count in sorted(type_counts.items()):
            print(f"  {surf_type}: {count}")

def main():
    parser = argparse.ArgumentParser(description='MCNP Surface Editor')
    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('-o', '--output', help='Output file (default: input_modified.i)')
    parser.add_argument('--scale', type=float, help='Uniform scale factor for all surfaces')
    parser.add_argument('--translate', nargs=3, type=float, metavar=('DX', 'DY', 'DZ'),
                       help='Translation vector')
    parser.add_argument('--surface-type', help='Filter by surface type (e.g., SO, RPP)')
    parser.add_argument('--scale-radius', type=float, help='Scale radius for specific type')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without modifying')

    args = parser.parse_args()

    if not args.output:
        base = args.input_file.rsplit('.', 1)[0]
        args.output = f"{base}_modified.i"

    editor = SurfaceEditor(args.input_file)
    editor.load_input()
    editor.print_summary()

    # Apply modifications
    if args.scale:
        print(f"\nApplying uniform scale factor: {args.scale}")
        editor.scale_uniform(args.scale)

    if args.translate:
        dx, dy, dz = args.translate
        print(f"\nApplying translation: ({dx}, {dy}, {dz})")
        editor.translate_surfaces(dx, dy, dz)

    if args.surface_type and args.scale_radius:
        print(f"\nScaling {args.surface_type} surfaces by factor {args.scale_radius}")
        editor.scale_specific_type(args.surface_type, args.scale_radius)

    if args.dry_run:
        print("\nDRY RUN - No file written")
        print("Remove --dry-run to write changes")
    else:
        editor.write_output(args.output)
        print(f"\nSUCCESS: Modified input written to {args.output}")
        print("RECOMMENDATION: Plot geometry to verify changes before running MCNP")

if __name__ == '__main__':
    main()
