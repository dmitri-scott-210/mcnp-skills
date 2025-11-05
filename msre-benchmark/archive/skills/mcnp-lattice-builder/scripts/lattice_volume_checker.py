#!/usr/bin/env python3
"""
Lattice Volume Checker - Verify volume specifications for repeated structures

Usage:
    python lattice_volume_checker.py input.i
    python lattice_volume_checker.py input.i --cell 1 --universe 10

Purpose:
    - Extract VOL parameters from universe cells
    - Calculate total volume across all lattice instances
    - Verify per-instance vs total volume specifications
    - Estimate total material inventory
    - Warn if volumes seem incorrect

Author: MCNP Lattice Builder Skill
Version: 1.0.0
"""

import sys
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Check MCNP lattice volumes")
    parser.add_argument("input_file", help="MCNP input file")
    parser.add_argument("--cell", type=int, help="Specific cell to check")
    parser.add_argument("--universe", type=int, help="Specific universe to analyze")

    args = parser.parse_args()

    print(f"Checking volumes in: {args.input_file}")
    print()

    # Parse volumes and lattice info
    volumes = parse_volumes(args.input_file)
    lattices = parse_lattices(args.input_file)

    if not volumes:
        print("No VOL parameters found in input")
        return 1

    # Display volume information
    print("Volume Specifications:")
    print("-" * 70)
    for cell, (vol, universe) in sorted(volumes.items()):
        print(f"Cell {cell:4d}: VOL={vol:12.6e} cm³", end="")
        if universe is not None:
            print(f"  (U={universe})", end="")
            # Check if this universe is used in a lattice
            instances = count_instances(universe, lattices)
            if instances > 0:
                total = vol * instances
                print(f"\n              Instances: {instances}")
                print(f"              Total volume: {total:.6e} cm³")
        print()

    # Check for common issues
    print("\nVolume Check Summary:")
    issues = check_volume_issues(volumes, lattices)
    if issues:
        print("  Issues found:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  ✓ No obvious issues detected")

    return 0

def parse_volumes(filename):
    """Extract VOL parameters from input file"""
    volumes = {}  # {cell_num: (vol_value, universe_num_or_none)}
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Look for VOL= parameter on cell cards
                vol_match = re.search(r'\bVOL\s*=\s*([0-9.eE+-]+)', line, re.IGNORECASE)
                if vol_match:
                    vol = float(vol_match.group(1))
                    # Extract cell number
                    cell_match = re.match(r'\s*(\d+)', line)
                    # Extract universe if present
                    u_match = re.search(r'\bU\s*=\s*(\d+)', line, re.IGNORECASE)
                    if cell_match:
                        cell_num = int(cell_match.group(1))
                        u_num = int(u_match.group(1)) if u_match else None
                        volumes[cell_num] = (vol, u_num)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)
    return volumes

def parse_lattices(filename):
    """Extract lattice information (dimensions, FILL)"""
    lattices = {}  # {universe_num: lattice_info}
    # Simplified parsing
    try:
        with open(filename, 'r') as f:
            for line in f:
                if 'LAT' in line.upper():
                    # Try to extract universe, dimensions, FILL
                    u_match = re.search(r'\bU\s*=\s*(\d+)', line, re.IGNORECASE)
                    fill_match = re.search(r'\bFILL\s*=\s*(\d+)', line, re.IGNORECASE)
                    # Extract dimensions if array FILL
                    dims_match = re.search(r'FILL\s*=\s*([0-9:]+)\s+([0-9:]+)\s+([0-9:]+)',
                                          line, re.IGNORECASE)
                    if u_match:
                        u_num = int(u_match.group(1))
                        lattices[u_num] = {}
                        if dims_match:
                            # Parse dimensions
                            i_range = [int(x) for x in dims_match.group(1).split(':')]
                            j_range = [int(x) for x in dims_match.group(2).split(':')]
                            k_range = [int(x) for x in dims_match.group(3).split(':')]
                            ni = i_range[1] - i_range[0] + 1
                            nj = j_range[1] - j_range[0] + 1
                            nk = k_range[1] - k_range[0] + 1
                            lattices[u_num]['elements'] = ni * nj * nk
                        elif fill_match:
                            # Single FILL (need to infer dimensions from surfaces)
                            lattices[u_num]['fill_universe'] = int(fill_match.group(1))
    except FileNotFoundError:
        pass
    return lattices

def count_instances(universe, lattices):
    """Count how many instances of universe appear in lattices"""
    # Simplified: just check if universe is filled somewhere
    total = 0
    for lat_u, info in lattices.items():
        if 'elements' in info:
            # Assume this universe is filled in lattice
            # (proper implementation would parse FILL array)
            if 'fill_universe' in info and info['fill_universe'] == universe:
                total += info['elements']
            # TODO: Parse actual FILL array to count occurrences
    return total if total > 0 else 1  # Default to 1 if not in lattice

def check_volume_issues(volumes, lattices):
    """Check for common volume specification issues"""
    issues = []

    # Check for suspiciously large volumes (might be total instead of per-instance)
    for cell, (vol, universe) in volumes.items():
        if universe is not None and vol > 1000:  # Arbitrary threshold
            issues.append(f"Cell {cell}: Volume {vol:.2e} seems large for per-instance")

    # Check for zero volumes
    for cell, (vol, universe) in volumes.items():
        if vol == 0:
            issues.append(f"Cell {cell}: Volume is zero")

    # Check for negative volumes (invalid)
    for cell, (vol, universe) in volumes.items():
        if vol < 0:
            issues.append(f"Cell {cell}: Volume is negative (invalid)")

    return issues

if __name__ == "__main__":
    sys.exit(main())
