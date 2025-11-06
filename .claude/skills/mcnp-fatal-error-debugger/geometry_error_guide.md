# MCNP Geometry Error Debugging Guide

**Purpose:** Comprehensive guide to diagnosing and fixing geometry errors (lost particles, overlaps, gaps).

**Companion to:** mcnp-fatal-error-debugger SKILL.md

---

## Overview

Geometry errors occur when particles cannot determine their location during transport. These manifest as "lost particle" or "bad trouble in subroutine track" messages. This guide provides systematic procedures for identifying and correcting geometry issues.

---

## Geometry Error Types

### Lost Particle - Overlap

**Symptom:**
```
bad trouble in subroutine track of mcrun
  source particle no.       1234

  particle lost at point:
    x =   5.12345
    y =   3.67890
    z =   0.00000

  in cell    2
```

**Cause:** Two or more cells claim the same physical space

**How Overlap Occurs:**

**Example 1: Complete Enclosure**
```
Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Sphere R=10
2  2  -2.3  -2  IMP:N=1                $ Sphere R=12 (encloses cell 1!)

Surface Cards
1  SO  10                              $ Sphere radius 10
2  SO  12                              $ Sphere radius 12
```

**Problem:** Cell 2 defined as "inside surface 2" (-2), which includes all of cell 1.

**Fix:**
```
Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Inner sphere R=10
2  2  -2.3  1 -2  IMP:N=1              $ Shell: outside 1, inside 2
```

**Example 2: Incorrect Boolean Logic**
```
Cell Cards
1  1  -1.0  -1 -2  IMP:N=1             $ Box (-5 < x < 5, -10 < y < 10)
2  2  -2.3  -3 -4  IMP:N=1             $ Box (-3 < x < 3, -8 < y < 8)

Surface Cards
1  PX  5
2  PX  -5
3  PX  3
4  PX  -3
```

**Problem:** Cell 2 region completely inside cell 1 (overlap in region -3 < x < 3).

**Fix:**
```
Cell Cards
1  1  -1.0  -1 -2 (3:4)  IMP:N=1      $ Box 1 minus box 2
2  2  -2.3  -3 -4  IMP:N=1            $ Box 2 (no overlap now)
```

### Lost Particle - Gap

**Symptom:**
```
bad trouble in subroutine track of mcrun
  particle lost at point:
    x =  10.00001
    y =   0.00000
    z =   0.00000

  no cell found at position   10.00001   0.00000   0.00000
```

**Key Indicator:** "no cell found" (vs "in cell X" for overlap)

**Cause:** Space exists but no cell defined there

**How Gaps Occur:**

**Example 1: Incomplete Coverage**
```
Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Inner sphere R=10
2  2  -2.3  2  IMP:N=1                 $ Outer region, outside R=12
999  0  1 -2  IMP:N=0                  $ Graveyard

Surface Cards
1  SO  10                              $ Sphere R=10
2  SO  12                              $ Sphere R=12
```

**Problem:** No cell defined for region between R=10 and R=12 (gap from 10 < r < 12).

**Fix Option 1** (Add cell for gap):
```
Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Inner sphere R=10
2  0        1 -2  IMP:N=1              $ Void gap R=10 to R=12
3  2  -2.3  2  IMP:N=1                 $ Outer region, outside R=12
999  0  -2  IMP:N=0                    $ Graveyard (outside 2)
```

**Fix Option 2** (Extend cell 1):
```
Cell Cards
1  1  -1.0  -2  IMP:N=1                $ Extended to R=12 (no gap)
2  2  -2.3  2  IMP:N=1                 $ Outer region
999  0  -2  IMP:N=0                    $ Graveyard
```

**Example 2: Complex Intersection**
```
Cell Cards
1  1  -1.0  -1 2  IMP:N=1              $ Cylinder, outside plane
2  2  -2.3  -3 -2  IMP:N=1             $ Sphere, inside plane
999  0  1 3  IMP:N=0                   $ Graveyard

Surface Cards
1  CZ  5                               $ Cylinder Z-axis, R=5
2  PZ  0                               $ XY plane
3  SO  10                              $ Sphere R=10
```

**Problem:** Gap exists in region where:
- Inside cylinder (-1) AND inside plane (-2) → not covered by any cell

**Fix:**
```
Cell Cards
1  1  -1.0  -1 2  IMP:N=1              $ Cylinder, z > 0
2  2  -2.3  -3 -2  IMP:N=1             $ Sphere, z < 0
3  3  -1.2  -1 -2 3  IMP:N=1           $ Gap region: inside cyl, z<0, outside sphere
999  0  1 3  IMP:N=0                   $ Graveyard
```

### Lost Particle - Wrong Surface Sense

**Symptom:**
```
particle lost at   10.00000   0.00000   0.00000
on surface     1
event log shows crossing surface 1 repeatedly
```

**Cause:** Cell definition uses incorrect surface sense (+ vs -)

**How It Occurs:**

**Example: Shell with Wrong Senses**
```
Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Inner sphere
2  2  -2.3  -1 -2  IMP:N=1             $ WRONG: both -1 and -2 (inside both)

Surface Cards
1  SO  10
2  SO  20
```

**Problem:** Cell 2 defined as "inside surface 1 AND inside surface 2" → same as cell 1!

**Fix:**
```
Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Inner sphere (r < 10)
2  2  -2.3  1 -2  IMP:N=1              $ Shell (10 < r < 20): outside 1, inside 2
```

**Rule:** For shells, inner surface positive (+), outer surface negative (-).

### Dashed Lines in Plots

**Symptom:** Geometry plot shows dashed lines on surfaces

**Meaning:** Not exactly one cell on each side of surface

**Possible Causes:**
1. Overlap (>1 cell claims space on one side)
2. Gap (0 cells on one side)
3. Legitimate (plot plane coincident, DXTRAN spheres)

**Diagnosis:**
```
# Plot geometry
mcnp6 IP

# In plotter:
# - Locate dashed line
# - Click on cells adjacent to dashed surface
# - Verify exactly one cell on each side
# - If not, diagnose overlap or gap
```

---

## Event Log Analysis

### Event Log Structure

```
event log of particle        1234
  surface     cell    mat     nps
                1      1        1234    ← Born in cell 1
      10        2      2        1234    ← Crossed surf 10 → cell 2
      15        3      3        1234    ← Crossed surf 15 → cell 3
      15        ?      ?        1234    ← Crossed surf 15 again → LOST
```

### Interpretation

**Each Line:**
- `surface`: Surface just crossed
- `cell`: Cell entered after crossing
- `mat`: Material of that cell
- `nps`: Source particle number

**First Line** (blank surface):
- Particle born in cell 1
- Shows initial cell and material

**Subsequent Lines:**
- Show particle trajectory through geometry
- Each cross into new cell

**Last Line with "?":**
- Particle lost after crossing this surface
- Could not determine destination cell
- Indicates overlap or gap at that location

### Using Event Log for Diagnosis

**Step 1:** Identify problematic surface
```
  15        ?      ?        1234    ← Lost crossing surface 15
```

**Step 2:** Look at previous cell
```
  15        3      3        1234    ← Was in cell 3 before crossing 15
```

**Step 3:** Plot at lost location
```
# Use lost particle coordinates from output:
IP  5.12 3.69 0

# Examine surfaces involved:
# - Surface 15 (where lost)
# - Cell 3 (previous cell)
# - Cells adjacent to surface 15
```

**Step 4:** Identify geometry issue
- Overlap: Cell 3 and another cell both claim space beyond surface 15
- Gap: No cell defined beyond surface 15
- Wrong sense: Cell 3 defined incorrectly relative to surface 15

---

## Geometry Plotting for Debugging

### Plot at Lost Location

**When particle lost, MCNP reports coordinates:**
```
particle lost at   5.12345  3.67890  0.00000
```

**Create plot centered at that location:**
```
c Add to input file or use IP mode:
IP  5.12 3.69 0                        $ Origin at lost location
BA  10                                 $ Extent ±10 cm
PX  1 0 0                              $ View along +X axis
```

**What to Look For:**
1. Dashed lines (geometry errors)
2. Cell labels on both sides of surfaces
3. Overlapping cell regions
4. Undefined regions (gaps)

### Interactive Plotting Workflow

```bash
# Start MCNP in interactive plotter mode
mcnp6 IP inp=problem.i

# In plotter:
# 1. Move origin to lost particle location
#    - Click "Origin" button
#    - Enter coordinates: 5.12 3.69 0
#
# 2. Adjust view
#    - Rotate to see problematic region clearly
#    - Use "Color by Cell" to distinguish cells
#    - Use "Show Surface Numbers" to identify surfaces
#
# 3. Zoom in
#    - Click "Extent" to zoom to region around lost particle
#    - Look for dashed lines in that area
#
# 4. Click on cells
#    - Click near lost location to see cell definitions
#    - Verify geometry makes sense
#
# 5. Examine surfaces
#    - Click "Show Surfaces" to highlight
#    - Verify surface senses (+ vs -)
```

### Multi-View Plotting

**View from three orthogonal directions:**
```
c View 1: XY plane (looking down Z)
IP  5.12 3.69 0
PX  0 0 1

c View 2: XZ plane (looking down Y)
IP  5.12 3.69 0
PX  0 1 0

c View 3: YZ plane (looking down X)
IP  5.12 3.69 0
PX  1 0 0
```

**Why:** 3D geometry errors may only be visible from certain angles.

---

## VOID Card Test

### Purpose

Comprehensive test to flood geometry with particles and detect any overlaps or gaps.

### Procedure

**Step 1:** Save original input
```bash
cp original.i original_backup.i
```

**Step 2:** Create test input `test_geom.i`

**Modify cell cards:**
```
c Original cell definitions (keep as-is)
1  1  -1.0  -1  IMP:N=1
2  2  -2.3  1 -2  IMP:N=1
[... more cells ...]

c Add two new cells:
998  0  -998 999  IMP:N=1              $ Region between system and flood sphere
999  0  998  IMP:N=0                   $ Graveyard outside flood sphere
```

**Modify surface cards:**
```
c Original surfaces (keep as-is)
1  SO  10
2  SO  20
[... more surfaces ...]

c Add flood surfaces:
998  SO  1000                          $ Large sphere enclosing entire system
999  SO  100                           $ Approximate outer boundary of system
```

**Modify data cards:**
```
VOID                                   $ Override all materials → void
MODE  N
IMP:N  1  1  1  1  ...  1  1  0       $ All cells IMP=1 except graveyard (last=0)
SDEF  SUR=998  NRM=-1                  $ Inward-directed surface source
NPS  10000                             $ Short test run
```

**Step 3:** Run test
```bash
mcnp6 inp=test_geom.i outp=test_geom.o
```

**Step 4:** Examine output

**If particles get lost:**
- Geometry error exists
- Check event log for location
- Plot at lost particle coordinates
- Fix geometry

**If all particles track successfully:**
- Geometry likely correct (at least for regions accessed)
- No guarantees for unvisited regions

**Step 5:** Fix issues and repeat

**Step 6:** Restore original input
```bash
# Remove VOID card, restore materials
# Test with actual materials and sources
```

### Why VOID Test Works

**Key Principles:**
1. **No collisions:** Void materials → particles stream through without scattering
2. **More tracks:** Particles travel farther → more geometry tested
3. **Flooding:** Surface source floods from outside → tests all boundaries
4. **Short run:** 10k particles sufficient for most geometries

**What It Catches:**
- Overlaps (particles get confused between cells)
- Gaps (particles enter undefined regions)
- Surface sense errors (particles cross incorrectly)

**What It May Miss:**
- Errors in rarely-visited regions
- Errors that only occur with specific physics (scattering angles)

---

## Surface Sense Verification

### Understanding Surface Sense

**Positive sense (+):** Points where surface equation > 0
**Negative sense (-):** Points where surface equation < 0

**Example: Sphere SO  10**
- Equation: x² + y² + z² - R² = 0
- At (15,0,0): 15² + 0² + 0² - 10² = 225 - 100 = +125 → positive sense (outside)
- At (5,0,0): 5² + 0² + 0² - 10² = 25 - 100 = -75 → negative sense (inside)

### Common Sense Errors

**Error 1: Shell with both surfaces negative**
```
c WRONG:
2  2  -2.3  -1 -2  IMP:N=1             $ Inside both surfaces (not a shell!)

c CORRECT:
2  2  -2.3  1 -2  IMP:N=1              $ Outside 1, inside 2 (shell)
```

**Error 2: Graveyard overlapping with system**
```
c WRONG:
999  0  1  IMP:N=0                     $ Outside surface 1
1  1  -1.0  1  IMP:N=1                 $ Also outside surface 1 (OVERLAP!)

c CORRECT:
1  1  -1.0  -1  IMP:N=1                $ Inside surface 1
999  0  1  IMP:N=0                     $ Outside surface 1 (no overlap)
```

### Verification Method

**For each surface, verify:**

1. **Count cells on each side:**
   - Plot geometry
   - Click on regions on both sides of surface
   - Should see different cells

2. **Check sense matches intent:**
   - Inner cell: typically negative sense of outer surface
   - Outer cell: typically positive sense of inner surface

3. **Verify with test point:**
   ```
   # Choose test point, evaluate surface equation
   # Example: Surface 1 SO 10, test point (5,0,0)
   # x² + y² + z² - R² = 25 + 0 + 0 - 100 = -75 < 0 → negative sense
   #
   # If cell should contain (5,0,0), use "-1" in definition
   ```

---

## Transformation Errors

### Symptom

```
particle lost at  15.00000  0.00000  0.00000
in cell    5 (or near cell 5, which uses transformation)
```

### Common Transformation Errors

**Error 1: Non-orthonormal rotation matrix**
```
*TR1  10 0 0  0 2 0  1 0 0  0 0 1     $ WRONG: Row 2 has length 2

# Verify matrix:
# Row 1: (0, 2, 0) → length = sqrt(0² + 2² + 0²) = 2 ≠ 1 (INVALID)
```

**Fix:**
```
*TR1  10 0 0  0 1 0  1 0 0  0 0 1     $ Correct: All rows length 1
```

**Error 2: Transformation applied to wrong surface**
```
10  1  SO  5                           $ Surface 10 uses TR1
# But TR1 intended for different surface
```

**Diagnosis:**
- Plot transformed geometry
- Verify surface is where expected
- Check if transformation necessary

**Fix:**
```
# Remove transformation to isolate issue:
10  SO  5                              $ Test without transformation

# If works, TR1 is problematic
# If still fails, error elsewhere
```

---

## Incremental Complexity Testing

### Strategy

Build geometry incrementally, testing at each stage to isolate errors.

### Example Progression

**Stage 1: Minimal geometry**
```
Simple Sphere Test
c Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Single sphere
999  0  1  IMP:N=0                     $ Graveyard

c Surface Cards
1  SO  10                              $ Sphere R=10

c Data Cards
MODE  N
M1  1001.80c  1.0                      $ Simple material
SDEF  POS=0 0 0  ERG=14.1
NPS  100
```

**Test:** Run → Should work flawlessly

**Stage 2: Add inner sphere**
```
c Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Inner sphere
2  2  -2.0  1 -2  IMP:N=1              $ Shell
999  0  2  IMP:N=0                     $ Graveyard

c Surface Cards
1  SO  5                               $ Inner radius
2  SO  10                              $ Outer radius
```

**Test:** Run → If error here, problem is in shell definition

**Stage 3: Add complexity**
```
# Add transformations, complex intersections, lattices one at a time
# Test after each addition
# When error occurs, last addition is likely cause
```

### Benefits

- **Isolates errors:** Know exactly which addition caused problem
- **Confidence:** Each stage verified before proceeding
- **Faster debugging:** Don't debug complex geometry all at once

---

## Common Geometry Patterns and Pitfalls

### Pattern 1: Concentric Spheres

**Correct:**
```
1  1  -1.0  -1  IMP:N=1                $ r < 10
2  2  -2.0  1 -2  IMP:N=1              $ 10 < r < 20
3  3  -3.0  2 -3  IMP:N=1              $ 20 < r < 30
999  0  3  IMP:N=0                     $ r > 30

1  SO  10
2  SO  20
3  SO  30
```

**Common Error:**
```
2  2  -2.0  -2  IMP:N=1                $ WRONG: -2 includes region of cell 1!
```

### Pattern 2: Rectangular Box

**Correct:**
```
1  1  -1.0  1 -2 3 -4 5 -6  IMP:N=1   $ Box
999  0  -1:2:-3:4:-5:6  IMP:N=0       $ Outside (De Morgan's law)

1  PX  10
2  PX  -10
3  PY  20
4  PY  -20
5  PZ  30
6  PZ  -30
```

**Common Error:**
```
999  0  1 2 3 4 5 6  IMP:N=0           $ WRONG: Would require all to be true (impossible!)
```

### Pattern 3: Cylinder with Endcaps

**Correct:**
```
1  1  -1.0  -1 -2 3  IMP:N=1           $ Inside CZ, between planes
999  0  1:2:-3  IMP:N=0                $ Outside

1  CZ  5                               $ Cylinder Z-axis, R=5
2  PZ  10                              $ Top endcap
3  PZ  -10                             $ Bottom endcap
```

**Common Error:**
```
999  0  1 2 3  IMP:N=0                 $ WRONG: AND logic (too restrictive)
```

---

## Best Practices

1. **Plot Before Running:** Catch visual errors early
2. **Use VOID Test:** Comprehensive geometry validation
3. **Build Incrementally:** Test at each stage
4. **Study Event Logs:** Show exact particle path to error
5. **Check Surface Senses:** Verify + vs - is correct
6. **Test Points:** Manually verify cell definitions at key locations
7. **Simplify to Debug:** Remove complexity until error disappears
8. **Save Working Versions:** Easy rollback if changes break geometry

---

## References

- **fatal_error_catalog.md:** Error message meanings
- **debugging_workflow.md:** Systematic procedures
- **MCNP Manual Chapter 4.8:** Geometry Errors
- **MCNP Primer:** Geometry Definition

---

**END OF GEOMETRY ERROR GUIDE**
