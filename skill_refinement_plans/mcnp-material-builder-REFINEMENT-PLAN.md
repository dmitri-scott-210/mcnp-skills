# mcnp-material-builder SKILL REFINEMENT PLAN
## Focused Plan for Material Card Excellence

**Created**: November 8, 2025
**Based On**: AGR-1 Material Card Analysis (385 materials, 46 KB analysis document)
**Priority**: 🔴 **CRITICAL** - Missing thermal scattering causes 1000s pcm reactivity errors
**Execution Time**: 2-3 hours for HIGH priority items

---

## EXECUTIVE SUMMARY

Analysis of professional reactor models (AGR-1, HTGR) revealed **CRITICAL gaps** in mcnp-material-builder skill:

### Current State (GOOD)
✅ Basic MT cards covered with comprehensive temperature tables
✅ Weight vs atomic fractions explained
✅ Simple fuel examples (UO₂)
✅ Stainless steel, concrete examples

### Critical Gaps (MUST FIX)
❌ **Missing graphite MT card examples** - Found in 50+ materials in AGR-1, ZERO had MT cards!
❌ **No comprehensive fuel composition reference** - Only UO₂, missing UCO, MOX, metallic, HALEU
❌ **No burnup tracking guidance** - Which isotopes to track, how to set up
❌ **No ZAID selection decision tree** - When .70c vs .00c vs .80c, isotopic vs natural
❌ **Temperature-dependent library selection unclear** - grph.10t vs grph.18t vs grph.24t

### Impact
- **Reactivity errors**: 1000-5000 pcm from missing graphite S(α,β)
- **Invalid benchmarks**: Cannot reproduce published results without proper MT cards
- **User confusion**: "Why isn't my model matching the reference?"
- **TRISO fuel gaps**: UCO composition pattern not documented

---

## FINDINGS FROM AGR-1 ANALYSIS

### Finding 1: CRITICAL Thermal Scattering Omission

**From AGR1_Material_Card_Analysis.md**:

```
## 5.4 Graphite Thermal Scattering - CRITICAL OMISSION

**Expected library:** grph.10t (graphite thermal scattering)

**Observed:** NONE in any of the three files.

**Materials affected:**
- m9040-m9056: Pure graphite spacers
- m9070-m9075: Borated graphite holders
- m9090-m9094: TRISO coating layers (Buffer, IPyC, SiC, OPyC, Matrix)

**Impact:**
- **Low-energy neutron transport:** Free gas scattering model used instead
- **Reactivity:** Underestimation of thermal neutron scattering cross-sections
- **Spectrum:** Harder thermal spectrum than physical reality
```

**CRITICAL**: Professional models are **missing required MT cards**. Skill MUST teach this explicitly.

### Finding 2: UCO Fuel Composition Pattern

**From analysis** (lines 189-212):

```mcnp
c kernel, UCO: density=10.924 g/cm3
m9111
   92234.00c  3.34179E-03  $ U-234
   92235.00c  1.99636E-01  $ U-235 (19.96% enrichment)
   92236.00c  1.93132E-04  $ U-236
   92238.00c  7.96829E-01  $ U-238
    6012.00c  0.3217217    $ C-12
    6013.00c  0.0035783    $ C-13
    8016.00c  1.3613       $ O-16 ← EXCEEDS 1.0!
```

**Chemical formula**: UC₀.₃₂O₁.₃₆ (uranium carbide-oxide)
**Key pattern**: Stoichiometric ratios >1.0 are valid - MCNP normalizes

### Finding 3: ZAID Library Selection Patterns

**From analysis** (lines 78-109):

Primary libraries in AGR-1 model:
- **.70c** (ENDF/B-VII.0): H, O, C, Al, actinides, fission products
- **.60c** (ENDF/B-VI.8): Natural Mg, Si, Ti, Zr, Mo
- **.50c** (ENDF/B-V): Natural Cr, Fe, Ni
- **.00c** (ENDF/B-VI.0): AGR graphite, helium, SS316L
- **.20c** (Special): B-10 optimized
- **.80c** (ENDF/B-VIII.0): Air constituents

**NO explanation exists for WHY these choices were made!**

### Finding 4: Burnup Tracking Material Pattern

**From analysis** (lines 234-237, 919-932):

ATR fuel materials track:
- **Actinides**: U-234/235/236/237/238, Np-237, Pu-239/240/241
- **Strong absorbers**: Sm-149 (40,000 barn), Gd-157 (254,000 barn)
- **Stable FPs**: Kr-83, Xe-131/133, Cs-133, Nd-143/145, etc.
- **~25 fission product isotopes per material**

Pattern: Depleted fuel has unique composition for each zone (210 materials for 10 elements × 3 radial × 7 axial)

### Finding 5: Temperature-Dependent Libraries Critical

**From analysis recommendations** (lines 1183-1209):

```mcnp
**HIGH PRIORITY:**
1. **Add graphite thermal scattering:**
   mt9040  grph.10t   $ or grph.18t for 600K
   mt9090  grph.10t   $ Buffer
   mt9091  grph.10t   $ IPyC
   mt9093  grph.10t   $ OPyC
   mt9094  grph.10t   $ Matrix

2. **Use temperature-appropriate S(α,β):**
   - Water: lwtr.11t (325K) or lwtr.13t (350K) instead of lwtr.10t (294K)
   - Graphite: grph.18t (600K) or grph.24t (1200K) for high-temp regions
```

**Current skill does NOT emphasize temperature matching strongly enough.**

---

## REFINEMENT STRATEGY

### Phase 1: CRITICAL Fixes (Session 1 - HIGH PRIORITY)

**Fix the most impactful gaps that prevent correct reactor modeling**

1. **Add graphite MT card examples to SKILL.md** (CRITICAL)
2. **Create comprehensive fuel_compositions_reference.md** (all fuel types)
3. **Create ZAID_selection_guide.md** (decision tree)
4. **Create burnup_tracking_guide.md** (which isotopes, why)
5. **Enhance thermal_scattering_reference.md** (temperature emphasis)
6. **Create thermal_scattering_checker.py** (validation tool)
7. **Create triso_fuel_reference.md** (supplemental, not main focus)

### Phase 2: Enhancements (Session 2 - MEDIUM PRIORITY)

8. Update example_materials with complete coverage
9. Add enrichment calculator tool
10. Add isotopic fraction calculator

### Phase 3: Advanced (Session 3 - LOW PRIORITY)

11. Integration examples with burnup codes
12. Advanced ZAID library troubleshooting

---

# PHASE 1: CRITICAL FIXES (DETAILED)

## 1. Update SKILL.md - Add Graphite Examples

**File**: `.claude/skills/mcnp-material-builder/SKILL.md`

**Issue**: No graphite examples despite being CRITICAL for HTGRs, RBMKs, graphite-moderated reactors

**ADD new section after line 177** (after Use Case 4: Concrete Shielding):

```markdown
### Use Case 5: Graphite Moderator/Reflector (CRITICAL FOR THERMAL REACTORS)

**Scenario:** Define graphite for HTGR moderator, reflector, or TRISO coating layers.

**Goal:** Proper thermal neutron scattering with temperature-appropriate S(α,β) library.

**Implementation:**
```mcnp
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
- ✅ **MT card is MANDATORY** for graphite in thermal reactors
- ✅ Match MT temperature to TMP: 600 K → grph.43t (see thermal_scattering_reference.md)
- ✅ Impact of missing MT: 1000-5000 pcm reactivity error, wrong spectrum
- ✅ C-12 and C-13 natural abundances (98.90% and 1.10%)
- ✅ Temperature selection critical: grph.40t (293K) vs grph.43t (600K) vs grph.46t (1000K)

**Expected Results:** Correct thermal neutron thermalization, accurate reactivity

**CRITICAL WARNING:** Professional reactor models have been found with MISSING graphite MT cards.
This causes significant physics errors. ALWAYS include MT card for graphite!

### Use Case 6: UCO TRISO Fuel Kernel (Advanced)

**Scenario:** Define uranium carbide-oxide (UCO) fuel kernel for TRISO particles in HTGR.

**Goal:** Specify UCO stoichiometry with 19.75% U-235 enrichment.

**Implementation:**
```mcnp
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
- ✅ Oxygen fraction >1.0 is VALID - represents stoichiometric ratio UC₀.₃₂O₁.₃₆
- ✅ MCNP normalizes using cell density: cell card has `-10.924` (g/cm³)
- ✅ Enrichment in U-235: 19.75% typical for TRISO fuel
- ✅ Temperature: 900K typical centerline, adjust for your application
- ✅ See triso_fuel_reference.md for complete 5-layer TRISO structure

**Expected Results:** Correct UCO fuel physics, proper fission rates

**For more fuel types:** See fuel_compositions_reference.md (UO₂, MOX, UCO, metallic, HALEU)

### Use Case 7: Depleted Fuel with Burnup Tracking (Advanced)

**Scenario:** Define depleted fuel composition after burnup with fission products and Pu buildup.

**Goal:** Track important isotopes for accurate reactivity and spectrum.

**Implementation:**
```mcnp
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
- ✅ Track actinide buildup: Pu-239/240/241 from U-238 capture
- ✅ Track strong absorbers: Xe-135, Sm-149, Gd-157 (huge impact on reactivity)
- ✅ See burnup_tracking_guide.md for complete isotope list (25+ isotopes typical)
- ✅ Fission product concentrations from depletion calculation (ORIGEN, MONTEBURNS)
- ✅ Depleted U-235: dropped from ~4.5% to ~1.0% after burnup

**Expected Results:** Accurate depleted fuel reactivity, poison effects

**For burnup setup:** See burnup_tracking_guide.md for which isotopes to track and why
```

**ADD to Common Errors section** (after Error 3, around line 213):

```markdown
### Error 4: Missing Graphite Thermal Scattering (CRITICAL)

**Symptom:** k-eff 1000-5000 pcm lower than expected, thermal flux distribution incorrect

**Cause:** Missing MT card for graphite in thermal reactor

**WRONG:**
```mcnp
M1   6012.00c  0.9890  6013.00c  0.0110  $ Graphite - NO MT CARD!
```

**RIGHT:**
```mcnp
M1   6012.00c  0.9890  6013.00c  0.0110
MT1  C-GRPH.43t  $ ← ESSENTIAL for thermal reactors!
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
```

**ADD to Best Practices section** (around line 282):

```markdown
11. **ALWAYS add MT cards for graphite** in thermal reactors (HTGR, RBMK, graphite-moderated) - even professional models have missed this critical requirement
12. **Match MT table temperature to operating conditions** - grph.40t (cold), grph.43t (operating), grph.46t (high-temp)
13. **Track fission products in burnup** - minimum Xe-135, Sm-149, Gd-157 for accurate depletion (see burnup_tracking_guide.md)
```

**Validation**: User asks "How do I model graphite in an HTGR?"
**Expected**: Skill provides complete example with MT card, temperature matching, emphasis on critical requirement

---

## 2. Create fuel_compositions_reference.md

**File**: `.claude/skills/mcnp-material-builder/fuel_compositions_reference.md`

**Purpose**: Comprehensive reference for ALL reactor fuel types (not just UO₂)

**Content**:

```markdown
# Comprehensive Fuel Compositions Reference
## Material Specifications for All Reactor Fuel Types

**Purpose**: Complete reference for fuel material cards across all reactor types.
**Scope**: UO₂, MOX, UCO, metallic, HALEU, various enrichments

---

## 1. LIGHT WATER REACTOR FUELS

### 1.1 UO₂ Fuel (Standard PWR/BWR)

#### UO₂ at 3.5% Enrichment
```mcnp
c UO2 fuel, 3.5% enriched, 10.5 g/cm3 (95% theoretical density)
M1   92235.80c  0.035    $ U-235 (enrichment)
     92238.80c  0.965    $ U-238
      8016.80c  2.0      $ O-16 (stoichiometric UO2)
TMP1  8.62e-8             $ 1000 K centerline temperature
```

**Key Data**:
- Theoretical density UO₂: 10.96 g/cm³
- Typical as-fabricated: 10.2-10.5 g/cm³ (93-96% TD)
- Enrichment range: 2-5% typical for LWRs
- Temperature: 600-1200 K typical (fuel centerline hotter than pellet edge)

#### UO₂ at 4.5% Enrichment (Modern PWR)
```mcnp
c UO2 fuel, 4.5% enriched, 10.4 g/cm3
M2   92235.80c  0.045
     92238.80c  0.955
      8016.80c  2.0
TMP2  9.48e-8             $ 1100 K
```

#### UO₂ at 5.0% Enrichment (Extended Burnup)
```mcnp
c UO2 fuel, 5.0% enriched, 10.3 g/cm3
M3   92235.80c  0.050
     92238.80c  0.950
      8016.80c  2.0
TMP3  8.62e-8             $ 1000 K
```

**Usage Notes**:
- Higher enrichment → longer fuel cycles
- U-234 typically neglected for fresh fuel (<0.1%)
- U-236 appears after irradiation (from U-235 n,gamma)
- For burnup tracking, see burnup_tracking_guide.md

### 1.2 MOX Fuel (Mixed Oxide: UO₂ + PuO₂)

#### MOX with 5% Pu Content
```mcnp
c MOX fuel, 5% PuO2 in UO2, depleted uranium host
c Density: 10.3 g/cm3
c Pu vector: weapons-grade (94% Pu-239)
M4   92235.80c  0.002    $ U-235 (depleted U host)
     92238.80c  0.948    $ U-238 (depleted U host)
     94239.80c  0.047    $ Pu-239 (5% Pu, 94% is Pu-239)
     94240.80c  0.003    $ Pu-240 (6% of Pu)
      8016.80c  2.0      $ O-16
TMP4  9.48e-8             $ 1100 K
```

**Pu Isotopic Vectors**:

| Pu Type | Pu-238 | Pu-239 | Pu-240 | Pu-241 | Pu-242 |
|---------|--------|--------|--------|--------|--------|
| Weapons-grade | <1% | 93-94% | 6% | <1% | <1% |
| Reactor-grade | 1-2% | 55-60% | 24-26% | 10-12% | 3-5% |

#### MOX with Reactor-Grade Pu
```mcnp
c MOX fuel, 7% PuO2, reactor-grade Pu vector
c Density: 10.2 g/cm3
M5   92235.80c  0.002    $ U-235
     92238.80c  0.928    $ U-238
     94238.80c  0.0014   $ Pu-238 (2% of Pu)
     94239.80c  0.0399   $ Pu-239 (57% of Pu)
     94240.80c  0.0175   $ Pu-240 (25% of Pu)
     94241.80c  0.0077   $ Pu-241 (11% of Pu)
     94242.80c  0.0035   $ Pu-242 (5% of Pu)
      8016.80c  2.0      $ O-16
TMP5  9.48e-8
```

**Usage Notes**:
- MOX used for Pu disposition and fuel cycle closure
- Harder neutron spectrum than UO₂
- Higher Pu-240 → higher neutron source from spontaneous fission
- Reactor-grade Pu typical from reprocessed LWR fuel

---

## 2. HIGH-TEMPERATURE GAS-COOLED REACTOR FUELS

### 2.1 UCO Fuel (Uranium Carbide-Oxide for TRISO)

#### UCO at 19.75% Enrichment (HTGR Standard)
```mcnp
c UCO kernel: UC0.32O1.36, 19.75% enriched
c Density: 10.924 g/cm3
c Stoichiometric ratios (values >1.0 valid, MCNP normalizes)
M10   92234.00c  3.34179E-03  $ U-234 (0.334%)
      92235.00c  1.99636E-01  $ U-235 (19.75% enrichment)
      92236.00c  1.93132E-04  $ U-236 (trace contamination)
      92238.00c  7.96829E-01  $ U-238 (balance)
       6012.00c  0.3217217    $ C-12 (carbide component)
       6013.00c  0.0035783    $ C-13 (natural C-13)
       8016.00c  1.3613       $ O-16 (oxide component, >1.0 OK!)
TMP10  7.75e-8                $ 900 K kernel temperature
```

**Chemical Formula**: UC₀.₃₂O₁.₃₆

**Key Points**:
- Oxygen fraction >1.0 is VALID - stoichiometric ratio not atom fraction
- MCNP normalizes using cell card density: `-10.924` g/cm³
- UCO preferred over UO₂ in TRISO for reduced CO production
- C/O ratio optimized to minimize pressure in particle

**TRISO Coating Layers** (see triso_fuel_reference.md for complete 5-layer structure):
```mcnp
c Buffer: Porous carbon, 1.10 g/cm3
M11   6012.00c  0.9890  6013.00c  0.0110
c NOTE: Buffer should have MT card for accurate physics
MT11  C-GRPH.43t          $ 600 K graphite S(alpha,beta)

c IPyC: Dense pyrolytic carbon, 1.912 g/cm3
M12   6012.00c  0.9890  6013.00c  0.0110
MT12  C-GRPH.43t

c SiC: Silicon carbide, 3.207 g/cm3
M13  14028.00c  0.9223   $ Si-28 (92.23%)
     14029.00c  0.0467   $ Si-29 (4.67%)
     14030.00c  0.0310   $ Si-30 (3.10%)
      6012.00c  0.9890   $ C-12
      6013.00c  0.0110   $ C-13
c NOTE: SiC should ideally have MT for carbon component
MT13  C-GRPH.43t

c OPyC: Dense pyrolytic carbon, 1.901 g/cm3
M14   6012.00c  0.9890  6013.00c  0.0110
MT14  C-GRPH.43t

c Matrix: Graphite binder, 1.256 g/cm3
M15   6012.00c  0.9890  6013.00c  0.0110
MT15  C-GRPH.43t
```

**CRITICAL**: All carbon-containing TRISO layers REQUIRE MT cards in thermal systems!

#### UO₂ TRISO Kernel (Alternative)
```mcnp
c UO2 kernel for TRISO, 19.75% enriched
c Density: 10.8 g/cm3
M20   92235.80c  0.1975   $ U-235
      92238.80c  0.8025   $ U-238
       8016.80c  2.0      $ O-16
TMP20  7.75e-8
```

---

## 3. FAST REACTOR FUELS

### 3.1 Metallic Fuel (U-Zr Alloy)

#### U-10Zr (10 wt% Zr)
```mcnp
c U-10Zr metallic fuel, 19.75% enriched
c Density: 15.8 g/cm3
c Weight fractions (negative values)
M30   92235.80c  -0.1778  $ U-235 (19.75% of U, 90% U in alloy)
      92238.80c  -0.7222  $ U-238 (80.25% of U, 90% U in alloy)
      40000.60c  -0.1000  $ Zr-nat (10 wt%)
TMP30  7.75e-8             $ 900 K
```

**Key Data**:
- High density → compact core
- Better thermal conductivity than oxide
- Used in EBR-II, some Gen-IV fast reactors
- Zr content: 6-10% typical
- Low melting point (~1400 K) requires careful thermal design

#### U-Pu-Zr (Ternary Alloy)
```mcnp
c U-20Pu-10Zr metallic fuel for fast reactor
c Density: 15.5 g/cm3
c Composition: 70% U, 20% Pu, 10% Zr by weight
M31   92235.80c  -0.014   $ U-235 (2% enriched, 70% U)
      92238.80c  -0.686   $ U-238 (98% of U, 70% U)
      94239.80c  -0.120   $ Pu-239 (60% of Pu, 20% Pu)
      94240.80c  -0.050   $ Pu-240 (25% of Pu, 20% Pu)
      94241.80c  -0.022   $ Pu-241 (11% of Pu, 20% Pu)
      94242.80c  -0.008   $ Pu-242 (4% of Pu, 20% Pu)
      40000.60c  -0.100   $ Zr-nat (10 wt%)
TMP31  8.62e-8             $ 1000 K
```

---

## 4. ADVANCED REACTOR FUELS

### 4.1 HALEU (High-Assay Low-Enriched Uranium)

**Definition**: Enrichment between 5% and 20% (>LWR limit, <HEU threshold)

#### HALEU UO₂ at 10% Enrichment
```mcnp
c HALEU UO2, 10% enriched for advanced reactor
c Density: 10.5 g/cm3
M40   92235.80c  0.10     $ U-235 (10% enrichment)
      92238.80c  0.90     $ U-238
       8016.80c  2.0      $ O-16
TMP40  8.62e-8             $ 1000 K
```

**Applications**:
- Microreactors (compact cores)
- Advanced small modular reactors (SMRs)
- Long-life cores (>10 years)

#### HALEU UO₂ at 15% Enrichment
```mcnp
c HALEU UO2, 15% enriched
c Density: 10.4 g/cm3
M41   92235.80c  0.15
      92238.80c  0.85
       8016.80c  2.0
TMP41  9.48e-8             $ 1100 K
```

#### HALEU UO₂ at 19.75% Enrichment (Maximum HALEU)
```mcnp
c HALEU UO2, 19.75% enriched (max HALEU, <20% limit)
c Density: 10.3 g/cm3
M42   92235.80c  0.1975
      92238.80c  0.8025
       8016.80c  2.0
TMP42  8.62e-8
```

**Regulatory Note**: >20% is HEU (highly enriched), export-controlled

### 4.2 Ceramic-Metallic Composite (Cermet)

#### UO₂-Mo Cermet (Research Reactor Fuel)
```mcnp
c UO2-Mo cermet, 19.75% enriched
c 60% UO2, 40% Mo by volume
c Effective density: 9.5 g/cm3
c WEIGHT fractions calculated from volume fractions
M50   92235.80c  -0.0658  $ U-235
      92238.80c  -0.2672  $ U-238
       8016.80c  -0.0357  $ O-16 (from UO2)
      42000.60c  -0.6313  $ Mo-nat (40% by volume)
TMP50  4.31e-8             $ 500 K
```

**Applications**: Research reactors, high-flux systems

---

## 5. RESEARCH REACTOR FUELS

### 5.1 Aluminum-Dispersion Fuel (MTR-Type)

#### U-Al Fuel Meat (HEU)
```mcnp
c U-Al dispersion, 93% enriched (HEU - being phased out)
c UAl3 dispersed in Al matrix
c Density: 3.5 g/cm3
M60   92235.80c  -0.186   $ U-235 (93% enriched, 20 wt% U)
      92238.80c  -0.014   $ U-238 (7% of U)
      13027.80c  -0.800   $ Al-27 (80 wt% matrix + cladding)
TMP60  3.45e-8             $ 400 K
```

#### U-Al Fuel Meat (LEU Conversion)
```mcnp
c U-Al dispersion, 19.75% enriched (LEU converted from HEU)
c Higher U loading (45 wt%) to maintain reactivity
c Density: 4.8 g/cm3
M61   92235.80c  -0.089   $ U-235 (19.75%, 45 wt% U)
      92238.80c  -0.361   $ U-238
      13027.80c  -0.550   $ Al-27 (55 wt%)
TMP61  3.45e-8
```

---

## 6. ISOTOPIC DETAIL: WHEN TO INCLUDE

### 6.1 Fresh Fuel (Beginning of Life)

**Minimum isotopes**:
```mcnp
M100  92235  X.XX    $ U-235 (enrichment)
      92238  X.XX    $ U-238 (balance)
       8016  2.0     $ O-16 (for UO2)
```

**Recommended (higher fidelity)**:
```mcnp
M100  92234  X.XXX   $ U-234 (~0.3-0.5% of total U)
      92235  X.XX    $ U-235 (enrichment)
      92236  X.XXXX  $ U-236 (trace, from reprocessing)
      92238  X.XX    $ U-238 (balance)
       8016  2.0     $ O-16
```

**U-234 fraction calculation**:
- Fresh UO₂: U-234/U-235 ≈ 0.008 (natural ratio)
- Example: 4.5% U-235 → 0.036% U-234
- Usually negligible for k-eff, but include for accuracy

### 6.2 Depleted/Burned Fuel

**Must include** (minimum):
```mcnp
M200  92235  X.XX    $ U-235 (depleted)
      92238  X.XX    $ U-238 (depleted)
      94239  X.XX    $ Pu-239 (bred from U-238)
      94240  X.XX    $ Pu-240 (bred from Pu-239)
      54135  X.XX    $ Xe-135 (equilibrium poison)
      62149  X.XX    $ Sm-149 (equilibrium poison)
       8016  2.0     $ O-16
```

**Recommended** (25+ isotopes for high fidelity):
- See burnup_tracking_guide.md for complete list
- Track all actinides: U-234/235/236/238, Np-237, Pu-239/240/241/242, Am-241, Cm-242/244
- Track strong absorbers: Xe-135, Sm-149, Gd-155/157, Eu-153/155
- Track stable FPs: Nd-143/145, Cs-133, Mo-95, Ru-101

---

## 7. ZAID LIBRARY SELECTION

### 7.1 Library Priority by Fuel Type

**For UO₂, MOX, HALEU (general use)**:
```mcnp
M1   92235.80c  ...  $ ENDF/B-VIII.0 (latest, preferred)
     92238.80c  ...
      8016.80c  ...
```

**Alternative if .80c not available**:
```mcnp
M1   92235.70c  ...  $ ENDF/B-VII.0 (widely available)
     92238.70c  ...
      8016.70c  ...
```

**For HTGR/UCO (specific evaluation)**:
```mcnp
M10  92235.00c  ...  $ ENDF/B-VI.0 (some AGR models use this)
     92238.00c  ...
      6012.00c  ...
      8016.00c  ...
```

**For metallic fuel**:
```mcnp
M30  92235.80c  ...  $ Latest evaluation
     92238.80c  ...
     40000.60c  ...  $ Natural Zr (ENDF/B-VI.8)
```

### 7.2 Decision Tree

```
Fresh fuel, modern library available?
  ├─→ Yes: Use .80c (ENDF/B-VIII.0)
  └─→ No: Use .70c (ENDF/B-VII.0)

Benchmark validation required?
  └─→ Use EXACT library specified in benchmark

Isotopic detail needed?
  ├─→ Actinides: ALWAYS isotopic (92234, 92235, 92236, 92238, 94239, etc.)
  ├─→ Carbon: Isotopic if high accuracy (6012, 6013)
  ├─→ Oxygen: Usually natural (8016 sufficient)
  └─→ Structural (Fe, Cr, Ni): Natural OK (26000, 24000, 28000)
```

**See ZAID_selection_guide.md for complete decision tree**

---

## 8. TEMPERATURE CONSIDERATIONS

### 8.1 Typical Fuel Temperatures by Reactor Type

| Reactor Type | Fuel Temperature (K) | TMP Card (MeV) | Notes |
|--------------|---------------------|----------------|-------|
| PWR centerline | 1000-1200 | 8.62e-8 to 1.03e-7 | Peak in pellet center |
| PWR average | 800-900 | 6.89e-8 to 7.75e-8 | Volume-averaged |
| BWR | 800-1000 | 6.89e-8 to 8.62e-8 | Similar to PWR |
| HTGR (TRISO kernel) | 900-1200 | 7.75e-8 to 1.03e-7 | Normal operation |
| HTGR (accident) | up to 1600 | 1.38e-7 | Maximum design |
| Fast reactor (metallic) | 800-1000 | 6.89e-8 to 8.62e-8 | Better conductivity |
| Research reactor (Al) | 400-500 | 3.45e-8 to 4.31e-8 | Low power density |

**Temperature Conversion**:
```
T [MeV] = T [K] × 8.617×10⁻¹¹

Examples:
293.6 K → 2.53×10⁻⁸ MeV (room temperature)
600 K   → 5.17×10⁻⁸ MeV (HTGR graphite)
1000 K  → 8.62×10⁻⁸ MeV (typical fuel centerline)
1200 K  → 1.03×10⁻⁷ MeV (high-power fuel)
```

---

## 9. VALIDATION CHECKLIST

Before using any fuel material:

- [ ] Enrichment correct for reactor type (2-5% LWR, 19.75% HALEU/HTGR, etc.)
- [ ] Isotopic fractions sum correctly (for atomic fractions)
- [ ] Weight fractions sum to -1.0 (if using negative fractions)
- [ ] Stoichiometry correct (UO₂ has 2 oxygen per uranium)
- [ ] Temperature specified (TMP card matches expected fuel temperature)
- [ ] Library version consistent across materials (.80c or .70c throughout)
- [ ] Graphite MT cards included for HTGR fuels (CRITICAL!)
- [ ] Depletion isotopes included if modeling burnup
- [ ] Cell density matches material card format (negative for g/cm³ with weight fractions)

---

## 10. REFERENCES

**For complete TRISO structure**:
- triso_fuel_reference.md - 5-layer coating details, particle lattices

**For burnup calculations**:
- burnup_tracking_guide.md - Which isotopes to track, why, how many

**For library selection**:
- ZAID_selection_guide.md - Complete decision tree for ZAID extensions

**For thermal scattering**:
- thermal_scattering_reference.md - MT cards, temperature tables

**For density calculations**:
- scripts/material_density_calculator.py - Automated calculations

**External Data Sources**:
- JANIS Nuclear Data Viewer (https://www.oecd-nea.org/janis/)
- KAERI Table of Nuclides (https://atom.kaeri.re.kr/)
- PNNL-15870 Rev.1: Compendium of Material Composition Data

---

**Version:** 1.0
**Created:** 2025-11-08
**For:** mcnp-material-builder skill v2.0
```

**Validation**: User asks "How do I model UCO fuel for TRISO particles?"
**Expected**: Skill provides complete UCO example with stoichiometry explanation, links to triso_fuel_reference.md

---

## 3. Create ZAID_selection_guide.md

**File**: `.claude/skills/mcnp-material-builder/ZAID_selection_guide.md`

**Purpose**: Decision tree for selecting appropriate ZAID library extensions

**Content**:

```markdown
# ZAID Library Selection Guide
## Complete Decision Tree for Cross-Section Library Extensions

**Purpose**: Help users choose the correct .nnX extension for ZAIDs
**Scope**: When to use .80c vs .70c vs .60c vs .00c, isotopic vs natural elements

---

## ZAID FORMAT REVIEW

```
ZZZAAA.nnX

ZZZ:    Atomic number (Z) - 001 to 098
AAA:    Mass number (A) - 000 for natural element, specific for isotope
nn:     Library identifier (00-99)
X:      Particle/physics type (c=continuous-energy neutron, most common)
```

**Examples**:
- `92235.80c` = U-235, ENDF/B-VIII.0, continuous-energy neutrons
- `6000.70c` = Natural carbon, ENDF/B-VII.0, continuous-energy neutrons
- `1001.80c` = H-1, ENDF/B-VIII.0, continuous-energy neutrons

---

## LIBRARY EXTENSIONS (nn)

### Modern Libraries (Preferred)

| Extension | ENDF Version | Status | When to Use |
|-----------|--------------|--------|-------------|
| **.80c** | ENDF/B-VIII.0 | Latest (2018+) | **Preferred** for new models if available |
| **.70c** | ENDF/B-VII.0 | Standard (2006) | **Default** for most applications |
| **.71c** | ENDF/B-VII.1 | Updated (2011) | Alternative to .70c, minor updates |

### Legacy Libraries (Use if Required)

| Extension | ENDF Version | When to Use |
|-----------|--------------|-------------|
| **.60c** | ENDF/B-VI.8 | Natural elements if .70c unavailable |
| **.50c** | ENDF/B-V | Structural materials (legacy models) |
| **.00c** | ENDF/B-VI.0 or earlier | Benchmark reproduction only |

### Special Libraries

| Extension | Purpose | Example Use |
|-----------|---------|-------------|
| **.20c** | B-10 optimized thermal | Burnable poison, control rods |
| **.55c** | W special evaluation | Tungsten shielding |
| **.31c** | JEFF-3.1 European library | European benchmark validation |

---

## DECISION TREE

### Step 1: New Model or Benchmark Validation?

```
Are you reproducing a published benchmark?
  ├─→ YES: Use EXACT library specified in benchmark documentation
  │         Example: AGR-1 benchmark specifies .00c for graphite
  └─→ NO: Continue to Step 2
```

### Step 2: Library Availability

```
Check xsdir for availability:
  grep "92235" $DATAPATH/xsdir

Is .80c available for your isotope?
  ├─→ YES: Use .80c (latest data)
  └─→ NO: Is .70c available?
           ├─→ YES: Use .70c (standard)
           └─→ NO: Use .60c or consult mcnp-cross-section-manager
```

### Step 3: Isotopic vs Natural Element

```
Does isotopic composition matter for physics?
  ├─→ YES (actinides, absorbers, fission products):
  │    Use specific isotope: 92235.80c, 54135.70c, 62149.70c
  │
  └─→ NO (structural materials, low-importance):
       Use natural element: 26000.70c (Fe-nat), 24000.70c (Cr-nat)
```

**When isotopic detail MATTERS**:
- ✅ Actinides (U, Pu, Np, Am, Cm): ALWAYS isotopic
- ✅ Fission products: Individual isotopes (Xe-135, Sm-149, Gd-157)
- ✅ Carbon in HTGR: C-12 and C-13 for accuracy
- ✅ Boron: B-10 and B-11 for control/burnable poison
- ✅ Silicon in SiC: Si-28/29/30 for TRISO coating
- ✅ Lithium: Li-6 and Li-7 for tritium breeding

**When natural element OK**:
- ✅ Structural steel: Fe, Cr, Ni, Mn (unless activation study)
- ✅ Concrete: Ca, Si, Al (bulk composition)
- ✅ Coolant impurities: Trace elements
- ✅ Shielding: Pb, W (unless detailed gamma transport)

### Step 4: Consistency Check

```
All materials using same library version?
  ├─→ YES: Proceed
  └─→ NO: Mix only if necessary (e.g., special B-10 evaluation)
           Document reason in comments
```

---

## LIBRARY SELECTION BY APPLICATION

### 1. Light Water Reactors (PWR/BWR)

**Standard approach**:
```mcnp
c UO2 fuel
M1   92235.80c  0.045    $ ENDF/B-VIII.0 (preferred)
     92238.80c  0.955
      8016.80c  2.0

c Zircaloy clad
M2   40000.70c  1.0      $ Natural Zr, ENDF/B-VII.0 (widely available)

c Water
M3    1001.80c  2        $ H-1, ENDF/B-VIII.0
      8016.80c  1
MT3  H-H2O.40t

c Stainless steel
M4   26000.70c  -0.70    $ Natural elements for structure
     24000.70c  -0.19
     28000.70c  -0.11
```

**Why**:
- Actinides: Latest evaluations (.80c) for best accuracy
- Zr: .70c widely available, .80c if you have it
- Structure: Natural elements sufficient, .70c standard
- Consistency: Mostly .80c, acceptable to mix .70c for unavailable isotopes

### 2. High-Temperature Gas Reactors (HTGR)

**Observed in AGR-1 benchmark**:
```mcnp
c UCO fuel kernel
M10  92235.00c  0.1996   $ ENDF/B-VI.0 (benchmark specified .00c)
     92238.00c  0.7968
      6012.00c  0.3217
      8016.00c  1.3613

c Graphite (CRITICAL: needs MT card!)
M11   6012.00c  0.9890   $ .00c for AGR-1 benchmark
      6013.00c  0.0110
MT11  C-GRPH.43t          $ 600 K thermal scattering

c SS316L structure
M12  26056.00c  -0.6041  $ Isotopic Fe, .00c for benchmark
     24052.00c  -0.1426  $ Isotopic Cr
     28058.00c  -0.0805  $ Isotopic Ni
```

**Why**:
- Benchmark validation: Must use .00c to reproduce published results
- New HTGR model: Use .80c or .70c instead

**For new HTGR models (not benchmark)**:
```mcnp
M10  92235.80c  0.1975   $ Use .80c for new designs
     92238.80c  0.8025
      6012.80c  0.9890   $ C-12 with latest evaluation
      6013.80c  0.0110
      8016.80c  2.0
```

### 3. Fast Reactors (Metallic or MOX Fuel)

**Standard approach**:
```mcnp
c U-Pu-Zr metallic fuel
M20  92238.80c  -0.686
     94239.80c  -0.120
     94240.80c  -0.050
     40000.70c  -0.100   $ Zr: .70c widely available

c SS316 clad (isotopic for activation)
M21  26054.70c  -0.038
     26056.70c  -0.604
     26057.70c  -0.013
     24050.70c  -0.007
     24052.70c  -0.143
     28058.70c  -0.081
```

**Why**:
- Actinides: .80c for best resonance data in fast spectrum
- Zr: Natural element, .70c or .60c
- Structure: Isotopic if activation calculation, .70c standard

### 4. Research Reactors (MTR-Type)

**U-Al dispersion**:
```mcnp
M30  92235.70c  -0.089   $ LEU fuel
     92238.70c  -0.361
     13027.70c  -0.550   $ Al-27
```

**Why**:
- .70c standard for research reactors
- .80c if available and consistent
- Older facilities may have .50c or .60c legacy data

---

## MIXING LIBRARY VERSIONS

### When Mixing is Acceptable

✅ **Special evaluations for specific isotopes**:
```mcnp
M1    5010.20c  ...      $ B-10 special thermal evaluation
      5011.70c  ...      $ B-11 standard ENDF/B-VII.0
      6000.70c  ...      $ C-nat standard
```
**Reason**: B-10 .20c library optimized for thermal neutron absorption

✅ **Unavailable isotope in standard library**:
```mcnp
M2   92235.80c  ...      $ U-235 ENDF/B-VIII.0
     92238.80c  ...      $ U-238 ENDF/B-VIII.0
     40000.70c  ...      $ Zr-nat only in .70c, not .80c
```
**Reason**: Natural Zr not in ENDF/B-VIII.0, use .70c

### When Mixing is WRONG

❌ **Inconsistent for no reason**:
```mcnp
M3   92235.80c  ...      $ BAD: mixing .80c and .70c for same element type
     92238.70c  ...      $ Should be 92238.80c
      8016.70c  ...      $ Should be 8016.80c
```

❌ **Benchmark validation with wrong library**:
```mcnp
c AGR-1 benchmark specifies .00c for graphite
M4   6012.70c  ...       $ WRONG: should be 6012.00c per benchmark spec
     6013.70c  ...
```

---

## LIBRARY VERSION HISTORY

### ENDF/B-VIII.0 (.80c) - 2018

**Major improvements**:
- Updated U-235, U-238 resonances (better reactivity predictions)
- Improved fission product data (Xe, Sm, Gd)
- Better thermal scattering (water, graphite)
- Pu-239, Pu-240, Pu-241 evaluations updated

**Use for**: New reactor designs, modern calculations

### ENDF/B-VII.0 (.70c) - 2006

**Standard for 15+ years**:
- Widely validated
- Available for most isotopes
- Default in many MCNP installations

**Use for**: General-purpose calculations, broad availability

### ENDF/B-VI.8 (.60c) - 2001

**Legacy**:
- Natural elements (Mg, Si, Ti, Zr, Mo)
- Some benchmarks specify .60c

**Use for**: Natural element backups, benchmark reproduction

### ENDF/B-VI.0 (.00c) - 1990

**Old but sometimes required**:
- Some benchmarks (AGR-1) specify .00c
- Legacy models

**Use for**: Benchmark validation ONLY

---

## VERIFICATION

### Check xsdir for Availability

```bash
# Check if isotope available in specific library
grep "92235.80c" $DATAPATH/xsdir

# Check all available versions of U-235
grep "92235" $DATAPATH/xsdir

# Check natural element
grep "40000" $DATAPATH/xsdir
```

**Interpretation**:
```
92235.80c   237.048080  endf80sab  ...   <- ENDF/B-VIII.0 available
92235.70c   235.043924  endf70sab  ...   <- ENDF/B-VII.0 available
92235.60c   235.043924  endf60sab  ...   <- ENDF/B-VI.8 available
```

### Use scripts/zaid_library_validator.py

```bash
python scripts/zaid_library_validator.py input.i
```

**Checks**:
- ✅ All ZAIDs exist in xsdir
- ✅ Library version consistency
- ✅ Flags mixed libraries (with reason if acceptable)
- ✅ Suggests alternatives if ZAID not found

---

## COMMON PATTERNS FROM PROFESSIONAL MODELS

### AGR-1 Benchmark (Mixed Libraries)

**Observations**:
```mcnp
c Actinides and oxygen: .70c (ENDF/B-VII.0)
   92235.70c, 92238.70c, 8016.70c

c Natural elements (Mg, Si, Ti, Zr, Mo): .60c (ENDF/B-VI.8)
   12000.60c, 14000.60c, 22000.60c, 40000.60c, 42000.60c

c Structural steel (Fe, Cr, Ni): .50c (ENDF/B-V)
   24000.50c, 26000.50c, 28000.50c

c AGR-specific materials: .00c (ENDF/B-VI.0)
   6012.00c, 2004.00c (for graphite, helium)

c B-10 special: .20c (optimized thermal)
   5010.20c

c Air: .80c (ENDF/B-VIII.0)
   7014.80c, 8016.80c
```

**Lesson**: Professional models mix libraries for specific reasons (benchmark specs, availability, optimization). Document reasons in comments!

---

## BEST PRACTICES

1. **Prefer latest library (.80c) for new models** unless specific reason not to
2. **Use .70c as default** if .80c not available (widely supported)
3. **Check xsdir availability** before running MCNP (use validation script)
4. **Be consistent within material type** (all actinides same library)
5. **Document exceptions** when mixing libraries (comments explaining why)
6. **For benchmarks: use EXACT library specified** in documentation
7. **Isotopic detail for physics-important nuclides** (U, Pu, FPs, absorbers)
8. **Natural elements for structural materials** (Fe, Cr, Ni) unless activation study
9. **Validate with mcnp-cross-section-manager** skill for complex cases

---

## DECISION SUMMARY FLOWCHART

```
START: Need to select ZAID library extension

├─→ Benchmark validation?
│    └─→ YES: Use library specified in benchmark → DONE
│    └─→ NO: Continue
│
├─→ Check xsdir for .80c
│    ├─→ Available: Use .80c → DONE
│    └─→ Not available: Continue
│
├─→ Check xsdir for .70c
│    ├─→ Available: Use .70c → DONE
│    └─→ Not available: Continue
│
├─→ Check xsdir for .60c
│    ├─→ Available: Use .60c (document why) → DONE
│    └─→ Not available: Consult mcnp-cross-section-manager
│
└─→ Special case (B-10, W, etc.)?
     └─→ Use special library (.20c, .55c, etc.) → DONE
```

---

## TROUBLESHOOTING

### Error: "nuclide zaid.nnx not available on any cross-section table"

**Cause**: Library extension not in xsdir

**Solution**:
1. Check xsdir: `grep "ZAID" $DATAPATH/xsdir`
2. Try alternative: .80c → .70c → .60c
3. For natural elements: ZZZAAA → ZZZ000
4. Consult mcnp-cross-section-manager skill

### Warning: "using old library .60c instead of newer .80c"

**Not an error**, but check if .80c available for better accuracy

**Action**:
- Review xsdir for .80c availability
- Update if consistent across materials
- Document reason if keeping .60c

---

## REFERENCES

**For library management**:
- mcnp-cross-section-manager skill - xsdir parsing, library installation

**For validation**:
- scripts/zaid_library_validator.py - Automated checking

**External Resources**:
- NNDC ENDF/B Library: https://www.nndc.bnl.gov/endf/
- MCNP6 Manual Section 1.2.2: Target Identifier Formats

---

**Version:** 1.0
**Created:** 2025-11-08
**For:** mcnp-material-builder skill v2.0
```

**Validation**: User asks "Should I use .80c or .70c for my PWR model?"
**Expected**: Skill provides decision tree, recommends .80c if available, shows how to check xsdir

---

[Continue in next response due to length...]

## 4. Create burnup_tracking_guide.md

**File**: `.claude/skills/mcnp-material-builder/burnup_tracking_guide.md`

**Purpose**: Guide for which isotopes to track in depletion calculations

**Content**:

```markdown
# Burnup Tracking Guide
## Which Isotopes to Track in Depletion Calculations and Why

**Purpose**: Help users select appropriate isotopes for burnup/depletion modeling
**Scope**: Actinide chains, fission products, activation products

---

## WHY TRACK SPECIFIC ISOTOPES?

Depletion calculations solve Bateman equations for isotope evolution during irradiation:

```
dN_i/dt = Σ_j (λ_j→i N_j + σ_j→i φ N_j) - (λ_i + σ_i φ) N_i

where:
  N_i = number density of isotope i
  λ_i = decay constant
  σ_i = reaction cross-section (capture, fission)
  φ = neutron flux
```

**Impact on reactor physics**:
- **Reactivity**: Fission products absorb neutrons (negative reactivity)
- **Spectrum**: Pu buildup hardens spectrum
- **Shutdown dose**: Activation products determine post-shutdown radiation
- **Fuel cycle**: Pu inventory affects reprocessing economics

**Trade-off**:
- More isotopes → better accuracy, longer computation time
- Fewer isotopes → faster, but may miss important physics

---

## MINIMUM ISOTOPE SET (20-25 isotopes)

### Actinides (Minimum: 8 isotopes)

**ALWAYS track**:
```mcnp
92234.70c  ...  $ U-234 (from U-235 decay, alpha source)
92235.70c  ...  $ U-235 (primary fissile, depletes)
92236.70c  ...  $ U-236 (from U-235 capture, parasitic absorber)
92238.70c  ...  $ U-238 (primary fertile, breeds Pu-239)
93237.70c  ...  $ Np-237 (from U-235 fission, Pu precursor)
94239.70c  ...  $ Pu-239 (bred from U-238, fissile)
94240.70c  ...  $ Pu-240 (from Pu-239 capture, parasitic)
94241.70c  ...  $ Pu-241 (fissile, important for reactivity)
```

**Why these**:
- U-235: Primary fissile, depletes monotonically
- U-238: Fertile material, breeds Pu-239 via (n,γ) then β⁻ decay
- Pu-239: Builds up from U-238, becomes dominant fissile after ~15 GWd/MTU
- Pu-240: Parasitic absorber, high spontaneous fission neutron source
- Pu-241: Fissile, important for reactivity but decays to Am-241
- Others: Complete chain from U-235 → Np-237 → Pu-238/239/240/241

**Reactivity impact**: Pu buildup compensates for U-235 depletion, extends fuel life

### Fission Products (Minimum: 10-12 isotopes)

**Strong absorbers (MUST track)**:
```mcnp
54135.70c  ...  $ Xe-135 (highest thermal σ_abs ≈ 2.65×10⁶ barn, equilibrium poison)
62149.70c  ...  $ Sm-149 (σ_abs ≈ 4.1×10⁴ barn, equilibrium + residual)
64157.70c  ...  $ Gd-157 (σ_abs ≈ 2.54×10⁵ barn, depletes slowly)
64155.70c  ...  $ Gd-155 (σ_abs ≈ 6.1×10⁴ barn, depletes)
```

**Medium absorbers**:
```mcnp
47109.70c  ...  $ Ag-109 (control rod material, if present)
61147.70c  ...  $ Pm-147 (β⁻ emitter, precursor)
61148.70c  ...  $ Pm-148 (β⁻ emitter)
61149.70c  ...  $ Pm-149 (precursor to Sm-149)
63151.70c  ...  $ Eu-151 (σ_abs ≈ 9,000 barn)
63153.70c  ...  $ Eu-153 (σ_abs ≈ 312 barn)
```

**Stable fission products** (for mass balance):
```mcnp
42095.70c  ...  $ Mo-95 (stable, high yield)
44101.70c  ...  $ Ru-101 (stable)
55133.70c  ...  $ Cs-133 (stable, high yield)
60143.70c  ...  $ Nd-143 (stable)
60145.70c  ...  $ Nd-145 (stable)
```

**Why these**:
- Xe-135: Equilibrium poison, huge cross-section, load-following transients
- Sm-149: Equilibrium + residual poison, doesn't decay, builds up
- Gd: Ultra-strong absorbers, used in burnable poisons
- Stable FPs: ~30-40% of fission products, affect spectrum

**Reactivity impact**: Fission products cause ~3000-5000 pcm negative reactivity after equilibrium

---

## COMPREHENSIVE ISOTOPE SET (40-60 isotopes)

### Extended Actinides (Add 6 more)

```mcnp
94242.70c  ...  $ Pu-242 (from Pu-241 capture, minor actinide)
95241.70c  ...  $ Am-241 (from Pu-241 decay, strong absorber)
95242.70c  ...  $ Am-242 (short-lived, from Am-241 capture)
95243.70c  ...  $ Am-243 (from Am-242 capture)
96242.70c  ...  $ Cm-242 (from Pu-241 beta decay, alpha emitter)
96244.70c  ...  $ Cm-244 (from Cm-242 capture chain, heat source)
```

**Why**:
- Am-241: Builds from Pu-241 decay (14.4 yr half-life), strong absorber
- Cm-242/244: Heat sources for spent fuel, important for decay heat
- Pu-242: Minor actinide, small but measurable impact

### Extended Fission Products (Add 20-30 more)

**Noble gases** (for release analysis):
```mcnp
36083.70c  ...  $ Kr-83 (stable, high yield)
54131.70c  ...  $ Xe-131 (stable, high yield)
54133.70c  ...  $ Xe-133 (radioactive, 5.2 day, release monitor)
```

**Absorbers**:
```mcnp
43099.70c  ...  $ Tc-99 (long-lived, absorber)
45103.70c  ...  $ Rh-103 (stable, moderate σ)
45105.70c  ...  $ Rh-105 (radioactive)
46105.70c  ...  $ Pd-105 (stable)
46107.70c  ...  $ Pd-107 (stable)
46108.70c  ...  $ Pd-108 (stable)
```

**High-yield stable isotopes**:
```mcnp
40093.70c  ...  $ Zr-93 (stable, cladding activation)
50117.70c  ...  $ Sn-117 (stable)
52130.70c  ...  $ Te-130 (stable)
56138.70c  ...  $ Ba-138 (stable, high yield)
57139.70c  ...  $ La-139 (stable)
58140.70c  ...  $ Ce-140 (stable, highest single FP yield ~6%)
59141.70c  ...  $ Pr-141 (stable)
```

**Why**:
- Better mass balance (track 60-70% of FP inventory)
- Activation products for dose calculations
- Release fractions for safety analysis

---

## BURNUP CALCULATION SETUP EXAMPLE

### Fresh Fuel (BOL)

```mcnp
c ========================================================================
c Material 1: Fresh UO2 fuel, 4.5% enriched
c ========================================================================
M1   92234.70c  3.6e-4   $ U-234 (~0.8% of U-235 content)
     92235.70c  0.045    $ U-235 (enrichment)
     92238.70c  0.955    $ U-238 (balance)
      8016.70c  2.0      $ O-16 (stoichiometric)
c Cell card:
1    1  -10.4  -1  IMP:N=1  TMP=8.62e-8  VOL=1000.0  $ Specify volume for tallies
```

**Key points**:
- VOL card REQUIRED for depletion tallies (normalize flux per unit volume)
- Only initial composition specified
- Depletion code (ORIGEN, CINDER) adds tracked isotopes

### Mid-Burnup Fuel (30 GWd/MTU)

**After depletion calculation**:
```mcnp
c ========================================================================
c Material 2: Depleted UO2 fuel at 30 GWd/MTU
c ========================================================================
M2   92234.70c  2.1e-4   $ U-234 (depleted)
     92235.70c  0.010    $ U-235 (depleted from 4.5%)
     92236.70c  0.0051   $ U-236 (built up from U-235 capture)
     92238.70c  0.9405   $ U-238 (slightly depleted)
     93237.70c  5.2e-4   $ Np-237 (from U-235 fission)
     94238.70c  2.1e-5   $ Pu-238
     94239.70c  0.0054   $ Pu-239 (bred from U-238)
     94240.70c  0.0024   $ Pu-240 (bred from Pu-239)
     94241.70c  0.0015   $ Pu-241 (bred from Pu-240)
     94242.70c  5.8e-4   $ Pu-242
     95241.70c  6.2e-5   $ Am-241 (from Pu-241 decay)
     54135.70c  1.2e-8   $ Xe-135 (equilibrium concentration)
     62149.70c  8.7e-9   $ Sm-149 (equilibrium + residual)
     64155.70c  3.1e-10  $ Gd-155
     64157.70c  2.4e-10  $ Gd-157
     42095.70c  6.8e-4   $ Mo-95 (stable FP)
     44101.70c  5.2e-4   $ Ru-101
     55133.70c  7.1e-4   $ Cs-133
     60143.70c  5.9e-4   $ Nd-143
     60145.70c  4.1e-4   $ Nd-145
      8016.70c  2.0      $ O-16 (constant)
c Cell card:
2    2  -10.1  -2  IMP:N=1  TMP=9.48e-8  VOL=1000.0
```

**Observations**:
- U-235 dropped from 4.5% → 1.0% (major depletion)
- Pu-239 built up to 0.54% (comparable to remaining U-235)
- Xe-135, Sm-149 at equilibrium (very small concentrations but huge cross-sections)
- Minor actinides (Np, Am) present at trace levels
- Stable FPs accumulating (mass balance)

---

## DEPLETION CALCULATION WORKFLOW

### Step 1: MCNP Neutron Transport

**Calculate neutron flux in depletion zones**:
```mcnp
c Tallies for depletion (one per depletion cell)
F4:N  (1 2 3 4 5 6 7 8 9 10)  $ Flux in each fuel pin
FM4   (-1 1 -6)                $ Total fission rate
SD4   1 10R                    $ Segment divisors (or use VOL card)
E4    1e-10 20                 $ Full energy range
```

**Output**: Neutron flux spectrum and reaction rates per cell

### Step 2: ORIGEN/CINDER Depletion

**Input to ORIGEN**:
- Flux spectrum from MCNP F4 tally
- One-group cross-sections (calculated from spectrum)
- Initial isotopic inventory
- Power level and time steps

**Calculation**:
- Solve Bateman equations for ~3000 isotopes
- Condense to tracked isotopes (~25-60)
- Output new composition at each time step

**Time steps** (typical PWR):
```
BOL → 1 day → 1 week → 1 month → 3 months → 6 months → 1 year → ...
Fine steps early (flux transients)
Coarser steps later (slow evolution)
```

### Step 3: Update MCNP Materials

**Replace material card with depleted composition**:
```bash
# Automated workflow (MOAA, VESTA, etc.)
mcnp6 i=input_BOL.i runtpe=BOL.r
extract_flux BOL.r → flux_spectrum.txt
origen < origen_input.txt > output.txt
extract_composition output.txt → depleted_material.m
update_input depleted_material.m → input_step2.i
mcnp6 i=input_step2.i runtpe=step2.r
# Repeat for multiple steps
```

### Step 4: Photon Transport (Shutdown Dose)

**At decay time t after shutdown**:
```mcnp
c Photon source from decaying isotopes (from ORIGEN output)
MODE P
SDEF  CEL=D1  ERG=D2  PAR=2
SI1  L  1 2 3 4 5       $ Source cells (fuel pins)
SP1     0.2 0.2 0.2 0.2 0.2  $ Cell probabilities
SI2  H  0.01 0.1 0.5 1.0 2.0 3.0  $ Photon energies [MeV]
SP2     0.0  0.35 0.28 0.22 0.10 0.05  $ Spectrum from ORIGEN
c Dose tally
F4:P  100                $ Detector cell
DE4   <ICRP energy bins>
DF4   <ICRP dose factors>
```

---

## ISOTOPE IMPORTANCE BY APPLICATION

### Criticality Safety

**Focus**: k-eff accuracy, minimal isotope set
```
Track: U-235, U-238, Pu-239, Pu-240, Pu-241
Skip: Minor actinides, most FPs (unless credit for burnup)
```

### Reactor Physics / Core Design

**Focus**: Reactivity coefficients, power distribution
```
Track: Full actinide chain (U-234→Cm-244)
       Strong FP absorbers (Xe-135, Sm-149, Gd-155/157)
       Stable FPs for spectrum effects
```

### Spent Fuel Characterization

**Focus**: Isotopic inventory for safeguards, waste
```
Track: All actinides (Pu vector, Am, Cm)
       Long-lived FPs (Tc-99, I-129, Cs-135/137, Sr-90)
       Heat-generating isotopes (Cs-137, Sr-90, Cm-244)
```

### Shutdown Dose Rate

**Focus**: Gamma/neutron sources after shutdown
```
Track: Co-60 (structure activation)
       Mn-54 (steel activation)
       Short-lived FPs (Ba-140, La-140, Ce-144)
       Actinides (alpha→n from Cm-244, Pu-240)
```

---

## VALIDATION

### Check Isotope Mass Balance

**Sum of all isotopes should equal total heavy metal**:
```
Σ(N_i × A_i) ≈ Initial heavy metal mass

Example: 1 kg UO2 @ 4.5% enrichment
Initial U: ~882 g
Final (after 30 GWd/MTU):
  U-235: ~88 g  (depleted)
  U-238: ~832 g (slightly depleted)
  Pu-239: ~47 g (bred)
  Pu-240: ~21 g
  Pu-241: ~13 g
  Minor actinides: ~5 g
  Fission products: ~35 g
  O-16: ~118 g (constant)
  Total: ~1159 g (includes FP mass)
```

**Fission product mass** ≈ Burnup × 0.95 g/GWd per kg initial HM

### Check Reactivity Evolution

**k-eff should decrease monotonically**:
```
BOL: k ≈ 1.30 (excess reactivity for burnup)
5 GWd/MTU: k ≈ 1.25
15 GWd/MTU: k ≈ 1.15 (Pu buildup compensates)
30 GWd/MTU: k ≈ 1.05
EOL: k ≈ 1.00 (critical, discharge)
```

**Non-monotonic behavior indicates**:
- Missing important isotope (Xe-135, Sm-149)
- Time step too coarse
- Flux spectrum mismatch (MCNP vs ORIGEN)

---

## BEST PRACTICES

1. **Start with minimum set** (20-25 isotopes), validate against measured data
2. **Add isotopes incrementally** if reactivity or mass balance errors >1%
3. **ALWAYS track Xe-135 and Sm-149** for thermal reactors (even if equilibrium assumption used)
4. **Track full Pu vector** (238-242) for burnup credit, safeguards
5. **Use fine time steps early** (first week), coarser later (after 1 month)
6. **Validate with measured data** (gamma spectroscopy, destructive assay) if available
7. **Document isotope selection** in input comments (why included/excluded)

---

## COMMON MISTAKES

### Mistake 1: Missing Xe-135 and Sm-149

**Impact**: k-eff 1000-3000 pcm too high
**Fix**: Always include equilibrium poisons

### Mistake 2: Incomplete Pu Chain

**Impact**: Underestimate Pu inventory, wrong spectrum
**Fix**: Track Pu-238 through Pu-242 minimum

### Mistake 3: Too Few FPs

**Impact**: Wrong neutron spectrum (too soft), reactivity error
**Fix**: Include at least 10 stable FPs for mass balance

### Mistake 4: Time Steps Too Coarse

**Impact**: Oscillating k-eff, unrealistic isotope concentrations
**Fix**: Use <1 week steps for first month, <1 month thereafter

---

## REFERENCES

**For depletion workflows**:
- MOAA (MCNP-ORIGEN Activation Automation): ORNL/TM-2018/1014
- VESTA: Verified, Efficient Simulation and Transport Analysis
- FISPACT-II: Inventory code for activation

**For isotope data**:
- JANIS: https://www.oecd-nea.org/janis/
- KAERI Table of Nuclides: https://atom.kaeri.re.kr/

**For fission yields**:
- ENDF/B-VIII.0 Fission Product Yields
- JEFF-3.3 Yield Library

**Integration**:
- mcnp-burnup-builder skill - Complete depletion setup
- mcnp-isotope-lookup skill - Find ZAIDs, cross-sections, yields

---

**Version:** 1.0
**Created:** 2025-11-08
**For:** mcnp-material-builder skill v2.0
```

**Validation**: User asks "Which isotopes should I track for PWR burnup?"
**Expected**: Skill provides minimum set (actinides + Xe/Sm/Gd), explains why, gives example material cards

---

## 5. Enhance thermal_scattering_reference.md

**File**: `.claude/skills/mcnp-material-builder/thermal_scattering_reference.md`

**Current state**: Good coverage of S(α,β) tables (336 lines)

**ADD at end** (before "See Also" section, around line 310):

```markdown
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
```

**Validation**: Skill now EMPHASIZES graphite MT cards as CRITICAL, not optional

---

## 6. Create thermal_scattering_checker.py

**File**: `.claude/skills/mcnp-material-builder/scripts/thermal_scattering_checker.py`

**Purpose**: Automated validation of MT card requirements

**Content**:

```python
#!/usr/bin/env python3
"""
MCNP Thermal Scattering Checker

Validates that materials requiring S(alpha,beta) treatment have MT cards.

CRITICAL CHECK: Detects missing graphite MT cards (common professional model error)

Usage:
    python thermal_scattering_checker.py input.i
    python thermal_scattering_checker.py --verbose input.i

Author: MCNP Skills System
Version: 1.0
Created: 2025-11-08
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Elements that REQUIRE thermal scattering in thermal systems
THERMAL_SCATTERING_ELEMENTS = {
    '1': 'H',   # Hydrogen
    '2': 'He',  # Helium (sometimes)
    '4': 'Be',  # Beryllium
    '6': 'C',   # Carbon (GRAPHITE - CRITICAL!)
    '8': 'O',   # Oxygen (in water, BeO)
}

# S(alpha,beta) table patterns
SALPHABETA_TABLES = {
    'H-H2O': 'Hydrogen in water',
    'H-CH2': 'Hydrogen in polyethylene',
    'H-BENZ': 'Hydrogen in benzene',
    'H-ZRH': 'Hydrogen in zirconium hydride',
    'D-D2O': 'Deuterium in heavy water',
    'C-GRPH': 'Carbon in graphite',
    'Be-MET': 'Beryllium metal',
    'Be-BEO': 'Beryllium in BeO',
    'O-BEO': 'Oxygen in BeO',
    'LWTR': 'Light water (old format)',
    'HWTR': 'Heavy water (old format)',
    'POLY': 'Polyethylene (old format)',
    'GRPH': 'Graphite (old format)',
    'BE': 'Beryllium (old format)',
}


class MaterialCard:
    """Represents an MCNP material card"""

    def __init__(self, material_number: str):
        self.number = material_number
        self.isotopes: List[Tuple[str, str, str]] = []  # (ZAID, fraction, library)
        self.has_mt_card = False
        self.mt_tables: List[str] = []
        self.tmp_temperature = None
        self.elements_present: Set[str] = set()

    def add_isotope(self, zaid: str, fraction: str):
        """Add isotope to material composition"""
        # Extract Z, A, library
        match = re.match(r'(\d+)(\d{3})\.?(\d*\w*)?', zaid)
        if match:
            z = str(int(match.group(1)))  # Atomic number
            a = match.group(2)  # Mass number (000 for natural)
            lib = match.group(3) if match.group(3) else ''
            self.isotopes.append((f"{z}{a}", fraction, lib))
            self.elements_present.add(z)

    def needs_thermal_scattering(self) -> bool:
        """Check if material contains elements requiring S(alpha,beta)"""
        return bool(self.elements_present & THERMAL_SCATTERING_ELEMENTS.keys())

    def get_elements_needing_mt(self) -> List[str]:
        """Return list of element symbols that need MT cards"""
        return [THERMAL_SCATTERING_ELEMENTS[z] for z in
                self.elements_present & THERMAL_SCATTERING_ELEMENTS.keys()]


def parse_mcnp_input(filename: str) -> Tuple[Dict[str, MaterialCard], Dict[str, float]]:
    """
    Parse MCNP input file for material and MT cards

    Returns:
        materials: Dict of material number → MaterialCard
        tmp_cards: Dict of material number → temperature (MeV)
    """
    materials = {}
    tmp_cards = {}

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Track which block we're in
    in_data_block = False
    current_material = None
    current_card_type = None
    continuation_lines = []

    for line in lines:
        # Strip comments
        if 'c ' == line[:2].lower() and line[1] == ' ':
            continue

        # Handle line continuation
        stripped = line.rstrip()
        if stripped and stripped[-1] == '&':
            continuation_lines.append(stripped[:-1])
            continue
        else:
            if continuation_lines:
                full_line = ''.join(continuation_lines) + stripped
                continuation_lines = []
            else:
                full_line = stripped

        # Skip blank lines
        if not full_line.strip():
            current_material = None
            current_card_type = None
            continue

        # Check for data block start (first blank line after cell cards)
        # Simple heuristic: data cards start with known keywords
        if full_line.strip() and full_line[0] not in ['c', 'C', ' ']:
            in_data_block = True

        # Parse M cards (material composition)
        m_match = re.match(r'^[mM](\d+)\s+', full_line)
        if m_match:
            mat_num = m_match.group(1)
            if mat_num not in materials:
                materials[mat_num] = MaterialCard(mat_num)
            current_material = mat_num
            current_card_type = 'M'

            # Parse isotopes on this line
            remainder = full_line[m_match.end():]
            parse_material_isotopes(materials[mat_num], remainder)
            continue

        # Parse MT cards (thermal scattering)
        mt_match = re.match(r'^[mM][tT](\d+)\s+', full_line)
        if mt_match:
            mat_num = mt_match.group(1)
            if mat_num in materials:
                materials[mat_num].has_mt_card = True
                remainder = full_line[mt_match.end():]
                tables = remainder.split()
                materials[mat_num].mt_tables.extend(tables)
            current_card_type = 'MT'
            continue

        # Parse TMP cards (temperature)
        tmp_match = re.match(r'^[tT][mM][pP](\d+)\s+(\S+)', full_line)
        if tmp_match:
            mat_num = tmp_match.group(1)
            temp_mev = float(tmp_match.group(2))
            tmp_cards[mat_num] = temp_mev
            current_card_type = 'TMP'
            continue

        # Continuation of current card
        if current_material and current_card_type == 'M':
            parse_material_isotopes(materials[current_material], full_line)

    return materials, tmp_cards


def parse_material_isotopes(material: MaterialCard, line: str):
    """Extract ZAID and fraction pairs from material card line"""
    tokens = line.split()
    i = 0
    while i < len(tokens) - 1:
        zaid = tokens[i]
        fraction = tokens[i + 1]
        # Check if it looks like a ZAID (number with optional .nnX)
        if re.match(r'\d+\.?\d*\w*', zaid) and re.match(r'-?\d+\.?\d*[eE]?[+-]?\d*', fraction):
            material.add_isotope(zaid, fraction)
            i += 2
        else:
            i += 1


def temperature_from_mev(temp_mev: float) -> float:
    """Convert temperature from MeV to Kelvin"""
    # T [K] = T [MeV] / 8.617e-11
    return temp_mev / 8.617e-11


def check_mt_temperature_match(mt_table: str, tmp_kelvin: float) -> Tuple[bool, str]:
    """
    Check if MT table temperature matches TMP card temperature

    Returns:
        (matches, message)
    """
    # Extract temperature from table name (approximate)
    temp_map = {
        '40': (293, 296),    # Room temp
        '41': (323, 400),    # Warm
        '42': (373, 500),    # Elevated
        '43': (423, 600),    # Operating
        '44': (473, 700),    # High
        '45': (523, 800),    # Very high
        '46': (573, 1000),   # VHTR
        '47': (623, 1200),   # Extreme
        '48': (800, 1600),   # Accident
        '49': (1000, 2000),  # Maximum
    }

    # Extract nn from table name (e.g., C-GRPH.43t → 43, GRPH.47T → 47)
    match = re.search(r'\.(\d{2})[tT]', mt_table)
    if match:
        code = match.group(1)
        if code in temp_map:
            t_min, t_max = temp_map[code]
            if t_min <= tmp_kelvin <= t_max:
                return True, f"Temperature match OK ({tmp_kelvin:.0f}K within {t_min}-{t_max}K range)"
            else:
                return False, f"MISMATCH: TMP={tmp_kelvin:.0f}K, but MT table is for {t_min}-{t_max}K"

    return None, "Cannot determine MT table temperature"


def main():
    parser = argparse.ArgumentParser(
        description='Check MCNP input for missing thermal scattering (MT) cards'
    )
    parser.add_argument('input_file', help='MCNP input file to check')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed information for all materials')
    parser.add_argument('--critical-only', action='store_true',
                        help='Only report critical errors (missing MT cards)')

    args = parser.parse_args()

    if not Path(args.input_file).exists():
        print(f"ERROR: File '{args.input_file}' not found!")
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print(f"MCNP Thermal Scattering Checker")
    print(f"{'=' * 70}")
    print(f"Input file: {args.input_file}\n")

    # Parse input file
    materials, tmp_cards = parse_mcnp_input(args.input_file)

    if not materials:
        print("WARNING: No material cards found in input file!")
        sys.exit(0)

    print(f"Found {len(materials)} material(s)\n")

    # Check each material
    errors = []
    warnings = []
    ok_count = 0

    for mat_num in sorted(materials.keys(), key=lambda x: int(x)):
        material = materials[mat_num]

        # Skip materials that don't need thermal scattering
        if not material.needs_thermal_scattering():
            if args.verbose:
                print(f"Material M{mat_num}: No thermal scattering elements present")
            continue

        # Material needs S(alpha,beta) treatment
        elements_needing_mt = material.get_elements_needing_mt()

        # CRITICAL: Check for graphite
        has_carbon = '6' in material.elements_present
        has_hydrogen = '1' in material.elements_present

        if not material.has_mt_card:
            # CRITICAL ERROR
            error_msg = (
                f"Material M{mat_num}: MISSING MT CARD!\n"
                f"  Contains: {', '.join(elements_needing_mt)}\n"
                f"  Impact: Free-gas scattering instead of molecular binding\n"
            )

            if has_carbon:
                error_msg += (
                    f"  **CRITICAL**: Graphite detected - reactivity error 1000-5000 pcm likely!\n"
                    f"  FIX: Add MT{mat_num}  C-GRPH.43t (or appropriate temperature)\n"
                )
            elif has_hydrogen:
                error_msg += (
                    f"  FIX: Add MT{mat_num}  H-H2O.40t (or H-CH2.40t, etc.)\n"
                )

            errors.append(error_msg)
            print(f"❌ {error_msg}")

        else:
            # MT card present - check details
            print(f"✅ Material M{mat_num}: MT card present")
            print(f"   Contains: {', '.join(elements_needing_mt)}")
            print(f"   MT tables: {', '.join(material.mt_tables)}")

            # Check temperature match if TMP card present
            if mat_num in tmp_cards:
                tmp_kelvin = temperature_from_mev(tmp_cards[mat_num])
                print(f"   TMP{mat_num} = {tmp_cards[mat_num]:.2e} MeV ({tmp_kelvin:.0f} K)")

                for table in material.mt_tables:
                    match, msg = check_mt_temperature_match(table, tmp_kelvin)
                    if match is True:
                        print(f"   ✅ {msg}")
                    elif match is False:
                        warn_msg = f"Material M{mat_num}: {msg}"
                        warnings.append(warn_msg)
                        print(f"   ⚠️  {msg}")

            ok_count += 1
            print()

    # Summary
    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total materials checked: {len([m for m in materials.values() if m.needs_thermal_scattering()])}")
    print(f"✅ Correct MT cards: {ok_count}")
    print(f"❌ Missing MT cards: {len(errors)}")
    print(f"⚠️  Warnings: {len(warnings)}")

    if errors:
        print(f"\n{'=' * 70}")
        print(f"CRITICAL ERRORS (must fix before running)")
        print(f"{'=' * 70}")
        for error in errors:
            print(error)

    if warnings and not args.critical_only:
        print(f"\n{'=' * 70}")
        print(f"WARNINGS (check carefully)")
        print(f"{'=' * 70}")
        for warning in warnings:
            print(f"⚠️  {warning}")

    # Exit code
    if errors:
        print(f"\n❌ FAILED: {len(errors)} critical error(s) found")
        print(f"   Fix missing MT cards before running MCNP!")
        sys.exit(1)
    elif warnings:
        print(f"\n⚠️  PASSED with warnings: Review temperature mismatches")
        sys.exit(0)
    else:
        print(f"\n✅ PASSED: All thermal scattering requirements met")
        sys.exit(0)


if __name__ == '__main__':
    main()
```

**Validation**: Run on input file with missing graphite MT cards
**Expected**: Script detects error, provides fix, exits with error code

---

## 7. Create triso_fuel_reference.md (Supplemental)

**File**: `.claude/skills/mcnp-material-builder/triso_fuel_reference.md`

**Purpose**: TRISO-specific material patterns (supplemental to main fuel reference)

**Content** (abbreviated - full version in actual file):

```markdown
# TRISO Fuel Reference (Supplemental)
## Material Specifications for TRISO Particle Fuel

**Purpose**: Supplemental reference for TRISO-specific patterns
**Note**: This supplements fuel_compositions_reference.md - refer there for general fuel types

---

## TRISO PARTICLE STRUCTURE

5-layer coated particle design:

```
Layer 1: Kernel (UCO or UO2, fissile)
Layer 2: Buffer (porous carbon, accommodate fission gases)
Layer 3: IPyC (inner pyrolytic carbon, diffusion barrier)
Layer 4: SiC (silicon carbide, structural, fission product retention)
Layer 5: OPyC (outer pyrolytic carbon, protect SiC)
```

**Complete 5-layer example**: See fuel_compositions_reference.md Section 2.1

---

## COMMON TRISO SPECIFICATIONS

### AGR-1 Experiment (INL)

**UCO kernel**: 19.75% enriched, 10.924 g/cm³
**Coating densities**: Buffer 1.10, IPyC 1.912, SiC 3.207, OPyC 1.901 g/cm³
**Dimensions**: See QUICK_REFERENCE_TRISO_SPECS.md

### HTR-10 (China)

**UO₂ kernel**: 17% enriched, 10.4 g/cm³
**Coating densities**: Similar to AGR-1

### PBMR (South Africa)

**UO₂ kernel**: 9.6% enriched, fuel element design

---

## CRITICAL: MT CARDS FOR ALL CARBON LAYERS

**REQUIRED for correct physics**:
```mcnp
MT11  C-GRPH.43t  $ Buffer carbon
MT12  C-GRPH.43t  $ IPyC
MT13  C-GRPH.43t  $ SiC (carbon component)
MT14  C-GRPH.43t  $ OPyC
MT15  C-GRPH.43t  $ Matrix
```

**Professional models have missed this - DO NOT SKIP!**

---

## SEE ALSO

- fuel_compositions_reference.md - Complete fuel type coverage (UO₂, MOX, UCO, etc.)
- thermal_scattering_reference.md - MT card requirements
- mcnp-lattice-builder skill - TRISO particle lattice structures
```

**Validation**: TRISO content is supplemental, not main focus of skill

---

## 8. Update Example Materials

**Files**: `.claude/skills/mcnp-material-builder/example_materials/*.txt`

**ACTION**: Add examples for UCO, MOX, metallic, HALEU fuels

**Specifically update**:
- `02_htgr_materials.txt` - Add complete TRISO 5-layer with MT cards, UCO kernel
- `03_fast_reactor_materials.txt` - Add U-Zr, U-Pu-Zr metallic examples
- NEW: `07_haleu_fuels.txt` - Examples at 10%, 15%, 19.75% enrichment

---

# PHASE 1 IMPLEMENTATION CHECKLIST

Execute in this order during refinement session:

## Session 1: Critical Material Card Fixes (2-3 hours)

### Task 1.1: Update SKILL.md (30 min)
- [ ] Add Use Case 5: Graphite Moderator (with MT card, temperature matching)
- [ ] Add Use Case 6: UCO TRISO Fuel Kernel
- [ ] Add Use Case 7: Depleted Fuel with Burnup Tracking
- [ ] Add Error 4: Missing Graphite Thermal Scattering
- [ ] Add Best Practices 11-13 (graphite MT, temperature matching, FP tracking)
- [ ] Test: Ask skill "How do I model graphite?" → Should provide MT card example

### Task 1.2: Create fuel_compositions_reference.md (45 min)
- [ ] Section 1: LWR Fuels (UO₂ at 3.5%, 4.5%, 5.0%, MOX)
- [ ] Section 2: HTGR Fuels (UCO, UO₂ TRISO, complete 5-layer with MT cards)
- [ ] Section 3: Fast Reactor Fuels (U-Zr, U-Pu-Zr metallic)
- [ ] Section 4: Advanced Fuels (HALEU at 10%, 15%, 19.75%)
- [ ] Section 5-10: Research, isotopic detail, libraries, temperature, validation
- [ ] Test: Ask "UCO fuel composition?" → Should get complete example with O>1.0 explanation

### Task 1.3: Create ZAID_selection_guide.md (30 min)
- [ ] Decision tree flowchart (benchmark vs new, availability, isotopic vs natural)
- [ ] Library selection by application (LWR, HTGR, fast reactor, research)
- [ ] Mixing library versions (when OK, when WRONG)
- [ ] Library version history (.80c, .70c, .60c, .00c)
- [ ] Verification (xsdir checking, validation script)
- [ ] Common patterns from professional models (AGR-1 example)
- [ ] Test: Ask ".80c or .70c?" → Should get decision tree, xsdir check command

### Task 1.4: Create burnup_tracking_guide.md (45 min)
- [ ] Why track specific isotopes (physics impact)
- [ ] Minimum set (20-25 isotopes): actinides + strong FP absorbers
- [ ] Comprehensive set (40-60 isotopes): extended actinides + FPs
- [ ] Depletion workflow (MCNP → ORIGEN → update materials)
- [ ] Isotope importance by application (criticality, reactor physics, spent fuel, dose)
- [ ] Validation (mass balance, reactivity evolution)
- [ ] Common mistakes (missing Xe/Sm, incomplete Pu, too few FPs)
- [ ] Test: Ask "isotopes for burnup?" → Should get minimum set with explanation

### Task 1.5: Enhance thermal_scattering_reference.md (15 min)
- [ ] Add CRITICAL REMINDER section on graphite MT cards
- [ ] Add impact of missing graphite S(alpha,beta)
- [ ] Add temperature selection table for graphite (293K → 2000K)
- [ ] Add validation script reference
- [ ] Test: Skill should now EMPHASIZE graphite MT as critical, not optional

### Task 1.6: Create thermal_scattering_checker.py (45 min)
- [ ] Parse MCNP input for M, MT, TMP cards
- [ ] Detect materials with H, C, Be, O (need thermal scattering)
- [ ] Check if MT cards present
- [ ] CRITICAL: Flag missing graphite MT cards
- [ ] Validate temperature matching (MT table temp vs TMP card)
- [ ] Generate error/warning report
- [ ] Exit codes (0=pass, 1=critical errors)
- [ ] Test: Run on file with missing graphite MT → Should detect and report error

### Task 1.7: Create triso_fuel_reference.md (15 min)
- [ ] Note: Supplemental to fuel_compositions_reference.md
- [ ] 5-layer TRISO structure
- [ ] Common TRISO specifications (AGR-1, HTR-10, PBMR)
- [ ] CRITICAL: MT cards for all carbon layers
- [ ] Cross-references to main fuel reference
- [ ] Test: TRISO content should be supplement, not main skill focus

### Task 1.8: Update example_materials (15 min)
- [ ] 02_htgr_materials.txt: Complete TRISO 5-layer with MT cards
- [ ] 03_fast_reactor_materials.txt: U-Zr, U-Pu-Zr metallic fuels
- [ ] Create 07_haleu_fuels.txt: 10%, 15%, 19.75% enrichment examples

---

# VALIDATION TESTS

Run these tests after Phase 1 completion:

## Test 1: Graphite MT Card Emphasis

**Query**: "How do I model graphite for an HTGR?"

**Expected Response**:
```
Material card example with C-12/C-13 composition
MT card (C-GRPH.43t or appropriate temperature) - EMPHASIZED AS REQUIRED
TMP card matching MT temperature
WARNING about missing MT cards in professional models
Impact: 1000-5000 pcm error if missing
Reference to thermal_scattering_reference.md
```

## Test 2: UCO Fuel Composition

**Query**: "What's the composition for UCO TRISO fuel kernel?"

**Expected Response**:
```
Complete UCO example (U-234/235/236/238, C-12/13, O-16)
Explanation that O fraction >1.0 is VALID (stoichiometric ratio)
Chemical formula UC0.32O1.36
Enrichment: 19.75% typical
Reference to fuel_compositions_reference.md
Cross-reference to triso_fuel_reference.md for complete 5-layer
```

## Test 3: ZAID Library Selection

**Query**: "Should I use .80c or .70c libraries for my PWR?"

**Expected Response**:
```
Decision tree: Check .80c availability → use if available
If not, use .70c (standard)
Command to check xsdir: grep "92235" $DATAPATH/xsdir
Consistency requirement (all materials same library if possible)
Reference to ZAID_selection_guide.md for complete decision tree
```

## Test 4: Burnup Isotope Tracking

**Query**: "Which isotopes should I track for depletion calculation?"

**Expected Response**:
```
Minimum set (20-25): Actinides (U-234→Pu-241), Xe-135, Sm-149, Gd-155/157
Explanation of why (reactivity impact, strong absorbers)
Example material card with depleted composition
Reference to burnup_tracking_guide.md for comprehensive set
```

## Test 5: Thermal Scattering Checker Usage

**Query**: "How do I check if I'm missing MT cards?"

**Expected Response**:
```
Use thermal_scattering_checker.py script
Command: python scripts/thermal_scattering_checker.py input.i
What it checks: Materials with H/C/Be/O, MT card presence, temperature matching
CRITICAL: Detects missing graphite MT cards
Example output showing errors and fixes
```

---

# SUCCESS CRITERIA

## Skill Refinement Complete When:

1. ✅ **Graphite MT cards EMPHASIZED throughout**
   - Use Case 5 in SKILL.md shows complete example
   - Error 4 warns of critical impact
   - thermal_scattering_reference.md has CRITICAL REMINDER section
   - thermal_scattering_checker.py flags missing graphite MT

2. ✅ **Comprehensive fuel coverage**
   - fuel_compositions_reference.md covers UO₂, MOX, UCO, metallic, HALEU
   - Each fuel type has multiple enrichment examples
   - Stoichiometry explained (O>1.0 valid for UCO)
   - TRISO is supplemental content, not main focus

3. ✅ **ZAID selection guidance clear**
   - ZAID_selection_guide.md provides decision tree
   - When to use .80c vs .70c vs .60c explained
   - Isotopic vs natural element criteria
   - Benchmark validation vs new model distinction

4. ✅ **Burnup tracking complete**
   - burnup_tracking_guide.md explains minimum set (20-25 isotopes)
   - Why track each isotope (physics impact)
   - Example depleted material cards
   - Validation methods (mass balance, k-eff evolution)

5. ✅ **Validation tools functional**
   - thermal_scattering_checker.py runs without errors
   - Detects missing MT cards correctly
   - Provides actionable fix recommendations
   - Exit codes appropriate for automation

6. ✅ **User queries answered correctly**
   - All 5 validation tests pass
   - Skill provides complete examples with explanations
   - Cross-references to detailed documentation
   - CRITICAL issues emphasized, not buried

---

# EXECUTION TIME ESTIMATE

**Total Phase 1 Time**: 2.5 - 3 hours

| Task | Time | Cumulative |
|------|------|------------|
| 1.1 Update SKILL.md | 30 min | 0:30 |
| 1.2 fuel_compositions_reference.md | 45 min | 1:15 |
| 1.3 ZAID_selection_guide.md | 30 min | 1:45 |
| 1.4 burnup_tracking_guide.md | 45 min | 2:30 |
| 1.5 Enhance thermal_scattering_reference.md | 15 min | 2:45 |
| 1.6 thermal_scattering_checker.py | 45 min | 3:30 |
| 1.7 triso_fuel_reference.md | 15 min | 3:45 |
| 1.8 Update example_materials | 15 min | 4:00 |
| **Validation & Testing** | 30 min | **4:30** |

**With focused execution**: Can complete in 2.5-3 hours

---

# READY FOR EXECUTION

This refinement plan is:
- ✅ **Specific**: Exact files, sections, content specified
- ✅ **Actionable**: Clear tasks with completion criteria
- ✅ **Based on real findings**: AGR-1 analysis identified all gaps
- ✅ **Prioritized**: CRITICAL thermal scattering emphasized throughout
- ✅ **Generalized**: Covers ALL fuel types, not just TRISO
- ✅ **Validated**: 5 test queries ensure correct behavior
- ✅ **Time-bounded**: 2.5-3 hours for high-priority fixes

**Execute Phase 1 in next session to complete mcnp-material-builder refinement.**

---

**PLAN COMPLETE**
**Created**: 2025-11-08
**For**: mcnp-material-builder skill v2.0 → v2.1
