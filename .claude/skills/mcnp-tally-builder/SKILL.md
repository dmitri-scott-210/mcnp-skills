---
name: mcnp-tally-builder
description: "Build MCNP tallies (F1-F8) with energy/time bins, multipliers (FM), and dose functions (DE/DF) for flux, current, and energy deposition"
version: "2.0.0"
dependencies: "python>=3.8 (for scripts)"
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

**Tally flags:**
- **Asterisk (*Fn):** Multiply by energy (e.g., *F1 = energy current, *F8 = energy deposition)
- **Plus (+Fn):** Charge tally (e.g., +F1 = charge current, +F8 = electrons=-1, positrons=+1)

### Tally Number Convention

**Format**: `Fn:p` where:
- `n`: Tally number (recommended increments of 10: 4, 14, 24, ...)
- `:p`: Particle type (`:N`, `:P`, `:E`, etc.)
- **Limit:** n ≤ 99,999,999

**Examples**:
```
F4:N        $ Tally 4, neutrons
F14:P       $ Tally 14, photons
F124:N      $ Tally 124, neutrons
```

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
- **C1**: Cosine bins (optional, see `tally_binning_advanced.md` for *C degree option)
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

**Advanced options**: See `tally_binning_advanced.md` for NT (no total), C (cumulative), E0 (default), cyclic time bins (CBEG/CFRQ), and FT FRV (custom reference vector).

**Output**: Flux in each energy bin

---

## Use Case 6: Reaction Rate (F4 + FM)

**Scenario**: U-235 fission rate in fuel

```
c =================================================================
c Reaction Rate: U-235 Fission
c =================================================================

F4:N  1                                     $ Flux in fuel cell
FM4   (-1 1 -6)                             $ Fission rate multiplier
c      ^  ^ ^
c      C  m R
c      C=-1: Atom density → macroscopic
c      m=1: Material 1
c      R=-6: Total fission
FC4   U-235 fission rate (fissions/cm³/source particle)

c --- Material Definition ---
M1   92235  1.0                             $ Pure U-235
```

**FM Card Format**: `FMn (C m₁ R₁) (C m₂ R₂) ...`
- `C`: Normalization constant (use -1 for atom density → macroscopic)
- `m`: Material number
- `R`: Reaction MT number or special code

**Common MT Numbers**:
- `-1`: Total cross section
- `-2`: Absorption
- `-6`: Total fission
- `-7`: Fission ν (neutron multiplicity)
- `-8`: Fission Q (MeV/fission)
- `18`: Total fission (specific MT)
- `102`: (n,γ) radiative capture
- `103`: (n,p) proton emission
- `107`: (n,α) alpha emission
- `16`: (n,2n) reaction

**Complete MT table**: See `fm_reaction_numbers_complete.md` for all reaction numbers including photoatomic, proton, photonuclear, multigroup, and electron stopping powers.

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
- Built-in functions: `DF5 IC=99 IU=2 FAC=-3` for ICRP-60

**Output Units**: Sv/source particle (or mrem, etc.)

**Conversion**:
```
Dose = ∫ Φ(E) × CF(E) dE
```
where Φ(E) = flux, CF(E) = dose coefficient

**Advanced options**: See `dose_and_special_tallies.md` for IC keyword, built-in response functions (Table 5.21), LIN/LOG interpolation, DE0/DF0 defaults, and F8 special features.

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

**Purpose**: Reaction rates, heating multipliers

```
FM4   (-1 1 102)                           $ (n,γ) capture rate
c      ^  ^ ^
c      C  m MT
```

**Multiple Reactions**:
```
FM4   (-1 1 -6)  (-1 1 -2)  (-1 1 16)     $ Fission, capture, (n,2n)
c      ^fission  ^capture   ^(n,2n)
```

**Operators**: Space (multiply), Colon (add), Pound (subtract). See `fm_reaction_numbers_complete.md` for complete operator usage and k=-3 option.

### EM, TM, CM (Histogram Multipliers)

**Purpose**: Per-unit normalization (histogram, not continuous like DE/DF)

```
EM4   0.1  0.9  9  9                       $ Per-MeV multipliers (1/ΔE)
TM4   1e-2  1e-2  1e-2                     $ Per-shake multipliers (1/Δt)
CM1   0.5  0.5  0.5                        $ Per-steradian (F1 only)
```

**Difference from DE/DF**: EM/TM/CM are histogram (step function) applied to bins, while DE/DF is continuous interpolation. See `tally_multipliers_histogram.md` for detailed usage including EM0/TM0/CM0 defaults.

### FS (Segment)

**Purpose**: Subdivide tally by surfaces (doesn't require surfaces in geometry)

```
F4:N  1
FS4   -10  11  12  T                       $ Segment by planes, add Total
c      ^negative sense
```

See `tally_flagging_segmentation.md` for segment bin logic, sense importance, and T option details.

### SD (Segment Divisor)

**Purpose**: Normalize segments by volume/area/mass

```
F4:N  1
FS4   10  20  30
SD4   100  200  300  600                   $ Volumes for 3 segments + total
```

**Hierarchy**: Non-zero SD → VOL/AREA → MCNP calculation → fatal error. See `tally_flagging_segmentation.md` for segment divisor modes.

### FQ (Print Hierarchy)

**Purpose**: Control output table organization

```
FQ4   M E                                  $ Multiplier bins (rows) × Energy (columns)
```

**Default order**: F D U S M C E T (energy × time table). See `dose_and_special_tallies.md` for complete bin type definitions.

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
F14:P  1                                  $ Photon tally
```

### Error 5: FM Card Material Mismatch
**Symptom**: Zero tally or warning

**Cause**: FM references material not in tally cell

**Fix**:
```
c BAD:
F4:N  1
FM4   (-1 2 18)                           $ Material 2 not in cell 1!
c Cell:
1  1  -1.0  -1  IMP:N=1                   $ Material 1

c GOOD:
F4:N  1
FM4   (-1 1 18)                           $ Material 1 (correct)
c Cell:
1  1  -1.0  -1  IMP:N=1
```

### Error 6: F8 Without Zero/Epsilon Bins
**Symptom**: Normalization loss, incorrect pulse-height distribution

**Cause**: F8 requires zero and epsilon bins

**Fix**:
```
c BAD:
F8:P  10
E8    0.1  0.5  1.0  2.0                  $ Missing zero/epsilon!

c GOOD:
F8:P  10
E8    0  1E-5  1E-3  0.1  0.5  1.0  2.0   $ Zero and epsilon bins included
```

See `dose_and_special_tallies.md` for complete F8 requirements, variance reduction restrictions, and asterisk/plus flagging details.

---

## Advanced Topics

### 1. Radiography Tallies (FIP, FIR, FIC)

**Purpose**: Create images from transmitted particles

- **FIP**: Pinhole image (point detector as camera)
- **FIR**: Planar radiograph (rectangular grid)
- **FIC**: Cylindrical radiograph (unrolled cylinder)

Uses FS/C cards for grid definition. See `advanced_tally_types.md` for complete specifications, NOTRN card usage, and gridconv utility.

### 2. Flagging (CF/SF)

**Purpose**: Track particle history through specific regions

```
F4:N  10
CF4   -5  -6                               $ Flag particles colliding in cells 5, 6
SF4   20  30                               $ Flag particles crossing surfaces 20, 30
```

Creates second tally output for flagged contributions. Negative cell requires collision before flagging. See `tally_flagging_segmentation.md`.

### 3. Repeated Structures Tallies

**Purpose**: Tally individual lattice elements

```
F4:N  10[0 0 0]                            $ Single element [i j k]
F4:N  10[0:2 0:2 0:0]                     $ Range (3×3 slice)
F4:N  (1<10[0 0 0]<20)                    $ Lattice tally chain
F4:N  U=5                                  $ All cells filled by universe 5
```

See `repeated_structures_tallies.md` for bracket notation, lattice chains, SPDTL optimization, and SD card modes for repeated structures.

### 4. Segmentation Without Extra Geometry

**Purpose**: Subdivide cell spatially without defining extra cells

```
F4:N  1
FS4   -10  11  12  T                       $ Segment cell 1 by surfaces 10,11,12
SD4   698  1396  1396  698  4189          $ Volumes for each segment + total
```

Surfaces don't need to be in geometry. See `tally_flagging_segmentation.md` for segment bin logic and hierarchy.

### 5. Special Tally Treatments (FT Card)

**FT options** (21 total):
- **PHL**: Pulse-height light (scintillators, gas detectors)
- **CAP**: Coincidence capture (neutron multiplicity)
- **RES**: Residual nuclides (heavy-ion production)
- **TAG**: Tally tagging (track production history)
- **FRV**: Fixed reference vector (custom C card reference)
- **GEB**: Gaussian energy broadening (detector resolution)
- **ICD**: Identify contributing cell
- **PDS**: Point detector sampling (pre-collision estimator)

See `dose_and_special_tallies.md` for complete FT option descriptions and usage.

### 6. Pulse Height (F8)

**Requirements**:
- Zero and epsilon bins: `E8 0 1E-5 1E-3 ...`
- Variance reduction: WWG NOT allowed (fatal error)
- Cannot use: DE/DF cards, flagging bins, multiplier bins

**Flags**:
- `*F8`: Energy deposition tally
- `+F8`: Charge deposition

See `dose_and_special_tallies.md` for microscopic realism requirements, union tally behavior, and RR control.

---

## Integration with Other Skills

### 1. **mcnp-geometry-builder**
- Tally cells/surfaces must exist in geometry
- F4 requires VOL parameter in cell card
- FS segmenting surfaces don't need to be in geometry (can be auxiliary)

### 2. **mcnp-material-builder**
- FM card references material numbers
- Reaction MT numbers depend on isotopes in material
- Materials can be "off-geometry" for FM cards

### 3. **mcnp-source-builder**
- Energy bins should span source spectrum
- Tally positions relative to source
- Source time dependence → T card bins

### 4. **mcnp-physics-builder**
- Tally particle types must be in MODE
- Energy cutoffs affect tally energy range
- Analog capture required for some FT options

### 5. **mcnp-variance-reducer**
- WWG optimizes for TF-selected bin
- F8 restrictions (no WWG, use WWN)
- Point detector PDS option (FT PDS)

### Workflow:
```
1. mcnp-input-builder     → Basic structure
2. mcnp-geometry-builder  → Define cells/surfaces
3. mcnp-material-builder  → Define materials
4. mcnp-source-builder    → Define source
5. mcnp-tally-builder     → Define tallies (THIS SKILL)
6. mcnp-physics-builder   → Physics options
7. mcnp-input-validator   → Validate before running
```

---

## References

**Detailed Information:**
See **root skill direcroy** for comprehensive specifications:

- **Advanced Tally Types** (`advanced_tally_types.md`)
  - Radiography tallies: FIP (pinhole), FIR (planar), FIC (cylindrical)
  - Grid definition with FS/C cards
  - NOTRN card integration for direct-only contributions
  - Gridconv utility for image conversion

- **Tally Flagging and Segmentation** (`tally_flagging_segmentation.md`)
  - CF card: Cell flagging (negative = requires collision)
  - SF card: Surface flagging
  - FS card: Tally segmentation creating K+1 bins
  - SD card: Segment divisor hierarchy
  - Segment order and sense importance

- **Repeated Structures Tallies** (`repeated_structures_tallies.md`)
  - Bracket notation: `[i j k]`, `[i1:i2 j1:j2 k1:k2]`
  - Universe format: `U=#`
  - Lattice tally chains with `<` operator
  - SPDTL card for performance
  - SD card modes for repeated structures

- **Tally Binning Advanced** (`tally_binning_advanced.md`)
  - E card options: NT (no total), C (cumulative), E0 (default)
  - T card cyclic time: CBEG, CFRQ, COFI, CONI, CSUB, CEND
  - C card: *C format for degrees, FT FRV custom vector
  - Grazing angle approximation (DBCN 24th entry)

- **Tally Multipliers Histogram** (`tally_multipliers_histogram.md`)
  - EM card: Energy-dependent histogram (requires E card)
  - TM card: Time-dependent histogram (requires T card)
  - CM card: Cosine-dependent histogram (F1/F2, requires C card)
  - EM0, TM0, CM0: Default multipliers
  - Per-unit-energy/time/steradian use cases

- **FM Reaction Numbers Complete** (`fm_reaction_numbers_complete.md`)
  - Complete Table 5.19 from Chapter 5.09
  - Neutron reactions: R = -1 to -8
  - Photoatomic reactions: R = -1 to -6
  - Proton, photonuclear reactions
  - Multigroup reactions
  - Electron stopping powers: R = 1-13
  - k=-3 option: Microscopic cross section
  - PERT card interaction with FM

- **Dose and Special Tallies** (`dose_and_special_tallies.md`)
  - DE/DF built-in response functions (IC keyword, Table 5.21)
  - IC=99: ICRP-60 dose conversion factors
  - IU keyword: Units (1=rem/h, 2=Sv/h)
  - FAC keyword: Normalization factor
  - F8 pulse-height special details (zero/epsilon bins, variance reduction, forbidden cards)
  - FT special treatments: PHL, CAP, RES, TAG, FRV, GEB, ICD, PDS
  - FQ print hierarchy: F D U S M C E T bin types

**Templates and Examples:**
See `` subdirectory:

- **Example Tallies** (`example_tallies/`)
  - 01_basic_flux_spectrum.i (F4 + E + SD)
  - 02_point_detector_dose.i (F5 + DE/DF)
  - 03_reaction_rates.i (F4 + FM)
  - 04_segmented_tally.i (F4 + FS + SD)
  - 05_pulse_height_detector.i (F8 with zero/epsilon)
  - 06_lattice_element_tally.i (bracket notation)
  - Each with detailed description file

**Automation Tools:**
See `scripts/` subdirectory:

- **tally_validator.py** - Validates tally cards before running MCNP
  - Checks F card references to valid cells/surfaces
  - Validates energy bins monotonically increasing
  - Verifies FM card material references
  - Checks DE/DF entry count matching
  - Validates FS/SD compatibility
  - Usage: `python tally_validator.py input.i`

- **dose_function_plotter.py** - Plots flux-to-dose conversion factors
  - Extracts DE/DF cards from input files
  - Built-in ICRP-74 AP neutron factors
  - Plots response functions on log-log scale
  - Usage: `python dose_function_plotter.py input.i 14`

- **README.md** - Script usage documentation and integration examples

**External Documentation:**
- MCNP6 User Manual, Chapter 5.9: Tally Data Cards
- MCNP6 User Manual, Chapter 10.2: Tally Examples

---

## Best Practices

1. **Start with F4**: Volume-averaged flux (simple, robust)
2. **Add FC comments**: Describe tally purpose for output clarity
3. **Energy bins**: Match source spectrum or omit for total
4. **VOL parameter**: Always specify for F4 tallies
5. **Multiple tallies**: Different locations, particles, quantities
6. **FM for reactions**: Use c=-1 for per-cm³ rates, verify material number matches cell
7. **DE/DF for dose**: Use standard coefficients (ICRP-74, ICRP-116, IC=99)
8. **Check importance**: Ensure tally regions have IMP≠0
9. **Verify statistics**: Relative error <10% for reliable results (use mcnp-statistics-checker)
10. **Use automation tools**: `tally_validator.py` before running, `dose_function_plotter.py` to verify response functions

---

**End of MCNP Tally Builder Skill**
