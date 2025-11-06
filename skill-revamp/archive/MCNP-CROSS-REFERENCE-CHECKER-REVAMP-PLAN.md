# mcnp-cross-reference-checker Revamp Plan

**Session:** 20
**Date:** 2025-11-05
**Current Status:** Original skill at 708 lines (~5,000 words)
**Target:** <3,000 words with progressive disclosure structure

---

## Gap Analysis Summary

### Strengths to Preserve
- ✅ Excellent conceptual coverage of all reference types
- ✅ Good Python code examples (but should be in scripts/)
- ✅ Clear error explanations
- ✅ Comprehensive cross-reference relationship types

### Issues to Fix
- ❌ No proper directory structure (missing references/, scripts/, example_inputs/)
- ❌ SKILL.md too long (~5,000 words vs <3,000 target)
- ❌ All Python code embedded in SKILL.md
- ❌ References wrong path format (`.claude/commands/` doesn't exist)
- ❌ No example files showing reference errors
- ❌ Verbose content that should be extracted

---

## Revamp Steps

### Step 5: Extract Content to Root-Level Reference Files

Create these files at `.claude/skills/mcnp-cross-reference-checker/`:

1. **reference_relationships.md** (~2,500 words)
   - Cell → Surface references (with parsing details)
   - Cell → Material references
   - Tally → Cell/Surface references
   - Importance card → Cell count matching
   - Transformation references (TRCL)
   - Universe and Fill references
   - FM card → Material references
   - All technical specifications from Chapter 5

2. **error_catalog.md** (~2,000 words)
   - Common cross-reference errors (7 types)
   - Error messages and meanings
   - Fix procedures for each error type
   - Cascading error detection
   - Troubleshooting flowchart

3. **dependency_analysis.md** (~1,800 words)
   - Dependency graph building algorithms
   - Unused entity detection
   - Visualization formats
   - Hierarchical universe structure mapping
   - Complex lattice dependency tracing

4. **validation_procedures.md** (~1,500 words)
   - Step-by-step validation workflow
   - Quick vs comprehensive checking
   - Pre-modification verification
   - Post-modification verification
   - Integration with other validation skills

### Step 6: Add Example Files to example_inputs/

Create `.claude/skills/mcnp-cross-reference-checker/example_inputs/`:

**Before/After Pairs (3 pairs = 6 files):**

1. **01_undefined_surface_error.i** + **01_undefined_surface_fixed.i**
   - Demonstrates: Cell references undefined surface
   - Error: "cell 10 references undefined surface 203"
   - Fix: Add surface 203 definition

2. **02_undefined_material_error.i** + **02_undefined_material_fixed.i**
   - Demonstrates: Cell uses undefined material
   - Error: "material 5 not found"
   - Fix: Add M5 material card

3. **03_importance_mismatch_error.i** + **03_importance_mismatch_fixed.i**
   - Demonstrates: IMP card has wrong number of entries
   - Error: "IMP:N has 4 entries but 7 cells exist"
   - Fix: Correct IMP card to have 7 entries

**Description Files (3 files):**
- 01_description.txt
- 02_description.txt
- 03_description.txt

**Total:** 9 example files

### Step 7: Create Scripts in scripts/

Create `.claude/skills/mcnp-cross-reference-checker/scripts/`:

1. **mcnp_cross_reference_checker.py** (~400 lines)
   - MCNPCrossReferenceChecker class
   - build_dependency_graph() method
   - find_broken_references() method
   - detect_unused_entities() method
   - validate_universe_hierarchy() method

2. **dependency_visualizer.py** (~200 lines)
   - Generate text-based dependency graphs
   - Create hierarchical universe trees
   - Export to DOT format for Graphviz
   - Simple ASCII art visualization

3. **cross_reference_validator.py** (~250 lines)
   - CLI tool for quick validation
   - Reads input file, runs all checks
   - Generates comprehensive report
   - Integrates with workflow

4. **reference_fixer.py** (~150 lines)
   - Automated fix suggestions
   - Safe reference renumbering
   - Unused entity removal
   - Backup before modifications

5. **README.md** (~300 lines)
   - Usage guide for all scripts
   - Installation instructions
   - Example workflows
   - API documentation

**Total:** 5 files in scripts/

### Step 8: Streamline SKILL.md

**Target Structure (~2,500 words):**

```markdown
---
name: mcnp-cross-reference-checker
description: "Validates cross-references in MCNP inputs: cells→surfaces, cells→materials, tallies→cells, transformations, and universe dependencies. Use for dependency analysis."
version: "2.0.0"
dependencies: "mcnp-input-validator, mcnp-geometry-builder"
---

# MCNP Cross Reference Checker

## Overview
[3 paragraphs: what, why, when]

## When to Use This Skill
[6-8 bulleted trigger conditions]

## Decision Tree
[ASCII workflow diagram]

## Quick Reference
[Table: Reference Type | Source | Target | Validation Rule]

## Use Cases (4 cases)
### Use Case 1: Undefined Surface Detection
**Scenario:** ...
**Implementation:** [Concise code/procedure]
**Key Points:** ...

### Use Case 2: Material Reference Validation
### Use Case 3: Importance Card Count Check
### Use Case 4: Universe Dependency Analysis

## Integration with Other Skills
[Workflow connections]

## References
- Reference relationships: See `reference_relationships.md`
- Error catalog: See `error_catalog.md`
- Dependency analysis: See `dependency_analysis.md`
- Validation procedures: See `validation_procedures.md`
- Scripts: See `scripts/README.md`
- Examples: See `example_inputs/`

## Best Practices
[10 numbered items]
```

**Content Reduction:**
- Extract all detailed reference types → reference_relationships.md
- Extract all error descriptions → error_catalog.md
- Extract all Python code → scripts/
- Condense use cases to essential workflow
- Keep only high-level decision tree

**Current:** ~5,000 words → **Target:** ~2,500 words (50% reduction)

### Step 9: Validate Quality (26-Item Checklist)

**YAML Frontmatter (5 items):**
- [ ] 1. Name matches directory name
- [ ] 2. Description is third-person and trigger-specific
- [ ] 3. No non-standard fields
- [ ] 4. Version "2.0.0"
- [ ] 5. Dependencies include mcnp-input-validator

**SKILL.md Structure (10 items):**
- [ ] 6. Overview section (2-3 paragraphs)
- [ ] 7. "When to Use" with conditions
- [ ] 8. Decision tree diagram
- [ ] 9. Quick reference table
- [ ] 10. 4 use cases with format
- [ ] 11. Integration section
- [ ] 12. References section
- [ ] 13. Best practices (10 items)
- [ ] 14. Word count <3,000
- [ ] 15. No duplication with reference files

**Bundled Resources (8 items):**
- [ ] 16. 4 reference .md files at root level
- [ ] 17. Large content extracted
- [ ] 18. scripts/ directory exists
- [ ] 19. Python modules functional
- [ ] 20. example_inputs/ has 9 files (at root)
- [ ] 21. No templates needed for this skill
- [ ] 22. Each example has description
- [ ] 23. **CRITICAL:** NO assets/ directory (ZERO TOLERANCE)

**Content Quality (3 items):**
- [ ] 24. All code examples valid
- [ ] 25. Cross-references accurate
- [ ] 26. Documentation references correct

### Step 10: Test Skill
- Invoke skill with Claude Code
- Verify reference .md files load from root
- Test scripts execute
- Verify examples accessible

### Step 11: Update Status Document
- Move to "Completed Skills" in PHASE-1-PROJECT-STATUS-PART-6.md
- Update progress: 14/16 (87.5%)

---

## Token Estimate

- Step 5 (Extract): ~8k tokens (4 reference files, parallel writes)
- Step 6 (Examples): ~3k tokens (9 files with descriptions)
- Step 7 (Scripts): ~5k tokens (5 Python files)
- Step 8 (Streamline): ~3k tokens
- Step 9 (Validate): ~1k tokens
- **Total:** ~20k tokens

**Remaining after this skill:** ~90k tokens for 2 more skills

---

## Integration Points

**Dependencies:**
- mcnp-input-validator (basic syntax check first)
- mcnp-geometry-builder (understand reference patterns)

**Used by:**
- mcnp-geometry-checker (comprehensive validation)
- Users modifying complex inputs

**Workflow Position:**
```
input-validator → cross-reference-checker → geometry-checker → physics-validator
```

---

**END OF REVAMP PLAN**
