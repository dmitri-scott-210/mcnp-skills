---
name: "MCNP Cross Reference Checker"
description: "Validates cross-references in MCNP inputs: cells→surfaces, cells→materials, tallies→cells, transformations, and universe dependencies. Use for dependency analysis."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Cross Reference Checker

## Overview

MCNP input files contain numerous cross-references where one card references entities defined on other cards. Broken references cause FATAL errors. This skill validates all reference relationships:

- Cells → Surfaces (geometry expressions)
- Cells → Materials (M card numbers)
- Cells → Transformations (TRCL references)
- Cells → Universes (U and FILL parameters)
- Tallies → Cells/Surfaces
- FM cards → Materials
- Importance cards → Cell count matching
- Data cards → Entity count matching

Use this when users have reference errors, are modifying inputs, or need dependency mapping for complex geometries.

## Workflow Decision Tree

### When to Invoke
- User gets "undefined surface/material/cell" errors
- After adding/deleting cells, surfaces, or materials
- Before major input modifications
- For complex geometries (lattices, repeated structures)
- User wants dependency visualization

### Checking Approach

**Quick Reference Check:**
- Verify all surfaces referenced in cells exist
- Check all materials are defined
- Validate importance card counts
→ Fast check for common errors

**Comprehensive Cross-Reference Analysis** (recommended):
- All quick checks
- Build complete dependency graph
- Find unused entities
- Check transformation references
- Validate universe/fill relationships
→ Full dependency analysis

**Dependency Mapping:**
- Create visual dependency graph
- Show which cells use which surfaces/materials
- Identify orphaned entities
- Map universe hierarchy
→ For understanding complex inputs

## Tool Invocation

This skill includes a Python implementation for automated cross-reference validation and dependency analysis.

### Importing the Tool

```python
from mcnp_cross_reference import MCNPCrossReferenceChecker

# Initialize the checker
checker = MCNPCrossReferenceChecker()
```

### Basic Usage

**Build Complete Dependency Graph**:
```python
# Analyze all cross-references
graph = checker.build_dependency_graph('path/to/input.inp')

# Structure:
# {
#     'cells_to_surfaces': {cell_num: [surf_nums]},
#     'cells_to_materials': {cell_num: mat_num},
#     'tallies_to_cells': {tally_num: [cell_nums]},
#     'unused_surfaces': [surf_nums],
#     'unused_materials': [mat_nums]
# }

# Display cell-to-surface dependencies
print("Cell → Surface Dependencies:")
for cell, surfs in graph['cells_to_surfaces'].items():
    print(f"  Cell {cell}: surfaces {surfs}")

# Show unused entities
if graph['unused_surfaces']:
    print(f"\n⚠ Unused surfaces: {graph['unused_surfaces']}")
if graph['unused_materials']:
    print(f"⚠ Unused materials: {graph['unused_materials']}")
```

**Find Broken References**:
```python
# Detect all broken cross-references
broken = checker.find_broken_references('input.inp')

if broken:
    print("❌ BROKEN REFERENCES FOUND:")
    for item in broken:
        cell = item['cell']
        missing = item['missing_surface']
        print(f"  Cell {cell} references undefined surface {missing}")
else:
    print("✓ All cross-references valid")
```

**Check Specific Dependencies**:
```python
# Build dependency graph
graph = checker.build_dependency_graph('reactor.inp')

# Check which cells use a specific surface
target_surface = 105
cells_using_surf = [
    cell for cell, surfs in graph['cells_to_surfaces'].items()
    if target_surface in surfs
]
print(f"Cells using surface {target_surface}: {cells_using_surf}")

# Check which cells use a specific material
target_material = 3
cells_using_mat = [
    cell for cell, mat in graph['cells_to_materials'].items()
    if mat == target_material
]
print(f"Cells using material {target_material}: {cells_using_mat}")
```

### Integration with MCNP Workflow

```python
from mcnp_cross_reference import MCNPCrossReferenceChecker

def validate_cross_references(input_file):
    """Complete cross-reference validation workflow"""
    print(f"Validating cross-references: {input_file}")
    print("=" * 60)

    checker = MCNPCrossReferenceChecker()

    # Build dependency graph
    graph = checker.build_dependency_graph(input_file)

    # Find broken references
    broken = checker.find_broken_references(input_file)

    # Report broken references (FATAL)
    if broken:
        print("\n❌ FATAL ERRORS - Broken References:")
        for i, item in enumerate(broken, 1):
            cell = item['cell']
            missing = item['missing_surface']
            print(f"  {i}. Cell {cell} references undefined surface {missing}")
            print(f"     Fix: Add surface {missing} definition or correct cell {cell} geometry")

    # Report unused entities (WARNINGS)
    warnings = False
    if graph['unused_surfaces']:
        warnings = True
        print("\n⚠ WARNINGS - Unused Surfaces:")
        for surf in graph['unused_surfaces']:
            print(f"  • Surface {surf} defined but never used")
        print("  Action: Remove if not needed, or verify should be used")

    if graph['unused_materials']:
        warnings = True
        print("\n⚠ WARNINGS - Unused Materials:")
        for mat in graph['unused_materials']:
            print(f"  • Material {mat} defined but never used in any cell")
        print("  Action: Remove if not needed")

    # Display dependency summary
    print("\n📊 DEPENDENCY SUMMARY:")
    print(f"  Cells: {len(graph['cells_to_surfaces'])}")
    print(f"  Cell → Surface dependencies: {sum(len(s) for s in graph['cells_to_surfaces'].values())} total references")
    print(f"  Cell → Material dependencies: {len(graph['cells_to_materials'])}")

    # Show some examples
    if graph['cells_to_surfaces']:
        print("\n  Example dependencies:")
        for cell, surfs in list(graph['cells_to_surfaces'].items())[:3]:
            print(f"    Cell {cell} → surfaces {surfs}")

    print("\n" + "=" * 60)

    # Return validation status
    if broken:
        print("✗ VALIDATION FAILED - Fix broken references before running")
        return False
    elif warnings:
        print("⚠ VALIDATION PASSED with warnings - Review unused entities")
        return True
    else:
        print("✓ VALIDATION PASSED - All cross-references valid")
        return True

# Example usage
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.inp"
    validate_cross_references(input_file)
```

---

## Cross-Reference Validation Procedure

### Step 1: Understand User Need
Ask clarifying questions:
- "What error message are you seeing?"
- "Did you recently add/delete cells, surfaces, or materials?"
- "Do you need full dependency analysis or just error checking?"
- "Is this a lattice or repeated structure problem?"

### Step 2: Read Reference Materials
**MANDATORY - READ ENTIRE FILE**: Read `.claude/commands/mcnp-cross-reference-checker.md` for:
- Complete cross-reference checking procedures
- All reference relationship types
- Dependency graph building
- Common reference errors and fixes

### Step 3: Build Dependency Graph

Use the Python checker (see **Tool Invocation** section above for detailed usage):

```python
from mcnp_cross_reference import MCNPCrossReferenceChecker

checker = MCNPCrossReferenceChecker()

# Build complete dependency graph
graph = checker.build_dependency_graph('input.inp')

# Structure:
# {
#     'cells_to_surfaces': {cell_num: [surf_nums]},
#     'cells_to_materials': {cell_num: mat_num},
#     'tallies_to_cells': {tally_num: [cell_nums]},
#     'unused_surfaces': [surf_nums],
#     'unused_materials': [mat_nums]
# }

# Find broken references
broken = checker.find_broken_references('input.inp')
# Returns list of {cell: X, missing_surface: Y} dicts
```

### Step 4: Report Reference Issues

Organize by type and severity:
1. **FATAL** - Broken references (undefined entities)
2. **WARNINGS** - Unused entities (defined but not referenced)
3. **INFO** - Dependency structure information

### Step 5: Guide User to Fix

For each broken reference:
- Show source of reference
- Identify missing target
- Suggest fix (add definition or correct reference)
- Verify fix resolves issue

## Reference Relationship Types

### Cell → Surface References (Chapter 5.2)

**How cells reference surfaces:**
```
10 1 -2.7  -1 2 -3 (4:5) #6

References:
- Surface 1 (negative sense)
- Surface 2 (positive sense)
- Surface 3 (negative sense)
- Surface 4 (positive sense in union)
- Surface 5 (positive sense in union)
- Cell 6 (complement operator)
```

**Validation:**
```python
# Extract all surface numbers from geometry expression
# including unions (:), intersections (space), complements (#)
surfaces = geom_evaluator.get_all_surfaces(cell.geometry)

# Verify each exists
for surf in surfaces:
    if surf not in defined_surfaces:
        ERROR: f"Cell {cell.number} references undefined surface {surf}"
```

### Cell → Material References (Chapter 5.6)

**Cell card format:** `j m d geom params`
- j = cell number
- m = material number (0 = void)
- d = density

**Validation:**
```
Cell: 10 5 -2.7 ...
      ↓
Material: M5 ...

If M5 doesn't exist → FATAL ERROR
```

**Special cases:**
- m = 0: Void (no material needed)
- m > 0: Must have corresponding M card

### Tally → Cell/Surface References (Chapter 5.9)

**Tally types and references:**
```
F1:N 10 20 30      ← Surface current on surfaces 10, 20, 30
F2:P 5 10 15       ← Surface flux on surfaces 5, 10, 15
F4:N 2 4 6         ← Cell flux in cells 2, 4, 6
F5:P 0 0 0 0.1     ← Point detector (no cell/surface ref)
F6:N 8             ← Energy deposition in cell 8
```

**Validation:**
- F1, F2 → Verify surfaces exist
- F4, F6, F7, F8 → Verify cells exist
- F5 → No validation needed (point coordinates)

### Importance Card → Cell Count (Chapter 3.2.5.2)

**CRITICAL RULE:** Number of entries must equal number of cells

```
c 5 cells defined
1 1 -2.7 -1
2 1 -2.7  1 -2
3 0      2 -3
4 2 -8.0  3 -4
5 0      4

c Must have exactly 5 entries
IMP:N 1 1 1 1 0    ← CORRECT

IMP:N 1 1 1        ← WRONG: Only 3 entries for 5 cells
IMP:N 1 1 1 1 0 0  ← WRONG: 6 entries for 5 cells
```

**Error consequences:**
- Too few → WARNING (assumes 0 for missing)
- Too many → FATAL ERROR

### Transformation References (Chapter 5.5)

**Cell transformations (TRCL):**
```
10 1 -2.7 -1 TRCL=5    ← References TR5

c Must have TR5 defined:
TR5 1 2 3  0 0 0 ...
```

**Surface transformations:**
```
105 10 PX 5    ← Surface 105 uses TR10

c Must have TR10 defined:
TR10 0 0 0 ...
```

**Limitations:**
- Cell transform numbers: ≤ 99,999,999
- Surface transform numbers: ≤ 999
- Total transformations: ≤ 999

### Universe and Fill References (Chapter 5.5)

**Universe system:**
```
c Define universe 5
10 1 -2.7 -1 U=5

c Fill cell with universe 5
20 0 -10 11 -12 13 FILL=5

Validation: Universe 5 must exist before FILL=5
```

**Lattice fills:**
```
FILL=5:10 1 2 3 ...

Must define universes 5, 6, 7, 8, 9, 10
```

**Common errors:**
- FILL references undefined universe
- Circular references (universe fills itself)
- Lattice element count mismatch

### FM Tally Multiplier → Material (Chapter 5.9)

**Format:**
```
FM4 c m1 r1 m2 r2 ...

where:
- c = normalization constant
- m = material number (-1 for cell material)
- r = reaction number (MT)
```

**Validation:**
```
FM4 1.0 5 -6    ← References material 5

Material 5 must be defined (M5 card)
If m=-1, uses material from tally cell (no validation needed)
```

## Common Cross-Reference Errors

### Error 1: Undefined Surface

```
10 1 -2.7 -1 2 -105    ← References surface 105

c But surface 105 not defined!

Fix options:
1. Add surface 105 definition
2. Correct cell geometry (wrong number typo)
3. Remove reference if not needed
```

### Error 2: Undefined Material

```
15 3 -8.0 -20 21 -22   ← Uses material 3

c But no M3 card!

Fix options:
1. Add M3 material specification
2. Change to correct material number
3. Change to void: 15 0 -20 21 -22
```

### Error 3: Importance Count Mismatch

```
c 15 cells defined, but:
IMP:N 1 1 1 0    ← Only 4 entries!

Fix: Add 11 more entries (total 15)
IMP:N 1 1 1 0 1 1 1 1 1 1 1 1 1 1 0
```

### Error 4: Tally References Deleted Cell

```
F4:N 10 15 20    ← References cells 10, 15, 20

c Cell 15 was deleted but tally not updated!

Fix: Remove 15 from tally
F4:N 10 20
```

### Error 5: Transformation Not Defined

```
50 2 -7.8 -100 TRCL=8    ← References TR8

c But no TR8 card!

Fix: Add transformation
TR8 1.0 2.0 3.0  0 0 0 ...
```

## Unused Entity Detection

### Unused Surfaces

**Problem:** Surface defined but never used
```
10 PX 5    ← Defined

c But no cell references surface 10!

Possible causes:
1. Forgot to use in cell geometry
2. Leftover from deleted cells
3. Typo in cell geometry (referenced wrong number)
```

**Recommendation:**
- Review if surface should be used
- Remove if truly not needed
- May indicate incomplete geometry

### Unused Materials

**Problem:** Material defined but never used
```
M5 6000.80c 1    ← Defined

c But no cell has material 5!

Possible causes:
1. Copied from another input
2. Material changed in cells
3. Planning to use but forgot
```

**Recommendation:**
- Verify not needed
- Remove to reduce clutter
- May indicate copy-paste error

## Dependency Graph Visualization

### Simple Text Format

```
DEPENDENCY ANALYSIS:

Cells → Surfaces:
  Cell 1: surfaces [1, 2, 3]
  Cell 2: surfaces [1, 4, 5]
  Cell 3: surfaces [2, 4, 6]

Cells → Materials:
  Cell 1: material 1
  Cell 2: material 1
  Cell 3: material 2

Tallies → Cells:
  F4: cells [1, 2, 3]
  F14: cells [5, 10, 15]

Unused:
  Surfaces: [99]
  Materials: [4]

Undefined References:
  Cell 10 → surface 203 (MISSING!)
  Cell 15 → material 5 (MISSING!)
```

### Hierarchical Universe Structure

```
Universe 0 (base):
  ├─ Cell 1 (material 1)
  ├─ Cell 2 (material 1)
  └─ Cell 10 (FILL=5)
      │
      Universe 5:
        ├─ Cell 20 (material 2)
        ├─ Cell 21 (material 3)
        └─ Cell 22 (FILL=10)
            │
            Universe 10:
              └─ Cell 30 (material 4)
```

## Integration with Other Skills

**Workflow:**
1. mcnp-input-validator (basic syntax)
2. mcnp-cross-reference-checker (dependencies) ← YOU ARE HERE
3. Fix any broken references
4. mcnp-geometry-checker (detailed geometry)

**Related skills:**
- mcnp-input-validator: Overall validation
- mcnp-geometry-builder: Create correct references from start
- mcnp-card-modifier: Help fix references when modifying

## Example Cross-Reference Check Workflow

```
User: "MCNP says 'cell 10 references undefined surface 203', can you help?"

Claude: I'll analyze all cross-references in your input file to find and fix broken dependencies.

[Reads .claude/commands/mcnp-cross-reference-checker.md]
[Uses MCNPCrossReferenceChecker]

**Cross-Reference Analysis:**

FATAL ERRORS (broken references):
❌ 1. Cell 10 references undefined surface 203
   Location: Cell geometry "-1 2 -203 4"
   Problem: Surface 203 not found in surface cards
   
   Possible fixes:
   A. Add surface 203 definition:
      203 PZ 10.5    ← (or appropriate surface type)
   
   B. Correct cell 10 geometry (if 203 is a typo):
      Check if you meant surface 103, 201, or 230?
   
   Reference: Chapter 5.3 (Surface Cards)

❌ 2. FM4 multiplier references undefined material 3
   Location: FM4 card "FM4 1.0 3 -6"
   Problem: No M3 card found
   
   Fix: Add material 3 definition or change FM4 to use different material
   Reference: Chapter 5.9.10 (FM Card)

WARNINGS (unused entities):
⚠ Surface 99 defined but never used
   Defined: Line 45 "99 SO 100"
   Impact: Clutters input, may indicate incomplete geometry
   Action: Remove if not needed, or verify should be used somewhere

⚠ Material 4 defined but never used in any cell
   Defined: M4 card at line 120
   Impact: Wastes memory, may be leftover from previous version
   Action: Remove if not needed

DEPENDENCY GRAPH:
Cells → Surfaces (15 cells reference 32 surfaces):
  Cell 1: [1, 2, 3, 4]
  Cell 2: [1, 5, 6, 7]
  Cell 10: [1, 2, 203(MISSING!), 4]  ← Problem here
  ...

Cells → Materials (12 non-void cells use 3 materials):
  Cells 1,2,5,8: material 1
  Cells 3,4,6: material 2
  Cell 10: material 1

Tallies → Cells:
  F4: cells [1, 2, 3, 5, 8]
  F14: cells [10, 15, 20]

SUMMARY:
- 2 FATAL broken references must be fixed
- 2 unused entities (consider removing)
- 1 surface missing (203)
- 1 material missing (3, for FM4)

Would you like me to:
1. Help add surface 203 definition?
2. Fix FM4 material reference?
3. Generate cleaned input with unused entities removed?
4. Create visual dependency map?
```

## Important Principles

1. **First error is real; fix in order** - Subsequent errors may cascade
2. **Count mismatches are FATAL** - IMP cards must match cell count exactly
3. **Unused entities may indicate errors** - Don't automatically delete
4. **Universe dependencies are complex** - Trace carefully in lattices
5. **Validate after every modification** - Easy to break references

## Code Style

When checking cross-references:
- Report broken references before unused entities
- Show both source and target of reference
- Provide specific line numbers when available
- Suggest multiple fix options
- Group related issues

## Dependencies

Required components:
- Python module: `skills/validation/mcnp_cross_reference.py`
- Input parser: `parsers/input_parser.py`
- Geometry evaluator: `utils/geometry_evaluator.py`
- Reference: `.claude/commands/mcnp-cross-reference-checker.md`

## References

**Primary References:**
- `.claude/commands/mcnp-cross-reference-checker.md` - Detailed procedures
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Quick reference for all cards
- Chapter 3.2.5.2: Cell and surface parameter cards
- Chapter 4: Input structure and limitations
- §5.2: Cell cards (surface and material references)
- §5.5: Geometry data cards (universe, fill, transformations)
- §5.6: Material specification (M card numbering)
- §5.9: Tally specification (cell/surface references)
- Table 4.1 & 4.2: Limitations on card numbers and counts

**Key Topics:**
- Cross-reference validation
- Dependency graph building
- Unused entity detection
- Universe/fill relationships
- Transformation references

**Related Skills:**
- mcnp-input-validator
- mcnp-geometry-checker
- mcnp-geometry-builder
- mcnp-card-modifier
