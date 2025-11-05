"""
Analyze MSRE lattice requirements to match design spec exactly
Target: ~1140 fuel channels with 22.5% fuel fraction
"""

import math

# Design spec parameters
core_radius_cm = 70.485  # cm
pitch_cm = 5.08  # cm
fuel_channel_radius_cm = 1.321  # cm
target_fuel_channels = 1140
target_fuel_fraction = 0.225

# Calculate core area
core_area_cm2 = math.pi * core_radius_cm**2
print(f"Core cross-sectional area: {core_area_cm2:.2f} cm²")

# Calculate unit cell area
unit_cell_area_cm2 = pitch_cm**2
print(f"Unit cell area: {unit_cell_area_cm2:.2f} cm²")

# Calculate fuel channel area
fuel_channel_area_cm2 = math.pi * fuel_channel_radius_cm**2
print(f"Fuel channel area: {fuel_channel_area_cm2:.3f} cm²")

# Calculate fuel fraction per unit cell
fuel_fraction_per_cell = fuel_channel_area_cm2 / unit_cell_area_cm2
print(f"Fuel fraction per unit cell: {fuel_fraction_per_cell:.3f} ({fuel_fraction_per_cell*100:.1f}%)")

# How many unit cells fit in the core?
max_cells_in_core = core_area_cm2 / unit_cell_area_cm2
print(f"\nMax unit cells that fit in core area: {max_cells_in_core:.1f}")

# With target fuel fraction, how many should have fuel?
cells_with_fuel_for_target_fraction = (target_fuel_fraction * core_area_cm2) / fuel_channel_area_cm2
print(f"Cells with fuel for {target_fuel_fraction*100}% fraction: {cells_with_fuel_for_target_fraction:.0f}")

# Current model analysis
current_fuel_cells = 593
current_total_fuel_area = current_fuel_cells * fuel_channel_area_cm2
current_fuel_fraction = current_total_fuel_area / core_area_cm2
print(f"\nCurrent model:")
print(f"  Fuel channels: {current_fuel_cells}")
print(f"  Total fuel area: {current_total_fuel_area:.2f} cm²")
print(f"  Fuel fraction: {current_fuel_fraction:.3f} ({current_fuel_fraction*100:.1f}%)")

# What if we use target 1140 channels?
target_total_fuel_area = target_fuel_channels * fuel_channel_area_cm2
target_actual_fuel_fraction = target_total_fuel_area / core_area_cm2
print(f"\nWith {target_fuel_channels} channels:")
print(f"  Total fuel area: {target_total_fuel_area:.2f} cm²")
print(f"  Fuel fraction: {target_actual_fuel_fraction:.3f} ({target_actual_fuel_fraction*100:.1f}%)")

# Array size calculation
max_radius_lattice_units = core_radius_cm / pitch_cm
print(f"\nCore radius in lattice units: {max_radius_lattice_units:.2f}")

# For different array sizes, count how many positions fall within core
for array_half_size in range(14, 22):
    count = 0
    array_min = -array_half_size
    array_max = array_half_size

    for j in range(array_min, array_max + 1):
        for i in range(array_min, array_max + 1):
            # Position of this lattice element center in cm
            x_cm = i * pitch_cm
            y_cm = j * pitch_cm
            r_cm = math.sqrt(x_cm**2 + y_cm**2)

            # Check if center is within core radius
            if r_cm <= core_radius_cm:
                count += 1

    fuel_frac = (count * fuel_channel_area_cm2) / core_area_cm2
    print(f"Array -{array_half_size}:{array_half_size} ({(2*array_half_size+1)}×{(2*array_half_size+1)}): {count} fuel channels, {fuel_frac:.1%} fuel fraction")
