---
name: "mcnp-cell-checker"
description: "Validates MCNP cell cards for universe, lattice, and fill correctness. Checks U/FILL references, LAT specifications, fill array dimensions, and nesting hierarchy. Use for repeated structures validation."
version: "2.0.0"
dependencies: "python>=3.8, mcnp-geometry-builder, mcnp-lattice-builder"
---

# MCNP Cell Checker

## Overview

Cell cards in MCNP can contain complex repeated structure features (universes, lattices, fill arrays) that create multi-level geometry hierarchies. Errors in these features are difficult to debug and often cause fatal errors from undefined universe references, dimension mismatches in fill arrays, invalid lattice type specifications, circular universe dependencies, or deep nesting causing performance issues.

This skill provides specialized validation for cell-specific features: universe definition/reference checking (U/FILL), lattice type validation (LAT=1 or LAT=2), fill array dimension validation, nesting hierarchy analysis, and lattice boundary surface validation. It complements general input validation by focusing specifically on the complex universe and lattice systems used in reactor modeling and repeated geometry structures.

Use this skill after creating lattices with mcnp-lattice-builder, before production runs, when debugging universe errors, for complex repeated structures, or when nesting exceeds 3-4 levels. The validation procedures catch errors that would otherwise cause MCNP fatal errors during execution.

## When to Use This Skill

- User mentions "universe", "lattice", or "fill" errors in MCNP
- User asks about repeated structures or "u=" parameter issues
- User reports "undefined universe" or "fill array mismatch" errors
- Building reactor cores, fuel assemblies, or TRISO particle models
- Cells contain `lat=` or `fill=` parameters with arrays
- Debugging "lost particles" in lattice cells
- Checking universe hierarchy depth or circular references
- Validating geometry after mcnp-lattice-builder usage
- Pre-production validation for complex geometries
- Performance issues suspected from deep universe nesting

## Decision Tree

```
User Request → Validation Scope Selection
  |
  +--> Quick universe check
  |    └─> Verify all FILL references defined
  |        └─> scripts/validate_cells_prerun.py (Step 1 only)
  |
  +--> Full cell validation (recommended)
  |    ├─> Universe references (U/FILL)
  |    ├─> Lattice specifications (LAT=1 or LAT=2)
  |    ├─> Fill array dimensions
  |    ├─> Dependency tree (circular refs, depth)
  |    └─> Lattice boundaries
  |        └─> scripts/validate_cells_prerun.py (all steps)
  |
  +--> Lattice-only check
  |    ├─> LAT/FILL array validation
  |    └─> Boundary surface appropriateness
  |        └─> scripts/fill_array_validator.py
  |
  +--> Dependency mapping
  |    ├─> Build universe tree
  |    ├─> Detect circular references
  |    └─> Analyze nesting depth
  |        └─> scripts/universe_tree_visualizer.py
  |
  └─-> Specific cell deep dive
       └─> Single cell detailed analysis
           └─> Python API: MCNPCellChecker methods
```

## Quick Reference

### Validation Types

| Type | What It Checks | When to Use | Script |
|------|----------------|-------------|--------|
| **Universe References** | All `fill=N` have `u=N` | Undefined universe errors | validate_cells_prerun.py |
| **Lattice Types** | LAT=1 or LAT=2 only | Invalid LAT value errors | validate_cells_prerun.py |
| **Fill Arrays** | Array size matches declaration | Dimension mismatch errors | fill_array_validator.py |
| **Dependency Tree** | No circular refs, depth OK | Circular reference errors | universe_tree_visualizer.py |
| **Boundaries** | Appropriate surfaces for LAT type | Lattice geometry issues | validate_cells_prerun.py |

### Common Problems Quick Guide

| Problem | Symptom | Quick Fix | Details |
|---------|---------|-----------|---------|
| Undefined universe | "Universe N not found" | Add `u=N` cell definition | example_inputs/01_* |
| Fill mismatch | "Array size incorrect" | Add missing values or fix range | example_inputs/02_* |
| Circular ref | "Circular dependency" | Make one universe terminal | example_inputs/03_* |
| Invalid LAT | "Invalid LAT value" | Use LAT=1 or LAT=2 only | cell_concepts_reference.md |
| Deep nesting | Slow performance | Use negative u=, combine levels | best_practices_detail.md |

## Use Cases

### Use Case 1: Undefined Universe Reference

**Scenario:** MCNP reports "Universe 50 not found" error. Fill array in lattice cell references u=50 but no cell has `u=50` definition.

**Goal:** Identify and fix undefined universe references before running MCNP.

**Implementation:**
```bash
# Run universe validation
python scripts/validate_cells_prerun.py input.inp
```

**Expected Output:**
```
[1/5] Checking universe references...
  ❌ FATAL: Undefined universe references
     Universe 50 referenced in FILL but not defined
```

**Solution:** Either add definition for u=50 or fix typo in fill array (50 → 5).

**Key Points:**
- Every `fill=N` must have corresponding `u=N` definition
- Check all values in large fill arrays carefully
- Use validation scripts before every MCNP run
- See `example_inputs/01_universe_errors_*` for complete example

---

### Use Case 2: Fill Array Dimension Mismatch

**Scenario:** Lattice cell has `fill= -7:7 -7:7 0:0` (225 values needed) but only 210 values provided. MCNP reports "fill array size incorrect".

**Goal:** Verify fill array sizes match lattice declarations exactly.

**Implementation:**
```bash
# Check fill array dimensions
python scripts/fill_array_validator.py input.inp
```

**Expected Output:**
```
Cell 200:
  Declaration: fill= -7:7 -7:7 0:0
  Dimensions: 15 × 15 × 1
  Expected: 225 values
  Actual: 210 values
  Status: ✗ Size mismatch (-15)
  ERROR: Missing 15 values
```

**Solution:** Add missing rows or correct fill declaration range. Formula: (i2-i1+1) × (j2-j1+1) × (k2-k1+1).

**Key Points:**
- Calculate expected size carefully: inclusive ranges
- Document array dimensions in comments
- Format arrays visually (one row per line)
- Use scripts to generate large arrays
- See `example_inputs/02_fill_mismatch_*` for complete example

---

### Use Case 3: Building Universe Dependency Tree

**Scenario:** Complex reactor model with many universe levels. Need to visualize hierarchy, check for circular references, and analyze nesting depth.

**Goal:** Build complete universe tree showing levels, fills, and potential issues.

**Implementation:**
```bash
# Visualize universe hierarchy
python scripts/universe_tree_visualizer.py reactor.inp -o tree.txt
```

**Expected Output:**
```
Universe Dependency Tree: reactor.inp
======================================================================
Summary:
  Total universes: 12
  Maximum depth: 6 levels
  ✓ No circular references

Hierarchy Tree:
u=0 (real world): level 0, 2 cells, fills=[1, 2]
  u=1: level 1, 3 cells, fills=[10, 20]
    u=10: level 2, 2 cells, fills=[100]
      u=100: level 3, 1 cell, fills=none
    u=20: level 2, 1 cell, fills=none
  u=2: level 1, 2 cells, fills=[30]
    u=30: level 2, 1 cell, fills=none

Performance Analysis:
  ✓ Moderate nesting (6 levels) - Acceptable performance
  💡 Consider negative universe optimization for levels 3+
======================================================================
```

**Key Points:**
- Visualize hierarchy for debugging
- Detect circular references automatically
- Identify deep nesting (>10 levels)
- Document universe purpose in input file
- See `example_inputs/03_circular_reference_*` for circular ref example

---

### Use Case 4: Pre-Production Comprehensive Validation

**Scenario:** Reactor core model ready for production run. Need comprehensive validation of all cell card features before committing computational resources.

**Goal:** Run all 5 validation procedures and verify input is error-free.

**Implementation:**
```bash
# Comprehensive pre-run validation
python scripts/validate_cells_prerun.py core_model.inp
```

**Expected Output:**
```
======================================================================
MCNP Cell Card Validation: core_model.inp
======================================================================

[1/5] Checking universe references...
  ✓ All 15 universe references valid
    15 universes defined

[2/5] Validating lattice specifications...
  ✓ All 3 lattice cells valid

[3/5] Checking fill array dimensions...
  ✓ All 3 fill arrays have correct dimensions

[4/5] Building universe dependency tree...
  ✓ No circular references
    Maximum nesting depth: 6 levels

[5/5] Checking lattice boundary surfaces...
  ✓ All 3 lattice boundaries appropriate

======================================================================
✓ CELL VALIDATION PASSED
======================================================================
Summary:
  • 15 universes defined
  • 3 lattice cells
  • 3 fill arrays
  • 6 levels of nesting

Ready for MCNP execution:
  mcnp6 i=core_model.inp
======================================================================
```

**Key Points:**
- Run before every production simulation
- All 5 validation procedures in one command
- Catches errors that would waste computational time
- Integration with MCNP workflow: `validate && mcnp6`

---

### Use Case 5: Lattice-Specific Debugging

**Scenario:** Fuel assembly lattice showing unexpected behavior. Need to focus validation on lattice cells only.

**Goal:** Quick check of lattice specifications, fill arrays, and boundary surfaces.

**Implementation:**
```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()

# Lattice validation
lattice_results = checker.validate_lattices('assembly.inp')

for cell_num, result in lattice_results.items():
    print(f"Cell {cell_num} (LAT={result['lat_type']}):")
    if result['errors']:
        for err in result['errors']:
            print(f"  ✗ {err}")
    else:
        print(f"  ✓ Valid")

# Fill array check
fill_check = checker.check_fill_dimensions('assembly.inp')

for cell_num, result in fill_check.items():
    if not result['valid']:
        print(f"Cell {cell_num}: Size mismatch")
        print(f"  Expected: {result['expected_size']}")
        print(f"  Actual: {result['actual_size']}")
```

**Key Points:**
- Focus validation on specific cell type
- Python API for programmatic access
- Useful for debugging single lattice issues
- See `python_api_reference.md` for complete API

## Integration with Other Skills

### Workflow Position

**Typical sequence:**
1. **mcnp-lattice-builder** → Create lattice structures
2. **mcnp-cell-checker** (this skill) → Validate universe/lattice/fill
3. **mcnp-geometry-checker** → Check geometry overlaps/gaps
4. **MCNP execution** → Run simulation

### Complementary Skills

**Strong integration with mcnp-lattice-builder:**
- Validates lattices created by lattice-builder
- Checks U/FILL/LAT parameters automatically
- Workflow: `lattice-builder` → `cell-checker` → `mcnp6`

**Complements mcnp-geometry-builder:**
- Geometry-builder creates cells with u= parameters
- Cell-checker validates universe references
- Both needed for complex repeated structures

**Works with mcnp-input-validator:**
- Input-validator: General syntax and structure
- Cell-checker: Specialized universe/lattice validation
- Combined: Complete input verification

### Example Complete Workflow

```bash
# Step 1: Build lattice (mcnp-lattice-builder)
# Creates input with LAT/FILL arrays

# Step 2: Validate cell cards (this skill)
python scripts/validate_cells_prerun.py reactor.inp

# Step 3: Check geometry (mcnp-geometry-checker)
# Validates overlaps, gaps, lost particles

# Step 4: Run MCNP
mcnp6 i=reactor.inp
```

## References

### Comprehensive Documentation

**Reference files** (root skill directory):
- **`cell_concepts_reference.md`** - Universe system, lattice types, nesting depth, cell parameters
- **`validation_procedures.md`** - Five detailed validation algorithms with pseudocode
- **`troubleshooting_guide.md`** - Six common problems with diagnosis and solutions
- **`best_practices_detail.md`** - Ten best practices with detailed explanations
- **`python_api_reference.md`** - Complete API documentation for MCNPCellChecker class

### Scripts and Tools

**Python validation scripts** (`scripts/` directory):
- **`mcnp_cell_checker.py`** - Main validation class library
- **`validate_cells_prerun.py`** - Comprehensive pre-run validation (all 5 procedures)
- **`universe_tree_visualizer.py`** - Hierarchy tree visualization and analysis
- **`fill_array_validator.py`** - Standalone fill array dimension checker
- **`README.md`** - Scripts usage guide and API examples

### Templates and Examples

**Templates** (`templates/` directory):
- **`validation_checklist.md`** - Pre-run validation checklist template
- **`universe_map_template.md`** - Template for documenting universe hierarchy

**Examples** (`example_inputs/` directory):
- **01_universe_errors_** (before/after + description) - Undefined universe references
- **02_fill_mismatch_** (before/after + description) - Fill array dimension mismatch
- **03_circular_reference_** (before/after + description) - Circular universe dependencies

### External Documentation

- **MCNP6 Manual Chapter 5.2:** Cell Cards - Complete cell card syntax
- **MCNP6 Manual Chapter 5.5.5:** Repeated Structures (U/LAT/FILL keywords)
- **MCNP6 Manual Chapter 3.4.1:** Best practices for geometry setup

## Best Practices

1. **Run validation before every MCNP execution** - Use `validate_cells_prerun.py` as standard practice. Catches errors before wasting computational time.

2. **Document universe hierarchy in input file** - Add comments showing universe map at top of file. Include purpose, level, fills, and filled_by for each universe.

3. **Use negative universe numbers for fully enclosed cells** - Apply `u=-N` for cells at level 3+ that are completely inside their parent. 10-30% performance improvement for deep nesting.

4. **Keep nesting depth below 10 levels** - Recommended: 1-3 levels (ideal), 4-7 levels (acceptable), 8-10 levels (caution), >10 levels (simplify geometry).

5. **Validate fill array dimensions with comments** - Document expected size: "Lattice: 15×15×1 = 225 values". Add row labels: `$ j=-7`, `$ j=-6`, etc.

6. **Check for circular references in complex geometries** - Use `universe_tree_visualizer.py` to visualize hierarchy. Detects cycles that are difficult to spot manually.

7. **Use appropriate lattice boundary surfaces** - LAT=1: RPP macrobody or 6 planes. LAT=2: RHP macrobody or 8 planes (6 P + 2 PZ). Improves lattice indexing.

8. **Pre-validate lattices created by mcnp-lattice-builder** - Always run cell-checker after lattice-builder. Workflow: `lattice-builder` → `cell-checker` → `mcnp6`.

9. **Build universe reference map for complex inputs** - Use template at `templates/universe_map_template.md`. Documents purpose, relationships, and hierarchy for maintenance.

10. **Format fill arrays for visual verification** - One row per line, aligned columns. Makes symmetry checks and counting easier. Use row labels for large arrays.

---

**END OF MCNP CELL CHECKER SKILL**
