---
category: C
name: mcnp-best-practices-checker
description: "Review MCNP inputs against the 57-item best practices checklist from Chapter 3.4 to ensure correct and efficient simulations before running"
version: "2.0.0"
---

# MCNP Best Practices Checker

## Overview

This skill systematically reviews MCNP inputs against the comprehensive 57-item best practices checklist from Chapter 3.4. These practices exist because users got wrong answers by skipping them - they are requirements for reliable results, not optional suggestions.

The checklist is organized into four phases: **Setup** (22 items - before first run), **Preproduction** (20 items - during test runs), **Production** (10 items - during long runs), and **Criticality** (5 items - additional for KCODE). Each practice addresses common mistakes that lead to incorrect results, wasted time, or missed errors.

## When to Use This Skill

- **Before ANY MCNP run** (proactive quality assurance)
- After input creation but before running production
- When results seem questionable or unexpected
- Before criticality (KCODE) production runs
- When preparing inputs for publication or licensing
- As final review in validation workflow

## The 57-Item Checklist

### Phase 1: Problem Setup (§3.4.1) - 22 Items

**Before first run - prevents basic errors**

**Geometry (Items 1-7):**
1. Draw geometry picture on paper
2. **ALWAYS plot geometry** (mcnp6 ip) - **CRITICAL**
3. Model in sufficient detail (not too simple, not too complex)
4. Use simple cells (avoid complex Boolean expressions)
5. Use simplest surfaces (prefer RPP, SPH, RCC macrobodies)
6. Avoid excessive # operator (sign of over-complexity)
7. Build incrementally (test each addition)

**Organization (Items 8-9):**
8. Use READ card for common components
9. Pre-calculate volumes/masses (compare with MCNP VOL output)

**Validation (Items 10-13):**
10. **Use VOID card test** - **CRITICAL** (finds overlaps/gaps quickly)
11. Check source (Tables 10, 110, 170)
12. Check source with mesh tally (visual verification)
13. Understand physics approximations and limitations

**Cross Sections & Tallies (Items 14-16):**
14. Cross-section sets matter! (verify libraries in output)
15. Separate tallies for fluctuation (don't combine too much)
16. Conservative variance reduction (start simple)

**General (Items 17-22):**
17. Don't use too many VR techniques (diminishing returns)
18. Balance user vs computer time (don't over-optimize)
19. **Study ALL warnings** - **CRITICAL**
20. Generate best output (PRINT card for detailed tables)
21. Recheck INP file (materials, source, tallies correct?)
22. Garbage in = garbage out (MCNP will run bad inputs!)

**Detailed Explanations:** See `checklist_reference.md` for why each matters and consequences

### Phase 2: Preproduction (§3.4.2) - 20 Items

**During short test runs (10k-100k particles)**

**Understanding (Items 1-3):**
1. Don't use as black box (understand Monte Carlo theory)
2. Run short calculations first (10k-100k for testing)
3. Examine outputs carefully (read entire output)

**Statistics (Items 4-7):**
4. Study summary tables (activity, collisions, tracks)
5. **Study statistical checks** (all 10 must pass) - **CRITICAL**
6. Study FOM and VOV trends (should be stable)
7. Consider collisions/particle (typical: 100-10,000)

**Efficiency (Items 8-12):**
8. Examine track populations (particles getting where needed?)
9. Scan mean-free-path column (identify problem regions)
10. Check detector diagnostics (F5, DXTRAN effectiveness)
11. Understand large contributions (no single particle dominance)
12. Reduce unimportant tracks (kill in unimportant regions)

**Physics (Items 13-14):**
13. Check secondary production (expected numbers?)
14. Back-of-envelope check (does answer make sense?)

**Remaining Items:** See `checklist_reference.md` for Items 15-20

### Phase 3: Production (§3.4.3) - 10 Items

**During long production runs**

**Files (Items 1-2):**
1. Save RUNTPE (for analysis and restarts)
2. Limit RUNTPE size with PRDMP (balance restart vs disk)

**Statistics (Items 3-8):**
3. Check FOM stability (should be roughly constant)
4. Answers seem reasonable (physics intuition)
5. **Examine 10 statistical checks** (ALL must pass) - **CRITICAL**
6. Form valid confidence intervals (understand error bars)
7. Continue-run if necessary (until converged)
8. Verify errors decrease 1/√N (theory validation)

**Final (Items 9-10):**
9. Accuracy has multiple factors (not just statistics!)
10. Adequately sample all cells (check track populations)

### Phase 4: Criticality (§3.4.4) - 5 Items

**Additional for KCODE problems**

1. **Determine inactive cycles** (plot keff and Shannon entropy) - **CRITICAL**
2. Large histories/cycle (minimum 10,000 for production)
3. Examine keff behavior (stable after inactive cycles)
4. At least 100 active cycles (for confidence intervals)
5. Recheck convergence after run (verify inactive sufficient)

## Use Case 1: Pre-Production Review

**Scenario:** User ready to run expensive production calculation

**Workflow:**

**Step 1: Phase 1 Review**
```
Critical Items Check:
✗ Item 2: Geometry not plotted yet
  Action: MUST run `mcnp6 ip i=input.inp` NOW
  Why: Catches 90% of errors before expensive run

✗ Item 10: VOID test not performed
  Action: Run VOID card test with 1M particles
  Why: Quickly finds overlaps/gaps

✓ Item 14: Consistent cross sections (all .80c)
✓ Item 19: No warnings in test run
✓ Item 20: PRINT card included

Assessment: 3/22 critical items incomplete
Action Required: STOP - Complete plotting and VOID test first
Estimated Time: 30 minutes to complete Phase 1
```

**Step 2: Recommendations**
```
BEFORE ANY PRODUCTION RUN:

1. Plot geometry (MANDATORY):
   mcnp6 ip i=input.inp
   # Plot from 3 views minimum (XY, XZ, YZ)
   # Look for dashed lines = errors

2. Run VOID test (MANDATORY):
   [Generate test input with VOID card]
   # If particles lost → geometry error
   # Must pass before production

3. Pre-calculate volumes:
   Expected: ~50,000 cm³ (from drawings)
   Compare: VOL card output after test
   # Large difference (>5%) = geometry error
```

**Step 3: Next Phase**
```
After Phase 1 complete:
→ Run 100k particle test (Phase 2)
→ Check all 10 statistical tests pass
→ Verify FOM stable
→ If passes → Proceed to production
```

## Use Case 2: KCODE Production Setup

**Scenario:** Criticality calculation needs validation

**Additional Checks (Phase 4):**
```
Criticality-Specific Requirements:

1. Shannon entropy convergence:
   Status: Trending upward through cycle 50
   Problem: Source not converged
   Action: Increase inactive cycles to 100

2. Histories per cycle:
   Current: 5,000
   Minimum: 10,000 for production
   Action: Increase to 20,000

3. Active cycles:
   Current: 50
   Minimum: 100
   Action: Increase to 150

KCODE Recommendation:
  Current: KCODE  5000  1.0  50  100
  Required: KCODE  20000  1.0  100  250
```

## Use Case 3: Results Seem Wrong

**Scenario:** Production run complete but results questionable

**Diagnostic Checklist:**
```
Phase 1 Retroactive Check:
□ Was geometry plotted? (Item 2)
□ Was VOID test performed? (Item 10)
□ Were volumes pre-calculated? (Item 9)
□ Were all warnings studied? (Item 19)

Phase 2/3 Statistical Check:
□ Do all 10 statistical tests pass? (Items 2.5, 3.5)
□ Is FOM stable? (Items 2.6, 3.3)
□ Are errors decreasing as 1/√N? (Item 3.8)
□ Back-of-envelope reasonable? (Item 2.14)

If Critical Items Missed:
→ Cannot trust results
→ Must go back and complete checks
→ Rerun after validation
```

## Integration with Other Skills

**Complete Validation Workflow:**
1. **mcnp-input-validator** → Syntax and structure
2. **mcnp-geometry-checker** → Geometry validity
3. **mcnp-physics-validator** → Physics settings
4. **mcnp-best-practices-checker** → Comprehensive review ← **YOU ARE HERE**
5. Run simulation
6. **mcnp-statistics-checker** → Results quality
7. **mcnp-warning-analyzer** → Warning significance
8. **mcnp-tally-analyzer** → Results interpretation

## References

### Comprehensive Guides
- **checklist_reference.md:** Complete 57-item checklist with detailed explanations, why each matters, and consequences of skipping
- **scripts/README.md:** Automated checking tools and workflow guidance

### MCNP Documentation
- **Chapter 3.4:** Tips for Correct and Efficient Problems (source of checklist)
  - §3.4.1: Problem Setup (22 items)
  - §3.4.2: Preproduction (20 items)
  - §3.4.3: Production (10 items)
  - §3.4.4: Criticality (5 items)
- **Chapter 2.6.9:** Tally statistics theory
- **Chapter 6:** Geometry plotting

### Related Skills
- mcnp-input-validator (syntax checking)
- mcnp-geometry-checker (geometry validation)
- mcnp-statistics-checker (statistical quality)
- mcnp-warning-analyzer (warning interpretation)

## Best Practices

1. **Not Optional:** These are requirements, not suggestions
2. **Fix First Error First:** Don't skip validation steps
3. **30 Minutes Now Saves Days Later:** Time spent on validation pays off
4. **"I'm in a Hurry" Not an Excuse:** Wrong faster ≠ better
5. **Document Everything:** Track what you checked and when
6. **Iterative Process:** Expect to revise and revalidate
7. **When in Doubt:** Over-validate rather than under-validate
8. **Phase Order Matters:** Don't skip to Phase 3 without completing Phase 1-2
9. **Critical Items Are Critical:** Items marked CRITICAL must not be skipped
10. **MCNP Will Run Bad Inputs:** You are responsible for validation

## Critical Reminders

**Never Skip:**
- Geometry plotting (Item 1.2) - 90% of errors found here
- VOID card test (Item 1.10) - Finds overlaps/gaps quickly
- All warnings studied (Item 1.19) - May indicate serious issues
- All 10 statistical checks (Items 2.5, 3.5) - Results validity requirement
- Shannon entropy converged (Item 4.1) - Keff reliability requirement

**Remember:**
- MCNP doesn't check physics reasonableness
- No error message ≠ correct answer
- Statistical convergence ≠ accuracy
- You are responsible for ensuring results are right

## Validation Checklist

Before declaring input ready for production:
- [ ] Phase 1 complete (all 22 items addressed)
- [ ] Critical items verified: plotting (2), VOID test (10), warnings (19)
- [ ] Phase 2 test run completed (10k-100k particles)
- [ ] All 10 statistical checks passed
- [ ] FOM stable (±10%)
- [ ] Back-of-envelope check reasonable
- [ ] For KCODE: Shannon entropy converged (flat in final 30% of inactive)
- [ ] For KCODE: At least 100 active cycles planned
- [ ] Documentation complete (what checked, what found, what fixed)

---

**END OF MCNP BEST PRACTICES CHECKER SKILL**

For detailed explanations of each checklist item, consequences, and examples, see checklist_reference.md.
