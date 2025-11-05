# CLAUDE SESSION REQUIREMENTS - MCNP SKILLS REVAMP PROJECT

**Version:** 2.3
**Created:** 2025-11-02
**Last Updated:** 2025-11-04 (Session 16 - ALL TIER 1 SKILLS COMPLETE)

---

## 🚨 CURRENT PROJECT STATE (READ THIS FIRST) 🚨

**Last Updated:** Session 16 - 2025-11-04

### Current Phase Information
- **Active Phase:** Phase 1 (Category A&B - 16 skills)
- **Phase Master Plan:** `PHASE-1-MASTER-PLAN.md`
- **Active Status Document:** `PHASE-1-PROJECT-STATUS-PART-6.md`
- **Session:** 18
- **Tier 1 Skills Complete:** 7/7 (100%) ✅ ALL TIER 1 COMPLETE
- **Tier 2 Skills Complete:** 4/4 (100%) ✅ ALL TIER 2 COMPLETE
  - ✅ mcnp-input-builder (Session 8)
  - ✅ mcnp-geometry-builder (Session 8)
  - ✅ mcnp-material-builder (Session 10)
  - ✅ mcnp-source-builder (Session 13)
  - ✅ mcnp-tally-builder (Sessions 14-15)
  - ✅ mcnp-physics-builder (Session 15)
  - ✅ mcnp-lattice-builder (Session 16)
- **Phase 1 Overall:** 11/16 skills complete (68.75%)
- **Next Tier:** Tier 3 (Validation - 5 skills, 1 complete)

### Critical Context
- **Token budget optimization:** 6-step startup procedure (saves ~10k tokens)
- **Working directory:** ALWAYS verify at session start - c:\Users\dman0\mcnp_projects\ (Lesson #15 - 2 consecutive failures)
- **MCNP format:** Applies to ALL content types (.i, .inp, .txt, .mcnp, .md MCNP snippets)
- **Most violated requirement:** Blank lines in MCNP content (Lesson #11 - 4 incidents)
- **Fundamental requirement:** Documentation must be in YOUR context before gap analysis (Lesson #12)

---

## 🚨 MANDATORY SESSION STARTUP PROCEDURE (7 STEPS) 🚨

**EVERY Claude starting a session on this project MUST follow this 7-step procedure IN ORDER:**

**Total Startup Tokens:** ~85k (optimized through techniques in TOKEN-OPTIMIZATION-BEST-PRACTICES.md)

**VERIFICATION:** After reading all documents, output completed checklist to user before starting work

---

### Step 0: VERIFY WORKING DIRECTORY (CRITICAL - DO THIS FIRST)
**BEFORE reading ANY documents or starting ANY work**

**🚨 MOST CRITICAL STEP - FAILURE LEADS TO REPEATED DIRECTORY ERRORS 🚨**

**Action Required:**
1. Run `pwd` command to verify current working directory
2. Verify output is: `c:\Users\dman0\mcnp_projects` or `c:/Users/dman0/mcnp_projects`
3. If different directory, run: `cd c:/Users/dman0/mcnp_projects`
4. Run `pwd` again to confirm

**Directory Rules (ZERO TOLERANCE):**

✅ **ALWAYS WRITE HERE (WORKING DIRECTORY):**
```
c:\Users\dman0\mcnp_projects\
```
OR HERE

```
c:\Users\dman0\mcnp_projects\skill-revamp
```

**Before EVERY Write Tool Call:**
- [ ] Verify file path AT LEAST starts with `c:\Users\dman0\mcnp_projects\` or `c:/Users/dman0/mcnp_projects/`
- [ ] If path starts with Desktop directory → STOP and correct path
- [ ] Cannot proceed without correct path verification

---

### Step 1: Read SKILL-REVAMP-OVERVIEW.md
**File:** `skill-revamp/SKILL-REVAMP-OVERVIEW.md`
**Purpose:** High-level project strategy, batching approach, quality standards
**Tokens:** ~15k
**Action:** Read entire document for project context and execution phases

**⚠️ Why this first:**
- Provides big-picture understanding of project
- Explains token optimization strategy
- Shows quality standards and success criteria

---

### Step 2: Read Current Phase Master Plan
**File:** As indicated in CURRENT PROJECT STATE section above
**Purpose:** Phase-specific workflows, 11-step per-skill procedure, documentation requirements
**Tokens:** ~20k
**Action:** Read entire phase master plan for current active phase

**⚠️ Why this matters:**
- Contains phase-specific quality standards
- Shows 11-step workflow for skill revamps
- Lists which documentation to reference
- MCNP format verification requirements

---

### Step 3: Read Latest Phase Status Document AND Check Line Count
**File:** As indicated in CURRENT PROJECT STATE section above
**Purpose:** Where previous session ended, what's complete, what's pending
**Tokens:** ~15k
**Action:** Read entire document, focus on session handoff section

**⚠️ MANDATORY LINE COUNT CHECK:**
1. After reading status document, run: `wc -l [status-document-path]`
2. Check line count against 900-line threshold
3. If > 900 lines:
   - Create PHASE-N-PROJECT-STATUS-PART-[X+1].md
   - Update CURRENT PROJECT STATE section (lines 9-33) to reference new part
   - Part X: Retain session summaries and completed skills
   - Part X+1: Active skill progress and remaining skills
4. If >=120 lines away from 900 line length requirement: Continue with current document

**⚠️ Why this matters:**
- Shows exactly where to resume work
- Lists current skill and completion percentage
- Contains critical context for next steps
- Prevents duplicate work
- Ensures document stays manageable (prevents >1,400 line documents)

---

### Step 4: Read LESSONS-LEARNED.md
**File:** `skill-revamp/LESSONS-LEARNED.md`
**Purpose:** 13 documented lessons - prevents repeating mistakes
**Tokens:** ~10k
**Action:** Read entire file before starting work

**⚠️ Most Critical Lessons:**
- **Lesson #12:** Documentation must be in YOUR context before gap analysis (FUNDAMENTAL)
- **Lesson #11:** MCNP format applies to ALL content types - most violated requirement (4 incidents)
- **Lesson #13:** Failed to migrate critical content during deprecation (Session 11)
- **Lesson #1:** Read mandatory startup documents

---

### After Completing All 5 Steps (Steps 0-4):
1. Confirm current phase, skill, and next steps
2. Check token budget (should have ~115k remaining for work)
3. Apply TOKEN-OPTIMIZATION techniques to ALL work in this session
4. Resume work from exactly where previous Claude stopped

---

## PROJECT OVERVIEW

### Purpose
Revamp 36 MCNP Claude skills to meet Anthropic's official standards using the skill-creator skill, incorporating:
1. Comprehensive knowledge base documentation from markdown_docs/ (not fully used originally)
2. Example MCNP files from example_files/ (NOT used originally - critical gap)
3. Progressive disclosure structure (supplemental [reference].md files, scripts/, templates/, example_files OR example_geometry )
4. Streamlined SKILL.md files (<3k words preferred, <5k max)

### Why Revamp Needed
**Original skill creation issues:**
- ❌ Claude Code did not have skill-creator skill installed (now globally available)
- ❌ No [reference].md documentation created (all content in monolithic SKILL.md)
- ❌ No scripts/ subdirectories (Python modules mentioned but not bundled)
- ❌ No key asset subdirectories (no templates or example inputs included)
- ❌ Example files from example_files/ directory NEVER incorporated
- ❌ Some context lost between sessions → quality degradation
- ❌ YAML frontmatter inconsistent (custom fields, not Anthropic standard)

**What's working (preserve these):**
- ✅ Good decision trees in most skills
- ✅ Integration sections connect skills
- ✅ Comprehensive use cases with code examples
- ✅ Clear "When to Use" sections

### Project Scope
- **Total skills to revamp:** 36 (31 required + 5 bonus)
- **Estimated sessions:** 5-7 sessions
- **Estimated total tokens:** ~430k tokens (with batched approach)
- **Key optimization:** Read shared documentation ONCE per category (saves ~85% tokens)

---

## 🚨 CRITICAL: MCNP FORMAT REQUIREMENTS (ALL CONTENT TYPES) 🚨

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

1. **CLAUDE-SESSION-REQUIREMENTS.md** (THIS FILE)
   - Location: `skill-revamp/CLAUDE-SESSION-REQUIREMENTS.md`
   - When: FIRST thing every session
   - Why: Ensures no context loss

2. **Phase-Specific Project Status Documents**
   - **Phase 0:** `skill-revamp/archive/REVAMP-PROJECT-STATUS.md` (infrastructure - ARCHIVED)
   - **Phase 1:** `skill-revamp/PHASE-1-PROJECT-STATUS.md` (16 skills)
   - **Phase 2:** `skill-revamp/PHASE-2-PROJECT-STATUS.md` (6 skills)
   - **Phase 3:** `skill-revamp/PHASE-3-PROJECT-STATUS.md` (4 skills)
   - **Phase 4:** `skill-revamp/PHASE-4-PROJECT-STATUS.md` (6 skills)
   - **Phase 5:** `skill-revamp/PHASE-5-PROJECT-STATUS.md` (8 skills)
   - When: SECOND thing every session (read active phase status per CURRENT PROJECT STATE)
   - Why: Shows current progress, active skill, next steps FOR CURRENT PHASE
   - **Update Frequency:** After major milestones (step completion, file creation) and at session end
   - **Structure:** Each phase status begins with summary of previous phase
   - **🚨 SPLITTING RULE:** When ANY Phase N status document exceeds 900 lines:
     - Create PART N: `PHASE-N-PROJECT-STATUS-PART-N.md`
     - Part N-1: Retain session summary/summaries, completed skills, overall progress
     - Part N: Active skill revamp progress details and remaining skills
     - **IMMEDIATELY update CURRENT PROJECT STATE section (lines 9-33):**
       - Change line 16 "Active Status Document" to reference new PART-N filename
       - This is the ONLY location that should have explicit part number
     - Continue updating Part N until phase N complete or until Part N reaches the 900 line limit.

3. **Phase-Specific Master Plans** (Read for current active phase)
   - **PHASE-1-MASTER-PLAN.md** - Category A&B (16 skills) detailed execution
   - **PHASE-2-MASTER-PLAN.md** - Category D (6 skills) detailed execution
   - **PHASE-3-MASTER-PLAN.md** - Category E (4 skills) detailed execution
   - **PHASE-4-MASTER-PLAN.md** - Category F (6 skills) detailed execution
   - **PHASE-5-MASTER-PLAN.md** - Category C & Specialized (8 skills) detailed execution
   - Location: `skill-revamp/PHASE-N-MASTER-PLAN.md`
   - When: After reading status document (read plan for CURRENT phase only)
   - Why: Phase-specific workflows, documentation requirements, skill ordering
   - **Note:** Each phase has its own master plan - only read the one for current active phase

### Reference Documents (As Needed)

1. **planning-research/*.md** (5 files)
   - anthropic-standards-analysis.md - Skill-creator standards breakdown
   - current-skills-assessment.md - All 36 skills reviewed
   - example-files-inventory.md - 1,107 example files catalogued
   - knowledge-base-map.md - 72 documentation files mapped
   - optimization-strategy.md - Token savings calculations

2. **mcnp-skills-requirements.md**
   - Location: `c:\Users\dman0\mcnp_projects\mcnp-skills-requirements.md`
   - When: Reference for original requirements
   - Why: Understand skill categories, capabilities, success criteria

3. **must-read-docs.md**
   - Location: `c:\Users\dman0\mcnp_projects\must-read-docs.md`
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

**Note:** Detailed token estimates and per-phase workflows are available in the TOKEN MANAGEMENT GUIDELINES section below. Comprehensive execution plans for each phase are in the respective PHASE-N-MASTER-PLAN.md files.

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

## SKILL REVAMP WORKFLOW (PER SKILL)

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
- What templates to add to 
- How to streamline SKILL.md
- Target word count
- Integration improvements

**5. Extract Content to Root Skill Directory (SAME LEVEL AS SKILL.md):**

**CRITICAL STRUCTURE REQUIREMENT:**
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── card_specifications.md            ← Reference files at ROOT level
├── theory_background.md              ← NOT in subdirectory
├── detailed_examples.md              ← Same level as SKILL.md
├── error_catalog.md                  ← Root skill directory
├── [other-topic-specific].md         ← Root skill directory
├── scripts/                          ← Subdirectory for scripts
│   └── [script files]
└── assets/                           ← Subdirectory for examples
    └── [example files]
```

**WRONG Structure (DO NOT DO THIS):**
```
.claude/skills/[skill-name]/
├── SKILL.md
└── references/                       ← WRONG - No subdirectory!
    └── [reference files]             ← Should be at root level
```

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
Create subdirectories: 
- `.claude/skills/[skill-name]/templates/` - Template MCNP input files
- `example_inputs/` or `example_geometries/` - 5-10 relevant examples

**Selection criteria:**
- Relevant to skill's purpose
- Properly formatted and validated
- Range of complexity (basic → advanced)
- Include description/explanation file (.md) for each example

**🚨 MANDATORY:** Before writing ANY MCNP content, complete verification checklist in "CRITICAL: MCNP FORMAT REQUIREMENTS" section (lines 160-268). Complete 3-block structure = EXACTLY 2 blank lines between CELL card block, SURFACE card block, and DATA card blocks; snippets = ZERO blank lines.

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
Run through 25-item quality checklist (see Section below)

**10. Test Skill**
- Invoke skill with Claude Code
- Verify references load correctly
- Test scripts execute
- Validate examples work

---

## QUALITY ASSURANCE CHECKLIST (25 ITEMS)

Before marking any skill as complete, verify ALL items:

### YAML Frontmatter (5 items)
- [ ] 1. `name:` field present and matches skill directory name
- [ ] 2. `description:` field is third-person and trigger-specific
- [ ] 3. No non-standard fields (removed `activation_keywords`, `category`)
- [ ] 4. `version:` field present (use "2.0.0" for revamped skills)
- [ ] 5. `dependencies:` field present if skill uses other CUSTOM SKILLS or external tools

### SKILL.md Structure (10 items)
- [ ] 6. Overview section present (2-3 paragraphs)
- [ ] 7. "When to Use This Skill" section with bulleted conditions
- [ ] 8. Decision tree diagram present (ASCII art)
- [ ] 9. Quick reference table present
- [ ] 10. 3-5 use cases with standardized format
- [ ] 11. Integration section documents connections to other skills
- [ ] 12. References section points to bundled resources
- [ ] 13. Best practices section with 10 numbered items
- [ ] 14. Word count <3k (preferred) or <5k (maximum)
- [ ] 15. No duplication with `reference` document content

### Bundled Resources (7 items)
- [ ] 16. Additional reference .md documents exists with relevant content
- [ ] 17. Large content (>500 words single topic) extracted to supplementary .md files in root skill directory
- [ ] 18. scripts/ directory exists if skill mentions automation
- [ ] 19. Python modules in scripts/ are functional
- [ ] 20. Relevant examples are contained in example_files/
- [ ] 21. templates/ has template files (if applicable)
- [ ] 22. Each example has description/explanation

### Content Quality (3 items)
- [ ] 23. ALL code examples are valid MCNP syntax
- [ ] 24. Cross-references to other skills are accurate
- [ ] 25. Documentation references are correct (file paths, sections)

**If any item fails:** Document issue and fix before proceeding to next skill.

---

## LESSONS-LEARNED UPDATE PROTOCOL

**MANDATORY:** Every time you make a mistake or identify an improvement opportunity, you MUST update LESSONS-LEARNED.md.

### When to Update LESSONS-LEARNED.md

**Trigger events:**
- Any error you made that had to be corrected
- User points out a mistake or oversight
- You identify a pattern that could be prevented
- A requirement was unclear and caused confusion
- An opportunity for process improvement is discovered

### How to Update

1. **STOP current work immediately**
2. **Read LESSONS-LEARNED.md** to understand existing lessons
3. **Identify the appropriate category:**
   - Session Startup Failures
   - Planning and Thinking Ahead
   - MCNP Format Errors
   - Project Management
   - Quality Control
   - Session Startup Protocol
   - MCNP Format Errors (Repeated Violations)
   - Context and Knowledge Management
4. **Add new lesson at top of category** using the template format:
   ```
   #### Lesson #X: [Title] (Session N, Date)
   **What happened:** [Description]
   **Why it was wrong:** [Impact]
   **Root cause:** [Why]
   **How to prevent:** [Actions]
   **Verification:** [Checklist]
   **Status:** [ ] Applied in this session
   ```
5. **Update statistics section** at bottom of LESSONS-LEARNED.md
6. **Increment version number** at top of file
7. **CONTINUE work** with lesson applied

### Lesson Numbering

- Lessons are numbered sequentially across all categories
- Current count: 13 lessons
- Next lesson will be #14
- Do NOT renumber existing lessons

### Quality Standards for Lessons

**Prevention steps must be:**
- Actionable (specific actions to take)
- Verifiable (can check if done)
- Enforceable (documented in workflow)

### Integration with Project Documents

**After adding a lesson:**
- If it affects startup procedure → Update CLAUDE-SESSION-REQUIREMENTS.md
- If it affects skill workflow → Update relevant PHASE-N-MASTER-PLAN.md
- If it affects format requirements → Emphasize in MCNP format section
- If critical → Add to "Most Critical" list in statistics section

---

## PHASE-SPECIFIC PROJECT STATUS UPDATE REQUIREMENTS

### When to Update
**CONTINUOUSLY throughout session for Key Milestones** - NOT just at end
- After reading each documentation file with notes about key information and guidance
- After identifying each discrepancy and developing "skill revamp plan"
- After completing each step (TODOs) of skill revamp plan (skill revamp workflow)
- **Before session ends (CRITICAL)**

### Which File to Update
- Update active Phase N status document (see CURRENT PROJECT STATE section for exact filename)

**Note:** When a status document is split into parts (exceeds 900 lines), CURRENT PROJECT STATE section will specify the active part number.

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
2. Create new PHASE-[N+1]-PROJECT-STATUS.md for next phase
3. New phase status document MUST begin with:
   - Summary of previous phase (key accomplishments, skills completed, lessons learned)
   - Current phase overview
   - Blank "Currently Active Skill" section (to be filled during execution)

---

## TOKEN MANAGEMENT GUIDELINES

### Session Budget
- **Total:** 200,000 tokens per session
- **Reserve:** 15,000-20,000 tokens for session handoff
- **Usable:** ~180,000 tokens per session

### Token Tracking Requirements
Monitor token usage via system messages throughout session:
- Check every 30 minutes of work
- If tokens < 30,000: Begin session handoff procedure

---

## EMERGENCY PROCEDURES

### If Running Out of Tokens (< 26,000 remaining)

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
6. Include directive for next Claude to immediately read `SKILL-REVAMP-OVERVIEW.md` and THIS DOCUMENT at the start of the next session.

**Priority 2: Check Status Accuracy**
- Verify completed skills list is accurate
- Confirm next skill in queue is correct
- Update progress percentages

**Priority 3: Save Partial Work**
- If SKILL.md partially edited: Save with clear "[IN PROGRESS]" marker in filename
- If additional reference .md file partially created: Document what's complete vs pending
- Do NOT leave files in broken state

**Priority 4: Create Handoff Note**
Add to top of active phase status document:
```markdown
## 🚨 URGENT SESSION HANDOFF - TOKEN LIMIT REACHED 🚨
**Previous Session:** [Session N]
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
1. Read SKILL-REVAMP-OVERVIEW.md and current PHASE-N-MASTER-PLAN.md
2. Read mcnp-skills-requirements.md for original requirements
3. Read must-read-docs.md for category documentation map
4. Check planning-research/ files for detailed analysis
5. Read Anthropic skill-creator skill (globally installed)
6. Ask user for clarification if still unclear

**NEVER:**
- Guess at requirements
- Skip reading documentation
- Make assumptions about standards

---

## INTEGRATION WITH GLOBAL SKILLS

### skill-creator Skill (Use Extensively)
**Location:** `C:\Users\dman0\AppData\Roaming\Claude\skills\skill-creator\`
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
   - Every skill should have 5-10 relevant examples in 
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
   - Use full 25-item checklist for each skill
   - Don't skip validation steps

9. **Communicate with User**
   - Report progress at milestones
   - Ask for clarification when needed
   - Show confidence in quality of work

---

## FILE STRUCTURE REFERENCE

### Project Root
```
c:\Users\dman0\mcnp_projects\
├── skill-revamp/                          ← Project directory
│   ├── archive/                           ← Archived documents
│   │   ├── CLAUDE.md (v4.0)               ← Deprecated pointer
│   │   └── REVAMP-PROJECT-STATUS.md       ← Phase 0 complete (archived)
│   ├── CLAUDE-SESSION-REQUIREMENTS.md     ← THIS FILE (mandatory first read)
│   ├── LESSONS-LEARNED.md                 ← 12 lessons (mandatory read)
│   ├── SKILL-REVAMP-OVERVIEW.md           ← High-level guide
│   ├── PHASE-1-MASTER-PLAN.md             ← Phase 1 execution plan
│   ├── PHASE-2-MASTER-PLAN.md             ← Phase 2 execution plan
│   ├── PHASE-3-MASTER-PLAN.md             ← Phase 3 execution plan
│   ├── PHASE-4-MASTER-PLAN.md             ← Phase 4 execution plan
│   ├── PHASE-5-MASTER-PLAN.md             ← Phase 5 execution plan
│   ├── PHASE-1-PROJECT-STATUS.md          ← Phase 1 Part 1 status
│   ├── PHASE-1-PROJECT-STATUS-PART-2.md   ← Phase 1 Part 2 status (ACTIVE)
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
├── .claude/skills/                        ← Original skills (to be revamped)
│   ├── mcnp-input-builder/
│   ├── mcnp-geometry-builder/
│   ├── [... 34 more skills ...]
├── .claude/skills_backup_original/        ← Backup
├── markdown_docs/                         ← Knowledge base
│   ├── user_manual/
│   ├── appendices/
│   ├── examples/
│   ├── theory_manual/
│   └── primers/
├── example_files/                         ← Example MCNP files
│   ├── basic_examples/
│   ├── reactor-model_examples/            ← Most comprehensive
│   ├── [... 7 more categories ...]
├── mcnp-skills-requirements.md            ← Original requirements
├── must-read-docs.md                      ← Documentation map by category
```

---

## SUCCESS CRITERIA

### Project Complete When:
- ✅ All 36 skills revamped to Anthropic standards
- ✅ Every skill has supplementary [reference].md file(s) with extracted content
- ✅ Every skill has example files from `C:\Users\dman0\mcnp_projects\example_files`
- ✅ Applicable skills have scripts/ with bundled Python modules
- ✅ All SKILL.md files are <5k words (ideally <3k)
- ✅ All 36 skills pass 25-item quality checklist
- ✅ Integration map created showing skill connections
- ✅ All testing complete and validated

### Per-Skill Complete When:
- ✅ 25-item quality checklist passed (see QUALITY ASSURANCE CHECKLIST section above)
- ✅ Tested with Claude Code invocation
- ✅ Active phase status document updated

---

## COMMON PITFALLS & KEY PRACTICES

### Documentation Reading
✅ **DO:** Read all required docs per must-read-docs.md for category
❌ **DON'T:** Skip documentation or rely solely on summaries

✅ **DO:** Read primary sources for accuracy
❌ **DON'T:** Rely on previous Claude's notes exclusively

### Status Updates & Context Preservation
✅ **DO:** Update active phase status document continuously (detailed requirements in PHASE-SPECIFIC PROJECT STATUS UPDATE REQUIREMENTS section)
❌ **DON'T:** Batch all updates to end of session

✅ **DO:** Be specific ("extracted card specifications to card_specs.md, lines 1-250 complete")
❌ **DON'T:** Use vague descriptions ("made progress on X")

### Content Organization
✅ **DO:** Extract detailed content to supplementary [reference].md files (content >500 words on single topic)
❌ **DON'T:** Keep all content in monolithic SKILL.md

✅ **DO:** Use imperative/infinitive form ("To accomplish X, do Y")
❌ **DON'T:** Write in second person ("you should...")

### Example Files
✅ **DO:** Add 5-10 relevant examples to every skill's  with description files
❌ **DON'T:** Ignore example_files/ directory or include examples without explanation

### Token Management
✅ **DO:** Read documentation once per category, process all skills in batch
❌ **DON'T:** Re-read same documentation for each skill in category

✅ **DO:** Begin handoff procedure when tokens < 30k
❌ **DON'T:** Continue working without preserving context

### Quality Assurance
✅ **DO:** Complete all 25 items from quality checklist for every skill
❌ **DON'T:** Skip validation steps

✅ **DO:** Verify against documentation, identify discrepancies
❌ **DON'T:** Assume current content is all correct

---

## CURRENT/POST SESSION CHECKLIST

### During Session
3. ✅ Update phase status continuously (detailed requirements: lines 567-640)
4. ✅ Follow MCNP format rules for ALL content (lines 160-268)
5. ✅ Use 25-item quality checklist for each skill (lines 458-495)

### Before Session End
6. ✅ Reserve 15-20k tokens for handoff documentation
7. ✅ Update phase status document with detailed progress
8. ✅ If tokens < 30k: Follow emergency handoff procedure (lines 681-738)

### Project Philosophy
**"Zero Context Loss"** - Every session continues seamlessly through comprehensive documentation. Quality and thoroughness over speed.

---

## VERSION HISTORY

**v1.0 (2025-11-02 - Session 1):**
- Initial creation during infrastructure setup phase
- Established mandatory session startup procedure (originally 7 steps)
- Defined batched processing strategy
- Created comprehensive quality standards
- Implemented emergency procedures for token limits
- Set up continuous status update requirements

---

**END OF CLAUDE-SESSION-REQUIREMENTS.MD**

**Remember:** This document exists to ensure the success of every Claude working on this project. Follow it faithfully, and context will never be lost.

**Next Step:** Follow the 6-step mandatory startup procedure (see Section "MANDATORY SESSION STARTUP PROCEDURE" above).
