# MCNP Physics Settings Guide

**Version:** 2.0.0
**Skill:** mcnp-physics-validator

---

## MODE Card

**Purpose:** Specify particle types to transport
**Position:** MUST be first data card
**Format:** `MODE <particle-list>`

**Common Modes:**
- `MODE N` - Neutrons only
- `MODE P` - Photons only
- `MODE N P` - Coupled neutron-photon
- `MODE N P E` - Neutron-photon-electron

---

## PHYS Cards

**Purpose:** Control physics models and parameters
**Format:** `PHYS:<particle> <emax> <emcnf> <ides> ...`

**Common Settings:**
- `PHYS:N 100` - Neutron physics, 100 MeV max
- `PHYS:P 100` - Photon physics, 100 MeV max
- `PHYS:E 100` - Electron physics, 100 MeV max

---

## CUT Cards

**Purpose:** Set energy cutoffs
**Format:** `CUT:<particle> <energy>`

**Recommendations:**
- Thermal problems: `CUT:N 1e-8` (0.01 eV)
- Fast problems: `CUT:N 0.01` (0.01 MeV)
- Photons: `CUT:P 0.001` (1 keV)

---

## Cross-Section Libraries

**ZAID Format:** ZZZAAA.NNx

- ZZZ = atomic number
- AAA = mass number
- NN = library number
- x = type (c=continuous, t=thermal)

**Common Libraries:**
- 80c - ENDF/B-VIII.0 continuous
- 80t - ENDF/B-VIII.0 thermal
- 70c - ENDF/B-VII.0 continuous

---

## Best Practices

1. MODE card must be first
2. Use conservative energy cutoffs
3. Check library availability in xsdir
4. Match TMP to material temperatures
5. Document non-default settings

---

**END OF GUIDE**
