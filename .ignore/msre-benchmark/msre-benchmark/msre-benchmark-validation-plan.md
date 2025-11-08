# MSRE Benchmark Validation Plan

## Executive Summary

**Objective:** Validate that all MCNP "builder" skills can appropriately develop a full reactor model in MCNP strictly from science literature reactor design specifications and parameters.

**Approach:** Build complete, comprehensive MSRE (Molten Salt Reactor Experiment) reactor models from published literature specifications without any simplified approximations. Start with full-detail model based on MSRE_Overview_Spec.md, then iteratively refine to match exact Berkeley benchmark specifications.

**Key Principle:** MCNP can handle full complexity - no simplified models. Demonstrate that MCNP builder skills can create production-quality models from design specifications alone.

**Expected Outcome:** Prove MCNP skills can translate reactor design specifications from literature into accurate, validated MCNP models that match benchmark results (keff = 1.02132 ± 0.00003 with ENDF/B-VII.1).

---

## 1. VALIDATION OBJECTIVES

### 1.1 Primary Objectives

1. **Prove Literature-to-MCNP Translation Capability**
   - Extract all design parameters from published papers
   - Translate specifications into complete MCNP geometry
   - Create production-quality input decks without simplifications

2. **Validate All MCNP Builder Skills**
   - Test 14 MCNP skills comprehensively across all phases
   - Demonstrate each skill can handle complex, realistic reactor geometry
   - Verify skills work together in integrated workflow

3. **Match IRPhEP Benchmark Results**
   - Achieve keff = 1.02132 ± 0.00003 (Serpent/ENDF-VII.1 reference)
   - Reproduce 2.154% C-E discrepancy (expected for graphite systems)
   - Validate all geometric features match benchmark specification

4. **Demonstrate No-Simplification Approach**
   - Prove MCNP can handle full complexity (1,140 fuel channels, detailed lattice)
   - Show simplified models are unnecessary for MCNP
   - Create models suitable for production use, not just validation

### 1.2 Success Criteria

**Phase 2 (Initial Comprehensive Model):**
- ✓ MCNP runs without fatal errors
- ✓ Zero lost particles
- ✓ keff in range 1.00-1.03 (reasonable for first iteration)
- ✓ Shannon entropy converges
- ✓ All 1,140 fuel channels explicitly modeled
- ✓ Full lattice structure with proper indexing
- ✓ All materials with isotopics defined

**Phase 3 (Berkeley Benchmark Model):**
- ✓ keff = 1.02132 ± 0.00003 (match Serpent reference)
- ✓ Thermal expansion properly applied (293 K → 911 K)
- ✓ All dimensions match benchmark specification
- ✓ Material compositions match benchmark tables
- ✓ Thermal scattering laws correctly applied
- ✓ C-E discrepancy = 2.154% (as expected)

**Phase 4 (Validation Analysis):**
- ✓ All convergence criteria met
- ✓ Geometry plots match literature figures
- ✓ Mass inventories correct
- ✓ Physics verification complete
- ✓ Cross-reference checks pass

**Overall Integration Test:**
- ✓ All 14 MCNP skills successfully used
- ✓ Complete workflow from literature → production model
- ✓ Model suitable for further studies (burnup, transients, etc.)

---

## 2. REFERENCE DOCUMENTS

### 2.1 Primary Literature Sources

1. **msre-design-spec.md** (Created Phase 1)
   - Comprehensive extraction of all design parameters
   - Organized by geometry, materials, operating conditions
   - Complete uncertainty analysis
   - Modeling recommendations

2. **MSRE_Overview_Spec.md**
   - Section 2.3: MSRE description
   - Table 5: Key characteristics (dimensions, compositions)
   - Operating conditions and design specifications

3. **msre-benchmark-berkeley.md** (Shen et al., 2021)
   - IRPhEP benchmark specification
   - Detailed geometry and material specifications
   - Expected keff values and uncertainties
   - Thermal expansion methodology
   - Sensitivity studies and nuclear data comparisons

4. **msre-horizontal-cross-section.png**
   - Visual verification of radial geometry
   - Material layer identification
   - Lattice arrangement confirmation

5. **msre-vertical-cross-section.png**
   - Axial geometry verification
   - Component elevation relationships
   - Control rod and sample basket positions

### 2.2 Benchmark Expected Values

**Experimental (First Criticality, June 1, 1965):**
- keff: 1.0000 (by definition at criticality)
- Temperature: 911 K (1181°F)
- Power: ~10 W (zero power, stationary salt)
- Control rods: 2 withdrawn, 1 at 46.6 in. (3% insertion)

**Calculated (Serpent 2.1.30 / ENDF/B-VII.1):**
- keff: 1.02132 ± 0.00003
- C-E discrepancy: 2.154% or 2154 pcm
- Model bias (neglected components): -22 ± 5 pcm

**Uncertainties:**
- Experimental: ±420 pcm (1σ)
- Nuclear data: ±664 pcm (1σ)
- Total: Dominated by graphite density, ⁶Li enrichment, carbon cross sections

---

## 3. PHASE-BY-PHASE VALIDATION PLAN

### PHASE 1: Documentation Preparation ✓ COMPLETED

**Status:** COMPLETED
**Duration:** 30-45 minutes
**Deliverable:** msre-design-spec.md

**Accomplishments:**
- ✓ Extracted all geometry specifications (cold and hot dimensions)
- ✓ Compiled all material compositions with isotopics
- ✓ Documented operating conditions and temperatures
- ✓ Organized benchmark expected values
- ✓ Included complete uncertainty analysis
- ✓ Provided modeling recommendations

**Result:** Comprehensive 10-section, 1000+ line design specification document ready for model development.

---

### PHASE 2: Initial Comprehensive Lattice Model

**Objective:** Create first fully-detailed, production-quality MCNP model from MSRE_Overview_Spec.md specifications

**Duration:** 2-3 hours

**MCNP Skills to Invoke:**

1. **mcnp-lattice-builder**
   - Create full graphite lattice structure with 1,140 fuel passages
   - Define unit cell: graphite stringer + surrounding fuel channels
   - Implement LAT=1 rectangular lattice with proper indexing
   - Handle partial stringers at outer edge
   - Set up flux-based grouping for future burnup

2. **mcnp-geometry-builder**
   - Define all surfaces (cylinders, planes, complex features)
   - Create cell definitions for all regions
   - Build torispherical vessel heads
   - Model half-torus flow distributor
   - Define 3 control rod thimbles geometry
   - Define 3 sample basket geometries
   - Create thermal shield and insulation layers

3. **mcnp-material-builder**
   - Fuel salt: LiF-BeF2-ZrF4-UF4 with proper isotopics
   - Uranium isotopes: ²³⁴U, ²³⁵U, ²³⁶U, ²³⁸U at specified enrichment
   - Lithium isotopes: ⁶Li at 0.005 at.%, ⁷Li balance
   - Graphite: Natural carbon with boron impurity (0.8 ppm)
   - INOR-8: Ni-Mo-Cr-Fe-C alloy at proper composition
   - Control rod poison: 70% Gd₂O₃, 30% Al₂O₃
   - Type 304 stainless steel for thermal shield
   - Vermiculite insulation (homogenized mixture)

4. **mcnp-source-builder**
   - KCODE criticality source configuration
   - Initial source points distributed in fuel salt regions
   - 20-50 KSRC points covering core volume
   - Proper spatial distribution for convergence

5. **mcnp-physics-builder**
   - KCODE parameters: 100k histories, 50 skip, 200 active cycles
   - MODE N (neutron transport)
   - Temperature treatments (TMP cards for 911 K and 305 K)
   - Thermal scattering laws for graphite and water

6. **mcnp-cross-section-manager**
   - Configure ENDF/B-VII.1 library (.80c or .81c)
   - Set up thermal scattering: grph.12t (graphite at ~900K)
   - Set up thermal scattering: lwtr.XX (water in insulation)
   - Verify XSDIR path and library availability
   - Temperature interpolation setup

7. **mcnp-input-builder**
   - Assemble complete three-block structure
   - Organize cell cards by region (core, vessel, shield)
   - Organize surface cards by type (cylinders, planes, complex)
   - Organize data cards (materials, physics, source)
   - Add comprehensive comments and documentation
   - Create production-quality input deck

**Model Features (ALL Comprehensive - No Simplifications):**

**Geometry:**
- Full explicit lattice: 1,140 fuel channels in graphite stringers
- Graphite stringers: 5.08 cm × 5.08 cm square cross-section
- Fuel channels: 1.018 cm × 3.053 cm with 0.508 cm rounded corners
- Horizontal graphite lattice support (2 layers perpendicular)
- Partial stringers at outer edge of lattice
- 3 control rod thimbles with segmented poison sections (38 elements each)
- 3 sample baskets with individual graphite and INOR-8 samples
- Core can (INOR-8): 71.097-71.737 cm radius
- Reactor vessel (INOR-8): 74.299-76.862 cm radius
- Downcomer annulus: 2.54 cm width (void at criticality)
- Torispherical vessel heads (upper and lower)
- Half-torus flow distributor at vessel top
- Complete thermal shield and insulation (multiple shells)

**Dimensions:**
- Use hot dimensions from Table 5 (MSRE_Overview_Spec.md)
- Graphite lattice radius: 70.285 cm
- Graphite stringer height: 170.311 cm
- Total vessel height: 272.113 cm
- Core can height: 174.219 cm

**Materials:**
- Fuel salt: 64.88LiF-29.27BeF2-5.06ZrF4-0.79UF4 (molar %)
- Density: 2.3275 g/cm³
- ²³⁵U: 1.409 wt% of salt, ~93% enriched
- ⁶Li: 0.005 at.% in lithium
- Graphite: 1.8507 g/cm³ (or 1.86 g/cm³)
- INOR-8: 71% Ni, 17% Mo, 7% Cr, 5% Fe
- Control rod: 70% Gd₂O₃, 30% Al₂O₃, 5.873 g/cm³

**Physics:**
- Temperature: 911 K (core), 305 K (thermal shield)
- ENDF/B-VII.1 cross sections
- Thermal scattering: grph at 911 K, lwtr at 305 K
- KCODE: 100k histories, 50 skip, 200 active

**Control Rod Configuration:**
- Rod 1: Fully withdrawn (51 in. = 129.54 cm)
- Rod 2: Fully withdrawn (51 in. = 129.54 cm)
- Regulating rod: 46.6 in. = 118.364 cm (3% insertion)

**Expected Results:**
- keff: 1.00-1.03 (reasonable range for first iteration)
- Zero lost particles (MUST be zero)
- Shannon entropy convergence within 50 cycles
- Neutron balance closes
- Fission source distribution reasonable

**Success Criteria:**
- ✓ MCNP runs without fatal errors
- ✓ No geometry errors or lost particles
- ✓ Converged criticality calculation
- ✓ keff in physically reasonable range
- ✓ All lattice elements properly indexed
- ✓ Visual verification of geometry

**Deliverable:** `msre-model-v1.inp` - Complete comprehensive MCNP input file

---

### PHASE 3: Refined Berkeley Benchmark Model

**Objective:** Iteratively refine Phase 2 model to exactly match IRPhEP benchmark specification from Berkeley paper

**Duration:** 2-3 hours

**MCNP Skills to Invoke:**

1. **mcnp-geometry-editor**
   - Apply thermal expansion corrections (293 K → 911 K)
   - Update all dimensions from cold to hot values
   - Adjust lattice boundaries for thermal expansion
   - Refine control rod positions for exact benchmark match
   - Fine-tune torispherical head geometry

2. **mcnp-cross-reference-checker**
   - Verify all cell references to surfaces are valid
   - Check all FILL references to universes exist
   - Validate material assignments to all cells
   - Ensure no undefined universes or materials
   - Verify temperature assignments complete

3. **mcnp-input-validator**
   - Validate input syntax against benchmark specification
   - Check all dimensions match hot (911 K) values
   - Verify material compositions match benchmark tables
   - Validate control rod positions match criticality config
   - Check thermal scattering law assignments

4. **mcnp-material-builder** (refinement)
   - Refine salt composition to exact benchmark weight %
   - Verify uranium isotopic fractions (1.409%, 0.014%, 0.006%)
   - Confirm ⁶Li enrichment (0.005 at.%)
   - Add salt impurities if needed (Fe, Cr, Ni, O)
   - Verify graphite impurities (B, ash, V, S)
   - Check INOR-8 composition matches benchmark

5. **mcnp-physics-builder** (refinement)
   - Exact thermal scattering treatments
   - Temperature preprocessing to 911 K
   - Verify interpolation between thermal scattering libraries
   - Optimize KCODE parameters for <30 pcm uncertainty
   - Confirm cross-section temperature specifications

**Refinements from Phase 2 → Phase 3:**

**1. Thermal Expansion Applied:**
- Coefficients: Graphite 1.5×10⁻⁶ °F⁻¹, INOR-8 7.8×10⁻⁶ °F⁻¹
- Reference: Vessel expands downward from outlet pipe
- All cold dimensions (293 K) → hot dimensions (911 K)
- Document expansion methodology in comments

**2. Exact Hot Dimensions (911 K) - Per Berkeley Table I:**
```
Component                          Cold (293K)    Hot (911K)
Graphite lattice radius            70.168 cm      70.285 cm
Core can inner radius              70.485 cm      71.097 cm
Core can outer radius              71.120 cm      71.737 cm
Vessel inner radius                73.660 cm      74.299 cm
Vessel outer radius                76.200 cm      76.862 cm
Stringer width                     5.075 cm       5.084 cm
Fuel channel width                 1.016 cm       1.018 cm
Fuel channel length                3.048 cm       3.053 cm
Graphite stringer height           170.027 cm     170.311 cm
Total vessel height                269.771 cm     272.113 cm
Control rod inserted length        76.414 cm      77.077 cm
```

**3. Refined Salt Composition (Benchmark - Weight %):**
```
Element          Weight %
Li               10.957
Be               6.349
Zr               11.101
U                4.495
F                67.027
Impurities       0.071
Total            100.000
```

Uranium Isotopics:
- ²³⁵U: 1.409 ± 0.007 wt% of total salt
- ²³⁴U: 0.014 ± 0.007 wt%
- ²³⁶U: 0.006 ± 0.006 wt%
- ²³⁸U: Balance

Lithium Isotopics:
- ⁶Li: 0.005 ± 0.001 at.%
- ⁷Li: >99.99 at.%

Salt Impurities:
- Fe: 162 ± 65 ppm
- Cr: 28 ± 7 ppm
- Ni: 30 ± 20 ppm
- O: 490 ± 49 ppm

**4. Graphite Specification (Benchmark):**
- Density: 1.8507 g/cm³ (or test sensitivity with 1.86 g/cm³)
- Effective core height: 166.724 ± 1.0 cm
- Impurities:
  - Boron: 0.00008 ± 0.000008 wt%
  - Ash: 0.00050 ± 0.00005 wt%
  - Vanadium: 0.00090 ± 0.00009 wt%
  - Sulfur: 0.00050 ± 0.00005 wt%

**5. Thermal Scattering (Critical):**
- Carbon in graphite (core): 911 K via interpolation (800K-1000K libraries)
- Carbon in thermal shield: 305 K
- Hydrogen in insulation: 305 K (lwtr)
- Cross-sections: Preprocessed to 911 K by MCNP TMP cards
- Note: ±100 K in thermal scattering → ~600 pcm change in keff

**6. Control Rod Configuration (Exact Criticality State):**
- Control Rod 1: 51 in. (129.54 cm) - Fully withdrawn
- Control Rod 2: 51 in. (129.54 cm) - Fully withdrawn
- Regulating Rod: 46.6 in. (118.364 ± 0.127 cm) - 3% insertion
- Poison section length: 150.774 cm (38 segments of 3.968 cm each)

**7. KCODE Optimization:**
```
KCODE 100000 1.0 50 250
```
- 100,000 histories per cycle
- 50 skip cycles (for source convergence)
- 250 active cycles (for <30 pcm statistical uncertainty)
- Initial guess: keff = 1.0

**Expected Results:**
- keff: 1.02132 ± 0.00003 (match Serpent/ENDF-VII.1)
- Statistical uncertainty: <0.00003 (30 pcm)
- C-E discrepancy: 2.154% from experimental keff = 1.0000
- Shannon entropy: Converged and stable
- Neutron balance: Closed within statistics

**Success Criteria:**
- ✓ keff matches Serpent reference within ±200 pcm
- ✓ C-E discrepancy = 2.1-2.2% (expected for graphite systems)
- ✓ All dimensions exactly match Berkeley Table I
- ✓ All materials exactly match Berkeley tables
- ✓ Thermal expansion properly documented
- ✓ Statistical uncertainty < 30 pcm
- ✓ Zero lost particles

**Deliverable:** `msre-benchmark.inp` - Production-quality IRPhEP benchmark model

---

### PHASE 4: Comprehensive Analysis and Validation

**Objective:** Perform complete validation analysis on benchmark model

**Duration:** 1-2 hours

**MCNP Skills to Invoke:**

1. **mcnp-output-parser**
   - Extract final keff and uncertainty
   - Extract cycle-by-cycle keff values
   - Parse Shannon entropy history
   - Extract neutron balance (creation, loss, leakage)
   - Parse warnings and fatal messages (should be none)
   - Extract timing and performance data
   - Compile key results into summary table

2. **mcnp-statistics-checker**
   - Verify Shannon entropy convergence
   - Check source distribution stability
   - Validate skip cycles sufficient
   - Verify keff uncertainty acceptable (<30 pcm)
   - Check for statistical trends or anomalies
   - Validate figure of merit (FOM) behavior
   - Assess convergence quality metrics

3. **mcnp-tally-analyzer**
   - Analyze neutron spectrum in fuel vs graphite vs reflector
   - Extract reaction rates (fission, capture, scattering)
   - Assess flux distribution (thermal peak, fast component)
   - Calculate power distribution (if tallied)
   - Verify physics makes sense (thermal reactor characteristics)
   - Compare flux shapes to expected behavior

4. **mcnp-cross-reference-checker**
   - Final verification of model consistency
   - Check all cells reference valid surfaces
   - Verify all materials are defined and used
   - Confirm all surfaces referenced by cells
   - Validate universe hierarchy (no dangling references)
   - Check temperature assignments complete and consistent

5. **mcnp-plotter**
   - Generate horizontal cross-section plot (z = 145.396 cm)
   - Generate vertical cross-section plot (y = 0, offset for control rods)
   - Generate core center detail plot
   - Display lattice indices for verification
   - Create color-coded material plots
   - Export plots as PNG for documentation
   - Compare visually to literature Figures 5 & 6

6. **mcnp-variance-reducer**
   - Assess if variance reduction needed (should not be for criticality)
   - Check for any source convergence issues
   - Optimize if convergence is slow (unlikely)
   - Document any variance reduction applied (if any)

7. **mcnp-fatal-error-debugger**
   - Review output for any warnings or errors
   - Verify no fatal errors occurred (should be clean run)
   - Check for geometry warnings (should be none)
   - Validate no lost particles (must be zero)
   - Document clean run status

**Validation Tasks:**

**1. Eigenvalue Validation**
| Metric | Expected | Acceptance Criteria |
|--------|----------|---------------------|
| keff (calculated) | 1.02132 | 1.019-1.024 |
| Statistical uncertainty | ±0.00003 | <0.00005 |
| keff (experimental) | 1.0000 | Reference value |
| C-E discrepancy | 2.154% | 1.5-2.5% |
| C-E in pcm | 2154 pcm | ±500 pcm |

**2. Convergence Verification**
- Shannon entropy: Stable after ~20-50 cycles
- Shannon entropy value: ~7-8 (typical for large systems)
- No trends in active cycles
- keff by cycle: Random fluctuations only
- Source distribution: Converged and symmetric

**3. Geometry Verification**
- Visual plots match Figures 5 & 6 from literature
- Lost particles: ZERO (mandatory)
- Cell volumes: All positive and reasonable
- Fuel salt volume: ~4-5 m³ (estimate)
- Graphite volume: ~10-12 m³ (estimate)
- No overlapping cells
- No void regions unintended

**4. Material Verification**
- Atom density calculations correct (weight % → atoms/barn-cm)
- Salt composition: Check against benchmark table
- Uranium enrichment: ~93% ²³⁵U verified
- ⁶Li enrichment: 0.005 at.% verified
- Total uranium mass: Calculate and verify reasonable
- Material temperatures: 911 K (core), 305 K (shield) confirmed

**5. Physics Verification**
- Neutron balance closed (creation = loss + leakage)
- Leakage fraction: ~30-40% reasonable for reflected system
- Thermal flux peak: Should be in graphite moderator
- Fast flux peak: Should be in fuel salt channels
- Spectrum: Thermal reactor characteristic (peak ~0.025 eV)
- Fission rate: Highest in center, falls toward edges

**6. Cross-Reference Checks**
- All 1,140+ cells reference valid surfaces ✓
- All lattice FILL references point to defined universes ✓
- All materials (M cards) are assigned to cells ✓
- All surfaces referenced by at least one cell ✓
- Temperature (TMP) assignments complete ✓
- Thermal scattering (MT) assignments correct ✓

**Expected Results Summary:**
```
FINAL VALIDATION RESULTS:
========================
Model: msre-benchmark.inp (IRPhEP specification)
Code: MCNP6 (or MCNP5)
Library: ENDF/B-VII.1
Date: [Run date]

EIGENVALUE RESULTS:
keff (final):           1.02132 ± 0.00003
keff (experimental):    1.00000 (by definition)
C-E discrepancy:        2.154% (2154 pcm)
Expected C-E:           2.154% (match!)
Statistical unc:        ±30 pcm (excellent)

CONVERGENCE:
Shannon entropy:        Converged cycle 45, stable after
Lost particles:         0 (PASS)
Skip cycles:            50 (adequate)
Active cycles:          250 (excellent statistics)

GEOMETRY:
Total cells:            ~1200+ (full lattice detail)
Fuel channels:          1,140 (explicit)
Lattice elements:       All properly indexed
Visual verification:    Matches literature figures

PHYSICS:
Neutron balance:        Closed (PASS)
Spectrum:               Thermal peak confirmed
Flux distribution:      Symmetric, peaked at center
Control rod effect:     3% insertion modeled

VALIDATION STATUS:      ✓ PASS
Benchmark match:        ✓ EXCELLENT
Production ready:       ✓ YES
```

**Success Criteria:**
- ✓ keff = 1.02132 ± 0.00003
- ✓ C-E discrepancy = 2.154%
- ✓ All convergence metrics passed
- ✓ Geometry verified visually
- ✓ Physics validated
- ✓ Zero errors, zero lost particles
- ✓ Production-quality model confirmed

**Deliverables:**
- `msre-validation-results.txt` - Complete output analysis
- `msre-horizontal-section-mcnp.png` - Horizontal cross-section plot
- `msre-vertical-section-mcnp.png` - Vertical cross-section plot
- `msre-core-center-mcnp.png` - Core center detail plot
- `msre-convergence-analysis.txt` - Statistics summary

---

### PHASE 5: Sensitivity Studies

**Objective:** Demonstrate nuclear data impact and parameter sensitivity

**Duration:** 1-2 hours

**MCNP Skills to Invoke:**

1. **mcnp-cross-section-manager**
   - Switch between ENDF/B-VII.1 and JENDL-4.0 libraries
   - Configure different thermal scattering temperatures
   - Test carbon cross-section variations
   - Document library differences

2. **mcnp-material-builder**
   - Create alternative salt compositions
   - Implement chemical analysis composition
   - Implement anticipated composition
   - Vary densities within uncertainties

3. **mcnp-input-editor**
   - Modify parameters for sensitivity studies
   - Create input variants systematically
   - Document changes clearly

4. **mcnp-output-parser**
   - Extract results from all sensitivity runs
   - Compare keff values
   - Calculate differences (Δk in pcm)
   - Compile sensitivity matrix

**Sensitivity Studies:**

**Study 1: Nuclear Data Libraries**

Test different cross-section libraries to quantify nuclear data uncertainty:

| Library | Expected keff | Expected Δk vs ENDF-VII.1 |
|---------|---------------|---------------------------|
| ENDF/B-VII.1 (baseline) | 1.02132 | 0 pcm (reference) |
| JENDL-4.0 (all nuclides) | 1.02061 | -71 pcm |
| ENDF-VII.1 with JENDL C | 1.01954 | -178 pcm |

**Interpretation:** Carbon cross-section data has major impact (~178 pcm). Library choice significant (~71 pcm).

**Study 2: Thermal Scattering Temperature Sensitivity**

Test thermal scattering law temperature dependence:

| Graphite S(α,β) Temp | Expected keff | Expected Δk vs 911K |
|----------------------|---------------|---------------------|
| 800 K | 1.02723 | +591 pcm |
| 911 K (benchmark) | 1.02132 | 0 pcm |
| 1000 K | 1.01640 | -492 pcm |

**Interpretation:** EXTREME sensitivity (~600 pcm per 100 K). Accurate thermal scattering temperature is CRITICAL.

**Study 3: Salt Composition Variations**

Test documented alternative salt compositions:

| Composition | Expected keff | Expected Δk vs Benchmark |
|-------------|---------------|--------------------------|
| Benchmark (selected) | 1.02132 | 0 pcm |
| Chemical analysis | 1.02248 | +116 pcm |
| Anticipated | 1.02595 | +463 pcm |

**Interpretation:** Salt composition uncertainty ~100-500 pcm. Benchmark selection justified by ²³⁵U mass fraction agreement.

**Study 4: Major Parameter Uncertainties**

Test parameters with largest uncertainty impact:

| Parameter | Nominal | Perturbation | Expected Δk (pcm) |
|-----------|---------|--------------|-------------------|
| Graphite density | 1.86 g/cm³ | ±0.02 g/cm³ | ±334 |
| ⁶Li enrichment | 0.005 at.% | ±0.001 at.% | ±172 |
| Salt density | 2.3275 g/cm³ | ±0.016 g/cm³ | ±103 |
| ²³⁵U mass fraction | 1.409 wt% | ±0.007 wt% | ±81 |
| ²³⁴U mass fraction | 0.014 wt% | ±0.007 wt% | ±74 |
| Fuel channel width | 1.018 cm | ±0.0127 cm | ±51 |

**Interpretation:** Graphite density dominates experimental uncertainty. Moderator characterization critical for graphite-moderated systems.

**Expected Results:**
- All sensitivity studies confirm literature values within statistical uncertainty
- Nuclear data choice matters significantly (~71-178 pcm)
- Thermal scattering temperature CRITICAL (~1100 pcm total range)
- Salt composition matters but benchmark selection validated
- Graphite density is largest experimental uncertainty contributor

**Success Criteria:**
- ✓ JENDL-4.0 difference = -71 ± 10 pcm
- ✓ Thermal scattering sensitivity = ~600 pcm per 100 K
- ✓ Salt composition variations match literature
- ✓ Major parameter sensitivities reproduce benchmark Table IV

**Deliverables:**
- `msre-sensitivity-study-results.md` - Complete sensitivity analysis
- Multiple input files: `msre-benchmark-jendl.inp`, `msre-benchmark-chem-analysis.inp`, etc.
- Comparison tables and plots

---

### PHASE 6: Documentation and Reporting

**Objective:** Create comprehensive validation report documenting entire process

**Duration:** 1-2 hours

**Deliverables:**

**1. msre-design-spec.md** ✓ COMPLETED
- Comprehensive design specification (10 sections)
- All geometry, materials, operating conditions
- Benchmark expected values
- Uncertainty analysis
- Modeling recommendations

**2. msre-benchmark-validation-plan.md** (THIS DOCUMENT)
- Complete validation strategy
- Phase-by-phase plan with success criteria
- MCNP skills invocation schedule
- Expected results and acceptance criteria
- Timeline and resource estimates

**3. msre-model-v1.inp**
- Phase 2 comprehensive model (MSRE_Overview_Spec basis)
- Full lattice structure, no simplifications
- Extensively commented
- Production-quality input

**4. msre-benchmark.inp**
- Phase 3 refined benchmark model (Berkeley basis)
- Exact IRPhEP specification
- Thermal expansion applied
- Production-quality, validation-ready

**5. msre-validation-report.md**
- Executive summary of results
- Model description and methodology
- Results tables (keff, uncertainties, convergence)
- Geometry verification (plots, volumes, masses)
- Material inventory verification
- Statistical analysis (convergence, uncertainties)
- Sensitivity study results
- Comparison to benchmark expected values
- Skills validation assessment (all 14 skills tested)
- Lessons learned and recommendations
- Conclusion: Integration test success/failure

**6. Geometry Plots**
- `msre-horizontal-section-mcnp.png` - Compare to literature Figure 5
- `msre-vertical-section-mcnp.png` - Compare to literature Figure 6
- `msre-core-center-mcnp.png` - Control rods and sample baskets detail
- Side-by-side comparisons with literature figures

**7. Output Files**
- `msre-model-v1.out` - Phase 2 output
- `msre-benchmark.out` - Phase 3 output
- Various sensitivity study outputs
- Extracted results summaries

**8. Sensitivity Study Documentation**
- `msre-sensitivity-study-results.md` - Complete analysis
- Input files for all sensitivity cases
- Results comparison tables
- Discussion of nuclear data impact

**Final Report Structure:**
```
MSRE BENCHMARK VALIDATION REPORT
=================================

1. EXECUTIVE SUMMARY
   - Objectives achieved
   - Key results
   - Skills validated
   - Conclusions

2. INTRODUCTION
   - MSRE background
   - IRPhEP benchmark description
   - Validation objectives
   - Success criteria

3. METHODOLOGY
   - Literature review and specification extraction
   - MCNP model development approach
   - Skills invocation workflow
   - Quality assurance procedures

4. MODEL DESCRIPTION
   - Geometry (full lattice, vessels, shields)
   - Materials (compositions, densities, isotopics)
   - Physics (temperatures, cross sections, thermal scattering)
   - Source and criticality calculation setup

5. RESULTS
   - Phase 2: Initial comprehensive model
   - Phase 3: Refined benchmark model
   - Eigenvalue comparison to benchmark
   - Convergence analysis
   - Geometry verification
   - Material verification
   - Physics verification

6. SENSITIVITY STUDIES
   - Nuclear data libraries (ENDF vs JENDL)
   - Thermal scattering temperature
   - Salt composition variations
   - Major parameter uncertainties
   - Comparison to literature values

7. SKILLS VALIDATION ASSESSMENT
   - mcnp-lattice-builder: [Assessment]
   - mcnp-geometry-builder: [Assessment]
   - mcnp-material-builder: [Assessment]
   - mcnp-source-builder: [Assessment]
   - mcnp-physics-builder: [Assessment]
   - mcnp-cross-section-manager: [Assessment]
   - mcnp-input-builder: [Assessment]
   - mcnp-output-parser: [Assessment]
   - mcnp-statistics-checker: [Assessment]
   - mcnp-tally-analyzer: [Assessment]
   - mcnp-cross-reference-checker: [Assessment]
   - mcnp-plotter: [Assessment]
   - mcnp-variance-reducer: [Assessment]
   - mcnp-fatal-error-debugger: [Assessment]

8. DISCUSSION
   - Literature-to-MCNP translation success
   - Comparison to IRPhEP benchmark
   - C-E discrepancy (2.154%) - expected for graphite systems
   - Model quality and production readiness
   - Limitations and assumptions
   - Recommendations for future work

9. CONCLUSIONS
   - Integration test: PASS/FAIL
   - All skills successfully validated: YES/NO
   - Production-quality model achieved: YES/NO
   - Benchmark results reproduced: YES/NO
   - Lessons learned
   - Final assessment

10. REFERENCES
    - All literature sources
    - MCNP documentation
    - IRPhEP handbook
    - Nuclear data libraries

APPENDICES:
A. Complete design specification
B. Input file listings (key sections)
C. Geometry plots
D. Convergence plots
E. Sensitivity study detailed results
F. Quality assurance checklists
```

---

## 4. MCNP SKILLS VALIDATION MATRIX

### 4.1 Skills to Be Tested

| Skill # | Skill Name | Phase(s) Used | Capability Tested | Pass Criteria |
|---------|-----------|---------------|-------------------|---------------|
| 1 | mcnp-lattice-builder | 2 | Complex lattice (1,140 channels), flux-based grouping | Lattice correct, proper indexing |
| 2 | mcnp-geometry-builder | 2, 3 | Multi-region cylinders, complex surfaces, torispherical heads | All geometry correct, zero lost particles |
| 3 | mcnp-material-builder | 2, 3, 5 | Complex mixtures, isotopics, impurities | Materials match specs, proper atom densities |
| 4 | mcnp-source-builder | 2 | Criticality source in complex geometry | Good initial distribution, fast convergence |
| 5 | mcnp-physics-builder | 2, 3 | KCODE, temperatures, thermal scattering | Proper physics setup, correct results |
| 6 | mcnp-cross-section-manager | 2, 3, 5 | ENDF/B-VII.1, thermal scattering laws, library switching | Libraries correctly applied |
| 7 | mcnp-input-builder | 2, 3 | Complete production input assembly | Clean, organized, documented input |
| 8 | mcnp-output-parser | 4, 5 | Extract results, convergence data | All key results extracted correctly |
| 9 | mcnp-statistics-checker | 4 | Verify convergence, uncertainties | Convergence confirmed, stats acceptable |
| 10 | mcnp-tally-analyzer | 4 | Physics analysis, flux spectra | Reasonable physics validated |
| 11 | mcnp-cross-reference-checker | 3, 4 | Model consistency verification | All references valid |
| 12 | mcnp-plotter | 4 | Geometry visualization | Plots match literature |
| 13 | mcnp-variance-reducer | 4 | Convergence optimization (if needed) | Applied if necessary |
| 14 | mcnp-fatal-error-debugger | 4 | Error resolution | No errors to debug (clean run) |

### 4.2 Integration Test Assessment

**Overall Integration Test Goal:**
Prove MCNP builder skills can translate reactor design specifications from published literature into accurate, validated, production-quality MCNP models without simplifications.

**Success Criteria:**
- ✓ All 14 skills successfully invoked and tested
- ✓ Complete workflow from literature → production model
- ✓ keff matches benchmark: 1.02132 ± 0.00003
- ✓ C-E discrepancy matches expected: 2.154%
- ✓ All geometry features properly modeled
- ✓ All materials correctly specified
- ✓ Model suitable for further studies (burnup, transients, etc.)
- ✓ Zero simplifications required (MCNP handles full complexity)
- ✓ Production-quality documentation created

**Assessment Categories:**

1. **Literature Translation** (Critical)
   - Can skills extract design specs from papers? YES/NO
   - Are specifications sufficient for modeling? YES/NO
   - Are missing parameters handled appropriately? YES/NO

2. **Geometry Capability** (Critical)
   - Can skills handle 1,140-channel lattice? YES/NO
   - Are complex surfaces (torispherical, torus) modeled? YES/NO
   - Is thermal expansion properly applied? YES/NO

3. **Material Capability** (Critical)
   - Are complex mixtures properly defined? YES/NO
   - Are isotopics correctly specified? YES/NO
   - Are impurities appropriately included? YES/NO

4. **Physics Capability** (Critical)
   - Are thermal scattering laws correctly applied? YES/NO
   - Is temperature treatment proper? YES/NO
   - Is criticality calculation configured correctly? YES/NO

5. **Validation Capability** (Critical)
   - Does model match benchmark results? YES/NO
   - Are uncertainties properly assessed? YES/NO
   - Is quality assurance comprehensive? YES/NO

6. **Production Readiness** (Important)
   - Is model suitable for production use? YES/NO
   - Is documentation complete? YES/NO
   - Can model be extended for other studies? YES/NO

**Final Verdict:** PASS / FAIL / PARTIAL PASS

---

## 5. TIMELINE AND RESOURCE ESTIMATES

### 5.1 Phase Duration Estimates

| Phase | Description | Estimated Duration | Status |
|-------|-------------|-------------------|--------|
| 1 | Documentation Preparation | 30-45 min | ✓ COMPLETED |
| 2 | Initial Comprehensive Model | 2-3 hours | PENDING |
| 3 | Refined Benchmark Model | 2-3 hours | PENDING |
| 4 | Validation Analysis | 1-2 hours | PENDING |
| 5 | Sensitivity Studies | 1-2 hours | PENDING |
| 6 | Final Documentation | 1-2 hours | PENDING |
| **TOTAL** | **Complete Validation** | **7.5-12.5 hours** | **IN PROGRESS** |

### 5.2 Computational Resource Estimates

**MCNP Run Times (estimated):**
- Phase 2 model: 2-6 hours (depending on hardware, 100k histories × 250 cycles)
- Phase 3 model: 2-6 hours (same configuration)
- Sensitivity studies: 1-2 hours each × 8 studies = 8-16 hours
- Total MCNP runtime: ~12-28 hours

**Hardware Recommendations:**
- Modern multi-core CPU (8+ cores)
- 16+ GB RAM
- MCNP6 or MCNP6.2 (or MCNP5 acceptable)
- ENDF/B-VII.1 cross-section libraries installed
- Optional: JENDL-4.0 for sensitivity studies

**Parallelization:**
- Use MPI or OpenMP if available
- Speedup: ~6-8x with 8 cores
- Reduces wall time to 2-4 hours per major run

### 5.3 Critical Path Items

**Blockers (Must resolve before proceeding):**
1. MCNP skills invocation (currently not working) - **CRITICAL**
2. ENDF/B-VII.1 library availability verification
3. Thermal scattering libraries at appropriate temperatures

**Dependencies:**
- Phase 2 must complete before Phase 3
- Phase 3 must complete before Phase 4
- Phase 4 must complete before Phase 5
- All phases must complete before Phase 6

---

## 6. QUALITY ASSURANCE

### 6.1 QA Checkpoints

**Before Each MCNP Run:**
- [ ] All dimensions verified against specifications
- [ ] All material compositions verified against tables
- [ ] Temperature assignments checked (911 K core, 305 K shield)
- [ ] Thermal scattering laws assigned correctly
- [ ] KCODE parameters appropriate
- [ ] Multiple KSRC points distributed spatially
- [ ] All cells have valid surface definitions
- [ ] No syntax errors in input

**After Each MCNP Run:**
- [ ] Zero lost particles (MANDATORY)
- [ ] Shannon entropy converged
- [ ] keff in reasonable range
- [ ] Statistical uncertainty acceptable
- [ ] Neutron balance closed
- [ ] No fatal errors or warnings
- [ ] Geometry plots match expectations
- [ ] Mass inventories reasonable

**Final Validation:**
- [ ] keff matches benchmark: 1.02132 ± 0.00003
- [ ] C-E discrepancy = 2.154%
- [ ] All geometry features verified visually
- [ ] All materials verified against tables
- [ ] All physics treatments verified
- [ ] All 14 skills successfully utilized
- [ ] Production-quality model confirmed
- [ ] Complete documentation delivered

### 6.2 Acceptance Criteria Summary

**Phase 2 Acceptance:**
- MCNP runs successfully (no fatal errors)
- keff = 1.00-1.03 (reasonable range)
- Zero lost particles
- Converged criticality calculation
- Full lattice modeled (1,140 channels)

**Phase 3 Acceptance:**
- keff = 1.021 ± 0.003 (within 200 pcm of Serpent reference)
- Dimensions match Berkeley Table I
- Materials match Berkeley tables
- Thermal expansion applied correctly
- Statistical uncertainty < 50 pcm

**Phase 4 Acceptance:**
- All convergence criteria met
- Geometry verified (plots match literature)
- Materials verified (inventories correct)
- Physics validated (reasonable distributions)
- Cross-references checked (all valid)
- Zero errors, zero lost particles

**Phase 5 Acceptance:**
- All sensitivity studies complete
- Results match literature expectations
- JENDL-4.0 difference = -71 ± 20 pcm
- Thermal scattering sensitivity confirmed
- Major parameter sensitivities reproduced

**Overall Integration Test Acceptance:**
- All phases completed successfully
- All 14 skills validated
- keff matches benchmark
- C-E discrepancy matches expected
- Production-quality model delivered
- Complete documentation delivered

---

## 7. RISK MANAGEMENT

### 7.1 Identified Risks

**Risk 1: MCNP Skills Not Invoking**
- **Status:** CURRENT BLOCKER
- **Impact:** HIGH - Cannot proceed with planned workflow
- **Mitigation:**
  - Debug skill invocation mechanism
  - Alternative: Manual modeling using skill documentation
  - Alternative: Restart session to refresh skill discovery

**Risk 2: ENDF/B-VII.1 Library Not Available**
- **Status:** POTENTIAL
- **Impact:** HIGH - Cannot reproduce benchmark results
- **Mitigation:**
  - Verify library installation before extensive modeling
  - Download ENDF/B-VII.1 if needed
  - Alternative: Use ENDF/B-VIII.0 with documented differences

**Risk 3: Thermal Scattering Libraries Missing**
- **Status:** POTENTIAL
- **Impact:** HIGH - 600 pcm error possible
- **Mitigation:**
  - Verify grph and lwtr libraries at needed temperatures
  - Extract from MCNP data distributions if needed
  - Document any temperature interpolation

**Risk 4: Model Too Complex (Convergence Issues)**
- **Status:** LOW RISK (MCNP handles complexity well)
- **Impact:** MEDIUM - Slow convergence, need more cycles
- **Mitigation:**
  - Use good initial source distribution (multiple KSRC points)
  - Increase skip cycles if needed (50 → 100)
  - Monitor Shannon entropy carefully

**Risk 5: keff Significantly Different from Benchmark**
- **Status:** POSSIBLE (many parameters)
- **Impact:** MEDIUM - Model validation failed
- **Mitigation:**
  - Systematic verification of all dimensions
  - Careful atom density calculations
  - Check thermal expansion application
  - Verify thermal scattering temperature
  - Expected range: 1.019-1.024 acceptable

**Risk 6: Lost Particles**
- **Status:** POSSIBLE (complex geometry)
- **Impact:** HIGH - Indicates geometry errors
- **Mitigation:**
  - Careful geometry construction
  - Verify all cell definitions
  - Check surface ordering on LAT cells
  - Use geometry plotter extensively
  - Fix any lost particle issues before production runs

### 7.2 Contingency Plans

**If skills cannot be invoked:**
- Proceed with manual MCNP model development
- Use skill documentation (SKILL.md files) as guidance
- Reference skill templates and examples
- Document process for skill validation report
- Still achieves objective (prove specs sufficient for modeling)

**If keff significantly off (>500 pcm difference):**
- Systematic debugging:
  1. Verify geometry (visual inspection)
  2. Check material compositions (atom densities)
  3. Verify thermal scattering (major impact)
  4. Check thermal expansion (dimensions)
  5. Validate control rod positions
- Compare to Phase 2 result for trends
- Document any necessary corrections

**If convergence problems:**
- Increase skip cycles (50 → 100 → 200)
- Add more KSRC points (20 → 50 → 100)
- Check for geometry errors (lost particles)
- Verify source distribution reasonable
- May need to run longer (250 → 500 cycles)

---

## 8. SUCCESS METRICS

### 8.1 Quantitative Metrics

| Metric | Target | Acceptable Range | Priority |
|--------|--------|------------------|----------|
| keff (calculated) | 1.02132 | 1.019-1.024 | CRITICAL |
| Statistical uncertainty | <30 pcm | <50 pcm | HIGH |
| C-E discrepancy | 2.154% | 1.5-2.5% | CRITICAL |
| Lost particles | 0 | 0 (no tolerance) | CRITICAL |
| Shannon entropy convergence | <50 cycles | <100 cycles | MEDIUM |
| Skills successfully tested | 14 | ≥12 | HIGH |
| Phases completed | 6 | ≥5 | HIGH |
| MCNP run success rate | 100% | ≥90% | MEDIUM |

### 8.2 Qualitative Metrics

**Model Quality:**
- [ ] Geometry matches literature descriptions
- [ ] Materials properly defined with isotopics
- [ ] Physics treatments appropriate
- [ ] Input well-organized and documented
- [ ] Suitable for production use

**Validation Quality:**
- [ ] Comprehensive analysis performed
- [ ] All key parameters verified
- [ ] Sensitivity studies complete
- [ ] Results properly documented
- [ ] Comparisons to benchmark thorough

**Integration Test Quality:**
- [ ] Literature-to-MCNP translation successful
- [ ] All skills tested in realistic workflow
- [ ] No simplifications required
- [ ] Process well-documented
- [ ] Lessons learned captured

### 8.3 Final Assessment Rubric

**PASS Criteria (All must be met):**
1. keff matches benchmark: 1.019-1.024
2. C-E discrepancy correct: 1.5-2.5%
3. All geometry features properly modeled
4. All materials correctly specified
5. Zero lost particles (MANDATORY)
6. All phases completed (2-6)
7. At least 12 of 14 skills successfully tested
8. Production-quality model delivered
9. Complete documentation delivered

**PARTIAL PASS Criteria:**
- Most criteria met but some deficiencies
- keff within 1000 pcm of target
- Minor geometry or material issues
- Some skills not tested
- Documentation incomplete

**FAIL Criteria:**
- keff >1000 pcm from target
- Major geometry or material errors
- Lost particles present
- Cannot complete key phases
- Skills fundamentally inadequate for task

---

## 9. LESSONS LEARNED (To Be Updated)

### 9.1 Technical Lessons

**What Worked Well:**
- [To be filled during/after validation]
- Comprehensive design specification very helpful
- Literature review thorough and complete
- ...

**What Could Be Improved:**
- [To be filled during/after validation]
- Skill invocation mechanism needs debugging
- ...

**Unexpected Challenges:**
- [To be filled during/after validation]
- Skills not discoverable in current session
- ...

**Best Practices Identified:**
- [To be filled during/after validation]
- Start with complete design spec
- No simplifications approach works well
- ...

### 9.2 Process Lessons

**Project Management:**
- [To be filled during/after validation]

**Documentation:**
- [To be filled during/after validation]

**Quality Assurance:**
- [To be filled during/after validation]

### 9.3 Skills Assessment Lessons

**Skills That Exceeded Expectations:**
- [To be filled during/after validation]

**Skills That Need Improvement:**
- [To be filled during/after validation]

**Skills Gaps Identified:**
- [To be filled during/after validation]

**Recommendations for Skill Enhancement:**
- [To be filled during/after validation]

---

## 10. CONCLUSIONS AND NEXT STEPS

### 10.1 Current Status

**Completed:**
- ✓ Phase 1: Documentation Preparation (msre-design-spec.md)
- ✓ Validation plan creation (this document)
- ✓ Literature review and parameter extraction
- ✓ Success criteria definition

**In Progress:**
- Phase 2: Initial comprehensive model development
- Resolving skill invocation issue

**Pending:**
- Phase 3: Benchmark model refinement
- Phase 4: Validation analysis
- Phase 5: Sensitivity studies
- Phase 6: Final documentation

### 10.2 Immediate Next Steps

1. **Resolve skill invocation issue** (BLOCKER)
   - Debug why skills not discoverable in current session
   - Alternative: Proceed with manual modeling using skill documentation

2. **Begin Phase 2 model development**
   - Invoke mcnp-lattice-builder (or implement lattice manually)
   - Build complete MSRE geometry
   - Define all materials
   - Set up criticality calculation

3. **Run Phase 2 model**
   - Execute MCNP calculation
   - Verify basic functionality
   - Check keff in reasonable range

4. **Proceed through remaining phases**
   - Refine to benchmark specification
   - Perform validation analysis
   - Execute sensitivity studies
   - Complete final documentation

### 10.3 Long-Term Vision

**If Integration Test Successful:**
- MCNP skills proven capable of literature-to-model translation
- Expand to other reactor types (PWR, BWR, HTGR, fast reactors)
- Create library of validated benchmark models
- Develop automated literature-to-MCNP translation tools
- Share validated models with community

**If Integration Test Identifies Gaps:**
- Document specific skill deficiencies
- Develop additional skills or enhance existing ones
- Create targeted training materials
- Refine skill invocation and discovery mechanisms
- Iterate until comprehensive capability achieved

### 10.4 Final Thoughts

This MSRE benchmark validation represents a comprehensive test of MCNP builder skills' ability to translate published reactor design specifications into accurate, production-quality neutronics models. By choosing a well-documented, experimentally-validated benchmark and requiring NO simplifications, we set a high bar for success.

The validation plan ensures systematic, thorough testing across all model development phases - from initial geometry construction through final validation and sensitivity studies. Success will definitively prove that MCNP skills can handle real-world reactor modeling workflows from literature alone.

The no-simplification approach demonstrates MCNP's power - a full 1,140-channel explicit lattice with complex geometry, detailed materials, and proper physics treatments. This is production-quality modeling, not just a validation exercise.

**Expected outcome:** Complete validation success, proving MCNP builder skills are ready for production reactor modeling tasks.

---

**Document Version:** 1.0
**Date Created:** November 4, 2025
**Status:** Phase 1 Complete, Phase 2 Pending
**Next Review:** After Phase 2 completion

**END OF VALIDATION PLAN**
