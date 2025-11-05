# Python API Reference - mcnp_cell_checker

Complete API documentation for the MCNPCellChecker validation class.

## Overview

The `mcnp_cell_checker` module provides programmatic cell card validation for MCNP input files. It focuses on universe references, lattice specifications, fill array dimensions, dependency hierarchies, and boundary surfaces.

---

## Installation

```python
# Add scripts/ directory to Python path
import sys
sys.path.append('path/to/mcnp-cell-checker/scripts')

from mcnp_cell_checker import MCNPCellChecker
```

**Dependencies:**
- Python >= 3.8
- Standard library only (no external packages required)

---

## Class: MCNPCellChecker

### Constructor

```python
checker = MCNPCellChecker()
```

**Parameters:** None

**Returns:** MCNPCellChecker instance

**Example:**
```python
from mcnp_cell_checker import MCNPCellChecker

# Initialize checker
checker = MCNPCellChecker()
```

---

## Method: validate_universes()

Validates that all `fill=` references have corresponding `u=` definitions.

### Signature

```python
validate_universes(input_file: str) -> dict
```

### Parameters

- **input_file** (str): Path to MCNP input file (.inp, .i, or .txt)

### Returns

Dictionary with keys:
- **'defined'** (list): List of defined universe numbers (from u= parameters)
- **'used'** (list): List of referenced universe numbers (from fill= parameters)
- **'undefined'** (list): List of universes referenced but not defined
- **'valid'** (bool): True if no undefined references

### Example

```python
checker = MCNPCellChecker()
result = checker.validate_universes('reactor_core.inp')

print(f"Defined universes: {result['defined']}")
# Output: [1, 2, 3, 10, 20, 50, 100]

print(f"Used universes: {result['used']}")
# Output: [1, 2, 10, 20, 50]

print(f"Undefined references: {result['undefined']}")
# Output: []

if result['valid']:
    print("✓ All universe references are valid")
else:
    print(f"✗ {len(result['undefined'])} undefined references")
```

### Detailed Example

```python
# Check for problems
universe_check = checker.validate_universes('input.inp')

if universe_check['undefined']:
    print("❌ FATAL: Undefined universe references:")
    for u in universe_check['undefined']:
        print(f"  Universe {u} referenced in FILL but not defined")
    sys.exit(1)

# Check for unused definitions (warning only)
unused = set(universe_check['defined']) - set(universe_check['used'])
if unused:
    print(f"⚠ WARNING: Unused universes: {unused}")
    print("  These universes are defined but never used")

# Success
print(f"✓ All {len(universe_check['used'])} universe references valid")
```

---

## Method: validate_lattices()

Validates lattice type specifications (LAT=1 or LAT=2) and associated requirements.

### Signature

```python
validate_lattices(input_file: str) -> dict
```

### Parameters

- **input_file** (str): Path to MCNP input file

### Returns

Dictionary mapping cell numbers to validation results:
```python
{
    cell_number: {
        'lat_type': int,           # 1 or 2
        'has_fill': bool,          # True if fill= present
        'fill_valid': bool,        # True if fill specification valid
        'material_ok': bool,       # True if material is 0 (void)
        'surface_count': int,      # Number of bounding surfaces
        'errors': list,            # List of error messages
        'warnings': list           # List of warning messages
    }
}
```

### Example

```python
checker = MCNPCellChecker()
lattice_results = checker.validate_lattices('input.inp')

for cell_num, result in lattice_results.items():
    lat_type = result['lat_type']
    type_name = "Cubic" if lat_type == 1 else "Hexagonal"

    print(f"Cell {cell_num} (LAT={lat_type} {type_name}):")

    if result['errors']:
        print("  Errors:")
        for err in result['errors']:
            print(f"    ✗ {err}")
    else:
        print("  ✓ Valid")

    if result['warnings']:
        print("  Warnings:")
        for warn in result['warnings']:
            print(f"    ⚠ {warn}")
```

### Detailed Example

```python
# Comprehensive lattice validation
lattice_results = checker.validate_lattices('fuel_assembly.inp')

fatal_errors = []
warnings = []

for cell_num, result in lattice_results.items():
    # Check for fatal errors
    if result['errors']:
        fatal_errors.extend(result['errors'])

    # Collect warnings
    if result['warnings']:
        warnings.extend(result['warnings'])

    # Display cell information
    print(f"\nCell {cell_num}:")
    print(f"  Lattice type: LAT={result['lat_type']}")
    print(f"  Has FILL: {result['has_fill']}")
    print(f"  Material: {'void' if result['material_ok'] else 'non-void'}")
    print(f"  Surface count: {result['surface_count']}")

if fatal_errors:
    print("\n❌ FATAL ERRORS (must fix):")
    for err in fatal_errors:
        print(f"  • {err}")
    sys.exit(1)

if warnings:
    print("\n⚠ WARNINGS (review recommended):")
    for warn in warnings:
        print(f"  • {warn}")

print("\n✓ Lattice validation passed")
```

---

## Method: check_fill_dimensions()

Validates fill array sizes match lattice declarations.

### Signature

```python
check_fill_dimensions(input_file: str) -> dict
```

### Parameters

- **input_file** (str): Path to MCNP input file

### Returns

Dictionary mapping cell numbers to dimension results:
```python
{
    cell_number: {
        'declaration': str,        # fill= declaration string
        'i_range': tuple,          # (i1, i2)
        'j_range': tuple,          # (j1, j2)
        'k_range': tuple,          # (k1, k2)
        'dimensions': tuple,       # (i_size, j_size, k_size)
        'expected_size': int,      # Required number of values
        'actual_size': int,        # Provided number of values
        'array_values': list,      # Actual universe IDs
        'valid': bool              # True if sizes match
    }
}
```

### Example

```python
checker = MCNPCellChecker()
fill_check = checker.check_fill_dimensions('input.inp')

for cell_num, result in fill_check.items():
    print(f"\nCell {cell_num}:")
    print(f"  Declaration: {result['declaration']}")
    print(f"  Dimensions: {result['dimensions']}")
    print(f"  Expected: {result['expected_size']} values")
    print(f"  Actual: {result['actual_size']} values")

    if result['valid']:
        print(f"  ✓ Correct size")
    else:
        diff = result['actual_size'] - result['expected_size']
        print(f"  ✗ Size mismatch ({diff:+d})")
```

### Detailed Example with Universe Analysis

```python
# Comprehensive fill array analysis
fill_check = checker.check_fill_dimensions('core_lattice.inp')

for cell_num, result in fill_check.items():
    print(f"\n{'='*70}")
    print(f"Cell {cell_num} Fill Array Analysis")
    print('='*70)

    # Dimensions
    i_size, j_size, k_size = result['dimensions']
    print(f"Declaration: {result['declaration']}")
    print(f"Dimensions: {i_size} × {j_size} × {k_size}")
    print(f"Expected: {result['expected_size']} values")
    print(f"Actual: {result['actual_size']} values")

    # Validation
    if not result['valid']:
        diff = result['actual_size'] - result['expected_size']
        print(f"\n❌ SIZE MISMATCH: {diff:+d} values")
        if diff < 0:
            print(f"   Missing {-diff} values")
        else:
            print(f"   Extra {diff} values")
        continue

    print("✓ Size matches\n")

    # Universe composition analysis
    array_values = result['array_values']
    unique_universes = set(array_values) - {0}

    print(f"Universe Composition:")
    for u in sorted(unique_universes):
        count = array_values.count(u)
        percentage = (count / len(array_values)) * 100
        print(f"  u={u}: {count:3d} times ({percentage:5.1f}%)")
```

---

## Method: build_universe_tree()

Constructs complete universe hierarchy and detects circular references.

### Signature

```python
build_universe_tree(input_file: str) -> dict
```

### Parameters

- **input_file** (str): Path to MCNP input file

### Returns

Dictionary with universe hierarchy information:
```python
{
    'universes': {
        universe_number: {
            'cells': list,         # Cell numbers in this universe
            'fills': list,         # Universe numbers this one fills (children)
            'filled_by': list,     # Universe numbers that fill this (parents)
            'level': int           # Hierarchy level (0 = real world)
        }
    },
    'max_depth': int,              # Maximum nesting level
    'circular_refs': list,         # List of circular reference cycles
    'unreachable': list            # Universes not connected to real world
}
```

### Example

```python
checker = MCNPCellChecker()
tree = checker.build_universe_tree('reactor.inp')

print(f"Universe hierarchy depth: {tree['max_depth']} levels")

if tree['circular_refs']:
    print("\n❌ CIRCULAR REFERENCES:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))} → (loops back)")
else:
    print("✓ No circular references")

if tree['unreachable']:
    print(f"\n⚠ UNREACHABLE UNIVERSES: {tree['unreachable']}")
```

### Detailed Example with Tree Visualization

```python
# Build and visualize hierarchy
tree = checker.build_universe_tree('complex_reactor.inp')

def print_tree(u, indent=0, universe_info=None):
    """Recursively print universe tree"""
    if universe_info is None:
        universe_info = tree['universes']

    info = universe_info[u]
    indent_str = "  " * indent

    # Format universe info
    if u == 0:
        name = "u=0 (real world)"
    else:
        name = f"u={u}"

    cell_count = len(info['cells'])
    level = info['level']
    fills_str = str(info['fills']) if info['fills'] else "none"

    print(f"{indent_str}{name}: level {level}, {cell_count} cells, fills={fills_str}")

    # Recursively print children
    for child_u in sorted(info['fills']):
        print_tree(child_u, indent + 1, universe_info)

print("\nUniverse Hierarchy:")
print_tree(0)

# Performance analysis
print(f"\nPerformance Analysis:")
print(f"  Max nesting depth: {tree['max_depth']} levels")

if tree['max_depth'] <= 3:
    print("  ✓ Shallow nesting (optimal performance)")
elif tree['max_depth'] <= 7:
    print("  ✓ Moderate nesting (acceptable)")
    print("  💡 Consider negative universe optimization for levels 3+")
elif tree['max_depth'] <= 10:
    print("  ⚠ Deep nesting (performance impact expected)")
    print("  💡 Apply negative universe optimization")
    print("  💡 Consider combining levels")
else:
    print("  ❌ Excessive nesting (significant performance penalty)")
    print("  💡 Simplify geometry or homogenize lower levels")
```

---

## Method: check_lattice_boundaries()

Validates lattice boundary surface types are appropriate.

### Signature

```python
check_lattice_boundaries(input_file: str) -> dict
```

### Parameters

- **input_file** (str): Path to MCNP input file

### Returns

Dictionary mapping cell numbers to boundary analysis:
```python
{
    cell_number: {
        'lat_type': int,           # 1 or 2
        'surfaces': list,          # Surface numbers
        'surface_types': list,     # Surface type strings
        'appropriate': bool,       # True if surfaces are appropriate
        'recommendations': list    # Suggestions for improvement
    }
}
```

### Example

```python
checker = MCNPCellChecker()
boundary_check = checker.check_lattice_boundaries('input.inp')

for cell_num, result in boundary_check.items():
    lat_type = result['lat_type']
    print(f"\nCell {cell_num} (LAT={lat_type}):")
    print(f"  Surfaces: {result['surfaces']}")
    print(f"  Types: {result['surface_types']}")

    if result['appropriate']:
        print("  ✓ Boundary surfaces appropriate")
    else:
        print("  ⚠ Non-standard boundaries")
        print("  Recommendations:")
        for rec in result['recommendations']:
            print(f"    • {rec}")
```

---

## Method: check_cells()

Runs all validations in a single comprehensive check.

### Signature

```python
check_cells(input_file: str) -> dict
```

### Parameters

- **input_file** (str): Path to MCNP input file

### Returns

Dictionary with comprehensive results:
```python
{
    'valid': bool,                 # True if all checks passed
    'errors': list,                # Fatal errors (must fix)
    'warnings': list,              # Warnings (should review)
    'info': list,                  # Informational messages
    'universe_check': dict,        # Results from validate_universes()
    'lattice_check': dict,         # Results from validate_lattices()
    'fill_check': dict,            # Results from check_fill_dimensions()
    'tree': dict,                  # Results from build_universe_tree()
    'boundary_check': dict         # Results from check_lattice_boundaries()
}
```

### Example

```python
checker = MCNPCellChecker()
results = checker.check_cells('reactor.inp')

# Display results
if results['errors']:
    print("❌ FATAL ERRORS:")
    for err in results['errors']:
        print(f"  • {err}")

if results['warnings']:
    print("\n⚠ WARNINGS:")
    for warn in results['warnings']:
        print(f"  • {warn}")

if results['info']:
    print("\n📝 INFORMATION:")
    for info in results['info']:
        print(f"  • {info}")

# Overall status
if results['valid']:
    print("\n✓ CELL VALIDATION PASSED")
    print("  Ready for MCNP execution")
else:
    print("\n✗ CELL VALIDATION FAILED")
    print("  Fix errors before running MCNP")
```

---

## Complete Workflow Example

### Pre-Run Validation Script

```python
#!/usr/bin/env python3
"""
Complete cell card validation before MCNP run
Usage: python validate_cells.py input.inp
"""

import sys
from mcnp_cell_checker import MCNPCellChecker

def validate_cell_cards(input_file):
    """Comprehensive pre-run validation"""
    print(f"{'='*70}")
    print(f"Cell Card Validation: {input_file}")
    print(f"{'='*70}")

    checker = MCNPCellChecker()

    # Step 1: Universe references
    print("\n[1/5] Checking universe references...")
    universe_check = checker.validate_universes(input_file)

    if universe_check['undefined']:
        print("  ❌ FATAL: Undefined universe references:")
        for u in universe_check['undefined']:
            print(f"     Universe {u} referenced but not defined")
        return False
    else:
        print(f"  ✓ All {len(universe_check['used'])} references valid")

    # Step 2: Lattice types
    print("\n[2/5] Validating lattice specifications...")
    lattice_results = checker.validate_lattices(input_file)

    lattice_errors = sum(len(r['errors']) for r in lattice_results.values())
    if lattice_errors:
        print(f"  ❌ FATAL: {lattice_errors} lattice errors")
        for cell, result in lattice_results.items():
            if result['errors']:
                for err in result['errors']:
                    print(f"     Cell {cell}: {err}")
        return False
    else:
        print(f"  ✓ All {len(lattice_results)} lattice cells valid")

    # Step 3: Fill dimensions
    print("\n[3/5] Checking fill array dimensions...")
    fill_check = checker.check_fill_dimensions(input_file)

    dimension_errors = sum(1 for r in fill_check.values()
                          if not r['valid'])
    if dimension_errors:
        print(f"  ❌ FATAL: {dimension_errors} dimension mismatches")
        for cell, result in fill_check.items():
            if not result['valid']:
                print(f"     Cell {cell}: Expected {result['expected_size']}, "
                      f"found {result['actual_size']}")
        return False
    else:
        print("  ✓ All fill array dimensions correct")

    # Step 4: Dependency tree
    print("\n[4/5] Building universe dependency tree...")
    tree = checker.build_universe_tree(input_file)

    if tree['circular_refs']:
        print("  ❌ FATAL: Circular references:")
        for cycle in tree['circular_refs']:
            print(f"     {' → '.join(map(str, cycle))}")
        return False
    else:
        print(f"  ✓ No circular references (depth: {tree['max_depth']})")

    if tree['max_depth'] > 10:
        print(f"  ⚠ Deep nesting ({tree['max_depth']} levels)")

    # Step 5: Boundaries
    print("\n[5/5] Checking lattice boundaries...")
    boundary_check = checker.check_lattice_boundaries(input_file)

    non_standard = sum(1 for r in boundary_check.values()
                       if not r['appropriate'])
    if non_standard:
        print(f"  ⚠ {non_standard} non-standard boundaries")
    else:
        print("  ✓ All lattice boundaries appropriate")

    # Final summary
    print(f"\n{'='*70}")
    print("✓ CELL VALIDATION PASSED")
    print(f"  • {len(universe_check['defined'])} universes")
    print(f"  • {len(lattice_results)} lattice cells")
    print(f"  • {tree['max_depth']} nesting levels")
    print("  • Ready for MCNP execution")
    print(f"{'='*70}")

    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_cells.py input.inp")
        sys.exit(1)

    input_file = sys.argv[1]

    if validate_cell_cards(input_file):
        print(f"\n✓ Ready to run: mcnp6 i={input_file}")
        sys.exit(0)
    else:
        print("\n✗ Fix errors before running MCNP")
        sys.exit(1)
```

---

## Integration Patterns

### With mcnp-input-validator

```python
from mcnp_input_validator import MCNPInputValidator
from mcnp_cell_checker import MCNPCellChecker

def complete_validation(input_file):
    """Comprehensive input validation"""

    # Basic input validation
    validator = MCNPInputValidator()
    input_results = validator.validate_file(input_file)

    if not input_results['valid']:
        print("❌ Basic validation failed")
        return False

    # Cell-specific validation
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)

    if not cell_results['valid']:
        print("❌ Cell validation failed")
        return False

    print("✓ Complete validation passed")
    return True
```

### With mcnp-lattice-builder

```python
from mcnp_lattice_builder import MCNPLatticeBuilder
from mcnp_cell_checker import MCNPCellChecker

def build_and_validate_lattice(params):
    """Build lattice and validate immediately"""

    # Build lattice
    builder = MCNPLatticeBuilder()
    lattice_cards = builder.create_lattice(**params)

    # Write to temp file
    with open('temp_lattice.inp', 'w') as f:
        f.write(lattice_cards)

    # Validate
    checker = MCNPCellChecker()
    results = checker.validate_lattices('temp_lattice.inp')

    # Check validity
    if all(not r['errors'] for r in results.values()):
        return lattice_cards
    else:
        raise ValueError("Generated lattice failed validation")
```

---

## Error Handling

All methods handle errors gracefully and return structured results. No exceptions are raised for validation failures (only for file I/O errors).

```python
try:
    checker = MCNPCellChecker()
    results = checker.check_cells('input.inp')
except FileNotFoundError:
    print("Error: Input file not found")
except PermissionError:
    print("Error: Cannot read input file (permission denied)")
except Exception as e:
    print(f"Error: {e}")
```

---

**END OF PYTHON API REFERENCE**
