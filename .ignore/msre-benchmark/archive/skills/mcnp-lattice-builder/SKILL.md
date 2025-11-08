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

**Templates and Examples (assets/ directory):**
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

---

**Version:** 2.0.0
**Documentation:** 8 reference files (~20,000 words), 10 examples, 4 templates, 6 scripts
**Integration Test Ready:** Can translate reactor design specs from literature to functional MCNP lattice model with proper flux-based grouping for accurate physics.
