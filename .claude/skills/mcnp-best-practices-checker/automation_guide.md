# MCNP Reactor Model Automation Guide

**Purpose:** Best practices for automated MCNP input generation

**When to use:** Models with ≥3 similar cases, parametric studies, reproducible research

---

## Decision Framework: When to Automate

### Automate When:

✅ **More than 3 similar cases**
- 5 enrichments × 4 burnup loadings = 20 inputs
- 13 reactor cycles with varying conditions
- Parameter studies (geometry, materials, power)

✅ **Parameters change frequently**
- Control positions vary cycle-to-cycle
- Burnup-dependent isotopics
- Experimental measurements update

✅ **Geometry follows algorithmic pattern**
- Lattices (assemblies, particle arrays)
- Symmetric structures (core quarters)
- Repeated units (fuel pins, compacts)

✅ **High error risk in manual entry**
- 10,000+ line files
- Complex numbering schemes
- Many cross-references

✅ **Reproducibility critical**
- Publication requirements
- Licensing submissions
- Collaboration with others

### Don't Automate When:

❌ **One-time model**
- Proof-of-concept calculation
- Single verification case
- Simple test problem

❌ **Highly irregular geometry**
- Experimental facility with unique features
- Ad-hoc modifications
- One-off design

❌ **Automation effort > manual effort**
- 1-2 simple inputs
- More time to automate than manually create
- Debugging automation too complex

---

## Two Approaches: Template vs Programmatic

### Template-Based (Jinja2)

**When to use:**
- Large existing base model (stable geometry)
- Experiment inserted into host reactor
- Parametric variations on fixed base
- Multiple similar cases from one template

**Pros:**
- Preserves complex validated geometry
- Clear separation: static vs dynamic
- Rapid parametric variations
- Lower learning curve

**Cons:**
- Limited to template variables
- Large template files still complex
- Less flexible than programmatic

**Example workflow (AGR-1 in ATR):**
```python
from jinja2 import Environment, FileSystemLoader
import pandas as pd

# Load template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('atr_base.template')

# Load experimental data
power_df = pd.read_csv('power.csv')

# Generate inputs for each cycle
cycles = ['138B', '139A', '139B', ..., '145A']

for cycle in cycles:
    # Extract cycle-specific parameters
    power = power_df[power_df['cycle'] == cycle]['power_MW'].values[0]
    duration = power_df[power_df['cycle'] == cycle]['days'].values[0]

    # Time-averaged control positions
    oscc_angle = calculate_average_angle(cycle)

    # Render template
    output = template.render(
        cycle=cycle,
        power=power,
        duration=duration,
        oscc_angle=oscc_angle,
        fuel_cells=generate_fuel_cells(cycle)
    )

    # Write to file
    with open(f'mcnp/atr_{cycle}.i', 'w') as f:
        f.write(output)
```

**Template structure (atr_base.template):**
```jinja2
AGR-1 Experiment in ATR, Cycle {{ cycle }}
c Generated: {{ generation_date }}
c Power: {{ power }} MW, Duration: {{ duration }} days
c
c CELLS
c
{{ fuel_cells }}  {# Programmatically generated #}
c
c ATR Core (Static)
10001  1  -1.0  -10001  imp:n=1  $ ATR fuel element 1
10002  1  -1.0  -10002  imp:n=1  $ ATR fuel element 2
...
c
c SURFACES
c
{{ oscc_surfaces }}  {# Cycle-specific control positions #}
c
c Static ATR surfaces
10001  rpp  -10 10 -10 10 0 100
...
```

---

### Programmatic (Python Functions)

**When to use:**
- Model built from scratch
- Regular/symmetric geometry
- Algorithmic complexity (lattices)
- Tight parameter coupling

**Pros:**
- Complete flexibility
- Algorithmic geometry generation
- Easy parameter studies
- Version control of logic

**Cons:**
- Higher learning curve
- Need to test generated outputs
- More code to maintain

**Example workflow (Microreactor):**
```python
def fuel_assembly(layer, number, variant='baseline'):
    """Generate complete fuel assembly geometry.

    Args:
        layer: Axial layer (0-3)
        number: Assembly number (1-36)
        variant: Fuel type ('baseline', 'variant1', etc.)

    Returns:
        (cells, surfaces, materials) as formatted strings
    """
    # Validate inputs
    assert 0 <= layer < 4, f"Invalid layer: {layer}"
    assert 1 <= number <= 36, f"Invalid assembly: {number}"

    # Calculate base IDs
    base = (layer + 1) * 1000 + number * 10

    # Generate cells
    cells = f"""c Layer {layer}, Assembly {number:02d} ({variant})
{base}01  {base}1  -10.5  -{base}01 -{base}02 {base}03  imp:n=1  $ Fuel pellet
{base}02  {base}2  -0.001 -{base}02  {base}01  imp:n=1           $ Gap
{base}03  {base}3  -6.5   -{base}03  {base}02  imp:n=1           $ Cladding
{base}04  4  -1.74  -{base}04  {base}03  imp:n=1                $ Moderator
"""

    # Generate surfaces
    surfaces = f"""c Layer {layer}, Assembly {number:02d} surfaces
{base}01  so  0.41    $ Fuel radius
{base}02  so  0.42    $ Gap outer
{base}03  so  0.48    $ Clad outer
{base}04  rhp 0 0 0  0 0 10  0 5 0  $ Hex boundary
"""

    # Generate materials (variant-dependent)
    enrichment = {'baseline': 4.5, 'variant1': 5.0, 'variant2': 5.5}[variant]
    materials = f"""c Layer {layer}, Assembly {number:02d} materials
m{base}1  92235.70c {enrichment/100}  92238.70c {1-enrichment/100}  $ UO2 fuel
      8016.70c 2.0
m{base}2  2004.70c 1.0  $ Helium gap
m{base}3  40000.70c 1.0  $ Zircaloy cladding
"""

    # Validate outputs
    assert_no_conflicts(base, existing_ids)

    return cells, surfaces, materials

# Build entire model
all_cells = ""
all_surfaces = ""
all_materials = ""

for layer in range(4):
    for assy in range(1, 37):
        variant = determine_variant(layer, assy)
        c, s, m = fuel_assembly(layer, assy, variant)
        all_cells += c
        all_surfaces += s
        all_materials += m

# Write MCNP input
write_mcnp_input('reactor.i', all_cells, all_surfaces, all_materials)
```

---

## Quality Assurance for Automation

### Validation During Generation

**Check constraints:**
```python
def validate_inputs(layer, assembly, variant):
    """Validate inputs before generation."""
    assert 0 <= layer < 4, "Layer out of range"
    assert 1 <= assembly <= 36, "Assembly number invalid"
    assert variant in ['baseline', 'variant1', 'variant2'], "Unknown variant"
```

**Check physical consistency:**
```python
def validate_geometry(radii):
    """Ensure radii increase monotonically."""
    for i in range(len(radii) - 1):
        assert radii[i] < radii[i+1], f"Radius {i} >= radius {i+1}"
```

**Check lattice dimensions:**
```python
def validate_lattice(imax, imin, jmax, jmin, kmax, kmin, fill_array):
    """Ensure fill array matches declared bounds."""
    expected = (imax-imin+1) * (jmax-jmin+1) * (kmax-kmin+1)
    actual = count_fill_entries(fill_array)  # Account for nR notation
    assert actual == expected, f"Fill count mismatch: {actual} vs {expected}"
```

### Validation After Generation

**Compare to reference:**
```python
def compare_to_reference(generated, reference):
    """Compare generated input to known-good reference."""
    # Extract key features
    gen_cells = extract_cell_ids(generated)
    ref_cells = extract_cell_ids(reference)

    # Check counts match
    assert len(gen_cells) == len(ref_cells), "Cell count mismatch"

    # Check specific values
    for cell_id in ref_cells:
        assert cell_id in gen_cells, f"Missing cell {cell_id}"
```

**Check for conflicts:**
```python
def check_numbering(input_file):
    """Detect duplicate IDs."""
    cells = extract_cell_ids(input_file)
    surfaces = extract_surface_ids(input_file)
    materials = extract_material_ids(input_file)

    conflicts = []

    if len(cells) != len(set(cells)):
        conflicts.append(f"Duplicate cells: {find_duplicates(cells)}")

    if len(surfaces) != len(set(surfaces)):
        conflicts.append(f"Duplicate surfaces: {find_duplicates(surfaces)}")

    if len(materials) != len(set(materials)):
        conflicts.append(f"Duplicate materials: {find_duplicates(materials)}")

    if conflicts:
        raise ValueError(f"Numbering conflicts: {conflicts}")
```

**Verify cross-references:**
```python
def check_cross_references(input_file):
    """Ensure all references are defined."""
    defined_surfaces = extract_surface_ids(input_file)
    referenced_surfaces = extract_cell_surface_refs(input_file)

    missing = referenced_surfaces - defined_surfaces
    if missing:
        raise ValueError(f"Undefined surfaces: {missing}")
```

---

## Complete Automation Example

**Project structure:**
```
reactor-model/
├── README.md                   # Complete workflow documentation
├── requirements.txt            # Python dependencies
├── data/
│   ├── power.csv              # Experimental measurements
│   ├── positions.csv          # Control positions
│   └── materials.json         # Material database
├── templates/
│   └── base_reactor.template  # Jinja2 template (if used)
├── scripts/
│   ├── input_definition.py    # Shared parameters
│   ├── create_inputs.py       # Main generation script
│   ├── validate_inputs.py     # Validation script
│   └── utils.py               # Helper functions
└── outputs/
    └── mcnp/                  # Generated inputs (gitignored)
```

**Main generation script (create_inputs.py):**
```python
#!/usr/bin/env python3
"""Generate all MCNP inputs for reactor parametric study."""

import pandas as pd
from input_definition import *
from utils import *

def main():
    print("Generating MCNP inputs...")

    # Load external data
    power_df = pd.read_csv('data/power.csv')

    # Generate inputs
    for cycle in cycles:
        print(f"  Generating {cycle}...")

        # Extract parameters
        power = power_df[power_df['cycle'] == cycle]['power_MW'].values[0]

        # Generate geometry
        cells, surfaces, materials = generate_geometry(cycle, power)

        # Validate before writing
        validate_generated_geometry(cells, surfaces, materials)

        # Write to file
        write_mcnp_input(f'outputs/mcnp/reactor_{cycle}.i',
                         cells, surfaces, materials)

    print(f"Generated {len(cycles)} inputs successfully")

    # Run validation suite
    print("Running validation...")
    validate_all_inputs('outputs/mcnp/*.i')

    print("Complete!")

if __name__ == '__main__':
    main()
```

**Validation script (validate_inputs.py):**
```python
#!/usr/bin/env python3
"""Validate all generated MCNP inputs."""

import sys
from pathlib import Path
from utils import *

def validate_input(filepath):
    """Validate single input file."""
    print(f"Validating {filepath}...")

    checks = {
        'syntax': check_basic_syntax(filepath),
        'numbering': check_no_duplicate_ids(filepath),
        'cross_refs': check_all_references_exist(filepath),
        'lattices': check_lattice_dimensions(filepath),
        'thermal': check_thermal_scattering(filepath),
    }

    failed = [name for name, passed in checks.items() if not passed]

    if failed:
        print(f"  FAILED: {', '.join(failed)}")
        return False
    else:
        print(f"  PASSED all checks")
        return True

def main():
    inputs = list(Path('outputs/mcnp').glob('*.i'))

    results = [validate_input(inp) for inp in inputs]

    if all(results):
        print(f"\n✓ All {len(inputs)} inputs validated successfully")
        sys.exit(0)
    else:
        print(f"\n✗ {sum(not r for r in results)} of {len(inputs)} failed validation")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## Time-Weighted Averaging

**Problem:** Continuous parameters → discrete MCNP states

**Example: Control rod positions**
```python
def time_weighted_average(values, time_intervals):
    """Calculate time-weighted average of parameter.

    Args:
        values: List of parameter values at each timestep
        time_intervals: Duration of each timestep (days)

    Returns:
        Time-weighted average value
    """
    total_time = sum(time_intervals)
    weighted_sum = sum(v * t for v, t in zip(values, time_intervals))
    return weighted_sum / total_time

# Usage
angles = [30, 45, 60, 45, 30]  # degrees
times = [10, 15, 20, 15, 10]   # days

ave_angle = time_weighted_average(angles, times)  # 45.0 degrees

# Find closest discrete position
available_angles = [0, 30, 45, 60, 90]
mcnp_angle = min(available_angles, key=lambda x: abs(x - ave_angle))
```

---

## Best Practices Summary

1. **Start simple, add complexity gradually**
   - Generate 1 input, validate thoroughly
   - Then generate all inputs

2. **Separate concerns**
   - Data (CSV) ≠ Logic (Python) ≠ Templates (Jinja2)

3. **Validate at every step**
   - Input validation before generation
   - Generation-time checks
   - Post-generation validation suite

4. **Document everything**
   - README explains workflow
   - Comments in generation code
   - Comments in generated MCNP inputs

5. **Version control all source**
   - Scripts, templates, data files
   - NOT generated outputs (too large)

6. **Single command regeneration**
   - `python create_inputs.py` regenerates everything
   - Reproducible by others

---

**END OF AUTOMATION GUIDE**

For reactor patterns see: reactor_patterns_reference.md
For reproducibility see: reproducibility_checklist.md
