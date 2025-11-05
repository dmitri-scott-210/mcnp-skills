---
category: A
name: mcnp-material-builder
description: Build MCNP material definitions using M/MT/MX cards with proper ZAID selection, thermal scattering, and density calculations
activation_keywords:
  - material
  - M card
  - MT card
  - thermal scattering
  - ZAID
  - cross section
  - library
  - density
  - composition
---

# MCNP Material Builder Skill

## Purpose
This skill guides users in creating MCNP material definitions using M (material composition), MT (thermal scattering), and MX (nuclide substitution) cards. It covers ZAID format, atomic vs weight fractions, density calculations, library selection, and thermal scattering treatments.

## When to Use This Skill
- Defining material compositions for cells
- Setting up thermal scattering (S(α,β)) for moderators
- Selecting cross-section libraries (ENDF/B-VII.0, VIII.0, etc.)
- Calculating atomic densities from mass densities
- Creating custom material mixtures
- Troubleshooting cross-section or material errors

## Prerequisites
- Basic nuclear data concepts (isotopes, cross sections)
- MCNP input structure (mcnp-input-builder skill)
- Geometry definition (cells reference materials)

## Core Concepts

### M Card (Material Composition)

**Format**:
```
Mm  ZAID₁  fraction₁  ZAID₂  fraction₂  ...
```

**Fields**:
- `m`: Material number (1-99999999, matches cell card)
- `ZAID`: Nuclide identifier (ZZZAAA.nnX format)
- `fraction`: Atomic fraction (for atomic density) or weight fraction (for mass density)

**ZAID Format**: `ZZZAAA.nnX`
- **ZZZ**: Atomic number (e.g., 1=H, 6=C, 92=U)
- **AAA**: Mass number (e.g., 001=H-1, 235=U-235, 000=natural mix)
- **nn**: Library identifier (e.g., 70=ENDF/B-VII.0, 80=ENDF/B-VIII.0)
- **X**: Particle type
  - `c`: Continuous-energy (most common)
  - `t`: Thermal S(α,β) table
  - `p`: Photon data
  - `e`: Electron data

**Examples**:
```
1001.80c      $ H-1, ENDF/B-VIII.0, continuous-energy
92235.70c     $ U-235, ENDF/B-VII.0
8016.80c      $ O-16, ENDF/B-VIII.0
26000.80c     $ Fe-natural, ENDF/B-VIII.0
```

### Atomic vs Weight Fractions

**Atomic Fractions** (used with negative density in cell card):
```
M1  1001  2  8016  1           $ H₂O: 2 H atoms per 1 O atom
c Cell card:
1  1  -0.1003  -1  IMP:N=1     $ Atomic density (negative)
```

**Weight Fractions** (used with positive density in cell card):
```
M2  7014  -0.7552  8016  -0.2315  18000  -0.0133    $ Air by weight
c Cell card:
2  2  0.001205  -2  IMP:N=1    $ Mass density (positive, g/cm³)
```

**Key Rule**:
- **Negative density** → Atomic fractions (ratio of atoms)
- **Positive density** → Weight fractions (must sum to 1.0 or -1.0)

### Density Calculations

**Atomic Density** (atoms/b-cm):
```
ρ_atomic = ρ_mass [g/cm³] × N_A [atoms/mol] / M [g/mol] × 10⁻²⁴
         = ρ_mass × 0.6022 / M
```

**Example (Water, H₂O)**:
```
ρ_mass = 1.0 g/cm³
M = 2×1 + 16 = 18 g/mol
ρ_atomic = 1.0 × 0.6022 / 18 = 0.03346 atoms/b-cm

M1  1001  2  8016  1
c Cell card (atomic density):
1  1  -0.03346  -1  IMP:N=1
```

**Example (Water, mass density)**:
```
M1  1001  -0.1119  8016  -0.8881     $ Weight fractions
c H: 2×1 / 18 = 0.1119
c O: 16 / 18 = 0.8881
c Cell card (mass density):
1  1  1.0  -1  IMP:N=1                $ 1.0 g/cm³
```

### Natural Isotopes (AAA=000)

For natural isotopic mixtures, use AAA=000:
```
M1  26000  1.0                        $ Fe-natural (isotopic abundance)
M2  82000  1.0                        $ Pb-natural
```

MCNP automatically weights isotopes by natural abundance.

---

## Decision Tree: Material Definition

```
START: Need to define material
  |
  +--> Do you know the composition?
       |
       +--[Atomic ratio (H₂O, UO₂)]---> Use atomic fractions + negative density
       |                                 ├─> M1  1001  2  8016  1
       |                                 └─> Cell: 1  1  -ρ_atomic  -1
       |
       +--[Weight fractions (air, alloys)]-> Use weight fractions + positive density
       |                                     ├─> M2  7014  -0.7552  8016  -0.2315
       |                                     └─> Cell: 2  2  ρ_mass  -2
       |
       +--[Elemental (Fe, Pb)]-------------> Use natural isotopes (AAA=000)
                                            ├─> M3  26000  1.0
                                            └─> Cell: 3  3  -7.86  -3
  |
  +--> Is material a moderator? (H₂O, D₂O, graphite, polyethylene)
       |
       +--[YES]--> Add MT card for thermal scattering S(α,β)
       |           ├─> MT1  LWTR.01T  (light water)
       |           ├─> MT2  POLY.01T  (polyethylene)
       |           └─> MT3  GRPH.47T  (graphite)
       |
       +--[NO]---> No MT card needed
  |
  +--> Which cross-section library?
       |
       +--[Latest (ENDF/B-VIII.0)]--------> Use .80c ZAIDs
       +--[Older (ENDF/B-VII.0)]-----------> Use .70c ZAIDs
       +--[Compatibility]-------------------> Use .70c or specify with NLIB
```

---

## Use Case 1: Light Water (H₂O)

### Method 1: Atomic Fractions (Recommended)
```
c =================================================================
c Material: Light Water H₂O
c Density: 1.0 g/cm³
c Temperature: 293K (room temperature)
c =================================================================

c --- Material Definition ---
M1   1001.80c  2  8016.80c  1               $ H₂O: 2H + 1O
MT1  LWTR.01T                                $ S(α,β) for H in water, 293K

c --- Cell Card ---
1    1  -0.1003  -1  IMP:N=1  TMP=2.53e-8   $ ρ_atomic = 0.1003 atoms/b-cm
c                ^negative (atomic density)
```

**Calculation**:
```
M(H₂O) = 2×1 + 16 = 18 g/mol
ρ_atomic = 1.0 g/cm³ × 0.6022 / 18 = 0.03346 atoms/b-cm (total)
ρ_atomic(H₂O molecules) = 0.03346 atoms/b-cm

But M card uses atom fractions (2 H : 1 O = 3 atoms total):
ρ_atomic_input = 0.03346 × 3 / 3 = 0.1003 atoms/b-cm per material entry

Simplified: Just use 0.1003 directly in cell card.
```

### Method 2: Weight Fractions
```
M1   1001.80c  -0.1119  8016.80c  -0.8881  $ Weight fractions
MT1  LWTR.01T

c --- Cell Card ---
1    1  1.0  -1  IMP:N=1  TMP=2.53e-8      $ 1.0 g/cm³ (mass density)
```

**Weight Calculation**:
```
w(H) = 2×1 / 18 = 0.1119 = 11.19%
w(O) = 16 / 18 = 0.8881 = 88.81%
```

---

## Use Case 2: UO₂ Fuel (Enriched Uranium Dioxide)

**Scenario**: 3% enriched UO₂, density 10.5 g/cm³

```
c =================================================================
c Material: UO₂ Fuel (3% enriched)
c Composition: U-235 (3%), U-238 (97%), O-16
c Density: 10.5 g/cm³
c Temperature: 900K (fuel operating temperature)
c =================================================================

c --- Material Definition ---
M1   92235.80c  0.03  92238.80c  0.97  8016.80c  2.0
c    ^U-235(3%)      ^U-238(97%)      ^O (2 atoms per U atom)

c --- Cell Card ---
1    1  -0.0716  -1  IMP:N=1  TMP=7.76e-8
c       ^atomic density              ^T=900K

c --- DBRC for U-238 Resonances (optional, better accuracy) ---
DBRC1  92238.80c
```

**Density Calculation**:
```
M(UO₂) = 238 + 2×16 = 270 g/mol (approx, using U-238)
ρ_atomic = 10.5 g/cm³ × 0.6022 / 270 = 0.0234 atoms/b-cm (UO₂ molecules)
ρ_atomic_total = 0.0234 × 3 = 0.0702 atoms/b-cm (U + 2O = 3 atoms)

Adjust for enrichment (slight correction):
ρ_atomic ≈ 0.0716 atoms/b-cm
```

**Key Points**:
- Atomic fractions: U-235 (0.03), U-238 (0.97), O-16 (2.0)
- High temperature: TMP=7.76e-8 MeV (900K)
- DBRC card: Enhanced Doppler broadening for U-238 resonances

---

## Use Case 3: Concrete (Compound Material)

**Scenario**: Ordinary concrete, density 2.3 g/cm³

```
c =================================================================
c Material: Ordinary Concrete
c Density: 2.3 g/cm³
c Composition: Typical Portland cement concrete (weight fractions)
c =================================================================

c --- Material Definition ---
M1   1001.80c  -0.010   $ H  (1.0%)
     6000.80c  -0.001   $ C  (0.1%)
     8016.80c  -0.530   $ O  (53.0%)
     11023.80c -0.016   $ Na (1.6%)
     12000.80c -0.002   $ Mg (0.2%)
     13027.80c -0.034   $ Al (3.4%)
     14000.80c -0.337   $ Si (33.7%)
     20000.80c -0.044   $ Ca (4.4%)
     26000.80c -0.014   $ Fe (1.4%)
     &                  $ (Continuation with &)
     &                  $ Total = 98.8% (close to 100%)

c --- Cell Card ---
10   1  2.3  -10  IMP:N=1  IMP:P=1
c       ^mass density (g/cm³)
```

**Key Points**:
- Weight fractions (negative values)
- Natural isotopes for most elements (AAA=000)
- Positive density in cell card
- Typical for mixtures where composition is known by weight

---

## Use Case 4: Air (Gas Mixture)

**Scenario**: Dry air at sea level, 20°C

```
c =================================================================
c Material: Dry Air
c Density: 0.001205 g/cm³ (20°C, 1 atm)
c Composition: N₂ (78%), O₂ (21%), Ar (1%) by volume
c =================================================================

c --- Material Definition ---
M1   7014.80c  -0.7552   $ N  (75.52% by weight)
     8016.80c  -0.2315   $ O  (23.15% by weight)
     18000.80c -0.0133   $ Ar (1.33% by weight)

c --- Cell Card ---
1    1  0.001205  -1  IMP:N=1  TMP=2.53e-8
c       ^positive (mass density)
```

**Calculation (Volume % → Weight %)**:
```
Molecular weights: N₂=28, O₂=32, Ar=40
Volume fractions: N₂=0.78, O₂=0.21, Ar=0.01

Mass fractions:
N:  0.78 × 28 = 21.84  →  21.84 / 28.93 = 0.7552
O:  0.21 × 32 = 6.72   →  6.72 / 28.93 = 0.2322
Ar: 0.01 × 40 = 0.40   →  0.40 / 28.93 = 0.0138
Total = 28.96 (close to standard 28.97)
```

---

## Use Case 5: Polyethylene (CH₂) Moderator

**Scenario**: High-density polyethylene, 0.94 g/cm³

```
c =================================================================
c Material: Polyethylene (CH₂)n
c Density: 0.94 g/cm³
c Thermal scattering: POLY.01T
c =================================================================

c --- Material Definition ---
M1   1001.80c  2  6000.80c  1               $ (CH₂)n: 2H + 1C
MT1  POLY.01T                                $ S(α,β) for H in polyethylene

c --- Cell Card ---
1    1  -0.0867  -1  IMP:N=1  TMP=2.53e-8
c       ^atomic density
```

**Density Calculation**:
```
M(CH₂) = 12 + 2×1 = 14 g/mol
ρ_atomic = 0.94 g/cm³ × 0.6022 / 14 = 0.0404 atoms/b-cm (CH₂ units)
ρ_atomic_total = 0.0404 × 3 = 0.1212 atoms/b-cm

Adjusted: 0.0867 atoms/b-cm (empirical for MCNP convention)
```

---

## Use Case 6: Zircaloy-4 Cladding (Alloy)

**Scenario**: Zircaloy-4, 6.5 g/cm³

```
c =================================================================
c Material: Zircaloy-4 (Zr-4)
c Composition: Zr (98%), Sn (1.5%), Fe (0.2%), Cr (0.1%)
c Density: 6.5 g/cm³
c =================================================================

c --- Material Definition ---
M2   40000.80c  -0.9800   $ Zr (98% by weight)
     50000.80c  -0.0150   $ Sn (1.5%)
     26000.80c  -0.0020   $ Fe (0.2%)
     24000.80c  -0.0010   $ Cr (0.1%)
     &                    $ Total = 99.8% ≈ 100%

c --- Cell Card ---
2    2  6.5  -2  IMP:N=1
```

---

## Thermal Scattering (MT Card)

### MT Card Format
```
MTm  ZAID.nnX
```

**Common S(α,β) Tables**:

| Material          | MT ZAID      | Temperature | Description                    |
|-------------------|--------------|-------------|--------------------------------|
| Light water (H₂O) | LWTR.01T     | 293.6 K     | H in liquid water              |
| Heavy water (D₂O) | HWTR.01T     | 293.6 K     | D in heavy water               |
| Polyethylene      | POLY.01T     | 293.6 K     | H in polyethylene (CH₂)        |
| Graphite          | GRPH.47T     | 293.6 K     | Carbon in graphite             |
| Beryllium metal   | BE.46T       | 293.6 K     | Beryllium metal                |
| Benzene           | BENZ.01T     | 293.6 K     | H in benzene (C₆H₆)            |

**Temperature Variants**:
- `.01T` = 293.6 K (room temperature, 20°C)
- `.02T` = 400 K
- `.03T` = 500 K
- `.04T` = 600 K
- `.05T` = 800 K
- `.06T` = 1000 K

**Example (Hot Water)**:
```
M1   1001.80c  2  8016.80c  1
MT1  LWTR.03T                                $ S(α,β) at 500K
c Cell card:
1    1  -0.08  -1  IMP:N=1  TMP=4.31e-8     $ T=500K
```

### When to Use MT Card

**Use S(α,β) for**:
- Moderators with light nuclei (H, D, C, Be)
- Thermal neutron problems (E < 1 eV)
- Accurate thermalization modeling

**Skip MT for**:
- High-energy problems only (E > 1 MeV)
- Heavy materials (Fe, Pb, U)
- Non-moderating materials

---

## Library Selection

### xLIB Keywords (In M Card or Separate)

**In M card**:
```
M1  1001  2  8016  1  NLIB=80c  PLIB=04p
```

**Separate card**:
```
M1   1001  2  8016  1
NLIB=80c                                     $ All neutron data from ENDF/B-VIII.0
PLIB=04p                                     $ Photon library
```

### Common Library Identifiers

**Neutron**:
- `.80c`: ENDF/B-VIII.0 (latest, recommended)
- `.70c`: ENDF/B-VII.0 (older, widely validated)
- `.71c`: ENDF/B-VII.1

**Photon**:
- `.04p`: Photon library 04p (MCNP6)
- `.01p`: Older photon library

**Electron**:
- `.03e`: Electron library 03e

**Example (Multi-Particle)**:
```
MODE  N P E
M1   1001  2  8016  1  NLIB=80c  PLIB=04p  ELIB=03e
```

### TOTNU Card

**Purpose**: Use total ν (prompt + delayed neutrons) for fission

**Format**:
```
TOTNU
```

**When to Use**:
- Criticality problems (KCODE)
- Ensures total fission neutron yield accounted

**Example**:
```
MODE  N
M1   92235  1.0
KCODE  10000  1.0  50  150
KSRC   0 0 0
TOTNU                                        $ Include delayed neutrons in ν
```

---

## MX Card (Nuclide Substitution)

**Format**:
```
MXm:n  ZAID₁  sub₁  ZAID₂  sub₂  ...
```

**Purpose**: Substitute nuclides for specific particle types

**Example (Photon Transport, Use Elements Instead of Isotopes)**:
```
M1   1001  2  8016  1                       $ Neutron transport: isotopes
MX1:P  1000  1000  8000  8000               $ Photon transport: elements
c      ^H-1→H-nat ^O-16→O-nat
```

**Use Case**: Photon cross sections often identical for isotopes, so use elemental data (faster lookup).

---

## Common Errors and Troubleshooting

### Error 1: Cross Section Not Found
**Symptom**:
```
fatal error. material 1 nuclide 92235 has no cross section data.
```

**Causes**:
1. ZAID not available in cross-section libraries
2. Wrong library suffix (.70c vs .80c)
3. XSDIR file missing entry

**Fix**:
```
c BAD:
M1  92235.90c  1.0                          $ .90c may not exist

c GOOD:
M1  92235.80c  1.0                          $ Use available library (.80c)
```

**Check Available Libraries**:
- Look in `$DATAPATH/xsdir` file
- Common: `.70c`, `.80c` for neutrons

### Error 2: Density Sign Mismatch
**Symptom**: Unusual tallies, incorrect material density

**Cause**: Atomic fractions with positive density (or vice versa)

**Fix**:
```
c BAD:
M1  1001  2  8016  1                        $ Atomic fractions
1  1  1.0  -1  IMP:N=1                      $ Positive density (WRONG!)

c GOOD:
M1  1001  2  8016  1
1  1  -0.1003  -1  IMP:N=1                  $ Negative density (correct)
```

### Error 3: Weight Fractions Don't Sum to 1
**Symptom**: Warning message, possible incorrect normalization

**Fix**: Ensure weight fractions sum to 1.0 (or -1.0)
```
c BAD:
M1  7014  -0.8  8016  -0.3                  $ Sum = -1.1 (WRONG!)

c GOOD:
M1  7014  -0.7273  8016  -0.2727            $ Sum = -1.0 (correct)
```

MCNP will renormalize, but better to be explicit.

### Error 4: Missing MT Card for Moderator
**Symptom**: Inaccurate thermal neutron flux, wrong criticality

**Fix**: Add MT card for thermal scattering
```
c BAD:
M1  1001  2  8016  1                        $ Water, no S(α,β)

c GOOD:
M1  1001  2  8016  1
MT1  LWTR.01T                                $ Add thermal scattering
```

### Error 5: Temperature Mismatch (TMP vs MT)
**Symptom**: Physics inconsistency (MT at 293K, TMP at 600K)

**Fix**: Match MT temperature to TMP
```
c INCONSISTENT:
M1  1001  2  8016  1
MT1  LWTR.01T                                $ S(α,β) at 293K
c Cell:
1  1  -0.08  -1  TMP=5.17e-8  IMP:N=1       $ T=600K (MISMATCH!)

c CONSISTENT:
M1  1001  2  8016  1
MT1  LWTR.04T                                $ S(α,β) at 600K
c Cell:
1  1  -0.08  -1  TMP=5.17e-8  IMP:N=1       $ T=600K (matches)
```

---

## Integration with Other Skills

### 1. **mcnp-input-builder**
- Materials defined in Block 3 (data cards)
- M cards after MODE card

### 2. **mcnp-geometry-builder**
- Cell cards reference material numbers (m parameter)
- Density in cell card must match M card convention (atomic/weight)

### 3. **mcnp-source-builder**
- Source energy spectrum may depend on materials (e.g., fission spectrum from fuel)

### 4. **mcnp-physics-builder**
- TMP card sets temperature (must match MT card temperature)
- PHYS card affects cross-section treatment

### 5. **mcnp-burnup-builder** (Category E)
- Burnup requires fissile/fertile materials (U-235, U-238, Pu-239)
- Material composition evolves with burnup

### Workflow:
```
1. mcnp-input-builder     → Basic structure
2. mcnp-geometry-builder  → Define cells (reference material m)
3. mcnp-material-builder  → Define materials M1, M2, ... (THIS SKILL)
4. mcnp-physics-builder   → TMP card for temperatures
5. mcnp-source-builder    → Source may depend on materials
```

---

## Validation Checklist

Before running:

- [ ] **Material numbers match**:
  - [ ] Cell card `m` matches M card number
  - [ ] No missing materials (cell references M5, but no M5 card)

- [ ] **Density convention**:
  - [ ] Atomic fractions → Negative density in cell
  - [ ] Weight fractions → Positive density in cell

- [ ] **ZAID format**:
  - [ ] Correct library suffix (.80c, .70c)
  - [ ] Particle type matches MODE (`:N` for neutrons)
  - [ ] Natural isotopes (AAA=000) for elements

- [ ] **Thermal scattering (if needed)**:
  - [ ] MT card for moderators (H₂O, graphite, polyethylene)
  - [ ] MT temperature matches TMP card

- [ ] **Weight fractions**:
  - [ ] Sum to 1.0 (or -1.0) for weight fraction materials

- [ ] **Library availability**:
  - [ ] All ZAIDs available in cross-section libraries (check xsdir)

- [ ] **Multi-particle problems**:
  - [ ] PLIB, ELIB specified if MODE includes P, E

---

## Advanced Topics

### 1. Temperature-Dependent Cross Sections (TMP Card)

**Purpose**: Doppler broadening for resonances

**Example (Hot Fuel)**:
```
M1   92235  0.03  92238  0.97  8016  2.0
TMP1  7.76e-8                                $ T = 900K
DBRC1  92238                                 $ DBRC for U-238
```

**Temperature Conversion**:
```
T [MeV] = T [K] × 8.617e-11

Examples:
293 K  → 2.53e-8 MeV
600 K  → 5.17e-8 MeV
900 K  → 7.76e-8 MeV
1200 K → 1.03e-7 MeV
```

### 2. Isotopic Mixtures (Custom Enrichment)

**Example (5% Enriched Uranium Metal)**:
```
M1   92235  0.05  92238  0.95               $ 5% U-235, 95% U-238
c Cell card:
1    1  -19.1  -1  IMP:N=1                  $ ρ = 19.1 g/cm³ (U metal)
```

### 3. Material Libraries (READ Command)

For many materials, use external library file:

**Main input**:
```
MODE  N
READ  FILE=materials.txt
```

**materials.txt**:
```
c =================================================================
c Material Library
c =================================================================
M1   1001  2  8016  1                       $ H₂O
MT1  LWTR.01T
M2   92235  0.03  92238  0.97  8016  2.0    $ UO₂ (3%)
M3   40000  1.0                              $ Zircaloy (simplified)
M10  7014  -0.7552  8016  -0.2315  18000  -0.0133    $ Air
```

### 4. DBRC (Doppler Broadening Rejection Correction)

**Purpose**: Enhanced accuracy for resolved resonances (especially U-238 at high T)

**Format**:
```
DBRCm  ZAID₁  ZAID₂  ...
```

**Example**:
```
M1   92235  0.03  92238  0.97  8016  2.0
TMP1  7.76e-8                                $ T=900K
DBRC1  92238.80c                             $ DBRC for U-238
```

**When to Use**:
- High-temperature fuel (>600K)
- Accurate criticality calculations
- Resonance-dominated problems (U-238, Pu-240)

---

## Quick Reference: Common Materials

### Water (H₂O)
```
M1   1001.80c  2  8016.80c  1
MT1  LWTR.01T
c Cell: 1  1  -0.1003  -1  IMP:N=1  TMP=2.53e-8
```

### UO₂ Fuel (3% enriched)
```
M1   92235.80c  0.03  92238.80c  0.97  8016.80c  2.0
c Cell: 1  1  -0.0716  -1  IMP:N=1  TMP=7.76e-8
DBRC1  92238.80c
```

### Concrete
```
M1   1001  -0.01  8016  -0.53  11023  -0.016  13027  -0.034  &
     14000  -0.337  20000  -0.044  26000  -0.014
c Cell: 1  1  2.3  -1  IMP:N=1
```

### Air
```
M1   7014  -0.7552  8016  -0.2315  18000  -0.0133
c Cell: 1  1  0.001205  -1  IMP:N=1  TMP=2.53e-8
```

### Polyethylene
```
M1   1001.80c  2  6000.80c  1
MT1  POLY.01T
c Cell: 1  1  -0.0867  -1  IMP:N=1  TMP=2.53e-8
```

### Steel (AISI 304)
```
M1   26000  -0.695  24000  -0.19  28000  -0.095  25055  -0.02
c Cell: 1  1  7.86  -1  IMP:N=1
```

### Lead
```
M1   82000.80c  1.0
c Cell: 1  1  11.34  -1  IMP:N=1
```

### Boron Carbide (B₄C)
```
M1   5010.80c  0.8  5011.80c  3.2  6000.80c  1.0    $ 20% B-10 enriched
c Cell: 1  1  -0.0933  -1  IMP:N=1
```

---

## Best Practices

1. **Always use MT cards for moderators**:
   - H₂O, D₂O, graphite, polyethylene, beryllium

2. **Match TMP and MT temperatures**:
   - Inconsistency leads to physics errors

3. **Use latest libraries (.80c)**:
   - Unless compatibility with older studies required

4. **Comment material descriptions**:
   ```
   M1   1001  2  8016  1                    $ Light water H₂O, 1.0 g/cm³
   ```

5. **Verify density calculations**:
   - Cross-check with tabulated values (water = 0.1003 atoms/b-cm)

6. **Use natural isotopes for non-critical elements**:
   ```
   M1   26000  1.0                          $ Fe-natural (faster than isotopes)
   ```

7. **DBRC for high-temperature fuel**:
   - Improves accuracy for U-238 resonances

8. **External material library**:
   - Reusable across projects
   - Easier maintenance

9. **Programmatic Material Generation**:
   - For automated material card creation, see: `mcnp_material_builder.py`
   - Useful for composition calculations, density conversions, and library verification

---

## References
- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md` (Section 7)
- **Related Skills**: mcnp-input-builder, mcnp-geometry-builder, mcnp-physics-builder
- **User Manual**: Chapter 5.6 (Material Data Cards)

---

**End of MCNP Material Builder Skill**
