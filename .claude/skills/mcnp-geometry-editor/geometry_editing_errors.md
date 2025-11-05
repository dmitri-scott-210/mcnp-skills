# MCNP Geometry Editing Errors and Troubleshooting

**Purpose:** Comprehensive catalog of common errors when editing geometry

---

## Error 1: Lost Particles After Scaling

**Symptom:**
```
fatal error.  lost particle.
  xyz=  5.123  0.000  0.000
```

**Cause:** Scaling created gaps or overlaps between previously touching surfaces

**Example:**
```
BEFORE SCALING:
1  SO  10.0  $ Inner sphere R=10
2  SO  10.0  $ Outer sphere R=10 (WRONG - should be >10)

AFTER 1.5× SCALING:
1  SO  15.0  $ Inner
2  SO  15.0  $ Outer (still equal, now overlap!)
```

**Why Wrong:**
- Surfaces meant to touch but both scaled identically
- Creates either gap (particles escape) or overlap (geometry error)

**Solution:**
```
Maintain surface relationships:
Inner sphere: R=10 → R=15 (1.5×)
Outer sphere: R=15 → R=22.5 (1.5×, maintains gap)
```

**Prevention:**
1. Identify surface relationships before scaling
2. Scale all related dimensions consistently
3. Verify gaps/overlaps maintained with geometry plot
4. Test with short run (NPS 100)

---

## Error 2: Rotation Matrix Not Orthonormal

**Symptom:**
```
bad trouble in subroutine trnsrc
 transformation matrix rows are not orthogonal.
```

**Cause:** Manually entered rotation matrix violates orthonormality constraints

**Example (WRONG):**
```
*TR1  0 0 0  1.0 0.5 0.0  0.0 1.0 0.0  0.0 0.0 1.0
              ^row not unit length!
```

**Requirements:**
```
For rotation matrix R:
1. Rows must be perpendicular: R_i · R_j = 0 (i≠j)
2. Rows must be unit length: |R_i| = 1
3. Determinant must be +1: det(R) = +1
```

**Check:**
```python
import numpy as np
R = np.array([[1.0, 0.5, 0.0],
              [0.0, 1.0, 0.0],
              [0.0, 0.0, 1.0]])

# Row lengths
print("|Row1| =", np.linalg.norm(R[0]))  # 1.118 ≠ 1 (ERROR)
print("|Row2| =", np.linalg.norm(R[1]))  # 1.000 ✓
print("|Row3| =", np.linalg.norm(R[2]))  # 1.000 ✓
```

**Solution:**
Use MCNP degrees mode (m=1) to avoid manual matrix:
```
*TR1  0 0 0  30 45 0  1  $ MCNP calculates correct matrix
```

**Prevention:**
1. Always use m=1 with Euler angles unless expert
2. If manual matrix needed, validate with script
3. Use numpy or MATLAB to compute correct matrix

---

## Error 3: Cell Volume Changed Unexpectedly

**Symptom:**
- Tally results differ significantly after "minor" geometry edit
- Source intensity seems wrong
- Flux values don't match expectations

**Cause:** VOL parameter not updated after scaling

**Example:**
```
BEFORE:
1  1  -1.0  -1  VOL=4188.79  IMP:N=1  $ Sphere R=10

AFTER 1.2× SCALE:
Surface: R=12 (correct)
Cell: VOL=4188.79  ← WRONG! Still old volume
```

**Correct Volume:**
```
V_sphere = 4/3 π R³
V_original = 4/3 π (10)³ = 4188.79 cm³
V_scaled = 4/3 π (12)³ = 7238.23 cm³
Factor: 1.2³ = 1.728 ✓
```

**Why It Matters:**
- Source strength proportional to volume
- Tally normalization uses volume
- Reaction rate calculations depend on volume

**Solution:**
```
Update VOL parameter:
1  1  -1.0  -1  VOL=7238.23  IMP:N=1
```

**OR Remove VOL (MCNP calculates):**
```
1  1  -1.0  -1  IMP:N=1  $ No VOL, MCNP computes
```

**Prevention:**
1. After ANY scaling: Recalculate volumes (×f³ for uniform)
2. OR remove VOL cards entirely (safer but slower)
3. Document volume scaling in comments

---

## Error 4: Lattice Indices Out of Bounds

**Symptom:**
```
 bad trouble in subroutine set_nblat of mcnpn
   index out of fill-array range
```

**Cause:** FILL array size doesn't match LAT dimensions

**Example (WRONG):**
```
100  0  geom  LAT=1  FILL=-1:1  -1:1  0:0  &
                           ^3×3×1 = 9 elements needed
              1 1 1  &
              1 2 1  &  $ Only 6 elements provided!
```

**Solution:**
```
100  0  geom  LAT=1  FILL=-1:1  -1:1  0:0  &
              1 1 1  &
              1 2 1  &
              1 1 1  $ 9 elements (3×3×1) ✓
```

**Calculation:**
```
nx = imax - imin + 1 = 1-(-1)+1 = 3
ny = jmax - jmin + 1 = 1-(-1)+1 = 3
nz = kmax - kmin + 1 = 0-0+1 = 1
Total = nx × ny × nz = 3×3×1 = 9
```

**Prevention:**
1. Calculate required elements: (i2-i1+1)×(j2-j1+1)×(k2-k1+1)
2. Count FILL array elements manually
3. Use script to generate FILL array for complex lattices
4. Verify with lattice plot before running

---

## Error 5: Geometry Overlaps After Transformation

**Symptom:**
```
warning.  3 cells overlap at position  x=5.0 y=0.0 z=0.0
         cell 1 density= -1.00E+00
         cell 2 density= -2.30E+00
```

**Cause:** TR card transformation moved cell into occupied space

**Example:**
```
ORIGINAL:
1  1  -1.0  -10  IMP:N=1  $ Cell at x=0 to 10
2  2  -2.3  -20  IMP:N=1  $ Cell at x=10 to 20 (touching)

AFTER TR1 (shift cell 1 by +5):
*TR1  5 0 0
1  1  -1.0  -10  TRCL=1  IMP:N=1  $ Now at x=5 to 15
2  2  -2.3  -20  IMP:N=1  $ Still at x=10 to 20
$ OVERLAP from x=10 to x=15!
```

**Detection:**
1. Use MCNP plot with color-by-cell
2. Overlapping regions show multiple colors (flashing)
3. Run with random point sampling

**Solution:**
```
Option 1: Adjust TR to avoid overlap
*TR1  2 0 0  $ Shift only +2 cm (now x=2 to 12, no overlap)

Option 2: Move both cells proportionally
*TR1  5 0 0  $ Cell 1
*TR2  10 0 0  $ Cell 2 (maintain gap)

Option 3: Use complement operator
1  1  -1.0  -10 #2  TRCL=1  IMP:N=1  $ Exclude cell 2
```

**Prevention:**
1. Visualize with plot BEFORE running
2. Check bounding boxes of transformed components
3. Test with very short run (NPS 10) to catch errors early
4. Keep transformation log showing component positions

---

## Error 6: Surface Sense Reversed After Transformation

**Symptom:**
- Cell becomes "inside-out"
- Particles escape unexpectedly
- Geometry appears inverted in plot

**Cause:** Transformation with negative determinant (reflection) reverses surface sense

**Example:**
```
*TR1  0 0 0  -1 0 0  0 1 0  0 0 1  $ Reflection across yz-plane
              ^negative determinant

ORIGINAL:
1  1  -1.0  -10  IMP:N=1  $ -10 = inside surface 10

AFTER TR:
1  1  -1.0  -10  TRCL=1  IMP:N=1
$ -10 now means OUTSIDE surface 10! (sense reversed)
```

**Check Determinant:**
```python
import numpy as np
R = np.array([[-1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]])
det = np.linalg.det(R)
print(f"Determinant: {det}")  # -1.0 (LEFT-HANDED!)
```

**Solution:**
```
AVOID reflections (det=-1)
Use explicit mirroring instead:

Original sphere: 10  S  5 0 0  3.0
Mirrored: 20  S  -5 0 0  3.0  $ Explicit new surface
```

**Prevention:**
1. Check det(R) = +1 before using TR
2. Avoid reflection transformations
3. Use explicit geometry copies for mirrors
4. Test with geometry plot (check inside/outside)

---

## Error 7: Inconsistent Scaling of Dependent Dimensions

**Symptom:**
- Physics results unrealistic after scaling
- Reaction rates wrong
- Shielding effectiveness changed unexpectedly

**Cause:** Scaled some dimensions but not related parameters

**Example:**
```
ORIGINAL:
- Shield thickness: 10 cm
- Mean free path in material: ~5 cm
- Effectiveness: ~86% attenuation

SCALED 2× (thickness to 20 cm):
- Shield thickness: 20 cm ✓
- BUT: Density unchanged → mean free path still ~5 cm
- Effectiveness: ~98% (correct for thicker shield)

If ALSO scaled density 2× (error):
- Density: 2× original
- Mean free path: ~2.5 cm (smaller)
- Effectiveness: ~99.99% (unrealistic for this geometry)
```

**Physical Dependencies:**
- Scale length → Volume scales by f³
- Scale length → Mass scales by f³ (if density constant)
- Scale length + density → Mass scales by f⁴ (usually wrong)

**Solution:**
1. Identify physical relationships before scaling
2. Typically: Scale dimensions only, keep densities constant
3. Exception: If modeling requires density adjustment, document why

**Prevention:**
1. Think about physics, not just geometry
2. Document assumptions about material properties
3. Verify results against expected scaling laws

---

## Error 8: Edited Wrong Surface (Off-by-One Error)

**Symptom:**
- Unexpected geometry changes
- Different component modified than intended

**Cause:** Surface/cell numbering error during editing

**Example:**
```
INTENDED: Scale surface 100 (outer boundary)
ACTUALLY EDITED: Surface 10 (fuel region)

Result: Fuel region scaled, boundary unchanged (ERROR)
```

**Prevention:**
1. Use descriptive comments:
   ```
   100  RPP  -50 50  -50 50  -50 50  c OUTER BOUNDARY
   10   SO   5.0                      c FUEL SPHERE
   ```

2. Visual confirmation:
   - Plot geometry
   - Identify surface by color/position
   - Verify it's the intended surface

3. Edit in systematic order:
   - List surfaces to edit
   - Check off each one
   - Plot after each major change

4. Use search functionality:
   - Search for surface number
   - Verify it's in correct geometric region

---

## Error 9: Forgot to Update Bounding Surface After Lattice Expansion

**Symptom:**
```
warning.  particle leaving via bounding surface is being reflected.
```

**Cause:** Expanded lattice but didn't enlarge bounding surface

**Example:**
```
ORIGINAL:
LAT cell: 3×3 lattice, pitch 1.26 cm
Bounding: RPP  -1.89 1.89  ...  (3×1.26 = 3.78, ±1.89)

AFTER EXPANSION TO 5×5:
LAT cell: 5×5 lattice, pitch 1.26 cm
Bounding: RPP  -1.89 1.89  ...  (WRONG! Too small)
```

**Correct:**
```
Bounding: RPP  -3.15 3.15  ...  (5×1.26 = 6.30, ±3.15)
```

**Solution:**
1. Calculate new lattice dimensions: N × pitch
2. Update bounding surface to enclose expanded lattice
3. Add small buffer (~0.1 cm) for numerical safety

**Prevention:**
1. Always check bounding surface after lattice changes
2. Use formula: bound = (N × pitch) / 2 + buffer
3. Verify with lattice plot (all elements visible)

---

## Error 10: Transformation Applied to Wrong Object

**Symptom:**
- Wrong component moved/rotated
- Intended component unchanged

**Cause:** TR number referenced incorrectly

**Example:**
```
*TR1  10 0 0  $ Intended for component A
*TR2  0 10 0  $ Intended for component B

INTENDED:
10  1  SO  5.0  $ Component A uses TR1

ACCIDENTALLY:
10  2  SO  5.0  $ Component A uses TR2 (WRONG TR!)
```

**Solution:**
1. Verify TR number in surface/cell card
2. Use consistent naming/numbering scheme
3. Comment TR cards with purpose:
   ```
   *TR1  10 0 0  $ Component A translation
   *TR2  0 10 0  $ Component B translation
   ```

**Prevention:**
1. Document which TR applies to which component
2. Use TR numbers systematically (e.g., TR1-10 for component A)
3. Plot before running to verify transformations correct

---

## Debugging Workflow

### Step 1: Identify Error Type
```
1. Read error message carefully
2. Note error location (xyz, cell, surface)
3. Classify error:
   - Geometry (lost particles, overlaps)
   - Transformation (bad matrix)
   - Lattice (indices, FILL array)
   - Volume (physics results wrong)
```

### Step 2: Isolate Problem
```
1. Plot geometry:
   - Multiple views
   - Color-by-cell
   - Zoom to error location

2. Simplify:
   - Comment out recent changes
   - Run without transformations
   - Test with simpler geometry

3. Compare:
   - Before vs after edit
   - Expected vs actual geometry
```

### Step 3: Fix and Verify
```
1. Apply fix from appropriate error pattern above

2. Verify fix:
   - Plot shows correct geometry
   - No new errors introduced
   - Test run (NPS 100-1000) clean

3. Document:
   - What was wrong
   - How it was fixed
   - Date of fix
```

---

## Prevention Best Practices

### Before Editing
1. ✅ Create backup of input file
2. ✅ Document current geometry state
3. ✅ Plan changes systematically
4. ✅ Review mcnp-geometry-builder concepts

### During Editing
1. ✅ Change one thing at a time
2. ✅ Verify each change with plot
3. ✅ Test incrementally (short runs)
4. ✅ Keep transformation log

### After Editing
1. ✅ Complete validation checklist
2. ✅ Full geometry plot review
3. ✅ Test run with statistics check
4. ✅ Document all changes

---

## Quick Error Reference

| Error Message | Most Likely Cause | Quick Fix |
|---------------|-------------------|-----------|
| "lost particle" | Geometry gap or overlap | Plot, find gap, adjust surfaces |
| "matrix not orthogonal" | Bad TR card | Use m=1 with Euler angles |
| "fill-array range" | FILL size mismatch | Count elements, match to LAT dims |
| "cells overlap" | Transformation collision | Adjust TR or use # operator |
| "surface sense" | det(R)=-1 reflection | Avoid reflections, use explicit geometry |

---

**END OF GEOMETRY EDITING ERRORS**
