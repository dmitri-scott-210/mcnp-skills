# COMPREHENSIVE FIX PLAN - ALL PHASE MASTER PLANS

**Created:** 2025-11-06
**Status:** CRITICAL - Must fix before any work continues
**Scope:** Fix all inconsistencies, linearized language, and incorrect information across all 5 PHASE-N-MASTER-PLAN.md files

---

## PHASE 5 CORRECTIONS (CRITICAL)

### Issues Identified
1. **Skill count inconsistency**: Header says 8, detailed sections say 6, parallel section lists 8
2. **Wrong skills added**: burnup-builder and input-updater don't belong in Phase 5
3. **Linearized language**: "Phases 1-4 complete" assumes sequential execution
4. **Hardcoded line numbers**: Lines 77, 649 reference specific line numbers
5. **Missing skill details**: If 8 skills, missing details for 2; if 6 skills, parallel section wrong

### Correct Information (Per User's Edit + SKILL-REVAMP-OVERVIEW.md)
- **Phase 5 has 6 skills:**
  1. mcnp-fatal-error-debugger (Category C)
  2. mcnp-warning-analyzer (Category C)
  3. mcnp-best-practices-checker (Bonus)
  4. mcnp-example-finder (Category F)
  5. mcnp-knowledge-docs-finder (Category F)
  6. mcnp-criticality-analyzer (Bonus)

- **burnup-builder** → Category E → **Phase 3**
- **input-updater** → Category B → **Phase 1**

### Fixes Required for Phase 5
1. Remove burnup-builder and input-updater from parallel section (lines 60-61)
2. Change line 35 from "0/8" to "0/6"
3. Keep line 176 as "6 TOTAL" (already correct per user's edit)
4. Keep detailed sections as-is (already correct per user's edit - 6 skills)
5. Keep line 334 as "6 skills" (already correct per user's edit)
6. Fix linearized language at line 367
7. Remove hardcoded line numbers (lines 77, 649)
8. Verify all references are consistent with 6 skills

---

## PHASE 1 CORRECTIONS

### Check if input-updater should be added
- Category B (Input Editing) skill
- May need to be added to Phase 1 skill list
- Need to verify against current Phase 1 plan

### Linearized Language to Fix
- Any references assuming Phase 1 must complete before Phase 2-5 can start
- Update to parallel-execution-aware language

---

## PHASE 2 CORRECTIONS

### Linearized Language to Fix
- Any references assuming Phase 1 completion
- Update dependencies section to be accurate for parallel execution

---

## PHASE 3 CORRECTIONS

### Check if burnup-builder should be added
- Category E (Advanced Operations) skill
- May need to be added to Phase 3 skill list
- Need to verify against current Phase 3 plan

### Linearized Language to Fix
- Any references assuming previous phases complete
- Update dependencies section accurately

---

## PHASE 4 CORRECTIONS

### Linearized Language to Fix
- Any references assuming previous phases complete
- Update to parallel-execution-aware language

---

## UNIVERSAL FIXES NEEDED (ALL PHASES)

### 1. Remove Linearized Assumptions
**Wrong patterns to find and fix:**
- "After Phase X complete"
- "When Phases 1-N are done"
- "Phases X-Y complete"
- "Previous phases finished"

**Correct patterns:**
- "Check which other phases are in progress"
- "If Phase X is complete" (conditional, not assumption)
- "Phase dependencies: [list actual dependencies]"

### 2. Fix Hardcoded Line Number References
**Pattern:** `GLOBAL-SESSION-REQUIREMENTS.md lines X-Y`
**Replace with:** `GLOBAL-SESSION-REQUIREMENTS.md Phase N Progress and Summary section`

### 3. Verify Parallel Execution Sections
For each phase, verify:
- [ ] Parallel execution section accurately lists skills in that phase
- [ ] Can execute in parallel with: lists are accurate
- [ ] Dependencies are correctly stated
- [ ] Session ID tracking instructions are correct
- [ ] End-of-session requirements reference correct sections (not line numbers)

### 4. Verify Internal Consistency
For each phase, verify:
- [ ] Header skill count matches detailed sections
- [ ] Parallel section skill count matches header
- [ ] Execution checklist has all skills
- [ ] Completion criteria reference correct skill count
- [ ] All skill numbers/IDs are consistent

---

## EXECUTION PLAN

### Step 1: Fix Phase 5 (HIGHEST PRIORITY - Most Broken)
1. Read current PHASE-5-MASTER-PLAN.md completely
2. Apply all Phase 5 corrections listed above
3. Verify internal consistency
4. Test against checklist

### Step 2: Verify and Fix Phase 1
1. Check if input-updater belongs here
2. Fix any linearized language
3. Verify consistency
4. Ensure all Phase 1 skills are correctly listed

### Step 3: Verify and Fix Phase 3
1. Check if burnup-builder belongs here
2. Fix any linearized language
3. Verify consistency
4. Check dependencies are accurate

### Step 4: Fix Phase 2 and 4
1. Fix linearized language
2. Update dependencies to be accurate
3. Verify consistency

### Step 5: Update GLOBAL-SESSION-REQUIREMENTS.md
1. Fix Phase 5 skill list (remove burnup/updater OR confirm they belong there)
2. Verify all phase skill lists match their master plans
3. Ensure all cross-references are correct

### Step 6: Commit All Fixes
- Single comprehensive commit explaining all fixes
- Reference this document in commit message
- Push to branch

---

## VERIFICATION CHECKLIST

After all fixes complete, verify:

### Phase 5
- [ ] Has exactly 6 skills listed consistently everywhere
- [ ] burnup-builder and input-updater removed
- [ ] No linearized language
- [ ] No hardcoded line numbers
- [ ] All internal references consistent

### Phase 1
- [ ] All Category A & B skills listed
- [ ] input-updater included (if it belongs here)
- [ ] No linearized language
- [ ] All internal references consistent

### Phase 3
- [ ] All Category E skills listed
- [ ] burnup-builder included (if it belongs here)
- [ ] No linearized language
- [ ] Dependencies accurately stated

### Phase 2, 4
- [ ] No linearized language
- [ ] Dependencies accurately stated
- [ ] All internal references consistent

### GLOBAL-SESSION-REQUIREMENTS.md
- [ ] Phase 5 lists 6 skills (matches master plan)
- [ ] Phase skill lists match their master plans
- [ ] No inconsistencies between GLOBAL and phase plans

---

## SUCCESS CRITERIA

- ✅ All 5 phase master plans internally consistent
- ✅ No linearized workflow language
- ✅ No hardcoded line number references
- ✅ Skill counts accurate and consistent
- ✅ Skills in correct phases per SKILL-REVAMP-OVERVIEW.md
- ✅ Dependencies accurately stated for parallel execution
- ✅ GLOBAL-SESSION-REQUIREMENTS.md matches all phase plans
- ✅ User can confidently use any phase plan without encountering contradictions

---

**CRITICAL:** This must be done THOROUGHLY and ASSIDUOUSLY, reading every line, not surface-level.
