---
category: A
name: mcnp-template-generator
description: Create reusable MCNP input templates for common problem types including shielding, criticality, dose calculations, and activation analysis
activation_keywords:
  - template
  - generate template
  - input template
  - starting point
  - example input
  - boilerplate
  - skeleton input
  - quick start
---

# MCNP Template Generator Skill

## Purpose

This skill guides users in creating, organizing, and using reusable MCNP input templates for common simulation types. Templates provide standardized starting points that accelerate input development, ensure best practices, reduce errors, and maintain consistency across projects. This skill covers template design, parameterization, common problem types, and template library organization.

## When to Use This Skill

- Starting a new MCNP project (need quick starting point)
- Repeating similar simulations (shielding studies, parameter scans)
- Training new users (provide standard examples)
- Ensuring consistency across team projects
- Documenting standard practices
- Creating input skeletons for common problems
- Building project-specific template libraries
- Rapid prototyping of new geometries
- Standardizing validation test cases

## Prerequisites

- **mcnp-input-builder**: Understanding of MCNP input structure
- **mcnp-geometry-builder**: Basic geometry creation
- **mcnp-material-builder**: Material definition knowledge
- **mcnp-source-builder**: Source specification
- **mcnp-tally-builder**: Tally definition
- Understanding of common simulation types (shielding, criticality, dose)

## Core Concepts

### Template Structure

**Complete Template** (All sections defined):
```
[Template Name]
c ==================================================
c TEMPLATE: [Problem Type]
c DESCRIPTION: [What this template does]
c PARAMETERS: [List of parameters to customize]
c AUTHOR: [Name]
c DATE: [Date]
c ==================================================
c
c INSTRUCTIONS:
c 1. Replace [PARAMETER] with actual value
c 2. Adjust geometry dimensions as needed
c 3. Update material compositions
c 4. Set appropriate NPS for statistics
c ==================================================

c Cell Cards
[... standard cell definitions with [PARAMETERS] ...]

c Surface Cards
[... standard surface definitions ...]

c Data Cards
[... standard data cards ...]
```

**Skeleton Template** (Structure only):
```
c ==================================================
c SKELETON INPUT - [Problem Type]
c ==================================================
c TODO: Define cells
c TODO: Define surfaces
c TODO: Define materials
c TODO: Define source
c TODO: Define tallies
c ==================================================

c Cell Cards
c [Add cell definitions here]

c Surface Cards
c [Add surface definitions here]

c Data Cards
MODE  N
c [Add remaining data cards]
```

### Parameterization Strategies

**Strategy 1: Comment Placeholders**
```
c PARAMETER: SHIELD_THICKNESS = [VALUE] cm
1  1  -11.3  -1  IMP:N=1        $ Shield cell, [SHIELD_THICKNESS] cm thick
```

**Strategy 2: Obvious Values** (easy to find/replace)
```
1  SO  999.99                    $ RADIUS: Change 999.99 to actual value
```

**Strategy 3: External Script** (Python, etc.)
```python
# generate_input.py
RADIUS = 10.0
THICKNESS = 5.0
template = open('template.i').read()
input_file = template.replace('[RADIUS]', str(RADIUS))
```

### Template Categories

**By Problem Type**:
- Shielding calculations
- Criticality (KCODE)
- Dose/activation
- Detector response
- Source characterization
- Transmission/reflection

**By Geometry Type**:
- Simple (sphere, box, cylinder)
- Multi-region (shells, layers)
- Lattice/array
- Complex (CAD-based, repeated structures)

**By Physics**:
- Neutron only
- Photon only
- Coupled neutron-photon
- Electron-photon
- Heavy ion

### Template Library Organization

**Directory Structure**:
```
templates/
├── shielding/
│   ├── simple_sphere.i
│   ├── multilayer_slab.i
│   └── point_kernel.i
├── criticality/
│   ├── bare_sphere.i
│   ├── reflected_sphere.i
│   └── pin_lattice.i
├── dose/
│   ├── ambient_dose.i
│   ├── effective_dose.i
│   └── organ_dose.i
├── activation/
│   ├── simple_activation.i
│   └── decay_photons.i
└── README.md
```

## Decision Tree: Selecting/Creating Templates

```
START: What type of simulation?
  |
  +--> Shielding Problem
  |      ├─> Simple geometry (sphere, slab)
  |      |    └─> Use: shielding/simple_sphere.i or multilayer_slab.i
  |      |
  |      ├─> Complex geometry (facility, room)
  |      |    └─> Use: shielding/complex_geometry.i (CAD-based)
  |      |
  |      └─> Deep penetration
  |           └─> Use: shielding/variance_reduced.i (with WWG)
  |
  +--> Criticality Problem
  |      ├─> Simple system (bare or reflected sphere)
  |      |    └─> Use: criticality/bare_sphere.i or reflected_sphere.i
  |      |
  |      ├─> Lattice (fuel assembly)
  |      |    └─> Use: criticality/pin_lattice.i
  |      |
  |      └─> Full core
  |           └─> Use: criticality/reactor_core.i
  |
  +--> Dose Calculation
  |      ├─> Ambient dose
  |      |    └─> Use: dose/ambient_dose.i (with DE/DF)
  |      |
  |      ├─> Effective dose
  |      |    └─> Use: dose/effective_dose.i (ICRP coefficients)
  |      |
  |      └─> Organ dose
  |           └─> Use: dose/organ_dose.i (phantom geometry)
  |
  +--> Activation Analysis
  |      ├─> Simple activation
  |      |    └─> Use: activation/simple_activation.i
  |      |
  |      └─> Decay photon source
  |           └─> Use: activation/decay_photons.i (two-stage)
  |
  +--> Detector Response
  |      ├─> Pulse height spectrum
  |      |    └─> Use: detector/pulse_height.i (F8 tally)
  |      |
  |      └─> Energy deposition
  |           └─> Use: detector/energy_deposition.i (F6 tally)
  |
  +--> Custom Problem (no template exists)
         ├─> Start from closest template
         ├─> Modify for new problem
         └─> Save as new template for future use
```

## Use Case 1: Simple Shielding Template (Sphere)

**Template File**: `templates/shielding/simple_sphere.i`

```
Simple Spherical Shielding Problem
c ==================================================
c TEMPLATE: Simple Shielding (Spherical Geometry)
c DESCRIPTION:
c   Point source at center, spherical shield,
c   dose at outer surface
c
c PARAMETERS TO CUSTOMIZE:
c   - SHIELD_RADIUS: Outer radius of shield (cm)
c   - SHIELD_MATERIAL: Material number
c   - SHIELD_DENSITY: Density (g/cm³)
c   - SOURCE_ENERGY: Source energy (MeV)
c   - SOURCE_STRENGTH: Particles per second
c ==================================================
c
c INSTRUCTIONS:
c 1. Search for [PARAMETER] and replace with values
c 2. Update material composition in M cards
c 3. Adjust NPS for desired statistics
c 4. Run and check dose rate at outer surface
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
1   1   -[SHIELD_DENSITY]   -1      IMP:N=1  IMP:P=1   $ Shield sphere
2   0                        1      IMP:N=0  IMP:P=0   $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
1   SO   [SHIELD_RADIUS]                              $ Outer boundary

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N P                                             $ Coupled neutron-photon
c
c --- Materials ---
c [Replace with actual shield material]
M1   82000  1.0                                       $ Lead (example)
c    OR: 26000 1.0 (iron)
c    OR: 6000 1.0 8016 1.0 (concrete - simplified)
c
c --- Source ---
SDEF  POS=0 0 0  ERG=[SOURCE_ENERGY]  PAR=1          $ Point source (photon)
c     For neutron: PAR=1 → PAR=1 (n) or omit for default
c
c --- Tallies ---
F2:P  1                                               $ Surface flux
FC2   Photon flux at shield outer surface
c
c --- Dose Conversion ---
DE2   0.01  0.1  1  10  20                           $ Energy bins (MeV)
DF2   1e-12 5e-12 1e-11 2e-11 3e-11                  $ Dose coefficients (Sv·cm²)
c     [Update with actual ICRP-74 AP coefficients]
c
c --- Run Control ---
NPS   1e6                                             $ 1 million particles

c ==================================================
c EXPECTED RESULTS:
c - F2 tally: dose rate at surface (Sv/source particle)
c - Multiply by source strength for total dose rate
c ==================================================
```

**Usage**:
```bash
# Copy template
cp templates/shielding/simple_sphere.i my_problem.i

# Edit parameters
# Replace [SHIELD_RADIUS] with 50
# Replace [SHIELD_DENSITY] with 11.3 (lead)
# Replace [SOURCE_ENERGY] with 1.0 (MeV)

# Run
mcnp6 inp=my_problem.i outp=output.o
```

## Use Case 2: Criticality Template (Bare Sphere)

**Template File**: `templates/criticality/bare_sphere.i`

```
Bare Sphere Criticality Benchmark
c ==================================================
c TEMPLATE: Bare Sphere Criticality
c DESCRIPTION:
c   Simple bare fissile sphere for keff calculation
c   Useful for benchmarking, validation, training
c
c PARAMETERS TO CUSTOMIZE:
c   - FUEL_RADIUS: Radius of fissile sphere (cm)
c   - FUEL_DENSITY: Atomic density (atoms/b-cm)
c   - ENRICHMENT: U-235 fraction (atomic)
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
1   1   -[FUEL_DENSITY]   -1      IMP:N=1             $ Fuel sphere
2   0                      1      IMP:N=0             $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
1   SO   [FUEL_RADIUS]                                $ Fuel outer radius

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N
c
c --- Materials ---
c Uranium (HEU example)
M1   92235.80c  [ENRICHMENT]  &                       $ U-235
     92238.80c  [1-ENRICHMENT]                        $ U-238
c    Example: 0.93 enrichment = 93% U-235
c
c --- Criticality Source ---
KCODE  10000  1.0  50  150                            $ 10k/cyc, skip 50, 100 active
KSRC   0 0 0                                          $ Initial source at center
c
c --- Tallies (optional) ---
c F4:N  1                                             $ Flux in fuel
c FC4   Flux in fuel sphere
c
c --- Run Control ---
c (KCODE replaces NPS)

c ==================================================
c EXPECTED RESULTS:
c - keff and uncertainty
c - Shannon entropy (check convergence)
c - keff should be ~1.0 for critical sphere
c ==================================================
```

## Use Case 3: Dose Calculation Template (Effective Dose)

**Template File**: `templates/dose/effective_dose.i`

```
Effective Dose Calculation
c ==================================================
c TEMPLATE: Effective Dose (ICRP-74 AP)
c DESCRIPTION:
c   Calculate effective dose using ICRP-74
c   anteroposterior (AP) dose coefficients
c
c PARAMETERS TO CUSTOMIZE:
c   - Geometry (cells, surfaces)
c   - Source definition
c   - Detector locations (F5 tallies)
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
c [Define geometry here]
c Example: simple source-shield-detector
1   1   -2.3   -1      IMP:N=1  IMP:P=1              $ Shield (concrete)
2   0          1       IMP:N=0  IMP:P=0              $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
1   SO   100                                          $ Outer boundary

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N P                                             $ Coupled transport
c
c --- Materials ---
M1   1001  -0.01  6000  -0.001  8016  -0.53  &       $ Concrete (simplified)
     11023 -0.016 12000 -0.002  13027 -0.034  &
     14000 -0.337 20000 -0.044  26000 -0.014
c
c --- Source ---
SDEF  POS=0 0 0  ERG=1.0  PAR=2                      $ 1 MeV photon source
c
c --- Tallies ---
F5:P   50 0 0  0.5                                    $ Detector at 50 cm
FC5    Effective dose at 50 cm
c
c --- Dose Conversion (ICRP-74 AP, photons) ---
DE5    0.01  0.015  0.02  0.03  0.04  0.05  0.06  0.08  0.1  &
       0.15  0.2  0.3  0.4  0.5  0.6  0.8  1.0  &
       1.5  2.0  3.0  4.0  5.0  6.0  8.0  10.0
DF5    0.0485 0.1254 0.2325 0.4374 0.6273 0.7768 0.8951 1.0890 1.2260 &
       1.4702 1.6245 1.8498 1.9836 2.0769 2.1468 2.2431 2.3159 &
       2.4336 2.5183 2.6375 2.7248 2.7947 2.8546 2.9503 3.0317
c    Units: pSv·cm² (multiply by 1e-10 for Sv·cm²)
c
c --- Run Control ---
NPS    1e7                                            $ 10 million particles

c ==================================================
c EXPECTED RESULTS:
c - F5 tally: effective dose per source particle (Sv)
c - Multiply by source strength (part/s) for dose rate (Sv/s)
c ==================================================
```

## Use Case 4: Multi-Layer Slab Template

**Template File**: `templates/shielding/multilayer_slab.i`

```
Multi-Layer Slab Shielding
c ==================================================
c TEMPLATE: Multi-Layer Slab (1D Geometry)
c DESCRIPTION:
c   Plane source → Layer 1 → Layer 2 → Layer 3 → Detector
c   Useful for shielding optimization studies
c
c PARAMETERS:
c   - LAYER1_THICK: Thickness of layer 1 (cm)
c   - LAYER2_THICK: Thickness of layer 2 (cm)
c   - LAYER3_THICK: Thickness of layer 3 (cm)
c   - Materials: M1, M2, M3
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
1   1   -[DENS1]   -1         IMP:N=1  IMP:P=1       $ Layer 1
2   2   -[DENS2]    1  -2     IMP:N=1  IMP:P=1       $ Layer 2
3   3   -[DENS3]    2  -3     IMP:N=1  IMP:P=1       $ Layer 3
4   0               3  -4     IMP:N=1  IMP:P=1       $ Air gap / detector
999 0               4         IMP:N=0  IMP:P=0       $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
c Planes perpendicular to z-axis
1   PZ   [LAYER1_THICK]                              $ Layer 1 boundary
2   PZ   [LAYER1_THICK + LAYER2_THICK]               $ Layer 2 boundary
3   PZ   [LAYER1_THICK + LAYER2_THICK + LAYER3_THICK]  $ Layer 3 boundary
4   PZ   [LAYER1_THICK + LAYER2_THICK + LAYER3_THICK + 100]  $ Far boundary

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N P
c
c --- Materials ---
M1   [Material 1 definition]
M2   [Material 2 definition]
M3   [Material 3 definition]
c
c --- Source (Plane source at z=0) ---
SDEF  SUR=0  POS=0 0 0  AXS=0 0 1  EXT=0  RAD=D1  ERG=[ENERGY]  PAR=2
SI1  0  100                                          $ Radial extent (0-100 cm)
SP1  -21  1                                          $ r² weighting (uniform area)
c
c --- Tallies ---
F2:P  3                                              $ Flux at layer 3 exit surface
FC2   Transmitted flux after 3 layers
c
c --- Run Control ---
NPS   1e7

c ==================================================
c EXPECTED RESULTS:
c - F2 tally: transmission coefficient
c ==================================================
```

## Use Case 5: Lattice Template (Pin Array)

**Template File**: `templates/criticality/pin_lattice.i`

```
Fuel Pin Lattice
c ==================================================
c TEMPLATE: Rectangular Fuel Pin Lattice
c DESCRIPTION:
c   NxN array of fuel pins in water
c   Universe-based lattice structure
c
c PARAMETERS:
c   - PIN_RADIUS: Fuel pin radius (cm)
c   - CLAD_RADIUS: Cladding outer radius (cm)
c   - PIN_PITCH: Pin-to-pin spacing (cm)
c   - ARRAY_SIZE: Number of pins per side (N×N)
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
c --- Pin Universe (U=1) ---
1   1   -10.5   -1      U=1  IMP:N=1                 $ Fuel (UO2)
2   2   -6.5     1  -2  U=1  IMP:N=1                 $ Cladding (Zircaloy)
3   3   -1.0     2      U=1  IMP:N=1                 $ Coolant (water)

c --- Lattice Element ---
10  0   -10  LAT=1  U=2  FILL=-[N]:[ N]  -[N]:[N]  0:0  &
                          [Array of universe IDs]   IMP:N=1

c --- Main Geometry ---
100  0   -100  FILL=2  IMP:N=1                       $ Fill with lattice universe
999  0    100  IMP:N=0                               $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
c --- Pin Surfaces ---
1    C/Z  0 0  [PIN_RADIUS]                          $ Fuel radius
2    C/Z  0 0  [CLAD_RADIUS]                         $ Clad outer radius

c --- Lattice Surfaces ---
10   RPP  -[PITCH/2]  [PITCH/2]  &                   $ Pin cell boundary
         -[PITCH/2]  [PITCH/2]  &
         -50  50

c --- Assembly Surfaces ---
100  RPP  -[N*PITCH/2]  [N*PITCH/2]  &               $ Assembly boundary
         -[N*PITCH/2]  [N*PITCH/2]  &
         -50  50

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N
c
c --- Materials ---
M1   92235.80c  -0.03  92238.80c  -0.97  8016.80c  -0.12  $ UO2 (simplified)
M2   40000.80c  1.0                                        $ Zircaloy
M3   1001.80c  2  8016.80c  1                             $ Water
MT3  LWTR.20T                                              $ H in H2O thermal
c
c --- Criticality Source ---
KCODE  10000  1.0  50  150
KSRC   0 0 0  [PITCH] 0 0  0 [PITCH] 0               $ Multiple start points
c
c --- Run Control ---
c (KCODE replaces NPS)

c ==================================================
c EXPECTED RESULTS:
c - keff (typically <1.0 for small arrays, >1.0 for large)
c - Shannon entropy convergence
c ==================================================
```

## Use Case 6: Activation Template

**Template File**: `templates/activation/simple_activation.i`

```
Neutron Activation Analysis
c ==================================================
c TEMPLATE: Simple Activation
c DESCRIPTION:
c   Calculate neutron-induced activation
c   Uses FM card with activation reactions
c
c PARAMETERS:
c   - Sample geometry
c   - Neutron source spectrum
c   - Activation reactions of interest
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
1   1   -[SAMPLE_DENSITY]   -1      IMP:N=1         $ Sample
2   0                        1      IMP:N=0         $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
1   RPP  -5 5  -5 5  -5 5                            $ Sample box

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N
c
c --- Materials ---
M1   [SAMPLE_MATERIAL]                               $ Define sample composition
c    Example: 27059.80c 1.0 (Co-59 for Co-60 production)
c
c --- Source ---
SDEF  CEL=1  ERG=D1                                  $ Volume source in sample
SI1  H  0  0.1  1  10  14                            $ Energy spectrum
SP1    0  1    1  0                                  $ Histogram
c
c --- Tallies ---
F4:N  1                                              $ Flux in sample
FM4   -1.0  1  102                                   $ (n,γ) reaction rate
c     ^normalize by mass
FC4   (n,gamma) reaction rate in sample
c
c --- Run Control ---
NPS   1e7

c ==================================================
c POST-PROCESSING:
c - Tally result = reactions per source neutron per gram
c - Multiply by:
c   * Source strength (n/s)
c   * Sample mass (g)
c   * Irradiation time (s)
c - Result: Total reactions (decays)
c - Apply decay correction for activity at t>0
c ==================================================
```

## Use Case 7: Pulse Height Spectrum Template

**Template File**: `templates/detector/pulse_height.i`

```
Pulse Height Spectrum (F8 Tally)
c ==================================================
c TEMPLATE: Detector Pulse Height Spectrum
c DESCRIPTION:
c   Calculate energy deposition spectrum in detector
c   Uses F8 tally (energy distribution)
c
c PARAMETERS:
c   - Detector geometry
c   - Detector material
c   - Source definition
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
1   0                -1      IMP:N=1  IMP:P=1       $ Void (source region)
2   1   -[DET_DENS]   1  -2  IMP:N=1  IMP:P=1       $ Detector
999 0                 2      IMP:N=0  IMP:P=0       $ Graveyard

c ==================================================
c SURFACE CARDS
c ==================================================
1   SO   10                                          $ Source sphere
2   SO   20                                          $ Outer boundary

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N P                                            $ Coupled (if needed)
c    OR: MODE P (photon only)
c
c --- Materials ---
M1   [DETECTOR_MATERIAL]                             $ NaI, HPGe, etc.
c    Example NaI(Tl):
c    M1  11023.80c  0.5  53127.80c  0.5
c
c --- Source ---
SDEF  POS=0 0 0  ERG=[SOURCE_ENERGY]  PAR=2         $ Photon point source
c
c --- Tallies ---
F8:P  2                                              $ Pulse height in detector
E8    0  0.01  0.02  0.03  ... [MAX_ENERGY]  & $ Energy bins (MeV)
      [Fine binning for spectrum resolution]
FC8   Pulse height spectrum
c
c --- Run Control ---
NPS   1e8                                            $ High stats for spectrum

c ==================================================
c EXPECTED RESULTS:
c - F8 tally: counts vs deposited energy
c - Should see photopeak, Compton edge, backscatter
c ==================================================
```

## Use Case 8: Variance Reduction Template

**Template File**: `templates/shielding/variance_reduced.i`

```
Deep Penetration with Weight Windows
c ==================================================
c TEMPLATE: Shielding with Automatic Variance Reduction
c DESCRIPTION:
c   Two-stage calculation:
c   Stage 1: Generate weight windows (WWG)
c   Stage 2: Production run with weight windows
c
c THIS FILE: Stage 1 (WWG generation)
c ==================================================

c ==================================================
c CELL CARDS
c ==================================================
[... geometry definition ...]

c ==================================================
c SURFACE CARDS
c ==================================================
[... surface definition ...]

c ==================================================
c DATA CARDS
c ==================================================
c
c --- Physics ---
MODE  N P
c
c --- Materials ---
[... material definitions ...]
c
c --- Importance Mesh for WWG ---
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=[X0] [Y0] [Z0]
      IMESH=[X1]  IINTS=[NX]
      JMESH=[Y1]  JINTS=[NY]
      KMESH=[Z1]  KINTS=[NZ]
c
c --- Energy Bins for Weight Windows ---
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c --- Source ---
SDEF  [... source definition ...]
c
c --- Detector Tally (for WWG) ---
F5:N  [DETECTOR_LOCATION]  0.5
FC5   Detector for weight window generation
c
c --- Generate Weight Windows ---
WWG  5  0  1.0                                       $ From F5, target=1.0
c
c --- Run Control (moderate stats for WWG) ---
NPS   1e5                                            $ Quick WWG run

c ==================================================
c NEXT STEPS:
c 1. Run this input → generates wwout file
c 2. Copy to production input, modify:
c    - Remove WWG card
c    - Add: WWP:N J J J 0 -1 (read wwout)
c    - Increase NPS to 1e7+ for production
c 3. Run production → high FOM, good statistics
c ==================================================
```

## Common Errors and Troubleshooting

### Error 1: Forgot to Replace Parameter Placeholders

**Symptom**: Fatal error "surface 999.99 not found" or similar

**Cause**: Template placeholder not replaced with actual value

**Example (Bad)**:
```
1  SO  [RADIUS]                     $ Forgot to replace [RADIUS]
```

**Fix**:
```
1  SO  50.0                         $ Replaced with actual value
```

**Prevention**: Search for `[` before running to find unreplaced placeholders

### Error 2: Inconsistent Parameter Updates

**Symptom**: Geometry errors, overlapping cells

**Cause**: Updated one parameter but not related parameters

**Example (Bad)**:
```
c Updated shield radius:
1  SO  100                          $ Changed from 50 to 100

c But forgot to update detector location:
F5:N  75 0 0  0.5                   $ Still at 75 (now inside shield!)
```

**Fix**:
```
1  SO  100
F5:N  110 0 0  0.5                  $ Moved outside shield
```

### Error 3: Copied Template with Wrong Physics Mode

**Symptom**: Photon tallies in neutron-only simulation (no results)

**Cause**: Template designed for coupled transport, but MODE changed

**Example (Bad)**:
```
MODE  N                             $ Changed to neutron only
...
F5:P  100 0 0  0.5                  $ Photon tally (no photons!)
```

**Fix**:
```
MODE  N P                           $ Keep coupled transport
(OR)
F5:N  100 0 0  0.5                  $ Change tally to neutron
```

### Error 4: Template Material Definitions Incomplete

**Symptom**: Fatal error "material X not defined"

**Cause**: Template has placeholder M card, not filled in

**Fix**:
```
c Template had:
c M1  [DEFINE MATERIAL HERE]

c Must replace with:
M1  82000  1.0                      $ Lead (actual definition)
```

## Integration with Other Skills

### 1. **mcnp-input-builder**

Template-generator creates starting points, input-builder finishes customization.

**Workflow**:
```
1. template-generator: Select appropriate template
2. Copy template to working file
3. input-builder: Customize geometry, materials, source
4. Validate and run
```

### 2. **mcnp-geometry-builder**

Templates provide geometry skeletons, geometry-builder adds complexity.

**Example**:
```
1. template-generator: Start with simple_sphere.i
2. geometry-builder: Add inner fuel region (2-region sphere)
3. geometry-builder: Add lattice structure if needed
```

### 3. **mcnp-material-builder**

Templates often have placeholder materials, material-builder defines them.

**Pattern**:
```
c Template has:
M1  [SHIELD_MATERIAL]

c material-builder provides:
M1  82000  1.0  $ Lead
(OR)
M1  26000  0.7  28000  0.2  24000  0.1  $ Stainless steel
```

### 4. **mcnp-tally-builder**

Templates include basic tallies, tally-builder enhances them.

**Example**:
```
c Template has:
F4:N  1

c tally-builder adds:
F4:N  1
E4    0.01  0.1  1  10  14          $ Energy bins
FM4   -1  1  -6                     $ Heating (MeV/g)
```

### 5. **mcnp-input-validator**

Always validate after customizing template.

**Workflow**:
```
1. template-generator: Copy template
2. Customize parameters
3. input-validator: Check correctness
4. Fix issues
5. Run simulation
```

## Validation Checklist

Before using customized template:

- [ ] All `[PARAMETER]` placeholders replaced
- [ ] Geometry consistent (radii, thicknesses)
- [ ] Materials defined (not placeholders)
- [ ] Source definition complete
- [ ] Tallies match physics mode (N, P, or both)
- [ ] Importance (IMP) defined for all cells
- [ ] Graveyard cell has IMP=0
- [ ] NPS appropriate for problem (1e6 typical start)
- [ ] Comments updated (remove template instructions if not needed)
- [ ] Input runs without fatal errors
- [ ] Results make physical sense (quick check)

## Advanced Topics

### 1. Parameterized Template Scripts

**Python Example**:
```python
def generate_input(radius, density, energy, output_file):
    """Generate MCNP input from template"""
    template = '''Simple Sphere
c Cell Cards
1   1   -{density:.2f}   -1      IMP:N=1
2   0                     1      IMP:N=0

c Surface Cards
1   SO  {radius:.2f}

c Data Cards
MODE  N
M1  82000  1.0
SDEF  POS=0 0 0  ERG={energy:.2f}
F4:N  1
NPS  1e6
'''
    with open(output_file, 'w') as f:
        f.write(template.format(
            radius=radius,
            density=density,
            energy=energy
        ))

# Usage
generate_input(radius=50, density=11.3, energy=1.0,
               output_file='lead_sphere.i')
```

### 2. Template Inheritance

**Concept**: Build complex templates from simpler ones

**Example**:
```
base_template.i              → Basic structure
  ↓
shielding_base.i             → Add shielding-specific cards
  ↓
multilayer_shielding.i       → Add multiple layers
  ↓
optimized_shielding.i        → Add variance reduction
```

### 3. Template Documentation

**Best Practice**: Comprehensive README for template library

**README.md Example**:
```markdown
# MCNP Template Library

## Directory Structure
- `shielding/`: Shielding calculations
- `criticality/`: Criticality problems
- `dose/`: Dose calculations

## Usage
1. Copy template to working directory
2. Search for [PARAMETER] and replace
3. Validate with mcnp-input-validator
4. Run

## Template List
### shielding/simple_sphere.i
- **Description**: Point source, spherical shield
- **Parameters**: RADIUS, DENSITY, ENERGY
- **Use Cases**: Quick dose estimates, benchmarking

[... more templates ...]
```

### 4. Version Control for Templates

**Best Practice**: Git repository for template library

```bash
templates/
├── .git/
├── README.md
├── CHANGELOG.md
├── shielding/
│   └── ...
└── criticality/
    └── ...

# Track changes
git add templates/shielding/simple_sphere.i
git commit -m "Add DBRC to fuel materials"
git tag v2.0
```

## Quick Reference: Template Selection Guide

| Problem Type | Template File | Key Features |
|--------------|---------------|--------------|
| Simple shielding | `shielding/simple_sphere.i` | Point source, single shield, dose tally |
| Multi-layer shield | `shielding/multilayer_slab.i` | Plane source, 3 layers, transmission |
| Deep penetration | `shielding/variance_reduced.i` | WWG variance reduction, 2-stage |
| Bare criticality | `criticality/bare_sphere.i` | KCODE, simple fissile sphere |
| Reflected critical | `criticality/reflected_sphere.i` | KCODE, fuel + reflector |
| Lattice criticality | `criticality/pin_lattice.i` | Universe-based lattice, KCODE |
| Effective dose | `dose/effective_dose.i` | ICRP-74 coefficients, F5 tally |
| Activation | `activation/simple_activation.i` | Reaction rates, FM card |
| Pulse height | `detector/pulse_height.i` | F8 tally, energy spectrum |

## Best Practices

1. **Start Simple**: Use simplest template that fits problem
   ```
   Simple → Customize → Validate → Run
   ```

2. **Document Customizations**: Track changes from template
   ```
   c CUSTOMIZATIONS FROM TEMPLATE:
   c - Changed radius from 50 to 75 cm
   c - Updated material from Pb to Fe
   c - Added energy bins to tally
   ```

3. **Validate Before Running**: Check template customization
   ```bash
   # Quick syntax check
   mcnp6 inp=custom.i TASKS 1 &
   # Check for warnings, fix before production run
   ```

4. **Build Template Library**: Save good inputs as templates
   ```
   # After successful simulation:
   cp validated_input.i templates/new_template.i
   # Add [PARAMETER] placeholders
   # Add documentation comments
   ```

5. **Use Meaningful Names**: Template files should be descriptive
   ```
   Good: shielding_sphere_dose.i
   Bad:  template1.i
   ```

6. **Include Expected Results**: Help users verify correctness
   ```
   c EXPECTED RESULTS:
   c - keff ~1.0 ± 0.001 (critical)
   c - Dose rate ~1 mSv/hr at 1m
   ```

7. **Version Templates**: Track improvements over time
   ```
   simple_sphere_v1.i  → Basic version
   simple_sphere_v2.i  → Added DBRC
   simple_sphere_v3.i  → Added variance reduction
   ```

8. **Test Templates Periodically**: Ensure compatibility with new MCNP versions
   ```bash
   # Regression test
   for template in templates/*/*.i; do
       mcnp6 inp=$template outp=test.o
   done
   ```

9. **Share Templates**: Team standardization improves consistency
   ```
   # Central repository
   /shared/mcnp_templates/
   # Everyone uses same validated templates
   ```

10. **Keep Templates Simple**: Complexity defeats the purpose
    ```
    Template should be 80% ready to run
    User customizes remaining 20%
    ```

11. **Programmatic Template Generation**:
    - For automated template creation and customization, see: `mcnp_template_generator.py`
    - Useful for batch template generation, parameter substitution, and workflow automation

## References

- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md` (All sections)
- **Related Skills**:
  - mcnp-input-builder (complete input creation)
  - mcnp-geometry-builder (geometry customization)
  - mcnp-material-builder (material definitions)
  - mcnp-source-builder (source customization)
  - mcnp-tally-builder (tally enhancement)
  - mcnp-input-validator (template validation)
- **User Manual**:
  - Chapter 10: Examples (template inspiration)
  - Appendix A: Sample Problems
- **Template Repository**: `templates/` (project-specific)

---

**End of MCNP Template Generator Skill**
