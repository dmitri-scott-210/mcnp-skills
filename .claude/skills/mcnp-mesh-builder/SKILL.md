---
category: E
name: mcnp-mesh-builder
description: Build TMESH, FMESH, and unstructured mesh (UM) tally specifications for spatial distribution analysis
version: 2.0.0
auto_activate: true
activation_keywords:
  - mesh tally
  - FMESH
  - TMESH
  - spatial distribution
  - mesh geometry
  - superimposed mesh
  - XDMF
  - ParaView
  - mesh visualization
  - mesh binning
dependencies:
  - mcnp-input-builder
  - mcnp-output-parser
  - mcnp-plotter
related_skills:
  - mcnp-tally-analyzer
  - mcnp-statistics-checker
output_formats:
  - MCNP input cards (TMESH/FMESH)
  - Mesh specification
  - Visualization guidance
---

# mcnp-mesh-builder

**Purpose**: Build TMESH, FMESH, and unstructured mesh (UM) tally specifications for analyzing spatial distributions of neutron/photon flux, energy deposition, and reaction rates over regular or irregular grids.

## What Are Mesh Tallies?

**Mesh tallies** superimpose a grid over the problem geometry to calculate tallies in each mesh cell, providing spatial distribution data.

**Three types:**
1. **FMESH** - Modern structured mesh (Cartesian or cylindrical grids)
2. **TMESH** - Legacy structured mesh (backward compatibility)
3. **Unstructured Mesh (UM)** - Irregular mesh from external tools (GMSH, ABAQUS, etc.)

### TMESH vs FMESH vs UM

| Feature | TMESH | FMESH | UM (Unstructured) |
|---------|-------|-------|-------------------|
| **Format** | Legacy (pre-MCNP6) | Modern (MCNP6+) | MCNP6+ with EMBED |
| **Grid Type** | Regular | Regular (XYZ/RZT) | Irregular (CAD-based) |
| **Output** | Text meshtal | XDMF/HDF5 | HDF5 or legacy EEOUT |
| **Mesh Generation** | Built-in | Built-in | External (GMSH, etc.) |
| **Geometry Matching** | No | No | Yes (conforms to geometry) |
| **Visualization** | Manual | ParaView/VisIt | ParaView (via um_post_op) |
| **Best For** | Legacy compatibility | Most work | Complex CAD geometry |

**Recommendation**: Use **FMESH** for most work. Use **UM** for complex CAD-based geometry.

## Decision Tree: Which Mesh Type?

```
START: Need spatial distribution of quantity?
│
├─→ YES: What geometry?
│   │
│   ├─→ Simple rectangular/cylindrical
│   │   │
│   │   ├─→ What quantity?
│   │   │   ├─→ Neutron/photon flux → FMESH (modern, XDMF)
│   │   │   ├─→ Source distribution → TMESH Type 2 (legacy)
│   │   │   ├─→ Energy deposition → FMESH with FM card
│   │   │   ├─→ Isotopic reactions → FMESH with FM card
│   │   │   └─→ DXTRAN contrib → TMESH Type 4 (legacy)
│   │   │
│   │   └─→ Use FMESH (XYZ or RZT)
│   │
│   ├─→ Complex CAD-based geometry
│   │   └─→ Use Unstructured Mesh (UM)
│   │       ├─→ Generate mesh in GMSH/ABAQUS
│   │       ├─→ Import with EMBED command
│   │       └─→ See unstructured_mesh_guide.md
│   │
│   └─→ Variance reduction mesh
│       └─→ MESH card (for weight windows)
│
└─→ NO: Use standard cell/surface tallies (see mcnp-tally-analyzer)
```

## FMESH Syntax (Modern Format)

### Basic Structure

```
FMESH<n>:<pl> <GEOM keyword>=<value>
              <origin/mesh keywords>
              <energy/time keywords>
              <output keywords>
```

Where:
- `<n>` = tally number (4, 14, 24, ..., 994 - must end in 4)
- `<pl>` = particle type (N, P, E, H, /, etc.)
- Keywords can span multiple lines (use continuation with +)

### Geometry Keywords

**Cartesian (XYZ)**:
```
FMESH14:N GEOM=XYZ
          ORIGIN=x0 y0 z0
          IMESH=x1 x2 ... xn  IINTS=i1 i2 ... in
          JMESH=y1 y2 ... yn  JINTS=j1 j2 ... jn
          KMESH=z1 z2 ... zn  KINTS=k1 k2 ... kn
```

**Cylindrical (RZT)**:
```
FMESH24:P GEOM=RZT
          ORIGIN=x0 y0 z0          $ Axis origin
          AXS=ux uy uz              $ Axis direction (default: 0 0 1)
          VEC=vx vy vz              $ Reference vector for theta=0 (default: 1 0 0)
          IMESH=r1 r2 ... rn  IINTS=i1 i2 ... in   $ Radial
          JMESH=z1 z2 ... zn  JINTS=j1 j2 ... jn   $ Axial
          KMESH=θ1 θ2 ... θn  KINTS=k1 k2 ... kn   $ Azimuthal (degrees)
```

**Mesh Specification Logic**:
- `IMESH/JMESH/KMESH`: Coarse mesh boundaries (absolute coordinates)
- `IINTS/JINTS/KINTS`: Fine mesh subdivisions (number of intervals in each coarse bin)
- Total bins = Σ(IINTS) × Σ(JINTS) × Σ(KINTS)

**Example**: Uniform 20×20×20 mesh from (-10,-10,-10) to (10,10,10):
```
FMESH4:N GEOM=XYZ
         ORIGIN=-10 -10 -10
         IMESH=10  IINTS=20
         JMESH=10  JINTS=20
         KMESH=10  KINTS=20
```

**Example**: Non-uniform mesh with refinement:
```
FMESH14:N GEOM=XYZ
          ORIGIN=0 0 0
          IMESH=5 10 50  IINTS=5 5 10    $ Fine near origin, coarse far
          JMESH=5 10 50  JINTS=5 5 10
          KMESH=5 10 50  KINTS=5 5 10
```

### Energy and Time Binning

**Energy bins**:
```
FMESH24:N ...
          EMESH=e1 e2 ... en   $ Energy boundaries (MeV)
          EINTS=1 1 ... 1       $ Subdivisions (usually 1 per bin)
```

**Time bins**:
```
FMESH34:N ...
          TMESH=t1 t2 ... tn   $ Time boundaries (shakes)
          TINTS=1 1 ... 1       $ Subdivisions (usually 1 per bin)
```

**Default**: If omitted, single bin covering all energies/times.

### Output Keywords

**Output format**:
```
OUT=<option>
```

Options:
- `col` = Column format (ASCII text, one line per mesh cell)
- `ij`, `ik`, `jk` = Matrix format (2D slices, one per file)
- `xdmf` = XDMF/HDF5 format for ParaView/VisIt (**RECOMMENDED**)
- `none` = Suppress output (for FM-only tallies)

**Output files** (for `OUT=xdmf`):
- `meshtal.xdmf` = XDMF metadata file (open in ParaView)
- `meshtal_<n>.h5` = HDF5 data file (binary, efficient storage)

### Tally Multipliers (FM Card)

**Isotopic reaction rates**:
```
FMESH44:N GEOM=XYZ ...
          OUT=xdmf
FM44 -1 235 -6    $ U-235 fission rate per cm³
```

Where:
- `-1` = density multiplier (use material density)
- `235` = material number containing U-235
- `-6` = reaction MT number (total fission)

**Multiple reactions**:
```
FMESH54:N ...
+FM54 (-1 235 -6) (-1 238 -6)   $ U-235 and U-238 fission rates
```

**Common reaction numbers**:
- `-2` = Absorption (MT 101)
- `-6` = Total fission (MT 18)
- `-7` = Net fission (ν × fission)
- `-8` = Fission Q-value (MeV/fission)
- `102` = (n,γ) radiative capture

## TMESH Syntax (Legacy Format)

### Basic Structure

```
TMESH
<type keyword>
CORA<n> bounds  IINTS
CORB<n> bounds  JINTS
CORC<n> bounds  KINTS
ERGSH<n> e1 e2 ... en
TMSH<n> t1 t2 ... tn
ENDMD
```

### Type Keywords

**Type 1**: Track-averaged flux
```
RMESH<n>:<pl> <quantity>
```
- Quantities: `FLUX` (default), `POPUL` (population), `PEDEP` (energy deposition), `TRKL` (track length)
- Most common: `FLUX`

**Type 2**: Source mesh
```
SMESH<n>:<pl>
```
- Tallies where particles originated (source distribution)

**Type 3**: Energy deposition
```
TMESH<n>:<pl>
```
- Energy deposited by all particles (like +F6 tally)

**Type 4**: DXTRAN mesh
```
DMESH<n>:<pl>
```
- Tallies tracks contributing to DXTRAN detectors

### Coordinate Specification

**CORA/CORB/CORC** (spatial bins):
```
CORA<n> c0 <n>i c1   $ n intervals from c0 to c1
CORA<n> c0 c1 c2 c3  $ Explicit boundaries
```

**IINTS/JINTS/KINTS** (subdivisions):
```
CORA11 0 10i 100     $ 10 intervals from 0 to 100
CORB11 -50 5i 50     $ 5 intervals from -50 to 50
CORC11 0 20i 200     $ 20 intervals from 0 to 200
```

**ERGSH** (energy bins):
```
ERGSH11 0 1e-6 1e-3 0.1 1 14   $ Thermal to 14 MeV (6 bins)
```

**TMSH** (time bins):
```
TMSH11 0 1 10 100 1000   $ Time bins (shakes)
```

### Transformation (TRANS)

Apply coordinate transformation:
```
RMESH21:N FLUX TRANS=5
```
- Applies transformation TR5 to mesh origin/orientation
- Useful for rotated or offset meshes

### Example: Complete TMESH Specification

```
TMESH
RMESH11:N FLUX
CORA11 0 10i 100
CORB11 0 10i 100
CORC11 0 10i 100
ERGSH11 0 14
ENDMD
```

## Tally Algorithms

MCNP6 supports multiple mesh tally algorithms for performance/accuracy tradeoffs:

```
FMESH<n>:N ...
          MSHMF=<algorithm>
```

**Algorithms**:
- `fast_hist` = Fast histogram (default in MCNP6.3, parallel-efficient)
- `hist` = Histogram (numerically stable, sequential)
- `batch` = Batch statistics (better uncertainty estimates)
- `rma_batch` = Distributed memory batch (for huge meshes on clusters)

**Guidance**:
- Use **fast_hist** (default) for most work
- Use **batch** if statistical quality is poor with fast_hist
- Use **rma_batch** for meshes > 10 million cells on distributed systems

## Common Use Cases

### Use Case 1: Neutron Flux Distribution in Reactor Core

**Goal**: Map neutron flux in 3D Cartesian mesh with energy binning.

```
c --- Mesh tally for flux distribution ---
FMESH104:N GEOM=XYZ
           ORIGIN=-50 -50 -100       $ Core center at origin
           IMESH=50  IINTS=25         $ 25 bins in X (4 cm each)
           JMESH=50  JINTS=25         $ 25 bins in Y
           KMESH=100 KINTS=50         $ 50 bins in Z (4 cm each)
           EMESH=1e-10 1e-6 0.1 1 20  $ Thermal, epithermal, fast, high
           OUT=xdmf                   $ ParaView visualization
```

**Result**: 25×25×50 = 31,250 mesh cells × 4 energy groups = 125,000 tally bins.

**Visualization**:
1. Open `meshtal.xdmf` in ParaView
2. Select energy group in dropdown
3. Apply "Clip" filter to view interior
4. Color by flux magnitude

### Use Case 2: Fission Rate Distribution with Isotope Separation

**Goal**: Compare U-235 vs U-238 fission rates in fuel assemblies.

```
c --- U-235 fission rate ---
FMESH14:N GEOM=XYZ
          ORIGIN=0 0 0
          IMESH=10  IINTS=20
          JMESH=10  JINTS=20
          KMESH=10  KINTS=20
          OUT=xdmf
+FM14 -1 100 -6    $ Material 100 contains U-235

c --- U-238 fission rate ---
FMESH24:N GEOM=XYZ
          ORIGIN=0 0 0
          IMESH=10  IINTS=20
          JMESH=10  JINTS=20
          KMESH=10  KINTS=20
          OUT=xdmf
+FM24 -1 200 -6    $ Material 200 contains U-238

c --- Material definitions ---
M100  92235 1.0    $ Pure U-235 (for FM tally)
M200  92238 1.0    $ Pure U-238 (for FM tally)
```

**Result**: Two mesh tallies with identical geometry, showing fission rate spatial distribution for each isotope separately.

### Use Case 3: Cylindrical Mesh for Beam Target

**Goal**: Map dose in cylindrical target struck by particle beam.

```
c --- Cylindrical mesh around beam axis ---
FMESH34:N GEOM=RZT
          ORIGIN=0 0 0               $ Beam enters at z=0
          AXS=0 0 1                  $ Beam along +Z
          VEC=1 0 0                  $ Theta=0 at +X
          IMESH=5 10 20              $ Radial: 0-5, 5-10, 10-20 cm
          IINTS=5 5 10               $ Fine near axis, coarse far
          JMESH=50                   $ Axial: 0-50 cm
          JINTS=50                   $ 1 cm per bin
          KMESH=360                  $ Full azimuth
          KINTS=36                   $ 10° per bin
          OUT=xdmf
```

**Result**: Cylindrical dose map with radial, axial, and azimuthal resolution.

### Use Case 4: Time-Dependent Flux (Pulsed Source)

**Goal**: Track neutron flux evolution over time in pulsed system.

```
c --- Time-dependent flux mesh ---
FMESH44:N GEOM=XYZ
          ORIGIN=-10 -10 -10
          IMESH=10  IINTS=20
          JMESH=10  JINTS=20
          KMESH=10  KINTS=20
          TMESH=1e-8 1e-7 1e-6 1e-5 1e-4   $ Time bins (shakes)
          OUT=xdmf
```

**Result**: 4D data (X, Y, Z, time) showing flux propagation through geometry.

**Visualization**: Use ParaView's time slider to animate flux evolution.

### Use Case 5: Activation Products with FMESH

**Goal**: Calculate Na-24 production rate in concrete shield.

```
c --- Na-24 production mesh ---
FMESH54:N GEOM=XYZ
          ORIGIN=0 0 0
          IMESH=100  IINTS=50    $ Shield dimensions
          JMESH=100  JINTS=50
          KMESH=200  KINTS=100
          OUT=xdmf
+FM54 -1 20 102    $ (n,γ) on Na-23 → Na-24

c --- Dummy material for Na-23 ---
M20  11023 1.0     $ Pure Na-23 (target isotope)
```

**Physical interpretation**:
- Tally result = (n,γ) reaction rate per cm³
- Use with actual Na density in concrete to get absolute production rate

## Mesh Tally Output Analysis

### Column Format (OUT=col)

Output file: `meshtal`

```
Mesh Tally Number   14
Particle(s): neutrons

  Tally bin: (x = 0.00 to 1.00, y = 0.00 to 1.00, z = 0.00 to 1.00)
     Energy bin: 0.00 to 14.00 MeV
        Result: 1.2345E-04
        Rel Error: 0.0521
```

### XDMF Format (OUT=xdmf)

**Files generated**:
- `meshtal.xdmf` = XML metadata (small, text-based)
- `meshtal_14.h5` = Binary HDF5 data (large, efficient)

**Opening in ParaView**:
1. File → Open → `meshtal.xdmf`
2. Click "Apply" to load data
3. Select variable from dropdown (e.g., "neutron_flux")
4. Choose representation: Surface, Volume, Slice, Clip

**Advanced visualization**:
- **Thresholding**: Display → Threshold → Set flux range
- **Contouring**: Filters → Contour → Isosurface at flux level
- **Volume rendering**: Representation → Volume → Opacity transfer function
- **Streamlines**: (Not applicable to scalar flux, but useful for vector fields)

### Statistical Quality

**Relative error check**:
```python
import h5py

# Load FMESH HDF5 output
f = h5py.File('meshtal_14.h5', 'r')
flux = f['flux'][:]
error = f['error'][:]

# Check convergence
print(f"Bins with error > 10%: {(error > 0.1).sum()}")
print(f"Bins with error > 20%: {(error > 0.2).sum()}")
print(f"Mean error: {error.mean():.3f}")
```

**Acceptance criteria** (from mcnp-statistics-checker):
- Errors < 10% for most bins
- Errors < 20% for all bins
- No zero-flux bins (indicates insufficient sampling)

## Troubleshooting

### Problem: Mesh tally has many zero-flux bins

**Cause**: Mesh extends into void regions or poorly sampled areas.

**Fix**:
1. Reduce mesh extent to match geometry
2. Use variance reduction (weight windows) to increase sampling
3. Increase NPS (more particles)

**Example**:
```
c BEFORE: Mesh covers entire problem (including voids)
FMESH14:N GEOM=XYZ
          ORIGIN=-100 -100 -100
          IMESH=100  IINTS=50
          JMESH=100  JINTS=50
          KMESH=100  KINTS=50

c AFTER: Mesh covers only geometry of interest
FMESH14:N GEOM=XYZ
          ORIGIN=-20 -20 -20
          IMESH=20  IINTS=40
          JMESH=20  JINTS=40
          KMESH=20  KINTS=40
```

### Problem: Mesh tally has large relative errors (> 20%)

**Cause**: Insufficient particle histories in mesh cells.

**Fix**:
1. Increase NPS
2. Reduce mesh resolution (larger bins)
3. Use variance reduction
4. Change algorithm to `batch` for better statistics

**Example**:
```
c Reduce mesh resolution (fewer, larger bins)
c BEFORE: 50×50×50 = 125,000 bins
FMESH24:N ...
          IINTS=50 JINTS=50 KINTS=50

c AFTER: 25×25×25 = 15,625 bins (8× fewer)
FMESH24:N ...
          IINTS=25 JINTS=25 KINTS=25
          MSHMF=batch    $ Better statistics
```

### Problem: FMESH tally shows warning "mesh cells are empty"

**Cause**: Mesh geometry doesn't intersect problem geometry.

**Fix**: Check ORIGIN coordinates and mesh boundaries.

**Debugging**:
```
c Add geometry plot to verify mesh location
c (Use MCNP plotter or mcnp-plotter skill)
```

### Problem: Cylindrical mesh (RZT) gives unexpected results

**Cause**: AXS or VEC vectors incorrectly specified.

**Fix**: Verify axis direction and reference vector.

**Example**:
```
c Beam enters from -Z, travels to +Z
FMESH34:N GEOM=RZT
          ORIGIN=0 0 -10        $ Start at z=-10
          AXS=0 0 1             $ Axis points +Z (beam direction)
          VEC=1 0 0             $ Theta=0 at +X axis
          ...
```

### Problem: Mesh tally output file is enormous (> 10 GB)

**Cause**: Too many mesh cells or energy/time bins.

**Fix**:
1. Reduce mesh resolution
2. Reduce energy/time bins
3. Use `OUT=none` if only FM tally matters
4. Use `rma_batch` algorithm for distributed storage

**Calculation**:
```
Mesh cells = IINTS × JINTS × KINTS × EMESH bins × TMESH bins
File size ≈ Mesh cells × 16 bytes (8 for value, 8 for error)

Example: 100×100×100 mesh × 10 E bins × 5 T bins
       = 1,000,000 cells × 10 × 5 = 50,000,000 bins
       = 50M × 16 bytes = 800 MB
```

## Integration with Other Skills

### With mcnp-output-parser

**Parse mesh tally output files:**

After running MCNP with FMESH:
1. Use mcnp-output-parser to read `meshtal.xdmf` or `MCTAL` files
2. Extract mesh tally data for analysis
3. See mcnp-output-parser documentation for HDF5/XDMF parsing methods

For UM output, use um_post_op utility (see `unstructured_mesh_guide.md`).

### With mcnp-tally-analyzer

**Analyze mesh tally results:**

After parsing mesh output:
- Interpret tally values (physical meaning)
- Check statistical quality (relative errors)
- Convert units (per source particle → absolute rates)
- Identify peak flux locations

See mcnp-tally-analyzer for detailed mesh data analysis workflows.

### With mcnp-plotter

**Visualize mesh geometry:**

Use mcnp-plotter to:
- Verify mesh extent covers problem geometry
- Check mesh alignment with geometry features
- Overlay mesh on geometry plots for validation

Mesh visualization workflow:
1. Plot geometry cross-section
2. Overlay mesh boundaries
3. Verify mesh positioning before running expensive simulation

### With mcnp-ww-optimizer

**Generate weight windows from mesh results:**

After initial coarse mesh run:
1. Analyze flux distribution from mesh tally
2. Use mcnp-ww-optimizer to generate weight windows from mesh
3. Re-run with fine mesh + weight windows for better statistics

See mcnp-ww-optimizer for mesh-to-weight-window workflows.

## Best Practices

1. **Use FMESH for new work** - Better visualization, simpler syntax, direct ParaView support
2. **Start coarse, refine** - Begin with low resolution to verify setup, then increase
3. **Energy binning** - Use 4-6 energy groups (thermal, epithermal, fast, high) for most reactor work
4. **Mesh extent** - Match mesh to geometry of interest; don't cover empty space
5. **XDMF output** - Always use `OUT=xdmf` for 3D visualization in ParaView
6. **FM multipliers** - Use separate materials (M100, M200, etc.) for each isotope in FM tallies
7. **Verify geometry** - Plot geometry first to ensure mesh is positioned correctly
8. **Check statistics** - Verify relative errors < 10% before trusting results
9. **Cylindrical symmetry** - Use RZT mesh for cylindrical problems (faster, fewer bins)
10. **Time-dependent** - Use TMESH bins for pulsed sources or transient analysis
11. **Programmatic Mesh Generation**:
    - Use `scripts/fmesh_generator.py` for automated FMESH card creation
    - Use `scripts/mesh_visualizer.py` to verify mesh extent and positioning
    - Use `scripts/mesh_converter.py` for UM format conversion (GMSH, ABAQUS, VTK)
12. **Unstructured Mesh**:
    - Use UM for complex CAD-based geometry (not regular grids)
    - Generate meshes in GMSH (open-source, best compatibility)
    - See `unstructured_mesh_guide.md` for complete UM workflow

## References

**Bundled Documentation:**
- `unstructured_mesh_guide.md` - Complete UM workflow (EMBED, external meshes, um_post_op)
- `mesh_file_formats.md` - GMSH, ABAQUS, VTK, CGAL format specifications
- `mesh_optimization_guide.md` - Resolution strategies, performance, statistical quality

**Bundled Scripts:**
- `scripts/fmesh_generator.py` - Programmatic FMESH card generation
- `scripts/mesh_visualizer.py` - Mesh geometry visualization
- `scripts/mesh_converter.py` - Format conversion (GMSH ↔ ABAQUS ↔ VTK)
- `scripts/README.md` - Script usage and examples

**Example Files:**
- `example_inputs/01_simple_fmesh_cartesian.i` - Basic XYZ mesh
- `example_inputs/07_unstructured_mesh_embed.i` - UM with EMBED command
- See `example_inputs/` directory for complete examples

**MCNP Manual:**
- Chapter 5.11 - Mesh Tallies (FMESH, TMESH)
- Chapter 8 - Unstructured Mesh
- Appendix A - Mesh File Formats
- Appendix D.4-D.9 - Mesh output formats
- Appendix E.11 - um_post_op utility

**Related Skills:**
- mcnp-output-parser - Parse mesh output files
- mcnp-tally-analyzer - Analyze mesh tally results
- mcnp-plotter - Visualize mesh and geometry
- mcnp-ww-optimizer - Generate weight windows from mesh
