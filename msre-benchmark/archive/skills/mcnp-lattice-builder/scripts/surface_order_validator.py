#!/usr/bin/env python3
"""
Surface Order Validator - Check surface ordering on LAT cell cards

Usage:
    python surface_order_validator.py input.i --cell 100
    python surface_order_validator.py input.i --all-lattices

Purpose:
    - Extract surface list from LAT cell cards
    - Validate LAT=1 has 6 surfaces, LAT=2 has 8 surfaces
    - Interpret surface order as index directions
    - Suggest corrections if ordering seems wrong
    - Generate geometry plot commands for verification

Author: MCNP Lattice Builder Skill
Version: 1.0.0
"""

import sys
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Validate MCNP lattice surface ordering")
    parser.add_argument("input_file", help="MCNP input file")
    parser.add_argument("--cell", type=int, help="Specific lattice cell to check")
    parser.add_argument("--all-lattices", action="store_true", help="Check all lattice cells")

    args = parser.parse_args()

    print(f"Checking surface ordering in: {args.input_file}")
    print()

    # Parse lattice cells
    lattices = parse_lattice_cells(args.input_file)

    if not lattices:
        print("No lattice cells (LAT parameter) found in input")
        return 1

    # Filter by cell if specified
    if args.cell:
        if args.cell in lattices:
            lattices = {args.cell: lattices[args.cell]}
        else:
            print(f"ERROR: Cell {args.cell} not found or not a lattice cell")
            return 1

    # Validate each lattice
    for cell_num, lat_info in sorted(lattices.items()):
        validate_lattice(cell_num, lat_info)
        print()

    return 0

def parse_lattice_cells(filename):
    """Extract lattice cell information from input file"""
    lattices = {}  # {cell_num: {type, universe, surfaces, fill}}
    try:
        with open(filename, 'r') as f:
            content = f.read()
            # Find cell cards with LAT parameter
            # This is simplified - production version would handle continuations properly
            for line in content.split('\n'):
                if 'LAT' in line.upper() and not line.strip().startswith('c'):
                    # Extract cell number
                    cell_match = re.match(r'\s*(\d+)', line)
                    if not cell_match:
                        continue
                    cell_num = int(cell_match.group(1))

                    # Extract LAT type
                    lat_match = re.search(r'\bLAT\s*=\s*([12])', line, re.IGNORECASE)
                    if not lat_match:
                        continue
                    lat_type = int(lat_match.group(1))

                    # Extract universe
                    u_match = re.search(r'\bU\s*=\s*(\d+)', line, re.IGNORECASE)
                    universe = int(u_match.group(1)) if u_match else None

                    # Extract surfaces (simplified - assumes they're on same line)
                    # Look for geometry specification (between material/density and parameters)
                    # Pattern: cell# mat density surfaces params
                    parts = line.split()
                    surfaces = []
                    in_geom = False
                    for part in parts[3:]:  # Skip cell#, mat, density
                        if part.upper().startswith(('U=', 'LAT=', 'FILL=', 'IMP:')):
                            break
                        if part.startswith(('-', '+')):
                            surfaces.append(part)
                            in_geom = True
                        elif in_geom and part.isdigit():
                            surfaces.append(part)

                    lattices[cell_num] = {
                        'type': lat_type,
                        'universe': universe,
                        'surfaces': surfaces
                    }
    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)
    return lattices

def validate_lattice(cell_num, lat_info):
    """Validate a single lattice cell"""
    lat_type = lat_info['type']
    surfaces = lat_info['surfaces']
    universe = lat_info['universe']

    print(f"Cell {cell_num}: LAT={lat_type}, U={universe}")
    print(f"  Surfaces: {' '.join(surfaces)}")
    print()

    # Check surface count
    expected = 6 if lat_type == 1 else 8
    if len(surfaces) != expected:
        print(f"  ⚠ WARNING: LAT={lat_type} requires {expected} surfaces, found {len(surfaces)}")
        print()
        return

    # Interpret ordering
    if lat_type == 1:
        interpret_lat1(surfaces)
    else:
        interpret_lat2(surfaces)

    # Generate plot commands
    print("\n  Verification commands:")
    print(f"    mcnp6 inp=<file> ip")
    print(f"    Plot: origin at lattice center")
    print(f"    Display lattice indices (LAT=1 option)")
    print(f"    Verify index directions match expected")

def interpret_lat1(surfaces):
    """Interpret LAT=1 (rectangular) surface ordering"""
    print("  LAT=1 Rectangular Lattice Interpretation:")
    print(f"    Surfaces {surfaces[0]}, {surfaces[1]} → i-index (varies in X)")
    print(f"    Surfaces {surfaces[2]}, {surfaces[3]} → j-index (varies in Y)")
    print(f"    Surfaces {surfaces[4]}, {surfaces[5]} → k-index (varies in Z)")
    print()
    print("  Index ordering: i fastest, j middle, k slowest")
    print("  FILL array: List k-planes, then j-rows, then i-columns")
    print()
    print("  Expected element positions:")
    print("    [0,0,0]: Near surfaces", surfaces[0], surfaces[2], surfaces[4])
    print("    [imax,jmax,kmax]: Near surfaces", surfaces[1], surfaces[3], surfaces[5])

def interpret_lat2(surfaces):
    """Interpret LAT=2 (hexagonal) surface ordering"""
    print("  LAT=2 Hexagonal Prism Lattice Interpretation:")
    print(f"    Surfaces {' '.join(surfaces[0:6])} → 6 hex prism sides")
    print(f"    Surfaces {surfaces[6]}, {surfaces[7]} → bottom, top (k-direction)")
    print()
    print("  Hexagon orientation: FLAT sides LEFT/RIGHT, POINTS UP/DOWN")
    print("  Index scheme: See MCNP6 Manual 3.3.4.1 for hexagonal indexing")
    print()
    print("  Central element: [0,0,k]")
    print("  Surrounding elements: 6 neighbors in hexagonal pattern")

if __name__ == "__main__":
    sys.exit(main())
