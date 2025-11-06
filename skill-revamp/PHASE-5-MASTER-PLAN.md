# PHASE 5 MASTER PLAN - CATEGORY C & SPECIALIZED SKILLS (8 SKILLS)

**Phase:** 5 of 5 (FINAL PHASE)
**Skills:** 8 (Category C: Validation + Specialized/Meta Skills)
**Estimated Sessions:** 1
**Estimated Tokens:** ~80k tokens
**Created:** 2025-11-02 (Session 2)

---

## 🎯 PHASE OVERVIEW

### Objectives
Complete the final 8 skills: validation/debugging tools and specialized meta-skills that help users navigate the MCNP ecosystem.

### Why This Phase Last?
1. **Minimal shared documentation** - Each skill relatively independent
2. **Build on all previous phases** - Reference other skills extensively
3. **Meta-skills** - Help users find and use other skills
4. **Cleanup phase** - Final integration and cross-referencing

### Token Optimization Strategy
- **Sequential approach:** 8 skills × 50k tokens = 400k tokens ❌
- **Batched approach:** 20k (minimal docs) + 80k (8×10k) = 100k tokens ✅
- **Savings:** 300k tokens (75% reduction)

---

## 🚨 PARALLEL EXECUTION SUPPORT 🚨

**This phase has FULL parallel execution support - HIGHEST PRIORITY phase.**

### Parallel Execution Capabilities

**Phase 5 Status:** ⏸️ NOT STARTED - 0/8 skills complete (0%)

**Can Execute in Parallel with:**
- ✅ Phase 1 (different documentation)
- ✅ Phase 2 (different documentation)
- ✅ Phase 3 (independent)
- ✅ Phase 4 (independent)

**Dependencies:** NONE - All Phase 5 skills are fully independent

**🚨 CRITICAL: HIGHEST PRIORITY PHASE 🚨**
- These are validation/debugging skills that should have been done first
- mcnp-fatal-error-debugger and mcnp-warning-analyzer are ESSENTIAL
- mcnp-best-practices-checker ensures quality across all skills
- mcnp-example-finder and knowledge-docs-finder help navigate ecosystem

### Skills - All Independent and HIGH PRIORITY

All 8 skills can start immediately:
1. ⏸️ mcnp-fatal-error-debugger (CRITICAL)
2. ⏸️ mcnp-warning-analyzer (CRITICAL)
3. ⏸️ mcnp-best-practices-checker (HIGH VALUE)
4. ⏸️ mcnp-example-finder (HIGH VALUE)
5. ⏸️ mcnp-knowledge-docs-finder (HIGH VALUE)
6. ⏸️ mcnp-criticality-analyzer
7. ⏸️ mcnp-burnup-builder
8. ⏸️ mcnp-input-updater

**Parallelization Strategy:**
- **HIGHEST PRIORITY** - Start Phase 5 ASAP, don't wait for other phases
- Can execute in parallel with ALL other phases
- All 8 skills can be split across multiple sessions
- Recommend: Start with skills 1-5 (most critical)
- Single session can complete 4-6 skills

### Session ID Tracking

**Every session working on Phase 5 MUST:**

1. **Generate unique session ID:** `Session-YYYYMMDD-HHMMSS-Phase5`
2. **Record in PHASE-5-PROJECT-STATUS.md**
3. **Update GLOBAL-SESSION-REQUIREMENTS.md lines 159-182 (Phase 5 section)**

### Coordination with Global Requirements

**Session startup reads:**
1. GLOBAL-SESSION-REQUIREMENTS.md
2. TOKEN-OPTIMIZATION-BEST-PRACTICES.md
3. THIS FILE (PHASE-5-MASTER-PLAN.md)
4. PHASE-5-PROJECT-STATUS.md
5. LESSONS-LEARNED.md

---

## 🚨 CRITICAL STRUCTURE REQUIREMENTS (ZERO TOLERANCE)

**MANDATORY for ALL Phase 5 skills - NO EXCEPTIONS:**

### Correct Directory Structure
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── fatal_error_catalog.md            ← Reference files at ROOT level
├── warning_catalog.md                ← NOT in subdirectories
├── example_catalog.md                ← Same level as SKILL.md
├── [other-reference].md              ← Root skill directory
├── scripts/                          ← Subdirectory for scripts ONLY
│   ├── error_parser.py
│   ├── example_finder.py
│   └── README.md
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    └── [error examples or data]
```

### WRONG Structures (NEVER CREATE THESE)
```
❌ WRONG #1: references/ subdirectory
.claude/skills/[skill-name]/
└── references/                       ← WRONG - No subdirectory!
    └── [reference files]             ← Should be at root level

❌ WRONG #2: assets/ subdirectory (MOST COMMON ERROR)
.claude/skills/[skill-name]/
└── assets/                           ← WRONG - assets/ NEVER EXISTS!
    └── example_inputs/               ← Should be at root level
```

**Reference:** CLAUDE-SESSION-REQUIREMENTS.md lines 495-540, LESSONS-LEARNED.md Lesson #16

---

## 📚 DOCUMENTATION TO READ (ONCE AT PHASE START)

### Required Reading List

Phase 5 skills have **minimal shared documentation** - mostly skill-specific needs.

#### Core Error/Validation Documentation (2-3 files)

1. **markdown_docs/user_manual/03_Introduction_to_MCNP_Usage.md** (if not cached)
   - Purpose: Basic execution, error messages overview
   - Key sections: §3.5 Error messages, §3.6 Debugging
   - Token estimate: ~15k (if not cached) or 0k (if cached from Phase 1)

2. **markdown_docs/user_manual/04_Description_of_MCNP6_Input.md** (if not cached)
   - Purpose: Input format, common errors
   - Key sections: §4.7 Input Error Messages, §4.8 Geometry Errors
   - Token estimate: ~20k (if not cached) or 0k (if cached from Phase 1)

#### Skill-Specific Documentation

3. **markdown_docs/primers/source_primer/05_Known_Source_Errors.md**
   - Purpose: Common source definition errors
   - Token estimate: ~5k
   - Needed for: fatal-error-debugger, warning-analyzer

4. **markdown_docs/user_manual/chapter_05_input_cards/05_13_Output_Control_Misc.md**
   - Purpose: Error message tables, debugging cards
   - Token estimate: Included in Phase 1 (0k if cached)

5. **Skills Project Documentation** (existing in this project)
   - Location: `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\skills-project-docs\`
   - Purpose: Meta information about skill ecosystem
   - Token estimate: ~5k
   - Needed for: example-finder, knowledge-docs-finder

### Total Documentation
- **Minimal new reading:** ~5-10k tokens (primers, project docs)
- **If Phase 1 cached:** ~10k tokens
- **If Phase 1 not cached:** ~40k tokens
- **Read:** As needed per skill (not all skills need all docs)

### Documentation Strategy for Phase 5
**Different from previous phases:**
- NOT read all docs upfront
- Read specific docs as needed per skill
- Many skills rely on previous phase knowledge
- Focus on error patterns, debugging, meta-navigation

---

## 🛠️ SKILLS TO PROCESS (6 TOTAL)

### Processing Order

#### Validation & Debugging (3 skills)

1. **mcnp-fatal-error-debugger** (Category C)
   - **Priority:** HIGHEST - Critical for users
   - **Current:** ~950 lines (estimate)
   - **Focus:** Diagnosing and fixing fatal MCNP errors
   - **Key capabilities:**
     - Error message interpretation
     - Geometry errors (lost particles, overlaps, gaps)
     - Input syntax errors
     - Source problems (outside geometry, wrong distributions)
     - BAD TROUBLE messages
     - Memory/resource errors
   - **Documentation needs:**
     - Chapter 4 §4.7-4.8 (error messages)
     - Source primer error section
   - **References to create:**
     - fatal_error_catalog.md (comprehensive error patterns)
     - geometry_error_guide.md (lost particles, overlaps, gaps)
     - source_error_guide.md (source definition problems)
     - bad_trouble_guide.md (critical errors, recovery)
     - debugging_workflow.md (systematic debugging approach)
   - **Scripts to bundle:**
     - error_parser.py (parse output for error patterns)
     - lost_particle_analyzer.py (analyze lost particle locations)
   - **example_files/ needed:**
     - Problematic inputs with errors (from basic_examples/)
     - Error output examples with fixes

2. **mcnp-warning-analyzer** (Category C)
   - **Priority:** High
   - **Current:** ~850 lines (estimate)
   - **Focus:** Interpreting and addressing warning messages
   - **Key capabilities:**
     - Material warnings (negative densities, missing data)
     - Physics warnings (energy cutoffs, particle production)
     - Statistical warnings (poor convergence)
     - Deprecation warnings
     - Performance warnings
   - **References to create:**
     - warning_catalog.md (all warning types, meanings, actions)
     - material_warnings.md (density, cross-section warnings)
     - statistical_warnings.md (convergence, FOM warnings)
   - **Scripts to bundle:**
     - warning_filter.py (parse and categorize warnings)
     - warning_prioritizer.py (identify critical warnings)
   - **example_files/ needed:**
     - Output files with various warnings
     - Warning fixes demonstrated

3. **mcnp-best-practices-checker** (Bonus skill)
   - **Priority:** Medium
   - **Current:** ~800 lines (estimate)
   - **Focus:** Check inputs against 57-item best practices checklist
   - **Key capabilities:**
     - Setup best practices (Chapter 3.4.1)
     - Preproduction practices (Chapter 3.4.2)
     - Production run practices (Chapter 3.4.3)
     - Criticality-specific practices (Chapter 3.4.4)
     - Automated checking where possible
   - **Documentation needs:**
     - Chapter 3 (MCNP usage, best practices section)
   - **References to create:**
     - best_practices_catalog.md (all 57 items from Chapter 3.4)
     - setup_checklist.md (items 1-24)
     - production_checklist.md (items 25-45)
     - criticality_checklist.md (items 46-57)
   - **Scripts to bundle:**
     - best_practices_checker.py (automated checking)
     - checklist_generator.py (generate custom checklists)
   - **Assets needed:**
     - Interactive checklist (markdown/PDF)
     - Best practices quick reference

#### Meta/Navigation Skills (3 skills)

4. **mcnp-example-finder** (Category F)
   - **Priority:** High - Help users navigate examples
   - **Current:** ~750 lines (estimate)
   - **Focus:** Find relevant MCNP examples from example_files/
   - **Key capabilities:**
     - Search 1,107 example files by keyword, problem type
     - Categorize examples (basic, reactor, VR, mesh, etc.)
     - Recommend examples for skill learning
     - Index by complexity level
   - **Documentation needs:**
     - skills-project-docs/ (example organization)
     - example_files/ directory structure
   - **References to create:**
     - example_catalog.md (all 1,107 files categorized)
     - example_index_by_topic.md (geometry, tallies, sources, etc.)
     - example_index_by_complexity.md (basic, intermediate, advanced)
     - reactor_examples_guide.md (reactor-model_examples/ detailed)
   - **Scripts to bundle:**
     - example_finder.py (search and retrieve examples)
     - example_indexer.py (create searchable index)
   - **Assets needed:**
     - Example index database (JSON)
     - Quick reference to example categories

5. **mcnp-knowledge-docs-finder** (Category F)
   - **Priority:** Medium - Help navigate documentation
   - **Current:** ~700 lines (estimate)
   - **Focus:** Find relevant sections in markdown_docs/
   - **Key capabilities:**
     - Search 72 markdown documentation files
     - Find card specifications
     - Locate examples in Chapter 10
     - Search by keyword or card name
   - **Documentation needs:**
     - skills-project-docs/ (documentation organization)
     - markdown_docs/ directory structure
   - **References to create:**
     - documentation_map.md (all 72 files organized)
     - card_index.md (which cards in which files)
     - topic_index.md (find topics across docs)
   - **Scripts to bundle:**
     - doc_finder.py (search documentation)
     - card_lookup.py (find card specification by name)
   - **Assets needed:**
     - Documentation index (JSON)
     - Card-to-file mapping

6. **mcnp-criticality-analyzer** (Bonus skill)
   - **Priority:** Medium - Specialized analysis
   - **Current:** ~850 lines (estimate)
   - **Focus:** Analyze KCODE criticality calculations
   - **Key capabilities:**
     - keff analysis (mean, std dev, confidence intervals)
     - Entropy convergence checking
     - Source distribution convergence
     - Shannon entropy interpretation
     - Cycle-to-cycle variability
     - Active cycle determination
   - **Documentation needs:**
     - Chapter 5 (KCODE card specification)
     - Statistical theory (if available)
   - **References to create:**
     - kcode_analysis.md (keff, entropy, convergence)
     - criticality_statistics.md (confidence intervals, correlation)
     - source_convergence.md (entropy, distribution)
   - **Scripts to bundle:**
     - kcode_analyzer.py (parse and analyze KCODE output)
     - entropy_plotter.py (visualize entropy convergence)
   - **example_files/ needed:**
     - criticality_examples/ outputs
     - KCODE convergence examples

---

## 📋 PER-SKILL WORKFLOW (11 STEPS)

### Same Core Workflow as Previous Phases

For EACH of the 6 skills, follow the standard 11-step workflow:

1. **Read Current SKILL.md** (2k tokens)
2. **Cross-Reference with Documentation** (0k if cached, or read specific docs as needed)
3. **Identify Discrepancies and Gaps** (1k tokens)
4. **Create Skill Revamp Plan** (1k tokens)
5. **Extract Content to Root Skill Directory** (2k tokens) - Reference .md files at ROOT level
6. **Add Example Files to example_inputs/ at ROOT Level** (1k tokens) - DIRECTLY at root, NO assets/
7. **Create/Bundle Scripts** (1k tokens)
8. **Streamline SKILL.md** (3k tokens)
9. **Validate Quality - 26-Item Checklist** (1k tokens)
10. **Test Skill** (minimal tokens)
11. **Update PHASE-5-PROJECT-STATUS.md** (minimal tokens)

**Total per skill:** ~10k tokens

### Special Considerations for Phase 5

**Documentation Reading (Step 2):**
- Not batched upfront like previous phases
- Read specific sections as needed per skill
- Many skills reference Phases 1-4 work (zero tokens)

**Integration (Throughout):**
- Extensive cross-referencing to other skills
- Meta-skills help users navigate skill ecosystem
- Validation skills use knowledge from all phases

---

## 🎯 EXECUTION CHECKLIST

### Before Starting Phase 5
- [ ] Phases 1-4 complete (32 skills revamped)
- [ ] Check which skills were completed in Phase 1:
  - [ ] mcnp-input-validator - done in Phase 1? [Yes/No]
  - [ ] mcnp-geometry-checker - done in Phase 1? [Yes/No]
  - If done, count as 6 skills in Phase 5, not 8
- [ ] PHASE-5-PROJECT-STATUS.md updated with Phase 5 start
- [ ] Token budget noted (~90-120k depending on cache)

### Documentation Reading (As Needed Per Skill)
- [ ] Check Phase 1 cache (Chapters 3-4)
- [ ] Read primers if needed (source errors, etc.)
- [ ] Read skills-project-docs for meta-skills
- [ ] Take notes for error/warning catalogs

### Skill Processing (6-8 iterations)
**For each skill:**
- [ ] Check if already done in Phase 1 first
- [ ] Follow 11-step workflow
- [ ] Extract reference .md files to ROOT level (NOT in subdirectories)
- [ ] Add to example_inputs/ DIRECTLY at root (NO assets/)
- [ ] Emphasize integration with other skills
- [ ] Create comprehensive error catalogs
- [ ] Update STATUS continuously
- [ ] Complete 26-item quality checklist (includes NO assets/ check)

**Skills (in order):**
1. [ ] mcnp-fatal-error-debugger
2. [ ] mcnp-warning-analyzer
3. [ ] mcnp-best-practices-checker
4. [ ] mcnp-example-finder
5. [ ] mcnp-knowledge-docs-finder
6. [ ] mcnp-criticality-analyzer

### Phase 5 Completion = PROJECT COMPLETION
- [ ] All 6 Phase 5 skills completed
- [ ] **ALL 36 SKILLS REVAMPED** 🎉
- [ ] Final integration check across all phases
- [ ] Create skill ecosystem map (which skills connect to which)
- [ ] PHASE-5-PROJECT-STATUS.md marked as COMPLETE
- [ ] Celebrate! 🎊

---

## 🔍 SKILL-SPECIFIC NOTES

### mcnp-fatal-error-debugger (Skill #1 - CRITICAL)
**Why first:** Most needed when things go wrong
**Key focus:**
- Comprehensive error catalog
- Clear fix procedures for each error
- Visual examples (geometry plots for lost particles)
**Integration critical:**
- Reference ALL other skills for fixes
- Example: "Lost particle → see geometry-checker skill"
**References essential:**
- fatal_error_catalog.md must be COMPREHENSIVE
- Include every error message from Chapter 4

### mcnp-example-finder (Skill #4 - HIGH VALUE)
**Why high value:** Helps users navigate 1,107 examples
**Key focus:**
- Searchable index of all examples
- Categorization by topic and complexity
- Recommendations per skill
**Python script ESSENTIAL:**
- example_finder.py must search by keyword
- example_indexer.py creates searchable database
**Assets critical:**
- Complete example catalog (all 1,107 files)
- Organized by: topic, complexity, skill relevance
**Integration:**
- Reference which skills use which examples
- Link from EVERY skill to relevant examples

### mcnp-knowledge-docs-finder (Skill #5 - META)
**Why meta:** Helps navigate knowledge base itself
**Key focus:**
- Map 72 documentation files
- Find card specs quickly
- Search by topic/keyword
**Python script ESSENTIAL:**
- doc_finder.py with keyword search
- card_lookup.py with fuzzy matching
**Integration:**
- Reference from documentation sections of all skills
- Help users find detailed info beyond SKILL.md

### mcnp-best-practices-checker (Skill #3 - QUALITY)
**Why important:** Ensures good simulation practices
**Key focus:**
- 57-item checklist from Chapter 3.4
- Automated checking where possible
- Interactive checklist for manual items
**Categories (from Chapter 3.4):**
- Setup (items 1-24): Input preparation, problem definition
- Preproduction (items 25-45): Trial runs, convergence
- Production (items 46-52): Final runs, documentation
- Criticality (items 53-57): KCODE-specific
**Python script:**
- Automated checks (syntax, formats)
- Generate checklist for manual review

---

## 🚨 PHASE 5 CONTINGENCIES

**Actions:**
1. Check REVAMP-PROJECT-STATUS.md carefully
2. If done: Mark as complete, skip in Phase 5
3. If not done: Process in Phase 5
4. Update skill count (6 vs 8 skills)
5. Adjust token budget accordingly

### If Error Catalogs Are Incomplete
**Issue:** Chapter 4 may not list all error messages

**Actions:**
1. Supplement with real error examples
2. Create error pattern matching (not exhaustive list)
3. Focus on common errors (80/20 rule)
4. Note that catalog will grow with user feedback
5. Provide debugging methodology, not just error list

### If Meta-Skills Hard to Define
**Issue:** example-finder and knowledge-docs-finder are meta

**Actions:**
1. Focus on practical utility
2. Interactive tools are key (Python scripts)
3. Use cases showing how they help
4. Integration examples with other skills
5. Root-level supplemenental [reference-doc].md files and scripts/ are more important than detailed SKILL.md

---

## ✅ PHASE 5 SUCCESS CRITERIA

### Phase Complete When:
- ✅ All required Phase 5 skills completed
- ✅ Every skill passes 26-item quality checklist (includes NO assets/ check)
- ✅ Error catalogs comprehensive
- ✅ Meta-skills have functional search tools
- ✅ Integration map complete (all 36 skills connected)
- ✅ PHASE-5-PROJECT-STATUS.md marked COMPLETE
- ✅ Token budget within estimates (~90-120k)
- ✅ **PROJECT COMPLETE** 🎉

### PROJECT SUCCESS (ALL 36 SKILLS):
- ✅ Phase 1: 16 skills complete (Categories A&B)
- ✅ Phase 2: 6 skills complete (Category D)
- ✅ Phase 3: 4 skills complete (Category E)
- ✅ Phase 4: 6 skills complete (Category F)
- ✅ Phase 5: 6-8 skills complete (Category C + specialized)
- ✅ **TOTAL: 36/36 skills revamped** ✅
- ✅ All skills pass quality checklists
- ✅ All skills tested and validated
- ✅ Integration complete
- ✅ Documentation comprehensive
- ✅ Zero context loss throughout

---

## 📈 PROGRESS TRACKING

**Monitor in PHASE-5-PROJECT-STATUS.md:**

```markdown
## PHASE 5 PROGRESS (FINAL PHASE)

**Status:** [In Progress / Complete]
**Session:** [Current session number]
**Tokens used:** [X]k / 120k budgeted

### Phase 1 Skills Check
- [ ] mcnp-input-validator - Completed in Phase 1? [Yes/No]
- [ ] mcnp-geometry-checker - Completed in Phase 1? [Yes/No]

### Documentation Reading
- [ ] Phase 1 docs (if needed) - [Status]
- [ ] Source primer errors - [Status]
- [ ] skills-project-docs/ - [Status]
- [ ] Documentation phase complete: [✅/⏸️]

### Skills Completed: X/[6-8] (Y%)

**Validation & Debugging:**
1. [ ] mcnp-fatal-error-debugger
2. [ ] mcnp-warning-analyzer
3. [ ] mcnp-input-validator (if not in Phase 1)
4. [ ] mcnp-geometry-checker (if not in Phase 1)
5. [ ] mcnp-best-practices-checker

**Meta/Navigation:**
6. [ ] mcnp-example-finder
7. [ ] mcnp-knowledge-docs-finder

**Specialized:**
8. [ ] mcnp-criticality-analyzer

**Phase 5 Complete:** [Date/Session]

---

## 🎉 PROJECT COMPLETION STATUS

**Total Skills:** 36/36 ✅
**All Phases Complete:** [Date]
**Total Sessions:** [X]
**Total Tokens Used:** [Y]k
**Token Savings vs Sequential:** [Z]k (XX%)

**SUCCESS!** All 36 MCNP skills revamped to Anthropic standards! 🎊
```

---

## 🔗 FINAL INTEGRATION

### Phase 5 Integration with All Phases

**Validation skills support ALL other phases:**
- fatal-error-debugger → Helps when any skill's output fails
- warning-analyzer → Interprets warnings from any simulation
- best-practices-checker → Validates inputs from any builder skill

**Meta-skills connect entire ecosystem:**
- example-finder → Helps users find examples for any skill
- knowledge-docs-finder → Helps users learn more about any topic

**Criticality analyzer:**
- Specialized for KCODE (source-builder from Phase 1)
- Uses tally-analyzer (Phase 3) for statistics
- Uses statistics-checker (Phase 3) for convergence

### Final Cross-Reference Review
**After Phase 5 complete:**
1. Review all 36 skills' integration sections
2. Ensure bidirectional links (if A mentions B, B should mention A)
3. Create ecosystem map showing all connections
4. Update each SKILL.md with complete integration info

---

## 🎊 PROJECT COMPLETION CEREMONY

### When Phase 5 Complete:

1. **Update PHASE-5-PROJECT-STATUS.md:**
   - Mark all 36 skills as complete
   - Add final statistics
   - Celebrate success! 🎉

2. **Create Final Integration Map:**
   - Visual diagram of skill connections
   - Document in skill-revamp/SKILL-ECOSYSTEM-MAP.md

3. **Generate Summary Report:**
   - Total skills: 36
   - Total tokens used
   - Token savings achieved
   - Time taken (sessions)
   - Key improvements made

4. **Test Suite:**
   - Invoke each skill to verify working
   - Check all cross-references valid
   - Ensure all scripts executable

5. **User Handoff:**
   - Inform user that all 36 skills revamped
   - Provide summary of changes
   - Explain how to use revamped skills

---

## 🚨 END-OF-SESSION REQUIREMENTS (PARALLEL EXECUTION) 🚨

**MANDATORY for every session working on Phase 5:**

### Update Documents

1. **PHASE-5-PROJECT-STATUS.md** - Add session summary with session ID
2. **GLOBAL-SESSION-REQUIREMENTS.md lines 159-182** - Update Phase 5 Progress section
3. Inform user of completion status

**Emphasize:**
- Phase 5 is **HIGHEST PRIORITY** - critical validation/debugging skills
- Has NO dependencies - can execute with ALL other phases in parallel
- When Phase 5 complete, project benefits from validation skills across all phases

---

**END OF PHASE 5 MASTER PLAN**

**This is the FINAL phase!** 🎉

**Remember:** Phase 5 is HIGHEST PRIORITY. These validation/debugging skills should be started ASAP, not saved for last. Can execute in parallel with ALL other phases. Update GLOBAL-SESSION-REQUIREMENTS.md at session end. When all 5 phases complete, entire project is complete!
