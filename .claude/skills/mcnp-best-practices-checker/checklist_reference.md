# MCNP Best Practices - Complete 57-Item Checklist

**Purpose:** Comprehensive reference for MCNP Chapter 3.4 best practices checklist with detailed explanations.

**Companion to:** mcnp-best-practices-checker SKILL.md

---

## Overview

These 57 practices ensure correct and efficient MCNP simulations. They exist because users got wrong answers by skipping them. This is not optional advice - these are requirements for reliable results.

**Organization:**
- **Phase 1: Problem Setup** (22 items) - Before first run
- **Phase 2: Preproduction** (20 items) - During short test runs
- **Phase 3: Production** (10 items) - During long production runs
- **Phase 4: Criticality** (5 items) - Additional for KCODE problems

---

## Phase 1: Problem Setup (§3.4.1)

**Purpose:** Prevent basic errors before running expensive calculations

**When:** Before ANY MCNP run

### Geometry Practices (Items 1-7)

#### 1. Draw Geometry Picture

**Practice:** Sketch geometry on paper before coding

**Why:** Visualizing helps identify:
- Dimension errors
- Missing components
- Spatial relationships
- Coordinate system issues

**How:**
- Draw cross-sections (XY, XZ, YZ planes)
- Label dimensions
- Mark material boundaries
- Note symmetries

**Consequence of skipping:** Coding errors harder to debug

---

#### 2. ALWAYS Plot Geometry

**Practice:** Use MCNP plotter before running particles

**Command:**
```bash
mcnp6 ip i=input.inp
```

**Why:** Catches 90% of geometry errors
- Overlaps (dashed lines)
- Gaps (missing cells)
- Wrong dimensions
- Transformation errors

**Minimum:** Plot from 3 orthogonal views
```
PX 1 0 0    $ View along X
PX 0 1 0    $ View along Y
PX 0 0 1    $ View along Z
```

**Consequence of skipping:** Lost particles, BAD TROUBLE, wrong answers

**CRITICAL:** This is the MOST IMPORTANT practice

---

#### 3. Model in Sufficient Detail

**Practice:** Balance accuracy vs. complexity

**Too Simple:**
- Missing critical components
- Over-simplified geometry
- Wrong physics

**Too Complex:**
- Unnecessary detail
- Slow calculations
- Hard to debug

**How to Judge:**
- What's the question? (dose, keff, activation?)
- What precision needed? (screening vs. licensing)
- Sensitivity analysis on detail level

---

#### 4. Use Simple Cells

**Practice:** Avoid overly complex Boolean expressions

**Bad:**
```
5  1  -1.0  (-1:2:#3):(4 -5 (-6:7))  IMP:N=1    $ Too complex!
```

**Good:**
```
5  1  -1.0  -1 2  IMP:N=1                        $ Simple
6  1  -1.0  4 -5 -6  IMP:N=1                     $ Clear
```

**Why:** Simpler = fewer errors, easier debugging

---

#### 5. Use Simplest Surfaces

**Practice:** Prefer macrobodies and simple surfaces

**Preference Order:**
1. RPP, SPH, RCC macrobodies (easiest)
2. PX, PY, PZ planes
3. SO, SX, SY, SZ spheres
4. CX, CY, CZ cylinders
5. General surfaces (last resort)

**Why:** Simpler surfaces = faster tracking, fewer errors

---

#### 6. Avoid Excessive # Operator

**Practice:** Minimize complement operator usage

**Warning Sign:**
```
10  1  -1.0  #1 #2 #3 #4 #5 #6 #7    $ Too many complements!
```

**Better:**
```
10  1  -1.0  -10 (1:2:3:4:5:6:7)     $ Explicit boundary, union of interior
```

**Why:** Excessive complements indicate overly complex design

---

#### 7. Build Incrementally

**Practice:** Add and test geometry piece by piece

**Workflow:**
1. Start simple (single cell)
2. Test with VOID card
3. Add next component
4. Test again
5. Repeat until complete

**Why:** Isolates errors to recent additions

---

### Organization Practices (Items 8-9)

#### 8. Use READ Card

**Practice:** Store common cards in separate files

**Example:**
```
c Main input
READ FILE=materials.txt
READ FILE=common_surfaces.txt
```

**Benefits:**
- Reusable components
- Cleaner main input
- Version control easier

---

#### 9. Pre-calculate Volumes/Masses

**Practice:** Calculate system volume by hand, compare with MCNP

**Workflow:**
1. Calculate expected volume analytically
2. Run MCNP with VOL card
3. Compare results
4. Investigate large discrepancies (>5%)

**Example:**
```
c Expected: Sphere R=10 → V = 4/3 π R³ = 4188.8 cm³
VOL  NO                                $ Calculate volumes
c After run: Check Table 126 for volumes
c If MCNP says 4500 cm³ → geometry error!
```

**Why:** Major discrepancies = geometry errors

---

### Validation Practices (Items 10-13)

#### 10. Use VOID Card

**Practice:** Test geometry with VOID card

**Procedure:**
```
VOID                                   $ Make all cells void
MODE  N
IMP:N  1  1  1  ...  1  0             $ All cells IMP=1 except graveyard
SDEF  SUR=998  NRM=-1                 $ Flood from outside
NPS  1000000                           $ Many particles
```

**Why:** Quickly finds overlaps and gaps
- No collisions → particles stream through
- Lost particle = geometry error
- Very effective, takes minutes

**When:** Before any production run

---

#### 11. Check Source (Tables 10, 110, 170)

**Practice:** Verify source distribution in output

**Tables to Check:**
- **Table 10:** Source overview
- **Table 110:** Source position distribution
- **Table 170:** Source energy distribution

**Verify:**
- Positions where expected?
- Energy distribution correct?
- Particles in right cells?

---

#### 12. Check Source with Mesh Tally

**Practice:** Use TMESH or FMESH to visualize source

**Example:**
```
TMESH
  RMESH1:N  FLUX
    CORA1  -100  99i  100              $ X bins
    CORB1  -100  99i  100              $ Y bins
    CORC1  -100  99i  100              $ Z bins
```

**Why:** Visual verification of source location and intensity

---

#### 13. Understand Physics Approximations

**Practice:** Know what physics MCNP models and what it doesn't

**Key Limitations:**
- Energy cutoffs (particles killed below threshold)
- Physics models (not all interactions included)
- Cross-section availability (some ZAIDs incomplete)
- Thermal treatment (may need S(α,β))

**Action:** Document assumptions and limitations

---

### Cross Sections & Tallies (Items 14-16)

#### 14. Cross-Section Sets Matter!

**Practice:** Verify correct libraries loaded

**Check in Output:**
```
 tables from file /path/to/xsdir
   1001.80c    ENDF/B-VIII.0
   8016.80c    ENDF/B-VIII.0
```

**Common Issues:**
- Mixed library versions (.70c and .80c)
- Wrong temperature libraries
- Missing thermal scattering

**Consequence:** Can change answers by 5-10%

---

#### 15. Separate Tallies for Fluctuation

**Practice:** Don't combine too many things in one tally

**Bad:**
```
F4:N  1 2 3 4 5 6 7 8 9 10            $ All cells in one tally
```

**Better:**
```
F4:N  1                                $ Tally each cell separately
F14:N  2
F24:N  3
```

**Why:** Combined tallies mask poor statistics in individual regions

---

#### 16. Conservative Variance Reduction

**Practice:** Start simple, add complexity gradually

**Progression:**
1. Analog (no VR) → establish baseline
2. Simple importance (IMP cards)
3. Weight windows if needed
4. Advanced techniques only if necessary

**Why:** Complex VR hard to debug, may introduce errors

---

### General Practices (Items 17-22)

#### 17. Don't Use Too Many VR Techniques

**Practice:** KISS principle - Keep It Simple

**Warning Signs:**
- IMP + WWG + DXTRAN + FCL + ...
- Diminishing returns
- Hard to debug

**Recommendation:** 1-2 VR techniques maximum

---

#### 18. Balance User vs Computer Time

**Practice:** Don't over-optimize simple problems

**Example:**
- Problem runs in 10 minutes analog
- Spend 2 hours optimizing to 5 minutes?
- Not worth it!

**When to Optimize:**
- Production runs >1 hour
- Repeated calculations
- Large parameter studies

---

#### 19. Study ALL Warnings

**Practice:** Read and understand every warning message

**Don't Ignore:**
- "minor" normalization warnings
- Statistical check failures
- IEEE exceptions (if many)

**Use:** mcnp-warning-analyzer skill

---

#### 20. Generate Best Output (PRINT Card)

**Practice:** Request comprehensive output

**Recommendation:**
```
PRINT  10  40  50  110  117  118  126  128  140  160  170
```

**Why:** More information = better debugging

**Balance:** Disk space vs. information

---

#### 21. Recheck INP File

**Practice:** Final review before running

**Checklist:**
- Materials correct? (densities, fractions)
- Source reasonable? (position, energy)
- Tallies in right locations?
- Importance sensible?
- NPS appropriate?

**When:** Before production run

---

#### 22. Garbage In = Garbage Out

**Practice:** MCNP WILL RUN bad inputs

**Remember:**
- MCNP doesn't check physics reasonableness
- No error ≠ correct answer
- You are responsible for validation

**Example:**
- MCNP will track 10 MeV thermal neutrons
- Wrong, but no error message
- YOU must catch these!

---

## Phase 2: Preproduction (§3.4.2)

**Purpose:** Validate setup during short test runs

**When:** After setup, before production (10k-100k particles)

### Understanding Practices (Items 1-3)

#### 1. Don't Use as Black Box

**Practice:** Understand Monte Carlo theory

**Must Know:**
- Central limit theorem
- Variance reduction principles
- Statistical error interpretation
- Sampling methods

**Resources:**
- MCNP Manual Chapter 2
- Monte Carlo textbooks

---

#### 2. Run Short Calculations

**Practice:** Test with 10k-100k particles before production

**Why:**
- Fast feedback (minutes vs. hours)
- Find errors early
- Test VR effectiveness
- Estimate time for production

**Typical:** 100k particles for testing

---

#### 3. Examine Outputs Carefully

**Practice:** Read entire output file

**Check:**
- All warnings
- All tables
- Statistical summaries
- Diagnostic messages

**Time:** 10-15 minutes per output review

---

### Statistics Practices (Items 4-7)

#### 4. Study Summary Tables

**Practice:** Review activity, collision, track summaries

**Key Tables:**
- Table 126: Cell activity
- Table 130: Surface crossings
- Table 140: Nuclide activity

**Look For:**
- Unexpected values
- Zero activity in important regions
- Excessive activity in unimportant regions

---

#### 5. Study Statistical Checks

**Practice:** ALL 10 statistical tests must pass

**Rule:**
- 0 failed: Excellent ✓
- 1-2 failed: Marginal, investigate
- 3+ failed: Unreliable, must fix

**Action:** Use mcnp-statistics-checker skill

---

#### 6. Study FOM and VOV Trends

**Practice:** Figure of Merit and Variance of Variance should be stable

**FOM:** Should be constant (±10%)
**VOV:** Should be <0.10 and decreasing

**If not:** Variance reduction issue or rare events

---

#### 7. Consider Collisions/Particle

**Practice:** Check average collisions per source particle

**Typical Ranges:**
- Shielding: 100-1,000
- Reactor core: 1,000-10,000
- Deep penetration: 10-100

**If Very Low (<10):** Particles not interacting enough
**If Very High (>100,000):** May need better VR or geometry simplification

---

### Efficiency Practices (Items 8-12)

#### 8. Examine Track Populations

**Practice:** Check Table 126 for particles by cell

**Question:** Are particles getting where needed?

**Look For:**
- High population in unimportant regions
- Low population in important regions (tally locations)

**Fix:** Adjust importance or add VR

---

#### 9. Scan Mean-Free-Path Column

**Practice:** Identify problem regions in output tables

**Large MFP:** Void or low-density (fast streaming)
**Small MFP:** High-density (many collisions)

**Use:** Identify where VR needed

---

#### 10. Check Detector Diagnostics

**Practice:** Review F5 and DXTRAN effectiveness

**Output Shows:**
- Detector contributions
- Effectiveness of point detector methods
- Whether DXTRAN working

**If Ineffective:** Adjust or remove

---

#### 11. Understand Large Contributions

**Practice:** No single particle should dominate tally

**Warning Sign:**
- One particle contributes >10% of total
- Indicates rare large event

**Fix:** Better VR or much longer run

---

#### 12. Reduce Unimportant Tracks

**Practice:** Kill particles in unimportant regions

**Methods:**
- IMP:N=0 (kill immediately)
- Low importance (roulette)
- Energy cutoffs

**Balance:** Don't kill particles that might contribute later

---

### Physics Practices (Items 13-14)

#### 13. Check Secondary Production

**Practice:** Verify expected particles generated

**Tables:**
- Photon production from neutrons
- Electron production from photons
- Neutron production from fission

**Expected?** Cross-check with physics intuition

---

#### 14. Back-of-Envelope Check

**Practice:** Rough physics estimate before run

**Examples:**
- Keff should be ~1.0 for critical system
- Dose decreases exponentially through shield
- Flux higher in fuel than reflector

**If MCNP result wildly different:** Something wrong

---

## Phase 3: Production (§3.4.3)

**Purpose:** Ensure quality during long runs

**When:** During production (millions of particles)

### File Practices (Items 1-2)

#### 1. Save RUNTPE

**Practice:** Keep RUNTPE file for analysis

**Uses:**
- Restart calculations
- PTRAC analysis
- MCTAL extraction
- Mesh tally visualization

**Storage:** Archive important RUNTPE files

---

#### 2. Limit RUNTPE Size (PRDMP)

**Practice:** Control dump frequency

**Card:**
```
PRDMP  J  J  1                         $ Dump every cycle
PRDMP  J  J  10                        $ Dump every 10 cycles (smaller file)
```

**Balance:** Restart granularity vs. disk space

---

### Statistics Practices (Items 3-8)

#### 3. Check FOM Stability

**Practice:** FOM should remain roughly constant

**If Decreasing:**
- Particles reaching harder regions
- VR becoming less effective
- May be OK if gradual

**If Increasing:**
- Suspicious (check for errors)

---

#### 4. Answers Seem Reasonable

**Practice:** Physics intuition check

**Questions:**
- Does magnitude make sense?
- Does trend make sense?
- Comparable to similar problems?

---

#### 5. Examine 10 Statistical Checks

**Practice:** ALL tallies must pass all 10 checks

**Non-Negotiable:** Production results must be statistically valid

---

#### 6. Form Valid Confidence Intervals

**Practice:** Understand error bars

**68% CI:** Result ± 1σ
**95% CI:** Result ± 2σ
**99% CI:** Result ± 3σ

**Remember:** These assume normal distribution and statistical convergence

---

#### 7. Continue-Run if Necessary

**Practice:** Extend run until converged

**Command:**
```bash
mcnp6 c runtpe=runtpe outp=outp_continued
```

**When:** Statistical checks not passing after initial run

---

#### 8. Verify Errors Decrease 1/√N

**Practice:** Theory check

**Expected:** Doubling particles → error decreases by √2

**If Not:** Statistical anomaly or setup error

---

### Final Practices (Items 9-10)

#### 9. Accuracy Has Multiple Factors

**Practice:** Statistics ≠ accuracy

**Other Factors:**
- Geometry approximations
- Material approximations
- Physics models
- Cross-section data quality
- Source approximations

**Total Error:** √(statistical² + systematic²)

---

#### 10. Adequately Sample All Cells

**Practice:** Check all cells have sufficient tracks

**Minimum:** ~100 tracks per cell for basic reliability

**Action:** Review Table 126 populations

---

## Phase 4: Criticality (§3.4.4)

**Purpose:** Additional requirements for KCODE problems

**When:** Criticality (eigenvalue) calculations

### Criticality Practices (Items 1-5)

#### 1. Determine Inactive Cycles

**Practice:** Plot keff and Shannon entropy

**Converged When:**
- Entropy flat (±5%) for final 30% of inactive
- Keff stable (no trend)

**Typical:** 50-200 inactive cycles depending on complexity

---

#### 2. Large Histories/Cycle

**Practice:** Minimum 10,000 particles per cycle for production

**Recommendations:**
- Testing: 1,000-5,000 per cycle
- Production: 10,000-100,000 per cycle

**Why:** Better statistics within each cycle

---

#### 3. Examine Keff Behavior

**Practice:** Keff should be stable after inactive cycles

**Warning Signs:**
- Trend continuing in active cycles
- Large cycle-to-cycle fluctuations (>0.001)

**Action:** More inactive cycles

---

#### 4. At Least 100 Active Cycles

**Practice:** Minimum active cycles for confidence intervals

**Typical:** 100-300 active cycles

**Balance:** Cycles vs. histories per cycle

---

#### 5. Recheck Convergence After Run

**Practice:** Verify inactive cycles were sufficient

**Check:**
- Entropy plot retrospectively
- Keff trend in active cycles
- Source distribution settled

**If Not Converged:** Discard run, increase inactive cycles

---

## Quick Reference: Critical Practices

**Never Skip These:**
1. Plot geometry (Item 1.2) - 90% of errors
2. VOID card test (Item 1.10) - Finds overlaps/gaps
3. Study all warnings (Item 1.19) - May indicate serious issues
4. All 10 statistical checks pass (Items 2.5, 3.5) - Result validity
5. Shannon entropy converged (Item 4.1) - Keff reliability

---

## References

- **MCNP Manual Chapter 3.4:** Complete best practices discussion
- **phase_workflows.md:** Systematic review procedures
- **MCNP Manual Chapter 2:** Statistical theory background

---

**END OF CHECKLIST REFERENCE**
