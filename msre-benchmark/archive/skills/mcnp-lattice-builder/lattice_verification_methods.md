# Lattice Verification Methods

**Reference for:** mcnp-lattice-builder skill
**Source:** AGR-1 analysis + LATTICE-INFO-SUMMARY.md + best practices
**Created:** 2025-11-04 (Session 16)

---

## OVERVIEW

Lattice verification is CRITICAL before running expensive simulations. Complex nested structures have many opportunities for errors: surface ordering, index mismatches, universe references, volume specifications, and coordinate transformations.

**Golden Rule:** Trust but verify. Always validate lattice geometry before production runs.

---

## VERIFICATION METHOD 1: Geometry Plotting with Index Labels

### Purpose
Visual confirmation that lattice elements appear in correct positions with correct contents.

### Tools
- MCNP built-in plotter
- Visual Editor (VISED)
- Third-party tools (MCNP6-VisEd, Moritz)

### Basic Plotting Command
```
c Add to MCNP input file data block:
c Plot XY plane at Z=0, showing lattice indices

c For MCNP6:
PLOT  PX 0 0 0  EX 0 100 0  OR 0 0 100  SCALE 0.5 LAT=1
```

### Plot Command Parameters

**PX/PY/PZ:** Origin of plot plane
```
PX 0 0 0   $ Plot origin at (0, 0, 0)
```

**EX (extent):** View extent
```
EX -50 50 -50 50   $ View from X=-50 to +50, Y=-50 to +50
```

**OR (orientation):** View direction
```
OR 0 0 1   $ Look down from +Z (XY plane view)
OR 1 0 0   $ Look from +X direction (YZ plane view)
OR 0 1 0   $ Look from +Y direction (XZ plane view)
```

**LAT=1:** Display lattice indices
```
LAT=1   $ Show lattice element indices on plot
```

**COLOR:** Color by material or cell
```
COLOR=MAT    $ Color by material number
COLOR=CELL   $ Color by cell number
```

### Verification Steps

**Step 1: Overview plot**
```
c Full core view, colored by material
PLOT  PX 0 0 0  EX -200 200 -200 200  OR 0 0 1  COLOR=MAT  SCALE 0.3
```
- Verify overall layout (symmetry, pattern)
- Check outer boundaries
- Confirm material distribution

**Step 2: Lattice index plot**
```
c Zoomed view with indices displayed
PLOT  PX 0 0 50  EX -30 30 -30 30  OR 0 0 1  LAT=1  SCALE 1.0
```
- Verify index scheme (i, j, k directions)
- Check indices increase in correct directions
- Confirm FILL array pattern matches plot

**Step 3: Cross-section through lattice**
```
c Vertical cross-section through center
PLOT  PX 0 0 50  EX -100 100 0 100  OR 0 1 0  COLOR=MAT  SCALE 0.5
```
- Verify vertical structure
- Check lattice element heights
- Confirm universe nesting at boundaries

**Step 4: Detail view of single element**
```
c Zoom into single lattice element
PLOT  PX 0.63 0.63 50  EX -0.2 0.2 -0.2 0.2  OR 0 0 1  COLOR=MAT  SCALE 5.0
```
- Verify internal structure of element
- Check for overlaps or gaps
- Confirm material assignments

### Expected Results

**Correct lattice:**
- Indices match intended scheme (e.g., i increases in +X direction)
- FILL array pattern visible in plot (fuel vs control assemblies)
- No gaps between elements
- No overlaps at element boundaries
- Universe cells contained within elements

**Common errors revealed:**
- Indices in wrong direction → surface ordering error
- Elements in wrong positions → FILL array indexing error
- Gaps between elements → lattice spacing error
- Overlaps → universe containment error

---

## VERIFICATION METHOD 2: Volume Calculation Verification

### Purpose
Confirm volume specifications are correct for repeated structures (per-instance, not total).

### Manual Calculation

**For hexahedral lattice (LAT=1):**
```
Element volume = (X_max - X_min) × (Y_max - Y_min) × (Z_max - Z_min)

Example: Lattice element surfaces
  10  PX  -0.63
  11  PX   0.63
  12  PY  -0.63
  13  PY   0.63
  14  PZ  0
  15  PZ  100

Element volume = (0.63 - (-0.63)) × (0.63 - (-0.63)) × (100 - 0)
                = 1.26 × 1.26 × 100
                = 158.76 cm³
```

**For hexagonal lattice (LAT=2):**
```
Hexagonal prism volume = (√3/2) × pitch² × height

Example: Hexagonal element with pitch = 21.5 cm, height = 100 cm
  Volume = (√3/2) × 21.5² × 100
         = 0.866 × 462.25 × 100
         = 40,039 cm³
```

### VOL Specification Check

**Rule:** VOL on universe cell = volume of SINGLE instance (not total across all instances)

**Example:**
```
c Fuel pin in lattice (10 cm³ per pin)
1  1  -10.0  -1  U=1  VOL=10  IMP:N=1  $ VOL = single pin volume

c If 100 pins in lattice:
c   Total fuel volume = 10 cm³ × 100 = 1000 cm³
c   But VOL card still says 10 (per instance)
```

### MCNP Volume Calculation

**Let MCNP calculate volumes automatically:**
```
c Add to data block:
VOL  NO  $ Tell MCNP to calculate volumes

c Run with VOID card to check:
VOID
```

**MCNP output will show:**
- Per-cell volumes
- Number of instances
- Total volume across all instances

**Verification:** Compare MCNP-calculated vs hand-calculated volumes.

### Volume Report Analysis

**Check MCNP output file for:**
```
cell   1 volume = 3.1416E+00 (fuel)
       instances = 289 (17×17 lattice)
       total = 9.0788E+02 cm³

cell   100 volume = 1.5876E+02 (lattice element)
       instances = 289
       total = 4.5882E+04 cm³
```

**Verification checklist:**
- [ ] Single element volume matches hand calculation
- [ ] Number of instances matches lattice dimensions
- [ ] Total volume reasonable for geometry
- [ ] Volume ratios match material fractions

---

## VERIFICATION METHOD 3: Simplified Reference Case Comparison

### Purpose
Validate lattice approach against explicit geometry or simplified model with known solution.

### Method

**Step 1: Build simplified reference**
```
c Reference: 3×3 array of pins (explicit, no lattice)
c Fuel pins at 9 positions, explicitly defined

1  1  -10.0  -1               IMP:N=1  $ Pin 1 at (0, 0)
2  1  -10.0  -2  TRCL=(1.26 0 0)  IMP:N=1  $ Pin 2 at (1.26, 0)
3  1  -10.0  -3  TRCL=(2.52 0 0)  IMP:N=1  $ Pin 3 at (2.52, 0)
... [9 pins total, explicit positions]

1  CZ  0.4   $ Pin 1 fuel radius
2  CZ  0.4   $ Pin 2 fuel radius
... [9 surface definitions]
```

**Step 2: Build lattice version**
```
c Lattice: 3×3 array using repeated structures
1  1  -10.0  -1  U=1  IMP:N=1  $ Fuel pin universe

100  RPP  -0.63  0.63  -0.63  0.63  0  100   $ Element
200  0  -100  U=10  LAT=1  FILL=0:2 0:2 0:0  1 1 1 1 1 1 1 1 1

1000  0  -1000  FILL=10  IMP:N=1   $ Fill into real world
```

**Step 3: Compare results**
```
Run both models with identical source, tallies:
  - k-effective (criticality)
  - Flux distribution
  - Reaction rates
  - Dose rates
```

**Expected:** Results match within statistical uncertainty

**If mismatch:**
- Check lattice surface ordering
- Verify FILL array indices
- Confirm volume specifications
- Check universe containment

### AGR-1 Verification Exercise Example

**From AGR-1 paper (Fairhurst-Agosta & Kozlowski, 2024):**

Three approaches tested on 8×8 pin array:

**Approach 1: Explicit cells (no lattice)**
- 64 pins, each with unique cell definitions
- Result: Gamma source intensity = 100% (reference)

**Approach 2: Whole-core grouping (single universe)**
- All 64 pins as single depletion universe
- Result: 115.6% (15.6% error) - UNACCEPTABLE

**Approach 3: Assembly-level grouping (flux zones)**
- 4 groups based on expected flux levels
- Result: 104.3% (4.3% error) - ACCEPTABLE

**Lesson:** Lattice must use flux-based grouping for accuracy in burnup/activation calculations.

---

## VERIFICATION METHOD 4: Particle Tracking Verification

### Purpose
Confirm particles transport correctly through lattice hierarchy without being lost.

### Method 1: Short Test Run

**Run MCNP with:**
```
NPS  1000   $ Small number of particles (test only)
PRINT  110  $ Print summary tables
```

**Check output for:**
```
0 particles lost   $ Should be zero
All source particles tracked successfully
No "BAD TROUBLE" messages
No "lost particle" warnings
```

**If particles lost:**
- Universe cells not fully contained
- Gaps in geometry
- Transformation errors

### Method 2: Particle History Tracking

**Enable detailed tracking:**
```
c Track 10 particles in detail
PTRAC  FILE=ASC  EVENT=BNK  WRITE=POS  MAX=10
```

**Output shows:**
- Particle position at each event
- Cell number and universe
- Boundary crossings
- Coordinate transformations

**Manual verification:**
- Trace particle path through lattice
- Verify coordinates transform correctly at universe boundaries
- Check particle stays within valid geometry

### Method 3: VOID Card Check

**Add VOID card:**
```
VOID   $ Check for geometry voids
```

**MCNP performs extra checks:**
- Samples random points throughout geometry
- Identifies points not assigned to any cell
- Reports void regions

**Clean output:**
```
No voids found in geometry
```

**If voids found:**
- Gap in universe cells
- Lattice element not fully covered
- Background cell missing

---

## VERIFICATION METHOD 5: Cross-Section Visualization

### Purpose
Check lattice structure in multiple planes to catch errors not visible in single view.

### Recommended Cross-Sections

**XY Plane (looking down):**
```
PLOT  PX 0 0 0  EX -100 100 -100 100  OR 0 0 1  LAT=1
PLOT  PX 0 0 50  EX -100 100 -100 100  OR 0 0 1  LAT=1
PLOT  PX 0 0 100  EX -100 100 -100 100  OR 0 0 1  LAT=1
```
- Verify lattice pattern (fuel vs control assemblies)
- Check indices at different Z heights
- Confirm pattern consistent vertically

**XZ Plane (side view, Y=0):**
```
PLOT  PX 0 0 50  EX -100 100 0 200  OR 0 1 0  COLOR=MAT
```
- Verify vertical structure
- Check lattice element heights match
- Confirm top and bottom boundaries

**YZ Plane (side view, X=0):**
```
PLOT  PX 0 0 50  EX -100 100 0 200  OR 1 0 0  COLOR=MAT
```
- Verify symmetry (if expected)
- Check vertical alignment
- Confirm edge boundaries

**Diagonal cross-sections:**
```
c 45° angle through lattice
PLOT  PX 0 0 50  EX -100 100 -100 100  OR 1 1 0  COLOR=MAT
```
- Catch diagonal gaps or overlaps
- Verify corner elements correct

### What to Look For

**✓ Correct:**
- Clean boundaries between elements
- No white gaps (voids)
- Consistent pattern across planes
- Symmetric if geometry should be symmetric
- Materials in expected locations

**✗ Errors:**
- White spaces (geometry voids)
- Overlapping colors (geometry overlaps)
- Asymmetry where symmetry expected
- Wrong materials in elements
- Inconsistent vertical structure

---

## VERIFICATION METHOD 6: Flux Spatial Distribution Check

### Purpose
Verify lattice grouping strategy produces physical flux distribution.

### Method

**Step 1: Run criticality calculation**
```
KCODE  10000 1.0 25 125   $ 125 cycles, skip first 25
```

**Step 2: Set up mesh tally**
```
FMESH4:N  GEOM=XYZ  ORIGIN=-100 -100 0
          IMESH=100  IINTS=20
          JMESH=100  JINTS=20
          KMESH=200  KINTS=4
```

**Step 3: Analyze flux distribution**
- Plot flux map across core
- Check for expected spatial effects:
  - Peak flux in core center (PWR)
  - Lower flux at core periphery
  - Flux depression near control assemblies
  - Symmetric pattern (if core symmetric)

**Physical expectations:**
```
For PWR core:
  - Center assemblies: Flux ~1.2-1.4 × average
  - Edge assemblies: Flux ~0.6-0.8 × average
  - Near control rods: Flux ~0.3-0.5 × average
```

**If spatial effects wrong:**
- Grouping too coarse (whole-core single universe)
- Universe assignments incorrect
- Material densities wrong
- Control rod positions incorrect

### AGR-1 Verification Example

**Problem:** Initial model showed 15.6% error in gamma source intensity

**Root cause:** All compacts grouped as single depletion universe (no flux spatial effects)

**Solution:** Flux-based grouping (72 independent universes for 72 compacts)

**Result:** Error reduced to 4.3% (acceptable)

**Lesson:** Group by flux zone, not geometric convenience.

---

## VERIFICATION METHOD 7: Material Inventory Check

### Purpose
Confirm total material masses/volumes match design specifications.

### Method

**Step 1: Calculate expected inventory**
```
Example: 17×17 PWR assembly with 264 fuel pins
  - Fuel pin volume: 10 cm³ (per pin)
  - Total fuel volume: 264 × 10 = 2,640 cm³
  - UO2 density: 10.5 g/cm³
  - Total fuel mass: 2,640 × 10.5 = 27,720 g = 27.72 kg
```

**Step 2: Extract from MCNP output**
```
c MCNP output file shows:
material   1 (fuel)    density = 10.5 g/cm³
                       volume = 2640 cm³
                       mass = 27720 g
```

**Step 3: Compare**
- Hand-calculated vs MCNP-calculated volumes
- Expected vs actual material masses
- Cross-check with design specifications

**Verification checklist:**
- [ ] Total fuel volume matches design
- [ ] Cladding mass reasonable
- [ ] Coolant/moderator volume matches
- [ ] Control material inventory correct
- [ ] Structural material masses reasonable

---

## VERIFICATION METHOD 8: Benchmark Against Published Results

### Purpose
Validate model produces results consistent with literature for same geometry.

### Method

**Step 1: Find published benchmark**
- ICSBEP (International Criticality Safety Benchmark Evaluation Project)
- Reactor physics papers with reported k-effective
- Experimental data for dose rates, flux distributions

**Example:** AGR-1 published results
- Gamma source intensity: 11.2 R/hr (reported)
- k-effective: Not reported (subcritical experiment)
- Flux distribution: Qualitative description

**Step 2: Replicate geometry as closely as possible**
- Match dimensions from literature
- Use reported material compositions
- Apply same source definition

**Step 3: Compare results**
```
k-effective (if available):
  - Published: 1.0234 ± 0.0003
  - MCNP:      1.0239 ± 0.0015
  - Difference: 0.05% (within uncertainty) ✓

Gamma dose rate:
  - Published: 11.2 R/hr
  - MCNP:      11.7 R/hr
  - Difference: 4.5% (reasonable) ✓
```

**Acceptable differences:**
- k-effective: <0.5% (0.5 mk or 500 pcm)
- Reaction rates: <5%
- Flux distributions: <10% point-by-point
- Dose rates: <10%

**If larger differences:**
- Check geometry discrepancies
- Verify material compositions
- Confirm cross-section libraries match
- Check source definition

---

## VERIFICATION CHECKLIST

**Before production runs, verify:**

### Geometry Structure
- [ ] Geometry plots from 3 orthogonal directions
- [ ] Lattice index labels match intended scheme
- [ ] Cross-sections through multiple planes clean (no voids/overlaps)
- [ ] Single element detail view shows correct internal structure

### Volume and Mass
- [ ] Hand-calculated element volume matches MCNP
- [ ] VOL specifications are per-instance (not total)
- [ ] Total material masses match design specifications
- [ ] Material inventory reasonable for geometry size

### Universe Hierarchy
- [ ] Hierarchy diagram documented in input comments
- [ ] FILL references point to existing universes
- [ ] No circular universe references
- [ ] All universe cells bounded (no infinite cells touching boundaries)

### Particle Tracking
- [ ] Short test run (1000 particles) completes with zero lost particles
- [ ] VOID card check finds no geometry voids
- [ ] Particle history tracking shows correct coordinate transformations

### Physics Validation
- [ ] Flux spatial distribution matches physical expectations
- [ ] Flux-based grouping used (not whole-core single universe)
- [ ] Material inventory matches design specifications
- [ ] Results comparable to published benchmarks (if available)

### Simplified Reference
- [ ] Simplified test case (few elements) validated against explicit geometry
- [ ] Results match within statistical uncertainty
- [ ] Scaling to full problem verified incrementally

---

## WHEN TO USE EACH METHOD

| Method | Use When | Time Required | Reliability |
|--------|----------|---------------|-------------|
| Geometry plotting | Always | 5-10 min | High - catches 80% of errors |
| Volume verification | Always | 10-15 min | High - catches volume errors |
| Simplified reference | Complex hierarchies | 1-2 hours | Very high - validates approach |
| Particle tracking | Lost particle errors | 30 min | High - identifies containment issues |
| Cross-section views | Suspected overlaps/gaps | 15-20 min | High - catches 3D issues |
| Flux spatial check | Burnup/activation | After first run | Medium - physics-level validation |
| Material inventory | Critical calculations | 30 min | High - confirms total material |
| Benchmark comparison | Final validation | 2-4 hours | Very high - literature agreement |

---

## DEBUGGING WORKFLOW

**If verification reveals errors:**

### Step 1: Geometry Plotting Issues
```
Issue: Lattice indices in wrong direction
Fix: Check surface ordering on LAT cell card

Issue: Elements in wrong positions
Fix: Check FILL array indexing (i-fastest ordering)

Issue: Gaps between elements
Fix: Check lattice element dimensions vs pitch
```

### Step 2: Volume Calculation Issues
```
Issue: Volumes don't match hand calculation
Fix: Check surface definitions, verify element boundaries

Issue: Total volume unreasonable
Fix: Check number of instances, verify VOL is per-instance

Issue: Material masses wrong
Fix: Check density specifications, verify material assignments
```

### Step 3: Particle Tracking Issues
```
Issue: Lost particles
Fix: Check universe cell containment, add background cells

Issue: Voids found by VOID card
Fix: Add cells to cover all space in universe

Issue: Particles cross boundaries incorrectly
Fix: Check coordinate transformations, verify TRCL specifications
```

---

## SUMMARY

**Essential verification steps (always do):**
1. **Geometry plotting** with lattice indices (5-10 min)
2. **Volume verification** against hand calculations (10 min)
3. **Short test run** (1000 particles, check for lost particles) (5 min)
4. **Cross-section views** from 3 orthogonal directions (15 min)

**Additional verification (for critical calculations):**
5. **Simplified reference case** comparison (1-2 hours)
6. **Flux spatial distribution** check (after first run)
7. **Material inventory** verification (30 min)
8. **Benchmark comparison** if available (2-4 hours)

**Total time for essential verification: ~30-45 minutes**

**ROI:** Prevents wasted days/weeks on runs with incorrect geometry. Always worth the investment.

**Golden Rule:** If you're not confident enough to bet your reputation on the geometry being correct, it's not verified enough. Keep checking until you're certain.

---

**END OF LATTICE_VERIFICATION_METHODS.MD**
