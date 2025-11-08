# MSRE Design Specification for MCNP Benchmark Model

**Document Purpose:** Comprehensive design specification for the Molten Salt Reactor Experiment (MSRE) first criticality benchmark, extracted from published literature for MCNP model development.

**Primary Sources:**
- MSRE_Overview_Spec.md (Table 5 specifications)
- Shen et al. (2021), "Reactor Physics Benchmark of the First Criticality in the Molten Salt Reactor Experiment," Nuclear Science and Engineering, 195:8, 825-837
- IRPhEP Handbook 2019 Edition

**Model Target:** Zero-power first criticality with ²³⁵U fuel (June 1, 1965, ~6:00 PM)

---

## 1. REACTOR OVERVIEW

### 1.1 General Characteristics
- **Reactor Type:** Graphite-moderated molten salt reactor
- **Design Power:** 10 MWth
- **First Criticality Power:** ~10 W (zero power, stationary salt)
- **Operating Temperature:** 911 K (1181°F)
- **Fuel/Coolant:** Molten fluoride salt (LiF-BeF₂-ZrF₄-UF₄)
- **Moderator:** Graphite
- **Structural Material:** INOR-8 (Hastelloy-N, Ni-based alloy)

### 1.2 Criticality Configuration
- **Date:** June 1, 1965
- **Salt Condition:** Stationary (not flowing)
- **Temperature Distribution:** Uniform at 911 K (except thermal shield at 305 K)
- **Control Rod 1:** Fully withdrawn (51 in. = 129.54 cm)
- **Control Rod 2:** Fully withdrawn (51 in. = 129.54 cm)
- **Regulating Rod:** 46.6 in. (118.364 ± 0.127 cm) - 3% integral worth inserted
- **Experimental keff:** 1.0000 (by definition at criticality)

### 1.3 Benchmark Expected Values
- **Experimental keff:** 1.0000
- **Expected keff (with bias):** 0.99978 ± 0.00420
- **Calculated keff (Serpent/ENDF-VII.1):** 1.02132 ± 0.00003
- **C-E Discrepancy:** 2.154% or 2154 pcm
- **Model Simplification Bias:** -22 ± 5 pcm
- **Total Experimental Uncertainty:** ±420 pcm (1σ)
- **Nuclear Data Uncertainty:** ±664 pcm (1σ)

---

## 2. GEOMETRY SPECIFICATIONS

### 2.1 Dimensional Reference System

**Temperature States:**
- **Cold (as-built):** 293 K (68°F) - all blueprints and design documents
- **Hot (operating):** 911 K (1181°F) - first criticality condition

**Thermal Expansion Coefficients:**
- **Graphite:** 1.5 ± 0.2 × 10⁻⁶ °F⁻¹
- **INOR-8 and metallic components:** 7.8 ± 0.2 × 10⁻⁶ °F⁻¹

**Expansion Reference:**
- Reactor vessel expands downward from interface between outlet pipe and upper insulation
- Horizontal graphite lattice connected to vessel bottom (z = 0 reference)
- Vertical graphite stringers supported by horizontal lattice

**Coordinate System:**
- z = 0 corresponds to bottom of horizontal graphite lattice
- Positive z is upward
- Radial symmetry about vertical axis (cylindrical geometry)

### 2.2 Radial Dimensions

#### 2.2.1 As-Built Cold Dimensions (293 K)

| Component | Inner Radius (cm) | Outer Radius (cm) | Thickness (cm) |
|-----------|-------------------|-------------------|----------------|
| Graphite lattice | 0.0 | 70.168 | - |
| Core can (inner) | 70.168 | 70.485 | 0.317 |
| Core can (outer) | 70.485 | 71.120 | 0.635 |
| Downcomer annulus (void) | 71.120 | 73.660 | 2.540 |
| Reactor vessel (inner) | 73.660 | 76.200 | 2.540 |
| Insulation layer | 76.200 | ~91.44 | 15.24 |
| Thermal shield | ~91.44 | ~158.75 | Variable |

#### 2.2.2 Hot Operating Dimensions (911 K) - BENCHMARK MODEL

| Component | Inner Radius (cm) | Outer Radius (cm) | Thickness (cm) | Notes |
|-----------|-------------------|-------------------|----------------|-------|
| Graphite lattice | 0.0 | **70.285** | - | Core region |
| Core can (inner) | **70.285** | **71.097** | 0.812 | INOR-8 |
| Core can (outer) | 71.097 | **71.737** | 0.640 | INOR-8 |
| Downcomer annulus (void) | 71.737 | **74.299** | 2.562 | Flow region |
| Reactor vessel (inner) | 74.299 | **75.741** | 1.442 | INOR-8 shell |
| Reactor vessel (outer) | 75.741 | **76.862** | 1.121 | Active region |
| Insulation layer | 76.862 | ~93.09 | ~16.23 | Vermiculite (homogenized) |
| Thermal shield (inner) | ~93.09 | ~118.11 | 25.02 | Type 304 SS |
| Thermal shield (outer) | 118.11 | 158.75 | 40.64 | Multiple shells |

**Key Radii (Hot, 911 K):**
- Graphite lattice radius: **70.285 cm** (Table 5, MSRE_Overview_Spec)
- Core can inner radius: **71.097 cm**
- Core can outer radius: **71.737 cm**
- Reactor vessel inner radius: **74.299 cm**
- Reactor vessel outer radius (active region): **75.741 cm**
- Thermal shield outer radius: **158.75 cm** (316.5 cm diameter)

### 2.3 Axial Dimensions

#### 2.3.1 As-Built Cold Dimensions (293 K)

| Component | Height/Length (cm) | Axial Position | Notes |
|-----------|-------------------|----------------|-------|
| Horizontal graphite lattice | 2.54 × 4.1275 | z = 0 (reference) | 2 layers, perpendicular |
| Graphite stringer height | 170.027 | Above lattice | Vertical |
| Effective core height | ~166.7 | Variable | Active fuel region |
| Core can height | ~173.9 | Above lattice | Surrounds stringers |
| Total vessel height | 269.771 | Bottom to outlet top | Torispherical heads |

#### 2.3.2 Hot Operating Dimensions (911 K) - BENCHMARK MODEL

| Component | Height/Length (cm) | Axial Position | Notes |
|-----------|-------------------|----------------|-------|
| Horizontal graphite lattice | 2.54 × 4.1275 | z = 0 | Reference plane |
| Graphite stringer height | **170.311** | z = 0 to 170.311 | Active core |
| Effective core height | **166.724 ± 1.0** | Variable | Benchmark parameter |
| Core can height | **174.219** | Above lattice | Contains core |
| Total vessel height | **272.113** | Bottom to outlet | Expanded |
| Lower head vertical section | 6.475 ± 1.0 | Below z = 0 | Torispherical |
| Upper plenum | Variable | Above core | Salt region |
| Lower plenum | Variable | Below z = 0 | Salt region |
| Outlet pipe height | 36.180 ± 1.0 | Top of vessel | Connection |

**Key Elevations (Hot, 911 K):**
- Bottom of horizontal lattice: z = 0 (reference)
- Top of vertical stringers: z = 170.311 cm
- Top of core can: z = 174.219 cm
- Control rod position reference: 0 = fully inserted, 51 in. = fully withdrawn

### 2.4 Graphite Core Structure

#### 2.4.1 Graphite Stringer Geometry

**Cold Dimensions (293 K):**
- Cross-section: 5.075 cm × 5.075 cm (square)
- Height: 170.027 cm
- Dowel section diameter (bottom): 2.54 cm
- Lattice block hole diameter: 2.642 cm

**Hot Dimensions (911 K) - BENCHMARK:**
- Cross-section: **5.084 cm × 5.084 cm** (square)
- Height: **170.311 cm**
- Dowel section diameter: ~2.55 cm (expanded)
- Material: Graphite, density 1.8507 g/cm³ (or 1.86 g/cm³)

**Arrangement:**
- Close-packed vertical array
- Total equivalent passages: **1,140** (including fractional sizes)
- Mounted on horizontal graphite lattice (2 layers at right angles)
- Upper surface tapered to prevent salt retention after drainage

#### 2.4.2 Fuel Channel Geometry

**Cold Dimensions (293 K):**
- Channel cross-section: 1.016 cm × 3.048 cm
- Corner radius: 0.508 cm (rounded corners)
- Channel count: 1,140 equivalent full-size passages

**Hot Dimensions (911 K) - BENCHMARK:**
- Channel width: **1.018 cm**
- Channel length: **3.053 cm**
- Corner radius: **0.508 cm** (rounded, radius = stringer width/10)
- Formed by grooves in 4 sides of stringers
- Material: Fuel salt

**Fuel-to-Graphite Ratio:**
- Nearly optimum for MSRE design
- Large enough to avoid blockage by small graphite pieces

#### 2.4.3 Horizontal Graphite Lattice (Support Structure)

- Cross-section: 2.54 cm × 4.1275 cm
- Arrangement: 2 layers at right angles
- Function: Support vertical stringers, rest on vessel bottom
- Holes: 2.642 cm diameter to house stringer dowels
- Position: z = 0 reference plane

### 2.5 Control Rods and Sample Baskets

#### 2.5.1 Location and Arrangement

- **Position:** Near center of core, replacing 4 graphite stringers
- **Configuration:** 3 control rod thimbles + 1 sample basket channel (central region)
- **Arrangement:** Equidistant spacing
- **Purpose:** Reactivity control (rods), graphite/INOR-8 specimen testing (baskets)

#### 2.5.2 Control Rod Thimble Geometry

**Cold Dimensions:**
- Outer diameter: 5.08 cm
- Wall thickness: 0.1651 cm
- Inner diameter: 4.7498 cm
- Material: INOR-8
- Length: Through full core height

**Control Rod Assembly:**
- **Poison material:** 70 wt% Gd₂O₃, 30 wt% Al₂O₃ (ceramic)
- **Poison density:** 5.873 ± 0.020 g/cm³
- **Poison section length:** 150.774 cm
- **Number of segments:** 38 elements
- **Segment length:** ~3.968 cm each
- **Canning:** Inconel shell around ceramic cylinders (3 per element)
- **Flexible hose OD:** 1.905 cm
- **Flexible hose ID:** 1.5875 cm
- **Hose material:** Helically wound stainless steel
- **Restraining cables:** 2 × 0.3175 cm diameter, braided Inconel

**Position Reference System:**
- **Zero position:** Fully inserted (driven in)
- **Withdrawn position:** 51 in. (129.54 cm) from zero
- **At criticality:**
  - Control Rod 1: 51 in. (fully withdrawn)
  - Control Rod 2: 51 in. (fully withdrawn)
  - Regulating Rod: **46.6 in. (118.364 ± 0.127 cm)** - 3% insertion

#### 2.5.3 Sample Basket Geometry

**Cold Dimensions:**
- Outer diameter: **5.4287 ± 0.0127 cm**
- Wall thickness: 0.079 cm INOR-8 plate
- Hole diameter: 0.238 cm
- Number of baskets: 3 (mounted vertically)

**Sample Configuration (per basket):**
- **Graphite samples:** 5 samples
  - Dimensions: 0.635 cm × 1.1938 cm cross-section
  - Length: 167.64 cm
- **INOR-8 samples:** 4 samples
  - Diameter: 0.635 cm
  - Length: 167.64 cm

**Function:** Periodic removal for investigation of material behavior in reactor environment

### 2.6 Reactor Vessel

#### 2.6.1 Main Vessel Body

**Cold Dimensions:**
- Inner diameter: 147.32 cm
- Height: 233.90 cm (cylindrical section)
- Wall thickness: 2.54 cm
- Material: INOR-8

**Hot Dimensions (911 K):**
- Inner diameter: ~148.66 cm (expanded)
- Wall thickness at inner surface: Variable with expansion

#### 2.6.2 Vessel Heads (Torispherical Domes)

**Upper Head (Upper Plenum):**
- Type: Torispherical dome
- Inner diameter: 147.32 cm (cold)
- Thickness: 2.54 cm
- Function: Upper plenum, fuel collection
- Contains: Flow distributor connection

**Lower Head (Lower Plenum):**
- Type: Torispherical dome
- Inner diameter: 147.32 cm (cold)
- Thickness: 2.54 cm
- Vertical section height: 6.475 ± 1.0 cm (hot)
- Function: Lower plenum, salt turning region
- Contains: 48 straightening vanes
- Simplification in benchmark: Homogeneous mixture, 90.8:9.2 volume ratio salt:INOR-8

#### 2.6.3 Flow Distributor

**Geometry:**
- Shape: Half-circular cross-section (half-torus)
- Inside radius: 10.16 cm
- Location: Top of vessel, connects to fuel inlet
- Connection: Tangential to vessel top
- Function: Distribute fuel evenly around circumference
- Flow path: Tangential entry → circumferential distribution → downward annulus

#### 2.6.4 Downcomer Annulus

**Dimensions (Hot):**
- Width: 2.54 cm (nominal) to 2.562 cm (hot)
- Location: Between core can and vessel wall
- Function: Downward spiral flow path for fuel salt
- Condition at criticality: Void (stationary salt)
- Flow vanes: 48 straightening vanes in lower plenum

#### 2.6.5 Outlet and Inlet Features

**Outlet Pipe:**
- Height: 36.180 ± 1.0 cm (hot)
- Thickness: 2.511 ± 0.25 cm
- Location: Top of vessel
- Function: Fuel exit from upper plenum

**Distributor:**
- Thickness: 0.826 ± 0.08 cm

**Upper Plenum Simplification:**
- Modeled as pure salt region (benchmark)
- Contains support ring with 36 lugs (welded to vessel wall)
- Support ring: Holds core can and graphite structure

### 2.7 Thermal Shield and Insulation

#### 2.7.1 Insulation Layer

**Material:** High-temperature insulation (vermiculite)
- **Composition:** Homogenized mixture of O, Fe, Al, H, Si, Ca
- **Thickness (cold):** 15.24 cm
- **Thickness (hot):** ~16.23 cm (estimated with expansion)
- **Location:** Between reactor vessel outer surface and thermal shield
- **Temperature:** 305 K
- **Function:** Thermal insulation, protect thermal shield

**Simplified in benchmark:** Homogeneous mixture with approximate composition

#### 2.7.2 Thermal Shield

**Material:** Type 304 stainless steel (primarily), with structural steel
- **Inner diameter:** ~236.22 cm
- **Outer diameter:** ~317.5 cm (158.75 cm radius)
- **Height:** 383.54 cm
- **Thickness:** Variable, multiple shell structure
- **Temperature:** 305 K (nominal), range 305-600 K
- **Function:** Support vessel, contain reactor furnace, radiation shielding

**Simplified in benchmark:** Homogeneous mixture representing average composition

**Support:** Reactor vessel supported from top removable cover of thermal shield

---

## 3. MATERIAL SPECIFICATIONS

### 3.1 Fuel Salt Composition

#### 3.1.1 Salt at First Criticality (June 1, 1965)

**Molar Composition:**
- LiF: **64.88 mol%**
- BeF₂: **29.27 mol%**
- ZrF₄: **5.06 mol%**
- UF₄: **0.79 mol%**

**Weight Composition (Benchmark):**
- Lithium (Li): **10.957 wt%**
- Beryllium (Be): **6.349 wt%**
- Zirconium (Zr): **11.101 wt%**
- Uranium (U): **4.495 wt%**
- Fluorine (F): **67.027 wt%**
- Impurities: **0.071 wt%**

**Total:** 100.000 wt%

**Physical Properties:**
- **Density:** 2.3275 ± 0.0160 g/cm³ at 911 K
- **Temperature:** 911 ± 1 K
- **Condition:** Stationary (not flowing) at criticality

#### 3.1.2 Uranium Isotopics

**Uranium Concentration in Salt:**
- **²³⁵U:** 1.409 ± 0.007 wt% of total salt (corrected book mass fraction)
- **²³⁴U:** 0.014 ± 0.007 wt% of total salt
- **²³⁶U:** 0.006 ± 0.006 wt% of total salt
- **²³⁸U:** Balance (remaining uranium)

**Uranium Enrichment:**
- **²³⁵U enrichment:** ~93% (in uranium fraction)
- **Total U in salt:** 4.495 wt%

**Dilution Correction:**
- Corrected for residual flush salt in freeze valves and drain tank heels

#### 3.1.3 Lithium Isotopics

**⁶Li Enrichment:**
- **⁶Li:** 0.005 ± 0.001 at.% in lithium
- **⁷Li:** Balance (>99.99 at.%)

**Sensitivity:** ⁶Li enrichment contributes ±172 pcm uncertainty to keff

#### 3.1.4 Carrier Salt Component Masses

**As-Loaded Masses:**
- **Beryllium mass:** 309.62 ± 5.00 kg
- **Zirconium mass:** 541.36 ± 5.00 kg

**Zirconium Impurity:**
- **Hafnium in Zr:** 0-50 ppm (affects reactivity by ~12 pcm)

#### 3.1.5 Salt Impurities

**Measured Impurities:**
- **Iron (Fe):** 162 ± 65 ppm
- **Chromium (Cr):** 28 ± 7 ppm
- **Nickel (Ni):** 30 ± 20 ppm
- **Oxygen (O):** 490 ± 49 ppm

**Total impurities:** ~0.071 wt%

**Impact:** Combined impurity uncertainty ~12 pcm on keff

#### 3.1.6 Helium Void and Salt Absorption

**Helium Void in Salt:**
- Range: 0 to 0.076 vol%
- Impact on keff: ~5 pcm

**Salt Absorption in Graphite:**
- Range: 0 to 0.0010 vol%
- Impact on keff: ~2 pcm

#### 3.1.7 Alternative Salt Compositions (Sensitivity Studies)

**Chemical Analysis Composition:**
- Li: 10.327 wt%, Be: 6.695 wt%, Zr: 11.016 wt%, U: 4.44 wt%, F: 67.451 wt%
- Expected keff: 1.02248 (116 pcm higher than benchmark)
- Note: Chemical analysis showed measurement bias for Li and Be

**Anticipated Composition:**
- Li: 10.97 wt%, Be: 6.324 wt%, Zr: 10.972 wt%, U: 4.641 wt%, F: 67.023 wt%
- Expected keff: 1.02595 (463 pcm higher than benchmark)

**Benchmark Selection:** Selected composition based on best agreement with recorded ²³⁵U mass fraction (1.409% vs 1.408 ± 0.007% recorded)

### 3.2 Graphite Specifications

#### 3.2.1 Physical Properties

**Density:**
- **Nominal:** 1.8507 g/cm³ (MSRE_Overview_Spec)
- **Alternative:** 1.86 g/cm³ (Berkeley paper reference)
- **Range:** 1.83 to 1.87 g/cm³
- **Uncertainty impact:** ±0.02 g/cm³ → ±334 pcm (largest contributor)

**Characteristics:**
- Lighter than fuel salt (salt: 2.3275 g/cm³)
- Buoyant when immersed in salt
- Average density from fabricated stringers

#### 3.2.2 Graphite Composition

**Major Component:**
- **Carbon:** >99.99 wt% (balance after impurities)

**Impurities (Benchmark Model):**
- **Boron (B):** 0.000080 ± 0.000008 wt% (0.8 ± 0.08 ppm)
- **Ash content:** 0.00050 ± 0.00005 wt% (5 ± 0.5 ppm)
- **Vanadium (V):** 0.00090 ± 0.00009 wt% (9 ± 0.9 ppm)
- **Sulfur (S):** 0.00050 ± 0.00005 wt% (5 ± 0.5 ppm)

**Uncertainty Impact:**
- Boron in graphite: ±17 pcm
- Ash/V/S combined: ~4 pcm

**Note:** Graphite impurity content and carbon cross-section accuracy are suspected contributors to typical 1-2% C-E discrepancy in graphite-moderated benchmarks

#### 3.2.3 Graphite Temperature

- **Operating temperature:** 911 ± 1 K (uniform in core)
- **Thermal shield graphite (if any):** 305 K
- **Thermal expansion coefficient:** 1.5 ± 0.2 × 10⁻⁶ °F⁻¹
- **Uncertainty impact of expansion coefficient:** ±18 pcm

### 3.3 INOR-8 (Hastelloy-N) Specifications

#### 3.3.1 Physical Properties

**Density:**
- **Nominal:** 8.7745 ± 0.0200 g/cm³
- **Temperature:** 911 K
- **Uncertainty impact:** ±3 pcm

#### 3.3.2 Composition

**Major Components (weight %):**
- **Nickel (Ni):** Balance (~70-71 wt%)
- **Molybdenum (Mo):** 17.0 ± 0.5 wt%
- **Chromium (Cr):** 7.0 ± 0.5 wt%
- **Iron (Fe):** 5.0 ± 0.5 wt%
- **Carbon (C):** 0.06 to 0.08 wt%

**Minor Elements:** Present but not fully specified in benchmark

**Uncertainty Impacts:**
- Mo variation: ±12 pcm
- Cr variation: ±5 pcm
- Fe variation: ±4 pcm
- C variation: ±5 pcm

**Applications:**
- Reactor vessel
- Core can
- Control rod thimbles
- Sample baskets
- Piping and structural components

**Thermal Expansion:**
- Coefficient: 7.8 ± 0.2 × 10⁻⁶ °F⁻¹
- Uncertainty impact: ±17 pcm

### 3.4 Control Rod Poison Material

#### 3.4.1 Composition

**Ceramic Mixture:**
- **Gadolinium oxide (Gd₂O₃):** 70 ± 1 wt%
- **Aluminum oxide (Al₂O₃):** 30 ± 1 wt%

**Uncertainty impact:**
- Gd₂O₃ fraction: ±0.6 pcm

#### 3.4.2 Physical Properties

**Density:**
- **Nominal:** 5.873 ± 0.020 g/cm³
- **Uncertainty impact:** ±0.5 pcm

**Form:**
- Thin-walled ceramic cylinders
- Canned in Inconel shell
- 3 cylinders per control rod element
- 38 elements per control rod

**Poison Section:**
- Total length: 150.774 cm (hot)
- Position at criticality: Regulating rod at 118.364 cm (46.6 in.)

### 3.5 Structural Materials

#### 3.5.1 Type 304 Stainless Steel (Thermal Shield)

**Composition (typical):**
- Fe: ~68-70 wt% (balance)
- Cr: ~18-20 wt%
- Ni: ~8-10 wt%
- Mn: <2 wt%
- C: <0.08 wt%
- Other: <1 wt%

**Density:** ~7.9 g/cm³

**Temperature:** 305 K (nominal), range 305-600 K

**Simplified in benchmark:** Homogeneous mixture representing average composition

#### 3.5.2 Inconel (Control Rod Components)

**Similar to INOR-8:**
- Ni-based superalloy
- Used in control rod shells and cables
- Properties similar to INOR-8

#### 3.5.3 Stainless Steel (Control Rod Hose)

**Type:** Helically wound flexible hose
- OD: 1.905 cm
- ID: 1.5875 cm
- Material: Austenitic stainless steel

### 3.6 Insulation Material

#### 3.6.1 Vermiculite Insulation

**Type:** High-temperature insulation
**Thickness:** 15.24 cm (cold)

**Composition (simplified):**
- Elements: O, Fe, Al, H, Si, Ca
- Proportions: Not precisely specified
- Simplified as homogeneous mixture

**Temperature:** 305 K

**Density:** Not specified (low density, insulating material)

**Function:** Thermal insulation between reactor vessel and thermal shield

### 3.7 Void Regions and Gas

#### 3.7.1 Downcomer Annulus

**Condition at criticality:** Void (no flowing salt)
**Width:** 2.54-2.56 cm
**Material:** Helium atmosphere (cell gas)

#### 3.7.2 Cell Atmosphere

**Composition:** Helium gas
**Pressure:** Atmospheric (implied)
**Temperature:** Variable (305 K in shield region, 911 K near core)

**Note:** Gas composition (mass fraction vs atom fraction) has negligible impact (<1 pcm)

---

## 4. OPERATING CONDITIONS AND PHYSICS

### 4.1 Temperature Distribution

#### 4.1.1 Core Region (911 K)

**Uniform Temperature:** 911 ± 1 K (1181°F)

**Components at 911 K:**
- Fuel salt
- Graphite (all core graphite)
- INOR-8 (vessel, core can, control rod thimbles, sample baskets)
- Control rod poison material
- All materials within reactor vessel

**Uncertainty:**
- Temperature: ±1 K
- Impact on keff from fuel salt temp: ±6 pcm
- Impact on keff from graphite temp: ±1 pcm

#### 4.1.2 Thermal Shield Region (305 K)

**Temperature:** 305 K (90°F nominal)

**Components at 305 K:**
- Thermal shield (stainless steel)
- Insulation (vermiculite)
- Any graphite in thermal shield region

**Temperature Range:**
- Nominal: 305 K
- Possible range: 305-600 K
- Impact on keff from range: ±2 pcm

### 4.2 Power and Neutron Source

#### 4.2.1 Criticality Conditions

**Power Level:** ~10 W (zero power)
**Salt Condition:** Stationary (not flowing)
**Configuration:** Isothermal, uniform temperature

**Verification Method:**
- Neutron multiplication measured
- Power leveled at successively higher levels with same rod position
- Stable critical configuration

#### 4.2.2 Neutron Detection

**Counting Channels:** 4 channels used during experiment
1. Fission chamber #1 in instrument shaft
2. Fission chamber #2 in instrument shaft
3. BF₃ chamber in instrument shaft
4. BF₃ chamber in thermal shield

**Purpose:** Monitor source multiplication during approach to criticality

### 4.3 Control Rod Configuration

#### 4.3.1 Position at Criticality

**Control Rod 1:**
- Position: 51 in. (129.54 cm) - **Fully withdrawn**
- Worth: Not inserted

**Control Rod 2:**
- Position: 51 in. (129.54 cm) - **Fully withdrawn**
- Worth: Not inserted

**Regulating Rod:**
- Position: **46.6 in. (118.364 ± 0.127 cm)**
- Insertion: **3% of integral worth**
- Uncertainty: ±0.127 cm → ±0.7 pcm

**Position Reference:**
- 0 in. = Fully inserted (poison at bottom of active core)
- 51 in. = Fully withdrawn (poison above active core)

#### 4.3.2 Control Rod Worth

**Regulating rod at criticality:**
- 3% insertion = small negative reactivity
- Balances excess reactivity to achieve keff = 1.000

**Note:** Exact differential and integral worth values not provided in benchmark specification

### 4.4 Design Power Operation (Not Modeled)

**Note:** First criticality was at zero power. Full power operation characteristics:
- Design power: 10 MWth
- Fuel circulation rate: 4.54 m³/min
- Heat removal via coolant salt to air
- Not applicable to this benchmark

---

## 5. BENCHMARK MODEL REQUIREMENTS

### 5.1 Nuclear Data Libraries

#### 5.1.1 Primary Library

**Library:** ENDF/B-VII.1
**Application:** All neutron cross sections
**Expected keff:** 1.02132 ± 0.00003

**Cross-Section Temperature:**
- Base temperature: 900 K
- Preprocessed to 911 K (Doppler broadening)
- Method: MCNP TMP card or equivalent

#### 5.1.2 Thermal Scattering Laws

**Carbon in Graphite (core):**
- Temperature: 911 K
- S(α,β) library: grph (graphite thermal scattering)
- Interpolation: Between 800 K and 1000 K libraries
- Sensitivity: ±100 K → ~600 pcm change in keff

**Carbon in Graphite (thermal shield, if present):**
- Temperature: 305 K
- S(α,β) library: grph

**Hydrogen in Water (insulation):**
- Temperature: 305 K
- S(α,β) library: lwtr (light water thermal scattering)
- Note: H in vermiculite insulation

**Importance:** Thermal scattering treatment is CRITICAL. Must use accurate temperature libraries.

#### 5.1.3 Alternative Libraries (Sensitivity Studies)

**JENDL-4.0:**
- Expected keff: 1.02061 ± 0.00003
- Difference from ENDF-VII.1: 71 ± 5 pcm

**Carbon-only JENDL-4.0:**
- Expected impact: -178 ± 5 pcm vs ENDF-VII.1
- Indicates strong sensitivity to carbon data

### 5.2 Criticality Calculation Parameters

#### 5.2.1 MCNP KCODE Recommended Settings

**Suggested Parameters:**
```
KCODE 100000 1.0 50 250
```
- Histories per cycle: 100,000
- Initial guess keff: 1.0
- Skip cycles: 50 (discard for source convergence)
- Active cycles: 200-250 (for statistics)

**Source Definition:**
- KSRC: Distribute initial source points in fuel salt regions
- Multiple points for good spatial coverage
- Avoid point sources (use spatial distribution)

**Expected Convergence:**
- Shannon entropy should stabilize within 20-50 cycles
- Fission source distribution should converge
- keff std dev: <0.00003 (30 pcm) achievable

#### 5.2.2 Statistical Requirements

**Target Uncertainties:**
- keff: ±0.00003 (±30 pcm) or better
- Statistical confidence: 1σ
- Figure of Merit: Monitor for stability

**Convergence Checks:**
- Shannon entropy (stable and flat)
- keff by cycle (no trends)
- Fission source distribution (converged)

### 5.3 Quality Assurance Requirements

#### 5.3.1 Geometry Verification

**Required Checks:**
1. Visual rendering (MCNP plotter or VISED)
   - Horizontal cross-section at z = 145.396 cm
   - Vertical cross-section at y = 0 (offset to show control rods)
   - Core center detail

2. Volume calculations
   - All cells should have reasonable volumes
   - Total fuel salt volume ~4-5 m³ (estimate)
   - Graphite volume ~10-12 m³ (estimate)

3. Lost particle check
   - Must be ZERO lost particles
   - Any lost particles indicate geometry errors

4. Cell overlap check
   - Use MCNP geometry debugger
   - No overlapping cells

#### 5.3.2 Material Verification

**Required Checks:**
1. Atom density calculations
   - Verify salt composition from weight % to atoms/barn-cm
   - Check uranium enrichment
   - Verify ⁶Li enrichment

2. Mass inventory
   - Total uranium mass ~X kg (calculate from density, volume, wt%)
   - Check against experimental values

3. Isotopic abundances
   - ²³⁵U should be ~93% of uranium
   - Natural isotopics for other elements (except Li)

4. Material temperature assignments
   - All core materials: 911 K
   - Thermal shield: 305 K
   - TMP cards correctly applied

#### 5.3.3 Physics Verification

**Required Checks:**
1. Neutron balance
   - Total production = total loss + leakage
   - Should close within statistics

2. Shannon entropy
   - Must converge and remain stable
   - Typical range: 7-8 for large systems

3. Source distribution
   - Should be peaked in center of core
   - Symmetric distribution

4. Comparison to benchmark
   - keff = 1.02132 ± 0.00003 (target for Serpent/ENDF-VII.1)
   - Discrepancy from 1.0000 expected at 2.154%

---

## 6. UNCERTAINTY ANALYSIS

### 6.1 Experimental Uncertainties

#### 6.1.1 Major Contributors (>50 pcm)

| Parameter | Nominal Value | Uncertainty | Δk (pcm) |
|-----------|---------------|-------------|----------|
| Graphite density | 1.86 g/cm³ | ±0.02 g/cm³ | ±334 |
| Fuel salt density | 2.3275 g/cm³ | ±0.0160 g/cm³ | ±103 |
| ⁶Li enrichment | 0.005 at.% | ±0.001 at.% | ±172 |
| ²³⁵U mass fraction | 1.409 wt% | ±0.007 wt% | ±81 |
| ²³⁴U mass fraction | 0.014 wt% | ±0.007 wt% | ±74 |
| Fuel channel width | 1.018 cm | ±0.0127 cm | ±51 |

#### 6.1.2 Moderate Contributors (10-50 pcm)

| Parameter | Nominal Value | Uncertainty | Δk (pcm) |
|-----------|---------------|-------------|----------|
| Fuel channel length | 3.053 cm | ±0.0127 cm | ±23 |
| Graphite core height | 166.724 cm | ±1.0 cm | ±21 |
| Thermal expansion coeff (graphite) | 1.5×10⁻⁶ °F⁻¹ | ±0.2×10⁻⁶ | ±18 |
| Thermal expansion coeff (INOR-8) | 7.8×10⁻⁶ °F⁻¹ | ±0.2×10⁻⁶ | ±17 |
| ²³⁶U mass fraction | 0.006 wt% | ±0.006 wt% | ±17 |
| Boron in graphite | 0.00008 wt% | ±0.000008 wt% | ±17 |
| Graphite stringer width | 5.084 cm | ±0.0127 cm | ±13 |
| Be mass in carrier salt | 309.62 kg | ±5.0 kg | ±8 |
| Zr mass in carrier salt | 541.36 kg | ±5.0 kg | ±12 |
| Mo in INOR-8 | 17.0 wt% | ±0.5 wt% | ±12 |
| Impurities in salt | Various | Various | ±12 |
| Hf in Zr | 0-50 ppm | 25 ppm | ±12 |

#### 6.1.3 Minor Contributors (<10 pcm)

All other geometric, material, and operating condition uncertainties contribute <10 pcm individually.

#### 6.1.4 Total Experimental Uncertainty

**Root-mean-square combination:** ±420 pcm (1σ)

**Measurement Uncertainty:** ±10 pcm (in keff determination)

### 6.2 Nuclear Data Uncertainties

#### 6.2.1 Cross-Section Sensitivity Coefficients

**Major Sensitivities (×10⁻⁵):**

| Nuclide | Reaction | Sensitivity | Impact |
|---------|----------|-------------|--------|
| ²³⁵U | ν (neutrons/fission) | +22,990 | High |
| ²³⁵U | Fission | +37,020 | Very high |
| ²³⁵U | Capture (n,γ) | -14,080 | High |
| ¹⁹F | Elastic | +8,410 | High |
| natC | Elastic | +51,400 | Extreme |
| natC | Capture | -1,760 | Moderate |
| ⁹Be | Elastic | +2,920 | Moderate |
| ⁹Be | Capture | -340 | Low |
| ⁶Li | Capture | -1,430 | High |
| ⁷Li | Elastic | +770 | Moderate |
| ⁷Li | Capture | -1,380 | Moderate |

**Note:** Carbon elastic scattering has extreme sensitivity due to large graphite mass in core.

#### 6.2.2 Major Nuclear Data Uncertainty Contributors

**From Covariance Data (56-group):**

| Source | Uncertainty (pcm) |
|--------|-------------------|
| ²³⁵U, ν | 373 |
| Carbon, elastic | 264 |
| ²³⁵U, χ (fission spectrum) | 257 |
| ⁷Li(n,γ) | 197 |
| ²³⁵U(n,γ) | 172 |
| ¹⁹F elastic × ²³⁵U(n,γ) correlation | 150 |
| ²³⁵U(n,f) | 128 |
| ⁵⁸Ni(n,γ) | 120 |
| ¹⁹F inelastic | 97 |
| Others | <100 each |

#### 6.2.3 Total Nuclear Data Uncertainty

**Root-mean-square combination:** ±664 pcm (1σ)

**Note:** Larger than experimental uncertainty, dominated by carbon elastic and ²³⁵U data

### 6.3 Model Simplification Bias

#### 6.3.1 Neglected Components

**Components Omitted from Benchmark Model:**
- Fuel inlet pipe
- Fuel outlet pipe (detailed geometry)
- Fuel outlet strainer
- Reactor access port
- External primary loop
- Thermal shield base details

**Combined Bias:** -22 ± 5 pcm

**Justification:** Components outside thermal shield have negligible impact on core neutronics

#### 6.3.2 Simplified Model Variations (Not Recommended)

If simplified models are used, biases are:

| Simplification | Bias (pcm) | Cumulative keff |
|----------------|------------|-----------------|
| Reference (full detail) | 0 | 1.02132 |
| Remove flow distributor | -98 | 1.02032 |
| Flat vessel heads | +243 | 1.02380 |
| Homogenize sample baskets | -37 | 1.02094 |
| Replace baskets with graphite | +1623 | 1.03790 |
| Circular fuel channels | +311 | 1.02450 |
| Rectangular fuel channels | +19 | 1.02151 |
| Remove thermal shield | -885 | 1.01228 |

**Note:** These simplifications are NOT recommended for MCNP validation. Included only for comparison to other codes.

### 6.4 Total Uncertainty Budget

**Experimental (input) uncertainty:** ±420 pcm
**Nuclear data uncertainty:** ±664 pcm
**Model bias:** -22 ± 5 pcm

**Expected benchmark keff:** 0.99978 ± 0.00420 (experimental)
**Calculated keff (Serpent/ENDF-VII.1):** 1.02132 ± 0.00003 (statistical)
**C-E discrepancy:** 2154 ± 420 pcm (5.1σ)

**Note:** Large C-E discrepancy is typical of graphite-moderated systems (1-2% common). Attributed to:
1. Graphite impurity characterization uncertainties
2. Carbon capture cross-section uncertainties
3. Thermal scattering data uncertainties

---

## 7. MODELING RECOMMENDATIONS

### 7.1 Geometry Modeling Strategy

#### 7.1.1 Coordinate System

**Recommended:**
- Origin: On axis at bottom of horizontal graphite lattice (z = 0)
- Axis: Vertical (z-axis)
- Symmetry: Cylindrical (rotational symmetry except control rods/sample baskets)

#### 7.1.2 Surface Definitions

**Radial Surfaces (cylinders):**
1. Graphite lattice outer: 70.285 cm
2. Core can inner: 71.097 cm
3. Core can outer: 71.737 cm
4. Vessel inner: 74.299 cm
5. Vessel outer: 75.741 cm (active), 76.862 cm (full)
6. Insulation outer: ~93.09 cm
7. Thermal shield boundaries: Multiple cylinders

**Axial Surfaces (planes):**
1. Bottom of horizontal lattice: z = 0
2. Top of horizontal lattice: z ≈ 2.5-4 cm
3. Top of vertical stringers: z = 170.311 cm
4. Top of core can: z = 174.219 cm
5. Various plenum boundaries

**Complex Surfaces:**
- Torispherical heads: Sphere + torus combinations
- Flow distributor: Half-torus
- Fuel channel corners: Torus sections for rounding

#### 7.1.3 Lattice Strategy

**Option 1: Explicit Lattice (Recommended)**
- Use MCNP LAT=1 (hexagonal) or manual universe/fill
- Define unit cell: 1 graphite stringer + surrounding fuel channels
- Repeat in array pattern
- Handle partial stringers at edge explicitly

**Option 2: Homogenized Core (Not Recommended)**
- Homogenize graphite and fuel salt
- Preserve volume fractions
- Much simpler but loses spatial detail
- Only for scoping calculations

**Recommended:** Use Option 1 (explicit lattice) for validation

### 7.2 Material Modeling Strategy

#### 7.2.1 Fuel Salt

**Method:**
1. Convert weight % to atom densities
2. Use MCNP M card with isotopes
3. Apply ⁶Li and ⁷Li explicitly
4. Add uranium isotopes (²³⁴U, ²³⁵U, ²³⁶U, ²³⁸U)
5. Include impurities if sensitivity studied

**Example Structure (pseudo-code):**
```
M1    3006  X.XXXE-XX    $ Li-6
      3007  X.XXXE-XX    $ Li-7
      4009  X.XXXE-XX    $ Be-9
      9019  X.XXXE-XX    $ F-19
      40000 X.XXXE-XX    $ Zr-nat
      92234 X.XXXE-XX    $ U-234
      92235 X.XXXE-XX    $ U-235
      92236 X.XXXE-XX    $ U-236
      92238 X.XXXE-XX    $ U-238
```

#### 7.2.2 Graphite

**Method:**
1. Natural carbon (6000) or C-12 explicitly
2. Include boron impurity (10010, 10011, or 5000)
3. Density: 1.8507 g/cm³
4. Apply thermal scattering: MT1 GRPH.XX (XX = temperature ID)

**Example:**
```
M2    6000  X.XXXE-XX    $ Natural carbon
      5000  X.XXXE-XX    $ Boron (natural)
MT2   GRPH.12T           $ Graphite S(a,b) at 900K, interpolate to 911K
```

#### 7.2.3 INOR-8

**Method:**
1. Define all major constituents (Ni, Mo, Cr, Fe, C)
2. Use natural isotopics (28000, 42000, 24000, 26000, 6000)
3. Density: 8.7745 g/cm³

**Example:**
```
M3    28000 X.XXXE-XX    $ Nickel (balance)
      42000 X.XXXE-XX    $ Molybdenum
      24000 X.XXXE-XX    $ Chromium
      26000 X.XXXE-XX    $ Iron
      6000  X.XXXE-XX    $ Carbon
```

#### 7.2.4 Control Rod Poison

**Method:**
1. Define Gd₂O₃ and Al₂O₃
2. Use natural gadolinium (64000) or explicit isotopes
3. Density: 5.873 g/cm³

**Example:**
```
M4    64000 X.XXXE-XX    $ Gadolinium (from Gd2O3)
      8016  X.XXXE-XX    $ Oxygen (from Gd2O3 and Al2O3)
      13027 X.XXXE-XX    $ Aluminum (from Al2O3)
```

### 7.3 Physics Modeling Strategy

#### 7.3.1 Temperature Treatments

**MCNP TMP Card:**
- Fuel salt cells: TMP=911K → 7.878E-08 MeV
- Graphite cells (core): TMP=911K
- INOR-8 cells (core): TMP=911K
- Thermal shield: TMP=305K → 2.639E-08 MeV

**Thermal Scattering:**
- MT card for each graphite material at appropriate temperature
- MT card for hydrogen in insulation (lwtr.XX)

#### 7.3.2 Source Definition

**KSRC Card:**
- Define 20-50 initial source points
- Distribute spatially in fuel salt regions
- Cover radial and axial extent
- Avoid clustering

**Example:**
```
KSRC  0 0 85    $ Center of core, mid-height
      30 0 85   $ Off-center points
      -30 0 85
      0 30 100
      0 -30 70
      [... more points ...]
```

#### 7.3.3 Cross-Section Libraries

**MCNP ENDF/B-VII.1:**
- Use .80c or .81c libraries (if available)
- Ensure DATAPATH set correctly
- Verify thermal scattering libraries available

**XSDIR:**
- Check XSDIR file for available temperatures
- Graphite thermal scattering: grph.10t (800K), grph.12t (1000K), etc.

### 7.4 Validation Checklist

**Before Running:**
- [ ] All dimensions match hot (911K) specifications
- [ ] All material compositions verified against tables
- [ ] Temperature assignments correct (911K core, 305K shield)
- [ ] Thermal scattering applied to graphite and H
- [ ] KCODE parameters set (50 skip, 200+ active, 100k histories)
- [ ] Multiple KSRC points distributed in fuel
- [ ] All cells defined (no gaps)
- [ ] All surfaces referenced

**After Running:**
- [ ] Zero lost particles
- [ ] Shannon entropy converged
- [ ] keff ≈ 1.021 ± 0.003
- [ ] Statistical uncertainty < 0.00005
- [ ] Neutron balance closed
- [ ] Visual plots match literature figures
- [ ] Mass inventory reasonable

---

## 8. EXPECTED RESULTS AND ACCEPTANCE CRITERIA

### 8.1 Primary Observables

#### 8.1.1 Eigenvalue (keff)

**Expected Values:**
- **MCNP/ENDF-VII.1:** 1.021 ± 0.003 (acceptable range)
- **Serpent reference:** 1.02132 ± 0.00003
- **Experimental:** 1.0000 (by definition)
- **C-E discrepancy:** 2.1-2.2% (expected)

**Acceptance Criteria:**
- Statistical uncertainty: <0.00005 (50 pcm)
- Agreement with Serpent reference: ±200 pcm
- C-E discrepancy: 1.5-2.5% (typical for graphite systems)

#### 8.1.2 Neutron Balance

**Expected:**
- Absorption: ~60-70% (fuel absorption + parasitic)
- Leakage: ~30-40% (despite thick reflector)
- Production: Balances losses within statistics

**Acceptance:**
- Neutron balance closes (production = loss + leakage)
- No unexplained losses

#### 8.1.3 Spatial Distribution

**Expected:**
- Fission source peaked at core center
- Radial flux: Peaked at center, falling toward reflector
- Axial flux: Peaked at mid-plane, falling at top/bottom
- Flux spectrum: Thermal peak in graphite, fast peak in salt

### 8.2 Convergence Criteria

#### 8.2.1 Shannon Entropy

**Expected:**
- Initial: Variable (depends on source distribution)
- Converged: Stable within 20-50 cycles
- Value: ~7-8 (typical for large systems)

**Acceptance:**
- Flat after skip cycles
- No trends in active cycles
- Sufficient skip cycles (50+ recommended)

#### 8.2.2 keff Stability

**Expected:**
- Initial: May vary significantly
- After convergence: Fluctuates around mean
- Trend: No systematic drift

**Acceptance:**
- keff by cycle shows random fluctuations only
- No monotonic trends
- Standard deviation decreases as 1/√N

### 8.3 Sensitivity Study Results

#### 8.3.1 Nuclear Data Libraries

**JENDL-4.0 vs ENDF-VII.1:**
- Expected difference: 71 ± 5 pcm
- JENDL-4.0 lower

**Carbon JENDL-4.0:**
- Expected difference: -178 ± 5 pcm
- Demonstrates carbon sensitivity

#### 8.3.2 Salt Composition

**Chemical analysis composition:**
- Expected: +116 pcm vs benchmark

**Anticipated composition:**
- Expected: +463 pcm vs benchmark

#### 8.3.3 Thermal Scattering

**Graphite at 800K:**
- Expected: +591 pcm vs 911K

**Graphite at 1000K:**
- Expected: -492 pcm vs 911K

**Note:** Extreme sensitivity demonstrates importance of accurate S(α,β) temperature

### 8.4 Quality Metrics

#### 8.4.1 Geometry Quality

**Lost Particles:**
- Requirement: ZERO
- Any lost particles indicate geometry error

**Cell Volumes:**
- Fuel salt: ~4-5 m³
- Graphite: ~10-12 m³
- All cells positive volumes

#### 8.4.2 Statistical Quality

**keff Uncertainty:**
- Target: <0.00005
- Minimum: <0.0001

**Figure of Merit:**
- Should increase with run time
- Indicates good sampling

**Relative Error:**
- keff: <0.005%

---

## 9. REFERENCES

### 9.1 Primary Sources

1. **Shen, D., Ilas, G., Powers, J.J., and Fratoni, M.** (2021). "Reactor Physics Benchmark of the First Criticality in the Molten Salt Reactor Experiment," *Nuclear Science and Engineering*, 195:8, 825-837. DOI: 10.1080/00295639.2021.1880850

2. **Bess, J.D. et al.** (2019). "The 2019 Edition of the IRPhEP Handbook," INL/CON-19-53745-Rev000, Idaho National Laboratory.

3. **Robertson, R.C.** (1965). "MSRE Design and Operations Report Part I: Description of Reactor Design," ORNL-TM-728, Oak Ridge National Laboratory.

4. **Prince, B.E. et al.** (1968). "Zero-Power Physics Experiments on the Molten-Salt Reactor Experiment," ORNL-4233, Oak Ridge National Laboratory.

5. **Haubenreich, P.N. et al.** (1964). "MSRE Design and Operations Report Part III: Nuclear Analysis," ORNL-TM-730, Oak Ridge National Laboratory.

6. **Thoma, R.E.** (1971). "Chemical Aspects of MSRE Operation," ORNL-4658, Oak Ridge National Laboratory.

### 9.2 Related Benchmarks

**Other Graphite-Moderated System Benchmarks (IRPhEP):**
- HTR-10 (high-fidelity and simplified)
- HTTR (fully loaded)
- PROTEUS Core 3

**Observation:** All show 1-2% C-E discrepancy with calculated keff higher than experimental.

### 9.3 Code References

**Serpent 2:**
- Leppänen, J. et al. (2013). "The Serpent Monte Carlo Code: Status, Development and Applications in 2013," *Ann. Nucl. Energy*, 82, 142-150.

**SCALE:**
- Wieselquist, W.A., Lefebvre, R.A., and Jessee, M.A. (2020). "SCALE Code System," ORNL/TM-2005/39, Version 6.2.4, Oak Ridge National Laboratory.

---

## 10. DOCUMENT REVISION HISTORY

**Version 1.0** - Initial release for MCNP model development
- Compiled from MSRE_Overview_Spec.md and msre-benchmark-berkeley.md
- All specifications extracted for production-quality MCNP modeling
- Comprehensive uncertainty analysis included
- Validation requirements defined

---

**END OF SPECIFICATION**

**Note to Modelers:** This specification is comprehensive but complex. It is recommended to:
1. Start with the full-detail model (no simplifications)
2. Verify each component systematically
3. Use thermal expansion corrections
4. Apply proper thermal scattering treatments
5. Compare results to Serpent reference (1.02132)
6. Expect 2.1% C-E discrepancy (normal for graphite systems)

Good luck with your MCNP modeling!
