# MCNP Transformation Specifications (TR/TRCL Cards)

**Purpose:** Complete reference for MCNP coordinate transformation cards

**Source:** MCNP6.3.1 Manual Chapter 5.05 (Geometry Data Cards)

---

## TR Card Overview

The TR (transformation) card defines coordinate system transformations in MCNP. Transformations can be applied to:
- **Surfaces:** Via TR number on surface card (e.g., `10 1 SO 5.0` uses TR1)
- **Cells:** Via TRCL parameter (e.g., `TRCL=1` in cell card)
- **Universe fills:** Via TRCL in FILL parameter

**Purpose:**
- Translate (move) geometry components
- Rotate geometry about axes
- Combine translation and rotation
- Create repeated structures with variations

---

## TR Card Formats

### Format 1: Translation Only

```
*TRn  dx dy dz
```

**Parameters:**
- `n`: Transformation number (1-999)
- `dx, dy, dz`: Translation vector (cm by default)
- `*` prefix: Required (marks card as transformation)

**Example:**
```
*TR1  10 0 0  $ Move +10 cm in x-direction
```

**Effect:**
- Origin shifts from (0,0,0) to (dx,dy,dz)
- Axes remain aligned with global system

---

### Format 2: Rotation Only (about origin)

```
*TRn  0 0 0  a11 a12 a13  a21 a22 a23  a31 a32 a33  m
```

**Parameters:**
- Translation: (0, 0, 0) - no translation
- Rotation matrix: 3×3 matrix (9 elements)
- `m`: Interpretation flag

**Example:**
```
*TR2  0 0 0  0 1 0  -1 0 0  0 0 1  1
      ^no translation
              ^90° rotation about z-axis
                                      ^m=1 (interpret as degrees)
```

---

### Format 3: Combined Rotation + Translation

```
*TRn  dx dy dz  a11 a12 a13  a21 a22 a23  a31 a32 a33  m
```

**Order of Operations (MCNP convention):**
1. First: Apply rotation (about origin of new system)
2. Then: Apply translation

**Example:**
```
*TR3  5 0 0  0.866 0 0.5  0 1 0  -0.5 0 0.866  1
      ^translate (5,0,0)
               ^rotate 30° about y-axis
                                              ^degrees
```

---

## Rotation Matrix Specification

### General 3×3 Rotation Matrix

```
     | a11  a12  a13 |
R =  | a21  a22  a23 |
     | a31  a32  a33 |
```

**Requirements (Orthonormal):**
1. **Rows perpendicular:**
   - Row1 · Row2 = 0
   - Row1 · Row3 = 0
   - Row2 · Row3 = 0

2. **Rows unit length:**
   - |Row1| = 1
   - |Row2| = 1
   - |Row3| = 1

3. **Determinant = +1:**
   - det(R) = +1 (right-handed system)
   - det(R) = -1 (left-handed, reflection - AVOID)

**Verification:**
```python
import numpy as np
R = np.array([[a11, a12, a13],
              [a21, a22, a23],
              [a31, a32, a33]])

# Check orthonormal
assert np.allclose(R @ R.T, np.eye(3)), "Not orthonormal"
assert np.isclose(np.linalg.det(R), 1.0), "Determinant not +1"
```

---

### Shortcut Rotation Specifications

MCNP allows fewer than 9 elements for common rotations:

#### 3 Elements (Euler Angles)
```
*TRn  dx dy dz  α β γ  m
```
- α: Rotation about x-axis (degrees if m=1)
- β: Rotation about y-axis
- γ: Rotation about z-axis

**Example:**
```
*TR4  0 0 0  0 30 0  1  $ 30° rotation about y-axis
```

#### 5 Elements (Two Axes)
```
*TRn  dx dy dz  a b c  d e
```
Specifies:
- First row: (a, b, c) normalized to unit length
- Second row: (d, e, ?) where ? is calculated
- Third row: Cross product of first two

**Not commonly used - prefer 3 or 9 element forms**

#### 6 Elements (Two Complete Rows)
```
*TRn  dx dy dz  a11 a12 a13  a21 a22 a23
```
- First two rows specified
- Third row: Calculated as cross product

**Example:**
```
*TR5  0 0 0  1 0 0  0 1 0
$ Third row auto-calculated as (0,0,1)
```

---

## m Parameter (Interpretation Flag)

The `m` parameter controls how rotation values are interpreted:

### m = 0 (Default - Direction Cosines)
```
*TRn  dx dy dz  a11 a12 a13  a21 a22 a23  a31 a32 a33
```
- Matrix elements are **direction cosines** (exact values)
- Must satisfy orthonormality exactly
- Use for precise control

### m = 1 (Degrees for 3-Element Form)
```
*TRn  dx dy dz  α β γ  1
```
- α, β, γ interpreted as **degrees** (not radians)
- MCNP calculates rotation matrix automatically
- **Recommended for simplicity**

### m > 1 (Origin Interpretation)
```
*TRn  dx dy dz  ...  m
```
- m specifies which coordinate system's origin is used
- **Rare usage** - typically use m=0 or m=1

**Best Practice:** Use m=1 with 3-element Euler angles for simplicity

---

## Standard Rotation Matrices

### Rotation about X-Axis (θ degrees)

```
Rx(θ) = | 1    0         0      |
        | 0  cos(θ)  -sin(θ)    |
        | 0  sin(θ)   cos(θ)    |
```

**MCNP TR card:**
```
*TRn  0 0 0  θ 0 0  1  $ θ degrees about x-axis
```

**Example (45° about x):**
```
*TR10  0 0 0  45 0 0  1
```

---

### Rotation about Y-Axis (θ degrees)

```
Ry(θ) = | cos(θ)   0  sin(θ)  |
        |   0      1    0     |
        | -sin(θ)  0  cos(θ)  |
```

**MCNP TR card:**
```
*TRn  0 0 0  0 θ 0  1  $ θ degrees about y-axis
```

**Example (30° about y):**
```
*TR11  0 0 0  0 30 0  1
```

---

### Rotation about Z-Axis (θ degrees)

```
Rz(θ) = | cos(θ)  -sin(θ)  0 |
        | sin(θ)   cos(θ)  0 |
        |   0        0     1 |
```

**MCNP TR card:**
```
*TRn  0 0 0  0 0 θ  1  $ θ degrees about z-axis
```

**Example (90° about z):**
```
*TR12  0 0 0  0 0 90  1
```

---

## Combined Euler Rotations

**Order:** Rx → Ry → Rz (MCNP convention)

**Combined matrix:**
```
R(α,β,γ) = Rz(γ) × Ry(β) × Rx(α)
```

**MCNP TR card:**
```
*TRn  dx dy dz  α β γ  1
```

**Example (30° about x, 45° about y, 60° about z):**
```
*TR13  0 0 0  30 45 60  1
```

**Matrix result:**
```
R = | 0.354  -0.935   0.000 |
    | 0.612   0.231   0.756 |
    | -0.707  0.267   0.654 |
```

---

## Applying Transformations

### Method 1: Surface Transformation

**Syntax:**
```
surface_number  TR_number  surface_type  parameters
```

**Example:**
```
c TR card
*TR1  10 0 0  $ Move +10 in x

c Surface using TR1
10  1  SO  5.0  $ Sphere R=5 at (10,0,0) due to TR1
```

---

### Method 2: Cell Transformation (TRCL)

**Syntax:**
```
cell_number  material  density  geometry  TRCL=n  params
```

**Example:**
```
c TR card
*TR2  0 5 0  $ Move +5 in y

c Cell using TRCL
1  1  -1.0  -10  TRCL=2  IMP:N=1
$ Entire cell shifted +5 in y
```

**Effect:** ALL surfaces in cell definition are transformed

---

### Method 3: Fill Transformation

**Syntax:**
```
FILL=universe_number (dx dy dz  TR_number)
```

**Example:**
```
c TR card
*TR3  0 0 0  0 0 45  1  $ Rotate 45° about z

c Cell with transformed fill
10  0  -100  FILL=1 (5 0 0  3)  IMP:N=1
$ Universe 1 rotated 45° and translated to (5,0,0)
```

---

## Translation Effects on Surfaces

### Surface at Origin

**Original:**
```
10  SO  5.0  $ Sphere R=5 at origin
```

**After TR1 (translation to 10,0,0):**
```
*TR1  10 0 0
10  1  SO  5.0  $ Sphere now at (10,0,0)
```

### General Surface

**Original:**
```
20  S  3 4 0  2.0  $ Sphere at (3,4,0), R=2
```

**After TR1 (translation by 10,0,0):**
```
*TR1  10 0 0
20  1  S  3 4 0  2.0  $ Sphere now at (13,4,0)
```

**Formula:** New position = Original position + Translation vector

---

## Rotation Effects on Surfaces

### Surface Aligned with Axis

**Original:**
```
30  RCC  0 0 0  10 0 0  2.0  $ Cylinder along +x, R=2
```

**After TR2 (90° rotation about z):**
```
*TR2  0 0 0  0 0 90  1
30  2  RCC  0 0 0  10 0 0  2.0
$ Cylinder now along +y (rotated 90°)
```

**New axis:** (0, 10, 0) after rotation

---

## Coordinate System Interpretation

### Default (m=0 or m=1)

**Transformation defines NEW coordinate system:**
- Origin at (dx, dy, dz) in old system
- Axes rotated by matrix R

**Surfaces defined in NEW system:**
```
*TR1  5 0 0  0 0 90  1
10  1  SO  2.0
$ SO 2.0 = sphere R=2 at origin OF NEW SYSTEM
$ New system origin = (5,0,0) in global
$ Therefore sphere at (5,0,0) globally
```

---

## Advanced: m > 1 (Alternate Origins)

**m = 1:** Standard (displacement is translation)
**m = 2:** Displacement is in rotated system

**Rarely used - stick with m=0 or m=1**

---

## Transformation Composition

### Multiple Transformations

To apply T1 then T2:
1. **Method 1:** Apply T1, then apply T2 to result
2. **Method 2:** Compute combined transformation T3 = T2 × T1

**MCNP does NOT automatically compose transformations**

**Manual composition:**
```python
import numpy as np

# T1: Translate (5,0,0)
dx1, dy1, dz1 = 5, 0, 0
R1 = np.eye(3)

# T2: Rotate 30° about y
dx2, dy2, dz2 = 0, 0, 0
theta = np.radians(30)
R2 = np.array([[np.cos(theta), 0, np.sin(theta)],
               [0, 1, 0],
               [-np.sin(theta), 0, np.cos(theta)]])

# Combined: T_combined = T2 × T1
R_combined = R2 @ R1  # Rotation
d_combined = R2 @ np.array([dx1, dy1, dz1]) + np.array([dx2, dy2, dz2])
```

---

## Inverse Transformations

**To reverse transformation:**

**Forward:**
```
*TR1  dx dy dz  R11 R12 R13  R21 R22 R23  R31 R32 R33
```

**Inverse:**
```
*TR2  -dx' -dy' -dz'  R11 R21 R31  R12 R22 R32  R13 R23 R33
```

Where:
- Rotation inverse = Transpose (for orthonormal matrices)
- Translation inverse = -(R^T @ translation)

**Calculation:**
```python
R_inv = R.T  # Transpose
d_inv = -R.T @ np.array([dx, dy, dz])
```

---

## Validation Procedures

### Check TR Card Validity

```
1. Verify orthonormality:
   R @ R.T ≈ I (identity matrix)

2. Check determinant:
   det(R) = +1 (not -1)

3. Test with simple surface:
   - Create sphere at origin with TR
   - Plot to verify position

4. Run MCNP with short test:
   NPS 100, check for lost particles
```

### Common TR Errors

**Error 1:** Rotation matrix not orthonormal
```
Fix: Use m=1 with Euler angles instead of manual matrix
```

**Error 2:** Determinant = -1 (reflection)
```
Fix: Remove reflection, use explicit mirroring instead
```

**Error 3:** Wrong rotation direction
```
Fix: Check right-hand rule, reverse angle sign if needed
```

---

## Best Practices

1. **Use m=1 with Euler angles** - Simpler, less error-prone
2. **Verify with geometry plot** - Visual confirmation
3. **Test incrementally** - Apply transformations one at a time
4. **Document transformations** - Comment purpose in input
5. **Avoid reflections** - Use det(R)=+1 only

---

## Quick Reference: Common Transformations

### Translation
```
*TRn  dx dy dz
```

### Rotation about single axis
```
*TRn  0 0 0  α 0 0  1  $ x-axis
*TRn  0 0 0  0 β 0  1  $ y-axis
*TRn  0 0 0  0 0 γ  1  $ z-axis
```

### Combined rotation + translation
```
*TRn  dx dy dz  α β γ  1
```

### Mirror across plane (x=0)
```
*TRn  0 0 0  -1 0 0  0 1 0  0 0 1
$ Note: det=-1, AVOID unless necessary
```

---

## Fill Transformations for Lattice Positioning

### Overview

Fill transformations position entire universe structures at specified locations with optional rotation. This is essential for placing lattice universes within parent geometries, particularly in multi-level reactor structures.

**Syntax:**
```
FILL=universe_number (dx dy dz)
FILL=universe_number (dx dy dz) TR_number
```

**Applications:**
- Positioning fuel compacts in capsules
- Placing assemblies in reactor core
- Translating repeated structures
- Rotating lattice orientations

---

### Basic Fill Transformation (Translation Only)

**Example:** Position compact lattice at specific location in capsule

```mcnp
c Compact lattice universe (u=1110)
91110 0  -91118  u=1110 lat=1  fill=0:0 0:0 -15:15  &
     [... fill array ...]

c Cell that fills with compact lattice
91111 0  -97011  98005 -98051  fill=1110  (25.547039 -24.553123 19.108100)
                               ↑ Universe     ↑ Translation vector (x, y, z)

c Bounding surfaces
97011 c/z  25.547039 -24.553123  0.63500  $ Cylinder centered at fill position
98005 pz   17.81810   $ Bottom z-plane
98051 pz   20.35810   $ Top z-plane
```

**Interpretation:**
- Universe 1110 origin placed at (25.547039, -24.553123, 19.108100) in global coordinates
- All geometry in u=1110 translated by this vector
- Lattice axes remain aligned with global axes (no rotation)

---

### Fill Transformation with Rotation

**Method 1: Using TR Card Reference**

```mcnp
c Define transformation (rotation + translation)
*TR91  24.553123 -25.547039 19.108100  0 0 30  1
       ↑ Translation to Stack 2              ↑ 30° rotation about Z
                                                ↑ Degrees mode

c Cell with transformed fill
91111 0  -97011  98005 -98051  fill=1110  trcl=91
                               ↑ Universe     ↑ References TR91
```

**Method 2: Combined Syntax (MCNP6)**

```mcnp
c Some MCNP versions allow combined fill + TR syntax
91111 0  -97011  98005 -98051  fill=1110 (24.553123 -25.547039 19.108100) tr=91
```

**Note:** Syntax varies by MCNP version - check manual for your version

---

### Fill Transformation Validation

**Critical Checks:**

1. **Bounding Surface Alignment**
   ```
   - Fill position should match bounding surface center
   - For c/z: center (x, y) = fill (x, y)
   - For pz: z-range should bracket fill z-position
   ```

2. **Translation Vector Components**
   ```
   - X, Y: Position in radial plane (for cylindrical geometries)
   - Z: Axial position
   - Units: cm (MCNP default)
   ```

3. **Lattice Extent**
   ```
   - Bounding surface must enclose entire filled universe
   - Lattice extent = N × pitch (for rectangular lattices)
   - For hex: extent ≈ (max_index) × pitch × √3
   ```

**Example Validation:**
```mcnp
c Fill transformation
fill=1110 (25.547039 -24.553123 19.108100)

c Check bounding surface
97011 c/z  25.547039 -24.553123  0.63500
           ↑ Center matches fill x,y ✓

c Check z-planes
98005 pz   17.81810   $ Z_min
98051 pz   20.35810   $ Z_max
c Fill z = 19.108 is between 17.818 and 20.358 ✓

c Check lattice fits in cylinder
c Lattice extent: ±0.65 cm (from u=1110 bounding surface)
c Cylinder radius: 0.635 cm ≈ 0.65 cm ✓
```

---

### Multiple Fill Transformations

**Example:** Three stacks in hexagonal arrangement

```mcnp
c Stack 1 at 120° (hexagonal position)
91111 0  -97011  98005 -98051  fill=1110  (25.547039 -24.553123 19.108100)
97011 c/z  25.547039 -24.553123  0.63500

c Stack 2 at 180° (60° rotation from Stack 1)
91112 0  -97012  98005 -98051  fill=1110  (24.553123 -25.547039 19.108100)
97012 c/z  24.553123 -25.547039  0.63500

c Stack 3 at 240° (120° rotation from Stack 1)
91113 0  -97013  98005 -98051  fill=1110  (23.000000 -26.000000 19.108100)
97013 c/z  23.000000 -26.000000  0.63500

c Hexagonal spacing calculation:
c θ = 120°, 180°, 240° (60° intervals)
c R = 36 cm (pitch radius)
c x = x_center + R×cos(θ)
c y = y_center + R×sin(θ)
```

---

### Fill Transformation Coordinate Systems

**Interpretation:**

**Without TR card:**
```mcnp
fill=universe (dx dy dz)
```
- Translation in **global coordinate system**
- No rotation
- Simple offset of universe origin

**With TR card (TRCL):**
```mcnp
fill=universe  trcl=n
```
- TR card defines full transformation
- Translation AND rotation possible
- More complex, but more flexible

**Order of Operations (with TR card):**
1. Apply rotation (about universe origin)
2. Apply translation
3. Result: universe rotated and positioned

---

### Hexagonal Fill Patterns

**Example:** Three compacts in triangular arrangement (120° spacing)

```mcnp
c Central axis at (43.55, -55.73) in global coordinates
c Compact positions at R = 36 cm, 120° intervals

c Calculate positions:
c   θ₁ = 120°: x = 43.55 + 36×cos(120°) = 43.55 - 18 = 25.55
c              y = -55.73 + 36×sin(120°) = -55.73 + 31.18 = -24.55
c   θ₂ = 180°: x = 43.55 + 36×cos(180°) = 43.55 - 36 = 7.55
c              y = -55.73 + 36×sin(180°) = -55.73 + 0 = -55.73
c   θ₃ = 240°: x = 43.55 + 36×cos(240°) = 43.55 - 18 = 25.55
c              y = -55.73 + 36×sin(240°) = -55.73 - 31.18 = -86.91

c Compact cells with fill transformations
91111 0  -97011  98005 -98051  fill=1110  (25.55 -24.55 19.108)  $ Stack 1
91112 0  -97012  98005 -98051  fill=1110  (7.55 -55.73 19.108)   $ Stack 2
91113 0  -97013  98005 -98051  fill=1110  (25.55 -86.91 19.108)  $ Stack 3
```

---

### Editing Fill Transformations

**Scenario 1: Reposition Single Fill**

```mcnp
c BEFORE: Stack at position A
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)

c AFTER: Move to position B
91111 0  -97011  98005 -98051  fill=1110  (24.553 -25.547 19.108)
c Update bounding surface center to match
97011 c/z  24.553 -25.547  0.63500  $ Updated center
```

**Scenario 2: Add Rotation to Existing Fill**

```mcnp
c BEFORE: Translation only
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)

c AFTER: Add 45° rotation
*TR91  25.547 -24.553 19.108  0 0 45  1  $ 45° about Z
91111 0  -97011  98005 -98051  fill=1110  trcl=91
```

**Scenario 3: Scale Fill Position (with geometry)**

```mcnp
c BEFORE: Original position
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)

c AFTER: Scale geometry 1.2×, position scales too
91111 0  -97011  98005 -98051  fill=1110  (30.656 -29.464 22.930)
c                                          ↑ 25.547×1.2  ↑ -24.553×1.2  ↑ 19.108×1.2
c Bounding surfaces also scaled
97011 c/z  30.656 -29.464  0.762  $ R: 0.635×1.2
98005 pz   21.382  $ Z: 17.818×1.2
98051 pz   24.429  $ Z: 20.358×1.2
```

---

### Common Errors with Fill Transformations

**Error 1: Bounding Surface Mismatch**

```mcnp
c ERROR: Fill position doesn't match bounding surface
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)
97011 c/z  20.000 -20.000  0.635  ✗ Center at (20, -20), fill at (25.55, -24.55)
```

**Fix:**
```mcnp
c CORRECT: Center matches fill
97011 c/z  25.547 -24.553  0.635  ✓
```

---

**Error 2: Fill Outside Bounding Surface**

```mcnp
c ERROR: Lattice extent exceeds bounding surface
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)
c Lattice extent from u=1110: ±0.85 cm
97011 c/z  25.547 -24.553  0.635  ✗ R=0.635 < extent=0.85
```

**Fix:**
```mcnp
c CORRECT: Bounding surface encloses lattice
97011 c/z  25.547 -24.553  0.900  ✓ R=0.90 > extent=0.85
```

---

**Error 3: Z-Position Outside Z-Planes**

```mcnp
c ERROR: Fill z not within z-plane range
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 25.000)
98005 pz   17.818  $ Z_min
98051 pz   20.358  $ Z_max
c Fill z=25.0 > Z_max=20.358 ✗
```

**Fix:**
```mcnp
c CORRECT: Fill z within range
91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)
c 17.818 < 19.108 < 20.358 ✓
```

---

### Best Practices for Fill Transformations

1. **Match bounding surface to fill position**
   - Cylinder center = fill (x, y)
   - Z-planes bracket fill z ± lattice extent

2. **Document fill positions**
   ```mcnp
   c Stack 1 at 120° hexagonal position (R=36 cm)
   91111 0  -97011  98005 -98051  fill=1110  (25.547 -24.553 19.108)
   ```

3. **Validate before running**
   - Check bounding surface alignment
   - Verify lattice fits within bounds
   - Plot geometry to visualize

4. **Use systematic positioning**
   - Hexagonal: θ = 0°, 60°, 120°, 180°, 240°, 300°
   - Rectangular: x = i×pitch, y = j×pitch
   - Document pattern in comments

5. **Preserve positions when scaling**
   - If scaling geometry, decide if positions scale too
   - Document whether centers move or stay fixed

---

### Quick Reference

**Basic fill transformation:**
```
fill=universe (x y z)
```

**Fill with rotation:**
```
*TRn  x y z  angles  1
fill=universe  trcl=n
```

**Validation checks:**
- [ ] Bounding surface center = fill (x,y)
- [ ] Z-planes bracket fill z
- [ ] Lattice extent < bounding surface radius
- [ ] Translation vector reasonable (not extreme values)
- [ ] Plot shows fill positioned correctly

---

**END OF FILL TRANSFORMATION SECTION**

---

**END OF TRANSFORMATION SPECIFICATIONS**
