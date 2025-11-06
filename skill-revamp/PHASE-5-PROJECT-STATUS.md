# PHASE 5 PROJECT STATUS - CATEGORY C & SPECIALIZED SKILLS

**Phase:** 5 of 5 (FINAL PHASE)
**Category:** C (Validation) & Specialized (Meta-navigation, Analysis)
**Skills:** 6 total
**Status:** 🚧 IN PROGRESS
**Created:** 2025-11-06 (Session-20251106-000000-Phase5)
**Last Updated:** 2025-11-06

---

## 🎯 PHASE 5 OVERVIEW

### Phase Summary

**Total Skills:** 6 (Category C: Validation + Specialized/Meta Skills)
**Skills Completed:** 0/6 (0%)
**Current Session:** Session-20251106-000000-Phase5

### Why Phase 5 is HIGHEST PRIORITY

From PHASE-5-MASTER-PLAN.md:
- These are validation/debugging skills that should have been prioritized earlier
- mcnp-fatal-error-debugger and mcnp-warning-analyzer are ESSENTIAL
- mcnp-best-practices-checker ensures quality across all skills
- mcnp-example-finder and knowledge-docs-finder help navigate ecosystem
- **ALL Phase 5 skills are fully independent - NO dependencies**

### Skills in Phase 5

**Validation & Debugging (3 skills):**
1. ⏸️ mcnp-fatal-error-debugger (CRITICAL - HIGHEST PRIORITY)
2. ⏸️ mcnp-warning-analyzer (CRITICAL)
3. ⏸️ mcnp-best-practices-checker

**Meta/Navigation Skills (3 skills):**
4. ⏸️ mcnp-example-finder
5. ⏸️ mcnp-knowledge-docs-finder
6. ⏸️ mcnp-criticality-analyzer

---

## 📊 PHASE 5 PROGRESS DASHBOARD

### Overall Progress
- **Skills Completed:** 1/6 (16.67%)
- **Skills In Progress:** 0
- **Skills Remaining:** 5
- **Token Budget:** ~80-100k for all 6 skills
- **Tokens Used This Session:** ~112k tokens
- **Tokens Remaining:** ~88k tokens

### Skills Completion Status

| Skill | Status | Session Completed | Notes |
|-------|--------|-------------------|-------|
| mcnp-fatal-error-debugger | ✅ Complete | Session-20251106-000000-Phase5 | CRITICAL - Done! |
| mcnp-warning-analyzer | 🚧 Next | - | CRITICAL skill - Start next |
| mcnp-best-practices-checker | ⏸️ Pending | - | High value |
| mcnp-example-finder | ⏸️ Pending | - | High value |
| mcnp-knowledge-docs-finder | ⏸️ Pending | - | Medium priority |
| mcnp-criticality-analyzer | ⏸️ Pending | - | Medium priority |

---

## ✅ COMPLETED SKILLS

### 1. mcnp-fatal-error-debugger ✅

**Status:** COMPLETE
**Completed:** 2025-11-06 (Session-20251106-000000-Phase5)
**Priority:** CRITICAL

**Changes Made:**
- **Streamlined SKILL.md:** Reduced from 1,099 lines to 303 lines (~72% reduction)
- **Structure:** Version 2.0.0, proper YAML frontmatter, decision tree, 4 key use cases, integration section
- **Extracted content to 5 reference files at ROOT level:**
  - fatal_error_catalog.md (16k - comprehensive error patterns by category)
  - geometry_error_guide.md (17k - lost particles, overlaps, gaps, VOID test)
  - source_error_guide.md (16k - SDEF errors, invalid dependencies)
  - bad_trouble_guide.md (15k - BAD TROUBLE messages, recovery)
  - debugging_workflow.md (18k - systematic procedures, VOID test, binary search)
- **Created scripts/ directory:**
  - Moved mcnp_fatal_error_debugger.py to scripts/
  - Created scripts/README.md with usage documentation
- **Created example_inputs/ directory:**
  - material_not_defined_error.i (representative example)
- **Quality verified:** NO assets/ directory ✅, all reference files at ROOT ✅

**Token Cost:** ~10k tokens

---

## 🚧 NEXT SKILL

### mcnp-warning-analyzer (CRITICAL - Skill #2)

**Status:** Ready to start
**Priority:** CRITICAL
**Session:** Session-20251106-000000-Phase5

**Skill Overview:**
- **Purpose:** Interpret and address MCNP warning messages
- **Current state:** Needs reading and analysis
- **Target:** Comprehensive warning catalog with significance assessment

**Key Capabilities:**
- Material warnings (negative densities, missing data)
- Physics warnings (energy cutoffs, particle production)
- Statistical warnings (poor convergence)
- Deprecation warnings
- Performance warnings

**References to Create (at ROOT level):**
- warning_catalog.md
- material_warnings.md
- statistical_warnings.md

**Scripts to Bundle:**
- warning_filter.py
- warning_prioritizer.py

**Example Files Needed:**
- Output files with various warnings
- Warning fixes demonstrated

---

## 📋 DOCUMENTATION READING STATUS

### Phase 1 Documentation (Check if Cached)
- [ ] Chapter 3 (MCNP Usage) - May need §3.5-3.6 for errors
- [ ] Chapter 4 (Input Description) - May need §4.7-4.8 for errors
- [ ] Status: Need to verify if cached from Phase 1

### Phase 5-Specific Documentation
- [ ] Source primer error section
- [ ] Project documentation maps (example-files-inventory.md, knowledge-base-map.md)
- [ ] Status: Not yet read

### Reading Strategy for Phase 5
**Different from previous phases:**
- NOT reading all docs upfront
- Read specific docs as needed per skill
- Many skills rely on previous phase knowledge
- Focus on error patterns, debugging, meta-navigation

---

## ✅ COMPLETED SKILLS

**None yet - Phase 5 just started**

---

## 🎯 NEXT SESSION PRIORITIES

### Immediate Next Steps
1. **Read mcnp-fatal-error-debugger SKILL.md** (current state)
2. **Check documentation cache** (Chapter 3-4 from Phase 1)
3. **Read error documentation** (if not cached)
4. **Create skill revamp plan**
5. **Execute 11-step workflow**

### Skills Order (Recommended)
1. mcnp-fatal-error-debugger (CRITICAL - users need this most)
2. mcnp-warning-analyzer (CRITICAL - complement to error debugger)
3. mcnp-best-practices-checker (ensures quality)
4. mcnp-example-finder (high user value)
5. mcnp-knowledge-docs-finder (navigation)
6. mcnp-criticality-analyzer (specialized)

---

## 🚨 CRITICAL REMINDERS FOR PHASE 5

### Structure Requirements (ZERO TOLERANCE)
✅ **CORRECT Structure:**
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── [reference].md files              ← At ROOT level
├── scripts/                          ← Scripts subdirectory at ROOT
│   └── [script files]
└── example_inputs/                   ← DIRECTLY at root (NO assets/)
    └── [example files]
```

❌ **WRONG Structure (NEVER CREATE):**
```
.claude/skills/[skill-name]/
└── assets/                           ← WRONG! NEVER create assets/
    └── example_inputs/               ← Should be at root level
```

**From LESSONS-LEARNED.md Lesson #16:**
- NO assets/ directory - ZERO TOLERANCE
- All subdirectories go DIRECTLY at root level
- Quality checklist item #23: NO assets/ check

### MCNP Format Requirements
**Before writing ANY MCNP content:**
- [ ] Complete 3-block verification
- [ ] Count blank lines (2 for complete files, 0 for snippets)
- [ ] NO blank lines within blocks
- [ ] Use completed skills as references
- [ ] Reference mcnp-input-builder examples

**From LESSONS-LEARNED.md:**
- Lessons #4, #9, #11, #14: Format violations (6 lessons total)
- This is MOST VIOLATED requirement (37.5% of all mistakes)
- MANDATORY verification before Write tool

### Session Management
- Update this document continuously
- Mark todos as completed immediately
- Update GLOBAL-SESSION-REQUIREMENTS.md at session end
- Record session ID in both locations

---

## 📈 TOKEN TRACKING

### Session Token Usage
- **Startup reading:** ~60k tokens
  - GLOBAL-SESSION-REQUIREMENTS.md: ~37k
  - PHASE-5-MASTER-PLAN.md: ~13k
  - LESSONS-LEARNED.md: ~10k
- **Status document creation:** ~2k
- **Remaining for work:** ~140k tokens

### Estimated Token Budget
- **Per skill:** ~10k tokens
- **6 skills:** ~60k tokens
- **Documentation:** ~10-20k (if not cached)
- **Total estimated:** ~80-100k tokens
- **Buffer:** ~40-60k tokens

---

## 🎊 PHASE 5 = PROJECT COMPLETION

### When Phase 5 Complete
- ✅ All 6 Phase 5 skills revamped
- ✅ **ALL 36 SKILLS COMPLETE** 🎉
- ✅ Final integration check
- ✅ Skill ecosystem map created
- ✅ Project SUCCESS!

### Project Status
- **Phase 1:** ✅ 16/16 skills complete (100%)
- **Phase 2:** ⏸️ 0/6 skills complete (0%)
- **Phase 3:** ⏸️ 0/4 skills complete (0%)
- **Phase 4:** ⏸️ 0/6 skills complete (0%)
- **Phase 5:** 🚧 0/6 skills complete (0%)
- **TOTAL:** 16/36 skills complete (44.44%)

---

## 📝 SESSION SUMMARIES

### Session-20251106-000000-Phase5 Summary

**Date:** 2025-11-06
**Session ID:** Session-20251106-000000-Phase5
**Phase:** 5 (Category C & Specialized)
**Duration:** In progress

**Session Startup:**
- ✅ Read GLOBAL-SESSION-REQUIREMENTS.md
- ✅ Read PHASE-5-MASTER-PLAN.md
- ✅ Read LESSONS-LEARNED.md
- ✅ Created PHASE-5-PROJECT-STATUS.md
- ✅ Generated session ID
- ✅ Verified dependencies (NONE)
- ✅ Created TODO list

**Skills Completed This Session:**
1. ✅ mcnp-fatal-error-debugger - Fully revamped with 5 reference files, scripts, examples

**Skills In Progress:**
- None currently

**Skills Remaining:** 5 skills

**Next Session Should:**
1. Read mcnp-fatal-error-debugger current SKILL.md
2. Check documentation cache (Chapter 3-4)
3. Create skill revamp plan
4. Execute 11-step workflow for skill #1
5. Continue with remaining skills

**Critical Context:**
Phase 5 has just begun. All required startup documents have been read. The session is ready to begin work on mcnp-fatal-error-debugger, which is the highest priority critical skill. Phase 5 has NO dependencies and can execute in parallel with all other phases. All 6 skills are independent and can start immediately. Token budget is healthy with ~140k remaining.

---

**END OF PHASE-5-PROJECT-STATUS.md**

**Next update:** After completing mcnp-fatal-error-debugger skill
