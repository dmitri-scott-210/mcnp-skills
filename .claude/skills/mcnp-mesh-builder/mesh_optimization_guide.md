# Mesh Optimization Guide for MCNP6

**Purpose:** Strategies for optimizing mesh resolution, performance, and statistical quality in MCNP mesh tallies.

**Companion to:** SKILL.md, unstructured_mesh_guide.md, mesh_file_formats.md

---

## Overview

Mesh tally performance depends on three competing factors:

1. **Spatial resolution** - How fine the mesh is (more bins = better detail)
2. **Statistical quality** - How many particles per bin (fewer bins = better statistics)
3. **Computational cost** - How long the simulation takes (more bins = slower)

**Goal:** Find optimal balance for your specific problem.

---

## Mesh Resolution Strategies

### The Resolution-Statistics Tradeoff

**Fine mesh (many small bins):**
- ✅ High spatial resolution (captures gradients, hotspots)
- ❌ Poor statistics per bin (few particles per bin)
- ❌ Large output files (millions of bins)
- ❌ Slower tallying (more bins to check)

**Coarse mesh (few large bins):**
- ✅ Good statistics per bin (many particles per bin)
- ✅ Small output files (thousands of bins)
- ✅ Faster tallying
- ❌ Low spatial resolution (may miss features)

**Optimal approach:** **Adaptive refinement** - fine where needed, coarse elsewhere.

### Rule of Thumb for Bin Count

| Problem Type | Recommended Total Bins | Typical Resolution |
|-------------|----------------------|-------------------|
| Quick survey | 1,000 - 10,000 | 10×10×10 to 20×20×25 |
| Standard analysis | 10,000 - 100,000 | 25×25×40 to 50×50×80 |
| Detailed study | 100,000 - 1,000,000 | 50×50×100 to 100×100×100 |
| High-resolution | > 1,000,000 | > 100×100×100 |

**Example:**
- 20×20×20 mesh = 8,000 bins (good statistics)
- 50×50×50 mesh = 125,000 bins (moderate statistics)
- 100×100×100 mesh = 1,000,000 bins (poor statistics unless very high NPS)

### Particles Per Bin Guideline

**Minimum for acceptable statistics:**
- **10 particles/bin** - Bare minimum (errors ~30%)
- **100 particles/bin** - Acceptable (errors ~10%)
- **1,000 particles/bin** - Good (errors ~3%)
- **10,000 particles/bin** - Excellent (errors ~1%)

**Calculate from NPS:**
```
Average particles per bin = NPS × (fraction reaching mesh region) / (number of bins)
```

**Example:**
- NPS = 1e8
- 50% of particles reach mesh region
- 100,000 bins
- Average particles/bin = 1e8 × 0.5 / 100,000 = 500 (errors ~4-5%)

---

## Adaptive Refinement Techniques

### Coarse-to-Fine Workflow

**Step 1:** Start with coarse mesh (10×10×10)
```
FMESH4:N GEOM=XYZ
         ORIGIN=0 0 0
         IMESH=100  IINTS=10
         JMESH=100  JINTS=10
         KMESH=100  KINTS=10
```

**Step 2:** Run simulation, identify regions of interest
- High flux regions
- Steep gradients
- Critical components

**Step 3:** Refine mesh in those regions only
```
FMESH14:N GEOM=XYZ
          ORIGIN=0 0 0
          IMESH=20 40 100   IINTS=10 10 10    $ Fine (0-20), medium (20-40), coarse (40-100)
          JMESH=20 40 100   JINTS=10 10 10
          KMESH=20 40 100   KINTS=10 10 10
```

**Step 4:** Re-run with refined mesh

**Result:** High resolution where needed, good statistics overall.

### Non-Uniform Mesh Binning

**Use IMESH/JMESH/KMESH with multiple intervals:**

```
c --- Reactor core with central assembly ---
FMESH24:N GEOM=XYZ
          ORIGIN=-100 -100 -150
          c Central region: fine mesh
          IMESH=  -10  10  100    IINTS=  20  20  10
          JMESH=  -10  10  100    JINTS=  20  20  10
          c Axial: fine in active core, coarse above/below
          KMESH=  -50  50  150    KINTS=  10  50  10
```

**Interpretation:**
- X direction: 20 bins from -100 to -10, 20 bins from -10 to +10, 10 bins from +10 to +100
- Central 20×20 cm region has 40×40 bins
- Outer regions have 10×10 bins
- Total: (20+20+10) × (20+20+10) × (10+50+10) = 50×50×70 = 175,000 bins

### Logarithmic Spacing

**For problems with exponential attenuation (shielding):**

Use logarithmic spacing in depth direction:

```python
import numpy as np

# Logarithmic mesh boundaries (1 cm to 100 cm)
depths = np.logspace(0, 2, 20)  # [1, 1.26, 1.58, ..., 100]

# Convert to KMESH format
kmesh_line = "KMESH=  " + " ".join(f"{d:.2f}" for d in depths)
kints_line = "KINTS=  " + " ".join(["1"] * (len(depths)-1))

print(kmesh_line)
print(kints_line)
```

**Result:** Fine bins near source, coarse bins far away (matches exponential flux profile).

---

## Performance Optimization

### MSHMF Algorithm Selection

MCNP6 supports multiple mesh tally algorithms (MSHMF keyword):

| Algorithm | Best For | Parallel Scaling | Memory Use | Accuracy |
|-----------|---------|------------------|------------|----------|
| `fast_hist` | Most problems (default) | Excellent | Low | Good |
| `hist` | Sequential runs | Poor | Low | Excellent |
| `batch` | Poor statistics | Good | Medium | Excellent |
| `rma_batch` | Huge meshes (>10M bins) | Excellent | High | Excellent |

**Recommendation:**
- **Default** (fast_hist) for most work
- **batch** if statistical quality is poor with default
- **rma_batch** for very large meshes on clusters

**Example:**
```
FMESH34:N GEOM=XYZ ...
          MSHMF=batch    $ Better statistics than fast_hist
```

### Memory Considerations

**Memory per bin:**
- ~16 bytes per bin (8 bytes value + 8 bytes error)
- + overhead for mesh geometry (~50 bytes per element for UM)

**Example calculations:**

**FMESH (100×100×100 bins):**
```
Bins = 1,000,000
Memory ≈ 1M × 16 bytes = 16 MB (negligible)
```

**UM (100,000 elements, 50,000 vertices):**
```
Elements = 100,000
Vertices = 50,000
Memory ≈ 100k × 50 bytes + 50k × 12 bytes = 5.6 MB (still small)
```

**Memory is rarely an issue** unless using > 10 million bins.

### Output File Size

**File size estimates:**

| Mesh Size | FMESH (XDMF) | UM (HDF5) | Legacy (ASCII) |
|-----------|--------------|-----------|----------------|
| 10k bins | ~1 MB | ~2 MB | ~5 MB |
| 100k bins | ~10 MB | ~20 MB | ~50 MB |
| 1M bins | ~100 MB | ~200 MB | ~500 MB |
| 10M bins | ~1 GB | ~2 GB | ~5 GB |

**If file size is a problem:**
- Use `OUT=none` if only FM tally matters (suppresses flux output)
- Reduce energy/time bins
- Use lower mesh resolution
- Compress output files (gzip, HDF5 built-in compression)

---

## Energy and Time Binning Optimization

### Energy Group Collapse

**Instead of continuous energy bins, use broad groups:**

```
c --- Many bins (slow, poor statistics) ---
EMESH=1e-10 1e-9 1e-8 ... 14    $ 100 energy bins

c --- Few groups (fast, good statistics) ---
EMESH=1e-10 1e-6 0.1 1 14       $ 4 energy groups: thermal, epithermal, fast, high
```

**Standard reactor groups:**
- Thermal: 0 to 1 eV
- Epithermal: 1 eV to 100 keV
- Fast: 100 keV to 1 MeV
- High: 1 MeV to 20 MeV

### Time Binning Strategy

**For pulsed sources:**

Use logarithmic time bins to capture early and late flux:

```python
import numpy as np

# Time bins from 1 ns to 1 ms (7 orders of magnitude)
time_bins = np.logspace(-8, -3, 20)  # shakes (1e-8 s)

tmesh_line = "TMESH=  " + " ".join(f"{t:.2e}" for t in time_bins)
print(tmesh_line)
```

**For steady-state:** Omit TMESH (single time bin = integrated flux).

---

## Statistical Quality Metrics

### 10 MCNP Statistical Checks

For mesh tallies, focus on:

**Check 1:** Mean behavior (should be random noise around mean)
**Check 2:** Relative error < 0.10 (10% error)
**Check 4:** VOV (variance of variance) < 0.1
**Check 8:** Figure of merit (FOM) constant

**Good mesh tally:**
```
All 10 checks passed
Mean relative error: 0.05
No bins with error > 0.10
```

**Poor mesh tally:**
```
Checks 2, 4, 8 failed
Mean relative error: 0.25
50% of bins have error > 0.20
```

### Assessing Mesh Tally Quality

**After running MCNP, check:**

```python
import h5py
import numpy as np

f = h5py.File('meshtal_14.h5', 'r')
flux = f['flux'][:]
error = f['error'][:]

# Histogram of errors
bins_under_10_pct = (error < 0.10).sum()
bins_under_20_pct = (error < 0.20).sum()
bins_over_50_pct = (error > 0.50).sum()

print(f"Bins with error < 10%: {bins_under_10_pct / len(error):.1%}")
print(f"Bins with error < 20%: {bins_under_20_pct / len(error):.1%}")
print(f"Bins with error > 50%: {bins_over_50_pct / len(error):.1%}")

# Identify problem regions
worst_bins = np.where(error > 0.50)[0]
print(f"Worst bins: {worst_bins}")
```

**Acceptance criteria:**
- **90% of bins** with error < 10%
- **100% of bins** with error < 20%
- **0% of bins** with error > 50%

### Fixing Poor Statistics

**If mesh tally has bad statistics:**

1. **Increase NPS** (more particles)
   ```
   NPS  1e9    $ Up from 1e8
   ```

2. **Reduce mesh resolution** (fewer, larger bins)
   ```
   IINTS=25 JINTS=25 KINTS=25    $ Down from 50×50×50
   ```

3. **Use variance reduction** (weight windows)
   ```
   IMP:N  1  1  1  ...    $ Cell importances
   WWE:N  1e-3             $ Weight window lower bound
   ```

4. **Change algorithm** (batch for better error estimates)
   ```
   MSHMF=batch
   ```

5. **Reduce energy bins** (group collapse)
   ```
   EMESH=1e-10 1e-6 0.1 1 14    $ 4 groups instead of 100
   ```

---

## Mesh Design Best Practices

### 1. Match Mesh to Physics

**Neutron diffusion length** sets minimum useful bin size:

```
Diffusion length L ≈ 1/√(3 Σ_a Σ_tr) ≈ 1-5 cm for thermal reactors
```

**Guideline:** Mesh bins smaller than ~L/2 provide little additional information.

**Example:**
- Thermal reactor with L ≈ 3 cm
- Minimum useful bin size: ~1.5 cm
- 100 cm cube → 100/1.5 ≈ 67 bins per dimension

### 2. Align Mesh with Geometry

**For structured geometry (fuel assemblies), align mesh with pitch:**

```
c --- 17×17 assembly, 1.26 cm pitch ---
FMESH4:N GEOM=XYZ
         ORIGIN=0 0 0
         IMESH=21.42  IINTS=17    $ 17 bins at 1.26 cm each
         JMESH=21.42  JINTS=17
         KMESH=366    KINTS=100   $ Active height
```

**Result:** Each bin contains exactly one fuel pin (easier interpretation).

### 3. Avoid Empty Bins

**Don't extend mesh into voids:**

```
c --- BAD: Mesh covers entire problem (including air) ---
FMESH14:N ORIGIN=-500 -500 -500
          IMESH=500  IINTS=100    $ Most bins are air/void

c --- GOOD: Mesh covers geometry of interest only ---
FMESH14:N ORIGIN=-50 -50 -100
          IMESH=50  IINTS=50    $ All bins in reactor core
```

### 4. Test with Geometry Plotter

**Before running expensive simulation:**

```bash
# Plot geometry with mesh overlay (using MCNP plotter)
mcnp6 ip i=input.i com="plot origin 0 0 0 extent 100 100"
```

**Verify:**
- Mesh covers intended region
- Mesh doesn't extend into voids
- Mesh alignment with geometry features

### 5. Progressive Refinement

**Start coarse, refine iteratively:**

**Run 1:** 10×10×10 mesh, 1e7 particles (quick survey)
**Run 2:** 20×20×20 mesh, 1e8 particles (identify hotspots)
**Run 3:** Non-uniform mesh (fine in hotspots), 1e9 particles (final)

**Total time:** Less than single 100×100×100 run with 1e10 particles.

---

## Advanced Techniques

### Mesh Tally Variance Reduction

**Weight windows based on mesh tally:**

**Step 1:** Run with coarse mesh to get flux distribution
```
FMESH4:N GEOM=XYZ ...
         OUT=xdmf
```

**Step 2:** Generate weight windows from flux mesh
```python
from mcnp_ww_optimizer import WWOptimizer

optimizer = WWOptimizer()
optimizer.generate_from_mesh('meshtal.xdmf', tally=4, output='wwinp')
```

**Step 3:** Re-run with weight windows + fine mesh
```
WWN:N  -1    $ Read weight windows from wwinp file
FMESH14:N GEOM=XYZ ...    $ Fine mesh for final results
          IINTS=50 JINTS=50 KINTS=50
```

**Result:** Better statistics in hard-to-reach regions.

### Overlapping Meshes

**Use multiple FMESH cards for different regions:**

```
c --- Coarse mesh for entire geometry ---
FMESH4:N GEOM=XYZ
         ORIGIN=-100 -100 -100
         IMESH=100  IINTS=20
         ...

c --- Fine mesh for central region only ---
FMESH14:N GEOM=XYZ
          ORIGIN=-10 -10 -10
          IMESH=10  IINTS=40
          ...
```

**Advantage:** Full coverage + high resolution in ROI, without wasting bins.

### Cylindrical Mesh for Cylindrical Problems

**For axially symmetric geometry, use RZT mesh:**

**Cartesian (inefficient):**
```
FMESH4:N GEOM=XYZ
         IMESH=50  IINTS=50    $ 50×50×50 = 125,000 bins
         JMESH=50  JINTS=50
         KMESH=50  KINTS=50
```

**Cylindrical (efficient):**
```
FMESH14:N GEOM=RZT
          IMESH=50  IINTS=25    $ Radial: 25 bins
          JMESH=50  JINTS=50    $ Axial: 50 bins
          KMESH=360 KINTS=36    $ Azimuthal: 36 bins
          c Total: 25×50×36 = 45,000 bins (64% fewer!)
```

**Savings:** Fewer bins, better statistics, same spatial information.

---

## Performance Benchmarks

### Mesh Tally Overhead

**Relative simulation time vs. no mesh tally:**

| Mesh Size | FMESH Overhead | UM Overhead |
|-----------|----------------|-------------|
| 1k bins | +1% | +2% |
| 10k bins | +5% | +10% |
| 100k bins | +10% | +20% |
| 1M bins | +20% | +40% |

**Mesh tallying is relatively cheap** - Most time spent on transport.

### Parallel Scaling

**Speedup with N cores (fast_hist algorithm):**

| Cores | Speedup (no mesh) | Speedup (100k mesh) |
|-------|------------------|---------------------|
| 1 | 1.0× | 1.0× |
| 4 | 3.8× | 3.7× |
| 16 | 14.5× | 13.2× |
| 64 | 52× | 45× |

**Mesh tallies scale well** - Only minor parallel efficiency loss.

---

## Common Mistakes to Avoid

### 1. Too Fine Mesh Without Enough Particles

**Mistake:**
```
FMESH4:N ...
         IINTS=100 JINTS=100 KINTS=100    $ 1 million bins
NPS  1e7    $ Only 10 particles per bin on average
```

**Result:** All bins have 50%+ errors (useless).

**Fix:** Either increase NPS to 1e10 or reduce bins to 50×50×50.

### 2. Mesh Covering Voids

**Mistake:**
```
c Reactor in center (±50 cm), but mesh covers ±500 cm
FMESH14:N ORIGIN=-500 -500 -500
          IMESH=500  IINTS=100
```

**Result:** 90% of bins are zero (air/void), wasted computation.

**Fix:** Match mesh extent to geometry of interest.

### 3. Uniform Mesh in Non-Uniform Problem

**Mistake:**
```
c Shielding problem (exponential attenuation)
c Using uniform bins (same size everywhere)
IMESH=100  IINTS=100
```

**Result:** Good statistics near source, terrible statistics far away.

**Fix:** Use logarithmic or adaptive refinement.

### 4. Ignoring Geometry Symmetry

**Mistake:**
```
c Cylindrical reactor core, using Cartesian mesh
FMESH4:N GEOM=XYZ ...
```

**Result:** Many more bins than needed, worse statistics.

**Fix:** Use RZT cylindrical mesh for cylindrical problems.

### 5. Too Many Energy Bins

**Mistake:**
```
c 100 energy bins for mesh tally
EMESH=1e-10 1.26e-10 1.58e-10 ... 14
```

**Result:** 100× more bins, 100× worse statistics per energy bin.

**Fix:** Use 4-6 energy groups (thermal, epithermal, fast, high).

---

## Summary: Mesh Optimization Checklist

**Before running:**
- [ ] Calculated total bins (X × Y × Z × E × T)
- [ ] Estimated particles per bin (NPS × efficiency / bins)
- [ ] Verified mesh extent matches geometry (no voids)
- [ ] Checked mesh alignment with geometry features
- [ ] Considered cylindrical mesh for symmetric geometry
- [ ] Used adaptive refinement (fine where needed)
- [ ] Limited energy bins to 4-6 groups
- [ ] Plotted geometry with mesh overlay

**After initial run:**
- [ ] Checked statistical quality (errors < 10%)
- [ ] Identified regions with poor statistics
- [ ] Refined mesh in regions of interest
- [ ] Reduced mesh in unimportant regions
- [ ] Considered variance reduction if statistics poor

**For final run:**
- [ ] Used optimized mesh from iterations
- [ ] Sufficient NPS for target error (< 5%)
- [ ] Appropriate algorithm (batch if needed)
- [ ] Output format suitable for visualization (XDMF)

---

## References

- **MCNP Manual:** Chapter 5.11 - Mesh Tallies
- **mcnp-statistics-checker:** Tally quality assessment
- **mcnp-ww-optimizer:** Weight window generation from mesh
- **mcnp-plotter:** Geometry visualization

---

**END OF MESH OPTIMIZATION GUIDE**
