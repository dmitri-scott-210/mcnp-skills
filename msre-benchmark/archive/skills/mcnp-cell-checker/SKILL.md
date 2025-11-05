---
name: "MCNP Cell Checker"
description: "Validates MCNP cell cards for universe, lattice, and fill correctness. Checks U/FILL references, LAT specifications, fill array dimensions, and nesting hierarchy. Use for repeated structures validation."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Cell Checker

## Overview

Cell cards in MCNP can contain complex repeated structure features (universes, lattices, fill arrays) that create multi-level geometry hierarchies. Errors in these features are difficult to debug and often cause:

- FATAL errors from undefined universe references
- Dimension mismatches in fill arrays
- Invalid lattice type specifications
- Circular universe dependencies (infinite loops)
- Deep nesting causing performance issues
- Incorrect lattice boundary surfaces

**This skill provides specialized validation for cell-specific features:**

- **Universe Definition/Reference Checking**: Verify all `u=N` universes are unique and all `fill=N` references are defined
- **Lattice Type Validation**: Ensure `lat=1` (cubic) or `lat=2` (hexagonal) only
- **Fill Array Dimension Validation**: Match array sizes to lattice declarations
- **Nesting Hierarchy Analysis**: Build and validate universe dependency trees
- **Lattice Boundary Validation**: Check appropriate surfaces for lattice types
- **Circular Reference Detection**: Prevent infinite universe loops

**When to Use:** After creating lattices, before production runs, when debugging universe errors, for complex repeated structures, when nesting exceeds 3-4 levels.

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User mentions "universe", "lattice", or "fill" errors
- User asks about repeated structures or "u=" parameter
- User reports "undefined universe" errors
- User mentions TRISO particles, fuel assemblies, or core lattices
- User has cells with `lat=` or `fill=` parameters
- User asks "how deep can I nest universes?"
- User building reactor cores or complex arrays

**Context Clues:**
- "My fill array isn't working"
- "MCNP says universe not found"
- "How do I check my lattice?"
- "Lost particles in lattice cells"
- "Circular reference error"
- "Universe nesting too deep"

### Validation Approach Decision Tree

**Step 1: Determine Validation Scope**

```
User request → Select scope:
├── Quick universe check → Verify all FILL references defined
├── Full cell validation → All checks (recommended)
├── Lattice-only check → LAT/FILL array validation
├── Dependency mapping → Build universe tree
└── Specific cell → Deep dive on one cell
```

**Step 2: Problem Type**

```
If error already occurring:
├── "Undefined universe" → Check U/FILL references
├── "Array size mismatch" → Validate FILL dimensions
├── "Invalid LAT value" → Check lattice type
├── "Lost particles" → Check lattice boundaries
├── "Circular reference" → Build dependency graph
└── "Too deep nesting" → Analyze hierarchy depth

If proactive checking:
├── Complex geometry → Full validation
├── Before production → Comprehensive check
├── After modifications → Targeted validation
└── Learning/tutorial → Educational mode
```

**Step 3: Validation Depth**

```
Quick Check (< 1 minute):
├── Collect all universe IDs from u= parameters
├── Collect all universe references from fill= parameters
├── Find undefined references
└── Report fatal errors

Comprehensive Validation (recommended, 2-5 minutes):
├── Quick checks
├── Build complete dependency graph
├── Validate lattice specifications
├── Check fill array dimensions
├── Analyze nesting depth
├── Validate boundary surfaces
└── Provide recommendations

Diagnostic Analysis (problem solving, 5-15 minutes):
├── Comprehensive checks
├── Visualize universe tree
├── Map cell-to-universe relationships
├── Identify performance issues
├── Suggest optimizations
└── Compare to best practices
```

## Tool Invocation

This skill includes a Python implementation for automated cell card validation focused on universes, lattices, and fill arrays.

### Importing the Tool

```python
from mcnp_cell_checker import MCNPCellChecker

# Initialize the checker
checker = MCNPCellChecker()
```

### Basic Usage

**Check All Cell Cards**:
```python
# Run comprehensive cell validation
results = checker.check_cells('path/to/input.inp')

# Review results
if results['valid']:
    print("✓ All cell cards validated successfully")
else:
    print(f"✗ Found {len(results['errors'])} cell validation errors")

# Display findings
for error in results['errors']:
    print(f"ERROR: {error}")

for warning in results['warnings']:
    print(f"WARNING: {warning}")

for info in results['info']:
    print(f"INFO: {info}")
```

**Check Universe References Only**:
```python
# Quick universe validation
universe_check = checker.validate_universes('reactor.inp')

# Get results
defined_universes = universe_check['defined']  # [1, 2, 3, 40, 50]
used_universes = universe_check['used']        # [1, 2, 3, 40, 50]
undefined = universe_check['undefined']        # []

if undefined:
    print("❌ UNDEFINED UNIVERSE REFERENCES:")
    for u in undefined:
        print(f"  Universe {u} is referenced but not defined")
else:
    print("✓ All universe references are valid")

# Check for unused universes
unused = set(defined_universes) - set(used_universes)
if unused:
    print(f"\n⚠ WARNING: Unused universes: {unused}")
```

**Validate Lattice Specifications**:
```python
# Check all lattice cells
lattice_results = checker.validate_lattices('input.inp')

for cell_num, result in lattice_results.items():
    lat_type = result['lat_type']  # 1 or 2
    has_fill = result['has_fill']  # True/False
    fill_valid = result['fill_valid']  # True/False
    errors = result['errors']  # List of error messages

    if errors:
        print(f"Cell {cell_num} (LAT={lat_type}):")
        for err in errors:
            print(f"  ✗ {err}")
    else:
        print(f"Cell {cell_num} (LAT={lat_type}): ✓ Valid")
```

**Check Fill Array Dimensions**:
```python
# Validate fill array sizes match lattice declarations
fill_check = checker.check_fill_dimensions('input.inp')

for cell_num, result in fill_check.items():
    expected = result['expected_size']  # (i2-i1+1) × (j2-j1+1) × (k2-k1+1)
    actual = result['actual_size']      # Count of values in array
    declaration = result['declaration'] # "fill= -7:7 -7:7 0:0"

    if expected != actual:
        print(f"❌ Cell {cell_num}: Size mismatch")
        print(f"   Declaration: {declaration}")
        print(f"   Expected: {expected} values")
        print(f"   Actual: {actual} values")
        print(f"   Missing/extra: {expected - actual}")
    else:
        print(f"✓ Cell {cell_num}: Fill array size correct ({actual} values)")
```

**Build Universe Dependency Tree**:
```python
# Create complete universe hierarchy
tree = checker.build_universe_tree('reactor.inp')

# Structure:
# {
#     'universes': {
#         0: {'cells': [1, 2, 999], 'fills': [1], 'level': 0},
#         1: {'cells': [100, 200], 'fills': [2, 3], 'level': 1},
#         2: {'cells': [300], 'fills': [], 'level': 2}
#     },
#     'max_depth': 7,
#     'circular_refs': []
# }

# Analyze tree
print(f"Universe hierarchy depth: {tree['max_depth']} levels")

if tree['circular_refs']:
    print("\n❌ CIRCULAR REFERENCES DETECTED:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))} → (loops back)")
else:
    print("✓ No circular universe references")

# Show hierarchy
print("\nUniverse Hierarchy:")
for u_num, u_info in sorted(tree['universes'].items()):
    indent = "  " * u_info['level']
    fills = u_info['fills'] if u_info['fills'] else "none"
    print(f"{indent}u={u_num}: {len(u_info['cells'])} cells, fills={fills}")
```

**Check Lattice Boundary Surfaces**:
```python
# Validate lattice cells have appropriate boundary surfaces
boundary_check = checker.check_lattice_boundaries('input.inp')

for cell_num, result in boundary_check.items():
    lat_type = result['lat_type']
    surfaces = result['surfaces']
    appropriate = result['appropriate']
    recommendations = result['recommendations']

    print(f"Cell {cell_num} (LAT={lat_type}):")
    if appropriate:
        print(f"  ✓ Boundary surfaces appropriate: {surfaces}")
    else:
        print(f"  ⚠ Boundary surfaces: {surfaces}")
        print(f"  Recommendations:")
        for rec in recommendations:
            print(f"    • {rec}")
```

### Integration with MCNP Workflow

**Pre-Run Cell Validation Script**:
```python
from mcnp_cell_checker import MCNPCellChecker

def validate_cell_cards(input_file):
    """Complete cell card validation before MCNP run"""
    print(f"Validating cell cards in: {input_file}")
    print("=" * 70)

    checker = MCNPCellChecker()

    # Step 1: Check universe references
    print("\n[1/5] Checking universe references...")
    universe_check = checker.validate_universes(input_file)

    if universe_check['undefined']:
        print("  ❌ FATAL: Undefined universe references:")
        for u in universe_check['undefined']:
            print(f"     Universe {u} referenced in FILL but not defined")
        return False
    else:
        print(f"  ✓ All {len(universe_check['used'])} universe references valid")

    unused = set(universe_check['defined']) - set(universe_check['used'])
    if unused:
        print(f"  ⚠ WARNING: {len(unused)} unused universes: {unused}")

    # Step 2: Validate lattice types
    print("\n[2/5] Validating lattice specifications...")
    lattice_results = checker.validate_lattices(input_file)

    lattice_errors = []
    for cell_num, result in lattice_results.items():
        if result['errors']:
            lattice_errors.extend(result['errors'])

    if lattice_errors:
        print("  ❌ FATAL: Lattice specification errors:")
        for err in lattice_errors:
            print(f"     {err}")
        return False
    else:
        print(f"  ✓ All {len(lattice_results)} lattice cells valid")

    # Step 3: Check fill array dimensions
    print("\n[3/5] Checking fill array dimensions...")
    fill_check = checker.check_fill_dimensions(input_file)

    dimension_errors = []
    for cell_num, result in fill_check.items():
        if result['expected_size'] != result['actual_size']:
            dimension_errors.append(
                f"Cell {cell_num}: Expected {result['expected_size']} "
                f"values, found {result['actual_size']}"
            )

    if dimension_errors:
        print("  ❌ FATAL: Fill array dimension mismatches:")
        for err in dimension_errors:
            print(f"     {err}")
        return False
    else:
        print(f"  ✓ All fill array dimensions correct")

    # Step 4: Build universe dependency tree
    print("\n[4/5] Building universe dependency tree...")
    tree = checker.build_universe_tree(input_file)

    if tree['circular_refs']:
        print("  ❌ FATAL: Circular universe references:")
        for cycle in tree['circular_refs']:
            print(f"     {' → '.join(map(str, cycle))} → (loops back)")
        return False
    else:
        print(f"  ✓ No circular references (max depth: {tree['max_depth']})")

    if tree['max_depth'] > 10:
        print(f"  ⚠ WARNING: Deep nesting ({tree['max_depth']} levels) "
              "may impact performance")

    # Step 5: Check lattice boundaries
    print("\n[5/5] Checking lattice boundary surfaces...")
    boundary_check = checker.check_lattice_boundaries(input_file)

    boundary_warnings = []
    for cell_num, result in boundary_check.items():
        if not result['appropriate']:
            boundary_warnings.extend(result['recommendations'])

    if boundary_warnings:
        print(f"  ⚠ {len(boundary_warnings)} boundary recommendations:")
        for warn in boundary_warnings[:3]:  # Show first 3
            print(f"     {warn}")
        if len(boundary_warnings) > 3:
            print(f"     ... and {len(boundary_warnings) - 3} more")
    else:
        print(f"  ✓ All lattice boundaries appropriate")

    # Final summary
    print("\n" + "=" * 70)
    print("✓ CELL VALIDATION PASSED")
    print(f"  • {len(universe_check['defined'])} universes defined")
    print(f"  • {len(lattice_results)} lattice cells")
    print(f"  • {tree['max_depth']} levels of nesting")
    print(f"  • Ready for MCNP execution")
    print("=" * 70)

    return True

# Example usage
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.inp"

    if validate_cell_cards(input_file):
        print(f"\n✓ Ready to run: mcnp6 i={input_file}")
    else:
        print("\n✗ Fix cell card errors before running MCNP")
        sys.exit(1)
```

---

## Cell Card Validation Concepts

### Universe System (U and FILL Parameters)

**Universe Definitions** (`u=N`):
- Assigns cell to universe N (N > 0)
- Universe 0 = "real world" (default, no u= parameter)
- Universe numbers must be unique within each cell
- Multiple cells can belong to same universe
- Creates geometric building blocks for reuse

**Universe References** (`fill=N`):
- Fills a cell with all cells from universe N
- Referenced universe must be defined somewhere in input
- Creates hierarchy levels (level 0 = real world, level 1+= filled)
- Can have up to 20 levels of nesting (typical: 3-7)

**Common Universe Patterns**:

```
Single-level fill:
  1 0 -100 fill=1 imp:n=1          $ Real world cell, fill with u=1
  10 1 -2.7 -200 u=1 imp:n=1       $ Universe 1 definition

Multi-level fill:
  1 0 -100 fill=1 imp:n=1          $ Level 0 (real world)
  10 0 -200 u=1 fill=2 imp:n=1     $ Level 1 (fills level 0)
  20 1 -2.7 -300 u=2 imp:n=1       $ Level 2 (fills level 1)

Lattice fill:
  100 0 -500 lat=1 u=5 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1
      1 2 2 2 2 2 1
      1 2 3 3 3 2 1
      1 2 3 4 3 2 1    $ 4 = center, 1 = edge
      1 2 3 3 3 2 1
      1 2 2 2 2 2 1
      1 1 1 1 1 1 1
```

**Validation Rules**:
1. Every `fill=N` must have corresponding `u=N` definition(s)
2. Universe 0 cannot be explicitly used (it's the default)
3. No circular references: u=1 fills u=2 which fills u=1 (infinite loop)
4. Negative u= indicates cell fully enclosed (performance optimization)
5. Maximum 20 nesting levels (practical limit: 10)

### Lattice System (LAT and FILL Arrays)

**Lattice Types**:
- `lat=1`: Cubic/rectangular lattice (hexahedral elements, 6 faces)
- `lat=2`: Hexagonal lattice (hexagonal prism elements, 8 faces)
- No other values allowed (lat=3, lat=0, etc. are INVALID)

**LAT=1 Cubic Lattice**:

```
Cell card:
  200 0 -200 lat=1 u=10 fill=-5:5 -5:5 0:0 imp:n=1
      1 1 1 1 1 1 1 1 1 1 1    $ i = -5 to +5 (11 elements)
      1 2 2 2 2 2 2 2 2 2 1    $ j = -5 to +5 (11 elements)
      ...                        $ k = 0 to 0 (1 element)
      (11 lines × 11 values = 121 total values)

Surface definition:
  200 rpp -11 11 -11 11 0 10    $ Rectangular parallelepiped

Element [0,0,0] is bounded by first 6 surfaces in cell geometry
Element indices increase across surfaces in order listed
```

**LAT=2 Hexagonal Lattice**:

```
Cell card:
  300 0 -301 -302 -303 -304 -305 -306 -307 -308
      lat=2 u=20 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1    $ Hexagonal arrangement
      1 2 2 2 2 2 1
      1 2 3 3 3 2 1
      1 2 3 4 3 2 1
      1 2 3 3 3 2 1
      1 2 2 2 2 2 1
      1 1 1 1 1 1 1

Surface definitions (hexagon with 6 sides + 2 bases):
  301 p ...    $ Six planar surfaces defining hexagon
  302 p ...
  303 p ...
  304 p ...
  305 p ...
  306 p ...
  307 pz 0     $ Bottom base
  308 pz 10    $ Top base
```

**Fill Array Dimension Validation**:

The fill array must match the declared lattice range:

```
Declaration: fill= i1:i2 j1:j2 k1:k2

Required values = (i2-i1+1) × (j2-j1+1) × (k2-k1+1)

Example:
fill= -7:7 -7:7 0:0
  → i: -7 to 7 = 15 values
  → j: -7 to 7 = 15 values
  → k: 0 to 0 = 1 value
  → Total required: 15 × 15 × 1 = 225 values

Must provide exactly 225 universe IDs after fill= declaration
```

**Lattice Surface Ordering**:

For `lat=1`, surface order in cell card determines lattice indexing:
- Surfaces 1-2: Define i-direction ([1,0,0] and [-1,0,0])
- Surfaces 3-4: Define j-direction ([0,1,0] and [0,-1,0])
- Surfaces 5-6: Define k-direction ([0,0,1] and [0,0,-1])

For `lat=2`, eight surfaces define hexagonal prism:
- Surfaces 1-6: Six sides of hexagon (i and j directions)
- Surfaces 7-8: Top and bottom bases (k direction)

**Common Lattice Errors**:

```
BAD: Wrong lattice type
  100 0 -100 lat=3 fill=1 imp:n=1    ✗ lat=3 doesn't exist

GOOD: Valid lattice type
  100 0 -100 lat=1 fill=1 imp:n=1    ✓ lat=1 (cubic)

BAD: Lattice without fill
  100 0 -100 lat=1 imp:n=1            ✗ LAT requires FILL

GOOD: Lattice with fill
  100 0 -100 lat=1 fill=5 imp:n=1    ✓ Fills with u=5

BAD: Dimension mismatch
  100 0 -100 lat=1 fill=-2:2 -2:2 0:0 imp:n=1
      1 2 3 4 5    ✗ Only 5 values, need 5×5×1 = 25

GOOD: Correct dimensions
  100 0 -100 lat=1 fill=-2:2 -2:2 0:0 imp:n=1
      1 1 1 1 1
      1 2 2 2 1
      1 2 3 2 1    ✓ 25 values (5×5×1)
      1 2 2 2 1
      1 1 1 1 1
```

### Nesting Depth and Performance

**Nesting Levels**:
- Level 0: Real world (u=0, implicit)
- Level 1: Cells filled into level 0
- Level 2: Cells filled into level 1
- ...
- Level N: Up to 20 allowed

**Performance Impact**:

```
Shallow nesting (1-3 levels): Minimal impact
  Example: Fuel pins in assembly in core
  Level 0: Core
  Level 1: Assembly
  Level 2: Pins

Moderate nesting (4-7 levels): Noticeable but acceptable
  Example: TRISO particles in compact in fuel block in core
  Level 0: Reactor vessel
  Level 1: Core
  Level 2: Fuel column
  Level 3: Fuel block
  Level 4: Fuel compact
  Level 5: TRISO particle lattice
  Level 6: Particle layers

Deep nesting (8-10 levels): Performance degradation
  Particle tracking slower
  Memory usage increases
  Consider simplification

Excessive nesting (>10 levels): Not recommended
  Significant performance penalty
  Difficult to debug
  May indicate over-modeling
```

**Optimization Recommendation**: If nesting exceeds 7 levels, consider:
- Combining levels where possible
- Using negative universe numbers for enclosed cells
- Simplifying geometry representation
- Homogenizing lower levels

### Cell Parameter Validation

**Required Combinations**:

```
If cell has lat= parameter:
  → MUST have fill= parameter
  → Cannot have material/density (must be void, m=0)
  → Surfaces define [0,0,0] lattice element

If cell has fill= parameter (non-lattice):
  → Usually void (m=0), but can have material
  → Material in filled cell adds to fill universe
  → Surfaces define window boundary

If cell has u= parameter:
  → Belongs to that universe
  → Can be filled into other cells via fill=
  → Can have material or be void
```

**Parameter Conflicts**:

```
BAD: Lattice with material
  100 1 -2.7 -100 lat=1 fill=5 imp:n=1    ✗ Lattice must be void

GOOD: Lattice as void
  100 0 -100 lat=1 fill=5 imp:n=1         ✓ Void lattice

BAD: Lattice without fill
  100 0 -100 lat=1 imp:n=1                ✗ LAT requires FILL

GOOD: Lattice with fill array
  100 0 -100 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1
      ...                                  ✓ Complete fill array

BAD: Undefined universe fill
  100 0 -100 fill=99 imp:n=1              ✗ u=99 not defined

GOOD: Defined universe fill
  100 0 -100 fill=5 imp:n=1               ✓ u=5 defined elsewhere
  500 1 -2.7 -500 u=5 imp:n=1             ✓ Universe 5 definition
```

## Validation Procedures

### Procedure 1: Universe Reference Validation

**Goal**: Ensure all `fill=` references have corresponding `u=` definitions

**Steps**:

1. **Parse all cell cards** and extract universe information:
   ```python
   cells = parse_input_file('input.inp')

   defined_universes = set()
   used_universes = set()

   for cell in cells:
       # Collect definitions
       if 'u' in cell.parameters:
           u_num = cell.parameters['u']
           if u_num in defined_universes:
               error(f"Duplicate universe definition: u={u_num}")
           defined_universes.add(u_num)

       # Collect references
       if 'fill' in cell.parameters:
           fill_value = cell.parameters['fill']
           if isinstance(fill_value, int):
               # Simple fill: fill=5
               used_universes.add(fill_value)
           elif isinstance(fill_value, list):
               # Array fill: fill= -3:3 ... 1 2 3 4 ...
               for u in fill_value['array_values']:
                   used_universes.add(u)
   ```

2. **Find undefined references**:
   ```python
   undefined = used_universes - defined_universes

   if undefined:
       for u in undefined:
           error(f"Universe {u} referenced in FILL but not defined with u={u}")
   ```

3. **Check for unused definitions** (warning only):
   ```python
   unused = defined_universes - used_universes

   if unused:
       warning(f"Unused universe definitions: {unused}")
   ```

4. **Check for universe 0 misuse**:
   ```python
   if 0 in defined_universes:
       error("Universe 0 cannot be explicitly defined (it is the default)")

   if 0 in used_universes:
       error("Universe 0 cannot be used in FILL (it is the real world)")
   ```

**Expected Output**:
```
✓ Universe validation passed
  • 15 universes defined: [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
  • 15 universes referenced
  • 0 undefined references
  • 2 unused definitions: [300, 400] (warning)
```

### Procedure 2: Lattice Type Validation

**Goal**: Verify LAT parameter values are valid (1 or 2 only)

**Steps**:

1. **Find all lattice cells**:
   ```python
   for cell in cells:
       if 'lat' in cell.parameters:
           lat_value = cell.parameters['lat']

           # Check valid values
           if lat_value not in [1, 2]:
               error(f"Cell {cell.number}: Invalid LAT={lat_value} "
                     "(must be 1 or 2)")

           # Check FILL requirement
           if 'fill' not in cell.parameters:
               error(f"Cell {cell.number}: LAT specified without FILL "
                     "(lattice requires fill)")

           # Check material (should be void)
           if cell.material != 0:
               error(f"Cell {cell.number}: Lattice cell must be void "
                     f"(has material {cell.material})")
   ```

2. **Validate surface count**:
   ```python
   if lat_value == 1:
       # Cubic lattice needs 6 bounding surfaces minimum
       surfaces = extract_surfaces(cell.geometry)
       if len(surfaces) < 6:
           warning(f"Cell {cell.number}: LAT=1 typically needs 6 surfaces "
                   f"for proper indexing (found {len(surfaces)})")

   elif lat_value == 2:
       # Hexagonal lattice needs 8 surfaces (6 sides + 2 bases)
       surfaces = extract_surfaces(cell.geometry)
       if len(surfaces) < 8:
           warning(f"Cell {cell.number}: LAT=2 typically needs 8 surfaces "
                   f"for hexagonal prism (found {len(surfaces)})")
   ```

**Expected Output**:
```
✓ Lattice type validation passed
  • Cell 200 (LAT=1): ✓ Cubic lattice, 6 surfaces
  • Cell 500 (LAT=2): ✓ Hexagonal lattice, 8 surfaces
  • Cell 800 (LAT=1): ✓ Cubic lattice, 6 surfaces
```

### Procedure 3: Fill Array Dimension Validation

**Goal**: Ensure fill array size matches lattice declaration

**Steps**:

1. **Parse fill declaration**:
   ```python
   for cell in lattice_cells:
       fill_params = cell.parameters['fill']

       if isinstance(fill_params, dict):  # Array fill
           # Extract range: fill= i1:i2 j1:j2 k1:k2
           i_range = fill_params['i_range']  # (i1, i2)
           j_range = fill_params['j_range']  # (j1, j2)
           k_range = fill_params['k_range']  # (k1, k2)

           # Calculate expected size
           i_size = i_range[1] - i_range[0] + 1
           j_size = j_range[1] - j_range[0] + 1
           k_size = k_range[1] - k_range[0] + 1
           expected_size = i_size * j_size * k_size

           # Count actual values
           actual_values = fill_params['array_values']
           actual_size = len(actual_values)

           # Compare
           if actual_size != expected_size:
               error(f"Cell {cell.number}: Fill array size mismatch\n"
                     f"  Declaration: fill= {i_range[0]}:{i_range[1]} "
                     f"{j_range[0]}:{j_range[1]} {k_range[0]}:{k_range[1]}\n"
                     f"  Expected: {i_size}×{j_size}×{k_size} = {expected_size} values\n"
                     f"  Found: {actual_size} values\n"
                     f"  Difference: {actual_size - expected_size}")
   ```

2. **Validate universe IDs in array**:
   ```python
   # Check that all values are integers
   for val in actual_values:
       if not isinstance(val, int):
           error(f"Cell {cell.number}: Non-integer value in fill array: {val}")

       # Values should be defined universe numbers
       if val != 0 and val not in defined_universes:
           error(f"Cell {cell.number}: Fill array references undefined "
                 f"universe {val}")
   ```

**Expected Output**:
```
✓ Fill array dimensions validated
  • Cell 200: 15×15×1 = 225 values (expected 225, found 225) ✓
  • Cell 500: 23×23×1 = 529 values (expected 529, found 529) ✓
  • Cell 800: 7×7×3 = 147 values (expected 147, found 147) ✓
```

### Procedure 4: Universe Dependency Tree Construction

**Goal**: Build complete universe hierarchy and detect circular references

**Steps**:

1. **Initialize data structures**:
   ```python
   universe_info = {}
   for u in all_universe_numbers:
       universe_info[u] = {
           'cells': [],           # Cells belonging to this universe
           'fills': [],           # Universes that this universe fills
           'filled_by': [],       # Universes that fill this one
           'level': None,         # Hierarchy level (0 = real world)
       }
   ```

2. **Build relationships**:
   ```python
   for cell in cells:
       u_num = cell.parameters.get('u', 0)  # Default = real world
       universe_info[u_num]['cells'].append(cell.number)

       if 'fill' in cell.parameters:
           fill_val = cell.parameters['fill']

           if isinstance(fill_val, int):
               # Simple fill
               universe_info[u_num]['fills'].append(fill_val)
               universe_info[fill_val]['filled_by'].append(u_num)

           elif isinstance(fill_val, dict):
               # Array fill - get unique universe IDs
               unique_fills = set(fill_val['array_values'])
               for f_u in unique_fills:
                   universe_info[u_num]['fills'].append(f_u)
                   universe_info[f_u]['filled_by'].append(u_num)
   ```

3. **Calculate hierarchy levels** (breadth-first search):
   ```python
   from collections import deque

   # Start with real world (level 0)
   queue = deque([(0, 0)])  # (universe_num, level)
   visited = {0}

   while queue:
       u, level = queue.popleft()
       universe_info[u]['level'] = level

       # Process universes this one fills
       for filled_u in universe_info[u]['fills']:
           if filled_u not in visited:
               visited.add(filled_u)
               queue.append((filled_u, level + 1))

   max_level = max(info['level'] for info in universe_info.values()
                   if info['level'] is not None)
   ```

4. **Detect circular references**:
   ```python
   def find_cycles(u, visited, rec_stack, path):
       """DFS to find cycles in universe dependency graph"""
       visited.add(u)
       rec_stack.add(u)
       path.append(u)

       for filled_u in universe_info[u]['fills']:
           if filled_u not in visited:
               if find_cycles(filled_u, visited, rec_stack, path):
                   return True
           elif filled_u in rec_stack:
               # Found cycle
               cycle_start = path.index(filled_u)
               cycle = path[cycle_start:] + [filled_u]
               error(f"Circular universe reference: "
                     f"{' → '.join(map(str, cycle))}")
               return True

       rec_stack.remove(u)
       path.pop()
       return False

   # Check for cycles starting from real world
   find_cycles(0, set(), set(), [])
   ```

**Expected Output**:
```
✓ Universe dependency tree constructed
  • Max nesting depth: 6 levels
  • No circular references detected

  Hierarchy:
    u=0 (real world): 5 cells, fills=[1, 2]
      u=1 (level 1): 3 cells, fills=[10, 20]
        u=10 (level 2): 2 cells, fills=[100]
          u=100 (level 3): 1 cell, fills=[200]
            u=200 (level 4): 1 cell, fills=[300]
              u=300 (level 5): 5 cells, fills=[]
        u=20 (level 2): 1 cell, fills=[]
      u=2 (level 1): 2 cells, fills=[30]
        u=30 (level 2): 1 cell, fills=[]
```

### Procedure 5: Lattice Boundary Surface Validation

**Goal**: Check that lattice cells have appropriate boundary surfaces

**Steps**:

1. **For LAT=1 (cubic) lattices**:
   ```python
   for cell in cubic_lattice_cells:
       surfaces = extract_surfaces(cell.geometry)
       surface_types = [get_surface_type(s) for s in surfaces]

       # Recommend RPP (right parallelepiped) or 6 planes
       has_rpp = 'RPP' in surface_types
       has_box = 'BOX' in surface_types
       plane_count = surface_types.count('P') + surface_types.count('PX') + \
                     surface_types.count('PY') + surface_types.count('PZ')

       if has_rpp or has_box:
           info(f"Cell {cell.number} (LAT=1): Using macrobody (optimal)")
       elif plane_count >= 6:
           info(f"Cell {cell.number} (LAT=1): Using {plane_count} planes")
       else:
           warning(f"Cell {cell.number} (LAT=1): Unusual boundary surfaces\n"
                   f"  Recommend: RPP macrobody or 6 planes\n"
                   f"  Found: {surface_types}")
   ```

2. **For LAT=2 (hexagonal) lattices**:
   ```python
   for cell in hex_lattice_cells:
       surfaces = extract_surfaces(cell.geometry)
       surface_types = [get_surface_type(s) for s in surfaces]

       # Recommend HEX macrobody or 6 planes + 2 z-planes
       has_hex = 'HEX' in surface_types
       has_rhp = 'RHP' in surface_types
       p_count = surface_types.count('P')
       pz_count = surface_types.count('PZ')

       if has_hex or has_rhp:
           info(f"Cell {cell.number} (LAT=2): Using hexagonal macrobody (optimal)")
       elif p_count >= 6 and pz_count >= 2:
           info(f"Cell {cell.number} (LAT=2): Using {p_count} planes + "
                f"{pz_count} z-planes")
       else:
           warning(f"Cell {cell.number} (LAT=2): Unusual boundary surfaces\n"
                   f"  Recommend: HEX macrobody or 6 P surfaces + 2 PZ surfaces\n"
                   f"  Found: {surface_types}")
   ```

**Expected Output**:
```
✓ Lattice boundary surfaces checked
  • Cell 200 (LAT=1): Using RPP macrobody (optimal)
  • Cell 500 (LAT=2): Using HEX macrobody (optimal)
  • Cell 800 (LAT=1): Using 6 planes

  ⚠ 1 recommendation:
    • Cell 850 (LAT=2): Using cylinders instead of hexagonal prism
      Recommend: HEX macrobody or 6 P + 2 PZ surfaces
```

## Common Cell Card Problems & Solutions

### Problem 1: Undefined Universe Reference

**Symptoms**:
```
FATAL ERROR: Universe 50 not found
         Cell 200 references fill=50 but no cell has u=50
```

**Diagnosis**:
```python
# Check universe definitions
checker = MCNPCellChecker()
universe_check = checker.validate_universes('input.inp')

undefined = universe_check['undefined']
print(f"Undefined universes: {undefined}")  # [50]
```

**Root Causes**:
1. Typo in universe number (u=50 vs u=5)
2. Deleted cell that defined u=50
3. Copy-paste error from different input
4. Off-by-one error in lattice fill array

**Solutions**:

```
BAD: Reference without definition
  200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1
      1 2 2 2 2 2 1
      1 2 3 50 3 2 1    ✗ u=50 not defined
      ...

GOOD: Define the universe
  200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1
      1 2 2 2 2 2 1
      1 2 3 50 3 2 1    ✓ u=50 defined below
      ...
  500 1 -10.5 -500 u=50 imp:n=1    ✓ Universe 50 definition

GOOD: Fix the typo
  200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1
      1 2 2 2 2 2 1
      1 2 3 5 3 2 1     ✓ Changed 50 → 5
      ...
  50 1 -10.5 -50 u=5 imp:n=1       ✓ u=5 already defined
```

### Problem 2: Fill Array Dimension Mismatch

**Symptoms**:
```
FATAL ERROR: Cell 200 fill array size incorrect
         Expected 225 values (15×15×1), found 210
```

**Diagnosis**:
```python
# Check fill dimensions
fill_check = checker.check_fill_dimensions('input.inp')

for cell, result in fill_check.items():
    if result['expected_size'] != result['actual_size']:
        print(f"Cell {cell}:")
        print(f"  Expected: {result['expected_size']}")
        print(f"  Actual: {result['actual_size']}")
        print(f"  Missing: {result['expected_size'] - result['actual_size']}")
```

**Root Causes**:
1. Miscounted array values
2. Wrong range in fill declaration
3. Copy-paste missing lines
4. Off-by-one in range calculation

**Solutions**:

```
BAD: Missing values
  200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
      40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
      40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
      ... (only 210 lines, missing 15)
  ✗ Expected 15×15×1 = 225 values, found 210

GOOD: Complete array
  200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
      40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
      40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
      ... (all 15 lines present)
  ✓ Expected 15×15×1 = 225 values, found 225

GOOD: Correct the range
  200 0 -200 lat=1 fill=-6:7 -7:7 0:0 imp:n=1
      ... (210 values)
  ✓ Expected 14×15×1 = 210 values, found 210
```

**Prevention**: Use comments to track array size
```
c Lattice cell 200: 15×15×1 cubic array (225 values)
c Each line = 15 values (i = -7 to 7)
c Need 15 lines (j = -7 to 7)
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40  $ j=-7
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40  $ j=-6
    ...
```

### Problem 3: Circular Universe Reference

**Symptoms**:
```
FATAL ERROR: Circular universe dependency detected
         u=1 fills u=2, u=2 fills u=1 (infinite loop)
```

**Diagnosis**:
```python
# Build dependency tree
tree = checker.build_universe_tree('input.inp')

if tree['circular_refs']:
    print("Circular references detected:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))} → (loops back)")
```

**Root Causes**:
1. Recursive fill structure
2. Copy-paste error creating loop
3. Misunderstanding universe hierarchy

**Solutions**:

```
BAD: Direct circular reference
  100 0 -100 u=1 fill=2 imp:n=1    ✗ u=1 fills u=2
  200 0 -200 u=2 fill=1 imp:n=1    ✗ u=2 fills u=1 (circular!)

GOOD: Hierarchical structure
  100 0 -100 u=1 fill=2 imp:n=1    ✓ u=1 fills u=2
  200 0 -200 u=2 imp:n=1           ✓ u=2 is terminal (no fill)

BAD: Indirect circular reference
  100 0 -100 u=1 fill=2 imp:n=1    ✗ u=1 → u=2
  200 0 -200 u=2 fill=3 imp:n=1    ✗ u=2 → u=3
  300 0 -300 u=3 fill=1 imp:n=1    ✗ u=3 → u=1 (circular!)

GOOD: Linear hierarchy
  100 0 -100 u=1 fill=2 imp:n=1    ✓ u=1 → u=2
  200 0 -200 u=2 fill=3 imp:n=1    ✓ u=2 → u=3
  300 1 -2.7 -300 u=3 imp:n=1      ✓ u=3 terminal (has material)
```

### Problem 4: Invalid Lattice Type

**Symptoms**:
```
FATAL ERROR: Invalid LAT value
         Cell 200 has lat=3 (must be 1 or 2)
```

**Diagnosis**:
```python
# Validate lattice types
lattice_results = checker.validate_lattices('input.inp')

for cell, result in lattice_results.items():
    if result['errors']:
        for err in result['errors']:
            print(f"Cell {cell}: {err}")
```

**Root Causes**:
1. Typo (lat=3 instead of lat=1)
2. Confusion about lattice types
3. Trying to use non-existent lattice type

**Solutions**:

```
BAD: Invalid LAT value
  200 0 -200 lat=3 fill=1 imp:n=1    ✗ lat=3 doesn't exist

GOOD: Cubic lattice
  200 0 -200 lat=1 fill=1 imp:n=1    ✓ lat=1 (cubic)

GOOD: Hexagonal lattice
  200 0 -200 lat=2 fill=1 imp:n=1    ✓ lat=2 (hexagonal)

BAD: Lattice without FILL
  200 0 -200 lat=1 imp:n=1           ✗ LAT requires FILL

GOOD: Lattice with FILL
  200 0 -200 lat=1 fill=5 imp:n=1    ✓ Complete specification
```

### Problem 5: Lattice Cell with Material

**Symptoms**:
```
WARNING: Lattice cell has material
         Cell 200 has lat=1 but material 1 (should be void)
```

**Diagnosis**:
```python
for cell in cells:
    if 'lat' in cell.parameters:
        if cell.material != 0:
            warning(f"Cell {cell.number}: Lattice cell should be void, "
                   f"has material {cell.material}")
```

**Root Causes**:
1. Misunderstanding lattice structure
2. Trying to add background material
3. Copy-paste from non-lattice cell

**Solutions**:

```
BAD: Lattice with material
  200 1 -2.7 -200 lat=1 fill=5 imp:n=1    ✗ Material in lattice cell

GOOD: Void lattice
  200 0 -200 lat=1 fill=5 imp:n=1         ✓ Lattice cell is void

If you want background material:
  200 0 -200 lat=1 fill=5 imp:n=1         ✓ Lattice (void)
  300 1 -2.7 -300 u=5 imp:n=1             ✓ Background in universe 5
  400 2 -8.0 -400 u=5 imp:n=1             ✓ Embedded objects
```

### Problem 6: Deep Nesting Performance

**Symptoms**:
```
WARNING: Universe nesting depth is 12 levels
         This may cause performance degradation
```

**Diagnosis**:
```python
tree = checker.build_universe_tree('input.inp')

if tree['max_depth'] > 10:
    warning(f"Deep nesting detected: {tree['max_depth']} levels\n"
            f"  Performance may be impacted\n"
            f"  Consider simplification or negative universe optimization")
```

**Solutions**:

```
Strategy 1: Use negative universe numbers for enclosed cells
  BAD:
    500 1 -10.5 -500 u=50 imp:n=1    ✗ Positive u (slower)

  GOOD:
    500 1 -10.5 -500 u=-50 imp:n=1   ✓ Negative u (faster)
    $ Negative indicates fully enclosed, no higher-level checks

Strategy 2: Combine universe levels
  BAD: Excessive levels
    u=1 → u=2 → u=3 → u=4 → u=5 → u=6 → u=7 → u=8 → u=9 → u=10 → u=11 → u=12

  GOOD: Consolidated
    u=1 → u=2 → u=5 → u=10                    ✓ 4 levels instead of 12

Strategy 3: Homogenize lower levels
  Instead of modeling every detail:
    Replace detailed TRISO particle structure with homogenized material
```

## Best Practices for Cell Cards

### 1. Universe Organization

**Group universe definitions logically**:
```
c ============================================================================
c UNIVERSE 0: REAL WORLD
c ============================================================================
1 0 -100 fill=1 imp:n=1                      $ Core vessel
999 0 100 imp:n=0                             $ Outside world

c ============================================================================
c UNIVERSE 1: REACTOR CORE
c ============================================================================
100 0 -200 u=1 fill=2 lat=1 imp:n=1         $ Fuel assembly lattice
        fill=-5:5 -5:5 0:0
        ...

c ============================================================================
c UNIVERSE 2: FUEL ASSEMBLY
c ============================================================================
200 0 -300 u=2 fill=3 lat=1 imp:n=1         $ Pin lattice
        fill=-8:8 -8:8 0:0
        ...

c ============================================================================
c UNIVERSE 3: FUEL PIN
c ============================================================================
300 1 -10.5 -400 u=3 imp:n=1                 $ Fuel pellet
301 2 -6.5 400 -401 u=3 imp:n=1              $ Cladding
302 3 -1.0 401 -402 u=3 imp:n=1              $ Coolant
```

### 2. Fill Array Documentation

**Always document fill array dimensions**:
```
c LATTICE CELL 200: 15×15×1 cubic array
c Declaration: fill= -7:7 -7:7 0:0
c i-direction: -7 to 7 (15 elements)
c j-direction: -7 to 7 (15 elements)
c k-direction: 0 to 0 (1 element)
c Total values: 15 × 15 × 1 = 225
c
c Layout (j=-7 to j=7, reading left to right):
c Each row = 15 values (i=-7 to i=7)
c Row 1 (j=-7): 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
c Row 2 (j=-6): 40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
c ...
200 0 -200 lat=1 u=10 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
    ...
```

### 3. Negative Universe Optimization

**Use negative u= for fully enclosed cells**:
```
c Positive u= (default, slower):
c   MCNP checks cell against all higher-level boundaries

100 1 -2.7 -100 u=50 imp:n=1           $ Standard

c Negative u= (optimized, faster):
c   MCNP skips higher-level boundary checks (cell fully enclosed)

100 1 -2.7 -100 u=-50 imp:n=1          $ Optimized

c WARNING: Only use negative u= if cell is TRULY fully enclosed
c          Incorrect usage can cause wrong answers with no warnings!
```

### 4. Lattice Boundary Surface Standards

**LAT=1 (Cubic)**:
```
c Recommended: RPP macrobody
200 0 -200 lat=1 u=10 fill=1 imp:n=1
200 rpp -10 10 -10 10 0 20                    $ Rectangular box

c Alternative: 6 planes
200 0 -201 202 -203 204 -205 206 lat=1 u=10 fill=1 imp:n=1
201 px -10    $ i=-1 direction
202 px 10     $ i=+1 direction
203 py -10    $ j=-1 direction
204 py 10     $ j=+1 direction
205 pz 0      $ k=-1 direction
206 pz 20     $ k=+1 direction
```

**LAT=2 (Hexagonal)**:
```
c Recommended: HEX macrobody
300 0 -300 lat=2 u=20 fill=1 imp:n=1
300 rhp 0 0 0  0 0 20  5                      $ Hexagonal prism

c Alternative: 6 planes + 2 z-planes
300 0 -301 302 -303 304 -305 306 -307 308 lat=2 u=20 fill=1 imp:n=1
301 p ...    $ Hex side 1
302 p ...    $ Hex side 2
303 p ...    $ Hex side 3
304 p ...    $ Hex side 4
305 p ...    $ Hex side 5
306 p ...    $ Hex side 6
307 pz 0     $ Bottom
308 pz 20    $ Top
```

### 5. Universe Hierarchy Limits

**Recommended nesting depths**:
```
1-3 levels: Ideal (minimal overhead)
  Example: Pins → Assembly → Core

4-7 levels: Acceptable (common for reactors)
  Example: Particles → Compact → Block → Column → Core → Vessel

8-10 levels: Use with caution (performance impact)
  Consider negative u= optimization

>10 levels: Not recommended
  Simplify geometry or homogenize lower levels
```

### 6. Fill Array Validation Comments

**Include validation information**:
```
c FILL ARRAY VALIDATION:
c   Universe 40: Standard fuel compact (214 cells)
c   Universe 50: Control rod compact (1 cell)
c   Expected occurrences: 40 appears ~224 times, 50 appears 1 time
c   Total array size: 225 values (15×15×1)
c
200 0 -200 lat=1 u=10 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
    ...
```

### 7. Universe Reference Map

**Create reference map at top of file**:
```
c ============================================================================
c UNIVERSE REFERENCE MAP
c ============================================================================
c u=0:  Real world (5 cells)
c   fills: [1, 2]
c
c u=1:  Reactor core (3 cells)
c   fills: [10, 20, 30]
c   filled by: [0]
c
c u=10: Fuel region (2 cells)
c   fills: [100]
c   filled by: [1]
c
c u=100: Fuel pin (5 cells)
c   fills: []
c   filled by: [10]
c ============================================================================
```

### 8. Consistent Fill Array Formatting

**Format fill arrays for readability**:
```
c GOOD: Aligned, symmetric, easy to verify
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 3 3 2 1
    1 2 3 4 3 2 1
    1 2 3 3 3 2 1
    1 2 2 2 2 2 1
    1 1 1 1 1 1 1

c BAD: Unaligned, hard to verify
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1 1 2 2 2 2 2 1 1 2 3 3 3 2 1 1 2 3 4 3 2 1
    1 2 3 3 3 2 1 1 2 2 2 2 2 1 1 1 1 1 1 1 1
```

### 9. Pre-Validation Before MCNP

**Always validate cell cards before running**:
```bash
# Command-line validation
python -c "
from mcnp_cell_checker import MCNPCellChecker
checker = MCNPCellChecker()
results = checker.check_cells('input.inp')
if not results['valid']:
    print('ERRORS FOUND - FIX BEFORE RUNNING')
    exit(1)
"

# If validation passes, then run MCNP
if [ $? -eq 0 ]; then
    mcnp6 i=input.inp
fi
```

### 10. Document Universe Purpose

**Add purpose comments to universe definitions**:
```
c ============================================================================
c UNIVERSE 50: TRISO PARTICLE (5-layer coated particle)
c Purpose: Represents single TRISO fuel particle with kernel + 4 coatings
c Used in: Universe 40 (fuel compact particle lattice)
c Nesting level: 5
c ============================================================================
501 1 7.086e-2 -501 u=50 imp:n=1              $ UCO kernel
502 2 5.0147e-2 501 -502 u=50 imp:n=1         $ Buffer layer
503 3 1.9e-1 502 -503 u=50 imp:n=1            $ IPyC layer
504 4 3.18e-1 503 -504 u=50 imp:n=1           $ SiC layer
505 5 1.9e-1 504 -505 u=50 imp:n=1            $ OPyC layer
```

## Integration with Other Skills

### With mcnp-input-validator

Cell checker complements input validator:

```python
from mcnp_input_validator import MCNPInputValidator
from mcnp_cell_checker import MCNPCellChecker

def complete_input_validation(input_file):
    """Comprehensive input validation including cell-specific checks"""

    # Step 1: Basic input validation
    validator = MCNPInputValidator()
    input_results = validator.validate_file(input_file)

    if not input_results['valid']:
        print("❌ BASIC VALIDATION FAILED")
        return False

    # Step 2: Cell-specific validation
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)

    if not cell_results['valid']:
        print("❌ CELL VALIDATION FAILED")
        return False

    print("✓ COMPLETE VALIDATION PASSED")
    return True
```

### With mcnp-geometry-checker

Cell checker validates cell parameters, geometry checker validates spatial relationships:

```python
from mcnp_geometry_checker import MCNPGeometryChecker
from mcnp_cell_checker import MCNPCellChecker

def validate_repeated_structures(input_file):
    """Validate both cell parameters and geometry for lattices"""

    # Check cell cards (universe/lattice/fill)
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)

    # Check geometry (overlaps/gaps)
    geom_checker = MCNPGeometryChecker()
    geom_results = geom_checker.check_geometry(input_file)

    # Both must pass
    return cell_results['valid'] and len(geom_results['errors']) == 0
```

### With mcnp-lattice-builder

Cell checker validates lattices created by lattice builder:

```python
from mcnp_lattice_builder import MCNPLatticeBuilder
from mcnp_cell_checker import MCNPCellChecker

def build_and_validate_lattice(params):
    """Build lattice and immediately validate"""

    # Build lattice
    builder = MCNPLatticeBuilder()
    lattice_cards = builder.create_lattice(**params)

    # Write to temporary file
    with open('temp_lattice.inp', 'w') as f:
        f.write(lattice_cards)

    # Validate
    checker = MCNPCellChecker()
    results = checker.validate_lattices('temp_lattice.inp')

    # Return cards only if valid
    if all(not r['errors'] for r in results.values()):
        return lattice_cards
    else:
        raise ValueError("Generated lattice failed validation")
```

## Example Workflows

### Example 1: Quick Universe Check

**Scenario**: User asks "Did I define all my universes correctly?"

```python
from mcnp_cell_checker import MCNPCellChecker

# Quick check
checker = MCNPCellChecker()
universe_check = checker.validate_universes('reactor_core.inp')

# Report
print("Universe Validation Report")
print("=" * 60)
print(f"Defined universes: {len(universe_check['defined'])}")
print(f"  {universe_check['defined']}")
print(f"\nReferenced universes: {len(universe_check['used'])}")
print(f"  {universe_check['used']}")

if universe_check['undefined']:
    print(f"\n❌ UNDEFINED REFERENCES: {universe_check['undefined']}")
    print("   These universes are used in FILL but not defined with u=")
else:
    print("\n✓ All universe references valid")

unused = set(universe_check['defined']) - set(universe_check['used'])
if unused:
    print(f"\n⚠ UNUSED DEFINITIONS: {unused}")
    print("   These universes are defined but never used")
```

### Example 2: Full Cell Validation Workflow

**Scenario**: User preparing for production run

```python
from mcnp_cell_checker import MCNPCellChecker

def production_cell_validation(input_file):
    """Comprehensive pre-production cell validation"""
    print(f"Production Cell Validation: {input_file}")
    print("=" * 70)

    checker = MCNPCellChecker()

    # Full validation
    results = checker.check_cells(input_file)

    # Report errors (blockers)
    if results['errors']:
        print("\n❌ FATAL ERRORS (must fix):")
        for i, err in enumerate(results['errors'], 1):
            print(f"  {i}. {err}")
        print("\n✗ VALIDATION FAILED - Cannot proceed to production")
        return False

    # Report warnings (should review)
    if results['warnings']:
        print("\n⚠ WARNINGS (review recommended):")
        for warn in results['warnings']:
            print(f"  • {warn}")

    # Report info (FYI)
    if results['info']:
        print("\n📝 INFORMATION:")
        for info in results['info']:
            print(f"  • {info}")

    # Success
    print("\n✓ CELL VALIDATION PASSED")
    print("  Ready for production run")
    print("=" * 70)
    return True

# Run validation
if production_cell_validation('gt_mhr_core.inp'):
    print("\nProceed with MCNP execution")
else:
    print("\nFix errors and re-validate")
```

### Example 3: Lattice-Specific Validation

**Scenario**: User debugging lattice issues

```python
from mcnp_cell_checker import MCNPCellChecker

# Focus on lattice cells
checker = MCNPCellChecker()

# Get lattice-specific results
lattice_results = checker.validate_lattices('fuel_assembly.inp')
fill_check = checker.check_fill_dimensions('fuel_assembly.inp')
boundary_check = checker.check_lattice_boundaries('fuel_assembly.inp')

# Detailed lattice report
for cell_num in lattice_results.keys():
    print(f"\n{'=' * 70}")
    print(f"CELL {cell_num} LATTICE ANALYSIS")
    print('=' * 70)

    # Type
    lat_type = lattice_results[cell_num]['lat_type']
    type_name = "Cubic (hexahedral)" if lat_type == 1 else "Hexagonal (prism)"
    print(f"Lattice Type: LAT={lat_type} ({type_name})")

    # Fill validation
    if cell_num in fill_check:
        fill_info = fill_check[cell_num]
        print(f"\nFill Array:")
        print(f"  Declaration: {fill_info['declaration']}")
        print(f"  Expected: {fill_info['expected_size']} values")
        print(f"  Actual: {fill_info['actual_size']} values")

        if fill_info['expected_size'] == fill_info['actual_size']:
            print(f"  Status: ✓ Correct size")
        else:
            diff = fill_info['actual_size'] - fill_info['expected_size']
            print(f"  Status: ✗ Size mismatch ({diff:+d})")

    # Boundary validation
    if cell_num in boundary_check:
        boundary_info = boundary_check[cell_num]
        print(f"\nBoundary Surfaces:")
        print(f"  Surfaces: {boundary_info['surfaces']}")

        if boundary_info['appropriate']:
            print(f"  Status: ✓ Appropriate for LAT={lat_type}")
        else:
            print(f"  Status: ⚠ Non-standard")
            print(f"  Recommendations:")
            for rec in boundary_info['recommendations']:
                print(f"    • {rec}")

    # Errors
    if lattice_results[cell_num]['errors']:
        print(f"\n❌ ERRORS:")
        for err in lattice_results[cell_num]['errors']:
            print(f"  • {err}")
```

## Dependencies

- **Python >= 3.8**
- **parsers/input_parser.py**: For parsing MCNP input files
- **utils/geometry_evaluator.py**: For extracting surface numbers from geometry strings

## References

### MCNP Manual Chapters

- **Chapter 5.2 - Cell Cards**: Complete cell card syntax and parameters
- **Chapter 5.5.5 - Repeated Structures**: Universe (U), lattice (LAT), and fill (FILL) cards
- **Chapter 5.5.5.1 - U: Universe Keyword**: Universe definitions and hierarchy
- **Chapter 5.5.5.2 - LAT: Lattice**: Lattice types and indexing
- **Chapter 5.5.5.3 - FILL: Fill**: Fill specifications and array declarations
- **Chapter 5.5.4 - TRCL: Cell Coordinate Transformation**: Cell transformations
- **Chapter 3.4.1**: Best practices for geometry setup (items 1-7)
- **Chapter 10.1.3**: Repeated structures examples

### Related Skills

- **mcnp-input-validator**: General input file validation (syntax, cross-references)
- **mcnp-geometry-checker**: Geometry overlaps, gaps, lost particles
- **mcnp-cross-reference-checker**: Dependency analysis and orphaned entities
- **mcnp-lattice-builder**: Creating lattice structures (validates with this skill)
- **mcnp-geometry-builder**: Building cell cards (uses universe features)

### Bug Report Documentation

- **BUG_REPORT_AND_FIXES.md**: Specification for this skill from GT-MHR validation
- **gt_mhr_validation_report.md**: Example complex geometry using universes/lattices

---

**END OF MCNP CELL CHECKER SKILL**
