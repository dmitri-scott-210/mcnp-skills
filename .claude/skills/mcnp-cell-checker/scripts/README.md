# MCNP Cell Checker - Scripts

Python automation tools for validating MCNP cell cards with focus on universe, lattice, and fill features.

---

## mcnp_cell_checker.py

**Purpose**: Main validation module for cell card features

**Usage**:
```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
results = checker.check_cells('input.inp')
```

**Key Methods**:

### validate_universes(input_file)
Check all universe definitions and references.

**Returns**:
```python
{
    'defined': [1, 2, 3, ...],        # Universe numbers defined with u=
    'used': [1, 2, 3, ...],           # Universe numbers referenced in fill=
    'undefined': [],                   # Referenced but not defined
}
```

**Example**:
```python
universe_check = checker.validate_universes('reactor.inp')
if universe_check['undefined']:
    print(f"❌ Undefined universes: {universe_check['undefined']}")
```

---

### validate_lattices(input_file)
Validate all lattice type specifications.

**Returns**:
```python
{
    cell_number: {
        'lat_type': 1 or 2,
        'has_fill': True/False,
        'fill_valid': True/False,
        'errors': [list of error messages]
    },
    ...
}
```

**Example**:
```python
lattice_results = checker.validate_lattices('input.inp')
for cell, result in lattice_results.items():
    if result['errors']:
        print(f"Cell {cell}: {result['errors']}")
```

---

### check_fill_dimensions(input_file)
Validate fill array sizes match lattice declarations.

**Returns**:
```python
{
    cell_number: {
        'expected_size': 225,           # Calculated from fill= declaration
        'actual_size': 225,             # Count of array values
        'declaration': 'fill= -7:7 -7:7 0:0',
    },
    ...
}
```

**Example**:
```python
fill_check = checker.check_fill_dimensions('input.inp')
for cell, result in fill_check.items():
    if result['expected_size'] != result['actual_size']:
        print(f"Cell {cell}: Dimension mismatch")
        print(f"  Expected: {result['expected_size']}")
        print(f"  Found: {result['actual_size']}")
```

---

### build_universe_tree(input_file)
Build complete universe hierarchy and detect circular references.

**Returns**:
```python
{
    'universes': {
        0: {'cells': [1, 2, 999], 'fills': [1], 'level': 0},
        1: {'cells': [100, 200], 'fills': [2, 3], 'level': 1},
        ...
    },
    'max_depth': 6,
    'circular_refs': []  # List of circular dependency cycles
}
```

**Example**:
```python
tree = checker.build_universe_tree('reactor.inp')
print(f"Max nesting: {tree['max_depth']} levels")

if tree['circular_refs']:
    print("❌ Circular references:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))}")
```

---

### check_lattice_boundaries(input_file)
Check lattice cells have appropriate boundary surfaces.

**Returns**:
```python
{
    cell_number: {
        'lat_type': 1 or 2,
        'surfaces': [list of surface numbers],
        'appropriate': True/False,
        'recommendations': [list of suggestions]
    },
    ...
}
```

**Example**:
```python
boundary_check = checker.check_lattice_boundaries('input.inp')
for cell, result in boundary_check.items():
    if not result['appropriate']:
        print(f"Cell {cell} recommendations:")
        for rec in result['recommendations']:
            print(f"  • {rec}")
```

---

### check_cells(input_file)
Run all validation checks and return comprehensive results.

**Returns**:
```python
{
    'valid': True/False,              # Overall pass/fail
    'errors': [list of fatal errors],
    'warnings': [list of warnings],
    'info': [list of informational messages]
}
```

**Example**:
```python
results = checker.check_cells('input.inp')

if results['valid']:
    print("✓ All cell validation passed")
else:
    print("❌ Validation failed:")
    for err in results['errors']:
        print(f"  {err}")
```

---

## Command-Line Usage

### Quick Universe Check
```bash
python -c "
from mcnp_cell_checker import MCNPCellChecker
checker = MCNPCellChecker()
results = checker.validate_universes('input.inp')
print(f\"Defined: {results['defined']}\")
print(f\"Used: {results['used']}\")
print(f\"Undefined: {results['undefined']}\")
"
```

### Complete Validation
```bash
python -c "
from mcnp_cell_checker import MCNPCellChecker
import sys
checker = MCNPCellChecker()
results = checker.check_cells('input.inp')
if not results['valid']:
    print('VALIDATION FAILED')
    sys.exit(1)
print('VALIDATION PASSED')
"
```

### Pre-Run Validation Script
```bash
#!/bin/bash
# validate_before_run.sh

INPUT_FILE=$1

python -c "
from mcnp_cell_checker import MCNPCellChecker
import sys

checker = MCNPCellChecker()
results = checker.check_cells('$INPUT_FILE')

if results['valid']:
    print('✓ Cell validation passed')
    sys.exit(0)
else:
    print('❌ Cell validation failed:')
    for err in results['errors']:
        print(f'  {err}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "Proceeding with MCNP..."
    mcnp6 i=$INPUT_FILE
else
    echo "Fix errors before running MCNP"
fi
```

---

## Integration Examples

### With mcnp-input-validator
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
    if not checker.check_cells(input_file)['valid']:
        return False

    return True
```

### Batch Validation
```python
from mcnp_cell_checker import MCNPCellChecker
import glob

checker = MCNPCellChecker()
for input_file in glob.glob("*.inp"):
    results = checker.check_cells(input_file)
    status = "✓" if results['valid'] else "❌"
    print(f"{status} {input_file}")
```

---

## Dependencies

- Python >= 3.8
- Standard library only (no external packages required)

---

## Error Handling

The checker provides three levels of feedback:

1. **Errors** (fatal, must fix):
   - Undefined universe references
   - Invalid lattice types
   - Fill array dimension mismatches
   - Circular universe dependencies

2. **Warnings** (should review):
   - Unused universe definitions
   - Deep nesting (>10 levels)
   - Non-standard boundary surfaces
   - Lattice cells with materials

3. **Info** (informational):
   - Universe hierarchy statistics
   - Lattice configuration details
   - Optimization suggestions

---

## Performance

**Typical validation times**:
- Small input (<1000 cells): <1 second
- Medium input (1000-5000 cells): 1-5 seconds
- Large input (>5000 cells): 5-15 seconds

**Memory usage**: Minimal (~10-50 MB for most inputs)

---

**END OF SCRIPTS README**
