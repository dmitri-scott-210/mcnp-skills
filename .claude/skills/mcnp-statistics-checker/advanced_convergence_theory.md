# Advanced Convergence Theory for VR

**Phase 3 Addition - Statistical Theory Integration**

## Overview

This reference provides theoretical foundation for statistical quality checks in the context of variance reduction. Based on MCNP Theory Manual §2.7.1 and §2.7.2.

---

## Central Limit Theorem with VR

### Standard CLT

For N independent, identically distributed samples with finite variance:

$$\bar{x} \xrightarrow{d} \mathcal{N}\left(\mu, \frac{\sigma^2}{N}\right)$$

**Implications for MCNP:**
- Relative error R ∝ 1/√N
- Confidence intervals valid
- FOM constant

### VR Modifications to CLT

**Weight transport modifies sampling:**

$$\tilde{x}_i = w_i \cdot x_i$$

Where:
- x_i = analog score
- w_i = particle weight
- $\tilde{x}_i$ = weighted score

**Modified variance:**

$$\text{Var}(\tilde{x}) = E[w^2] \cdot \text{Var}(x)$$

**Key insight:** Weight variance multiplies score variance!

**Consequence:** If weights vary wildly (w_max/w_min > 1E6), CLT breaks down.

---

## Figure of Merit Theory

### Definition

$$\text{FOM} = \frac{1}{R^2 \cdot T}$$

**Ideal behavior:**
- Constant FOM → CLT holds
- Increasing FOM → VR converging
- Decreasing FOM → VR failing (overbiasing)

### FOM with Weight Windows

**Theory:** Properly tuned weight windows reduce variance without increasing work.

**Expected FOM ratio:**

$$\frac{\text{FOM}_{\text{WW}}}{\text{FOM}_{\text{analog}}} \approx \left(\frac{I_{\text{max}}}{I_{\text{min}}}\right)^{0.5 \text{ to } 1.0}$$

Where I = importance values

**Example:** Importance varies 1E6 → Expect FOM improvement ~1000×

---

## Variance of Variance (VOV)

### Theory

VOV measures uncertainty in the variance estimate itself:

$$\text{VOV} = \frac{\text{Var}(\hat{\sigma}^2)}{\hat{\sigma}^4}$$

**Ideal value:** VOV → 0 as N → ∞

**Practical threshold:** VOV < 0.10

### VOV with VR

High VOV usually indicates:

1. **Few particles dominate** (top 10 > 80%)
2. **Extreme weights** (w_max/w_min > 1E6)
3. **Insufficient sampling** (< 100 particles scored)

**Relationship to weight distribution:**

$$\text{VOV} \propto \frac{E[w^4]}{E[w^2]^2}$$

→ Fourth moment of weights! Very sensitive to extremes.

---

## History Score Slope

### Theory

MCNP fits tally vs history to power law:

$$\text{Score}(N) = a \cdot N^b$$

**Expected slope:** b ∈ [3, 10] for CLT-compliant tallies

### Interpretation

**Slope = 5 (typical):**
- Normal CLT behavior
- Well-sampled problem
- Good VR setup

**Slope < 3:**
- Super-convergence (suspicious!)
- Possible batch correlation
- May indicate bias

**Slope > 10:**
- Slow convergence
- Under-sampling
- VR insufficient

### VR Impact on Slope

**Well-tuned VR:** Slope → middle of range (4-6)
**Poor VR:** Slope outside range, especially high (>10)

---

## Convergence Rate Theory

### Analog Transport

$$R_{\text{analog}}(N) = \frac{C}{\sqrt{N}}$$

Where C = problem-specific constant

**Time to reach target R:**

$$T = \frac{C^2}{R_{\text{target}}^2} \cdot t_{\text{per particle}}$$

### With Variance Reduction

$$R_{\text{VR}}(N) = \frac{C_{\text{VR}}}{\sqrt{N}}$$

Where $C_{\text{VR}} < C$ (reduced constant)

**FOM improvement:**

$$\frac{\text{FOM}_{\text{VR}}}{\text{FOM}_{\text{analog}}} = \left(\frac{C}{C_{\text{VR}}}\right)^2 \cdot \frac{t_{\text{analog}}}{t_{\text{VR}}}$$

**Typical:** $C_{\text{VR}} / C \approx 0.1$ → FOM improves ~100× (if times comparable)

---

## Confidence Intervals with VR

### Standard Confidence Interval

For analog transport with N histories:

$$\mu \in \left[\bar{x} \pm t_{\alpha/2} \frac{s}{\sqrt{N}}\right]$$

Where:
- $t_{\alpha/2}$ = Student's t-value (typically 1.96 for 95%)
- s = sample standard deviation

### VR Considerations

**Valid IF:**
1. CLT applicable (large N, finite variance)
2. Weights well-behaved (ratio < 1E4)
3. No systematic bias (mean vs analog agrees)
4. All 10 checks pass

**Invalid IF:**
- High VOV (>0.10)
- Extreme weight ratio (>1E6)
- Few particles dominate (top 10 > 80%)

**Conservative approach:** Compare VR to short analog run to verify agreement.

---

## Statistical Power Analysis

### Hypothesis Testing for VR

**Null hypothesis:** VR result = Analog result

**Test statistic:**

$$z = \frac{|\bar{x}_{\text{VR}} - \bar{x}_{\text{analog}}|}{\sqrt{\sigma_{\text{VR}}^2 + \sigma_{\text{analog}}^2}}$$

**Decision:**
- z < 2: Accept null (VR unbiased) ✓
- z > 3: Reject null (VR biased) ✗

### Sample Size for Comparison

**To detect bias at 95% confidence:**

$$N_{\text{analog}} = \frac{4 \cdot \sigma_{\text{analog}}^2}{\Delta^2}$$

Where Δ = minimum detectable difference

**Example:** To detect 5% bias with σ = 15%:
- N_analog ≈ 3600 histories

---

## Batch Statistics Theory

### Purpose

Detect autocorrelation in sequential samples.

### Batch Mean Method

1. Divide N histories into K batches
2. Calculate mean per batch: $\bar{x}_k$
3. Estimate variance from batch means

**Effective sample size:**

$$N_{\text{eff}} = \frac{N}{1 + 2\rho}$$

Where ρ = autocorrelation coefficient

**VR impact:** WWG can create particle "families" → ρ > 0 → N_eff < N

---

## Integration with 10 Statistical Checks

### Enhanced Check Interpretation

| Check # | Standard Criterion | VR-Enhanced Interpretation |
|---------|-------------------|----------------------------|
| 1 | Mean stable | Mean stable AND agrees with analog |
| 2 | R < 0.10 | R < 0.10 AND weight ratio < 1E4 |
| 3 | VOV < 0.10 | VOV < 0.10 AND top 10 < 50% |
| 4 | FOM constant | FOM constant AND improved over analog |
| 5 | FOM > 100 | FOM > 100 AND > 10× analog FOM |
| 6 | Slope 3-10 | Slope 3-10 (especially 4-6 with VR) |
| 7 | No negative bins | No negative AND no unphysical jumps |
| 8 | 10/10 TFC | 10/10 TFC consistently across iterations |
| 9 | R ∝ 1/√N | R ∝ 1/√N with slope -0.5 ± 0.1 |
| 10 | PDF normal | PDF normal with no extreme outliers |

---

## Quick Reference Formulas

**FOM:**
$$\text{FOM} = \frac{1}{R^2 \cdot T}$$

**Required histories for target R:**
$$N_{\text{target}} = N_{\text{current}} \cdot \left(\frac{R_{\text{current}}}{R_{\text{target}}}\right)^2$$

**Time estimate:**
$$T_{\text{target}} = \frac{1}{\text{FOM} \cdot R_{\text{target}}^2}$$

**Confidence interval (95%):**
$$\mu \in [\bar{x} \pm 1.96 R \bar{x}]$$

**Agreement test:**
$$z = \frac{|x_1 - x_2|}{\sqrt{\sigma_1^2 + \sigma_2^2}} < 2$$

---

## References

**MCNP Theory Manual:**
- §2.7.1.2 - Central Limit Theorem
- §2.7.1.3 - Confidence intervals
- §2.7.2 - Variance reduction theory
- §2.7.2.12 - Weight window generator

**Related Files:**
- ./vr_quality_metrics.md - VR-specific quality indicators
- ../mcnp-tally-analyzer/convergence_diagnostics.md - Practical convergence analysis

**MCNP User Manual:**
- §3.4.2.4 - Ten statistical checks
- §3.4.3 - Production run criteria
