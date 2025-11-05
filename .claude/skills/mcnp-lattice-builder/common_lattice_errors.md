# Common Lattice Errors and Solutions

**Reference for:** mcnp-lattice-builder skill
**Source:** Current SKILL.md troubleshooting section + LATTICE-INFO-SUMMARY.md pitfalls
**Created:** 2025-11-04 (Session 16)

---

## OVERVIEW

Lattice geometry errors are among the most common issues in MCNP modeling. This document catalogs frequent problems, their causes, and proven solutions. Understanding these patterns helps diagnose issues quickly and build robust lattice models from the start.

**Most Common Error:** Incorrect surface ordering on LAT cell card (causes index mismatch)

---

## ERROR 1: Surface Ordering Causes Index Mismatch

### Symptom
- Lattice elements appear in wrong positions
- Fuel assemblies located where control assemblies expected
- Visual plots show unexpected arrangement
- FILL array pattern doesn't match intended design

### Root Cause
**Surface ordering on the LAT cell card defines lattice indexing**, not surface numbering. The order surfaces appear on the cell card determines which direction each index (i, j, k) increases.

### Example Problem
```
c Intended: i-index increases in +X direction
c But surfaces ordered incorrectly on cell card:

c WRONG surface order:
100  0  -12 11 -13 14 -15 16  U=10  LAT=1  FILL=...
         ^  ^   ^  ^   ^  ^
         Sfc order: -Y, +Y, -X, +X, -Z, +Z
         Result: i varies in Y direction (NOT X!)
```

### Solution
**For LAT=1 (hexahedral):** 6 surfaces in specific order
- Surfaces 1-2: Define direction for FIRST index (i)
- Surfaces 3-4: Define direction for SECOND index (j)
- Surfaces 5-6: Define direction for THIRD index (k)

**Correct ordering example:**
```
c i-index in X, j-index in Y, k-index in Z:
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=...
         ^  ^   ^  ^   ^  ^
         -X +X  -Y +Y  -Z +Z
         i varies in X direction (as intended)
```

**For LAT=2 (hexagonal prism):** 8 surfaces required
- First 6 surfaces: Hexagonal cross-section boundaries
- Surfaces 7-8: Top and bottom (Z direction)

### Verification Method
1. Run geometry plotter with lattice index labels displayed
2. Check which direction each index increases
3. If mismatch found, reorder surfaces on LAT cell card
4. Verify again with plotter

---

## ERROR 2: Lost Particle - Universe Cells Not Contained

### Symptom
```
FATAL ERROR: Lost particle
         Cell = 3
         Universe = 1
         Location = (0.55, 0.0, 50.0)
```

### Root Cause
One or more cells in the universe extend to infinity or are not fully bounded. When universe is filled into lattice element, particles "leak" at boundaries between elements.

### Example Problem
```
c Universe 1: Fuel pin with unbounded coolant
1  1  -10.0  -1       U=1  IMP:N=1  $ Fuel (r < 0.4)
2  2  -6.5    1 -2    U=1  IMP:N=1  $ Clad (0.4 < r < 0.5)
3  3  -1.0    2       U=1  IMP:N=1  $ Coolant (r > 0.5, UNBOUNDED!)

c When filled into lattice element with boundary at r=0.63,
c particles at 0.5 < r < 0.63 leak between elements
```

### Solution
**Ensure ALL cells in universe are bounded.** Add background cell if needed.

```
c CORRECT: All cells bounded
1  1  -10.0  -1       U=1  IMP:N=1  $ Fuel (r < 0.4)
2  2  -6.5    1 -2    U=1  IMP:N=1  $ Clad (0.4 < r < 0.5)
3  3  -1.0    2 -10   U=1  IMP:N=1  $ Coolant (0.5 < r < 0.63)
4  3  -1.0   10       U=1  IMP:N=1  $ Background (r > 0.63, fills element)

10  CZ  0.63  $ Lattice element boundary
```

### Alternative: Negative Universe Optimization

**⚠️ USE WITH EXTREME CAUTION**

If universe cells are FULLY enclosed within lattice element (never truncated), negative universe number can skip boundary checks:

```
c Only use if CERTAIN cells never touch element boundaries
1  1  -10.0  -1       U=-1  IMP:N=1  $ Negative universe (optimization)
```

**Danger:** If assumption wrong, MCNP produces silent errors with wrong answers. Always verify with VOID card and extensive plotting.

---

## ERROR 3: FILL Index Out of Range

### Symptom
```
ERROR: FILL array dimensions don't match lattice size
       Expected: 3×3×1 = 9 values
       Found: 4 values
```

### Root Cause
FILL array specification doesn't provide correct number of values for lattice dimensions.

### Example Problem
```
c Lattice element surfaces span 3 elements in X, 3 in Y, 1 in Z
c Total elements: 3×3×1 = 9

c WRONG: Only 4 values provided
100  0  -10 11 -12 13 -14 15  U=10  LAT=1
     FILL=0:2  0:2  0:0    $ Declares 3×3×1
          1 1               $ Only 4 values!
          1 1

c CORRECT: Full 9 values
100  0  -10 11 -12 13 -14 15  U=10  LAT=1
     FILL=0:2  0:2  0:0    $ Declares 3×3×1
          1 1 1             $ j=0: i=0,1,2
          1 1 1             $ j=1: i=0,1,2
          1 1 1             $ j=2: i=0,1,2
```

### Understanding FILL Array Format
```
FILL = i_min:i_max  j_min:j_max  k_min:k_max
       <values in Fortran order>
```

**Fortran ordering:** i-index varies FASTEST
- For 2D array (k=0): List all i values for j=j_min, then j=j_min+1, etc.
- For 3D array: List full i-j plane for k=k_min, then k=k_min+1, etc.

### Solution Checklist
1. Calculate total elements: (i_max - i_min + 1) × (j_max - j_min + 1) × (k_max - k_min + 1)
2. Count values in FILL array
3. Verify count matches total elements
4. Check i-varies-fastest ordering

---

## ERROR 4: Lattice Spacing Incorrect (Gaps or Overlaps)

### Symptom
- Geometry plots show gaps between lattice elements
- Lost particles at element boundaries
- Overlapping geometry errors

### Root Cause
Lattice element surface dimensions don't match intended pitch.

### Example Problem
```
c Intended pitch: 1.26 cm square
c Pin radius: 0.5 cm

c WRONG: Element too small (1.0×1.0 cm)
10  PX  -0.5
11  PX   0.5
12  PY  -0.5
13  PY   0.5
c Pitch = 1.0 cm → 0.26 cm gaps between elements!

c CORRECT: Element matches pitch (1.26×1.26 cm)
10  PX  -0.63
11  PX   0.63
12  PY  -0.63
13  PY   0.63
c Pitch = 1.26 cm → no gaps
```

### Verification
Calculate element dimensions from surface definitions:
- For PX surfaces: X-dimension = |PX2 - PX1|
- For PY surfaces: Y-dimension = |PY2 - PY1|
- For PZ surfaces: Z-dimension = |PZ2 - PZ1|

Compare to intended pitch in each direction.

---

## ERROR 5: Can't Tally in Specific Lattice Element

### Symptom
- Tally sums over entire lattice instead of single element
- Need flux in specific pin (e.g., corner pin, or pin at [i=8, j=8])

### Root Cause
Standard tallies sum over all instances of a cell/surface in a lattice. MCNP needs special syntax to specify individual elements.

### Solution 1: FS Card (Limited)
```
c Tally fuel in specific lattice cell (limited capability)
F4:N  1               $ Fuel cell (universe 1)
FS4  -100 10          $ Lattice cell 100, element at surface 10
C4   0 0 8*8          $ Comment (not functional - just documentation)
```

**Limitation:** FS approach has restrictions and may not work for all cases.

### Solution 2: TALLYX Subroutine (Recommended)
For precise lattice element tallying, use TALLYX Fortran subroutine. Allows full control over which elements contribute to tally.

**Reference:** MCNP6 User Manual §5.9.17 (TALLYX card)

### Alternative: Unique Materials Per Element
```
c Assign different material numbers to each element
c Element [0,0]: Use material 101
c Element [1,0]: Use material 102
c Element [0,1]: Use material 103
c ...

c Then tally material-specific:
F4:N  (101)  $ Flux in element [0,0] only
```

**Trade-off:** Increases memory usage, but provides tally flexibility.

---

## ERROR 6: Hexagonal Lattice Orientation Wrong

### Symptom
- Hexagonal lattice elements rotated 30° from expected
- Elements don't align with design specifications
- Assembly boundaries misaligned

### Root Cause
LAT=2 hexagonal lattices have **flat sides on LEFT/RIGHT, points UP/DOWN**. This is MCNP convention and cannot be changed.

### Standard LAT=2 Orientation
```
      ___
     /   \
    |     |  ← Flat sides on left/right
     \___/
       ↑
    Points up/down
```

### Solution
If different orientation needed (e.g., points left/right):
1. Use transformation (TRCL) to rotate entire filled lattice
2. Adjust surface definitions to match LAT=2 convention
3. Rotate filled cell by 30° or 90° as needed

**Example:**
```
c Rotate lattice 30° to change orientation
TR10  0 0 0   30 30 90  120 30 90  90 90 0

c Fill with transformation
1000  0  -1000  FILL=100 (TR10)  IMP:N=1
```

---

## ERROR 7: Nested Lattice Levels Confused

### Symptom
- Universe references incorrect
- FILL card points to wrong universe
- Hierarchy doesn't match intended design
- Complex error messages about universe nesting

### Root Cause
Multi-level lattice hierarchies have many universe references. Without clear documentation, easy to lose track of which universe is at which level.

### Example Confusion
```
c Intended hierarchy:
c   Pin (U=1) → Assembly (U=10) → Core (U=100)

c But coded as:
c   Pin (U=1) → ??? → Core filled with U=1 (WRONG!)
```

### Solution
**Document universe hierarchy explicitly with comments:**

```
c ===== UNIVERSE HIERARCHY =====
c U=0:   Main geometry (real world)
c U=1:   Fuel pin cell
c U=2:   Guide tube cell
c U=3:   Control rod cell
c U=10:  Assembly lattice (17×17, contains U=1,2,3)
c U=20:  Assembly + shroud (contains U=10)
c U=100: Core lattice (15×15, contains U=20)
c ===============================

c Level 1: Individual pins
1  1  -10.0  -1     U=1  IMP:N=1  $ Fuel pin
...

c Level 2: Assembly lattice
100  0  -10  U=10  LAT=1  FILL=0:16 0:16 0:0  1 1 2 1 ...  $ Pin lattice

c Level 3: Assembly with shroud
1000  0  -100  FILL=10  U=20  IMP:N=1  $ Fill with assembly lattice
...

c Level 4: Core lattice
10000  0  -1000  U=100  LAT=1  FILL=0:14 0:14 0:0  20 20 20 ...  $ Core

c Main geometry: Fill core
100000  0  -10000  FILL=100  IMP:N=1  $ Real world contains core
```

**Best practice:** Draw ASCII diagram showing hierarchy before coding.

---

## ERROR 8: FILL Card Missing on Lattice Cell

### Symptom
```
ERROR: Lattice cell has no FILL specification
       Cell = 100
       Universe = 10
```

### Root Cause
Cell has LAT parameter but no FILL parameter. Lattice cells MUST specify what fills them.

### Solution
```
c WRONG: LAT without FILL
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  IMP:N=1

c CORRECT: LAT with FILL
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
```

Every LAT cell requires either:
- `FILL=n` (single universe fills all elements)
- `FILL=i1:i2 j1:j2 k1:k2 <array>` (array of universes)

---

## ERROR 9: Non-Convex Lattice Element Cross-Sections

### Symptom
```
WARNING: Lattice element may not be convex
ERROR: Particle lost in lattice
```

### Root Cause
MCNP requires lattice element cross-sections to be convex and have opposite sides parallel. Non-convex shapes (e.g., L-shaped) not allowed.

### Example Problem
```
c INVALID: L-shaped element (not convex)
10  RPP  0  2  0  1  0  100
11  RPP  0  1  1  2  0  100
c Combined shape is L (not allowed in lattice)
```

### Solution
**Use only convex cross-sections:**
- Rectangle (LAT=1): Opposite sides parallel
- Hexagonal prism (LAT=2): Regular hexagon
- Both types must be convex

If complex shape needed, use multiple lattices or explicit geometry (not lattice).

---

## ERROR 10: Array Index Mismatch in FILL

### Symptom
- Specific universe appears in wrong lattice position
- Pattern in FILL array doesn't match intended layout
- Control assemblies at wrong coordinates

### Root Cause
Fortran array ordering misunderstood. First index (i) varies FASTEST in FILL array specification.

### Example Problem
```
c Intended layout (looking down from +Z):
c   j=1: [F F C]
c   j=0: [F C F]
c        i=0 1 2

c WRONG: Assuming j varies fastest
FILL=0:2  0:1  0:0
     1 1 2   $ Assumed j=0, then j=1 (WRONG!)
     1 2 1

c CORRECT: i varies fastest
FILL=0:2  0:1  0:0
     1 2 1   $ j=0: i=0(F), i=1(C), i=2(F)
     1 1 2   $ j=1: i=0(F), i=1(F), i=2(C)
```

### Verification Method
Write out explicit comments for each row:
```
FILL=0:2  0:1  0:0
     1 2 1   $ j=0: (i=0,j=0)=1, (i=1,j=0)=2, (i=2,j=0)=1
     1 1 2   $ j=1: (i=0,j=1)=1, (i=1,j=1)=1, (i=2,j=1)=2
```

---

## ERROR 11: Transformation Confusion

### Symptom
- Filled universe appears at wrong location
- Rotation not as expected
- Lattice elements misaligned after TRCL applied

### Root Cause
TRCL transformation syntax misunderstood or rotation matrix incorrect.

### Common Mistakes
1. **Displacement and rotation order:** MCNP applies rotation first, then displacement
2. **Rotation matrix elements:** Must satisfy orthogonality conditions
3. **Degree vs radian:** Angles in degrees (not radians)

### Solution
**Test transformation incrementally:**
```
c Step 1: Test displacement only (no rotation)
TR1  10 0 0   $ Translate +10 cm in X

c Step 2: Add rotation (verify each component)
TR1  10 0 0   30 30 90  120 30 90  90 90 0  $ 30° about Z
```

**Use standard rotation shortcuts:**
- 0 elements: No rotation (identity)
- 3 elements: Axis rotation (simpler than full matrix)
- 9 elements: Full rotation matrix

**Reference:** MCNP6 Manual §5.5.3 (TR card) for rotation matrix requirements.

---

## ERROR 12: Volume Specification Errors for Repeated Structures

### Symptom
- Source intensity calculations incorrect
- Tally normalization wrong
- Flux values off by factor equal to number of lattice elements

### Root Cause
VOL parameter on universe cell specifies volume **per instance**, not total volume of all instances.

### Example Problem
```
c 100 fuel pins in lattice, each with volume 10 cm³
c Total fuel volume = 1000 cm³

c WRONG: Specify total
1  1  -10.0  -1  U=1  VOL=1000  $ WRONG!

c CORRECT: Specify per instance
1  1  -10.0  -1  U=1  VOL=10    $ Volume of ONE pin
```

### Solution
**VOL for universe cell = volume of single instance**

MCNP automatically multiplies by number of instances when calculating:
- Source intensities (SDEF)
- Tally normalization (F4, F6, F7)
- Reaction rates

---

## ERROR 13: Negative Universe Misuse

### Symptom
- Wrong results with no error messages
- Silent calculation errors
- Validation against known solutions fails

### Root Cause
Negative universe used incorrectly. Cell marked as "fully enclosed" but actually truncated by higher-level boundary.

### Example Problem
```
c DANGEROUS: Assuming cell never truncated
1  1  -10.0  -1  U=-1  IMP:N=1  $ "Fully enclosed" (maybe not!)

c Later in model:
c Lattice element boundary at r=0.63 truncates cell 1
c But MCNP skips boundary checks due to U=-1
c Result: SILENT ERRORS
```

### Solution
**Avoid negative universes unless:**
1. Absolutely certain cells fully enclosed
2. Extensive geometry plotting confirms containment
3. VOID card verification performed
4. Validation against known solution successful

**Better approach:** Use positive universes (U=n, not U=-n). Slight computational overhead worth the safety.

---

## DIAGNOSTIC WORKFLOW

When encountering lattice errors, follow this systematic approach:

### Step 1: Check Surface Ordering
- Most common error
- Run plotter with index labels
- Verify i, j, k directions match intent

### Step 2: Verify Universe Containment
- Check all universe cells bounded
- Look for infinite cells (missing surfaces)
- Add background cells if needed

### Step 3: Validate FILL Array
- Count total elements
- Count FILL array values
- Verify Fortran ordering (i fastest)

### Step 4: Check Lattice Element Dimensions
- Calculate pitch from surfaces
- Compare to design specifications
- Verify no gaps or overlaps

### Step 5: Review Universe Hierarchy
- Draw hierarchy diagram
- Trace FILL references through levels
- Confirm universe numbers consistent

### Step 6: Plot, Plot, Plot
- Multiple viewing angles
- Cross-sections through key planes
- Index labels displayed
- Color by material AND universe

---

## PREVENTION CHECKLIST

Before running complex lattice model:

- [ ] Surface order verified with geometry plotter
- [ ] All universe cells bounded (no infinite cells)
- [ ] FILL array value count matches element count
- [ ] Lattice element dimensions match intended pitch
- [ ] Universe hierarchy documented with comments
- [ ] Volume specifications per-instance, not total
- [ ] Transformations tested incrementally
- [ ] Geometry plotted from multiple angles
- [ ] Cross-sections through lattice verified
- [ ] Simple test case validated before scaling up

---

## SUMMARY

**Top 5 Most Common Errors:**
1. **Surface ordering wrong** (index mismatch)
2. **Universe cells not fully contained** (lost particles)
3. **FILL array dimension mismatch** (wrong element count)
4. **Lattice spacing incorrect** (gaps or overlaps)
5. **Volume specification wrong** (per-instance vs total)

**Golden Rule:** When in doubt, PLOT THE GEOMETRY with lattice indices displayed.

**Debugging Strategy:** Start simple (single lattice element), verify, then scale up incrementally.

---

**END OF COMMON_LATTICE_ERRORS.MD**
