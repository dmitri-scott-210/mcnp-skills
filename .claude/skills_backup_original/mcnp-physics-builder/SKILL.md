---
category: A
name: mcnp-physics-builder
description: Configure MCNP physics options using MODE/PHYS/CUT/TMP cards for particle transport, energy cutoffs, and temperature-dependent cross sections
activation_keywords:
  - physics
  - MODE
  - PHYS
  - CUT
  - TMP
  - cutoff
  - temperature
  - physics options
  - particle transport
---

# MCNP Physics Builder Skill

## Purpose
This skill guides users in configuring MCNP physics options using MODE (particle types), PHYS (physics parameters), CUT (energy/time cutoffs), TMP (temperature), and other physics cards. It covers single and multi-particle transport, energy ranges, temperature-dependent cross sections, and physics model selection.

## When to Use This Skill
- Specifying particle types for transport (neutron, photon, electron)
- Setting energy cutoffs to improve efficiency
- Configuring temperature-dependent cross sections (Doppler broadening)
- Enabling/disabling specific physics processes
- Multi-particle coupled transport (n-γ, n-γ-e)
- Troubleshooting physics-related errors or unexpected behavior

## Prerequisites
- MCNP input structure (mcnp-input-builder skill)
- Material definitions (mcnp-material-builder skill)
- Understanding of transport physics (neutron, photon, electron)

## Core Concepts

### MODE Card (Particle Types) - REQUIRED

**Format**:
```
MODE  P₁  P₂  P₃  ...
```

**Particle Types**:
- `N`: Neutron
- `P`: Photon (gamma)
- `E`: Electron
- `/` or `|`: Proton
- `H`: Deuteron, triton, He-3, He-4
- `A`: Alpha particle
- `+`: Positron
- `S`: Heavy ions

**Examples**:
```
MODE  N                         $ Neutron-only transport
MODE  N P                       $ Coupled neutron-photon
MODE  N P E                     $ Neutron-photon-electron
MODE  P E                       $ Photon-electron (no neutrons)
```

**CRITICAL**: MODE must be the **first data card** in Block 3.

---

## Decision Tree: Physics Configuration

```
START: Need to configure physics
  |
  +--> What particles?
       |
       +--[Neutrons only]-----------> MODE N
       +--[Neutrons + photons]------> MODE N P (coupled)
       +--[Photons + electrons]-----> MODE P E (coupled)
       +--[All three]---------------> MODE N P E
  |
  +--> Default physics OK?
       |
       +--[YES]--> Omit PHYS/CUT (use defaults)
       +--[NO]---> Specify PHYS and/or CUT cards
  |
  +--> Need energy cutoffs?
       |
       +--[YES]--> Add CUT card (E_min, E_max, T_max)
       +--[NO]---> Use defaults (E_min=0 for neutrons, 0.001 for photons)
  |
  +--> Temperature-dependent?
       |
       +--[YES]--> Add TMP card for each material
       |           └─> Optional: DBRC for enhanced accuracy
       +--[NO]---> Omit TMP (use 293K default)
```

---

## Use Case 1: Neutron-Only Transport (Default Physics)

**Scenario**: Simple neutron shielding problem

```
c =================================================================
c Neutron-Only Transport (Default Physics)
c =================================================================

MODE  N                         $ Neutron transport only

c --- No PHYS/CUT cards needed (defaults are fine) ---
c Default: E_max=100 MeV, E_min=0, T_max=1e33 shakes

c --- Materials ---
M1   1001  2  8016  1           $ Water
MT1  LWTR.01T
M2   1001  -0.01  8016  -0.53  11023  -0.016  14000  -0.337  20000  -0.044  $ Concrete

c --- Source, Geometry, Tallies ---
SDEF  POS=0 0 0  ERG=14.1
F4:N  1
NPS  1000000
```

**Key Points**:
- MODE N: Neutron transport only
- No PHYS/CUT: Use MCNP defaults (good for most cases)
- Defaults: E_max=100 MeV, no energy cutoff, no time cutoff

---

## Use Case 2: Coupled Neutron-Photon Transport

**Scenario**: Neutron transport with photon production (capture gammas, fission gammas)

```
c =================================================================
c Coupled Neutron-Photon Transport
c =================================================================

MODE  N P                       $ Neutron + photon transport

c --- Neutron Physics ---
PHYS:N  100  J  J  1            $ E_max=100 MeV, photon production ON
c           ^emax ^defaults ^iphot=1 (implicit)

c --- Photon Physics ---
PHYS:P  100  1  1  0            $ E_max=100 MeV, electrons=simple
c           ^emax ^ides ^nocoh ^ispn

c --- Energy Cutoffs ---
CUT:N  J  0.001  100  1e5       $ E_min=1 keV, E_max=100 MeV, T_max=1 ms
CUT:P  J  0.01   100  1e5       $ E_min=10 keV
c      ^J=default wc1/wc2

c --- Materials ---
M1   92235  1.0                 $ U-235
M2   1001  2  8016  1           $ Water
MT2  LWTR.01T

c --- Source ---
SDEF  CEL=1  ERG=D1
SI1   0  20
SP1   -3  0.988  2.249          $ Fission spectrum

c --- Tallies ---
F4:N  2                         $ Neutron flux in water
F14:P  2                        $ Photon flux in water

NPS  10000000
```

**Key Points**:
- MODE N P: Coupled transport (neutrons produce photons)
- PHYS:N with iphot=1: Implicit photon production (efficient)
- PHYS:P: Photon physics with electron production
- CUT cards: Energy cutoffs for efficiency

---

## Use Case 3: Photon-Electron Transport (No Neutrons)

**Scenario**: Gamma-ray shielding with electron transport

```
c =================================================================
c Photon-Electron Transport
c =================================================================

MODE  P E                       $ Photon + electron (no neutrons)

c --- Photon Physics ---
PHYS:P  100  2  1  0            $ Detailed electron production
c           ^emax ^ides=2

c --- Electron Physics ---
PHYS:E  100  J  J  1  0         $ Standard electron physics
c           ^emax ^defaults ^iphot

c --- Energy Cutoffs ---
CUT:P  J  0.01   100  1e5       $ Photon: E_min=10 keV
CUT:E  J  0.001  100  1e5       $ Electron: E_min=1 keV

c --- Materials ---
M1   82000  1.0                 $ Lead

c --- Source ---
SDEF  POS=0 0 0  ERG=1.25  PAR=P    $ Co-60 gamma

c --- Tallies ---
F4:P  1                         $ Photon flux
F14:E  1                        $ Electron flux
F6:P,E  1                       $ Energy deposition (both)

NPS  1000000
```

**Key Points**:
- MODE P E: Photon-electron only (no neutrons)
- PHYS:P ides=2: Detailed electron production
- CUT:E: Electron energy cutoff

---

## Use Case 4: Temperature-Dependent Cross Sections

**Scenario**: High-temperature fuel (900K) with Doppler broadening

```
c =================================================================
c Temperature-Dependent Cross Sections
c =================================================================

MODE  N

c --- Materials with Temperatures ---
M1   92235.80c  0.03  92238.80c  0.97  8016.80c  2.0    $ UO₂ fuel
TMP1  7.76e-8                   $ T=900K (fuel operating temperature)
DBRC1  92238.80c                $ Enhanced Doppler for U-238

M2   1001.80c  2  8016.80c  1   $ Water coolant
TMP2  5.17e-8                   $ T=600K (hot coolant)
MT2  LWTR.04T                   $ S(α,β) at 600K

c --- Cell Cards ---
1    1  -10.5  -1  IMP:N=1      $ Fuel (material 1, T=900K)
2    2  -0.7   1 -2  IMP:N=1    $ Coolant (material 2, T=600K)
3    0         2  IMP:N=0       $ Graveyard

c --- Source ---
KCODE  10000  1.0  50  150
KSRC   0 0 0

PRINT
```

**Key Points**:
- TMP card: Temperature in MeV (k*T, k=Boltzmann constant)
- DBRC: Enhanced Doppler Broadening Rejection Correction (U-238 resonances)
- MT temperature must match TMP temperature

**Temperature Conversion**:
```
T [MeV] = T [K] × 8.617e-11

Examples:
293 K  → 2.53e-8 MeV (room temperature)
600 K  → 5.17e-8 MeV
900 K  → 7.76e-8 MeV
1200 K → 1.03e-7 MeV
```

---

## PHYS Card Details

### PHYS:N (Neutron Physics)

**Format**:
```
PHYS:N  emax  j  j  j  j  emcnf  iphot  nodop
```

**Parameters**:
- `emax`: Maximum energy (MeV, default: 100)
- `emcnf`: Multigroup/continuous-energy transition (default: 1e10 = all CE)
- `iphot`: Photon production (0=analog, 1=implicit, default: 0)
- `nodop`: Doppler broadening (0=on, 1=off, default: 0)

**Common Settings**:
```
PHYS:N  100  J  J  1  J  J  J  J
c       ^emax     ^iphot=1 (implicit photons, faster)
```

**When to Use**:
- Change emax if source >100 MeV
- iphot=1 for coupled n-γ (efficiency)
- nodop=1 to disable Doppler (testing only)

### PHYS:P (Photon Physics)

**Format**:
```
PHYS:P  emax  ides  nocoh  ispn  j  nodop
```

**Parameters**:
- `emax`: Maximum energy (MeV, default: 100)
- `ides`: Electron production (0=none, 1=simple, 2=detailed, default: 0)
- `nocoh`: Coherent scattering (0=on, 1=off, -1=on for E<100keV, default: 0)
- `ispn`: Photonuclear (0=off, 1=on for biased, 2=on for all, default: 0)
- `nodop`: Doppler broadening (0=on, 1=off, default: 0)

**Common Settings**:
```
PHYS:P  100  1  1  0  J  J
c       ^emax ^simple-e ^coherent-off ^no-photonuclear
```

**When to Use**:
- ides=1 or 2 if electron transport needed (MODE P E)
- nocoh=1 to disable coherent scattering (speed up low-E photons)
- ispn=1 for high-energy photonuclear reactions (>10 MeV)

### PHYS:E (Electron Physics)

**Format**:
```
PHYS:E  emax  j  j  ides  iphot
```

**Parameters**:
- `emax`: Maximum energy (MeV, default: 100)
- `ides`: Bremsstrahlung sampling (default: 0=detailed)
- `iphot`: Photon production (0=thick-target, 1=detailed, default: 0)

**Common Settings**:
```
PHYS:E  100  J  J  1  0
c       ^emax     ^detailed-brems ^thick-target
```

---

## CUT Card Details

### Format
```
CUT:n  j  emin  emax  tmax  wc1  wc2
```

**Parameters**:
- `emin`: Minimum energy (MeV, default: 0 for neutrons, 0.001 for photons)
- `emax`: Maximum energy (MeV, default: 100)
- `tmax`: Maximum time (shakes, default: 1e33)
- `wc1`, `wc2`: Weight cutoffs (roulette/survival)

**Examples**:
```
CUT:N  J  0.001  100  1e5   $ E_min=1 keV, T_max=1 ms
CUT:P  J  0.01   100  1e5   $ E_min=10 keV
CUT:E  J  0.001  100  1e5   $ E_min=1 keV
```

### When to Use CUT

**Energy Cutoffs (E_min)**:
- **Neutrons**: Typically 0 (thermal important), or 1e-3 (fast problems)
- **Photons**: 0.01 MeV (10 keV) typical for shielding
- **Electrons**: 0.001 MeV (1 keV) typical

**Time Cutoffs (T_max)**:
- Time-dependent problems: Set to physical time of interest
- Pulsed sources: Set to pulse duration + decay time
- Default (1e33 shakes = 1e25 s) is effectively infinite

**Trade-off**:
- **Higher cutoff**: Faster simulation, less accurate (particles killed early)
- **Lower cutoff**: Slower, more accurate (more transport)

---

## TMP Card Details

### Format
```
TMPm  T₁  T₂  T₃  ...
```

**Parameters**:
- `m`: Material number
- `T`: Temperature in MeV (k*T, k=Boltzmann constant)

**Examples**:
```
M1   92235  0.03  92238  0.97  8016  2.0
TMP1  7.76e-8                   $ T=900K (fuel)

M2   1001  2  8016  1
TMP2  2.53e-8                   $ T=293K (water, room temp)
```

### When to Use TMP

**Always Use**:
- High-temperature materials (fuel, coolant in reactors)
- Temperature significantly different from 293K
- Accurate criticality calculations

**Matches MT Card**:
- If MT card used, TMP temperature must match MT temperature
- Example: MT2 LWTR.04T (600K) → TMP2 5.17e-8 MeV (600K)

**Temperature Conversion Table**:
| Temperature (K) | Temperature (MeV) | Application            |
|-----------------|-------------------|------------------------|
| 293             | 2.53e-8           | Room temperature       |
| 400             | 3.45e-8           | Warm water             |
| 600             | 5.17e-8           | Hot coolant            |
| 900             | 7.76e-8           | Fuel operating         |
| 1200            | 1.03e-7           | High-temp fuel         |

---

## DBRC Card (Doppler Broadening Rejection Correction)

### Format
```
DBRCm  ZAID₁  ZAID₂  ...
```

**Purpose**: Enhanced accuracy for resolved resonances at high temperature

**Example**:
```
M1   92235  0.03  92238  0.97  8016  2.0
TMP1  7.76e-8                   $ T=900K
DBRC1  92238.80c                $ DBRC for U-238 resonances
```

### When to Use DBRC

**Recommended**:
- High-temperature fuel (>600K)
- Accurate criticality calculations
- U-238, Pu-240, other resonance-dominated isotopes

**Impact**:
- Improved accuracy: ~50-200 pcm (0.05-0.2% Δk/k)
- Modest computational cost (~10-20% slower)

**Isotopes to Include**:
- **U-238**: Most important (strong resonances)
- **Pu-240**: For MOX fuel
- **Other**: Pu-242, Am-241 (if significant)

---

## ACT Card (Analog Capture)

### Format
```
ACT  option
```

**Options**:
- `FISSION`: Analog treatment of fission
- `NONFISS`: Analog treatment of non-fission reactions

**Default**: All reactions use implicit capture (weight game)

**When to Use**:
- Testing or verification (compare analog vs implicit)
- Rarely needed in production runs

---

## Common Physics Configurations

### Configuration 1: Simple Neutron Shielding
```
MODE  N
c Use defaults (no PHYS/CUT needed)
```

### Configuration 2: Coupled Neutron-Photon
```
MODE  N P
PHYS:N  100  J  J  1            $ Implicit photon production
PHYS:P  100  1  1  0            $ Simple electron, no coherent
CUT:N  J  0.001  100  1e5
CUT:P  J  0.01   100  1e5
```

### Configuration 3: Photon-Electron (Radiography)
```
MODE  P E
PHYS:P  100  2  1  0            $ Detailed electron production
PHYS:E  100  J  J  1  0
CUT:P  J  0.01   100  1e5
CUT:E  J  0.001  100  1e5
```

### Configuration 4: High-Temperature Criticality
```
MODE  N
M1   92235  0.03  92238  0.97  8016  2.0
TMP1  7.76e-8                   $ T=900K
DBRC1  92238.80c
KCODE  10000  1.0  50  150
```

### Configuration 5: Fast Neutron Problem (No Thermalization)
```
MODE  N
CUT:N  J  0.1  100  1e5         $ E_min=0.1 MeV (skip thermal)
c No MT cards (no thermal scattering needed)
```

---

## Common Errors and Troubleshooting

### Error 1: MODE Not First Data Card
**Symptom**:
```
bad trouble in subroutine mcrun
   mode card must precede all data cards.
```

**Fix**: Move MODE to be first data card
```
c BAD:
M1  1001  2  8016  1
MODE  N                         $ MODE must be first!

c GOOD:
MODE  N                         $ First data card
M1  1001  2  8016  1
```

### Error 2: Particle Type Mismatch (Tally vs MODE)
**Symptom**: Zero tally results

**Fix**: Ensure tally particle types in MODE
```
c BAD:
MODE  N                         $ Neutrons only
F4:P  1                         $ Photon tally (no photons!)

c GOOD:
MODE  N P
F4:N  1                         $ Neutron tally
F14:P  1                        $ Photon tally
```

### Error 3: Temperature Mismatch (TMP vs MT)
**Symptom**: Physics inconsistency warning

**Fix**: Match TMP and MT temperatures
```
c BAD:
M1  1001  2  8016  1
MT1  LWTR.01T                   $ S(α,β) at 293K
TMP1  5.17e-8                   $ T=600K (MISMATCH!)

c GOOD:
M1  1001  2  8016  1
MT1  LWTR.04T                   $ S(α,β) at 600K
TMP1  5.17e-8                   $ T=600K (consistent)
```

### Error 4: Cutoff Too High
**Symptom**: Unexpectedly low tally results, physics wrong

**Fix**: Lower energy cutoff or remove CUT card
```
c BAD (thermal problem):
CUT:N  J  1.0  100  1e5         $ E_min=1 MeV (kills thermal!)

c GOOD (thermal problem):
CUT:N  J  0.0  100  1e5         $ E_min=0 (allow thermal)
c OR omit CUT:N entirely
```

### Error 5: Wrong Particle in PHYS
**Symptom**: Error or warning

**Fix**: PHYS particle must be in MODE
```
c BAD:
MODE  N                         $ Neutrons only
PHYS:P  100  1  1  0            $ Photon physics (no photons!)

c GOOD:
MODE  N P
PHYS:N  100  J  J  1
PHYS:P  100  1  1  0
```

---

## Integration with Other Skills

### 1. **mcnp-material-builder**
- TMP card sets temperature for materials
- DBRC references isotopes in M cards
- MT card temperature must match TMP

### 2. **mcnp-source-builder**
- Source energy affects PHYS emax parameter
- CUT energy cutoffs affect source particle fate

### 3. **mcnp-tally-builder**
- MODE determines allowed tally particle types (`:N`, `:P`, `:E`)
- CUT energy cutoffs affect tally energy range

### Workflow:
```
1. mcnp-input-builder     → Basic structure
2. mcnp-geometry-builder  → Define cells/surfaces
3. mcnp-material-builder  → Define materials
4. mcnp-physics-builder   → Set MODE, PHYS, CUT, TMP (THIS SKILL)
5. mcnp-source-builder    → Define source
6. mcnp-tally-builder     → Define tallies
```

---

## Validation Checklist

Before running:

- [ ] **MODE card first**:
  - [ ] MODE is first data card in Block 3
  - [ ] All transported particle types listed

- [ ] **Particle consistency**:
  - [ ] Tally particle types (`:N`, `:P`) in MODE
  - [ ] Source particle type (PAR) in MODE
  - [ ] PHYS cards match MODE particles

- [ ] **Temperature consistency**:
  - [ ] TMP temperature matches MT temperature
  - [ ] TMP in MeV (not Kelvin!)
  - [ ] DBRC for high-T fuel (>600K)

- [ ] **Energy cutoffs appropriate**:
  - [ ] CUT:N E_min=0 for thermal problems
  - [ ] CUT:P E_min≥0.01 typical
  - [ ] Cutoffs don't exclude source energy

- [ ] **PHYS parameters**:
  - [ ] emax ≥ source max energy
  - [ ] iphot=1 for coupled n-γ (efficiency)
  - [ ] ides≥1 for MODE P E

---

## Advanced Topics

### 1. Photonuclear Reactions (High-Energy Photons)

**Purpose**: (γ,n), (γ,p) reactions for E>10 MeV

```
MODE  N P
PHYS:P  100  1  1  1            $ ispn=1 (photonuclear ON)
```

**When to Use**:
- High-energy bremsstrahlung (>10 MeV)
- Accelerator photon sources
- Activation studies

### 2. Multigroup Transport

**Purpose**: Use multigroup cross sections (legacy, rarely needed)

```
PHYS:N  100  J  J  J  J  0.01   $ emcnf=0.01 MeV (MG below 10 keV)
```

**When to Use**:
- Testing/verification
- Legacy input compatibility
- Typically use continuous-energy (emcnf=1e10)

### 3. Time-Dependent Problems (THTME Card)

**Purpose**: Output thermal motion data at specific times

```
THTME  0  1e2  1e3  1e4         $ Time points (shakes)
```

---

## Quick Reference: Default Values

| Card    | Parameter | Default   | Notes                     |
|---------|-----------|-----------|---------------------------|
| PHYS:N  | emax      | 100 MeV   | Max neutron energy        |
| PHYS:N  | iphot     | 0         | 0=analog, 1=implicit      |
| PHYS:N  | nodop     | 0         | 0=Doppler on              |
| PHYS:P  | emax      | 100 MeV   | Max photon energy         |
| PHYS:P  | ides      | 0         | 0=no e⁻, 1=simple, 2=full |
| PHYS:E  | emax      | 100 MeV   | Max electron energy       |
| CUT:N   | emin      | 0         | Min neutron energy        |
| CUT:P   | emin      | 0.001 MeV | Min photon energy (1 keV) |
| CUT:E   | emin      | 0.001 MeV | Min electron energy       |
| CUT:n   | tmax      | 1e33      | Max time (effectively ∞)  |
| TMP     | T         | 2.53e-8   | Room temp (293K)          |

---

## Best Practices

1. **MODE first**: Always first data card
2. **Use defaults**: Omit PHYS/CUT unless specific need
3. **Temperature matching**: TMP and MT must agree
4. **DBRC for fuel**: High-temperature (>600K) criticality
5. **Energy cutoffs**: Conservative (don't exclude physics)
6. **Coupled transport**: iphot=1 for n-γ (efficient)
7. **Comment choices**: Explain non-default physics settings

---

## References
- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md` (Sections 8, 16)
- **Related Skills**: mcnp-input-builder, mcnp-material-builder, mcnp-source-builder, mcnp-tally-builder
- **User Manual**: Chapter 5.7 (Physics Data Cards), Chapter 10.5 (Physics Model Examples)

---

**End of MCNP Physics Builder Skill**
