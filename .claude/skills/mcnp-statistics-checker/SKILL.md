---
name: "MCNP Statistics Checker"
description: "Validates MCNP tally statistical quality using the 10 statistical checks. Ensures results are reliable before use. Use when verifying simulation convergence."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Statistics Checker

## Overview

When a user needs to verify whether MCNP simulation results are statistically reliable, use this skill to comprehensively validate tally quality using MCNP's 10 statistical checks.

**Critical principle:** A result can have a small relative error but still be completely unreliable if statistical quality checks fail. This skill prevents users from trusting incorrect results.

This skill validates:
- **10 statistical quality checks** (Table 2.2, Chapter 2.6.9)
- Tally fluctuation chart trends
- Figure of Merit (FOM) stability
- Variance of Variance (VOV) behavior
- Mean convergence and stability
- Central Limit Theorem compliance
- History contribution balance

And provides:
- Clear pass/fail assessment for each check
- Physical interpretation of failures
- Specific recommendations to improve quality
- Estimates of required histories
- Production run readiness assessment

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User asks if results are "reliable", "converged", or "trustworthy"
- User mentions "statistical checks", "TFC", or "tally fluctuation chart"
- User asks "how many histories do I need?"
- User reports simulation results without mentioning statistics
- User says "my tally has high uncertainty"
- User asks about "VOV", "FOM", or "figure of merit"
- User is preparing for production runs
- User mentions "the 10 checks" or "10/10"
- **Phase 3:** User asks about VR quality or effectiveness
- **Phase 3:** User wants to validate weight windows
- **Phase 3:** User mentions overbiasing concerns

**Context Clues:**
- "Can I use these results?"
- "Should I run longer?"
- "Why is my error so high?"
- "The checks aren't all passing..."
- "Is my variance reduction working?"
- **Phase 3:** "Are my weight windows causing problems?"
- **Phase 3:** "Low error but checks fail - why?"
- **Phase 3:** "Is my WWG converged?"

### Validation Approach Decision Tree

**Step 1: Determine Scope**

```
User request → Select validation scope:
├── Single tally → Focus on one tally's 10 checks
├── All tallies → Validate all tallies, compare quality
├── Specific check → Deep dive into one failed check
├── Convergence trend → Analyze evolution over run
└── Production readiness → Comprehensive assessment
```

**Step 2: Assessment Depth**

```
Quick check (test run):
├── Read "passed m/10" message from output
├── Quick pass/fail per tally
└── Basic recommendation

Comprehensive validation (production):
├── All 10 checks analyzed individually
├── Tally fluctuation chart trends
├── Failed check interpretation
├── Specific recommendations
├── History requirement estimates
└── Convergence predictions

Diagnostic analysis (persistent problems):
├── Plot mean vs NPS trends
├── Analyze FOM evolution
├── Check for systematic issues
├── Compare to benchmark
└── Review variance reduction setup

Phase 3 - VR quality validation:
├── FOM stability assessment (±10% threshold)
├── Weight distribution analysis (ratio, top-N contrib)
├── Mean vs analog comparison (bias detection)
├── WWG iteration convergence tracking
├── VR-specific quality score (0-100)
└── Overbiasing artifact detection
```

## Tool Invocation

This skill includes a Python implementation for automated statistical quality validation.

### Importing the Tool

```python
from mcnp_statistics_checker import MCNPStatisticsChecker

# Initialize the checker
checker = MCNPStatisticsChecker()
```

### Basic Usage

**Check All Tallies in Output File**:
```python
# Validate all tallies
tally_results = checker.check_all_tallies('path/to/outp')

# Review results for each tally
for tally_num, result in tally_results.items():
    passed = result['all_passed']
    checks = result['checks']
    fom = result['fom']

    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"Tally {tally_num}: {status}")
    print(f"  Checks: {checks}")
    print(f"  FOM: {fom}")
```

**Get Failed Checks Only**:
```python
# Find only tallies with failures
failed = checker.get_failed_checks('outp')

if failed:
    print("❌ FAILED STATISTICAL CHECKS:")
    for tally_num, check_list in failed.items():
        print(f"\n  Tally {tally_num}:")
        for check_name in check_list:
            print(f"    • Failed: {check_name}")
else:
    print("✓ All tallies passed statistical checks")
```

**Get Improvement Recommendations**:
```python
# Get specific recommendations for failed checks
recommendations = checker.recommend_improvements('outp')

if recommendations:
    print("💡 RECOMMENDATIONS:")
    for rec in recommendations:
        tally = rec['tally']
        issue = rec['issue']
        suggestions = rec['suggestions']

        print(f"\n  Tally {tally}: {issue}")
        for suggestion in suggestions:
            print(f"    → {suggestion}")
else:
    print("✓ No improvements needed - all checks passed")
```

### Integration with MCNP Workflow

```python
from mcnp_statistics_checker import MCNPStatisticsChecker

def validate_simulation_quality(output_file, target_error=0.05):
    """Complete statistical quality validation workflow"""
    print(f"Validating statistical quality: {output_file}")
    print("=" * 60)

    checker = MCNPStatisticsChecker()

    # Check all tallies
    tally_results = checker.check_all_tallies(output_file)

    # Categorize results
    passed_all = []
    passed_some = []
    failed_badly = []

    for tally_num, result in tally_results.items():
        checks = result['checks']
        if not checks:
            continue

        passed_count = sum(1 for v in checks.values() if v)
        total_count = len(checks)

        if passed_count == total_count:
            passed_all.append(tally_num)
        elif passed_count >= total_count * 0.7:  # ≥70%
            passed_some.append(tally_num)
        else:
            failed_badly.append(tally_num)

    # Report summary
    print(f"\n📊 SUMMARY:")
    print(f"  ✓ Excellent (10/10): {len(passed_all)} tallies")
    print(f"  ⚠ Marginal (7-9/10): {len(passed_some)} tallies")
    print(f"  ✗ Poor (≤6/10):      {len(failed_badly)} tallies")

    # Report excellent tallies
    if passed_all:
        print(f"\n✓ EXCELLENT QUALITY:")
        for tally in passed_all:
            fom = tally_results[tally]['fom']
            print(f"  Tally {tally}: All checks passed (FOM: {fom})")

    # Report marginal tallies
    if passed_some:
        print(f"\n⚠ MARGINAL QUALITY (review needed):")
        failed_checks = checker.get_failed_checks(output_file)
        for tally in passed_some:
            checks_failed = failed_checks.get(tally, [])
            print(f"  Tally {tally}: Failed {len(checks_failed)} checks")
            for check in checks_failed:
                print(f"    • {check}")

    # Report poor tallies
    if failed_badly:
        print(f"\n✗ POOR QUALITY (DO NOT USE):")
        for tally in failed_badly:
            checks = tally_results[tally]['checks']
            passed = sum(1 for v in checks.values() if v)
            total = len(checks)
            print(f"  Tally {tally}: Only {passed}/{total} checks passed")

    # Get recommendations
    recommendations = checker.recommend_improvements(output_file)
    if recommendations:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"\n  Tally {rec['tally']}: {rec['issue']}")
            for suggestion in rec['suggestions']:
                print(f"    → {suggestion}")

    # Production readiness assessment
    print("\n" + "=" * 60)
    if failed_badly:
        print("✗ NOT READY FOR PRODUCTION")
        print("  Fix tallies with ≤6/10 checks before using results")
        return False
    elif passed_some:
        print("⚠ MARGINAL - USE WITH CAUTION")
        print("  Consider running longer for marginal tallies")
        return True
    else:
        print("✓ READY FOR PRODUCTION")
        print("  All tallies meet quality standards")
        return True

# Example usage
if __name__ == "__main__":
    import sys
    output_file = sys.argv[1] if len(sys.argv) > 1 else "outp"

    if validate_simulation_quality(output_file):
        print("\nResults can be used for analysis")
    else:
        print("\nRun longer or improve variance reduction")
```

---

## The 10 Statistical Quality Checks

### Overview (Chapter 2.6.9, Table 2.2)

MCNP tests every tally against **10 criteria** to assess statistical reliability. These appear in output as:

```
tally 4 passed 10 of 10 statistical checks
```

**Quality interpretation:**
- **10/10 passed**: EXCELLENT - results fully reliable
- **9/10 passed**: GOOD - review which check failed, likely okay
- **7-8/10 passed**: MARGINAL - use with caution, need more histories
- **≤6/10 passed**: POOR - results unreliable, do NOT use
- **≤5/10 passed**: UNACCEPTABLE - completely untrustworthy

**Critical rule:** ALL 10 checks must pass for production calculations.

### Check 1: Mean Behavior

**What it tests:** The estimated mean should vary randomly about the final value, not trend systematically.

**Pass criterion:** Mean exhibits random walk behavior around converged value in last 50% of histories.

**Physical meaning:** If mean is still drifting up or down, the tally hasn't converged yet.

**Common failure causes:**
- Insufficient histories (mean still finding true value)
- KCODE source not converged (fission source still shifting)
- Weight windows still adapting (WWG method)
- Systematic geometry error (lost particles changing distribution)

**How to fix:**
- Run more histories (at least 2× current)
- KCODE: Increase KSRC skip cycles
- Fixed source: Let weight windows stabilize before tallying
- Check for lost particles or geometry errors

**Example failure:**
```
NPS       Mean
10000     2.45E-04  ← trending up
20000     2.67E-04  ← still rising
50000     2.89E-04  ← not stable
100000    3.01E-04  ← systematic drift = FAIL
```

### Check 2: Relative Error Decreasing Monotonically

**What it tests:** Relative error should decrease smoothly with increasing histories.

**Pass criterion:** R(N) ≤ R(N/2) for all history checkpoints.

**Physical meaning:** As you run more histories, uncertainty should only get smaller, never larger.

**Common failure causes:**
- Too few histories to establish trend
- Rare large contributions causing jumps
- Variance reduction changing efficiency
- Statistical fluctuation in early run

**How to fix:**
- Run much longer (10× current histories)
- Smooth out early fluctuations by discarding initial cycles
- Improve variance reduction stability

**Example failure:**
```
NPS       Rel Error
10000     0.15      ← starting value
20000     0.11      ← decreasing ✓
50000     0.08      ← decreasing ✓
100000    0.09      ← increased! = FAIL
```

### Check 3: Relative Error < 0.10

**What it tests:** Final relative error is acceptably small.

**Pass criterion:** R < 0.10 (10%)

**Physical meaning:** Uncertainty should be small enough for the result to be useful.

**Quality guidelines:**
- R < 0.02 (2%): **EXCELLENT** - benchmark quality
- R < 0.05 (5%): **VERY GOOD** - production quality
- R < 0.10 (10%): **ACCEPTABLE** - minimum for production
- R = 0.10 - 0.20: **MARGINAL** - use with extreme caution
- R > 0.20 (20%): **POOR** - unreliable, order-of-magnitude estimate only
- R > 0.50 (50%): **UNACCEPTABLE** - meaningless

**Common failure causes:**
- Insufficient histories
- Poor tally placement (low importance region)
- Ineffective variance reduction
- Intrinsically difficult tally (deep penetration, rare event)

**How to fix:**
- Run more histories: N_new = N_current × (R_current / R_target)²
- Improve variance reduction (importance, weight windows)
- Relocate tally to higher-flux region
- Use different tally type (F5 → F4, detector → track-length)

**Example:**
To reduce R from 0.15 to 0.05:
  N_new = N_current × (0.15 / 0.05)² = N_current × 9

**Need 9× more histories**

### Check 4: Relative Error vs N Behavior

**What it tests:** Relative error should decrease as 1/√N (statistical law).

**Pass criterion:** Log-log plot of R vs N has slope ≈ -0.5

**Physical meaning:** This is the fundamental law of statistics. If it's not true, something is fundamentally wrong.

**Common failure causes:**
- Not enough history range to establish slope
- Variance reduction still adapting (changing efficiency)
- Non-random sampling (systematic bias)
- Source convergence issues (KCODE)

**How to fix:**
- Run over wider history range (more checkpoints)
- Stabilize variance reduction before analyzing
- Check for systematic errors in setup

**Theory:** For N independent samples, σ_mean = σ / √N, so R ∝ 1/√N

### Check 5: Figure of Merit (FOM) Constant

**What it tests:** FOM = 1/(R²×T) should remain approximately constant.

**Pass criterion:** FOM doesn't vary by more than factor of 3 over last 50% of run.

**Physical meaning:** FOM measures tally efficiency (inverse of computational cost to achieve given uncertainty). It should be constant if variance reduction is stable.

**Formula:** FOM = 1 / (R² × T)
- R = relative error
- T = computer time (minutes)

**Interpretation:**
- FOM increasing: Variance reduction improving (good!)
- FOM constant: Stable, efficient sampling
- FOM decreasing: Efficiency degrading (bad!)
- FOM varying wildly: Unstable variance reduction

**Common failure causes:**
- Weight window parameters adapting (WWG method)
- Importance values changing
- Source distribution shifting (KCODE)
- Variance reduction poorly tuned

**How to fix:**
- WWG: Let generator stabilize, then lock parameters
- Importance: Verify values correct for geometry
- KCODE: Increase skip cycles
- Consider regenerating weight windows

**Good FOM values:** Higher is better, but absolute value depends on problem
- FOM > 1000: Excellent efficiency
- FOM = 100-1000: Good
- FOM = 10-100: Acceptable
- FOM < 10: Poor (need better VR)

### Check 6: PDF Normality (Relative Error vs FOM)

**What it tests:** The probability distribution of history scores should be normal (Gaussian).

**Pass criterion:** PDF of tally scores fits normal distribution.

**Physical meaning:** Central Limit Theorem says sum of many random variables is normal. If not normal, CLT doesn't apply.

**Common failure causes:**
- Few histories with very large contributions
- Rare events dominating tally
- Point detector with infrequent contributions
- Non-analog tallies with large weights

**How to fix:**
- Improve variance reduction to reduce score variance
- Relocate detector to region with more contributions
- Use track-length estimator instead of detector (F4 vs F5)
- Run many more histories to approach CLT limit

**Visual check:** MCNP plots PDF in output - should be bell-shaped and centered.

### Check 7: Largest History Score < 50% of Tally

**What it tests:** No single particle history contributes more than half the total tally.

**Pass criterion:** max(score_i) / total_score < 0.5

**Physical meaning:** If one history dominates, statistics break down - not a statistical sample.

**Common failure causes:**
- Rare event with huge weight (e.g., scattered particle reaching detector)
- Point detector in low-probability region
- Excessive weight window lower bound
- Importance sampling creating very high-weight particles

**How to fix:**
- Improve variance reduction to smooth contributions
- Reduce weight window lower bound ratio (default 0.25 may be too high)
- Relocate detector closer to source/flux
- Use cutoff cards to limit maximum weights

**Example failure:**
```
Total tally: 1.23E-04
Largest history contribution: 8.45E-05 (69% of total) = FAIL
```

### Check 8: Largest History Score < 80% of Tally (Stricter)

**What it tests:** Same as Check 7, but more stringent limit.

**Pass criterion:** max(score_i) / total_score < 0.8

**Physical meaning:** Even 80% from one history indicates poor sampling.

**This check can fail while Check 7 passes:** Indicates significant but not catastrophic dominance.

**Typical scenario:**
- Check 7 passes (largest < 50%)
- Check 8 fails (largest > 80%) - impossible, so this means >50% but <80%
- Usually indicates: largest contribution is 50-80% of total

**How to fix:** Same as Check 7, but less urgent if only Check 8 fails.

### Check 9: Variance of Variance (VOV) < 0.1

**What it tests:** The variance of the estimated variance should be small.

**Pass criterion:** VOV < 0.10

**Physical meaning:** The variance estimate itself should be stable. High VOV means you don't even know the uncertainty accurately.

**Formula:** VOV = S_x² / (x̄² × N)
- S_x² = sample variance of scores
- x̄ = mean score
- N = number of histories

**Quality levels:**
- VOV < 0.01: Excellent
- VOV = 0.01 - 0.05: Very good
- VOV = 0.05 - 0.10: Acceptable
- VOV > 0.10: Poor (high variance in variance)
- VOV > 0.50: Unacceptable

**Common failure causes:**
- Large fluctuations in history scores
- Few histories contributing most of tally
- Non-central limit theorem behavior
- Fundamental sampling problem

**How to fix:**
- Run many more histories (VOV decreases slowly)
- Improve variance reduction dramatically
- Change tally type or location
- May need fundamentally different approach

**Critical importance:** VOV is often the most revealing check. High VOV indicates fundamental convergence problems.

### Check 10: Slope of Largest 201 Bins

**What it tests:** The slope of the largest history scores (on log-log plot) should be ≈ 3.0.

**Pass criterion:** Slope fits theoretical value from Central Limit Theorem.

**Physical meaning:** For normally distributed samples, the tail of the distribution has specific shape characterized by slope = 3.0.

**Acceptable range:** Typically 3.0 ± 1.5 (between 1.5 and 4.5)

**Common failure causes:**
- Too few histories to establish tail distribution
- Non-normal distribution (violates CLT)
- Sampling issues preventing CLT convergence

**How to fix:**
- Run more histories (need many samples in tail)
- Address other failed checks first
- This check often passes once others do

**Theory:** For Gaussian distribution, P(|x| > nσ) decreases as exp(-n²/2), giving characteristic slope.

## Analysis Procedures

### Step 1: Initial Assessment

**Ask user for context:**
- "Which output file should I analyze?" (get file path)
- "Which tallies need validation?" (specific numbers or all)
- "Is this a production run or test?" (sets standards)
- "Are you seeing specific problems?" (failing checks, high errors)
- "What's your target relative error?" (default: <10%, production: <5%)

### Step 2: Read Reference Materials

**MANDATORY - READ ENTIRE FILE**: Before performing validation, read:
- `.claude/commands/mcnp-statistics-checker.md` - Complete validation procedures
- If needed: `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Statistical quality section

### Step 3: Extract Statistical Data

Use the Python module:

```python
from skills.output_analysis.mcnp_statistics_checker import MCNPStatisticsChecker

checker = MCNPStatisticsChecker()

# Check all tallies
all_stats = checker.check_all_tallies('output.o')

# Results structure:
# {
#     tally_num: {
#         'all_passed': boolean,
#         'checks': {
#             'check_1': True/False,
#             'check_2': True/False,
#             ...
#             'check_10': True/False
#         },
#         'fom': value,
#         'rel_error': value,
#         'vov': value,
#         'slope': value
#     },
#     ...
# }

# Get failed checks
failed = checker.get_failed_checks('output.o')

# Get recommendations
recommendations = checker.recommend_improvements('output.o')
```

### Step 4: Analyze Tally Fluctuation Chart

The TFC appears at end of OUTP file for each tally:

```
tally  4
           nps      mean     error   vov  slope    fom
         10000  2.73E-04   0.1234  0.234  1.2   1.2E+02
         20000  2.65E-04   0.0987  0.156  2.1   1.3E+02
         50000  2.71E-04   0.0654  0.078  2.5   1.3E+02
        100000  2.69E-04   0.0432  0.043  2.8   1.4E+02
        200000  2.70E-04   0.0321  0.025  2.9   1.3E+02
        500000  2.70E-04   0.0201  0.012  3.0   1.3E+02

 tally  4 passed 10 of 10 statistical checks
```

**How to read:**
- **nps**: Cumulative particle histories
- **mean**: Tally mean value at this checkpoint
- **error**: Relative error (fractional, not %)
- **vov**: Variance of variance
- **slope**: History score slope (target = 3.0)
- **fom**: Figure of merit (efficiency)

**Healthy trends:**
- Mean: Fluctuates randomly, converges to stable value
- Error: Decreases smoothly and monotonically
- VOV: Decreases toward 0
- Slope: Approaches 3.0 from below or above
- FOM: Remains roughly constant (±factor of 2)

**Unhealthy trends:**
- Mean: Systematically drifting up or down
- Error: Increasing or oscillating
- VOV: Remains high (>0.1) or increasing
- Slope: Far from 3.0 or diverging
- FOM: Decreasing steadily

### Step 5: Interpret Results

**For each tally, categorize:**

```python
def categorize_tally_quality(checks_passed, rel_error, vov):
    """Determine tally reliability category"""

    if checks_passed == 10 and rel_error < 0.05 and vov < 0.05:
        return "EXCELLENT - Production ready"

    elif checks_passed >= 9 and rel_error < 0.10 and vov < 0.10:
        return "GOOD - Acceptable for production"

    elif checks_passed >= 7 and rel_error < 0.15:
        return "MARGINAL - Use with caution, prefer more statistics"

    elif checks_passed >= 5 and rel_error < 0.20:
        return "POOR - Preliminary results only, not reliable"

    else:
        return "UNACCEPTABLE - Do not use, completely unreliable"
```

**Present results clearly:**
```
TALLY 4: EXCELLENT ✓
  Checks: 10/10 passed
  Rel Error: 3.2% (target: <10%)
  VOV: 0.0045 (target: <0.10)
  FOM: 1234.5 (stable)
  Status: Fully reliable for production calculations

TALLY 14: MARGINAL ⚠
  Checks: 7/10 passed (failed: #3, #5, #9)
  Rel Error: 12.5% (target: <10%)
  VOV: 0.156 (target: <0.10)
  FOM: 45.3 (decreasing trend)
  Status: Needs improvement before production use
```

### Step 6: Diagnose Failures

**For each failed check, identify root cause:**

```python
def diagnose_check_failure(check_number, tally_stats):
    """Diagnose why specific check failed"""

    diagnoses = {
        1: {
            'name': 'Mean stability',
            'likely_causes': [
                'Insufficient histories',
                'KCODE source not converged',
                'Weight windows still adapting',
                'Systematic geometry error'
            ],
            'fixes': [
                'Run 2-5× more histories',
                'Increase KCODE skip cycles',
                'Lock weight window parameters',
                'Check for lost particles'
            ]
        },
        2: {
            'name': 'Error decreasing monotonically',
            'likely_causes': [
                'Too few histories',
                'Rare large contributions',
                'Early statistical noise'
            ],
            'fixes': [
                'Run 10× more histories',
                'Improve variance reduction',
                'Discard early cycles'
            ]
        },
        3: {
            'name': 'Relative error < 10%',
            'likely_causes': [
                'Insufficient histories',
                'Poor variance reduction',
                'Difficult tally location'
            ],
            'fixes': [
                f'Run {estimate_needed_histories(tally_stats)} histories',
                'Improve importance or weight windows',
                'Relocate tally to higher-flux region'
            ]
        },
        # ... (continue for all 10 checks)
    }

    return diagnoses.get(check_number, {})
```

### Step 7: Provide Recommendations

**Calculate required histories:**

```python
def estimate_needed_histories(current_nps, current_error, target_error=0.05):
    """Estimate histories needed to achieve target error"""

    # Error decreases as 1/√N
    ratio = current_error / target_error
    needed_nps = current_nps * ratio**2

    return int(needed_nps)

# Example:
current = 100_000
R_current = 0.15
R_target = 0.05

needed = estimate_needed_histories(current, R_current, R_target)
# Result: 900,000 histories (9× more)
```

**Provide actionable advice:**
```
RECOMMENDATIONS FOR TALLY 14:

1. INCREASE HISTORIES (High Priority)
   Current: 100,000 histories, R = 12.5%
   Target: R < 10% (minimum) or R < 5% (preferred)

   To achieve R = 10%: need ~156,000 histories (+56%)
   To achieve R = 5%: need ~625,000 histories (6.25×)

   Action: Increase NPS card to 625000

2. ADDRESS HIGH VOV (Critical)
   Current VOV: 0.156 (should be <0.10)

   This indicates few histories dominating the tally.
   Likely causes:
   - Point detector in low-flux region
   - Poor variance reduction
   - Rare events contributing heavily

   Actions:
   a) Review detector placement (DD card output)
   b) Improve weight windows around detector
   c) Consider using F4 track-length instead of F5 detector

3. STABILIZE FOM (Medium Priority)
   FOM decreasing: 65 → 52 → 45 → 38

   Indicates variance reduction efficiency degrading.

   Actions:
   a) Check importance values in detector region
   b) Verify weight window parameters appropriate
   c) May need to regenerate weight windows

4. PRODUCTION READINESS
   Current status: NOT READY
   Estimated run time to acceptable quality: 6× current time
   Alternative: Redesign tally (F4 instead of F5) may be more efficient

Would you like me to help with any of these improvements?
```

## Common Statistical Problems & Solutions

### Problem 1: "Passed 5/10 checks"

**Diagnosis:** Grossly insufficient histories

**Root cause:** Simulation stopped too early, statistics haven't converged

**Solution:**
1. Continue run to at least 10× current NPS
2. Check which 5 checks failed - if all error-related, just need more histories
3. Monitor convergence - should see checks passing as run continues

**Rule of thumb:** Below 5/10 means need order-of-magnitude more histories

### Problem 2: "FOM steadily decreasing"

**Diagnosis:** Variance reduction efficiency degrading over run

**Root causes:**
- Weight window parameters drifting from optimal
- Importance values incorrect for geometry
- Source distribution shifting (KCODE)

**Solutions:**
1. **WWG method:** Lock weight window parameters after initial adaptation
   - Use UPDATE=0 on WWN card after WWG converges
2. **Manual WW:** Check WW parameters in suspected regions
   - Look for WW values differing by >100× across boundaries
3. **Importance:** Verify IMP values consistent with geometry
   - Detector region should have IMP:N 1, not 0
4. **KCODE:** Increase skip cycles to stabilize fission source

**Verification:** FOM should stabilize after fix

### Problem 3: "VOV > 0.5" (Very High)

**Diagnosis:** Fundamental sampling problem - few histories dominate tally

**Root causes:**
- Point detector with rare direct contributions
- Deep penetration tally with exponential attenuation
- Rare event being tallied (e.g., high-energy scattered photon)

**Solutions:**
1. **Change tally type:**
   - F5 point detector → F4 track-length flux
   - Detector eliminates rare high-weight contributions

2. **Improve variance reduction dramatically:**
   - Use weight windows (WWG card to generate)
   - Use DXTRAN sphere for deep penetration
   - Adjust importance values

3. **Relocate tally:**
   - Move detector closer to source/high-flux region
   - Increase detector volume/area

4. **Accept high VOV and run 100× more histories:**
   - VOV decreases slowly (∝ 1/N, not 1/√N)
   - May be only option for intrinsically difficult tallies

**Warning:** VOV > 0.5 typically requires 100-1000× more histories than VOV < 0.1

### Problem 4: "Mean still drifting after 1M histories"

**Diagnosis:** Source not converged (KCODE) or systematic problem

**Root causes:**
- KCODE: Fission source distribution still evolving
- Fixed source: Geometry error causing lost particles
- Weight windows: Still adapting (WWG method)

**Solutions:**

**For KCODE:**
1. Check KCODE cycle output - is k_eff stable?
2. Increase skip cycles (KSRC): typically 50-200 cycles
3. Look for "source distribution has converged" message
4. Consider longer inactive cycles before tallying

**For fixed source:**
1. Check for "N lost particles" warnings
2. Plot geometry to find gaps/overlaps
3. Verify source definition (SDEF card)
4. Check importance values (IMP cards)

**For WWG:**
1. Lock WW parameters after initial adaptation
2. Use UPDATE=0 on WWN card
3. Verify WW actually improving FOM

**Test:** Mean should stabilize in last 50% of run

### Problem 5: "Error not decreasing - stuck at 20%"

**Diagnosis:** Hitting fundamental efficiency limit of variance reduction

**Root causes:**
- Variance reduction maximally effective already
- Tally location inherently difficult
- No path to improve efficiency further

**Solutions:**
1. **Try different VR technique:**
   - Importance → Weight windows
   - Manual WW → Automatic WWG
   - Add DXTRAN spheres

2. **Reformulate problem:**
   - Different tally location
   - Different tally type (F2 vs F4 vs F5)
   - Mesh tally instead of point tally

3. **Accept limitation and run much longer:**
   - To reduce R from 0.20 to 0.10: need 4× histories
   - To reduce R from 0.20 to 0.05: need 16× histories

4. **Consider hybrid methods:**
   - Variance reduction + deep penetration may need CADIS/FW-CADIS
   - Consult advanced VR literature

**Reality check:** Some problems are just computationally hard

### Problem 6: "Check 10 (slope) failing, all others pass"

**Diagnosis:** Insufficient histories to establish tail distribution

**Root cause:** Need many samples in distribution tail (201 largest scores)

**Solution:**
1. Run more histories (typically 2-5× current)
2. This check often last to pass
3. If other 9 checks pass and slope between 1.5-4.5, acceptable
4. Slope far from 3.0 indicates non-normal distribution - investigate

**Low priority if:** Other 9 checks pass and R < 0.05

### Problem 7: "Checks passed early, now failing"

**Diagnosis:** Statistical fluctuation or variance reduction changing

**Root causes:**
- Early in run, statistical fluctuations can cause false passes
- Variance reduction parameters adjusted mid-run
- Rare large event occurred

**Solutions:**
1. Don't trust checks until run is well-developed (>10^5 histories)
2. Look at trend over multiple checkpoints, not single value
3. If consistently failing after initially passing:
   - May indicate systematic problem
   - Review variance reduction settings
   - Check for geometry errors introduced by restarts

**Rule:** Final assessment only, don't react to early fluctuations

## Production Run Guidelines

### Minimum Requirements for Production

**All of these must be satisfied:**
1. ✓ All 10 statistical checks passing
2. ✓ Relative error < 10% (preferably < 5%)
3. ✓ VOV < 0.1 (preferably < 0.05)
4. ✓ FOM stable (varies < factor of 3)
5. ✓ Mean stable (no drift in last 50%)
6. ✓ Trend analysis shows convergence (not oscillating)
7. ✓ No "lost particle" warnings in output
8. ✓ Physical reasonableness check passed

### Recommended Procedure

**Phase 1: Test run (10-20% of planned histories)**
- Verify geometry correct (plotting)
- Check for errors/warnings
- Estimate FOM and required histories
- Tune variance reduction

**Phase 2: Pre-production (full planned run)**
- Run with all tallies active
- Monitor statistical checks
- Verify convergence trends
- If checks passing, this becomes production run

**Phase 3: Validation (2× planned histories)**
- Continue run to twice target NPS
- Verify stability maintained
- Confirm convergence not spurious
- Use as production result

**Phase 4: Documentation**
- Record final NPS, FOM, R, VOV
- Save TFC data for each tally
- Document any failed checks and justification
- Archive input/output files

### Benchmarking Standards

**For code validation/benchmarking:**
- All 10 checks pass: MANDATORY
- R < 2% per tally: Target
- R < 1% for k_eff: Standard
- VOV < 0.01: Recommended
- Run until 2× minimum NPS: Verification

**For production calculations:**
- All 10 checks pass: MANDATORY
- R < 5% per tally: Typical
- VOV < 0.05: Recommended
- Comparison with independent estimate: Recommended

**For preliminary scoping:**
- ≥7/10 checks pass: Acceptable
- R < 15%: May be sufficient
- Document as "preliminary" or "order-of-magnitude"

## Integration with Other Skills

After statistical validation:

- **mcnp-output-parser**: If need to extract TFC data for plotting
- **mcnp-tally-analyzer**: Once statistics validated, interpret physical meaning
- **mcnp-variance-reducer**: If statistics poor, improve VR setup
- **mcnp-plotter**: Plot convergence trends (mean vs NPS, FOM vs NPS)
- **mcnp-best-practices-checker**: Verify overall simulation quality

## Important Validation Principles

1. **Never trust R alone**
   - Can have R=5% but still be wrong if checks fail
   - Small error bar doesn't mean correct answer
   - ALL 10 checks matter

2. **VOV is the truth teller**
   - VOV reveals fundamental convergence
   - High VOV means even R estimate is uncertain
   - VOV < 0.1 is non-negotiable for production

3. **FOM monitors efficiency**
   - Constant FOM = healthy simulation
   - Decreasing FOM = deteriorating VR
   - Increasing FOM = VR improving (good!)

4. **Mean drift is a red flag**
   - If mean hasn't converged, nothing else matters
   - Always check TFC for mean stability
   - Systematic drift = fundamental problem

5. **Early checks are unreliable**
   - Don't trust passes/fails until >100K histories
   - Statistical fluctuations cause false results
   - Judge based on trends, not snapshots

6. **Production = all checks pass**
   - No exceptions for production calculations
   - 9/10 requires explicit justification
   - Document any deviations

7. **Physics validates statistics**
   - Statistical quality necessary but not sufficient
   - Results must also be physically reasonable
   - Cross-check with analytical estimates

8. **Conservative estimates for NPS**
   - Calculated NPS is minimum, not target
   - Run 2-5× calculated minimum for confidence
   - Verify stability over extended run

9. **Document everything**
   - Record TFC data, failed checks, justifications
   - Archive output files
   - Enable reproducibility and review

10. **When in doubt, run longer**
    - Computational time is cheap compared to wrong answers
    - Overconvergence is safe; underconvergence is dangerous
    - Better to waste computer time than trust bad statistics

## Example Workflows

### Example 1: Comprehensive Validation

```
User: "Check if my simulation results are reliable"

Claude: I'll perform a comprehensive statistical validation of all your tallies.

[Reads .claude/commands/mcnp-statistics-checker.md]
[Uses MCNPStatisticsChecker]

**STATISTICAL QUALITY REPORT**

Run parameters:
- Total histories: 500,000
- Computer time: 45.3 minutes
- Tallies analyzed: 3 (F4, F14, F24)

---

**TALLY 4 (F4:N Cell Flux - Fuel):** ✓ EXCELLENT

Statistical checks: 10/10 passed ✓

Quality metrics:
  Relative error: 3.2% ✓ (excellent, <5%)
  VOV: 0.0045 ✓ (very good, <0.01)
  FOM: 1234.5 ✓ (stable over run)
  Slope: 3.1 ✓ (near ideal 3.0)

Convergence trends:
  NPS        Mean        Error    VOV      FOM
  50K     2.68E-04     0.098    0.045    1205
  100K    2.71E-04     0.067    0.024    1228
  250K    2.70E-04     0.042    0.011    1241
  500K    2.70E-04     0.032    0.0045   1235

Analysis: ✓ Excellent convergence
  - Mean stable since 100K histories
  - Error decreasing smoothly as 1/√N
  - VOV approaching zero
  - FOM stable (varies <3%)

**STATUS: PRODUCTION READY** ✓
Can be used with full confidence for critical calculations.

---

**TALLY 14 (F5:N Point Detector):** ⚠ MARGINAL

Statistical checks: 7/10 passed
Failed checks: #3 (error too large), #5 (FOM unstable), #9 (VOV high)

Quality metrics:
  Relative error: 12.5% ✗ (target: <10%)
  VOV: 0.156 ✗ (target: <0.10)
  FOM: 38.2 ✗ (decreasing trend)
  Slope: 3.4 ✓ (acceptable)

Convergence trends:
  NPS        Mean        Error    VOV      FOM
  50K     3.45E-05     0.245    0.456     65
  100K    3.52E-05     0.187    0.312     52
  250K    3.49E-05     0.142    0.201     45
  500K    3.48E-05     0.125    0.156     38

Analysis: ⚠ Problematic convergence
  - Mean stable ✓
  - Error decreasing but still high
  - VOV too high (>0.10) - few histories dominating
  - FOM decreasing steadily - efficiency degrading

Failed check interpretations:

Check #3: Relative error too large (12.5% > 10%)
  Impact: Uncertainty unacceptably high for production
  Cause: Insufficient histories OR poor variance reduction
  Fix: Need more histories or improve VR

Check #5: FOM unstable (decreasing 65→38, factor of 1.7)
  Impact: Detector efficiency degrading
  Cause: Weight windows or importance suboptimal
  Fix: Review detector diagnostics, improve VR around detector

Check #9: VOV too high (0.156 > 0.10)
  Impact: High variance in variance - even error estimate uncertain
  Cause: Few particle histories contributing most of tally
  Fix: Major VR improvement or change to F4 track-length

**RECOMMENDATIONS:**

Option 1: RUN LONGER (Conservative approach)
  To achieve R < 10%: need ~780,000 histories (1.56× more)
  To achieve R < 5%: need ~3,125,000 histories (6.25× more)

  BUT: VOV and FOM trends suggest fundamental problem
  Running longer may not solve underlying issues

Option 2: IMPROVE VARIANCE REDUCTION (Recommended)
  a) Use detector diagnostics: Add "PD" to F5 card
     - Shows which cells contribute to detector
     - Identifies importance issues

  b) Improve weight windows around detector:
     - Generate with WWG card focused on detector
     - Ensure path from source to detector well-sampled

  c) Check importance values:
     - Detector cell should have IMP:N 1
     - Path to detector should have IMP:N ≥ 1

Option 3: CHANGE TALLY TYPE (Alternative)
  Replace F5 point detector with F4 track-length flux
  - More stable statistics (many contributions per history)
  - Better VOV behavior
  - May lose spatial resolution

**STATUS: NOT PRODUCTION READY** ✗
Acceptable for preliminary analysis only. Requires improvement for critical use.

---

**TALLY 24 (F6:N+P Energy Deposition - Shield):** ✓ GOOD

Statistical checks: 9/10 passed
Failed check: #6 (PDF normality - marginal)

Quality metrics:
  Relative error: 8.2% ✓ (good, <10%)
  VOV: 0.067 ✓ (good, <0.10)
  FOM: 287.5 ✓ (stable)
  Slope: 2.7 ~ (slightly low, acceptable)

Analysis: ✓ Good quality with minor issue
  - Check #6 failure likely due to coupled N+P transport
  - All critical checks (R, VOV, FOM) pass
  - Slope = 2.7 close enough to 3.0

**STATUS: PRODUCTION ACCEPTABLE** ✓
Minor PDF issue acceptable given other strong indicators.

---

**OVERALL ASSESSMENT:**

Production ready: 2/3 tallies (F4, F24)
Needs improvement: 1/3 tallies (F14)

**RECOMMENDATIONS:**
1. Use F4 and F24 results with confidence
2. For F14:
   - Run detector diagnostics (PD card)
   - Improve variance reduction
   - OR replace with F4 tally
   - Do NOT use current F14 for production decisions

3. Consider continuing run to 1M histories:
   - May bring F14 into acceptable range (R < 10%)
   - Verify F4 and F24 stability maintained
   - Estimated time: ~45 minutes more

Would you like me to:
1. Show how to add detector diagnostics (PD card)?
2. Help improve variance reduction for F14?
3. Calculate exact NPS needed for target errors?
4. Analyze detector diagnostic output?
```

### Example 2: Diagnosing Persistent Problems

```
User: "My tally still fails checks after 5 million histories - what's wrong?"

Claude: Let me analyze your tally fluctuation chart to diagnose the problem.

[Reads .claude/commands/mcnp-statistics-checker.md]
[Analyzes TFC data]

**DETAILED DIAGNOSTIC ANALYSIS**

Tally: F5:N Point Detector
Total histories: 5,000,000
Computer time: 8.3 hours
Checks passed: 4/10 ✗ (UNACCEPTABLE after 5M histories)

**Tally Fluctuation Chart:**

NPS          Mean        Error    VOV      Slope    FOM
500K      1.23E-06     0.456    2.345     1.2     8.5
1M        1.45E-06     0.387    1.876     1.5    11.2
2M        1.58E-06     0.298    1.234     1.8    13.5
5M        1.67E-06     0.234    0.892     2.1    14.8

**CRITICAL PROBLEMS IDENTIFIED:**

Problem 1: MEAN STILL DRIFTING (Check #1 failed)
  Evidence: Mean increasing 1.23→1.45→1.58→1.67 E-06
  This is systematic upward trend, NOT random fluctuation

  Diagnosis: **SOURCE NOT CONVERGED** or **FUNDAMENTAL GEOMETRY ERROR**

  Possible causes:
  a) KCODE fission source still evolving after 5M histories
     → Extremely unusual, suggests insufficient skip cycles
     → Check: What are your KCODE parameters?

  b) Weight windows still adapting (WWG UPDATE>0)
     → Changing importance changes tally mean
     → Check: Is WWN card using UPDATE parameter?

  c) Lost particles accumulating
     → Check output for "N lost particles" warnings
     → Lost particles bias source distribution

  d) Detector in zero-importance region initially
     → Importance gradually increasing, more particles reach detector
     → Check: What's IMP:N value at detector location?

Problem 2: EXTREME VOV (Check #9 failed catastrophically)
  Evidence: VOV = 0.892 (should be <0.10)
  This is nearly 9× the limit - SEVERE problem

  Diagnosis: **SINGLE HISTORIES DOMINATING TALLY**

  Physics: With 5M histories and VOV ~ 1, approximately:
    Top 1% of histories contribute ~90% of tally
    Top 10 histories might contribute ~50% of tally

  This is NOT a statistical sample - it's rare event counting

  Cause: Point detector in very low-probability location
    - Deep penetration through thick shield
    - Long distance from source
    - Small solid angle
    - Only rare scattered particles reach detector

Problem 3: FOM EXTREMELY LOW (Check #5 failed)
  Evidence: FOM = 14.8 (should be >100, preferably >1000)

  Calculation: FOM = 1/(R²T) = 1/(0.234² × 8.3 hr × 60 min/hr)
              ≈ 1/(0.0548 × 498) ≈ 0.037 per minute ≈ 2.2 per hour

  Diagnosis: **FUNDAMENTALLY INEFFICIENT TALLY SETUP**

  This means: To achieve R=5%, would need:
    Time = 1/(FOM × R²) = 1/(2.2/hr × 0.05²) = 182 hours ≈ 7.6 DAYS

  Even with perfect variance reduction (10× FOM improvement):
    Still need ~18 hours for R=5%

Problem 4: SLOPE TOO LOW (Check #10 failed)
  Evidence: Slope = 2.1 (should be ≈3.0)

  Diagnosis: **NON-NORMAL DISTRIBUTION**
  PDF is not Gaussian - central limit theorem not applicable
  Confirms rare-event nature of tally

**ROOT CAUSE SYNTHESIS:**

This is a **FUNDAMENTALLY UNSUITABLE TALLY CONFIGURATION**.

The point detector is in a location where:
1. Very few particles ever reach it
2. Those that do have wildly varying weights
3. Statistics are dominated by rare lucky events
4. No reasonable amount of runtime will fix this

**SOLUTIONS (IN ORDER OF PREFERENCE):**

**Option 1: USE DIFFERENT TALLY TYPE** ★ RECOMMENDED
Replace F5 point detector with F4 track-length flux in small cell at same location

Advantages:
  - Every particle in cell contributes (not just rare events)
  - Much better statistics (many contributions per history)
  - VOV will drop to <0.1
  - FOM will increase 100-1000×

Implementation:
  1. Create small cell (~1 cm³) at detector location
  2. Fill with void (material 0) to not perturb physics
  3. Use F4:N tally on this cell
  4. Results will be flux at that location (comparable to F5)

**Option 2: ADD DXTRAN SPHERE** ★ FOR DEEP PENETRATION
If must use point detector, add deterministic transport sphere

Purpose: Forces particles toward detector deterministically
Implementation:
  DXC:N 0 0 0  0.1        $ DXTRAN contribution 0 if within 0.1 cm of detector
  DXT:N X Y Z  R          $ Sphere at detector location, radius R (e.g., 50 cm)

Effect: Will massively improve FOM, reduce VOV

**Option 3: EXTENSIVE VARIANCE REDUCTION**
Generate weight windows specifically for this detector

Steps:
  1. Run with WWG card to generate weight windows:
     WWG 15 0               $ Generate for F5 detector (tally 15)

  2. Review generated WWINP file, verify reasonable

  3. Rerun with weight windows active

Expected: FOM increase 10-100×, VOV decrease significantly

**Option 4: ACCEPT LIMITATION AND CHANGE PROBLEM**
Ask: Do you really need flux at this exact point?

Alternatives:
  - Average over larger region (F4 in cell)
  - Surface flux at boundary (F2)
  - Mesh tally showing spatial distribution (FMESH)
  - Move detector to more accessible location

**IMMEDIATE ACTION REQUIRED:**

❌ DO NOT continue running current setup
   - Will not converge even with 50M histories
   - Wasting computer time

✓ STOP and reconfigure:
   - Implement Option 1 (F4 tally) for quick fix
   - OR implement Option 2 (DXTRAN) if must use F5
   - Re-run with new setup

**EXPECTED RESULTS AFTER FIX:**

With F4 tally or DXTRAN:
  - VOV < 0.1 achievable with ~500K histories
  - FOM > 100 (maybe > 1000)
  - All 10 checks passing
  - R < 5% in reasonable time (<1 hour)

Would you like me to:
1. Show specific input cards for recommended fix?
2. Help set up DXTRAN sphere?
3. Design weight window generation run?
4. Explain F4 vs F5 differences in detail?
```

## Code Style Guidelines

When performing statistical validation:
- Present results clearly (check marks, colors if possible)
- Group by severity (excellent/good/marginal/poor)
- Explain failed checks physically, not just mathematically
- Provide specific, actionable recommendations
- Estimate computational requirements realistically
- Flag unacceptable results prominently
- Never let user trust bad statistics

## Dependencies

**Required Python packages:**
- Standard library: `math`, `collections`

**Required components:**
- Python module: `skills/output_analysis/mcnp_statistics_checker.py`
- Output parser: `parsers/output_parser.py`
- Reference: `.claude/commands/mcnp-statistics-checker.md` (detailed procedures)

## References

**Primary References:**
- `.claude/commands/mcnp-statistics-checker.md` - Complete validation procedures
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Statistical quality section
- Chapter 2.6.9: Tally Statistics and Convergence
- Table 2.2: Ten Statistical Checks Criteria
- Chapter 3.4.2: Preproduction Checks (items 5-6)
- Chapter 3.4.3: Production Run Statistical Requirements (items 3-8)

**Key Sections:**
- §2.6.9.1-2.6.9.10: Detailed explanation of each of 10 checks
- §3.4.2.4: Ten statistical checks must all pass
- Figure 2.6: Tally fluctuation chart example
- Table 3.1: Statistical quality requirements by problem type

**Phase 3 - VR Integration:**
- `vr_quality_metrics.md` - VR-specific quality indicators and assessment
- `advanced_convergence_theory.md` - Statistical theory with VR context
- `example_inputs/` - VR quality examples (overbiasing, WWG convergence)

**Related Skills:**
- mcnp-tally-analyzer: Interpret validated results
- mcnp-output-parser: Extract TFC data
- mcnp-variance-reducer: Improve failed statistics
- mcnp-plotter: Visualize convergence trends
- **Phase 3:** mcnp-ww-optimizer: Refine weight windows based on quality feedback
- **Phase 3:** mcnp-tally-analyzer (VR): Joint tally + statistics VR validation
