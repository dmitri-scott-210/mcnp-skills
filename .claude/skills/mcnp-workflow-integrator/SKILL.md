# mcnp-workflow-integrator

Orchestrate multi-physics workflows, automate data pipelines, and create reproducible reactor analysis calculations involving MCNP and coupled codes.

## WHEN TO USE THIS SKILL

Use this skill when the user needs to:

✅ Set up multi-physics workflows (MCNP + depletion codes)
✅ Automate parametric studies (many similar MCNP cases)
✅ Integrate external data (experimental, operational) into MCNP models
✅ Create burnup-to-dose-rate calculation pipelines
✅ Implement reproducible research workflows
✅ Orchestrate batch calculations on HPC systems
✅ Generate publication-quality results from MCNP outputs

Do NOT use this skill for:
❌ Basic MCNP syntax (see mcnp-input-builder)
❌ Geometry definitions (see mcnp-geometry-builder)
❌ Depletion physics (see mcnp-burnup-builder)
❌ Individual code capabilities - this skill focuses on **INTEGRATION**

## CORE WORKFLOW PATTERNS

### 1. Sequential Multi-Physics Coupling (Burnup-to-Shutdown-Dose-Rate)

**Complete workflow pattern**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 1: NEUTRON TRANSPORT                    │
├─────────────────────────────────────────────────────────────────┤
│ Input:  MCNP neutron transport model (kcode or sdef)           │
│ Output: Cell-wise flux/power distributions                      │
│ Tools:  MCNP6                                                    │
│ Data:   Cell power tallies (F7), flux tallies (F4)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 2: DEPLETION/ACTIVATION TRACKING             │
├─────────────────────────────────────────────────────────────────┤
│ Input:  Flux/power from Phase 1, initial compositions          │
│ Output: Cell-wise isotopic inventories vs. time                │
│ Tools:  MOAA, ORIGEN, CINDER90, or similar                     │
│ Data:   ~150-170 cells tracked individually                     │
│         Isotopic inventory at shutdown time                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         PHASE 3: DECAY SOURCE GENERATION (Cooling Period)       │
├─────────────────────────────────────────────────────────────────┤
│ Input:  Isotopic inventories from Phase 2, decay time          │
│ Output: Photon source spectra by cell                          │
│ Tools:  ORIGEN/CINDER decay calculations                       │
│ Data:   Energy-dependent photon emission rates                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 4: PHOTON TRANSPORT (Dose Rates)             │
├─────────────────────────────────────────────────────────────────┤
│ Input:  MCNP photon transport model with decay sources         │
│ Output: Spatial dose rate maps (Sv/h)                          │
│ Tools:  MCNP6 (mode p)                                          │
│ Data:   FMESH tallies, point detector tallies (F5)             │
│         Dose conversion factors (ICRP-21, ANSI/ANS-6.1.1)      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 5: POST-PROCESSING                      │
├─────────────────────────────────────────────────────────────────┤
│ Tools:  Python (matplotlib, pandas), ParaView, VISIT           │
│ Output: Publication-quality plots, tables, 3D visualizations   │
│ Data:   Comparison to experimental data, regulatory limits     │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features**:
- Sequential coupling (output of stage N → input of stage N+1)
- Cell-level tracking (preserves spatial resolution)
- Time-dependent configurations (power history, cycle-by-cycle)
- Quality checks between stages

**Example**: AGR-1 HTGR experiment - 13 cycles of irradiation → shutdown dose rates

### 2. Parametric Study Automation

**Pattern**: One template/script → Many similar cases

**Use Cases**:
- Cycle-by-cycle reactor analysis (different power, control positions)
- Design optimization (varying geometric parameters)
- Uncertainty quantification (parameter sampling)
- Benchmark suite creation (systematic variations)

**Two Implementation Approaches**:

#### Template-Based (Jinja2)

**When to Use**:
- Large stable base model (e.g., reactor core) with parametric insertions
- Multiple similar cases with different parameters
- Experiment-specific geometry inserted into host reactor

**Example Structure**:
```python
# Jinja2 template with strategic insertion points
template_variables = {
    'cells': programmatically_generated_cells,
    'surfaces': programmatically_generated_surfaces,
    'materials': programmatically_generated_materials,
    'oscc_surfaces': cycle_specific_control_positions,
    'power_MW': average_power
}

rendered_input = template.render(**template_variables)
```

**See**: `template_automation_guide.md` for complete examples

#### Programmatic (Python Functions)

**When to Use**:
- Model built from scratch
- Regular/symmetric geometry patterns (lattices, assemblies)
- Algorithmic complexity needed
- Tight coupling between parameters

**Example Structure**:
```python
# Modular function-based generation
def fuel_assembly(layer, assembly_number):
    surfaces = generate_surfaces(layer, assembly_number)
    cells = generate_cells(layer, assembly_number)
    materials = generate_materials(layer, assembly_number)
    return cells, surfaces, materials

# Build entire model programmatically
for layer in layers:
    for assembly in assemblies[layer]:
        c, s, m = fuel_assembly(layer, assembly)
        accumulate(c, s, m)
```

**See**: `programmatic_generation_guide.md` for complete examples

### 3. Data Integration Pipeline

**Pattern**: External Data → Processing → MCNP → Results

**Data Flow**:
```
CSV/Excel Files (Experimental/Operational Data)
    ↓
Python Processing (pandas, numpy)
    ↓
MCNP Input Generation (Jinja2 templates or programmatic)
    ↓
MCNP Execution
    ↓
Results Post-Processing (matplotlib)
    ↓
Publication-Quality Outputs
```

**Common Data Sources**:
- Power histories by cycle/timestep
- Control position data (angles, insertion depths)
- Material property databases
- Experimental measurements for validation
- Operational records

**Key Operations**:

1. **Time-Weighted Averaging**: Continuous operational parameters → discrete MCNP configurations
   ```python
   ave_power = (power * time_intervals).sum() / total_time
   ```

2. **Discrete Parameter Selection**: Find closest modeled configuration
   ```python
   closest_angle = find_closest(available_angles, ave_angle)
   ```

3. **Binary State Selection**: Inserted/withdrawn states
   ```python
   selected_state = round(time_weighted_average(states))
   ```

**See**: `data_integration_guide.md` for complete tools and examples

### 4. Quality Assurance Checkpoints

**Multi-Level Validation Strategy**:

#### Pre-Run Validation
- Input file syntax checking
- Dimension verification (FILL arrays)
- Cross-reference validation (all referenced surfaces/materials exist)
- Physical constraint checks (packing fraction < 1, radii increase)
- Geometry visualization (MCNP plotter)

#### Mid-Run Monitoring
- Statistical convergence checks (keff, entropy, source distribution)
- Lost particle tracking (geometry errors)
- Progress monitoring (output file timestamps)
- Resource usage (memory, time)

#### Post-Run Validation
- Result sanity checks (physical limits, expected ranges)
- Benchmark comparisons (experimental data, analytical limits)
- Uncertainty quantification
- Regression testing (compare to previous results)

**See**: `quality_assurance_workflows.md` for implementation details

## IMPLEMENTATION STRATEGIES

### Choosing Template vs. Programmatic Approach

**Decision Matrix**:

| Factor | Template | Programmatic |
|--------|----------|--------------|
| **Base Model** | Large existing (e.g., ATR reactor) | Built from scratch |
| **Variations** | Parametric changes only | Structural changes needed |
| **Complexity** | Stable base geometry | Algorithmic geometry |
| **Flexibility** | Limited to template variables | Complete freedom |
| **Learning Curve** | Lower (if template exists) | Higher |
| **Best For** | Experiment in host reactor | New reactor design |

**Hybrid Approach**: Combine both
- Base model (template)
- Generated insertions (programmatic)
- Best of both worlds

### Workflow Orchestration

#### Bash Script Orchestration

Simple sequential workflow:

```bash
#!/bin/bash
# Example workflow script

set -e  # Exit on error

# Stage 1: Generate inputs
echo "Generating MCNP inputs..."
python scripts/create_inputs.py

# Stage 2: Validate
echo "Validating inputs..."
for f in inputs/*.i; do
    python scripts/validate_input.py "$f" || exit 1
done

# Stage 3: Run MCNP (parallel execution)
echo "Running MCNP calculations..."
for f in inputs/*.i; do
    mcnp6 i="$f" n="${f%.i}." tasks 8 &
done
wait

# Stage 4: Post-process
echo "Post-processing results..."
python scripts/aggregate_results.py
python scripts/generate_plots.py

echo "Workflow complete!"
```

#### Python Workflow Manager

More sophisticated orchestration with error handling:

```python
from workflow_orchestrator import Workflow, InputGenerationStage, ValidationStage, MCNPExecutionStage, PostProcessingStage

workflow = Workflow("HTGR Analysis", working_dir=".")

workflow.add_stage(InputGenerationStage(script="scripts/create_inputs.py"))
workflow.add_stage(ValidationStage(input_files=["inputs/case1.i", "inputs/case2.i"]))
workflow.add_stage(MCNPExecutionStage(input_files=["inputs/case1.i"], tasks=8))
workflow.add_stage(PostProcessingStage(script="scripts/post_process.py"))

success = workflow.run()
```

**See**: `scripts/workflow_orchestrator.py` for complete implementation

#### HPC Job Submission

**SLURM Example**:
```bash
#!/bin/bash
#SBATCH --job-name=mcnp_workflow
#SBATCH --nodes=1
#SBATCH --ntasks=36
#SBATCH --time=48:00:00
#SBATCH --mem=128G

module load mcnp6
module load python

# Generate inputs
python create_inputs.py

# Run MCNP
mcnp6 i=input.i n=output. tasks 36

# Post-process
python post_process.py
```

## DATA MANAGEMENT

### External Data Integration

**CSV/Excel → Pandas → MCNP**:

```python
import pandas as pd
import numpy as np

# Load experimental measurements
power_df = pd.read_csv('data/power.csv')

# Time-weighted averaging
def time_weighted_average(values, times):
    intervals = np.diff(times, prepend=0)
    return (values * intervals).sum() / intervals.sum()

# Apply to each cycle
for cycle in power_df['Cycle'].unique():
    data = power_df[power_df['Cycle'] == cycle]
    ave_power = time_weighted_average(data['Power_MW'], data['Time_h'])
    # Use ave_power in MCNP input generation
```

**Common Data Formats**:
- Power histories: `Cycle, Time_h, Power_MW, [Lobe-specific columns]`
- Control positions: `Cycle, Time_h, Angle_deg` or `Depth_cm`
- Material properties: `Material, Temperature_K, Density_g/cm3, Composition`
- Experimental results: `Location, Measurement, Uncertainty`

**See**: `scripts/data_integration_tools.py` for complete toolkit

### Inter-Code Data Handoff

#### MCNP → Depletion Code

**Data Passed**:
- Cell-wise flux distributions (from F4 tallies)
- Cell-wise power distributions (from F7 tallies)
- Neutron spectra (for activation calculations)

**Format**: Typically MCNP OUTP/MCTAL files → parsed by coupling tool

#### Depletion Code → MCNP

**Data Passed**:
- Isotopic inventories → material card updates
- Decay gammas → photon source definitions (SDEF)

**Example Material Update**:
```
c Updated material after 100 days burnup
m101  $ Depleted UO2
     92235.00c   1.234e-03  $ U-235 (depleted)
     92238.00c   2.123e-02  $ U-238
     94239.00c   5.678e-05  $ Pu-239 (bred)
     94240.00c   1.234e-05  $ Pu-240 (bred)
      8016.00c   4.456e-02  $ O-16
     [... fission products ...]
```

**Example Photon Source**:
```
c Decay photon source from depleted fuel
sdef par=p erg=d1 pos=d2
si1  L  0.511 0.662 1.173 1.332  $ Photon energies (MeV)
sp1    0.15  0.35  0.25  0.25   $ Probabilities
si2  L  (0 0 0) (10 0 0) (20 0 0)  $ Source positions (cells)
sp2    0.4      0.35     0.25       $ Position probabilities (by cell activity)
```

### Results Management

#### MCNP Outputs → Post-Processing

**Output Files**:
- `*.o` - Main output file (tallies, keff, warnings)
- `*.m` - MCTAL file (tally data in binary/ASCII)
- `*.msht` - MESHTAL file (mesh tally data)
- `*.h5` - HDF5 output (large datasets)

**Python Processing**:
```python
import re
import pandas as pd

def parse_keff(output_file):
    """Extract keff from MCNP output."""
    with open(output_file, 'r') as f:
        for line in f:
            if 'final result' in line.lower():
                match = re.search(r'(\d+\.\d+)\s+(\d+\.\d+)', line)
                if match:
                    keff = float(match.group(1))
                    uncertainty = float(match.group(2))
                    return keff, uncertainty
    return None, None

def parse_tally(mctal_file, tally_number):
    """Extract tally data from MCTAL file."""
    # Use MCNPTools or custom parser
    # Return as pandas DataFrame
    pass
```

## REPRODUCIBILITY ENGINEERING

### Version Control Integration

**Git Workflow for MCNP Projects**:

```bash
# Initialize repository
git init
git add scripts/ data/ templates/ README.md LICENSE

# Ignore generated files
echo "inputs/*.i" >> .gitignore
echo "outputs/" >> .gitignore
echo "*.o" >> .gitignore
echo "*.m" >> .gitignore

# Track changes
git commit -m "Initial commit: MCNP workflow framework"
```

**.gitignore Patterns**:
```gitignore
# MCNP outputs
*.o
*.r
*.m
*.s
*.msht
*.mctal

# Generated inputs (regenerate with scripts)
inputs/*.i

# Large output files
outputs/

# Temporary files
*.tmp
*.swp
*~

# Python cache
__pycache__/
*.pyc

# Jupyter checkpoints
.ipynb_checkpoints/
```

**Commit Message Conventions**:
```
feat: Add hexagonal lattice support
fix: Correct FILL array dimension calculation
docs: Update README with workflow description
test: Add validation for thermal scattering
refactor: Simplify material generation function
```

### Data Provenance

**Track Data Lineage**:

```python
PROVENANCE = {
    'power_data': {
        'source': 'ATR operational records',
        'file': 'data/power.csv',
        'date_accessed': '2024-01-10',
        'notes': 'Lobe-specific power by cycle'
    },
    'control_positions': {
        'source': 'ATR control system logs',
        'file': 'data/oscc.csv',
        'date_accessed': '2024-01-10',
        'notes': 'Outer safety control cylinder angles'
    },
    'geometry': {
        'source': 'ORNL-TM-6744 (AGR-1 design report)',
        'reference': 'Maki et al., ORNL/TM-6744, 2009',
        'notes': 'TRISO particle dimensions, compact specifications'
    }
}

# Save provenance with results
import json
with open('results/data_provenance.json', 'w') as f:
    json.dump(PROVENANCE, f, indent=2)
```

### Documentation Automation

**README.md Template**:
```markdown
# Project Title

Brief description of reactor model and analysis goals.

## Purpose

What question does this analysis answer?

## Repository Contents

- `data/`: External data sources
- `scripts/`: Model generation and analysis
- `results/`: Publication-quality outputs

## Requirements

- MCNP6.2 or later
- Python 3.8+ with pandas, numpy, matplotlib
- (Optional) MOAA for depletion coupling

## Usage

### Generate MCNP Inputs

    python scripts/create_inputs.py

### Run Calculations

    ./scripts/run_workflow.sh

### Post-Process Results

    python scripts/post_process.py

## Validation

Results compared to:
- Experimental measurements (data/experimental_results.csv)
- Benchmark calculations (reference)

## Citation

If you use this work, please cite:

[Author et al., Journal, Year, DOI]

## License

[License type]

## Contact

[Author contact information]
```

### Archival and Citation

**CITATION.cff Format**:
```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Doe"
    given-names: "Jane"
    orcid: "https://orcid.org/0000-0000-0000-0000"
title: "HTGR Burnup and Dose Rate Analysis"
version: 1.0.0
date-released: 2024-01-15
url: "https://github.com/user/repo"
doi: 10.5281/zenodo.1234567
```

**Zenodo Integration**: Create releases with DOI for permanent citation

## EXAMPLE WORKFLOWS

### Example 1: Burnup-to-Shutdown-Dose-Rate (B2SDR)

**Location**: `examples/b2sdr_workflow/`

**Complete working example**:
1. Generate neutron transport model
2. Run MCNP neutron calculation
3. Extract flux distributions
4. Run ORIGEN depletion
5. Generate photon sources from decay
6. Generate photon transport model
7. Run MCNP photon calculation
8. Post-process dose rates

**See**: `examples/b2sdr_workflow/README.md` for complete instructions

### Example 2: Parametric Reactor Study

**Location**: `examples/parametric_study/`

**13-cycle AGR-1 workflow**:
- One template → 13 cycle-specific inputs
- Automated variation (power, control positions)
- Pre-run validation
- Parallel execution
- Results aggregation

**See**: `examples/parametric_study/README.md` for complete instructions

## COMMON PATTERNS

### Time-Weighted Averaging

**Problem**: Continuous operational parameters → discrete MCNP configurations

**Solution**:
```python
def time_weighted_average(values, times):
    intervals = np.diff(times, prepend=0)
    return (values * intervals).sum() / intervals.sum()

# Example: Average control angle over cycle
ave_angle = time_weighted_average(
    cycle_data['Angle_deg'].values,
    cycle_data['Time_h'].values
)
```

### Cell Selection for Tracking

**Which cells to track in depletion calculations?**

**Guidelines**:
- ✅ Fuel cells (isotopic evolution critical)
- ✅ Structural materials (activation important)
- ✅ Moderator (neutron spectrum changes)
- ✅ Control materials (burnup affects worth)
- ❌ Void cells (no material to deplete)
- ❌ Far reflector (minimal activation)

**Balance**: Fidelity vs. computational cost (~150-200 cells typical)

### Source Definition from Depletion

**Convert isotopic inventory → SDEF cards**:

```python
def create_photon_source(isotopic_inventory, decay_time):
    """
    Generate SDEF cards from depleted isotopics.

    Args:
        isotopic_inventory: dict of {cell: {isotope: atoms}}
        decay_time: cooling time (days)

    Returns:
        SDEF card string
    """
    # Decay isotopes to get gamma spectra
    gamma_sources = decay_isotopes(isotopic_inventory, decay_time)

    # Build SDEF
    sdef = "sdef par=p erg=d1 pos=d2\n"

    # Energy distribution (combine all cells)
    energies, probabilities = combine_spectra(gamma_sources)
    sdef += f"si1  L  {' '.join(map(str, energies))}\n"
    sdef += f"sp1    {' '.join(map(str, probabilities))}\n"

    # Position distribution (by cell)
    positions = [cell_center(c) for c in gamma_sources.keys()]
    intensities = [gamma_sources[c]['total_intensity'] for c in gamma_sources.keys()]

    sdef += f"si2  L  {' '.join(f'({p[0]} {p[1]} {p[2]})' for p in positions)}\n"
    sdef += f"sp2    {' '.join(map(str, normalize(intensities)))}\n"

    return sdef
```

### Variance Reduction in Coupled Calculations

**Challenge**: Photon dose rates far from source (shielding)

**Solutions**:
1. **Importance Maps**: Higher importance in detector regions
2. **Weight Windows**: Generate from adjoint calculation
3. **Source Biasing**: Emphasize high-energy gammas
4. **Geometry Splitting**: Split particles at boundaries

**See**: mcnp-variance-reducer skill for detailed implementation

## TOOLS AND LIBRARIES

### Python Libraries

- **pandas**: Data manipulation (CSV processing)
- **numpy**: Numerical calculations
- **jinja2**: Template rendering
- **matplotlib**: Plotting
- **h5py**: HDF5 file handling (large MCNP outputs)

**Installation**:
```bash
pip install pandas numpy jinja2 matplotlib h5py
```

### MCNP-Specific Tools

- **MOAA**: MCNP-ORIGEN coupling for depletion
- **MCNPTools**: Output parsing library
- **MCNP Plotter**: Geometry visualization
- **ADVANTG**: Automated variance reduction

### Version Control

- **Git**: Source control
- **Git LFS**: Large file storage (for large datasets)
- **Zenodo**: DOI assignment for archival

## TROUBLESHOOTING

### Common Issues

**Issue**: Generated inputs have FILL array dimension mismatches

**Solution**: Validate FILL arrays before running
```python
def validate_fill_array(lat_spec, fill_data):
    nx, ny, nz = parse_lattice_spec(lat_spec)
    expected_elements = nx * ny * nz
    actual_elements = len(fill_data)
    assert expected_elements == actual_elements, \
        f"FILL mismatch: need {expected_elements}, have {actual_elements}"
```

**Issue**: Time-weighted averaging gives unexpected results

**Solution**: Visualize data before averaging
```python
import matplotlib.pyplot as plt

plt.figure()
plt.step(times, values, where='post', label='Raw Data')
plt.axhline(ave_value, color='r', linestyle='--', label='Time-Weighted Average')
plt.legend()
plt.savefig('parameter_check.png')
```

**Issue**: Workflow fails mid-execution

**Solution**: Implement checkpoint-restart
```python
# Check if stage already completed
if os.path.exists('outputs/stage2_complete.flag'):
    print("Stage 2 already completed, skipping...")
else:
    run_stage_2()
    open('outputs/stage2_complete.flag', 'w').close()
```

## REFERENCES

### Primary Sources

1. **HTGR Burnup and Dose Rates Study** (Zenodo DOI: 10.5281/zenodo.10257801)
   - Professional workflow example
   - AGR-1 and microreactor case studies
   - Template and programmatic approaches

2. **MOAA User Manual** - MCNP-ORIGEN coupling methodology

3. **MCNP6 Manual Chapter 5** - Repeated structures and lattices

### Related Skills

- **mcnp-input-builder**: Basic MCNP syntax
- **mcnp-geometry-builder**: Geometry definitions
- **mcnp-lattice-builder**: Repeated structures
- **mcnp-material-builder**: Material definitions
- **mcnp-burnup-builder**: Depletion physics
- **mcnp-input-validator**: Pre-run validation

## REFERENCE FILES

This skill includes detailed reference guides:

1. `workflow_patterns_reference.md` - Comprehensive workflow examples
2. `data_integration_guide.md` - External data integration
3. `template_automation_guide.md` - Jinja2 templating
4. `programmatic_generation_guide.md` - Python-based generation
5. `quality_assurance_workflows.md` - Validation checkpoints
6. `reproducibility_guide.md` - Version control and archival

## SKILL WORKFLOW

When user requests workflow integration help:

1. **Identify Pattern**: Which workflow pattern applies?
   - Sequential multi-physics coupling?
   - Parametric study automation?
   - Data integration pipeline?

2. **Choose Approach**: Template or programmatic?
   - Assess base model, variations needed
   - Recommend appropriate strategy

3. **Provide Implementation**: Concrete code examples
   - Generation scripts
   - Orchestration scripts
   - Validation checks

4. **Enable QA**: Quality assurance checkpoints
   - Pre-run validation
   - Mid-run monitoring
   - Post-run validation

5. **Ensure Reproducibility**: Documentation and version control
   - README template
   - .gitignore patterns
   - CITATION.cff

**Always**: Reference detailed guides for complete examples
