# MCNP Cell Checker - Detailed Examples

**Purpose:** Complete workflow examples and integration patterns

---

## Example 1: Quick Universe Check

**Scenario**: User asks "Did I define all my universes correctly?"

### Implementation

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

---

## Example 2: Full Cell Validation Workflow

**Scenario**: User preparing for production run

### Implementation

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

---

## Example 3: Lattice-Specific Validation

**Scenario**: User debugging lattice issues

### Implementation

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

---

## Integration Example 1: With mcnp-input-validator

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

---

## Integration Example 2: With mcnp-geometry-checker

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

---

## Integration Example 3: With mcnp-lattice-builder

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

---

## Complete Pre-Run Validation Script

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

**END OF DETAILED EXAMPLES**
