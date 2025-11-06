# Unstructured Mesh (UM) Guide for MCNP6

**Purpose:** Comprehensive guide to using unstructured meshes in MCNP6 for tallying on complex geometries that don't align with Cartesian or cylindrical grids.

**Companion to:** SKILL.md (main mesh-builder skill)

---

## Overview

**Unstructured meshes (UM)** allow tallying on arbitrary 3D geometries using tetrahedral or hexahedral mesh elements. Unlike FMESH (structured grids), UM can:

- Conform to complex CAD geometry
- Use adaptive refinement (fine mesh near features, coarse elsewhere)
- Import meshes from external tools (GMSH, ABAQUS, CGAL, Cubit)
- Support mixed element types (tets and hexes in same mesh)

**Key difference:**
- **FMESH:** Regular grid superimposed on geometry (fast, simple, may waste bins in voids)
- **UM:** Irregular mesh conforming to geometry (efficient binning, requires mesh generation)

---

## When to Use Unstructured Mesh

### Use UM when:

1. **Complex curved geometry** - Reactor pressure vessel, tokamak, biological phantoms
2. **Adaptive resolution needed** - Fine mesh near hotspots, coarse elsewhere
3. **CAD integration** - Importing geometry from SolidWorks, CATIA, etc.
4. **Efficiency matters** - Don't want to waste bins on void regions
5. **Irregular shapes** - Geology, anthropomorphic phantoms, experimental setups

### Use FMESH when:

1. **Simple geometry** - Rectangular cores, cylindrical targets
2. **Quick setup** - No external mesh generation needed
3. **Uniform resolution** - Same binning everywhere is acceptable
4. **Visualization focus** - ParaView with regular grids is easier

---

## UM Geometry Specification: EMBED Command

### Basic Syntax

```
EMBED  <MESHGEO or BGREAD>  <MFILE or BACKGROUND>  [MESHTALLY or MGEOM]
```

**Three main approaches:**

1. **External mesh file** (most common):
   ```
   EMBED  MESHGEO=gmsh  MFILE=mesh.msh  MESHTALLY=102
   ```

2. **Background mesh** (automatic generation):
   ```
   EMBED  BGREAD  BACKGROUND  MESHTALLY=ALL
   ```

3. **Legacy MESHGEO card** (deprecated):
   ```
   EMBED  MESHGEO  MFILE=mesh.vtk  MGEOM
   ```

### MESHGEO Keyword - Mesh Format Specification

Specifies the external mesh file format:

```
MESHGEO=<format>
```

**Supported formats:**

| Format | Keyword | File Extension | Source Tool |
|--------|---------|----------------|-------------|
| ABAQUS | `abaqus` | `.inp` | Abaqus/CAE |
| CGAL | `cgal` | `.mesh` | CGAL library |
| GMSH | `gmsh` | `.msh` | Gmsh (open-source) |
| VTK | `vtk` | `.vtk` | ParaView, VTK tools |

**Example:**
```
EMBED  MESHGEO=gmsh  MFILE=reactor_core.msh  MESHTALLY=ALL
```

**Recommendation:** Use **GMSH** format - open-source, widely supported, good documentation.

### MFILE Keyword - Mesh File Path

Specifies the path to the external mesh file:

```
MFILE=<filepath>
```

**Rules:**
- Path can be absolute or relative to MCNP execution directory
- Filename must match MESHGEO format (e.g., `.msh` for gmsh)
- File must exist before MCNP run

**Examples:**
```
MFILE=mesh.msh                  $ Relative path (same directory)
MFILE=../meshes/core.msh        $ Relative path (parent directory)
MFILE=/home/user/mcnp/mesh.vtk  $ Absolute path
```

### MESHTALLY Keyword - Which Tallies Use UM

Specifies which tallies use the unstructured mesh:

```
MESHTALLY=<tally_list>
```

**Options:**
- `MESHTALLY=102` - Only tally 102 uses UM
- `MESHTALLY=102 112 122` - Tallies 102, 112, 122 use UM
- `MESHTALLY=ALL` - All tallies use UM (including FMESH if present)
- Omit MESHTALLY → No tallies use UM (geometry definition only)

**Example:**
```
c --- UM geometry ---
EMBED  MESHGEO=gmsh  MFILE=core.msh  MESHTALLY=102 112

c --- Tallies on UM ---
F102:N  1 2 3      $ Cell tallies on UM elements 1, 2, 3
F112:P  10 11 12   $ Photon tallies on UM elements 10, 11, 12
```

### MGEOM Keyword - Geometry Definition Only

Use UM to define problem geometry (not just tallies):

```
EMBED  MESHGEO=gmsh  MFILE=geometry.msh  MGEOM
```

**Purpose:**
- Replace cell cards with mesh elements
- Useful for complex CAD-based geometries
- Each mesh element becomes a "cell" with material assignment

**Material assignment:**
- Materials specified in mesh file (element attributes)
- Or use MCNP material cards with UM element numbers

**Example workflow:**
1. Create CAD model in SolidWorks
2. Export to STEP format
3. Generate mesh in GMSH with material IDs
4. Use MGEOM to import as MCNP geometry

**Limitation:** Cannot mix MGEOM with traditional cell cards in same problem.

### BACKGROUND Keyword - Automatic Mesh Generation

Generate mesh automatically from MCNP geometry:

```
EMBED  BGREAD  BACKGROUND  MESHTALLY=102
```

**Purpose:**
- No external mesh generation required
- MCNP creates mesh from existing cell geometry
- Useful for quick UM setup

**Process:**
1. MCNP reads cell cards and surfaces
2. Generates tetrahedral mesh filling geometry
3. Assigns mesh elements to cells
4. Applies tally to mesh elements

**Limitations:**
- Less control over mesh quality
- May not work for very complex geometries
- External tools (GMSH) usually give better results

**Recommendation:** Use BACKGROUND for testing, external mesh for production.

### Complete EMBED Examples

**Example 1: External GMSH mesh for flux tally**
```
c --- Import GMSH mesh for neutron flux tally ---
EMBED  MESHGEO=gmsh  MFILE=reactor_core.msh  MESHTALLY=102

c --- Neutron flux on UM elements ---
F102:N  1 2 3 4 5 6 7 8 9 10   $ First 10 mesh elements
SD102   1 1 1 1 1 1 1 1 1 1    $ Element volumes (from mesh file)
```

**Example 2: ABAQUS mesh for dose calculation**
```
c --- Import ABAQUS mesh for dose tally ---
EMBED  MESHGEO=abaqus  MFILE=phantom.inp  MESHTALLY=112

c --- Photon dose on all UM elements ---
F112:P  1 < 1000    $ All elements from 1 to 1000
FM112   (1.6022e-10)  $ Convert MeV/g to Gy
```

**Example 3: Background mesh for quick setup**
```
c --- Auto-generate mesh from geometry ---
EMBED  BGREAD  BACKGROUND  MESHTALLY=ALL

c --- Tallies automatically use UM ---
F4:N  1 2 3    $ Cell flux (UM elements)
```

**Example 4: Geometry definition with MGEOM**
```
c --- Import CAD geometry as mesh ---
EMBED  MESHGEO=gmsh  MFILE=cad_model.msh  MGEOM

c --- No cell cards needed; mesh defines geometry ---
c --- Materials assigned via mesh element attributes ---
```

---

## UM Tally Specification

### Cell Tallies on UM Elements

Once mesh is embedded with MESHTALLY, use standard cell tallies:

```
F<n>:<pl>  <element_list>
```

**Element numbering:**
- Elements numbered 1, 2, 3, ... as defined in mesh file
- Use `<` operator for ranges: `1 < 100` = elements 1 through 100
- Element volumes specified in SD card (or from mesh file)

**Example:**
```
c --- Flux in specific UM elements ---
F4:N  1 2 3 10 11 12    $ Specific elements
SD4   10.5 10.5 10.5 8.2 8.2 8.2   $ Volumes (cm³)

c --- Flux in range of elements ---
F14:N  1 < 500          $ Elements 1 through 500
c SD14 not needed if volumes in mesh file
```

### Energy and Time Binning

Use standard tally cards:

```
c --- Energy bins ---
E4  0 1e-6 0.1 1 14     $ 4 energy groups

c --- Time bins ---
T4  0 1e-8 1e-6 1e-4    $ 3 time bins
```

**Works same as cell tallies** - UM elements treated as cells.

### Tally Multipliers (FM Card)

Use FM card for reaction rates on UM:

```
c --- U-235 fission rate on UM ---
F24:N  1 < 1000
FM24   -1 10 -6    $ Material 10, total fission
```

**Interpretation:**
- Each mesh element gets isotopic reaction rate
- Multiply by element volume for total reaction rate
- Useful for activation, burnup, power distribution

---

## UM Output Formats

### HDF5 Format (Modern, Recommended)

**Output files:**
- `<inpname>_um.h5` - HDF5 file with mesh tally results
- Contains: mesh geometry, tally data, errors, metadata

**Structure:**
```
<inpname>_um.h5
├── /tally_102/
│   ├── values      (dataset: [n_elements] array of tally results)
│   ├── errors      (dataset: [n_elements] array of relative errors)
│   └── bins        (dataset: energy bins, time bins, etc.)
├── /mesh/
│   ├── vertices    (dataset: [n_vertices, 3] coordinates)
│   ├── elements    (dataset: [n_elements, 4 or 8] connectivity)
│   └── volumes     (dataset: [n_elements] element volumes)
└── /metadata/
    └── attributes
```

**Reading with Python:**
```python
import h5py

f = h5py.File('inpname_um.h5', 'r')

# Get tally 102 results
values = f['tally_102']['values'][:]
errors = f['tally_102']['errors'][:]

# Get mesh geometry
vertices = f['mesh']['vertices'][:]
elements = f['mesh']['elements'][:]

print(f"Max flux: {values.max():.3e}")
print(f"Mean error: {errors.mean():.3f}")
```

**Visualization:**
- Export to VTK format using um_post_op (see below)
- Open VTK in ParaView for 3D rendering

### EEOUT Format (Legacy ASCII)

**Output file:**
- `EEOUT` - ASCII file with element-by-element results

**Format:**
```
Tally 102
Element     Flux           Error
1           1.234e-04      0.052
2           1.567e-04      0.048
3           1.890e-04      0.051
...
```

**When to use:**
- Legacy compatibility
- Quick text inspection
- Scripting without HDF5 libraries

**Limitation:** No mesh geometry in EEOUT (need mesh file separately).

### XDMF Format (Via um_post_op)

Convert HDF5 to XDMF for direct ParaView import:

```bash
um_post_op -op vtk_convert -input inpname_um.h5 -output results.xdmf
```

**Result:**
- `results.xdmf` - XDMF metadata file
- `results.h5` - HDF5 data (same as input)
- Open `results.xdmf` in ParaView

---

## um_post_op Utility

**Purpose:** Post-process UM output files (HDF5, EEOUT) for visualization and analysis.

**Location:** Included with MCNP6 installation (usually in `bin/` directory)

### Seven Operations

#### 1. VTK Convert - Export to VTK Format

**Syntax:**
```bash
um_post_op -op vtk_convert -input <h5_file> -output <vtk_file>
```

**Purpose:** Convert HDF5 UM output to VTK legacy format for ParaView.

**Example:**
```bash
um_post_op -op vtk_convert -input reactor_um.h5 -output reactor.vtk
```

**Output:** `reactor.vtk` (can open in ParaView, VisIt, Mayavi)

#### 2. Extract - Extract Specific Tally

**Syntax:**
```bash
um_post_op -op extract -input <h5_file> -tally <n> -output <h5_file>
```

**Purpose:** Extract single tally from HDF5 file with multiple tallies.

**Example:**
```bash
um_post_op -op extract -input results_um.h5 -tally 102 -output tally102.h5
```

**Output:** `tally102.h5` (contains only tally 102)

#### 3. Combine - Merge Multiple UM Files

**Syntax:**
```bash
um_post_op -op combine -input <file1> <file2> ... -output <merged_file>
```

**Purpose:** Merge results from parallel runs or different simulations.

**Example:**
```bash
um_post_op -op combine -input run1_um.h5 run2_um.h5 run3_um.h5 -output merged.h5
```

**Requirements:** All files must use same mesh geometry.

#### 4. Average - Average Multiple Runs

**Syntax:**
```bash
um_post_op -op average -input <file1> <file2> ... -output <avg_file>
```

**Purpose:** Average tally results across multiple independent runs.

**Example:**
```bash
um_post_op -op average -input batch1.h5 batch2.h5 batch3.h5 -output average.h5
```

**Statistics:** Computes mean and standard deviation across runs.

#### 5. Scale - Scale Tally Results

**Syntax:**
```bash
um_post_op -op scale -input <h5_file> -factor <value> -output <scaled_file>
```

**Purpose:** Multiply all tally values by constant factor.

**Example:**
```bash
um_post_op -op scale -input flux_um.h5 -factor 1e6 -output flux_scaled.h5
```

**Use case:** Convert units (e.g., per source particle → per second)

#### 6. Threshold - Filter by Value

**Syntax:**
```bash
um_post_op -op threshold -input <h5_file> -min <value> -max <value> -output <filtered_file>
```

**Purpose:** Keep only elements with tally values in specified range.

**Example:**
```bash
um_post_op -op threshold -input dose_um.h5 -min 1e-6 -max 1e-2 -output hotspots.h5
```

**Use case:** Identify hotspots, exclude low-dose regions

#### 7. Info - Print File Metadata

**Syntax:**
```bash
um_post_op -op info -input <h5_file>
```

**Purpose:** Display file contents (tallies, mesh stats, dimensions).

**Example:**
```bash
um_post_op -op info -input reactor_um.h5
```

**Output:**
```
File: reactor_um.h5
Tallies: 102, 112, 122
Mesh elements: 45,231 tetrahedra
Vertices: 9,847
Energy bins: 4
Time bins: 1
```

### Workflow Example: From UM Output to ParaView

**Step 1:** Run MCNP with UM
```
mcnp6 i=input.i
```

**Step 2:** Check output with info
```bash
um_post_op -op info -input input_um.h5
```

**Step 3:** Extract specific tally
```bash
um_post_op -op extract -input input_um.h5 -tally 102 -output flux.h5
```

**Step 4:** Convert to VTK
```bash
um_post_op -op vtk_convert -input flux.h5 -output flux.vtk
```

**Step 5:** Open in ParaView
```
paraview flux.vtk
```

**Step 6:** Visualize
- Color by: "flux"
- Representation: Surface with Edges
- Apply Clip filter to see interior
- Add Colorbar

---

## External Mesh Generation Workflows

### GMSH Workflow (Recommended)

**Step 1:** Create geometry in GMSH

```gmsh
// reactor_core.geo
Point(1) = {0, 0, 0, 1.0};
Point(2) = {10, 0, 0, 1.0};
Point(3) = {10, 10, 0, 1.0};
Point(4) = {0, 10, 0, 1.0};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
Extrude {0, 0, 10} { Surface{1}; }
```

**Step 2:** Generate mesh
```bash
gmsh -3 reactor_core.geo -o reactor_core.msh
```

**Step 3:** Use in MCNP
```
EMBED  MESHGEO=gmsh  MFILE=reactor_core.msh  MESHTALLY=102
F102:N  1 < 1000
```

### ABAQUS Workflow

**Step 1:** Create mesh in Abaqus/CAE

- Use Part → Mesh → Seed/Generate
- Export as `.inp` file

**Step 2:** Use in MCNP
```
EMBED  MESHGEO=abaqus  MFILE=phantom.inp  MESHTALLY=112
```

### CAD → GMSH → MCNP Workflow

**Full workflow for complex CAD models:**

1. **Create CAD model** in SolidWorks, CATIA, etc.
2. **Export to STEP format** (.step or .stp file)
3. **Import STEP into GMSH:**
   ```bash
   gmsh cad_model.step
   ```
4. **Set mesh parameters:**
   - Mesh → Define → Size (global or local)
   - Mesh → 3D (generate tetrahedral mesh)
5. **Assign physical groups** (material regions):
   ```gmsh
   Physical Volume("fuel") = {1, 2, 3};
   Physical Volume("coolant") = {4, 5};
   ```
6. **Export mesh:**
   ```bash
   gmsh -3 cad_model.step -o cad_model.msh
   ```
7. **Use in MCNP:**
   ```
   EMBED  MESHGEO=gmsh  MFILE=cad_model.msh  MGEOM
   ```

---

## Mesh Quality Considerations

### Element Size

**Too fine:**
- ❌ Huge file sizes (> 1 GB)
- ❌ Slow tallying (more elements to track)
- ❌ Poor statistics (few histories per element)

**Too coarse:**
- ❌ Loss of spatial detail
- ❌ Can't resolve gradients

**Optimal:**
- ✅ Balance resolution vs. statistics
- ✅ Refine near features of interest
- ✅ Coarsen in uniform regions

**Rule of thumb:** Aim for ~10,000 to 100,000 elements for typical problems.

### Element Quality

**Metrics:**
- **Aspect ratio:** < 10 (ideally < 3)
- **Skewness:** < 0.8 (ideally < 0.5)
- **Jacobian:** > 0 (positive everywhere)

**Poor quality causes:**
- Inaccurate tracking (particles miss elements)
- Statistical fluctuations
- Convergence issues

**Check in GMSH:**
```
Tools → Statistics → Mesh Quality
```

### Adaptive Refinement

**Strategy:**
- Fine mesh near sources, detectors, interfaces
- Coarse mesh in bulk shielding, voids
- Use GMSH "Size Fields" for automatic refinement

**Example GMSH refinement:**
```gmsh
// Fine mesh near point (0, 0, 0)
Field[1] = Attractor;
Field[1].PointsList = {1};

Field[2] = Threshold;
Field[2].InField = 1;
Field[2].SizeMin = 0.1;    // Fine mesh size
Field[2].SizeMax = 5.0;    // Coarse mesh size
Field[2].DistMin = 1.0;    // Start refinement at 1 cm
Field[2].DistMax = 10.0;   // End refinement at 10 cm

Background Field = 2;
```

---

## Troubleshooting UM

### Problem: "Error reading mesh file"

**Cause:** File path incorrect or format mismatch.

**Fix:**
1. Check MFILE path (relative vs absolute)
2. Verify file extension matches MESHGEO (e.g., `.msh` for gmsh)
3. Confirm mesh file exists in specified location

### Problem: "UM elements have zero volume"

**Cause:** Mesh generation error (degenerate elements).

**Fix:**
1. Regenerate mesh with quality checks
2. Use GMSH optimization: `Mesh → Optimize 3D`
3. Avoid extremely small or large elements

### Problem: "Particle lost in UM"

**Cause:** Poor mesh quality or geometry gaps.

**Fix:**
1. Check mesh quality metrics (aspect ratio, skewness)
2. Verify mesh covers entire problem geometry
3. Use `Mesh → Check` in GMSH before export

### Problem: "UM tally has huge errors"

**Cause:** Insufficient sampling (too many elements, too few particles).

**Fix:**
1. Increase NPS (more particles)
2. Reduce mesh resolution (fewer, larger elements)
3. Use variance reduction (weight windows)
4. Check that mesh covers regions with particle flux

### Problem: "um_post_op command not found"

**Cause:** MCNP bin directory not in PATH.

**Fix:**
```bash
export PATH=$PATH:/path/to/mcnp6/bin
```

Or use full path:
```bash
/path/to/mcnp6/bin/um_post_op -op vtk_convert -input file.h5 -output file.vtk
```

---

## UM Best Practices

1. **Start with FMESH, move to UM if needed** - UM adds complexity; use only if FMESH insufficient
2. **Use GMSH for mesh generation** - Open-source, well-documented, good MCNP integration
3. **Check mesh quality before running** - Avoid poor-quality elements (aspect ratio, skewness)
4. **Adaptive refinement** - Fine near features, coarse elsewhere
5. **Element count** - Aim for 10k-100k elements (balance resolution vs. statistics)
6. **HDF5 output** - Use modern format for efficient storage and processing
7. **um_post_op workflows** - Convert to VTK for ParaView visualization
8. **CAD integration** - Use STEP → GMSH → MCNP workflow for complex geometry
9. **Test with BACKGROUND first** - Quick UM setup to verify tally cards before generating external mesh
10. **Material assignment** - Use GMSH Physical Groups to define material regions in mesh

---

## References

- **MCNP Manual:** Chapter 8 - Unstructured Mesh
- **Appendix A:** Mesh File Formats (ABAQUS, CGAL, GMSH, VTK)
- **Appendix D.6:** Unstructured Mesh HDF5 Output Format
- **Appendix D.7:** Unstructured Mesh Legacy Output Format
- **Appendix E.11:** um_post_op Utility Documentation
- **GMSH Manual:** https://gmsh.info/doc/texinfo/gmsh.html
- **ParaView Guide:** https://www.paraview.org/documentation/

---

**END OF UNSTRUCTURED MESH GUIDE**
