# PHASE 4 PROJECT STATUS - CATEGORY F SKILLS (6 SKILLS)

**Phase:** 4 of 5
**Category:** F - Utilities & Reference Tools
**Skills:** 6 (unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator)
**Status:** IN PROGRESS (Session 1)
**Session ID:** Session-20251106-043353-Phase4
**Created:** 2025-11-06

---

## 🎯 PHASE 4 OVERVIEW

### Phase Objectives
Revamp 6 utility and reference skills that provide supporting tools, unit conversions, physical constants, isotope lookups, and cross-section management. These are "horizontal" skills that support all other phases.

### Phase Strategy
- **Documentation:** Read Appendix E (12 files) ONCE at phase start
- **Token Budget:** ~90k tokens total (30-37k docs + 60k skills)
- **Dependencies:** NONE - All skills independent, can start immediately
- **Special Focus:** Python scripts are ESSENTIAL (core functionality, not optional)

### Skills in Phase 4 (Processing Order)

#### Reference & Lookup Tools (High Priority)
1. ✅ **mcnp-unit-converter** - Converting between unit systems for MCNP (COMPLETED)
2. ✅ **mcnp-physical-constants** - Physical constants for MCNP calculations (COMPLETED)
3. ✅ **mcnp-isotope-lookup** - Isotope properties and ZAID format (COMPLETED)

#### Specialized Tools
4. ✅ **mcnp-cross-section-manager** - Cross-section library management and xsdir (COMPLETED)
5. ⏸️ **mcnp-parallel-configurator** - Parallel execution, checkpointing, restart (NEXT)
6. ⏸️ **mcnp-template-generator** - Generate template MCNP inputs for common problems

### Progress Summary
- **Skills Completed:** 4/6 (66.67%)
- **Documentation Reading:** ✅ COMPLETED (12/12 files read)
- **Tokens Used:** ~280k / 90k budgeted (significantly over due to comprehensive Python tools and extensive reference documentation)

---

## 📚 DOCUMENTATION READING PHASE

### Required Documentation: Appendix E (12 files)

**Location:** `markdown_docs/appendices/`

#### Utility Tools Documentation
1. ⏸️ **AppendixE_01_Doppler_Broadening.md** (~3k tokens)
   - Doppler broadening program for cross sections
   - Temperature broadening techniques

2. ⏸️ **AppendixE_02_Event_Log_Analyzer.md** (~3k tokens)
   - mcnp_ela executable for event log analysis
   - Log file format, event analysis

3. ⏸️ **AppendixE_03_Doppler_Fitting.md** (~3k tokens)
   - dopplerfit executable for cross-section fitting
   - Fitting parameters, optimization

4. ⏸️ **AppendixE_04_Gridconv.md** (~3k tokens)
   - gridconv executable for grid conversion
   - Grid format conversion, interpolation

5. ⏸️ **AppendixE_05_Cross_Section_Tool.md** (~4k tokens)
   - cse (Cross Section Evaluator) tool
   - ENDF/ACE format, cross-section plotting

6. ⏸️ **AppendixE_06_Merge_ASCII_Tally.md** (~3k tokens)
   - merge_ascii_tally executable for combining tallies
   - Merging multiple runs, statistical combination

7. ⏸️ **AppendixE_07_Merge_Mesh_Tally.md** (~3k tokens)
   - merge_mesh_tally executable for mesh combination
   - Mesh tally merging, format handling

8. ⏸️ **AppendixE_08_Parameter_Study_Tool.md** (~4k tokens)
   - pst executable for parametric studies
   - Input parameterization, batch execution

9. ⏸️ **AppendixE_09_Simple_ACE_Tools.md** (~3k tokens)
   - Basic ACE file manipulation tools
   - ACE format, cross-section data structure

10. ⏸️ **AppendixE_10_UM_Converter.md** (~4k tokens)
    - umconv executable for unstructured mesh conversion
    - Mesh format conversion, UM tools

11. ⏸️ **AppendixE_11_UM_Post_Processing.md** (~4k tokens)
    - UM post-processing utilities
    - Visualization, data extraction
    - **Note:** May be cached from Phase 2 if that phase was executed

12. ⏸️ **AppendixE_12_UM_Pre_Processing.md** (~4k tokens)
    - UM pre-processing tools
    - Mesh generation, quality checking

### Documentation Reading Strategy
- Read all 12 files in parallel (multiple Read tool calls in single message)
- Take comprehensive notes on key utility tools and their applications
- Focus on practical usage patterns for the 6 skills
- Estimated tokens: 30-37k (37k if E.11 not cached from Phase 2)

### Documentation Reading Status
- **Files Read:** 12/12 ✅ COMPLETED
- **Status:** All Appendix E files read in parallel
- **Tokens Used:** ~40k
- **Key Findings:** Most relevant to cross-section-manager and parallel-configurator; utility skills (unit-converter, physical-constants, isotope-lookup) require standard reference data rather than Appendix E documentation

---

## 🛠️ SKILLS PROCESSING (6 SKILLS)

### Skill #1: mcnp-unit-converter (HIGH PRIORITY)
**Status:** ✅ COMPLETED
**Priority:** High - Used constantly by MCNP practitioners
**Final Size:** 1333 lines SKILL.md + 2694 lines support files

**Completed Components:**

✅ **Python Scripts (scripts/ at ROOT - ESSENTIAL):**
- unit_converter.py (647 lines) - Standalone interactive/CLI conversion tool
  * Supports 9 conversion types (energy, length, density, temperature, cross section, activity, mass, time, angle)
  * Both interactive and command-line modes
  * No external dependencies (pure stdlib)
  * Conversion history tracking
- mcnp_unit_checker.py (481 lines) - MCNP input file validator
  * Scans input files for unit errors
  * Validates densities, energies, temperatures, time/energy bins
  * Provides suggestions and fixes
  * Exit codes for CI/CD integration
- README.md (comprehensive) - Usage guide with examples

✅ **Reference Files (at ROOT level - NO subdirectories):**
- conversion_tables.md - Complete conversion factors, physical constants, unit matrices
- unit_standards.md - MCNP card-by-card unit specifications
- physical_unit_systems.md - SI, CGS, Imperial system comparisons

✅ **Data Files (example_inputs/ at ROOT - NO assets/):**
- quick_reference.csv - Common conversion reference data (35+ conversions)

✅ **Structure Verification:**
- NO assets/ directory (ZERO TOLERANCE requirement met!)
- All reference files at ROOT level
- Python tools functional and standalone

**Commit:** 348a409 (2694 lines added)
**Progress:** COMPLETE

---

### Skill #2: mcnp-physical-constants (HIGH PRIORITY)
**Status:** ✅ COMPLETED
**Priority:** High - Core reference
**Final Size:** 380 lines SKILL.md + comprehensive support files

**Completed Components:**

✅ **Python Scripts (scripts/ at ROOT - ESSENTIAL):**
- constants_lookup.py (438 lines) - Interactive/CLI constant and particle lookup
  * Search physical constants and particle properties
  * CODATA 2018 and PDG 2020 values
  * Interactive and command-line modes
  * No external dependencies (pure stdlib)
- unit_aware_calculator.py (528 lines) - Scientific calculator with unit handling
  * 8 calculation types (atom density, thermal energy, neutron speed, Q-value, binding energy, fission rate, decay constant, specific activity)
  * Automatic unit conversions
  * Interactive and command-line modes
  * Pure stdlib implementation
- README.md (comprehensive) - Complete tool documentation with examples

✅ **Reference Files (at ROOT level - NO subdirectories):**
- fundamental_constants.md (412 lines) - CODATA 2018 universal, EM, gravitational constants
- particle_properties.md (440 lines) - Leptons, nucleons, light nuclei detailed properties
- nuclear_constants.md (577 lines) - Fission, fusion, decay data, nuclear energy scales
- benchmark_cross_sections.md (584 lines) - Thermal cross sections, typical values for validation

✅ **Data Files (example_inputs/ at ROOT - NO assets/):**
- quick_reference.csv - 30 most common constants with multiple unit systems

✅ **Structure Verification:**
- NO assets/ directory (ZERO TOLERANCE requirement met!) ✅
- All reference files at ROOT level
- Python tools functional and tested
- 26-item quality checklist PASSED

**Progress:** COMPLETE

---

### Skill #3: mcnp-isotope-lookup (HIGH PRIORITY)
**Status:** ✅ COMPLETED
**Priority:** High - Essential for material definitions
**Final Size:** 497 lines SKILL.md + 4,857 lines support files

**Completed Components:**

✅ **Python Scripts (scripts/ at ROOT - ESSENTIAL):**
- zaid_lookup.py (380 lines) - Interactive/CLI ZAID conversion tool
  * Element/isotope to ZAID conversion
  * ZAID parsing and validation
  * Interactive and command-line modes
  * No external dependencies (pure stdlib)
- isotope_properties.py (369 lines) - Isotope data retrieval
  * Atomic masses and natural abundances
  * Half-life lookup
  * Average mass calculation
  * Interactive and command-line modes
- library_checker.py (393 lines) - xsdir availability checking
  * Check ZAID availability in MCNP data files
  * Search for isotopes by pattern
  * Validate entire input files
  * Library statistics
- README.md (414 lines) - Comprehensive tool documentation with examples

✅ **Reference Files (at ROOT level - NO subdirectories):**
- zaid_format_guide.md (607 lines) - ZAID format specification, library suffixes, thermal scattering
- isotope_database.md (485 lines) - Atomic masses, natural abundances, element properties
- library_availability.md (700 lines) - Cross-section libraries, xsdir format, temperature libraries
- decay_data.md (736 lines) - Decay modes, half-lives, fission products, activation products

✅ **Data Files (example_inputs/ at ROOT - NO assets/):**
- common_isotopes.csv - 48 commonly used isotopes with properties
- natural_abundances.csv - Natural isotopic compositions for 8 multi-isotope elements
- library_temperatures.csv - Temperature-dependent library reference

✅ **Structure Verification:**
- NO assets/ directory (ZERO TOLERANCE requirement met!) ✅
- All reference files at ROOT level
- Python tools functional and tested
- 26-item quality checklist PASSED

**Progress:** COMPLETE

---

### Skill #4: mcnp-cross-section-manager
**Status:** ✅ COMPLETED
**Priority:** Medium - Advanced users
**Final Size:** 511 lines SKILL.md + comprehensive support files

**Completed Components:**

✅ **Python Scripts (scripts/ at ROOT - ESSENTIAL):**
- xsdir_parser.py (502 lines) - Interactive/CLI xsdir file parsing and querying
  * Find specific ZAIDs in xsdir
  * Search by pattern (regex)
  * List by section (directory, thermal, photoatomic, photoelectron)
  * Extract library statistics
  * Temperature conversion (MeV ↔ Kelvin)
  * Interactive and command-line modes
- library_finder.py (462 lines) - Find available libraries and recommend alternatives
  * Find all libraries for an isotope
  * List all isotopes of an element
  * Check ZAID availability
  * Recommend alternatives for missing libraries
  * Interactive and command-line modes
- missing_library_diagnoser.py (476 lines) - Diagnose library errors systematically
  * Verify DATAPATH and xsdir setup
  * Diagnose MCNP error messages (4 error types)
  * Check input files for missing libraries
  * Provide systematic troubleshooting steps
  * Interactive and command-line modes
- README.md (414 lines) - Comprehensive tool documentation with workflows

✅ **Reference Files (at ROOT level - NO subdirectories):**
- xsdir_format.md (562 lines) - Complete xsdir specification, parsing methods, diagnostics
- library_types.md (528 lines) - Detailed library type reference (.c, .t, .p, .e, .d)
- temperature_libraries.md (612 lines) - Temperature-dependent library guide, interpolation
- troubleshooting_libraries.md (562 lines) - Comprehensive error diagnosis procedures

✅ **Data Files (example_inputs/ at ROOT - NO assets/):**
- xsdir_example.txt (160 lines) - Sample xsdir entries showing format
- error_messages.txt (246 lines) - Common MCNP error examples for practice
- library_matrix.csv (86 lines) - Library availability matrix by version

✅ **Structure Verification:**
- NO assets/ directory (ZERO TOLERANCE requirement met!) ✅
- All reference files at ROOT level
- Python tools functional with both interactive and CLI modes
- 26-item quality checklist PASSED

**Progress:** COMPLETE

---

### Skill #5: mcnp-parallel-configurator
**Status:** ⏸️ Not started
**Priority:** Medium - HPC users
**Current:** ~850 lines (estimate)

**Key Capabilities:**
- PRDMP card (checkpointing intervals)
- TASKS card (multi-tasking specification)
- DBCN card (source distribution)
- MPI/OpenMP execution
- Runtpe file management
- Checkpoint/restart workflow

**References to Create (at ROOT level):**
- parallel_execution.md - MPI vs OpenMP, thread models
- checkpoint_restart.md - PRDMP, runtpe files, restart procedure
- distributed_computing.md - TASKS, DBCN usage
- performance_optimization.md - Load balancing, scaling

**Scripts to Bundle (scripts/ at ROOT):**
- prdmp_calculator.py - Optimal checkpoint intervals
- parallel_launcher.py - Generate submission scripts

**Examples (example_inputs/ at ROOT - NO assets/):**
- Parallel execution examples
- HPC job submission scripts

**Progress:** Not started

---

### Skill #6: mcnp-template-generator
**Status:** ⏸️ Not started
**Priority:** Medium - Convenience tool
**Current:** ~800 lines (estimate)

**Key Capabilities:**
- Basic problem types (shielding, criticality, dose, activation)
- Template generation from parameters
- Boilerplate input sections
- Standard configurations (material libraries, tallies)

**References to Create (at ROOT level):**
- problem_types.md - Shielding, criticality, etc. templates
- template_structure.md - Anatomy of templates
- customization_guide.md - How to modify templates

**Scripts to Bundle (scripts/ at ROOT):**
- template_generator.py - Interactive template creation
- problem_configurator.py - Parameterized input generation

**Assets (templates/ at ROOT - NO assets/):**
- Template library from basic_examples/
- Boilerplate sections (header, materials, tallies)
- Templates from other skills (Phase 1)

**Integration:**
- Links to input-builder (Phase 1)
- References templates/ from Phase 1 skills
- Uses examples from example_files/ as templates

**Progress:** Not started

---

## 🚨 CRITICAL REQUIREMENTS (ZERO TOLERANCE)

### Directory Structure (MANDATORY)
```
.claude/skills/[skill-name]/
├── SKILL.md                          ← Main skill file
├── [reference].md files              ← At ROOT level (NOT in subdirectories)
├── scripts/                          ← Subdirectory for scripts ONLY
│   └── [script files]
├── templates/                        ← DIRECTLY at root (NOT in assets/)
│   └── [template files]
└── example_inputs/                   ← DIRECTLY at root (NOT in assets/)
    └── [data files]
```

### WRONG Structures (NEVER CREATE)
❌ NO references/ subdirectory
❌ NO assets/ subdirectory - ZERO TOLERANCE (Lesson #16)

### Quality Checklist (26 Items)
**Item #23:** NO assets/ directory exists (ZERO TOLERANCE - auto-fail if present)

### Python Scripts
- **ESSENTIAL** for these utility skills (core functionality, not optional)
- Must be functional and tested
- Well-documented with README.md in scripts/
- Interactive calculators, converters, lookup tools

---

## 📊 PHASE 4 PROGRESS TRACKING

### Overall Progress
- **Phase Status:** IN PROGRESS
- **Skills Completed:** 0/6 (0%)
- **Documentation Reading:** Not started (0/12 files)
- **Current Session:** Session-20251106-043353-Phase4
- **Tokens Used:** ~60k / 90k budgeted (~67% remaining)

### Skills Queue
1. ⏸️ mcnp-unit-converter (NEXT - HIGH PRIORITY)
2. ⏸️ mcnp-physical-constants
3. ⏸️ mcnp-isotope-lookup
4. ⏸️ mcnp-cross-section-manager
5. ⏸️ mcnp-parallel-configurator
6. ⏸️ mcnp-template-generator

### Next Session Should
1. Read all 12 Appendix E files (parallel reading for efficiency)
2. Take comprehensive notes on utility tools
3. Begin processing first skill: mcnp-unit-converter
4. Create Python scripts (ESSENTIAL for utility skills)
5. Update this status document continuously

---

## 🎯 SESSION SUMMARIES

### Session 1: Session-20251106-043353-Phase4

**Date:** 2025-11-06
**Session ID:** Session-20251106-043353-Phase4
**Duration:** In progress
**Tokens Used:** ~60k

**Session Objectives:**
1. Complete parallel session startup procedure
2. Create PHASE-4-PROJECT-STATUS.md
3. Read Appendix E documentation (12 files)
4. Begin processing skills in order

**Completed This Session:**
- ✅ Verified working directory
- ✅ Read PHASE-4-MASTER-PLAN.md
- ✅ Read LESSONS-LEARNED.md
- ✅ Generated session ID: Session-20251106-043353-Phase4
- ✅ Verified Phase 4 dependencies: NONE (all skills independent)
- ✅ Created PHASE-4-PROJECT-STATUS.md
- ⏸️ Documentation reading pending
- ⏸️ Skill processing pending

**Skills In Progress:** None yet

**Skills Completed This Session:** 0

**Skills Remaining:** 6

**Critical Context:**
Phase 4 is fully independent with NO dependencies on other phases. All 6 skills are utility and reference tools that support other phases. Python scripts are ESSENTIAL (core functionality). Data files go in example_inputs/ at root level (NO assets/ subdirectory - ZERO TOLERANCE per Lesson #16). Ready to begin documentation reading phase.

**Next Actions:**
1. Read all 12 Appendix E files in parallel
2. Take comprehensive notes on utility tools
3. Begin mcnp-unit-converter (first skill - HIGH PRIORITY)
4. Create functional Python scripts
5. Update status document continuously

---

## ✅ PHASE 4 SUCCESS CRITERIA

### Phase Complete When:
- ✅ All 12 Appendix E files read and understood
- ✅ All 6 skills processed through 11-step workflow
- ✅ Every skill passes 26-item quality checklist (includes NO assets/ check)
- ✅ All Python scripts functional and tested
- ✅ Reference data files created at root level
- ✅ Integration with other phases documented
- ✅ This status document reflects accurate completion
- ✅ Token budget within estimates (~90k)
- ✅ GLOBAL-SESSION-REQUIREMENTS.md Phase 4 section updated

---

**END OF PHASE 4 PROJECT STATUS**

**Remember:** Phase 4 skills are fully independent. Python scripts are ESSENTIAL. NO assets/ directory - ZERO TOLERANCE. Update this document continuously during session.
