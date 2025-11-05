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

**END OF SURFACE EDITING GUIDE**
