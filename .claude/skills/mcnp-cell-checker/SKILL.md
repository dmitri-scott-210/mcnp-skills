---
name: "MCNP Cell Checker"
description: "Validates MCNP cell cards for universe, lattice, and fill correctness. Checks U/FILL references, LAT specifications, fill array dimensions, and nesting hierarchy. Use for repeated structures validation."
version: "2.0.0"
dependencies: "mcnp-geometry-builder, mcnp-lattice-builder, mcnp-input-validator"
---

# MCNP Cell Checker

## Overview

Cell cards in MCNP can contain complex repeated structure features (universes, lattices, fill arrays) that create multi-level geometry hierarchies. Errors in these features are difficult to debug and often cause fatal errors. This skill provides specialized validation for:

- **Universe Definition/Reference Checking**: Verify all `u=N` universes are unique and all `fill=N` references are defined
- **Lattice Type Validation**: Ensure `lat=1` (cubic) or `lat=2` (hexagonal) only
- **Fill Array Dimension Validation**: Match array sizes to lattice declarations
- **Nesting Hierarchy Analysis**: Build and validate universe dependency trees
- **Circular Reference Detection**: Prevent infinite universe loops
- **Lattice Boundary Validation**: Check appropriate surfaces for lattice types

**When to Use**: After creating lattices, before production runs, when debugging universe errors, for complex repeated structures, when nesting exceeds 3-4 levels.

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User mentions "universe", "lattice", or "fill" errors
- User reports "undefined universe" or "circular reference" errors
- User has cells with `lat=` or `fill=` parameters
- User building reactor cores, fuel assemblies, or complex arrays
- User asks "how deep can I nest universes?"

### Validation Approach

```
User request → Select scope:
├── Quick universe check → Verify all FILL references defined
├── Full cell validation → All checks (recommended)
├── Lattice-only check → LAT/FILL array validation
├── Dependency mapping → Build universe tree
└── Specific cell → Deep dive on one cell

If error already occurring:
├── "Undefined universe" → Check U/FILL references
├── "Array size mismatch" → Validate FILL dimensions
├── "Invalid LAT value" → Check lattice type
├── "Lost particles" → Check lattice boundaries
├── "Circular reference" → Build dependency graph
└── "Too deep nesting" → Analyze hierarchy depth

Validation Depth:
├── Quick (< 1 min): Universe references only
├── Comprehensive (2-5 min): All 5 validation procedures
└── Diagnostic (5-15 min): Full analysis + recommendations
```

## Quick Reference

### Universe System (U and FILL)

| Feature | Syntax | Purpose | Validation |
|---------|--------|---------|------------|
| Universe definition | `u=N` | Assign cell to universe N | Must be unique |
| Universe reference | `fill=N` | Fill cell with universe N | N must be defined |
| Simple fill | `fill=5` | Fill with single universe | u=5 must exist |
| Array fill | `fill=-3:3 -3:3 0:0 ...` | Lattice fill array | Dimensions must match |
| Real world | u=0 (default) | Top-level geometry | Cannot use in fill= |

**Key Rules:**
- Every `fill=N` must have corresponding `u=N` definition
- No circular references (u=1 → u=2 → u=1)
- Maximum 20 nesting levels (recommend ≤7)
- Negative u= for enclosed cells (performance optimization)

### Lattice System (LAT and FILL Arrays)

| Lattice Type | Value | Geometry | Surfaces Needed | Array Format |
|--------------|-------|----------|-----------------|--------------|
| Cubic | `lat=1` | Hexahedral (box) | 6 (or RPP) | i j k indices |
| Hexagonal | `lat=2` | Hex prism | 8 (6 sides + 2 bases) | i j k indices |

**Fill Array Dimensions:**
```
Declaration: fill= i1:i2 j1:j2 k1:k2
Required values = (i2-i1+1) × (j2-j1+1) × (k2-k1+1)

Example: fill= -7:7 -7:7 0:0
  i: 15 values, j: 15 values, k: 1 value
  Total: 15 × 15 × 1 = 225 values required
```

**Lattice Requirements:**
- LAT parameter MUST have FILL parameter
- Lattice cell MUST be void (material 0)
- Only `lat=1` or `lat=2` allowed (lat=3 is invalid)

## Tool Invocation

### Python Module Usage

```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()

# Complete validation
results = checker.check_cells('input.inp')
if results['valid']:
    print("✓ All cell cards validated")
else:
    for error in results['errors']:
        print(f"ERROR: {error}")

# Universe validation only
universe_check = checker.validate_universes('input.inp')
undefined = universe_check['undefined']
if undefined:
    print(f"❌ Undefined universes: {undefined}")

# Lattice validation
lattice_results = checker.validate_lattices('input.inp')
for cell, result in lattice_results.items():
    if result['errors']:
        print(f"Cell {cell}: {result['errors']}")

# Fill array dimensions
fill_check = checker.check_fill_dimensions('input.inp')
for cell, result in fill_check.items():
    if result['expected_size'] != result['actual_size']:
        print(f"Cell {cell}: Size mismatch")
        print(f"  Expected: {result['expected_size']}")
        print(f"  Found: {result['actual_size']}")

# Universe dependency tree
tree = checker.build_universe_tree('input.inp')
print(f"Max nesting: {tree['max_depth']} levels")
if tree['circular_refs']:
    print("❌ Circular references detected")

# Lattice boundaries
boundary_check = checker.check_lattice_boundaries('input.inp')
for cell, result in boundary_check.items():
    if not result['appropriate']:
        print(f"Cell {cell} recommendations:")
        for rec in result['recommendations']:
            print(f"  • {rec}")
```

See **scripts/README.md** for complete API documentation and command-line usage.

## Use Cases

### Use Case 1: Quick Universe Validation

**Scenario**: User asks "Did I define all my universes correctly?"

**Workflow**:
1. Parse input file for universe definitions (`u=`)
2. Parse input file for universe references (`fill=`)
3. Compare defined vs used
4. Report undefined references (fatal) and unused definitions (warning)

**Example**:
```python
checker = MCNPCellChecker()
universe_check = checker.validate_universes('reactor.inp')

print(f"Defined: {universe_check['defined']}")
print(f"Used: {universe_check['used']}")

if universe_check['undefined']:
    print(f"❌ FATAL: Undefined: {universe_check['undefined']}")
else:
    print("✓ All universe references valid")
```

### Use Case 2: Lattice Dimension Validation

**Scenario**: User debugging "array size mismatch" error

**Workflow**:
1. Find all lattice cells (`lat=1` or `lat=2`)
2. Parse fill array declaration (`fill= i1:i2 j1:j2 k1:k2`)
3. Calculate expected size: (i2-i1+1) × (j2-j1+1) × (k2-k1+1)
4. Count actual values in array
5. Report mismatches

**Example**:
```python
fill_check = checker.check_fill_dimensions('fuel_assembly.inp')

for cell, result in fill_check.items():
    expected = result['expected_size']
    actual = result['actual_size']
    if expected != actual:
        print(f"Cell {cell}: Mismatch")
        print(f"  Declaration: {result['declaration']}")
        print(f"  Expected: {expected} values")
        print(f"  Found: {actual} values")
        print(f"  Difference: {expected - actual}")
```

### Use Case 3: Circular Reference Detection

**Scenario**: User reports "infinite loop" or tracking very slow

**Workflow**:
1. Build complete universe dependency graph
2. Use depth-first search to detect cycles
3. Report circular dependencies
4. Analyze nesting depth

**Example**:
```python
tree = checker.build_universe_tree('input.inp')

if tree['circular_refs']:
    print("❌ Circular references detected:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))} → (loops back)")
else:
    print(f"✓ No circular references")
    print(f"  Max nesting: {tree['max_depth']} levels")
```

### Use Case 4: Pre-Production Complete Validation

**Scenario**: Validate all cell features before production run

**Workflow**:
1. Validate universe references
2. Check lattice types (1 or 2 only)
3. Verify fill array dimensions
4. Build dependency tree (check circular refs)
5. Check lattice boundaries
6. Report comprehensive results

**Example**:
```python
results = checker.check_cells('gt_mhr_core.inp')

if results['valid']:
    print("✓ ALL CELL VALIDATION PASSED")
    print("  Ready for production run")
else:
    print("❌ VALIDATION FAILED:")
    for err in results['errors']:
        print(f"  {err}")
    print("\nFix errors before running MCNP")
```

### Use Case 5: Lattice Boundary Recommendations

**Scenario**: Optimize lattice geometry for performance

**Workflow**:
1. Check lattice type (LAT=1 or LAT=2)
2. Analyze boundary surfaces
3. Recommend optimal surfaces:
   - LAT=1: RPP macrobody or 6 planes
   - LAT=2: HEX/RHP macrobody or 6 planes + 2 z-planes
4. Provide surface count and type information

**Example**:
```python
boundary_check = checker.check_lattice_boundaries('input.inp')

for cell, result in boundary_check.items():
    lat_type = result['lat_type']
    print(f"Cell {cell} (LAT={lat_type}):")

    if result['appropriate']:
        print(f"  ✓ Boundary surfaces appropriate")
    else:
        print(f"  ⚠ Recommendations:")
        for rec in result['recommendations']:
            print(f"    • {rec}")
```

## Best Practices

### 1. Universe Organization

**Group universe definitions logically** with clear comments:
```
c === UNIVERSE 0: REAL WORLD ===
1 0 -100 fill=1 imp:n=1

c === UNIVERSE 1: REACTOR CORE ===
100 0 -200 u=1 fill=2 lat=1 imp:n=1

c === UNIVERSE 2: FUEL ASSEMBLY ===
200 0 -300 u=2 fill=3 lat=1 imp:n=1

c === UNIVERSE 3: FUEL PIN ===
300 1 -10.5 -400 u=3 imp:n=1
```

### 2. Fill Array Documentation

**Always document fill array dimensions**:
```
c LATTICE CELL 200: 15×15×1 cubic array (225 values)
c i-direction: -7 to 7 (15 elements)
c j-direction: -7 to 7 (15 elements)
c k-direction: 0 to 0 (1 element)
200 0 -200 lat=1 u=10 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 ...  $ Row 1 (j=-7)
    40 40 50 ...  $ Row 2 (j=-6)
    ...
```

### 3. Negative Universe Optimization

Use negative u= for fully enclosed cells (faster tracking):
```
c Standard (slower):
100 1 -2.7 -100 u=50 imp:n=1

c Optimized (faster):
100 1 -2.7 -100 u=-50 imp:n=1
$ Negative u indicates fully enclosed, skips higher-level checks

WARNING: Only use negative u= if cell is TRULY fully enclosed!
```

### 4. Universe Hierarchy Limits

**Recommended nesting depths**:
- 1-3 levels: Ideal (minimal overhead)
- 4-7 levels: Acceptable (common for reactors)
- 8-10 levels: Use caution (performance impact, consider negative u=)
- >10 levels: Not recommended (simplify or homogenize)

### 5. Pre-Validation Before MCNP

**Always validate before running**:
```bash
python -c "
from mcnp_cell_checker import MCNPCellChecker
import sys
checker = MCNPCellChecker()
results = checker.check_cells('input.inp')
if not results['valid']:
    print('ERRORS FOUND - FIX BEFORE RUNNING')
    for err in results['errors']:
        print(f'  {err}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    mcnp6 i=input.inp
fi
```

### 6. Use Universe Reference Map

Create reference map at top of file:
```
c === UNIVERSE REFERENCE MAP ===
c u=0:  Real world (5 cells) → fills=[1, 2]
c u=1:  Reactor core (3 cells) → fills=[10, 20]
c u=10: Fuel region (2 cells) → fills=[100]
c u=100: Fuel pin (5 cells) → fills=[]
```

### 7. Lattice Surface Standards

**LAT=1 (Cubic)**: Use RPP macrobody
```
200 0 -200 lat=1 u=10 fill=1 imp:n=1
200 rpp -10 10 -10 10 0 20
```

**LAT=2 (Hexagonal)**: Use HEX/RHP macrobody
```
300 0 -300 lat=2 u=20 fill=1 imp:n=1
300 rhp 0 0 0  0 0 20  5
```

### 8. Consistent Fill Array Formatting

Format arrays for readability (aligned, symmetric):
```
c GOOD: Aligned, easy to verify
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 4 3 2 1
    1 2 2 2 2 2 1
    1 1 1 1 1 1 1

c BAD: Unaligned, hard to verify
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1 1 2 2 2 2 2 1 1 2 3 4 3 2 1 ...
```

## Integration with Other Skills

### With mcnp-input-validator

Cell checker complements input validator:
```python
from mcnp_input_validator import MCNPInputValidator
from mcnp_cell_checker import MCNPCellChecker

def complete_validation(input_file):
    # Basic validation first
    validator = MCNPInputValidator()
    if not validator.validate_file(input_file)['valid']:
        return False

    # Then cell-specific checks
    checker = MCNPCellChecker()
    return checker.check_cells(input_file)['valid']
```

### With mcnp-lattice-builder

Build and validate lattices:
```python
from mcnp_lattice_builder import MCNPLatticeBuilder
from mcnp_cell_checker import MCNPCellChecker

def build_and_validate(params):
    builder = MCNPLatticeBuilder()
    lattice_cards = builder.create_lattice(**params)

    # Write and validate
    with open('temp.inp', 'w') as f:
        f.write(lattice_cards)

    checker = MCNPCellChecker()
    results = checker.check_cells('temp.inp')

    if results['valid']:
        return lattice_cards
    else:
        raise ValueError("Generated lattice failed validation")
```

### Typical Workflow

```
1. mcnp-lattice-builder → Create lattice structure
2. mcnp-cell-checker → Validate LAT/FILL/dimensions (THIS SKILL)
3. mcnp-geometry-checker → Check spatial relationships
4. mcnp-input-validator → Final comprehensive check
5. MCNP execution
```

## References

### Root Skill Directory Files

**Validation Procedures** (`validation_procedures.md`):
- Procedure 1: Universe reference validation (U/FILL checks)
- Procedure 2: Lattice type validation (LAT=1/2)
- Procedure 3: Fill array dimension validation (size matching)
- Procedure 4: Universe dependency tree construction (hierarchy, circular refs)
- Procedure 5: Lattice boundary surface validation (appropriate surfaces)

**Theory** (`universe_lattice_theory.md`):
- Universe system (U and FILL parameters)
- Lattice system (LAT and FILL arrays)
- Nesting depth and performance
- Cell parameter validation
- Best practices for universes and lattices

**Error Catalog** (`error_catalog.md`):
- Problem 1: Undefined universe reference
- Problem 2: Fill array dimension mismatch
- Problem 3: Circular universe reference
- Problem 4: Invalid lattice type
- Problem 5: Lattice cell with material
- Problem 6: Deep nesting performance
- Problem 7: Duplicate universe definition
- Problem 8: Unused universe definitions

**Integration Guide** (`integration_guide.md`):
- Integration with mcnp-input-validator
- Integration with mcnp-geometry-checker
- Integration with mcnp-lattice-builder
- Integration with mcnp-cross-reference-checker
- Integration with mcnp-geometry-builder
- Pre-production validation script
- Batch validation script
- Continuous integration example

### Scripts

**Python Tools** (`scripts/`):
- mcnp_cell_checker.py: Main validation module
- README.md: Complete API documentation, command-line usage, integration examples

### Example Inputs

**Example Files** (`assets/example_inputs/`):
- 01_valid_simple_universe.i: Correct universe fill
- 02_valid_cubic_lattice.i: Correct LAT=1 with fill array
- 03_invalid_undefined_universe.i: Undefined universe error
- 04_invalid_lattice_dimension_mismatch.i: Fill array size error

Each example has DESCRIPTION.md with validation details.

### MCNP Manual References

- **Chapter 5.2**: Cell Cards (complete syntax)
- **Chapter 5.5.5**: Repeated Structures (U, LAT, FILL)
- **Chapter 5.5.5.1**: U keyword (universe definitions)
- **Chapter 5.5.5.2**: LAT keyword (lattice types)
- **Chapter 5.5.5.3**: FILL keyword (fill specifications)
- **Chapter 3.4.1**: Best practices (items 1-7)
- **Chapter 10.1.3**: Repeated structures examples

### Related Skills

- **mcnp-input-validator**: General input file validation
- **mcnp-geometry-checker**: Geometry overlaps, gaps, lost particles
- **mcnp-cross-reference-checker**: Dependency analysis
- **mcnp-lattice-builder**: Creating lattice structures
- **mcnp-geometry-builder**: Building cell cards with universe features

---

**END OF MCNP CELL CHECKER SKILL**
