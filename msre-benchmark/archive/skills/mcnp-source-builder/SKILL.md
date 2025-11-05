---
name: mcnp-source-builder
description: Build MCNP source definitions using SDEF/KCODE/SSR with spatial, energy, and directional distributions
version: "2.0.0"
dependencies: "mcnp-input-builder, mcnp-geometry-builder"
---

# MCNP Source Builder Skill

## Purpose
This skill guides users in creating MCNP source definitions using SDEF (fixed source), KCODE (criticality), and SSR/SSW (surface source read/write) cards. It covers spatial distributions, energy spectra, directional sampling, and source distributions using SI/SP cards.

## When to Use This Skill
- Defining particle sources for transport simulations
- Setting up criticality calculations (eigenvalue problems)
- Creating energy spectra (monoenergetic, continuous, fission)
- Specifying source geometry (point, surface, volume)
- Setting directional distributions (isotropic, beamed, cosine)
- Reusing sources from previous calculations (SSR/SSW)
- Troubleshooting source sampling errors

## Prerequisites
- MCNP input structure (mcnp-input-builder skill)
- Geometry definition (mcnp-geometry-builder skill)
- Understanding of problem type (fixed source vs criticality)

## Core Concepts

### Fixed Source vs Criticality

**Fixed Source** (SDEF):
- User specifies source (position, energy, direction)
- Particle histories simulated from defined source
- Uses NPS card for termination
- Example: Shielding, detector response, activation

**Criticality** (KCODE):
- Self-sustaining fission chain reaction
- Source evolves from fission neutrons
- Eigenvalue problem (solve for keff)
- Uses KCODE card (no SDEF, no NPS)
- Example: Reactor cores, critical assemblies

### SDEF Card (Fixed Source Definition)

**Format**:
```
SDEF  var1=value1  var2=value2  ...
```

**Common Variables**:
- `POS`: Position (x y z)
- `ERG`: Energy (MeV) or distribution number
- `DIR`: Cosine of angle from reference direction
- `VEC`: Reference direction vector (ux uy uz)
- `PAR`: Particle type (N, P, E, etc.)
- `CEL`: Source cell number
- `SUR`: Source surface number
- `X`, `Y`, `Z`: Position distributions
- `RAD`: Radial distribution
- `EXT`: Axial extent distribution
- `AXS`: Axis for cylindrical sources

### SI/SP Cards (Source Information/Probability)

**SI** (Source Information): Defines distribution bins or values
**SP** (Source Probability): Specifies probabilities or function types

**Format**:
```
SDEF  VAR=Dn
SIn   list of values
SPn   list of probabilities or function code
```

---

## Decision Tree: Source Definition

```
START: Need to define source
  |
  +--> What problem type?
       |
       +--[Fixed Source]-----> Use SDEF card
       |                      |
       |                      +--> What source geometry?
       |                            |
       |                            +--[Point]-------> SDEF POS=x y z
       |                            +--[Surface]-----> SDEF SUR=n RAD=Dn
       |                            +--[Volume]------> SDEF CEL=n
       |                            +--[Distributed]--> SDEF X=D1 Y=D2 Z=D3
       |
       +--[Criticality]------> Use KCODE + KSRC cards
                              ├─> KCODE Nsrc k0 Nskip Ncycles
                              └─> KSRC x1 y1 z1  x2 y2 z2  ...
  |
  +--> What energy spectrum?
       |
       +--[Monoenergetic]-------> SDEF ERG=14.1
       +--[Discrete lines]------> SDEF ERG=D1, SI1 L ..., SP1 ...
       +--[Continuous]----------> SDEF ERG=D1, SI1 H ..., SP1 ...
       +--[Fission (Watt)]------> SP1 -3 a b
       +--[Maxwellian]----------> SP1 -4 T
  |
  +--> What direction?
       |
       +--[Isotropic (4π)]------> Omit DIR/VEC (default)
       +--[Monodirectional]-----> SDEF VEC=ux uy uz DIR=1
       +--[Beamed]--------------> SDEF VEC=... DIR=Dn
       +--[Surface normal]------> Implicit with SUR
```

---

## Use Case 1: Point Isotropic Source

**Scenario**: 14.1 MeV neutron point source at origin, isotropic emission

```
c =================================================================
c Point Isotropic Source
c 14.1 MeV neutrons at origin, 4π emission
c =================================================================

SDEF  POS=0 0 0  ERG=14.1  PAR=N
c     ^position  ^energy   ^particle type

NPS  1000000
```

**Key Points**:
- `POS=x y z`: Source position
- `ERG=14.1`: Monoenergetic (14.1 MeV)
- `PAR=N`: Neutron (default, can omit if MODE N only)
- No `DIR`/`VEC`: Isotropic (4π) by default

---

## Use Case 2: Monodirectional Beam

**Scenario**: 1 MeV photon beam along +x axis

```
c =================================================================
c Monodirectional Beam
c 1 MeV photons, collimated beam along +x
c =================================================================

SDEF  POS=-100 0 0  VEC=1 0 0  DIR=1  ERG=1.0  PAR=P
c     ^position     ^direction  ^μ=1  ^energy  ^photon

NPS  1000000
```

**Key Points**:
- `VEC=ux uy uz`: Reference direction (unit vector)
- `DIR=1`: Cosine μ=1 (angle=0°, parallel to VEC)
- Beam originates at x=-100, travels in +x direction

**DIR Parameter**:
- `DIR=1`: μ=1, parallel to VEC (0° cone)
- `DIR=0`: μ=0, perpendicular to VEC (90°)
- `DIR=-1`: μ=-1, antiparallel to VEC (180°)
- `DIR=Dn`: Distribution (e.g., cosine-weighted)

---

## Use Case 3: Surface Source (Disk)

**Scenario**: Uniform neutron source on circular disk (R=10 cm)

```
c =================================================================
c Surface Source (Circular Disk)
c 14.1 MeV neutrons, uniform over disk at z=0
c =================================================================

SDEF  SUR=1  POS=0 0 0  RAD=D1  AXS=0 0 1  ERG=14.1
c     ^surf  ^center   ^radial ^axis(z)   ^energy

SI1   0  10                                $ Radii: 0 to 10 cm
SP1   -21  1                               $ r² weighting (uniform area)

c --- Surface Definition ---
1    PZ  0.0                                $ Disk at z=0

NPS  1000000
```

**Key Points**:
- `SUR=1`: Source on surface 1
- `POS=0 0 0`: Surface center
- `RAD=D1`: Radial distribution (references SI1/SP1)
- `AXS=0 0 1`: Axis normal to surface (z-axis)
- `SP1 -21 1`: Power law r¹ (uniform area sampling)

**Power Law (-21 code)**:
- `SP1 -21 0`: r⁰ (point source at center)
- `SP1 -21 1`: r¹ (uniform area)
- `SP1 -21 2`: r² (weighted to edge)

---

## Use Case 4: Volume Source (Uniform in Cell)

**Scenario**: Uniform volumetric source in cell 1

```
c =================================================================
c Volume Source (Uniform in Cell)
c Fission spectrum neutrons, uniform in cell 1
c =================================================================

SDEF  CEL=1  ERG=D1
c     ^cell  ^energy distribution

SI1   0  20                                $ Energy range 0-20 MeV
SP1   -3  0.988  2.249                     $ Watt fission spectrum

c --- Cell Definition ---
1    1  -1.0  -1  IMP:N=1  VOL=4188.79    $ Sphere R=10 cm

NPS  10000000
```

**Key Points**:
- `CEL=1`: Source uniformly distributed in cell 1
- `ERG=D1`: Energy from distribution 1 (Watt spectrum)
- `SP1 -3 a b`: Watt fission spectrum with parameters a, b

---

## Use Case 5: Distributed Source (Gaussian Spatial)

**Scenario**: Gaussian-distributed source in x, y, z

```
c =================================================================
c Distributed Source (Gaussian)
c 1 MeV neutrons, 3D Gaussian distribution (σ=5 cm)
c =================================================================

SDEF  X=D1  Y=D2  Z=D3  ERG=1.0
c     ^x    ^y    ^z    ^energy

c --- X Distribution (Gaussian, σ=5) ---
SI1   -15  15                              $ Range: μ±3σ
SP1   -21  0  5                            $ Gaussian: mean=0, σ=5

c --- Y Distribution (Same) ---
SI2   -15  15
SP2   -21  0  5

c --- Z Distribution (Same) ---
SI3   -15  15
SP3   -21  0  5

NPS  1000000
```

**Key Points**:
- `X=D1`, `Y=D2`, `Z=D3`: Independent distributions
- `SP1 -21 0 5`: Gaussian (code -21) with μ=0, σ=5

---

## Use Case 6: Discrete Energy Lines

**Scenario**: Multi-line source (e.g., calibration isotope)

```
c =================================================================
c Discrete Energy Source
c Multiple gamma lines (e.g., Co-60: 1.17, 1.33 MeV)
c =================================================================

SDEF  POS=0 0 0  ERG=D1  PAR=P
c                ^energy ^photon

SI1   L  1.173  1.332                      $ List (L) of energies
SP1     0.5     0.5                        $ Equal probability

NPS  1000000
```

**Key Points**:
- `SI1 L`: List (discrete values)
- `SP1`: Probabilities (must sum to 1.0)
- Each history samples one energy

---

## Use Case 7: Continuous Energy Spectrum (Histogram)

**Scenario**: Bremsstrahlung or measured spectrum

```
c =================================================================
c Continuous Energy Spectrum (Histogram)
c User-defined histogram from 0 to 10 MeV
c =================================================================

SDEF  POS=0 0 0  ERG=D1  PAR=P

SI1   H  0  1  2  5  10                    $ Histogram bins (MeV)
SP1     0  1  0.5  0.2  0                  $ Probability density
c       ^  ^  ^    ^    ^
c       E0 E1 E2   E3   E4

NPS  1000000
```

**Key Points**:
- `SI1 H`: Histogram (continuous)
- `SP1`: Probability density at bin edges
- Linear interpolation between points

**Interpretation**:
- 0-1 MeV: Linearly increase from 0 to 1
- 1-2 MeV: Linearly decrease from 1 to 0.5
- 2-5 MeV: Decrease from 0.5 to 0.2
- 5-10 MeV: Decrease from 0.2 to 0

---

## Use Case 8: Watt Fission Spectrum

**Scenario**: U-235 thermal fission neutron spectrum

```
c =================================================================
c Watt Fission Spectrum
c U-235 thermal fission neutrons
c =================================================================

SDEF  CEL=1  ERG=D1

SI1   0  20                                $ Energy range 0-20 MeV
SP1   -3  0.988  2.249                     $ Watt: a=0.988, b=2.249 MeV

NPS  10000000
```

**Watt Spectrum Formula**:
```
f(E) ∝ exp(-E/a) × sinh(√(b×E))
```

**Parameters for Common Fissile Isotopes**:
- **U-235 thermal**: a=0.988, b=2.249
- **Pu-239 thermal**: a=0.966, b=2.383
- **U-235 fast**: a=1.028, b=2.926

**Key Points**:
- `SP1 -3 a b`: Code -3 for Watt spectrum
- `SI1`: Energy range (0 to upper limit, typically 20 MeV)

---

## Use Case 9: Maxwellian Thermal Spectrum

**Scenario**: Thermal neutron source (e.g., from moderator)

```
c =================================================================
c Maxwellian Thermal Spectrum
c Thermal neutrons at T=293K
c =================================================================

SDEF  CEL=1  ERG=D1

SI1   1e-11  0.1                           $ Energy range (MeV)
SP1   -4  2.53e-8                          $ Maxwellian at T=2.53e-8 MeV (293K)

NPS  10000000
```

**Maxwellian Formula**:
```
f(E) ∝ E × exp(-E/kT)
```

**Key Points**:
- `SP1 -4 T`: Code -4 for Maxwellian, T in MeV
- T = 2.53e-8 MeV = 293K (room temperature)

**Temperature Conversion**:
```
T [MeV] = T [K] × 8.617e-11

293K → 2.53e-8 MeV
600K → 5.17e-8 MeV
```

---

## Use Case 10: Directional Distribution (Cosine-Weighted)

**Scenario**: Source emitting preferentially forward

```
c =================================================================
c Cosine-Weighted Directional Source
c Forward-peaked emission (cosine distribution)
c =================================================================

SDEF  POS=0 0 0  VEC=1 0 0  DIR=D1  ERG=1.0
c     ^position  ^ref(+x)   ^dir   ^energy

SI1   -1  1                                $ Cosine range: μ ∈ [-1, 1]
SP1   0   1                                $ Linear: more forward

NPS  1000000
```

**Cosine Distribution**:
- `μ = cos(θ)` where θ = angle from VEC
- `SP1 0 1`: Linear increase (more particles at μ=1)
- Forward hemisphere: μ > 0 (θ < 90°)
- Backward hemisphere: μ < 0 (θ > 90°)

**Alternative (Forward Only)**:
```
SI1   0  1                                 $ μ ∈ [0, 1] (forward only)
SP1   0  1                                 $ Cosine-weighted forward
```

---

## Criticality Source (KCODE + KSRC)

### KCODE Card

**Format**:
```
KCODE  Nsrc  k0  Nskip  Ncycles
```

**Parameters**:
- `Nsrc`: Number of source neutrons per cycle
- `k0`: Initial guess for keff (e.g., 1.0)
- `Nskip`: Number of inactive cycles (discard for convergence)
- `Ncycles`: Total cycles (active = Ncycles - Nskip)

**Example**:
```
KCODE  10000  1.0  50  150
c      ^10k/cycle ^guess ^skip50 ^total150 (100 active)
```

### KSRC Card

**Format**:
```
KSRC  x1 y1 z1  x2 y2 z2  x3 y3 z3  ...
```

**Purpose**: Initial source locations for first cycle

**Example (5 points)**:
```
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0
c     ^center ^±x    ^±x      ^±y     ^±y
```

**Key Points**:
- KSRC only affects first cycle (source converges)
- Typical: 1-10 starting points in/around fissile region
- MCNP iterates to fission source distribution
- No SDEF or NPS with KCODE

---

## Use Case 11: Bare Sphere Criticality

**Scenario**: Pu-239 metal sphere, calculate keff

```
c =================================================================
c Bare Pu-239 Sphere - Criticality Calculation
c Critical radius ≈ 6.4 cm
c =================================================================

c --- Cell Cards ---
1    1  -19.816   -1   IMP:N=1              $ Pu-239 metal
2    0            1    IMP:N=0              $ Graveyard

c --- Surface Cards ---
1    SO  6.385                               $ Critical radius

c --- Data Cards ---
MODE  N
M1   94239.80c  1.0                         $ Pu-239 (pure)
KCODE  10000  1.0  50  150                  $ 10k/cycle, skip 50, 100 active
KSRC   0 0 0  2 0 0  -2 0 0  0 2 0  0 -2 0 $ 5 starting points
PRINT
```

**Key Points**:
- No SDEF (replaced by KCODE)
- No NPS (KCODE controls termination)
- KSRC provides initial guesses (converges quickly)
- Output: keff ± σ (e.g., 1.0000 ± 0.0005)

---

## Surface Source Write/Read (SSW/SSR)

### SSW (Surface Source Write)

**Purpose**: Write particles crossing surfaces to file for later reuse

**Format**:
```
SSW  surf1  surf2  surf3  ...
```

**Example**:
```
c --- Write particles crossing surface 10 ---
SSW  10

c --- Output ---
c Creates file 'wssa' (surface source write file)
```

**Use Cases**:
- Two-stage calculations (generate source → multiple detector configs)
- Variance reduction (generate biased source → reuse)

### SSR (Surface Source Read)

**Purpose**: Read particles from SSW file as source

**Format**:
```
SSR  OLD=filename  NEW=filename  WGTF=factor
```

**Parameters**:
- `OLD`: Input filename (default: `wssa` if `OLD=-1`)
- `NEW`: Output filename (optional, continue writing)
- `WGTF`: Weight factor multiplier

**Example**:
```
c --- Stage 1: Generate surface source ---
c Input: input1.i
SSW  10                                     $ Write to wssa

c --- Stage 2: Reuse surface source ---
c Input: input2.i
SSR  OLD=-1                                 $ Read from wssa (default name)
c No SDEF card (replaced by SSR)
```

---

## Use Case 12: Two-Stage Calculation (SSW/SSR)

**Scenario**: Generate shielding source once, reuse for multiple detector configs

**Stage 1: Generate Source**:
```
c =================================================================
c Stage 1: Generate Surface Source at Shield Exit
c =================================================================

c --- Geometry ---
1    1  -1.0   -1        IMP:N=1           $ Water source region
10   2  -2.3   1  -2     IMP:N=2           $ Concrete shield
20   0         2  -3     IMP:N=4           $ Void (detector region)
999  0         3         IMP:N=0           $ Graveyard

c --- Surfaces ---
1    SO  10                                $ Source boundary
2    SO  110                               $ Shield exit (WRITE HERE)
3    SO  200                               $ Outer boundary

c --- Data ---
MODE  N
M1   1001  2  8016  1
M2   1001  -0.01  8016  -0.53  11023  -0.016  14000  -0.337  20000  -0.044
SDEF  CEL=1  ERG=D1
SI1   0  20
SP1   -3  0.988  2.249                     $ Fission spectrum
SSW  2                                      $ Write particles crossing surf 2
NPS  100000000
```

**Stage 2: Reuse Source**:
```
c =================================================================
c Stage 2: Detector Response Using Surface Source
c =================================================================

c --- Geometry (Detector Config 1) ---
20   0         -2        IMP:N=1           $ Void (source from surf 2)
30   1  -1.0   2  -3     IMP:N=1           $ Water detector
999  0         3         IMP:N=0           $ Graveyard

c --- Surfaces ---
2    SO  110                               $ Surface source location
3    SO  120                               $ Detector boundary

c --- Data ---
MODE  N
M1   1001  2  8016  1
SSR  OLD=-1                                $ Read from wssa
F4:N  30                                   $ Flux in detector
NPS  10000000
```

**Key Points**:
- Stage 1: Expensive (thick shield, 100M histories)
- Stage 2: Fast (reuse source, only transport in detector region)
- Multiple Stage 2 runs with different detector configs

---

## Common Source Distributions (SI/SP Reference)

### Discrete (List)
```
SI1   L  1.0  5.0  10.0  14.1             $ Discrete energies
SP1     0.1  0.3  0.4   0.2               $ Probabilities (sum=1)
```

### Histogram (Continuous)
```
SI1   H  0  1  5  10                      $ Bin edges
SP1     0  1  0.5  0                      $ Probability density
```

### Power Law
```
SP1   -21  n                              $ r^n distribution
c     Code: -21, Exponent: n
```

### Watt Spectrum
```
SI1   0  20
SP1   -3  a  b                            $ Watt fission spectrum
c     Code: -3, Parameters: a, b (MeV)
```

### Maxwellian
```
SI1   1e-11  0.1
SP1   -4  T                                $ Maxwellian at temperature T
c     Code: -4, Temperature: T (MeV)
```

### Evaporation Spectrum
```
SI1   0  20
SP1   -5  T                                $ Evaporation spectrum
c     Code: -5, Temperature: T (MeV)
```

### Gaussian
```
SI1   -15  15
SP1   -21  μ  σ                            $ Gaussian: mean μ, std dev σ
c     Code: -21, Parameters: μ, σ
```

---

## Common Errors and Troubleshooting

### Error 1: Source in Zero Importance Region
**Symptom**:
```
fatal error. source particle not in a cell of nonzero importance.
```

**Cause**: Source position in cell with IMP:N=0

**Fix**:
```
c BAD:
SDEF  POS=0 0 0
c Cell:
1  0  -1  IMP:N=0                         $ Source in graveyard!

c GOOD:
SDEF  POS=0 0 0
c Cell:
1  1  -1.0  -1  IMP:N=1                   $ Source in active region
2  0        1   IMP:N=0                   $ Graveyard outside
```

### Error 2: Source Outside Geometry
**Symptom**: Lost particle at first collision

**Cause**: Source position not inside any cell

**Fix**: Verify POS is inside defined geometry, plot source region

### Error 3: Invalid Probability Distribution
**Symptom**:
```
bad trouble in subroutine source
   probabilities do not sum to unity.
```

**Cause**: SP card probabilities don't sum to 1.0

**Fix**:
```
c BAD:
SI1  L  1  5  10
SP1    0.5  0.3  0.1                      $ Sum = 0.9 (WRONG!)

c GOOD:
SI1  L  1  5  10
SP1    0.5  0.3  0.2                      $ Sum = 1.0 (correct)
```

### Error 4: KCODE with SDEF
**Symptom**: Warning or error about conflicting source

**Fix**: Use KCODE **OR** SDEF, never both
```
c BAD (criticality):
SDEF  POS=0 0 0  ERG=1.0                  $ Don't use SDEF with KCODE!
KCODE  10000  1.0  50  150

c GOOD (criticality):
KCODE  10000  1.0  50  150
KSRC   0 0 0
```

### Error 5: Missing SI/SP for Distribution
**Symptom**: Error referencing undefined distribution

**Fix**: Define SI/SP for all referenced distributions
```
c BAD:
SDEF  ERG=D1                              $ References D1, but no SI1!

c GOOD:
SDEF  ERG=D1
SI1   L  1  5  10
SP1    0.5  0.3  0.2
```

---

## Integration with Other Skills

### 1. **mcnp-geometry-builder**
- Source position (POS, CEL, SUR) must be in defined geometry
- Source in non-zero importance region (IMP:N ≠ 0)

### 2. **mcnp-material-builder**
- Fission spectrum depends on fissile isotope (U-235, Pu-239)
- Source energy affects required cross-section data

### 3. **mcnp-tally-builder**
- Tallies positioned to capture source particles
- Energy bins should span source spectrum

### 4. **mcnp-physics-builder**
- MODE card determines allowed particle types (PAR)
- Source energy affects physics settings (PHYS, CUT)

### Workflow:
```
1. mcnp-input-builder     → Basic structure
2. mcnp-geometry-builder  → Define cells/surfaces (source location)
3. mcnp-material-builder  → Materials (fission spectrum depends on fuel)
4. mcnp-source-builder    → Define source (THIS SKILL)
5. mcnp-tally-builder     → Tallies to capture source response
```

---

## Validation Checklist

Before running:

- [ ] **Source type selected**:
  - [ ] Fixed source: SDEF + NPS
  - [ ] Criticality: KCODE + KSRC (no SDEF, no NPS)

- [ ] **Source position valid**:
  - [ ] POS, CEL, or SUR defined
  - [ ] Inside non-zero importance region (IMP:N ≠ 0)
  - [ ] Inside defined geometry (no gaps)

- [ ] **Energy spectrum defined**:
  - [ ] Monoenergetic: ERG=value
  - [ ] Distribution: ERG=D1 with SI1/SP1 cards

- [ ] **Directional sampling**:
  - [ ] Isotropic: Omit DIR/VEC (default)
  - [ ] Beamed: VEC + DIR specified

- [ ] **Distributions complete**:
  - [ ] All referenced Dn have SIn/SPn cards
  - [ ] Probabilities sum to 1.0 (discrete)

- [ ] **Particle type**:
  - [ ] PAR matches MODE (PAR=N for MODE N)

- [ ] **Termination**:
  - [ ] Fixed source: NPS specified
  - [ ] Criticality: KCODE specified (no NPS)

---

## Advanced Topics

### 1. Multiple Particle Types

**Example (n + γ source)**:
```
MODE  N P
SDEF  POS=0 0 0  PAR=D1  ERG=D2

c --- Particle Type Distribution ---
SI1   L  N  P                             $ Neutron or photon
SP1    0.9  0.1                           $ 90% n, 10% γ

c --- Energy Distribution (Depends on Particle) ---
DS2   S  3  4                             $ Sub-distributions
c     ^S: depends on SI1 (N→3, P→4)

c --- Neutron Energy (Distribution 3) ---
SI3   0  20
SP3   -3  0.988  2.249                    $ Fission spectrum

c --- Photon Energy (Distribution 4) ---
SI4   L  0.662  1.173  1.332             $ Gamma lines
SP4    0.5  0.25  0.25

NPS  1000000
```

### 2. Time-Dependent Source

**Example (Pulsed source)**:
```
SDEF  POS=0 0 0  ERG=14.1  TME=D1

SI1   0  1e-6  2e-6  3e-6                 $ Time bins (shakes)
SP1   0  1     0     0                    $ Pulse at t=1e-6 shakes
c     ^  ^     ^     ^
c     Triangle: 0→1→0
```

### 3. Dependent Distributions (DS Card)

**Purpose**: Link distributions (e.g., energy depends on position)

**Example**:
```
SDEF  CEL=D1  ERG=D2

SI1   L  1  2                             $ Cell 1 or 2
SP1    0.5  0.5

DS2   S  3  4                             $ Energy depends on cell
c     Cell 1 → SI3/SP3, Cell 2 → SI4/SP4

SI3   L  1.0                              $ Cell 1: 1 MeV
SP3    1.0

SI4   L  14.1                             $ Cell 2: 14.1 MeV
SP4    1.0
```

### 4. Biased Source (Variance Reduction)

**Example (Energy biasing)**:
```
SDEF  POS=0 0 0  ERG=D1

SI1   0  0.1  1  10  20                   $ Energy bins
SP1   0  1    1  1   0                    $ Biased distribution
SB1   1  0.1  0.01  0.001  0              $ Bias (weight adjustment)
c     ^Weight: 1/bias to preserve physics
```

---

## Quick Reference: Common Sources

### Point Isotropic (Monoenergetic)
```
SDEF  POS=0 0 0  ERG=14.1
```

### Monodirectional Beam
```
SDEF  POS=-100 0 0  VEC=1 0 0  DIR=1  ERG=1.0
```

### Surface Source (Uniform Disk)
```
SDEF  SUR=1  POS=0 0 0  RAD=D1  AXS=0 0 1  ERG=14.1
SI1   0  10
SP1   -21  1
```

### Volume Source (Cell)
```
SDEF  CEL=1  ERG=D1
SI1   0  20
SP1   -3  0.988  2.249
```

### Fission Spectrum
```
SDEF  CEL=1  ERG=D1
SI1   0  20
SP1   -3  0.988  2.249
```

### Discrete Lines
```
SDEF  POS=0 0 0  ERG=D1
SI1   L  1.173  1.332
SP1    0.5  0.5
```

### Criticality
```
KCODE  10000  1.0  50  150
KSRC   0 0 0  5 0 0  -5 0 0
```

---

## Best Practices

1. **Start simple**: Point isotropic, then add complexity
2. **Verify source position**: Plot geometry, check IMP≠0
3. **Energy spectrum**: Match problem (14.1 MeV for D-T, fission for reactors)
4. **Direction**: Isotropic default (omit DIR/VEC) unless beamed
5. **Criticality**: Use KCODE for eigenvalue, SDEF for fixed source (never both)
6. **SSW/SSR**: Two-stage for expensive shielding calculations
7. **Distributions**: Always check SP sums to 1.0 (discrete)
8. **Comment sources**: Explain energy spectrum, spatial distribution, rationale
9. **Programmatic Source Definition**:
   - For automated source card generation, see: `mcnp_source_builder.py`
   - Useful for complex distributions, parametric studies, and source optimization

---

## References
- **Documentation**: `advanced_source_topics.md`, `source_distribution_reference.md`, `source_error_catalog.md`
- **Related Skills**: mcnp-input-builder, mcnp-geometry-builder, mcnp-material-builder, mcnp-tally-builder
- **User Manual**: Chapter 5.8 (Source Data Cards), Chapter 10.3 (Source Examples)

---

**End of MCNP Source Builder Skill**
