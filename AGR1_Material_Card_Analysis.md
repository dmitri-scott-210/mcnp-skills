# AGR-1 MATERIAL CARD STRUCTURE ANALYSIS
**Comprehensive Documentation of MCNP Material Definitions**

**Files Analyzed:**
1. `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/bench_138B.i` (385 materials)
2. `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/bench_143A.i` (385 materials)
3. `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/sdr-agr.i` (130 materials)

---

## 1. MATERIAL NUMBERING SCHEMES

### 1.1 ATR Fuel Element Materials (bench_138B.i, bench_143A.i)
**Material Range:** m2106 through m2315 (210 materials)
**Purpose:** Depleted ATR fuel compositions for 10 fuel elements, 3 radial zones, 7 axial zones

**Numbering Convention:**
```
m2XYZ
  X = Element number (1-2)
  Y = Radial zone (1-3)
  Z = Axial zone (1-7)

Examples:
m2106 = Element 6, Radial Zone 1, Axial Zone 1
m2114 = Element 6, Radial Zone 1, Axial Zone 4
m2315 = Element 15, Radial Zone 3, Axial Zone 7
```

### 1.2 AGR-1 TRISO Fuel Materials (all files)
**Material Ranges:**
- **m9111-m9634:** UCO fuel kernels (unique for each compact/capsule/stack)
- **m9090-m9094:** TRISO coating layers (shared across all particles)
  - m9090: Buffer layer (porous carbon)
  - m9091: IPyC (Inner Pyrolytic Carbon)
  - m9092: SiC (Silicon Carbide)
  - m9093: OPyC (Outer Pyrolytic Carbon)
  - m9094: Graphite matrix

**Numbering Convention for Kernels:**
```
m9XYZ
  X = Capsule/position identifier (1-6)
  Y = Stack number (1-3)
  Z = Axial compact level (1-4)
```

### 1.3 Structural and Moderator Materials
**Water-based materials:**
- m10: Pure water (H₂O)
- m14-m16: Beryllium + water mixtures (varying H₂O content)
- m19-m33: Aluminum alloys + water (structural with coolant)

**Solid materials:**
- m17: Helium gas
- m18: Pure beryllium metal
- m38: Stainless Steel 348
- m43-m44: Cobalt + Aluminum targets
- m71: Hafnium (control material)
- m75, m77, m80, m82: Zirconium-hafnium shrouds

**AGR-specific materials:**
- m8900: Air
- m8901: Light water (62°C, 2.5 MPa)
- m8902: Helium coolant
- m9000-m9036: SS316L stainless steel (multiple instances)
- m9040-m9056: Pure graphite spacers
- m9070-m9075: Borated graphite holders
- m9081-m9086: Hafnium shrouds

**Test materials:**
- m621-m632: SE flux trap experiment materials (Zr + Hf + water)
- m711-m714: Support structure materials
- m732, m7410, m7510: Detailed test materials with isotopic specifications

---

## 2. ZAID SELECTIONS AND LIBRARY SUFFIXES

### 2.1 Cross-Section Library Usage

**Primary Libraries:**
- **.70c** - ENDF/B-VII.0 continuous energy (MOST COMMON)
  - Used for: H-1, O-16, C-12, Al-27, most actinides, most fission products
  - Example: `1001.70c`, `8016.70c`, `92235.70c`

- **.60c** - ENDF/B-VI.8 continuous energy
  - Used for: Natural elements (Mg, Si, Ti, Zr, Mo)
  - Example: `12000.60c`, `14000.60c`, `40000.60c`

- **.50c** - ENDF/B-V continuous energy
  - Used for: Natural Cr, Fe, Ni (structural steel isotopes)
  - Example: `24000.50c`, `26000.50c`, `28000.50c`

- **.80c** - ENDF/B-VIII.0 (in AGR materials)
  - Used for: Air constituents
  - Example: `7014.80c`, `8016.80c`

- **.00c** - ENDF/B-VI.0 or earlier (in AGR materials)
  - Used for: Some AGR stainless steel isotopes, graphite, helium
  - Example: `24050.00c`, `6012.00c`, `2004.00c`

- **.20c** - Special evaluations
  - Used for: B-10 in borated graphite
  - Example: `5010.20c`

- **.55c** - Special tungsten evaluation
  - Example: `74000.55c`

### 2.2 Isotopic vs. Natural Element ZAIDs

**Isotopically-resolved materials:**
- **Uranium:** Always isotopic (U-234, U-235, U-236, U-237, U-238)
- **Plutonium:** Always isotopic (Pu-239, Pu-240, Pu-241)
- **Fission Products:** Specific isotopes (Kr-83, Xe-131, Xe-133, Cs-133, Sm-149, etc.)
- **Carbon:** C-12 and C-13 explicitly specified in TRISO/graphite
- **Silicon:** Si-28, Si-29, Si-30 in SiC coating
- **Boron:** B-10 and B-11 in borated graphite and burnable poisons
- **Stainless Steel (SS316L):** Isotopic Cr, Fe, Ni, Mo

**Natural element ZAIDs (ZZZAAA = ZZZ000):**
- **Structural:** Cr (24000), Fe (26000), Ni (28000), Cu (29000)
- **Light elements:** Mg (12000), Si (14000), Ti (22000)
- **Heavy elements:** Zr (40000), Mo (42000), Hf (72000)

---

## 3. DENSITY SPECIFICATIONS

### 3.1 Atom Density Format (atoms/barn-cm)

**ATR Fuel Elements (m2106-m2315):**
```mcnp
m2106
    1001.70c  3.393340E-02  $ H-1
    8016.70c  1.696670E-02  $ O-16
   12000.60c  2.176490E-04  $ Mg-nat
   13027.70c  2.793720E-02  $ Al-27
   14000.60c  1.130110E-04  $ Si-nat
   24000.50c  2.304760E-05  $ Cr-nat
   29000.50c  2.081160E-05  $ Cu-nat
    5010.70c  4.522560E-06  $ B-10 (burnable poison)
   92234.70c  5.873407E-06  $ U-234
   92235.70c  4.198373E-04  $ U-235
   92236.70c  1.517056E-05  $ U-236
   92237.70c  1.326253E-07  $ U-237
   92238.70c  3.057844E-05  $ U-238
   93237.70c  1.886031E-07  $ Np-237
   94239.70c  3.962382E-07  $ Pu-239
   [... fission products ...]
mt2106    lwtr.10t
```

**Cell card density:** Specified separately in cell definition
```mcnp
60106 2106 7.969921E-02  1111  -1118  74  -29  53  100 -110
      ^^^^
      Total atom density (atoms/barn-cm)
```

**CRITICAL PATTERN:** Material card contains isotopic FRACTIONS (sum to ~1.0), cell card contains TOTAL density.

### 3.2 Mass Density Format (g/cm³)

**Stainless Steel SS316L (m9000):**
```mcnp
c ss316l, density = 8.03 g/cm3
m9000
   24050.00c -0.00653131  $ Cr-50 (negative = weight fraction)
   24052.00c -0.14263466  $ Cr-52
   24053.00c -0.01730730  $ Cr-53
   24054.00c -0.00352673  $ Cr-54
   25055.00c -0.02000000  $ Mn-55
   26054.00c -0.03799186  $ Fe-54
   26056.00c -0.60409084  $ Fe-56 (major component)
   26057.00c -0.01336731  $ Fe-57
   28058.00c -0.08053185  $ Ni-58
   [... continues ...]
```

**Cell card with mass density:**
```mcnp
92000 9002 -8.03  -97064  98010 -98011  vol=6.179954  $ bottom support: ss316L
          ^^^^^
          Negative density = g/cm³, uses mass fractions from material card
```

**CRITICAL PATTERN:** Negative sign on density triggers mass density mode. Material card fractions must sum to 1.0 (or close).

### 3.3 UCO Fuel Kernel Special Case

**UCO Kernel (m9111):**
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

**Cell card:**
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel
```

**INTERPRETATION:** The values appear to be ATOM RATIOS or STOICHIOMETRIC COEFFICIENTS, not fractions. The negative density in cell card (-10.924 g/cm³) indicates MCNP should interpret these as relative atom counts and normalize internally.

**Chemical formula implied:** UC₀.₃₂₅O₁.₃₆ (approximate UCO composition)

---

## 4. MATERIAL COMPOSITION PATTERNS

### 4.1 ATR Fuel Composition (Depleted U-Al Dispersion Fuel)

**Base composition:**
- **Fuel meat:** U-Al alloy dispersed in aluminum matrix
- **Cladding:** Aluminum alloy (Al-6061)
- **Coolant/moderator:** Light water

**Burn-up tracking:**
Each of 210 materials (m2106-m2315) has unique isotopic composition reflecting:
1. **Initial enrichment:** ~93% U-235 (HEU fuel)
2. **Burn-up state:** Variable U-235 depletion, Pu build-up, fission product inventory
3. **Position dependence:** Radial and axial power distribution effects

**Key isotopes tracked:**
- **Actinides:** U-234/235/236/237/238, Np-237, Pu-239/240/241
- **Fission Products:** Kr-83, Mo-95, Ru-101, Rh-103/105, Cd-113, Xe-131/133/135, Cs-133, La-140, Ce-141, Pr-143, Nd-143/145, Pm-147/149/151, Sm-149/151/152, Eu-153/155, Gd-157
- **Burnable Poison:** B-10 (explicitly tracked)

**Peculiarity:** Some fission products have extremely low densities (e.g., `7.425954E-31` for Rh-105), indicating radioactive decay to negligible levels.

### 4.2 TRISO Fuel Structure (AGR-1 Specific)

**Five-layer coating structure:**

```
┌─────────────────────────────────────────┐
│  Matrix (m9094)                         │
│  ┌─────────────────────────────────┐    │
│  │ OPyC (m9093, ρ=1.901 g/cm³)    │    │
│  │ ┌─────────────────────────────┐ │    │
│  │ │ SiC (m9092, ρ=3.207 g/cm³) │ │    │
│  │ │ ┌─────────────────────────┐ │ │    │
│  │ │ │ IPyC (m9091, 1.912)    │ │ │    │
│  │ │ │ ┌─────────────────────┐ │ │ │    │
│  │ │ │ │ Buffer (m9090, 1.1)│ │ │ │    │
│  │ │ │ │ ┌─────────────────┐ │ │ │ │    │
│  │ │ │ │ │ UCO Kernel     │ │ │ │ │    │
│  │ │ │ │ │ (m911X series) │ │ │ │ │    │
│  │ │ │ │ │ ρ=10.924 g/cm³ │ │ │ │ │    │
│  │ │ │ │ └─────────────────┘ │ │ │ │    │
│  │ │ │ └─────────────────────┘ │ │ │    │
│  │ │ └─────────────────────────┘ │ │    │
│  │ └─────────────────────────────┘ │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Layer compositions:**

1. **UCO Kernel (m9111-m9634):**
   - Uranium isotopes: U-234 (0.334%), U-235 (19.96%), U-236 (0.019%), U-238 (79.68%)
   - Carbon: C-12, C-13
   - Oxygen: O-16
   - Density: 10.924 g/cm³
   - Formula: ~UC₀.₃₂₅O₁.₃₆

2. **Buffer Layer (m9090):**
   - Pure porous carbon: C-12 (98.90%), C-13 (1.10%)
   - Density: 1.10 g/cm³
   - Purpose: Accommodation of fission gas and fuel swelling

3. **IPyC - Inner Pyrolytic Carbon (m9091):**
   - Pure carbon: C-12 (98.90%), C-13 (1.10%)
   - Density: 1.912 g/cm³ (variant densities: 1.853-1.912)
   - Purpose: Protects SiC from fission products, provides structural support

4. **SiC - Silicon Carbide (m9092):**
   - Silicon: Si-28 (92.20%), Si-29 (4.70%), Si-30 (3.10%)
   - Carbon: C-12 (98.90%), C-13 (1.10%)
   - Density: 3.207 g/cm³ (variant densities: 3.205-3.208)
   - Purpose: Primary fission product retention barrier, pressure vessel

5. **OPyC - Outer Pyrolytic Carbon (m9093):**
   - Pure carbon: C-12 (98.90%), C-13 (1.10%)
   - Density: 1.901 g/cm³ (variant densities: 1.898-1.911)
   - Purpose: Protects SiC from chemical attack, provides bonding surface

6. **Matrix (m9094):**
   - Pure carbon: C-12 (98.90%), C-13 (1.10%)
   - Density: 1.256 g/cm³ (variant densities: 1.219-1.344)
   - Purpose: Binds TRISO particles into fuel compact

**Variants:** Comments indicate "baseline" and "variant1/2/3" densities for quality assurance and parametric studies.

### 4.3 Structural Materials

**Stainless Steel 348 (m38):**
```mcnp
c SSTL 348  (8.71157-2 atoms/barn-cm)
m38
    6000.70c  3.20084-4   $ C
   14000.60c  1.28331-3   $ Si
   15031.70c  6.20611-5   $ P-31
   16032.70c  4.49604-5   $ S-32
   24000.50c  1.84847-2   $ Cr
   25055.70c  1.74949-3   $ Mn-55
   26000.50c  4.94791-2   $ Fe
   28000.50c  1.51482-2   $ Ni
   41093.70c  5.17259-4   $ Nb-93
   73181.60c  2.65583-5   $ Ta-181
```

**SS316L (m9000-m9036) - Isotopically detailed:**
```mcnp
c ss316l, density = 8.03 g/cm3
m9000
   24050.00c -0.00653131  $ Cr-50
   24052.00c -0.14263466  $ Cr-52
   24053.00c -0.01730730  $ Cr-53
   24054.00c -0.00352673  $ Cr-54
   25055.00c -0.02000000  $ Mn-55
   26054.00c -0.03799186  $ Fe-54
   26056.00c -0.60409084  $ Fe-56 (dominates)
   26057.00c -0.01336731  $ Fe-57
   28058.00c -0.08053185  $ Ni-58
   28060.00c -0.03185216  $ Ni-60
   28061.00c -0.00124553  $ Ni-61
   28062.00c -0.00506366  $ Ni-62
   28064.00c -0.00130679  $ Ni-64
   42092.00c -0.00354458  $ Mo-92
   42094.00c -0.00220235  $ Mo-94
   42095.00c -0.00395701  $ Mo-95
   42096.00c -0.00424858  $ Mo-96
   42097.00c -0.00239899  $ Mo-97
   42098.00c -0.00612312  $ Mo-98
   42100.00c -0.00252537  $ Mo-100
```

**Aluminum 6061 (m30, m712):**
```mcnp
c Aluminum-6061  (6.02136-2 atoms/barn-cm)
m30
   13027.70c  5.90699-2   $ Al-27 (98.9%)
   24000.50c  6.25887-5   $ Cr
   14000.60c  3.47620-4   $ Si
   12000.60c  6.69484-4   $ Mg
   29000.50c  6.40160-5   $ Cu
```

**Hafnium (Control Material, m71):**
```mcnp
c Hafnium (4.55926e-02 atoms/barn-cm)
m71
    1001.70c  3.91044e-05  $ H-1 (trace)
    6012.50c  4.59419e-05  $ C-12 (trace)
    7014.70c  1.74468e-05  $ N-14 (trace)
   13027.70c  1.46081e-05  $ Al-27 (trace)
   22000.60c  8.23201e-06  $ Ti (trace)
   29000.50c  6.20258e-06  $ Cu (trace)
   40000.60c  2.67882e-03  $ Zr (alloying element)
   41093.70c  4.24243e-06  $ Nb-93 (trace)
   42000.60c  8.21657e-07  $ Mo (trace)
   72000.60c  4.27740e-02  $ Hf ← PRIMARY ISOTOPE (93.8%)
   74000.55c  3.21579e-06  $ W (trace)
```
**Purpose:** Neutron absorber for reactivity control. Natural hafnium includes strong absorbers like Hf-177.

**Hafnium Shroud (m9081-m9086) - Isotopically detailed:**
```mcnp
c hafnium shroud
m9081
    8016.00c  1.3500E-4   $ O-16
    6012.00c  4.4300E-5   $ C-12
   14028.00c  6.3341E-6   $ Si-28
   14029.00c  3.2289E-7   $ Si-29
   14030.00c  2.1297E-7   $ Si-30
   40090.00c  1.0169E-3   $ Zr-90
   40091.00c  2.2288E-4   $ Zr-91
   40092.00c  3.4029E-4   $ Zr-92
   40094.00c  3.4626E-4   $ Zr-94
   40096.00c  5.5719E-5   $ Zr-96
   72174.00c  6.7512E-5   $ Hf-174
   72176.00c  2.1934E-3   $ Hf-176
   72177.00c  7.8473E-3   $ Hf-177 ← STRONG ABSORBER
   72178.00c  1.1431E-2   $ Hf-178 (most abundant)
   72179.00c  5.7955E-3   $ Hf-179
   72180.00c  1.4845E-2   $ Hf-180
```

### 4.4 Moderator and Coolant Materials

**Water (m10):**
```mcnp
c Water (1.00276e-01 atoms/barn-cm total)
m10
    8016.70c  3.34253-2   $ O-16
    1001.70c  6.68506-2   $ H-1 (2:1 ratio)
mt10  lwtr.10t            $ Light water thermal scattering
```

**Light Water at Operating Conditions (m8901):**
```mcnp
c light water, 62 C, 2.5 MPa, density ~= 0.9853 g/cm3
m8901
    1001.00c  2  $ H-1 (atom ratio, not density)
    8016.00c  1  $ O-16
```
**Note:** Uses simple 2:1 atom ratio. Density specified in cell card accounts for temperature/pressure.

**Helium Coolant (m8902, m17):**
```mcnp
c helium, NT = 1.24931E-04 a/b/cm
m8902
    2004.00c  1  $ He-4
```

**Beryllium Reflector (m18):**
```mcnp
c Beryllium (1.23621-1 atoms/barn-cm)
m18
    4009.60c  1.23621-1  $ Be-9
mt18  be.01t             $ Beryllium metal thermal scattering
```

**Be + H₂O Mixtures (m14-m16, m19-m20):**
```mcnp
c Medium I hole Be + H2O (1.22430-1 atoms/barn-cm)
m14
    1001.70c  3.40940-3   $ H-1
    8016.70c  1.70470-3   $ O-16
    4009.60c  1.17316-1   $ Be-9 (95.8%)
mt14  lwtr.10t  be.01t    $ DUAL thermal scattering
```
**Key feature:** MT card specifies BOTH lwtr.10t and be.01t for mixed thermal scattering treatment.

### 4.5 Graphite Materials

**Pure Graphite Spacers (m9040-m9056):**
```mcnp
c pure graphite (lower spacer) density = 1.015 g/cm3
m9040
    6012.00c  0.9890  $ C-12 (98.90%)
    6013.00c  0.0110  $ C-13 (1.10%)
```
**Cell usage:**
```mcnp
91001 9041 -1.015  -97060  98004 -98005  vol=5.027315  $ lower graphite spacer
```

**Borated Graphite Holders (m9070-m9075):**
```mcnp
c borated graphite holder, 4.76 atom percent boron, 1.7695 g/cm3, capsule 1,6
m9070
    6012.00c  8.4900E-2   $ C-12 (base matrix)
    5010.20c  8.4496E-4   $ B-10 (19.8% of boron)
    5011.00c  3.4003E-3   $ B-11 (80.2% of boron)
```
Total B concentration: 4.25E-3 atoms/barn-cm → 4.76 atom% in C+B mixture.

```mcnp
c borated graphite holder, 6.05 atom percent boron, 1.7788 g/cm3, capsule 2-5
m9072
    6012.00c  8.4300E-2   $ C-12
    5010.20c  1.0804E-3   $ B-10 (higher loading)
    5011.00c  4.3476E-3   $ B-11
```
Total B concentration: 5.43E-3 atoms/barn-cm → 6.05 atom% in C+B mixture.

**Purpose:** Burnable poison for reactivity control and power shaping in AGR-1 test.

### 4.6 Special Test Materials

**Test Material 1 (m732) - Detailed isotopic specification:**
```mcnp
c Test material 1  (7.48430e-02 atoms/barn-cm)
m732
    1001.70c  3.64953e-02  $ H-1
    1002.70c  5.47512e-06  $ H-2 (deuterium, natural abundance)
    6000.70c  5.32292e-05  $ C
    7014.70c  1.31734e-05  $ N-14
    7015.70c  4.88373e-08  $ N-15 (natural abundance)
    8016.70c  1.82429e-02  $ O-16
    8017.70c  7.30008e-06  $ O-17 (natural abundance)
   12000.60c  2.93842e-05  $ Mg
   13027.70c  2.17096e-03  $ Al-27
   14000.60c  1.67916e-04  $ Si
   15031.70c  6.32925e-06  $ P-31
   16000.60c  4.68259e-06  $ S
   22000.60c  3.44557e-05  $ Ti
   24000.50c  4.33917e-03  $ Cr
   25055.70c  1.48419e-04  $ Mn-55
   26000.50c  4.12504e-03  $ Fe
   27059.70c  6.65141e-05  $ Co-59
   28000.50c  8.89432e-03  $ Ni
   29000.50c  3.80863e-06  $ Cu
   30000.70c  2.27521e-06  $ Zn
   40000.60c  2.69164e-05  $ Zr
   92235.70c  5.37608e-06  $ U-235 ← TRACE CONTAMINATION
```

**Interpretation:** Complex stainless steel + water mixture with trace uranium contamination (possibly from fuel handling or cross-contamination). Includes rare isotopes (H-2, O-17, N-15) at natural abundances.

---

## 5. THERMAL SCATTERING (MT CARDS)

### 5.1 Thermal Scattering Usage Summary

**bench_138B.i:**
- **210 MT cards** for water thermal scattering (lwtr.10t)
- **15 MT cards** for mixed water + beryllium (lwtr.10t + be.01t)
- **1 MT card** for pure beryllium (be.01t)
- **ZERO MT cards** for graphite (grph.10t)

**sdr-agr.i:**
- **ZERO MT cards** (no thermal scattering treatments)

### 5.2 Light Water Thermal Scattering

**Library:** lwtr.10t (Light Water at Room Temperature, ENDF/B-VII.0)

**Applied to:**
- All ATR fuel materials (m2106-m2315)
- Water-based coolant/moderator (m10)
- Water + structural mixtures (m14-m33)

**Example:**
```mcnp
m10
    8016.70c  3.34253-2
    1001.70c  6.68506-2
mt10  lwtr.10t
```

**Critical omission:** No temperature-dependent water libraries (lwtr.01t through lwtr.20t) despite operating at elevated temperatures. This may introduce small errors in thermal neutron scattering.

### 5.3 Beryllium Thermal Scattering

**Library:** be.01t (Beryllium metal, room temperature)

**Applied to:**
- Pure beryllium (m18)
- Beryllium + water mixtures (m14-m16, m19-m20)

**Example:**
```mcnp
m18
    4009.60c  1.23621-1
mt18  be.01t
```

**Dual thermal scattering:**
```mcnp
m14
    1001.70c  3.40940-3
    8016.70c  1.70470-3
    4009.60c  1.17316-1
mt14  lwtr.10t  be.01t  $ Both H₂O and Be scattering
```

### 5.4 Graphite Thermal Scattering - CRITICAL OMISSION

**Expected library:** grph.10t (graphite thermal scattering)

**Observed:** NONE in any of the three files.

**Materials affected:**
- m9040-m9056: Pure graphite spacers
- m9070-m9075: Borated graphite holders
- m9090-m9094: TRISO coating layers (Buffer, IPyC, SiC, OPyC, Matrix)

**Impact:**
- **Low-energy neutron transport:** Free gas scattering model used instead of proper graphite crystal lattice scattering
- **Temperature effects:** No Doppler broadening or temperature-dependent scattering
- **Reactivity:** Underestimation of thermal neutron scattering cross-sections
- **Spectrum:** Harder thermal spectrum than physical reality

**Best practice recommendation:** Add MT cards for all graphite-containing materials:
```mcnp
mt9040  grph.10t
mt9041  grph.10t
mt9090  grph.10t
mt9091  grph.10t
mt9092  grph.10t  $ Even for SiC (carbon component)
mt9093  grph.10t
mt9094  grph.10t
```

---

## 6. CROSS-REFERENCING: MATERIALS TO CELLS

### 6.1 ATR Fuel Elements (bench_138B.i)

**Pattern:** Direct one-to-one mapping between cell number and material number.

```mcnp
Cell       Material   Density         Geometry
----       --------   -------         --------
60106  →   m2106      7.969921E-02    Element 6, Radial Zone 1, Axial Zone 1
60107  →   m2107      7.967400E-02    Element 6, Radial Zone 1, Axial Zone 2
60108  →   m2108      7.965632E-02    Element 6, Radial Zone 1, Axial Zone 3
...
60315  →   m2315      [density]       Element 15, Radial Zone 3, Axial Zone 7
```

**Total:** 210 cells, 210 unique materials (no material reuse).

**Density variation:** Ranges from 7.86E-02 to 8.29E-02 atoms/barn-cm due to burn-up effects (density increases with fission product build-up, decreases with U-235 depletion).

### 6.2 AGR-1 TRISO Fuel (sdr-agr.i)

**Hierarchical structure:**

1. **Kernel cells (91101, 91121, etc.):**
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel
      ^^^^
      Unique material per particle/compact
```

2. **TRISO coating cells (shared materials):**
```mcnp
92102 9090 -1.100  92111 -92112  u=2114  $ Buffer
92103 9091 -1.912  92112 -92113  u=2114  $ IPyC
92104 9092 -3.207  92113 -92114  u=2114  $ SiC
92105 9093 -1.901  92114 -92115  u=2114  $ OPyC
92106 9094 -1.256  92115         u=2114  $ Matrix
      ^^^^
      SAME materials (m9090-m9094) for ALL particles
```

3. **Lattice fill:**
```mcnp
92108 0  -92117  u=2116  lat=1  fill=-7:7 -7:7 0:0 [...]
                                  Repeated structure
```

**Material reuse factor:**
- **Kernels:** Each compact has unique m911X material
- **Coatings:** Only 5 materials (m9090-m9094) used for ALL ~150,000 particles
- **Graphite:** 6 pairs of spacers (m9040-m9056), 6 borated holders (m9070-m9075)

### 6.3 Structural Material Reuse

**Single-use materials (no reuse):**
- ATR fuel (m2106-m2315): Each material → one cell only

**Heavily reused materials:**
- m10 (water): Used in dozens of coolant channel cells
- m18 (beryllium): Used in all beryllium reflector cells
- m30 (Al-6061): Used in multiple structural components
- m9000-m9036 (SS316L): Nominally identical, separate numbers for different geometric regions
- m9040-m9056 (graphite spacers): Upper and lower spacers for 6 capsules

**Reuse pattern for SS316L:**
```mcnp
m9000  → Capsule 1 structural component
m9001  → Capsule 1 different component
m9002  → Capsule 1 another component
m9003  → Capsule 2 structural component
...
```
**Rationale:** Identical compositions but separate material numbers for:
- Easier post-processing (tally by component)
- Potential future material variations (different densities, burn-up)
- Clear documentation/traceability

### 6.4 Thermal Scattering Cross-Reference

**Material → MT Card Mapping:**

| Material Range | MT Card | S(α,β) Library | Comments |
|----------------|---------|----------------|----------|
| m2106-m2315    | mt2106-mt2315 | lwtr.10t | ATR fuel + water |
| m10, m21-m33   | mt10, mt21-mt33 | lwtr.10t | Pure water or water mixtures |
| m14-m16, m19-m20 | mt14-mt16, mt19-mt20 | lwtr.10t + be.01t | Mixed Be + H₂O |
| m18            | mt18 | be.01t | Pure beryllium |
| m9040-m9094    | NONE | (none) | **MISSING graphite S(α,β)** |

---

## 7. DENSITY CALCULATION APPROACHES

### 7.1 Direct Specification (Most Common)

**Method:** Atom density directly provided for each isotope in material card.

**ATR Fuel Example (m2106):**
```mcnp
m2106
    1001.70c  3.393340E-02  $ atoms/barn-cm
    8016.70c  1.696670E-02
   13027.70c  2.793720E-02
   92235.70c  4.198373E-04
   [...]
```

**Cell specification:**
```mcnp
60106 2106 7.969921E-02  [geometry]
           ^^^^^^^^^^^^
           Total density (sum of all isotopes)
```

**Calculation check:**
```
H:   3.393340E-02
O:   1.696670E-02
Mg:  2.176490E-04
Al:  2.793720E-02
Si:  1.130110E-04
[... all isotopes ...]
-------------------------
Sum: 7.969921E-02 atoms/barn-cm ✓ (matches cell card)
```

### 7.2 Fractional Specification + Cell Density

**Method:** Material card has fractions (sum to 1.0), cell card provides total density.

**Graphite Example (m9040):**
```mcnp
m9040
    6012.00c  0.9890  $ fraction
    6013.00c  0.0110  $ fraction
                      $ sum = 1.0000
```

**Cell specification:**
```mcnp
91001 9041 -1.015  [geometry]
           ^^^^^^
           Mass density (g/cm³)
```

**MCNP calculation:**
```
ρ_mass = 1.015 g/cm³
M_avg = 0.9890×12.000 + 0.0110×13.003 = 12.011 g/mol
ρ_atom = ρ_mass × N_A / M_avg
       = 1.015 × 6.022E23 / 12.011
       = 5.086E22 atoms/cm³
       = 0.08442 atoms/barn-cm

N(C-12) = 0.9890 × 0.08442 = 0.08349 atoms/barn-cm
N(C-13) = 0.0110 × 0.08442 = 0.00093 atoms/barn-cm
```

### 7.3 Mass Fraction + Cell Density (SS316L)

**Method:** Material card has mass fractions (negative sign, sum to 1.0), cell has mass density.

**SS316L Example (m9000):**
```mcnp
m9000
   26056.00c -0.60409084  $ mass fraction (60.4% Fe-56)
   24052.00c -0.14263466  $ mass fraction (14.3% Cr-52)
   28058.00c -0.08053185  $ mass fraction (8.1% Ni-58)
   [...]
```

**Cell specification:**
```mcnp
92000 9002 -8.03  [geometry]
           ^^^^^
           Negative = mass density (g/cm³)
```

**MCNP calculation for each isotope:**
```
For Fe-56:
w_Fe56 = 0.60409084 (mass fraction)
ρ_mat = 8.03 g/cm³
A_Fe56 = 55.934937 u
N_Fe56 = (w_Fe56 × ρ_mat × N_A) / A_Fe56
       = (0.60409084 × 8.03 × 6.022E23) / 55.934937
       = 5.217E22 atoms/cm³
       = 0.08659 atoms/barn-cm
```

### 7.4 Stoichiometric Ratios (UCO Kernel)

**Method:** Material card has atom ratios, cell has mass density, MCNP normalizes.

**UCO Kernel Example (m9111):**
```mcnp
m9111
   92235.00c  1.99636E-01  $ atom ratio
   92238.00c  7.96829E-01  $ atom ratio
    6012.00c  0.3217217    $ atom ratio
    8016.00c  1.3613       $ atom ratio (>1.0!)
```

**Cell specification:**
```mcnp
91101 9111 -10.924  [geometry]
           ^^^^^^^
           Mass density (g/cm³)
```

**MCNP internal calculation:**
```
Total atom ratio sum: 0.19964 + 0.79683 + 0.32172 + 1.3613 = 2.68 (not 1.0!)

Step 1: Calculate average molecular weight
M_avg = Σ(ratio_i × A_i) / Σ(ratio_i)
      = (0.19964×235 + 0.79683×238 + 0.32172×12 + 1.3613×16) / 2.68
      = (46.92 + 189.6 + 3.86 + 21.78) / 2.68
      = 262.16 / 2.68
      = 97.8 g/mol

Step 2: Calculate total atom density
N_total = ρ × N_A / M_avg
        = 10.924 × 6.022E23 / 97.8
        = 6.724E22 atoms/cm³
        = 0.1116 atoms/barn-cm

Step 3: Normalize atom ratios
N(U-235) = (0.19964 / 2.68) × 0.1116 = 0.00831 atoms/barn-cm
N(U-238) = (0.79683 / 2.68) × 0.1116 = 0.03318 atoms/barn-cm
N(C-12)  = (0.32172 / 2.68) × 0.1116 = 0.01340 atoms/barn-cm
N(O-16)  = (1.3613  / 2.68) × 0.1116 = 0.05670 atoms/barn-cm
```

**Chemical formula verification:**
```
U atoms: 0.00831 + 0.03318 = 0.04149
C atoms: 0.01340
O atoms: 0.05670

Ratio U:C:O = 1 : 0.323 : 1.367
Formula: UC₀.₃₂₃O₁.₃₆₇ ≈ UC₀.₃₂O₁.₃₆
```

This matches expected UCO (Uranium Carbide-Oxide) stoichiometry!

---

## 8. NOTABLE PATTERNS AND BEST PRACTICES

### 8.1 Material Numbering Best Practices

✅ **Good practices observed:**
1. **Systematic numbering:** m2106-m2315 for ATR fuel (element/zone/level encoded)
2. **Grouped materials:** m9000-m9036 (SS316L), m9040-m9056 (graphite)
3. **Functional grouping:** m9090-m9094 (TRISO coatings)
4. **Reserved ranges:** Leaves room for expansion

❌ **Potential improvements:**
1. **Non-sequential gaps:** m71, m75, m77, m80, m82 (could be m71-m75)
2. **Inconsistent prefixes:** m621-m632 vs. m711-m714 vs. m732
3. **Mixed numbering schemes:** ATR uses m2XXX, AGR uses m9XXX

### 8.2 Cross-Section Library Selection

✅ **Good practices:**
1. **Consistent library version:** Mostly .70c (ENDF/B-VII.0) throughout
2. **Isotopic actinides:** All U, Pu, Np isotopes explicitly specified
3. **Special evaluations:** B-10 uses .20c (optimized thermal evaluation)

❌ **Inconsistencies:**
1. **Mixed ENDF versions:** .00c, .50c, .60c, .70c, .80c in same input
2. **Natural vs. isotopic:** Fe uses 26000.50c in m38, but isotopic (26054/56/57.00c) in m9000
3. **Library availability:** Some .00c ZAIDs may not be in all MCNP distributions

### 8.3 Thermal Scattering Best Practices

✅ **Good usage:**
1. **Dual S(α,β):** lwtr.10t + be.01t for Be+H₂O mixtures
2. **Consistent application:** All water materials have lwtr.10t

❌ **Critical omissions:**
1. **No graphite S(α,β):** Despite ~50 graphite-containing materials
2. **No temperature-dependent S(α,β):** Using room-temperature libraries for 300°C+ operation
3. **No SiC S(α,β):** SiC has both Si and C components, only free-gas scattering used

**Recommended additions:**
```mcnp
mt9040  grph.10t  $ or grph.18t for 600K
mt9041  grph.10t
mt9070  grph.10t  $ borated graphite still needs C scattering
mt9071  grph.10t
mt9090  grph.10t  $ buffer layer
mt9091  grph.10t  $ IPyC
mt9092  grph.10t  $ SiC carbon component
mt9093  grph.10t  $ OPyC
mt9094  grph.10t  $ matrix
mt10    lwtr.11t  $ 325K instead of lwtr.10t (294K)
```

### 8.4 Density Specification Best Practices

✅ **Clear specification:**
1. **Commented densities:** `c density = 8.03 g/cm3` before material card
2. **Consistent units:** Atom density in atoms/barn-cm clearly distinguished from g/cm³
3. **Traceable sources:** Comments indicate element number, zone, burn-up state

❌ **Potential confusion:**
1. **Mixed modes:** Some materials use fractions (sum to 1), others use direct densities
2. **UCO atom ratios:** Values >1.0 without explanation of normalization
3. **Natural element densities:** e.g., `4009.60c 1.23621-1` looks like density but is actually ZAID.library + density

### 8.5 Burn-up Material Tracking

✅ **Excellent practice (ATR fuel):**
1. **Unique materials:** 210 separate materials for depleted fuel compositions
2. **Complete fission product tracking:** 25+ fission product isotopes per material
3. **Actinide chains:** U-234/235/236/237/238, Np-237, Pu-239/240/241

**Example fission product detail:**
```mcnp
   36083.70c  2.749474E-07  $ Kr-83  (stable)
   54131.70c  9.237888E-07  $ Xe-131 (stable)
   54135.70c  5.732034E-31  $ Xe-135 (near-zero, short t₁/₂)
   55133.70c  2.445752E-06  $ Cs-133 (stable)
   62149.70c  2.657344E-08  $ Sm-149 (strong absorber)
   64157.70c  1.440627E-10  $ Gd-157 (strongest absorber)
```

❌ **Limitations:**
1. **No Pu-242, Pu-243, Am, Cm:** Higher actinides not tracked
2. **Limited FP detail:** Only ~25 FPs, but ~200+ fission products exist
3. **Trace isotope treatment:** Some FPs have densities like 5.23E-31 (negligible, could be omitted)

### 8.6 Material Reuse Strategy

✅ **Efficient reuse (AGR-1):**
- 5 TRISO coating materials serve 150,000+ particles
- Graphite spacer materials (m9040-m9056) reused across capsules

❌ **Inefficient duplication (SS316L):**
- 37 identical SS316L materials (m9000-m9036)
- Could use single m9000 with multiple cell references

**Trade-off:** Duplicate materials allow component-specific tallies but increase input file size.

---

## 9. COMPLEX MATERIAL EXAMPLES

### 9.1 ATR Depleted Fuel (Element 6, RZ1, AZ1)

**Material m2106 - Complete Specification:**

```mcnp
c            ATR Element No. =  6
c            Radial Zone No. =  1
c            Axial  Zone No. =  1
c            Neutron Cross Sections = 27 C
c            Total Number Density   = 7.969921E-02 a/b-cm
m2106
             1001.70c  3.393340E-02  $ H-1  (hydrogen in water)
             8016.70c  1.696670E-02  $ O-16 (oxygen in water)
            12000.60c  2.176490E-04  $ Mg-nat (cladding/matrix)
            13027.70c  2.793720E-02  $ Al-27 (matrix/cladding)
            14000.60c  1.130110E-04  $ Si-nat (impurity)
            24000.50c  2.304760E-05  $ Cr-nat (structural alloy)
            29000.50c  2.081160E-05  $ Cu-nat (impurity)
             5010.70c  4.522560E-06  $ B-10 (burnable poison)
            92234.70c  5.873407E-06  $ U-234 (0.15% of U)
            92235.70c  4.198373E-04  $ U-235 (10.7% of U, depleted)
            92236.70c  1.517056E-05  $ U-236 (0.39% of U, from capture)
            92237.70c  1.326253E-07  $ U-237 (transient, β→ Np-237)
            92238.70c  3.057844E-05  $ U-238 (0.78% of U, natural tail)
            93237.70c  1.886031E-07  $ Np-237 (from U-237 decay)
            94239.70c  3.962382E-07  $ Pu-239 (from U-238 + n)
            94240.70c  3.184477E-08  $ Pu-240 (from Pu-239 + n)
            94241.70c  1.038741E-08  $ Pu-241 (from Pu-240 + n)
            36083.70c  2.749474E-07  $ Kr-83 (fission product)
            42095.70c  9.415301E-08  $ Mo-95 (fission product)
            44101.70c  2.720314E-06  $ Ru-101 (fission product)
            45103.70c  3.635464E-07  $ Rh-103 (fission product)
            45105.70c  7.425954E-31  $ Rh-105 (FP, essentially decayed)
            48113.70c  7.621751E-10  $ Cd-113 (FP, neutron absorber)
            54131.70c  9.237888E-07  $ Xe-131 (FP, stable)
            54133.70c  5.861527E-31  $ Xe-133 (FP, decayed)
            55133.70c  2.445752E-06  $ Cs-133 (FP, stable)
            54135.70c  5.732034E-31  $ Xe-135 (FP, decayed)
            57140.70c  5.568047E-31  $ La-140 (FP, decayed)
            58141.70c  5.528633E-31  $ Ce-141 (FP, decayed)
            59143.70c  5.451170E-31  $ Pr-143 (FP, decayed)
            60143.70c  1.325206E-06  $ Nd-143 (FP, stable)
            60145.70c  2.037404E-06  $ Nd-145 (FP, stable)
            61147.70c  5.302593E-31  $ Pm-147 (FP, decayed)
            61149.70c  5.231266E-31  $ Pm-149 (FP, decayed)
            62149.70c  2.657344E-08  $ Sm-149 (FP, STRONG absorber)
            61151.70c  5.161789E-31  $ Pm-151 (FP, decayed)
            62151.70c  7.853828E-08  $ Sm-151 (FP, absorber)
            62152.70c  2.482928E-07  $ Sm-152 (FP)
            63153.70c  1.027083E-07  $ Eu-153 (FP, absorber)
            63155.70c  1.247127E-08  $ Eu-155 (FP, absorber)
            64157.70c  1.440627E-10  $ Gd-157 (FP, STRONGEST absorber)
mt2106      lwtr.10t
```

**Cell reference:**
```mcnp
60106 2106 7.969921E-02  1111 -1118  74 -29  53  100 -110
      ^^^^
      Material assignment
```

**Physics interpretation:**
1. **Original fuel:** HEU (~93% U-235) in Al matrix + water coolant
2. **Burn-up state:** ~80% U-235 depletion (from 93% → 10.7% of total U)
3. **Pu build-up:** Pu-239/240/241 from U-238 neutron capture chain
4. **Fission products:** Major stable FPs (Nd, Ru, Cs) + strong absorbers (Sm-149, Gd-157)
5. **Decay products:** Short-lived FPs (Xe-135, Pm-147) decayed to negligible levels (E-31)

### 9.2 UCO TRISO Fuel Kernel (Capsule 2, Stack 1, Compact 1)

**Material m9211 - Complete Specification:**

```mcnp
c kernel, UCO: density=10.924 g/cm3
m9211
           92234.00c  3.34179E-03  $ U-234 (0.334% of total atoms)
           92235.00c  1.99636E-01  $ U-235 (19.96% enrichment)
           92236.00c  1.93132E-04  $ U-236 (0.019%, feed contamination)
           92238.00c  7.96829E-01  $ U-238 (79.68%, depleted tail)
            6012.00c  0.3217217    $ C-12 (carbide component)
            6013.00c  0.0035783    $ C-13 (natural abundance)
            8016.00c  1.3613       $ O-16 (oxide component)
```

**Cell reference:**
```mcnp
92101 9211 -10.924 -92111  u=2114 vol=0.091694  $ Kernel
      ^^^^
      Material assignment
```

**Chemistry:**
- **Formula:** UC₀.₃₂O₁.₃₆ (approximate)
- **Phase:** Mixed carbide-oxide, likely UC + UO₂ phases
- **Enrichment:** 19.96% U-235 (LEU fuel)
- **Density:** 10.924 g/cm³ (theoretical density of UCO)

**TRISO Coating Layers for this particle:**

```mcnp
92101 9211 -10.924 -92111         u=2114  vol=0.091694  $ Kernel (UCO)
92102 9090 -1.100   92111 -92112  u=2114                $ Buffer (porous C)
92103 9091 -1.912   92112 -92113  u=2114                $ IPyC (dense C)
92104 9092 -3.207   92113 -92114  u=2114                $ SiC (barrier)
92105 9093 -1.901   92114 -92115  u=2114                $ OPyC (dense C)
92106 9094 -1.256   92115         u=2114                $ Matrix (C)
```

**Geometry:**
- Kernel radius: ~200-250 μm (from vol=0.091694 mm³)
- Buffer thickness: ~95 μm
- IPyC thickness: ~35 μm
- SiC thickness: ~35 μm
- OPyC thickness: ~40 μm
- Total particle diameter: ~800-900 μm

### 9.3 Borated Graphite Holder (High Loading)

**Material m9072 - Complete Specification:**

```mcnp
c borated graphite holder, 6.05 atom percent boron, 1.7788 g/cm3, capsule 2-5
m9072
    6012.00c  8.4300E-2   $ C-12 (93.95% natural)
    5010.20c  1.0804E-3   $ B-10 (19.8% of boron, 1.20% of total)
    5011.00c  4.3476E-3   $ B-11 (80.2% of boron, 4.84% of total)
```

**Cell reference:**
```mcnp
92080 9072 -1.7788  97012 97022 97032 -97060  98012 -98014  vol=34.27310
      ^^^^
      Material assignment
```

**Boron loading calculation:**
```
Total atom density (from cell):
ρ_mass = 1.7788 g/cm³
For graphite matrix: M ≈ 12.011 g/mol
ρ_atom_graphite = 1.7788 × 6.022E23 / 12.011 = 8.92E22 atoms/cm³ = 0.148 atoms/barn-cm

From material card:
N(C-12)  = 8.4300E-2 atoms/barn-cm
N(B-10)  = 1.0804E-3 atoms/barn-cm
N(B-11)  = 4.3476E-3 atoms/barn-cm
N_total  = 8.4300E-2 + 1.0804E-3 + 4.3476E-3 = 8.9728E-2 atoms/barn-cm

Boron atom percent:
(1.0804E-3 + 4.3476E-3) / 8.9728E-2 × 100% = 6.05% ✓
```

**Purpose:**
- **Reactivity control:** B-10 strong thermal neutron absorber (3840 barn at thermal)
- **Power shaping:** Controls axial and radial power distribution in AGR-1 test
- **Capsule variation:** 4.76% B (capsules 1,6) vs. 6.05% B (capsules 2-5)

**Physics:**
- B-10(n,α)Li-7 reaction: Dominant neutron absorption mechanism
- High cross-section at thermal energies (~1/v behavior)
- Burn-out: Boron depletes over irradiation, reactivity control degrades

### 9.4 Hafnium Shroud (Isotopically Detailed)

**Material m9081 - Complete Specification:**

```mcnp
c hafnium shroud
m9081
    8016.00c  1.3500E-4   $ O-16 (surface oxide)
    6012.00c  4.4300E-5   $ C-12 (impurity)
   14028.00c  6.3341E-6   $ Si-28 (92.23% of Si)
   14029.00c  3.2289E-7   $ Si-29 (4.67% of Si)
   14030.00c  2.1297E-7   $ Si-30 (3.10% of Si)
   40090.00c  1.0169E-3   $ Zr-90 (51.45% of Zr, alloying)
   40091.00c  2.2288E-4   $ Zr-91 (11.22% of Zr)
   40092.00c  3.4029E-4   $ Zr-92 (17.15% of Zr)
   40094.00c  3.4626E-4   $ Zr-94 (17.38% of Zr)
   40096.00c  5.5719E-5   $ Zr-96 (2.80% of Zr, double-β decay)
   72174.00c  6.7512E-5   $ Hf-174 (0.16% of Hf)
   72176.00c  2.1934E-3   $ Hf-176 (5.21% of Hf)
   72177.00c  7.8473E-3   $ Hf-177 (18.61% of Hf, σ=373 barn)
   72178.00c  1.1431E-2   $ Hf-178 (27.14% of Hf, dominant)
   72179.00c  5.7955E-3   $ Hf-179 (13.74% of Hf, σ=41 barn)
   72180.00c  1.4845E-2   $ Hf-180 (35.20% of Hf)
```

**Cell reference:**
```mcnp
91081 9081 [density] [geometry] $ hafnium shroud
```

**Composition analysis:**
```
Total Hf atoms: 6.7512E-5 + 2.1934E-3 + 7.8473E-3 + 1.1431E-2 + 5.7955E-3 + 1.4845E-2
               = 4.215E-2 atoms/barn-cm (90.8% of material)

Total Zr atoms: 1.0169E-3 + 2.2288E-4 + 3.4029E-4 + 3.4626E-4 + 5.5719E-5
               = 1.977E-3 atoms/barn-cm (4.26% of material)

Hf:Zr ratio = 4.215E-2 / 1.977E-3 = 21.3 : 1
```

**Purpose:**
- **Control rod material:** Strong thermal neutron absorber
- **Hf-177 absorption:** σ_thermal = 373 barn (dominant absorber)
- **Burn-up resistance:** Hf-177 → Hf-178 (still absorbing) maintains control worth
- **Zr alloying:** Improves mechanical strength and corrosion resistance

**Isotopic importance:**
- **Hf-177:** 18.6% abundance, 373 barn → 69.5 effective barn
- **Hf-179:** 13.7% abundance, 41 barn → 5.6 effective barn
- **Hf-174/176/178/180:** Low cross-sections (<10 barn), structural role

---

## 10. SUMMARY AND RECOMMENDATIONS

### 10.1 Material Card Quality Assessment

**Strengths:**
✅ Comprehensive burn-up tracking (210 depleted ATR fuel materials)
✅ Detailed TRISO particle modeling (5-layer coating structure)
✅ Isotopically-resolved structural materials (SS316L, Hf shrouds)
✅ Clear documentation (comments with densities, element/zone identifiers)
✅ Proper thermal scattering for water and beryllium

**Critical Deficiencies:**
❌ **NO graphite thermal scattering** (affects 50+ materials, thermal spectrum, reactivity)
❌ **NO temperature-dependent S(α,β)** (room-temperature libraries for 300-600°C operation)
❌ Mixed ENDF library versions (.00c, .50c, .60c, .70c, .80c) without justification
❌ Some materials duplicated unnecessarily (37× SS316L)

### 10.2 Immediate Recommendations

**HIGH PRIORITY:**
1. **Add graphite thermal scattering:**
   ```mcnp
   mt9040  grph.10t
   mt9041  grph.10t
   mt9070  grph.10t
   mt9071  grph.10t
   mt9072  grph.10t
   mt9073  grph.10t
   mt9074  grph.10t
   mt9075  grph.10t
   mt9090  grph.10t  $ Buffer
   mt9091  grph.10t  $ IPyC
   mt9093  grph.10t  $ OPyC
   mt9094  grph.10t  $ Matrix
   ```

2. **Use temperature-appropriate S(α,β):**
   - Water: `lwtr.11t` (325K) or `lwtr.13t` (350K) instead of `lwtr.10t` (294K)
   - Graphite: `grph.18t` (600K) or `grph.24t` (1200K) for high-temp regions

3. **Standardize ENDF library versions:**
   - Prefer .70c (ENDF/B-VII.0) or .80c (ENDF/B-VIII.0) consistently
   - Update .50c natural elements (Cr, Fe, Ni) to .70c equivalents

**MEDIUM PRIORITY:**
4. **Consolidate duplicate materials:**
   - Use single m9000 for all SS316L instead of m9000-m9036
   - Use tally multipliers or F4 cell-based tallies for component-specific results

5. **Add higher actinides to burn-up tracking:**
   - Pu-242, Am-241, Am-243, Cm-242, Cm-244 for high burn-up regions

6. **Document material provenance:**
   - Add comments citing source documents for compositions
   - Include calculation dates and depletion codes used (ORIGEN, MONTEBURNS, etc.)

### 10.3 Best Practices for Future Models

**Material definition:**
1. Use systematic numbering (encode geometry/position in material number)
2. Comment all materials with density, description, source
3. Use isotopic resolution for absorbers (Hf, B, Gd) and actinides

**Cross-section libraries:**
1. Use latest ENDF evaluation (.80c or .70c) consistently
2. Document library version at top of input file
3. Use temperature-interpolated libraries when available

**Thermal scattering:**
1. Apply S(α,β) to ALL materials with H, Be, C, D₂O
2. Match S(α,β) temperature to actual material temperature
3. Use dual S(α,β) for mixtures (e.g., Be + H₂O)

**Density specification:**
1. Clearly distinguish atom density (barn⁻¹cm⁻¹) vs. mass density (g/cm³)
2. Use negative sign for mass density in cell cards
3. Verify sum of isotopic densities matches total density

**Burn-up materials:**
1. Track all significant actinides (U, Np, Pu, Am, Cm)
2. Include important fission products (Xe-135, Sm-149, Gd-155/157, Nd-143/145)
3. Omit negligible isotopes (density < 1E-15) to reduce input file size

---

## 11. CROSS-REFERENCE TABLES

### 11.1 Material-to-Function Mapping

| Material ID | Function | Type | Density | Key Isotopes |
|-------------|----------|------|---------|--------------|
| m10 | Coolant/moderator | Water | 0.1003 a/b-cm | H-1, O-16 |
| m14-m16 | Be reflector + water | Be + H₂O | 0.122-0.123 | Be-9, H-1, O-16 |
| m17 | Coolant gas | Helium | 1E-4 | He-4 |
| m18 | Reflector | Be metal | 0.124 | Be-9 |
| m21-m33 | Structural + coolant | SS/Al + H₂O | 0.072-0.095 | Fe, Cr, Ni, Al, H, O |
| m38 | Structure | SS-348 | 0.0871 | Fe, Cr, Ni, Nb, Ta |
| m43-m44 | Targets | Co + Al | 0.056 | Co-59, Al-27 |
| m71 | Control | Hafnium | 0.0456 | Hf-nat, Zr |
| m75-m82 | Shroud | Zr + Hf | 0.043-0.044 | Zr-nat, Hf-nat |
| m2106-m2315 | Fuel | U-Al + H₂O | 0.079-0.083 | U-235, Al, H₂O, FPs |
| m621-m632 | Experiments | Zr + Hf + H₂O | 0.060-0.068 | Zr, Hf, U-235, H₂O |
| m711 | Coolant | Water | 0.100 | H-1, O-16 |
| m712 | Structure | Al-6061 | 0.0598 | Al-27 |
| m714 | Structure | SS-304 | 0.0885 | Fe, Cr, Ni |
| m732 | Test material | SS + H₂O + U | 0.0748 | Fe, Cr, Ni, H₂O, U-235 |
| m7410 | Test material | SS + Mo + H₂O | 0.0721 | Fe, Cr, Ni, Mo, H₂O |
| m7510 | Test material | SS + Mo + H₂O | 0.0732 | Fe, Cr, Ni, Mo, H₂O |
| m8900 | Coolant | Air | -0.001164 g/cm³ | N-14, O-16 |
| m8901 | Coolant | Water (hot) | -0.9853 g/cm³ | H-1, O-16 |
| m8902 | Coolant | Helium | 1.25E-4 | He-4 |
| m9000-m9036 | Structure | SS316L | -8.03 g/cm³ | Fe-56, Cr-52, Ni-58, Mo |
| m9040-m9056 | Moderator | Graphite | -0.95 to -1.015 | C-12, C-13 |
| m9070-m9075 | Absorber/structure | Borated C | -1.77 to -1.78 | C-12, B-10, B-11 |
| m9081-m9086 | Control shroud | Hf + Zr | [varies] | Hf isotopes, Zr isotopes |
| m9090 | TRISO buffer | Porous C | -1.10 | C-12, C-13 |
| m9091 | TRISO IPyC | Dense C | -1.912 | C-12, C-13 |
| m9092 | TRISO SiC | Carbide | -3.207 | Si, C |
| m9093 | TRISO OPyC | Dense C | -1.901 | C-12, C-13 |
| m9094 | TRISO matrix | Graphite | -1.256 | C-12, C-13 |
| m9111-m9634 | TRISO fuel | UCO kernel | -10.924 | U-235, U-238, C, O |

### 11.2 Thermal Scattering Library Usage

| Library | Temperature | Materials Applied | Count |
|---------|-------------|-------------------|-------|
| lwtr.10t | 294 K (21°C) | m10, m14-m16, m19-m33, m2106-m2315, m621-m632, m711 | ~240 |
| be.01t | Room temp | m14-m16, m18, m19-m20 | 7 |
| grph.10t | 294 K | **NONE (should be ~50)** | 0 ❌ |

**Recommended additions:**
| Library | Temperature | Should Apply To | Count |
|---------|-------------|-----------------|-------|
| grph.18t | 600 K (327°C) | m9040-m9056, m9070-m9075, m9090-m9094 | ~28 |
| lwtr.11t | 325 K (52°C) | ATR coolant (m10, m21-m33, m2106-m2315) | ~240 |
| lwtr.13t | 350 K (77°C) | AGR coolant (m8901) | 1 |

### 11.3 ENDF Library Version Distribution

| Library Suffix | ENDF Version | Element Types | Count |
|----------------|--------------|---------------|-------|
| .00c | ENDF/B-VI.0 | Graphite C, He, SS isotopes (AGR) | ~120 |
| .20c | Special | B-10 (optimized) | 12 |
| .50c | ENDF/B-V | Natural Cr, Fe, Ni (ATR structural) | ~30 |
| .55c | Special | W | 1 |
| .60c | ENDF/B-VI.8 | Natural Mg, Si, Ti, Zr, Mo | ~40 |
| .70c | ENDF/B-VII.0 | H, C, O, Al, actinides, FPs (ATR) | ~300 |
| .80c | ENDF/B-VIII.0 | Air (N, O) in AGR | 2 |

---

**END OF ANALYSIS**

This comprehensive analysis documents all material card structures, patterns, and best practices observed in the AGR-1 MCNP benchmark models. The most critical finding is the absence of graphite thermal scattering (grph.10t or grph.18t) for ~50 graphite-containing materials, which will affect thermal neutron spectrum and reactivity predictions.
