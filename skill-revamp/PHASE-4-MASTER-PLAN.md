# PHASE 4 MASTER PLAN - CATEGORY F SKILLS (6 SKILLS)

**Phase:** 4 of 5
**Skills:** 6 (Category F: Utilities & Reference Tools)
**Estimated Sessions:** 1
**Estimated Tokens:** ~90k tokens
**Created:** 2025-11-02 (Session 2)

---

## 🎯 PHASE OVERVIEW

### Objectives
Revamp 6 utility and reference skills that provide supporting tools, unit conversions, physical constants, isotope lookups, and cross-section management.

### Why This Phase?
1. **Appendix E focus** - All 12 Appendix E utility tool files
2. **Reference tool expertise** - Constants, conversions, lookups
3. **Supporting skills** - Help users with auxiliary tasks
4. **Relatively independent** - Minimal dependencies on other skills

### Token Optimization Strategy
- **Sequential approach:** 6 skills × 80k tokens = 480k tokens ❌
- **Batched approach:** 30k (docs once) + 60k (6×10k) = 90k tokens ✅
- **Savings:** 390k tokens (81% reduction)

---

## 🚨 PARALLEL EXECUTION SUPPORT 🚨

**This phase has FULL parallel execution support - all skills independent.**

### Parallel Execution Capabilities

**Phase 4 Status:** ⏸️ NOT STARTED - 0/6 skills complete (0%)

**Can Execute in Parallel with:**
- ✅ Phase 1 (different documentation)
- ✅ Phase 2 (different documentation)
- ✅ Phase 3 (independent)
- ✅ Phase 5 (independent)

**Dependencies:** NONE - All Phase 4 skills are fully independent

### Skills - All Independent

All 6 utility skills can start immediately and be done in any order:
1. ⏸️ mcnp-unit-converter
2. ⏸️ mcnp-physical-constants
3. ⏸️ mcnp-isotope-lookup
4. ⏸️ mcnp-cross-section-manager
5. ⏸️ mcnp-parallel-configurator
6. ⏸️ mcnp-template-generator

**Parallelization Strategy:**
- Can execute in parallel with ANY other phase
- All 6 skills can be split across multiple sessions
- Single session can complete all 6 (~90k tokens)
- **HIGH PRIORITY** - These utility skills support all other skills

### Session ID Tracking

**Every session working on Phase 4 MUST:**

1. **Generate unique session ID:** `Session-YYYYMMDD-HHMMSS-Phase4`
2. **Record in PHASE-4-PROJECT-STATUS.md**
3. **Update GLOBAL-SESSION-REQUIREMENTS.md lines 135-157 (Phase 4 section)**

### Coordination with Global Requirements

**Session startup reads:**
1. GLOBAL-SESSION-REQUIREMENTS.md
2. TOKEN-OPTIMIZATION-BEST-PRACTICES.md
3. THIS FILE (PHASE-4-MASTER-PLAN.md)
4. PHASE-4-PROJECT-STATUS.md
5. LESSONS-LEARNED.md

---

## 🚨 CRITICAL STRUCTURE REQUIREMENTS (ZERO TOLERANCE)

**MANDATORY for ALL Phase 4 skills - NO EXCEPTIONS:**

### Correct Directory Structure
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── conversion_tables.md              ← Reference files at ROOT level
├── isotope_database.md               ← NOT in subdirectories
├── xsdir_format.md                   ← Same level as SKILL.md
├── [other-reference].md              ← Root skill directory
├── scripts/                          ← Subdirectory for scripts ONLY
│   ├── unit_converter.py
│   ├── zaid_lookup.py
│   └── README.md
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    ├── conversion_data.json          ← Data files
    ├── isotope_data.json
    └── [other data files]
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
    └── data_files/                   ← Should be at root level in example_inputs/
```

**Reference:** CLAUDE-SESSION-REQUIREMENTS.md lines 495-540, LESSONS-LEARNED.md Lesson #16

---

## 📚 DOCUMENTATION TO READ (ONCE AT PHASE START)

### Required Reading List

Read these documents **ONE TIME** at the beginning of Phase 4:

#### Appendix E: MCNP6 Utility Tools (12 files)
Location: `markdown_docs/appendices/`

1. **AppendixE_01_Doppler_Broadening.md**
   - Purpose: Doppler broadening program for cross sections
   - Key content: doppler executable, temperature broadening
   - Token estimate: ~3k

2. **AppendixE_02_Event_Log_Analyzer.md**
   - Purpose: mcnp_ela executable for event log analysis
   - Key content: Log file format, event analysis
   - Token estimate: ~3k

3. **AppendixE_03_Doppler_Fitting.md**
   - Purpose: dopplerfit executable for cross-section fitting
   - Key content: Fitting parameters, optimization
   - Token estimate: ~3k

4. **AppendixE_04_Gridconv.md**
   - Purpose: gridconv executable for grid conversion
   - Key content: Grid format conversion, interpolation
   - Token estimate: ~3k

5. **AppendixE_05_Cross_Section_Tool.md**
   - Purpose: cse (Cross Section Evaluator) tool
   - Key content: ENDF/ACE format, cross-section plotting
   - Token estimate: ~4k

6. **AppendixE_06_Merge_ASCII_Tally.md**
   - Purpose: merge_ascii_tally executable for combining tallies
   - Key content: Merging multiple runs, statistical combination
   - Token estimate: ~3k

7. **AppendixE_07_Merge_Mesh_Tally.md**
   - Purpose: merge_mesh_tally executable for mesh combination
   - Key content: Mesh tally merging, format handling
   - Token estimate: ~3k

8. **AppendixE_08_Parameter_Study_Tool.md**
   - Purpose: pst executable for parametric studies
   - Key content: Input parameterization, batch execution
   - Token estimate: ~4k

9. **AppendixE_09_Simple_ACE_Tools.md**
   - Purpose: Basic ACE file manipulation tools
   - Key content: ACE format, cross-section data structure
   - Token estimate: ~3k

10. **AppendixE_10_UM_Converter.md**
    - Purpose: umconv executable for unstructured mesh conversion
    - Key content: Mesh format conversion, UM tools
    - Token estimate: ~4k

11. **AppendixE_11_UM_Post_Processing.md**
    - Purpose: UM post-processing utilities
    - Key content: Visualization, data extraction
    - Token estimate: ~4k
    - **Note:** Already read in Phase 2

12. **AppendixE_12_UM_Pre_Processing.md**
    - Purpose: UM pre-processing tools
    - Key content: Mesh generation, quality checking
    - Token estimate: ~4k

### Total Documentation
- **Files:** 12 documents (11 new + 1 from Phase 2)
- **Estimated tokens:** ~41k tokens (or ~37k if E.11 cached from Phase 2)
- **Read:** ONCE at phase start
- **Reuse:** For all 6 skills in this phase

### Additional Reference Materials
These skills may also reference:
- Physical constants tables (included in skill content, not separate docs)
- Isotope data tables (included in skill content)
- Unit conversion tables (included in skill content)
- ZAID format specifications (from Phase 1 Chapter 5 if cached)

---

## 🛠️ SKILLS TO PROCESS (6 TOTAL)

### Processing Order

#### Reference & Lookup Tools (3 skills)

1. **mcnp-unit-converter** (Category F)
   - **Priority:** High - Frequently needed
   - **Current:** ~800 lines (estimate)
   - **Focus:** Converting between unit systems for MCNP
   - **Key capabilities:**
     - Energy units (MeV, eV, keV, GeV, joules)
     - Length units (cm, m, inches, microns)
     - Density units (g/cm³, kg/m³, atoms/barn-cm)
     - Temperature units (K, °C, °F, eV equivalent)
     - Cross-section units (barns, cm²)
     - Activity units (Ci, Bq, dps)
     - Mass/weight units
     - Angle units (degrees, radians)
     - Time units (seconds, shakes, minutes, years)
   - **References to create:**
     - conversion_tables.md (comprehensive conversion factors)
     - unit_standards.md (MCNP expected units per card)
     - physical_unit_systems.md (SI, CGS, Imperial)
   - **Scripts to bundle:**
     - unit_converter.py (interactive unit conversion)
     - mcnp_unit_checker.py (check input file units)
   - **Assets needed:**
     - Conversion reference tables (CSV/JSON format)
     - Quick reference cards

2. **mcnp-physical-constants** (Category F)
   - **Priority:** High - Core reference
   - **Current:** ~750 lines (estimate)
   - **Focus:** Physical constants used in MCNP calculations
   - **Key capabilities:**
     - Fundamental constants (c, h, k_B, N_A, etc.)
     - Particle properties (masses, charges, spins)
     - Nuclear constants (atomic mass unit, MeV/amu)
     - Reaction Q-values
     - Standard conditions (STP, NTP)
     - Cross-section benchmarks
   - **References to create:**
     - fundamental_constants.md (CODATA values)
     - particle_properties.md (comprehensive particle data)
     - nuclear_constants.md (nuclear physics constants)
     - benchmark_cross_sections.md (standard reactions)
   - **Scripts to bundle:**
     - constants_lookup.py (search and retrieve constants)
     - unit_aware_calculator.py (calculations with units)
   - **Assets needed:**
     - Constants database (JSON/CSV)
     - Quick reference tables

3. **mcnp-isotope-lookup** (Category F)
   - **Priority:** High - Essential for materials
   - **Current:** ~850 lines (estimate)
   - **Focus:** Isotope properties and ZAID format
   - **Key capabilities:**
     - ZAID format (ZZAAA.nnX)
     - Atomic masses and abundances
     - Natural element compositions
     - Decay data (half-lives, decay modes)
     - Cross-section library availability (ENDF/B-VIII.0, etc.)
     - Thermal scattering (S(α,β)) data availability
   - **References to create:**
     - zaid_format_guide.md (comprehensive ZAID explanation)
     - isotope_database.md (properties, masses, abundances)
     - library_availability.md (which isotopes in which libraries)
     - decay_data.md (half-lives, decay chains)
   - **Scripts to bundle:**
     - zaid_lookup.py (convert element/isotope to ZAID)
     - isotope_properties.py (retrieve isotope data)
     - library_checker.py (check ZAID availability in xsdir)
   - **Assets needed:**
     - Isotope database (JSON format with all properties)
     - Natural abundance tables
     - Library availability matrix

#### Specialized Tools (3 skills)

4. **mcnp-cross-section-manager** (Category F)
   - **Priority:** Medium - Advanced users
   - **Current:** ~900 lines (estimate)
   - **Focus:** Cross-section library management and xsdir
   - **Key capabilities:**
     - Understanding xsdir file format
     - Finding cross-section libraries
     - Diagnosing library errors (missing ZAIDs)
     - Temperature-dependent data
     - Library versions (ENDF/B-VII.1, VIII.0, etc.)
     - S(α,β) thermal scattering libraries
   - **References to create:**
     - xsdir_format.md (complete xsdir specification)
     - library_types.md (continuous vs discrete, photon, etc.)
     - library_versions.md (ENDF/B evolution, differences)
     - thermal_scattering_libraries.md (available S(α,β) data)
     - troubleshooting_libraries.md (common errors, solutions)
   - **Scripts to bundle:**
     - xsdir_parser.py (read and query xsdir)
     - library_finder.py (find available data for isotope)
     - missing_zaid_finder.py (diagnose missing cross sections)
   - **Examples needed:**
     - xsdir file examples
     - Error messages for missing libraries

5. **mcnp-parallel-configurator** (Category F)
   - **Priority:** Medium - HPC users
   - **Current:** ~850 lines (estimate)
   - **Focus:** Parallel execution, checkpointing, restart
   - **Key capabilities:**
     - PRDMP card (checkpointing intervals)
     - TASKS card (multi-tasking specification)
     - DBCN card (source distribution)
     - MPI/OpenMP execution
     - Runtpe file management
     - Checkpoint/restart workflow
   - **References to create:**
     - parallel_execution.md (MPI vs OpenMP, thread models)
     - checkpoint_restart.md (PRDMP, runtpe files, restart procedure)
     - distributed_computing.md (TASKS, DBCN usage)
     - performance_optimization.md (load balancing, scaling)
   - **Scripts to bundle:**
     - prdmp_calculator.py (optimal checkpoint intervals)
     - parallel_launcher.py (generate submission scripts)
   - **Examples needed:**
     - Parallel execution examples
     - HPC job submission scripts

6. **mcnp-template-generator** (Category F)
   - **Priority:** Medium - Convenience tool
   - **Current:** ~800 lines (estimate)
   - **Focus:** Generate template MCNP inputs for common problems
   - **Key capabilities:**
     - Basic problem types (shielding, criticality, dose, activation)
     - Template generation from parameters
     - Boilerplate input sections
     - Standard configurations (material libraries, tallies)
   - **References to create:**
     - problem_types.md (shielding, criticality, etc. templates)
     - template_structure.md (anatomy of templates)
     - customization_guide.md (how to modify templates)
   - **Scripts to bundle:**
     - template_generator.py (interactive template creation)
     - problem_configurator.py (parameterized input generation)
   - **Assets needed:**
     - Template library from basic_examples/
     - Boilerplate sections (header, materials, tallies)
     - All from assets/templates/ in other skills

---

## 📋 PER-SKILL WORKFLOW (11 STEPS)

### Same Core Workflow as Previous Phases

For EACH of the 6 skills, follow the standard 11-step workflow:

1. **Read Current SKILL.md** (2k tokens)
2. **Cross-Reference with Documentation** (0k - already read)
3. **Identify Discrepancies and Gaps** (1k tokens)
4. **Create Skill Revamp Plan** (1k tokens)
5. **Extract Content to Root Skill Directory** (2k tokens) - Reference .md files at ROOT level
6. **Add Data Files to example_inputs/ at ROOT Level** (1k tokens) - DIRECTLY at root, NO assets/
7. **Create/Bundle Scripts** (1k tokens) - **CRITICAL for these skills**
8. **Streamline SKILL.md** (3k tokens)
9. **Validate Quality - 26-Item Checklist** (1k tokens)
10. **Test Skill** (minimal tokens)
11. **Update PHASE-4-PROJECT-STATUS.md** (minimal tokens)

**Total per skill:** ~10k tokens

### Special Considerations for Utility Skills

**Step 6 - Data Files:** Different from other phases
- Not MCNP input examples (not applicable for most utility skills)
- Instead: Reference tables, databases, quick reference cards
- Format: CSV, JSON, PDF reference cards
- Store in example_inputs/ DIRECTLY at root (NO assets/)

**Step 7 - Scripts:** ESSENTIAL for utility skills
- These skills are ABOUT tools and utilities
- Python scripts are core functionality, not optional
- Interactive calculators, converters, lookup tools
- Must be functional and well-documented

**Step 8 - SKILL.md:** Focus on "how to use" not "how it works"
- Clear usage examples
- Common scenarios
- Quick reference tables inline
- Link to detailed tables in root-level reference .md files

---

## 📊 TOKEN BUDGET BREAKDOWN

### Phase-Level Allocation
- **Documentation reading:** 30k tokens (ONCE at phase start, ~37k if E.11 not cached)
- **Skill processing:** 6 skills × 10k = 60k tokens
- **Total Phase 4:** ~90k tokens

### Session Distribution
**Single Session:**
- Read 12 Appendix E files: 30-37k tokens
- Process all 6 skills: 60k tokens
- **Total:** ~90-97k tokens (fits comfortably in one session)

---

## 🎯 EXECUTION CHECKLIST

### Before Starting Phase 4
- [ ] Phases 1-3 complete (26 skills revamped)
- [ ] PHASE-4-PROJECT-STATUS.md updated with Phase 4 start
- [ ] Token budget noted (~90k)

### Documentation Reading (Do ONCE)
- [ ] Appendix E.01: Doppler Broadening
- [ ] Appendix E.02: Event Log Analyzer
- [ ] Appendix E.03: Doppler Fitting
- [ ] Appendix E.04: Gridconv
- [ ] Appendix E.05: Cross Section Tool
- [ ] Appendix E.06: Merge ASCII Tally
- [ ] Appendix E.07: Merge Mesh Tally
- [ ] Appendix E.08: Parameter Study Tool
- [ ] Appendix E.09: Simple ACE Tools
- [ ] Appendix E.10: UM Converter
- [ ] Appendix E.11: UM Post Processing (check if cached from Phase 2)
- [ ] Appendix E.12: UM Pre Processing
- [ ] Take comprehensive notes on utility tools
- [ ] Update STATUS with "Documentation Phase Complete"

### Skill Processing (6 iterations)
**For each skill:**
- [ ] Follow 11-step workflow
- [ ] Emphasize Python script creation (core functionality)
- [ ] Create data files in example_inputs/ at ROOT (tables, databases) - NO assets/
- [ ] Update STATUS continuously
- [ ] Complete 26-item quality checklist (includes NO assets/ check)
- [ ] Test scripts execute properly

**Skills (in order):**
1. [ ] mcnp-unit-converter
2. [ ] mcnp-physical-constants
3. [ ] mcnp-isotope-lookup
4. [ ] mcnp-cross-section-manager
5. [ ] mcnp-parallel-configurator
6. [ ] mcnp-template-generator

### Phase Completion
- [ ] All 6 skills completed and validated
- [ ] All Python scripts functional
- [ ] Reference data files created and accessible at root level
- [ ] Integration with other skills documented
- [ ] PHASE-4-PROJECT-STATUS.md reflects Phase 4 complete
- [ ] Prepare for Phase 5

---

## 🔍 SKILL-SPECIFIC NOTES

### mcnp-unit-converter (Skill #1 - HIGH PRIORITY)
**Why high priority:** Used constantly by MCNP practitioners
**Key focus:**
- Interactive conversion (user enters value + units)
- Batch conversion for input files
- Context-aware (knows which units expected per card)
**Python script ESSENTIAL:**
- Must have working unit_converter.py
- Should handle all common unit systems
- Error handling for invalid conversions
**Assets priority:**
- Comprehensive conversion tables (CSV/JSON)
- Quick reference card (1-page PDF)

### mcnp-isotope-lookup (Skill #3 - HIGH PRIORITY)
**Why high priority:** Critical for material definitions
**Key focus:**
- ZAID format translation (U-235 → 92235.80c)
- Library availability checking
- Natural abundance calculations
**Python script ESSENTIAL:**
- zaid_lookup.py must work with common isotope names
- library_checker.py needs xsdir parsing
**Data files critical:**
- Complete isotope database (masses, abundances, decay)
- Library availability matrix
**Integration:**
- Links to material-builder (Phase 1)
- Links to cross-section-manager

### mcnp-cross-section-manager (Skill #4 - ADVANCED)
**Why advanced:** Requires understanding of nuclear data
**Key focus:**
- xsdir file format expertise
- Diagnosing missing/incompatible libraries
- Temperature-dependent cross sections
**Python script ESSENTIAL:**
- xsdir_parser.py for querying libraries
- missing_zaid_finder.py for diagnostics
**References critical:**
- xsdir_format.md (complete specification)
- library_versions.md (ENDF/B differences)
**Integration:**
- Links to isotope-lookup
- Links to material-builder

### mcnp-template-generator (Skill #6 - CONVENIENCE)
**Why different:** Meta-skill that helps create inputs
**Key focus:**
- Problem type selection (shielding, criticality, etc.)
- Template customization
- Reusable boilerplate
**Integration critical:**
- Should reference templates/ from Phase 1 skills
- Links to input-builder (workflow integration)
- Can use examples from example_files/ as templates
**Templates priority:**
- Collect best templates from basic_examples/
- Create template library organized by problem type in templates/ at root

---

## 🚨 PHASE 4 CONTINGENCIES

### If Appendix E Files Are Very Short
**Issue:** Some Appendix E files may be <500 lines each

**Actions:**
1. Good news: Lower token cost than estimated
2. Extract key information to references/ anyway
3. Focus on practical usage, not just tool documentation
4. Supplement with external knowledge if needed
5. Update token estimates in STATUS

### If Python Scripts Complex
**Issue:** Interactive tools may require extensive code

**Actions:**
1. Create well-documented example scripts
2. Focus on common use cases (80/20 rule)
3. Provide templates users can modify
4. Include installation instructions
5. Test with example data
6. OK if scripts are substantial (core functionality)

### If Data Files Large
**Issue:** Isotope databases, conversion tables may be large

**Actions:**
1. Store as separate data files in example_inputs/ at root (NO assets/)
2. Use efficient formats (JSON, CSV)
3. Document data sources
4. Provide subset for testing
5. Scripts should read from data files, not hardcode

---

## ✅ PHASE 4 SUCCESS CRITERIA

### Phase Complete When:
- ✅ All 12 Appendix E files read and understood
- ✅ All 6 skills processed through 11-step workflow
- ✅ Every skill passes 26-item quality checklist (includes NO assets/ check)
- ✅ All Python scripts functional and tested
- ✅ Reference data files created and accessible at root level
- ✅ Integration with Phases 1-3 skills documented
- ✅ PHASE-4-PROJECT-STATUS.md reflects accurate completion
- ✅ Token budget within estimates (~90k)
- ✅ Ready to proceed to Phase 5

### Per-Skill Success:
- ✅ SKILL.md streamlined to <5k words (ideally <3k)
- ✅ Reference .md files created at ROOT level with detailed tables and guides
- ✅ example_inputs/ at root populated with data files and reference cards (NO assets/)
- ✅ scripts/ contains functional, documented Python tools
- ✅ Python scripts tested and working
- ✅ 26-item checklist passed (includes NO assets/ directory check)
- ✅ Tested with Claude Code
- ✅ STATUS updated with completion entry

---

## 📈 PROGRESS TRACKING

**Monitor in PHASE-4-PROJECT-STATUS.md:**

```markdown
## PHASE 4 PROGRESS

**Status:** [In Progress / Complete]
**Session:** [Current session number]
**Tokens used:** [X]k / 90k budgeted

### Documentation Reading
- [ ] Appendix E files (12 total) - [Status]
  - [ ] E.01-E.04: Doppler and grid tools
  - [ ] E.05-E.07: Cross-section and tally tools
  - [ ] E.08-E.09: Parameter study and ACE tools
  - [ ] E.10-E.12: UM tools
- [ ] Documentation phase complete: [✅/⏸️]

### Skills Completed: X/6 (Y%)

**Reference & Lookup:**
1. [ ] mcnp-unit-converter
2. [ ] mcnp-physical-constants
3. [ ] mcnp-isotope-lookup

**Specialized Tools:**
4. [ ] mcnp-cross-section-manager
5. [ ] mcnp-parallel-configurator
6. [ ] mcnp-template-generator

**Phase 4 Complete:** [Date/Session]
```

---

## 🔗 INTEGRATION WITH OTHER PHASES

### Phase 1 → Phase 4 Connection
**Phase 1 skills referenced by Phase 4:**
- **material-builder** → Uses isotope-lookup, unit-converter
- **input-builder** → Uses template-generator
- **physics-builder** → May use cross-section-manager

### Phase 4 → All Phases Connection
**Phase 4 provides supporting tools for all other phases:**
- unit-converter: Used by ALL skills with quantitative inputs
- physical-constants: Used for validation and calculations
- isotope-lookup: Used by material-builder, source-builder
- cross-section-manager: Used for library troubleshooting
- template-generator: Helps users get started with any skill

**Integration emphasis:**
- These are "horizontal" skills that support others
- SKILL.md should show usage examples with other skills
- Cross-reference extensively

---

## 🚨 END-OF-SESSION REQUIREMENTS (PARALLEL EXECUTION) 🚨

**MANDATORY for every session working on Phase 4:**

### Update Documents

1. **PHASE-4-PROJECT-STATUS.md** - Add session summary with session ID
2. **GLOBAL-SESSION-REQUIREMENTS.md lines 135-157** - Update Phase 4 Progress section
3. Inform user of completion status

**Emphasize:**
- Phase 4 has NO dependencies - can execute with any other phase in parallel
- Python scripts are ESSENTIAL (not optional) for these utility skills
- These skills support ALL other phases

---

**END OF PHASE 4 MASTER PLAN**

**Remember:** Phase 4 utility skills are fully independent. Can execute in parallel with ALL other phases. Update GLOBAL-SESSION-REQUIREMENTS.md at session end. Python scripts are core functionality.
