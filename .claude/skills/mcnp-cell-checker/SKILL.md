---
name: "mcnp-cell-checker"
description: "Validates MCNP cell cards for universe, lattice, and fill correctness. Checks U/FILL references, LAT specifications, fill array dimensions, and nesting hierarchy. Use for repeated structures validation."
version: "2.0.0"
dependencies: "python>=3.8, mcnp-geometry-builder, mcnp-lattice-builder"
---

# MCNP Cell Checker

## Overview

Cell cards in MCNP can contain complex repeated structure features (universes, lattices, fill arrays) that create multi-level geometry hierarchies. Errors in these features are difficult to debug and often cause fatal errors from undefined universe references, dimension mismatches in fill arrays, invalid lattice type specifications, circular universe dependencies, or deep nesting causing performance issues.

**This skill provides specialized validation for:**
- Universe definition/reference checking (u=, fill=)
- Lattice type validation (lat=1 or lat=2 only)
- Fill array dimension validation (match array sizes to declarations)
- Nesting hierarchy analysis (build universe dependency trees)
- Circular reference detection (prevent infinite loops)
- Lattice boundary validation (check appropriate surfaces)

**When to Use:** After creating lattices, before production runs, when debugging universe errors, for complex repeated structures, when nesting exceeds 3-4 levels.

---

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User mentions "universe", "lattice", or "fill" errors
- User asks about repeated structures or "u=" parameter
- User reports "undefined universe" errors
- User mentions TRISO particles, fuel assemblies, or core lattices
- User has cells with `lat=` or `fill=` parameters
- User asks "how deep can I nest universes?"

**Context Clues:**
- "My fill array isn't working"
- "MCNP says universe not found"
- "Lost particles in lattice cells"
- "Circular reference error"

### Validation Approach

```
User request → Select scope:
├── Quick universe check → Verify all FILL references defined
├── Full cell validation → All checks (recommended)
├── Lattice-only check → LAT/FILL array validation
├── Dependency mapping → Build universe tree
└── Specific cell → Deep dive on one cell

Problem Type:
├── "Undefined universe" → Check U/FILL references
├── "Array size mismatch" → Validate FILL dimensions
├── "Invalid LAT value" → Check lattice type
├── "Lost particles" → Check lattice boundaries
├── "Circular reference" → Build dependency graph
└── "Too deep nesting" → Analyze hierarchy depth
```

---

## Tool Invocation

### Python API

```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
results = checker.check_cells('input.inp')

if results['valid']:
    print("✓ All cell cards validated")
else:
    print(f"✗ Found {len(results['errors'])} errors")
```

### Command-Line Usage

```bash
python scripts/mcnp_cell_checker.py reactor.inp
```

### Quick Validation Checks

**Universe References:**
```python
universe_check = checker.validate_universes('input.inp')
print(f"Defined: {universe_check['defined']}")
print(f"Undefined: {universe_check['undefined']}")
```

**Lattice Specifications:**
```python
lattice_results = checker.validate_lattices('input.inp')
for cell_num, result in lattice_results.items():
    if result['errors']:
        print(f"Cell {cell_num}: {result['errors']}")
```

**Fill Array Dimensions:**
```python
fill_check = checker.check_fill_dimensions('input.inp')
for cell_num, result in fill_check.items():
    if result['expected_size'] != result['actual_size']:
        print(f"Cell {cell_num}: Size mismatch")
```

**Universe Dependency Tree:**
```python
tree = checker.build_universe_tree('input.inp')
print(f"Max depth: {tree['max_depth']} levels")
if tree['circular_refs']:
    print(f"Circular references: {tree['circular_refs']}")
```

---

## Quick Reference

### Universe System (U and FILL)

| Feature | Syntax | Purpose |
|---------|--------|---------|
| **Define universe** | `u=N` | Assign cell to universe N (N > 0) |
| **Fill simple** | `fill=N` | Fill cell with all cells from universe N |
| **Fill array** | `fill=i1:i2 j1:j2 k1:k2 [IDs]` | Fill lattice with universe array |
| **Real world** | `u=0` (default) | Default universe (no u= needed) |
| **Nesting limit** | Up to 20 levels | Practical limit: 3-7 levels |

### Lattice System (LAT and FILL)

| Lattice Type | Syntax | Boundary | Elements |
|--------------|--------|----------|----------|
| **Cubic** | `lat=1` | RPP or 6 planes | Hexahedral (6 faces) |
| **Hexagonal** | `lat=2` | HEX or 6P+2PZ | Hexagonal prism (8 faces) |

### Fill Array Dimension Calculation

```
Declaration: fill= i1:i2 j1:j2 k1:k2
Required values = (i2-i1+1) × (j2-j1+1) × (k2-k1+1)

Example: fill= -7:7 -7:7 0:0
  → i: 15 values, j: 15 values, k: 1 value
  → Total: 15 × 15 × 1 = 225 universe IDs required
```

### Validation Checklist

- [ ] All `fill=N` have corresponding `u=N` definitions
- [ ] Universe 0 not explicitly used
- [ ] LAT value is 1 or 2 only
- [ ] Lattice cells are void (material 0)
- [ ] Lattice cells have FILL parameter
- [ ] Fill array size matches declaration
- [ ] No circular universe references
- [ ] Nesting depth ≤ 10 levels (recommended)
- [ ] Lattice boundaries appropriate (RPP/HEX)

---

## Common Problems & Quick Fixes

### 1. Undefined Universe Reference

**Symptom:** `FATAL: Universe 50 not found`

**Fix:** Add universe definition or correct typo
```
$ Add missing definition:
500 1 -10.5 -500 u=50 imp:n=1
```

### 2. Fill Array Size Mismatch

**Symptom:** `Expected 225 values, found 210`

**Fix:** Add missing rows or correct fill= range
```
$ Verify calculation: (i2-i1+1) × (j2-j1+1) × (k2-k1+1)
$ Add missing 15 values (one complete row)
```

### 3. Circular Universe Reference

**Symptom:** `u=1 fills u=2, u=2 fills u=1 (infinite loop)`

**Fix:** Make hierarchy linear (no loops)
```
$ BAD: u=1 → u=2 → u=1 (circular)
$ GOOD: u=1 → u=2 → u=3 (linear)
```

### 4. Invalid Lattice Type

**Symptom:** `Invalid LAT=3 (must be 1 or 2)`

**Fix:** Change to lat=1 (cubic) or lat=2 (hexagonal)
```
$ BAD: lat=3
$ GOOD: lat=1 (cubic) or lat=2 (hexagonal)
```

### 5. Lattice Cell with Material

**Symptom:** `Lattice cell should be void, has material 1`

**Fix:** Change lattice cell to void (material 0)
```
$ BAD: 200 1 -2.7 -200 lat=1 fill=5 imp:n=1
$ GOOD: 200 0 -200 lat=1 fill=5 imp:n=1
```

### 6. Deep Nesting Performance

**Symptom:** `Nesting depth is 12 levels (performance impact)`

**Fix:** Use negative u= for enclosed cells or consolidate levels
```
$ Strategy 1: Negative universe (faster)
500 1 -10.5 -500 u=-50 imp:n=1

$ Strategy 2: Consolidate levels (12 → 4)
u=1 → u=2 → u=5 → u=10
```

---

## Best Practices

1. **Universe Organization**
   - Group universe definitions logically by hierarchy level
   - Use comment headers to identify universe purpose
   - Document universe reference map at top of file

2. **Fill Array Documentation**
   - Always comment fill array dimensions
   - Include calculation: `(i2-i1+1) × (j2-j1+1) × (k2-k1+1)`
   - Mark rows with inline comments (`$ j=-7`, `$ j=-6`, etc.)

3. **Negative Universe Optimization**
   - Use `u=-N` for fully enclosed cells (performance boost)
   - WARNING: Only if cell is TRULY fully enclosed
   - Incorrect usage can cause wrong answers with no warnings

4. **Lattice Boundary Standards**
   - LAT=1 (cubic): Use RPP macrobody or 6 planes
   - LAT=2 (hexagonal): Use HEX macrobody or 6P+2PZ

5. **Universe Hierarchy Limits**
   - 1-3 levels: Ideal (minimal overhead)
   - 4-7 levels: Acceptable (common for reactors)
   - 8-10 levels: Use with caution (performance impact)
   - >10 levels: Not recommended (simplify or homogenize)

6. **Fill Array Formatting**
   - Align array visually for readability
   - One row per line (easier to count and verify)
   - Symmetric patterns make errors obvious

7. **Pre-Validation Before MCNP**
   - Always run cell checker before MCNP execution
   - Catches errors faster than waiting for MCNP run
   - Provides clearer error messages

8. **Document Universe Purpose**
   - Add purpose comments to each universe definition
   - Include: what it represents, where it's used, nesting level
   - Helps debugging complex hierarchies

9. **Validation Comments**
   - Include expected occurrences of each universe
   - Total array size verification
   - Cross-reference to other skills (lattice-builder, geometry-builder)

10. **Integration Testing**
    - Validate after building lattices with mcnp-lattice-builder
    - Combine with mcnp-geometry-checker for complete validation
    - Use with mcnp-input-validator for full input checking

---

## Integration with Other Skills

### With mcnp-input-validator

Complete validation workflow:
```python
# Step 1: General validation
from mcnp_input_validator import MCNPInputValidator
validator = MCNPInputValidator()
if not validator.validate_file('input.inp')['valid']:
    return False

# Step 2: Cell-specific validation
from mcnp_cell_checker import MCNPCellChecker
checker = MCNPCellChecker()
return checker.check_cells('input.inp')['valid']
```

### With mcnp-lattice-builder

Build and validate lattices:
```python
from mcnp_lattice_builder import MCNPLatticeBuilder
from mcnp_cell_checker import MCNPCellChecker

# Build
builder = MCNPLatticeBuilder()
lattice_cards = builder.create_lattice(**params)

# Validate immediately
checker = MCNPCellChecker()
results = checker.validate_lattices('temp.inp')
```

### With mcnp-geometry-checker

Validate cell parameters and geometry:
```python
from mcnp_geometry_checker import MCNPGeometryChecker
from mcnp_cell_checker import MCNPCellChecker

# Cell validation
cell_checker = MCNPCellChecker()
cell_valid = cell_checker.check_cells('input.inp')['valid']

# Geometry validation
geom_checker = MCNPGeometryChecker()
geom_valid = len(geom_checker.check_geometry('input.inp')['errors']) == 0

return cell_valid and geom_valid
```

---

## Documentation References

### Root Skill Directory Files

- **validation_procedures.md** - Detailed 5-step validation procedures
- **cell_card_concepts.md** - Universe and lattice system theory
- **error_catalog.md** - 6 common problems with solutions
- **detailed_examples.md** - Complete workflow examples

### Scripts Directory

- **scripts/mcnp_cell_checker.py** - Main validation class
- **scripts/universe_validator.py** - Universe reference checking
- **scripts/lattice_validator.py** - Lattice and fill array validation
- **scripts/dependency_tree_builder.py** - Hierarchy analysis
- **scripts/README.md** - Script usage guide

### Example Files

- **assets/example_inputs/** - 4 validated example files with descriptions
  - 01_simple_universe_valid.i (2-level hierarchy)
  - 02_cubic_lattice_lat1.i (LAT=1 example)
  - 03_hex_lattice_lat2.i (LAT=2 example)
  - 04_fill_array_error.i (dimension mismatch example)

### MCNP Manual References

- Chapter 5.2: Cell Cards - Complete cell card syntax
- Chapter 5.5.5: Repeated Structures - Universe, lattice, and fill specifications
- Chapter 5.5.5.1: U keyword - Universe definitions and hierarchy
- Chapter 5.5.5.2: LAT keyword - Lattice types and indexing
- Chapter 5.5.5.3: FILL keyword - Fill specifications and arrays
- Chapter 3.4.1: Best practices for geometry setup
- Chapter 10.1.3: Repeated structures examples

---

**END OF MCNP CELL CHECKER SKILL**
