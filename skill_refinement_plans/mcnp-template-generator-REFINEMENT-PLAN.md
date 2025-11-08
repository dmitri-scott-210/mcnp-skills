# MCNP-TEMPLATE-GENERATOR SKILL REFINEMENT PLAN
## NEW SKILL - Jinja2 Template-Based Input Generation

**Created**: November 8, 2025
**Status**: NEW SKILL - Complete implementation required
**Priority**: 🔴 **CRITICAL** - Enables automated multi-cycle reactor modeling
**Based On**: AGR-1 template analysis (13-cycle HTGR burnup study)

---

## EXECUTIVE SUMMARY

This plan details the creation of a NEW skill: **mcnp-template-generator**, which enables users to:

1. **Convert existing MCNP inputs** into parameterized Jinja2 templates
2. **Identify variable sections** (control positions, materials, geometry variants)
3. **Integrate CSV data files** for time-varying operational parameters
4. **Apply time-weighted averaging** to collapse operational history into static configurations
5. **Generate multiple MCNP inputs** from a single template + data workflow

**Key Achievement**: 1 template + CSV data → 13 cycle-specific MCNP inputs (as demonstrated in AGR-1 analysis)

---

## SKILL PURPOSE AND SCOPE

### What This Skill Does

**mcnp-template-generator** automates the creation of multiple related MCNP input files from a single master template. This is essential for:

- **Multi-cycle burnup calculations** (reactor operating history over 13+ cycles)
- **Parameter sensitivity studies** (varying enrichment, geometry, materials)
- **Configuration management** (different control rod positions, temperatures, compositions)
- **Benchmark series** (same geometry, different operational states)
- **Design optimization** (systematic variation of design parameters)

### What This Skill Does NOT Do

- **Real-time coupling** (this is for static MCNP inputs, not dynamic coupling)
- **Automated MCNP execution** (generates inputs, user runs MCNP separately)
- **Results processing** (focus is input generation, not output analysis)

### Key Capabilities

1. **Template Conversion**: Analyze existing MCNP input → identify parameterizable sections → generate Jinja2 template
2. **CSV Integration**: Design data file schemas → parse operational history → apply to templates
3. **Time Averaging**: Collapse time-varying parameters (power, control positions) into representative values
4. **Batch Generation**: Render template for multiple cycles/scenarios → write organized output files
5. **Validation**: Pre-check generated inputs for completeness and consistency

---

## ANALYSIS FINDINGS (FROM REQUIRED READING)

### AGR-1 Template Example (Key Patterns)

**Template Structure** (bench.template, 13,727 lines):
```
Fixed Content (ATR quarter-core):
  - 10 fuel elements (210 cells)
  - Beryllium reflector
  - Water regions
  - Structural components

Parameterized Sections (6 placeholders):
  Line 621:  {{ne_cells}}        ← NE neck shim cells (cycle-dependent)
  Line 674:  {{se_cells}}        ← SE neck shim cells (cycle-dependent)
  Line 1430: {{cells}}           ← AGR-1 test assembly (static)
  Line 1782: {{oscc_surfaces}}   ← Control drum positions (cycle-dependent)
  Line 2214: {{surfaces}}        ← AGR-1 surfaces (static)
  Line 13603: {{materials}}      ← AGR-1 materials (static)
```

**Result**: 1 template → 13 cycle-specific inputs (bench_138B.i through bench_145A.i)

### Data-Driven Workflow

**CSV Files Drive Parameterization**:
1. **power.csv** (616 timesteps × 10 columns):
   - Cycle, Timestep, Time Interval, Lobe Powers
   - Used for: Time-averaged power per cycle → MOAA burnup input

2. **oscc.csv** (616 timesteps × 8 columns):
   - Control drum angles (0-150°) vs time
   - Used for: Time-averaged angle → select predefined surface definition

3. **neck_shim.csv** (616 timesteps × 28 columns):
   - Binary insertion states (0=water, 1=hafnium) vs time
   - Used for: Time-averaged state → round to 0 or 1 → material selection

### Time-Weighted Averaging Algorithm

**Critical Pattern** (handles variable timestep durations):
```python
# Weighted average over cycle duration
ave_value = (value × time_interval).sum() / total_time

# For continuous parameters (drum angles):
ave_angle = (angle × time_interval).sum() / cum_time[-1]
closest = find_closest_value(predefined_angles, ave_angle)

# For binary parameters (shim insertion):
ave_insertion = (insertion × time_interval).sum() / cum_time[-1]
condition = int(np.rint(ave_insertion))  # Round to 0 or 1
```

**Purpose**: Collapse 616 fine-grained timesteps into 13 static configurations

---

## SKILL DIRECTORY STRUCTURE

```
.claude/skills/mcnp-template-generator/
├── SKILL.md                                # Main skill definition
├── template_conversion_guide.md            # How to convert inputs → templates
├── csv_integration_reference.md            # CSV data file design
├── time_averaging_algorithms.md            # Averaging methods
├── jinja2_reference.md                     # Jinja2 syntax for MCNP
├── workflow_patterns.md                    # Complete workflows
├── scripts/
│   ├── analyze_input.py                    # Identify parameterizable sections
│   ├── create_template.py                  # Generate template from input
│   ├── design_csv_schema.py                # Create CSV data file template
│   ├── render_template.py                  # Apply data to template
│   ├── time_averaging.py                   # Time-weighted averaging utilities
│   └── batch_generator.py                  # Generate multiple inputs
├── example_inputs/
│   ├── base_model.i                        # Example base MCNP input
│   ├── base_model.template                 # Generated Jinja2 template
│   ├── cycle_data.csv                      # Example operational data
│   ├── generated_cycle_001.i               # Example rendered output
│   └── generation_script.py                # Complete workflow example
└── tests/
    ├── test_template_conversion.py         # Validation tests
    └── test_data_integration.py            # CSV parsing tests
```

---

## SKILL.md CONTENT (COMPLETE)

```markdown
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
```

---

## TOOL IMPLEMENTATIONS

### 1. analyze_input.py

**File**: `.claude/skills/mcnp-template-generator/scripts/analyze_input.py`

```python
"""
MCNP Input Analyzer for Template Conversion
Identifies sections suitable for parameterization
"""

import re
import argparse
from collections import defaultdict


def analyze_mcnp_input(filename):
    """
    Analyze MCNP input to identify candidate template variables.

    Args:
        filename: Path to MCNP input file

    Returns:
        dict with analysis results
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Identify block boundaries
    blocks = identify_blocks(lines)

    # Analyze each block
    cell_analysis = analyze_cells(lines, blocks['cells'])
    surface_analysis = analyze_surfaces(lines, blocks['surfaces'])
    data_analysis = analyze_data(lines, blocks['data'])

    # Identify repeated patterns
    patterns = find_repeated_patterns(lines)

    # Generate recommendations
    recommendations = generate_recommendations(
        cell_analysis, surface_analysis, data_analysis, patterns
    )

    return {
        'blocks': blocks,
        'cell_analysis': cell_analysis,
        'surface_analysis': surface_analysis,
        'data_analysis': data_analysis,
        'patterns': patterns,
        'recommendations': recommendations
    }


def identify_blocks(lines):
    """Identify cell, surface, and data block boundaries."""
    blocks = {'cells': [], 'surfaces': [], 'data': []}

    current_block = 'cells'
    blank_count = 0

    for i, line in enumerate(lines):
        # Detect block transitions (blank line)
        if line.strip() == '':
            blank_count += 1
            if blank_count == 1 and current_block == 'cells':
                current_block = 'surfaces'
            elif blank_count == 2 and current_block == 'surfaces':
                current_block = 'data'
        else:
            blank_count = 0

        blocks[current_block].append(i)

    return blocks


def analyze_cells(lines, cell_indices):
    """Analyze cell block for parameterization candidates."""
    cells = []

    for i in cell_indices:
        line = lines[i].strip()
        if not line or line.startswith('c'):
            continue

        # Parse cell card
        parts = line.split()
        if len(parts) < 3:
            continue

        cell_num = parts[0]
        mat_num = parts[1]
        density = parts[2] if parts[1] != '0' else None

        cells.append({
            'line': i,
            'cell_num': cell_num,
            'mat_num': mat_num,
            'density': density,
            'universe': extract_universe(line)
        })

    # Identify patterns
    universe_groups = defaultdict(list)
    for cell in cells:
        if cell['universe']:
            universe_groups[cell['universe']].append(cell)

    return {
        'total_cells': len(cells),
        'universe_groups': dict(universe_groups),
        'material_variants': count_material_variants(cells)
    }


def analyze_surfaces(lines, surface_indices):
    """Analyze surface block for parameterization candidates."""
    surfaces = []

    for i in surface_indices:
        line = lines[i].strip()
        if not line or line.startswith('c'):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        surf_num = parts[0]
        surf_type = parts[1]

        surfaces.append({
            'line': i,
            'surf_num': surf_num,
            'surf_type': surf_type
        })

    return {
        'total_surfaces': len(surfaces),
        'surface_types': count_surface_types(surfaces)
    }


def analyze_data(lines, data_indices):
    """Analyze data block for parameterization candidates."""
    materials = []
    current_material = None

    for i in data_indices:
        line = lines[i].strip()

        # Material card start
        if line.startswith('m') and not line.startswith('mt'):
            mat_match = re.match(r'm(\d+)', line, re.IGNORECASE)
            if mat_match:
                current_material = {
                    'line': i,
                    'mat_num': mat_match.group(1),
                    'isotopes': []
                }
                materials.append(current_material)

        # Isotope line
        elif current_material and not line.startswith('c'):
            isotope_match = re.findall(r'(\d+\.\d+c)\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', line)
            current_material['isotopes'].extend(isotope_match)

    return {
        'total_materials': len(materials),
        'materials': materials
    }


def find_repeated_patterns(lines):
    """Identify repeated multi-line patterns (candidate for loops/templates)."""
    # Look for repeated cell definitions (similar structure)
    patterns = []

    # Example: Find repeated lattice fill patterns
    fill_pattern = re.compile(r'fill=(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)')

    for i, line in enumerate(lines):
        match = fill_pattern.search(line)
        if match:
            patterns.append({
                'line': i,
                'type': 'fill_array',
                'bounds': match.groups()
            })

    return patterns


def count_material_variants(cells):
    """Count how many different materials are used."""
    materials = set(cell['mat_num'] for cell in cells if cell['mat_num'] != '0')
    return len(materials)


def count_surface_types(surfaces):
    """Count surface types."""
    types = defaultdict(int)
    for surf in surfaces:
        types[surf['surf_type']] += 1
    return dict(types)


def extract_universe(line):
    """Extract universe number from cell card."""
    match = re.search(r'u=(\d+)', line, re.IGNORECASE)
    return match.group(1) if match else None


def generate_recommendations(cell_analysis, surface_analysis, data_analysis, patterns):
    """Generate template variable recommendations."""
    recommendations = []

    # Recommend lattice fill arrays as template variables
    if patterns:
        recommendations.append({
            'type': 'fill_array',
            'variable_name': 'lattice_fills',
            'reason': f'Found {len(patterns)} lattice fill arrays',
            'benefit': 'Can vary lattice contents programmatically'
        })

    # Recommend universe groups as template variables
    if len(cell_analysis['universe_groups']) > 5:
        recommendations.append({
            'type': 'universe_cells',
            'variable_name': 'assembly_cells',
            'reason': f'Found {len(cell_analysis["universe_groups"])} universe groups',
            'benefit': 'Can swap assembly types easily'
        })

    # Recommend material variations
    if cell_analysis['material_variants'] > 20:
        recommendations.append({
            'type': 'materials',
            'variable_name': 'fuel_materials',
            'reason': f'Found {cell_analysis["material_variants"]} material definitions',
            'benefit': 'Can vary compositions for burnup or enrichment studies'
        })

    return recommendations


def print_report(analysis):
    """Print analysis report."""
    print("=" * 70)
    print("MCNP INPUT ANALYSIS FOR TEMPLATE CONVERSION")
    print("=" * 70)

    print(f"\n📊 BLOCK STRUCTURE")
    print(f"  Cell block:    lines 1-{len(analysis['blocks']['cells'])}")
    print(f"  Surface block: lines {len(analysis['blocks']['cells'])+1}-"
          f"{len(analysis['blocks']['cells'])+len(analysis['blocks']['surfaces'])}")
    print(f"  Data block:    lines {len(analysis['blocks']['cells'])+len(analysis['blocks']['surfaces'])+1}-end")

    print(f"\n📐 CELL ANALYSIS")
    print(f"  Total cells: {analysis['cell_analysis']['total_cells']}")
    print(f"  Universe groups: {len(analysis['cell_analysis']['universe_groups'])}")
    print(f"  Material variants: {analysis['cell_analysis']['material_variants']}")

    print(f"\n🔷 SURFACE ANALYSIS")
    print(f"  Total surfaces: {analysis['surface_analysis']['total_surfaces']}")
    print(f"  Surface types:")
    for surf_type, count in analysis['surface_analysis']['surface_types'].items():
        print(f"    {surf_type}: {count}")

    print(f"\n⚛️  DATA ANALYSIS")
    print(f"  Total materials: {analysis['data_analysis']['total_materials']}")

    print(f"\n🔁 REPEATED PATTERNS")
    print(f"  Lattice fill arrays: {len(analysis['patterns'])}")

    print(f"\n💡 RECOMMENDATIONS FOR TEMPLATE VARIABLES")
    if analysis['recommendations']:
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"\n  {i}. Template Variable: {{{{ {rec['variable_name']} }}}}")
            print(f"     Type: {rec['type']}")
            print(f"     Reason: {rec['reason']}")
            print(f"     Benefit: {rec['benefit']}")
    else:
        print("  No strong candidates found. Input may be too simple for templating.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analyze MCNP input for template conversion'
    )
    parser.add_argument('input_file', help='MCNP input file to analyze')
    args = parser.parse_args()

    analysis = analyze_mcnp_input(args.input_file)
    print_report(analysis)
```

### 2. time_averaging.py

**File**: `.claude/skills/mcnp-template-generator/scripts/time_averaging.py`

```python
"""
Time-Weighted Averaging Utilities
For collapsing operational history into representative configurations
"""

import numpy as np


def time_weighted_average(values, time_intervals):
    """
    Calculate time-weighted average.

    Args:
        values: Array of parameter values at each timestep
        time_intervals: Array of time duration for each timestep (same length as values)

    Returns:
        Time-weighted average value

    Example:
        >>> power = np.array([23.5, 24.1, 23.8])
        >>> time = np.array([24.0, 18.5, 30.0])  # hours
        >>> time_weighted_average(power, time)
        23.79... MW
    """
    if len(values) != len(time_intervals):
        raise ValueError("Values and time_intervals must have same length")

    if np.sum(time_intervals) == 0:
        raise ValueError("Total time interval is zero")

    return np.sum(values * time_intervals) / np.sum(time_intervals)


def snap_to_discrete(value, discrete_values):
    """
    Snap continuous value to nearest discrete option.

    Useful for control drum angles, rod positions with predefined detents.

    Args:
        value: Continuous value (e.g., 82.3 degrees)
        discrete_values: List of allowed values (e.g., [0, 25, 40, 50, ...])

    Returns:
        Nearest discrete value

    Example:
        >>> angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100]
        >>> snap_to_discrete(82.3, angles)
        80
    """
    discrete_array = np.array(discrete_values)
    differences = np.abs(discrete_array - value)
    idx = np.argmin(differences)
    return discrete_values[idx]


def round_binary(value):
    """
    Round to binary state (0 or 1).

    Useful for control rod insertion states after time-averaging.

    Args:
        value: Continuous value between 0 and 1 (e.g., 0.73 = mostly inserted)

    Returns:
        0 or 1

    Example:
        >>> round_binary(0.23)  # Mostly withdrawn
        0
        >>> round_binary(0.78)  # Mostly inserted
        1
    """
    return int(np.rint(value))


def cycle_average(data, cycle_column, time_column, value_column):
    """
    Calculate time-weighted average for each cycle in a DataFrame.

    Args:
        data: Pandas DataFrame
        cycle_column: Name of cycle identifier column
        time_column: Name of time interval column
        value_column: Name of value column to average

    Returns:
        Dict mapping cycle -> average value

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'Cycle': ['138B', '138B', '139A', '139A'],
        ...     'Time_hrs': [24, 20, 18, 22],
        ...     'Power_MW': [23.5, 24.1, 24.3, 24.0]
        ... })
        >>> cycle_average(df, 'Cycle', 'Time_hrs', 'Power_MW')
        {'138B': 23.77..., '139A': 24.14...}
    """
    averages = {}

    for cycle in data[cycle_column].unique():
        cycle_data = data[data[cycle_column] == cycle]
        values = cycle_data[value_column].values
        times = cycle_data[time_column].values

        averages[cycle] = time_weighted_average(values, times)

    return averages


def validate_time_data(time_intervals):
    """
    Validate time interval data.

    Checks:
    - All positive
    - No NaN/Inf
    - Total > 0

    Args:
        time_intervals: Array of time durations

    Raises:
        ValueError: If validation fails
    """
    if np.any(time_intervals < 0):
        raise ValueError("Time intervals must be positive")

    if np.any(np.isnan(time_intervals)) or np.any(np.isinf(time_intervals)):
        raise ValueError("Time intervals contain NaN or Inf")

    if np.sum(time_intervals) == 0:
        raise ValueError("Total time is zero")


# Example usage and tests
if __name__ == "__main__":
    print("=" * 60)
    print("Time-Weighted Averaging Utilities - Examples")
    print("=" * 60)

    # Example 1: Simple time-weighted average
    print("\nExample 1: Time-Weighted Average")
    power = np.array([23.5, 24.1, 23.8, 24.0])
    time = np.array([24.0, 18.5, 30.0, 20.0])  # hours
    ave = time_weighted_average(power, time)
    print(f"  Power values: {power}")
    print(f"  Time intervals: {time} hrs")
    print(f"  Time-weighted average: {ave:.2f} MW")
    print(f"  (Compare to simple mean: {power.mean():.2f} MW)")

    # Example 2: Snap to discrete values
    print("\nExample 2: Snap to Discrete Values")
    angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
    continuous_angle = 82.3
    closest = snap_to_discrete(continuous_angle, angles)
    print(f"  Continuous angle: {continuous_angle}°")
    print(f"  Discrete options: {angles}")
    print(f"  Closest discrete: {closest}°")

    # Example 3: Round binary
    print("\nExample 3: Round Binary State")
    insertion_states = np.array([1, 1, 0, 1, 1, 0])  # Binary: in/out
    time_intervals = np.array([10, 15, 5, 20, 18, 12])  # hours
    ave_insertion = time_weighted_average(insertion_states, time_intervals)
    representative_state = round_binary(ave_insertion)
    print(f"  States over time: {insertion_states}")
    print(f"  Time intervals: {time_intervals} hrs")
    print(f"  Time-weighted average: {ave_insertion:.2f}")
    print(f"  Representative state: {representative_state} ({'inserted' if representative_state else 'withdrawn'})")

    # Example 4: Cycle averaging
    print("\nExample 4: Cycle Averaging from DataFrame")
    import pandas as pd
    df = pd.DataFrame({
        'Cycle': ['138B', '138B', '138B', '139A', '139A', '139A'],
        'Timestep': [1, 2, 3, 1, 2, 3],
        'Time_hrs': [24, 20, 18, 22, 25, 19],
        'Power_MW': [23.5, 24.1, 23.8, 24.3, 24.0, 24.2]
    })
    print("  Input DataFrame:")
    print(df.to_string(index=False))

    averages = cycle_average(df, 'Cycle', 'Time_hrs', 'Power_MW')
    print("\n  Cycle-averaged power:")
    for cycle, ave_power in averages.items():
        print(f"    {cycle}: {ave_power:.2f} MW")

    print("\n" + "=" * 60)
```

---

## REFERENCE FILE: template_conversion_guide.md

**File**: `.claude/skills/mcnp-template-generator/template_conversion_guide.md`

```markdown
# Template Conversion Guide
## Converting Existing MCNP Inputs to Jinja2 Templates

This guide details the process of converting an existing MCNP input file into a parameterized Jinja2 template.

## Step 1: Identify Fixed vs. Variable Content

**Fixed content** (stays the same across all scenarios):
- Core reactor geometry (if constant)
- Structural materials (if constant)
- Most physics cards (MODE, KCODE, etc.)
- Source definition (if constant)

**Variable content** (changes between scenarios):
- Control rod/drum positions
- Material compositions (enrichment, burnup state)
- Test assembly configurations
- Operational parameters (power, temperature)

## Step 2: Mark Template Boundaries

**Choose strategic insertion points** for template variables:

**Good insertion points**:
- Between major comment blocks
- At start of repeated geometry sections
- Before/after material definitions

**Bad insertion points**:
- Middle of cell definition
- Inside surface definitions
- Breaking MCNP syntax

## Step 3: Replace Variable Sections

### Example: Control Drum Surfaces

**Original MCNP input**:
```mcnp
c   ---------------------------------------------------------------------------
c      CONTROL DRUM POSITION SURFACES
c   ---------------------------------------------------------------------------
c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
c
```

**Template version**:
```jinja2
c   ---------------------------------------------------------------------------
c      CONTROL DRUM POSITION SURFACES
c   ---------------------------------------------------------------------------
{{oscc_surfaces}}
```

**Rendering script generates**:
```python
oscc_surfaces[cycle] = """c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
c
"""
```

### Example: Material Definitions

**Original**:
```mcnp
m1  $ UO2 fuel, 4.5% enriched
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
```

**Template**:
```jinja2
{{fuel_material}}
```

**Rendering**:
```python
# For enrichment study
enrichments = [3.0, 3.5, 4.0, 4.5, 5.0]
for enr in enrichments:
    fuel_material = f"""m1  $ UO2 fuel, {enr}% enriched
   92235.70c  {enr/100:.6f}
   92238.70c  {1-enr/100:.6f}
    8016.70c  2.0
"""
    template.render(fuel_material=fuel_material)
```

## Step 4: Validate Template

**Checks**:
1. Template is valid MCNP input (can run standalone with placeholders as comments)
2. Placeholder names are descriptive ({{oscc_surfaces}} not {{var1}})
3. Minimal number of placeholders (3-6 typical, >10 is complex)
4. All placeholders documented

## Step 5: Test Rendering

**Minimal test**:
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('test.template')

# Test with dummy data
output = template.render(
    oscc_surfaces="c\n  981 c/z 0 0 1\n",
    ne_cells="c\n  701 10 -1.0 -701\n"
)

print(output)

# Check for leftover placeholders
assert '{{' not in output, "Template variables not fully replaced"
```

## Complete Workflow Example

See `example_inputs/conversion_workflow_example.py`
```

---

## EXAMPLE WORKFLOW: agr1_burnup_workflow.py

**File**: `.claude/skills/mcnp-template-generator/example_inputs/agr1_burnup_workflow.py`

```python
"""
Complete AGR-1 Multi-Cycle Burnup Workflow Example
Demonstrates template-based generation of 13 cycle-specific MCNP inputs
"""

import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import os


# Define cycles
cycles = [
    '138B', '139A', '139B', '140A', '140B', '141A',
    '142A', '142B', '143A', '143B', '144A', '144B', '145A'
]

# Predefined control drum angles (discrete options)
angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]

# Neck shim materials (0=water withdrawn, 1=hafnium inserted)
neck_materials = {
    0: (10, 1.00276E-1),   # Material 10, density
    1: (71, 4.55926E-2),   # Material 71, density
}


def find_closest_value(options, target):
    """Find closest discrete value."""
    differences = np.abs(np.array(options) - target)
    return options[np.argmin(differences)]


def time_weighted_average(values, time_intervals):
    """Calculate time-weighted average."""
    return (values * time_intervals).sum() / time_intervals.sum()


def load_and_process_data():
    """Load CSV files and process by cycle."""

    # Read CSV files
    power_df = pd.read_csv('power.csv', index_col="Cumulative Timestep")
    oscc_df = pd.read_csv('oscc.csv', index_col="Cumulative Timestep")
    neck_df = pd.read_csv('neck_shim.csv', index_col="Cumulative Timestep")

    # Group by cycle
    cycles_list = power_df['Cycle'].to_list()
    time_interval = power_df["Time Interval(hrs)"].to_numpy()

    # Organize data by cycle
    data_by_cycle = {}
    prev = 0

    for cycle in cycles:
        time_steps = cycles_list.count(cycle)
        time_intervals = time_interval[prev:prev+time_steps]

        # Power data
        ne_power = power_df['NELobePower(MW)'].iloc[prev:prev+time_steps].values
        c_power = power_df['CLobePower(MW)'].iloc[prev:prev+time_steps].values
        se_power = power_df['SELobePower(MW)'].iloc[prev:prev+time_steps].values

        ave_power = ((ne_power + c_power + se_power) / 3 * time_intervals).sum() / time_intervals.sum()

        # OSCC data
        ne_oscc = oscc_df['NEOSCC(degrees)'].iloc[prev:prev+time_steps].values
        se_oscc = oscc_df['SEOSCC(degrees)'].iloc[prev:prev+time_steps].values

        ave_ne_angle = time_weighted_average(ne_oscc, time_intervals)
        ave_se_angle = time_weighted_average(se_oscc, time_intervals)

        closest_ne = find_closest_value(angles, ave_ne_angle)
        closest_se = find_closest_value(angles, ave_se_angle)

        # Neck shim data (6 rods each in NE and SE)
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

        data_by_cycle[cycle] = {
            'power': ave_power,
            'ne_angle': closest_ne,
            'se_angle': closest_se,
            'ne_shims': ne_shims,
            'se_shims': se_shims,
            'time_days': time_intervals.sum() / 24
        }

        prev += time_steps

    return data_by_cycle


def generate_oscc_surfaces(ne_angle, se_angle):
    """Generate control drum surface definitions."""

    # Hardcoded surface positions for each angle (from precomputed geometry)
    drum_surfaces = {
        'ne': {
            85: """c
  981   c/z   48.0375  -18.1425  9.195       $ DRUM E1 AT 85 DEGREES
  982   c/z   31.5218  -27.3612  9.195       $ DRUM E2 AT 85 DEGREES
c """,
            # ... other angles
        },
        'se': {
            85: """c
  983   c/z   27.3612  -31.5218  9.195       $ DRUM E3 AT 85 DEGREES
  984   c/z   18.1425  -48.0375  9.195       $ DRUM E4 AT 85 DEGREES
c """,
            # ... other angles
        }
    }

    return drum_surfaces['ne'].get(ne_angle, "") + drum_surfaces['se'].get(se_angle, "")


def generate_neck_shim_cells(shims, quadrant):
    """Generate neck shim cell definitions."""

    # Cell numbering: NE starts at 702, SE starts at 792
    cell_start = 702 if quadrant == 'NE' else 792
    surf_start = 701 if quadrant == 'NE' else 791

    cells = "c\n"
    for i, (rod_name, state) in enumerate(shims.items(), start=1):
        mat, density = neck_materials[state]
        state_str = "inserted" if state == 1 else "withdrawn"

        cells += f"""  {cell_start + (i-1)*5}   {mat} {density:.5e}    {surf_start + (i-1)*5} -{surf_start + (i-1)*5 + 1}  100  -200        $ {rod_name} Hf neck shim - {state_str}
                                    -30    10        $ East Quadrant
c
"""

    return cells


def generate_inputs():
    """Main workflow: generate all 13 cycle inputs."""

    # Load and process data
    print("Loading CSV data...")
    data = load_and_process_data()

    # Create output directory
    if not os.path.exists('mcnp'):
        os.mkdir('mcnp')

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('bench.template')

    # Generate inputs for each cycle
    for cycle in cycles:
        print(f"Generating {cycle}...")

        cycle_data = data[cycle]

        # Generate cycle-specific content
        oscc_surfaces = generate_oscc_surfaces(
            cycle_data['ne_angle'],
            cycle_data['se_angle']
        )

        ne_cells = generate_neck_shim_cells(cycle_data['ne_shims'], 'NE')
        se_cells = generate_neck_shim_cells(cycle_data['se_shims'], 'SE')

        # Render template
        output = template.render(
            oscc_surfaces=oscc_surfaces,
            ne_cells=ne_cells,
            se_cells=se_cells,
            # cells, surfaces, materials are static (same for all cycles)
            cells=static_agr1_cells,
            surfaces=static_agr1_surfaces,
            materials=static_agr1_materials
        )

        # Write output
        filename = f'mcnp/bench_{cycle}.i'
        with open(filename, 'w') as f:
            f.write(output)

        print(f"  → {filename} ({len(output)} bytes)")
        print(f"     Power: {cycle_data['power']:.2f} MW")
        print(f"     NE angle: {cycle_data['ne_angle']}°")
        print(f"     SE angle: {cycle_data['se_angle']}°")

    print(f"\n✓ Generated {len(cycles)} MCNP inputs in mcnp/")


# Static geometry content (same for all cycles)
static_agr1_cells = """c AGR-1 test assembly cells
[... hardcoded AGR-1 geometry ...]
"""

static_agr1_surfaces = """c AGR-1 surfaces
[... hardcoded surfaces ...]
"""

static_agr1_materials = """c AGR-1 materials
[... hardcoded materials ...]
"""


if __name__ == "__main__":
    print("=" * 70)
    print("AGR-1 Multi-Cycle Input Generation")
    print("=" * 70)
    generate_inputs()
```

---

## TESTING AND VALIDATION

### Test 1: Template Conversion

**User Query**: "Convert this MCNP input to a template for varying control rod positions"

**Expected Skill Response**:
1. ✅ Analyze input using `analyze_input.py`
2. ✅ Identify control rod cells as variable section
3. ✅ Generate template with {{control_rod_cells}} placeholder
4. ✅ Create CSV schema for rod positions
5. ✅ Provide rendering script example

### Test 2: Multi-Cycle Burnup

**User Query**: "Generate 10 MCNP inputs for reactor operating history with different power levels"

**Expected Skill Response**:
1. ✅ Request operational data (power vs time CSV)
2. ✅ Guide CSV schema design (Cycle, Timestep, Time_Interval, Power)
3. ✅ Explain time-weighted averaging
4. ✅ Provide complete workflow script
5. ✅ Show validation steps (plots, file size checks)

### Test 3: Enrichment Study

**User Query**: "Create inputs for enrichment sensitivity study (3% to 5%)"

**Expected Skill Response**:
1. ✅ Identify fuel material cards as variable
2. ✅ Generate {{fuel_material}} template
3. ✅ Provide loop for enrichment values
4. ✅ Show material card generation
5. ✅ Systematic file naming (pwr_enr30.i, pwr_enr35.i, etc.)

---

## SUCCESS CRITERIA

**Skill is successful when users can**:
1. ✅ Convert existing MCNP input to Jinja2 template
2. ✅ Design CSV data file schemas
3. ✅ Apply time-weighted averaging correctly
4. ✅ Render templates with cycle/scenario-specific data
5. ✅ Generate multiple inputs systematically
6. ✅ Validate generated inputs before MCNP execution

**Integration success**:
- ✅ Works with mcnp-input-builder (create base inputs)
- ✅ Works with mcnp-input-validator (validate generated inputs)
- ✅ Works with mcnp-burnup-builder (multi-cycle depletion)

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Core Skill (Session 1)
- [ ] Create `.claude/skills/mcnp-template-generator/` directory
- [ ] Write SKILL.md (complete content above)
- [ ] Create template_conversion_guide.md
- [ ] Create csv_integration_reference.md
- [ ] Create time_averaging_algorithms.md
- [ ] Create jinja2_reference.md
- [ ] Create workflow_patterns.md

### Phase 2: Tools (Session 1)
- [ ] Implement scripts/analyze_input.py
- [ ] Implement scripts/create_template.py
- [ ] Implement scripts/design_csv_schema.py
- [ ] Implement scripts/render_template.py
- [ ] Implement scripts/time_averaging.py
- [ ] Implement scripts/batch_generator.py

### Phase 3: Examples (Session 2)
- [ ] Create example_inputs/base_model.i
- [ ] Create example_inputs/base_model.template
- [ ] Create example_inputs/cycle_data.csv
- [ ] Create example_inputs/agr1_burnup_workflow.py
- [ ] Create example_inputs/enrichment_study_workflow.py
- [ ] Create example_inputs/control_rod_study_workflow.py

### Phase 4: Testing (Session 2)
- [ ] Test template conversion workflow
- [ ] Test multi-cycle generation
- [ ] Test time-averaging algorithms
- [ ] Validate with real AGR-1 data (if available)
- [ ] Test integration with other skills

---

## DEPENDENCIES AND PREREQUISITES

**Required Python packages**:
```
jinja2>=3.1.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0  # For QA plots
```

**User must have**:
- Basic Python knowledge (loops, functions)
- Understanding of MCNP input structure
- Operational data in CSV format (or ability to create it)

**Related skills (must exist)**:
- mcnp-input-builder (create base inputs)
- mcnp-input-validator (validate generated outputs)

---

## MAINTENANCE AND UPDATES

**Future enhancements**:
1. Support for Mako templates (alternative to Jinja2)
2. Graphical template editor
3. Automated CSV generation from experimental logs
4. Integration with MOAA/ORIGEN for burnup workflows
5. Web interface for non-Python users

**Version tracking**:
- Document Jinja2 version compatibility
- Test with MCNP 6.2, 6.3 (input syntax changes)
- Update examples as new reactor types are analyzed

---

## CONCLUSION

This skill enables **automated, reproducible, data-driven MCNP input generation** - a critical capability for modern reactor analysis. The AGR-1 example demonstrates this can reduce 13-cycle input creation from days of manual work to seconds of automated generation.

**Key Innovation**: Separation of concerns
- Template = fixed geometry structure
- CSV = operational parameters (editable by non-programmers)
- Python = logic and averaging (version controlled)

**Ready for immediate implementation.**
