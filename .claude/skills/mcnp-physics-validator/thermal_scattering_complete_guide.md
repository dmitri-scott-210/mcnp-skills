# Complete Thermal Scattering Reference Guide

## Overview

This guide provides comprehensive information on S(α,β) thermal scattering libraries in MCNP, based on analysis of production HTGR reactor models and MCNP best practices.

---

## Why Thermal Scattering Matters

**Free gas scattering** (MCNP default): Assumes atoms are free, independent particles
**Thermal scattering** (with MT card): Accounts for chemical binding, crystal structure, molecular motion

**Impact of missing MT cards**:
| Material | Reactivity Error | Spectrum Error | Typical Application |
|----------|------------------|----------------|---------------------|
| Graphite | 1000-5000 pcm | 10-20% | HTGR, RBMK, fast reactor reflectors |
| Light water | 500-2000 pcm | 5-15% | PWR, BWR, research reactors |
| Heavy water | 800-3000 pcm | 10-25% | CANDU, research reactors |
| Beryllium | 200-1000 pcm | 2-10% | Reflectors, test reactors |
| Polyethylene | 100-500 pcm | 2-5% | Neutron shielding |

**Conclusion**: Missing MT cards invalidate thermal neutron results!

---

## Graphite Thermal Scattering

### Available Libraries

| Library | Temperature | Application |
|---------|-------------|-------------|
| grph.10t | 296K (23°C) | Cold critical experiments, zero-power tests |
| grph.18t | 600K (327°C) | **HTGR operating (most common)**, some fast reactors |
| grph.22t | 800K (527°C) | High-temperature HTGR designs |
| grph.24t | 1000K (727°C) | VHTR (Very High Temperature Reactor) operating |
| grph.26t | 1200K (927°C) | VHTR accident scenarios |
| grph.28t | 1600K (1327°C) | Severe accident conditions |
| grph.30t | 2000K (1727°C) | Extreme accident analysis |

### Selection Guide

```python
def select_graphite_library(temperature_K):
    if temperature_K < 400:
        return 'grph.10t'  # Room temperature
    elif temperature_K < 700:
        return 'grph.18t'  # HTGR operating - MOST COMMON
    elif temperature_K < 900:
        return 'grph.22t'  # High-temp HTGR
    elif temperature_K < 1100:
        return 'grph.24t'  # VHTR
    elif temperature_K < 1400:
        return 'grph.26t'  # VHTR accident
    elif temperature_K < 1800:
        return 'grph.28t'  # Severe accident
    else:
        return 'grph.30t'  # Extreme conditions
```

### Examples

**HTGR operating at 600K**:
```mcnp
m1  $ Graphite moderator/reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ 600K - CORRECT for HTGR
```

**TRISO particle buffer layer** (600K):
```mcnp
m2  $ Porous carbon buffer
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ REQUIRED even for particle coating!
```

**Cold critical experiment**:
```mcnp
m3  $ Graphite at room temperature
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.10t  $ 296K - CORRECT for cold critical
```

---

## Light Water Thermal Scattering

### Available Libraries

| Library | Temperature | Application |
|---------|-------------|-------------|
| lwtr.10t | 294K (21°C) | Room temperature, cold critical |
| lwtr.11t | 325K (52°C) | **PWR cold leg, common operating** |
| lwtr.13t | 350K (77°C) | **PWR average, most common** |
| lwtr.14t | 400K (127°C) | PWR hot leg |
| lwtr.16t | 500K (227°C) | Supercritical water reactor |
| lwtr.20t | 800K (527°C) | Steam conditions, BWR |

### Selection Guide

```python
def select_water_library(temperature_K):
    if temperature_K < 310:
        return 'lwtr.10t'  # Room temperature
    elif temperature_K < 337:
        return 'lwtr.11t'  # PWR cold leg
    elif temperature_K < 375:
        return 'lwtr.13t'  # PWR average - MOST COMMON
    elif temperature_K < 450:
        return 'lwtr.14t'  # PWR hot leg
    elif temperature_K < 650:
        return 'lwtr.16t'  # Supercritical
    else:
        return 'lwtr.20t'  # Steam
```

### Examples

**PWR at 350K average**:
```mcnp
m1  $ Light water moderator
    1001.70c  2.0
    8016.70c  1.0
mt1 lwtr.13t  $ 350K - CORRECT for PWR
```

**BWR steam regions**:
```mcnp
m2  $ Steam
    1001.70c  2.0
    8016.70c  1.0
mt2 lwtr.20t  $ 800K - High temperature
```

**Research reactor pool**:
```mcnp
m3  $ Water pool at room temperature
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.10t  $ 294K - Room temperature
```

---

## Heavy Water Thermal Scattering

### Available Libraries

| Library | Temperature | Application |
|---------|-------------|-------------|
| hwtr.10t | 294K (21°C) | Room temperature |
| hwtr.11t | 325K (52°C) | **CANDU operating (most common)** |

### Examples

**CANDU reactor**:
```mcnp
m1  $ Heavy water moderator
    1002.70c  2.0  $ Deuterium
    8016.70c  1.0
mt1 hwtr.11t  $ 325K - CANDU operating
```

---

## Beryllium Thermal Scattering

### Available Library

| Library | Temperature | Application |
|---------|-------------|-------------|
| be.01t | 296K | Beryllium metal reflectors, moderators |

### Examples

**Pure beryllium reflector**:
```mcnp
m1  $ Beryllium metal
    4009.60c  1.23621-1
mt1 be.01t  $ REQUIRED!
```

**Mixed beryllium + water** (DUAL S(α,β)):
```mcnp
m2  $ Be + H2O mixture
    1001.70c  3.40940-3
    8016.70c  1.70470-3
    4009.60c  1.17316-1
mt2 lwtr.10t be.01t  $ BOTH required!
```

**Note**: For Be + H₂O, **BOTH** lwtr and be libraries must be specified!

---

## Polyethylene Thermal Scattering

### Available Library

| Library | Temperature | Application |
|---------|-------------|-------------|
| poly.10t | 296K | Polyethylene (CH₂)ₙ shielding |

### Examples

**Neutron shield**:
```mcnp
m1  $ Polyethylene
    1001.70c  0.667  $ Hydrogen
    6000.70c  0.333  $ Carbon
mt1 poly.10t  $ REQUIRED for shielding
```

---

## Validation Checklist

### Before Running Any Thermal Neutron Calculation:

#### 1. Identify Materials Requiring S(α,β)

- [ ] List all materials containing C (carbon/graphite)
- [ ] List all materials containing H (light water, polyethylene)
- [ ] List all materials containing D (heavy water)
- [ ] List all materials containing Be (beryllium)

#### 2. Check MT Cards Present

- [ ] Every graphite material has `mtX grph.XXt`
- [ ] Every water material has `mtX lwtr.XXt`
- [ ] Every D₂O material has `mtX hwtr.XXt`
- [ ] Every Be material has `mtX be.01t`
- [ ] Every polyethylene material has `mtX poly.XXt`

#### 3. Verify Temperature Appropriateness

- [ ] Graphite: grph.18t for 600K HTGR operating
- [ ] Water: lwtr.13t for 350K PWR average
- [ ] Room temp experiments: grph.10t, lwtr.10t

#### 4. Check for Mixed Materials

- [ ] Be + H₂O: Both `lwtr.XXt be.01t` specified
- [ ] No missing components in dual S(α,β)

#### 5. Review MCNP Output

- [ ] Check for "free gas scattering" warnings
- [ ] Verify MT libraries loaded correctly
- [ ] Look for missing data warnings

### Common Mistakes to Avoid

❌ **Missing graphite MT card entirely** (1000-5000 pcm error!)
❌ **Room temp library for operating reactor** (grph.10t for 600K reactor)
❌ **Water without MT card** (500-2000 pcm error!)
❌ **Mixed Be + H₂O with only one S(α,β)** (incomplete physics)
❌ **Assuming MCNP will warn** (it runs without error but results are wrong!)

---

## Real-World Example: AGR-1 TRISO Fuel

**Problem Found**: AGR-1 model had ~50 graphite materials WITHOUT MT cards!

**Materials affected**:
- m9040-m9056: Graphite spacers ← Missing grph.18t
- m9070-m9075: Borated graphite holders ← Missing grph.18t
- m9090: Buffer layer (porous carbon) ← Missing grph.18t
- m9091: IPyC (dense carbon) ← Missing grph.18t
- m9093: OPyC (dense carbon) ← Missing grph.18t
- m9094: Matrix (graphite) ← Missing grph.18t

**Impact**:
- Wrong thermal neutron spectrum
- Reactivity error estimated 1000-5000 pcm
- Invalid benchmark comparisons

**Fix**:
```mcnp
mt9040 grph.18t  $ Graphite spacers
mt9070 grph.18t  $ Borated graphite holders
mt9071 grph.18t
mt9072 grph.18t
mt9073 grph.18t
mt9074 grph.18t
mt9075 grph.18t
mt9090 grph.18t  $ Buffer layer
mt9091 grph.18t  $ IPyC
mt9093 grph.18t  $ OPyC
mt9094 grph.18t  $ Matrix
```

**Lesson**: Even production models can have critical physics errors!

---

## TRISO Particle Complete Validation

### Five-Layer TRISO Structure

```
┌─────────────────────────────────────────┐
│  Matrix (m6) - needs grph.18t          │
│  ┌─────────────────────────────────┐    │
│  │ OPyC (m5) - needs grph.18t     │    │
│  │ ┌─────────────────────────────┐ │    │
│  │ │ SiC (m4) - NO MT needed    │ │    │
│  │ │ ┌─────────────────────────┐ │ │    │
│  │ │ │ IPyC (m3) - grph.18t   │ │ │    │
│  │ │ │ ┌─────────────────────┐ │ │ │    │
│  │ │ │ │ Buffer (m2)        │ │ │ │    │
│  │ │ │ │   - needs grph.18t │ │ │ │    │
│  │ │ │ │ ┌─────────────────┐ │ │ │ │    │
│  │ │ │ │ │ UCO Kernel     │ │ │ │ │    │
│  │ │ │ │ │ (m1) NO MT     │ │ │ │ │    │
│  │ │ │ │ └─────────────────┘ │ │ │ │    │
│  │ │ │ └─────────────────────┘ │ │ │    │
│  │ │ └─────────────────────────┘ │ │    │
│  │ └─────────────────────────────┘ │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Layer-by-Layer Requirements

**Layer 1: UCO Kernel**
- Contains: U, C, O
- MT card: **NO** - This is fuel, not moderator
- Validation: Skip MT check if material contains U/Pu

**Layer 2: Buffer (Porous Carbon)**
- Contains: Pure carbon (porous)
- MT card: **YES** - grph.18t required
- Impact if missing: Wrong neutron thermalization in fuel

**Layer 3: IPyC (Inner Pyrolytic Carbon)**
- Contains: Dense carbon
- MT card: **YES** - grph.18t required
- Impact if missing: Wrong neutron transport through coating

**Layer 4: SiC (Silicon Carbide)**
- Contains: Si, C (ceramic)
- MT card: **NO** - Ceramic, not graphite crystal structure
- Validation: Skip MT check for SiC

**Layer 5: OPyC (Outer Pyrolytic Carbon)**
- Contains: Dense carbon
- MT card: **YES** - grph.18t required
- Impact if missing: Wrong particle-to-particle neutron transport

**Layer 6: Graphite Matrix**
- Contains: Pure graphite
- MT card: **YES** - grph.18t required
- Impact if missing: Wrong fuel compact neutronics

### Complete TRISO Validation Example

```mcnp
c ===================================================
c TRISO Particle - COMPLETE with MT cards
c ===================================================

c Layer 1: UCO Kernel
m1  $ UCO fuel kernel
   92235.00c  0.002   $ U-235 enriched
   92238.00c  0.008   $ U-238
    6012.00c  0.32    $ Carbon (in UCO)
    8016.00c  1.36    $ Oxygen
c NO MT card - fuel material

c Layer 2: Buffer (porous carbon)
m2  $ Buffer layer
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ ✅ REQUIRED - 600K

c Layer 3: IPyC
m3  $ Inner PyC
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.18t  $ ✅ REQUIRED - 600K

c Layer 4: SiC
m4  $ Silicon carbide
   14028.00c  0.9223  $ Si-28
   14029.00c  0.0468  $ Si-29
   14030.00c  0.0309  $ Si-30
    6012.00c  0.9890  $ C-12
    6013.00c  0.0110  $ C-13
c NO MT card - ceramic, not graphite

c Layer 5: OPyC
m5  $ Outer PyC
    6012.00c  0.9890
    6013.00c  0.0110
mt5 grph.18t  $ ✅ REQUIRED - 600K

c Layer 6: Matrix
m6  $ Graphite matrix
    6012.00c  0.9890
    6013.00c  0.0110
mt6 grph.18t  $ ✅ REQUIRED - 600K
```

---

## Temperature Conversion

### Kelvin to Celsius

```
T(°C) = T(K) - 273.15

Examples:
600K = 327°C (HTGR operating)
350K = 77°C (PWR average)
800K = 527°C (High-temp HTGR)
```

### Common Reactor Operating Temperatures

| Reactor Type | Temperature | Recommended Library |
|--------------|-------------|---------------------|
| PWR cold leg | 325K (52°C) | lwtr.11t |
| PWR average | 350K (77°C) | lwtr.13t |
| PWR hot leg | 400K (127°C) | lwtr.14t |
| HTGR operating | 600K (327°C) | grph.18t |
| VHTR operating | 1000K (727°C) | grph.24t |
| CANDU | 325K (52°C) | hwtr.11t |
| Cold critical | 296K (23°C) | grph.10t, lwtr.10t |

---

## Summary

**CRITICAL RULES**:

1. ✅ **ALWAYS use MT cards for C, H, D, Be** in thermal systems
2. ✅ **Match library temperature to operating conditions**
3. ✅ **Use BOTH S(α,β) for mixed materials** (Be + H₂O)
4. ✅ **Validate BEFORE running** - MCNP won't warn!
5. ✅ **Check output for "free gas" warnings**

**Remember**: Missing MT cards are **CRITICAL ERRORS**, not optional!

**Impact**: 1000-5000 pcm reactivity errors, wrong thermal spectrum, invalid results

**Fix**: Add appropriate MT cards for ALL moderator/reflector materials

---

**END OF GUIDE**
