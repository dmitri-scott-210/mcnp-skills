# PHASE 1 MASTER PLAN - CATEGORY A & B SKILLS (16 SKILLS)

**Phase:** 1 of 5
**Skills:** 16 (Category A: Input Creation, Category B: Input Editing)
**Estimated Sessions:** 2-3
**Estimated Tokens:** ~240k tokens
**Created:** 2025-11-02 (Session 2)

---

## 🎯 PHASE OVERVIEW

### Objectives
Revamp 16 input-focused skills (Categories A & B) that share the largest documentation overlap. These skills are foundational to MCNP usage and must be completed first due to dependency chains.

### Why This Phase First?
1. **Largest documentation overlap** - 16 skills share the same 20 documentation files
2. **Maximum token savings** - 85% reduction by reading docs once
3. **Foundational dependencies** - Other skills reference these
4. **Most comprehensive** - Input creation is core MCNP functionality

### Token Optimization Strategy
- **Sequential approach:** 16 skills × 90k tokens = 1,440k tokens ❌
- **Batched approach:** 80k (docs once) + 160k (16×10k) = 240k tokens ✅
- **Savings:** 1,200k tokens (83% reduction)

---

## 📚 DOCUMENTATION TO READ (ONCE AT PHASE START)

### Required Reading List

Read these documents **ONE TIME** at the beginning of Phase 1, before processing any skills:

#### Core Usage Chapters (2 files)
1. **markdown_docs/user_manual/03_Introduction_to_MCNP_Usage.md**
   - Purpose: Basic MCNP concepts, file structure, execution
   - Key content: Three-block structure, basic syntax, command line
   - Token estimate: ~8k

2. **markdown_docs/user_manual/04_Description_of_MCNP6_Input.md**
   - Purpose: Input file format, card types, continuation
   - Key content: Format specifications, comments, character limits
   - Token estimate: ~10k

#### Chapter 5: Input Cards (12 files) - THE BIG ONE
Location: `markdown_docs/user_manual/chapter_05_input_cards/`

3. **05_01_Geometry_Specification_Intro.md**
   - Purpose: Geometry overview, cells, surfaces, bodies
   - Token estimate: ~5k

4. **05_02_Cell_Cards.md**
   - Purpose: Cell card format, material assignment, importance
   - Key content: Cell parameters, universe, fill, lattice
   - Token estimate: ~12k

5. **05_03_Surface_Cards.md**
   - Purpose: All surface types, equations, transformations
   - Key content: Planes, spheres, cylinders, cones, quadrics, macrobodies
   - Token estimate: ~15k

6. **05_04_Data_Cards_Intro.md**
   - Purpose: Data card overview
   - Token estimate: ~3k

7. **05_05_Geometry_Data_Cards.md**
   - Purpose: TR (transformations), U (universe), LAT, FILL
   - Key content: Transformation matrices, repeated structures
   - Token estimate: ~8k

8. **05_06_Material_Data_Cards.md**
   - Purpose: M (materials), MT (S(α,β)), MX (cross-sections)
   - Key content: ZAID format, densities, thermal scattering
   - Token estimate: ~10k

9. **05_07_Physics_Data_Cards.md**
   - Purpose: MODE, PHYS, CUT, TMP cards
   - Key content: Particle transport, energy cutoffs, physics models
   - Token estimate: ~12k

10. **05_08_Source_Data_Cards.md**
    - Purpose: SDEF, SSR, KCODE, source distributions
    - Key content: SI/SP/SB, energy/spatial/directional distributions
    - Token estimate: ~14k

11. **05_09_Tally_Data_Cards.md**
    - Purpose: F1-F8 tallies, segmentation, multipliers
    - Key content: Flux, current, heating, pulse height
    - Token estimate: ~15k

12. **05_10_Tally_Perturbations.md**
    - Purpose: FM (multipliers), FU (user bins), FC (comments)
    - Key content: Dose functions, energy bins, time bins
    - Token estimate: ~8k

13. **05_11_Mesh_Tallies.md**
    - Purpose: FMESH, TMESH specifications
    - Key content: Rectangular/cylindrical/spherical mesh
    - Token estimate: ~10k

14. **05_12_Variance_Reduction_Cards.md**
    - Purpose: IMP, WWN, WWE, WWP, DXTRAN, forced collisions
    - Key content: Weight windows, importance, biasing
    - Token estimate: ~12k

15. **05_13_Output_Control_Misc.md**
    - Purpose: PRINT, PRDMP, FILES, DBCN
    - Key content: Output control, dump files, debugging
    - Token estimate: ~8k

#### Chapter 10: Examples (5 files)
Location: `markdown_docs/examples/chapter_10/`

16. **10_01_Geometry_Examples.md**
    - Purpose: Practical geometry construction examples
    - Token estimate: ~10k

17. **10_02_Tally_Examples.md**
    - Purpose: Tally setup examples
    - Token estimate: ~10k

18. **10_03_Source_Examples.md**
    - Purpose: Source definition examples
    - Token estimate: ~10k

19. **10_05_Physics_Models.md**
    - Purpose: Physics configuration examples
    - Token estimate: ~8k

20. **10_06_Variance_Reduction_Examples.md**
    - Purpose: VR technique examples
    - Token estimate: ~10k

### Total Documentation
- **Files:** 20 documents
- **Estimated tokens:** ~200k tokens (accounting for formatting)
- **Read:** ONCE at phase start
- **Reuse:** For all 16 skills in this phase

---

## 🛠️ SKILLS TO PROCESS (16 TOTAL)

### Processing Order (By Dependency)

Process skills in this order to maintain logical flow and dependency chains:

#### Tier 1: Core Input Building (7 skills)
**Dependencies:** None - These are foundational
**ALL Example Files Located at:** `C:\Users\dman0\mcnp_projects\example_files\`

1. **mcnp-input-builder** (Category A)
   - **Priority:** HIGHEST - Do this first
   - **Why:** Most foundational skill, referenced by all others
   - **Current:** 1,041 lines
   - **Focus:** Overall input structure, three-block format
   - **Examples needed:** basic_examples/simple*.txt, reactor-model_examples/agr-1/bench_*.i

2. **mcnp-geometry-builder** (Category A)
   - **Priority:** High - Needed by many others
   - **Current:** 1,087 lines
   - **Focus:** Cell and surface cards, Boolean logic
   - **Examples needed:** basic_examples/shield*.txt, reactor-model_examples with complex geometry

3. **mcnp-material-builder** (Category A)
   - **Priority:** High
   - **Current:** ~900 lines (estimate)
   - **Focus:** M/MT/MX cards, ZAID format
   - **Examples needed:** reactor-model_examples with fuel materials

4. **mcnp-source-builder** (Category A)
   - **Priority:** High
   - **Current:** ~950 lines (estimate)
   - **Focus:** SDEF, KCODE, distributions
   - **Examples needed:** criticality_examples/, basic_examples/src*.txt

5. **mcnp-tally-builder** (Category A)
   - **Priority:** High
   - **Current:** ~1,000 lines (estimate)
   - **Focus:** F1-F8 tallies, FM, energy bins
   - **Examples needed:** basic_examples/tal*.txt

6. **mcnp-physics-builder** (Category A)
   - **Priority:** Medium
   - **Current:** ~850 lines (estimate)
   - **Focus:** MODE, PHYS, CUT, TMP cards
   - **Examples needed:** Various reactor-model_examples

7. **mcnp-lattice-builder** (Category E, but shares A/B docs)
   - **Priority:** Medium
   - **Current:** ~900 lines (estimate)
   - **Focus:** U/LAT/FILL, repeated structures
   - **Examples needed:** various intermediate_examples/, /intermediate_examples/critsrc.txt

#### Tier 2: Input Editing (4 skills)
**Dependencies:** Tier 1 skills

8. **mcnp-geometry-editor** (Category B)
   - **Priority:** Medium
   - **Dependencies:** geometry-builder
   - **Current:** ~950 lines (estimate)
   - **Focus:** Modifying existing geometry

9. **mcnp-input-editor** (Category B)
   - **Priority:** Medium
   - **Dependencies:** input-builder
   - **Current:** ~900 lines (estimate)
   - **Focus:** Systematic input modifications

10. **mcnp-transform-editor** (Category B)
    - **Priority:** Medium
    - **Dependencies:** geometry-builder
    - **Current:** ~850 lines (estimate)
    - **Focus:** TR card creation and modification

11. **mcnp-variance-reducer** (Category B)
    - **Priority:** Medium-High
    - **Dependencies:** input-builder, tally-builder
    - **Current:** 1,006 lines
    - **Focus:** Basic VR techniques (IMP, weight windows)
    - **Note:** Will be completed further in Phase 3

#### Tier 3: Validation (5 skills)
**Dependencies:** All Tier 1, most Tier 2

12. **mcnp-input-validator** (Category C)
    - **Priority:** High for validation
    - **Dependencies:** input-builder, all card builders
    - **Current:** ~1,100 lines (estimate)
    - **Focus:** Pre-simulation validation

13. **mcnp-cell-checker** (Category C)
    - **Priority:** Medium
    - **Dependencies:** geometry-builder
    - **Current:** ~800 lines (estimate)
    - **Focus:** Cell card validation, U/FILL references

14. **mcnp-cross-reference-checker** (Category C)
    - **Priority:** Medium
    - **Dependencies:** input-validator
    - **Current:** ~850 lines (estimate)
    - **Focus:** Cross-reference validation

15. **mcnp-geometry-checker** (Category C)
    - **Priority:** Medium
    - **Dependencies:** geometry-builder
    - **Current:** ~900 lines (estimate)
    - **Focus:** Geometry validation, overlaps, gaps

16. **mcnp-physics-validator** (Category C, bonus)
    - **Priority:** Low
    - **Dependencies:** physics-builder
    - **Current:** ~800 lines (estimate)
    - **Focus:** Physics settings validation

---

## 📋 PER-SKILL WORKFLOW (11 STEPS)

For EACH of the 16 skills above, follow this standardized workflow:

### Step 1: Read Current SKILL.md (2k tokens)
```bash
Read: .claude/skills/[skill-name]/SKILL.md
```
**Note in STATUS:**
- Current length (lines, estimated word count)
- Strengths to preserve (decision trees, examples, integration)
- Areas for improvement

### Step 2: Cross-Reference with Documentation (Already Read)
**⚠️ CRITICAL: Verify Documentation is in YOUR Context BEFORE Gap Analysis**

**MANDATORY VERIFICATION (See LESSONS-LEARNED.md Lesson #12):**
- [ ] Identify which Chapter 5/10 files are relevant for this skill
- [ ] Check: Do I have this documentation in MY current context?
  - ✅ Read it in this session? → HAVE IT, proceed
  - ✅ Comprehensive summary in autocompact (>1k words with specifications)? → HAVE IT, proceed
  - ❌ Just mentioned as "read in Sessions 3-5"? → DON'T HAVE IT
- [ ] If NOT in context:
  - **Option A:** Read the primary documentation NOW (costs tokens but ensures accuracy)
  - **Option B:** Work from comprehensive summaries if available
  - **Option C:** CANNOT proceed with accurate gap analysis
- [ ] After loading context: Can I explain 3-5 key concepts from the documentation?
- [ ] Only then: Proceed with cross-reference

**Use documentation read at phase start** (zero additional tokens if in context)
- Identify which Chapter 5 sections apply to this skill
- Note relevant Chapter 10 examples
- List key card specifications needed

**State explicitly to user:** "I have Chapter 5.0X in my context because [read 1,900 lines in this session / comprehensive summary available / etc.]"

### Step 3: Identify Discrepancies and Gaps (1k tokens)
**Document in active Phase 1 status document under "Currently Active Skill":**
- Missing coverage (e.g., "No mention of macrobody surfaces")
- Incorrect information (e.g., "Wrong ZAID format for MT card")
- Inconsistencies (e.g., "Contradicts 05_06 on density units")
- Need for examples (e.g., "Missing complex lattice examples")
- Improvement opportunities (e.g., "Decision tree could include validation step")

### Step 4: Create Skill Revamp Plan (1k tokens)
**Document detailed checklist in STATUS:**

**Content to extract to root-level .md files:**
- [ ] Card specifications (which cards, which sections from Ch 5)
- [ ] Theory/background (if applicable)
- [ ] Detailed examples (beyond 3-5 for SKILL.md)
- [ ] Error patterns (common mistakes)

**Examples to add to example_inputs/ (DIRECTLY at root):**
- [ ] From basic_examples/: [list specific files]
- [ ] From reactor-model_examples/: [list specific files]
- [ ] From [other category]/: [list specific files]
- [ ] Total: 5-10 examples covering basic → advanced

**Scripts to create in scripts/:**
- [ ] [script name].py - [purpose]
- [ ] [script name].sh - [purpose]
- [ ] README.md explaining usage

**Templates for templates/ (DIRECTLY at root):**
- [ ] basic_template.i
- [ ] intermediate_template.i (if applicable)

**SKILL.md streamlining:**
- Current word count: [X words]
- Target word count: <3k words (preferred) or <5k (max)
- Sections to condense: [list]
- Content to move to root-level .md files: [list]

### Step 5: Extract Content to Root Skill Directory (2k tokens)

**🚨 CRITICAL: Reference `.md` files go at ROOT skill directory level (same as SKILL.md) - NO assets/ subdirectory! 🚨**

**Correct structure:**
```bash
.claude/skills/[skill-name]/
├── SKILL.md                     ← Main skill file
├── card_specifications.md       ← Root level, NOT in subdirectory
├── theory_background.md         ← Root level
├── detailed_examples.md         ← Root level
├── error_catalog.md             ← Root level
├── scripts/                     ← Subdirectory for scripts
├── templates/                   ← DIRECTLY at root (NOT in assets/)
└── example_inputs/              ← DIRECTLY at root (NOT in assets/)
```

**Create reference files at root level:**
- **card_specifications.md** (for card-heavy skills)
  - Extract all detailed card syntax from Ch 5
  - Format specifications, parameter lists
  - Include grep patterns for large files

- **theory_background.md** (if applicable)
  - Mathematical derivations
  - Physics principles
  - Algorithms

- **detailed_examples.md**
  - Extended examples beyond SKILL.md's 3-5
  - Complex scenarios
  - Edge cases

- **error_catalog.md**
  - Common error messages
  - Causes and fixes
  - Troubleshooting guide

**Extraction principles:**
- Reference `.md` files at ROOT skill directory (NOT in `references/` subdirectory)
- Move content >500 words on single topic
- Keep SKILL.md as workflow guide
- Avoid duplication between SKILL.md and reference files
- Cross-reference from SKILL.md to specific sections

---

## 🚨 MCNP FORMAT VERIFICATION (MANDATORY BEFORE ALL FILE CREATION)

**Before creating ANY file with MCNP content (.i, .inp, .txt, .dat, .md snippets) in Steps 6, 7, or 8:**

### Universal Scope Requirement
- ✅ Complete input files (.i, .inp) - EXACTLY 2 blank lines
- ✅ Material library files (.txt, .dat) - ZERO blank lines within definitions
- ✅ Code snippets in markdown (.md) - ZERO blank lines within code blocks
- ✅ All templates in templates/ (at root level)
- ✅ All examples in example_inputs/ (at root level)
- ✅ Python-generated MCNP content

### Pre-Write Verification Checklist
**MANDATORY before EVERY Write tool use with MCNP content:**
1. [ ] Reference mcnp-input-builder and mcnp-geometry-builder documentation
2. [ ] Draft content mentally or in comments
3. [ ] Verify three-block structure (for complete files)
4. [ ] Count blank lines: 2 for complete files, 0 for snippets
5. [ ] Use `c ========` comment headers for readability, NEVER blank lines
6. [ ] Only after ALL checks pass: use Write tool

**Reference:** LESSONS-LEARNED.md Lesson #11 (MOST VIOLATED - 4 incidents)
**Consequence:** Files with incorrect format are INVALID and must be corrected immediately

---

### Step 6: Add Example Files to example_inputs/ at ROOT Level (1k tokens)

**🚨 CRITICAL: Create example_inputs/ DIRECTLY at root - NO assets/ parent! 🚨**
**Create directory structure:**
```bash
.claude/skills/[skill-name]/
├── SKILL.md
├── [reference].md files (at root)
├── scripts/
├── templates/                        ← DIRECTLY at root (NOT in assets/)
│   ├── basic_template.i
│   ├── intermediate_template.i (optional)
│   └── template_README.md
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    ├── example_01_[descriptive-name].i
    ├── example_01_description.txt
    ├── example_02_[descriptive-name].i
    ├── example_02_description.txt
    └── [5-10 total examples]
```

**Example selection criteria:**
1. Relevance to skill's core functionality
2. Range: basic (50-100 lines) → intermediate (200-300) → advanced (500+)
3. Validated (runs without fatal errors)
4. Demonstrates skill-specific techniques
5. From priority directories:
   - basic_examples/ for simple validation
   - reactor-model_examples/agr-1/mcnp/ for production quality
   - reactor-model_examples/repeated_structures/ for lattices
   - variance-reduction_examples/ for VR skills

**Description file format:**
```
EXAMPLE: [Descriptive Title]
SOURCE: [Which example_files/ directory and filename]
COMPLEXITY: [Basic / Intermediate / Advanced]

DEMONSTRATES:
- [Key feature 1]
- [Key feature 2]
- [Key feature 3]

KEY FEATURES:
- [Important aspect 1]
- [Important aspect 2]

RELATED SKILLS:
- [skill-name]: [Why related]

USAGE NOTES:
[Any special considerations]
```

### Step 7: Create/Bundle Scripts (1k tokens)
**Create directory:**
```bash
.claude/skills/[skill-name]/scripts/
```

**When to bundle scripts:**
- ✅ SKILL.md mentions Python automation
- ✅ Operation is repeatedly rewritten
- ✅ Complex algorithm better as executable
- ✅ Validation/checking is critical

**Script types:**
- **mcnp_[function].py** - Main automation tools
- **validate_[aspect].py** - Validation scripts
- **helper_[task].py** - Utility functions
- **README.md** - Usage documentation

**Script documentation requirements:**
```python
"""
[Script Name]

[Brief description of purpose]

Usage:
    python [script-name].py [arguments]

Arguments:
    [arg1]: [description]
    [arg2]: [description]

Returns:
    [return value description]

Example:
    python validate_input.py input.i
"""
```

**Create requirements.txt if needed:**
```
numpy>=1.20.0
pandas>=1.3.0
[other dependencies]
```

### Step 8: Streamline SKILL.md (3k tokens)
**Restructure to Anthropic standards:**

```markdown
---
name: [skill-name]
description: "Third-person, trigger-specific description. Be specific about when to use."
version: "2.0.0"
dependencies: "[python>=3.8, numpy>=1.20] # if applicable"
---

# [Skill Display Name]

## Overview

[Paragraph 1: What this skill does]
[Paragraph 2: Why/when users need this skill]
[Paragraph 3: High-level approach]

## When to Use This Skill

- [Specific trigger condition 1]
- [Specific trigger condition 2]
- [Specific trigger condition 3]
- [Specific trigger condition 4]
- [Specific trigger condition 5]
[5-10 total conditions]

## Decision Tree

```
[ASCII art workflow diagram]
Example:
User needs to [task]
  ↓
Has existing input?
  ├─→ Yes → Use input-editor skill
  └─→ No → Use this skill
       ↓
  What complexity?
       ├─→ Simple → Start with basic_template.i
       ├─→ Moderate → Use intermediate_template.i
       └─→ Complex → Review reactor-model examples
            ↓
       Build geometry?
            └─→ See geometry-builder skill
                 ↓
            Validate?
                 └─→ See input-validator skill
```

## Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| [Key concept 1] | [Brief explanation] | `[syntax]` |
| [Key concept 2] | [Brief explanation] | `[syntax]` |
| [Key concept 3] | [Brief explanation] | `[syntax]` |
[Create 1-page cheat sheet]

## Use Cases

### Use Case 1: [Basic Scenario Title]

**Scenario:** [What problem is the user facing?]

**Goal:** [What the user wants to achieve]

**Approach:** [Strategy to solve]

**Implementation:**
```
[MCNP code or procedure]
[Include inline comments]
```

**Key Points:**
- [Why this works]
- [Common pitfall to avoid]
- [When to use variation]

**Expected Results:** [What output should show]

### Use Case 2: [Intermediate Scenario]
[Repeat format]

### Use Case 3: [Advanced Scenario]
[Repeat format]

[3-5 total use cases, increasing complexity]

## Integration with Other Skills

**Typical Workflow:**
1. [prerequisite-skill] → [purpose]
2. **[THIS SKILL]** → [core task]
3. [followup-skill] → [purpose]

**Complementary Skills:**
- [related-skill-1]: Use when [condition]
- [related-skill-2]: Provides [complementary functionality]

**Example Complete Workflow:**
```
Project Goal: [Overall objective]

Step 1: [skill-a] - [purpose]
Step 2: [THIS SKILL] - [purpose]
Step 3: [skill-b] - [purpose]
Result: [Final output]
```

## References

**Detailed Information:**
- Card specifications: See `references/card_specifications.md`
- Theory and background: See `references/theory_background.md`
- Additional examples: See `references/detailed_examples.md`
- Error troubleshooting: See `references/error_catalog.md`

**Templates and Examples:**
- Input templates: See `templates/` (at root level)
- Validated examples: See `example_inputs/` (at root level)

**Automation Tools:**
- Python scripts: See `scripts/README.md`
- [Script name]: `scripts/[filename].py`

**External Documentation:**
- MCNP6 Manual Chapter [X]: [Topic]
- [Other references]

## Best Practices

1. [First best practice - most important]
2. [Second best practice]
3. [Third best practice]
4. [Fourth best practice]
5. [Fifth best practice]
6. [Sixth best practice]
7. [Seventh best practice]
8. [Eighth best practice]
9. [Ninth best practice]
10. [Tenth best practice]

[Each actionable, based on common issues/pitfalls]
```

**Target:** <3,000 words (preferred), <5,000 words (maximum)

**Writing standards:**
- ✅ Imperative/infinitive form: "To accomplish X, do Y"
- ❌ NO second person: Avoid "you should"
- ✅ Objective, instructional tone

### Step 9: Validate Quality - 25-Item Checklist (1k tokens)

Run through complete checklist from CLAUDE-SESSION-REQUIREMENTS.md:

**YAML Frontmatter (5 items):**
- [ ] 1. `name:` field matches directory name
- [ ] 2. `description:` is third-person and trigger-specific
- [ ] 3. No non-standard fields (removed `activation_keywords`, `category`)
- [ ] 4. `version: "2.0.0"` for revamped skills
- [ ] 5. `dependencies:` if skill uses external tools

**SKILL.md Structure (10 items):**
- [ ] 6. Overview section (2-3 paragraphs)
- [ ] 7. "When to Use This Skill" with bulleted conditions
- [ ] 8. Decision tree diagram (ASCII art)
- [ ] 9. Quick reference table
- [ ] 10. 3-5 use cases with standardized format
- [ ] 11. Integration section documents connections
- [ ] 12. References section points to bundled resources
- [ ] 13. Best practices section (10 numbered items)
- [ ] 14. Word count <3k (preferred) or <5k (max)
- [ ] 15. No duplication with references/ content

**Bundled Resources (7 items):**
- [ ] 16. references/ directory exists with relevant content
- [ ] 17. Large content (>500 words single topic) extracted
- [ ] 18. scripts/ directory exists if skill mentions automation
- [ ] 19. Python modules in scripts/ are functional
- [ ] 20. example_inputs/ directory at ROOT level has relevant examples from example_files/
- [ ] 21. templates/ directory at ROOT level has template files (if applicable)
- [ ] 22. Each example has description/explanation
- [ ] 23. **CRITICAL:** NO assets/ directory exists (ZERO TOLERANCE - auto-fail if present)

**Content Quality (3 items):**
- [ ] 24. All code examples are valid MCNP syntax
- [ ] 25. Cross-references to other skills are accurate
- [ ] 26. Documentation references are correct (paths, sections)

**If any item fails:** Document in STATUS, fix before marking skill complete

### Step 10: Test Skill (minimal tokens)
**Invoke skill with Claude Code:**
```
[Trigger phrase for skill]
```

**Verify:**
- Skill activates correctly
- Reference .md files (at root) load when referenced
- scripts/ execute without errors
- example_inputs/ examples are accessible (at root level)
- NO assets/ directory exists
- Integration links work

**If issues found:** Document and fix before proceeding

### Step 11: Update active Phase 1 status document (minimal tokens)
**Move skill from "Currently Active Skill" to "Completed Skills":**

**Completed entry format:**
```markdown
### [N]. [skill-name] ✅
- **Completed:** [Date/Session]
- **Changes:** [3-5 bullets summarizing key changes]
- **Structure:** [X reference .md files at root], scripts/[Y files], templates/[Z templates], example_inputs/[N examples]
- **Validation:** 25-item checklist passed
- **Word count:** [X words] (<3k ✅ or <5k ✅)
```

**Update progress counters:**
- Skills completed: X/16 Phase 1 (Y%)
- Overall progress: X/36 total (Y%)

**Mark next skill as active, begin Step 1**

---

## 📊 TOKEN BUDGET BREAKDOWN

### Phase-Level Allocation
- **Documentation reading:** 80k tokens (ONCE at phase start)
- **Skill processing:** 16 skills × 10k = 160k tokens
- **Total Phase 1:** ~240k tokens

### Per-Skill Token Breakdown (10k each)
- Step 1 (Read current SKILL.md): 2k
- Step 2 (Cross-reference): 0k (docs already read)
- Step 3 (Identify gaps): 1k
- Step 4 (Create plan): 1k
- Step 5 (Extract to references/): 2k
- Step 6 (Add examples): 1k
- Step 7 (Bundle scripts): 1k
- Step 8 (Streamline SKILL.md): 3k
- Step 9 (Validate): 1k
- Step 10 (Test): <1k
- Step 11 (Update STATUS): <1k
- **Total:** ~10k per skill

### Session Distribution
**Session 2 (This Session):**
- Create all 5 phase plans: ~40k tokens
- Backup original skills: minimal
- Begin Phase 1:
  - Read 20 documentation files: 80k tokens
  - Process skills 1-3: 30k tokens
- **Total Session 2:** ~150k tokens

**Session 3:**
- Continue Phase 1: Skills 4-10 (7 skills × 10k = 70k)
- **Total Session 3:** ~70k tokens

**Session 4:**
- Complete Phase 1: Skills 11-16 (6 skills × 10k = 60k)
- **Total Session 4:** ~60k tokens

**Phase 1 Total:** ~180k tokens actual (240k budgeted with buffer)

---

## 🎯 EXECUTION CHECKLIST

### Before Starting Phase 1
- [ ] All phase-specific master plans created (PHASE-1 through PHASE-5)
- [ ] Original skills backed up to .claude/skills_backup_original/
- [ ] active Phase 1 status document updated with Phase 1 start
- [ ] Token budget noted (~80k for docs, 160k for skills)

### Documentation Reading (Do ONCE)
- [ ] Chapter 3: Introduction to MCNP Usage
- [ ] Chapter 4: Description of MCNP6 Input
- [ ] Chapter 5: All 12 input card files
- [ ] Chapter 10: All 5 example files
- [ ] Take comprehensive notes for reference during skill processing
- [ ] Update STATUS with "Documentation Phase Complete"

### Skill Processing (16 iterations)
**For each skill:**
- [ ] Follow 11-step workflow
- [ ] Update STATUS continuously (not just at end)
- [ ] Complete 25-item quality checklist
- [ ] Test before marking complete
- [ ] Document completion in STATUS

**Skills (in order):**
1. [ ] mcnp-input-builder
2. [ ] mcnp-geometry-builder
3. [ ] mcnp-material-builder
4. [ ] mcnp-source-builder
5. [ ] mcnp-tally-builder
6. [ ] mcnp-physics-builder
7. [ ] mcnp-lattice-builder
8. [ ] mcnp-geometry-editor
9. [ ] mcnp-input-editor
10. [ ] mcnp-transform-editor
11. [ ] mcnp-variance-reducer
12. [ ] mcnp-input-validator
13. [ ] mcnp-cell-checker
14. [ ] mcnp-cross-reference-checker
15. [ ] mcnp-geometry-checker
16. [ ] mcnp-physics-validator

### Phase Completion
- [ ] All 16 skills completed and validated
- [ ] Integration map updated (skill connections documented)
- [ ] active Phase 1 status document reflects Phase 1 complete
- [ ] Prepare for Phase 2

---

## 🔍 SKILL-SPECIFIC NOTES

### mcnp-input-builder (Skill #1 - CRITICAL)
**Why first:** Most foundational, referenced by all others
**Key focus areas:**
- Three-block structure (cells, surfaces, data)
- Basic formatting rules
- Overall file organization
**References to create:**
- card_specifications.md (all card types overview)
- input_structure.md (detailed format specs)
**Examples priority:**
- basic_examples/simple*.txt (5 files)
- reactor-model_examples/agr-1/bench_*.i (2-3 simple ones)

### mcnp-geometry-builder (Skill #2 - HIGH PRIORITY)
**Why second:** Core functionality, many dependencies
**Key focus areas:**
- Cell cards (Boolean logic, complement operator)
- Surface cards (all types, especially macrobodies)
- Coordinate systems
**References to create:**
- surface_types.md (comprehensive surface catalog from 05_03)
- boolean_logic.md (intersection, union, complement)
- macrobodies.md (BOX, RPP, SPH, RCC, etc.)
**Examples priority:**
- basic_examples/shield*.txt
- reactor-model_examples with complex geometry

### mcnp-lattice-builder (Skill #7 - SPECIAL)
**Why special:** Complex topic, needs detailed examples
**Key focus areas:**
- U/LAT/FILL card interactions
- Hexagonal vs rectangular lattices
- Nested universes
**References to create:**
- lattice_theory.md (universe concept, filling)
- lattice_examples.md (extensive examples from Ch 10)
**Examples priority:**
- reactor-model_examples/repeated_structures/ (ALL files)
- Any fuel assembly examples

### mcnp-variance-reducer (Skill #11 - PARTIAL)
**Why partial:** Will be completed more in Phase 3
**Phase 1 focus:**
- Basic importance (IMP card)
- Simple weight windows (WWN/WWE cards)
- DXTRAN spheres
**Phase 3 completion:**
- Advanced WWG (WWGE, mesh-based generation)
- Coupling with tally-analyzer
- Optimization strategies
**References to create in Phase 1:**
- basic_vr_techniques.md (IMP, WWN, DXTRAN)
**References to add in Phase 3:**
- advanced_ww_optimization.md
- wwg_generation.md

---

## 🚨 PHASE 1 CONTINGENCIES

### If Running Low on Tokens
**Trigger:** < 30k tokens remaining in session

**Actions:**
1. **STOP** current skill processing
2. Update active Phase 1 status document with maximum detail:
   - Current skill, current step (1-11)
   - Exactly what was completed
   - Exactly what's pending
   - Critical context for continuation
3. Mark skill as "in_progress" in STATUS
4. Create session handoff note
5. Exit gracefully

**Resume in next session:**
- Read STATUS carefully
- Continue from exact step noted
- Complete current skill before moving to next

### If Discovering Major Issues
**Examples:** Documentation contradicts skill, examples don't work, missing critical info

**Actions:**
1. Document issue in active Phase 1 status document under "Issues Found"
2. Include:
   - Skill affected
   - Specific problem
   - Evidence (quotes, references)
   - Impact on revamp plan
3. Create proposed solution
4. Ask user for guidance if uncertain
5. Do NOT skip or work around - fix properly

### If Skills Need Reorganization
**Example:** Realize skill categories don't match documentation perfectly

**Actions:**
1. Document observation in STATUS
2. Continue with current phase plan (don't reorganize mid-phase)
3. Note for end-of-project review
4. Ensure integration sections properly link skills
5. User can decide on reorganization after all revamps complete

---

## ✅ PHASE 1 SUCCESS CRITERIA

### Phase Complete When:
- ✅ All 20 documentation files read and comprehended
- ✅ All 16 skills processed through 11-step workflow
- ✅ Every skill passes 25-item quality checklist
- ✅ All skills tested and validated
- ✅ Integration map created for Phase 1 skills
- ✅ active Phase 1 status document reflects accurate completion
- ✅ Token budget within estimates (~240k)
- ✅ Ready to proceed to Phase 2

### Per-Skill Success:
- ✅ SKILL.md streamlined to <5k words (ideally <3k)
- ✅ references/ created with extracted content
- ✅ example_inputs/ (at root level) populated with 5-10 relevant examples
- ✅ NO assets/ directory exists
- ✅ scripts/ created if applicable
- ✅ 25-item checklist passed
- ✅ Tested with Claude Code
- ✅ STATUS updated with completion entry

---

## 📈 PROGRESS TRACKING

**Monitor in active Phase 1 status document:**

```markdown
## PHASE 1 PROGRESS

**Status:** [In Progress / Complete]
**Session:** [Current session number]
**Tokens used:** [X]k / 240k budgeted

### Documentation Reading
- [ ] Core usage chapters (2 files) - [Status]
- [ ] Chapter 5: Input cards (12 files) - [Status]
- [ ] Chapter 10: Examples (5 files) - [Status]
- [ ] Documentation phase complete: [✅/⏸️]

### Skills Completed: X/16 (Y%)

**Tier 1: Core Input Building**
1. [ ] mcnp-input-builder
2. [ ] mcnp-geometry-builder
3. [ ] mcnp-material-builder
4. [ ] mcnp-source-builder
5. [ ] mcnp-tally-builder
6. [ ] mcnp-physics-builder
7. [ ] mcnp-lattice-builder

**Tier 2: Input Editing**
8. [ ] mcnp-geometry-editor
9. [ ] mcnp-input-editor
10. [ ] mcnp-transform-editor
11. [ ] mcnp-variance-reducer (partial)

**Tier 3: Validation**
12. [ ] mcnp-input-validator
13. [ ] mcnp-cell-checker
14. [ ] mcnp-cross-reference-checker
15. [ ] mcnp-geometry-checker
16. [ ] mcnp-physics-validator

**Phase 1 Complete:** [Date/Session]
```

---

## 🔗 INTEGRATION WITH OTHER PHASES

### Phase 1 → Phase 2 Handoff
**Skills that continue in Phase 2:**
- None directly, but Phase 2 skills will reference Phase 1 skills heavily

**Documentation overlap:**
- Phase 2 reads different docs (Chapter 8, Appendix D)
- No token waste from documentation reuse

### Phase 1 → Phase 3 Handoff
**Skills that continue in Phase 3:**
- **mcnp-variance-reducer:** Basic VR in Phase 1, advanced in Phase 3
- **mcnp-tally-analyzer:** May need Phase 1 + Phase 3 docs

**Plan:**
- Complete basic functionality in Phase 1
- Add advanced features in Phase 3
- Mark clearly in SKILL.md what's basic vs advanced

---

**END OF PHASE 1 MASTER PLAN**

**Next Step:** Create PHASE-2-MASTER-PLAN.md, then backup skills, then begin Phase 1 execution.

**Remember:** Read documentation ONCE at phase start, process all 16 skills in batch, update STATUS continuously, use 25-item checklist for every skill.
