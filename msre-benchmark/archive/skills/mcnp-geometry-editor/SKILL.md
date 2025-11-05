---
category: B
name: mcnp-geometry-editor
description: Modify MCNP geometry through transformations, scaling, rotations, and geometric operations while preserving physics
activation_keywords:
  - geometry edit
  - modify geometry
  - scale geometry
  - rotate geometry
  - transform geometry
  - change dimensions
  - geometric transformation
  - cell geometry
  - surface modification
---

# MCNP Geometry Editor Skill

## Purpose

This skill guides users in modifying existing MCNP geometries through coordinate transformations, scaling operations, rotations, translations, and geometric manipulations while maintaining physical consistency and proper surface relationships. It specializes in geometry-aware editing beyond simple text modifications.

## When to Use This Skill

- Scaling entire geometries or specific regions
- Rotating geometry components or assemblies
- Translating (moving) geometric elements
- Converting between coordinate systems
- Modifying lattice structures (expanding, compacting)
- Changing surface parameters (radii, positions, orientations)
- Applying transformation matrices (TR/TRCL cards)
- Converting macrobodies to fundamental surfaces
- Adjusting universe positions within fills
- Ensuring geometric consistency after modifications
- Optimizing geometry for variance reduction

## Prerequisites

- **mcnp-geometry-builder**: Understanding geometry creation
- **mcnp-input-editor**: Basic input editing skills
- Understanding of coordinate systems and transformations
- Basic linear algebra (matrices, vectors, rotations)
- Knowledge of MCNP surface types and parameters

## Core Concepts

### Coordinate Systems

**Cartesian (Default)**:
```
x, y, z axes (right-handed)
Origin at (0, 0, 0)
```

**Transformations** change reference frames:
- **Translation**: Shift origin
- **Rotation**: Reorient axes
- **Combined**: Both translation and rotation

### Transformation Cards (TR)

**Format**:
```
*TRn  dx dy dz  a11 a12 a13  a21 a22 a23  a31 a32 a33  m
      ^translation  ^rotation matrix (3×3)       ^format flag
```

**Translation Only**:
```
*TR1  10 0 0  $ Move +10 cm in x-direction
```

**Rotation + Translation**:
```
*TR2  5 5 0  0 1 0  -1 0 0  0 0 1  1
      ^trans  ^90° rotation about z-axis  ^degrees flag
```

**Usage**:
- Surface card: `10  1  SPH  0 0 0  5`  (surface 10 uses TR1)
- Cell card: `TRCL=n` parameter

### Surface Types and Editability

| Surface Type | Parameters | Easy to Edit? | Notes |
|--------------|------------|---------------|-------|
| SO (sphere) | R | ✓ Yes | Simple radius change |
| S (sphere) | x y z R | ✓ Yes | Change center or radius |
| PX, PY, PZ | D | ✓ Yes | Change plane position |
| C/Z (cylinder) | x y R | ✓ Yes | Change axis or radius |
| RPP (box) | xmin xmax ymin ymax zmin zmax | ✓ Yes | Change box dimensions |
| RCC (cylinder) | x y z vx vy vz R | ⚠ Moderate | Axis vector + radius |
| GQ (quadric) | 10 coefficients | ✗ Difficult | Complex, use TR instead |

### Scaling Operations

**Uniform Scaling**: All dimensions × same factor
```
Original: Sphere R=10 cm
Scale 1.5×: Sphere R=15 cm
```

**Non-Uniform Scaling**: Different factors per axis
```
Original: Box 10×10×10 cm
Scale (2, 1, 1): Box 20×10×10 cm (elongated in x)
```

**Important**: Not all surfaces scale uniformly
- Planes: Constant term scales, coefficients don't
- Spheres: Radius scales
- Cylinders: Radius and axis position scale
- Macrobodies: All dimensions scale

### Rotation Operations

**Rotation Matrices** (direction cosines):
```
90° about z-axis:
[ 0  1  0 ]
[-1  0  0 ]
[ 0  0  1 ]
```

**Euler Angles**: Rotations about x, y, z axes
```
Rx(θ): Rotate θ degrees about x-axis
Ry(θ): Rotate θ degrees about y-axis
Rz(θ): Rotate θ degrees about z-axis
```

**Application**:
- Use TR card with rotation matrix
- Convert Euler angles to rotation matrix
- Apply to surfaces or cells (TRCL)

---

## Decision Tree: Geometry Modification Workflow

```
START: Need to modify geometry
  |
  +--> What type of modification?
       |
       +--[Scale]-----------------> Uniform or non-uniform?
       |                           |
       |                           +--[Uniform]-----> Scale all dimensions equally
       |                           |                  └─> Multiply surface params by factor
       |                           +--[Non-uniform]--> Scale axes differently
       |                                              └─> Use transformation matrix
       |
       +--[Rotate]----------------> About which axis?
       |                           ├─> X, Y, or Z axis: Use Euler angle
       |                           └─> Arbitrary axis: Use general rotation matrix
       |
       +--[Translate]-------------> Move entire geometry or component
       |                           └─> Add translation vector to coordinates
       |
       +--[Surface Parameter]-----> Which surface type?
       |                           ├─> Simple (SO, PX, etc.): Direct edit
       |                           └─> Complex (GQ, etc.): Use TR instead
       |
       +--[Lattice]---------------> Expand or compact lattice
       |                           └─> Modify LAT/FILL parameters
       |
       +--[Macrobody]-------------> Convert to surfaces or edit params
                                   ├─> Edit: Change RPP/RCC/etc. parameters
                                   └─> Convert: Expand to fundamental surfaces
  |
  +--> After modification:
       ├─> Verify geometry (MCNP plot)
       ├─> Check for lost particles
       ├─> Validate cell/surface consistency
       └─> Test run
```

---

## Use Case 1: Scale Entire Geometry Uniformly

**Scenario**: Scale entire model by factor of 1.2 (20% larger)

**Original Geometry**:
```
c Cell Cards
1    1  -1.0  -1       IMP:N=1  $ Inner sphere
2    2  -2.3  1  -2    IMP:N=1  $ Shell
3    0        2        IMP:N=0  $ Graveyard

c Surface Cards
1    SO  10.0          $ R=10 cm
2    SO  20.0          $ R=20 cm
```

**Editing Steps**:

1. **Identify all dimension parameters**:
```
Surface 1: R = 10.0
Surface 2: R = 20.0
```

2. **Apply scale factor (1.2×)**:
```
Surface 1: R = 10.0 × 1.2 = 12.0
Surface 2: R = 20.0 × 1.2 = 24.0
```

3. **Update surface cards**:
```
c Surface Cards
1    SO  12.0          $ R=12 cm (scaled from 10)
2    SO  24.0          $ R=24 cm (scaled from 20)
```

4. **Update densities** (if needed):
```
Note: Densities typically don't change with scaling
Exception: If using number densities (negative), may need adjustment
```

5. **Document change**:
```
c GEOMETRY SCALED 1.2× on 2025-10-31
c Original: R1=10 cm, R2=20 cm
c Scaled:   R1=12 cm, R2=24 cm
```

**Key Points**:
- All dimensions scale by same factor
- Densities usually unchanged (unless modeling requires it)
- Volume scales by factor³ (1.2³ = 1.728 in this case)
- Update VOL parameters if present: VOL × factor³

---

## Use Case 2: Rotate Geometry Component

**Scenario**: Rotate a cylinder 45° about z-axis

**Original Geometry**:
```
c Cylinder along x-axis
10  0  -10  FILL=1  IMP:N=1  $ Cell filled with universe 1

c Surface
10  RCC  0 0 0  10 0 0  2.0  $ Cylinder: base (0,0,0), axis (10,0,0), R=2
```

**Method 1: Using TR Card**

1. **Create transformation** (45° about z):
```
*TR1  0 0 0  0.707 0.707 0  -0.707 0.707 0  0 0 1  1
      ^no translation
              ^cos(45°) ^sin(45°)    (rotation matrix)
                        ^degrees flag (1=interpret as degrees)
```

2. **Apply to surface**:
```
10  1  RCC  0 0 0  10 0 0  2.0  $ Uses TR1
    ^TR number
```

3. **Verify** orientation:
```
Original axis: (10, 0, 0) = along +x
Rotated axis:  (7.07, 7.07, 0) = 45° from +x toward +y ✓
```

**Method 2: Direct Calculation**

1. **Calculate new axis vector**:
```
Original: (10, 0, 0)
Rotation matrix (45° about z):
[cos(45°)  -sin(45°)  0] [10]   [7.07]
[sin(45°)   cos(45°)  0] [0 ] = [7.07]
[0          0         1] [0 ]   [0   ]
```

2. **Update surface directly**:
```
10  RCC  0 0 0  7.07 7.07 0  2.0  $ Rotated cylinder
```

**Key Points**:
- TR method: Non-destructive, can be reversed
- Direct calculation: Permanent change to surface
- Verify rotation direction (right-hand rule)
- Check geometry plot after rotation

---

## Use Case 3: Translate (Move) Geometry Component

**Scenario**: Move a sphere from origin to (50, 0, 0)

**Original Geometry**:
```
c Sphere at origin
1    1  -1.0  -1  IMP:N=1

c Surface
1    SO  10.0  $ Sphere R=10 at origin (0,0,0)
```

**Method 1: Change Surface Definition**

```
c Original
1    SO  10.0  $ Sphere at (0,0,0), R=10

c Modified
1    S  50 0 0  10.0  $ Sphere at (50,0,0), R=10
     ^General sphere (not SO = sphere at origin)
```

**Method 2: Using TR Card**

```
c Surface (unchanged)
1    SO  10.0

c Transformation
*TR1  50 0 0  $ Translation only

c Surface references TR
1    1  SO  10.0  $ Uses TR1
```

**Method 3: Modify Cell with TRCL**

```
c Cell card
1    1  -1.0  -1  TRCL=1  IMP:N=1
                  ^cell transformation

c Transformation
*TR1  50 0 0
```

**Key Points**:
- Method 1: Direct, clear, recommended for simple cases
- Method 2: Good when multiple surfaces move together
- Method 3: Moves entire cell (all surfaces in that cell)
- Update any dependent geometries (neighboring cells)

---

## Use Case 4: Non-Uniform Scaling (Aspect Ratio Change)

**Scenario**: Stretch box in z-direction by 2×, keep x and y unchanged

**Original Geometry**:
```
c Box 10×10×10 cm
1    1  -1.0  -1  IMP:N=1

c Surface
1    RPP  -5 5  -5 5  -5 5  $ 10×10×10 cm box
```

**Method 1: Direct Edit** (simple shapes):

```
c Modified box: 10×10×20 cm
1    RPP  -5 5  -5 5  -10 10  $ Stretched in z
           ^unchanged  ^doubled
```

**Method 2: Transformation Matrix** (complex shapes):

```
*TR1  0 0 0  1 0 0  0 1 0  0 0 2
      ^no translation
              ^x unchanged
                      ^y unchanged
                             ^z doubled

c Apply to surface
1    1  RPP  -5 5  -5 5  -5 5  $ Original dims, TR1 stretches
```

**Volume Correction**:
```
Original volume: 10×10×10 = 1000 cm³
New volume: 10×10×20 = 2000 cm³

If VOL parameter present:
VOL  1000  → VOL  2000  (update accordingly)
```

**Key Points**:
- Non-uniform scaling changes aspect ratio
- Volume scales by product of factors (1×1×2 = 2× in this case)
- Check physical reasonableness (e.g., thin vs thick)
- May affect physics (streaming, leakage)

---

## Use Case 5: Modify Lattice Structure

**Scenario**: Expand 3×3 lattice to 5×5

**Original Geometry**:
```
c Lattice cell
100  0  -10  LAT=1  FILL=-1:1  -1:1  0:0  &
                                1 1 1  &
                                1 2 1  &
                                1 1 1  IMP:N=1
c 3×3 lattice (indices -1:1, -1:1)
```

**Editing Steps**:

1. **Determine new lattice bounds**:
```
Original: -1:1, -1:1 (3×3)
New: -2:2, -2:2 (5×5)
```

2. **Expand FILL array**:
```
c 5×5 lattice
100  0  -10  LAT=1  FILL=-2:2  -2:2  0:0  &
     1 1 1 1 1  &
     1 1 1 1 1  &
     1 1 2 1 1  &
     1 1 1 1 1  &
     1 1 1 1 1  IMP:N=1
c Center cell (0,0) is universe 2, rest are universe 1
```

3. **Update bounding surface** (if needed):
```
Original: Box size for 3×3 with pitch p
New: Box size for 5×5 with pitch p

If pitch=1.26 cm:
Original box: 3×1.26 = 3.78 cm per side
New box: 5×1.26 = 6.30 cm per side

10  RPP  -1.89 1.89  -1.89 1.89  -10 10  $ Old
10  RPP  -3.15 3.15  -3.15 3.15  -10 10  $ New
```

**Key Points**:
- FILL array size = (imax-imin+1) × (jmax-jmin+1) × (kmax-kmin+1)
- Index carefully (MCNP uses column-major ordering)
- Update bounding surface to enclose expanded lattice
- Verify no gaps or overlaps with MCNP plot

---

## Use Case 6: Convert Macrobody to Fundamental Surfaces

**Scenario**: Convert RPP (rectangular parallelepiped) to 6 plane surfaces

**Original Geometry**:
```
c Cell
1    1  -1.0  -10  IMP:N=1

c Macrobody surface
10  RPP  -5 5  -5 5  -5 5  $ Box
```

**Conversion**:

1. **Identify macrobody parameters**:
```
RPP  xmin xmax  ymin ymax  zmin zmax
     -5   5     -5   5     -5   5
```

2. **Create equivalent planes**:
```
c Planes replacing RPP
11  PX  -5  $ xmin plane
12  PX   5  $ xmax plane
13  PY  -5  $ ymin plane
14  PY   5  $ ymax plane
15  PZ  -5  $ zmin plane
16  PZ   5  $ zmax plane
```

3. **Update cell geometry**:
```
c Original
1    1  -1.0  -10  IMP:N=1

c Converted (intersection of 6 half-spaces)
1    1  -1.0  -11  -12  -13  -14  -15  -16  IMP:N=1
c            inside all 6 planes
```

4. **Simplify using sense**:
```
c Equivalent (positive sense = outside, negative = inside)
1    1  -1.0  11 -12  13 -14  15 -16  IMP:N=1
c            xmin<x<xmax, ymin<y<ymax, zmin<z<zmax
```

**Why Convert?**:
- Individual face control (different surfaces for different faces)
- Apply reflective/white boundaries to specific faces
- Easier to extend geometry (add adjacent cells)
- More flexible for complex Boolean operations

**Key Points**:
- RPP → 6 PX/PY/PZ planes
- RCC → cylinder surface + 2 plane surfaces (top/bottom)
- SPH → single SO or S surface
- Verify geometry with plot after conversion

---

## Use Case 7: Apply Combined Transformation (Rotate + Translate)

**Scenario**: Rotate component 30° about y-axis, then move to (10, 0, 0)

**Original Geometry**:
```
c Component at origin, aligned with axes
10  0  -100  FILL=1  IMP:N=1
100  RCC  0 0 0  10 0 0  2.0  $ Cylinder along +x
```

**Transformation**:

1. **Define combined transformation**:
```
*TR1  10 0 0  0.866 0 0.5  0 1 0  -0.5 0 0.866  1
      ^translate to (10,0,0)
               ^rotation matrix (30° about y)
                                              ^degrees flag
```

**Explanation**:
- Translation: (10, 0, 0)
- Rotation matrix (30° about y-axis):
```
[cos(30°)   0   sin(30°) ]   [0.866  0    0.5  ]
[0          1   0        ] = [0      1    0    ]
[-sin(30°)  0   cos(30°) ]   [-0.5   0    0.866]
```

2. **Apply to cell or surface**:
```
Method 1 (cell):
10  0  -100  FILL=1  TRCL=1  IMP:N=1

Method 2 (surface):
100  1  RCC  0 0 0  10 0 0  2.0  $ Uses TR1
```

3. **Verify result**:
```
Original axis: (10, 0, 0)
After rotation: (8.66, 0, 5.0)  $ 30° tilt toward +z
After translation: Center at (10, 0, 0)
```

**Key Points**:
- Order matters: MCNP applies rotation THEN translation
- Verify transformation direction (coordinate system vs object)
- Use MCNP plot to visualize result
- Test with lost particle check

---

## Use Case 8: Mirror Geometry Across Plane

**Scenario**: Create mirror image of component across x=0 plane

**Original Geometry**:
```
c Component on +x side
1    1  -1.0  -10  IMP:N=1

c Surface (sphere at x=5)
10  S  5 0 0  3.0  $ Sphere center (5,0,0), R=3
```

**Method 1: Reflective Surface** (if appropriate):

```
c Add reflecting surface at x=0
1    *PX  0.0  $ Reflective plane (* prefix)
```

**Method 2: Create Mirrored Component**:

1. **Calculate mirror position**:
```
Original center: (5, 0, 0)
Mirror across x=0: (-5, 0, 0)
```

2. **Create new surface**:
```
20  S  -5 0 0  3.0  $ Mirrored sphere
```

3. **Create new cell**:
```
2    1  -1.0  -20  IMP:N=1  $ Mirrored cell
```

**Method 3: Using Transformation**:

```
*TR2  0 0 0  -1 0 0  0 1 0  0 0 1
      ^no translation
              ^x reflected (negative)
                      ^y unchanged
                             ^z unchanged

20  2  S  5 0 0  3.0  $ Surface uses TR2 (reflects to x=-5)
```

**Key Points**:
- Reflective surface: Physics automatically handles mirror
- Explicit copy: Full control, but more surfaces/cells
- Transformation: Clean, but requires TR card
- Check sense conventions after mirroring

---

## Common Errors and Troubleshooting

### Error 1: "Lost particles after scaling"

**Symptom**: Geometry has gaps after scaling

**Cause**: Scaling created space between surfaces that were previously touching

**Example**:
```
Original:
1  SO  10.0  $ Inner sphere
2  SO  10.0  $ Outer sphere (same radius, touching)

After 1.5× scale:
1  SO  15.0  $ Inner
2  SO  15.0  $ Outer (still same, but now overlapping!)
```

**Fix**:
```
Ensure surfaces maintain proper relationships:
1  SO  15.0  $ Inner (scaled)
2  SO  22.5  $ Outer (scaled: 15×1.5=22.5, maintains gap)
```

**Prevention**: Scale all related dimensions consistently

---

### Error 2: "Rotation matrix not orthonormal"

**Symptom**: MCNP error about invalid transformation matrix

**Cause**: Rotation matrix rows/columns not perpendicular or unit length

**Check**:
```
For rotation matrix:
[a11  a12  a13]
[a21  a22  a23]
[a31  a32  a33]

Rows must be perpendicular:
Row1 · Row2 = 0
Row1 · Row3 = 0
Row2 · Row3 = 0

Rows must be unit length:
|Row1| = 1
|Row2| = 1
|Row3| = 1
```

**Fix**: Use MCNP degrees mode (m=1) to avoid manual matrix calculation:
```
*TR1  0 0 0  30 0 0  1  $ 30° about x-axis, degrees mode
```

**Prevention**: Use validated rotation matrices or degrees mode

---

### Error 3: "Cell volume changed unexpectedly"

**Symptom**: Tally results change after geometric edit

**Cause**: VOL parameter not updated after scaling

**Example**:
```
Original:
1  1  -1.0  -1  VOL=4188.79  IMP:N=1  $ Sphere R=10, V=4/3πr³

After 1.2× scale:
Surface 1: R=12 cm (scaled)
Cell 1: VOL=4188.79  ← WRONG! Should be VOL=7238.23

Correct volume: V = 4/3 × π × 12³ = 7238.23 cm³
```

**Fix**:
```
Update VOL parameter:
1  1  -1.0  -1  VOL=7238.23  IMP:N=1  $ Updated volume
```

**Prevention**:
- Recalculate volumes after scaling (V scales by factor³)
- Or omit VOL and let MCNP calculate (slower but always correct)

---

### Error 4: "Lattice indices out of bounds"

**Symptom**: MCNP error about lattice fill indices

**Cause**: FILL array doesn't match lattice dimensions

**Example**:
```
LAT=1  FILL=-1:1  -1:1  0:0  ...
       ^3×3×1 = 9 entries needed

FILL array: 1 1 1  1 2 1  $ Only 6 entries! ✗
```

**Fix**:
```
LAT=1  FILL=-1:1  -1:1  0:0  &
       1 1 1  &
       1 2 1  &
       1 1 1     $ 9 entries ✓
```

**Prevention**: Count entries carefully
- (imax-imin+1) × (jmax-jmin+1) × (kmax-kmin+1) = total entries

---

### Error 5: "Geometry overlaps after transformation"

**Symptom**: Multiple cells occupy same space after TR applied

**Cause**: Transformation moved cell into occupied space

**Check**:
```
Use MCNP plot with color-by-cell to visualize overlaps
Use random point sampling to detect overlaps programmatically
```

**Fix**:
```
Option 1: Adjust transformation to avoid overlap
Option 2: Modify neighboring cells to accommodate
Option 3: Use # (complement) operator to exclude overlapping region
```

**Prevention**:
- Visualize with plot before running
- Check bounding boxes of transformed components
- Test with very short run (NPS 100) to catch lost particles early

---

### Error 6: "Surface sense reversed after transformation"

**Symptom**: Cell geometry becomes inverted (inside becomes outside)

**Cause**: Some transformations (reflections) reverse surface sense

**Example**:
```
Original: -1  $ Inside surface 1
After reflection: Still -1, but now outside! ✗
```

**Fix**:
```
Check transformation determinant:
det(R) = +1: Right-handed, sense preserved ✓
det(R) = -1: Left-handed, sense reversed ✗

If determinant negative, flip surface sense:
-1  →  1  (or vice versa)
```

**Prevention**: Avoid reflection transformations (det=-1), use explicit mirroring instead

---

## Integration with Other Skills

### 1. **mcnp-geometry-builder**
How it integrates: Builder creates, Editor modifies

**Workflow**:
```
1. mcnp-geometry-builder → Create initial geometry
2. Run simulation
3. Analyze results (e.g., flux distribution)
4. THIS SKILL → Adjust geometry (scale, rotate, optimize)
5. Repeat until satisfactory
```

---

### 2. **mcnp-input-editor**
How it integrates: General editing vs geometry-specific

**Workflow**:
```
mcnp-input-editor: Text-based edits (search/replace, batch)
THIS SKILL: Geometry-aware edits (transformations, scaling)

Use input-editor for: Simple parameter changes
Use THIS SKILL for: Geometric transformations
```

---

### 3. **mcnp-transform-editor**
How it integrates: Specialized TR card editing

**Workflow**:
```
THIS SKILL: High-level geometry operations (scale, rotate)
mcnp-transform-editor: Low-level TR card manipulation

THIS SKILL generates transformation requirements →
mcnp-transform-editor implements TR cards
```

---

### 4. **mcnp-input-validator**
How it integrates: Validates geometry after edits

**Workflow**:
```
1. THIS SKILL → Make geometric modifications
2. mcnp-input-validator → Check for geometry errors
3. If errors: THIS SKILL → Fix issues
4. Repeat until validated ✓
```

---

### 5. **mcnp-variance-reducer**
How it integrates: Geometry affects variance reduction

**Workflow**:
```
1. Initial geometry
2. Run simulation
3. mcnp-variance-reducer → Identify regions needing splitting
4. THIS SKILL → Subdivide geometry into smaller cells
5. Apply importance sampling
6. Re-run, evaluate FOM improvement
```

---

### Typical Workflow: Iterative Geometry Optimization

```
1. mcnp-geometry-builder   → Create initial geometry
2. [Run MCNP]
3. [Analyze results]
4. Identify geometric issues:
   - Too much leakage? → Increase shield thickness (THIS SKILL)
   - Poor tally statistics? → Subdivide regions (THIS SKILL)
   - Want parameter study? → Scale systematically (THIS SKILL)
5. THIS SKILL              → Apply geometric modifications
6. mcnp-input-validator    → Validate changes
7. [Run MCNP again]
8. Compare results
9. Repeat steps 4-8 until optimized
10. DONE ✓
```

---

## Validation Checklist

After geometric edits:

### Geometric Integrity
- [ ] All surfaces still valid (no negative radii, etc.)
- [ ] No gaps between adjacent cells
- [ ] No overlapping cells (unless intentional)
- [ ] Bounding surfaces enclose all non-graveyard cells
- [ ] Lattice dimensions consistent with FILL array

### Transformation Correctness
- [ ] TR matrices are orthonormal (if manual)
- [ ] Determinant = +1 (no reflections unless intended)
- [ ] Translation vectors reasonable (not off by orders of magnitude)
- [ ] Applied to correct surfaces/cells

### Physics Consistency
- [ ] Volumes updated if scaled (VOL parameters)
- [ ] Densities still reasonable
- [ ] Material assignments unchanged (unless intended)
- [ ] Importances still appropriate for new geometry

### Verification
- [ ] MCNP plot shows correct geometry
- [ ] No lost particles in test run (NPS 1000)
- [ ] Tallies in expected locations
- [ ] Results physically reasonable

---

## Advanced Topics

### 1. Programmatic Geometry Generation

**Python Script for Scaling**:
```python
import re

def scale_geometry(input_file, factor):
    """Scale all surface dimensions by factor"""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # Detect surface cards (e.g., "1 SO 10.0")
        if re.match(r'^\s*\d+\s+(SO|S|PX|PY|PZ|CZ)\s+', line):
            parts = line.split()
            surf_num = parts[0]
            surf_type = parts[1]
            # Scale numeric parameters
            params = [float(p) * factor if p.replace('.','').replace('-','').isdigit()
                     else p for p in parts[2:]]
            lines[i] = f"{surf_num}  {surf_type}  " + "  ".join(map(str, params)) + "\n"

    with open(input_file, 'w') as f:
        f.writelines(lines)

# Usage
scale_geometry('input.i', 1.5)  # Scale 1.5×
```

---

### 2. Rotation Matrix Calculation

**Euler Angle to Matrix**:
```python
import numpy as np

def euler_to_matrix(roll, pitch, yaw, degrees=True):
    """Convert Euler angles to rotation matrix"""
    if degrees:
        roll, pitch, yaw = np.radians([roll, pitch, yaw])

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])

    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])

    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])

    return Rz @ Ry @ Rx  # Combined rotation

# Usage
R = euler_to_matrix(0, 30, 0)  # 30° pitch
print(f"*TR1  0 0 0  {R[0,0]:.3f} {R[0,1]:.3f} {R[0,2]:.3f} ...")
```

---

### 3. Parametric Geometry Studies

**Automated Dimension Sweep**:
```python
def create_parametric_inputs(base_input, param_name, values):
    """Create multiple inputs with varying parameter"""
    for i, val in enumerate(values):
        with open(base_input, 'r') as f:
            content = f.read()

        # Replace parameter (e.g., sphere radius)
        modified = content.replace(f"{param_name}=X", f"{param_name}={val}")

        with open(f"input_{param_name}_{val}.i", 'w') as f:
            f.write(modified)

# Usage: Study radius from 5 to 15 cm
create_parametric_inputs('template.i', 'radius', range(5, 16))
```

---

## Best Practices

### 1. **Always Visualize After Geometric Edit**
```
mcnp6 inp=input.i ip
PLOT
  (check all views: xy, xz, yz)
  (color by cell to see overlaps)
  (color by material to verify assignments)
```

### 2. **Scale Systematically**
```
Good:
- Scale all related dimensions by same factor
- Update dependent parameters (volumes, etc.)
- Document scale factor

Bad:
- Scale some dimensions but not others
- Forget to update cell volumes
- No documentation of changes
```

### 3. **Use TR Cards for Reversibility**
```
Prefer:
*TR1  10 0 0  (transformation card)
10  1  SO  5.0

Over:
10  S  10 0 0  5.0  (modified surface)

Reason: TR can be easily changed/removed
```

### 4. **Test Incrementally**
```
1. Make small geometric change
2. Validate (plot + short run)
3. If OK, continue; if not, revert
4. Don't make 10 changes before testing
```

### 5. **Document Geometric Changes**
```
c GEOMETRY MODIFICATIONS LOG:
c 2025-10-31 10:00: Scaled entire geometry 1.2×
c 2025-10-31 10:30: Rotated component A 30° about y-axis
c 2025-10-31 11:00: Expanded lattice from 3×3 to 5×5
```

### 6. **Preserve Geometric Hierarchy**
```
When editing:
- Maintain universe structure (U, FILL)
- Preserve lattice relationships
- Keep transformation hierarchy consistent
- Don't break cell complement (#) operators
```

### 7. **Check Physical Plausibility**
```
After editing, ask:
- Are dimensions reasonable? (not nanometers or kilometers)
- Are densities still correct? (no negative mass densities)
- Does geometry make physical sense?
- Are tallies still in correct locations?
```

### 8. **Programmatic Geometry Editing**

For automated geometry modifications and parametric variations, see: `mcnp_geometry_editor.py`

This tool is useful for:
- Batch geometry transformations
- Parametric geometry optimization
- Automated cell/surface modifications

---

## References

**Documentation Summary**:
- **Section 3-5**: Geometry specification (cells, surfaces, CSG)
- **Section 6**: Transformation cards (TR, TRCL)
- **Section 13**: Geometry examples
- **Section 18**: Variance reduction (geometry optimization)

**Related Skills**:
- **mcnp-geometry-builder**: Creating geometry from scratch
- **mcnp-input-editor**: General text-based editing
- **mcnp-transform-editor**: Specialized TR card editing
- **mcnp-input-validator**: Validating geometry after edits
- **mcnp-lattice-builder**: Creating/modifying lattice structures

**User Manual References**:
- Chapter 5.1: Geometry Specification
- Chapter 5.2: Cell Cards
- Chapter 5.3: Surface Cards
- Chapter 5.5: Geometry Data Cards (TR, LAT, FILL)

**Slash Command**:
- `.claude/commands/mcnp-geometry-editor.md`: Quick reference for geometry editing

---

**End of MCNP Geometry Editor Skill**
