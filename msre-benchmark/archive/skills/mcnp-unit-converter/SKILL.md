---
category: F
name: mcnp-unit-converter
description: Convert between different unit systems for MCNP input parameters including energy, length, density, temperature, cross sections, activity, mass, angle, and time units
activation_keywords:
  - unit conversion
  - convert units
  - unit converter
  - change units
  - MeV to eV
  - cm to meters
  - barns conversion
  - temperature units
  - density conversion
---

# MCNP Unit Converter Skill

## Purpose

This utility skill provides comprehensive unit conversion capabilities for MCNP simulations. It helps Claude accurately convert between different measurement systems when creating or editing MCNP inputs, ensuring physical consistency and reducing errors from unit mismatches. This skill integrates with all MCNP skills that require numerical parameters.

## When to Use This Skill

- Converting energy units for source definitions (MeV ↔ eV ↔ keV ↔ J)
- Converting length units for geometry specifications (cm ↔ m ↔ mm ↔ inches)
- Converting density units for material definitions (g/cm³ ↔ kg/m³ ↔ atom/b-cm)
- Converting temperature between Kelvin and energy units (K ↔ MeV ↔ eV)
- Converting cross section units (barns ↔ cm² ↔ mb)
- Converting activity units for source strength (Bq ↔ Ci ↔ dps)
- Converting mass units for atomic/nuclear calculations (g ↔ kg ↔ amu)
- Converting angle units for source directions (degrees ↔ radians)
- Converting time units for time-dependent problems (s ↔ shakes ↔ ns)
- Verifying dimensional consistency across MCNP input cards

## Prerequisites

- **mcnp-material-builder**: Uses converted densities and atomic masses
- **mcnp-source-builder**: Uses converted energies and activities
- **mcnp-geometry-builder**: Uses converted lengths and dimensions
- **mcnp-physics-builder**: Uses converted temperatures and energy cutoffs
- Basic understanding of SI and CGS unit systems
- Familiarity with nuclear physics units (barns, MeV, amu)

## Core Concepts

### MCNP Standard Units

**Primary Units in MCNP**:
- **Energy**: MeV (mega-electron volts)
- **Length**: cm (centimeters)
- **Density**: g/cm³ (grams per cubic centimeter) or atom/b-cm
- **Temperature**: MeV (as thermal energy) or Kelvin (on TMP card)
- **Cross Section**: barns (10⁻²⁴ cm²)
- **Time**: shakes (10⁻⁸ seconds)
- **Mass**: amu (atomic mass units)
- **Angle**: degrees (for some cards) or cosines

### Fundamental Conversion Constants

**Physical Constants**:
- Speed of light: c = 2.99792458 × 10⁸ m/s
- Avogadro's number: N_A = 6.02214076 × 10²³ mol⁻¹
- Boltzmann constant: k_B = 8.617333262 × 10⁻⁵ eV/K = 8.617333262 × 10⁻¹¹ MeV/K
- Atomic mass unit: 1 amu = 1.66053906660 × 10⁻²⁷ kg = 931.494102 MeV/c²
- Electron volt: 1 eV = 1.602176634 × 10⁻¹⁹ J
- Barn: 1 b = 10⁻²⁴ cm²

### Energy Conversions

**Energy Units**:
- 1 MeV = 10⁶ eV = 10³ keV = 10⁻³ GeV
- 1 MeV = 1.602176634 × 10⁻¹³ J
- 1 J = 6.241509074 × 10¹² MeV
- Temperature: T(K) = E(MeV) / (8.617333262 × 10⁻¹¹)
- Temperature: T(K) = E(eV) / (8.617333262 × 10⁻⁵)

### Length Conversions

**Length Units**:
- 1 cm = 10⁻² m = 10 mm = 0.393701 inches
- 1 m = 100 cm = 39.3701 inches = 3.28084 feet
- 1 inch = 2.54 cm
- 1 Angstrom = 10⁻⁸ cm = 10⁻¹⁰ m

### Density Conversions

**Density Units**:
- 1 g/cm³ = 1000 kg/m³ = 0.001 kg/cm³
- atom/b-cm = (ρ_g/cm³ × N_A) / (A × 10²⁴)
  - ρ = mass density (g/cm³)
  - A = atomic mass (g/mol)
  - N_A = Avogadro's number

**Example**: Water at 1 g/cm³ with A = 18 g/mol
- atom/b-cm = (1 × 6.022×10²³) / (18 × 10²⁴) = 0.03346 atom/b-cm

### Cross Section Conversions

**Cross Section Units**:
- 1 barn (b) = 10⁻²⁴ cm²
- 1 millibarn (mb) = 10⁻³ b = 10⁻²⁷ cm²
- 1 cm² = 10²⁴ b

### Activity Conversions

**Activity Units**:
- 1 Becquerel (Bq) = 1 disintegration/second (dps)
- 1 Curie (Ci) = 3.7 × 10¹⁰ Bq
- 1 mCi = 3.7 × 10⁷ Bq
- 1 μCi = 3.7 × 10⁴ Bq

### Mass Conversions

**Mass Units**:
- 1 amu = 1.66053906660 × 10⁻²⁴ g = 931.494102 MeV/c²
- 1 g = 6.02214076 × 10²³ amu
- 1 kg = 1000 g

### Time Conversions

**Time Units**:
- 1 shake = 10⁻⁸ s = 10 ns
- 1 s = 10⁸ shakes
- 1 μs = 10⁻⁶ s = 100 shakes
- 1 ns = 10⁻⁹ s = 0.1 shakes

### Angle Conversions

**Angle Units**:
- 1 radian = 180/π degrees ≈ 57.2958 degrees
- 1 degree = π/180 radians ≈ 0.0174533 radians
- Cosine for MCNP direction vectors: cos(θ) where θ in radians

## Decision Tree: Unit Conversion

```
START: Need to convert units for MCNP input
  |
  +--> What physical quantity?
  |      |
  |      +--> Energy
  |      |      ├─> From: MeV, eV, keV, GeV, J
  |      |      ├─> To: MeV (MCNP standard)
  |      |      ├─> Formula: Use energy conversion factors
  |      |      └─> Example: 1.5 keV → 0.0015 MeV
  |      |
  |      +--> Length
  |      |      ├─> From: m, mm, inches, Angstroms
  |      |      ├─> To: cm (MCNP standard)
  |      |      ├─> Formula: Use length conversion factors
  |      |      └─> Example: 2.5 m → 250 cm
  |      |
  |      +--> Density
  |      |      ├─> From: kg/m³, atom/b-cm
  |      |      ├─> To: g/cm³ or atom/b-cm (MCNP accepts both)
  |      |      ├─> Formula: kg/m³ / 1000 = g/cm³
  |      |      ├─> Formula: atom/b-cm = (ρ × N_A) / (A × 10²⁴)
  |      |      └─> Example: 1000 kg/m³ → 1 g/cm³
  |      |
  |      +--> Temperature
  |      |      ├─> From: K, eV, MeV
  |      |      ├─> To: MeV or K (both used in MCNP)
  |      |      ├─> Formula: E(MeV) = k_B × T(K) = 8.617×10⁻¹¹ × T(K)
  |      |      ├─> Formula: T(K) = E(MeV) / (8.617×10⁻¹¹)
  |      |      └─> Example: 300 K → 2.585×10⁻⁸ MeV
  |      |
  |      +--> Cross Section
  |      |      ├─> From: cm², mb
  |      |      ├─> To: barns (MCNP reports in barns)
  |      |      ├─> Formula: cm² × 10²⁴ = barns
  |      |      └─> Example: 1×10⁻²⁴ cm² → 1 barn
  |      |
  |      +--> Activity
  |      |      ├─> From: Ci, mCi, μCi, dps
  |      |      ├─> To: Bq or particles/s for SDEF
  |      |      ├─> Formula: Ci × 3.7×10¹⁰ = Bq
  |      |      └─> Example: 1 mCi → 3.7×10⁷ Bq
  |      |
  |      +--> Mass
  |      |      ├─> From: kg, amu
  |      |      ├─> To: g or amu (context dependent)
  |      |      ├─> Formula: amu × 1.6605×10⁻²⁴ = g
  |      |      └─> Example: 235.044 amu → 3.903×10⁻²² g
  |      |
  |      +--> Time
  |      |      ├─> From: s, μs, ns
  |      |      ├─> To: shakes (for TYME card)
  |      |      ├─> Formula: s × 10⁸ = shakes
  |      |      └─> Example: 1 μs → 100 shakes
  |      |
  |      └─> Angle
  |             ├─> From: degrees
  |             ├─> To: radians or cosine
  |             ├─> Formula: deg × (π/180) = radians
  |             ├─> Formula: cos(radians) for direction
  |             └─> Example: 45° → 0.7071 (cosine)
  |
  +--> Apply conversion
  |      ├─> Use appropriate formula
  |      ├─> Verify significant figures
  |      └─> Check result makes physical sense
  |
  +--> Verify dimensional consistency
         ├─> Check all related parameters use consistent units
         ├─> Example: If density in g/cm³, volume must be cm³
         └─> Document conversion in comments
```

## Tool Invocation

This skill includes a Python implementation for automated unit conversions. The `MCNPUnitConverterSkill` class provides programmatic access to all conversion functions.

### Importing the Tool

```python
from mcnp_unit_converter import MCNPUnitConverterSkill

# Initialize the converter
converter = MCNPUnitConverterSkill()
```

### Basic Usage

**Convert Energy**:
```python
# Convert keV to MeV
mev = converter.convert_energy(14.1, 'keV', 'MeV')
# Result: 0.0141 MeV

# Convert eV to MeV
mev = converter.convert_energy(1000000, 'eV', 'MeV')
# Result: 1.0 MeV
```

**Convert Length**:
```python
# Convert inches to cm
cm = converter.convert_length(1.0, 'inch', 'cm')
# Result: 2.54 cm

# Convert meters to cm
cm = converter.convert_length(1.5, 'm', 'cm')
# Result: 150.0 cm
```

**Convert Density (g/cm³ to atoms/b-cm)**:
```python
# Water: density 1.0 g/cm³, molecular weight 18.015 g/mol
atoms_per_b_cm = converter.density_g_to_atoms(1.0, 18.015)
# Result: 0.03343 atoms/b-cm

# Aluminum: density 2.7 g/cm³, atomic weight 26.982 g/mol
atoms_per_b_cm = converter.density_g_to_atoms(2.7, 26.982)
# Result: 0.06026 atoms/b-cm
```

### Integration with MCNP Workflow

The Python tool automates conversions when building input files programmatically:

```python
# Example: Building material card with density conversion
from mcnp_unit_converter import MCNPUnitConverterSkill
converter = MCNPUnitConverterSkill()

# User provides density in kg/m³
density_kg_m3 = 2700  # Aluminum
atomic_weight = 26.982

# Convert to g/cm³
density_g_cm3 = density_kg_m3 / 1000

# Convert to atoms/b-cm for MCNP
atoms_per_b_cm = converter.density_g_to_atoms(density_g_cm3, atomic_weight)

# Generate MCNP material card
print(f"m1 13027.80c -{atoms_per_b_cm:.5f}  $ Al at {density_kg_m3} kg/m³")
# Output: m1 13027.80c -0.06026  $ Al at 2700 kg/m³
```

---

## Use Case 1: Convert Source Energy from keV to MeV

**Problem**: User provides neutron source energy as 14.1 keV, need MeV for SDEF card

**Input**:
```
Source energy: 14.1 keV
```

**Conversion**:
```
Energy (MeV) = Energy (keV) / 1000
Energy (MeV) = 14.1 / 1000 = 0.0141 MeV
```

**MCNP Input**:
```
c Neutron source at 14.1 keV = 0.0141 MeV
SDEF  PAR=1  ERG=0.0141
```

**Verification**:
- 14.1 keV × 10⁻³ = 0.0141 MeV ✓
- Energy reasonable for thermal/epithermal neutrons ✓

## Use Case 2: Convert Density from kg/m³ to g/cm³

**Problem**: Material density given as 7850 kg/m³ (steel), need g/cm³ for M card

**Input**:
```
Density: 7850 kg/m³
```

**Conversion**:
```
Density (g/cm³) = Density (kg/m³) / 1000
Density (g/cm³) = 7850 / 1000 = 7.85 g/cm³
```

**MCNP Input**:
```
c Steel density: 7850 kg/m³ = 7.85 g/cm³
M1  26000.80c  -0.98        $ Iron (98% by weight)
    6000.80c   -0.02        $ Carbon (2% by weight)
10  1  -7.85  -100          $ Cell with steel at 7.85 g/cm³
```

**Verification**:
- 7850 kg/m³ = 7.85 g/cm³ ✓
- Density typical for steel ✓

## Use Case 3: Convert Temperature from Celsius to MeV

**Problem**: Material at 500°C, need temperature for TMP card

**Input**:
```
Temperature: 500°C
```

**Conversion**:
```
Step 1: Convert to Kelvin
T(K) = T(°C) + 273.15
T(K) = 500 + 273.15 = 773.15 K

Step 2: Convert to MeV
E(MeV) = k_B × T(K)
k_B = 8.617333262 × 10⁻¹¹ MeV/K
E(MeV) = 8.617333262 × 10⁻¹¹ × 773.15
E(MeV) = 6.662 × 10⁻⁸ MeV
```

**MCNP Input**:
```
c Temperature: 500°C = 773.15 K = 6.662×10⁻⁸ MeV
TMP  6.662E-8
```

**Alternative** (Using Kelvin directly):
```
c Temperature: 500°C = 773.15 K
TMP  773.15           $ TMP accepts Kelvin directly
```

**Verification**:
- Room temperature (~300 K) ≈ 2.585×10⁻⁸ MeV
- 773 K should be ~2.6× room temperature energy ✓

## Use Case 4: Convert Activity from mCi to Particles/Second

**Problem**: Co-60 source at 10 mCi, need particles/s for WGT parameter

**Input**:
```
Activity: 10 mCi Co-60
Branching ratio: 2 gammas per decay
```

**Conversion**:
```
Step 1: Convert mCi to Bq
Activity (Bq) = Activity (mCi) × 3.7 × 10⁷
Activity (Bq) = 10 × 3.7 × 10⁷ = 3.7 × 10⁸ Bq

Step 2: Account for branching
Gammas/s = Activity (Bq) × gammas per decay
Gammas/s = 3.7 × 10⁸ × 2 = 7.4 × 10⁸ gammas/s

Step 3: Normalize for MCNP (usually run 1 source particle)
WGT = 7.4 × 10⁸  (source weight)
```

**MCNP Input**:
```
c Co-60 source: 10 mCi = 3.7×10⁸ Bq
c 2 gammas per decay = 7.4×10⁸ gammas/s
SDEF  PAR=2  ERG=D1  POS=0 0 0  WGT=7.4E8
SI1  L  1.173  1.332  $ Co-60 gamma energies (MeV)
SP1     0.5    0.5    $ Equal probability
```

**Verification**:
- 1 mCi = 3.7×10⁷ Bq ✓
- 10 mCi = 3.7×10⁸ Bq ✓
- Co-60 has 2 gammas per decay ✓

## Use Case 5: Convert Geometry Dimensions from Meters to Centimeters

**Problem**: Cylindrical tank dimensions given in meters, need cm for surface cards

**Input**:
```
Radius: 2.5 m
Height: 5.0 m
```

**Conversion**:
```
Radius (cm) = Radius (m) × 100
Radius (cm) = 2.5 × 100 = 250 cm

Height (cm) = Height (m) × 100
Height (cm) = 5.0 × 100 = 500 cm
```

**MCNP Input**:
```
c Cylindrical tank: R=2.5m, H=5.0m (converted to cm)
c R = 250 cm, H = 500 cm
c
c Surface cards
10  CZ   250            $ Cylinder radius 2.5 m = 250 cm
20  PZ   0              $ Bottom plane
30  PZ   500            $ Top plane at 5 m = 500 cm
c
c Cell cards
1   1  -1.0  -10 20 -30  $ Water inside cylinder
2   0       10:-20:30   $ Void outside
```

**Verification**:
- 2.5 m = 250 cm ✓
- 5.0 m = 500 cm ✓
- Volume = πr²h = π(250)²(500) = 9.817×10⁷ cm³ ✓

## Use Case 6: Convert Atomic Density to g/cm³

**Problem**: Material specified as 0.024 atom/b-cm, need g/cm³ for comparison

**Input**:
```
Atomic density: 0.024 atom/b-cm
Atomic mass: 238 g/mol (Uranium-238)
```

**Conversion**:
```
Formula: ρ (g/cm³) = (N × A × 10²⁴) / N_A
where:
  N = atomic density (atom/b-cm) = 0.024
  A = atomic mass (g/mol) = 238
  N_A = Avogadro's number = 6.022×10²³

ρ = (0.024 × 238 × 10²⁴) / (6.022×10²³)
ρ = (5.712 × 10²⁴) / (6.022×10²³)
ρ = 9.485 g/cm³
```

**Verification**:
- Uranium metal density ≈ 19 g/cm³
- Our result (9.485 g/cm³) suggests 50% packing or UO₂
- Reasonable for nuclear fuel ✓

**Reverse Conversion** (g/cm³ to atom/b-cm):
```
N (atom/b-cm) = (ρ × N_A) / (A × 10²⁴)
N = (9.485 × 6.022×10²³) / (238 × 10²⁴)
N = 0.024 atom/b-cm ✓
```

## Use Case 7: Convert Cross Section from cm² to Barns

**Problem**: Microscopic cross section given as 5.8 × 10⁻²⁴ cm², need barns

**Input**:
```
Cross section: 5.8 × 10⁻²⁴ cm²
```

**Conversion**:
```
σ (barns) = σ (cm²) × 10²⁴
σ (barns) = 5.8 × 10⁻²⁴ × 10²⁴
σ (barns) = 5.8 barns
```

**Context**:
```
c Microscopic absorption cross section
c σ_a = 5.8 × 10⁻²⁴ cm² = 5.8 barns
c Typical for thermal neutron absorption
c (e.g., similar to U-235 at 0.0253 eV)
```

**Macroscopic Cross Section**:
```
If atomic density N = 0.048 atom/b-cm:
Σ (cm⁻¹) = σ (barns) × N (atom/b-cm) × 10⁻²⁴
Σ = 5.8 × 0.048 × 10⁻²⁴
Σ = 2.784 × 10⁻²⁵ cm⁻¹

Wait, this is wrong. Correct formula:
Σ (cm⁻¹) = σ (cm²) × N (atom/cm³)

Convert atom/b-cm to atom/cm³:
N (atom/cm³) = N (atom/b-cm) × 10²⁴
N = 0.048 × 10²⁴ = 4.8 × 10²²

Σ = 5.8 × 10⁻²⁴ cm² × 4.8 × 10²² atom/cm³
Σ = 0.2784 cm⁻¹
```

**Verification**:
- 1 barn = 10⁻²⁴ cm² (by definition) ✓
- 5.8 barns is typical thermal absorption ✓

## Use Case 8: Convert Time from Microseconds to Shakes

**Problem**: Pulse duration 5 μs, need shakes for TYME card

**Input**:
```
Time: 5 μs
```

**Conversion**:
```
Time (shakes) = Time (μs) × 100
Time (shakes) = 5 × 100 = 500 shakes

Alternative:
Time (shakes) = Time (s) × 10⁸
Time (μs) = 5 × 10⁻⁶ s
Time (shakes) = 5 × 10⁻⁶ × 10⁸ = 500 shakes
```

**MCNP Input**:
```
c Pulse duration: 5 μs = 500 shakes
c Time bins for tally
T4  0  100  200  300  400  500   $ 0 to 5 μs in 1 μs bins (100 shakes)
```

**Verification**:
- 1 μs = 100 shakes ✓
- 5 μs = 500 shakes ✓
- 1 shake = 10 ns ✓

## Use Case 9: Convert Angle from Degrees to Direction Cosines

**Problem**: Source pointing 30° from Z-axis, need direction cosines for VEC parameter

**Input**:
```
Polar angle θ = 30° from Z-axis
Azimuthal angle φ = 0° (in XZ plane)
```

**Conversion**:
```
Direction vector (u, v, w):
  u = sin(θ) × cos(φ)
  v = sin(θ) × sin(φ)
  w = cos(θ)

Convert degrees to radians:
  θ_rad = 30° × (π/180) = 0.5236 rad
  φ_rad = 0° × (π/180) = 0 rad

Calculate components:
  u = sin(0.5236) × cos(0) = 0.5 × 1 = 0.5
  v = sin(0.5236) × sin(0) = 0.5 × 0 = 0
  w = cos(0.5236) = 0.866

Verify normalization: u² + v² + w² = 0.25 + 0 + 0.75 = 1.0 ✓
```

**MCNP Input**:
```
c Beam at 30° from Z-axis in XZ plane
c θ = 30°, φ = 0° → (u,v,w) = (0.5, 0, 0.866)
SDEF  PAR=1  ERG=14  POS=0 0 0  VEC=0.5 0 0.866  DIR=1
```

**Verification**:
- cos(30°) = 0.866 ✓
- sin(30°) = 0.5 ✓
- Direction vector normalized ✓

## Use Case 10: Multi-Step Conversion (Engineering Units to MCNP)

**Problem**: Neutron flux measurement from detector in n/(cm²·s·W), need to scale for 100 MW reactor

**Input**:
```
Measured flux: 5.2 × 10⁸ n/(cm²·s·W)
Reactor power: 100 MW
Source strength calibration needed
```

**Conversion**:
```
Step 1: Convert power to watts
P = 100 MW × 10⁶ = 1 × 10⁸ W

Step 2: Calculate actual flux
Φ = 5.2 × 10⁸ n/(cm²·s·W) × 1 × 10⁸ W
Φ = 5.2 × 10¹⁶ n/(cm²·s)

Step 3: Relate to MCNP normalization
MCNP runs 1 source neutron by default
Scale factor = actual flux / MCNP flux

If MCNP gives Φ_MCNP = 2.3 × 10⁻⁶ (per source particle):
Scale = 5.2 × 10¹⁶ / 2.3 × 10⁻⁶ = 2.26 × 10²² source particles

Step 4: Convert to source intensity
Source rate = 2.26 × 10²² n/s
```

**MCNP Application**:
```
c Reactor: 100 MW = 1×10⁸ W
c Measured flux: 5.2×10⁸ n/(cm²·s·W)
c Actual flux: 5.2×10¹⁶ n/(cm²·s)
c
c Run MCNP with default (1 source particle)
c Multiply F4 tally results by 2.26×10²²
c to get actual flux values
```

## Use Case 11: Convert Photon Energy from Wavelength

**Problem**: X-ray wavelength 0.71 Å (Mo K-α), need energy in MeV

**Input**:
```
Wavelength: 0.71 Å
```

**Conversion**:
```
Formula: E (eV) = hc / λ
where:
  h = Planck's constant = 4.136 × 10⁻¹⁵ eV·s
  c = speed of light = 2.998 × 10⁸ m/s
  λ = wavelength

Simplified: E (eV) = 12398.4 / λ(Å)

Step 1: Calculate energy in eV
E = 12398.4 / 0.71 = 17463 eV

Step 2: Convert to keV
E = 17463 / 1000 = 17.463 keV

Step 3: Convert to MeV
E = 17.463 / 1000 = 0.017463 MeV
```

**MCNP Input**:
```
c Mo K-α X-ray: λ = 0.71 Å → E = 17.463 keV = 0.017463 MeV
SDEF  PAR=2  ERG=0.017463  POS=0 0 0
```

**Verification**:
- Typical Mo K-α energy ≈ 17.4 keV ✓
- X-ray energy range 1-100 keV ✓

## Use Case 12: Convert Macroscopic Cross Section to Mean Free Path

**Problem**: Material has Σ_t = 0.35 cm⁻¹, need mean free path

**Input**:
```
Total macroscopic cross section: Σ_t = 0.35 cm⁻¹
```

**Conversion**:
```
Mean free path: λ = 1 / Σ_t

λ = 1 / 0.35 cm⁻¹
λ = 2.857 cm

This is the average distance a neutron travels before interaction.
```

**MCNP Context**:
```
c Material with Σ_t = 0.35 cm⁻¹
c Mean free path = 2.857 cm
c
c For geometry: make cells >> λ for good statistics
c Recommended: cell dimension > 3-5 × λ
c Minimum cell size: ~8.6 to 14.3 cm
c
c For variance reduction:
c Import regions should be ~ λ in size
```

**Related Conversions**:
```
Relaxation length = λ (same as mean free path)
Attenuation coefficient μ = Σ_t (same value)
Half-value layer = 0.693 × λ = 1.98 cm
Tenth-value layer = 2.303 × λ = 6.58 cm
```

## Use Case 13: Convert Particle Fluence to Dose

**Problem**: Neutron fluence 1 × 10¹⁰ n/cm², need dose equivalent in rem

**Input**:
```
Neutron fluence: Φ_total = 1 × 10¹⁰ n/cm²
Average neutron energy: 1 MeV
```

**Conversion**:
```
Use fluence-to-dose conversion factor from ICRP 74/116

For 1 MeV neutrons:
DCF = 3.7 × 10⁻⁸ rem·cm² / neutron

Dose equivalent = Φ_total × DCF
H = 1 × 10¹⁰ × 3.7 × 10⁻⁸
H = 370 rem = 3.7 Sv
```

**MCNP Application**:
```
c Calculate dose from F4 tally
c F4:N  10                    $ Flux in cell 10
c
c If F4 result = 5.2 × 10⁻⁷ (per source particle)
c And NPS = 1 × 10⁸ particles
c
c Fluence = 5.2 × 10⁻⁷ × 1 × 10⁸ = 5.2 × 10¹ n/cm²
c
c Dose = 5.2 × 10¹ × 3.7 × 10⁻⁸ = 1.92 × 10⁻⁶ rem
```

**Energy-Dependent DCF**:
```
Thermal (0.025 eV):  DCF = 3.67 × 10⁻⁹ rem·cm²/n
100 keV:             DCF = 1.32 × 10⁻⁸ rem·cm²/n
1 MeV:               DCF = 3.7 × 10⁻⁸ rem·cm²/n
10 MeV:              DCF = 1.38 × 10⁻⁷ rem·cm²/n

Use energy-binned tallies for accurate dose!
```

## Use Case 14: Convert Material Atom Fractions to Weight Fractions

**Problem**: Concrete specified as atom fractions, need weight fractions for comparison

**Input (Ordinary Concrete)**:
```
Atom fractions:
  H:  0.168
  O:  0.562
  Na: 0.015
  Si: 0.180
  Ca: 0.075
```

**Conversion**:
```
Formula: w_i = (f_i × A_i) / Σ(f_j × A_j)
where:
  w_i = weight fraction of element i
  f_i = atom fraction of element i
  A_i = atomic mass of element i

Step 1: Calculate weighted sum
Atomic masses:
  H:  1.008
  O:  15.999
  Na: 22.990
  Si: 28.086
  Ca: 40.078

Denominator = 0.168×1.008 + 0.562×15.999 + 0.015×22.990
            + 0.180×28.086 + 0.075×40.078
            = 0.169 + 8.991 + 0.345 + 5.055 + 3.006
            = 17.566

Step 2: Calculate weight fractions
w_H  = (0.168 × 1.008) / 17.566 = 0.0096 (0.96%)
w_O  = (0.562 × 15.999) / 17.566 = 0.5118 (51.18%)
w_Na = (0.015 × 22.990) / 17.566 = 0.0196 (1.96%)
w_Si = (0.180 × 28.086) / 17.566 = 0.2877 (28.77%)
w_Ca = (0.075 × 40.078) / 17.566 = 0.1712 (17.12%)

Verify: 0.96 + 51.18 + 1.96 + 28.77 + 17.12 = 99.99% ✓
```

**MCNP M Card Comparison**:
```
c Atom fractions (positive):
M1  1001.80c  0.168
    8016.80c  0.562
    11023.80c 0.015
    14000.80c 0.180
    20000.80c 0.075

c Weight fractions (negative):
M2  1001.80c  -0.0096
    8016.80c  -0.5118
    11023.80c -0.0196
    14000.80c -0.2877
    20000.80c -0.1712

c Both are equivalent in MCNP!
```

## Use Case 15: Convert Volumetric Flow Rate to Particle Source Rate

**Problem**: Argon gas flow 10 L/min at STP, need particle emission rate

**Input**:
```
Flow rate: 10 L/min
Gas: Argon at STP (273.15 K, 1 atm)
Assume radioactive Kr-85 tracer at 1 Bq/L
```

**Conversion**:
```
Step 1: Convert flow to SI units
Q = 10 L/min × (1 m³/1000 L) × (1 min/60 s)
Q = 1.667 × 10⁻⁴ m³/s

Step 2: Calculate molar flow rate
At STP: 1 mole = 22.414 L
n_dot = (10 L/min) / (22.414 L/mol) × (1 min/60 s)
n_dot = 7.43 × 10⁻³ mol/s

Step 3: Calculate atom flow rate
N_dot = n_dot × N_A
N_dot = 7.43 × 10⁻³ × 6.022 × 10²³
N_dot = 4.47 × 10²¹ atoms/s

Step 4: Calculate radioactive tracer source strength
Activity concentration = 1 Bq/L = 1 decay/(L·s)
Source strength = 1 Bq/L × 10 L/min × (1 min/60 s)
Source strength = 0.167 Bq = 0.167 decays/s
```

**MCNP Source Definition**:
```
c Argon flow with Kr-85 tracer
c Flow: 10 L/min, Activity: 1 Bq/L
c Total source: 0.167 Bq
c
SDEF  PAR=2  ERG=0.514  WGT=0.167  $ Kr-85 beta (514 keV max)
```

## Common Errors and Troubleshooting

### Error 1: Confusing Mass Density and Atomic Density

**Symptom**: Material definition with unrealistic density

**Problem**: Using g/cm³ value where atom/b-cm expected or vice versa

**Example (Bad)**:
```
c Aluminum: 2.7 g/cm³ (correct mass density)
M1  13027.80c  2.7     $ WRONG! This is interpreted as 2.7 atom/b-cm
```

**Fix (Good)**:
```
c Aluminum: 2.7 g/cm³
c Convert to atom/b-cm:
c N = (ρ × N_A) / (A × 10²⁴)
c N = (2.7 × 6.022×10²³) / (27 × 10²⁴) = 0.0602 atom/b-cm
M1  13027.80c  0.0602  $ Correct atomic density

c OR use negative for mass density:
10  1  -2.7  -100      $ Cell card with mass density (negative sign)
```

**Rule**: Positive density on cell card → atom/b-cm, Negative → g/cm³

### Error 2: Temperature Conversion Sign Error

**Symptom**: Negative temperature or unreasonably high energy

**Problem**: Incorrect temperature conversion formula

**Example (Bad)**:
```
c 600 K converted incorrectly
T(MeV) = 600 / 8.617E-11 = 6.96E12 MeV  $ WRONG! Inverted formula
```

**Fix (Good)**:
```
c 600 K conversion
T(MeV) = k_B × T(K) = 8.617E-11 × 600 = 5.17E-8 MeV  $ Correct
```

**Rule**: E(MeV) = k_B × T(K), not T/k_B

### Error 3: Forgetting Unit Prefix Scaling

**Symptom**: Results off by factors of 1000, 10⁶, etc.

**Problem**: Not accounting for prefixes (k, M, m, μ)

**Example (Bad)**:
```
c 2.5 keV source
SDEF ERG=2.5      $ WRONG! This is 2.5 MeV, not 2.5 keV
```

**Fix (Good)**:
```
c 2.5 keV = 0.0025 MeV
SDEF ERG=0.0025   $ Correct: converted keV to MeV
```

**Common Prefixes**:
- k (kilo) = 10³
- M (mega) = 10⁶
- G (giga) = 10⁹
- m (milli) = 10⁻³
- μ (micro) = 10⁻⁶
- n (nano) = 10⁻⁹

### Error 4: Dimensional Inconsistency

**Symptom**: Calculated quantity doesn't match expected physics

**Problem**: Mixed units in formula

**Example (Bad)**:
```
c Volume of cylinder: r=250 cm, h=5 m (MIXED UNITS!)
V = π × r² × h = π × (250)² × 5 = 9.817×10⁵ cm³  $ WRONG!
```

**Fix (Good)**:
```
c Convert height to cm first
h = 5 m × 100 = 500 cm
V = π × (250)² × 500 = 9.817×10⁷ cm³  $ Correct
```

**Rule**: Always verify all terms in formula have consistent units

### Error 5: Activity vs. Source Intensity Confusion

**Symptom**: Source way too strong or weak

**Problem**: Using activity (Bq) directly as source weight without accounting for particles per decay

**Example (Bad)**:
```
c 1 Ci Co-60 source
Activity = 3.7×10¹⁰ Bq
SDEF WGT=3.7E10    $ WRONG! Doesn't account for 2 gammas per decay
```

**Fix (Good)**:
```
c 1 Ci Co-60 source
Activity = 3.7×10¹⁰ Bq (decays/s)
Gammas/s = 3.7×10¹⁰ × 2 = 7.4×10¹⁰  $ 2 gammas per decay
SDEF WGT=7.4E10 PAR=2
```

## Integration with Other Skills

### 1. **mcnp-material-builder**

Material builder uses unit converter for density conversions.

**Workflow**:
```
1. User provides: ρ = 11.34 g/cm³ (lead)
2. material-builder: Check units
3. unit-converter: Verify g/cm³ or convert if needed
4. material-builder: Use in M card with negative sign
   M1  82000.80c  -1.0    $ Lead
   10  1  -11.34  -100    $ Correct density
```

### 2. **mcnp-source-builder**

Source builder uses unit converter for energies and activities.

**Workflow**:
```
1. User provides: E = 662 keV (Cs-137 gamma)
2. source-builder: Recognize energy needs conversion
3. unit-converter: Convert 662 keV → 0.662 MeV
4. source-builder: Create SDEF
   SDEF  PAR=2  ERG=0.662
```

### 3. **mcnp-geometry-builder**

Geometry builder uses unit converter for dimensions.

**Workflow**:
```
1. User provides: Sphere radius 1.5 m
2. geometry-builder: Recognize non-MCNP units
3. unit-converter: Convert 1.5 m → 150 cm
4. geometry-builder: Create surface
   10  SO  150    $ Sphere radius 150 cm
```

### 4. **mcnp-physics-builder**

Physics builder uses unit converter for temperature and energy cutoffs.

**Workflow**:
```
1. User provides: T = 900°C, E_cut = 10⁻⁴ eV
2. physics-builder: Check units
3. unit-converter: 900°C → 1173.15 K → 1.011×10⁻⁷ MeV
                    10⁻⁴ eV → 10⁻¹⁰ MeV
4. physics-builder: Create cards
   TMP  1.011E-7
   CUT:N  1E-10  J
```

### 5. **mcnp-tally-builder**

Tally builder uses unit converter for energy bins.

**Workflow**:
```
1. User provides: Energy bins in keV: 0, 10, 100, 1000
2. tally-builder: Recognize needs conversion
3. unit-converter: Convert to MeV: 0, 0.01, 0.1, 1.0
4. tally-builder: Create energy bins
   F4:N  10
   E4  0  0.01  0.1  1.0
```

### 6. **mcnp-input-validator**

Validator uses unit converter to check dimensional consistency.

**Workflow**:
```
1. input-validator: Find M1 with density 7850 kg/m³
2. unit-converter: Convert to MCNP units: 7.85 g/cm³
3. input-validator: Verify cell uses -7.85 (correct sign)
4. Result: Pass or fail with suggestion
```

## Validation Checklist

Before completing unit conversions:

- [ ] Identified source and target units correctly
- [ ] Applied appropriate conversion factor
- [ ] Checked for prefix scaling (k, M, m, μ, etc.)
- [ ] Verified dimensional consistency across related parameters
- [ ] Confirmed result is physically reasonable:
  - [ ] Energies: thermal (~0.025 eV) to fast (~10 MeV) for neutrons
  - [ ] Densities: typical ranges for materials known
  - [ ] Lengths: reasonable for geometry scale
  - [ ] Temperatures: positive Kelvin, reasonable for materials
- [ ] Documented conversion in comments
- [ ] Used correct sign convention (positive/negative) for MCNP cards
- [ ] Verified significant figures appropriate for precision
- [ ] Cross-checked critical conversions with independent method

## Advanced Topics

### 1. Temperature-Dependent Density Corrections

**Thermal Expansion**:
```
ρ(T) = ρ₀ / (1 + β × ΔT)
where:
  ρ₀ = density at reference temperature
  β = volumetric thermal expansion coefficient
  ΔT = temperature difference from reference

Example: Aluminum
  ρ₀ = 2.70 g/cm³ at 20°C
  β = 7.5 × 10⁻⁵ K⁻¹
  T = 300°C (ΔT = 280 K)

  ρ(300°C) = 2.70 / (1 + 7.5×10⁻⁵ × 280)
  ρ(300°C) = 2.70 / 1.021 = 2.644 g/cm³
```

### 2. Relativistic Energy Conversions

**Relativistic Kinetic Energy**:
```
For particles at high energies:
KE = (γ - 1) × m₀c²
where:
  γ = 1 / sqrt(1 - v²/c²)
  m₀ = rest mass

Example: 2 MeV electron
  m₀c² = 0.511 MeV (electron rest mass energy)
  KE = 2 MeV
  Total E = KE + m₀c² = 2 + 0.511 = 2.511 MeV
  γ = E / (m₀c²) = 2.511 / 0.511 = 4.915
  v/c = sqrt(1 - 1/γ²) = 0.979
```

### 3. Doppler Broadening Temperature Effects

**Effective Temperature for Cross Sections**:
```
σ(E, T) depends on material temperature
MCNP uses temperature on TMP card or material suffix

Example: U-238 cross sections
  92238.80c  → 293.6 K (room temperature)
  92238.81c  → 600 K
  92238.82c  → 900 K

Use TMP card for intermediate temperatures:
  TMP  773.15    $ 500°C = 773 K
  M1  92238.80c  1.0  $ MCNP interpolates to 773 K
```

### 4. Number Density from Weight Fractions

**Converting Weight % to Atom Density**:
```
For compound with elements i:
N_i (atom/b-cm) = (w_i × ρ × N_A) / (A_i × 10²⁴)
where:
  w_i = weight fraction of element i
  ρ = total density (g/cm³)
  A_i = atomic mass of element i

Example: Water (H₂O) at 1.0 g/cm³
  H: w = 0.1119 (11.19%), A = 1.008
  O: w = 0.8881 (88.81%), A = 15.999

  N_H = (0.1119 × 1.0 × 6.022×10²³) / (1.008 × 10²⁴)
  N_H = 0.06685 atom/b-cm

  N_O = (0.8881 × 1.0 × 6.022×10²³) / (15.999 × 10²⁴)
  N_O = 0.03343 atom/b-cm

  Ratio: N_H / N_O = 0.06685 / 0.03343 = 2.00 ✓
```

### 5. Unit Conversion in Tally Results

**Flux to Dose Rate**:
```
Dose rate (mrem/hr) = Flux (n/cm²-s) × DCF
where DCF = dose conversion factor

Convert MCNP F4 tally (per source particle) to dose rate:
  Φ_MCNP = 1.234E-5 (per source particle)
  Source strength = 1E7 n/s
  Φ = 1.234E-5 × 1E7 = 1.234E2 n/cm²-s

  With DCF = 3.7E-6 (mrem-cm²)/neutron:
  Dose rate = 1.234E2 × 3.7E-6 × 3600
  Dose rate = 1.64 mrem/hr
```

### 6. Pressure-Density Relationships

**Ideal Gas Law**:
```
ρ = (P × M) / (R × T)
where:
  P = pressure (Pa)
  M = molar mass (g/mol)
  R = gas constant = 8.314 J/(mol·K)
  T = temperature (K)

Example: Air at 1 atm, 300 K
  P = 101325 Pa
  M = 28.97 g/mol (air)
  ρ = (101325 × 28.97) / (8.314 × 300)
  ρ = 1176.6 g/m³ = 0.001177 g/cm³
```

## Quick Reference: Common Conversions

| From | To | Factor | Example |
|------|-----|--------|---------|
| keV | MeV | ÷ 1000 | 1.5 keV = 0.0015 MeV |
| eV | MeV | ÷ 10⁶ | 0.025 eV = 2.5×10⁻⁸ MeV |
| J | MeV | × 6.242×10¹² | 1 J = 6.242×10¹² MeV |
| m | cm | × 100 | 2.5 m = 250 cm |
| mm | cm | ÷ 10 | 150 mm = 15 cm |
| inches | cm | × 2.54 | 6 in = 15.24 cm |
| kg/m³ | g/cm³ | ÷ 1000 | 7850 kg/m³ = 7.85 g/cm³ |
| K | MeV | × 8.617×10⁻¹¹ | 300 K = 2.585×10⁻⁸ MeV |
| °C | K | + 273.15 | 100°C = 373.15 K |
| Ci | Bq | × 3.7×10¹⁰ | 1 Ci = 3.7×10¹⁰ Bq |
| mCi | Bq | × 3.7×10⁷ | 10 mCi = 3.7×10⁸ Bq |
| μCi | Bq | × 3.7×10⁴ | 100 μCi = 3.7×10⁶ Bq |
| b | cm² | × 10⁻²⁴ | 5.8 b = 5.8×10⁻²⁴ cm² |
| mb | b | ÷ 1000 | 580 mb = 0.58 b |
| amu | g | × 1.6605×10⁻²⁴ | 235 amu = 3.902×10⁻²² g |
| amu | MeV/c² | × 931.494 | 1 amu = 931.494 MeV/c² |
| μs | shakes | × 100 | 5 μs = 500 shakes |
| ns | shakes | × 0.1 | 100 ns = 10 shakes |
| s | shakes | × 10⁸ | 1 s = 10⁸ shakes |
| deg | rad | × π/180 | 90° = π/2 rad |
| rad | deg | × 180/π | π rad = 180° |

## Best Practices

1. **Always Document Conversions**
   ```
   c Original: 2.5 m radius
   c Converted: 250 cm for MCNP
   10  SO  250
   ```

2. **Verify Physical Reasonableness**
   ```
   After conversion, check:
   - Is density in typical range for material?
   - Is energy reasonable for particle type?
   - Is temperature physically plausible?
   ```

3. **Use Consistent Units Throughout Input**
   ```
   If using cm for geometry:
   - All surfaces in cm
   - All volumes in cm³
   - All densities in g/cm³ or atom/b-cm
   ```

4. **Preserve Significant Figures**
   ```
   Input:  2.5 m (2 sig figs)
   Output: 250 cm or 2.5E2 cm (maintain 2 sig figs)
   Not:    250.0000 cm (false precision)
   ```

5. **Double-Check Critical Conversions**
   ```
   For safety-critical parameters:
   - Convert forward
   - Convert backward to verify
   - Compare with independent reference
   ```

6. **Use Negative Sign Convention Correctly**
   ```
   Mass density:   -7.85 g/cm³ (negative)
   Atomic density: +0.0602 atom/b-cm (positive)
   ```

7. **Account for Particle Multiplicity in Sources**
   ```
   Activity (decays/s) × particles per decay = particles/s
   Not just activity!
   ```

8. **Check Temperature Units on Specific Cards**
   ```
   TMP card: Accepts Kelvin or MeV
   Material suffix (e.g., .80c): Specifies library temperature
   ```

9. **Use Standard Prefixes Consistently**
   ```
   Prefer: 0.0025 MeV over 2.5 keV in input
   Maintain: MCNP standard units throughout
   ```

10. **Create Conversion Comment Blocks**
    ```
    c ========================================
    c UNIT CONVERSIONS
    c ========================================
    c Source energy: 14.1 keV = 0.0141 MeV
    c Tank radius: 2.5 m = 250 cm
    c Steel density: 7850 kg/m³ = 7.85 g/cm³
    c Temperature: 500°C = 773.15 K
    c ========================================
    ```

## References

- **Physical Constants**:
  - CODATA 2018 recommended values
  - NIST Reference on Constants, Units, and Uncertainty
- **Related Skills**:
  - mcnp-material-builder (uses density conversions)
  - mcnp-source-builder (uses energy and activity conversions)
  - mcnp-geometry-builder (uses length conversions)
  - mcnp-physics-builder (uses temperature conversions)
  - mcnp-tally-builder (uses energy bin conversions)
  - mcnp-physical-constants (provides fundamental constants)
- **User Manual**:
  - Chapter 2: General Input Format (unit conventions)
  - Chapter 3: Geometry Specification (length units)
  - Chapter 5.2: Material Cards (density conventions)
  - Chapter 5.4: Source Cards (energy units)
  - Chapter 5.7: Temperature Cards (TMP card units)

---

**End of MCNP Unit Converter Skill**
