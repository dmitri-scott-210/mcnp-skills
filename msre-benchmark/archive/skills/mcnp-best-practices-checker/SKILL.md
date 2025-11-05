---
name: "MCNP Best Practices Checker"
description: "Reviews MCNP inputs against the 57-item best practices checklist from Chapter 3.4 (setup, preproduction, production, criticality). Use before running simulations."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Best Practices Checker

## Overview

MCNP provides comprehensive checklists in Chapter 3.4 for ensuring correct and efficient simulations. This skill reviews user inputs against these requirements across four phases:

1. **Problem Setup** (22 items) - Before first run
2. **Preproduction** (20 items) - During short test runs
3. **Production** (10 items) - During long production runs
4. **Criticality** (5 items) - Additional for KCODE problems

These practices exist because users got wrong answers by skipping them. This skill helps prevent costly mistakes and ensures reliable results.

## Workflow Decision Tree

### When to Invoke
- Before ANY MCNP run (proactive)
- User planning production calculation
- After setup but before running
- When results seem questionable
- For criticality (KCODE) problems

### Review Approach

**Quick Setup Check:**
- Phase 1 only (22 items)
- Before first run
→ Prevents basic setup errors

**Comprehensive Review** (recommended):
- Phase 1 + Phase 2
- Setup + preproduction checks
→ Use before production runs

**Production Monitoring:**
- Phase 3 checks
- During/after production run
→ Verify statistical quality

**Criticality-Specific:**
- Phase 4 checks (+ others)
- For KCODE problems
→ Additional requirements

## Best Practices Review Procedure

### Step 1: Determine Problem Phase
Ask user:
- "What phase are you in?" (setup, testing, production)
- "Is this a criticality problem?" (KCODE)
- "Have you run any simulations yet?"
- "What issues are you encountering?"

### Step 2: Read Reference Materials
**MANDATORY - READ ENTIRE FILE**: Read `.claude/commands/mcnp-best-practices-checker.md` for:
- Complete 57-item checklist
- Explanation of each practice
- Why each matters
- Consequences of ignoring

### Step 3: Review Against Checklist

```python
from parsers.input_parser import MCNPInputParser

parser = MCNPInputParser()
parsed = parser.parse_file('input.inp')

# Check each phase based on user's situation
# Manual review using checklist items
```

### Step 4: Report Checklist Status

Organize by:
1. **CRITICAL MISSING** - Essential items not done
2. **COMPLETED** - Items already done
3. **RECOMMENDATIONS** - Next steps
4. **PHASE-SPECIFIC** - Relevant to current phase

### Step 5: Guide Through Workflow

Help user:
- Understand why each practice matters
- Implement missing items
- Progress through phases systematically
- Avoid common pitfalls

## Phase 1: Problem Setup (§3.4.1)

### 22 Essential Items Before First Run

**Geometry (Items 1-7):**

1. ✓ **Draw geometry picture**
   Why: Visualize before coding
   
2. ✓ **ALWAYS plot geometry**
   Command: `mcnp6 ip i=input.inp`
   Critical: Catches 90% of errors
   
3. ✓ **Model in sufficient detail**
   Balance: Not too simple, not too complex
   
4. ✓ **Use simple cells**
   Avoid: Overly complex Boolean expressions
   
5. ✓ **Use simplest surfaces**
   Prefer: RPP, SPH, RCC macrobodies
   
6. ✓ **Avoid excessive # operator**
   Sign: Overly complex geometry
   
7. ✓ **Build incrementally**
   Test each addition before continuing

**Organization (Items 8-9):**

8. ✓ **Use READ card**
   Store common cards separately
   
9. ✓ **Pre-calculate volumes/masses**
   Compare with MCNP VOL card output

**Validation (Items 10-13):**

10. ✓ **Use VOID card**
    Quickly finds overlaps/gaps
    
11. ✓ **Check source (tables 10, 110, 170)**
    Verify source distribution
    
12. ✓ **Check source with mesh tally**
    Visual verification
    
13. ✓ **Understand physics approximations**
    Know defaults and limitations

**Cross Sections & Tallies (Items 14-16):**

14. ✓ **Cross-section sets matter!**
    Verify loaded libraries in output
    
15. ✓ **Separate tallies for fluctuation**
    Don't combine too much
    
16. ✓ **Conservative variance reduction**
    Start simple

**General (Items 17-22):**

17. ✓ **Don't use too many VR techniques**
    Diminishing returns
    
18. ✓ **Balance user vs computer time**
    Don't over-optimize small problems
    
19. ✓ **Study ALL warnings**
    Don't ignore any
    
20. ✓ **Generate best output (PRINT card)**
    More info = better debugging
    
21. ✓ **Recheck INP file**
    Materials, densities, source correct?
    
22. ✓ **Garbage in = garbage out**
    MCNP will run bad inputs

## Phase 2: Preproduction (§3.4.2)

### 20 Checks During Short Test Runs

**Understanding (Items 1-3):**

1. ✓ **Don't use as black box**
   Understand theory
   
2. ✓ **Run short calculations**
   10k-100k histories for testing
   
3. ✓ **Examine outputs carefully**
   Read all messages

**Statistics (Items 4-7):**

4. ✓ **Study summary tables**
   Activity, collisions, tracks
   
5. ✓ **Study statistical checks**
   All 10 must pass
   
6. ✓ **Study FOM and VOV trends**
   Should be stable
   
7. ✓ **Consider collisions/particle**
   Typical: 100-10,000

**Efficiency (Items 8-12):**

8. ✓ **Examine track populations**
   Particles getting where needed?
   
9. ✓ **Scan mean-free-path column**
   Identify problem regions
   
10. ✓ **Check detector diagnostics**
    F5 and DXTRAN effectiveness
    
11. ✓ **Understand large contributions**
    No single particle dominance
    
12. ✓ **Reduce unimportant tracks**
    Kill in unimportant regions

**Physics (Items 13-14):**

13. ✓ **Check secondary production**
    Expected numbers?
    
14. ✓ **Back-of-envelope check**
    Does answer make sense?

## Phase 3: Production (§3.4.3)

### 10 Checks During Long Runs

**Files (Items 1-2):**

1. ✓ **Save RUNTPE**
   For analysis and restarts
   
2. ✓ **Limit RUNTPE size (PRDMP)**
   Balance restart vs disk space

**Statistics (Items 3-8):**

3. ✓ **Check FOM stability**
   Should be roughly constant
   
4. ✓ **Answers seem reasonable**
   Physics intuition
   
5. ✓ **Examine 10 statistical checks**
   ALL must pass
   
6. ✓ **Form valid confidence intervals**
   Understand error bars
   
7. ✓ **Continue-run if necessary**
   Until converged
   
8. ✓ **Verify errors decrease 1/√N**
   Theory validation

**Final (Items 9-10):**

9. ✓ **Accuracy has multiple factors**
   Not just statistics!
   
10. ✓ **Adequately sample all cells**
    Check track populations

## Phase 4: Criticality (§3.4.4)

### 5 Additional Items for KCODE

1. ✓ **Determine inactive cycles**
   Plot k-eff and Shannon entropy
   
2. ✓ **Large histories/cycle**
   Minimum 10,000 for production
   
3. ✓ **Examine k-eff behavior**
   Stable after inactive cycles
   
4. ✓ **At least 100 active cycles**
   Balance with histories/cycle
   
5. ✓ **Recheck convergence after run**
   Verify inactive cycles sufficient

## Integration with Other Skills

**Complete workflow:**
1. mcnp-input-validator (syntax)
2. mcnp-geometry-checker (geometry)
3. mcnp-physics-validator (physics)
4. mcnp-cross-reference-checker (dependencies)
5. mcnp-best-practices-checker (comprehensive review) ← YOU ARE HERE
6. Run simulation
7. mcnp-statistics-checker (results quality)
8. mcnp-tally-analyzer (interpret results)

## Example Best Practices Review

```
User: "Review my reactor setup before production run"

Claude: I'll review your input against the comprehensive MCNP best practices checklist.

[Reads .claude/commands/mcnp-best-practices-checker.md]
[Reviews input file]

**Phase 1: Problem Setup Review**

CRITICAL ITEMS MISSING:
❌ Item 2: Geometry NOT plotted yet
   Status: No evidence of plotting
   Action: MUST run `mcnp6 ip i=input.inp` NOW
   Why: Catches 90% of errors before expensive run
   Reference: §3.4.1 #2

❌ Item 10: VOID card test not performed
   Status: No VOID test run
   Action: Add VOID card, run 1M particles
   Why: Quickly finds geometry overlaps/gaps
   Reference: §3.4.1 #10

❌ Item 9: Volumes not pre-calculated
   Status: No comparison documented
   Action: Calculate system volume by hand
   Compare: With VOL card output after test run
   Why: Major discrepancies = geometry errors

COMPLETED ITEMS:
✓ Item 1: Geometry drawn (documented in comments)
✓ Item 13: Physics appropriate (MODE N P for reactor)
✓ Item 14: Consistent cross sections (all .80c)
✓ Item 16: Conservative VR (IMP cards only)
✓ Item 19: No warnings in test run
✓ Item 20: PRINT card included

RECOMMENDATIONS:

**BEFORE ANY RUN:**
1. Plot geometry from 3 views MINIMUM
   ```
   mcnp6 ip i=reactor.inp
   
   plot origin=0 0 0 basis=xy extent=100 100
   plot origin=0 0 0 basis=xz extent=100 100
   plot origin=0 0 0 basis=yz extent=100 100
   ```
   Look for dashed lines = errors

2. Run VOID test (ESSENTIAL)
   [Provides complete VOID test setup]

3. Pre-calculate reactor core volume
   Expected: ~50,000 cm³ (based on geometry)
   Verify: Check VOL card output matches

**Phase 2: After Short Test Run (10k histories)**
1. Check all 10 statistical tests passing
2. Verify FOM stability
3. Examine track populations by cell
4. Compare k-eff to expected value

**Phase 3: Production Run Requirements**
1. Only start after Phase 1 & 2 complete
2. Run until all tallies pass 10 checks
3. Save RUNTPE for analysis
4. Monitor FOM remains stable

**Criticality-Specific (KCODE)**
1. Plot k-eff vs cycle number
2. Plot Shannon entropy vs cycle
3. Determine inactive cycles needed
4. Run 100+ active cycles minimum

**Overall Assessment:**
- Setup: 6/22 items complete
- CRITICAL: Cannot run production until plotting and VOID test done
- Estimated time to complete Phase 1: 30 minutes
- Then run short test (Phase 2): 10 minutes
- If passes: Proceed to production

Don't skip these steps! They exist because people got wrong answers.

Would you like me to:
1. Help with geometry plotting?
2. Generate VOID test input?
3. Create Phase 2 checklist?
```

## Important Principles

1. **Not optional suggestions** - Required for reliable results
2. **Skipping = wrong answers** - Not just inefficiency
3. **"I'm in a hurry" not excuse** - Wrong faster ≠ better
4. **Validation is iterative** - Expect revisions
5. **Document what you tried** - Keep good records

## When Users Resist

**Politely but firmly remind:**
- "MCNP will run with bad inputs, results meaningless"
- "These practices prevent wrong answers, not slow you down"
- "30 minutes validation saves days of debugging"
- "Would you rather find errors now or after 1M histories?"

## Code Style

When reviewing practices:
- Reference specific checklist item numbers
- Explain WHY each matters, not just WHAT
- Show consequences of skipping
- Provide concrete next steps
- Balance encouragement with firmness

## Dependencies

Required components:
- Input parser: `parsers/input_parser.py`
- Reference: `.claude/commands/mcnp-best-practices-checker.md`
- Knowledge base: `COMPLETE_MCNP6_KNOWLEDGE_BASE.md`

## References

**Primary Reference:**
- `.claude/commands/mcnp-best-practices-checker.md` - Complete 57-item checklist
- Chapter 3.4: Tips for Correct and Efficient Problems
  - §3.4.1: Problem Setup (22 items)
  - §3.4.2: Preproduction (20 items)
  - §3.4.3: Production (10 items)
  - §3.4.4: Criticality (5 items)

**Supporting References:**
- Chapter 2.6.9: Tally statistics
- Table 2.2: Ten statistical checks
- §3.2.8: VOID card usage
- Chapter 6: Geometry plotting

**Related Skills:**
- mcnp-input-validator
- mcnp-geometry-checker
- mcnp-physics-validator
- mcnp-statistics-checker
- mcnp-plotter
