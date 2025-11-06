---
name: mcnp-physical-constants
description: "Lookup fundamental physical constants, particle properties, and nuclear data needed for MCNP calculations including conversion factors, masses, energies, and cross-section benchmarks"
version: "2.0.0"
dependencies: "mcnp-unit-converter (optional)"
---

# MCNP Physical Constants

## Overview

This utility skill provides quick reference to fundamental physical constants, particle properties, and nuclear data required for accurate MCNP calculations. The skill includes comprehensive reference documentation, Python lookup tools, and quick-reference data files for efficient access to CODATA 2018 recommended values and Particle Data Group (PDG) 2020 particle properties.

Physical constants are essential for density calculations, energy conversions, cross-section interpretations, and physics validations in MCNP. This skill bridges theoretical physics values with practical MCNP input requirements, ensuring calculations use the most current and accurate data available.

The skill provides both interactive Python tools for detailed lookup and quick-reference tables for common constants, supporting workflows from material definition to reactor physics calculations.

## When to Use This Skill

- Calculating atom density from mass density (requires Avogadro's number)
- Converting temperature to thermal energy (requires Boltzmann constant)
- Finding particle rest masses for Q-value or binding energy calculations
- Retrieving neutron properties for source definitions
- Checking speed of light for relativistic corrections
- Getting atomic mass unit conversion (amu to MeV/c²)
- Verifying calculated values against known benchmarks
- Determining fission energy releases and neutron yields
- Looking up cross-section typical values for validation
- Converting between energy and wavelength for photons/neutrons

## Quick Reference Tables

### Most Common Constants (CODATA 2018)

| Constant | Symbol | Value | Units | Use in MCNP |
|----------|--------|-------|-------|-------------|
| Avogadro's number | N_A | 6.022×10²³ | mol⁻¹ | Atom density calculations |
| Boltzmann constant | k_B | 8.617×10⁻⁵ | eV/K | TMP card (temperature) |
| Speed of light | c | 2.998×10¹⁰ | cm/s | Relativistic transport |
| AMU energy | - | 931.494 | MeV/c² | Mass-energy conversion |
| Elementary charge | e | 1.602×10⁻¹⁹ | C | Charged particles |
| Planck constant | h | 6.626×10⁻³⁴ | J·s | Wavelength calculations |

### Key Particle Masses

| Particle | Mass (MeV/c²) | Mass (amu) | MCNP Relevance |
|----------|---------------|------------|----------------|
| Electron | 0.511 | 5.486×10⁻⁴ | Pair production, beta decay |
| Proton | 938.272 | 1.00728 | Recoil, hydrogen nucleus |
| Neutron | 939.565 | 1.00866 | Primary transport particle |
| Deuteron | 1875.613 | 2.01355 | D₂O moderator, fusion |
| Alpha (⁴He) | 3727.379 | 4.00151 | Alpha decay, AmBe sources |

### Nuclear Benchmarks

| Quantity | Value | Notes |
|----------|-------|-------|
| Thermal neutron energy | 0.0253 eV | At T = 293.6 K |
| Thermal neutron speed | 2200 m/s | Standard reference |
| U-235 fission energy | 200 MeV | Total release |
| U-235 neutrons/fission | 2.43 | Thermal (ν) |
| Free neutron half-life | 879.4 s | ≈ 14.7 minutes |
| 1 barn | 10⁻²⁴ cm² | Cross section unit |

**For complete constants:** See `fundamental_constants.md`
**For particle data:** See `particle_properties.md`
**For nuclear data:** See `nuclear_constants.md`
**For cross sections:** See `benchmark_cross_sections.md`

## Decision Tree

```
User needs physical constant/property?
    │
    ├─ For quick lookup (common values)?
    │  └─ Use quick_reference.csv or tables in this file
    │
    ├─ For detailed constant data?
    │  └─ Use scripts/constants_lookup.py --search "<query>"
    │
    ├─ For calculation with constants?
    │  └─ Use scripts/unit_aware_calculator.py
    │
    ├─ For material definition?
    │  ├─ Need Avogadro's number → atom density = (ρ × N_A) / A
    │  └─ Use calculator: python unit_aware_calculator.py --calc atom_density
    │
    ├─ For temperature conversion?
    │  ├─ Need Boltzmann constant → E = k_B × T
    │  └─ Use calculator: python unit_aware_calculator.py --calc thermal_energy
    │
    ├─ For nuclear reaction?
    │  ├─ Need particle masses → Q-value calculation
    │  └─ See particle_properties.md or use calculator
    │
    └─ For validation/verification?
       └─ See benchmark_cross_sections.md for typical values
```

## Use Cases

### Use Case 1: Material Definition (Atom Density)

**Scenario:** Define iron material at ρ = 7.85 g/cm³ for MCNP

**Goal:** Calculate atom density in atoms/barn-cm

**Constants Needed:**
- Avogadro's number: N_A = 6.022×10²³ mol⁻¹
- Atomic mass of Fe: A = 55.845 g/mol

**Implementation:**

**Manual calculation:**
```
N (atoms/cm³) = (ρ × N_A) / A
N = (7.85 g/cm³ × 6.022×10²³ mol⁻¹) / 55.845 g/mol
N = 8.46×10²² atoms/cm³ = 0.0846 atoms/barn-cm
```

**Using Python tool:**
```bash
python scripts/unit_aware_calculator.py --calc atom_density --density 7.85 --mass 55.845
# Result: 0.084603 atoms/barn-cm
```

**MCNP Material Card:**
```
M1  26000.80c  0.0846    $ Iron at natural density
```

**Key Points:**
- Avogadro's number converts moles to atoms
- Factor of 10²⁴ converts cm³ to barn-cm
- Can use positive (atom density) or negative (mass density) in MCNP
- Accuracy: Use at least 4 significant figures for N_A

### Use Case 2: Temperature to Thermal Energy

**Scenario:** Material at 600 K, need to specify on TMP card

**Goal:** Convert temperature to thermal energy (MeV)

**Constants Needed:**
- Boltzmann constant: k_B = 8.617×10⁻¹¹ MeV/K

**Implementation:**
```
E = k_B × T
E = 8.617×10⁻¹¹ MeV/K × 600 K = 5.17×10⁻⁸ MeV

Compare to thermal (293.6 K):
E_thermal = 8.617×10⁻¹¹ × 293.6 = 2.53×10⁻⁸ MeV = 0.0253 eV
```

**MCNP Application:**
```
M1  92235.80c  1.0
TMP  600                  $ Temperature in Kelvin (recommended)
c Or equivalently:
TMP  5.17E-8              $ Temperature in MeV (less common)
```

**Key Points:**
- TMP card accepts both Kelvin and MeV
- Kelvin preferred for clarity
- Room temp (293.6 K) = 0.0253 eV (thermal neutron energy)
- Higher temperature → broader resonances (Doppler effect)

### Use Case 3: Nuclear Reaction Q-Value

**Scenario:** Calculate energy release for D-D fusion: ²H + ²H → ³He + n

**Goal:** Determine Q-value and product energies

**Constants Needed:**
- Particle masses (amu): ²H = 2.014102, ³He = 3.016029, n = 1.008665
- Conversion: 1 amu = 931.494 MeV/c²

**Implementation:**
```
Reactants: 2 × 2.014102 = 4.028204 amu
Products: 3.016029 + 1.008665 = 4.024694 amu
Mass defect: Δm = 4.028204 - 4.024694 = 0.003510 amu

Q-value: Q = Δm × 931.494 = 0.003510 × 931.494 = 3.27 MeV

Energy distribution (momentum conservation):
  Neutron: ~2.45 MeV
  ³He: ~0.82 MeV
```

**MCNP Source Definition:**
```
c D-D fusion neutron source
SDEF  PAR=1  ERG=2.45    $ Neutron from D-D fusion
```

**Key Points:**
- Positive Q-value → exothermic (energy released)
- Negative Q-value → endothermic (energy required)
- Products share energy by momentum conservation
- Lighter product gets more kinetic energy

### Use Case 4: Neutron Speed from Energy

**Scenario:** Thermal neutron (0.0253 eV), find velocity

**Goal:** Calculate speed and wavelength

**Constants Needed:**
- Neutron mass: m_n = 1.675×10⁻²⁷ kg
- Energy conversion: 1 eV = 1.602×10⁻¹⁹ J
- Planck constant: h = 6.626×10⁻³⁴ J·s

**Implementation:**
```
Non-relativistic: E = ½mv²
v = sqrt(2E/m)

E = 0.0253 eV × 1.602×10⁻¹⁹ J/eV = 4.05×10⁻²¹ J
v = sqrt(2 × 4.05×10⁻²¹ / 1.675×10⁻²⁷) = 2200 m/s ✓

De Broglie wavelength:
λ = h/p = h/(mv) = 6.626×10⁻³⁴ / (1.675×10⁻²⁷ × 2200)
λ = 1.80 Å (comparable to atomic spacing)
```

**Key Points:**
- Thermal neutrons: v ≈ 2200 m/s (standard)
- Wavelength similar to crystal lattice spacing → diffraction effects
- Non-relativistic valid for E ≪ 939 MeV (neutron rest energy)
- Fast neutrons (MeV range) may need relativistic correction

### Use Case 5: Reactor Power Calculation

**Scenario:** 1 MW thermal reactor, find fission rate

**Goal:** Calculate fissions/second and fuel consumption

**Constants Needed:**
- Energy per fission: ~200 MeV (U-235)
- Conversion: 1 MeV = 1.602×10⁻¹³ J
- Avogadro's number: 6.022×10²³ mol⁻¹

**Implementation:**
```
P (watts) = F (fissions/s) × E (J/fission)
P = F × 200 MeV × 1.602×10⁻¹³ J/MeV
F = P / (200 × 1.602×10⁻¹³)
F = 1×10⁶ W / (3.204×10⁻¹¹ J) = 3.12×10¹⁶ fissions/s

Fuel consumption:
  Mass rate = (F × M_fuel) / N_A
  dm/dt = (3.12×10¹⁶ × 235) / 6.022×10²³
  dm/dt = 1.22×10⁻⁵ g/s = 1.05 g/day

Rule of thumb: ~1 g U-235/day per MW thermal
```

**Key Points:**
- 200 MeV/fission includes prompt and delayed energy
- Excludes neutrinos (~12 MeV, not deposited)
- Actual recoverable: ~188 MeV
- Fuel consumption nearly linear with power

## Integration with Other Skills

### Supports Material Builder
**mcnp-material-builder** uses Avogadro's number for atom density calculations and atomic masses for material composition.

### Supports Source Builder
**mcnp-source-builder** uses particle energies, decay constants, and reaction Q-values for neutron and photon source definitions.

### Supports Physics Builder
**mcnp-physics-builder** uses Boltzmann constant for temperature conversions on TMP cards and energy cutoff specifications.

### Uses Unit Converter
**mcnp-unit-converter** provides additional conversion factors; this skill focuses on fundamental constants rather than unit conversions.

### Supports Isotope Lookup
**mcnp-isotope-lookup** uses atomic mass unit conversion and particle masses for isotope property calculations.

## Python Tools

This skill includes two Python tools in the `scripts/` directory:

### constants_lookup.py
Interactive and command-line lookup for physical constants and particle properties.

**Quick start:**
```bash
# Interactive mode
python scripts/constants_lookup.py

# Search for constant
python scripts/constants_lookup.py --search "avogadro"

# Display constant
python scripts/constants_lookup.py --constant "boltzmann_constant"

# Show particle properties
python scripts/constants_lookup.py --particle "neutron"
```

### unit_aware_calculator.py
Scientific calculator with automatic unit handling for MCNP physics calculations.

**Quick start:**
```bash
# Interactive mode
python scripts/unit_aware_calculator.py

# Atom density
python scripts/unit_aware_calculator.py --calc atom_density --density 7.85 --mass 55.845

# Thermal energy
python scripts/unit_aware_calculator.py --calc thermal_energy --temperature 600
```

**See `scripts/README.md` for complete documentation.**

## References

### Bundled Resources

**Reference Documentation (at ROOT level):**
- `fundamental_constants.md` - CODATA 2018 universal, electromagnetic, and gravitational constants
- `particle_properties.md` - Leptons, nucleons, light nuclei with detailed properties
- `nuclear_constants.md` - Fission, fusion, decay data and nuclear energy scales
- `benchmark_cross_sections.md` - Typical cross sections for validation

**Python Tools (scripts/):**
- `constants_lookup.py` - Interactive constant/particle lookup
- `unit_aware_calculator.py` - Physics calculator with unit handling
- `README.md` - Complete tool documentation and examples

**Data Files (example_inputs/):**
- `quick_reference.csv` - Most common constants in CSV format

### External References

**Official Sources:**
- NIST Physical Constants: https://physics.nist.gov/cuu/Constants/
- Particle Data Group: https://pdg.lbl.gov/
- IAEA Nuclear Data: https://www-nds.iaea.org/

**Related MCNP Skills:**
- mcnp-unit-converter - Unit conversion tool
- mcnp-material-builder - Uses Avogadro's number
- mcnp-isotope-lookup - Particle masses and ZAID format
- mcnp-source-builder - Particle energies
- mcnp-physics-builder - Temperature settings

## Best Practices

1. **Use CODATA 2018 Values** - Always reference most recent CODATA recommendations for fundamental constants (bundled in `fundamental_constants.md`)

2. **Maintain Adequate Precision** - Use at least 4 significant figures for Avogadro's number and Boltzmann constant in calculations; MCNP typically handles 5-6 significant figures

3. **Verify with Benchmarks** - Cross-check calculated values against known benchmarks (thermal neutron = 2200 m/s, 1 MW ≈ 1 g U-235/day)

4. **Document Constant Sources** - Note where constants were obtained, especially for critical calculations or publications

5. **Use Consistent Unit Systems** - Convert all inputs to one system (SI or CGS) before calculation to avoid errors

6. **Check Physical Reasonableness** - Compare results to typical values (e.g., atom densities 0.01-0.1 atoms/b-cm for most materials)

7. **Prefer Kelvin for Temperature** - Use Kelvin on TMP card rather than MeV for clarity and to match cross-section library temperatures

8. **Update Constants Periodically** - CODATA revises values every 4 years; check for updates, though changes rarely affect MCNP significantly

9. **Use Python Tools for Complex Calculations** - Leverage `unit_aware_calculator.py` for multi-step calculations to reduce human error

10. **Distinguish Exact vs Measured** - Some constants are exact by definition (c, h, k_B, e, N_A as of 2019); others have uncertainties (G)

---

**For detailed constants, see bundled reference documentation. For calculations, use Python tools in scripts/.**
