# MSRE Validation Execution Checklist
## Quick Reference for Workflow Testing

**Date Started:** _____________
**Executor:** _____________

---

## PRE-EXECUTION SETUP

- [ ] MSRE benchmark literature available (`msre-benchmark/`)
- [ ] All MCNP skills accessible
- [ ] All MCNP agents accessible
- [ ] MCNP6 executable available
- [ ] ENDF/B-VII.1 cross-section library configured
- [ ] Output directory structure created

---

## PHASE 1: LITERATURE ANALYSIS

### Step 1.1: Document Analysis (PARALLEL)
- [ ] Launch `mcnp-tech-doc-analyzer` Instance 1 (Berkeley benchmark)
- [ ] Launch `mcnp-tech-doc-analyzer` Instance 2 (Design spec)
- [ ] Launch `mcnp-tech-doc-analyzer` Instance 3 (Additional literature)
- [ ] Claude consolidates all outputs
- [ ] Parameter discrepancies identified
- [ ] **Gate 1.1 PASSED** ✓

### Step 1.2: Parameter Validation
- [ ] Units converted to cm, g/cm³
- [ ] Material densities validated at 911 K
- [ ] Isotopic abundances verified
- [ ] Thermal expansion calculated (293 K → 911 K)
- [ ] Fuel salt composition verified
- [ ] **Gate 1.2 PASSED** ✓

### Step 1.3: Design Spec Document
- [ ] `MSRE_Design_Specification_Complete.md` created
- [ ] All parameters sourced from literature
- [ ] Assumptions documented
- [ ] **GATE 1 (Critical): Claude approval** ✓

**Phase 1 Token Count:** _________ (Target: < 50K)

---

## PHASE 2: INITIAL MODEL DEVELOPMENT

### Step 2.1: Geometry Strategy
- [ ] `mcnp-geometry-builder` planning complete
- [ ] `mcnp-lattice-builder` planning complete
- [ ] Surface numbering scheme approved
- [ ] Universe hierarchy designed
- [ ] Claude strategy approval
- [ ] **Gate 2.1 PASSED** ✓

### Step 2.2: Core Lattice Construction
- [ ] `mcnp-lattice-builder` executes build (hexahedral/square, LAT=1)
- [ ] `mcnp-geometry-builder` skill reviews syntax
- [ ] `mcnp-cell-checker` validates references
- [ ] Iteration complete (zero errors)
- [ ] All 1,140 fuel channels defined
- [ ] Infinite square lattice bounded by RCC core geometry
- [ ] **Gate 2.2 PASSED** ✓

### Step 2.3: Reflector/Vessel (PARALLEL)
- [ ] Task 1: Radial reflector built
- [ ] Task 2: Vessel and structures built
- [ ] Claude verifies no overlaps
- [ ] **Gate 2.3 PASSED** ✓

### Step 2.4: Materials (PARALLEL)
- [ ] Instance 1: Fuel salt material complete
- [ ] Instance 2: Graphite material complete
- [ ] Instance 3: Hastelloy-N material complete
- [ ] Instance 4: Control materials complete
- [ ] `mcnp-cross-section-manager` verifies all ZAIDs
- [ ] **Gate 2.4 PASSED** ✓

### Step 2.5: Source Definition
- [ ] KCODE parameters set
- [ ] Physics options configured
- [ ] **Gate 2.5 PASSED** ✓

### Step 2.6: Validation Cascade
- [ ] `mcnp-input-validator` PASS
- [ ] `mcnp-geometry-checker` PASS
- [ ] `mcnp-cross-reference-checker` PASS
- [ ] `mcnp-best-practices-checker` PASS (57 items)
- [ ] `mcnp-physics-validator` PASS
- [ ] **GATE 2 (Critical): Claude approval to run** ✓

### Step 2.7: Initial MCNP Run
- [ ] Geometry plot mode executed
- [ ] If fatal errors: `mcnp-fatal-error-debugger` used
- [ ] Full run executed
- [ ] If warnings: `mcnp-warning-analyzer` assessed
- [ ] `mcnp-output-parser` extracted results
- [ ] **Gate 2.7 PASSED** ✓

### Step 2.8: Results Analysis (PARALLEL)
- [ ] `mcnp-criticality-analyzer` completed
- [ ] `mcnp-statistics-checker` completed
- [ ] `mcnp-plotter` generated plots
- [ ] Claude synthesized report
- [ ] keff = ________ (Target: 0.99-1.03)
- [ ] Shannon entropy slope = ________ (Target: < 0.001)
- [ ] Lost particles = ________% (Target: < 0.01%)
- [ ] **GATE 3 (Critical): Phase 1 complete** ✓

**Phase 2 Token Count:** _________ (Target: < 200K)

**Phase 1 Model File:** `msre_phase1_model.inp`

---

## PHASE 3: BENCHMARK REFINEMENT

### Step 3.1: Benchmark Comparison
- [ ] `mcnp-tech-doc-analyzer` re-analyzes benchmark
- [ ] Claude compares Phase 1 vs benchmark
- [ ] Discrepancy list created
- [ ] Refinement plan prioritized
- [ ] **Gate 3.1 PASSED** ✓

### Step 3.2: Geometry Refinements
- [ ] `mcnp-geometry-editor` applies refinements
- [ ] `mcnp-cell-checker` validates
- [ ] `mcnp-geometry-checker` verifies
- [ ] All dimensions within ±0.01 cm of benchmark
- [ ] **Gate 3.2 PASSED** ✓

### Step 3.3: Material Refinements (PARALLEL)
- [ ] Fuel salt updated to exact benchmark
- [ ] Graphite density updated (911 K)
- [ ] Hastelloy-N refined
- [ ] Temperature cards applied
- [ ] **Gate 3.3 PASSED** ✓

### Step 3.4: Physics Refinement
- [ ] KCODE parameters matched to benchmark
- [ ] Statistics increased (500/100/50K)
- [ ] `mcnp-physics-validator` confirms
- [ ] **Gate 3.4 PASSED** ✓

### Step 3.5: Validation Cascade (Repeat)
- [ ] All 5 validators PASS
- [ ] **GATE 4 (Critical): Benchmark run approval** ✓

### Step 3.6: Benchmark Execution
- [ ] Benchmark run executed
- [ ] `mcnp-criticality-analyzer` analyzed
- [ ] `mcnp-statistics-checker` validated
- [ ] keff = ________ (Target: 1.02132 ± 0.00003)
- [ ] C-E discrepancy = ________% (Target: 2.154%)
- [ ] **GATE 5 (Critical): Benchmark validation success** ✓

### Step 3.7: Results Documentation
- [ ] `mcnp-plotter` publication plots generated
- [ ] Results summary table created
- [ ] Final model documentation complete
- [ ] **Gate 3.7 PASSED** ✓

**Phase 3 Token Count:** _________ (Target: < 150K)

**Benchmark Model File:** `msre_benchmark_model.inp`

---

## PHASE 4: ADVANCED FEATURES (OPTIONAL)

### Step 4.1: Variance Reduction
- [ ] `mcnp-variance-reducer` strategy designed
- [ ] `mcnp-ww-optimizer` implemented
- [ ] FOM improvement = ________× (Target: > 10×)
- [ ] **Gate 4.1 PASSED** ✓

### Step 4.2: Tally Suite (PARALLEL)
- [ ] Flux tallies (F4) built
- [ ] Power distribution (F7) built
- [ ] Reaction rates (F4+FM) built
- [ ] 3D mesh tally built
- [ ] All tallies pass 10 statistical checks
- [ ] **Gate 4.2 PASSED** ✓

### Step 4.3: Parallel Configuration
- [ ] `mcnp-parallel-configurator` configured HPC
- [ ] Checkpointing set up
- [ ] Restart tested
- [ ] **Gate 4.3 PASSED** ✓

### Step 4.4: Burnup Setup
- [ ] `mcnp-burnup-builder` configured BURN card
- [ ] Depletion regions defined
- [ ] **Gate 4.4 PASSED** ✓

**Phase 4 Token Count:** _________ (Target: < 100K)

---

## INTEGRATION VALIDATION MATRIX

### Skills Used (15 Total)

- [ ] mcnp-input-builder
- [ ] mcnp-geometry-builder
- [ ] mcnp-material-builder
- [ ] mcnp-source-builder
- [ ] mcnp-tally-builder
- [ ] mcnp-physics-builder
- [ ] mcnp-lattice-builder
- [ ] mcnp-mesh-builder
- [ ] mcnp-geometry-editor
- [ ] mcnp-input-editor
- [ ] mcnp-plotter
- [ ] mcnp-physical-constants
- [ ] mcnp-unit-converter
- [ ] mcnp-isotope-lookup
- [ ] mcnp-cross-section-manager

**Skills Coverage:** _____ / 15 (Target: 15/15)

### Agents Used (17 Total)

- [ ] mcnp-tech-doc-analyzer
- [ ] mcnp-example-finder
- [ ] mcnp-input-validator
- [ ] mcnp-geometry-checker
- [ ] mcnp-cell-checker
- [ ] mcnp-cross-reference-checker
- [ ] mcnp-best-practices-checker
- [ ] mcnp-physics-validator
- [ ] mcnp-fatal-error-debugger
- [ ] mcnp-warning-analyzer
- [ ] mcnp-output-parser
- [ ] mcnp-criticality-analyzer
- [ ] mcnp-statistics-checker
- [ ] mcnp-variance-reducer
- [ ] mcnp-ww-optimizer
- [ ] mcnp-parallel-configurator
- [ ] mcnp-burnup-builder

**Agents Coverage:** _____ / 17 (Target: 17/17)

### Integration Patterns Tested (8 Total)

- [ ] Sequential Cascade
- [ ] Parallel Execution
- [ ] Validation Loop
- [ ] Skill-Agent Handoff
- [ ] Agent-Skill Handoff
- [ ] Claude Orchestration
- [ ] Cross-Validation
- [ ] Iterative Refinement

**Patterns Coverage:** _____ / 8 (Target: 8/8)

---

## FINAL SUCCESS CRITERIA

### Phase 1 Success
- [ ] MCNP runs without fatal errors
- [ ] Lost particles < 0.01%
- [ ] keff = 0.99-1.03
- [ ] Shannon entropy converged
- [ ] 1,140 fuel channels defined
- [ ] All validators pass

### Phase 2 Success (Benchmark)
- [ ] keff = 1.02132 ± 0.00003
- [ ] C-E discrepancy = 2.154% ± 0.003%
- [ ] All dimensions match benchmark
- [ ] All materials match benchmark
- [ ] Statistical quality excellent

### Overall Integration Success
- [ ] All 15 skills tested
- [ ] All 17 agents tested
- [ ] All 8 integration patterns demonstrated
- [ ] Total tokens < 600K
- [ ] All quality gates passed
- [ ] Production-ready model created

---

## TOKEN EFFICIENCY TRACKING

| Phase | Target | Actual | Status |
|-------|--------|--------|--------|
| Phase 1 (Literature) | < 50K | _____ | ⬜ |
| Phase 2 (Initial Model) | < 200K | _____ | ⬜ |
| Phase 3 (Benchmark) | < 150K | _____ | ⬜ |
| Phase 4 (Advanced) | < 100K | _____ | ⬜ |
| **TOTAL** | **< 500K** | **_____** | **⬜** |

---

## DELIVERABLES CHECKLIST

### Documentation
- [ ] `MSRE_Design_Specification_Complete.md`
- [ ] `Phase1_Validation_Report.md`
- [ ] `Phase1_Results.md`
- [ ] `Phase3_Refinements_Log.md`
- [ ] `Phase3_Benchmark_Results.md`
- [ ] `Integration_Test_Results.md`
- [ ] `Token_Efficiency_Report.md`
- [ ] `Skills_Agents_Coverage_Matrix.md`
- [ ] `Workflow_Lessons_Learned.md`

### MCNP Files
- [ ] `msre_phase1_model.inp`
- [ ] `msre_benchmark_model.inp`
- [ ] Output files (OUTP, MCTAL)
- [ ] Geometry plot files

### Plots & Figures
- [ ] Phase1_Geometry_Plots/
- [ ] Phase3_Geometry_Plots/
- [ ] keff convergence plots
- [ ] Shannon entropy plots
- [ ] Publication-quality figures

---

## ISSUES LOG

| Issue # | Description | Tool Used | Resolution | Status |
|---------|-------------|-----------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

---

## NOTES & OBSERVATIONS

_Use this space to record insights, challenges, and recommendations for future workflow improvements_

---

## SIGN-OFF

**Phase 1 Complete:** __________ (Date/Signature)

**Phase 2 Complete:** __________ (Date/Signature)

**Phase 3 Complete:** __________ (Date/Signature)

**Phase 4 Complete:** __________ (Date/Signature)

**Overall Validation:** __________ (Date/Signature)

---

**VALIDATION STATUS: ⬜ NOT STARTED | ⬜ IN PROGRESS | ⬜ COMPLETE**
