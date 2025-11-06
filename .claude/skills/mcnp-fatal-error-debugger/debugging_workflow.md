# MCNP Systematic Debugging Workflows

**Purpose:** Step-by-step procedures for systematic debugging of MCNP fatal errors.

**Companion to:** mcnp-fatal-error-debugger SKILL.md

---

## Overview

This guide provides systematic, reproducible workflows for debugging MCNP fatal errors. Each workflow is designed to isolate and fix errors efficiently using proven techniques.

---

## Universal Debugging Workflow

### When to Use

Any fatal error or BAD TROUBLE message.

### Procedure

**Step 1: Identify Error Type**
```
Read first fatal error or BAD TROUBLE message

Categories:
- Input syntax error → Fix syntax
- Cross-reference error → Fix missing definition
- Geometry error → Use Geometry Workflow (below)
- Source error → Use Source Workflow (below)
- Material/ZAID error → Check xsdir, fix ZAID
- BAD TROUBLE → See bad_trouble_guide.md
```

**Step 2: Fix First Error Only**
```
# CRITICAL RULE: Fix only the FIRST fatal error

fatal error #1: material 3 not defined  ← FIX THIS
fatal error #2: cell 5 invalid          ← Ignore (likely cascade)
fatal error #3: importance not set      ← Ignore (likely cascade)

# Add M3 card
# Re-run
# Check if errors #2 and #3 disappear
```

**Step 3: Verify Fix**
```
# Re-run MCNP after fix
# Check output:
#   - No fatal errors?  → Success, proceed
#   - Different error?  → Start over at Step 1
#   - Same error?       → Fix didn't work, try different approach
```

**Step 4: Test with Short Run**
```
NPS  1000                              $ Short test before full run

# If 1000 particles succeed:
NPS  10000                             $ Longer test
# Then proceed to production
```

---

## Geometry Debugging Workflow (VOID Card Test)

### When to Use

- Lost particle errors
- "bad trouble in subroutine track"
- Suspected overlaps or gaps
- Dashed lines in plots

### Procedure

**Step 1: Save Original Input**
```bash
cp original.i original_backup.i
```

**Step 2: Create Test Input** `test_geom.i`

```
[Title Card]
c =================================================================
c Cell Cards
c =================================================================
c
c Original cell definitions (keep unchanged):
1  1  -1.0  -1  IMP:N=1
2  2  -2.3  1 -2  IMP:N=1
3  3  -11.3  2 -3  IMP:N=1
c [... more original cells ...]

c Add flooding cells at end:
998  0  -998 999  IMP:N=1              $ Between system and flood sphere
999  0  998  IMP:N=0                   $ Graveyard outside flood

c =================================================================
c Surface Cards
c =================================================================
c
c Original surfaces (keep unchanged):
1  SO  10
2  SO  20
3  SO  30
c [... more original surfaces ...]

c Add flood surfaces at end:
998  SO  1000                          $ Large sphere enclosing system
999  SO  [value]                       $ System outer boundary (estimate)
    c [value] should be larger than outermost system surface
    c Example: if system extends to R=50, use SO  80

c =================================================================
c Data Cards
c =================================================================
c
VOID                                   $ Override all materials → void
MODE  N                                $ Neutrons only (or original MODE)
IMP:N  1  1  1  ...  1  1  0          $ All cells IMP=1 except 999 (last=0)
                                       $ Count: one entry per cell
SDEF  SUR=998  NRM=-1                  $ Inward-directed surface source
NPS  10000                             $ Short test run
```

**Step 3: Run Test**
```bash
mcnp6 inp=test_geom.i outp=test_geom.o
```

**Step 4: Interpret Results**

**Case A: All particles track successfully (no lost particles)**
```
# Check output:
10000 particles run
0 particles lost

# Interpretation: Geometry likely correct
# Action: Remove VOID card, restore materials, test with full input
```

**Case B: Particles get lost**
```
# Check output for lost particle messages:
  particle lost at   5.12 3.69 0.00
  in cell    2

# Action:
1. Note lost location coordinates
2. Examine event log for path
3. Plot geometry at lost location (Step 5)
```

**Step 5: Plot at Lost Location**
```
# Use coordinates from lost particle message
IP  5.12 3.69 0                        $ Origin at lost location
BA  10                                 $ Extent ±10 cm
PX  1 0 0                              $ View along X

# In plotter:
# - Look for dashed lines (geometry errors)
# - Check cells on both sides of surfaces
# - Identify overlap or gap
```

**Step 6: Fix Geometry Error**

**If overlap detected:**
```
c WRONG (cell 2 overlaps cell 1):
1  1  -1.0  -1  IMP:N=1                $ Sphere R=10
2  2  -2.3  -2  IMP:N=1                $ Sphere R=20 (encloses cell 1!)

c CORRECT (cell 2 is shell):
1  1  -1.0  -1  IMP:N=1                $ Inner sphere R=10
2  2  -2.3  1 -2  IMP:N=1              $ Shell: 10 < R < 20
```

**If gap detected:**
```
c WRONG (gap between R=10 and R=20):
1  1  -1.0  -1  IMP:N=1                $ R < 10
2  2  -2.3  2  IMP:N=1                 $ R > 20 (GAP: 10 < R < 20)

c CORRECT (add cell for gap):
1  1  -1.0  -1  IMP:N=1                $ R < 10
2  0        1 -2  IMP:N=1              $ Void: 10 < R < 20
3  2  -2.3  2  IMP:N=1                 $ R > 20
```

**Step 7: Re-run VOID Test**
```bash
# Test with fixed geometry
mcnp6 inp=test_geom.i outp=test_geom.o

# If still failing, repeat Steps 5-6
# If succeeds, proceed to Step 8
```

**Step 8: Restore Original Input**
```
# Remove VOID card
# Restore original materials
# Remove flood cells 998-999 and surfaces 998-999
# Keep geometry fixes
# Test with original source and materials
```

---

## Source Debugging Workflow

### When to Use

- "impossible source variable dependencies"
- "source particle not in any cell"
- "bad trouble in subroutine sourcc"
- Source-related fatal errors

### Procedure

**Step 1: Test with Minimal Source**
```
c Replace complex source with simplest possible:
c SDEF  POS=D1  AXS=FPOS=D2  ERG=FCEL=D3  ...  (complex, failing)

c Minimal test:
SDEF  POS=0 0 0  ERG=14.1                      $ Point source, monoenergetic
NPS  100

# Run test:
# - If works: Problem is in complex source specification
# - If fails: Problem is geometry or position
```

**Step 2: Verify Source Position Inside Geometry**
```
# Plot at source position:
IP  0 0 0                              $ Origin at source (or POS value)
PX  1 0 0                              $ View along X

# Verify:
# - Source point is inside a defined cell
# - Cell has material (not void with IMP=0)
# - Cell has IMP > 0
```

**Step 3: Add Complexity Incrementally**
```
c Test 1: Position distribution
SDEF  POS=D1  ERG=14.1
SI1  L  0 0 0  5 0 0
SP1     1  1
# Run → If works, position OK

c Test 2: Energy distribution
SDEF  POS=D1  ERG=D2
SI2  L  1  14.1
SP2     0.9  0.1
# Run → If works, energy OK

c Test 3: Direction
SDEF  POS=D1  ERG=D2  DIR=D3
SI3  -1  1
SP3  0  1
# Run → If fails, problem in DIR specification

# Continue adding features until error reproduces
# Last added feature is likely cause
```

**Step 4: Check SI/SP Consistency**
```
c For each distribution:

SI1  L  0 0 0  10 0 0  20 0 0          $ 3 entries
SP1     0.2  0.3  0.5                  $ 3 entries (MATCH)

SI2  H  0  1  10  100                  $ 4 bin boundaries
SP2     1  1  1                        $ 3 probabilities (N-1 for histogram, CORRECT)

# Verify:
# - List (L): SI and SP same count
# - Histogram (H): SP has N-1 entries
# - DS points to existing distributions
```

**Step 5: Check for Invalid Dependencies**
```
c INVALID:
SDEF  POS=D1  AXS=FPOS=D2              $ AXS cannot depend on POS

c INVALID:
SDEF  POS=D1  SUR=FPOS=D2              $ SUR cannot depend on POS

c VALID:
SDEF  CEL=D1  ERG=FCEL=D2              $ ERG can depend on CEL

c VALID:
SDEF  POS=D1  DIR=FPOS=D2              $ DIR can depend on POS

# See Source Primer Table 5-1 for complete list
```

**Step 6: Test Each Distribution Value**
```
c For POS=D1:
SI1  L  0 0 0  10 0 0  20 0 0

# Test each position:
SDEF  POS=0 0 0  ERG=14.1              $ Test position 1
# Run → works?
SDEF  POS=10 0 0  ERG=14.1             $ Test position 2
# Run → works?
SDEF  POS=20 0 0  ERG=14.1             $ Test position 3
# Run → fails? → This position is outside geometry!
```

**Step 7: Fix Source Specification**
```
c Remove invalid dependency:
SDEF  POS=D1  AXS=0 0 1  ERG=14.1     $ Fixed AXS

c Remove position outside geometry:
SI1  L  0 0 0  10 0 0                  $ Removed (20,0,0)
SP1     1  1                            $ Updated probabilities

c Fix energy distribution:
SI2  H  0  0.1  1  10                  $ Non-zero bin widths (was 0,0,1)
SP2     1  1  1
```

---

## Incremental Complexity Workflow

### When to Use

- Building new complex geometry
- Adding features to working input
- Debugging input with many features

### Procedure

**Step 1: Start with Minimal Working Input**
```
Minimal Test
c Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Single sphere
999  0  1  IMP:N=0                     $ Graveyard

c Surface Cards
1  SO  10                              $ Sphere R=10

c Data Cards
MODE  N
M1  1001.80c  1.0                      $ Hydrogen
SDEF  POS=0 0 0  ERG=14.1
NPS  100
```

**Test:** Should work flawlessly

**Step 2: Add One Feature**
```
c Add inner sphere:
1  1  -1.0  -1  IMP:N=1                $ Inner R=5
2  2  -2.0  1 -2  IMP:N=1              $ Shell R=5 to R=10
999  0  2  IMP:N=0

1  SO  5
2  SO  10
```

**Test:** Run 100 particles
- **If works:** Continue to Step 3
- **If fails:** Error is in this addition (shell definition)

**Step 3: Add Next Feature**
```
c Add material complexity:
M1  1001.80c  2  8016.80c  1          $ Water
M2  6000.80c  1                        $ Carbon
```

**Test:** Run 100 particles
- **If works:** Continue
- **If fails:** Error in material definition

**Step 4: Continue Adding Features**
```
# Add in order:
1. Basic geometry → test
2. Materials → test
3. Source complexity → test
4. Tallies → test
5. Variance reduction → test

# Test after each addition
# When error occurs, last addition is cause
```

**Step 5: When Error Occurs**
```
# Last added feature caused error
# Focus debugging on that feature only
# Don't debug entire input
```

---

## Event Log Analysis Workflow

### When to Use

- Lost particle errors
- Need to understand particle path
- Geometry errors

### Procedure

**Step 1: Locate Event Log in Output**
```
# Search outp for "event log":
grep -A 20 "event log" outp

# Find section like:
  event log of particle        1234
    surface     cell    mat     nps
                  1      1        1234
        10        2      2        1234
        15        3      3        1234
        15        ?      ?        1234
```

**Step 2: Interpret Event Log**
```
Line 1 (blank surface): Born in cell 1, material 1
Line 2: Crossed surface 10 → entered cell 2, material 2
Line 3: Crossed surface 15 → entered cell 3, material 3
Line 4: Crossed surface 15 again → LOST (? = unknown cell)
```

**Step 3: Identify Problem Surface**
```
# Last line shows problem:
        15        ?      ?        1234    ← Lost crossing surface 15

# Problem is near surface 15
# Cell on other side of surface 15 from cell 3 is undefined/overlapping
```

**Step 4: Plot Problematic Region**
```
# Use lost particle coordinates:
IP  [x] [y] [z]                        $ From "particle lost at" message
BA  10                                 $ View ±10 cm

# Focus on:
# - Surface 15
# - Cell 3 (last known cell)
# - Cells adjacent to surface 15
```

**Step 5: Examine Cell Definitions**
```
# Cell 3 definition:
3  3  -11.3  [geometry]  IMP:N=1

# Check:
# - What's on other side of surface 15?
# - Is there a cell defined there?
# - Does cell 3 geometry make sense relative to surface 15?
```

**Step 6: Fix Geometry**
```
# If gap: Add missing cell
# If overlap: Fix cell 3 or adjacent cell definition
# If wrong sense: Correct surface sense in cell 3
```

---

## Binary Search Debugging Workflow

### When to Use

- Large complex input with error
- Don't know which section causes error
- Input has many features

### Procedure

**Step 1: Verify Input Has Error**
```bash
mcnp6 inp=complex.i
# Verify fatal error occurs
```

**Step 2: Comment Out Half the Features**
```
c Divide input conceptually:
# Half 1: Cells 1-50, related surfaces, materials
# Half 2: Cells 51-100, related surfaces, materials

# Comment out Half 2:
c 51  1  -1.0  -51  IMP:N=1
c 52  2  -2.3  -52  IMP:N=1
c [... rest of Half 2 ...]
```

**Step 3: Test**
```bash
mcnp6 inp=complex.i
```

**Case A: Error disappears**
```
# Error is in commented Half 2
# Uncomment Half 2
# Comment out Half 1
# Test again
```

**Case B: Error persists**
```
# Error is in active Half 1
# Keep Half 2 commented
# Now divide Half 1 in half
# Comment out half of Half 1
# Test
```

**Step 4: Repeat**
```
# Keep dividing in half until error isolated to small section
# Example progression:
# 100 cells → 50 cells → 25 cells → 12 cells → 6 cells → 3 cells → 1 cell

# Eventually isolate to specific cell or card causing error
```

**Step 5: Fix Isolated Error**
```
# With error isolated to single cell or small section:
# Much easier to debug
# Fix that specific element
# Uncomment rest of input
# Test full input
```

---

## Transformation Debugging Workflow

### When to Use

- Errors in geometry using transformations
- Lost particles in transformed regions
- Suspicious behavior with TR/TRCL cards

### Procedure

**Step 1: Identify Transformations**
```
# Find all TR cards:
grep "^\*TR\|^TR" input.i

# Find all surfaces/cells using transformations:
grep " [0-9]$" [surface cards]         $ Surface with TR number
grep "TRCL=" [cell cards]              $ Cell with TRCL
```

**Step 2: Test Without Transformations**
```
c Original (with transformation):
10  1  SO  5                           $ Surface 10 transformed by TR1

c Test (without transformation):
10  SO  5                              $ Remove TR number
c *TR1  10 0 0  0 1 0  1 0 0  0 0 1   $ Comment out TR card

# Run test:
# - If works: Problem is in transformation
# - If fails: Problem is elsewhere
```

**Step 3: Verify Transformation Matrix**
```
*TR1  10 0 0  0 1 0  1 0 0  0 0 1

# Check orthonormality:
# Row 1: (0, 1, 0) → length = sqrt(0² + 1² + 0²) = 1 ✓
# Row 2: (1, 0, 0) → length = sqrt(1² + 0² + 0²) = 1 ✓
# Row 3: (0, 0, 1) → length = sqrt(0² + 0² + 1²) = 1 ✓

# Check orthogonality:
# Row 1 · Row 2 = 0×1 + 1×0 + 0×0 = 0 ✓
# Row 1 · Row 3 = 0×0 + 1×0 + 0×1 = 0 ✓
# Row 2 · Row 3 = 1×0 + 0×0 + 0×1 = 0 ✓

# If any check fails, transformation is invalid
```

**Step 4: Plot Transformed Geometry**
```
# View original and transformed geometry:

# Origin view:
IP  0 0 0
PX  1 0 0

# Transformation center view:
IP  10 0 0                             $ If TR1 = 10 0 0 (translation)
PX  1 0 0

# Verify surfaces appear where expected
```

**Step 5: Test Transformation Independently**
```
c Create simple test case:
Simple Transformation Test
c Cell Cards
1  1  -1.0  -1  IMP:N=1                $ Untransformed sphere
2  1  -1.0  -2  IMP:N=1                $ Transformed sphere
999  0  1 2  IMP:N=0

c Surface Cards
1  SO  5                               $ Untransformed
2  1  SO  5                            $ Transformed by TR1

c Data Cards
*TR1  10 0 0  0 1 0  1 0 0  0 0 1     $ Translation +10 in X
MODE  N
M1  1001.80c  1.0
SDEF  POS=0 0 0  ERG=14.1
NPS  100

# Should see two spheres: one at origin, one at (10,0,0)
# Plot to verify
```

---

## Multi-View Plotting Workflow

### When to Use

- Visual geometry verification
- Looking for overlaps/gaps
- Understanding complex 3D geometry

### Procedure

**Step 1: Create Plot File**
```
c Add plot cards to input:
c (or use interactive plotter)

IP  0 0 0                              $ Origin
BA  50                                 $ Extent
PX  0 0 1                              $ View down Z-axis (XY plane)
```

**Step 2: Generate Plots from Three Directions**
```
c View 1: XY plane (Z-axis view)
IP  0 0 0
PX  0 0 1

c View 2: XZ plane (Y-axis view)
IP  0 0 0
PX  0 1 0

c View 3: YZ plane (X-axis view)
IP  0 0 0
PX  1 0 0
```

**Step 3: Look for Dashed Lines**
```
# In each view:
# - Dashed lines = potential geometry error
# - Solid lines = surfaces with exactly one cell on each side
# - No lines = no surfaces (possible gap)

# Focus on dashed lines near:
# - Complex intersections
# - Transformed regions
# - Lost particle locations
```

**Step 4: Zoom Into Suspicious Regions**
```
c If dashed line found at (10, 20, 30):
IP  10 20 30                           $ Center on suspicious region
BA  5                                  $ Zoom in (±5 cm)
PX  0 0 1
```

**Step 5: Verify Cell Labels**
```
# In interactive plotter:
# - Enable "Color by Cell"
# - Click on regions near dashed lines
# - Verify cell numbers make sense
# - Check for overlapping cell definitions
```

---

## Checklist-Based Debugging

### Universal Fatal Error Checklist

Before running MCNP, verify:

**Input Structure:**
- [ ] Three-block structure (cells, surfaces, data)
- [ ] Exactly one blank line between blocks
- [ ] Title card present (first line)

**Cross-References:**
- [ ] All material numbers in cells have M cards
- [ ] All surface numbers in cells are defined
- [ ] All transformations referenced are defined
- [ ] All tally surfaces/cells exist

**Geometry:**
- [ ] Plotted from multiple angles
- [ ] No dashed lines (or understood)
- [ ] Every point in space belongs to exactly one cell
- [ ] Graveyard cell with IMP=0 exists

**Source:**
- [ ] Source position inside geometry (plotted)
- [ ] Source cell has IMP > 0
- [ ] Source cell not void (unless intentional)
- [ ] No invalid dependencies (AXS=FPOS, etc.)

**Materials:**
- [ ] All ZAIDs exist in xsdir (checked with grep)
- [ ] Cross-section library version consistent
- [ ] Thermal scattering (MT) cards match M cards

**Physics:**
- [ ] MODE consistent with materials
- [ ] IMP card entries for all cells
- [ ] PHYS card parameters reasonable

---

## References

- **fatal_error_catalog.md:** Error messages
- **geometry_error_guide.md:** Geometry debugging details
- **source_error_guide.md:** Source error details
- **bad_trouble_guide.md:** BAD TROUBLE recovery
- **MCNP Manual Chapter 3:** Debugging techniques

---

**END OF DEBUGGING WORKFLOW GUIDE**
