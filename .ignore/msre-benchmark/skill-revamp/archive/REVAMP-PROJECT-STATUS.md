# MCNP SKILLS REVAMP - MASTER PROJECT STATUS

**Document Purpose:** High-level project overview + Phase 0 (infrastructure) detailed status
**Active Phase Status:** See PHASE-[N]-PROJECT-STATUS.md for detailed tracking of current phase

---

## ⚠️⚠️⚠️ MANDATORY READING BEFORE THIS DOCUMENT ⚠️⚠️⚠️

**IF YOU HAVE NOT ALREADY READ THESE FILES, STOP AND READ THEM NOW IN THIS ORDER:**

### 1. CLAUDE.md (ABSOLUTE FIRST PRIORITY)
**File:** `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\skill-revamp\CLAUDE.md`
**Version:** 3.1 (updated Session 10)
**Contains:** 11 lessons learned, MCNP format requirements, verification checklists, mandatory disclaimers
**DO NOT SKIP THIS FILE**

### 2. CLAUDE-SESSION-REQUIREMENTS.md
**File:** `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\skill-revamp\CLAUDE-SESSION-REQUIREMENTS.md`
**Version:** 1.4 (updated Session 10)
**Contains:** Mandatory 7-step startup procedure, session protocol
**DO NOT SKIP THIS FILE**

### 3. THIS DOCUMENT (REVAMP-PROJECT-STATUS.md)
You are reading it now. Continue below to determine which phase is active.

**CRITICAL:** All documents must reference each other. NO document should ever be skipped.

---

**Last Updated:** Session 10 - 2025-11-03 (Phase 1 Active - 3 skills complete)
**Current Phase:** Phase 1 - Category A&B Skills (EXECUTION 🚧)
**Active Status Document:** PHASE-1-PROJECT-STATUS-PART-2.md (use for Session 11+)
**Skills Completed:** 3/16 Phase 1 skills (mcnp-input-builder, mcnp-geometry-builder, mcnp-material-builder)
**Next Skill:** mcnp-source-builder (Priority 4)

---

## 🚀 FOR NEW SESSIONS: START HERE

**Complete 7-step startup procedure from CLAUDE-SESSION-REQUIREMENTS.md:**

1. **Read CLAUDE.md** (MANDATORY FIRST)
2. **Read CLAUDE-SESSION-REQUIREMENTS.md**
3. **Read this file (REVAMP-PROJECT-STATUS.md)** to determine active phase
4. **Read active phase status document:** PHASE-1-PROJECT-STATUS-PART-2.md
5. **Read PHASE-1-MASTER-PLAN.md** (phase-specific requirements)
6. **Read SKILL-REVAMP-OVERVIEW.md** (high-level strategy)
7. **Output verification checklist to user** (from CLAUDE.md)

2. **Create PHASE-1-PROJECT-STATUS.md** (~5k tokens):
   - Copy structure from this document
   - Begin with Phase 0 summary (infrastructure complete)
   - Set up blank "Currently Active Skill" section

3. **Read PHASE-1-MASTER-PLAN.md** (~8k tokens)

4. **Read Phase 1 docs ONCE** (~80k tokens):
   - Chapters 3, 4, all Chapter 5 (12 files), all Chapter 10 (5 files)

5. **Process 2-3 skills** (~30k tokens):
   - Start with mcnp-input-builder (priority 1)
   - Follow 11-step workflow
   - Update PHASE-1-PROJECT-STATUS.md continuously

**Token Budget:** ~148k total (fits in one session)

### Session 2 Key Deliverables:
- ✅ 5 phase-specific master plans (~9,000 lines)
- ✅ Original skills backed up
- ✅ Phase-specific status tracking approach implemented
- ✅ All planning documents updated

**Critical Decision:** Phase-specific status documents prevent bloat (each phase = separate status doc, 2-4k lines each vs single 15k+ line doc)

---

## 📋 MODULAR STATUS TRACKING APPROACH

**Why Phase-Specific Status Documents?**
- Each phase tracks 4-16 skills with detailed progress
- Single document would exceed 15,000+ lines by project end
- Phase-specific docs keep context focused and manageable

**Document Structure:**
- **THIS DOCUMENT (REVAMP-PROJECT-STATUS.md):**
  - High-level overview of all 5 phases
  - Detailed tracking for Phase 0 (infrastructure)
  - Points to active phase status document

- **PHASE-N-PROJECT-STATUS.md (Created when phase starts):**
  - Detailed tracking for that phase's skills
  - Begins with summary of previous phase
  - Continuously updated during phase execution
  - ~2,000-4,000 lines per phase

**For Future Claudes:**
1. Read this document FIRST to determine current phase
2. Then read active PHASE-N-PROJECT-STATUS.md for detailed status
3. Update active phase status continuously during work
4. Update THIS document when starting/completing phases

---

## ✅ INFRASTRUCTURE SETUP COMPLETE - READY FOR PHASE 1

**Session:** 2 (Infrastructure Completion)
**Status:** Infrastructure 100% COMPLETE ✅
**Outcome:** All planning documents created, original skills backed up, ready to begin Phase 1 execution

### What Was Completed This Session ✅

1. **✅ skill-revamp/ directory structure COMPLETE**
   - Created all subdirectories:
     - skill-revamp/planning-research/
     - skill-revamp/templates/skill-template-structure/ (with references/, scripts/, assets/ subdirs)
     - skill-revamp/shared-resources/common-references/
     - skill-revamp/shared-resources/common-examples/

2. **✅ CLAUDE-SESSION-REQUIREMENTS.md COMPLETE** (2,500+ lines)
   - Location: skill-revamp/CLAUDE-SESSION-REQUIREMENTS.md
   - Status: Fully written and saved
   - Contents:
     - Mandatory session startup procedure (6 steps)
     - Project overview and scope
     - Documentation requirements
     - Batched processing strategy (5 phases)
     - Skill revamp workflow (11 steps per skill)
     - 25-item quality assurance checklist
     - Token management guidelines
     - Emergency procedures (token limits, errors, confusion)
     - Integration with global skills
     - 10 best practices
     - File structure reference
     - Success criteria
     - Common pitfalls to avoid
   - **This is the MOST CRITICAL document - future Claudes MUST read this first**

3. **✅ Comprehensive Research Completed**
   - Agent research gathered extensive findings (stored in memory):
     - Anthropic skill-creator standards analysis
     - Current 36 MCNP skills assessment
     - Example files inventory (1,107 files catalogued)
     - Knowledge base organization (72 docs mapped)
     - Optimization strategy (85% token savings via batching)
   - **These findings need to be written to planning-research/ files**

### What Was IN PROGRESS When API Error Occurred 🚧

4. **🚧 SKILL-REVAMP-MASTER-PLAN.md - NOT YET CREATED**
   - Location: skill-revamp/SKILL-REVAMP-MASTER-PLAN.md
   - Status: **Was about to write when API error occurred**
   - Planned contents (9,000+ lines):
     - Section 1: Executive Summary (500 lines)
     - Section 2: Research Findings (2,000 lines)
       - Anthropic standards
       - Current skills assessment
       - Example files inventory
       - Knowledge base organization
     - Section 3: Optimization Strategy (1,500 lines)
       - Batched processing approach
       - Token consumption analysis
       - Documentation sharing matrix
     - Section 4: Structural Changes Required (1,500 lines)
     - Section 5: Implementation Workflow (1,500 lines)
     - Section 6: Quality Assurance (1,000 lines)
     - Section 7: Risk Mitigation (500 lines)
     - Section 8: Emergency Procedures (500 lines)

### What Is PENDING (Not Yet Started) ⏸️

5. **⏸️ planning-research/ files (5 files) - NOT CREATED**
   - anthropic-standards-analysis.md
   - current-skills-assessment.md
   - example-files-inventory.md
   - knowledge-base-map.md
   - optimization-strategy.md

6. **⏸️ templates/ - NOT CREATED**
   - skill-template-structure/SKILL.md (template)
   - revamp-checklist.md (25-item checklist)

7. **⏸️ .claude/skills_backup_original/ - NOT CREATED**
   - Backup of original 36 skills not yet made

---

---

## 🎉 SESSION 2 COMPLETION SUMMARY

**Date:** 2025-11-02
**Outcome:** Infrastructure Setup 100% COMPLETE ✅
**Tokens Used:** ~102k / 200k (51%)

### Session 2 Deliverables (8 documents created)

**Phase-Specific Master Plans (5 documents, ~9,000 lines total):**
1. ✅ **PHASE-1-MASTER-PLAN.md** (~3,000 lines)
   - Category A&B skills (16 skills)
   - Documentation: Chapters 3,4,5 (all 12 files), 10 (all 5 files)
   - Token budget: ~240k (docs 80k + processing 160k)
   - Detailed 11-step workflow per skill
   - Skill-specific notes for critical skills

2. ✅ **PHASE-2-MASTER-PLAN.md** (~1,300 lines)
   - Category D skills (6 skills)
   - Documentation: Chapter 8, Appendix D (7 files), Appendix E.11
   - Token budget: ~100k
   - Focus: Output formats, mesh, visualization

3. ✅ **PHASE-3-MASTER-PLAN.md** (~1,400 lines)
   - Category E skills (4 skills)
   - Documentation: Phase 2 docs + VR theory (02_07)
   - Token budget: ~90k
   - Completes partial skills from Phases 1&2

4. ✅ **PHASE-4-MASTER-PLAN.md** (~1,600 lines)
   - Category F skills (6 skills)
   - Documentation: All Appendix E (12 utility files)
   - Token budget: ~90k
   - Focus: Utilities, references, Python scripts essential

5. ✅ **PHASE-5-MASTER-PLAN.md** (~1,700 lines)
   - Category C & specialized skills (8 skills)
   - Documentation: Minimal (error catalogs, primers)
   - Token budget: ~90-120k
   - Final phase - validation, debugging, meta-skills

**Infrastructure Completion:**
6. ✅ **Original skills backed up**
   - Location: `.claude/skills_backup_original/`
   - All 36 original skills preserved before revamp

### Key Accomplishments

**Planning Infrastructure:**
- All 5 phase-specific execution plans created
- Total ~9,000 lines of detailed guidance
- Each phase has complete documentation lists, token budgets, skill ordering
- Per-skill workflows standardized across all phases

**Project Organization:**
- Modular documentation approach validated
- Phase plans created on-demand (not all at once)
- Token optimization strategy implemented
- Original skills safely backed up

**Ready State:**
- Infrastructure 100% complete
- All planning documents in place
- Original skills preserved
- Session 3 can begin Phase 1 execution immediately

### Token Efficiency

**Session 2 actual:** ~102k tokens
**Estimated:** ~150k tokens
**Efficiency:** Used 32% less than estimated

**Breakdown:**
- Read startup docs (REQUIREMENTS, STATUS, OVERVIEW): ~15k
- Create 5 phase plans: ~60k
- Backup skills: minimal
- Updates and TODO management: ~27k

---

## NEXT CLAUDE: START HERE 👇

### ✅ Infrastructure Setup: 100% COMPLETE

**What Sessions 1 & 2 Completed:**
1. ✅ Directory structure created
2. ✅ CLAUDE-SESSION-REQUIREMENTS.md (2,500+ lines) - CRITICAL document
3. ✅ SKILL-REVAMP-OVERVIEW.md (high-level guide)
4. ✅ REVAMP-PROJECT-STATUS.md (this file)
5. ✅ All 5 planning-research/ files created
6. ✅ Template structure created (SKILL.md template + READMEs + checklist)
7. ✅ PHASE-1-MASTER-PLAN.md (16 skills execution plan)
8. ✅ PHASE-2-MASTER-PLAN.md (6 skills execution plan)
9. ✅ PHASE-3-MASTER-PLAN.md (4 skills execution plan)
10. ✅ PHASE-4-MASTER-PLAN.md (6 skills execution plan)
11. ✅ PHASE-5-MASTER-PLAN.md (8 skills execution plan)
12. ✅ Original skills backed up to .claude/skills_backup_original/

**Infrastructure Status:** 100% COMPLETE ✅

---

### 🚀 SESSION 3 PRIORITIES (NEXT SESSION)

**Objective:** Begin Phase 1 execution - Revamp Category A&B skills

**Session 3 Workflow:**

1. **Read Mandatory Startup Documents** (15k tokens)
   - CLAUDE-SESSION-REQUIREMENTS.md (MUST READ FIRST)
   - REVAMP-PROJECT-STATUS.md (this file - determines current phase)
   - SKILL-REVAMP-OVERVIEW.md

2. **Create PHASE-1-PROJECT-STATUS.md** (5k tokens)
   - New status document for Phase 1 execution
   - Begin with Phase 0 summary (infrastructure complete)
   - Use REVAMP-PROJECT-STATUS.md as template
   - Set up "Currently Active Skill" section (blank initially)
   - This becomes the PRIMARY status doc for Phase 1

3. **Read Phase 1 Master Plan** (8k tokens)
   - skill-revamp/PHASE-1-MASTER-PLAN.md
   - Review 16 skills to process
   - Note documentation requirements
   - Understand 11-step workflow

4. **Read Phase 1 Documentation ONCE** (80k tokens)
   - markdown_docs/user_manual/03_Introduction_to_MCNP_Usage.md
   - markdown_docs/user_manual/04_Description_of_MCNP6_Input.md
   - markdown_docs/user_manual/chapter_05_input_cards/*.md (ALL 12 files)
   - markdown_docs/examples/chapter_10/*.md (ALL 5 files)
   - **CRITICAL:** Take comprehensive notes for reuse
   - **Update STATUS after reading complete**

5. **Begin Processing Skills** (remainder of session)
   - Start with mcnp-input-builder (highest priority)
   - Follow 11-step workflow from PHASE-1-MASTER-PLAN.md
   - Update PHASE-1-PROJECT-STATUS.md continuously after each step
   - Update THIS document when phase starts/ends
   - Estimated: 2-3 skills per session

**Token Budget for Session 3:**
- Startup docs: ~23k
- Create PHASE-1-PROJECT-STATUS.md: ~5k
- Phase 1 documentation: ~80k
- Process 2-3 skills: ~20-30k
- Updates and handoff: ~20k
- **Total: ~148-158k tokens** (fits in one session)

**Expected Outcome:**
- PHASE-1-PROJECT-STATUS.md created and active
- Phase 1 documentation read and understood
- mcnp-input-builder revamped (priority 1)
- mcnp-geometry-builder revamped (priority 2)
- Possibly mcnp-material-builder (priority 3)
- Clear STATUS in PHASE-1-PROJECT-STATUS.md for Session 4

**Key Reminders for Next Claude:**
- Create PHASE-1-PROJECT-STATUS.md at session start
- Update PHASE-1-PROJECT-STATUS.md continuously (not THIS file)
- Update THIS file only when starting/completing phases
- Read documentation ONCE, use for all 16 skills
- Don't re-read docs between skills (token waste)
- Use 25-item quality checklist for every skill
- Test each skill before marking complete

---

---

## COMPREHENSIVE RESEARCH FINDINGS (For Next Claude)

### 1. Anthropic Skill-Creator Standards Analysis

**Source:** Global skill at C:\Users\dman0\AppData\Roaming\Claude\skills\skill-creator\

**Key Requirements:**

#### YAML Frontmatter Structure
```yaml
---
name: skill-name
description: "Third-person description of when to use. Be specific about trigger conditions."
version: "1.0.0"
dependencies: "python>=3.8" # optional
---
```
- Remove non-standard fields: `activation_keywords`, `category`
- Description must be trigger-focused, not capability-focused

#### Progressive Disclosure Design
1. **Metadata** (always loaded): ~100 words in YAML
2. **SKILL.md body** (loaded when triggered): <5k words (preferably <3k)
3. **Bundled resources** (loaded as needed): Unlimited

#### Three Subdirectories Structure

**references/** - Documentation loaded into context as needed
- Detailed technical specs, schemas, API docs
- Large reference material (>10k words)
- Should include grep search patterns if files are large
- Avoid duplication with SKILL.md

**scripts/** - Executable code for deterministic tasks
- Python/Bash scripts that may be executed
- For repeatedly rewritten code or reliability-critical operations
- Include README.md explaining each script

**assets/** - Files used in output (NOT loaded into context)
- Templates, boilerplate files
- Copied or modified for user output
- Example: HTML templates, example input files

#### Writing Standards
- **Imperative/infinitive form** (verb-first): "To accomplish X, do Y"
- **NOT second person**: Avoid "you should"
- **Objective, instructional tone**
- **Description examples:**
  - ✅ Good: "This skill should be used when users want to create MCNP input files with proper formatting"
  - ❌ Bad: "Use this skill for inputs"

---

### 2. Current 36 MCNP Skills Assessment

**Skills Examined in Detail:**

#### mcnp-input-builder (Category A)
- **Length:** 1,041 lines
- **Strengths:**
  - Clear three-block structure explanation
  - Multiple practical examples
  - Comprehensive error troubleshooting
  - Integration section present
  - Validation checklist
- **Missing:**
  - No references/ subdirectory for large card specifications
  - Could extract template examples to assets/
  - Has `activation_keywords` (non-standard field)

#### mcnp-geometry-builder (Category A)
- **Length:** 1,087 lines
- **Strengths:**
  - Excellent Boolean logic explanation
  - Many surface type examples (planes, spheres, cylinders, macrobodies)
  - Lattice and transformation examples
- **Missing:**
  - Surface card specifications could be in references/surface_types.md
  - Macrobody details could be separate reference file
  - Script mentioned but no scripts/ directory

#### mcnp-output-parser (Category D)
- **Length:** 1,231 lines
- **Strengths:**
  - Python integration examples
  - Multiple file format support (OUTP, MCTAL, HDF5, XDMF)
  - Decision trees for format selection
- **Missing:**
  - File format specifications should be in references/
  - HDF5 structure details too detailed for SKILL.md
  - Python module mentioned but not in scripts/

#### mcnp-variance-reducer (Category B)
- **Length:** 1,006 lines
- Very comprehensive, well-structured
- **Missing:** Could benefit from references/vr_theory.md

**Common Quality Patterns Across All 36:**

**✅ What's Working:**
- All skills have clear "When to Use" sections
- Decision trees present in most
- Good use of code examples
- Integration sections connect skills

**❌ What's Missing Universally:**
1. No references/ subdirectories - Large reference material embedded in SKILL.md
2. No scripts/ subdirectories - Python modules mentioned but not bundled
3. No assets/ subdirectories - Template examples inline instead of separate files
4. Some descriptions could be more specific about trigger conditions
5. Variable YAML frontmatter - Some use custom fields

**Category Distribution:**
- Category A (Core input building): ~12 skills - Share ALL Chapter 5 + Chapter 10 docs
- Category B (Input editing): ~4 skills - Same as A
- Category C (Validation): ~4 skills - Minimal docs (Chapters 3, 4)
- Category D (Output/mesh): ~6 skills - Appendix D + Chapter 8
- Category E (Advanced): ~4 skills - All D + VR docs
- Category F (Utilities): ~6 skills - Appendix E docs

---

### 3. Example Files Inventory

**Total:** 1,107 MCNP input files across 9 categories

#### Directory Structure:

1. **basic_examples/** (~100 files, .txt format)
   - Simple problems: shields, sources, tallies
   - Good for skill validation tests
   - Files: shield.txt, tal01.txt, src1.txt, puc1.txt, etc.

2. **intermediate_examples/**
   - More complex multi-component problems

3. **criticality_examples/**
   - KCODE problems for criticality skills

4. **reactor-model_examples/** (⭐ MOST COMPREHENSIVE)
   - **htgr-model-burnup-and-doserates/** subdirectories:
     - agr-1/mcnp/ - 14+ real reactor input files (bench_*.i)
     - verification/ - Test cases with reference solutions
     - repeated_structures/ - Lattice examples
   - Production-quality, complex examples
   - Research article: https://nstopenresearch.org/articles/1-20/v2

5. **rad-protection_examples/**
   - Shielding and dose calculations

6. **safeguards_examples/**
   - Specialized applications

7. **unstructured-mesh_examples/**
   - Mesh tally examples for Category D/E skills

8. **variance-reduction_examples/**
   - WWG, importance sampling examples

9. **MCNP6_VnV/**
   - Verification and validation cases

**Strategic Value:**
- reactor-model_examples: Real-world complexity, burnup, lattices
- variance-reduction_examples: WWG workflows
- unstructured-mesh_examples: FMESH with XDMF output
- basic_examples: Quick validation, template generation

**Recommendation:**
- Extract 5-10 representative examples per skill category
- Place in assets/example_inputs/ with descriptions
- Reference in SKILL.md with specific use cases

---

### 4. Knowledge Base Organization

**Total Documentation:** 4.2 MB, 72 markdown files

#### Structure:
```
markdown_docs/
├── user_manual/
│   ├── 03_Introduction_to_MCNP_Usage.md
│   ├── 04_Description_of_MCNP6_Input.md
│   ├── chapter_05_input_cards/ (12 files - THE BIG ONE)
│   │   ├── 05_01_Geometry_Specification_Intro.md
│   │   ├── 05_02_Cell_Cards.md
│   │   ├── 05_03_Surface_Cards.md
│   │   ├── 05_05_Geometry_Data_Cards.md
│   │   ├── 05_06_Material_Data_Cards.md
│   │   ├── 05_07_Physics_Data_Cards.md
│   │   ├── 05_08_Source_Data_Cards.md
│   │   ├── 05_09_Tally_Data_Cards.md
│   │   ├── 05_10_Tally_Perturbations.md
│   │   ├── 05_11_Mesh_Tallies.md
│   │   ├── 05_12_Variance_Reduction_Cards.md
│   │   └── 05_13_Output_Control_Misc.md
│   └── 08_Unstructured_Mesh.md
├── appendices/
│   ├── AppendixA_Mesh_File_Formats.md
│   ├── AppendixD_03_Particle_Track_Output.md
│   ├── AppendixD_04_Mesh_Tally_XDMF.md
│   ├── AppendixD_05_Fission_Matrix.md
│   ├── AppendixD_06_Unstructured_Mesh_HDF5.md
│   ├── AppendixD_07_Unstructured_Mesh_Legacy.md
│   ├── AppendixD_08_HDF5_Script.md
│   ├── AppendixD_09_inxc_File_Structure.md
│   └── AppendixE_* (01-12: Utility tools)
├── examples/chapter_10/ (5 files)
│   ├── 10_01_Geometry_Examples.md
│   ├── 10_02_Tally_Examples.md
│   ├── 10_03_Source_Examples.md
│   ├── 10_05_Physics_Models.md
│   └── 10_06_Variance_Reduction_Examples.md
└── theory_manual/chapter_02/
    └── 02_07_Variance_Reduction.md
```

**Documentation Sharing Patterns:**

**Category A & B (16 skills) - LARGEST OVERLAP:**
- All of Chapter 5 (12 files) - Input cards
- All of Chapter 10 examples (5 files)
- Chapters 3, 4
- **Total: ~20 files, ~1 MB**
- **Shared by:** input-builder, geometry-builder, material-builder, source-builder, tally-builder, physics-builder, lattice-builder, geometry-editor, input-editor, input-validator, cell-checker, cross-reference-checker, geometry-checker, physics-validator, transform-editor, variance-reducer

**Category D (6 skills):**
- Chapter 8 (Unstructured Mesh)
- Appendix D (D.3-D.9: 7 files)
- Appendix E.11 (Post-processing)
- **Shared by:** output-parser, mctal-processor, mesh-builder, plotter, tally-analyzer (partial), statistics-checker (partial)

**Category E (4 skills):**
- All Category D docs PLUS:
- Variance reduction: 05_12, 10_06, theory 02_07
- **Shared by:** variance-reducer, ww-optimizer, tally-analyzer (complete), statistics-checker (complete)

**Category F (6 skills):**
- Appendix E (E.1-E.12 utility tools)
- **Shared by:** unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator

---

### 5. Optimization Strategy (TOKEN SAVINGS)

#### Problem: Sequential Reading Wastes Tokens

**Sequential approach (DON'T DO THIS):**
- Skill 1: Read 20 docs (80k tokens) + process (10k) = 90k
- Skill 2: Read SAME 20 docs (80k tokens) + process (10k) = 90k
- Skill 3: Read SAME 20 docs (80k tokens) + process (10k) = 90k
- ...for 16 skills = 1,440k tokens total
- **EXTREMELY WASTEFUL**

**Batched approach (DO THIS):**
- Read 20 docs ONCE (80k tokens)
- Process skill 1 (10k tokens)
- Process skill 2 (10k tokens)
- Process skill 3 (10k tokens)
- ...for 16 skills = 80k + 160k = 240k tokens total
- **SAVES 1,200k tokens (83% reduction!)**

#### Batched Processing Plan

**Phase 1: Category A & B (16 skills)**
- Read ONCE: Chapters 3, 4, all Chapter 5 (12 files), all Chapter 10 (5 files)
- Token cost: ~80k (one-time) + 10k×16 (processing) = 240k tokens
- Sessions needed: 2-3 (with 200k token limit per session)
- Skills:
  1. mcnp-input-builder
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
  16. mcnp-variance-reducer (partially)

**Phase 2: Category D (6 skills)**
- Read ONCE: Chapter 8, Appendix D (all), Appendix E.11
- Token cost: ~40k + 60k = 100k tokens
- Sessions needed: 1
- Skills: output-parser, mctal-processor, mesh-builder, plotter, tally-analyzer (partial), statistics-checker (partial)

**Phase 3: Category E (4 skills)**
- Read ONCE: All D docs + variance reduction docs
- Token cost: ~50k + 40k = 90k tokens
- Sessions needed: 1
- Skills: variance-reducer (complete), ww-optimizer, tally-analyzer (complete), statistics-checker (complete)

**Phase 4: Category F (6 skills)**
- Read ONCE: Appendix E (all utility tools)
- Token cost: ~30k + 60k = 90k tokens
- Sessions needed: 1
- Skills: unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator

**Phase 5: Category C & Specialized (4 skills)**
- Read: Minimal docs, skill-specific
- Token cost: ~20k + 40k = 60k tokens
- Sessions needed: 1
- Skills: fatal-error-debugger, warning-analyzer, criticality-analyzer, best-practices-checker, example-finder, knowledge-docs-finder, burnup-builder, input-updater

**Total Token Budget:**
- Batched: ~430k tokens
- Sequential: ~2,400k tokens
- **Savings: ~2,000k tokens (85% reduction)**

---

## PHASE-BY-PHASE EXECUTION PLAN

### Phase 0: Infrastructure Setup (Current Session)
**Status:** ~50% complete (API error interrupted)
**Tasks:**
- ✅ Create directory structure
- ✅ Create CLAUDE-SESSION-REQUIREMENTS.md
- 🚧 Create SKILL-REVAMP-MASTER-PLAN.md (NEXT PRIORITY)
- ⏸️ Create planning-research/ files
- ⏸️ Create templates/
- ⏸️ Backup original skills

### Phase 1: Category A & B - 16 Skills (Sessions 2-3)
**Documentation to read (ONCE):**
- markdown_docs/user_manual/03_Introduction_to_MCNP_Usage.md
- markdown_docs/user_manual/04_Description_of_MCNP6_Input.md
- markdown_docs/user_manual/chapter_05_input_cards/*.md (ALL 12 FILES)
- markdown_docs/examples/chapter_10/*.md (ALL 5 FILES)

**Skills to process:**
1. mcnp-input-builder (foundational - do first)
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

**Per-skill workflow:**
1. Read current SKILL.md
2. Review against knowledge base docs (already read)
3. Identify discrepancies/gaps
4. Create skill revamp plan
5. Extract to references/ (card specs, theory, detailed examples)
6. Add examples from example_files/basic_examples/ and reactor-model_examples/
7. Create/update scripts/ (if Python modules mentioned)
8. Streamline SKILL.md to <3k words
9. Run 25-item quality checklist
10. Test skill invocation
11. Update REVAMP-PROJECT-STATUS.md

**Expected:**
- Token usage: ~240k tokens
- Sessions: 2-3
- Time: 6-8 hours

### Phase 2: Category D - 6 Skills (Session 4)
**Documentation to read (ONCE):**
- markdown_docs/user_manual/08_Unstructured_Mesh.md
- markdown_docs/appendices/AppendixA_Mesh_File_Formats.md
- markdown_docs/appendices/AppendixD_03_Particle_Track_Output.md
- markdown_docs/appendices/AppendixD_04_Mesh_Tally_XDMF.md
- markdown_docs/appendices/AppendixD_05_Fission_Matrix.md
- markdown_docs/appendices/AppendixD_06_Unstructured_Mesh_HDF5.md
- markdown_docs/appendices/AppendixD_07_Unstructured_Mesh_Legacy.md
- markdown_docs/appendices/AppendixD_08_HDF5_Script.md
- markdown_docs/appendices/AppendixD_09_inxc_File_Structure.md
- markdown_docs/appendices/AppendixE_11_UM_Post_Processing.md

**Skills to process:**
1. mcnp-output-parser
2. mcnp-mctal-processor
3. mcnp-mesh-builder
4. mcnp-plotter
5. mcnp-tally-analyzer (if not fully done in Phase 1)
6. mcnp-statistics-checker (if not fully done in Phase 1)

**Expected:**
- Token usage: ~100k tokens
- Sessions: 1
- Time: 3-4 hours

### Phase 3: Category E - 4 Skills (Session 5)
**Documentation to read (ONCE):**
- All Category D docs (if not cached)
- markdown_docs/theory_manual/chapter_02/02_07_Variance_Reduction.md
- markdown_docs/user_manual/chapter_05_input_cards/05_12_Variance_Reduction_Cards.md
- markdown_docs/examples/chapter_10/10_06_Variance_Reduction_Examples.md

**Skills to process:**
1. mcnp-variance-reducer (complete if partial from Phase 1)
2. mcnp-ww-optimizer
3. mcnp-tally-analyzer (complete if partial from Phase 2)
4. mcnp-statistics-checker (complete if partial from Phase 2)

**Expected:**
- Token usage: ~90k tokens
- Sessions: 1
- Time: 2-3 hours

### Phase 4: Category F - 6 Skills (Session 6)
**Documentation to read (ONCE):**
- markdown_docs/appendices/AppendixE_01_Doppler_Broadening.md
- markdown_docs/appendices/AppendixE_02_Event_Log_Analyzer.md
- markdown_docs/appendices/AppendixE_03_Doppler_Fitting.md
- markdown_docs/appendices/AppendixE_04_Gridconv.md
- markdown_docs/appendices/AppendixE_05_Cross_Section_Tool.md
- markdown_docs/appendices/AppendixE_06_Merge_ASCII_Tally.md
- markdown_docs/appendices/AppendixE_07_Merge_Mesh_Tally.md
- markdown_docs/appendices/AppendixE_08_Parameter_Study_Tool.md
- markdown_docs/appendices/AppendixE_09_Simple_ACE_Tools.md
- markdown_docs/appendices/AppendixE_10_UM_Converter.md
- markdown_docs/appendices/AppendixE_11_UM_Post_Processing.md
- markdown_docs/appendices/AppendixE_12_UM_Pre_Processing.md

**Skills to process:**
1. mcnp-unit-converter
2. mcnp-physical-constants
3. mcnp-isotope-lookup
4. mcnp-cross-section-manager
5. mcnp-parallel-configurator
6. mcnp-template-generator

**Expected:**
- Token usage: ~90k tokens
- Sessions: 1
- Time: 2-3 hours

### Phase 5: Category C & Specialized (Session 7)
**Documentation to read:**
- Skill-specific, minimal overlap

**Skills to process:**
1. mcnp-fatal-error-debugger
2. mcnp-warning-analyzer
3. mcnp-criticality-analyzer
4. mcnp-best-practices-checker
5. mcnp-example-finder
6. mcnp-knowledge-docs-finder
7. mcnp-burnup-builder
8. mcnp-input-updater

**Expected:**
- Token usage: ~60k tokens
- Sessions: 1
- Time: 2-3 hours

---

## QUICK STATUS OVERVIEW

### Infrastructure Setup (Phase 0)
- Directory structure: ✅ COMPLETE
- CLAUDE-SESSION-REQUIREMENTS.md: ✅ COMPLETE (2,500+ lines)
- SKILL-REVAMP-MASTER-PLAN.md: 🚧 NEXT PRIORITY
- REVAMP-PROJECT-STATUS.md: ✅ COMPLETE (this file)
- planning-research/ files: ⏸️ PENDING
- templates/: ⏸️ PENDING
- Backup: ⏸️ PENDING

### Skill Revamp Progress
- Phase 1 (A&B - 16 skills): ⏸️ NOT STARTED
- Phase 2 (D - 6 skills): ⏸️ NOT STARTED
- Phase 3 (E - 4 skills): ⏸️ NOT STARTED
- Phase 4 (F - 6 skills): ⏸️ NOT STARTED
- Phase 5 (C+ - 4 skills): ⏸️ NOT STARTED

**Total Progress: 0/36 skills revamped (0%)**
**Infrastructure: 2/7 tasks complete (~29%)**

---

## SESSION HANDOFF FOR NEXT CLAUDE

### Resume From Here:

**You are picking up in the middle of Infrastructure Setup (Phase 0).**

**Completed:**
1. ✅ All directory structures created
2. ✅ CLAUDE-SESSION-REQUIREMENTS.md written (2,500+ lines) - READ THIS FIRST!

**Next Actions (in order):**
1. **Create SKILL-REVAMP-MASTER-PLAN.md** (highest priority)
   - Use "COMPREHENSIVE RESEARCH FINDINGS" section above
   - Structure as 8 sections per CLAUDE-SESSION-REQUIREMENTS.md
   - ~9,000 lines total
   - This provides complete project strategy

2. **Create planning-research/ files (5 files)**
   - Extract from research findings above
   - anthropic-standards-analysis.md
   - current-skills-assessment.md
   - example-files-inventory.md
   - knowledge-base-map.md
   - optimization-strategy.md

3. **Create templates/**
   - skill-template-structure/SKILL.md (template)
   - skill-template-structure/references/README.md
   - skill-template-structure/scripts/README.md
   - skill-template-structure/assets/README.md
   - revamp-checklist.md (25-item checklist)

4. **Create backup**
   - Copy .claude/skills/ to .claude/skills_backup_original/

5. **Begin Phase 1** (if tokens allow)
   - Start revamping Category A&B skills

**Critical Notes:**
- All research findings are captured in this STATUS document
- CLAUDE-SESSION-REQUIREMENTS.md has complete workflow procedures
- Zero context lost - you have everything needed to continue
- API error interrupted but no work was lost

---

## TOKEN TRACKING

**Session 1 (This Session):**
- Used: ~94,000 tokens
- Remaining: ~106,000 tokens
- Status: API error occurred, infrastructure ~50% complete

**Estimated for Remaining Infrastructure (Session 2):**
- SKILL-REVAMP-MASTER-PLAN.md: ~15k tokens
- planning-research/ files: ~10k tokens
- templates/: ~3k tokens
- Backup: minimal
- **Total: ~28k tokens**
- **Leaves ~150k tokens for starting Phase 1 work**

---

---

## SESSION 1 FINAL SUMMARY

**Date:** 2025-11-02
**Status:** Infrastructure Setup Complete (85%)
**Tokens Used:** ~132k / 200k (66%)
**Outcome:** ✅ Successful - Zero context lost

### Deliverables Created

**Core Documents (3):**
1. ✅ CLAUDE-SESSION-REQUIREMENTS.md (2,500 lines) - **MOST CRITICAL**
2. ✅ SKILL-REVAMP-OVERVIEW.md (1,500 lines)  - High-level guide
3. ✅ REVAMP-PROJECT-STATUS.md (This file) - Progress tracker

**Planning Research (5 files):**
4. ✅ anthropic-standards-analysis.md - Skill-creator standards
5. ✅ current-skills-assessment.md - 36 skills analyzed
6. ✅ example-files-inventory.md - 1,107 files catalogued
7. ✅ knowledge-base-map.md - 72 docs mapped
8. ✅ optimization-strategy.md - Token savings analysis

**Templates (4 files):**
9. ✅ skill-template-structure/SKILL.md - Template
10. ✅ skill-template-structure/references/README.md
11. ✅ skill-template-structure/scripts/README.md
12. ✅ skill-template-structure/assets/README.md
13. ✅ revamp-checklist.md - 25-item QA checklist

**Total:** 13 comprehensive documentation files created

### Key Decisions Made

1. **Modular Master Plans:** Split into 5 phase-specific plans (not one 9,000-line document)
2. **Batched Processing:** Read docs ONCE per category (85% token savings)
3. **Progressive Disclosure:** Extract content to references/, scripts/, assets/
4. **Example Integration:** Use 1,107 files from example_files/ (critical gap fixed)

### Critical Context Preserved

**All research findings captured in:**
- REVAMP-PROJECT-STATUS.md (comprehensive research section)
- planning-research/ files (detailed analysis)
- SKILL-REVAMP-OVERVIEW.md (strategy and approach)

**Zero context lost - Next Claude has everything needed to continue**

### Session 2 Priorities

1. Create 5 phase-specific master plans (~40-50k tokens)
2. Backup original skills (minimal tokens)
3. Begin Phase 1 execution if tokens allow (~100k tokens)

**Estimated Session 2 completion:** Phase-specific plans + backup + start Phase 1

---

**END OF REVAMP-PROJECT-STATUS.md**

**Remember:** Read CLAUDE-SESSION-REQUIREMENTS.md FIRST every session!
