#!/usr/bin/env python3
"""
MSRE Lattice Visualizer
Generates visual representation of MSRE lattice structure
Shows stringer positions, control rods, sample basket, and boundary
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# MSRE Parameters (hot, 911 K)
LATTICE_RADIUS = 70.285  # cm
STRINGER_PITCH = 5.084   # cm
CORE_HEIGHT = 170.311    # cm
ARRAY_SIZE = 29
HALF_SIZE = ARRAY_SIZE // 2

# Universe assignments (assumed - verify from literature)
CENTRAL_POSITIONS = {
    (0, 0): 4,   # Sample basket
    (1, 0): 2,   # Control rod 1 (withdrawn)
    (0, 1): 2,   # Control rod 2 (withdrawn)
    (-1, 0): 3,  # Regulating rod (3% inserted)
}

def calculate_position(i, j):
    """Convert lattice indices to (x, y, r) position"""
    x = i * STRINGER_PITCH
    y = j * STRINGER_PITCH
    r = math.sqrt(x**2 + y**2)
    return x, y, r

def get_universe(i, j):
    """Determine universe number for position (i, j)"""
    if (i, j) in CENTRAL_POSITIONS:
        return CENTRAL_POSITIONS[(i, j)]
    
    x, y, r = calculate_position(i, j)
    if r <= LATTICE_RADIUS:
        return 1  # Graphite stringer
    else:
        return 0  # Outside lattice (void or external)

def plot_lattice_xy():
    """Plot XY view of lattice at mid-height"""
    fig, ax = plt.subplots(figsize=(14, 14))
    
    # Count positions by type
    counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    # Plot each position
    for i in range(-HALF_SIZE, HALF_SIZE + 1):
        for j in range(-HALF_SIZE, HALF_SIZE + 1):
            x, y, r = calculate_position(i, j)
            universe = get_universe(i, j)
            counts[universe] += 1
            
            # Color by universe type
            if universe == 0:  # Outside
                color = 'white'
                edgecolor = 'lightgray'
                alpha = 0.3
            elif universe == 1:  # Graphite stringer
                color = 'gray'
                edgecolor = 'black'
                alpha = 0.7
            elif universe == 2:  # Control rod (withdrawn)
                color = 'blue'
                edgecolor = 'darkblue'
                alpha = 1.0
            elif universe == 3:  # Regulating rod (inserted)
                color = 'red'
                edgecolor = 'darkred'
                alpha = 1.0
            elif universe == 4:  # Sample basket
                color = 'green'
                edgecolor = 'darkgreen'
                alpha = 1.0
            else:
                color = 'yellow'
                edgecolor = 'black'
                alpha = 1.0
            
            # Draw square stringer position
            rect = patches.Rectangle(
                (x - STRINGER_PITCH/2, y - STRINGER_PITCH/2),
                STRINGER_PITCH, STRINGER_PITCH,
                linewidth=0.5, edgecolor=edgecolor,
                facecolor=color, alpha=alpha
            )
            ax.add_patch(rect)
            
            # Label central positions
            if (i, j) in CENTRAL_POSITIONS:
                ax.text(x, y, f'({i},{j})\nU={universe}', 
                       ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Draw circular boundary
    boundary = plt.Circle((0, 0), LATTICE_RADIUS, 
                          color='red', fill=False, linewidth=3, 
                          label=f'Lattice Radius: {LATTICE_RADIUS} cm')
    ax.add_patch(boundary)
    
    # Draw core can (inner)
    core_can_inner = plt.Circle((0, 0), 71.097, 
                                color='orange', fill=False, linewidth=2, 
                                linestyle='--', label='Core Can Inner: 71.097 cm')
    ax.add_patch(core_can_inner)
    
    # Axes and labels
    ax.set_xlim(-80, 80)
    ax.set_ylim(-80, 80)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    ax.set_xlabel('X (cm)', fontsize=12)
    ax.set_ylabel('Y (cm)', fontsize=12)
    ax.set_title('MSRE Lattice Structure - XY View at Mid-Height\n' + 
                 f'29×29 Array, {STRINGER_PITCH:.3f} cm Pitch',
                 fontsize=14, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(facecolor='gray', edgecolor='black', label=f'Graphite Stringer (U=1): {counts[1]}'),
        patches.Patch(facecolor='blue', edgecolor='darkblue', label=f'Control Rod Withdrawn (U=2): {counts[2]}'),
        patches.Patch(facecolor='red', edgecolor='darkred', label=f'Regulating Rod Inserted (U=3): {counts[3]}'),
        patches.Patch(facecolor='green', edgecolor='darkgreen', label=f'Sample Basket (U=4): {counts[4]}'),
        patches.Patch(facecolor='white', edgecolor='lightgray', label=f'Outside Lattice: {counts[0]}'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Statistics
    total_in_lattice = counts[1] + counts[2] + counts[3] + counts[4]
    stringers = counts[1]
    
    stats_text = f"""
    Total Positions: {ARRAY_SIZE}×{ARRAY_SIZE} = {ARRAY_SIZE**2}
    Within Lattice: {total_in_lattice}
    Graphite Stringers: {stringers}
    Specification: 540-590
    Match: {'YES' if 540 <= stringers <= 590 else 'NO'}
    """
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('/home/user/mcnp-skills/MSRE_Lattice_XY_View.png', dpi=300)
    print(f"Saved: /home/user/mcnp-skills/MSRE_Lattice_XY_View.png")
    
    return counts, total_in_lattice, stringers

def plot_central_region():
    """Plot detailed view of central 9×9 region"""
    fig, ax = plt.subplots(figsize=(12, 12))
    
    central_size = 4  # ±4 positions
    
    for i in range(-central_size, central_size + 1):
        for j in range(-central_size, central_size + 1):
            x, y, r = calculate_position(i, j)
            universe = get_universe(i, j)
            
            # Color by universe type
            if universe == 1:
                color = 'gray'
                edgecolor = 'black'
            elif universe == 2:
                color = 'blue'
                edgecolor = 'darkblue'
            elif universe == 3:
                color = 'red'
                edgecolor = 'darkred'
            elif universe == 4:
                color = 'green'
                edgecolor = 'darkgreen'
            else:
                color = 'white'
                edgecolor = 'lightgray'
            
            # Draw square stringer position
            rect = patches.Rectangle(
                (x - STRINGER_PITCH/2, y - STRINGER_PITCH/2),
                STRINGER_PITCH, STRINGER_PITCH,
                linewidth=1.5, edgecolor=edgecolor,
                facecolor=color, alpha=0.8
            )
            ax.add_patch(rect)
            
            # Label all positions in central region
            label = f'({i},{j})\nU={universe}\nr={r:.1f}'
            ax.text(x, y, label, ha='center', va='center', 
                   fontsize=9, fontweight='bold' if (i,j) in CENTRAL_POSITIONS else 'normal')
    
    # Draw circular boundary
    boundary = plt.Circle((0, 0), LATTICE_RADIUS, 
                          color='red', fill=False, linewidth=2, 
                          linestyle='--', alpha=0.5)
    ax.add_patch(boundary)
    
    # Axes and labels
    limit = (central_size + 0.5) * STRINGER_PITCH
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=1)
    ax.axvline(x=0, color='k', linewidth=1)
    
    ax.set_xlabel('X (cm)', fontsize=12)
    ax.set_ylabel('Y (cm)', fontsize=12)
    ax.set_title('MSRE Lattice - Central Region Detail (9×9)\n' + 
                 'Control Rods and Sample Basket',
                 fontsize=14, fontweight='bold')
    
    # Legend
    legend_elements = [
        patches.Patch(facecolor='gray', edgecolor='black', label='Graphite Stringer (U=1)'),
        patches.Patch(facecolor='blue', edgecolor='darkblue', label='Control Rod Withdrawn (U=2)'),
        patches.Patch(facecolor='red', edgecolor='darkred', label='Regulating Rod 3% Inserted (U=3)'),
        patches.Patch(facecolor='green', edgecolor='darkgreen', label='Sample Basket (U=4)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/home/user/mcnp-skills/MSRE_Lattice_Central_Detail.png', dpi=300)
    print(f"Saved: /home/user/mcnp-skills/MSRE_Lattice_Central_Detail.png")

def generate_fill_array():
    """Generate FILL array for MCNP input"""
    fill_array = []
    
    # j from +14 to -14 (top to bottom in MCNP)
    for j in range(HALF_SIZE, -HALF_SIZE - 1, -1):
        row = []
        # i from -14 to +14 (left to right)
        for i in range(-HALF_SIZE, HALF_SIZE + 1):
            universe = get_universe(i, j)
            row.append(str(universe))
        fill_array.append(' '.join(row))
    
    # Write to file
    output_file = '/home/user/mcnp-skills/MSRE_FILL_Array.txt'
    with open(output_file, 'w') as f:
        f.write("c MSRE Lattice FILL Array\n")
        f.write("c 29×29×1 array, centered indexing (i,j = -14:14, k=0)\n")
        f.write("c Fortran ordering: i varies fastest (left-right)\n")
        f.write("c                   j varies middle (top-bottom)\n")
        f.write("c                   k varies slowest (only k=0)\n")
        f.write("c\n")
        f.write("FILL=-14:14 -14:14 0:0\n")
        for idx, row in enumerate(fill_array):
            j_val = HALF_SIZE - idx
            f.write(f"     {row}    $ j={j_val:+3d}\n")
        f.write("c    ")
        for i in range(-HALF_SIZE, HALF_SIZE + 1):
            f.write(f"{i:+2d} ")
        f.write(" (i index)\n")
    
    print(f"Saved: {output_file}")
    return fill_array

def print_statistics(counts, total, stringers):
    """Print lattice statistics"""
    print("\n" + "="*60)
    print("MSRE LATTICE STATISTICS")
    print("="*60)
    print(f"Array Size:          {ARRAY_SIZE}×{ARRAY_SIZE} = {ARRAY_SIZE**2} positions")
    print(f"Stringer Pitch:      {STRINGER_PITCH} cm")
    print(f"Lattice Radius:      {LATTICE_RADIUS} cm")
    print(f"Core Height:         {CORE_HEIGHT} cm")
    print(f"\nPositions Summary:")
    print(f"  Total in lattice:  {total}")
    print(f"  Graphite stringers: {stringers}")
    print(f"  Control rods:      {counts[2] + counts[3]}")
    print(f"  Sample basket:     {counts[4]}")
    print(f"  Outside boundary:  {counts[0]}")
    print(f"\nSpecification Check:")
    print(f"  Expected stringers: 540-590")
    print(f"  Calculated:         {stringers}")
    print(f"  Match:              {'✓ YES' if 540 <= stringers <= 590 else '✗ NO'}")
    print(f"\nFuel Channel Estimate:")
    estimated_channels = stringers * 4 / 2  # 4 grooves per stringer, paired
    print(f"  Estimated channels: {estimated_channels:.0f}")
    print(f"  Specification:      1,140")
    print(f"  Difference:         {abs(estimated_channels - 1140):.0f} ({abs(estimated_channels - 1140)/1140*100:.1f}%)")
    print("="*60)

if __name__ == "__main__":
    print("MSRE Lattice Visualizer")
    print("Generating lattice structure plots...")
    
    # Generate plots
    counts, total, stringers = plot_lattice_xy()
    plot_central_region()
    
    # Generate FILL array
    fill_array = generate_fill_array()
    
    # Print statistics
    print_statistics(counts, total, stringers)
    
    print("\n✓ All visualizations complete!")
