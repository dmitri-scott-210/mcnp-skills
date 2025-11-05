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

**END OF TRANSFORMATION SPECIFICATIONS**
