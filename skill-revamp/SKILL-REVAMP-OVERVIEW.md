# MCNP SKILLS REVAMP PROJECT - OVERVIEW & MASTER GUIDE

**Version:** 1.2
**Created:** 2025-11-02 (Session 1)
**Updated:** 2025-11-05 (Session 18 - Phase 1: 81.25% complete, Tiers 1 & 2 done)
**Purpose:** High-level project overview and execution roadmap

---

## 📚 DOCUMENT STRUCTURE

This project uses a **modular documentation approach** to prevent context overload:

### Core Documents (Read Every Session)
1. **CLAUDE-SESSION-REQUIREMENTS.md** (2,500 lines) - MANDATORY FIRST READ
   - Session startup procedure
   - Workflow requirements
   - Quality standards
   - Emergency procedures

2. **Project Status Documents** (phase-specific, continuously updated)
   - **archive/REVAMP-PROJECT-STATUS.md** (ARCHIVED) - Phase 0 infrastructure (historical reference only)
   - **PHASE-1-PROJECT-STATUS-PART-6.md** - Phase 1 execution tracking (16 skills, CURRENTLY ACTIVE)
     - Parts 1-5 archived (exceeded 900-line threshold)
     - Part 6: Sessions 17-18, Tier 2 & Tier 3 skills
   - **PHASE-2-PROJECT-STATUS.md** - Phase 2 execution tracking (6 skills, not started)
   - **PHASE-3-PROJECT-STATUS.md** - Phase 3 execution tracking (4 skills, not started)
   - **PHASE-4-PROJECT-STATUS.md** - Phase 4 execution tracking (6 skills, not started)
   - **PHASE-5-PROJECT-STATUS.md** - Phase 5 execution tracking (8 skills, not started)
   - **Structure:** Each phase status begins with previous phase summary
   - **Purpose:** Focused tracking per phase, prevents document bloat
   - **🚨 SPLITTING RULE:** When ANY status document exceeds 900 lines, create PART N
     - Example: PHASE-1-PROJECT-STATUS.md → PHASE-1-PROJECT-STATUS-PART-2.md
     - Part N-1 retains session summaries and completed skills
     - Part N contains currently active skill and remaining skills
     - Update CLAUDE-SESSION-REQUIREMENTS.md CURRENT PROJECT STATE to reference latest part

3. **SKILL-REVAMP-OVERVIEW.md** (THIS FILE - 1,500 lines)
   - Project goals and scope
   - High-level strategy
   - Quick reference guide

### Detailed Research Documents (Reference As Needed)
Located in `planning-research/`:
- **anthropic-standards-analysis.md** - Skill-creator standards breakdown
- **current-skills-assessment.md** - All 36 MCNP skills reviewed
- **example-files-inventory.md** - 1,107 example files catalogued
- **knowledge-base-map.md** - 72 documentation files mapped
- **optimization-strategy.md** - Token savings calculations and batching approach

### Phase-Specific Master Plans (Create When Needed)
- **PHASE-1-MASTER-PLAN.md** - Category A&B (16 skills) detailed execution plan
- **PHASE-2-MASTER-PLAN.md** - Category D (6 skills)
- **PHASE-3-MASTER-PLAN.md** - Category E (4 skills)
- **PHASE-4-MASTER-PLAN.md** - Category F (6 skills)
- **PHASE-5-MASTER-PLAN.md** - Category C & Specialized (4 skills)

**Note:** Phase-specific plans will be created at the START of each phase to avoid loading unnecessary context.

---

## 🎯 PROJECT GOALS

### Primary Objective
Revamp all 36 MCNP Claude skills to meet Anthropic's official skill-creator standards by incorporating:

1. **Progressive Disclosure Structure**
   - Lean SKILL.md files (<3k words preferred, <5k max)
   - references/ subdirectories for detailed specifications
   - scripts/ subdirectories for Python automation tools
   - assets/ subdirectories for templates and example inputs

2. **Comprehensive Knowledge Base Integration**
   - Full utilization of 72 markdown documentation files (4.2 MB)
   - Proper coverage from markdown_docs/ per must-read-docs.md

3. **Example Files Integration** (CRITICAL - NOT DONE ORIGINALLY)
   - Incorporation of 1,107 example MCNP files from example_files/
   - 5-10 relevant examples per skill in assets/example_inputs/
   - Emphasis on reactor-model_examples/ (most comprehensive)

4. **Zero Context Loss Between Sessions**
   - Comprehensive session documentation
   - Clear handoff procedures
   - Detailed progress tracking

### Success Criteria
- ✅ All 36 skills comply with Anthropic standards
- ✅ Every skill has proper references/, scripts/, assets/ structure
- ✅ SKILL.md files streamlined to <5k words
- ✅ All skills include relevant examples from example_files/
- ✅ 25-item quality checklist passed for each skill
- ✅ Zero context loss between sessions
- ✅ 85% token savings achieved via batched processing

---

## 📊 PROJECT SCOPE

### Skills Inventory (36 Total)

**Category A: Input Creation (7 skills)**
- mcnp-input-builder
- mcnp-geometry-builder
- mcnp-material-builder
- mcnp-source-builder
- mcnp-tally-builder
- mcnp-physics-builder
- mcnp-template-generator

**Category B: Input Editing (5 skills)**
- mcnp-input-editor
- mcnp-geometry-editor
- mcnp-transform-editor
- mcnp-variance-reducer
- mcnp-input-updater

**Category C: Validation (5 skills)**
- mcnp-input-validator
- mcnp-geometry-checker
- mcnp-cross-reference-checker
- mcnp-fatal-error-debugger
- mcnp-warning-analyzer

**Category D: Output Analysis (5 skills)**
- mcnp-output-parser
- mcnp-mctal-processor
- mcnp-tally-analyzer
- mcnp-statistics-checker
- mcnp-plotter

**Category E: Advanced Operations (5 skills)**
- mcnp-burnup-builder
- mcnp-mesh-builder
- mcnp-lattice-builder
- mcnp-ww-optimizer
- mcnp-parallel-configurator

**Category F: Utilities (6 skills)**
- mcnp-unit-converter
- mcnp-isotope-lookup
- mcnp-cross-section-manager
- mcnp-physical-constants
- mcnp-example-finder
- mcnp-knowledge-docs-finder

**Bonus Skills (3 skills)**
- mcnp-best-practices-checker
- mcnp-physics-validator
- mcnp-criticality-analyzer
- mcnp-cell-checker

---

## ⚡ OPTIMIZATION STRATEGY (KEY INSIGHT)

### The Problem
Original skill creation wasted tokens by re-reading the same documentation repeatedly:
- 16 Category A/B skills × 80k tokens per skill = 1,280k tokens wasted
- **Total waste across all 36 skills: ~2,000k tokens**

### The Solution: Batched Processing
Read shared documentation **ONCE per category**, then process all skills in that category:
- Category A/B: Read docs once (80k) → Process 16 skills (160k) = 240k total
- **Total for all 36 skills: ~430k tokens**
- **Savings: 85% (2,000k → 430k tokens)**

### Implementation
Group skills by shared documentation requirements (per must-read-docs.md):

**Phase 1: Category A & B (16 skills)**
- Read: Chapters 3, 4, all Chapter 5 (12 files), all Chapter 10 (5 files)
- Token cost: 80k (docs once) + 160k (16 skills × 10k each) = 240k
- Sessions: 2-3

**Phase 2: Category D (6 skills)**
- Read: Chapter 8, Appendix D (7 files), Appendix E.11
- Token cost: 40k + 60k = 100k
- Sessions: 1

**Phase 3: Category E (4 skills)**
- Read: All D docs + variance reduction docs
- Token cost: 50k + 40k = 90k
- Sessions: 1

**Phase 4: Category F (6 skills)**
- Read: Appendix E (12 utility tool files)
- Token cost: 30k + 60k = 90k
- Sessions: 1

**Phase 5: Category C & Specialized (4 skills)**
- Read: Minimal, skill-specific
- Token cost: 20k + 40k = 60k
- Sessions: 1

**Total: 5-7 sessions, ~430k tokens (vs ~2,400k sequential)**

---

## 🏗️ SKILL REVAMP WORKFLOW

### Standard 11-Step Process (Per Skill)

**1. Review Current SKILL.md**
- Read existing .claude/skills/[skill-name]/SKILL.md
- Note structure, length, strengths to preserve
- Identify areas for improvement

**2. Review Knowledge Base Documentation**
- Read required docs per must-read-docs.md (already done for category batch)
- Take notes on key concepts, specifications, examples
- Cross-reference with current SKILL.md

**3. Identify Discrepancies and Gaps**
Document in active PHASE-N-PROJECT-STATUS-PART-N.md:
- Missing topic coverage
- Incorrect/outdated information
- Inconsistencies with documentation
- Need for more examples
- Improvement opportunities

**4. Create Skill Revamp Plan**
Detailed checklist of changes:
- What to extract to references/
- Which examples to add from example_files/
- What scripts to create/bundle
- Templates for assets/
- Target word count for streamlined SKILL.md

**5. Extract Content to references/**
Create: `.claude/skills/[skill-name]/references/`
- card_specifications.md (if applicable)
- theory_background.md
- detailed_examples.md
- error_catalog.md
- [topic-specific files as needed]

**Extraction guidelines:**
- Content >500 words on single topic → references/
- All card format specifications → references/
- Theory/mathematical derivations → references/
- Comprehensive examples (keep 3-5 in SKILL.md, rest in references/)

**6. Add Example Files to assets/**
Create: `.claude/skills/[skill-name]/assets/`
```
assets/
├── templates/
│   ├── basic_template.i
│   ├── intermediate_template.i
│   └── advanced_template.i
└── example_inputs/
    ├── example_01.i
    ├── example_01_description.txt
    ├── example_02.i
    ├── example_02_description.txt
    └── [5-10 total examples]
```

**Selection from example_files/:**
- Relevant to skill's purpose
- Range of complexity (basic → advanced)
- Properly formatted and validated
- Include description/context file for each

**Key directories:**
- basic_examples/ - Simple validation examples
- reactor-model_examples/ - Complex, production-quality
- variance-reduction_examples/ - VR techniques
- unstructured-mesh_examples/ - Mesh tallies

**7. Create/Bundle Scripts in scripts/**
Create: `.claude/skills/[skill-name]/scripts/`
- Python automation modules (currently only mentioned, not bundled)
- Validation scripts
- Helper utilities
- README.md explaining usage

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
[2-3 paragraphs]

## When to Use This Skill
[Bulleted trigger conditions]

## Decision Tree
[ASCII workflow diagram]

## Quick Reference
[Summary table]

## Use Cases (3-5 examples)
### Use Case 1: [Title]
**Scenario:** ...
**Implementation:** ...
**Key Points:** ...

## Integration with Other Skills
[Workflow connections]

## References
- See references/[file].md for details
- See assets/templates/ for templates
- See assets/example_inputs/ for examples
- See scripts/README.md for automation

## Best Practices
[10 numbered items]
```

**Target: <3k words (preferred), <5k words (maximum)**

**9. Standardize YAML Frontmatter**
- Remove non-standard fields: `activation_keywords`, `category`
- Ensure `description` is third-person and trigger-specific
- Add `version: "2.0.0"` for revamped skills
- Add `dependencies` if applicable

**10. Validate Quality (25-Item Checklist)**
See CLAUDE-SESSION-REQUIREMENTS.md Section "QUALITY ASSURANCE CHECKLIST"
- YAML frontmatter (5 items)
- SKILL.md structure (10 items)
- Bundled resources (7 items)
- Content quality (3 items)

**11. Test and Update Status**
- Invoke skill with Claude Code to verify
- Test that references/ load correctly
- Validate scripts/ execute properly
- Check examples in assets/
- Update active PHASE-N-PROJECT-STATUS-PART-N.md with completion

---

## 📋 QUALITY STANDARDS & REQUIREMENTS

**See CLAUDE-SESSION-REQUIREMENTS.md for complete quality standards:**
- Anthropic Skill-Creator Standards (progressive disclosure, directory structure, writing standards)
- 25-Item Quality Checklist (YAML, SKILL.md structure, bundled resources, content quality)
- MCNP format requirements (applies to ALL content types)
- Emergency procedures and token management

**All skills must pass the 25-item quality checklist before marking complete.**

---

## 🚀 EXECUTION PHASES

### Phase 0: Infrastructure Setup
**Status:** In progress (Session 1, interrupted by API error)
**Tasks:**
- ✅ Create directory structure
- ✅ Create CLAUDE-SESSION-REQUIREMENTS.md
- ✅ Create SKILL-REVAMP-OVERVIEW.md (this file)
- ✅ Create REVAMP-PROJECT-STATUS.md
- 🚧 Create planning-research/ files (5 documents)
- ⏸️ Create templates/
- ⏸️ Backup original skills

**When complete:** Proceed to Phase 1

### Phase 1: Category A & B (16 Skills)
**Sessions:** 2-3
**Documentation:** Read ONCE at phase start
- Chapters 3, 4
- All Chapter 5 (12 files)
- All Chapter 10 (5 files)

**Skills (in dependency order):**
1. mcnp-input-builder (foundational)
2. mcnp-geometry-builder
3. mcnp-material-builder
4. mcnp-source-builder
5. mcnp-tally-builder
6. mcnp-physics-builder
7. mcnp-lattice-builder
8. mcnp-geometry-editor
9. mcnp-input-editor
10. mcnp-input-validator
11. mcnp-cell-checker
12. mcnp-cross-reference-checker
13. mcnp-geometry-checker
14. mcnp-physics-validator
15. mcnp-transform-editor
16. mcnp-variance-reducer

**Expected:** 240k tokens, 2-3 sessions

**At phase start:** Create PHASE-1-MASTER-PLAN.md with detailed execution plan

### Phase 2: Category D (6 Skills)
**Sessions:** 1
**Documentation:** Chapter 8, Appendix D (7 files), Appendix E.11
**Skills:** output-parser, mctal-processor, mesh-builder, plotter, tally-analyzer (partial), statistics-checker (partial)
**Expected:** 100k tokens, 1 session

### Phase 3: Category E (4 Skills)
**Sessions:** 1
**Documentation:** All D docs + variance reduction theory
**Skills:** variance-reducer (complete), ww-optimizer, tally-analyzer (complete), statistics-checker (complete)
**Expected:** 90k tokens, 1 session

### Phase 4: Category F (6 Skills)
**Sessions:** 1
**Documentation:** Appendix E (12 utility files)
**Skills:** unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator
**Expected:** 90k tokens, 1 session

### Phase 5: Category C & Specialized (4 Skills)
**Sessions:** 1
**Documentation:** Minimal, skill-specific
**Skills:** fatal-error-debugger, warning-analyzer, criticality-analyzer, best-practices-checker, example-finder, knowledge-docs-finder, burnup-builder, input-updater
**Expected:** 60k tokens, 1 session

**Total Project:** 5-7 sessions, ~430k tokens

---

## 📁 FILE STRUCTURE

**See CLAUDE-SESSION-REQUIREMENTS.md Section 'FILE STRUCTURE REFERENCE' for complete project directory tree.**

---

## 🎓 BEST PRACTICES

### For Every Session:
1. ✅ Follow the 5-step mandatory startup procedure (see CLAUDE-SESSION-REQUIREMENTS.md)
2. ✅ Check CURRENT PROJECT STATE section for active phase and documents
3. ✅ Update active PHASE-N-PROJECT-STATUS-PART-N.md after major milestones and at session end
4. ✅ Reserve 15-20k tokens for session handoff documentation
5. ✅ Use 25-item quality checklist for every skill (see CLAUDE-SESSION-REQUIREMENTS.md)
6. ✅ Batch documentation reading by category
7. ✅ Test skills after revamp
8. ✅ Preserve context for next session

### Documentation Practices:
- **Read primary sources** - Don't rely only on summaries
- **Document as you go** - Update active PHASE-N-PROJECT-STATUS.md continuously
- **Be specific** - "Extracted card specs to references/card_specs.md, lines 1-250" not "made progress"
- **Track tokens** - Monitor usage, note when reading large docs
- **Create handoff** - If tokens < 30k, begin handoff procedure
- **Phase transitions** - Summarize completed phase in new phase status doc

### Content Practices:
- **Extract aggressively** - When in doubt, move to references/
- **Use examples liberally** - 5-10 per skill from example_files/
- **Bundle scripts** - Don't just mention Python modules, include them
- **Preserve quality** - Keep good decision trees, integration sections
- **Test incrementally** - Don't wait until all 36 done

---

## 🚨 EMERGENCY PROCEDURES

### If Running Out of Tokens (< 30k Remaining)

**STOP ALL WORK IMMEDIATELY**

**Priority 1:** Update active PHASE-N-PROJECT-STATUS.md with maximum detail
- Current skill's "Currently Active Skill" section
- Exactly where reading stopped (file, line number, section)
- Key findings from completed portions
- Next steps explicitly stated
- Critical context paragraph
- Update active PHASE-N-PROJECT-STATUS-PART-N.md after major milestones

**Priority 2:** Verify STATUS accuracy
- Completed skills list correct
- Next skill in queue identified
- Progress percentages updated

**Priority 3:** Save partial work
- Mark in-progress files clearly
- Document what's complete vs pending
- Don't leave broken states

**Priority 4:** Create handoff note at top of STATUS

**Priority 5:** Inform user, exit gracefully

### If Discovering Errors in Revamped Skills

**DON'T:**
- Delete/overwrite without documenting
- Make changes without understanding original intent
- Assume previous Claude made mistakes

**DO:**
1. Document issue in active PHASE-N-PROJECT-STATUS.md
2. Create "Issues Found" section with details
3. Ask user for guidance if uncertain
4. Create fix plan for current/next session

### If Confused About Requirements

**Escalation path:**
1. Read SKILL-REVAMP-OVERVIEW.md (this file)
2. Read CLAUDE-SESSION-REQUIREMENTS.md
3. Check planning-research/ files
4. Read mcnp-skills-requirements.md
5. Read must-read-docs.md
6. Use skill-creator skill (globally installed)
7. Ask user for clarification

---

## 📊 SUCCESS METRICS

### Project Level
- ✅ All 36 skills revamped to Anthropic standards
- ✅ Every skill has proper structure (references/, scripts/, assets/)
- ✅ All SKILL.md files <5k words
- ✅ Example files from example_files/ incorporated
- ✅ Token savings achieved (430k vs 2,400k)
- ✅ Zero context loss between sessions
- ✅ All testing complete

### Skill Level
- ✅ 25-item quality checklist passed
- ✅ YAML frontmatter standardized
- ✅ SKILL.md streamlined and structured
- ✅ references/ created with extracted content
- ✅ assets/ populated with relevant examples
- ✅ scripts/ created if applicable
- ✅ No duplication between components
- ✅ Integration documented
- ✅ Tested and validated

---

## 🔍 QUICK REFERENCE

### Essential Commands
- **Invoke skill-creator:** "I need guidance on skill structure per Anthropic standards"
- **Check tokens:** Monitor system messages throughout session
- **Test skill:** Invoke with Claude Code after revamp

### Key Files to Reference
- **Standards:** planning-research/anthropic-standards-analysis.md
- **Skills:** planning-research/current-skills-assessment.md
- **Examples:** planning-research/example-files-inventory.md
- **Docs:** planning-research/knowledge-base-map.md
- **Strategy:** planning-research/optimization-strategy.md
- **Original requirements:** mcnp-skills-requirements.md
- **Doc mapping:** must-read-docs.md

### Global Skills Available
- **skill-creator** - Anthropic's official skill creation guide
- **docx/pptx/xlsx/pdf** - Document processing
- **canvas-design** - Visual diagrams
- **theme-factory** - Styled documentation

---

## 📈 PROGRESS TRACKING

### High-Level Status
See **CURRENT PROJECT STATE** section in CLAUDE-SESSION-REQUIREMENTS.md for active phase and status documents:
```
Phase 0 (Infrastructure): ✅ COMPLETE (Sessions 1-2)
Phase 1 (A&B - 16 skills): 🚧 IN PROGRESS - 13/16 complete (81.25%)
  - Tier 1 (Core Building): ✅ 7/7 complete (100%)
  - Tier 2 (Input Editing): ✅ 5/5 complete (100%)
  - Tier 3 (Validation): 🚧 1/4 complete (25%) - 3 skills remaining
Phase 2 (D - 6 skills): ⏸️ NOT STARTED
Phase 3 (E - 4 skills): ⏸️ NOT STARTED
Phase 4 (F - 6 skills): ⏸️ NOT STARTED
Phase 5 (C+ - 8 skills): ⏸️ NOT STARTED

Total: 13/36 skills complete (36.11%)
Current Phase: Phase 1 (Category A&B)
Active Status Doc: PHASE-1-PROJECT-STATUS-PART-6.md
Current Session: 19 (next)
```

### Detailed Phase Tracking
Each phase has dedicated status document:
- **PHASE-1-PROJECT-STATUS.md** - Tracks 16 skills in detail
- **PHASE-2-PROJECT-STATUS.md** - Tracks 6 skills in detail
- **PHASE-3-PROJECT-STATUS.md** - Tracks 4 skills in detail
- **PHASE-4-PROJECT-STATUS.md** - Tracks 6 skills in detail
- **PHASE-5-PROJECT-STATUS.md** - Tracks 8 skills in detail

**Why separate?** Prevents any single document from exceeding 5,000 lines

---

## 🎯 NEXT STEPS

### Session 2 (Next Session):
1. Complete infrastructure setup:
   - Create planning-research/ files (5 docs)
   - Create templates/
   - Backup original skills
2. Create PHASE-1-MASTER-PLAN.md
3. Begin Phase 1 execution (if tokens allow)

### Sessions 3-7:
- Execute phases 1-5 sequentially
- Follow batched processing strategy
- Maintain continuous documentation

---

**END OF SKILL-REVAMP-OVERVIEW.MD**

**Remember:** This is a high-level guide. For detailed procedures, always refer to CLAUDE-SESSION-REQUIREMENTS.md first, then phase-specific master plans as they're created.

**Philosophy:** "Zero Context Loss Through Comprehensive Documentation"
