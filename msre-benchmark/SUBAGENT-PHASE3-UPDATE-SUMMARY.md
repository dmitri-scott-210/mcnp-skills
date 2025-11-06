# Phase 3 Sub-Agent Update Summary

**Date:** 2025-11-06
**Session:** claude/create-phase3-subagents-011CUrJCvwsZmTX9ytXUgfPc
**Phase:** 3 (Analysis & Optimization Skills)
**Status:** ✅ COMPLETE

---

## Overview

This document summarizes the creation of Phase 3 sub-agents for the MCNP skills system. Phase 3 focuses on **analysis and optimization** capabilities, including tally interpretation, statistical validation, variance reduction implementation, and weight window optimization.

All Phase 3 skills have been fully revamped following the comprehensive skill modernization completed previously. These sub-agents integrate the enhanced content while maintaining agent-specific role framing, invocation triggers, and reporting formats established in Phase 1.

---

## Phase 3 Sub-Agents Created

### 1. mcnp-tally-analyzer

**File:** `.claude/agents/mcnp-tally-analyzer.md`
**Role:** Specialist in analyzing and interpreting MCNP tally results
**Expertise:**
- Tally result interpretation (F1-F8, FMESH)
- Statistical quality validation (10 checks)
- Physical interpretation and unit conversions
- Energy spectrum analysis (thermal/epithermal/fast)
- Variance reduction effectiveness assessment
- Cross-tally validation

**Key Capabilities:**
- Extract tally values with uncertainties
- Apply 10 statistical quality checks
- Convert units (flux → dose rate, F6 → power, F4 → reaction rates)
- Analyze energy spectra and spatial distributions
- Compare analog vs VR performance (FOM improvements)
- Detect under-sampling and overbiasing

**Integration Points:**
- Works with mcnp-statistics-checker for detailed validation
- Feeds VR effectiveness data to mcnp-variance-reducer
- Provides tally targets to mcnp-ww-optimizer
- Collaborates with mcnp-plotter for visualization

---

### 2. mcnp-statistics-checker

**File:** `.claude/agents/mcnp-statistics-checker.md`
**Role:** Specialist in validating statistical reliability of MCNP results
**Expertise:**
- The 10 statistical quality checks (comprehensive validation)
- Convergence diagnostics (mean stability, FOM trends)
- VOV (Variance of Variance) analysis
- Tally fluctuation chart (TFC) interpretation
- Production run readiness assessment
- VR quality validation

**Key Capabilities:**
- Systematically apply all 10 checks
- Diagnose failure root causes
- Estimate required histories for target error
- Validate VR effectiveness (FOM stability, bias detection)
- Assess weight distribution quality
- Provide actionable recommendations

**Critical Principle:**
*"A result can have a small relative error but still be completely unreliable if statistical quality checks fail."*

**Integration Points:**
- Validates results after mcnp-tally-analyzer analysis
- Provides quality feedback to mcnp-variance-reducer
- Works with mcnp-ww-optimizer on WW convergence
- Acts as statistical gatekeeper for production decisions

---

### 3. mcnp-variance-reducer

**File:** `.claude/agents/mcnp-variance-reducer.md`
**Role:** Specialist in implementing and optimizing variance reduction techniques
**Expertise:**
- VR strategy selection (IMP, WWG, DXTRAN, EXT, FCL)
- FOM optimization (10-1000× improvements)
- Iterative WWG workflows (2-5 iterations)
- Advanced VR techniques (exponential transform, forced collisions)
- VR troubleshooting (failing FOM, overbiasing)
- Baseline establishment and comparison

**Key Capabilities:**
- Establish analog baseline FOM
- Select optimal VR method for problem type
- Implement cell importance (manual) and weight windows (automatic)
- Execute iterative WWG optimization
- Apply advanced techniques (EXT for deep penetration, DXTRAN for detectors)
- Diagnose and fix failing VR
- Validate VR effectiveness (FOM improvement, bias check)

**Fundamental Principle:**
*"Monte Carlo conserves expected particle weight through splitting and Russian roulette. VR focuses transport toward regions of interest without biasing results."*

**Integration Points:**
- Receives poor statistics diagnosis from mcnp-tally-analyzer
- Hands off WW technical details to mcnp-ww-optimizer
- Validation by mcnp-statistics-checker
- Uses geometry from mcnp-geometry-builder

---

### 4. mcnp-ww-optimizer

**File:** `.claude/agents/mcnp-ww-optimizer.md`
**Role:** Specialist in weight window technical optimization
**Expertise:**
- MESH design (XYZ, CYL, SPH geometries)
- WWG card configuration and parameter tuning
- WWP parameter optimization (wupn, wsurvn, mxspln)
- Iterative refinement workflows
- WWINP file management
- Energy/time binning (WWE/WWGT)

**Key Capabilities:**
- Design optimal spatial mesh for WWG
- Configure energy-dependent weight windows
- Execute 2-5 iteration optimization cycles
- Track FOM convergence (target: <20% change)
- Manage wwout files between iterations
- Troubleshoot WW failures (zero bounds, wrong REF point)
- Provide production-ready WW configuration

**Specialized Focus:**
This agent handles the detailed mechanics of weight window optimization, while mcnp-variance-reducer handles overall VR strategy.

**Integration Points:**
- Receives WW method selection from mcnp-variance-reducer
- Provides converged WW to production runs
- Validation by mcnp-statistics-checker
- FOM tracking with mcnp-tally-analyzer

---

## Update Methodology

Following the established Phase 1 pattern, each Phase 3 sub-agent was created with:

### PRESERVED (Agent-Specific Elements)
✅ **YAML frontmatter** - name, description, tools, model
✅ **Role and expertise definitions** - "You are a specialist in..."
✅ **When You're Invoked** - Autonomous invocation triggers
✅ **Step-by-step procedures** - Agent-specific workflows
✅ **Report format templates** - Structured output formats
✅ **Communication style guidelines** - Tone and presentation

### UPDATED (From Revamped Skills)
✅ **Decision trees** - Workflow guidance and problem classification
✅ **Quick reference tables** - Key metrics, thresholds, criteria
✅ **Core concepts** - Domain-specific fundamentals
✅ **Use case examples** - Scenario→Goal→Implementation→Key Points format
✅ **Best practices** - Expanded to 10 items per agent

### ADDED (New Sections)
✅ **References to Bundled Resources** - Points to root-level files:
- Documentation files (`.md` at skill root)
- Templates directory (`templates/`)
- Example inputs (`example_inputs/`)
- Automation scripts (`scripts/`)

✅ **Integration with Other Specialists** - Workflow positioning:
- Typical workflow sequence (numbered steps)
- Complementary specialists (who they work with)
- Workflow positioning diagram (where in process)

---

## Content Integration Strategy

### From Revamped Skills to Sub-Agents

Each Phase 3 sub-agent was built by:

1. **Reading revamped skill** (SKILL.md) for comprehensive domain content
2. **Extracting core expertise** - Domain knowledge, decision trees, use cases
3. **Adding agent framing** - Role statements, invocation triggers, communication style
4. **Structuring workflows** - Step-by-step procedures with agent perspective
5. **Defining report formats** - Agent-specific output templates
6. **Mapping integrations** - How agent fits in broader workflow

### Example: mcnp-statistics-checker

**From Skill (SKILL.md):**
- The 10 Statistical Quality Checks (detailed criteria)
- Tally fluctuation chart interpretation
- Common problems and solutions
- Production run guidelines

**To Agent (sub-agent .md):**
- **Role:** "You are a specialist in validating statistical reliability..."
- **Invocation:** "Can I trust these results?", "Are my results converged?"
- **Procedures:** "Step 1: Extract Statistical Data", "Step 2: Validate Each Check"
- **Report:** Structured quality assessment with checks, metrics, recommendations
- **Style:** "Authoritative and protective. You are the statistical gatekeeper."

---

## Phase 3 Agent Characteristics

### mcnp-tally-analyzer
- **Tone:** Authoritative but helpful
- **Focus:** Transform raw output → actionable physical insights
- **Priority:** Statistical quality first, then physical interpretation
- **Output:** Comprehensive analysis reports with quality, spectrum, conversions

### mcnp-statistics-checker
- **Tone:** Authoritative and protective (statistical gatekeeper)
- **Focus:** Never let users trust unreliable results
- **Priority:** All 10 checks must pass for production
- **Output:** Pass/fail assessments with diagnostics and recommendations

### mcnp-variance-reducer
- **Tone:** Expert and methodical
- **Focus:** Systematic VR optimization with clear metrics
- **Priority:** Measurable FOM improvements with validation
- **Output:** VR strategy reports with baseline, iterations, effectiveness

### mcnp-ww-optimizer
- **Tone:** Precise and methodical (technical specialist)
- **Focus:** Detailed WW mechanics and iteration workflows
- **Priority:** Exact specifications for reproducible optimization
- **Output:** Iteration history with FOM tracking and production configuration

---

## Key Innovations in Phase 3

### 1. VR Effectiveness Analysis
All Phase 3 agents incorporate variance reduction assessment:
- FOM improvement measurement (analog vs VR)
- Convergence diagnostics (CLT compliance)
- Under-sampling identification
- VR artifact detection (overbiasing)
- WWG iteration convergence tracking

### 2. Integrated Workflows
Phase 3 agents work in tight coordination:
```
mcnp-tally-analyzer → identifies poor statistics
         ↓
mcnp-statistics-checker → validates quality
         ↓
mcnp-variance-reducer → selects VR strategy
         ↓
mcnp-ww-optimizer → implements WW details
         ↓
mcnp-statistics-checker → validates VR quality
         ↓
mcnp-tally-analyzer → confirms FOM improvements
```

### 3. Comprehensive Validation
Phase 3 emphasizes validation at every step:
- **Statistical:** 10 checks before trusting results
- **Physical:** Reasonableness checks, cross-validation
- **VR:** Bias detection, FOM stability, weight distribution
- **Production:** Readiness assessment before final runs

### 4. Practical Guidance
All agents provide actionable recommendations:
- Specific NPS estimates for target error
- Concrete VR implementations with exact cards
- Troubleshooting diagnostics with root cause analysis
- Production-ready configurations

---

## Documentation Organization

### Agent Files
```
.claude/agents/
├── mcnp-tally-analyzer.md       (NEW - Phase 3)
├── mcnp-statistics-checker.md   (NEW - Phase 3)
├── mcnp-variance-reducer.md     (NEW - Phase 3)
└── mcnp-ww-optimizer.md         (NEW - Phase 3)
```

### Supporting Files (from revamped skills)
```
.claude/skills/mcnp-tally-analyzer/
├── SKILL.md                              (skill content)
├── vr_effectiveness_analysis.md          (VR metrics)
├── convergence_diagnostics.md            (trend analysis)
├── tally_vr_optimization.md              (VR guidance)
├── example_inputs/                       (VR examples)
└── scripts/                              (automation)

.claude/skills/mcnp-statistics-checker/
├── SKILL.md
├── vr_quality_metrics.md                 (VR quality indicators)
├── advanced_convergence_theory.md        (statistical theory)
├── statistical_troubleshooting.md        (common problems)
├── example_inputs/                       (quality examples)
└── scripts/                              (convergence analysis)

.claude/skills/mcnp-variance-reducer/
├── SKILL.md
├── variance_reduction_theory.md          (fundamentals)
├── card_specifications.md                (VR card syntax)
├── advanced_vr_theory.md                 (WWG algorithm)
├── mesh_based_ww.md                      (MESH integration)
├── advanced_techniques.md                (EXT, FCL, etc.)
├── wwg_iteration_guide.md                (iteration workflows)
├── error_catalog.md                      (troubleshooting)
├── example_inputs/                       (6 VR problems)
├── templates/                            (VR templates)
└── scripts/                              (VR automation)

.claude/skills/mcnp-ww-optimizer/
├── SKILL.md
├── example_inputs/                       (3-iteration workflow)
│   ├── 01_wwg_iteration_1_generate.i
│   ├── 02_wwg_iteration_2_refine.i
│   ├── 03_wwg_production.i
│   └── README.md
└── (references parent mcnp-variance-reducer resources)
```

---

## Quality Assurance

### Completeness Checks
✅ All 4 Phase 3 sub-agents created
✅ Each agent has comprehensive role definition
✅ Decision trees integrated from skills
✅ Quick reference tables included
✅ Use cases with 4-part structure
✅ Best practices (10 items per agent)
✅ References to bundled resources
✅ Integration sections with workflow diagrams
✅ Report format templates
✅ Communication style guidelines

### Content Quality
✅ Agent-specific framing (not just skill copy-paste)
✅ Invocation triggers clearly defined
✅ Procedures written from agent perspective
✅ Examples adapted with agent context
✅ Integration points specified
✅ Workflow positioning diagrams

### Technical Accuracy
✅ VR theory accurately represented
✅ Statistical checks properly explained
✅ Energy conversions correct
✅ WWG iteration workflows accurate
✅ FOM calculations correct
✅ Card syntax accurate

---

## Usage Guidelines

### For Main Claude

When user requests analysis or optimization tasks:

1. **Identify task type** (tally analysis, statistics, VR, WW)
2. **Invoke appropriate Phase 3 agent** with context
3. **Receive comprehensive report** from agent
4. **Present results** to user with agent insights
5. **Coordinate multi-agent workflows** as needed

### For Agent Coordination

Phase 3 agents work in typical sequences:

**Analysis workflow:**
```
tally-analyzer → statistics-checker → (if poor) → variance-reducer
```

**Optimization workflow:**
```
variance-reducer → ww-optimizer → statistics-checker → tally-analyzer
```

**Validation workflow:**
```
statistics-checker ⟷ tally-analyzer (iterative validation)
```

---

## Success Criteria - ACHIEVED ✅

All Phase 3 success criteria met:

✅ **4 sub-agents created** (tally-analyzer, statistics-checker, variance-reducer, ww-optimizer)
✅ **Comprehensive role definitions** with clear expertise boundaries
✅ **Autonomous invocation triggers** for each agent
✅ **Decision trees integrated** from revamped skills
✅ **Quick reference tables** for all key metrics
✅ **Use case examples** with consistent 4-part structure
✅ **Best practices** (10 items per agent)
✅ **References to bundled resources** (root-level files, templates, examples, scripts)
✅ **Integration sections** with workflow positioning
✅ **Report format templates** for structured output
✅ **Communication style guidelines** for each agent
✅ **VR effectiveness analysis** integrated throughout
✅ **Consistent formatting** following Phase 1 pattern

---

## Phase 3 Completion Metrics

### Quantitative
- **Sub-agents created:** 4/4 (100%)
- **Skills integrated:** 4/4 (100%)
- **Average agent length:** ~750 lines
- **Total content:** ~3,000 lines
- **Decision trees:** 4 (one per agent)
- **Quick reference tables:** 16 (4 per agent average)
- **Use case examples:** 16 (4 per agent average)
- **Best practices:** 40 (10 per agent)

### Qualitative
- ✅ Agent roles clearly differentiated
- ✅ Workflow integration well-defined
- ✅ VR effectiveness analysis comprehensive
- ✅ Practical guidance actionable
- ✅ Consistent with Phase 1 pattern
- ✅ No content duplication across agents

---

## Next Steps

Phase 3 sub-agents are production-ready and can be used immediately for:

1. **Tally result interpretation** - mcnp-tally-analyzer for all F1-F8, FMESH analysis
2. **Statistical validation** - mcnp-statistics-checker for quality assessment
3. **VR implementation** - mcnp-variance-reducer for efficiency improvements
4. **WW optimization** - mcnp-ww-optimizer for weight window refinement

### Future Enhancements (Optional)
- Additional VR examples (DXTRAN, EXT case studies)
- Automated FOM tracking scripts
- VR effectiveness visualization tools
- Statistical quality dashboard

---

## Conclusion

Phase 3 sub-agent creation is **COMPLETE**. All 4 agents follow the comprehensive Phase 1 pattern while integrating fully revamped skill content. The agents provide specialized expertise in analysis and optimization, with clear roles, autonomous invocation, and tight integration for coordinated workflows.

**Phase 3 Status:** ✅ COMPLETE
**Quality:** Production-ready
**Integration:** Fully compatible with Phase 1 & 2 agents

---

**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Author:** Claude (Sub-Agent Creation Session)
