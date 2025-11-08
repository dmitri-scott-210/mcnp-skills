#!/usr/bin/env python3
"""
Calculate MSRE lattice FILL array
Determines which 28x28 lattice positions are inside 70.285 cm radius core
"""

import numpy as np

# MSRE parameters
core_radius = 70.285  # cm (hot dimensions at 911 K)
lattice_pitch = 5.084  # cm (stringer width, hot)

# Lattice array dimensions
imin, imax = -13, 14  # 28 elements in i direction
jmin, jmax = -13, 14  # 28 elements in j direction
k = 0  # Single layer

# Calculate which positions are inside core
fill_array = []
for j in range(jmin, jmax + 1):
    row = []
    for i in range(imin, imax + 1):
        # Center position of this lattice element
        x = i * lattice_pitch
        y = j * lattice_pitch
        r = np.sqrt(x**2 + y**2)

        # Determine universe
        if r <= core_radius:
            # Inside core - use fuel stringer (U=1)
            # TODO: Place control rods (U=2) and sample basket (U=3) near center
            # For now, all fuel stringers
            row.append(1)
        else:
            # Outside core radius - void (U=0)
            row.append(0)

    fill_array.append(row)

# Print FILL array in MCNP format
print("FILL array for MSRE lattice (28x28):")
print(f"FILL={imin}:{imax} {jmin}:{jmax} {k}:{k}")

# Print in groups of 28 (one row per line)
for j_idx, row in enumerate(fill_array):
    j_val = jmin + j_idx
    # Format as space-separated integers
    row_str = ' '.join(str(u) for u in row)
    print(f"     {row_str}")

print()
print(f"Total elements inside core: {sum(sum(1 for u in row if u != 0) for row in fill_array)}")
print(f"Core radius: {core_radius} cm")
print(f"Lattice pitch: {lattice_pitch} cm")
print()

# Show which positions for control rods (near center, ~4 positions)
print("Center region analysis (for control rod placement):")
for j in range(-2, 3):
    for i in range(-2, 3):
        x = i * lattice_pitch
        y = j * lattice_pitch
        r = np.sqrt(x**2 + y**2)
        print(f"  i={i:2d}, j={j:2d}: x={x:6.2f}, y={y:6.2f}, r={r:6.2f} cm")
