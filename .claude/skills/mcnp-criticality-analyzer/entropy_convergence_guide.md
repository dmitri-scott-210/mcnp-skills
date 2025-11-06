# Entropy Convergence Guide

**Purpose:** Comprehensive guide to Shannon entropy, fission source convergence, dominance ratio, and troubleshooting convergence issues in KCODE calculations.

---

## Overview

Before keff statistics can be trusted, the fission source distribution must converge to the fundamental eigenmode. Shannon entropy is the primary metric MCNP uses to monitor source convergence.

**Critical Rule:** If source not converged, keff is meaningless!

---

## Shannon Entropy Fundamentals

### Definition

**Shannon Entropy (H)**: Quantifies spatial distribution of fission source

**Formula:**
```
H = -Σᵢ pᵢ log₂(pᵢ)
```

Where:
- pᵢ = fraction of fission source in mesh cell i
- Sum over all spatial mesh cells
- Units: bits (information theory)

### Physical Interpretation

**Low Entropy (H ~ 3-4):**
- Source concentrated in small region
- Few cells contain significant source
- Early cycles or poor initial guess

**High Entropy (H ~ 6-8):**
- Source spread throughout fissile regions
- Many cells contain source
- Equilibrium distribution reached

**Plateau:**
- Entropy stops changing
- Source distribution converged
- **Safe to start collecting keff statistics**

### Typical Entropy Behavior

```
Cycle    Entropy    Status
  1      4.5       Initial guess (localized)
  10     5.2       Source spreading
  20     5.6       Still spreading
  30     5.8       Near convergence
  40     5.9       Converging
  50     5.95      Plateau reached ← START ACTIVE CYCLES
  100    5.95      Stable (good)
  150    5.94      Stable (good)
  200    5.95      Converged ✓
```

---

## Entropy vs Cycle Analysis

### Reading the Output

Look for "source entropy" table in MCNP output:
```
    cycle     keff     entropy
        1    0.98234    5.2341
       10    1.00123    5.7832
       20    1.00456    5.9124
       30    1.00234    5.9456
       40    1.00321    5.9523
       50    1.00345    5.9534  ← Last inactive cycle (nskip=50)
       60    1.00338    5.9531  ← Active cycle 1
      100    1.00345    5.9533
      150    1.00344    5.9532  ← Final cycle
```

### Good Convergence Pattern

**Characteristics:**
- Entropy rises rapidly (cycles 1-30)
- Entropy plateaus (cycles 30-50)
- Entropy remains flat during active cycles (50-150)
- Small fluctuations (±0.02) acceptable

**Conclusion:** Source converged, nskip=50 appropriate ✓

### Poor Convergence Pattern

```
    cycle     keff     entropy
        1    0.95234    4.8341
       20    1.00456    5.6124
       40    1.01321    5.9123
       50    1.00845    5.9534  ← Last inactive (START ACTIVE)
       60    1.00538    5.9712  ← Still changing!
       80    1.00245    5.9891
      100    1.00165    5.9956  ← Still rising
      150    1.00145    5.9987  ← Never plateaued
```

**Characteristics:**
- Entropy continuously rising through active cycles
- keff trending downward (correlated)
- Source distribution still evolving

**Conclusion:** nskip=50 insufficient, active cycles contaminated

**Fix:** Increase nskip to 100-150

---

## Dominance Ratio

### Definition

**Dominance Ratio (DR)**: Ratio of 2nd to 1st eigenvalue

```
DR = λ₁ / λ₀
```

Where:
- λ₀ = fundamental eigenvalue (largest)
- λ₁ = first harmonic (second-largest)

### Physical Meaning

**Fission Source Evolution:**
```
S(n) = c₀φ₀ + c₁φ₁ + c₂φ₂ + ...
       ^fundamental  ^1st harmonic  ^higher modes
```

After n cycles:
```
S(n) ≈ c₀φ₀ + c₁(DR)ⁿφ₁
```

Higher modes decay as (DR)ⁿ

**Low DR (DR ~ 0.5):**
- Fast convergence
- 1st harmonic decays quickly
- (0.5)⁵⁰ = 8.9×10⁻¹⁶ (negligible after 50 cycles)

**High DR (DR ~ 0.95):**
- Slow convergence
- 1st harmonic persists
- (0.95)⁵⁰ = 0.077 (still 7.7% after 50 cycles!)
- (0.95)¹⁰⁰ = 0.006 (0.6% after 100 cycles)
- (0.95)⁵⁰⁰ ≈ 0 (negligible after 500 cycles)

### Impact on Convergence Time

| DR | Fast Convergence | Complete Convergence | Notes |
|----|------------------|---------------------|-------|
| 0.5 | 20 cycles | 50 cycles | Bare sphere, simple geometry |
| 0.7 | 50 cycles | 100 cycles | Typical PWR assembly |
| 0.85 | 100 cycles | 300 cycles | Large reactor core |
| 0.95 | 300 cycles | 1000 cycles | Loosely coupled systems |
| 0.98 | 500 cycles | 2000+ cycles | Very loosely coupled |

### Systems with High DR

**Characteristics:**
- Large systems with weak coupling
- Two separated fissile regions
- Thick reflectors
- Control rods partially inserted
- Startup configurations

**Symptoms:**
- Oscillating entropy
- Long-period oscillations (20-100 cycles)
- Slow keff convergence
- Large cycle-to-cycle variations

---

## Convergence Patterns and Diagnostics

### Pattern 1: Fast Convergence (Good)

**Symptoms:**
```
Cycle    Entropy    keff
  1      5.1       0.98234
  10     5.7       1.00234
  20     5.9       1.00345
  30     5.95      1.00342  ← Plateau reached
  50     5.95      1.00345  (last inactive)
  100    5.95      1.00344
  150    5.95      1.00345
```

**Characteristics:**
- Entropy plateaus quickly (by cycle 30)
- keff stable after cycle 30
- No oscillations
- Small fluctuations only

**Action:** nskip=50 is conservative and appropriate ✓

### Pattern 2: Continuous Rise (Poor Source Convergence)

**Symptoms:**
```
Cycle    Entropy    keff
  1      4.5       0.95234
  20     5.6       1.00456
  40     5.9       1.01321
  50     5.95      1.00845  (last inactive)
  60     5.97      1.00538  ← Still rising
  80     5.98      1.00245
  100    5.99      1.00165
  150    6.00      1.00145  ← Never plateaued
```

**Characteristics:**
- Entropy continuously rising
- keff trending downward (correlated with entropy)
- Active cycles contaminated

**Diagnosis:** nskip too small

**Fix:**
```
OLD: KCODE  10000  1.0  50  150
NEW: KCODE  10000  1.0  100  250  (increase nskip to 100)
```

### Pattern 3: Oscillation (High Dominance Ratio)

**Symptoms:**
```
Cycle    Entropy    keff
  50     5.95      1.00845  (last inactive)
  60     5.96      1.00938  ← Rising
  70     5.94      1.00638  ← Falling
  80     5.97      1.00838  ← Rising
  90     5.93      1.00538  ← Falling
  100    5.96      1.00745  ← Rising
  110    5.94      1.00645  ← Falling
  ...
  (continues for many cycles)
```

**Characteristics:**
- Long-period oscillation (10-50 cycles)
- Entropy and keff oscillate together
- Amplitude may decrease slowly
- May persist for hundreds of cycles

**Diagnosis:** High dominance ratio (DR ~ 0.90-0.98)

**Fix:** See "High Dominance Ratio Solutions" section below

### Pattern 4: Early Plateau Then Drift (Inadequate Inactive)

**Symptoms:**
```
Cycle    Entropy    keff
  20     5.9       1.00456
  30     5.92      1.00234
  40     5.92      1.00321  ← Appears converged
  50     5.92      1.00345  (last inactive)
  60     5.94      1.00338  ← Small drift
  100    5.96      1.00245
  150    5.98      1.00145  ← Slow trend
```

**Characteristics:**
- Entropy appears flat during inactive
- Slow upward drift during active
- Very high DR (2nd mode decaying extremely slowly)

**Diagnosis:** Appeared converged but wasn't (subtle case)

**Fix:** Much longer nskip (200-500 cycles)

---

## High Dominance Ratio Solutions

### Solution 1: Dramatically Increase Inactive Cycles

**Approach:** Let 2nd eigenmode decay to negligible level

**Formula:**
```
To reduce 2nd mode to 1%: n ~ log(0.01) / log(DR)
```

**Examples:**
- DR = 0.90: n ~ 44 cycles
- DR = 0.95: n ~ 90 cycles
- DR = 0.98: n ~ 229 cycles

**Implementation:**
```
OLD: KCODE  10000  1.0  50  150
NEW (DR~0.95): KCODE  10000  1.0  200  500
NEW (DR~0.98): KCODE  10000  1.0  500  1000
```

**Rule:** For high DR, use nskip = 3-5× the observed oscillation period

### Solution 2: Better Initial Source Guess

**Approach:** Start with source closer to fundamental mode

**Poor Initial Guess:**
```
KSRC  0 0 0  $ Single point (far from fundamental)
```

**Good Initial Guess:**
```
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0
     20 0 0  -20 0 0  0 20 0  0 -20 0
     10 10 0  -10 10 0  10 -10 0  -10 -10 0
     5 5 10  5 5 -10  -5 -5 10  -5 -5 -10
     ... (20-50 points spanning entire core)
```

**Guidelines:**
- Distribute points throughout all fissile regions
- More points for loosely coupled systems
- Cover axial and radial extent
- Include points near boundaries

**Effect:** Reduces amplitude of 2nd mode (smaller c₁ coefficient)

### Solution 3: Increase nsrc

**Approach:** Better sampling of spatial distribution each cycle

**Mechanism:**
- More neutrons → better statistics per cycle
- Better convergence of spatial moments
- Reduces Monte Carlo noise in eigenmodes

**Implementation:**
```
OLD: KCODE  10000  1.0  200  500
NEW: KCODE  50000  1.0  200  500  (5× neutrons/cycle)
```

**Effect:** Moderate improvement in convergence rate

### Solution 4: Modify Geometry (If Possible)

**Approach:** Reduce spatial decoupling

**Techniques:**
- Add coupling between separated regions
- Reduce reflector thickness (increase leakage)
- Adjust control rod positions
- Modify fuel loading pattern

**Effect:** Reduces dominance ratio at fundamental level

---

## Determining Adequate nskip

### Method 1: Visual Inspection

**Steps:**
1. Plot entropy vs cycle
2. Identify where plateau begins (cycle N)
3. Set nskip = N × 1.2 (20% safety margin)

**Example:**
```
Entropy plateaus at cycle 40
nskip = 40 × 1.2 = 48 ≈ 50 cycles
```

### Method 2: Conservative Rule

**Simple Rule:**
```
nskip = 2 × (observed convergence cycle)
```

**Example:**
```
Entropy stable by cycle 50
nskip = 2 × 50 = 100 cycles (conservative)
```

### Method 3: Problem-Dependent Guidelines

| Geometry Type | Typical nskip |
|---------------|---------------|
| Simple bare sphere | 20-30 |
| Reflected sphere | 30-50 |
| Single fuel assembly | 50-100 |
| Small reactor core | 100-200 |
| Large reactor core | 150-300 |
| Loosely coupled (DR>0.9) | 300-1000 |

**Rule:** When in doubt, use more inactive cycles

---

## Verification Tests

### Test 1: Repeat Run with Different nskip

**Method:**
```
Run 1: KCODE  10000  1.0   50  150
Run 2: KCODE  10000  1.0  100  200
Run 3: KCODE  10000  1.0  200  400
```

**Analysis:**
- Compare final keff values
- Should agree within 2σ if all converged
- If Run 1 differs from Runs 2-3: nskip=50 insufficient

### Test 2: Check Entropy Flatness

**Criteria for Converged:**
```
1. Entropy plateau reached before nskip
2. Entropy variation during active cycles < 0.05 (5%)
3. No systematic trend (rising/falling)
4. Oscillations (if any) < 0.02 amplitude
```

### Test 3: Correlation Test

**Check:** Are keff and entropy still correlated during active cycles?

**If YES:** Source not converged, increase nskip

**If NO:** Source likely converged ✓

---

## Common Mistakes

### Mistake 1: Trusting Keff When Entropy Not Flat

**Error:**
```
Entropy rising during active cycles
But user reports: "keff = 1.00345 ± 0.00087"
```

**Problem:** Active cycles contaminated, keff biased

**Fix:** Increase nskip until entropy flat

### Mistake 2: Insufficient nskip for Complex Geometry

**Error:**
```
Large loosely-coupled core
Using nskip=50 (typical for small problem)
```

**Problem:** Source takes 200+ cycles to converge

**Fix:** Scale nskip with problem complexity

### Mistake 3: Ignoring Oscillations

**Error:**
```
Entropy oscillates ±0.1
User: "Average entropy is constant, so converged"
```

**Problem:** Oscillation indicates 2nd mode present

**Fix:** Increase nskip to let oscillation decay

### Mistake 4: Starting Active Cycles Too Early

**Error:**
```
Entropy appears flat at cycle 40
Set nskip=40 (no safety margin)
```

**Problem:** Minor drifts not detected, no margin for error

**Fix:** Always add 20-50% safety margin to observed convergence

---

## Advanced Diagnostics

### Fission Matrix

**Purpose:** Diagnose spatial coupling between regions

**MCNP Input:**
```
FMESH:N  GEOM=XYZ  ORIGIN=-50 -50 -50
         IMESH=50  IINTS=5
         JMESH=50  JINTS=5
         KMESH=50  KINTS=5
         OUT=IJ  $ Output fission matrix
```

**Interpretation:**
- Diagonal elements: Self-coupling (fissions in region i from neutrons born in i)
- Off-diagonal: Inter-region coupling
- Weak off-diagonal → High DR → Slow convergence

### Cycle-by-Cycle keff Plot

**Method:** Plot all three estimators vs cycle

**Good Convergence:**
- All three estimators converge to same value
- Convergence by end of inactive cycles
- Stable during active cycles

**Poor Convergence:**
- Estimators disagree
- Trending during active cycles
- Large cycle-to-cycle scatter

### Running Average Test

**Method:** Plot running average of keff

**Formula:**
```
keff_avg(n) = (1/n) Σᵢ₌₁ⁿ keff(i)
```

**Good:** Running average plateaus during active cycles

**Poor:** Running average still changing (not converged)

---

## Summary: Entropy Convergence Checklist

Before trusting keff results:

### Visual Checks
- [ ] Entropy plot shows plateau before nskip
- [ ] Entropy remains flat during active cycles (variation < 5%)
- [ ] No long-period oscillations (or amplitude < 0.02)
- [ ] keff not correlated with entropy during active cycles

### Quantitative Checks
- [ ] nskip ≥ (convergence cycle) × 1.2
- [ ] Entropy variation during active < 0.05
- [ ] If oscillating: period identified and nskip > 5× period

### Verification
- [ ] Repeat run with 2× nskip gives same keff (within 2σ)
- [ ] Three keff estimators agree (within 2σ)
- [ ] No systematic trends in keff vs cycle

### Problem-Specific
- [ ] nskip appropriate for geometry type (see guidelines)
- [ ] High DR systems: nskip ≥ 200-500 cycles
- [ ] KSRC points distributed throughout core

---

## References

- **kcode_analysis_guide.md**: K-effective interpretation, statistical checks
- **scripts/README.md**: Python tools for entropy analysis
- **MCNP User Manual**: Chapter 5.8 (KCODE), Appendix (eigenvalue methods)

---

**END OF ENTROPY CONVERGENCE GUIDE**
