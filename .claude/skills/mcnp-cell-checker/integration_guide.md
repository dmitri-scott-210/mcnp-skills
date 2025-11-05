# MCNP Cell Checker - Integration Guide

Complete guide for integrating cell checker with other MCNP skills and validation workflows.

---

## Integration with mcnp-input-validator

Cell checker complements input validator by providing specialized cell card validation.

### Complete Input Validation

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
        for err in input_results['errors']:
            print(f"  {err}")
        return False

    # Step 2: Cell-specific validation
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)

    if not cell_results['valid']:
        print("❌ CELL VALIDATION FAILED")
        for err in cell_results['errors']:
            print(f"  {err}")
        return False

    print("✓ COMPLETE VALIDATION PASSED")
    return True
```

### Workflow

```
mcnp-input-validator → Check overall syntax, block structure, cross-references
          ↓
    (If passes)
          ↓
mcnp-cell-checker → Check universe/lattice/fill specifics
          ↓
    (If passes)
          ↓
     Ready for MCNP execution
```

---

## Integration with mcnp-geometry-checker

Cell checker validates cell parameters, geometry checker validates spatial relationships.

### Combined Validation for Lattices

```python
from mcnp_geometry_checker import MCNPGeometryChecker
from mcnp_cell_checker import MCNPCellChecker

def validate_repeated_structures(input_file):
    """Validate both cell parameters and geometry for lattices"""

    # Check cell cards (universe/lattice/fill)
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)

    if not cell_results['valid']:
        print("❌ Cell parameter errors found")
        return False

    # Check geometry (overlaps/gaps)
    geom_checker = MCNPGeometryChecker()
    geom_results = geom_checker.check_geometry(input_file)

    if geom_results['errors']:
        print("❌ Geometry errors found")
        return False

    print("✓ Cell parameters and geometry validated")
    return True
```

### Division of Responsibilities

| Check Type | mcnp-cell-checker | mcnp-geometry-checker |
|------------|-------------------|------------------------|
| Universe references | ✓ | |
| Lattice type (LAT=1/2) | ✓ | |
| Fill array dimensions | ✓ | |
| Nesting depth | ✓ | |
| Circular references | ✓ | |
| Geometry overlaps | | ✓ |
| Geometry gaps | | ✓ |
| Lost particles | | ✓ |
| Surface definitions | | ✓ |

---

## Integration with mcnp-lattice-builder

Cell checker validates lattices created by lattice builder.

### Build and Validate Workflow

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
        print("✓ Lattice validated successfully")
        return lattice_cards
    else:
        print("❌ Generated lattice failed validation:")
        for cell, result in results.items():
            for err in result['errors']:
                print(f"  Cell {cell}: {err}")
        raise ValueError("Generated lattice failed validation")
```

### Recommended Workflow

```
1. mcnp-lattice-builder → Create lattice structure
2. mcnp-cell-checker → Validate LAT/FILL/dimensions
3. mcnp-geometry-checker → Check spatial relationships
4. mcnp-input-validator → Final comprehensive check
```

---

## Integration with mcnp-cross-reference-checker

Cell checker focuses on universe/lattice, cross-reference checker handles broader dependencies.

### Combined Dependency Analysis

```python
from mcnp_cross_reference_checker import MCNPCrossReferenceChecker
from mcnp_cell_checker import MCNPCellChecker

def complete_dependency_analysis(input_file):
    """Analyze all dependency types"""

    print("Checking universe dependencies...")
    cell_checker = MCNPCellChecker()
    tree = cell_checker.build_universe_tree(input_file)

    print(f"  Max nesting: {tree['max_depth']} levels")
    if tree['circular_refs']:
        print("  ❌ Circular universe references found")
        return False

    print("\nChecking all cross-references...")
    xref_checker = MCNPCrossReferenceChecker()
    xref_results = xref_checker.check_all_references(input_file)

    if xref_results['errors']:
        print("  ❌ Cross-reference errors found")
        return False

    print("✓ All dependencies validated")
    return True
```

---

## Integration with mcnp-geometry-builder

Cell checker validates geometry created by geometry builder.

### Build-Validate Loop

```python
from mcnp_geometry_builder import MCNPGeometryBuilder
from mcnp_cell_checker import MCNPCellChecker

def build_reactor_core(config):
    """Build reactor core with validation at each level"""

    builder = MCNPGeometryBuilder()
    checker = MCNPCellChecker()

    # Level 1: Build fuel pin universe
    pin_cells = builder.create_fuel_pin(config['pin'])
    # Validate immediately
    if not validate_universe(pin_cells, checker):
        raise ValueError("Pin universe validation failed")

    # Level 2: Build assembly with pin lattice
    assembly_cells = builder.create_assembly(config['assembly'], pin_universe=1)
    # Validate lattice
    if not validate_lattice(assembly_cells, checker):
        raise ValueError("Assembly lattice validation failed")

    # Level 3: Build core with assembly lattice
    core_cells = builder.create_core(config['core'], assembly_universe=10)
    # Final validation
    if not validate_complete_hierarchy(core_cells, checker):
        raise ValueError("Core hierarchy validation failed")

    return core_cells
```

---

## Pre-Production Validation Script

Complete validation before production runs:

```python
from mcnp_input_validator import MCNPInputValidator
from mcnp_cell_checker import MCNPCellChecker
from mcnp_geometry_checker import MCNPGeometryChecker
from mcnp_cross_reference_checker import MCNPCrossReferenceChecker

def production_validation(input_file):
    """Comprehensive pre-production validation"""

    print("=" * 70)
    print(f"PRODUCTION VALIDATION: {input_file}")
    print("=" * 70)

    # Stage 1: Basic input validation
    print("\n[1/4] Basic input validation...")
    validator = MCNPInputValidator()
    if not validator.validate_file(input_file)['valid']:
        print("  ❌ FAILED - Fix syntax errors first")
        return False
    print("  ✓ PASSED")

    # Stage 2: Cell card validation
    print("\n[2/4] Cell card validation...")
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)
    if not cell_results['valid']:
        print("  ❌ FAILED - Fix cell card errors")
        for err in cell_results['errors'][:5]:  # Show first 5
            print(f"     {err}")
        return False
    print("  ✓ PASSED")

    # Stage 3: Geometry validation
    print("\n[3/4] Geometry validation...")
    geom_checker = MCNPGeometryChecker()
    geom_results = geom_checker.check_geometry(input_file)
    if geom_results['errors']:
        print("  ❌ FAILED - Fix geometry errors")
        for err in geom_results['errors'][:5]:
            print(f"     {err}")
        return False
    print("  ✓ PASSED")

    # Stage 4: Cross-reference validation
    print("\n[4/4] Cross-reference validation...")
    xref_checker = MCNPCrossReferenceChecker()
    xref_results = xref_checker.check_all_references(input_file)
    if xref_results['errors']:
        print("  ❌ FAILED - Fix cross-reference errors")
        for err in xref_results['errors'][:5]:
            print(f"     {err}")
        return False
    print("  ✓ PASSED")

    # Success
    print("\n" + "=" * 70)
    print("✓ ALL VALIDATION STAGES PASSED")
    print("  Ready for production MCNP execution")
    print("=" * 70)
    return True

# Usage
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.inp"

    if production_validation(input_file):
        print(f"\nExecute: mcnp6 i={input_file}")
        sys.exit(0)
    else:
        print("\nFix errors and re-validate")
        sys.exit(1)
```

---

## Batch Validation Script

Validate multiple input files:

```python
from mcnp_cell_checker import MCNPCellChecker
import glob
import os

def batch_cell_validation(pattern="*.inp"):
    """Validate all input files matching pattern"""

    files = glob.glob(pattern)
    checker = MCNPCellChecker()

    results = {}
    for input_file in files:
        print(f"\nValidating: {input_file}")
        print("-" * 60)

        cell_results = checker.check_cells(input_file)

        results[input_file] = {
            'valid': cell_results['valid'],
            'error_count': len(cell_results['errors']),
            'warning_count': len(cell_results['warnings'])
        }

        if cell_results['valid']:
            print(f"  ✓ PASSED ({len(cell_results['warnings'])} warnings)")
        else:
            print(f"  ❌ FAILED ({len(cell_results['errors'])} errors)")

    # Summary
    print("\n" + "=" * 60)
    print("BATCH VALIDATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results.values() if r['valid'])
    failed = len(results) - passed

    print(f"Total files: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        print("\nFailed files:")
        for file, result in results.items():
            if not result['valid']:
                print(f"  {file}: {result['error_count']} errors")

    return passed == len(results)
```

---

## Continuous Integration Example

Integrate cell checker into CI/CD pipeline:

```bash
#!/bin/bash
# ci_validate_inputs.sh

echo "MCNP Input Validation Pipeline"
echo "================================"

# Find all input files
INPUT_FILES=$(find . -name "*.inp" -o -name "*.i")

FAILED=0
for FILE in $INPUT_FILES; do
    echo ""
    echo "Validating: $FILE"
    echo "----------------------------"

    # Run cell checker
    python -c "
from mcnp_cell_checker import MCNPCellChecker
import sys

checker = MCNPCellChecker()
results = checker.check_cells('$FILE')

if not results['valid']:
    print('❌ FAILED')
    for err in results['errors']:
        print(f'  ERROR: {err}')
    sys.exit(1)
else:
    print('✓ PASSED')
    sys.exit(0)
"

    if [ $? -ne 0 ]; then
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "================================"
if [ $FAILED -eq 0 ]; then
    echo "✓ ALL FILES PASSED"
    exit 0
else
    echo "❌ $FAILED FILE(S) FAILED"
    exit 1
fi
```

---

**END OF INTEGRATION_GUIDE.MD**
