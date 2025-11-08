# MCNP Hierarchical Agent Architecture - Project Plan

**Project**: Convert 35 MCNP skills into a 3-tier hierarchical agent system
**Status**: In Progress - Creating specialist agents and mega-agents
**Last Updated**: 2025-11-04

---

## Executive Summary

### Goal
Create a hierarchical agent system where **mega-agents** (Lead Developers) orchestrate **specialist agents** (Junior Developers) to provide comprehensive MCNP analysis with parallel execution capabilities.

### The Breakthrough Insight
- **Problem**: Agents cannot invoke skills via Skill tool
- **Solution**: Convert skills INTO agents (they're both Markdown + YAML frontmatter)
- **Architecture**: 3-tier hierarchy with mega-agents delegating to specialists

### Key Benefits
✅ **Preserves all 35 skills' expertise** (20,000-30,000 lines of procedures)
✅ **Enables parallelization** (mega-agents invoke multiple specialists simultaneously)
✅ **Clear delegation pattern** (Lead → Junior developer model)
✅ **Manageable complexity** (6 mega-agents vs 35 individual choices)
✅ **Real engineering workflow** (exactly how teams work in practice)

---

## Architecture Overview

### 2-Tier Orchestrated System (REVISED 2025-11-05)

```
┌─────────────────────────────────────────────────────────────────┐
│ TIER 1: Main Claude (Intelligent Orchestrator)                 │
│ - Analyzes user requests and determines workflow               │
│ - Selects appropriate specialist agents based on context       │
│ - Invokes specialists sequentially or in parallel              │
│ - Passes context between specialists in workflows              │
│ - Synthesizes results into comprehensive reports               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  │ Task tool (parallel or sequential)
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ TIER 2: Specialist Agents (35+ Domain Experts)                 │
│ - Perform focused, expert tasks                                │
│ - Each has 500-5,000 lines of procedures                       │
│ - Report findings back to Main Claude                          │
│ - Can be chained in complex workflows                          │
└─────────────────────────────────────────────────────────────────┘

EXAMPLE WORKFLOWS:

Simple (1 specialist):
  User: "Validate this input file"
  → Main Claude → mcnp-input-validator → Result

Sequential Chain (3 specialists):
  User: "Build and validate a shielding model"
  → Main Claude → mcnp-geometry-builder → input file
  → Main Claude → mcnp-material-builder → enhanced input
  → Main Claude → mcnp-input-validator → validated input

Parallel + Sequential (4 specialists):
  User: "Validate against benchmark"
  → Main Claude → mcnp-tech-doc-analyzer → benchmark specs
  → Main Claude → [mcnp-input-validator + mcnp-geometry-checker
                   + mcnp-cross-reference-checker] (parallel)
  → Main Claude synthesizes → comprehensive validation report

Complex Workflow (5+ specialists):
  User: "Optimize this deep penetration problem"
  → Main Claude → mcnp-input-validator → check validity
  → Main Claude → mcnp-variance-reducer → analyze problem
  → Main Claude → mcnp-ww-optimizer → generate weight windows
  → Main Claude → mcnp-input-editor → apply modifications
  → Main Claude → mcnp-input-validator → verify optimized input
```

**Why This Works Better**:
- ✅ Main Claude has full conversation context
- ✅ Can invoke specialists in parallel (no delegation needed)
- ✅ Can chain specialists based on workflow needs
- ✅ No agent-to-agent delegation limitation
- ✅ User gets comprehensive orchestration with intelligent routing

---

## Orchestration Patterns (Main Claude's Role)

As the intelligent orchestrator, I (main Claude) will recognize common MCNP workflow patterns and automatically chain specialists:

### Pattern 1: Benchmark Validation Workflow
**User request**: "Validate this model against the benchmark"
**My orchestration**:
1. Invoke mcnp-tech-doc-analyzer → extract benchmark specs
2. Invoke 3-4 validators in parallel → comprehensive checks
3. Synthesize → benchmark compliance report

### Pattern 2: Model Development Workflow
**User request**: "Build a reactor core model with these specifications"
**My orchestration**:
1. Invoke mcnp-geometry-builder → create geometry
2. Invoke mcnp-material-builder → add materials
3. Invoke mcnp-source-builder → define source
4. Invoke mcnp-tally-builder → add tallies
5. Invoke mcnp-input-validator → verify complete input

### Pattern 3: Optimization Workflow
**User request**: "Optimize variance reduction for this shielding problem"
**My orchestration**:
1. Invoke mcnp-input-validator → ensure valid starting point
2. Invoke mcnp-variance-reducer → analyze problem & recommend techniques
3. Invoke mcnp-ww-optimizer → generate weight windows
4. Invoke mcnp-input-editor → apply VR techniques
5. Invoke mcnp-input-validator → verify optimized input

### Pattern 4: Error Debugging Workflow
**User request**: "MCNP failed with errors, help me fix it"
**My orchestration**:
1. Invoke mcnp-output-parser → extract error messages
2. Invoke mcnp-fatal-error-debugger → diagnose and fix
3. Invoke mcnp-geometry-checker → if geometry errors
4. Invoke mcnp-cross-reference-checker → if undefined references
5. Synthesize → corrected input file

### Pattern 5: Results Analysis Workflow
**User request**: "Analyze my simulation results"
**My orchestration**:
1. Invoke mcnp-output-parser → extract tallies and data
2. Invoke mcnp-statistics-checker → verify convergence
3. Invoke mcnp-tally-analyzer → interpret physics
4. Invoke mcnp-plotter → visualize results (if needed)
5. Synthesize → comprehensive analysis report

### Pattern 6: Literature-Informed Modeling
**User request**: "Build MSRE model from this technical paper"
**My orchestration**:
1. Invoke mcnp-tech-doc-analyzer → extract geometry/materials/specs
2. Invoke mcnp-geometry-builder → build geometry from specs
3. Invoke mcnp-material-builder → create materials from compositions
4. Invoke mcnp-physics-builder → configure physics settings
5. Invoke mcnp-input-validator → verify complete model
6. Synthesize → benchmark-ready input file

**Key Advantage**: I maintain context across the entire workflow, passing results between specialists and making intelligent decisions about what to do next based on each specialist's findings.

---

## The 35+ Specialist Agents (Domain Experts)

Main Claude orchestrates these specialists based on workflow needs.

### Conversion Process: Skill → Specialist Agent

**Original Skill Format**:
```yaml
---
name: "MCNP Input Validator"
description: "..."
version: "1.0.0"
dependencies: "python>=3.8"
---
[500-5,000 lines of expert procedures]
```

**Specialist Agent Format**:
```yaml
---
name: mcnp-input-validator
description: "..."
tools: Read, Grep, Glob, Bash, SlashCommand
model: inherit
---
[500-5,000 lines of expert procedures]
+ Agent-specific instructions (role, reporting format)
```

### Validation Specialists (9 agents)

| # | Agent Name | Skill Lines | Status |
|---|------------|-------------|--------|
| 1 | mcnp-input-validator | 519 | ✅ CREATED |
| 2 | mcnp-geometry-checker | 639 | ✅ CREATED |
| 3 | mcnp-cross-reference-checker | 707 | ✅ CREATED |
| 4 | mcnp-physics-validator | ~550 | TODO |
| 5 | mcnp-cell-checker | ~600 | TODO |
| 6 | mcnp-fatal-error-debugger | ~550 | TODO |
| 7 | mcnp-warning-analyzer | ~500 | TODO |
| 8 | mcnp-best-practices-checker | ~700 | TODO |
| 9 | mcnp-statistics-checker | ~600 | TODO |

### Building Specialists (10 agents)

| # | Agent Name | Skill Lines | Status |
|---|------------|-------------|--------|
| 1 | mcnp-input-builder | ~1,200 | TODO |
| 2 | mcnp-geometry-builder | 5,085 | TODO |
| 3 | mcnp-material-builder | ~1,500 | TODO |
| 4 | mcnp-source-builder | ~1,200 | TODO |
| 5 | mcnp-tally-builder | ~2,000 | TODO |
| 6 | mcnp-physics-builder | ~1,500 | TODO |
| 7 | mcnp-lattice-builder | 3,000+ | TODO |
| 8 | mcnp-mesh-builder | ~600 | TODO |
| 9 | mcnp-burnup-builder | ~800 | TODO |
| 10 | mcnp-template-generator | ~700 | TODO |

### Editing Specialists (4 agents)

| # | Agent Name | Skill Lines | Status |
|---|------------|-------------|--------|
| 1 | mcnp-input-editor | ~600 | TODO |
| 2 | mcnp-geometry-editor | ~700 | TODO |
| 3 | mcnp-transform-editor | ~550 | TODO |
| 4 | mcnp-unit-converter | ~500 | TODO |

### Analysis Specialists (6 agents)

| # | Agent Name | Skill Lines | Status |
|---|------------|-------------|--------|
| 1 | mcnp-output-parser | ~800 | TODO |
| 2 | mcnp-mctal-processor | ~700 | TODO |
| 3 | mcnp-tally-analyzer | ~650 | TODO |
| 4 | mcnp-criticality-analyzer | ~600 | TODO |
| 5 | mcnp-statistics-checker | ~600 | TODO |
| 6 | mcnp-plotter | ~700 | TODO |

### Reference Specialists (6 agents)

| # | Agent Name | Skill Lines | Status |
|---|------------|-------------|--------|
| 1 | mcnp-isotope-lookup | ~600 | TODO |
| 2 | mcnp-cross-section-manager | ~650 | TODO |
| 3 | mcnp-physical-constants | ~500 | TODO |
| 4 | mcnp-example-finder | ~550 | TODO |
| 5 | mcnp-knowledge-docs-finder | ~500 | TODO |
| 6 | mcnp-unit-converter | ~500 | TODO |

### Optimization Specialists (4 agents)

| # | Agent Name | Skill Lines | Status |
|---|------------|-------------|--------|
| 1 | mcnp-variance-reducer | ~800 | TODO |
| 2 | mcnp-ww-optimizer | ~750 | TODO |
| 3 | mcnp-burnup-builder | ~800 | TODO |
| 4 | (future: parallel-optimizer) | TBD | FUTURE |

**Total**: **36 specialist agents** (35 from skills + 1 new cross-cutting specialist)

**Current Progress**: 5/36 agents created (14%)
- Validation specialists: 3/9 (33%) ✅
- Reference specialists: 1/6 (17%) ✅ [mcnp-tech-doc-analyzer]
- Other specialists: 0/21 (0%)

**Architecture Decision (2025-11-05)**:
- ❌ Mega-agents removed (agent-to-agent delegation doesn't work)
- ✅ Main Claude orchestrates specialists directly (intelligent routing)
- ✅ Specialists can be chained in complex workflows

---

## Implementation Plan (REVISED 2025-11-05)

### Phase 1: Validation Specialists (IN PROGRESS)
**Status**: 4/9 agents created (44%)
**Architecture**: Main Claude → Specialists (no mega-agents)

**Completed**:
1. ✅ mcnp-input-validator (540 lines) - syntax/format validation
2. ✅ mcnp-geometry-checker (650+ lines) - geometry validation
3. ✅ mcnp-cross-reference-checker (650+ lines) - cross-reference validation
4. ✅ mcnp-tech-doc-analyzer (650+ lines) - documentation analysis [NEW]

**Remaining**:
5. ⏳ mcnp-physics-validator (~550 lines)
6. ⏳ mcnp-cell-checker (~600 lines)
7. ⏳ mcnp-fatal-error-debugger (~550 lines)
8. ⏳ mcnp-warning-analyzer (~500 lines)
9. ⏳ mcnp-best-practices-checker (~700 lines)

**Testing Plan**:
- [✅] Test specialist invocation from main Claude
- [✅] Test workflow chaining (doc-analyzer → validators)
- [⏳] Test parallel invocation (3+ validators simultaneously)
- [⏳] Assess result quality vs skills architecture

**Success Criteria**:
- Main Claude can invoke specialists using Task tool ✅ VERIFIED
- Specialists perform validation using embedded procedures ✅ VERIFIED
- Main Claude synthesizes multiple specialist reports ✅ VERIFIED
- Parallel invocation works (to be tested)
- Quality equals or exceeds skill-based approach ✅ VERIFIED (9/10 quality)

---

### Phase 2: Remaining Teams (PLANNED)
**Order of creation**:

1. **Builder Team** (most complex, highest value)
   - 10 specialists, including geometry-builder (5,085 lines!)
   - Critical for input file creation

2. **Analysis Team** (high value for results interpretation)
   - 6 specialists for output analysis

3. **Reference Team** (supporting role)
   - 6 specialists for lookup tasks

4. **Editor Team** (modification tasks)
   - 4 specialists for input modifications

5. **Optimization Team** (advanced users)
   - 4 specialists for variance reduction

---

### Phase 3: Testing & Refinement
**Test scenarios**:

1. **Single specialist invocation**
   - User → Lead → Specialist → Report
   - Verify specialist uses embedded procedures

2. **Parallel specialist invocation**
   - Lead invokes 3+ specialists simultaneously
   - Verify all complete and report back

3. **Cross-team coordination**
   - Validation lead recommends builder specialist
   - Builder lead invokes validators for QA

4. **Complex multi-step workflow**
   - Build input → Validate → Run → Analyze
   - Multiple mega-agents coordinate

---

### Phase 4: Documentation & User Guide
**Deliverables**:

1. **User guide**: "How to use MCNP mega-agents"
2. **Architecture diagram**: Visual representation of 3-tier system
3. **Workflow examples**: Common use cases
4. **Specialist catalog**: Quick reference for all 35 specialists

---

## Technical Details

### Mega-Agent Structure

```yaml
---
name: mcnp-[domain]-lead
description: Lead [domain] expert coordinating N specialist agents...
tools: Task, Read, [domain-specific tools]
model: inherit
---

# Role & Responsibilities
- Orchestrator, not implementer
- Coordinates specialist team
- Synthesizes findings

# Specialist Team (list all N specialists)
- Brief description of each
- When to invoke each

# Orchestration Workflow
- Delegation logic
- Parallel invocation strategy
- Synthesis procedure

# Communication Style
- How to present results

# Example Sessions
- Demonstration of coordination
```

**Size**: 300-500 lines (orchestration logic only)

---

### Specialist Agent Structure

```yaml
---
name: mcnp-[skill-name]
description: Specialist in [specific expertise]...
tools: Read, Grep, Glob, Bash, SlashCommand
model: inherit
---

[Original skill content: 500-5,000 lines]
+ Agent-specific additions:
  - Role statement ("You are a specialist in...")
  - When invoked ("You're invoked when...")
  - Report format (standardized output structure)
  - Communication style (how to present findings)
```

**Size**: 500-5,000 lines (full skill procedures + agent wrapper)

---

### Delegation Pattern

**Mega-agent invokes specialist**:
```markdown
Task(subagent_type="mcnp-input-validator",
     description="Syntax validation",
     prompt="Validate the MCNP input file reactor.inp. Check block structure,
             syntax, format, and delimiters. Report all errors, warnings, and
             recommendations in your standard format.")
```

**Parallel invocation**:
```markdown
# Invoke multiple specialists simultaneously
Task(subagent_type="mcnp-input-validator", ...)
Task(subagent_type="mcnp-geometry-checker", ...)
Task(subagent_type="mcnp-physics-validator", ...)

[Wait for all to complete]
[Synthesize findings]
```

---

## Current Status

### Completed ✅
1. mcnp-validation-lead.md (364 lines)
2. mcnp-input-validator.md (540 lines)

### In Progress ⏳
3. Creating remaining 8 validation specialists
4. Testing delegation pattern after CLI restart

### Planned 📋
- 5 more mega-agents (builder, editor, analysis, reference, optimization)
- 34 more specialist agents
- Testing & refinement
- Documentation

---

## Testing Requirements

### Test 1: Basic Delegation (After CLI Restart)
**User request**: "Validate test-broken.inp using mcnp-validation-lead"

**Expected behavior**:
1. Validation lead receives request
2. Lead invokes mcnp-input-validator specialist
3. Specialist performs validation using embedded procedures
4. Specialist reports findings to lead
5. Lead presents synthesized report to user

**Success criteria**:
- Lead successfully invokes specialist via Task tool
- Specialist uses embedded procedures (not training knowledge)
- Report includes specialist findings
- Quality matches or exceeds previous architecture

---

### Test 2: Parallel Invocation
**User request**: "Comprehensive validation of msre-reactor.inp"

**Expected behavior**:
1. Lead identifies need for multiple specialists
2. Lead invokes 3-5 specialists in parallel
3. All specialists complete their analyses
4. Lead synthesizes all findings
5. Lead presents unified comprehensive report

**Success criteria**:
- Multiple specialists invoked in single message
- All complete and report back
- Lead successfully deduplicates findings
- Faster than sequential invocation

---

### Test 3: Cross-Team Coordination
**User request**: "Build and validate a simple shielding calculation"

**Expected behavior**:
1. User → Builder lead
2. Builder lead creates input file
3. Builder lead invokes validation lead for QA
4. Validation lead runs specialists
5. Validation reports issues → Builder lead fixes
6. Final validated input delivered

**Success criteria**:
- Builder and validator leads coordinate
- Cross-mega-agent communication works
- Final deliverable is validated and ready

---

## Success Metrics

**Quantitative**:
- All 35 specialists created: 0/35 (0%)
- All 6 mega-agents created: 1/6 (17%)
- Total lines of embedded expertise: ~500/25,000 (2%)

**Qualitative**:
- Hierarchical delegation works
- Parallel invocation successful
- Result quality high
- User experience improved

---

## Known Issues & Risks

### Issue 1: Agent Size Limits
**Risk**: Claude Code may have file size limits for agent files
**Impact**: Largest specialist (geometry-builder: 5,085 lines) may fail
**Mitigation**: Test progressively larger files; split if needed

### Issue 2: Parallel Invocation Limits
**Risk**: Unknown limit on simultaneous agent invocations
**Impact**: May not be able to invoke 9 specialists in parallel
**Mitigation**: Test limits; use sequential batches if needed

### Issue 3: Context Length
**Risk**: Specialists may hit context limits with full skill content
**Impact**: Agent may not have access to all procedures
**Mitigation**: Monitor agent performance; condense if needed

---

## Questions for Resolution

1. **File size limits?**
   - Does 500-line agent work?
   - Does 5,000-line agent work?
   - What's the maximum viable size?

2. **Parallel invocation limits?**
   - Can lead invoke 3 specialists simultaneously?
   - Can lead invoke 9 specialists simultaneously?
   - What's the practical limit?

3. **Context management?**
   - Do specialists have full access to embedded procedures?
   - Is there context pruning?
   - Does agent size affect performance?

4. **Cross-agent communication?**
   - Can mega-agents invoke other mega-agents?
   - Can specialists recommend other specialists?
   - How does coordination work?

---

## Next Session Checklist

**Before CLI restart, create**:
- [ ] Remaining 8 validation specialists
- [ ] OR test with just 2-3 specialists first

**After CLI restart, test**:
- [ ] Can mcnp-validation-lead be invoked?
- [ ] Does lead successfully invoke mcnp-input-validator?
- [ ] Does specialist use embedded procedures?
- [ ] Quality of validation report?
- [ ] Can lead invoke 2-3 specialists in parallel?

**Based on test results**:
- [ ] If successful → Create all 35 specialists
- [ ] If issues → Debug and refine
- [ ] Document findings in SUBAGENT-DEV-PROGRESS.md

---

## File Organization

```
.claude/
├── agents/
│   ├── mcnp-validation-lead.md          ✅ Mega-agent
│   ├── mcnp-input-validator.md          ✅ Specialist
│   ├── mcnp-geometry-checker.md         📋 TODO
│   ├── [... 33 more specialists]        📋 TODO
│   ├── mcnp-builder-lead.md             📋 TODO
│   ├── mcnp-editor-lead.md              📋 TODO
│   ├── mcnp-analysis-lead.md            📋 TODO
│   ├── mcnp-reference-lead.md           📋 TODO
│   └── mcnp-optimization-lead.md        📋 TODO
│
├── skills/
│   ├── mcnp-input-validator/
│   │   └── SKILL.md                     (source for specialist agent)
│   ├── [... 34 more skill directories]
│   └── [Keep all skills for reference]
│
└── settings.local.json                  (all 35 skills pre-approved)
```

**Documentation**:
- `MCNP-AGENT-ARCHITECTURE-PLAN.md` - This file (project plan)
- `SUBAGENT-DEV-PROGRESS.md` - Detailed session-by-session progress
- `README-AGENTS.md` - User guide (to be created)

---

## Revision History

| Date | Session | Changes |
|------|---------|---------|
| 2025-11-04 | 1-3 | Initial agent creation attempts, skill invocation testing |
| 2025-11-04 | 4 | Breakthrough: Hierarchical architecture designed |
| 2025-11-04 | 4 | Created validation lead + first specialist |
| 2025-11-04 | 4 | Created this project plan document |

---

**Last Updated**: 2025-11-04 Session 4
**Next Review**: After CLI restart and delegation testing
