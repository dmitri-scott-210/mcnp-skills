# MCNP Cell Checker Scripts

Python automation tools for validating MCNP cell cards with universe/lattice/fill features.

---

## Installation

```bash
# No external dependencies required (uses Python standard library)
python --version  # Requires Python 3.8+
```

---

## Quick Start

### Command-Line Usage

```bash
# Basic validation
python mcnp_cell_checker.py input.inp

# Output shows validation results
# Exit code: 0 = passed, 1 = failed
```

### Python API Usage

```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
results = checker.check_cells('input.inp')

if results['valid']:
    print("✓ Validation passed")
else:
    print(f"✗ Found {len(results['errors'])} errors")
```

---

## Scripts Overview

### 1. mcnp_cell_checker.py

**Purpose:** Main validation class coordinating all checks

**Usage:**
```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
results = checker.check_cells('reactor.inp')

# Returns dict with:
#   - 'valid': bool
#   - 'errors': list of error messages
#   - 'warnings': list of warning messages
#   - 'info': list of informational messages
```

**Command line:**
```bash
python mcnp_cell_checker.py reactor.inp
```

---

### 2. universe_validator.py

**Purpose:** Validate universe definitions and references

**Usage:**
```python
from scripts.universe_validator import UniverseValidator

validator = UniverseValidator()
results = validator.validate_universes('input.inp')

# Returns dict with:
#   - 'defined': set of universe numbers with u=
#   - 'used': set of universe numbers in fill=
#   - 'undefined': set of used but not defined

print(f"Defined: {results['defined']}")
print(f"Used: {results['used']}")
print(f"Undefined: {results['undefined']}")
```

**Checks:**
- All `fill=N` references have corresponding `u=N` definitions
- Universe 0 not explicitly used
- Identifies unused universe definitions (warning)

---

### 3. lattice_validator.py

**Purpose:** Validate lattice specifications and fill arrays

**Usage:**
```python
from scripts.lattice_validator import LatticeValidator

validator = LatticeValidator()

# Check lattice types
lattice_results = validator.validate_lattices('input.inp')
for cell_num, result in lattice_results.items():
    print(f"Cell {cell_num}: LAT={result['lat_type']}")
    if result['errors']:
        print(f"  Errors: {result['errors']}")

# Check fill array dimensions
fill_results = validator.check_fill_dimensions('input.inp')
for cell_num, result in fill_results.items():
    print(f"Cell {cell_num}:")
    print(f"  Expected: {result['expected_size']} values")
    print(f"  Actual: {result['actual_size']} values")

# Check boundary surfaces
boundary_results = validator.check_lattice_boundaries('input.inp')
for cell_num, result in boundary_results.items():
    if not result['appropriate']:
        print(f"Cell {cell_num}: {result['recommendations']}")
```

**Checks:**
- LAT value is 1 or 2 only
- Lattice cells have FILL parameter
- Lattice cells are void (material 0)
- Fill array size matches declaration
- Appropriate boundary surfaces for lattice type

---

### 4. dependency_tree_builder.py

**Purpose:** Build universe hierarchy and detect circular references

**Usage:**
```python
from scripts.dependency_tree_builder import DependencyTreeBuilder

builder = DependencyTreeBuilder()
tree = builder.build_universe_tree('input.inp')

# Returns dict with:
#   - 'universes': dict of universe info
#   - 'max_depth': maximum nesting level
#   - 'circular_refs': list of circular references found

print(f"Max depth: {tree['max_depth']} levels")

if tree['circular_refs']:
    print("Circular references:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))}")

# Print hierarchy
for u_num, u_info in sorted(tree['universes'].items()):
    indent = "  " * (u_info['level'] or 0)
    print(f"{indent}u={u_num}: {len(u_info['cells'])} cells")
```

**Checks:**
- Builds complete universe dependency tree
- Calculates nesting depth (level 0 = real world)
- Detects circular references (infinite loops)
- Warns if nesting exceeds 10 levels

---

## Complete Validation Example

```python
from mcnp_cell_checker import MCNPCellChecker

def validate_before_mcnp_run(input_file):
    """Complete pre-run validation"""

    checker = MCNPCellChecker()
    results = checker.check_cells(input_file)

    # Print errors
    if results['errors']:
        print("\n❌ ERRORS:")
        for err in results['errors']:
            print(f"  • {err}")
        return False

    # Print warnings
    if results['warnings']:
        print("\n⚠ WARNINGS:")
        for warn in results['warnings']:
            print(f"  • {warn}")

    # Print info
    print("\n📝 INFO:")
    for info in results['info']:
        print(f"  • {info}")

    return True

# Use in workflow
if validate_before_mcnp_run('reactor.inp'):
    print("\n✓ Ready to run MCNP")
    # Run: mcnp6 i=reactor.inp
else:
    print("\n✗ Fix errors before running MCNP")
```

---

## Integration Examples

### With MCNP Input Validator

```python
from mcnp_input_validator import MCNPInputValidator
from mcnp_cell_checker import MCNPCellChecker

def complete_validation(input_file):
    """Two-stage validation: general + cell-specific"""

    # Stage 1: General input validation
    general_validator = MCNPInputValidator()
    general_results = general_validator.validate_file(input_file)

    if not general_results['valid']:
        return False

    # Stage 2: Cell-specific validation
    cell_checker = MCNPCellChecker()
    cell_results = cell_checker.check_cells(input_file)

    return cell_results['valid']
```

### With MCNP Lattice Builder

```python
from mcnp_lattice_builder import MCNPLatticeBuilder
from mcnp_cell_checker import MCNPCellChecker

def build_and_validate(params):
    """Build lattice and validate immediately"""

    # Build
    builder = MCNPLatticeBuilder()
    lattice_cards = builder.create_lattice(**params)

    # Write temporary file
    with open('temp.inp', 'w') as f:
        f.write(lattice_cards)

    # Validate
    checker = MCNPCellChecker()
    results = checker.check_cells('temp.inp')

    if results['valid']:
        return lattice_cards
    else:
        raise ValueError("Lattice validation failed")
```

---

## Common Issues

### Import Errors

If you see `ModuleNotFoundError`, ensure scripts are in correct location:
```
.claude/skills/mcnp-cell-checker/
├── scripts/
│   ├── mcnp_cell_checker.py
│   ├── universe_validator.py
│   ├── lattice_validator.py
│   ├── dependency_tree_builder.py
│   └── README.md
```

### File Not Found

Provide absolute path or ensure working directory is correct:
```python
import os
input_file = os.path.abspath('input.inp')
```

---

## Testing

```bash
# Test with example file
cd /home/user/mcnp-skills/.claude/skills/mcnp-cell-checker/assets/example_inputs
python ../../scripts/mcnp_cell_checker.py 01_simple_universe_valid.i
```

---

## Support

See main skill documentation:
- `../SKILL.md` - Overview and workflow
- `../validation_procedures.md` - Detailed validation procedures
- `../cell_card_concepts.md` - Universe/lattice concepts
- `../error_catalog.md` - Common problems and solutions
- `../detailed_examples.md` - Complete workflow examples