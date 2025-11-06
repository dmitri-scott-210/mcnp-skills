---
category: C
name: mcnp-warning-analyzer
description: "Interpret and address MCNP warning messages including material warnings, physics warnings, statistical warnings, and convergence issues to ensure result validity"
version: "2.0.0"
---

# MCNP Warning Analyzer

## Overview

This skill provides systematic procedures for interpreting and addressing MCNP warning messages. Unlike fatal errors, warnings allow calculations to proceed but indicate potentially problematic conditions that may affect result validity. This skill covers material warnings, statistical quality checks, convergence issues (criticality), physics warnings, deprecation notices, and decision frameworks for determining which warnings require action.

Warning analysis is critical for Monte Carlo result validation. Statistical warnings indicate insufficient convergence, material warnings may affect physics accuracy, and convergence warnings (KCODE) invalidate criticality results if ignored. This skill emphasizes the "statistical checks first" principle: address statistical quality (10 checks) before trusting any tally results.

## When to Use This Skill

- MCNP output contains warning messages after run completes
- Need to determine if warnings affect result validity
- Statistical checks show "missed" or poor convergence (>2 of 10 checks failed)
- Material composition warnings require evaluation
- Source convergence warnings in criticality calculations (Shannon entropy)
- Tally statistics warnings indicate reliability issues
- Physics model warnings need assessment
- Deprecation warnings for input syntax modernization

## Decision Tree: Analyzing Warnings

\`\`\`
START: Warning Message in MCNP Output
  |
  +--> Is it a "fatal error"?
  |      |
  |      +--> YES: Use mcnp-fatal-error-debugger skill instead
  |      |
  |      +--> NO: Continue (it's a warning or comment)
  |
  +--> What type of warning?
  |      |
  |      +--> Statistical Warning (tally checks failed)
  |      |      ├─> Check tally fluctuation chart
  |      |      ├─> Count failed checks (1-10)
  |      |      ├─> 0 failed: Reliable result ✓
  |      |      ├─> 1-2 failed: Marginal, investigate ⚠️
  |      |      ├─> 3+ failed: Unreliable, must fix ❌
  |      |      └─> Actions: Run longer, improve VR (see statistical_checks_guide.md)
  |      |
  |      +--> Convergence Warning (KCODE Shannon entropy)
  |      |      ├─> Check Shannon entropy plot in output
  |      |      ├─> If trending: More inactive cycles needed
  |      |      ├─> If oscillating: Better initial KSRC
  |      |      └─> Action: Extend inactive cycles, verify source converged
  |      |
  |      +--> Material Warning (unnormalized fractions)
  |      |      ├─> Check Table 40 for normalized values
  |      |      ├─> Compare MCNP normalization to intent
  |      |      ├─> <1% difference: Likely acceptable
  |      |      ├─> >5% difference: Fix composition
  |      |      └─> Document material composition choice
  |      |
  |      +--> Physics Warning (energy cutoffs, models disabled)
  |      |      ├─> "physics models disabled" → Expected for MODE?
  |      |      ├─> Energy cutoff reached → Are cutoffs appropriate?
  |      |      └─> Verify physics setup matches problem intent
  |      |
  |      +--> Deprecation Warning (obsolete syntax)
  |      |      ├─> Note for future input updates
  |      |      ├─> Functionality still works (no immediate action)
  |      |      └─> Plan migration to new syntax when convenient
  |      |
  |      └─> IEEE Exception Warning (floating point)
  |             ├─> If run completed → Usually safe
  |             ├─> "inexact" very common (harmless)
  |             ├─> If excessive (>10k) → Check input values
  |             └─> Document if unusual pattern observed
  |
  +--> Does warning affect result validity?
         |
         +--> YES: Fix issue and re-run with verification
         |
         +--> NO: Document warning and proceed with analysis
\`\`\`

## Quick Reference: Common Warning Messages

| Warning Pattern | Significance | Action | Detailed Reference |
|----------------|--------------|--------|-------------------|
| "failed X of 10 checks" | HIGH (X>2) | Run longer, improve VR | statistical_checks_guide.md |
| "entropy not converged" | CRITICAL | More inactive cycles | warning_catalog.md §8 |
| "unnormalized fractions" | LOW-MEDIUM | Verify intent, fix if wrong | warning_catalog.md §1 |
| "relative error > 0.50" | HIGH | Run longer, add VR | statistical_checks_guide.md |
| "no photon production" | MEDIUM | Check if photons needed | warning_catalog.md §2 |
| "deprecated syntax" | LOW | Note for future update | warning_catalog.md §14 |
| "particles killed by WW" | LOW (<100) | Acceptable, monitor | warning_catalog.md §16 |
| "particles killed by WW" | HIGH (>1000) | Fix weight windows | warning_catalog.md §16 |
| "IEEE inexact trapped" | LOW | Usually harmless | warning_catalog.md §18 |

## Use Case 1: Statistical Checks Failed

**Scenario:** Tally shows failed statistical checks requiring evaluation.

**Warning Message:**
\`\`\`
the tally in the tally fluctuation chart bin did not pass 3 of the 10 statistical checks.
\`\`\`

**Tally Fluctuation Chart:**
\`\`\`
 statistical checks
     1 passed  ✓
     2 passed  ✓
     3 passed  ✓
     4 missed  ✗  ← Relative error not decreasing in second half
     5 passed  ✓
     6 passed  ✓
     7 missed  ✗  ← Variance of variance (VOV) > 0.10
     8 passed  ✓
     9 missed  ✗  ← VOV not decreasing in second half
    10 passed  ✓
\`\`\`

**Interpretation:**
- **3 checks missed** (4, 7, 9) → Poor, must improve
- Checks 4, 9: Convergence issues
- Check 7: VOV > 0.10 (rare large events)

**Fix:**
\`\`\`
c Run much longer
NPS  5e6                              $ Was 5e5, increase 10×

c Or add variance reduction
WWG  4  0  1.0                        $ Generate weight windows for F4
\`\`\`

**Verification:** Re-run and check that ≤2 checks fail (preferably 0)

**Detailed Guide:** See \`statistical_checks_guide.md\`

## Use Case 2: Shannon Entropy Not Converged

**Scenario:** Criticality calculation with unconverged fission source.

**Warning Message:**
\`\`\`
the kcode Shannon entropy appears not to be converged.
\`\`\`

**Problem:** Entropy increasing through inactive cycles → source not converged → keff unreliable

**Fix:**
\`\`\`
c Original:
KCODE  10000  1.0  50  150           $ 50 inactive

c Increase inactive cycles:
KCODE  10000  1.0  100  200          $ 100 inactive
\`\`\`

**Verification:** Entropy must be flat (±5%) in final 30% of inactive cycles

**Key Point:** CRITICAL - keff invalid if source not converged

## Use Case 3: Material Unnormalized Fractions

**Scenario:** Material fractions don't sum exactly.

**Warning Message:**
\`\`\`
warning.  1 materials had unnormalized fractions. print table 40.
\`\`\`

**Input:**
\`\`\`
M1  1001.80c  2.1  8016.80c  1.0    $ Should be 2:1
\`\`\`

**Evaluation:**
- Check Table 40 for normalized values
- <1% difference: Acceptable but fix recommended
- >5% difference: Must fix and re-run

**Fix:**
\`\`\`
M1  1001.80c  2.0  8016.80c  1.0    $ Exact 2:1 ratio
\`\`\`

## Use Case 4: Large Relative Error

**Scenario:** Tally uncertainty too high.

**Warning Message:**
\`\`\`
warning.  tally 14 has a relative error greater than 0.50.
\`\`\`

**Result:** 58.5% error → meaningless

**Fix:**
\`\`\`
c Run much longer
NPS  1e8                              $ 100× increase

c Or add variance reduction
WWG  14  0  1.0
\`\`\`

**Target:** Error <10% (preferably <5%)

## Integration with Other Skills

### 1. mcnp-statistics-checker
Validates tally quality per warning-analyzer criteria.

### 2. mcnp-fatal-error-debugger
Some warnings escalate to fatal errors if ignored.

### 3. mcnp-output-parser
Extracts warnings for systematic analysis.

### 4. mcnp-variance-reducer
Optimizes to eliminate statistical warnings.

### 5. mcnp-criticality-analyzer
Handles KCODE convergence warnings specifically.

### 6. mcnp-material-builder
Prevents material warnings at input creation.

## References

### Comprehensive Warning Guides
- **warning_catalog.md:** Complete catalog of 22+ warning types by category
- **statistical_checks_guide.md:** Detailed explanation of 10 statistical quality checks

### Python Scripts
- **scripts/README.md:** Script documentation and usage
- **scripts/mcnp_warning_analyzer.py:** Automated warning extraction and categorization

### MCNP Documentation
- Chapter 4 §4.7: Input Error Messages
- Chapter 2: Monte Carlo Statistics

## Best Practices

1. **Prioritize Statistical Warnings:** Never use results with >2 checks failed
2. **Verify KCODE Convergence:** Entropy must be flat before trusting keff
3. **Document Warning Resolution:** Track what warnings mean for your problem
4. **Set Realistic Goals:** <1% (academic), <5% (engineering), <10% (screening)
5. **Material Warnings Require Judgment:** <1% OK, >5% must fix
6. **Trend Analysis:** Watch warnings across runs to verify improvement
7. **Deprecation Warnings:** Plan updates but code still works
8. **Statistical Checks First:** Most important for result validity
9. **Use Warnings to Guide Optimization:** Statistical → VR, Entropy → inactive cycles
10. **Context Matters:** Some warnings expected (e.g., MODE N → photon warnings OK)

## Validation Checklist

- [ ] ≤2 statistical checks failed per tally (preferably 0)
- [ ] Relative error <10% (preferably <5%)
- [ ] FOM stable or increasing
- [ ] Shannon entropy flat if KCODE (±5% in final 30% inactive)
- [ ] Keff stable (no trend in active cycles)
- [ ] Material warnings documented and acceptable
- [ ] Physics warnings expected for MODE or fixed
- [ ] Deprecation warnings noted for future

---

**END OF MCNP WARNING ANALYZER SKILL**

For detailed information, consult the reference files listed above.
