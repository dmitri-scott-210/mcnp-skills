# GLOBAL SESSION REQUIREMENTS - MCNP SKILLS REVAMP PROJECT (PARALLEL EXECUTION)

**Version:** 3.0 (Parallel Execution)
**Created:** 2025-11-06
**Purpose:** Coordinate asynchronous/parallelized skill revamp execution across multiple concurrent sessions

---

## 🚨 CRITICAL: Token Optimization Best Practices - MANDATORY FOR ALL SESSIONS🚨 

### MANDATORY TECHNIQUE 1: Parallel Tool Calls

#### The Rule

**When multiple operations are INDEPENDENT (no dependencies), call ALL tools in a SINGLE message.**

**Parallel approach:**
```
Message 1: Tool calls A, B, C (in single message)
Response 1: Results A, B, C (single overhead ~4k tokens)

Total: 1 × 4k overhead = 4k tokens
Savings: 8k tokens (for 3 operations)
```

#### When to Use

✅ **Use parallel calls for:**
- Reading multiple files that don't depend on each other
- Creating multiple files in one step
- Running multiple bash commands (if independent)
- Checking multiple file locations simultaneously

❌ **DO NOT use parallel calls when:**
- Operation B needs result from Operation A
- Order matters (e.g., mkdir before writing file)
- One operation's parameter depends on another's result

#### Example: Reading Documentation

**Session 14 success:**
- Read Chapter 5.09 in 4 chunks: offset 1-800, 801-1600, 1601-2400, 2401-3396
- All 4 Read calls in SINGLE message
- **Saved:** 12k tokens (avoided 3 extra request/response cycles)

#### Example: Creating Reference Files

**If creating files with NO dependencies:**
```
Single message with:
- Write file 1
- Write file 2
- Write file 3
(All independent, no dependencies)

Saves: 8k tokens vs sequential
```

**If files have dependencies:**
```
Sequential required:
- Read existing file → Process → Write new file
(Next file depends on previous result)
```

### MANDATORY TECHNIQUE 2: Direct File Creation

#### The Rule

**Create files directly with Write tool. Do NOT draft content in response text first.**

#### Why it Matters

Maintain comprehensive and detailed doucment creation without outputting it in respone text and wasting significant amounts of session tokens

**Optimized approach:**
```
Minimal response text: "Creating file1.md..."

Write tool with full comprehensive, detailed content in parameter

Result: Content tokenized ONCE (only in write parameter)
Cost: 1,000 tokens per file
Savings: 1,000 tokens per file
```

#### When to Use

✅ **Use direct Write when:**
- Creating reference documents
- Creating template files
- Creating example files
- Content is >500 words

✅ **Show content to user when:**
- User explicitly asks to see it
- Content is <200 words
- User needs to approve before writing

### MANDATORY TECHNIQUE 3: Structured Extraction

#### The Rule

**Read large documentation ONCE, then immediately extract into multiple organized files. Avoid repetitive explanations.**

#### When to Use

✅ **Use structured extraction when:**
- Reading documentation >2,000 lines
- Creating multiple reference files
- Information needs to be organized into categories
- Future sessions will need this information

✅ **Create summary documents:**
- HIGH-level (yet still comprehensive) overview (what's in each file)
- Detailed Key concepts and organization
- Quick reference for future sessions
- Saves future Claudes from re-reading original source

---

### MANDATORY TECHNIQUE 4: Strategic Document Management

### The Rule

**Split documents BEFORE they become unwieldy. Use efficient edit tools. Update only what changed.**

### Why It Matters

**Poor approach:**
```
Status document reaches 1,400 lines
Reading full document: 8k tokens
Editing full document: 8k tokens
Writing full document: 8k tokens
Total per update: 24k tokens
```

**Optimized approach:**
```
Split at 900 lines → PART-4 created
PART-1: Historical (rarely accessed)
PART-2: Active work (frequently updated)

Reading PART-3: 3k tokens
Editing with MCP tool: 1k tokens (precise changes only)
Total per update: 4k tokens
Savings: 20k tokens per update cycle
```

### When to Use

✅ **Split documents when:**
- Status document exceeds 900 lines
- Document has clearly separable sections (historical vs active)
- Frequent updates to only one section

✅ **Use MCP edit tool when:**
- Making targeted changes to large files
- Updating specific sections only
- Correcting small errors

✅ **Use Write tool when:**
- Creating new files
- Complete file replacement needed

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

### How Parallel Execution Works - CRITICAL REQUIREMENTS

**Session Startup:**
1. User directs Claude to specific phase: "Work on PHASE 5" or "Continue PHASE 2"
2. Claude reads THIS document (GLOBAL-SESSION-REQUIREMENTS.md)
3. Claude reads specific PHASE-N-MASTER-PLAN.md for assigned phase
4. Claude reads specific PHASE-N-PROJECT-STATUS.md (or PART-N) for assigned phase
5. Claude begins work on assigned phase ONLY

**Session Completion:**
1. Claude updates PHASE-N-PROJECT-STATUS.md with session ID
2. Claude updates THIS document's Phase N Progress section
3. Next session can continue same phase OR work on different phase

**Session ID Format:** `Session-YYYYMMDD-HHMMSS-PhaseN` (e.g., Session-20251106-143022-Phase5)

---

## 🚨 CURRENT GLOBAL PROJECT STATE 🚨

**Total Progress:** 34/36 skills complete (50.00%)

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
- **Tier 2 (Input Editing):** ✅ 5/5 complete (100%)
- **Tier 3 (Validation):** ✅ 4/4 complete (100%)
**Skills Remaining:** 0 skills - PHASE 1 COMPLETE ✅

---

### Phase 2 Progress and Summary

**Status:** ✅ COMPLETE - 6/6 skills complete (100%)
**Category:** D - Output Analysis & Mesh
**Latest Status Document:** `PHASE-2-PROJECT-STATUS.md`
**Last Updated:** 2025-11-06 (Session Session-20251106-120000-Phase2)
**Latest Session ID:** Session-20251106-120000-Phase2
**Completed:** Session-20251106-120000-Phase2 (2025-11-06)

**Skills Queue:**
1. ✅ mcnp-output-parser (v2.0.0 COMPLETE)
2. ✅ mcnp-mctal-processor (v2.0.0 COMPLETE)
3. ✅ mcnp-mesh-builder (v2.0.0 COMPLETE)
4. ✅ mcnp-plotter (v2.0.0 COMPLETE)
5. ✅ mcnp-tally-analyzer (v1.5.0 PARTIAL - complete in Phase 3)
6. ✅ mcnp-statistics-checker (v1.5.0 PARTIAL - complete in Phase 3)

**Skills Remaining:** 0 skills - PHASE 2 COMPLETE ✅
**Documentation Used:** Chapter 8, Appendix D (7 files), Appendix E.11

---

### Phase 3 Progress and Summary

**Status:** ⏸️ NOT STARTED - 0/4 skills complete (0%)
**Category:** E - Advanced Operations (VR & Analysis)
**Latest Status Document:** `PHASE-3-PROJECT-STATUS.md` (Needs Creation, remove this tag after creating when updating document at end of session)
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

**Status:** ✅ **COMPLETE** - 6/6 skills complete (100%)
**Category:** F - Utilities & Reference Tools
**Latest Status Document:** `PHASE-4-PROJECT-STATUS.md`
**Last Updated:** 2025-11-06 (Session Continued - Phase Complete)
**Latest Session ID:** Session-20251106-120000-Phase4

**Skills Queue:**
1. ✅ mcnp-unit-converter (COMPLETED)
2. ✅ mcnp-physical-constants (COMPLETED)
3. ✅ mcnp-isotope-lookup (COMPLETED)
4. ✅ mcnp-cross-section-manager (COMPLETED)
5. ✅ mcnp-parallel-configurator (COMPLETED)
6. ✅ mcnp-template-generator (COMPLETED)

**Skills Remaining:** 0 skills - **PHASE 4 COMPLETE!**
**Can Execute in Parallel:** YES - All skills independent, no dependencies
**Documentation Requirements:** Appendix E (12 files - utility tools - COMPLETED)

---

### Phase 5 Progress and Summary

**Status:** 🚧 IN PROGRESS - 1/6 skills complete (16.67%)
**Category:** C & Specialized - Validation, Debugging, Meta-navigation
**Latest Status Document:** `PHASE-5-PROJECT-STATUS.md`
**Last Updated:** 2025-11-06 (Session-20251106-000000-Phase5)
**Latest Session ID:** Session-20251106-000000-Phase5

**Skills Queue:**
1. ✅ mcnp-fatal-error-debugger (COMPLETE - 2025-11-06)
2. 🚧 mcnp-warning-analyzer (NEXT - CRITICAL skill)
3. ⏸️ mcnp-best-practices-checker (CAN start now)
4. ⏸️ mcnp-example-finder (CAN start now)
5. ⏸️ mcnp-knowledge-docs-finder (CAN start now)
6. ⏸️ mcnp-criticality-analyzer (CAN start now)

**Skills Remaining:** 5 skills
**Can Execute in Parallel:** YES - All skills independent
**Documentation Requirements:** Minimal (error catalogs, project docs)
**PRIORITY:** HIGH - Critical validation/debugging skills

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

### Step 6: Confirm and Begin Work

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
| Phase 1 | COMLPETED  |
| Phase 2 | ✅ YES | None | Independent docs (Chapter 8, Appendix D) |
| Phase 3 (partial) | ✅ YES | Skills 3-4 | Skills 1-2 need Phase 2 complete |
| Phase 4 | ✅ YES | None | All utility skills independent |
| Phase 5 | ✅ YES | None | PRIORITY - Critical validation skills |

**Total: 4 concurrent sessions possible, completing project much faster**

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

### Step-by-Step Process

**1. Review Current SKILL.md**
- Read existing .claude/skills/[skill-name]/SKILL.md
- Note length, structure, strengths
- Identify what to preserve

**2. Review Knowledge Base Documentation**
- Read required docs per must-read-docs.md for skill's category
- Take notes on key concepts, card specifications, examples
- Identify gaps between current SKILL.md and documentation

**3. Identify Discrepancies and Gaps**
- Missing coverage of topics
- Incorrect or outdated information
- Inconsistencies with documentation
- Areas needing more examples
- Opportunities for improvement

**4. Create Skill Revamp Plan**
- What to extract to additional reference .md documents
- What examples to add from example_files/
- What scripts to create in scripts/
- What templates to add
- How to streamline SKILL.md
- Target word count
- Integration improvements

**5. Extract Content to Root Skill Directory (SAME LEVEL AS SKILL.md):**

**🚨 CRITICAL STRUCTURE REQUIREMENT - ZERO TOLERANCE 🚨**

**CORRECT Structure (MANDATORY):**
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── card_specifications.md            ← Reference files at ROOT level
├── theory_background.md              ← NOT in subdirectory
├── detailed_examples.md              ← Same level as SKILL.md
├── error_catalog.md                  ← Root skill directory
├── [other-topic-specific].md         ← Root skill directory
├── scripts/                          ← Subdirectory for scripts ONLY
│   └── [script files]
├── templates/                        ← Subdirectory at ROOT (NOT in assets/)
│   └── [template files]
└── example_inputs/                   ← Subdirectory at ROOT (NOT in assets/)
    └── [example files]
    OR
└── example_geometries/               ← Skill-specific naming (NOT in assets/)
    └── [geometry files]
```

**❌ WRONG Structures (NEVER DO THESE):**

**WRONG #1: references/ subdirectory**
```
.claude/skills/[skill-name]/
├── SKILL.md
└── references/                       ← WRONG - No subdirectory!
    └── [reference files]             ← Should be at root level
```

**WRONG #2: assets/ subdirectory (MOST COMMON ERROR)**
```
.claude/skills/[skill-name]/
├── SKILL.md
└── assets/                           ← WRONG - assets/ SHOULD NEVER EXIST!
    ├── templates/                    ← Should be at root level
    └── example_inputs/               ← Should be at root level
```

**🚨 CRITICAL RULE: NO assets/ DIRECTORY - EVER! 🚨**

The `assets/` subdirectory should **NEVER** exist in any skill directory. ALL subdirectories (templates/, example_inputs/, example_geometries/, scripts/) must be placed DIRECTLY at the root skill directory level, alongside SKILL.md.

**Why this matters:**
- Violates project-specific structural requirements
- Creates unnecessary nesting
- Inconsistent with completed skills
- Causes confusion for future sessions

**Extract to root skill directory:** `.claude/skills/[skill-name]/`
- card_specifications.md (if applicable)
- theory_background.md (if applicable)
- detailed_examples.md (extensive examples)
- error_catalog.md (comprehensive error patterns)
- [other topic-specific files]

**Guidelines:**
- Reference `.md` files go at ROOT skill directory level (same as SKILL.md)
- Extract content >500 words on single topic
- Extract all card specifications
- Extract theory/mathematical derivations
- Keep SKILL.md lean, references detailed
- NO `references/` subdirectory - files go at root level

**6. Add Example Files and Templates**

**🚨 CRITICAL: Create subdirectories DIRECTLY at root skill level - NO assets/ parent! 🚨**

Create these subdirectories at `.claude/skills/[skill-name]/` (root level):
- `templates/` - Template MCNP input files (DIRECTLY at root, NOT in assets/)
- `example_inputs/` or `example_geometries/` - 5-10 relevant examples (DIRECTLY at root, NOT in assets/)

**Selection criteria:**
- Relevant to skill's purpose (see `planning-research/example-files-inventory.md` for explicit guidance)
- Properly formatted and validated
- Range of complexity (basic → advanced)
- Include description/explanation file (.md) for each example

**🚨 MANDATORY:** Before writing ANY MCNP content, complete verification checklist in "CRITICAL: MCNP FORMAT REQUIREMENTS" section above. Complete 3-block structure = EXACTLY 2 blank lines between CELL card block, SURFACE card block, and DATA card blocks; snippets = ZERO blank lines.

**7. Create/Bundle Scripts in scripts/**
Create subdirectory: `.claude/skills/[skill-name]/scripts/`
- Python automation modules (if applicable)
- Validation scripts
- Helper utilities
- README.md explaining each script

**8. Streamline SKILL.md**
Restructure to Anthropic standards:
```markdown
---
name: skill-name
description: "Third-person, trigger-specific description"
version: "2.0.0"
dependencies: "[if applicable]"
---

# [Skill Name]

## Overview
[2-3 paragraphs - what, why, when]

## When to Use This Skill
[Bulleted list of specific trigger conditions]

## Decision Tree
[ASCII art workflow diagram]

## Quick Reference
[Summary table]

## Use Cases
### Use Case 1: [Title]
**Scenario:** [problem]
**Goal:** [objective]
**Implementation:** [code]
**Key Points:** [bullets]

[Repeat for 3-5 use cases]

## Integration with Other Skills
[Workflow connections]

## References
- Detailed specifications: See `card_specifications.md`
- Theory and background: See `theory_background.md`
- More examples: See `detailed_examples.md`
- Templates: See `templates/`
- Example inputs: See `example_inputs/`
- Automation: See `scripts/README.md`

## Best Practices
[10 numbered items]
```

**Target:** <3k words (preferred), <5k words (maximum)

**9. Validate Quality**
Run through 26-item quality checklist (see Quality Assurance Checklist section below)

**10. Test Skill**
- Invoke skill with Claude Code
- Verify references load correctly
- Test scripts execute
- Validate examples work

**11. Update PHASE-N-PROJECT-STATUS.md**
- Document completion in phase status document
- Update skill count and progress percentages
- Update THIS document's Phase N Progress section

**Total per skill: ~10k tokens**

---

## 🚨 CRITICAL: MCNP FORMAT REQUIREMENTS (ALL PHASES) 🚨

**EVERY Claude creating ANY MCNP content (.i, .inp, .txt, .md snippets) MUST follow these rules:**

**This applies to:** Complete input files, material libraries, code snippets in documentation, templates, examples, and Python-generated MCNP content.

### Three-Block Structure (MANDATORY)

MCNP input files have THREE blocks separated by EXACTLY ONE blank line (TWO BLANK LINES TOTAL):

```
<Title Card - First Line>
c =========================
c Comments allowed here
c
c
c =========================
c
c =========================
c Cell Cards Block
c =========================
c
<cell cards>
c

c =========================
c Surface Cards Block
c =========================
c
<surface cards>
c

c =========================
c Data Cards Block
c =========================
c
<data cards>
c
```

### Format Rules (NEVER VIOLATE THESE)

1. **Block Separators:** EXACTLY ONE blank line between EACH INPUT CARD block
   - ✅ CORRECT: ONE blank line between CELL cards and SURFACE cards
   - ✅ CORRECT: ONE blank line between SURFACE cards and DATA cards
   - ❌ WRONG: TWO or more blank lines BETWEEN input card blocks
   - ❌ WRONG: NO (ZERO) blank line between INPUT CARD blocks
   - ❌ WRONG: ONE or more blank line(s) WITHIN Input card blocks

2. **Three Blocks Required:**
   - Block 1: Cell cards (cells defined with surface and material definitions)
   - Block 2: Surface cards (surface definitions)
   - Block 3: Data cards (MODE, materials, source, tallies, etc.)

3. **Block Order:** Must be Cell → Surface → Data (NEVER EVER change this order)

### MANDATORY Verification Checklist (BEFORE Writing ANY MCNP Content)

**EVERY SINGLE TIME before using Write tool for ANY file/snippet containing MCNP code, you MUST:**

**Step 1: USE COMPLETED SKILLS (NON-NEGOTIABLE - ALWAYS FIRST)**
- [ ] **INVOKE** relevant completed skills using Skill tool:
  - mcnp-input-builder (for overall structure)
  - mcnp-geometry-builder (for geometry examples)
  - mcnp-material-builder (for material examples)
- [ ] **READ** at least 2 example files from completed skills' example_[files]/ subdirectories:
- [ ] **VERIFY** three-block structure in those examples:
  - Title line
  - c Cell Cards section with Header encapsulated in TWO c === separators
  - c
  - Cell definitions
  - c
  - BLANK LINE
  - c
  - c Surface Cards section with Header encapsulated in TWO c === separators
  - c
  - Surface definitions
  - c
  - BLANK LINE
  - c
  - c Data Cards section with Header encapsulated in TWO c === separators
  - c
  - Data cards (MODE, M, SDEF, tallies, NPS)
  - c
- [ ] **COPY** the structure pattern (not content) from completed examples
- [ ] **CANNOT PROCEED** without completing this step

**Step 2: Reference Documentation**
- [ ] Read relevant sections from created skill [reference].md supplemental documentation (mcnp-input-builder, mcnp-geometry-builder)
- [ ] Verify card syntax against knowledge base documentation
- [ ] Check examples from completed skills for correct format

**Step 3: Verify Structure**
- [ ] **VERIFY** three-block structure in those examples:
  - Title line
  - c Cell Cards section with Header encapsulated in TWO c === separators
  - c
  - Cell definitions
  - c
  - BLANK LINE
  - c
  - c Surface Cards section with Header encapsulated in TWO c === separators
  - c
  - Surface definitions
  - c
  - BLANK LINE
  - c
  - c Data Cards section with Header encapsulated in TWO c === separators
  - c
  - Data cards (MODE, M, SDEF, tallies, NPS)
  - c

**Step 4: Verify Syntax**
- [ ] All surface types use correct format (check surface_types_comprehensive.md)
- [ ] All macrobodies use correct parameter count (check macrobodies_reference.md)
- [ ] Cell cards have correct format: `j m d geom params`
- [ ] Material cards reference valid ZAIDs
- [ ] All cross-references valid (surfaces exist, materials defined)

**Step 5: Count Blank Lines**
- [ ] Manually count blank lines in drafted content
- [ ] Verify EXACTLY 2 blank lines total (one after cells, one after surfaces)
- [ ] If more than 2 blank lines, STOP and revise

**This is NON-NEGOTIABLE. Files with incorrect format are INVALID and waste project resources.**

### Common Mistakes to AVOID

❌ **WRONG - Double blank line separator:**
```
5    0    4    IMP:N=0    $ Graveyard

c Blank line separator

c ======================
c Surface Cards
c ======================
```

✅ **CORRECT - Single blank line separator:**
```
5    0    4    IMP:N=0    $ Graveyard

c ======================
c Surface Cards
c ======================
```

### When This Applies - UNIVERSAL SCOPE

**MCNP format verification is required based on CONTENT TYPE (not file extension):**

- ✅ **Complete 3-block input structure** (Cell Cards → blank → Surface Cards → blank → Data Cards) - EXACTLY 2 blank lines, REGARDLESS of file extension (.i, .inp, .txt, .dat, .mcnp, or no extension)
- ✅ **Snippets/partial content** (material definitions, source definitions, geometry sections) - ZERO blank lines within content, REGARDLESS of file extension (.txt, .dat, .md code blocks, Python strings)
- ✅ **All template files** in templates/ - Apply rule based on content (complete structure = 2 blanks, snippet = 0 blanks)
- ✅ **All example files** in example_geometries/ and example_inputs/ - Apply rule based on content
- ✅ **Any MCNP content** in supplemental [reference].md documentation or scripts/ - Apply rule based on content
- ✅ **Python-generated MCNP content** - Scripts that write MCNP content must follow format rules based on what they generate

**Readability separator:** Use TWO encapsulating `c ========` comment headers for visual separation, NEVER blank lines

**Reference:** See LESSONS-LEARNED.md Lesson #11 for comprehensive requirements and 4 documented violations

### Enforcement

- Every example file and template MUST be verified for correct format before commit
- Any file failing this format requirement is INVALID and must be corrected immediately
- This is a ZERO-TOLERANCE requirement - MCNP will not run with incorrect block separators

---

## DOCUMENTATION REQUIREMENTS

### Core Project Documents (Read Every Session)

1. **GLOBAL-SESSION-REQUIREMENTS.md** (THIS FILE)
   - Location: `skill-revamp/GLOBAL-SESSION-REQUIREMENTS.md`
   - When: FIRST thing every session
   - Why: Ensures no context loss, coordinates parallel execution

2. **Phase-Specific Project Status Documents**
   - **Phase 1:** `skill-revamp/PHASE-1-PROJECT-STATUS.md` (may be split into PART-N files)
   - **Phase 2:** `skill-revamp/PHASE-2-PROJECT-STATUS.md`
   - **Phase 3:** `skill-revamp/PHASE-3-PROJECT-STATUS.md`
   - **Phase 4:** `skill-revamp/PHASE-4-PROJECT-STATUS.md`
   - **Phase 5:** `skill-revamp/PHASE-5-PROJECT-STATUS.md`
   - When: SECOND thing every session (read active phase status per CURRENT GLOBAL PROJECT STATE)
   - Why: Shows current progress, active skill, next steps FOR CURRENT PHASE
   - **Update Frequency:** After major milestones (step completion, file creation) and at session end
   - **Structure:** Each phase status begins with summary of previous phase
   - **🚨 SPLITTING RULE:** When ANY Phase N status document exceeds 900 lines:
     - Create PART N: `PHASE-N-PROJECT-STATUS-PART-N.md`
     - Part N-1: Retain session summary/summaries, completed skills, overall progress
     - Part N: Active skill revamp progress details and remaining skills
     - **IMMEDIATELY update Phase N Progress and Summary section in THIS document:**
       - Change "Latest Status Document" field to reference new PART-N filename
       - This is the ONLY location that should have explicit part number
     - Continue updating Part N until phase N complete or until Part N reaches the 900 line limit.

3. **Phase-Specific Master Plans** (Read for current active phase in session)
   - **PHASE-1-MASTER-PLAN.md** - Category A&B (16 skills) detailed execution (COMPLETED)
   - **PHASE-2-MASTER-PLAN.md** - Category D (6 skills) detailed execution
   - **PHASE-3-MASTER-PLAN.md** - Category E (4 skills) detailed execution
   - **PHASE-4-MASTER-PLAN.md** - Category F (6 skills) detailed execution
   - **PHASE-5-MASTER-PLAN.md** - Category C & Specialized (6 skills) detailed execution
   - Location: `skill-revamp/PHASE-N-MASTER-PLAN.md`
   - When: After reading status document (read plan for CURRENT phase only)
   - Why: Phase-specific workflows, documentation requirements, skill ordering
   - **Note:** Each phase has its own master plan - only read the one for current active phase in session

4. **LESSONS-LEARNED.md**
   - Location: `skill-revamp/LESSONS-LEARNED.md`
   - When: During session startup
   - Why: Avoid repeating documented mistakes

### Reference Documents (As Needed)

1. **planning-research/*.md** (5 files)
   - anthropic-standards-analysis.md - Skill-creator standards breakdown
   - current-skills-assessment.md - All 36 skills reviewed
   - example-files-inventory.md - 1,107 example files catalogued
   - knowledge-base-map.md - 72 documentation files mapped
   - optimization-strategy.md - Token savings calculations

2. **mcnp-skills-requirements.md**
   - Location: Root project directory
   - When: Reference for original requirements
   - Why: Understand skill categories, capabilities, success criteria

3. **must-read-docs.md**
   - Location: Root project directory
   - When: Starting each phase (to know which knowledge base docs to read)
   - Why: Maps skill categories to required documentation

---

## BATCHED PROCESSING STRATEGY (TOKEN OPTIMIZATION)

### Key Principle: Read Documentation ONCE Per Category

**Problem:** Sequential approach wastes tokens
- Reading same docs 16 times for Category A/B skills = ~1.5M tokens WASTED

**Solution:** Batched processing by category
- Read Category A/B docs ONCE; take notes on key concepts, card specifications, examples; process all 16 skills = ~80k tokens
- Re-read documentation IF necessary in subsequent sessions.
- **Token savings: 85% (from ~2.4M to ~430k total)**

### Phase Structure

**Note:** Detailed token estimates and per-phase workflows are available in the phase-specific PHASE-N-MASTER-PLAN.md files.

**Phase 1: Category A & B (16 skills)**
- Read ONCE: Chapters 3, 4, all of Chapter 5 (12 files), all of Chapter 10 (5 files)
- Skills: input-builder, geometry-builder, material-builder, source-builder, tally-builder, physics-builder, lattice-builder, geometry-editor, input-editor, input-validator, cell-checker, cross-reference-checker, geometry-checker, physics-validator, transform-editor, variance-reducer

**Phase 2: Category D (6 skills)**
- Read ONCE: Chapter 8, Appendix D (7 files), Appendix E.11
- Skills: output-parser, mctal-processor, mesh-builder, plotter, tally-analyzer (partial), statistics-checker (partial)

**Phase 3: Category E (4 skills)**
- Read ONCE: All Category D docs + variance reduction docs
- Skills: variance-reducer (complete), ww-optimizer, tally-analyzer (complete), statistics-checker (complete)

**Phase 4: Category F (6 skills)**
- Read ONCE: Appendix E (E.1-E.12 utility tools)
- Skills: unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator

**Phase 5: Category C & Specialized (8 skills)**
- Read: Minimal docs, skill-specific
- Skills: fatal-error-debugger, warning-analyzer, criticality-analyzer, best-practices-checker, example-finder, knowledge-docs-finder, burnup-builder, input-updater

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

## TOKEN MANAGEMENT GUIDELINES

Monitor token usage via system messages throughout session:
- Check every 30 minutes of work
- If tokens < 18,000: Begin session handoff procedure

---

## 🚨 EMERGENCY PROCEDURES (ALL PHASES) 🚨

### If Running Out of Tokens (< 18,000 remaining)

**STOP ALL WORK IMMEDIATELY**

**Priority 1: Update Active Phase Status Document**
1. Save current "Currently Active Skill" section with maximum detail
2. Document exactly where reading stopped:
   - File name
   - Line number or section heading
   - What was being processed
3. List key findings from completed portions
4. Specify next steps explicitly
5. Include critical context paragraph
6. Include directive for next Claude to immediately read required documents at the start of the next session.

**Priority 2: Check Status Accuracy**
- Verify completed skills list is accurate
- Confirm next skill in queue is correct
- Update progress percentages in THIS document's Phase N section

**Priority 3: Save Partial Work**
- If SKILL.md partially edited: Save with clear "[IN PROGRESS]" marker in filename
- If additional reference .md file partially created: Document what's complete vs pending
- Do NOT leave files in broken state

**Priority 4: Create Handoff Note**
Add to top of active phase status document:
```markdown
## 🚨 URGENT SESSION HANDOFF - TOKEN LIMIT REACHED 🚨
**Previous Session:** [Session ID]
**Tokens Used:** [X/200,000]
**Status:** Ran out of tokens during [specific task]

**NEXT CLAUDE START HERE:**
1. Read [specific file] starting at line [number]
2. Continue with [specific task description]
3. Current skill is [percentage]% complete
4. After finishing current skill, move to [next skill name]

**Critical Context:**
[Detailed paragraph about state of work]
```

**Priority 5: Exit Gracefully**
- Inform user that session is ending due to token limit
- Confirm that all critical context has been saved
- Recommend continuing in new session

### If Discovering Errors in Revamped Skills

**DO NOT:**
- Delete or overwrite skills without documenting
- Make changes without understanding original intent
- Assume previous Claude made mistakes

**DO:**
1. Document the issue in active phase status document
2. Create "Issues Found" section with:
   - Skill name
   - Specific problem
   - Evidence (quotes, references)
   - Proposed fix
3. Ask user for guidance if uncertain
4. Create fix plan for current or next session

### If Confused About Requirements

**Follow this escalation:**
1. Read GLOBAL-SESSION-REQUIREMENTS.md (THIS file) and current PHASE-N-MASTER-PLAN.md
2. Read mcnp-skills-requirements.md for original requirements
3. Read must-read-docs.md for category documentation map
4. Check planning-research/ files for detailed analysis
5. Read Anthropic skill-creator skill (globally installed)
6. Ask user for clarification if still unclear

**NEVER:**
- Guess at requirements
- Skip reading documentation
- Make assumptions about standards

### If Discovering Cross-Phase Dependencies

**Issue:** Working on Phase X, discover it needs Phase Y completion

**Actions:**
1. Document dependency in PHASE-X-PROJECT-STATUS.md
2. Update THIS document's Phase X Progress section with dependency note
3. Update dependency matrix section
4. Inform user of dependency
5. Suggest completing prerequisite phase first

### If Phase Status Document Exceeds 900 Lines

**Actions:**
1. Create PHASE-N-PROJECT-STATUS-PART-X.md
2. Move older sessions to previous part
3. Keep current work in new part
4. Update THIS document's Phase N Progress section with new filename
5. Continue work

---

## PHASE-SPECIFIC PROJECT STATUS UPDATE REQUIREMENTS

### When to Update
- After reading each documentation file with notes about key information and guidance
- After identifying each discrepancy and developing "skill revamp plan"
- After completing each step (TODOs) of skill revamp plan (skill revamp workflow)
- **Before session ends (CRITICAL)**

### Which File to Update
- Update active Phase N status document (see Phase N Progress and Summary section for exact filename)

**Note:** When a status document is split into parts (exceeds 900 lines), the Phase N Progress section will specify the active part number.

### Active Skill Section Requirements
The "Currently Active Skill" section in PHASE-N-PROJECT-STATUS.md MUST contain:

1. **Phase indicator:** Which phase and what step

2. **Documentation Review Progress:**
   - List each required doc with status (✅ complete, 🚧 in progress, ⏸️ pending)
   - For IN PROGRESS docs: Specify line number or section where stopped
   - Include key findings from completed docs

3. **Discrepancies/Gaps Found:**
   - Numbered list with source, impact, fix needed
   - Specific quotes from current SKILL.md vs documentation

4. **Skill Revamp Plan:**
   - Numbered checklist of all planned changes
   - Status indicators (✅ done, 🚧 in progress, ⏸️ pending)

5. **Token Tracking for This Skill:**
   - Documentation reading
   - Current SKILL.md review
   - Processing steps
   - Total and estimated remaining

6. **Critical Context for Next Session:**
   - Detailed paragraph describing state of work
   - What was just completed
   - What's next
   - Any blockers or considerations

### Completed Skills Section Requirements
Once a skill is finished:
1. Move from "Currently Active Skill" to "Completed Skills" (in same PHASE-N-PROJECT-STATUS.md)
2. Condense to HIGH-LEVEL summary (3-5 bullets)
3. Keep: skill name, changes made, new structure, validation status
4. Remove: Detailed progress tracking, documentation notes, token counts

**Purpose:** Keep document manageable while preserving critical information

### Phase Completion Requirements
When a phase is complete:
1. Create comprehensive summary in PHASE-N-PROJECT-STATUS.md
2. Update THIS document's Phase N Progress and Summary section with completion status
3. Next session can work on different phase or continue with remaining phases

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
- ✅ Phase 4: 6/6 skills complete (COMPLETE - 100%)
- ⏸️ Phase 5: 0/6 skills (NOT STARTED)
- 🔄 **Total: 32/36 skills revamped (88.89%)**
- 🔄 Quality checklists: 32 passed
- ✅ Zero context loss across all sessions
- 🔄 Integration ongoing

---

## 🔗 INTEGRATION WITH ORIGINAL DOCUMENTS

**Relationship to other project documents:**
- **THIS DOCUMENT:** Supersedes for parallel execution coordination
- **PHASE-N-MASTER-PLAN.md:** Phase-specific workflows (read per phase)
- **PHASE-N-PROJECT-STATUS.md:** Phase-specific progress (update per session)
- **LESSONS-LEARNED.md:** Universal lessons and mistakes to avoid

**For parallel execution: Read THIS document + assigned phase documents only.**

---

## INTEGRATION WITH GLOBAL SKILLS

### skill-creator Skill (Use Extensively)
**Location:** Globally installed in Claude Code
**Purpose:** Anthropic's official guide to creating skills
**When to use:**
- Before starting each skill revamp
- When unsure about structure
- For validation of approach
- To understand progressive disclosure

**How to invoke:**
```
I need guidance on skill structure per Anthropic standards
```

### Other Relevant Global Skills
- **docx/pptx/xlsx/pdf skills:** For processing documentation
- **canvas-design:** For creating visual diagrams (decision trees)
- **theme-factory:** If creating styled documentation

---

## BEST PRACTICES FOR THIS PROJECT

1. **Read First, Code Second**
   - Always read required documentation before revamping skill
   - Don't rely on memory or assumptions
   - Document key findings as you read

2. **Preserve What Works**
   - Current skills have good decision trees → keep them
   - Integration sections are valuable → preserve
   - Don't reinvent if current content is good

3. **Extract Aggressively**
   - When in doubt, extract to supplemental [reference].md documentation
   - SKILL.md should be workflow guide, not encyclopedia
   - Detailed specs belong in supplemental [reference].md documentation

4. **Use Examples Liberally**
   - 1,107 example files available → use them
   - Every skill should have 5-10 relevant examples
   - Range from simple to complex

5. **Test As You Go**
   - Don't wait until all 36 skills done
   - Test each skill after revamp
   - Catch issues early

6. **Think About Next Claude**
   - Would another Claude understand where you stopped?
   - Is critical context captured in STATUS document?
   - Are file paths and line numbers specific?

7. **Batch by Category**
   - Read documentation once per category
   - Process all skills in that category together
   - Don't jump between categories unnecessarily

8. **Quality Over Speed**
   - Better to do 5 skills excellently than 10 poorly
   - Use full 26-item checklist for each skill
   - Don't skip validation steps

9. **Communicate with User**
   - Report progress at milestones
   - Ask for clarification when needed
   - Show confidence in quality of work

---

## FILE STRUCTURE REFERENCE

### Project Root
```
mcnp-skills/
├── skill-revamp/                          ← Project directory
│   ├── archive/                           ← Archived documents
│   │   └── REVAMP-PROJECT-STATUS.md       ← Phase 0 complete (archived)
│   ├── GLOBAL-SESSION-REQUIREMENTS.md     ← THIS FILE (mandatory first read)
│   ├── CLAUDE-SESSION-REQUIREMENTS.md     ← Original sequential requirements (reference)
│   ├── LESSONS-LEARNED.md                 ← Documented lessons
│   ├── SKILL-REVAMP-OVERVIEW.md           ← High-level guide
│   ├── PHASE-1-MASTER-PLAN.md             ← Phase 1 execution plan
│   ├── PHASE-2-MASTER-PLAN.md             ← Phase 2 execution plan
│   ├── PHASE-3-MASTER-PLAN.md             ← Phase 3 execution plan
│   ├── PHASE-4-MASTER-PLAN.md             ← Phase 4 execution plan
│   ├── PHASE-5-MASTER-PLAN.md             ← Phase 5 execution plan
│   ├── PHASE-1-PROJECT-STATUS.md          ← Phase 1 status (ARCHIVED)
│   ├── PHASE-2-PROJECT-STATUS.md          ← Phase 2 status
│   ├── PHASE-3-PROJECT-STATUS.md          ← Phase 3 status
│   ├── PHASE-4-PROJECT-STATUS.md          ← Phase 4 status
│   ├── PHASE-5-PROJECT-STATUS.md          ← Phase 5 status
│   ├── planning-research/                 ← Research findings
│   │   ├── anthropic-standards-analysis.md
│   │   ├── current-skills-assessment.md
│   │   ├── example-files-inventory.md
│   │   ├── knowledge-base-map.md
│   │   └── optimization-strategy.md
│   ├── templates/                         ← Skill templates
│   │   ├── skill-template-structure/
│   │   └── revamp-checklist.md
│   └── shared-resources/                  ← Common materials
│       ├── common-references/
│       └── common-examples/
├── .claude/skills/                        ← Skills being revamped
│   ├── mcnp-input-builder/
│   ├── mcnp-geometry-builder/
│   └── [... 34 more skills ...]
├── markdown_docs/                         ← Knowledge base
│   ├── user_manual/
│   ├── appendices/
│   ├── examples/
│   ├── theory_manual/
│   └── primers/
├── example_files/                         ← Example MCNP files
│   ├── basic_examples/
│   ├── reactor-model_examples/
│   └── [... more categories ...]
├── mcnp-skills-requirements.md            ← Original requirements
└── must-read-docs.md                      ← Documentation map by skill category (reference only)
```

---

## COMMON PITFALLS & KEY PRACTICES

### Documentation Reading
✅ **DO:** Read all required docs per must-read-docs.md for category
❌ **DON'T:** Skip documentation or rely solely on summaries

✅ **DO:** Read primary sources for accuracy
❌ **DON'T:** Rely on previous Claude's notes exclusively

### Status Updates & Context Preservation
✅ **DO:** Update active phase status document continuously (see PHASE-SPECIFIC PROJECT STATUS UPDATE REQUIREMENTS section)
❌ **DON'T:** Batch all updates to end of session

✅ **DO:** Be specific ("extracted card specifications to card_specs.md, lines 1-250 complete")
❌ **DON'T:** Use vague descriptions ("made progress on X")

### Content Organization
✅ **DO:** Extract detailed content to supplementary [reference].md files (content >500 words on single topic)
❌ **DON'T:** Keep all content in monolithic SKILL.md

✅ **DO:** Use imperative/infinitive form ("To accomplish X, do Y")
❌ **DON'T:** Write in second person ("you should...")

### Example Files
✅ **DO:** Add 5-10 relevant examples to every skill with description files
❌ **DON'T:** Ignore example_files/ directory or include examples without explanation

### Token Management
✅ **DO:** Read documentation once per category, process all skills in batch
❌ **DON'T:** Re-read same documentation for each skill in category

✅ **DO:** Begin handoff procedure when tokens < 30k
❌ **DON'T:** Continue working without preserving context

### Quality Assurance
✅ **DO:** Complete all 26 items from quality checklist for every skill
❌ **DON'T:** Skip validation steps

✅ **DO:** Verify against documentation, identify discrepancies
❌ **DON'T:** Assume current content is all correct

---

## CURRENT/POST SESSION CHECKLIST

### During Session
1. ✅ Follow parallel session startup procedure
2. ✅ Work on assigned phase only
3. ✅ Update phase status continuously (see PHASE-SPECIFIC PROJECT STATUS UPDATE REQUIREMENTS)
4. ✅ Follow MCNP format rules for ALL content
5. ✅ Use 26-item quality checklist for each skill (including NO assets/ check)

### Before Session End
6. ✅ Reserve 15-20k tokens for handoff documentation
7. ✅ Update phase status document with detailed progress
8. ✅ Update THIS document's Phase N Progress section
9. ✅ Record session ID in both locations
10. ✅ If tokens < 30k: Follow emergency handoff procedure

### Project Philosophy
**"Zero Context Loss Through Parallel Phase Coordination"** - Every session continues seamlessly through comprehensive documentation and phase-specific status tracking. Quality and thoroughness over speed.

---

## VERSION HISTORY

**v1.0 (CLAUDE-SESSION-REQUIREMENTS.md - 2025-11-02 ):**
- Initial creation during infrastructure setup phase
- Established mandatory session startup procedure
- Defined batched processing strategy
- Created comprehensive quality standards
- Implemented emergency procedures for token limits
- Set up continuous status update requirements

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

**Remember:** Each session works on ONE phase. Update phase status document, then update THIS document. Next session can continue same phase or work on different phase. Dependencies managed through dependency matrix.
