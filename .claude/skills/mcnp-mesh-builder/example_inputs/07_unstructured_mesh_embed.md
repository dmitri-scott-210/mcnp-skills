# Example 7: Unstructured Mesh with EMBED Command

**Purpose:** Demonstrate UM (unstructured mesh) import from external GMSH file

**File:** `07_unstructured_mesh_embed.i` (requires `reactor_core.msh`)

## Description

Shows how to:
- Import external GMSH mesh using EMBED command
- Apply tallies to UM elements
- Specify element volumes

## Key Features

- **Mesh Type:** Unstructured (tetrahedral elements)
- **Source:** GMSH mesh file (`reactor_core.msh`)
- **Format:** GMSH .msh format (version 2.2)
- **Elements:** ~10,000 tetrahedra
- **Output:** HDF5 format (`input_um.h5`)

## EMBED Syntax

```
EMBED  MESHGEO=gmsh  MFILE=reactor_core.msh  MESHTALLY=102
```

- `MESHGEO=gmsh` - Mesh file format
- `MFILE=reactor_core.msh` - External mesh file path
- `MESHTALLY=102` - Tally 102 uses UM elements

## Tally Specification

```
F102:N  1 < 10000    $ All UM elements (1 through 10000)
```

- UM elements numbered 1, 2, 3, ... as in mesh file
- Use `<` operator for ranges
- Element volumes from mesh file (no SD card needed)

## Workflow

**1. Create mesh in GMSH:**
```bash
gmsh -3 reactor_geometry.geo -o reactor_core.msh
```

**2. Run MCNP with UM:**
```bash
mcnp6 i=07_unstructured_mesh_embed.i
```

**3. Post-process with um_post_op:**
```bash
# Convert to VTK for ParaView
um_post_op -op vtk_convert -input input_um.h5 -output results.vtk

# Open in ParaView
paraview results.vtk
```

## Advantages of UM

- Conforms to complex CAD geometry
- Adaptive refinement (fine near features, coarse elsewhere)
- Efficient binning (no wasted bins in voids)
- Direct CAD integration

## Mesh Generation (GMSH Example)

```gmsh
// reactor_geometry.geo
SetFactory("OpenCASCADE");

// Import STEP file
Merge "cad_model.step";

// Set mesh parameters
Mesh.CharacteristicLengthMin = 0.5;  // Fine mesh
Mesh.CharacteristicLengthMax = 5.0;  // Coarse mesh

// Define physical volumes (material regions)
Physical Volume("fuel") = {1, 2, 3};
Physical Volume("coolant") = {4, 5};

// Generate mesh
Mesh 3;
```

Generate:
```bash
gmsh reactor_geometry.geo -3 -o reactor_core.msh
```

## See Also

- `unstructured_mesh_guide.md` - Complete UM documentation
- `mesh_file_formats.md` - GMSH format specification
- `mesh_converter.py` - Format conversion utilities
