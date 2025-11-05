---
category: F
name: mcnp-physical-constants
description: Lookup fundamental physical constants, particle properties, and nuclear data needed for MCNP calculations including conversion factors, masses, energies, and cross-section benchmarks
activation_keywords:
  - physical constants
  - fundamental constants
  - particle mass
  - speed of light
  - Planck constant
  - Boltzmann constant
  - Avogadro number
  - electron mass
  - neutron mass
  - conversion factor
---

# MCNP Physical Constants Skill

## Purpose

This utility skill provides quick reference to fundamental physical constants, particle properties, and nuclear data required for MCNP calculations. Ensures accurate values for density calculations, energy conversions, cross-section interpretations, and physics validations.

## When to Use This Skill

- Looking up Avogadro's number for atom density calculations
- Finding particle masses for energy-mass conversions
- Retrieving Boltzmann constant for temperature conversions
- Checking speed of light for relativistic calculations
- Getting neutron/proton masses for Q-value calculations
- Finding conversion factors between units
- Verifying cross-section typical values
- Calculating fission energy releases
- Determining decay constants from half-lives
- Validating calculated values against known benchmarks

## Prerequisites

- **mcnp-unit-converter**: Uses conversion factors
- **mcnp-isotope-lookup**: Uses particle masses
- **mcnp-material-builder**: Uses Avogadro's number
- Basic physics and nuclear engineering knowledge
- Understanding of SI and CGS unit systems

## Core Concepts

### Fundamental Physical Constants (CODATA 2018)

**Universal Constants**:
```
Speed of light in vacuum:
  c = 299,792,458 m/s (exact, by definition)
  c = 2.99792458 × 10¹⁰ cm/s

Planck constant:
  h = 6.62607015 × 10⁻³⁴ J·s (exact, by definition)
  ℏ = h/(2π) = 1.054571817 × 10⁻³⁴ J·s

Boltzmann constant:
  k_B = 1.380649 × 10⁻²³ J/K (exact, by definition)
  k_B = 8.617333262 × 10⁻⁵ eV/K
  k_B = 8.617333262 × 10⁻¹¹ MeV/K

Elementary charge:
  e = 1.602176634 × 10⁻¹⁹ C (exact, by definition)

Avogadro constant:
  N_A = 6.02214076 × 10²³ mol⁻¹ (exact, by definition)
```

**Gravitational and Electromagnetic**:
```
Gravitational constant:
  G = 6.67430 × 10⁻¹¹ m³/(kg·s²)

Permittivity of free space:
  ε₀ = 8.8541878128 × 10⁻¹² F/m

Permeability of free space:
  μ₀ = 1.25663706212 × 10⁻⁶ N/A²

Fine structure constant:
  α = 7.2973525693 × 10⁻³ ≈ 1/137.036
```

### Particle Rest Masses

**Leptons**:
```
Electron:
  m_e = 9.1093837015 × 10⁻³¹ kg
  m_e = 5.48579909065 × 10⁻⁴ amu
  m_e c² = 0.51099895000 MeV

Muon:
  m_μ = 1.883531627 × 10⁻²⁸ kg
  m_μ c² = 105.6583755 MeV

Tau:
  m_τ = 3.16754 × 10⁻²⁷ kg
  m_τ c² = 1776.86 MeV
```

**Nucleons**:
```
Proton:
  m_p = 1.67262192369 × 10⁻²⁷ kg
  m_p = 1.007276466621 amu
  m_p c² = 938.27208816 MeV

Neutron:
  m_n = 1.67492749804 × 10⁻²⁷ kg
  m_n = 1.00866491595 amu
  m_n c² = 939.56542052 MeV

Deuteron (²H nucleus):
  m_d = 3.3435837724 × 10⁻²⁷ kg
  m_d = 2.013553212745 amu
  m_d c² = 1875.61294257 MeV
```

**Composite Particles**:
```
Alpha particle (⁴He nucleus):
  m_α = 6.6446573357 × 10⁻²⁷ kg
  m_α = 4.001506179129 amu
  m_α c² = 3727.3794066 MeV

Helium-3 nucleus:
  m_³He = 5.0064127862 × 10⁻²⁷ kg
  m_³He c² = 2808.39160743 MeV
```

### Atomic Mass Unit (amu)

**Definition**:
```
1 amu = 1/12 of mass of ¹²C atom (exact)
1 amu = 1.66053906660 × 10⁻²⁷ kg
1 amu = 1.66053906660 × 10⁻²⁴ g
1 amu = 931.49410242 MeV/c²

Conversion:
  Energy (MeV) = mass (amu) × 931.494102
```

**Example - Mass Defect**:
```
²H (deuterium) mass:
  Constituents: 1 proton + 1 neutron
  Sum: 1.007276 + 1.008665 = 2.015941 amu
  Actual ²H mass: 2.014102 amu
  Mass defect: Δm = 0.001839 amu
  Binding energy: EB = 0.001839 × 931.494 = 1.71 MeV
```

### Energy-Related Constants

**Energy Conversion**:
```
1 eV = 1.602176634 × 10⁻¹⁹ J (exact)
1 MeV = 1.602176634 × 10⁻¹³ J

1 J = 6.241509074 × 10¹² MeV

Temperature-Energy relation:
  1 eV = 11604.518 K
  1 K = 8.617333 × 10⁻⁵ eV

Room temperature (T = 293 K):
  kT = 0.0253 eV = 2.53 × 10⁻⁸ MeV (thermal neutron energy)
```

**Wavelength-Energy Relation**:
```
E (eV) = hc / λ = 12398.419843 / λ (Å)

Example: 1 Å X-ray
  E = 12398.4 / 1 = 12.398 keV
```

### Nuclear Constants

**Neutron Properties**:
```
Neutron decay:
  Mode: β⁻ → proton + electron + antineutrino
  Half-life: 879.4 ± 0.6 seconds (14.66 min)
  Decay constant: λ = 7.88 × 10⁻⁴ s⁻¹

Thermal neutron (at 20°C):
  Energy: E_th = 0.0253 eV
  Speed: v_th = 2200 m/s
  Wavelength: λ = 1.80 Å
```

**Fission Constants**:
```
Energy per U-235 fission:
  Total: ~200 MeV
  Breakdown:
    Fission fragments: ~167 MeV
    Prompt neutrons: ~5 MeV
    Prompt gammas: ~7 MeV
    Beta decay: ~7 MeV
    Neutrinos: ~12 MeV (not deposited)
    Delayed gammas: ~6 MeV

  Recoverable: ~188 MeV (excluding neutrinos)

Neutrons per fission (ν):
  U-235 thermal: ν = 2.43
  U-238 fast: ν = 2.60
  Pu-239 thermal: ν = 2.87
```

**Cross-Section Benchmarks**:
```
Barn definition:
  1 barn (b) = 10⁻²⁴ cm²

Typical thermal cross sections (at 0.0253 eV):
  H-1 scatter: σ_s = 20.5 b
  H-1 absorption: σ_a = 0.332 b
  C-12 scatter: σ_s = 4.75 b
  U-235 fission: σ_f = 585 b
  U-235 absorption: σ_a = 681 b
  Pu-239 fission: σ_f = 748 b
  Cd-113 absorption: σ_a = 20,600 b
  Xe-135 absorption: σ_a = 2,650,000 b (strongest)
```

### Decay and Activity

**Decay Constant**:
```
λ = ln(2) / t₁/₂
λ = 0.693147 / t₁/₂

Activity: A = λN
where N = number of atoms

Units:
  1 Becquerel (Bq) = 1 decay/second
  1 Curie (Ci) = 3.7 × 10¹⁰ Bq
```

**Specific Activity**:
```
A_specific = (λ × N_A) / A_mass

where:
  A_mass = atomic mass (g/mol)
  λ = decay constant (s⁻¹)
  N_A = Avogadro's number

Example - Co-60:
  t₁/₂ = 5.27 yr = 1.66 × 10⁸ s
  λ = 0.693 / 1.66×10⁸ = 4.17 × 10⁻⁹ s⁻¹
  A_specific = (4.17×10⁻⁹ × 6.022×10²³) / 60
  A_specific = 4.18 × 10¹³ Bq/g = 1129 Ci/g
```

## Tool Invocation

This skill includes a Python implementation for physical constants lookup and unit conversions.

### Importing the Tool

```python
from mcnp_physical_constants import MCNPPhysicalConstants
constants = MCNPPhysicalConstants()
```

### Basic Usage

```python
# Get fundamental constants
c = constants.get_speed_of_light()  # cm/s
N_A = constants.get_avogadro()  # 1/mol

# Perform unit conversions
temp_mev = constants.kelvin_to_mev(600)  # K → MeV
energy_j = constants.mev_to_joules(14.1)  # MeV → J
```

### Integration with MCNP Workflow

```python
from mcnp_physical_constants import MCNPPhysicalConstants

constants = MCNPPhysicalConstants()

# Calculate atom density
density_g_cm3 = 2.7  # Al
atomic_weight = 26.982
atom_density = constants.calc_atom_density(density_g_cm3, atomic_weight)
print(f"Atom density: {atom_density:.5f} atoms/b-cm")
```

---

## Use Case 1: Calculate Atom Density from Mass Density

**Problem**: Steel ρ = 7.85 g/cm³, find atom density

**Constants Needed**:
- Avogadro's number: N_A = 6.022 × 10²³ mol⁻¹
- Atomic mass of Fe: A = 55.845 g/mol

**Calculation**:
```
N (atom/cm³) = (ρ × N_A) / A
N = (7.85 g/cm³ × 6.022×10²³ mol⁻¹) / 55.845 g/mol
N = 8.46 × 10²² atoms/cm³

Convert to atom/b-cm:
N (atom/b-cm) = N (atom/cm³) / 10²⁴
N = 8.46 × 10²² / 10²⁴ = 0.0846 atom/b-cm
```

**MCNP Material Card**:
```
c Iron: ρ = 7.85 g/cm³ = 0.0846 atom/b-cm
M1  26000.80c  0.0846      $ Natural iron
c Or use mass density (negative):
10  1  -7.85  -100         $ Cell with mass density
```

## Use Case 2: Convert Temperature to Thermal Energy

**Problem**: Material at 600 K, express as thermal energy

**Constants Needed**:
- Boltzmann constant: k_B = 8.617333 × 10⁻¹¹ MeV/K

**Calculation**:
```
E = k_B × T
E = 8.617333 × 10⁻¹¹ MeV/K × 600 K
E = 5.17 × 10⁻⁸ MeV

Compare to room temperature (293 K):
E_room = 8.617333 × 10⁻¹¹ × 293 = 2.53 × 10⁻⁸ MeV

Ratio: 600 K / 293 K = 2.05× hotter
```

**MCNP Application**:
```
c Material at 600 K
M1  92235.80c  1.0
TMP  600                    $ Temperature in Kelvin
c Or use energy:
TMP  5.17E-8                $ Temperature in MeV
```

## Use Case 3: Calculate Q-Value for Nuclear Reaction

**Problem**: Determine Q-value for ²H(d,n)³He reaction

**Constants Needed**:
- Particle masses (amu):
  - Deuterium (²H): 2.014102
  - Tritium (³H): 3.016049
  - Neutron: 1.008665
  - Helium-3: 3.016029
- Conversion: 1 amu = 931.494 MeV/c²

**Calculation**:
```
Reaction: ²H + ²H → ³He + n

Masses:
  Reactants: 2 × 2.014102 = 4.028204 amu
  Products: 3.016029 + 1.008665 = 4.024694 amu

Mass defect: Δm = 4.028204 - 4.024694 = 0.003510 amu

Q-value: Q = Δm × 931.494 MeV/amu
Q = 0.003510 × 931.494 = 3.27 MeV

Interpretation: 3.27 MeV energy released (exothermic)
```

**MCNP Fusion Source**:
```
c D-D fusion neutron energy
c Q = 3.27 MeV shared between products
c Neutron gets: E_n ≈ 2.45 MeV (by momentum conservation)
SDEF  PAR=1  ERG=2.45      $ D-D fusion neutron
```

## Use Case 4: Verify Fission Energy Release

**Problem**: Check if calculated fission energy reasonable

**Constant Needed**:
- Energy per U-235 fission: ~200 MeV

**Calculation**:
```
Power = Energy per fission × fission rate

Example: 1 MW thermal power
  1 MW = 1 × 10⁶ J/s = 6.242 × 10¹⁸ MeV/s

Fission rate = Power / Energy per fission
Fission rate = 6.242 × 10¹⁸ MeV/s / 200 MeV
Fission rate = 3.12 × 10¹⁶ fissions/s

Mass consumption:
  N_fissions = 3.12 × 10¹⁶ fissions/s
  Atoms per gram U-235 = 6.022×10²³ / 235 = 2.56 × 10²¹

  Consumption = 3.12 × 10¹⁶ / 2.56 × 10²¹
  Consumption = 1.22 × 10⁻⁵ g/s = 1.05 g/day
```

**Verification**:
```
Rule of thumb: 1 MW ≈ 1 g U-235/day
Calculated: 1.05 g/day ✓ Close to benchmark
```

## Use Case 5: Calculate Neutron Speed from Energy

**Problem**: Thermal neutron at 0.0253 eV, find speed

**Constants Needed**:
- Neutron mass: m_n = 1.675 × 10⁻²⁷ kg
- Energy conversion: 1 eV = 1.602 × 10⁻¹⁹ J

**Calculation**:
```
Non-relativistic: E = ½mv²

v = sqrt(2E / m)

E = 0.0253 eV × 1.602×10⁻¹⁹ J/eV = 4.05 × 10⁻²¹ J

v = sqrt(2 × 4.05×10⁻²¹ J / 1.675×10⁻²⁷ kg)
v = sqrt(4.84 × 10⁶)
v = 2200 m/s

Benchmark: Thermal neutrons at 20°C = 2200 m/s ✓
```

**MCNP Context**:
```
c Thermal neutron source (room temperature)
SDEF  PAR=1  ERG=2.53E-8   $ 0.0253 eV = 2.53×10⁻⁸ MeV
c Neutron velocity ~ 2200 m/s
```

## Integration with Other Skills

### 1. **mcnp-unit-converter**
Provides conversion factors between units.

### 2. **mcnp-material-builder**
Uses Avogadro's number and atomic masses.

### 3. **mcnp-isotope-lookup**
Uses particle masses and decay constants.

### 4. **mcnp-source-builder**
Uses particle energies and decay data.

### 5. **mcnp-physics-builder**
Uses Boltzmann constant for temperature.

## Quick Reference Tables

### Fundamental Constants
| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Speed of light | c | 2.998×10⁸ | m/s |
| Planck constant | h | 6.626×10⁻³⁴ | J·s |
| Boltzmann constant | k_B | 1.381×10⁻²³ | J/K |
| | k_B | 8.617×10⁻⁵ | eV/K |
| Elementary charge | e | 1.602×10⁻¹⁹ | C |
| Avogadro constant | N_A | 6.022×10²³ | mol⁻¹ |

### Particle Masses
| Particle | Mass (kg) | Mass (amu) | Rest Energy (MeV) |
|----------|-----------|------------|-------------------|
| Electron | 9.109×10⁻³¹ | 5.486×10⁻⁴ | 0.511 |
| Proton | 1.673×10⁻²⁷ | 1.00728 | 938.272 |
| Neutron | 1.675×10⁻²⁷ | 1.00866 | 939.565 |
| Deuteron | 3.344×10⁻²⁷ | 2.01355 | 1875.613 |
| Alpha | 6.645×10⁻²⁷ | 4.00151 | 3727.379 |

### Energy Conversions
| From | To | Factor |
|------|-----|--------|
| eV | J | 1.602×10⁻¹⁹ |
| J | eV | 6.242×10¹⁸ |
| amu | MeV/c² | 931.494 |
| eV | K | 11604.5 |
| K | eV | 8.617×10⁻⁵ |

### Nuclear Benchmarks
| Quantity | Value | Notes |
|----------|-------|-------|
| Thermal neutron energy | 0.0253 eV | At 20°C |
| Thermal neutron speed | 2200 m/s | At 20°C |
| U-235 fission energy | 200 MeV | Total released |
| Neutrons per U-235 fission | 2.43 | Thermal |
| 1 barn | 10⁻²⁴ cm² | Cross section unit |
| 1 Curie | 3.7×10¹⁰ Bq | Activity unit |

## Best Practices

1. **Use CODATA Values**: Reference CODATA 2018 for constants
2. **Maintain Precision**: Keep adequate significant figures
3. **Verify Calculations**: Cross-check with known benchmarks
4. **Document Sources**: Note where constants obtained
5. **Use Consistent Units**: Convert early, calculate in one system
6. **Check Reasonableness**: Compare results to typical values
7. **Update Periodically**: Constants refined over time
8. **Reference This Skill**: Link calculations to constant source

## References

- **CODATA 2018**: Recommended values of fundamental physical constants
- **NIST Physical Constants**: https://physics.nist.gov/cuu/Constants/
- **Particle Data Group**: pdg.lbl.gov (particle properties)
- **NNDC**: www.nndc.bnl.gov (nuclear data)
- **Related Skills**:
  - mcnp-unit-converter
  - mcnp-isotope-lookup
  - mcnp-material-builder

---

**End of MCNP Physical Constants Skill**
