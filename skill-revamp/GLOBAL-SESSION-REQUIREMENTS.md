# GLOBAL SESSION REQUIREMENTS - MCNP SKILLS REVAMP PROJECT (PARALLEL EXECUTION)

**Version:** 3.0 (Parallel Execution)
**Created:** 2025-11-06
**Purpose:** Coordinate asynchronous/parallelized skill revamp execution across multiple concurrent sessions

---

## 🚨 CRITICAL: PARALLEL EXECUTION OVERVIEW 🚨

**This document enables PARALLEL and ASYNCHRONOUS execution of skill revamps across ALL 5 phases simultaneously.**

### Key Differences from Sequential Execution

**Sequential Approach (Original):**
- Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
- One phase active at a time
- Linear dependency chain

**Parallel Approach (This Document):**
- Multiple phases can be active simultaneously
- Each session works on ONE specific phase
- Phase-specific status tracking with session IDs
- Global coordination through this document

### How Parallel Execution Works

**Session Startup:**
1. User directs Claude to specific phase: "Work on PHASE 5" or "Continue PHASE 2"
2. Claude reads THIS document (GLOBAL-SESSION-REQUIREMENTS.md)
3. Claude reads TOKEN-OPTIMIZATION-BEST-PRACTICES.md
4. Claude reads specific PHASE-N-MASTER-PLAN.md for assigned phase
5. Claude reads specific PHASE-N-PROJECT-STATUS.md (or PART-N) for assigned phase
6. Claude begins work on assigned phase ONLY

**Session Completion:**
1. Claude updates PHASE-N-PROJECT-STATUS.md with session ID
2. Claude updates THIS document's Phase N Progress section
3. Next session can continue same phase OR work on different phase

**Session ID Format:** `Session-YYYYMMDD-HHMMSS-PhaseN` (e.g., Session-20251106-143022-Phase5)

---

## 🚨 CURRENT GLOBAL PROJECT STATE 🚨

**Last Global Update:** Session 20 - 2025-11-05
**Total Progress:** 16/36 skills complete (44.44%)

---

### Phase 1 Progress and Summary

**Status:** ✅ COMPLETE - 16/16 skills complete (100%)
**Category:** A&B - Input Creation & Input Editing
**Latest Status Document:** `PHASE-1-PROJECT-STATUS-PART-6.md`
**Last Updated:** Session 20 - 2025-11-05
**Latest Session ID:** Session-20251105-XXXXXX-Phase1
**Completed:** Session 20 (2025-11-05)

**Tier Progress:**
- **Tier 1 (Core Building):** ✅ 7/7 complete (100%)
  - ✅ mcnp-input-builder
  - ✅ mcnp-geometry-builder
  - ✅ mcnp-material-builder
  - ✅ mcnp-source-builder
  - ✅ mcnp-tally-builder
  - ✅ mcnp-physics-builder
  - ✅ mcnp-lattice-builder

- **Tier 2 (Input Editing):** ✅ 5/5 complete (100%)
  - ✅ mcnp-input-validator
  - ✅ mcnp-geometry-editor
  - ✅ mcnp-input-editor
  - ✅ mcnp-transform-editor
  - ✅ mcnp-variance-reducer

- **Tier 3 (Validation):** ✅ 4/4 complete (100%)
  - ✅ mcnp-cell-checker
  - ✅ mcnp-cross-reference-checker
  - ✅ mcnp-geometry-checker
  - ✅ mcnp-physics-validator

**Skills Remaining:** 0 skills - PHASE 1 COMPLETE ✅

---

### Phase 2 Progress and Summary

**Status:** ⏸️ NOT STARTED - 0/6 skills complete (0%)
**Category:** D - Output Analysis & Mesh
**Latest Status Document:** `PHASE-2-PROJECT-STATUS.md`
**Last Updated:** Not started
**Latest Session ID:** N/A

**Skills Queue:**
1. ⏸️ mcnp-output-parser (NEXT for Phase 2)
2. ⏸️ mcnp-mctal-processor
3. ⏸️ mcnp-mesh-builder
4. ⏸️ mcnp-plotter
5. ⏸️ mcnp-tally-analyzer (partial - complete in Phase 3)
6. ⏸️ mcnp-statistics-checker (partial - complete in Phase 3)

**Skills Remaining:** 6 skills
**Can Execute in Parallel:** Yes, independent of Phase 1 (uses different documentation)
**Documentation Requirements:** Chapter 8, Appendix D (7 files), Appendix E.11

---

### Phase 3 Progress and Summary

**Status:** ⏸️ NOT STARTED - 0/4 skills complete (0%)
**Category:** E - Advanced Operations (VR & Analysis)
**Latest Status Document:** `PHASE-3-PROJECT-STATUS.md`
**Last Updated:** Not started
**Latest Session ID:** N/A

**Skills Queue:**
1. ⏸️ mcnp-tally-analyzer (complete from Phase 2 partial - NEEDS Phase 2 completion)
2. ⏸️ mcnp-statistics-checker (complete from Phase 2 partial - NEEDS Phase 2 completion)
3. ⏸️ mcnp-variance-reducer (complete from Phase 1 partial - CAN start now if Phase 1 docs cached)
4. ⏸️ mcnp-ww-optimizer (NEW - CAN start now)

**Skills Remaining:** 4 skills
**Can Execute in Parallel:** PARTIALLY
- Skills 1-2: Require Phase 2 completion (dependencies)
- Skills 3-4: Can start independently
**Documentation Requirements:** VR theory (new), Phase 2 docs (for skills 1-2)

---

### Phase 4 Progress and Summary

**Status:** ⏸️ NOT STARTED - 0/6 skills complete (0%)
**Category:** F - Utilities & Reference Tools
**Latest Status Document:** `PHASE-4-PROJECT-STATUS.md`
**Last Updated:** Not started
**Latest Session ID:** N/A

**Skills Queue:**
1. ⏸️ mcnp-unit-converter (CAN start now)
2. ⏸️ mcnp-physical-constants (CAN start now)
3. ⏸️ mcnp-isotope-lookup (CAN start now)
4. ⏸️ mcnp-cross-section-manager (CAN start now)
5. ⏸️ mcnp-parallel-configurator (CAN start now)
6. ⏸️ mcnp-template-generator (CAN start now)

**Skills Remaining:** 6 skills
**Can Execute in Parallel:** YES - All skills independent, no dependencies
**Documentation Requirements:** Appendix E (12 files - utility tools)

---

### Phase 5 Progress and Summary

**Status:** ⏸️ NOT STARTED - 0/8 skills complete (0%)
**Category:** C & Specialized - Validation, Debugging, Meta-navigation
**Latest Status Document:** `PHASE-5-PROJECT-STATUS.md`
**Last Updated:** Not started
**Latest Session ID:** N/A

**Skills Queue:**
1. ⏸️ mcnp-fatal-error-debugger (CAN start now - CRITICAL skill)
2. ⏸️ mcnp-warning-analyzer (CAN start now - CRITICAL skill)
3. ⏸️ mcnp-best-practices-checker (CAN start now)
4. ⏸️ mcnp-example-finder (CAN start now)
5. ⏸️ mcnp-knowledge-docs-finder (CAN start now)
6. ⏸️ mcnp-criticality-analyzer (CAN start now)
7. ⏸️ mcnp-burnup-builder (CAN start now)
8. ⏸️ mcnp-input-updater (CAN start now)

**Skills Remaining:** 8 skills
**Can Execute in Parallel:** YES - Most skills independent
**Documentation Requirements:** Minimal (error catalogs, project docs)
**PRIORITY:** HIGH - These are critical validation/debugging skills that should have been done earlier

---

## 🚨 MANDATORY PARALLEL SESSION STARTUP PROCEDURE 🚨

**EVERY Claude starting a parallel execution session MUST follow this procedure:**

### Step 0: Identify Assigned Phase (CRITICAL)

**User will specify which phase to work on. Confirm understanding:**
```
User says: "Work on Phase 5"
Claude confirms: "Understood. I will work on Phase 5 (Category C & Specialized skills)."
```

**Verify working directory:**
```bash
pwd
# Should output: /home/user/mcnp-skills OR /home/user/mcnp-skills/skill-revamp
```

---

### Step 1: Read Assigned Phase Master Plan

**File:** `skill-revamp/PHASE-N-MASTER-PLAN.md` (where N = assigned phase)
**Purpose:** Understand phase-specific workflow and requirements
**Tokens:** ~20k
**Action:** Read entire master plan for assigned phase ONLY

**Phase-specific files:**
- Phase 1: `PHASE-1-MASTER-PLAN.md`
- Phase 2: `PHASE-2-MASTER-PLAN.md`
- Phase 3: `PHASE-3-MASTER-PLAN.md`
- Phase 4: `PHASE-4-MASTER-PLAN.md`
- Phase 5: `PHASE-5-MASTER-PLAN.md`

---

### Step 2: Read Assigned Phase Status Document

**File:** `skill-revamp/PHASE-N-PROJECT-STATUS.md` (or PART-X if split)
**Purpose:** Understand where previous session ended in THIS phase
**Tokens:** ~15k
**Action:** Read entire status document for assigned phase

**Check line count after reading:**
```bash
wc -l skill-revamp/PHASE-N-PROJECT-STATUS.md
```

**If > 900 lines:** Create PHASE-N-PROJECT-STATUS-PART-X.md and update THIS document (Step 8)

---

### Step 3: Read LESSONS-LEARNED.md

**File:** `skill-revamp/LESSONS-LEARNED.md`
**Purpose:** Avoid repeating documented mistakes
**Tokens:** ~10k
**Action:** Read entire file, focus on most critical lessons

---

### Step 4: Generate Unique Session ID

**Format:** `Session-YYYYMMDD-HHMMSS-PhaseN`
**Example:** `Session-20251106-143022-Phase5`

**Store for end-of-session updates.**

---

### Step 5: Verify Phase-Specific Dependencies

**Before starting work on assigned phase, verify:**

**Phase 1:** ✅ No dependencies, can start immediately
**Phase 2:** ✅ No dependencies on Phase 1 (different docs), can start immediately
**Phase 3:**
- ⚠️ Skills 1-2 (tally-analyzer, statistics-checker): Require Phase 2 completion
- ✅ Skills 3-4 (variance-reducer completion, ww-optimizer), Can start immediately (may need to read Phase 1 docs if not cached)
**Phase 4:** ✅ No dependencies, can start immediately
**Phase 5:** ✅ No dependencies, can start immediately (PRIORITY)

**If skill(s)' dependencies not met:**
1. Inform user of dependency requirement(s) and proceed executing Phase for skills with no unresolved dependencies 
3. Update THIS document if dependency discovered

---

### Step 8: Confirm and Begin Work

**Output to user:**
```
✅ Parallel Session Startup Complete

**Assigned Phase:** Phase N
**Session ID:** Session-YYYYMMDD-HHMMSS-PhaseN
**Status Document:** PHASE-N-PROJECT-STATUS.md (or PART-X)
**Skills in Phase:** X total, Y complete, Z remaining
**Next Skill:** [skill-name]
**Dependencies:** [None / Requires Phase X completion]

**Ready to begin work on Phase N.**
```

**Token budget remaining:** ~115k for work (out of 200k total)

---

## 📋 PHASE DEPENDENCY MATRIX

**Use this to determine which phases can execute in parallel:**

| Phase | Can Start Now? | Dependencies | Notes |
|-------|----------------|--------------|-------|
| Phase 1 | ✅ YES | None | Tier 3 skills remain |
| Phase 2 | ✅ YES | None | Independent docs (Chapter 8, Appendix D) |
| Phase 3 (partial) | ✅ YES | Skills 3-4 | Skills 1-2 need Phase 2 complete |
| Phase 4 | ✅ YES | None | All utility skills independent |
| Phase 5 | ✅ YES | None | PRIORITY - Critical validation skills |

**Optimal Parallel Execution Strategy:**
- **Session A:** Complete Phase 1 (3 skills remaining)
- **Session B:** Execute Phase 2 (6 skills, independent)
- **Session C:** Execute Phase 4 (6 skills, independent)
- **Session D:** Execute Phase 5 (8 skills, independent, HIGH PRIORITY)
- **Session E:** Execute Phase 3 after Phase 2 complete (4 skills)

**Total: 4-5 concurrent sessions possible, completing project much faster**

---

## 🚨 END-OF-SESSION REQUIREMENTS (MANDATORY) 🚨

**At the end of EVERY parallel execution session, Claude MUST:**

### Step 1: Update Phase-Specific Status Document

**Update:** `PHASE-N-PROJECT-STATUS.md` (or PART-X if split)

**Add session summary with session ID:**
```markdown
### Session [Session-ID] Summary

**Date:** YYYY-MM-DD
**Session ID:** Session-YYYYMMDD-HHMMSS-PhaseN
**Phase:** N
**Duration:** ~Xk tokens used

**Skills Completed This Session:**
1. [skill-name] - [brief status]
2. [skill-name] - [brief status]

**Skills In Progress:**
- [skill-name]: [% complete, current step]

**Skills Remaining:** X skills

**Next Session Should:**
1. [specific next action]
2. [specific next action]

**Critical Context:**
[Paragraph describing state of work, blockers, considerations]
```

---

### Step 2: Update THIS Document (GLOBAL-SESSION-REQUIREMENTS.md)

**Update the Phase N Progress and Summary section (lines 43-182) with:**

1. **Status:** Update progress (X/Y complete)
2. **Latest Status Document:** Update if created new PART-X
3. **Last Updated:** Current date and session number
4. **Latest Session ID:** Current session ID
5. **Tier Progress / Skills Queue:** Update completion status (✅/🚧/⏸️)
6. **Skills Remaining:** Update count

**Use Edit tool or MCP edit tool for precise changes.**

---

### Step 3: Verify Global Consistency

**Check:**
- [ ] Total progress (sum of all phases) is accurate
- [ ] Phase N progress matches status document
- [ ] Session ID is recorded in both locations
- [ ] Next session guidance is clear

---

### Step 4: Inform User

**Output:**
```
✅ Session Complete

**Phase:** N
**Session ID:** Session-YYYYMMDD-HHMMSS-PhaseN
**Skills Completed:** X
**Progress:** Y/Z skills in Phase N (W% complete)
**Global Progress:** A/36 total skills (B% complete)

**Status documents updated:**
✅ PHASE-N-PROJECT-STATUS.md (or PART-X)
✅ GLOBAL-SESSION-REQUIREMENTS.md

**Next session can:**
- Continue Phase N (Z skills remaining)
- Work on different phase (see dependency matrix)
```

---

## 📊 SKILL REVAMP WORKFLOW (UNIVERSAL - ALL PHASES)

**Every skill in every phase follows this 11-step workflow:**

### 1. Read Current SKILL.md (2k tokens)
### 2. Cross-Reference with Documentation (0k if cached, or read as needed)
### 3. Identify Discrepancies and Gaps (1k tokens)
### 4. Create Skill Revamp Plan (1k tokens)
### 5. Extract Content to Root Skill Directory (2k tokens)
**CRITICAL: Reference .md files at ROOT level, NOT in subdirectories**
### 6. Add Assets to Subdirectories at ROOT (1k tokens)
**CRITICAL: templates/, example_inputs/ DIRECTLY at root - NO assets/ parent**
### 7. Create/Bundle Scripts (1k tokens)
### 8. Streamline SKILL.md (3k tokens)
**Target: <3k words (preferred), <5k words (maximum)**
### 9. Validate Quality - 26-Item Checklist (1k tokens)
### 10. Test Skill (minimal tokens)
### 11. Update PHASE-N-PROJECT-STATUS.md (minimal tokens)

**Total per skill: ~10k tokens**

**See phase-specific master plans for detailed step descriptions.**

---

## 🚨 CRITICAL: MCNP FORMAT REQUIREMENTS (ALL PHASES) 🚨

**EVERY Claude creating ANY MCNP content MUST follow these rules:**

### Three-Block Structure (MANDATORY)

**Complete input files:**
```
Title Card
c Cell Cards
<cell definitions>

c Surface Cards
<surface definitions>

c Data Cards
<data cards>
```

**EXACTLY 2 blank lines total (one after cells, one after surfaces)**

### Format Rules (NEVER VIOLATE)

1. **Block Separators:** EXACTLY ONE blank line between blocks
2. **Within Blocks:** ZERO blank lines
3. **Readability:** Use `c ========` headers, NEVER blank lines
4. **Verification:** Count blank lines before writing ANY MCNP content

### MANDATORY Pre-Write Checklist

**BEFORE writing ANY file with MCNP content:**
- [ ] Invoke relevant completed skills (mcnp-input-builder, mcnp-geometry-builder)
- [ ] Read at least 2 example files from completed skills
- [ ] Verify three-block structure in examples
- [ ] Copy structure pattern (not content)
- [ ] Count blank lines in draft: 2 for complete files, 0 for snippets
- [ ] CANNOT PROCEED without completing verification

**Reference:** LESSONS-LEARNED.md Lesson #11 (MOST VIOLATED - 4 incidents)

---

## 🚨 CRITICAL STRUCTURE REQUIREMENTS (ALL PHASES) 🚨

### Correct Directory Structure (MANDATORY)

```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── [reference].md files              ← At ROOT level (NOT in subdirectories)
├── scripts/                          ← Subdirectory for scripts ONLY
│   └── [script files]
├── templates/                        ← DIRECTLY at root (NOT in assets/)
│   └── [template files]
└── example_inputs/ OR example_geometries/  ← DIRECTLY at root (NOT in assets/)
    └── [example files]
```

### WRONG Structures (NEVER CREATE)

```
❌ WRONG #1: references/ subdirectory
.claude/skills/[skill-name]/
└── references/                       ← WRONG!
    └── [reference files]

❌ WRONG #2: assets/ subdirectory
.claude/skills/[skill-name]/
└── assets/                           ← WRONG! assets/ NEVER EXISTS!
    ├── templates/
    └── example_inputs/
```

**This is item #23 in the 26-item quality checklist: NO assets/ directory (ZERO TOLERANCE)**

---

## 📋 QUALITY ASSURANCE CHECKLIST (26 ITEMS - ALL PHASES)

**Before marking ANY skill complete, verify ALL items:**

### YAML Frontmatter (5 items)
- [ ] 1. `name:` matches skill directory name
- [ ] 2. `description:` is third-person and trigger-specific
- [ ] 3. No non-standard fields
- [ ] 4. `version: "2.0.0"` for revamped skills
- [ ] 5. `dependencies:` if applicable

### SKILL.md Structure (10 items)
- [ ] 6. Overview section (2-3 paragraphs)
- [ ] 7. "When to Use This Skill" with bulleted conditions
- [ ] 8. Decision tree diagram (ASCII art)
- [ ] 9. Quick reference table
- [ ] 10. 3-5 use cases with standardized format
- [ ] 11. Integration section documents connections
- [ ] 12. References section points to bundled resources
- [ ] 13. Best practices section (10 numbered items)
- [ ] 14. Word count <3k (preferred) or <5k (max)
- [ ] 15. No duplication with reference files

### Bundled Resources (8 items)
- [ ] 16. Reference .md files exist at ROOT level
- [ ] 17. Large content (>500 words single topic) extracted
- [ ] 18. scripts/ exists if skill mentions automation
- [ ] 19. Python modules in scripts/ are functional
- [ ] 20. example_inputs/ or example_geometries/ at ROOT with relevant examples
- [ ] 21. templates/ at ROOT with template files (if applicable)
- [ ] 22. Each example has description/explanation
- [ ] 23. **CRITICAL:** NO assets/ directory exists (ZERO TOLERANCE)

### Content Quality (3 items)
- [ ] 24. All code examples are valid MCNP syntax
- [ ] 25. Cross-references to other skills are accurate
- [ ] 26. Documentation references are correct

---

## 🚨 EMERGENCY PROCEDURES (ALL PHASES) 🚨

### If Running Out of Tokens (< 30k remaining)

**STOP ALL WORK IMMEDIATELY**

**Priority 1:** Update PHASE-N-PROJECT-STATUS.md with maximum detail
**Priority 2:** Update THIS document's Phase N section
**Priority 3:** Save partial work clearly marked
**Priority 4:** Create handoff note with session ID
**Priority 5:** Exit gracefully

### If Discovering Cross-Phase Dependencies

**Issue:** Working on Phase X, discover it needs Phase Y completion

**Actions:**
1. Document dependency in PHASE-X-PROJECT-STATUS.md
2. Update THIS document's Phase X section with dependency note
3. Update dependency matrix (lines 203-223)
4. Inform user of dependency
5. Suggest completing prerequisite phase first

### If Phase Status Document Exceeds 900 Lines

**Actions:**
1. Create PHASE-N-PROJECT-STATUS-PART-X.md
2. Move older sessions to previous part
3. Keep current work in new part
4. Update THIS document's Phase N section with new filename
5. Continue work

---

## 📈 LESSONS-LEARNED INTEGRATION

**All lessons from LESSONS-LEARNED.md apply to parallel execution:**

**Most Critical for Parallel Execution:**
- **Lesson #12:** Documentation must be in YOUR context before gap analysis
- **Lesson #11:** MCNP format applies to ALL content types (4 violations)
- **Lesson #15:** Verify working directory FIRST (2 consecutive failures)

**When working in parallel:**
- Each session is independent - cannot rely on other sessions' context
- Each session must load required documentation fresh
- Session IDs prevent confusion about which session did what

---

## 🎯 SUCCESS CRITERIA

### Per-Phase Success
- ✅ All skills in phase processed through 11-step workflow
- ✅ Every skill passes 26-item quality checklist
- ✅ Phase status document reflects accurate completion
- ✅ THIS document updated with phase completion
- ✅ Session ID recorded

### Project Success (All Phases Complete)
- ✅ Phase 1: 16/16 skills complete
- ✅ Phase 2: 6/6 skills complete
- ✅ Phase 3: 4/4 skills complete
- ✅ Phase 4: 6/6 skills complete
- ✅ Phase 5: 8/8 skills complete
- ✅ **Total: 36/36 skills revamped**
- ✅ All quality checklists passed
- ✅ Zero context loss across all sessions
- ✅ Integration complete across all skills

---

## 🔗 INTEGRATION WITH ORIGINAL DOCUMENTS

**Relationship to other project documents:**

- **CLAUDE-SESSION-REQUIREMENTS.md:** Original sequential requirements (reference only)
- **THIS DOCUMENT:** Supersedes for parallel execution coordination
- **PHASE-N-MASTER-PLAN.md:** Phase-specific workflows (read per phase)
- **PHASE-N-PROJECT-STATUS.md:** Phase-specific progress (update per session)
- **TOKEN-OPTIMIZATION-BEST-PRACTICES.md:** Universal optimization techniques
- **LESSONS-LEARNED.md:** Universal lessons and mistakes to avoid

**For parallel execution: Read THIS document + assigned phase documents only.**

---

## 🎊 PROJECT COMPLETION

**When all 5 Phase Progress sections show 100% complete:**

1. Mark global status as COMPLETE
2. Generate final project summary
3. Create skill ecosystem integration map
4. Test all 36 skills for functionality
5. Celebrate! 🎉

**Total Project: 36 skills across 5 phases, completed through parallel asynchronous execution**

---

**END OF GLOBAL-SESSION-REQUIREMENTS.MD**

**Philosophy:** "Parallel Execution with Zero Context Loss Through Phase-Specific Coordination"

**Remember:** Each session works on ONE phase. Update phase status document, then update THIS document. Next session can continue same phase or work on different phase. Dependencies managed through dependency matrix.
