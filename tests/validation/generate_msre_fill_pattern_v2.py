"""
Generate FILL array pattern for MSRE explicit lattice - CORRECTED VERSION
Uses proper dimensions from msre_design_spec.md:
- Fuel channel radius: 1.321 cm (diameter 2.642 cm)
- Graphite stringer pitch: 5.08 cm
- Square lattice with circular core boundary
"""

import math

# MSRE parameters - CORRECT VALUES
core_radius_cm = 70.485  # cm (core cylinder radius)
pitch_cm = 5.08  # cm (graphite stringer pitch) - CORRECT!
max_radius_lattice = core_radius_cm / pitch_cm  # ≈ 13.87 lattice units

# Array size: -14:14 (29x29 = 841 positions)
array_min = -14
array_max = 14

# Generate FILL pattern
print("c FILL array for MSRE lattice (29x29, square lattice with circular trim)")
print("c Fuel channel radius: 1.321 cm, Stringer pitch: 5.08 cm")
print("     FILL= -14:14 -14:14 0:0")

for j in range(array_min, array_max + 1):  # j from -14 to +14 (FORTRAN ORDER!)
    row_str = f"c Row {j:3d}"
    print(row_str)
    row_data = "     "

    for i in range(array_min, array_max + 1):  # i from -14 to +14 (left to right)
        # Calculate radial distance in lattice units
        r = math.sqrt(i**2 + j**2)

        # If within core radius, use fuel channel universe (universe 1)
        # Otherwise use graphite only universe (universe 2)
        if r <= max_radius_lattice:
            row_data += "1 "
        else:
            row_data += "2 "

    print(row_data.rstrip())

# Count fuel channels
fuel_count = 0
for j in range(array_min, array_max + 1):
    for i in range(array_min, array_max + 1):
        r = math.sqrt(i**2 + j**2)
        if r <= max_radius_lattice:
            fuel_count += 1

print(f"\nc Total fuel channels in pattern: {fuel_count}")
print(f"c Target: 1140 channels (from benchmark)")
print(f"c Difference: {fuel_count - 1140} ({100*(fuel_count-1140)/1140:.1f}%)")
print(f"c Core radius in lattice units: {max_radius_lattice:.2f}")
