---
category: C
name: mcnp-warning-analyzer
description: Interpret and address MCNP warning messages including material warnings, physics warnings, statistical warnings, and deprecation notices
activation_keywords:
  - warning message
  - mcnp warning
  - analyze warning
  - warning output
  - deprecation
  - check warnings
  - interpret warning
  - warning significance
---

# MCNP Warning Analyzer Skill

## Purpose

This skill guides users in interpreting and addressing MCNP warning messages. Unlike fatal errors, warnings allow the calculation to proceed but indicate potentially problematic conditions that may affect results. This skill covers material warnings, physics warnings, statistical warnings, convergence issues, deprecation notices, and systematic procedures for determining which warnings require action versus which are informational.

## When to Use This Skill

- MCNP output contains warning messages after run completes
- Need to determine if warnings affect result validity
- Statistical checks show "missed" or poor convergence
- Material composition warnings appear
- Cross-section library warnings reported
- Deprecation warnings for old input syntax
- Tally statistics warnings require interpretation
- Source convergence warnings in criticality calculations
- Weight window warnings indicate variance reduction issues
- Physics model warnings need evaluation

## Prerequisites

- **mcnp-output-parser**: Ability to extract warnings from output
- **mcnp-statistics-checker**: Understanding of statistical quality metrics
- **mcnp-input-validator**: Input validation concepts
- Basic understanding of Monte Carlo statistics
- Familiarity with MCNP output file structure

## Core Concepts

### Warning Message Types

**Material Warnings**:
- Unnormalized fractions
- Missing thermal scattering data
- Photon production not available
- ZAID substitutions

**Physics Warnings**:
- Physics models disabled
- Energy range issues
- Particle cutoffs reached
- Mode incompatibilities

**Statistical Warnings**:
- Tally fluctuation chart failed checks (1-10)
- Large relative errors
- Poor bin statistics
- Zero tally results

**Convergence Warnings** (criticality):
- Shannon entropy not converged
- Keff trend not stabilized
- Source distribution not settled
- Inactive cycles insufficient

**Deprecation Warnings**:
- Obsolete card syntax
- Old-style parameters
- Legacy features

**IEEE Exception Warnings**:
- Floating point exceptions
- Divide by zero
- Overflow/underflow
- Invalid operations

### Warning Severity Levels

**Critical** (Action Required):
- Statistical checks failed (many 1-10 checks missed)
- Material normalization warnings (may affect physics)
- Source convergence not achieved (criticality)
- Tally relative error >10%

**Important** (Should Investigate):
- Missing thermal scattering for some nuclides
- Physics warnings affecting simulation scope
- Moderate statistical issues (1-2 checks missed)
- Energy cutoffs reached

**Informational** (Generally Safe):
- Deprecation notices (code still works)
- IEEE exceptions that completed without crash
- Minor normalization adjustments
- Comment messages

### Statistical Quality Checks (1-10)

**MCNP's 10 Statistical Tests** (for tally reliability):
1. Mean behavior acceptable (slope <0.1)
2. Relative error acceptable (<0.10 typically)
3. Relative error decreasing trend
4. Relative error decreased in second half
5. Figure of merit (FOM) behavior acceptable
6. FOM increasing in second half
7. Variance of variance (VOV) <0.10
8. VOV decreasing
9. VOV decreased in second half
10. Fitted slope behaves appropriately

**"Passed" Criteria**:
- All 10 checks pass → Result reliable
- 1-2 checks "missed" → Marginal, investigate
- 3+ checks "missed" → Result unreliable

## Decision Tree: Analyzing Warnings

```
START: Warning Message Encountered
  |
  +--> Is it a "fatal error"?
  |      |
  |      +--> YES: Use mcnp-fatal-error-debugger skill instead
  |      |
  |      +--> NO: Continue (it's a warning or comment)
  |
  +--> What type of warning?
  |      |
  |      +--> Material Warning
  |      |      ├─> "unnormalized fractions" → Check if adjustment reasonable
  |      |      ├─> "no photon production" → Expected for MODE N?
  |      |      ├─> "thermal scattering not used" → Should MT card exist?
  |      |      └─> Fix material definition if incorrect
  |      |
  |      +--> Statistical Warning
  |      |      ├─> Check tally fluctuation chart
  |      |      ├─> Count failed checks (1-10)
  |      |      ├─> If >2 failed → Run longer
  |      |      ├─> If all failed → Check tally setup
  |      |      └─> If variance reduction issue → Adjust WWG/IMP
  |      |
  |      +--> Convergence Warning (KCODE)
  |      |      ├─> Check Shannon entropy plot
  |      |      ├─> If trending → More inactive cycles
  |      |      ├─> Check keff vs cycle plot
  |      |      └─> Verify source distribution reasonable
  |      |
  |      +--> Physics Warning
  |      |      ├─> "physics models disabled" → Intentional for MODE?
  |      |      ├─> Energy cutoff reached → Are cutoffs appropriate?
  |      |      └─> Verify physics setup matches intent
  |      |
  |      +--> Deprecation Warning
  |      |      ├─> Note for future input updates
  |      |      ├─> Functionality still works (no immediate action)
  |      |      └─> Plan migration to new syntax
  |      |
  |      └─> IEEE Exception Warning
  |             ├─> If run completed → Usually safe
  |             ├─> If large numbers → Check input reasonableness
  |             └─> If concerned → Investigate source of exception
  |
  +--> Does warning affect result validity?
         |
         +--> YES: Fix issue and re-run
         |
         +--> NO: Document and proceed
```

## Tool Invocation

This skill includes a Python implementation for automated warning analysis and categorization.

### Importing the Tool

```python
from mcnp_warning_analyzer import MCNPWarningAnalyzer

# Initialize the analyzer
analyzer = MCNPWarningAnalyzer()
```

### Basic Usage

**Analyze Warnings from Output File**:
```python
# Extract and categorize all warnings
warnings = analyzer.analyze_warnings('outp')

# Review warnings by category
for category, messages in warnings.items():
    if messages:
        print(f"\n{category.upper()} Warnings:")
        for msg in messages:
            print(f"  - {msg}")
```

**Prioritize Warnings by Severity**:
```python
# Analyze warnings
warnings = analyzer.analyze_warnings('outp')

# Get prioritized list (geometry → material → source → tally → other)
prioritized = analyzer.prioritize_warnings(warnings)

for item in prioritized:
    print(f"[{item['category'].upper()}] {item['message']}")
```

**Check for Critical Warnings**:
```python
# Analyze output file
warnings = analyzer.analyze_warnings('outp')

# Check for critical categories
critical_categories = ['geometry', 'material', 'source']
has_critical = any(warnings.get(cat, []) for cat in critical_categories)

if has_critical:
    print("CRITICAL warnings found - review before using results:")
    for cat in critical_categories:
        for msg in warnings.get(cat, []):
            print(f"  [{cat}] {msg}")
```

### Integration with MCNP Workflow

```python
from mcnp_warning_analyzer import MCNPWarningAnalyzer

# Initialize analyzer
analyzer = MCNPWarningAnalyzer()

# Run post-simulation warning analysis
output_file = 'path/to/outp'
warnings = analyzer.analyze_warnings(output_file)

# Generate warning report
print("=" * 60)
print("MCNP WARNING ANALYSIS REPORT")
print("=" * 60)

# Prioritize for systematic review
prioritized = analyzer.prioritize_warnings(warnings)

if not prioritized:
    print("\n✓ No warnings detected - clean run")
else:
    print(f"\nTotal warnings: {len(prioritized)}\n")

    for i, item in enumerate(prioritized, 1):
        cat = item['category']
        msg = item['message']

        # Assign severity based on category
        if cat in ['geometry', 'material']:
            severity = 'HIGH'
        elif cat in ['source', 'tally']:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'

        print(f"{i}. [{severity}] {cat.upper()}: {msg}")

print("\n" + "=" * 60)
```

---

## Use Case 1: Material Fractions Not Normalized

**Warning Message**:
```
warning.  1 materials had unnormalized fractions. print table 40.
```

**Cause**: Material fractions don't sum to 1.0 (atomic fractions) or to total mass (weight fractions)

**Example**:
```
M1  1001.80c  2.1  8016.80c  1.0    $ Sum = 3.1, not 3.0 (H2O should be 2:1)
```

**Check Table 40** (in output):
```
print table 40
           material     composition         density
   1    1001.80c      0.677419              $ MCNP normalized: 2.1/3.1
        8016.80c      0.322581              $ MCNP normalized: 1.0/3.1
```

**Evaluation**:
```
Original intent: H2O with 2:1 ratio
Actual ratio: 2.1:1 (67.7% H, 32.3% O by atom)
Expected: 66.7% H, 33.3% O
Difference: ~1%
```

**Decision**:
- Small difference (<5%): Likely typo, fix but results approximately correct
- Large difference (>5%): Material composition wrong, must fix and re-run

**Fix**:
```
M1  1001.80c  2.0  8016.80c  1.0    $ Corrected: exact 2:1 ratio
```

**Key Point**: MCNP automatically normalizes but warns; check if normalization matches intent

## Use Case 2: No Photon Production Cross Sections

**Warning Message**:
```
warning.  photon production cross sections do not exist for nuclide 92235.
```

**Context**: Running MODE N P (coupled neutron-photon)

**Example Input**:
```
MODE  N P                             $ Coupled transport
M1  92235.80c  0.03  92238.80c  0.97  $ Uranium fuel
```

**Evaluation**:
- Is photon production important for this problem?
  - If calculating photon dose → YES, critical warning
  - If only neutron transport needed → NO, can use MODE N instead

**Fix Option 1** (If photons not needed):
```
MODE  N                               $ Neutron only
```

**Fix Option 2** (If photons needed):
```
c Use nuclide with photon production data
c Or accept that photons from U-235 reactions not included
c (may be acceptable depending on problem)
```

**Key Point**: Not all ZAIDs have photon production data; verify importance for problem

## Use Case 3: Statistical Checks Failed

**Warning Message**:
```
the tally in the tally fluctuation chart bin did not pass  3 of the 10 statistical checks.
```

**Tally Fluctuation Chart** (from output):
```
tally        4        nps      mean     error    vov   slope    fom
        100000    1.234E-02  0.0850  0.0050  10.0  12345
        200000    1.241E-02  0.0620  0.0042   9.8  12890
        300000    1.238E-02  0.0505  0.0038   9.5  13120
        400000    1.240E-02  0.0440  0.0035   9.2  13100
        500000    1.239E-02  0.0395  0.0032   8.9  13150

 the estimated slope of the 200 largest tallies will be 10.0
 the large tally grid structure may indicate geometry problems.

 ***************************************************************
 dump no.    2 on file runtpe     nps =      500000   coll =       2345678
        3 warning messages so far.

    1 tally fluctuation charts

                   tally        4
     mean        1.23900E-02
     error       0.0395

 statistical checks
     1 passed
     2 passed
     3 passed
     4 missed  ← FAILED
     5 passed
     6 passed
     7 missed  ← FAILED
     8 passed
     9 missed  ← FAILED
    10 passed
```

**Interpretation**:
- 3 checks missed (4, 7, 9)
- Check 4: Relative error not decreasing in second half
- Check 7: VOV > 0.10
- Check 9: VOV not decreasing in second half

**Causes**:
- Insufficient particles (need more NPS)
- Poor variance reduction
- Tally in low-probability region
- Geometry issues causing large tallies

**Fix**:
```
c Option 1: Run longer
NPS  5e6                              $ Was 5e5, increase 10×

c Option 2: Improve variance reduction
WWG  4  0  1.0                        $ Generate weight windows for F4

c Option 3: Check tally setup
c - Is tally in reasonable location?
c - Are energy bins too fine?
c - Is FOM stable? (Yes in example: 12345 → 13150)
```

**Re-run and Re-check**: If FOM stable and error decreasing, likely converging

**Key Point**: 1-2 missed checks marginal, 3+ requires action

## Use Case 4: Shannon Entropy Not Converged (Criticality)

**Warning Message**:
```
the kcode Shannon entropy appears not to be converged.
```

**Shannon Entropy Plot** (from output):
```
cycle   keff    entropy
   10  1.0123   5.234
   20  1.0145   5.412
   30  1.0132   5.523
   40  1.0128   5.601  ← Still increasing
   50  1.0125   5.648
   60  1.0122   5.671
   ...
  150  1.0118   5.712  ← Not yet flat
```

**Problem**: Entropy still trending upward, source not converged

**Cause**: Inactive cycles insufficient for source convergence

**Fix**:
```
c Original:
KCODE  10000  1.0  50  150           $ 50 inactive, 100 active

c Increase inactive cycles:
KCODE  10000  1.0  100  200          $ 100 inactive, 100 active
```

**Alternative**: Better initial source guess
```
c Original:
KSRC  0 0 0                          $ Single point

c Multiple initial points:
KSRC  0 0 0  10 0 0  -10 0 0  0 10 0  0 -10 0  0 0 10  0 0 -10
```

**Verification**: Re-run and check entropy flattens in inactive cycles

**Key Point**: Active cycle keff unreliable if source not converged

## Use Case 5: Deprecation Warning - Old Syntax

**Warning Message**:
```
warning.  the dbcn card is obsolete. use the rand card instead.
```

**Old Input**:
```
DBCN  12345  0  0  1  13  19073486328125  0  0  0
```

**Modern Equivalent**:
```
RAND  GEN=1  SEED=19073486328125  HIST=1  STRIDE=152917
```

**Action**:
- **Immediate**: No action required, code still works
- **Future**: Update to modern syntax when revising input
- **Documentation**: Note for next input version

**Key Point**: Deprecation warnings don't prevent execution, plan for future update

## Use Case 6: Weight Window Warning

**Warning Message**:
```
warning.  3 particles were killed by the weight window.
```

**Cause**: Weight window bounds too restrictive

**Example Output Section**:
```
 weight window summary
   neutrons
     particles entering weight window                       1000000
     particles surviving weight window                       999997
     particles killed by weight window                            3
     particles splitting in weight window                     12345
     particles undergoing roulette in weight window           54321
```

**Evaluation**:
- 3 particles killed out of 1,000,000 → 0.0003% → Negligible
- If 10,000+ killed → Problem with weight windows

**Fix if Significant**:
```
c Widen weight window bounds
WWP:N  10  5  10  0  0               $ wupn=10 (was 5), wider window
```

**Or regenerate weight windows**:
```
c Re-run WWG with longer statistics
NPS  5e5                              $ Was 1e5
WWG  5  0  1.0
```

**Key Point**: Few killed particles (<1%) acceptable, many indicates issue

## Use Case 7: Large Relative Error Warning

**Warning Message**:
```
warning.  tally    14 has a relative error greater than 0.50.
```

**Tally Result**:
```
 tally  14
        result    1.234E-08 ± 0.7234 (58.5%)
```

**Causes**:
- Tally in very low-probability region
- Insufficient particles
- No variance reduction

**Evaluation**:
- 58.5% error → Result essentially meaningless
- Need error <10% for reliable result
- Need error <5% for publication quality

**Fix**:
```
c Option 1: Much longer run
NPS  1e8                              $ Was 1e6, increase 100×

c Option 2: Add variance reduction
WWG  14  0  1.0                       $ Weight windows for tally 14

c Option 3: Move tally to higher probability location
c (if physically meaningful)

c Option 4: Accept that quantity is very small
c (document that quantity negligible)
```

**Key Point**: High error means result unreliable, not necessarily wrong answer

## Use Case 8: IEEE Floating Point Exception

**Warning Message**:
```
ieee_flags: Warning: hardware overflow trapped 0 times.
ieee_flags: Warning: hardware inexact trapped 123456 times.
```

**Interpretation**:
- "overflow": Number too large to represent
- "inexact": Result cannot be represented with infinite precision (e.g., 2/3)
- "divide by zero": Division by zero occurred
- "underflow": Number too small (near zero)

**Evaluation**:
- If run completed successfully → Usually safe
- "inexact" very common (nearly always harmless)
- "overflow" or "divide by zero" → Investigate if many occurrences

**Action**:
- **If few (<100)**: Likely harmless, numerical rounding
- **If many (>10,000)**: Check for:
  - Very large or very small numbers in input
  - Unreasonable parameter values
  - Source or tally issues

**Example Investigation**:
```
c Check for unreasonable values:
c - Source energy: ERG=1e20 (too large?)
c - Cell volume: VOL=1e-30 (too small?)
c - Importance: IMP:N=1e10 (too large?)
```

**Key Point**: Most IEEE exceptions benign if run completes; investigate if concerned

## Common Errors and Troubleshooting

### Error 1: Ignoring Critical Statistical Warnings

**Symptom**: Published results with >10% error or many failed checks

**Problem**: Results unreliable, conclusions invalid

**Example (Bad)**:
```
Result: keff = 1.0234 ± 0.1456 (14.2%)
Statistical checks: 7 of 10 missed
Decision: Published anyway (WRONG!)
```

**Fix (Good)**:
```
Result: keff = 1.0234 ± 0.1456 (14.2%)
Statistical checks: 7 of 10 missed
Decision: Run longer, improve VR, achieve <5% error
New result: keff = 1.0241 ± 0.0048 (0.47%)
Statistical checks: 10 of 10 passed
```

**Rule**: Never use results with >10% error or >2 failed checks

### Error 2: Material Warning Indicates Wrong Composition

**Symptom**: Unnormalized fraction warning but intent unclear

**Example**:
```
M1  92235.80c  0.93  92238.80c  0.93  $ Intended 93% enrichment
warning.  material 1 unnormalized (sum = 1.86, not 1.0)
```

**Problem**: User intended 93% U-235, 7% U-238, but entered both as 0.93

**Fix**:
```
M1  92235.80c  0.93  92238.80c  0.07  $ Correct: 93% U-235, 7% U-238
```

**Prevention**: Always verify material fractions sum correctly

### Error 3: Deprecation Warning Ignored Too Long

**Symptom**: Input works in MCNP6.2 but fails in MCNP6.3

**Cause**: Deprecated feature finally removed

**Example**:
```
c MCNP6.2: Warning, DBCN obsolete (still works)
c MCNP6.3: Fatal error, DBCN not recognized
```

**Prevention**: Address deprecation warnings proactively
```
c Replace deprecated syntax when warned:
c DBCN → RAND (do it when warned)
c Don't wait for feature removal
```

### Error 4: Entropy Warning But User Trusts Result

**Symptom**: Shannon entropy clearly not converged but user accepts keff

**Problem**: Active cycle keff biased by unconverged source

**Example (Bad)**:
```
Entropy trending through all 150 cycles
keff = 1.0234 ± 0.0012
User: "Error bar small, must be good!" (WRONG!)
```

**Fix (Good)**:
```
Increase inactive cycles to 200
Re-run
Verify entropy flat
Then trust keff result
```

**Rule**: Entropy must be converged before trusting keff

### Error 5: Weight Window Warnings Indicate Poor VR

**Symptom**: Thousands of particles killed by weight windows

**Cause**: Weight windows too restrictive or incorrectly generated

**Fix**:
```
c Check WWG statistics:
c - Was WWG run long enough? (Need low relative error in detector)
c - Are WWE bins appropriate?
c - Is mesh resolution sufficient?

c Regenerate with better settings:
NPS  5e5                              $ Longer WWG run
WWG  5  0  1.0
c Then use in production run
```

## Integration with Other Skills

### 1. **mcnp-output-parser**

Parser extracts warnings for systematic analysis.

**Example**:
```python
warnings = output_parser.extract_warnings('outp')
for w in warnings:
    if w.type == 'statistical':
        # Analyze with warning-analyzer procedures
        check_tally_reliability(w.tally_number)
```

### 2. **mcnp-statistics-checker**

Statistics-checker validates tally quality per warning-analyzer criteria.

**Workflow**:
```
1. Run MCNP
2. warning-analyzer: Note statistical warnings
3. statistics-checker: Check all 10 statistical tests
4. If failed → re-run with changes
```

### 3. **mcnp-fatal-error-debugger**

Some warnings escalate to fatal errors if ignored.

**Pattern**:
```
Run 1: Warning about material issue
Run 2: Warning still present, geometry changed
Run 3: Now fatal error (material/geometry mismatch)
→ Use fatal-error-debugger
```

### 4. **mcnp-input-validator**

Validator can catch issues before they become warnings.

**Workflow**:
```
1. input-validator: Check material normalization
2. Fix issues found
3. Run MCNP
4. Fewer warnings (already caught by validator)
```

### 5. **mcnp-tally-analyzer**

Tally-analyzer interprets statistical warnings in context.

**Example**:
```
Warning: Tally 4 relative error 0.15
tally-analyzer: Check if tally in low-probability region
→ If yes: expected, may need VR
→ If no: something wrong with setup
```

### 6. **mcnp-variance-reducer**

Variance-reducer optimizes to eliminate statistical warnings.

**Workflow**:
```
1. warning-analyzer: Identify tallies with poor statistics
2. variance-reducer: Design VR strategy (WWG, IMP, DXTRAN)
3. Re-run with VR
4. warning-analyzer: Verify statistical warnings resolved
```

**Example**:
```
Initial: F4 tally with 0.25 relative error, 5 checks failed
variance-reducer: Add WWG for F4
Result: F4 tally with 0.03 relative error, all checks passed
```

### 7. **mcnp-criticality-analyzer**

Criticality-analyzer specifically handles KCODE convergence warnings.

**Integration**:
```
warning-analyzer: Detect Shannon entropy warning
criticality-analyzer: Full convergence analysis
  - Plot entropy vs cycle
  - Plot keff vs cycle
  - Check source distribution evolution
  - Recommend inactive cycle adjustment
```

### 8. **mcnp-material-builder**

Material-builder prevents material warnings at input creation.

**Prevention Pattern**:
```
material-builder: Create M card with proper normalization
→ Fractions sum to 1.0 (atomic) or correct mass
→ Include thermal scattering (MT) when needed
→ Result: No material warnings
```

### 9. **mcnp-physics-builder**

Physics-builder prevents physics warnings through proper setup.

**Example**:
```
physics-builder: Set up MODE N P
  - Ensure nuclides have photon production data
  - Or warn user that some photon production missing
  - Set appropriate energy ranges
→ Result: Expected physics warnings documented
```

### 10. **mcnp-best-practices-checker**

Best-practices checks for warning-prone patterns.

**Checks**:
```
- NPS sufficient for desired error? (check-03)
- Inactive cycles sufficient? (check-04 for KCODE)
- Materials normalized? (check-06)
- Variance reduction planned for deep penetration? (check-08)
→ Prevents many warnings before run
```

## Validation Checklist

After addressing warnings:

- [ ] All critical warnings resolved (statistical failures, convergence issues)
- [ ] Material warnings understood (normalization acceptable or fixed)
- [ ] Statistical checks reviewed:
  - [ ] <2 checks failed per tally (preferably 0)
  - [ ] Relative error <10% (preferably <5%)
  - [ ] FOM stable or increasing
- [ ] Convergence checks (if KCODE):
  - [ ] Shannon entropy converged (flat in inactive cycles)
  - [ ] Keff stable (no trend in active cycles)
- [ ] Physics warnings understood (expected for MODE or issue)
- [ ] Deprecation warnings noted for future updates
- [ ] IEEE exceptions minimal (<100) or understood
- [ ] Documentation includes warning analysis and resolution

## Advanced Topics

### 1. Statistical Test Interpretation

**Test 1-4** (Mean and Error Behavior):
- Tests if mean and error converging properly
- Failed test → Simulation not converged yet
- Solution: Run longer

**Test 5-6** (FOM Behavior):
- FOM should be constant (±10%)
- Failed test → Variance reduction issue or binning problem
- Solution: Adjust VR or tally binning

**Test 7-10** (Variance of Variance):
- VOV should be <0.10 and decreasing
- Failed test → Large rare events dominating
- Solution: Better VR, more particles, check for anomalies

### 2. Warning Suppression (Advanced)

**PRINT Card** can suppress some output:
```
PRINT  -140                           $ Suppress Table 140 (nuclide activity warnings)
```

**Use Sparingly**:
- Suppressing warnings doesn't fix underlying issues
- Only suppress known benign warnings
- Document why suppressed

### 3. Custom Warning Thresholds

**STOP Card** for tally error:
```
STOP  F4 0.05                         $ Stop when F4 error <5%
```

**Use**: Automate runs to stop when statistics sufficient

### 4. Batch Statistics for Better Error Estimates

**NPS Card with Batches**:
```
NPS  1e6  J  10000                    $ 1M particles, batches of 10k
```

**Benefit**: More robust error estimates for tallies

### 5. Warning Correlation Analysis

**Pattern Recognition**:
- Material warning + large error → Material issue affecting tally
- Entropy warning + keff trend → Source convergence affects criticality
- Many IEEE exceptions + tally anomaly → Numerical instability

**Example Correlation 1**:
```
Warning: Material 5 unnormalized (sum=10.5 vs 10.0)
Warning: Tally 14 failed 8 of 10 checks
Analysis: Material 5 used in cell with tally 14
Conclusion: Material composition error affecting tally physics
Action: Fix material normalization, re-run
```

**Example Correlation 2**:
```
Warning: Shannon entropy not converged
Warning: keff trending upward through active cycles
Analysis: Source still evolving, keff not trustworthy
Conclusion: Need more inactive cycles
Action: Double inactive cycles (50→100), re-run
```

**Example Correlation 3**:
```
Warning: 45000 IEEE inexact exceptions
Warning: Tally 6 has anomalously large bins
Analysis: Numerical precision issues in specific geometry region
Conclusion: Geometry issue or source in unrealistic location
Action: Review geometry cells, check source definition
```

### 6. Multi-Tally Warning Analysis

**Pattern**: Multiple tallies with warnings

**Example Output**:
```
warning.  tally    4 failed  3 of 10 statistical checks.
warning.  tally    5 failed  3 of 10 statistical checks.
warning.  tally    6 failed  7 of 10 statistical checks.
```

**Analysis Strategy**:
```
1. Check if same geometry region:
   F4:N  10      $ Cell 10
   F5:N  0 0 0 1 $ Near cell 10
   F6:N  10      $ Cell 10
   → All near same region suggests local VR issue

2. Check if same energy range:
   E4  1e-8 20i 20  $ Thermal to 20 MeV
   E5  1e-8 20i 20
   E6  1e-8 20i 20
   → All same energy suggests source spectrum issue

3. Priority:
   - Tally 6 (7 failed) → Most critical, fix first
   - Tallies 4,5 (3 failed) → Fix after tally 6
```

**Solution Strategy**:
```
c Add weight windows for worst tally first
WWG  6  0  1.0                        $ Generate for F6
c This may improve F4 and F5 as well (same region)
```

### 7. KCODE Warning Deep Dive

**Shannon Entropy Convergence Details**

**Entropy Formula**:
```
H = -Σ(p_i * log(p_i))
where p_i = fraction of source in spatial bin i
```

**What Entropy Measures**:
- Source distribution spread across geometry
- Higher H → more spread out
- Lower H → more localized
- Flat H → converged distribution

**Ideal Pattern**:
```
Cycles 1-30:   Entropy rises rapidly (source spreading)
Cycles 31-75:  Entropy rises slowly (fine adjustment)
Cycles 76-100: Entropy flat within ±5% (CONVERGED)
Cycles 101+:   Active cycles, use for keff
```

**Problem Patterns**:

**Pattern A: Continuous Rise**
```
Cycles 1-150: Entropy continuously increasing
Problem: Source never converges
Cause: Complex geometry, poor initial guess
Fix: More inactive cycles (150→300) or better KSRC
```

**Pattern B: Oscillation**
```
Cycles: H = 5.2, 5.8, 5.1, 5.9, 5.3, 5.7...
Problem: Source oscillating between regions
Cause: Multiple fissile regions with similar importance
Fix: Better initial KSRC covering all regions
```

**Pattern C: Late Jump**
```
Cycles 1-90: Flat at H=5.5
Cycles 91-95: Jump to H=6.2
Cycles 96-150: Flat at 6.2
Problem: Source found new important region late
Cause: Inactive cycles barely sufficient
Fix: More inactive cycles (100→150) for safety margin
```

### 8. Statistical Test Failure Patterns

**Pattern Analysis by Test Numbers**

**Tests 1-2 Failed (Mean/Error Not Acceptable)**:
```
Cause: Fundamental convergence issue
Solution: Much longer run (5-10× more particles)
Example: NPS 1e5 → 1e6
```

**Test 3-4 Failed (Error Not Decreasing)**:
```
Cause: Variance not decreasing with √N
Solution: Check for:
  - Rare events dominating (need VR)
  - Tally in wrong location
  - Geometry errors causing occasional huge tallies
```

**Tests 5-6 Failed (FOM Issues)**:
```
Cause: Efficiency changing during run
Solution: Check for:
  - Variance reduction turning on/off
  - Source distribution changing
  - Weight window issues
Example:
  Cycle 1-100: FOM=1000
  Cycle 101+: FOM=100 (10× worse)
  → Something changed, investigate
```

**Tests 7-9 Failed (VOV Too Large)**:
```
Cause: Large rare events
Solution:
  - Add variance reduction (WWG, IMP)
  - Check for geometry errors (lost particles creating huge tallies)
  - Increase particles to reduce impact of rare events
Rule: VOV > 0.10 means rare large events dominating
```

**Test 10 Failed (Slope Issues)**:
```
Cause: Statistical behavior inconsistent with 1/√N
Solution:
  - Usually paired with other failures
  - Focus on fixing tests 1-9 first
  - Test 10 often passes when others fixed
```

### 9. Material Warning Resolution Workflow

**Step-by-Step Material Warning Analysis**

**Step 1: Identify Warning**
```
grep "material.*unnormalized" outp
→ warning.  1 materials had unnormalized fractions. print table 40.
```

**Step 2: Find Table 40**
```
grep -A 20 "print table 40" outp
```

**Step 3: Compare Intent vs Actual**
```
Input:  M1  1001.80c  2.1  8016.80c  1.0
Intent: H2O (2:1 ratio)
Actual: 2.1:1 ratio (67.7%:32.3%)
Expected: 2.0:1 ratio (66.7%:33.3%)
Error: 1.5% error in hydrogen fraction
```

**Step 4: Determine Significance**
```
If error <1%: Rounding, likely OK
If error 1-5%: Typo, fix recommended
If error >5%: Wrong material, must fix
If error >20%: Completely wrong, critical fix
```

**Step 5: Fix and Document**
```
c FIXED 2024-10-31: H2O ratio corrected
c Original: M1  1001.80c  2.1  8016.80c  1.0 (warning)
c Corrected to exact 2:1 ratio:
M1  1001.80c  2.0  8016.80c  1.0
```

### 10. Warning Severity Decision Matrix

**Matrix for Action Decisions**

| Warning Type | Error >10% | Error 5-10% | Error <5% |
|--------------|------------|-------------|-----------|
| Statistical (tally) | CRITICAL - Fix required | Important - Fix recommended | Monitor - OK if >2 checks pass |
| Convergence (KCODE) | CRITICAL - Cannot trust result | CRITICAL - Extend run | Monitor - Check trend |
| Material | Important - Check physics impact | Low - Likely OK if intent correct | Very Low - Document only |
| Physics | Context - Check if expected | Context - Verify MODE correct | Informational |
| IEEE | Low - Monitor count | Very Low | Very Low |
| Deprecation | Low - Plan update | Very Low | Very Low |

**Action Key**:
- **CRITICAL**: Must fix before using results
- **Important**: Should fix, results may be questionable
- **Monitor**: Watch in future runs
- **Low/Very Low**: Document, fix when convenient
- **Context**: Depends on problem specifics

### 11. Automated Warning Analysis Scripts

**Example Script Structure** (bash/python):

```bash
#!/bin/bash
# analyze_warnings.sh - Automated warning analysis

OUTPUT_FILE="outp"

echo "=== MCNP Warning Analysis ==="
echo ""

# Count warnings
WARN_COUNT=$(grep -c "warning\." $OUTPUT_FILE)
echo "Total warnings: $WARN_COUNT"

# Statistical warnings (critical)
STAT_WARN=$(grep "failed.*of.*10.*statistical" $OUTPUT_FILE)
if [ ! -z "$STAT_WARN" ]; then
    echo ""
    echo "CRITICAL - Statistical warnings found:"
    echo "$STAT_WARN"
fi

# Entropy warnings (critical for KCODE)
ENTROPY_WARN=$(grep -i "entropy.*not.*converged" $OUTPUT_FILE)
if [ ! -z "$ENTROPY_WARN" ]; then
    echo ""
    echo "CRITICAL - Entropy convergence issue:"
    echo "$ENTROPY_WARN"
fi

# Material warnings (important)
MAT_WARN=$(grep "material.*unnormalized" $OUTPUT_FILE)
if [ ! -z "$MAT_WARN" ]; then
    echo ""
    echo "IMPORTANT - Material normalization:"
    echo "$MAT_WARN"
fi

# Large error warnings
ERROR_WARN=$(grep "relative error greater than" $OUTPUT_FILE)
if [ ! -z "$ERROR_WARN" ]; then
    echo ""
    echo "HIGH ERROR - Check tally setup:"
    echo "$ERROR_WARN"
fi

# Deprecation warnings (informational)
DEP_WARN=$(grep -i "obsolete\|deprecated" $OUTPUT_FILE)
if [ ! -z "$DEP_WARN" ]; then
    echo ""
    echo "INFO - Deprecation notices:"
    echo "$DEP_WARN"
fi

echo ""
echo "=== Analysis Complete ==="
```

**Python Version** (more sophisticated):

```python
#!/usr/bin/env python3
# warning_analyzer.py - Advanced warning analysis

import re
from collections import defaultdict

def analyze_mcnp_warnings(output_file):
    """Analyze MCNP output for warnings and categorize by severity."""

    warnings = {
        'critical': [],
        'important': [],
        'informational': []
    }

    with open(output_file, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'warning.' in line.lower():
            # Statistical warnings - CRITICAL
            if 'failed' in line and 'statistical checks' in line:
                match = re.search(r'failed\s+(\d+)\s+of.*10', line)
                if match:
                    failed_count = int(match.group(1))
                    if failed_count >= 3:
                        warnings['critical'].append(
                            f"Line {i}: {failed_count} statistical checks failed"
                        )
                    else:
                        warnings['important'].append(
                            f"Line {i}: {failed_count} statistical checks failed"
                        )

            # Entropy warnings - CRITICAL
            elif 'entropy' in line.lower() and 'converged' in line.lower():
                warnings['critical'].append(f"Line {i}: Source convergence issue")

            # Material warnings - IMPORTANT
            elif 'material' in line.lower() and 'unnormalized' in line.lower():
                warnings['important'].append(f"Line {i}: Material normalization")

            # High error warnings - IMPORTANT
            elif 'relative error greater than' in line.lower():
                warnings['important'].append(f"Line {i}: High tally error")

            # Deprecation - INFORMATIONAL
            elif 'obsolete' in line.lower() or 'deprecated' in line.lower():
                warnings['informational'].append(f"Line {i}: Deprecated syntax")

            # IEEE exceptions - Usually INFORMATIONAL
            elif 'ieee' in line.lower():
                warnings['informational'].append(f"Line {i}: IEEE exception")

    return warnings

def print_warning_report(warnings):
    """Print formatted warning report."""
    print("=" * 60)
    print("MCNP WARNING ANALYSIS REPORT")
    print("=" * 60)

    if warnings['critical']:
        print("\n*** CRITICAL WARNINGS (ACTION REQUIRED) ***")
        for w in warnings['critical']:
            print(f"  • {w}")

    if warnings['important']:
        print("\n*** IMPORTANT WARNINGS (SHOULD INVESTIGATE) ***")
        for w in warnings['important']:
            print(f"  • {w}")

    if warnings['informational']:
        print("\n*** INFORMATIONAL WARNINGS ***")
        for w in warnings['informational']:
            print(f"  • {w}")

    if not any(warnings.values()):
        print("\n✓ No warnings found - clean run")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    import sys
    output_file = sys.argv[1] if len(sys.argv) > 1 else "outp"
    warnings = analyze_mcnp_warnings(output_file)
    print_warning_report(warnings)
```

**Usage**:
```bash
python warning_analyzer.py outp
```

## Quick Reference: Common Warning Messages

| Warning | Significance | Action |
|---------|--------------|--------|
| "unnormalized fractions" | Low-Medium | Verify intent, fix if wrong |
| "no photon production" | Medium | Check if photons needed for MODE |
| "failed X of 10 checks" | High (X>2) | Run longer, improve VR |
| "entropy not converged" | High | More inactive cycles |
| "relative error > 0.50" | High | Run longer, add VR |
| "deprecated syntax" | Low | Note for future update |
| "IEEE inexact trapped" | Low | Usually harmless |
| "particles killed by WW" | Low (<100) | Acceptable, monitor |
| "particles killed by WW" | High (>1000) | Fix weight windows |

## Best Practices

1. **Read All Warnings**: Don't ignore, even if run completes
   ```
   grep -i "warning" outp | less
   ```

2. **Prioritize Statistical Warnings**: Most critical for result validity
   ```
   Check tally fluctuation charts first
   ```

3. **Document Warning Resolution**: Track what warnings mean
   ```
   c WARNING RESOLVED 2024-10-31:
   c   Material 1 unnormalized (2.05 vs 2.0)
   c   Fixed H2O ratio, now exact 2:1
   ```

4. **Trend Analysis**: Watch warnings across multiple runs
   ```
   Run 1: 3 checks failed
   Run 2: 1 check failed  ← Improving
   Run 3: 0 checks failed ← Good
   ```

5. **Understand Context**: Some warnings expected
   ```
   MODE N → "photon production" warning expected
   ```

6. **Set Realistic Goals**:
   ```
   Academic: <1% error, all 10 checks passed
   Engineering: <5% error, ≤1 check missed
   Screening: <10% error, ≤2 checks missed
   ```

7. **Use Warnings to Improve**: Warnings guide optimization
   ```
   High error → Need better VR
   Entropy issues → Need more inactive cycles
   ```

8. **Keep Warning Log**: Track across project
   ```
   warnings.txt:
     2024-10-31: Material 1 normalization warning
     2024-11-01: Resolved with correct fractions
     2024-11-02: Tally 4 high error, added WWG
   ```

9. **Test Warning Fixes**: Verify fix resolves issue
   ```
   Before: Warning X present
   After fix: Warning X gone
   ```

10. **Share Warning Interpretations**: Build team knowledge
    ```
    # Common warnings in this project:
    # - LWTR thermal scattering: Expected, safe
    # - F5 high error: Need WWG per procedure doc
    ```

## References

- **Documentation**:
  - Chapter 4: §4.7 Input Error Messages
  - Chapter 5.13: Output Control and PRINT tables
  - Chapter 3: Introduction (sample problem warnings)
- **Related Skills**:
  - mcnp-statistics-checker (statistical test validation)
  - mcnp-output-parser (warning extraction)
  - mcnp-fatal-error-debugger (escalated warnings)
  - mcnp-tally-analyzer (tally-specific warnings)
  - mcnp-input-validator (prevent warnings)
- **User Manual**:
  - Chapter 4.7: Input Error Messages (warning types)
  - Chapter 2: Monte Carlo Statistics (statistical tests)
  - Chapter 5: Tally Fluctuation Charts (10 checks)

---

**End of MCNP Warning Analyzer Skill**
