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
  - Shannon entropy
version: "2.0.0"
---

# MCNP Criticality Analyzer Skill

## Purpose

Analyze MCNP criticality (KCODE) calculation results, interpret k-effective (keff) values, assess source convergence through Shannon entropy, and validate that criticality calculations have converged to statistically reliable results.

## When to Use This Skill

- Analyzing output from KCODE criticality calculations
- Interpreting k-effective values and confidence intervals
- Checking whether fission source distribution has converged
- Evaluating Shannon entropy plots for source convergence
- Determining if additional inactive or active cycles needed
- Troubleshooting non-converging criticality problems
- Comparing keff results from different configurations
- Validating reactor core designs or critical assemblies

## Prerequisites

- **kcode_analysis_guide.md**: Complete KCODE analysis procedures and statistical checks
- **entropy_convergence_guide.md**: Shannon entropy, dominance ratio, convergence diagnostics
- **scripts/README.md**: Python tools for automated analysis
- **mcnp-source-builder**: Understanding KCODE and KSRC cards
- **mcnp-statistics-checker**: General statistical validation concepts

## Core Concepts

### K-Effective (keff)

**Definition**: Effective neutron multiplication factor
- **keff > 1.0**: Supercritical (chain reaction grows)
- **keff = 1.0**: Critical (steady-state chain reaction)
- **keff < 1.0**: Subcritical (chain reaction dies out)

**Physical Meaning:**
```
keff = (neutrons in generation n+1) / (neutrons in generation n)
```

### Active vs Inactive Cycles

**KCODE Format:**
```
KCODE  nsrc  k0  nskip  ncycles
       10000 1.0  50    150
       ^neutrons/cycle
              ^guess
                  ^inactive cycles (source convergence)
                      ^total cycles (100 active for statistics)
```

**Inactive Cycles (nskip):**
- Source distribution converging
- Not used in keff calculation
- Typical: 20-500 cycles (problem-dependent)

**Active Cycles (ncycles - nskip):**
- Cycles after source convergence
- Used for keff statistics
- Typical: 100-2000 cycles

### Shannon Entropy (Source Convergence Metric)

**Purpose:** Quantifies spatial distribution of fission source

**Formula:**
```
H = -Σᵢ pᵢ log₂(pᵢ)
```

**Interpretation:**
- **Rising entropy**: Source still spreading/converging
- **Flat entropy**: Source converged (good) ✓
- **Oscillating entropy**: High dominance ratio issue
- **Trending during active**: Not converged (increase nskip)

**See entropy_convergence_guide.md** for comprehensive diagnostics

### Three keff Estimators

MCNP provides three independent estimates:
- **Collision**: Based on collision rates
- **Absorption**: Based on absorption/fission rates
- **Track-Length**: Based on flux integrals

**All three should agree within 2σ** (good convergence indicator)

### Statistical Checks

MCNP performs 10 statistical quality checks on final keff:
1. Mean behavior
2. Relative error (R < 0.05 or 5%)
3. Variance of variance (VOV < 0.10)
4. Figure of merit (FOM constant)
5. Relative slope (|slope| < 0.1)
6. TFC bins 1-8 pass
7. TFC slope near zero
8. Central moment (no outliers)
9. Normality test
10. Largest history score

**Goal:** Pass all 10 checks for reliable results

**See kcode_analysis_guide.md** for detailed explanation of each check

---

## Decision Tree: Criticality Analysis

```
START: Received KCODE output
  |
  +--> Extract keff and uncertainty
       |
       +--> Check entropy convergence
            |
            +--> Entropy flat after nskip?
                 |
                 +--[YES]--> Check statistical quality
                 |           |
                 |           +--> All 10 checks passed?
                 |                |
                 |                +--[YES]--> RESULT ACCEPTABLE ✓
                 |                |           Report: keff ± uncertainty
                 |                |
                 |                +--[NO]---> POOR STATISTICS
                 |                            → Increase nsrc or active cycles
                 |                            → Rerun
                 |
                 +--[NO]---> SOURCE NOT CONVERGED
                             → Increase nskip
                             → Check for high dominance ratio
                             → Improve KSRC distribution
                             → Rerun

See entropy_convergence_guide.md for convergence diagnostics
See kcode_analysis_guide.md for statistical quality fixes
```

## Tool Invocation

Python implementation for automated criticality analysis.

### Basic Usage

```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

# Initialize
analyzer = MCNPCriticalityAnalyzer()

# Analyze KCODE results
results = analyzer.analyze_kcode('outp')

# Access results
print(f"keff: {results['keff']} ± {results['error']}")
print(f"Relative error: {results['relative_error']}%")
print(f"Entropy converged: {results['entropy_converged']}")
print(f"Statistical quality: {results['quality']}")

# Check quality
if results['quality'] == 'EXCELLENT':
    print("✓ Results reliable")
else:
    print("⚠ Poor quality - increase cycles or check convergence")
```

**See scripts/README.md** for complete API documentation and integration examples.

---

## Use Case 1: Basic KCODE Analysis

**Scenario**: Analyzing bare U-235 sphere criticality calculation

**Output Excerpt:**
```
 the final estimated combined collision/absorption/track-length keff = 1.00345 
 with an estimated standard deviation of 0.00087

 the final keff estimator values and 68, 95, and 99 percent confidence intervals are:

                     keff       68% confidence      95% confidence
      collision     1.00321      1.00234 to 1.00408  1.00147 to 1.00495
      absorption    1.00368      1.00281 to 1.00455  1.00194 to 1.00542
      track length  1.00346      1.00259 to 1.00433  1.00172 to 1.00520
      col/abs/trk   1.00345      1.00258 to 1.00432  1.00171 to 1.00519
```

**Entropy Table:**
```
    cycle     keff     entropy
       50    1.00345    5.9534  ← Last inactive
       60    1.00338    5.9531
      100    1.00345    5.9533
      150    1.00344    5.9532  ← Final
```

**Analysis:**
- **keff = 1.00345 ± 0.00087**: System critical (≈1.00)
- **Relative error = 0.087%**: Good precision
- **Three estimators agree**: ✓ Good convergence
- **Entropy flat after cycle 50**: ✓ Source converged
- **Conclusion**: ACCEPTABLE RESULT ✓

**See kcode_analysis_guide.md** for complete analysis procedure

## Use Case 2: Detecting Poor Source Convergence

**Scenario**: Entropy still changing during active cycles

**Entropy Table:**
```
    cycle     keff     entropy
       50    1.00845    5.9534  ← Last inactive
       60    1.00538    5.9712  ← Still changing!
       80    1.00245    5.9891
      100    1.00165    5.9956  ← Still rising
      150    1.00145    5.9987  ← Never plateaued
```

**Diagnosis:**
- Entropy continuously rising through active cycles
- keff trending downward (correlated)
- nskip=50 insufficient

**Solution:**
```
c OLD: KCODE  10000  1.0  50  150
c NEW: KCODE  10000  1.0  100  250  (increase nskip)
```

**See entropy_convergence_guide.md** for detailed convergence troubleshooting

## Use Case 3: Insufficient Statistics

**Scenario**: Source converged but uncertainty too large

**Output:**
```
keff = 1.00345 ± 0.00487
Relative error = 0.485%  (target: < 0.1%)

Statistical checks:
  ✓ mean
  ✗ relative error FAILED (R = 0.485% > 0.1%)
  ✓ VOV
  ✗ FOM FAILED (not constant)
```

**Diagnosis:** Only 100 active cycles insufficient

**Solutions:**

**Option 1: More cycles**
```
OLD: KCODE  10000  1.0  50  150  (100 active)
NEW: KCODE  10000  1.0  50  550  (500 active)
```

**Option 2: More neutrons/cycle**
```
OLD: KCODE  10000  1.0  50  150
NEW: KCODE  50000  1.0  50  150
```

**Option 3: Combined**
```
KCODE  20000  1.0  50  350  (best approach)
```

**Statistical Relationship:**
```
R ∝ 1/√(nsrc × n_active)
```

**See kcode_analysis_guide.md** for complete statistical quality fixes

## Use Case 4: Comparing Configurations

**Scenario**: Control rod worth (keff with rods IN vs OUT)

**Configuration 1: Rods OUT**
```
keff₁ = 1.05432 ± 0.00045
```

**Configuration 2: Rods IN**
```
keff₂ = 0.98765 ± 0.00052
```

**Statistical Comparison:**
```python
analyzer = MCNPCriticalityAnalyzer()
comparison = analyzer.compare_keff(1.05432, 0.00045, 0.98765, 0.00052)

Δk = 0.06667
σ_total = 0.00069
N_σ = 96.6 σ
```

**Interpretation:** Difference is HIGHLY SIGNIFICANT (>3σ)

**Reactivity Worth:**
```
ρ₁ = +5154 pcm
ρ₂ = -1250 pcm
Control rod worth: Δρ = 6404 pcm
```

**See kcode_analysis_guide.md** for complete comparison procedures

---

## Integration with Other Skills

### mcnp-source-builder
- **Provides**: KCODE/KSRC setup
- **This skill analyzes**: First run convergence
- **source-builder adjusts**: KSRC points if needed
- **This skill validates**: Improved convergence

### mcnp-statistics-checker
- **This skill**: Criticality-specific (keff, entropy, source)
- **statistics-checker**: General tally validation (10 checks)
- **Use both**: For complete validation

### mcnp-material-builder
- **material-builder**: Defines fissile materials
- **This skill**: Analyzes resulting keff
- **If keff ≠ target**: material-builder adjusts enrichment
- **This skill validates**: New keff value

### mcnp-output-parser
- **output-parser**: Extracts keff/entropy data from files
- **This skill**: Interprets extracted data

### Typical Workflow
```
1. mcnp-geometry-builder   → Define core
2. mcnp-material-builder   → Define materials
3. mcnp-source-builder     → Create KCODE/KSRC
4. [Run MCNP]
5. mcnp-output-parser      → Extract data
6. THIS SKILL              → Analyze convergence
7. IF not converged:
     mcnp-source-builder   → Adjust parameters
     Go to step 4
8. IF converged:
     THIS SKILL            → Report final keff
     DONE ✓
```

---

## Common Issues and Solutions

### Issue 1: Entropy Not Converging

**Symptom:** Entropy continuously rising during active cycles

**Solution:** Increase nskip
```
KCODE  10000  1.0  100  300  (was 50 nskip)
```

**See entropy_convergence_guide.md § Pattern 2**

### Issue 2: VOV > 0.10

**Symptom:** Check 3 fails, variance unstable

**Solution:** Increase active cycles
```
KCODE  10000  1.0  50  450  (was 150 total)
```

**See kcode_analysis_guide.md § Troubleshooting**

### Issue 3: Oscillating keff and Entropy

**Symptom:** Long-period oscillations (20-100 cycles)

**Diagnosis:** High dominance ratio

**Solutions:**
- Dramatically increase nskip (200-500 cycles)
- Better KSRC distribution (20-50 points)
- Increase nsrc (50,000 neutrons/cycle)

**See entropy_convergence_guide.md § High Dominance Ratio**

### Issue 4: keff = 0.00000

**Causes:**
- No fissile material
- SDEF card present (wrong mode)
- NPS card present (wrong mode)
- Geometry errors

**See kcode_analysis_guide.md § Zero or Invalid keff**

---

## Validation Checklist

Before accepting keff results:

### Source Convergence
- [ ] Entropy plot reviewed
- [ ] Entropy plateaued before active cycles
- [ ] No trends during active cycles
- [ ] nskip ≥ convergence_cycle × 1.2

### Statistical Quality
- [ ] Relative error < 0.1% (design) or < 0.01% (benchmark)
- [ ] All 10 statistical checks passed
- [ ] VOV < 0.10
- [ ] Three estimators agree within 2σ

### Physical Reasonableness
- [ ] keff value makes physical sense
- [ ] No lost particles
- [ ] Geometry verified with plot

### Documentation
- [ ] KCODE parameters recorded
- [ ] Final keff ± uncertainty documented
- [ ] Convergence behavior noted

**See kcode_analysis_guide.md for complete checklist**

---

## Best Practices

1. **Always Check Entropy First**
   - If entropy not converged, keff is meaningless
   - Plot entropy vs cycle
   - Ensure plateau before active cycles

2. **Use Conservative nskip**
   - nskip = convergence_cycle × 1.2 (minimum)
   - Better to oversample inactive than undersample

3. **Distribute KSRC Points**
   - Span entire fissile region
   - 8-50 points for complex geometries

4. **Target < 0.1% Relative Error**
   - 0.1-0.5%: Preliminary
   - 0.05-0.1%: Design
   - < 0.05%: Verification
   - < 0.01%: Benchmark

5. **Verify with Plot**
   - Before long runs: `mcnp6 inp=input.i ip`
   - Check for gaps, overlaps

6. **Document Everything**
   - KCODE parameters
   - Final keff ± uncertainty
   - Convergence behavior
   - Runtime

**See kcode_analysis_guide.md § Best Practices for complete list**

---

## Quick Reference

| Need | Check | Target | Action if Failed |
|------|-------|--------|------------------|
| Source convergence | Entropy plot | Flat after nskip | Increase nskip |
| Statistical quality | 10 checks | All pass | Increase cycles or nsrc |
| Precision | Relative error | < 0.1% | Increase nsrc × n_active |
| Variance stability | VOV | < 0.10 | Increase active cycles |
| Estimator agreement | Col/Abs/Trk | Within 2σ | Check convergence |

---

## References

- **kcode_analysis_guide.md**: Complete KCODE analysis procedures, statistical checks, keff interpretation
- **entropy_convergence_guide.md**: Shannon entropy, dominance ratio, source convergence diagnostics
- **scripts/README.md**: Python tools for automated analysis
- **mcnp-statistics-checker**: General statistical validation (10 checks explained)
- **mcnp-source-builder**: KCODE/KSRC card creation
- **MCNP User Manual**: Chapter 5.8 (KCODE), Appendix (statistical tests)

---

**End of MCNP Criticality Analyzer Skill**
