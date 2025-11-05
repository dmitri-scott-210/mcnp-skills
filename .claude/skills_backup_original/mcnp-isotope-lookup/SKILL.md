---
category: F
name: mcnp-isotope-lookup
description: Look up isotope properties including ZAID format, atomic masses, natural abundances, decay data, and cross-section library availability for MCNP material and source definitions
activation_keywords:
  - isotope lookup
  - ZAID
  - atomic mass
  - natural abundance
  - isotope properties
  - nuclide identifier
  - decay data
  - half-life
  - cross section library
---

# MCNP Isotope Lookup Skill

## Purpose

This utility skill provides comprehensive isotope property lookup for MCNP simulations. It helps Claude identify correct ZAID identifiers, retrieve atomic masses, determine natural abundances, access decay data, and verify cross-section library availability. This skill is essential for accurate material definitions and radioactive source specifications.

## When to Use This Skill

- Finding ZAID identifiers for isotopes (e.g., U-235 → 92235)
- Looking up atomic masses for material density calculations
- Determining natural isotopic abundances for element definitions
- Identifying decay modes and half-lives for source terms
- Verifying cross-section library availability (e.g., .80c, .81c)
- Converting element names to ZAID format
- Finding stable vs. radioactive isotopes
- Selecting appropriate isotopes for shielding materials
- Determining fission product compositions
- Identifying activation products in materials

## Prerequisites

- **mcnp-material-builder**: Uses ZAID and atomic mass data
- **mcnp-source-builder**: Uses decay data for radioactive sources
- **mcnp-cross-section-manager**: Uses library availability information
- **mcnp-physical-constants**: Uses fundamental constants
- Basic understanding of nuclear notation (Z, A, N)
- Familiarity with MCNP ZAID format

## Core Concepts

### ZAID Format

**MCNP Nuclide Identifier Structure**:
```
ZZZAAA.nnX
where:
  ZZZ = atomic number (Z) - 1 to 3 digits
  AAA = mass number (A) - 1 to 3 digits
  nn = library identifier (e.g., 80, 81, 82)
  X = library type (c=continuous, d=discrete, t=thermal, etc.)

Examples:
  1001.80c   → H-1 (protium) with .80c library
  92235.80c  → U-235 with .80c library
  6000.80c   → Carbon (natural mix) with .80c library
  8016.80c   → O-16 with .80c library
```

**Special Cases**:
- **Natural element**: ZZZ000.nnX (e.g., 6000.80c for natural carbon)
- **Metastable state**: ZZZAAA + 300, 400, etc. (e.g., 43099 for Tc-99m)
- **Element symbol**: Can use ZAID or sometimes element symbol

### Atomic Structure Basics

**Nuclear Notation**:
```
Element Symbol: X
Atomic Number (Z): Number of protons
Mass Number (A): Protons + neutrons
Neutron Number (N): A - Z

Notation: ᴬX or X-A
Example: ²³⁵U or U-235
  Z = 92 (uranium)
  A = 235
  N = 235 - 92 = 143 neutrons
```

**Isotopes**: Same Z, different A (different number of neutrons)
**Isobars**: Same A, different Z
**Isotones**: Same N, different Z and A

### Common Cross-Section Libraries

**ENDF/B Library Suffixes**:
```
.80c → ENDF/B-VIII.0 continuous energy (most recent)
.70c → ENDF/B-VII.0 continuous energy
.66c → ENDF/B-VI.6 continuous energy
.60c → ENDF/B-VI.0 continuous energy

.80d → Discrete energy library
.80t → Thermal scattering library (e.g., lwtr.80t for light water)
.80p → Photoatomic data
.80e → Electron data
```

**Temperature-Dependent Libraries**:
```
.80c → 293.6 K (room temperature)
.81c → 600 K
.82c → 900 K
.83c → 1200 K
.84c → 2500 K
```

### Natural Abundances

**Definition**: Fraction of each isotope in naturally occurring element

**Example - Chlorine**:
```
Cl-35: 75.76%
Cl-37: 24.24%

MCNP representation:
M1  17035.80c  0.7576    $ Cl-35
    17037.80c  0.2424    $ Cl-37

Or use natural mix:
M1  17000.80c  1.0       $ Natural chlorine
```

**Elements with Single Stable Isotope**:
```
Be-9:   100% (Z=4, A=9)
F-19:   100% (Z=9, A=19)
Na-23:  100% (Z=11, A=23)
Al-27:  100% (Z=13, A=27)
P-31:   100% (Z=15, A=31)
```

### Atomic Masses

**Atomic Mass Unit (amu)**:
- 1 amu = 1.66053906660 × 10⁻²⁴ g
- 1 amu = 931.494102 MeV/c²
- Based on C-12 = exactly 12 amu

**Common Isotopes**:
```
H-1:    1.00783 amu
H-2:    2.01410 amu (deuterium)
C-12:   12.00000 amu (definition)
O-16:   15.99491 amu
U-235:  235.04393 amu
U-238:  238.05078 amu
Pu-239: 239.05216 amu
```

**Average Atomic Mass**:
```
For natural mix:
A_avg = Σ (f_i × A_i)
where f_i = fractional abundance of isotope i

Example - Natural chlorine:
A_avg = 0.7576 × 34.969 + 0.2424 × 36.966
A_avg = 26.50 + 8.96 = 35.45 amu
```

### Decay Properties

**Decay Modes**:
- **α decay**: Emission of He-4 nucleus (2 protons, 2 neutrons)
- **β⁻ decay**: Neutron → proton + electron + antineutrino
- **β⁺ decay**: Proton → neutron + positron + neutrino
- **Electron capture (EC)**: Proton + electron → neutron + neutrino
- **γ emission**: Excited nucleus → ground state + photon
- **Spontaneous fission (SF)**: Nucleus splits into fragments

**Half-Life (t₁/₂)**:
```
Time for half of nuclei to decay
Activity: A(t) = A₀ × e^(-λt)
where λ = ln(2) / t₁/₂ = decay constant

Common ranges:
  Stable: t₁/₂ = ∞
  Long-lived: t₁/₂ > 10⁸ years
  Short-lived: t₁/₂ < 1 day
```

## Decision Tree: Isotope Lookup

```
START: Need isotope information
  |
  +--> What information needed?
  |      |
  |      +--> ZAID identifier
  |      |      ├─> Know element symbol and mass number?
  |      |      │   ├─> Yes: Construct ZZZAAA
  |      |      │   │   Example: U-235 → Z=92, A=235 → 92235
  |      |      │   └─> No: Look up element → Get Z → Construct
  |      |      ├─> Natural element mix?
  |      |      │   └─> Use ZZZ000 (e.g., 6000 for natural C)
  |      |      └─> Add library suffix (e.g., .80c)
  |      |
  |      +--> Atomic mass
  |      |      ├─> Specific isotope: Use isotopic mass
  |      |      ├─> Natural element: Use average atomic mass
  |      |      └─> For density calculation: Use in formula
  |      |             ρ or N = f(atomic mass)
  |      |
  |      +--> Natural abundance
  |      |      ├─> Check if element has multiple stable isotopes
  |      |      ├─> Look up abundance fractions
  |      |      ├─> Verify sum = 100% (or 1.0)
  |      |      └─> Use in material card:
  |      |            M1  ZAID₁  f₁
  |      |                ZAID₂  f₂
  |      |
  |      +--> Decay data
  |      |      ├─> Is isotope stable?
  |      |      │   ├─> Yes: No decay, use for shielding
  |      |      │   └─> No: Get decay mode, t₁/₂, energies
  |      |      ├─> Decay mode determines particles emitted
  |      |      ├─> Half-life determines activity vs. time
  |      |      └─> Energies used in SDEF card
  |      |
  |      +--> Cross-section availability
  |      |      ├─> Check xsdir file for isotope
  |      |      ├─> Verify library (.80c most common)
  |      |      ├─> Check temperature if needed (.81c, .82c)
  |      |      └─> If not available: use natural mix or similar
  |      |
  |      └─> Element → ZAID conversion
  |             ├─> Look up Z for element
  |             ├─> Determine A (specific or 000 for natural)
  |             ├─> Construct ZZZAAA
  |             └─> Add library suffix
  |
  +--> Apply in MCNP input
  |      ├─> Material card: Use ZAID with abundance/fraction
  |      ├─> Source card: Use decay energies for ERG
  |      └─> Document isotope choice in comments
  |
  └─> Verify
         ├─> ZAID format correct (6-9 characters)
         ├─> Library available in xsdir
         ├─> Abundances sum to 1.0
         └─> Physical properties reasonable
```

## Tool Invocation

This skill includes a Python implementation for automated isotope property lookups.

### Importing the Tool

```python
from mcnp_isotope_lookup import MCNPIsotopeLookup

# Initialize the lookup tool
lookup = MCNPIsotopeLookup()
```

### Basic Usage

**Look Up ZAID from Isotope Name**:
```python
# Find ZAID for specific isotope
zaid_u235 = lookup.lookup_zaid('U-235', library='80c')
print(f"U-235 ZAID: {zaid_u235}")
# Output: U-235 ZAID: 92235.80c

# Natural element
zaid_pb = lookup.lookup_zaid('Pb', library='80c')
print(f"Natural Pb ZAID: {zaid_pb}")
# Output: Natural Pb ZAID: 82000.80c
```

**Get Atomic Weight**:
```python
# Get atomic weight for element
weight_u = lookup.get_atomic_weight('U')
print(f"Uranium atomic weight: {weight_u} amu")

weight_pb = lookup.get_atomic_weight('Pb')
print(f"Lead atomic weight: {weight_pb} amu")
```

**Expand Natural Element to Isotopes**:
```python
# Get all isotopes of natural element with abundances
isotopes = lookup.expand_natural_element('Cl', library='80c')

print("Natural Chlorine isotopes:")
for isotope in isotopes:
    zaid = isotope['zaid']
    abundance = isotope['abundance']
    print(f"  {zaid}: {abundance * 100:.2f}%")

# Output:
# Natural Chlorine isotopes:
#   17035.80c: 75.76%
#   17037.80c: 24.24%
```

**Recommend Library for Isotope**:
```python
# Get recommended cross-section library
library = lookup.recommend_library('Pu-239', particle='n')
print(f"Recommended library for Pu-239 (neutron): {library}")
# Output: Recommended library for Pu-239 (neutron): 80c

# For photons
library_p = lookup.recommend_library('Fe-56', particle='p')
print(f"Recommended library for Fe-56 (photon): {library_p}")
```

### Integration with MCNP Workflow

```python
from mcnp_isotope_lookup import MCNPIsotopeLookup

def create_material_card(element, enrichment=None, density=None):
    """Generate MCNP material card with isotope lookup"""
    lookup = MCNPIsotopeLookup()

    print(f"Creating material card for {element}")
    print("=" * 60)

    if enrichment is None:
        # Use natural element
        zaid = lookup.lookup_zaid(element, library='80c')
        atomic_weight = lookup.get_atomic_weight(element)

        print(f"\nMaterial: Natural {element}")
        print(f"ZAID: {zaid}")
        print(f"Atomic weight: {atomic_weight} amu")

        # Generate M card
        print(f"\nMCNP Material Card:")
        print(f"c Natural {element}")
        if density:
            print(f"c ρ = {density} g/cm³")
        print(f"M1  {zaid}  1.0")

    else:
        # Use specific isotopes (enriched)
        isotopes = lookup.expand_natural_element(element, library='80c')

        print(f"\nMaterial: {element} with isotopic detail")
        print(f"Number of natural isotopes: {len(isotopes)}")

        # Generate M card with all isotopes
        print(f"\nMCNP Material Card (explicit isotopes):")
        print(f"c {element} with natural isotopic composition")
        if density:
            print(f"c ρ = {density} g/cm³")

        for i, isotope in enumerate(isotopes):
            zaid = isotope['zaid']
            abundance = isotope['abundance']
            if i == 0:
                print(f"M1  {zaid}  {abundance:.6f}    $ {isotope['name']}")
            else:
                print(f"    {zaid}  {abundance:.6f}    $ {isotope['name']}")

        # Verify normalization
        total = sum(iso['abundance'] for iso in isotopes)
        print(f"c Verify sum: {total:.6f}")

    print("=" * 60)

# Example usage
if __name__ == "__main__":
    # Natural lead for shielding
    create_material_card('Pb', density=11.34)

    print("\n")

    # Natural uranium (with isotopic detail)
    create_material_card('U', enrichment='natural', density=19.05)

    print("\n")

    # Lookup specific isotope properties
    lookup = MCNPIsotopeLookup()

    # Find ZAID for common isotopes
    print("Common Isotope ZAIDs:")
    isotopes_to_lookup = ['H-1', 'C-12', 'O-16', 'U-235', 'Pu-239']
    for iso in isotopes_to_lookup:
        zaid = lookup.lookup_zaid(iso, library='80c')
        print(f"  {iso}: {zaid}")
```

---

## Use Case 1: Look Up ZAID for Common Shielding Material (Lead)

**Problem**: Need to define lead shielding, find appropriate ZAID

**Lookup Process**:
```
Element: Lead (Pb)
Atomic number: Z = 82

Lead has 4 stable isotopes:
  Pb-204: 1.4% abundance
  Pb-206: 24.1%
  Pb-207: 22.1%
  Pb-208: 52.4%

ZAID options:
  1. Natural mix:  82000.80c (simplest, recommended)
  2. Individual:   82204.80c, 82206.80c, 82207.80c, 82208.80c
```

**MCNP Material Card (Recommended)**:
```
c Lead shielding (natural isotopic composition)
c ρ = 11.34 g/cm³
M1  82000.80c  1.0         $ Natural lead
10  1  -11.34  -100        $ Lead shield
```

**Alternative (Explicit Isotopes)**:
```
c Lead shielding (explicit isotopes)
M2  82204.80c  0.014       $ Pb-204 (1.4%)
    82206.80c  0.241       $ Pb-206 (24.1%)
    82207.80c  0.221       $ Pb-207 (22.1%)
    82208.80c  0.524       $ Pb-208 (52.4%)
c Verify: 0.014 + 0.241 + 0.221 + 0.524 = 1.000 ✓
```

**When to Use Natural vs. Individual**:
- Use natural (82000) for most shielding applications
- Use individual isotopes for:
  - Isotope-specific cross-section studies
  - When one isotope dominates physics
  - Isotopically enriched materials

## Use Case 2: Find Atomic Mass for Density Calculation

**Problem**: Need atomic mass of B-10 for borated water density calculation

**Lookup**:
```
Isotope: Boron-10 (B-10)
ZAID: 5010
Atomic mass: 10.012937 amu

Natural boron composition:
  B-10: 19.9% (A = 10.012937 amu)
  B-11: 80.1% (A = 11.009305 amu)

Average: A_avg = 0.199 × 10.01 + 0.801 × 11.01 = 10.81 amu
```

**Application - Calculate Atom Density**:
```
Borated water: 1000 ppm B-10 by weight in H₂O

Step 1: Composition by weight
  B-10: 1000 ppm = 0.001 weight fraction
  H₂O:  0.999 weight fraction

Step 2: Calculate atom densities
For B-10:
  ρ_total = 1.0 g/cm³ (water density)
  ρ_B10 = 1.0 × 0.001 = 0.001 g/cm³

  N_B10 = (ρ_B10 × N_A) / (A_B10 × 10²⁴)
  N_B10 = (0.001 × 6.022×10²³) / (10.013 × 10²⁴)
  N_B10 = 6.015 × 10⁻⁵ atom/b-cm

For H₂O (weight fraction 0.999):
  ρ_H2O = 0.999 g/cm³
  A_H2O = 18.015 amu

  N_H2O = (0.999 × 6.022×10²³) / (18.015 × 10²⁴)
  N_H2O = 0.03342 atom/b-cm

  N_H = 2 × N_H2O = 0.06684 atom/b-cm
  N_O = N_H2O = 0.03342 atom/b-cm
```

**MCNP Material Card**:
```
c Borated water: 1000 ppm B-10 by weight
c ρ = 1.0 g/cm³
M1  5010.80c   6.015E-5    $ B-10
    1001.80c   0.06684     $ H-1
    8016.80c   0.03342     $ O-16
```

## Use Case 3: Determine Natural Isotopic Composition (Uranium)

**Problem**: Define natural uranium material, need isotopic abundances

**Lookup - Natural Uranium**:
```
Element: Uranium (U), Z = 92

Natural isotopes:
  U-234: 0.0054% (trace, often ignored)
  U-235: 0.7204%
  U-238: 99.2742%

Atomic masses:
  U-234: 234.040952 amu
  U-235: 235.043930 amu
  U-238: 238.050788 amu

Average atomic mass:
  A_avg = 0.000054×234.04 + 0.007204×235.04 + 0.992742×238.05
  A_avg = 0.0126 + 1.694 + 236.322 = 238.03 amu
```

**MCNP Material Card Options**:

**Option 1 - Natural mix (simplest)**:
```
c Natural uranium metal
c ρ = 19.05 g/cm³
M1  92000.80c  1.0          $ Natural uranium
10  1  -19.05  -100         $ Uranium metal
```

**Option 2 - Explicit isotopes (U-234, U-235, U-238)**:
```
c Natural uranium metal (explicit)
M2  92234.80c  0.000054     $ U-234 (0.0054%)
    92235.80c  0.007204     $ U-235 (0.7204%)
    92238.80c  0.992742     $ U-238 (99.2742%)
c Verify: 0.000054 + 0.007204 + 0.992742 = 1.000 ✓
10  2  -19.05  -100         $ Uranium metal
```

**Option 3 - Ignore U-234 (common approximation)**:
```
c Natural uranium (U-234 ignored)
M3  92235.80c  0.0072       $ U-235 (0.72%)
    92238.80c  0.9928       $ U-238 (99.28%)
c Verify: 0.0072 + 0.9928 = 1.000 ✓
```

**When to Include U-234**:
- High-precision criticality calculations
- Long-term decay/burnup studies
- Isotopic inventory tracking
- **Can usually ignore** for shielding and basic criticality

## Use Case 4: Find Decay Data for Radioactive Source (Co-60)

**Problem**: Define Co-60 gamma source, need decay information

**Lookup - Co-60**:
```
Isotope: Cobalt-60 (Co-60)
ZAID: 27060
Z = 27, A = 60

Decay properties:
  Mode: β⁻ decay to Ni-60
  Half-life: 5.2714 years = 1.925 × 10⁸ seconds
  Decay constant: λ = ln(2)/t₁/₂ = 3.60 × 10⁻⁹ s⁻¹

Gamma emissions (2 per decay):
  E₁ = 1.173 MeV (99.85% intensity)
  E₂ = 1.332 MeV (99.98% intensity)

Beta emission:
  E_max = 0.318 MeV (99.88% branching)
```

**MCNP Source Definition**:
```
c Co-60 source: 10 Ci = 3.7×10¹¹ Bq
c 2 gammas per decay = 7.4×10¹¹ gammas/s
c
SDEF  PAR=2  ERG=D1  POS=0 0 0  WGT=7.4E11
c
c Energy distribution (2 gammas)
SI1  L  1.173  1.332       $ Co-60 gamma energies (MeV)
SP1     0.5    0.5          $ Equal probability (1 of each per decay)
c
c Material definition (if modeling source material)
M1  27060.80c  1.0          $ Co-60 isotope
```

**Activity Decay Calculation**:
```
A(t) = A₀ × e^(-λt)

Example: After 5 years (t = 5 yr)
  t = 5 yr / 5.2714 yr = 0.948 half-lives
  A(5yr) = A₀ × e^(-0.693 × 0.948)
  A(5yr) = A₀ × 0.528 = 52.8% of initial
```

## Use Case 5: Verify Cross-Section Library Availability

**Problem**: Want to use Am-241, verify library available

**Lookup Process**:
```
Isotope: Americium-241 (Am-241)
ZAID: 95241

Step 1: Check if isotope exists in ENDF/B
  Am-241: Yes, available

Step 2: Check available libraries
  95241.80c → ENDF/B-VIII.0 ✓
  95241.70c → ENDF/B-VII.0 ✓
  95241.66c → ENDF/B-VI.6 ✓

Step 3: Select library (use most recent unless compatibility needed)
  Recommended: 95241.80c

Step 4: Check xsdir file
  grep "95241" $DATAPATH/xsdir
  Should see entries like:
    95241.80c  239.052 ...
```

**If Isotope NOT Available**:
```
Options when specific isotope not in library:
1. Use natural element mix (if available):
   Example: For Ag-107, use 47000.80c (natural silver)

2. Use nearby isotope as approximation:
   Example: For Np-238, might use 93237.80c (Np-237)

3. Request library addition (for production runs)

4. Use NJOY to process evaluation (advanced)
```

**MCNP Material Card**:
```
c Am-241 source (alpha emitter)
c Often in oxide form: AmO₂
c
M1  95241.80c  1.0          $ Am-241 (verify .80c available)
    8016.80c   2.0          $ O-16
c
c If .80c not available, try:
c M1  95241.70c  1.0        $ Use ENDF/B-VII.0 instead
```

## Use Case 6: Convert Element Name to ZAID

**Problem**: User specifies "boron carbide" (B₄C), need ZAIDs

**Conversion Process**:
```
Compound: B₄C (boron carbide)

Step 1: Identify elements
  - Boron (B)
  - Carbon (C)

Step 2: Look up atomic numbers
  B: Z = 5
  C: Z = 6

Step 3: Determine if natural or specific isotope needed
  - For shielding: Usually natural is fine
  - For B-10 content: Specify isotope

Step 4: Construct ZAIDs
  Natural boron: 5000
  Natural carbon: 6000
  B-10 (enriched): 5010
  B-11: 5011
  C-12: 6012

Step 5: Add library suffix
  5000.80c → natural boron
  6000.80c → natural carbon
```

**MCNP Material Card**:

**Natural B₄C**:
```
c Boron carbide (B₄C, natural isotopes)
c ρ = 2.52 g/cm³
c Molecular weight: 4×10.81 + 12.01 = 55.25 g/mol
c
M1  5000.80c  4.0          $ Boron (natural, 4 atoms)
    6000.80c  1.0          $ Carbon (natural, 1 atom)
10  1  -2.52  -100         $ B₄C shield
```

**B-10 Enriched B₄C** (95% B-10):
```
c B₄C with 95% B-10 enrichment
c ρ = 2.52 g/cm³
c
c B-10: 95% × 4 atoms = 3.8
c B-11: 5% × 4 atoms = 0.2
M2  5010.80c  3.8          $ B-10 (enriched)
    5011.80c  0.2          $ B-11 (remaining)
    6000.80c  1.0          $ Carbon
```

## Use Case 7: Identify Fission Product Isotopes

**Problem**: Model spent fuel, need important fission products

**Key Fission Products from U-235**:

**High Yield, Long-Lived**:
```
Isotope        ZAID      Half-life     Yield (%)   Importance
Tc-99          43099     211,000 yr    6.1         Long-term waste
I-129          53129     1.57×10⁷ yr   0.7         Environmental
Cs-137         55137     30.17 yr      6.2         Gamma, heat
Sr-90          38090     28.79 yr      5.8         Beta, heat
Kr-85          36085     10.76 yr      0.3         Gas, beta
Ru-106         44106     373.6 d       0.4         Beta
Ce-144         58144     284.9 d       5.5         Beta-gamma
```

**Important for Criticality**:
```
Isotope        ZAID      Thermal σ_a   Notes
Xe-135         54135     2.65×10⁶ b    Strongest absorber, "iodine pit"
Sm-149         62149     40,140 b      Long-lived poison
Sm-151         62151     15,000 b      Long-lived
Gd-155         64155     60,900 b      Strong absorber
Eu-155         63155     3,950 b
```

**MCNP Material (Simplified Fission Products)**:
```
c Spent fuel fission products (simplified)
c Major contributors to dose and reactivity
M10 43099.80c  0.061       $ Tc-99
    53129.80c  0.007       $ I-129
    55137.80c  0.062       $ Cs-137
    38090.80c  0.058       $ Sr-90
    54135.80c  0.001       $ Xe-135 (xenon poison)
    62149.80c  0.001       $ Sm-149 (samarium poison)
c Note: Normalized to ~0.19 (19% of fissions)
c Add remaining actinides and other FPs as needed
```

## Use Case 8: Determine Activation Products

**Problem**: Irradiating aluminum, find activation products

**Aluminum Activation**:
```
Parent: Al-27 (100% natural abundance)
ZAID: 13027.80c

Primary activation reaction:
  Al-27 + n → Al-28 + γ (radiative capture)

Product: Al-28
  ZAID: 13028
  Half-life: 2.245 minutes
  Decay mode: β⁻ → Si-28
  Beta energy: 2.865 MeV (max)
  Gamma: 1.779 MeV (100%)
```

**Secondary Reactions** (higher energy neutrons):
```
Al-27(n,α)Na-24:
  Product: Na-24
  ZAID: 11024
  Half-life: 14.997 hours
  Gammas: 1.369 MeV (100%), 2.754 MeV (99.86%)

Al-27(n,p)Mg-27:
  Product: Mg-27
  ZAID: 12027
  Half-life: 9.458 minutes
  Beta: 1.75 MeV (max)
  Gamma: 0.844 MeV, 1.014 MeV
```

**MCNP Activation Calculation**:
```
c Step 1: Irradiation - Model Al-27 target
M1  13027.80c  1.0         $ Natural aluminum
10  1  -2.7  -100          $ Al target
c
c F4:N  10                  $ Flux in target
c FM4  (1 10 102)           $ (n,γ) reaction rate
c
c Step 2: Extract reaction rates from output
c
c Step 3: Calculate activity
c A = φ × σ × N × V
c where φ = flux, σ = (n,γ) cross section, N = atom density
c
c Step 4: Define activated source for dose calculation
c SDEF with Al-28 decay gammas (1.779 MeV)
```

## Use Case 9: Look Up Thermal Scattering ZAIDs

**Problem**: Model light water moderated reactor, need thermal scattering

**Thermal Scattering Libraries**:

**Water (Light Water - H₂O)**:
```
Library: lwtr.nnT
  lwtr.80t → ENDF/B-VIII.0
  lwtr.70t → ENDF/B-VII.0

Temperature-dependent:
  lwtr.80t → 293.6 K
  lwtr.81t → 323.6 K
  lwtr.82t → 373.6 K
  lwtr.83t → 423.6 K
  lwtr.84t → 473.6 K
  lwtr.85t → 523.6 K
  lwtr.86t → 573.6 K
  lwtr.87t → 623.6 K
```

**Other Thermal Scattering Materials**:
```
Heavy water (D₂O):    hwtr.nnT
Graphite:             grph.nnT, graph.nnT
Beryllium:            be.nnT
Beryllium oxide:      beo.nnT
Zirconium hydride:    zrzh.nnT, zrh.nnT
Polyethylene:         poly.nnT
Benzene:              benz.nnT
```

**MCNP Material Card with Thermal Scattering**:
```
c Light water at room temperature
c ρ = 1.0 g/cm³, T = 300 K
M1  1001.80c  2.0          $ H-1 (2 atoms per molecule)
    8016.80c  1.0          $ O-16 (1 atom per molecule)
MT1  lwtr.80t              $ Thermal scattering for H in H₂O
c
10  1  -1.0  -100 IMP:N=1  $ Water cell
```

**Important Notes**:
- MT card references material number (M1 → MT1)
- Thermal scattering only applies to bound atoms (H in H₂O, not free H)
- Use for E < ~4 eV (thermal/epithermal neutrons)
- Required for accurate keff in thermal systems

## Use Case 10: Distinguish Stable vs. Radioactive Isotopes

**Problem**: Selecting isotopes for long-term shielding analysis

**Stability Determination**:

**Stable Isotopes** (t₁/₂ = ∞):
```
Element    Stable Isotopes (A)         Natural Abundance
H          1, 2                        99.985%, 0.015%
He         3, 4                        0.000137%, 99.999863%
C          12, 13                      98.93%, 1.07%
O          16, 17, 18                  99.757%, 0.038%, 0.205%
Fe         54, 56, 57, 58              5.85%, 91.75%, 2.12%, 0.28%
Pb         204, 206, 207, 208          1.4%, 24.1%, 22.1%, 52.4%
```

**Long-Lived Radioactive** (t₁/₂ > 10⁸ yr):
```
Isotope    ZAID     Half-life        Decay      Notes
K-40       19040    1.248×10⁹ yr     β⁻, EC     Primordial
Th-232     90232    1.405×10¹⁰ yr    α          Fuel cycle
U-235      92235    7.04×10⁸ yr      α          Fissile
U-238      92238    4.468×10⁹ yr     α          Fertile
Pu-239     94239    2.411×10⁴ yr     α          Fissile
```

**Selection Guide**:
```
For long-term shielding (t > 100 years):
  - Use only stable isotopes if possible
  - Exception: Very long-lived (t₁/₂ >> analysis time)

For activation analysis:
  - Model short-lived products for immediate dose
  - Model long-lived products for waste characterization

For criticality:
  - Include all actinides (U, Pu, etc.)
  - Include major fission products (Xe-135, Sm-149)
  - Stable isotopes for structural materials
```

## Common Errors and Troubleshooting

### Error 1: Incorrect ZAID Format

**Symptom**: MCNP fatal error "nuclide ZAID not found"

**Problem**: ZAID format incorrect or library not available

**Example (Bad)**:
```
M1  92-235.80c  1.0        $ WRONG! Hyphen not allowed
M2  U235.80c  1.0          $ WRONG! Must be numeric
M3  235.80c  1.0           $ WRONG! Missing atomic number
M4  92235.90c  1.0         $ WRONG! .90c library doesn't exist
```

**Fix (Good)**:
```
M1  92235.80c  1.0         $ Correct: ZZZAAA.nnX format
c     ^^ ^^^ ^^  ^
c     Z  A   lib type
```

**Verification Steps**:
1. Check Z is correct (92 for uranium)
2. Check A is correct (235 for U-235)
3. Verify library exists: `grep "92235" xsdir`
4. Use correct library type (c for continuous energy)

### Error 2: Natural Abundance Sum Doesn't Equal 1.0

**Symptom**: Warning about material normalization

**Problem**: Isotopic fractions don't sum to exactly 1.0

**Example (Bad)**:
```
c Natural chlorine
M1  17035.80c  0.76        $ Cl-35 (should be 0.7576)
    17037.80c  0.24        $ Cl-37 (should be 0.2424)
c Sum: 0.76 + 0.24 = 1.00, but individual values rounded
```

**Fix (Good)**:
```
c Natural chlorine (correct abundances)
M1  17035.80c  0.7576      $ Cl-35 (75.76%)
    17037.80c  0.2424      $ Cl-37 (24.24%)
c Verify: 0.7576 + 0.2424 = 1.0000 ✓
```

**Best Practice**:
- Use 4 significant figures for abundances
- Always verify sum = 1.0
- If sum ≠ 1.0, MCNP will normalize but issue warning
- Document source of abundance data

### Error 3: Using Wrong Atomic Mass

**Symptom**: Calculated density or atom density incorrect

**Problem**: Using average atomic mass for isotope, or vice versa

**Example (Bad)**:
```
c Enriched U-235 (93% U-235, 7% U-238)
c Using natural uranium atomic mass: A_avg = 238.03 amu
c WRONG! Should use weighted average of enriched mix
```

**Fix (Good)**:
```
c Enriched U-235 (93% U-235, 7% U-238)
c U-235: 235.044 amu
c U-238: 238.051 amu
c A_enriched = 0.93 × 235.044 + 0.07 × 238.051
c A_enriched = 218.59 + 16.66 = 235.25 amu ✓
c
c Use 235.25 amu for density calculations, not 238.03!
```

### Error 4: Forgetting Thermal Scattering for Light Nuclides

**Symptom**: keff significantly wrong for thermal systems

**Problem**: No MT card for hydrogen in water/polyethylene

**Example (Bad)**:
```
c Light water (missing thermal scattering)
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
c Missing MT1 lwtr.80t!
```

**Fix (Good)**:
```
c Light water with thermal scattering
M1  1001.80c  2.0          $ H-1
    8016.80c  1.0          $ O-16
MT1  lwtr.80t              $ Thermal scattering (REQUIRED!)
```

**When to Use MT Card**:
- H in H₂O, D₂O, polyethylene, ZrH
- C in graphite
- Be in beryllium metal or BeO
- Any bound light nuclide at thermal energies

### Error 5: Wrong Library Temperature

**Symptom**: Results don't match expected for high-temperature system

**Problem**: Using room temperature library for hot system

**Example (Bad)**:
```
c Reactor core at 900 K
c Using .80c (293.6 K library)
M1  92235.80c  1.0         $ WRONG temperature!
TMP  900                    $ Doesn't fully fix it
```

**Fix (Good)**:
```
c Reactor core at 900 K
c Use .82c library (900 K)
M1  92235.82c  1.0         $ Correct temperature library
c Or use TMP with .80c for interpolation
M2  92235.80c  1.0
TMP  900                    $ MCNP interpolates cross sections
```

**Temperature Library Guidelines**:
- T < 400 K: Use .80c with TMP
- 400 K < T < 800 K: Use .81c or TMP interpolation
- 800 K < T < 1500 K: Use .82c
- T > 1500 K: Use highest temp library + TMP

## Integration with Other Skills

### 1. **mcnp-material-builder**

Material builder uses isotope lookup for ZAID selection and atomic masses.

**Workflow**:
```
1. User specifies: "stainless steel 316"
2. material-builder: Determines composition (Fe, Cr, Ni, Mo)
3. isotope-lookup: Provides ZAIDs:
   - Fe: 26000.80c (natural)
   - Cr: 24000.80c (natural)
   - Ni: 28000.80c (natural)
   - Mo: 42000.80c (natural)
4. material-builder: Creates M card with ZAIDs
5. isotope-lookup: Provides atomic masses for density calculation
```

### 2. **mcnp-source-builder**

Source builder uses decay data for radioactive sources.

**Workflow**:
```
1. User specifies: "1 Ci Cs-137 source"
2. source-builder: Needs decay information
3. isotope-lookup: Provides:
   - Half-life: 30.17 years
   - Decay mode: β⁻ to Ba-137m
   - Gamma: 0.662 MeV (85% after Ba-137m decay)
4. source-builder: Creates SDEF with 0.662 MeV gamma
5. isotope-lookup: Activity conversion: 1 Ci = 3.7×10¹⁰ Bq
```

### 3. **mcnp-cross-section-manager**

Cross-section manager uses isotope lookup to verify library availability.

**Workflow**:
```
1. User wants: Am-243 in calculation
2. cross-section-manager: Check if available
3. isotope-lookup: ZAID = 95243, check xsdir
4. isotope-lookup: Found 95243.80c ✓
5. cross-section-manager: Confirm library loaded
```

### 4. **mcnp-burnup-builder**

Burnup builder uses isotope properties for depletion chains.

**Workflow**:
```
1. burnup-builder: Setting up fuel depletion
2. isotope-lookup: Provides fissile isotopes (U-235, Pu-239, etc.)
3. isotope-lookup: Provides decay constants for actinides
4. isotope-lookup: Provides fission product yield data
5. burnup-builder: Constructs BURN card
```

### 5. **mcnp-physics-builder**

Physics builder uses thermal scattering ZAIDs.

**Workflow**:
```
1. physics-builder: Setting up thermal reactor
2. User specifies: Light water moderator
3. isotope-lookup: Provides lwtr.80t for MT card
4. physics-builder: Adds MT1 lwtr.80t to input
```

## Validation Checklist

Before using isotope information:

- [ ] ZAID format correct (ZZZAAA.nnX)
- [ ] Atomic number Z matches element
- [ ] Mass number A correct for isotope
- [ ] Library suffix appropriate (.80c typical)
- [ ] Library available in xsdir file
- [ ] Natural abundances sum to 1.0 (if using multiple isotopes)
- [ ] Atomic mass appropriate (isotopic vs. average)
- [ ] Decay data current (half-life, energies, branching)
- [ ] Thermal scattering (MT card) included for light nuclides
- [ ] Temperature library matches system temperature
- [ ] Stable vs. radioactive correctly identified
- [ ] Documented isotope selection in comments

## Advanced Topics

### 1. Isotopic Enrichment Calculations

**LEU (Low-Enriched Uranium) - 4.5% U-235**:
```
Natural U: 0.72% U-235
Target: 4.5% U-235

Material composition:
  U-235: 4.5% = 0.045 atom fraction
  U-238: 95.5% = 0.955 atom fraction
  (Ignore U-234 for this example)

MCNP M card:
M1  92235.80c  0.045       $ U-235 (4.5% enriched)
    92238.80c  0.955       $ U-238 (balance)

Atomic mass of mix:
A_LEU = 0.045 × 235.044 + 0.955 × 238.051
A_LEU = 10.577 + 227.339 = 237.92 amu

Density: ρ = 19.05 g/cm³ (metallic uranium)
```

**Weapons-Grade Pu (93% Pu-239)**:
```
Composition:
  Pu-239: 93%
  Pu-240: 7%

MCNP M card:
M2  94239.80c  0.93        $ Pu-239 (93%)
    94240.80c  0.07        $ Pu-240 (7%)
```

### 2. Isotope Production and Decay Chains

**Neptunium-237 Production from U-238**:
```
Reaction chain:
  U-238 + n → U-239 + γ
  U-239 → Np-239 + β⁻ (t₁/₂ = 23.5 min)
  Np-239 → Pu-239 + β⁻ (t₁/₂ = 2.356 d)

Side reaction:
  U-238 + 2n → U-237 + γ + n
  U-237 → Np-237 + β⁻ (t₁/₂ = 6.75 d)

Result: Np-237 accumulates in spent fuel
```

**Activation Chain Example - Mn-54 from Fe-54**:
```
Fe-54(n,p)Mn-54:
  Parent: Fe-54 (5.85% of natural Fe)
  Product: Mn-54
  Half-life: 312.3 days
  Gamma: 0.835 MeV (99.98%)

Used for: Radiation damage studies in steel
```

### 3. Metastable States

**Tc-99m (Metastable Technetium-99)**:
```
Ground state: Tc-99
  ZAID: 43099
  Half-life: 211,000 years

Metastable state: Tc-99m
  ZAID: 43099 (same, or 43399 in some codes)
  Half-life: 6.01 hours
  Decay: IT (isomeric transition) to Tc-99
  Gamma: 0.140 MeV (89%)

Medical use: Diagnostic imaging

MCNP doesn't typically distinguish metastable states in ZAID
Model as separate isotopes if needed for activation
```

### 4. Natural Radioactivity in Common Materials

**Potassium**:
```
K-40: 0.0117% of natural potassium
  ZAID: 19040
  Half-life: 1.248×10⁹ years
  Decay: β⁻ (89.3%) → Ca-40
         EC (10.7%) → Ar-40
  Gamma: 1.461 MeV (10.7%)

Activity in human body (~140 g K):
  A = N × λ
  N = 140 g × 0.000117 × (6.022×10²³ / 39.1)
  A ≈ 4400 Bq

MCNP material:
M1  19000.80c  1.0         $ Natural potassium (includes K-40)
```

**Concrete (contains U, Th, K)**:
```
Typical activity: ~1 Bq/g
Sources:
  - K-40: ~0.3 Bq/g
  - U-238 series: ~0.3 Bq/g
  - Th-232 series: ~0.3 Bq/g

For shielding calculations:
  - Usually negligible vs. primary source
  - Important for background studies
  - Model if needed for low-level counting
```

### 5. Isotope Separation and Enrichment

**Methods**:
```
1. Gaseous diffusion (UF₆)
   - Uses mass difference (¹²³⁵UF₆ vs. ¹²³⁸UF₆)
   - Many stages needed (cascade)

2. Gas centrifuge
   - Higher efficiency than diffusion
   - Current commercial method

3. Laser isotope separation
   - SILEX, AVLIS processes
   - Very selective

4. Electromagnetic separation (Calutron)
   - Historical (Manhattan Project)
   - Very pure but low yield
```

**MCNP Modeling**:
```
Use enrichment specification to determine isotopic fractions
Example: 20% enriched U:
  M1  92235.80c  0.20
      92238.80c  0.80
```

## Quick Reference: Common Isotopes

| Element | ZAID (natural) | Common Isotopes | Natural Abundance |
|---------|----------------|-----------------|-------------------|
| H       | 1000.80c       | H-1, H-2 (D)    | 99.99%, 0.015%   |
| B       | 5000.80c       | B-10, B-11      | 19.9%, 80.1%     |
| C       | 6000.80c       | C-12, C-13      | 98.93%, 1.07%    |
| N       | 7000.80c       | N-14, N-15      | 99.63%, 0.37%    |
| O       | 8000.80c       | O-16, O-17, O-18| 99.76%, 0.04%, 0.20% |
| Al      | 13000.80c      | Al-27           | 100%             |
| Si      | 14000.80c      | Si-28, -29, -30 | 92.2%, 4.7%, 3.1%|
| Cl      | 17000.80c      | Cl-35, Cl-37    | 75.76%, 24.24%   |
| Fe      | 26000.80c      | Fe-54, -56, -57, -58 | 5.85%, 91.75%, 2.12%, 0.28% |
| Cu      | 29000.80c      | Cu-63, Cu-65    | 69.15%, 30.85%   |
| Pb      | 82000.80c      | Pb-204, -206, -207, -208 | 1.4%, 24.1%, 22.1%, 52.4% |
| U       | 92000.80c      | U-235, U-238    | 0.72%, 99.27%    |

## Quick Reference: Radioactive Isotopes

| Isotope | ZAID      | Half-life  | Decay | Gamma (MeV) | Use            |
|---------|-----------|------------|-------|-------------|----------------|
| H-3     | 1003.80c  | 12.3 yr    | β⁻    | None        | Fusion, tracer |
| Co-60   | 27060.80c | 5.27 yr    | β⁻    | 1.17, 1.33  | Calibration    |
| Sr-90   | 38090.80c | 28.8 yr    | β⁻    | None        | Fission product|
| Cs-137  | 55137.80c | 30.2 yr    | β⁻    | 0.662       | Calibration    |
| Ir-192  | 77192.80c | 73.8 d     | β⁻    | 0.3-0.6     | Radiography    |
| U-235   | 92235.80c | 7.04×10⁸ yr| α     | Various     | Fissile fuel   |
| U-238   | 92238.80c | 4.47×10⁹ yr| α     | Various     | Fertile fuel   |
| Pu-239  | 94239.80c | 2.41×10⁴ yr| α     | Various     | Fissile fuel   |
| Am-241  | 95241.80c | 432.2 yr   | α     | 0.060       | Smoke detector |

## Best Practices

1. **Always Verify ZAID Format**
   ```
   Correct: 92235.80c (U-235 with ENDF/B-VIII.0)
   Check: ZZZAAA.nnX where each component makes sense
   ```

2. **Document Isotope Choices**
   ```
   c Material: Lead shielding
   c Using natural lead (82000) for simplicity
   c Could use explicit isotopes if needed for precision
   M1  82000.80c  1.0
   ```

3. **Use Natural Mix When Appropriate**
   ```
   For shielding: Natural is usually fine
   For criticality: May need specific isotopes (U-235 vs. U-238)
   For activation: Need specific isotopes (Al-27 for activation)
   ```

4. **Check Abundance Normalization**
   ```
   Always verify: Σ f_i = 1.0
   Document if intentionally not normalized
   ```

5. **Use Correct Atomic Mass**
   ```
   Isotopic mass: For specific isotope
   Average mass: For natural element
   Enriched mass: Weighted average of mixture
   ```

6. **Include Thermal Scattering**
   ```
   For H in H₂O, C in graphite, etc.
   MT card must match M card number
   Temperature must match system
   ```

7. **Verify Library Availability**
   ```
   Check xsdir before running
   grep "ZAID" $DATAPATH/xsdir
   Use alternate if primary not available
   ```

8. **Consider Temperature Effects**
   ```
   T < 400 K: .80c + TMP OK
   T > 800 K: Use .82c or higher temp library
   ```

9. **Document Decay Data Sources**
   ```
   c Co-60 decay data from NNDC (2024)
   c Half-life: 5.2714 years
   c Gammas: 1.173 MeV, 1.332 MeV
   ```

10. **Be Consistent Across Input**
    ```
    If using natural elements in M cards:
    - Use natural everywhere unless specific reason
    If using isotopes:
    - Be consistent across all materials
    ```

## References

- **Nuclear Data Sources**:
  - NNDC (National Nuclear Data Center): www.nndc.bnl.gov
  - IAEA Nuclear Data Services: www-nds.iaea.org
  - ENDF/B cross-section libraries
  - Chart of the Nuclides (Karlsruhe, KAERI)
- **Related Skills**:
  - mcnp-material-builder (uses ZAIDs and atomic masses)
  - mcnp-source-builder (uses decay data)
  - mcnp-cross-section-manager (manages libraries)
  - mcnp-physical-constants (fundamental constants)
  - mcnp-unit-converter (unit conversions)
- **User Manual**:
  - Chapter 5.2: Material Cards (ZAID format)
  - Appendix G: ZAID cross-section library tables
  - Appendix H: Atomic mass and abundance tables
- **External Resources**:
  - NIST Atomic Weights and Isotopic Compositions
  - ICRP Publication 107 (decay data)
  - Nuclear Wallet Cards (Jagdish K. Tuli)

---

**End of MCNP Isotope Lookup Skill**
