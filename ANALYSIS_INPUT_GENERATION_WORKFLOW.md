# COMPREHENSIVE ANALYSIS: MCNP INPUT GENERATION WORKFLOW
## AGR-1 HTGR Burnup and Dose Rates Model

**Date:** 2025-11-07
**Analysis Focus:** Automated input generation for multi-cycle reactor simulations
**Example:** /example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/

---

## EXECUTIVE SUMMARY

The AGR-1 example demonstrates a sophisticated **data-driven input generation workflow** for creating multiple MCNP input files representing different reactor operating cycles. The workflow uses:
- **Jinja2 templating** for parameterized input generation
- **Pandas-based CSV parsing** for time-dependent operational data
- **Programmatic geometry generation** (TRISO particles, lattices)
- **Time-averaging algorithms** for control drum positions and neck shim states
- **Automated file naming and organization** for burnup sequences

This is a production-grade example of how to manage complex reactor models with time-dependent configurations.

---

## 1. AUTOMATION WORKFLOW

### 1.1 Overall Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT DATA SOURCES                       │
├─────────────────────────────────────────────────────────────┤
│ • bench.template (13,727 lines - base MCNP model)          │
│ • power.csv (power history by lobe and timestep)           │
│ • oscc.csv (outer shim control cylinder angles)            │
│ • neck_shim.csv (neck shim rod insertion states)           │
│ • MOAA_burnup_FIMA.csv (burnup results for plotting)       │
│ • Hardcoded: TRISO particle specifications, capsule data   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               PYTHON SCRIPT: create_inputs.py               │
├─────────────────────────────────────────────────────────────┤
│ 1. Define hardcoded geometry functions (TRISO, lattices)   │
│ 2. Generate static geometry (cells, surfaces, materials)   │
│ 3. Read CSV files → Parse by cycle                         │
│ 4. Compute time-averaged parameters per cycle              │
│ 5. Select control positions (drums, shims) per cycle       │
│ 6. Render Jinja2 template → Write cycle-specific inputs    │
│ 7. Generate plots for QA (power, OSCC, neck shim)          │
│ 8. Print burnup summary and irradiation schedule           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT FILES GENERATED                    │
├─────────────────────────────────────────────────────────────┤
│ mcnp/                                                       │
│   ├── bench_138B.i    (Cycle 138B input)                   │
│   ├── bench_139A.i    (Cycle 139A input)                   │
│   ├── ...             (13 cycle-specific inputs)           │
│   ├── bench_145A.i    (Final cycle)                        │
│   └── sdr-agr.i       (MOAA depletion model)               │
│                                                             │
│ Plots (PNG):                                                │
│   ├── oscc_cycle_138B.png, ..., oscc_cycle_145A.png        │
│   ├── neck_cycle_138B.png, ..., neck_cycle_145A.png        │
│   ├── power_cycle_138B.png, ..., power_cycle_145A.png      │
│   └── burnup_axial.png                                     │
│                                                             │
│ Console Output:                                             │
│   └── Irradiation schedule (MOAA burnup input format)      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Template Processing Mechanism

**Template Engine:** Jinja2 (industry-standard Python templating)

**Template Structure:**
```
bench.template (13,727 lines)
├── Lines 1-620: Static ATR reactor geometry (fuel elements, flux traps)
├── Line 621: {{ne_cells}} ← Neck shim cells (NE quadrant) - DYNAMIC
├── Lines 622-673: Static NE water cells
├── Line 674: {{se_cells}} ← Neck shim cells (SE quadrant) - DYNAMIC
├── Lines 675-1429: Static geometry (fuel, targets, B-holes, I-holes)
├── Line 1430: {{cells}} ← AGR-1 capsule cells (TRISO compacts) - DYNAMIC
├── Lines 1431-1781: Static geometry (remaining structures)
├── Line 1782: {{oscc_surfaces}} ← Control drum surfaces - DYNAMIC
├── Lines 1783-2213: Static surfaces (lobes, fuel regions, drums)
├── Line 2214: {{surfaces}} ← AGR-1 capsule surfaces (TRISO) - DYNAMIC
├── Lines 2215-13602: Static surfaces and data cards
└── Line 13603: {{materials}} ← AGR-1 fuel kernel materials - DYNAMIC
```

**Template Rendering (Lines 888-900):**
```python
env = Environment(loader=FileSystemLoader('./'))
for cycle in cycles:
    template = env.get_template('bench.template')
    full_input = template.render(
        cells=cells,                        # AGR-1 capsule cells (static)
        surfaces=surfaces,                  # AGR-1 capsule surfaces (static)
        materials=materials,                # AGR-1 materials (static)
        oscc_surfaces=oscc_surfaces[cycle], # Control drum surfaces (cycle-specific)
        ne_cells=ne_cells[cycle],           # NE neck shims (cycle-specific)
        se_cells=se_cells[cycle],           # SE neck shims (cycle-specific)
    )
    with open(f'mcnp/{filename[cycle]}', 'w+') as f:
        f.write(full_input)
```

**Key Insight:** Only 6 template variables, but 3 are cycle-dependent (OSCC drums, NE/SE neck shims). The AGR-1 experiment geometry is static across all cycles.

### 1.3 Programmatic Geometry Generation

**TRISO Particle Geometry (Lines 27-48):**
```python
def compact_surfaces(s, thick, n_particles):
    """
    Generate MCNP surface cards for TRISO particle layers and lattice unit.

    Args:
        s: Surface number prefix (e.g., 9111 for capsule 1, stack 1, compact 1)
        thick: Layer thicknesses [kernel_radius, buffer, IPyC, SiC, OPyC] (µm)
        n_particles: Number of particles per compact

    Returns:
        MCNP surface cards (spheres for TRISO, RPP for lattice unit)
    """
    # Calculate cumulative radii
    radii = [sum(thick[:i+1])/1e4 for i in range(len(thick))]

    # Calculate packing fraction and lattice unit size
    vol_compact = π × 0.635² × (2.54 - 0.16 - 0.2)  # Compact volume
    vol_triso = (4/3) × π × radii[-1]³             # TRISO volume
    pf = (vol_triso × n_particles) / vol_compact    # Packing fraction
    vol_cube = vol_triso / pf                       # Lattice unit volume
    side = (vol_cube^(1/3)) / 2                     # Half-width of unit

    # Generate MCNP surfaces (SO, RPP)
    return f-string with surfaces
```

**TRISO Lattice Cell Generation (Lines 51-164):**
```python
def compact_cells(cap, stack, comp, particle):
    """
    Generate MCNP cell cards for a single fuel compact with TRISO lattice.

    Args:
        cap: Capsule number (1-6)
        stack: Stack position (1-3)
        comp: Compact position (1-4)
        particle: TRISO variant ('baseline', 'variant1', 'variant2', 'variant3')

    Returns:
        MCNP cell cards including:
        - TRISO layer cells (kernel, buffer, IPyC, SiC, OPyC, matrix)
        - Matrix filler cell
        - 2D lattice (15×15×1) with particle distribution pattern
        - 3D lattice (1×1×31) for axial stacking
    """
    # Calculate cell/surface/material/universe numbers
    c = 90000 + cap*1000 + stack*100 + 2*(comp-1)*10  # Cell base
    s = 9000 + cap*100 + stack*10 + comp              # Surface base
    m = 9000 + cap*100 + stack*10 + comp              # Material number
    u = cap*100 + stack*10 + comp                     # Universe base

    # Lookup densities by particle variant
    dens = {...}[particle]

    # Generate TRISO layer cells (u=XXX4)
    # Generate matrix filler cell (u=XXX5)
    # Generate 2D lattice (u=XXX6, 15×15, variant-specific pattern)
    # Generate 3D lattice (u=XXX0, 1×1×31)

    return cells
```

**Key Features:**
1. **Hierarchical universe structure:** u=XXX4 (TRISO) → u=XXX6 (2D lattice) → u=XXX0 (3D lattice)
2. **Variant-specific particle distributions:** Different lattice fill patterns for baseline/variant1/2/3
3. **Numbering scheme:** Systematic encoding (capsule × 1000 + stack × 100 + compact × 10)
4. **Automated volume calculation:** Ensures packing fraction consistency

### 1.4 Cycle Loop and File Generation

**Reactor Cycles (Lines 576-581):**
```python
cycles = [
    '138B', '139A', '139B', '140A', '140B', '141A',
    '142A', '142B', '143A', '143B', '144A', '144B', '145A'
]
```

**Per-Cycle File Generation:**
1. **Filename mapping:** `bench_138B.i`, `bench_139A.i`, ..., `bench_145A.i`
2. **Template rendering:** Jinja2 substitutes 6 variables (3 static, 3 cycle-dependent)
3. **File writing:** Output to `mcnp/` directory

**Special Output - MOAA Burnup Model (Lines 912-920):**
```python
# Generate single unified geometry for burnup analysis (no cycle variations)
moaa_xml = 'mcnp/sdr-agr.i'
with open(moaa_xml, 'w+') as f:
    f.write('AGR PIE MCNP model\nc\nc Cells\n')
    f.write(cells)          # All AGR-1 capsule cells
    f.write('\nc\nc Surfaces\n')
    f.write(surfaces)       # All AGR-1 surfaces
    f.write('\nc\nc Materials\n')
    f.write(materials)      # All AGR-1 materials
    f.write('\nimp:p   1  880r  0')  # Photon importance
```

### 1.5 Error Checking and Validation

**Minimal in this example** - Production considerations:
- No MCNP syntax validation (cells, surfaces, materials)
- No cross-reference checking (surface numbers, material numbers)
- No geometry overlap detection
- No validation of CSV data ranges
- **Plotting serves as QA:** Visual inspection of power/OSCC/neck shim trends

**Implicit Validation:**
- f-string formatting ensures consistent syntax
- Hardcoded geometry functions ensure structural correctness
- CSV parsing errors would raise Pandas exceptions

---

## 2. DATA INTEGRATION

### 2.1 CSV File Structures

**power.csv (741 KB):**
```csv
Cycle, Timestep, Cumulative Timestep, Time Interval(hrs),
NWLobePower(MW), NELobePower(MW), CLobePower(MW),
SWLobePower(MW), SELobePower(MW), TotalCorePower(MW)
```
- **Timesteps:** 616 rows (fine-grained power history)
- **Cycles:** 13 cycles (138B through 145A)
- **Usage:** Compute time-averaged power for each cycle → burnup calculations

**oscc.csv:**
```csv
Cycle, Timestep, Cumulative Timestep, Time Interval(hrs),
NWOSCC(degrees), SWOSCC(degrees), NEOSCC(degrees), SEOSCC(degrees)
```
- **Control drums:** 4 outer shim control cylinders (NW/SW/NE/SE quadrants)
- **Angles:** 0-150 degrees (rotation position)
- **Usage:** Find closest predefined angle → select control drum surface definition

**neck_shim.csv:**
```csv
Cycle, Timestep, Cumulative Timestep, Time Interval(hrs),
NW 1, NW 2, ..., NW 6, NE 1, ..., NE 6, SW 1, ..., SW 6, SE 1, ..., SE 6
```
- **Neck shim rods:** 24 rods (6 per quadrant × 4 quadrants)
- **States:** 0 = withdrawn (water), 1 = inserted (hafnium)
- **Usage:** Compute time-averaged insertion → round to 0 or 1 → select material

**MOAA_burnup_FIMA.csv:**
```csv
[Cell numbers], [time column 1], [time column 2], ..., [time column 25]
91101, 0.58, 0.58, 1.27, ..., 11.83  (% FIMA burnup)
...
```
- **Format:** Cell number (row) × burnup at each time snapshot (column)
- **Usage:** Post-processing only (plotting axial burnup profiles)

### 2.2 Data Parsing Strategy

**Read CSV → Group by Cycle (Lines 741-751):**
```python
power_df = pd.read_csv('power.csv', index_col="Cumulative Timestep")
cycles_by_timestep = power_df['Cycle'].to_list()  # ['138B', '138B', ..., '145A']
time_interval = power_df["Time Interval(hrs)"].to_numpy()

time_interval_by_cycle = {}
cum_time = {}
prev = 0
for cycle in cycles:
    time_steps = cycles_by_timestep.count(cycle)  # Count rows per cycle
    time_interval_by_cycle[cycle] = time_interval[prev:prev+time_steps]
    cum_time[cycle] = np.cumsum(time_interval_by_cycle[cycle])  # Cumulative time
    prev += time_steps
```

**Key Pattern:**
1. Read entire CSV (all cycles)
2. Use `count()` to determine rows per cycle
3. Slice arrays by cycle (`prev:prev+time_steps`)
4. Store in dictionaries keyed by cycle name

**Same pattern applied to:**
- OSCC data (lines 756-770)
- Neck shim data (lines 800-817)
- Power data (lines 931-946)

### 2.3 Time-Averaging Algorithms

**Power Time-Averaging (Lines 962-971):**
```python
# Compute weighted average power for each lobe, then sum NE/C/SE lobes
e_power_by_cycle = {}
for cycle, power_by_lobe in power_by_cycle.items():
    add_power = 0
    for lobe_long, power in power_by_lobe.items():
        lobe = lobe_long.split('_')[0]
        if lobe in ['ne', 'c', 'se']:  # Only east lobes (AGR-1 position)
            # Time-weighted average
            ave_power = (power * time_interval_by_cycle[cycle]).sum() / cum_time[cycle][-1]
            add_power += ave_power / 3  # Divide by 3 lobes
    e_power_by_cycle[cycle] = add_power  # Average power for this cycle
```

**OSCC Angle Averaging + Snapping (Lines 787-795):**
```python
def find_closest_value(angles, ave_angle):
    """Snap computed average to nearest predefined angle."""
    n_angles = np.array(angles) - ave_angle
    idx = np.absolute(n_angles).argmin()
    return angles[idx]

angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]  # Predefined

oscc_surfaces = {}
for cycle, angle_by_group in oscc_by_cycle.items():
    for group, angle in angle_by_group.items():
        ave_angle = (angle * time_interval_by_cycle[cycle]).sum() / cum_time[cycle][-1]
        angle = find_closest_value(angles, ave_angle)  # Snap to closest
        oscc_surfaces[cycle] += drum_surfaces[group][angle]  # Lookup surface definition
```

**Neck Shim State Averaging + Rounding (Lines 862-880):**
```python
ne_cells = {}
se_cells = {}
for cycle, rod_insertion in neck_by_cycle.items():
    for rod, insertion in rod_insertion.items():
        # Time-weighted average of 0/1 states
        ave_insertion = (insertion * time_interval_by_cycle[cycle]).sum() / cum_time[cycle][-1]

        # Round to nearest integer (0 = withdrawn, 1 = inserted)
        condition = int(np.rint(ave_insertion))

        # Lookup material (10=water, 71=hafnium)
        mat = neck_materials[condition]  # {0: (10, 1.00276E-1), 1: (71, 4.55926E-2)}

        # Generate cell with appropriate material
        cell_value = get_neck_shim_cells(vals, mat, rod, condition)
        if 'NE' in rod:
            ne_cells[cycle] += cell_value
```

**Key Insight:** Time-weighted averaging handles variable timestep durations correctly:
```
Average = Σ(value_i × duration_i) / Σ(duration_i)
```

### 2.4 Data Format Requirements

**CSV Format:**
- **Encoding:** UTF-8 with BOM (﻿ character in line 1)
- **Index column:** "Cumulative Timestep" used as Pandas index
- **Numeric data:** Floats (scientific notation accepted: 1.4611, 1.00276-1)
- **Cycle labels:** String identifiers ('138B', '139A', etc.)

**Hardcoded Data (not in CSV):**
```python
# TRISO particle specifications (lines 198-208)
thick = {
    'baseline': [349.7/2, 103.5, 39.4, 35.3, 41.0],  # µm
    'variant1': [349.7/2, 102.5, 40.5, 35.7, 41.1],
    ...
}
n_particles = {'baseline': 4154, 'variant1': 4145, ...}

# Capsule-to-particle mapping (lines 216-223)
capsule_particle = {1: 'variant3', 2: 'variant2', 3: 'baseline', ...}

# Shutdown durations (lines 586-592)
shutdown_duration = [15, 95, 15, 14, 9, 56, 14, 24, 16, 20, 15, 62]  # days

# Control drum surface definitions (lines 596-736)
# Hardcoded MCNP surface cards for 13 angles × 2 quadrants
```

**Trade-offs:**
- ✅ CSV for time-varying operational data (easy to edit, version control)
- ✅ Python for geometry specifications (validated by functions, reusable)
- ⚠️ Hardcoded constants reduce flexibility but improve code clarity

### 2.5 Data Validation Approaches

**Implicit validation:**
1. **Pandas parsing errors:** Invalid CSV format raises exception
2. **Cycle counting:** `cycles_by_timestep.count(cycle)` verifies data completeness
3. **Array slicing:** Out-of-bounds access would fail

**Explicit validation (minimal):**
- None for numeric ranges (e.g., OSCC angles 0-150°)
- None for material number conflicts
- None for cell/surface number uniqueness

**Post-processing QA:**
- **Plotting:** Visual inspection of power, OSCC, neck shim trends (lines 773-831)
- **Console output:** Irradiation schedule printed for review (lines 989-992)

---

## 3. INPUT GENERATION LOGIC

### 3.1 String Replacement Strategies

**Method: Jinja2 Template Substitution (not string.replace())**

**Simple Variable Substitution:**
```jinja2
{{cells}}           → Replaced with multi-line string (AGR-1 cells)
{{surfaces}}        → Replaced with multi-line string (AGR-1 surfaces)
{{materials}}       → Replaced with multi-line string (AGR-1 materials)
{{oscc_surfaces}}   → Replaced with cycle-specific control drum surfaces
{{ne_cells}}        → Replaced with cycle-specific NE neck shim cells
{{se_cells}}        → Replaced with cycle-specific SE neck shim cells
```

**No loops or conditionals in template** - all logic handled in Python.

**Advantages over naive string replacement:**
- ✅ Clear separation: logic (Python) vs. structure (template)
- ✅ Maintainable: template is valid MCNP input (can be edited/tested)
- ✅ No escaping issues (Jinja2 handles special characters)
- ✅ Industry-standard tool (extensive documentation, debugging)

### 3.2 Parameter Interpolation Methods

**F-strings for Dynamic Cell/Surface/Material Generation:**

**Example 1: TRISO Surface Cards (Lines 37-46):**
```python
surfaces = f"""\nc
{s}1 so   {radii[0]:.6f}  $ Kernel
{s}2 so   {radii[1]:.6f}  $ Buffer
{s}3 so   {radii[2]:.6f}  $ InnerPyC
{s}4 so   {radii[3]:.6f}  $ SiC
{s}5 so   {radii[4]:.6f}  $ OuterPyC
{s}6 so   1.000000  $ Matrix
{s}7 rpp -{side:.6f} {side:.6f} -{side:.6f} {side:.6f} -0.050000 0.050000
{s}8 rpp -0.650000 0.650000 -0.650000 0.650000 -{side:.6f} {side:.6f}
{s}9 c/z  0.0 0.0   0.6500"""
```

**Example 2: TRISO Cell Cards (Lines 70-78):**
```python
cells = f"""c Capsule {cap}, stack {stack}, compact #{comp}
{c+1} {m1} -{dens[0]:.3f} -{s}1         u={u}4 vol={vol:.6f}    $ Kernel
{c+2} 9090 -{dens[1]:.3f}  {s}1 -{s}2  u={u}4                 $ Buffer
{c+3} 9091 -{dens[2]:.3f}  {s}2 -{s}3  u={u}4                 $ IPyC
{c+4} 9092 -{dens[3]:.3f}  {s}3 -{s}4  u={u}4                 $ SiC
{c+5} 9093 -{dens[4]:.3f}  {s}4 -{s}5  u={u}4                 $ OPyC
{c+6} 9094 -{dens[5]:.3f}  {s}5         u={u}4                 $ SiC Matrix
{c+7} 9094 -{dens[5]:.3f} -{s}6         u={u}5                 $ SiC Matrix
"""
```

**Interpolation features:**
- **Format specifiers:** `.6f` (6 decimal places), `.3f` (3 decimals), `.2f` (2 decimals)
- **Arithmetic in interpolation:** `{c+1}`, `{s}1`, `{u}4`
- **Comments preserved:** `$ Kernel`, `$ Buffer`, etc.
- **Multi-line strings:** `f"""..."""` for entire cell/surface blocks

**Loop-based accumulation:**
```python
cells = """"""  # Initialize empty string
for cap, particle in capsule_particle.items():
    for stack in range(1, 4):
        for comp in range(1, 5):
            cells += compact_cells(cap, stack, comp, particle)  # Accumulate
```

### 3.3 File Naming Conventions

**Pattern: `bench_<CYCLE>.i`**
```python
filename = {cycle: f'bench_{cycle}.i' for cycle in cycles}
# Results in:
# {'138B': 'bench_138B.i', '139A': 'bench_139A.i', ..., '145A': 'bench_145A.i'}
```

**Rationale:**
- **Consistent prefix:** `bench_` identifies base model
- **Cycle identifier:** `138B`, `139A`, etc. (matches CSV data)
- **MCNP extension:** `.i` (standard MCNP input file)

**Alternative naming patterns seen in practice:**
- `<model>_<cycle>_<date>.i` (e.g., `agr1_138B_20250107.i`)
- `<model>_<cycle>_<parameter>.i` (e.g., `agr1_138B_power25MW.i`)
- `<model>_c<num>.i` (e.g., `agr1_c001.i`)

**Best practice:** Include cycle identifier in filename for traceability.

### 3.4 Output File Organization

**Directory Structure:**
```
agr-1/
├── create_inputs.py       # Input generation script
├── plots.py               # Post-processing script
├── bench.template         # Base MCNP model (13,727 lines)
├── power.csv              # Power history data
├── oscc.csv               # Control drum angle data
├── neck_shim.csv          # Neck shim insertion data
├── MOAA_burnup_FIMA.csv   # Burnup results (from previous run)
└── mcnp/                  # Generated inputs (created by script)
    ├── bench_138B.i       # Cycle 138B input
    ├── bench_139A.i       # Cycle 139A input
    ├── ...
    ├── bench_145A.i       # Cycle 145A input
    └── sdr-agr.i          # MOAA burnup model
```

**File creation logic:**
```python
if 'mcnp' not in os.listdir('./'):
    os.mkdir('mcnp')  # Create directory if not exists
```

**Organizational principles:**
1. **Separation:** Input data (CSV) vs. generated files (mcnp/)
2. **Naming:** Clear cycle identification
3. **Automation:** Script creates directory structure
4. **Version control:** `.gitignore` should exclude mcnp/ (generated files)

---

## 4. BEST PRACTICES EXTRACTED

### 4.1 Input Automation Strategies

**1. Template-based generation for multi-scenario studies:**
```
✅ Use templating (Jinja2, Mako) for parameterized inputs
✅ Keep template as valid MCNP input (testable standalone)
✅ Limit template variables to truly cycle-dependent parameters
✅ Use functions for complex geometry (TRISO, lattices, assemblies)
```

**2. Separation of concerns:**
```
Static geometry        → Template file (bench.template)
Time-varying config    → CSV files (power.csv, oscc.csv, neck_shim.csv)
Geometry logic         → Python functions (compact_cells, compact_surfaces)
Data processing        → Python script (create_inputs.py)
```

**3. Systematic numbering schemes:**
```python
# Cell numbers: 90000 + capsule*1000 + stack*100 + compact*10 + layer
cell_91101 = 90000 + 1*1000 + 1*100 + 1*10 + 1  # Capsule 1, Stack 1, Compact 1, Layer 1
cell_96432 = 90000 + 6*1000 + 4*100 + 3*10 + 2  # Capsule 6, Stack 4, Compact 3, Layer 2

# Surface numbers: 9000 + capsule*100 + stack*10 + compact
surf_9614 = 9000 + 6*100 + 1*10 + 4  # Capsule 6, Stack 1, Compact 4

# Universe numbers: capsule*100 + stack*10 + compact
u_614 = 6*100 + 1*10 + 4  # Capsule 6, Stack 1, Compact 4
```

**Advantages:**
- Human-readable (can decode numbers by inspection)
- No conflicts (unique number per component)
- Scalable (systematic generation in loops)

**4. Data-driven control positioning:**
```python
# Rather than hardcoding control positions:
# ❌ drum_angle = 85  # degrees

# Use lookup tables indexed by cycle:
# ✅ drum_angle = oscc_angles[cycle][quadrant]
```

**5. Automated plotting for QA:**
```python
# Generate diagnostic plots alongside inputs
for cycle in cycles:
    plt.figure()
    plt.step(time, power_by_cycle[cycle], where='post')
    plt.savefig(f'power_cycle_{cycle}')
```

### 4.2 Data-Driven Modeling Approaches

**1. External data sources for operational parameters:**
```
Power history       → CSV (timestep × power by lobe)
Control positions   → CSV (timestep × drum angles, shim states)
Material properties → CSV or JSON (temperature-dependent)
Geometry variants   → Database or configuration files
```

**Benefits:**
- Non-programmers can edit data files
- Version control tracks parameter changes
- Easy to regenerate inputs with updated data

**2. Time-averaging for cycle-representative configurations:**
```python
# Compute weighted average over cycle duration
ave_power = Σ(power_i × Δt_i) / Σ(Δt_i)

# Round binary states to 0 or 1
shim_state = round(ave_insertion)  # 0.23 → 0 (withdrawn), 0.78 → 1 (inserted)

# Snap continuous values to discrete options
drum_angle = find_closest(predefined_angles, ave_angle)
```

**Trade-off:** Time-averaged configuration may not capture peak reactivity or transients, but enables static MCNP calculations.

**3. Dictionary-based parameter lookup:**
```python
# Material by insertion state
neck_materials = {
    0: (10, 1.00276E-1),   # Material 10 (water), density
    1: (71, 4.55926E-2),   # Material 71 (hafnium), density
}

# TRISO variant by capsule
capsule_particle = {
    1: 'variant3',
    2: 'variant2',
    3: 'baseline',
    ...
}

# Surface definitions by angle
drum_surfaces['ne'][85] = "c/z 48.0375 -18.1425 9.195"
```

**Benefits:**
- Declarative (what, not how)
- Easy to extend (add new cycles, variants)
- Self-documenting (keys explain meaning)

### 4.3 Version Control Considerations

**What to commit:**
```
✅ create_inputs.py          # Generation script
✅ bench.template            # Base model
✅ power.csv, oscc.csv, ...  # Input data
✅ README.md                 # Documentation
✅ .gitignore                # Exclude generated files
```

**What to exclude (.gitignore):**
```
mcnp/                  # Generated inputs (can be regenerated)
*.png                  # Plots (can be regenerated)
__pycache__/           # Python bytecode
*.pyc                  # Python compiled files
```

**Rationale:**
- Generated files are build artifacts (like compiled code)
- Changes should be tracked in source (script, template, data), not outputs
- Reduces repository size
- Forces users to run generation script (ensures consistency)

**Exception:** Commit one example output for reference:
```
examples/
└── bench_138B_example.i   # Example generated input
```

**Commit messages for data changes:**
```
✅ "Update power.csv: Add cycle 145B data from experiment log"
✅ "Fix oscc.csv: Correct SE drum angle at timestep 312"
❌ "Update files" (too vague)
```

### 4.4 Reproducibility Patterns

**1. Pinned dependencies:**
```python
# requirements.txt
numpy==1.24.3
pandas==2.0.2
matplotlib==3.7.1
jinja2==3.1.2
```

**2. Script self-documentation:**
```python
# Print key parameters to console
print(f"Generating {len(cycles)} cycle inputs")
print(f"Power history: {len(power_df)} timesteps")
print("\nPower History:")
print(irradiation_cases)  # Show computed cycle-averaged powers
```

**3. Deterministic processing:**
- No random number generation
- No timestamps in filenames (unless needed)
- Consistent ordering (sorted dictionaries, explicit loops)

**4. Logging and traceability:**
```python
# Add metadata to generated inputs (as comments)
f.write(f"c Generated by create_inputs.py on {datetime.now()}\n")
f.write(f"c Data sources: power.csv, oscc.csv, neck_shim.csv\n")
f.write(f"c Cycle: {cycle}\n")
f.write(f"c Average power: {e_power_by_cycle[cycle]:.4f} MW\n")
```

**5. Validation against known results:**
```python
# Compare generated cell numbers to expected ranges
expected_cells = range(91101, 96434)
generated_cells = extract_cell_numbers(cells)
assert set(generated_cells) == set(expected_cells), "Cell number mismatch"
```

### 4.5 MCNP Skills Integration Recommendations

**Skills that should support automated input generation:**

**mcnp-input-builder:**
- Generate template skeletons with placeholder variables
- Validate template syntax (ensure {{vars}} don't break MCNP parsing)
- Suggest systematic numbering schemes

**mcnp-geometry-builder:**
- Provide geometry generation functions (like `compact_cells`)
- Support parameterized geometry (TRISO, fuel pins, assemblies)
- Generate lattice fill arrays programmatically

**mcnp-lattice-builder:**
- Create hierarchical universe structures
- Calculate packing fractions and lattice unit sizes
- Generate fill arrays with variant-specific patterns

**mcnp-material-builder:**
- Generate material cards from composition databases
- Support temperature-dependent densities
- Handle material variations (by cycle, by component)

**mcnp-input-validator:**
- Validate generated inputs before MCNP execution
- Check cell/surface/material cross-references
- Verify numbering scheme consistency

**mcnp-input-editor:**
- Batch update parameters across multiple generated inputs
- Apply corrections to entire cycle sequence
- Update material densities or cross-sections

**New skill needed: mcnp-template-generator:**
- Create Jinja2/Mako templates from existing MCNP inputs
- Identify parameters suitable for template variables
- Generate CSV data file schemas
- Create generation scripts (like create_inputs.py)

**New skill needed: mcnp-parameter-study-manager:**
- Orchestrate multi-input generation
- Manage CSV data files
- Run MCNP calculations in parallel
- Collect and compare results

---

## 5. ADVANCED PATTERNS OBSERVED

### 5.1 Hierarchical Universe Generation

**3-level universe hierarchy for TRISO compacts:**
```
Universe XXX0 (3D lattice, 1×1×31)
  └─ Fills with → Universe XXX6 (2D lattice, 15×15×1)
       └─ Fills with → Universe XXX4 (TRISO particle)
                       Universe XXX5 (matrix filler)
```

**Code structure (Lines 82-162):**
```python
cells += f"""c
{c+8} 0   -{s}7  u={u}6 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     {u}5 {u}5 {u}5 {u}5 {u}5 {u}5 {u}4 {u}4 {u}4 {u}5 {u}5 {u}5 {u}5 {u}5 {u}5
     ...
     {u}5 {u}5 {u}5 {u}5 {u}5 {u}5 {u}4 {u}4 {u}4 {u}5 {u}5 {u}5 {u}5 {u}5 {u}5
"""

cells += f"""c
{c+10} 0  -{s}8 u={u}0 lat=1  fill=0:0 0:0 -15:15 {u}7 2R {u}6 24R {u}7 2R
"""
```

**Key insight:** Hardcoded lattice fill patterns (15×15) are variant-specific:
- Baseline: 161 particles (15×15 grid with edge particles removed)
- Variant1: 158 particles (slightly different pattern)
- Variant2: 153 particles
- Variant3: 156 particles

### 5.2 Control Drum Surface Definitions

**13 predefined angles × 2 quadrants = 26 surface sets:**
```python
angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]

ne_surfaces = []
surf = f"""c
  981   c/z    44.2436  -6.3119  9.195       $ DRUM E1 AT 0 DEGREES
  982   c/z    30.3697 -17.5600  9.195       $ DRUM E2 AT 0 DEGREES
c """
ne_surfaces.append(surf)
# ... repeat for each angle

drum_surfaces['ne'] = dict(zip(angles, ne_surfaces))
```

**Usage:**
```python
# Time-averaged angle = 82.3 degrees
ave_angle = 82.3
# Snap to closest predefined angle
angle = find_closest_value([0, 25, 40, ..., 150], 82.3)  # Returns 85
# Lookup surface definition
surf = drum_surfaces['ne'][85]  # Returns "c/z 48.0375 -18.1425 9.195 ..."
```

**Why this approach?**
- Control drum geometry is complex (partial cylinders with hafnium inserts)
- Precomputing surfaces avoids geometric calculations in script
- Discrete angles match physical drum positions (notches)

### 5.3 Multi-Output Generation

**Single script generates multiple output types:**

1. **Cycle-specific inputs** (13 files):
   - `bench_138B.i`, `bench_139A.i`, ..., `bench_145A.i`
   - Time-averaged configurations per cycle

2. **Unified burnup model** (1 file):
   - `sdr-agr.i`
   - Static geometry (no cycle variations)
   - Used for MOAA/ORIGEN burnup calculations

3. **Diagnostic plots** (39 PNG files):
   - `power_cycle_*.png` (13 files)
   - `oscc_cycle_*.png` (13 files)
   - `neck_cycle_*.png` (13 files)

4. **Console output** (irradiation schedule):
   - MOAA input format (timestep, power, duration)
   - Fuel cell numbers for burnup tracking

**Pattern:** Single data source → multiple output formats

### 5.4 Irradiation History Generation

**MOAA/ORIGEN irradiation schedule (Lines 973-980):**
```python
def define_irrad_case(filename, time, power):
    irradiation_case = f"""
    mcnp_input_file: {filename}
    time: {time:.2f} days
    power: {power:.2f} MW"""
    return irradiation_case

irradiation_cases = """"""
for cycle in cycles:
    time = cum_time[cycle][-1] / 24  # hours → days
    irradiation_cases += define_irrad_case(filename[cycle], time, e_power_by_cycle[cycle])
    if cycle is not cycles[-1]:
        irradiation_cases += '\n'
        # Add shutdown period
        irradiation_cases += define_irrad_case(filename[cycle], shutdown_cycle[cycle], 0)
        irradiation_cases += '\n'
```

**Output format:**
```
mcnp_input_file: bench_138B.i
time: 49.04 days
power: 23.45 MW

mcnp_input_file: bench_138B.i
time: 15.00 days
power: 0.00 MW

mcnp_input_file: bench_139A.i
time: 23.21 days
power: 24.12 MW
...
```

**Usage:** Fed to MOAA (MCNP-ORIGEN Automated Analysis) for burnup calculations.

### 5.5 Compact Position Calculation

**Geometric calculation of compact centers (Lines 167-191):**
```python
def compact_center(cap, stack, comp):
    # Stack positions (radial, in ATR B10 hole)
    if stack == 1:
        cx, cy = 25.547039, -24.553123
    elif stack == 2:
        cx, cy = 24.553123, -25.547039
    elif stack == 3:
        cx, cy = 25.910838, -25.910838

    # Capsule axial positions
    if cap == 1:
        cz = 17.81810
    elif cap == 2:
        cz = 33.04540
    # ... caps 3-6

    # Compact offset within capsule
    cz += (comp-1)*2.54 + 0.2 + (2.54-0.16-0.2)/2

    return cx, cy, cz
```

**Used in FILL card:**
```python
cells += f"""c
{c+11} 0 -{s1} {limit+1} -{limit+47} fill={u}0 ({cx:.6f} {cy:.6f} {cz:.6f})
"""
```

**Pattern:** Systematic position calculation enables loop-based generation.

---

## 6. LIMITATIONS AND IMPROVEMENTS

### 6.1 Current Limitations

**1. No input validation:**
- CSV data not checked (e.g., power < 0, angles > 180°)
- Generated MCNP syntax not validated
- No cross-reference checking (materials, surfaces)

**2. Hardcoded geometry:**
- TRISO specifications embedded in script
- Control drum surfaces precomputed (not parametric)
- Difficult to adapt to different experiments

**3. Limited error handling:**
- CSV parsing errors not caught gracefully
- Division by zero possible if cycle has zero duration
- No checks for missing cycles in data

**4. Manual data preparation:**
- CSV files must be prepared externally
- No tools for experimental data import
- Shutdown durations hardcoded (should be in CSV)

**5. No documentation in template:**
- Template lacks comments explaining placeholder variables
- No validation that template matches script expectations

### 6.2 Suggested Improvements

**1. Add input validation:**
```python
def validate_power_data(power_df, cycles):
    """Validate power CSV data."""
    # Check all cycles present
    cycles_in_data = set(power_df['Cycle'].unique())
    missing = set(cycles) - cycles_in_data
    if missing:
        raise ValueError(f"Missing cycles in power.csv: {missing}")

    # Check positive power
    if (power_df['TotalCorePower(MW)'] < 0).any():
        raise ValueError("Negative power detected in power.csv")

    # Check timestep continuity
    ...
```

**2. Parameterize geometry:**
```python
# Replace hardcoded values with configuration file
config = {
    'triso': {
        'baseline': {'layers': [174.85, 103.5, 39.4, 35.3, 41.0], 'n_particles': 4154},
        'variant1': {'layers': [174.85, 102.5, 40.5, 35.7, 41.1], 'n_particles': 4145},
    },
    'capsules': {1: 'variant3', 2: 'variant2', ...},
    'shutdown_days': [15, 95, 15, 14, 9, 56, 14, 24, 16, 20, 15, 62],
}

# Load from JSON or YAML
with open('config.json') as f:
    config = json.load(f)
```

**3. Generate control drum surfaces parametrically:**
```python
def generate_drum_surface(drum_id, angle, center, radius):
    """Calculate drum surface coordinates from angle."""
    cx = center[0] + radius * np.cos(np.radians(angle))
    cy = center[1] + radius * np.sin(np.radians(angle))
    return f"c/z {cx:.6f} {cy:.6f} {radius:.6f}"

# No need for 26 hardcoded surface definitions
```

**4. Add MCNP syntax validation:**
```python
# After generating input, run basic checks
def validate_mcnp_input(filename):
    """Check basic MCNP syntax."""
    with open(filename) as f:
        lines = f.readlines()

    # Check cell cards have valid format
    for line in cell_lines:
        parts = line.split()
        cell_num = int(parts[0])
        mat_num = int(parts[1]) if parts[1] != '0' else 0
        # Check material referenced in materials section
        ...

    # Check surface numbers used in cells exist
    # Check universe numbers are consistent
    # etc.
```

**5. Modularize script:**
```python
# Current: 993-line monolithic script
# Improved: Separate modules

# geometry.py
def compact_surfaces(...): ...
def compact_cells(...): ...
def compact_center(...): ...

# data_processing.py
def read_power_csv(...): ...
def compute_time_average(...): ...
def find_closest_angle(...): ...

# template_rendering.py
def render_cycle_input(...): ...
def generate_irradiation_schedule(...): ...

# main.py
from geometry import *
from data_processing import *
from template_rendering import *

if __name__ == '__main__':
    # Orchestrate workflow
    ...
```

**6. Add command-line interface:**
```python
import argparse

parser = argparse.ArgumentParser(description='Generate AGR-1 MCNP inputs')
parser.add_argument('--cycles', nargs='+', default=all_cycles,
                    help='Cycles to generate (default: all)')
parser.add_argument('--power-csv', default='power.csv',
                    help='Power history CSV file')
parser.add_argument('--output-dir', default='mcnp/',
                    help='Output directory')
parser.add_argument('--validate', action='store_true',
                    help='Validate generated inputs')
args = parser.parse_args()

# Usage:
# python create_inputs.py --cycles 138B 139A --validate
```

**7. Add progress indicators:**
```python
from tqdm import tqdm

for cycle in tqdm(cycles, desc="Generating inputs"):
    template = env.get_template('bench.template')
    ...
```

---

## 7. SKILLS DEVELOPMENT RECOMMENDATIONS

### 7.1 New Skill: mcnp-template-generator

**Purpose:** Convert existing MCNP inputs into Jinja2 templates and generation scripts.

**Capabilities:**
1. **Analyze input file:**
   - Identify repeated patterns (e.g., fuel assemblies, lattices)
   - Detect parameter variations (e.g., densities, positions)
   - Find candidates for template variables

2. **Generate template:**
   - Replace parameters with {{placeholders}}
   - Add Jinja2 control structures (if/for) if needed
   - Preserve comments and formatting

3. **Create generation script skeleton:**
   ```python
   # Generated by mcnp-template-generator
   from jinja2 import Environment, FileSystemLoader

   # TODO: Define parameter values
   parameters = {
       'power': 100,  # MW
       'enrichment': 19.75,  # %
       ...
   }

   env = Environment(loader=FileSystemLoader('.'))
   template = env.get_template('model.template')
   output = template.render(**parameters)

   with open('model.i', 'w') as f:
       f.write(output)
   ```

4. **Suggest CSV data schema:**
   ```csv
   cycle, power_MW, enrichment_pct, control_position_deg
   138B, 23.45, 19.75, 85
   139A, 24.12, 19.75, 90
   ...
   ```

**Workflow:**
```
User: "Convert bench_138B.i to a template"
Skill: [Analyzes input]
       "Found 13 cycle-specific parameters:
        - NE neck shim cells (lines 621-670)
        - SE neck shim cells (lines 674-723)
        - OSCC drum surfaces (lines 1782-1800)

        Suggest template variables:
        {{ne_cells}}, {{se_cells}}, {{oscc_surfaces}}

        Created bench.template with 3 placeholders.
        Created generate_bench.py script skeleton."
```

### 7.2 Enhanced Skill: mcnp-lattice-builder

**Add support for automated lattice fill generation:**

```python
# Current: Manual specification
fill = "1 1 1 2 2 2 1 1 1 ..."

# Enhanced: Programmatic generation
from mcnp_skills.lattice_builder import create_circular_fill

fill = create_circular_fill(
    center_universe=1,
    edge_universe=2,
    radius=7,  # Grid units
    grid_size=(15, 15)
)
# Returns: 15×15 fill array with circular pattern
```

**Add TRISO packing fraction calculator:**
```python
from mcnp_skills.lattice_builder import calculate_triso_packing

packing = calculate_triso_packing(
    compact_radius=0.635,  # cm
    compact_height=2.18,   # cm
    triso_radius=radii[-1],  # cm (outer PyC)
    n_particles=4154
)
# Returns: packing_fraction, lattice_unit_size
```

### 7.3 Enhanced Skill: mcnp-material-builder

**Add support for CSV-based material definitions:**

```python
from mcnp_skills.material_builder import materials_from_csv

# CSV format:
# material_id, isotope, fraction_type, fraction
# 9000, 92235, weight, 0.19975
# 9000, 92238, weight, 0.80025

materials = materials_from_csv('materials.csv', density=10.5)
# Returns MCNP material cards
```

**Add temperature-dependent density lookup:**
```python
from mcnp_skills.material_builder import get_density

dens = get_density(
    material='water',
    temperature=62,  # °C
    pressure=2.5     # MPa
)
# Returns: 0.9853 g/cm³
```

### 7.4 New Skill: mcnp-cycle-manager

**Purpose:** Manage multi-cycle simulations (burnup, parameter studies).

**Capabilities:**

1. **Irradiation schedule management:**
   ```python
   from mcnp_skills.cycle_manager import IrradiationSchedule

   schedule = IrradiationSchedule()
   schedule.add_cycle('138B', power=23.45, duration=49.04)  # days
   schedule.add_shutdown(duration=15)
   schedule.add_cycle('139A', power=24.12, duration=23.21)

   schedule.export_moaa('irradiation.txt')
   schedule.plot('schedule.png')
   ```

2. **Burnup cell tracking:**
   ```python
   from mcnp_skills.cycle_manager import BurnupTracker

   tracker = BurnupTracker()
   tracker.add_cells(range(91101, 96434))  # Fuel cells
   tracker.load_results('mctal')
   tracker.plot_burnup_vs_position('burnup.png')
   ```

3. **Batch input generation:**
   ```python
   from mcnp_skills.cycle_manager import BatchGenerator

   generator = BatchGenerator('bench.template')
   generator.load_cycle_data('power.csv', 'oscc.csv', 'neck_shim.csv')
   generator.generate_all(output_dir='mcnp/')
   generator.validate_all()  # Check MCNP syntax
   ```

### 7.5 Integration Example

**User workflow with enhanced skills:**

```
User: "I need to create MCNP inputs for 13 reactor cycles with time-varying control positions"

Agent: [Invokes mcnp-template-generator]
       "I'll help you set up a template-based workflow.

        Step 1: Convert your base input to a template.
        Which MCNP input should I use as the base?"

User: "bench_138B.i"

Agent: [Analyzes bench_138B.i]
       "I found cycle-dependent sections:
        - Control drum positions (lines 1782-1800)
        - Neck shim rod materials (lines 621-723)

        I've created:
        ✓ bench.template (with {{oscc_surfaces}}, {{ne_cells}}, {{se_cells}})
        ✓ generate_inputs.py (script skeleton)

        Step 2: Provide cycle data.
        Do you have power history and control position data?"

User: "Yes, I have power.csv, oscc.csv, and neck_shim.csv"

Agent: [Invokes mcnp-cycle-manager]
       "I'll set up the batch generation workflow.

        [Reads CSV files]
        ✓ Found 13 cycles (138B through 145A)
        ✓ Found 616 timesteps
        ✓ Validated data completeness

        [Generates inputs]
        ✓ bench_138B.i (25 MW avg, OSCC 85°)
        ✓ bench_139A.i (24 MW avg, OSCC 88°)
        ...
        ✓ bench_145A.i (23 MW avg, OSCC 82°)

        [Validates inputs]
        ✓ All 13 inputs pass MCNP syntax check

        Generated irradiation schedule for MOAA:
        - Total irradiation: 1074 days
        - Total shutdowns: 341 days
        - Average power: 23.8 MW

        Next steps:
        1. Review diagnostic plots (power_cycle_*.png)
        2. Run MCNP: mcnp6 i=bench_138B.i
        3. Track burnup with mcnp-burnup-builder"
```

---

## 8. CONCLUSION

### 8.1 Key Takeaways

**1. Template-based automation is production-ready:**
- Jinja2 provides robust, maintainable templating
- Separation of logic (Python) and structure (template) is critical
- Industry-standard tools reduce development time

**2. Time-averaging enables static MCNP models:**
- Weighted averages capture cycle-representative configurations
- Snapping (angles) and rounding (binary states) work well
- Trade-off: May miss peak reactivity or transients

**3. Data-driven approaches scale:**
- CSV files enable non-programmer edits
- Systematic numbering schemes enable loop-based generation
- Dictionary lookups provide declarative configuration

**4. Multiple output types from single source:**
- Cycle-specific inputs for transport calculations
- Unified geometry for burnup calculations
- Diagnostic plots for QA
- Irradiation schedules for depletion codes

**5. Reproducibility requires discipline:**
- Pin dependencies, document data sources
- Generate metadata in outputs
- Exclude generated files from version control

### 8.2 Applicability to Other Reactor Models

**This workflow pattern generalizes to:**

1. **PWR/BWR cycle depletion:**
   - Control rod positions by cycle
   - Boron concentration by cycle
   - Fuel assembly shuffling

2. **Fast reactor parameter studies:**
   - Control rod worth curves
   - Coolant void reactivity
   - Fuel composition variations

3. **MSR salt composition evolution:**
   - Online fission product removal rates
   - Feed composition adjustments
   - Graphite moderator density changes

4. **Research reactor experiments:**
   - Sample irradiation schedules
   - Beam port configurations
   - Reflector material studies

**Common elements:**
- Base template (static geometry)
- CSV data (time-varying or parametric)
- Generation script (data processing + rendering)
- Validation (plotting, syntax checking)

### 8.3 Priority Enhancements for MCNP Skills

**High priority:**
1. ✅ **mcnp-template-generator:** Convert inputs → templates + scripts
2. ✅ **mcnp-cycle-manager:** Batch generation, validation, tracking
3. ✅ **mcnp-lattice-builder enhancements:** Packing, fill patterns

**Medium priority:**
4. ✅ **mcnp-material-builder enhancements:** CSV import, T-dependent properties
5. ✅ **mcnp-input-validator:** Syntax checking, cross-reference validation

**Low priority:**
6. ⏳ **mcnp-geometry-builder enhancements:** Parametric geometry functions
7. ⏳ **mcnp-plotting enhancements:** Automated QA plot generation

---

## APPENDIX A: COMPLETE FILE LISTING

**Python scripts:**
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/create_inputs.py` (993 lines)
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/plots.py` (237 lines)

**Data files:**
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/bench.template` (13,727 lines)
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/power.csv` (617 rows × 10 columns)
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/oscc.csv` (617 rows × 8 columns)
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/neck_shim.csv` (617 rows × 28 columns)
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/MOAA_burnup_FIMA.csv` (73 rows × 26 columns)

**Generated outputs (example):**
- `mcnp/bench_138B.i`, `mcnp/bench_139A.i`, ..., `mcnp/bench_145A.i` (13 files)
- `mcnp/sdr-agr.i` (unified burnup model)
- `power_cycle_*.png`, `oscc_cycle_*.png`, `neck_cycle_*.png` (39 plots)
- `burnup_axial.png` (post-processing plot)

---

## APPENDIX B: EXAMPLE TEMPLATE VARIABLE

**Template section (bench.template, lines 619-625):**
```
c   ---------------------------------------------------------------------------
c      NE NECK SHIMS
c
{{ne_cells}}
  701  010 1.00276-1          -701  100  -200        $ NE 1 water inside shim
                                    -30    10        $ East Quadrant
  703  010 1.00276-1    702   -703  100  -200        $ NE 1 water outside shim
```

**Generated content for cycle 138B (ne_cells['138B']):**
```python
# Cycle 138B: All NE neck shims inserted (hafnium)
"""c
  702   71 4.55926E-2    701   -702  100  -200        $ NE 1 Hf neck shim - inserted
                                    -30    10        $ East Quadrant
c
  707   71 4.55926E-2    706   -707  100  -200        $ NE 2 Hf neck shim - inserted
                                    -30    10        $ East Quadrant
c
...
  727   71 4.55926E-2    726   -727  100  -200        $ NE 6 Hf neck shim - inserted
                                    -30    10        $ East Quadrant
"""
```

**Generated content for cycle 145A (ne_cells['145A']):**
```python
# Cycle 145A: Some NE neck shims withdrawn (water)
"""c
  702   10 1.00276E-1    701   -702  100  -200        $ NE 1 Hf neck shim - withdrawn
                                    -30    10        $ East Quadrant
c
  707   10 1.00276E-1    706   -707  100  -200        $ NE 2 Hf neck shim - withdrawn
                                    -30    10        $ East Quadrant
c
...
  727   71 4.55926E-2    726   -727  100  -200        $ NE 6 Hf neck shim - inserted
                                    -30    10        $ East Quadrant
"""
```

**Key observation:** Material number (10=water, 71=hafnium) changes based on time-averaged insertion state.

---

**END OF ANALYSIS**
