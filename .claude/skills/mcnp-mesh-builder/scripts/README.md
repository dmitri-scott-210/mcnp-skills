# MCNP Mesh Builder Scripts

**Purpose:** Python utilities for MCNP6 mesh tally generation, visualization, and format conversion.

**Location:** `.claude/skills/mcnp-mesh-builder/scripts/`

---

## Scripts Overview

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `fmesh_generator.py` | Generate FMESH cards programmatically | numpy |
| `mesh_visualizer.py` | Visualize mesh geometry and tallies | numpy, matplotlib, h5py |
| `mesh_converter.py` | Convert between mesh formats | meshio |

---

## Installation

### Required Dependencies

```bash
pip install numpy matplotlib h5py meshio
```

**Individual packages:**
- `numpy` - Numerical arrays and calculations
- `matplotlib` - 2D plotting
- `h5py` - HDF5 file reading (for XDMF mesh output)
- `meshio` - Mesh format conversion (GMSH, ABAQUS, VTK, etc.)

---

## Script 1: fmesh_generator.py

**Purpose:** Programmatically generate FMESH card specifications for MCNP6 input files.

### Features

- Cartesian (XYZ) and cylindrical (RZT) mesh generation
- Automatic binning optimization (uniform, logarithmic, adaptive)
- Energy and time binning support
- Total bin count calculation
- Command-line interface for quick generation

### Usage

**Basic Cartesian mesh:**
```bash
python fmesh_generator.py --geometry XYZ \
                          --origin 0 0 0 \
                          --extent 100 100 100 \
                          --bins 20 20 20 \
                          --output xdmf
```

**Output:**
```
FMESH4:N GEOM=XYZ
          ORIGIN=0.0 0.0 0.0
          IMESH=100.0  IINTS=20
          JMESH=100.0  JINTS=20
          KMESH=100.0  KINTS=20
          OUT=xdmf

c Total bins: 8,000
```

**Cylindrical mesh with energy bins:**
```bash
python fmesh_generator.py --geometry RZT \
                          --origin 0 0 -50 \
                          --extent 50 50 100 \
                          --bins 25 50 36 \
                          --energy 1e-10 1e-6 0.1 1 14
```

**Custom tally number and particle:**
```bash
python fmesh_generator.py --tally 24 --particle P \
                          --origin -50 -50 -50 \
                          --extent 100 100 100 \
                          --bins 30 30 30
```

### Python API

```python
from fmesh_generator import FMESHGenerator, create_uniform_cartesian

# Method 1: High-level helper
card = create_uniform_cartesian(
    origin=(0, 0, 0),
    extent=(100, 100, 100),
    bins=(20, 20, 20),
    tally_number=4,
    particle='N'
)
print(card)

# Method 2: Full control
gen = FMESHGenerator(tally_number=14, particle='P')
gen.set_cartesian(
    origin=(0, 0, 0),
    x_bounds=[50, 100], x_bins=[25, 25],  # Non-uniform
    y_bounds=[100], y_bins=[50],
    z_bounds=[100], z_bins=[50]
)
gen.set_energy_bins([1e-10, 1e-6, 0.1, 1, 14])
gen.set_output('xdmf')
card = gen.generate()
print(card)

# Calculate total bins
total_bins = gen.calculate_bins()
print(f"Total bins: {total_bins:,}")
```

**Advanced examples:**

```python
# Logarithmic radial binning (for shielding)
from fmesh_generator import create_logarithmic_radial

card = create_logarithmic_radial(
    origin=(0, 0, 0),
    r_min=0.1, r_max=100, r_bins=20,  # Log spacing 0.1-100 cm
    z_min=0, z_max=50, z_bins=25,
    tally_number=14,
    particle='N'
)
```

---

## Script 2: mesh_visualizer.py

**Purpose:** Visualize MCNP mesh tally geometry for validation and quality checking.

### Features

- Plot 2D slices of mesh (XY, XZ, YZ planes)
- Support for FMESH (XYZ, RZT) and unstructured mesh (UM)
- Parse FMESH cards directly from MCNP input files
- Read XDMF/HDF5 mesh output files
- Print mesh summary statistics

### Usage

**Visualize FMESH from input file:**
```bash
python mesh_visualizer.py input.i --tally 4 --slice XY
```

**Visualize UM from output file:**
```bash
python mesh_visualizer.py meshtal.xdmf --slice XZ --position 0
```

**Print mesh summary only (no plot):**
```bash
python mesh_visualizer.py input.i --tally 14 --summary
```

**Save plot to file:**
```bash
python mesh_visualizer.py input.i --tally 4 --slice XY --output mesh.png
```

### Example Output

```
============================================================
MESH SUMMARY
============================================================
Mesh Type: XYZ
Origin: (0.00, 0.00, 0.00)
I-direction boundaries: 1
J-direction boundaries: 1
K-direction boundaries: 1
============================================================
```

**For unstructured mesh:**
```
============================================================
MESH SUMMARY
============================================================
Mesh Type: UM
Vertices: 45,231
Elements: 250,487
============================================================
```

### Python API

```python
from mesh_visualizer import MeshVisualizer

vis = MeshVisualizer()

# Load from MCNP input file
vis.parse_fmesh_card('input.i', tally_number=4)

# Print summary
vis.print_summary()

# Plot XY slice at Z=0
vis.plot_2d_slice(plane='XY', position=0.0, output_file='mesh_xy.png')

# Load from XDMF output
vis.load_xdmf('meshtal.xdmf')
vis.plot_2d_slice(plane='XZ', position=0.0)
```

---

## Script 3: mesh_converter.py

**Purpose:** Convert between mesh file formats for MCNP unstructured mesh (UM) import.

### Features

- Convert GMSH ↔ ABAQUS ↔ VTK ↔ CGAL formats
- Auto-detect file format from extension
- Validate mesh files (check for errors, print summary)
- List supported formats

### Usage

**Convert GMSH to VTK:**
```bash
python mesh_converter.py input.msh --output output.vtk
```

**Convert ABAQUS to GMSH:**
```bash
python mesh_converter.py phantom.inp --output phantom.msh
```

**Validate mesh file:**
```bash
python mesh_converter.py reactor.msh --validate
```

**Example validation output:**
```
============================================================
MESH VALIDATION: reactor.msh
============================================================

Format: gmsh
Vertices: 45,231

Element types:
  tetra: 250,487 elements

Bounding box:
  X: [-50.000, 50.000]
  Y: [-50.000, 50.000]
  Z: [0.000, 100.000]

Validation checks:
  ✅ No duplicate vertices
  ✅ All element types supported by MCNP
  ✅ No quadratic elements

============================================================
```

**List supported formats:**
```bash
python mesh_converter.py --list-formats
```

**Output:**
```
Supported mesh formats:

Format          Extension    meshio ID    Description
---------------------------------------------------------------------------
GMSH            .msh         gmsh         Open-source mesh generator
ABAQUS          .inp         abaqus       Abaqus FEA input
VTK Legacy      .vtk         vtk          VTK legacy ASCII format
VTK XML         .vtu         vtu          VTK XML unstructured grid
CGAL/Medit      .mesh        medit        CGAL mesh format
STL             .stl         stl          Stereolithography (surface only)
OBJ             .obj         obj          Wavefront OBJ (surface only)

Note: MCNP supports tetrahedra, hexahedra, wedges, and pyramids only.
      Use GMSH or ABAQUS formats for best MCNP compatibility.
```

### Python API

```python
from mesh_converter import convert_mesh, validate_mesh

# Convert formats
convert_mesh('input.msh', 'output.vtk')

# Validate before using in MCNP
validate_mesh('reactor.msh')
```

---

## Common Workflows

### Workflow 1: Generate FMESH Card

```bash
# Generate card
python fmesh_generator.py --origin 0 0 0 --extent 100 100 100 --bins 20 20 20 > fmesh.txt

# Visualize to verify
python mesh_visualizer.py input.i --tally 4 --slice XY
```

### Workflow 2: CAD to MCNP UM

```bash
# 1. Create mesh in GMSH from CAD
gmsh -3 model.step -o model.msh

# 2. Validate mesh
python mesh_converter.py model.msh --validate

# 3. Convert to VTK (if needed)
python mesh_converter.py model.msh --output model.vtk

# 4. Visualize
python mesh_visualizer.py model.msh --slice XY
```

### Workflow 3: Verify Mesh Extent

```bash
# Check mesh bounds before running MCNP
python mesh_visualizer.py input.i --tally 14 --summary

# Plot to verify mesh covers geometry
python mesh_visualizer.py input.i --tally 14 --slice XY --output check.png
```

---

## Error Handling

### Common Errors

**1. Import Error: meshio not found**
```
Error: meshio not installed.
Install with: pip install meshio
```

**Fix:** `pip install meshio`

**2. HDF5 Import Error**
```
Warning: h5py not available. HDF5 visualization disabled.
```

**Fix:** `pip install h5py` (only needed for XDMF visualization)

**3. Matplotlib Display Error**
```
UserWarning: Matplotlib is currently using agg, which is a non-GUI backend
```

**Fix:** Use `--output file.png` to save plot instead of displaying

**4. Invalid Tally Number**
```
ValueError: FMESH tally number must end in 4 (e.g., 4, 14, 24)
```

**Fix:** Use tally numbers 4, 14, 24, 34, ..., 994

---

## Script Testing

### Test fmesh_generator.py

```bash
# Test Cartesian
python fmesh_generator.py --geometry XYZ --origin 0 0 0 --extent 10 10 10 --bins 5 5 5

# Test cylindrical
python fmesh_generator.py --geometry RZT --origin 0 0 0 --extent 50 50 100 --bins 10 20 10

# Test energy binning
python fmesh_generator.py --geometry XYZ --origin 0 0 0 --extent 100 100 100 \
                          --bins 20 20 20 --energy 1e-10 1e-6 0.1 1 14
```

### Test mesh_visualizer.py

```bash
# Create test MCNP input with FMESH
cat > test.i << 'EOF'
Test input
c ===========================
c Cell Cards
c ===========================
1    1  -1.0  -1   IMP:N=1
2    0         1   IMP:N=0
c
c ===========================
c Surface Cards
c ===========================
1    SO  100
c
c ===========================
c Data Cards
c ===========================
MODE N
M1   1001 2  8016 1
SDEF  POS=0 0 0  ERG=14
FMESH4:N  GEOM=XYZ
          ORIGIN=-50 -50 -50
          IMESH=50  IINTS=20
          JMESH=50  JINTS=20
          KMESH=50  KINTS=20
NPS  1e6
EOF

# Test visualization
python mesh_visualizer.py test.i --tally 4 --slice XY --summary
```

### Test mesh_converter.py

```bash
# List formats
python mesh_converter.py --list-formats

# If you have test mesh files:
python mesh_converter.py test.msh --validate
python mesh_converter.py test.msh --output test.vtk
```

---

## Integration with MCNP Skills

These scripts integrate with other MCNP skills:

**With mcnp-input-builder:**
- Use `fmesh_generator.py` output directly in MCNP input files

**With mcnp-output-parser:**
- Use `mesh_visualizer.py` to visualize XDMF output from MCNP runs

**With mcnp-plotter:**
- Combine mesh overlay with geometry plots for validation

**With mcnp-tally-analyzer:**
- Convert mesh formats for post-processing workflows

---

## License

These scripts are part of the MCNP Skills Project and are provided as-is for educational and research purposes.

---

## Support

For issues or questions, see:
- Main skill documentation: `../SKILL.md`
- Unstructured mesh guide: `../unstructured_mesh_guide.md`
- Mesh optimization guide: `../mesh_optimization_guide.md`

---

**END OF README**
