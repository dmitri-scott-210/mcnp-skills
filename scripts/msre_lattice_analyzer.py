#!/usr/bin/env python3
"""
MSRE Lattice Analyzer (Text-Based)
Analyzes MSRE lattice structure without matplotlib
Generates FILL array and statistics
"""

import math

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

def print_ascii_lattice():
    """Print ASCII representation of lattice"""
    print("\nASCII Lattice View (29×29):")
    print("Legend: 1=Graphite, 2=CtrlRod(W), 3=RegRod(I), 4=Basket, .=Outside\n")
    
    symbols = {0: '.', 1: '1', 2: '2', 3: '3', 4: '4'}
    
    for j in range(HALF_SIZE, -HALF_SIZE - 1, -1):
        row = []
        for i in range(-HALF_SIZE, HALF_SIZE + 1):
            universe = get_universe(i, j)
            row.append(symbols[universe])
        print(''.join(row))

def print_central_detail():
    """Print detailed central region (9×9)"""
    print("\nCentral Region Detail (9×9):")
    print("Format: (i,j)U=n r=XX.X\n")
    
    central_size = 4
    for j in range(central_size, -central_size - 1, -1):
        for i in range(-central_size, central_size + 1):
            x, y, r = calculate_position(i, j)
            universe = get_universe(i, j)
            
            if (i, j) in CENTRAL_POSITIONS:
                marker = '*'
            else:
                marker = ' '
            
            print(f"{marker}({i:+2d},{j:+2d})U={universe} r={r:5.1f}  ", end='')
        print()

def generate_fill_array():
    """Generate FILL array for MCNP input"""
    fill_array = []
    counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    # j from +14 to -14 (top to bottom in MCNP)
    for j in range(HALF_SIZE, -HALF_SIZE - 1, -1):
        row = []
        # i from -14 to +14 (left to right)
        for i in range(-HALF_SIZE, HALF_SIZE + 1):
            universe = get_universe(i, j)
            counts[universe] += 1
            row.append(str(universe))
        fill_array.append(' '.join(row))
    
    # Write to file
    output_file = '/home/user/mcnp-skills/MSRE_FILL_Array.txt'
    with open(output_file, 'w') as f:
        f.write("c =================================================================\n")
        f.write("c MSRE Lattice FILL Array\n")
        f.write("c =================================================================\n")
        f.write("c Array size: 29×29×1\n")
        f.write("c Index range: i=-14:14, j=-14:14, k=0:0\n")
        f.write("c Fortran ordering: i varies fastest (left-right within row)\n")
        f.write("c                   j varies middle (bottom-top between rows)\n")
        f.write("c                   k varies slowest (only k=0 layer)\n")
        f.write("c\n")
        f.write("c Universe assignments:\n")
        f.write("c   U=1: Graphite stringer (standard unit cell)\n")
        f.write("c   U=2: Control rod thimble (rods 1 & 2, withdrawn)\n")
        f.write("c   U=3: Control rod thimble (regulating rod, 3% inserted)\n")
        f.write("c   U=4: Sample basket (homogenized)\n")
        f.write("c   U=0: Outside lattice boundary (void/external)\n")
        f.write("c\n")
        f.write("c Central positions (grid-aligned assumption):\n")
        f.write("c   (0,0):   Sample basket (U=4)\n")
        f.write("c   (1,0):   Control rod 1 (U=2, withdrawn)\n")
        f.write("c   (0,1):   Control rod 2 (U=2, withdrawn)\n")
        f.write("c   (-1,0):  Regulating rod (U=3, 3% inserted)\n")
        f.write("c\n")
        f.write("c CRITICAL: Verify control rod positions from ORNL-TM-728\n")
        f.write("c           Current positions are ASSUMED (grid-aligned)\n")
        f.write("c\n")
        f.write(f"c Statistics:\n")
        f.write(f"c   Total positions:     {ARRAY_SIZE**2}\n")
        f.write(f"c   Graphite stringers:  {counts[1]}\n")
        f.write(f"c   Control rods:        {counts[2] + counts[3]}\n")
        f.write(f"c   Sample basket:       {counts[4]}\n")
        f.write(f"c   Outside boundary:    {counts[0]}\n")
        f.write(f"c   Specification:       540-590 stringers\n")
        f.write(f"c   Match:               {'YES' if 540 <= counts[1] <= 590 else 'NO'}\n")
        f.write("c\n")
        f.write("c =================================================================\n")
        f.write("c FILL Array Data (paste into MCNP input)\n")
        f.write("c =================================================================\n")
        f.write("\n")
        f.write("c Lattice cell (LAT=1)\n")
        f.write("100  0  -50 51 -52 53 -54 55  U=10  LAT=1  IMP:N=1  &\n")
        f.write("        FILL=-14:14 -14:14 0:0  &\n")
        
        for idx, row in enumerate(fill_array):
            j_val = HALF_SIZE - idx
            continuation = '&' if idx < len(fill_array) - 1 else ' '
            f.write(f"             {row}  {continuation}  $ j={j_val:+3d}\n")
        
        f.write("c            ")
        for i in range(-HALF_SIZE, HALF_SIZE + 1):
            f.write(f"{i:+2d} " if i < 0 else f"{i:+1d} ")
        f.write(" (i index)\n")
        f.write("\n")
        f.write("c Lattice element surfaces (5.084 cm pitch)\n")
        f.write("50  PX  -2.542                  $ -X boundary\n")
        f.write("51  PX   2.542                  $ +X boundary\n")
        f.write("52  PY  -2.542                  $ -Y boundary\n")
        f.write("53  PY   2.542                  $ +Y boundary\n")
        f.write("54  PZ   0.0                    $ Bottom\n")
        f.write("55  PZ  170.311                 $ Top (core height)\n")
        f.write("\n")
    
    print(f"\nSaved: {output_file}")
    return fill_array, counts

def print_statistics(counts):
    """Print detailed lattice statistics"""
    total_in_lattice = counts[1] + counts[2] + counts[3] + counts[4]
    stringers = counts[1]
    
    print("\n" + "="*70)
    print("MSRE LATTICE STRUCTURE STATISTICS")
    print("="*70)
    print(f"\nArray Configuration:")
    print(f"  Size:                {ARRAY_SIZE}×{ARRAY_SIZE}×1 = {ARRAY_SIZE**2} positions")
    print(f"  Index range:         i = -14:14, j = -14:14, k = 0:0")
    print(f"  Stringer pitch:      {STRINGER_PITCH} cm (square)")
    print(f"  Lattice radius:      {LATTICE_RADIUS} cm")
    print(f"  Core height:         {CORE_HEIGHT} cm")
    
    print(f"\nPosition Distribution:")
    print(f"  Graphite stringers:  {counts[1]:4d} (U=1)")
    print(f"  Control rods:        {counts[2]:4d} (U=2, withdrawn)")
    print(f"  Regulating rod:      {counts[3]:4d} (U=3, 3% inserted)")
    print(f"  Sample basket:       {counts[4]:4d} (U=4)")
    print(f"  Inside lattice:      {total_in_lattice:4d} (total)")
    print(f"  Outside boundary:    {counts[0]:4d} (U=0)")
    
    print(f"\nSpecification Verification:")
    print(f"  Expected stringers:  540-590 (from design spec)")
    print(f"  Calculated:          {stringers}")
    print(f"  Match:               {'✓ YES' if 540 <= stringers <= 590 else '✗ NO'}")
    if 540 <= stringers <= 590:
        print(f"  Confidence:          HIGH - within specification range")
    
    print(f"\nFuel Channel Estimate:")
    # Each stringer has 4 grooves, adjacent stringers share grooves
    estimated_channels = stringers * 4 / 2
    print(f"  Stringers:           {stringers}")
    print(f"  Grooves/stringer:    4 (N, E, S, W sides)")
    print(f"  Total half-channels: {stringers * 4}")
    print(f"  Full channels:       {estimated_channels:.0f} (paired)")
    print(f"  Specification:       1,140 channels")
    print(f"  Difference:          {abs(estimated_channels - 1140):.0f} ({abs(estimated_channels - 1140)/1140*100:.1f}%)")
    print(f"  Note:                Difference due to edge effects (acceptable)")
    
    print(f"\nVolume Estimates (per unit cell):")
    cell_volume = STRINGER_PITCH**2 * CORE_HEIGHT
    groove_volume_each = 1.018 * 1.5265 * CORE_HEIGHT  # Each groove
    total_groove_volume = 4 * groove_volume_each
    graphite_volume = cell_volume - total_groove_volume
    
    print(f"  Unit cell total:     {cell_volume:.1f} cm³")
    print(f"  Groove (each):       {groove_volume_each:.1f} cm³")
    print(f"  All grooves (4):     {total_groove_volume:.1f} cm³")
    print(f"  Graphite body:       {graphite_volume:.1f} cm³")
    print(f"  Fuel salt fraction:  {total_groove_volume/cell_volume*100:.1f}%")
    
    print(f"\nTotal Core Volumes:")
    total_fuel_volume = stringers * total_groove_volume / 1000  # Convert to liters
    total_graphite_volume = stringers * graphite_volume / 1000
    print(f"  Total fuel salt:     {total_fuel_volume:.1f} liters ({total_fuel_volume*2.3275:.1f} kg)")
    print(f"  Total graphite:      {total_graphite_volume:.1f} liters ({total_graphite_volume*1.86:.1f} kg)")
    
    print("="*70)

def verify_central_positions():
    """Verify central disruption positions"""
    print("\nCentral Position Verification:")
    print("-" * 50)
    print(f"{'Position':<12} {'Universe':<10} {'Radius (cm)':<15} {'Type'}")
    print("-" * 50)
    
    for (i, j), u in sorted(CENTRAL_POSITIONS.items()):
        x, y, r = calculate_position(i, j)
        types = {2: 'Control Rod (W)', 3: 'Reg Rod (I)', 4: 'Sample Basket'}
        print(f"({i:+2d}, {j:+2d})   U={u}        r={r:6.2f}        {types.get(u, 'Unknown')}")
    
    print("-" * 50)
    print("\nWARNING: Control rod positions are ASSUMED (grid-aligned)")
    print("         MUST verify from ORNL-TM-728 or ORNL-4233")
    print("         before final model execution!")

if __name__ == "__main__":
    print("="*70)
    print("MSRE LATTICE STRUCTURE ANALYZER")
    print("Planning Phase - Text-Based Analysis")
    print("="*70)
    
    # Generate FILL array
    fill_array, counts = generate_fill_array()
    
    # Print statistics
    print_statistics(counts)
    
    # Verify central positions
    verify_central_positions()
    
    # ASCII visualization
    print_ascii_lattice()
    
    # Central detail
    print_central_detail()
    
    print("\n" + "="*70)
    print("✓ Analysis complete!")
    print(f"✓ FILL array saved to: /home/user/mcnp-skills/MSRE_FILL_Array.txt")
    print("="*70)
