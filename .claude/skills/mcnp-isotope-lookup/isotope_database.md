# MCNP Isotope Database

## Overview

This reference provides comprehensive isotope property data for MCNP material definitions, including atomic masses, natural abundances, stable isotope identification, and element-to-ZAID conversion tables. Data sourced from NIST, IAEA, and NNDC (2024 values).

## Atomic Mass Unit (AMU)

### Definition

The atomic mass unit (amu or u) is defined as exactly 1/12 the mass of a carbon-12 atom.

```
1 amu = 1.66053906660 × 10⁻²⁷ kg    (exact, by definition)
1 amu = 1.66053906660 × 10⁻²⁴ g

Energy equivalent:
1 amu = 931.49410242 MeV/c²         (CODATA 2018)

Inverse:
1 MeV/c² = 1.07354410⁻³ amu
```

### Historical Note

Before 2019, the amu was a measured value with uncertainty. Since the 2019 SI redefinition, fundamental constants (including NA) are exact, making the amu calculable with higher precision.

### MCNP Usage

```
Material density calculation:
  N (atoms/b-cm) = (ρ × NA) / (A × 10²⁴)

where:
  ρ  = mass density (g/cm³)
  NA = 6.02214076 × 10²³ mol⁻¹ (Avogadro constant)
  A  = atomic mass (amu or g/mol)

Example - Iron at 7.85 g/cm³:
  A_Fe = 55.845 amu (average atomic mass)
  N = (7.85 × 6.022×10²³) / (55.845 × 10²⁴)
  N = 0.0846 atoms/b-cm
```

## Atomic Masses - Common Isotopes

### Light Elements

| Isotope | Z | A | Atomic Mass (amu) | Natural Abundance | Notes |
|---------|---|---|-------------------|-------------------|-------|
| H-1     | 1 | 1 | 1.00782503207     | 99.9885%         | Protium |
| H-2     | 1 | 2 | 2.01410177812     | 0.0115%          | Deuterium (D) |
| H-3     | 1 | 3 | 3.0160492779      | ~0% (radioactive)| Tritium (T), t₁/₂=12.3 yr |
| He-3    | 2 | 3 | 3.0160293201      | 0.000137%        | Rare |
| He-4    | 2 | 4 | 4.00260325413     | 99.999863%       | Alpha particle |
| Li-6    | 3 | 6 | 6.0151228874      | 7.59%            | Neutron absorber |
| Li-7    | 3 | 7 | 7.0160034366      | 92.41%           | |
| Be-9    | 4 | 9 | 9.0121831065      | 100%             | Monoisotopic |
| B-10    | 5 | 10| 10.0129369280     | 19.9%            | Strong absorber |
| B-11    | 5 | 11| 11.0093054600     | 80.1%            | |
| C-12    | 6 | 12| 12.0000000000     | 98.93%           | Mass standard |
| C-13    | 6 | 13| 13.0033548378     | 1.07%            | |
| N-14    | 7 | 14| 14.0030740044     | 99.636%          | |
| N-15    | 7 | 15| 15.0001088989     | 0.364%           | |
| O-16    | 8 | 16| 15.9949146196     | 99.757%          | Most common |
| O-17    | 8 | 17| 16.9991317565     | 0.038%           | |
| O-18    | 8 | 18| 17.9991596129     | 0.205%           | |
| F-19    | 9 | 19| 18.9984031627     | 100%             | Monoisotopic |
| Na-23   | 11| 23| 22.9897692820     | 100%             | Monoisotopic |
| Al-27   | 13| 27| 26.9815385160     | 100%             | Monoisotopic, activation |
| Si-28   | 14| 28| 27.9769265350     | 92.223%          | |
| Si-29   | 14| 29| 28.9764946649     | 4.685%           | |
| Si-30   | 14| 30| 29.9737701340     | 3.092%           | |
| P-31    | 15| 31| 30.9737619985     | 100%             | Monoisotopic |
| Cl-35   | 17| 35| 34.9688527280     | 75.76%           | |
| Cl-37   | 17| 37| 36.9659026230     | 24.24%           | |

### Structural Materials

| Isotope | Z | A | Atomic Mass (amu) | Natural Abundance | Notes |
|---------|---|---|-------------------|-------------------|-------|
| Fe-54   | 26| 54| 53.9396090         | 5.845%           | |
| Fe-56   | 26| 56| 55.9349375         | 91.754%          | Dominant |
| Fe-57   | 26| 57| 56.9353940         | 2.119%           | |
| Fe-58   | 26| 58| 57.9332756         | 0.282%           | |
| Ni-58   | 28| 58| 57.9353429         | 68.077%          | |
| Ni-60   | 28| 60| 59.9307864         | 26.223%          | |
| Ni-61   | 28| 61| 60.9310560         | 1.140%           | |
| Ni-62   | 28| 62| 61.9283451         | 3.634%           | |
| Ni-64   | 28| 64| 63.9279660         | 0.926%           | |
| Cu-63   | 29| 63| 62.9295975         | 69.15%           | |
| Cu-65   | 29| 65| 64.9277895         | 30.85%           | |
| Zr-90   | 40| 90| 89.9047044         | 51.45%           | Cladding |
| Zr-91   | 40| 91| 90.9056458         | 11.22%           | |
| Zr-92   | 40| 92| 91.9050408         | 17.15%           | |
| Zr-94   | 40| 94| 93.9063152         | 17.38%           | |
| Zr-96   | 40| 96| 95.9082734         | 2.80%            | |

### Heavy Metals and Shielding

| Isotope | Z | A | Atomic Mass (amu) | Natural Abundance | Notes |
|---------|---|---|-------------------|-------------------|-------|
| Pb-204  | 82| 204| 203.9730440       | 1.4%             | |
| Pb-206  | 82| 206| 205.9744653       | 24.1%            | |
| Pb-207  | 82| 207| 206.9758969       | 22.1%            | |
| Pb-208  | 82| 208| 207.9766521       | 52.4%            | Dominant, double magic |
| Bi-209  | 83| 209| 208.9803987       | 100%             | Monoisotopic |
| W-180   | 74| 180| 179.9467108       | 0.12%            | |
| W-182   | 74| 182| 181.9482042       | 26.50%           | |
| W-183   | 74| 183| 182.9502230       | 14.31%           | |
| W-184   | 74| 184| 183.9509312       | 30.64%           | |
| W-186   | 74| 186| 185.9543641       | 28.43%           | |

### Fissile and Fertile Materials

| Isotope | Z | A | Atomic Mass (amu) | Natural Abundance | Notes |
|---------|---|---|-------------------|-------------------|-------|
| U-233   | 92| 233| 233.0396352       | ~0% (bred)       | Fissile, t₁/₂=1.6×10⁵ yr |
| U-234   | 92| 234| 234.0409521       | 0.0054%          | Fertile, trace in natural U |
| U-235   | 92| 235| 235.0439301       | 0.7204%          | Fissile |
| U-238   | 92| 238| 238.0507882       | 99.2742%         | Fertile, dominant |
| Np-237  | 93| 237| 237.0481734       | ~0% (bred)       | α emitter, t₁/₂=2.1×10⁶ yr |
| Pu-238  | 94| 238| 238.0495599       | ~0% (bred)       | RTG fuel, t₁/₂=87.7 yr |
| Pu-239  | 94| 239| 239.0521634       | ~0% (bred)       | Fissile, t₁/₂=2.4×10⁴ yr |
| Pu-240  | 94| 240| 240.0538135       | ~0% (bred)       | Fertile, high spontaneous fission |
| Pu-241  | 94| 241| 241.0568515       | ~0% (bred)       | Fissile, t₁/₂=14.3 yr |
| Pu-242  | 94| 242| 242.0587426       | ~0% (bred)       | Fertile |
| Am-241  | 95| 241| 241.0568291       | ~0% (bred)       | α emitter, t₁/₂=432.2 yr |
| Am-243  | 95| 243| 243.0613811       | ~0% (bred)       | α emitter, t₁/₂=7370 yr |

## Natural Isotopic Compositions

### Elements with Single Stable Isotope

These elements have 100% natural abundance of one isotope:

| Element | Z | Isotope | A | Atomic Mass (amu) |
|---------|---|---------|---|-------------------|
| Beryllium | 4 | Be-9   | 9 | 9.0121831         |
| Fluorine  | 9 | F-19   | 19| 18.9984032        |
| Sodium    | 11| Na-23  | 23| 22.9897693        |
| Aluminum  | 13| Al-27  | 27| 26.9815386        |
| Phosphorus| 15| P-31   | 31| 30.9737620        |
| Scandium  | 21| Sc-45  | 45| 44.9559083        |
| Manganese | 25| Mn-55  | 55| 54.9380451        |
| Cobalt    | 27| Co-59  | 59| 58.9331950        |
| Arsenic   | 33| As-75  | 75| 74.9215965        |
| Yttrium   | 39| Y-89   | 89| 88.9058403        |
| Niobium   | 41| Nb-93  | 93| 92.9063730        |
| Rhodium   | 45| Rh-103 | 103| 102.905504       |
| Iodine    | 53| I-127  | 127| 126.904473       |
| Cesium    | 55| Cs-133 | 133| 132.905452       |
| Praseodymium | 59| Pr-141 | 141| 140.907653    |
| Terbium   | 65| Tb-159 | 159| 158.925347       |
| Holmium   | 67| Ho-165 | 165| 164.930322       |
| Thulium   | 69| Tm-169 | 169| 168.934213       |
| Gold      | 79| Au-197 | 197| 196.966569       |
| Bismuth   | 83| Bi-209 | 209| 208.980399       |

**MCNP Usage**: For monoisotopic elements, natural ZAID (ZZZ000) and specific isotope ZAID (ZZZAAA) are equivalent.

### Important Multi-Isotope Elements

**Chlorine (Z=17)**:
```
Cl-35: 75.76% (34.9688527 amu)
Cl-37: 24.24% (36.9659026 amu)

Average atomic mass:
A_Cl = 0.7576 × 34.969 + 0.2424 × 36.966 = 35.45 amu

MCNP natural mix:
M1  17000.80c  1.0      $ Natural chlorine

MCNP explicit isotopes:
M1  17035.80c  0.7576   $ Cl-35
    17037.80c  0.2424   $ Cl-37
```

**Boron (Z=5)** - Important for neutron absorption:
```
B-10: 19.9% (10.0129369 amu) - Strong thermal absorber (σ = 3840 b)
B-11: 80.1% (11.0093055 amu)

Average atomic mass:
A_B = 0.199 × 10.013 + 0.801 × 11.009 = 10.81 amu

MCNP for natural boron:
M1  5000.80c  1.0       $ Natural boron

MCNP for B-10 enriched (95%):
M1  5010.80c  0.95      $ B-10 (enriched)
    5011.80c  0.05      $ B-11
```

**Iron (Z=26)**:
```
Fe-54:  5.845% (53.9396090 amu)
Fe-56: 91.754% (55.9349375 amu)
Fe-57:  2.119% (56.9353940 amu)
Fe-58:  0.282% (57.9332756 amu)

Average atomic mass:
A_Fe = 0.05845×53.940 + 0.91754×55.935 + 0.02119×56.935 + 0.00282×57.933
A_Fe = 55.845 amu

MCNP natural iron:
M1  26000.80c  1.0      $ Natural iron (simplest)

MCNP explicit isotopes:
M1  26054.80c  0.05845
    26056.80c  0.91754
    26057.80c  0.02119
    26058.80c  0.00282
```

**Uranium (Z=92)** - Natural vs. enriched:
```
Natural uranium:
  U-234:  0.0054% (234.0409521 amu) - Often ignored
  U-235:  0.7204% (235.0439301 amu) - Fissile
  U-238: 99.2742% (238.0507882 amu) - Fertile

Average atomic mass (with U-234):
A_U = 0.000054×234.041 + 0.007204×235.044 + 0.992742×238.051
A_U = 238.029 amu

MCNP natural uranium:
M1  92000.80c  1.0      $ Natural U (0.72% U-235)

MCNP natural U (explicit, ignoring U-234):
M1  92235.80c  0.0072   $ U-235 (0.72%)
    92238.80c  0.9928   $ U-238 (99.28%)

MCNP LEU (4.5% enriched):
M1  92235.80c  0.045    $ U-235 (4.5%)
    92238.80c  0.955    $ U-238 (95.5%)

MCNP HEU (93% enriched):
M1  92235.80c  0.93     $ U-235 (93%)
    92238.80c  0.07     $ U-238 (7%)
```

## Average Atomic Mass Calculation

### Formula

```
A_avg = Σ (fi × Ai)

where:
  fi = fractional abundance of isotope i
  Ai = atomic mass of isotope i (amu)
  Σ fi = 1.0 (must sum to unity)
```

### Example: Silicon

```
Natural isotopes:
  Si-28: 92.223% (27.9769265 amu)
  Si-29:  4.685% (28.9764947 amu)
  Si-30:  3.092% (29.9737701 amu)

Calculation:
  A_avg = 0.92223 × 27.977 + 0.04685 × 28.976 + 0.03092 × 29.974
  A_avg = 25.798 + 1.357 + 0.927
  A_avg = 28.082 amu

Verification:
  Σ fi = 0.92223 + 0.04685 + 0.03092 = 1.00000 ✓
```

### Example: Enriched Material

**Plutonium (weapons-grade, 93% Pu-239)**:
```
Composition:
  Pu-239: 93.0% (239.0521634 amu)
  Pu-240:  7.0% (240.0538135 amu)

Calculation:
  A_avg = 0.930 × 239.052 + 0.070 × 240.054
  A_avg = 222.318 + 16.804
  A_avg = 239.122 amu

Use 239.12 amu for density calculations
```

## Element-to-ZAID Quick Reference

| Element | Symbol | Z | Natural ZAID | Common Isotope ZAIDs | Notes |
|---------|--------|---|-------------|----------------------|-------|
| Hydrogen | H | 1 | 1000.80c | 1001, 1002 (D), 1003 (T) | H-1 dominant |
| Helium | He | 2 | 2000.80c | 2003, 2004 | He-4 dominant |
| Lithium | Li | 3 | 3000.80c | 3006, 3007 | Li-7 dominant |
| Beryllium | Be | 4 | 4009.80c | 4009 | Monoisotopic |
| Boron | B | 5 | 5000.80c | 5010, 5011 | B-10 for absorption |
| Carbon | C | 6 | 6000.80c | 6012, 6013 | C-12 dominant |
| Nitrogen | N | 7 | 7000.80c | 7014, 7015 | N-14 dominant |
| Oxygen | O | 8 | 8000.80c | 8016, 8017, 8018 | O-16 dominant |
| Fluorine | F | 9 | 9019.80c | 9019 | Monoisotopic |
| Sodium | Na | 11 | 11023.80c | 11023 | Monoisotopic |
| Magnesium | Mg | 12 | 12000.80c | 12024, 12025, 12026 | Three isotopes |
| Aluminum | Al | 13 | 13027.80c | 13027 | Monoisotopic, activation |
| Silicon | Si | 14 | 14000.80c | 14028, 14029, 14030 | Three isotopes |
| Phosphorus | P | 15 | 15031.80c | 15031 | Monoisotopic |
| Chlorine | Cl | 17 | 17000.80c | 17035, 17037 | Two isotopes |
| Argon | Ar | 18 | 18000.80c | 18036, 18038, 18040 | Ar-40 dominant |
| Potassium | K | 19 | 19000.80c | 19039, 19040, 19041 | K-39 dominant, K-40 radioactive |
| Calcium | Ca | 20 | 20000.80c | 20040, 20042, 20043, 20044, 20046, 20048 | Ca-40 dominant |
| Iron | Fe | 26 | 26000.80c | 26054, 26056, 26057, 26058 | Fe-56 dominant |
| Nickel | Ni | 28 | 28000.80c | 28058, 28060, 28061, 28062, 28064 | Five isotopes |
| Copper | Cu | 29 | 29000.80c | 29063, 29065 | Two isotopes |
| Zirconium | Zr | 40 | 40000.80c | 40090, 40091, 40092, 40094, 40096 | Cladding material |
| Molybdenum | Mo | 42 | 42000.80c | 42092, 42094, 42095, 42096, 42097, 42098, 42100 | Seven isotopes |
| Silver | Ag | 47 | 47000.80c | 47107, 47109 | Two isotopes |
| Cadmium | Cd | 48 | 48000.80c | Multiple | Strong absorber |
| Tungsten | W | 74 | 74000.80c | 74180, 74182, 74183, 74184, 74186 | Five isotopes |
| Lead | Pb | 82 | 82000.80c | 82204, 82206, 82207, 82208 | Pb-208 dominant |
| Bismuth | Bi | 83 | 83209.80c | 83209 | Monoisotopic |
| Uranium | U | 92 | 92000.80c | 92234, 92235, 92238 | Natural = 0.72% U-235 |
| Plutonium | Pu | 94 | N/A | 94238, 94239, 94240, 94241, 94242 | No natural, bred in reactor |

## Isotopic Abundance Normalization

### Importance

MCNP requires material fractions to sum to 1.0 (or scale proportionally). Incorrect normalization causes:
- Warning messages
- Automatic renormalization (may not be intended)
- Potential physics errors

### Verification

```
Always check: Σ fi = 1.0000

Example (natural chlorine):
  Cl-35: 0.7576
  Cl-37: 0.2424
  Sum: 0.7576 + 0.2424 = 1.0000 ✓

Example (error):
  Cl-35: 0.76     ← Rounded
  Cl-37: 0.24     ← Rounded
  Sum: 0.76 + 0.24 = 1.00 (appears OK, but lost precision)
```

### Best Practice

```
Use 4-6 significant figures for abundances:

Good:
  M1  17035.80c  0.7576
      17037.80c  0.2424

Better:
  M1  17035.80c  0.757600
      17037.80c  0.242400

Bad:
  M1  17035.80c  0.76      ← Lost precision
      17037.80c  0.24
```

### Enriched Materials

For enriched materials, specify exact composition:

```
LEU (4.5% U-235):
  M1  92235.80c  0.045000   $ U-235 (4.5% exact)
      92238.80c  0.955000   $ U-238 (balance)
  c Verify: 0.045 + 0.955 = 1.000 ✓

Weapons-grade Pu (93% Pu-239):
  M2  94239.80c  0.930000   $ Pu-239 (93% exact)
      94240.80c  0.070000   $ Pu-240 (balance)
  c Verify: 0.930 + 0.070 = 1.000 ✓
```

## Stable vs. Radioactive Isotopes

### Stability Criteria

**Stable**: t₁/₂ = ∞ (effectively stable)
**Long-lived**: t₁/₂ > 10⁸ years (quasi-stable)
**Short-lived**: t₁/₂ < 1 day

### Common Stable Isotopes (by Element)

```
H:  H-1, H-2 (D)
He: He-3, He-4
C:  C-12, C-13
N:  N-14, N-15
O:  O-16, O-17, O-18
Fe: Fe-54, Fe-56, Fe-57, Fe-58
Pb: Pb-204, Pb-206, Pb-207, Pb-208
```

### Long-Lived Radioactive (Primordial)

| Isotope | t₁/₂ (years) | Decay Mode | Found in Nature |
|---------|-------------|------------|-----------------|
| K-40    | 1.25×10⁹    | β⁻, EC     | 0.0117% of natural K |
| Th-232  | 1.41×10¹⁰   | α          | Primordial, 100% of Th |
| U-235   | 7.04×10⁸    | α          | 0.72% of natural U |
| U-238   | 4.47×10⁹    | α          | 99.27% of natural U |

### Selection for MCNP

**For shielding** (t > 100 years):
- Use only stable isotopes
- Exception: Very long-lived if t₁/₂ ≫ analysis timeframe

**For activation**:
- Model short-lived for immediate dose
- Model long-lived for waste characterization

**For criticality**:
- All actinides (U, Pu, Am, etc.)
- Major fission products (Xe-135, Sm-149)
- Stable isotopes for structural materials

## MCNP Material Card Examples

### Natural Element

```
c Natural iron
M1  26000.80c  1.0
c This automatically includes all natural isotopes at correct abundances
```

### Explicit Isotopes

```
c Natural iron (explicit)
M1  26054.80c  0.05845   $ Fe-54 (5.845%)
    26056.80c  0.91754   $ Fe-56 (91.754%)
    26057.80c  0.02119   $ Fe-57 (2.119%)
    26058.80c  0.00282   $ Fe-58 (0.282%)
c Verify: 0.05845 + 0.91754 + 0.02119 + 0.00282 = 1.00000 ✓
```

### Enriched Material

```
c LEU fuel (4.5% enriched UO₂)
c U component:
M1  92235.80c  0.045     $ U-235 (4.5% enriched)
    92238.80c  0.955     $ U-238 (balance)
c O component: (2 oxygen per U)
    8016.80c   2.0       $ O-16
c Fractions are relative within material
```

## Data Sources and References

**Primary Sources**:
- NIST Atomic Weights and Isotopic Compositions (2024)
  https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions
- IAEA Nuclear Data Services
  https://www-nds.iaea.org/
- NNDC (National Nuclear Data Center)
  https://www.nndc.bnl.gov/

**Recommended References**:
- Chart of the Nuclides (Karlsruhe, KAERI)
- Nuclear Wallet Cards (Jagdish K. Tuli)
- ICRP Publication 107 (Nuclear Decay Data)
- AME (Atomic Mass Evaluation) 2020

**MCNP-Specific**:
- MCNP6 User Manual, Appendix H (Atomic Mass Tables)
- xsdir file (specific to installed library)

---

**For ZAID format details, see `zaid_format_guide.md`**
**For cross-section library availability, see `library_availability.md`**
**For decay properties and activation, see `decay_data.md`**
