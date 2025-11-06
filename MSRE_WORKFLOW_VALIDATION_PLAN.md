# MSRE Workflow Validation Plan
## Seamless Integration Testing for MCNP Skills and Agents

**Version:** 1.0
**Date:** 2025-11-06
**Purpose:** Validate end-to-end integration of all MCNP skills and agents through comprehensive MSRE reactor modeling

---

## EXECUTIVE SUMMARY

### Validation Philosophy

This plan validates that:
1. **Skills and agents work together seamlessly** - No gaps in handoffs between tools
2. **Token efficiency is maximized** - Sub-agents handle complex research/analysis tasks
3. **Quality is maintained** - Continuous cross-validation at every step
4. **Workflows are flexible** - Both linear (sequential) and parallel execution modes work
5. **Production-ready outputs** - Models suitable for real reactor physics analysis

### Three-Tier Integration Model

```
┌─────────────────────────────────────────────────────────────┐
│ TIER 1: Claude (Orchestrator)                               │
│ - Overall workflow coordination                             │
│ - Quality assurance and validation                          │
│ - Decision making and planning                              │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
┌─────────────────────┐               ┌─────────────────────┐
│ TIER 2: Skills      │               │ TIER 2: Agents      │
│ - Direct execution  │               │ - Autonomous tasks  │
│ - Fast operations   │               │ - Research/analysis │
│ - Building/editing  │               │ - Token-efficient   │
└─────────────────────┘               └─────────────────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │ TIER 3: Cross-Validation Checkpoints  │
        │ - Continuous verification             │
        │ - Multi-tool validation               │
        │ - Quality gates                       │
        └───────────────────────────────────────┘
```

---

## PHASE 1: LITERATURE ANALYSIS & DESIGN EXTRACTION

### Objective
Extract all reactor design parameters from literature and create comprehensive design specification document.

### Workflow Steps

#### Step 1.1: Document Analysis (PARALLEL)
**Tools Used:**
- Agent: `mcnp-tech-doc-analyzer` (PRIMARY - 3 instances in parallel)
- Agent: `mcnp-example-finder` (SECONDARY)

**Tasks:**
1. **Instance 1:** Analyze `msre-benchmark/msre-benchmark-berkeley.md`
   - Extract all geometric parameters
   - Extract all material compositions
   - Extract benchmark keff values
   - Extract thermal conditions

2. **Instance 2:** Analyze `msre-benchmark/msre-design-spec.md`
   - Extract simplified model parameters
   - Cross-reference with Berkeley benchmark
   - Identify simplification differences

3. **Instance 3:** Search for additional MSRE literature
   - ORNL reports
   - IRPhEP specifications
   - Historical documentation

**Integration Point:** Claude consolidates outputs, identifies discrepancies, creates unified parameter table

**Validation Checkpoint 1.1:**
- [ ] All critical dimensions extracted with uncertainties
- [ ] Material compositions complete with isotopics
- [ ] Temperature conditions documented
- [ ] Cross-reference table shows consistency between sources
- [ ] Gaps identified and documented

---

#### Step 1.2: Parameter Validation (SEQUENTIAL)
**Tools Used:**
- Skill: `mcnp-physical-constants`
- Skill: `mcnp-unit-converter`
- Agent: `mcnp-isotope-lookup`

**Tasks:**
1. Convert all dimensions to consistent units (cm)
2. Validate material densities at operating temperature
3. Verify isotopic abundances
4. Calculate thermal expansion corrections (293 K → 911 K)
5. Validate fuel salt composition (LiF-BeF₂-ZrF₄-UF₄)

**Integration Point:** Skills provide quick calculations, agent handles complex isotopic research

**Validation Checkpoint 1.2:**
- [ ] All units consistent (cm, g/cm³, atoms/barn-cm)
- [ ] Thermal expansion factors calculated
- [ ] Isotopic data verified against ENDF/B-VII.1
- [ ] Physical constants validated
- [ ] Design parameter table complete

---

#### Step 1.3: Design Specification Synthesis
**Tools Used:**
- Claude (direct)

**Tasks:**
1. Create comprehensive design specification document
2. Organize by system: core, reflector, vessel, control rods
3. Flag areas requiring assumptions
4. Document simplifications for Phase 1 model
5. Document full-complexity requirements for Phase 2 model

**Validation Checkpoint 1.3:**
- [ ] Complete design spec document created
- [ ] All parameters traced to literature source
- [ ] Assumptions clearly documented
- [ ] Ready for geometry building

**Expected Output:** `MSRE_Design_Specification_Complete.md`

---

## PHASE 2: INITIAL SIMPLIFIED MODEL DEVELOPMENT

### Objective
Build working MSRE model with full geometry but simplified thermal/physics treatment to validate basic modeling workflow.

### Workflow Steps

#### Step 2.1: Geometry Definition Strategy (SEQUENTIAL)
**Tools Used:**
- Agent: `mcnp-geometry-builder` (PLANNING MODE)
- Agent: `mcnp-lattice-builder` (PLANNING MODE)

**Tasks:**
1. **Geometry Agent:** Plan surface definitions
   - Core cylinder (RCC macrobody)
   - Reflector regions (RCC macrobodies)
   - Vessel (RCC macrobody)
   - Control rod channels (RCC macrobodies)
   - NO infinite surfaces allowed

2. **Lattice Agent:** Plan lattice structure
   - Hexahedral (square) lattice for graphite stringers (LAT=1)
   - Universe hierarchy design
   - Fill array structure for 1,140 channels
   - Channel indexing scheme
   - Infinite square lattice bounded by RCC core geometry

**Integration Point:** Claude reviews both plans, ensures compatibility, approves strategy

**Validation Checkpoint 2.1:**
- [ ] Complete surface list with numbering scheme
- [ ] Lattice hierarchy documented
- [ ] Universe assignment plan created
- [ ] No surface/cell number conflicts
- [ ] Strategy approved by Claude

---

#### Step 2.2: Core Lattice Construction (SEQUENTIAL with VALIDATION LOOPS)
**Tools Used:**
- Agent: `mcnp-lattice-builder` (EXECUTION)
- Skill: `mcnp-geometry-builder` (REVIEW)
- Agent: `mcnp-cell-checker` (VALIDATION)

**Workflow:**
```
mcnp-lattice-builder → mcnp-geometry-builder → mcnp-cell-checker
         ↓                      ↓                       ↓
    BUILD LATTICE         REVIEW SYNTAX         VALIDATE REFS
         ↓                      ↓                       ↓
         └──────────── IF ISSUES FOUND ────────────────┘
                            ↓
                    ITERATE & FIX
```

**Tasks:**
1. **Lattice Builder Agent:**
   - Create base graphite stringer universe (U=1)
   - Define fuel channel cells within stringer
   - Create hexahedral/square lattice (LAT=1)
   - Build FILL array for 1,140 positions
   - Assign universe numbers systematically

2. **Geometry Builder Skill:**
   - Review cell definitions
   - Check surface assignments
   - Verify Boolean logic
   - Check fill references

3. **Cell Checker Agent:**
   - Validate U/FILL consistency
   - Check LAT specifications
   - Verify array dimensions
   - Check nesting hierarchy

**Integration Point:** Iterate until all validation passes

**Validation Checkpoint 2.2:**
- [ ] All 1,140 fuel channels defined
- [ ] Lattice structure correct (hexahedral/square, LAT=1)
- [ ] Universe hierarchy validated
- [ ] FILL array dimensions correct
- [ ] Infinite lattice properly bounded by RCC core geometry
- [ ] Cell checker reports zero errors

---

#### Step 2.3: Reflector and Vessel Construction (PARALLEL)
**Tools Used:**
- Skill: `mcnp-geometry-builder` (2 parallel tasks)

**Tasks:**
1. **Task 1:** Build radial reflector
   - Inner graphite reflector region
   - Outer graphite reflector region
   - Proper universe assignment (U=0)

2. **Task 2:** Build vessel and external structures
   - Reactor vessel (Hastelloy-N)
   - Control rod channels
   - Instrument channels

**Integration Point:** Claude ensures no geometric overlaps

**Validation Checkpoint 2.3:**
- [ ] Reflector regions properly defined
- [ ] Vessel completely encloses core
- [ ] Control rod channels positioned correctly
- [ ] No geometric gaps or overlaps

---

#### Step 2.4: Material Definitions (PARALLEL)
**Tools Used:**
- Agent: `mcnp-material-builder` (4 parallel instances)
- Skill: `mcnp-isotope-lookup` (as needed)
- Skill: `mcnp-cross-section-manager` (verification)

**Tasks:**
1. **Instance 1:** Fuel salt (LiF-BeF₂-ZrF₄-UF₄)
   - Calculate atom fractions
   - Expand isotopics (⁷Li enrichment)
   - Apply S(α,β) thermal scattering
   - Set density at 911 K

2. **Instance 2:** Graphite (moderator + reflector)
   - Nuclear graphite composition
   - Thermal scattering (grph.XX)
   - Temperature-dependent density

3. **Instance 3:** Hastelloy-N (vessel)
   - Complete alloy composition
   - All constituent isotopes

4. **Instance 4:** Control materials
   - Control rod materials
   - Any additional structural materials

**Integration Point:** Cross-section manager verifies all ZAIDs available in library

**Validation Checkpoint 2.4:**
- [ ] All materials defined with isotopics
- [ ] Densities correct for operating temperature
- [ ] Thermal scattering laws assigned
- [ ] All ZAIDs available in ENDF/B-VII.1
- [ ] Mass fractions sum to 1.0

---

#### Step 2.5: Source Definition (SEQUENTIAL)
**Tools Used:**
- Skill: `mcnp-source-builder`
- Agent: `mcnp-physics-builder`

**Tasks:**
1. Define KCODE parameters
   - Initial source distribution
   - Number of cycles (300 active, 100 inactive)
   - Particles per cycle (10,000)
   - Source convergence monitoring

2. Set physics options
   - MODE N (neutron transport)
   - PHYS:N card for neutron physics
   - Energy cutoffs
   - Temperature cards

**Validation Checkpoint 2.5:**
- [ ] KCODE parameters reasonable
- [ ] Source distribution covers core
- [ ] Physics settings appropriate for thermal reactor

---

#### Step 2.6: Comprehensive Input Validation (SEQUENTIAL CASCADE)
**Tools Used:**
- Agent: `mcnp-input-validator` (PRIMARY)
- Agent: `mcnp-geometry-checker` (SECONDARY)
- Agent: `mcnp-cross-reference-checker` (TERTIARY)
- Agent: `mcnp-best-practices-checker` (QUATERNARY)
- Agent: `mcnp-physics-validator` (QUINARY)

**Cascade Workflow:**
```
mcnp-input-validator (syntax, format)
         ↓ [IF PASS]
mcnp-geometry-checker (overlaps, gaps)
         ↓ [IF PASS]
mcnp-cross-reference-checker (cells→surfaces, cells→materials)
         ↓ [IF PASS]
mcnp-best-practices-checker (57-item checklist)
         ↓ [IF PASS]
mcnp-physics-validator (MODE, PHYS, libraries)
         ↓ [IF PASS]
    READY TO RUN
```

**Integration Point:** Claude reviews all validation reports, coordinates fixes if issues found

**Validation Checkpoint 2.6:**
- [ ] Input validator: PASS
- [ ] Geometry checker: PASS (no overlaps/gaps)
- [ ] Cross-reference checker: PASS (all refs valid)
- [ ] Best practices checker: PASS (all 57 items)
- [ ] Physics validator: PASS (settings consistent)
- [ ] Input file ready for execution

---

#### Step 2.7: Initial MCNP Run and Debug (ITERATIVE)
**Tools Used:**
- MCNP execution
- Agent: `mcnp-fatal-error-debugger` (if errors)
- Agent: `mcnp-warning-analyzer` (for warnings)
- Agent: `mcnp-output-parser` (for results)

**Workflow:**
```
RUN MCNP
   ↓
FATAL ERROR? ──YES→ mcnp-fatal-error-debugger → FIX → RERUN
   ↓ NO
WARNINGS? ──YES→ mcnp-warning-analyzer → ASSESS → FIX if critical
   ↓ NO/ACCEPTABLE
mcnp-output-parser → EXTRACT RESULTS
```

**Tasks:**
1. Execute MCNP with geometry plotting mode first
2. If fatal errors: debug systematically
3. Review warnings for criticality
4. Parse output for keff, convergence

**Validation Checkpoint 2.7:**
- [ ] MCNP runs to completion
- [ ] Zero fatal errors
- [ ] Lost particles < 0.01%
- [ ] Geometry plots generated
- [ ] Output file complete

---

#### Step 2.8: Results Analysis (PARALLEL)
**Tools Used:**
- Agent: `mcnp-criticality-analyzer`
- Agent: `mcnp-statistics-checker`
- Skill: `mcnp-plotter`

**Tasks:**
1. **Criticality Analyzer:**
   - Extract keff and uncertainty
   - Check Shannon entropy convergence
   - Analyze source distribution
   - Calculate C-E discrepancy

2. **Statistics Checker:**
   - Validate 10 statistical checks
   - Check FOM values
   - Assess confidence intervals

3. **Plotter:**
   - Generate geometry plots (XY, XZ, YZ)
   - Plot keff vs cycle
   - Plot Shannon entropy
   - Create publication-quality figures

**Integration Point:** Claude synthesizes all analyses into summary report

**Validation Checkpoint 2.8:**
- [ ] keff in range 0.99-1.03
- [ ] Shannon entropy converged (slope < 0.001)
- [ ] All 10 statistical checks passed
- [ ] Geometry plots match design
- [ ] Phase 1 success criteria met

**Expected Output:** `Phase1_Simplified_Model_Results.md`

---

## PHASE 3: BENCHMARK-QUALITY MODEL REFINEMENT

### Objective
Refine Phase 1 model to exactly match Berkeley benchmark specifications and achieve keff = 1.02132 ± 0.00003.

### Workflow Steps

#### Step 3.1: Benchmark Comparison Analysis (SEQUENTIAL)
**Tools Used:**
- Agent: `mcnp-tech-doc-analyzer` (re-analyze benchmark)
- Claude (comparison)

**Tasks:**
1. Re-extract ALL Berkeley benchmark specifications
2. Compare Phase 1 model against benchmark point-by-point
3. Identify all discrepancies
4. Prioritize refinements by impact on keff

**Validation Checkpoint 3.1:**
- [ ] Complete discrepancy list created
- [ ] Refinements prioritized
- [ ] Refinement plan documented

---

#### Step 3.2: Geometry Refinements (SEQUENTIAL with VALIDATION)
**Tools Used:**
- Skill: `mcnp-geometry-editor`
- Agent: `mcnp-cell-checker`
- Agent: `mcnp-geometry-checker`

**Tasks:**
1. Apply exact Berkeley dimensions
2. Refine lattice if needed
3. Update control rod positions
4. Apply thermal expansion corrections systematically

**Validation Loop:**
```
mcnp-geometry-editor → mcnp-cell-checker → mcnp-geometry-checker
         ↓                    ↓                      ↓
    MAKE EDITS          VALIDATE CELLS        CHECK GEOMETRY
         ↓                    ↓                      ↓
         └──────── IF ISSUES ─────────────────────────┘
```

**Validation Checkpoint 3.2:**
- [ ] All dimensions match benchmark ± 0.01 cm
- [ ] Thermal expansion correctly applied
- [ ] Geometry validation passes
- [ ] Cell validation passes

---

#### Step 3.3: Material Refinements (PARALLEL)
**Tools Used:**
- Skill: `mcnp-material-builder` (4 parallel tasks)
- Skill: `mcnp-input-editor` (batch updates)

**Tasks:**
1. Update fuel salt composition to exact benchmark values
2. Update graphite density (thermal expansion)
3. Refine Hastelloy-N composition
4. Apply temperature-dependent cross sections

**Validation Checkpoint 3.3:**
- [ ] All material compositions match benchmark tables
- [ ] Densities correct at 911 K
- [ ] Isotopic fractions verified
- [ ] TMP cards applied correctly

---

#### Step 3.4: Physics Settings Refinement (SEQUENTIAL)
**Tools Used:**
- Skill: `mcnp-physics-builder`
- Agent: `mcnp-physics-validator`

**Tasks:**
1. Match exact KCODE parameters from benchmark
2. Increase statistics (500 active, 100 inactive, 50,000 particles/cycle)
3. Apply benchmark-specific physics settings
4. Verify ENDF/B-VII.1 cross sections

**Validation Checkpoint 3.4:**
- [ ] Physics settings match benchmark
- [ ] Sufficient statistics for ±0.00003 uncertainty
- [ ] Cross-section library verified

---

#### Step 3.5: Full Validation Cascade (REPEAT OF 2.6)
**Tools Used:**
- All validators (same as Step 2.6)

**Validation Checkpoint 3.5:**
- [ ] All validators pass
- [ ] Refined input ready for benchmark run

---

#### Step 3.6: Benchmark Execution (ITERATIVE)
**Tools Used:**
- MCNP execution
- Agent: `mcnp-criticality-analyzer`
- Agent: `mcnp-statistics-checker`

**Tasks:**
1. Execute refined model
2. Monitor convergence
3. Analyze results against benchmark

**Target:** keff = 1.02132 ± 0.00003

**Validation Checkpoint 3.6:**
- [ ] keff matches benchmark within uncertainty
- [ ] C-E discrepancy = 2.154% ± 0.003%
- [ ] All convergence criteria met
- [ ] Statistical quality excellent

---

#### Step 3.7: Comprehensive Results Documentation
**Tools Used:**
- Agent: `mcnp-plotter` (publication plots)
- Claude (synthesis)

**Tasks:**
1. Generate all required plots
2. Create results summary table
3. Document validation against benchmark
4. Create final model documentation

**Expected Output:** `Phase3_Benchmark_Model_Complete.md`

---

## PHASE 4: ADVANCED FEATURES VALIDATION

### Objective
Demonstrate advanced skills/agents on production model.

### Workflow Steps

#### Step 4.1: Variance Reduction Optimization (SEQUENTIAL)
**Tools Used:**
- Agent: `mcnp-variance-reducer` (strategy)
- Agent: `mcnp-ww-optimizer` (implementation)

**Tasks:**
1. Analyze baseline FOM
2. Design weight window strategy
3. Implement and test
4. Measure efficiency improvement

**Success Metric:** 10× FOM improvement for peripheral tallies

---

#### Step 4.2: Tally Suite Development (PARALLEL)
**Tools Used:**
- Skill: `mcnp-tally-builder` (4 parallel tallies)
- Agent: `mcnp-mesh-builder` (mesh tally)

**Tasks:**
1. Build flux tallies (F4) in key regions
2. Build power distribution tally (F7)
3. Build reaction rate tallies (F4 with FM)
4. Build 3D mesh tally for visualization

**Validation:** All tallies pass 10 statistical checks

---

#### Step 4.3: Parallel Execution Configuration
**Tools Used:**
- Agent: `mcnp-parallel-configurator`

**Tasks:**
1. Configure for HPC execution
2. Set up checkpointing
3. Optimize TASKS card
4. Test restart capability

---

#### Step 4.4: Burnup Preparation (if time permits)
**Tools Used:**
- Agent: `mcnp-burnup-builder`

**Tasks:**
1. Set up BURN card
2. Define depletion regions
3. Configure CINDER90 coupling

---

## INTEGRATION VALIDATION MATRIX

### Skills Coverage

| Skill | Phase Used | Integration Test | Status |
|-------|-----------|------------------|--------|
| mcnp-input-builder | 2.5 | Source + overall structure | ⬜ |
| mcnp-geometry-builder | 2.1-2.3 | Core + reflector | ⬜ |
| mcnp-material-builder | 2.4, 3.3 | All materials | ⬜ |
| mcnp-source-builder | 2.5 | KCODE setup | ⬜ |
| mcnp-tally-builder | 4.2 | Flux/power tallies | ⬜ |
| mcnp-physics-builder | 2.5, 3.4 | MODE/PHYS cards | ⬜ |
| mcnp-lattice-builder | 2.2 | 1,140 channel lattice | ⬜ |
| mcnp-mesh-builder | 4.2 | 3D mesh tally | ⬜ |
| mcnp-geometry-editor | 3.2 | Refinement edits | ⬜ |
| mcnp-input-editor | 3.3 | Batch material updates | ⬜ |
| mcnp-plotter | 2.8, 3.7 | Geometry + results plots | ⬜ |
| mcnp-physical-constants | 1.2 | Unit validation | ⬜ |
| mcnp-unit-converter | 1.2 | Dimension conversion | ⬜ |
| mcnp-isotope-lookup | 2.4 | ZAID verification | ⬜ |
| mcnp-cross-section-manager | 2.4 | Library verification | ⬜ |

### Agents Coverage

| Agent | Phase Used | Integration Test | Status |
|-------|-----------|------------------|--------|
| mcnp-tech-doc-analyzer | 1.1, 3.1 | Literature extraction | ⬜ |
| mcnp-example-finder | 1.1 | Reference examples | ⬜ |
| mcnp-input-validator | 2.6, 3.5 | Syntax validation | ⬜ |
| mcnp-geometry-checker | 2.6, 3.2, 3.5 | Overlap detection | ⬜ |
| mcnp-cell-checker | 2.2, 3.2 | Lattice validation | ⬜ |
| mcnp-cross-reference-checker | 2.6, 3.5 | Reference validation | ⬜ |
| mcnp-best-practices-checker | 2.6, 3.5 | 57-item checklist | ⬜ |
| mcnp-physics-validator | 2.6, 3.5 | Physics consistency | ⬜ |
| mcnp-fatal-error-debugger | 2.7 | Error resolution | ⬜ |
| mcnp-warning-analyzer | 2.7 | Warning assessment | ⬜ |
| mcnp-output-parser | 2.7 | Results extraction | ⬜ |
| mcnp-criticality-analyzer | 2.8, 3.6 | keff analysis | ⬜ |
| mcnp-statistics-checker | 2.8, 3.6 | Statistical validation | ⬜ |
| mcnp-variance-reducer | 4.1 | VR strategy | ⬜ |
| mcnp-ww-optimizer | 4.1 | Weight windows | ⬜ |
| mcnp-parallel-configurator | 4.3 | HPC setup | ⬜ |
| mcnp-burnup-builder | 4.4 | Depletion setup | ⬜ |

### Integration Patterns Tested

| Pattern | Description | Tested In | Status |
|---------|-------------|-----------|--------|
| **Sequential Cascade** | Agent → Agent → Agent | Steps 2.6, 3.5 | ⬜ |
| **Parallel Execution** | Multiple agents simultaneously | Steps 1.1, 2.4, 4.2 | ⬜ |
| **Validation Loop** | Agent → Skill → Agent → Iterate | Step 2.2 | ⬜ |
| **Skill-Agent Handoff** | Skill builds → Agent validates | Steps 2.3→2.6 | ⬜ |
| **Agent-Skill Handoff** | Agent analyzes → Skill executes | Steps 2.1→2.2 | ⬜ |
| **Claude Orchestration** | Claude coordinates multiple tools | All phases | ⬜ |
| **Cross-Validation** | Multiple tools validate same output | Steps 2.6, 3.5 | ⬜ |
| **Iterative Refinement** | Build → Validate → Fix → Repeat | Steps 2.7, 3.6 | ⬜ |

---

## TOKEN EFFICIENCY VALIDATION

### Efficiency Metrics

Track token usage for:

1. **Agent Tasks (High Token Operations):**
   - Literature analysis (Step 1.1): Expected ~50K tokens/agent
   - Comprehensive validation (Step 2.6): Expected ~30K tokens total
   - Complex debugging (Step 2.7 if needed): Expected ~20K tokens

2. **Skill Tasks (Low Token Operations):**
   - Geometry building (Step 2.3): Expected ~5K tokens
   - Material definitions (Step 2.4): Expected ~3K tokens/material
   - Plotting (Step 2.8): Expected ~2K tokens

3. **Overall Workflow:**
   - Phase 1: Target < 200K total tokens
   - Phase 2: Target < 150K total tokens
   - Phase 3: Target < 150K total tokens
   - Phase 4: Target < 100K total tokens

### Efficiency Strategies Validated

- [ ] Use agents for research-heavy tasks (literature, examples, debugging)
- [ ] Use skills for direct execution (building, editing, plotting)
- [ ] Parallel execution reduces sequential token accumulation
- [ ] Validation cascades catch errors early (cheaper than debugging late)
- [ ] Claude orchestrates efficiently without redundant context

---

## QUALITY ASSURANCE CHECKPOINTS

### Critical Validation Gates

**GATE 1: After Step 1.3 (Design Spec Complete)**
- All parameters extracted from literature
- Cross-references validated
- Ready to begin geometry building
- **HOLD POINT:** Claude reviews and approves before Phase 2

**GATE 2: After Step 2.6 (Pre-Execution Validation)**
- All validators pass
- Input file syntax perfect
- Geometry verified
- **HOLD POINT:** Claude reviews validation reports before first run

**GATE 3: After Step 2.8 (Phase 1 Complete)**
- Model runs successfully
- keff reasonable (0.99-1.03)
- Convergence achieved
- **HOLD POINT:** Claude assesses if ready for refinement

**GATE 4: After Step 3.5 (Pre-Benchmark Run)**
- All refinements complete
- Validators pass
- Benchmark-ready
- **HOLD POINT:** Claude approves benchmark execution

**GATE 5: After Step 3.6 (Benchmark Complete)**
- keff matches target ± 0.00003
- All success criteria met
- **HOLD POINT:** Claude declares validation success

---

## COMMUNICATION & COORDINATION PROTOCOLS

### Agent-to-Agent Communication

When agents need to share information:

1. **Via Claude Orchestration (PRIMARY):**
   ```
   Agent A completes → Output to Claude → Claude analyzes → Passes to Agent B
   ```

2. **Via Shared Files (SECONDARY):**
   ```
   Agent A writes results to file → Agent B reads file → Validates
   ```

### Skill-to-Agent Communication

1. **Skill outputs reviewed by Claude, then:**
   - Claude invokes agent for validation
   - Agent receives context about what skill produced
   - Agent validates and reports back

### Cross-Validation Protocol

For critical outputs (geometry, materials, physics):

1. **Builder creates** (Skill or Agent)
2. **Claude reviews** (sanity check)
3. **Validator checks** (Agent)
4. **Claude approves** (final gate)
5. **Proceed to next step**

---

## SUCCESS CRITERIA SUMMARY

### Phase 1 Success
- ✓ MCNP runs without fatal errors
- ✓ Zero lost particles
- ✓ keff = 0.99-1.03
- ✓ Shannon entropy converges
- ✓ All lattice cells defined (1,140 channels)
- ✓ All validators pass

### Phase 2 Success
*(Currently Phase 3 in implementation)*
- ✓ keff = 1.02132 ± 0.00003
- ✓ C-E discrepancy = 2.154%
- ✓ All dimensions match benchmark
- ✓ All materials match benchmark
- ✓ Statistical quality excellent

### Integration Success
- ✓ All 15 skills tested
- ✓ All 17 agents tested
- ✓ All 8 integration patterns demonstrated
- ✓ Token efficiency targets met
- ✓ Quality gates all passed
- ✓ Production-ready model created

---

## DELIVERABLES

### Phase 1 Deliverables
1. `MSRE_Design_Specification_Complete.md` - Complete parameter extraction
2. `msre_phase1_model.inp` - Working MCNP input file
3. `Phase1_Validation_Report.md` - All validation results
4. `Phase1_Results.md` - keff, plots, analysis

### Phase 2 Deliverables
*(Phase 3 in implementation)*
1. `msre_benchmark_model.inp` - Benchmark-quality input
2. `Phase3_Refinements_Log.md` - All changes from Phase 1
3. `Phase3_Benchmark_Results.md` - Final keff, C-E analysis
4. `Phase3_Geometry_Plots/` - All verification plots

### Integration Deliverables
1. `Integration_Test_Results.md` - All checkpoints with pass/fail
2. `Token_Efficiency_Report.md` - Usage analysis
3. `Skills_Agents_Coverage_Matrix.md` - What was tested
4. `Workflow_Lessons_Learned.md` - Improvements identified

---

## RISK MITIGATION

### Potential Issues & Responses

| Risk | Mitigation | Responsible Tool |
|------|-----------|------------------|
| Fatal geometry errors | Comprehensive validation before run | mcnp-geometry-checker |
| Material definition errors | Cross-section verification early | mcnp-cross-section-manager |
| Lattice fill errors | Dedicated cell checker | mcnp-cell-checker |
| Poor convergence | Statistics checker guides refinement | mcnp-statistics-checker |
| keff far from target | Systematic geometry/material review | mcnp-tech-doc-analyzer |
| Lost particles | Geometry checker finds gaps/overlaps | mcnp-geometry-checker |
| Cross-reference errors | Automated checking before run | mcnp-cross-reference-checker |

---

## EXECUTION TIMELINE ESTIMATE

**Phase 1:** 6-8 hours (human + compute time)
- Literature analysis: 1-2 hours
- Geometry building: 2-3 hours
- Validation: 1 hour
- Initial run + debug: 2 hours

**Phase 2:** 3-4 hours
*(Currently Phase 3)*
- Benchmark comparison: 1 hour
- Refinements: 1-2 hours
- Validation: 0.5 hour
- Benchmark run: 0.5-1 hour

**Phase 3:** 2-3 hours
*(Currently Phase 4)*
- Advanced features: 2-3 hours

**Total: 11-15 hours** end-to-end for complete validation

---

## CONCLUSION

This validation plan comprehensively tests:
1. ✓ All 15 MCNP skills
2. ✓ All 17 MCNP agents
3. ✓ 8 integration patterns
4. ✓ Sequential workflows
5. ✓ Parallel workflows
6. ✓ Cross-validation protocols
7. ✓ Token efficiency strategies
8. ✓ Production-quality outputs

**Success = Production-ready MSRE model matching benchmark keff within 30 pcm, created through seamless integration of all tools.**
