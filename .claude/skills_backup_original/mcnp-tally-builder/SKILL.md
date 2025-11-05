---
category: A
name: mcnp-tally-builder
description: Build MCNP tallies (F1-F8) with energy/time bins, multipliers (FM), and dose functions (DE/DF) for flux, current, and energy deposition
activation_keywords:
  - tally
  - F4
  - F5
  - F6
  - flux
  - current
  - energy deposition
  - dose
  - FM card
  - reaction rate
---

# MCNP Tally Builder Skill

## Purpose
This skill guides users in creating MCNP tallies to score particle flux, current, energy deposition, and other quantities. It covers F-type tallies (F1-F8), energy/time/cosine binning, multipliers for reaction rates (FM), and dose conversion (DE/DF).

## When to Use This Skill
- Measuring particle flux in regions or at detectors
- Calculating energy deposition (heating) in materials
- Computing reaction rates (fission, capture, etc.)
- Converting flux to dose (radiation protection)
- Measuring particle current across surfaces
- Time-dependent or energy-dependent tallies
- Troubleshooting tally errors or poor statistics

## Prerequisites
- MCNP input structure (mcnp-input-builder skill)
- Geometry definition (mcnp-geometry-builder skill)
- Source definition (mcnp-source-builder skill)

## Core Concepts

### F-Type Tallies Overview

| Tally | Type                    | Location          | Units               |
|-------|-------------------------|-------------------|---------------------|
| F1    | Current                 | Surface           | particles           |
| F2    | Flux (area-averaged)    | Surface           | particles/cm²       |
| F4    | Flux (volume-averaged)  | Cell              | particles/cm²       |
| F5    | Flux (point detector)   | Point             | particles/cm²       |
| F6    | Energy deposition       | Cell              | MeV/g               |
| F7    | Fission energy deposition| Cell             | MeV/g               |
| F8    | Pulse height            | Cell              | pulses              |

### Tally Number Convention

**Format**: `Fn:p` where:
- `n`: Tally number (1, 4, 14, 24, 114, etc.)
- `:p`: Particle type (`:N`, `:P`, `:E`, etc.)

**Examples**:
```
F4:N        $ Tally 4, neutrons
F14:P       $ Tally 14, photons
F124:N      $ Tally 124, neutrons
```

**Numbering Scheme** (user choice):
- 1-9: Basic tallies
- 10-99: Standard tallies
- 100-999: Extended tallies

---

## Decision Tree: Tally Selection

```
START: Need to measure quantity
  |
  +--> What quantity?
       |
       +--[Flux]-----------------------> Where?
       |                                 |
       |                                 +--[In cell (average)]-----> F4:N
       |                                 +--[At point (detector)]---> F5:N
       |                                 +--[On surface (average)]---> F2:N
       |
       +--[Current]--------------------> F1:N (surface crossing)
       |
       +--[Energy deposition]-----------> F6:N (heating/dose)
       |
       +--[Fission energy]--------------> F7:N (fission heating only)
       |
       +--[Pulse height]----------------> F8:N (detector response)
       |
       +--[Reaction rate]--------------> F4:N + FM multiplier
  |
  +--> Need energy resolution?
       |
       +--[YES]--> Add E card (energy bins)
       +--[NO]---> Total (integrated over all energies)
  |
  +--> Need time resolution?
       |
       +--[YES]--> Add T card (time bins)
       +--[NO]---> Time-integrated
  |
  +--> Convert to dose?
       |
       +--[YES]--> Add DE/DF cards (flux-to-dose coefficients)
       +--[NO]---> Raw tally units
```

---

## Use Case 1: Volume-Averaged Flux (F4)

**Scenario**: Neutron flux in water sphere

```
c =================================================================
c F4 Tally: Volume-Averaged Neutron Flux
c =================================================================

F4:N  1                                     $ Flux in cell 1
E4    0.01  0.1  1  10  14                 $ Energy bins (MeV)
FC4   Neutron flux in water sphere

c --- Cell Definition ---
1    1  -1.0  -1  IMP:N=1  VOL=4188.79     $ Water sphere, R=10 cm
```

**Key Points**:
- **F4:N**: Volume-averaged flux (particles/cm²)
- **E4**: Energy bins (optional, omit for total)
- **FC4**: Comment (descriptive text in output)
- **VOL**: Volume required for normalization (cm³)

**Output Units**: particles/cm²

---

## Use Case 2: Point Detector (F5)

**Scenario**: Flux at detector location 100 cm from source

```
c =================================================================
c F5 Tally: Point Detector Flux
c =================================================================

F5:N  100 0 0  0.5                          $ Detector at (100,0,0), R=0.5 cm
E5    0.01  0.1  1  10  14                 $ Energy bins
FC5   Neutron flux at detector (100 cm from source)
```

**Format**: `F5:N x y z R`
- `(x, y, z)`: Detector location
- `R`: Exclusion sphere radius (particles within R ignored)

**Key Points**:
- Point-in-space measurement (not volume-averaged)
- Fast computation (next-event estimator)
- Use for detectors far from source

**Output Units**: particles/cm²

---

## Use Case 3: Energy Deposition (F6)

**Scenario**: Heating in steel shield

```
c =================================================================
c F6 Tally: Energy Deposition (Heating)
c =================================================================

F6:N  10                                    $ Energy deposition in cell 10
FM6   (-1 10 -6)                            $ Total heating (KERMA)
FC6   Heating in steel shield (MeV/g)

c --- Cell Definition ---
10   1  7.86  1 -2  IMP:N=1                $ Steel, density=7.86 g/cm³
```

**Key Points**:
- **F6**: Energy deposition (MeV/g)
- **FM6 (-1 m -6)**: Total heating multiplier
  - `-1`: Normalization factor
  - `m`: Material number
  - `-6`: MT number for total heating (KERMA)

**Output Units**: MeV/g (convertible to W, Gy, etc.)

---

## Use Case 4: Surface Current (F1)

**Scenario**: Particles crossing shield boundary

```
c =================================================================
c F1 Tally: Surface Current
c =================================================================

F1:N  10                                    $ Current across surface 10
C1    -1  0  1                              $ Cosine bins (backward, normal, forward)
FC1   Neutron current through shield exit

c --- Surface Definition ---
10   SO  110                                $ Sphere R=110 cm
```

**Key Points**:
- **F1**: Particle current (number crossing surface)
- **C1**: Cosine bins (optional)
  - `-1`: Inward (μ<0)
  - `0`: Tangent (μ=0)
  - `1`: Outward (μ>0)

**Output Units**: particles

---

## Use Case 5: Flux with Energy Bins (F4 + E)

**Scenario**: Energy spectrum in detector

```
c =================================================================
c F4 Tally with Energy Bins
c =================================================================

F4:N  1
E4    0.001  0.01  0.1  1  10              $ Energy bins (MeV)
FC4   Neutron energy spectrum

c Alternative (logarithmic spacing with nI):
E4    1e-8  10I  1                          $ 10 log-spaced bins from 1e-8 to 1 MeV
```

**Energy Bin Shortcuts**:
- `nI`: `n` logarithmically interpolated bins
- `nR`: Repeat value `n` times
- Example: `E4 0.01 5I 1` = 5 log bins from 0.01 to 1 MeV

**Output**: Flux in each energy bin

---

## Use Case 6: Reaction Rate (F4 + FM)

**Scenario**: U-235 fission rate in fuel

```
c =================================================================
c Reaction Rate: U-235 Fission
c =================================================================

F4:N  1                                     $ Flux in fuel cell
FM4   1  1  -2                              $ Reaction rate multiplier
c     ^  ^  ^
c     C  m  MT
c     C=1: Constant multiplier
c     m=1: Material 1
c     MT=-2: ν̄σ_f (nu-bar × fission cross section)
FC4   U-235 fission rate (fissions/cm³/source particle)

c --- Material Definition ---
M1   92235  1.0                             $ Pure U-235
```

**FM Card Format**: `FMn C m₁ r₁ m₂ r₂ ...`
- `C`: Overall constant
- `m`: Material number (-1=all, -2=cell mass)
- `r`: Reaction MT number or special code

**Common MT Numbers**:
- `-1`: χ (fission spectrum)
- `-2`: ν̄σ_f (nu-bar × fission)
- `-6`: Total heating (KERMA)
- `1`: Total cross section
- `2`: Elastic scattering
- `18`: Total fission
- `102`: (n,γ) radiative capture
- `103`: (n,p) proton emission
- `107`: (n,α) alpha emission

**Output**: Reaction rate (reactions/cm³/source particle)

---

## Use Case 7: Dose Conversion (F5 + DE/DF)

**Scenario**: Convert flux to effective dose

```
c =================================================================
c Dose Tally: Flux-to-Dose Conversion
c =================================================================

F5:N  100 0 0  0.5                          $ Point detector
DE5   0.01  0.1  1  10  20                 $ Energy bins (MeV)
DF5   1e-12  5e-12  1e-11  2e-11  3e-11    $ Dose coefficients (Sv·cm²)
FC5   Effective dose at detector (Sv/source particle)
```

**DE/DF Cards**:
- **DE**: Dose energy bins (must match E card if both present)
- **DF**: Dose function (flux-to-dose conversion factors)

**Common Dose Coefficients**:
- ICRP-74 AP (anteroposterior): Effective dose
- ICRP-116: Ambient dose equivalent H*(10)

**Output Units**: Sv/source particle (or mrem, etc.)

**Conversion**:
```
Dose = ∫ Φ(E) × CF(E) dE
```
where Φ(E) = flux, CF(E) = dose coefficient

---

## Use Case 8: Multi-Cell Tally

**Scenario**: Flux in multiple cells

```
c =================================================================
c Multi-Cell Tally: Flux in Three Regions
c =================================================================

F4:N  (1 2 3)  (10 20 30)  (100 200 300)
c     ^inner   ^middle     ^outer
E4    0.01  0.1  1  10
FC4   Flux in inner, middle, outer regions
```

**Grouping with Parentheses**:
- `(1 2 3)`: Sum flux in cells 1, 2, 3 (single tally result)
- `10 20 30`: Separate results for cells 10, 20, 30

**Output**: 6 tally results (3 groups + 3 individual cells)

---

## Use Case 9: Time-Dependent Tally (F4 + T)

**Scenario**: Flux as function of time

```
c =================================================================
c Time-Dependent Tally
c =================================================================

F4:N  1
T4    0  1e2  1e3  1e4  1e5                $ Time bins (shakes)
E4    0.01  0.1  1  10                     $ Energy bins
FC4   Time-dependent neutron flux
```

**T Card**: Time bins in shakes (1 shake = 10⁻⁸ s)

**Output**: Flux in each time and energy bin

---

## Use Case 10: Fission Energy Deposition (F7)

**Scenario**: Heating from fission only

```
c =================================================================
c F7 Tally: Fission Energy Deposition
c =================================================================

F7:N  1                                     $ Fission heating in fuel
FC7   Fission energy deposition (MeV/g)

c --- Fuel Cell ---
1    1  -10.5  -1  IMP:N=1                 $ UO₂ fuel
```

**Key Points**:
- **F7**: Energy from fission reactions only
- No FM card needed (automatic)
- Useful for separating fission vs total heating

**Output Units**: MeV/g

---

## Tally Modifications

### FC (Tally Comment)

**Purpose**: Descriptive text in output

```
F4:N  1
FC4   Neutron flux in water moderator (particles/cm²)
```

### E (Energy Bins)

**Purpose**: Energy-dependent tally

```
E4    0.01  0.1  1  10  20                 $ Specific bins
E4    1e-8  20I  20                        $ 20 log-spaced bins
```

### T (Time Bins)

**Purpose**: Time-dependent tally

```
T4    0  1e2  1e3  1e4                     $ Time bins (shakes)
```

### C (Cosine Bins)

**Purpose**: Angular distribution (F1/F2 tallies)

```
C1    -1  -0.5  0  0.5  1                  $ Cosine bins (μ)
```

### FM (Multiplier)

**Purpose**: Reaction rates, dose rates

```
FM4   1  1  102                            $ (n,γ) capture rate
c     ^  ^  ^
c     C  m  MT
```

**Multiple Reactions**:
```
FM4   1  1  18  1  102                     $ Fission + capture
c        ^mat ^fission ^capture
```

### FS (Segment)

**Purpose**: Subdivide tally by cell/surface

```
F1:N  10
FS1   -1  -2  -3                           $ Segment by cells 1, 2, 3
```

### SD (Segment Divisor)

**Purpose**: Normalize segments

```
F4:N  1  2  3
SD4   1000  2000  3000                     $ Divide by volumes
```

### FU (User Edit)

**Purpose**: Custom tally operations

```
FU4   1  2  3                              $ User-defined function
```

### TF (Tally Fluctuation)

**Purpose**: Statistical analysis

```
TF4   100                                  $ Check convergence every 100 NPS
```

### SF (Scale Factor)

**Purpose**: Multiply tally by constant

```
SF4   1e6                                  $ Scale by 10⁶
```

---

## Common Tally Patterns

### Pattern 1: Basic Flux (No Bins)
```
F4:N  1                                    $ Total flux (all energies)
FC4   Total neutron flux
```

### Pattern 2: Flux Spectrum
```
F4:N  1
E4    0.01  0.1  1  10  20                $ Energy bins
FC4   Neutron flux spectrum
```

### Pattern 3: Heating
```
F6:N  10
FM6   (-1 10 -6)                           $ Total heating
FC6   Energy deposition in shield
```

### Pattern 4: Reaction Rate
```
F4:N  1
FM4   1  1  18                             $ Fission rate
FC4   Fission rate in fuel
```

### Pattern 5: Dose
```
F5:N  100 0 0  0.5
DE5   0.01  0.1  1  10  20
DF5   1e-12  5e-12  1e-11  2e-11  3e-11   $ ICRP-74 AP
FC5   Effective dose at detector
```

### Pattern 6: Multi-Detector
```
F5:N  (50 0 0  0.5)  (100 0 0  0.5)  (150 0 0  0.5)
c      ^detector1     ^detector2       ^detector3
E5    0.01  0.1  1  10
FC5   Flux at three detector locations
```

---

## Common Errors and Troubleshooting

### Error 1: Tally in Zero Importance Cell
**Symptom**: Zero tally result

**Cause**: Tally cell has IMP=0

**Fix**:
```
c BAD:
F4:N  1
1  1  -1.0  -1  IMP:N=0                   $ No particles!

c GOOD:
F4:N  1
1  1  -1.0  -1  IMP:N=1                   $ Active region
```

### Error 2: Missing Volume for F4
**Symptom**: Warning about unknown volume

**Fix**: Specify VOL in cell card
```
c BAD:
F4:N  1
1  1  -1.0  -1  IMP:N=1                   $ VOL unknown (MCNP calculates)

c GOOD:
F4:N  1
1  1  -1.0  -1  IMP:N=1  VOL=4188.79      $ VOL specified
```

### Error 3: Energy Bins Out of Range
**Symptom**: Zero tally or poor statistics

**Cause**: Energy bins don't span source energy

**Fix**:
```
c BAD (14.1 MeV source):
E4    0.01  0.1  1  10                    $ Doesn't include 14.1 MeV!

c GOOD:
E4    0.01  0.1  1  10  15                $ Includes 14.1 MeV
```

### Error 4: Particle Type Mismatch
**Symptom**: Zero tally result

**Cause**: Tally particle doesn't match MODE

**Fix**:
```
c BAD:
MODE  N                                   $ Neutrons only
F4:P  1                                   $ Photon tally (no photons!)

c GOOD:
MODE  N P                                 $ Neutrons + photons
F4:N  1                                   $ Neutron tally
F4:P  1                                   $ Photon tally
```

### Error 5: FM Card Material Mismatch
**Symptom**: Zero tally or warning

**Cause**: FM references material not in tally cell

**Fix**:
```
c BAD:
F4:N  1
FM4   1  2  18                            $ Material 2 not in cell 1!
c Cell:
1  1  -1.0  -1  IMP:N=1                   $ Material 1

c GOOD:
F4:N  1
FM4   1  1  18                            $ Material 1 (correct)
c Cell:
1  1  -1.0  -1  IMP:N=1
```

---

## Integration with Other Skills

### 1. **mcnp-geometry-builder**
- Tally cells/surfaces must exist in geometry
- F4 requires VOL parameter in cell card

### 2. **mcnp-material-builder**
- FM card references material numbers
- Reaction MT numbers depend on isotopes in material

### 3. **mcnp-source-builder**
- Energy bins should span source spectrum
- Tally positions relative to source

### 4. **mcnp-physics-builder**
- Tally particle types must be in MODE
- Energy cutoffs affect tally energy range

### Workflow:
```
1. mcnp-input-builder     → Basic structure
2. mcnp-geometry-builder  → Define cells/surfaces
3. mcnp-material-builder  → Define materials
4. mcnp-source-builder    → Define source
5. mcnp-tally-builder     → Define tallies (THIS SKILL)
6. mcnp-physics-builder   → Physics options
```

---

## Validation Checklist

Before running:

- [ ] **Tally type appropriate**:
  - [ ] F4 for volume flux (requires VOL)
  - [ ] F5 for point detectors
  - [ ] F6 for energy deposition
  - [ ] F1 for surface current

- [ ] **Particle type matches MODE**:
  - [ ] `:N` for neutrons (MODE N)
  - [ ] `:P` for photons (MODE P)

- [ ] **Tally locations exist**:
  - [ ] Cell numbers (F4, F6, F7, F8) defined in geometry
  - [ ] Surface numbers (F1, F2) defined
  - [ ] Point (F5) inside non-zero importance

- [ ] **Energy bins span source**:
  - [ ] E card includes source energies
  - [ ] Or omit E card for total

- [ ] **FM card correct**:
  - [ ] Material number matches tally cell
  - [ ] MT number valid for material isotopes

- [ ] **DE/DF consistent**:
  - [ ] DE bins match E bins (if both present)
  - [ ] DF has n+1 values for n DE bins

- [ ] **Comments added**:
  - [ ] FC card describes tally purpose

---

## Advanced Topics

### 1. Tally Segmentation (FS Card)

**Purpose**: Split tally by cell/surface

```
F1:N  10                                   $ Current through surf 10
FS1   -1  -2  -3                           $ Segment by cells 1, 2, 3
c     ^negative = by cell
```

**Output**: Current through surf 10, segmented by originating cell

### 2. Coincident Tallies (Multiple Particles)

```
F4:N,P  1                                  $ Neutron + photon flux (separate)
c Alternative:
F4:N  1                                    $ Neutron flux
F14:P  1                                   $ Photon flux
```

### 3. User-Defined Functions (FU Card)

**Purpose**: Custom tally combinations

```
FU4   -1  4  14                            $ Sum of tallies 4 and 14
```

### 4. Pulse Height (F8 Tally)

**Purpose**: Energy deposition spectrum (detector response)

```
F8:P  1                                    $ Pulse height in cell 1
E8    0  0.1  0.2  0.5  1  2  5  10       $ Energy deposition bins
FC8   Gamma-ray pulse height spectrum
```

---

## Quick Reference: Tally Types

| Tally | Quantity               | Location | Particle | Units          |
|-------|------------------------|----------|----------|----------------|
| F1    | Current                | Surface  | Any      | particles      |
| F2    | Flux (area-avg)        | Surface  | Any      | particles/cm²  |
| F4    | Flux (volume-avg)      | Cell     | Any      | particles/cm²  |
| F5    | Flux (point)           | Point    | Any      | particles/cm²  |
| F6    | Energy deposition      | Cell     | Any      | MeV/g          |
| F7    | Fission energy         | Cell     | Neutron  | MeV/g          |
| F8    | Pulse height           | Cell     | Any      | pulses         |

## Quick Reference: MT Numbers

| MT   | Reaction               | Description                    |
|------|------------------------|--------------------------------|
| -1   | χ                      | Fission spectrum               |
| -2   | ν̄σ_f                   | Nu-bar × fission               |
| -6   | KERMA                  | Total heating                  |
| 1    | σ_total                | Total cross section            |
| 2    | σ_elastic              | Elastic scattering             |
| 18   | σ_fission              | Total fission                  |
| 102  | (n,γ)                  | Radiative capture              |
| 103  | (n,p)                  | Proton emission                |
| 107  | (n,α)                  | Alpha emission                 |

---

## Best Practices

1. **Start with F4**: Volume-averaged flux (simple, robust)
2. **Add FC comments**: Describe tally purpose
3. **Energy bins**: Match source spectrum or omit for total
4. **VOL parameter**: Always specify for F4 tallies
5. **Multiple tallies**: Different locations, particles, quantities
6. **FM for reactions**: Use material number from tally cell
7. **DE/DF for dose**: Use standard coefficients (ICRP-74, ICRP-116)
8. **Check importance**: Ensure tally regions have IMP≠0
9. **Verify statistics**: Relative error <10% for reliable results
10. **Programmatic Tally Generation**:
    - For automated tally card creation, see: `mcnp_tally_builder.py`
    - Useful for multi-tally setups, energy binning schemes, and dose function applications

---

## References
- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md` (Sections 10, 14)
- **Related Skills**: mcnp-input-builder, mcnp-geometry-builder, mcnp-source-builder, mcnp-mesh-builder (Category E)
- **User Manual**: Chapter 5.9 (Tally Data Cards), Chapter 10.2 (Tally Examples)

---

**End of MCNP Tally Builder Skill**
