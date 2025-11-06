# Fundamental Physical Constants

Complete reference of fundamental physical constants based on CODATA 2018 recommended values. These constants form the foundation of physics calculations in MCNP and nuclear engineering.

## Universal Constants

### Speed of Light in Vacuum

**Symbol:** c

**Value:**
- 299,792,458 m/s (exact, by definition)
- 2.99792458 × 10¹⁰ cm/s
- 2.99792458 × 10⁸ m/s

**Notes:**
- Exact value by definition of the meter (since 1983)
- Defines the meter as distance traveled by light in 1/299,792,458 of a second
- Fundamental speed limit in the universe
- Used in relativistic energy calculations: E² = (pc)² + (mc²)²

**MCNP Applications:**
- Relativistic particle transport
- Energy-momentum conversions
- Photon transport (always travels at c)
- Time-of-flight calculations

### Planck Constant

**Symbol:** h (h-bar: ℏ = h/2π)

**Values:**
- h = 6.62607015 × 10⁻³⁴ J·s (exact, by definition since 2019)
- h = 4.135667696 × 10⁻¹⁵ eV·s
- ℏ = 1.054571817 × 10⁻³⁴ J·s
- ℏ = 6.582119569 × 10⁻¹⁶ eV·s
- ℏc = 197.3269804 MeV·fm

**Notes:**
- Fundamental quantum of action
- Relates energy to frequency: E = hν
- Relates momentum to wavelength: p = h/λ
- Central to quantum mechanics and nuclear physics

**MCNP Applications:**
- De Broglie wavelength: λ = h/p
- Energy-wavelength conversions
- Photon energy: E = hc/λ
- Uncertainty principle: ΔxΔp ≥ ℏ/2

### Boltzmann Constant

**Symbol:** k_B (or k)

**Values:**
- k_B = 1.380649 × 10⁻²³ J/K (exact, by definition since 2019)
- k_B = 8.617333262 × 10⁻⁵ eV/K
- k_B = 8.617333262 × 10⁻¹¹ MeV/K

**Notes:**
- Relates temperature to energy
- Defines the kelvin (since 2019)
- Thermal energy per particle: E_thermal = k_B T
- Room temperature (293 K) ≈ 0.0253 eV (thermal neutron energy)

**MCNP Applications:**
- Temperature-energy conversions for TMP card
- Thermal neutron energy: E_th = k_B T (T = 293.6 K → 0.0253 eV)
- Cross-section Doppler broadening
- Maxwell-Boltzmann energy distributions

**Common Temperature Conversions:**
```
Room temperature (20°C = 293 K):
  k_B T = 0.0253 eV = 2.53 × 10⁻⁸ MeV

Reactor operating temperature (600 K):
  k_B T = 0.0517 eV = 5.17 × 10⁻⁸ MeV

Reactor fuel centerline (2000 K):
  k_B T = 0.172 eV = 1.72 × 10⁻⁷ MeV
```

### Elementary Charge

**Symbol:** e

**Values:**
- e = 1.602176634 × 10⁻¹⁹ C (exact, by definition since 2019)
- e = 4.803204712 × 10⁻¹⁰ esu (electrostatic unit)

**Notes:**
- Fundamental unit of electric charge
- Charge of proton: +e
- Charge of electron: -e
- Defines the coulomb (since 2019)

**MCNP Applications:**
- Electron/positron transport
- Electromagnetic interaction strength
- Energy loss calculations (dE/dx)
- Charged particle stopping power

### Avogadro Constant

**Symbol:** N_A (or L)

**Value:**
- N_A = 6.02214076 × 10²³ mol⁻¹ (exact, by definition since 2019)

**Notes:**
- Number of particles (atoms/molecules) per mole
- Defines the mole (since 2019)
- Bridges atomic and macroscopic scales
- Named after Amedeo Avogadro

**MCNP Applications:**
- **Critical for material definitions**
- Atom density calculation: N = (ρ × N_A) / A
  - ρ = mass density (g/cm³)
  - A = atomic/molecular weight (g/mol)
  - N = atom density (atoms/cm³)
- Convert between mass fractions and atom fractions
- Specific activity calculations

**Example - Iron Density:**
```
Iron: ρ = 7.85 g/cm³, A = 55.845 g/mol

N = (7.85 g/cm³ × 6.022×10²³ mol⁻¹) / 55.845 g/mol
N = 8.46 × 10²² atoms/cm³
N = 0.0846 atoms/b-cm

MCNP material card:
M1  26000.80c  0.0846    $ Iron at natural density
```

## Gravitational Constant

### Newtonian Constant of Gravitation

**Symbol:** G

**Value:**
- G = 6.67430(15) × 10⁻¹¹ m³/(kg·s²)
- G = 6.67430 × 10⁻⁸ cm³/(g·s²)

**Uncertainty:**
- Relative standard uncertainty: 2.2 × 10⁻⁵ (22 ppm)
- Least precisely known fundamental constant

**Notes:**
- Appears in Newton's law of gravitation: F = G m₁m₂/r²
- Determines gravitational field strength
- Negligible in nuclear physics (gravity ≪ nuclear forces)

**MCNP Applications:**
- Generally not used (gravity negligible at nuclear scales)
- May appear in astrophysical applications
- Gravity force ratio: F_gravity/F_electromagnetic ≈ 10⁻³⁶ for protons

## Electromagnetic Constants

### Permittivity of Free Space

**Symbol:** ε₀ (epsilon-zero)

**Value:**
- ε₀ = 8.8541878128(13) × 10⁻¹² F/m (farads per meter)
- ε₀ = 8.8541878128 × 10⁻¹² C²/(N·m²)

**Relation to Other Constants:**
- μ₀ε₀ = 1/c² (exact relation)
- ε₀ = 1/(μ₀c²)

**Notes:**
- Electric permittivity of vacuum
- Appears in Coulomb's law: F = (1/4πε₀) × q₁q₂/r²
- Determines strength of electric field
- Electric constant in Maxwell's equations

**MCNP Applications:**
- Charged particle interactions
- Electromagnetic field calculations
- Dielectric material properties
- Capacitance calculations

### Permeability of Free Space

**Symbol:** μ₀ (mu-zero)

**Value:**
- μ₀ = 1.25663706212(19) × 10⁻⁶ N/A² (newtons per ampere squared)
- μ₀ = 1.25663706212 × 10⁻⁶ H/m (henrys per meter)
- μ₀ = 4π × 10⁻⁷ N/A² (approximately, was exact before 2019)

**Notes:**
- Magnetic permeability of vacuum
- Determines strength of magnetic field
- Magnetic constant in Maxwell's equations
- No longer exactly 4π × 10⁻⁷ after 2019 redefinition

**MCNP Applications:**
- Magnetic field calculations
- Magnetic material properties
- Inductance calculations
- Electromagnetic wave propagation

### Fine Structure Constant

**Symbol:** α (alpha)

**Value:**
- α = 7.2973525693(11) × 10⁻³
- α ≈ 1/137.035999084
- α = e²/(4πε₀ℏc) (dimensionless)

**Uncertainty:**
- Relative standard uncertainty: 1.5 × 10⁻¹⁰ (0.15 ppb)
- One of the most precisely known constants

**Notes:**
- Dimensionless fundamental constant
- Measures strength of electromagnetic interaction
- Ratio of electron velocity in first Bohr orbit to speed of light
- Appears throughout atomic physics and QED

**Physical Interpretation:**
- α = (v₁/c) for electron in hydrogen ground state
- α² = ratio of electron rest energy to Rydberg energy
- Coupling constant for electromagnetic interactions

**MCNP Applications:**
- Atomic physics calculations
- Fine structure splitting in spectroscopy
- Electromagnetic coupling strength
- Precision physics validations
- QED corrections in high-precision transport

## Combined Constants (Derived but Commonly Used)

### Energy-Wavelength Conversion

**Photon energy from wavelength:**
```
E (eV) = hc/λ

where:
  hc = 1.23984198 × 10⁻⁶ eV·m
  hc = 12398.4198 eV·Å
  hc = 1.23984198 keV·nm

For X-rays and gamma rays:
  E (keV) = 12.39842 / λ (nm)
  E (keV) = 1.239842 / λ (Å)
```

**Example:**
```
1 Å X-ray:
  E = 12398.4 / 1 = 12.398 keV

Copper Kα X-ray (8.05 keV):
  λ = 12398.4 / 8050 = 1.54 Å
```

### Rydberg Constant

**Symbol:** R_∞

**Value:**
- R_∞ = 10,973,731.568160(21) m⁻¹
- R_∞ = 1.0973731568160 × 10⁷ m⁻¹
- R_∞ = 1.097373 × 10⁵ cm⁻¹

**Rydberg Energy:**
- E_Ry = hcR_∞ = 13.605693122994 eV
- Binding energy of hydrogen ground state

**Notes:**
- Hydrogen spectral lines: 1/λ = R_∞ (1/n₁² - 1/n₂²)
- Most precisely measured fundamental constant
- Defines atomic energy scale

### Compton Wavelength

**Electron Compton wavelength:**
- λ_C = h/(m_e c) = 2.42631023867 × 10⁻¹² m
- λ_C = 0.024263 Å

**Reduced Compton wavelength:**
- λ̄_C = ℏ/(m_e c) = 3.8615926796 × 10⁻¹³ m
- Classical electron radius: r_e = α²λ̄_C

**MCNP Applications:**
- Compton scattering wavelength shift: Δλ = λ_C (1 - cos θ)
- Electron structure scale
- Photon-electron interaction cross sections

## Standard Conditions

### Standard Temperature and Pressure (STP)

**IUPAC Definition (since 1982):**
- Temperature: T = 273.15 K (0°C)
- Pressure: P = 100 kPa = 1 bar = 0.986923 atm

**Old STP (pre-1982, still sometimes used):**
- Temperature: T = 273.15 K (0°C)
- Pressure: P = 101.325 kPa = 1 atm

**Molar Volume (Ideal Gas at STP):**
- V_m = 22.71095 L/mol (at 273.15 K, 100 kPa)
- V_m = 22.41396 L/mol (at 273.15 K, 101.325 kPa - old STP)

### Normal Temperature and Pressure (NTP)

**Definition:**
- Temperature: T = 293.15 K (20°C)
- Pressure: P = 101.325 kPa = 1 atm

**Molar Volume (Ideal Gas at NTP):**
- V_m = 24.04648 L/mol

**Notes:**
- Often used for gas density specifications
- "Room temperature and pressure"
- More realistic for laboratory conditions

### MCNP Standard Conditions

**For cross-section libraries:**
- Most libraries at T = 293.6 K (20.44°C)
- Corresponds to thermal energy E = 0.0253 eV
- Standard neutron velocity v = 2200 m/s

**For material densities:**
- Usually specified at room temperature (20-25°C)
- Pressure: 1 atm (101.325 kPa)
- Important for gas densities and thermal properties

## Precision and Uncertainty

### CODATA 2018 Revisions

**Exact constants (by definition as of May 20, 2019):**
1. Speed of light: c
2. Planck constant: h
3. Elementary charge: e
4. Boltzmann constant: k_B
5. Avogadro constant: N_A
6. Luminous efficacy of 540 THz radiation: K_cd

**These exact values define the SI units:**
- Meter (from c)
- Kilogram (from h)
- Kelvin (from k_B)
- Ampere (from e)
- Mole (from N_A)
- Candela (from K_cd)

**Measured constants (with uncertainty):**
- Gravitational constant: G (22 ppm uncertainty)
- Proton-to-electron mass ratio
- Fine structure constant (measured, but can also be derived)

### Significant Figures in MCNP

**Recommended precision:**
- Avogadro's number: Use at least 4 significant figures (6.022 × 10²³)
- Boltzmann constant: Use at least 4 significant figures
- Conversion factors: Match precision of input data
- Cross sections: Match library precision (typically 5-6 figures)

**Example:**
```
Good practice:
  N_A = 6.022e23    (4 sig figs, adequate for most calculations)
  N_A = 6.02214e23  (6 sig figs, high precision)

Excessive precision:
  N_A = 6.02214076e23  (9 sig figs, exceeds typical MCNP needs)

Insufficient precision:
  N_A = 6.0e23  (2 sig figs, may introduce errors)
```

## References and Resources

### Official Sources

**NIST (National Institute of Standards and Technology):**
- Website: https://physics.nist.gov/cuu/Constants/
- CODATA 2018 recommended values
- Includes uncertainties and correlations
- Regularly updated

**CODATA (Committee on Data for Science and Technology):**
- International collaboration
- Publishes recommended fundamental constant values
- Major updates every 4 years (2010, 2014, 2018, next ~2022-2024)

**Bureau International des Poids et Mesures (BIPM):**
- Maintains SI unit definitions
- https://www.bipm.org/

### Related MCNP Skills

- **mcnp-unit-converter**: Uses these constants for conversions
- **mcnp-material-builder**: Uses Avogadro's number extensively
- **mcnp-isotope-lookup**: Uses atomic mass unit definition
- **mcnp-physics-builder**: Uses Boltzmann constant for temperature

### Additional Reading

**Textbooks:**
- Krane, "Introductory Nuclear Physics" - Appendix with constants
- Mohr, Newell, Taylor (2016) - "CODATA Recommended Values"
- PDG (Particle Data Group) - Annual review with constants

**Online Databases:**
- NIST Physical Reference Data
- Particle Data Group (pdg.lbl.gov)
- NNDC (National Nuclear Data Center)

## Version History

**CODATA 2018 (current):**
- Published: May 2019
- Implemented new SI definitions
- Five constants now exact by definition

**CODATA 2014:**
- Previous recommended values
- Pre-SI redefinition

**CODATA 2010:**
- Earlier values
- Some differences in less well-known constants

**For MCNP users:**
- Always use CODATA 2018 or later
- Most MCNP applications not sensitive to small constant changes
- Critical applications: verify constant values match reference

---

**End of Fundamental Constants Reference**
