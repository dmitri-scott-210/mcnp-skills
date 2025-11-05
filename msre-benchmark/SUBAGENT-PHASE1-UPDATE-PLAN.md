# Phase 1 Sub-Agent Update Plan

**Created:** 2025-11-05
**Purpose:** Update sub-agents developed from Phase 1 skills to align with newly revamped skills
**Status:** In Progress

---

## Executive Summary

**Situation:**
- 9 sub-agents were created from Phase 1 skills BEFORE those skills were revamped
- All 16 Phase 1 skills have now been revamped per PHASE-1-MASTER-PLAN.md
- Sub-agents need to be updated to incorporate improvements from revamped skills

**Approach:**
- Systematically update each of the 9 Phase 1 sub-agents
- Preserve agent-specific structure (role, invocation, reporting)
- Incorporate improvements from revamped skills (decision trees, quick refs, bundled resources)
- Maintain 2-tier architecture (Main Claude → Specialists)

---

## Phase 1 Sub-Agents Requiring Updates (9 Total)

### Building Specialists (7 sub-agents)
1. **mcnp-input-builder** - Create MCNP input files from scratch
2. **mcnp-geometry-builder** - Build geometry with cells, surfaces, Boolean ops
3. **mcnp-material-builder** - Create material definitions (M/MT/MX cards)
4. **mcnp-source-builder** - Define sources (SDEF/KCODE)
5. **mcnp-tally-builder** - Create tallies (F1-F8, FM, energy bins)
6. **mcnp-physics-builder** - Configure physics (MODE/PHYS/CUT/TMP)
7. **mcnp-lattice-builder** - Build repeated structures (U/LAT/FILL)

### Validation Specialists (2 sub-agents)
8. **mcnp-cell-checker** - Validate universe/lattice/fill correctness
9. **mcnp-physics-validator** - Validate physics settings

---

## Sub-Agent Structure (Current)

### YAML Frontmatter
```yaml
---
name: mcnp-[skill-name]
description: "Agent-specific description for Task tool routing"
tools: Read, Write, Edit, Grep, Glob, Bash, SlashCommand
model: inherit
---
```

### Content Sections (Agent-Specific)
1. **Role Statement** - "You are a specialist in..."
2. **Your Expertise** - Domain knowledge overview
3. **When You're Invoked** - Trigger conditions
4. **Approach** - Quick/comprehensive/specific modes
5. **Step-by-Step Procedures** - Systematic workflow
6. **Common Issues** - Error patterns and solutions
7. **Report Format** - Standardized output template
8. **Communication Style** - How to present findings

---

## Revamped Skill Structure (v2.0.0)

### YAML Frontmatter
```yaml
---
name: mcnp-[skill-name]
version: "2.0.0"
description: "Skill-specific description"
triggers: [optional list]
---
```

### Content Sections (Anthropic Standards)
1. **Overview** - What/why/when paragraphs
2. **When to Use This Skill** - Bulleted trigger conditions
3. **Decision Tree** - ASCII art workflow
4. **Quick Reference** - Tables with essential info
5. **Core Concepts** - Key principles (for some skills)
6. **Use Cases** - 3-5 examples with increasing complexity
7. **Integration with Other Skills** - Workflow connections
8. **References** - Bundled resources (templates/, example_inputs/, scripts/)
9. **Best Practices** - 10 numbered items

---

## Update Methodology

### For Each Sub-Agent:

#### Step 1: Read Both Files
- `.claude/agents/mcnp-[name].md` (current sub-agent)
- `.claude/skills/mcnp-[name]/SKILL.md` (revamped skill)

#### Step 2: Identify Improvements
Extract from revamped skill:
- [ ] New/improved decision trees
- [ ] Updated quick reference tables
- [ ] Core concepts (if present)
- [ ] Enhanced use cases
- [ ] Integration points with other skills
- [ ] References to bundled resources (templates, examples, scripts)
- [ ] Updated best practices
- [ ] Improved step-by-step procedures

#### Step 3: Preserve Agent Elements
Keep from current sub-agent:
- [ ] YAML frontmatter with tools and model fields
- [ ] "When You're Invoked" agent-specific language
- [ ] Report format templates
- [ ] Communication style guidelines
- [ ] Agent role framing

#### Step 4: Merge Content
Update sub-agent with:
1. **Keep:** Agent frontmatter (tools, model)
2. **Update:** Role/expertise with core concepts from skill
3. **Keep:** "When You're Invoked" section (may enhance with skill triggers)
4. **Add:** Decision tree from revamped skill
5. **Add/Update:** Quick reference tables from skill
6. **Update:** Step-by-step procedures with skill improvements
7. **Add:** References to bundled resources (at root level)
   - templates/ directory (NOT assets/templates/)
   - example_inputs/ directory (NOT assets/example_inputs/)
   - scripts/ directory
   - Reference .md files (at root level, NOT references/ subdirectory)
8. **Update:** Integration section with skill cross-references
9. **Keep/Update:** Report format template
10. **Keep:** Communication style

#### Step 5: Verify Bundled Resources
For each sub-agent, check that revamped skill has:
- [ ] templates/ at root level (if applicable)
- [ ] example_inputs/ at root level with 5-10 examples
- [ ] scripts/ subdirectory (if applicable)
- [ ] Reference .md files at root (NOT in references/ or assets/)
- [ ] NO assets/ directory exists

Update sub-agent to reference these correctly:
```markdown
## References

**Templates:**
- Basic template: `templates/basic_template.i`
- Advanced template: `templates/advanced_template.i`

**Example Inputs:**
- See `example_inputs/` directory for 8 validated examples
- Example 1: `example_inputs/example_01_simple.i`

**Automation Scripts:**
- See `scripts/README.md` for usage
- Script 1: `scripts/[script-name].py`

**Detailed References:**
- Card specifications: `card_specifications.md`
- Theory background: `theory_background.md`
```

#### Step 6: Validate Quality
Checklist:
- [ ] Agent frontmatter preserved (tools, model)
- [ ] Role and expertise updated
- [ ] Decision tree added/updated
- [ ] Quick reference tables current
- [ ] Procedures reflect skill improvements
- [ ] Bundled resources referenced (at root level)
- [ ] Integration points documented
- [ ] Report format maintained
- [ ] No references to assets/ or references/ subdirectories
- [ ] File compiles without errors

---

## Key Improvements to Incorporate

### From All Revamped Skills:

#### 1. Decision Trees
All revamped skills now have ASCII art decision trees showing:
- Problem type selection
- Complexity assessment
- Template selection
- Validation flow
- Integration with other skills

**Action:** Add decision tree section to each sub-agent

#### 2. Quick Reference Tables
Comprehensive tables with:
- Card syntax
- Parameter options
- Examples
- Common values

**Action:** Update/add quick reference section

#### 3. Bundled Resources
All skills now have:
- `templates/` at root level
- `example_inputs/` at root level (5-10 examples)
- `scripts/` subdirectory (if applicable)
- Reference `.md` files at root (NOT in subdirectories)

**Action:** Update References section to point to these resources

#### 4. Integration Mapping
Skills now document:
- Prerequisite skills
- Complementary skills
- Typical workflows
- Cross-references

**Action:** Add/update Integration section

#### 5. Use Cases
Skills now have 3-5 use cases with:
- Scenario description
- Goal
- Approach
- Implementation
- Key points
- Expected results

**Action:** May incorporate into procedures or examples

---

## Specific Updates by Sub-Agent

### 1. mcnp-input-builder
**Revamped skill location:** `.claude/skills/mcnp-input-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for problem type selection
- Quick reference table for essential cards
- Templates: `basic_fixed_source_template.i`, `kcode_criticality_template.i`, etc.
- Example inputs: 8 examples from simple to complex
- Integration with: geometry-builder, material-builder, source-builder, tally-builder
- Formatting rules section (3-block structure, continuation, comments)

**Bundled resources to reference:**
- `templates/` - 4 problem-type templates
- `example_inputs/` - 8 complete example files
- `input_formatting_rules.md` - Detailed formatting reference
- `common_errors.md` - Fatal error catalog

### 2. mcnp-geometry-builder
**Revamped skill location:** `.claude/skills/mcnp-geometry-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for geometry complexity
- Core concepts: CSG, surface sense, Boolean operators
- Quick reference: Cell/surface formats, Boolean operators
- Surface type hierarchy (planes → spheres → cylinders → macrobodies)
- Integration with: geometry-editor, lattice-builder, cell-checker

**Bundled resources to reference:**
- `templates/` - Basic geometry templates
- `example_inputs/` - 10 geometry examples (simple → complex)
- `surface_types.md` - Comprehensive surface catalog
- `boolean_operations.md` - Boolean logic guide
- `macrobodies.md` - Macrobody reference

### 3. mcnp-material-builder
**Revamped skill location:** `.claude/skills/mcnp-material-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for material type selection
- ZAID format reference
- Density calculation methods
- Thermal scattering (MT card) usage
- Integration with: physics-builder (TMP consistency)

**Bundled resources to reference:**
- `templates/` - Material library templates
- `example_inputs/` - Common material definitions
- `zaid_reference.md` - ZAID format guide
- `thermal_scattering.md` - MT card reference
- `scripts/material_library_builder.py`

### 4. mcnp-source-builder
**Revamped skill location:** `.claude/skills/mcnp-source-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree: Fixed-source vs criticality
- SDEF vs KCODE decision logic
- Distribution types (SI/SP/SB cards)
- Energy, spatial, directional distributions
- Integration with: input-builder, physics-builder

**Bundled resources to reference:**
- `templates/` - Source definition templates
- `example_inputs/` - Source examples (point, distributed, KCODE)
- `distribution_types.md` - SI/SP/SB reference
- `scripts/distribution_generator.py`

### 5. mcnp-tally-builder
**Revamped skill location:** `.claude/skills/mcnp-tally-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for tally type selection (F1-F8)
- Quick reference: Tally types, units, applications
- Energy binning strategies
- FM multiplier usage
- Dose function (DE/DF) setup
- Integration with: mesh-builder (FMESH), variance-reducer

**Bundled resources to reference:**
- `templates/` - Tally templates for each type
- `example_inputs/` - Tally examples with energy bins, FM, DE/DF
- `tally_types.md` - F1-F8 comprehensive reference
- `dose_functions.md` - DE/DF catalog
- `scripts/energy_bin_generator.py`
- `scripts/dose_function_builder.py`

### 6. mcnp-physics-builder
**Revamped skill location:** `.claude/skills/mcnp-physics-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for particle type and physics models
- MODE card first (mandatory)
- PHYS card options by particle
- Energy cutoffs (CUT cards)
- Temperature-dependent cross sections (TMP cards)
- Integration with: material-builder (TMP consistency)

**Bundled resources to reference:**
- `templates/` - Physics configuration templates
- `example_inputs/` - Physics examples (neutron, photon, coupled)
- `physics_models.md` - PHYS card reference
- `energy_cutoffs.md` - CUT card guide

### 7. mcnp-lattice-builder
**Revamped skill location:** `.claude/skills/mcnp-lattice-builder/SKILL.md`

**Key improvements to incorporate:**
- Decision tree: Rectangular (LAT=1) vs Hexagonal (LAT=2)
- Universe hierarchy (3-level typical)
- FILL array specifications
- Lattice boundary conditions
- Integration with: geometry-builder (universes), cell-checker (validation)

**Bundled resources to reference:**
- `templates/` - Lattice templates (rectangular, hexagonal)
- `example_inputs/` - Lattice examples (simple → reactor core)
- `universe_hierarchy.md` - U/LAT/FILL guide
- `hexagonal_lattice.md` - LAT=2 reference
- `scripts/universe_tree_builder.py`
- `scripts/fill_array_generator.py`

### 8. mcnp-cell-checker
**Revamped skill location:** `.claude/skills/mcnp-cell-checker/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for validation approach
- U/FILL reference validation
- LAT specification checking
- Fill array dimension verification
- Circular reference detection
- Integration with: lattice-builder, geometry-checker

**Bundled resources to reference:**
- `example_inputs/` - Test cases with errors
- `common_errors.md` - Universe/lattice error catalog
- `scripts/mcnp_cell_checker.py`
- `scripts/universe_tree_visualizer.py`

### 9. mcnp-physics-validator
**Revamped skill location:** `.claude/skills/mcnp-physics-validator/SKILL.md`

**Key improvements to incorporate:**
- Decision tree for physics validation
- MODE card validation (must be first)
- PHYS card consistency checks
- Cross-section library verification
- Energy cutoff validation
- Integration with: physics-builder, material-builder (TMP)

**Bundled resources to reference:**
- `example_inputs/` - Physics validation test cases
- `physics_errors.md` - Common physics errors
- `scripts/physics_consistency_checker.py`

---

## Update Execution Plan

### Session 1: Update Building Specialists (7 agents)
**Order:**
1. mcnp-input-builder (most foundational)
2. mcnp-geometry-builder (high priority)
3. mcnp-material-builder
4. mcnp-source-builder
5. mcnp-tally-builder
6. mcnp-physics-builder
7. mcnp-lattice-builder

**Per agent:**
- Read current agent + revamped skill
- Identify improvements
- Update agent file
- Verify bundled resources
- Test compilation

### Session 2: Update Validation Specialists (2 agents)
**Order:**
8. mcnp-cell-checker
9. mcnp-physics-validator

**Per agent:**
- Same process as building specialists

### Session 3: Validation & Documentation
- Test all updated agents
- Create update summary
- Commit and push
- Update progress tracking

---

## Success Criteria

### Per Sub-Agent:
- [ ] Agent frontmatter preserved (tools, model)
- [ ] Content updated with skill improvements
- [ ] Decision tree added/updated
- [ ] Quick reference current
- [ ] Bundled resources referenced correctly (at root level)
- [ ] NO references to assets/ or references/ subdirectories
- [ ] Integration points documented
- [ ] Report format maintained
- [ ] File compiles without errors

### Overall:
- [ ] All 9 Phase 1 sub-agents updated
- [ ] Consistency across agents maintained
- [ ] Architecture documentation updated
- [ ] Changes committed to git
- [ ] Update summary created

---

## Notes

### Sub-Agents NOT Being Updated (Not Phase 1)
These will be updated after their skills are revamped:
- mcnp-best-practices-checker (validation, not Phase 1)
- mcnp-burnup-builder (advanced, Phase 3+)
- mcnp-fatal-error-debugger (debugging, not Phase 1)
- mcnp-mesh-builder (advanced, Phase 3+)
- mcnp-template-generator (may be Phase 1, verify)
- mcnp-warning-analyzer (debugging, not Phase 1)

### Architecture Notes
- Maintaining 2-tier: Main Claude → Specialists
- No mega-agents (delegation doesn't work)
- Specialists can be invoked in parallel or sequential chains
- Main Claude performs intelligent orchestration

---

**Status:** Ready to begin updating
**Next Step:** Update mcnp-input-builder sub-agent
