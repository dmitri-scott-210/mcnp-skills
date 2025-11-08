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
