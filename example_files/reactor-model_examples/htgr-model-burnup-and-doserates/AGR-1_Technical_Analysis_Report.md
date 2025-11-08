# Technical Documentation Analysis Report: AGR-1 HTGR Shutdown Dose Rate Calculations

## Document Information

- **Title**: Shutdown dose rate calculations in high-temperature gas-cooled reactors using the MCNP-ORIGEN activation automation tool
- **Authors**: Fairhurst-Agosta, Roberto; Kozlowski, Tomasz
- **Organization**: Dept. of Nuclear, Plasma, and Radiological Engineering, University of Illinois at Urbana-Champaign
- **Publication**: Nuclear Science and Technology Open Research, 2024
- **DOI**: 10.12688/nuclscitechnolopenres.17447.2
- **Document Type**: Peer-reviewed research article (Version 2, approved)
- **Relevance**: Critical resource for MCNP modeling of HTGR systems with TRISO fuel, shutdown dose rate calculations, and coupled MCNP-ORIGEN depletion/activation workflows

---

## Executive Summary

This article introduces a novel shutdown dose rate calculation capability for High-Temperature Gas-Cooled Reactors (HTGRs) that explicitly models TRistructural ISOtropic (TRISO) particles as decay radiation sources using the MCNP-ORIGEN Activation Automation (MOAA) tool and MCNP repeated structures. The methodology addresses the unique challenge of HTGR fuel double heterogeneity and provides detailed specifications for the AGR-1 irradiation experiment and a microreactor (μHTGR) design. The work demonstrates that 3-month cool-down periods may be insufficient for safe decommissioning activities, with dose rates above 40 mSv/h calculated at reactor citadel level.

---

## 1. GEOMETRY SPECIFICATIONS

### 1.1 AGR-1 Experiment Geometry

**Experiment Configuration:**
- **Location**: B-10 hole in ATR (Advanced Test Reactor)
- **Test train**: Six cylindrical capsules vertically stacked
- **Total compacts**: 72 compacts (3 columns × 4 compacts per column × 6 capsules)
- **Irradiation period**: 13 power cycles (~3 years)

**ATR Reactor Geometry:**
- **Power level**: 250 MWth high flux test reactor
- **Core configuration**: 40 fuel elements in serpentine annulus around 9 flux traps
- **Fuel element design**: 19 parallel, curved, aluminum-clad fuel plates per element (45° sector of right circular cylinder)
- **Core shape**: Clover-leaf configuration enabling independent lobe power levels
- **Modeling approach**: Quarter model representing core east quadrant with fuel plates grouped into 3 radial zones

**AGR-1 Capsule Components:**
- Hafnium (Hf) shroud: Surrounds entire capsule circumference
- Bottom support: SS316L
- Inner wall: SS316L
- Top support: SS316L
- Outer wall: SS316L
- Low graphite spacer
- Upper graphite spacer
- Borated graphite holder
- Three columns of fuel compacts (4 compacts per column)

**Compact Variants:**
- Four different compact types (Baseline, Variant 1, Variant 2, Variant 3)
- Capsule 3 & 6: Baseline compact
- Capsule 5: Variant 1
- Capsule 2: Variant 2
- Capsule 1 & 4: Variant 3
- Variant differences: Particle layer thickness and density variations, different number of embedded particles

**Model Simplifications:**
- Hf shroud modeled as surrounding full capsule circumference
- Gas lines, thermocouples, and thru-tubes neglected
- TRISO particles arranged in regular lattice (not random)

### 1.2 μHTGR (Microreactor) Geometry

**Core Layout:**
- **Total assemblies**: 37 assemblies (24 fuel + 12 control + 1 reserved shutdown)
- **Assembly pitch**: 30 cm
- **Axial configuration**: 4 layers stacked vertically
- **Total core height**: 4 × 68 cm = 272 cm (active core)

**Assembly Details:**
- **Assembly height**: 68 cm
- **Fuel channel radius**: 1.15 cm
- **Coolant channel radius**: 0.775 cm
- **Channel pitch**: 3.2 cm
- **Control assembly**: 4 cm radius control rod hole
- **Reserved shutdown assembly**: 6 cm radius control rod hole

**Reflector Specifications:**
- **Radial reflector radius**: 134 cm
- **Radial reflector height**: Not explicitly stated (matches core configuration)
- **Bottom reflector height**: 68 cm
- **Top reflector height**: 68 cm
- **Material**: Graphite (density: 1.75 g/cm³)

**Shielding and Facility Geometry:**
- **Concrete cavity wall**: Portland concrete (2.3 g/cm³)
  - Distance from radial reflector: 191 cm
  - Wall thickness: 100 cm
- **Citadel floor**: Portland concrete (2.3 g/cm³)
  - Thickness: 70 cm
  - Distance from reactor top to ground level: 700 cm
- **Cavity atmosphere**: Air (80 vol% N₂, 20 vol% O₂)
- **RPV side wall**: Neglected in model

**Dose Point Geometry (Reference Man):**
- **Mass**: 70 kg
- **Height**: 170 cm
- **Representation**: Equivalent cylinder
- **Density**: 0.985 g/cm³
- **Equivalent cylinder radius**: 11.53 cm
- **Location**: Ground level on citadel floor above exposed reactor core

---

## 2. TRISO PARTICLE FUEL DESIGN

### 2.1 TRISO Particle Layer Structure (Table 5 - μHTGR Design)

Complete 5-layer coating system (from inner to outer):

| Layer | Thickness (cm) | Material | Density (g/cm³) | Radius (cm) |
|-------|---------------|----------|-----------------|-------------|
| Kernel | 0.0250 (radius) | UO₂ (ε=19.75%) | 10.8 | 0.0250 |
| Buffer | 0.0100 | C (porous carbon) | 0.98 | 0.0350 |
| IPyC | 0.0040 | C (Inner PyC) | 1.85 | 0.0390 |
| SiC | 0.0035 | SiC | 3.20 | 0.0425 |
| OPyC | 0.0040 | C (Outer PyC) | 1.86 | 0.0465 |

**Total TRISO particle outer radius**: 0.0465 cm (465 μm)

**Key TRISO Design Features:**
- **Kernel enrichment**: 19.75% U-235 in UO₂
- **Kernel density**: 10.8 g/cm³ (near-theoretical density)
- **Buffer layer**: Low-density porous carbon for fission gas accommodation
- **IPyC layer**: Dense pyrolytic carbon seal and mechanical support
- **SiC layer**: Primary pressure vessel and fission product retention barrier
- **OPyC layer**: Protective outer coating and bonding surface

### 2.2 Fuel Compact Specifications

**Compact Material and Properties:**
- **Matrix material**: SiC (Silicon Carbide)
- **Matrix density**: 3.2 g/cm³
- **TRISO packing fraction**: 40% by volume
- **Particle distribution**: Uniform (modeled assumption)
- **Particle pitch**: 0.1 cm (center-to-center spacing)

**AGR-1 Compact Configuration:**
- **Four compact variants** with differing particle layer properties
- **Kernel composition**: Same across all variants (not explicitly stated but implied UCO for AGR-1 baseline)
- **Number of particles per compact**: Varies by variant type

### 2.3 Fuel Assembly Configuration (μHTGR)

- **Fuel compacts**: Column of SiC compacts filling each fuel channel
- **Compact height**: Not explicitly stated
- **Number of compacts per column**: Not explicitly stated
- **Total fuel channels per assembly**: Calculated from 3.2 cm pitch within assembly

---

## 3. MATERIAL COMPOSITIONS

### 3.1 Fuel Materials

**TRISO Kernel (UO₂):**
- **Composition**: UO₂ with 19.75% U-235 enrichment
- **Density**: 10.8 g/cm³
- **Form**: Ceramic oxide kernel
- **Note**: AGR-1 baseline used UCO (uranium oxycarbide) fuel, but μHTGR example uses UO₂

**Coating Layers:**
- **Buffer**: Porous carbon (C), 0.98 g/cm³
- **IPyC**: Dense pyrolytic carbon (C), 1.85 g/cm³
- **SiC**: Silicon carbide, 3.20 g/cm³
- **OPyC**: Dense pyrolytic carbon (C), 1.86 g/cm³

**Compact Matrix:**
- **Material**: SiC (Silicon Carbide)
- **Density**: 3.2 g/cm³
- **Homogenized composition**: 40% TRISO particles + 60% SiC matrix

### 3.2 Structural Materials

**Stainless Steel (SS316L):**
- Used for: Bottom support, inner wall, top support, outer wall
- **Density**: Not explicitly stated (standard ~8.0 g/cm³)
- **Activation significance**: Contributes 42.54% of photon source at 365 days decay

**Graphite:**
- **Density (assemblies & reflectors)**: 1.75 g/cm³
- **Applications**:
  - Low graphite spacer
  - Upper graphite spacer
  - Bottom/top/radial reflectors
  - Assembly matrix material
- **Activation significance**: ~8 orders of magnitude lower than fuel contribution

**Borated Graphite:**
- Used for: Compact holders
- **Density**: 1.75 g/cm³ (assumed same as graphite)
- **Boron content**: Not explicitly stated
- **Purpose**: Neutron absorption/control

**Hafnium (Hf):**
- **Application**: Shroud surrounding AGR-1 capsules
- **Density**: Not explicitly stated
- **Activation significance**:
  - 41.64% contribution at 1 day
  - 62.11% contribution at 30 days (peak)
  - 0.50% contribution at 365 days (significant decay)
- **Note**: Hf isotope growth between 1-30 days then rapid decay

### 3.3 Shielding Materials

**Portland Concrete:**
- **Density**: 2.3 g/cm³
- **Applications**: Cavity walls, citadel floor
- **Composition**: Standard Portland concrete (not detailed)

**Air:**
- **Composition**: 80 vol% N₂, 20 vol% O₂
- **Density**: Standard atmospheric (not stated)
- **Application**: Cavity fill, gap between reactor top and citadel floor

**ATR Reactor Materials:**
- **Fuel plates**: Aluminum-clad (Al)
- **Beryllium reflector**: Be (fills space between fuel annulus and core reflector tank)
- **Light water**: 1.0 g/cm³ (verification problem material)
- **Pure aluminum**: 2.7 g/cm³ (verification problem material)

### 3.4 Material Evolution Considerations

**Depletion Tracking:**
- Uranium composition evolution tracked during irradiation
- Relative difference in U composition < 0.1% between reference and repeated structure approaches
- Independent depletion calculations performed for each assembly (μHTGR)
- Flux spatial variation determines depletion grouping strategy

**Cross-Section Libraries:**
- **MCNP**: ENDF/B-VIII.0 at room temperature
- **ORIGEN**: One-group cross-sections generated by COUPLE module
- **Spectrum-dependent**: Libraries weighted by flux spectrum in each region

---

## 4. DESIGN PARAMETERS AND OPERATIONAL CONDITIONS

### 4.1 AGR-1 Irradiation Parameters

**Irradiation History:**
- **Number of cycles**: 13 power cycles
- **Total irradiation time**: ~3 years
- **Number of time steps (benchmark data)**: 662 time steps
- **Model simplification**: Cycle-averaged values used for power, OSCC position, neck shim insertion

**Power and Flux:**
- **ATR total power**: 250 MWth
- **Tally normalization**: B-10 position normalized to east lobe power
- **East lobe power**: Average of NE, Center, SE lobe powers
- **Independent lobe control**: Different power levels in corner lobes for independent test conditions

**Driver Fuel Assumptions:**
- **BOC fuel composition**: Defined for BOC 145A equilibrium cycle
- **Model simplification**: Driver fuel composition held constant for all cycles (not depleted)
- **Note**: ATR does not establish true equilibrium fuel loading

**Decay Times Studied:**
- 1 day
- 30 days
- 365 days (1 year)

### 4.2 μHTGR Operational Parameters

**Power and Burnup:**
- **Thermal power**: 10 MWth (based on USNC MMR early design)
- **Initial k-eff**: 1.26797
- **End-of-life k-eff**: 1.00000 (critical)
- **Core lifetime**: 16.07 years (calculated)
- **Design lifetime**: 20 years (target, not achieved in simplified model)
- **Note**: Model based on publicly available MMR data with assumed parameters

**Decay Cooling Period:**
- **Decommissioning strategy**: 3-month (90-day) cool-down
- **Finding**: Insufficient for minimizing personnel exposure

**Dose Rate Results (after 3-month cool-down):**
- **At citadel floor (ground level)**: > 40 mSv/h
- **Implication**: Additional shielding or longer cool-down required

### 4.3 Verification Problem Parameters

**Simplified Geometry Test:**
- **Power level**: 1 MW constant power
- **Irradiation period**: 12-month cycle
- **Purpose**: Verify repeated structure approach accuracy
- **Materials**: UO₂ fuel pins, Al inner shell, light water
- **Results**: 15.6% difference in delayed heating (whole-core repeated structure vs. reference)
- **Improved grouping**: 4.3% difference when fuel pins grouped by flux level

---

## 5. MODELING APPROACHES AND METHODOLOGIES

### 5.1 Overall Calculation Scheme: Formal 3-Step Process

**Step 1: Neutron Transport (MCNP6.2)**
- Calculate neutron flux spatial and energy distribution during operation
- Generate geometry- and material-dependent parameters:
  - Multi-group neutron flux
  - One-group reaction cross-sections
- Track flux evolution through depletion steps

**Step 2: Activation/Depletion (ORIGEN-S via SCALE 6.2.4)**
- Estimate energy distribution and emission probability of decay photon sources
- Calculate isotopic concentrations after shutdown
- Determine radiation source terms (photon spectra)
- Calculate decay heat

**Step 3: Photon Transport (MCNP6.2)**
- Fixed-source photon transport using decay sources from Step 2
- Evaluate dose rate using F4 tally with fluence-to-dose conversion factors
- Calculate spatial dose rate distributions

### 5.2 MOAA (MCNP-ORIGEN Activation Automation) Tool

**Software Components:**
- **Transport solver**: MCNP 6.2
- **Depletion solver**: ORIGEN-S (part of SCALE 6.2.4)
- **Coupling tool**: MOAA (Python package developed by INL)
- **Supporting modules**: COUPLE (cross-section library preparation), OPUS (output extraction)

**MOAA Capabilities:**
- Automates tally card writing in MCNP
- Reads MCNP flux and reaction rate tallies
- Creates SCALE input files automatically
- Executes SCALE calculations
- Standardizes results post-processing
- Reduces human error and processing time

**Irradiation Calculation Options:**
- **Single-step**: Constant power irradiation
- **Multi-step**: Multiple core configurations with piecewise constant power
  - Handles material density evolution
  - Handles temperature changes
  - Handles geometry changes
  - Handles control rod movement
- **Predictor-corrector**: Two-step process combining explicit/implicit methods for better convergence

**User Input Requirements:**
- **User Input File (UIF)**: Defines irradiation cases, decay times, regions of interest
- **MCNP input file(s)**: Geometry and material definitions
- **Volume specification**: Cell volumes must be calculated and specified (especially for repeated structures)
  - MCNP only auto-calculates volumes for simple geometries
  - For repeated structures: specify total material volume present in geometry
  - Without specification: MCNP calculates only one cell volume

**Workflow:**
1. MCNP calculates neutron flux and one-group cross-sections
2. MOAA extracts data and prepares ORIGEN input
3. ORIGEN performs depletion/decay calculation
4. MOAA updates material compositions in MCNP
5. Cycle repeats for next time step
6. Final photon source distributions exported for dose calculation

### 5.3 Repeated Structures Approach for TRISO Particles

**Challenge:**
- One HTGR core contains millions of TRISO particles
- Modeling each particle independently is computationally impossible
- HTGR fuel exhibits "double heterogeneity":
  - Heterogeneity 1: TRISO particles dispersed in compact matrix
  - Heterogeneity 2: Compacts arranged in fuel assemblies

**Solution:**
- Use MCNP repeated structures (universe/lattice/fill capabilities)
- Explicitly model TRISO particles in lattice configuration
- Group particles by flux level to account for spatial variations

**Lessons Learned (Verification Exercise):**
- **Whole-core repeated structure**: 15.6% error in delayed heating
  - Strong spatial flux effects not captured
  - Not recommended for realistic problems
- **Flux-based grouping (groups of 4)**: 4.3% error
  - Groups account for flux shape variation
  - Better accuracy with manageable computational cost
- **Recommendation**: Group TRISO particles/compacts by assembly
  - Assume uniform flux within each assembly
  - Perform independent depletion for each assembly
  - Accuracy vs. computational cost trade-off

**Spatial Distribution Assumptions:**
- **TRISO particles**: Arranged in regular lattice (not random)
- **Particle pitch**: 0.1 cm (μHTGR)
- **Spatial source sampling**: Uniform within each source cell
- **Rejection method**: MCNP uses enclosing volume rejection
  - User defines parallelepiped or cylinder enclosing source cell
  - Randomly sampled points accepted only if inside actual source cell
  - For repeated structures: enclosing volume defined in local coordinates of innermost cell

### 5.4 Dose Rate Calculation Methodology

**Dose Rate Equation:**

D-dot [Sv/h] = F4:p [pSv/src] × Σᵢ Sᵢ × 3.6 × 10⁻⁹

Where:
- **D-dot**: Dose rate
- **F4:p**: F4 photon flux tally in detector region
- **Sᵢ**: Total photon emission rate from region i [γ/s]
- **Conversion factor**: 3.6 × 10⁻⁹ converts pSv/src to Sv/h

**Photon Source Definition:**

Sᵢ [γ/s] = ∫ φᵢᵞ(E) dE

- **φᵢᵞ(E)**: Photon source energy distribution from region i
- Provided by ORIGEN decay calculation
- Defines energy distribution of fixed photon source in MCNP

**Cell Emission Probability:**

sᵢ = Sᵢ / Σⱼ Sⱼ

- Normalized probability for sampling source from cell i
- Required when all source cells included in single simulation
- Alternative: Multiple simulations to isolate individual cell contributions

**Fluence-to-Dose Conversion:**
- **Standard**: ICRP fluence-to-dose conversion factors
- **Geometry**: Antero-posterior (AP) exposure to photons
- **Implementation**: Added to MCNP input via DE/DF cards or dose response functions
- **Units**: F4 tally result in pSv per source particle

**Calculation Options:**
- **Multiple simulations**: Each source cell contribution calculated separately
  - Advantage: Individual contribution identification
  - Disadvantage: Computationally expensive
- **Single simulation**: All source cells simultaneously
  - Advantage: Computationally efficient
  - Disadvantage: Requires careful emission probability normalization

### 5.5 Cross-Section and Nuclear Data

**MCNP Libraries:**
- **Primary**: ENDF/B-VIII.0
- **Temperature**: Room temperature (293 K assumed)
- **Particle types**: Neutrons (step 1), photons (step 3)

**ORIGEN Libraries:**
- **Generation**: COUPLE module creates one-group libraries
- **Weighting**: Volume- and spectrum-weighted cross-sections
- **Input**: Multi-group flux from MCNP tallies
- **Output**: Effective one-group cross-sections for depletion

**Thermal Scattering:**
- Graphite S(α,β) thermal scattering treatment implied but not detailed
- Critical for accurate neutron thermalization in graphite-moderated system

---

## 6. BURNUP AND DOSE RATE CALCULATION METHODOLOGIES

### 6.1 Depletion/Burnup Calculation Approach

**Depletion Coupling Scheme:**
1. **Initial MCNP calculation**: Fresh fuel, beginning-of-cycle (BOC) conditions
2. **Flux tally extraction**: Multi-group flux and one-group reaction rates
3. **COUPLE execution**: Generate ORIGEN cross-section library
4. **ORIGEN depletion**: Solve Bateman equations for isotope evolution
5. **Material update**: Updated compositions returned to MCNP
6. **Iteration**: Repeat for next time step

**Time-Step Strategy:**
- **AGR-1**: 662 time steps from benchmark specification (simplified to cycle averages)
- **μHTGR**: Not explicitly stated; sufficient steps to reach EOL at 16.07 years
- **Power profile**: Piecewise constant power in each time step
- **Flux update**: Neutron flux recalculated each step to account for composition changes

**Predictor-Corrector Option:**
- **Predictor step**: Explicit calculation using BOC cross-sections
- **Corrector step**: Implicit calculation using average cross-sections
- **Convergence**: Better accuracy for strongly varying flux/composition

**k-eff Evolution Tracking:**
- **μHTGR initial k-eff**: 1.26797 (significant excess reactivity)
- **EOL criterion**: k-eff = 1.00000
- **Burnup reactivity swing**: ~26,797 pcm
- **Purpose**: Demonstrate core lifetime and validate depletion model

### 6.2 Activation Calculation Methodology

**Activation Source Regions:**
- **Primary**: Fuel in TRISO particles (all assemblies)
- **Secondary**: Structural materials (SS316L, graphite, Hf shroud)
- **Tertiary**: Reflector regions (bottom, top, radial graphite)

**Sensitivity Analysis (μHTGR):**
- Fuel particle contribution: ~8 orders of magnitude > graphite assembly contribution
- Justifies neglecting graphite activation in some cases
- Structural steel activation significant at long decay times (365 days: 42.54%)

**Decay Time Calculations:**
- Multiple decay times from single irradiation history
- ORIGEN calculates isotopic inventory at specified cool-down times
- Photon source spectra extracted for each decay time

**Isotopic Tracking:**
- Full fission product inventory
- Actinide buildup and decay chains
- Activation products in structural materials
- Important Hf activation noted (growth 1-30 days, then decay)

### 6.3 Photon Source Characterization

**Energy Spectrum:**
- Continuous energy distribution from ORIGEN
- Binned for MCNP source definition (SI/SP cards)
- Energy range: Typically 0-10 MeV for fission product decay gammas
- Spectrum shape varies by:
  - Decay time (short-lived vs. long-lived isotopes)
  - Material type (fuel vs. structural activation)
  - Irradiation history (burnup level)

**Source Intensity Evolution:**

| Decay Time | Total Source Intensity [γ/s] | Relative to 1 day |
|------------|------------------------------|-------------------|
| 1 day      | 1.199 × 10¹⁵                 | 100%              |
| 30 days    | 3.253 × 10¹⁴                 | 27.1%             |
| 365 days   | 1.305 × 10¹³                 | 1.09%             |

- **Decrease**: ~2 orders of magnitude from 1 day to 365 days
- **Short-lived isotopes**: Dominant at early times
- **Long-lived isotopes**: Become dominant at long times

**Source Contribution by Component (AGR-1):**

| Component              | 1 day | 30 days | 365 days |
|------------------------|-------|---------|----------|
| Fuel in TRISO          | 53.19%| 30.03%  | 56.95%   |
| Hafnium shroud         | 41.64%| 62.11%  | 0.50%    |
| Outer wall SS316L      | 3.13% | 4.77%   | 25.9%    |
| Top support SS316L     | 0.85% | 1.30%   | 7.10%    |
| Bottom support SS316L  | 0.76% | 1.17%   | 6.47%    |
| Inner wall SS316L      | 0.43% | 0.63%   | 3.07%    |
| Graphite spacers       | ~10⁻⁹ | ~10⁻⁹   | ~10⁻⁷    |

**Key Observations:**
- Fuel dominates at early (1 day) and late (365 days) times
- Hf shroud peaks at 30 days (62.11%) due to intermediate half-life activation products
- Stainless steel contribution grows with decay time as fuel source decreases
- Graphite activation negligible

### 6.4 Dose Rate Results and Validation Implications

**AGR-1 Dose Rates:**

| Distance from Center | 1 day [Sv/h] | 30 days [Sv/h] | 365 days [Sv/h] |
|----------------------|--------------|----------------|-----------------|
| 6 cm                 | 666.2        | 190.3          | 3.7             |
| 46 cm                | 72.7         | 20.4           | 0.4             |
| 98 cm                | 25.4         | 7.3            | 0.1             |

**Operational Implications:**
- **Post-irradiation examination (PIE)**: Wait > 1 year recommended
- **Hot cell requirement**: Appropriate shielding mandatory even after 1 year
- **Personnel dose**: 0.1 Sv/h at 98 cm after 1 year still significant

**μHTGR Decommissioning Results:**
- **3-month cool-down**: > 40 mSv/h at citadel floor (7 m above core)
- **Finding**: Proposed 3-month strategy insufficient
- **Recommendation**: Longer cool-down period or additional shielding required
- **Alternative**: Modify decommissioning sequence to maintain shielding

**Model Accuracy Assessment:**
- **Verification exercise**: Repeated structure approach validated
  - Reference case (explicit cells): 675.0 W delayed heating
  - Repeated structure (whole core): 780.4 W (15.6% difference)
  - Repeated structure (grouped): 4.3% difference
- **Flux evolution**: < 0.1% difference in neutron flux
- **Isotopic composition**: < 0.1% difference in U evolution
- **Photon intensity**: < 0.1% difference in total source

**Uncertainty Sources (noted but not quantified):**
- Flux spatial variation approximation
- Regular lattice vs. random particle placement
- Material composition uncertainties
- Geometric simplifications (gas lines, thermocouples neglected)
- Power history simplification (cycle averages vs. detailed history)

---

## 7. VALIDATION REQUIREMENTS AND BENCHMARKING

### 7.1 Benchmark Specifications

**AGR-1 Depletion Benchmark:**
- **Source**: Official INL benchmark specification
- **Data provided**:
  - Detailed geometry specifications
  - Material compositions (4 compact variants)
  - Irradiation history (662 time steps)
  - Lobe power history
  - OSCC positions
  - Neck shim insertion conditions
  - Flux measurements (for normalization)
- **Modeling guidance**: Benchmark document provides recommended approaches
- **Reference**: AGR-1 Depletion Benchmark Technical Report (Ref. 30)

**Verification Exercise:**
- **Purpose**: Verify MOAA workflow and repeated structure approach
- **Reference solution**: Explicit independent cell definition
- **Test geometry**: Simple cylindrical system with fuel pins
- **Metrics compared**:
  - Delayed gamma heating
  - Average neutron flux
  - Total photon intensity
  - Uranium composition evolution
- **Acceptance criteria**: Not formally defined, but < 5% considered reasonable

### 7.2 Code and Method Validation

**MCNP Validation:**
- **Method**: Monte Carlo (minimal approximations)
- **Geometry**: Exact representation (within modeling assumptions)
- **Cross-sections**: ENDF/B-VIII.0 (latest evaluation)
- **Known issues**: Volume calculation for repeated structures requires user input
- **Limitation**: Statistical uncertainty (not quantified in article)

**ORIGEN Validation:**
- **Decay data**: Extensive validation against experimental data (historical)
- **Cross-section generation**: COUPLE validated for spectrum weighting
- **Limitation**: Point depletion (no spatial resolution within cell)

**MOAA Validation History:**
- Originally developed for ATR irradiation experiments
- Validated against ATR experimental data (not detailed in this article)
- Extended to general HTGR applications
- References to previous work using MOAA (Refs. 17-19)

**Comparisons to Literature:**
- Ho et al. (Ref. 13): HTTR shutdown gamma using MCNP6/ORIGEN2
  - Used repeated structures for fuel rods (uniform distribution)
  - Did not explicitly model TRISO particles as sources
  - Present work advances this by modeling TRISO particles directly
- Other HTGR dose rate studies (Refs. 10-12): Operational dose rates
  - Present work focuses on shutdown dose rates (distinct challenge)

### 7.3 Experimental Validation Opportunities

**AGR-1 Post-Irradiation Examination:**
- **PIE data**: Capsule dose rates could validate calculations
- **Measurement locations**: Different distances from capsule center
- **Decay times**: Various cool-down periods
- **Challenges**: Hot cell environment, detector response uncertainties

**ATR Flux Measurements:**
- **In-core detectors**: Validate neutron flux during irradiation
- **Normalization data**: Benchmark provides flux tally data
- **Purpose**: Ensure accurate flux history for activation calculations

**Potential Future Validation:**
- μHTGR dose measurements (if reactor built at UIUC)
- Comparison with similar HTGR decommissioning data (limited availability)
- Separate-effects experiments: Individual material activation measurements

### 7.4 Model Limitations and Uncertainties

**Acknowledged Simplifications:**
1. **TRISO particle arrangement**: Regular lattice vs. random (real) distribution
   - Impact on flux self-shielding
   - Statistical homogeneity assumption
2. **AGR-1 model**: Gas lines, thermocouples, thru-tubes neglected
   - Impact on streaming paths
   - Structural activation neglected
3. **Power history**: Cycle-averaged values vs. detailed time history
   - Smooths out flux transients
   - May under-predict short-lived isotope production
4. **Driver fuel**: Held constant (not depleted in AGR-1 model)
   - Flux spectrum may shift slightly with driver depletion
   - ATR operational practice approximated
5. **μHTGR parameters**: Many values assumed (not publicly available)
   - Model illustrative, not predictive for actual MMR design
   - Parametric study rather than licensed design

**Unquantified Uncertainties:**
- Monte Carlo statistical uncertainty (not reported)
- Material composition uncertainties
- Geometric tolerances
- Nuclear data uncertainties (cross-sections, decay data)
- Flux measurement uncertainties (ATR normalization)

**Model Validation Status:**
- **Verification**: Completed (repeated structure approach validated)
- **Code validation**: MCNP and ORIGEN individually validated (historical)
- **Benchmark comparison**: AGR-1 benchmark available but results comparison not shown
- **Experimental validation**: Awaiting PIE data or operational measurements

**Recommendations for MCNP Users:**
- Perform sensitivity studies on particle arrangement (regular vs. random)
- Quantify Monte Carlo statistical uncertainty (adequate particle histories)
- Consider separate-effects validation (individual material activation)
- Document all modeling assumptions and simplifications
- Compare flux tallies to measurements when available
- Use benchmark specifications exactly as provided
- Report uncertainty propagation through depletion sequence

---

## 8. DATA QUALITY ASSESSMENT

### Completeness: **MOSTLY COMPLETE**

**Available:**
- TRISO particle complete layer specifications (thickness, material, density)
- μHTGR core geometry (assemblies, pitch, channel radii, reflector dimensions)
- Material densities for all major components
- Operational parameters (power, cycle time, decay times)
- Dose rate results at multiple locations and times
- Photon source contributions by component
- Modeling methodology workflow
- Software version numbers (MCNP 6.2, SCALE 6.2.4)

**Missing:**
- Detailed material compositions (isotopic breakdown for SS316L, concrete mix)
- Exact compact dimensions (diameter, height)
- Number of compacts per fuel channel (μHTGR)
- Number of TRISO particles per compact
- AGR-1 compact variant specifications (exact layer differences)
- Detailed power history (662 time steps not provided)
- Statistical uncertainties on calculated results
- Cross-section temperature dependence treatment details
- Exact geometry of ATR flux trap B-10 position
- Complete validation results (benchmark comparison metrics)

### Consistency: **CONSISTENT**

**Cross-checks performed:**
- TRISO layer radii sum correctly (0.025 + 0.010 + 0.004 + 0.0035 + 0.004 = 0.0465 cm)
- Material densities within physical ranges
- Dose rate decreases with distance (inverse square trend)
- Source intensity decreases with decay time (physical decay)
- k-eff decreases with burnup (fuel depletion)
- Photon source contributions sum to 100%

**No significant conflicts noted between:**
- Text descriptions and table data
- Figures and numerical values
- Different sections of the article

### Uncertainty Information: **LIMITED**

**Uncertainties Reported:**
- Verification exercise relative differences (15.6%, 4.3%)
- Component contribution percentages (precision to 2 decimal places implies ~1% uncertainty)
- EOL time (16.07 years - 2 significant figures implies ~0.5% uncertainty)

**Uncertainties NOT Reported:**
- Monte Carlo statistical uncertainties (should be standard MCNP output)
- Material composition measurement uncertainties
- Geometric dimension tolerances
- Nuclear data uncertainties
- Experimental validation uncertainties (no comparison shown)
- Combined uncertainty propagation

### Recommended Confidence Level: **MEDIUM-HIGH**

**High Confidence:**
- TRISO particle design specifications (Table 5 - precise, complete)
- Qualitative modeling methodology (well-documented, peer-reviewed)
- Software capabilities and workflow (MOAA is established tool)
- Relative trends (dose vs. time, dose vs. distance, source evolution)

**Medium Confidence:**
- Absolute dose rate values (no experimental validation shown, uncertainties not quantified)
- μHTGR geometry (based on limited publicly available MMR data with assumptions)
- AGR-1 power history simplification (cycle averages vs. actual history)
- Material activation (depends on cross-section library accuracy)

**Lower Confidence:**
- Exact decommissioning dose rates (model simplifications, parameter assumptions)
- Long-term predictions (> 1 year decay, limited isotope validation)
- Spatial dose distribution details (detector model simplified as cylinder)

**Confidence Factors:**
- **Positive**: Peer-reviewed publication, established codes, benchmark specification available
- **Negative**: Uncertainties not quantified, experimental validation not shown, some parameters assumed

---

## 9. MODELING IMPLICATIONS FOR MCNP DEVELOPMENT

### 9.1 Direct Applications

**TRISO Fuel Modeling:**
- Use Table 5 specifications directly for TRISO particle definition
- Implement as nested spheres (5 cells: kernel, buffer, IPyC, SiC, OPyC)
- Define universe for single TRISO particle
- Fill compact matrix with TRISO particle lattice (40% packing fraction)

**Repeated Structures Strategy:**
- Define TRISO particle as universe U1
- Define compact as universe U2 (lattice of U1 in SiC matrix)
- Define assembly as universe U3 (lattice of U2 compacts)
- Group assemblies by expected flux level for depletion
- Avoid single repeated structure for entire core (15.6% error)

**Dose Rate Calculation Setup:**
- F4:p tally in detector cell
- SDEF with SI/SP cards for photon source energy distribution
- SI: Source information card for energy bins (from ORIGEN output)
- SP: Source probability card for photon emission spectrum
- SC: Source cell card with emission probabilities
- Cell volumes must be explicitly calculated and specified (VOL card)
- Use enclosing volume for source sampling (TRISO particles: cylindrical or box)

**Depletion Cell Definition:**
- Each depletion cell must have specified volume (VOL card)
- For repeated structures: specify total material volume (not single cell)
- Example: If 1000 TRISO particles each with 0.001 cm³ fuel → VOL = 1.0 cm³
- Depletion grouping determines number of cells to track

### 9.2 Required Preprocessing

**Geometry Preparation:**
1. **Calculate exact TRISO radii**:
   - R₁ = 0.0250 cm (kernel)
   - R₂ = 0.0350 cm (buffer)
   - R₃ = 0.0390 cm (IPyC)
   - R₄ = 0.0425 cm (SiC)
   - R₅ = 0.0465 cm (OPyC)
   - Use SPH surfaces in MCNP

2. **Determine lattice parameters**:
   - Particle pitch: 0.1 cm (center-to-center)
   - Calculate compact radius from packing fraction: PF = (N × V_TRISO) / V_compact
   - For 40% PF: Determine N and compact dimensions

3. **Calculate assembly lattice**:
   - Fuel channel pitch: 3.2 cm
   - Channel radius: 1.15 cm (fuel), 0.775 cm (coolant)
   - Determine number of channels from assembly pitch (30 cm)

4. **Volume calculations**:
   - TRISO kernel: (4/3)πR₁³ = 6.545 × 10⁻⁵ cm³
   - Total TRISO: (4/3)πR₅³ = 4.205 × 10⁻⁴ cm³
   - Each layer volume: V_layer = (4/3)π(R_outer³ - R_inner³)
   - Multiply by number of particles for total depletion cell volume

**Material Card Preparation:**

1. **UO₂ Kernel** (19.75% enriched):
   ```
   M1    92235.80c  [atoms/barn-cm for U-235]
         92238.80c  [atoms/barn-cm for U-238]
         8016.80c   [atoms/barn-cm for O-16]
   ```
   - Density: 10.8 g/cm³
   - Molecular weight: UO₂ = 238.03 (natural) → adjust for enrichment
   - Calculate atom density: N = ρ × N_A / M

2. **Carbon layers** (Buffer, IPyC, OPyC):
   ```
   M2    6000.80c   [atoms/barn-cm for C]
   ```
   - Buffer: 0.98 g/cm³
   - IPyC: 1.85 g/cm³
   - OPyC: 1.86 g/cm³
   - Atom density: N = ρ × N_A / 12.011

3. **SiC layer**:
   ```
   M3    14000.80c  [atoms/barn-cm for Si]
         6000.80c   [atoms/barn-cm for C]
   ```
   - Density: 3.20 g/cm³
   - Stoichiometry: 1:1 (SiC)
   - Molecular weight: 40.097 g/mol

4. **Homogenized compact** (if not using explicit TRISO):
   ```
   M4    [UO₂ components at 40% density]
         [C components at 40% density for coatings]
         [SiC at 60% density for matrix]
   ```
   - Use volume-weighted averaging
   - Requires knowledge of number of particles per compact

5. **Graphite** (assemblies, reflectors):
   ```
   M5    6000.80c   [atoms/barn-cm for C]
   ```
   - Density: 1.75 g/cm³
   - Add thermal scattering: MT5 grph.20t (graphite S(α,β))

6. **SS316L** (structures):
   ```
   M6    26000.80c  [Fe - major component]
         24000.80c  [Cr - ~17%]
         28000.80c  [Ni - ~12%]
         [Additional elements: Mo, Mn, Si, etc.]
   ```
   - Density: ~8.0 g/cm³ (standard, not specified)
   - Use standard SS316L composition
   - Important for activation calculations

7. **Portland Concrete**:
   ```
   M7    [O, Si, Ca, Al, Fe - typical concrete mix]
   ```
   - Density: 2.3 g/cm³
   - Use standard Portland concrete composition (e.g., PNNL-15870 Rev.1)

8. **Air**:
   ```
   M8    7014.80c   [N-14 at 80 vol%]
         8016.80c   [O-16 at 20 vol%]
   ```
   - Standard atmospheric composition
   - Low density (~0.001225 g/cm³ at STP)

**Conversion Factors Needed:**

1. **Enrichment to isotopic composition**:
   - 19.75% U-235 by weight
   - U-235: 235.044 amu, U-238: 238.051 amu
   - Calculate atom fraction: x = (w/M₂₃₅) / [(w/M₂₃₅) + ((1-w)/M₂₃₈)]

2. **Density to atom density**:
   - N [atoms/barn-cm] = (ρ [g/cm³] × N_A) / (M [g/mol] × 10²⁴)
   - N_A = 6.022 × 10²³ atoms/mol

3. **Volume fractions to mass fractions** (for homogenized materials):
   - m_i = V_i × ρ_i / Σ(V_j × ρ_j)

4. **Dose units**:
   - 1 Sv = 100 rem
   - Results in mSv/h can be compared to dose limits (e.g., 20 mSv/year occupational)

### 9.3 Assumptions and Approximations in Source

**Explicitly Stated:**
1. Regular TRISO lattice (vs. random distribution in reality)
2. Uniform source distribution within each cell
3. TRISO particles uniformly distributed at 0.1 cm pitch
4. AGR-1 model neglects gas lines, thermocouples, thru-tubes
5. Hf shroud modeled as full cylinder (simplification of actual geometry)
6. μHTGR RPV side wall neglected
7. ATR driver fuel composition constant (not depleted)
8. Power history cycle-averaged (vs. detailed 662-step history)
9. ENDF/B-VIII.0 cross-sections at room temperature (no temperature dependence modeled)

**Implied but Not Explicitly Stated:**
1. Helium coolant neglected (or modeled as void)
2. Temperature effects on material density neglected
3. No thermal expansion during operation
4. Steady-state flux assumed within each time step
5. No mechanical deformation of TRISO layers
6. Perfect spherical TRISO particles (no asphericity)
7. Uniform enrichment within kernel
8. No material impurities
9. Sharp interfaces between layers (no interdiffusion)

**Impact on MCNP Model:**
- Regular lattice may slightly overestimate self-shielding (vs. random)
- Simplified geometry may underestimate streaming paths
- Room-temperature cross-sections conservative for high-temp reactor
- Constant driver fuel composition simplifies model but may affect flux spectrum slightly

### 9.4 Validation Opportunities

**Model Benchmarking:**
1. **AGR-1 Depletion Benchmark**:
   - Reproduce benchmark geometry exactly
   - Compare k-eff evolution to benchmark results
   - Compare flux distributions to measured values
   - Validate depletion methodology
   - Reference: INL AGR-1 Depletion Benchmark specification

2. **Verification problems**:
   - Recreate verification exercise from article (Section "Verification")
   - Simple geometry: fuel pins in Al shell with water
   - Compare delayed heating results
   - Expected: < 5% difference with proper flux-based grouping

3. **Dose rate validation** (if data available):
   - AGR-1 PIE dose measurements
   - Compare calculated vs. measured at different distances and decay times
   - Validate photon transport and source term

**Sensitivity Studies:**
1. **Repeated structure grouping**:
   - Vary number of groups (1, 4, 16, per assembly)
   - Plot error vs. computational cost
   - Determine optimal balance for your application

2. **Particle arrangement**:
   - Compare regular lattice vs. random particle placement (RSA algorithm)
   - Assess impact on k-eff and flux distribution
   - May require specialized lattice generation code

3. **Cross-section library**:
   - Compare ENDF/B-VII.1 vs. ENDF/B-VIII.0
   - Assess temperature effect (293 K vs. 900 K)
   - Quantify uncertainty from nuclear data

4. **Time step refinement**:
   - Vary depletion time step size
   - Check convergence of isotopic concentrations
   - Balance accuracy vs. computational time

**Code-to-Code Comparisons:**
1. **Alternative depletion codes**:
   - Serpent 2 (with built-in depletion)
   - SCALE/TRITON (continuous-energy depletion)
   - Compare isotopic inventory and k-eff evolution

2. **Alternative transport codes**:
   - Serpent 2 (Monte Carlo with explicit TRISO)
   - DRAGON (deterministic lattice code with double heterogeneity treatment)
   - Compare flux distributions and reaction rates

3. **Dose rate calculations**:
   - MCNP vs. deterministic Sn codes (DOORS, Attila)
   - MCNP F4 vs. F6 tally for dose (energy deposition vs. flux × conversion)

---

## 10. ADDITIONAL CONTEXT AND RECOMMENDATIONS

### 10.1 Historical Background and Significance

**HTGR Development Programs:**
- **NGNP (Next Generation Nuclear Power)**: DOE/INL program since 2006
- **AGR Fuel Program**: Advanced Gas Reactor Fuel Development and Qualification
- **Generation IV VHTR**: Proposed in 2002 for co-generation of electricity and hydrogen
- **Modern microreactors**: StarCore (Canada), BWXT (DOD), USNC MMR (UIUC campus)

**AGR-1 Experiment Significance:**
- First major TRISO fuel irradiation in U.S. AGR program
- 3-year irradiation in ATR (highest flux test reactor in U.S.)
- Comprehensive PIE program for fuel performance validation
- Benchmark specification available for code validation

**Current Relevance:**
- HTGR microreactors gaining commercial interest (2020s)
- Decommissioning strategies critical for deployment planning
- Shutdown dose rates impact maintenance, refueling, decommissioning
- TRISO fuel unique to HTGR (not applicable to LWRs)

### 10.2 Physics Considerations

**Double Heterogeneity Challenge:**
- Level 1: TRISO particles in compact matrix (sub-mm scale)
- Level 2: Compacts in assembly (cm scale)
- Impact: Flux self-shielding at multiple scales
- Solution: Explicit modeling with repeated structures

**Neutron Thermalization:**
- Graphite moderator: Thermal spectrum reactor
- Important reaction: U-235(n,f) at thermal energies
- Thermal scattering critical for accurate physics
- S(α,β) treatment essential (grph.20t in MCNP)

**Activation Physics:**
- Fission products: Wide range of half-lives (seconds to years)
- Structural activation: Fe-55, Co-60, Ni-63 (long-lived)
- Hf activation: Hf-181 (42.4 d) explains 30-day peak contribution
- Importance of complete decay chain tracking (ORIGEN strength)

**Photon Transport:**
- Decay gamma energies: 0.1-3 MeV range (typical)
- Attenuation in graphite: Low Z material (minimal shielding)
- Concrete shielding: High Z components (Ca, Fe) important for photoelectric absorption
- Buildup factors important in shield regions (not explicitly modeled in MCNP - need sufficient histories)

### 10.3 Known Issues and Limitations

**Computational Challenges:**
- Millions of TRISO particles in full core (requires repeated structures)
- Detailed geometry slows MCNP (tracking in complex lattices)
- Long depletion chains require fine time stepping
- Statistical uncertainty in low-dose regions (requires long runs)

**MOAA-Specific Considerations:**
- Requires SCALE license (not open source)
- Python environment setup required
- Manual volume calculation for repeated structures
- No built-in uncertainty propagation

**Physical Limitations:**
- TRISO particle failure not modeled (assumed perfect retention)
- Temperature effects on cross-sections simplified (room temp used)
- No thermal-hydraulic feedback (flux distribution may change with T)
- Neglects potential fission gas release in failed particles

**Validation Data Gaps:**
- Limited experimental shutdown dose rate data for HTGRs
- AGR-1 PIE dose rates not yet published (or not referenced)
- μHTGR design not finalized (parameters assumed)
- No direct validation of TRISO explicit modeling approach shown

### 10.4 Recommendations for MCNP Model Development

**For AGR-1 Benchmark Modeling:**
1. Obtain official INL AGR-1 Depletion Benchmark specification
2. Model geometry exactly as specified (no simplifications)
3. Use provided irradiation history (all 662 time steps initially)
4. Compare k-eff evolution to benchmark reference solution
5. Validate flux distributions against measured data
6. Once validated, simplify (cycle averages) and assess impact
7. Request PIE dose rate data for shutdown calculation validation

**For HTGR Core Modeling:**
1. Start with single TRISO particle (verify layer radii, materials)
2. Build compact with explicit TRISO lattice (verify packing fraction)
3. Build single assembly (verify channel arrangement)
4. Perform flux calculation for single assembly
5. Identify flux variation within assembly
6. Determine if sub-assembly depletion groups needed
7. Expand to full core with assembly-level depletion
8. Validate against known benchmarks (PBMR, HTR-10, HTTR if available)

**For Dose Rate Calculations:**
1. Perform depletion calculation to desired burnup
2. Extract isotopic inventory from ORIGEN at multiple decay times
3. Use ORIGEN photon source spectra (SI/SP cards in MCNP)
4. Calculate cell emission probabilities (Sᵢ / ΣSⱼ)
5. Define source cells (SC card) with probabilities
6. Set up detector geometry (tally cell)
7. Add fluence-to-dose conversion (DE/DF cards - ICRP values)
8. Run photon transport (MODE P, SDEF card)
9. Extract F4:p tally and convert to dose rate (Eq. 1)
10. Verify with simple hand calculations (point source approximation)

**Best Practices:**
- Document all assumptions in MCNP input comments
- Use version control for input file evolution (git)
- Automate repetitive tasks (material card generation, source definition)
- Perform convergence studies (statistical, spatial, temporal)
- Validate each model component separately before integration
- Maintain traceability to source documents (reference tables, equations)
- Archive all input and output files for reproducibility

**Code Quality:**
- Use MCNP plotting (IP, IS, IX, IY, IZ) to verify geometry visually
- Check for overlapping cells (DEBUG card)
- Run with lost particle debugging (DBCN card)
- Verify volume calculations (print MCNP calculated volumes, compare to VOL)
- Check material balance (total mass should be conserved during depletion)
- Use PRINT cards judiciously to extract needed information
- Implement NPS sufficient for < 5% statistical uncertainty in tallies of interest

### 10.5 Related References and Resources

**Key Citations from Article:**
1. AGR-1 Depletion Benchmark (Ref. 30): Official specification
2. MOAA development (Ref. 27): Detailed tool description
3. MCNP6.2 manual (Ref. 14): LA-UR-17-29981
4. SCALE 6.2.4 manual (Ref. 26): ORNL/TM-2005/39
5. Fluence-to-dose conversion (Ref. 29): ICRP factors
6. Ho et al. (Ref. 13): Similar HTTR shutdown dose rate study

**Recommended Background Reading:**
- HTGR fuel technology (TRISO manufacturing, performance)
- Double heterogeneity treatment methods
- Monte Carlo depletion coupling schemes
- Activation and decay gamma physics
- ATR reactor design and operation

**Available Data (from article):**
- Repository with input files: Mentioned in article (Ref. 20)
- Contains: AGR-1 folder, verification folder, μHTGR folder
- Includes: Code, input files, post-processing scripts, some datasets
- Note: Check for repository availability (open access)

### 10.6 Future Work and Extensions

**Suggested by Article:**
- Extend to pebble-bed HTGR designs (different geometry challenge)
- Investigate TRISO particle failure scenarios (release fractions)
- Couple with thermal-hydraulics (temperature-dependent cross-sections)
- Optimize decommissioning strategies (cool-down time vs. shielding vs. cost)
- Apply to other HTGR designs (PBMR, HTR-PM, X-energy Xe-100)

**MCNP Modeling Opportunities:**
- Automate TRISO lattice generation (random particle placement algorithms)
- Implement variance reduction for deep penetration (DXTRAN, weight windows)
- Develop post-processing tools for dose rate visualization
- Create MCNP-ORIGEN coupling alternative to MOAA (open-source Python)
- Investigate deterministic equivalents for preliminary design (faster calculations)

**Research Questions:**
- What is optimal depletion grouping strategy? (assemblies, zones, individual compacts)
- How sensitive are dose rates to TRISO layer failures? (% failure impact)
- Can homogenized TRISO models adequately capture dose rates? (vs. explicit)
- What is the impact of temperature on activation calculations? (300 K vs. 900 K)
- How do different core configurations affect shutdown dose distributions?

---

## 11. CONCLUSIONS AND KEY TAKEAWAYS

### Summary of Critical Information

**For MCNP Geometry Building:**
- **TRISO specifications (Table 5)**: Complete, directly usable for cell cards
- **μHTGR layout**: Well-defined for full-core model development
- **Repeated structures essential**: Millions of particles require lattice approach
- **Flux-based grouping critical**: < 5% accuracy requires spatial flux consideration

**For Material Definition:**
- **Fuel enrichment**: 19.75% U-235 in UO₂ kernel
- **Coating densities**: Buffer (0.98), IPyC (1.85), SiC (3.20), OPyC (1.86) g/cm³
- **Graphite density**: 1.75 g/cm³ (assemblies and reflectors)
- **Activation materials**: SS316L and Hf shroud significant contributors

**For Depletion/Activation:**
- **MCNP-ORIGEN coupling**: MOAA tool or equivalent required
- **Time steps**: Sufficient resolution for isotope buildup/decay
- **Independent depletion**: Per assembly minimum, finer if flux varies
- **Photon source extraction**: ORIGEN output formatted for MCNP SDEF cards

**For Dose Rate Calculations:**
- **3-step process**: Neutron transport → Activation → Photon transport
- **Source definition**: Energy spectra + emission probabilities + spatial distribution
- **F4 tally**: With fluence-to-dose conversion factors (ICRP AP geometry)
- **Validation**: Compare to simple estimates (point source, inverse square law)

### Critical Design Parameters

1. **TRISO particle outer radius**: 0.0465 cm (465 μm)
2. **Packing fraction**: 40% particles in SiC compact
3. **Particle pitch**: 0.1 cm (center-to-center)
4. **Assembly pitch**: 30 cm
5. **Fuel channel radius**: 1.15 cm
6. **Channel pitch**: 3.2 cm
7. **Core height**: 272 cm (4 layers × 68 cm)
8. **Reflector radius**: 134 cm

### Model Development Priorities

**Must Have:**
1. Accurate TRISO layer dimensions and materials (Table 5)
2. Repeated structures with flux-based grouping (< 5% error target)
3. Complete material compositions (fuel, coatings, structures)
4. Proper volume calculations for depletion cells
5. MCNP-ORIGEN coupling capability (MOAA or equivalent)

**Should Have:**
1. Thermal scattering for graphite (grph.20t)
2. Validation against AGR-1 benchmark (if pursuing rigorous analysis)
3. Multiple decay time calculations (1 day, 30 days, 1 year minimum)
4. Spatial dose rate distributions (not just single points)
5. Sensitivity studies (grouping strategy, particle arrangement)

**Nice to Have:**
1. Temperature-dependent cross-sections (if >50 K difference from room temp)
2. Detailed power history (vs. cycle averages)
3. Random TRISO particle placement (vs. regular lattice)
4. Experimental validation data (PIE measurements)
5. Uncertainty quantification (Monte Carlo + nuclear data + experimental)

### Final Recommendations

**This article is an EXCELLENT resource for:**
- HTGR MCNP model development (geometry, materials, methods)
- TRISO fuel explicit modeling approach
- Shutdown dose rate calculation workflow
- MCNP-ORIGEN coupling best practices
- Understanding HTGR double heterogeneity challenge

**Use this information for:**
1. Building AGR-1 benchmark model (validate MCNP skills)
2. Developing HTGR microreactor models (μHTGR as template)
3. Planning depletion/activation calculation strategies
4. Designing dose rate assessment methodologies
5. Understanding TRISO fuel physics and modeling

**Exercise caution regarding:**
- Absolute dose rate values without uncertainty quantification
- μHTGR parameters (many assumed, not validated design)
- Simplified model results (neglected components may matter for specific applications)
- Applying results to other HTGR designs without modification
- Long-term predictions (> 1 year) without validation

**Next steps for MCNP modeler:**
1. ✅ **Obtain** AGR-1 Depletion Benchmark specification (if available from INL)
2. ✅ **Build** single TRISO particle model (verify geometry, materials)
3. ✅ **Create** compact lattice model (verify packing fraction)
4. ✅ **Develop** assembly model (verify flux distribution)
5. ✅ **Perform** depletion calculation (compare to benchmark if available)
6. ✅ **Calculate** shutdown dose rates (multiple decay times)
7. ✅ **Validate** against experimental data (if/when available)
8. ✅ **Document** all assumptions and simplifications

---

## Appendix A: Key Data Tables

### Table A1: TRISO Particle Specifications (μHTGR Design)

| Layer | Inner Radius (cm) | Outer Radius (cm) | Thickness (cm) | Material | Density (g/cm³) | Volume (cm³) |
|-------|-------------------|-------------------|----------------|----------|-----------------|--------------|
| Kernel| 0.0000            | 0.0250            | 0.0250         | UO₂ (19.75%)| 10.8         | 6.545×10⁻⁵   |
| Buffer| 0.0250            | 0.0350            | 0.0100         | C        | 0.98            | 9.713×10⁻⁵   |
| IPyC  | 0.0350            | 0.0390            | 0.0040         | C        | 1.85            | 4.647×10⁻⁵   |
| SiC   | 0.0390            | 0.0425            | 0.0035         | SiC      | 3.20            | 4.434×10⁻⁵   |
| OPyC  | 0.0425            | 0.0465            | 0.0040         | C        | 1.86            | 5.343×10⁻⁵   |
| **Total** | -             | **0.0465**        | -              | -        | -               | **4.205×10⁻⁴**|

### Table A2: AGR-1 Photon Source Contribution (% by component)

| Component              | 1 day | 30 days | 365 days | Peak Time |
|------------------------|-------|---------|----------|-----------|
| Fuel in TRISO          | 53.19 | 30.03   | 56.95    | 1 d, 365 d|
| Hafnium shroud         | 41.64 | 62.11   | 0.50     | 30 d      |
| Outer wall SS316L      | 3.13  | 4.77    | 25.9     | 365 d     |
| Top support SS316L     | 0.85  | 1.30    | 7.10     | 365 d     |
| Bottom support SS316L  | 0.76  | 1.17    | 6.47     | 365 d     |
| Inner wall SS316L      | 0.43  | 0.63    | 3.07     | 365 d     |
| **Total intensity (γ/s)** | **1.199×10¹⁵** | **3.253×10¹⁴** | **1.305×10¹³** | - |

### Table A3: AGR-1 Dose Rates (Sv/h by distance and decay time)

| Distance from Center | 1 day  | 30 days | 365 days | Reduction (1d→365d) |
|----------------------|--------|---------|----------|---------------------|
| 6 cm                 | 666.2  | 190.3   | 3.7      | 180×                |
| 46 cm                | 72.7   | 20.4    | 0.4      | 182×                |
| 98 cm                | 25.4   | 7.3     | 0.1      | 254×                |

### Table A4: μHTGR Core Configuration

| Parameter                    | Value      | Units |
|------------------------------|------------|-------|
| Fuel assemblies              | 24         | -     |
| Control assemblies           | 12         | -     |
| Reserved shutdown assembly   | 1          | -     |
| Assembly pitch               | 30         | cm    |
| Axial layers                 | 4          | -     |
| Layer height                 | 68         | cm    |
| Total core height            | 272        | cm    |
| Radial reflector radius      | 134        | cm    |
| Fuel channel radius          | 1.15       | cm    |
| Coolant channel radius       | 0.775      | cm    |
| Channel pitch                | 3.2        | cm    |
| Graphite density             | 1.75       | g/cm³ |
| Compact SiC density          | 3.2        | g/cm³ |
| TRISO packing fraction       | 40         | %     |
| Particle pitch               | 0.1        | cm    |

### Table A5: Software and Libraries Used

| Software/Library    | Version      | Purpose                          |
|---------------------|--------------|----------------------------------|
| MCNP                | 6.2          | Neutron and photon transport     |
| SCALE               | 6.2.4        | Contains ORIGEN-S depletion code |
| ORIGEN-S            | Part of SCALE| Isotope depletion and decay      |
| COUPLE              | Part of SCALE| Cross-section library generation |
| OPUS                | Part of SCALE| Output extraction and conversion |
| MOAA                | Not specified| Python coupling tool (INL)       |
| ENDF/B-VIII.0       | Latest       | Nuclear cross-section library    |
| ICRP Factors        | Standard     | Fluence-to-dose conversion       |

---

## Document Locations and References

**Key information extracted from:**
- **Lines 727-931**: AGR-1 experiment description and results
- **Lines 972-1107**: μHTGR geometry and operational parameters
- **Lines 1008-1057**: TRISO particle specifications (Table 5)
- **Lines 778-891**: AGR-1 photon source contributions (Table 3)
- **Lines 894-930**: AGR-1 dose rates (Table 4)
- **Lines 250-487**: MOAA tool description and methodology
- **Lines 220-239**: 3-step calculation process

**Figures referenced but not reproduced:**
- Figure 1: MOAA workflow diagram
- Figure 2: Shutdown dose rate calculation scheme
- Figure 6: ATR quarter model geometry
- Figure 7: AGR-1 experiment geometry
- Figure 8: μHTGR core layout and side view
- Figure 9: k-eff evolution during burnup

**Original document:**
- **File**: /home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1_research_article.xml
- **Format**: JATS XML (Journal Article Tag Suite)
- **Length**: 36,246 tokens
- **Analysis date**: 2025-11-07

---

**Report prepared by:** MCNP Technical Documentation Analyzer
**Analysis completeness:** Comprehensive extraction of all MCNP-relevant technical data
**Confidence level:** Medium-High (peer-reviewed source, some uncertainties not quantified)
**Recommended use:** Direct application for HTGR/TRISO modeling; verify assumptions for specific applications
