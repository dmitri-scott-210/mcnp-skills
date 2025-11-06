# Tally Analysis Examples with Variance Reduction

**Phase 3 Addition - VR Integration Examples**

## Overview

This directory contains example outputs demonstrating tally analysis with and without variance reduction. Use these to understand how VR affects tally behavior, convergence, and statistical quality.

---

## Example Comparisons

### analog_vs_vr_comparison.txt

**Scenario:** Concrete shield with F4 flux tally on far side

**Analog run:**
```
F4:N Result: 2.73E-06 ± 45%
FOM: 24.5
10 checks: 4/10 passed
Time: 120 minutes
```

**With cell importance:**
```
F4:N Result: 2.68E-06 ± 8%
FOM: 766
10 checks: 10/10 passed
Time: 150 minutes
FOM improvement: 31×
```

**Key observations:**
- **Value agreement:** Within combined uncertainty ✓
- **Error reduction:** 45% → 8% = 5.6× improvement
- **Statistical quality:** 4/10 → 10/10 checks passed
- **Time cost:** 25% more time, but 31× better FOM
- **Conclusion:** Cell importance very effective for this problem

---

### wwg_iteration_convergence.txt

**Scenario:** Tracking WWG convergence over 4 iterations

```
Iteration 1 (generation):
  FOM = 125
  R = 15%
  Baseline from analog

Iteration 2 (refinement):
  FOM = 347 (2.8× improvement)
  R = 8%
  Good progress

Iteration 3 (further refinement):
  FOM = 382 (1.1× improvement)
  R = 7%
  Converged (<20% FOM change)

Iteration 4 (over-iteration):
  FOM = 215 (0.56× DECREASE!)
  R = 9%
  Overbiasing - don't use!
```

**Lesson:** WWG converged at iteration 3. Iteration 4 shows overbiasing. **Use iteration 3 for production.**

**Convergence criterion:** Stop when FOM change < 20% between iterations

---

### point_detector_dxtran.txt

**Scenario:** F5 point detector in void region

**Without DXTRAN:**
```
F5:N Result: 2.73E-08 ± 250%
FOM: 0.08
Scores: 3 particles out of 1E6 histories
Assessment: Essentially no information
```

**With DXTRAN sphere:**
```
DXT:N 100 0 0  5 20    $ Inner 5 cm, outer 20 cm
F5:N Result: 2.68E-08 ± 4.5%
FOM: 24.5
Scores: 15,234 particles
Assessment: Excellent statistics
FOM improvement: 306×
```

**Lesson:** DXTRAN is **essential** for point detectors in void/low-importance regions. Without it, F5 tallies are essentially unusable.

---

### energy_spectrum_wwge.txt

**Scenario:** F4 tally with energy bins, using WWGE to improve energy-dependent sampling

**Without WWGE (uniform WW):**
```
Energy Bins:
  0.0 - 1 eV:    R = 3%  ✓
  1 - 100 eV:    R = 8%  ✓
  100 - 1 keV:   R = 35% ⚠
  1 keV - 1 MeV: R = 85% ✗

Average R: 32%
Problem: Fast neutrons under-sampled
```

**With WWGE (energy-dependent WW):**
```
WWGE:N  1e-10  1e-6  1e-3  0.1  1  20
        (fine structure in problem range)

Energy Bins:
  0.0 - 1 eV:    R = 3%  ✓
  1 - 100 eV:    R = 7%  ✓
  100 - 1 keV:   R = 9%  ✓
  1 keV - 1 MeV: R = 12% ✓

Average R: 7.8%
FOM improvement (high-E bins): 56×
```

**Lesson:** Use WWGE when energy spectrum analysis shows highly variable errors across energy ranges.

---

### mesh_tally_wwg.txt

**Scenario:** FMESH4:N spatial distribution with mesh-based WWG

**Without WWG:**
```
Mesh: 20×20×20 = 8000 bins
Average R: 35%
Bins with R > 50%: 1247 (15.6%)
Worst bin R: 127%
FOM (worst): 2.1
```

**With mesh-based WWG:**
```
MESH GEOM=XYZ [matches FMESH]
WWG 4 0 1.0

Average R: 8%
Bins with R > 50%: 0 (0%)
Worst bin R: 18%
FOM (worst): 78.3
FOM improvement: 37×
```

**Lesson:** Mesh-based WWG dramatically improves uniformity across spatial bins. All bins now have reliable statistics.

---

### deep_penetration_ext.txt

**Scenario:** Gamma shielding (20 cm lead, ~18 MFP)

**WWG alone:**
```
F2:P (far surface)
Result: 1.23E-07 ± 35%
FOM: 41
Time: 240 minutes
Problem: Deep penetration, WWG alone insufficient
```

**WWG + Exponential Transform:**
```
EXT:P 0.90  [cells]
VECT  0 0 1  (toward detector)
WWG 2 0 1.0

Result: 1.19E-07 ± 3.5%
FOM: 4080
Time: 250 minutes
FOM improvement: 100×
```

**Lesson:** For deep penetration (>15 MFP), **combine EXT + WWG**. EXT provides directional biasing, WWG controls weights. Together they're synergistic.

---

## Common VR Patterns in Output

### Pattern 1: Successful VR

**Indicators:**
- FOM improvement >10×
- All 10 statistical checks pass
- Value agrees with analog (within 2σ)
- Error reduced by >5×
- VOV < 0.10
- Weight ratio < 1E4

**Example:** analog_vs_vr_comparison.txt

---

### Pattern 2: Overbiasing

**Indicators:**
- VOV > 0.10 despite low R
- Few particles dominate tally (top 10 > 80%)
- Statistical checks fail (especially slope, VOV)
- FOM decreasing in later iterations
- Weight ratio > 1E6

**Example:** wwg_iteration_convergence.txt (iteration 4)

**Fix:** Widen weight windows (WWP wupn=10), reduce EXT parameter

---

### Pattern 3: Under-Optimization

**Indicators:**
- FOM still increasing significantly (>20% per iteration)
- Some energy/spatial bins still high R
- Uneven error distribution
- WWG not converged

**Example:** Early WWG iterations

**Fix:** Continue iterating WWG until FOM change < 20%

---

## Using These Examples

### For Learning

1. **Compare analog vs VR outputs** - See how VR changes tally behavior
2. **Study convergence patterns** - Understand what good/bad convergence looks like
3. **Identify VR artifacts** - Recognize overbiasing symptoms

### For Validation

1. **Check your results match expected patterns**
2. **Compare FOM improvements to typical values**
3. **Verify statistical quality consistent with examples**

### For Troubleshooting

1. **Match your problem to similar example**
2. **Check if VR effectiveness is comparable**
3. **If underperforming, review VR setup**

---

## Integration with Documentation

**See also:**
- ../vr_effectiveness_analysis.md - Detailed VR analysis methods
- ../convergence_diagnostics.md - Convergence validation techniques
- ../tally_vr_optimization.md - VR selection and tuning

**Related variance reduction examples:**
- ../../mcnp-variance-reducer/example_inputs/ - Full VR problem setups
- ../../mcnp-ww-optimizer/example_inputs/ - WWG iteration templates

---

## Quick Reference: Example → Lesson Learned

| Example File | Key Lesson | FOM Improvement |
|--------------|------------|-----------------|
| analog_vs_vr_comparison.txt | Cell IMP very effective for simple geometry | 31× |
| wwg_iteration_convergence.txt | Stop iterating when FOM change <20% | 3× over analog |
| point_detector_dxtran.txt | DXTRAN essential for F5 in void | 306× |
| energy_spectrum_wwge.txt | Use WWGE for energy-dependent issues | 56× (high-E bins) |
| mesh_tally_wwg.txt | Mesh-based WWG for spatial uniformity | 37× |
| deep_penetration_ext.txt | Combine EXT + WWG for >15 MFP | 100× |

**General conclusion:** Proper VR selection and tuning typically yields 10-500× FOM improvements with validated results.
