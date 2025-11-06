# Mesh-Based Weight Windows

## Overview

This reference describes mesh-based weight window generation in MCNP, which uses a superimposed importance mesh grid independent of the geometry cell structure. Mesh-based WW is essential for complex geometries where cell-based generation is impractical.

---

## Why Mesh-Based Weight Windows?

### Advantages Over Cell-Based WW

**Cell-Based Limitations:**
1. **Complex geometries** → hundreds/thousands of cells → impractical WWN specification
2. **Repeated structures** → each lattice cell needs separate importance
3. **Non-uniform importance** within large cells → single bound insufficient
4. **Geometry changes** → must regenerate WWN for every cell

**Mesh-Based Advantages:**
1. **Independent of geometry** → mesh overlays cells
2. **Flexible resolution** → refine mesh where needed
3. **Easy to modify** → change mesh without touching geometry
4. **Automatic with WWG** → no manual specification required
5. **Handles repeated structures** naturally

### When to Use Mesh-Based WW

- ✅ Complex geometries (>50 cells)
- ✅ Repeated structures (lattices, arrays)
- ✅ Large cells with importance gradients
- ✅ Iterative geometry optimization
- ✅ Automatic WWG generation preferred

---

## MESH Card Specification

### Rectangular Mesh (GEOM=XYZ)

**Syntax:**
```
MESH  GEOM=XYZ  REF=x₀ y₀ z₀  ORIGIN=xₘᵢₙ yₘᵢₙ zₘᵢₙ
      IMESH=x₁ x₂ ... xₘ  IINTS=i₁ i₂ ... iₘ
      JMESH=y₁ y₂ ... yₙ  JINTS=j₁ j₂ ... jₙ
      KMESH=z₁ z₂ ... zₖ  KINTS=k₁ k₂ ... kₖ
```

**Parameters:**
- `GEOM=XYZ` → Rectangular (Cartesian) mesh
- `REF=x₀ y₀ z₀` → Reference point (typically problem origin)
- `ORIGIN=xₘᵢₙ yₘᵢₙ zₘᵢₙ` → Lower-left corner of mesh
- `IMESH=...` → X-axis mesh boundaries
- `IINTS=...` → Number of intervals in each X segment
- `JMESH=...` → Y-axis mesh boundaries
- `JINTS=...` → Number of intervals in each Y segment
- `KMESH=...` → Z-axis mesh boundaries
- `KINTS=...` → Number of intervals in each Z segment

**Example - Simple Shielding:**
```
c Problem: Source at origin, detector at (100,0,0), shield from x=10 to x=90
c
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-10 -10 -10
      IMESH=10  90  100  IINTS=4  16  2
      JMESH=10            JINTS=4
      KMESH=10            KINTS=4
c
c Result:
c   X: -10 to 10 (4 bins), 10 to 90 (16 bins, shield region), 90 to 100 (2 bins)
c   Y: -10 to 10 (4 bins, symmetric)
c   Z: -10 to 10 (4 bins, symmetric)
c   Total: 22 × 4 × 4 = 352 mesh cells
```

### Cylindrical Mesh (GEOM=CYL or RZT)

**Syntax:**
```
MESH  GEOM=CYL  REF=x₀ y₀ z₀  AXS=uₓ uᵧ uᵤ  VEC=vₓ vᵧ vᵤ  ORIGIN=xₘᵢₙ yₘᵢₙ zₘᵢₙ
      IMESH=r₁ r₂ ... rₘ  IINTS=i₁ i₂ ... iₘ    $ Radial
      JMESH=z₁ z₂ ... zₙ  JINTS=j₁ j₂ ... jₙ    $ Axial
      KMESH=θ₁ θ₂ ... θₖ  KINTS=k₁ k₂ ... kₖ    $ Angular (degrees)
```

**Parameters:**
- `GEOM=CYL` → Cylindrical mesh (r, z, θ)
- `AXS=...` → Cylinder axis direction (unit vector)
- `VEC=...` → Reference vector for θ=0° (unit vector)
- `IMESH=...` → Radial mesh boundaries
- `JMESH=...` → Axial (z) mesh boundaries
- `KMESH=...` → Angular mesh boundaries (0-360°)

**Example - Cylindrical Source:**
```
c Problem: Cylindrical reactor core, radius 200 cm, height 400 cm
c
MESH  GEOM=CYL  REF=0 0 0  AXS=0 0 1  VEC=1 0 0  ORIGIN=0 0 -200
      IMESH=50  100  150  200  250  IINTS=5  5  5  5  5    $ Radial: 5 bins each
      JMESH=0  200  400              JINTS=10  10           $ Axial: 10 bins each half
      KMESH=90  180  270  360        KINTS=3  3  3  3        $ Angular: 12 bins total
c
c Result:
c   R: 0-50 (core), 50-100 (reflector), 100-150 (shield), 150-200 (outer shield), 200-250 (detector)
c   Z: -200 to 0 (lower half), 0 to 200 (upper half)
c   θ: 12 angular bins
c   Total: 25 × 20 × 12 = 6,000 mesh cells
```

---

## Mesh Resolution Guidelines

### Balancing Resolution vs. Sampling

**Too Coarse:**
- Large regions with varying importance
- Single WW bound inadequate
- Symptom: FOM improvement limited (<10×)

**Too Fine:**
- Individual mesh cells not adequately sampled
- Statistical noise in importance estimates
- Symptom: Many flagged WW inconsistencies, erratic FOM

**Optimal Resolution:**
- ~5-20 mean free paths per mesh cell in penetration direction
- At least ~100 particles entering each mesh cell during WWG run
- Refine mesh near detectors, coarsen in unimportant regions

### Region-Specific Resolution

**High-resolution regions:**
- Near detectors (factor 2-4 finer)
- Interfaces between materials
- Streaming paths
- Regions with steep importance gradients

**Low-resolution regions:**
- Void regions (1-2 cells sufficient)
- Homogeneous bulk shielding
- Regions far from tallies

**Example - Non-uniform Mesh:**
```
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-100 -100 -100
      IMESH=-50  0  50  80  100  IINTS=2  5  15  5  2
c              ^^coarse   ^^fine near detector at x=90
      JMESH=100  JINTS=5
      KMESH=100  KINTS=5
```

---

## WWG with MESH Integration

### Basic Workflow

**Step 1: Define Mesh**
```
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-60 -60 -60
      IMESH=60  IINTS=12
      JMESH=60  JINTS=12
      KMESH=60  KINTS=12
```

**Step 2: Define Energy Bins (Optional)**
```
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c       ^thermal   ^epithermal  ^fast    ^high energy
```

**Step 3: Run WWG**
```
F5:N  100 0 0  0.5           $ Point detector at (100,0,0)
WWG  5  0  1.0               $ Generate WW from F5
NPS  1e5                     $ Moderate statistics
```

**Step 4: MCNP Creates wwout File**
Contains mesh-based weight window values:
- One value per mesh cell × energy group
- Format suitable for input to next run

**Step 5: Production Run**
```
c Same MESH definition
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-60 -60 -60
      IMESH=60  IINTS=12
      JMESH=60  JINTS=12
      KMESH=60  KINTS=12
c
c Same energy bins
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c Use weight windows from wwout
WWP:N  J  J  J  0  -1
c
F5:N  100 0 0  0.5
NPS  1e7                     $ High statistics
```

---

## Advanced Mesh Techniques

### Nested Mesh Refinement

For problems with multiple scales, use coarse mesh globally with local refinement:

**NOT SUPPORTED:** MCNP does not allow multiple MESH cards.

**Alternative - Single Mesh with Variable Resolution:**
```
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-200 -200 -200
      IMESH=-100  -10  10  100  200  IINTS=5  20  20  5  5
c            ^^coarse  ^^fine near origin  ^^coarse
```

### Cylindrical Mesh for Cylindrical Problems

**When to use:**
- Cylindrical/spherical source geometry
- Cylindrical detectors or dose planes
- Radial shielding problems

**Advantages:**
- Natural coordinate system
- Fewer mesh cells for same resolution
- Importance typically varies by radius

**Example - Reactor Shielding:**
```
MESH  GEOM=CYL  REF=0 0 0  AXS=0 0 1  VEC=1 0 0
      IMESH=100  200  300  400  500  IINTS=10  10  10  10  10
c           ^core  ^reflector ^shield1 ^shield2  ^detector
      JMESH=-200  0  200  JINTS=10  10
c           ^lower half  ^upper half
      KMESH=360  KINTS=12
c           ^12 angular bins (30° each)
```

---

## Troubleshooting Mesh-Based WW

### Problem: Too Many Flagged WW Adjustments

**Symptom:** MCNP warns about WW ratios >4× between adjacent mesh cells.

**Causes:**
1. Mesh too fine → insufficient sampling
2. True importance varies rapidly
3. Statistical flukes

**Solutions:**
1. Coarsen mesh (fewer IINTS)
2. Run longer WWG generation (more NPS)
3. Manually smooth flagged values before production run

### Problem: WW Not Improving FOM

**Symptom:** FOM with WW ≈ FOM without WW.

**Causes:**
1. Mesh doesn't align with importance contours
2. Energy binning too coarse
3. WWG target tally not representative

**Solutions:**
1. Adjust mesh orientation/resolution
2. Add WWGE energy bins
3. Verify WWG tally represents problem importance

### Problem: Memory Limitations

**Symptom:** MCNP reports insufficient memory for WW storage.

**Cause:** Too many mesh cells × energy bins.

**Calculation:**
```
WW entries = (mesh cells) × (energy bins)
Example: 100×100×100 mesh, 10 energy bins = 10,000,000 entries
```

**Solutions:**
1. Reduce mesh resolution (fewer IINTS)
2. Reduce energy bins (fewer WWGE entries)
3. Increase MCNP memory allocation
4. Use cell-based WW for subset of geometry

---

## Example: Complete Mesh-Based WWG Workflow

### Problem Setup

Neutron source at origin, point detector at (100,0,0), complex shield between.

### Stage 1 - Generate Weight Windows

```
MCNP Example - Mesh-Based WWG Generation
c
c =================================================================
c Cell Cards
c =================================================================
c
1   1  -7.85  -1       IMP:N=1     $ Source region (steel)
2   2  -2.3   1 -2     IMP:N=1     $ Concrete shield
3   3  -11.3  2 -3     IMP:N=1     $ Lead shield
4   0        3 -4     IMP:N=1     $ Detector region (void)
5   0        4        IMP:N=0     $ Graveyard
c
c =================================================================
c Surface Cards
c =================================================================
c
1   SO   10              $ Source sphere
2   SO   50              $ Concrete outer
3   SO   80              $ Lead outer
4   SO   120             $ Outer boundary
c
c =================================================================
c Data Cards
c =================================================================
c
MODE  N
c
c Define rectangular mesh
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-120 -120 -120
      IMESH=120  IINTS=24       $ X: 24 bins (5 cm each near detector)
      JMESH=120  JINTS=24       $ Y: 24 bins
      KMESH=120  KINTS=24       $ Z: 24 bins
c     Total mesh cells: 24×24×24 = 13,824
c
c Energy bins for weight windows
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  14.5
c       ^thermal ^epithermal  ^fast  ^source energy
c     Total WW entries: 13,824 × 8 = 110,592
c
c Point detector at (100,0,0)
F5:N  100 0 0  0.5
c
c Generate weight windows from F5
WWG  5  0  1.0               $ tally 5, time group 0, target weight 1.0
c
c Source
SDEF  POS=0 0 0  ERG=14.1
c
NPS  5e4                      $ 50k particles for WWG generation
```

### Stage 2 - Production with Mesh-Based WW

```
MCNP Example - Production Run with Mesh-Based WW
c
c [Same cell and surface cards]
c
c =================================================================
c Data Cards
c =================================================================
c
MODE  N
c
c Same mesh definition (MUST match Stage 1)
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-120 -120 -120
      IMESH=120  IINTS=24
      JMESH=120  JINTS=24
      KMESH=120  KINTS=24
c
c Same energy bins (MUST match Stage 1)
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  14.5
c
c Use weight windows from wwout
WWP:N  J  J  J  0  -1
c     ^read from wwout file
c
c Point detector
F5:N  100 0 0  0.5
c
c Source
SDEF  POS=0 0 0  ERG=14.1
c
NPS  1e7                      $ 10M particles for production
```

---

## Best Practices

1. **Start with coarse mesh** → refine only if needed
2. **Align mesh with geometry** when possible (minimize mesh/cell crossings)
3. **Energy bins match physics** (thermal/epithermal/fast boundaries)
4. **MESH and WWGE must be identical** between WWG and production runs
5. **Iterate 2-5 times** with increasing NPS each iteration
6. **Check flagged WW** after each iteration, adjust mesh if necessary
7. **Production run:** Remove WWG card, keep MESH and WWGE, add WWP:N J J J 0 -1

---

## References

**MCNP6 User Manual:**
- Chapter 5.11: MESH Card Specification
- Chapter 5.12.6: WWG Card with Mesh
- Chapter 5.12.3: WWGE Card (Energy Bins)

**See Also:**
- `wwg_iteration_guide.md` - Step-by-step WWG workflow
- `advanced_vr_theory.md` - WWG algorithm and convergence
- `card_specifications.md` - WWN, WWE, WWP, WWG syntax
