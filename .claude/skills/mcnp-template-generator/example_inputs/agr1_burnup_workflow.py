"""
AGR-1 Multi-Cycle Burnup Workflow Example
Demonstrates template-based generation of 13 cycle-specific MCNP inputs

Based on ATR AGR-1 HTGR fuel irradiation experiment
- 13 reactor operating cycles
- 616 timesteps with varying power and control positions
- Time-weighted averaging to collapse history into static configurations
"""

import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
import sys

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from time_averaging import time_weighted_average


# Configuration
CYCLES = [
    '138B', '139A', '139B', '140A', '140B', '141A',
    '142A', '142B', '143A', '143B', '144A', '144B', '145A'
]

PREDEFINED_ANGLES = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]


def find_closest_value(options, target):
    """Find closest discrete value."""
    differences = np.abs(np.array(options) - target)
    return options[np.argmin(differences)]


def load_and_process_data():
    """Load CSV files and process by cycle."""
    
    print("Loading CSV data...")
    
    # NOTE: This is a simplified example
    # Real AGR-1 workflow would load actual CSV files:
    # power_df = pd.read_csv('data/power.csv', index_col="Cumulative Timestep")
    # oscc_df = pd.read_csv('data/oscc.csv', index_col="Cumulative Timestep")
    # neck_df = pd.read_csv('data/neck_shim.csv', index_col="Cumulative Timestep")
    
    # For demonstration, create synthetic data
    data_by_cycle = {}
    
    for cycle in CYCLES:
        # Synthetic data (replace with real CSV processing)
        data_by_cycle[cycle] = {
            'power': 23.5 + np.random.rand() * 1.0,  # ~23.5-24.5 MW
            'ne_angle': np.random.choice([75, 80, 85]),
            'se_angle': np.random.choice([80, 85]),
            'ne_shims': {f'NE {i}': np.random.choice([0, 1]) for i in range(1, 7)},
            'se_shims': {f'SE {i}': np.random.choice([0, 1]) for i in range(1, 7)},
            'duration_days': 45.0 + np.random.rand() * 10.0
        }
    
    return data_by_cycle


def generate_oscc_surfaces(ne_angle, se_angle):
    """Generate control drum surface definitions."""
    
    # Simplified version - real implementation would have full geometry database
    return f"""c Control drum surfaces at NE={ne_angle}°, SE={se_angle}°
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT {ne_angle} DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT {ne_angle} DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT {se_angle} DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT {se_angle} DEGREES
"""


def generate_neck_shim_cells(shims, quadrant):
    """Generate neck shim cell definitions."""
    
    cell_start = 702 if quadrant == 'NE' else 792
    
    cells = f"c {quadrant} Neck Shim Cells\n"
    for i, (rod_name, state) in enumerate(shims.items(), start=1):
        mat = 71 if state == 1 else 10  # 71=Hf, 10=water
        density = 4.55926e-02 if state == 1 else 1.00276e-01
        state_str = "inserted" if state == 1 else "withdrawn"
        
        cells += f"  {cell_start + (i-1)*5}   {mat} {density:.5e}    -100  $ {rod_name} - {state_str}\n"
    
    cells += "c\n"
    return cells


def generate_inputs():
    """Main workflow: generate all 13 cycle inputs."""
    
    print("=" * 70)
    print("AGR-1 Multi-Cycle Input Generation Example")
    print("=" * 70)
    
    # Load and process data
    cycle_data = load_and_process_data()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'generated_agr1')
    os.makedirs(output_dir, exist_ok=True)
    
    # Note: In real workflow, would load template from file
    # For this example, create minimal template
    template_content = """c AGR-1 MCNP Input - Cycle {{cycle}}
c Generated: {{generation_date}}
c Average Power: {{average_power}} MW
c
c BLOCK 1: CELL CARDS
c
c --- Fixed Core Geometry ---
  1  1  -2.7   -10  100  -200          $ ATR Core
  2  2  -1.0   -20  200  -300          $ Water
c
c --- Variable Neck Shims ---
{{ne_cells}}
{{se_cells}}
c
c --- End of Cell Block ---

c
c BLOCK 2: SURFACE CARDS
c
c --- Fixed Surfaces ---
  10  rpp  0 100  0 100  0 100
  20  rpp  0 120  0 120  0 120
c
c --- Variable Control Drum Positions ---
{{oscc_surfaces}}
c
c --- End of Surface Block ---

c
c BLOCK 3: DATA CARDS
c
mode n p
nps 10000
"""
    
    # Write template file
    template_path = os.path.join(output_dir, 'bench.template')
    with open(template_path, 'w') as f:
        f.write(template_content)
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(output_dir))
    template = env.get_template('bench.template')
    
    # Generate inputs for each cycle
    print(f"\nGenerating MCNP inputs in {output_dir}/...")
    print("-" * 70)
    
    for cycle in CYCLES:
        data = cycle_data[cycle]
        
        # Generate cycle-specific geometry
        oscc_surfaces = generate_oscc_surfaces(data['ne_angle'], data['se_angle'])
        ne_cells = generate_neck_shim_cells(data['ne_shims'], 'NE')
        se_cells = generate_neck_shim_cells(data['se_shims'], 'SE')
        
        # Render template
        output = template.render(
            cycle=cycle,
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            average_power=f'{data["power"]:.2f}',
            ne_angle=data['ne_angle'],
            se_angle=data['se_angle'],
            oscc_surfaces=oscc_surfaces,
            ne_cells=ne_cells,
            se_cells=se_cells
        )
        
        # Write output
        filename = os.path.join(output_dir, f'bench_{cycle}.i')
        with open(filename, 'w') as f:
            f.write(output)
        
        print(f"✓ {cycle:5s}: {len(output):5d} bytes | "
              f"Power={data['power']:5.2f} MW | "
              f"NE={data['ne_angle']:3d}° | SE={data['se_angle']:3d}°")
    
    print("-" * 70)
    print(f"\n✓ Generated {len(CYCLES)} MCNP inputs in {output_dir}/")
    print(f"  Template: {template_path}")
    print(f"  Total reactor history: {sum(d['duration_days'] for d in cycle_data.values()):.1f} days")
    
    print("\nNext steps:")
    print(f"  1. Inspect generated files: ls -lh {output_dir}/bench_*.i")
    print(f"  2. Test one input: mcnp6 inp={output_dir}/bench_138B.i")
    print(f"  3. Run full batch (if MCNP available)")


if __name__ == "__main__":
    generate_inputs()
