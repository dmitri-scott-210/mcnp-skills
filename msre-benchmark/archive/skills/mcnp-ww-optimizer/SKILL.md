---
category: E
name: mcnp-ww-optimizer
description: Build and optimize weight window variance reduction using WWN/WWE/WWT/WWP/WWG cards and MESH-based automatic generation
version: 1.0.0
auto_activate: true
activation_keywords:
  - weight window
  - variance reduction
  - WWN
  - WWE
  - WWT
  - WWP
  - WWG
  - MESH
  - importance
  - splitting
  - russian roulette
  - deep penetration
  - shielding
dependencies:
  - mcnp-input-builder
  - mcnp-mesh-builder
related_skills:
  - mcnp-tally-analyzer
  - mcnp-statistics-checker
  - mcnp-plotter
output_formats:
  - MCNP input cards (WWN/WWE/WWT/WWP/WWG/MESH)
  - WWINP file
  - Weight window specification
---

# mcnp-ww-optimizer

**Purpose**: Build and optimize weight window variance reduction to dramatically improve statistical quality for deep penetration, shielding, and low-probability events by guiding particles toward tally regions and preventing wasted sampling in unimportant areas.

## What Are Weight Windows?

**Weight windows** = Space-energy-time dependent variance reduction technique that:
- **Splits** high-importance particles (when weight > upper bound)
- **Roulettes** low-importance particles (when weight < lower bound)
- **Preserves** particles in acceptable weight range (between bounds)

**Result**: More particles reach tally regions, fewer wasted in unimportant zones, better FOM (Figure of Merit).

### When to Use Weight Windows?

```
START: Is your problem converging well?
│
├─→ YES: Don't use weight windows (unnecessary complexity)
│
└─→ NO: What's the issue?
    │
    ├─→ Deep penetration (thick shield, many mean free paths)
    │   → Use weight windows (mesh-based WWG recommended)
    │
    ├─→ Localized tally in large geometry
    │   → Use weight windows + DXTRAN
    │
    ├─→ Detector far from source
    │   → Use weight windows (point detector or mesh-based)
    │
    ├─→ Low-probability event (rare reaction)
    │   → Use importance sampling + weight windows
    │
    └─→ Geometry very complex, many voids
        → Use weight windows (automatic generation with WWG)
```

**FOM Calculation**:
```
FOM = 1 / (R² × T)
```
Where:
- R = relative error of tally
- T = computer time (minutes)
- **Goal**: Maximize FOM (lower error in less time)

## Weight Window Concepts

### Upper and Lower Bounds

For each space-energy-time bin, weight window has:
- **Lower bound** (W_lower): Weight below which particle may be rouletted
- **Upper bound** (W_upper): Weight above which particle is split

**Relationship**:
```
W_upper = wupn × W_lower
```
Where `wupn` = weight window ratio (default: 5)

**Particle behavior**:
```
if W < W_lower:
    Roulette: survive with weight W_survive = wsurvn × W_lower
              or kill with probability (1 - W/W_survive)

if W > W_upper:
    Split into N particles, each with weight W/N
    where N = ceiling(W / (wupn × W_lower))

if W_lower ≤ W ≤ W_upper:
    No action (transport normally)
```

### Weight Window Parameters (WWP Card)

```
WWP:N  wupn  wsurvn  mxspln  mwhere  switchn  mtime  wnorm  etsplt  wu  nmfp
```

**Key parameters**:
- `wupn` (default: 5) = Upper bound multiplier (W_upper = wupn × W_lower)
  - Typical range: 3-10
  - Lower → more splitting (expensive)
  - Higher → less splitting (may miss tally)

- `wsurvn` (default: 3) = Survival weight multiplier after roulette
  - W_survive = wsurvn × W_lower
  - Typical: 2-4

- `mxspln` (default: 5) = Maximum splits per event
  - Prevents excessive splitting
  - Typical: 5-10

- `mwhere` (default: 0) = Where to check weight windows
  - -1 = Collisions only
  - 0 = Both collisions and surfaces (recommended)
  - 1 = Surfaces only

- `switchn` (default: 0) = Source of weight window bounds
  - < 0 = Read from WWINP file
  - = 0 = Use WWN cards
  - > 0 = Generate from cell importance (IMP:N)

- `wnorm` = Normalization factor (multiplies all bounds)

**Example** (typical settings):
```
WWP:N  5  3  5  0  0   $ Upper=5×lower, survive=3×lower, max 5 splits
```

## Weight Window Methods

### Method 1: Cell-Based Weight Windows (WWN Cards)

**Use case**: Simple geometries with few cells.

**Workflow**:
1. Define energy bins (WWE card)
2. Define time bins if needed (WWT card)
3. Specify lower bounds for each cell-energy-time bin (WWN cards)

**Example**: 3-cell problem with 2 energy groups.

```
c --- Energy bins (2 groups: thermal + fast) ---
WWE:N  0.625e-6  20   $ Thermal: 0-0.625 eV, Fast: 0.625 eV-20 MeV

c --- Weight window lower bounds ---
c Format: WWN<n>:N  val_cell1  val_cell2  val_cell3 ...
WWN1:N  1.0  0.5  0.1   $ Energy group 1 (thermal)
WWN2:N  1.0  0.6  0.2   $ Energy group 2 (fast)

c --- Weight window parameters ---
WWP:N  5 3 5 0 0   $ Upper=5×lower, survive=3×lower, check both
```

**Interpretation**:
- Cell 1 (source region): bounds = [1.0, 5.0] (both groups)
- Cell 2 (intermediate): bounds = [0.5, 2.5] (thermal), [0.6, 3.0] (fast)
- Cell 3 (detector region): bounds = [0.1, 0.5] (thermal), [0.2, 1.0] (fast)

**Result**: Particles gain importance (lower bounds) as they approach detector (cell 3).

### Method 2: Mesh-Based Weight Windows (MESH + WWG Cards)

**Use case**: Complex geometries, automatic generation, deep penetration.

**Advantages**:
- Geometry-independent (superimposed mesh)
- Automatic generation from adjoint or flux solution
- Handles complex 3D problems
- **RECOMMENDED for most problems**

#### Step 1: Define Importance Mesh (MESH Card)

```
MESH  GEOM=<geom>  REF=x y z  ORIGIN=x0 y0 z0
      IMESH=... IINTS=... JMESH=... JINTS=... KMESH=... KINTS=...
```

Where:
- `GEOM=XYZ` (Cartesian) or `CYL` (cylindrical) or `SPH` (spherical)
- `REF=x y z` = Reference point (usually detector location)
- `ORIGIN=` = Mesh origin (lower-left corner for XYZ)
- `IMESH/JMESH/KMESH` = Coarse mesh boundaries
- `IINTS/JINTS/KINTS` = Fine mesh subdivisions

**Example** (Cartesian mesh for shielding problem):
```
MESH  GEOM=XYZ  REF=100 0 0  ORIGIN=-10 -10 -10
      IMESH=100  IINTS=50    $ 50 bins from -10 to 100 cm (toward detector)
      JMESH=10   JINTS=10
      KMESH=10   KINTS=10
```

**Example** (Cylindrical mesh for beam target):
```
MESH  GEOM=CYL  REF=0 0 50  ORIGIN=0 0 0
      IMESH=20   IINTS=20    $ Radial: 0-20 cm
      JMESH=50   JINTS=50    $ Axial: 0-50 cm (toward detector at z=50)
      KMESH=360  KINTS=36    $ Azimuthal: full circle
```

#### Step 2: Generate Weight Windows (WWG Card)

```
WWG  <tally_number>  <source_normalization>  <reference_value>
```

Where:
- `<tally_number>` = Tally number to optimize (must be F4 cell tally or mesh tally)
- `<source_normalization>` = (Optional) normalization factor
- `<reference_value>` = (Optional) target tally value at reference point

**Example** (generate from F4 tally):
```
c --- Define tally at detector ---
F4:N  100   $ Detector cell

c --- Define importance mesh ---
MESH  GEOM=XYZ  REF=100 0 0  ORIGIN=-10 -10 -10
      IMESH=100  IINTS=50
      JMESH=10   JINTS=10
      KMESH=10   KINTS=10

c --- Generate weight windows ---
WWG  4  0  0.5   $ Generate from F4, target flux = 0.5 at REF point
```

**MCNP runs TWO calculations**:
1. **Transport run** (without WW): Calculate tally, estimate importance
2. **Rerun** (with generated WW): Apply weight windows from step 1

**Output**: `wwinp` file containing mesh-based weight windows.

#### Step 3: Energy and Time Binning (WWGE/WWGT Cards)

**Energy groups** (WWGE card):
```
WWGE:N  e1  e2  e3  ...  en   $ Energy bin boundaries (MeV)
```

**Time groups** (WWGT card):
```
WWGT:N  t1  t2  t3  ...  tn   $ Time bin boundaries (shakes)
```

**Example** (4 energy groups):
```
WWGE:N  1e-10  1e-6  0.1  1.0  20   $ Thermal, epithermal, fast, high
WWG  4  0  0.5
```

**Result**: Weight windows generated for each mesh-energy-time bin.

### Method 3: Read Pre-Generated Weight Windows (WWINP File)

**Use case**: Iterative refinement, reuse from previous runs.

**Workflow**:
1. Run with WWG to generate initial `wwinp`
2. Rerun using `wwinp` (set `switchn < 0` on WWP card)
3. Optional: Update `wwinp` with new WWG run

**Example**:
```
c --- Read weight windows from file ---
WWP:N  5  3  5  0  -1   $ switchn=-1 → read from wwinp file
```

**WWINP file location**: Same directory as input file, or specify with `WWOUT` card.

**Format** (binary file, don't edit manually):
```
wwinp   $ Binary file generated by MCNP
```

## Decision Tree: Which Weight Window Method?

```
START: Need variance reduction?
│
├─→ Simple geometry (< 10 cells)
│   └─→ Method 1: Cell-based WWN cards
│       - Manually specify bounds
│       - Works well for 1D/2D problems
│
├─→ Complex geometry, deep penetration
│   └─→ Method 2: Mesh-based WWG
│       - Automatic generation
│       - Handles 3D complexity
│       - **RECOMMENDED**
│
├─→ Have good weight windows from previous run
│   └─→ Method 3: Read WWINP file
│       - Faster (skip generation run)
│       - Requires switchn < 0
│
└─→ Extremely complex (criticality, burnup)
    └─→ Use MCNP6 built-in VARI (see User Manual Chapter 5.12.4)
        - Automatic variance reduction
        - Experimental feature
```

## Common Use Cases

### Use Case 1: Deep Penetration Through Shield

**Problem**: Source on one side of thick concrete shield, detector on other side.

```
c ============================================================
c Deep Penetration: 100 cm Concrete Shield
c ============================================================

c --- Geometry ---
c Cell 1: Source region (air)
c Cell 2: Concrete shield (0 < x < 100)
c Cell 3: Detector region (x > 100)

1  1  -0.001  -1         IMP:N=1   $ Air (source)
2  2  -2.3     1 -2      IMP:N=1   $ Concrete shield
3  1  -0.001   2 -3      IMP:N=1   $ Air (detector)
4  0           3         IMP:N=0   $ Outside

1  PX  0       $ Shield front
2  PX  100     $ Shield back
3  PX  110     $ Detector boundary

c --- Materials ---
M1  7014 -0.78  8016 -0.21  18000 -0.01   $ Air
M2  1001 -0.01  8016 -0.50  14000 -0.34   $ Concrete
         11023 -0.02  13027 -0.04  20000 -0.08
         26000 -0.01

c --- Source (1 MeV neutrons at x=0) ---
SDEF  POS=0 0 0  AXS=1 0 0  ERG=1  PAR=N

c --- Tally at detector ---
F4:N  3   $ Flux in detector cell

c --- Mesh for weight windows ---
MESH  GEOM=XYZ  REF=105 0 0  ORIGIN=-5 -10 -10
      IMESH=110  IINTS=50    $ 50 bins through shield + detector
      JMESH=10   JINTS=10
      KMESH=10   KINTS=10

c --- Energy groups for WWG ---
WWGE:N  1e-10  1e-6  0.1  1.0  14   $ Thermal, epi, fast, source

c --- Generate weight windows ---
WWG  4  45  0.5   $ From F4, gen 45 iterations, target=0.5

c --- Weight window parameters ---
WWP:N  5  3  10  0  0   $ Allow up to 10 splits for deep penetration

c --- Run parameters ---
NPS  1000000
PRDMP  2J  1   $ Print dump for restart
```

**Expected FOM improvement**: 100-1000× compared to analog.

**Key settings**:
- `WWG 4 45 0.5`: Generate from F4, run 45 iterations (deep shield needs more)
- `MESH REF=105 0 0`: Reference point inside detector
- `IINTS=50`: Fine mesh through shield (captures importance gradient)
- `WWP mxspln=10`: Allow more splits for deep penetration

### Use Case 2: Point Detector in Large Geometry

**Problem**: Calculate flux at point detector far from source.

```
c ============================================================
c Point Detector in Large Room
c ============================================================

c --- Geometry ---
1  1  -0.001  -1  IMP:N=1   $ Room (10 m cube)
2  0   1  IMP:N=0

1  RPP  -500 500  -500 500  -500 500   $ 10 m × 10 m × 10 m

c --- Source (center of room) ---
SDEF  POS=0 0 0  ERG=2  PAR=N

c --- Point detector (corner of room) ---
F5:N  400 400 400  1   $ Detector at (400,400,400), radius 1 cm

c --- Mesh for weight windows ---
MESH  GEOM=XYZ  REF=400 400 400  ORIGIN=-500 -500 -500
      IMESH=500  IINTS=25    $ Coarse toward source, fine near detector
      JMESH=500  JINTS=25
      KMESH=500  KINTS=25

c --- Generate weight windows ---
WWG  5  0  0.1   $ From F5, target=0.1

c --- Weight window parameters ---
WWP:N  5  3  5  0  0

NPS  100000
```

**FOM improvement**: 10-100× (point detectors benefit greatly from WW).

### Use Case 3: Cylindrical Geometry (Beam on Target)

**Problem**: Proton beam on tungsten target, neutron flux at radial detector.

```
c ============================================================
c Beam Target with Cylindrical Weight Windows
c ============================================================

c --- Geometry ---
1  1  -19.3  -1  IMP:H,N=1   $ Tungsten target (r < 2 cm, 0 < z < 10)
2  2  -0.001  1 -2 -3  IMP:H,N=1   $ Air around target
3  0  3  IMP:H,N=0

1  RCC  0 0 0  0 0 10  2   $ Target cylinder
2  RCC  0 0 0  0 0 10  20   $ Air cylinder
3  RCC  0 0 0  0 0 15  25   $ Outer boundary

c --- Materials ---
M1  74000 1.0   $ Tungsten
M2  7014 -0.78  8016 -0.21  18000 -0.01   $ Air

c --- Source (500 MeV protons, beam axis +Z) ---
SDEF  POS=0 0 0  AXS=0 0 1  ERG=500  PAR=H

c --- Tally (neutron flux at r=15 cm, z=5 cm) ---
F4:N  2   $ Flux in air
FS4  -1   $ Segment by radius

c --- Cylindrical mesh for weight windows ---
MESH  GEOM=CYL  REF=15 0 5  ORIGIN=0 0 0
      IMESH=20   IINTS=20    $ Radial: 0-20 cm
      JMESH=15   JINTS=15    $ Axial: 0-15 cm
      KMESH=360  KINTS=36    $ Azimuthal

c --- Energy groups (neutron energies) ---
WWGE:N  1e-10  1e-6  1  10  100  500   $ Thermal to 500 MeV

c --- Generate weight windows ---
WWG  4  0  0.5

c --- Weight window parameters ---
WWP:N  5  3  5  0  0

MODE  H N   $ Transport protons and neutrons
NPS  500000
```

**Cylindrical mesh**: Matches geometry symmetry, reduces mesh cell count.

### Use Case 4: Time-Dependent Weight Windows

**Problem**: Pulsed source, want good statistics at late times.

```
c ============================================================
c Time-Dependent Weight Windows (Pulsed Source)
c ============================================================

c --- Geometry (simple sphere) ---
1  1  -1.0  -1  IMP:N=1
2  0   1  IMP:N=0

1  SO  100

c --- Materials ---
M1  1001 2  8016 1   $ Water

c --- Pulsed source (delta function at t=0) ---
SDEF  POS=0 0 0  ERG=14  TME=0  PAR=N

c --- Time-dependent tally ---
F4:N  1
E4  0  14
T4  0  1e-8  1e-7  1e-6  1e-5  1e-4   $ Time bins (shakes)

c --- Mesh for weight windows ---
MESH  GEOM=SPH  REF=0 0 0  ORIGIN=0 0 0
      IMESH=100  IINTS=50

c --- Time groups for WWG ---
WWGT:N  0  1e-8  1e-7  1e-6  1e-5  1e-4  1e-3

c --- Generate time-dependent weight windows ---
WWG  4  0  0.5

WWP:N  5  3  5  0  0

NPS  1000000
```

**WWGT card**: Specifies time bins for weight windows (matches T4 tally).

### Use Case 5: Iterative Refinement

**Problem**: Initial WWG run not optimal, need to refine.

**Iteration 1** (generate initial WW):
```
WWG  4  0  0.5   $ Generate from F4
WWP:N  5  3  5  0  0
NPS  100000      $ Short run for initial estimate
```

**Check output**:
- Look at FOM in output file
- Check relative errors
- If poor, increase NPS and rerun with generated WW

**Iteration 2** (use generated WW):
```
c WWG  4  0  0.5   $ Comment out (don't regenerate)
WWP:N  5  3  5  0  -1   $ Read from wwinp file (switchn=-1)
NPS  1000000   $ Longer run with optimized WW
```

**Iteration 3** (optional: regenerate with more particles):
```
WWG  4  0  0.5   $ Regenerate with better statistics
WWP:N  5  3  5  0  0
NPS  1000000   $ Use more particles for WW generation
```

**Result**: Each iteration improves weight window quality, leading to better FOM.

## Advanced Techniques

### Combining Weight Windows with Other Variance Reduction

**Weight windows + Importance (IMP)**:
```
c Cells with IMP>0 required for WW
1  1  -10.5  -1  IMP:N=1   $ Source region
2  1  -10.5   1 -2  IMP:N=1   $ Shield
3  1  -10.5   2  IMP:N=1   $ Detector region

WWG  4  0  0.5
WWP:N  5  3  5  0  0   $ switchn=0 → use WWG (ignore IMP values)
```

**Weight windows + DXTRAN**:
```
c Point detector far from source
F5:N  100 0 0  1

c DXTRAN sphere at detector
DXC  100 0 0  5   $ DXTRAN centered at (100,0,0), radius 5 cm

c Weight windows toward detector
MESH  GEOM=XYZ  REF=100 0 0  ...
WWG  5  0  0.1
```

**Weight windows + Energy/Time Splitting (ESPLT/TSPLT)**:
```
c Energy splitting at shield boundary
ESPLT:N  2  0.1  2  0.01   $ Split by 2 at 0.1 MeV, by 2 at 0.01 MeV

c Weight windows for overall importance
WWG  4  0  0.5
```

**Guideline**: Weight windows handle space-energy-time importance; other techniques handle specific local effects.

### Weight Window Generation Parameters

**WWG syntax**:
```
WWG  <tally>  <ic>  <target>  <maxsp>  <e_min>  <e_max>
```

Where:
- `<ic>` = Number of iterations (default: automatic)
  - 0 = Use mesh-based generation (recommended)
  - > 0 = Use cell-based generation with `ic` iterations
- `<target>` = Target tally value at reference point
- `<maxsp>` = Maximum space splitting
- `<e_min>`, `<e_max>` = Energy range for generation

**Example** (fine control):
```
WWG  4  0  0.5  10  1e-6  20   $ Mesh-based, target=0.5, maxsp=10, 1 eV-20 MeV
```

### Spherical Weight Window Mesh

**Use case**: Point source in large spherical geometry.

```
MESH  GEOM=SPH  REF=0 0 0  ORIGIN=0 0 0
      IMESH=10  20  50  100  IINTS=5  5  10  20   $ Fine near source, coarse far
```

**Advantage**: Radial symmetry → fewer mesh cells, faster generation.

## Troubleshooting

### Problem: Weight windows make FOM worse

**Causes**:
1. Wrong reference point (REF not at tally)
2. Mesh too coarse (importance gradient not captured)
3. Too few particles for WW generation (NPS too small)

**Fix**:
```
c Check reference point
MESH  GEOM=XYZ  REF=<detector_x> <detector_y> <detector_z>  ...

c Refine mesh near detector
MESH  ...
      IMESH=10  50  100  IINTS=10  20  10   $ Fine near detector (x=50)

c Increase NPS for WW generation
NPS  1000000   $ More particles → better WW estimate
```

### Problem: "weight window lower bound = 0" warnings

**Cause**: Some mesh cells have zero importance (particles never reach).

**Fix**: Acceptable if cells are truly unimportant. If many cells have zero bounds, mesh may be too fine or extend into voids.

```
c Reduce mesh extent to cover only relevant geometry
MESH  GEOM=XYZ  REF=100 0 0  ORIGIN=0 -10 -10   $ Don't start at -100 (void)
      IMESH=110  IINTS=50
```

### Problem: Excessive splitting (too many particles)

**Cause**: `mxspln` too high or `wupn` too low.

**Fix**:
```
c Reduce maximum splits
WWP:N  5  3  5  0  0   $ mxspln=5 (was 20)

c Increase upper bound ratio
WWP:N  10  3  5  0  0   $ wupn=10 (less splitting)
```

### Problem: Particles killed too aggressively (poor statistics)

**Cause**: `wsurvn` too low or weight window bounds too strict.

**Fix**:
```
c Increase survival weight
WWP:N  5  4  5  0  0   $ wsurvn=4 (was 2)

c Widen weight window (higher wupn)
WWP:N  10  4  5  0  0   $ wupn=10, wsurvn=4
```

### Problem: Weight windows don't converge (WWG iterations fail)

**Cause**: Tally has zero or very low scores.

**Fix**:
1. Run longer (increase NPS)
2. Use coarser mesh
3. Use simpler variance reduction first (IMP only)

```
c Start with cell importance
1  1  -10.5  -1  IMP:N=1
2  1  -10.5   1 -2  IMP:N=10    $ Increase importance toward detector
3  1  -10.5   2  IMP:N=100

c Then add WW once tally scores
```

### Problem: Weight windows file (wwinp) not created

**Cause**: WWG card syntax error or tally not scoring.

**Fix**: Check output file for "weight window generation" section. Verify tally scores non-zero.

### Problem: Rerunning with wwinp doesn't improve FOM

**Cause**: Weight windows not being read (switchn wrong).

**Fix**:
```
WWP:N  5  3  5  0  -1   $ switchn=-1 (read wwinp)
```

Verify message in output: "reading weight windows from file wwinp".

## Integration with Other Skills

### With mcnp-mesh-builder

Use mesh tally results to create weight windows:
```python
from skills.variance_reduction.mcnp_ww_optimizer import WWOptimizer
from skills.output_analysis.mcnp_tally_analyzer import MCNPTallyAnalyzer

# Parse mesh tally
analyzer = MCNPTallyAnalyzer('meshtal.xdmf')
flux = analyzer.get_mesh_tally(14)

# Generate weight windows from flux distribution
optimizer = WWOptimizer()
optimizer.generate_from_flux(
    flux=flux,
    reference_point=(100, 0, 0),
    output_file='wwinp'
)
```

### With mcnp-statistics-checker

Check if weight windows improved FOM:
```python
from skills.output_analysis.mcnp_statistics_checker import StatisticsChecker

# Compare FOM before and after WW
checker_analog = StatisticsChecker('output_analog.o')
checker_ww = StatisticsChecker('output_with_ww.o')

fom_analog = checker_analog.get_fom(tally=4)
fom_ww = checker_ww.get_fom(tally=4)

improvement = fom_ww / fom_analog
print(f"FOM improvement: {improvement:.1f}×")
```

### With mcnp-plotter

Visualize weight window distribution:
```python
from skills.visualization.mcnp_plotter import MCNPPlotter

plotter = MCNPPlotter('input.i')

# Plot weight window mesh overlaid on geometry
plotter.plot_weight_windows(
    wwinp_file='wwinp',
    energy_group=2,
    basis='XZ',
    origin=(0, 0, 0)
)
```

## Best Practices

1. **Use mesh-based WWG** - Automatic, geometry-independent, handles complexity
2. **Reference point at detector** - Ensures importance increases toward tally
3. **Fine mesh near detector** - Captures steep importance gradient
4. **Energy groups match tally** - WWGE bins should align with tally energy bins
5. **Start coarse, refine** - Use coarse mesh first, verify improvement, then refine
6. **Check FOM** - Weight windows should improve FOM (not just reduce error)
7. **Iterate** - First run generates WW, second run uses WW, third run regenerates with better statistics
8. **Don't over-split** - mxspln=5-10 is usually sufficient; higher values waste time
9. **Combine techniques** - WW works well with DXTRAN, importance, energy splitting
10. **Verify with plots** - Visualize weight window distribution to ensure correctness
11. **Programmatic WW Optimization**:
    - For automated weight window generation and iterative optimization, see: `mcnp_ww_optimizer.py`
    - Useful for systematic WWG parameter studies, wwout file processing, and automated WW iteration workflows

## References

- **Theory Manual**: Chapter 2.7 - Variance Reduction
- **User Manual**: Chapter 5.12 - Variance Reduction Cards
- **Examples**: Chapter 10.6 - Variance Reduction Examples
- **COMPLETE_MCNP6_KNOWLEDGE_BASE.md**: Weight window specification
- **Related skills**: mcnp-mesh-builder, mcnp-statistics-checker, mcnp-tally-analyzer
