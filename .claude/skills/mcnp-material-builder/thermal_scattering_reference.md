# Thermal Scattering S(α,β) Reference

## Purpose
Comprehensive reference for MT cards, S(α,β) tables, MT0 special treatment, and thermal neutron scattering data.

---

## MT Card: Thermal Neutron Scattering

**Format:**
```
MTm  sabid1  sabid2  ...  sabidK
```

**Purpose:** Attach S(α,β) neutron thermal scattering tables to material m to account for molecular binding effects at low energies (E < ~10 eV).

**Effect:** Replaces free-gas neutron physics with molecular/crystalline binding effects for specified nuclides.

---

## Complete S(α,β) Table Listing

### Moderators (Common)

| Material | Modern ID | Old ID | Temperature | Target Nuclide | Application |
|----------|-----------|--------|-------------|----------------|-------------|
| **Light Water (H₂O)** | H-H2O.40t | LWTR.01T | 293.6 K | Hydrogen | Reactors, shielding |
| | H-H2O.41t | LWTR.02T | 323.6 K | | Warm water |
| | H-H2O.42t | LWTR.03T | 373.6 K | | Hot water |
| | H-H2O.43t | LWTR.04T | 423.6 K | | Pressurized water |
| | H-H2O.44t | LWTR.05T | 473.6 K | | High-temp water |
| | H-H2O.45t | LWTR.06T | 523.6 K | | Very hot water |
| | H-H2O.46t | LWTR.07T | 573.6 K | | Steam regime |
| | H-H2O.47t | LWTR.08T | 623.6 K | | Superheated steam |
| | H-H2O.48t | LWTR.09T | 800 K | | High-temp applications |
| **Heavy Water (D₂O)** | D-D2O.40t | HWTR.01T | 293.6 K | Deuterium | CANDU reactors |
| | D-D2O.41t | HWTR.02T | 323.6 K | | Warm D₂O |
| | D-D2O.42t | HWTR.03T | 373.6 K | | Hot D₂O |
| | D-D2O.43t | HWTR.04T | 423.6 K | | High-temp D₂O |
| **Polyethylene (CH₂)** | H-CH2.40t | POLY.01T | 293.6 K | Hydrogen | Shielding, moderators |
| | H-CH2.42t | POLY.02T | 350 K | | Elevated temp |
| **Graphite (C)** | C-GRPH.40t | GRPH.47T | 293.6 K | Carbon | High-temp reactors |
| | C-GRPH.41t | GRPH.48T | 400 K | | Warm graphite |
| | C-GRPH.42t | GRPH.49T | 500 K | | Elevated temp |
| | C-GRPH.43t | GRPH.50T | 600 K | | Reactor operating temp |
| | C-GRPH.44t | GRPH.51T | 700 K | | High-temp reactor |
| | C-GRPH.45t | GRPH.52T | 800 K | | Very hot graphite |
| | C-GRPH.46t | GRPH.53T | 1000 K | | VHTR applications |
| | C-GRPH.47t | GRPH.54T | 1200 K | | Extreme temp |
| | C-GRPH.48t | GRPH.55T | 1600 K | | Ultra-high temp |
| | C-GRPH.49t | GRPH.56T | 2000 K | | Maximum temp |

### Other Moderators and Materials

| Material | Modern ID | Old ID | Temperature | Target | Application |
|----------|-----------|--------|-------------|--------|-------------|
| **Beryllium Metal** | Be-MET.40t | BE.46T | 293.6 K | Beryllium | Reflectors |
| | Be-MET.41t | BE.47T | 400 K | | Warm Be |
| | Be-MET.42t | BE.48T | 500 K | | Elevated temp |
| | Be-MET.43t | BE.49T | 600 K | | Reactor temp |
| | Be-MET.44t | BE.50T | 700 K | | High temp |
| | Be-MET.45t | BE.51T | 800 K | | Very high temp |
| | Be-MET.46t | BE.52T | 1000 K | | Maximum temp |
| **Beryllium Oxide (BeO)** | Be-BEO.40t | BEBEO.01T | 293.6 K | Beryllium | Reflectors, moderators |
| | O-BEO.40t | OBEO.01T | 293.6 K | Oxygen | (both Be and O need MT) |
| **Benzene (C₆H₆)** | H-BENZ.40t | BENZ.01T | 293.6 K | Hydrogen | Organic moderators |
| **Zirconium Hydride (ZrH)** | H-ZRH.40t | ZRH.01T | 293.6 K | Hydrogen | TRIGA reactors |
| | H-ZRH.42t | ZRH.02T | 400 K | | Elevated temp |
| | H-ZRH.43t | ZRH.03T | 500 K | | Hot ZrH |
| | H-ZRH.44t | ZRH.04T | 600 K | | High-temp ZrH |
| | H-ZRH.45t | ZRH.05T | 700 K | | Very hot ZrH |
| | H-ZRH.46t | ZRH.06T | 800 K | | Maximum temp |

---

## Naming Conventions

### Modern Format (Target-Molecule)
```
Target-Molecule.nnX

Target:    Element-Isotope (H, D, C, Be, O)
Molecule:  H2O, D2O, CH2, GRPH, BEO, etc.
nn:        Temperature code (40-49 typically)
X:         Physics identifier (t = thermal scattering)
```

**Examples:**
- `H-H2O.40t` = Hydrogen in water at 293.6 K
- `D-D2O.43t` = Deuterium in heavy water at 423.6 K
- `C-GRPH.46t` = Carbon in graphite at 1000 K

### Old Format (Legacy)
```
NAME.nnT

NAME:  Short name (LWTR, HWTR, POLY, GRPH, etc.)
nn:    Sequential number (01, 02, 03, ...)
T:     Thermal scattering indicator
```

**Examples:**
- `LWTR.01T` = Light water at 293.6 K
- `GRPH.47T` = Graphite at 293.6 K
- `POLY.01T` = Polyethylene at 293.6 K

**Compatibility:** Both formats work in MCNP6. Modern format preferred for clarity.

---

## Temperature Code Mapping

| Temperature Code (nn) | Temperature (K) | Temperature (°C) | Common Use |
|----------------------|-----------------|------------------|------------|
| 40 | 293.6 | 20 | Room temperature |
| 41 | 323.6 | 50 | Slightly warm |
| 42 | 373.6 | 100 | Boiling water |
| 43 | 423.6 | 150 | Pressurized water |
| 44 | 473.6 | 200 | High-pressure steam |
| 45 | 523.6 | 250 | Superheated |
| 46 | 573.6-1000 | 300-727 | Reactor operating |
| 47 | 1200 | 927 | High-temp reactor |
| 48 | 1600 | 1327 | Very high temp |
| 49 | 2000 | 1727 | Maximum |

**Note:** Exact temperature depends on material. Consult xsdir for precise values.

---

## When to Use MT Card

### Use S(α,β) for:
✅ Moderators with light nuclei (H, D, C, Be)
✅ Thermal neutron problems (E < 1 eV dominant)
✅ Criticality calculations in moderated systems
✅ Accurate thermalization modeling
✅ Reactor physics applications

### Skip MT card for:
❌ High-energy problems only (E > 1 MeV, no thermalization)
❌ Heavy materials (Fe, Pb, U - no molecular effects)
❌ Non-moderating materials
❌ Void or gas regions (unless hydrogen-containing)

---

## MT Card Examples

### Example 1: Light Water (Simple)
```
M1   1001.80c  2  8016.80c  1      $ H₂O composition
MT1  H-H2O.40t                      $ S(α,β) at 293.6 K
c Cell card:
1    1  -0.1003  -1  IMP:N=1  TMP=2.53e-8
```

### Example 2: Heavy Water
```
M2   1002.80c  2  8016.80c  1      $ D₂O composition
MT2  D-D2O.40t                      $ S(α,β) for deuterium at 293.6 K
c Cell:
2    2  -0.110  -2  IMP:N=1  TMP=2.53e-8
```

### Example 3: Polyethylene
```
M3   1001.80c  2  6000.80c  1      $ (CH₂)n composition
MT3  H-CH2.40t                      $ S(α,β) for H in polyethylene
c Cell:
3    3  -0.0867  -3  IMP:N=1  TMP=2.53e-8
```

### Example 4: Graphite at High Temperature
```
M4   6000.80c  1                   $ Carbon
MT4  C-GRPH.46t                     $ S(α,β) at 1000 K
c Cell:
4    4  -1.70  -4  IMP:N=1  TMP=8.62e-8    $ T=1000 K
```

### Example 5: Mixed Moderators (Water + Beryllium)
```
M5   1001.80c  2  8016.80c  1  4009.80c  0.001   $ H₂O with trace Be
MT5  H-H2O.40t  Be-MET.40t                       $ S(α,β) for both H and Be
c Cell:
5    5  -1.0  -5  IMP:N=1  TMP=2.53e-8
```

**IMPORTANT:** All specified nuclides affected by their respective S(α,β) tables.

---

## MT0 Card: Special Treatment for Stochastic Mixing

### Purpose
Match specific S(α,β) tables to specific isotope libraries when using **stochastic temperature mixing** (approximating intermediate temperatures with weighted mixtures).

### Format
```
MT0  sabid1  identifier_1  sabid2  identifier_2  ...
```

**Pairs:** Each S(α,β) table (sabid) is matched to a specific nuclide library (identifier).

### When to Use MT0
- **Stochastic mixing:** Material at temperature T₁ < T_cell < T₂, using mixture of T₁ and T₂ libraries
- **Multiple temperatures:** Same nuclide appears multiple times in M card at different temperatures
- **Precise matching required:** Ensure correct S(α,β) table used with correct nuclear data library

### Example: Water at Intermediate Temperature

**Problem:** Cell at 446.8 K, but S(α,β) tables only available at 293.6 K and 600 K.

**Solution:** Stochastic mixing with 50% at each temperature.

```
c MT0 card: Match S(α,β) to specific isotope libraries
MT0  H-H2O.40t  1001.00c      $ 293.6 K S(α,β) ↔ H-1 at 293.6 K library
     H-H2O.54t  1001.01c      $ 600 K S(α,β) ↔ H-1 at 600 K library

c Material card: 50% at low temp, 50% at high temp
M100  1001.00c  1.0  8016.00c  0.5    $ H and O at 293.6 K
      1001.01c  1.0  8016.01c  0.5    $ H and O at 600 K

c MT card: Include both S(α,β) tables
MT100  H-H2O.40t  H-H2O.54t

c Cell card:
100  100  -1.0  -100  IMP:N=1  TMP=3.85e-8    $ T=446.8 K
```

**How it works:**
- MCNP stochastically samples 293.6 K data 50% of time, 600 K data 50% of time
- MT0 ensures H-H2O.40t modifies only 1001.00c, and H-H2O.54t modifies only 1001.01c
- Average approximates 446.8 K behavior

**Verification:** Check PRINT Table 102 to verify correct assignments.

---

## Temperature Matching: TMP and MT

**CRITICAL RULE:** MT table temperature MUST match TMP card temperature.

### Temperature Conversion
```
T [MeV] = T [K] × 8.617×10⁻¹¹

Examples:
293.6 K → 2.53×10⁻⁸ MeV
600 K   → 5.17×10⁻⁸ MeV
1000 K  → 8.62×10⁻⁸ MeV
```

### Correct Matching
```
c Consistent:
M1   1001  2  8016  1
MT1  H-H2O.40t                       $ S(α,β) at 293.6 K
c Cell card:
1    1  -0.1003  -1  TMP=2.53e-8  IMP:N=1    $ T=293.6 K (matches MT1)
```

### Incorrect Matching (Physics Error)
```
c INCONSISTENT:
M1   1001  2  8016  1
MT1  H-H2O.40t                       $ S(α,β) at 293.6 K
c Cell card:
1    1  -0.08  -1  TMP=5.17e-8  IMP:N=1      $ T=600 K (MISMATCH!)
```

**Fix:** Use `MT1  H-H2O.43t` for 600 K.

---

## Troubleshooting S(α,β) Issues

### Error: S(α,β) Table Not Found
**Symptom:**
```
fatal error. S(alpha,beta) table H-H2O.99t not found in xsdir.
```

**Cause:** Specified table doesn't exist in cross-section library.

**Fix:**
1. Check available tables in `$DATAPATH/xsdir`
2. Use correct temperature code (40-49 range)
3. Verify modern vs old naming convention

### Error: Multiple Tables Affect Same Nuclide
**Symptom:**
```
warning. multiple S(alpha,beta) tables affect hydrogen in material 1.
```

**Cause:** Two S(α,β) tables both target same element (e.g., H-H2O and H-CH2).

**Fix:**
- Remove conflicting table, or
- Use MT0 card for explicit matching (stochastic mixing case)

### Warning: No S(α,β) for Moderator
**Symptom:** Inaccurate thermal flux, wrong keff

**Cause:** Missing MT card for water/graphite/polyethylene.

**Fix:** Add appropriate MT card for moderator material.

---

## Best Practices

1. **Always use MT for moderators:** H₂O, D₂O, graphite, polyethylene, beryllium
2. **Match temperatures:** MT table temperature = TMP card temperature
3. **Modern naming preferred:** Use `H-H2O.40t` instead of `LWTR.01T` for clarity
4. **Check PRINT Table 102:** Verify S(α,β) assignments are correct
5. **Stochastic mixing:** Use MT0 card for precise library matching at intermediate temperatures
6. **Skip for heavy materials:** No S(α,β) needed for Fe, Pb, U, etc.

---

## CRITICAL REMINDER: Graphite MT Cards

### Impact of Missing Graphite S(α,β)

**Found in professional reactor models**: AGR-1 HTGR model had 50+ graphite materials with **ZERO MT cards**!

**Physics errors**:
- Free-gas scattering used instead of crystalline binding
- Thermal spectrum too hard (overestimates high-energy tail)
- Reactivity error: 1000-5000 pcm (model-dependent)
- Flux distribution spatially incorrect
- Benchmark validation FAILS

**Materials requiring graphite MT cards**:
```mcnp
c Pure graphite (moderator, reflector)
M1   6012.00c  0.9890  6013.00c  0.0110
MT1  C-GRPH.43t  $ REQUIRED! (600K example)

c TRISO buffer (porous carbon)
M2   6012.00c  0.9890  6013.00c  0.0110
MT2  C-GRPH.43t  $ REQUIRED!

c PyC coating layers (dense pyrolytic carbon)
M3   6012.00c  0.9890  6013.00c  0.0110
MT3  C-GRPH.43t  $ REQUIRED!

c Graphite matrix
M4   6012.00c  0.9890  6013.00c  0.0110
MT4  C-GRPH.43t  $ REQUIRED!

c SiC with carbon (may benefit from MT card)
M5  14000.00c  0.5  6012.00c  0.4890  6013.00c  0.0110
MT5  C-GRPH.43t  $ Recommended for thermal systems
```

**Temperature selection for graphite**:

| Reactor State | Temperature | S(α,β) Table | Code |
|---------------|-------------|--------------|------|
| Cold critical | 293 K | C-GRPH.40t | grph.40t |
| Startup | 400 K | C-GRPH.41t | grph.41t |
| Low power | 500 K | C-GRPH.42t | grph.42t |
| Operating (typical HTGR) | 600 K | C-GRPH.43t | grph.43t |
| High power | 700 K | C-GRPH.44t | grph.44t |
| Very high temp | 800 K | C-GRPH.45t | grph.45t |
| VHTR normal | 1000 K | C-GRPH.46t | grph.46t |
| VHTR high temp | 1200 K | C-GRPH.47t | grph.47t |
| Accident conditions | 1600 K | C-GRPH.48t | grph.48t |
| Maximum | 2000 K | C-GRPH.49t | grph.49t |

**CRITICAL DECISION**:
```
Modeling graphite-containing reactor?
  ├─→ Thermal neutrons present (E < 1 eV)?
  │    ├─→ YES: MT card MANDATORY
  │    └─→ NO (fast reactor): MT card optional
  │
  └─→ What temperature?
       ├─→ Match TMP card temperature
       └─→ Use closest available S(α,β) table
```

**Validation script** (use before running):
```bash
python scripts/thermal_scattering_checker.py input.i
```

Expected output:
```
Checking material M1 (carbon detected):
  ✅ MT1 card present: C-GRPH.43t
  ✅ Temperature match: TMP1 = 5.17e-8 MeV (600K), MT1 = 600K

Checking material M2 (carbon detected):
  ❌ ERROR: No MT card found for carbon-containing material M2!
  ❌ CRITICAL: Missing thermal scattering will cause physics errors!
  FIX: Add MT2  C-GRPH.43t (or appropriate temperature)
```

---

## See Also

- **Material Specifications:** `material_card_specifications.md` for M card keywords
- **Advanced Cards:** `advanced_material_cards.md` for OTFDB (on-the-fly Doppler)
- **Error Catalog:** `material_error_catalog.md` for troubleshooting
- **MCNP Documentation:** Chapter 5.6.2 (MT Card), Section 2.3.6 (S(α,β) Theory)

---

**Version:** 1.0
**Created:** 2025-11-03
**For:** mcnp-material-builder skill v2.0
