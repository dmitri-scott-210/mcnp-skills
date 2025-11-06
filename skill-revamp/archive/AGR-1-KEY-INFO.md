# AGR-1 EXPERIMENT - KEY INFORMATION FOR MCNP LATTICE MODELING

**Source:** "Shutdown dose rate calculations in high-temperature gas-cooled reactors using the MCNP-ORIGEN activation automation tool"
**Authors:** Roberto Fairhurst-Agosta, Tomasz Kozlowski
**Journal:** Nuclear Science and Technology Open Research (2024)
**DOI:** 10.12688/nuclscitechnolopenres.17447.2

**Extracted:** 2025-11-04 (Session 15)
**Purpose:** Key information for understanding lattice construction from public science literature for mcnp-lattice-builder skill

---

## PROJECT OVERVIEW

### AGR-1 Experiment Background

**What:** TRISO-particle irradiation test in the Advanced Test Reactor (ATR) at Idaho National Laboratory

**Purpose:** Part of DOE Advanced Gas Reactor Fuel Development and Qualification Program to support Next Generation Nuclear Power (NGNP) program

**Duration:** Irradiated over 13 power cycles spanning approximately 3 years

**Location:** B-10 hole in ATR (beryllium reflector)

---

## REACTOR FACILITY - ADVANCED TEST REACTOR (ATR)

### Core Configuration

**Power:** 250 MWth high-flux test reactor

**Core Layout:**
- 40 fuel elements arranged in serpentine annulus
- Between and around 9 flux traps
- Each fuel element: 19 parallel, curved, aluminum-clad fuel plates
- Forms 45-degree sector of right circular cylinder
- **Core shape:** Clover-leaf configuration

**Operational Flexibility:**
- Different power levels in corner lobes
- Independent testing conditions within same operating cycle

**Test Positions:**
- 9 flux trap positions
- 68 additional irradiation positions inside core reflector tank
- Neck shim housing with 24 neck shim and regulating rods
- 8 inner A-holes and 8 outer A-holes
- Outer shim control cylinders (OSCC) in beryllium reflector
- B-holes and I-holes for irradiation
- Water holes

### MCNP Modeling Approach

**Model Type:** Quarter model (east quadrant only)

**Simplifications:**
- Fuel plates grouped into 3 radial zones
- Cyclic average for power, OSCC position, neck shim insertion
- Driver fuel composition held constant at BOC 145A for all cycles
- 662 time steps simplified to cycle averages

**Normalization:** B-10 position tally data normalized to average of northeast, center, and southeast lobe powers

---

## AGR-1 TEST TRAIN GEOMETRY

### Overall Configuration

**Structure:** 6 cylindrical capsules vertically stacked

**Compact Arrangement:**
- 3 columns per capsule
- 4 compacts per column
- **Total: 72 compacts**

### Capsule Types and Variants

**Baseline Compact:**
- Capsule 3
- Capsule 6

**Variant 1:**
- Capsule 5

**Variant 2:**
- Capsule 2

**Variant 3:**
- Capsule 1
- Capsule 4

**Differences Between Variants:**
- Particle layer thickness varies slightly
- Particle layer density varies slightly
- Fuel kernel remains the same across all types
- Different number of embedded particles per compact type

### Key Structural Components

1. **Hafnium (Hf) Shroud:**
   - Surrounds entire circumference of capsule
   - Major contributor to dose rate (41.64% at 1 day, 62.11% at 30 days, 0.50% at 365 days)

2. **Stainless Steel Structures:**
   - Bottom support (SS316L)
   - Inner wall (SS316L)
   - Top support (SS316L)
   - Outer wall (SS316L)
   - Combined contribution: 42.54% at 365 days

3. **Graphite Components:**
   - Low graphite spacer
   - Upper graphite spacer
   - Borated graphite holder (contains boron, higher activation than spacers)

---

## MODELING SIMPLIFICATIONS USED

### Geometry Simplifications

1. **Hf shroud:** Modeled as surrounding entire capsule circumference (continuous)

2. **Omitted components:**
   - Gas lines
   - Thermocouples
   - Thru-tubes

3. **TRISO arrangement:** Regular lattice (not random)
   - Critical simplification for MCNP modeling
   - Actual fuel has random particle positions
   - Regular lattice allows repeated structures approach

### Why Regular Lattice Was Used

**Computational necessity:**
- One HTGR core = millions of TRISO particles
- Modeling each cell independently = not realistically possible
- Regular lattice enables MCNP repeated structures
- Enables explicit modeling of TRISO particles as decay sources

---

## TRISO FUEL PARTICLE STRUCTURE

### Layer Configuration

The AGR-1 experiment uses TRISO (TRistructural ISOtropic) particles with specific layered structure:

**Standard TRISO layers** (from center outward):
1. **Kernel:** UO₂ fuel (diameter varies by compact type)
2. **Buffer layer:** Porous carbon (absorbs fission gas)
3. **IPyC:** Inner pyrolytic carbon (gas-tight seal)
4. **SiC:** Silicon carbide (structural strength, fission product retention)
5. **OPyC:** Outer pyrolytic carbon (protective layer)

**Compact-specific variations:**
- Layer thicknesses differ between baseline, variant 1, variant 2, variant 3
- Layer densities differ between variants
- Number of particles per compact differs between variants
- Fuel kernel composition consistent across all variants

---

## PHOTON SOURCE CONTRIBUTIONS

### Time Evolution of Source Contributors

**After 1 Day Decay:**
- Fuel in TRISO: 53.19%
- Hf shroud: 41.64%
- Outer wall SS316L: 3.13%
- Top support SS316L: 0.85%
- Bottom support SS316L: 0.76%
- Inner wall SS316L: 0.43%
- Graphite components: Negligible (~10⁻⁷ to 10⁻¹⁰ %)
- **Total intensity:** 1.199 × 10¹⁵ γ/s

**After 30 Days Decay:**
- Hf shroud: 62.11% (dominant contributor)
- Fuel in TRISO: 30.03%
- Outer wall SS316L: 4.77%
- Top support SS316L: 1.30%
- Bottom support SS316L: 1.17%
- Inner wall SS316L: 0.63%
- Graphite components: Negligible (~10⁻⁶ to 10⁻⁹ %)
- **Total intensity:** 3.253 × 10¹⁴ γ/s (decreased by factor of ~3.7)

**After 365 Days Decay:**
- Fuel in TRISO: 56.95% (dominant contributor again)
- Outer wall SS316L: 25.90%
- Top support SS316L: 7.10%
- Bottom support SS316L: 6.47%
- Inner wall SS316L: 3.07%
- Hf shroud: 0.50% (dramatic decrease)
- Graphite components: Still negligible (~10⁻⁵ to 10⁻⁸ %)
- **Total intensity:** 1.305 × 10¹³ γ/s (decreased by factor of ~92 from 1 day)

### Key Observations

1. **Hf shroud behavior:**
   - Increases from 1 to 30 days
   - Drops dramatically by 365 days
   - Specific Hf isotope(s) growing then decaying

2. **Fuel contribution:**
   - Remains significant at all times
   - Dominant at 1 day and 365 days
   - Temporarily overshadowed at 30 days by Hf

3. **Stainless steel:**
   - Relatively minor early on
   - Becomes significant contributor at 365 days
   - Long-lived activation products

4. **Graphite:**
   - Essentially negligible at all times
   - Clean material with low activation

---

## DOSE RATE RESULTS

### Calculated Dose Rates by Distance and Time

**At 6 cm from center:**
- 1 day: 666.2 Sv/h
- 30 days: 190.3 Sv/h
- 365 days: 3.7 Sv/h

**At 46 cm from center:**
- 1 day: 72.7 Sv/h
- 30 days: 20.4 Sv/h
- 365 days: 0.4 Sv/h

**At 98 cm from center:**
- 1 day: 25.4 Sv/h
- 30 days: 7.3 Sv/h
- 365 days: 0.1 Sv/h

### Operational Implications

**Post-Irradiation Examination (PIE):**
- Even at ~1 m distance after 1 year decay: Exposure is HIGH
- PIE requires either:
  - Waiting > 1 year for decay
  - Using hot cell with appropriate shielding
- Personnel protection essential

---

## METHODOLOGY - REPEATED STRUCTURES APPROACH

### Verification Exercise (8×8 Pin Array)

**Purpose:** Verify repeated structures approach vs. explicit cell definition

**Geometry:**
- Simple LWR-like configuration
- 8×8 array of fuel pins
- 1.25 cm pin radius, 4 cm pitch
- 80 cm height, 32 cm inner shell side length
- Aluminum inner shell (2 cm thick)
- Light water reflector tank (40 cm radius)

**Results:**
- Neutron flux: <0.1% difference
- Photon intensity: <0.1% difference
- Delayed gamma heating: 15.6% difference (whole core as single universe)

**Key Finding:**
- Repeated structures with uniform flux assumption overestimates heating in periphery
- Grouping structures based on flux spatial variation improves accuracy
- Grouping in sets of 4 pins: 4.3% difference (acceptable)

**Conclusion:** Accuracy depends on accounting for flux spatial effects when grouping cells

### Implications for AGR-1 and HTGR Modeling

**Challenge:** Millions of TRISO particles cannot be modeled individually

**Solution:** Repeated structures with flux-based grouping
- Group TRISO particles by assembly (similar flux level)
- Each assembly has independent depletion
- Assumes uniform flux within assembly
- Balances accuracy vs. computational feasibility

**Critical consideration:** Group structures based on flux spatial variation, not just geometric convenience

---

## μHTGR MICROREACTOR EXAMPLE (COMPARATIVE CONTEXT)

### Reactor Configuration

**Core Layout:**
- 24 fuel assemblies
- 12 control assemblies
- 1 reserved shutdown assembly (center)
- Assembly pitch: 30 cm
- 4 axial layers of assemblies
- Core height: 272 cm (4 × 68 cm)
- Radial reflector radius: 134 cm

**Assembly Internal Structure:**
- Fuel channels: 1.15 cm radius
- Coolant channels: 0.775 cm radius
- Channel pitch: 3.2 cm
- Control assembly: 4 cm radius control rod hole
- Shutdown assembly: 6 cm radius control rod hole

### TRISO Particle Specifications

| Layer | Thickness (cm) | Material | Density (g/cm³) |
|-------|----------------|----------|-----------------|
| Kernel | 0.0250 | UO₂ (ε=19.75%) | 10.8 |
| Buffer | 0.0100 | C | 0.98 |
| IPyC | 0.0040 | C | 1.85 |
| SiC | 0.0035 | SiC | 3.20 |
| OPyC | 0.0040 | C | 1.86 |

**Fuel Compact Properties:**
- SiC matrix density: 3.2 g/cm³
- TRISO packing fraction: 40%
- Particle pitch: 0.1 cm (uniform distribution assumption)
- Graphite density (assemblies/reflector): 1.75 g/cm³

### μHTGR Modeling Approach

**Lattice Strategy:**
- Separate TRISO contribution by assembly
- Uniform flux assumed within each assembly
- Each assembly = independent depletion calculation
- Explicit TRISO particle modeling using repeated structures

**Cross Sections:** ENDF/B-VIII.0 at room temperature

**Simplifications:**
- RPV side wall neglected
- Concrete cavity modeled instead
- Portland concrete: 2.3 g/cm³, 100 cm thick, 191 cm from radial reflector

---

## CRITICAL INSIGHTS FOR LATTICE BUILDER

### Design Principles from AGR-1 Experience

1. **Regular Lattice Assumption:**
   - Trade-off between accuracy and computational feasibility
   - Acceptable for most reactor physics analyses
   - Essential for MCNP repeated structures approach
   - Alternative: Stochastic geometry (URAN card) for limited randomness

2. **Flux-Based Grouping:**
   - DO NOT group entire core as single universe if strong spatial flux effects
   - Group by similar flux levels (e.g., by assembly, by axial/radial zone)
   - Balance: More groups = more accuracy but more computational cost

3. **Multi-Level Hierarchies:**
   - Capsule level → Compact level → TRISO particle level
   - Core level → Assembly level → Fuel channel level → TRISO particle level
   - Proper universe nesting enables complex geometries

4. **Volume Specification:**
   - For repeated structures: Specify total volume across ALL instances
   - Critical for accurate source intensities
   - Example: 72 compacts → Volume = 72 × single compact volume

5. **Verification Strategy:**
   - Always compare against simpler reference case when possible
   - Check for flux spatial effects
   - Verify gamma source intensities are reasonable
   - Cross-check results at multiple decay times

### Practical Takeaways

**When modeling HTGR cores:**
- Use repeated structures for fuel particles (computational necessity)
- Arrange TRISO in regular lattice (computational feasibility)
- Group by assembly or zone (flux spatial variation)
- Each group = independent depletion (accuracy improvement)
- Verify with simplified problems first (validation)

**When modeling experiments like AGR-1:**
- Capsule-level organization natural for test trains
- Compact-level grouping appropriate scale
- Regular TRISO lattice within compacts acceptable
- Include structural materials (Hf shroud, SS, graphite) for activation

**Key limitation:**
- Regular lattice underestimates double heterogeneity effects
- Acceptable for most analyses
- For high-fidelity: Consider URAN card for limited randomness
- Critical safety analyses may require different approach

---

## TRANSLATION FROM LITERATURE TO MCNP

### Information Typically Available in Papers

**Geometric specifications:**
- Overall dimensions (height, radius)
- Lattice pitch
- Number of elements
- Layer thicknesses
- Material compositions

**Operating conditions:**
- Power level
- Irradiation duration
- Burnup

**Results for comparison:**
- k-effective evolution
- Flux distributions
- Dose rates
- Isotopic compositions

### Information Often Missing (Requires Assumptions)

**Detailed geometry:**
- Exact surface definitions
- Transformation matrices for tilted/rotated components
- Gap dimensions between components

**Material specifications:**
- Exact density values
- Isotopic enrichments
- Impurity levels
- Temperature-dependent properties

**Operational details:**
- Control rod positions
- Detailed power history
- Coolant flow distribution

### Recommended Approach

1. **Extract what's available:** Dimensions, compositions, power
2. **Make reasonable assumptions:** Standard values for missing data
3. **Document assumptions:** Clear statements in model description
4. **Sensitivity analysis:** Test impact of uncertain parameters
5. **Validate where possible:** Compare results to published values

---

## BENCHMARK CALCULATIONS (From Article)

### AGR-1 Depletion Benchmark

**Reference:** Sterbentz & Cogliati, INL, July 2018

**Contents:**
- Detailed capsule geometry
- TRISO particle specifications by variant
- Material compositions
- Power history (662 time steps over 13 cycles)
- OSCC positions
- Neck shim insertion conditions

**Benchmark Use:**
- Validation of MCNP models
- Verification of repeated structures approach
- Comparison of depletion calculations

### Key Validation Metrics

1. **Neutron flux distribution**
2. **Photon source intensities**
3. **Dose rates at specified locations**
4. **Isotopic evolution**
5. **Activation of structural materials**

---

## LESSONS FOR FUTURE MCNP MODELING

### From Verification Exercise

1. Whole-core single universe: 15.6% error (unacceptable)
2. Quarter-core grouping (4 pins): 4.3% error (acceptable)
3. Individual cells: 0% error (reference, but impractical for large systems)

**Rule of thumb:** Group by flux zone, not geometric convenience

### From AGR-1 Analysis

1. Include ALL activation sources (fuel, structures, shrouds)
2. Time-dependent contributions vary significantly
3. Short-lived isotopes dominate early (Hf at 30 days)
4. Long-lived isotopes dominate late (SS at 365 days)
5. Regular lattice sufficient for most purposes

### For HTGR Cores

1. Assembly-level grouping typically sufficient
2. Millions of particles → repeated structures mandatory
3. Explicit TRISO modeling achievable with proper organization
4. Uniform flux within assembly usually acceptable approximation
5. Always verify assumptions with sensitivity studies

---

**END OF AGR-1-KEY-INFO.MD**

**Next Steps:**
1. Use this information to inform mcnp-lattice-builder examples
2. Include AGR-1 as advanced lattice example in assets/
3. Reference in skill documentation for reactor modeling context
4. Emphasize flux-based grouping in best practices
