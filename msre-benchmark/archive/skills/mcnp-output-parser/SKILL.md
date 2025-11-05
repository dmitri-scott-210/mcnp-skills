---
name: "MCNP Output Parser"
description: "Parses MCNP output files (OUTP, MCTAL, HDF5, XDMF) extracting tallies, warnings, mesh results, and particle tracks. Use when analyzing MCNP simulation results."
version: "1.0.0"
dependencies: "python>=3.8, h5py, numpy"
---

# MCNP Output Parser

## Overview

When a user needs to extract, analyze, or understand MCNP simulation output data, use this skill to parse and extract information from various MCNP output file formats:

- **OUTP**: Main ASCII output file with warnings, tallies, statistical tables, problem summary
- **MCTAL**: Machine-readable ASCII tally file for plotting and post-processing
- **HDF5** (RUNTPE.H5): Binary restart files with mesh tallies, problem state, particle tracks
- **XDMF**: XML descriptor files linking to HDF5 data for ParaView/VisIt visualization
- **MESHTAL**: ASCII mesh tally output
- **PTRAC**: Particle tracking output (HDF5 or ASCII)

This skill helps users extract data for validation, plotting, post-processing, and identifying simulation problems through warning/error analysis.

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User asks to "parse", "extract", "read", or "analyze" MCNP output
- User mentions output file names: `outp`, `output`, `mctal`, `meshtal`, `runtpe.h5`, `.xdmf`
- User wants tally values, statistical checks, or mesh results
- User needs to check warnings/errors from a completed run
- User wants to prepare data for visualization or plotting
- User mentions ParaView, VisIt, or visualization tools
- User asks about particle trajectories or tracking data

**Context Clues:**
- "My simulation finished, now I need to..."
- "What are the tally results?"
- "Extract the flux distribution..."
- "Check if there were any warnings..."
- "Prepare data for plotting..."
- "Load mesh tally into ParaView..."

### File Format Decision Tree

**Step 1: Identify File Type**

```
User provides file → Check extension/format:
├── .o, .out, outp, output → OUTP (main ASCII output)
├── mctal, mctal.h5 → MCTAL (tally output)
├── runtpe.h5, .h5 → HDF5 (restart/mesh data)
├── .xdmf → XDMF (visualization descriptor)
├── meshtal → MESHTAL (ASCII mesh tallies)
├── ptrac, ptrac.h5 → PTRAC (particle tracking)
└── Unknown → Ask user or inspect file header
```

**Step 2: Select Parsing Strategy**

```
OUTP file:
├── Full analysis → Parse all sections (header, tallies, warnings, tables)
├── Tally extraction → Extract specific tally numbers
├── Warning check → Search for warning/error messages
├── Statistics → Extract 10 statistical quality checks
└── Problem summary → Extract geometry/material tables

MCTAL file:
├── All tallies → Parse complete file structure
├── Specific tally → Extract by tally number
├── TFC data → Extract tally fluctuation chart
└── Convert to DataFrame → Prepare for plotting

HDF5 file (RUNTPE.H5):
├── Mesh tally → Navigate /results/mesh_tally_N hierarchy
├── PTRAC → Navigate /particle_N/step_data structure
├── Problem info → Extract /problem_info metadata
├── Fission matrix → Read CSR sparse format
└── Inspect structure → List all groups/datasets

XDMF file:
├── View in ParaView → Instruct user to load .xdmf
├── Extract geometry → Parse XML for mesh coordinates
├── Extract data → Follow HDF5 references
└── Generate new XDMF → Create descriptor for custom data
```

## Tool Invocation

This skill includes a Python implementation for automated output file parsing and data extraction.

### Importing the Tool

```python
from mcnp_output_analyzer import MCNPOutputAnalyzer

# Initialize the analyzer
analyzer = MCNPOutputAnalyzer()
```

### Basic Usage

**Parse Complete Output File**:
```python
# Parse entire output file
results = analyzer.parse_output('outp')

# Access header information
header = results['header']
print(f"Problem ID: {header['problem_id']}")
print(f"NPS: {header['nps']:,}")

# Access all tallies
tallies = results['tallies']
for tally_num, tally_data in tallies.items():
    print(f"Tally F{tally_num}: {tally_data['value']} ± {tally_data['error']}")
```

**Extract Specific Tally Data**:
```python
# Extract single tally
tally_4 = analyzer.extract_tally('outp', tally_num=4)

print(f"Tally F4 Results:")
print(f"  Value: {tally_4['value']:.4e}")
print(f"  Relative Error: {tally_4['rel_error']:.4f}")
```

**Check for Warnings and Errors**:
```python
# Extract diagnostics
warnings = analyzer.get_warnings('outp')
errors = analyzer.get_fatal_errors('outp')

if errors:
    print("FATAL ERRORS found:")
    for err in errors:
        print(f"  - {err}")
```

### Integration with MCNP Workflow

```python
from mcnp_output_analyzer import MCNPOutputAnalyzer

def analyze_simulation_results(output_file):
    """Complete output analysis workflow"""
    analyzer = MCNPOutputAnalyzer()
    results = analyzer.parse_output(output_file)

    # Check for fatal errors
    errors = analyzer.get_fatal_errors(output_file)
    if errors:
        print("❌ FATAL ERRORS - Simulation failed")
        return False

    # Display tally results
    tallies = results['tallies']
    print(f"📊 TALLY RESULTS ({len(tallies)} tallies):")

    for tally_num in sorted(tallies.keys()):
        tally = tallies[tally_num]
        value = tally.get('value', 0)
        error = tally.get('rel_error', 999)
        print(f"  F{tally_num}: {value:.4e} ± {error:.1%}")

    print("✓ Analysis complete")
    return True

# Example usage
if __name__ == "__main__":
    analyze_simulation_results("outp")
```

---

## Parsing Procedures

### Step 1: Initial Assessment

**Ask user for context:**
- "Which output file do you need to parse?" (get file path)
- "What information do you need?" (tallies, warnings, mesh data, statistics)
- "Do you need specific tally numbers or all tallies?"
- "Are you preparing data for visualization or analysis?"
- "Did the simulation complete normally?"

### Step 2: Read Reference Materials

**MANDATORY - READ ENTIRE FILE**: Before performing parsing, read:
- `.claude/commands/mcnp-output-parser.md` - Complete parsing procedures for all formats
- If HDF5: Review Appendices D.3-D.6 structure in knowledge base
- If mesh tallies: Review Chapter 8 and Appendix D.4 (XDMF)

### Step 3: Parse Output File

Use appropriate Python module for file type:

**For OUTP files:**
```python
from skills.output_analysis.mcnp_output_analyzer import MCNPOutputAnalyzer

analyzer = MCNPOutputAnalyzer()

# Full analysis
analysis = analyzer.analyze_output('output.o')

# Results structure:
# {
#     'summary': {
#         'terminated_normally': bool,
#         'n_warnings': int,
#         'n_errors': int,
#         'n_tallies': int,
#         'has_kcode': bool,
#         'computer_time': float
#     },
#     'details': {
#         'warnings': [list],
#         'errors': [list],
#         'tallies': {tally_num: data},
#         'kcode': {...} or None
#     }
# }

# Extract specific sections
warnings = analyzer.extract_warnings('output.o')
errors = analyzer.extract_errors('output.o')
report = analyzer.generate_report('output.o')
```

**For MCTAL files:**
```python
from skills.output_analysis.mcnp_mctal_processor import MCNPMCTALProcessor

processor = MCNPMCTALProcessor()

# Parse MCTAL file
mctal_data = processor.parse_mctal('mctal')

# Extract specific tally
tally_4 = processor.extract_tally(mctal_data, tally_number=4)

# Get tally fluctuation chart data
tfc = processor.extract_tfc_data(tally_4)

# Convert to DataFrame for plotting
import pandas as pd
df = processor.to_dataframe(tally_4)
```

**For HDF5 files:**
```python
import h5py
import numpy as np

# Open HDF5 file
with h5py.File('runtpe.h5', 'r') as f:
    # Inspect structure
    def print_structure(name, obj):
        indent = "  " * name.count('/')
        obj_type = "GROUP" if isinstance(obj, h5py.Group) else "DATASET"
        print(f"{indent}{name} ({obj_type})")
        if isinstance(obj, h5py.Dataset):
            print(f"{indent}  Shape: {obj.shape}, Type: {obj.dtype}")
        # Print attributes
        for key, val in obj.attrs.items():
            print(f"{indent}  @{key} = {val}")

    f.visititems(print_structure)

    # Extract mesh tally (Appendix D.6)
    mesh_path = '/results/mesh_tally_14/energy_total/time_total'
    values = f[mesh_path + '/values'][:]  # numpy array
    errors = f[mesh_path + '/errors'][:]  # relative errors

    # Get mesh geometry
    geom_path = '/results/mesh_tally_14/geometry'
    if geom_path in f:
        coordinates = f[geom_path + '/coordinates'][:]  # Nx3 array
        connectivity = f[geom_path + '/connectivity'][:]  # Element-node map

    # Extract PTRAC data (Appendix D.3)
    if '/particle_1' in f:
        particle_1 = f['/particle_1/step_data']
        x = particle_1['x'][:]  # X coordinates
        y = particle_1['y'][:]  # Y coordinates
        z = particle_1['z'][:]  # Z coordinates
        energy = particle_1['energy'][:]
        time = particle_1['time'][:]
        event_type = particle_1['event_type'][:]

    # Extract fission matrix (Appendix D.5)
    if '/fission_matrix' in f:
        row_ptr = f['/fission_matrix/row_ptr'][:]
        col_ind = f['/fission_matrix/col_ind'][:]
        values = f['/fission_matrix/values'][:]
        # Compressed Sparse Row (CSR) format
        # row_ptr[i] = starting index for row i
        # col_ind[j] = column index for element j
        # values[j] = value of element j
```

**For XDMF files:**
```python
import xml.etree.ElementTree as ET

# Parse XDMF descriptor
tree = ET.parse('meshtal.xdmf')
root = tree.getroot()

# Extract mesh geometry reference
geometry = root.find('.//Geometry/DataItem')
hdf5_path = geometry.text.strip()  # e.g., "runtpe.h5:/results/mesh_tally_14/geometry/coordinates"

# Extract attribute (tally data) reference
attribute = root.find('.//Attribute[@Name="flux"]/DataItem')
flux_path = attribute.text.strip()  # e.g., "runtpe.h5:/results/mesh_tally_14/values"

# Usually easier to just load in ParaView:
# ParaView → File → Open → Select .xdmf file
```

### Step 4: Extract Specific Data

**Tally Extraction from OUTP:**
```python
# Tallies in OUTP format:
# 1tally       14        nps =   1000000
#            tally type 4    track length estimate of particle flux.
#            particle(s): neutrons
#
#  cell  5
#                  cell union total
#                    1.23456E-02   0.0123

# Parse tally section
tally_number = 14
tally_type = 4  # F4 = track length flux
particle = 'neutrons'
cells = [5]
value = 1.23456e-2
relative_error = 0.0123  # 1.23% (NOT 12.3%!)
```

**Warning/Error Extraction:**
```python
# Common warning patterns in OUTP:
warnings = []
errors = []

with open('output.o', 'r') as f:
    for line in f:
        if 'warning' in line.lower():
            warnings.append(line.strip())
        if 'fatal error' in line.lower() or 'error termination' in line.lower():
            errors.append(line.strip())

# Critical warnings to flag:
# - "lost particle"
# - "negative cross section"
# - "bad trouble in subroutine"
# - "error termination"
# - "geometry error"
```

**Statistical Quality Checks (10 checks):**
```python
# From Tally Fluctuation Chart in OUTP:
#
# results   tally            mean     mean      vov    slope      fom
#  check  number             x        x/nps     ...     10th
#    1       14  4.5678E-02  4.5678E-08  0.0023   3.5   1234.5
#
# 10 Statistical Quality Checks (Chapter 3):
# 1. Mean should not change significantly in last half
# 2. Relative error R < 0.10 (10%)
# 3. Variance of Variance (VOV) < 0.10
# 4. Figure of Merit (FOM) should be constant ±10%
# 5. FOM > 100 for reliable results
# 6. Slope of history score fits 3.0-10.0 range
# 7. No zero or negative tally bins
# 8. All 10 statistical tests passed
# 9. Relative error decreasing as ~1/√N
# 10. PDF shows reasonable distribution

statistical_quality = {
    'mean': 4.5678e-2,
    'relative_error': 0.0123,  # 1.23%
    'vov': 0.0023,  # < 0.10 ✓
    'slope': 3.5,  # In range [3, 10] ✓
    'fom': 1234.5,
    'tests_passed': '10/10'
}
```

**Mesh Tally Extraction:**
```python
# HDF5 mesh tally structure (Appendix D.6):
# /results/mesh_tally_N/
#   energy_total/time_total/
#     values (dataset: shape based on mesh)
#     errors (dataset: relative errors)
#   energy_bin_1/time_total/
#     values
#     errors
#   geometry/
#     coordinates (Nx3: x,y,z for N nodes)
#     connectivity (element-to-node mapping)

with h5py.File('runtpe.h5', 'r') as f:
    # For rectangular mesh (FMESH14):
    mesh_14 = f['/results/mesh_tally_14/energy_total/time_total']
    values = mesh_14['values'][:]  # Shape: (nx, ny, nz)
    errors = mesh_14['errors'][:]

    # Get mesh dimensions from attributes
    nx = mesh_14.attrs['nx']
    ny = mesh_14.attrs['ny']
    nz = mesh_14.attrs['nz']

    # Get mesh boundaries
    x_bounds = mesh_14.attrs['x_bounds']  # [xmin, xmax]
    y_bounds = mesh_14.attrs['y_bounds']
    z_bounds = mesh_14.attrs['z_bounds']
```

### Step 5: Present Results

**Organize by user's goal:**

**For validation:**
- Report warnings/errors first
- Check normal termination
- Verify statistical quality
- Flag any fatal issues

**For analysis:**
- Extract tally values with uncertainties
- Present in user's requested units
- Provide statistical quality assessment
- Suggest visualization approaches

**For visualization:**
- Extract mesh data as numpy arrays
- Provide coordinate information
- Suggest ParaView/VisIt workflow
- Generate XDMF if needed

## Output File Format Details

### OUTP Structure (Main ASCII Output)

**File sections in order:**
```
1. Header
   - Problem title
   - Code version (e.g., "mcnp version 6.3.0")
   - Date and time
   - Random number seed

2. Input Echo
   - Complete input file listing with line numbers

3. Problem Summary Tables (Chapter 3)
   - Table 10: Source distribution
   - Table 30: Surfaces (with transformations)
   - Table 40: Cells (volumes, masses)
   - Table 60: Cell materials
   - Table 90: Material compositions (mass fractions)
   - Table 100: Cross-section tables loaded
   - Table 110: Activity by cell (Bq/Ci)

4. Execution Progress
   - NPS checkpoints
   - KCODE cycle information (criticality)
   - Dump file creation

5. Tally Results
   - For each tally (F1, F2, ..., F4, F6, F8)
   - Values by bin (energy, time, cell, surface)
   - Relative errors (fractional, not %)
   - VOV, FOM, slope

6. Tally Fluctuation Charts
   - 10 statistical quality checks per tally
   - Status: passed/missed per check
   - Recommendations

7. Computer Time Summary
   - Total execution time
   - Time per particle history

8. Termination Message
   - "mcnp run terminated when [NPS] particle histories were done."
   - OR error termination message
```

**Parsing markers:**
```python
# Key text patterns to search for:
TALLY_START = r"1tally\s+(\d+)"  # Start of tally section
WARNING = r"warning\.|^\s*warning"  # Warning message
ERROR = r"fatal error|error termination"  # Fatal errors
TERMINATION_NORMAL = r"mcnp run terminated when"
TERMINATION_ERROR = r"error termination"
KCODE_RESULTS = r"the final estimated"  # Criticality results
TABLE_START = r"1\s*\w+ table"  # Problem summary tables
```

### MCTAL Format (Machine-Readable Tallies)

**File structure:**
```
Line 1: kod ver probid
  kod = code identifier
  ver = version
  probid = problem ID

Line 2: knod ntal jtty npert (comment)
  ntal = number of tallies
  npert = number of perturbations

Line 3: nps rnr
  nps = histories run
  rnr = random number seed

Line 4+: Tally sections
  For each tally:
    Header line: f d u s m c e t
      f = tally number
      d = detector flag
      u = user bin flag
      s = segment flag
      m = multiplier flag
      c = cosine flag
      e = energy flag
      t = time flag

    Dimension lines:
      Number of bins for each dimension
      Bin boundaries

    Data lines:
      Value Error (repeated for all bins)

    TFC line (optional):
      Tally fluctuation chart 8 quantities
```

**Advantages over OUTP:**
- Structured format easier to parse programmatically
- Used by MCPLOT for visualization
- Contains all binning details
- No formatting ambiguities

### HDF5 Format (RUNTPE.H5)

**Overall structure (Appendix D):**
```
/
├── /config_control
│   └── Attributes: code version, compile info
├── /problem_info
│   ├── title (dataset)
│   ├── nps (dataset)
│   ├── random_seed (dataset)
│   ├── mode (dataset: particle types)
│   └── ... (other problem parameters)
├── /results
│   ├── /mesh_tally_14
│   │   ├── /energy_total
│   │   │   ├── /time_total
│   │   │   │   ├── values (dataset)
│   │   │   │   ├── errors (dataset)
│   │   │   │   └── @attributes (tally type, units)
│   │   │   └── /time_bin_1
│   │   │       ├── values
│   │   │       └── errors
│   │   ├── /energy_bin_1
│   │   │   └── ...
│   │   └── /geometry
│   │       ├── coordinates (Nx3 dataset)
│   │       ├── connectivity (element map)
│   │       └── @attributes (element type)
│   └── /mesh_tally_24
│       └── ...
├── /particle_1 (PTRAC output, Appendix D.3)
│   └── /step_data
│       ├── nps (history numbers)
│       ├── x, y, z (positions)
│       ├── u, v, w (directions)
│       ├── energy
│       ├── time
│       ├── event_type (scatter, capture, etc.)
│       └── cell
├── /particle_2
│   └── ...
├── /fission_matrix (Appendix D.5)
│   ├── row_ptr (CSR format)
│   ├── col_ind
│   └── values
└── /dumps
    ├── /dump_1
    │   └── (complete problem state at dump)
    └── /dump_2
        └── ...
```

**Navigation with h5py:**
```python
import h5py

with h5py.File('runtpe.h5', 'r') as f:
    # List all groups
    print("HDF5 structure:")
    f.visititems(lambda name, obj: print(f"  {name}"))

    # Check if path exists
    if '/results/mesh_tally_14' in f:
        mesh = f['/results/mesh_tally_14']

        # List attributes
        for key, val in mesh.attrs.items():
            print(f"@{key} = {val}")

        # Read dataset
        values = f['/results/mesh_tally_14/energy_total/time_total/values'][:]
```

**Key HDF5 concepts:**
- **Groups**: Like directories, organize data hierarchically
- **Datasets**: N-dimensional arrays (like numpy arrays)
- **Attributes**: Metadata attached to groups/datasets
- **Slicing**: Can read partial data: `dataset[0:100]` reads first 100 elements

### XDMF Format (Visualization Descriptor)

**Purpose:** XML file that tells ParaView/VisIt where to find mesh geometry and data in HDF5 files

**Example XDMF file (Appendix D.4):**
```xml
<?xml version="1.0" ?>
<Xdmf Version="2.0">
  <Domain>
    <Grid Name="TimeSeries" GridType="Collection" CollectionType="Temporal">

      <!-- Time step 1 -->
      <Grid Name="mesh_tally_14_t0" GridType="Uniform">
        <Time Value="0.0" />

        <!-- Mesh topology -->
        <Topology TopologyType="Hexahedron" NumberOfElements="1000">
          <DataItem Format="HDF" Dimensions="1000 8">
            runtpe.h5:/results/mesh_tally_14/geometry/connectivity
          </DataItem>
        </Topology>

        <!-- Mesh geometry (node coordinates) -->
        <Geometry GeometryType="XYZ">
          <DataItem Format="HDF" Dimensions="8000 3">
            runtpe.h5:/results/mesh_tally_14/geometry/coordinates
          </DataItem>
        </Geometry>

        <!-- Tally data (flux values) -->
        <Attribute Name="flux" AttributeType="Scalar" Center="Cell">
          <DataItem Format="HDF" Dimensions="1000">
            runtpe.h5:/results/mesh_tally_14/energy_total/time_total/values
          </DataItem>
        </Attribute>

        <!-- Relative errors -->
        <Attribute Name="error" AttributeType="Scalar" Center="Cell">
          <DataItem Format="HDF" Dimensions="1000">
            runtpe.h5:/results/mesh_tally_14/energy_total/time_total/errors
          </DataItem>
        </Attribute>
      </Grid>

      <!-- Additional time steps... -->

    </Grid>
  </Domain>
</Xdmf>
```

**Key XDMF elements:**
- **Topology**: Element type (Tetrahedron, Hexahedron, etc.) and connectivity
- **Geometry**: Node coordinates (XYZ format)
- **Attribute**: Field data (scalars, vectors) mapped to cells or nodes
- **DataItem**: Reference to HDF5 dataset path
- **Temporal Collection**: Time series of mesh tallies

**Usage workflow:**
1. MCNP generates `runtpe.h5` with mesh tally data
2. User creates/generates `.xdmf` descriptor pointing to HDF5
3. Open `.xdmf` in ParaView (automatically loads linked HDF5 data)
4. Visualize with color maps, slicing, iso-surfaces

### PTRAC Format (Particle Tracking)

**Purpose:** Record particle trajectories for detailed physics analysis

**HDF5 PTRAC structure (Appendix D.3):**
```
/particle_1/
  step_data/
    nps (dataset: history number for each step)
    x, y, z (datasets: position)
    u, v, w (datasets: direction cosines)
    energy (dataset: particle energy in MeV)
    time (dataset: time in shakes)
    weight (dataset: particle weight)
    cell (dataset: current cell number)
    event_type (dataset: scatter, capture, bank, etc.)

/particle_2/
  step_data/
    ...

... (one group per tracked particle)
```

**Event types:**
- 1000: Source particle
- 2000: Collision (scatter)
- 3000: Surface crossing
- 4000: Termination (capture, escape)
- 5000: Banking (fission, secondary production)

**Extraction example:**
```python
import h5py
import matplotlib.pyplot as plt

with h5py.File('ptrac.h5', 'r') as f:
    # Plot trajectory of particle 1
    p1 = f['/particle_1/step_data']
    x = p1['x'][:]
    y = p1['y'][:]
    z = p1['z'][:]
    energy = p1['energy'][:]

    # 3D trajectory
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Color by energy
    scatter = ax.scatter(x, y, z, c=energy, cmap='viridis')
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    plt.colorbar(scatter, label='Energy (MeV)')
    plt.title('Particle Trajectory')
    plt.show()
```

### Fission Matrix (Criticality Calculations)

**Format:** Compressed Sparse Row (CSR) - efficient for sparse matrices

**Structure (Appendix D.5):**
```
row_ptr[i]: Starting index in col_ind/values for row i
col_ind[j]: Column index of non-zero element j
values[j]: Value of non-zero element j

Matrix element (i, k) = values[j] where:
  j in range(row_ptr[i], row_ptr[i+1])
  col_ind[j] == k
```

**Example:**
```python
import h5py
import numpy as np
from scipy.sparse import csr_matrix

with h5py.File('runtpe.h5', 'r') as f:
    row_ptr = f['/fission_matrix/row_ptr'][:]
    col_ind = f['/fission_matrix/col_ind'][:]
    values = f['/fission_matrix/values'][:]

    # Reconstruct sparse matrix
    n_rows = len(row_ptr) - 1
    n_cols = row_ptr[-1]  # or get from attributes

    fission_matrix = csr_matrix((values, col_ind, row_ptr), shape=(n_rows, n_cols))

    # Convert to dense for visualization (if small enough)
    dense = fission_matrix.toarray()

    import matplotlib.pyplot as plt
    plt.imshow(dense, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Fission source contribution')
    plt.title('Fission Matrix')
    plt.xlabel('Source mesh element')
    plt.ylabel('Fission mesh element')
    plt.show()
```

## Common Parsing Tasks

### Task 1: Quick Validation Check

**Goal:** Verify simulation completed normally and check for warnings

```python
from skills.output_analysis.mcnp_output_analyzer import MCNPOutputAnalyzer

analyzer = MCNPOutputAnalyzer()
analysis = analyzer.analyze_output('output.o')

# Report summary
print(f"Terminated normally: {analysis['summary']['terminated_normally']}")
print(f"Warnings: {analysis['summary']['n_warnings']}")
print(f"Errors: {analysis['summary']['n_errors']}")

# Show warnings
if analysis['details']['warnings']:
    print("\nWARNINGS:")
    for w in analysis['details']['warnings']:
        print(f"  {w}")

# Show errors
if analysis['details']['errors']:
    print("\nERRORS:")
    for e in analysis['details']['errors']:
        print(f"  {e}")
```

### Task 2: Extract Specific Tally

**Goal:** Get tally values with uncertainties for analysis

```python
# From MCTAL file (easier to parse)
from skills.output_analysis.mcnp_mctal_processor import MCNPMCTALProcessor

processor = MCNPMCTALProcessor()
mctal = processor.parse_mctal('mctal')

# Extract F4 tally
tally_4 = processor.extract_tally(mctal, 4)

# Present results
print(f"Tally F{tally_4['number']}")
print(f"Type: {tally_4['type']}")
print(f"Particle: {tally_4['particle']}")
print(f"\nEnergy Bin Results:")

for i, (energy, value, error) in enumerate(zip(tally_4['energy_bins'],
                                                 tally_4['values'],
                                                 tally_4['errors'])):
    print(f"  {energy[0]:.2e} - {energy[1]:.2e} MeV: {value:.4e} ± {error:.2%}")
```

### Task 3: Extract Mesh Tally for Plotting

**Goal:** Get mesh data as numpy arrays for visualization

```python
import h5py
import numpy as np

# Extract from HDF5
with h5py.File('runtpe.h5', 'r') as f:
    mesh_path = '/results/mesh_tally_14/energy_total/time_total'

    # Get data
    flux = f[mesh_path + '/values'][:]  # Shape: (nx, ny, nz)
    errors = f[mesh_path + '/errors'][:]

    # Get mesh dimensions from attributes
    nx = f[mesh_path].attrs['nx']
    ny = f[mesh_path].attrs['ny']
    nz = f[mesh_path].attrs['nz']

    # Get spatial bounds
    xmin, xmax = f[mesh_path].attrs['x_bounds']
    ymin, ymax = f[mesh_path].attrs['y_bounds']
    zmin, zmax = f[mesh_path].attrs['z_bounds']

# Create coordinate arrays
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
z = np.linspace(zmin, zmax, nz)

# Now can plot with matplotlib, mayavi, etc.
import matplotlib.pyplot as plt

# 2D slice at z midpoint
z_mid = nz // 2
plt.imshow(flux[:, :, z_mid].T, extent=[xmin, xmax, ymin, ymax],
           origin='lower', cmap='viridis')
plt.colorbar(label='Flux')
plt.xlabel('X (cm)')
plt.ylabel('Y (cm)')
plt.title(f'Neutron Flux at z={z[z_mid]:.1f} cm')
plt.show()
```

### Task 4: Prepare for ParaView

**Goal:** Guide user to visualize mesh tallies in ParaView

**Instructions:**
```
1. Locate your XDMF file (e.g., meshtal.xdmf)
   - Generated automatically if XDMF card in input
   - Or create manually pointing to runtpe.h5

2. Open ParaView

3. File → Open → Select meshtal.xdmf

4. Click "Apply" in Properties panel

5. In Pipeline Browser, select your mesh

6. Change representation from "Outline" to "Surface"

7. In coloring dropdown, select field (e.g., "flux", "error")

8. Visualization options:
   - Slice: Add filter → Slice → Select normal direction
   - Iso-surface: Add filter → Contour → Select value
   - Volume render: Change representation to "Volume"
   - Clip: Add filter → Clip → Define plane

9. Export images: File → Save Screenshot

10. Export data: File → Save Data → CSV or spreadsheet
```

### Task 5: Batch Process Multiple Runs

**Goal:** Extract same tally from multiple output files (e.g., parameter study)

```python
import os
from skills.output_analysis.mcnp_mctal_processor import MCNPMCTALProcessor

processor = MCNPMCTALProcessor()

# List of MCTAL files
mctal_files = ['run1/mctal', 'run2/mctal', 'run3/mctal', 'run4/mctal']
tally_number = 4

results = []
for mctal_file in mctal_files:
    mctal = processor.parse_mctal(mctal_file)
    tally = processor.extract_tally(mctal, tally_number)

    # Extract total value
    total_value = tally['values'][-1]  # Last bin often "total"
    total_error = tally['errors'][-1]

    results.append({
        'file': mctal_file,
        'value': total_value,
        'error': total_error
    })

# Create comparison table
import pandas as pd
df = pd.DataFrame(results)
print(df)

# Plot comparison
import matplotlib.pyplot as plt
plt.errorbar(range(len(results)),
             df['value'],
             yerr=df['value'] * df['error'],  # Convert relative to absolute
             fmt='o-')
plt.xlabel('Run number')
plt.ylabel(f'Tally {tally_number} value')
plt.title('Parameter Study Results')
plt.grid(True)
plt.show()
```

## Integration with Other Skills

After parsing output, recommend:

- **mcnp-tally-analyzer**: For detailed tally analysis, unit conversions, dose calculations
- **mcnp-statistics-checker**: For comprehensive statistical quality validation
- **mcnp-plotter**: For automated plotting of tally results
- **mcnp-output-comparator**: For comparing multiple runs (parameter studies)

## Important Parsing Principles

1. **Check file completeness first**
   - Interrupted runs produce incomplete output files
   - Check for normal termination message
   - HDF5 files may be corrupted if run crashed

2. **Relative errors are fractional, not percentages**
   - MCNP reports: 0.0123 means 1.23% (NOT 12.3%)
   - Always convert for user presentation: `error * 100`
   - Formula: Absolute uncertainty = value × relative_error

3. **HDF5 groups use path syntax**
   - Use '/' separators like filesystem paths
   - Check if path exists before accessing: `if path in f:`
   - Use `.visititems()` to explore unknown structure

4. **XDMF is just a roadmap**
   - Actual data lives in HDF5 files
   - XDMF can be regenerated if lost
   - Errors in XDMF don't corrupt data

5. **Energy/time bins have boundaries, not centers**
   - Bin specification: [E_low, E_high]
   - "Total" bin often last entry
   - Energy bins in MeV, time bins in shakes

6. **Statistical quality before value accuracy**
   - A result with R=0.50 is unreliable even if it "looks reasonable"
   - Check 10 statistical tests
   - FOM should be stable across bins

7. **Mesh tally indexing**
   - HDF5 arrays are 0-indexed (Python convention)
   - MCNP mesh numbering is 1-indexed
   - Coordinate systems: match input FMESH card

8. **Warning severity matters**
   - "lost particle" → serious geometry error
   - "adjusting weight window" → informational
   - "bad trouble" → fatal physics error
   - "negative score" → variance reduction issue

9. **PTRAC files can be huge**
   - Read in chunks or select specific particles
   - Use HDF5 slicing: `dataset[0:1000]`
   - Filter by event type to reduce data

10. **CSR fission matrix is sparse**
    - Most elements are zero (not stored)
    - Use scipy.sparse for manipulation
    - Converting to dense may exhaust memory

## Example Workflows

### Example 1: Post-Run Validation

```
User: "Can you check my MCNP output for errors?"

Claude: I'll parse your output file and check for warnings, errors, and verify normal termination.

[Reads .claude/commands/mcnp-output-parser.md]
[Uses MCNPOutputAnalyzer]

**Output Analysis Results:**

✓ Simulation terminated normally after 1,000,000 histories

**Warnings Found (2):**

1. Line 1247: "warning. neutron energy cutoff is below some cross-section tables"
   Impact: May affect low-energy transport accuracy
   Recommendation: Check PHYS:N card emax parameter

2. Line 3891: "warning. tally 4 has relative error = 0.15"
   Impact: Statistical quality marginal (>10%)
   Recommendation: Increase NPS or improve variance reduction

**No Fatal Errors**

**Tally Summary:**
- F4 (cell flux): 4.567E-03 ± 15.0% ⚠ (high uncertainty)
- F6 (energy deposition): 2.345E-04 ± 3.2% ✓ (good)
- F14 (mesh flux): See mesh tally output

**Recommendations:**
1. Run longer to reduce F4 uncertainty below 10%
2. Check energy cutoff settings for thermal calculations
3. All other tallies have good statistical quality

Would you like me to:
1. Extract detailed tally results?
2. Check statistical quality in detail (10 tests)?
3. Plot tally convergence?
```

### Example 2: Extract Mesh Tally

```
User: "Extract the flux distribution from mesh tally 14"

Claude: I'll extract mesh tally 14 from your HDF5 output file.

[Reads .claude/commands/mcnp-output-parser.md]
[Opens runtpe.h5 with h5py]

**Mesh Tally 14 - Neutron Flux:**

Mesh type: Rectangular (Cartesian)
Dimensions: 20 × 20 × 20 = 8000 voxels

Spatial extent:
  X: -50.0 to 50.0 cm (20 bins, 5.0 cm width)
  Y: -50.0 to 50.0 cm (20 bins, 5.0 cm width)
  Z: -100.0 to 100.0 cm (20 bins, 10.0 cm width)

Energy bins: Total (all energies)
Time bins: Total (all times)

**Statistical Summary:**
- Mean flux: 2.345E-04 n/cm²
- Max flux: 5.678E-03 n/cm² at (x=0, y=0, z=10 cm)
- Min flux: 1.234E-07 n/cm² at (x=-45, y=-45, z=-90 cm)
- Mean relative error: 2.8% ✓
- Max relative error: 8.9% ✓

Data extracted to numpy array (shape: 20×20×20)

Would you like me to:
1. Plot 2D slices?
2. Export to CSV for analysis?
3. Generate visualization in ParaView?
4. Show high-flux regions?
```

### Example 3: Tally Comparison

```
User: "Compare tally 4 across my three sensitivity runs"

Claude: I'll extract F4 from all three MCTAL files and compare the results.

[Reads .claude/commands/mcnp-output-parser.md]
[Parses mctal files from run1/, run2/, run3/]

**F4 Tally Comparison - Cell Flux:**

Case 1 (baseline):
  Total: 1.234E-02 ± 2.1%

Case 2 (enrichment +5%):
  Total: 1.456E-02 ± 2.3%
  Change: +18.0% ± 3.2%

Case 3 (density +10%):
  Total: 1.389E-02 ± 2.0%
  Change: +12.6% ± 2.9%

**Energy-Dependent Comparison:**

Energy Range       Case 1         Case 2         Case 3
0.0 - 1.0 MeV    4.56E-03±2.5%  5.23E-03±2.7%  5.01E-03±2.4%
1.0 - 5.0 MeV    3.89E-03±3.1%  4.67E-03±3.3%  4.45E-03±3.0%
5.0 - 14.0 MeV   2.89E-03±4.2%  3.56E-03±4.5%  3.43E-03±4.1%

All results have acceptable statistical quality (<5% error)

[Would generate comparison plot]

The enrichment increase has larger impact (+18%) than density increase (+12%) on flux.
```

## Code Style Guidelines

When using parsing modules:
- Always check for normal termination first
- Report errors before warnings
- Present uncertainties with values
- Use scientific notation for very small/large values
- Convert relative errors to percentages for users
- Provide context (what tally measures, units)
- Offer next steps (plotting, analysis, validation)

## Dependencies

**Required Python packages:**
- `h5py` - HDF5 file I/O
- `numpy` - Array operations
- `xml.etree.ElementTree` - XDMF parsing (built-in)

**Required components:**
- Python module: `skills/output_analysis/mcnp_output_analyzer.py`
- Python module: `skills/output_analysis/mcnp_mctal_processor.py`
- Output parser: `parsers/output_parser.py`
- Reference: `.claude/commands/mcnp-output-parser.md` (detailed procedures)

**Optional packages:**
- `pandas` - DataFrame for tabular data
- `matplotlib` - Plotting
- `scipy.sparse` - Sparse matrix operations (fission matrix)

## References

**Primary References:**
- `.claude/commands/mcnp-output-parser.md` - Complete parsing procedures for all formats
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Quick reference for output formats
- Chapter 3: Introduction to MCNP Usage (statistical quality checks, validation)
- Chapter 8: Unstructured Mesh (mesh geometry, tallies)

**HDF5 Output Formats (Appendix D):**
- Appendix D.3: Particle Track Output (PTRAC HDF5 structure)
- Appendix D.4: Mesh Tally XDMF (visualization format)
- Appendix D.5: Fission Matrix (CSR sparse format)
- Appendix D.6: Unstructured Mesh HDF5 (mesh geometry storage)
- Appendix D.7: Unstructured Mesh Legacy (deprecated EEOUT format)
- Appendix D.8: HDF5 Script (Python utility examples)
- Appendix D.9: inxc File Structure (cross-section editing)

**Utility Programs:**
- Appendix E.6: Merge ASCII Tally (combining MCTAL files)
- Appendix E.7: Merge Mesh Tally (combining mesh results)
- Appendix E.11: UM Post Processing (deprecated um_post_op utility)

**Key Sections:**
- §3.4.2.4: Ten statistical checks for tally reliability
- §8.5: Mesh tally output formats
- Table D.1: PTRAC event types
- Table D.3: HDF5 group hierarchy
- Figure D.2: XDMF structure example

**Related Skills:**
- mcnp-tally-analyzer: Detailed tally analysis
- mcnp-statistics-checker: Statistical quality validation
- mcnp-plotter: Automated plotting
- mcnp-mesh-builder: Creating mesh tallies (input side)
