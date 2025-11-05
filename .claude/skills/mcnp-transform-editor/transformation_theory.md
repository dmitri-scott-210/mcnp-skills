# Transformation Theory - TR Card Fundamentals

## Rotation Matrix Fundamentals

### Matrix Structure

The rotation matrix in a TR card represents the orientation of a transformed coordinate system:

```
    [a11  a12  a13]     [x'_unit]
R = [a21  a22  a23]  =  [y'_unit]
    [a31  a32  a33]     [z'_unit]
```

**Interpretation:**
- **Row 1** (a11, a12, a13): Direction cosines of the new x-axis in the old coordinate system
- **Row 2** (a21, a22, a23): Direction cosines of the new y-axis in the old coordinate system
- **Row 3** (a31, a32, a33): Direction cosines of the new z-axis in the old coordinate system

**Example:** Identity matrix (no rotation)
```
R = [1  0  0]    $ x' = x (new x-axis points along old x-axis)
    [0  1  0]    $ y' = y (new y-axis points along old y-axis)
    [0  0  1]    $ z' = z (new z-axis points along old z-axis)
```

### Required Properties

For a valid rotation matrix, the following properties **must** be satisfied:

#### 1. Orthonormality
Each row must be a unit vector (length = 1):

```
||row 1|| = √(a11² + a12² + a13²) = 1
||row 2|| = √(a21² + a22² + a23²) = 1
||row 3|| = √(a31² + a32² + a33²) = 1
```

#### 2. Orthogonality
Rows must be mutually perpendicular (dot product = 0):

```
row1 · row2 = a11·a21 + a12·a22 + a13·a23 = 0
row1 · row3 = a11·a31 + a12·a32 + a13·a33 = 0
row2 · row3 = a21·a31 + a22·a32 + a23·a33 = 0
```

#### 3. Right-Handedness
Determinant must equal +1 (or -1 for reflections):

```
det(R) = a11(a22·a33 - a23·a32) - a12(a21·a33 - a23·a31) + a13(a21·a32 - a22·a31)
```

**Values:**
- det(R) = +1: Proper rotation (preserves orientation)
- det(R) = -1: Improper rotation/reflection (reverses orientation)
- MCNP accepts both, but +1 is standard for physical rotations

### Validation Example

**Given rotation matrix:**
```
R = [0  -1   0]
    [1   0   0]
    [0   0   1]
```

**Check orthonormality:**
```
||row 1|| = √(0² + (-1)² + 0²) = 1 ✓
||row 2|| = √(1² + 0² + 0²) = 1 ✓
||row 3|| = √(0² + 0² + 1²) = 1 ✓
```

**Check orthogonality:**
```
row1·row2 = 0·1 + (-1)·0 + 0·0 = 0 ✓
row1·row3 = 0·0 + (-1)·0 + 0·1 = 0 ✓
row2·row3 = 1·0 + 0·0 + 0·1 = 0 ✓
```

**Check determinant:**
```
det = 0·(0·1 - 0·0) - (-1)·(1·1 - 0·0) + 0·(1·0 - 0·0)
    = 0 + 1 + 0 = +1 ✓
```

**Result:** This is a 90° counterclockwise rotation about the z-axis.

## Transformation Direction and Application

### Forward vs Inverse Transformation

**Forward transformation** (old coordinates → new coordinates):
```
r_new = R · (r_old - d)
```

**Inverse transformation** (new coordinates → old coordinates):
```
r_old = R^T · r_new + d
```

Where:
- `r` = position vector (x, y, z)
- `R` = rotation matrix
- `d` = displacement vector (dx, dy, dz)
- `R^T` = transpose of R

### MCNP Application Context

The direction MCNP applies transformations depends on usage:

**Surface Transformation (number in surface card):**
```
10 1 SO 5.0    $ Surface 10 uses TR1
```
- Transforms the surface definition into the original coordinate system
- Surface is moved/rotated as specified by TR card
- Particles see the surface at the transformed location

**Cell Transformation (TRCL parameter):**
```
1  1  -1.0  -10  TRCL=1  IMP:N=1    $ Cell contents transformed by TR1
```
- Transforms the universe filling the cell
- The filled universe is oriented/positioned by TR card
- Used with FILL parameter for placing universes

### Physical Interpretation

**Example:** Translation vector d = (10, 0, 0)

**Surface TR:**
```
*TR1  10 0 0
10 1 SO 5.0    $ Sphere center at (10, 0, 0)
```
The sphere is **located** at x=10 in the global coordinate system.

**Cell TRCL:**
```
*TR1  10 0 0
10  0  -100  FILL=1  TRCL=1  IMP:N=1
```
Universe 1 is **placed** into cell 10 with its origin at (10, 0, 0).

## Matrix Composition

### Composing Two Transformations

Given two transformations TR1 and TR2, create a single transformation TR3 that applies both.

**Mathematical formulation:**
```
TR3 = TR2 ∘ TR1  (apply TR1 first, then TR2)
```

**Rotation composition:**
```
R3 = R2 · R1   (matrix multiplication, note right-to-left order)
```

**Translation composition:**
```
d3 = d2 + R2 · d1
```

### Example: Rotate then Translate

**TR1:** Rotate 90° about z-axis
```
R1 = [0  -1   0]
     [1   0   0]
     [0   0   1]
d1 = (0, 0, 0)
```

**TR2:** Translate by (5, 0, 0)
```
R2 = [1   0   0]  (identity)
     [0   1   0]
     [0   0   1]
d2 = (5, 0, 0)
```

**Composition TR3 = TR2 ∘ TR1:**
```
R3 = R2 · R1 = I · R1 = [0  -1   0]
                        [1   0   0]
                        [0   0   1]

d3 = d2 + R2·d1 = (5, 0, 0) + I·(0, 0, 0) = (5, 0, 0)
```

**Result:**
```
*TR3  5 0 0  0 -1 0  1 0 0  0 0 1
```

### Example: Rotate About Point (not origin)

To rotate θ degrees about a point P = (px, py, pz):

1. **Translate P to origin:** T1 with d1 = -P
2. **Rotate about origin:** R with desired rotation
3. **Translate back:** T2 with d2 = +P

**Combined transformation:**
```
d_final = P + R·(-P) = P - R·P = P(I - R)
R_final = R
```

**For 90° rotation about point (5, 5, 0):**
```
R = [0  -1   0]
    [1   0   0]
    [0   0   1]

P = (5, 5, 0)

d = (5, 5, 0) - [0  -1   0] · [5]   = [5]   - [ 5]   = [ 0]
                [1   0   0]   [5]     [5]     [-5]     [10]
                [0   0   1]   [0]     [0]     [ 0]     [ 0]
```

Wait, let me recalculate:
```
R·P = [0  -1   0] · [5]   = [-5]
      [1   0   0]   [5]     [ 5]
      [0   0   1]   [0]     [ 0]

d = P - R·P = [5]   - [-5]   = [10]
              [5]     [ 5]     [ 0]
              [0]     [ 0]     [ 0]
```

**Result:**
```
*TR  10 0 0  0 -1 0  1 0 0  0 0 1
```

## Common Rotation Matrices

### Rotations About Principal Axes

**Rotation by θ about x-axis:**
```
Rx(θ) = [1      0         0    ]
        [0   cos(θ)   -sin(θ)  ]
        [0   sin(θ)    cos(θ)  ]
```

**Rotation by θ about y-axis:**
```
Ry(θ) = [ cos(θ)   0   sin(θ) ]
        [    0     1      0    ]
        [-sin(θ)   0   cos(θ) ]
```

**Rotation by θ about z-axis:**
```
Rz(θ) = [cos(θ)  -sin(θ)   0]
        [sin(θ)   cos(θ)   0]
        [  0         0     1]
```

**Convention:** Positive angle = counterclockwise when looking down the axis toward origin (right-hand rule)

### Specific Angle Examples

**90° rotations:**
```
Rx(90°) = [1   0   0]
          [0   0  -1]
          [0   1   0]

Ry(90°) = [ 0  0   1]
          [ 0  1   0]
          [-1  0   0]

Rz(90°) = [0  -1   0]
          [1   0   0]
          [0   0   1]
```

**180° rotations:**
```
Rx(180°) = [1   0    0]
           [0  -1    0]
           [0   0   -1]

Ry(180°) = [-1   0   0]
           [ 0   1   0]
           [ 0   0  -1]

Rz(180°) = [-1   0   0]
           [ 0  -1   0]
           [ 0   0   1]
```

## Reflection Matrices

Reflections are improper rotations (determinant = -1).

**Reflect across YZ plane (x → -x):**
```
R = [-1   0   0]
    [ 0   1   0]
    [ 0   0   1]
det(R) = -1
```

**Reflect across XZ plane (y → -y):**
```
R = [ 1   0   0]
    [ 0  -1   0]
    [ 0   0   1]
det(R) = -1
```

**Reflect across XY plane (z → -z):**
```
R = [ 1   0   0]
    [ 0   1   0]
    [ 0   0  -1]
det(R) = -1
```

**Note:** MCNP accepts reflections, but verify particle transport behaves correctly. Reflections reverse chirality.

## Transformation Inverse

Given a transformation TR with rotation R and translation d, the inverse transformation TR_inv satisfies:

```
TR_inv(TR(r)) = r
```

**Inverse parameters:**
```
R_inv = R^T  (transpose, since R is orthogonal)
d_inv = -R^T · d
```

**Example:**
```
TR1:  R = [0  -1   0]    d = (10, 0, 0)
          [1   0   0]
          [0   0   1]

TR_inv:  R_inv = R^T = [0   1   0]
                       [-1   0   0]
                       [0   0   1]

         d_inv = -R^T · d = -[0   1   0] · [10]   = -[ 0]   = [ 0]
                             [-1   0   0]   [ 0]     [-10]    [10]
                             [0   0   1]   [ 0]     [ 0]     [ 0]
```

**Result:**
```
*TR_inv  0 10 0  0 1 0  -1 0 0  0 0 1
```

**Verification:**
```
Original point: (1, 0, 0)
After TR1: R·(1,0,0) + (10,0,0) = (0,1,0) + (10,0,0) = (10,1,0)
After TR_inv: R_inv·(10,1,0) + (0,10,0) = (1,0,0) + (0,10,0)...
```

Actually let me recalculate to verify:
```
TR1(r) = R·r + d
TR_inv(r') = R^T·r' + d_inv = R^T·r' - R^T·d

TR_inv(TR1(r)) = R^T·(R·r + d) - R^T·d
                = R^T·R·r + R^T·d - R^T·d
                = I·r + 0
                = r ✓
```

## Euler Angles and Degree Input Mode

When using m=1 flag, TR card accepts Euler angles (in degrees) instead of explicit matrix.

**Format:**
```
*TRn  dx dy dz  θx θy θz  1
```

**MCNP Convention:** Rotations applied in sequence: Rx(θx) · Ry(θy) · Rz(θz)

**Example:**
```
*TR1  0 0 0  90 0 0  1    $ 90° about x only
*TR2  0 0 0  0 90 0  1    $ 90° about y only
*TR3  0 0 0  0 0 90  1    $ 90° about z only
*TR4  0 0 0  30 45 60  1  $ Combined: Rx(30°)·Ry(45°)·Rz(60°)
```

**Matrix equivalent:**
For TR4, the explicit matrix is:
```
R = Rx(30°) · Ry(45°) · Rz(60°)
```

This is calculated by multiplying the three individual rotation matrices in order.

**Note:** Degree input is convenient but less transparent than explicit matrices for debugging.
