# MCNP Skill Refinement Plans - Index

**Created**: November 7, 2025
**Status**: ✅ All 15 skill-specific plans completed
**Total Documentation**: ~150 pages across 15 focused plans

---

## ✅ COMPLETED PLANS (15 Total)

### Phase 1: Critical Fixes (4 plans)

1. **mcnp-lattice-builder-REFINEMENT-PLAN.md** ✅
   - Multi-level nesting (up to 6 levels)
   - BOTH rectangular (LAT=1) AND hexagonal (LAT=2)
   - FILL array dimension calculation
   - Repeat notation (nR = n+1)
   - Complete 13×13 hex pattern included

2. **mcnp-material-builder-REFINEMENT-PLAN.md** ✅
   - Thermal scattering (MT cards) - CRITICAL
   - Temperature-dependent libraries
   - All fuel types (UO₂, MOX, UCO, metallic, HALEU)
   - TRISO as supplemental content

3. **mcnp-input-validator-REFINEMENT-PLAN.md** ✅
   - FILL array validation (both LAT types)
   - Universe cross-reference checking
   - Thermal scattering verification
   - Numbering conflict detection

4. **mcnp-geometry-builder-REFINEMENT-PLAN.md** ✅
   - Multi-scale geometry (μm to meters)
   - Reactor assembly templates
   - Surface type selection (RPP vs RHP)
   - Concentric geometry patterns

### Phase 2: Major Enhancements (6 plans)

5. **mcnp-template-generator-REFINEMENT-PLAN.md** ✅ (NEW SKILL)
   - Jinja2 template conversion
   - CSV parameter integration
   - Time-weighted averaging
   - Multi-cycle burnup workflows

6. **mcnp-input-builder-REFINEMENT-PLAN.md** ✅
   - Systematic numbering schemes
   - Three-block organization
   - Cross-reference consistency
   - Comment conventions

7. **mcnp-cell-checker-REFINEMENT-PLAN.md** ✅
   - Universe hierarchy validation
   - Circular reference detection
   - FILL array validation
   - LAT specification checking

8. **mcnp-cross-reference-checker-REFINEMENT-PLAN.md** ✅
   - Cell → Surface validation
   - Cell → Material validation
   - Cell → Universe validation
   - Automated validation tools

9. **mcnp-input-editor-REFINEMENT-PLAN.md** ✅
   - Multi-file batch editing
   - Template-aware editing
   - Lattice fill array editing
   - Material batch updates

10. **mcnp-geometry-editor-REFINEMENT-PLAN.md** ✅
    - Lattice geometry modification
    - Multi-level hierarchy editing
    - Hexagonal geometry editing
    - Universe hierarchy modification

### Phase 3: Advanced Features (5 plans)

11. **mcnp-programmatic-generator-REFINEMENT-PLAN.md** ✅ (NEW SKILL)
    - Function-based geometry generation
    - Parametric assembly definitions
    - Loop-based core generation
    - Model variant generation

12. **mcnp-workflow-integrator-REFINEMENT-PLAN.md** ✅ (NEW SKILL)
    - Multi-physics coupling (MCNP → ORIGEN → MCNP)
    - Workflow automation
    - Data handoff between codes
    - Burnup-to-dose-rate workflows

13. **mcnp-burnup-builder-REFINEMENT-PLAN.md** ✅
    - Cell selection for depletion
    - Fission product inclusion (4-tier system)
    - Actinide tracking
    - ORIGEN coupling

14. **mcnp-physics-validator-REFINEMENT-PLAN.md** ✅
    - Thermal scattering validation (CRITICAL)
    - Temperature-dependent libraries
    - Cross-section consistency
    - Energy cutoff verification

15. **mcnp-best-practices-checker-REFINEMENT-PLAN.md** ✅
    - 57-item checklist updates
    - Phase 0: Professional modeling (15 new items)
    - Reactor-specific extensions (8 new items)
    - Automated checking tool

---

## 📁 FILE STRUCTURE

```
/home/user/mcnp-skills/skill_refinement_plans/
├── README.md (this file)
├── ANALYSIS_DOCUMENT_LOCATIONS.md (reference guide)
├── mcnp-lattice-builder-REFINEMENT-PLAN.md
├── mcnp-material-builder-REFINEMENT-PLAN.md
├── mcnp-input-validator-REFINEMENT-PLAN.md
├── mcnp-geometry-builder-REFINEMENT-PLAN.md
├── mcnp-template-generator-REFINEMENT-PLAN.md (NEW SKILL)
├── mcnp-input-builder-REFINEMENT-PLAN.md
├── mcnp-cell-checker-REFINEMENT-PLAN.md
├── mcnp-cross-reference-checker-REFINEMENT-PLAN.md
├── mcnp-input-editor-REFINEMENT-PLAN.md
├── mcnp-geometry-editor-REFINEMENT-PLAN.md
├── mcnp-programmatic-generator-REFINEMENT-PLAN.md (NEW SKILL)
├── mcnp-workflow-integrator-REFINEMENT-PLAN.md (NEW SKILL)
├── mcnp-burnup-builder-REFINEMENT-PLAN.md
├── mcnp-physics-validator-REFINEMENT-PLAN.md
└── mcnp-best-practices-checker-REFINEMENT-PLAN.md
```

---

## 📊 ANALYSIS DOCUMENT MAPPING

Each skill plan references specific technical analysis documents:

### Primary Analysis Documents (Location: `/home/user/mcnp-skills/`)

1. **AGENT8_FILL_ARRAY_DEEP_DIVE.md** (46 KB)
   - Used by: mcnp-lattice-builder, mcnp-input-validator, mcnp-cell-checker

2. **AGR1_CELL_CARD_COMPLETE_ANALYSIS.md** (31 KB)
   - Used by: mcnp-lattice-builder, mcnp-geometry-builder, mcnp-input-builder, mcnp-cell-checker

3. **AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md** (39 KB)
   - Used by: mcnp-lattice-builder, mcnp-geometry-builder, mcnp-geometry-editor

4. **AGR1_Material_Card_Analysis.md** (46 KB)
   - Used by: mcnp-material-builder, mcnp-burnup-builder, mcnp-physics-validator

5. **AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md** (50 KB)
   - Used by: mcnp-template-generator, mcnp-input-editor

6. **ANALYSIS_INPUT_GENERATION_WORKFLOW.md** (50 KB)
   - Used by: mcnp-template-generator, mcnp-input-editor, mcnp-programmatic-generator

7. **HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md** (39 KB)
   - Used by: mcnp-workflow-integrator, mcnp-best-practices-checker

8. **COMPREHENSIVE_FINDINGS_SYNTHESIS.md** (28 KB)
   - Used by: ALL skills (context)

### Analysis Reports (Location: `/home/user/mcnp-skills/analysis_reports/`)

9. **AGENT9_CROSS_REFERENCING_PATTERNS.md** (45 KB)
   - Used by: mcnp-input-validator, mcnp-cross-reference-checker, mcnp-input-builder

10. **AGENT9_QUICK_REFERENCE.md** (8.7 KB)
    - Used by: mcnp-cross-reference-checker

11. **AGENT9_VISUAL_DIAGRAMS.md** (37 KB)
    - Used by: mcnp-cross-reference-checker

12. **README_AGENT9.md** (11 KB)
    - Used by: mcnp-cross-reference-checker

### Example Files (Location: `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/`)

13. **AGR-1_Technical_Analysis_Report.md** (58 KB)
    - Used by: mcnp-material-builder, mcnp-geometry-builder

14. **QUICK_REFERENCE_TRISO_SPECS.md** (20 KB)
    - Used by: mcnp-material-builder

---

## ⚠️ FILE PATH CORRECTIONS

**IMPORTANT**: Some agents tried to read files from wrong locations. Correct paths:

❌ WRONG: `/home/user/mcnp-skills/AGENT9_CROSS_REFERENCING_PATTERNS.md`
✅ CORRECT: `/home/user/mcnp-skills/analysis_reports/AGENT9_CROSS_REFERENCING_PATTERNS.md`

All Agent 9 documents are in: `/home/user/mcnp-skills/analysis_reports/`

---

## 📋 EXECUTION PLAN

### Parallel Execution (Recommended)

Execute Phase 1 skills in parallel (4 agents simultaneously):
```bash
# Session 1: Phase 1 (3-4 hours total, all parallel)
Agent 1: mcnp-lattice-builder (2-3 hours)
Agent 2: mcnp-material-builder (2.5-3 hours)
Agent 3: mcnp-input-validator (2 hours)
Agent 4: mcnp-geometry-builder (2.5 hours)
```

Then Phase 2 (6 agents):
```bash
# Session 2: Phase 2 (6-8 hours total, all parallel)
Agent 5: mcnp-template-generator (4-5 hours)
Agent 6: mcnp-input-builder (7 hours)
Agent 7: mcnp-cell-checker (2-3 hours)
Agent 8: mcnp-cross-reference-checker (2-3 hours)
Agent 9: mcnp-input-editor (10 hours)
Agent 10: mcnp-geometry-editor (3.5 hours)
```

Finally Phase 3 (5 agents):
```bash
# Session 3: Phase 3 (5-7 hours total, all parallel)
Agent 11: mcnp-programmatic-generator (6-8 hours)
Agent 12: mcnp-workflow-integrator (6-8 hours)
Agent 13: mcnp-burnup-builder (2-3 hours)
Agent 14: mcnp-physics-validator (5-7 hours)
Agent 15: mcnp-best-practices-checker (3.5 hours)
```

**Total Sequential**: ~50 hours
**Total Parallel**: ~15-20 hours (3 sessions)

---

## ✅ COMPLETION STATUS

All 15 skill-specific refinement plans are:
- ✅ Complete and comprehensive
- ✅ Based on real reactor model analysis
- ✅ Immediately executable
- ✅ Include validation tests
- ✅ Reference source documents
- ✅ Follow consistent structure

**Ready for user review and execution!**

---

## 📝 NEXT STEPS

1. **User reviews** each plan individually
2. **Corrects** any issues or gaps
3. **Approves** plans for execution
4. **Executes** Phase 1 (4 skills in parallel)
5. **Validates** Phase 1 results
6. **Proceeds** to Phase 2, then Phase 3

---

**Created by**: 15 parallel mcnp-tech-doc-analyzer sub-agents
**Quality**: Production-ready, based on professional reactor models
**Status**: Awaiting user review
