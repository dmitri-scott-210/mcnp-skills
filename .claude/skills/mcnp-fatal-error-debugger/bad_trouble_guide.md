# MCNP BAD TROUBLE Messages Guide

**Purpose:** Comprehensive guide to BAD TROUBLE messages, their causes, and recovery procedures.

**Companion to:** mcnp-fatal-error-debugger SKILL.md

---

## Overview

BAD TROUBLE messages indicate MCNP detected an imminent catastrophic failure and terminated immediately to prevent incorrect results or code crash. These occur during particle transport and typically indicate serious input errors or numerical instabilities.

---

## BAD TROUBLE Characteristics

**When They Occur:**
- During particle transport phase (after input processing)
- MCNP detects potential crash condition
- Immediate termination to prevent undefined behavior

**What They Indicate:**
- Divide by zero
- Array bounds exceeded
- Invalid memory access
- Numerical instability
- User input errors causing code instability

**Key Principle:** BAD TROUBLE is almost always caused by incorrect input, not MCNP bugs.

---

## BAD TROUBLE Categories

### Category 1: Geometry-Related

#### 1.1 BAD TROUBLE in TRACK

**Message:**
```
bad trouble in subroutine track of mcrun
  source particle no.       1234

  particle lost at point:
    x =   5.12345
    y =   3.67890
    z =   0.00000

  in cell    2
```

**Cause:** Geometry error (overlap or gap) detected during particle tracking

**Why BAD TROUBLE:** Particle cannot determine location → undefined behavior imminent

**Fix:** See geometry_error_guide.md for complete procedures

**Quick Actions:**
1. Note lost particle coordinates
2. Plot geometry at that location
3. Identify overlap or gap
4. Fix geometry definition
5. Use VOID card test to verify

---

#### 1.2 BAD TROUBLE in CHKCEL

**Message:**
```
bad trouble in subroutine chkcel of mcrun
  cell    5 definition error
```

**Cause:** Cell definition logically inconsistent or mathematically undefined

**Examples:**
```
c WRONG (impossible to satisfy):
5  1  -1.0  -1 1  IMP:N=1              $ Requires inside AND outside surface 1

c WRONG (complement of nothing):
5  1  -1.0  #999  IMP:N=1              $ Cell 999 doesn't exist
```

**Fix:**
```
c CORRECT:
5  1  -1.0  -1  IMP:N=1                $ Inside surface 1

c CORRECT:
5  1  -1.0  #1  IMP:N=1                $ Complement of cell 1 (which exists)
```

---

### Category 2: Source-Related

#### 2.1 BAD TROUBLE in SOURCC

**Message:**
```
bad trouble in subroutine sourcc of mcrun
  nps =        1
```

**Causes:**
1. Source position outside geometry
2. Source in void cell with IMP=0
3. Source specification produces invalid particle state

**Example 1: Source Outside**
```
c Geometry: Sphere R=10
1  1  -1.0  -1  IMP:N=1
999  0  1  IMP:N=0

c Source (WRONG):
SDEF  POS=20 0 0  ERG=14.1            $ Outside geometry!
```

**Fix:**
```
SDEF  POS=0 0 0  ERG=14.1             $ Inside sphere
```

**Example 2: Divide by Zero in Distribution**
```
c WRONG:
SDEF  CEL=1  ERG=D1
SI1  H  0  0  1                        $ Zero bin width (0 to 0)
SP1     0  1

bad trouble in subroutine source - divide by zero
```

**Fix:**
```
SI1  H  0  0.1  1  10                  $ Non-zero bin widths
SP1     0  1    1  0
```

---

#### 2.2 BAD TROUBLE in KCODE (Criticality)

**Message:**
```
bad trouble in subroutine kcode of mcrun
  no fission neutrons generated
```

**Causes:**
1. KSRC points not in fissile material
2. No fissile material defined
3. Fissile concentration too low

**Example:**
```
c Fuel cell:
1  1  -10.0  -1  IMP:N=1               $ Cell 1

c Material (WRONG - no fissile isotopes):
M1  8016.80c  1.0                      $ Only oxygen!

c KSRC:
KSRC  0 0 0                            $ In cell 1, but no fissile material

bad trouble - no fission source generated
```

**Fix:**
```
M1  92235.80c  0.03  92238.80c  0.97  8016.80c  2.0   $ Add U-235 (fissile)
```

---

### Category 3: Numerical Errors

#### 3.1 Divide by Zero

**Message:**
```
bad trouble in subroutine [name]
  floating point exception - divide by zero
  nps =        5678
```

**Common Locations:**

**Location 1: Source Specification**
```
c Zero volume in volume source:
SDEF  CEL=1  VOL=0  ERG=14.1          $ VOL=0 causes divide by zero

c Zero area in surface source:
SDEF  SUR=1  ARA=0  ERG=14.1          $ ARA=0 causes divide by zero
```

**Fix:**
```
c Let MCNP calculate volume:
SDEF  CEL=1  ERG=14.1                  $ No explicit VOL

c Or specify correct volume:
SDEF  CEL=1  VOL=4188.8  ERG=14.1     $ Volume of sphere R=10
```

**Location 2: Tally Normalization**
```
c Cell volume = 0:
VOL  10  0  30                         $ Cell 2 has zero volume!

c Tally normalized by volume:
F4:N  2                                $ Tally in cell 2
# Result: Divide by zero when normalizing
```

**Fix:**
```
c Calculate volume correctly:
VOL  10  20  30                        $ Non-zero volume

c Or let MCNP calculate:
c (remove VOL card)
```

**Location 3: Weight Window**
```
c Weight window with zero value:
WWN:N  1  0  1  1  ...                $ Second entry = 0 (invalid!)
```

**Fix:**
```
WWN:N  1  0.01  1  1  ...             $ Replace 0 with small positive value
```

---

#### 3.2 Numerical Overflow

**Message:**
```
bad trouble in subroutine [name]
  floating point exception - overflow
```

**Causes:**
1. Extremely large tally result (insufficient particles in small region)
2. Weight window values too extreme
3. Importance ratio too large

**Example:**
```
c Importance too extreme:
IMP:N  1  1e10  1  0                   $ Factor of 1e10 → overflow in splitting
```

**Fix:**
```
c Use geometric progression:
IMP:N  1  10  100  0                   $ More reasonable progression
```

---

#### 3.3 Array Bounds Exceeded

**Message:**
```
bad trouble in subroutine [name]
  array bounds exceeded
  index =   10000000
```

**Causes:**
1. Too many particles generated (splitting out of control)
2. Invalid index calculation (usually from bad geometry)
3. Transformation error producing huge coordinates

**Fix:**
```
c Reduce importance ratio:
IMP:N  1  2  4  0                      $ Instead of 1  1000  1000000  0

c Check transformations for errors
```

---

### Category 4: Weight Window Errors

#### 4.1 BAD TROUBLE in WWG

**Message:**
```
bad trouble in subroutine wwg of mcrun
  particle weight exceeds weight window bounds
```

**Causes:**
1. Weight window values incompatible
2. WWN/WWE inconsistent
3. Mesh dimensions wrong

**Temporary Diagnostic:**
```
c Disable weight windows to test:
c WWP:N  J  J  J  0  -1
c WWN:N  [values]

# If problem disappears, weight windows are cause
```

**Fixes:**
1. Regenerate weight windows with WWINP/WWOUT
2. Check mesh dimensions match geometry
3. Verify WWN lower bounds < WWE upper bounds

---

#### 4.2 BAD TROUBLE in WWGPLT

**Message:**
```
bad trouble in subroutine wwgplt
  weight window mesh inconsistent with geometry
```

**Cause:** WWGE/WWGN mesh doesn't align with geometry

**Fix:**
```
c Verify mesh bounds contain geometry:
WWGE:N  -100  100  10                 $ X boundaries
         -100  100  10                 $ Y boundaries
         -100  100  10                 $ Z boundaries

# Ensure geometry fits within -100 to 100 in each dimension
```

---

### Category 5: DXTRAN Errors

#### 5.1 BAD TROUBLE in DXTRAN

**Message:**
```
bad trouble in subroutine dxtran
  dxtran sphere   1 geometry error
```

**Causes:**
1. DXTRAN sphere overlaps with geometry
2. DXTRAN contribution point outside sphere
3. Multiple DXTRAN spheres overlapping

**Fix:**
```
c Ensure DXTRAN sphere doesn't overlap cells:
DXC  10 0 0  5                         $ Center (10,0,0), radius 5

# Check that sphere (10±5, 0±5, 0±5) doesn't overlap any cell boundaries
# Make sphere smaller or move away from boundaries
```

---

### Category 6: Tally Errors

#### 6.1 BAD TROUBLE in Tally Subroutine

**Message:**
```
bad trouble in subroutine [tally-related]
  tally   4 specification error
```

**Causes:**
1. Tally references undefined surface/cell
2. Tally multiplier references undefined material
3. Energy/time bins invalid

**Example:**
```
c WRONG:
F4:N  999                              $ Cell 999 doesn't exist

c WRONG:
FM4  1.0  10  -6                       $ Material 10 not defined
```

**Fix:**
```
c Correct cell number:
F4:N  1

c Correct material number:
FM4  1.0  1  -6                        $ Material 1 (defined)
```

---

### Category 7: Physics Card Errors

#### 7.1 BAD TROUBLE in Physics Routines

**Message:**
```
bad trouble in subroutine [physics-related]
  physics specification inconsistent
```

**Causes:**
1. PHYS card parameters out of range
2. MODE includes particle type not supported by materials
3. Cutoff energies invalid

**Fix:**
```
c Check PHYS card:
PHYS:N  20 J J J J                     $ Verify energy cutoff reasonable

c Check MODE consistent with materials:
MODE  N P                              $ If photon mode, need photon xsecs
M1  1001.80c  2  8016.80c  1          $ Neutron
     1000.04p  2  8000.04p  1          $ Photon (add if MODE includes P)
```

---

## Recovery Procedures

### Immediate Actions After BAD TROUBLE

**Step 1: Read Error Message**
```
bad trouble in subroutine [NAME] of mcrun
  [additional information]
  nps =        XXXX
```

**Note:**
- Subroutine name (indicates where failure occurred)
- NPS (how many particles ran before failure)
- Additional diagnostic information

---

**Step 2: Check NPS Value**

```
nps = 1          → Immediate failure (likely source error)
nps = 100-1000   → Early failure (likely geometry error near source)
nps = 10000+     → Late failure (rare event, statistical region, or VR issue)
```

**Interpretation:**
- **NPS = 1-10:** Source specification problem
- **NPS = 10-1000:** Geometry error in commonly visited region
- **NPS = 1000+:** Geometry error in rare region OR variance reduction issue

---

**Step 3: Simplify Input**

```
c Create test input with minimal features:

c Test 1: Simplest possible
SDEF  POS=0 0 0  ERG=14.1              $ Simple source
c (remove all variance reduction)
c (use simple geometry)
NPS  1000                               $ Short run

# If works: Problem is in removed complexity

c Test 2: Add back one feature at a time
c Test 3: Continue until error reproduces
# Last added feature likely cause
```

---

**Step 4: Examine Event Log** (if geometry-related)

```
event log of particle        XXXX
  surface     cell    mat     nps
                1      1        XXXX    ← Start
      10        2      2        XXXX    ← Path
      15        ?      ?        XXXX    ← Lost

# Plot surfaces 10 and 15, cells 1 and 2
```

---

**Step 5: Use Diagnostic Cards**

```
c Print more information:
PRINT                                  $ Print all tables

c Debug mode (MCNP6):
DBCN  17  J  J                         $ Debug level 17 (detailed)

c Track specific particles:
NPS  1                                 $ Run only 1 particle
# Examine detailed output
```

---

### Systematic Debugging Workflow

**1. Isolate Error Category**
- Geometry? → See geometry_error_guide.md
- Source? → See source_error_guide.md
- Tally? → Check tally specifications
- VR? → Remove VR cards temporarily
- Physics? → Check PHYS, MODE cards

**2. Create Minimal Reproducing Case**
```
c Start with working input
c Add features one by one
c When error appears, last addition is cause
```

**3. Test with VOID Card** (geometry)
```
c If geometry suspected:
VOID                                   $ Make all cells void
SDEF  SUR=998  NRM=-1                 $ Flood from outside
NPS  10000

# If still fails → geometry error confirmed
```

**4. Check Against Working Example**
```
c Find similar working input
c Compare card by card
c Identify differences
```

**5. Consult Error Catalog**
- fatal_error_catalog.md
- geometry_error_guide.md
- source_error_guide.md

---

## Prevention Strategies

### 1. Validate Before Running

```
c Use mcnp-input-validator skill
c Check:
#  - All cross-references valid
#  - Geometry plotted visually
#  - Source positioned correctly
```

### 2. Build Incrementally

```
c Stage 1: Simple geometry + source → test
c Stage 2: + materials → test
c Stage 3: + tallies → test
c Stage 4: + variance reduction → test
```

### 3. Use Short Test Runs

```
c Before production:
NPS  1000                              $ Short test run

# If succeeds, increase:
NPS  10000                             $ Longer test
NPS  1000000                           $ Production
```

### 4. Plot Everything

```
# Plot from multiple angles
# Check for dashed lines
# Verify cell definitions
# Confirm source location
```

### 5. Start Conservative

```
c Conservative importance:
IMP:N  1  2  4  0                      $ Gentle progression

c Conservative weight windows:
# Start with analog (no VR)
# Add VR incrementally after verifying geometry
```

---

## Platform-Specific BAD TROUBLE

### Windows

**Memory Issues:**
```
bad trouble - insufficient memory

# Increase stack size:
# mcnp6 inp=input.i STACKSIZE=100000000
```

### Linux

**Segmentation Fault:**
```
bad trouble - segmentation fault

# Check ulimit:
ulimit -s unlimited

# Check file permissions
```

### Cluster/MPI

**MPI Communication Errors:**
```
bad trouble in mpi communication

# Check MPI installation:
which mpirun
mpirun --version

# Verify correct MCNP executable:
which mcnp6.mpi
```

---

## Emergency Recovery

### If All Else Fails

**1. Use FATAL Option** (with extreme caution)
```bash
# Forces MCNP to continue despite fatal errors
mcnp6 inp=input.i FATAL

# WARNING: Results may be incorrect
# Use ONLY for diagnosis, never for production
```

**2. Examine Verbose Output**
```
PRINT                                  $ Print everything
DBCN  17  J  J                         $ Maximum debug info
NPS  10                                $ Run few particles

# Examine outp for detailed information
```

**3. Binary Search for Error**
```
c Comment out half the input
# If works, problem in commented half
# If fails, problem in active half
# Repeat until error isolated
```

**4. Ask for Help**
```
# Create minimal reproducing example
# Post to MCNP forum
# Include:
#   - MCNP version
#   - Operating system
#   - Complete input (minimal)
#   - Complete output (through error)
#   - What you've tried
```

---

## Common Patterns

### Pattern 1: Immediate BAD TROUBLE (NPS=1)
**Likely:** Source error
**Action:** Check SDEF, KSRC, SI/SP cards

### Pattern 2: BAD TROUBLE in TRACK
**Likely:** Geometry overlap/gap
**Action:** Plot at lost location, use VOID test

### Pattern 3: BAD TROUBLE with Divide by Zero
**Likely:** Zero volume, area, or bin width
**Action:** Check VOL, SI histograms, weight windows

### Pattern 4: BAD TROUBLE Only with VR
**Likely:** Weight window or importance issue
**Action:** Remove VR, test analog

### Pattern 5: BAD TROUBLE After Many Particles
**Likely:** Rare event in unusual region
**Action:** Examine event log, plot that region

---

## References

- **fatal_error_catalog.md:** Error messages and fixes
- **geometry_error_guide.md:** Geometry debugging procedures
- **source_error_guide.md:** Source specification errors
- **MCNP Manual Chapter 4.8:** Geometry Errors
- **MCNP Manual Chapter 3.5:** Debugging Techniques

---

**END OF BAD TROUBLE GUIDE**
