# Thermal Scattering (S(α,β)) Reference Guide

**Purpose:** Complete guide to MCNP thermal scattering libraries (MT cards)

**CRITICAL:** Missing thermal scattering = 1000-5000 pcm reactivity error!

---

## When Thermal Scattering is REQUIRED

### ALWAYS Required For:

✅ **ALL graphite** (any reactor type)
- HTGRs, RBMKs, MSRs, graphite-moderated research reactors
- Impact if missing: ~2000 pcm error in keff
- Impact if wrong temperature: ~500 pcm error

✅ **ALL water** (light or heavy)
- PWRs, BWRs, CANDUs, research reactors
- Impact if missing: ~3000 pcm error in keff
- Impact if wrong temperature: ~200 pcm error

✅ **Polyethylene** (CH₂)
- Shielding materials
- Moderator in some compact reactors
- Impact if missing: Dose rates wrong by factor of 2-5

✅ **Beryllium and BeO**
- Reflectors, neutron sources
- Impact if missing: ~1000 pcm error in reflector worth

---

## Complete Library List

### Graphite (grph)

| Library | Temperature (K) | Use Case |
|---------|----------------|----------|
| grph.10t | 294 | Room temperature, cold critical |
| grph.11t | 350 | Warm startup |
| grph.12t | 400 | Heating to operating |
| grph.13t | 450 | Intermediate |
| grph.14t | 500 | Approaching operating |
| grph.15t | 550 | Near operating |
| grph.16t | 600 | HTGR cold leg |
| grph.17t | 650 | HTGR intermediate |
| grph.18t | 700 | HTGR hot leg (TYPICAL) |
| grph.19t | 800 | High temperature |
| grph.20t | 1000 | Very high temperature |
| grph.21t | 1200 | Extreme temperature |
| grph.22t | 1600 | Maximum available |
| grph.23t | 2000 | Accident scenarios |

**Selection guide:**
```mcnp
c HTGR operating (average 600-700K)
m1  6012.00c 0.9890  6013.00c 0.0110
mt1 grph.18t  $ 700K - typical HTGR operating

c HTGR cold critical (room temperature)
m2  6012.00c 0.9890  6013.00c 0.0110
mt2 grph.10t  $ 294K - startup physics

c Graphite reflector (cooler than core)
m3  6012.00c 0.9890  6013.00c 0.0110
mt3 grph.16t  $ 600K - reflector temperature
```

---

### Light Water (lwtr)

| Library | Temperature (K) | Use Case |
|---------|----------------|----------|
| lwtr.10t | 294 | Room temperature, pools |
| lwtr.11t | 325 | PWR cold leg |
| lwtr.12t | 350 | PWR average |
| lwtr.13t | 400 | PWR hot leg (TYPICAL) |
| lwtr.14t | 450 | BWR conditions |
| lwtr.15t | 500 | High temperature |
| lwtr.16t | 550 | Supercritical |
| lwtr.17t | 600 | Very high temperature |

**Selection guide:**
```mcnp
c PWR operating (hot leg ~350-400K)
m1  1001.70c 2.0  8016.70c 1.0
mt1 lwtr.13t  $ 400K - PWR hot leg

c PWR cold leg (~325K)
m2  1001.70c 2.0  8016.70c 1.0
mt2 lwtr.11t  $ 325K - PWR cold leg

c Research reactor pool (room temperature)
m3  1001.70c 2.0  8016.70c 1.0
mt3 lwtr.10t  $ 294K - room temperature
```

---

### Heavy Water (hwtr)

| Library | Temperature (K) | Use Case |
|---------|----------------|----------|
| hwtr.10t | 294 | Room temperature |
| hwtr.11t | 325 | CANDU operating (TYPICAL) |
| hwtr.12t | 350 | High temperature |
| hwtr.13t | 400 | Very high temperature |

**Selection guide:**
```mcnp
c CANDU moderator (operating ~325K)
m1  1002.70c 2.0  8016.70c 1.0
mt1 hwtr.11t  $ 325K - CANDU operating

c Heavy water reflector (room temperature)
m2  1002.70c 2.0  8016.70c 1.0
mt2 hwtr.10t  $ 294K - cold reflector
```

---

### Polyethylene (poly)

| Library | Temperature (K) | Use Case |
|---------|----------------|----------|
| poly.10t | 294 | Room temperature (TYPICAL) |
| poly.11t | 350 | Elevated temperature |

**Selection guide:**
```mcnp
c Polyethylene shield (room temperature)
m1  1001.70c 2.0  6012.00c 1.0
mt1 poly.10t  $ 294K - typical shielding

c Note: Polyethylene is (CH2)n
c Ratio: 2 H atoms per 1 C atom
```

---

### Beryllium (be)

| Library | Temperature (K) | Use Case |
|---------|----------------|----------|
| be.10t | 294 | Room temperature |
| be.11t | 400 | Elevated temperature |
| be.12t | 600 | High temperature |
| be.13t | 800 | Very high temperature |
| be.14t | 1000 | Maximum available |

**Selection guide:**
```mcnp
c Beryllium reflector (room temperature)
m1  4009.70c 1.0
mt1 be.10t  $ 294K - typical reflector
```

---

### Beryllium Oxide (beo)

| Library | Temperature (K) | Use Case |
|---------|----------------|----------|
| beo.10t | 294 | Room temperature |
| beo.11t | 400 | Elevated temperature |
| beo.12t | 600 | High temperature |
| beo.13t | 800 | Very high temperature |
| beo.14t | 1000 | Maximum available |

**Selection guide:**
```mcnp
c BeO reflector (operating ~600K)
m1  4009.70c 1.0  8016.70c 1.0
mt1 beo.12t  $ 600K - operating temperature

c Note: BeO stoichiometry is 1:1
```

---

## Temperature Selection Guidelines

### General Rules:

1. **Match physics temperature**
   - Use operating temperature, not room temperature
   - Account for spatial variations (core vs reflector)

2. **Conservative selection**
   - If unsure, choose slightly higher temperature
   - Better to overestimate than underestimate

3. **Document assumptions**
   - Comment why temperature chosen
   - Reference source of temperature data

4. **Consistency across materials**
   - Don't mix 294K and 700K in same region
   - Reflect actual temperature profile

### Reactor-Specific Guidelines:

**HTGRs:**
- Core graphite: 600-1000K (grph.16t to grph.20t)
- Reflector graphite: 500-700K (grph.14t to grph.18t)
- TRISO coating PyC: same as compact (grph.18t typical)
- Typical choice: grph.18t (700K) for operating conditions

**PWRs:**
- Hot leg water: 350-400K (lwtr.12t to lwtr.13t)
- Cold leg water: 300-325K (lwtr.10t to lwtr.11t)
- Average: 350K (lwtr.12t)
- Typical choice: lwtr.13t (400K) for hot assembly

**CANDUs:**
- Heavy water moderator: 325K (hwtr.11t)
- Heavy water coolant: 325K (hwtr.11t)
- Typical choice: hwtr.11t for all D₂O

---

## Common Errors and Fixes

### Error 1: Missing MT Card

**Problem:**
```mcnp
m1  6012.00c 0.9890  6013.00c 0.0110  $ Graphite - NO MT CARD!
```

**Fix:**
```mcnp
m1  6012.00c 0.9890  6013.00c 0.0110
mt1 grph.18t  $ 700K thermal scattering - REQUIRED!
```

**Impact:** ~2000 pcm reactivity error for graphite

---

### Error 2: Wrong Temperature

**Problem:**
```mcnp
c HTGR operating at 700K
m1  6012.00c 0.9890  6013.00c 0.0110
mt1 grph.10t  $ WRONG! 294K library for 700K physics
```

**Fix:**
```mcnp
c HTGR operating at 700K
m1  6012.00c 0.9890  6013.00c 0.0110
mt1 grph.18t  $ CORRECT! 700K library
```

**Impact:** ~500 pcm reactivity error

---

### Error 3: MT Card for Wrong Material

**Problem:**
```mcnp
m1  26056.70c 1.0  $ Iron - does NOT need thermal scattering
mt1 grph.18t        $ WRONG! Graphite S(α,β) for iron
```

**Fix:**
```mcnp
m1  26056.70c 1.0  $ Iron - no MT card needed
```

**When NOT needed:** Heavy elements (Fe, Pb, U, etc.) at any energy

---

### Error 4: Inconsistent Library Families

**Problem:**
```mcnp
m1  92235.70c ...  $ ENDF/B-VII.0
    92238.21c ...  $ ENDF/B-IV (WRONG!)
    6012.80c  ...  $ ENDF/B-VIII.0 (WRONG!)
mt1 grph.18t
```

**Fix:**
```mcnp
m1  92235.70c ...  $ ENDF/B-VII.0
    92238.70c ...  $ ENDF/B-VII.0 (CONSISTENT)
    6012.70c  ...  $ ENDF/B-VII.0 (CONSISTENT)
mt1 grph.18t
```

---

## Validation Checklist

Before running MCNP:
- [ ] Every graphite material has MT card (grph.XXt)
- [ ] Every water material has MT card (lwtr.XXt or hwtr.XXt)
- [ ] Every polyethylene material has MT card (poly.XXt)
- [ ] Every Be/BeO material has MT card (be.XXt or beo.XXt)
- [ ] Temperature matches physics conditions (not all 294K!)
- [ ] Cross-section library families consistent (.70c, .80c, not mixed)
- [ ] Temperatures documented in comments

Automated check:
```bash
python reactor_model_checker.py input.i
# Will flag missing MT cards as CRITICAL errors
```

---

## Quick Reference Card

| Material | MT Syntax | Typical Operating | Cold Critical |
|----------|-----------|-------------------|---------------|
| Graphite | grph.XXt | grph.18t (700K) | grph.10t (294K) |
| Light water | lwtr.XXt | lwtr.13t (400K) | lwtr.10t (294K) |
| Heavy water | hwtr.XXt | hwtr.11t (325K) | hwtr.10t (294K) |
| Polyethylene | poly.XXt | poly.10t (294K) | poly.10t (294K) |
| Beryllium | be.XXt | be.10t (294K) | be.10t (294K) |
| BeO | beo.XXt | beo.12t (600K) | beo.10t (294K) |

---

## Impact Summary

| Missing MT Card | Typical Error | Critical? |
|-----------------|---------------|-----------|
| Graphite in HTGR | ~2000 pcm keff | YES |
| Water in PWR | ~3000 pcm keff | YES |
| Heavy water in CANDU | ~2500 pcm keff | YES |
| Polyethylene shield | Dose rates ×2-5 | YES |
| BeO reflector | ~1000 pcm worth | YES |

**Bottom line:** NEVER omit thermal scattering for these materials!

---

**END OF THERMAL SCATTERING REFERENCE**

For material building see: mcnp-material-builder skill
For validation see: reactor_model_checker.py
