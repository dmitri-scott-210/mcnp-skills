# MCNP Surface Editing Guide

**Purpose:** Comprehensive guide to editing MCNP surface parameters

**Source:** MCNP6.3.1 Manual Chapter 5.03 (Surface Cards)

---

## Surface Types Overview

MCNP surfaces fall into three categories:
1. **Simple surfaces** - Easy to edit directly (planes, spheres, cylinders)
2. **Macrobodies** - Composite shapes, straightforward parameter editing
3. **General quadrics** - Complex, prefer TR card transformations

---

## Simple Surfaces (Direct Editing)

###

 Planes

#### PX, PY, PZ (Axis-Aligned Planes)

**Format:**
```
PX  D  $ Plane perpendicular to x-axis at x=D
PY  D  $ Plane perpendicular to y-axis at y=D
PZ  D  $ Plane perpendicular to z-axis at z=D
```

**Parameters:**
- D: Distance from origin along axis (cm)

**Editing:**
```
Original: 10  PX  5.0   $ Plane at x=5
Moved:    10  PX  8.0   $ Plane at x=8 (+3 cm shift)
```

**Scaling:** Multiply D by scale factor
```
Original: 10  PZ  10.0
Scaled 1.5×: 10  PZ  15.0
```

---

#### P (General Plane)

**Format:**
```
P  A B C D
```
**Equation:** Ax + By + Cz - D = 0

**Parameters:**
- A, B, C: Normal vector components (not necessarily unit)
- D: Distance parameter

**Editing:**
- **Move parallel:** Change D only
- **Rotate:** Change A, B, C (normal vector)

**Example:**
```
Original: 20  P  1 0 0  5  $ Plane x=5
Moved:    20  P  1 0 0  8  $ Plane x=8
Rotated:  20  P  0.707 0.707 0  5  $ 45° rotation in xy-plane
```

**Scaling:** Multiply D by scale factor, keep A,B,C unchanged

---

### Spheres

#### SO (Sphere at Origin)

**Format:**
```
SO  R
```

**Parameters:**
- R: Radius (cm)

**Editing:**
```
Original: 30  SO  10.0   $ R=10 cm
Scaled:   30  SO  15.0   $ R=15 cm (1.5× scale)
```

**Note:** Cannot move - convert to S surface for repositioning

---

#### S (General Sphere)

**Format:**
```
S  x y z  R
```

**Parameters:**
- x, y, z: Center coordinates (cm)
- R: Radius (cm)

**Editing:**
```
Original: 40  S  5 0 0  10.0   $ Center (5,0,0), R=10
Moved:    40  S  8 0 0  10.0   $ Moved to (8,0,0)
Scaled:   40  S  5 0 0  15.0   $ R scaled to 15
Both:     40  S  7.5 0 0  15.0  $ Moved and scaled
```

**Uniform scaling:** Multiply R and center coordinates by factor
```
S  x y z  R  →  S  (x×f) (y×f) (z×f)  (R×f)
```

---

### Cylinders

#### C/X, C/Y, C/Z (Axis-Aligned Cylinders)

**Format:**
```
C/X  y z  R  $ Cylinder along x-axis
C/Y  x z  R  $ Cylinder along y-axis
C/Z  x y  R  $ Cylinder along z-axis
```

**Parameters:**
- Position of axis in other two coordinates
- R: Radius (cm)

**Editing:**
```
Original: 50  C/Z  0 0  5.0   $ Along z-axis, center (0,0), R=5
Moved:    50  C/Z  2 3  5.0   $ Axis at (2,3) in xy-plane
Scaled:   50  C/Z  0 0  7.5   $ R=7.5 (1.5× scale)
```

**Uniform scaling:**
```
C/Z  x y  R  →  C/Z  (x×f) (y×f)  (R×f)
```

---

#### CX, CY, CZ (Axis-Aligned, Origin-Centered)

**Format:**
```
CX  R  $ Along x-axis through origin
CY  R  $ Along y-axis through origin
CZ  R  $ Along z-axis through origin
```

**Editing:** Only radius can change
```
Original: 60  CZ  5.0
Scaled:   60  CZ  7.5  $ 1.5× scale
```

**To move:** Convert to C/Z format with position

---

### Cones

#### K/X, K/Y, K/Z (Axis-Aligned Cones)

**Format:**
```
K/Z  x y z  t²  ±1
```

**Parameters:**
- x, y, z: Apex position
- t²: Tangent squared of half-angle
- ±1: Sheet selector

**Editing:**
```
Original: 70  K/Z  0 0 0  1.0  1   $ Apex at origin, 45° half-angle
Moved:    70  K/Z  0 0 5  1.0  1   $ Apex at z=5
```

**Scaling apex:**
```
K/Z  x y z  t²  ±1  →  K/Z  (x×f) (y×f) (z×f)  t²  ±1
```

**Note:** t² (angle) typically unchanged during scaling

---

## Macrobodies (Straightforward Editing)

### RPP (Rectangular Parallelepiped)

**Format:**
```
RPP  xmin xmax  ymin ymax  zmin zmax
```

**Editing:**
```
Original: 100  RPP  -5 5  -5 5  -5 5   $ 10×10×10 box
Moved:    100  RPP  0 10  -5 5  -5 5   $ Shifted +5 in x
Scaled:   100  RPP  -7.5 7.5  -7.5 7.5  -7.5 7.5  $ 1.5× uniform
Stretched: 100  RPP  -5 5  -5 5  -10 10  $ 2× in z only
```

**Uniform scaling:** Multiply all 6 parameters by factor

**Non-uniform scaling:**
```
RPP  xmin xmax  ymin ymax  zmin zmax
→  RPP  (xmin×fx) (xmax×fx)  (ymin×fy) (ymax×fy)  (zmin×fz) (zmax×fz)
```

---

### BOX (General Parallelepiped)

**Format:**
```
BOX  vx vy vz  a1 a2 a3  b1 b2 b3  c1 c2 c3
```

**Parameters:**
- v: Corner position vector
- a, b, c: Three edge vectors from corner

**Editing:**
```
Original: 110  BOX  0 0 0  10 0 0  0 10 0  0 0 10  $ Aligned box
Scaled:   110  BOX  0 0 0  15 0 0  0 15 0  0 0 15  $ 1.5× uniform
Rotated:  110  BOX  0 0 0  7 7 0  -7 7 0  0 0 10  $ 45° in xy
```

**Uniform scaling:** Multiply v and all edge vectors by factor

---

### SPH (Sphere)

**Format:**
```
SPH  x y z  R
```

**Identical to S surface**

**Editing:** Same as S surface

---

### RCC (Right Circular Cylinder)

**Format:**
```
RCC  x y z  vx vy vz  R
```

**Parameters:**
- x, y, z: Base center
- vx, vy, vz: Axis vector (base to top)
- R: Radius

**Editing:**
```
Original: 120  RCC  0 0 0  10 0 0  2.0  $ Along x, length 10, R=2
Moved:    120  RCC  5 0 0  10 0 0  2.0  $ Base at (5,0,0)
Scaled:   120  RCC  0 0 0  15 0 0  3.0  $ 1.5× (length and R)
Rotated:  120  RCC  0 0 0  7 7 0  2.0  $ Axis rotated 45°
```

**Uniform scaling:**
```
RCC  x y z  vx vy vz  R  →  RCC  (x×f) (y×f) (z×f)  (vx×f) (vy×f) (vz×f)  (R×f)
```

---

### RHP (Right Hexagonal Prism)

**Format:**
```
RHP  vx vy vz  hx hy hz  r1 r2 r3
```

**Parameters:**
- v: Base center
- h: Axis vector (height)
- r: Apothem vector (perpendicular to axis, points to face center)

**Editing:**
```
Original: 130  RHP  0 0 0  0 0 10  2 0 0  $ Height 10, apothem 2
Scaled:   130  RHP  0 0 0  0 0 15  3 0 0  $ 1.5× uniform
```

**Uniform scaling:** Multiply v, h, and r vectors by factor

**Note:** Apothem r must be perpendicular to axis h

---

### REC (Right Elliptical Cylinder)

**Format:**
```
REC  x y z  vx vy vz  r1x r1y r1z  r2x r2y r2z
```

**Parameters:**
- v: Base center
- h: Axis vector (v components)
- r1: Major axis vector
- r2: Minor axis vector

**Editing:**
```
Original: 140  REC  0 0 0  0 0 10  5 0 0  0 2 0  $ Ellipse 5×2
Scaled:   140  REC  0 0 0  0 0 15  7.5 0 0  0 3 0  $ 1.5× uniform
```

**Non-uniform scaling:**
- Multiply height vector by fz
- Multiply r1 by fx (or desired major axis scale)
- Multiply r2 by fy (or desired minor axis scale)

---

## General Quadrics (Use TR Cards Instead)

### GQ (General Quadric)

**Format:**
```
GQ  A B C D E F G H J K
```

**Equation:**
```
Ax² + By² + Cz² + Dxy + Eyz + Fzx + Gx + Hy + Jz + K = 0
```

**Editing Approach:**
- **DO NOT edit coefficients directly** (extremely error-prone)
- **USE TR card for transformations**

**Example:**
```
Original: 200  GQ  1 1 1  0 0 0  0 0 0  -25  $ Sphere R=5
Transform: *TR1  10 0 0  $ Move sphere to (10,0,0)
           200  1  GQ  1 1 1  0 0 0  0 0 0  -25
```

---

## Scaling Effects by Surface Type

### Uniform Scaling (Factor f)

| Surface | Parameters Affected | Formula |
|---------|---------------------|---------|
| PX, PY, PZ | D | D → D×f |
| P | D only | D → D×f, A,B,C unchanged |
| SO | R | R → R×f |
| S | x,y,z,R | All → All×f |
| C/X, C/Y, C/Z | position, R | All → All×f |
| RPP | all 6 bounds | All → All×f |
| RCC | base, axis, R | All → All×f |
| SPH | center, R | All → All×f |

### Non-Uniform Scaling (fx, fy, fz)

**Only feasible for:**
- RPP: Scale bounds independently
- BOX: Scale edge vectors independently
- REC: Scale axis and radii independently

**Difficult/Impossible for:**
- Spheres (become ellipsoids - use REC or ELL)
- Cylinders (become elliptical - use REC)

**Solution:** Use transformation matrix with non-uniform diagonal

---

## Coordinate System Considerations

### Global vs. Transformed Coordinates

**Surface defined in global system:**
```
10  S  5 0 0  3.0  $ Sphere at (5,0,0) in global
```

**Surface with TR card:**
```
*TR1  10 0 0  $ TR defines new system
10  1  S  0 0 0  3.0  $ Sphere at origin of TR1 system
$ = (10,0,0) in global system
```

**Editing transformed surfaces:**
- Option 1: Edit TR card (non-destructive)
- Option 2: Remove TR, edit surface in global, re-add TR

---

## Surface Editing Workflows

### Workflow 1: Direct Parameter Edit

**Use when:**
- Simple surface (PX, S, RCC, RPP, etc.)
- Small modification
- No transformation involved

**Steps:**
1. Identify surface type
2. Calculate new parameters (scaling, moving)
3. Update surface card
4. Verify with geometry plot

---

### Workflow 2: TR Card Addition

**Use when:**
- Complex surface (GQ)
- Repeated transformations needed
- Want reversibility

**Steps:**
1. Create TR card with desired transformation
2. Apply TR number to surface card
3. Original surface parameters unchanged
4. Verify with geometry plot

---

### Workflow 3: Macrobody to Fundamental Surfaces

**Use when:**
- Need individual face control
- Applying different boundary conditions to faces
- Complex Boolean operations

**Example:**
```
Original:
100  RPP  -5 5  -5 5  -5 5

Converted:
101  PX  -5  $ xmin
102  PX   5  $ xmax
103  PY  -5  $ ymin
104  PY   5  $ ymax
105  PZ  -5  $ zmin
106  PZ   5  $ zmax

Cell: 1  1  -1.0  101 -102  103 -104  105 -106  IMP:N=1
```

**After conversion, can edit each face independently**

---

## Volume Calculations After Scaling

### Uniform Scaling (Factor f)

**Volume scales by f³:**
```
V_new = V_original × f³
```

**Examples:**
```
Sphere R=10: V = 4/3 π(10³) = 4188.79 cm³
After 1.2× scale: V = 4/3 π(12³) = 7238.23 cm³
Factor: 1.2³ = 1.728 ✓

Box 10×10×10: V = 1000 cm³
After 1.5× scale: V = 15×15×15 = 3375 cm³
Factor: 1.5³ = 3.375 ✓
```

### Non-Uniform Scaling (fx, fy, fz)

**Volume scales by product:**
```
V_new = V_original × fx × fy × fz
```

**Example:**
```
Box 10×10×10: V = 1000 cm³
Scale (2, 1, 1.5): V = 20×10×15 = 3000 cm³
Factor: 2×1×1.5 = 3.0 ✓
```

### VOL Parameter Update

**After scaling:**
```
Original: VOL=1000.0
After 1.5× scale: VOL=3375.0  $ Must update!
```

**If VOL omitted:** MCNP calculates automatically (slower but correct)

---

## Common Editing Patterns

### Pattern 1: Scale Entire Geometry

```
1. List all surfaces with dimensions
2. Multiply all dimensions by scale factor
3. Update VOL parameters (×f³)
4. Verify with plot
5. Test run (NPS 100)
```

### Pattern 2: Move Component

```
1. Identify all surfaces in component
2. Add translation to positions
3. OR use TR card + TRCL on cell
4. Verify no overlaps with neighbors
```

### Pattern 3: Rotate Component

```
1. Calculate rotation matrix (or use Euler angles)
2. Create TR card
3. Apply to surfaces OR use TRCL on cell
4. Verify axis orientation with plot
```

### Pattern 4: Expand Lattice

```
1. Identify lattice boundaries (LAT cell surfaces)
2. Calculate new dimensions (pitch × new count)
3. Update bounding surface
4. Update FILL array
5. Verify with lattice plot
```

---

## Surface Editing Best Practices

1. **Visualize before and after** - Always plot geometry
2. **Check physical units** - Confirm dimensions reasonable (cm, not m or mm by accident)
3. **Verify sense** - Ensure +/- conventions maintained
4. **Test incrementally** - Change one surface, test, then continue
5. **Document changes** - Comment edits in input file
6. **Update dependent parameters** - VOL, IMP, etc.
7. **Use TR for complex surfaces** - Easier than manual coefficient editing
8. **Verify relationships** - Surfaces that were touching should remain so

---

## Quick Reference: Editing Difficulty

### Easy (Direct Edit)
- PX, PY, PZ - Change D
- SO, S - Change R and/or center
- C/X, C/Y, C/Z - Change position and R
- RPP - Change all 6 bounds

### Moderate (Direct Edit Possible)
- P - Change normal or D
- RCC, REC, RHP - Change vectors
- BOX - Change vectors
- Cones - Change apex, angle

### Difficult (Use TR Instead)
- GQ - General quadric
- TOR - Torus
- ELL - Ellipsoid
- Complex Boolean combinations

---

## Hexagonal Geometry Surface Editing

### RHP (Right Hexagonal Prism) - Complete Reference

**Format:**
```
RHP  vx vy vz  hx hy hz  r1 r2 r3
```

**Parameters:**
- **v** = (vx, vy, vz): Base center position (origin of hexagon)
- **h** = (hx, hy, hz): Height vector (axis of prism, base to top)
- **r** = (r1, r2, r3): R-vector (perpendicular to h, points to face center)

**Key Relationships:**
- **Hexagonal pitch**: pitch = |r| × √3 (NOT |r|!)
- **R-vector magnitude**: |r| = apothem (distance from center to face midpoint)
- **Height**: |h| = prism height
- **R perpendicular to h**: r · h = 0 (usually, but not strictly required)

---

### RHP Parameters and Geometry

**Example:**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
```

**Interpretation:**
- **Origin**: (0, 0, 0) - base center at global origin
- **Height vector**: (0, 0, 68) - extends 68 cm along +Z axis
- **R-vector**: (0, 1.6, 0) - points 1.6 cm along +Y axis
  - Magnitude: |r| = 1.6 cm (apothem)
  - Hexagonal pitch: 1.6 × 1.732 = 2.771 cm
  - Hexagon oriented with **flat sides parallel to X-Z plane**

**Visualization:**
```
Top view (looking down -Z):

       Flat side
      ___________
     /           \
    /             \
   |       ●       |  ← R-vector points to this flat side (along +Y)
    \             /      Center at (0,0)
     \___________/       Apothem R = 1.6 cm
                         Pitch = R×√3 = 2.771 cm

Height: 68 cm (along Z)
```

---

### Hexagonal Pitch Calculation

**Formula:**
```
pitch = |R| × √3
```

Where:
- |R| = magnitude of R-vector = apothem
- √3 ≈ 1.732
- pitch = distance between parallel sides of hexagon

**Example:**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
c                              ↑ R-vector

R-vector: (0, 1.6, 0)
|R| = sqrt(0² + 1.6² + 0²) = 1.6 cm
pitch = 1.6 × 1.732 = 2.771 cm
```

**For hexagonal lattices (LAT=2):**
- Lattice spacing = pitch
- Pin positions separated by pitch × √3
- RHP surface defines SINGLE hexagonal cell
- Lattice FILL indices determine array extent

---

### Editing RHP Surfaces

#### Edit 1: Change Hexagonal Pitch (Scale R-Vector)

**Original:**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
c Pitch = 1.6 × √3 = 2.771 cm
```

**Scaled 1.2× (larger pitch):**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.92 0
c                              ↑ R = 1.6 × 1.2 = 1.92 cm
c New pitch = 1.92 × √3 = 3.325 cm
```

**Verification:**
- R-vector magnitude: 1.92 cm ✓
- Height vector unchanged: 68 cm ✓
- Pitch increased by 1.2× (2.771 → 3.325 cm) ✓

---

#### Edit 2: Change Prism Height (Scale H-Vector)

**Original:**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
c Height = 68 cm
```

**Scaled 1.5× (taller prism):**
```mcnp
100 rhp  0 0 0  0 0 102  0 1.6 0
c                      ↑ H = 68 × 1.5 = 102 cm
c R-vector unchanged
c Pitch unchanged = 2.771 cm
```

**Verification:**
- Height vector: 102 cm ✓
- R-vector unchanged: 1.6 cm ✓
- Pitch unchanged: 2.771 cm ✓

---

#### Edit 3: Rotate Hexagon (Rotate R-Vector)

**Original (R along +Y):**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
c Hexagon with flat sides parallel to X-Z plane
```

**Rotated 30° about Z-axis:**

**Method 1: Calculate rotated R-vector**
```
Rotation matrix (30° about Z):
[cos(30°)  -sin(30°)  0] [0  ]   [0.866×0 - 0.5×1.6 ]   [-0.8  ]
[sin(30°)   cos(30°)  0] [1.6] = [0.5×0 + 0.866×1.6 ] = [1.386 ]
[0          0         1] [0  ]   [0                 ]   [0     ]

cos(30°) = 0.866
sin(30°) = 0.5
```

```mcnp
100 rhp  0 0 0  0 0 68  -0.8 1.386 0
c                              ↑ Rotated R-vector
c Magnitude: sqrt(0.8² + 1.386²) = 1.6 ✓
c Pitch unchanged: 1.6 × √3 = 2.771 cm ✓
```

**Method 2: Use TR card**
```mcnp
*TR100  0 0 0  0 0 30  1  $ 30° rotation about Z
100  100  rhp  0 0 0  0 0 68  0 1.6 0
     ↑ Uses TR100
```

**Effect of 30° rotation:**
- Original: Flat sides parallel to X-Z plane
- Rotated: Hexagon rotated 30° → points now align with ±Y axes
- Pitch magnitude preserved: 2.771 cm ✓

---

#### Edit 4: Move RHP (Translate Origin)

**Original (centered at origin):**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
```

**Translated to (50, 30, 10):**
```mcnp
100 rhp  50 30 10  0 0 68  0 1.6 0
c        ↑ New origin (base center)
c                  ↑ Height vector unchanged (relative to new origin)
c                          ↑ R-vector unchanged
```

**Interpretation:**
- Base center at (50, 30, 10)
- Top center at (50, 30, 78) [base + h]
- Orientation unchanged (R-vector same)
- Pitch unchanged

---

#### Edit 5: Uniform Scaling (All Dimensions)

**Original:**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
```

**Scaled 1.3× (all dimensions):**
```mcnp
100 rhp  0 0 0  0 0 88.4  0 2.08 0
c        ↑ Origin unchanged (at 0,0,0)
c                  ↑ H = 68 × 1.3 = 88.4 cm
c                           ↑ R = 1.6 × 1.3 = 2.08 cm
c Pitch = 2.08 × √3 = 3.603 cm (was 2.771 cm)
```

**Verification:**
- Height scaled: 68 → 88.4 cm ✓
- R-vector scaled: 1.6 → 2.08 cm ✓
- Pitch scaled: 2.771 → 3.603 cm ✓
- Volume scaled by 1.3³ = 2.197 ✓

---

### RHP Orientation and R-Vector Direction

**R-vector defines hexagon orientation:**

**Case 1: R along +Y (flat sides parallel to X-Z)**
```mcnp
100 rhp  0 0 0  0 0 68  0 1.6 0
```
```
Top view:
      ___________
     /           \
    /             \
   |       ●----→  |  R points to flat side (along +Y)
    \             /
     \___________/
```

**Case 2: R along +X (flat sides parallel to Y-Z)**
```mcnp
100 rhp  0 0 0  0 0 68  1.6 0 0
```
```
Top view:
        /\
       /  \
      /    \
     |  ●→ |  R points to flat side (along +X)
      \    /
       \  /
        \/
```

**Case 3: R at 45° (flat side at 45°)**
```mcnp
100 rhp  0 0 0  0 0 68  1.131 1.131 0
c                              ↑ R = (1.131, 1.131, 0)
c                              |R| = sqrt(1.131² + 1.131²) = 1.6 cm
c                              Angle = 45° from +X
```

**Key Point:** R-vector direction determines hexagon orientation, NOT size

---

### Hexagonal Symmetry and Rotation

**60° Rotational Symmetry:**
- Hexagons have 6-fold symmetry
- Rotating by 60° produces identical hexagon (if uniform)
- Rotating by 30° changes flat-to-flat to point-to-point orientation

**Example: 60° Rotation**
```
Original R-vector: (0, 1.6, 0)
After 60° rotation about Z:
  x' = 0×cos(60°) - 1.6×sin(60°) = -1.386
  y' = 0×sin(60°) + 1.6×cos(60°) = 0.8
  R' = (-1.386, 0.8, 0)

Magnitude: |R'| = sqrt(1.386² + 0.8²) = 1.6 ✓
Pitch unchanged: 2.771 cm ✓
```

**Special Angles:**
- 0°, 60°, 120°, 180°, 240°, 300° → Same orientation (6-fold symmetry)
- 30°, 90°, 150°, 210°, 270°, 330° → Point-to-point (rotated by 30°)

---

### RHP Editing Patterns

**Pattern 1: Scale Assembly (Preserve Orientation)**
```mcnp
c Original
100 rhp  0 0 0  0 0 68  0 1.6 0

c Scaled 1.2× (all dimensions)
100 rhp  0 0 0  0 0 81.6  0 1.92 0
c Scale H: 68 × 1.2 = 81.6
c Scale R: 1.6 × 1.2 = 1.92
c Orientation preserved (R still along +Y)
```

**Pattern 2: Change Pitch Only (Preserve Height)**
```mcnp
c Original (pitch = 2.771 cm)
100 rhp  0 0 0  0 0 68  0 1.6 0

c New pitch = 3.0 cm
c Required R = pitch / √3 = 3.0 / 1.732 = 1.732 cm
100 rhp  0 0 0  0 0 68  0 1.732 0
c Height unchanged, R increased for larger pitch
```

**Pattern 3: Rotate Assembly (Preserve Size)**
```mcnp
c Original
100 rhp  0 0 0  0 0 68  0 1.6 0

c Rotated 45° about Z
c R' = (R×cos(45°), R×sin(45°), 0) assuming R was along +X
c But R is along +Y, so:
c R' = (-R×sin(45°), R×cos(45°), 0) = (-1.131, 1.131, 0)
100 rhp  0 0 0  0 0 68  -1.131 1.131 0
c Magnitude preserved: |R'| = 1.6 ✓
```

---

### Hexagonal Lattice (LAT=2) Considerations

**RHP defines SINGLE hexagonal cell:**
```mcnp
c Hexagonal lattice cell
400 0  -400  u=400 lat=2  fill=-3:3 -3:3 0:0  &
    [... fill array ...]

c RHP surface (defines ONE hexagonal cell)
400 rhp  0 0 0  0 0 68  0 1.6 0
c This RHP is the "unit cell" - lattice replicates it
```

**Lattice extent determined by FILL indices:**
- `fill=-3:3` means 7×7 grid (but hexagonal, not rectangular)
- Total hexagons in 7-ring pattern: 127 (not 49!)
- RHP pitch = spacing between hexagon centers

**When editing hexagonal lattice:**
1. RHP surface: defines single cell geometry
2. FILL indices: determine how many cells
3. Lattice bounding surface: must enclose all filled cells

---

### RHP Validation Checklist

After editing RHP surface:
- [ ] **R-vector magnitude**: |R| = sqrt(r1² + r2² + r3²)
- [ ] **Pitch calculation**: pitch = |R| × √3
- [ ] **Height vector**: |h| = sqrt(hx² + hy² + hz²)
- [ ] **Perpendicularity** (if intended): r · h = 0
- [ ] **Orientation**: R-vector points toward intended face
- [ ] **Bounding**: RHP encloses intended region
- [ ] **Lattice fit** (if LAT=2): cells fit within bounding surface

---

### Common RHP Errors

**Error 1: Confusing |R| with Pitch**
```mcnp
c WRONG: Using pitch value as R
c Intended pitch: 3.0 cm
100 rhp  0 0 0  0 0 68  0 3.0 0  ✗
c This gives pitch = 3.0 × √3 = 5.196 cm (NOT 3.0!)

c CORRECT: R = pitch / √3
100 rhp  0 0 0  0 0 68  0 1.732 0  ✓
c Pitch = 1.732 × √3 = 3.0 cm ✓
```

---

**Error 2: Scaling Only R (Forgetting H)**
```mcnp
c WRONG: Scale R but not H
c Intent: Uniform 1.5× scale
100 rhp  0 0 0  0 0 68  0 2.4 0  ✗
c R scaled: 1.6 × 1.5 = 2.4 ✓
c H NOT scaled: still 68 (should be 102) ✗

c CORRECT: Scale both R and H
100 rhp  0 0 0  0 0 102  0 2.4 0  ✓
c R: 1.6 × 1.5 = 2.4 ✓
c H: 68 × 1.5 = 102 ✓
```

---

**Error 3: Wrong Rotation Calculation**
```mcnp
c WRONG: Rotating R-vector without preserving magnitude
c Original: R = (0, 1.6, 0)
c Attempt 60° rotation (incorrect calculation)
100 rhp  0 0 0  0 0 68  -1.5 0.9 0  ✗
c Magnitude: sqrt(1.5² + 0.9²) = 1.75 ≠ 1.6 ✗

c CORRECT: Preserve magnitude
c cos(60°) = 0.5, sin(60°) = 0.866
c R' = (0×0.5 - 1.6×0.866, 0×0.866 + 1.6×0.5, 0)
c    = (-1.386, 0.8, 0)
100 rhp  0 0 0  0 0 68  -1.386 0.8 0  ✓
c Magnitude: sqrt(1.386² + 0.8²) = 1.6 ✓
```

---

### Quick Reference: RHP Editing

**Scale pitch:**
```
R_new = R_old × scale_factor
pitch_new = pitch_old × scale_factor
```

**Scale height:**
```
H_new = H_old × scale_factor
```

**Rotate about Z (preserving magnitude):**
```
R' = (R_x×cos(θ) - R_y×sin(θ), R_x×sin(θ) + R_y×cos(θ), R_z)
```

**Translate:**
```
v_new = v_old + translation_vector
H unchanged
R unchanged
```

---

**END OF HEXAGONAL GEOMETRY SECTION**

---

**END OF SURFACE EDITING GUIDE**
