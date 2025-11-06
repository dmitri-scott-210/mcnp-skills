---
name: mcnp-variance-reducer
description: Implements and optimizes variance reduction techniques in MCNP including cell importance, weight windows, DXTRAN, and iterative WWG optimization for improving simulation efficiency
version: "2.0.0"
dependencies: "mcnp-input-builder, mcnp-tally-builder, mcnp-geometry-builder"
---

# MCNP Variance Reducer

## Overview

This skill guides implementation and optimization of variance reduction (VR) techniques in MCNP simulations. Variance reduction dramatically improves computational efficiency by focusing particle transport toward regions of interest, achieving 10-1000× improvements in Figure of Merit (FOM).

The skill covers cell importance (IMP), weight windows (WWN/WWE/WWP), automated weight window generation (WWG), DXTRAN spheres, and iterative optimization strategies. Proper variance reduction transforms intractable deep penetration problems into manageable simulations.

Understanding the fundamental principle—Monte Carlo conserves expected particle weight through splitting and Russian roulette—is essential for effective VR implementation.

## When to Use This Skill

- Deep penetration shielding calculations (transmission <1e-6)
- Point detector problems far from source (>10 mean free paths)
- Low-probability events (rare reactions, trace material capture)
- Multi-region dose calculations with poor statistics
- Criticality source convergence issues
- Tally relative error >10% despite long run times
- Achieving FOM improvements of 10-1000×
- Converting analog simulations to variance-reduced equivalents
- Iterative WWG optimization across multiple runs
- Diagnosing and fixing failing variance reduction

## Decision Tree

```
What is the simulation challenge?
  |
  +-> Source far from detector (shielding)
  |     |
  |     +-> Simple geometry (<10 regions)
  |     |     └─> Cell importance (IMP) - manual setup
  |     |
  |     +-> Complex geometry (10-100 regions)
  |     |     └─> Weight windows (WWG cell-based)
  |     |
  |     +-> Very complex geometry (>100 regions)
  |     |     └─> Mesh-based WW (MESH + WWG)
  |     |
  |     +-> Thick shield (5-15 MFP)
  |     |     └─> WWG (automatic)
  |     |
  |     └-> Very thick shield (>15 MFP)
  |           └─> WWG + exponential transform (EXT)
  |
  +-> Point detector (small volume)
  |     |
  |     +-> Not too far (<5 MFP)
  |     |     └─> Weight windows (WWG)
  |     |
  |     +-> Far (5-10 MFP)
  |     |     └─> WWG with fine mesh near detector
  |     |
  |     └-> Very far (>10 MFP)
  |           ├─> DXTRAN (deterministic)
  |           └─> WWG + DXTRAN (combined, best)
  |
  +-> Multiple detectors
  |     |
  |     +-> Similar importance
  |     |     └─> Single WWG targeting average
  |     |
  |     └-> Different patterns
  |           └─> Separate runs per detector
  |
  +-> Repeated structures (lattices)
  |     └─> Mesh-based WW (MESH overlays geometry)
  |
  +-> Existing VR failing (FOM decreasing)
  |     ├─> Check weight statistics (min/max ratio)
  |     ├─> Widen WWP parameters (increase wupn)
  |     ├─> Regenerate WWG with more statistics
  |     ├─> Coarsen mesh (if mesh-based)
  |     └─> Simplify (remove aggressive methods like EXT)
  |
  +-> Low-density region issues
  |     └─> Forced collisions (FCL)
  |
  +-> Energy-dependent problem
  |     ├─> Energy-dependent WW (WWE + WWGE)
  |     └─> Energy splitting/roulette (ESPLT)
  |
  +-> Time-dependent problem
        └─> Time splitting/roulette (TSPLT)
```

## Quick Reference

### VR Method Selection

| Problem Type | Primary Method | Expected FOM Gain | When to Use |
|--------------|----------------|-------------------|-------------|
| Simple shielding (1-3 layers) | IMP (cell importance) | 5-20× | Manual setup acceptable |
| Complex shielding | WWG (weight windows) | 20-100× | >10 regions, auto-generate |
| Deep penetration (>10 MFP) | WWG + EXT | 100-1000× | Thick shields, spherical |
| Point detector (close) | WWG | 20-100× | Standard optimization |
| Point detector (far >5 MFP) | DXTRAN + WWG | 50-500× | Line-of-sight to detector |
| Low-density regions | FCL | 5-20× | Air gaps, streaming |
| Energy-specific | WWE (energy-dependent WW) | 10-50× | Thermal vs. fast importance |

### Key Cards

| Card | Purpose | Typical Syntax |
|------|---------|----------------|
| IMP | Cell importance | `IMP:N 1 2 4 8 0` |
| WWG | Generate weight windows | `WWG 5 0 1.0` |
| WWP | Weight window parameters | `WWP:N 5 3 5 0 -1` |
| WWE | Energy-dependent WW | `WWE:N 0 1e-8 1e-6 0.01 20` |
| WWN | Weight window lower bounds | `WWN:N J` (from wwout) |
| DXTRAN | Deterministic to detector | `DXTRAN 1.0 100 0 0 1000` |
| MESH | WWG spatial mesh | `MESH GEOM=XYZ ...` |

## Use Cases

### Use Case 1: Cell Importance (Manual, Simple Geometry)

**Scenario:** Neutron source at center, detector in outer shell, 3 concentric shields. Simple geometry allows manual importance specification.

**Goal:** Increase particle population near detector through geometric importance progression.

**Implementation:**

```
c Cell Cards with importance
1  1  -1.0   -1         IMP:N=1     $ Source (baseline)
2  2  -7.8   1 -2       IMP:N=2     $ Shield 1 (2× importance)
3  3  -11.3  2 -3       IMP:N=4     $ Shield 2 (4×)
4  4  -2.7   3 -4       IMP:N=8     $ Shield 3 (8×)
5  0        4 -5       IMP:N=16    $ Detector (16×)
999  0      5          IMP:N=0     $ Graveyard (killed)

c Surface Cards
1  SO  10              $ Source sphere
2  SO  30              $ Shield 1 outer
3  SO  50              $ Shield 2 outer
4  SO  70              $ Shield 3 outer
5  SO  80              $ Outer boundary

c Data Cards
MODE  N
SDEF  POS=0 0 0  ERG=14.1
F4:N  5               $ Flux in detector
NPS  1e6
```

**Key Points:**
- Importance doubles each region (geometric progression)
- Particles split moving outward (toward detector)
- Graveyard must have IMP=0
- Limit importance ratio to ≤4× between adjacent cells
- FOM improvement: ~10-50× for this simple geometry

**Expected Results:** More particles near detector, reduced variance, FOM = 10-50× analog.

---

### Use Case 2: Weight Window Generation (Automatic, WWG)

**Scenario:** Complex geometry, point detector at (100,0,0). Too complex for manual importance—use automatic WWG.

**Goal:** Generate optimal weight windows automatically from detector flux distribution.

**Two-Stage Workflow:**

**Stage 1 - Generate Weight Windows:**
```
c Geometry definition (same as production)
[... cells and surfaces ...]

c Data Cards
MODE  N
c
c Define importance mesh
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-60 -60 -60
      IMESH=60  IINTS=12
      JMESH=60  JINTS=12
      KMESH=60  KINTS=12
c
c Energy bins for weight windows
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c Point detector
F5:N  100 0 0  0.5
c
c Generate weight windows from F5 tally
WWG  5  0  1.0
c
SDEF  POS=0 0 0  ERG=14.1
NPS  1e5            $ Moderate statistics for WWG
```

**Stage 2 - Production with Weight Windows:**
```
c Same geometry

c Data Cards
MODE  N
c
c Read weight windows from wwout (Stage 1 output)
WWP:N  J  J  J  0  -1
c
c Energy bins (must match Stage 1)
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
F5:N  100 0 0  0.5
SDEF  POS=0 0 0  ERG=14.1
NPS  1e7            $ High statistics with good VR
```

**Key Points:**
- Stage 1 generates wwout file (quick run)
- Stage 2 uses wwout for production (long run)
- Can iterate: use Stage 2 output to regenerate improved wwout
- Typical convergence: 2-5 iterations
- FOM improvement: 20-100× for complex geometries

**Expected Results:** FOM = 20-100× analog, relative error <5%.

---

### Use Case 3: Iterative WWG Optimization

**Scenario:** Optimize weight windows over 3-4 iterations until FOM converges.

**Goal:** Achieve maximum FOM through iterative refinement.

**Iteration Workflow:**

**Iteration 1 (Baseline):**
```
c Generate initial WW
WWG  5  0  1.0
NPS  1e5
c Output: wwout file
c Result: FOM ≈ 1500 (10× improvement over analog)
```

**Iteration 2 (Use WW, regenerate):**
```
c Use previous wwout
WWP:N  J  J  J  0  -1
c Generate improved WW
WWG  5  0  1.0
NPS  2e5
c Output: new wwout (overwrites previous)
c Result: FOM ≈ 4500 (30× improvement, 3× better than iter 1)
```

**Iteration 3 (Converged):**
```
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  5e5
c Result: FOM ≈ 5000 (33× improvement, change <20% → converged)
```

**Convergence Criteria:**
- FOM improvement <20% between iterations
- Detector tally relative error <10%
- Weight window values stable (change <10%)

**Key Points:**
- Each iteration improves accuracy
- Diminishing returns after 3-5 iterations
- Final production run uses converged wwout without WWG card
- Monitor FOM at each iteration

**Expected Results:** 30-50× FOM improvement, <5% relative error, reproducible results.

---

### Use Case 4: Mesh-Based Weight Windows

**Scenario:** Complex geometry with 100+ cells makes cell-based WWN impractical. Use superimposed mesh for automatic importance generation.

**Goal:** Generate weight windows independent of geometry complexity using rectangular or cylindrical mesh.

**Implementation:**

**Stage 1 - Mesh-Based WWG:**
```
c Complex geometry (many cells)
[... cell cards ...]

c Data Cards
MODE  N
c
c Define rectangular mesh overlay
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-100 -100 -100
      IMESH=100  IINTS=20      $ 20 bins in X (5 cm each)
      JMESH=100  JINTS=20      $ 20 bins in Y
      KMESH=100  KINTS=20      $ 20 bins in Z
c     Total: 20×20×20 = 8,000 mesh cells
c
c Energy bins for importance
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c       8 energy groups → 8,000×8 = 64,000 WW entries
c
c Point detector
F5:N  80 0 0  0.5
c
c Generate mesh-based weight windows
WWG  5  0  1.0
c
SDEF  POS=0 0 0  ERG=14.1
NPS  1e5
```

**Stage 2 - Production:**
```
c Same geometry and MESH definition (MUST match!)
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-100 -100 -100
      IMESH=100  IINTS=20
      JMESH=100  JINTS=20
      KMESH=100  KINTS=20
c
c Same energy bins (MUST match!)
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c
c Use mesh-based weight windows
WWP:N  J  J  J  0  -1
c
F5:N  80 0 0  0.5
SDEF  POS=0 0 0  ERG=14.1
NPS  1e7
```

**Key Points:**
- Mesh independent of geometry cells
- Can refine mesh near detector, coarsen elsewhere
- MESH and WWGE must be identical between stages
- Rectangular (XYZ) for Cartesian problems
- Cylindrical (CYL) for cylindrical problems
- Mesh resolution: ~5-20 MFP per bin in penetration direction
- FOM improvement: 50-500× for complex geometries

**Expected Results:** Automatic importance for complex geometries, FOM = 50-500×.

---

### Use Case 5: Exponential Transform for Deep Penetration

**Scenario:** Deep shielding penetration (>15 MFP), detector 500 cm from source through thick concrete/steel. Analog and basic WWG insufficient.

**Goal:** Bias particle transport in preferred direction using exponential transform, combined with weight windows.

**Implementation:**

```
c Geometry: thick shield, detector at x=500
[... cells: source, shield layers, detector ...]

c Data Cards
MODE  N
c
c Exponential transform in shield cells
EXT:N  0.75  2  3  4  5  6
c      ^^p value (0.75 moderate for neutrons in concrete)
c              ^^shield cells where EXT active
c
c Preferred direction toward detector
VECT  1  0  0
c     ^^+x direction
c
c Energy bins for WW
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c CRITICAL: Generate weight windows with EXT active
WWG  5  0  1.0
c
c Detector tally
F5:N  500 0 0  0.5
c
c Source
SDEF  POS=0 0 0  ERG=14.1  VEC=1 0 0  DIR=D1
SI1  -1  0.9999              $ Cone toward detector
SP1   0  1
c
NPS  5e5
```

**Parameter Selection:**
- **Neutrons in concrete/earth:** p = 0.6-0.8
- **Neutrons in steel/lead:** p = 0.7-0.85
- **Photons in high-Z:** p = 0.85-0.95
- **Highly absorbing media:** Higher p (→ 0.9)
- **Scattering media:** Lower p (→ 0.6)

**Two-Stage Workflow:**
1. **Stage 1:** EXT + WWG together (generate wwout)
2. **Stage 2:** EXT + WWP (use wwout) for production

**Key Points:**
- NEVER use EXT without weight windows (causes high-weight pathology)
- EXT works best in 1D or near-1D geometries
- Test p values: start p=0.7, increase if penetration poor
- Monitor weight statistics (max/min ratio should be <1000)
- Iterate WWG 2-3 times with EXT active
- FOM improvement: 100-5000× for deep penetration

**Expected Results:** Deep penetration tractable, FOM = 100-5000×, relative error <5%.

## Integration with Other Skills

### mcnp-tally-builder
Tally design drives VR strategy. Define detector tallies first (F4, F5, FMESH), then design VR to optimize those specific tallies. Energy bins in tallies should match WWE energy structure for energy-dependent VR.

### mcnp-geometry-builder
Geometry affects VR effectiveness. Cell-based importance (IMP) requires well-defined cell structure. WWG mesh should align with geometry. Complex geometries benefit from automatic WWG rather than manual importance.

### mcnp-output-parser
Essential for VR optimization. Extract FOM values, relative errors, weight statistics, and tally fluctuation charts. Track FOM across iterations to verify convergence. Check 10 statistical tests pass.

### mcnp-input-validator
Validate VR configuration before running. Check all cells have importance defined, WWN entries match cells × energy groups, DXTRAN sphere location correct, WWP parameters sensible.

### mcnp-ww-optimizer (Phase 3)
Advanced weight window optimization and tuning. Automatic WWG setup, mesh generation, iterative refinement, and convergence analysis. Use for complex WWG workflows and parameter optimization.

### Typical Workflow
```
1. input-builder: Create basic input (analog)
2. tally-builder: Define detector tallies
3. variance-reducer: Establish baseline FOM (analog run)
4. variance-reducer: Add cell importance or WWG
5. variance-reducer: Iterate WWG 2-5 times
6. output-parser: Extract FOM, verify convergence
7. variance-reducer: Final production run (high statistics)
```

## References

**Fundamental Theory:**
- `variance_reduction_theory.md` - FOM definition, splitting/RR fundamentals, basic weight windows
- `card_specifications.md` - Complete syntax for all VR cards (IMP, WWN, WWE, WWP, WWG, DXTRAN, FCL, EXT, MESH)

**Advanced Theory (Phase 3):**
- `advanced_vr_theory.md` - WWG algorithm, optimization strategies, erratic error diagnosis, overbiasing avoidance
- `mesh_based_ww.md` - MESH card integration, rectangular/cylindrical meshes, resolution guidelines
- `advanced_techniques.md` - Exponential transform (EXT), forced collisions (FCL), energy/time splitting, source biasing

**Workflows and Troubleshooting:**
- `wwg_iteration_guide.md` - Step-by-step WWG iteration workflows, convergence criteria
- `error_catalog.md` - Common VR errors with diagnosis and solutions

**Examples:**
- `example_inputs/` - 6 representative VR problems with comprehensive README
  - Duct streaming (cell importance, WWG)
  - Room geometry (complex multi-region)
  - Maze penetration (deep penetration, WWG essential)
  - Iron detector (point detector, DXTRAN)
  - Gamma lead shield (exponential transform)
  - Dogleg geometry (bent duct)

**Templates and Tools:**
- `templates/` - 3 VR template input files (cell importance, WWG Stage 1/2)
- `scripts/` - 4 Python automation tools (importance calculator, FOM tracker, WWP optimizer, DXTRAN locator)
- `scripts/README.md` - Comprehensive script usage guide

**MCNP6 Manual:**
- Chapter 2.7: Variance Reduction Theory (§2.7.1-2.7.2)
- Chapter 5.11: MESH Card Specification
- Chapter 5.12: Variance Reduction Cards (IMP, WWN, WWE, WWP, WWG, EXT, FCL, DXTRAN)
- Chapter 10.6: Variance Reduction Examples

## Best Practices

1. **Always Start with Analog** - Establish baseline FOM before adding VR. Compare all VR results to analog baseline to verify correctness and measure improvement.

2. **Use WWG, Don't Guess** - Automatic WWG generation is superior to manual WWN specification for complex geometries. Let MCNP calculate optimal importance.

3. **Iterate WWG 2-5 Times** - Each iteration improves weight windows. Diminishing returns after 5 iterations. Monitor FOM convergence.

4. **Monitor FOM Trends** - FOM should remain constant as simulation runs. Decreasing FOM indicates VR parameters incorrect.

5. **Check All 10 Statistical Tests** - VR can bias results if configured incorrectly. Ensure tally passes all statistical checks.

6. **Limit Importance Ratios** - Keep IMP ratio ≤4× between adjacent cells. Large jumps cause excessive splitting overhead.

7. **Match Energy Bins to Physics** - WWE energy structure must align with problem physics (thermal vs. fast). Use 5-20 energy groups typically.

8. **Validate Weight Window Parameters** - Check weight min/max ratio in output. If ratio >100, widen WWP bounds (increase wupn to 10-20).

9. **Combine Methods Carefully** - Test each VR method individually before combining. WWG + DXTRAN powerful but test separately first.

10. **Archive wwout Files** - Save converged weight windows for reproducibility. Document iteration count, target weight, FOM achieved.

---

**For Advanced Topics:** See `error_catalog.md` for troubleshooting, `wwg_iteration_guide.md` for detailed iteration procedures, and `variance_reduction_theory.md` for mathematical foundations.
