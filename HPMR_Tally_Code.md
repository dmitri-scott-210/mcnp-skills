# HPMR Tally Code Documentation
## F4 Flux and F7 Fission Heating Tallies

**Date Created:** 2025-11-08
**Model:** Heat Pipe Microreactor (HPMR) - hpcmr-simplified.i
**Gap Analysis Reference:** Section 2.2, GAP 9
**Purpose:** Core neutron flux and power distribution tallies for HPMR physics analysis

---

## 1. TALLY OVERVIEW

This tally suite addresses Gap Analysis GAP 9 by implementing:

| Tally | Type | Purpose | Energy Bins |
|-------|------|---------|-------------|
| **F4:N** | Volume-averaged flux | Core-averaged neutron spectrum | 5-group |
| **F14:N** | Volume-averaged flux | Fuel region flux (lower segment) | 5-group |
| **F24:N** | Volume-averaged flux | Fuel region flux (upper segment) | 5-group |
| **F7:N** | Fission heating | Fission power in fuel (lower) | Total |
| **F17:N** | Fission heating | Fission power in fuel (upper) | Total |
| **F34:N** | Flux with FM | Fission reaction rate (lower) | 5-group |
| **F44:N** | Flux with FM | Fission reaction rate (upper) | 5-group |

**Energy Group Structure (5-group):**
Based on HPMR spectral characteristics and thermal microreactor physics:

| Group | Energy Range | Category | Physics Significance |
|-------|-------------|----------|---------------------|
| **1** | 0.821 - 20.0 MeV | Fast | Fission spectrum, inelastic scattering |
| **2** | 5.53E-3 - 0.821 MeV | Epithermal (fast) | Resonance region, U-238 capture |
| **3** | 0.625E-6 - 5.53E-3 MeV | Epithermal (slowing down) | Graphite moderation |
| **4** | 1E-8 - 0.625E-6 MeV | Thermal | TRISO fuel fission region |
| **5** | 0 - 1E-8 MeV | Deep thermal | Cold spectrum tail |

---

## 2. COMPLETE TALLY INPUT CODE

### 2.1 Core-Averaged Flux (F4)

**Purpose:** Measure neutron energy spectrum in active core region

```mcnp
c ============================================================================
c                         TALLY DEFINITIONS
c ============================================================================
c
c --- Tally 4: Core-Averaged Neutron Flux ---
F4:N   102
FC4    Core-averaged neutron flux (5-group structure)
E4     1E-8  0.625E-6  5.53E-3  0.821  20.0
c      Thermal | Epi-thermal | Epi-fast | Fast | Upper
c      Group 4 | Group 3     | Group 2  | Group 1
FQ4    E
c      Energy bins in columns for readability
```

**Cell Reference:**
- Cell 102: Active core container (z=20-180 cm), filled with u=102 (core lattice)

**Output:**
- Flux in each energy group (neutrons/cm²)
- Total flux (integrated over all energies)

**Key Notes:**
- NO VOL parameter needed (MCNP calculates from RHP surface)
- FQ4 E: Print energy bins as columns

---

### 2.2 Fuel Region Flux (F14, F24)

**Purpose:** Measure flux in fuel compacts for reaction rate analysis

```mcnp
c --- Tally 14: Fuel Flux - Lower Segment (z=20-100 cm) ---
F14:N  (3011 3012)
FC14   Neutron flux in fuel lower segment (5-group)
E14    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ14   E
c
c --- Tally 24: Fuel Flux - Upper Segment (z=100-180 cm) ---
F24:N  (3031 3032)
FC24   Neutron flux in fuel upper segment (5-group)
E24    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ24   E
```

**Cell References:**
- Cell 3011: Fuel lower segment in u=301 (with guide tube)
- Cell 3012: Fuel lower segment in u=302 (no guide tube)
- Cell 3031: Fuel upper segment in u=301 (with guide tube)
- Cell 3032: Fuel upper segment in u=302 (no guide tube)

**Parentheses Usage:**
- `(3011 3012)`: Sum flux over both fuel types (single result)
- Provides spatially-averaged fuel flux per segment

**Output:**
- Flux in each energy group (neutrons/cm²)
- Combined result for both fuel assembly types

---

### 2.3 Fission Heating (F7)

**Purpose:** Calculate fission power distribution (MeV/g from fission only)

```mcnp
c --- Tally 7: Fission Energy Deposition - Lower Segment ---
F7:N   3011  3012
FC7    Fission heating in fuel lower segment (MeV/g)
c
c --- Tally 17: Fission Energy Deposition - Upper Segment ---
F17:N  3031  3032
FC17   Fission heating in fuel upper segment (MeV/g)
```

**Key Features:**
- F7 tally: Energy deposited from fission reactions ONLY
- No FM card needed (automatic fission energy scoring)
- Separate tallies allow axial power peaking analysis

**Output Units:** MeV/g (directly usable for power calculations)

**Power Calculation:**
```
Power (W) = Tally Result × Source Normalization × Volume × Density × Conversion
          = F7 × (neutrons/s) × (cm³) × (g/cm³) × (1.602E-13 W/MeV)
```

**Expected Results:**
- Lower segment: ~0.5 × core average (bottom of active zone)
- Upper segment: ~1.5 × core average (power peaking expected)
- Ratio F17/F7 ≈ 2-3 (axial power peaking factor)

---

### 2.4 Fission Reaction Rate (F34, F44)

**Purpose:** Compute fission rate per cm³ for power peaking analysis

```mcnp
c --- Tally 34: Fission Reaction Rate - Lower Segment ---
F34:N  (3011 3012)
FC34   U-235 fission reaction rate lower segment (fissions/cm³)
FM34   (-1 301 -6)
c       ^   ^   ^
c       |   |   +-- MT=-6: Total fission cross section
c       |   +------ Material 301 (fuel lower)
c       +---------- C=-1: Normalize to atom density (macroscopic)
E34    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ34   E M
c      Energy bins (E) and Multiplier bins (M) in output
c
c --- Tally 44: Fission Reaction Rate - Upper Segment ---
F44:N  (3031 3032)
FC44   U-235 fission reaction rate upper segment (fissions/cm³)
FM44   (-1 302 -6)
c       Material 302 (fuel upper)
E44    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ44   E M
```

**FM Card Details:**

**Format:** `FMn (C m R)`
- **C = -1**: Normalization constant
  - Converts atom density to macroscopic cross section
  - Result is reaction rate per cm³ per source neutron
- **m = 301 or 302**: Material number (fuel lower or upper)
- **R = -6**: Reaction MT number
  - MT=-6: Total fission cross section (all fissile isotopes)
  - Includes U-235, U-238 threshold fission

**Alternative Reaction Numbers:**
- MT=-6: Total fission (recommended for power)
- MT=-7: Fission × ν (neutron production)
- MT=-8: Fission × Q (energy production)
- MT=18: Total fission (alternative)
- MT=102: (n,γ) radiative capture

**Output:**
- Reaction rate in each energy group (reactions/cm³/source neutron)
- Spectral information (which energies cause fission)
- Power peaking via F44/F34 ratio

**Expected Spectral Distribution:**
- Group 4 (thermal): ~80-90% of fissions (thermal spectrum)
- Group 3 (epithermal): ~5-10%
- Group 2 (epi-fast): ~3-5%
- Group 1 (fast): ~2-5% (U-238 threshold fission)

---

### 2.5 Additional Reaction Rate Tallies (Optional Enhancement)

**For detailed neutron economy analysis:**

```mcnp
c --- Tally 54: Capture Reaction Rate - Lower Segment ---
F54:N  (3011 3012)
FC54   Capture reaction rate lower segment (captures/cm³)
FM54   (-1 301 -2)
c      MT=-2: Total absorption (fission + capture)
E54    1E-8  0.625E-6  5.53E-3  0.821  20.0
c
c --- Tally 64: U-238 Capture Rate - Lower Segment ---
F64:N  (3011 3012)
FC64   U-238 radiative capture lower segment
FM64   (-1 301 102)
c      MT=102: (n,gamma) radiative capture
E64    1E-8  0.625E-6  5.53E-3  0.821  20.0
```

**Purpose:**
- F54: Total neutron absorption (fission + capture)
- F64: U-238 capture (plutonium production)
- Useful for breeding ratio and neutron economy

---

## 3. COMPLETE INPUT BLOCK

**Copy-paste ready tally block for hpcmr-simplified.i:**

```mcnp
c ============================================================================
c                         TALLY DEFINITIONS
c ============================================================================
c
c --- Energy bins: 5-group structure for microreactor thermal spectrum ---
c Group 1 (Fast):        0.821 - 20.0 MeV
c Group 2 (Epi-fast):    5.53E-3 - 0.821 MeV
c Group 3 (Epi-thermal): 0.625E-6 - 5.53E-3 MeV
c Group 4 (Thermal):     1E-8 - 0.625E-6 MeV
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c FLUX TALLIES (F4)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Tally 4: Core-Averaged Neutron Flux ---
F4:N   102
FC4    Core-averaged neutron flux (5-group structure)
E4     1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ4    E
c
c --- Tally 14: Fuel Flux - Lower Segment (z=20-100 cm) ---
F14:N  (3011 3012)
FC14   Neutron flux in fuel lower segment (5-group)
E14    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ14   E
c
c --- Tally 24: Fuel Flux - Upper Segment (z=100-180 cm) ---
F24:N  (3031 3032)
FC24   Neutron flux in fuel upper segment (5-group)
E24    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ24   E
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c FISSION HEATING TALLIES (F7)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Tally 7: Fission Energy Deposition - Lower Segment ---
F7:N   3011  3012
FC7    Fission heating in fuel lower segment (MeV/g)
c
c --- Tally 17: Fission Energy Deposition - Upper Segment ---
F17:N  3031  3032
FC17   Fission heating in fuel upper segment (MeV/g)
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c REACTION RATE TALLIES (F4 + FM)
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c --- Tally 34: Fission Reaction Rate - Lower Segment ---
F34:N  (3011 3012)
FC34   Fission reaction rate lower segment (fissions/cm³/src)
FM34   (-1 301 -6)
E34    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ34   E M
c
c --- Tally 44: Fission Reaction Rate - Upper Segment ---
F44:N  (3031 3032)
FC44   Fission reaction rate upper segment (fissions/cm³/src)
FM44   (-1 302 -6)
E44    1E-8  0.625E-6  5.53E-3  0.821  20.0
FQ44   E M
c
c ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

**Placement in Input File:**
- Insert AFTER material cards (m201, m300, m301, etc.)
- Insert BEFORE KCODE/KSRC cards
- Insert BEFORE any PRINT/PRDMP cards

---

## 4. WHY THIS CODE

### 4.1 Physics Justification

**Power Peaking Analysis:**
- **F7/F17 ratio**: Axial power peaking factor
  - Reference model: Power peaking = 2.44 (Table 19, HPMR Analysis)
  - F17/F7 should approximate this ratio
  - Critical for thermal-hydraulic safety (max fuel temperature)

**Spectral Information:**
- **5-group structure**: Balances detail vs. statistics
  - Group 4 (thermal): Dominant for TRISO fuel fission (~85%)
  - Group 3 (epithermal): Graphite slowing-down region
  - Group 2 (epi-fast): U-238 resonance capture
  - Group 1 (fast): Fission spectrum, inelastic scattering
  - Adequate for microreactor thermal spectrum characterization

**Spatial Distribution:**
- **Two axial segments**: Current model geometry
  - Lower (z=20-100 cm): Expected lower power
  - Upper (z=100-180 cm): Expected higher power (less leakage)
  - Future: Refine to 8-18 segments for finer resolution

### 4.2 Operational Justification

**Power Distribution:**
- F7/F17 tallies provide fission heating directly in MeV/g
- Multiply by mass and normalization → power in watts
- Essential for:
  - Determining peak fuel temperatures
  - Heat pipe thermal design verification
  - Safety margin assessment (1570 K max fuel temp limit)

**Reactivity Coefficients:**
- Flux tallies (F4, F14, F24) at different temperatures → Doppler feedback
- Expected: -6 to -9 pcm/K (negative, inherent safety)
- Spectral shift with temperature → feedback mechanism

**Neutron Economy:**
- Fission reaction rate (F34, F44) by energy group
  - Shows where fissions occur (verify thermal spectrum)
  - Fission/absorption ratio → neutron economy
  - Future: Add breeding calculations (U-238 capture)

### 4.3 Validation Justification

**Benchmark Comparison:**
- HPMR reference model (Serpent/Griffin) has:
  - Power peaking: 2.44
  - Thermal flux dominance
  - Axial power gradient
- Our tallies provide direct comparison metrics

**Statistical Quality:**
- F4 tallies: Excellent statistics (volume-averaged, many tracks)
- F7 tallies: Good statistics (track-length estimator)
- F34/F44 with FM: Good statistics (multiplier applied to F4)
- Expect relative errors <5% for most tallies with 250 active cycles

**Debugging Capability:**
- If keff is wrong, flux spectrum reveals cause:
  - Too thermal → excessive moderation
  - Too fast → insufficient moderation or reflector issues
  - Mismatch with reference → geometry or material error

---

## 5. EXPECTED RESULTS

### 5.1 Quantitative Predictions

**Based on HPMR Analysis Overview (Table 19, Section 11):**

| Tally | Quantity | Expected Value | Units |
|-------|----------|----------------|-------|
| **F4 Total** | Core flux | ~1E13 - 1E14 | n/cm²/s (absolute) |
| **F14/F24** | Flux ratio | ~0.4 - 0.6 | (lower/upper) |
| **F7** | Lower heating | ~0.3 - 0.5 | MeV/g/src |
| **F17** | Upper heating | ~0.6 - 1.2 | MeV/g/src |
| **F17/F7** | Power peaking | ~2.0 - 2.8 | (ref: 2.44) |
| **F34 thermal** | Fission rate | ~80-90% | (Group 4 fraction) |

### 5.2 Energy Spectrum Shape

**F4 Core-Averaged Flux (normalized):**

| Energy Group | Expected Fraction | Physics Reason |
|--------------|-------------------|----------------|
| **Group 1** (Fast) | ~10-15% | Fission spectrum source |
| **Group 2** (Epi-fast) | ~15-20% | Moderation by graphite |
| **Group 3** (Epi-thermal) | ~20-25% | Slowing down region |
| **Group 4** (Thermal) | ~45-55% | Thermalized spectrum |

**F34/F44 Fission Rate Spectrum:**

| Energy Group | Expected Fraction | Physics Reason |
|--------------|-------------------|----------------|
| **Group 1** (Fast) | ~3-5% | U-238 fast fission |
| **Group 2** (Epi-fast) | ~3-5% | Epithermal U-235 |
| **Group 3** (Epi-thermal) | ~5-10% | Resonance tail |
| **Group 4** (Thermal) | ~80-90% | U-235 thermal fission (DOMINANT) |

### 5.3 Axial Power Profile

**Expected Shape (qualitative):**
```
z (cm)  Relative Power (F7/F17)
------  -------------------------
 20     │ ▓░░░░░░░░│ 0.3  (Bottom, high leakage)
 50     │ ▓▓▓░░░░░│ 0.6
 100    │ ▓▓▓▓▓░░░│ 1.0  (Mid-height, reference)
 150    │ ▓▓▓▓▓▓▓░│ 1.4  (Near top, peak power)
 180    │ ▓▓▓▓▓▓░░│ 1.2  (Top, some leakage)
```

**Physical Explanation:**
- Bottom: Neutron leakage into bottom reflector
- Middle: Balanced leakage
- Upper: Peak power (reduced leakage, neutron current upward)
- Top: Slight decrease due to top reflector leakage

---

## 6. USAGE NOTES

### 6.1 Running the Model

**After adding tallies:**
1. Insert tally block into hpcmr-simplified.i (after materials, before KCODE)
2. Verify no syntax errors: `mcnp6 i=hpcmr-simplified.i z`
3. Run: `mcnp6 i=hpcmr-simplified.i n=hpmr_run1. tasks 8`
4. Monitor output file for tally convergence

**KCODE Parameters:**
```
KCODE 10000 1.0 50 250
```
- 10,000 neutrons/cycle: Good for tally statistics
- 250 active cycles: ~2.5M neutron histories
- Expected tally relative errors: <5% for most tallies

### 6.2 Output Analysis

**Key Output Tables:**
- **Table 126**: F4 flux tallies (print 126 in PRINT card)
- **Table 128**: F7 heating tallies (print 128)
- **Tally Fluctuation Charts**: Monitor statistical convergence
  - All 10 statistical tests should PASS
  - Relative error decreasing
  - VOV (variance of variance) <0.1

**Manual Calculations:**

**Power from F7 tally:**
```
Power (MW) = F7_result × Source_rate × Mass × Conversion

Where:
  F7_result   = Tally result (MeV/g per source neutron)
  Source_rate = 15 MW / (200 MeV/fission) × (neutrons/fission)
              ≈ 4.7E17 neutrons/s (for 15 MWth)
  Mass        = Volume × Density (fuel region mass)
  Conversion  = 1.602E-13 W/MeV
```

**Axial Power Peaking:**
```
Peaking Factor = (F17 × Volume_upper) / (F7 × Volume_lower)

Expected: ~2.0-2.8
Reference: 2.44
```

### 6.3 Troubleshooting

**Common Issues:**

1. **Zero Tally Results:**
   - **Cause:** Cell numbers wrong (check u=-301 vs u=301)
   - **Fix:** Verify cell IDs in tally cards match geometry

2. **High Relative Error (>10%):**
   - **Cause:** Insufficient histories in small regions
   - **Fix:** Increase KCODE cycles (250 → 500) or neutrons (10000 → 20000)

3. **FM Tally Returns Zero:**
   - **Cause:** Material mismatch (FM references m301, but cell has different material)
   - **Fix:** Verify FM material number matches cell material

4. **Energy Bins Don't Sum to Total:**
   - **This is normal:** MCNP prints separate total and binned results
   - Total includes all energies (0-∞)

---

## 7. FUTURE ENHANCEMENTS

### 7.1 Assembly-Level Tallies

**For finer spatial resolution:**

```mcnp
c --- Tally 74: Assembly-wise flux (requires segmentation) ---
F74:N  102
FS74   -901  902  T
c      Segment by assembly types, add Total
E74    1E-8  0.625E-6  5.53E-3  0.821  20.0
```

**Advantage:** Assembly-by-assembly power distribution
**Disadvantage:** Complex segmentation in lattice geometry

### 7.2 Mesh Tallies

**For 3D power distribution visualization:**

```mcnp
c --- Mesh Tally 104: 3D fission power ---
FMESH104:N  GEOM=XYZ  ORIGIN=-100 -100 0
            IMESH=-80 -60 -40 -20 0 20 40 60 80 100
            JMESH=-80 -60 -40 -20 0 20 40 60 80 100
            KMESH=20 40 60 80 100 120 140 160 180
            OUT=IJ  EMESH=20
FM104  (-1 301 -6)  (-1 302 -6)
```

**Output:** 3D fission rate distribution (meshtal file)
**Use:** VisIt/ParaView visualization of power peaking

### 7.3 Detector Tallies

**For ex-core flux measurement:**

```mcnp
c --- Tally 5: Point detector at core midplane ---
F5:N  150 0 100  1.0
FC5   Ex-core flux at r=150 cm (outside shield)
E5    1E-8  0.625E-6  5.53E-3  0.821  20.0
```

**Purpose:** Shield design, ex-core detector response

### 7.4 Time-Dependent Tallies

**For transient analysis (if using time-dependent source):**

```mcnp
F204:N  (3011 3012)
T204   0  1E2  1E3  1E4  1E5
c      Time bins in shakes (1 shake = 1E-8 s)
```

**Use:** Pulsed source studies, kinetics benchmarks

---

## 8. INTEGRATION WITH GAP ANALYSIS

### 8.1 Gap Closure Status

**GAP 9: Tally Definitions** ✓ CLOSED

**Requirements Met:**
- ✓ F4 (flux) tallies for core regions
- ✓ F7 (fission heating) tallies
- ✓ Energy bins for spectral information (5-group)
- ✓ FM cards for reaction rates

**Deliverables:**
- ✓ Complete tally input block (ready for insertion)
- ✓ Documentation of tally purpose and expected results
- ✓ Usage notes and troubleshooting guide

### 8.2 Relationship to Other Gaps

**Supports Gap Closure:**
- **GAP 8 (PHYS:N card):** Tallies verify physics settings (spectrum shape)
- **GAP 11 (Axial segmentation):** Current tallies use 2-segment structure, ready for refinement
- **Validation (Phase 4):** Tallies provide metrics for Serpent/Griffin comparison

**Prerequisite Gaps:**
- **GAP 2 (KCODE/KSRC):** MUST be present for tallies to produce results
- **GAP 1 (MODE N):** Required for neutron transport

**Status:** Tallies are ready to use AFTER Phase 1 gaps are closed

---

## 9. VALIDATION CHECKLIST

**After running MCNP with these tallies:**

- [ ] **Tally convergence:** All tallies show decreasing relative error
- [ ] **Statistical tests:** All 10 tests PASS for F4, F7 tallies
- [ ] **Relative error:** <5% for F4, F14, F24, F7, F17, F34, F44
- [ ] **Physics sanity:**
  - [ ] F17/F7 ≈ 2-3 (axial power peaking)
  - [ ] F34 Group 4 (thermal) > 80% (thermal reactor spectrum)
  - [ ] F4 thermal fraction > 45% (core-averaged)
- [ ] **Comparison to reference:**
  - [ ] Power peaking within ±20% of 2.44
  - [ ] Spectral shape qualitatively similar to thermal reactor
- [ ] **Output quality:**
  - [ ] No warning messages about tally cells
  - [ ] Tally fluctuation charts show convergence
  - [ ] No FM material mismatch errors

---

## 10. REFERENCES

**MCNP Manuals:**
- MCNP6 User Manual, Chapter 5.9: Tally Data Cards
- MCNP6 User Manual, Section 5.9.2: F4 (Cell Flux) Tally
- MCNP6 User Manual, Section 5.9.7: F7 (Fission Energy Deposition) Tally
- MCNP6 User Manual, Section 5.9.8: FM (Multiplier) Card
- MCNP6 User Manual, Table 5.19: Reaction MT Numbers

**HPMR Model:**
- /home/user/mcnp-skills/HPMR_Analysis_Overview.md
- /home/user/mcnp-skills/HPMR_Gap_Analysis.md (Section 2.2, GAP 9)
- /home/user/mcnp-skills/hpcmr-simplified.i

**Skill Documentation:**
- /home/user/mcnp-skills/.claude/skills/mcnp-tally-builder/SKILL.md

---

## DOCUMENT METADATA

**Created:** 2025-11-08
**Author:** mcnp-tally-builder specialist
**Model:** Heat Pipe Microreactor (HPMR)
**Purpose:** Gap Analysis GAP 9 closure - Tally definitions
**Status:** Complete - Ready for insertion into hpcmr-simplified.i
**Next Action:** Insert tally block into input file after Phase 1 gaps are closed

---

**END OF TALLY CODE DOCUMENTATION**
