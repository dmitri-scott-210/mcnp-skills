# PHYS Card Detailed Parameters Reference

## Overview

This reference provides comprehensive details on all PHYS card parameters for all particle types. The PHYS card controls physics treatment and transport cutoffs for specific particle types.

---

## General PHYS Card Format

```
PHYS:P emax ean tabl ides ielas ipreq iexisa ichoic jcoul nexite npidk noact others...
```

Where `P` is the particle designator (N, P, H, E, etc.)

---

## PHYS:N - Neutron Physics

### Syntax
```
PHYS:N emax ean tabl cupn cutn fism recl dnbias jghd j jghp tmptgt other...
```

### Complete Parameter List

| Position | Parameter | Default | Description |
|----------|-----------|---------|-------------|
| 1 | emax | 100 MeV | Maximum energy for neutron transport (MeV) |
| 2 | ean | 0 | Analog simulation, survival biasing, or implicit capture |
| 3 | tabl | J | Use cross-section tables |
| 4 | cupn | 0 | Production cutoff energy (MeV) |
| 5 | cutn | 0 | Transport cutoff energy (MeV) |
| 6 | fism | (see FMULT) | Fission multiplicity options (deprecated, use FMULT card) |
| 7 | recl | J | Detailed residual and correlated neutron treatment |
| 8 | dnbias | 0 | Delayed neutron biasing |
| 9 | jghd | J | Group-dependent heating deposition |
| 10 | j | J | Placeholder |
| 11 | jghp | J | Photonuclear contribution to heating |
| 12 | tmptgt | J | Temperature of target nucleus |
| 13+ | other | J | Reserved for future use |

### Key Parameters Explained

#### emax - Maximum Energy
- Particles above emax are killed
- Default: 100 MeV (sufficient for most reactor problems)
- Typical high-energy: 20,000 MeV or higher
- Set to highest source or (n,xn) neutron energy expected

#### ean - Capture Treatment
- `ean > 0`: Analog capture below ean, implicit capture above
- `ean < 0`: Survival biasing analog above |ean|, implicit below
- `ean = 0`: Implicit capture everywhere (DEFAULT, efficient for deep penetration)

#### tabl - Cross-Section Tables
- `J`: Use cross-section tables (DEFAULT)
- Other values: Reserved/deprecated

#### cutn - Transport Cutoff
- Neutrons below cutn are killed
- Default: 0 (transport to thermal energies)
- Set > 0 to save time when low-energy neutrons unimportant

#### recl - Residual Nucleus Treatment
- `J`: Detailed treatment ON (DEFAULT)
- Other: OFF

#### dnbias - Delayed Neutron Biasing
- `0`: No delayed neutron biasing (DEFAULT)
- `> 0`: Weight window generator active for delayed neutrons

---

## PHYS:P - Photon Physics

### Syntax
```
PHYS:P emax ean tabl ides nocoh ispn nodop fism (others)
```

### Complete Parameter List

| Position | Parameter | Default | Description |
|----------|-----------|---------|-------------|
| 1 | emax | 100 MeV | Maximum photon energy (MeV) |
| 2 | ean | 0 | Analog vs implicit capture |
| 3 | tabl | J | Use cross-section tables |
| 4 | ides | 0 | Detailed photon physics |
| 5 | nocoh | 1 | Coherent (Rayleigh) scattering |
| 6 | ispn | -1 | Photonuclear particle production |
| 7 | nodop | 1 | Doppler energy broadening for photoatomic |
| 8 | fism | (see FMULT) | Fission multiplicity for photonuclear (deprecated) |

### Key Parameters Explained

#### emax - Maximum Energy
- Photons above emax are killed
- Default: 100 MeV
- For photonuclear problems: set to 150-200 MeV

#### ides - Detailed Physics
- `0`: Simple physics (DEFAULT, faster)
- `1`: Detailed physics (electron energy deposition, bremsstrahlung)

#### nocoh - Coherent Scattering
- `0`: Coherent (Rayleigh) scattering ON
- `1`: Coherent scattering OFF (DEFAULT, minimal effect at most energies)

#### ispn - Photonuclear Production
- `-1`: Produce only neutrons from photonuclear reactions (DEFAULT)
- `0`: Produce all particles from photonuclear
- `1`: Photonuclear OFF

#### nodop - Doppler Broadening
- `0`: Doppler energy broadening OFF
- `1`: Doppler broadening ON (DEFAULT)

---

## PHYS:H - Proton Physics

### Syntax
```
PHYS:H emax ean tabl ides ielas ipreq jcoul nexite npidk noact sehfpp
```

### Complete Parameter List

| Position | Parameter | Default | Description |
|----------|-----------|---------|-------------|
| 1 | emax | 100 MeV | Maximum proton energy (MeV) |
| 2 | ean | 0 | Analog vs implicit capture |
| 3 | tabl | 1 | Use cross-section tables when available |
| 4 | ides | 0 | Detailed physics (not currently used) |
| 5 | ielas | 2 | Elastic scattering (0=off, 1=n only, 2=n+p) |
| 6 | ipreq | 1 | Pre-equilibrium model (0=off, 1=on) |
| 7 | jcoul | 1 | Coulomb barrier (0=off, 1=on) |
| 8 | nexite | 1 | Nuclear recoil energy subtraction |
| 9 | npidk | 0 | Pion termination treatment |
| 10 | noact | 1 | Transport options (see LCA card noact) |
| 11 | sehfpp | J | Stepping algorithm for protons |

### Key Parameters Explained

#### emax - Maximum Energy
- Protons above emax are killed
- Default: 100 MeV
- For proton therapy: typically 250 MeV
- For accelerator applications: 1000-20000 MeV

#### tabl - Table vs Model Physics
- `1`: Use tables when available (DEFAULT)
- `0`: Force model physics

**Important:** For proton energies above cross-section table limits, model physics automatically invoked regardless of tabl setting.

#### ielas - Elastic Scattering
- `0`: No elastic scattering
- `1`: Elastic for neutrons only (not applicable to protons)
- `2`: Elastic for neutrons and protons (DEFAULT)

#### sehfpp - Stepping Algorithm
- `J`: Default algorithm
- Other values: Reserved for future development

---

## PHYS:E - Electron Physics

### Syntax
```
PHYS:E emax ean tabl ides ibad istrg bnum xnum rnok enum numb (others)
```

### Complete Parameter List

| Position | Parameter | Default | Description |
|----------|-----------|---------|-------------|
| 1 | emax | 100 MeV | Maximum electron energy (MeV) |
| 2 | ean | 0 | Analog vs implicit capture |
| 3 | tabl | J | Use cross-section tables |
| 4 | ides | 0 | Detailed physics treatment |
| 5 | ibad | J | Electron energy indexing algorithm |
| 6 | istrg | 0 | Energy-loss straggling |
| 7 | bnum | 0 | Number of bremsstrahlung photons |
| 8 | xnum | 1 | Number of characteristic X-rays |
| 9 | rnok | 0 | K-shell electron knockout |
| 10 | enum | 1 | Number of knock-on electrons |
| 11 | numb | 0 | Number of bremsstrahlung photons at non-linearity |

### Key Parameters Explained

#### emax - Maximum Energy
- Electrons above emax are killed
- Default: 100 MeV
- For electron accelerators: 10-50 MeV typical

#### istrg - Energy-Loss Straggling
- `0`: No straggling (CSDA, DEFAULT)
- `1`: Landau straggling
- `2`: Vavilov straggling (more accurate, slower)

#### bnum - Bremsstrahlung Production
- `0`: Simple thick-target bremsstrahlung model (DEFAULT)
- `1`: Detailed bremsstrahlung production

#### rnok - K-Shell Knockout
- `0`: No K-shell knockout (DEFAULT)
- `1`: K-shell knockout enabled

---

## PHYS:/ - Positron Physics

### Syntax
```
PHYS:/ emax ean tabl ides ibad istrg bnum xnum rnok enum annihil
```

### Parameters

Essentially same as PHYS:E, with additional parameter:

#### annihil - Annihilation Treatment
- Position 11
- Controls positron annihilation photon production

---

## PHYS:| - Muon Physics

### Syntax
```
PHYS:| emax ean tabl cutp cut|
```

### Parameters

| Position | Parameter | Default | Description |
|----------|-----------|---------|-------------|
| 1 | emax | 100 MeV | Maximum muon energy |
| 2 | ean | 0 | Analog vs implicit |
| 3 | tabl | J | Use tables |
| 4 | cutp | 0 | Production cutoff |
| 5 | cut\| | 0 | Transport cutoff |

**Note:** Muon physics simplified compared to electrons due to higher mass.

---

## PHYS Card for Other Particles

### Heavy Ions, Pions, etc.

For particles like deuteron (D), triton (T), helium-3 (S), alpha (A), pions (Z, ?, !), etc.:

```
PHYS:X emax ean tabl cupx cutx (model physics parameters)
```

Basic parameters (emax, ean, tabl, cupx, cutx) similar to neutrons.
Additional parameters depend on model physics requirements (see model_physics_comprehensive.md).

---

## Common PHYS Parameter Patterns

### High-Energy Neutron Transport
```
PHYS:N 20000 0 J 0 0
```
- emax=20 GeV (covers spallation)
- Implicit capture everywhere
- Tables used when available
- No production or transport cutoffs

### Coupled Neutron-Photon with Detailed Photon Physics
```
PHYS:N 100 0 J 0 0
PHYS:P 100 0 J 1 0
```
- 100 MeV max for both
- Implicit capture
- Detailed photon physics (ides=1)

### Proton Therapy
```
PHYS:H 250 0 1
```
- 250 MeV max (covers therapy energies)
- Implicit capture
- Tables used

### Electron Beam with Bremsstrahlung
```
PHYS:E 20 0 J 1 J 1 1 1 1 1
PHYS:P 20 0 J 1
```
- 20 MeV electrons
- Detailed electron physics
- Straggling ON
- Bremsstrahlung production detailed
- Coupled to photons

---

## Parameter Interdependencies

### PHYS:N and FMULT
The 6th parameter (fism) on PHYS:N card is deprecated. Use FMULT card instead for fission multiplicity control.

### PHYS:P ispn and FMULT
When photonuclear fission enabled (ispn≠1), use FMULT for multiplicity control.

### PHYS:H and Model Physics (LCA, LCB, etc.)
When proton energy exceeds table limits, model physics invoked. See model_physics_comprehensive.md for LCA/LCB/LCC/LEA/LEB parameters.

### PHYS:E/PHYS:/ and CUT Card
Electron and positron transport cutoffs often specified on CUT card instead of PHYS card for better control.

---

## Performance Considerations

### Neutron Transport
- **emax too high:** Wastes memory for unlikely high-energy neutrons
- **cutn too high:** May miss important low-energy contributions
- **ean=0 (implicit capture):** Most efficient for deep penetration

### Photon Transport
- **ides=0:** Faster, adequate for most shielding/criticality
- **ides=1:** Required for accurate electron energy deposition
- **nocoh:** Minimal impact at >100 keV, can disable for speed

### Electron Transport
- **istrg=0:** Fastest, adequate for many problems
- **istrg=2:** Most accurate, needed for precise dose
- **bnum=1:** Detailed bremsstrahlung adds significant time

---

## Validation Checklist

**For Each PHYS Card:**
- [ ] emax covers maximum expected particle energy (source + (n,xn) + reactions)
- [ ] ean appropriate for problem type (0 for deep penetration, survival biasing for variance reduction)
- [ ] Cutoff energies (cutn, cutp, etc.) appropriate for tallies (must be below tally energy range)
- [ ] Detailed physics (ides, istrg, bnum, etc.) justified for problem (adds computational cost)
- [ ] Model physics parameters consistent if emax exceeds table limits
- [ ] Particle types on PHYS cards match MODE card

---

## Common Errors

### Error 1: emax Below Source Energy
```
SDEF ERG=200
PHYS:N 100
```
**Problem:** Source neutrons at 200 MeV killed immediately by emax=100.
**Fix:** PHYS:N 250 (or higher)

### Error 2: cutn Above Tally Energy
```
F4:N 1
E4 0 0.001 0.01 0.1 1 10
PHYS:N 100 0 J 0 1.0
```
**Problem:** cutn=1.0 MeV kills neutrons before thermal tally bins.
**Fix:** PHYS:N 100 0 J 0 0

### Error 3: Missing PHYS Card for MODE Particle
```
MODE N P
PHYS:N 100
c Missing PHYS:P
```
**Problem:** Photons use default emax=100 MeV, may be insufficient.
**Fix:** Add PHYS:P 100 (or appropriate emax)

### Error 4: Inconsistent Model Physics
```
PHYS:H 5000 0 0
c Forces models ON by tabl=0, but no LCA/LCB cards
```
**Problem:** Model physics required but not configured.
**Fix:** Add LCA/LCB cards or set tabl=1

---

## Integration with Other Skills

**Use Before PHYS Cards:**
- mcnp-input-builder - Understand data cards block
- mcnp-source-builder - Know source energy range (sets emax minimum)

**Use After PHYS Cards:**
- mcnp-tally-builder - Ensure tally energy ranges below cutoffs
- mcnp-physics-validator - Validate PHYS settings
- mcnp-best-practices-checker - Check for common PHYS errors

**Related Cards:**
- MODE - Defines which PHYS cards needed
- CUT - Alternative cutoff specifications
- TMP - Temperature-dependent cross sections
- DBRC - Doppler broadening rejection correction
- FMULT - Fission multiplicity (replaces PHYS:N fism)
- LCA/LCB - Model physics control (when emax exceeds tables)

---

## Summary

PHYS cards control the physics treatment for each particle type in MCNP transport. Key points:

1. **One PHYS card per MODE particle type** (PHYS:N, PHYS:P, PHYS:H, etc.)
2. **emax must cover maximum expected energy** (source + secondary production)
3. **Cutoff energies affect both transport and tallies** (must be below tally bins)
4. **Detailed physics add computational cost** (justify need: ides, istrg, bnum, etc.)
5. **Model physics invoked automatically** when energy exceeds table limits
6. **Performance tuning critical** for large problems (implicit capture, cutoffs, simplified physics)

Proper PHYS card configuration balances physics accuracy with computational efficiency.
