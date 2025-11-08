# MCNP Template Generator

## Purpose

Automate the generation of multiple MCNP input files from a single master template using Jinja2 templating and CSV data files. Essential for multi-cycle burnup calculations, parameter studies, and configuration management.

## When to Use This Skill

**Use this skill when**:
- ✅ Generating multiple MCNP inputs with similar geometry but varying parameters
- ✅ Modeling reactor operating history (multiple cycles with different control positions)
- ✅ Conducting parameter sensitivity studies (varying enrichment, temperature, materials)
- ✅ Managing configuration variants (different operational states of same reactor)
- ✅ Automating benchmark series (same model, different conditions)

**Do NOT use this skill when**:
- ❌ Building a single one-off MCNP input (use mcnp-input-builder instead)
- ❌ Need real-time coupling or dynamic simulations
- ❌ Template complexity exceeds benefit (< 3 variants)

## Core Workflow

### Step 1: Identify Parameterizable Sections

**Analyze existing MCNP input** to find:
- Sections that vary between cycles/scenarios
- Parameters driven by operational data
- Geometry/material variants

**Example findings**:
```
Fixed Content:
  - Reactor core geometry (always the same)
  - Structural materials
  - Physics cards (mostly constant)

Variable Content:
  - Control drum positions (vary by cycle)
  - Neck shim rod states (vary by cycle)
  - Test assembly configurations (vary by design)
  - Material compositions (evolve with burnup)
```

### Step 2: Create Jinja2 Template

**Convert input → template** by replacing variable sections with placeholders:

**Before** (MCNP input):
```mcnp
c Control drum surfaces
  981   c/z   48.0375  -18.1425  9.195  $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195  $ DRUM E2 AT 85 DEGREES
```

**After** (Jinja2 template):
```jinja2
c Control drum surfaces
{{oscc_surfaces}}
```

**Template syntax**:
- `{{variable}}` - Simple variable substitution
- No loops/conditionals in template (keep logic in Python)
- Template remains valid MCNP input (can be tested standalone)

### Step 3: Design CSV Data Files

**Create structured data files** for parameters:

**Example: control_positions.csv**
```csv
Cycle, Timestep, Time_Interval_hrs, OSCC_NE_deg, OSCC_SE_deg
138B, 1, 24.0, 80, 85
138B, 2, 24.0, 82, 87
...
145A, 53, 18.5, 75, 78
```

**Schema design principles**:
- One row per timestep or configuration
- Cycle/scenario identifier column
- Time interval column (for averaging)
- Clear column names with units

### Step 4: Apply Time-Weighted Averaging

**Collapse operational history** into representative values:

```python
# Read CSV data
data = pd.read_csv('control_positions.csv')

# Group by cycle
for cycle in cycles:
    cycle_data = data[data['Cycle'] == cycle]
    time_intervals = cycle_data['Time_Interval_hrs'].values

    # Time-weighted average
    ave_angle_ne = (cycle_data['OSCC_NE_deg'] * time_intervals).sum() / time_intervals.sum()

    # Snap to predefined values (if applicable)
    predefined_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
    closest_angle = predefined_angles[np.argmin(np.abs(predefined_angles - ave_angle_ne))]
```

**For binary states** (0/1):
```python
ave_state = (states * time_intervals).sum() / time_intervals.sum()
representative_state = int(np.rint(ave_state))  # Round to 0 or 1
```

### Step 5: Render Template

**Apply data to template** using Jinja2:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('base_model.template')

for cycle in cycles:
    # Prepare data for this cycle
    data = {
        'oscc_surfaces': oscc_surfaces[cycle],
        'ne_cells': ne_cells[cycle],
        'se_cells': se_cells[cycle],
        # ... other cycle-specific data
    }

    # Render template
    output = template.render(**data)

    # Write output file
    with open(f'mcnp/input_{cycle}.i', 'w') as f:
        f.write(output)
```

### Step 6: Validate Generated Inputs

**Pre-check before MCNP execution**:
- ✅ All placeholders filled (no remaining `{{...}}`)
- ✅ Cell/surface/material numbers consistent
- ✅ File sizes reasonable (compare to base input)
- ✅ Visual inspection of key sections

## Key Concepts

### Jinja2 Template Variables

**Simple substitution** (most common):
```jinja2
{{variable_name}}
```

**In Python**:
```python
template.render(variable_name="replacement text")
```

**Multi-line strings**:
```python
ne_cells = """c
  702   71 4.55926e-02    701   -702  100  -200
c
  707   71 4.55926e-02    706   -707  100  -200
"""
template.render(ne_cells=ne_cells)
```

### Time-Weighted Averaging

**Formula**:
```
Average = Σ(value_i × duration_i) / Σ(duration_i)
```

**Use cases**:
- **Continuous parameters**: Power, temperature, control angles
- **Binary parameters**: Shim rods in/out (round to 0 or 1 after averaging)
- **Discrete parameters**: Snap to nearest predefined value

**Why this works**: Represents the "effective" configuration over the cycle duration

### Systematic File Naming

**Pattern**: `<base>_<cycle>_<optional>.i`

**Examples**:
- `bench_138B.i` (cycle 138B)
- `bench_139A.i` (cycle 139A)
- `sensitivity_case01_enr45.i` (sensitivity study, case 1, 4.5% enrichment)

**Benefits**:
- Easy sorting and identification
- Traceability to data sources
- Supports automation scripts

### Directory Organization

**Recommended structure**:
```
project/
├── base_model.template          # Master template (version controlled)
├── generation_script.py         # Rendering script (version controlled)
├── data/
│   ├── power.csv               # Operational data (version controlled)
│   ├── control_positions.csv  # (version controlled)
│   └── cycle_definitions.csv  # (version controlled)
├── mcnp/                       # Generated inputs (excluded from git)
│   ├── bench_138B.i
│   ├── bench_139A.i
│   └── ...
└── plots/                      # QA plots (excluded from git)
    ├── power_vs_time.png
    └── control_angles.png
```

**Version control**:
- ✅ Commit: template, scripts, CSV data
- ❌ Exclude: generated inputs (can be regenerated)

## Working Examples

### Example 1: Multi-Cycle Burnup Study

**Scenario**: Generate 13 MCNP inputs representing reactor operating history

**Files**:
- `bench.template` (13,727 lines) - ATR quarter-core with AGR-1 test
- `power.csv` - Power by lobe vs time (616 timesteps)
- `oscc.csv` - Control drum angles vs time
- `neck_shim.csv` - Neck shim insertion states vs time

**Workflow**:
1. Read CSV files → group by cycle (13 cycles)
2. Time-average power, drum angles, shim states per cycle
3. Render template 13 times with cycle-specific data
4. Output: `bench_138B.i`, `bench_139A.i`, ..., `bench_145A.i`

**See**: `example_inputs/agr1_burnup_workflow.py`

### Example 2: Enrichment Sensitivity Study

**Scenario**: Vary fuel enrichment from 3% to 5% in 0.5% increments

**Files**:
- `pwr_assembly.template` - Base PWR assembly
- `enrichment_study.csv` - Enrichment values and case IDs

**Workflow**:
1. Define enrichment values: [3.0, 3.5, 4.0, 4.5, 5.0]
2. For each enrichment, generate material cards with updated U-235 fraction
3. Render template with enrichment-specific materials
4. Output: `pwr_enr30.i`, `pwr_enr35.i`, ..., `pwr_enr50.i`

**See**: `example_inputs/enrichment_study_workflow.py`

### Example 3: Control Rod Worth Curves

**Scenario**: Calculate reactivity vs control rod position (0-100% withdrawn)

**Files**:
- `core_model.template` - Full core model
- `control_rod_positions.csv` - Rod positions (11 cases: 0%, 10%, ..., 100%)

**Workflow**:
1. Define rod positions: 0 to 100% in 10% increments
2. For each position, calculate geometry of control rod cells
3. Render template with position-specific geometry
4. Output: `core_rod_000.i`, `core_rod_010.i`, ..., `core_rod_100.i`

**See**: `example_inputs/control_rod_study_workflow.py`

## Common Pitfalls and Fixes

### Pitfall 1: Leftover Template Variables

**Error**: Generated input contains `{{variable}}` (not replaced)

**Cause**: Variable name mismatch between template and rendering script

**Fix**:
```python
# Check for leftover placeholders
if '{{' in output or '}}' in output:
    raise ValueError(f"Template variables not fully replaced in {filename}")
```

### Pitfall 2: Wrong Time Averaging

**Error**: Averaging over wrong time base

**Fix**: Always use weighted average with duration:
```python
# WRONG: Simple mean (ignores timestep duration)
ave_power = power.mean()

# RIGHT: Time-weighted average
ave_power = (power * time_interval).sum() / time_interval.sum()
```

### Pitfall 3: Inconsistent File Naming

**Error**: Cannot identify which file corresponds to which cycle

**Fix**: Use systematic naming with cycle identifier
```python
# WRONG: Generic numbering
filename = f'input_{i}.i'

# RIGHT: Cycle identifier in name
filename = f'bench_{cycle}.i'  # cycle = '138B', '139A', etc.
```

### Pitfall 4: Missing Data Validation

**Error**: CSV data incomplete, script crashes mid-generation

**Fix**: Validate data before rendering
```python
# Check all cycles present in CSV
cycles_in_data = set(data['Cycle'].unique())
missing = set(expected_cycles) - cycles_in_data
if missing:
    raise ValueError(f"Missing cycles in CSV: {missing}")
```

## Validation Checklist

Before running generated MCNP inputs:

- [ ] Template syntax valid (no `{{...}}` remaining)
- [ ] All CSV data files present and complete
- [ ] Time-weighted averaging applied correctly
- [ ] Generated files have correct naming pattern
- [ ] Visual inspection of key sections (materials, geometry)
- [ ] File sizes reasonable (compare to base input)
- [ ] Cell/surface/material numbering consistent
- [ ] Created QA plots for operational data

## Reference Files

For detailed guidance:
- **template_conversion_guide.md** - How to convert inputs → templates
- **csv_integration_reference.md** - CSV schema design
- **time_averaging_algorithms.md** - Averaging methods
- **jinja2_reference.md** - Jinja2 syntax for MCNP
- **workflow_patterns.md** - Complete workflow examples

## Tools and Scripts

### analyze_input.py

Analyze existing MCNP input to identify parameterizable sections:
```bash
python scripts/analyze_input.py base_input.i
```

**Output**: Report of candidate template variables

### create_template.py

Convert MCNP input to Jinja2 template:
```bash
python scripts/create_template.py base_input.i --output base.template --variables oscc_surfaces,ne_cells
```

### design_csv_schema.py

Generate CSV template for data collection:
```bash
python scripts/design_csv_schema.py --cycles 13 --parameters power,oscc_angle,shim_state --output data_template.csv
```

### render_template.py

Render template with data:
```bash
python scripts/render_template.py base.template --data cycle_data.csv --output-dir mcnp/
```

### time_averaging.py

Utilities for time-weighted averaging:
```python
from scripts.time_averaging import time_weighted_average, snap_to_discrete, round_binary

ave_power = time_weighted_average(power_values, time_intervals)
closest_angle = snap_to_discrete(ave_angle, predefined_angles)
shim_state = round_binary(ave_insertion)
```

## Integration with Other Skills

**Works with**:
- **mcnp-input-builder**: Create initial base input → convert to template
- **mcnp-lattice-builder**: Generate lattice fill arrays programmatically → insert in template
- **mcnp-material-builder**: Generate material cards for parameter studies
- **mcnp-input-validator**: Validate all generated inputs before MCNP execution
- **mcnp-burnup-builder**: Create depletion sequences from multi-cycle inputs

## Best Practices

### 1. Keep Template Minimal

**Principle**: Only parameterize what actually varies

```
✅ Good: 3-6 template variables (cycle-dependent parameters)
❌ Bad: 50+ template variables (overly complex)
```

### 2. Separate Concerns

**Principle**: Template = structure, CSV = data, Python = logic

```
Template: Fixed geometry + placeholders
CSV: Operational parameters (power, angles, states)
Python: Time averaging, geometry generation, rendering
```

### 3. Validate Early and Often

**Principle**: Catch errors before expensive MCNP runs

```python
# After reading CSV
validate_data_completeness(data, expected_cycles)

# After rendering
check_template_variables(output)
validate_mcnp_syntax(output)

# Before MCNP execution
plot_qa_diagnostics(data)
```

### 4. Document Data Sources

**Principle**: Ensure reproducibility

```python
# Add metadata to generated inputs
header = f"""c Generated by {script_name} on {datetime.now()}
c Data sources: {', '.join(csv_files)}
c Cycle: {cycle}
c Average power: {ave_power:.4f} MW
c Control drum angle: {drum_angle}°
"""
```

### 5. Version Control Strategy

**Principle**: Track sources, not generated files

```gitignore
# Commit these
*.template
*.csv
generation_script.py

# Exclude these
mcnp/*.i
plots/*.png
```

## Common Use Cases

### Use Case 1: Multi-Cycle Reactor Burnup

**Challenge**: Model 13 reactor operating cycles with different control positions

**Solution**:
- Template: Fixed core geometry + {{control_positions}}
- CSV: Power, control drum angles, shim states vs time
- Workflow: Time-average each cycle → generate 13 static inputs

**Benefit**: 1 template + CSV → 13 MCNP inputs in seconds

### Use Case 2: Material Property Sensitivity

**Challenge**: Study impact of fuel density variation (±5%)

**Solution**:
- Template: Fixed geometry + {{fuel_density}}
- CSV: Density values (-5%, -2.5%, 0%, +2.5%, +5%)
- Workflow: Generate material cards with varying density

**Benefit**: Systematic exploration of uncertainty

### Use Case 3: Geometry Configuration Management

**Challenge**: Model reactor with 5 different test assemblies in flux trap

**Solution**:
- Template: Core + {{test_assembly_cells}}
- Python: Generate test assembly geometry variants
- Workflow: Render 5 inputs with different assemblies

**Benefit**: Consistent core, variable test section

## Troubleshooting

### Problem: Template renders but MCNP fails

**Check**:
1. Are cell/surface/material numbers unique?
2. Are all surfaces referenced in cells defined?
3. Are all materials referenced in cells defined?
4. Run with `print` card to see full geometry

### Problem: Time averaging gives unrealistic values

**Check**:
1. Are time intervals in correct units (hrs, days)?
2. Is sum of time intervals correct?
3. Plot averaged values vs time to visualize

### Problem: Generated files have wrong parameters

**Check**:
1. CSV data loaded correctly (check Pandas dtypes)
2. Cycle identifier matching correctly
3. Variable names in template match rendering script

## Additional Resources

**External references**:
- Jinja2 documentation: https://jinja.palletsprojects.com/
- Pandas CSV parsing: https://pandas.pydata.org/docs/user_guide/io.html#csv-text-files
- MCNP input syntax: LA-UR-17-29981 (MCNP6.2 manual)

**Related skills**:
- mcnp-input-builder (create base inputs)
- mcnp-burnup-builder (depletion sequences)
- mcnp-cycle-manager (workflow orchestration - future skill)
