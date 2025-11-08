---
category: D
name: mcnp-criticality-analyzer
description: Analyze KCODE output (keff, entropy, source convergence) and interpret confidence intervals for criticality calculations
activation_keywords:
  - keff
  - criticality
  - KCODE
  - eigenvalue
  - source convergence
  - entropy
  - criticality analysis
  - k-effective
  - Shannon entropy
  - fission source
---

# MCNP Criticality Analyzer Skill

## Purpose

This skill guides users in analyzing MCNP criticality (KCODE) calculation results, interpreting k-effective (keff) values, assessing source convergence through Shannon entropy, and validating that criticality calculations have converged to statistically reliable results. It synthesizes knowledge of source definitions, statistical analysis, and reactor physics to provide comprehensive eigenvalue problem analysis.

## When to Use This Skill

- Analyzing output from KCODE criticality calculations
- Interpreting k-effective values and confidence intervals
- Checking whether the fission source distribution has converged
- Evaluating Shannon entropy plots for source convergence
- Determining if additional inactive or active cycles are needed
- Troubleshooting non-converging criticality problems
- Comparing keff results from different geometric configurations
- Validating reactor core designs or critical assemblies
- Understanding dominance ratio and cycle-to-cycle correlation
- Interpreting the 10 statistical checks for criticality tallies

## Prerequisites

- **mcnp-source-builder**: Understanding KCODE and KSRC cards
- **mcnp-geometry-builder**: Core geometry with fissile materials
- **mcnp-material-builder**: Fissile material definitions
- **mcnp-statistics-checker**: Statistical validation concepts
- Basic understanding of reactor physics and criticality

## Core Concepts

### K-Effective (keff)

**Definition**: The effective neutron multiplication factor
- **keff > 1.0**: Supercritical (chain reaction grows)
- **keff = 1.0**: Critical (steady-state chain reaction)
- **keff < 1.0**: Subcritical (chain reaction dies out)

**Physical Meaning**:
```
keff = (neutrons in generation n+1) / (neutrons in generation n)
```

**MCNP Calculation**:
- MCNP runs multiple fission generations (cycles)
- Each cycle tracks nsrc neutrons from fission
- keff estimated from neutron balance
- Final keff is average over active cycles

### Active vs Inactive Cycles

**Inactive Cycles** (nskip):
- First N cycles discarded
- Source distribution converging
- Not used in keff calculation
- Typical: 20-100 cycles

**Active Cycles**:
- Cycles after source convergence
- Used for keff statistics
- Typical: 100-500 cycles
- More cycles = better statistics

**KCODE Format**:
```
KCODE  nsrc  k0  nskip  ncycles
       10000 1.0  50    150
       ^src  ^guess ^inactive ^total
```
- Total active cycles = ncycles - nskip = 100

### Shannon Entropy (Source Convergence Metric)

**Purpose**: Quantifies spatial distribution of fission source

**Formula**:
```
H = -Σᵢ pᵢ log₂(pᵢ)
```
- pᵢ = fraction of source in mesh cell i
- H increases as source spreads
- H plateaus when converged

**Interpretation**:
- **Rising entropy**: Source still spreading/converging
- **Flat entropy**: Source converged (good)
- **Oscillating entropy**: Possible dominance ratio issue
- **Continuously changing**: Not converged (increase nskip)

**Typical Behavior**:
```
Cycle    Entropy    Status
  1      4.5       Initial guess
  10     5.2       Source spreading
  30     5.8       Near convergence
  50     5.9       Converged ← start active cycles
  100    5.9       Stable (good)
```

### Statistical Checks for Criticality

MCNP performs 10 statistical checks on the final keff:

1. **Mean behavior**: keff estimate converged?
2. **Relative error**: R < 0.05 (5%)?
3. **Variance of variance (VOV)**: < 0.10?
4. **Figure of merit (FOM)**: Constant over 2nd half?
5. **Relative slope**: |slope| < 0.1?
6. **Tally fluctuation chart (TFC)**: Bins 1-8 pass?
7. **TFC slope**: Slope of last 1/2 bins near zero?
8. **Central moment**: Check for outliers
9. **Normality**: Distribution approximately normal?
10. **Largest history score**: Single history didn't dominate?

**Goal**: Pass all 10 checks for reliable results

### Confidence Intervals

**Standard Output**:
```
keff = 1.05432 ± 0.00045
       ^mean    ^1-sigma uncertainty
```

**Interpretation**:
- 68% confidence: keff in [1.05387, 1.05477]
- 95% confidence: keff in [1.05342, 1.05522] (±2σ)
- 99.7% confidence: keff in [1.05297, 1.05567] (±3σ)

**Relative Error**:
```
Rel. Error = (σ / keff) × 100%
           = (0.00045 / 1.05432) × 100%
           = 0.043%
```
- Target: < 0.1% for design calculations
- Target: < 0.01% for benchmarks

### Dominance Ratio

**Definition**: Ratio of 2nd to 1st eigenvalue (λ₁/λ₀)

**Impact on Convergence**:
- **DR ~ 0.5**: Fast convergence (~50 cycles)
- **DR ~ 0.8**: Moderate convergence (~200 cycles)
- **DR > 0.95**: Slow convergence (>1000 cycles)

**Symptoms of High DR**:
- Oscillating entropy
- Slow keff convergence
- Large cycle-to-cycle variation

**Solutions**:
- Increase inactive cycles (nskip)
- Increase source points (nsrc)
- Improve initial source guess (KSRC)

### Fission Matrix

**Purpose**: Track fission neutron flow between spatial regions

**Use**:
- Diagnose source convergence issues
- Identify dominant fission regions
- Detect spatial decoupling

**Output** (if requested):
```
FM  region1→region1  region1→region2
    region2→region1  region2→region2
```

---

## Decision Tree: Criticality Analysis Workflow

```
START: Received KCODE output file
  |
  +--> Extract keff and uncertainty
       |
       +--> Is relative error < target?
            |
            +--[YES]--> Check source convergence (entropy)
            |           |
            |           +--> Is entropy flat after nskip?
            |                |
            |                +--[YES]--> Check 10 statistical tests
            |                |           |
            |                |           +--> All 10 passed?
            |                |                |
            |                |                +--[YES]--> RESULT ACCEPTABLE ✓
            |                |                |           └─> Report keff ± uncertainty
            |                |                |
            |                |                +--[NO]---> INCREASE ACTIVE CYCLES
            |                |                            └─> Rerun with more ncycles
            |                |
            |                +--[NO]---> SOURCE NOT CONVERGED
            |                            ├─> Increase nskip
            |                            ├─> Check for high dominance ratio
            |                            └─> Improve KSRC initial guess
            |
            +--[NO]---> POOR STATISTICS
                        ├─> Increase nsrc (more neutrons/cycle)
                        ├─> Increase active cycles
                        └─> Check for geometry issues
```

## Tool Invocation

This skill includes a Python implementation for automated criticality analysis.

### Importing the Tool

```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer
analyzer = MCNPCriticalityAnalyzer()
```

### Basic Usage

```python
# Analyze KCODE results
kcode_analysis = analyzer.analyze_kcode('outp')

print(f"keff: {kcode_analysis['keff']} ± {kcode_analysis['error']}")
print(f"Entropy converged: {kcode_analysis['entropy_converged']}")
print(f"Statistical quality: {kcode_analysis['quality']}")
```

### Integration with MCNP Workflow

```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

analyzer = MCNPCriticalityAnalyzer()
results = analyzer.analyze_kcode("outp")

if results['quality'] == 'EXCELLENT':
    print(f"✓ keff = {results['keff']} ± {results['error']}")
else:
    print(f"⚠ Poor quality - increase cycles")
```

---

## Use Case 1: Basic KCODE Analysis (Bare U-235 Sphere)

**Scenario**: Analyzing output from bare U-235 sphere criticality calculation

**Input File** (for reference):
```
Bare U-235 Sphere Criticality
c Cell Cards
1    1  -18.7  -1  IMP:N=1          $ U-235 metal sphere
2    0          1  IMP:N=0          $ Graveyard

c Surface Cards
1    SO  8.7                         $ Critical radius ~8.7 cm

c Data Cards
MODE  N
M1   92235  1.0                      $ Pure U-235
KCODE  10000  1.0  50  150           $ 10k/cycle, skip 50, total 150
KSRC  0 0 0  2 0 0  -2 0 0  0 2 0   $ Initial source points
```

**Output Analysis**:

**Step 1: Extract keff from output file**
```
Look for final keff results table:

 the final estimated combined collision/absorption/track-length keff = 1.00345 with an estimated standard deviation of 0.00087

 the final keff estimator values and 68, 95, and 99 percent confidence intervals are:

                     keff       68% confidence      95% confidence      99% confidence
      collision     1.00321      1.00234 to 1.00408  1.00147 to 1.00495  1.00086 to 1.00556
      absorption    1.00368      1.00281 to 1.00455  1.00194 to 1.00542  1.00133 to 1.00603
      track length  1.00346      1.00259 to 1.00433  1.00172 to 1.00520  1.00111 to 1.00581
      col/abs/trk   1.00345      1.00258 to 1.00432  1.00171 to 1.00519  1.00110 to 1.00580
```

**Interpretation**:
- **keff = 1.00345**: System is slightly supercritical (expected for critical benchmark)
- **Uncertainty = ±0.00087**: 1-sigma (68% confidence)
- **Relative error = 0.087%**: Acceptable for design work
- **All three estimators agree**: Good sign of convergence

**Step 2: Check entropy plot**
```
Look for "source entropy" table:

    cycle     keff     entropy
        1    0.98234    5.2341
       10    1.00123    5.7832
       20    1.00456    5.9124
       30    1.00234    5.9456
       40    1.00321    5.9523
       50    1.00345    5.9534  ← Last inactive cycle
       60    1.00338    5.9531
      100    1.00345    5.9533
      150    1.00344    5.9532  ← Final cycle
```

**Interpretation**:
- Entropy rises rapidly (cycles 1-30): Source spreading
- Entropy plateaus at ~5.95 (cycles 30-150): Source converged
- Flat after cycle 50: nskip=50 is appropriate ✓

**Step 3: Check 10 statistical tests**
```
Look for "final result" section:

 the estimated 68, 95, and 99 percent confidence intervals are:
      1.00258 to 1.00432
      1.00171 to 1.00519
      1.00110 to 1.00580

 the 10 keff results and associated statistics are:

    test         result     status
    ----         ------     ------
    mean         passed     (fluctuation < 5%)
    relative error passed   (R = 0.087% < 10%)
    VOV          passed     (VOV = 0.054 < 0.10)
    FOM          passed     (constant over 2nd half)
    slope        passed     (|slope| = 0.03 < 0.1)
    TFC bins     passed     (bins 1-8 pass)
    TFC slope    passed     (slope near zero)
    central mom. passed     (no outliers)
    normality    passed     (approximately normal)
    largest hist.passed     (no single history dominance)

  *** All 10 statistical tests passed ***
```

**Interpretation**:
- **All tests passed**: Results are statistically reliable ✓
- **VOV = 0.054**: Well below 0.10 limit
- **Relative error = 0.087%**: Good precision

**Conclusion**:
```
RESULT: keff = 1.00345 ± 0.00087 (0.087%)
STATUS: ACCEPTABLE ✓
- Source converged by cycle 50
- All 10 statistical checks passed
- Adequate precision for design calculations
- System is critical (keff ≈ 1.00)
```

---

## Use Case 2: Detecting Poor Source Convergence

**Scenario**: Analysis shows entropy not converged, nskip too small

**Output Symptoms**:
```
    cycle     keff     entropy
        1    0.95234    4.8341
       10    0.98123    5.2832
       20    1.00456    5.6124
       30    1.02234    5.8456
       40    1.01321    5.9123
       50    1.00845    5.9534  ← Last inactive cycle (START ACTIVE)
       60    1.00538    5.9712  ← Still changing!
       70    1.00338    5.9823
       80    1.00245    5.9891
       90    1.00198    5.9934
      100    1.00165    5.9956  ← Still rising
      150    1.00145    5.9987  ← Never plateaued
```

**Problem Identification**:
- Entropy continuously rising through active cycles
- keff trending downward (correlated with entropy)
- Source distribution still evolving
- **DIAGNOSIS**: nskip=50 insufficient, active cycles contaminated

**Solution**:
```
c Increase inactive cycles to allow source convergence
c OLD: KCODE  10000  1.0  50  150
c NEW: KCODE  10000  1.0  100  200
         KCODE  10000  1.0  100  250
c              ^same  ^   ^increase skip to 100
c                         ^increase total cycles
```

**Expected Improved Output**:
```
    cycle     keff     entropy
        1    0.95234    4.8341
       50    1.00845    5.9534
      100    1.00345    5.9987  ← Plateau reached (last inactive)
      150    1.00342    5.9985  ← Stable
      200    1.00345    5.9986  ← Stable
      250    1.00344    5.9987  ← Converged ✓
```

**Key Points**:
- Monitor entropy: must plateau before active cycles begin
- If entropy trends during active cycles: increase nskip
- Typical rule: nskip should be where entropy stabilizes + 20% margin
- Better to oversample inactive than undersample

---

## Use Case 3: Insufficient Active Cycles (Poor Statistics)

**Scenario**: Source converged but statistical uncertainty too large

**Output Analysis**:
```
 the final estimated keff = 1.00345 with an estimated standard deviation of 0.00487
                                                                          ^^^^^
                                                                          TOO LARGE!

 relative error = 0.485%  (target: < 0.1%)
                 ^^^^^
                 POOR STATISTICS

 the 10 keff results:
    test         result     status
    ----         ------     ------
    mean         passed
    relative error FAILED   (R = 0.485% > 0.1%)  ← KEY ISSUE
    VOV          passed
    FOM          FAILED    (not constant)        ← SYMPTOM
    ...
```

**Problem**: Only 100 active cycles insufficient for <0.1% precision

**Solution 1: Increase Total Cycles**
```
c OLD: KCODE  10000  1.0  50  150  (100 active cycles)
c NEW: KCODE  10000  1.0  50  550  (500 active cycles)
         KCODE  10000  1.0  50  550
c                         ^same ^increase total
```

**Solution 2: Increase Neutrons Per Cycle**
```
c Increase nsrc for better per-cycle statistics
c OLD: KCODE  10000  1.0  50  150
c NEW: KCODE  50000  1.0  50  150
         KCODE  50000  1.0  50  150
c              ^50k neutrons/cycle
```

**Solution 3: Combined Approach**
```
c Best: Increase both nsrc and active cycles
KCODE  20000  1.0  50  350
c      ^20k/cycle  ^300 active cycles
```

**Statistical Relationship**:
```
Relative Error ∝ 1 / √(nsrc × n_active)

Example:
- Original: nsrc=10000, n_active=100 → R ~ 0.485%
- Increase nsrc to 20000: R ~ 0.343% (√2 improvement)
- Increase n_active to 400: R ~ 0.242% (2× improvement)
- Both: R ~ 0.121% (√8 improvement)
```

---

## Use Case 4: High Dominance Ratio (Oscillating Convergence)

**Scenario**: Large, loosely-coupled reactor with slow convergence

**Symptoms**:
```
    cycle     keff     entropy
       50    1.00845    5.9534
       60    1.00938    5.9612  ← Rising
       70    1.00638    5.9723  ← Falling
       80    1.00838    5.9656  ← Rising
       90    1.00538    5.9734  ← Falling
      100    1.00745    5.9678  ← Oscillating
      ...
      (continues oscillating for many cycles)
```

**Diagnosis**:
- Entropy and keff oscillate together
- Long-period oscillation (10-50 cycles)
- **Cause**: High dominance ratio (2nd eigenmode slow to decay)

**Explanation**:
```
Fission source = c₀φ₀ + c₁φ₁ + c₂φ₂ + ...
                 ^fundamental  ^1st harmonic

After n cycles: source ≈ c₀φ₀ + c₁(DR)ⁿφ₁

If DR = 0.95:
- After 50 cycles: c₁(0.95)⁵⁰φ₁ = 0.077c₁φ₁  (still 7.7%)
- After 100 cycles: c₁(0.95)¹⁰⁰φ₁ = 0.006c₁φ₁ (0.6%)
- After 500 cycles: negligible
```

**Solutions**:

**Solution 1: Dramatically Increase Inactive Cycles**
```
c For DR ~ 0.95, need ~100 cycles to reduce 2nd mode to 1%
c OLD: KCODE  10000  1.0  50  150
c NEW: KCODE  10000  1.0  200  500
         KCODE  10000  1.0  200  500
c                         ^skip 200 cycles
```

**Solution 2: Better Initial Source Guess**
```
c Use more KSRC points distributed throughout reactor
c OLD: KSRC  0 0 0  10 0 0  -10 0 0
c NEW: KSRC with 20-50 points spanning entire core
KSRC  0 0 0    10 0 0   -10 0 0    0 10 0    0 -10 0
     50 0 0   -50 0 0    0 50 0    0 -50 0
     20 20 0  -20 20 0   20 -20 0  -20 -20 0
     ...  (more points in all fuel regions)
```

**Solution 3: Increase nsrc**
```
c More neutrons per cycle helps sample higher modes
c OLD: KCODE  10000  1.0  200  500
c NEW: KCODE  50000  1.0  200  500
         KCODE  50000  1.0  200  500
```

**Verification**:
After fixes, should see:
```
    cycle     keff     entropy
      200    1.00345    5.9987  ← Last inactive
      250    1.00342    5.9986  ← Stable
      300    1.00345    5.9987  ← Stable
      400    1.00344    5.9986  ← No oscillation ✓
      500    1.00345    5.9987  ← Converged
```

---

## Use Case 5: Comparing Keff from Different Configurations

**Scenario**: Evaluating control rod worth (keff with rods IN vs OUT)

**Configuration 1: Control Rods OUT**
```
Output: keff = 1.05432 ± 0.00045 (0.043%)
```

**Configuration 2: Control Rods IN**
```
Output: keff = 0.98765 ± 0.00052 (0.053%)
```

**Analysis: Is the difference significant?**

**Method 1: Confidence Interval Test**
```
Config 1: keff₁ = 1.05432 ± 0.00045
Config 2: keff₂ = 0.98765 ± 0.00052

Difference: Δk = keff₁ - keff₂ = 0.06667

Combined uncertainty:
σ_total = √(σ₁² + σ₂²) = √(0.00045² + 0.00052²) = 0.00069

Number of standard deviations:
N_σ = Δk / σ_total = 0.06667 / 0.00069 = 96.6 σ

Conclusion: Difference is HIGHLY SIGNIFICANT (>3σ threshold)
```

**Method 2: Reactivity Calculation**
```
Reactivity (in $): ρ = (keff - 1) / keff

Config 1: ρ₁ = (1.05432 - 1) / 1.05432 = 0.05154 = +5154 pcm
Config 2: ρ₂ = (0.98765 - 1) / 0.98765 = -0.01250 = -1250 pcm

Control rod worth: Δρ = ρ₁ - ρ₂ = 6404 pcm = $6.40 (assuming β_eff ~ 0.0065)
```

**Key Points**:
- Always account for combined uncertainty when comparing
- Difference should be >3σ to claim significance
- Report reactivity worth in pcm or dollars
- Consider correlated uncertainties if using same geometry with modifications

---

## Use Case 6: Interpreting the 10 Statistical Checks

**Scenario**: Understanding what each statistical check means

**MCNP Output**:
```
 the 10 keff results and associated statistics:

    result    status    value     criterion    notes
    ------    ------    -----     ---------    -----
1.  mean      passed    ---       (behavior)   keff mean converged
2.  rel err   passed    0.082%    < 5%         Acceptable precision
3.  VOV       MISSED    0.156     < 0.10       Variance unstable!
4.  FOM       passed    constant  2nd half     Efficiency stable
5.  slope     passed    0.03      < 0.1        No trend
6.  TFC 1-8   passed    ---       all pass     Bins converged
7.  TFC slope passed    -0.02     ~0           Bin trend okay
8.  central   passed    ---       no outliers  No anomalies
9.  normal    passed    ---       approx norm  Distribution okay
10. largest   passed    ---       not dominate No single history outlier
```

**Detailed Interpretation**:

**Check 1: Mean Behavior**
- Tests if keff is fluctuating wildly or settling down
- **Pass**: Mean converging to stable value
- **Fail**: Mean still trending (need more cycles)

**Check 2: Relative Error**
- R = (σ / keff) × 100%
- **Pass**: R < 5% (loose criterion for criticality)
- **Target for design**: R < 0.1%
- **Target for benchmarks**: R < 0.01%

**Check 3: Variance of Variance (VOV)**
- Measures stability of variance estimator
- **Pass**: VOV < 0.10 (variance itself has converged)
- **Fail**: VOV ≥ 0.10 (need more cycles, variance unstable)
- **In this example**: VOV=0.156 → INCREASE ACTIVE CYCLES

**Check 4: Figure of Merit (FOM)**
- FOM = 1 / (R² × T) where T = computer time
- **Pass**: FOM constant over 2nd half of active cycles
- **Fail**: FOM changing (efficiency problem)

**Check 5: Relative Slope**
- Tests for linear trend in keff vs cycle
- **Pass**: |slope| < 0.1
- **Fail**: Strong trend (source not converged or physics bias)

**Check 6: Tally Fluctuation Chart (TFC) Bins 1-8**
- Divides active cycles into 10 bins, checks convergence in each
- **Pass**: All 8 bins (1-8) show good behavior
- **Fail**: Early bins show poor statistics (increase cycles)

**Check 7: TFC Slope**
- Checks trend in last 5 bins (2nd half)
- **Pass**: Slope near zero (no systematic drift)
- **Fail**: Strong trend (not converged)

**Check 8: Central Moment**
- Checks for outlier cycles
- **Pass**: No individual cycles with extreme keff
- **Fail**: One or more cycles are statistical outliers

**Check 9: Normality**
- Tests if keff distribution is approximately normal
- **Pass**: Approximately Gaussian
- **Fail**: Skewed distribution (unusual, check for problems)

**Check 10: Largest History Score**
- Ensures no single neutron history dominated result
- **Pass**: Largest score << total
- **Fail**: One history contributed excessively (rare, check geometry)

**Action for This Example**:
```
Problem: VOV = 0.156 (failed Check 3)
Solution: Increase active cycles from 100 to 300+

c OLD: KCODE  10000  1.0  50  150
c NEW: KCODE  10000  1.0  50  400
```

---

## Use Case 7: Optimizing Cycle Parameters

**Scenario**: Determining optimal nsrc, nskip, ncycles for new problem

**Step-by-Step Optimization**:

**Step 1: Initial Conservative Run**
```
c Start with conservative parameters
KCODE  5000  1.0  20  50
c      ^small nsrc  ^minimal cycles for quick test
```

**Run 1 Output**:
```
Entropy plateaus at cycle 15
Relative error = 0.8%
VOV = 0.25 (too high)
Runtime: 5 minutes
```

**Analysis**: Source converges quickly, but statistics poor

**Step 2: Increase Statistics**
```
c Entropy converged by cycle 15, use nskip=20 (margin)
c Increase nsrc and active cycles
KCODE  10000  1.0  20  120
c      ^double nsrc    ^100 active cycles
```

**Run 2 Output**:
```
Entropy stable after cycle 20 ✓
Relative error = 0.25%
VOV = 0.12 (still slightly high)
Runtime: 20 minutes
```

**Analysis**: Better, but VOV still above 0.10 limit

**Step 3: Final Optimization**
```
c Keep nsrc=10000, increase active cycles
KCODE  10000  1.0  30  230
c      ^same     ^add margin ^200 active
```

**Run 3 Output**:
```
Entropy stable ✓
Relative error = 0.09%
VOV = 0.08 ✓
All 10 checks passed ✓
Runtime: 45 minutes
```

**Final Recommendation**:
```
KCODE  10000  1.0  30  230
c      Optimized parameters:
c      - nsrc = 10,000 (adequate sampling per cycle)
c      - nskip = 30 (entropy converges by cycle 15, use 2× margin)
c      - ncycles = 230 (200 active cycles for good statistics)
c      Expected: R ~ 0.09%, VOV ~ 0.08, runtime ~ 45 min
```

**General Guidelines**:
```
Problem Type          nsrc      nskip    n_active
-------------         ------    ------   --------
Simple (sphere)       5000      20-50    100-200
PWR assembly          10000     50-100   200-400
Full core             20000     100-200  400-800
Loosely coupled       50000     200-500  500-2000
```

---

## Use Case 8: Troubleshooting Zero or Invalid Keff

**Scenario**: MCNP reports keff = 0.00000 or crashes

**Common Causes and Solutions**:

**Problem 1: No Fissile Material**
```
ERROR: keff estimator = 0.00000

Check material definitions:
M1   92238  1.0  $ U-238 only - NOT FISSILE!

Solution: Add fissile isotope
M1   92235  0.03  92238  0.97  $ Add U-235
```

**Problem 2: SDEF Card Present (Wrong Mode)**
```
ERROR: SDEF card conflicts with KCODE

Input has both:
SDEF  POS=0 0 0  ERG=14.1  $ FIXED SOURCE
KCODE  10000  1.0  50  150   $ CRITICALITY

Solution: Remove SDEF for criticality problems
c SDEF  POS=0 0 0  ERG=14.1  $ DELETE THIS LINE
KCODE  10000  1.0  50  150
KSRC  0 0 0
```

**Problem 3: NPS Card Present (Wrong Mode)**
```
ERROR: NPS card conflicts with KCODE

Solution: Remove NPS card
c NPS  1000000  $ DELETE - not used with KCODE
KCODE  10000  1.0  50  150
```

**Problem 4: Geometry Errors (Lost Particles)**
```
ERROR: Lost particles, keff unreliable

fatal error.  12 particles got lost

Check for:
- Gaps between cells
- Overlapping cells
- Missing graveyard (IMP:N=0 cell)

Solution: Run geometry plot
mcnp6 inp=input.i ip
  PLOT → check for geometry errors
```

**Problem 5: All Neutrons Absorbed (Keff << 1)**
```
Output: keff = 0.12345 (extremely subcritical)

Possible causes:
- Insufficient fissile material
- Strong absorber present (control rods, poisons)
- Geometry too small (high leakage)

Check:
- Material compositions (M cards)
- Core size (increase dimensions)
- Reflector presence (reduce leakage)
```

**Problem 6: Source Outside Fissile Region**
```
Warning: KSRC points outside fissile material

KSRC  100 100 100  $ Point far from core

Solution: Place KSRC in/near fuel
KSRC  0 0 0  5 0 0  -5 0 0  $ Points in core region
```

---

## Common Errors and Troubleshooting

### Error 1: "Entropy not converging"

**Symptom**: Entropy continuously rises through active cycles

**Cause**: nskip too small, source still spreading

**Fix**:
```
c BAD:
KCODE  10000  1.0  20  120  $ Only 20 inactive

c GOOD:
KCODE  10000  1.0  100  300  $ 100 inactive for convergence
```

---

### Error 2: "VOV > 0.10 (Check 3 failed)"

**Symptom**: Variance of variance exceeds limit

**Cause**: Insufficient active cycles, variance estimator unstable

**Fix**:
```
c BAD:
KCODE  10000  1.0  50  100  $ Only 50 active cycles

c GOOD:
KCODE  10000  1.0  50  350  $ 300 active cycles
c OR increase nsrc:
KCODE  30000  1.0  50  150  $ 3× more neutrons/cycle
```

---

### Error 3: "keff trending during active cycles"

**Symptom**: keff shows consistent upward or downward trend

**Cause**: Source not converged (correlated with entropy trend)

**Fix**:
```
Check entropy plot:
- If entropy also trending → increase nskip
- If entropy flat but keff trends → check for geometry/physics errors

c Solution:
KCODE  10000  1.0  150  350  $ Increase nskip from 50 to 150
```

---

### Error 4: "Relative error > 5% (Check 2 failed)"

**Symptom**: Unacceptable statistical uncertainty

**Cause**: Too few source neutrons × active cycles

**Fix**:
```
c Target: Rel Error ∝ 1/√(nsrc × n_active)

c BAD:
KCODE  5000  1.0  50  100  $ nsrc × n_active = 250,000

c GOOD (Option 1):
KCODE  20000  1.0  50  100  $ 4× nsrc → 2× improvement

c GOOD (Option 2):
KCODE  5000  1.0  50  500  $ 4× n_active → 2× improvement

c BEST (Option 3):
KCODE  10000  1.0  50  250  $ Combined approach
```

---

### Error 5: "Oscillating keff and entropy"

**Symptom**: Both oscillate with long period (20-100 cycles)

**Cause**: High dominance ratio (2nd eigenmode slow to decay)

**Fix**:
```
c Solution 1: Dramatically increase nskip
KCODE  10000  1.0  300  600  $ 300 inactive cycles

c Solution 2: Better initial source guess
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0
     20 0 0  -20 0 0  0 20 0  0 -20 0
     (distribute 20-50 points throughout core)

c Solution 3: Increase nsrc
KCODE  50000  1.0  200  500
```

---

### Error 6: "keff differs from benchmark"

**Symptom**: Your result differs significantly from reference

**Cause**: Multiple possibilities

**Debugging Steps**:
```
1. Check material definitions (ZAID numbers, fractions)
   - Verify isotopes (92235 vs 92238)
   - Check atomic vs weight fractions
   - Verify densities (positive vs negative)

2. Check geometry
   - Run MCNP plot to visualize
   - Compare dimensions to benchmark specs
   - Check for gaps/overlaps

3. Check data libraries
   - Verify ENDF version (70c vs 80c)
   - Check thermal scattering (MT cards)
   - Confirm temperature (TMP cards)

4. Check convergence
   - Ensure source converged (entropy flat)
   - Verify sufficient statistics (R < 0.1%)
   - Pass all 10 checks

5. Compare intermediate results
   - Check fission rate distribution
   - Compare neutron spectrum
   - Verify leakage fraction
```

---

## Integration with Other Skills

### 1. **mcnp-source-builder**
How it integrates: Provides KCODE/KSRC setup that this skill analyzes

**Workflow**:
```
1. mcnp-source-builder → Creates KCODE card with initial parameters
2. THIS SKILL → Analyzes first run, determines if source converged
3. mcnp-source-builder → Adjusts KSRC points if convergence poor
4. THIS SKILL → Validates improved convergence
```

**Example**:
```
Initial setup (source-builder):
KCODE  10000  1.0  50  150
KSRC  0 0 0

Analysis (THIS SKILL):
- Entropy shows poor convergence
- Recommendation: Add more KSRC points

Improved setup (source-builder):
KCODE  10000  1.0  100  250
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0  0 0 10  0 0 -10
```

---

### 2. **mcnp-statistics-checker**
How it integrates: Provides general statistical validation framework

**Workflow**:
```
1. THIS SKILL → Focuses on criticality-specific checks (entropy, keff)
2. mcnp-statistics-checker → Validates general statistical quality
3. Combined → Comprehensive validation of criticality results
```

**Overlap and Differences**:
- **Statistics-checker**: Generic tally validation (10 checks for any tally)
- **THIS SKILL**: Criticality-specific (keff, entropy, source convergence)
- **Use both**: For complete validation of criticality + tallies

---

### 3. **mcnp-geometry-builder**
How it integrates: Geometry affects convergence rate and keff

**Workflow**:
```
1. mcnp-geometry-builder → Creates core geometry
2. THIS SKILL → Analyzes keff and convergence
3. IF convergence slow (high DR) → geometry-builder modifies layout
4. THIS SKILL → Validates improved convergence
```

**Example**:
```
Problem: Two separated fuel regions cause high dominance ratio

Solution (geometry-builder):
- Add coupling between regions (reduce neutron streaming)
- Adjust reflector to reduce leakage
- Modify control rod positions

Result (THIS SKILL):
- Faster convergence (lower DR)
- More stable entropy
- Fewer inactive cycles needed
```

---

### 4. **mcnp-material-builder**
How it integrates: Material composition directly affects keff

**Workflow**:
```
1. mcnp-material-builder → Defines fissile materials
2. THIS SKILL → Analyzes keff results
3. IF keff differs from target → material-builder adjusts enrichment
4. THIS SKILL → Validates new keff value
```

**Example - Enrichment Adjustment**:
```
Initial (material-builder):
M1  92235  0.03  92238  0.97  $ 3% enriched

Analysis (THIS SKILL):
keff = 0.95432 (subcritical, need keff ≈ 1.00)

Adjusted (material-builder):
M1  92235  0.032  92238  0.968  $ 3.2% enriched (small increase)

New Analysis (THIS SKILL):
keff = 1.00123 (critical ✓)
```

---

### 5. **mcnp-output-parser**
How it integrates: Extracts keff/entropy data from output files

**Workflow**:
```
1. mcnp-output-parser → Reads output file, extracts keff table
2. THIS SKILL → Interprets extracted data
3. mcnp-output-parser → Extracts entropy vs cycle
4. THIS SKILL → Analyzes convergence behavior
```

**Data Extracted**:
- Final keff (collision, absorption, track-length)
- Confidence intervals (68%, 95%, 99%)
- Entropy vs cycle number
- 10 statistical check results
- Active/inactive cycle data

---

### Typical Workflow: Complete Criticality Analysis

```
1. mcnp-geometry-builder   → Define core geometry
2. mcnp-material-builder   → Define fissile materials
3. mcnp-source-builder     → Create KCODE/KSRC cards
4. mcnp-physics-builder    → Set MODE N, physics options
5. [Run MCNP]
6. mcnp-output-parser      → Extract keff and entropy data
7. THIS SKILL              → Analyze convergence and statistics
8. IF not converged:
   - mcnp-source-builder   → Adjust KCODE parameters
   - Go to step 5
9. IF converged:
   - THIS SKILL            → Report final keff ± uncertainty
   - mcnp-statistics-checker → Validate tally statistics (if present)
10. DONE ✓
```

---

## Validation Checklist

Before accepting criticality results:

### Source Convergence
- [ ] Entropy plot shows plateau after nskip cycles
- [ ] Entropy remains stable during all active cycles
- [ ] No long-period oscillations in entropy or keff
- [ ] nskip ≥ convergence cycle + 20% margin

### Statistical Quality
- [ ] Relative error < 0.1% (design) or < 0.01% (benchmark)
- [ ] All 10 statistical checks passed
- [ ] VOV < 0.10
- [ ] No trending in keff during active cycles
- [ ] Confidence intervals reasonable (not too wide)

### Physical Reasonableness
- [ ] Keff value makes physical sense for system
- [ ] Three estimators (col/abs/trk) agree within 2σ
- [ ] No warning messages about lost particles
- [ ] No fatal errors in output
- [ ] Geometry plotted and verified

### Computational Adequacy
- [ ] Sufficient nsrc (typically ≥ 5,000)
- [ ] Adequate active cycles (typically ≥ 100)
- [ ] Total runtime reasonable for problem complexity
- [ ] Results reproducible (check with different random seeds)

### Documentation
- [ ] KCODE parameters recorded
- [ ] Final keff ± uncertainty documented
- [ ] Convergence behavior noted
- [ ] Any anomalies or warnings addressed
- [ ] Comparison to expected/benchmark values (if available)

---

## Advanced Topics

### 1. Fission Matrix Analysis

**Purpose**: Diagnose spatial coupling and source convergence

**FMESH Card** (generates fission matrix):
```
FMESH4:N  GEOM=XYZ  ORIGIN=-50 -50 -50
          IMESH=50  IINTS=5
          JMESH=50  JINTS=5
          KMESH=50  KINTS=5
          OUT=IJ  $ Output fission matrix
```

**Interpretation**:
- Diagonal elements: Self-coupling (fissions in region i from neutrons born in i)
- Off-diagonal: Inter-region coupling
- Weak coupling → High dominance ratio → Slow convergence

---

### 2. Adjoint-Weighted Tallies

**Purpose**: Reaction rate tallies weighted by importance to keff

**Application**:
```
F4:N  1  $ Flux tally
FM4  -1 1 -6  $ KERMA (heating) weighted by adjoint
```

**Use Case**: Identify most important fissile regions for keff

---

### 3. Sensitivity and Uncertainty Analysis

**Perturbation Method**:
```
1. Run base case: keff₀
2. Perturb parameter (e.g., density +1%)
3. Run perturbed: keff₁
4. Sensitivity: S = (Δkeff/keff₀) / (Δρ/ρ₀)
```

**Example**:
```
Base: M1 92235 -18.7  → keff₀ = 1.00000
Pert: M1 92235 -18.887 (+1%) → keff₁ = 1.00234
S = (0.00234/1.00000) / (0.01) = 0.234 (23.4% per 1% density change)
```

---

### 4. Temperature Coefficient of Reactivity

**Method**: Calculate keff at different temperatures

```
Case 1 (Cold): TMP1 2.53e-8  → keff₁ = 1.01234
Case 2 (Hot):  TMP1 1.20e-7  → keff₂ = 0.99876

Temperature coefficient:
α_T = (ρ₂ - ρ₁) / (T₂ - T₁)
    = [(k₂-1)/k₂ - (k₁-1)/k₁] / (1400K - 293K)
    = [-0.00124 - 0.01218] / 1107K
    = -1.21×10⁻⁵ /K = -1.21 pcm/K (negative = safe)
```

---

### 5. Parallel Reproducibility

**Issue**: MPI runs with different task numbers may give slightly different keff

**Cause**: Different random number sequences

**Solution**: Use same random seed and tasks
```
MCNP command:
mcnp6 inp=input.i tasks 16 seed 123456789
```

**Verification**:
```
Run 1: tasks 8,  seed 123 → keff = 1.00345
Run 2: tasks 8,  seed 123 → keff = 1.00345 (identical ✓)
Run 3: tasks 16, seed 123 → keff = 1.00348 (different, but within uncertainty)
```

---

## Best Practices

### 1. **Always Check Entropy Before Trusting Keff**
Rule: If entropy not converged, keff is meaningless
- Plot entropy vs cycle
- Ensure plateau before active cycles begin
- Use conservative nskip (better to overestimate)

### 2. **Use Conservative Initial Parameters**
Start with:
```
KCODE  10000  1.0  100  300
c      ^adequate ^conservative ^good statistics
```
Adjust down only after confirming faster convergence

### 3. **Distribute KSRC Points Throughout Fissile Regions**
Bad:
```
KSRC  0 0 0  $ Single point
```
Good:
```
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0
     0 0 10  0 0 -10  5 5 0  -5 -5 0
c    8 points spanning core
```

### 4. **Target < 0.1% Relative Error for Design**
- 0.1-0.5%: Preliminary analysis
- 0.05-0.1%: Design calculations
- < 0.05%: Final design verification
- < 0.01%: Benchmark validation

### 5. **Always Verify Geometry with Plot**
Before long production runs:
```
mcnp6 inp=input.i ip
PLOT
  (verify no gaps, overlaps, correct materials)
```

### 6. **Document All Runs**
Record:
- KCODE parameters used
- Final keff ± uncertainty
- Convergence behavior (entropy, cycles needed)
- Runtime
- Any warnings or errors
- Comparison to expected values

### 7. **Use Multiple Random Seeds for Validation**
Check reproducibility:
```
Run 1: mcnp6 inp=input.i
Run 2: mcnp6 inp=input.i seed 987654321
Compare: keff should agree within 2σ
```

### 8. **Understand Physical Context**
- Know approximate keff before running
- Critical system: keff ≈ 1.00
- Fuel assembly in water: keff typically 1.2-1.4
- Bare metal sphere: Check critical mass tables
- If result unexpected: verify input, don't trust blindly

---

## References

**Documentation Summary**:
- **Section 9**: KCODE, KSRC cards (source-builder reference)
- **Section 15**: Criticality examples (example calculations)
- **Section 10**: Tally definitions (if using tallies with criticality)
- **Section 1-4**: Input structure and formatting

**Related Skills**:
- **mcnp-source-builder**: KCODE/KSRC card creation
- **mcnp-statistics-checker**: General statistical validation (10 checks)
- **mcnp-output-parser**: Extracting keff and entropy data
- **mcnp-geometry-builder**: Core geometry definition
- **mcnp-material-builder**: Fissile material specifications

**User Manual References**:
- Chapter 5.8: Source Data Cards (KCODE, KSRC)
- Chapter 3: Introduction to MCNP Usage (criticality workflow)
- Appendix: Statistical tests explanation

**Slash Command**:
- `.claude/commands/mcnp-criticality-analyzer.md`: Quick reference for analysis tasks

---

**End of MCNP Criticality Analyzer Skill**
