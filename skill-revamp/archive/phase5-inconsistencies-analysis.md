# PHASE 5 MASTER PLAN - CRITICAL INCONSISTENCIES IDENTIFIED

**File:** skill-revamp/PHASE-5-MASTER-PLAN.md
**Review Date:** 2025-11-06
**Status:** WILDLY INCONSISTENT - REQUIRES COMPLETE FIX

---

## CRITICAL INCONSISTENCY #1: NUMBER OF SKILLS

### Conflicting Information Within Same Document

| Location | What It Says | Correct? |
|----------|--------------|----------|
| Line 4 (header) | "**Skills:** 8" | ??? |
| Line 35 (parallel section) | "0/8 skills complete (0%)" | ??? |
| Line 53-62 (skill list) | Lists 8 skills | ??? |
| **Line 176 (section header)** | **"## 🛠️ SKILLS TO PROCESS (6 TOTAL)"** | **❌ WRONG** |
| Lines 182-327 | Details ONLY 6 skills | ❌ INCONSISTENT |
| Line 334 | "For EACH of the 6 skills" | ❌ INCONSISTENT |
| Line 392-398 | Execution checklist has 6 skills | ❌ INCONSISTENT |
| Line 401 | "All 6 Phase 5 skills completed" | ❌ INCONSISTENT |
| Line 519 | "Phase 5: 6-8 skills complete" | ❌ VAGUE |

### The Problem

The document simultaneously claims:
- **8 skills** in header and parallel execution section
- **6 skills** in the detailed workflow sections

**Skills listed in parallel section (line 53-62) - 8 TOTAL:**
1. mcnp-fatal-error-debugger
2. mcnp-warning-analyzer
3. mcnp-best-practices-checker
4. mcnp-example-finder
5. mcnp-knowledge-docs-finder
6. mcnp-criticality-analyzer
7. **mcnp-burnup-builder** ← Missing from detailed sections
8. **mcnp-input-updater** ← Missing from detailed sections

**Skills detailed in workflow section (lines 182-327) - 6 TOTAL:**
1. mcnp-fatal-error-debugger ✓
2. mcnp-warning-analyzer ✓
3. mcnp-best-practices-checker ✓
4. mcnp-example-finder ✓
5. mcnp-knowledge-docs-finder ✓
6. mcnp-criticality-analyzer ✓
7. mcnp-burnup-builder ❌ MISSING
8. mcnp-input-updater ❌ MISSING

---

## CRITICAL INCONSISTENCY #2: LINEARIZED WORKFLOW LANGUAGE

### Language That Assumes Sequential Execution

**Line 367:** "- [ ] Phases 1-4 complete (32 skills revamped)"

**Problem:** This assumes Phases 1-4 must be done BEFORE Phase 5. But:
- Line 45-48 says "🚨 CRITICAL: HIGHEST PRIORITY PHASE 🚨... should have been done first"
- Line 38-41 says "Can Execute in Parallel with: ✅ Phase 1, ✅ Phase 2, ✅ Phase 3, ✅ Phase 4"
- Line 43 says "**Dependencies:** NONE - All Phase 5 skills are fully independent"

**This is completely contradictory.**

### Correct Approach for Parallel Execution

Should say something like:
"- [ ] Determine which other phases are in progress or complete
- [ ] Phase 5 has NO dependencies - can start immediately
- [ ] Update GLOBAL-SESSION-REQUIREMENTS.md with Phase 5 status"

---

## CRITICAL INCONSISTENCY #3: OVERLY SPECIFIC LINE REFERENCES

**Line 77:** "Update GLOBAL-SESSION-REQUIREMENTS.md lines 159-182 (Phase 5 section)"
**Line 649:** "GLOBAL-SESSION-REQUIREMENTS.md lines 159-182"

**Problem:** Hardcoded line numbers that will become outdated if GLOBAL-SESSION-REQUIREMENTS.md changes.

**Correct approach:** "Update GLOBAL-SESSION-REQUIREMENTS.md Phase 5 Progress and Summary section"

---

## CRITICAL INCONSISTENCY #4: WRONG/INCOMPLETE SKILL DETAILS

### Missing Skills

If Phase 5 truly has 8 skills (as stated in header and parallel section), then the following sections are INCOMPLETE:

1. **"## 🛠️ SKILLS TO PROCESS" section** (lines 176-327)
   - Missing: mcnp-burnup-builder details
   - Missing: mcnp-input-updater details

2. **"## 📋 PER-SKILL WORKFLOW" section** (line 334)
   - Says "For EACH of the 6 skills" - WRONG if 8 total

3. **"## 🎯 EXECUTION CHECKLIST" section** (lines 392-398)
   - Lists only 6 skills
   - Missing: burnup-builder and input-updater

4. **Phase 5 Completion criteria** (line 401)
   - Says "All 6 Phase 5 skills" - WRONG if 8 total

---

## CRITICAL INCONSISTENCY #5: REFERENCE TO WRONG SKILLS

**Lines 368-371:**
```
- [ ] Check which skills were completed in Phase 1:
  - [ ] mcnp-input-validator - done in Phase 1? [Yes/No]
  - [ ] mcnp-geometry-checker - done in Phase 1? [Yes/No]
  - If done, count as 6 skills in Phase 5, not 8
```

**Problem:** This logic doesn't make sense with the current skill list:
- mcnp-input-validator IS listed as Phase 1 skill (it's a validator)
- mcnp-geometry-checker IS listed as Phase 1 skill (it's a checker)
- But Phase 5 parallel section (lines 53-62) does NOT list these skills
- Instead it lists burnup-builder and input-updater

**This is completely confused.**

---

## ORIGINAL DOCUMENT ANALYSIS

**Original had CONSISTENT information:**
- Said 8 skills in header
- Said "6 TOTAL" in workflow section
- Explained logic: 2 skills (input-validator, geometry-checker) might be done in Phase 1
- Therefore 6-8 skills depending on what was already done
- This made INTERNAL SENSE

**My modifications BROKE this logic:**
- Added parallel section listing 8 specific skills (including burnup-builder, input-updater)
- Did NOT add details for burnup-builder or input-updater
- Did NOT update "6 TOTAL" to "8 TOTAL"
- Did NOT update execution checklist
- Did NOT remove references to input-validator and geometry-checker
- Created COMPLETE INCONSISTENCY

---

## WHAT NEEDS TO BE FIXED

### Option 1: Phase 5 has 8 skills (burnup-builder, input-updater included)

**If this is correct:**
1. Change line 176 from "6 TOTAL" to "8 TOTAL"
2. Add detailed sections for:
   - 7. mcnp-burnup-builder
   - 8. mcnp-input-updater
3. Update line 334 from "6 skills" to "8 skills"
4. Update execution checklist (lines 392-398) to include all 8
5. Update line 401 from "6 Phase 5 skills" to "8 Phase 5 skills"
6. Remove references to input-validator and geometry-checker (lines 368-371)
7. Update contingencies section

### Option 2: Phase 5 has 6 skills (original logic)

**If this is correct:**
1. Remove burnup-builder and input-updater from parallel section (lines 60-61)
2. Change line 35 from "0/8" to "0/6"
3. Restore logic about input-validator and geometry-checker possibly being done in Phase 1
4. Keep "6 TOTAL" at line 176
5. Keep detailed sections as-is (6 skills)

### LINEARIZED LANGUAGE TO FIX (Both Options)

1. Line 367: Remove "Phases 1-4 complete" assumption
2. Replace with parallel-execution-aware language
3. Remove hardcoded line numbers (lines 77, 649)
4. Replace with section references

---

## SEVERITY: CRITICAL

This document is **UNUSABLE** in its current state:
- Claude reading this will not know how many skills to process
- Execution checklist is incomplete
- Contradictory instructions throughout
- Linearized assumptions conflict with parallel execution claims

**USER WAS ABSOLUTELY RIGHT TO BE FURIOUS**

This was a lazy, surface-level modification that broke internal document consistency.
