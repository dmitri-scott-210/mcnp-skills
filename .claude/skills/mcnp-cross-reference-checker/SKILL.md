---
name: mcnp-cross-reference-checker
description: "Validates cross-references in MCNP inputs: cells→surfaces, cells→materials, tallies→cells, transformations, and universe dependencies. Use for dependency analysis."
version: "2.0.0"
dependencies: "python>=3.8, mcnp-input-validator"
---

# MCNP Cross Reference Checker

## Overview

MCNP input files contain numerous cross-references where one card references entities defined on other cards. Broken references cause FATAL errors that terminate simulations before running. This skill validates all reference relationships between cells, surfaces, materials, tallies, transformations, and universes.

Cross-reference validation is essential before running MCNP because undefined references produce immediate FATAL errors. Common issues include cells referencing non-existent surfaces, materials that aren't defined, or importance card entry counts mismatching the number of cells. These errors waste compute time and delay results.

This skill provides automated checking via Python scripts, comprehensive error catalogs with fixes, and dependency analysis tools for understanding complex input structures. It detects eight types of references and can map dependencies for lattice structures with universe hierarchies.

## When to Use This Skill

- Getting "undefined surface/material/cell" errors from MCNP
- After adding or deleting cells, surfaces, or materials (check for stale references)
- Before running modified inputs (pre-validation catches errors early)
- Working with complex lattice geometries (universe/fill dependency validation)
- Need dependency visualization (what uses which entities)
- Systematic input cleanup (identify unused surfaces/materials)
- Impact analysis before deletions (what breaks if I remove this?)
- Post-modification verification (ensure no broken references introduced)

## Decision Tree

```
User has cross-reference problem
      ↓
What type of check needed?
      ├─→ [Quick Pre-Run Check]
      │   └─→ Run: cross_reference_validator.py --mode quick
      │       └─→ Broken references found?
      │           ├─→ YES → Fix FATAL errors first (see error_catalog.md)
      │           └─→ NO → Proceed to geometry validation
      │
      ├─→ [Comprehensive Analysis]
      │   └─→ Run: mcnp_cross_reference_checker.py input.inp
      │       └─→ Generate full report:
      │           ├─→ Broken references (FATAL)
      │           ├─→ Unused entities (WARNING)
      │           └─→ Dependency statistics (INFO)
      │
      ├─→ [Dependency Mapping]
      │   └─→ Complex lattice/universe structure?
      │       ├─→ YES → Build universe hierarchy tree
      │       │          Check for circular dependencies
      │       └─→ NO → Build simple dependency graph
      │
      └─→ [Impact Analysis]
          └─→ Planning to delete entity?
              └─→ Check: What references this entity?
                  ├─→ Used → Cannot delete (FATAL errors would result)
                  └─→ Unused → Safe to delete
```

## Quick Reference

### Cross-Reference Types

| Reference Type | Source | Target | Validation | Severity |
|----------------|--------|--------|------------|----------|
| Cell → Surface | Geometry expression | Surface cards | All refs exist | FATAL |
| Cell → Material | Material field (m) | M cards | m>0 must exist | FATAL |
| Cell → Transform | TRCL parameter | TR cards | TRCL=N needs TRN | FATAL |
| Cell → Universe | FILL parameter | U parameter | FILL=N needs U=N | FATAL |
| Tally → Cell/Surf | F4/F1 card | Cell/Surface | F4:N refs exist | WARNING |
| FM → Material | FM multiplier | M cards | Material exists | WARNING |
| IMP → Cell Count | IMP entries | Cell count | Exact match | FATAL if > |
| VOL → Cell Count | VOL entries | Cell count | Exact match | WARNING if < |

### Common Errors Summary

| Error | Message | Fix |
|-------|---------|-----|
| Undefined Surface | "surface 203 in cell 10 is not defined" | Add surface 203 or correct cell geometry |
| Undefined Material | "material 5 for cell 15 is not defined" | Add M5 card or change cell material |
| IMP Mismatch | "too many entries on imp:n card" | Correct IMP entries = cell count |
| Tally Stale Ref | "cell 25 in f4 tally 4 is not defined" | Remove cell 25 from tally or add cell |
| Missing Transform | "trcl card 8 specified on cell 50 not found" | Add TR8 card |

### Validation Workflow

```
1. mcnp-input-validator     → Syntax check (basic structure)
2. mcnp-cross-reference-checker → Dependency check (THIS SKILL)
3. Fix broken references     → Critical (FATAL errors)
4. mcnp-geometry-checker     → Geometry validation
5. mcnp-physics-validator    → Physics settings
```

## Use Cases

### Use Case 1: Pre-Run Quick Validation

**Scenario:** Modified input file, need quick validation before submitting MCNP job.

**Goal:** Detect broken references in <1 minute before wasting compute time.

**Implementation:**
```bash
# Quick validation script
python scripts/mcnp_cross_reference_checker.py reactor.inp
```

**Output Interpretation:**
```
FATAL ERRORS:
  Cell 10 references undefined surface 203  → Must fix before running
  Material 5 for cell 15 not defined         → Must fix before running

WARNINGS:
  Surface 99 defined but never used          → Optional cleanup
  Material 4 defined but no cells use it     → Optional cleanup

STATISTICS:
  15 cells, 32 surfaces, 4 materials         → Informational
```

**Key Points:**
- Fix ALL FATAL errors before running (MCNP will terminate)
- WARNINGS are optional but indicate potential issues
- Run after every modification (catches errors early)
- Saves compute time (detects errors in seconds vs hours)

### Use Case 2: Undefined Surface Debugging

**Scenario:** MCNP error: "fatal error. surface 203 in cell 10 is not defined"

**Goal:** Find and fix the missing surface reference.

**Implementation:**
```python
from scripts.mcnp_cross_reference_checker import MCNPCrossReferenceChecker

checker = MCNPCrossReferenceChecker()
broken = checker.find_broken_references('input.inp')

for err in broken:
    if err['type'] == 'undefined_surface':
        print(f"Cell {err['cell']} → Surface {err['missing_surface']} MISSING")
```

**Diagnosis:**
1. Parse cell 10 geometry: `-1 2 -203 4`
2. Extract surface numbers: 1, 2, 203, 4
3. Check Surface Cards: 1✓ 2✓ 203✗ 4✓
4. Surface 203 is missing

**Fix Options:**
- **Option A:** Add surface 203 (example_inputs/01_undefined_surface_fixed.i)
- **Option B:** Correct geometry if 203 was typo (meant 3?)
- **Option C:** Remove -203 constraint if not needed

**Key Points:**
- First error in file is usually the real problem (cascading errors)
- Check for typos (203 vs 3, transposed digits)
- See error_catalog.md for complete diagnosis procedure

### Use Case 3: Impact Analysis for Deletion

**Scenario:** Want to delete surface 20, need to know what breaks.

**Goal:** Determine if deletion is safe and what needs updating.

**Implementation:**
```python
checker = MCNPCrossReferenceChecker()
graph = checker.build_dependency_graph('input.inp')

# Check what uses surface 20
if 20 in graph['surfaces_used_by']:
    cells = graph['surfaces_used_by'][20]
    print(f"⚠ Cannot delete surface 20")
    print(f"  Used by cells: {cells}")
    print(f"  Must update these cells first")
else:
    print(f"✓ Surface 20 unused - safe to delete")
```

**Impact Assessment:**
```
Surface 20 used by:
  - Cell 5 geometry: -19 20 -21
  - Cell 10 geometry: 20 -22 23
  - Tally F1: surfaces [10, 20, 30]

Required actions if deleting:
1. Modify cell 5 geometry (remove 20 constraint)
2. Modify cell 10 geometry (remove 20 constraint)
3. Remove 20 from F1 tally
```

**Key Points:**
- Always check dependencies before deletion
- Forward impact: What uses this entity?
- Backward impact: What does this entity need?
- See dependency_analysis.md for complex structures

### Use Case 4: Universe Hierarchy Validation

**Scenario:** Complex lattice with multiple universe levels, verify no circular dependencies.

**Goal:** Validate universe fill relationships and detect cycles.

**Implementation:**
```python
checker = MCNPCrossReferenceChecker()
graph = checker.build_dependency_graph('lattice.inp')

# Check universe structure
universe_fills = {}
for cell, u_data in graph.get('cells_to_universes', {}).items():
    if u_data['fills']:
        print(f"Cell {cell}: U={u_data['defined']} → FILL={u_data['fills']}")
```

**Hierarchy Visualization:**
```
Universe 0 (base):
  ├─ Cell 10 (FILL=5)
  │  │
  │  Universe 5:
  │    ├─ Cell 20 (defines U=5)
  │    └─ Cell 22 (FILL=10)
  │       │
  │       Universe 10:
  │         └─ Cell 30 (defines U=10)
```

**Circular Dependency Check:**
```python
# If Universe 5 fills Universe 10
# And Universe 10 fills Universe 5
# → CIRCULAR → BAD TROUBLE error
```

**Key Points:**
- Universe hierarchies must be acyclic (no loops)
- FILL must reference defined universe (U=N somewhere)
- See dependency_analysis.md for hierarchy algorithms

## Integration with Other Skills

**Typical Validation Pipeline:**
1. **mcnp-input-validator** → Basic syntax (three-block structure, MODE card)
2. **mcnp-cross-reference-checker** (THIS SKILL) → Dependencies validated
3. **mcnp-geometry-checker** → Overlaps, gaps, lost particles
4. **mcnp-physics-validator** → Physics settings consistency

**Complementary Skills:**
- **mcnp-input-validator:** Run before this skill (basic structure check)
- **mcnp-geometry-builder:** Create correct references from start
- **mcnp-input-editor:** Systematic modifications with reference tracking
- **mcnp-fatal-error-debugger:** Interpret MCNP error messages

**Workflow Example:**
```
Project: Modify reactor core geometry

Step 1: mcnp-input-validator  → Verify syntax OK
Step 2: mcnp-cross-reference-checker → Baseline dependencies
Step 3: Make geometry changes (add/delete cells)
Step 4: mcnp-cross-reference-checker → Re-validate
Step 5: Fix broken references
Step 6: mcnp-geometry-checker → Verify geometry
Result: Ready to run MCNP
```

## References

**Detailed Technical Specifications:**
- **reference_relationships.md** - Complete specs for all 8 reference types
- **error_catalog.md** - Common errors with diagnosis and fixes
- **dependency_analysis.md** - Graph algorithms and visualization
- **validation_procedures.md** - Step-by-step validation workflows

**Examples and Templates:**
- **example_inputs/** - Before/after pairs demonstrating errors
  - 01_undefined_surface_error.i + fixed version
  - 02_undefined_material_error.i + fixed version
  - 03_importance_mismatch_error.i + fixed version
  - Description files explain each error

**Automation Tools:**
- **scripts/mcnp_cross_reference_checker.py** - Core validation library
- **scripts/README.md** - Complete API documentation and usage examples

**External Documentation:**
- MCNP6 Manual Chapter 3.2.5.2 (Cell and surface parameter cards)
- MCNP6 Manual Chapter 4 (Input structure and limitations)
- MCNP6 Manual Chapter 5.2 (Cell cards - surface/material references)
- MCNP6 Manual Chapter 5.5 (Geometry data cards - universe/fill/transformations)
- MCNP6 Manual Chapter 5.6 (Material specification - M card numbering)
- MCNP6 Manual Chapter 5.9 (Tally specification - cell/surface references)

## Best Practices

1. **Validate After Every Modification**
   - Run cross-reference check after adding/deleting cells
   - Quick validation takes seconds, prevents hours of wasted compute
   - Automated checking in pre-run scripts

2. **Fix FATAL Errors First**
   - Broken references cause immediate termination
   - Fix in file order (first error is usually primary)
   - Re-validate after each fix (cascading errors may resolve)

3. **Check IMP Card Counts Religiously**
   - IMP entries must EXACTLY equal cell count
   - Too many = FATAL, too few = WARNING (particles killed)
   - Update IMP whenever adding/deleting cells

4. **Use Dependency Analysis Before Deletion**
   - Check what references entity before deleting
   - Assess impact on tallies, other cells
   - Safe deletion: unused surfaces/materials only

5. **Document Universe Hierarchies**
   - Complex lattices need visual diagrams
   - Verify no circular dependencies
   - Test incremental assembly (add universes gradually)

6. **Maintain Sequential Numbering**
   - Surfaces: 1, 2, 3... (easier to track)
   - Materials: M1, M2, M3... (no gaps)
   - Cells: 1, 10, 20... (logical grouping)

7. **Use Python Scripts for Large Inputs**
   - Manual checking impractical for >100 cells
   - Automated analysis finds hidden issues
   - Integrate into validation pipeline

8. **Keep Unused Entity Count Low**
   - Remove unused surfaces/materials
   - Clutters input, may indicate incomplete work
   - Clean inputs easier to modify

9. **Test Lattices Incrementally**
   - Validate base universe first
   - Add filled universes one level at a time
   - Check references at each step

10. **Version Control Inputs**
    - Track changes to cell/surface numbering
    - Roll back if references break
    - Document major restructuring

---

**END OF SKILL**
