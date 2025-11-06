# Variance Reduction Quality Metrics

**Phase 3 Addition - VR-Specific Statistical Validation**

## Overview

Standard statistical checks (10 checks from Chapter 3.4.2.4) validate tally reliability, but variance reduction introduces additional quality concerns. This reference provides VR-specific metrics to ensure VR is effective AND not introducing bias or artifacts.

**Key Questions:**
- Are my weight windows helping or hurting?
- Is VR introducing statistical bias?
- How do I know if VR is converged?

---

## VR-Specific Quality Metrics

### Metric 1: FOM Stability Ratio

**Definition:** Ratio of FOM variation to mean FOM in last 50% of run

$$\text{FOM Stability} = \frac{\sigma_{\text{FOM}}}{\mu_{\text{FOM}}}$$

**Thresholds:**
- **Good:** < 0.10 (±10% variation)
- **Marginal:** 0.10-0.20
- **Poor:** > 0.20

**Interpretation:**
```
Good FOM stability → VR converged, CLT applicable
Poor FOM stability → VR still evolving OR overbiasing issues
```

**Example:**
```python
def calculate_fom_stability(fom_history):
    """Calculate FOM stability in last half of run"""
    import numpy as np

    last_half = fom_history[len(fom_history)//2:]
    mean_fom = np.mean(last_half)
    std_fom = np.std(last_half)
    stability = std_fom / mean_fom if mean_fom > 0 else 999

    if stability < 0.10:
        status = 'GOOD'
    elif stability < 0.20:
        status = 'MARGINAL'
    else:
        status = 'POOR'

    return {
        'stability_ratio': stability,
        'mean_fom': mean_fom,
        'std_fom': std_fom,
        'status': status,
        'recommendation': 'VR converged' if status == 'GOOD' else 'Continue iterating or widen WWP'
    }
```

---

### Metric 2: Weight Distribution Quality

**Purpose:** Detect if few particles dominate tally (sign of overbiasing)

**Measurements:**

**a) Maximum/Minimum Weight Ratio:**
```
Weight ratio = w_max / w_min

Thresholds:
  Good:     < 1E4
  Marginal: 1E4 - 1E6
  Poor:     > 1E6
```

**b) Top-N Particle Contribution:**
```
Top 10 contribution = (Sum of top 10 weights) / (Total weight)

Thresholds:
  Good:     < 0.50 (top 10 < 50%)
  Marginal: 0.50 - 0.80
  Poor:     > 0.80 (top 10 dominate!)
```

**c) Weight Coefficient of Variation:**
```
CV = σ_weights / μ_weights

Thresholds:
  Good:     CV < 2.0
  Marginal: CV = 2.0 - 5.0
  Poor:     CV > 5.0
```

**Implementation:**
```python
def assess_weight_distribution(particle_weights):
    """
    Comprehensive weight distribution quality assessment

    Args:
        particle_weights: list or array of particle weights contributing to tally

    Returns:
        assessment: dict with multiple weight quality metrics
    """
    import numpy as np

    if len(particle_weights) < 10:
        return {
            'status': 'ERROR',
            'message': 'Insufficient particles (<10) scored',
            'recommendation': 'Drastically improve VR or increase histories'
        }

    weights = np.array(particle_weights)

    # Metric 1: Weight ratio
    w_max = np.max(weights)
    w_min = np.min(weights)
    w_ratio = w_max / w_min

    # Metric 2: Top 10 contribution
    weights_sorted = np.sort(weights)[::-1]  # Descending
    top_10 = weights_sorted[:10]
    top_10_contrib = np.sum(top_10) / np.sum(weights)

    # Metric 3: Coefficient of variation
    cv = np.std(weights) / np.mean(weights)

    # Assess each metric
    issues = []

    if w_ratio > 1E6:
        issues.append('Extreme weight ratio (>1E6) - severe overbiasing')
    elif w_ratio > 1E4:
        issues.append('Large weight ratio (>1E4) - caution advised')

    if top_10_contrib > 0.80:
        issues.append(f'Top 10 particles contribute {top_10_contrib:.0%} (>80%) - dominance issue')
    elif top_10_contrib > 0.50:
        issues.append(f'Top 10 particles contribute {top_10_contrib:.0%} (>50%) - borderline')

    if cv > 5.0:
        issues.append(f'High weight CV ({cv:.1f} > 5.0) - extreme variance')
    elif cv > 2.0:
        issues.append(f'Moderate weight CV ({cv:.1f}) - acceptable but monitor')

    # Overall status
    if not issues:
        overall_status = 'EXCELLENT'
        recommendation = 'Weight distribution is healthy'
    elif len(issues) == 1 and 'borderline' in issues[0]:
        overall_status = 'GOOD'
        recommendation = 'Minor weight issues, acceptable for production'
    elif any('severe' in issue or 'dominance' in issue for issue in issues):
        overall_status = 'POOR'
        recommendation = 'Widen weight windows (WWP wupn=10) or reduce VR aggressiveness'
    else:
        overall_status = 'MARGINAL'
        recommendation = 'Monitor closely, consider widening weight windows'

    return {
        'status': overall_status,
        'weight_ratio': w_ratio,
        'top_10_contribution': top_10_contrib,
        'cv': cv,
        'n_particles': len(weights),
        'issues': issues,
        'recommendation': recommendation
    }
```

---

### Metric 3: Mean Stability in VR Context

**Enhanced check:** Mean should be stable, AND agree with analog within uncertainty

**Comparison test:**
```python
def compare_vr_to_analog(mean_analog, error_analog, mean_vr, error_vr):
    """
    Statistical test: do VR and analog results agree?

    Returns:
        agreement_test: dict with statistical comparison
    """
    import numpy as np

    # Combined standard deviation
    sigma_combined = np.sqrt(
        (mean_analog * error_analog)**2 +
        (mean_vr * error_vr)**2
    )

    # Difference in standard deviations
    difference = abs(mean_vr - mean_analog)
    n_sigma = difference / sigma_combined if sigma_combined > 0 else 999

    if n_sigma < 2:
        status = 'AGREEMENT'
        assessment = f'VR and analog agree within {n_sigma:.2f}σ (< 2σ)'
        recommendation = 'VR is unbiased ✓'
    elif n_sigma < 3:
        status = 'MARGINAL'
        assessment = f'VR and analog differ by {n_sigma:.2f}σ (2-3σ range)'
        recommendation = 'Marginal agreement, investigate if persistent'
    else:
        status = 'DISAGREEMENT'
        assessment = f'VR and analog differ by {n_sigma:.2f}σ (> 3σ)'
        recommendation = '⚠ Possible VR bias! Review setup immediately'

    return {
        'status': status,
        'analog_value': mean_analog,
        'vr_value': mean_vr,
        'difference': difference,
        'n_sigma': n_sigma,
        'assessment': assessment,
        'recommendation': recommendation
    }

# Example usage:
result = compare_vr_to_analog(
    mean_analog=2.73e-4,
    error_analog=0.15,
    mean_vr=2.68e-4,
    error_vr=0.03
)

print(f"Status: {result['status']}")
print(f"Assessment: {result['assessment']}")
print(f"Recommendation: {result['recommendation']}")
```

---

### Metric 4: VOV Behavior with VR

**Standard VOV threshold:** < 0.10

**VR-enhanced interpretation:**

| VOV | Standard Check | VR Interpretation |
|-----|----------------|-------------------|
| < 0.05 | Excellent | ✓ VR producing good sampling |
| 0.05-0.10 | Good | ✓ Acceptable, VR working |
| 0.10-0.20 | Marginal | ⚠ VR may be too aggressive |
| > 0.20 | Poor | ✗ Overbiasing likely, widen WWP |

**Diagnostic:**
```
High VOV with VR usually means:
  1. Weight windows too narrow (particles split/RR too frequently)
  2. Few particles have extreme weights
  3. Insufficient convergence of importance function

Solutions:
  - WWP:N 10 3 5 0 -1 (widen wupn to 10)
  - Iterate WWG more times
  - Check weight distribution (Metric 2)
```

---

### Metric 5: History Slope Consistency

**Standard range:** 3.0 ≤ slope ≤ 10.0

**VR context:**

**Slope < 3.0 with VR:**
```
Possible causes:
  1. Batch correlation (WWG creates "families" of particles)
  2. Source biasing too aggressive
  3. Statistical artifact from few dominant particles

Check:
  - Autocorrelation (should be < 0.10)
  - Weight distribution (top 10 < 50%)
  - Mean stability (should be converged)
```

**Slope > 10.0 with VR:**
```
Possible causes:
  1. VR insufficient for problem difficulty
  2. Importance function not optimized
  3. Need more WWG iterations

Actions:
  - Continue iterating WWG
  - Consider adding exponential transform (EXT)
  - May need fundamentally different VR approach
```

---

### Metric 6: WWG Iteration Convergence

**Purpose:** Track WWG convergence over multiple iterations

**Convergence criterion:** FOM change < 20% between iterations

**Tracking:**
```python
def assess_wwg_convergence(iteration_history):
    """
    Evaluate WWG convergence over iterations

    Args:
        iteration_history: list of dicts with 'iteration', 'fom', 'error'

    Returns:
        convergence_status: dict with convergence assessment
    """
    if len(iteration_history) < 2:
        return {
            'status': 'INSUFFICIENT_DATA',
            'message': 'Need at least 2 iterations to assess convergence'
        }

    # Calculate FOM changes
    fom_changes = []
    for i in range(1, len(iteration_history)):
        fom_prev = iteration_history[i-1]['fom']
        fom_curr = iteration_history[i]['fom']
        pct_change = (fom_curr - fom_prev) / fom_prev if fom_prev > 0 else 0
        fom_changes.append(pct_change)

    latest_change = fom_changes[-1]

    # Check for convergence
    if abs(latest_change) < 0.20:  # <20% change
        status = 'CONVERGED'
        message = f'Latest FOM change: {latest_change:+.1%} (< ±20%)'
        recommendation = 'WWG converged! Use current wwout for production'
    elif abs(latest_change) < 0.40:  # <40% change
        status = 'CONVERGING'
        message = f'Latest FOM change: {latest_change:+.1%} (20-40%)'
        recommendation = 'Good progress, iterate 1-2 more times'
    elif latest_change > 0:  # Still improving
        status = 'NOT_CONVERGED'
        message = f'Latest FOM change: {latest_change:+.1%} (> +40%)'
        recommendation = 'Still improving significantly, continue iterating'
    else:  # Decreasing FOM
        status = 'DIVERGING'
        message = f'FOM DECREASING: {latest_change:+.1%}'
        recommendation = '⚠ Overbiasing! Use previous iteration wwout'

    return {
        'status': status,
        'n_iterations': len(iteration_history),
        'latest_fom_change': latest_change,
        'all_changes': fom_changes,
        'message': message,
        'recommendation': recommendation
    }
```

---

### Metric 7: Particle Balance with VR

**Standard balance:** Source = Absorption + Leakage + (n,xn)

**VR context:**

**Acceptable imbalance:** < 5%

**Warning signs:**
```
Imbalance > 10% with VR suggests:
  1. Particles lost due to weight cutoff
  2. Importance causing premature termination
  3. Weight windows rejecting particles

Check MCNP output for:
  - "N particles got lost" warnings
  - Weight cutoff card (CUT card)
  - Cell importance =0 in paths
```

---

### Metric 8: Energy/Spatial Uniformity

**Purpose:** Ensure VR improves ALL bins, not just some

**Measurement:**
```python
def assess_vr_uniformity(bin_errors_analog, bin_errors_vr):
    """
    Compare error distribution across bins

    Good VR: Reduces error uniformly
    Poor VR: Some bins improve, others worsen
    """
    import numpy as np

    improvements = []
    for e_analog, e_vr in zip(bin_errors_analog, bin_errors_vr):
        if e_analog > 0:
            improvement = e_analog / e_vr
            improvements.append(improvement)

    improvements = np.array(improvements)

    mean_improvement = np.mean(improvements)
    std_improvement = np.std(improvements)
    min_improvement = np.min(improvements)
    max_improvement = np.max(improvements)

    # Check uniformity
    cv_improvement = std_improvement / mean_improvement if mean_improvement > 0 else 999

    if cv_improvement < 0.30:  # Uniform improvement
        status = 'UNIFORM'
        message = 'VR improves all bins uniformly'
    elif cv_improvement < 0.60:
        status = 'MODERATE'
        message = 'VR improvement varies moderately across bins'
    else:
        status = 'NON_UNIFORM'
        message = 'VR improvement highly variable - some bins helped, others not'

    # Check for bins that got WORSE
    worsened_bins = [i for i, imp in enumerate(improvements) if imp < 1.0]

    return {
        'status': status,
        'mean_improvement': mean_improvement,
        'cv_improvement': cv_improvement,
        'min_improvement': min_improvement,
        'max_improvement': max_improvement,
        'worsened_bins': worsened_bins,
        'message': message,
        'recommendation': 'Adjust VR to improve uniformity' if status == 'NON_UNIFORM' else 'Good VR coverage'
    }
```

---

## Comprehensive VR Quality Assessment

### Integrated Checklist

Run ALL standard checks + VR-specific metrics:

| Check | Standard Threshold | VR-Enhanced Threshold | Priority |
|-------|-------------------|----------------------|----------|
| **Standard 10 Checks** | 10/10 passed | 10/10 passed | CRITICAL |
| **FOM stability** | — | < 10% variation | HIGH |
| **Weight ratio** | — | < 1E4 | HIGH |
| **Top 10 contrib** | — | < 50% | HIGH |
| **VOV** | < 0.10 | < 0.10 (< 0.05 better) | CRITICAL |
| **Mean vs analog** | — | < 2σ difference | HIGH |
| **WWG convergence** | — | FOM change < 20% | MEDIUM |
| **Particle balance** | < 5% | < 5% | MEDIUM |
| **Uniformity** | — | CV < 0.60 | LOW |

**Overall quality:**
- **EXCELLENT:** All CRITICAL + HIGH pass
- **GOOD:** All CRITICAL pass, 1-2 HIGH marginal
- **MARGINAL:** Some HIGH fail, CRITICAL pass
- **POOR:** Any CRITICAL fail

---

## VR Quality Score

**Automated scoring:**
```python
def calculate_vr_quality_score(results):
    """
    Calculate overall VR quality score (0-100)

    Args:
        results: dict with all VR quality metrics

    Returns:
        score: 0-100, with interpretation
    """
    score = 0
    max_score = 100

    # Standard checks (40 points)
    checks_passed = results.get('standard_checks_passed', 0)
    score += (checks_passed / 10) * 40

    # FOM stability (15 points)
    fom_stability = results.get('fom_stability', 999)
    if fom_stability < 0.10:
        score += 15
    elif fom_stability < 0.20:
        score += 10

    # Weight distribution (20 points)
    weight_status = results.get('weight_status', 'POOR')
    if weight_status == 'EXCELLENT':
        score += 20
    elif weight_status == 'GOOD':
        score += 15
    elif weight_status == 'MARGINAL':
        score += 10

    # Mean agreement (15 points)
    n_sigma = results.get('mean_vs_analog_sigma', 999)
    if n_sigma < 2:
        score += 15
    elif n_sigma < 3:
        score += 10

    # WWG convergence (10 points)
    wwg_converged = results.get('wwg_converged', False)
    if wwg_converged:
        score += 10

    # Interpretation
    if score >= 90:
        quality = 'EXCELLENT'
        message = 'VR is highly effective and reliable'
    elif score >= 75:
        quality = 'GOOD'
        message = 'VR is effective with minor issues'
    elif score >= 60:
        quality = 'MARGINAL'
        message = 'VR has significant issues, improvements needed'
    else:
        quality = 'POOR'
        message = 'VR is unreliable or ineffective, major changes required'

    return {
        'score': score,
        'max_score': max_score,
        'percentage': score / max_score,
        'quality': quality,
        'message': message
    }
```

---

## Quick VR Quality Checklist

**Before trusting VR results, verify:**

- [ ] ✅ All 10 standard statistical checks pass
- [ ] ✅ FOM stable in last 50% (variation <10%)
- [ ] ✅ Weight ratio < 1E4
- [ ] ✅ Top 10 particles < 50% of total weight
- [ ] ✅ VOV < 0.10
- [ ] ✅ Mean agrees with analog (if available, <2σ)
- [ ] ✅ WWG converged (FOM change <20% per iteration)
- [ ] ✅ Particle balance within 5%
- [ ] ✅ No warnings about lost particles
- [ ] ✅ Error improved uniformly across bins

**If ALL checks passed → VR is reliable ✓**
**If ANY CRITICAL check failed → Do not trust results ✗**

---

## References

**VR Theory:**
- ../mcnp-variance-reducer/advanced_vr_theory.md - VR optimization strategies
- ../mcnp-variance-reducer/variance_reduction_theory.md - FOM fundamentals

**Statistical Theory:**
- ./advanced_convergence_theory.md - CLT and convergence diagnostics
- ./statistical_troubleshooting.md - VR-specific problem solving

**Related Analysis:**
- ../mcnp-tally-analyzer/vr_effectiveness_analysis.md - FOM analysis
- ../mcnp-tally-analyzer/convergence_diagnostics.md - Convergence validation

**MCNP Manual:**
- §3.4.2.4 - Ten statistical checks
- §2.7.2.12 - Weight window generator
- §3.4.3 - Production run checks
