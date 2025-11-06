# MCNP Statistical Checks Guide

**Purpose:** Detailed explanation of MCNP's 10 statistical quality checks for tally reliability.

**Companion to:** mcnp-warning-analyzer SKILL.md

---

## Overview

MCNP applies 10 statistical tests to each tally to assess result reliability. These checks verify that the tally behaves as expected for a properly converged Monte Carlo calculation. Passing all 10 checks indicates a reliable result; failing multiple checks indicates insufficient statistics or fundamental problems.

**Rule of Thumb:**
- **0 checks failed:** Result reliable ✅
- **1-2 checks failed:** Marginal, investigate ⚠️
- **3+ checks failed:** Result unreliable, extend run or improve VR ❌

---

## The 10 Statistical Checks

### Check 1: Mean Behavior Acceptable

**What It Tests:** Whether the estimated mean is converging properly

**Criterion:** Slope of mean vs. history should be <0.1 in magnitude

**Why It Fails:**
- Simulation hasn't run long enough
- Large rare events dominating late in run
- Fundamental setup error

**Fix:**
```
NPS  5e6                              $ Increase from current value
```

**Interpretation:**
- Failed alone: Need more particles
- Failed with checks 2-4: Convergence issue

---

### Check 2: Relative Error Acceptable

**What It Tests:** Whether the relative error is small enough

**Criterion:** Relative error typically should be <0.10 (10%)

**Standard Goals:**
- Academic/publication: <0.01 (1%)
- Engineering: <0.05 (5%)
- Screening: <0.10 (10%)

**Why It Fails:**
- Insufficient particles
- Tally in low-probability region
- Poor variance reduction

**Fix:**
```
c Option 1: More particles
NPS  1e7

c Option 2: Variance reduction
WWG  4  0  1.0                        $ For F4 tally
```

**Interpretation:**
- Error >50%: Result meaningless
- Error >10%: Unreliable
- Error <5%: Generally acceptable

---

### Check 3: Relative Error Decreasing

**What It Tests:** Whether error is consistently decreasing

**Criterion:** Overall trend should show decreasing relative error

**Why It Fails:**
- Simulation length insufficient to establish trend
- Large fluctuations in later histories
- Rare events occurring sporadically

**Fix:**
```
c Run much longer to establish trend
NPS  1e7                              $ Increase significantly
```

**Interpretation:**
- Failed early in run: Expected, keep running
- Failed late in run: Problem with tally setup or VR

---

### Check 4: Relative Error Decreased in Second Half

**What It Tests:** Whether second half of run shows improvement

**Criterion:** Error in second half < error in first half

**Why It Fails:**
- Rare event occurred in second half
- Variance reduction turned on/off mid-run
- Source convergence issue (KCODE)

**Fix:**
```
c Continue running longer
NPS  [2× current value]

c Check for source convergence (KCODE):
c - Ensure entropy flat before active cycles
c - More inactive cycles if needed
```

**Interpretation:**
- Common failure with checks 3, 7, 9
- Indicates need for longer run

---

### Check 5: Figure of Merit (FOM) Behavior Acceptable

**What It Tests:** Whether calculation efficiency is consistent

**FOM Definition:**
```
FOM = 1 / (R² × T)
where:
  R = relative error
  T = computer time
```

**Criterion:** FOM should be approximately constant (within ±10%)

**Why It Fails:**
- Computer load varying during run
- Variance reduction inconsistent
- Source distribution changing (KCODE)
- Geometry complexity changing (deep penetration)

**Fix:**
```
c If FOM decreasing significantly:
c - Check variance reduction setup
c - Verify importance map reasonable
c - For KCODE: ensure source converged

c If FOM acceptable but check fails:
c - Usually OK if overall FOM stable
c - Small fluctuations normal
```

**Interpretation:**
- FOM stable: Good efficiency
- FOM decreasing: Particles reaching more difficult regions
- FOM increasing: Unrealistic (check for errors)

---

### Check 6: FOM Increasing in Second Half

**What It Tests:** Whether second half shows equal or better efficiency

**Criterion:** FOM in second half ≥ FOM in first half

**Why It Fails:**
- Particles penetrating deeper (harder regions)
- Variance reduction less effective later
- Source evolution (KCODE)

**Fix:**
```
c Improve variance reduction:
WWG  [tally]  0  1.0

c Or accept if FOM reasonably stable
c - FOM changes <20% usually acceptable
```

**Interpretation:**
- Failed alone: Monitor, often acceptable
- Failed with check 5: VR issue

---

### Check 7: Variance of Variance (VOV) Acceptable

**What It Tests:** Whether tally contributions are consistent

**Criterion:** VOV < 0.10

**What VOV Means:**
- VOV = variance of the variance estimate
- Measures how "lumpy" tally contributions are
- High VOV: Few large rare events dominate

**Why It Fails:**
- Large rare events (e.g., deep penetration tallies)
- Insufficient variance reduction
- Geometry issues causing occasional huge tallies

**Fix:**
```
c Critical check - must address:

c Option 1: Better variance reduction
WWG  [tally]  0  1.0
IMP:N  1  2  4  8  16  0              $ Geometric importance

c Option 2: Much longer run
NPS  1e8                              $ Need many histories to average rare events

c Option 3: Check geometry
c - Lost particles creating anomalous tallies?
c - Use VOID test to verify geometry
```

**Interpretation:**
- VOV <0.10: Excellent
- VOV 0.10-0.20: Acceptable if other checks pass
- VOV >0.20: Result dominated by rare events, unreliable

---

### Check 8: VOV Decreasing

**What It Tests:** Whether VOV improves with more histories

**Criterion:** VOV should decrease as simulation progresses

**Why It Fails:**
- Rare events occurring throughout run
- Fundamental problem with tally setup
- Geometry errors

**Fix:**
```
c If VOV not decreasing:
c 1. Check geometry (VOID test)
c 2. Improve variance reduction significantly
c 3. Consider if tally measures reasonable quantity
```

**Interpretation:**
- Failed with check 7: Serious issue
- VOV constant or increasing: Major problem

---

### Check 9: VOV Decreased in Second Half

**What It Tests:** Whether second half shows VOV improvement

**Criterion:** VOV in second half < VOV in first half

**Why It Fails:**
- Rare event in second half
- Variance reduction less effective later
- Simulation still converging

**Fix:**
```
c Run longer
NPS  [2× current value]

c Improve variance reduction
c Focus on reducing rare large events
```

**Interpretation:**
- Similar to check 4 but for VOV
- Often fails together with checks 7-8

---

### Check 10: Fitted Slope Behaves Appropriately

**What It Tests:** Whether error decreases as expected (∝ 1/√N)

**Criterion:** Slope of log(error) vs. log(N) should be near -0.5

**Expected Behavior:**
```
For well-behaved tally:
  Error ∝ 1/√N
  log(Error) ∝ -0.5 × log(N)
  Slope ≈ -0.5
```

**Why It Fails:**
- Statistical behavior not following 1/√N
- Usually fails with other checks
- Rare events disrupting convergence

**Fix:**
```
c Usually resolves when other checks fixed
c Focus on fixing checks 1-9 first
c Check 10 often passes when others pass
```

**Interpretation:**
- Rarely fails alone
- Indicates fundamental statistical issue
- Fix other failed checks first

---

## Tally Fluctuation Chart Example

**Output Section:**
```
tally        4        nps      mean     error    vov   slope    fom
        100000    1.234E-02  0.0850  0.0050  10.0  12345
        200000    1.241E-02  0.0620  0.0042   9.8  12890
        300000    1.238E-02  0.0505  0.0038   9.5  13120
        400000    1.240E-02  0.0440  0.0035   9.2  13100
        500000    1.239E-02  0.0395  0.0032   8.9  13150

 statistical checks
     1 passed  ✓
     2 passed  ✓
     3 passed  ✓
     4 missed  ✗
     5 passed  ✓
     6 passed  ✓
     7 missed  ✗
     8 passed  ✓
     9 missed  ✗
    10 passed  ✓
```

**Analysis:**
- **Mean:** Stable around 1.239E-02 ✓
- **Error:** Decreasing (0.085 → 0.0395) ✓
- **VOV:** <0.10 and decreasing ✓
- **FOM:** Increasing (12345 → 13150) ✓
- **Failed checks:** 4, 7, 9 (3 total) → Marginal

**Action:** Run longer (NPS 5e6) to pass all checks

---

## Common Failure Patterns

### Pattern 1: Checks 1-2 Failed (Mean/Error Issues)
```
Diagnosis: Fundamental convergence problem
Action: Run much longer (5-10× particles)
Priority: HIGH
```

### Pattern 2: Checks 3-4 Failed (Trend Issues)
```
Diagnosis: Convergence not established
Action: Continue simulation, establish trend
Priority: MEDIUM-HIGH
```

### Pattern 3: Checks 5-6 Failed (FOM Issues)
```
Diagnosis: Efficiency changing
Action: Check variance reduction, source convergence
Priority: MEDIUM
```

### Pattern 4: Checks 7-9 Failed (VOV Issues)
```
Diagnosis: Rare large events
Action: Improve VR, check geometry, run much longer
Priority: HIGH (indicates fundamental issue)
```

### Pattern 5: All Checks Failed
```
Diagnosis: Tally setup error or insufficient run
Action: Check tally definition, run much longer, improve VR
Priority: CRITICAL
```

---

## Statistical Check Decision Tree

```
START: Tally fluctuation chart shows X checks failed

X = 0:
  └─> Result reliable, use with confidence ✓

X = 1-2:
  ├─> Check which tests failed
  ├─> If checks 1-2: Run longer
  ├─> If checks 5-6: Check FOM stability
  ├─> If checks 7-9: Improve VR
  └─> Result marginal, use with caution ⚠️

X = 3-5:
  ├─> Result unreliable
  ├─> If checks 7-9 failed: Major VR needed
  ├─> If checks 1-4 failed: Run much longer
  ├─> Action: Fix issues before using results
  └─> Do NOT publish/use until fixed ❌

X ≥ 6:
  ├─> Result completely unreliable
  ├─> Fundamental problem with tally or setup
  ├─> Action: Review tally definition
  ├─> Check geometry for errors
  ├─> Implement aggressive VR
  └─> Run much longer (10-100× particles) ❌
```

---

## Improving Statistical Quality

### Strategy 1: Increase Particle Count

**Most Straightforward:**
```
c To reduce error by factor of 2:
c Need 4× more particles (error ∝ 1/√N)

Current: NPS  1e6   → Error = 0.10
Target:  NPS  4e6   → Error ≈ 0.05
```

**Limitation:** Can be computationally expensive

### Strategy 2: Variance Reduction

**More Efficient:**
```
c Weight windows for specific tally:
WWG  4  0  1.0                        $ Generate WW for F4

c Or importance biasing:
IMP:N  1  2  4  8  16  32  0          $ Geometric progression
```

**Benefit:** Can achieve 10-100× efficiency improvement

### Strategy 3: Tally Optimization

**Adjust Binning:**
```
c Bad (too fine):
E4  0.001  100i  20                   $ 100 bins (each has poor statistics)

c Good (reasonable):
E4  0.001  10i  20                    $ 10 bins (better statistics per bin)
```

### Strategy 4: Hybrid Approach

**Combine Methods:**
```
1. Implement variance reduction (WWG, IMP)
2. Optimize tally binning
3. Run longer with improved setup
4. Achieve target error efficiently
```

---

## References

- **warning_catalog.md:** Warning messages related to statistical issues
- **MCNP Manual Chapter 2:** Monte Carlo Statistics theory
- **MCNP Manual Chapter 5:** Tally Fluctuation Charts
- **mcnp-variance-reducer SKILL:** Techniques to improve tally statistics

---

**END OF STATISTICAL CHECKS GUIDE**
