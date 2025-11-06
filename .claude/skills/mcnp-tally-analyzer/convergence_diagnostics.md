# Convergence Diagnostics for Tally Analysis

**Phase 3 Addition - Advanced Convergence Theory**

## Overview

This reference provides advanced convergence diagnostic techniques based on Monte Carlo statistical theory (from MCNP Theory Manual §2.7). Use these methods to diagnose convergence issues, predict required histories, and validate Central Limit Theorem compliance.

**Key Questions:**
- Is my tally converging properly?
- How many more histories do I need?
- Is the Central Limit Theorem applicable?

---

## Central Limit Theorem (CLT) Requirements

### Theory (§2.7.1.2)

The CLT states that the sample mean approaches a normal distribution as N → ∞:

$$\bar{x} \sim \mathcal{N}\left(\mu, \frac{\sigma^2}{N}\right)$$

**Required conditions:**
1. **Independent samples** - Each history independent
2. **Identically distributed** - Same underlying distribution
3. **Finite variance** - σ² < ∞
4. **Large N** - Typically N > 30 for reasonable approximation

**MCNP implications:**
- Relative error R should decrease as ~1/√N
- FOM should remain constant
- Tally mean should stabilize
- Histogram should approach bell curve

### CLT Validation Procedure

```python
def validate_clt_compliance(history_data):
    """
    Check if tally behavior consistent with CLT

    Args:
        history_data: dict with 'nps', 'means', 'errors', 'fom'

    Returns:
        clt_status: dict with compliance assessment
    """
    import numpy as np

    nps = np.array(history_data['nps'])
    means = np.array(history_data['means'])
    errors = np.array(history_data['errors'])
    fom = np.array(history_data['fom'])

    issues = []

    # Test 1: Error should decrease as 1/√N
    # ln(R) = constant - 0.5×ln(N)
    log_nps = np.log(nps)
    log_errors = np.log(errors)
    fit = np.polyfit(log_nps, log_errors, 1)
    slope = fit[0]

    if abs(slope + 0.5) > 0.15:  # Should be -0.5 ± 0.15
        issues.append({
            'test': 'Error trend',
            'expected': -0.5,
            'observed': slope,
            'status': 'FAIL',
            'implication': 'Error not decreasing as 1/√N → Non-CLT behavior'
        })
    else:
        issues.append({
            'test': 'Error trend',
            'expected': -0.5,
            'observed': slope,
            'status': 'PASS'
        })

    # Test 2: FOM should be constant (±10%)
    fom_mean = np.mean(fom[len(fom)//2:])  # Last half
    fom_std = np.std(fom[len(fom)//2:])
    fom_variation = fom_std / fom_mean if fom_mean > 0 else 999

    if fom_variation > 0.10:
        issues.append({
            'test': 'FOM stability',
            'expected': '<10% variation',
            'observed': f'{fom_variation:.1%}',
            'status': 'FAIL',
            'implication': 'FOM not constant → Biasing or sampling issues'
        })
    else:
        issues.append({
            'test': 'FOM stability',
            'expected': '<10% variation',
            'observed': f'{fom_variation:.1%}',
            'status': 'PASS'
        })

    # Test 3: Mean should stabilize (last 50% has small variation)
    means_last_half = means[len(means)//2:]
    mean_final = means[-1]
    mean_variation = np.std(means_last_half) / abs(mean_final) if mean_final != 0 else 999

    if mean_variation > 0.05:  # >5% variation in last half
        issues.append({
            'test': 'Mean stability',
            'expected': '<5% variation in last half',
            'observed': f'{mean_variation:.1%}',
            'status': 'FAIL',
            'implication': 'Mean still drifting → Not converged'
        })
    else:
        issues.append({
            'test': 'Mean stability',
            'expected': '<5% variation',
            'observed': f'{mean_variation:.1%}',
            'status': 'PASS'
        })

    # Overall assessment
    n_passed = sum(1 for issue in issues if issue['status'] == 'PASS')
    n_total = len(issues)

    if n_passed == n_total:
        overall_status = 'CLT_COMPLIANT'
        recommendation = 'Convergence behavior is normal. Continue to target R.'
    elif n_passed >= n_total - 1:
        overall_status = 'CLT_MARGINAL'
        recommendation = 'Minor issues detected. Monitor convergence closely.'
    else:
        overall_status = 'CLT_VIOLATION'
        recommendation = 'Serious convergence issues. Review variance reduction setup.'

    return {
        'status': overall_status,
        'tests': issues,
        'passed': f'{n_passed}/{n_total}',
        'recommendation': recommendation
    }
```

**Example Output:**
```
CLT COMPLIANCE ASSESSMENT

Test 1: Error trend
  Expected: -0.5 (R ∝ N^-0.5)
  Observed: -0.48
  Status: ✓ PASS

Test 2: FOM stability
  Expected: <10% variation
  Observed: 6.3%
  Status: ✓ PASS

Test 3: Mean stability
  Expected: <5% variation in last half
  Observed: 2.1%
  Status: ✓ PASS

Overall: CLT_COMPLIANT (3/3 tests passed)
Recommendation: Convergence behavior is normal. Continue to target R.
```

---

## Convergence Trend Analysis

### History-by-History Behavior

**Ideal convergence (CLT-compliant):**
```
NPS        Mean           Error      FOM
1.0E4      2.45E-04       0.350      8.2
5.0E4      2.31E-04       0.155      20.8
1.0E5      2.28E-04       0.110      20.5
5.0E5      2.27E-04       0.049      21.3
1.0E6      2.27E-04       0.035      20.8

Observations:
  ✓ Mean stabilized by 1E5 histories
  ✓ Error decreasing as 1/√N
  ✓ FOM constant (~21)
  → GOOD CONVERGENCE
```

**Problematic convergence:**
```
NPS        Mean           Error      FOM
1.0E4      2.45E-04       0.450      4.9
5.0E4      1.89E-04       0.320      4.9
1.0E5      3.12E-04       0.285      6.1
5.0E5      2.71E-04       0.210      11.4
1.0E6      2.55E-04       0.195      13.2

Observations:
  ✗ Mean oscillating (not stable)
  ⚠ FOM increasing (not constant)
  ✗ Error not following 1/√N
  → POOR CONVERGENCE - Check VR setup!
```

### Autocorrelation Detection

**Theory:** Sequential tallies should be uncorrelated. Correlation indicates:
- Batch effects
- Source biasing issues
- VR creating particle "families"

```python
def check_autocorrelation(tally_sequence):
    """
    Detect autocorrelation in tally scores

    Strong autocorrelation suggests non-independent samples
    """
    import numpy as np

    scores = np.array(tally_sequence)
    n = len(scores)

    # Lag-1 autocorrelation
    mean_score = np.mean(scores)
    numerator = np.sum((scores[:-1] - mean_score) * (scores[1:] - mean_score))
    denominator = np.sum((scores - mean_score)**2)

    autocorr = numerator / denominator if denominator > 0 else 0

    if abs(autocorr) < 0.10:
        status = 'GOOD'
        message = f'Low autocorrelation ({autocorr:.3f}) → Independent samples'
    elif abs(autocorr) < 0.30:
        status = 'CAUTION'
        message = f'Moderate autocorrelation ({autocorr:.3f}) → Check batching'
    else:
        status = 'WARNING'
        message = f'High autocorrelation ({autocorr:.3f}) → Samples not independent!'

    return {
        'autocorr': autocorr,
        'status': status,
        'message': message,
        'recommendation': 'Use larger batch sizes' if status != 'GOOD' else 'No action needed'
    }
```

---

## Required Histories Prediction

### Method 1: Extrapolation from Current R

**Formula:**
$$N_{\text{target}} = N_{\text{current}} \times \left(\frac{R_{\text{current}}}{R_{\text{target}}}\right)^2$$

**Example:**
```python
def predict_required_histories(current_nps, current_R, target_R):
    """
    Estimate histories needed to achieve target relative error

    Assumes CLT holds: R ∝ 1/√N
    """
    required_nps = current_nps * (current_R / target_R)**2

    return {
        'current_nps': current_nps,
        'current_R': current_R,
        'target_R': target_R,
        'required_nps': required_nps,
        'additional_nps': required_nps - current_nps,
        'multiplier': required_nps / current_nps
    }

# Example usage:
result = predict_required_histories(
    current_nps=1e6,
    current_R=0.15,
    target_R=0.05
)

print(f"Current: {result['current_nps']:.1e} histories → R = {result['current_R']:.1%}")
print(f"Target:  {result['target_R']:.1%} error")
print(f"Need:    {result['required_nps']:.1e} histories (×{result['multiplier']:.1f})")
print(f"Additional: {result['additional_nps']:.1e} histories")
```

**Output:**
```
Current: 1.0e+06 histories → R = 15.0%
Target:  5.0% error
Need:    9.0e+06 histories (×9.0)
Additional: 8.0e+06 histories
```

### Method 2: FOM-Based Estimation

**Formula:**
$$T_{\text{target}} = \frac{1}{\text{FOM} \times R_{\text{target}}^2}$$

**Example:**
```python
def estimate_time_to_target(current_fom, target_R):
    """
    Estimate computer time needed for target error

    Args:
        current_fom: Figure of merit from current run
        target_R: Desired relative error (not %)

    Returns:
        time_minutes: Estimated time in minutes
    """
    time_minutes = 1 / (current_fom * target_R**2)

    return {
        'fom': current_fom,
        'target_R': target_R,
        'time_minutes': time_minutes,
        'time_hours': time_minutes / 60,
        'time_days': time_minutes / 1440
    }

# Example:
result = estimate_time_to_target(current_fom=21.3, target_R=0.05)

print(f"FOM = {result['fom']:.1f}")
print(f"Target R = {result['target_R']:.1%}")
print(f"Estimated time: {result['time_minutes']:.1f} min")
print(f"             = {result['time_hours']:.2f} hours")
print(f"             = {result['time_days']:.3f} days")
```

**Output:**
```
FOM = 21.3
Target R = 5.0%
Estimated time: 18.8 min
             = 0.31 hours
             = 0.013 days
```

---

## Non-Convergence Diagnosis

### Problem: Mean Drifting

**Symptoms:**
- Mean changes >5% in last 50% of run
- Mean oscillates without stabilizing
- Check 1 (mean stability) fails

**Diagnosis:**
```python
def diagnose_mean_drift(history_means):
    """
    Analyze mean behavior to identify drift causes
    """
    import numpy as np

    # Split into quarters
    n = len(history_means)
    q1_mean = np.mean(history_means[:n//4])
    q2_mean = np.mean(history_means[n//4:n//2])
    q3_mean = np.mean(history_means[n//2:3*n//4])
    q4_mean = np.mean(history_means[3*n//4:])

    # Check for monotonic drift
    quarters = [q1_mean, q2_mean, q3_mean, q4_mean]
    is_increasing = all(quarters[i] < quarters[i+1] for i in range(3))
    is_decreasing = all(quarters[i] > quarters[i+1] for i in range(3))

    if is_increasing:
        return {
            'pattern': 'MONOTONIC_INCREASE',
            'likely_cause': 'Insufficient burn-in for source convergence (KCODE) or biased sampling',
            'recommendation': 'For KCODE: Increase KSRC, check entropy. For fixed-source: Review VR setup.'
        }
    elif is_decreasing:
        return {
            'pattern': 'MONOTONIC_DECREASE',
            'likely_cause': 'Source particles exhausting high-importance regions',
            'recommendation': 'Check importance values, may be too high near source'
        }
    else:
        # Calculate drift magnitude
        drift = abs(q4_mean - q1_mean) / abs(q1_mean) if q1_mean != 0 else 999

        return {
            'pattern': 'OSCILLATING',
            'drift_magnitude': drift,
            'likely_cause': 'Insufficient statistics or improper weight windows',
            'recommendation': 'Increase NPS or widen weight window bounds (WWP wupn)'
        }
```

### Problem: Error Not Decreasing as 1/√N

**Symptoms:**
- R decreases slower than expected
- Error trend slope ≠ -0.5
- FOM decreasing

**Diagnosis:**

**Case 1: Slope > -0.5 (error decreasing too slowly)**
```
Observed slope: -0.35 (should be -0.5)

Likely causes:
  1. Few high-weight particles dominating
  2. Under-sampling in critical regions
  3. Weight windows too narrow

Solutions:
  1. Widen weight windows: WWP:N 10 3 5 0 -1
  2. Add importance to under-sampled regions
  3. Check weight distribution (top 10 particles < 50% contribution)
```

**Case 2: Slope < -0.5 (error decreasing too quickly)**
```
Observed slope: -0.65 (should be -0.5)

Likely causes:
  1. Batch correlation (not independent samples)
  2. Systematic bias being "burned off"
  3. Source convergence (KCODE problems)

Solutions:
  1. Increase batch size
  2. For KCODE: Increase skip cycles
  3. Check autocorrelation
```

### Problem: FOM Not Constant

**Symptoms:**
- FOM varies > ±10% in last half
- FOM steadily increasing or decreasing
- Check 4 (FOM stability) fails

**Diagnosis:**

**Case 1: FOM Increasing**
```
NPS       FOM
1E5       45
5E5       67
1E6       89
5E6       112

Pattern: Steadily increasing

Diagnosis:
  - Variance reduction converging during run
  - WWG still refining importance function
  - Not necessarily bad, but need more histories

Recommendation:
  - If using WWG: Iterate until FOM stable
  - Run longer to confirm FOM levels off
  - Don't trust early FOM values
```

**Case 2: FOM Decreasing**
```
NPS       FOM
1E5       125
5E5       98
1E6       67
5E6       42

Pattern: Steadily decreasing

Diagnosis: ⚠️ SERIOUS PROBLEM
  - Variance reduction deteriorating
  - Overbiasing creating high-variance artifacts
  - Weight windows may be too aggressive

Recommendation:
  - Immediately widen weight windows
  - Reduce VR aggressiveness
  - May need to restart with better VR setup
```

---

## Advanced Diagnostics

### Variance of Variance (VOV) Analysis

**Theory:** VOV measures the uncertainty in the uncertainty estimate itself.

$$\text{VOV} = \frac{S_{\hat{S}^2}^2}{\hat{S}^4}$$

**Interpretation:**
- VOV < 0.10: Good (uncertainty estimate reliable)
- VOV > 0.10: Poor (uncertainty estimate unreliable)

**High VOV diagnosis:**
```python
def diagnose_high_vov(vov, weight_data):
    """
    Identify cause of high VOV (>0.10)
    """
    if vov < 0.10:
        return {'status': 'GOOD', 'message': f'VOV = {vov:.4f} < 0.10'}

    # High VOV usually from few particles dominating
    if weight_data:
        w_max = max(weight_data)
        w_avg = sum(weight_data) / len(weight_data)
        w_ratio = w_max / w_avg

        if w_ratio > 100:
            return {
                'status': 'WEIGHT_OUTLIERS',
                'vov': vov,
                'weight_ratio': w_ratio,
                'diagnosis': 'Few particles have extreme weights',
                'solution': 'Widen weight windows or add weight cutoff'
            }

    return {
        'status': 'INSUFFICIENT_SAMPLING',
        'vov': vov,
        'diagnosis': 'High variance from insufficient sampling',
        'solution': 'Increase histories or improve variance reduction'
    }
```

### History Score Slope Analysis

**Theory:** MCNP fits tally-vs-history to power law:

$$\text{Tally}(N) = a \times N^b$$

**Expected slope:** b ∈ [3, 10] for well-behaved tallies

**Interpretation:**
- Slope 3-10: Normal (CLT behavior)
- Slope < 3: Super-convergence (suspicious!)
- Slope > 10: Under-convergence (needs more histories)

```python
def interpret_slope(slope):
    """Interpret history score slope"""

    if 3 <= slope <= 10:
        return {
            'status': 'NORMAL',
            'slope': slope,
            'message': 'Slope in acceptable range [3,10]',
            'implication': 'Normal CLT convergence behavior'
        }
    elif slope < 3:
        return {
            'status': 'WARNING',
            'slope': slope,
            'message': f'Slope {slope:.1f} < 3 (too low)',
            'implication': 'Super-convergence suggests systematic bias or batch correlation',
            'recommendation': 'Verify independence, check autocorrelation'
        }
    else:  # slope > 10
        return {
            'status': 'POOR',
            'slope': slope,
            'message': f'Slope {slope:.1f} > 10 (too high)',
            'implication': 'Slow convergence, very high variance',
            'recommendation': 'Significantly improve variance reduction or increase histories'
        }
```

---

## Integration with Variance Reduction

### VR-Specific Convergence Issues

**Issue 1: WWG Not Converged**
```
Symptom: FOM still increasing after 5+ iterations

Solution:
  1. Continue iterating until FOM change < 20%
  2. Check mesh resolution (may be too fine)
  3. Verify WWGE energy structure appropriate
```

**Issue 2: Exponential Transform Divergence**
```
Symptom: FOM decreasing, VOV > 0.10, weight ratio > 1E6

Solution:
  1. ALWAYS use weight windows with EXT
  2. Reduce EXT parameter p (try 0.7 instead of 0.9)
  3. Verify VECT points toward tally region
```

**Issue 3: DXTRAN Overbiasing**
```
Symptom: F5 has low R but fails checks 3,4,6,10

Solution:
  1. Increase DXTRAN inner sphere radius
  2. Reduce DXC contribution probabilities
  3. Add weight windows to control DXTRAN particle weights
```

---

## Quick Diagnostic Checklist

| Issue | Check | Threshold | Action if Failed |
|-------|-------|-----------|------------------|
| **Mean stability** | Last 50% variation | < 5% | Run longer or check VR |
| **Error trend** | Slope of log(R) vs log(N) | -0.5 ± 0.15 | Fix VR setup |
| **FOM stability** | FOM variation in last 50% | < 10% | Iterate WWG or widen WWP |
| **VOV** | Variance of variance | < 0.10 | Widen weight windows |
| **Slope** | History score fit | 3-10 | Improve sampling |
| **Autocorrelation** | Lag-1 correlation | < 0.10 | Increase batch size |
| **Weight ratio** | Max/min particle weights | < 1E4 | Widen weight windows |
| **Top particle contrib** | Top 10 particles | < 50% of total | Add importance |

**All checks passed → Reliable convergence → Trust results ✓**

---

## References

**Statistical Theory:**
- MCNP Theory Manual §2.7.1.2 - Central Limit Theorem
- MCNP Theory Manual §2.7.1.3 - Confidence intervals
- MCNP User Manual §3.4.2.4 - Ten statistical checks

**Convergence Analysis:**
- ../mcnp-statistics-checker/SKILL.md - Comprehensive statistical validation
- ../mcnp-statistics-checker/advanced_convergence_theory.md - Detailed theory

**Variance Reduction:**
- ../mcnp-variance-reducer/advanced_vr_theory.md - VR convergence issues
- ./vr_effectiveness_analysis.md - FOM and VR validation
