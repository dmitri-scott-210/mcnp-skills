# PHASE 2 MASTER PLAN - CATEGORY D SKILLS (6 SKILLS)

**Phase:** 2 of 5
**Skills:** 6 (Category D: Output Analysis & Mesh)
**Estimated Sessions:** 1
**Estimated Tokens:** ~100k tokens
**Created:** 2025-11-02 (Session 2)

---

## 🎯 PHASE OVERVIEW

### Objectives
Revamp 6 output analysis and mesh-focused skills that share documentation about MCNP output formats, mesh tallies, and post-processing tools.

### Why This Phase?
1. **Unified documentation** - All 6 skills need Chapter 8 + Appendix D
2. **Output format expertise** - MCTAL, HDF5, XDMF, particle tracks
3. **Mesh tallies** - FMESH, TMESH, unstructured mesh
4. **Post-processing focus** - Extracting and analyzing simulation results

### Token Optimization Strategy
- **Sequential approach:** 6 skills × 80k tokens = 480k tokens ❌
- **Batched approach:** 40k (docs once) + 60k (6×10k) = 100k tokens ✅
- **Savings:** 380k tokens (79% reduction)

---

## 🚨 PARALLEL EXECUTION SUPPORT 🚨

**This phase supports PARALLEL execution with other phases.**

### Parallel Execution Capabilities

**Phase 2 Status:** ⏸️ NOT STARTED - 0/6 skills complete (0%)

**Can Execute in Parallel with:**
- ✅ Phase 1 (different documentation - Chapters 3-5)
- ✅ Phase 4 (different documentation - Appendix E utilities)
- ✅ Phase 5 (minimal documentation, independent skills)
- ❌ Phase 3 (Phase 3 skills 1-2 require Phase 2 completion)

**Dependencies:**
- **Within Phase 2:** All 6 skills use same documentation - can batch read docs once
- **External Dependencies:** None - Phase 2 is independent of other phases
- **Phase 3 Impact:** Phase 3 skills #1-2 (tally-analyzer, statistics-checker completion) require Phase 2 skills to be done first

### Session ID Tracking

**Every session working on Phase 2 MUST:**

1. **Generate unique session ID:**
   - Format: `Session-YYYYMMDD-HHMMSS-Phase2`
   - Example: `Session-20251106-150000-Phase2`

2. **Record session ID in PHASE-2-PROJECT-STATUS.md:**
   - Add session summary with ID at end of session
   - Include date, skills worked, progress

3. **Update GLOBAL-SESSION-REQUIREMENTS.md:**
   - Update "Phase 2 Progress and Summary" section
   - Record latest session ID
   - Update skill completion status

### Coordination with Global Requirements

**This phase plan works in conjunction with:**
- **GLOBAL-SESSION-REQUIREMENTS.md** - Global project coordination
- **PHASE-2-PROJECT-STATUS.md** - Phase-specific progress tracking
- **TOKEN-OPTIMIZATION-BEST-PRACTICES.md** - Universal optimization techniques

**Session startup reads:**
1. GLOBAL-SESSION-REQUIREMENTS.md (identify Phase 2 status)
2. TOKEN-OPTIMIZATION-BEST-PRACTICES.md
3. THIS FILE (PHASE-2-MASTER-PLAN.md)
4. PHASE-2-PROJECT-STATUS.md
5. LESSONS-LEARNED.md

### Skills and Dependencies

**All 6 skills in Phase 2 are independent of each other:**
1. ⏸️ mcnp-output-parser (can start immediately)
2. ⏸️ mcnp-mctal-processor (can start immediately)
3. ⏸️ mcnp-mesh-builder (can start immediately)
4. ⏸️ mcnp-plotter (can start immediately)
5. ⏸️ mcnp-tally-analyzer (partial - will complete in Phase 3)
6. ⏸️ mcnp-statistics-checker (partial - will complete in Phase 3)

**Parallelization Strategy:**
- All 6 skills can be worked on in parallel by different sessions
- Recommended: Complete in listed order for logical flow
- Single session can complete all 6 skills (~100k tokens)

---

## 🚨 CRITICAL STRUCTURE REQUIREMENTS (ZERO TOLERANCE)

**MANDATORY for ALL Phase 2 skills - NO EXCEPTIONS:**

### Correct Directory Structure
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── output_formats.md                 ← Reference files at ROOT level
├── mctal_format.md                   ← NOT in subdirectories
├── hdf5_structure.md                 ← Same level as SKILL.md
├── [other-reference].md              ← Root skill directory
├── scripts/                          ← Subdirectory for scripts ONLY
│   ├── mcnp_output_reader.py
│   └── README.md
├── templates/                        ← DIRECTLY at root (NOT in assets/)
│   └── [template files]
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    └── [example files]
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
    ├── templates/                    ← Should be at root level
    └── example_inputs/               ← Should be at root level
```

**Reference:** CLAUDE-SESSION-REQUIREMENTS.md lines 495-540, LESSONS-LEARNED.md Lesson #16

---

## 📚 DOCUMENTATION TO READ (ONCE AT PHASE START)

### Required Reading List

Read these documents **ONE TIME** at the beginning of Phase 2:

#### Core Mesh Chapter (1 file)
1. **markdown_docs/user_manual/08_Unstructured_Mesh.md**
   - Purpose: Unstructured mesh geometry, EMBED command, mesh generation
   - Key content: UM geometry input, MESHGEO, EMBED syntax
   - Token estimate: ~12k

#### Appendix A: Mesh Formats (1 file)
2. **markdown_docs/appendices/AppendixA_Mesh_File_Formats.md**
   - Purpose: Mesh file format specifications
   - Key content: ABAQUS, CGAL, GMSH, VTK formats
   - Token estimate: ~5k

#### Appendix D: Output Files (7 files)
Location: `markdown_docs/appendices/`

3. **AppendixD_03_Particle_Track_Output.md**
   - Purpose: PTRAC file format, particle tracking
   - Key content: PTRAC card, binary format, track data
   - Token estimate: ~6k

4. **AppendixD_04_Mesh_Tally_XDMF.md**
   - Purpose: XDMF format for mesh tallies (standard structured mesh)
   - Key content: FMESH XDMF output, ParaView visualization
   - Token estimate: ~5k

5. **AppendixD_05_Fission_Matrix.md**
   - Purpose: Fission matrix file format
   - Key content: FM card output, matrix structure
   - Token estimate: ~4k

6. **AppendixD_06_Unstructured_Mesh_HDF5.md**
   - Purpose: HDF5 format for unstructured mesh
   - Key content: File structure, dataset organization, UM tallies
   - Token estimate: ~7k

7. **AppendixD_07_Unstructured_Mesh_Legacy.md**
   - Purpose: Legacy UM output formats
   - Key content: ASCII output, backward compatibility
   - Token estimate: ~4k

8. **AppendixD_08_HDF5_Script.md**
   - Purpose: Python scripts for HDF5 processing
   - Key content: Example scripts, h5py usage, data extraction
   - Token estimate: ~6k

9. **AppendixD_09_inxc_File_Structure.md**
   - Purpose: INXC file format for cross-section data
   - Key content: File structure, data organization
   - Token estimate: ~4k

#### Appendix E: Post-Processing Tool (1 file)
10. **markdown_docs/appendices/AppendixE_11_UM_Post_Processing.md**
    - Purpose: Unstructured mesh post-processing utilities
    - Key content: Visualization, data extraction, file conversion
    - Token estimate: ~5k

### Total Documentation
- **Files:** 10 documents
- **Estimated tokens:** ~58k tokens (accounting for formatting)
- **Read:** ONCE at phase start
- **Reuse:** For all 6 skills in this phase

### Additional Context from Phase 1
Some skills may reference:
- Chapter 5 (tallies) - already read in Phase 1
- Chapter 10 examples - already read in Phase 1
- Zero additional tokens if cached from Phase 1

---

## 🛠️ SKILLS TO PROCESS (6 TOTAL)

### Processing Order

#### Output File Processing (2 skills)
1. **mcnp-output-parser** (Category D)
   - **Priority:** HIGHEST - Foundation for output analysis
   - **Current:** 1,231 lines
   - **Focus:** Reading OUTP, MCTAL, HDF5, XDMF, PTRAC files
   - **Key capabilities:**
     - Parse standard text output
     - Extract tally results from MCTAL
     - Read HDF5 structured mesh data
     - Process XDMF for visualization
     - Parse particle tracks from PTRAC
   - **References to create:**
     - output_formats.md (comprehensive format specifications)
     - mctal_format.md (MCTAL file structure)
     - hdf5_structure.md (HDF5 dataset organization)
   - **Scripts to bundle:**
     - mcnp_output_reader.py (parse OUTP files)
     - mctal_extractor.py (extract tallies from MCTAL)
     - hdf5_mesh_reader.py (read HDF5 mesh data)
   - **Examples needed:**
     - Basic output files from basic_examples/
     - Mesh tally outputs from unstructured-mesh_examples/

2. **mcnp-mctal-processor** (Category D)
   - **Priority:** High - Specialized MCTAL processing
   - **Current:** ~900 lines (estimate)
   - **Focus:** Advanced MCTAL manipulation (merge, convert, extract)
   - **Key capabilities:**
     - Merge multiple MCTAL files
     - Convert MCTAL to other formats (CSV, JSON)
     - Extract specific tallies
     - Statistical analysis of tally data
   - **References to create:**
     - mctal_operations.md (merge, convert, extract procedures)
     - statistical_methods.md (error propagation, confidence intervals)
   - **Scripts to bundle:**
     - mctal_merge.py
     - mctal_to_csv.py
     - tally_statistics.py
   - **Examples needed:**
     - Multiple MCTAL files for merging examples
     - Various tally types for conversion examples

#### Mesh and Visualization (2 skills)
3. **mcnp-mesh-builder** (Category E, but fits Phase 2 docs)
   - **Priority:** High - Mesh tally creation
   - **Current:** ~850 lines (estimate)
   - **Focus:** FMESH, TMESH, unstructured mesh specification
   - **Key capabilities:**
     - Rectangular/cylindrical/spherical FMESH
     - TMESH for time-dependent results
     - Unstructured mesh with EMBED
     - Mesh refinement strategies
   - **References to create:**
     - mesh_types.md (FMESH vs TMESH vs UM)
     - mesh_generation.md (external tools, MESHGEO)
     - mesh_optimization.md (resolution, cell overlay)
   - **Scripts to bundle:**
     - fmesh_generator.py (create FMESH cards)
     - mesh_converter.py (convert external mesh formats)
   - **Examples needed:**
     - All files from unstructured-mesh_examples/
     - FMESH examples from basic_examples/

4. **mcnp-plotter** (Category D)
   - **Priority:** Medium - Visualization
   - **Current:** ~800 lines (estimate)
   - **Focus:** Geometry plots, tally visualization, mesh rendering
   - **Key capabilities:**
     - Geometry cross-sections
     - 2D/3D tally plots
     - Mesh tally visualization
     - ParaView/VisIt integration
   - **References to create:**
     - plotting_guide.md (mcnp_plot.py, geometry visualization)
     - paraview_workflow.md (XDMF import, filters, rendering)
     - visualization_best_practices.md
   - **Scripts to bundle:**
     - plot_geometry.py
     - plot_mesh_tally.py
     - xdmf_to_vtk.py
   - **Examples needed:**
     - Geometry plot examples
     - Mesh visualization examples from unstructured-mesh_examples/

#### Analysis Skills (2 skills - Partial)
5. **mcnp-tally-analyzer** (Category D, partial - completed in Phase 3)
   - **Priority:** Medium - Basic analysis in Phase 2
   - **Current:** ~950 lines (estimate)
   - **Phase 2 focus:**
     - Tally result interpretation
     - Statistical quality checks (basic)
     - Unit conversions
     - Physical meaning extraction
   - **Phase 3 additions:**
     - Advanced statistical analysis
     - Variance reduction effectiveness
     - Convergence analysis
   - **References to create in Phase 2:**
     - tally_interpretation.md (what tally results mean)
     - units_reference.md (unit conversions)
   - **References to add in Phase 3:**
     - advanced_statistics.md
     - convergence_analysis.md

6. **mcnp-statistics-checker** (Category D, partial - completed in Phase 3)
   - **Priority:** Medium - Basic checks in Phase 2
   - **Current:** ~850 lines (estimate)
   - **Phase 2 focus:**
     - 10 statistical checks overview
     - FOM (Figure of Merit) calculation
     - Basic convergence indicators
   - **Phase 3 additions:**
     - Advanced convergence diagnostics
     - Variance reduction quality metrics
   - **References to create in Phase 2:**
     - ten_statistical_checks.md (comprehensive guide)
     - fom_calculation.md
   - **References to add in Phase 3:**
     - advanced_diagnostics.md
     - vr_effectiveness_metrics.md

---

## 📋 PER-SKILL WORKFLOW (11 STEPS)

### Same as Phase 1

For EACH of the 6 skills, follow the standard 11-step workflow:

1. **Read Current SKILL.md** (2k tokens)
2. **Cross-Reference with Documentation** (0k - already read)
3. **Identify Discrepancies and Gaps** (1k tokens)
4. **Create Skill Revamp Plan** (1k tokens)
5. **Extract Content to Root Skill Directory** (2k tokens) - Reference .md files at ROOT level
6. **Add Example Files to example_inputs/ at ROOT Level** (1k tokens) - DIRECTLY at root, NO assets/
7. **Create/Bundle Scripts** (1k tokens)
8. **Streamline SKILL.md** (3k tokens)
9. **Validate Quality - 26-Item Checklist** (1k tokens)
10. **Test Skill** (minimal tokens)
11. **Update PHASE-2-PROJECT-STATUS.md** (minimal tokens)

**Total per skill:** ~10k tokens

See PHASE-1-MASTER-PLAN.md for detailed step descriptions and CRITICAL structure requirements (NO assets/ subdirectory).

---

## 📊 TOKEN BUDGET BREAKDOWN

### Phase-Level Allocation
- **Documentation reading:** 40k tokens (ONCE at phase start)
- **Skill processing:** 6 skills × 10k = 60k tokens
- **Total Phase 2:** ~100k tokens

### Session Distribution
**Single Session:**
- Read 10 documentation files: 40k tokens
- Process all 6 skills: 60k tokens
- **Total:** ~100k tokens (fits comfortably in one session)

**Phase 2 Total:** ~100k tokens (well within 200k session limit)

---

## 🎯 EXECUTION CHECKLIST

### Before Starting Phase 2
- [ ] Check GLOBAL-SESSION-REQUIREMENTS.md for overall project status
- [ ] Phase 2 has NO dependencies - can start immediately
- [ ] Determine which other phases are in progress
- [ ] PHASE-2-PROJECT-STATUS.md created or updated with Phase 2 start
- [ ] Token budget noted (~40k for docs, 60k for skills)

### Documentation Reading (Do ONCE)
- [ ] Chapter 8: Unstructured Mesh
- [ ] Appendix A: Mesh File Formats
- [ ] Appendix D (7 files): Output file formats
- [ ] Appendix E.11: UM Post-Processing
- [ ] Take comprehensive notes for reference during skill processing
- [ ] Update STATUS with "Documentation Phase Complete"

### Skill Processing (6 iterations)
**For each skill:**
- [ ] Follow 11-step workflow from PHASE-1-MASTER-PLAN.md
- [ ] Extract reference .md files to ROOT level (NOT in subdirectories)
- [ ] Create example_inputs/ and templates/ DIRECTLY at root (NO assets/ parent)
- [ ] Update STATUS continuously
- [ ] Complete 26-item quality checklist (includes NO assets/ check)
- [ ] Test before marking complete

**Skills (in order):**
1. [ ] mcnp-output-parser (highest priority)
2. [ ] mcnp-mctal-processor
3. [ ] mcnp-mesh-builder
4. [ ] mcnp-plotter
5. [ ] mcnp-tally-analyzer (partial)
6. [ ] mcnp-statistics-checker (partial)

### Phase Completion
- [ ] All 6 skills completed and validated
- [ ] Integration with other phases documented
- [ ] PHASE-2-PROJECT-STATUS.md reflects Phase 2 complete
- [ ] Phase 2 complete - other phases may continue in parallel

---

## 🔍 SKILL-SPECIFIC NOTES

### mcnp-output-parser (Skill #1 - CRITICAL)
**Why first:** Foundation for all output analysis
**Key focus areas:**
- Multiple file format support (OUTP, MCTAL, HDF5, XDMF, PTRAC)
- Format detection and selection
- Error handling for malformed files
**Structure requirements:**
- Reference .md files (output_formats.md, mctal_format.md, hdf5_structure.md) at ROOT level
- scripts/ with Python modules (mcnp_output_reader.py, mctal_extractor.py, hdf5_mesh_reader.py)
- example_inputs/ DIRECTLY at root (NO assets/)
- **VERIFY:** NO assets/ or references/ subdirectories exist
**Python scripts essential:**
- This skill MUST have bundled scripts (mentioned but not bundled originally)
- Create comprehensive Python module for output parsing
**Examples priority:**
- unstructured-mesh_examples/ (ALL output files)
- Output files from any basic_examples/ runs

### mcnp-mesh-builder (Skill #3 - HIGH PRIORITY)
**Why important:** Mesh tallies increasingly important for visualization
**Key focus areas:**
- FMESH vs unstructured mesh decision
- External mesh generation (GMSH, ABAQUS, etc.)
- EMBED command for UM
**Structure requirements:**
- Reference .md files (mesh_types.md, mesh_generation.md, mesh_optimization.md) at ROOT level
- scripts/ with fmesh_generator.py and mesh_converter.py
- example_inputs/ DIRECTLY at root with mesh examples (NO assets/)
- **VERIFY:** NO assets/ or references/ subdirectories exist
**References critical:**
- Chapter 8 extraction (UM geometry specification)
- Appendix A (external mesh formats)
**Examples priority:**
- unstructured-mesh_examples/ (HIGHEST PRIORITY)
- Any reactor models with mesh tallies

### mcnp-tally-analyzer & mcnp-statistics-checker (Partial)
**Phase 2 vs Phase 3 split:**
- **Phase 2:** Basic functionality using Phase 2 docs
  - Tally interpretation
  - 10 statistical checks
  - FOM calculation
- **Phase 3:** Advanced functionality using VR docs
  - VR effectiveness analysis
  - Advanced convergence diagnostics
  - Optimization recommendations
**Mark clearly in SKILL.md:** Which features are basic vs advanced

---

## 🚨 PHASE 2 CONTINGENCIES

### If Running Low on Tokens
**Trigger:** < 30k tokens remaining

**Same procedure as Phase 1:**
1. STOP current work
2. Update REVAMP-PROJECT-STATUS.md with maximum detail
3. Mark skill as "in_progress"
4. Create session handoff note
5. Exit gracefully

### If HDF5/XDMF Examples Not Available
**Issue:** unstructured-mesh_examples/ might not have output files, only inputs

**Actions:**
1. Document in STATUS
2. Use example inputs with description of expected output
3. Reference Appendix D specifications
4. Create synthetic example descriptions
5. Note that users would need to run simulations to generate outputs

### If Python Scripts Too Complex
**Issue:** HDF5 parsing scripts might be very complex

**Actions:**
1. Create simplified example scripts
2. Extensive documentation in reference .md files at root level
3. Point to external libraries (h5py, PyTables)
4. Include installation instructions
5. Test scripts with example data if available

---

## ✅ PHASE 2 SUCCESS CRITERIA

### Phase Complete When:
- ✅ All 10 documentation files read and comprehended
- ✅ All 6 skills processed through 11-step workflow
- ✅ Every skill passes 26-item quality checklist (includes NO assets/ check)
- ✅ All skills tested and validated
- ✅ Partial skills (tally-analyzer, statistics-checker) clearly marked
- ✅ Integration with Phase 1 skills documented
- ✅ PHASE-2-PROJECT-STATUS.md reflects accurate completion
- ✅ Token budget within estimates (~100k)
- ✅ Ready to proceed to Phase 3

### Per-Skill Success:
- ✅ SKILL.md streamlined to <5k words (ideally <3k)
- ✅ Reference .md files created at ROOT level (NOT in subdirectories)
- ✅ example_inputs/ populated with relevant examples (DIRECTLY at root, NO assets/)
- ✅ templates/ created at ROOT level (if applicable, NO assets/)
- ✅ scripts/ created (ESSENTIAL for output parsing skills)
- ✅ 26-item checklist passed (includes NO assets/ directory check)
- ✅ Tested with Claude Code
- ✅ STATUS updated with completion entry

---

## 📈 PROGRESS TRACKING

**Monitor in PHASE-2-PROJECT-STATUS.md:**

```markdown
## PHASE 2 PROGRESS

**Status:** [In Progress / Complete]
**Session:** [Current session number]
**Tokens used:** [X]k / 100k budgeted

### Documentation Reading
- [ ] Chapter 8: Unstructured Mesh - [Status]
- [ ] Appendix A: Mesh File Formats - [Status]
- [ ] Appendix D (7 files): Output formats - [Status]
- [ ] Appendix E.11: UM Post-Processing - [Status]
- [ ] Documentation phase complete: [✅/⏸️]

### Skills Completed: X/6 (Y%)

**Output Processing:**
1. [ ] mcnp-output-parser
2. [ ] mcnp-mctal-processor

**Mesh & Visualization:**
3. [ ] mcnp-mesh-builder
4. [ ] mcnp-plotter

**Analysis (Partial):**
5. [ ] mcnp-tally-analyzer (partial - complete in Phase 3)
6. [ ] mcnp-statistics-checker (partial - complete in Phase 3)

**Phase 2 Complete:** [Date/Session]
```

---

## 🔗 INTEGRATION WITH OTHER PHASES

### Phase 1 → Phase 2 Connection
**Phase 1 skills referenced by Phase 2:**
- **tally-builder** → Defines tallies that output-parser extracts
- **mesh-builder** → Creates FMESH that output-parser processes
- **input-builder** → Overall structure impacts output format

**Documentation reuse:**
- Chapter 5 (tallies) - may reference if cached from Phase 1
- Chapter 10 (examples) - may reference if cached from Phase 1

### Phase 2 → Phase 3 Connection
**Skills continued in Phase 3:**
- **mcnp-tally-analyzer:** Basic in Phase 2, advanced in Phase 3
- **mcnp-statistics-checker:** Basic in Phase 2, advanced in Phase 3

**Documentation addition in Phase 3:**
- Variance reduction theory
- Advanced convergence diagnostics
- VR effectiveness metrics

---

## 🚨 END-OF-SESSION REQUIREMENTS (PARALLEL EXECUTION) 🚨

**MANDATORY for every session working on Phase 2:**

### Step 1: Update PHASE-2-PROJECT-STATUS.md

**Add session summary:**
```markdown
### Session [Session-ID] Summary

**Date:** YYYY-MM-DD
**Session ID:** Session-YYYYMMDD-HHMMSS-Phase2
**Phase:** 2
**Duration:** ~Xk tokens used

**Skills Completed This Session:**
1. [skill-name] - [status]

**Phase 2 Overall:** X/6 skills complete (Y% complete)

**Next Session Should:**
[Specific guidance]

**Critical Context:**
[State of work]
```

### Step 2: Update GLOBAL-SESSION-REQUIREMENTS.md

**Update Phase 2 Progress and Summary section:**
- Status, progress fractions
- Latest session ID
- Skill completion status (✅/🚧/⏸️)

### Step 3: Inform User

```
✅ Phase 2 Session Complete

**Session ID:** Session-YYYYMMDD-HHMMSS-Phase2
**Skills Completed:** X/6
**Global Progress:** A/36 total skills

**Phase 2 can execute in parallel with Phases 1, 4, 5**
**Phase 3 skills 1-2 require Phase 2 completion**
```

---

**END OF PHASE 2 MASTER PLAN**

**Remember:** Phase 2 is streamlined (6 skills, 1 session). Focus on output format expertise and Python script bundling. Mark partial skills (tally-analyzer, statistics-checker) clearly for Phase 3 completion. Update GLOBAL-SESSION-REQUIREMENTS.md Phase 2 Progress section at end of session. Phase 2 can execute in parallel with Phases 1, 4, 5. Phase 3 skills 1-2 require Phase 2 completion.
