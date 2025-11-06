# Statistical Quality Examples with VR

**Phase 3 Addition - VR Statistical Validation Examples**

## Overview

Examples demonstrating statistical quality checks with variance reduction, showing how VR affects the 10 statistical checks and VR-specific quality metrics.

---

## Example 1: Excellent VR Quality

```
TALLY 4 (F4:N):
╔═══════════════════════════════════╗
║  STATISTICAL QUALITY: EXCELLENT   ║
╠═══════════════════════════════════╣
║ Standard 10 Checks:         10/10 ║
║ Relative Error:              3.2% ║
║ VOV:                        0.045 ║
║ FOM:                         1234 ║
║ Slope:                        4.2 ║
╠═══════════════════════════════════╣
║ VR-Specific Metrics:              ║
║ FOM Stability:               ±5%  ║
║ Weight Ratio:              2.3E3  ║
║ Top 10 Contribution:          32% ║
║ Mean vs Analog:          0.8σ ✓  ║
║ WWG Converged:              YES   ║
╠═══════════════════════════════════╣
║ VR Quality Score:         95/100  ║
║ Assessment:         TRUST RESULTS ║
╚═══════════════════════════════════╝

VR Method: WWG mesh-based (3 iterations)
FOM Improvement over Analog: 87×
```

**Key Observations:**
- All standard checks pass
- All VR metrics in "Good" range
- Weight distribution healthy
- FOM stable and significantly improved
- **Conclusion: VR is effective and unbiased ✓**

---

## Example 2: Overbiasing (Poor VR)

```
TALLY 14 (F4:N):
╔═══════════════════════════════════╗
║  STATISTICAL QUALITY: POOR        ║
╠═══════════════════════════════════╣
║ Standard 10 Checks:          7/10 ║
║ Relative Error:              2.8% ║ ✗ Low R but...
║ VOV:                        0.342 ║ ✗ FAIL (>0.10)
║ FOM:                          523 ║
║ Slope:                       14.8 ║ ✗ FAIL (>10)
╠═══════════════════════════════════╣
║ VR-Specific Metrics:              ║
║ FOM Stability:              ±35%  ║ ✗ FAIL
║ Weight Ratio:              4.7E7  ║ ✗ FAIL (>1E6)
║ Top 10 Contribution:          89% ║ ✗ FAIL (>80%)
║ Mean vs Analog:          4.2σ ✗  ║ ✗ FAIL
║ WWG Converged:               NO   ║
╠═══════════════════════════════════╣
║ VR Quality Score:         32/100  ║
║ Assessment:      DO NOT TRUST ✗   ║
╚═══════════════════════════════════╝

VR Method: WWG + EXT (p=0.95, too aggressive)
Problem: 10 particles contribute 89% of tally
```

**Key Observations:**
- Low relative error is **MISLEADING**
- VOV, slope, and FOM stability all fail
- Extreme weight ratio (47 million!)
- Few particles dominate (overbiasing)
- Mean disagrees with analog
- **Conclusion: VR is biased, results invalid ✗**

**Fix:**
1. Reduce EXT parameter: p = 0.95 → 0.75
2. Widen weight windows: WWP wupn = 10
3. Iterate WWG more times

---

## Example 3: WWG Iteration Convergence

**Iteration 1 (Initial Generation):**
```
10 Checks: 6/10
R: 15%
VOV: 0.085
FOM: 125
Weight ratio: 8.2E3
Status: MARGINAL - Initial WWG generation
```

**Iteration 2 (Refinement):**
```
10 Checks: 9/10
R: 8%
VOV: 0.052
FOM: 347 (2.8× improvement)
Weight ratio: 3.1E3
Status: GOOD - Converging
```

**Iteration 3 (Further Refinement):**
```
10 Checks: 10/10
R: 7%
VOV: 0.041
FOM: 382 (1.1× over iter 2)
Weight ratio: 2.4E3
Status: EXCELLENT - CONVERGED (<20% FOM change)
```

**Iteration 4 (Over-iteration):**
```
10 Checks: 7/10
R: 9%
VOV: 0.187
FOM: 215 (0.56× DECREASE!)
Weight ratio: 1.8E5
Status: POOR - Overbiasing, don't use!
```

**Lesson:** Stop at iteration 3 when FOM change < 20%. Iteration 4 shows overbiasing.

---

## Example 4: Energy-Dependent Quality

**Without WWGE (uniform WW):**
```
Energy Range     R      VOV   FOM   Status
0.0 - 1 eV      3%    0.032  1250  ✓ Good
1 - 100 eV      8%    0.067   780  ✓ Good
100 - 1 keV    35%    0.287    42  ✗ Poor
1 keV - 1 MeV  85%    0.645     7  ✗ Very Poor

Problem: Fast neutrons under-sampled
```

**With WWGE (energy-dependent WW):**
```
WWGE:N  1e-10  1e-6  1e-3  0.1  1  20

Energy Range     R      VOV   FOM   Status
0.0 - 1 eV      3%    0.031  1245  ✓ Good
1 - 100 eV      7%    0.054   850  ✓ Good
100 - 1 keV     9%    0.048   612  ✓ Good (was 35%!)
1 keV - 1 MeV  12%    0.082   347  ✓ Good (was 85%!)

Improvement: All energy bins now reliable
```

**Lesson:** Use WWGE when statistical quality varies significantly across energy ranges.

---

## Example 5: Comparing VR to Analog

**Analog (Short Run):**
```
NPS: 1E6
Result: 2.73E-04 ± 15%
FOM: 37
Time: 120 min
10 Checks: 7/10 (marginal)
```

**VR (Same Time):**
```
NPS: 8E5 (fewer histories, but weighted)
Result: 2.68E-04 ± 3.5%
FOM: 766
Time: 120 min
10 Checks: 10/10
Weight ratio: 1.2E3
VR Quality Score: 92/100
```

**Statistical Comparison:**
```
Difference: |2.73E-04 - 2.68E-04| = 5E-06
Combined σ: sqrt((2.73E-04 × 0.15)² + (2.68E-04 × 0.035)²) = 4.1E-05
z-score: 5E-06 / 4.1E-05 = 0.12σ

Result: Values agree within 0.12σ (< 2σ threshold) ✓
Conclusion: VR is unbiased
```

**FOM Comparison:**
```
FOM_VR / FOM_analog = 766 / 37 = 21×
Same time, 21× better efficiency!
```

---

## VR Quality Indicators Summary

| Indicator | Good | Marginal | Poor | Critical Action |
|-----------|------|----------|------|-----------------|
| **10 checks** | 10/10 | 7-9/10 | <7/10 | Fix VR if <7/10 |
| **VOV** | <0.05 | 0.05-0.10 | >0.10 | Widen WWP if >0.10 |
| **FOM stability** | <±10% | ±10-20% | >±20% | Iterate more or fix VR |
| **Weight ratio** | <1E4 | 1E4-1E6 | >1E6 | Widen WWP immediately |
| **Top 10 contrib** | <50% | 50-80% | >80% | Add importance |
| **Mean vs analog** | <2σ | 2-3σ | >3σ | Review VR for bias |
| **WWG FOM change** | <20% | 20-40% | >40% or negative | Converge or use previous iter |

---

## Using These Examples

### For Validation
1. **Compare your statistics to examples**
2. **Identify which pattern matches your results**
3. **Apply appropriate fixes if needed**

### For Troubleshooting
1. **Example 2** → Recognize overbiasing symptoms
2. **Example 3** → Track WWG convergence properly
3. **Example 4** → Handle energy-dependent issues
4. **Example 5** → Validate VR against analog

### For Quality Assurance
- **Example 1:** Target quality level
- Aim for all metrics in "Good" column
- VR Quality Score > 85/100

---

## Quick Diagnostic Guide

**Symptom:** Low R but checks fail
→ **Example 2** (overbiasing)
→ **Fix:** Widen WWP, reduce EXT parameter

**Symptom:** FOM oscillating
→ **Example 3** iteration 4 (over-iteration)
→ **Fix:** Use previous iteration wwout

**Symptom:** Energy bins highly variable
→ **Example 4** (no WWGE)
→ **Fix:** Add WWGE with refined energy structure

**Symptom:** Unsure if VR biased
→ **Example 5** (analog comparison)
→ **Fix:** Run short analog, compare with z-test

---

## Integration

**See also:**
- ../vr_quality_metrics.md - Detailed VR metrics definitions
- ../advanced_convergence_theory.md - Statistical theory
- ../../mcnp-tally-analyzer/example_inputs/ - Tally-focused VR examples

**Related Skills:**
- mcnp-variance-reducer - Implement VR fixes
- mcnp-ww-optimizer - Refine weight windows
- mcnp-tally-analyzer - Analyze VR effectiveness from tally perspective
