# Particle Properties

Comprehensive reference for particle rest masses, energies, and properties used in MCNP calculations. Based on CODATA 2018 and Particle Data Group (PDG) 2020 values.

## Overview

This document provides detailed properties for fundamental particles encountered in MCNP transport calculations:
- Leptons (electrons, muons, taus, neutrinos)
- Nucleons (protons, neutrons)
- Light nuclei (deuteron, triton, helium-3, alpha)
- Mesons and other particles
- Conversion between mass, energy, and momentum units

## Atomic Mass Unit (amu)

### Definition and Conversions

**Unified Atomic Mass Unit (u or amu):**
- Defined as exactly 1/12 of the mass of an unbound neutral ¹²C atom at rest and in ground state
- Symbol: u (SI) or amu (commonly used)

**Values:**
```
1 amu = 1.66053906660(50) × 10⁻²⁷ kg
1 amu = 1.66053906660 × 10⁻²⁴ g
1 amu = 931.49410242(28) MeV/c²
```

**Energy-Mass Conversion:**
```
E (MeV) = m (amu) × 931.49410242

Example:
  Proton mass: 1.007276 amu
  Proton energy: 1.007276 × 931.494 = 938.272 MeV
```

**Reciprocal Conversion:**
```
1 MeV/c² = 1.07354410233 × 10⁻³ amu
1 MeV/c² = 1.78266192 × 10⁻³⁰ kg
```

### MCNP Applications

**Material Definitions:**
- Atomic weights in MCNP use amu scale
- Natural element weights are abundance-weighted averages
- Isotopic masses for mass defect and Q-value calculations

**Nuclear Reactions:**
- Q-value = (Σm_reactants - Σm_products) × 931.494 MeV
- Threshold energy calculations
- Binding energy per nucleon

## Leptons

### Electron

**Rest Mass:**
```
m_e = 9.1093837015(28) × 10⁻³¹ kg
m_e = 5.48579909065(16) × 10⁻⁴ amu
m_e = 0.51099895000(15) MeV/c²
```

**Charge:**
- e = -1.602176634 × 10⁻¹⁹ C (exact)
- Charge number: Z = -1

**Properties:**
- Spin: ½ (fermion)
- Lepton number: +1
- Stable (does not decay)
- Magnetic moment: μ_e = -1.00115965218128 μ_B
  - μ_B = Bohr magneton = 5.7883818012 × 10⁻¹¹ MeV/T

**Classical Electron Radius:**
```
r_e = e²/(4πε₀m_e c²)
r_e = 2.8179403262(13) × 10⁻¹⁵ m
r_e = 2.818 fm
```

**Compton Wavelength:**
```
λ_C = h/(m_e c) = 2.42631023867(73) × 10⁻¹² m
λ̄_C = ℏ/(m_e c) = 3.8615926796(12) × 10⁻¹³ m
```

**MCNP Applications:**
- Electron transport (MODE E)
- Beta decay particles
- Compton scattering
- Pair production threshold: E_γ ≥ 2m_e c² = 1.022 MeV
- Energy loss calculations (dE/dx)

### Positron

**Rest Mass:**
- Same as electron: m_e⁺ = 0.51099895000 MeV/c²

**Charge:**
- e = +1.602176634 × 10⁻¹⁹ C
- Charge number: Z = +1

**Properties:**
- Antiparticle of electron
- Same mass, opposite charge
- Unstable in matter (annihilates with electrons)
- Typical lifetime in matter: nanoseconds to picoseconds

**Annihilation:**
```
e⁺ + e⁻ → 2γ (most common)
E_γ = m_e c² = 0.511 MeV (each photon, if at rest)

Or: e⁺ + e⁻ → 3γ (less common, ~0.3% of annihilations)
```

**MCNP Applications:**
- Positron transport (MODE E with PHYS:E)
- Pair production products
- Positron annihilation source (0.511 MeV gammas)
- PET (Positron Emission Tomography) simulations

### Muon

**Rest Mass:**
```
m_μ = 1.883531627(42) × 10⁻²⁸ kg
m_μ = 0.1134289259(25) amu
m_μ = 105.6583755(23) MeV/c²
```

**Charge:**
- μ⁻: -e (negative muon)
- μ⁺: +e (positive muon, antimuon)

**Properties:**
- Spin: ½ (fermion)
- Lepton number: +1 (μ⁻) or -1 (μ⁺)
- Unstable
- Mean lifetime: τ = 2.1969811(22) × 10⁻⁶ s (2.2 μs)
- Mass ratio: m_μ/m_e = 206.768283

**Decay Mode:**
```
μ⁻ → e⁻ + ν̄_e + ν_μ (100%)
μ⁺ → e⁺ + ν_e + ν̄_μ (100%)

Mean decay energy:
  E_e (average) ≈ 35 MeV (max 52.8 MeV)
```

**MCNP Applications:**
- Cosmic ray shielding (muons from pion decay)
- Muon radiography
- Spallation neutron sources
- Generally not transported in standard MCNP (rare in most applications)

### Tau Lepton

**Rest Mass:**
```
m_τ = 3.16754(21) × 10⁻²⁷ kg
m_τ = 1.90754(13) amu
m_τ = 1776.86(12) MeV/c²
```

**Properties:**
- Spin: ½ (fermion)
- Charge: ±e (τ⁻ and τ⁺)
- Unstable
- Mean lifetime: τ = 2.903(5) × 10⁻¹³ s
- Mass ratio: m_τ/m_e = 3477.23

**Decay Modes:**
- Many decay channels (leptonic and hadronic)
- Too short-lived for most MCNP applications

**MCNP Applications:**
- Generally not relevant (high-energy physics only)
- Lifetime too short for transport

### Neutrinos

**Types:**
- Electron neutrino: ν_e
- Muon neutrino: ν_μ
- Tau neutrino: ν_τ

**Mass:**
- Very small (< 1 eV/c²)
- Exact masses unknown (only differences measured)
- Upper limit: Σm_ν < 0.12 eV (cosmological)

**Properties:**
- Spin: ½ (fermion)
- Charge: 0 (neutral)
- Lepton number: +1 (ν) or -1 (ν̄)
- Interact only via weak force
- Extremely small cross sections (σ ~ 10⁻⁴³ cm² for MeV neutrinos)

**MCNP Applications:**
- **Not transported in MCNP** (cross sections too small)
- Appear in decay/reaction energy balance
- Carry away undetectable energy (e.g., fission neutrinos ~12 MeV)
- Relevant for reactor antineutrino detection simulations (specialized)

## Nucleons

### Proton

**Rest Mass:**
```
m_p = 1.67262192369(51) × 10⁻²⁷ kg
m_p = 1.007276466621(53) amu
m_p = 938.27208816(29) MeV/c²
```

**Charge:**
- e = +1.602176634 × 10⁻¹⁹ C (exact)
- Charge number: Z = +1

**Properties:**
- Spin: ½ (fermion)
- Baryon number: +1
- Stable (no observed decay, τ > 10³⁴ years)
- Magnetic moment: μ_p = 2.79284734463 μ_N
  - μ_N = Nuclear magneton = 3.15245125 × 10⁻¹⁴ MeV/T

**Mass Ratios:**
```
m_p/m_e = 1836.15267343(11)
m_p/m_n = 0.99862347812(49) (proton lighter than neutron)
```

**MCNP Applications:**
- Proton transport (MODE H)
- Target nuclei (hydrogen)
- Recoil protons in neutron detectors
- Proton therapy simulations
- Spallation reactions

### Neutron

**Rest Mass:**
```
m_n = 1.67492749804(95) × 10⁻²⁷ kg
m_n = 1.00866491595(49) amu
m_n = 939.56542052(54) MeV/c²
```

**Charge:**
- 0 (neutral)

**Properties:**
- Spin: ½ (fermion)
- Baryon number: +1
- Magnetic moment: μ_n = -1.91304273 μ_N (negative, unusual for neutral particle)
- Unstable when free

**Free Neutron Decay:**
```
n → p + e⁻ + ν̄_e (β⁻ decay)

Half-life: t₁/₂ = 879.4(6) s ≈ 14.66 min
Mean lifetime: τ = 879.4/ln(2) = 1268.6 s ≈ 21.1 min
Decay constant: λ = ln(2)/t₁/₂ = 7.88 × 10⁻⁴ s⁻¹

Q-value:
  Q = (m_n - m_p - m_e)c²
  Q = (1.008665 - 1.007276 - 0.000549) × 931.494
  Q = 0.000840 × 931.494 = 0.782 MeV

Maximum electron energy: E_e(max) = 0.782 MeV
Average electron energy: E_e(avg) ≈ 0.260 MeV
```

**Thermal Neutron Properties (T = 293.6 K):**
```
Energy: E_th = k_B T = 0.0253 eV = 2.53 × 10⁻⁸ MeV
Speed: v_th = sqrt(2E/m) = 2200 m/s
Wavelength: λ = h/(mv) = 1.798 Å
De Broglie: λ (Å) = 0.286 / sqrt(E (eV)) = 1.798 Å at 0.0253 eV
```

**Neutron-Proton Mass Difference:**
```
Δm = m_n - m_p = 1.29333236 MeV/c²

This mass difference:
  - Determines neutron stability (heavier than proton)
  - Sets neutron decay Q-value
  - Important for nuclear stability (neutrons stable in nuclei)
```

**MCNP Applications:**
- **Primary particle in MCNP** (MODE N)
- Fission neutrons
- Fusion neutrons
- Neutron shielding
- Criticality calculations
- Neutron activation
- Most MCNP simulations

## Light Nuclei

### Deuteron (²H Nucleus)

**Rest Mass:**
```
m_d = 3.3435837724(10) × 10⁻²⁷ kg
m_d = 2.013553212745(40) amu
m_d = 1875.61294257(57) MeV/c²
```

**Composition:**
- 1 proton + 1 neutron

**Binding Energy:**
```
Constituent masses:
  m_p + m_n = 1.007276 + 1.008665 = 2.015941 amu

Actual deuteron mass: 2.013553 amu

Mass defect: Δm = 2.015941 - 2.013553 = 0.002388 amu

Binding energy:
  E_B = Δm × c² = 0.002388 × 931.494 = 2.224 MeV

Binding energy per nucleon:
  E_B/A = 2.224 / 2 = 1.112 MeV (weakly bound)
```

**Properties:**
- Spin: 1 (boson)
- Charge: +e
- Stable (does not decay)
- Magnetic moment: μ_d = 0.857438230 μ_N

**MCNP Applications:**
- Heavy water (D₂O) moderator
- Deuterium target in fusion reactions
- D-D fusion: ²H + ²H → ³He + n (Q = 3.27 MeV)
- D-T fusion: ²H + ³H → ⁴He + n (Q = 17.6 MeV)

### Triton (³H Nucleus)

**Rest Mass:**
```
m_t = 5.0073567446(15) × 10⁻²⁷ kg
m_t = 3.01604927912(7) amu
m_t = 2808.92113662(84) MeV/c²
```

**Composition:**
- 1 proton + 2 neutrons

**Binding Energy:**
```
Constituent masses:
  m_p + 2m_n = 1.007276 + 2(1.008665) = 3.024606 amu

Actual triton mass: 3.016049 amu

Mass defect: Δm = 0.008557 amu

Binding energy:
  E_B = 0.008557 × 931.494 = 7.972 MeV

Binding energy per nucleon:
  E_B/A = 7.972 / 3 = 2.657 MeV
```

**Properties:**
- Spin: ½ (fermion)
- Charge: +e
- Unstable (radioactive)
- Half-life: t₁/₂ = 12.32 years
- Decay mode: β⁻ to ³He (E_max = 18.6 keV)

**MCNP Applications:**
- Tritium breeding in fusion blankets
- D-T fusion fuel
- Tritium contamination studies
- Low-energy beta source

### Helium-3 Nucleus

**Rest Mass:**
```
m_³He = 5.0064127862(15) × 10⁻²⁷ kg
m_³He = 3.0160293201(26) amu
m_³He = 2808.39160743(85) MeV/c²
```

**Composition:**
- 2 protons + 1 neutron

**Binding Energy:**
```
Constituent masses:
  2m_p + m_n = 2(1.007276) + 1.008665 = 3.023217 amu

Actual ³He mass: 3.016029 amu

Mass defect: Δm = 0.007188 amu

Binding energy:
  E_B = 0.007188 × 931.494 = 6.696 MeV (less than triton)

Binding energy per nucleon:
  E_B/A = 6.696 / 3 = 2.232 MeV
```

**Properties:**
- Spin: ½ (fermion)
- Charge: +2e
- Stable
- Natural abundance: 0.000137% (very rare)

**MCNP Applications:**
- Neutron detection: ³He(n,p)³H reaction
  - Large thermal cross section: σ = 5330 barns
  - Q = 0.764 MeV
- ³He-filled proportional counters
- D-³He fusion: ²H + ³He → ⁴He + p (Q = 18.3 MeV)

### Alpha Particle (⁴He Nucleus)

**Rest Mass:**
```
m_α = 6.6446573357(20) × 10⁻²⁷ kg
m_α = 4.001506179129(62) amu
m_α = 3727.3794066(11) MeV/c²
```

**Composition:**
- 2 protons + 2 neutrons
- Very stable configuration (magic numbers)

**Binding Energy:**
```
Constituent masses:
  2m_p + 2m_n = 2(1.007276) + 2(1.008665) = 4.031882 amu

Actual alpha mass: 4.001506 amu

Mass defect: Δm = 0.030376 amu

Binding energy:
  E_B = 0.030376 × 931.494 = 28.296 MeV

Binding energy per nucleon:
  E_B/A = 28.296 / 4 = 7.074 MeV (very tightly bound)
```

**Properties:**
- Spin: 0 (boson)
- Charge: +2e
- Extremely stable
- Natural abundance: 99.999863% of helium

**MCNP Applications:**
- Alpha decay particles (typical E = 4-6 MeV)
- Alpha transport (MODE A or MODE H for heavy ions)
- Radon decay chains
- Americium-beryllium sources: ⁹Be(α,n)¹²C
- Range calculations (Bragg peak)
- Radiation damage (high LET)

## Neutron Energy Classification

### Energy Ranges (Approximate)

```
Cold neutrons:      E < 0.025 eV     (λ > 1.8 Å)
Thermal neutrons:   0.025 eV         (λ = 1.8 Å, v = 2200 m/s)
Epithermal:         0.025 eV - 1 eV
Cadmium cutoff:     ~0.5 eV          (Cd absorption edge)
Resonance region:   1 eV - 1 keV
Intermediate:       1 keV - 100 keV
Fast:               100 keV - 20 MeV
High energy:        > 20 MeV
```

### De Broglie Wavelength

```
λ (Å) = h/(mv) = h/(sqrt(2mE))

For neutrons:
  λ (Å) = 0.286 / sqrt(E (eV))

Examples:
  Thermal (0.0253 eV):  λ = 1.798 Å
  1 eV:                  λ = 0.286 Å
  1 MeV:                 λ = 2.86 × 10⁻⁴ Å
```

## Conversion Formulas

### Energy-Momentum-Mass Relations

**Non-relativistic (valid for E ≪ mc²):**
```
E = ½mv² = p²/(2m)
p = mv = sqrt(2mE)
v = sqrt(2E/m)
```

**Relativistic (always valid):**
```
E_total = sqrt((pc)² + (mc²)²)
E_kinetic = E_total - mc²
p = (1/c)sqrt(E_total² - (mc²)²)

For photons (m = 0):
  E = pc
  p = E/c
```

### Practical Neutron Conversions

**Speed to Energy:**
```
E (eV) = 5.227 × 10⁻⁶ × v² (m/s)
E (MeV) = 5.227 × 10⁻¹² × v² (m/s)

Example: v = 2200 m/s
  E = 5.227 × 10⁻⁶ × (2200)² = 0.0253 eV ✓
```

**Energy to Speed:**
```
v (m/s) = 1.383 × 10⁴ × sqrt(E (eV))
v (m/s) = 1.383 × 10⁷ × sqrt(E (MeV))

Example: E = 1 MeV
  v = 1.383 × 10⁷ × 1 = 1.383 × 10⁷ m/s = 0.046c
```

### Temperature to Energy

**Thermal energy:**
```
E = k_B T

For neutrons in Maxwell-Boltzmann distribution:
  E_avg = (3/2) k_B T
  E_mode = (1/2) k_B T  (most probable)

At T = 293.6 K:
  E_mode = 0.0253 eV (definition of thermal energy)
  E_avg = 0.0380 eV
```

## References

### Official Data Sources

**NIST (National Institute of Standards and Technology):**
- CODATA 2018 recommended values
- https://physics.nist.gov/cuu/Constants/

**Particle Data Group (PDG):**
- Comprehensive particle properties
- Annual Review of Particle Physics
- https://pdg.lbl.gov/

**IAEA Nuclear Data Services:**
- Atomic masses and binding energies
- https://www-nds.iaea.org/

### Related MCNP Skills

- **mcnp-physical-constants**: Fundamental constants
- **mcnp-isotope-lookup**: Nuclear masses and properties
- **mcnp-source-builder**: Particle source energies
- **mcnp-unit-converter**: Energy unit conversions

---

**End of Particle Properties Reference**
