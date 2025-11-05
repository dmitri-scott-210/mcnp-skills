#!/usr/bin/env python3
"""
Lattice Index Calculator - Calculate and visualize lattice indices

Usage:
    python lattice_index_calculator.py --type LAT1 --surfaces "10 11 12 13 14 15"
    python lattice_index_calculator.py --from-file input.i --cell 100

Purpose:
    - Interpret surface ordering on LAT cell card
    - Visualize which direction each index (i,j,k) varies
    - Generate ASCII diagram showing index scheme
    - Help debug lattice index mismatches

Author: MCNP Lattice Builder Skill
Version: 1.0.0
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Calculate MCNP lattice indices")
    parser.add_argument("--type", choices=["LAT1", "LAT2"], help="Lattice type")
    parser.add_argument("--surfaces", help="Surface list (space-separated)")
    parser.add_argument("--from-file", help="Extract from MCNP input file")
    parser.add_argument("--cell", type=int, help="Cell number to analyze")

    args = parser.parse_args()

    if args.from_file:
        # Parse MCNP input file
        print(f"Analyzing lattice in file: {args.from_file}, cell {args.cell}")
        # TODO: Implement file parsing
        print("ERROR: File parsing not yet implemented")
        print("Use --type and --surfaces for now")
        return 1

    if not args.type or not args.surfaces:
        print("ERROR: Must specify --type and --surfaces")
        parser.print_help()
        return 1

    surfaces = args.surfaces.split()

    if args.type == "LAT1":
        analyze_lat1(surfaces)
    elif args.type == "LAT2":
        analyze_lat2(surfaces)

    return 0

def analyze_lat1(surfaces):
    """Analyze LAT=1 (hexahedral) lattice"""
    if len(surfaces) != 6:
        print(f"ERROR: LAT=1 requires exactly 6 surfaces, got {len(surfaces)}")
        return

    print("\nLAT=1 Rectangular Lattice Analysis")
    print("="*50)
    print(f"\nSurface ordering: {' '.join(surfaces)}")
    print("\nInterpretation:")
    print(f"  Surfaces {surfaces[0]}, {surfaces[1]} → i-index (X direction)")
    print(f"  Surfaces {surfaces[2]}, {surfaces[3]} → j-index (Y direction)")
    print(f"  Surfaces {surfaces[4]}, {surfaces[5]} → k-index (Z direction)")
    print("\nIndex scheme:")
    print("  i varies FASTEST (innermost loop)")
    print("  j varies MIDDLE (middle loop)")
    print("  k varies SLOWEST (outermost loop)")
    print("\nFILL array ordering: k-planes, then j-rows, then i-columns")
    print("\nExample for 3×3×2 lattice:")
    print("  FILL=0:2 0:2 0:1")
    print("       <k=0 plane>")
    print("       1 2 3    $ j=0, i=0:2")
    print("       4 5 6    $ j=1, i=0:2")
    print("       7 8 9    $ j=2, i=0:2")
    print("       <k=1 plane>")
    print("       10 11 12 $ j=0, i=0:2")
    print("       13 14 15 $ j=1, i=0:2")
    print("       16 17 18 $ j=2, i=0:2")

def analyze_lat2(surfaces):
    """Analyze LAT=2 (hexagonal prism) lattice"""
    if len(surfaces) != 8:
        print(f"ERROR: LAT=2 requires exactly 8 surfaces, got {len(surfaces)}")
        return

    print("\nLAT=2 Hexagonal Prism Lattice Analysis")
    print("="*50)
    print(f"\nSurface ordering: {' '.join(surfaces)}")
    print("\nInterpretation:")
    print(f"  Surfaces {surfaces[0:6]} → 6 hex prism sides")
    print(f"  Surfaces {surfaces[6]}, {surfaces[7]} → bottom and top (k-direction)")
    print("\nHexagon orientation:")
    print("  FLAT sides on LEFT and RIGHT (MCNP convention)")
    print("  POINTS facing UP and DOWN")
    print("\nIndex scheme (hexagonal):")
    print("  Central element: [0,0,k]")
    print("  +X direction: [1,0,k]")
    print("  +Y direction: [0,1,k]")
    print("  See MCNP6 Manual 3.3.4.1 for complete indexing")

if __name__ == "__main__":
    sys.exit(main())
