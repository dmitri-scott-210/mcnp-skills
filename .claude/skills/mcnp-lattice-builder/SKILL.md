---
name: mcnp-lattice-builder
description: Build MCNP repeated structures (U/LAT/FILL) for reactor cores, fuel assemblies, and complex geometries with hierarchical organization; essential for reactor-to-MCNP translation and flux-based grouping
version: 2.0.0
dependencies: mcnp-geometry-builder, mcnp-material-builder
---

# MCNP Lattice Builder

## Overview

The MCNP Lattice Builder skill guides construction of repeated structure geometries using the universe/lattice/fill methodology (U, LAT, FILL cards). This is essential for modeling reactor cores where hundreds or thousands of identical components (fuel pins, TRISO particles, assemblies) must be represented efficiently. A single fuel pin universe can be replicated 17×17 times in an assembly, then that assembly replicated 15×15 times in a core - all with minimal input.

Beyond geometric efficiency, proper lattice construction is CRITICAL for accurate reactor physics. The skill emphasizes flux-based grouping strategies that prevent 15%+ errors in burnup and activation calculations. It demonstrates translating reactor design specifications from literature into MCNP lattice models, essential for the integration test goal of building full reactor models from design specs alone.

Lattices provide memory and input file savings but NO speed benefit in MCNP. The primary value is maintainability (change pin design once, affects all instances) and accuracy (flux-based grouping for independent depletion tracking).

## When to Use This Skill

- Building reactor core geometry with repeated fuel assemblies (PWR, BWR, HTGR)
- Modeling HTGR TRISO particle distributions in fuel compacts (double heterogeneity)
- Creating pin-by-pin fuel assembly lattices (17×17, 19×19 arrays)
- Translating reactor design specifications from literature to MCNP input
- Setting up flux-based grouping for burnup/activation calculations (preventing 15%+ errors)
- Debugging lattice indexing errors (surface ordering, FILL array mismatches)
- Verifying universe hierarchy and nesting (up to 20 levels allowed)
- Optimizing large repeated geometries for memory usage

## Decision Tree

```
Need repeated geometry?
  ↓
Single repeated element or array?
  ├→ Single → Use U + FILL (single universe number)
  └→ Array → Continue
       ↓
  Rectangular or hexagonal arrangement?
       ├→ Rectangular → LAT=1 (6 surfaces: ±X, ±Y, ±Z)
       └→ Hexagonal → LAT=2 (8 surfaces: 6 hex sides + 2 top/bottom)
            ↓
       All elements identical?
            ├→ Yes → FILL=n (single universe fills all)
            └→ No → FILL array (specify dimensions + values)
                 ↓
            Need transformations (rotations/translations)?
                 ├→ Yes → Add TRCL to filled cell
                 └→ No → Continue
                      ↓
                 Multiple hierarchy levels?
                      ├→ Yes → Nested universes (U/FILL recursion)
                      └→ No → Complete
                           ↓
                      Burnup/activation calculation?
                           ├→ Yes → FLUX-BASED GROUPING REQUIRED
                           └→ No → Any grouping acceptable
                                ↓
                           Verify surface ordering and indices
                                └→ Use geometry plotter with LAT=1 option
```

## Quick Reference

| Concept | Card Example | Notes |
|---------|-------------|-------|
| Universe assignment | `U=1` | Assign cell to universe 1 |
| Lattice type | `LAT=1` | 1=hexahedral (rectangular), 2=hexagonal prism |
| Fill single | `FILL=2` | All elements filled with universe 2 |
| Fill array | `FILL=0:2 0:1 0:0`<br>`1 2 3`<br>`4 5 6` | i varies fastest (Fortran order) |
| Transformation | `TRCL=5` or `(x y z ...)` | Reference TR5 or inline |
| Surface order LAT=1 | `-10 11 -12 13 -14 15` | Defines i(X), j(Y), k(Z) directions |
| Surface order LAT=2 | `-10 11 ... -16 17` | 6 hex sides + 2 top/bottom |
| Volume spec | `VOL=0.503` | Per-instance volume (NOT total) |

**CRITICAL:** Surface ordering on LAT cell card defines lattice indexing scheme (most common error source).

## Use Cases

### Use Case 1: Simple 3×3 Fuel Assembly

**Scenario:** Model 3×3 array of identical fuel pins in water.

**Goal:** Basic rectangular lattice demonstration.

**Implementation:**
```
c Universe 1: Fuel pin (repeated element)
1  1  -10.0  -1      U=1  IMP:N=1  VOL=0.503   $ Fuel
2  0         1  -2   U=1  IMP:N=1  VOL=0.053   $ Gap
3  2  -6.5    2  -3  U=1  IMP:N=1  VOL=0.236   $ Clad
4  3  -1.0    3      U=1  IMP:N=1  VOL=1.261   $ Water

c Universe 10: 3×3 Lattice
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1

c Real World: Container filled with lattice
1000  0  -1000  FILL=10  IMP:N=1
1001  0  1000  IMP:N=0

c Surfaces
1  CZ  0.4     $ Fuel radius
2  CZ  0.42    $ Gap outer
3  CZ  0.475   $ Clad outer
10  PX  0.0    $ Lattice boundaries (3×1.26 = 3.78 cm)
11  PX  3.78
12  PY  0.0
13  PY  3.78
14  PZ  0.0
15  PZ  100.0
1000  RPP  -1 5 -1 5 -1 101  $ Container

c Data Cards
MODE N
M1  92235.80c 0.045  92238.80c 0.955  8016.80c 2.0
M2  40000.80c -0.98
M3  1001.80c 2  8016.80c 1
MT3  LWTR.01T
KCODE 10000 1.0 50 150
KSRC  1.89 1.89 50
PRINT
```

**Key Points:**
- FILL=1 means all 9 elements filled with same universe
- Surface order (-10 11 -12 13 -14 15) defines i in X, j in Y, k in Z
- VOL per instance: 0.503 cm³ fuel (MCNP multiplies by 9 for total)

**Expected Results:** 9 fuel pins, uniform flux distribution, k-eff ~1.0-1.1

### Use Case 2: Reactor Core with Flux-Based Grouping

**Scenario:** 3×3 core with fresh and burned assemblies, need accurate burnup/activation.

**Goal:** Demonstrate flux-based grouping (prevents 15.6% error).

**Implementation:**
```
c Pin universes (same geometry, different materials by burnup)
c Universe 1: Fresh fuel
1  1  -10.5  -1  U=1  IMP:N=1  VOL=0.503
2  3  -1.0    1  U=1  IMP:N=1  VOL=1.26

c Universe 2: Once-burned fuel
11  2  -10.3  -1  U=2  IMP:N=1  VOL=0.503
12  3  -1.0    1  U=2  IMP:N=1  VOL=1.26

c Universe 3: Twice-burned fuel
21  3  -10.1  -1  U=3  IMP:N=1  VOL=0.503
22  3  -1.0    1  U=3  IMP:N=1  VOL=1.26

c Assembly lattices (flux-based grouping: separate U# per zone)
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1  $ Fresh assy
110  0  -10 11 -12 13 -14 15  U=11  LAT=1  FILL=2  IMP:N=1  $ Once-burned
120  0  -10 11 -12 13 -14 15  U=12  LAT=1  FILL=3  IMP:N=1  $ Twice-burned

c Core lattice with flux-based FILL pattern
1000  0  -100 101 -102 103 -104 105  U=100  LAT=1  IMP:N=1  &
        FILL=0:2 0:2 0:0                                       &
             12 11 12                                          &
             11 10 11                                          &
             12 11 12
c Pattern: Fresh (U=10) at center (highest flux)
c          Once-burned (U=11) at middle ring
c          Twice-burned (U=12) at corners (lowest flux)

c Real World
10000  0  -10000  FILL=100  IMP:N=1
10001  3  -0.7  10000 -10001  IMP:N=1  $ Reflector
10002  0  10001  IMP:N=0
```

**Key Points:**
- **CRITICAL:** Each flux zone = independent universe for accurate depletion
- Whole-core grouping (all U=10): 15.6% error in gamma source (AGR-1 study)
- Flux-based grouping (U=10,11,12 by zone): 4.3% error (acceptable)
- Rule: Group by FLUX ZONE, not geometric convenience

**Expected Results:** Accurate spatial flux distribution, correct burnup per zone

### Use Case 3: HTGR TRISO Particle Lattice (4-Level Hierarchy)

**Scenario:** Fuel compact with 6,800 TRISO particles in regular lattice.

**Goal:** Model HTGR double heterogeneity (particle + compact levels).

**Implementation:**
```
c Level 1: TRISO particle (5-layer structure)
1  1  -10.8  -1      U=1  IMP:N=1  VOL=6.54e-6   $ UO2 kernel
2  2  -0.98   1  -2  U=1  IMP:N=1  VOL=1.47e-5   $ Buffer (porous C)
3  3  -1.85   2  -3  U=1  IMP:N=1  VOL=4.19e-6   $ IPyC
4  4  -3.20   3  -4  U=1  IMP:N=1  VOL=5.76e-6   $ SiC
5  5  -1.86   4  -5  U=1  IMP:N=1  VOL=4.56e-6   $ OPyC
6  6  -1.70   5      U=1  IMP:N=1  VOL=5.03e-4   $ Matrix filler

c Level 2: TRISO lattice (10×10×68 = 6,800 particles)
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1

c Level 3: Compact (contains TRISO lattice)
200  0  -200       FILL=10  U=20  IMP:N=1
201  6  -1.70  200 -201  U=20  IMP:N=1  $ Matrix shell

c Level 0: Real World
1000  0  -1000  FILL=20  IMP:N=1
1001  7  -1.74  1000 -1001  IMP:N=1  $ Graphite block

c Surfaces (TRISO layers)
1  SO  0.01750  $ Kernel R
2  SO  0.02750  $ Buffer OR
3  SO  0.03150  $ IPyC OR
4  SO  0.03500  $ SiC OR
5  SO  0.03850  $ OPyC OR

c Lattice element (1.05 mm pitch)
10  PX  0.0
11  PX  1.05    $ 10×0.105 cm
12  PY  0.0
13  PY  1.05
14  PZ  0.0
15  PZ  7.14    $ 68×0.105 cm

c Compact cylinder
200  RCC  0 0 0  0 0 7.14  1.05
201  RCC  0 0 0  0 0 7.14  1.245
```

**Key Points:**
- 4-level hierarchy: Kernel → TRISO → Lattice → Compact
- Regular lattice approximation (vs stochastic URAN) necessary for 6,800+ particles
- VOL specifications per-instance (6.54e-6 cm³ per kernel, ×6800 by MCNP)
- Total fuel: 6,800 × 6.54e-6 = 0.0445 cm³ UO2
- Computational trade-off: <2% error vs exact, but 100× faster

**Expected Results:** Proper TRISO physics, epithermal spectrum, k-eff depends on enrichment

### Use Case 4: Translating Reactor Design Specs to MCNP

**Scenario:** Given paper specifying 17×17 PWR assembly, 1.26 cm pitch, 4.5% enriched fuel.

**Goal:** Demonstrate literature-to-MCNP workflow.

**Information Available (typical):**
- Assembly size: 17×17 pins
- Pin pitch: 1.26 cm
- Fuel enrichment: 4.5% U-235
- Active height: 400 cm
- Guide tube positions: 24 tubes in standard pattern

**Information Missing (must estimate):**
- Exact pin dimensions (use typical: 0.4 cm fuel, 0.475 cm clad)
- Gap size (assume 0.02 cm)
- Densities (use standard: 10.5 g/cm³ UO2, 6.5 g/cm³ Zircaloy)
- Temperatures (estimate from operating conditions)

**Translation Steps:**
1. Define pin universe (fuel/gap/clad/water cells)
2. Calculate lattice boundaries: 17 × 1.26 = 21.42 cm
3. Create 17×17 FILL array with guide tubes at standard positions
4. Add reflector, containment structures
5. Specify materials with available compositions
6. Document assumptions clearly

**Expected Results:** Functional model matching literature geometry, k-eff within 1-2% if assumptions reasonable

### Use Case 5: Debugging Lattice Index Mismatch

**Scenario:** Lattice elements appearing in wrong positions (fuel where control rod expected).

**Goal:** Fix surface ordering to match intended index scheme.

**Diagnostic Process:**
1. Run geometry plotter: `mcnp6 inp=file.i ip`
2. Display lattice indices (LAT=1 option in plotter)
3. Compare shown indices with intended scheme
4. Check surface order on LAT cell card
5. Identify which direction is wrong
6. Reorder surfaces to correct

**Solution:**
```
c WRONG surface order (i and j swapped):
100  0  -12 13 -10 11 -14 15  U=10  LAT=1  FILL=...
         ^  ^   ^  ^   ^  ^
         -Y +Y  -X +X  -Z +Z
         Result: i in Y (WRONG!), j in X (WRONG!)

c CORRECT surface order:
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=...
         ^  ^   ^  ^   ^  ^
         -X +X  -Y +Y  -Z +Z
         Result: i in X (correct), j in Y (correct)
```

**Key Points:**
- Surface order ≠ surface numbering
- Order on cell card determines index directions
- FILL array assumes i-fastest, j-middle, k-slowest
- Geometry plotter essential for verification

## Integration with Other Skills

**Typical Workflow:**
1. **mcnp-input-builder** → Create three-block structure
2. **mcnp-geometry-builder** → Define pin/element geometry (cells, surfaces)
3. **mcnp-material-builder** → Define materials for lattice elements
4. **mcnp-lattice-builder** (THIS SKILL) → Organize into repeated structures
5. **mcnp-source-builder** → Define source in lattice geometry
6. **mcnp-tally-builder** → Set up tallies on lattice elements
7. **mcnp-input-validator** → Verify U/FILL cross-references

**Complementary Skills:**
- **mcnp-geometry-checker:** Verify no overlaps in lattice elements
- **mcnp-cell-checker:** Validate U/FILL references
- **mcnp-transform-editor:** Adjust TRCL transformations for lattices
- **mcnp-burnup-builder:** Set up depletion with flux-based grouping

**Example Complete Workflow:**
```
Project Goal: Full PWR core model with burnup tracking

Step 1: mcnp-input-builder - Create basic structure
Step 2: mcnp-geometry-builder - Define pin geometry (fuel/clad/coolant)
Step 3: mcnp-material-builder - Define UO2, Zircaloy, water materials
Step 4: mcnp-lattice-builder - Create pin lattice → assembly → core hierarchy
Step 5: mcnp-source-builder - Define KCODE criticality source
Step 6: mcnp-tally-builder - Set up flux, power tallies per assembly
Step 7: mcnp-burnup-builder - Configure BURN card with proper grouping
Result: Full core model ready for multi-cycle depletion
```

## References

**Detailed Information (root directory):**
- `lattice_fundamentals.md` (4,200 words): U/LAT/FILL core concepts, surface ordering, Fortran ordering
- `transformations_for_lattices.md` (1,800 words): TR cards, rotation matrices, TRCL
- `universe_hierarchy_guide.md` (1,500 words): Multi-level nesting, negative universe warnings
- `reactor_to_mcnp_workflow.md` (3,800 words): Literature-to-MCNP translation, 9-step process
- `flux_based_grouping_strategies.md` (3,200 words): AGR-1 study, 15.6% vs 4.3% error
- `htgr_double_heterogeneity.md` (4,900 words): TRISO 5-layer structure, regular vs stochastic
- `lattice_verification_methods.md` (1,000 words): Geometry plotting, volume checks
- `common_lattice_errors.md` (1,500 words): Surface ordering, FILL mismatches, lost particles

**Templates and Examples ("" directory):**
- 4 templates: Rectangular, hexagonal, nested, reactor core
- 10 example inputs: Simple (1-3), intermediate (4-6), advanced reactor modeling (7-10)

**Automation Tools (scripts/ directory):**
- `lattice_index_calculator.py`: Visualize index directions from surface ordering
- `fill_array_generator.py`: Generate FILL arrays with correct Fortran ordering
- `universe_hierarchy_visualizer.py`: Parse input and show nesting tree
- `lattice_volume_checker.py`: Verify VOL specifications (per-instance vs total)
- `surface_order_validator.py`: Check LAT cell surface ordering
- `reactor_spec_to_lattice.py`: Template generator from design specs

**External Documentation:**
- MCNP6 Manual Chapter 5.2: Cell Cards (U parameter)
- MCNP6 Manual Chapter 5.5: Geometry Data Cards (LAT, FILL, TRCL)
- MCNP6 Manual Chapter 10.1.3: Repeated Structures Examples

## Best Practices

1. **Always verify surface order on LAT cell card** - This defines index scheme. Use geometry plotter with index labels to confirm before complex modeling.

2. **Group by flux zones, not geometric convenience** - Whole-core as single universe produces 15%+ errors. Group assemblies/regions with similar flux for independent depletion.

3. **Start simple and build incrementally** - Test each level (pin → assembly → core) separately before combining. Easier to debug in stages.

4. **Specify volumes carefully for repeated structures** - VOL must be per-instance (NOT total). Critical for source intensities and tally normalization.

5. **Use negative universe only when absolutely certain** - Cell must be fully enclosed, never truncated. Plot thoroughly and run VOID check. Wrong usage produces silent errors.

6. **Plot, plot, plot** - Geometry plotter is best verification tool. Multiple views, different angles, with lattice indices displayed. Catch errors before expensive runs.

7. **Document universe hierarchy clearly** - Use comments showing nesting structure. Example: "U=1 (pin) → U=10 (assembly) → U=100 (core)".

8. **FILL arrays follow Fortran ordering** - First index (i) varies fastest. Write explicit pattern in comments to avoid confusion.

9. **For reactor models: Use flux-based independent depletion groups** - Each assembly or zone = separate universe for independent flux/depletion. Critical for burnup/activation accuracy.

10. **Verify with simplified reference case** - Before modeling millions of particles, test approach with 10-pin array. Compare explicit vs repeated structures to validate methodology.

## CRITICAL LATTICE CONCEPTS

### Lattice Types in MCNP

MCNP supports TWO lattice types. **ALWAYS specify which type you're building.**

#### LAT=1: Rectangular (Hexahedral) Lattice

- **Coordinate system**: Cartesian grid (x, y, z)
- **Bounding surface**: RPP (rectangular parallelepiped)
- **Pitch**: Element spacing in x, y, z directions
- **Common uses**:
  - PWR fuel assemblies (17×17 pin arrays)
  - BWR fuel bundles
  - Simple reactor cores
  - Vertical stacks
  - TRISO particle arrays

**Example surface**:
```mcnp
100 rpp  xmin xmax  ymin ymax  zmin zmax
```

#### LAT=2: Hexagonal Lattice

- **Coordinate system**: 60° skewed axes
- **Bounding surface**: RHP (right hexagonal prism)
- **Pitch**: R-vector magnitude × √3
- **Common uses**:
  - HTGR cores (hexagonal assemblies)
  - Fast reactor assemblies
  - CANDU fuel bundles
  - Prismatic reactor cores

**Example surface**:
```mcnp
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
100 rhp  0 0 0  0 0 68  0 1.6 0
```

**Key difference**: Hexagonal lattices have staggered rows (60° symmetry), rectangular do not.

### Multi-Level Lattice Hierarchies

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 4**: MCNP supports up to 6 practical levels of nested lattices.

**Example hierarchy** (AGR-1 model):

```
Level 1: TRISO Particle (u=1114)
   └─ 5 concentric spherical shells (kernel, buffer, IPyC, SiC, OPyC)

Level 2: Matrix Cell (u=1115)
   └─ Single cell filled with SiC matrix

Level 3: Particle Lattice (u=1116) - LAT=1 rectangular
   ├─ 15×15×1 array
   ├─ fill=-7:7 -7:7 0:0 (225 positions)
   └─ Circular packing: ~169 particles + ~56 matrix

Level 4: Matrix Filler (u=1117)
   └─ Top/bottom caps for compact

Level 5: Compact Lattice (u=1110) - LAT=1 rectangular
   ├─ 1×1×31 vertical stack
   ├─ fill=0:0 0:0 -15:15
   └─ Pattern: 1117 2R 1116 24R 1117 2R

Level 6: Global Placement
   └─ fill=1110 (x,y,z) transformation
```

**Efficiency**: This represents ~300,000 TRISO particles using ~900 cells (333× reduction).

**Both rectangular AND hexagonal lattices can be nested in same model.**

### FILL Array Dimension Calculation

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 1.2**:

**CRITICAL RULE**:
```
Elements needed = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
```

**This applies to BOTH LAT=1 and LAT=2!**

**Examples**:

```mcnp
fill=-7:7 -7:7 0:0
  I: -7 to 7 → (-7)-(-7)+1 = 15 elements  (count: -7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7)
  J: -7 to 7 → 15 elements
  K: 0 to 0 → 1 element
  Total: 15 × 15 × 1 = 225 elements ✓
```

```mcnp
fill=0:16 0:16 0:0
  I: 0 to 16 → 17 elements  (count: 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
  J: 0 to 16 → 17 elements
  K: 0 to 0 → 1 element
  Total: 17 × 17 × 1 = 289 elements ✓ (17×17 PWR assembly)
```

```mcnp
fill=-6:6 -6:6 0:0
  I: -6 to 6 → 13 elements
  J: -6 to 6 → 13 elements
  K: 0 to 0 → 1 element
  Total: 13 × 13 × 1 = 169 elements ✓ (13×13 hexagonal assembly)
```

**ALWAYS include ZERO when counting negative to positive indices!**

### Repeat Notation (nR)

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 2.2**:

**CRITICAL RULE**: `U nR` = (n+1) total copies, NOT n copies!

**Repeat notation syntax**:
```
U nR  →  U repeated (n+1) times total
```

**Examples**:
```mcnp
100 2R     →  100 100 100           (3 copies total: first + 2 repeats)
200 24R    →  200 (repeated 25 times)
1117 0R    →  1117                  (1 copy: first + 0 repeats)
```

**Full compact lattice example** (from sdr-agr.i):
```mcnp
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

Breakdown:
  fill=0:0 0:0 -15:15  →  1×1×31 = 31 elements needed

  1117 2R   = 3 layers of universe 1117  (bottom cap)
  1116 24R  = 25 layers of universe 1116 (fuel region)
  1117 2R   = 3 layers of universe 1117  (top cap)

  Total: 3 + 25 + 3 = 31 elements ✓
```

**Benefit**: Compact notation for long arrays. Without repeat notation:
```mcnp
c Would require writing:
1117 1117 1117 1116 1116 1116 ... (25 times) ... 1116 1117 1117 1117
c Instead of:
1117 2R 1116 24R 1117 2R
```

**Works identically for rectangular and hexagonal lattices.**

### Index Ordering

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 1.2**:

**CRITICAL RULE**: Arrays filled in **K, J, I** order (K outermost loop, I innermost)

**Applies to BOTH LAT=1 and LAT=2.**

For `fill=-1:1 -1:1 -1:1` (3×3×3 = 27 elements):

```
Position  K   J   I   Element#
--------------------------------
   1     -1  -1  -1      1      ← First element in FILL array
   2     -1  -1   0      2      ← Second element
   3     -1  -1   1      3      ← Third element
   4     -1   0  -1      4
   5     -1   0   0      5
   6     -1   0   1      6
   7     -1   1  -1      7
   8     -1   1   0      8
   9     -1   1   1      9
  10      0  -1  -1     10
  ...     ...  ...     ...
  27      1   1   1     27      ← Last element in FILL array
```

**Reading the FILL array**:
- First line (elements 1-3): K=-1, J=-1, I=-1,0,1
- Second line (elements 4-6): K=-1, J=0, I=-1,0,1
- Third line (elements 7-9): K=-1, J=1, I=-1,0,1
- Fourth line (elements 10-12): K=0, J=-1, I=-1,0,1
- etc.

**For 2D lattices** (k=0:0):
- First row: J=JMIN, I varies from IMIN to IMAX
- Second row: J=JMIN+1, I varies from IMIN to IMAX
- etc.

### Rectangular Lattice (LAT=1) Specifics

**Bounding Surface**: RPP (rectangular parallelepiped)

**Per AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md, section 3.1**:

```mcnp
c RPP: xmin xmax ymin ymax zmin zmax
100 rpp -10.71 10.71 -10.71 10.71 -180 180  $ 17×17 assembly

c Lattice cell using this RPP
200 0  -100  u=200 lat=1  fill=-8:8 -8:8 0:0
     [... 289 universe numbers ...]
```

**Pitch**: Element spacing = (MAX - MIN) / N_elements (in each direction)

**Example**:
```
X-extent: -10.71 to +10.71 = 21.42 cm
Elements: 17
Pitch: 21.42 / 17 = 1.26 cm
```

**Fill pattern**: Straightforward grid (no offsets)

### Hexagonal Lattice (LAT=2) Specifics

**Bounding Surface**: RHP (right hexagonal prism)

**Per input_definition.py, lines 111-124**:

```mcnp
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
{n}13 rhp  0 0 {h}     0 0 68     0  1.6  0

c Lattice cell using this RHP
{n}15 0  -{n}13 u={n}0 lat=2  fill=-6:6 -6:6 0:0
     [... 169 universe numbers in hexagonal pattern ...]
```

**Pitch calculation**:
```
Pitch = R-vector magnitude × √3

Example: R = 1.6 cm
Pitch = 1.6 × 1.732 = 2.77 cm
```

**Fill pattern**: Staggered rows (60° symmetry)

**Visual representation** (indentation is OPTIONAL but helps show pattern):
```mcnp
c Row j=-6 (no indent):
300 300 300 300 300 300 300 300 300 300 300 300 300
c Row j=-5 (indented - offset by half pitch):
 300 300 300 300 300 300 100 100 100 300 300 300 300
c Row j=-4 (no indent):
300 300 300 300 300 100 100 200 100 100 300 300 300
```

**MCNP ignores whitespace** - indentation is for human readability only.

### Circular/Hexagonal Packing Patterns

**Common in reactor models**: Approximate cylindrical or hexagonal geometry using rectangular lattice.

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 2.1**:

**Example: TRISO particles in cylindrical compact** (LAT=1 rectangular)

```mcnp
c Particle lattice (u=1116) - 15×15 rectangular approximating circle
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ 225 positions

c Circular packing pattern (corners = matrix, center = particles):
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115

c Result: ~169 particles (u=1114) + ~56 matrix (u=1115) in circular pattern
c Physical constraint: Fits in cylindrical compact (r=6.35 mm) using square lattice
```

**Pattern benefits**:
- Approximates cylindrical geometry
- Uses efficient rectangular lattice
- Avoids complex curved lattice boundaries

### Universe Hierarchy Validation

**Rules for valid nested lattices** (both LAT=1 and LAT=2):

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 6.2**:

1. ✅ **Define child universes BEFORE parent universes**
   - Universe 100 (pin) defined before universe 200 (assembly using pin)

2. ✅ **No circular references**
   - ❌ WRONG: u=100 fill=200, u=200 fill=100
   - ✅ RIGHT: u=100 (pin), u=200 fill with 100 instances

3. ✅ **All filled universes must exist**
   - If fill array contains "150", universe u=150 must be defined

4. ✅ **Universe 0 is always global**
   - Never define explicitly (u=0 forbidden in cell cards)
   - All top-level cells automatically in universe 0

5. ✅ **Lattice bounding surface must contain N × pitch**
   - For LAT=1: RPP extent = N_elements × pitch (each direction)
   - For LAT=2: RHP must geometrically contain hex pattern

**Example hierarchy validation**:

```
CORRECT order of definition:

c Level 1: Define fuel pin
100 1 -10.2  -1  u=100  $ Fuel
101 2 -6.5   1 -2  u=100  $ Clad
102 3 -1.0   2  u=100  $ Water

c Level 2: Define assembly lattice (uses u=100)
200 0  -10  u=200 lat=1  fill=-8:8 -8:8 0:0
    100 100 100 ... (289 instances of u=100)

c Level 3: Place assembly in global space (uses u=200)
999 0  -10  fill=200
```

## WORKING EXAMPLES

### Example 1: Rectangular Lattice (LAT=1) - PWR Pin Array

**Full 17×17 PWR assembly** (289 fuel pins):

```mcnp
c 17×17 PWR Assembly - Rectangular Lattice Example
c Demonstrates LAT=1 with proper RPP surface sizing
c
c Cells
c
c Fuel pin (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Guide tube (u=101)
110 0       -110          u=101  imp:n=1  $ Void
111 2 -6.5   110 -111     u=101  imp:n=1  $ Tube wall
112 3 -1.0   111          u=101  imp:n=1  $ Water

c Instrument tube (u=102)
120 0       -120          u=102  imp:n=1  $ Void
121 2 -6.5   120 -121     u=102  imp:n=1  $ Tube wall
122 3 -1.0   121          u=102  imp:n=1  $ Water

c Assembly lattice (u=200) - LAT=1 rectangular
c fill=-8:8 -8:8 0:0 → 17×17×1 = 289 elements
200 0  -200  u=200 lat=1  imp:n=1  fill=-8:8 -8:8 0:0
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     100 100 100 101 100 100 100 100 100 100 100 100 100 101 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 101 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 102 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 101 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 101 100 100 100 100 100 100 100 100 100 101 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100

c Global placement
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0  $ Outside world

c
c Surfaces
c
c Pin surfaces (centered at origin for universe)
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
110 cz  0.56  $ Guide tube inner radius
111 cz  0.61  $ Guide tube outer radius
120 cz  0.52  $ Instrument tube inner radius
121 cz  0.57  $ Instrument tube outer radius

c Assembly surface - RPP for LAT=1
c Calculation: 17 elements × 1.26 cm pitch = 21.42 cm extent
c Centered: ±10.71 cm from origin
200 rpp -10.71 10.71 -10.71 10.71 -180 180

c
c Materials
c
m1  $ UO2 fuel, 4.5% enriched
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
m2  $ Zircaloy clad
   40000.60c  1.0
m3  $ Light water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t  $ 350K PWR conditions
```

### Example 2: Hexagonal Lattice (LAT=2) - HTGR Assembly

**COMPLETE 13×13 hexagonal assembly** (ALL 169 elements):

**Per input_definition.py, lines 111-124** (verified complete pattern):

```mcnp
c HTGR Hexagonal Assembly - LAT=2 Example
c Demonstrates hexagonal geometry with RHP surface
c COMPLETE 13×13 pattern (all 169 elements shown)
c
c Cells
c
c Fuel channel (u=100)
100 1 -1.8  -100         u=100  imp:n=1  $ Fuel compact
101 2 -1.7   100 -101    u=100  imp:n=1  $ Graphite channel

c Coolant channel (u=200)
200 3 -5e-3  -102         u=200  imp:n=1  $ Helium
201 2 -1.7    102 -103    u=200  imp:n=1  $ Graphite

c Graphite reflector (u=300)
300 2 -1.7  -104         u=300  imp:n=1  $ Solid graphite

c Assembly lattice (u=400) - LAT=2 hexagonal
c fill=-6:6 -6:6 0:0 → 13×13×1 = 169 elements
c Pitch = R × √3 = 1.6 × 1.732 = 2.77 cm
400 0  -400  u=400 lat=2  imp:n=1  fill=-6:6 -6:6 0:0
     300 300 300 300 300 300 300 300 300 300 300 300 300
      300 300 300 300 300 300 100 100 100 300 300 300 300
       300 300 300 300 300 100 100 200 100 100 300 300 300
        300 300 300 100 100 100 100 100 100 100 100 300 300
         300 300 100 100 100 100 100 100 100 100 100 100 300
          300 100 100 200 100 100 200 100 100 200 100 100 300
           300 100 100 100 100 100 100 100 100 100 100 300 300
            300 100 200 100 100 200 100 100 200 100 300 300 300
             300 100 100 100 100 100 100 100 100 300 300 300 300
              300 100 100 200 100 100 200 100 100 300 300 300 300
               300 100 100 100 100 100 100 100 300 300 300 300 300
                300 300 100 100 100 100 100 300 300 300 300 300 300
                 300 300 300 100 100 100 300 300 300 300 300 300 300

c Note: Visual indentation shows hexagonal stagger (optional formatting)

c Global placement
999 0  -400 fill=400  imp:n=1
1000 0  400  imp:n=0  $ Outside world

c
c Surfaces
c
c Channel surfaces
100 cz  0.6     $ Fuel compact radius
101 cz  0.7     $ Fuel channel outer
102 cz  0.4     $ Coolant channel radius
103 cz  0.5     $ Coolant channel outer
104 cz  0.7     $ Graphite cell radius

c Assembly surface - RHP for LAT=2
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
c      0       0       0         0       0      68       0  1.6  0
c R = 1.6 cm → pitch = 1.6 × √3 = 2.77 cm
400 rhp  0 0 0  0 0 68  0 1.6 0  $ Hex prism, height=68 cm

c
c Materials
c
m1  $ Graphite fuel matrix
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ 600K graphite - REQUIRED!
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ REQUIRED!
m3  $ Helium coolant
    2004.00c  1.0
```

**Pattern breakdown**:
- Row j=-6: All reflector (300)
- Rows j=-5 to -2: Fuel (100) + coolant (200) + reflector (300) mix
- Rows j=-1 to 1: Inner fuel/coolant region
- Rows j=2 to 5: Fuel (100) + coolant (200) + reflector (300) mix
- Row j=6: All reflector (300)

## COMMON PITFALLS AND FIXES

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 10**:

| Pitfall | Example | Fix |
|---------|---------|-----|
| **Dimension mismatch** | fill=0:10, provide 10 elements | Need 11: (10-0+1)=11 |
| **Repeat off-by-one** | fill=0:10, use "U 10R" (=11) | Use "U 9R" for 10 elements |
| **Negative index error** | fill=-5:5, think it's 5 or 10 | It's 11 (include 0!) |
| **Wrong index order** | Assume I,J,K ordering | MCNP uses K,J,I! |
| **RPP for hex lattice** | LAT=2 with RPP surface | Use RHP for LAT=2 |
| **RHP for rect lattice** | LAT=1 with RHP surface | Use RPP for LAT=1 |
| **Hex pitch wrong** | Use R directly as pitch | Pitch = R × √3 |
| **Surface too small** | 15×15 lattice, 14 pitches | Surface = N × pitch |
| **Universe conflict** | Reuse U=100 for different geom | Use unique numbers |
| **Circular fill** | u=100 fill=200, u=200 fill=100 | Define hierarchy bottom-up |
| **Missing universe** | fill array has "150", no u=150 | Define all universes |

## VALIDATION CHECKLIST

Before running MCNP, verify:

- [ ] Lattice type specified: LAT=1 (rectangular) or LAT=2 (hexagonal)
- [ ] Surface type matches: RPP for LAT=1, RHP for LAT=2
- [ ] FILL array element count = (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1)
- [ ] Repeat notation: nR gives (n+1) total copies
- [ ] All filled universes are defined before use
- [ ] No circular universe references
- [ ] Lattice bounding surface matches N × pitch (or N × R×√3 for hex)
- [ ] Child universes defined before parent universes
- [ ] Universe numbers are unique (no conflicts)
- [ ] Index ordering understood (K, J, I)

**Use validation tools**: `scripts/lattice_dimension_calculator.py`

## REFERENCE FILES

For detailed examples and patterns:

- **lattice_patterns_reference.md** - Comprehensive rectangular and hexagonal examples
- **complex_reactor_patterns.md** - Multi-level nesting, mixed lattice types
- **triso_fuel_reference.md** - TRISO-specific patterns (optional supplemental)

---

## WHEN TO USE EACH LATTICE TYPE

### Use LAT=1 (Rectangular) When:

✅ Modeling square/rectangular arrays
- PWR fuel assemblies (17×17, 15×15, etc.)
- BWR fuel bundles
- Simple reactor cores
- Vertical stacks
- TRISO particle arrays (approximating cylinders)

### Use LAT=2 (Hexagonal) When:

✅ Modeling hexagonal arrangements
- HTGR cores
- Fast reactor assemblies
- CANDU fuel bundles
- Any 60° symmetric geometry

### Use Mixed (Both in Same Model) When:

✅ Nesting different geometries
- Hexagonal assemblies with rectangular pin arrays
- Rectangular fuel pins in hexagonal core
- Complex multi-scale reactors

---

**Version:** 2.0.0
**Documentation:** 8 reference files (~20,000 words), 10 examples, 4 templates, 6 scripts
**Integration Test Ready:** Can translate reactor design specs from literature to functional MCNP lattice model with proper flux-based grouping for accurate physics.
