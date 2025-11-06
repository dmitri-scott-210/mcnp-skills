# MCNP Unit Conversion Tables

Comprehensive conversion factors for all unit systems used in MCNP simulations. Use these tables for manual conversions or to verify automated conversion tool results.

---

## Table of Contents

1. [Energy Conversions](#energy-conversions)
2. [Length Conversions](#length-conversions)
3. [Density Conversions](#density-conversions)
4. [Temperature Conversions](#temperature-conversions)
5. [Cross Section Conversions](#cross-section-conversions)
6. [Activity Conversions](#activity-conversions)
7. [Mass Conversions](#mass-conversions)
8. [Time Conversions](#time-conversions)
9. [Angle Conversions](#angle-conversions)
10. [Physical Constants](#physical-constants)

---

## Energy Conversions

### Energy Unit Conversion Matrix

| From ↓ To → | eV | keV | MeV | GeV | J |
|-------------|-----|-----|-----|-----|-----|
| **eV** | 1 | 10⁻³ | 10⁻⁶ | 10⁻⁹ | 1.602×10⁻¹⁹ |
| **keV** | 10³ | 1 | 10⁻³ | 10⁻⁶ | 1.602×10⁻¹⁶ |
| **MeV** | 10⁶ | 10³ | 1 | 10⁻³ | 1.602×10⁻¹³ |
| **GeV** | 10⁹ | 10⁶ | 10³ | 1 | 1.602×10⁻¹⁰ |
| **J** | 6.242×10¹⁸ | 6.242×10¹⁵ | 6.242×10¹² | 6.242×10⁹ | 1 |

### Common Energy Values

| Energy | eV | keV | MeV | Description |
|--------|-----|-----|-----|-------------|
| Thermal neutron (20°C) | 0.0253 | 2.53×10⁻⁵ | 2.53×10⁻⁸ | Room temperature thermal energy |
| Epithermal neutron | 1.0 | 0.001 | 10⁻⁶ | Slowing down region |
| Fission neutron (avg) | 2×10⁶ | 2000 | 2.0 | Average fission neutron |
| D-T fusion neutron | 1.41×10⁷ | 14,100 | 14.1 | Deuterium-tritium fusion |
| U-235 fission energy | 2.0×10⁸ | 2×10⁵ | 200 | Energy per fission event |
| Cs-137 gamma | 6.62×10⁵ | 662 | 0.662 | Common calibration source |
| Co-60 gamma (high) | 1.33×10⁶ | 1332 | 1.332 | High energy gamma |
| Electron rest mass | 5.11×10⁵ | 511 | 0.511 | m₀c² for electron |

### Energy-Wavelength-Frequency Relations

For photons:
- **E (eV) = 1240 / λ (nm)**
- **E (eV) = 12398.4 / λ (Å)**
- **E (J) = h × ν = (6.626×10⁻³⁴) × ν (Hz)**
- **λ (m) = c / ν = 3×10⁸ / ν (Hz)**

---

## Length Conversions

### Length Unit Conversion Matrix

| From ↓ To → | cm | m | mm | μm | inch | foot | Angstrom |
|-------------|-----|-----|-----|-----|------|------|----------|
| **cm** | 1 | 0.01 | 10 | 10⁴ | 0.3937 | 0.03281 | 10⁸ |
| **m** | 100 | 1 | 1000 | 10⁶ | 39.37 | 3.281 | 10¹⁰ |
| **mm** | 0.1 | 0.001 | 1 | 1000 | 0.03937 | 0.003281 | 10⁷ |
| **μm** | 10⁻⁴ | 10⁻⁶ | 0.001 | 1 | 3.937×10⁻⁵ | 3.281×10⁻⁶ | 10⁴ |
| **inch** | 2.54 | 0.0254 | 25.4 | 25,400 | 1 | 0.08333 | 2.54×10⁸ |
| **foot** | 30.48 | 0.3048 | 304.8 | 304,800 | 12 | 1 | 3.048×10⁹ |
| **Angstrom** | 10⁻⁸ | 10⁻¹⁰ | 10⁻⁷ | 10⁻⁴ | 3.937×10⁻⁹ | 3.281×10⁻¹⁰ | 1 |

### Common Dimensions in MCNP (cm)

| Object | Typical Size | cm |
|--------|--------------|-----|
| Neutron mean free path (water) | ~2.5 cm | 2.5 |
| Fuel pin radius | ~0.4 cm | 0.4 |
| Reactor core | ~3 m | 300 |
| Shielding wall | ~1 m | 100 |
| Nuclear radius | ~10⁻¹² cm | 10⁻¹² |
| Atomic radius | ~1 Å | 10⁻⁸ |

---

## Density Conversions

### Mass Density

| From ↓ To → | g/cm³ | kg/m³ | lb/ft³ | lb/in³ |
|-------------|-------|-------|--------|--------|
| **g/cm³** | 1 | 1000 | 62.43 | 0.03613 |
| **kg/m³** | 0.001 | 1 | 0.06243 | 3.613×10⁻⁵ |
| **lb/ft³** | 0.01602 | 16.02 | 1 | 5.787×10⁻⁴ |
| **lb/in³** | 27.68 | 27,680 | 1728 | 1 |

### Atomic/Number Density

**Conversion between mass density and atomic density:**

N (atom/b-cm) = [ρ (g/cm³) × N_A (mol⁻¹)] / [A (g/mol) × 10²⁴]

Where:
- N = atomic density (atom/barn-cm)
- ρ = mass density (g/cm³)
- A = atomic weight (g/mol)
- N_A = 6.02214076 × 10²³ mol⁻¹

**Examples:**

| Material | Mass Density (g/cm³) | Atomic Weight | Atomic Density (atom/b-cm) |
|----------|---------------------|---------------|----------------------------|
| Hydrogen (liq) | 0.0708 | 1.008 | 0.0423 |
| Water | 1.000 | 18.015 | 0.0334 (molecules) |
| Aluminum | 2.699 | 26.982 | 0.0602 |
| Iron | 7.874 | 55.845 | 0.0849 |
| Lead | 11.34 | 207.2 | 0.0330 |
| Uranium | 19.05 | 238.029 | 0.0482 |

### Common Material Densities (g/cm³)

| Material | Density | Notes |
|----------|---------|-------|
| Air (STP) | 0.001205 | 1 atm, 20°C |
| Water | 1.000 | 4°C, maximum density |
| Concrete | 2.3–2.5 | Ordinary concrete |
| Aluminum | 2.699 | Pure Al |
| Steel | 7.85 | Carbon steel |
| Copper | 8.96 | Pure Cu |
| Lead | 11.34 | Pure Pb |
| Tungsten | 19.25 | W metal |
| Uranium (depleted) | 19.05 | Natural U |
| UO₂ | 10.97 | Ceramic fuel (theoretical) |
| MOX fuel | 10.4–11.0 | Mixed oxide fuel |

---

## Temperature Conversions

### Temperature Unit Conversion Formulas

| From | To | Formula |
|------|-----|---------|
| **°C** | K | K = °C + 273.15 |
| **K** | °C | °C = K - 273.15 |
| **°F** | °C | °C = (°F - 32) × 5/9 |
| **°C** | °F | °F = °C × 9/5 + 32 |
| **K** | °F | °F = (K - 273.15) × 9/5 + 32 |
| **°F** | K | K = (°F - 32) × 5/9 + 273.15 |
| **K** | MeV | MeV = K × 8.617333262×10⁻¹¹ |
| **MeV** | K | K = MeV / (8.617333262×10⁻¹¹) |
| **K** | eV | eV = K × 8.617333262×10⁻⁵ |
| **eV** | K | K = eV / (8.617333262×10⁻⁵) |

### Common Temperatures

| Temperature | K | °C | °F | MeV | eV |
|-------------|-----|-----|-----|-----|-----|
| Absolute zero | 0 | -273.15 | -459.67 | 0 | 0 |
| Liquid nitrogen | 77.4 | -195.75 | -320.35 | 6.67×10⁻⁹ | 6.67×10⁻³ |
| Dry ice | 194.65 | -78.5 | -109.3 | 1.68×10⁻⁸ | 0.0168 |
| Water freezing | 273.15 | 0 | 32 | 2.35×10⁻⁸ | 0.0235 |
| Room temperature | 293.15 | 20 | 68 | 2.53×10⁻⁸ | 0.0253 |
| Human body | 310.15 | 37 | 98.6 | 2.67×10⁻⁸ | 0.0267 |
| Water boiling | 373.15 | 100 | 212 | 3.21×10⁻⁸ | 0.0321 |
| Reactor coolant | ~573 | ~300 | ~572 | 4.94×10⁻⁸ | 0.0494 |
| Reactor fuel | ~1200 | ~927 | ~1700 | 1.03×10⁻⁷ | 0.103 |

### Thermal Energy Groups

| Group | Energy (eV) | Temperature (K) | Description |
|-------|-------------|-----------------|-------------|
| Cold | 0.001 | 0.012 | Liquid H₂ |
| Thermal | 0.0253 | 293.6 | Room temp |
| Epithermal | 0.1–1 | 1161–11,605 | Slowing down |
| Fast | 10³–10⁷ | 10⁷–10¹¹ | High energy |

---

## Cross Section Conversions

### Cross Section Unit Conversion Matrix

| From ↓ To → | barn (b) | millibarn (mb) | cm² |
|-------------|----------|----------------|-----|
| **barn** | 1 | 1000 | 10⁻²⁴ |
| **millibarn** | 0.001 | 1 | 10⁻²⁷ |
| **cm²** | 10²⁴ | 10²⁷ | 1 |

### Definition

**1 barn = 10⁻²⁴ cm² = 10⁻²⁸ m² = 100 fm²**

Origin: Approximately the cross-sectional area of a uranium nucleus, considered "as big as a barn" compared to typical nuclear interaction scales.

### Typical Cross Sections

| Reaction | Cross Section (barns) | Energy | Notes |
|----------|----------------------|--------|-------|
| H-1 elastic | 20 | Thermal | High scattering |
| U-235 fission | 585 | Thermal (0.0253 eV) | Very high |
| U-238 fission | 0.00002 | Thermal | Very low |
| U-238 fission | 0.3 | Fast (~1 MeV) | Threshold reaction |
| Pu-239 fission | 742 | Thermal | Higher than U-235 |
| Cd-113 absorption | 20,600 | Thermal | Poison/control |
| Xe-135 absorption | 2.65×10⁶ | Thermal | Major poison |
| B-10 (n,α) | 3837 | Thermal | Detector/poison |
| Gd-157 absorption | 254,000 | Thermal | Burnable poison |

### Macroscopic Cross Section

Σ (cm⁻¹) = σ (barns) × N (atom/b-cm)

Where:
- Σ = macroscopic cross section (cm⁻¹)
- σ = microscopic cross section (barns)
- N = atomic density (atom/b-cm)

**Mean free path:** λ = 1/Σ (cm)

---

## Activity Conversions

### Activity Unit Conversion Matrix

| From ↓ To → | Bq | kBq | MBq | GBq | Ci | mCi | μCi |
|-------------|-----|-----|-----|-----|-----|-----|-----|
| **Bq** | 1 | 10⁻³ | 10⁻⁶ | 10⁻⁹ | 2.703×10⁻¹¹ | 2.703×10⁻⁸ | 2.703×10⁻⁵ |
| **kBq** | 1000 | 1 | 10⁻³ | 10⁻⁶ | 2.703×10⁻⁸ | 2.703×10⁻⁵ | 0.02703 |
| **MBq** | 10⁶ | 1000 | 1 | 10⁻³ | 2.703×10⁻⁵ | 0.02703 | 27.03 |
| **GBq** | 10⁹ | 10⁶ | 1000 | 1 | 0.02703 | 27.03 | 27,030 |
| **Ci** | 3.7×10¹⁰ | 3.7×10⁷ | 3.7×10⁴ | 37 | 1 | 1000 | 10⁶ |
| **mCi** | 3.7×10⁷ | 3.7×10⁴ | 37 | 0.037 | 0.001 | 1 | 1000 |
| **μCi** | 3.7×10⁴ | 37 | 0.037 | 3.7×10⁻⁵ | 10⁻⁶ | 0.001 | 1 |

### Definition

- **Becquerel (Bq):** 1 disintegration/second
- **Curie (Ci):** 3.7 × 10¹⁰ disintegrations/second (originally based on 1 g of Ra-226)

### Common Source Activities

| Source | Typical Activity | Use |
|--------|------------------|-----|
| Smoke detector (Am-241) | 1 μCi (37 kBq) | Ionization chamber |
| Check source (Cs-137) | 10 μCi (370 kBq) | Calibration |
| Radiography source (Ir-192) | 10–100 Ci (0.4–4 TBq) | Industrial NDT |
| Medical isotope (Tc-99m) | 20–30 mCi (0.7–1.1 GBq) | Diagnostic imaging |
| Therapy source (Co-60) | 1000 Ci (37 TBq) | Cancer treatment |
| Spent fuel assembly | 10⁶ Ci (3.7×10¹⁶ Bq) | 1 year cooling |

---

## Mass Conversions

### Mass Unit Conversion Matrix

| From ↓ To → | g | kg | amu | MeV/c² | lb |
|-------------|-----|-----|-----|--------|-----|
| **g** | 1 | 0.001 | 6.022×10²³ | 5.61×10²⁹ | 0.002205 |
| **kg** | 1000 | 1 | 6.022×10²⁶ | 5.61×10³² | 2.205 |
| **amu** | 1.661×10⁻²⁴ | 1.661×10⁻²⁷ | 1 | 931.494 | 3.66×10⁻²⁷ |
| **MeV/c²** | 1.783×10⁻³⁰ | 1.783×10⁻³³ | 0.001074 | 1 | 3.93×10⁻³³ |
| **lb** | 453.592 | 0.454 | 2.73×10²⁶ | 2.54×10³² | 1 |

### Particle Rest Masses

| Particle | Mass (amu) | Mass (MeV/c²) | Mass (kg) |
|----------|------------|---------------|-----------|
| Electron | 5.486×10⁻⁴ | 0.511 | 9.109×10⁻³¹ |
| Proton | 1.007276 | 938.272 | 1.673×10⁻²⁷ |
| Neutron | 1.008665 | 939.565 | 1.675×10⁻²⁷ |
| Deuteron | 2.014102 | 1875.613 | 3.344×10⁻²⁷ |
| Alpha (He-4) | 4.002603 | 3727.379 | 6.645×10⁻²⁷ |
| U-235 | 235.044 | 218,872 | 3.903×10⁻²⁵ |
| U-238 | 238.051 | 221,673 | 3.953×10⁻²⁵ |

---

## Time Conversions

### Time Unit Conversion Matrix

| From ↓ To → | s | ms | μs | ns | ps | shake |
|-------------|-----|-----|-----|-----|-----|-------|
| **s** | 1 | 1000 | 10⁶ | 10⁹ | 10¹² | 10⁸ |
| **ms** | 0.001 | 1 | 1000 | 10⁶ | 10⁹ | 10⁵ |
| **μs** | 10⁻⁶ | 0.001 | 1 | 1000 | 10⁶ | 100 |
| **ns** | 10⁻⁹ | 10⁻⁶ | 0.001 | 1 | 1000 | 0.1 |
| **ps** | 10⁻¹² | 10⁻⁹ | 10⁻⁶ | 0.001 | 1 | 10⁻⁴ |
| **shake** | 10⁻⁸ | 10⁻⁵ | 0.01 | 10 | 10⁴ | 1 |

### Definition

**1 shake = 10⁻⁸ s = 10 ns**

Origin: The name comes from the phrase "two shakes of a lamb's tail," representing a very short time. It's approximately the time for one generation in a fast-neutron chain reaction.

### Characteristic Times in Nuclear Processes

| Process | Time | Shakes | Description |
|---------|------|--------|-------------|
| Neutron generation (fast) | 10 ns | 1 | Prompt neutron chain |
| Light travel (1 cm) | 33 ps | 0.0033 | c = 30 cm/ns |
| Neutron thermalization | 1–10 μs | 100–1000 | Slowing down to thermal |
| Prompt neutron lifetime | 10⁻⁴ s | 10,000 | Typical thermal reactor |
| Delayed neutron emission | 0.1–80 s | 10⁷–10¹⁰ | Precursor decay |
| Pulse width (accelerator) | 1 μs | 100 | Typical beam pulse |

---

## Angle Conversions

### Angle Unit Conversion

| From ↓ To → | Degrees | Radians | Gradians |
|-------------|---------|---------|----------|
| **Degrees** | 1 | π/180 ≈ 0.01745 | 10/9 ≈ 1.111 |
| **Radians** | 180/π ≈ 57.2958 | 1 | 200/π ≈ 63.662 |
| **Gradians** | 9/10 = 0.9 | π/200 ≈ 0.01571 | 1 |

### Common Angles

| Angle | Degrees | Radians | Cosine | Sine |
|-------|---------|---------|--------|------|
| 0° | 0 | 0 | 1.000 | 0.000 |
| 30° | 30 | π/6 ≈ 0.5236 | 0.866 | 0.500 |
| 45° | 45 | π/4 ≈ 0.7854 | 0.707 | 0.707 |
| 60° | 60 | π/3 ≈ 1.047 | 0.500 | 0.866 |
| 90° | 90 | π/2 ≈ 1.571 | 0.000 | 1.000 |
| 120° | 120 | 2π/3 ≈ 2.094 | -0.500 | 0.866 |
| 180° | 180 | π ≈ 3.142 | -1.000 | 0.000 |

### MCNP Direction Cosines

In MCNP, directions are specified using direction cosines (u, v, w) where:
- u = sin(θ) cos(φ)
- v = sin(θ) sin(φ)
- w = cos(θ)

Constraint: u² + v² + w² = 1

---

## Physical Constants

### Fundamental Constants (CODATA 2018)

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Speed of light | c | 2.99792458 × 10⁸ | m/s |
| Planck constant | h | 6.62607015 × 10⁻³⁴ | J·s |
| Reduced Planck | ℏ | 1.054571817 × 10⁻³⁴ | J·s |
| Elementary charge | e | 1.602176634 × 10⁻¹⁹ | C |
| Electron mass | m_e | 9.1093837015 × 10⁻³¹ | kg |
| Proton mass | m_p | 1.67262192369 × 10⁻²⁷ | kg |
| Neutron mass | m_n | 1.67492749804 × 10⁻²⁷ | kg |
| Atomic mass unit | u | 1.66053906660 × 10⁻²⁷ | kg |
| Avogadro constant | N_A | 6.02214076 × 10²³ | mol⁻¹ |
| Boltzmann constant | k_B | 1.380649 × 10⁻²³ | J/K |
| Boltzmann (energy) | k_B | 8.617333262 × 10⁻⁵ | eV/K |
| Boltzmann (energy) | k_B | 8.617333262 × 10⁻¹¹ | MeV/K |
| Gas constant | R | 8.314462618 | J/(mol·K) |

### Derived Constants

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Fine structure | α | 7.2973525693 × 10⁻³ | dimensionless |
| Electron volt | eV | 1.602176634 × 10⁻¹⁹ | J |
| Barn | b | 10⁻²⁴ | cm² |
| Classical electron radius | r_e | 2.8179403262 × 10⁻¹⁵ | m |
| Compton wavelength | λ_C | 2.42631023867 × 10⁻¹² | m |
| Bohr radius | a_0 | 5.29177210903 × 10⁻¹¹ | m |

---

## Quick Reference Card

### MCNP Standard Units Summary

| Quantity | MCNP Unit | Common Alternatives |
|----------|-----------|---------------------|
| Energy | MeV | eV, keV, GeV, J |
| Length | cm | m, mm, inch |
| Density (mass) | g/cm³ (negative sign) | kg/m³ |
| Density (atomic) | atom/b-cm (positive sign) | atoms/cm³ |
| Temperature | K or MeV | °C, °F, eV |
| Cross section | barn | cm², millibarn |
| Time | shake (10⁻⁸ s) | s, μs, ns |
| Mass | amu | g, kg, MeV/c² |
| Activity | Bq or Ci | mCi, μCi, dps |
| Angle | degrees or radians | cosines for directions |

### Key Conversion Factors

- **1 MeV = 10⁶ eV = 1.602×10⁻¹³ J**
- **1 m = 100 cm**
- **1 kg/m³ = 0.001 g/cm³**
- **1 barn = 10⁻²⁴ cm²**
- **1 Ci = 3.7×10¹⁰ Bq**
- **1 amu = 931.494 MeV/c² = 1.661×10⁻²⁴ g**
- **1 shake = 10⁻⁸ s = 10 ns**
- **k_B = 8.617×10⁻¹¹ MeV/K = 8.617×10⁻⁵ eV/K**

---

**Last Updated**: 2025-11-06
**Source**: CODATA 2018, MCNP User Manual 6.3, NIST Physical Constants
