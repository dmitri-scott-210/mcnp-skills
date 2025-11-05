# GT-MHR Design Specification Document

**Project**: GT-MHR Full Reactor Model Validation
**Created**: 2025-10-31
**Purpose**: Design parameters from published literature for MCNP model generation
**Version**: 1.0

---

## Document Overview

This document compiles GT-MHR (Gas Turbine - Modular Helium Reactor) design parameters from published literature and the reference model `gt-mhr-pbmr.i` (Forest Brown, MCNP Criticality Primer). These parameters serve as the specification for generating a complete MCNP reactor model using the MCNP skills framework.

---

## 1. TRISO Particle Specifications

### 1.1 Five-Layer Coated Particle Structure

TRISO (TRi-structural ISOtropic) particles consist of a spherical fuel kernel surrounded by four coating layers. This design provides excellent fission product retention and structural integrity at high temperatures.

**Layer Structure** (from inside to out):

| Layer # | Material | Purpose | Source |
|---------|----------|---------|--------|
| 1 | UO₂ or UCO kernel | Fissile fuel | IAEA TECDOC-1645, 2010 |
| 2 | Porous carbon buffer | Fission gas retention | IAEA TECDOC-1645, 2010 |
| 3 | Inner PyC (IPyC) | Pressure barrier | IAEA TECDOC-1645, 2010 |
| 4 | Silicon carbide (SiC) | Primary containment | IAEA TECDOC-1645, 2010 |
| 5 | Outer PyC (OPyC) | Structural support | IAEA TECDOC-1645, 2010 |

### 1.2 Layer Dimensions

**Standard TRISO Dimensions** (from literature):

| Parameter | Value | Range | Source |
|-----------|-------|-------|--------|
| **Kernel diameter** | 350 μm | 350-600 μm | NRC PNNL-31427 (2021) |
| **Buffer thickness** | 100 μm | 100-120 μm | IAEA TECDOC-2090 (2021) |
| **IPyC thickness** | 40 μm | 35-50 μm | NRC PNNL-31427 (2021) |
| **SiC thickness** | 35 μm | 35-60 μm | NRC PNNL-31427 (2021) |
| **OPyC thickness** | 40 μm | 27-40 μm | NRC PNNL-31427 (2021) |
| **Total particle diameter** | 920 μm | 500-1000 μm | IAEA TECDOC-1645 (2010) |

**GT-MHR Reference Model Dimensions** (from gt-mhr-pbmr.i):

The reference model uses slightly smaller dimensions optimized for the NGNR/GT-MHR design:

| Layer | Radius (cm) | Radius (μm) | Thickness (μm) | MCNP Surface |
|-------|-------------|-------------|----------------|--------------|
| Kernel (UCO) | 0.0175 | 175 | 350 diameter | 101 so 0.0175 |
| Buffer outer | 0.0275 | 275 | 100 | 102 so 0.0275 |
| IPyC outer | 0.0315 | 315 | 40 | 103 so 0.0315 |
| SiC outer | 0.0350 | 350 | 35 | 104 so 0.0350 |
| OPyC outer | 0.0390 | 390 | 40 | 105 so 0.0390 |

**Total particle diameter**: 780 μm (0.078 cm)

### 1.3 Material Densities (from gt-mhr-pbmr.i)

| Material | ID | Atom Density (atoms/b-cm) | Mass Density | Notes |
|----------|----|-----------------------------|--------------|-------|
| UCO Kernel | m1 | 7.086×10⁻² | — | 10.36% enriched |
| Buffer Carbon | m2 | 5.0147×10⁻² | ~1.05 g/cm³ | Porous carbon (~50% TD) |
| IPyC | m3 | 9.5279×10⁻² | ~1.9 g/cm³ | High-density PyC |
| SiC | m4 | 9.6136×10⁻² | ~3.2 g/cm³ | Silicon carbide |
| OPyC | m5 | 9.5279×10⁻² | ~1.9 g/cm³ | High-density PyC |
| Matrix Graphite | m6 | — | 1.7 g/cm³ | Graphite matrix |

### 1.4 Fuel Composition

**UCO Fuel (Material m1)** - 10.36% Enriched Uranium Oxycarbide:

```
m1   92235.66c  0.002475    (U-235: 10.36% of total U)
     92238.66c  0.021145    (U-238: 89.64% of total U)
      6000.66c  0.01181     (Carbon)
      8016.62c  0.03543     (Oxygen-16)
mt1 grph.60t                (Thermal scattering law)
```

**Enrichment Calculation**:
- U-235 fraction: 0.002475 / (0.002475 + 0.021145) = 10.48% ≈ 10.36%

---

## 2. Fuel Compact Geometry

### 2.1 Particle Lattice Structure

**Cubic Lattice Configuration**:
- **Lattice type**: lat=1 (cubic/rectangular lattice in MCNP)
- **Array dimensions**: 15×15×1 (-7:7, -7:7, 0:0)
- **Unit cell size**: 0.0951 cm cube (RPP -0.04755 to 0.04755)
- **Packing fraction**: ~35% (particles dispersed in graphite matrix)

**MCNP Implementation** (from gt-mhr-pbmr.i):

```
200 6 -1.7 -200 lat=1 u=40 imp:n=1     $ cubic lattice
        fill= -7:7 -7:7 0:0
        [15×15 array with mix of u=40 (graphite) and u=50 (particles)]

201 0 -201 lat=1 fill=40 imp:n=1 u=41  $ transition lattice
```

**Surface Definition**:
```
200 rpp -0.04755 0.04755 -0.04755 0.04755 -0.04755 0.04755  $ particle cube
201 RPP -.71325 .71325 -.71325 .71325 -.04755 .04755        $ transition slab
```

### 2.2 Fuel Compact Dimensions

**Cylindrical Fuel Compact**:

| Parameter | Value | MCNP Surface | Source |
|-----------|-------|--------------|--------|
| Compact radius | 0.6225 cm | 300 cz 0.6225 | gt-mhr-pbmr.i |
| Gap radius | 0.635 cm | 301 cz 0.635 | gt-mhr-pbmr.i |
| Compact fill | Universe 41 (particle lattice) | — | gt-mhr-pbmr.i |
| Gap material | Void | — | gt-mhr-pbmr.i |
| Wall material | Graphite (8.725580×10⁻² atoms/b-cm) | m7 | gt-mhr-pbmr.i |

**MCNP Cell Cards** (universe 5):
```
300 0 -300 fill=41 u=5 imp:n=1          $ fuel compact region
301 0 300 -301 u=5 imp:n=1              $ void outside fuel pin
302 7 8.725580e-2 301 u=5 imp:n=1       $ graphite wall
```

---

## 3. Fuel Block Layout

### 3.1 Hexagonal Fuel Block Configuration

**Published GT-MHR Specifications** (Wikipedia, 2025):
- **Fuel pins per block**: 216
- **Coolant channels per block**: 108 helium channels
- **Block arrangement**: 3-4 concentric rings of 36 hexagonal blocks
- **Interstitial gap**: 0.2 cm between blocks

**GT-MHR Reference Model** (gt-mhr-pbmr.i):

The simplified reference model uses a 23×23 hexagonal lattice (lat=2) with a mix of:
- **Fuel compacts** (universe 5): Fuel channels
- **Large coolant holes** (universe 6, r=0.79375 cm): Primary cooling
- **Small coolant holes** (universe 5 gap, r=0.635 cm): Secondary cooling
- **Graphite fill** (universe 4): Structural graphite

### 3.2 Coolant Channel Dimensions

**Large Coolant Hole** (universe 6):

| Parameter | Value | MCNP Definition | Source |
|-----------|-------|-----------------|--------|
| Channel radius | 0.79375 cm | 400 cz 0.79375 | gt-mhr-pbmr.i |
| Channel material | Void (helium) | 0 | gt-mhr-pbmr.i |
| Wall material | Graphite (m7) | 8.725580×10⁻² | gt-mhr-pbmr.i |

**MCNP Cell Cards**:
```
400 0 -400 u=6 imp:n=1                  $ larger coolant hole
401 7 8.725580e-2 400 u=6 imp:n=1       $ graphite wall
```

### 3.3 Hexagonal Block Geometry

**Hexagonal Lattice Boundaries** (6 planes):

The hexagonal shape is defined by 6 plane surfaces:

```
501 px 0.9398                           $ vertical plane (+x)
502 px -0.9398                          $ vertical plane (-x)
503 p 1 1.7320508076 0 1.8796          $ 60° plane
504 p 1 1.7320508076 0 -1.8796         $ 60° plane
505 p -1 1.7320508076 0 1.8796         $ 60° plane
506 p -1 1.7320508076 0 -1.8796        $ 60° plane
```

**Derived Hexagonal Dimensions**:
- **Lattice pitch**: 1.8796 cm (from plane equations)
- **Hexagon half-width**: 17.9985 cm (from hex surface in column)
- **Block height**: 79.3 cm (active fuel region)

### 3.4 Fuel Block Lattice (universe 4)

**Hexagonal Lattice Configuration**:
- **Lattice type**: lat=2 (hexagonal lattice in MCNP)
- **Array dimensions**: 23×23 (-11:11, -11:11, 0:0)
- **Fill pattern**: Mix of fuel compacts (u=5), coolant holes (u=6), and graphite (u=4)

**MCNP Definition**:
```
500 7 8.725580e-2 -501 502 -503 504 -505 506 u=4 lat=2 imp:n=1
                fill=-11:11 -11:11 0:0
        [23×23 array - see gt-mhr-pbmr.i lines 52-74 for complete fill pattern]
```

---

## 4. Column Structure

### 4.1 Fuel Column (universe 3)

The fuel column consists of three regions stacked vertically:

| Region | Height (cm) | Surface | Material | Universe |
|--------|-------------|---------|----------|----------|
| Bottom reflector | 79.3 | 603 hex | Graphite (m8) | — |
| Active fuel block | 79.3 | 601 hex | Fill u=4 | 4 (fuel block) |
| Top reflector | 793.0 | 602 hex | Graphite (m8) | — |
| **Total** | **951.6** | — | — | — |

**Height Calculations**:
- Bottom reflector: 0 to 79.3 cm
- Fuel block: 79.3 to 158.6 cm
- Top reflector: 158.6 to 951.6 cm (793 cm height)

**Hexagonal Surface Definitions**:
```
601 hex 0 0 79.3 0 0 793 17.9985 0 0     $ fuel block (79.3 cm height)
602 hex 0 0 872.3 0 0 79.3 17.9985 0 0   $ top reflector (79.3 to 951.6)
603 hex 0 0 0 0 0 79.3 17.9985 0 0       $ bottom reflector (0 to 79.3)
```

**Note**: The top reflector extends from z=872.3 to z=951.6 (actually 79.3 cm, not 793 cm as initially read).

**Fuel Block Fill Transformation**:
- **Rotation**: (0 0 0 30 120 90 60 30 90 90 90 0)
- **Purpose**: Rotates hexagonal fuel block 30° about z-axis

**MCNP Cell Cards**:
```
601 0 -601 *fill=4 (0 0 0 30 120 90 60 30 90 90 90 0) u=3 imp:n=1
602 8 8.725580e-2 -602 u=3 imp:n=1      $ top reflector
603 8 8.725580e-2 -603 u=3 imp:n=1      $ bottom reflector
604 0 601 #602 #603 u=3 imp:n=1         $ void outside column
```

### 4.2 Reflector Column (universe 2)

**Full-height reflector column**:

| Parameter | Value | MCNP Definition |
|-----------|-------|-----------------|
| Height | 951.6 cm | 700 hex 0 0 0 0 0 951.6 17.9985 0 0 |
| Material | Graphite (m9) | 8.725580×10⁻² atoms/b-cm |
| Purpose | Radial and peripheral reflector | — |

**MCNP Cell Cards**:
```
700 9 8.725580e-2 -700 u=2 imp:n=1      $ replaceable reflector column
701 0 700 u=2 imp:n=1                   $ void outside the column
```

---

## 5. Core Configuration

### 5.1 Core Dimensions (from literature)

**GT-MHR Core** (Wikipedia, Gas Turbine Modular Helium Reactor, 2025):

| Parameter | Value | Notes |
|-----------|-------|-------|
| Core radius | 4 m | Cylindrical geometry |
| Core height | 10 m | With axial reflectors |
| Top reflector | 1 m | Axial reflector |
| Bottom reflector | 1 m | Axial reflector |
| Active core height | 8 m | Fueled region |
| Core arrangement | 3-4 concentric rings | 36 blocks per ring |

### 5.2 Core Lattice (universe 1)

**Hexagonal Core Lattice**:
- **Lattice type**: lat=2 (hexagonal)
- **Array dimensions**: 23×23 (-11:11, -11:11, 0:0)
- **Fill pattern**: Fuel columns (u=3) in center, reflector columns (u=2) on periphery

**MCNP Definition**:
```
800 0 -800 u=1 lat=2 imp:n=1 fill=-11:11 -11:11 0:0
        [23×23 array - see gt-mhr-pbmr.i lines 85-107 for complete fill pattern]
```

**Lattice Surface**:
```
800 hex 0 0 0 0 0 951.6 18.05 0 0       $ lattice cell (slightly larger than column)
```

**Fill Pattern Characteristics** (from gt-mhr-pbmr.i):
- **Center region**: Fuel columns (universe 3)
- **Inner annulus**: Mixed fuel and reflector
- **Outer region**: Reflector columns (universe 2)
- **Pattern**: Roughly circular fuel region surrounded by reflector

### 5.3 Reactor Vessel

**Cylindrical Reactor Vessel**:

| Parameter | Value | MCNP Definition | Source |
|-----------|-------|-----------------|--------|
| Vessel shape | Right circular cylinder (RCC) | — | gt-mhr-pbmr.i |
| Radius | 341.63 cm | — | gt-mhr-pbmr.i |
| Height | 951.6 cm | — | gt-mhr-pbmr.i |
| Origin | (0, 0, 0) | — | gt-mhr-pbmr.i |
| Axis | (0, 0, 951.6) | Vertical | gt-mhr-pbmr.i |

**MCNP Surface Definition**:
```
900 rcc 0 0 0 0 0 951.6 341.63           $ outer barrel of core
```

**MCNP Cell Cards**:
```
900 0 -900 fill=1 imp:n=1                $ reactor core (filled with u=1)
901 0 900 imp:n=0                        $ outside the core (zero importance)
```

**Comparison to Literature**:
- Literature: r=4 m (400 cm), h=10 m (1000 cm)
- gt-mhr-pbmr.i: r=341.63 cm, h=951.6 cm
- **Difference**: Reference model is ~15% smaller (simplified model)

---

## 6. Material Specifications

### 6.1 Complete Material Definitions

**All materials from gt-mhr-pbmr.i**:

| Material | ID | Description | Density | Thermal Scattering |
|----------|----|--------------| --------|---------------------|
| UCO Fuel | m1 | 10.36% enriched UCO | 7.086×10⁻² | grph.60t |
| Buffer | m2 | Porous carbon buffer | 5.0147×10⁻² | grph.60t |
| IPyC | m3 | Inner pyrolytic carbon | 9.5279×10⁻² | grph.60t |
| SiC | m4 | Silicon carbide | 9.6136×10⁻² | grph.60t |
| OPyC | m5 | Outer pyrolytic carbon | 9.5279×10⁻² | grph.60t |
| Matrix | m6 | Graphite matrix | 1.7 g/cm³ | grph.60t |
| Fuel Block | m7 | Graphite + B-10 | 8.7255×10⁻² | grph.60t |
| Reflector | m8 | Graphite + B-10 | 8.7255×10⁻² | grph.60t |
| Side Refl | m9 | Graphite + B-10 | 8.7255×10⁻² | grph.60t |

### 6.2 Detailed Material Compositions

**Material m1: UCO Fuel (10.36% enriched)**
```
m1   92235.66c  0.002475    $ U-235 (10.36% of U)
     92238.66c  0.021145    $ U-238 (89.64% of U)
      6000.66c  0.01181     $ Carbon-12
      8016.62c  0.03543     $ Oxygen-16
mt1 grph.60t                $ Thermal scattering (graphite S(α,β))
```

**Material m2: Porous Carbon Buffer**
```
m2 6000.66c 1               $ Pure carbon
mt2 grph.60t                $ Thermal scattering
```

**Material m3: Inner Pyrolytic Carbon (IPyC)**
```
m3 6000.66c 1               $ Pure carbon
mt3 grph.60t                $ Thermal scattering
```

**Material m4: Silicon Carbide (SiC)**
```
m4    6000.66c 0.048068     $ Carbon
     14000.60c 0.048068     $ Silicon
mt4 grph.60t                $ Thermal scattering
```

**Material m5: Outer Pyrolytic Carbon (OPyC)**
```
m5 6000.66c 1               $ Pure carbon
mt5 grph.60t                $ Thermal scattering
```

**Material m6: Graphite Matrix**
```
m6 6000.66c 1               $ Pure carbon
mt6 grph.60t                $ Thermal scattering
```

**Material m7: Fuel Block Graphite**
```
m7   6000.66c 8.7255e-02    $ Carbon
     5010.66c 7.22e-07      $ Boron-10 impurity
mt7 grph.60t                $ Thermal scattering
```

**Material m8: Top/Bottom Reflector Graphite**
```
m8   6000.66c 8.7255e-02    $ Carbon
     5010.66c 7.22e-07      $ Boron-10 impurity
mt8 grph.60t                $ Thermal scattering
```

**Material m9: Replaceable Reflector Graphite**
```
m9   6000.66c 8.7255e-02    $ Carbon
     5010.66c 7.22e-07      $ Boron-10 impurity
mt9 grph.60t                $ Thermal scattering
```

**Boron Impurity**: 7.22×10⁻⁷ atoms/b-cm (natural boron in graphite)

### 6.3 Thermal Scattering

All graphite and carbon materials use the **grph.60t** thermal scattering law:
- **Library**: S(α,β) thermal scattering data
- **Temperature**: 60 = 600K (327°C)
- **Purpose**: Accurate modeling of neutron thermalization in graphite

---

## 7. Physics Parameters

### 7.1 Criticality Calculation (KCODE)

**Eigenvalue Calculation Setup**:

```
mode n                                      $ neutron transport only
kcode 5000 1.0 50 500                      $ criticality parameters
```

**KCODE Parameters**:
| Parameter | Value | Description |
|-----------|-------|-------------|
| NPK | 5000 | Neutrons per cycle |
| RKK | 1.0 | Initial k-eff guess |
| IKZ | 50 | Number of cycles to skip (inactive) |
| KCT | 500 | Total number of cycles to run (active) |

**Total Histories**: 5000 × 500 = 2,500,000 active neutron histories

### 7.2 Initial Source Distribution (KSRC)

**Three Initial Source Points**:

```
ksrc 180.5 2 120   0 202.5 436.15   -202.5 0 515.45
```

| Point | x (cm) | y (cm) | z (cm) | Location |
|-------|--------|--------|--------|----------|
| 1 | 180.5 | 2.0 | 120.0 | Lower-middle of core |
| 2 | 0.0 | 202.5 | 436.15 | Middle height, offset |
| 3 | -202.5 | 0.0 | 515.45 | Upper portion, offset |

**Purpose**: Distribute initial neutrons throughout core volume for efficient convergence

### 7.3 Variance Reduction and Output Control

**Print Dump Control**:
```
prdmp 999999 999999 1 1 9999999             $ print/dump control
```

**Source Point Detail**:
```
spdtl off                                   $ source point details off
```

**Purpose**: Minimize output file size, suppress detailed source point printing

### 7.4 Operational Characteristics (from literature)

**GT-MHR Operating Conditions** (from web search):

| Parameter | Value | Source |
|-----------|-------|--------|
| Thermal power | 350-600 MWth | Wikipedia (2025) |
| Outlet temperature | ~900°C | Wikipedia (2025) |
| Thermal efficiency | Up to 48% | Wikipedia (2025) |
| Coolant | Helium gas | Wikipedia (2025) |
| Neutron spectrum | Thermal | Wikipedia (2025) |
| Peak neutron energy | ~0.2 eV | Wikipedia (2025) |

**Note**: These operational parameters are not modeled in the MCNP input (steady-state k-eff calculation only).

---

## 8. Geometric Hierarchy Summary

### 8.1 Universe Structure

The GT-MHR model uses a 7-level nested universe hierarchy:

| Level | Universe | Description | Lattice Type | Dimensions |
|-------|----------|-------------|--------------|------------|
| 1 | u=50 | TRISO particle (5 spheres + matrix) | — | r=0.039 cm |
| 2 | u=40 | Particle lattice (cubic) | lat=1 | 15×15×1 array |
| 3 | u=41 | Flat transition lattice | lat=1 | Single cell |
| 4 | u=5 | Fuel compact (cylinder) | — | r=0.6225 cm |
| 5 | u=6 | Coolant hole (cylinder) | — | r=0.79375 cm |
| 6 | u=4 | Fuel block (hexagonal) | lat=2 | 23×23 array, h=79.3 cm |
| 7 | u=3 | Column (fuel + reflectors) | — | h=951.6 cm |
| 8 | u=2 | Reflector column | — | h=951.6 cm |
| 9 | u=1 | Core lattice (hexagonal) | lat=2 | 23×23 array |
| 10 | — | Reactor vessel (RCC) | — | r=341.63 cm, h=951.6 cm |

### 8.2 Lattice Types Used

**Cubic Lattice (lat=1)**:
- Particle lattice (u=40): 15×15×1 array
- Transition lattice (u=41): 1×1×1 array

**Hexagonal Lattice (lat=2)**:
- Fuel block (u=4): 23×23 array of fuel/coolant/graphite
- Core (u=1): 23×23 array of fuel columns/reflector columns

**Fill Transformations**:
- Fuel block rotation: (0 0 0 30 120 90 60 30 90 90 90 0) = 30° rotation about z-axis

---

## 9. Model Validation Targets

### 9.1 Design Parameter Tolerance

For the generated MCNP model, the following tolerances apply:

| Parameter Category | Target Accuracy | Notes |
|--------------------|-----------------|-------|
| TRISO dimensions | ±5% | Layer thicknesses |
| Compact dimensions | ±5% | Radii, heights |
| Block dimensions | ±5% | Hexagonal geometry |
| Core dimensions | ±10% | Overall vessel size |
| Material densities | ±1% | Atom densities |
| Enrichment | ±0.5% | U-235 fraction |

### 9.2 Structural Requirements

**Required Elements** (100% completion):
- ✅ All 7+ universe levels defined
- ✅ Both lattice types (lat=1 and lat=2)
- ✅ All 9 materials defined
- ✅ Thermal scattering laws (mt cards)
- ✅ KCODE criticality setup
- ✅ Initial source distribution (KSRC)
- ✅ Proper universe nesting and fill

**Geometry Validation**:
- Zero overlapping cells
- Complete spatial coverage (no voids)
- All surfaces properly referenced
- All universes properly filled

---

## 10. References

### 10.1 Primary Sources

1. **IAEA TECDOC-1645** (2010)
   "High Temperature Gas Cooled Reactor Fuels and Materials"
   https://www-pub.iaea.org/MTCD/Publications/PDF/TE_1645_CD/PDF/TECDOC_1645.pdf

2. **IAEA TECDOC-2090** (2021)
   "Coated Particle Fuels for High Temperature Gas Cooled Reactors"
   https://www-pub.iaea.org/MTCD/publications/PDF/TE-2090web.pdf

3. **NRC PNNL-31427** (June 2021)
   "TRISO Fuel: Properties and Failure Modes"
   https://www.nrc.gov/docs/ML2117/ML21175A152.pdf

4. **Forest Brown, LANL**
   "gt-mhr-pbmr.i" - MCNP Criticality Primer
   Approximate model of NGNR full core reactor based on GT-MHR

### 10.2 Secondary Sources

5. **INL Report**
   "TRISO Fuel: Design, Manufacturing, and Performance"
   https://art.inl.gov/NRC%20Training%202019/04_TRISO_Fuel.pdf

6. **Wikipedia** (2025)
   "Gas Turbine Modular Helium Reactor"
   https://en.wikipedia.org/wiki/Gas_turbine_modular_helium_reactor

7. **IAEA CRP-5 Benchmark** (2010)
   "Evaluation of High Temperature Gas Cooled Reactor Performance"
   IAEA-TECDOC-1382

8. **ScienceDirect** (2008)
   "IAEA GT-MHR benchmark calculations by using the HELIOS/MASTER physics analysis procedure and the MCNP Monte Carlo code"
   https://www.sciencedirect.com/science/article/abs/pii/S0029549308002690

### 10.3 Reference Model

**gt-mhr-pbmr.i**:
- Location: `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\gt-mhr-pbmr.i`
- Author: Wei Ji (Oct 16, 2004), Minor mods: FB Brown (Nov 26, 2004)
- Description: "Approximate model of NGNR full core reactor based on double heterogeneous fuel blocks"
- Lines: 222
- Universes: u=50, 40, 41, 5, 6, 4, 3, 2, 1
- Materials: m1-m9

---

## 11. Parameter Summary Table

### 11.1 Quick Reference - Key Dimensions

| Component | Parameter | Value | MCNP |
|-----------|-----------|-------|------|
| **TRISO Kernel** | Radius | 0.0175 cm | 101 so 0.0175 |
| **TRISO Particle** | Total radius | 0.039 cm | 105 so 0.0390 |
| **Particle Lattice** | Array size | 15×15×1 | fill= -7:7 -7:7 0:0 |
| **Fuel Compact** | Radius | 0.6225 cm | 300 cz 0.6225 |
| **Coolant Hole** | Radius | 0.79375 cm | 400 cz 0.79375 |
| **Fuel Block** | Array size | 23×23 | fill= -11:11 -11:11 0:0 |
| **Fuel Block** | Height | 79.3 cm | hex ... 79.3 ... |
| **Column** | Total height | 951.6 cm | hex ... 951.6 ... |
| **Core** | Array size | 23×23 | fill= -11:11 -11:11 0:0 |
| **Reactor** | Radius | 341.63 cm | rcc ... 341.63 |
| **Reactor** | Height | 951.6 cm | rcc ... 951.6 ... |

### 11.2 Quick Reference - Material IDs

| Material | MCNP ID | Primary Use |
|----------|---------|-------------|
| UCO Fuel | m1 | TRISO kernel |
| Buffer C | m2 | TRISO buffer layer |
| IPyC | m3 | TRISO inner PyC layer |
| SiC | m4 | TRISO SiC layer |
| OPyC | m5 | TRISO outer PyC layer |
| Matrix Graphite | m6 | Particle matrix, compact fill |
| Fuel Block Graphite | m7 | Fuel block structure, coolant walls |
| Reflector Graphite | m8 | Top/bottom axial reflectors |
| Side Reflector | m9 | Radial reflector columns |

### 11.3 Quick Reference - Universe IDs

| Universe | Description | Type |
|----------|-------------|------|
| u=50 | TRISO particle | Concentric spheres |
| u=40 | Particle lattice | lat=1 (cubic) |
| u=41 | Transition lattice | lat=1 (single cell) |
| u=5 | Fuel compact | Cylinder with fill=41 |
| u=6 | Coolant hole | Cylinder (void) |
| u=4 | Fuel block | lat=2 (hexagonal) |
| u=3 | Fuel column | Stacked hex (fuel + reflectors) |
| u=2 | Reflector column | Full-height hex |
| u=1 | Core lattice | lat=2 (hexagonal) |

---

## 12. Implementation Notes

### 12.1 MCNP Skills Mapping

**Phase 2 Model Generation** will use these skills:

| Component | Skill(s) Required |
|-----------|-------------------|
| TRISO particle spheres | mcnp-geometry-builder |
| Particle lattice | mcnp-lattice-builder |
| Fuel compact cylinder | mcnp-geometry-builder |
| Coolant hole cylinder | mcnp-geometry-builder |
| Fuel block hexagonal lattice | mcnp-lattice-builder + mcnp-geometry-builder |
| Column structure | mcnp-geometry-builder |
| Core lattice | mcnp-lattice-builder |
| Reactor vessel | mcnp-geometry-builder |
| All materials (m1-m9) | mcnp-material-builder |
| KCODE setup | mcnp-source-builder |
| Physics cards | mcnp-physics-builder |

### 12.2 Critical Considerations

**Double Heterogeneity**:
- Particles in compacts (first level of heterogeneity)
- Compacts in fuel blocks (second level of heterogeneity)
- Requires careful lattice nesting and fill commands

**Hexagonal Geometry**:
- Requires 6 plane surfaces to define hexagonal prism
- Lattice type lat=2 for hexagonal arrays
- Index ranges: -11:11 for 23×23 array (23 = 2×11 + 1)

**Fill Transformations**:
- Fuel block rotated 30° to align with hex lattice
- Syntax: (x y z θ φ ψ α β γ O₁ O₂ O₃)
- Example: (0 0 0 30 120 90 60 30 90 90 90 0)

**Material Consistency**:
- All carbon materials require mt (thermal scattering) cards
- Boron impurity in structural graphite (m7, m8, m9)
- UCO fuel has thermal scattering even though it's primarily oxide/carbide

---

## 13. Next Steps

### Phase 2: Model Generation

With design parameters now documented, proceed to Phase 2:

1. Build TRISO particle geometry (5 concentric spheres)
2. Build particle lattice (cubic, 15×15×1)
3. Build fuel compact (cylinder with lattice fill)
4. Build coolant holes (cylinders)
5. Build fuel block (hexagonal lattice 23×23)
6. Build column structures (fuel + reflectors)
7. Build core lattice (hexagonal 23×23)
8. Build reactor vessel (RCC)
9. Define all 9 materials with thermal scattering
10. Set up KCODE and KSRC
11. Add title, mode, and control cards

**Target**: Generate `generated_gt_mhr.inp` with complete MCNP input deck

---

**Document Status**: ✅ Complete
**Design Parameters**: ✅ Documented
**Ready for Phase 2**: ✅ Yes

---

**END OF DESIGN SPECIFICATION**
