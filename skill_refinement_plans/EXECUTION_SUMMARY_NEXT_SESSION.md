# NEXT SESSION: IMMEDIATE EXECUTION GUIDE
## Complete MCNP Skills Refinement Based on HTGR Analysis

**Status**: ✅ **ANALYSIS COMPLETE** - Ready for implementation
**Date**: November 7, 2025
**Estimated Execution Time**: 3-4 hours (Phase 1 only)

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
9. ✅ **Agent 9**: Cross-referencing patterns → 4 documents (102 KB)
10. ✅ **Agent 10**: Best practices synthesis → HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md (39 KB)

**Total**: 13 comprehensive documents, 469 KB of detailed analysis

### ✅ Synthesis Complete

Created **COMPREHENSIVE_FINDINGS_SYNTHESIS.md** integrating all agent findings into:
- Critical lattice building patterns
- Systematic numbering schemes
- Material card best practices
- Template-based automation workflows
- Programmatic generation approaches
- Cross-referencing validation
- Multi-physics workflow integration

### ✅ Executable Plan Complete

Created **SKILL_REFINEMENT_PLAN_EXECUTABLE.md** with:
- Specific file paths to modify
- Exact content to add (ready to insert)
- New Python tools (complete code)
- New example files (complete content)
- Validation tests for each skill
- 3-phase execution strategy

---

## CRITICAL FINDINGS

### 🔴 HIGH-PRIORITY ISSUES IDENTIFIED

1. **mcnp-lattice-builder**:
   - ❌ No multi-level nesting guidance (>2 levels)
   - ❌ No FILL array dimension calculator
   - ❌ No repeat notation (nR) explanation
   - ❌ No circular packing patterns
   - **Impact**: Users cannot build reactor models with TRISO fuel

2. **mcnp-material-builder**:
   - ❌ No thermal scattering (MT card) requirements
   - ❌ No temperature-dependent library selection
   - ❌ No TRISO material examples
   - **Impact**: Missing MT cards cause 1000s of pcm reactivity errors

3. **mcnp-input-validator**:
   - ❌ No FILL array validation
   - ❌ No universe cross-reference checking
   - ❌ No numbering conflict detection
   - **Impact**: Errors only caught when MCNP fails (wasted computation)

4. **mcnp-geometry-builder**:
   - ❌ No TRISO particle templates
   - ❌ No reactor assembly patterns
   - ❌ No multi-scale geometry guidance
   - **Impact**: Users cannot create complex reactor geometries

### 🟡 MAJOR ENHANCEMENT OPPORTUNITIES

1. **mcnp-template-generator** (NEW SKILL NEEDED):
   - Would enable parametric studies
   - Would support multi-cycle burnup
   - Would integrate with external data (CSV)

2. **mcnp-programmatic-generator** (NEW SKILL NEEDED):
   - Would enable function-based geometry
   - Would support large-scale models
   - Would ensure consistency between variants

---

## HOW TO EXECUTE IN NEXT SESSION

### STEP 1: Start Session

```
I'm ready to execute the MCNP skill refinement plan.

Start with Phase 1 (HIGH PRIORITY) from SKILL_REFINEMENT_PLAN_EXECUTABLE.md.

Begin with skill #1: mcnp-lattice-builder
```

### STEP 2: For Each Skill in Phase 1

The plan provides **exact instructions** for each skill:

**Example: mcnp-lattice-builder**

1. ✅ Read section 1 of SKILL_REFINEMENT_PLAN_EXECUTABLE.md
2. ✅ File path given: `.claude/skills/mcnp-lattice-builder/SKILL.md`
3. ✅ Content to add: Complete markdown section (copy-paste ready)
4. ✅ New tool: `lattice_dimension_calculator.py` (complete code provided)
5. ✅ Examples: 2 complete MCNP files provided
6. ✅ Validation test: Specific user query with expected output

### STEP 3: Validation

After each skill update:
```
Test the updated mcnp-lattice-builder skill with this query:
"How do I create a lattice with 15×15 TRISO particles?"

Expected output should include:
1. Dimension calculation (225 elements)
2. fill=-7:7 -7:7 0:0 specification
3. Circular packing pattern
4. Working example
```

### STEP 4: Commit Progress

After completing each skill:
```
git add .claude/skills/mcnp-lattice-builder
git commit -m "Refine mcnp-lattice-builder: Add multi-level nesting, FILL arrays, TRISO examples"
```

### STEP 5: Repeat for All Phase 1 Skills

1. mcnp-lattice-builder ✓
2. mcnp-material-builder
3. mcnp-input-validator
4. mcnp-geometry-builder

---

## PHASE 1 EXECUTION CHECKLIST

### Skill 1: mcnp-lattice-builder (60 min)

- [ ] Update SKILL.md
  - [ ] Add FILL array mechanics section
  - [ ] Add repeat notation section
  - [ ] Add multi-level hierarchy section
  - [ ] Add circular packing section
  - [ ] Add validation checklist
  - [ ] Add common pitfalls table

- [ ] Create tools/lattice_dimension_calculator.py
  - [ ] calculate_fill_dimensions()
  - [ ] repeat_notation_converter()
  - [ ] validate_lattice_dimensions()

- [ ] Create assets/examples/triso_particle_lattice.i
  - [ ] 15×15 particle lattice example
  - [ ] Complete with surfaces, materials

- [ ] Create assets/examples/triso_compact_lattice.i
  - [ ] 3-level nested lattice
  - [ ] Compact with repeat notation

- [ ] Test with user query
  - [ ] "How do I create 15×15 TRISO lattice?"
  - [ ] Verify all 5 expected outputs

### Skill 2: mcnp-material-builder (45 min)

- [ ] Update SKILL.md
  - [ ] Add thermal scattering section
  - [ ] Add temperature library table
  - [ ] Add TRISO materials section
  - [ ] Add burnup tracking section
  - [ ] Add common errors section

- [ ] Create tools/thermal_scattering_checker.py
  - [ ] check_material_for_thermal_scattering()
  - [ ] recommend_thermal_library()

- [ ] Create assets/examples/triso_materials.txt
  - [ ] 6 TRISO materials (kernel + 5 coatings)
  - [ ] All with MT cards

- [ ] Test with user query
  - [ ] "Create materials for TRISO fuel"
  - [ ] Verify MT cards included

### Skill 3: mcnp-input-validator (30 min)

- [ ] Update SKILL.md
  - [ ] Add FILL array validation section
  - [ ] Add universe validation section
  - [ ] Add thermal scattering checks

- [ ] Create tools/fill_array_validator.py
  - [ ] parse_fill_spec()
  - [ ] count_fill_elements()
  - [ ] validate_fill_array()

- [ ] Test validation
  - [ ] Provide input with wrong dimensions
  - [ ] Verify error caught

### Skill 4: mcnp-geometry-builder (30 min)

- [ ] Create assets/templates/triso_particle_template.txt
  - [ ] Complete 5-layer geometry
  - [ ] Annotated surfaces

- [ ] Update SKILL.md
  - [ ] Add multi-scale geometry section
  - [ ] Add TRISO template reference

- [ ] Test with user query
  - [ ] "Create TRISO particle geometry"
  - [ ] Verify template provided

---

## WHAT YOU'LL HAVE AFTER PHASE 1

### 4 Refined Skills

1. ✅ **mcnp-lattice-builder** - Can build complex reactor lattices
2. ✅ **mcnp-material-builder** - Always includes thermal scattering
3. ✅ **mcnp-input-validator** - Catches errors pre-execution
4. ✅ **mcnp-geometry-builder** - Has reactor geometry templates

### User Capabilities Enabled

✅ Build TRISO fuel particle models
✅ Create multi-level lattice hierarchies (up to 6 levels)
✅ Generate proper material cards with MT cards
✅ Validate FILL arrays before running MCNP
✅ Avoid common thermal scattering errors

### New Assets Created

- 2 Python validation tools (lattice dimension, thermal scattering)
- 4 complete MCNP example files (TRISO lattices + materials)
- Comprehensive documentation (updated SKILL.md files)
- Working templates (TRISO geometry)

---

## AFTER PHASE 1: NEXT STEPS

### Phase 2 (Session 2)

Create 2 new skills:
1. **mcnp-template-generator** - Jinja2 templating for parametric studies
2. **mcnp-programmatic-generator** - Function-based model creation

Enhance 3 existing skills:
3. **mcnp-input-builder** - Add systematic numbering
4. **mcnp-cell-checker** - Add universe hierarchy validation
5. **mcnp-cross-reference-checker** - Add automated validation

### Phase 3 (Session 3)

Advanced features:
1. **mcnp-workflow-integrator** - Multi-physics coupling
2. Additional enhancements based on user feedback

---

## REFERENCE DOCUMENTS

### Analysis Documents (Read for Context)

Located in `/home/user/mcnp-skills/`:

1. **COMPREHENSIVE_FINDINGS_SYNTHESIS.md** - Master synthesis (all findings)
2. **SKILL_REFINEMENT_PLAN_EXECUTABLE.md** - Detailed execution plan (THIS IS THE KEY DOC)
3. **AGR1_CELL_CARD_COMPLETE_ANALYSIS.md** - Cell card patterns
4. **AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md** - Surface card patterns
5. **AGR1_Material_Card_Analysis.md** - Material card patterns
6. **AGENT8_FILL_ARRAY_DEEP_DIVE.md** - FILL array mechanics (CRITICAL)
7. **HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md** - Overall best practices

Located in `analysis_reports/`:

8. **AGENT9_CROSS_REFERENCING_PATTERNS.md** - Cross-reference validation
9. **AGENT9_QUICK_REFERENCE.md** - Quick syntax lookup

### Source Examples (Copy from Here)

Located in `example_files/reactor-model_examples/htgr-model-burnup-and-doserates/`:

- **agr-1/mcnp/sdr-agr.i** - Complete TRISO model (4,653 lines)
- **agr-1/bench.template** - Jinja2 template example (13,727 lines)
- **micro/input_definition.py** - Programmatic generation example

---

## QUICK START

### Command to Begin Next Session

```bash
# Navigate to skills directory
cd /home/user/mcnp-skills

# Open the execution plan
cat SKILL_REFINEMENT_PLAN_EXECUTABLE.md | less

# Start with Phase 1, Skill 1
# All content is copy-paste ready!
```

### What to Say

```
I'm ready to refine the MCNP skills based on the HTGR analysis.

Execute Phase 1 from SKILL_REFINEMENT_PLAN_EXECUTABLE.md.

Start with mcnp-lattice-builder (section 1).
```

---

## SUCCESS METRICS

### After Phase 1 Completion

You should be able to:

1. ✅ Ask skill: "How do I build a TRISO particle lattice?"
   - Get complete working example
   - Get FILL array dimension calculation
   - Get repeat notation explanation

2. ✅ Ask skill: "Create TRISO fuel materials"
   - Get all 6 materials with densities
   - Get MT cards for all carbon materials
   - Get temperature recommendations

3. ✅ Provide input with wrong FILL dimensions
   - Validator catches error
   - Clear error message explains fix

4. ✅ Ask skill: "Create TRISO particle geometry"
   - Get complete 5-layer template
   - Get surface definitions
   - Get material assignments

### Repository State

After Phase 1:
```
.claude/skills/
├── mcnp-lattice-builder/
│   ├── SKILL.md ← UPDATED (multi-level, FILL arrays)
│   ├── tools/
│   │   └── lattice_dimension_calculator.py ← NEW
│   └── assets/examples/
│       ├── triso_particle_lattice.i ← NEW
│       └── triso_compact_lattice.i ← NEW
├── mcnp-material-builder/
│   ├── SKILL.md ← UPDATED (thermal scattering)
│   ├── tools/
│   │   └── thermal_scattering_checker.py ← NEW
│   └── assets/examples/
│       └── triso_materials.txt ← NEW
├── mcnp-input-validator/
│   ├── SKILL.md ← UPDATED
│   └── tools/
│       └── fill_array_validator.py ← NEW
└── mcnp-geometry-builder/
    ├── SKILL.md ← UPDATED
    └── assets/templates/
        └── triso_particle_template.txt ← NEW
```

---

## IMPORTANT NOTES

1. **All content is provided** - No need to research or create from scratch
2. **Copy-paste ready** - Code and examples are complete
3. **Validated patterns** - All from production reactor models
4. **Immediately testable** - Each skill has validation query
5. **Incremental** - Complete one skill before moving to next

---

**YOU ARE READY TO EXECUTE**

The plan is comprehensive, detailed, and immediately executable.

Start next session with:
"Execute Phase 1 from SKILL_REFINEMENT_PLAN_EXECUTABLE.md"
