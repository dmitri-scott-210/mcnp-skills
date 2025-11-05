# HTGR Double Heterogeneity and TRISO Particle Modeling

**Reference for:** mcnp-lattice-builder skill
**Source:** AGR-1 experiment (TRISO fuel irradiation test)
**Purpose:** Guidance for modeling TRISO-fueled HTGR systems with lattice structures

---

## Overview

High-Temperature Gas-cooled Reactors (HTGRs) use TRISO (TRIstructural ISOtropic) coated particle fuel. This creates a **double heterogeneity** problem:

1. **Particle-level heterogeneity:** TRISO particles (~1 mm diameter) dispersed in graphite matrix
2. **Compact-level heterogeneity:** Fuel compacts arranged in assemblies/channels

This reference explains how to model TRISO fuel using MCNP lattice structures.

---

## TRISO Particle Structure

### Five-Layer Design

TRISO particles consist of a fuel kernel surrounded by four coating layers:

```
        ___
       /OPyC\      Layer 5: Outer Pyrolytic Carbon (OPyC)
      / SiC  \     Layer 4: Silicon Carbide (SiC)
     / IPyC   \    Layer 3: Inner Pyrolytic Carbon (IPyC)
    / Buffer   \   Layer 2: Buffer (porous carbon)
   |  Kernel   |   Layer 1: Fuel kernel (UO₂, UCO, or UC₂)
    \ Buffer  /
     \ IPyC  /
      \ SiC /
       \OPyC/
        ‾‾‾
```

### Layer Functions

**Layer 1: Fuel Kernel**
- Material: UO₂ (most common), UCO (U-C-O), or UC₂
- Diameter: 350-500 μm typical
- Function: Contains fissile/fertile material
- Density: ~10.9 g/cm³ (UO₂), ~11.0 g/cm³ (UCO)

**Layer 2: Buffer (Porous Carbon)**
- Material: Low-density pyrolytic carbon
- Thickness: 90-110 μm typical
- Function: Absorbs fission gases, accommodates swelling
- Density: ~1.0-1.1 g/cm³

**Layer 3: Inner Pyrolytic Carbon (IPyC)**
- Material: Dense pyrolytic carbon
- Thickness: 35-45 μm typical
- Function: Gas-tight seal, protects buffer from HF/HCl during SiC deposition
- Density: ~1.85-1.90 g/cm³

**Layer 4: Silicon Carbide (SiC)**
- Material: β-SiC (cubic)
- Thickness: 30-40 μm typical
- Function: Primary fission product retention barrier, structural strength
- Density: ~3.18-3.21 g/cm³
- **Most important layer for containment**

**Layer 5: Outer Pyrolytic Carbon (OPyC)**
- Material: Dense pyrolytic carbon
- Thickness: 35-45 μm typical
- Function: Protect SiC from chemical attack, bonding surface for matrix
- Density: ~1.87-1.91 g/cm³

### AGR-1 Example Dimensions

**Baseline compact (Capsules 3 & 6):**
- Kernel radius: 174.85 μm
- Buffer: +104.2 μm (outer radius 279.05 μm)
- IPyC: +38.8 μm (outer radius 317.85 μm)
- SiC: +35.9 μm (outer radius 353.75 μm)
- OPyC: +39.3 μm (outer radius 393.05 μm)
- Total particle diameter: ~786 μm

**Variant 1 compact (Capsule 5):**
- Layer thicknesses slightly different
- Densities slightly different
- Kernel same composition and size

---

## Double Heterogeneity Concept

### First Level: Particle-in-Matrix

**Physical reality:** TRISO particles randomly distributed in graphite (or SiC) matrix

**Particle packing fraction:** Typically 30-50% by volume
- AGR-1: ~40% (estimated from compact specifications)
- Commercial HTGR: 30-40% typical

**Matrix material:**
- Graphite matrix (older designs)
- SiC matrix (advanced designs like AGR-1)
- Density: ~1.2-1.8 g/cm³

**Spatial arrangement:**
- Actual: Stochastic (random positions)
- MCNP model: Regular lattice (computational necessity)

### Second Level: Compact-in-Assembly

**Fuel compact:** Cylindrical or annular pellet containing thousands of TRISO particles in matrix

**Typical compact dimensions:**
- Diameter: 12-25 mm
- Length: 15-50 mm
- Each compact: 1,000-10,000 TRISO particles

**Assembly arrangement:**
- Compacts stacked in fuel channels
- Multiple channels per assembly
- Assemblies arranged in core

---

## Why Regular Lattice is Used

### Computational Necessity

**Problem scale:**
- One HTGR core: millions of TRISO particles
- Example: 10,000 particles/compact × 100 compacts/assembly × 400 assemblies = **400 million particles**

**Explicit modeling:**
- Each particle = 6 cells (kernel + 5 layers)
- 400M particles × 6 cells = 2.4 billion cells
- **NOT computationally feasible**

### Regular Lattice Solution

**Approach:** Arrange TRISO particles in regular (cubic or hexagonal) lattice

**Benefits:**
- One particle universe defined → replicated millions of times
- MCNP repeated structures (U/LAT/FILL)
- Computational cost: ~100-1000× reduction

**Accuracy trade-off:**
- Regular lattice underestimates double heterogeneity effects
- Typical impact: <2% on k-effective, <5% on reaction rates
- **Acceptable for most reactor analyses**

---

## MCNP Implementation: 4-Level Hierarchy

### Level 1: TRISO Particle Universe

**Universe definition:**

```
c ===== Universe 1: TRISO Particle (5 layers) =====
1  1  -10.924  -1         U=1  VOL=0.0000224  IMP:N=1   $ Kernel (UO2)
2  2  -1.100   1 -2      U=1                  IMP:N=1   $ Buffer (C)
3  3  -1.904   2 -3      U=1                  IMP:N=1   $ IPyC (C)
4  4  -3.208   3 -4      U=1                  IMP:N=1   $ SiC (Si+C)
5  5  -1.907   4 -5      U=1                  IMP:N=1   $ OPyC (C)
6  6  -1.297   5         U=1                  IMP:N=1   $ Matrix (SiC)

c ===== Surfaces for TRISO (spherical) =====
1  SO  0.017485   $ Kernel radius
2  SO  0.027905   $ Buffer outer
3  SO  0.031785   $ IPyC outer
4  SO  0.035375   $ SiC outer
5  SO  0.039305   $ OPyC outer
```

**Key points:**
- All surfaces centered at (0,0,0) in universe coordinate system
- Volumes should be per-instance (MCNP counts instances automatically)
- Material numbers can be shared across particles or unique per compact (for depletion tracking)

### Level 2: Matrix Filler Universe

**Purpose:** Fill gaps between TRISO particles in lattice

```
c ===== Universe 2: Matrix-only (no particle) =====
10  6  -1.297  -10  U=2  IMP:N=1   $ Matrix material fills cell

10  SO  1.0   $ Sphere to bound matrix cell (matches lattice element)
```

**Why needed:** Lattice packing <100% → some lattice positions have matrix only, no particle

### Level 3: TRISO Particle Lattice (2D or 3D)

**Purpose:** Create regular array of TRISO particles within compact

**Example: 15×15 rectangular lattice**

```
c ===== Lattice element (cubic cell for each particle/matrix) =====
100  RPP  -0.0437  0.0437  -0.0437  0.0437  -0.05  0.05   $ ~0.874 mm pitch

c ===== Particle lattice =====
1000  0  -100  LAT=1  U=10  FILL=-7:7  -7:7  0:0  IMP:N=1
      2 2 2 2 2 2 1 1 1 2 2 2 2 2 2   $ j=7 (outer ring: matrix only)
      2 2 2 1 1 1 1 1 1 1 1 1 2 2 2   $ j=6
      2 2 1 1 1 1 1 1 1 1 1 1 1 2 2   $ j=5
      2 2 1 1 1 1 1 1 1 1 1 1 1 2 2   $ j=4
      2 1 1 1 1 1 1 1 1 1 1 1 1 1 2   $ j=3
      2 1 1 1 1 1 1 1 1 1 1 1 1 1 2   $ j=2
      1 1 1 1 1 1 1 1 1 1 1 1 1 1 1   $ j=1
      1 1 1 1 1 1 1 1 1 1 1 1 1 1 1   $ j=0 (center)
      1 1 1 1 1 1 1 1 1 1 1 1 1 1 1   $ j=-1
      2 1 1 1 1 1 1 1 1 1 1 1 1 1 2   $ j=-2
      2 1 1 1 1 1 1 1 1 1 1 1 1 1 2   $ j=-3
      2 2 1 1 1 1 1 1 1 1 1 1 1 2 2   $ j=-4
      2 2 1 1 1 1 1 1 1 1 1 1 1 2 2   $ j=-5
      2 2 2 1 1 1 1 1 1 1 1 1 2 2 2   $ j=-6
      2 2 2 2 2 2 1 1 1 2 2 2 2 2 2   $ j=-7 (outer ring: matrix only)
```

**Analysis:**
- 15×15 = 225 total positions
- Universe 1 (particle): ~141 positions (62.7% packing)
- Universe 2 (matrix): ~84 positions (37.3% void)
- Pattern approximates circular cross-section of compact

**Pitch calculation:**
```
Compact diameter: 1.3 cm
15 lattice elements across diameter
Pitch = 1.3 / 15 ≈ 0.087 cm = 0.87 mm
```

### Level 4: Compact Lattice (1D Axial)

**Purpose:** Stack particle lattice layers to create full compact height

```
c ===== Matrix end cap universe =====
2000  6  -1.297  -200  U=20  IMP:N=1   $ Matrix-only top/bottom

200  RPP  -0.65  0.65  -0.65  0.65  -0.0437  0.0437   $ Lattice element height

c ===== Compact lattice (1D axial stacking) =====
10000  0  -1000  LAT=1  U=100  FILL=0:0  0:0  -15:15  IMP:N=1
       20 20 20   $ k=-15,-14,-13 (bottom end caps)
       10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10   $ k=-12 to 11 (particle layers)
       20 20 20   $ k=12,13,14 (top end caps)

1000  RPP  -0.65  0.65  -0.65  0.65  -0.0437  0.0437   $ Same as Level 3 element
```

**Shorthand notation:**
```
FILL=0:0  0:0  -15:15
     20 2R  10 23R  20 2R
```

Meaning: 20 (3×), 10 (24×), 20 (3×) = 3+24+3 = 30 elements (k=-14 to k=15, total 30)

**Total compact height:**
```
31 elements × 0.0874 mm = 2.71 cm
```

---

## Multi-Compact and Assembly Hierarchy

### Level 5: Fuel Channel (Multiple Compacts)

**Layout:** Stack 3-4 compacts with gaps

```
c ===== Stack of 4 compacts in channel =====
100000  0  -10000         98005 -98051  FILL=100  (x1 y1 z1)  IMP:N=1   $ Compact 1
100001  6  -1.297  10001  98005 -98051                        IMP:N=1   $ Gap
100002  0  -10000         98051 -98006  FILL=101  (x1 y1 z2)  IMP:N=1   $ Compact 2
100003  6  -1.297  10001  98051 -98006                        IMP:N=1   $ Gap
[... compacts 3 and 4 ...]

c ===== Cylinders for each compact position =====
10000  RCC  x1 y1 z1  0 0 2.71  0.65   $ Compact 1 cylinder
10001  RCC  x1 y1 z1  0 0 3.00  1.00   $ Gap around compact 1
[... surfaces for compacts 2, 3, 4 ...]

c ===== Axial planes =====
98005  PZ  10.0   $ Bottom of compact 1
98051  PZ  12.71  $ Top of compact 1 / bottom of gap
98006  PZ  15.0   $ Bottom of compact 2
[...]
```

**Flux-based grouping:** Each compact = unique universe for independent depletion

- Compact 1: Universe 100, material m101 (fuel kernel)
- Compact 2: Universe 101, material m102
- Compact 3: Universe 102, material m103
- Compact 4: Universe 103, material m104

**Reason:** Axial flux gradient → different burnup → must track separately

### Level 6: Assembly (Multiple Channels)

**Hexagonal assembly example (19 channels):**

```
c ===== Hex lattice of fuel channels =====
c Each channel contains 4 compacts (Level 5 geometry)

c Define channel universe (contains 4 compacts stacked)
[Universe 200 = channel 1]
[Universe 201 = channel 2]
[...]

c Hexagonal lattice element
20000  RHP  0 0 -190  0 0 380  3.0   $ Hexagonal pitch ~5.2 cm (apothem 3.0)

c Assembly lattice (19 channels)
200000  0  -20000  LAT=2  U=1000  FILL=-2:2  -2:2  0:0  IMP:N=1
                                  200 200 200 200 200   $ j=-2
                                200 201 201 201 200     $ j=-1
                              200 201 202 201 200       $ j=0 (center channel)
                                200 201 201 201 200     $ j=1
                                  200 200 200 200 200   $ j=2
```

**Channel grouping:** Each channel can have unique universe if flux varies radially

### Level 7: Core (Multiple Assemblies)

**Core lattice:**

```
c Core lattice of assemblies
2000000  0  -200000  LAT=2  U=10000  FILL=-3:3  -3:3  0:0  IMP:N=1
         [37 assemblies in hexagonal pattern]

200000  RHP  0 0 -200  0 0 400  10.0   $ Assembly pitch ~17.3 cm (apothem 10.0)
```

---

## Regular vs Stochastic Particle Distribution

### Regular Lattice (Standard Approach)

**Pros:**
- Computationally tractable
- Repeated structures reduce cell count
- Well-defined geometry for visualization/debugging

**Cons:**
- Underestimates double heterogeneity
- Not physically accurate
- May miss resonance shielding effects

**Impact:** Typically <2% on k-effective for HTGR systems

### Stochastic (URAN Card - Advanced)

**MCNP feature:** URAN card for random particle placement

**Syntax:**
```
URAN  dist  radius  mat  [additional parameters]
```

**Limited use:**
- Can only randomize within single cell
- Still requires many cells to represent compact volume
- Computational cost higher

**Recommendation:** Use regular lattice for most analyses. Use URAN for validation/sensitivity studies.

---

## Verification and Validation

### Verification: Regular vs Explicit

**Test case:** Single compact with 1,000 particles

1. **Explicit model:** Each particle = unique position (not repeated structure)
2. **Regular lattice:** TRISO particles in lattice

**Compare:** k-effective, reaction rates, flux distribution

**Expected:** <1% difference for well-designed lattice

### Validation: Comparison to Experiment

**AGR-1 example:**
- Measured dose rates at 1, 30, 365 days after irradiation
- Calculated dose rates using regular TRISO lattice
- Agreement within measurement uncertainty (~10%)

**Key:** Flux-based grouping more important than regular vs stochastic

---

## Best Practices for TRISO Modeling

1. **Use regular lattice** - Computational necessity, acceptable accuracy

2. **4-level hierarchy minimum** - Particle → Particle lattice → Compact → Channel/Assembly

3. **Flux-based compact grouping** - Each compact = unique universe if strong axial gradient

4. **Specify volumes** - VOL card on particle cells (per-instance volume)

5. **Matrix filler universe** - Don't forget to define matrix-only universe for non-particle positions

6. **Verify particle count** - Calculate expected particles per compact, verify lattice produces similar number

7. **Plot geometry** - Visual check that particles don't overlap, lattice truncation correct

8. **Check packing fraction** - Should match physical specifications (~30-50%)

9. **Test convergence** - Verify lattice pitch refinement doesn't change results significantly

10. **Validate** - Compare to measurements or high-fidelity stochastic models when possible

---

## Common Pitfalls

### Pitfall 1: Volume Specification Error

**Wrong:**
```
1  1  -10.924  -1  U=1  VOL=0.092522   $ Looks like total volume of all particles
```

**Issue:** Volume too large (by factor of ~4000)

**Correct:**
```
1  1  -10.924  -1  U=1  VOL=0.0000224   $ Geometric volume of single kernel
```
or
```
1  1  -10.924  -1  U=1  VOL=0.092522   $ Effective volume for source normalization
```

**Rule:** Specify per-instance volume, NOT total. Document if using effective volume.

### Pitfall 2: Missing Matrix Filler

**Wrong:**
```
c Only define particle universe
c Lattice FILL uses universe 1 everywhere
```

**Issue:** Packing fraction = 100% (unrealistic)

**Correct:**
```
c Define both particle and matrix-only universes
c Lattice FILL uses pattern: 1 (particle) and 2 (matrix) appropriately
```

### Pitfall 3: Infinite Universe Cells

**Wrong:**
```
6  6  -1.297  5  U=1  IMP:N=1   $ Matrix extends to infinity in universe 1
```

**Issue:** Lost particles at universe boundary

**Correct:**
```
6  6  -1.297  5 -100  U=1  IMP:N=1   $ Matrix bounded by lattice element

100  RPP  [lattice element bounds]   $ Matches Level 3 lattice element
```

### Pitfall 4: No Flux-Based Grouping

**Wrong:**
```
c All compacts use same fuel material
c 4 compacts × 25 assemblies = 100 compacts, all share material 1
```

**Issue:** 15.6% error in activation (whole-core grouping failure)

**Correct:**
```
c Each compact has unique fuel material
c Compact 1: m101, Compact 2: m102, ... Compact 100: m200
```

### Pitfall 5: Incorrect Lattice Pitch

**Wrong:**
```
c Lattice pitch 2.0 mm, but particle diameter ~0.8 mm
c Pitch / diameter = 2.5 → very loose packing
```

**Issue:** Packing fraction ~16% (should be ~40%)

**Correct:**
```
c Lattice pitch 0.87 mm for particle diameter 0.79 mm
c Pitch / diameter = 1.10 → realistic tight packing
c Packing fraction ~63% in central region, ~40% overall with matrix-only edges
```

---

**END OF HTGR DOUBLE HETEROGENEITY REFERENCE**

For lattice fundamentals, see lattice_fundamentals.md. For flux-based grouping, see flux_based_grouping_strategies.md.
