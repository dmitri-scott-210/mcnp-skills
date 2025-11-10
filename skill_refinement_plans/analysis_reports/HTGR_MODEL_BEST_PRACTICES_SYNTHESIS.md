# HTGR Reactor Model: Integration Analysis and Best Practices Synthesis

**Repository Analysis**: htgr-model-burnup-and-doserates
**Research Context**: Shutdown dose rate calculations for high-temperature gas-cooled reactors
**Publication**: Nuclear Science and Technology Open Research, 2024
**Authors**: Fairhurst-Agosta & Kozlowski, University of Illinois at Urbana-Champaign

---

## EXECUTIVE SUMMARY

This repository represents a professional-grade reactor modeling workflow demonstrating best practices for reproducible nuclear engineering research. The work introduces a novel shutdown dose rate calculation capability for HTGRs using the MCNP-ORIGEN Activation Automation (MOAA) tool, with explicit TRISO particle modeling enabled by MCNP repeated structures.

**Key Innovation**: The methodology explicitly models TRISO particles as decay radiation sources rather than using homogenized representations, enabled by MCNP's repeated structures feature combined with automated depletion calculations.

**Three Case Studies**:
1. **Verification**: Delayed heating calculation with simple geometry
2. **AGR-1**: TRISO-fueled Advanced Gas Reactor experiment in ATR (irradiation test)
3. **Micro**: μHTGR microreactor decommissioning strategy evaluation

This synthesis extracts overarching best practices applicable to professional MCNP reactor model development.

---

## 1. WORKFLOW INTEGRATION

### 1.1 Multi-Physics Coupling Architecture

**Burnup → Shutdown Dose Rate Workflow**:

```
[MCNP Neutronics]
      ↓
[MOAA Depletion Tracking]
      ↓ (isotopic inventory evolution)
[Decay Source Generation]
      ↓
[MCNP Photon Transport]
      ↓
[Dose Rate Calculation]
```

**Key Principles**:

1. **Sequential Physics Integration**: Neutron transport → depletion → photon transport
   - Neutron transport establishes power/flux distributions
   - MOAA tracks isotopic evolution in specific cells
   - Depleted isotopics become photon sources for shutdown analysis
   - Final photon transport yields dose rate maps

2. **Cell-Level Tracking**: Depletion calculated for individual cells
   - AGR-1: ~150 cells tracked (fuel, structural, graphite regions)
   - Micro: ~170 cells tracked (fuel assemblies, graphite blocks, reflectors)
   - Enables spatial resolution of isotopic distributions
   - Preserves double heterogeneity effects

3. **Time-Dependent Configurations**: Models evolve through operational history
   - Power levels change cycle-to-cycle
   - Control positions vary with burnup
   - Shutdown periods between cycles tracked
   - Complete irradiation history preserved

### 1.2 Data Flow Management

**External Data Integration**:

```
CSV Files (Experimental/Operational Data)
    ↓
Python Processing (pandas, numpy)
    ↓
MCNP Input Generation (Jinja2 templates or programmatic)
    ↓
MOAA Execution
    ↓
Results Post-Processing (matplotlib)
    ↓
Publication-Quality Outputs
```

**Data Sources** (AGR-1 example):
- `power.csv`: Lobe-specific power histories by cycle/timestep
- `oscc.csv`: Outer safety control cylinder rotation angles
- `neck_shim.csv`: Neck shim rod insertion conditions
- `MOAA_burnup_FIMA.csv`: Burnup results for validation

**Best Practices Demonstrated**:
- **Separation of Concerns**: Data, logic, and templates are distinct
- **Version Control**: CSV files are version-controlled with code
- **Provenance Tracking**: Each value traceable to experimental source
- **Reproducibility**: Complete workflow documented in README

### 1.3 Parametric Study Organization

**AGR-1 Parametric Study Structure**:
- 13 reactor cycles (138B through 145A)
- Each cycle: unique power, control positions, duration
- Automated generation of 13 MCNP input files from one template
- Time-averaged parameters from time-step data

**Automation Strategy**:
```python
# Time-weighted averaging for control positions
ave_angle = (angles * time_intervals).sum() / total_time
closest_discrete_angle = find_closest(available_angles, ave_angle)

# Time-weighted averaging for power
ave_power = (power * time_intervals).sum() / total_time
```

**Key Insight**: Continuous operational parameters → discrete MCNP configurations via intelligent averaging

---

## 2. MODEL DEVELOPMENT PROCESS

### 2.1 Dual Approach: Template vs. Programmatic

**Template-Based Approach (AGR-1)**:

**When to Use**:
- Large existing base model (ATR quarter-core: 13,727 lines)
- Experiment-specific geometry inserted into host reactor
- Base model stable, only parametric variations needed
- Multiple similar cases with different parameters

**Implementation Pattern**:
```python
# Jinja2 template with strategic insertion points
template_variables = {
    'cells': programmatically_generated_cells,
    'surfaces': programmatically_generated_surfaces,
    'materials': programmatically_generated_materials,
    'oscc_surfaces': cycle_specific_control_positions,
    'ne_cells': neck_shim_cells_northeast,
    'se_cells': neck_shim_cells_southeast
}

rendered_input = template.render(**template_variables)
```

**Advantages**:
- Preserves complex base geometry (ATR reactor core)
- Reduces duplication
- Enables rapid parametric variations
- Clear separation: static vs. dynamic content

**Programmatic Approach (Micro)**:

**When to Use**:
- Model built from scratch
- Regular/symmetric geometry patterns
- Need for algorithmic complexity (lattices, assemblies)
- Tight coupling between parameters

**Implementation Pattern**:
```python
# Modular function-based generation
def fuel(layer, assembly_number):
    surfaces = generate_surfaces(layer, assembly_number)
    cells = generate_cells(layer, assembly_number)
    materials = generate_materials(layer, assembly_number)
    return cells, surfaces, materials

# Build entire model programmatically
for layer in layers:
    for assembly in assemblies[layer]:
        if assembly.is_control():
            c, s, m = control(layer, assembly)
        else:
            c, s, m = fuel(layer, assembly)
        accumulate(c, s, m)
```

**Advantages**:
- Complete flexibility
- Algorithmic geometry generation (hexagonal arrays, repeated structures)
- Easy parameter studies (change one variable → regenerate)
- Version control of logic, not just geometry

### 2.2 TRISO Particle Modeling Strategy

**Multi-Level Universe Hierarchy**:

```
Level 1: TRISO Particle (5 layers)
    u=XX4: Kernel, Buffer, IPyC, SiC, OPyC

Level 2: Matrix Cell
    u=XX5: SiC matrix filling

Level 3: Particle Lattice (23×23×1)
    u=XX6: lat=1, cubic lattice of particles
    fill=-11:11 -11:11 0:0

Level 4: Compact Lattice (vertical stack)
    u=XX8: lat=1, fill=0:0 0:0 -335:335

Level 5: Fuel Channel
    u=XX1: Cylinder filled with compact lattice

Level 6: Hexagonal Assembly
    u=XX0: lat=2 (hexagonal), fill pattern
```

**Key Design Decisions**:

1. **Explicit Particle Geometry**: Each TRISO particle fully modeled
   - 5-layer structure preserved (kernel, buffer, IPyC, SiC, OPyC)
   - Double heterogeneity maintained
   - Enables particle-level source definition

2. **Lattice-Based Filling**: Repeated structures at multiple levels
   - Reduces input file size (pattern vs. enumeration)
   - Maintains geometric fidelity
   - Allows individual particle tracking for depletion

3. **Packing Fraction Calculations**: Physically consistent densities
   ```python
   vol_compact = π * R² * H  # Compact volume
   vol_triso = 4/3 * π * r³ * N_particles  # Total TRISO volume
   packing_fraction = vol_triso / vol_compact
   vol_cubic_cell = vol_triso / packing_fraction  # Lattice cell volume
   ```

4. **Material Variants**: Different TRISO designs in different capsules
   - Baseline, Variant1, Variant2, Variant3
   - Different layer thicknesses and densities
   - Different particle counts per compact

### 2.3 Numbering and Naming Conventions

**Systematic Numbering Schemes**:

**AGR-1 Convention** (Capsule-Stack-Compact):
```
Cell Numbers:
    90000 + capsule*1000 + stack*100 + 2*(compact-1)*10 + component
    Example: 91101 = Capsule 1, Stack 1, Compact 1, Component 1

Surface Numbers:
    9000 + capsule*100 + stack*10 + compact
    Example: 9111 = Capsule 1, Stack 1, Compact 1

Material Numbers:
    9000 + capsule*100 + stack*10 + compact
    Example: 9111 = Fuel in Capsule 1, Stack 1, Compact 1

Universe Numbers:
    capsule*100 + stack*10 + compact
    Example: 111 = Capsule 1, Stack 1, Compact 1
```

**Micro Convention** (Layer-Assembly):
```
Surface Numbers:
    assembly_number + component (201, 202, 203...)

Material Numbers:
    assembly_number + subregion (2011, 2012...)

Universe Numbers:
    assembly_number + function (2010, 2014, 2015...)
```

**Best Practices Extracted**:
- **Hierarchical Encoding**: Number encodes position/function
- **Deterministic**: Given location, number is calculable
- **Collision-Free**: Ranges allocated to prevent conflicts
- **Human-Readable**: Pattern discernible by inspection

### 2.4 Comment and Documentation Standards

**In-File Documentation** (from bench.template):
```
c     -------------------------------------------------------------------------
c
c     Case:  bench.1
c            cp /ANDROMEDA/ATR/MODELS/quarter/jhu  bench.1
c               (1) BOC 145A ATR fuel elements 6,7,8,9,10,11,12,13,14,15
c                           cells 60106-60315
c               (2) BOC 145A ATR fuel elements materials (m2106-m2315)
c
c     BOC 145A ATR FUEL IN ELEMENTS 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
c     THREE RADIAL REGIONS AND SEVEN AXIAL REGIONS
c     HOMOGENIZED FUEL ZONES FOR PLATES 1 - 4, 5 - 15, & 16 - 19
```

**Section Headers**:
```
c
c  ATR Fuel Element Cells (Northeast Lobe)
c        (210 total: 10 elements--3 radial zones--7 axial zones)
c        (atr fuel elements:  6, 7, 7, 8, 9, 10, 11, 12, 13, 14, 15)
```

**Inline Comments**:
```
60106 2106 7.969921E-02  1111  -1118   74  -29   53  100 -110 $Elem  6 RZ 1 AZ 1
```

**Best Practices**:
- **Header Block**: Model provenance, case description, key features
- **Section Organization**: Clear delineation of cell/surface/material blocks
- **Count Documentation**: "210 total: 10 elements--3 radial zones--7 axial zones"
- **Inline Annotation**: Every cell/surface has descriptive comment
- **Consistent Format**: `$Elem 6 RZ 1 AZ 1` pattern throughout

### 2.5 Version Control and Reproducibility

**Repository Structure**:
```
htgr-model-burnup-and-doserates/
├── README.md                    # Complete documentation
├── LICENSE                      # Legal framework
├── agr-1_research_article.xml   # Scientific context
├── agr-1/
│   ├── bench.template           # MCNP template (13,727 lines)
│   ├── create_inputs.py         # Generation script
│   ├── plots.py                 # Post-processing
│   ├── *.csv                    # Experimental data
│   └── mcnp/                    # Generated inputs
│       ├── bench_138B.i
│       ├── bench_139A.i
│       └── ...
└── micro/
    ├── input_definition.py      # Shared parameters
    ├── create_input_burnup.py   # Burnup model generator
    ├── create_input_sdr.py      # SDR model generator
    └── plots.py                 # Post-processing
```

**Reproducibility Features**:
1. **DOI Assignment**: Zenodo DOI for permanent citation
2. **Complete Data**: All input CSVs version-controlled
3. **Executable Scripts**: One-command regeneration
4. **Documentation**: README explains each file's role
5. **Publication Link**: Direct connection to peer-reviewed article
6. **Separation**: Generated files in subdirectories (mcnp/)

**Usage Pattern**:
```bash
# Regenerate all AGR-1 inputs
cd agr-1/
python create_inputs.py

# Regenerate micro burnup model
cd micro/
python create_input_burnup.py
```

---

## 3. QUALITY ASSURANCE

### 3.1 Physical Correctness Validation

**Multi-Level Validation Strategy**:

1. **Geometric Self-Consistency**:
   - Packing fraction calculations ensure particles fit in compacts
   - Lattice dimensions match physical dimensions
   - Volume cards (`vol=`) for tally normalization and verification

2. **Material Balance**:
   - Enrichment specifications from experimental data
   - Density values from material handbooks
   - Isotopic compositions sum to unity

3. **Benchmark Validation** (AGR-1):
   - Compared against experimental burnup measurements (MOAA_burnup_FIMA.csv)
   - Power history matched to ATR operational data
   - Control positions matched to experimental configurations

4. **Code-to-Code Verification**:
   - MCNP results compared to ORIGEN standalone
   - Verification exercise compares reference vs. repeated structures

### 3.2 Error Checking in Automation

**Python Script Quality Checks**:

```python
# 1. Range validation
assert 0 <= packing_fraction <= 1, "Invalid packing fraction"

# 2. Physical consistency
if particle == 'baseline':
    assert n_particles[particle] == 4154, "Particle count mismatch"

# 3. Data completeness
required_cycles = ['138B', '139A', '139B', ...]
assert all(cycle in power_df['Cycle'].values for cycle in required_cycles)

# 4. Geometric constraints
assert vol_triso_tot < vol_compact, "Overpacked compact"

# 5. Surface number uniqueness
all_surfaces = set()
for s in generated_surfaces:
    assert s not in all_surfaces, f"Duplicate surface {s}"
    all_surfaces.add(s)
```

**Best Practices Demonstrated**:
- **Defensive Programming**: Validate assumptions before proceeding
- **Early Failure**: Catch errors during generation, not runtime
- **Informative Messages**: Error messages identify the problem
- **Consistency Checks**: Cross-validate related parameters

### 3.3 Testing and Verification Strategies

**Verification Hierarchy**:

1. **Unit Testing** (Implicit in functions):
   ```python
   def compact_surfaces(s, thick, n_particles):
       """Generate TRISO compact surfaces.

       Verification:
       - Radii increase monotonically (each layer outside previous)
       - Final radius matches physical compact dimension
       - Surface numbers follow numbering convention
       """
       radii = calculate_radii(thick)
       assert all(radii[i] < radii[i+1] for i in range(len(radii)-1))
       return surfaces
   ```

2. **Integration Testing** (Verification case study):
   - Simple geometry with known answer
   - Compare reference model vs. repeated structures
   - Validates MOAA workflow end-to-end

3. **Regression Testing**:
   - Generated files compared to reference versions
   - Ensures code changes don't break existing cases

4. **Physical Validation**:
   - Results compared to experimental measurements
   - Plots generated for visual inspection
   - Dose rate magnitudes checked against expectations

### 3.4 Documentation of Assumptions

**Explicit Assumption Documentation**:

From README:
```
"Be aware that the files included here allow to reproduce (for the most part)
the results from the publication. However, some of the software developed for
this publication should be treated as export control and it is not included in
this repository."
```

From create_inputs.py:
```python
# Time-weighted averaging assumption:
# Control positions vary continuously during cycle
# MCNP model uses single average position per cycle
ave_angle = (angle * time_interval).sum() / cum_time[-1]
angle = find_closest_value(available_angles, ave_angle)
```

**Best Practices**:
- **Limitations Stated**: Missing software acknowledged
- **Approximations Documented**: Averaging methods explained
- **Physical Basis**: Packing fraction calculations shown
- **Source Attribution**: Experimental data sources cited

---

## 4. SCALABILITY PATTERNS

### 4.1 Handling Large-Scale Geometries

**Complexity Metrics**:

**AGR-1 Model**:
- Base model: 13,727 lines
- Generated additions: ~5,000 lines
- Total: ~18,400 lines per input
- 6 capsules × 3 stacks × 4 compacts × 5 TRISO layers = 360 fuel regions
- 13 cycle-specific inputs generated
- ~150 cells tracked for depletion

**Micro Model**:
- Fully programmatic generation
- 4 axial layers × 36 assemblies = 144 assembly positions
- Each assembly: hexagonal lattice of fuel/coolant channels
- Each fuel channel: vertical stack of TRISO compacts
- Each compact: 23×23 particle lattice
- ~170 cells tracked for depletion

**Scalability Strategies**:

1. **Hierarchical Universe Nesting**:
   - Recursive filling reduces complexity
   - Each level encapsulates lower-level detail
   - Pattern reuse across assemblies

2. **Lattice-Based Repetition**:
   - `lat=1` (cubic) and `lat=2` (hexagonal) extensively used
   - Avoids explicit enumeration of thousands of cells
   - Fill patterns define complex assemblies concisely

3. **Programmatic Generation**:
   - Loops generate repetitive geometry
   - Functions encapsulate assembly logic
   - Parameters drive variations

4. **Template Composition**:
   - Base model + programmatic insertions
   - Separation of static and dynamic content
   - Enables manageable 13,000+ line files

### 4.2 Computational Complexity Management

**Depletion Cell Selection**:

**Strategy**: Track only cells that matter for physics

**AGR-1**:
- Fuel cells (kernel): 72 cells (6×3×4 = capsules × stacks × compacts)
- Structural steel: ~30 cells (capsule walls, supports)
- Graphite spacers: ~20 cells
- Borated graphite holders: ~10 cells
- Hafnium shroud: ~10 cells
- **Total: ~150 cells** (not thousands)

**Micro**:
- Fuel assemblies: ~36 cells (layer-specific tracking)
- Graphite blocks: ~90 cells (moderator regions)
- Reflectors: ~6 cells (radial layers)
- **Total: ~170 cells**

**Key Insight**:
- Homogenize where appropriate (TRISO layers below kernel)
- Track heterogeneity where it matters (fuel vs. moderator)
- Balance fidelity and computational cost

**Variance Reduction**:
- Not explicitly shown in repository (likely in proprietary MOAA software)
- Repeated structures enable efficient particle tracking
- Universe-based importance maps possible

### 4.3 Parameter Study Enablement

**AGR-1 Parametric Workflow**:

```python
# One script generates 13 related cases
cycles = ['138B', '139A', '139B', ..., '145A']

for cycle in cycles:
    # Extract cycle-specific data
    power = power_by_cycle[cycle]
    oscc = oscc_by_cycle[cycle]
    neck_shim = neck_by_cycle[cycle]

    # Time-average parameters
    ave_power = time_weighted_average(power, time_intervals)
    ave_oscc = time_weighted_average(oscc, time_intervals)
    ave_neck = mode(neck_shim)  # Most common state

    # Render template
    input_file = template.render(
        power=ave_power,
        oscc_surfaces=oscc_surfaces[cycle],
        neck_cells=neck_cells[cycle]
    )

    # Write to file
    write(f'bench_{cycle}.i', input_file)
```

**Parameter Study Best Practices**:
- **Single Source of Truth**: One template/script for all cases
- **Automated Variation**: Loop over parameter values
- **Traceable**: Each output tagged with parameters
- **Consistent**: Same logic applied to all cases
- **Documented**: Parameter sources documented in README

**Extensibility**:
- Add new cycle: add row to CSV, re-run script
- Change averaging method: modify one function, regenerate all
- Vary geometry: modify template/function, regenerate all

### 4.4 Multi-Physics Coupling Scalability

**Sequential Coupling Architecture**:

```
MCNP (neutron, steady-state)
    ↓ (cell-wise power/flux)
MOAA/ORIGEN (depletion)
    ↓ (cell-wise isotopics)
MCNP (photon, steady-state)
    ↓ (spatial dose rates)
Post-Processing (visualization)
```

**Scalability Features**:

1. **Loose Coupling**: Each code runs independently
   - MCNP output → MOAA input
   - MOAA output → MCNP source definition
   - No online coupling overhead

2. **Cell-Level Granularity**: Physics tracked per cell
   - Enables spatial resolution
   - Avoids global homogenization
   - Preserves important gradients

3. **Parallel-Ready**: Independent cycle calculations
   - Each cycle is separate MOAA run
   - Can be parallelized across nodes
   - Results post-processed together

4. **Data Management**:
   - CSV files for time-dependent parameters
   - HDF5/binary for large MCNP outputs
   - Python for data processing pipeline

---

## 5. OVERALL BEST PRACTICES SYNTHESIS

### 5.1 Input File Organization Principles

**Three-Block Structure Adherence**:
```
TITLE CARD
c COMMENT BLOCK with provenance

c
c CELLS BLOCK
c
[cell definitions]

c
c SURFACES BLOCK
c
[surface definitions]

c
c MATERIALS BLOCK
c
[material definitions]
[thermal scattering]

c
c DATA CARDS
c
[source, tallies, physics]
```

**Organization Within Blocks**:

1. **Logical Grouping**:
   - Fuel elements together
   - Structural components together
   - Reflector regions together
   - Control systems together

2. **Hierarchical Ordering**:
   - Innermost regions first
   - Outward progression
   - Boundary cells last

3. **Consistent Spacing**:
   - Blank comment lines between sections
   - Aligned columns for readability
   - Indentation for continued lines

4. **Section Headers**:
   ```
   c
   c  ATR Fuel Element Cells (Northeast Lobe)
   c        (210 total: 10 elements--3 radial zones--7 axial zones)
   c
   ```

### 5.2 Naming and Numbering Conventions

**Systematic Numbering Philosophy**:

1. **Hierarchical Encoding**:
   - Most significant digits = major component (capsule, layer)
   - Middle digits = subcomponent (stack, assembly)
   - Least significant digits = detail (compact, element)

2. **Range Allocation**:
   - 60000s: ATR fuel elements
   - 90000s: AGR-1 experiment geometry
   - 2000s-5000s: Micro fuel assemblies (by layer)
   - 9000s: Micro reflectors and boundaries

3. **Consistent Offsets**:
   - Cells: base + 0, +1, +2... for components
   - Surfaces: matches cell number convention
   - Materials: matches cell number convention
   - Universes: condensed version of cell number

4. **Self-Documenting**:
   - Cell 91141: Capsule 1, Stack 1, Compact 4, Component 1
   - Immediately identifies position in geometry

**Universe Numbering Strategy**:

```
Fuel TRISO Particle: u=XXX4 (kernel, buffer, IPyC, SiC, OPyC)
Matrix Cell:         u=XXX5 (SiC matrix)
Particle Lattice:    u=XXX6 (23×23 array of particles)
Matrix Lattice:      u=XXX7 (filler cell)
Compact Lattice:     u=XXX8 (vertical stack)
Fuel Channel:        u=XXX1 (filled cylinder)
Graphite Block:      u=XXX2 (solid hex)
Coolant Channel:     u=XXX3 (hollow hex)
Assembly:            u=XXX0 (hexagonal lattice)
```

**Best Practice**: Last digit encodes function, prefix encodes location

### 5.3 Automation Strategies

**When to Automate**:

✅ **Automate When**:
- More than 3 similar cases needed
- Parameters change frequently
- Geometry follows algorithmic pattern
- Human error risk in manual entry
- Reproducibility critical

❌ **Don't Automate When**:
- One-time model
- Highly irregular geometry
- Automation effort > manual effort
- Debugging complexity outweighs benefit

**Automation Toolchain**:

1. **Python** for generation logic:
   - Pandas for data manipulation
   - NumPy for calculations
   - Jinja2 for templating
   - Matplotlib for visualization

2. **CSV** for external data:
   - Human-readable
   - Version-control friendly
   - Easy to edit in spreadsheets
   - Pandas-compatible

3. **Templates** for stable base geometry:
   - Jinja2 for complex logic
   - Simple string formatting for basic cases
   - Preserve original model structure

4. **Functions** for reusable patterns:
   - Encapsulate assembly logic
   - Return cells, surfaces, materials as group
   - Parameterize by position/variant

**Automation Quality Checklist**:

```python
def generate_assembly(layer, number, variant):
    """Generate MCNP geometry for fuel assembly.

    Quality checks:
    - Validate input parameters (range, type)
    - Calculate derived quantities (packing fraction, volumes)
    - Check physical constraints (PF < 1, radii increase)
    - Use consistent numbering scheme
    - Include comments in output
    - Return structured data (not just string)
    """
    validate_inputs(layer, number, variant)

    cells = generate_cells(...)
    surfaces = generate_surfaces(...)
    materials = generate_materials(...)

    assert_physical_consistency(cells, surfaces, materials)

    return cells, surfaces, materials
```

### 5.4 Maintainability Patterns

**Code Organization**:

```
project/
├── input_definition.py      # Shared parameters, constants
├── create_input_burnup.py   # Burnup model generator
├── create_input_sdr.py      # SDR model generator
├── plots.py                 # Post-processing functions
├── power.csv                # External data
└── mcnp/                    # Generated outputs (not version-controlled)
```

**Separation of Concerns**:
- **Parameters**: Central definition file
- **Logic**: Generation scripts
- **Data**: CSV files
- **Outputs**: Separate directory

**Maintainability Best Practices**:

1. **Don't Repeat Yourself (DRY)**:
   ```python
   # BAD: Repeated code
   surfaces1 = f"{n}01 so 0.0250 $ Kernel"
   surfaces2 = f"{n}01 so 0.0250 $ Kernel"

   # GOOD: Function
   def kernel_surface(n):
       return f"{n}01 so 0.0250 $ Kernel"
   ```

2. **Modular Functions**:
   - Each function has single responsibility
   - `fuel()` separate from `control()`
   - `compact_surfaces()` separate from `compact_cells()`

3. **Consistent Interfaces**:
   ```python
   # All assembly functions return same structure
   cells, surfaces, materials = fuel(layer, number)
   cells, surfaces, materials = control(layer, number)
   cells, surfaces, materials = reflector()
   ```

4. **Extensive Comments**:
   - Function docstrings
   - Inline comments for complex logic
   - Comments in generated MCNP output

5. **Version Control**:
   - Git for all source files
   - `.gitignore` for generated outputs
   - Meaningful commit messages
   - Tagged releases corresponding to publication

### 5.5 Reproducibility Requirements

**Essential Elements** (demonstrated in repository):

1. **Complete Data**:
   - ✅ All input CSVs included
   - ✅ Generation scripts included
   - ✅ README with instructions
   - ⚠️ MOAA software not included (export control)

2. **Executable Workflow**:
   ```bash
   # User can reproduce results
   python create_inputs.py  # Generates all MCNP inputs
   # (Run MOAA - not included)
   python plots.py          # Post-process results
   ```

3. **Documentation**:
   - ✅ README explains repository structure
   - ✅ Research article provides scientific context
   - ✅ Code comments explain logic
   - ✅ DOI provides permanent identifier

4. **Version Tracking**:
   - ✅ Git repository with history
   - ✅ Zenodo release with DOI
   - ✅ Article version noted (version 2)
   - ✅ Software versions in publication

5. **Validation Data**:
   - ✅ Experimental data (CSVs) included
   - ✅ Benchmark results (MOAA_burnup_FIMA.csv)
   - ✅ Plots comparing calculation vs. experiment

**Reproducibility Checklist**:

```markdown
- [ ] All input data version-controlled
- [ ] Generation scripts provided
- [ ] Dependencies documented (requirements.txt or equivalent)
- [ ] Instructions for use (README)
- [ ] Expected outputs described
- [ ] Validation data included
- [ ] Software versions recorded
- [ ] Permanent identifier (DOI)
- [ ] License specified
- [ ] Citation information provided
```

### 5.6 Publication-Quality Standards

**From Repository to Publication**:

1. **Data Provenance**:
   - CSV files → Pandas DataFrames → MCNP inputs
   - Every number traceable to source
   - Experimental references cited

2. **Visualization**:
   ```python
   # Publication-quality plots
   for cycle in cycles:
       plt.figure()
       plt.step(time, power, where='post', label=key)
       plt.ylabel('Power [MW]')
       plt.xlabel('Time [h]')
       plt.savefig(f'power_cycle_{cycle}.png')
   ```
   - Automated figure generation
   - Consistent formatting
   - Labeled axes with units
   - Version-controlled plotting code

3. **Results Documentation**:
   - Printed output from scripts (power history, cell lists)
   - Allows verification before MCNP runs
   - Captures calculated parameters for manuscript

4. **Peer Review Readiness**:
   - Complete repository can be shared with reviewers
   - Reviewers can reproduce calculations
   - Addresses reproducibility requirements of journals
   - DOI allows permanent citation

---

## 6. LESSONS FOR MCNP SKILLS DEVELOPMENT

### 6.1 Teaching Workflow Integration

**Skills Should Teach**:

1. **Multi-Physics Thinking**:
   - Neutron transport → depletion → photon transport
   - Cell-level tracking for spatial resolution
   - Time-dependent configurations

2. **Data Integration**:
   - CSV → Pandas → MCNP
   - Experimental data drives model parameters
   - Automation scripts process data

3. **Workflow Orchestration**:
   - Generation → Execution → Post-processing
   - Each stage with quality checks
   - Reproducible pipeline

### 6.2 Template vs. Programmatic Guidance

**Decision Framework**:

| Factor | Template | Programmatic |
|--------|----------|--------------|
| **Base Model** | Large existing | Built from scratch |
| **Variations** | Parametric changes | Structural changes |
| **Complexity** | Stable base geometry | Algorithmic geometry |
| **Flexibility** | Limited to template variables | Complete freedom |
| **Learning Curve** | Lower (if template exists) | Higher |
| **Best For** | Experiment in host reactor | New reactor design |

**Teaching Approach**:
- Show **both** approaches
- AGR-1 as template example
- Micro as programmatic example
- Explain when to use each

### 6.3 Repeated Structures Mastery

**Critical Skill for Modern Reactor Modeling**:

The TRISO particle modeling demonstrates the power of repeated structures:
- 6 levels of universe nesting
- Cubic and hexagonal lattices
- Fill patterns with mixed universes
- Transform cards for assembly positioning

**Skills Must Teach**:
1. Universe hierarchy design
2. Lattice types (`lat=1` vs `lat=2`)
3. Fill syntax and ranges
4. Transform applications
5. Debugging strategies (lost particles in universes)

### 6.4 Automation Best Practices

**Core Automation Principles**:

1. **Separation of Concerns**:
   - Data (CSV) ≠ Logic (Python) ≠ Templates (Jinja2)

2. **Defensive Programming**:
   - Validate inputs before generation
   - Check physical constraints
   - Assert expected properties

3. **Maintainability**:
   - Functions over copy-paste
   - Consistent naming
   - Extensive comments

4. **Reproducibility**:
   - Version control everything
   - Document dependencies
   - Provide usage examples

### 6.5 Quality Assurance Integration

**Multi-Level Validation**:

1. **Generation-Time**:
   - Python assertions check constraints
   - Physical consistency validated

2. **Pre-Execution**:
   - Visual inspection of geometry (MCNP plotter)
   - Manual review of generated inputs

3. **Post-Execution**:
   - Compare to experimental data
   - Check expected magnitudes
   - Verify conservation laws

4. **Benchmark**:
   - Code-to-code comparisons
   - Analytical limits checked
   - Published benchmark cases

---

## 7. KEY TAKEAWAYS FOR PROFESSIONAL MCNP MODELING

### 7.1 The Philosophy of Professional Modeling

This repository exemplifies a **professional engineering workflow**, not just academic exercises:

1. **Purpose-Driven**: Solves real engineering problem (decommissioning strategy)
2. **Publication-Ready**: Peer-reviewed, DOI-assigned, reproducible
3. **Industry-Relevant**: Microreactor decommissioning is practical concern
4. **Rigorously Validated**: Experimental data, benchmarks, verification
5. **Maintainable**: Future researchers can extend the work
6. **Documented**: Complete provenance and methodology

### 7.2 Complexity Management

**Principle**: Complexity is managed through **hierarchy and automation**

- **Geometric Hierarchy**: 6-level universe nesting manages TRISO complexity
- **Code Hierarchy**: Functions → Scripts → Workflows
- **Data Hierarchy**: Raw CSV → Processed → Parameters → MCNP input
- **Automation**: 13,000+ line files generated from concise logic

**Anti-Pattern Warning**: Manually editing 18,000-line MCNP files is **not scalable**

### 7.3 Reproducibility as a Core Value

**Reproducibility is not optional** for professional work:

- Enables peer review
- Allows future extensions
- Builds trust in results
- Required by funding agencies
- Expected by journals

**Implementation**:
- Version control (Git)
- Permanent identifiers (DOI)
- Complete data (CSV files)
- Executable scripts (Python)
- Clear documentation (README)

### 7.4 Integration with Broader Ecosystem

**Professional MCNP work exists in a larger context**:

- MCNP ↔ ORIGEN coupling (depletion)
- Python ecosystem (Pandas, NumPy, Matplotlib)
- Version control (Git)
- Publication platforms (Zenodo, journals)
- Experimental programs (ATR, microreactors)

**Skills must teach**: Integration, not just isolated MCNP syntax

### 7.5 The Path from Student to Professional

**Student Models**:
- Single input file
- Manually typed
- One calculation
- Maybe a plot

**Professional Models** (this repository):
- Automated generation
- Parametric studies (13 cases)
- Multi-physics workflow
- Publication-quality outputs
- Reproducible pipeline
- Version-controlled
- Validated against experiments
- Documented for others

**Skills Goal**: Bridge this gap systematically

---

## 8. RECOMMENDATIONS FOR MCNP SKILLS IMPLEMENTATION

### 8.1 Skill Structure Recommendations

1. **mcnp-template-generator** (new skill):
   - Create Jinja2 templates from MCNP inputs
   - Identify parametric sections
   - Generate multiple cases from one template
   - **Example**: AGR-1 workflow

2. **mcnp-programmatic-generator** (new skill):
   - Build MCNP inputs from scratch using Python
   - Hierarchical geometry generation
   - Universe and lattice automation
   - **Example**: Micro workflow

3. **mcnp-repeated-structures-builder** (enhanced):
   - Multi-level universe hierarchy design
   - Lattice types and fill patterns
   - Transform applications
   - TRISO particle modeling
   - **Example**: Both AGR-1 and Micro TRISO models

4. **mcnp-workflow-integrator** (new skill):
   - Multi-physics coupling patterns
   - Data pipeline design (CSV → MCNP → Results → Plots)
   - Quality assurance checkpoints
   - Reproducibility requirements

5. **mcnp-depletion-modeler** (new skill):
   - ORIGEN/MCNP coupling
   - Cell selection for tracking
   - Burnup → SDR workflow
   - Source definition from depleted isotopics

### 8.2 Documentation Enhancements

**Add to Each Skill**:

```markdown
## Professional Workflow Context

This skill is part of a larger professional modeling workflow:
- [Diagram showing where this skill fits]
- Integration points with other skills
- Real-world applications

## Example: HTGR Shutdown Dose Rate Study

[Reference to this repository as exemplar]
- How this skill was used
- Integration with other skills
- Quality assurance practices
```

### 8.3 Training Examples

**Use This Repository for**:

1. **Case Study Analysis**:
   - Students analyze the workflow
   - Identify best practices
   - Document the integration patterns

2. **Hands-On Exercises**:
   - Modify AGR-1 template for different parameters
   - Add a new capsule to the model
   - Generate a new micro assembly variant

3. **Quality Assurance Practice**:
   - Review generated files for correctness
   - Implement validation checks
   - Compare to reference outputs

### 8.4 Teaching Progression

**Beginner** (single input files):
- Basic MCNP syntax
- Simple geometries
- Manual input creation

**Intermediate** (template-based):
- Jinja2 templating
- Parametric studies
- CSV data integration
- **Example**: Simplified AGR-1 model

**Advanced** (programmatic):
- Full Python generation
- Multi-level universes
- Repeated structures mastery
- Workflow automation
- **Example**: Simplified Micro model

**Professional** (integrated workflows):
- Multi-physics coupling
- Reproducibility engineering
- Publication-quality outputs
- **Example**: Complete HTGR SDR study

---

## 9. CONCLUSION

This repository represents a **gold standard** for professional MCNP reactor modeling:

- **Scientifically Rigorous**: Peer-reviewed publication
- **Computationally Sophisticated**: Multi-level universes, TRISO particles
- **Methodologically Sound**: Experimental validation, benchmarking
- **Technologically Modern**: Python automation, version control, DOI
- **Pedagogically Valuable**: Multiple patterns demonstrated
- **Practically Relevant**: Addresses real decommissioning challenges

**Core Philosophy**:
> Professional reactor modeling requires integration of physics, computation, automation, validation, and documentation in a reproducible workflow.

**The skills should teach** not just MCNP syntax, but this **integrated professional practice**.

---

## APPENDIX: Quick Reference

### File Organization Pattern
```
project/
├── README.md                 # Always include
├── LICENSE                   # Always include
├── data/                     # External data (CSV, etc.)
├── templates/                # Jinja2 templates (if used)
├── scripts/                  # Python generation scripts
│   ├── input_definition.py  # Shared parameters
│   ├── create_input.py      # Main generator
│   └── plots.py             # Post-processing
└── outputs/                  # Generated files (gitignored)
```

### Numbering Convention Template
```
CATEGORY_REGION_COMPONENT

Examples:
- Cells:     CRSSS where C=Category, R=Region, SSS=Subregion
- Surfaces:  CRSSS matching cell numbers
- Materials: CRSSS matching cell numbers
- Universes: U=CRS (condensed)
```

### Generation Script Template
```python
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader

# 1. Load external data
data = pd.read_csv('data.csv')

# 2. Process data
processed = process(data)

# 3. Generate geometry
cells, surfaces, materials = generate_geometry(processed)

# 4. Render template (if using)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.inp')
output = template.render(cells=cells, surfaces=surfaces, materials=materials)

# 5. Write output
with open('output/input.i', 'w') as f:
    f.write(output)

# 6. Validate
validate(output)
```

### Quality Checklist
- [ ] All numbers traceable to source
- [ ] Physical constraints validated
- [ ] Numbering convention followed
- [ ] Comments on all cells/surfaces
- [ ] Volume cards for normalization
- [ ] Material compositions sum to 1
- [ ] Geometry visualized (plotter)
- [ ] Version controlled
- [ ] README documents usage
- [ ] Reproducible by others

---

**END OF SYNTHESIS**

**Document Prepared**: 2025-01-07
**Repository Analyzed**: htgr-model-burnup-and-doserates
**Purpose**: Extract best practices for MCNP skills development
**Status**: Complete integration analysis
