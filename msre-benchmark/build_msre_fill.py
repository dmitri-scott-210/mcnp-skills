#!/usr/bin/env python3
"""
Build MSRE lattice FILL array with control rods and sample basket
"""

import numpy as np

core_radius = 70.285  # cm
lattice_pitch = 5.084  # cm
imin, imax = -13, 14
jmin, jmax = -13, 14

# Build fill array
fill_array = []
for j in range(jmin, jmax + 1):
    row = []
    for i in range(imin, imax + 1):
        x = i * lattice_pitch
        y = j * lattice_pitch
        r = np.sqrt(x**2 + y**2)

        # Special positions: 3 control rods + 1 sample basket
        # Equidistant at ~5 cm radius from center
        if (i, j) in [(-1, 0), (1, 0), (0, -1)]:
            # Control rods (Universe 2)
            universe = 2
        elif (i, j) == (0, 1):
            # Sample basket (Universe 3)
            universe = 3
        elif r <= core_radius:
            # Fuel stringer (Universe 1)
            universe = 1
        else:
            # Outside core - void
            universe = 0

        row.append(universe)

    fill_array.append(row)

# Print in MCNP6 format (no & continuation, just 5+ spaces)
print("100  0  -500 501 -502 503 -504 505  U=10  LAT=1  IMP:N=1")
print(f"     FILL={imin}:{imax} {jmin}:{jmax} 0:0")

for row in fill_array:
    # Format row as space-separated integers
    row_str = ' '.join(str(u) for u in row)
    print(f"          {row_str}")

print()
count_fuel = sum(sum(1 for u in row if u == 1) for row in fill_array)
count_cr = sum(sum(1 for u in row if u == 2) for row in fill_array)
count_sb = sum(sum(1 for u in row if u == 3) for row in fill_array)
print(f"Fuel stringers (U=1): {count_fuel}")
print(f"Control rods (U=2): {count_cr}")
print(f"Sample baskets (U=3): {count_sb}")
print(f"Total active: {count_fuel + count_cr + count_sb}")
