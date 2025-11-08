# MCNP Cross-Reference Checker - Scripts Documentation

**Version:** 2.0.0
**Skill:** mcnp-cross-reference-checker

---

## Overview

This directory contains Python scripts for automated cross-reference validation and dependency analysis of MCNP input files.

**Available Scripts:**
1. **cross_reference_validator.py** - Main CLI validation tool (NEW - RECOMMENDED)
2. **mcnp_cross_reference_checker.py** - Legacy validation library
3. **dependency_visualizer.py** - Dependency graph visualization (planned)
4. **reference_fixer.py** - Automated fix suggestions (planned)

---

## Installation

**Requirements:**
```bash
python >= 3.8
```

**No external dependencies required** - uses Python standard library only.

**Optional (for visualization):**
```bash
pip install graphviz  # For DOT format diagrams
```

---

## Script 0: cross_reference_validator.py (RECOMMENDED)

### Description
**NEW in v2.0** - Comprehensive command-line validator with advanced features:
- Cell → Surface validation
- Cell → Material validation (with void cell type detection)
- Universe hierarchy validation
- Circular universe reference detection
- Duplicate ID detection
- Formatted validation reports

### Usage

**Basic validation:**
```bash
python cross_reference_validator.py <mcnp_input_file>
```

**Example:**
```bash
python cross_reference_validator.py reactor_model.i
```

### Output

The script generates two outputs:

1. **Console output**: Validation report printed to screen
2. **Report file**: `<input_filename>_validation_report.txt` saved to disk

### Exit Codes

- **0**: Validation passed (no fatal errors)
- **1**: Validation failed (fatal errors detected)

### What It Validates

| Check Type | Description | Severity |
|------------|-------------|----------|
| Cell → Surface | All surfaces in cell geometry exist | FATAL |
| Cell → Material | All materials referenced exist (excludes void) | FATAL |
| Universe Fill | All filled universes are declared | FATAL |
| Circular Universe | No cyclic dependencies in fill chains | FATAL |
| Duplicate IDs | No duplicate cell/surface/material IDs | FATAL |

### Example Output - Passing

```
======================================================================
MCNP CROSS-REFERENCE VALIDATION REPORT
File: simple_pwr_pin.i
======================================================================

SECTION 1: FATAL ERRORS
----------------------------------------------------------------------
✓ No fatal errors detected

SECTION 2: WARNINGS
----------------------------------------------------------------------
✓ No warnings

SECTION 3: STATISTICS
----------------------------------------------------------------------
Total cells:     5
Total surfaces:  6
Total materials: 3
Total universes: 1

SECTION 4: SUMMARY
----------------------------------------------------------------------
✅ VALIDATION PASSED
   No fatal cross-reference errors detected

======================================================================
```

### Example Output - Failing

```
======================================================================
MCNP CROSS-REFERENCE VALIDATION REPORT
File: test_input.i
======================================================================

SECTION 1: FATAL ERRORS
----------------------------------------------------------------------
[1] Cell 60106 references undefined surface 1119
    Location: Line 456

[2] Cell 200 references undefined material 50
    Location: Line 67

[3] Circular universe reference: 100 → 200 → 100

SECTION 2: WARNINGS
----------------------------------------------------------------------
✓ No warnings

SECTION 3: STATISTICS
----------------------------------------------------------------------
Total cells:     150
Total surfaces:  75
Total materials: 25
Total universes: 10

SECTION 4: SUMMARY
----------------------------------------------------------------------
❌ VALIDATION FAILED: 4 fatal error(s)
   Input file will NOT run successfully in MCNP

======================================================================
```

### Integration with Workflows

**Pre-Run Validation Script:**
```bash
#!/bin/bash
# Validate input before submitting MCNP job

INPUT_FILE="reactor.i"

# Run validation
python cross_reference_validator.py $INPUT_FILE

# Check exit code
if [ $? -eq 0 ]; then
    echo "Validation passed - submitting MCNP job"
    mcnp6 i=$INPUT_FILE
else
    echo "Validation failed - fix errors before running"
    exit 1
fi
```

**Batch Validation:**
```bash
#!/bin/bash
# Validate all input files in directory

for file in *.i; do
    echo "Validating $file..."
    python cross_reference_validator.py "$file"
    echo ""
done
```

### Performance

- **Small models** (< 100 cells): < 1 second
- **Medium models** (100-1000 cells): 1-5 seconds
- **Large models** (1000+ cells, e.g., AGR-1): 5-15 seconds

Much faster than waiting for MCNP to fail!

### Void Cell Handling

The validator properly distinguishes three types of void cells (material 0):

**1. Lattice Container (valid void):**
```mcnp
100 0  -10  u=100 lat=1  fill=-2:2 -2:2 0:0
```

**2. Fill Target (valid void):**
```mcnp
200 0  -20  fill=100
```

**3. True Void (valid void):**
```mcnp
999 0  9999  $ Particle termination
```

Only non-zero material IDs are validated against the materials block.

---

## Script 1: mcnp_cross_reference_checker.py

### Description
Core Python class for parsing MCNP inputs and validating cross-references.

### Usage as Library

**Import and initialize:**
```python
from mcnp_cross_reference_checker import MCNPCrossReferenceChecker

checker = MCNPCrossReferenceChecker()
```

**Build dependency graph:**
```python
graph = checker.build_dependency_graph('input.inp')

# Graph structure:
# {
#     'cells_to_surfaces': {1: [1,2,3], 2: [1,5,6]},
#     'cells_to_materials': {1: 1, 2: 2},
#     'surfaces_used_by': {1: [1,2], 2: [1]},
#     'materials_used_by': {1: [1], 2: [2]},
#     'unused_surfaces': [99],
#     'unused_materials': [4],
#     'defined_cells': [1, 2, 10],
#     'defined_surfaces': [1, 2, 3, 99],
#     'defined_materials': [1, 2, 4]
# }
```

**Find broken references:**
```python
broken = checker.find_broken_references('input.inp')

# Returns list of error dictionaries:
# [
#     {
#         'type': 'undefined_surface',
#         'cell': 10,
#         'missing_surface': 203,
#         'error': 'Cell 10 references undefined surface 203'
#     }
# ]
```

**Generate full report:**
```python
report = checker.generate_full_report('input.inp')

# Report structure:
# {
#     'fatal_errors': [...],     # Broken references
#     'warnings': {              # Unused entities
#         'unused_surfaces': [],
#         'unused_materials': []
#     },
#     'statistics': {            # Counts
#         'total_cells': 10,
#         'total_surfaces': 25,
#         'total_materials': 3,
#         'cell_surface_refs': 50,
#         'cell_material_refs': 8
#     }
# }
```

### Usage as Command-Line Tool

**Basic validation:**
```bash
python mcnp_cross_reference_checker.py input.inp
```

**Output:**
```
============================================================
CROSS-REFERENCE VALIDATION REPORT
============================================================

❌ FATAL ERRORS:
  1. Cell 10 references undefined surface 203
  2. Cell 15 references undefined material 5

⚠ WARNINGS:
  Unused surfaces: [99]
  Unused materials: [4]

📊 STATISTICS:
  total_cells: 15
  total_surfaces: 32
  total_materials: 4
  cell_surface_refs: 75
  cell_material_refs: 12
============================================================
```

### API Reference

#### Class: MCNPCrossReferenceChecker

**Methods:**

**`parse_input_file(filename: str) -> Tuple`**
- Parses MCNP input into three blocks
- Returns: (cell_lines, surface_lines, data_lines)
- Raises: ValueError if < 2 blank lines found

**`extract_surfaces_from_cells(cell_lines: List[str]) -> Dict`**
- Extracts surface references from cell geometries
- Returns: {cell_num: [surf_nums]}
- Handles operators: -, +, :, #, ()

**`extract_materials_from_cells(cell_lines: List[str]) -> Dict`**
- Extracts material references from cells
- Returns: {cell_num: mat_num}
- Ignores void cells (m=0)

**`build_dependency_graph(filename: str) -> Dict`**
- Builds complete dependency graph
- Returns: Comprehensive graph dictionary
- Includes forward and reverse mappings

**`find_broken_references(filename: str) -> List[Dict]`**
- Finds all undefined references
- Returns: List of error dictionaries
- Types: undefined_surface, undefined_material

**`detect_unused_entities(graph: Dict) -> Dict`**
- Identifies unused surfaces and materials
- Returns: {'unused_surfaces': [], 'unused_materials': []}

**`generate_full_report(filename: str) -> Dict`**
- Complete validation report
- Returns: fatal_errors, warnings, statistics

---

## Example Workflows

### Workflow 1: Pre-Run Validation

```python
from mcnp_cross_reference_checker import MCNPCrossReferenceChecker

def validate_before_run(input_file):
    """Quick validation before MCNP run"""
    checker = MCNPCrossReferenceChecker()
    broken = checker.find_broken_references(input_file)

    if broken:
        print("❌ FATAL: Cannot run MCNP - fix these errors first:")
        for err in broken:
            print(f"  - {err['error']}")
        return False
    else:
        print("✓ Cross-references validated")
        return True

# Usage
if validate_before_run('reactor.inp'):
    # Proceed to run MCNP
    pass
```

### Workflow 2: Impact Analysis

```python
def analyze_deletion_impact(filename, entity_type, entity_num):
    """Check what breaks if entity is deleted"""
    checker = MCNPCrossReferenceChecker()
    graph = checker.build_dependency_graph(filename)

    if entity_type == 'surface':
        if entity_num in graph['surfaces_used_by']:
            cells = graph['surfaces_used_by'][entity_num]
            print(f"⚠ Cannot delete surface {entity_num}")
            print(f"  Used by cells: {cells}")
            return False
        else:
            print(f"✓ Surface {entity_num} can be safely deleted (unused)")
            return True

    elif entity_type == 'material':
        if entity_num in graph['materials_used_by']:
            cells = graph['materials_used_by'][entity_num]
            print(f"⚠ Cannot delete material {entity_num}")
            print(f"  Used by cells: {cells}")
            return False
        else:
            print(f"✓ Material {entity_num} can be safely deleted (unused)")
            return True

# Usage
analyze_deletion_impact('input.inp', 'surface', 99)
```

### Workflow 3: Cleanup Unused Entities

```python
def report_cleanup_candidates(filename):
    """Identify entities that can be removed"""
    checker = MCNPCrossReferenceChecker()
    graph = checker.build_dependency_graph(filename)

    print("CLEANUP CANDIDATES:")
    print("=" * 50)

    if graph['unused_surfaces']:
        print("\nUnused Surfaces (safe to remove):")
        for surf in graph['unused_surfaces']:
            print(f"  - Surface {surf}")

    if graph['unused_materials']:
        print("\nUnused Materials (safe to remove):")
        for mat in graph['unused_materials']:
            print(f"  - Material {mat}")

    if not graph['unused_surfaces'] and not graph['unused_materials']:
        print("No unused entities found (input is clean)")

# Usage
report_cleanup_candidates('input.inp')
```

---

## Integration with Other Skills

**Validation Pipeline:**
```python
# Step 1: Syntax validation
from mcnp_input_validator import validate_syntax
syntax_ok = validate_syntax('input.inp')

# Step 2: Cross-reference validation (THIS SCRIPT)
from mcnp_cross_reference_checker import MCNPCrossReferenceChecker
checker = MCNPCrossReferenceChecker()
broken = checker.find_broken_references('input.inp')

if broken:
    print("Fix cross-references before continuing")
    sys.exit(1)

# Step 3: Geometry validation
from mcnp_geometry_checker import check_geometry
geom_ok = check_geometry('input.inp')

# Step 4: Ready to run MCNP
```

---

## Troubleshooting

**Problem:** "Input file must have at least 2 blank lines"
- **Cause:** Invalid three-block structure
- **Fix:** Ensure blank lines separate cells/surfaces/data blocks

**Problem:** Script doesn't detect known broken reference
- **Cause:** Complex geometry expression parsing
- **Fix:** Simplify geometry, report issue for script improvement

**Problem:** False positives for unused entities
- **Cause:** Dynamic references (FILL arrays, etc.)
- **Fix:** Manual review, these may be legitimate

---

## Future Enhancements

Planned features for future versions:
1. Universe/Fill dependency tracking
2. Transformation reference validation
3. Tally cell/surface reference checking
4. FM card material validation
5. IMP card count verification
6. Circular dependency detection
7. Graphviz DOT export
8. HTML report generation

---

## Contributing

To extend these scripts:
1. Maintain compatibility with Python 3.8+
2. Use type hints for all functions
3. Follow existing code style
4. Add docstrings to new methods
5. Update this README with new features

---

**END OF README**
