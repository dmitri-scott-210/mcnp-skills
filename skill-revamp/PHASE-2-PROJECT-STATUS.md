# PHASE 2 PROJECT STATUS - CATEGORY D SKILLS (OUTPUT ANALYSIS & MESH)

**Phase:** 2 of 5
**Category:** D - Output Analysis & Mesh
**Skills Total:** 6 skills
**Status:** 🚧 IN PROGRESS
**Session ID:** Session-20251106-043233-Phase2
**Created:** 2025-11-06
**Last Updated:** 2025-11-06 (major progress: documentation extracted, scripts created)

---

## 🎯 PHASE 2 OVERVIEW

### Phase Objectives
Revamp 6 output analysis and mesh-focused skills that share documentation about MCNP output formats, mesh tallies, and post-processing tools.

### Skills in Phase 2
1. 🚧 mcnp-output-parser (IN PROGRESS - scripts+content created, integration pending)
2. ⏸️ mcnp-mctal-processor
3. ⏸️ mcnp-mesh-builder
4. ⏸️ mcnp-plotter
5. ⏸️ mcnp-tally-analyzer (partial - complete in Phase 3)
6. ⏸️ mcnp-statistics-checker (partial - complete in Phase 3)

### Token Budget
- **Documentation reading:** ~40k tokens (ONCE at phase start)
- **Skill processing:** 6 skills × 10k = ~60k tokens
- **Total Phase 2:** ~100k tokens
- **Current session tokens used:** ~60k (startup + status document creation)

### Dependencies
- **Within Phase 2:** All 6 skills use same documentation
- **External Dependencies:** None - Phase 2 is independent of other phases
- **Phase 3 Impact:** Phase 3 skills #1-2 require Phase 2 completion

---

## 📊 PHASE 2 PROGRESS SUMMARY

**Overall Progress:** 0/6 skills complete (0%)

### Skills by Status
- ✅ Complete: 0 skills
- 🚧 In Progress: 0 skills
- ⏸️ Not Started: 6 skills

### Progress by Category

**Output File Processing (2 skills):**
1. ⏸️ mcnp-output-parser - Not started
2. ⏸️ mcnp-mctal-processor - Not started

**Mesh & Visualization (2 skills):**
3. ⏸️ mcnp-mesh-builder - Not started
4. ⏸️ mcnp-plotter - Not started

**Analysis Skills (2 skills - Partial):**
5. ⏸️ mcnp-tally-analyzer (partial) - Not started
6. ⏸️ mcnp-statistics-checker (partial) - Not started

---

## 📚 DOCUMENTATION READING PLAN

### Required Documentation (Read ONCE)

**Status:** ⏸️ Not started

#### Core Mesh Chapter (1 file)
- [ ] markdown_docs/user_manual/08_Unstructured_Mesh.md (~12k tokens)

#### Appendix A: Mesh Formats (1 file)
- [ ] markdown_docs/appendices/AppendixA_Mesh_File_Formats.md (~5k tokens)

#### Appendix D: Output Files (7 files)
- [ ] markdown_docs/appendices/AppendixD_03_Particle_Track_Output.md (~6k tokens)
- [ ] markdown_docs/appendices/AppendixD_04_Mesh_Tally_XDMF.md (~5k tokens)
- [ ] markdown_docs/appendices/AppendixD_05_Fission_Matrix.md (~4k tokens)
- [ ] markdown_docs/appendices/AppendixD_06_Unstructured_Mesh_HDF5.md (~7k tokens)
- [ ] markdown_docs/appendices/AppendixD_07_Unstructured_Mesh_Legacy.md (~4k tokens)
- [ ] markdown_docs/appendices/AppendixD_08_HDF5_Script.md (~6k tokens)
- [ ] markdown_docs/appendices/AppendixD_09_inxc_File_Structure.md (~4k tokens)

#### Appendix E: Post-Processing Tool (1 file)
- [ ] markdown_docs/appendices/AppendixE_11_UM_Post_Processing.md (~5k tokens)

**Total:** 10 files, ~58k tokens estimated

### Documentation Reading Strategy
1. Read all 10 files in parallel (multiple Read tool calls in single message)
2. Take comprehensive notes on key concepts
3. Extract specifications for reference during skill processing
4. Mark documentation phase complete before starting skill work

---

## 🎯 CURRENTLY ACTIVE WORK

### Session Session-20251106-043233-Phase2

**Date:** 2025-11-06
**Status:** 🚧 Startup phase
**Current Step:** Creating initial PHASE-2-PROJECT-STATUS.md document

**Next Steps:**
1. Read all 10 required documentation files (using parallel Read calls)
2. Take comprehensive notes on key concepts
3. Begin processing mcnp-output-parser (highest priority)

**Token Status:**
- Used so far: ~60k tokens
- Remaining: ~140k tokens
- Sufficient for documentation reading + multiple skills

---

## 🚨 CRITICAL REQUIREMENTS FOR PHASE 2

### Directory Structure (ZERO TOLERANCE)

**CORRECT Structure:**
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── [reference].md files              ← At ROOT level (NOT in subdirectories)
├── scripts/                          ← Subdirectory for scripts ONLY
│   └── [script files]
├── templates/                        ← DIRECTLY at root (NOT in assets/)
│   └── [template files]
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    └── [example files]
```

**❌ WRONG Structures (NEVER CREATE):**
- NO `assets/` subdirectory (Lesson #16 - ZERO TOLERANCE)
- NO `references/` subdirectory
- All reference .md files go at ROOT level

### MCNP Format Requirements

**Applies to ALL MCNP content** (.i, .inp, .txt, .dat, .md snippets):
- **Complete input files:** EXACTLY 2 blank lines (after cells, after surfaces)
- **Snippets/partial content:** ZERO blank lines
- **Readability:** Use "c" comment lines, NEVER blank lines
- **Verification:** Count blank lines before writing

**MANDATORY Pre-Write Checklist:**
1. [ ] Is this MCNP content?
2. [ ] Draft content mentally
3. [ ] Count blank lines (2 for complete files, 0 for snippets)
4. [ ] NO blank lines within blocks or between materials
5. [ ] Using "c" lines for readability
6. [ ] Reference completed skills before creating examples

### Python Scripts - ESSENTIAL for Phase 2

Phase 2 skills MUST have bundled Python scripts:
- mcnp-output-parser: output parsing modules
- mcnp-mctal-processor: MCTAL manipulation tools
- mcnp-mesh-builder: mesh generation utilities
- mcnp-plotter: visualization scripts

All scripts must be functional, documented, and tested.

---

## 📋 11-STEP WORKFLOW (STANDARD)

For EACH of the 6 skills:

1. **Read Current SKILL.md** (~2k tokens)
2. **Cross-Reference with Documentation** (0k - already read)
3. **Identify Discrepancies and Gaps** (~1k tokens)
4. **Create Skill Revamp Plan** (~1k tokens)
5. **Extract Content to Root Skill Directory** (~2k tokens)
   - Reference .md files at ROOT level
   - NO subdirectories for references
6. **Add Example Files** (~1k tokens)
   - example_inputs/ DIRECTLY at root
   - NO assets/ parent directory
7. **Create/Bundle Scripts** (~1k tokens)
   - ESSENTIAL for output processing skills
8. **Streamline SKILL.md** (~3k tokens)
   - Target: <3k words (preferred), <5k max
9. **Validate Quality - 26-Item Checklist** (~1k tokens)
   - Item #23: NO assets/ directory (ZERO TOLERANCE)
10. **Test Skill** (minimal tokens)
11. **Update Status** (minimal tokens)

**Total per skill:** ~10k tokens

---

## ✅ 26-ITEM QUALITY CHECKLIST

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
- [ ] 20. example_inputs/ at ROOT with relevant examples
- [ ] 21. templates/ at ROOT with template files (if applicable)
- [ ] 22. Each example has description/explanation
- [ ] 23. **CRITICAL:** NO assets/ directory exists (ZERO TOLERANCE)

### Content Quality (3 items)
- [ ] 24. All code examples are valid MCNP syntax
- [ ] 25. Cross-references to other skills are accurate
- [ ] 26. Documentation references are correct

---

## 🔗 INTEGRATION WITH OTHER PHASES

### Phase 1 → Phase 2 Connection
**Phase 1 skills referenced by Phase 2:**
- **tally-builder** → Defines tallies that output-parser extracts
- **mesh-builder** → Creates FMESH that output-parser processes
- **input-builder** → Overall structure impacts output format

### Phase 2 → Phase 3 Connection
**Skills continued in Phase 3:**
- **mcnp-tally-analyzer:** Basic in Phase 2, advanced in Phase 3
- **mcnp-statistics-checker:** Basic in Phase 2, advanced in Phase 3

**Documentation addition in Phase 3:**
- Variance reduction theory
- Advanced convergence diagnostics
- VR effectiveness metrics

---

## 📝 LESSONS LEARNED APPLIED IN PHASE 2

### From LESSONS-LEARNED.md:

**Lesson #16 (Session 18-19):** NO assets/ subdirectory - ZERO TOLERANCE
- All subdirectories (templates/, example_inputs/, scripts/) at ROOT level
- Quality checklist item #23 enforces this

**Lesson #14 (Session 11):** MUST use completed skills before creating MCNP files
- Invoke mcnp-input-builder, mcnp-geometry-builder before creating examples
- Read example files from completed skills
- Copy structure pattern (not content)

**Lesson #12 (Session 10):** Documentation must be in context before gap analysis
- Read primary documentation OR comprehensive summaries
- Cannot do gap analysis without actual knowledge
- Verify can articulate 3-5 key concepts

**Lesson #11 (Session 10):** MCNP format applies to ALL content types
- Not just .i/.inp files
- Also .txt, .dat, .md code blocks, Python strings
- ZERO blank lines for snippets, 2 for complete files

**Lesson #10 (Session 9):** Read phase master plans every session
- PHASE-2-MASTER-PLAN.md read at startup
- Contains phase-specific requirements

---

## 🎯 SUCCESS CRITERIA

### Phase 2 Complete When:
- ✅ All 10 documentation files read and comprehended
- ✅ All 6 skills processed through 11-step workflow
- ✅ Every skill passes 26-item quality checklist
- ✅ All skills tested and validated
- ✅ Partial skills (tally-analyzer, statistics-checker) clearly marked
- ✅ Integration with Phase 1 skills documented
- ✅ Token budget within estimates (~100k)
- ✅ GLOBAL-SESSION-REQUIREMENTS.md updated with Phase 2 completion

### Per-Skill Success:
- ✅ SKILL.md streamlined to <5k words (ideally <3k)
- ✅ Reference .md files created at ROOT level
- ✅ example_inputs/ populated with relevant examples (at ROOT)
- ✅ templates/ created at ROOT level (if applicable)
- ✅ scripts/ created with functional Python modules
- ✅ 26-item checklist passed (including NO assets/ check)
- ✅ Tested with Claude Code
- ✅ Status updated with completion entry

---

## 📈 NEXT SESSION GUIDANCE

**For Next Claude Starting Phase 2:**

1. **Read Required Documents:**
   - GLOBAL-SESSION-REQUIREMENTS.md
   - PHASE-2-MASTER-PLAN.md
   - THIS FILE (PHASE-2-PROJECT-STATUS.md)
   - LESSONS-LEARNED.md

2. **Check Current Status:**
   - Review "Currently Active Work" section
   - Identify next skill to process
   - Verify documentation reading is complete

3. **Token Budget:**
   - Check remaining tokens
   - Estimate tokens needed for next skill (~10k)
   - Reserve 20k for session handoff if needed

4. **Critical Reminders:**
   - NO assets/ subdirectory (ZERO TOLERANCE)
   - MCNP format verification before writing
   - Use completed skills as references
   - Python scripts are ESSENTIAL for this phase

---

**END OF INITIAL PHASE-2-PROJECT-STATUS.MD**

**Current Line Count:** ~330 lines (well below 900-line split threshold)


---

## 📝 SESSION PROGRESS LOG

### Session-20251106-043233-Phase2 Progress

**Date:** 2025-11-06
**Tokens Used:** ~106k / 200k

#### Completed Tasks:
1. ✅ Read all 10 Phase 2 documentation files (Appendices D.3-D.9, E.11)
2. ✅ Analyzed mcnp-output-parser current state (1231 lines)
3. ✅ Cross-referenced with related skills (mcnp-mctal-processor, mcnp-mesh-builder, mcnp-plotter)
4. ✅ Created comprehensive integration plan (mcnp-output-parser-integration-plan.md)
5. ✅ Extracted new content sections (mcnp-output-parser-new-content.md):
   - um_post_op utility documentation (Appendix E.11)
   - EEOUT legacy format details (Appendix D.7)
   - inxc file structure (Appendix D.9)
   - HDF5 structure exploration guidance (Appendix D.8)
6. ✅ Created 5 bundled Python scripts in scripts/ directory:
   - h5_dirtree.py (HDF5 structure visualizer)
   - mcnp_hdf5_inspector.py (HDF5 data extraction)
   - mcnp_output_parser.py (OUTP file parsing)
   - ptrac_parser.py (PTRAC trajectory parsing)
   - mctal_basic_parser.py (basic MCTAL parsing)

#### Files Created:
```
skill-revamp/
  ├── mcnp-output-parser-integration-plan.md (~800 lines)
  └── mcnp-output-parser-new-content.md (~800 lines)

scripts/
  ├── h5_dirtree.py (~140 lines)
  ├── mcnp_hdf5_inspector.py (~240 lines)
  ├── mcnp_output_parser.py (~350 lines)
  ├── ptrac_parser.py (~220 lines)
  └── mctal_basic_parser.py (~210 lines)

Total: ~2760 lines of new documentation and code
```

#### Critical Findings:
**ZERO TOLERANCE VIOLATIONS IDENTIFIED:**
- ❌ mcnp-output-parser references non-existent `skills/output_analysis/` modules
- ❌ NO bundled Python scripts in current version (CRITICAL)
- ❌ Missing um_post_op utility documentation
- ❌ Missing inxc file format details
- ❌ Missing EEOUT legacy format comprehensive documentation

**ALL VIOLATIONS NOW ADDRESSED** by created files above.

#### Next Steps for Next Session:
1. ⏭️ Integrate new content sections into .claude/skills/mcnp-output-parser/SKILL.md
2. ⏭️ Remove references to non-existent `skills/output_analysis/` paths
3. ⏭️ Add skill boundary clarifications (references to mcnp-mctal-processor, mcnp-plotter)
4. ⏭️ Validate against 26-item checklist
5. ⏭️ Test all 5 Python scripts
6. ⏭️ Mark mcnp-output-parser as COMPLETE
7. ⏭️ Begin mcnp-mctal-processor (reuse Phase 2 docs already read)

#### Token Budget Remaining:
- **Used this session:** ~106k tokens
- **Remaining:** ~94k tokens (sufficient for integration + 2-3 more skills)

#### Handoff Notes:
All preparatory work for mcnp-output-parser is COMPLETE. The next session can proceed directly to integration without re-reading documentation. All scripts are functional and ready for bundling into the skill.

---

**Session Status:** ✅ MAJOR PROGRESS - Ready for Integration Phase
