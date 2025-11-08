# NEXT SESSION: IMMEDIATE EXECUTION GUIDE (REVISED)
## Complete MCNP Skills Refinement Based on HTGR Analysis

**Status**: ✅ **ANALYSIS COMPLETE** - Ready for implementation
**Date**: November 7, 2025 (Revised)
**Estimated Execution Time**: 3-4 hours (Phase 1 only)

**REVISION NOTES**:
- ✅ Added hexagonal lattice (LAT=2) support throughout
- ✅ Always specify lattice TYPE in examples and tests
- ✅ Generalized to ALL complex reactor models (not TRISO-only)
- ✅ Corrected directory structure (no assets/ subdirectories)
- ✅ Python validation includes both rectangular AND hexagonal
- ✅ TRISO content moved to supplemental reference files

---

## WHAT WAS ACCOMPLISHED THIS SESSION

### ✅ Analysis Complete

**10 Parallel Agents** analyzed the HTGR reactor model repository comprehensively:

1. ✅ **Agent 1**: Research article analysis → AGR-1_Technical_Analysis_Report.md (58 KB)
2. ✅ **Agent 2**: Cell card structure → AGR1_CELL_CARD_COMPLETE_ANALYSIS.md (31 KB)
3. ✅ **Agent 3**: Surface card structure → AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md (39 KB)
4. ✅ **Agent 4**: Material cards → AGR1_Material_Card_Analysis.md (46 KB)
5. ✅ **Agent 5**: Template structure → AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md (50 KB)
6. ✅ **Agent 6**: Input generation workflow → ANALYSIS_INPUT_GENERATION_WORKFLOW.md (50 KB)
7. ✅ **Agent 7**: Microreactor programmatic model → Embedded in synthesis
8. ✅ **Agent 8**: FILL arrays deep dive → AGENT8_FILL_ARRAY_DEEP_DIVE.md (46 KB)
   - **CRITICAL**: Covers BOTH rectangular (LAT=1) AND hexagonal (LAT=2) lattices
9. ✅ **Agent 9**: Cross-referencing patterns → 4 documents (102 KB)
10. ✅ **Agent 10**: Best practices synthesis → HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md (39 KB)

**Total**: 13 comprehensive documents, 469 KB of detailed analysis

### ✅ Synthesis Complete

Created **COMPREHENSIVE_FINDINGS_SYNTHESIS.md** integrating all agent findings

### ✅ Executable Plan Complete (REVISED)

Created **SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md** with:
- **Hexagonal lattice (LAT=2) support** throughout
- **Lattice TYPE specification** in all examples
- **Complete Python validation** for both rectangular AND hexagonal
- **Generalized guidance** for ALL complex reactor models
- **Correct directory structure** (reference files at ROOT, scripts/ subdirectory)
- **TRISO as supplemental** content, not main focus

---

## CRITICAL FINDINGS (REVISED)

### 🔴 HIGH-PRIORITY ISSUES IDENTIFIED

1. **mcnp-lattice-builder**:
   - ❌ No multi-level nesting guidance (>2 levels)
   - ❌ No FILL array dimension calculator
   - ❌ No repeat notation (nR) explanation
   - ❌ **No hexagonal lattice (LAT=2) guidance**
   - ❌ **No lattice TYPE specification in examples**
   - **Impact**: Users cannot build ANY complex reactor models (PWR, BWR, HTGR, fast reactors, CANDU, etc.)

2. **mcnp-material-builder**:
   - ❌ No thermal scattering (MT card) requirements
   - ❌ No temperature-dependent library selection
   - ❌ No comprehensive fuel composition examples
   - **Impact**: Missing MT cards cause 1000-5000 pcm reactivity errors in ANY thermal reactor

3. **mcnp-input-validator**:
   - ❌ No FILL array validation for LAT=1 OR LAT=2
   - ❌ No universe cross-reference checking
   - ❌ No numbering conflict detection
   - **Impact**: Errors only caught when MCNP fails (wasted computation)

4. **mcnp-geometry-builder**:
   - ❌ No reactor assembly templates (rectangular or hexagonal)
   - ❌ No multi-scale geometry guidance
   - ❌ No lattice-type-specific examples
   - **Impact**: Users cannot create complex reactor geometries

---

## HOW TO EXECUTE IN NEXT SESSION

### STEP 1: Start Session

```
I'm ready to execute the REVISED MCNP skill refinement plan.

Start with Phase 1 (HIGH PRIORITY) from SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md.

Begin with skill #1: mcnp-lattice-builder
```

### STEP 2: For Each Skill in Phase 1

The REVISED plan provides **exact instructions** with BOTH lattice types:

**Example: mcnp-lattice-builder**

1. ✅ Read section 1 of SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md
2. ✅ File paths given with CORRECT structure:
   - SKILL.md (updated)
   - lattice_patterns_reference.md (ROOT level)
   - complex_reactor_patterns.md (ROOT level)
   - triso_fuel_reference.md (supplemental, ROOT level)
   - scripts/lattice_dimension_calculator.py (in scripts/ subdirectory)
   - example_inputs/rectangular_pwr_assembly.i
   - example_inputs/hexagonal_htgr_assembly.i
3. ✅ Content covers BOTH LAT=1 and LAT=2
4. ✅ Python tool validates BOTH rectangular and hexagonal
5. ✅ Examples for BOTH lattice types
6. ✅ Validation tests specify lattice TYPE

### STEP 3: Validation

After each skill update:
```
Test the updated mcnp-lattice-builder skill with these queries:

Query 1: "How do I create a RECTANGULAR lattice with 17×17 fuel pins?"
Expected:
1. Lattice type: LAT=1
2. Surface type: RPP
3. Dimension calculation (17×17×1 = 289)
4. fill=-8:8 -8:8 0:0 specification
5. Working PWR assembly example

Query 2: "How do I create a HEXAGONAL lattice for reactor assemblies?"
Expected:
1. Lattice type: LAT=2
2. Surface type: RHP
3. Pitch calculation (R × √3)
4. Dimension calculation for hex pattern
5. Working HTGR example with staggered rows
```

### STEP 4: Directory Structure Verification

After creating files, verify correct structure:

```bash
ls -R .claude/skills/mcnp-lattice-builder/

# Expected structure:
# .claude/skills/mcnp-lattice-builder/
# ├── SKILL.md
# ├── lattice_patterns_reference.md           ← ROOT level
# ├── complex_reactor_patterns.md             ← ROOT level
# ├── triso_fuel_reference.md                 ← ROOT level (supplemental)
# ├── scripts/                                 ← Subdirectory
# │   └── lattice_dimension_calculator.py
# └── example_inputs/                          ← Subdirectory at ROOT
#     ├── rectangular_pwr_assembly.i
#     └── hexagonal_htgr_assembly.i
#
# NOT assets/examples/ or assets/scripts/
```

### STEP 5: Commit Progress

After completing each skill:
```
git add .claude/skills/mcnp-lattice-builder
git commit -m "Refine mcnp-lattice-builder: Add LAT=1 & LAT=2, FILL arrays, multi-level nesting

- Added hexagonal lattice (LAT=2) support
- Created reference files at ROOT (not assets/)
- Python tool validates both rectangular and hexagonal
- Examples for PWR (rectangular) and HTGR (hexagonal)
- Generalized to all complex reactor models"
```

---

## PHASE 1 EXECUTION CHECKLIST (REVISED)

### Skill 1: mcnp-lattice-builder (90 min)

- [ ] Update SKILL.md
  - [ ] Add lattice types section (LAT=1 AND LAT=2)
  - [ ] Add FILL array mechanics (both types)
  - [ ] Add repeat notation section
  - [ ] Add multi-level hierarchy section
  - [ ] Add hexagonal-specific guidance (pitch = R×√3, staggered rows)
  - [ ] Add validation checklist (both types)
  - [ ] Add common pitfalls table (including hex-specific errors)

- [ ] Create lattice_patterns_reference.md (ROOT level)
  - [ ] Rectangular lattice examples (PWR, vertical stacks)
  - [ ] Hexagonal lattice examples (HTGR, fast reactors)
  - [ ] Mixed lattice hierarchies

- [ ] Create complex_reactor_patterns.md (ROOT level)
  - [ ] PWR core (4-level, all LAT=1)
  - [ ] HTGR core (5-level, mixed LAT=1 and LAT=2)
  - [ ] Fast reactor (3-level, LAT=2 hex bundles)

- [ ] Create triso_fuel_reference.md (ROOT level, supplemental)
  - [ ] TRISO-specific patterns (optional reading)

- [ ] Create scripts/lattice_dimension_calculator.py
  - [ ] calculate_fill_dimensions() - works for both types
  - [ ] repeat_notation_converter() - works for both types
  - [ ] validate_lattice_dimensions() - COMPLETE for LAT=1 AND LAT=2
  - [ ] calculate_hex_pitch() - hexagonal pitch calculator

- [ ] Create example_inputs/rectangular_pwr_assembly.i
  - [ ] 17×17 PWR assembly (LAT=1)
  - [ ] Complete with surfaces, materials

- [ ] Create example_inputs/hexagonal_htgr_assembly.i
  - [ ] 13×13 HTGR assembly (LAT=2)
  - [ ] RHP surface, staggered fill pattern

- [ ] Test with BOTH queries
  - [ ] "Create RECTANGULAR lattice with 17×17 pins"
  - [ ] "Create HEXAGONAL lattice for assemblies"
  - [ ] Verify type-specific guidance provided

### Skill 2: mcnp-material-builder (60 min)

- [ ] Update SKILL.md
  - [ ] Add thermal scattering section (ALL reactor types)
  - [ ] Add temperature library tables (grph, lwtr, hwtr)
  - [ ] Add common fuel types section (generalized)
  - [ ] Add burnup tracking section
  - [ ] Add common errors section (generalized)

- [ ] Create fuel_compositions_reference.md (ROOT level)
  - [ ] UO₂ fuel (PWR, BWR)
  - [ ] MOX fuel (Pu-bearing)
  - [ ] UCO fuel (HTGR, TRISO kernels)
  - [ ] Metallic fuel (fast reactors)
  - [ ] HALEU fuel (advanced reactors)

- [ ] Create thermal_scattering_guide.md (ROOT level)
  - [ ] Complete S(α,β) library reference
  - [ ] Temperature selection guide
  - [ ] Physics explanation

- [ ] Create triso_fuel_reference.md (ROOT level, supplemental)
  - [ ] TRISO-specific compositions (optional)

- [ ] Create scripts/thermal_scattering_checker.py
  - [ ] check_material_for_thermal_scattering()
  - [ ] recommend_thermal_library()

- [ ] Create example_inputs/common_fuel_materials.txt
  - [ ] UO₂, MOX, graphite, water examples
  - [ ] All with appropriate MT cards

- [ ] Test with various queries
  - [ ] "Create UO₂ fuel materials"
  - [ ] "Create graphite moderator"
  - [ ] "Create MOX fuel"
  - [ ] Verify MT cards included, generalized guidance

### Skill 3: mcnp-input-validator (40 min)

- [ ] Update SKILL.md
  - [ ] Add FILL array validation section (LAT=1 AND LAT=2)
  - [ ] Add universe validation section
  - [ ] Add thermal scattering checks

- [ ] Create scripts/fill_array_validator.py
  - [ ] parse_fill_spec()
  - [ ] count_fill_elements()
  - [ ] validate_fill_array() - BOTH rectangular and hexagonal

- [ ] Test validation
  - [ ] Provide rectangular lattice with wrong dimensions
  - [ ] Provide hexagonal lattice with wrong RHP surface
  - [ ] Verify both caught

### Skill 4: mcnp-geometry-builder (40 min)

- [ ] Create templates/fuel_pin_template.txt (ROOT level)
  - [ ] Standard PWR/BWR pin geometry

- [ ] Create templates/hex_assembly_template.txt (ROOT level)
  - [ ] HTGR hexagonal assembly

- [ ] Create triso_particle_reference.md (ROOT level, supplemental)
  - [ ] TRISO-specific geometry (optional)

- [ ] Update SKILL.md
  - [ ] Add multi-scale geometry section
  - [ ] Add template references
  - [ ] Add lattice-type-specific guidance

- [ ] Test with queries
  - [ ] "Create PWR fuel pin geometry"
  - [ ] "Create hexagonal assembly geometry"
  - [ ] Verify type-appropriate guidance

---

## WHAT YOU'LL HAVE AFTER PHASE 1 (REVISED)

### 4 Refined Skills with BOTH Lattice Types

1. ✅ **mcnp-lattice-builder**
   - Can build rectangular (LAT=1) AND hexagonal (LAT=2) lattices
   - Multi-level nesting for ALL reactor types
   - Type-specific validation

2. ✅ **mcnp-material-builder**
   - Thermal scattering for ALL reactor types
   - Comprehensive fuel compositions (UO₂, MOX, UCO, metallic, HALEU)
   - TRISO as ONE example among many

3. ✅ **mcnp-input-validator**
   - FILL array validation for BOTH lattice types
   - Catches errors pre-execution

4. ✅ **mcnp-geometry-builder**
   - Templates for BOTH rectangular and hexagonal assemblies
   - Multi-scale guidance

### User Capabilities Enabled

✅ Build ANY complex reactor model (PWR, BWR, HTGR, fast reactors, CANDU, etc.)
✅ Create rectangular lattices (LAT=1) for PWR assemblies, vertical stacks
✅ Create hexagonal lattices (LAT=2) for HTGR, fast reactors
✅ Combine both types in multi-level hierarchies
✅ Generate proper materials with MT cards for ALL reactor types
✅ Validate FILL arrays for BOTH lattice types
✅ Avoid thermal scattering errors

### New Assets Created

- 3 Python validation tools (lattice dimension for BOTH types, thermal scattering)
- 6+ complete MCNP example files (rectangular AND hexagonal)
- 8+ reference .md files (fuel compositions, lattice patterns, thermal scattering guide)
- Comprehensive documentation (updated SKILL.md files)
- Working templates (PWR pin, hex assembly, TRISO as supplemental)

### Directory Structure (CORRECT)

```
.claude/skills/mcnp-lattice-builder/
├── SKILL.md
├── lattice_patterns_reference.md           ← ROOT level
├── complex_reactor_patterns.md             ← ROOT level
├── triso_fuel_reference.md                 ← ROOT level (supplemental)
├── scripts/                                 ← Subdirectory
│   └── lattice_dimension_calculator.py
└── example_inputs/                          ← Subdirectory
    ├── rectangular_pwr_assembly.i
    └── hexagonal_htgr_assembly.i

.claude/skills/mcnp-material-builder/
├── SKILL.md
├── fuel_compositions_reference.md          ← ROOT level
├── thermal_scattering_guide.md             ← ROOT level
├── triso_fuel_reference.md                 ← ROOT level (supplemental)
├── scripts/
│   └── thermal_scattering_checker.py
└── example_inputs/
    └── common_fuel_materials.txt
```

**NOT** `assets/examples/` or `assets/templates/`

---

## REFERENCE DOCUMENTS

### Analysis Documents (Read for Context)

Located in `/home/user/mcnp-skills/`:

1. **COMPREHENSIVE_FINDINGS_SYNTHESIS.md** - Master synthesis
2. **SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md** - REVISED execution plan (USE THIS)
3. **AGENT8_FILL_ARRAY_DEEP_DIVE.md** - CRITICAL: covers LAT=1 AND LAT=2
4. **AGR1_CELL_CARD_COMPLETE_ANALYSIS.md** - Cell patterns
5. **AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md** - Surface patterns (RPP and RHP)

---

## QUICK START (REVISED)

### Command to Begin Next Session

```bash
# Navigate to skills directory
cd /home/user/mcnp-skills

# Open the REVISED execution plan
cat SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md | less

# Start with Phase 1, Skill 1
# All content includes BOTH rectangular AND hexagonal support!
```

### What to Say

```
"I'm ready to refine the MCNP skills based on the HTGR analysis.

Execute Phase 1 from SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md.

Start with mcnp-lattice-builder.

Include BOTH rectangular (LAT=1) and hexagonal (LAT=2) support."
```

---

## SUCCESS METRICS (REVISED)

### After Phase 1 Completion

You should be able to:

1. ✅ Ask skill: "Build a RECTANGULAR lattice with 17×17 pins"
   - Get LAT=1-specific guidance
   - Get RPP surface specification
   - Get PWR assembly example
   - Get dimension validation

2. ✅ Ask skill: "Build a HEXAGONAL lattice for reactor assemblies"
   - Get LAT=2-specific guidance
   - Get RHP surface specification
   - Get HTGR assembly example
   - Get hex pitch calculation (R × √3)

3. ✅ Ask skill: "Create UO₂ fuel materials"
   - Get UO₂ composition
   - Get appropriate MT card warning if needed
   - Get generalized guidance (not TRISO-only)

4. ✅ Ask skill: "Create graphite moderator"
   - Get graphite composition
   - Get CRITICAL MT card requirement
   - Get temperature selection guidance

5. ✅ Provide RECTANGULAR lattice with wrong FILL dimensions
   - Validator catches error
   - Type-specific error message

6. ✅ Provide HEXAGONAL lattice with RPP surface (wrong type)
   - Validator catches error
   - Recommends RHP for LAT=2

---

## IMPORTANT NOTES (REVISED)

1. **All content includes BOTH lattice types** - No research needed
2. **Copy-paste ready** - Code and examples complete for LAT=1 and LAT=2
3. **Validated patterns** - From production reactor models (PWR, HTGR, etc.)
4. **Generalized guidance** - Not TRISO-specific
5. **Correct structure** - Reference files at ROOT, scripts/ subdirectory
6. **TRISO as supplement** - Optional reading, not main focus

---

**YOU ARE READY TO EXECUTE THE REVISED PLAN!** 🚀

Start next session with:
```
"Execute Phase 1 from SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md

Include BOTH rectangular and hexagonal lattice support"
```
