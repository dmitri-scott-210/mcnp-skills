# KCODE Analysis Guide

**Purpose:** Comprehensive guide to analyzing MCNP KCODE criticality calculations, interpreting k-effective values, confidence intervals, and statistical quality checks.

---

## Overview

KCODE (K-code) calculations solve the criticality eigenvalue problem to determine the effective neutron multiplication factor (k-eff) of fissile systems. This guide explains how to analyze KCODE output, interpret results, and validate statistical quality.

---

## K-Effective (keff) Fundamentals

### Definition

**K-effective (keff)**: The effective neutron multiplication factor
- **keff > 1.0**: Supercritical (chain reaction grows)
- **keff = 1.0**: Critical (steady-state chain reaction)
- **keff < 1.0**: Subcritical (chain reaction dies out)

**Physical Meaning:**
```
keff = (neutrons in generation n+1) / (neutrons in generation n)
```

### MCNP Calculation Method

MCNP runs multiple fission generations (cycles):
1. Start with initial source distribution (KSRC)
2. Transport neutrons until they die (absorption, leakage)
3. Record fission sites
4. Sample new generation from fission sites
5. Repeat for many cycles
6. Average keff over active cycles

### Three keff Estimators

MCNP provides three independent estimators:

**1. Collision Estimator:**
```
Based on collision rates in fissile materials
Tracks: (fissions × ν) / (collisions)
```

**2. Absorption Estimator:**
```
Based on absorption and fission rates
Tracks: (fissions × ν) / (absorptions)
```

**3. Track-Length Estimator:**
```
Based on flux and cross sections
Tracks: (∫ flux × ν × Σf dV) / (∫ flux × Σa dV)
```

**Agreement Check:**
- All three should agree within 2σ
- If disagree: Convergence issues or geometry problems
- Final combined estimator: Weighted average of all three

---

## KCODE Card Format

```
KCODE  nsrc  k0  nskip  ncycles
```

**Parameters:**
- **nsrc**: Neutrons per cycle (5,000-50,000 typical)
- **k0**: Initial guess for keff (usually 1.0)
- **nskip**: Inactive cycles (source convergence, 20-500 typical)
- **ncycles**: Total cycles (nskip + active cycles)

**Active Cycles:**
```
n_active = ncycles - nskip
```
Active cycles used for keff statistics (100-2000 typical)

**Example:**
```
KCODE  10000  1.0  50  150
       ^10k neutrons/cycle
              ^guess 1.0
                  ^skip first 50 cycles
                      ^run 150 total (100 active)
```

---

## Extracting keff from Output

### Final keff Table

Look for this section in output:
```
 the final estimated combined collision/absorption/track-length keff = 1.00345 with an estimated standard deviation of 0.00087

 the final keff estimator values and 68, 95, and 99 percent confidence intervals are:

                     keff       68% confidence      95% confidence      99% confidence
      collision     1.00321      1.00234 to 1.00408  1.00147 to 1.00495  1.00086 to 1.00556
      absorption    1.00368      1.00281 to 1.00455  1.00194 to 1.00542  1.00133 to 1.00603
      track length  1.00346      1.00259 to 1.00433  1.00172 to 1.00520  1.00111 to 1.00581
      col/abs/trk   1.00345      1.00258 to 1.00432  1.00171 to 1.00519  1.00110 to 1.00580
```

### Key Information

**Combined keff:**
```
keff = 1.00345 ± 0.00087 (1σ)
```

**Relative Error:**
```
R = (σ / keff) × 100%
  = (0.00087 / 1.00345) × 100%
  = 0.087%
```

**Confidence Intervals:**
- 68% CI: keff ∈ [1.00258, 1.00432] (±1σ)
- 95% CI: keff ∈ [1.00171, 1.00519] (±2σ)
- 99.7% CI: keff ∈ [1.00110, 1.00580] (±3σ)

---

## Active vs Inactive Cycles

### Inactive Cycles (nskip)

**Purpose:** Allow fission source distribution to converge before collecting statistics

**Characteristics:**
- First N cycles discarded
- Source spreading/converging spatially
- Not used in keff calculation
- Shannon entropy monitored

**Typical Values:**
- Simple geometry: 20-50 cycles
- Complex geometry: 50-100 cycles
- Loosely coupled: 100-500 cycles
- High dominance ratio: 200-1000 cycles

### Active Cycles

**Purpose:** Collect statistics for keff after source converged

**Characteristics:**
- Cycles after nskip
- Used for keff mean and uncertainty
- More cycles = better statistics
- All 10 statistical checks applied

**Typical Values:**
- Preliminary: 50-100 active cycles
- Design: 200-500 active cycles
- Validation: 500-2000 active cycles

### Determining Adequate nskip

**Method:**
1. Plot entropy vs cycle number
2. Find cycle where entropy plateaus
3. Set nskip = plateau_cycle + 20% margin

**Example:**
```
Entropy plateaus at cycle 40
nskip = 40 × 1.2 = 48 ≈ 50 cycles
```

---

## The 10 Statistical Checks

MCNP performs 10 tests on final keff to validate statistical quality.

### Check 1: Mean Behavior

**Purpose:** Verify keff estimate has converged

**Test:** Is keff mean still fluctuating wildly?

**Pass Condition:** Mean settling to stable value

**Fail:** Mean still trending → Need more cycles or source not converged

### Check 2: Relative Error

**Purpose:** Verify statistical uncertainty acceptable

**Test:** R = (σ/keff) × 100%

**Pass Condition:**
- General: R < 5%
- Design: R < 0.1%
- Benchmark: R < 0.01%

**Fail:** R too large → Increase nsrc or active cycles

### Check 3: Variance of Variance (VOV)

**Purpose:** Verify variance estimator itself has converged

**Test:** VOV = Var(σ²) / [E(σ²)]²

**Pass Condition:** VOV < 0.10

**Fail:** VOV ≥ 0.10 → Variance unstable, need more active cycles

**This is the most commonly failed check**

### Check 4: Figure of Merit (FOM)

**Purpose:** Verify computational efficiency stable

**Test:** FOM = 1/(R² × T) where T = time

**Pass Condition:** FOM constant over 2nd half of active cycles

**Fail:** FOM changing → Efficiency issues

### Check 5: Relative Slope

**Purpose:** Detect linear trends in keff

**Test:** Fit line to keff vs cycle, measure slope

**Pass Condition:** |slope| < 0.1

**Fail:** Strong trend → Source not converged or physics bias

### Check 6: Tally Fluctuation Chart (TFC) Bins 1-8

**Purpose:** Check convergence in each time segment

**Test:** Divide active cycles into 10 bins, check each

**Pass Condition:** Bins 1-8 show good statistical behavior

**Fail:** Early bins poor → Need more total cycles

### Check 7: TFC Slope

**Purpose:** Detect trends in later cycles

**Test:** Slope of last 5 bins (2nd half)

**Pass Condition:** Slope near zero

**Fail:** Strong trend → Not fully converged

### Check 8: Central Moment

**Purpose:** Detect outlier cycles

**Test:** Check for cycles with extreme keff values

**Pass Condition:** No individual cycles are statistical outliers

**Fail:** Outliers present → Investigate anomalous cycles

### Check 9: Normality

**Purpose:** Verify keff distribution approximately Gaussian

**Test:** Statistical test for normality

**Pass Condition:** Approximately normal distribution

**Fail:** Skewed distribution → Unusual, check for problems

### Check 10: Largest History Score

**Purpose:** Ensure no single neutron history dominated

**Test:** Check if largest contribution << total

**Pass Condition:** No single history dominance

**Fail:** One history contributed excessively → Rare, check geometry

---

## Statistical Quality Targets

### By Application Type

| Application | Relative Error | VOV | Statistical Checks |
|-------------|----------------|-----|-------------------|
| Preliminary screening | < 1% | < 0.2 | 7-8 of 10 pass |
| Scoping studies | < 0.5% | < 0.15 | 9 of 10 pass |
| Design calculations | < 0.1% | < 0.10 | All 10 pass |
| Final verification | < 0.05% | < 0.08 | All 10 pass |
| Benchmark validation | < 0.01% | < 0.05 | All 10 pass |

### Recommended KCODE Parameters

| Problem Type | nsrc | nskip | n_active | Expected R |
|--------------|------|-------|----------|------------|
| Simple sphere | 5,000 | 30 | 100 | ~0.2% |
| Fuel assembly | 10,000 | 50 | 200 | ~0.1% |
| Reactor core | 20,000 | 100 | 500 | ~0.05% |
| Loosely coupled | 50,000 | 300 | 1000 | ~0.03% |

---

## Comparing keff Values

### Method: Confidence Interval Test

**Problem:** Determine if two keff values are statistically different

**Procedure:**
```
Case 1: keff₁ = k₁ ± σ₁
Case 2: keff₂ = k₂ ± σ₂

Difference: Δk = k₁ - k₂

Combined uncertainty: σ_total = √(σ₁² + σ₂²)

Number of σ: N_σ = Δk / σ_total
```

**Interpretation:**
- N_σ < 1: No significant difference
- 1 < N_σ < 2: Marginal difference
- 2 < N_σ < 3: Likely different (95% confidence)
- N_σ > 3: Definitely different (99.7% confidence)

### Example: Control Rod Worth

**Configuration 1: Rods OUT**
```
keff₁ = 1.05432 ± 0.00045
```

**Configuration 2: Rods IN**
```
keff₂ = 0.98765 ± 0.00052
```

**Analysis:**
```
Δk = 1.05432 - 0.98765 = 0.06667

σ_total = √(0.00045² + 0.00052²) = 0.00069

N_σ = 0.06667 / 0.00069 = 96.6 σ
```

**Conclusion:** Difference is HIGHLY SIGNIFICANT (>3σ)

**Reactivity Worth:**
```
ρ₁ = (k₁ - 1)/k₁ = 0.05154 = +5154 pcm
ρ₂ = (k₂ - 1)/k₂ = -0.01250 = -1250 pcm

Control rod worth: Δρ = 6404 pcm = $6.40 (if β_eff = 0.0065)
```

---

## Troubleshooting Poor Statistics

### Problem: Relative Error Too Large

**Symptom:** R > 0.1% or Check 2 fails

**Cause:** Insufficient nsrc × n_active

**Solution 1: Increase nsrc**
```
OLD: KCODE  10000  1.0  50  150
NEW: KCODE  30000  1.0  50  150  (3× nsrc → √3 = 1.73× better)
```

**Solution 2: Increase Active Cycles**
```
OLD: KCODE  10000  1.0  50  150  (100 active)
NEW: KCODE  10000  1.0  50  450  (400 active, 4× → 2× better)
```

**Solution 3: Combined**
```
OLD: KCODE  10000  1.0  50  150
NEW: KCODE  20000  1.0  50  350  (2× nsrc, 3× cycles → √6 = 2.45× better)
```

**Statistical Relationship:**
```
R ∝ 1/√(nsrc × n_active)
```

### Problem: VOV > 0.10

**Symptom:** Check 3 fails, variance unstable

**Cause:** Variance estimator hasn't converged (most common issue)

**Solution:** Increase active cycles significantly
```
OLD: KCODE  10000  1.0  50  150  (100 active)
NEW: KCODE  10000  1.0  50  450  (400 active)
```

**Rule of Thumb:** For VOV < 0.10, need ~300+ active cycles for most problems

### Problem: FOM Not Constant

**Symptom:** Check 4 fails, efficiency changing

**Cause:** Statistical behavior unstable over time

**Solutions:**
- Increase active cycles (same as VOV fix)
- Check for source convergence issues
- Verify geometry (no lost particles)

### Problem: TFC Bins 1-8 Fail

**Symptom:** Check 6 fails, early bins poor

**Cause:** Not enough total cycles to fill 10 bins adequately

**Solution:** Increase active cycles
```
OLD: KCODE  10000  1.0  50  100  (50 active, ~5 per bin)
NEW: KCODE  10000  1.0  50  350  (300 active, ~30 per bin)
```

**Rule:** Need ≥20 cycles per bin, so ≥200 active cycles minimum

---

## Zero or Invalid keff

### Problem 1: keff = 0.00000

**Cause:** No fissile material or no fissions occurring

**Check:**
```
M1  92238  1.0  $ Only U-238 (not fissile!)
```

**Fix:** Add fissile isotope
```
M1  92235  0.03  92238  0.97  $ Add U-235
```

### Problem 2: SDEF Card Present

**Cause:** SDEF conflicts with KCODE (fixed source vs criticality)

**Check:**
```
SDEF  POS=0 0 0  ERG=14.1  $ WRONG for criticality
KCODE  10000  1.0  50  150
```

**Fix:** Remove SDEF, use KSRC
```
c SDEF  POS=0 0 0  ERG=14.1  $ Delete this
KCODE  10000  1.0  50  150
KSRC  0 0 0
```

### Problem 3: NPS Card Present

**Cause:** NPS is for fixed-source, not criticality

**Check:**
```
NPS  1000000  $ WRONG for KCODE
KCODE  10000  1.0  50  150
```

**Fix:** Remove NPS
```
c NPS  1000000  $ Delete this line
KCODE  10000  1.0  50  150
```

### Problem 4: Geometry Errors

**Symptom:** Lost particles, keff unreliable

**Check Output:**
```
fatal error.  12 particles got lost
```

**Fix:** Use geometry plot to find overlaps/gaps
```
mcnp6 inp=input.i ip
```

### Problem 5: Extremely Subcritical

**Symptom:** keff << 1 (e.g., 0.12345)

**Causes:**
- Insufficient fissile material (too small, too dilute)
- Strong absorbers (control rods, poisons)
- High leakage (geometry too small, no reflector)

**Fix:** Check materials, geometry size, reflector presence

---

## Validation Checklist

Before accepting keff results:

### Source Convergence
- [ ] Entropy plot reviewed (see entropy_convergence_guide.md)
- [ ] Entropy plateaued before active cycles
- [ ] No entropy trends during active cycles

### Statistical Quality
- [ ] Relative error < target (0.1% for design, 0.01% for benchmark)
- [ ] All 10 statistical checks passed
- [ ] VOV < 0.10
- [ ] No trending in keff

### Physical Reasonableness
- [ ] keff value makes physical sense
- [ ] Three estimators (col/abs/trk) agree within 2σ
- [ ] No lost particles
- [ ] Geometry verified with plot

### Documentation
- [ ] KCODE parameters recorded
- [ ] Final keff ± uncertainty documented
- [ ] Statistical quality noted
- [ ] Any warnings addressed

---

## Advanced Topics

### Reactivity Definitions

**k-excess:**
```
k_excess = keff - 1
```

**Reactivity (absolute):**
```
ρ = (keff - 1) / keff
```

**Reactivity in pcm:**
```
ρ [pcm] = ρ × 10⁵
```

**Reactivity in dollars:**
```
ρ [$] = ρ / β_eff
```
Where β_eff = delayed neutron fraction (~0.0065 for U-235 thermal)

### Temperature Coefficient

**Method:** Calculate keff at different temperatures

**Example:**
```
Case 1 (Cold, 293K): keff₁ = 1.01234
Case 2 (Hot, 1400K): keff₂ = 0.99876

ρ₁ = (k₁-1)/k₁ = 0.01218
ρ₂ = (k₂-1)/k₂ = -0.00124

α_T = (ρ₂ - ρ₁) / (T₂ - T₁)
    = (-0.00124 - 0.01218) / (1400 - 293)
    = -1.21×10⁻⁵ K⁻¹
    = -1.21 pcm/K  (negative = safe)
```

### Sensitivity Analysis

**Perturbation Method:**
```
1. Run base case: keff₀
2. Perturb parameter by small amount (1%)
3. Run perturbed case: keff₁
4. Calculate sensitivity: S = (Δkeff/keff₀) / (Δp/p₀)
```

**Example: Density Sensitivity:**
```
Base: ρ = -18.7 g/cm³ → keff₀ = 1.00000
Pert: ρ = -18.887 g/cm³ (+1%) → keff₁ = 1.00234

S_ρ = (0.00234/1.00000) / (0.01) = 0.234

Interpretation: 1% increase in density → 0.234% increase in keff
```

---

## References

- **entropy_convergence_guide.md**: Shannon entropy, dominance ratio, source convergence
- **scripts/README.md**: Python tools for automated keff analysis
- **mcnp-statistics-checker**: General statistical validation (10 checks detail)
- **MCNP User Manual**: Chapter 5.8 (KCODE/KSRC), Appendix (statistical tests)

---

**END OF KCODE ANALYSIS GUIDE**
