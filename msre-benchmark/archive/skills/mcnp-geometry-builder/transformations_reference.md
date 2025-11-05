# MCNP Geometry Transformations Reference

Transformations allow geometric objects to be rotated, translated, or reflected without redefining surfaces. Essential for repeated components with varying orientations.

## Overview

**Two Types of Transformations:**
1. **Surface transformation** - Moves/rotates surface definition (specified in surface card)
2. **Cell transformation** - Moves/rotates cell contents (specified in cell TRCL parameter)

**Key Principle:** Transformations use **displacement** system (main system moves, auxiliary system stays fixed) for surface cards, and **auxiliary** system (object moves) for TRCL cell parameters.

---

## TR Card Format (Transformation Definition)

### Translation Only

**Format:** `*TRn  dx  dy  dz`

**Parameters:**
- n: Transformation number (1-999)
- dx, dy, dz: Translation vector (cm)

**Asterisk (*) is required** for all TR cards

**Example:**
```
*TR1  10 0 0                $ Translate +10 cm in x direction
```

### Translation + Rotation

**Format:** `*TRn  dx dy dz  a₁₁ a₁₂ a₁₃  a₂₁ a₂₂ a₂₃  a₃₁ a₃₂ a₃₃  [m]`

**Parameters:**
- dx, dy, dz: Translation vector
- a₁₁...a₃₃: Rotation matrix (3×3 direction cosines)
  - Row 1 (a₁₁ a₁₂ a₁₃): New x-axis direction in old coordinates
  - Row 2 (a₂₁ a₂₂ a₂₃): New y-axis direction in old coordinates
  - Row 3 (a₃₁ a₃₂ a₃₃): New z-axis direction in old coordinates
- m: Optional, if m=1 then matrix entries are in degrees (converted internally)

**Example - 90° Rotation About Z:**
```
*TR2  5 5 0  0 1 0  -1 0 0  0 0 1
c            ^new-x ^new-y ^new-z
c            (rotates x→y, y→-x)
```

**Alternative (degrees input):**
```
*TR2  5 5 0  90 0 0  0 90 0  0 0 90  1
c                                   ^m=1 for degree input
```

### Vertical Format (Recommended for Readability)

**Format:** Use `#` in columns 1-5 for card names on one line, data in columns below

```
*TR3  #  10 20 30
         0.707 0.707 0
        -0.707 0.707 0
         0 0 1
```

**Advantages:**
- Easier to read rotation matrix
- Clearer structure for complex transformations
- Reduces line length issues

---

## Surface Transformation (Surface Card)

**Format:** `j  n  mnemonic  parameters`

Where `n` is the transformation number (references *TRn card)

**Example:**
```
*TR1  10 0 0                $ Transformation: translate +10 in x

1  1  SPH  0 0 0  5         $ Sphere at (10, 0, 0) in main system
c  ^surface #
c     ^transformation TR1
```

**Effect:** Surface defined in auxiliary system (0,0,0), but appears at (10,0,0) in main system

**Negative Transformation Number:** Creates **periodic boundary**

```
1   1  PX  5.0              $ Surface at x=5
2  -1  PX  -5.0             $ Periodic boundary linked to surface 1
```

Particles crossing surface 2 reappear at surface 1 (and vice versa), creating infinite repetition effect.

**Use for periodic boundaries:** Infinite lattice approximations, crystalline structures

---

## Cell Transformation (TRCL Parameter)

### Method 1: Reference to *TRn Card

**Format:** Cell card with `TRCL=n` parameter

```
*TR5  20 0 0  0 1 0  -1 0 0  0 0 1    $ Transformation definition

1  1  -1.0  -1  U=1  TRCL=5  IMP:N=1  $ Cell uses transformation TR5
```

**Effect:** Cell contents (universe U=1) rotated and translated by TR5

### Method 2: Inline Transformation Matrix

**Format:** `TRCL=(dx dy dz  a₁₁ a₁₂ a₁₃  a₂₁ a₂₂ a₂₃  a₃₁ a₃₂ a₃₃  [m])`

**Example:**
```
1  1  -1.0  -1  U=1  TRCL=(10 0 0  1 0 0  0 1 0  0 0 1)  IMP:N=1
```

Transformation specified directly in cell card (no separate *TRn card needed)

**Advantages:**
- Self-contained (no external TR card)
- Clear which transformation applies to which cell

**Disadvantages:**
- Less reusable (can't share transformation across cells)
- Longer cell card lines

---

## Common Rotation Matrices

### 90° Rotation About Z-Axis

**x → y, y → -x, z → z**
```
*TR1  0 0 0  0 1 0  -1 0 0  0 0 1
c            ^x'   ^y'    ^z'
```

### 180° Rotation About Z-Axis

**x → -x, y → -y, z → z**
```
*TR2  0 0 0  -1 0 0  0 -1 0  0 0 1
```

### 90° Rotation About X-Axis

**x → x, y → z, z → -y**
```
*TR3  0 0 0  1 0 0  0 0 1  0 -1 0
```

### 90° Rotation About Y-Axis

**x → -z, y → y, z → x**
```
*TR4  0 0 0  0 0 1  0 1 0  -1 0 0
```

### 45° Rotation About Z-Axis

**Direction cosines: cos(45°) = sin(45°) = 0.707**
```
*TR5  0 0 0  0.707 0.707 0  -0.707 0.707 0  0 0 1
```

### Reflection About XY-Plane (Z → -Z)

**x → x, y → y, z → -z**
```
*TR6  0 0 0  1 0 0  0 1 0  0 0 -1
```

---

## Building Rotation Matrices

### Step-by-Step Process

1. **Identify new axis directions** in terms of old axes
2. **Write as column vectors** (new x', y', z' in terms of old x, y, z)
3. **Arrange as rows** in TR card (row 1 = new x', row 2 = new y', row 3 = new z')

**Example:** Rotate 90° about Z

- New x' points where old y pointed: **new x' = (0, 1, 0)**
- New y' points where old -x pointed: **new y' = (-1, 0, 0)**
- New z' unchanged: **new z' = (0, 0, 1)**

**TR card:**
```
*TR1  0 0 0  0 1 0  -1 0 0  0 0 1
c            ^new x' ^new y' ^new z'
```

### Direction Cosine Requirements

**Orthonormality:** Rotation matrices must satisfy:
- Each row is unit length: √(a₁² + a₂² + a₃²) = 1
- Rows are perpendicular: dot product = 0
- Determinant = ±1 (+ for rotation, - for rotation+reflection)

MCNP checks these automatically and reports errors if violated.

---

## Combining Translation and Rotation

**Order of Operations:**
1. Rotation applied **first** (about origin of auxiliary system)
2. Translation applied **second** (moves rotated object)

**Example:** Rotate cylinder 90° about Z, then move to (20, 30, 0)

```
*TR7  20 30 0  0 1 0  -1 0 0  0 0 1

1  7  C/Z  0 0  5           $ Cylinder along z in auxiliary system
c  ^uses TR7                $ Appears along y-axis at (20, 30, z) in main system
```

---

## Transformation with Universes and FILL

**Common Pattern:** Define component in universe, transform when filling

**Example - Rotated Fuel Assembly:**

```
c Define assembly in universe 1 (standard orientation)
1  1  -10.0  -1  U=1  IMP:N=1     $ Fuel pin in U=1
...

c Transformation for 90° rotation
*TR10  0 0 0  0 1 0  -1 0 0  0 0 1

c Place rotated assembly
100  0  -100  FILL=1  TRCL=10  IMP:N=1    $ U=1 rotated by TR10
```

**Use Cases:**
- Hexagonal core with rotated assemblies
- Detector arrays with varying orientations
- Complex geometries with repeated components at different angles

---

## Nested Transformations

Transformations can be nested through universe hierarchy:

**Example:**
```
c Pin in universe 1 (local coordinates)
1  1  -10.0  -1  U=1  IMP:N=1

c Assembly in universe 2 (uses U=1 with TR5)
10  0  -10  U=2  FILL=1  TRCL=5  IMP:N=1

c Core (uses U=2 with TR8)
100  0  -100  FILL=2  TRCL=8  IMP:N=1
```

**Effective transformation:** TR8 ∘ TR5 (TR5 applied first, then TR8)

---

## Periodic Boundaries (Infinite Lattices)

**Concept:** Particle leaving one boundary re-enters at opposite boundary

**Implementation:** Negative transformation number on paired surfaces

**Example - Infinite Slab:**
```
*TR1  10 0 0                $ Translation by 10 cm in x

1   1  PX  5.0              $ Right boundary at x=5
2  -1  PX  -5.0             $ Left boundary at x=-5 (periodic with surface 1)
```

**Effect:** 10 cm slab repeated infinitely in x direction

**Restrictions:**
- Transformations must be pure translation (no rotation)
- Only works with planar surfaces
- Particle direction unchanged when crossing boundary

**Use Cases:**
- Infinite lattice approximation (criticality studies)
- Periodic crystalline structures
- Bulk material simulation with boundary effects removed

---

## Debugging Transformations

### Common Errors

**Error: "Rotation matrix not orthonormal"**
- **Cause:** Matrix rows not unit length or not perpendicular
- **Fix:** Recalculate direction cosines, ensure orthogonality

**Error: "Particle lost after transformation"**
- **Cause:** Transformed geometry creates gap or overlap
- **Fix:** Plot geometry with transformation applied, check boundaries

**Error: "Transformation number not defined"**
- **Cause:** Cell references TRn, but *TRn card missing
- **Fix:** Add *TRn card before data block

### Validation Procedure

1. **Plot without transformation** - Verify base geometry correct
2. **Plot with transformation** - Check rotated/translated position
3. **Run test problem** - Verify particle transport behavior
4. **Check sense** - Ensure inside/outside still correct after rotation

---

## Best Practices

1. **Use *TR cards for reusable transformations** - Share across multiple cells/surfaces
2. **Use inline TRCL for one-off transformations** - Self-documenting
3. **Use vertical format for complex rotations** - Easier to read matrix
4. **Comment rotation angles** - `$ 90° about Z` for clarity
5. **Test incrementally** - Apply transformation, plot, verify
6. **Use standard rotations** - 90°, 180°, 45° easier to verify than arbitrary angles
7. **Document coordinate systems** - Sketch auxiliary vs main system relationship
8. **Check determinant** - Should be +1 (rotation) or -1 (rotation + reflection)

---

## Quick Reference Table

| Rotation | Transformation | Matrix Rows |
|----------|----------------|-------------|
| 90° about Z | x→y, y→-x | `0 1 0  -1 0 0  0 0 1` |
| 180° about Z | x→-x, y→-y | `-1 0 0  0 -1 0  0 0 1` |
| 90° about X | y→z, z→-y | `1 0 0  0 0 1  0 -1 0` |
| 90° about Y | x→-z, z→x | `0 0 1  0 1 0  -1 0 0` |
| 45° about Z | diagonal | `0.707 0.707 0  -0.707 0.707 0  0 0 1` |
| Reflect Z | z→-z | `1 0 0  0 1 0  0 0 -1` |

---

**References:**
- MCNP6 User Manual, Chapter 5.05: Geometry Data Cards (TR and TRCL)
- MCNP6 User Manual, Chapter 5.03: Surface Cards (Transformation usage)
- MCNP6 User Manual, Chapter 3: Coordinate systems and transformations
