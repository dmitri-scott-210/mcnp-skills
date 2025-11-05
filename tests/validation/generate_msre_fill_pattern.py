"""
Generate FILL array pattern for MSRE explicit lattice
Creates circular distribution of fuel channels (universe 1) vs graphite (universe 2)
"""

import math

# MSRE parameters
core_radius_cm = 70.485  # cm
pitch_cm = 3.5921  # cm
max_radius_lattice = core_radius_cm / pitch_cm  # ≈ 19.62 lattice units

# Array size: -20:20 (41x41)
array_min = -20
array_max = 20

# Generate FILL pattern
print("c FILL array for MSRE lattice (41x41, circular pattern)")
print("     FILL= -20:20 -20:20 0:0")

for j in range(array_max, array_min - 1, -1):  # j from +20 to -20 (top to bottom)
    row_str = "c Row " + str(j)
    print(row_str)
    row_data = "     "

    for i in range(array_min, array_max + 1):  # i from -20 to +20 (left to right)
        # Calculate radial distance in lattice units
        r = math.sqrt(i**2 + j**2)

        # If within core radius, use fuel channel (universe 1)
        # Otherwise use graphite only (universe 2)
        if r < max_radius_lattice:
            row_data += "1 "
        else:
            row_data += "2 "

    print(row_data.rstrip())

# Count fuel channels
fuel_count = 0
for j in range(array_min, array_max + 1):
    for i in range(array_min, array_max + 1):
        r = math.sqrt(i**2 + j**2)
        if r < max_radius_lattice:
            fuel_count += 1

print(f"\nc Total fuel channels in pattern: {fuel_count}")
print(f"c Target: 1140 channels")
print(f"c Difference: {fuel_count - 1140} ({100*(fuel_count-1140)/1140:.1f}%)")
