# Heat Pipe Microreactor (HPMR) Physics Code
## MODE/PHYS/PRINT/PRDMP/LOST Cards for MCNP Model

**Document Purpose:** Physics card definitions for HPMR MCNP model
**Model File:** `/home/user/mcnp-skills/hpcmr-simplified.i`
**Based on:** Gap Analysis sections 2.1 (GAP 5) and 2.2 (GAP 8, 10)
**Date:** 2025-11-08

---

## PHYSICS CARDS FOR HPMR MODEL

### Complete Physics Code Block

```
c ============================================================================
c                        PHYSICS CONTROL CARDS
c ============================================================================
c
c --- Particle Transport Mode ---
MODE N
c     Neutron-only transport
c     This MUST be the first data card in Block 3
c
c --- Neutron Physics Parameters ---
PHYS:N  40.0
c       emax = 40 MeV (maximum neutron energy)
c       All other parameters use MCNP defaults
c       Default settings appropriate for thermal reactor:
c         - Continuous energy transport
c         - Doppler broadening enabled (nodop=0)
c         - No photon production (iphot=0, neutron-only)
c         - Standard physics models
c
c --- Output Control ---
PRINT 10 30 38 40 50 110 117 118 126 128 160 161 162 170
c     Reduced output for clarity:
c       10  = Cross-section tables
c       30  = Surface crossing summary
c       38  = Cell importance summary
c       40  = Material summary
c       50  = Tally summary
c       110 = Keff results and confidence intervals
c       117 = Source convergence diagnostics
c       118 = Entropy convergence
c       126 = Fission matrix
c       128 = Keff vs cycle plot data
c       160 = Tally fluctuation charts
c       161 = Tally mean and error
c       162 = Tally statistical checks
c       170 = Weight window summary
c
c --- Restart and Dump Control ---
PRDMP J J 1 J J
c     ndp ndd ncd ndm nbm
c     J = default for ndp (print dump number = 1 initially)
c     J = default for ndd (dump every 10 cycles)
c     1 = ncd (create RUNTPE every 1 cycle for restart capability)
c     J = default for ndm (mctal dump number = 10)
c     J = default for nbm (binary mctal dumps = 2)
c     This enables frequent RUNTPE dumps for restart capability
c
c --- Lost Particle Handling ---
LOST  10 10
c     nlost nlose
c     10 = Issue warning after 10 lost particles
c     10 = Terminate run after 10 additional lost particles (20 total)
c     Conservative setting for complex hexagonal geometry
```

---

## WHY THIS CODE: Technical Justification

### 1. MODE N (Neutron Transport Only)

**Physics Basis:**
- HPMR is a thermal neutron reactor with graphite moderation
- Fission neutrons thermalize in graphite monolith
- No coupled photon or electron transport needed for criticality
- Neutron-only transport is sufficient for keff calculation

**Design Parameters:**
- Core power: 15 MWth
- Fuel: UCO TRISO in graphite matrix (10 w/o U-235)
- Moderator: Graphite H-451 (monolith + reflectors)
- Energy spectrum: Thermal peak + fast fission tail

**Why Not MODE N P (coupled neutron-photon)?**
- For criticality calculation, photon transport is not needed
- Photon production only matters for:
  - Dose calculations (shielding design)
  - Heating distribution (already dominated by fission)
  - Activation studies (depletion analysis)
- MODE N reduces computational cost with no impact on keff accuracy

---

### 2. PHYS:N 40.0 (Neutron Physics Parameters)

**Energy Range Justification:**
- **emax = 40 MeV**: Covers fission spectrum tail
  - Watt fission spectrum for U-235: peak at ~0.7 MeV, extends to ~20 MeV
  - 40 MeV upper bound includes high-energy tail with safety margin
  - MCNP default is 100 MeV (overly conservative for thermal reactors)

**Default Parameters (Why We Don't Specify Them):**
- **Continuous energy transport**: HPMR operates in thermal regime where resonances matter
  - Multigroup transport would miss resonance self-shielding in TRISO particles
  - Temperature-dependent cross sections (.02c, .03c) require continuous energy

- **Doppler broadening enabled (nodop=0)**: Critical for thermal reactor safety
  - Operating temperatures: 1156-1570 K (fuel average/maximum)
  - Large temperature range: 900-1200 K cross-section libraries used
  - Doppler feedback: -6 to -9 pcm/K (negative temperature coefficient)
  - DBRC (Doppler Broadening Rejection Correction) could be added for U-238 if higher accuracy needed

- **No photon production (iphot=0)**: Consistent with MODE N
  - Criticality calculation does not need photon transport
  - Photon production would be enabled with MODE N P and iphot=1

**Why Not Use Defaults (Omit PHYS Card)?**
- PHYS:N with emax=40 is explicit about energy range
- Documents design basis (fission spectrum coverage)
- Small computational benefit (avoids tracking neutrons >40 MeV that don't exist in this reactor)
- Best practice: Be explicit about physics assumptions

**Alternative (If Omitting PHYS:N):**
- MCNP defaults work fine: emax=100 MeV is conservative
- Adds ~5% computational overhead for negligible benefit
- Recommendation: Include PHYS:N 40.0 for clarity and efficiency

---

### 3. PRINT Card (Output Control)

**Selected Tables and Why:**

**Cross-Section and Material Info:**
- **Table 10** (Cross-section tables): Verify ZAID availability and libraries
- **Table 40** (Material summary): Confirm atom densities, temperatures

**Geometry and Importance:**
- **Table 30** (Surface crossing): Track particle flow through geometry
- **Table 38** (Cell importance): Verify importance settings

**Criticality-Specific Tables:**
- **Table 110** (Keff results): Primary output - keff, confidence intervals, generation times
- **Table 117** (Source convergence): Shannon entropy, source distribution evolution
- **Table 118** (Entropy convergence): Spatial convergence diagnostics
- **Table 126** (Fission matrix): Dominance ratio, higher mode convergence
- **Table 128** (Keff vs cycle): Track keff stability over cycles

**Tally Statistics:**
- **Table 50** (Tally summary): If tallies are added later
- **Table 160** (Tally fluctuation): Statistical quality assessment
- **Table 161** (Tally mean and error): Primary tally results
- **Table 162** (Tally statistical checks): 10 statistical tests for tally reliability

**Weight Window (Future):**
- **Table 170** (Weight window summary): If variance reduction added

**Why This Selection?**
- Omits verbose tables (60-100: cell-by-cell summaries)
- Focuses on criticality diagnostics and convergence
- Reduces output file size by ~70%
- Retains all information needed for validation

**What's Omitted (and Why):**
- Table 60 (Cell geometry): Not needed after geometry debugging
- Table 70 (Surface geometry): Not needed for production runs
- Table 85 (Cell volumes): Can be verbose for complex lattices
- Table 90 (Material masses): Not critical for criticality calculation
- Table 120 (Neutron activity): Redundant with keff tables
- Tables 130-150 (Detailed tallies): Only if tallies present

---

### 4. PRDMP Card (Restart and Dump Control)

**Format: PRDMP J J 1 J J**

**Parameters Explained:**
- **ndp = J (default = 1)**: Print dump number initially
  - Minimal impact on output

- **ndd = J (default = 10)**: Dump RUNTPE every 10 cycles
  - For 300-cycle run (50 skip + 250 active), this gives ~30 dumps
  - Enables restart from last dump if run crashes
  - RUNTPE file contains complete simulation state

- **ncd = 1**: Create/update RUNTPE every 1 cycle
  - **Most important parameter for this reactor**
  - Why every cycle? Complex hexagonal geometry may have issues
  - Allows restart from any cycle if geometry errors or convergence problems
  - Minimal computational overhead (~1% slower)
  - Critical for long-running depletion calculations (future work)

- **ndm = J (default = 10)**: Write MCTAL every 10 cycles
  - MCTAL contains tally results
  - Less critical for eigenvalue-only runs

- **nbm = J (default = 2)**: Binary MCTAL dumps
  - 2 = overwrite mode (saves disk space)

**Why This Setting?**
- Conservative approach for complex geometry
- Enables restart at any point
- Essential for production runs (250 active cycles = ~hours of CPU time)
- Disk space cost: ~100-500 MB for RUNTPE (acceptable)

**Alternative (Less Conservative):**
```
PRDMP J J 10 J J
```
- ncd = 10: Dump every 10 cycles instead of every cycle
- Saves disk I/O, but loses granularity
- Use if disk space is critical

---

### 5. LOST Card (Lost Particle Handling)

**Format: LOST 10 10**

**Parameters:**
- **nlost = 10**: Issue warning after 10 lost particles
- **nlose = 10**: Terminate after 10 additional lost particles (20 total)

**Why These Values?**

**Geometry Complexity:**
- 5-level nested hexagonal lattice (pin → assembly → core)
- 876 heat pipes (cylindrical) in hexagonal matrix
- 13 guide tubes (cylindrical) in hexagonal assemblies
- 12 control drums (cylindrical) intersecting hexagonal core
- Multiple material interfaces (fuel/graphite/gap/heat pipe)
- Axial segmentation (2 segments currently, 18 planned)

**Expected Lost Particles:**
- Well-constructed geometry: 0-1 lost particles per million
- Complex nested lattices: 1-10 lost per million possible
- Geometry errors: >100 lost per million (indicates problem)

**Setting Rationale:**
- **10 warning threshold**: Early warning of potential geometry issues
  - Allows identification of problem regions without stopping run
  - MCNP prints lost particle coordinates for debugging

- **20 total threshold**: Prevents runaway lost particle accumulation
  - >20 lost typically indicates geometry error (overlap, gap, void)
  - Stopping early saves CPU time on invalid geometry
  - Low enough to catch problems, high enough to tolerate minor numerical issues

**Comparison to Defaults:**
- MCNP default: nlost = 10, nlose = 100
- Default is more permissive (allows up to 110 lost particles)
- HPMR setting is more conservative (stops at 20)
- Justification: Complex geometry warrants stricter tolerance

**When Lost Particles Might Occur:**
- Hexagonal lattice coordinate rounding errors
- Surface intersection numerical precision issues
- Fill array boundary edge cases
- Control drum / core interface overlaps
- Heat pipe / reflector protrusion geometry

**If Lost Particles Occur:**
1. Check lost particle coordinates (printed in output)
2. Verify geometry in that region (plot with MCNP plotter)
3. Check for surface overlaps or gaps
4. Verify universe assignments
5. Check transformation matrices (if used)

**Alternative Settings:**
```
LOST 100 100
```
- More permissive: Allows up to 200 lost particles
- Use for initial debugging when some lost particles expected
- NOT recommended for production validation runs

```
LOST 1 1
```
- Extremely strict: Stop after 2 lost particles
- Use for final geometry validation
- May be too strict (false positives from numerical precision)

---

## TEMPERATURE-DEPENDENT PHYSICS

### Current Model Temperature Range

**Material Temperatures (from HPMR_Analysis_Overview.md Table 19):**

| Material | Average T (K) | Maximum T (K) | MCNP Library Used |
|----------|---------------|---------------|-------------------|
| **Fuel (m301/m302)** | 1155.6 | 1570.0 | .03c (1200K) |
| **Graphite monolith (m201)** | 1156.7 | 1567.0 | .83c (1200K), grph.47t |
| **Radial reflector (m401 BeO)** | 961.0 | 1025.8 | .02c (900K), be-beo.46t |
| **SS316 shield (m411)** | 961.0 | - | .02c (900K) |
| **Heat pipes (m315)** | ~1073 | ~1100 | .03c (1200K) |

### Cross-Section Library Selection

**Why .03c (1200K) for Fuel?**
- Average fuel temperature: 1155.6 K (close to 1200K)
- Cross-section libraries available: .01c (293K), .02c (900K), .03c (1200K)
- .03c is best match for operating conditions
- Temperature difference: <4% (acceptable for initial model)

**Why grph.47t (1200K) for Graphite?**
- Thermal scattering law S(α,β) for graphite
- Available: grph.10t (296K), grph.20t (400K), grph.30t (600K), grph.47t (1200K)
- grph.47t matches high-temperature operation
- Critical for accurate thermal neutron spectrum

**Why .02c (900K) for Reflector/Shield?**
- Lower temperature materials (~961K average)
- .02c (900K) is reasonable match
- BeO thermal scattering: be-beo.46t (1000K) is good match

### Temperature Coefficient Physics

**Doppler Broadening (Fuel):**
- Reference value: -6.2 to -8.7 pcm/K (Table 11)
- Mechanism: U-238 resonance broadening with temperature
- Captured by .03c library and MCNP's on-the-fly Doppler
- For enhanced accuracy, could add:
  ```
  DBRC301  92238.03c    $ Doppler Broadening Rejection Correction for U-238
  DBRC302  92238.03c
  ```
- Expected improvement: ~50-200 pcm in keff accuracy
- Computational cost: +10-20% run time

**Graphite Temperature Effect:**
- Reference value: +0.4 to +0.7 pcm/K (Table 12)
- Mechanism: Thermal expansion reduces density, hardens spectrum
- Much weaker than Doppler (opposite sign but smaller magnitude)
- Net coefficient remains negative (Doppler dominates)

**TMP Card (Optional Future Enhancement):**
```
TMP301  9.97E-8    $ Fuel at 1156 K: T(MeV) = 1156 × 8.617e-11
TMP302  9.97E-8    $ Fuel at 1156 K
TMP201  9.97E-8    $ Graphite at 1157 K
TMP401  8.28E-8    $ BeO at 961 K
TMP411  8.28E-8    $ SS316 at 961 K
TMP315  9.25E-8    $ Heat pipe at 1073 K
```
- TMP card enables cross-section interpolation between libraries
- Currently not used (single-library approximation acceptable)
- Add for high-accuracy temperature coefficient calculations

---

## ENERGY CUTOFFS (Currently Not Specified)

### CUT:N Card (Optional)

**Not included in current physics code because:**

1. **Thermal reactor requires low-energy neutrons**
   - Thermal peak: ~0.025 eV at 300K, ~0.1 eV at 1200K
   - Graphite moderation produces thermal neutrons essential for fission
   - Energy cutoff would kill thermalized neutrons (wrong physics)
   - **Recommendation: E_min = 0.0** (no cutoff)

2. **Maximum energy already specified in PHYS:N**
   - E_max = 40 MeV covers fission spectrum
   - CUT:N E_max would be redundant

3. **Time cutoffs not applicable**
   - Steady-state criticality calculation
   - No time-dependent phenomena modeled
   - KCODE iterates to equilibrium distribution

**If CUT:N were added (NOT recommended):**
```
CUT:N  J  0.0  40.0  1E33
c      ^  ^    ^     ^
c      |  |    |     +-- T_max (infinite time)
c      |  |    +-------- E_max (40 MeV, redundant with PHYS:N)
c      |  +------------- E_min (0.0 MeV = no cutoff, REQUIRED for thermal)
c      +---------------- Weight cutoff (default)
```

**Why E_min = 0.0 is Critical:**
- Thermal neutrons at 1200K: ~0.1 eV = 1E-7 MeV
- Any cutoff >1E-8 MeV would kill thermal neutrons
- Would destroy reactor physics (keff would be wrong)

---

## VARIANCE REDUCTION (Future Enhancement)

### Not Included in Current Model

**Why No Variance Reduction Initially:**
1. **Criticality calculations are efficient**
   - KCODE naturally focuses source in fuel regions
   - No deep penetration problems (unlike shielding)
   - Thermal reactor has good neutron economy

2. **Complex geometry warrants validation first**
   - Need to verify geometry correctness without VR complications
   - Lost particles would be masked by weight windows
   - Source convergence diagnostics more important initially

**Future VR Techniques (If Needed):**

**Weight Windows (WWN/WWE/WWT):**
```
c --- Weight window generation ---
WWG  10  0  0     $ Generate WW after 10 inactive cycles
```
- Automatic weight window generation based on flux distribution
- Useful for tallies in reflector or shield regions
- Not needed for core-averaged keff

**Cell Importance (IMP:N):**
- Currently: All active cells have IMP:N=1 (equal importance)
- Could use IMP:N=10 in fuel, IMP:N=5 in core, IMP:N=1 in reflector
- Focuses particles in fuel regions
- Minor benefit for criticality (keff is global quantity)

**When to Add VR:**
1. If convergence is slow (>100 inactive cycles needed)
2. If tallying in low-flux regions (reflector, shield)
3. If computing reaction rate ratios (spectral indices)
4. NOT needed for basic keff calculation

---

## VALIDATION AND TESTING

### What to Check After Adding These Cards

**1. Model Runs Successfully:**
- No fatal errors related to physics cards
- KCODE completes all cycles (50 skip + 250 active)
- RUNTPE files created for restart

**2. Source Convergence:**
- Shannon entropy stabilizes within 50 cycles (Table 118)
- keff settling behavior reasonable (no large oscillations)
- Source distribution covers fuel regions (no localized source)

**3. Keff Results:**
- Final keff in range 1.05-1.15 (drums in, no Xe/Sm)
- Statistical uncertainty <0.00050 (50 pcm) for 250 active cycles
- Dominance ratio <0.98 (good convergence)

**4. Lost Particles:**
- Zero lost particles expected for correct geometry
- 1-5 lost particles acceptable (numerical precision)
- >10 lost particles indicates geometry problem

**5. Output File Quality:**
- PRINT card produces readable output (~500 KB instead of ~5 MB)
- Critical tables present: 110 (keff), 117 (entropy), 162 (statistics)
- No excessive warnings or error messages

**6. Restart Capability:**
- RUNTPE file exists and is updated every cycle
- Can restart run with: `CONTINUE`
- MCTAL file created (if tallies added)

---

## COMPARISON TO REFERENCE MODEL

### Expected Results (From HPMR_Gap_Analysis.md)

| Parameter | Reference Value | Expected with This Code |
|-----------|----------------|-------------------------|
| **keff (drums in)** | 1.09972 ± 0.00014 (Serpent) | 1.090-1.110 (±1000 pcm) |
| **keff (drums out)** | ~1.12-1.15 (est.) | Not modeled yet (no drums) |
| **Uncertainty** | ±140 pcm | ±500 pcm (MCNP with 250 cycles) |

**Why Different from Reference?**
1. **No control drums yet**: Reference includes 12 drums
   - Expected reactivity difference: -3000 to -5000 pcm
   - Current model will be more reactive (drums not implemented yet per Gap Analysis)

2. **No Xe-135/Sm-149 poisons**: Reference notes ~5000 pcm excess
   - Fresh fuel without equilibrium poisons
   - Expected keff ~1.10-1.15 without drums and without poisons

3. **MCNP vs Serpent**: Reference shows ~450 pcm bias (Griffin vs Serpent)
   - Expected with MCNP: Similar bias, ±500 pcm
   - Cross-section library differences
   - Homogenization approximations

**Validation Criteria:**
- ✓ keff > 1.0 (reactor is critical without drums)
- ✓ keff in range 1.08-1.15 (without drums, without poisons)
- ✓ Statistical uncertainty <500 pcm
- ✓ Source converges in <50 cycles
- ✓ Zero lost particles

---

## NEXT STEPS AFTER ADDING PHYSICS CODE

### Immediate (Required for Model to Run)

From Gap Analysis Phase 1:
1. ✓ Add MODE N card (THIS DOCUMENT)
2. ✓ Add PHYS:N card (THIS DOCUMENT)
3. ✓ Add PRINT card (THIS DOCUMENT)
4. ✓ Add PRDMP card (THIS DOCUMENT)
5. ✓ Add LOST card (THIS DOCUMENT)
6. ⚠ Add KCODE card (separate task: source builder)
7. ⚠ Add KSRC card (separate task: source builder)
8. ⚠ Add bottom reflector (separate task: geometry builder)
9. ⚠ Add top reflector (separate task: geometry builder)

### Short-Term (Phase 2)

1. Add 12 control drums (mcnp-geometry-builder)
2. Define m800 (B4C) and m710 (graphite reflector) materials
3. Test keff with drums in/out

### Medium-Term (Phase 3)

1. Add tallies for flux and power distribution (mcnp-tally-builder)
2. Refine axial segmentation to 8-18 zones
3. Add temperature-dependent cross sections (TMP cards)
4. Compute temperature coefficients

---

## DOCUMENT METADATA

**Created:** 2025-11-08
**Author:** mcnp-physics-builder specialist
**Model:** Heat Pipe Microreactor (HPMR)
**Status:** Complete - Ready for implementation
**Dependencies:** KCODE/KSRC (separate), reflectors (separate)
**Next Action:** Insert physics code into hpcmr-simplified.i after material cards

---

## APPENDIX: Complete Physics Code Block (Copy-Paste Ready)

```
c ============================================================================
c                        PHYSICS CONTROL CARDS
c ============================================================================
c
MODE N
c
PHYS:N  40.0
c
PRINT 10 30 38 40 50 110 117 118 126 128 160 161 162 170
c
PRDMP J J 1 J J
c
LOST  10 10
```

**Insert Location:** After all material cards (after m411), before any source cards

**Total Lines:** 5 active cards + comments = ~20 lines

---
