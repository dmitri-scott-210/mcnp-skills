# MCNP Geometry Debugging - Complete Guide

Geometry errors are the most common and frustrating MCNP problems. This guide provides systematic methods to find and fix geometry issues BEFORE running expensive simulations.

## Three-Phase Debugging Strategy

1. **Prevention** - Build geometry correctly from the start
2. **Pre-run validation** - Test geometry before production runs
3. **Diagnosis** - Systematically fix errors when they occur

---

## Phase 1: Pre-Run Validation (DO THIS EVERY TIME)

### Step 1: VOID Card Testing (Geometry Flood Test)

**Purpose:** Test if geometry is closed (no gaps) without running particles

**How it works:**
- VOID card temporarily treats specified cells as void (m=0)
- MCNP creates uniform external source that floods problem
- Particles test if they can escape or get lost
- Fast test (minutes) instead of expensive production run

**Syntax:**
```
VOID  cell_list
```

**Example usage:**
```
c Cell cards
1  1  -10.5  -1  IMP:N=1
2  2  -8.0    1 -2  IMP:N=1
3  0          2  IMP:N=0

c Data block
MODE N
VOID  1 2              $ Temporarily treat cells 1 and 2 as void for testing
SDEF  ERG=1  POS=0 0 0 PAR=1
NPS   10000            $ Small number for quick test
```

**What to check in output:**
- **"geometry passes internal consistency check"** - GOOD
- **Lost particle errors** - BAD, geometry has gaps
- **Particles escape quickly** - Graveyard working correctly
- **Particles get stuck in loops** - Geometry error (overlap or gap)

**Best practice workflow:**
1. Add `VOID` card with all material cells listed
2. Run with `NPS 10000` (10-minute test)
3. Check output for lost particles
4. Remove VOID card for production run

**When to use:**
- Before EVERY first run of new geometry
- After making ANY geometry changes
- When adding new cells or surfaces
- When debugging lost particle errors

### Step 2: Geometry Plotting (Visual Inspection)

**Purpose:** Visualize geometry to spot errors by eye

**Interactive plotting:** Run MCNP with `ip` command:
```
mcnp6 inp=myfile.inp ip
```

**Plot commands (at MCNP prompt):**
```
basis  0 0 1         $ Set view direction (Z-axis view)
origin 0 0 50        $ Set plot center point
extent 20 20         $ Set plot size (±20 cm in X and Y)
px  0  400 400       $ Plot X-Y plane at Z=0, 400×400 pixels

label 1 2            $ Show cell/surface labels
color  1 2 3 4       $ Color cells by importance, material, density, etc.
```

**Common plot views:**
```
c X-Y plane (top view)
basis  0 0 1
px  0  600 600

c X-Z plane (side view)
basis  0 1 0
py  0  600 600

c Y-Z plane (front view)
basis  1 0 0
pz  0  600 600
```

**What to look for:**
- **White regions** - Void or low-importance cells
- **Black regions** - Undefined geometry (ERROR!)
- **Unexpected colors** - Wrong material assigned
- **Gaps between cells** - Geometry not closed
- **Overlapping cells** - Multiple cells claim same space (ERROR!)

**Using labels:**
```
label 1 2           $ Label: 1=cell numbers, 2=surface numbers
```
Shows cell numbers on plot - verify they match your expectation

### Step 3: Small Particle Run (Cheap Validation)

**Purpose:** Run small number of particles to catch errors early

**Method:**
```
NPS  1000           $ Start with just 1000 particles
```

**Run and check output for:**
1. Fatal errors (geometry failures) - FIX IMMEDIATELY
2. Warnings about surfaces, cells, transformations
3. Lost particle messages
4. Excessive run time (should be seconds for 1k particles)

**If successful:**
```
NPS  10000          $ Increase to 10k particles
```

Then check tallies for reasonable values before full production run.

---

## Phase 2: Lost Particle Diagnosis

### Understanding Lost Particles

**What is a lost particle?**
- Particle position doesn't match any cell geometry
- MCNP can't determine which cell particle is in
- Usually caused by geometry gaps or errors

**Lost particle message format:**
```
lost particle at x= 10.500 y= 5.230 z= 100.005
cell   20  surf   15  error code   1
```

**Error codes:**
- **Code 1** - Particle crossed surface but found no next cell (gap)
- **Code 2** - Particle in multiple cells (overlap)
- **Code 3** - Particle outside all cells (escaped through gap)
- **Code 4** - Surface tracking error (surface normal issue)

### Automatic Event Log Rerun

**MCNP feature:** When lost particle occurs, MCNP writes event log to file

**File created:** `runtpe` (binary file with particle history)

**How to use:**
1. Run fails with lost particle
2. MCNP creates `runtpe` with events leading to lost particle
3. Examine output for location: `x= ... y= ... z= ...`
4. Check cell and surface numbers in error message
5. Plot geometry at lost particle location

**Manual rerun from event log:**
```
mcnp6 inp=myfile.inp runtpe=previous_runtpe
```

This reruns EXACT particle that was lost (for debugging)

### Systematic Lost Particle Debugging (10 Steps)

#### Step 1: Locate the Problem
```
Lost particle message:
  x= 10.500 y= 5.230 z= 100.005
  cell 20  surf 15
```
Record: position (x,y,z), cell number, surface number

#### Step 2: Plot Geometry at Lost Particle Location
```
mcnp6 inp=myfile.inp ip
> origin 10.5 5.23 100.005    $ Set to lost particle location
> extent 5 5                  $ Small region around lost particle
> px 100.005 600 600          $ Plot X-Y plane at lost Z
> label 1 2                   $ Show cell and surface labels
```

#### Step 3: Check Surface Definition
Find surface 15 in input:
```
15  PZ  100.0                 $ Is this correct?
```

**Common issues:**
- Surface position wrong (should be 100.0, but lost particle at 100.005)
- Surface orientation wrong (plane facing wrong direction)
- Missing surface in geometry

#### Step 4: Check Cell Geometry at Lost Particle
Find cell 20:
```
20  1  -10.5  -10 11 -12 13 -14 15  IMP:N=1
```

**Questions to ask:**
- Does Boolean expression include surface 15?
- Is particle on correct side of surface 15?
- Are there other cells adjacent to surface 15?

#### Step 5: Check for Gaps (Most Common Cause)
```
c Cell 20 is inside surface 15: -15 means z < 100.0
20  1  -10.5  ... -15  IMP:N=1

c What cell is outside surface 15 (z > 100.0)?
c If no cell has +15 in geometry, there's a GAP
```

**Fix:** Add cell for region beyond surface 15, or modify boundary cell

#### Step 6: Check for Overlaps
If error code = 2 (multiple cells), two cells claim same space:
```
20  1  -10.5  -10 11 -12 13 -14 15  IMP:N=1
30  2  -8.0   -10 11 -12 13 -14 16  IMP:N=1
```

If surface 15 and 16 are the same location, cells 20 and 30 overlap

**Fix:** Ensure cells are mutually exclusive (one has -15, other has 15)

#### Step 7: Check Surface Tolerance Issues
Lost particle at z=100.005, but surface at z=100.0:
- Particle crossed surface due to finite precision
- May indicate surfaces too close together (< 1e-6 cm)

**Fix:** Use exact coincident surfaces or increase spacing

#### Step 8: Check Complement Operator Usage
```
20  1  -10.5  -10 #30  IMP:N=1
```

If cell 20 uses complement (#30), ensure cell 30 is properly defined

**Common mistake:** Cell 30 not defined, or cell 30 in different universe

#### Step 9: Check Universe/Fill Issues
Lost particle in lattice or filled universe:
- Check universe boundaries align
- Verify FILL array correct
- Ensure filled universe geometry matches fill cell

**Debug:** Plot at universe level, check local coordinates

#### Step 10: Manual Position Test
Calculate which cell particle SHOULD be in:

For position (10.5, 5.23, 100.005), manually evaluate surfaces:
```
10  PX  0.0      → x=10.5 is positive side (+10)
11  PX  20.0     → x=10.5 is negative side (-11)
12  PY  0.0      → y=5.23 is positive side (+12)
13  PY  10.0     → y=5.23 is negative side (-13)
14  PZ  0.0      → z=100.005 is positive side (+14)
15  PZ  100.0    → z=100.005 is positive side (+15)
```

Particle should be in cell with geometry: `-11 +12 -13 +15` (or similar)

If no cell has this geometry → **gap confirmed**

---

## Phase 3: Common Geometry Error Patterns

### Error 1: Missing Boundary Cell (Gap)

**Symptom:** Lost particles at outer boundary, error code 3

**Cause:** No cell defined beyond certain surface

**Example:**
```
1  1  -10.5  -1  IMP:N=1     $ Inside sphere
c ERROR: No cell for r > 10 (outside sphere)
1  SO  10.0
```

**Fix:** Add graveyard cell
```
1  1  -10.5  -1  IMP:N=1
2  0         1   IMP:N=0     $ Graveyard
```

### Error 2: Cell Overlap

**Symptom:** Lost particle error code 2, or particles in wrong cell

**Cause:** Two cells claim same space

**Example:**
```
1  1  -10.5  -1 -2  IMP:N=1   $ Inside surf 1 AND inside surf 2
2  2  -8.0   -2 -3  IMP:N=1   $ Inside surf 2 AND inside surf 3
c If surf 1 and 2 overlap, cells 1 and 2 overlap
```

**Fix:** Use mutually exclusive geometry
```
1  1  -10.5  -1 2  IMP:N=1    $ Inside 1, outside 2
2  2  -8.0    1 -2  IMP:N=1   $ Outside 1, inside 2
```

### Error 3: Gap Between Cells

**Symptom:** Lost particles between two cells, error code 1

**Cause:** No cell defined for region between surfaces

**Example:**
```
1  1  -10.5  -1  IMP:N=1       $ r < 8 cm
2  2  -8.0    2  IMP:N=1       $ r > 10 cm
c GAP: 8 cm < r < 10 cm undefined
1  SO  8.0
2  SO  10.0
```

**Fix:** Fill the gap
```
1  1  -10.5  -1     IMP:N=1
2  2  -8.0    1 -2  IMP:N=1    $ Between surfaces 1 and 2
3  0          2     IMP:N=0    $ Outside surface 2
```

### Error 4: Boolean Expression Error

**Symptom:** Unexpected geometry, particles in wrong regions

**Cause:** Incorrect Boolean logic (wrong operator precedence)

**Example:**
```
1  1  -10.5  -1 2 : -3  IMP:N=1
c Evaluates as: (-1 2) : (-3)  → (inside 1 AND outside 2) OR (inside 3)
c Probably wanted: -1 (2 : -3)  → inside 1 AND (outside 2 OR inside 3)
```

**Fix:** Use parentheses to control order
```
1  1  -10.5  -1 (2 : -3)  IMP:N=1
```

### Error 5: Complement Operator Misuse

**Symptom:** Lost particles, cells not where expected

**Cause:** Complement (#n) references wrong cell or undefined cell

**Example:**
```
1  1  -10.5  -1 #10  IMP:N=1
c ERROR: Cell 10 not defined, or cell 10 in different universe
```

**Fix:** Define cell 10, or remove complement
```
10  2  -8.0  -2  IMP:N=1       $ Define cell 10
1   1  -10.5  -1 #10  IMP:N=1  $ Now complement is valid
```

### Error 6: Surface Numbering Conflict

**Symptom:** Wrong geometry, surfaces not where expected

**Cause:** Surface number used twice (duplicate definitions)

**Example:**
```
1  PZ  0.0
2  CZ  5.0
1  PZ  100.0        $ ERROR: Surface 1 defined twice
```

**Fix:** Use unique surface numbers
```
1  PZ  0.0
2  CZ  5.0
3  PZ  100.0
```

### Error 7: Transformation Error

**Symptom:** Geometry in wrong location, lost particles near transformed cells

**Cause:** TRCL references undefined transformation, or transformation wrong

**Example:**
```
1  0  -1  FILL=2  TRCL=10  IMP:N=1
c ERROR: *TR10 not defined in data block
```

**Fix:** Define transformation
```
*TR10  10 0 0  1 0 0  0 1 0  0 0 1   $ Translation by (10,0,0)
```

### Error 8: Lattice Index Error

**Symptom:** Lattice positions wrong, or lost particles in lattice

**Cause:** FILL array indices don't match LAT geometry, or wrong index order

**Example (LAT=1):**
```
10  0  -10 11 -12 13 -14 15  LAT=1  U=2  IMP:N=1
       FILL=0:2 0:2 0:0
            1 1 2          $ j=2
            1 1 1          $ j=1
            2 1 1          $ j=0
c Reading order: i varies fastest (left to right)
c But lattice is 3×3, so should be i=0:2, j=0:2
```

**Fix:** Match FILL indices to actual lattice dimensions

### Error 9: Universe Fill Error

**Symptom:** "universe not found" or lost particles in filled cell

**Cause:** FILL references undefined universe

**Example:**
```
1  0  -1  FILL=5  IMP:N=1
c ERROR: No cells with U=5 defined
```

**Fix:** Define universe 5
```
10  1  -10.5  -10  U=5  IMP:N=1
```

### Error 10: Void Cell Without IMP:N=0

**Symptom:** Particles wander forever, simulation doesn't end

**Cause:** Outermost void cell has IMP:N=1 instead of 0

**Example:**
```
9999  0  100  IMP:N=1      $ Should terminate particles
```

**Fix:** Set importance to zero
```
9999  0  100  IMP:N=0      $ Graveyard
```

---

## Validation Checklist (Before Production Runs)

Use this checklist EVERY TIME before running expensive simulations:

### Geometry Validation
- [ ] VOID card test completed (10k particles, no lost particles)
- [ ] Geometry plotted in 3 planes (X-Y, X-Z, Y-Z)
- [ ] No black regions in plots (undefined geometry)
- [ ] Cell labels match expected layout
- [ ] All surfaces referenced in cells are defined
- [ ] Graveyard cell exists with IMP:N=0

### Material and Physics Checks
- [ ] All material numbers in cells have M cards defined
- [ ] Density signs correct (negative for g/cm³)
- [ ] IMP:N specified for all cells and all MODE particles
- [ ] Temperature (TMP) specified if needed
- [ ] NONU specified if using SSR with fissionable materials

### Source and Tally Checks
- [ ] Source definition reasonable (position inside geometry)
- [ ] Tally cells exist and are correct cells
- [ ] Energy bins appropriate for problem
- [ ] F4 tallies have VOL specified for cells

### Small Particle Test
- [ ] Run with NPS=1000 completes successfully
- [ ] No fatal errors or lost particles
- [ ] Tallies have non-zero values (particles reaching detectors)
- [ ] Run time reasonable (seconds to minutes for 1k particles)

---

## 10-Step Debugging Workflow (When Errors Occur)

1. **Read error message carefully** - Note cell, surface, position, error code
2. **Plot geometry at error location** - Use `origin` and `extent` to zoom in
3. **Check surface definition** - Is surface where you expect?
4. **Check cell geometry** - Does Boolean expression include all needed surfaces?
5. **Look for gaps** - Is there a cell on BOTH sides of every surface?
6. **Check for overlaps** - Are two cells claiming same space?
7. **Test simplified geometry** - Remove complexity until error disappears
8. **Add one component at a time** - Rebuild geometry to find error introduction point
9. **Use VOID card** - Verify overall geometry closure
10. **Review with fresh eyes** - Take break, or have colleague review

---

## Prevention Strategies (10 Best Practices)

1. **Build incrementally** - Test each component before adding next
2. **Use consistent numbering** - Cells 1-99, surfaces 1-99, materials 1-9
3. **Comment everything** - Describe every cell and surface purpose
4. **Plot frequently** - After every major change, plot and check
5. **Use VOID card always** - Before first run of any new geometry
6. **Start with simple test case** - 2×2 lattice before 17×17
7. **Define graveyard first** - Build inward from boundary
8. **Use parentheses in Boolean** - Don't rely on operator precedence
9. **Keep universes simple** - Each universe should be testable alone
10. **Document assumptions** - Note coordinate system, origin location, units

---

## Geometry Debugging Tools Summary

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **VOID card** | Test geometry closure | Before every first run |
| **ip (interactive plot)** | Visual inspection | After building, after changes |
| **basis/origin/extent** | Control plot view | Zooming to error location |
| **label 1 2** | Show cell/surface numbers | Verifying layout matches plan |
| **NPS 1000 test** | Quick particle test | Before expensive production run |
| **runtpe event log** | Replay lost particle | Diagnosing specific lost particle |
| **Manual surface evaluation** | Find which cell particle should be in | Confirming gap vs overlap |

---

## Quick Reference: Plotting Commands

```
mcnp6 inp=myfile.inp ip         $ Start interactive plotting

> basis  0 0 1                  $ Set view direction (X-Y plane)
> origin 0 0 0                  $ Set plot center
> extent 20 20                  $ Set plot size (±20 cm)
> px  0  600 600                $ Plot X-Y plane, 600×600 pixels

> py  0  600 600                $ Plot X-Z plane (side view)
> pz  0  600 600                $ Plot Y-Z plane (front view)

> label 1 2                     $ Show cell and surface labels
> color  2                      $ Color by material
> color  1                      $ Color by cell importance

> origin 10.5 5.2 100           $ Move to lost particle location
> extent 5 5                    $ Zoom in to ±5 cm region
> px  100  800 800              $ High-resolution plot at error

> end                           $ Exit plotting, start run
```

---

## Debugging Flowchart

```
START: Run MCNP
    ↓
Fatal error or lost particle?
    ↓ YES
Record: position, cell, surface, error code
    ↓
Plot geometry at error location
    ↓
Is there a gap (missing cell)?
    ↓ YES → Add cell for missing region → Re-run
    ↓ NO
Is there an overlap (multiple cells)?
    ↓ YES → Fix Boolean expression → Re-run
    ↓ NO
Is surface in wrong location?
    ↓ YES → Correct surface definition → Re-run
    ↓ NO
Is Boolean expression wrong?
    ↓ YES → Add parentheses, fix logic → Re-run
    ↓ NO
Check universe/fill/lattice issues
    ↓
Simplify geometry to isolate error
    ↓
Re-run VOID card test
    ↓
SUCCESS → Run production case
```

---

**References:**
- MCNP6 User Manual, Chapter 4: Variance Reduction - VOID card
- MCNP6 User Manual, Chapter 3: Geometry Plotting
- MCNP Primer: "How to Debug Lost Particles"
- See also: boolean_operations_guide.md for Boolean logic errors
- See also: cell_definition_comprehensive.md for cell card syntax
