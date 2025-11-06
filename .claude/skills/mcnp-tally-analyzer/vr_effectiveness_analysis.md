# Variance Reduction Effectiveness Analysis

**Phase 3 Addition - VR Integration**

## Overview

Variance reduction (VR) techniques modify particle transport to improve tally statistics. This reference provides methods to analyze VR effectiveness, identify under-sampled regions, and measure FOM (Figure of Merit) improvements.

**Key Question:** Is my variance reduction actually working?

---

## Figure of Merit (FOM) Analysis

### Definition

$$\text{FOM} = \frac{1}{R^2 \times T}$$

Where:
- **R** = relative error (not %)
- **T** = computer time (minutes)

**Interpretation:**
- **FOM constant → VR is neutral** (neither helps nor hurts, just uses time)
- **FOM increasing → VR is effective** (improving statistics faster than using time)
- **FOM decreasing → VR is harmful** (making statistics worse!)

### Comparing Analog vs. VR

**Baseline FOM (analog):**
```
Analog run:
  R = 0.15 (15%)
  T = 120 minutes
  FOM_analog = 1/(0.15² × 120) = 37.0
```

**VR run:**
```
With cell importance:
  R = 0.05 (5%)
  T = 150 minutes
  FOM_vr = 1/(0.05² × 150) = 267.0

FOM improvement = 267.0 / 37.0 = 7.2×
```

**Assessment:** ✅ **Cell importance improved FOM by 7.2×** - very effective!

### FOM Improvement Expectations by VR Method

| VR Technique | Typical FOM Improvement | When to Use |
|--------------|-------------------------|-------------|
| Cell importance (IMP) | 5-50× | Simple geometry, <20 cells |
| Weight windows (WWN/WWE) | 10-100× | Complex geometry, deep penetration |
| Weight window generator (WWG) | 50-500× | Automatic WW from tallies |
| Exponential transform (EXT) | 100-1000× | Deep penetration (>15 MFP) |
| DXTRAN sphere | 20-200× | Point detectors in void |
| Combined (WWG + EXT) | 500-5000× | Extreme deep penetration |

**Warning:** If FOM improvement < 2×, VR is probably not worth the setup effort!

---

## Identifying Under-Sampled Regions

### Symptoms of Poor Sampling

**1. High Relative Error Despite Many Histories**
```
Problem:
  NPS = 1E8 (100 million)
  R = 0.25 (25% error)
  Expected: R ∝ 1/√N → Should be ~0.001 (0.1%)!

Diagnosis: Region is severely under-sampled
Solution: Add importance or weight windows to critical path
```

**2. Large Energy Bin Variations**
```
Energy Bin Results (F4 tally):
  0.0 - 1 eV:    R = 0.03 (3%) ✓ Well-sampled
  1 - 100 eV:    R = 0.08 (8%) ✓ Acceptable
  100 - 1 keV:   R = 0.35 (35%) ⚠ Under-sampled!
  1 keV - 1 MeV: R = 0.85 (85%) ✗ Severely under-sampled

Diagnosis: Fast neutrons not reaching tally region
Solution:
  - Add energy-dependent weight windows (WWE card)
  - Use WWG with WWGE energy structure
  - Consider source biasing toward high energies
```

**3. Spatial Flux Anomalies**
```
Radial Flux Profile (cells at increasing distance):
  r = 0-10 cm:   φ = 1.23E-3 ± 2%  ✓
  r = 10-20 cm:  φ = 5.47E-4 ± 5%  ✓
  r = 20-30 cm:  φ = 1.89E-4 ± 15% ⚠
  r = 30-40 cm:  φ = 2.14E-3 ± 75% ✗ WRONG! (should decrease!)

Diagnosis: Poor statistics create unphysical result (flux should decrease)
Solution: Increase importance in outer cells
```

### Under-Sampling Detection Algorithm

```python
def detect_undersampling(tally_data, threshold_error=0.20):
    """
    Identify under-sampled regions in tally results

    Args:
        tally_data: dict with 'values', 'errors', 'labels'
        threshold_error: relative error threshold (default 20%)

    Returns:
        under_sampled: list of bin indices with poor statistics
    """
    under_sampled = []

    for i, (value, error) in enumerate(zip(tally_data['values'],
                                            tally_data['errors'])):
        # Check 1: High relative error
        if error > threshold_error:
            under_sampled.append({
                'bin': i,
                'label': tally_data['labels'][i],
                'value': value,
                'error': error,
                'issue': f'High error: {error:.1%}'
            })
            continue

        # Check 2: Unphysical jumps (for spatial distributions)
        if i > 0:
            prev_value = tally_data['values'][i-1]
            ratio = value / prev_value if prev_value > 0 else 0

            # Flux shouldn't increase by >5× in adjacent bins
            if ratio > 5.0 and error > 0.15:
                under_sampled.append({
                    'bin': i,
                    'label': tally_data['labels'][i],
                    'value': value,
                    'error': error,
                    'issue': f'Unphysical jump: {ratio:.1f}× with {error:.1%} error'
                })

    return under_sampled
```

---

## VR Convergence Analysis

### WWG Iteration Monitoring

When using weight window generator (WWG) with iteration:

```
Iteration 1 (initial generation):
  FOM = 125
  R = 0.15 (15%)

Iteration 2 (refined WW):
  FOM = 347
  R = 0.08 (8%)
  Improvement: 2.8× (good progress)

Iteration 3 (converged WW):
  FOM = 382
  R = 0.07 (7%)
  Improvement: 1.1× (converged! <20% change)

Assessment: ✅ WWG converged after 3 iterations
Action: Use iteration 3 wwout for production run
```

**Convergence Criterion:** FOM change < 20% between iterations

### Importance Function Validation

**Weight Window Bounds Check:**
```python
def validate_ww_bounds(wwout_file):
    """Check weight window lower bounds for reasonableness"""
    ww_data = read_wwout(wwout_file)

    min_ww = min(ww_data['lower_bounds'])
    max_ww = max(ww_data['lower_bounds'])
    ratio = max_ww / min_ww

    if ratio > 1E6:
        return {
            'status': 'WARNING',
            'message': f'WW ratio {ratio:.1e} is very large (>1E6)',
            'recommendation': 'Consider coarser mesh or manual importance'
        }
    elif ratio > 1E4:
        return {
            'status': 'CAUTION',
            'message': f'WW ratio {ratio:.1e} is large',
            'recommendation': 'Monitor for overbiasing'
        }
    else:
        return {
            'status': 'GOOD',
            'message': f'WW ratio {ratio:.1e} is reasonable'
        }
```

---

## Tally-Specific VR Effectiveness

### Surface Current (F1) with Cell Importance

**Without VR (analog):**
```
F1:N 100                  $ Leakage through outer surface
Cell importances: all = 1
Result: 1.23E-06 ± 45%
FOM: 24
```

**With geometric importance:**
```
IMP:N 1 2 4 8 16 32 64 128 256 512 1024
F1:N 100                  $ Same surface
Result: 1.19E-06 ± 8%
FOM: 766
```

**Analysis:**
- **Value agreement:** 1.23E-06 vs 1.19E-06 = 3% difference ✓
- **Error reduction:** 45% → 8% = 5.6× improvement
- **FOM improvement:** 766/24 = 32× ✓ **Excellent!**
- **Assessment:** Cell importance very effective for leakage tallies

### Point Detector (F5) with DXTRAN

**Without DXTRAN:**
```
F5:N 100 0 0  0.5        $ Point detector at (100, 0, 0)
Result: 2.73E-08 ± 125%  (unreliable!)
FOM: 0.04
```

**With DXTRAN sphere:**
```
DXT:N 100 0 0  5 20      $ Inner radius 5 cm, outer 20 cm
F5:N 100 0 0  0.5
Result: 2.68E-08 ± 4.5%
FOM: 24.5
```

**Analysis:**
- **Value agreement:** Within combined uncertainty ✓
- **Error reduction:** 125% → 4.5% = 28× improvement
- **FOM improvement:** 24.5/0.04 = 613× ✓ **Spectacular!**
- **Assessment:** DXTRAN essential for point detectors in void

### Mesh Tally (FMESH) with WWG

**Without WWG:**
```
FMESH4:N  GEOM=XYZ
          ORIGIN= -100 -100 -100
          IMESH= 100  IINTS= 20
          JMESH= 100  JINTS= 20
          KMESH= 100  KINTS= 20

Average R across 8000 mesh bins: 35%
Bins with R > 50%: 1247 (15.6%)
FOM (worst bin): 2.1
```

**With WWG (mesh-based):**
```
MESH  [same as FMESH above]
WWGE:N  1E-10 1E-6 0.01 1 20
WWG  4  0  1.0              $ Generate from FMESH4

Average R across bins: 8%
Bins with R > 50%: 0 (0%)
FOM (worst bin): 78.3
```

**Analysis:**
- **Average error reduction:** 35% → 8% = 4.4× improvement
- **Worst bin FOM:** 78.3/2.1 = 37× improvement ✓
- **Coverage:** 100% of bins now reliable (0% > 50%)
- **Assessment:** WWG dramatically improves mesh tally uniformity

---

## VR-Induced Artifacts

### Overbiasing Symptoms

**Problem:** VR too aggressive → introduces bias

**Symptom 1: Mean Shifts Between VR Runs**
```
Analog:     φ = 1.23E-04 ± 15%
VR run 1:   φ = 1.19E-04 ± 5%  (within uncertainty ✓)
VR run 2:   φ = 0.87E-04 ± 4%  (outside 3σ! ✗)

Diagnosis: Second VR run has overbiasing
Solution: Reduce VR aggressiveness (wider WWP bounds)
```

**Symptom 2: Statistical Checks Fail Despite Low R**
```
R = 0.03 (3% - excellent!)
But: VOV = 0.45 (>0.10 limit ✗)
And: Slope = 15.2 (outside 3-10 range ✗)

Diagnosis: Low error from few high-weight particles (not CLT)
Solution: Check weight window bounds, may be too narrow
```

**Symptom 3: FOM Peaks Then Crashes**
```
Iteration 1: FOM = 150
Iteration 2: FOM = 520  (3.5× improvement ✓)
Iteration 3: FOM = 890  (1.7× improvement ✓)
Iteration 4: FOM = 215  (0.24× DECREASE! ✗)

Diagnosis: Iteration 4 over-optimized, created overbiasing
Solution: Use iteration 3 wwout, don't iterate further
```

### Weight Distribution Validation

```python
def check_weight_distribution(output_file, tally_num):
    """
    Validate particle weight distribution for a tally
    Healthy VR has moderate weight variation
    """
    weights = extract_tally_contributing_weights(output_file, tally_num)

    if not weights:
        return {'status': 'ERROR', 'message': 'No weight data'}

    w_max = max(weights)
    w_min = min(weights)
    w_avg = sum(weights) / len(weights)
    w_ratio = w_max / w_min

    # Check for dominance by few particles
    weights_sorted = sorted(weights, reverse=True)
    top_10_contrib = sum(weights_sorted[:10]) / sum(weights)

    issues = []

    if w_ratio > 1E6:
        issues.append(f'Extreme weight ratio: {w_ratio:.1e} (>1E6)')

    if top_10_contrib > 0.80:
        issues.append(f'Top 10 particles contribute {top_10_contrib:.0%} (>80%)')

    if len(weights) < 100:
        issues.append(f'Only {len(weights)} particles scored (need >100)')

    if issues:
        return {
            'status': 'WARNING',
            'issues': issues,
            'recommendation': 'Widen weight windows or reduce VR aggressiveness'
        }
    else:
        return {
            'status': 'GOOD',
            'weight_ratio': w_ratio,
            'top_10_fraction': top_10_contrib,
            'n_particles': len(weights)
        }
```

---

## VR Troubleshooting Guide

### Problem: VR Not Improving FOM

**Checklist:**
1. ✓ Is VR targeting the problem tally?
   - WWG card references correct tally number?
   - IMP values increase toward tally region?
2. ✓ Is geometry path clear?
   - No IMP:N=0 cells blocking path?
   - Importance increases monotonically?
3. ✓ Is source properly defined?
   - Source in high-importance region?
   - Source not artificially constrained?
4. ✓ Are WW bounds reasonable?
   - WWP wupn not too wide (default 5)?
   - WW ratio < 1E6 across phase space?

### Problem: VR Making Results Worse

**Likely causes:**
1. **Overbiasing** - WW too narrow, few particles dominate
   - Solution: WWP:N 10 3 5 0 -1 (widen wupn to 10)
2. **Wrong tally targeted** - WWG optimizing wrong tally
   - Solution: WWG should target most important tally
3. **Importance discontinuities** - Abrupt IMP jumps
   - Solution: Use geometric progression (1,2,4,8...) not (1,100)
4. **Energy structure mismatch** - WWGE bins don't match physics
   - Solution: Refine WWGE bins in problem energy range

### Problem: Some Tallies Good, Others Bad

**Diagnosis:**
- VR optimizes ONE tally at expense of others
- Common with WWG (targets single tally)

**Solutions:**
1. Use multiple WWG targets (if supported)
2. Prioritize most important tally
3. Use cell importance (benefits all tallies) instead of WWG
4. Run separate simulations for different tallies

---

## Best Practices for VR Validation

### 1. Always Compare to Analog (Even Small Test)

```bash
# Short analog run for baseline
mcnp6 inp=problem.i outp=analog.out tasks 4

# Short VR run
mcnp6 inp=problem_vr.i outp=vr.out tasks 4

# Compare: Do values agree within combined uncertainty?
# Compare: Is FOM_vr > 2 × FOM_analog?
```

### 2. Iterate WWG to Convergence

```
Don't stop at first WWG generation!
Iterate 2-5 times until FOM change < 20%
```

### 3. Monitor All 10 Statistical Checks

```
VR can give low R but fail other checks
Always verify 10/10 passed, especially VOV and slope
```

### 4. Check Particle Balance

```
For neutrons: source = absorption + leakage + (n,xn)
If balance error > 10%, importance causing losses
```

### 5. Validate Against Benchmarks

```
If available, compare VR results to:
- Experimental data
- Benchmark calculations
- Deterministic codes (MCNP → PARTISN)
```

---

## Integration with Other Skills

**After VR effectiveness analysis, recommend:**
- **mcnp-variance-reducer** - Improve VR setup based on findings
- **mcnp-ww-optimizer** - Refine weight windows iteratively
- **mcnp-statistics-checker** - Comprehensive statistical validation
- **mcnp-output-parser** - Extract weight distribution data

---

## Quick Reference: VR Effectiveness Metrics

| Metric | Good | Marginal | Poor |
|--------|------|----------|------|
| **FOM improvement** | >10× | 2-10× | <2× |
| **Error reduction** | >5× | 2-5× | <2× |
| **Value agreement** | <2σ | 2-3σ | >3σ |
| **Iteration convergence** | 2-4 iters | 5-7 iters | >7 or oscillating |
| **10 checks passed** | 10/10 | 7-9/10 | <7/10 |
| **Weight ratio** | <1E4 | 1E4-1E6 | >1E6 |
| **FOM stability** | ±5% | ±10% | >±20% |

**Goal:** All metrics in "Good" column → VR is effective and reliable!

---

## References

**Variance Reduction Theory:**
- ../mcnp-variance-reducer/variance_reduction_theory.md - FOM fundamentals
- ../mcnp-variance-reducer/advanced_vr_theory.md - WWG algorithm, optimization

**Statistical Validation:**
- ../mcnp-statistics-checker/SKILL.md - 10 statistical checks
- ../mcnp-statistics-checker/vr_quality_metrics.md - VR-specific metrics

**MCNP Manual:**
- §3.4.2.4 - Ten statistical checks
- §2.7.2.12 - Weight window generator
- §3.4.3 - Production run checks
