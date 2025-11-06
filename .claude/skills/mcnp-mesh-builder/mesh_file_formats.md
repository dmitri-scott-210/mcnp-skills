# Mesh File Formats for MCNP6 Unstructured Mesh

**Purpose:** Detailed specifications for external mesh file formats supported by MCNP6 EMBED command.

**Companion to:** unstructured_mesh_guide.md, SKILL.md

---

## Overview

MCNP6 supports four external mesh file formats for unstructured mesh (UM) import:

| Format | Keyword | Extension | Source Tools | Element Types | Recommendation |
|--------|---------|-----------|--------------|---------------|----------------|
| **GMSH** | `gmsh` | `.msh` | Gmsh (open-source) | Tet, Hex, Prism, Pyramid | ⭐ **Best choice** - open-source, well-documented |
| **ABAQUS** | `abaqus` | `.inp` | Abaqus/CAE | Tet, Hex | Good for CAE users |
| **VTK** | `vtk` | `.vtk` | ParaView, VTK library | Tet, Hex | Good for scripting |
| **CGAL** | `cgal` | `.mesh` | CGAL library | Tet | Specialized (surface meshing) |

**Recommendation:** Use **GMSH format** unless you have specific toolchain requirements.

---

## GMSH Format (.msh)

### Overview

**Gmsh** is an open-source 3D finite element mesh generator with built-in CAD engine and post-processor.

**Website:** https://gmsh.info/
**License:** GPL (free for all uses)
**Platforms:** Windows, Linux, macOS

### Format Specification

**GMSH .msh file format** (ASCII version 2.2):

```
$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
<number_of_nodes>
<node_number> <x> <y> <z>
...
$EndNodes
$Elements
<number_of_elements>
<element_number> <element_type> <number_of_tags> <tag_list> <node_list>
...
$EndElements
```

**Element types:**
- `4` = 4-node tetrahedron
- `5` = 8-node hexahedron
- `6` = 6-node prism (wedge)
- `7` = 5-node pyramid

### Example GMSH File

```
$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
8
1 0 0 0
2 1 0 0
3 1 1 0
4 0 1 0
5 0 0 1
6 1 0 1
7 1 1 1
8 0 1 1
$EndNodes
$Elements
6
1 4 2 1 1 1 2 3 5     $ Tet element, physical group 1
2 4 2 1 1 2 3 5 6     $ Tet element, physical group 1
3 4 2 1 1 3 5 6 7     $ Tet element, physical group 1
4 4 2 1 1 5 6 7 8     $ Tet element, physical group 1
5 4 2 1 1 1 3 4 5     $ Tet element, physical group 1
6 4 2 1 1 4 5 7 8     $ Tet element, physical group 1
$EndElements
```

**Physical groups** (tag_list):
- First tag = physical entity (material region)
- Second tag = geometrical entity
- Use physical groups to assign materials in MCNP

### Creating GMSH Mesh

**Method 1: GUI (Interactive)**

1. Open Gmsh application
2. **Geometry** → Create points, lines, surfaces, volumes
3. **Mesh** → Define element size
4. **Mesh** → 3D (generate tetrahedral mesh)
5. **File** → Export → `.msh` format

**Method 2: Script (.geo file)**

Create `example.geo`:
```gmsh
// Geometry definition
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

// Extrude to 3D
Extrude {0, 0, 10} { Surface{1}; }

// Physical groups (materials)
Physical Volume("fuel") = {1};

// Mesh size
Mesh.CharacteristicLengthMin = 0.5;
Mesh.CharacteristicLengthMax = 2.0;
```

Generate mesh:
```bash
gmsh -3 example.geo -o example.msh
```

**Method 3: From CAD (STEP file)**

```bash
gmsh -3 model.step -o model.msh
```

### GMSH → MCNP Integration

**MCNP input:**
```
EMBED  MESHGEO=gmsh  MFILE=example.msh  MESHTALLY=102

F102:N  1 < 100    $ Tally on first 100 elements
```

**Material assignment (using physical groups):**
```
c Physical group 1 = fuel (elements 1-50)
c Physical group 2 = coolant (elements 51-100)

M1  92235 0.9  92238 0.1    $ Fuel
M2  1001 2  8016 1          $ Water coolant
```

**Element numbering:** GMSH element numbers (from .msh file) are used directly in MCNP tallies.

### GMSH Best Practices for MCNP

1. **Use ASCII format 2.2** - Best MCNP compatibility (default in GMSH 4.x)
2. **Assign physical groups** - Define material regions before meshing
3. **Check mesh quality** - Tools → Statistics → Mesh Quality (aspect ratio < 10)
4. **Optimize mesh** - Mesh → Optimize 3D (improves element quality)
5. **Export in version 2.2** - File → Export → MSH2 ASCII
6. **Element count** - Aim for 10k-100k elements for MCNP (balance resolution vs. statistics)

---

## ABAQUS Format (.inp)

### Overview

**Abaqus** is a commercial finite element analysis (FEA) software suite.

**Website:** https://www.3ds.com/products-services/simulia/products/abaqus/
**License:** Commercial (expensive, industry standard)
**Use case:** If you already have Abaqus license or Abaqus mesh files

### Format Specification

**ABAQUS .inp file** (keyword format):

```
*HEADING
Mesh for MCNP
*NODE
<node_number>, <x>, <y>, <z>
...
*ELEMENT, TYPE=<element_type>
<element_number>, <node1>, <node2>, <node3>, ...
...
*ELSET, ELSET=<set_name>
<element_list>
```

**Element types:**
- `C3D4` = 4-node tetrahedron (linear)
- `C3D10` = 10-node tetrahedron (quadratic)
- `C3D8` = 8-node hexahedron (linear)
- `C3D20` = 20-node hexahedron (quadratic)

**MCNP compatibility:** Use linear elements (C3D4, C3D8) only. Quadratic elements not supported.

### Example ABAQUS File

```
*HEADING
Simple tetrahedral mesh
*NODE
1, 0.0, 0.0, 0.0
2, 1.0, 0.0, 0.0
3, 0.0, 1.0, 0.0
4, 0.0, 0.0, 1.0
*ELEMENT, TYPE=C3D4
1, 1, 2, 3, 4
*ELSET, ELSET=FUEL
1
*END
```

### Creating ABAQUS Mesh

**Method 1: Abaqus/CAE (GUI)**

1. Part → Create → Solid (3D model)
2. Mesh → Seed → Global size
3. Mesh → Element Type → C3D4 (tetrahedral)
4. Mesh → Mesh Part
5. Job → Write Input → Export `.inp` file

**Method 2: From CAD**

1. Import STEP file into Abaqus/CAE
2. Partition into material regions
3. Assign sections (material properties)
4. Mesh each partition
5. Export `.inp`

### ABAQUS → MCNP Integration

**MCNP input:**
```
EMBED  MESHGEO=abaqus  MFILE=phantom.inp  MESHTALLY=112

F112:P  1 < 500    $ Photon dose on 500 elements
```

**Material assignment:**
- Use ELSET names from .inp file to identify material regions
- Manually map element numbers to MCNP materials

### ABAQUS Best Practices for MCNP

1. **Use linear elements** - C3D4 (tet) or C3D8 (hex) only
2. **Define ELSETs** - Group elements by material for easier MCNP setup
3. **Export mesh only** - Remove material properties, loads, BCs from .inp
4. **ASCII format** - Ensure text-based .inp (not binary .sim)
5. **Check element numbering** - Must be sequential starting from 1

---

## VTK Format (.vtk)

### Overview

**VTK (Visualization Toolkit)** is an open-source software system for 3D computer graphics, image processing, and visualization.

**Website:** https://vtk.org/
**License:** BSD (free, open-source)
**Use case:** Python scripting, programmatic mesh generation, ParaView

### Format Specification

**VTK legacy ASCII format:**

```
# vtk DataFile Version 2.0
<description>
ASCII
DATASET UNSTRUCTURED_GRID
POINTS <n> float
<x1> <y1> <z1>
<x2> <y2> <z2>
...
CELLS <n_cells> <size>
<n_nodes> <node1> <node2> ... <nodeN>
...
CELL_TYPES <n_cells>
<type1>
<type2>
...
```

**Cell types:**
- `10` = Tetrahedron (4 nodes)
- `12` = Hexahedron (8 nodes)
- `13` = Wedge/Prism (6 nodes)
- `14` = Pyramid (5 nodes)

### Example VTK File

```
# vtk DataFile Version 2.0
MCNP mesh
ASCII
DATASET UNSTRUCTURED_GRID
POINTS 8 float
0.0 0.0 0.0
1.0 0.0 0.0
1.0 1.0 0.0
0.0 1.0 0.0
0.0 0.0 1.0
1.0 0.0 1.0
1.0 1.0 1.0
0.0 1.0 1.0
CELLS 1 9
8 0 1 2 3 4 5 6 7
CELL_TYPES 1
12
```

### Creating VTK Mesh with Python

**Using PyVista (modern VTK wrapper):**

```python
import pyvista as pv
import numpy as np

# Define mesh vertices
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

# Define hexahedral cell (8 nodes)
cells = np.array([[8, 0, 1, 2, 3, 4, 5, 6, 7]])

# Create unstructured grid
mesh = pv.UnstructuredGrid(cells, np.array([12]), vertices)

# Save to VTK
mesh.save('mesh.vtk')
```

**Using meshio (format converter):**

```python
import meshio

# Read GMSH file
mesh = meshio.read('input.msh')

# Write VTK file
meshio.write('output.vtk', mesh)
```

### VTK → MCNP Integration

**MCNP input:**
```
EMBED  MESHGEO=vtk  MFILE=mesh.vtk  MESHTALLY=102

F102:N  1 < 1000
```

### VTK Best Practices for MCNP

1. **Use legacy ASCII format** - Better MCNP compatibility than XML formats
2. **Unstructured grid only** - Not structured or rectilinear grids
3. **Point-based numbering** - Indices start from 0 in VTK, 1 in MCNP (MCNP handles conversion)
4. **Cell data for materials** - Use SCALARS field to define material IDs
5. **Python automation** - VTK excels at programmatic mesh generation

---

## CGAL Format (.mesh)

### Overview

**CGAL (Computational Geometry Algorithms Library)** is a C++ library for computational geometry.

**Website:** https://www.cgal.org/
**License:** GPL/LGPL (open-source)
**Use case:** Advanced surface meshing, 3D reconstruction from point clouds

### Format Specification

**CGAL .mesh format** (Medit ASCII):

```
MeshVersionFormatted 1
Dimension 3
Vertices
<number_of_vertices>
<x1> <y1> <z1> <ref1>
<x2> <y2> <z2> <ref2>
...
Tetrahedra
<number_of_tetrahedra>
<n1> <n2> <n3> <n4> <ref>
...
End
```

**Limitation:** CGAL format supports tetrahedra only (no hexahedra).

### Example CGAL File

```
MeshVersionFormatted 1
Dimension 3
Vertices
4
0.0 0.0 0.0 1
1.0 0.0 0.0 1
0.0 1.0 0.0 1
0.0 0.0 1.0 1
Tetrahedra
1
1 2 3 4 1
End
```

### Creating CGAL Mesh

**Using CGAL C++ program:**

```cpp
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Mesh_triangulation_3.h>
#include <CGAL/Mesh_complex_3_in_triangulation_3.h>
#include <CGAL/make_mesh_3.h>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
// ... (complex C++ code for mesh generation)
```

**Recommendation:** Unless you have specific CGAL requirements, use GMSH instead (easier).

### CGAL → MCNP Integration

**MCNP input:**
```
EMBED  MESHGEO=cgal  MFILE=model.mesh  MESHTALLY=102
```

**Use case:** Surface reconstruction from point cloud data (medical imaging, laser scanning).

---

## Format Comparison

### Feature Matrix

| Feature | GMSH | ABAQUS | VTK | CGAL |
|---------|------|---------|-----|------|
| **Open-source** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **CAD import** | ✅ STEP, IGES | ✅ Many | ❌ Limited | ❌ No |
| **GUI** | ✅ Yes | ✅ Yes | ✅ ParaView | ❌ No |
| **Python API** | ⚠️ Limited | ❌ No | ✅ Excellent | ⚠️ C++ |
| **Element types** | Tet, Hex, Prism, Pyramid | Tet, Hex | Tet, Hex, Wedge, Pyramid | Tet only |
| **Quality tools** | ✅ Built-in | ✅ Built-in | ⚠️ External | ⚠️ External |
| **Documentation** | ✅ Excellent | ✅ Good | ✅ Good | ⚠️ Technical |
| **Learning curve** | Easy | Medium | Medium | Hard |

### Performance Comparison

**File size** (for same mesh):
- GMSH ASCII: 100 MB
- GMSH Binary: 50 MB
- ABAQUS: 120 MB
- VTK ASCII: 110 MB
- VTK Binary: 55 MB
- CGAL: 90 MB

**MCNP read time** (1M elements):
- GMSH: ~10 seconds
- ABAQUS: ~12 seconds
- VTK: ~11 seconds
- CGAL: ~9 seconds

**Negligible difference** - Choose format based on workflow, not performance.

---

## Format Conversion

### Using meshio (Python)

**Install:**
```bash
pip install meshio
```

**Convert between formats:**
```python
import meshio

# GMSH → VTK
mesh = meshio.read('input.msh')
meshio.write('output.vtk', mesh)

# ABAQUS → GMSH
mesh = meshio.read('input.inp')
meshio.write('output.msh', mesh)

# VTK → ABAQUS
mesh = meshio.read('input.vtk')
meshio.write('output.inp', mesh)
```

**Supported conversions:** All combinations of GMSH ↔ ABAQUS ↔ VTK ↔ CGAL

### Using GMSH (built-in converter)

```bash
gmsh input.vtk -o output.msh      # VTK → GMSH
gmsh input.inp -o output.msh      # ABAQUS → GMSH
gmsh input.msh -o output.vtk      # GMSH → VTK
```

---

## Best Practices Summary

### For most users: Use GMSH

**Why:**
- Free, open-source, cross-platform
- Excellent CAD import (STEP, IGES)
- Built-in mesh quality tools
- Good documentation and community
- Easy scripting (.geo files)

### For Abaqus users: Use ABAQUS format

**Why:**
- Already have Abaqus license
- Existing mesh files from FEA work
- Material regions defined in CAE

### For Python automation: Use VTK

**Why:**
- Excellent Python bindings (PyVista)
- Programmatic mesh generation
- Integration with scientific Python stack

### For specialized needs: Use CGAL

**Why:**
- Surface reconstruction from point clouds
- Medical imaging (CT, MRI voxel data)
- Advanced computational geometry

---

## Troubleshooting Format Issues

### Problem: "Unknown mesh format"

**Cause:** MESHGEO keyword doesn't match file extension.

**Fix:**
```
EMBED  MESHGEO=gmsh  MFILE=mesh.msh    ✅ Correct
EMBED  MESHGEO=gmsh  MFILE=mesh.vtk    ❌ Wrong (VTK file with GMSH keyword)
```

### Problem: "Invalid element type"

**Cause:** Quadratic elements (10-node tet, 20-node hex) not supported by MCNP.

**Fix:** Use linear elements only:
- Tet4 (4 nodes) ✅
- Hex8 (8 nodes) ✅
- Tet10 (10 nodes) ❌
- Hex20 (20 nodes) ❌

### Problem: "Node numbers not sequential"

**Cause:** Mesh generator created gaps in node numbering.

**Fix:** Re-number nodes sequentially before export (most tools have "renumber" option).

### Problem: "Unsupported format version"

**Cause:** Using newer format version not yet supported by MCNP.

**Fix:**
- GMSH: Export as MSH2 ASCII (version 2.2), not MSH4
- VTK: Use legacy ASCII format, not XML (.vtu)

---

## References

- **MCNP Manual:** Appendix A - Mesh File Formats
- **GMSH Manual:** https://gmsh.info/doc/texinfo/gmsh.html
- **VTK File Formats:** https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf
- **ABAQUS User Manual:** Section on .inp file format
- **CGAL Documentation:** https://doc.cgal.org/latest/Mesh_3/
- **meshio Documentation:** https://github.com/nschloe/meshio

---

**END OF MESH FILE FORMATS GUIDE**
