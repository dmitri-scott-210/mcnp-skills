# Nuclear Constants

Reference for nuclear physics constants, reaction data, fission properties, and decay parameters used in MCNP calculations and reactor physics.

## Nuclear Energy Scale

### Atomic Mass Unit Energy Equivalent

**Definition:**
```
1 amu = 931.49410242(28) MeV/c²
```

**This fundamental conversion factor enables:**
- Mass defect calculations
- Q-value determinations
- Binding energy calculations
- Reaction threshold energy

**Example - Proton Mass:**
```
m_p = 1.007276466621 amu
m_p c² = 1.007276 × 931.494 = 938.272 MeV
```

### Mass-Energy Equivalence

**Einstein's relation:**
```
E = mc²

For nuclear masses in amu:
  E (MeV) = m (amu) × 931.494

For masses in kg:
  E (J) = m (kg) × (2.998 × 10⁸)² = m × 8.988 × 10¹⁶
```

### Typical Nuclear Energy Scales

```
Binding energy per nucleon:     ~1-9 MeV
Nuclear reaction Q-values:      ~1-20 MeV
Fission energy release:         ~200 MeV
Fusion energy release:          ~3-18 MeV
Alpha decay energies:           ~4-6 MeV
Beta decay energies:            ~keV to ~MeV
Gamma ray energies:             ~keV to ~MeV
```

## Binding Energy

### Definition

**Nuclear binding energy:**
```
E_B = [Zm_p + Nm_n - M_nucleus] × c²

where:
  Z = number of protons
  N = number of neutrons
  A = Z + N (mass number)
  m_p = proton mass
  m_n = neutron mass
  M_nucleus = actual nuclear mass
```

**Binding energy per nucleon:**
```
E_B/A = E_B / (Z + N)
```

### Semi-Empirical Mass Formula (SEMF)

**Weizsäcker formula (approximate binding energy):**
```
E_B = a_v A - a_s A^(2/3) - a_c Z²/A^(1/3) - a_a (N-Z)²/A + δ(A,Z)

where:
  a_v = 15.75 MeV    (volume term)
  a_s = 17.8 MeV     (surface term)
  a_c = 0.711 MeV    (Coulomb term)
  a_a = 23.7 MeV     (asymmetry term)
  δ(A,Z) = pairing term:
    +12 A^(-1/2) MeV for even-even nuclei
    0 MeV for odd-A nuclei
    -12 A^(-1/2) MeV for odd-odd nuclei
```

**Physical interpretation:**
- Volume term: attractive strong force (proportional to A)
- Surface term: nucleons at surface less bound (proportional to surface area)
- Coulomb term: proton-proton electrostatic repulsion
- Asymmetry term: prefers N ≈ Z for stability
- Pairing term: even numbers of protons/neutrons more stable

### Binding Energy Curve

**Maximum binding energy per nucleon:**
```
Peak at ⁵⁶Fe and ⁵⁸Ni:
  E_B/A ≈ 8.8 MeV (most tightly bound nuclei)

Light nuclei (A < 60):
  Fusion releases energy (moving up curve)

Heavy nuclei (A > 60):
  Fission releases energy (moving up curve via splitting)
```

**Selected binding energies per nucleon:**
```
²H (deuterium):     E_B/A = 1.112 MeV (weakly bound)
⁴He (alpha):        E_B/A = 7.074 MeV (tightly bound)
¹²C:                E_B/A = 7.680 MeV
¹⁶O:                E_B/A = 7.976 MeV
⁵⁶Fe:               E_B/A = 8.790 MeV (peak)
²³⁸U:               E_B/A = 7.570 MeV
```

## Neutron Properties

### Free Neutron Decay

**Decay mode:**
```
n → p + e⁻ + ν̄_e (β⁻ decay)
```

**Decay parameters:**
```
Half-life: t₁/₂ = 879.4 ± 0.6 s
Mean lifetime: τ = t₁/₂ / ln(2) = 1268.6 s ≈ 21.1 minutes
Decay constant: λ = ln(2) / t₁/₂ = 7.88 × 10⁻⁴ s⁻¹
```

**Q-value:**
```
Q = (m_n - m_p - m_e) c²
Q = (1.008665 - 1.007276 - 0.000549) × 931.494
Q = 0.782 MeV

Maximum electron kinetic energy: 0.782 MeV
Average electron kinetic energy: ~0.260 MeV (1/3 of maximum for allowed β decay)
Antineutrino carries remainder (not detectable)
```

**MCNP Implications:**
- Neutron decay negligible in most simulations
  - For 1 MeV neutron: time to thermalize ~1 μs ≪ τ
  - For thermal neutron: diffusion time ~1 ms ≪ τ
- Only matters for:
  - Ultracold neutron (UCN) storage experiments
  - Neutron lifetime measurements
  - Cosmological nucleosynthesis

### Thermal Neutron (Standard Definition)

**Temperature and energy:**
```
Standard temperature: T = 293.6 K (20.44°C)

Thermal energy (most probable in M-B distribution):
  E_th = k_B T = 0.0253 eV = 2.53 × 10⁻⁸ MeV

Average energy:
  E_avg = (3/2) k_B T = 0.0380 eV
```

**Velocity:**
```
Most probable speed:
  v_th = sqrt(2 k_B T / m_n) = 2200 m/s

Average speed:
  v_avg = sqrt(8 k_B T / (π m_n)) = 2546 m/s

RMS speed:
  v_rms = sqrt(3 k_B T / m_n) = 2693 m/s
```

**Wavelength:**
```
De Broglie wavelength at E_th:
  λ = h / p = h / (m v_th)
  λ = 1.798 Å (comparable to atomic spacing in solids)
```

**MCNP standard:**
- Most cross-section libraries tabulated at 293.6 K
- Thermal scattering S(α,β) data at this temperature
- Reference energy for thermal reactor physics

### Neutron Temperature Regimes

```
Ultra-cold neutrons (UCN):  E < 300 neV   (T < 3.5 mK)
Very cold neutrons (VCN):   300 neV - 25 μeV
Cold neutrons:              25 μeV - 25 meV    (T < 290 K)
Thermal neutrons:           25 meV (0.025 eV)  (T ≈ 290 K)
Epithermal neutrons:        0.025 eV - 1 eV
Cadmium cutoff:             ~0.5 eV
Resonance region:           1 eV - 1 keV
Intermediate:               1 keV - 100 keV
Fast neutrons:              100 keV - 20 MeV
High-energy neutrons:       > 20 MeV
```

## Fission

### Energy Release in U-235 Thermal Fission

**Total energy per fission:**
```
E_total ≈ 200 MeV

Breakdown:
  Fission fragments kinetic energy:     167 MeV   (83.5%)
  Prompt neutron kinetic energy:        5 MeV     (2.5%)
  Prompt gamma rays:                    7 MeV     (3.5%)
  Beta decay of fission products:       7 MeV     (3.5%)
  Antineutrinos:                        12 MeV    (6.0%) - not deposited
  Delayed gamma rays:                   6 MeV     (3.0%)

Recoverable energy (excluding neutrinos):
  E_recoverable ≈ 188 MeV
```

**Energy deposition timeline:**
```
Prompt (< 1 μs):
  Fission fragments: 167 MeV
  Prompt neutrons: 5 MeV
  Prompt gammas: 7 MeV
  Total prompt: 179 MeV (90%)

Delayed (minutes to years):
  Beta decay: 7 MeV
  Delayed gammas: 6 MeV
  Total delayed: 13 MeV (6.5%)
  (Neutrinos: 12 MeV, not deposited)
```

**Practical heating values:**
```
Prompt heating: 179 MeV (released immediately in reactor)
Total heating: 192 MeV (includes delayed, excludes neutrinos)

For reactor power calculations:
  Use 200 MeV per fission (conservative)
  Or 192-195 MeV (more accurate, accounts for neutrinos)
```

### Neutrons per Fission (ν)

**Thermal fission (E_n = 0.0253 eV):**
```
U-233:  ν = 2.49 ± 0.01
U-235:  ν = 2.43 ± 0.01
Pu-239: ν = 2.87 ± 0.01
Pu-241: ν = 2.93 ± 0.01
```

**Fast fission (E_n = 1 MeV):**
```
U-235:  ν = 2.52
U-238:  ν = 2.60  (threshold ~1 MeV for fission)
Pu-239: ν = 2.98
```

**Energy dependence (approximate):**
```
ν(E) ≈ ν_thermal + (dν/dE) × E

For U-235:
  ν(E) ≈ 2.43 + 0.15 × E (MeV)

At E = 14 MeV (D-T fusion neutron):
  ν ≈ 2.43 + 0.15 × 14 = 4.53 neutrons/fission
```

**Prompt vs Delayed Neutrons:**
```
Prompt neutrons: 99.3-99.7% (released within 10⁻¹⁴ s)
Delayed neutrons: 0.3-0.7% (released seconds to minutes later)

Delayed neutron fraction (β):
  U-235: β = 0.0065 (0.65%)
  Pu-239: β = 0.0021 (0.21%)

Critical for reactor control (enables human response time)
```

### Fission Cross Sections

**Thermal cross sections (E = 0.0253 eV):**
```
U-233:
  σ_fission = 531 barns
  σ_absorption = 578 barns
  α (capture/fission) = 0.09

U-235:
  σ_fission = 585 barns
  σ_absorption = 681 barns
  α = 0.164
  η (neutrons per absorption) = 2.07

Pu-239:
  σ_fission = 748 barns
  σ_absorption = 1017 barns
  α = 0.36
  η = 2.11

Pu-241:
  σ_fission = 1011 barns
  σ_absorption = 1377 barns
```

**Fast fission (E = 1 MeV):**
```
U-235: σ_f ≈ 1.2 barns
U-238: σ_f ≈ 0.3 barns
Pu-239: σ_f ≈ 1.8 barns
```

### Mass Number Distribution of Fission Products

**Asymmetric fission (thermal U-235):**
```
Light fragment peak: A ≈ 95 (mass yield ~6%)
Heavy fragment peak: A ≈ 137 (mass yield ~6%)

Symmetric fission (A ≈ 117): very rare (~0.01%)

Most probable mass split: ~95 + 138 = 233 (loses 3 neutrons)
```

**Energy distribution of fragments:**
```
Light fragment (A ≈ 95): E ≈ 100 MeV
Heavy fragment (A ≈ 137): E ≈ 67 MeV
Total KE ≈ 167 MeV (momentum conserved)
```

## Fusion

### D-D Fusion Reactions

**Reaction 1 (50% probability):**
```
²H + ²H → ³He + n
Q = 3.27 MeV

Energy distribution:
  Neutron: 2.45 MeV
  ³He: 0.82 MeV
```

**Reaction 2 (50% probability):**
```
²H + ²H → ³H + p
Q = 4.03 MeV

Energy distribution:
  Proton: 3.02 MeV
  Tritium: 1.01 MeV
```

**Combined D-D fusion:**
```
Average Q-value: (3.27 + 4.03) / 2 = 3.65 MeV

Net reaction (combining both branches):
  6 ²H → 2 ³He + 2 ³H + 2 p + 2 n + 21.6 MeV
```

### D-T Fusion (Primary Fusion Reaction)

**Reaction:**
```
²H + ³H → ⁴He + n
Q = 17.6 MeV

Energy distribution (momentum conservation):
  Neutron: 14.1 MeV (80% of Q)
  Alpha: 3.5 MeV (20% of Q)
```

**Cross-section peak:**
```
Maximum at E ≈ 64 keV (deuteron energy in lab frame)
σ_max ≈ 5 barns

Much higher than D-D (σ_DD ≈ 0.1 barn at 64 keV)
```

**MCNP Applications:**
```
D-T fusion neutron source:
  SDEF  PAR=1  ERG=14.1    $ 14.1 MeV neutron

D-T fusion alpha source:
  SDEF  PAR=H  ERG=3.5     $ 3.5 MeV alpha (MODE H)
```

### D-³He Fusion

**Reaction:**
```
²H + ³He → ⁴He + p
Q = 18.3 MeV

Energy distribution:
  Proton: 14.7 MeV
  Alpha: 3.6 MeV
```

**Advantages:**
- Aneutronic (no neutron production)
- Lower radioactivity
- Direct energy conversion possible (charged products)

**Disadvantages:**
- ³He very rare (requires breeding from tritium)
- Higher ignition temperature required

### T-T Fusion

**Reaction:**
```
³H + ³H → ⁴He + 2n
Q = 11.3 MeV
```

**Notes:**
- Less likely than D-T in D-T fuel mix
- Contributes additional neutrons

### Fusion Reaction Rates

**Reactivity parameter <σv> (at temperature T):**
```
For D-T at T = 10 keV:
  <σv> ≈ 1.1 × 10⁻²² m³/s

For D-D at T = 10 keV:
  <σv> ≈ 5 × 10⁻²⁵ m³/s (much smaller)
```

**Fusion power density:**
```
P_fusion = (1/4) n²_fuel <σv> Q

For D-T at n_fuel = 10²⁰ m⁻³, T = 10 keV:
  P ≈ 48 MW/m³
```

## Radioactive Decay

### Decay Law

**Activity (decay rate):**
```
A(t) = A₀ e^(-λt) = λN(t)

where:
  A = activity (decays per unit time)
  A₀ = initial activity
  λ = decay constant
  N = number of radioactive atoms
  t = time
```

**Decay constant and half-life:**
```
λ = ln(2) / t₁/₂ = 0.693147 / t₁/₂

t₁/₂ = ln(2) / λ = 0.693147 / λ
```

**Mean lifetime:**
```
τ = 1 / λ = t₁/₂ / ln(2) = 1.44270 × t₁/₂
```

### Activity Units

**Becquerel (SI):**
```
1 Bq = 1 decay/second
```

**Curie (traditional):**
```
1 Ci = 3.7 × 10¹⁰ Bq = 3.7 × 10¹⁰ decay/s

Based on approximately ¹ gram of ²²⁶Ra activity
```

**Conversions:**
```
1 Ci = 3.7 × 10¹⁰ Bq
1 mCi = 3.7 × 10⁷ Bq
1 μCi = 3.7 × 10⁴ Bq = 37,000 Bq
1 Bq = 2.703 × 10⁻¹¹ Ci ≈ 27 pCi
```

### Specific Activity

**Definition:**
```
A_specific = λN_A / A_mass

where:
  λ = decay constant (s⁻¹)
  N_A = Avogadro's number (6.022 × 10²³ mol⁻¹)
  A_mass = atomic/molecular mass (g/mol)

In terms of half-life:
  A_specific = (ln(2) × N_A) / (t₁/₂ × A_mass)
  A_specific = (4.17 × 10²³) / (t₁/₂ × A_mass)  [Bq/g]

where t₁/₂ is in seconds
```

**Example - Co-60:**
```
t₁/₂ = 5.27 years = 1.663 × 10⁸ s
A_mass = 60 g/mol
λ = 0.693 / 1.663×10⁸ = 4.17 × 10⁻⁹ s⁻¹

A_specific = (4.17×10⁻⁹ × 6.022×10²³) / 60
A_specific = 4.18 × 10¹³ Bq/g = 1,129 Ci/g

1 gram of pure Co-60 has activity 1,129 Ci
```

**Example - Pu-239:**
```
t₁/₂ = 24,110 years = 7.61 × 10¹¹ s
A_mass = 239 g/mol

A_specific = (4.17×10²³) / (7.61×10¹¹ × 239)
A_specific = 2.30 × 10⁹ Bq/g = 62.1 mCi/g

1 gram of Pu-239 has activity 62.1 mCi (relatively low)
```

### Decay Chains

**Series decay (A → B → C):**
```
N_A(t) = N_A(0) e^(-λ_A t)

N_B(t) = (λ_A / (λ_B - λ_A)) N_A(0) [e^(-λ_A t) - e^(-λ_B t)] + N_B(0) e^(-λ_B t)

For long chains, use Bateman equations
```

**Secular equilibrium (λ_A ≪ λ_B):**
```
After equilibrium established:
  A_B = A_A (activity of daughter equals parent)
  N_B = (λ_A / λ_B) N_A

Example: ²²⁶Ra → ²²²Rn
  t₁/₂(Ra) = 1600 years ≫ t₁/₂(Rn) = 3.8 days
  After ~1 month, A_Rn ≈ A_Ra
```

**Transient equilibrium (λ_A < λ_B):**
```
After several half-lives of daughter:
  A_B = (λ_B / (λ_B - λ_A)) A_A > A_A

Example: ⁹⁹Mo → ⁹⁹ᵐTc
  t₁/₂(Mo) = 66 h, t₁/₂(Tc) = 6 h
  A_Tc ≈ 1.1 × A_Mo at equilibrium
```

## Radiation Yield and Energy

### Alpha Decay

**Typical energies:**
```
Natural alpha emitters: 4-6 MeV
²³⁸Pu: 5.50 MeV
²³⁹Pu: 5.16 MeV
²⁴¹Am: 5.49 MeV
²²²Rn: 5.49 MeV
²¹⁰Po: 5.30 MeV
```

**Q-value calculation:**
```
Q = (M_parent - M_daughter - M_alpha) c²

Kinetic energies (momentum conservation):
  E_α = Q × M_daughter / (M_alpha + M_daughter)
  E_recoil = Q × M_alpha / (M_alpha + M_daughter)

For heavy nuclei (M_daughter ≫ M_alpha):
  E_α ≈ Q × (1 - 4/A)  where A ≈ M_daughter
  E_recoil ≈ Q × (4/A)
```

### Beta Decay

**Maximum energies (endpoint):**
```
³H → ³He + e⁻ + ν̄:     E_max = 18.6 keV
¹⁴C → ¹⁴N + e⁻ + ν̄:    E_max = 156 keV
³²P → ³²S + e⁻ + ν̄:    E_max = 1.71 MeV
⁹⁰Sr → ⁹⁰Y + e⁻ + ν̄:   E_max = 546 keV
⁹⁰Y → ⁹⁰Zr + e⁻ + ν̄:   E_max = 2.28 MeV
¹³⁷Cs → ¹³⁷ᵐBa + e⁻ + ν̄: E_max = 514 keV
```

**Average beta energy:**
```
For allowed transitions:
  E_avg ≈ E_max / 3

For forbidden transitions:
  E_avg ≈ (0.3 to 0.4) × E_max
```

### Gamma Decay

**Common gamma energies:**
```
²⁴¹Am: 59.5 keV
¹³³Ba: 356 keV
⁶⁰Co: 1.17 MeV and 1.33 MeV (cascade)
¹³⁷Cs (via ¹³⁷ᵐBa): 662 keV
⁵⁴Mn: 835 keV
²²Na: 511 keV (β⁺ annihilation) + 1.27 MeV
```

**Fission product gammas:**
```
Delayed gammas: continuous spectrum, ~0.1-3 MeV
Total energy: ~6 MeV per fission (over time)
Important for decay heat in shutdown reactor
```

## MCNP Applications

### Reactor Power Calculations

**Power from fission rate:**
```
P (watts) = (fission rate) × (energy per fission) × (1.602×10⁻¹³ J/MeV)

Using 200 MeV/fission:
  P = F × 200 × 1.602×10⁻¹³
  P = F × 3.204×10⁻¹¹ watts

where F = fissions per second
```

**Fission rate from power:**
```
F = P / (200 × 1.602×10⁻¹³)
F = P / 3.204×10⁻¹¹
F ≈ 3.12×10¹⁰ P  (fissions/second per watt)

For 1 MW reactor:
  F = 3.12×10¹⁶ fissions/second
```

**Fuel consumption:**
```
Mass consumption rate:
  dm/dt = (F × M_fuel) / (N_A × ν)

For U-235 at 1 MW:
  F = 3.12×10¹⁶ fissions/s
  dm/dt = (3.12×10¹⁶ × 235) / (6.022×10²³)
  dm/dt = 1.22×10⁻⁵ g/s = 1.05 g/day ≈ 385 g/year

Rule of thumb: ~1 g U-235/day per MW thermal
```

### Source Definition

**Spontaneous fission neutron source (Cf-252):**
```
SDEF  PAR=SF  ERG=D1
SI1 H  0 0.5 1 1.5 ... 10    $ Energy bins
SP1 D  (Watt fission spectrum values)

Cf-252 neutrons per fission: ν = 3.77
Spontaneous fission rate: depends on mass and age
```

**Am-Be (α,n) source:**
```
²⁴¹Am α decay → ⁹Be(α,n)¹²C
Continuous spectrum, average ~4.5 MeV
Yield: ~60-70 neutrons per 10⁶ alphas

SDEF  PAR=1  ERG=D1  $ AmBe spectrum
```

### Decay Heat (MCNP BURN or standalone calculation)

**Fission product decay heat:**
```
After shutdown from power P₀:
  P(t) = P₀ × [0.066 t⁻⁰·² - 0.0013 t⁻⁰·⁴]  (for t in seconds, P₀ in watts)

Example: 1000 MW reactor, 1 hour after shutdown:
  t = 3600 s
  P = 1000 × [0.066 × 3600⁻⁰·² - 0.0013 × 3600⁻⁰·⁴]
  P ≈ 18 MW (~1.8% of operating power)
```

## References

### Nuclear Data Sources

**NNDC (National Nuclear Data Center):**
- https://www.nndc.bnl.gov/
- Nuclide charts, decay data, Q-values

**IAEA Nuclear Data Services:**
- https://www-nds.iaea.org/
- ENDF libraries, thermal scattering

**JANIS (Java-based Nuclear Information Software):**
- https://www.oecd-nea.org/janis/
- Cross-section visualization

### Textbook References

**Nuclear Physics:**
- Krane, "Introductory Nuclear Physics"
- Evans, "The Atomic Nucleus"

**Reactor Physics:**
- Lamarsh, "Introduction to Nuclear Reactor Theory"
- Duderstadt & Hamilton, "Nuclear Reactor Analysis"

### Related MCNP Skills

- **mcnp-physical-constants**: Fundamental constants
- **mcnp-particle-properties**: Particle masses
- **mcnp-isotope-lookup**: Isotope data and ZAIDs
- **mcnp-material-builder**: Uses decay/activation data
- **mcnp-source-builder**: Neutron/photon source energies
- **mcnp-burnup-builder**: Depletion and activation calculations

---

**End of Nuclear Constants Reference**
