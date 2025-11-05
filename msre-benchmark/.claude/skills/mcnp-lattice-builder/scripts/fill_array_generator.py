#!/usr/bin/env python3
"""
FILL Array Generator - Generate properly formatted FILL arrays

Usage:
    python fill_array_generator.py --dims "0:2 0:2 0:0" --pattern "1 1 2 1 2 1 1 1 1"
    python fill_array_generator.py --dims "0:4 0:4 0:0" --file pattern.txt

Purpose:
    - Generate MCNP FILL array with correct Fortran ordering
    - Validate dimensions match value count
    - Format with proper continuation and comments
    - Help prevent common indexing errors

Author: MCNP Lattice Builder Skill
Version: 1.0.0
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate MCNP FILL arrays")
    parser.add_argument("--dims", required=True, help="Dimensions: 'imin:imax jmin:jmax kmin:kmax'")
    parser.add_argument("--pattern", help="Universe pattern (space-separated)")
    parser.add_argument("--file", help="Read pattern from file")

    args = parser.parse_args()

    # Parse dimensions
    dims_parts = args.dims.split()
    if len(dims_parts) != 3:
        print("ERROR: Dimensions must be 'imin:imax jmin:jmax kmin:kmax'")
        return 1

    # Extract ranges
    i_range = [int(x) for x in dims_parts[0].split(':')]
    j_range = [int(x) for x in dims_parts[1].split(':')]
    k_range = [int(x) for x in dims_parts[2].split(':')]

    ni = i_range[1] - i_range[0] + 1
    nj = j_range[1] - j_range[0] + 1
    nk = k_range[1] - k_range[0] + 1
    total = ni * nj * nk

    # Get pattern
    if args.pattern:
        pattern = [int(x) for x in args.pattern.split()]
    elif args.file:
        with open(args.file, 'r') as f:
            pattern = [int(x) for line in f for x in line.split() if x.isdigit()]
    else:
        print("ERROR: Must specify --pattern or --file")
        return 1

    # Validate count
    if len(pattern) != total:
        print(f"ERROR: Dimension mismatch")
        print(f"  Expected: {ni}×{nj}×{nk} = {total} values")
        print(f"  Got: {len(pattern)} values")
        return 1

    # Generate FILL array
    generate_fill_array(i_range, j_range, k_range, pattern)

    return 0

def generate_fill_array(i_range, j_range, k_range, pattern):
    """Generate formatted FILL array with comments"""
    ni = i_range[1] - i_range[0] + 1
    nj = j_range[1] - j_range[0] + 1
    nk = k_range[1] - k_range[0] + 1

    print(f"FILL={i_range[0]}:{i_range[1]} {j_range[0]}:{j_range[1]} {k_range[0]}:{k_range[1]}")

    idx = 0
    for k in range(k_range[0], k_range[1] + 1):
        if nk > 1:
            print(f"c --- k={k} plane ---")
        for j in range(j_range[0], j_range[1] + 1):
            line_values = []
            for i in range(i_range[0], i_range[1] + 1):
                line_values.append(str(pattern[idx]))
                idx += 1
            # Format line with comment
            values_str = ' '.join(line_values)
            if nk == 1:
                print(f"     {values_str}    $ j={j}: i={i_range[0]}:{i_range[1]}")
            else:
                print(f"     {values_str}    $ k={k}, j={j}")

    print("\nc Pattern summary:")
    print(f"c   Total elements: {ni}×{nj}×{nk} = {len(pattern)}")
    print(f"c   Fortran ordering: i varies fastest, j middle, k slowest")
    unique = set(pattern)
    for u in sorted(unique):
        count = pattern.count(u)
        print(f"c   Universe {u}: {count} occurrences")

if __name__ == "__main__":
    sys.exit(main())
