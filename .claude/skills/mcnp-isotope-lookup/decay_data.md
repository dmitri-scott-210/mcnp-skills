# MCNP Decay Data and Activation Reference

## Overview

This reference provides comprehensive decay properties, activation products, fission product data, and radioactive decay information essential for MCNP source definitions, activation analysis, and decay calculations. Data sourced from NNDC, IAEA, and ICRP Publication 107 (2024).

## Radioactive Decay Fundamentals

### Decay Modes

**Alpha Decay (α)**:
```
Emission of He-4 nucleus (2 protons + 2 neutrons)

Decay equation:
  ᴬX → ᴬ⁻⁴Y + ⁴He + Q

Example:
  ²³⁹Pu → ²³⁵U + α (Q = 5.24 MeV)

Characteristics:
  - Reduces Z by 2, A by 4
  - Common in heavy elements (Z > 82)
  - Mono-energetic alphas (except recoil)
  - May produce gamma rays
```

**Beta-Minus Decay (β⁻)**:
```
Neutron converts to proton + electron + antineutrino

Decay equation:
  ᴬX → ᴬY + e⁻ + ν̄ₑ + Q

Example:
  ¹³⁷Cs → ¹³⁷Ba + β⁻ + γ (Q = 1.176 MeV)

Characteristics:
  - Increases Z by 1, A unchanged
  - Continuous beta spectrum
  - Common in neutron-rich isotopes
  - Often followed by gamma emission
```

**Beta-Plus Decay (β⁺) / Positron Emission**:
```
Proton converts to neutron + positron + neutrino

Decay equation:
  ᴬX → ᴬY + e⁺ + νₑ + Q

Example:
  ²²Na → ²²Ne + β⁺ + γ (Q = 2.842 MeV)

Characteristics:
  - Decreases Z by 1, A unchanged
  - Requires Q > 1.022 MeV (2mₑc²)
  - Positron annihilation → 2 × 0.511 MeV gammas
  - Common in proton-rich isotopes
```

**Electron Capture (EC)**:
```
Nucleus captures inner-shell electron

Decay equation:
  ᴬX + e⁻ → ᴬY + νₑ + X-rays

Example:
  ⁵⁵Fe + e⁻ → ⁵⁵Mn + νₑ + X-rays

Characteristics:
  - Decreases Z by 1, A unchanged
  - Competes with β⁺ decay
  - Produces characteristic X-rays
  - No positrons emitted
```

**Gamma Emission (γ)**:
```
Excited nucleus emits photon

Transition:
  ᴬX* → ᴬX + γ

Characteristics:
  - No change in Z or A
  - Mono-energetic photons
  - Follows other decay modes
  - Used for isotope identification
```

**Isomeric Transition (IT)**:
```
Long-lived excited state decays to ground state

Example:
  ⁹⁹ᵐTc → ⁹⁹Tc + γ (0.140 MeV)
  t₁/₂ = 6.01 hours

Metastable states (m):
  - Long-lived excited states
  - Typical t₁/₂ > 1 second
  - Medical isotopes (Tc-99m, In-111m)
```

**Spontaneous Fission (SF)**:
```
Nucleus splits into fragments without neutron absorption

Example:
  ²⁵²Cf → fission fragments + neutrons

Characteristics:
  - Heavy actinides (Z ≥ 90)
  - Competes with alpha decay
  - ~2-4 neutrons per fission
  - Californium-252 neutron source
```

### Half-Life and Decay Constant

**Definitions**:
```
Half-life (t₁/₂): Time for half of nuclei to decay

Decay constant (λ): Probability of decay per unit time

Relationship:
  λ = ln(2) / t₁/₂ = 0.693147 / t₁/₂

Activity:
  A(t) = A₀ × e⁻ᵏᵗ = A₀ × (½)^(t/t₁/₂)

Number of atoms:
  N(t) = N₀ × e⁻ᵏᵗ
```

**Half-Life Ranges**:
```
Very short:  t₁/₂ < 1 second
Short:       1 s < t₁/₂ < 1 day
Intermediate: 1 day < t₁/₂ < 1 year
Long:        1 yr < t₁/₂ < 10⁸ years
Very long:   t₁/₂ > 10⁸ years (quasi-stable)
Stable:      t₁/₂ = ∞
```

## Important Radioactive Isotopes for MCNP

### Calibration and Standard Sources

| Isotope | ZAID | Half-life | Decay Mode | Gamma Energies (MeV) | Use |
|---------|------|-----------|------------|----------------------|-----|
| Co-60   | 27060 | 5.2714 yr | β⁻ → Ni-60 | 1.173, 1.332 | Calibration, irradiation |
| Cs-137  | 55137 | 30.17 yr  | β⁻ → Ba-137m | 0.662 (Ba-137m) | Calibration, medical |
| Na-22   | 11022 | 2.603 yr  | β⁺ → Ne-22 | 0.511 (2×), 1.275 | PET, calibration |
| Mn-54   | 25054 | 312.3 d   | EC → Cr-54 | 0.835 | Activation |
| Am-241  | 95241 | 432.2 yr  | α → Np-237 | 0.060 | Smoke detectors, AmBe source |

### Medical Isotopes

| Isotope | ZAID | Half-life | Decay Mode | Gamma (MeV) | Application |
|---------|------|-----------|------------|-------------|-------------|
| Tc-99m  | 43099* | 6.01 hr | IT → Tc-99 | 0.140 | Diagnostic imaging |
| I-131   | 53131 | 8.02 d | β⁻ → Xe-131 | 0.364 | Thyroid treatment |
| I-125   | 53125 | 59.4 d | EC → Te-125 | 0.027-0.035 | Brachytherapy |
| F-18    | 9018 | 109.8 min | β⁺ → O-18 | 0.511 (2×) | PET imaging |
| Ir-192  | 77192 | 73.83 d | β⁻ → Pt-192 | 0.3-0.6 | HDR brachytherapy |

*Note: MCNP typically uses 43099 for both Tc-99 and Tc-99m

### Neutron Sources

| Isotope | ZAID | Half-life | Decay | Neutron Source Type | Yield |
|---------|------|-----------|-------|---------------------|-------|
| Cf-252  | 98252 | 2.645 yr | SF (3%), α | Spontaneous fission | 2.3×10⁶ n/s per μg |
| Pu-238  | 94238 | 87.7 yr | α | PuBe, PuF | Used in RTGs |
| Am-241  | 95241 | 432.2 yr | α | AmBe, AmLi | ~60 n/s per Ci (AmBe) |
| Pu-239  | 94239 | 2.411×10⁴ yr | α | PuBe | ~2×10⁶ n/g (PuBe) |

**AmBe Source**:
```
Reaction: ⁹Be(α,n)¹²C
Alpha from Am-241 → neutron from Be-9
Q-value: 5.7 MeV
Neutron spectrum: 0 to ~11 MeV (average ~4.5 MeV)

MCNP Source:
SDEF  PAR=1  ERG=D1  POS=0 0 0
SI1  H  0.0  11.0              $ Histogram (0 to 11 MeV)
SP1  D  0 0.1 0.2 ... (AmBe spectrum)
```

### Fissile and Fertile Actinides

| Isotope | ZAID | Half-life | Decay Mode | Fissile/Fertile | σ_f (thermal) |
|---------|------|-----------|------------|-----------------|---------------|
| U-233   | 92233 | 1.592×10⁵ yr | α | Fissile | 531 b |
| U-235   | 92235 | 7.04×10⁸ yr | α | Fissile | 585 b |
| U-238   | 92238 | 4.468×10⁹ yr | α | Fertile | <1 mb |
| Np-237  | 93237 | 2.144×10⁶ yr | α | Fertile | 0.02 b |
| Pu-238  | 94238 | 87.7 yr | α | Fertile | 18 b |
| Pu-239  | 94239 | 2.411×10⁴ yr | α | Fissile | 747 b |
| Pu-240  | 94240 | 6561 yr | α | Fertile | 0.3 b |
| Pu-241  | 94241 | 14.33 yr | β⁻ | Fissile | 1011 b |
| Am-241  | 95241 | 432.2 yr | α | Fertile | 3.0 b |
| Cm-244  | 96244 | 18.1 yr | α | Fertile | 1.0 b |

## Fission Products

### High-Yield Fission Products (U-235 Thermal)

**Long-Lived (t₁/₂ > 1 year)**:

| Isotope | ZAID | Half-life | Yield (%) | Decay Mode | Activity | Importance |
|---------|------|-----------|-----------|------------|----------|------------|
| Sr-90   | 38090 | 28.79 yr | 5.8 | β⁻ | High | Heat, dose |
| Zr-93   | 40093 | 1.53×10⁶ yr | 6.3 | β⁻ | Low | Long-term waste |
| Tc-99   | 43099 | 2.11×10⁵ yr | 6.1 | β⁻ | Low | Long-term waste |
| Ru-106  | 44106 | 373.6 d | 0.4 | β⁻ | Medium | Dose |
| Pd-107  | 46107 | 6.5×10⁶ yr | 0.15 | β⁻ | Very low | Long-term waste |
| I-129   | 53129 | 1.57×10⁷ yr | 0.7 | β⁻ | Very low | Environmental |
| Cs-135  | 55135 | 2.3×10⁶ yr | 6.5 | β⁻ | Very low | Long-term waste |
| Cs-137  | 55137 | 30.17 yr | 6.2 | β⁻ | High | Heat, dose, gamma |
| Ce-144  | 58144 | 284.9 d | 5.5 | β⁻ | Medium | Dose |
| Sm-151  | 62151 | 90 yr | 0.42 | β⁻ | Low | Absorber |

**Short-Lived but Important** (t₁/₂ < 1 year):

| Isotope | ZAID | Half-life | Yield (%) | Importance |
|---------|------|-----------|-----------|------------|
| Kr-85   | 36085 | 10.76 yr | 0.3 | Noble gas release |
| Sr-89   | 38089 | 50.5 d | 4.7 | Medical, dose |
| Y-90    | 39090 | 64.0 hr | Daughter of Sr-90 | Dose |
| I-131   | 53131 | 8.02 d | 2.9 | Medical, environmental |
| Xe-133  | 54133 | 5.24 d | 6.7 | Noble gas release |
| Ba-140  | 56140 | 12.75 d | 6.3 | Dose |
| La-140  | 57140 | 1.68 d | Daughter of Ba-140 | Gamma dose |

### Neutron Poisons (High Absorption Cross-Section)

| Isotope | ZAID | Half-life | Yield (%) | σ_a (thermal) | Impact |
|---------|------|-----------|-----------|---------------|--------|
| Xe-135  | 54135 | 9.14 hr | 0.003* | 2.65×10⁶ b | "Xenon pit" - strongest poison |
| Sm-149  | 62149 | Stable | 1.08** | 40,140 b | Equilibrium poison |
| Sm-151  | 62151 | 90 yr | 0.42 | 15,000 b | Long-term poison |
| Gd-155  | 64155 | Stable | 0.031** | 60,900 b | Control materials |
| Eu-155  | 63155 | 4.76 yr | 0.03 | 3,950 b | Moderate poison |

*Direct + from I-135 decay
**Cumulative yield including precursor decay

**Xenon-135 Production**:
```
Production paths:
  1. Direct fission: ~0.003% yield
  2. I-135 decay chain:
     Te-135 (19s) → I-135 (6.57h) → Xe-135 (9.14h) → Cs-135 (stable)

Removal:
  1. Neutron absorption: Xe-135(n,γ)Xe-136
  2. Radioactive decay: t₁/₂ = 9.14 hr

Peak concentration: 6-8 hours after shutdown
Reactivity effect: Up to -3000 pcm in thermal reactors
```

### Fission Product MCNP Material (Simplified)

```
c Spent fuel fission products (simplified representation)
c Major contributors to neutron absorption and gamma dose
M10 38090.80c  0.058       $ Sr-90 (5.8% yield, heat source)
    43099.80c  0.061       $ Tc-99 (6.1% yield, long-lived)
    44106.80c  0.004       $ Ru-106 (0.4% yield, beta-gamma)
    53129.80c  0.007       $ I-129 (0.7% yield, environmental)
    54135.80c  0.0001      $ Xe-135 (poison, equilibrium value)
    55137.80c  0.062       $ Cs-137 (6.2% yield, gamma source)
    58144.80c  0.055       $ Ce-144 (5.5% yield, beta-gamma)
    62149.80c  0.011       $ Sm-149 (cumulative yield, poison)
    62151.80c  0.004       $ Sm-151 (0.42% yield, absorber)
c Note: Fractions represent fission yields (not normalized)
c For accurate spent fuel, use ORIGEN or CINDER90
```

## Activation Products

### Aluminum (Al-27) Activation

**Primary Reaction**: Al-27(n,γ)Al-28
```
Parent: Al-27 (100% natural abundance)
Product: Al-28
  ZAID: 13028
  Half-life: 2.245 minutes
  Decay: β⁻ → Si-28
  Beta max: 2.865 MeV
  Gamma: 1.779 MeV (100%)

Cross section: σ(n,γ) = 0.232 b (thermal)

Activation rate:
  A = φ × σ × N
  where φ = neutron flux, σ = cross section, N = atom density
```

**Secondary Reactions** (threshold):
```
Al-27(n,α)Na-24:
  Threshold: ~3 MeV
  Product: Na-24 (t₁/₂ = 14.997 hr)
  Gammas: 1.369 MeV (100%), 2.754 MeV (99.86%)

Al-27(n,p)Mg-27:
  Threshold: ~2 MeV
  Product: Mg-27 (t₁/₂ = 9.458 min)
  Gammas: 0.844 MeV, 1.014 MeV
```

### Iron (Fe) Activation

**Fe-54(n,p)Mn-54**:
```
Parent: Fe-54 (5.845% of natural Fe)
Product: Mn-54
  ZAID: 25054
  Half-life: 312.3 days
  Decay: EC → Cr-54
  Gamma: 0.835 MeV (99.98%)

Threshold: ~1 MeV (fast neutron)
Application: Radiation damage studies, fast flux monitoring
```

**Fe-58(n,γ)Fe-59**:
```
Parent: Fe-58 (0.282% of natural Fe)
Product: Fe-59
  ZAID: 26059
  Half-life: 44.5 days
  Decay: β⁻ → Co-59
  Gammas: 1.099 MeV, 1.292 MeV

Cross section: σ(n,γ) = 1.15 b (thermal)
```

### Cobalt (Co-59) Activation

**Co-59(n,γ)Co-60**:
```
Parent: Co-59 (100% natural abundance)
Product: Co-60
  ZAID: 27060
  Half-life: 5.2714 years
  Decay: β⁻ → Ni-60
  Gammas: 1.173 MeV (99.85%), 1.332 MeV (99.98%)

Cross section: σ(n,γ) = 37.2 b (thermal)

High activation: Co-60 is major contributor in reactor components
Used for: Irradiators, calibration sources, sterilization

Production:
  1 g Co-59 in flux of 10¹³ n/cm²·s for 1 year
  → Activity ≈ 100 Ci Co-60
```

### Nickel Activation

**Ni-58(n,p)Co-58**:
```
Parent: Ni-58 (68.077% of natural Ni)
Product: Co-58
  ZAID: 27058
  Half-life: 70.86 days
  Decay: β⁺, EC → Fe-58
  Gammas: 0.811 MeV (99.4%)

Threshold: ~0.3 MeV
Application: Fast neutron dosimetry
```

### Zirconium (Cladding) Activation

**Zr-94(n,γ)Zr-95**:
```
Parent: Zr-94 (17.38% of natural Zr)
Product: Zr-95
  ZAID: 40095
  Half-life: 64.0 days
  Decay: β⁻ → Nb-95
  Gammas: 0.724 MeV, 0.757 MeV

Daughter: Nb-95 (t₁/₂ = 34.97 d)
  Gammas: 0.766 MeV

Importance: Reactor cladding, spent fuel dose
```

### Sodium (Coolant) Activation

**Na-23(n,γ)Na-24**:
```
Parent: Na-23 (100% natural abundance)
Product: Na-24
  ZAID: 11024
  Half-life: 14.997 hours
  Decay: β⁻ → Mg-24
  Gammas: 1.369 MeV (100%), 2.754 MeV (99.86%)

Cross section: σ(n,γ) = 0.530 b (thermal)

Impact: Sodium-cooled fast reactors
  - Primary coolant activation
  - Intermediate loop required for shielding
  - Decay during shutdown
```

### Stainless Steel Activation

**Major Products**:
```
Cr-51: (27.7 d) from Cr-50(n,γ) - Gamma: 0.320 MeV
Mn-54: (312.3 d) from Fe-54(n,p) - Gamma: 0.835 MeV
Fe-59: (44.5 d) from Fe-58(n,γ) - Gammas: 1.099, 1.292 MeV
Co-58: (70.86 d) from Ni-58(n,p) - Gamma: 0.811 MeV
Co-60: (5.27 yr) from Co-59(n,γ) - Gammas: 1.173, 1.332 MeV

Long-term dose dominated by Co-60
```

## Decay Chains

### U-238 Decay Series (4n+2)

```
U-238 (4.468×10⁹ yr, α)
  ↓
Th-234 (24.10 d, β⁻)
  ↓
Pa-234m (1.17 min, β⁻)
  ↓
U-234 (2.455×10⁵ yr, α)
  ↓
Th-230 (7.538×10⁴ yr, α)
  ↓
Ra-226 (1600 yr, α)
  ↓
Rn-222 (3.82 d, α) ← Noble gas, environmental concern
  ↓
Po-218 (3.10 min, α)
  ↓
Pb-214 (26.8 min, β⁻)
  ↓
Bi-214 (19.9 min, β⁻)
  ↓
Po-214 (164 μs, α)
  ↓
Pb-210 (22.3 yr, β⁻)
  ↓
Bi-210 (5.01 d, β⁻)
  ↓
Po-210 (138.4 d, α)
  ↓
Pb-206 (STABLE)

MCNP Relevance:
  - Natural uranium decay
  - Radon (Rn-222) production in soil
  - Background radiation sources
  - Mining and milling
```

### U-235 Decay Series (4n+3)

```
U-235 (7.04×10⁸ yr, α)
  ↓
Th-231 (25.5 hr, β⁻)
  ↓
Pa-231 (3.276×10⁴ yr, α)
  ↓
Ac-227 (21.77 yr, β⁻)
  ↓
Th-227 (18.68 d, α)
  ↓
Ra-223 (11.43 d, α)
  ↓
Rn-219 (3.96 s, α)
  ↓
Po-215 (1.78 ms, α)
  ↓
Pb-211 (36.1 min, β⁻)
  ↓
Bi-211 (2.14 min, α)
  ↓
Tl-207 (4.77 min, β⁻)
  ↓
Pb-207 (STABLE)
```

### Th-232 Decay Series (4n)

```
Th-232 (1.405×10¹⁰ yr, α)
  ↓
Ra-228 (5.75 yr, β⁻)
  ↓
Ac-228 (6.15 hr, β⁻)
  ↓
Th-228 (1.913 yr, α)
  ↓
Ra-224 (3.66 d, α)
  ↓
Rn-220 (55.6 s, α) ← Thoron gas
  ↓
Po-216 (0.145 s, α)
  ↓
Pb-212 (10.64 hr, β⁻)
  ↓
Bi-212 (60.55 min, α, β⁻)
  ↓
Po-212 (299 ns, α) or Tl-208 (3.05 min, β⁻)
  ↓
Pb-208 (STABLE)

Thorium fuel cycle relevance:
  - Th-232 → U-233 breeding
  - Ra-228 and Th-228 in waste
```

### Plutonium Production Chain

```
U-238 + n → U-239 + γ
  ↓
U-239 (23.5 min, β⁻)
  ↓
Np-239 (2.356 d, β⁻)
  ↓
Pu-239 (2.411×10⁴ yr, α) ← Fissile

Further captures:
Pu-239 + n → Pu-240 + γ (6561 yr, α)
Pu-240 + n → Pu-241 + γ (14.33 yr, β⁻)
Pu-241 + n → Pu-242 + γ (3.75×10⁵ yr, α)

Pu-241 decay:
Pu-241 (14.33 yr, β⁻) → Am-241 (432.2 yr, α)
```

## MCNP Source Definitions from Decay Data

### Co-60 Source Example

```
c Co-60 source: 10 Ci = 3.7×10¹¹ Bq
c Decay: β⁻ to Ni-60 with 2 cascade gammas
c Gamma 1: 1.173 MeV (99.85%)
c Gamma 2: 1.332 MeV (99.98%)
c ~2 gammas per decay
c
c Source strength: 3.7×10¹¹ decays/s × 2 = 7.4×10¹¹ γ/s
c
SDEF  PAR=2  ERG=D1  POS=0 0 0  WGT=7.4E11
SI1  L  1.173  1.332       $ Discrete energies (MeV)
SP1     0.5    0.5          $ Equal probability (1 of each)
```

### Cs-137 Source Example

```
c Cs-137 source: 1 Ci = 3.7×10¹⁰ Bq
c Decay: β⁻ to Ba-137m (94.6%), direct to Ba-137 (5.4%)
c Ba-137m IT: 0.662 MeV gamma (85%)
c Effective: 0.85 × 0.946 = 80.4% gammas at 0.662 MeV
c
c Source strength: 3.7×10¹⁰ × 0.804 = 2.97×10¹⁰ γ/s
c
SDEF  PAR=2  ERG=0.662  POS=0 0 0  WGT=2.97E10
c
c If modeling Ba-137m explicitly:
SI1  L  0  0.662           $ 0 for no gamma, 0.662 MeV
SP1     0.15 0.85          $ 15% no gamma, 85% gamma
```

### AmBe Neutron Source

```
c Am-241/Be neutron source: 1 Ci Am-241
c Reaction: ⁹Be(α,n)¹²C
c Neutron yield: ~60 n/s per Ci Am-241
c Spectrum: Continuous from 0 to ~11 MeV
c
SDEF  PAR=1  ERG=D1  POS=0 0 0  WGT=60
c
c AmBe spectrum (simplified histogram)
SI1  H  0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0
SP1  D  0.0 0.05 0.10 0.15 0.20 0.18 0.14 0.10 0.05 0.02 0.01 0.0
c
c For accurate spectrum, use tabulated AmBe data
```

### Cf-252 Fission Source

```
c Cf-252 spontaneous fission source: 1 μg
c SF branching: 3.09%
c Neutron yield: 2.3×10⁶ n/s per μg
c Spectrum: Fission spectrum (Watt distribution)
c
SDEF  PAR=1  ERG=D1  POS=0 0 0  WGT=2.3E6
c
c Watt fission spectrum
SI1  -3  A  B             $ Watt spectrum parameters
SP1      0.77 1.025       $ A=0.77 MeV, B=1.025 MeV⁻¹ for Cf-252
```

## Activity Calculations

### Basic Formulas

**Activity from Mass**:
```
A = λ × N = (ln(2) / t₁/₂) × N

where:
  λ = decay constant (s⁻¹)
  N = number of atoms
  t₁/₂ = half-life

Number of atoms:
  N = (m × Nₐ) / A
  m = mass (g)
  Nₐ = 6.022×10²³ mol⁻¹
  A = atomic mass (g/mol)

Combined:
  A (Bq) = (ln(2) × m × Nₐ) / (t₁/₂ × A)
```

**Example - Co-60**:
```
Given: 1 gram Co-60
  t₁/₂ = 5.2714 yr = 1.663×10⁸ s
  A = 59.934 g/mol

  N = (1 g × 6.022×10²³) / 59.934 = 1.005×10²² atoms

  A = (0.693 × 1.005×10²²) / (1.663×10⁸)
    = 4.19×10¹³ Bq
    = 1132 Ci

Rule of thumb: 1 g Co-60 ≈ 1100 Ci
```

### Specific Activity

**Definition**: Activity per unit mass

```
Aₛ (Bq/g) = (ln(2) × Nₐ) / (t₁/₂ × A)

Example values:
  H-3:     3.57×10¹⁴ Bq/g  (9650 Ci/g)
  Co-60:   4.19×10¹³ Bq/g  (1132 Ci/g)
  Sr-90:   5.09×10¹² Bq/g  (138 Ci/g)
  Cs-137:  3.22×10¹² Bq/g  (87 Ci/g)
  I-129:   6.55×10⁶ Bq/g   (177 μCi/g)
  U-235:   8.00×10⁴ Bq/g   (2.16 μCi/g)
  U-238:   1.24×10⁴ Bq/g   (0.336 μCi/g)
  Pu-239:  2.30×10⁹ Bq/g   (62.1 mCi/g)
```

## Natural Radioactivity

### Potassium-40 in Human Body

```
K-40: 0.0117% of natural potassium
  t₁/₂ = 1.248×10⁹ yr
  Decay: β⁻ (89.3%) → Ca-40
         EC (10.7%) → Ar-40
  Gamma: 1.461 MeV (10.7%)

Human body (~70 kg):
  Contains ~140 g K
  K-40 mass: 140 g × 0.000117 = 0.01638 g

  Activity: (ln(2) × 0.01638 × 6.022×10²³) / (3.94×10¹⁶ s × 39.964)
          ≈ 4400 Bq
          ≈ 0.12 μCi

Dose: ~0.17 mSv/yr (internal)
```

### Concrete Radioactivity

```
Typical activity: ~1 Bq/g total
Sources:
  - K-40: ~0.3 Bq/g (from potassium)
  - U-238 series: ~0.3 Bq/g
  - Th-232 series: ~0.3 Bq/g

Gamma dose rate: ~0.1 μSv/hr at contact
Important for: Low-level counting, background studies
```

## Data Sources and References

**Primary Nuclear Data**:
- NNDC (National Nuclear Data Center): www.nndc.bnl.gov
- IAEA Nuclear Data Services: www-nds.iaea.org
- ICRP Publication 107: Nuclear Decay Data (2008)

**Decay Data**:
- ENSDF (Evaluated Nuclear Structure Data File)
- Nuclear Wallet Cards (Jagdish K. Tuli)
- Evaluated Decay Schemes

**MCNP-Specific**:
- MCNP6 User Manual, Chapter 6 (Source Definitions)
- Activation calculations: CINDER90 manual
- Fission products: ORIGEN, SCALE

**Related Documentation**:
- Chart of the Nuclides (Karlsruhe, KAERI)
- Table of Isotopes (Firestone & Shirley)

---

**For ZAID format, see `zaid_format_guide.md`**
**For isotope masses and abundances, see `isotope_database.md`**
**For cross-section libraries, see `library_availability.md`**
