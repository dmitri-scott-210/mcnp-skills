# MCNP Warning Catalog

**Purpose:** Comprehensive catalog of MCNP warning messages, their meanings, severity, and resolution.

**Companion to:** mcnp-warning-analyzer SKILL.md

---

## Warning Severity Classification

### Critical (Action Required)
- Statistical checks failed (>2 of 10 checks missed)
- Source convergence not achieved (KCODE Shannon entropy)
- Tally relative error >10%
- Material normalization causing physics errors

### Important (Should Investigate)
- Missing thermal scattering for thermal neutrons
- Physics warnings affecting simulation scope
- Moderate statistical issues (1-2 checks missed)
- Energy cutoffs reached frequently
- Material composition discrepancies

### Informational (Generally Safe)
- Deprecation notices (code still works)
- IEEE exceptions that completed without crash
- Minor normalization adjustments <1%
- Comment messages

---

## Material Warnings

### 1. Unnormalized Material Fractions

**Message:**
```
warning.  1 materials had unnormalized fractions. print table 40.
```

**Cause:** Material fractions don't sum to 1.0 (atomic) or expected total

**Example:**
```
M1  1001.80c  2.1  8016.80c  1.0    $ Sum = 3.1 (H2O should be 2:1)
```

**Evaluation:**
- Check Table 40 in output for normalized values
- Compare MCNP normalization to intent
- Small difference (<1%): Likely rounding
- Large difference (>5%): Wrong composition

**Fix:**
```
M1  1001.80c  2.0  8016.80c  1.0    $ Exact 2:1 ratio
```

**Severity:** Low-Medium (depends on difference magnitude)

### 2. No Photon Production Cross Sections

**Message:**
```
warning.  photon production cross sections do not exist for nuclide 92235.
```

**Context:** MODE N P (coupled neutron-photon transport)

**Evaluation:**
- Is photon production important for this problem?
- If calculating photon dose → YES, critical
- If only neutron transport → NO, can use MODE N

**Fix Option 1** (Photons not needed):
```
MODE  N                               $ Change to neutron only
```

**Fix Option 2** (Photons needed):
```
c Accept limitation or use different ZAID
c Document that photons from some reactions excluded
```

**Severity:** Medium (context-dependent)

### 3. Missing Thermal Scattering Data

**Message:**
```
warning.  thermal scattering not used for nuclide 1001.
```

**Cause:** No MT (thermal scattering law) card for low-energy neutrons

**Example Problem:**
```
M1  1001.80c  2  8016.80c  1         $ Water, but no MT card
```

**Fix:**
```
M1  1001.80c  2  8016.80c  1
MT1  LWTR.20t                         $ Light water thermal scattering
```

**Severity:** Important (for thermal neutron problems)

### 4. ZAID Substitution

**Message:**
```
warning.  nuclide 92235.80c not found. using 92235.70c instead.
```

**Cause:** Requested library not available, MCNP substituted different version

**Evaluation:**
- Check if substitution appropriate for problem
- Library version differences usually small
- Document which library actually used

**Action:**
```
c Document in input:
c NOTE: Using ENDF/B-VII.0 (requested .80c not available)
```

**Severity:** Low (document for reproducibility)

---

## Statistical Warnings

### 5. Statistical Checks Failed

**Message:**
```
the tally in the tally fluctuation chart bin did not pass 3 of the 10 statistical checks.
```

**Cause:** Tally does not meet MCNP's reliability criteria

**Interpretation by Failed Count:**
- **0 failed:** Excellent (all checks passed)
- **1-2 failed:** Marginal (investigate, may be acceptable)
- **3-5 failed:** Poor (extend run, improve VR)
- **6+ failed:** Unreliable (results not trustworthy)

**Common Failed Checks:**
- **Check 4:** Relative error not decreasing in second half
- **Check 7:** Variance of variance (VOV) > 0.10
- **Check 9:** VOV not decreasing in second half

**Fix:**
```
c Option 1: Run longer
NPS  5e6                              $ Increase from 5e5

c Option 2: Improve variance reduction
WWG  4  0  1.0                        $ Generate weight windows

c Option 3: Check tally setup
c - Is tally in reasonable location?
c - Are energy bins too fine?
```

**Severity:** High (if ≥3 checks failed)

### 6. Large Relative Error

**Message:**
```
warning.  tally 14 has a relative error greater than 0.50.
```

**Interpretation:**
- Error >50%: Result meaningless
- Error >10%: Unreliable
- Error 5-10%: Marginal
- Error <5%: Acceptable
- Error <1%: Excellent

**Fix:**
```
c Run much longer
NPS  1e8                              $ 100x increase

c Or add variance reduction
WWG  14  0  1.0
```

**Severity:** High (results unreliable)

### 7. Zero Tally Result

**Message:**
```
warning.  tally 6 has zero results.
```

**Causes:**
- Tally in impossible location
- Particle type doesn't reach tally
- Energy range mismatch
- Geometry error

**Diagnostic:**
```
c Check tally definition:
F6:N  25                              $ Is cell 25 accessible?

c Check if particles reach region:
c - Plot geometry at tally location
c - Verify importance IMP:N > 0
c - Check energy range reasonable
```

**Fix:** Correct tally location or check geometry

**Severity:** High (indicates setup problem)

---

## Convergence Warnings (Criticality)

### 8. Shannon Entropy Not Converged

**Message:**
```
the kcode Shannon entropy appears not to be converged.
```

**Cause:** Fission source distribution still evolving during inactive cycles

**Entropy Pattern Problems:**
- **Continuous rise:** Source never converges (need more inactive cycles)
- **Oscillation:** Source alternating between regions
- **Late jump:** Source found new region late in inactive cycles

**Fix:**
```
c Original:
KCODE  10000  1.0  50  150           $ 50 inactive, 100 active

c Increase inactive cycles:
KCODE  10000  1.0  100  200          $ 100 inactive, 100 active

c Or better initial source:
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0  $ Multiple points
```

**Severity:** Critical (keff results unreliable if source not converged)

### 9. Keff Trending

**Message:**
```
warning.  the estimated keff trend is statistically significant.
```

**Cause:** keff still changing systematically during active cycles

**Interpretation:**
- Upward trend: Source still spreading or inactive cycles insufficient
- Downward trend: Source concentrating or sampling issue
- Either trend: Active cycle keff unreliable

**Fix:**
```
c More inactive cycles
KCODE  10000  1.0  150  250          $ Increase from 100 to 150 inactive
```

**Severity:** Critical (biases keff result)

### 10. Insufficient Cycles for Confidence Intervals

**Message:**
```
warning.  only N cycles available for confidence intervals.
```

**Cause:** Too few active cycles for meaningful statistics

**Fix:**
```
KCODE  10000  1.0  100  300          $ Need many active cycles (≥100)
```

**Severity:** Important (affects confidence intervals)

---

## Physics Warnings

### 11. Physics Model Disabled

**Message:**
```
warning.  photonuclear physics disabled for MODE N P.
```

**Cause:** Physics option not available or not enabled

**Evaluation:**
- Is this physics important for problem?
- Photonuclear usually minor for most problems
- Document if intentional limitation

**Action:**
```
c Document limitation:
c NOTE: Photonuclear reactions not modeled (negligible for this application)
```

**Severity:** Low (context-dependent)

### 12. Energy Cutoff Reached

**Message:**
```
warning.  N particles reached energy cutoff.
```

**Cause:** Particles down-scattered below PHYS:N energy cutoff

**Evaluation:**
```
PHYS:N  20                            $ 20 MeV cutoff

c Check:
c - Is cutoff appropriate for problem?
c - If thermal neutrons important, cutoff too high
c - If only fast neutrons, cutoff appropriate
```

**Fix if Needed:**
```
PHYS:N  0.001                         $ Lower cutoff for thermal problems
```

**Severity:** Medium (may bias results if cutoff inappropriate)

### 13. Particle Production Threshold

**Message:**
```
warning.  photon production below threshold not modeled.
```

**Cause:** PHYS card energy threshold excludes some photon production

**Evaluation:**
- Check if low-energy photons important
- For shielding: often important
- For fast neutron physics: often negligible

**Fix:**
```
PHYS:P  0.001  0  0  0  0  0  J  J  1  $ Lower photon production threshold
```

**Severity:** Medium (context-dependent)

---

## Deprecation Warnings

### 14. Obsolete Card Syntax

**Message:**
```
warning.  the DBCN card is obsolete. use the RAND card instead.
```

**Old:**
```
DBCN  12345  0  0  1  13  19073486328125
```

**Modern:**
```
RAND  GEN=1  SEED=19073486328125  HIST=1  STRIDE=152917
```

**Action:**
- Immediate: No action required (still works)
- Future: Update to modern syntax when revising input

**Severity:** Low (informational)

### 15. Legacy Parameter Format

**Message:**
```
warning.  old-style parameter format detected.
```

**Action:**
- Note for future update
- Code continues to work
- Plan migration when convenient

**Severity:** Low

---

## Weight Window Warnings

### 16. Particles Killed by Weight Window

**Message:**
```
warning.  N particles were killed by the weight window.
```

**Evaluation:**
- <100 particles (<0.01%): Acceptable
- 100-1000 (0.01-0.1%): Monitor
- >1000 (>0.1%): Problem with weight windows

**Fix if Significant:**
```
c Widen weight window bounds:
WWP:N  10  5  10  0  0               $ Increase wupn parameter

c Or regenerate weight windows:
NPS  1e6                              $ Longer statistics
WWG  5  0  1.0
```

**Severity:** Low (<1% killed), High (>1% killed)

### 17. Weight Window Mesh Issues

**Message:**
```
warning.  weight window mesh does not cover geometry.
```

**Cause:** WWGE mesh bounds don't encompass problem geometry

**Fix:**
```
c Extend mesh to cover geometry:
WWGE:N  -200  200  20                $ Extend X range
        -200  200  20                $ Extend Y range
        -200  200  20                $ Extend Z range
```

**Severity:** Important (VR ineffective or causing errors)

---

## IEEE Exception Warnings

### 18. Floating Point Exceptions

**Message:**
```
ieee_flags: Warning: hardware overflow trapped N times.
ieee_flags: Warning: hardware inexact trapped M times.
```

**Exception Types:**
- **Inexact:** Very common, harmless (e.g., 2/3 = 0.66666...)
- **Underflow:** Number near zero, usually harmless
- **Overflow:** Number too large, investigate if many
- **Divide by zero:** Investigate source

**Evaluation:**
- Inexact: Always acceptable (millions common)
- <100 others: Usually benign
- >10,000 overflow/divide: Investigate input values

**Action if Excessive:**
```
c Check for unreasonable values:
c - Source energy: ERG=1e20 (too large?)
c - Cell importance: IMP:N=1e10 (too large?)
c - Cell volume: VOL=1e-30 (too small?)
```

**Severity:** Low (if run completes), Medium (if excessive)

---

## Performance Warnings

### 19. Large Number of Surfaces

**Message:**
```
warning.  geometry contains N surfaces (performance may be slow).
```

**Interpretation:**
- >10,000 surfaces: Expect slower performance
- >100,000 surfaces: Significant performance impact

**Action:**
- Accept slower performance if geometry necessary
- Consider simplifying if possible
- Use appropriate cell importance to avoid tracking in complex regions

**Severity:** Informational

### 20. Cell Importance Span

**Message:**
```
warning.  cell importance ratio spans N orders of magnitude.
```

**Interpretation:**
- Large span (>6 orders): May cause particle weight issues
- Extreme importance biasing can cause splitting problems

**Action:**
- Review importance map reasonability
- Consider more gradual importance progression

**Severity:** Low (monitor particle population)

---

## Tally-Specific Warnings

### 21. Tally Segment Boundary Issues

**Message:**
```
warning.  tally segment boundaries may not align with geometry.
```

**Cause:** Energy or time bins don't match physics well

**Action:**
- Review bin structure reasonableness
- Ensure bins span range of interest
- Check for extremely fine bins

**Severity:** Low

### 22. Point Detector Too Close to Surface

**Message:**
```
warning.  F5 detector within surface tolerance.
```

**Cause:** Point detector positioned very close to surface

**Action:**
```
c Move detector slightly away from surface:
F5:N  10.01 0 0  1                   $ Was 10.00 (on surface)
```

**Severity:** Medium (may cause numerical issues)

---

## Quick Reference: Action Priority Matrix

| Warning Type | Rel. Error | Checks Failed | Action Priority |
|--------------|-----------|---------------|-----------------|
| Statistical | Any | 6-10 failed | CRITICAL - Extend run |
| Statistical | >10% | 3-5 failed | HIGH - Improve VR or extend |
| Statistical | 5-10% | 1-2 failed | MEDIUM - Monitor trend |
| Statistical | <5% | 0 failed | OK - Acceptable |
| Convergence (KCODE) | Any | Entropy not flat | CRITICAL - More inactive |
| Material | >5% diff | N/A | HIGH - Fix composition |
| Material | <5% diff | N/A | LOW - Document intent |
| Physics | Context | N/A | MEDIUM - Verify appropriate |
| Deprecation | N/A | N/A | LOW - Plan future update |
| IEEE | >10k events | N/A | MEDIUM - Check input |
| IEEE | <100 events | N/A | LOW - Usually harmless |

---

## Warning Correlation Patterns

### Pattern 1: Material + Statistical
```
Warning: Material 5 unnormalized
Warning: Tally 14 failed 8 checks

Analysis: Material 5 used in cell with tally 14
Conclusion: Material error affecting physics
Action: Fix material normalization first
```

### Pattern 2: Entropy + Keff Trend
```
Warning: Shannon entropy not converged
Warning: Keff trending upward

Analysis: Source still evolving
Conclusion: Inactive cycles insufficient
Action: Double inactive cycles
```

### Pattern 3: Weight Window + Zero Tally
```
Warning: 5000 particles killed by WW
Warning: Tally 6 has zero results

Analysis: WW preventing particles from reaching tally
Conclusion: WW setup error
Action: Regenerate WW or adjust mesh
```

---

## References

- **statistical_checks_guide.md:** Detailed explanation of 10 statistical checks
- **convergence_warnings.md:** KCODE-specific convergence issues
- **warning_resolution_workflow.md:** Systematic resolution procedures
- **MCNP Manual Chapter 4.7:** Input Error Messages (includes warnings)
- **MCNP Manual Chapter 2:** Monte Carlo Statistics

---

**END OF WARNING CATALOG**
