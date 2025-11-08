---
name: mcnp-material-builder
version: 2.0.0
description: Build MCNP material definitions using M/MT/MX cards with proper ZAID selection, thermal scattering, and density calculations
---

# MCNP Material Builder

## Overview

This skill helps build material definitions for MCNP simulations using M (material), MT (thermal scattering), and MX (nuclide substitution) cards. Materials are specified using ZAID format (ZZZAAA.nnX) for isotope identification, with either atomic or weight fractions, and proper density assignments. Thermal scattering treatments (S(α,β)) are critical for materials containing low-Z nuclides in thermal systems.

Material definitions appear in the Data Cards block of MCNP input files. Proper material specification is essential for accurate physics simulation, as materials determine how particles interact, scatter, and are absorbed throughout the geometry.

For advanced topics including OTFDB (on-the-fly Doppler broadening), NONU (disable fission), XS (custom cross-sections), and detailed library specifications, see the comprehensive **root skill directory** for additional documentation.

## When to Use This Skill

- Building material cards for reactor cores, shielding, or experimental setups
- Converting physical compositions to MCNP M card format
- Selecting appropriate cross-section libraries (ZAID extensions)
- Adding S(α,β) thermal scattering treatments for hydrogenous materials
- Troubleshooting material-related errors ("cross section not found", density mismatches)
- Setting up temperature-dependent materials with TMP cards
- Creating material libraries for reuse across multiple inputs

## Decision Tree

```
User needs material definition
  ↓
Know composition?
  ├─→ No → Use material_card_specifications.md for common materials
  └─→ Yes
       ↓
  Composition in weight or atomic fractions?
       ├─→ Weight → Use negative fractions (sum to -1.0)
       ├─→ Atomic → Use positive fractions (ratios)
       └─→ Unsure → Use scripts/material_density_calculator.py
            ↓
       Select ZAID library?
            ├─→ Unknown → See material_card_specifications.md library priority
            └─→ Known → Specify nnX extension (e.g., .80c)
                 ↓
            Thermal neutrons (<1 eV)?
                 ├─→ Yes, contains H/Be/C/O/D/Zr → Add MT card (S(α,β))
                 │    └─→ See thermal_scattering_reference.md
                 └─→ No → Skip MT card
                      ↓
                 Temperature ≠ 293.6 K?
                      ├─→ Yes → Add TMP card (T[MeV] = T[K] × 8.617×10⁻¹¹)
                      └─→ No → Use default temperature
                           ↓
                      Validate with mcnp-input-validator skill
```

## Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| **M card** | Material composition | `M1  92235.80c 0.05  92238.80c 0.95  8016.80c 2.0` |
| **Density** | In g/cm³ (negative) or atoms/barn-cm (positive) | `1  1  -10.4  -1  IMP:N=1` (cell card) |
| **ZAID format** | ZZZAAA.nnX (Z=atomic #, A=mass #, nn=library, X=type) | `92235.80c` (U-235, ENDF/B-VIII.0, continuous-energy) |
| **Atomic fractions** | Positive values, number ratios | `1001.80c 2  8016.80c 1` (H₂O: 2 H per 1 O) |
| **Weight fractions** | Negative values, must sum to -1.0 | `26000.80c -0.70  24000.80c -0.30` (70% Fe, 30% Cr) |
| **MT card** | S(α,β) thermal scattering | `MT1  H-H2O.40t` (water at 293.6 K) |
| **TMP card** | Temperature in MeV | `TMP1  6.89e-8` (800 K) |
| **M0 card** | Default libraries for all materials | `M0  NLIB=80c  PLIB=84p` |
| **MX card** | Substitute nuclides | `MX1:N  92235.80c  1.0` |

**Temperature conversion:** T[MeV] = T[K] × 8.617×10⁻¹¹

**Library loading priority:** MX card > M card full table > M card xLIB keyword > M0 card xLIB

## Use Cases

### Use Case 1: Light Water at Room Temperature

**Scenario:** Define light water (H₂O) for PWR moderator/coolant at 293.6 K.

**Goal:** Create material with proper hydrogen treatment for thermal neutrons.

**Implementation:**
```
c ========================================================================
c Material 1: Light Water at 293.6 K
c Density: 1.0 g/cm3
c S(alpha,beta) thermal scattering for hydrogen
c ========================================================================
M1   1001.80c  2  8016.80c  1
MT1  H-H2O.40t
```

**Key Points:**
- Atomic fractions (positive): 2 hydrogen atoms per 1 oxygen
- MT card essential for accurate thermal neutron scattering (<1 eV)
- `.40t` specifies 293.6 K temperature table (see thermal_scattering_reference.md for other temperatures)
- Density specified in cell card, not material card: `1  1  -1.0  ...`

**Expected Results:** Proper thermalization of neutrons, accurate moderation

### Use Case 2: UO₂ Fuel at 4.5% Enrichment

**Scenario:** Define uranium dioxide fuel pellet, 4.5% enriched in U-235, at 900 K centerline temperature.

**Goal:** Specify enrichment and temperature for fuel physics.

**Implementation:**
```
c ========================================================================
c Material 2: UO2 Fuel (4.5% enriched) at 900 K
c Density: 10.4 g/cm3 (95% theoretical density)
c ========================================================================
M2   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
TMP2  7.75e-8
```

**Key Points:**
- Atomic fractions: 4.5% U-235, 95.5% U-238, 2 oxygen per uranium
- TMP card for elevated temperature: 900 K = 7.75×10⁻⁸ MeV
- No MT card needed (no thermal scattering treatment for heavy metals)
- For Doppler broadening: Add DBRC card for U-238 (see mcnp-physics-builder)

**Expected Results:** Correct fission rates, temperature feedback

### Use Case 3: Stainless Steel 304 (Weight Fractions)

**Scenario:** Define SS-304 structural material (Fe 70%, Cr 19%, Ni 10%, Mn 1% by weight).

**Goal:** Use weight fractions for alloy composition.

**Implementation:**
```
c ========================================================================
c Material 3: Stainless Steel 304
c Density: 8.0 g/cm3
c Composition by weight: Fe 70%, Cr 19%, Ni 10%, Mn 1%
c ========================================================================
M3   26000.80c  -0.70  24000.80c  -0.19  28000.80c  -0.10  &
     25055.80c  -0.01
```

**Key Points:**
- Negative fractions = weight fractions (must sum to -1.0)
- Natural element ZAIDs (ZZZ000) when isotopic composition doesn't matter
- Line continuation with `&` for readability
- No MT card (metallic solid, no special thermal treatment)

**Expected Results:** Accurate neutron absorption and scattering for structural calculations

### Use Case 4: Concrete Shielding

**Scenario:** Define ordinary concrete for biological shielding.

**Goal:** Multi-element material with proper hydrogen content for neutron moderation.

**Implementation:**
```
c ========================================================================
c Material 4: Ordinary Concrete
c Density: 2.3 g/cm3
c Composition: H 1%, C 0.1%, O 52.9%, Na 1.6%, Mg 0.2%, Al 3.4%,
c              Si 33.7%, K 1.3%, Ca 4.4%, Fe 1.4%
c ========================================================================
M4   1001.80c  -0.01  6000.80c  -0.001  8016.80c  -0.529  &
     11023.80c  -0.016  12000.80c  -0.002  13027.80c  -0.034  &
     14000.80c  -0.337  19000.80c  -0.013  20000.80c  -0.044  &
     26000.80c  -0.014
```

**Key Points:**
- Weight fractions for complex mixture (sums to -1.0)
- Consider adding MT card for hydrogen if thermal neutrons important
- Multiple lines with continuation for clarity
- See ""example_materials/04_shielding_materials.txt for variations

**Expected Results:** Accurate gamma and neutron attenuation for dose calculations

### Use Case 5: Graphite Moderator/Reflector (CRITICAL FOR THERMAL REACTORS)

**Scenario:** Define graphite for HTGR moderator, reflector, or TRISO coating layers.

**Goal:** Proper thermal neutron scattering with temperature-appropriate S(α,β) library.

**Implementation:**
```
c ========================================================================
c Material 5: Graphite at 600 K (operating temperature)
c Density: 1.75 g/cm3
c Natural carbon isotopic composition
c S(alpha,beta) thermal scattering REQUIRED
c ========================================================================
M5   6012.00c  0.9890  6013.00c  0.0110
MT5  C-GRPH.43t
TMP5  5.17e-8
```

**Key Points:**
- MT card is MANDATORY for graphite in thermal reactors
- Match MT temperature to TMP: 600 K → grph.43t (see thermal_scattering_reference.md)
- Impact of missing MT: 1000-5000 pcm reactivity error, wrong spectrum
- C-12 and C-13 natural abundances (98.90% and 1.10%)
- Temperature selection critical: grph.40t (293K) vs grph.43t (600K) vs grph.46t (1000K)

**Expected Results:** Correct thermal neutron thermalization, accurate reactivity

**CRITICAL WARNING:** Professional reactor models have been found with MISSING graphite MT cards.
This causes significant physics errors. ALWAYS include MT card for graphite!

### Use Case 6: UCO TRISO Fuel Kernel (Advanced)

**Scenario:** Define uranium carbide-oxide (UCO) fuel kernel for TRISO particles in HTGR.

**Goal:** Specify UCO stoichiometry with 19.75% U-235 enrichment.

**Implementation:**
```
c ========================================================================
c Material 6: UCO Kernel (UC0.32O1.36) at 19.75% enrichment
c Density: 10.924 g/cm3
c Stoichiometric ratios (MCNP normalizes internally)
c ========================================================================
M6   92234.00c  3.34179E-03  $ U-234
     92235.00c  1.99636E-01  $ U-235 (19.75% enriched)
     92236.00c  1.93132E-04  $ U-236
     92238.00c  7.96829E-01  $ U-238
      6012.00c  0.3217217    $ C-12
      6013.00c  0.0035783    $ C-13
      8016.00c  1.3613       $ O-16 (>1.0 is valid!)
TMP6  7.75e-8
```

**Key Points:**
- Oxygen fraction >1.0 is VALID - represents stoichiometric ratio UC₀.₃₂O₁.₃₆
- MCNP normalizes using cell density: cell card has `-10.924` (g/cm³)
- Enrichment in U-235: 19.75% typical for TRISO fuel
- Temperature: 900K typical centerline, adjust for your application
- See triso_fuel_reference.md for complete 5-layer TRISO structure

**Expected Results:** Correct UCO fuel physics, proper fission rates

**For more fuel types:** See fuel_compositions_reference.md (UO₂, MOX, UCO, metallic, HALEU)

### Use Case 7: Depleted Fuel with Burnup Tracking (Advanced)

**Scenario:** Define depleted fuel composition after burnup with fission products and Pu buildup.

**Goal:** Track important isotopes for accurate reactivity and spectrum.

**Implementation:**
```
c ========================================================================
c Material 7: Depleted UO2 Fuel (after ~30 GWd/MTU burnup)
c Density: 10.2 g/cm3
c Tracks actinides and key fission products
c ========================================================================
M7   92235.70c  0.010    $ U-235 (depleted from ~4.5%)
     92238.70c  0.945    $ U-238 (slightly depleted)
      8016.70c  2.0      $ O-16
     94239.70c  0.005    $ Pu-239 (bred from U-238)
     94240.70c  0.002    $ Pu-240 (bred from Pu-239)
     94241.70c  0.001    $ Pu-241 (bred from Pu-240)
     54135.70c  1.0e-8   $ Xe-135 (strong absorber, equilibrium)
     62149.70c  5.0e-9   $ Sm-149 (strongest FP absorber)
     64157.70c  1.0e-10  $ Gd-157 (ultra-strong absorber)
TMP7  8.62e-8
```

**Key Points:**
- Track actinide buildup: Pu-239/240/241 from U-238 capture
- Track strong absorbers: Xe-135, Sm-149, Gd-157 (huge impact on reactivity)
- See burnup_tracking_guide.md for complete isotope list (25+ isotopes typical)
- Fission product concentrations from depletion calculation (ORIGEN, MONTEBURNS)
- Depleted U-235: dropped from ~4.5% to ~1.0% after burnup

**Expected Results:** Accurate depleted fuel reactivity, poison effects

**For burnup setup:** See burnup_tracking_guide.md for which isotopes to track and why

## Common Errors and Solutions

### Error 1: Cross Section Not Found

**MCNP Output:** `fatal error. nuclide zaid.nnx not available on any cross-section table`

**Cause:** ZAID not in xsdir file for specified library.

**Solution:**
1. Check xsdir file: `grep "92235" $DATAPATH/xsdir`
2. Use available library (e.g., `.80c`, `.70c`, `.31c`)
3. See material_error_catalog.md for full troubleshooting guide

### Error 2: Weight Fractions Don't Sum to -1.0

**MCNP Output:** `warning. material X sum of fractions = Y`

**Cause:** Weight fractions (negative values) must sum exactly to -1.0.

**Solution:**
1. Check sum: `-0.70 + -0.19 + -0.10 + -0.01 = -1.0` ✓
2. Use scripts/material_density_calculator.py for normalization
3. Adjust fractions: adjust largest component to balance

### Error 3: Missing S(α,β) Treatment

**Symptom:** Inaccurate k-eff or thermal flux for hydrogenous systems.

**Cause:** Missing MT card for water, polyethylene, graphite, etc.

**Solution:**
1. Identify materials with H, Be, C, O, D, Zr in thermal spectrum
2. Add MT card: `MT1  H-H2O.40t` for water
3. See thermal_scattering_reference.md for complete table listing

### Error 4: Missing Graphite Thermal Scattering (CRITICAL)

**Symptom:** k-eff 1000-5000 pcm lower than expected, thermal flux distribution incorrect

**Cause:** Missing MT card for graphite in thermal reactor

**WRONG:**
```
M1   6012.00c  0.9890  6013.00c  0.0110  $ Graphite - NO MT CARD!
```

**RIGHT:**
```
M1   6012.00c  0.9890  6013.00c  0.0110
MT1  C-GRPH.43t  $ <- ESSENTIAL for thermal reactors!
TMP1  5.17e-8    $ Match temperature (600K)
```

**Impact:** This is a CRITICAL ERROR found even in professional reactor models.
Missing graphite S(α,β) causes:
- Free-gas scattering instead of crystalline binding
- Harder thermal spectrum
- Wrong reactivity (typically 1000-5000 pcm error)
- Invalid benchmark comparisons

**Solution:**
1. ALWAYS add MT card for graphite in thermal systems
2. Match MT table temperature to TMP card temperature
3. Use temperature-appropriate table: grph.40t (293K), grph.43t (600K), grph.46t (1000K)
4. See thermal_scattering_reference.md for complete table listing
5. Use scripts/thermal_scattering_checker.py to validate

**For full list of materials requiring MT cards:** See thermal_scattering_reference.md

**For full error catalog:** See material_error_catalog.md (10 errors with diagnosis/fixes)

## Integration with Other Skills

**Typical Workflow:**
1. **mcnp-input-builder** → Create basic input structure
2. **mcnp-geometry-builder** → Define cells requiring materials
3. **mcnp-material-builder** (THIS SKILL) → Define materials for cells
4. **mcnp-source-builder** → Define particle source
5. **mcnp-physics-builder** → Set temperature (TMP), physics options
6. **mcnp-input-validator** → Validate material definitions

**Complementary Skills:**
- **mcnp-isotope-lookup**: Find ZAID formats, atomic masses, abundances
- **mcnp-cross-section-manager**: Check xsdir availability, manage libraries
- **mcnp-physical-constants**: Look up densities, conversion factors
- **mcnp-unit-converter**: Convert between density units, temperature units

**Example Complete Workflow:**
```
Project Goal: PWR pin cell model

Step 1: mcnp-input-builder - Create three-block structure
Step 2: mcnp-geometry-builder - Define fuel, clad, coolant cells
Step 3: mcnp-material-builder - Define UO₂, Zircaloy, water materials
Step 4: mcnp-source-builder - Set up fission source or KCODE
Step 5: mcnp-tally-builder - Define flux, fission rate tallies
Step 6: mcnp-physics-builder - Set temperature, energy cutoffs
Step 7: mcnp-input-validator - Check all cross-references
Result: Validated PWR pin cell input ready for simulation
```

## References

**Detailed Information:**
- Material card keywords (GAS, ESTEP, HSTEP, COND, REFI/REFC/REFS): `material_card_specifications.md`
- All xLIB keywords (NLIB, PLIB, PNLIB, ELIB, HLIB, ALIB, SLIB, TLIB, DLIB): `material_card_specifications.md`
- M0 card specification and examples: `material_card_specifications.md`
- Library loading priority hierarchy: `material_card_specifications.md`
- Complete S(α,β) table listing (40+ tables): `thermal_scattering_reference.md`
- MT0 card for stochastic mixing: `thermal_scattering_reference.md`
- Temperature-dependent S(α,β) selection: `thermal_scattering_reference.md`
- OTFDB, NONU, AWTAB, XS, DRXS cards: `advanced_material_cards.md`
- Material error troubleshooting (10 errors): `material_error_catalog.md`

**Templates and Examples:**
- Water materials (H₂O, D₂O, hot water): `templates/water_materials_template.i`
- Fuel materials (UO₂, MOX, various enrichments): `templates/fuel_materials_template.i`
- Structural materials (steel, Zircaloy, concrete): `templates/structural_materials_template.i`
- Moderator materials (graphite, polyethylene, beryllium): `templates/moderator_materials_template.i`
- Template usage guide: `templates/README.md`
- PWR core materials: `example_materials/01_pwr_core_materials.txt`
- HTGR TRISO materials: `example_materials/02_htgr_materials.txt`
- Fast reactor materials: `example_materials/03_fast_reactor_materials.txt`
- Shielding materials: `example_materials/04_shielding_materials.txt`
- Research reactor materials: `example_materials/05_research_reactor_materials.txt`
- Criticality safety materials: `example_materials/06_criticality_safety_materials.txt`

**Automation Tools:**
- Material density calculator: `scripts/material_density_calculator.py`
- ZAID library validator: `scripts/zaid_library_validator.py`
- Usage documentation: `scripts/README.md`

**External Documentation:**
- MCNP6 Manual Chapter 5.06: Material Data Cards
- MCNP6 Manual Section 1.2.2: Target Identifier Formats

## Best Practices

1. **Always verify ZAID availability** in xsdir before using non-standard libraries (use scripts/zaid_library_validator.py)
2. **Use consistent library versions** across all materials in an input (avoid mixing .80c with .70c)
3. **Add MT cards for thermal systems** whenever materials contain H, Be, C, O, D, or Zr and neutrons are thermal (<1 eV)
4. **Match TMP and MT temperatures** - ensure S(α,β) table temperature matches TMP card temperature
5. **Use atomic fractions for compounds** (H₂O, UO₂) and weight fractions for alloys (stainless steel)
6. **Normalize weight fractions** to sum exactly to -1.0 (use scripts/material_density_calculator.py)
7. **Document material sources** in comments (handbook values, measurements, compositions)
8. **Use M0 card** to set default libraries for all materials in large inputs (reduces card clutter)
9. **Check natural vs isotopic** - use natural element ZAIDs (ZZZ000) when isotopic detail doesn't matter
10. **Test materials separately** in simple geometries before using in complex models
11. **ALWAYS add MT cards for graphite** in thermal reactors (HTGR, RBMK, graphite-moderated) - even professional models have missed this critical requirement
12. **Match MT table temperature to operating conditions** - grph.40t (cold), grph.43t (operating), grph.46t (high-temp)
13. **Track fission products in burnup** - minimum Xe-135, Sm-149, Gd-157 for accurate depletion (see burnup_tracking_guide.md)
