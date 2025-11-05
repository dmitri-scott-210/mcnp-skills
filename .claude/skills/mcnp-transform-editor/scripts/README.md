# TR Card Scripts - Usage Guide

This directory contains Python tools for creating, validating, and manipulating MCNP transformation (TR) cards.

## Requirements

- Python 3.6+
- NumPy

Install dependencies:
```bash
pip install numpy
```

---

## Scripts Overview

### 1. tr_matrix_validator.py

**Purpose:** Validate rotation matrices for MCNP TR cards

**Usage:**
```bash
# Interactive mode (prompts for matrix)
python tr_matrix_validator.py

# Command-line mode (provide 9 matrix elements)
python tr_matrix_validator.py 0 -1 0 1 0 0 0 0 1
```

**Checks performed:**
- Row norms (should be 1.0)
- Orthogonality (dot products should be 0.0)
- Determinant (should be ±1.0)

**Example:**
```bash
$ python tr_matrix_validator.py 0 -1 0 1 0 0 0 0 1

============================================================
TR MATRIX VALIDATION
============================================================

Input Matrix:
  [ 0.000000  -1.000000   0.000000]
  [ 1.000000   0.000000   0.000000]
  [ 0.000000   0.000000   1.000000]

CHECK 1: Orthonormality (Row Norms)
------------------------------------------------------------
  Row 1 norm: 1.0000000000 (should be 1.0) ... ✓ PASS
  Row 2 norm: 1.0000000000 (should be 1.0) ... ✓ PASS
  Row 3 norm: 1.0000000000 (should be 1.0) ... ✓ PASS

CHECK 2: Orthogonality (Row Dot Products)
------------------------------------------------------------
  Row 1 · Row 2: 0.0000000000 (should be 0.0) ... ✓ PASS
  Row 1 · Row 3: 0.0000000000 (should be 0.0) ... ✓ PASS
  Row 2 · Row 3: 0.0000000000 (should be 0.0) ... ✓ PASS

CHECK 3: Right-Handedness (Determinant)
------------------------------------------------------------
  Determinant: 1.0000000000 (should be ±1.0) ... ✓ PASS
  Type: proper rotation

============================================================
RESULT: ✓ Matrix is VALID for MCNP TR card
============================================================
```

**Exit codes:**
- 0: Matrix is valid
- 1: Matrix is invalid

---

### 2. tr_composition.py

**Purpose:** Compose two TR transformations into a single equivalent transformation

**Usage:**
```bash
# Interactive mode (prompts for TR1 and TR2)
python tr_composition.py

# Example demonstration
python tr_composition.py --example
```

**Mathematical operation:** TR3 = TR2 ∘ TR1 (TR1 applied first, then TR2)

**Example:**
```bash
$ python tr_composition.py

============================================================
TR COMPOSITION CALCULATOR
============================================================

Compose two transformations: TR3 = TR2 ∘ TR1
(TR1 is applied first, then TR2)

Enter TR1 parameters:
  Format: dx dy dz [a11 a12 a13 a21 a22 a23 a31 a32 a33]
  (3 values for translation only, 12 for translation + rotation)
  TR1: 0 0 0 0 -1 0 1 0 0 0 0 1

Enter TR2 parameters:
  Format: dx dy dz [a11 a12 a13 a21 a22 a23 a31 a32 a33]
  TR2: 5 0 0

============================================================
TR COMPOSITION: TR3 = TR2 ∘ TR1
============================================================

TR1 (applied first):
  Translation: ( 0.000000,  0.000000,  0.000000)
  Rotation:
    [ 0.000000  -1.000000   0.000000]
    [ 1.000000   0.000000   0.000000]
    [ 0.000000   0.000000   1.000000]

TR2 (applied second):
  Translation: ( 5.000000,  0.000000,  0.000000)
  Rotation:
    [ 1.000000   0.000000   0.000000]
    [ 0.000000   1.000000   0.000000]
    [ 0.000000   0.000000   1.000000]

TR3 (composition):
  Translation: ( 5.000000,  0.000000,  0.000000)
  Rotation:
    [ 0.000000  -1.000000   0.000000]
    [ 1.000000   0.000000   0.000000]
    [ 0.000000   0.000000   1.000000]

MCNP TR Card:
  *TR3  5.000000 0.000000 0.000000  &
        0.000000 -1.000000 0.000000  &
        1.000000 0.000000 0.000000  &
        0.000000 0.000000 1.000000

Validation:
  Determinant: 1.0000000000 (should be ±1.0)
  Row norms: [1.0000000000, 1.0000000000, 1.0000000000]
============================================================
```

---

### 3. rotation_matrix_generator.py

**Purpose:** Generate rotation matrices from various rotation representations

**Usage:**
```bash
# Euler angles (x-y-z convention)
python rotation_matrix_generator.py --euler 30 45 60 --degrees

# Axis-angle representation (Rodrigues' formula)
python rotation_matrix_generator.py --axis 1 1 1 --angle 30 --degrees

# Single-axis rotations
python rotation_matrix_generator.py --rotate-x 90 --degrees
python rotation_matrix_generator.py --rotate-y 45 --degrees
python rotation_matrix_generator.py --rotate-z 30 --degrees
```

**Examples:**

**Example 1: 90° rotation about z-axis**
```bash
$ python rotation_matrix_generator.py --rotate-z 90 --degrees

============================================================
Rotation about Z-axis: 90.0 degrees
============================================================

Matrix:
  [ 0.000000  -1.000000   0.000000]
  [ 1.000000   0.000000   0.000000]
  [ 0.000000   0.000000   1.000000]

MCNP TR Card (translation at origin):
  *TRn  0 0 0  &
        0.000000 -1.000000 0.000000  &
        1.000000 0.000000 0.000000  &
        0.000000 0.000000 1.000000

Validation:
  Row norms: [1.0000000000, 1.0000000000, 1.0000000000]
  Dot products: [0.0000000000, 0.0000000000, 0.0000000000]
  Determinant: 1.0000000000
  Status: ✓ VALID rotation matrix
============================================================
```

**Example 2: Arbitrary axis rotation**
```bash
$ python rotation_matrix_generator.py --axis 1 1 1 --angle 30 --degrees

============================================================
Axis-Angle: k=(1.0, 1.0, 1.0) θ=30.0 degrees
============================================================

Matrix:
  [ 0.910684  -0.244017   0.333333]
  [ 0.333333   0.910684  -0.244017]
  [-0.244017   0.333333   0.910684]

MCNP TR Card (translation at origin):
  *TRn  0 0 0  &
        0.910684 -0.244017 0.333333  &
        0.333333 0.910684 -0.244017  &
        -0.244017 0.333333 0.910684

Validation:
  Row norms: [1.0000000000, 1.0000000000, 1.0000000000]
  Dot products: [0.0000000000, 0.0000000000, 0.0000000000]
  Determinant: 1.0000000000
  Status: ✓ VALID rotation matrix
============================================================
```

**Example 3: Euler angles**
```bash
$ python rotation_matrix_generator.py --euler 30 45 60 --degrees

============================================================
Euler Angles: θx=30.0 θy=45.0 θz=60.0 degrees
============================================================

Matrix:
  [ 0.353553  -0.866025   0.353553]
  [ 0.926777   0.250000  -0.279508]
  [-0.126826   0.433013   0.892539]

MCNP TR Card (translation at origin):
  *TRn  0 0 0  &
        0.353553 -0.866025 0.353553  &
        0.926777 0.250000 -0.279508  &
        -0.126826 0.433013 0.892539
...
```

---

## Common Workflows

### Workflow 1: Create and Validate TR Card

```bash
# Step 1: Generate rotation matrix
python rotation_matrix_generator.py --rotate-z 45 --degrees > output.txt

# Step 2: Extract matrix elements and validate
python tr_matrix_validator.py 0.707 -0.707 0 0.707 0.707 0 0 0 1
```

### Workflow 2: Compose Multiple Transformations

```bash
# Step 1: Define TR1 and TR2 in a text file (tr_params.txt)
# TR1: 10 0 0
# TR2: 0 0 0 0 -1 0 1 0 0 0 0 1

# Step 2: Run composition script
python tr_composition.py
# (Enter parameters when prompted)

# Step 3: Validate composed result
python tr_matrix_validator.py <resulting matrix elements>
```

### Workflow 3: Complex Rotation

```bash
# Generate rotation about arbitrary axis (1, 2, 3) by 60°
python rotation_matrix_generator.py --axis 1 2 3 --angle 60 --degrees

# Copy MCNP TR card from output to your input file
```

---

## Angle Conventions

### Degrees vs Radians
- Use `--degrees` flag for degree input
- Default is radians if flag not specified

### Euler Angles (x-y-z convention)
- MCNP applies rotations in order: Rx(θx) · Ry(θy) · Rz(θz)
- First rotate about x, then about rotated y, then about twice-rotated z

### Rotation Direction
- Positive angle = counterclockwise rotation
- Following right-hand rule (thumb along axis, fingers curl in rotation direction)

---

## Troubleshooting

### Common Errors

**Error: "Invalid matrix elements"**
- Ensure 9 values provided to tr_matrix_validator.py
- Check for typos in numbers

**Error: "Matrix is INVALID"**
- Row norms not equal to 1.0 → Normalize rows
- Dot products not zero → Recalculate from rotation definition
- Determinant not ±1 → Matrix is not a valid rotation

**Unexpected rotation results**
- Verify rotation direction (right-hand rule)
- Check Euler angle order (MCNP uses x-y-z)
- Test with simple case (90° single-axis) first

---

## Integration with MCNP

### Using Generated TR Cards

1. Generate rotation matrix with `rotation_matrix_generator.py`
2. Validate with `tr_matrix_validator.py`
3. Copy TR card from output to MCNP input file:
   ```
   c Transformation for detector rotation
   *TR1  0 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1  $ 45° CCW about z
   ```

4. Apply to surface or cell:
   ```
   10 1 SO 5.0        $ Surface with TR1
   OR
   1  1  -1.0  -10  TRCL=1  IMP:N=1    $ Cell with TR1
   ```

### Verification in MCNP

After adding TR card:
1. Run geometry plotter: `mcnp6 i=input.i ip`
2. Visually verify component position/orientation
3. Run void check: verify no overlaps or voids
4. Test with particle tracking

---

## Additional Resources

- **transformation_theory.md** - Mathematical background on rotation matrices
- **advanced_transformations.md** - Rodrigues' formula, quaternions, complex operations
- **error_catalog.md** - Common TR card errors and fixes

---

## Support

For issues or questions:
1. Check error_catalog.md for common problems
2. Validate matrices with tr_matrix_validator.py
3. Review transformation_theory.md for mathematical details
