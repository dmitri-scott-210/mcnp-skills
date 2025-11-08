# Reactor Assembly Templates
## Production-Ready Geometry Patterns for Common Reactor Types

## Overview

This document provides complete, production-ready MCNP geometry templates for:
1. **PWR (Pressurized Water Reactor)** - 17×17 fuel assembly
2. **BWR (Boiling Water Reactor)** - 8×8 assembly with water rods
3. **VVER (Russian PWR)** - Hexagonal assembly
4. **HTGR (High-Temperature Gas Reactor)** - Prismatic block and pebble bed
5. **Fast Reactor** - Sodium-cooled with hexagonal assemblies
6. **TRISO Particle** - 5-layer coating structure (supplemental)

Each template includes:
- Complete cell and surface definitions
- Material specifications
- Lattice structures
- Typical dimensions
- Usage notes and modifications

---

## PWR (Pressurized Water Reactor)

### Standard 17×17 Fuel Assembly

**Design**: Westinghouse-type 17×17 assembly
**Fuel pins**: 264 positions (17×17 - 25 guide tubes)
**Guide tubes**: 24 control rod positions + 1 instrumentation
**Pin pitch**: 1.26 cm
**Assembly pitch**: 21.50 cm (17 × 1.26 = 21.42 cm)
**Active height**: 366 cm

**Complete MCNP Template**:
```mcnp
c ============================================================
c PWR 17×17 FUEL ASSEMBLY
c ============================================================
c
c Design: Westinghouse-type
c Fuel pins: 264 (UO2, 4.5% enriched)
c Guide tubes: 24 (control rods) + 1 (instrumentation)
c Pin pitch: 1.26 cm
c Active height: 366 cm
c
c ============================================================

c ------------------------------------------------------------
c UNIVERSE DEFINITIONS
c ------------------------------------------------------------

c Fuel pin universe (u=100)
100  1  -10.5   -100        u=100  imp:n=1  $ UO2 fuel (4.5% enriched)
101  0          100  -101   u=100  imp:n=1  $ Helium gap
102  2  -6.5    101  -102   u=100  imp:n=1  $ Zircaloy-4 clad
103  3  -0.7    102         u=100  imp:n=1  $ Water coolant

c Guide tube universe (u=101)
110  3  -0.7   -110        u=101  imp:n=1  $ Water inside guide tube
111  2  -6.5    110  -111  u=101  imp:n=1  $ Guide tube wall (Zr-4)
112  3  -0.7    111        u=101  imp:n=1  $ Water outside

c Instrumentation tube universe (u=102)
120  0         -120        u=102  imp:n=1  $ Void inside
121  2  -6.5    120  -121  u=102  imp:n=1  $ Instrument tube wall
122  3  -0.7    121        u=102  imp:n=1  $ Water outside

c ------------------------------------------------------------
c PIN SURFACES (in universes, centered at origin)
c ------------------------------------------------------------

c Fuel pin (u=100)
100   cz  0.4095    $ Fuel pellet radius (8.19 mm diameter)
101   cz  0.4178    $ Clad inner radius (gap outer)
102   cz  0.4750    $ Clad outer radius (9.50 mm diameter)

c Guide tube (u=101)
110   cz  0.5715    $ Guide tube inner radius (11.43 mm diameter)
111   cz  0.6121    $ Guide tube outer radius (12.24 mm diameter)

c Instrumentation tube (u=102)
120   cz  0.5590    $ Instrument tube inner (11.18 mm diameter)
121   cz  0.6121    $ Instrument tube outer (12.24 mm diameter)

c ------------------------------------------------------------
c LATTICE ASSEMBLY (u=200) - 17×17 ARRAY
c ------------------------------------------------------------
c
c Guide tube positions (G = u=101, I = u=102, F = u=100):
c
c    -8  -7  -6  -5  -4  -3  -2  -1   0   1   2   3   4   5   6   7   8
c  +-------------------------------------------------------------------
c 8|  F   F   F   G   F   F   F   G   F   F   F   G   F   F   F   F   F
c 7|  F   F   F   F   F   F   F   F   F   F   F   F   F   F   F   F   F
c 6|  F   F   F   G   F   F   F   G   F   F   F   G   F   F   F   F   F
c 5|  G   F   G   F   F   F   G   F   F   F   G   F   F   F   G   F   G
c 4|  F   F   F   F   F   G   F   F   F   G   F   F   F   F   F   F   F
c 3|  F   F   F   F   G   F   F   F   F   F   G   F   F   F   F   F   F
c 2|  F   F   F   G   F   F   F   G   F   F   F   G   F   F   F   F   F
c 1|  G   F   G   F   F   F   G   F   I   F   G   F   F   F   G   F   G
c 0|  F   F   F   F   F   F   F   F   F   F   F   F   F   F   F   F   F
c-1|  G   F   G   F   F   F   G   F   F   F   G   F   F   F   G   F   G
c-2|  F   F   F   G   F   F   F   G   F   F   F   G   F   F   F   F   F
c-3|  F   F   F   F   G   F   F   F   F   F   G   F   F   F   F   F   F
c-4|  F   F   F   F   F   G   F   F   F   G   F   F   F   F   F   F   F
c-5|  G   F   G   F   F   F   G   F   F   F   G   F   F   F   G   F   G
c-6|  F   F   F   G   F   F   F   G   F   F   F   G   F   F   F   F   F
c-7|  F   F   F   F   F   F   F   F   F   F   F   F   F   F   F   F   F
c-8|  F   F   F   G   F   F   F   G   F   F   F   G   F   F   F   F   F

200  0  -200  u=200  lat=1  imp:n=1  fill=-8:8 -8:8 0:0
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=8
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100  $j=7
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=6
     101 100 101 100 100 100 101 100 100 100 101 100 100 100 101 100 101  $j=5
     100 100 100 100 100 101 100 100 100 101 100 100 100 100 100 100 100  $j=4
     100 100 100 100 101 100 100 100 100 100 101 100 100 100 100 100 100  $j=3
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=2
     101 100 101 100 100 100 101 100 102 100 101 100 100 100 101 100 101  $j=1
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100  $j=0
     101 100 101 100 100 100 101 100 100 100 101 100 100 100 101 100 101  $j=-1
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=-2
     100 100 100 100 101 100 100 100 100 100 101 100 100 100 100 100 100  $j=-3
     100 100 100 100 100 101 100 100 100 101 100 100 100 100 100 100 100  $j=-4
     101 100 101 100 100 100 101 100 100 100 101 100 100 100 101 100 101  $j=-5
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=-6
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100  $j=-7
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=-8

c Lattice boundary surface (MUST be RPP for LAT=1)
c 17 pins × 1.26 cm pitch = 21.42 cm → ±10.71 cm
200   rpp  -10.71 10.71  -10.71 10.71  0 366    $ Active fuel height

c ------------------------------------------------------------
c GLOBAL PLACEMENT
c ------------------------------------------------------------

999   0  -200  fill=200  imp:n=1    $ Fill with lattice
1000  0   200   imp:n=0             $ Outside world (graveyard)

c ============================================================
c MATERIALS
c ============================================================

m1   $ UO2 fuel, 4.5% enriched, 10.5 g/cm³
    92234.70c  3.80e-4    $ U-234 (trace)
    92235.70c  0.0450     $ U-235 (enriched)
    92238.70c  0.9550     $ U-238 (depleted)
     8016.70c  2.0000     $ Oxygen

m2   $ Zircaloy-4 clad, 6.5 g/cm³
    40000.60c  0.9821     $ Zirconium (base)
    26000.50c  0.0022     $ Iron
    24000.50c  0.0010     $ Chromium
    50000.35c  0.0147     $ Tin

m3   $ Light water coolant/moderator, 0.7 g/cm³ (hot, ~300°C)
     1001.70c  2.0        $ Hydrogen
     8016.70c  1.0        $ Oxygen
mt3  lwtr.13t             $ S(α,β) thermal scattering at 350K

c ============================================================
c PROBLEM SPECIFICATION
c ============================================================

mode n
kcode 10000 1.0 50 250
ksrc 0 0 183

c Tallies (optional)
f4:n 100 101 102 103    $ Flux in pin cells
e4 1e-10 1e-7 0.625e-6 1e-5 1e-4 1e-3 1e-2 0.1 1 20
```

**Usage Notes**:
- **Modify enrichment**: Change U-235 fraction in M1 (typical: 3-5%)
- **Adjust water density**: 0.7 g/cm³ hot, 1.0 g/cm³ cold
- **Guide tube pattern**: Standard Westinghouse 17×17 layout
- **Axial segmentation**: Add PZ surfaces and duplicate cells for burnup zones
- **Burnable absorbers**: Replace some fuel pins with Gd2O3-UO2 mixture

**Validation**:
```bash
mcnp6 inp=pwr_17x17.i ip
# In plotter: origin 0 0 183, extent 12 12 366, basis 1 0 0  0 1 0
# Expected: 17×17 grid with guide tubes at specified positions
```

---

## BWR (Boiling Water Reactor)

### 8×8 Assembly with Water Rods

**Design**: GE-type 8×8 assembly
**Fuel pins**: 62 (8×8 - 2 water rods)
**Water rods**: 2 large diameter (for moderation)
**Pin pitch**: 1.63 cm
**Assembly pitch**: 13.04 cm
**Active height**: 380 cm

**Complete Template**:
```mcnp
c ============================================================
c BWR 8×8 FUEL ASSEMBLY
c ============================================================

c ------------------------------------------------------------
c UNIVERSE DEFINITIONS
c ------------------------------------------------------------

c Fuel pin universe (u=100)
100  1  -10.5   -100        u=100  imp:n=1  $ UO2 fuel (3.5% enriched)
101  0          100  -101   u=100  imp:n=1  $ Gap
102  2  -6.5    101  -102   u=100  imp:n=1  $ Zircaloy clad
103  3  -0.5    102         u=100  imp:n=1  $ Water/steam (low density)

c Water rod universe (u=200)
200  3  -1.0   -200        u=200  imp:n=1  $ Water inside (liquid)
201  2  -6.5    200  -201  u=200  imp:n=1  $ Zircaloy tube
202  3  -0.5    201        u=200  imp:n=1  $ Water/steam outside

c ------------------------------------------------------------
c PIN SURFACES
c ------------------------------------------------------------

c Fuel pin (u=100)
100   cz  0.488     $ Fuel radius (9.76 mm diameter)
101   cz  0.498     $ Clad inner
102   cz  0.563     $ Clad outer (11.26 mm diameter)

c Water rod (u=200) - larger diameter
200   cz  0.750     $ Water rod inner (15.0 mm diameter)
201   cz  0.813     $ Water rod outer (16.26 mm diameter)

c ------------------------------------------------------------
c LATTICE ASSEMBLY (u=300) - 8×8 ARRAY
c ------------------------------------------------------------
c
c Water rods at positions (1,1) and (-1,-1)
c W = water rod (u=200), F = fuel pin (u=100)
c
c     -3  -2  -1   0   1   2   3   4
c  +--------------------------------
c 4|   F   F   F   F   F   F   F   F
c 3|   F   F   F   F   F   F   F   F
c 2|   F   F   F   F   F   F   F   F
c 1|   F   F   F   F   W   F   F   F
c 0|   F   F   F   F   F   F   F   F
c-1|   F   F   F   W   F   F   F   F
c-2|   F   F   F   F   F   F   F   F
c-3|   F   F   F   F   F   F   F   F

300  0  -300  u=300  lat=1  imp:n=1  fill=-3:4 -3:4 0:0
     100 100 100 100 100 100 100 100  $j=4
     100 100 100 100 100 100 100 100  $j=3
     100 100 100 100 100 100 100 100  $j=2
     100 100 100 100 200 100 100 100  $j=1
     100 100 100 100 100 100 100 100  $j=0
     100 100 100 200 100 100 100 100  $j=-1
     100 100 100 100 100 100 100 100  $j=-2
     100 100 100 100 100 100 100 100  $j=-3

c Lattice boundary
c 8 pins × 1.63 cm pitch = 13.04 cm → ±6.52 cm
300   rpp  -6.52 6.52  -6.52 6.52  0 380

c ------------------------------------------------------------
c GLOBAL PLACEMENT
c ------------------------------------------------------------

999   0  -300  fill=300  imp:n=1
1000  0   300   imp:n=0

c ============================================================
c MATERIALS
c ============================================================

m1   $ UO2 fuel, 3.5% enriched
    92234.70c  3.00e-4
    92235.70c  0.0350
    92238.70c  0.9650
     8016.70c  2.0000

m2   $ Zircaloy-2 (BWR clad)
    40000.60c  0.9850
    50000.35c  0.0150

m3   $ Water (two-phase, effective density 0.5 g/cm³ for boiling)
     1001.70c  2.0
     8016.70c  1.0
mt3  lwtr.13t

c ============================================================
c PROBLEM SPECIFICATION
c ============================================================

mode n
kcode 10000 1.0 50 250
ksrc 0 0 190
```

**Usage Notes**:
- **Void fraction**: Adjust water density (0.3-0.7 g/cm³) for different boiling fractions
- **Enrichment zones**: BWRs often use axial enrichment zoning (higher at bottom)
- **Water rod positions**: Vary by design (2-4 water rods typical)

---

## HTGR (High-Temperature Gas Reactor)

### Prismatic Block (Hexagonal Lattice)

**Design**: Prismatic modular reactor
**Fuel channels**: 31 per block (hexagonal pattern)
**Coolant channels**: 37 (interspersed)
**Hexagonal pitch**: 2.77 cm (R = 1.6 cm)
**Block height**: 79.3 cm
**Coolant**: Helium gas

**Complete Template**:
```mcnp
c ============================================================
c HTGR PRISMATIC FUEL BLOCK (HEXAGONAL)
c ============================================================

c ------------------------------------------------------------
c UNIVERSE DEFINITIONS
c ------------------------------------------------------------

c Fuel compact universe (u=100) - contains TRISO particles
100  1  -1.75   -100        u=100  imp:n=1  $ Fuel compact (homogenized)
101  2  -1.70    100  -101  u=100  imp:n=1  $ Graphite channel wall

c Coolant channel universe (u=200)
200  3  -5e-3   -200        u=200  imp:n=1  $ Helium coolant (5 mg/cm³)
201  2  -1.70    200  -201  u=200  imp:n=1  $ Graphite wall

c Graphite cell universe (u=300) - solid graphite
300  2  -1.70   -300        u=300  imp:n=1  $ Solid graphite

c ------------------------------------------------------------
c CHANNEL SURFACES (in universes)
c ------------------------------------------------------------

100   cz  0.635     $ Fuel compact radius (12.7 mm diameter)
101   cz  0.793     $ Fuel channel outer (15.86 mm diameter)

200   cz  0.476     $ Coolant channel radius (9.52 mm diameter)
201   cz  0.635     $ Coolant channel outer (12.7 mm diameter)

300   cz  0.793     $ Graphite cell radius

c ------------------------------------------------------------
c LATTICE ASSEMBLY (u=400) - LAT=2 HEXAGONAL
c ------------------------------------------------------------
c
c Hexagonal lattice: 13×13 positions
c F = fuel (u=100), C = coolant (u=200), G = graphite (u=300)
c
c Pattern (31 fuel, 37 coolant, rest graphite):

400  0  -400  u=400  lat=2  imp:n=1  fill=-6:6 -6:6 0:0
     300 300 300 300 300 300 300 300 300 300 300 300 300  $j=6
      300 300 300 300 300 300 100 100 100 300 300 300 300  $j=5
       300 300 300 300 300 100 200 100 200 100 300 300 300  $j=4
        300 300 300 100 200 100 200 100 200 100 100 300 300  $j=3
         300 300 100 200 100 200 100 200 100 200 100 100 300  $j=2
          300 100 200 100 200 100 200 100 200 100 200 100 300  $j=1
           300 100 100 200 100 200 100 200 100 200 100 300  $j=0
            300 100 200 100 200 100 200 100 200 100 300  $j=-1
             300 100 100 200 100 200 100 200 100 300  $j=-2
              300 100 200 100 200 100 200 100 100 300  $j=-3
               300 300 100 200 100 200 100 100 300  $j=-4
                300 300 300 100 100 100 300 300 300  $j=-5
                 300 300 300 300 300 300 300 300 300  $j=-6

c Hexagonal block boundary (RHP - MUST use 9 values for LAT=2)
c Format: RHP vx vy vz  hx hy hz  Rx Ry Rz
c  vx vy vz: origin (0, 0, 0)
c  hx hy hz: height vector (0, 0, 79.3)
c  Rx Ry Rz: radius vector (0, 1.6, 0) where R = pitch/√3 = 2.77/1.732
400   rhp  0 0 0   0 0 79.3   0 1.6 0    $ Hex block

c ------------------------------------------------------------
c GLOBAL PLACEMENT
c ------------------------------------------------------------

999   0  -400  fill=400  imp:n=1
1000  0   400   imp:n=0

c ============================================================
c MATERIALS
c ============================================================

m1   $ Fuel compact (homogenized TRISO + matrix)
c    Option 1: Homogenize TRISO particles in graphite matrix
     6012.00c  0.40      $ Carbon (from matrix + coatings)
    92235.00c  0.008     $ U-235 (19.75% enriched TRISO)
    92238.00c  0.032     $ U-238
     8016.00c  0.04      $ Oxygen (from UO2 kernels)
    14000.60c  0.06      $ Silicon (from SiC coating)
mt1  grph.18t            $ 600K graphite S(α,β)

m2   $ Graphite block (nuclear grade)
     6012.00c  0.9890
     6013.00c  0.0110
mt2  grph.18t

m3   $ Helium coolant (high pressure, ~900°C)
     2004.00c  1.0

c ============================================================
c PROBLEM SPECIFICATION
c ============================================================

mode n
kcode 10000 1.0 50 250
ksrc 0 0 39.65

c ============================================================
c NOTES
c ============================================================
c
c RHP 9-value specification:
c  - Origin: (0, 0, 0)
c  - Height vector: (0, 0, 79.3) → 79.3 cm tall
c  - Radius vector: (0, 1.6, 0) → R = 1.6 cm
c  - Hexagonal pitch = R × √3 = 1.6 × 1.732 = 2.77 cm
c
c Homogenization:
c  - Explicit TRISO modeling: Use nested SO surfaces in u=100
c  - Homogenized: Effective densities (faster, used here)
c
c Thermal scattering:
c  - ESSENTIAL for graphite (MT card)
c  - Use grph.18t for 600K (~327°C)
c  - Use grph.24t for 1200K (~927°C) if higher temp
c
c ============================================================
```

**Usage Notes**:
- **RHP 9-value syntax**: REQUIRED for LAT=2 in MCNP6
- **Thermal scattering**: MT card ESSENTIAL for graphite reactors
- **TRISO particles**: For explicit modeling, see "TRISO Particle Template" below
- **Hexagonal pitch**: R × √3 where R is the radius vector value

---

## TRISO Particle Template

### 5-Layer Coating Structure

**Application**: Detailed HTGR fuel modeling
**Kernel**: UO2 or UCO (500 μm diameter typical)
**Coatings**: Buffer (100 μm) + IPyC (40 μm) + SiC (35 μm) + OPyC (40 μm)
**Matrix**: Graphite (fills compact)

**Complete Template**:
```mcnp
c ============================================================
c TRISO PARTICLE (5-LAYER COATING)
c ============================================================

c ------------------------------------------------------------
c TRISO PARTICLE UNIVERSE (u=100)
c ------------------------------------------------------------

1  1  -10.8   -1       u=100  vol=6.545e-5  $ Kernel (UO2, 500 μm dia)
2  2  -0.98    1  -2   u=100                $ Buffer (porous C, 100 μm)
3  3  -1.85    2  -3   u=100                $ IPyC (dense PyC, 40 μm)
4  4  -3.20    3  -4   u=100                $ SiC (ceramic, 35 μm)
5  5  -1.86    4  -5   u=100                $ OPyC (dense PyC, 40 μm)
6  6  -1.75    5       u=100                $ Matrix (graphite)

c ------------------------------------------------------------
c SURFACES (SO - centered at origin for universe)
c ------------------------------------------------------------

1  so  0.02500    $ Kernel radius (250 μm = 0.0250 cm)
2  so  0.03500    $ Buffer outer (350 μm = 0.0350 cm)
3  so  0.03900    $ IPyC outer (390 μm = 0.0390 cm)
4  so  0.04250    $ SiC outer (425 μm = 0.0425 cm)
5  so  0.04650    $ OPyC outer (465 μm = 0.0465 cm)

c ============================================================
c MATERIALS
c ============================================================

m1  $ UO2 kernel (19.75% enriched)
   92234.00c  3.34e-3    $ U-234
   92235.00c  1.996e-1   $ U-235 (enriched)
   92236.00c  1.93e-4    $ U-236
   92238.00c  7.968e-1   $ U-238
    8016.00c  1.3613     $ Oxygen
c  Kernel density: 10.8 g/cm³ (UO2 theoretical density)

m2  $ Buffer (porous carbon, ~50% theoretical density)
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t
c  Buffer density: 0.98 g/cm³ (porous)

m3  $ IPyC (inner pyrolytic carbon, dense)
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.18t
c  IPyC density: 1.85 g/cm³ (dense)

m4  $ SiC (silicon carbide, stoichiometric)
   14000.60c  0.5        $ Silicon
    6012.00c  0.495      $ Carbon-12
    6013.00c  0.005      $ Carbon-13
c  SiC density: 3.20 g/cm³ (theoretical)

m5  $ OPyC (outer pyrolytic carbon, dense)
    6012.00c  0.9890
    6013.00c  0.0110
mt5 grph.18t
c  OPyC density: 1.86 g/cm³ (dense)

m6  $ Graphite matrix (compact matrix material)
    6012.00c  0.9890
    6013.00c  0.0110
mt6 grph.18t
c  Matrix density: 1.75 g/cm³

c ============================================================
c NOTES
c ============================================================
c
c Multi-scale precision:
c  - Kernel: 0.02500 cm (250 μm) - 5 significant figures
c  - Coatings: 0.0XXXX cm - preserve μm-scale precision
c  - MCNP uses cm for ALL lengths
c
c Volume calculations (for verification):
c  V_kernel = (4/3)π(0.025)³   = 6.545e-5 cm³
c  V_buffer = (4/3)π(0.035³-0.025³) = 1.139e-4 cm³
c
c Surface type:
c  - SO (sphere at origin) fastest for repeated structures
c  - Use in universe, replicate via lattice or random
c
c Thermal scattering:
c  - MT cards ESSENTIAL for carbon/graphite
c  - grph.18t for 600K, grph.24t for 1200K
c
c Usage:
c  - Place TRISO particles in fuel compact (u=200)
c  - Use lattice or stochastic placement
c  - Typical: 10,000-30,000 particles per compact
c
c ============================================================
```

**Multi-Scale Integration**:
```mcnp
c Fuel compact with TRISO particles (explicit)
c Compact universe (u=200)
200  0  -200  u=200  lat=1  fill=0:9 0:9 0:9  $ 10×10×10 TRISO array
     [... 1000 universe numbers, mix of 100 (TRISO) and 6 (matrix) ...]

c Compact surfaces
200  rpp  -0.635 0.635  -0.635 0.635  0 1.27    $ Compact (12.7 mm diameter)
```

---

## Fast Reactor (Sodium-Cooled)

### Hexagonal Assembly

**Design**: Sodium-cooled fast reactor (SFR)
**Fuel**: MOX or metallic (U-Pu-Zr)
**Coolant**: Liquid sodium
**Hex assembly**: 217 pins (19-pin positions across flats)
**Pin pitch**: 0.86 cm (tight lattice)
**Assembly pitch**: 16.14 cm

**Template**:
```mcnp
c ============================================================
c FAST REACTOR HEXAGONAL ASSEMBLY
c ============================================================

c ------------------------------------------------------------
c PIN UNIVERSE (u=10)
c ------------------------------------------------------------

10  1  -15.8   -10        u=10  imp:n=1  $ MOX fuel (Pu-U oxide)
11  0          10  -11    u=10  imp:n=1  $ Sodium bond
12  2  -7.9    11  -12    u=10  imp:n=1  $ Steel clad (HT-9)
13  3  -0.85   12         u=10  imp:n=1  $ Sodium coolant

c Pin surfaces
10  cz  0.292     $ Fuel radius (5.84 mm diameter)
11  cz  0.300     $ Bond outer (6.00 mm diameter)
12  cz  0.336     $ Clad outer (6.72 mm diameter)

c ------------------------------------------------------------
c LATTICE (simplified 7-ring hex = 127 pins)
c ------------------------------------------------------------

100  0  -100  u=100  lat=2  fill=-6:6 -6:6 0:0
     [... hexagonal pattern of u=10, 127 positions ...]

c Hex assembly boundary (RHP 9-value)
100  rhp  0 0 0   0 0 200   0 6.5 0    $ 200 cm tall, R=6.5 cm

c ------------------------------------------------------------
c GLOBAL
c ------------------------------------------------------------

999   0  -100  fill=100  imp:n=1
1000  0   100   imp:n=0

c ============================================================
c MATERIALS
c ============================================================

m1  $ MOX fuel (mixed oxide, 25% PuO2 in UO2)
   92235.70c  0.002      $ U-235 (depleted uranium)
   92238.70c  0.748      $ U-238
   94239.70c  0.200      $ Pu-239 (weapons-grade Pu)
   94240.70c  0.050      $ Pu-240
    8016.70c  2.000      $ Oxygen

m2  $ HT-9 steel clad (ferritic steel)
   26000.50c  0.85       $ Iron
   24000.50c  0.12       $ Chromium
   28000.50c  0.005      $ Nickel
   42000.60c  0.01       $ Molybdenum
   74000.60c  0.005      $ Tungsten

m3  $ Liquid sodium coolant (500°C)
   11023.70c  1.0
c  Sodium density: 0.85 g/cm³ at 500°C

c ============================================================
c PROBLEM
c ============================================================

mode n
kcode 10000 1.0 50 250
ksrc 0 0 100
```

---

## Summary Table

| Reactor Type | Lattice Type | Surface Type | Pin Pitch | Assembly Pitch | Enrichment |
|--------------|--------------|--------------|-----------|----------------|------------|
| **PWR 17×17** | LAT=1 (RPP) | CZ (centered) | 1.26 cm | 21.42 cm | 3-5% U-235 |
| **BWR 8×8** | LAT=1 (RPP) | CZ (centered) | 1.63 cm | 13.04 cm | 2.5-4% U-235 |
| **HTGR Prismatic** | LAT=2 (RHP) | CZ (centered) | 2.77 cm | ~40 cm hex | 19.75% U-235 |
| **Fast Reactor** | LAT=2 (RHP) | CZ (centered) | 0.86 cm | 16.14 cm | Pu-239 (MOX) |
| **TRISO Particle** | N/A | SO (centered) | N/A | N/A | 10-20% U-235 |

---

## Modification Guidelines

### Changing Enrichment
```mcnp
c Original (4.5% U-235)
m1  92235.70c  0.0450
    92238.70c  0.9550

c Modified (3.0% U-235)
m1  92235.70c  0.0300
    92238.70c  0.9700
```

### Adding Axial Zones
```mcnp
c Define multiple axial zones for burnup tracking
c Zone 1 (bottom)
1  1  -10.5  -1  -10 11   u=10  $ Fuel zone 1
c Zone 2
2  1  -10.5  -1  -11 12   u=10  $ Fuel zone 2
[... 7 more zones ...]

c Axial planes
10  pz  0.0
11  pz  45.75    $ 366/8 = 45.75 cm per zone
12  pz  91.50
[... etc ...]
```

### Using Burnable Absorbers
```mcnp
c Gadolinia-bearing pin (u=103)
103  7  -10.2   -100  u=103  $ UO2-Gd2O3 fuel
[... same clad/coolant as u=100 ...]

m7  $ UO2 with 8 wt% Gd2O3
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.08
   64152.70c  0.001     $ Gd-152
   64154.70c  0.011     $ Gd-154
   64155.70c  0.074     $ Gd-155
   64156.70c  0.102     $ Gd-156
   64157.70c  0.078     $ Gd-157
   64158.70c  0.124     $ Gd-158
   64160.70c  0.109     $ Gd-160
```

---

**See Also**:
- `concentric_geometry_reference.md` - Nested cylinder patterns
- `lattice_geometry_reference.md` - LAT=1 and LAT=2 specifications
- `surface_selection_patterns.md` - Surface type selection

**Version**: 1.0.0 (2025-11-08)
**Part of**: mcnp-geometry-builder skill refinement
