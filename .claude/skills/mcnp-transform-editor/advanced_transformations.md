# Advanced Transformation Techniques

## Rodrigues' Rotation Formula

For rotation by angle θ about an arbitrary axis k̂ = (kx, ky, kz) passing through the origin:

### Formula

```
R = I·cos(θ) + K·sin(θ) + k̂k̂^T·(1-cos(θ))
```

Where:
- **I** = 3×3 identity matrix
- **k̂** = unit vector along rotation axis (must have ||k̂|| = 1)
- **k̂k̂^T** = outer product of k̂ with itself
- **K** = skew-symmetric cross-product matrix:

```
K = [  0   -kz   ky ]
    [ kz    0   -kx ]
    [-ky   kx    0  ]
```

### Example: 30° Rotation About (1,1,1) Axis

**Step 1:** Normalize axis vector
```
k = (1, 1, 1)
||k|| = √(1² + 1² + 1²) = √3
k̂ = (1/√3, 1/√3, 1/√3)
```

**Step 2:** Calculate components
```
θ = 30° = π/6 rad
cos(30°) = 0.866025
sin(30°) = 0.5
1 - cos(30°) = 0.133975

k̂k̂^T = [1/3  1/3  1/3]
        [1/3  1/3  1/3]
        [1/3  1/3  1/3]

K = [   0    -1/√3   1/√3 ]
    [ 1/√3     0    -1/√3 ]
    [-1/√3   1/√3     0   ]
```

**Step 3:** Apply formula
```
R = [1 0 0]·0.866 + [   0    -0.577   0.577]·0.5 + [0.333  0.333  0.333]·0.134
    [0 1 0]         [ 0.577     0    -0.577]       [0.333  0.333  0.333]
    [0 0 1]         [-0.577   0.577     0  ]       [0.333  0.333  0.333]

R ≈ [0.91068  -0.24402   0.33333]
    [0.33333   0.91068  -0.24402]
    [-0.24402   0.33333   0.91068]
```

**TR card:**
```
*TR1  0 0 0  0.91068 -0.24402 0.33333  &
              0.33333 0.91068 -0.24402  &
              -0.24402 0.33333 0.91068
```

### Use Cases

Rodrigues' formula is useful when:
- Rotating about arbitrary axis (not x, y, or z)
- Converting axis-angle representation to matrix
- Interpolating between orientations (SLERP)
- Generating rotation matrices programmatically

**Recommendation:** Use Python script `rotation_matrix_generator.py` for calculations.

## Quaternion Representation

Quaternions provide an alternative rotation representation that avoids gimbal lock and simplifies composition.

### Quaternion Basics

A unit quaternion: **q = [w, x, y, z]** where w² + x² + y² + z² = 1

**Relationship to axis-angle:**
```
Given rotation by θ about unit axis k̂ = (kx, ky, kz):

q = [cos(θ/2), kx·sin(θ/2), ky·sin(θ/2), kz·sin(θ/2)]
```

### Conversion to Rotation Matrix

Given quaternion q = [w, x, y, z]:

```
R = [1-2(y²+z²)   2(xy-wz)     2(xz+wy)  ]
    [2(xy+wz)     1-2(x²+z²)   2(yz-wx)  ]
    [2(xz-wy)     2(yz+wx)     1-2(x²+y²)]
```

### Example: 90° Rotation About Z-Axis

**Quaternion:**
```
θ = 90° = π/2
k̂ = (0, 0, 1)

q = [cos(45°), 0, 0, sin(45°)]
  = [0.707, 0, 0, 0.707]
```

**Convert to matrix:**
```
w=0.707, x=0, y=0, z=0.707

R = [1-2(0+0.5)      2(0-0.5)        2(0+0)     ]
    [2(0+0.5)        1-2(0+0.5)      2(0-0)     ]
    [2(0-0)          2(0+0)          1-2(0+0)   ]

R = [0  -1   0]
    [1   0   0]
    [0   0   1]
```

**TR card:**
```
*TR1  0 0 0  0 -1 0  1 0 0  0 0 1
```

### Quaternion Composition

Composing rotations q1 and q2:
```
q3 = q2 ⊗ q1  (quaternion multiplication)
```

Where ⊗ is defined by Hamilton product (see scripts/rotation_matrix_generator.py for implementation).

### Advantages of Quaternions

1. **No gimbal lock** - Euler angles can have singularities
2. **Smooth interpolation** - SLERP (spherical linear interpolation)
3. **Compact** - 4 parameters vs 9 for matrix (with 6 constraints)
4. **Fast composition** - Quaternion multiplication faster than matrix

### When to Use Quaternions

- Animating transformations (smooth interpolation needed)
- Orientation optimization (parameter space is simpler)
- Composing many rotations (numerical stability)
- Camera/viewport manipulation in geometry visualization

**Note:** MCNP doesn't directly accept quaternions - must convert to rotation matrix for TR card.

## Transformation Sequences

Complex transformations can be built from simple operations applied sequentially.

### Pattern 1: Rotate About Point (Not Origin)

**Goal:** Rotate by angle θ about point P = (px, py, pz)

**Sequence:**
1. Translate P to origin: d1 = -P
2. Rotate about origin: R
3. Translate origin back to P: d2 = +P

**Combined result:**
```
R_final = R
d_final = P + R·(-P)
```

**Example:** 90° about z-axis through point (5, 5, 0)
```
R = Rz(90°) = [0  -1   0]
              [1   0   0]
              [0   0   1]

P = (5, 5, 0)

d = P + R·(-P) = [5] + [0  -1   0]·[-5]   = [5] + [-5]   = [10]
                 [5]   [1   0   0] [-5]     [5]   [ 5]     [ 0]
                 [0]   [0   0   1] [ 0]     [0]   [ 0]     [ 0]
```

Actually let me recalculate correctly:
```
d = P - R·P = [5] - [0  -1   0]·[5]   = [5] - [-5]   = [10]
              [5]   [1   0   0] [5]     [5]   [ 5]     [ 0]
              [0]   [0   0   1] [0]     [0]   [ 0]     [ 0]
```

**TR card:**
```
*TR1  10 0 0  0 -1 0  1 0 0  0 0 1
```

### Pattern 2: Align Coordinate Systems

**Goal:** Transform from coordinate system A to coordinate system B

**Given:**
- Basis vectors of system B in system A coordinates: x'_B, y'_B, z'_B

**Construction:**
```
R = [x'_B]^T     (rows are basis vectors)
    [y'_B]
    [z'_B]
```

**Example:** System B has axes rotated 45° in XY plane
```
x'_B = (cos(45°), sin(45°), 0) = (0.707, 0.707, 0)
y'_B = (-sin(45°), cos(45°), 0) = (-0.707, 0.707, 0)
z'_B = (0, 0, 1)

R = [ 0.707   0.707  0]
    [-0.707   0.707  0]
    [   0       0    1]
```

**TR card:**
```
*TR1  0 0 0  0.707 0.707 0  -0.707 0.707 0  0 0 1
```

### Pattern 3: Mirror Then Rotate

**Goal:** Create symmetric component via reflection + rotation

**Sequence:**
1. Reflect across plane: R_reflect (det = -1)
2. Rotate to final orientation: R_rotate

**Combined:**
```
R_final = R_rotate · R_reflect
det(R_final) = det(R_rotate) · det(R_reflect) = (+1)·(-1) = -1
```

**Example:** Reflect across YZ, then rotate 30° about z
```
R_reflect = [-1   0   0]
            [ 0   1   0]
            [ 0   0   1]

R_rotate = [cos(30°)  -sin(30°)   0]   = [0.866  -0.5    0]
           [sin(30°)   cos(30°)   0]     [0.5     0.866  0]
           [   0          0       1]     [0       0      1]

R_final = [0.866  -0.5    0] · [-1   0   0]   = [-0.866   -0.5     0]
          [0.5     0.866  0]   [ 0   1   0]     [-0.5      0.866   0]
          [0       0      1]   [ 0   0   1]     [ 0        0       1]
```

**TR card:**
```
*TR1  0 0 0  -0.866 -0.5 0  -0.5 0.866 0  0 0 1
```

## Coordinate System Conventions

### Right-Handed vs Left-Handed

MCNP uses **right-handed Cartesian** coordinate system:

**Right-hand rule:**
- Point fingers along +x
- Curl toward +y
- Thumb points along +z

**Verification:** x × y = z
```
(1,0,0) × (0,1,0) = (0,0,1) ✓
```

**Determinant check:**
- Right-handed: det(R) = +1 (proper rotation)
- Left-handed: det(R) = -1 (improper rotation/reflection)

### Active vs Passive Transformations

**Active transformation:** Object moves, coordinate system stays fixed
- "Rotate the component 90°"
- This is what TR cards do when applied to surfaces

**Passive transformation:** Coordinate system changes, object stays fixed
- "View the component from a rotated perspective"
- This is what TR cards do when applied to universes (TRCL)

**Mathematical equivalence:**
Active rotation by R = Passive rotation by R^T

## Optimization Techniques

### Reducing Transformation Count

**Problem:** Many transformations with slight variations clutter input file

**Solution 1:** Parameterize with scripts
- Generate TR cards programmatically
- Use Python to calculate systematic variations
- Include generated TR block in input file

**Example:** 12 fuel assemblies in a ring
```python
import numpy as np

for i in range(12):
    angle = i * 30  # degrees
    theta = np.radians(angle)
    R = 10  # ring radius

    dx = R * np.cos(theta)
    dy = R * np.sin(theta)

    print(f"*TR{i+1}  {dx:.3f} {dy:.3f} 0  $ Assembly {i+1}")
```

**Solution 2:** Use lattice for regular patterns
- TR cards for irregular/unique positions only
- LAT+FILL for regular rectangular/hexagonal arrays
- See mcnp-lattice-builder skill for lattice approach

### Numerical Precision Considerations

**Problem:** Accumulated rounding errors in matrix composition

**Best practices:**
1. Use double precision (15+ digits) in calculations
2. Re-orthonormalize after composing many transformations
3. Validate final matrix with scripts/tr_matrix_validator.py

**Gram-Schmidt orthonormalization:**
```python
import numpy as np

def orthonormalize(R):
    """Re-orthonormalize a nearly-orthogonal matrix"""
    # Gram-Schmidt process
    v1 = R[0,:]
    v1 = v1 / np.linalg.norm(v1)

    v2 = R[1,:] - np.dot(v1, R[1,:]) * v1
    v2 = v2 / np.linalg.norm(v2)

    v3 = R[2,:] - np.dot(v1, R[2,:]) * v1 - np.dot(v2, R[2,:]) * v2
    v3 = v3 / np.linalg.norm(v3)

    return np.array([v1, v2, v3])
```

## External Tools and Resources

### Python Libraries

**NumPy** - Matrix operations
```python
import numpy as np
R = np.array([[0, -1, 0],
              [1,  0, 0],
              [0,  0, 1]])
det = np.linalg.det(R)  # Calculate determinant
R_T = R.T  # Transpose
```

**SciPy** - Rotation utilities
```python
from scipy.spatial.transform import Rotation as R

# Create from Euler angles
r = R.from_euler('xyz', [30, 45, 60], degrees=True)
matrix = r.as_matrix()

# Create from quaternion
q = [0.707, 0, 0, 0.707]  # [w, x, y, z]
r = R.from_quat([q[1], q[2], q[3], q[0]])  # Note: scipy uses [x,y,z,w]
matrix = r.as_matrix()
```

### MATLAB

```matlab
% Rotation matrix from Euler angles
R = eul2rotm([30 45 60]*pi/180);

% Quaternion to rotation matrix
q = [0.707, 0, 0, 0.707];
R = quat2rotm(q);

% Verify orthonormality
is_valid = all(abs(R*R' - eye(3)) < 1e-10, 'all');
```

### Online Calculators

- **Quaternion Calculator:** https://www.andre-gaschler.com/rotationconverter/
- **Rotation Converter:** https://www.euclideanspace.com/maths/geometry/rotations/conversions/
- **Matrix Determinant:** https://matrix.reshish.com/determinant.php

**Note:** Always validate externally-generated matrices with tr_matrix_validator.py before use.
