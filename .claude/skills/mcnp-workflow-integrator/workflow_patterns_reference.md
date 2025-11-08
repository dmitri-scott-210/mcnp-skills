# Workflow Patterns Reference

Comprehensive examples of multi-physics workflows for reactor analysis.

## Overview

This reference provides detailed implementations of common workflow patterns for MCNP-based reactor analysis, drawn from professional-grade research projects.

## Pattern 1: Linear Sequential Workflow (Burnup-to-Shutdown-Dose-Rate)

### Description

A complete **MCNP → ORIGEN → MCNP** workflow for shutdown dose rate calculations.

### Use Cases

- Decommissioning planning (dose rates for personnel safety)
- Maintenance scheduling (shutdown period dose estimates)
- Waste characterization (isotopic inventories)
- Regulatory compliance (dose limit verification)

### Complete Implementation

#### Stage 1: Neutron Transport Model

**Purpose**: Establish flux/power distributions during operation

**MCNP Input** (`neutron_transport.i`):
```
HTGR Core - Neutron Transport for Depletion
c
c CELLS
c
c Fuel assemblies (to be tracked in depletion)
1001 101 -10.8  -1001  u=14 vol=948.35  imp:n=1  $ Fuel kernel
1002 102  -1.1   1001 -1002  u=14 imp:n=1  $ Buffer
c ... (complete TRISO particle definition)
c
c SURFACES
c
1001 so 0.0250  $ Kernel radius
1002 so 0.0350  $ Buffer outer radius
c ... (complete geometry)
c
c MATERIALS
c
m101  $ UO2 kernel
     92235.00c  4.816186e-03
     92238.00c  1.932238e-02
      8016.00c  4.827713e-02
c ... (complete materials)
c
c DATA CARDS
c
kcode 10000 1.0 50 250
ksrc 0 0 0
c
c Tallies for depletion
f4:n 1001 1002 1003 1004 $ Flux in fuel cells
f7:n 1001 1002 1003 1004 $ Fission power in fuel cells
```

**Execution**:
```bash
mcnp6 i=neutron_transport.i n=neutron. tasks 16
```

**Key Outputs**:
- Cell-wise flux distributions (from F4 tally)
- Cell-wise power distributions (from F7 tally)
- Keff (for criticality validation)

#### Stage 2: Depletion Tracking

**Purpose**: Track isotopic evolution under irradiation

**Approach**: Use MOAA (MCNP-ORIGEN Activation Automation) or similar coupling tool

**Input Requirements**:
- Flux/power from MCNP (Stage 1)
- Initial material compositions
- Irradiation time steps
- Cell list for tracking

**MOAA Example** (conceptual - tool-specific):
```
# MOAA input (simplified)
MCNP_OUTPUT neutron.o
CELLS_TO_TRACK 1001 1002 1003 1004
IRRADIATION_TIME 100 days
TIME_STEPS 10  # 10-day intervals
COOLING_TIME 1 day
```

**Execution**:
```bash
moaa neutron_transport.i depletion_config
```

**Key Outputs**:
- Cell-wise isotopic inventories vs. time
- Actinide buildup (Pu-239, Pu-240, etc.)
- Fission product accumulation
- Structural activation

#### Stage 3: Decay Source Generation

**Purpose**: Calculate photon emission from decaying isotopes after shutdown

**Input**: Isotopic inventories from Stage 2 at shutdown time

**Processing Script** (`generate_decay_sources.py`):
```python
import origen_parser  # Tool-specific
import numpy as np

def generate_photon_sources(isotopic_inventory, decay_time_days):
    """
    Convert ORIGEN isotopic inventory to MCNP photon sources.

    Args:
        isotopic_inventory: dict {cell_id: {isotope: atoms}}
        decay_time_days: cooling time after shutdown

    Returns:
        SDEF card string for MCNP
    """
    # Decay isotopes to get gamma spectra
    gamma_sources = {}

    for cell_id, isotopes in isotopic_inventory.items():
        # Decay each cell's inventory
        decayed = decay_isotopes(isotopes, decay_time_days)

        # Get gamma spectrum (energy, intensity pairs)
        spectrum = calculate_gamma_spectrum(decayed)

        gamma_sources[cell_id] = {
            'spectrum': spectrum,
            'total_intensity': sum(s[1] for s in spectrum),
            'position': get_cell_center(cell_id)
        }

    # Build SDEF cards
    return build_sdef_cards(gamma_sources)


def build_sdef_cards(gamma_sources):
    """Build MCNP SDEF cards from gamma sources."""

    # Combine all spectra (weighted by intensity)
    all_energies = []
    all_probabilities = []

    total_intensity = sum(g['total_intensity'] for g in gamma_sources.values())

    # Energy distribution (combine all cells)
    for cell_id, source in gamma_sources.items():
        weight = source['total_intensity'] / total_intensity
        for energy, intensity in source['spectrum']:
            all_energies.append(energy)
            all_probabilities.append(intensity * weight)

    # Normalize probabilities
    prob_sum = sum(all_probabilities)
    all_probabilities = [p/prob_sum for p in all_probabilities]

    # Position distribution
    positions = [s['position'] for s in gamma_sources.values()]
    pos_probs = [s['total_intensity']/total_intensity for s in gamma_sources.values()]

    # Build SDEF
    sdef = "sdef par=p erg=d1 pos=d2\n"

    # Energy bins
    sdef += "si1  L  " + " ".join(f"{e:.4f}" for e in all_energies) + "\n"
    sdef += "sp1    " + " ".join(f"{p:.6e}" for p in all_probabilities) + "\n"

    # Position bins
    sdef += "si2  L  " + " ".join(f"({p[0]:.3f} {p[1]:.3f} {p[2]:.3f})" for p in positions) + "\n"
    sdef += "sp2    " + " ".join(f"{p:.6e}" for p in pos_probs) + "\n"

    return sdef


# Execute
inventory = parse_origen_output('depletion_output.txt')
sdef_cards = generate_photon_sources(inventory, decay_time_days=1)
print(sdef_cards)
```

**Execution**:
```bash
python generate_decay_sources.py > photon_sources.txt
```

#### Stage 4: Photon Transport Model

**Purpose**: Calculate dose rates from decay gammas

**MCNP Input** (`photon_transport.i`):
```
HTGR Core - Photon Transport for Shutdown Dose Rates
c
c CELLS (same geometry as neutron model)
c
1001 101 -10.8  -1001  u=14 imp:p=1  $ Fuel kernel (now photon source)
c ... (same geometry)
c
c External regions for dose mapping
9001 0  -9001  imp:p=1  $ Detector region 1 (near core)
9002 0  -9002  imp:p=1  $ Detector region 2 (maintenance area)
c
c SURFACES (same as neutron model)
c
c DATA CARDS
c
mode p  $ Photon-only transport
c
c Photon sources from decay (generated in Stage 3)
sdef par=p erg=d1 pos=d2
si1  L  0.511 0.662 1.173 1.332  $ Example energies (MeV)
sp1    2.3e-2 4.5e-2 3.1e-2 5.2e-3  $ Example probabilities
si2  L  (0 0 0) (10 0 0) (20 0 0)  $ Source positions
sp2    0.40 0.35 0.25  $ Position probabilities
c
c Dose rate tallies
f5:p  50 0 0  0.1  $ Point detector (x,y,z,radius)
f15:p 100 0 0  0.1  $ Another point
c
c Dose conversion factors (ANSI/ANS-6.1.1-1977, Sv/h per photon)
de15  0.01 0.03 0.05 0.07 0.1 0.15 0.2 0.3 0.4 0.5
      0.6 0.8 1.0 1.5 2.0 3.0 4.0 5.0 6.0 8.0 10.0
df15  3.67e-6 5.58e-7 2.28e-7 1.47e-7 1.15e-7 9.86e-8
      9.09e-8 8.83e-8 9.06e-8 9.63e-8 1.03e-7 1.18e-7
      1.33e-7 1.72e-7 2.11e-7 2.87e-7 3.62e-7 4.35e-7
      5.07e-7 6.46e-7 7.80e-7
c
c Mesh tally for spatial map
fmesh4:p geom=xyz origin=-100 -100 -50
         imesh=100 iints=20
         jmesh=100 jints=20
         kmesh=50  kints=10
         out=ij
```

**Execution**:
```bash
mcnp6 i=photon_transport.i n=photon. tasks 16
```

**Key Outputs**:
- Point detector dose rates (Sv/h)
- 3D dose rate map (MESHTAL)

#### Stage 5: Post-Processing

**Purpose**: Generate publication-quality results

**Processing Script** (`post_process_dose.py`):
```python
import matplotlib.pyplot as plt
import numpy as np

def parse_dose_rates(output_file):
    """Extract dose rates from MCNP output."""
    dose_rates = {}

    with open(output_file, 'r') as f:
        content = f.read()

    # Parse F5 tallies (point detectors)
    # (Simplified - actual parsing more complex)
    import re
    for match in re.finditer(r'tally\s+(\d+).*?value\s+=\s+(\S+)\s+rel err\s+=\s+(\S+)', content, re.DOTALL):
        tally_num = int(match.group(1))
        value = float(match.group(2))
        rel_err = float(match.group(3))

        dose_rates[f'detector_{tally_num}'] = {
            'dose_rate_Sv_h': value,
            'relative_error': rel_err
        }

    return dose_rates


def plot_dose_rates(dose_rates, regulatory_limit):
    """Generate dose rate comparison plot."""
    locations = list(dose_rates.keys())
    values = [dose_rates[loc]['dose_rate_Sv_h'] for loc in locations]
    errors = [v * dose_rates[loc]['relative_error'] for loc, v in zip(locations, values)]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(locations, values, yerr=errors, capsize=5, alpha=0.7)
    ax.axhline(regulatory_limit, color='r', linestyle='--',
               label=f'Regulatory Limit ({regulatory_limit} Sv/h)')

    ax.set_ylabel('Dose Rate (Sv/h)', fontsize=12)
    ax.set_xlabel('Location', fontsize=12)
    ax.set_title('Shutdown Dose Rates (1 day cooling)', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('dose_rates.png', dpi=300)
    print("Saved: dose_rates.png")


def process_mesh_tally(meshtal_file):
    """Process MESHTAL file for 3D visualization."""
    # Parse MESHTAL format
    # Create 2D slice plots or 3D visualization
    # (Implementation depends on visualization tool)
    pass


# Execute
dose_rates = parse_dose_rates('photon.o')
plot_dose_rates(dose_rates, regulatory_limit=0.025)  # 25 mSv/h example

print("\nDose Rate Results:")
for loc, data in dose_rates.items():
    print(f"{loc}: {data['dose_rate_Sv_h']:.3e} ± {data['relative_error']*100:.1f}% Sv/h")
```

**Execution**:
```bash
python post_process_dose.py
```

### Workflow Orchestration Script

**Complete workflow** (`run_b2sdr_workflow.sh`):
```bash
#!/bin/bash
# Complete Burnup-to-Shutdown-Dose-Rate workflow

set -e  # Exit on error

echo "========================================="
echo "Burnup-to-Shutdown-Dose-Rate Workflow"
echo "========================================="

# Stage 1: Neutron transport
echo ""
echo "Stage 1: Neutron Transport..."
mcnp6 i=neutron_transport.i n=neutron. tasks 16

# Check for fatal errors
if grep -q "fatal error" neutron.o; then
    echo "ERROR: Fatal error in neutron transport"
    exit 1
fi

# Stage 2: Depletion (tool-specific)
echo ""
echo "Stage 2: Depletion Tracking..."
moaa neutron_transport.i depletion_config

# Stage 3: Generate photon sources
echo ""
echo "Stage 3: Generating decay sources..."
python generate_decay_sources.py > photon_sources.txt

# Insert sources into photon transport input
sed -i '/c PHOTON SOURCES PLACEHOLDER/r photon_sources.txt' photon_transport.i

# Stage 4: Photon transport
echo ""
echo "Stage 4: Photon Transport..."
mcnp6 i=photon_transport.i n=photon. tasks 16

# Check for fatal errors
if grep -q "fatal error" photon.o; then
    echo "ERROR: Fatal error in photon transport"
    exit 1
fi

# Stage 5: Post-processing
echo ""
echo "Stage 5: Post-Processing..."
python post_process_dose.py

echo ""
echo "========================================="
echo "Workflow Complete!"
echo "========================================="
echo "Results:"
echo "  - Dose rate plot: dose_rates.png"
echo "  - Dose rate data: dose_rates.txt"
```

### Quality Assurance Checkpoints

**Between Each Stage**:

1. **After Stage 1**: Check keff convergence, lost particles
2. **After Stage 2**: Verify isotopic inventory magnitudes
3. **After Stage 3**: Validate source spectrum (energy distribution)
4. **After Stage 4**: Check dose rate statistical quality
5. **After Stage 5**: Compare to expected ranges, regulatory limits

---

## Pattern 2: Iterative Coupling (MCNP ↔ Thermal-Hydraulics)

### Description

Iterative coupling between MCNP (neutronics) and T/H code until convergence.

### Use Case

- Power-temperature feedback in reactors
- Keff convergence with temperature-dependent cross sections
- Fuel temperature distribution affecting reactivity

### Implementation

**Iteration Loop**:

```python
def coupled_iteration(max_iterations=20, tolerance=1e-4):
    """
    Iterative coupling MCNP ↔ T/H.

    Convergence criterion: keff changes < tolerance
    """
    keff_old = 1.0

    for iteration in range(max_iterations):
        print(f"\n=== Iteration {iteration+1} ===")

        # 1. Run MCNP with current temperatures
        print("Running MCNP...")
        run_mcnp()
        keff_new = extract_keff('mcnp_output.o')
        power_distribution = extract_power('mcnp_output.o')

        # 2. Run T/H with current power distribution
        print("Running T/H...")
        run_thermal_hydraulics(power_distribution)
        temperature_distribution = extract_temperatures('th_output.dat')

        # 3. Update MCNP materials with new temperatures
        print("Updating temperatures...")
        update_mcnp_materials(temperature_distribution)

        # 4. Check convergence
        delta_keff = abs(keff_new - keff_old)
        print(f"keff: {keff_new:.5f}, Δkeff: {delta_keff:.2e}")

        if delta_keff < tolerance:
            print(f"\nConverged after {iteration+1} iterations!")
            return keff_new

        keff_old = keff_new

    print("\nWARNING: Did not converge within max iterations")
    return keff_new
```

---

## Pattern 3: Parallel Parametric Study

### Description

Multiple independent MCNP runs with different parameters, executed in parallel.

### Use Case

- Uncertainty quantification (sampling parameter space)
- Design optimization (grid search over parameters)
- Benchmark suite (multiple test cases)

### Implementation

**SLURM Array Job**:

```bash
#!/bin/bash
#SBATCH --job-name=mcnp_parametric
#SBATCH --array=1-100  # 100 cases
#SBATCH --ntasks=8
#SBATCH --time=4:00:00

# Get case ID from array task ID
CASE_ID=$SLURM_ARRAY_TASK_ID

# Run this case
mcnp6 i=inputs/case_${CASE_ID}.i n=outputs/case_${CASE_ID}. tasks 8
```

**Python Generation of Cases**:

```python
import numpy as np

# Parameter sampling
np.random.seed(42)
n_cases = 100

for case_id in range(1, n_cases+1):
    # Sample parameters
    enrichment = np.random.uniform(3.0, 5.0)  # % U-235
    density = np.random.uniform(10.0, 11.0)    # g/cm³
    radius = np.random.uniform(0.40, 0.45)     # cm

    # Generate input
    create_input(
        filename=f'inputs/case_{case_id}.i',
        enrichment=enrichment,
        density=density,
        radius=radius
    )

print(f"Generated {n_cases} cases")
```

**Results Aggregation**:

```python
import pandas as pd
import glob

results = []

for output_file in glob.glob('outputs/case_*.o'):
    case_id = int(output_file.split('_')[1].split('.')[0])

    keff, uncertainty = extract_keff(output_file)

    # Get parameters for this case
    params = get_case_parameters(case_id)

    results.append({
        'case_id': case_id,
        'enrichment': params['enrichment'],
        'density': params['density'],
        'radius': params['radius'],
        'keff': keff,
        'uncertainty': uncertainty
    })

df = pd.DataFrame(results)
df.to_csv('parametric_results.csv', index=False)

# Sensitivity analysis
print("\nSensitivity Analysis:")
print(f"Enrichment correlation: {df['enrichment'].corr(df['keff']):.3f}")
print(f"Density correlation:    {df['density'].corr(df['keff']):.3f}")
print(f"Radius correlation:     {df['radius'].corr(df['keff']):.3f}")
```

---

## Pattern 4: Multi-Stage Validation Pipeline

### Description

Generation → Validation → Execution → Analysis with quality gates at each stage.

### Use Case

- Production workflows requiring high reliability
- Automated testing and continuous integration
- Large parameter studies where early error detection is critical

### Implementation

```python
from workflow_orchestrator import Workflow, InputGenerationStage, ValidationStage, MCNPExecutionStage, PostProcessingStage

# Define workflow with quality gates
workflow = Workflow("Multi-Stage Validation", working_dir=".")

# Stage 1: Generate inputs
workflow.add_stage(InputGenerationStage(
    script="scripts/create_inputs.py",
    description="Generate MCNP inputs from parameters"
))

# Stage 2: Validate inputs (QUALITY GATE)
workflow.add_stage(ValidationStage(
    input_files=["inputs/case1.i", "inputs/case2.i"],
    validation_script="scripts/validate.py",
    description="Validate MCNP syntax, cross-references, dimensions"
))

# Stage 3: Execute MCNP (only if validation passed)
workflow.add_stage(MCNPExecutionStage(
    input_files=["inputs/case1.i", "inputs/case2.i"],
    tasks=16,
    description="Run MCNP calculations"
))

# Stage 4: Post-process (QUALITY GATE)
workflow.add_stage(PostProcessingStage(
    script="scripts/post_process.py",
    validation_checks=[
        ('keff_range', lambda k: 0.9 < k < 1.1),
        ('statistical_quality', lambda stats: all(s < 0.10 for s in stats)),
        ('lost_particles', lambda lp: lp == 0)
    ],
    description="Extract results and validate"
))

# Run workflow (stops at first failure)
success = workflow.run()

if success:
    print("All stages completed successfully!")
else:
    print("Workflow failed - check logs")
```

**Validation Script** (`scripts/validate.py`):

```python
def validate_mcnp_input(filename):
    """
    Comprehensive validation of MCNP input.

    Returns:
        dict with 'valid' (bool) and 'issues' (list of strings)
    """
    issues = []

    with open(filename, 'r') as f:
        content = f.read()

    # 1. Check three-block structure
    if not has_three_block_structure(content):
        issues.append("Missing proper three-block structure")

    # 2. Check FILL arrays
    lattice_cells = extract_lattice_cells(content)
    for cell in lattice_cells:
        expected, actual = check_fill_dimensions(cell)
        if expected != actual:
            issues.append(
                f"Cell {cell['number']}: FILL mismatch - "
                f"expected {expected} elements, found {actual}"
            )

    # 3. Check cross-references
    defined_surfaces = extract_defined_surfaces(content)
    referenced_surfaces = extract_referenced_surfaces(content)
    undefined = referenced_surfaces - defined_surfaces
    if undefined:
        issues.append(f"Undefined surfaces: {undefined}")

    defined_materials = extract_defined_materials(content)
    referenced_materials = extract_referenced_materials(content)
    undefined = referenced_materials - defined_materials
    if undefined:
        issues.append(f"Undefined materials: {undefined}")

    # 4. Check numbering conflicts
    all_surface_nums = [s['number'] for s in extract_surfaces(content)]
    duplicates = find_duplicates(all_surface_nums)
    if duplicates:
        issues.append(f"Duplicate surface numbers: {duplicates}")

    return {
        'valid': len(issues) == 0,
        'issues': issues
    }
```

---

## Summary

These four patterns cover the majority of professional MCNP workflows:

1. **Linear Sequential**: Multi-physics coupling (B2SDR)
2. **Iterative Coupling**: Feedback between codes (MCNP ↔ T/H)
3. **Parallel Parametric**: Independent cases run concurrently
4. **Multi-Stage Validation**: Quality gates at each stage

**Key Principles Across All Patterns**:
- Modular stages (each does one thing well)
- Quality checkpoints (validate before proceeding)
- Error handling (graceful failure with informative messages)
- Reproducibility (version control, documentation)
- Automation (scripts, not manual steps)

**Next Steps**:
- Choose pattern matching your workflow
- Adapt scripts to your specific tools/codes
- Implement quality gates appropriate to your application
- Document workflow for reproducibility
