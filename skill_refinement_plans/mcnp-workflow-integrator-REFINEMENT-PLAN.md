# SKILL REFINEMENT PLAN: mcnp-workflow-integrator (NEW SKILL)
## Multi-Physics Workflow Automation and Data Integration

**Date**: November 8, 2025
**Status**: NEW SKILL - Not yet implemented
**Priority**: 🟡 MEDIUM (Phase 2)
**Based On**: HTGR reactor model workflow analysis (htgr-model-burnup-and-doserates)

---

## EXECUTIVE SUMMARY

**mcnp-workflow-integrator** is a NEW skill that teaches users how to:
1. Orchestrate multi-physics workflows (MCNP → depletion codes → MCNP)
2. Automate data handoff between codes
3. Implement burnup-to-dose-rate calculation pipelines
4. Integrate external data sources (experimental, operational)
5. Create reproducible, version-controlled calculation workflows
6. Implement quality assurance checkpoints

**This skill bridges the gap** between isolated MCNP calculations and professional reactor analysis workflows involving multiple codes, data sources, and calculation stages.

---

## SKILL SCOPE AND RESPONSIBILITIES

### What This Skill DOES Teach

✅ **Multi-Physics Coupling Patterns**:
- MCNP neutron transport → depletion tracking (ORIGEN, CINDER90, etc.)
- Depletion results → photon source definitions
- Iterative coupling (flux-to-power, power-to-source)
- Sequential vs. coupled workflows

✅ **Data Pipeline Design**:
- CSV/Excel → Python processing → MCNP input generation
- MCNP output → intermediate processing → next calculation stage
- Results aggregation and post-processing
- Publication-quality output generation

✅ **Workflow Automation**:
- Script-based orchestration (bash, Python)
- Parametric study automation (multiple cases from one template)
- Error handling and checkpoint-restart
- Batch job submission for HPC systems

✅ **Quality Assurance**:
- Pre-run validation (input checking, dimension verification)
- Mid-workflow checkpoints (convergence checks, statistical quality)
- Post-run validation (result sanity checks, benchmark comparison)
- Automated testing and regression detection

✅ **Reproducibility Engineering**:
- Version control integration (Git workflows)
- Data provenance tracking (source → calculation → result)
- Documentation automation (README generation, plots)
- Permanent archival (DOI assignment, Zenodo)

### What This Skill DOES NOT Teach

❌ **MCNP Syntax** - See mcnp-input-builder, mcnp-geometry-builder
❌ **Lattice Building** - See mcnp-lattice-builder
❌ **Material Definitions** - See mcnp-material-builder
❌ **Depletion Physics** - See mcnp-burnup-builder
❌ **Statistical Analysis** - See mcnp-statistics-checker

**This skill focuses on INTEGRATION, not individual code capabilities.**

---

## KEY WORKFLOW PATTERNS FROM HTGR STUDY

### Pattern 1: Burnup-to-Shutdown-Dose-Rate (B2SDR)

**Complete workflow demonstrated in AGR-1 and Micro models**:

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

---

### Pattern 2: Parametric Study Workflow (AGR-1 13-Cycle Study)

**One template → 13 cycle-specific inputs**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   DATA PREPARATION STAGE                        │
├─────────────────────────────────────────────────────────────────┤
│ External Data Sources:                                          │
│   • power.csv         - Lobe-specific power by cycle/timestep  │
│   • oscc.csv          - Control drum angles vs. time           │
│   • neck_shim.csv     - Shim rod insertion states              │
│   • geometry_params.py - Fixed geometric parameters            │
│                                                                  │
│ Processing:                                                      │
│   • Time-weighted averaging (continuous → discrete)            │
│   • Closest-value selection (angles, positions)                │
│   • Data validation (range checks, completeness)               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   TEMPLATE RENDERING STAGE                      │
├─────────────────────────────────────────────────────────────────┤
│ Template: bench.template (13,727 lines)                         │
│ Variables: {{cells}}, {{surfaces}}, {{materials}},             │
│            {{oscc_surfaces}}, {{ne_cells}}, {{se_cells}}       │
│                                                                  │
│ Jinja2 Rendering:                                               │
│   for cycle in ['138B', '139A', ..., '145A']:                  │
│       params = process_cycle_data(cycle)                       │
│       input = template.render(**params)                        │
│       write(f'bench_{cycle}.i', input)                         │
│                                                                  │
│ Output: 13 MCNP input files (bench_138B.i ... bench_145A.i)    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   VALIDATION STAGE (Pre-Run)                    │
├─────────────────────────────────────────────────────────────────┤
│ Automated Checks:                                               │
│   ✓ Dimension verification (FILL arrays)                       │
│   ✓ Cross-reference validation (surfaces, materials)           │
│   ✓ Numbering conflict detection                               │
│   ✓ Physical constraint checks (PF < 1, radii increase)        │
│                                                                  │
│ Visualization:                                                   │
│   • 39 diagnostic plots (power, control positions vs. time)    │
│   • Visual inspection of parameters                            │
│                                                                  │
│ Quality Gates:                                                   │
│   • All checks pass → proceed to execution                     │
│   • Failures → fix and re-generate                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   EXECUTION STAGE (HPC Cluster)                 │
├─────────────────────────────────────────────────────────────────┤
│ Parallel Execution:                                             │
│   • 13 independent MOAA runs (one per cycle)                   │
│   • Each run: neutron transport + depletion                    │
│   • Resource allocation: 36 cores × 48 hours per cycle         │
│                                                                  │
│ Monitoring:                                                      │
│   • Track progress via output file timestamps                  │
│   • Check for fatal errors, lost particles                     │
│   • Statistical quality assessment (keff convergence)          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   RESULTS AGGREGATION STAGE                     │
├─────────────────────────────────────────────────────────────────┤
│ Data Extraction:                                                │
│   • Parse MCNP output files (keff, burnup, flux)               │
│   • Extract ORIGEN isotopic inventories                        │
│   • Compile time-series data                                   │
│                                                                  │
│ Post-Processing (plots.py):                                     │
│   • Burnup vs. cycle plots                                     │
│   • Comparison to experimental MOAA_burnup_FIMA.csv            │
│   • Isotopic evolution curves                                  │
│   • Publication-quality figures (matplotlib)                   │
│                                                                  │
│ Validation:                                                      │
│   • Compare to experimental measurements                       │
│   • Check expected trends                                      │
│   • Statistical analysis of results                            │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features**:
- Single-source-of-truth (one template, one script)
- Automated variation (loop over parameters)
- Pre-run validation (catch errors early)
- Parallel execution (independent cases)
- Traceable results (parameter → output linkage)

---

### Pattern 3: Programmatic Model Generation Workflow (Micro SDR)

**Complete model generation from Python functions**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   PARAMETER DEFINITION STAGE                    │
├─────────────────────────────────────────────────────────────────┤
│ File: input_definition.py                                       │
│                                                                  │
│ Centralized Parameters:                                         │
│   • TRISO particle dimensions (kernel, buffer, IPyC, SiC, OPyC)│
│   • Packing fractions by compact type                          │
│   • Assembly layout (4 layers × 36 assemblies)                 │
│   • Material densities and compositions                        │
│   • Universe numbering scheme                                   │
│                                                                  │
│ Assembly Functions:                                             │
│   def fuel(layer, number):        → cells, surfaces, materials │
│   def control(layer, number):     → cells, surfaces, materials │
│   def reflector():                → cells, surfaces, materials │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MODEL GENERATION STAGE                        │
├─────────────────────────────────────────────────────────────────┤
│ Script: create_input_burnup.py OR create_input_sdr.py          │
│                                                                  │
│ Algorithm:                                                       │
│   1. Import shared parameters from input_definition.py         │
│   2. Loop over layers and assemblies                           │
│   3. Call appropriate function (fuel, control, reflector)      │
│   4. Accumulate cells, surfaces, materials                     │
│   5. Add data cards (source, tallies, physics)                 │
│   6. Write complete MCNP input file                            │
│                                                                  │
│ Burnup Model:                                                    │
│   • Core geometry only                                         │
│   • Tracking materials for ~170 cells                          │
│                                                                  │
│ SDR Model:                                                       │
│   • Same core + shielding geometry                             │
│   • Photon sources from depletion results                      │
│   • FMESH tallies for 3D dose maps                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CONSISTENCY VALIDATION                        │
├─────────────────────────────────────────────────────────────────┤
│ Automated Checks:                                               │
│   assert 0 <= packing_fraction <= 1                            │
│   assert vol_triso_tot < vol_compact                           │
│   assert all(radii[i] < radii[i+1] for concentric layers)     │
│   assert no duplicate surface numbers                          │
│                                                                  │
│ Geometric Verification:                                         │
│   • MCNP plotter (geometry visualization)                      │
│   • Lost particle analysis                                     │
│                                                                  │
│ Model Comparison:                                               │
│   • Burnup model core ≡ SDR model core (diff check)            │
│   • Only sources and tallies differ                            │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features**:
- Fully algorithmic generation (no manual editing)
- Guaranteed consistency (shared parameter file)
- Easy variant generation (change parameters, re-run script)
- Built-in validation (defensive programming)

---

## SKILL.md STRUCTURE (TO BE CREATED)

### File Location
`.claude/skills/mcnp-workflow-integrator/SKILL.md`

### Proposed Content Outline

```markdown
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

## CORE WORKFLOW PATTERNS

### 1. Sequential Multi-Physics Coupling

[Detailed pattern with examples]

### 2. Parametric Study Automation

[Template-based and programmatic approaches]

### 3. Data Integration Pipeline

[External data → processing → MCNP → results]

### 4. Quality Assurance Checkpoints

[Validation at each stage]

## IMPLEMENTATION STRATEGIES

### Template-Based Workflows (Jinja2)

When to use:
- Large stable base model with parametric variations
- Multiple similar cases (cycle-by-cycle analysis)
- Insertion of generated content into existing model

Example: AGR-1 13-cycle study

### Programmatic Workflows (Python Functions)

When to use:
- Model built from scratch
- Algorithmic geometry (lattices, assemblies)
- Need for complete flexibility
- Tight parameter coupling

Example: Micro reactor SDR model

### Hybrid Workflows

Combine both approaches:
- Base model (template)
- Generated insertions (programmatic)
- Best of both worlds

## DATA MANAGEMENT

### External Data Integration

CSV/Excel → Pandas → MCNP:
- Experimental measurements
- Operational histories (power, control positions)
- Material properties databases
- Benchmark specifications

### Inter-Code Data Handoff

MCNP → Depletion Code:
- Cell-wise flux/power distributions
- Neutron spectra for activation

Depletion Code → MCNP:
- Isotopic inventories → material cards
- Decay gammas → photon sources

### Results Management

MCNP Outputs → Post-Processing:
- OUTP file parsing
- MCTAL file extraction
- MESHTAL/FMESH processing
- HDF5/XDMF for large datasets

## WORKFLOW ORCHESTRATION

### Bash Script Orchestration

```bash
#!/bin/bash
# Example workflow script

# Stage 1: Generate inputs
python create_inputs.py

# Stage 2: Validate
for f in inputs/*.i; do
    python validate_input.py "$f" || exit 1
done

# Stage 3: Run MCNP
for f in inputs/*.i; do
    mcnp6 i="$f" n="${f%.i}." &
done
wait

# Stage 4: Post-process
python aggregate_results.py
python generate_plots.py
```

### Python Workflow Manager

[More sophisticated orchestration with error handling]

### HPC Job Submission

SLURM, PBS, LSF examples

## QUALITY ASSURANCE

### Pre-Run Validation

- Input file syntax checking
- Dimension verification (FILL arrays)
- Cross-reference validation
- Physical constraint checks

### Mid-Run Monitoring

- Statistical convergence checks
- Lost particle tracking
- Progress monitoring

### Post-Run Validation

- Result sanity checks
- Benchmark comparisons
- Uncertainty quantification
- Regression testing

## REPRODUCIBILITY ENGINEERING

### Version Control Integration

Git workflow for MCNP projects:
- Track scripts, not generated files
- .gitignore patterns
- Commit message conventions
- Branch strategies for parametric studies

### Data Provenance

Track data lineage:
- Source attribution
- Processing history
- Calculation metadata
- Result documentation

### Documentation Automation

Auto-generate:
- README files with workflow description
- Input parameter summaries
- Result tables and figures
- Citation information

### Archival and Citation

- Zenodo integration for DOI assignment
- README.md best practices
- LICENSE selection
- CITATION.cff files

## EXAMPLE WORKFLOWS

### Example 1: Burnup-to-Shutdown-Dose-Rate (B2SDR)

[Complete working example from HTGR study]

### Example 2: Parametric Reactor Study

[13-cycle AGR-1 workflow]

### Example 3: Benchmark Validation Suite

[Automated comparison to experimental data]

## COMMON PATTERNS

### Time-Weighted Averaging

Continuous operational parameters → discrete MCNP configurations

### Cell Selection for Tracking

Which cells to track in depletion calculations

### Source Definition from Depletion

Convert isotopic inventory → SDEF cards

### Variance Reduction in Coupled Calculations

Importance maps, weight windows for SDR

## TOOLS AND LIBRARIES

### Python Libraries

- **pandas**: Data manipulation
- **numpy**: Numerical calculations
- **jinja2**: Template rendering
- **matplotlib**: Plotting
- **h5py**: HDF5 file handling

### MCNP-Specific Tools

- **MOAA**: MCNP-ORIGEN coupling
- **MCNPTools**: Output parsing
- **MCNP Plotter**: Geometry visualization

### Version Control

- **Git**: Source control
- **Git LFS**: Large file storage
- **Zenodo**: DOI assignment

## TROUBLESHOOTING

[Common workflow issues and solutions]

## REFERENCES

- HTGR Burnup and Dose Rates Study (Zenodo DOI)
- MOAA User Manual
- MCNP6 Manual Chapter 5 (Repeated Structures)
```

---

## REFERENCE FILES TO CREATE

### 1. workflow_patterns_reference.md

**Location**: `.claude/skills/mcnp-workflow-integrator/workflow_patterns_reference.md`

**Content**:
```markdown
# Workflow Patterns Reference

Comprehensive examples of multi-physics workflows for reactor analysis.

## Pattern 1: Linear Sequential Workflow

MCNP → ORIGEN → MCNP (B2SDR)

[Detailed example with code]

## Pattern 2: Iterative Coupling

MCNP ↔ Thermal-Hydraulics (k-eff convergence)

[Example workflow]

## Pattern 3: Parallel Parametric

Multiple independent MCNP runs

[Array job example]

## Pattern 4: Multi-Stage Validation

Generation → Validation → Execution → Analysis

[Quality gates example]
```

---

### 2. data_integration_guide.md

**Location**: `.claude/skills/mcnp-workflow-integrator/data_integration_guide.md`

**Content**:
```markdown
# Data Integration Guide

How to integrate external data sources into MCNP workflows.

## CSV Data Processing

### Power Histories

```python
import pandas as pd
import numpy as np

# Load experimental power data
power_df = pd.read_csv('power.csv')

# Time-weighted averaging
def time_weighted_average(values, times):
    intervals = np.diff(times, prepend=0)
    return (values * intervals).sum() / intervals.sum()

# Apply to each cycle
for cycle in power_df['Cycle'].unique():
    data = power_df[power_df['Cycle'] == cycle]
    ave_power = time_weighted_average(data['Power_MW'], data['Time_h'])
```

### Control Position Data

[Example of discrete parameter selection]

### Material Properties

[Database integration example]

## Excel Integration

[openpyxl, xlrd examples]

## Database Queries

[SQLite, PostgreSQL for large datasets]

## Experimental Data Formats

[Common measurement data structures]
```

---

### 3. template_automation_guide.md

**Location**: `.claude/skills/mcnp-workflow-integrator/template_automation_guide.md`

**Content**:
```markdown
# Template Automation Guide

Using Jinja2 for MCNP input generation.

## Basic Template Structure

```mcnp
c MCNP Template Example
c Generated by create_inputs.py
c
c Cycle: {{ cycle_name }}
c Power: {{ average_power_MW }} MW
c
c Cells
{{ cells_block }}
c
c Surfaces
{{ surfaces_block }}
c
c Materials
{{ materials_block }}
c
c Data
kcode 10000 1.0 50 250
ksrc {{ source_x }} {{ source_y }} {{ source_z }}
```

## Variable Substitution

Simple variables: `{{ variable_name }}`
Expressions: `{{ power * 1e6 | format_sci }}`
Conditionals: `{% if condition %}...{% endif %}`
Loops: `{% for item in list %}...{% endfor %}`

## Custom Filters

[MCNP-specific Jinja2 filters]

## Advanced Patterns

[Nested templates, includes, macros]
```

---

### 4. programmatic_generation_guide.md

**Location**: `.claude/skills/mcnp-workflow-integrator/programmatic_generation_guide.md`

**Content**:
```markdown
# Programmatic Generation Guide

Building MCNP inputs from Python functions.

## Function-Based Geometry

```python
def fuel_assembly(layer, number):
    """
    Generate complete fuel assembly geometry.

    Args:
        layer: Axial layer (0-3)
        number: Assembly number (1-36)

    Returns:
        Tuple of (cells_str, surfaces_str, materials_str)
    """
    # Calculate numbering
    n = f"{layer+1}{number:02d}"

    # Generate surfaces
    surfaces = f"""
c Assembly {n}
{n}01  so  0.0250    $ Kernel
{n}02  so  0.0350    $ Buffer
{n}10 c/z  0 0  1.150 $ Fuel channel
{n}13 rhp  0 0 {h}  0 0 68  0  1.6  0  $ Hex prism
"""

    # Generate cells
    cells = f"""
c Assembly {n}
{n}01 {n}1 -10.8  -{n}01  u={n}4 vol=948.35  imp:n=1  $ Kernel
{n}10 0  -{n}10  u={n}1 fill={n}8  (0 0 {hm:.1f}) imp:n=1  $ Fuel channel
"""

    # Generate materials
    materials = f"""
m{n}1  $ Kernel UO2
     92235.00c   4.816186e-03
     92238.00c   1.932238e-02
      8016.00c   4.827713e-02
"""

    return cells, surfaces, materials
```

## Consistent Interfaces

All generator functions return (cells, surfaces, materials)

## Assembly Logic

[Loop-based model building]

## Validation Integration

[Assertions, checks within functions]
```

---

### 5. quality_assurance_workflows.md

**Location**: `.claude/skills/mcnp-workflow-integrator/quality_assurance_workflows.md`

**Content**:
```markdown
# Quality Assurance Workflows

Implementing validation checkpoints in multi-physics workflows.

## Pre-Run Validation

### Input File Validation

```python
def validate_mcnp_input(filename):
    """
    Validate MCNP input before running.

    Checks:
    - File exists and is readable
    - Three-block structure present
    - FILL array dimensions correct
    - All referenced entities exist
    - No numbering conflicts

    Returns:
        dict with validation results
    """
    issues = []

    # Check file exists
    if not os.path.exists(filename):
        return {'valid': False, 'issues': [f'File {filename} not found']}

    # Parse file
    with open(filename, 'r') as f:
        content = f.read()

    # Check three-block structure
    if 'c\nc Cells\nc' not in content:
        issues.append('Missing cell block header')

    # Check FILL arrays
    lattice_cells = extract_lattice_cells(content)
    for cell in lattice_cells:
        fill_spec = extract_fill_spec(cell)
        elements_needed = calculate_fill_elements(fill_spec)
        elements_provided = count_fill_elements(cell)
        if elements_needed != elements_provided:
            issues.append(
                f'Cell {cell.number}: FILL mismatch - '
                f'need {elements_needed}, have {elements_provided}'
            )

    return {'valid': len(issues) == 0, 'issues': issues}
```

### Geometry Visualization

[MCNP plotter automation]

### Parameter Verification

[Diagnostic plots before execution]

## Mid-Run Monitoring

### Statistical Convergence

[Keff, entropy, source convergence checks]

### Lost Particle Analysis

[Geometry error detection]

### Resource Usage

[Memory, time monitoring]

## Post-Run Validation

### Result Sanity Checks

[Physical limits, expected ranges]

### Benchmark Comparison

[Automated comparison to experimental data]

### Regression Testing

[Compare to previous results]

## Continuous Integration

[GitHub Actions, GitLab CI for MCNP workflows]
```

---

### 6. reproducibility_guide.md

**Location**: `.claude/skills/mcnp-workflow-integrator/reproducibility_guide.md`

**Content**:
```markdown
# Reproducibility Engineering Guide

Making MCNP workflows reproducible for peer review and archival.

## Version Control Best Practices

### Repository Structure

```
mcnp-project/
├── README.md                 # Complete documentation
├── LICENSE                   # Legal framework
├── CITATION.cff              # Citation information
├── .gitignore                # Ignore generated files
├── data/                     # External data (CSV, Excel)
│   ├── power.csv
│   ├── geometry_params.yaml
│   └── experimental_results.csv
├── scripts/                  # Generation and analysis
│   ├── input_definition.py  # Shared parameters
│   ├── create_inputs.py     # Input generation
│   ├── validate.py          # Pre-run checks
│   ├── run_workflow.sh      # Orchestration script
│   └── post_process.py      # Results analysis
├── templates/                # Jinja2 templates (if used)
│   └── base_model.template
├── inputs/                   # Generated MCNP inputs (gitignored)
├── outputs/                  # MCNP outputs (gitignored)
└── results/                  # Processed results, figures
    ├── plots/
    └── tables/
```

### .gitignore Patterns

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

### Commit Message Conventions

```
feat: Add hexagonal lattice support
fix: Correct FILL array dimension calculation
docs: Update README with workflow description
test: Add validation for thermal scattering
refactor: Simplify material generation function
```

## Documentation Standards

### README.md Template

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

### CITATION.cff Format

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

## Data Provenance

### Tracking Data Sources

```python
# In input generation script

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

### Metadata Recording

[Calculation metadata, software versions, runtime info]

## Archival Best Practices

### Zenodo Integration

[How to create releases with DOI]

### Long-Term Storage

[File formats for archival: HDF5, ASCII, PDF/A]

### Minimal Reproducibility Package

What to include for others to reproduce:
- [ ] All data files
- [ ] All generation scripts
- [ ] README with complete instructions
- [ ] Software version requirements
- [ ] Expected runtime and resources
- [ ] Validation data
- [ ] LICENSE file
```

---

## PYTHON SCRIPTS TO CREATE

### 1. workflow_orchestrator.py

**Location**: `.claude/skills/mcnp-workflow-integrator/scripts/workflow_orchestrator.py`

```python
"""
MCNP Multi-Physics Workflow Orchestrator

Automates execution of multi-stage reactor analysis workflows.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class WorkflowStage:
    """Base class for workflow stages."""

    def __init__(self, name: str, working_dir: Path):
        self.name = name
        self.working_dir = Path(working_dir)
        self.status = 'pending'
        self.start_time = None
        self.end_time = None
        self.error_msg = None

    def execute(self) -> bool:
        """
        Execute this stage.

        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate prerequisites for this stage.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        return True, []

    def run(self) -> bool:
        """
        Run this stage with validation and error handling.

        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"STAGE: {self.name}")
        print(f"{'='*60}")

        # Validate prerequisites
        print(f"Validating prerequisites...")
        is_valid, issues = self.validate()
        if not is_valid:
            print(f"❌ Validation failed:")
            for issue in issues:
                print(f"   - {issue}")
            self.status = 'validation_failed'
            self.error_msg = '; '.join(issues)
            return False
        print(f"✓ Validation passed")

        # Execute stage
        print(f"Executing {self.name}...")
        self.status = 'running'
        self.start_time = time.time()

        try:
            success = self.execute()
            self.end_time = time.time()

            if success:
                self.status = 'completed'
                elapsed = self.end_time - self.start_time
                print(f"✓ {self.name} completed in {elapsed:.1f} seconds")
                return True
            else:
                self.status = 'failed'
                print(f"❌ {self.name} failed")
                return False

        except Exception as e:
            self.end_time = time.time()
            self.status = 'error'
            self.error_msg = str(e)
            print(f"❌ {self.name} error: {e}")
            return False


class InputGenerationStage(WorkflowStage):
    """Generate MCNP inputs from scripts."""

    def __init__(self, working_dir: Path, script: str, **kwargs):
        super().__init__("Input Generation", working_dir)
        self.script = script
        self.kwargs = kwargs

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        # Check script exists
        script_path = self.working_dir / self.script
        if not script_path.exists():
            issues.append(f"Generation script not found: {script_path}")

        # Check Python available
        try:
            subprocess.run(['python', '--version'],
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            issues.append("Python not available")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        cmd = ['python', self.script]
        result = subprocess.run(cmd, cwd=self.working_dir,
                              capture_output=True, text=True)

        if result.returncode != 0:
            self.error_msg = result.stderr
            print(result.stderr)
            return False

        print(result.stdout)
        return True


class ValidationStage(WorkflowStage):
    """Validate generated inputs."""

    def __init__(self, working_dir: Path, input_files: List[Path]):
        super().__init__("Input Validation", working_dir)
        self.input_files = [Path(f) for f in input_files]

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        for inp in self.input_files:
            if not inp.exists():
                issues.append(f"Input file not found: {inp}")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        # Import validation functions
        sys.path.insert(0, str(self.working_dir / 'scripts'))
        try:
            from validate import validate_mcnp_input
        except ImportError:
            print("Warning: validate.py not found, skipping detailed checks")
            return True

        all_valid = True
        for inp in self.input_files:
            print(f"  Validating {inp.name}...")
            result = validate_mcnp_input(inp)

            if not result['valid']:
                all_valid = False
                print(f"    ❌ Issues found:")
                for issue in result['issues']:
                    print(f"       - {issue}")
            else:
                print(f"    ✓ Valid")

        return all_valid


class MCNPExecutionStage(WorkflowStage):
    """Execute MCNP calculations."""

    def __init__(self, working_dir: Path, input_files: List[Path],
                 mcnp_cmd: str = 'mcnp6', tasks: int = 1):
        super().__init__("MCNP Execution", working_dir)
        self.input_files = [Path(f) for f in input_files]
        self.mcnp_cmd = mcnp_cmd
        self.tasks = tasks

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        # Check MCNP available
        try:
            result = subprocess.run([self.mcnp_cmd, 'v'],
                                  capture_output=True, timeout=5)
            # MCNP prints version to stderr typically
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            issues.append(f"MCNP not available (command: {self.mcnp_cmd})")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        for inp in self.input_files:
            print(f"  Running {inp.name}...")

            # MCNP command: mcnp6 i=input.i n=input.
            output_prefix = inp.stem + '.'
            cmd = [self.mcnp_cmd, f'i={inp}', f'n={output_prefix}',
                   f'tasks {self.tasks}']

            # Run MCNP
            result = subprocess.run(cmd, cwd=inp.parent,
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print(f"    ❌ MCNP failed")
                print(result.stderr)
                self.error_msg = f"MCNP failed for {inp.name}"
                return False

            # Check for fatal errors in output
            output_file = inp.parent / (output_prefix + 'o')
            if output_file.exists():
                with open(output_file, 'r') as f:
                    content = f.read()
                    if 'fatal error' in content.lower():
                        print(f"    ❌ Fatal error in MCNP output")
                        self.error_msg = f"Fatal error in {inp.name}"
                        return False

            print(f"    ✓ Completed")

        return True


class PostProcessingStage(WorkflowStage):
    """Post-process results."""

    def __init__(self, working_dir: Path, script: str):
        super().__init__("Post-Processing", working_dir)
        self.script = script

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        script_path = self.working_dir / self.script
        if not script_path.exists():
            issues.append(f"Post-processing script not found: {script_path}")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        cmd = ['python', self.script]
        result = subprocess.run(cmd, cwd=self.working_dir,
                              capture_output=True, text=True)

        if result.returncode != 0:
            self.error_msg = result.stderr
            print(result.stderr)
            return False

        print(result.stdout)
        return True


class Workflow:
    """Complete multi-stage workflow."""

    def __init__(self, name: str, working_dir: Path):
        self.name = name
        self.working_dir = Path(working_dir)
        self.stages: List[WorkflowStage] = []
        self.current_stage = 0

    def add_stage(self, stage: WorkflowStage):
        """Add a stage to the workflow."""
        self.stages.append(stage)

    def run(self, start_from: int = 0) -> bool:
        """
        Execute the complete workflow.

        Args:
            start_from: Stage index to start from (for restart)

        Returns:
            True if all stages successful, False otherwise
        """
        print(f"\n{'#'*60}")
        print(f"# WORKFLOW: {self.name}")
        print(f"# Stages: {len(self.stages)}")
        print(f"# Working Directory: {self.working_dir}")
        print(f"{'#'*60}")

        for i, stage in enumerate(self.stages[start_from:], start=start_from):
            self.current_stage = i

            success = stage.run()

            if not success:
                print(f"\n❌ Workflow failed at stage {i+1}/{len(self.stages)}: {stage.name}")
                self._print_summary()
                return False

        print(f"\n{'='*60}")
        print(f"✓ Workflow completed successfully")
        print(f"{'='*60}")
        self._print_summary()
        return True

    def _print_summary(self):
        """Print workflow execution summary."""
        print(f"\nWorkflow Summary:")
        print(f"{'Stage':<30} {'Status':<15} {'Time (s)':<10}")
        print(f"{'-'*60}")

        for i, stage in enumerate(self.stages):
            elapsed = ''
            if stage.start_time and stage.end_time:
                elapsed = f"{stage.end_time - stage.start_time:.1f}"

            status_symbol = {
                'pending': '⏸',
                'running': '▶',
                'completed': '✓',
                'failed': '❌',
                'error': '💥',
                'validation_failed': '⚠'
            }.get(stage.status, '?')

            print(f"{i+1}. {stage.name:<27} {status_symbol} {stage.status:<13} {elapsed:<10}")

            if stage.error_msg:
                print(f"   Error: {stage.error_msg}")


# Example usage
if __name__ == "__main__":
    # Define workflow
    workflow = Workflow("HTGR Burnup-to-SDR Analysis", Path.cwd())

    # Stage 1: Generate inputs
    workflow.add_stage(
        InputGenerationStage(
            working_dir=Path.cwd(),
            script='scripts/create_inputs.py'
        )
    )

    # Stage 2: Validate inputs
    workflow.add_stage(
        ValidationStage(
            working_dir=Path.cwd(),
            input_files=[
                Path('inputs/bench_138B.i'),
                Path('inputs/bench_139A.i'),
                # ... etc
            ]
        )
    )

    # Stage 3: Run MCNP
    workflow.add_stage(
        MCNPExecutionStage(
            working_dir=Path.cwd(),
            input_files=[Path('inputs/bench_138B.i')],
            mcnp_cmd='mcnp6',
            tasks=8
        )
    )

    # Stage 4: Post-process
    workflow.add_stage(
        PostProcessingStage(
            working_dir=Path.cwd(),
            script='scripts/post_process.py'
        )
    )

    # Run workflow
    success = workflow.run()
    sys.exit(0 if success else 1)
```

---

### 2. data_integration_tools.py

**Location**: `.claude/skills/mcnp-workflow-integrator/scripts/data_integration_tools.py`

```python
"""
Data Integration Tools for MCNP Workflows

Tools for processing external data (CSV, Excel) into MCNP-compatible formats.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any

def time_weighted_average(values: np.ndarray, times: np.ndarray) -> float:
    """
    Calculate time-weighted average of parameter values.

    Used to convert continuous operational data to discrete MCNP configuration.

    Args:
        values: Array of parameter values
        times: Array of timestamps (must be same length as values)

    Returns:
        Time-weighted average

    Example:
        Power varies from 100 MW to 150 MW over 10 days.
        Average for MCNP = time_weighted_average([100, 150], [0, 10])
    """
    if len(values) != len(times):
        raise ValueError("Values and times must have same length")

    if len(values) == 0:
        raise ValueError("Cannot average empty array")

    if len(values) == 1:
        return float(values[0])

    # Calculate time intervals
    intervals = np.diff(times, prepend=0)

    # Time-weighted sum
    weighted_sum = (values * intervals).sum()
    total_time = intervals.sum()

    if total_time == 0:
        raise ValueError("Total time is zero")

    return weighted_sum / total_time


def find_closest_value(allowed_values: List[float], target: float) -> float:
    """
    Find closest allowed value to target.

    Used when MCNP model has discrete options (e.g., control drum angles).

    Args:
        allowed_values: List of permitted values
        target: Desired value (may not be in list)

    Returns:
        Closest value from allowed_values

    Example:
        Allowed angles: [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
        Target: 73.5 → returns 75
    """
    allowed = np.array(allowed_values)
    differences = np.abs(allowed - target)
    closest_index = np.argmin(differences)
    return float(allowed[closest_index])


def process_power_history(csv_file: str, cycle_name: str) -> Dict[str, float]:
    """
    Process power history CSV into MCNP-compatible parameters.

    Args:
        csv_file: Path to power.csv
        cycle_name: Cycle identifier (e.g., '138B')

    Returns:
        Dictionary with averaged parameters

    CSV Format:
        Cycle, Time_h, Power_MW, Lobe_NE, Lobe_NW, Lobe_SE, Lobe_SW
    """
    df = pd.read_csv(csv_file)

    # Filter to this cycle
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted averaging
    result = {
        'cycle': cycle_name,
        'duration_days': (cycle_data['Time_h'].max() - cycle_data['Time_h'].min()) / 24,
        'avg_power_MW': time_weighted_average(
            cycle_data['Power_MW'].values,
            cycle_data['Time_h'].values
        )
    }

    # Lobe-specific if available
    for lobe in ['NE', 'NW', 'SE', 'SW']:
        col = f'Lobe_{lobe}'
        if col in cycle_data.columns:
            result[f'avg_power_{lobe}_MW'] = time_weighted_average(
                cycle_data[col].values,
                cycle_data[Time_h'].values
            )

    return result


def process_control_positions(csv_file: str, cycle_name: str,
                              allowed_angles: List[float]) -> Dict[str, float]:
    """
    Process control drum position history.

    Args:
        csv_file: Path to oscc.csv (outer safety control cylinder)
        cycle_name: Cycle identifier
        allowed_angles: Discrete angles modeled in MCNP

    Returns:
        Dictionary with selected angle

    CSV Format:
        Cycle, Time_h, Angle_deg
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted average of continuous angle
    avg_angle = time_weighted_average(
        cycle_data['Angle_deg'].values,
        cycle_data['Time_h'].values
    )

    # Find closest allowed angle
    selected_angle = find_closest_value(allowed_angles, avg_angle)

    return {
        'cycle': cycle_name,
        'avg_angle_continuous': avg_angle,
        'selected_angle_discrete': selected_angle,
        'difference': abs(avg_angle - selected_angle)
    }


def process_binary_state(csv_file: str, cycle_name: str,
                        state_materials: Dict[int, Tuple[int, float]]) -> Dict[str, Any]:
    """
    Process binary state data (inserted/withdrawn).

    Args:
        csv_file: Path to state data CSV
        cycle_name: Cycle identifier
        state_materials: Mapping of state → (material_number, density)
                        Example: {0: (10, 1.00276e-1), 1: (71, 4.55926e-2)}
                        0 = withdrawn (water), 1 = inserted (hafnium)

    Returns:
        Dictionary with selected state and material

    CSV Format:
        Cycle, Time_h, State (0 or 1)
    """
    df = pd.read_csv(csv_file)
    cycle_data = df[df['Cycle'] == cycle_name]

    if len(cycle_data) == 0:
        raise ValueError(f"No data found for cycle {cycle_name}")

    # Time-weighted average of state
    avg_state = time_weighted_average(
        cycle_data['State'].values,
        cycle_data['Time_h'].values
    )

    # Round to nearest integer (0 or 1)
    selected_state = int(np.rint(avg_state))

    # Get material for this state
    material_num, density = state_materials[selected_state]

    return {
        'cycle': cycle_name,
        'avg_state_continuous': avg_state,
        'selected_state': selected_state,
        'material_number': material_num,
        'density': density,
        'state_description': 'inserted' if selected_state == 1 else 'withdrawn'
    }


def validate_csv_data(csv_file: str, required_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate CSV file structure.

    Args:
        csv_file: Path to CSV
        required_columns: List of required column names

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        return False, [f"File not found: {csv_file}"]
    except pd.errors.EmptyDataError:
        return False, [f"File is empty: {csv_file}"]
    except Exception as e:
        return False, [f"Error reading file: {e}"]

    # Check columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")

    # Check for empty data
    if len(df) == 0:
        issues.append("No data rows in file")

    # Check for NaN values in required columns
    for col in required_columns:
        if col in df.columns:
            nan_count = df[col].isna().sum()
            if nan_count > 0:
                issues.append(f"Column '{col}' has {nan_count} NaN values")

    return len(issues) == 0, issues


# Example usage
if __name__ == "__main__":
    # Example: Process AGR-1 cycle 138B data

    print("Processing power history...")
    power_params = process_power_history('data/power.csv', '138B')
    print(f"  Average power: {power_params['avg_power_MW']:.2f} MW")
    print(f"  Duration: {power_params['duration_days']:.1f} days")

    print("\nProcessing control positions...")
    allowed_angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
    control_params = process_control_positions('data/oscc.csv', '138B', allowed_angles)
    print(f"  Continuous average: {control_params['avg_angle_continuous']:.2f}°")
    print(f"  Selected discrete: {control_params['selected_angle_discrete']:.0f}°")
    print(f"  Difference: {control_params['difference']:.2f}°")

    print("\nProcessing neck shim state...")
    state_materials = {
        0: (10, 1.00276e-1),  # Withdrawn: water
        1: (71, 4.55926e-2)   # Inserted: hafnium
    }
    shim_params = process_binary_state('data/neck_shim.csv', '138B', state_materials)
    print(f"  State: {shim_params['state_description']}")
    print(f"  Material: m{shim_params['material_number']}, density={shim_params['density']:.5e}")
```

---

## EXAMPLE WORKFLOWS TO CREATE

### Example 1: Complete B2SDR Workflow

**Location**: `.claude/skills/mcnp-workflow-integrator/examples/b2sdr_workflow/`

**Structure**:
```
b2sdr_workflow/
├── README.md
├── data/
│   └── power.csv
├── scripts/
│   ├── 01_generate_neutron_model.py
│   ├── 02_run_mcnp_neutron.sh
│   ├── 03_extract_flux.py
│   ├── 04_run_origen.sh
│   ├── 05_generate_photon_sources.py
│   ├── 06_generate_sdr_model.py
│   ├── 07_run_mcnp_photon.sh
│   └── 08_post_process_dose.py
└── run_complete_workflow.sh
```

### Example 2: Parametric Study Workflow

**Location**: `.claude/skills/mcnp-workflow-integrator/examples/parametric_study/`

**Structure**:
```
parametric_study/
├── README.md
├── template.inp
├── data/
│   └── cycle_parameters.csv
├── scripts/
│   ├── create_inputs.py
│   ├── validate_inputs.py
│   ├── run_all_cases.sh
│   └── aggregate_results.py
└── run_workflow.sh
```

---

## VALIDATION AND TESTING

### Test Cases

1. **Test Template-Based Workflow**
   - User: "Create a parametric study for 10 reactor cycles"
   - Expected: Skill provides Jinja2 template approach with CSV integration

2. **Test Programmatic Workflow**
   - User: "Generate HTGR core model from Python"
   - Expected: Skill provides function-based generation pattern

3. **Test B2SDR Workflow**
   - User: "Set up burnup to dose rate calculation"
   - Expected: Skill provides complete 5-stage workflow

4. **Test Data Integration**
   - User: "How do I use experimental power data in MCNP?"
   - Expected: Skill provides CSV → time-weighted averaging → MCNP pattern

5. **Test QA Workflow**
   - User: "How do I validate inputs before running?"
   - Expected: Skill provides pre-run validation checklist and scripts

---

## SUCCESS CRITERIA

This skill refinement is successful when:

✅ **User can orchestrate multi-physics workflows**
- MCNP → depletion code → MCNP coupling understood
- Data handoff patterns clear
- Quality checkpoints defined

✅ **User can automate parametric studies**
- Template-based workflows (Jinja2)
- Programmatic workflows (Python functions)
- Validation before execution

✅ **User can integrate external data**
- CSV/Excel → pandas → MCNP
- Time-weighted averaging
- Discrete parameter selection

✅ **User can implement QA**
- Pre-run validation
- Mid-run monitoring
- Post-run validation

✅ **User can create reproducible workflows**
- Version control integration
- Data provenance tracking
- Documentation standards
- Archival best practices

---

## IMPLEMENTATION PRIORITY

**Phase**: 2 (MEDIUM PRIORITY)

**Dependencies**:
- Requires Phase 1 skills (lattice-builder, material-builder, input-validator)
- Complements mcnp-template-generator
- Enables mcnp-burnup-modeler advanced features

**Estimated Implementation Time**: 6-8 hours

**Files to Create**: 15
- 1 SKILL.md (main skill file)
- 6 reference guides
- 3 Python scripts
- 2 example workflows
- 3 README files

---

## NEXT STEPS

After creating this skill:

1. **Test with HTGR Study Replication**
   - User attempts to replicate AGR-1 workflow
   - Verify skill provides adequate guidance

2. **Integration Testing**
   - Test interaction with mcnp-lattice-builder
   - Test interaction with mcnp-material-builder
   - Test interaction with mcnp-input-validator

3. **Documentation Review**
   - Ensure examples are complete
   - Verify code runs without errors
   - Check that references are accurate

4. **User Acceptance Testing**
   - Have users attempt various workflow types
   - Gather feedback on clarity
   - Refine based on actual usage

---

## REFERENCES

1. **Primary Source**: HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md
   - Section 1: Workflow Integration
   - Section 2.1: Template vs Programmatic
   - Section 3.2: Error Checking in Automation
   - Section 5.3: Automation Strategies

2. **Secondary Source**: COMPREHENSIVE_FINDINGS_SYNTHESIS.md
   - Part 9: Workflow Integration
   - Part 6: Template-Based Automation
   - Part 7: Programmatic Generation

3. **Implementation Guide**: SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md
   - Phase 2 priorities
   - Directory structure
   - Success criteria

---

**END OF REFINEMENT PLAN**

This plan provides a complete, executable roadmap for creating the **mcnp-workflow-integrator** skill. It can be implemented immediately following completion of Phase 1 skills.
