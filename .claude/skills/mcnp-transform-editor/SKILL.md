---
name: mcnp-transform-editor
description: Create, modify, and troubleshoot TR transformation cards for coordinate system rotation and translation operations in MCNP geometry
version: "2.0.0"
dependencies: "mcnp-geometry-builder"
---

# MCNP Transform Editor

## Overview

The mcnp-transform-editor skill guides users in creating, modifying, and troubleshooting TR (transformation) cards in MCNP inputs. TR cards define coordinate system transformations including translations, rotations, and combined operations that enable complex geometry positioning without duplicating surface definitions.

Transformations are essential for placing multiple instances of the same component at different positions and orientations, creating symmetric geometry through reflections, and building complex assemblies from simple building blocks. Understanding TR cards allows efficient reuse of geometry definitions through the FILL and TRCL mechanisms.

This skill covers TR card syntax, rotation matrix fundamentals, common transformation patterns, composition of transformations, and systematic troubleshooting of transformation errors. It integrates closely with mcnp-geometry-builder for creating the base geometry that transformations reposition and reorient.

## When to Use This Skill

- Creating new TR transformation cards from scratch
- Modifying existing transformation definitions
- Converting between rotation matrix and degree-based specifications
- Debugging transformation errors (lost particles, overlapping cells, wrong positions)
- Combining multiple transformations through composition
- Applying transformations to surfaces (surface TR number) or cells (TRCL parameter)
- Creating mirrored or symmetric geometry components
- Placing repeated structures at irregular positions (vs lattices for regular arrays)
- Validating transformation matrix orthonormality
- Understanding transformation direction and application context

## Decision Tree

```
User needs to create/modify TR card
  |
  +---> What type of transformation?
         |
         +---> Translation Only
         |      ├─> Use 3-parameter form: *TRn dx dy dz
         |      ├─> Example: *TR1 10 0 0  (move +10 cm in x)
         |      └─> Simple and unambiguous
         |
         +---> Rotation Only (about origin)
         |      ├─> Zero translation: dx=dy=dz=0
         |      ├─> Choose specification method:
         |      |    ├─> Degree input: *TRn 0 0 0 θx θy θz 1
         |      |    └─> Matrix input: *TRn 0 0 0 a11 a12 ... a33
         |      ├─> Use scripts/rotation_matrix_generator.py for complex rotations
         |      └─> Validate with scripts/tr_matrix_validator.py
         |
         +---> Translation + Rotation
         |      ├─> Full 12-parameter form
         |      ├─> Order: rotation applied first, then translation
         |      └─> Example: *TR1 10 0 0 0 -1 0 1 0 0 0 0 1
         |
         +---> Modify Existing TR
         |      ├─> Read current TR card
         |      ├─> Identify change needed:
         |      |    ├─> Translation only → modify dx,dy,dz
         |      |    ├─> Rotation only → modify matrix elements
         |      |    └─> Both → modify all parameters
         |      ├─> Update all references (surfaces, TRCL)
         |      └─> Validate modified result
         |
         +---> Compose Transformations
         |      ├─> Define TR1 and TR2
         |      ├─> Calculate TR3 = TR2 ∘ TR1 using scripts/tr_composition.py
         |      ├─> R3 = R2·R1, d3 = d2 + R2·d1
         |      └─> Validate composed result
         |
         +---> Debug Issues
                ├─> Lost particles → Check matrix orthonormality
                ├─> Wrong position → Verify translation vector
                ├─> Inverted geometry → Check determinant (should be ±1)
                └─> See error_catalog.md for systematic troubleshooting
```

## Quick Reference

| Operation | TR Card Syntax | Notes |
|-----------|----------------|-------|
| Translate (x=10) | `*TR1  10 0 0` | 3 parameters: dx dy dz |
| Translate (y=5, z=-3) | `*TR2  0 5 -3` | Positive = positive axis direction |
| Rotate 90° about z | `*TR3  0 0 0  0 -1 0  1 0 0  0 0 1` | Matrix form (12 parameters) |
| Rotate 90° about z (degree) | `*TR3  0 0 0  0 0 90  1` | Degree form (m=1 flag) |
| Rotate 45° about z | `*TR4  0 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1` | CCW rotation |
| Combined (translate + rotate) | `*TR5  10 0 0  0 -1 0  1 0 0  0 0 1` | Rotation first, then translation |
| Reflect across YZ (x→-x) | `*TR6  0 0 0  -1 0 0  0 1 0  0 0 1` | Determinant = -1 |

**Common rotation matrices:** See transformation_theory.md

**Application methods:**
- **Surface TR:** `10 1 SO 5.0` (surface 10 uses TR1)
- **Cell TRCL:** `10  0  -100  FILL=1  TRCL=1  IMP:N=1` (universe 1 transformed by TR1)

## Use Cases

### Use Case 1: Translate Detector to Specific Position

**Scenario:** Position detector sphere at (20, 0, -10)

**Implementation:**
```
1  SO  5.0              $ Sphere at origin, R=5 cm
*TR1  20 0 -10          $ Move to (20, 0, -10)
10 1 SO 5.0             $ Surface 10 uses TR1
```

**Key Points:** Translation-only uses 3 parameters; positive values move in positive axis direction

### Use Case 2: Rotate Component 90° About Z-Axis

**Scenario:** Reorient cylindrical beam port from horizontal (+x) to vertical (+y)

**Implementation:**
```
1  RCC  0 0 0  10 0 0  2.5           $ Cylinder along +x, R=2.5, H=10
*TR1  0 0 0  0 -1 0  1 0 0  0 0 1    $ 90° CCW about z
c Alternative: *TR1  0 0 0  0 0 90  1
10 1 RCC  0 0 0  10 0 0  2.5         $ Rotated cylinder
```

**Key Points:** Zero translation (rotation about origin); degree form simpler for standard angles

### Use Case 3: Place Component with Orientation

**Scenario:** Place fuel pin at (15, 10, 0) oriented horizontally

**Implementation:**
```
c Define fuel pin universe (vertical, at origin)
1  1  -10.5  -1  U=1  IMP:N=1
1  RCC  0 0 0  0 0 10  0.5  U=1
c Combined transformation: rotate 90° y, translate
*TR1  15 10 0  0 0 1  0 1 0  -1 0 0
c Place universe with transformation
10  0  -10  FILL=1  TRCL=1  IMP:N=1
```

**Key Points:** TRCL transforms filled universe; rotation first, then translation; order matters

### Use Case 4: Create Symmetric Geometry

**Scenario:** Create four detector banks using reflections

**Implementation:**
```
*TR1  0 0 0  1 0 0  0 -1 0  0 0 1     $ Reflect y→-y
*TR2  0 0 0  -1 0 0  0 1 0  0 0 1    $ Reflect x→-x
*TR3  0 0 0  -1 0 0  0 -1 0  0 0 1   $ Reflect both
10  0  -10  FILL=1  IMP:N=1           $ Original
11  0  -11  FILL=1  TRCL=1  IMP:N=1   $ Reflected
12  0  -12  FILL=1  TRCL=2  IMP:N=1   $ Reflected
13  0  -13  FILL=1  TRCL=3  IMP:N=1   $ Reflected
```

**Key Points:** Reflections have det(R)=-1; efficient for symmetric geometry

### Use Case 5: Compose Transformations

**Scenario:** Rotate locally, translate, then rotate globally

**Implementation:**
```
*TR1  0 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1  $ Local rotation
*TR2  30 0 0                                        $ Translation
c Calculate TR3 = TR2 ∘ TR1 with scripts/tr_composition.py
*TR3  30 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1
```

**Key Points:** R3=R2·R1, d3=d2+R2·d1; use tr_composition.py; validate result

## Integration with Other Skills

**mcnp-geometry-builder:** Creates base geometry; transform-editor repositions it via TR cards and FILL+TRCL

**mcnp-input-validator:** Validates TR card correctness (orthonormality, determinant, references)

**mcnp-lattice-builder:** Lattices for regular arrays; transformations for irregular placement

**mcnp-geometry-editor:** High-level geometry operations; transform-editor handles TR details

## References

- Rotation matrix fundamentals: `transformation_theory.md`
- Rodrigues' formula, quaternions: `advanced_transformations.md`
- Common errors and fixes: `error_catalog.md`
- Complex transformation sequences: `detailed_examples.md`
- Templates: `templates/`
- Example files: `example_inputs/`
- Scripts: `scripts/tr_matrix_validator.py`, `scripts/tr_composition.py`, `scripts/rotation_matrix_generator.py`
- Documentation: `scripts/README.md`

## Best Practices

1. Use descriptive comments documenting transformation purpose and effect

2. Number systematically by grouping related transformations (TR1-9: fuel, TR10-19: control rods)

3. Validate matrices with tr_matrix_validator.py before running MCNP

4. Prefer degree input for simple single-axis rotations (clearer than explicit matrix)

5. Document matrix source if calculated externally or by script

6. Test incrementally by changing one parameter at a time

7. Use geometry plotter (`mcnp6 i=input.i ip`) to verify transformations visually

8. Avoid unnecessary identity transformations (waste memory and clarity)

9. Check determinant: det(R)=+1 for rotations, -1 for reflections

10. Keep backups by commenting out original TR before modifying
