# MCNP Cross-Reference Checker - Scripts Documentation

**Version:** 2.0.0
**Skill:** mcnp-cross-reference-checker

---

## Overview

This directory contains Python scripts for automated cross-reference validation and dependency analysis of MCNP input files.

**Available Scripts:**
1. **mcnp_cross_reference_checker.py** - Core validation library
2. **dependency_visualizer.py** - Dependency graph visualization (planned)
3. **cross_reference_validator.py** - CLI validation tool (planned)
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
