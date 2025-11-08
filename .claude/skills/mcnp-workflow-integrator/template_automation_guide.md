# Template Automation Guide

Using Jinja2 for MCNP input generation from templates.

## Overview

Template-based automation is ideal when you have:
- Large existing base model (e.g., reactor core geometry)
- Need for parametric variations (same structure, different values)
- Multiple similar cases (cycle-by-cycle analysis)

**Key Advantage**: Preserves existing model structure while automating variations.

---

## When to Use Templates

✅ **Use template-based approach when**:
- Base model is large and stable (thousands of lines)
- Experiment-specific geometry inserted into host reactor
- Only parameters change (power, control positions, materials)
- Manual model already exists and works
- Multiple people need to understand the model

❌ **Don't use templates when**:
- Building model from scratch
- Geometry varies significantly between cases
- Algorithmic complexity needed (lattices, assemblies)
- Complete flexibility required

---

## Basic Template Structure

### Simple Variable Substitution

**MCNP Template** (`simple_template.inp`):
```jinja2
Simple Reactor Model - {{ cycle_name }}
c
c Average Power: {{ power_MW }} MW
c Duration: {{ duration_days }} days
c
c CELLS
c
1 1 -10.8  -1  imp:n=1  vol={{ fuel_volume }}  $ Fuel
2 2 -1.0   1 -2  imp:n=1  $ Moderator
3 0        2     imp:n=0  $ Void

c SURFACES
c
1 so {{ fuel_radius }}  $ Fuel sphere
2 so {{ moderator_radius }}  $ Moderator outer

c MATERIALS
c
m1  $ UO2 fuel ({{ enrichment }}% U-235)
    92235.00c  {{ u235_fraction }}
    92238.00c  {{ u238_fraction }}
     8016.00c  {{ o16_fraction }}

c DATA
c
kcode 10000 1.0 50 250
ksrc 0 0 0
```

**Python Generation Script**:
```python
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('simple_template.inp')

# Define parameters
params = {
    'cycle_name': '138B',
    'power_MW': 112.5,
    'duration_days': 42.3,
    'fuel_volume': 1256.64,
    'fuel_radius': 6.5,
    'moderator_radius': 12.0,
    'enrichment': 4.5,
    'u235_fraction': 4.816186e-03,
    'u238_fraction': 1.932238e-02,
    'o16_fraction': 4.827713e-02
}

# Render template
output = template.render(**params)

# Write output
with open('output/case_138B.i', 'w') as f:
    f.write(output)

print(f"Generated: output/case_138B.i")
```

---

## Advanced Template Features

### Conditional Blocks

**Use Case**: Include/exclude geometry based on configuration

**Template**:
```jinja2
c CELLS
c
1 1 -10.8  -1  imp:n=1  $ Fuel

{% if include_reflector %}
c Reflector region
2 2 -1.85  1 -2  imp:n=1  $ Graphite reflector
3 0        2     imp:n=0  $ Void
{% else %}
c No reflector
2 0        1     imp:n=0  $ Void
{% endif %}
```

**Usage**:
```python
params = {
    'include_reflector': True  # or False
}

output = template.render(**params)
```

### Loops

**Use Case**: Generate repetitive geometry (multiple fuel pins)

**Template**:
```jinja2
c CELLS - Fuel Pins
c
{% for pin in range(1, num_pins + 1) %}
{{ 100 + pin }} 1 -10.8  -{{ 100 + pin }}  imp:n=1  $ Fuel pin {{ pin }}
{% endfor %}

c SURFACES - Fuel Pins
c
{% for pin in range(1, num_pins + 1) %}
{{ 100 + pin }} c/z {{ pin_positions[pin-1][0] }} {{ pin_positions[pin-1][1] }} {{ pin_radius }}
{% endfor %}
```

**Usage**:
```python
import numpy as np

# Generate pin positions (e.g., hexagonal array)
num_pins = 19
pin_positions = generate_hex_array(pitch=1.26, rings=2)  # Returns list of (x,y) tuples

params = {
    'num_pins': num_pins,
    'pin_positions': pin_positions,
    'pin_radius': 0.4095
}

output = template.render(**params)
```

### Custom Filters

**Use Case**: Format numbers in MCNP-compatible way

**Define Custom Filters**:
```python
def format_scientific(value, precision=6):
    """Format number in scientific notation."""
    return f"{value:.{precision}e}"

def format_mcnp_number(value):
    """Format number in MCNP style (no leading zero)."""
    s = f"{value:.6e}"
    # MCNP style: 1.234e-03 not 1.234E-03
    return s.replace('E', 'e').replace('e+0', 'e+').replace('e-0', 'e-')

# Add filters to Jinja2 environment
env.filters['sci'] = format_scientific
env.filters['mcnp'] = format_mcnp_number
```

**Template**:
```jinja2
m1  $ UO2 fuel
    92235.00c  {{ u235_fraction | mcnp }}
    92238.00c  {{ u238_fraction | mcnp }}
     8016.00c  {{ o16_fraction | mcnp }}
```

**Output**:
```
m1  $ UO2 fuel
    92235.00c  4.816186e-03
    92238.00c  1.932238e-02
     8016.00c  4.827713e-02
```

---

## Complete Example: AGR-1 Multi-Cycle Template

### Template Structure

**Base Template** (`agr1_template.inp`):
```jinja2
AGR-1 Experiment - Cycle {{ cycle_name }}
c
c Generated: {{ generation_date }}
c Average Power: {{ avg_power_MW }} MW
c OSCC Angle: {{ oscc_angle }} degrees
c Neck Shim: {{ neck_shim_state }}
c
c ============================================================================
c CELLS - Base ATR Geometry (Static)
c ============================================================================
c
c ATR Fuel Elements (Northeast Lobe)
60106 2106 7.969921e-02  1111  -1118   74  -29   53  100 -110 $Elem  6 RZ 1 AZ 1
60107 2107 7.969921e-02  1111  -1118   74  -29  110 -120 $Elem  6 RZ 1 AZ 2
c ... [13,000+ lines of ATR base geometry - static, not changed] ...

c ============================================================================
c CELLS - AGR-1 Experiment Geometry (Generated)
c ============================================================================
{{ agr1_cells }}

c ============================================================================
c SURFACES - Base ATR Geometry (Static)
c ============================================================================
c
1111 px -9.843
1112 px -6.413
c ... [ATR surfaces - static] ...

c ============================================================================
c SURFACES - AGR-1 Experiment (Generated)
c ============================================================================
{{ agr1_surfaces }}

c ============================================================================
c SURFACES - OSCC (Cycle-Specific)
c ============================================================================
{{ oscc_surfaces }}

c ============================================================================
c MATERIALS - Base ATR (Static)
c ============================================================================
c
m2106  $ ATR Fuel Element 6, Region 1, Zone 1
       92235.00c  1.234e-03
       92238.00c  5.678e-03
c ... [ATR materials - static] ...

c ============================================================================
c MATERIALS - AGR-1 Experiment (Generated)
c ============================================================================
{{ agr1_materials }}

c ============================================================================
c MATERIALS - Neck Shim (Cycle-Specific)
c ============================================================================
{{ neck_shim_cells }}

c ============================================================================
c DATA CARDS
c ============================================================================
c
kcode 10000 1.0 50 250
ksrc {{ ksrc_x }} {{ ksrc_y }} {{ ksrc_z }}
c
c Tallies
f4:n (1001 1002 1003 1004)  $ Flux in fuel compacts
f7:n (1001 1002 1003 1004)  $ Power in fuel compacts
```

### Generation Script

**Complete Implementation** (`create_agr1_inputs.py`):
```python
#!/usr/bin/env python3
"""
Generate AGR-1 MCNP inputs for all cycles.

Usage:
    python create_agr1_inputs.py
"""

import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path

# Import data processing tools
from data_integration_tools import (
    time_weighted_average,
    find_closest_value,
    process_power_history,
    process_control_positions,
    process_binary_state
)


class AGR1InputGenerator:
    """Generate AGR-1 MCNP inputs for all cycles."""

    def __init__(self, data_dir='data', template_file='agr1_template.inp'):
        self.data_dir = Path(data_dir)
        self.template_file = template_file

        # Load template
        env = Environment(loader=FileSystemLoader('.'))
        self.template = env.get_template(template_file)

        # MCNP model parameters
        self.allowed_oscc_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
        self.neck_shim_materials = {
            0: (10, 1.00276e-1),  # Water
            1: (71, 4.55926e-2)   # Hafnium
        }

        # Cycles to process
        self.cycles = ['138B', '139A', '139B', '140A', '140B',
                      '141A', '142A', '142B', '143A', '143B',
                      '144A', '144B', '145A']

    def generate_all(self, output_dir='mcnp'):
        """Generate inputs for all cycles."""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        for cycle in self.cycles:
            print(f"\nGenerating cycle {cycle}...")
            self.generate_cycle(cycle, output_dir)

        print(f"\n✓ Generated {len(self.cycles)} input files in {output_dir}")

    def generate_cycle(self, cycle_name, output_dir):
        """Generate input for one cycle."""

        # Process external data
        params = self._gather_parameters(cycle_name)

        # Generate AGR-1 geometry
        params['agr1_cells'] = self._generate_agr1_cells()
        params['agr1_surfaces'] = self._generate_agr1_surfaces()
        params['agr1_materials'] = self._generate_agr1_materials()

        # Generate cycle-specific geometry
        params['oscc_surfaces'] = self._generate_oscc_surfaces(params['oscc_angle'])
        params['neck_shim_cells'] = self._generate_neck_shim_cells(
            params['neck_shim_material'],
            params['neck_shim_density']
        )

        # Metadata
        params['generation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Render template
        output = self.template.render(**params)

        # Write output
        output_file = output_dir / f'bench_{cycle_name}.i'
        with open(output_file, 'w') as f:
            f.write(output)

        print(f"  Written: {output_file}")
        print(f"    Power: {params['avg_power_MW']:.2f} MW")
        print(f"    OSCC:  {params['oscc_angle']:.0f}°")
        print(f"    Neck:  {params['neck_shim_state']}")

    def _gather_parameters(self, cycle_name):
        """Gather all parameters for one cycle."""

        # Power history
        power_params = process_power_history(
            self.data_dir / 'power.csv',
            cycle_name
        )

        # Control positions
        oscc_params = process_control_positions(
            self.data_dir / 'oscc.csv',
            cycle_name,
            self.allowed_oscc_angles
        )

        # Neck shim state
        neck_params = process_binary_state(
            self.data_dir / 'neck_shim.csv',
            cycle_name,
            self.neck_shim_materials
        )

        # Combine all parameters
        return {
            'cycle_name': cycle_name,
            'avg_power_MW': power_params['avg_power_MW'],
            'duration_days': power_params['duration_days'],
            'oscc_angle': oscc_params['selected_angle_discrete'],
            'neck_shim_state': neck_params['state_description'],
            'neck_shim_material': neck_params['material_number'],
            'neck_shim_density': neck_params['density'],
            'ksrc_x': 0.0,
            'ksrc_y': 0.0,
            'ksrc_z': 0.0
        }

    def _generate_agr1_cells(self):
        """Generate AGR-1 experiment cell block."""
        cells = []

        # 6 capsules × 3 stacks × 4 compacts
        for capsule in range(1, 7):
            for stack in range(1, 4):
                for compact in range(1, 5):
                    # Cell number: 90000 + capsule*1000 + stack*100 + compact*10
                    cell_num = 90000 + capsule*1000 + stack*100 + compact*10 + 1

                    # Material number
                    mat_num = 9000 + capsule*100 + stack*10 + compact

                    # Universe number
                    univ = capsule*100 + stack*10 + compact

                    # Surface numbers
                    surf_inner = 9000 + capsule*100 + stack*10 + compact
                    surf_outer = surf_inner + 1

                    cell = (f"{cell_num} {mat_num} -10.8  -{surf_inner}  "
                           f"u={univ}4 vol=948.35  imp:n=1  "
                           f"$ Cap{capsule} Stk{stack} Cmp{compact} Kernel")

                    cells.append(cell)

        return '\n'.join(cells)

    def _generate_agr1_surfaces(self):
        """Generate AGR-1 experiment surface block."""
        surfaces = []

        for capsule in range(1, 7):
            for stack in range(1, 4):
                for compact in range(1, 5):
                    surf_num = 9000 + capsule*100 + stack*10 + compact

                    surface = f"{surf_num} so 0.0250  $ Cap{capsule} Stk{stack} Cmp{compact}"
                    surfaces.append(surface)

        return '\n'.join(surfaces)

    def _generate_agr1_materials(self):
        """Generate AGR-1 fuel materials."""
        materials = []

        for capsule in range(1, 7):
            for stack in range(1, 4):
                for compact in range(1, 5):
                    mat_num = 9000 + capsule*100 + stack*10 + compact

                    material = f"""m{mat_num}  $ UO2 kernel - Cap{capsule} Stk{stack} Cmp{compact}
     92235.00c  4.816186e-03
     92238.00c  1.932238e-02
      8016.00c  4.827713e-02"""

                    materials.append(material)

        return '\n'.join(materials)

    def _generate_oscc_surfaces(self, angle):
        """Generate OSCC surfaces for given angle."""
        # Simplified - actual implementation would include rotated surfaces
        surfaces = f"c OSCC rotated to {angle} degrees\n"
        surfaces += f"c (Surface definitions would go here)\n"
        return surfaces

    def _generate_neck_shim_cells(self, material_num, density):
        """Generate neck shim cell definitions."""
        cells = f"c Neck shim cells - material m{material_num}\n"
        cells += f"5001 {material_num} {density:.5e}  -5001  imp:n=1  $ NE neck shim\n"
        cells += f"5002 {material_num} {density:.5e}  -5002  imp:n=1  $ SE neck shim\n"
        return cells


# Execute
if __name__ == "__main__":
    generator = AGR1InputGenerator()
    generator.generate_all()

    print("\n✓ Input generation complete!")
    print("\nNext steps:")
    print("  1. Validate inputs: python validate_inputs.py")
    print("  2. Run calculations: sbatch run_all.sh")
```

---

## Advanced Patterns

### Nested Templates (Template Includes)

**Main Template** (`main.inp`):
```jinja2
Reactor Model
c
c CELLS
{% include 'cells_template.inp' %}

c SURFACES
{% include 'surfaces_template.inp' %}

c MATERIALS
{% include 'materials_template.inp' %}
```

**Sub-Template** (`cells_template.inp`):
```jinja2
{% for assembly in assemblies %}
{{ assembly.cell_num }} {{ assembly.material }} {{ assembly.density }}  {{ assembly.surfaces }}  imp:n=1
{% endfor %}
```

### Macros (Reusable Template Functions)

**Define Macro**:
```jinja2
{% macro fuel_pin(number, x, y, radius) %}
c Fuel pin {{ number }}
{{ 100 + number }} 1 -10.8  -{{ 100 + number }}  imp:n=1  $ Fuel pin {{ number }}
{{ 100 + number }} c/z {{ x }} {{ y }} {{ radius }}  $ Pin {{ number }} surface
{% endmacro %}
```

**Use Macro**:
```jinja2
c FUEL PINS
{% for i, pos in enumerate(pin_positions) %}
{{ fuel_pin(i+1, pos[0], pos[1], 0.4095) }}
{% endfor %}
```

---

## Template Best Practices

### 1. Separate Static and Dynamic Content

✅ **Good**:
```jinja2
c ============ STATIC BASE GEOMETRY ============
[Large static block - unchanged]

c ============ DYNAMIC INSERTIONS ============
{{ generated_content }}
```

❌ **Bad**:
```jinja2
c Mixing static and dynamic throughout
cell1 static content
{{ dynamic_cell2 }}
cell3 static content
{{ dynamic_cell4 }}
```

### 2. Use Clear Section Markers

```jinja2
c ============================================================================
c SECTION: Fuel Assemblies (Generated)
c Count: {{ num_assemblies }}
c ============================================================================
{{ fuel_assemblies }}
```

### 3. Include Generation Metadata

```jinja2
c Generated: {{ generation_date }}
c Script: {{ script_name }}
c Parameters: {{ parameters_file }}
c Cycle: {{ cycle_name }}
```

### 4. Validate Before Rendering

```python
def validate_parameters(params):
    """Validate parameters before template rendering."""
    assert 0 < params['enrichment'] < 100, "Invalid enrichment"
    assert params['power_MW'] > 0, "Power must be positive"
    assert all(isinstance(x, (int, float)) for x in params['pin_positions']),\
        "Pin positions must be numeric"
    # ... more validation

# Use validation
validate_parameters(params)
output = template.render(**params)
```

### 5. Comment the Template Structure

```jinja2
{#
This template generates MCNP inputs for AGR-1 experiment.

Variables required:
- cycle_name: str (e.g., '138B')
- avg_power_MW: float
- oscc_angle: float (degrees)
- agr1_cells: str (generated cell block)
- agr1_surfaces: str (generated surface block)

Generation script: create_agr1_inputs.py
#}
```

---

## Debugging Templates

### View Rendered Output

```python
# Render to string first, check before writing
output = template.render(**params)

# Print first 50 lines
for i, line in enumerate(output.split('\n')[:50], 1):
    print(f"{i:3d}: {line}")

# Check for issues
if 'None' in output:
    print("WARNING: Template contains 'None' - missing variable?")
```

### Test with Minimal Parameters

```python
# Start with minimal params, add incrementally
minimal_params = {
    'cycle_name': 'TEST',
    'power_MW': 100.0
}

try:
    output = template.render(**minimal_params)
    print("Minimal render successful")
except Exception as e:
    print(f"Error with minimal params: {e}")
```

---

## Summary

**Template-Based Approach**:

**Strengths**:
- Preserves existing model structure
- Easy to understand (MCNP syntax visible)
- Rapid parametric variations
- Lower learning curve

**Limitations**:
- Less flexible than programmatic
- Template can get complex
- Variable management challenging for large models

**Best For**:
- Experiment in existing reactor model (AGR-1 example)
- Parametric studies with stable base geometry
- When manual model already exists
- Multiple collaborators need model transparency

**Key Tools**:
- **Jinja2**: Template engine
- **pandas**: Data processing
- **pathlib**: File management

**Next Steps**:
1. Identify static vs. dynamic content in your model
2. Create template with clear section markers
3. Build parameter dictionary from external data
4. Validate parameters before rendering
5. Test with simple case first
