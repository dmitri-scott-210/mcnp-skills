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

## Use Case 9: Modify Lattice Fill Transformation

**Scenario**: Reposition compact lattice to new location in capsule

**Original Geometry**:
```mcnp
c Compact lattice at original position
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
                                          ↑ Stack 1 position
```

**Editing Task**: Move to Stack 2 position at (24.553123, -25.547039, same Z)

**Method 1: Direct Edit of Translation Vector**

1. **Identify current transformation**:
```
Original: (25.547039, -24.553123, 19.108100)
New:      (24.553123, -25.547039, 19.108100)  ← Stack 2 position
```

2. **Update fill card**:
```mcnp
c Modified compact lattice
91111 0  -97011  98005 -98051 fill=1110  (24.553123 -25.547039 19.108100)
```

3. **Update bounding surface** (if off-axis cylinder):
```mcnp
c Original
97011 c/z   25.547039 -24.553123   0.63500  $ Stack 1 center

c Modified
97011 c/z   24.553123 -25.547039   0.63500  $ Stack 2 center
```

**Method 2: Using TR Card with TRCL**

```mcnp
c Define transformation
*TR91  24.553123 -25.547039 19.108100  $ Stack 2 position

c Apply to cell
91111 0  -97011  98005 -98051 fill=1110  trcl=91
```

**Validation Steps**:
- [ ] Check that new position doesn't overlap other components
- [ ] Verify bounding surface (97011) matches new center
- [ ] Confirm Z-planes (98005, 98051) still apply
- [ ] Plot geometry to visualize new position
- [ ] Test with short run (NPS 1000) to check for lost particles

**Key Points**:
- Fill transformations position entire universe at translated location
- Update off-axis surfaces (c/z) to match new position
- Hexagonal or triangular patterns: verify angular spacing (120°, 60°, etc.)
- Lattice orientation NOT affected by translation (only position changes)

---

## Use Case 10: Scale Multi-Level Lattice Hierarchy

**Scenario**: Scale AGR-1 TRISO particle compact by 1.2× (all levels)

**Original Hierarchy**:
```
Level 1: TRISO particle (u=1114)
  - Kernel: R = 0.017485 cm
  - Buffer: R = 0.027905 cm
  - IPyC:   R = 0.031785 cm
  - SiC:    R = 0.035375 cm
  - OPyC:   R = 0.039305 cm

Level 3: Particle lattice (u=1116)
  - Bounding RPP: ±0.043715 cm (X,Y), ±0.05 cm (Z)
  - 15×15×1 array

Level 5: Compact lattice (u=1110)
  - Bounding RPP: ±0.65 cm (X,Y), ±0.043715 cm (Z)
  - 1×1×31 vertical stack

Global: Compact placement
  - Cylinder 97011: c/z 25.547 -24.553  0.63500
  - Z-planes: 98005 (17.818), 98051 (20.358)
```

**Scaling Procedure (Bottom-Up)**:

**Step 1: Scale Level 1 (TRISO Particle)**
```mcnp
c Original surfaces
91111 so   0.017485  $ Kernel
91112 so   0.027905  $ Buffer
91113 so   0.031785  $ IPyC
91114 so   0.035375  $ SiC
91115 so   0.039305  $ OPyC

c Scaled surfaces (×1.2)
91111 so   0.020982  $ Kernel (0.017485 × 1.2)
91112 so   0.033486  $ Buffer (0.027905 × 1.2)
91113 so   0.038142  $ IPyC
91114 so   0.042450  $ SiC
91115 so   0.047166  $ OPyC
```

**Step 2: Scale Level 3 (Particle Lattice Bounding Surface)**
```mcnp
c Original
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000

c Scaled (×1.2)
91117 rpp -0.052458 0.052458 -0.052458 0.052458 -0.060000 0.060000
          ↑ 0.043715 × 1.2          ↑ 0.043715 × 1.2  ↑ 0.05 × 1.2
```

**Step 3: Scale Level 5 (Compact Lattice Bounding Surface)**
```mcnp
c Original
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715

c Scaled (×1.2)
91118 rpp -0.780000 0.780000 -0.780000 0.780000 -0.052458 0.052458
```

**Step 4: Scale Global Placement**
```mcnp
c Original cylinder
97011 c/z   25.547039 -24.553123   0.63500

c Scaled cylinder (radius only, center position depends on context)
97011 c/z   25.547039 -24.553123   0.76200  $ 0.635 × 1.2

c Original z-planes
98005 pz   17.81810
98051 pz   20.35810

c Scaled z-planes (if entire assembly scaled)
98005 pz   21.38172  $ 17.81810 × 1.2
98051 pz   24.42972  $ 20.35810 × 1.2

c Compact height increased from 2.54 cm to 3.048 cm
```

**Step 5: Update Cell Volumes**
```mcnp
c Original kernel volume
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel

c Scaled kernel volume (V_new = V_old × scale³)
c 0.092522 × 1.2³ = 0.092522 × 1.728 = 0.159878
91101 9111 -10.924 -91111  u=1114 vol=0.159878  $ Scaled kernel
```

**Validation Checklist**:
- [ ] All spherical surfaces scaled by same factor
- [ ] RPP surfaces scaled in all 3 dimensions
- [ ] Cylinder radii scaled
- [ ] Z-plane positions scaled (if applicable)
- [ ] Fill transformation updated (if global scaling)
- [ ] Cell volumes updated: V_new = V_old × factor³
- [ ] Lattice pitch consistency: surface extent = N × pitch
- [ ] Plot all 3 views (XY, XZ, YZ) to verify
- [ ] No lost particles in test run

**Key Points**:
- Scale **bottom-up** (innermost universe first)
- **All related dimensions** must scale together
- Volumes scale by **factor³** (1.2³ = 1.728)
- Lattice bounding surfaces must scale to contain scaled elements
- Fill transformations may need adjustment depending on context
- Document scale factor prominently in comments

---

## Use Case 11: Rotate Hexagonal Assembly

**Scenario**: Rotate hexagonal fuel assembly 60° about vertical axis

**Original Geometry**:
```mcnp
c Hexagonal assembly (u=400, LAT=2)
400 0  -400  u=400 lat=2  fill=-6:6 -6:6 0:0
    [... hexagonal fill pattern ...]

c RHP bounding surface
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
400 rhp  0 0 0  0 0 68  0 1.6 0  $ Height along +Z, R along +Y
```

**Method 1: Rotation via TR Card**

1. **Create 60° rotation about Z**:
```mcnp
c 60° rotation about Z-axis
*TR400  0 0 0  0.5 0.866 0  -0.866 0.5 0  0 0 1  1
        ↑ No translation
                ↑ cos(60°)=0.5, sin(60°)=0.866
                                    ↑ Z-axis unchanged
                                                      ↑ Degrees mode
```

2. **Apply to RHP surface**:
```mcnp
c Original surface with TR
400  400  rhp  0 0 0  0 0 68  0 1.6 0  $ Uses TR400
     ↑ TR number
```

**Method 2: Direct RHP Rotation (R-vector)**

1. **Calculate rotated R-vector**:
```
Original R-vector: (0, 1.6, 0) = along +Y
Rotation matrix (60° about Z):
[cos(60°)  -sin(60°)  0] [0  ]   [-1.386]
[sin(60°)   cos(60°)  0] [1.6] = [ 0.8  ]
[0          0         1] [0  ]   [ 0    ]

Rotated R-vector: (-1.386, 0.8, 0)
```

2. **Update RHP surface**:
```mcnp
c Rotated RHP surface
400 rhp  0 0 0  0 0 68  -1.386 0.8 0  $ R-vector rotated 60°
```

**Hexagonal Symmetry Consideration**:
- Hexagonal lattices have **60° rotational symmetry**
- Rotating 60° produces identical lattice pattern (if uniform fill)
- For mixed patterns, verify fill array matches rotated positions

**Validation**:
- [ ] R-vector magnitude unchanged: |R| = 1.6 ✓
- [ ] Height vector unchanged (rotation about Z)
- [ ] Hexagonal pitch unchanged: pitch = R × √3 = 2.77 cm
- [ ] Plot geometry to verify orientation
- [ ] Lattice fill pattern consistent with rotation

**Key Points**:
- RHP rotation modifies R-vector, NOT height vector (if rotating about height axis)
- Hexagonal pitch = |R| × √3 (magnitude preserved in rotation)
- 60° rotation is special for hex lattices (symmetry)
- Arbitrary angles may break hexagonal symmetry

---

## Use Case 12: Modify Universe Hierarchy Without Breaking Nesting

**Scenario**: Add additional lattice layer between compact and particle lattice

**Original Hierarchy** (3 levels):
```
Level 5: Compact lattice (u=1110)
  └─ Fills with u=1116 (particle lattice) and u=1117 (matrix)

Level 3: Particle lattice (u=1116)
  └─ Fills with u=1114 (particle) and u=1115 (matrix cell)

Level 1: TRISO particle (u=1114)
```

**New Hierarchy** (4 levels, insert intermediate layer):
```
Level 5: Compact lattice (u=1110)
  └─ Fills with u=1118 (NEW: sub-compact layer)

Level 4: Sub-compact layer (u=1118) ← NEW LEVEL
  └─ Fills with u=1116 (particle lattice) and u=1117 (matrix)

Level 3: Particle lattice (u=1116)
  └─ Fills with u=1114 (particle) and u=1115 (matrix cell)

Level 1: TRISO particle (u=1114)
```

**Modification Procedure**:

**Step 1: Create New Universe (u=1118)**
```mcnp
c New intermediate layer universe
91119 0  -91120  u=1118 lat=1  fill=0:0 -1:1 0:0  &
     1117 1116 1117  $ 1×3 vertical sub-stack
c Matrix - Particles - Matrix

c New bounding surface
91120 rpp -0.65 0.65 -0.65 0.65 -0.131145 0.131145
c Height = 3 × original particle lattice height (3 × 0.08743)
```

**Step 2: Modify Parent Universe (u=1110) to Reference New Child**
```mcnp
c BEFORE: Compact lattice fills directly with particle lattice
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15  &
     1117 2R 1116 24R 1117 2R  $ OLD: fills with u=1116

c AFTER: Compact lattice fills with new intermediate layer
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -5:5  &
     1117 1118 1118 1118 1118 1118 1118 1118 1118 1118 1117
c NEW: 11 layers, 10 of u=1118, top/bottom u=1117
c Adjust FILL indices: -15:15 (31) → -5:5 (11)
```

**Step 3: Update Bounding Surface (if needed)**
```mcnp
c Check if compact lattice height unchanged
c Original: 31 layers × 0.08743 cm/layer = 2.710 cm
c New: 11 layers × 0.262 cm/layer = 2.882 cm ← slightly taller!

c May need to adjust compact lattice RPP or renormalize
```

**Validation**:
- [ ] New universe (u=1118) defined before used in parent
- [ ] Parent fill array updated to reference new universe
- [ ] Fill array dimensions match new structure (11 not 31)
- [ ] Bounding surfaces enclose new hierarchy
- [ ] No orphaned universes (old u=1116 no longer referenced in u=1110)
- [ ] Plot geometry to verify nesting
- [ ] Child universes (u=1114, u=1115) unchanged

**Key Points**:
- Define new universes **before** modifying parents
- Update **all references** to modified universes
- Verify **fill array dimensions** match new structure
- Preserve **child universes** if still used elsewhere
- Document hierarchy change clearly

---

## GEOMETRY EDITING VALIDATION WORKFLOW

### Validation Workflow for Complex Reactor Geometries

After any geometric modification to multi-level structures:

**Stage 1: Surface Validation**
```
1. Check surface parameters:
   - [ ] No negative radii (SO, S, C/Z, CZ)
   - [ ] RPP/RHP bounds: xmin < xmax, ymin < ymax, zmin < zmax
   - [ ] Concentric surfaces: R1 < R2 < R3 (nested)
   - [ ] Plane positions reasonable

2. Check surface relationships:
   - [ ] Off-axis cylinders (c/z): centers unchanged (unless intentional)
   - [ ] Vertical planes (pz): sequential (z1 < z2 < z3)
   - [ ] Lattice bounding surfaces: extent = N × pitch
```

**Stage 2: Cell Validation**
```
3. Check cell geometry:
   - [ ] All surface references exist
   - [ ] Boolean expressions valid (no undefined surfaces)
   - [ ] Material assignments unchanged (unless intentional)
   - [ ] Importance (IMP) consistent

4. Check volumes:
   - [ ] VOL parameters updated if geometry scaled
   - [ ] Volume scaling: V_new = V_old × factor³
```

**Stage 3: Universe Validation**
```
5. Check universe hierarchy:
   - [ ] All filled universes exist
   - [ ] No circular references (A fills B, B fills A)
   - [ ] Child universes defined before parents
   - [ ] Universe numbers unique (no conflicts)

6. Check lattice consistency:
   - [ ] FILL array size = (imax-imin+1) × (jmax-jmin+1) × (kmax-kmin+1)
   - [ ] All universe IDs in FILL array exist
   - [ ] Lattice bounding surface matches N × pitch
   - [ ] LAT type matches surface (LAT=1 → RPP, LAT=2 → RHP)
```

**Stage 4: Transformation Validation**
```
7. Check transformations:
   - [ ] TR matrices orthonormal (if manual)
   - [ ] Determinant = +1 (no reflections unless intended)
   - [ ] Translation vectors reasonable
   - [ ] TRCL references valid TR cards
   - [ ] Fill transformations place lattices within bounds
```

**Stage 5: Numbering Validation**
```
8. Check systematic numbering (if applicable):
   - [ ] Cell numbers follow scheme (e.g., 9XYZW)
   - [ ] Surface numbers consistent with hierarchy
   - [ ] Material numbers match cell assignments
   - [ ] Universe numbers follow convention
```

**Stage 6: Visual Validation**
```
9. MCNP geometry plots:
   - [ ] XY plot at representative Z
   - [ ] XZ plot at representative Y
   - [ ] YZ plot at representative X
   - [ ] Color by cell: check overlaps
   - [ ] Color by material: verify assignments
   - [ ] Zoom on critical regions (lattices, boundaries)
```

**Stage 7: Physics Validation**
```
10. Test run:
    - [ ] Run NPS 1000 to check for lost particles
    - [ ] Check for geometry errors in output
    - [ ] Verify tallies in expected locations
    - [ ] Compare results to pre-edit (if applicable)
```

---

## SYSTEMATIC NUMBERING PRESERVATION

### Maintaining Hierarchical Numbering Schemes During Edits

**Common Reactor Numbering Schemes**:

**1. AGR-1 Style (XYZW Hierarchy)**:
```
Cells:     9XYZW
           9 = Experiment ID
           X = Capsule (1-6)
           Y = Stack (1-3)
           Z = Compact (1-4)
           W = Sequence (0-9)

Surfaces:  9XYZn
           Similar hierarchy, n = surface number

Universes: XYZW
           X = Capsule
           Y = Stack
           Z = Compact
           W = Component type (0,4,5,6,7)
```

**2. PWR Assembly Style (RZA)**:
```
Cells:     ERAAZZ
           E = Element (1-9)
           R = Radial zone (1-3)
           AA = Axial zone (01-07)
           ZZ = Sub-region (00-99)

Example: 610155 = Element 6, Radial 1, Axial 01, Sub 55
```

**Editing Workflow to Preserve Numbering**:

**Step 1: Document Current Scheme**
```mcnp
c NUMBERING SCHEME:
c Cells:     9XYZW (9=AGR, X=capsule, Y=stack, Z=compact, W=seq)
c Surfaces:  9XYZn (9=AGR, X=capsule, Y=stack, Z=compact, n=ID)
c Universes: XYZW (X=capsule, Y=stack, Z=compact, W=type)
c Materials: 9XYZ (9=AGR, X=capsule, Y=stack, Z=compact)
```

**Step 2: Reserve Number Ranges**
```mcnp
c RESERVED RANGES:
c Cells:     91000-91999 (Capsule 1)
c            92000-92999 (Capsule 2)
c            [... etc ...]
c Surfaces:  9100-9199 (Capsule 1, Stack 1)
c            9200-9299 (Capsule 1, Stack 2)
```

**Step 3: When Adding New Geometry**
```mcnp
c Adding Capsule 7 (new)
c Use next available range: 97000-97999

c NEW CELLS (follow scheme):
97101 9711 -10.924 -97111  u=9714 vol=0.092522  $ Capsule 7, Stack 1, Compact 1
                    ↑ Follows surface numbering
              ↑ Follows material numbering
                                   ↑ Follows universe numbering
```

**Step 4: When Modifying Existing Geometry**
```mcnp
c BEFORE: Stack 1, Compact 2
91131 9112 -10.924 -91211  u=1124 vol=0.092522  $ Original

c AFTER: Modified radius, PRESERVE numbering
91131 9112 -10.924 -91211  u=1124 vol=0.110000  $ Modified volume
↑ Cell number UNCHANGED
      ↑ Material UNCHANGED
                   ↑ Surface UNCHANGED
                          ↑ Universe UNCHANGED
                                 ↑ Volume UPDATED
```

**Step 5: When Scaling Entire Assembly**
```mcnp
c All cells/surfaces/universes in capsule 1 retain numbers
c Only PARAMETERS change (radii, positions, volumes)

c Surfaces (capsule 1, stack 1, compact 1):
91111 so   0.020982  $ Kernel (scaled from 0.017485)
91112 so   0.033486  $ Buffer (scaled from 0.027905)
↑ Surface numbers PRESERVED, radii CHANGED
```

**Key Points**:
- Number assignments are **permanent identity** of geometric elements
- When editing, **preserve numbers**, change **parameters**
- When adding, use **next available number in reserved range**
- Document numbering scheme prominently
- Validate: no number conflicts, scheme consistent

---

## HEXAGONAL GEOMETRY EDITING SPECIFICS

### Special Considerations for LAT=2 Hexagonal Lattices

**Hexagonal Geometry Parameters**:
```mcnp
c RHP surface definition
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
100 rhp  0 0 0  0 0 68  0 1.6 0

Parameters:
  Origin: (0, 0, 0)
  Height vector: (0, 0, 68) → 68 cm along +Z
  R vector: (0, 1.6, 0) → 1.6 cm along +Y
  Hexagonal pitch: |R| × √3 = 1.6 × 1.732 = 2.771 cm
```

**Editing Hexagonal Pitch**:

**Method 1: Scale R-Vector**
```mcnp
c Original (pitch = 2.771 cm)
100 rhp  0 0 0  0 0 68  0 1.6 0

c Scaled 1.2× (new pitch = 3.325 cm)
100 rhp  0 0 0  0 0 68  0 1.92 0
                              ↑ 1.6 × 1.2
```

**Method 2: Rotate R-Vector**
```mcnp
c Original (R along +Y)
100 rhp  0 0 0  0 0 68  0 1.6 0

c Rotated 30° about Z
c R_new = R × rotation_matrix(30°, Z-axis)
c (0, 1.6, 0) → (1.386, 0.8, 0)
100 rhp  0 0 0  0 0 68  1.386 0.8 0
```

**Editing Hexagonal Assembly Height**:
```mcnp
c Original (68 cm height)
100 rhp  0 0 0  0 0 68  0 1.6 0

c Scaled 1.5× (102 cm height)
100 rhp  0 0 0  0 0 102  0 1.6 0
                      ↑ 68 × 1.5
```

**Hexagonal Lattice Fill Editing**:

**Original 7×7 hex pattern** (fill=-3:3 -3:3 0:0 = 49 elements):
```mcnp
c 7 rows, staggered
300 300 300 300 300 300 300
 300 300 100 100 100 300 300
  300 100 100 200 100 100 300
   300 100 200 100 200 100 300  ← Center row
    300 100 100 200 100 100 300
     300 300 100 100 100 300 300
      300 300 300 300 300 300 300
```

**Expanded to 9×9 hex pattern** (fill=-4:4 -4:4 0:0 = 81 elements):
```mcnp
c 9 rows, staggered
300 300 300 300 300 300 300 300 300
 300 300 300 100 100 100 300 300 300
  300 300 100 100 200 100 100 300 300
   300 100 100 200 100 200 100 100 300
    300 100 200 100 200 100 200 100 300  ← Center row
     300 100 100 200 100 200 100 100 300
      300 300 100 100 200 100 100 300 300
       300 300 300 100 100 100 300 300 300
        300 300 300 300 300 300 300 300 300
```

**Validation for Hexagonal Edits**:
- [ ] R-vector magnitude: |R| = sqrt(R_x² + R_y² + R_z²)
- [ ] Height vector perpendicular to R-vector (usually)
- [ ] Hexagonal pitch = |R| × √3
- [ ] Lattice extent ≈ (max_index) × pitch (approximate for hex)
- [ ] Fill pattern symmetric (if uniform hex)
- [ ] No overlaps in hex packing

**Key Points**:
- RHP has **2 vectors**: height and R
- Hexagonal pitch = **|R| × √3**, NOT |R|
- R-vector can point in any direction (defines hex orientation)
- Height vector usually perpendicular to R (but not required)
- Hex fill patterns are **staggered rows** (60° symmetry)

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
