# Advanced Physics Cards Reference

## Overview

This reference covers advanced physics control cards: FMULT (fission multiplicity), TROPT (transport options), UNC (uncollided secondaries), and DRXS (discrete reaction cross sections). These cards provide specialized control beyond standard PHYS card settings.

---

## FMULT: Fission Multiplicity Constants and Physics Models

### Purpose

The FMULT card controls fission neutron multiplicity distributions and fission physics models for both spontaneous and neutron-induced fission.

**Why FMULT is Needed:**
- Nuclear data libraries contain average fission multiplicity ν̄ but not full probability distribution P(ν)
- Spontaneous fission decay data not in neutron-induced fission libraries
- Enables individual neutron emission sampling from spontaneous fission sources
- Allows advanced fission models (LLNL, FREYA, CGMF) with correlated neutron/photon production

### Syntax

```
FMULT target_identifier KEYWORD=value(s)
```

### Target Identifier

Format per §1.2.2 (all formats supported):
- ZAID format: 92235 or 92235.80c
- Element-Mass: U-235
- Metastable: Am-242m (note: currently converted to non-metastable internally)

### Keywords

#### sfnu - Spontaneous Fission Multiplicity

**Single Value (Gaussian sampling):**
```
FMULT Cf-252 sfnu=3.757
```
- `sfnu=x`: Average multiplicity ν̄ for Gaussian sampling with width specified by `width` keyword

**Multiple Values (Discrete distribution):**
```
FMULT Cf-252 sfnu=0.002 0.028 0.155 0.428 0.732 0.917 0.983 0.998 1.0
```
- Values form cumulative probability distribution P(ν=n) for n=0 to N
- Maximum: 10 values (0-9 neutrons per fission)
- When specified as distribution, `width` keyword ignored for spontaneous fission

#### width - Gaussian Width (FWHM)

```
FMULT U-235 width=1.16
```
- Full-width at half maximum (FWHM) for Gaussian sampling of P(ν)
- Applies to both spontaneous and neutron-induced fission
- Ignored for spontaneous fission when sfnu specified as cumulative distribution
- Required for neutron-induced fission even if sfnu is a distribution

#### sfyield - Spontaneous Fission Yield

```
FMULT Cf-252 sfyield=2.34e12
```
- Units: neutrons per second per gram (n/s-g)
- Required when multiple spontaneous fission nuclides present in material
- Used to select which nuclide undergoes spontaneous fission

#### watt - Watt Spectrum Parameters

```
FMULT Pu-239 watt=0.885247 3.8026
```
- Two parameters: a and b for Watt energy spectrum (Eq. 5.27 in manual)
- Controls spontaneous fission neutron energy sampling
- Watt spectrum form: P(E) ~ exp(-E/a) × sinh(√(b×E))

#### method - Sampling Algorithm or Fission Model

```
FMULT method=m
```

| Value | Description | Notes |
|-------|-------------|-------|
| 0 | MCNP5 sine/cosine sampling (DEFAULT) | Table 5.11 in manual |
| 1 | Lestone moment-fitting method | MCNPX polar sampling + 0.5 |
| 3 | Ensslin/Santi/Beddingfield/Mayo method | MCNPX polar + random [0,1] |
| 5 | LLNL fission library | Correlated prompt neutrons/photons |
| 6 | FREYA fission model | Event-by-event correlated fission |
| 7 | CGMF fission model | Event-by-event correlated fission |

**Important Restrictions:**
- method=5, 6, 7 **CANNOT** be used with delayed neutron biasing (dnbias on ACT card)
- method=5, 6, 7 are the ONLY way to produce correlated prompt fission photons with multiplicities

**Coverage:**
- method=5: LLNL library covers most common fissioning nuclides
- method=6: FREYA covers subset; falls back to LLNL if nuclide unavailable
- method=7: CGMF covers subset; falls back to LLNL if nuclide unavailable

#### data - Isotope Multiplicity Data

```
FMULT data=d
```

| Value | Description |
|-------|-------------|
| 0 | Bounded integer fission sampling (DEFAULT) |
| 1 | Lestone re-evaluated Gaussian width by isotope |
| 2 | Original Terrell Gaussian widths by isotope |
| 3 | Ensslin/Santi/Beddingfield/Mayo data |

#### shift - Multiplicity Preservation Method

```
FMULT shift=s
```

| Value | Description |
|-------|-------------|
| 0 | MCNP5 treatment (integer neutrons per fission, e.g., ν̄=2.7 → 2 neutrons 30%, 3 neutrons 70%) (DEFAULT) |
| 1 | MCNPX-style adjustment with re-evaluated Gaussian width |
| 2 | Sample Gaussian and preserve average by increasing ν threshold |
| 3 | Sample Gaussian without correction (will overpredict ν̄) |
| 4 | MCNP4C integer sampling with spontaneous fission present |

**Default Assignment Rules:**
- If no method/data/shift specified: method=0, data=0, shift=0
- If ANY keyword specified: method=3, data=3, shift=1 (unless explicitly set)

### Multiplicity Parameters Default Values

MCNP6 provides built-in defaults for common fissioning nuclides (PRINT Table 38). Defaults include:
- Average multiplicity ν̄
- Gaussian width
- Watt spectrum parameters (a, b)
- Spontaneous fission yield

**Nuclides with defaults:** Th-232, U-233, U-235, U-238, Pu-238, Pu-239, Pu-240, Pu-241, Pu-242, Cm-244, Cf-252, and others (see Table 38 in output).

**Nuclides WITHOUT defaults (require FMULT card):**
- Pu-246, Cm-246, Cm-248, Cf-246, Cf-250, Cf-254, Fm-257, No-252

### Examples

#### Example 1: Method/Data/Shift Only
```
FMULT method=0 data=1 shift=0
```
Uses MCNP5 sampling with Lestone data and integer treatment. Relies on default values in PRINT Table 38.

#### Example 2: Spontaneous Fission Source
```
SDEF PAR=SF
FMULT Pu-239 width=1.16 watt=0.885247 3.8026 sfyield=0.0218 sfnu=2.1
FMULT Cf-252 width=1.207 watt=1.18 1.03419 sfyield=2.34e12 &
      sfnu=0.002 0.028 0.155 0.428 0.732 0.917 0.983 0.998 1.0
```
- Two spontaneous fission sources (Pu-239 and Cf-252)
- Pu-239: Gaussian sampling with ν̄=2.1
- Cf-252: Discrete distribution P(ν=0) to P(ν=8)
- sfyield required to select between nuclides

#### Example 3: FREYA Event-by-Event Fission
```
FMULT method=6
```
Enables FREYA model for correlated neutron/photon emission from neutron-induced and spontaneous fission. Provides event-by-event fission with physically correlated multiplicities and energies.

#### Example 4: Cross-Section Substitution for Missing Data
```
M123 Fm-257 1
AWTAB Fm-257 254.88653438
MX123:N Cf-252
c
SDEF PAR=SF
FMULT Fm-257 watt=1.4 2.0 sfyield=5E11
```
- Fm-257 cross sections not generally available
- Use AWTAB for atomic weight ratio
- Use MX card to substitute Cf-252 cross sections
- FMULT provides spontaneous fission parameters

### Integration with PHYS:N

**Deprecated:** PHYS:N 6th parameter (fism) is deprecated in MCNP6.
**Use FMULT card instead** for all fission multiplicity control.

Mapping from MCNP5/MCNPX to MCNP6 (Table 5.11):

| MCNPX PHYS:N fism | MCNP6 FMULT method | data | shift |
|-------------------|--------------------|------|-------|
| 0                 | 0                  | 0    | 0     |
| -1, 1             | 3                  | 3    | 1     |
| 2                 | 3                  | 3    | 2     |
| 3                 | 3                  | 3    | 3     |
| 4                 | 3                  | 3    | 4     |
| 5                 | 5                  | N/A  | N/A   |

| MCNP5 PHYS:N fisnu | MCNP6 FMULT method | data | shift |
|--------------------|--------------------|------|-------|
| 0                  | 0                  | 0    | 0     |
| 1                  | 0                  | 1    | 0     |
| 2                  | 0                  | 2    | 0     |

---

## TROPT: Transport Options

### Purpose

The TROPT card modifies default particle interaction modeling options. Primarily used for:
- Diagnosing importance of physical processes
- Generating double-differential cross sections with physics models
- Turning off specific physics processes for sensitivity studies

**Important:** TROPT does NOT affect electron/positron PHYS card parameters.

### Syntax

```
TROPT KEYWORD=value(s)
```

### Keywords

#### mcscat - Multiple Coulomb Scattering

```
TROPT mcscat=option
```

| Option | Description |
|--------|-------------|
| off | Disable multiple Coulomb scattering (no angular deflection) |
| fnal1 | FNAL algorithm 1 (DEFAULT) |
| gaussian | Gaussian scattering model |
| fnal2 | FNAL algorithm 2 (treats eloss=strag1 as eloss=csda, recommended) |

**Use:** Turn OFF to isolate nuclear reaction effects. Gaussian/fnal2 for alternative scattering models.

#### eloss - Slowing Down Energy Losses

```
TROPT eloss=option
```

| Option | Description |
|--------|-------------|
| off | No energy loss during slowing down |
| strag1 | CSDA with straggling (DEFAULT) |
| csda | Energy loss using only CSDA (continuous slowing-down approximation) |

**Use:** Turn OFF to isolate scattering effects. CSDA for faster transport without straggling.

#### nreact - Nuclear Reactions

```
TROPT nreact=option
```

| Option | Description |
|--------|-------------|
| off | No nuclear reactions occur |
| on | Nuclear reactions allowed (DEFAULT) |
| atten | Attenuation mode: absorption weighting at collision |
| remove | Incident particle killed at collision |

**Use:**
- off: Isolate multiple scattering and energy loss
- atten: For genxs cross-section generation (see below)
- remove: Kill particles at first collision (flux calculations)

#### nescat - Nuclear Elastic Scattering

```
TROPT nescat=option
```

| Option | Description (when nreact ≠ off) |
|--------|----------------------------------|
| off | Delta-scatter for elastic in transport; zero elastic cross section in genxs |
| on | Normal elastic scattering (DEFAULT) |

**Important:** This keyword has NO effect if nreact=off.

**Use in genxs mode:**
- nescat=off: Calculate inelastic secondary particle production only
- nescat=on: Include elastic scattering

**Use in transport mode:**
- nescat=off: Elastic treated as delta-scatter (no direction change, useful for testing)

#### genxs - Cross-Section Generation Mode

```
TROPT genxs
TROPT genxs=filename
```

**Enables generation of:**
- Double-differential particle production cross sections
- Residual nucleus production cross sections
- From high-energy nuclear interaction models

**Behavior:**
- If `genxs` keyword absent: Standard transport
- If `genxs` present (no filename): Read edit input from file `inxc`
- If `genxs=filename`: Read edit input from file `filename`

**Requirements:**
- Requires auxiliary input file (inxc or specified filename)
- Auxiliary file format described in Appendix D.9
- Must use physics models (MPHYS on or particle energies above table limits)

**Typical Use:**
```
TROPT genxs nreact=atten nescat=off
```
- Generate inelastic cross sections only
- Attenuation weighting for statistics

### genxs Application

**Purpose:** Generate model-based cross sections without full transport.

**Source particles:**
- Specified inside a medium
- Each history = single interaction at source energy
- Tally: energies and direction cosines of secondaries and recoil nuclei

**Typical material:** Single isotope (but can be multi-isotopic element or complex composition).

**Density:** Genxs calculation independent of material density.

**Output:**
- Energy- and angle-integrated results as yield (multiplicity) and cross section
- Single- and double-differential cross sections
- Residual nucleus production

#### genxs Example 1: Elastic Scattering

**MCNP Input (example_genxs_1.mcnp.inp.txt):**
```
Test problem: RECOIL2
1  1  -16.654  -1 2 -3
2  0  -4  (1:-2:3)
3  0  4

1  cz 4.0
2  pz -1.0
3  pz 1.0
4  so 50.0

M1 74180 0.001300 74182 0.263000 74183 0.143000
   74184 0.306700 74186 0.286000
SDEF erg=23080 par=H dir=1 pos=0 0 0 vec 0 0 1
IMP:H 1 1 0
PHYS:H 23080
MODE H
PRINT 40 110 95
NPS 10000000
PRDMP 2J -1
TROPT genxs nreact=atten
```

**Auxiliary Input (inxc):**
```
Test problem: RECOIL2
5,1,1/
Elastic scattering edit
0,-200,1/
2.0/                    ! 200 bin boundaries, 2 deg to 0 deg
-1/                     ! elastic scattered projectile
Elastic scattering energy edit
125,0,1/
23079,23079.01/         ! 125 10-keV bins above 23.079 GeV
-1/                     ! elastic scattered projectile
Elastic recoil angle edit
0,102,1/
0.0,0.02/               ! 101 boundaries mu=0 to 0.02 & 1.0
-2/                     ! elastic recoil nucleus
Elastic recoil energy edit
125,0,1/
0.01/                   ! 125 10-keV bins below 1.25 MeV
-2/                     ! elastic recoil nucleus
Elastic recoil momentum edit
150,0,1,,1/
5/                      ! 150 5-MeV/c bins below 750 MeV/c
-2/                     ! elastic recoil nucleus
```

**Calculates:**
1. dσ/dΩ for projectile (binned by degrees)
2. dσ/dE for projectile (binned by energy)
3. dσ/dΩ for recoil nuclei (binned by cosine)
4. dσ/dE for recoil nuclei (binned by energy)
5. dσ/dp for recoil nucleus (binned by momentum)

**Result:** 23.08-GeV protons on natural tungsten, elastic scattering only (nreact=atten ensures all histories elastic).

#### genxs Example 2: Inelastic Production

**MCNP Input (example_genxs_2.mcnp.inp.txt):**
```
MCNP6 test: p + U238 by CEM03.03
1  1  1.0  -1 2 -3
2  0  -4  (1:-2:3)
3  0  4

1  cz 4.0
2  pz -1.0
3  pz 1.0
4  so 50.0

SDEF erg=1000 par=H dir=1 pos=0 0 0 vec 0 0 1
IMP:H 1 1 0
PHYS:H 1000
M1 92238 1.0
MODE H
LCA 8J 1                 $ use CEM03.03
TROPT genxs=inxc01 nreact=on nescat=off
PRINT 40 110 95
NPS 1000000
PRDMP 2J -1
```

**Auxiliary Input (inxc01):**
```
MCNP6 test: p + U238 at 1 GeV for TR applications
1 1 1/
Cross Section Edit
56 0 9/
5. 10. 15. 20. 25. 30. 35. 40. 45. 50. 55. 60. 65. 70. 75. 80.
85. 90. 95. 100. 120./
1 5 6 7 8 21 22 23 24/
```

**Calculates:**
- Angle-integrated energy spectra for 9 particle types (n, p, π⁺, π⁻, π⁰, d, t, ³He, ⁴He)
- 56 energy bins
- Inelastic production only (nescat=off)
- Residual nucleus production

**Result:** Identifies production of delayed neutron emitters (⁸⁷Br, ⁸⁸Br, ⁹Li, ¹⁷N, ¹⁶C) from 1-GeV protons on ²³⁸U.

### Summary: TROPT Use Cases

1. **Sensitivity Studies:** Turn off processes (nreact=off, nescat=off, mcscat=off, eloss=off) to isolate effects
2. **Cross-Section Generation:** genxs mode with inxc file for model-based tabulations
3. **Benchmarking:** Compare models with/without specific processes
4. **Debugging:** Simplify physics to identify issues

---

## UNC: Uncollided Secondaries

### Purpose

Control whether secondary particles are born as collided or uncollided. Useful for separating direct source contribution from secondary particle contribution in tallies.

### Background

**Historical MCNP definition of "uncollided":**
- Any particle that has not undergone a collision since creation
- Includes both:
  - Source particles (truly uncollided from source)
  - Secondary particles created at collision (technically "collided" from source perspective)

**Problem:** This makes separating direct source contribution from secondary contribution difficult, especially for track-length tallies in radiography.

**Solution:** UNC card allows secondaries to inherit parent's collision count (born as "collided").

### Syntax

#### Cell-card Form
```
UNC:P u
```

#### Data-card Form
```
UNC:P u1 u2 ... uJ
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| P | Particle designator (N, P, H, etc.) |
| u (cell-card) | 0=secondaries collided, 1=secondaries uncollided (DEFAULT) |
| uj (data-card) | Same as u, for cell j (J = total number of cells in problem) |

**Default:** uj=1 (secondaries considered uncollided for cell j)

### How It Works

**UNC:P 1 (DEFAULT):**
- Secondary particles created with ncol=0 (uncollided)
- First collision after creation increments ncol to 1

**UNC:P 0:**
- Secondary particles inherit parent's collision count
- If parent has ncol=1, secondary born with ncol=1
- Secondary always considered "collided" (ncol ≥ 1)

### Use Cases

#### Radiography with Track-Length Tallies

**Problem:**
```
c Photon source
SDEF PAR=P
c Track-length tally for uncollided flux
F4:P 1
FU4 0 1        $ Uncollided contribution only
```

Without UNC card: Tally includes Compton-scattered photons, bremsstrahlung photons, etc. (all born "uncollided").

**Solution:**
```
UNC:P 0        $ Secondaries born collided
```
Now FU4 0 1 captures ONLY direct source photons (no secondaries).

#### Separating Source vs Buildup

**Scenario:** Want to tally contribution from direct source vs buildup from scattered/secondary particles.

**Setup:**
```
F4:N 1
FU4 0 1   $ Direct source neutrons
FU14 1    $ First-collision neutrons
FU24 2 10 $ Multiply-scattered neutrons
UNC:N 0   $ Secondaries inherit collision count
```

With UNC:N 0:
- Source neutrons: ncol=0
- (n,2n) neutrons inherit parent ncol, so if parent collided once, secondary has ncol=1
- Cleanly separates primary from secondary

### Example

```
c Cell-card form for cell 3
3  1  -2.7  -10  IMP:N=1  UNC:N=0

c Data-card form for all cells
UNC:N 1 1 0 1 1
```

Cell 3 has UNC:N=0, all others UNC:N=1 (default).

### Integration

**Related Cards:**
- SDEF - Defines source (source particles always uncollided initially)
- FU (tally flagging) - Can flag on collision number to separate contributions
- MODE - UNC card needed for each particle type on MODE card

**Related Skills:**
- mcnp-tally-builder - Use FU card with UNC to separate components
- mcnp-source-builder - Understand source particle initial conditions

---

## DRXS: Discrete Reaction Cross Sections

### Purpose

(Note: DRXS card details not provided in Chapter 5.07 excerpt. This section is a placeholder.)

The DRXS card is used to control discrete reaction cross sections and sampling. Typically used for specialized reaction channel analysis.

**For comprehensive DRXS documentation, see:**
- MCNP6 User Manual, Chapter 5.3 (cross-section specification cards)
- Related to MT cards (reaction identifiers)

---

## Summary: Advanced Physics Cards

### FMULT - Fission Multiplicity
- **When to use:** Spontaneous fission sources, detailed fission multiplicity, correlated fission neutrons/photons
- **Key features:** Gaussian or discrete distributions, advanced models (LLNL, FREYA, CGMF)
- **Replaces:** PHYS:N fism parameter (deprecated)

### TROPT - Transport Options
- **When to use:** Sensitivity studies, cross-section generation (genxs), debugging, process isolation
- **Key features:** Turn on/off specific physics processes, generate model-based cross sections
- **Caution:** Does NOT affect electron/positron PHYS parameters

### UNC - Uncollided Secondaries
- **When to use:** Radiography, separating source from buildup, detailed collision-number analysis
- **Key features:** Control whether secondaries inherit parent collision count
- **Default:** Secondaries born uncollided (historical MCNP behavior)

### DRXS - Discrete Reactions
- **When to use:** Specialized reaction channel analysis
- **Documentation:** See MCNP6 Manual Chapter 5.3

---

## Integration with Other Skills

**Use Before Advanced Physics Cards:**
- mcnp-input-builder - Understand data cards block
- mcnp-physics-builder - Set up basic PHYS cards first
- mcnp-source-builder - Define sources (especially PAR=SF for FMULT)

**Use After Advanced Physics Cards:**
- mcnp-output-parser - Parse fission multiplicity tables (PRINT Tables 115, 117), genxs output
- mcnp-tally-builder - Use UNC with FU flagging, interpret genxs tallies
- mcnp-best-practices-checker - Validate advanced physics setup

**Related Skills:**
- mcnp-fatal-error-debugger - Debug FMULT/TROPT/UNC errors
- mcnp-physics-validator - Validate model physics with TROPT settings
