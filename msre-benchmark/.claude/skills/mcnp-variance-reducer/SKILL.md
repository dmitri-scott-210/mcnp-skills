---
category: B
name: mcnp-variance-reducer
description: Implement and optimize variance reduction techniques in MCNP including importance sampling, weight windows, source biasing, and advanced methods for improving simulation efficiency
activation_keywords:
  - variance reduction
  - weight windows
  - importance sampling
  - split particle
  - russian roulette
  - WWG generation
  - figure of merit
  - optimize efficiency
  - reduce variance
---

# MCNP Variance Reducer Skill

## Purpose

This skill guides users in implementing, configuring, and optimizing variance reduction (VR) techniques in MCNP simulations. Variance reduction methods dramatically improve computational efficiency by focusing particle transport toward regions and energies of interest. This skill covers cell importance, weight windows, source biasing, forced collisions, exponential transforms, DXTRAN, and automated optimization strategies for achieving high figure-of-merit (FOM) values.

## When to Use This Skill

- Deep penetration shielding calculations (thick shields, low transmission)
- Point detector problems (small geometric region far from source)
- Low-probability events (rare reactions, capture in trace materials)
- Multi-region dose calculations (many tallies at various locations)
- Criticality source convergence issues (fission source optimization)
- Poor tally statistics (high relative error >10%)
- Long run times with insufficient statistics
- Iterative optimization of existing variance reduction
- Converting analog simulations to variance-reduced equivalents
- Diagnosing and fixing variance reduction failures
- Achieving FOM improvements of 10-1000×

## Prerequisites

- **mcnp-input-builder**: Understanding of MCNP input structure
- **mcnp-tally-builder**: Knowledge of tally definitions
- **mcnp-geometry-builder**: Understanding of cell structure
- **mcnp-output-parser**: Ability to read FOM and tally statistics
- Understanding of Monte Carlo statistics (mean, variance, relative error)
- Knowledge of particle transport physics basics

## Core Concepts

### Figure of Merit (FOM)

**Definition**:
```
FOM = 1 / (R² × T)
```

**Variables**:
- `R`: Relative error of tally (σ/mean)
- `T`: Computer time (minutes)
- `FOM`: Figure of Merit (higher is better)

**Interpretation**:
- No VR (analog): FOM = baseline
- Good VR: FOM = 10-100× baseline
- Excellent VR: FOM = 100-1000× baseline
- Poor VR: FOM < baseline (VR made things worse!)

**Key Insight**: FOM should remain constant as simulation runs longer (if VR is working correctly)

### Splitting and Russian Roulette

**Splitting** (entering higher importance region):
- Particle with weight w enters cell with importance I_new > I_old
- Split ratio: N = I_new / I_old
- Create N particles, each with weight w/N
- Example: IMP=1→2 splits particle into 2 (weight/2 each)

**Russian Roulette** (entering lower importance region):
- Particle with weight w enters cell with importance I_new < I_old
- Survival ratio: S = I_new / I_old
- Particle survives with probability S, weight becomes w/S
- Example: IMP=2→1 plays roulette (50% survival, weight×2 if survives)

**Conservation**: Expected weight is conserved in both operations

### Weight Windows Mechanics

**Window Bounds**:
```
w_lower = WWN value
w_upper = w_lower × wupn (default: 5×)
w_survive = w_lower × wsurvn (default: 3×)
```

**Actions**:
1. `w < w_lower`: Russian roulette
   - Survive probability: w / w_survive
   - New weight if survives: w_survive

2. `w > w_upper`: Splitting
   - Split into N ≈ w / w_survive particles
   - Each particle weight ≈ w_survive

3. `w_lower ≤ w ≤ w_upper`: No action (particle in window)

**Goal**: Keep particle weights near w_survive for optimal variance

### Importance Function

**Theoretical Optimal**:
```
I(r⃗, E, t) = Expected contribution to tally per unit weight at phase space point
```

**Weight Window Relationship**:
```
w_optimal(r⃗, E) ∝ 1 / I(r⃗, E)
```

**Intuition**:
- High importance region (near detector): Low weight → many particles
- Low importance region (far from detector): High weight → few particles
- Trades particles for weight to maintain statistics

### WWG (Weight Window Generator)

**Algorithm**:
1. Run forward simulation with detector tally
2. Estimate importance from flux ratio: I(r⃗,E) ∝ Φ(r⃗,E) / Φ_detector(E)
3. Calculate weight windows: w_lower = target × Φ_detector / Φ
4. Write to wwout file
5. Subsequent runs use wwout for VR

**Advantages**:
- Automatic (no manual tuning)
- Works for complex geometries
- Iteratively improvable

## Decision Tree: Choosing Variance Reduction Method

```
START: What is the simulation challenge?
  |
  +--> Source far from detector (shielding)
  |      ├─> Simple geometry (few regions)
  |      |    └─> Cell Importance (IMP cards) - manual
  |      |
  |      ├─> Complex geometry (many regions)
  |      |    └─> Weight Windows (WWG automatic)
  |      |
  |      └─> Very thick shield (>10 MFP)
  |           └─> Weight Windows + Exponential Transform
  |
  +--> Point detector (small volume)
  |      ├─> Detector not too far
  |      |    └─> Weight Windows (WWG)
  |      |
  |      └─> Detector very far (>5 MFP)
  |           ├─> DXTRAN (deterministic contribution)
  |           └─> Weight Windows + DXTRAN (combined)
  |
  +--> Multiple detectors (distributed)
  |      ├─> Similar importance patterns
  |      |    └─> Single WWG targeting average location
  |      |
  |      └─> Very different patterns
  |           └─> Separate runs with different WWG per detector
  |
  +--> Low-density region issues (few collisions)
  |      └─> Forced Collisions (FCL card)
  |
  +--> Energy-dependent problem (specific energy range critical)
  |      └─> Energy-dependent weight windows (WWE card)
  |
  +--> Source biasing needed (adjust source distribution)
  |      ├─> Spatial biasing → SDEF with SI/SP distributions
  |      ├─> Energy biasing → SDEF with biased energy spectrum
  |      └─> Direction biasing → SDEF with DIR/VEC parameters
  |
  +--> Existing VR not working (FOM decreasing)
  |      ├─> Check particle population (PRDMP card output)
  |      ├─> Verify WWG converged (run longer WWG stage)
  |      ├─> Check for geometry issues (lost particles)
  |      └─> Simplify VR (remove some methods, re-optimize)
  |
  +--> Criticality problem (KCODE convergence issues)
         ├─> Entropy not converging → More inactive cycles
         ├─> Source shape wrong → Better initial KSRC
         └─> Fission sites clustered → Increase neutrons/cycle
```

## Use Case 1: Cell Importance (Manual, Simple Geometry)

**Scenario**: Source at center, detector in outer shell, 3 concentric shields

**Geometry**:
```
c Source region → Shield 1 → Shield 2 → Shield 3 → Detector → Graveyard
```

**Strategy**: Geometrically increasing importance (×2 each region)

**Implementation**:
```
c Cell Cards
1  1  -1.0   -1         IMP:N=1  $ Source region (baseline)
2  2  -2.3   1 -2       IMP:N=2  $ Shield 1 (2× importance)
3  3  -11.3  2 -3       IMP:N=4  $ Shield 2 (4× importance)
4  4  -7.8   3 -4       IMP:N=8  $ Shield 3 (8× importance)
5  0        4 -5       IMP:N=16  $ Detector region (16× importance)
999  0      5          IMP:N=0   $ Graveyard (killed)

c Surface Cards
1  SO  10                          $ Source sphere
2  SO  30                          $ Shield 1 outer
3  SO  50                          $ Shield 2 outer
4  SO  70                          $ Shield 3 outer
5  SO  80                          $ Outer boundary

c Data Cards
MODE  N
SDEF  POS=0 0 0  ERG=14.1
F4:N  5                            $ Detector tally
NPS  1e6
```

**Expected Results**:
- Particles split as they move outward
- More particles near detector
- FOM improvement: ~10-50× for this geometry

**Key Points**:
- Importance ratio between regions = split/roulette ratio
- Graveyard must have IMP=0
- All particle types need importance (IMP:N, IMP:P, etc.)
- Geometric progression (×2, ×4, ×8) generally works well

## Use Case 2: Weight Windows (Automatic, Mesh-Based)

**Scenario**: Complex geometry, point detector at (100, 0, 0), automatic VR

**Two-Stage Process**:

**Stage 1 - Generate Weight Windows**:
```
Point Detector with WWG
c Cell Cards
[... geometry definition ...]

c Surface Cards
[... surface definition ...]

c Data Cards
MODE  N

c --- Define importance mesh ---
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-50 -50 -50
      IMESH=50  IINTS=10              $ x: -50 to 50, 10 bins
      JMESH=50  JINTS=10              $ y: -50 to 50, 10 bins
      KMESH=50  KINTS=10              $ z: -50 to 50, 10 bins

c --- Energy bins for weight windows ---
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20

c --- Detector tally ---
F5:N  100 0 0  0.5                    $ Point at (100,0,0), R=0.5

c --- Generate weight windows from F5 ---
WWG  5  0  1.0                        $ Tally 5, mesh 0 (MESH card), target=1.0

c --- Source ---
SDEF  POS=0 0 0  ERG=14.1

c --- Run with moderate statistics ---
NPS  1e5                              $ Just for WWG generation
```

**Stage 2 - Use Generated Weight Windows**:
```
Point Detector with WW
c Cell Cards
[... same geometry ...]

c Data Cards
MODE  N

c --- Read weight windows from wwout (Stage 1 output) ---
WWP:N  J  J  J  0  -1                 $ switchn=-1: read from wwout file

c --- Detector tally ---
F5:N  100 0 0  0.5

c --- Source ---
SDEF  POS=0 0 0  ERG=14.1

c --- Full production run ---
NPS  1e7                              $ High statistics with good VR
```

**Key Points**:
- Stage 1: Generate wwout (quick run)
- Stage 2: Use wwout (production run)
- Can iterate: use Stage 2 output to generate improved wwout
- Typical iteration: 2-5 cycles for convergence

## Use Case 3: Iterative Weight Window Optimization

**Scenario**: Optimize weight windows over multiple iterations

**Iteration 1** (Baseline):
```
FOM = 150 (from analog run)
```

**Iteration 2** (First WWG):
```
c Generate initial WW
WWG  5  0  1.0
NPS  1e5
c Output: wwout file
c Result: FOM = 1500 (10× improvement)
```

**Iteration 3** (Use WW, regenerate):
```
c Use previous WW
WWP:N  J  J  J  0  -1
c Generate improved WW
WWG  5  0  1.0
NPS  2e5
c Output: new wwout file (overwrites)
c Result: FOM = 4500 (30× improvement)
```

**Iteration 4** (Converged):
```
c Use previous WW
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  5e5
c Result: FOM = 5000 (33× improvement, converged)
```

**Convergence Criteria**:
- FOM improvement <20% between iterations
- Relative error of detector tally <10%
- Weight window values stable (change <10%)

**Key Points**:
- Each iteration improves WWG accuracy
- Diminishing returns after 3-5 iterations
- Production run uses final wwout without WWG card

## Use Case 4: Energy-Dependent Weight Windows

**Scenario**: Thermal neutron detector, need different VR for different energies

**Implementation**:
```
c --- Energy groups for weight windows ---
WWE:N  0  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c      thermal epithermal fast    high

c --- Weight window lower bounds (cell-based example) ---
c      Cell 1  2    3     4     5 (by cell, by energy group)
WWN:N  1.0    0.8  0.6   0.5   0.4  &    $ Group 1: thermal
       0.8    0.6  0.5   0.4   0.3  &    $ Group 2: epithermal
       0.6    0.5  0.4   0.3   0.2  &    $ Group 3: fast
       0.5    0.4  0.3   0.2   0.1  &    $ Group 4: high energy

c --- Weight window parameters ---
WWP:N  5  3  5  0  0

c --- Thermal detector tally ---
F4:N  5
E4    0  1e-8  1e-6                $ Thermal range
```

**Key Points**:
- WWE defines energy groups
- WWN has entries for each cell × energy group
- Allows different VR strategy per energy range
- Essential for problems with strong energy dependence

## Use Case 5: Exponential Transform (Deep Penetration)

**Scenario**: Very thick shield (>10 MFP), exponential attenuation

**Theory**: Biases particle direction toward detector

**Implementation**:
```
c --- Concentric spheres for EXT ---
c Source at origin, detector at large radius
1  SO  10                          $ Inner sphere
2  SO  30                          $ Intermediate
3  SO  50
4  SO  70
5  SO  100                         $ Detector region

c --- Exponential transform ---
EXT:N  0  1  2  3  4  5  0.9       $ Surfaces, p=0.9
c      ^list of concentric spheres  ^stretching parameter

c --- Detector ---
F5:N  100 0 0  1.0

c --- Source ---
SDEF  POS=0 0 0  ERG=14.1

NPS  1e6
```

**Parameter Selection**:
- `p = 0`: No transform (analog)
- `p = 0.5`: Moderate biasing
- `p = 0.9`: Strong biasing (for thick shields)
- `p = 1`: Maximum biasing (can cause instabilities)

**Key Points**:
- Requires spherical or near-spherical geometry
- Stretches particle paths toward larger radii
- Combine with weight windows for best results
- Not suitable for backscatter problems

## Use Case 6: DXTRAN (Deterministic Transport to Detector)

**Scenario**: Point detector very far from source, deterministic contribution

**Implementation**:
```
c --- DXTRAN sphere at detector ---
DXTRAN  1.0  100 0 0  1000
c       ^R   ^x y z   ^MAX contributions per source particle

c --- Point detector ---
F5:N  100 0 0  0.5

c --- DXC: Which cells contribute to DXTRAN ---
DXC  1  2  3  4  J  J  J           $ Cells 1-4 contribute, rest don't

c --- Source ---
SDEF  POS=0 0 0  ERG=14.1

NPS  1e6
```

**How It Works**:
- Every collision in DXC cells sends deterministic contribution to DXTRAN sphere
- Reduces variance at detector significantly
- MAX limits contributions per source particle

**Key Points**:
- Very effective for point detectors
- Can combine with weight windows
- MAX parameter prevents memory overflow
- DXC=J J J... means all cells contribute (default)

## Use Case 7: Forced Collisions (Low-Density Regions)

**Scenario**: Air gap or void region with rare collisions

**Implementation**:
```
c --- Cell with low-density air ---
10  5  -0.001  -10  IMP:N=1        $ Air (ρ = 0.001 g/cm³)

c --- Forced collisions in air region ---
FCL:N  10                          $ Force collision in cell 10

c --- Air material ---
M5  7014  -0.78  8016  -0.21       $ Air composition

c --- Detector beyond air gap ---
F4:N  20                           $ Tally in cell 20 beyond air
```

**Effect**:
- Particle forced to collide in low-density cell
- Weight adjusted to maintain correct physics
- Reduces long flights through low-density regions

**Key Points**:
- Use for low-density materials (ρ < 0.01 typical threshold)
- Helps when particles stream through without interaction
- Don't use in high-density regions (wastes time)

## Use Case 8: Source Biasing (Spatial and Energy)

**Scenario**: Bias source toward detector direction and relevant energy range

**Spatial Biasing**:
```
c --- Bias source position toward detector ---
SDEF  POS=FPOS  D1  ERG=14.1
SI1   L  0 0 0  10 0 0  20 0 0     $ Three positions
SP1     0.5  0.3  0.2              $ Probabilities (biased toward detector)
c       ^source  ^middle  ^near detector

c --- Bias correction via importance ---
c Cells have adjusted importance to correct bias
```

**Energy Biasing**:
```
c --- Bias source energy toward thermal range ---
SDEF  POS=0 0 0  ERG=FERG  D1
SI1   H  1e-8  1e-6  0.01  1  14   $ Energy bins
SP1  D  0.4   0.3   0.2  0.1      $ Biased toward thermal
c        ^thermal^epithermal^fast

c --- Source bias (SB) card to correct ---
SB1   1.0  1.5  2.0  3.0           $ Correction factors
```

**Key Points**:
- Bias source toward important regions/energies
- MUST correct bias with SB card or importance adjustments
- Uncorrected bias gives wrong answer!
- Test against analog to verify correctness

## Common Errors and Troubleshooting

### Error 1: Decreasing FOM (VR Making Things Worse)

**Symptom**: FOM decreases as simulation runs, final FOM < analog FOM

**Cause**: Variance reduction parameters incorrect (weight windows too aggressive)

**Diagnosis**:
```
c Check tally fluctuation chart in output:
c - If FOM decreases steadily → bad VR
c - If FOM flat or increasing → good VR
```

**Fix**:
```
c Option 1: Adjust WWP parameters (less aggressive)
WWP:N  10  5  5  0  0              $ wupn=10 (wider window)

c Option 2: Regenerate WW with more statistics
NPS  5e5                           $ Increase WWG run length

c Option 3: Simplify (remove some VR)
c Remove EXT or DXTRAN if causing issues
```

### Error 2: No Particles Reaching Detector

**Symptom**: Tally results zero or near-zero, despite variance reduction

**Cause**: Weight windows too restrictive, killing all particles

**Diagnosis**:
```
c Check output for warnings:
c - "All particles killed by weight windows"
c - Tally shows 0 particles contributing
```

**Fix**:
```
c Option 1: Increase target weight in WWG
WWG  5  0  10.0                    $ Higher target → less aggressive VR

c Option 2: Widen weight window bounds
WWP:N  10  5  10  0  0             $ wupn=10, mxspln=10

c Option 3: Use cell importance instead
c Replace WW with simpler IMP cards
```

### Error 3: Weight Window Generation Failed

**Symptom**: wwout file empty or WWG doesn't improve FOM

**Cause**: WWG run too short, flux estimate unreliable

**Fix**:
```
c Increase WWG run statistics
NPS  5e5                           $ Was 1e5, now 5e5

c Check detector tally relative error in WWG run
c Should be <30% for reliable WW generation
```

### Error 4: DXTRAN Sphere Wrong Location

**Symptom**: DXTRAN not improving FOM for point detector

**Cause**: DXTRAN sphere not centered on detector

**Diagnosis**:
```
c Check output for DXTRAN statistics
c - Should show contributions reaching sphere
c - If zero contributions, location wrong
```

**Fix**:
```
c Verify detector and DXTRAN coordinates match
F5:N  100 0 0  0.5                 $ Detector at (100,0,0)
DXTRAN  1.0  100 0 0  1000         $ DXTRAN at same location ✓
```

### Error 5: Importance Discontinuity Issues

**Symptom**: Warning about large importance ratios, poor splitting efficiency

**Cause**: Importance changes too drastically between cells (>4×)

**Example (Bad)**:
```
1  1  -1.0  -1  IMP:N=1
2  1  -1.0  1 -2  IMP:N=100        $ 100× jump! Too large
```

**Fix (Good)**:
```
c Smooth importance gradient
1  1  -1.0  -1      IMP:N=1
2  1  -1.0  1 -2    IMP:N=2
3  1  -1.0  2 -3    IMP:N=4
4  1  -1.0  3 -4    IMP:N=8
5  1  -1.0  4 -5    IMP:N=16
6  1  -1.0  5 -6    IMP:N=32
```

**Rule of Thumb**: Limit importance ratio to ≤4× between adjacent cells

### Error 6: Energy-Dependent VR Not Working

**Symptom**: Some energy ranges have poor statistics despite WWE/WWN

**Cause**: Energy bins in WWE don't match problem physics

**Fix**:
```
c Match WWE bins to problem energy structure
c For thermal problem:
WWE:N  0  1e-8  1e-6  1e-4  0.01  0.1  1  20
c      ^thermal^epi  ^fast

c For fast neutron problem:
WWE:N  0  0.1  1  5  10  14  20
c      ^slow    ^fast range
```

## Integration with Other Skills

### 1. **mcnp-tally-builder**

Tally design drives variance reduction strategy.

**Workflow**:
```
1. tally-builder: Define detector tallies (F5, F4, etc.)
2. variance-reducer: Design VR to optimize tally statistics
3. tally-builder: Add energy bins, dose functions
4. variance-reducer: Add energy-dependent VR (WWE)
```

### 2. **mcnp-output-parser**

Output analysis crucial for VR optimization.

**What to Extract**:
- FOM values (track over iterations)
- Relative errors (target <10%)
- Tally fluctuation charts
- Weight window statistics
- Particle population trends

**Workflow**:
```
1. variance-reducer: Run with VR
2. output-parser: Extract FOM, relative error
3. variance-reducer: Adjust VR parameters
4. Iterate until FOM converged
```

### 3. **mcnp-geometry-builder**

Geometry affects VR effectiveness.

**Considerations**:
- Cell importance requires well-defined cell structure
- WWG mesh should align with geometry
- DXTRAN works best with line-of-sight geometry

**Example**:
```
c Geometry designed for cell importance
c Concentric shells around detector
1  ... -1      IMP:N=1
2  ... 1 -2    IMP:N=2
3  ... 2 -3    IMP:N=4
...
```

### 4. **mcnp-input-validator**

Validate VR configuration before running.

**Checks**:
- All cells have importance defined
- WWN entries match number of cells × energy groups
- DXTRAN sphere location reasonable
- Weight window parameters sensible (wupn > wsurvn > 1)

### 5. **mcnp-source-builder**

Source definition affects VR strategy.

**Patterns**:
- Point source → Use cell importance or WWG
- Distributed source → May need source biasing (SB)
- Surface source (SSW/SSR) → Can combine with VR

### Workflow:
```
1. source-builder: Define source (SDEF, KCODE)
2. variance-reducer: Design VR appropriate for source type
3. Test analog first (baseline FOM)
4. Apply VR (target FOM = 10-100× baseline)
```

## Validation Checklist

Before finalizing variance reduction:

- [ ] Baseline FOM established (analog run)
- [ ] VR method chosen appropriate for problem type
- [ ] Cell importance (if used):
  - [ ] All cells have IMP defined
  - [ ] IMP=0 for graveyard only
  - [ ] Importance ratios ≤4× between adjacent cells
  - [ ] Importance increases toward detector
- [ ] Weight windows (if used):
  - [ ] WWG run completed successfully (relative error <30%)
  - [ ] wwout file generated and non-zero size
  - [ ] WWE bins (if used) match problem energy structure
  - [ ] WWP parameters reasonable (wupn=5, wsurvn=3, mxspln=5)
- [ ] DXTRAN (if used):
  - [ ] Sphere location matches detector
  - [ ] Radius appropriate (1-10 cm typical)
  - [ ] MAX parameter prevents memory overflow (100-1000)
- [ ] Source biasing (if used):
  - [ ] SB correction factors applied
  - [ ] Results match analog (within statistics)
- [ ] Production run results:
  - [ ] FOM stable or increasing
  - [ ] FOM > 5× baseline (minimum)
  - [ ] Relative errors <10% (target <5%)
  - [ ] Tally passes 10 statistical checks
- [ ] Convergence verified:
  - [ ] Multiple iterations show FOM improvement
  - [ ] Final FOM change <20% from previous iteration

## Advanced Topics

### 1. Multi-Detector Optimization

**Challenge**: Multiple detectors with conflicting importance patterns

**Strategy 1 - Compromise WWG**:
```
c Average detector location
F5:N  100 0 0  0.5                 $ Detector 1
F15:N 100 100 0  0.5               $ Detector 2
c Use F5 for WWG (compromise)
WWG  5  0  1.0
```

**Strategy 2 - Separate Runs**:
```
c Run 1: Optimize for detector 1
WWG  5  0  1.0
c Run 2: Optimize for detector 2
WWG  15  0  1.0
```

**Strategy 3 - Mesh Tally Based**:
```
c Use FMESH instead of point detector
FMESH4:N  GEOM=XYZ  ORIGIN=0 0 0  ...
WWG  4  1  1.0                     $ Use FMESH (mesh_id=1)
```

### 2. Hybrid VR (Combining Multiple Methods)

**Example - WW + DXTRAN + EXT**:
```
c Weight windows (base VR)
WWP:N  J  J  J  0  -1

c DXTRAN for distant detector
DXTRAN  1.0  100 0 0  1000

c Exponential transform for deep penetration
EXT:N  0  1  2  3  4  5  0.9
```

**Key**: Methods are complementary, but test individually first

### 3. Weight Window Parameter Tuning

**wupn (Upper Bound Multiplier)**:
- Small (2-3): Narrow window → more splitting/roulette
- Large (10-20): Wide window → less variance reduction
- Default (5): Good starting point

**wsurvn (Survival Weight Multiplier)**:
- Should be: 1 < wsurvn < wupn
- Typical: wsurvn = wupn / 2
- Default (3): Good for wupn=5

**mxspln (Max Splits per Event)**:
- Limits splitting to prevent memory issues
- Too small: Poor VR effectiveness
- Too large: Memory and time overhead
- Default (5): Usually sufficient

### 4. Source Convergence in Criticality (KCODE)

**Challenge**: Fission source not converged, biasing active cycles

**Diagnosis**:
```
c Check Shannon entropy convergence in output
c - Should stabilize after ~20-50 inactive cycles
c - If still trending → need more inactive cycles
```

**Fix**:
```
c Increase inactive cycles
KCODE  10000  1.0  100  200         $ 100 inactive (was 50)

c Better initial source guess
KSRC  0 0 0  10 0 0  -10 0 0  ...  $ Multiple points

c Use mesh-based source (automatic)
c No KSRC → MCNP uses uniform source in fissile cells
```

### 5. Time-Dependent Weight Windows

**Use Case**: Time-dependent problems (pulse response, decay)

**Implementation**:
```
c Time bins for weight windows
WWT:N  0  1e2  1e3  1e4  1e5        $ Time bins (shakes)

c Weight window values (cell × time group)
WWN:N  1.0  0.9  0.8  0.7  0.6  &   $ Cell 1, all time bins
       0.8  0.7  0.6  0.5  0.4  &   $ Cell 2, all time bins
       ...
```

### 6. Adjoint-Weighted WWG

**Theory**: Use adjoint flux for optimal importance

**Advanced WWG Options**:
```
c WWG with adjoint weighting (not standard MCNP6)
c Typically requires ADVANTG or manual adjoint calculation
c Provides near-optimal weight windows
```

## Quick Reference: VR Method Selection

| Problem Type | Primary Method | Secondary Method | Expected FOM Gain |
|--------------|----------------|------------------|-------------------|
| Simple shielding (1-3 layers) | Cell importance (IMP) | - | 5-20× |
| Complex shielding (many regions) | Weight windows (WWG) | - | 20-100× |
| Deep penetration (>10 MFP) | Weight windows (WWG) | Exponential transform (EXT) | 100-1000× |
| Point detector (close) | Weight windows (WWG) | - | 20-100× |
| Point detector (far) | DXTRAN | Weight windows (WWG) | 50-500× |
| Low-density region | Forced collisions (FCL) | Weight windows (WWG) | 5-20× |
| Energy-specific | Energy-dependent WW (WWE) | - | 10-50× |
| Distributed source | Source biasing (SB) | Weight windows (WWG) | 10-50× |

## Quick Reference: WWG Iteration Workflow

**Iteration Template**:
```bash
# Stage 1: Generate initial WW
mcnp6 inp=input_wwg.i outp=out1.o runtpe=run1.r
# → Produces wwout file

# Stage 2: Production run with WW
mcnp6 inp=input_prod.i outp=out2.o runtpe=run2.r
# → Uses wwout from Stage 1

# Stage 3: Regenerate WW (if needed)
mcnp6 inp=input_wwg.i outp=out3.o runtpe=run3.r RUNTPE=run2.r
# → Restart from run2, produces improved wwout

# Stage 4: Final production run
mcnp6 inp=input_final.i outp=out4.o runtpe=run4.r
# → Uses final wwout, no WWG card
```

## Best Practices

1. **Always Start with Analog**: Establish baseline FOM before adding VR
   ```
   c Run 1: Analog (no VR) → FOM = 100
   c Run 2: With VR → Target FOM > 1000
   ```

2. **Test VR Incrementally**: Add one method at a time
   ```
   c Run 1: Analog
   c Run 2: + Cell importance only
   c Run 3: + Weight windows
   c Run 4: + DXTRAN (if needed)
   ```

3. **Monitor FOM Trends**: FOM should remain constant over time
   ```python
   # Check output every 1e5 particles
   # FOM should be: 1500 ± 10% throughout run
   ```

4. **Use WWG, Don't Guess**: Automatic WWG better than manual WWN
   ```
   c Good: WWG 5 0 1.0 (automatic)
   c Bad:  WWN:N 1.0 0.8 0.6 ... (manual guess)
   ```

5. **Iterate WWG 2-5 Times**: Diminishing returns after that
   ```
   c Iteration 1: FOM = 1000
   c Iteration 2: FOM = 3000
   c Iteration 3: FOM = 4000
   c Iteration 4: FOM = 4100 (converged, stop)
   ```

6. **Check All 10 Statistical Tests**: VR can bias results if wrong
   ```
   c Output tally section: all 10 checks should PASS
   c If any fail → results unreliable, fix VR
   ```

7. **Document VR Strategy**: Future users need to understand setup
   ```
   c ==================================================
   c VARIANCE REDUCTION STRATEGY:
   c - Method: Weight windows (WWG automatic)
   c - Target: Detector at (100,0,0)
   c - FOM improvement: 50× over analog
   c - Iterations: 3 (converged)
   c ==================================================
   ```

8. **Archive wwout Files**: Save for reproducibility
   ```bash
   cp wwout wwout_converged_iter3
   # Use in future runs with same geometry
   ```

9. **Validate Against Analog**: Periodically check VR results correct
   ```
   c Every few optimizations, run analog to verify
   c VR result should match analog within statistics
   ```

10. **Don't Over-Optimize**: Good enough is better than perfect
    ```
    c FOM = 5000 with 2 hours work: Good
    c FOM = 5500 with 20 hours work: Not worth it
    ```

11. **Programmatic Variance Reduction**:
    - For automated VR setup and weight window generation, see: `mcnp_variance_reducer.py`
    - Useful for systematic importance calculations, WWG parameter optimization, and batch VR setups

## References

- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md`
  - Section 12: Variance Reduction Cards (lines 1385-1546)
  - Section 17: Variance Reduction Examples (lines 1786-1842)
  - Section 18: Variance Reduction Theory (lines 1844-1887)
- **Related Skills**:
  - mcnp-tally-builder (detector setup)
  - mcnp-output-parser (FOM tracking)
  - mcnp-geometry-builder (cell structure for IMP)
  - mcnp-source-builder (source biasing)
  - mcnp-ww-optimizer (automated weight window optimization)
- **User Manual**:
  - Chapter 5.12 (Variance Reduction Cards)
  - Chapter 2.7 (Variance Reduction Theory)
  - Chapter 10.6 (Variance Reduction Examples)
- **External Resources**:
  - ADVANTG (automated WWG generator)
  - CADIS method (Consistent Adjoint Driven Importance Sampling)

---

**End of MCNP Variance Reducer Skill**
