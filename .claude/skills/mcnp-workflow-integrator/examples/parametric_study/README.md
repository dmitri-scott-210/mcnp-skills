# Parametric Study Workflow Example

Template-based parametric study for multi-cycle reactor analysis.

## Overview

This workflow demonstrates automated generation of multiple MCNP inputs from a single template, ideal for:

- Cycle-by-cycle reactor analysis
- Design optimization studies
- Uncertainty quantification
- Parameter sensitivity analysis

**Example**: AGR-1 experiment - 13 reactor cycles with varying power, control positions, and operating conditions.

## Workflow Diagram

```
[External Data (CSV)]
      ↓
[Data Processing (pandas)]
      ↓
[Template Rendering (Jinja2)]
      ↓
[13 MCNP Input Files]
      ↓
[Validation]
      ↓
[Parallel Execution]
      ↓
[Results Aggregation]
      ↓
[Comparison Plots]
```

## Directory Structure

```
parametric_study/
├── README.md                       # This file
├── template.inp                    # Jinja2 template for MCNP input
├── data/
│   ├── cycle_parameters.csv        # Cycle-specific parameters
│   ├── power.csv                   # Power history
│   ├── control_positions.csv       # Control drum angles
│   └── experimental_results.csv    # For validation
├── scripts/
│   ├── create_inputs.py            # Generate all inputs
│   ├── validate_inputs.py          # Pre-run validation
│   ├── run_all_cases.sh            # Execute all cases
│   └── aggregate_results.py        # Combine results
└── run_workflow.sh                 # Complete workflow
```

## Requirements

### Software

- MCNP6.2 or later
- Python 3.8+

### Python Packages

```bash
pip install pandas numpy jinja2 matplotlib
```

## Usage

### Complete Workflow (Automated)

Run entire workflow:

```bash
./run_workflow.sh
```

This will:
1. Generate 13 MCNP inputs from template
2. Validate all inputs
3. Run all cases in parallel
4. Aggregate results
5. Generate comparison plots

**Estimated time**: 6-12 hours (depending on case complexity and parallel resources)

### Step-by-Step Execution

#### Step 1: Generate MCNP Inputs

```bash
python scripts/create_inputs.py
```

**Output**: 13 input files in `inputs/`:
- `inputs/case_138B.i`
- `inputs/case_139A.i`
- `inputs/case_139B.i`
- ... (13 total)

**What it does**:
- Reads `data/cycle_parameters.csv`
- Processes power histories (time-weighted averaging)
- Processes control positions (discrete value selection)
- Renders template for each cycle
- Writes MCNP input files

#### Step 2: Validate Inputs

```bash
python scripts/validate_inputs.py
```

**Checks performed**:
- FILL array dimensions
- Surface/material cross-references
- Numbering conflicts
- Physical constraints (packing fractions, etc.)

**Output**: `validation_report.txt`

If validation fails, fix issues and regenerate (repeat Step 1).

#### Step 3: Run All Cases

**Option A: Local Parallel Execution**

```bash
bash scripts/run_all_cases.sh
```

Runs all 13 cases in parallel (background jobs).

**Option B: HPC Cluster (SLURM)**

```bash
sbatch scripts/submit_array_job.sh
```

Submits SLURM array job for parallel execution on cluster.

**Option C: Run One Case**

For testing:

```bash
mcnp6 i=inputs/case_138B.i n=outputs/case_138B. tasks 8
```

#### Step 4: Aggregate Results

```bash
python scripts/aggregate_results.py
```

**Output**:
- `results/keff_results.csv` - keff for all cycles
- `results/burnup_results.csv` - Burnup data
- `results/comparison_to_experimental.png` - Validation plot
- `results/parametric_analysis.txt` - Summary report

## Template Structure

The template (`template.inp`) contains:

```jinja2
AGR-1 Experiment - Cycle {{ cycle_name }}
c
c Average Power: {{ avg_power_MW }} MW
c Control Angle: {{ oscc_angle }} degrees
c
c ==================== STATIC GEOMETRY ====================
c (Large base geometry - unchanged between cycles)
[... 10,000+ lines of static ATR reactor geometry ...]

c ==================== PARAMETRIC INSERTIONS ====================
c Experiment geometry (generated)
{{ experiment_cells }}

c Control surfaces (cycle-specific)
{{ control_surfaces }}

c Materials (cycle-specific)
{{ materials }}

c ==================== DATA CARDS ====================
kcode 10000 1.0 50 250
ksrc {{ source_x }} {{ source_y }} {{ source_z }}
```

**Variables**:
- `cycle_name`: Cycle identifier (e.g., '138B')
- `avg_power_MW`: Time-weighted average power
- `oscc_angle`: Selected control drum angle
- `experiment_cells`: Generated AGR-1 geometry
- `control_surfaces`: Rotated control surfaces
- `materials`: Cycle-specific materials
- `source_x, source_y, source_z`: Source position

## Data Format

### cycle_parameters.csv

```csv
Cycle,Start_Date,End_Date,Notes
138B,2005-12-01,2006-01-15,Baseline cycle
139A,2006-01-16,2006-03-05,Increased power
139B,2006-03-06,2006-04-20,Control adjustment
...
```

### power.csv

```csv
Cycle,Time_h,Power_MW,Lobe_NE,Lobe_NW,Lobe_SE,Lobe_SW
138B,0.0,110.0,27.5,27.5,27.5,27.5
138B,24.0,115.0,28.75,28.75,28.75,28.75
138B,48.0,112.0,28.0,28.0,28.0,28.0
...
```

### control_positions.csv

```csv
Cycle,Time_h,Angle_deg
138B,0.0,65.0
138B,24.0,67.5
138B,48.0,70.0
...
```

## Key Parameters

### Time-Weighted Averaging

Continuous operational data → discrete MCNP values:

```python
# Power varies: 100 → 110 → 105 MW over 3 days
# MCNP needs single value
ave_power = (100*1 + 110*1 + 105*1) / 3 = 105 MW
```

### Discrete Value Selection

Control angle varies continuously, but MCNP has discrete positions:

```python
# Continuous average: 73.5°
# Allowed angles: [65, 75, 80, 85]
# Selected: 75° (closest)
```

## Validation

### Pre-Run Checks

Automated validation catches:
- FILL array dimension mismatches
- Undefined surface/material references
- Numbering conflicts

### Post-Run Comparison

Compare to experimental data:

```python
# Load calculated and experimental keff
calc = pd.read_csv('results/keff_results.csv')
expt = pd.read_csv('data/experimental_results.csv')

# Plot comparison
plt.errorbar(expt['Cycle'], expt['keff'], yerr=expt['uncertainty'], fmt='o', label='Experimental')
plt.errorbar(calc['Cycle'], calc['keff'], yerr=calc['uncertainty'], fmt='s', label='MCNP')
plt.legend()
```

## Results

Expected outputs:

### Numerical Results

- `results/keff_results.csv`: keff for all 13 cycles
  ```csv
  Cycle,keff,uncertainty,status
  138B,1.0045,0.0008,converged
  139A,1.0052,0.0009,converged
  ...
  ```

### Plots

- `results/keff_vs_cycle.png`: keff evolution
- `results/comparison_to_experimental.png`: Calc vs. experiment
- `results/power_history_all_cycles.png`: Power profiles
- `results/control_positions_all_cycles.png`: Control angles

### Summary Report

`results/parametric_analysis.txt`:

```
Parametric Study Results
========================

Cycles Analyzed: 13
Successfully Converged: 13
Statistical Quality: All rel err < 0.01

keff Range: 0.9980 - 1.0120
Average keff: 1.0045 ± 0.0012

Comparison to Experimental:
  Mean difference: -0.0012
  RMS difference: 0.0035
  All within 3σ: Yes

Power Correlation: r = 0.85
Control Position Correlation: r = -0.62
```

## Customization

### Add New Cycle

1. Add row to `data/cycle_parameters.csv`
2. Add data to `data/power.csv` and `data/control_positions.csv`
3. Re-run `python scripts/create_inputs.py`
4. New input file created automatically

### Change Averaging Method

Edit `scripts/create_inputs.py`:

```python
# Option 1: Time-weighted average (current)
ave_power = time_weighted_average(power, time)

# Option 2: Simple average
ave_power = power.mean()

# Option 3: Peak value
ave_power = power.max()
```

### Modify Template

Edit `template.inp` to:
- Add new geometric features
- Change material definitions
- Modify tally specifications

Then re-run `create_inputs.py` to regenerate all cases.

## Troubleshooting

### Issue: Template Rendering Fails

**Error**: `jinja2.exceptions.UndefinedError: 'variable' is undefined`

**Solution**: Check that all template variables are defined in `create_inputs.py`. Print parameter dictionary before rendering:

```python
print(f"Parameters for {cycle}: {params}")
output = template.render(**params)
```

### Issue: Validation Fails

**Error**: `FILL array dimension mismatch`

**Solution**: Check that generated FILL arrays match lattice specifications. Run validation on single file for detailed error:

```bash
python scripts/validate_inputs.py inputs/case_138B.i
```

### Issue: Some Cases Fail to Converge

**Solution**:
1. Check `outputs/*.o` files for warnings
2. Increase kcode particles: `kcode 50000 1.0 100 500`
3. Check for lost particles (geometry errors)

## Performance Optimization

### Parallel Execution

**Local machine** (4 cores):
```bash
# Run 4 cases at a time
for f in inputs/*.i; do
  mcnp6 i="$f" n="${f%.i}." tasks 2 &
  if (( $(jobs -r | wc -l) >= 4 )); then wait -n; fi
done
wait
```

**HPC cluster** (100 cores):
```bash
# SLURM array job
#SBATCH --array=1-13
#SBATCH --ntasks=8

mcnp6 i=inputs/case_${SLURM_ARRAY_TASK_ID}.i tasks 8
```

### Reduce Case Count

For testing, process only 3 cycles:

```python
# In create_inputs.py
cycles = ['138B', '139A', '139B']  # Instead of all 13
```

## Best Practices

1. **Single Source of Truth**: One template + one script → all inputs
2. **Version Control**: Git commit template and scripts, not generated inputs
3. **Validation Before Execution**: Catch errors early
4. **Automated Comparison**: Compare to experimental data automatically
5. **Documentation**: README explains parameters and workflow

## References

1. **AGR-1 Experiment**: INL/EXT-10-19222
2. **Template-Based Generation**: HTGR Model Best Practices (Zenodo DOI: 10.5281/zenodo.10257801)
3. **Jinja2 Documentation**: https://jinja.palletsprojects.com/

## Contact

For questions about this workflow example, see the main skill documentation at:
`.claude/skills/mcnp-workflow-integrator/SKILL.md`
