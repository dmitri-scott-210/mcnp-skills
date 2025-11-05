#!/usr/bin/env python3
"""
Reactor Spec to Lattice - Generate MCNP lattice from reactor specifications

Usage:
    python reactor_spec_to_lattice.py --pitch 1.26 --size 17 --enrichment 4.5
    python reactor_spec_to_lattice.py --config pwr_assembly.json
    python reactor_spec_to_lattice.py --interactive

Purpose:
    - Generate MCNP lattice skeleton from design specifications
    - Calculate surface positions from pitch
    - Create material card templates
    - Suggest volume specifications
    - Output complete lattice structure for user to fill

Author: MCNP Lattice Builder Skill
Version: 1.0.0
"""

import sys
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Generate MCNP lattice from specs")
    parser.add_argument("--pitch", type=float, help="Pin pitch (cm)")
    parser.add_argument("--size", type=int, help="Assembly size (N×N)")
    parser.add_argument("--enrichment", type=float, help="U-235 enrichment (%)")
    parser.add_argument("--height", type=float, default=400.0, help="Active height (cm)")
    parser.add_argument("--config", help="JSON configuration file")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--output", help="Output file (default: stdout)")

    args = parser.parse_args()

    # Get parameters
    if args.config:
        with open(args.config, 'r') as f:
            params = json.load(f)
    elif args.interactive:
        params = interactive_input()
    elif args.pitch and args.size and args.enrichment:
        params = {
            'pitch': args.pitch,
            'size': args.size,
            'enrichment': args.enrichment,
            'height': args.height
        }
    else:
        print("ERROR: Must specify --pitch, --size, --enrichment OR --config OR --interactive")
        parser.print_help()
        return 1

    # Generate lattice
    output = generate_lattice(params)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Lattice written to: {args.output}")
    else:
        print(output)

    return 0

def interactive_input():
    """Prompt user for parameters"""
    print("Interactive Lattice Generator")
    print("=" * 50)
    pitch = float(input("Pin pitch (cm): "))
    size = int(input("Assembly size (N×N): "))
    enrichment = float(input("U-235 enrichment (%): "))
    height = float(input("Active height (cm) [400]: ") or "400")
    return {
        'pitch': pitch,
        'size': size,
        'enrichment': enrichment,
        'height': height
    }

def generate_lattice(params):
    """Generate MCNP lattice input"""
    pitch = params['pitch']
    size = params['size']
    enrich = params['enrichment']
    height = params['height']

    total_width = pitch * size
    enrich_frac = enrich / 100.0
    u238_frac = 1.0 - enrich_frac

    output = []
    output.append(f"c Generated Lattice: {size}×{size} Assembly, {pitch} cm pitch")
    output.append(f"c Enrichment: {enrich}% U-235")
    output.append("c " + "=" * 70)
    output.append("")
    output.append("c " + "=" * 70)
    output.append("c BLOCK 1: Cell Cards")
    output.append("c " + "=" * 70)
    output.append("c --- Universe 1: Fuel Pin (User must complete) ---")
    output.append("1    1  -10.5  -1         U=1  IMP:N=1  VOL=<calculate>   $ UO2 fuel")
    output.append("2    0          1  -2     U=1  IMP:N=1  VOL=<calculate>   $ Gap")
    output.append("3    2  -6.5    2  -3     U=1  IMP:N=1  VOL=<calculate>   $ Clad")
    output.append("4    3  -1.0    3         U=1  IMP:N=1  VOL=<calculate>   $ Water")
    output.append("")
    output.append(f"c --- Universe 10: {size}×{size} Pin Lattice ---")
    output.append(f"100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1")
    output.append(f"c    All {size*size} positions filled with universe 1")
    output.append(f"c    To add guide tubes/control rods: Use FILL array with U=1,2,etc.")
    output.append("")
    output.append("c --- Real World: Assembly Container ---")
    output.append("1000 0  -1000  FILL=10  IMP:N=1")
    output.append("1001 3  -1.0  1000 -1001  IMP:N=1                        $ Water reflector")
    output.append("1002 0  1001  IMP:N=0                                    $ Graveyard")
    output.append("")
    output.append("c " + "=" * 70)
    output.append("c BLOCK 2: Surface Cards")
    output.append("c " + "=" * 70)
    output.append("c --- Pin Surfaces (Universe 1) - User must specify radii ---")
    output.append("1    CZ   <fuel_radius>                                  $ Fuel radius")
    output.append("2    CZ   <gap_radius>                                   $ Gap outer")
    output.append("3    CZ   <clad_radius>                                  $ Clad outer")
    output.append("")
    output.append(f"c --- Lattice Element Boundaries ({size}×{size} array, {pitch} cm pitch) ---")
    output.append(f"10   PX   0.0                                          $ -X boundary")
    output.append(f"11   PX   {total_width:.2f}                                       $ +X boundary ({size}×{pitch})")
    output.append(f"12   PY   0.0                                          $ -Y boundary")
    output.append(f"13   PY   {total_width:.2f}                                       $ +Y boundary")
    output.append(f"14   PZ   0.0                                          $ Bottom")
    output.append(f"15   PZ   {height:.1f}                                       $ Top")
    output.append("")
    output.append("c --- Container Boundaries ---")
    output.append(f"1000 RPP  -2.0  {total_width+2:.2f}  -2.0  {total_width+2:.2f}  -2.0  {height+2:.1f}")
    output.append(f"1001 RPP  -10.0  {total_width+10:.2f}  -10.0  {total_width+10:.2f}  -10.0  {height+10:.1f}")
    output.append("")
    output.append("c " + "=" * 70)
    output.append("c BLOCK 3: Data Cards")
    output.append("c " + "=" * 70)
    output.append("MODE  N")
    output.append(f"c --- Materials ({enrich}% enriched UO2) ---")
    output.append(f"M1   92235.80c  {enrich_frac:.6f}  92238.80c  {u238_frac:.6f}  8016.80c  2.0")
    output.append("M2   40000.80c  -0.98  26000.80c  -0.01  24000.80c  -0.005  &")
    output.append("     28000.80c  -0.005")
    output.append("M3   1001.80c  2  8016.80c  1")
    output.append("MT3  LWTR.01T")
    output.append("c --- Source Definition (User must specify) ---")
    output.append("c SDEF  ...  or  KCODE ...")
    output.append("c --- Tallies (User must specify) ---")
    output.append("c F4:N  ...")
    output.append("c --- Problem Termination ---")
    output.append("NPS   100000")
    output.append("PRINT")
    output.append("")
    output.append("c " + "=" * 70)
    output.append("c USER MUST COMPLETE:")
    output.append("c   1. Pin surface radii (cards 1-3)")
    output.append("c   2. VOL parameters (calculate from geometry)")
    output.append("c   3. Source definition (SDEF or KCODE)")
    output.append("c   4. Tally definitions (F4, F7, etc.)")
    output.append("c   5. FILL array if non-uniform (guide tubes, etc.)")
    output.append("c " + "=" * 70)

    return '\n'.join(output)

if __name__ == "__main__":
    sys.exit(main())
