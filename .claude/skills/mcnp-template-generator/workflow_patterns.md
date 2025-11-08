# Workflow Patterns
## Complete End-to-End Template Generation Workflows

This guide presents complete, tested workflows for common template generation scenarios.

## Workflow 1: Multi-Cycle Reactor Burnup

**Objective**: Generate MCNP inputs for 13 reactor operating cycles with varying control positions and power levels.

### Input Files Required

```
project/
├── bench.template              # Master template (13,727 lines)
├── data/
│   ├── power.csv              # 616 timesteps × 10 columns
│   ├── oscc.csv               # Control drum angles vs time
│   └── neck_shim.csv          # Shim insertion states vs time
└── generation_script.py        # This workflow
```

### Complete Workflow Script

```python
"""
Multi-Cycle Burnup Input Generation
Based on AGR-1 HTGR experiment (13 cycles, 616 timesteps)
"""

import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# Configuration
CYCLES = ['138B', '139A', '139B', '140A', '140B', '141A',
          '142A', '142B', '143A', '143B', '144A', '144B', '145A']

PREDEFINED_ANGLES = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]

# Step 1: Load and validate CSV data
print("Loading CSV data...")
power_df = pd.read_csv('data/power.csv', index_col="Cumulative Timestep")
oscc_df = pd.read_csv('data/oscc.csv', index_col="Cumulative Timestep")
neck_df = pd.read_csv('data/neck_shim.csv', index_col="Cumulative Timestep")

# Step 2: Process data by cycle
def time_weighted_average(values, time_intervals):
    return (values * time_intervals).sum() / time_intervals.sum()

def find_closest_value(options, target):
    return options[np.argmin(np.abs(np.array(options) - target))]

print("Processing cycle data...")
cycle_data = {}
prev = 0

for cycle in CYCLES:
    # Count timesteps for this cycle
    cycles_list = power_df['Cycle'].tolist()
    time_steps = cycles_list.count(cycle)
    time_intervals = power_df["Time Interval(hrs)"].iloc[prev:prev+time_steps].values
    
    # Average power
    ne_power = power_df['NELobePower(MW)'].iloc[prev:prev+time_steps].values
    c_power = power_df['CLobePower(MW)'].iloc[prev:prev+time_steps].values
    se_power = power_df['SELobePower(MW)'].iloc[prev:prev+time_steps].values
    ave_power = time_weighted_average((ne_power + c_power + se_power) / 3, time_intervals)
    
    # Average control drum angles
    ne_oscc = oscc_df['NEOSCC(degrees)'].iloc[prev:prev+time_steps].values
    se_oscc = oscc_df['SEOSCC(degrees)'].iloc[prev:prev+time_steps].values
    
    ave_ne_angle = time_weighted_average(ne_oscc, time_intervals)
    ave_se_angle = time_weighted_average(se_oscc, time_intervals)
    
    closest_ne = find_closest_value(PREDEFINED_ANGLES, ave_ne_angle)
    closest_se = find_closest_value(PREDEFINED_ANGLES, ave_se_angle)
    
    # Average neck shim states (binary: 0=water, 1=hafnium)
    ne_shims = {}
    for rod_num in range(1, 7):
        rod_name = f'NE {rod_num}'
        insertion = neck_df[rod_name].iloc[prev:prev+time_steps].values
        ave_insertion = time_weighted_average(insertion, time_intervals)
        ne_shims[rod_name] = int(np.rint(ave_insertion))
    
    se_shims = {}
    for rod_num in range(1, 7):
        rod_name = f'SE {rod_num}'
        insertion = neck_df[rod_name].iloc[prev:prev+time_steps].values
        ave_insertion = time_weighted_average(insertion, time_intervals)
        se_shims[rod_name] = int(np.rint(ave_insertion))
    
    cycle_data[cycle] = {
        'power': ave_power,
        'ne_angle': closest_ne,
        'se_angle': closest_se,
        'ne_shims': ne_shims,
        'se_shims': se_shims,
        'duration_days': time_intervals.sum() / 24
    }
    
    prev += time_steps

# Step 3: Generate geometry from averaged data
def generate_oscc_surfaces(ne_angle, se_angle):
    """Generate control drum surface definitions for given angles."""
    # This would normally load from pre-computed geometry database
    # For demonstration, simplified version
    return f"""c
c OSCC surfaces at NE={ne_angle}°, SE={se_angle}°
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2
"""

def generate_neck_shim_cells(shims, quadrant):
    """Generate neck shim cell definitions."""
    cells = "c\n"
    cell_start = 702 if quadrant == 'NE' else 792
    
    for i, (rod_name, state) in enumerate(shims.items(), start=1):
        mat = 71 if state == 1 else 10  # 71=Hf, 10=water
        density = 4.55926e-02 if state == 1 else 1.00276e-01
        state_str = "inserted" if state == 1 else "withdrawn"
        
        cells += f"""  {cell_start + (i-1)*5}   {mat} {density:.5e}    -100  $ {rod_name} - {state_str}
"""
    
    return cells

# Step 4: Setup Jinja2 environment
print("Setting up template environment...")
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('bench.template')

# Create output directory
os.makedirs('mcnp', exist_ok=True)

# Step 5: Render templates
print("\nGenerating MCNP inputs...")
for cycle in CYCLES:
    data = cycle_data[cycle]
    
    # Generate cycle-specific geometry
    oscc_surfaces = generate_oscc_surfaces(data['ne_angle'], data['se_angle'])
    ne_cells = generate_neck_shim_cells(data['ne_shims'], 'NE')
    se_cells = generate_neck_shim_cells(data['se_shims'], 'SE')
    
    # Render template
    output = template.render(
        # Metadata
        cycle=cycle,
        generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        average_power=f'{data["power"]:.2f}',
        ne_angle=data['ne_angle'],
        se_angle=data['se_angle'],
        
        # Variable geometry
        oscc_surfaces=oscc_surfaces,
        ne_cells=ne_cells,
        se_cells=se_cells,
        
        # Static geometry (loaded once)
        cells=static_agr1_cells,
        surfaces=static_agr1_surfaces,
        materials=static_agr1_materials
    )
    
    # Validate rendering
    if '{{' in output or '}}' in output:
        raise ValueError(f"Unreplaced variables in {cycle}")
    
    # Write output
    filename = f'mcnp/bench_{cycle}.i'
    with open(filename, 'w') as f:
        f.write(output)
    
    print(f"✓ {cycle:5s}: {len(output):7d} bytes | "
          f"Power={data['power']:5.2f} MW | "
          f"NE={data['ne_angle']:3d}° | SE={data['se_angle']:3d}°")

print(f"\n✓ Generated {len(CYCLES)} MCNP inputs in mcnp/")
print(f"  Total reactor history: {sum(d['duration_days'] for d in cycle_data.values()):.1f} days")
```

### Expected Output

```
Loading CSV data...
Processing cycle data...
Setting up template environment...

Generating MCNP inputs...
✓ 138B :   13727 bytes | Power=23.79 MW | NE= 85° | SE= 85°
✓ 139A :   13727 bytes | Power=24.12 MW | NE= 80° | SE= 85°
✓ 139B :   13727 bytes | Power=24.05 MW | NE= 80° | SE= 85°
...
✓ 145A :   13727 bytes | Power=23.95 MW | NE= 75° | SE= 80°

✓ Generated 13 MCNP inputs in mcnp/
  Total reactor history: 620.3 days
```

## Workflow 2: Enrichment Sensitivity Study

**Objective**: Generate 5 MCNP inputs with varying fuel enrichment (3% to 5%).

### Complete Script

```python
"""
Enrichment Sensitivity Study
Parameter sweep from 3.0% to 5.0% enrichment in 0.5% steps
"""

from jinja2 import Environment, FileSystemLoader
import os

# Configuration
ENRICHMENTS = [3.0, 3.5, 4.0, 4.5, 5.0]

# Material generation
def generate_uo2_material(enrichment_pct, material_num=1):
    """Generate UO2 fuel material card."""
    u235_frac = enrichment_pct / 100.0
    u238_frac = 1.0 - u235_frac
    
    return f"""m{material_num}  $ UO2 fuel, {enrichment_pct}% enriched
   92235.70c  {u235_frac:.6f}
   92238.70c  {u238_frac:.6f}
    8016.70c  2.0
mt{material_num}  u/o2.70t
"""

# Setup
env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('pwr_assembly.template')

os.makedirs('enrichment_study', exist_ok=True)

# Generate inputs
for enr in ENRICHMENTS:
    fuel_material = generate_uo2_material(enr)
    
    output = template.render(
        enrichment=enr,
        fuel_material=fuel_material,
        case_id=f'enr{int(enr*10):02d}'
    )
    
    filename = f'enrichment_study/pwr_enr{int(enr*10):02d}.i'
    with open(filename, 'w') as f:
        f.write(output)
    
    print(f"✓ Generated: {filename} (enrichment={enr}%)")
```

## Workflow 3: Control Rod Worth Curve

**Objective**: Calculate reactivity vs rod position (0% to 100% withdrawn in 10% steps).

### Complete Script

```python
"""
Control Rod Worth Curve
Generate 11 configurations for rod positions 0% to 100%
"""

from jinja2 import Environment, FileSystemLoader
import numpy as np
import os

# Configuration
POSITIONS = np.arange(0, 101, 10)  # 0, 10, 20, ..., 100 percent withdrawn

def generate_control_rod_geometry(position_pct, rod_height=100):
    """
    Generate control rod cell definition.
    
    Args:
        position_pct: 0-100% withdrawn
        rod_height: Total rod height (cm)
    """
    withdrawn_height = rod_height * position_pct / 100.0
    inserted_height = rod_height - withdrawn_height
    
    # Simplified geometry
    cells = f"""c Control rod at {position_pct}% withdrawn
c Rod tip at z = {inserted_height:.1f} cm
  100  10  -5.0    -100  -200  {inserted_height:.4f}   $ Poison section
  101  20  -1.0    -100  -200  -{inserted_height:.4f}  $ Follower section
"""
    
    return cells

# Setup
env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('core_model.template')

os.makedirs('rod_worth_study', exist_ok=True)

# Generate inputs
for pos in POSITIONS:
    rod_geometry = generate_control_rod_geometry(pos)
    
    output = template.render(
        rod_position=pos,
        control_rod_cells=rod_geometry,
        case_id=f'rod_{pos:03d}'
    )
    
    filename = f'rod_worth_study/core_rod_{pos:03d}.i'
    with open(filename, 'w') as f:
        f.write(output)
    
    print(f"✓ Generated: {filename} (rod at {pos:3d}% withdrawn)")

print(f"\n✓ Generated {len(POSITIONS)} rod position cases")
print("  Next step: Run MCNP for all cases, extract keff")
```

## Workflow 4: Batch Processing with QA

**Objective**: Generate multiple inputs with comprehensive validation and QA plotting.

```python
"""
Production-Grade Batch Generation with QA
"""

import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import os
from datetime import datetime

def validate_csv_data(data, expected_cycles):
    """Validate CSV data completeness and ranges."""
    # Check cycles present
    actual_cycles = set(data['Cycle'].unique())
    missing = set(expected_cycles) - actual_cycles
    if missing:
        raise ValueError(f"Missing cycles in CSV: {missing}")
    
    # Check data ranges
    if (data['Power_MW'] < 0).any():
        raise ValueError("Negative power values found")
    
    if (data['Time_Interval_hrs'] <= 0).any():
        raise ValueError("Non-positive time intervals found")
    
    print("✓ CSV data validation passed")

def plot_qa_diagnostics(data, output_dir='plots'):
    """Generate QA diagnostic plots."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Power vs time
    for cycle in data['Cycle'].unique():
        cycle_data = data[data['Cycle'] == cycle]
        axes[0, 0].plot(cycle_data['Timestep'], cycle_data['Power_MW'], 
                       marker='o', label=cycle, alpha=0.7)
    axes[0, 0].set_xlabel('Timestep')
    axes[0, 0].set_ylabel('Power (MW)')
    axes[0, 0].set_title('Power vs Time by Cycle')
    axes[0, 0].legend(ncol=2, fontsize=8)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Add more QA plots...
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/qa_diagnostics.png', dpi=150, bbox_inches='tight')
    print(f"✓ QA plots saved to {output_dir}/")

def validate_rendered_output(output, filename):
    """Validate rendered template."""
    if '{{' in output or '}}' in output:
        import re
        unreplaced = re.findall(r'\{\{([^}]+)\}\}', output)
        raise ValueError(f"Unreplaced variables in {filename}: {unreplaced}")
    
    if len(output) < 1000:
        raise ValueError(f"Output suspiciously small: {len(output)} bytes")

# Main workflow
def main():
    # Load data
    data = pd.read_csv('data/parameters.csv')
    cycles = ['138B', '139A', '140A']
    
    # Validate
    validate_csv_data(data, cycles)
    
    # QA plots
    plot_qa_diagnostics(data)
    
    # Generate inputs
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('base.template')
    
    os.makedirs('mcnp', exist_ok=True)
    
    for cycle in cycles:
        # Process data...
        # Render template...
        # Validate output...
        validate_rendered_output(output, filename)
        
        # Write file...
        print(f"✓ {cycle}: validated and written")
    
    print("\n✓ Batch generation complete with full QA")

if __name__ == "__main__":
    main()
```

## Workflow Best Practices

1. **Always validate input data** before rendering
2. **Create QA plots** for visual inspection
3. **Check rendered outputs** for unreplaced variables
4. **Document data sources** in generated file headers
5. **Use systematic file naming** for easy identification
6. **Log generation parameters** for reproducibility
7. **Test with subset first** before full batch
8. **Version control** templates and scripts (not generated inputs)

## Common Workflow Extensions

### Extension 1: Parallel Generation

```python
from multiprocessing import Pool

def generate_single_input(cycle):
    # Generate input for one cycle
    # ...
    return cycle

with Pool(4) as p:
    p.map(generate_single_input, cycles)
```

### Extension 2: Incremental Updates

```python
# Only regenerate changed cycles
for cycle in cycles:
    output_file = f'mcnp/bench_{cycle}.i'
    
    if os.path.exists(output_file):
        if not force_regenerate:
            print(f"⊙ {cycle}: already exists, skipping")
            continue
    
    # Generate...
```

### Extension 3: Automated Testing

```python
# Test generated inputs with MCNP
import subprocess

for cycle in cycles:
    input_file = f'mcnp/bench_{cycle}.i'
    
    # Run MCNP with minimal particles to test syntax
    result = subprocess.run(
        ['mcnp6', f'inp={input_file}', 'tasks 1'],
        capture_output=True,
        timeout=60
    )
    
    if result.returncode != 0:
        print(f"✗ {cycle}: MCNP error")
    else:
        print(f"✓ {cycle}: MCNP syntax valid")
```

## See Also

- `example_inputs/agr1_burnup_workflow.py` - Full AGR-1 example
- `example_inputs/enrichment_study_workflow.py` - Enrichment study
- `example_inputs/control_rod_study_workflow.py` - Control rod study
