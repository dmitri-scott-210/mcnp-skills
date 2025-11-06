# MCNP Cross-Section Library Types

## Overview

MCNP supports multiple library types for different particle transport modes and energy regimes. Understanding when to use each type is essential for correct physics modeling and avoiding library errors.

## Library Type Summary

| Type | Extension | Particle | Energy Range | Use Case |
|------|-----------|----------|--------------|----------|
| Continuous Energy | .nnc | Neutron | Full range | General neutron transport |
| Thermal Scattering | .nnT | Neutron | Thermal (E<4 eV) | Bound atoms (H in H₂O, etc.) |
| Photoatomic | .nnp | Photon | Full range | Photon transport |
| Electron | .nne | Electron | Full range | Electron transport |
| Discrete Reaction | .nnd | Neutron | Specific | Legacy, rarely used |
| Dosimetry | .nnm | Response | N/A | Dose response functions |

## Continuous Energy Neutron Libraries (.nnc)

### Purpose
Full energy-dependent neutron cross sections from thermal to high energy (~20 MeV).

### Library Versions
```
.80c = ENDF/B-VIII.0 (2018) - Most recent, recommended
.70c = ENDF/B-VII.0 (2006) - Mature, widely validated
.66c = ENDF/B-VI.6 (1998) - Legacy
.60c = ENDF/B-VI.0 (1990) - Historical
```

### MCNP Usage
```
MODE N                  $ Neutron transport
M1  92235.80c  1.0     $ U-235 continuous energy
M2  1001.80c   2.0     $ H-1 continuous energy
    8016.80c   1.0     $ O-16 continuous energy
```

### Coverage
- All reaction types: (n,γ), (n,2n), (n,f), (n,α), etc.
- Angular distributions
- Energy distributions
- Fission neutron spectra
- Resonance data

### Best Practices
1. **Use Latest Version** - .80c preferred when available
2. **Consistency** - All isotopes same version when possible
3. **Validate** - Check xsdir before running
4. **Temperature** - Match to system conditions

## Thermal Scattering Libraries (.nnT)

### Purpose
S(α,β) thermal scattering data for bound atoms at thermal energies (E < ~4 eV).

### Why Required
Free-gas treatment inadequate for:
- Molecular binding (H in H₂O vs. free H)
- Crystal lattice effects (C in graphite)
- Chemical binding effects
- Low-energy neutron thermalization

### Common Materials

**Water:**
```
lwtr.80t - Light water (H₂O)
hwtr.80t - Heavy water (D₂O)

Temperature variants:
lwtr.80t = 293.6 K
lwtr.81t = 323.6 K
lwtr.82t = 373.6 K
lwtr.83t = 423.6 K
lwtr.84t = 473.6 K
lwtr.85t = 523.6 K
lwtr.86t = 573.6 K
lwtr.87t = 623.6 K
```

**Moderators:**
```
grph.80t - Graphite (carbon)
be.80t   - Beryllium metal
beo.80t  - Beryllium oxide
```

**Hydrides:**
```
zrh.80t  - Zirconium hydride (ZrH₁.₆-ZrH₂)
yzh.80t  - Yttrium hydride
```

**Organics:**
```
poly.80t - Polyethylene (CH₂)
benz.80t - Benzene (C₆H₆)
```

### MCNP Usage
```
MODE N
M1  1001.80c  2.0      $ H-1 in water
    8016.80c  1.0      $ O-16
MT1 lwtr.80t           $ S(α,β) for H in H₂O

M2  6000.80c  1.0      $ C in graphite
MT2 grph.80t           $ S(α,β) for C in graphite
```

### Critical Rules
1. **MT Number Matches M Number** - MT1 for M1, MT2 for M2, etc.
2. **Temperature Must Match** - Use correct .nnT for system temperature
3. **TMP Card Does NOT Affect S(α,β)** - Must use correct library
4. **Required for Accuracy** - Missing S(α,β) can cause 1-5% keff error

### When to Use
- **REQUIRED:** Thermal reactors, critical assemblies
- **IMPORTANT:** Mixed-spectrum systems, shielding with thermals
- **OPTIONAL:** Fast reactors (small thermal component)

## Photoatomic Libraries (.nnp)

### Purpose
Photon interaction cross sections (pair production, Compton, photoelectric).

### MCNP Usage
```
MODE N P               $ Coupled neutron-photon
M1  1001.80c  2.0     $ Neutron library
    8016.80c  1.0
c Photoatomic data used automatically based on Z
c No explicit .nnp in M cards required
```

### Implicit Use
MCNP automatically finds photoatomic data based on atomic number (Z) when MODE includes P.

### Checking Availability
```bash
# Check if photon data available for element
grep "^1000.80p " xsdir  # Hydrogen
grep "^8000.80p " xsdir  # Oxygen
grep "^82000.80p " xsdir # Lead
```

### Coverage
- Coherent (Rayleigh) scattering
- Incoherent (Compton) scattering
- Photoelectric absorption
- Pair production (E > 1.022 MeV)
- Form factors
- Scattering functions

## Electron Libraries (.nne)

### Purpose
Electron transport cross sections for coupled electron-photon calculations.

### MCNP Usage
```
MODE E P               $ Coupled electron-photon
M1  6000.80c  1.0     $ Carbon
c Electron data .80e used automatically if available
```

### Coverage
- Elastic scattering
- Inelastic scattering
- Bremsstrahlung production
- Stopping powers
- Range tables

### Common Use Cases
- Medical physics (dose calculations)
- Electron beam applications
- Coupled particle transport
- Radiation effects

## Discrete Reaction Libraries (.nnd)

### Purpose
Legacy format for specific reaction types.

### Status
- **Rarely used** in modern MCNP
- Superseded by continuous energy libraries
- May appear in older input files
- Generally avoid for new work

## Dosimetry Libraries (.nnm, .nnH)

### Purpose
Dose response functions and heating numbers.

### Common Libraries
```
ansi.01h - ANSI/ANS-6.1.1-1977 flux-to-dose
icrp.nnm - ICRP dose conversion factors
```

### MCNP Usage
```
MODE N
M1  1001.80c  2.0
F4:N  10                $ Flux tally
FM4  (1.0)              $ Multiplier
DE4  ansi.01h           $ Use ANSI dose function
DF4  1.0                $ Scaling
```

### Applications
- Radiation protection calculations
- Dose equivalent determination
- Regulatory compliance

## Library Selection Decision Tree

```
What particle transport needed?
│
├─ Neutrons only (MODE N)
│  ├─> Use .nnc libraries (e.g., .80c)
│  └─> Thermal moderator present?
│     ├─> Yes: Add .nnT (MT card)
│     └─> No: .nnc only
│
├─ Neutrons + Photons (MODE N P)
│  ├─> Use .nnc for neutrons
│  ├─> .nnp automatic for photons
│  └─> Check .nnp available for all elements
│
├─ Photons only (MODE P)
│  └─> Use .nnp libraries (implicit)
│
├─ Electrons + Photons (MODE E P)
│  ├─> Use .nne for electrons (implicit)
│  └─> .nnp automatic for photons
│
└─ Dose calculations
   └─> Add .nnH or .nnm to tally
```

## Version Compatibility

### Mixing Library Versions
**Generally Avoid** mixing ENDF/B versions:
```
Bad:
M1  92235.80c  1.0     $ ENDF/B-VIII.0
    92238.70c  1.0     $ ENDF/B-VII.0 (inconsistent!)

Good:
M1  92235.80c  1.0     $ All ENDF/B-VIII.0
    92238.80c  1.0     $ Consistent version
```

**Exception:** When specific isotope only available in different version:
```
Acceptable (document reason):
M1  92235.80c  1.0     $ U-235 (ENDF/B-VIII.0)
    95255.70c  1.0     $ Es-255 (only in ENDF/B-VII.0)
c Note: Mixing versions - Es-255 not in .80c library
```

## Library Coverage by ENDF/B Version

| Version | Isotopes | Thermal S(α,β) | Photoatomic | Status |
|---------|----------|----------------|-------------|--------|
| VIII.0 (.80x) | ~400 | 30+ materials | Full | Current, recommended |
| VII.0 (.70x) | ~380 | 25+ materials | Full | Mature, validated |
| VI.6 (.66x) | ~320 | 20+ materials | Partial | Legacy |
| VI.0 (.60x) | ~300 | 15+ materials | Partial | Historical |

## Special Cases

### Natural Element Mix
```
Use ZZZ000.nnc for natural isotopic composition:
M1  6000.80c  1.0      $ Natural carbon (98.93% C-12, 1.07% C-13)
M2  82000.80c  1.0     $ Natural lead (4 stable isotopes)
```

### Metastable States
```
Some libraries distinguish ground and metastable states:
43099.80c - Tc-99 ground state
43399.80c - Tc-99m metastable (not always available)

Most libraries: Use ground state ZAID for both
```

### Temperature Interpolation
```
When exact temperature library unavailable:
M1  92235.80c  1.0     $ 293.6 K library
TMP  600               $ MCNP interpolates to 600 K

Better: Use closest native library
M1  92235.81c  1.0     $ 600 K library (exact)
```

## Verification Checklist

Before running MCNP:

- [ ] All continuous energy (.nnc) ZAIDs in xsdir
- [ ] Thermal scattering (.nnT) available for moderators
- [ ] Photoatomic (.nnp) available if MODE includes P
- [ ] Library versions consistent
- [ ] Temperature libraries appropriate
- [ ] DATAPATH set correctly
- [ ] Test case runs successfully

## Common Errors

**"cross-section table not found"**
- Check ZAID in xsdir
- Verify library type correct (.80c vs .70c)
- Confirm DATAPATH set

**"thermal scattering library not found"**
- Check MT card references correct .nnT
- Verify thermal library in xsdir
- Ensure MT number matches M number

**"photoatomic data not available"**
- For MODE P, check .nnp libraries
- Verify element's atomic number in photoatomic section
- May need different ENDF/B version

---

**See also:**
- `xsdir_format.md` - xsdir file structure
- `temperature_libraries.md` - Temperature-dependent libraries
- `troubleshooting_libraries.md` - Error diagnosis
