# Transformations for Lattices (TR and TRCL Cards)

**Reference for:** mcnp-lattice-builder skill
**Source:** LATTICE-INFO-SUMMARY.md + current SKILL.md examples
**Created:** 2025-11-04 (Session 16)

---

## OVERVIEW

Transformations allow positioning and orienting filled universes in space. Essential for:
- Multiple lattices at different positions in geometry
- Rotated fuel assemblies or detector arrays
- Off-axis positioning of repeated structures
- Coordinate system alignment between different geometry levels

**Key Distinction:**
- **TR card:** Defines transformation on separate data card (reusable)
- **TRCL parameter:** Applies transformation to filled cell (inline or reference)

---

## TR CARD SYNTAX (Transformation Definition)

### General Form
```
TRn  O  Bx By Bz  v1 v2 ... vm
```

**Parameters:**
- `n` = Transformation number (integer)
- `O` = Displacement vector origin (0 or 1, see below)
- `Bx By Bz` = Displacement vector (cm)
- `v1 v2 ... vm` = Rotation matrix elements (m = 0, 3, 5, 6, or 9)

### Displacement Vector

**Meaning of O parameter:**
- `O = 1` (default): Displacement vector in **main system** (universe 0)
- `O = 0`: Displacement vector in **auxiliary system** (transformed coordinates)

**Example:**
```
TR1  1  10 0 0   $ Translate +10 cm in X (main system)
TR2  0  10 0 0   $ Translate +10 cm in X (auxiliary system, after rotation)
```

**When to use each:**
- Use O=1 for simple translations (most common)
- Use O=0 when combining rotation + translation in rotated frame

---

## ROTATION MATRIX SPECIFICATIONS

MCNP allows 5 different rotation matrix formats (shortcuts for common cases):

### Format 1: No Rotation (m = 0)
```
TRn  O  Bx By Bz
```
- Translation only, no rotation
- Identity rotation matrix applied
- **Example:** `TR1  1  5 10 0`  (translate +5 X, +10 Y)

### Format 2: Axis Rotation (m = 3)
```
TRn  O  Bx By Bz  θx θy θz
```
- Rotation about coordinate axes in order: Z first, then Y, then X
- **θx, θy, θz** in degrees
- Order matters: θz applied first, θx applied last

**Example:**
```
TR5  1  0 0 0  0 0 45   $ Rotate 45° about Z-axis
```

### Format 3: Five Elements (m = 5)
```
TRn  O  Bx By Bz  cos1 cos2 cos3 cos4 cos5
```
- Five direction cosines define rotation
- Sixth cosine calculated from orthogonality
- Rarely used (full matrix more common)

### Format 4: Six Elements (m = 6)
```
TRn  O  Bx By Bz  cos1 cos2 cos3 cos4 cos5 cos6
```
- Six direction cosines define rotation
- Three remaining cosines calculated from orthogonality
- Useful when some angles known precisely

### Format 5: Full Matrix (m = 9)
```
TRn  O  Bx By Bz  a11 a12 a13  a21 a22 a23  a31 a32 a33
```

**Rotation matrix:**
```
    | a11  a12  a13 |   | cos(α,x̂')  cos(α,ŷ')  cos(α,ẑ') |
R = | a21  a22  a23 | = | cos(β,x̂')  cos(β,ŷ')  cos(β,ẑ') |
    | a31  a32  a33 |   | cos(γ,x̂')  cos(γ,ŷ')  cos(γ,ẑ') |
```

Where:
- α, β, γ = main system axes (x, y, z)
- x̂', ŷ', ẑ' = auxiliary (transformed) system axes

**Example:** 90° rotation about Z-axis
```
TR3  1  0 0 0   0 90 90   90 0 90   90 90 0
```

Interpretation:
- Main X-axis makes angles (0°, 90°, 90°) with (x̂', ŷ', ẑ')
  → Points in +x̂' direction
- Main Y-axis makes angles (90°, 0°, 90°) with (x̂', ŷ', ẑ')
  → Points in +ŷ' direction
- Main Z-axis makes angles (90°, 90°, 0°) with (x̂', ŷ', ẑ')
  → Points in +ẑ' direction

---

## ROTATION MATRIX REQUIREMENTS

**Orthogonality constraints:**
- Each row must be unit vector: a11² + a12² + a13² = 1
- Rows must be mutually orthogonal: row1 · row2 = 0
- Similar constraints for columns

**MCNP automatically checks** rotation matrix validity. If constraints violated, error issued.

**Tip:** Use 3-angle format (m=3) when possible - easier to understand and less error-prone than full matrix.

---

## TRCL PARAMETER (Applying Transformation)

### Usage on Cell Card
```
CELL  0  -SURF  FILL=u (TRn)    $ Reference TR card n
CELL  0  -SURF  FILL=u (...)    $ Inline transformation
```

### Reference Format (TRn)
```
c Define transformation
TR10  1  15 0 0  0 0 30   $ Translate +15X, rotate 30° about Z

c Apply to filled cell
1000  0  -1000  FILL=20 (TR10)  IMP:N=1
```

**Advantage:** Reusable - same TR card referenced by multiple cells

### Inline Format
```
1000  0  -1000  FILL=20 (15 0 0  0 0 30)  IMP:N=1
```

**Advantage:** Self-contained (no separate TR card needed)
**Disadvantage:** Not reusable

---

## TRANSFORMATION ORDER

**Critical:** MCNP applies transformations in specific order:

1. **Rotation applied FIRST** (about origin)
2. **Displacement applied SECOND**

This affects how combined rotation+translation works.

### Example: Rotate Then Translate
```
c Fuel assembly at X=+20 cm, rotated 90°
TR5  1  20 0 0   0 90 0   $ Rotation about Y, then translate +20 X

c Result:
c   1. Universe 10 rotated 90° about Y-axis (at origin)
c   2. Rotated universe moved to X=+20 cm

1000  0  -1000  FILL=10 (TR5)  IMP:N=1
```

**Visualization:**
```
Step 1: Rotation at origin          Step 2: Translation
     ↑ z                                 ↑ z
     |                                   |
     |___› x                             |      [Assembly]
     ↗                                   |___________› x
    y                                    ↗
  [Assembly]                            y
  (rotated)                         (at X=+20)
```

---

## COMMON TRANSFORMATION EXAMPLES

### Example 1: Four Assemblies at Corners
```
c Assembly universe (17×17 pins)
c Place at four corners with different rotations

c Bottom-left (no rotation)
1001  0  -101  FILL=10 (1 -10 -10 0)  IMP:N=1

c Bottom-right (90° rotation)
1002  0  -102  FILL=10 (1 10 -10 0  0 0 90)  IMP:N=1

c Top-left (180° rotation)
1003  0  -103  FILL=10 (1 -10 10 0  0 0 180)  IMP:N=1

c Top-right (270° rotation)
1004  0  -104  FILL=10 (1 10 10 0  0 0 270)  IMP:N=1

c Surface definitions
101  RPP  -10  0  -10  0  0  100   $ Bottom-left position
102  RPP   0  10  -10  0  0  100   $ Bottom-right position
103  RPP  -10  0   0  10  0  100   $ Top-left position
104  RPP   0  10   0  10  0  100   $ Top-right position
```

### Example 2: Hexagonal Core with Rotated Assemblies
```
c Central assembly (no rotation)
TR0  1  0 0 0

c Six surrounding assemblies, each rotated 60° relative to neighbor
TR1  1   17.32  0  0    0 0  60   $ +X direction, 60° rotation
TR2  1    8.66 15  0    0 0 120   $ +X+Y direction, 120° rotation
TR3  1   -8.66 15  0    0 0 180   $ -X+Y direction, 180° rotation
TR4  1  -17.32  0  0    0 0 240   $ -X direction, 240° rotation
TR5  1   -8.66-15  0    0 0 300   $ -X-Y direction, 300° rotation
TR6  1    8.66-15  0    0 0   0   $ +X-Y direction, 0° rotation

c Fill cells
1000  0  -1000  FILL=20 (TR0)  IMP:N=1   $ Center
1001  0  -1001  FILL=20 (TR1)  IMP:N=1
1002  0  -1002  FILL=20 (TR2)  IMP:N=1
1003  0  -1003  FILL=20 (TR3)  IMP:N=1
1004  0  -1004  FILL=20 (TR4)  IMP:N=1
1005  0  -1005  FILL=20 (TR5)  IMP:N=1
1006  0  -1006  FILL=20 (TR6)  IMP:N=1
```

### Example 3: Detector Array Around Source
```
c Identical detector at 8 positions around cylindrical source
c Radius = 50 cm from center

TR10  1   50  0  0   $ 0° (positive X-axis)
TR11  1   35.36 35.36 0  0 0 45   $ 45°
TR12  1    0 50  0   $ 90° (positive Y-axis)
TR13  1  -35.36 35.36 0  0 0 135  $ 135°
TR14  1  -50  0  0   $ 180° (negative X-axis)
TR15  1  -35.36-35.36 0  0 0 225  $ 225°
TR16  1    0-50  0   $ 270° (negative Y-axis)
TR17  1   35.36-35.36 0  0 0 315  $ 315°

c Fill cells with detector universe
2001  0  -2001  FILL=100 (TR10)  IMP:N=1
2002  0  -2002  FILL=100 (TR11)  IMP:N=1
... (repeat for TR12-TR17)
```

### Example 4: Tilted Fuel Assembly
```
c Assembly tilted 15° from vertical (rotation about Y-axis)

TR20  1  0 0 0   15 0 90   90 90 75   90 15 0

c Breakdown:
c   Main X-axis: angles (15°, 0°, 90°) - slightly tilted from horizontal
c   Main Y-axis: angles (90°, 90°, 75°) - remains horizontal
c   Main Z-axis: angles (90°, 15°, 0°) - tilted 15° from vertical

1500  0  -1500  FILL=30 (TR20)  IMP:N=1
```

---

## TRANSFORMATIONS WITH LATTICES

### Transforming Entire Lattice

**Scenario:** Multiple lattice structures at different positions, each rotated differently

```
c Lattice universe (3×3 fuel pins)
100  0  -10 11 -12 13 -14 15  U=50  LAT=1  FILL=1

c Place three instances of lattice at different locations

c Position 1: Origin, no rotation
1001  0  -1001  FILL=50  IMP:N=1

c Position 2: X=+30 cm, no rotation
1002  0  -1002  FILL=50 (1 30 0 0)  IMP:N=1

c Position 3: X=+60 cm, rotated 45° about Z
1003  0  -1003  FILL=50 (1 60 0 0  0 0 45)  IMP:N=1

c Surface definitions (each 10×10×100 cm)
1001  RPP   0  10   0  10  0  100
1002  RPP  30  40   0  10  0  100
1003  RPP  60  70   0  10  0  100
```

### Transformation Within Lattice Element

**Scenario:** Each lattice element contains rotated universe

```
c Fuel pin universe
1  1  -10.0  -1     U=10  IMP:N=1  $ Fuel
2  2  -6.5    1 -2  U=10  IMP:N=1  $ Clad
3  3  -1.0    2     U=10  IMP:N=1  $ Coolant

c Lattice with TRCL on individual elements (NOT DIRECTLY SUPPORTED)
c Must use FILL array with different rotated universes

c Create rotated versions as separate universes
c U=10: 0° rotation
c U=11: 90° rotation (requires separate cell definitions)
c U=12: 180° rotation (requires separate cell definitions)

c Lattice with pattern
200  0  -20 21 -22 23 -24 25  U=100  LAT=1
     FILL=0:2 0:0 0:0  10 11 12  $ Alternating rotations
```

**Note:** TRCL cannot be applied to individual lattice elements directly. Must create separate universes for each rotation needed.

---

## COORDINATE SYSTEM RELATIONSHIPS

### Understanding Main vs Auxiliary Systems

**Main system:** Original coordinate system (universe 0)
**Auxiliary system:** Transformed coordinate system (after rotation)

**Particle tracking:**
- Particle position defined in main system
- When entering filled cell with TRCL, position transformed to auxiliary system
- Universe geometry defined in auxiliary system
- When exiting, transformed back to main system

### Example: Rotated Assembly Coordinates
```
c Assembly defined in its own coordinates (auxiliary system)
c   Fuel pin at (0, 0, 50) in assembly frame

c Assembly placed at X=+20 cm in main system, rotated 90° about Z
TR5  1  20 0 0   0 0 90

c Assembly fill
1000  0  -1000  FILL=10 (TR5)  IMP:N=1

c Fuel pin location in MAIN system:
c   1. Pin at (0, 0, 50) in auxiliary system
c   2. Rotate 90° about Z: (0, 0, 50) → (0, 0, 50)  [Z unchanged]
c   3. Translate +20 X: (0, 0, 50) → (20, 0, 50)
c   Result: Pin at (20, 0, 50) in main system
```

---

## DEBUGGING TRANSFORMATIONS

### Verification Steps

1. **Test translation only (no rotation)**
```
TR10  1  10 0 0   $ Simple +X translation
1000  0  -1000  FILL=20 (TR10)  IMP:N=1
```

2. **Add rotation incrementally**
```
TR11  1  10 0 0  0 0 45   $ Translation + Z-rotation
```

3. **Plot from multiple angles**
- XY plane (looking down Z-axis)
- XZ plane (looking down Y-axis)
- YZ plane (looking down X-axis)

4. **Verify particle tracking**
- Run with particle history tracking
- Confirm particles enter/exit filled cells correctly

### Common Debugging Issues

**Problem:** Filled universe appears at wrong location
- Check displacement vector signs
- Verify O parameter (0 vs 1)
- Confirm rotation applied before displacement

**Problem:** Rotation not as expected
- Verify rotation matrix orthogonality
- Check angle units (degrees, not radians)
- Test with simpler rotation (axis-aligned)

**Problem:** Particles lost at boundaries
- Plot boundaries of both main and auxiliary systems
- Check surface definitions in universe match filled cell boundary
- Verify transformation doesn't cause geometry overlap

---

## TRANSFORMATION BEST PRACTICES

1. **Use TR card references for repeated transformations**
   - Easier to modify (change once, affects all uses)
   - Less error-prone than inline duplication

2. **Start simple: Translation only, then add rotation**
   - Verify each component works before combining

3. **Use 3-angle format (m=3) when possible**
   - More intuitive than full 9-element matrix
   - Less prone to orthogonality errors

4. **Document transformation intent with comments**
```
TR5  1  20 0 0  0 0 45   $ Assembly at X=+20 cm, rotated 45° about Z
```

5. **Plot transformed geometry thoroughly**
   - Multiple viewing angles essential
   - Check universe boundaries align with filled cell

6. **Test with simple universe first**
   - Verify transformation works with simple geometry
   - Then apply to complex lattice

7. **Remember transformation order: Rotate first, translate second**
   - Affects combined rotation+translation results

---

## COORDINATE TRANSFORMATION FORMULAS

### Point Transformation

**Forward transformation (main → auxiliary):**
```
x' = a11(x - Bx) + a12(y - By) + a13(z - Bz)
y' = a21(x - Bx) + a22(y - By) + a23(z - Bz)
z' = a31(x - Bx) + a32(y - By) + a33(z - Bz)
```

**Inverse transformation (auxiliary → main):**
```
x = a11·x' + a21·y' + a31·z' + Bx
y = a12·x' + a22·y' + a32·z' + By
z = a13·x' + a23·y' + a33·z' + Bz
```

Where:
- (x, y, z) = main system coordinates
- (x', y', z') = auxiliary system coordinates
- (Bx, By, Bz) = displacement vector
- aij = rotation matrix elements

### Direction Transformation

**Unit vector transformation (main → auxiliary):**
```
u' = a11·u + a12·v + a13·w
v' = a21·u + a22·v + a23·w
w' = a31·u + a32·v + a33·w
```

Where (u, v, w) and (u', v', w') are direction cosines in main and auxiliary systems.

---

## ADVANCED: NESTED TRANSFORMATIONS

**Scenario:** Transformation within transformation (multi-level hierarchy with rotations)

```
c Level 1: Pin in assembly frame (no transformation)
1  1  -10.0  -1  U=1  IMP:N=1

c Level 2: Assembly lattice (no transformation from assembly frame)
100  0  -10 11 -12 13  U=10  LAT=1  FILL=1

c Level 3: Assembly in core frame (rotated 30° about Z)
TR20  1  0 0 0  0 0 30
1000  0  -1000  FILL=10 (TR20)  U=20  IMP:N=1

c Level 4: Core in main geometry (translated +50 X)
TR30  1  50 0 0
10000  0  -10000  FILL=20 (TR30)  IMP:N=1

c Net transformation for pin:
c   1. Rotate 30° about Z (from TR20)
c   2. Translate +50 X (from TR30)
c MCNP handles composition automatically
```

**Key Point:** MCNP tracks particle through nested transformations automatically. No manual composition required.

---

## SUMMARY

**Key Concepts:**
1. TR card defines transformation (reusable)
2. TRCL parameter applies transformation to filled cell
3. Transformation order: Rotate FIRST, translate SECOND
4. Five rotation formats: 0, 3, 5, 6, or 9 elements
5. Displacement vector origin: O=0 (auxiliary) or O=1 (main)

**Most Common Use Cases:**
- Multiple lattices at different positions
- Rotated assemblies in reactor core
- Detector arrays around source
- Coordinate system alignment

**Debugging Strategy:**
- Test translation only first
- Add rotation incrementally
- Plot from multiple angles
- Verify with simple geometry

**Best Practice:** Use TR card references (not inline) for transformations used multiple times. Easier to modify and less error-prone.

---

**References:**
- MCNP6 User Manual §5.5.3: TR Card (Coordinate Transformation)
- MCNP6 User Manual §5.2.3: TRCL Parameter
- MCNP6 Primer Chapter 9: Transformations and Universes

---

**END OF TRANSFORMATIONS_FOR_LATTICES.MD**
