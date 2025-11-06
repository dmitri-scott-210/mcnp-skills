# MCNP Example Catalog

**Purpose:** Comprehensive catalog of MCNP examples organized by problem type and documentation source.

**Companion to:** mcnp-example-finder SKILL.md

---

## Documentation Sources

### 1. Criticality Primer (LA-UR-15-29136)

**Location:** `markdown_docs/primers/criticality_primer/`

**Chapter 2: Getting Started**
- Example 1: Bare metal sphere (Godiva) - Critical mass benchmark
- Example 2: Reflected sphere - Effect of reflection on criticality
- Example 3: Cylindrical geometry - Non-spherical criticality
- KCODE card basics, KSRC positioning, Shannon entropy

**Chapter 3-4: Basic Criticality**
- Material definitions for reactor problems
- Control rod modeling
- Thermal scattering (LWTR, HWTR)
- Temperature-dependent cross sections

**Chapter 5: Lattice Problems**
- Example 9: Simple fuel pin lattice (U=1 pin, LAT=1 square lattice)
- Example 10: Fuel assembly (more complex pin arrangements)
- Example 11: Core with control rods (selective fill)
- Universe nesting patterns
- FILL card syntax and array indexing

**Chapter 6-7: Advanced Topics**
- Burnup tracking
- Source convergence diagnostics
- Multi-group cross sections
- Unresolved resonance treatment

---

### 2. Source Primer (LA-UR-13-20140)

**Location:** `markdown_docs/primers/source_primer/`

**Chapter 1: Simple Sources**
- Point isotropic: `SDEF POS=0 0 0 ERG=14.1`
- Directional beam: `SDEF POS=0 0 0 VEC=0 0 1 DIR=1 ERG=14.1`
- Surface source: `SDEF SUR=1 NRM=-1 ERG=14.1`
- Mono-energetic vs. spectrum

**Chapter 2: SDEF Card Details**
- SI/SP card combinations (L, H, A distributions)
- Energy distributions (thermal, fission spectrum, monoenergetic)
- Directional distributions (isotropic, cosine, user-defined)
- Position distributions (point, line, area, volume)
- Dependent sources (FPOS, FERG, FCEL patterns)

**Chapter 3: Volume Sources**
- Cylindrical volume: `SDEF CEL=D1 ERG=14.1` with SI1 cell list
- Uniform vs. biased sampling
- Volume importance in distributed sources
- Rejection sampling for complex volumes

**Chapter 4: Advanced Features**
- User-defined distributions (via file)
- Source transformations (TR card with SDEF)
- Time-dependent sources
- Particle type selection (PAR card)

**Chapter 5: Common Errors**
- Impossible variable dependencies (AXS=FPOS)
- Source outside geometry
- Zero-width energy bins
- Incorrect distribution normalization

---

### 3. Shielding Primer (X-5 Monte Carlo Team)

**Location:** Test suite or example directories

**Chapter 2: Point Source Shielding**
- Simple geometry (sphere source, detector)
- F5 point detector tally
- Distance scaling (1/r²)
- Material effects on attenuation

**Chapter 3: Distributed Sources**
- Line source (rod activation)
- Area source (contaminated surface)
- Volume source (activated equipment)
- Source strength calculations

**Chapter 4: Dose Tallies**
- Flux-to-dose conversion (DE/DF cards)
- ICRP-recommended conversion factors
- Ambient dose equivalent H*(10)
- Effective dose calculation
- Multi-group dose response functions

**Chapter 5: Variance Reduction**
- Importance splitting (IMP cards)
  - Geometric progression rules
  - Typical factors: 2, 4, 8, 16
- Weight windows (WWG card)
  - MESH definition
  - Iterative generation
  - WWINP/WWOUT files
- Geometry splitting
- Energy/time splitting
- DXTRAN spheres for point detectors

---

### 4. User Manual Examples

**Location:** MCNP User Manual (mcnp631_user-manual.pdf)

**Chapter 3: Overview and Examples**

**§3.2: Simple Geometry Examples**
- Sphere: `1 SO 10` (sphere at origin, radius 10)
- Cylinder: `2 CZ 5` (infinite cylinder on Z-axis, radius 5)
- Plane: `3 PZ 0` (XY plane at Z=0)
- Box (RPP): `4 RPP -10 10 -10 10 -10 10`
- Boolean combinations: intersection (space), union (:), complement (#)

**§3.3: Lattice Examples**
- Square lattice (LAT=1): Regular array in X-Y plane
- Hexagonal lattice (LAT=2): Hexagonal packing
- FILL card: Array of universe numbers
- Infinite lattice: FILL without bounds
- Finite lattice: FILL with I/J/K limits

**§3.4: Tally Examples**
- F1 (surface current): `F1:N 10` (current across surface 10)
- F2 (surface flux): `F2:N 10` (average flux across surface)
- F4 (cell flux): `F4:N 5` (average flux in cell 5)
- F5 (point detector): `F5:N 100 0 0 0.1` (detector at 100,0,0 with radius 0.1)
- F6 (energy deposition): `F6:N 5` (energy deposition in cell 5)
- F8 (pulse height): `F8:N 5` (energy distribution of pulses in detector)

**§3.5: Physics Examples**
- Thermal scattering: `MT1 LWTR.20t` (light water S(α,β))
- Photon production: MODE N P with photon cross sections
- Electron transport: MODE N P E
- Energy cutoffs: `CUT:N J 0.001` (1 keV neutron cutoff)

---

### 5. Test Suite Examples

**Location:** MCNP installation directory, typically `MCNP_CODE/testsuite/`

**Verification Problems:**
- Godiva (bare U-235 sphere)
- Jezebel (bare Pu-239 sphere)
- ZPR assemblies (fast critical experiments)
- ZPPR (fast reactor mockups)
- BWR/PWR lattice benchmarks

**Feature Demonstrations:**
- DXTRAN effectiveness
- Weight window generation
- Mesh tally visualization
- Burnup calculations
- Unstructured mesh (UM) geometries

---

## Examples by Problem Category

### Reactor Physics (Criticality)

**Simple Critical Assembly:**
```
Bare U-235 Sphere (Godiva)
Location: Criticality Primer Ch 2, Example 1
Features: KCODE, simple geometry, material definition
Key Cards: KCODE, KSRC, MODE N, M card with U-235
```

**Fuel Pin Lattice:**
```
PWR Pin Cell
Location: Criticality Primer Ch 5, Example 9
Features: Universe, LAT=1, FILL, thermal scattering
Key Cards: U card, LAT, FILL, MT (LWTR)
Structure:
  - U=1: Pin (fuel, gap, clad)
  - U=2: Lattice (LAT=1, FILL with U=1 array)
  - Main cell: FILL=2
```

**Control Rod Insertion:**
```
Assembly with Control Rods
Location: Criticality Primer Ch 5, Example 11
Features: Selective FILL, material changes
Key Pattern: FILL array with different universe numbers for control rod positions
```

---

### Shielding (Fixed-Source)

**Point Source with Detector:**
```
Simple Point-to-Detector
Location: Shielding Primer Ch 2
Features: SDEF point source, F5 detector, distance scaling
Key Cards:
  SDEF  POS=0 0 0  ERG=14.1
  F5:N  100 0 0 1              $ Detector at x=100, radius=1
```

**Deep Penetration Shielding:**
```
Multi-Layer Shield
Location: Shielding Primer Ch 5 (VR chapter)
Features: Importance splitting, weight windows
Key Cards:
  IMP:N  1  2  4  8  16  0     $ Geometric progression
  WWG  5  0                     $ Generate WW for F5 tally
  MESH  GEOM=xyz ...           $ Spatial mesh for WW
```

**Dose Calculation:**
```
Neutron Dose from Source
Location: Shielding Primer Ch 4
Features: F4 flux tally with DE/DF dose conversion
Key Cards:
  F4:N  10                      $ Flux in cell 10
  E4  energy bins
  DE4  energy bins (match E4)
  DF4  dose conversion factors (rem/hr per particle/cm²-s)
```

---

### Geometry Patterns

**Concentric Spheres:**
```
Location: User Manual §3.2
Pattern:
  1  1  -10.0  -1        IMP:N=1    $ Inner sphere
  2  2  -5.0   1 -2      IMP:N=1    $ Shell
  3  3  -1.0   2 -3      IMP:N=1    $ Outer shell
  999  0  3              IMP:N=0    $ Outside
Surfaces:
  1  SO  10
  2  SO  20
  3  SO  30
```

**Repeated Structures (No Lattice):**
```
Location: User Manual §3.3
Pattern using FILL without LAT:
  10  0  -10  FILL=1     IMP:N=1    $ Cell filled with universe 1

  1  1  -1.0  -100  U=1  IMP:N=1    $ Universe 1 definition
  2  0  100     U=1  IMP:N=1        $ Outside in universe 1
```

**Hexagonal Lattice:**
```
Location: Criticality Primer, hexagonal examples
Pattern:
  20  3  -1.0  -20  LAT=2  U=2  FILL=-5:5 -5:5 0:0  ...
Note: LAT=2 for hexagonal packing
FILL indexing different from square lattice
```

---

### Source Examples by Type

**Isotropic Point Source:**
```
SDEF  POS=0 0 0  ERG=14.1
```

**Directional Beam:**
```
SDEF  POS=0 0 0  AXS=0 0 1  DIR=1  ERG=14.1
  (Perfectly aligned with +Z axis)

SDEF  POS=0 0 0  VEC=0 0 1  DIR=D1  ERG=14.1
SI1  0.9  1                            $ Cosine range (slightly off-axis allowed)
SP1  0  1
  (Nearly aligned with +Z, small divergence)
```

**Surface Source (Inward):**
```
SDEF  SUR=1  NRM=-1  ERG=14.1
  (Particles start on surface 1, directed inward)
```

**Volume Source (Uniform in Cell):**
```
SDEF  CEL=1  ERG=D1
SI1  L  0.001  1.0  14.1               $ Thermal, intermediate, fast
SP1     0.6    0.3   0.1               $ Probabilities
```

**Energy Spectrum (Fission):**
```
SDEF  POS=0 0 0  ERG=D1
SI1  H  0 0.1 1 10 20                  $ Histogram bins (MeV)
SP1  D  0 1.0 0.8 0.3 0               $ Watt fission-like spectrum shape
```

**D-T Fusion Source:**
```
SDEF  PAR=1  POS=0 0 0  ERG=14.1  VEC=0 0 1  DIR=D1
SI1  -1  1                             $ Cosine range
SP1  0  1                              $ For isotropic
  OR
SP1  D  0.5  1.5                       $ For anisotropic (forward-peaked)
```

---

### Tally Examples by Type

**F1: Surface Current**
```
F1:N  10                               $ Total current across surface 10
E1  0  0.625e-6  20.0                 $ Thermal and fast groups
```

**F2: Surface Flux**
```
F2:N  10                               $ Average flux across surface 10
FQ2  E F                               $ Print by energy and total flux
```

**F4: Cell Flux**
```
F4:N  5 10 15                         $ Average flux in cells 5, 10, 15
E4  1e-10  100i  20                   $ 100 log-spaced energy bins
```

**F5: Point Detector**
```
F5:N  100 0 0  0.1                    $ Detector at (100,0,0), radius 0.1
F15:N  100 0 10  0.1                  $ Second detector
E5  0  0.625e-6  20.0
```

**F6: Energy Deposition**
```
F6:N  5                                $ Total energy deposition in cell 5
SD6  1.0                               $ Divide by volume (result in MeV/cm³)
```

**F8: Pulse Height**
```
F8:N  10                               $ Detector cell 10
FT8  GEB  a  b  c                     $ Gaussian energy broadening
E8  0  0.1  20                        $ Energy bins for spectrum
```

**FMESH: Mesh Tally**
```
FMESH4:N                               $ Mesh tally based on F4 type
  GEOM=xyz                             $ Cartesian
  ORIGIN=-50 -50 -50
  IMESH=50  IINTS=20                  $ X: -50 to 50, 20 bins
  JMESH=50  JINTS=20                  $ Y: -50 to 50, 20 bins
  KMESH=50  KINTS=20                  $ Z: -50 to 50, 20 bins
```

---

### Variance Reduction Examples

**Importance (IMP) Card:**
```
IMP:N  1  2  4  8  16  32  64  128  0
  (Geometric progression toward detector, factor of 2)
  (Last cell: graveyard with IMP=0)
```

**Weight Windows (Manual):**
```
WWN:N  1.0  0.5  0.25  0.125  ...     $ Lower bounds
WWE:N  2.0  1.0  0.5   0.25   ...     $ Upper bounds (2× lower)
WWP:N  5  3  10  J  J                 $ wupn wpb wwn2 wwg wwge
```

**Weight Window Generator (WWG):**
```
WWG  5  0  1.0                        $ Generate for F5, no iterations, default parameters
c Requires MESH card:
MESH  GEOM=xyz
      ORIGIN=-100 -100 -100
      IMESH=100  IINTS=20
      JMESH=100  JINTS=20
      KMESH=100  KINTS=20
```

**DXTRAN:**
```
DXC  100 0 0  5  1                    $ DXTRAN sphere at (100,0,0), radius 5, contrib to F5:1
PD5  5e-6                             $ Probability of DXTRAN
```

---

## Quick Reference by Feature

| Feature | Primary Source | Chapter/Section |
|---------|---------------|-----------------|
| KCODE basics | Criticality Primer | Ch 2 |
| Lattices | Criticality Primer | Ch 5 |
| Simple sources | Source Primer | Ch 1 |
| SDEF details | Source Primer | Ch 2 |
| Dose tallies | Shielding Primer | Ch 4 |
| Importance | Shielding Primer | Ch 5.1 |
| Weight windows | Shielding Primer | Ch 5.2 |
| F1-F8 tallies | User Manual | §5.6 |
| Geometry | User Manual | §3.2 |
| DE/DF cards | User Manual | §5.7.3 |

---

## References

- **MCNP Primers:** Available in `markdown_docs/primers/`
- **User Manual:** Complete card syntax and examples
- **Test Suite:** Verified benchmark problems

---

**END OF EXAMPLE CATALOG**
