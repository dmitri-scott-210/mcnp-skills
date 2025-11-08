---
category: B
name: mcnp-transform-editor
description: Create, modify, and troubleshoot TR transformation cards for coordinate system rotation and translation operations in MCNP geometry
activation_keywords:
  - transform card
  - edit transformation
  - TR card
  - rotation matrix
  - translation vector
  - TRCL parameter
  - coordinate transform
  - modify transformation
---

# MCNP Transform Editor Skill

## Purpose

This skill guides users in creating, modifying, and troubleshooting TR (transformation) cards in MCNP inputs. TR cards define coordinate system transformations including translations, rotations, and combined operations. This skill focuses on editing and manipulating transformation definitions, understanding rotation matrices, debugging transformation errors, and applying transformations correctly to surfaces and cells.

## When to Use This Skill

- Creating new TR transformation cards from scratch
- Modifying existing transformation definitions
- Converting between rotation matrix and degree-based specifications
- Debugging transformation errors (lost particles, overlapping cells)
- Combining multiple transformations (composition)
- Applying transformations to surfaces or cells
- Creating mirrored or repeated geometry components
- Adjusting transformation parameters iteratively
- Validating transformation matrix orthonormality
- Understanding transformation direction (forward vs inverse)
- Creating complex repeated structures with different orientations

## Prerequisites

- **mcnp-geometry-builder**: Understanding of cells and surfaces
- **mcnp-input-editor**: Basic input file editing
- Understanding of coordinate systems (Cartesian)
- Basic linear algebra (matrix multiplication, vectors)
- Knowledge of rotation concepts (Euler angles, axis-angle)

## Core Concepts

### Transformation Card Syntax

**General Format**:
```
*TRn  dx dy dz  a11 a12 a13  a21 a22 a23  a31 a32 a33  m
```

**Fields**:
- `*` (asterisk prefix): Required for TR cards
- `n`: Transformation number (1-999)
- `(dx, dy, dz)`: Translation vector (cm)
- `aij`: Rotation matrix elements (3×3 direction cosines)
- `m`: Optional flag (1 = input angles in degrees)

**Two Usage Modes**:

1. **Translation Only** (3 parameters):
```
*TR1  10 0 0                    $ Translate +10 cm in x direction
```

2. **Translation + Rotation** (12 or 13 parameters):
```
*TR2  5 5 0  0 1 0  -1 0 0  0 0 1    $ Translate + rotate
```

3. **Degree Input Mode** (13 parameters, m=1):
```
*TR3  0 0 0  90 0 0  1           $ Rotate 90° about z-axis
```

### Rotation Matrix Fundamentals

**Matrix Structure**:
```
    [a11  a12  a13]     [x'_unit]
R = [a21  a22  a23]  =  [y'_unit]
    [a31  a32  a33]     [z'_unit]
```

**Interpretation**:
- Row 1: Direction cosines of new x-axis in old system
- Row 2: Direction cosines of new y-axis in old system
- Row 3: Direction cosines of new z-axis in old system

**Properties** (must be satisfied):
1. **Orthonormality**: Each row is unit vector (length = 1)
2. **Orthogonality**: Rows are perpendicular (dot product = 0)
3. **Right-handed**: Determinant = +1

**Identity Matrix** (no rotation):
```
*TR1  0 0 0  1 0 0  0 1 0  0 0 1
```

### Application Methods

**Method 1: Surface Transformation** (in surface card):
```
j  n  type  params
10 1  SO    5.0         $ Surface 10 uses transformation 1
```

**Method 2: Cell Transformation** (TRCL parameter):
```
1  1  -1.0  -10  TRCL=1  IMP:N=1    $ Cell contents transformed by TR1
```

**Critical Difference**:
- Surface TR: Transforms surface definition (moves/rotates surface itself)
- Cell TRCL: Transforms cell contents (universe filling the cell)

### Transformation Direction

**Forward Transformation** (old → new):
```
r_new = R · (r_old - displacement)
```

**Inverse Transformation** (new → old):
```
r_old = R^T · r_new + displacement
```

**MCNP Applies**: Depends on context
- Surface cards: Transforms surface into old coordinate system
- TRCL: Transforms universe into cell coordinate system

## Decision Tree: Creating/Editing TR Cards

```
START: What transformation do you need?
  |
  +--> Translation Only
  |      ├─> Simple TR: *TRn dx dy dz
  |      └─> Example: *TR1 10 0 0
  |
  +--> Rotation Only (about origin)
  |      ├─> Identity translation: dx=dy=dz=0
  |      ├─> Choose method:
  |      |    ├─> Degree input (m=1): *TRn 0 0 0 θx θy θz 1
  |      |    └─> Matrix input: *TRn 0 0 0 a11 a12 ... a33
  |      └─> Validate orthonormality
  |
  +--> Rotation + Translation
  |      ├─> Non-zero displacement vector
  |      ├─> Full 12-parameter form
  |      └─> Example: *TR2 5 0 0 0 1 0 -1 0 0 0 0 1
  |
  +--> Modify Existing TR
  |      ├─> Read current transformation
  |      ├─> Identify change needed:
  |      |    ├─> Adjust translation only → change dx,dy,dz
  |      |    ├─> Adjust rotation only → change matrix
  |      |    └─> Both → change all parameters
  |      └─> Validate modified result
  |
  +--> Compose Multiple Transformations
  |      ├─> TR1: First transformation
  |      ├─> TR2: Second transformation
  |      ├─> Calculate composition: R_total = R2 · R1, d_total = ...
  |      └─> Create new TR with combined result
  |
  +--> Debug Transformation Issues
         ├─> Lost particles → Check matrix orthonormality
         ├─> Wrong position → Verify translation vector
         └─> Inverted geometry → Check matrix determinant
```

## Use Case 1: Translation-Only Transformation

**Scenario**: Move a component 20 cm in +x direction and 10 cm in -z direction

**Input**:
```
c --- Original geometry (at origin) ---
10 SO 5.0                           $ Sphere at origin, R=5 cm

c --- Transformation: translate x=+20, z=-10 ---
*TR1  20 0 -10

c --- Transformed surface ---
20 1 SO 5.0                         $ Same sphere, moved by TR1
```

**Result**: Sphere center now at (20, 0, -10)

**Key Points**:
- Translation-only transformations use 3 parameters only
- Positive values move in positive axis direction
- No rotation matrix needed (identity assumed)
- Simple and unambiguous

## Use Case 2: Rotation About Z-Axis (90 degrees)

**Scenario**: Rotate coordinate system 90° counterclockwise about z-axis

**Method 1 - Degree Input**:
```
*TR2  0 0 0  0 0 90  1              $ m=1: angles in degrees
```

**Method 2 - Matrix Input**:
```
c Rotation matrix for 90° about z:
c   cos(90)=-sin(90) 0     0 -1  0
c   sin(90)= cos(90) 0  =  1  0  0
c      0       0     1     0  0  1
*TR2  0 0 0  0 -1 0  1 0 0  0 0 1
```

**Verification**:
```
c Original point: (1, 0, 0)
c After rotation: (0, 1, 0) → 90° CCW rotation verified
```

**Key Points**:
- Degree input simpler for common rotations
- Matrix input more explicit and general
- Verify rotation direction (CCW positive in right-handed system)
- No translation (dx=dy=dz=0)

## Use Case 3: Combined Translation and Rotation

**Scenario**: Create a component at position (10, 5, 0) rotated 45° about z-axis

**Calculation**:
```
θ = 45° = π/4
cos(45°) = sin(45°) = 0.70711

Rotation matrix (z-axis):
[ cos(θ) -sin(θ)  0 ]   [ 0.70711 -0.70711  0 ]
[ sin(θ)  cos(θ)  0 ] = [ 0.70711  0.70711  0 ]
[   0       0     1 ]   [   0        0      1 ]

Translation: (10, 5, 0)
```

**Implementation**:
```
*TR3  10 5 0  0.70711 -0.70711 0  0.70711 0.70711 0  0 0 1
```

**Alternative (degree input)**:
```
*TR3  10 5 0  0 0 45  1
```

**Usage Example**:
```
c Define fuel pin at origin in universe 1
1  1  -10.0  -1  U=1  IMP:N=1     $ Fuel
2  0         1   U=1  IMP:N=0     $ Outside

c Place pin at (10,5,0) rotated 45°
10  0  -10  FILL=1  TRCL=3  IMP:N=1
```

**Key Points**:
- Translation applies AFTER rotation (order matters)
- Degree input automatically calculates matrix
- TRCL=3 applies TR3 to filled universe
- Verify final position with geometry plot

## Use Case 4: Mirroring Across a Plane

**Scenario**: Create mirror image of component across YZ plane (x=0)

**Reflection Matrix** (across YZ plane):
```
[-1  0  0]     $ Flip x-coordinate
[ 0  1  0]     $ Keep y-coordinate
[ 0  0  1]     $ Keep z-coordinate
```

**Implementation**:
```
*TR4  0 0 0  -1 0 0  0 1 0  0 0 1
```

**Example**:
```
c Original component
1  1  -1.0  -1  IMP:N=1             $ At positive x

c Mirrored component
10 4  SO 5.0                        $ Sphere transformed by TR4
2  1  -1.0  -10  IMP:N=1            $ Mirror appears at negative x
```

**Key Points**:
- Determinant = -1 (left-handed transformation)
- MCNP allows improper rotations (reflections)
- Useful for symmetric geometry
- Verify particle transport behaves correctly

## Use Case 5: Rotation About Arbitrary Axis

**Scenario**: Rotate 30° about axis vector (1, 1, 1) passing through origin

**Rodrigues' Rotation Formula**:
```
For axis k=(kx,ky,kz), angle θ:
R = I·cos(θ) + K·sin(θ) + kk^T·(1-cos(θ))

Where K = [  0  -kz  ky ]
          [ kz   0  -kx ]
          [-ky  kx   0  ]
```

**For k̂=(1/√3, 1/√3, 1/√3), θ=30°**:
```
After calculation (omitting details):
R ≈ [0.91068 -0.24402  0.33333]
    [0.33333  0.91068 -0.24402]
    [-0.24402  0.33333  0.91068]
```

**Implementation**:
```
*TR5  0 0 0  0.91068 -0.24402 0.33333  &
              0.33333 0.91068 -0.24402  &
              -0.24402 0.33333 0.91068
```

**Key Points**:
- Complex rotations require matrix calculation
- Use external tools (Python, MATLAB) for matrix generation
- Verify orthonormality: ||row|| = 1, row·row = 0
- Test with simple geometry before applying to full model

## Use Case 6: Modifying Existing Transformation

**Scenario**: Existing TR1 needs adjustment - change translation from (10,0,0) to (15,5,0)

**Original**:
```
*TR1  10 0 0  1 0 0  0 1 0  0 0 1
```

**Modified**:
```
*TR1  15 5 0  1 0 0  0 1 0  0 0 1
```

**Systematic Approach**:
1. Identify transformation number (TR1)
2. Locate all uses (surfaces, TRCL parameters)
3. Determine what aspect to change (translation only here)
4. Preserve unchanged parameters (rotation matrix)
5. Update TR card
6. Validate geometry still makes sense

**Key Points**:
- One TR card can be used by multiple surfaces/cells
- Changing TR affects ALL references
- Test incrementally (small changes first)
- Use geometry plotter to verify results

## Use Case 7: Composing Two Transformations

**Scenario**: Apply TR1, then TR2. Create single TR3 = TR2 ∘ TR1

**TR1** (rotate 90° about z):
```
*TR1  0 0 0  0 -1 0  1 0 0  0 0 1
R1 = [0 -1  0]
     [1  0  0]
     [0  0  1]
d1 = (0, 0, 0)
```

**TR2** (translate by (5, 0, 0)):
```
*TR2  5 0 0  1 0 0  0 1 0  0 0 1
R2 = I
d2 = (5, 0, 0)
```

**Composition** (TR3 = TR2 ∘ TR1):
```
R3 = R2 · R1 = I · R1 = [0 -1  0]
                        [1  0  0]
                        [0  0  1]

d3 = d2 + R2 · d1 = (5, 0, 0) + 0 = (5, 0, 0)
```

**Result**:
```
*TR3  5 0 0  0 -1 0  1 0 0  0 0 1
```

**Key Points**:
- Composition order matters: TR3 = TR2(TR1(x))
- Matrix multiplication: R3 = R2 · R1 (right-to-left)
- Translation: d3 = d2 + R2·d1
- Useful for building complex transformations incrementally

## Use Case 8: Converting Degree Input to Matrix Form

**Scenario**: TR card uses degree input, need explicit matrix for debugging

**Degree Input**:
```
*TR6  10 0 0  30 45 60  1
```

**Interpretation**:
- Translation: (10, 0, 0)
- Rotation: 30° about x, then 45° about y, then 60° about z (Euler angles)
- m=1: Angles in degrees

**Matrix Calculation** (Rx·Ry·Rz):
```
Rz(60°) = [0.5 -0.866 0]
          [0.866 0.5  0]
          [0     0    1]

Ry(45°) = [0.707  0  0.707]
          [0      1  0    ]
          [-0.707 0  0.707]

Rx(30°) = [1  0      0     ]
          [0  0.866  -0.5  ]
          [0  0.5    0.866 ]

R = Rx·Ry·Rz (matrix multiplication)
```

**Explicit Form** (after calculation):
```
*TR6  10 0 0  0.354 -0.866 0.354  0.927 0.25 -0.280  -0.126 0.433 0.893
```

**Key Points**:
- Degree input uses Euler angle convention
- Order: rotations applied in x→y→z sequence
- Explicit matrix allows manual verification
- Use when debugging unexpected orientations

## Common Errors and Troubleshooting

### Error 1: Non-Orthogonal Rotation Matrix

**Symptom**: MCNP warning or fatal error about transformation matrix

**Cause**: Matrix rows not orthonormal (not unit length or not perpendicular)

**Example (Bad)**:
```
*TR1  0 0 0  1 0 0  0 2 0  0 0 1    $ Row 2 has length 2 (not 1)
```

**Fix**:
```
c Normalize row 2: (0,2,0) → (0,1,0)
*TR1  0 0 0  1 0 0  0 1 0  0 0 1
```

**Validation**:
```
Row 1: √(1² + 0² + 0²) = 1 ✓
Row 2: √(0² + 1² + 0²) = 1 ✓
Row 3: √(0² + 0² + 1²) = 1 ✓
Row1·Row2 = 1·0 + 0·1 + 0·0 = 0 ✓
```

### Error 2: Wrong Transformation Direction

**Symptom**: Geometry appears inverted or in wrong location

**Cause**: Confusion between forward/inverse transformation

**Bad**:
```
c Want to move sphere from (0,0,0) to (10,0,0)
c Using: *TR1  -10 0 0  $ WRONG!
10 1 SO 5.0
```

**Good**:
```
c Correct translation vector
*TR1  10 0 0
10 1 SO 5.0
```

**Key Point**: For surface transformations, TR vector points FROM origin TO new location

### Error 3: Mixing Surface TR and Cell TRCL

**Symptom**: Geometry in unexpected location or double transformation

**Bad**:
```
*TR1  10 0 0
10 1 SO 5.0                $ Surface transformed
1  1  -1.0  -10  TRCL=1  IMP:N=1  $ Cell ALSO transformed (double!)
```

**Good** (choose one):
```
c Option 1: Transform surface only
*TR1  10 0 0
10 1 SO 5.0
1  1  -1.0  -10  IMP:N=1

c Option 2: Transform cell only
10 SO 5.0
1  1  -1.0  -10  TRCL=1  IMP:N=1
```

**Key Point**: Don't apply transformation twice to same geometry

### Error 4: Transformation Number Conflicts

**Symptom**: Unexpected geometry changes or MCNP warnings

**Cause**: Reusing transformation number with different definition

**Bad**:
```
*TR1  10 0 0                $ TR1 defined
...
*TR1  0 10 0                $ TR1 redefined! (only second is used)
```

**Good**:
```
*TR1  10 0 0
*TR2  0 10 0                $ Use different number
```

**Key Point**: Each transformation needs unique number (1-999)

### Error 5: Lost Particles Due to Transformation

**Symptom**: Fatal error "lost particle" after adding transformation

**Cause**: Transformation creates geometry overlap or void

**Debug Process**:
1. Comment out transformation, verify original geometry valid
2. Apply transformation to single component, test
3. Check transformed geometry with plotter
4. Verify transformed surfaces don't overlap existing geometry
5. Check transformation matrix determinant (should be ≈ ±1)

**Example Fix**:
```
c Check transformation validity
*TR1  10 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1
c Verify determinant:
c det = 0.707·(0.707·1 - 0·0) - (-0.707)·(0.707·1 - 0·0) + 0
c     = 0.707·0.707 + 0.707·0.707 = 1.0 ✓
```

### Error 6: Incorrect Euler Angle Interpretation

**Symptom**: Geometry rotated incorrectly with degree input mode

**Cause**: Misunderstanding Euler angle convention (order matters)

**MCNP Convention**: Angles are rotations about x, then y, then z axes

**Bad Assumption**:
```
c Want 90° about z only
*TR1  0 0 0  0 0 90  1         $ WRONG if expecting different convention
```

**Correct for 90° about z only**:
```
*TR1  0 0 0  0 0 90  1         $ x=0, y=0, z=90
```

**For 90° about x only**:
```
*TR2  0 0 0  90 0 0  1         $ x=90, y=0, z=0
```

**Key Point**: Test single-axis rotations first to understand convention

## Integration with Other Skills

### 1. **mcnp-geometry-editor**

The geometry-editor provides high-level operations (scaling, rotation) while transform-editor focuses on TR card details.

**Workflow**:
- geometry-editor: "I need to rotate this assembly 45°"
- transform-editor: "Create TR card with proper rotation matrix"

**Example**:
```
c geometry-editor identifies need to rotate cell 10 by 45° about z
c transform-editor creates transformation:
*TR5  0 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1
c geometry-editor applies via TRCL:
10  0  -100  FILL=5  TRCL=5  IMP:N=1
```

### 2. **mcnp-input-editor**

Input-editor handles file-level edits, transform-editor focuses on transformation logic.

**Workflow**:
```
1. input-editor: Locate all TR cards in file
2. transform-editor: Modify specific TR definitions
3. input-editor: Apply changes to file
```

### 3. **mcnp-geometry-builder**

Geometry-builder creates initial geometry, transform-editor enables reuse via transformations.

**Pattern**:
```
1. geometry-builder: Create base component (universe)
2. transform-editor: Define transformations for multiple placements
3. Use FILL+TRCL to instantiate at different positions/orientations
```

### 4. **mcnp-lattice-builder**

Lattice-builder uses regular arrays, transform-editor enables irregular placement.

**When to use each**:
- Lattice: Regular rectangular/hexagonal array
- Transform: Irregular positions, different orientations

**Example** (mix both):
```
c Lattice for fuel pins
100  0  -10  LAT=1  FILL=...

c Irregular control rods via transformations
*TR1  5.5 5.5 0  0 0 90  1
*TR2  -7 3 0  0 0 45  1
```

### 5. **mcnp-input-validator**

Validator checks transformation correctness.

**Checks performed**:
- Matrix orthonormality
- Determinant ≈ ±1
- Translation vector reasonable
- No duplicate transformation numbers
- All referenced transformations defined

### Workflow:
```
1. transform-editor: Create/modify TR cards
2. input-validator: Check correctness
3. transform-editor: Fix any issues
4. geometry-checker: Verify resulting geometry
```

## Validation Checklist

Before finalizing TR cards:

- [ ] Transformation number unique (1-999, no duplicates)
- [ ] Asterisk prefix present (*TRn)
- [ ] Translation vector physically reasonable (not 1e6 cm)
- [ ] Rotation matrix orthonormal (if provided)
  - [ ] Each row has length 1
  - [ ] Rows mutually perpendicular
  - [ ] Right-handed (determinant = +1) or reflection (determinant = -1)
- [ ] If degree input (m=1), angles reasonable (-360 to 360)
- [ ] All surfaces/cells referencing TRn exist
- [ ] Transformation applied correctly:
  - [ ] Surface TR (in surface card) OR
  - [ ] Cell TRCL (in cell card) but not both
- [ ] Geometry plotted and verified correct position/orientation
- [ ] No lost particles when running MCNP
- [ ] Transformation composition (if any) calculated correctly

## Advanced Topics

### 1. Quaternion Representation

For complex rotation sequences, quaternions avoid gimbal lock.

**Quaternion** (unit): q = [w, x, y, z] where w² + x² + y² + z² = 1

**Convert to Matrix**:
```
R = [1-2(y²+z²)  2(xy-wz)    2(xz+wy)  ]
    [2(xy+wz)    1-2(x²+z²)  2(yz-wx)  ]
    [2(xz-wy)    2(yz+wx)    1-2(x²+y²)]
```

**Use Case**: Animation, multi-step rotations, optimization

### 2. Transformation Inverse

Given TR card, create inverse transformation (undo operation).

**Formula**:
```
TR: r' = R·r + d
TR_inv: r = R^T·(r' - d) = R^T·r' - R^T·d

Inverse parameters:
R_inv = R^T (transpose)
d_inv = -R^T · d
```

**Example**:
```
c Original
*TR1  10 0 0  0 -1 0  1 0 0  0 0 1

c Inverse (transpose rotation, adjust translation)
c R^T = [0  1  0]
c       [-1 0  0]
c       [0  0  1]
c d_inv = -R^T · (10,0,0) = -(0,10,0) = (0,-10,0)
*TR2  0 -10 0  0 1 0  -1 0 0  0 0 1
```

### 3. Transformation Sequences

Build complex transformations from simple steps.

**Example** (rotate about point P, not origin):
1. Translate P → origin: T1 = -P
2. Rotate about origin: R
3. Translate origin → P: T2 = +P
4. Combined: TR = T2 · R · T1

**Implementation**:
```
c Rotate 90° about point (5, 5, 0)
c Step 1: Translate to origin
c Step 2: Rotate
c Step 3: Translate back
c Combined result:
*TR3  5 5 0  0 -1 0  1 0 0  0 0 1
c (calculation omitted for brevity)
```

### 4. Coordinate System Conventions

MCNP uses right-handed Cartesian system.

**Verify Right-Handed**:
```
x × y = z
(1,0,0) × (0,1,0) = (0,0,1) ✓
```

**Determinant Check**:
```python
import numpy as np
R = np.array([[a11, a12, a13],
              [a21, a22, a23],
              [a31, a32, a33]])
det = np.linalg.det(R)
# Should be +1 (proper rotation) or -1 (reflection)
```

### 5. Optimization: Reducing Transformation Count

**Problem**: Many similar transformations clutter input

**Solution**: Parameterize with LIKE BUT

```
c Define base transformation
*TR1  10 0 0  1 0 0  0 1 0  0 0 1

c Use LIKE BUT for variations (NOT DIRECTLY SUPPORTED for TR cards)
c Instead: Calculate variations programmatically or use fill arrays
```

**Better Approach**: Use lattice with fill array for regular patterns

## Quick Reference: Common Transformations

| Operation | TR Card Syntax |
|-----------|----------------|
| Translate (x=10) | `*TR1  10 0 0` |
| Translate (y=5, z=-3) | `*TR2  0 5 -3` |
| Rotate 90° about z | `*TR3  0 0 0  0 -1 0  1 0 0  0 0 1` |
| Rotate 180° about z | `*TR4  0 0 0  -1 0 0  0 -1 0  0 0 1` |
| Rotate 90° about x | `*TR5  0 0 0  1 0 0  0 0 -1  0 1 0` |
| Rotate 90° about y | `*TR6  0 0 0  0 0 1  0 1 0  -1 0 0` |
| Reflect across YZ (x→-x) | `*TR7  0 0 0  -1 0 0  0 1 0  0 0 1` |
| Reflect across XZ (y→-y) | `*TR8  0 0 0  1 0 0  0 -1 0  0 0 1` |
| Identity (no change) | `*TR9  0 0 0  1 0 0  0 1 0  0 0 1` |

## Quick Reference: Matrix Validation

**Python Script for Validation**:
```python
import numpy as np

def validate_tr_matrix(a11, a12, a13, a21, a22, a23, a31, a32, a33):
    R = np.array([[a11, a12, a13],
                  [a21, a22, a23],
                  [a31, a32, a33]])

    # Check row norms
    row_norms = [np.linalg.norm(R[i,:]) for i in range(3)]
    print(f"Row norms: {row_norms} (should be ~1.0)")

    # Check orthogonality
    dot01 = np.dot(R[0,:], R[1,:])
    dot02 = np.dot(R[0,:], R[2,:])
    dot12 = np.dot(R[1,:], R[2,:])
    print(f"Dot products: {dot01:.6f}, {dot02:.6f}, {dot12:.6f} (should be ~0)")

    # Check determinant
    det = np.linalg.det(R)
    print(f"Determinant: {det:.6f} (should be ±1)")

    return all(abs(n - 1.0) < 1e-6 for n in row_norms) and \
           abs(dot01) < 1e-6 and abs(dot02) < 1e-6 and abs(dot12) < 1e-6 and \
           abs(abs(det) - 1.0) < 1e-6

# Example usage:
validate_tr_matrix(0, -1, 0, 1, 0, 0, 0, 0, 1)  # 90° rotation about z
```

## Best Practices

1. **Use Descriptive Comments**: Document what each transformation does
   ```
   *TR1  10 0 0                    $ Translate detector to position A
   *TR2  0 0 0  0 -1 0  1 0 0  0 0 1  $ Rotate source 90° CCW
   ```

2. **Number Systematically**: Group related transformations
   ```
   *TR1-*TR9: Fuel assembly positions
   *TR10-*TR19: Control rod positions
   *TR20-*TR29: Detector positions
   ```

3. **Validate Before Using**: Test transformation on simple geometry first
   ```
   c Test TR1 on simple sphere before applying to complex assembly
   999  1  SO  1.0            $ Test sphere
   ```

4. **Prefer Degree Input for Simple Rotations**:
   ```
   *TR1  0 0 0  0 0 90  1     $ Clear: 90° about z
   (vs)
   *TR1  0 0 0  0 -1 0  1 0 0  0 0 1  $ Less clear
   ```

5. **Document Matrix Source**: If calculated externally, note method
   ```
   c TR2: Rodrigues formula for 30° about (1,1,1), calculated via Python
   *TR2  0 0 0  0.91068 -0.24402 0.33333  ...
   ```

6. **Check Determinant**: Ensure proper orientation (det = +1 typically)
   ```python
   # In validation script:
   assert abs(det - 1.0) < 1e-6, "Improper rotation (det ≠ +1)"
   ```

7. **Avoid Unnecessary Transformations**: Identity transformations waste memory
   ```
   c Bad: *TR1  0 0 0  1 0 0  0 1 0  0 0 1  (identity, useless)
   c Good: Just omit transformation if not needed
   ```

8. **Use Transformation Composition Carefully**: Verify order
   ```
   c TR3 = TR2 ∘ TR1 means "apply TR1 first, then TR2"
   c Matrix: R3 = R2 · R1 (note order!)
   ```

9. **Test Incrementally**: Change one parameter at a time
   ```
   c Original: *TR1  10 0 0
   c Test translation: *TR1  15 0 0  (x only)
   c Then: *TR1  15 5 0  (add y)
   ```

10. **Keep Backup**: Save original before modifying
    ```
    c Original transformation (backup)
    c *TR1  10 0 0  1 0 0  0 1 0  0 0 1
    c Modified:
    *TR1  12 3 0  1 0 0  0 1 0  0 0 1
    ```

11. **Programmatic Transformation Editing**:
    - For automated transformation generation and matrix calculations, see: `mcnp_transform_editor.py`
    - Useful for complex rotation sequences, coordinate transformations, and parametric studies

## References

- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md` (Section 6: Geometry Data Cards, lines 576-611)
- **Related Skills**:
  - mcnp-geometry-editor (high-level transformations)
  - mcnp-geometry-builder (base geometry creation)
  - mcnp-input-editor (file editing)
  - mcnp-input-validator (TR card validation)
  - mcnp-lattice-builder (regular arrays vs transformations)
- **User Manual**: Chapter 5.5 (Geometry Data Cards - Transformation Cards)
- **External Tools**:
  - Python numpy for matrix calculations
  - MATLAB for rotation matrix generation
  - Online quaternion calculators

---

**End of MCNP Transform Editor Skill**
