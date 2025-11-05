"""
Generate FILL array for MSRE benchmark lattice - CORRECT Fortran order
Benchmark geometry: 0.961 cm radius, 3.5921 cm pitch
Array: 41x41 (-20:20)
"""
import math

# MSRE benchmark parameters
core_radius_cm = 70.485
pitch_cm = 3.5921  # BENCHMARK pitch
max_radius_lattice = core_radius_cm / pitch_cm  # ~19.62

# Array size for benchmark: -20:20 (41x41)
array_min = -20
array_max = 20

print("c FILL array for MSRE benchmark lattice (41x41)")
print("c CORRECT FORTRAN ORDER: j from -20 to +20")
print("     FILL= -20:20 -20:20 0:0")

# CORRECT order: j from -20 to +20 (Fortran array order!)
for j in range(array_min, array_max + 1):
    row_str = f"c Row {j:3d}"
    print(row_str)
    row_data = "     "
    
    for i in range(array_min, array_max + 1):
        r = math.sqrt(i**2 + j**2)
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

print(f"\nc Total fuel channels: {fuel_count}")
print(f"c Expected for benchmark: ~1201")
