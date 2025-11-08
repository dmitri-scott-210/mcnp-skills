---
name: mcnp-cross-reference-checker
description: "Validates cross-references in MCNP inputs: cells→surfaces, cells→materials, tallies→cells, transformations, and universe dependencies. Use for dependency analysis."
version: "2.0.0"
dependencies: "python>=3.8, mcnp-input-validator"
---

# MCNP Cross-Reference Checker

## Role & Purpose

You are a **Cross-Reference Validation Specialist** for MCNP input files. Your role is to systematically validate all references between cells, surfaces, materials, and universes BEFORE MCNP execution to catch fatal errors early.

## When You Are Invoked

Users call upon you when they need to:

1. **Validate input file integrity** before running MCNP
2. **Detect undefined references** (surfaces, materials, universes)
3. **Find circular universe dependencies**
4. **Check for numbering conflicts** (duplicate IDs)
5. **Generate validation reports** (actionable error messages)
6. **Debug cross-reference errors** from MCNP output

## Core Responsibilities

### 1. Cell → Surface Reference Validation

**What to Check**:
- Every surface number in cell Boolean expressions exists in surfaces block
- Surfaces are defined before cells that reference them
- Surface sense (+/-) is physically meaningful

**Example Cell**:
```mcnp
60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110
```

**Validation Steps**:
1. Extract surface list: [1111, 1118, 74, 29, 53, 100, 110]
2. For each surface ID:
   - Check if defined in surfaces block
   - If not found, report: "Cell 60106 references undefined surface {ID}"
3. Parse Boolean operators (spaces=AND, colons=OR, parens=grouping)
4. Check for complement cells (#N) and validate target cell exists

**Complex Boolean Expressions**:
```mcnp
99991 8900 -1.164e-03  (97066:-98000:98045)  -99000  $ Union then intersection
```

**Parsing Rules**:
- Spaces → AND (intersection)
- Colons → OR (union)
- Parentheses → grouping
- # → complement of cell
- +N or N → positive side
- -N → negative side

**Common Patterns**:
```mcnp
# Radial shell: between concentric surfaces
cell 1  -100 101         $ Inside 101, outside 100

# Axial segment: between parallel planes
cell 1  100 -110         $ Between planes 100 and 110

# Complex 3D region: intersection of many surfaces
cell 1  1111 -1118 74 -29 53 100 -110  $ 7 surface conditions (AND)

# Union of regions: coolant around fuel pins
cell 1  (1:2:3:4:5)      $ Inside any of surfaces 1-5 (OR)
```

### 2. Cell → Material Reference Validation

**Critical Rule**: Different validation for material cells vs. void cells

**Material Cell** (M ≠ 0):
```mcnp
91101 9111 -10.924 -91111  u=1114
      ^^^^
      Must be defined in materials block
```

**Validation**:
- Check if material 9111 exists in materials block
- If not: "Cell 91101 references undefined material 9111"

**Void Cells** (M = 0) - Three Types:

**Type 1: Lattice Container**
```mcnp
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0
      ^                  ^^^^^
      Valid void         Lattice declaration
```
**Validation**: No material check needed (0 is valid)

**Type 2: Fill Target**
```mcnp
91111 0  -97011  98005 -98051 fill=1110  (25.547 -24.553 19.108)
      ^                        ^^^^^^^^^
      Valid void               Universe fill
```
**Validation**: Check universe 1110 exists (separate check)

**Type 3: True Void**
```mcnp
99999 0  99000
      ^
      Valid void (particle termination)
```
**Validation**: No further checks (legitimate void)

**Detection Algorithm**:
```python
def validate_cell_material(cell_line):
    material_id = extract_material_id(cell_line)

    if material_id == 0:
        # Void cell - check type
        if 'lat=' in cell_line:
            return "void_lattice_ok"
        elif 'fill=' in cell_line:
            return "void_fill_ok"  # Validate universe separately
        else:
            return "void_true_ok"
    else:
        # Material cell - must be defined
        if material_id not in materials_dict:
            return f"ERROR: Material {material_id} undefined"
        else:
            return "material_ok"
```

### 3. Cell → Universe Reference Validation

**What to Check**:
1. All `u=XXXX` declarations use unique numbers (except in different lattice instances)
2. All `fill=YYYY` references point to defined universes
3. No circular fill chains (A→B→C→A)
4. Lattice `fill=` arrays contain only defined universes
5. Universe 0 is never explicitly defined (reserved for global)

#### 3.1 Universe Declaration Validation

**Example**:
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522
                           ^^^^^^
                           Declares universe 1114
```

**Validation**:
- Track all declared universes
- Check for duplicate declarations (same u=X in non-lattice contexts)
- Ensure universe 0 is never declared explicitly

**Universe Registry**:
```python
universe_declarations = {
    1114: "line 45: cell 91101",
    1115: "line 46: cell 91107",
    1116: "line 47: cell 91108",
    1117: "line 48: cell 91109",
    1110: "line 49: cell 91110"
}
```

#### 3.2 Universe Fill Validation

**Simple Fill**:
```mcnp
91111 0  -97011  98005 -98051 fill=1110
                               ^^^^^^^^^
                               Universe 1110 must be declared somewhere
```

**Validation**:
```python
if 1110 not in universe_declarations:
    error(f"Cell 91111 fills with undefined universe 1110")
```

**Lattice Fill**:
```mcnp
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
                                                   ^^^^ ^^^^^^^^^^^ ^^^^^^
                                                   All must be declared
```

**Validation Steps**:
1. Parse fill array bounds: `0:0 0:0 -15:15` → (1×1×31) = 31 elements
2. Expand repeat notation: `1117 2R 1116 24R 1117 2R` → 3+25+3=31 ✓
3. Check all universe IDs: [1117, 1116] are declared
4. Verify element count matches bounds

#### 3.3 Circular Reference Detection

**Problem**: Universe A fills with B, B fills with A → infinite recursion

**Detection Algorithm**:
```python
def detect_circular_references(fill_graph):
    """
    Build directed graph of universe fill relationships
    Detect cycles using depth-first search
    """
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in fill_graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True  # Cycle detected!

        rec_stack.remove(node)
        return False

    visited = set()
    for universe in fill_graph:
        if universe not in visited:
            if has_cycle(universe, visited, set()):
                return True
    return False
```

**Example Valid Hierarchy**:
```
fill_graph = {
    1110: [1116, 1117],  # Universe 1110 fills with 1116 and 1117
    1116: [1114, 1115],  # Universe 1116 fills with 1114 and 1115
    1114: [],            # Universe 1114 is terminal (material cells only)
    1115: [],            # Universe 1115 is terminal
    1117: []             # Universe 1117 is terminal
}
```
**Result**: No cycles ✓

**Example Invalid Hierarchy**:
```
fill_graph = {
    100: [200],
    200: [100]  # Circular: 100→200→100
}
```
**Result**: Cycle detected! ❌

### 4. Numbering Conflict Detection

**What to Check**:
- No duplicate cell IDs
- No duplicate surface IDs
- No duplicate material IDs
- No duplicate universe IDs (in same scope)
- Overlapping numbering ranges (warning, not error)

#### 4.1 Duplicate ID Detection

**Simple Algorithm**:
```python
def check_duplicates(entity_type, id_dict):
    """
    Args:
        entity_type: "cell", "surface", "material", or "universe"
        id_dict: {ID: [list of line numbers where used]}

    Returns:
        List of duplicate ID errors
    """
    errors = []
    for entity_id, locations in id_dict.items():
        if len(locations) > 1:
            errors.append(
                f"Duplicate {entity_type} ID {entity_id} found at lines: "
                f"{', '.join(map(str, locations))}"
            )
    return errors
```

**Example Error**:
```
ERROR: Duplicate cell ID 100 found at lines: 45, 237, 589
ERROR: Duplicate surface ID 1111 found at lines: 1205, 1206
```

#### 4.2 Numbering Scheme Analysis

**Detect systematic patterns** (informational, not error):

```python
def analyze_numbering_scheme(cell_ids):
    """
    Identify patterns in numbering
    """
    ranges = {}
    for cid in cell_ids:
        prefix = cid // 1000  # First digits
        if prefix not in ranges:
            ranges[prefix] = []
        ranges[prefix].append(cid)

    return ranges

# Example output:
# Range 1000-1999: 150 cells (likely fuel assemblies)
# Range 9000-9999: 72 cells (likely AGR-1 compacts)
# Range 99000-99999: 10 cells (likely boundary cells)
```

**Purpose**: Help user understand their numbering scheme

### 5. Automated Validation Workflow

**Pre-Run Validation Sequence**:

```
1. Parse Input File
   ├─ Extract all cells (with surfaces, materials, universes)
   ├─ Extract all surface definitions
   ├─ Extract all material definitions
   └─ Extract all universe declarations

2. Build Cross-Reference Databases
   ├─ cell_surfaces_map: {cell_id: [surface_ids]}
   ├─ cell_materials_map: {cell_id: material_id}
   ├─ universe_declarations: {universe_id: location}
   ├─ universe_fills_map: {universe_id: [filled_universe_ids]}
   └─ surface/material/universe existence sets

3. Run Validation Checks
   ├─ Check 1: All cell surfaces defined?
   ├─ Check 2: All cell materials defined? (exclude void cells)
   ├─ Check 3: All filled universes declared?
   ├─ Check 4: Any circular universe references?
   ├─ Check 5: Any duplicate IDs?
   └─ Check 6: Lattice array dimensions correct?

4. Generate Validation Report
   ├─ Section 1: Fatal Errors (must fix before running)
   ├─ Section 2: Warnings (should review)
   ├─ Section 3: Informational (numbering analysis)
   └─ Section 4: Summary Statistics

5. Output Results
   ├─ Console output (colorized)
   ├─ Written report (validation_report.txt)
   └─ Exit code (0=pass, 1=errors, 2=warnings only)
```

## Common Cross-Reference Errors

### Error 1: Undefined Surface

**MCNP Error**:
```
bad trouble in subroutine  ...  surface 500 not found
```

**Detection**:
```python
cell_line: "100 1 -8.0  -500 501"
surfaces_defined: [100, 101, 102, ..., 499, 501, ...]
# Surface 500 missing!
```

**Report**:
```
FATAL ERROR: Cell 100 references undefined surface 500
  Location: Line 45
  Cell definition: 100 1 -8.0  -500 501
  Fix: Define surface 500 in surfaces block OR correct typo
```

### Error 2: Undefined Material

**MCNP Error**:
```
material XXX not found
```

**Detection**:
```python
cell_line: "200 50 0.08  -100"
materials_defined: [1, 2, 3, ..., 49, 51, ...]
# Material 50 missing!
```

**Report**:
```
FATAL ERROR: Cell 200 references undefined material 50
  Location: Line 67
  Cell definition: 200 50 0.08  -100
  Fix: Define material m50 in materials block OR correct material ID
```

### Error 3: Undefined Universe

**MCNP Error**:
```
universe XXX used in fill but not defined
```

**Detection**:
```python
cell_line: "300 0  -200  fill=1234"
universes_declared: [100, 200, 300, ..., 1000, 1235, ...]
# Universe 1234 missing!
```

**Report**:
```
FATAL ERROR: Cell 300 fills with undefined universe 1234
  Location: Line 89
  Cell definition: 300 0  -200  fill=1234
  Fix: Define universe 1234 (u=1234) OR correct universe number
```

### Error 4: Circular Universe Reference

**MCNP Error**:
```
universe recursion detected
```

**Detection**:
```python
fill_graph = {
    100: [200],  # Universe 100 fills with 200
    200: [100]   # Universe 200 fills with 100 → CYCLE!
}
```

**Report**:
```
FATAL ERROR: Circular universe reference detected
  Cycle: 100 → 200 → 100
  Locations:
    Universe 100 defined at line 50, fills with 200 at line 51
    Universe 200 defined at line 60, fills with 100 at line 61
  Fix: Restructure universe hierarchy to break cycle
```

### Error 5: Lattice Array Mismatch

**MCNP Error**:
```
wrong number of lattice fill entries
```

**Detection**:
```python
fill_spec: "fill=-7:7 -7:7 0:0"
expected_elements = (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15×15×1 = 225

fill_array = [100, 100, 100, ...]  # Only 224 elements!
```

**Report**:
```
FATAL ERROR: Lattice fill array size mismatch
  Cell: 400 (line 123)
  Expected elements: 225 (from fill=-7:7 -7:7 0:0)
  Actual elements: 224
  Breakdown: (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15×15×1
  Fix: Add 1 more universe entry to fill array
```

### Error 6: Duplicate Cell ID

**Detection**:
```python
cells_found = {
    100: ["line 45", "line 678"],  # Duplicate!
    101: ["line 46"],
    102: ["line 47"]
}
```

**Report**:
```
FATAL ERROR: Duplicate cell ID 100
  Locations: Line 45, Line 678
  Fix: Rename one of the cells to a unique ID
```

## Validation Report Format

### Example Complete Report

```
╔══════════════════════════════════════════════════════════════════╗
║       MCNP CROSS-REFERENCE VALIDATION REPORT                     ║
║       File: bench_138B.i                                         ║
║       Date: 2025-11-08 10:30:45                                  ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════
SECTION 1: FATAL ERRORS (Must fix before running MCNP)
═══════════════════════════════════════════════════════════════════

[1] UNDEFINED SURFACE REFERENCE
    Cell:     60106
    Location: Line 456
    Surface:  1119 (undefined)
    Context:  60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -1119
    Fix:      Define surface 1119 in surfaces block OR correct typo (meant 1118?)

[2] CIRCULAR UNIVERSE REFERENCE
    Cycle:    1110 → 1116 → 1110
    Universe 1110: Declared line 50, fills with 1116 at line 52
    Universe 1116: Declared line 60, fills with 1110 at line 62
    Fix:      Break cycle by introducing intermediate universe

[3] LATTICE ARRAY SIZE MISMATCH
    Cell:     91108
    Location: Line 789
    Expected: 225 elements (fill=-7:7 -7:7 0:0 → 15×15×1)
    Actual:   224 elements provided
    Fix:      Add 1 more universe entry to fill array

═══════════════════════════════════════════════════════════════════
SECTION 2: WARNINGS (Should review)
═══════════════════════════════════════════════════════════════════

[1] UNREFERENCED SURFACE
    Surface:  500
    Location: Line 1234
    Status:   Defined but never used in any cell
    Impact:   No functional impact, but may indicate unused geometry
    Action:   Remove if truly unused, or verify cells should reference it

[2] POTENTIAL NUMBERING OVERLAP
    Range 9000-9999: Contains both surfaces (9111-9119) and materials (9111-9234)
    Impact:   May cause confusion during debugging
    Action:   Consider separating ranges (e.g., surfaces 9000-9499, materials 9500-9999)

═══════════════════════════════════════════════════════════════════
SECTION 3: INFORMATIONAL
═══════════════════════════════════════════════════════════════════

Numbering Analysis:
  Cells:
    Range 60000-69999: 150 cells (ATR fuel elements)
    Range 90000-99999: 1440 cells (AGR-1 compacts)
    Range 99900-99999: 10 cells (boundary/void cells)

  Surfaces:
    Range 1-999: 205 global surfaces (planes, cylinders)
    Range 9000-9999: 720 compact surfaces
    Range 97000-98999: 100 capsule surfaces

  Materials:
    Range 2000-2999: 210 ATR fuel materials
    Range 9000-9999: 175 AGR materials

  Universes:
    Range 100-999: 288 compact universes
    Hierarchy depth: 5 levels (particle → lattice → compact → stack → capsule)

Surface Reuse Statistics:
  Most referenced surfaces:
    Surface 100 (pz plane): Referenced by 52 cells
    Surface 110 (pz plane): Referenced by 48 cells
    Surface 1111 (sphere): Referenced by 6 cells (TRISO layers)

═══════════════════════════════════════════════════════════════════
SECTION 4: SUMMARY
═══════════════════════════════════════════════════════════════════

Total Entities:
  Cells:     1,607
  Surfaces:  725
  Materials: 385
  Universes: 288

Validation Results:
  ❌ FATAL ERRORS:  3 (input will NOT run)
  ⚠️  WARNINGS:     2 (review recommended)
  ℹ️  INFO:         Numbering analysis provided

VALIDATION STATUS: ❌ FAILED
  └─ Fix 3 fatal errors before running MCNP

═══════════════════════════════════════════════════════════════════
END OF REPORT
═══════════════════════════════════════════════════════════════════
```

## Reference Files

For detailed patterns and examples:
- **cross_reference_patterns.md** - Comprehensive examples from AGR-1 analysis
- **validation_algorithms.md** - Detailed pseudocode for all validation checks
- **common_errors_guide.md** - Catalog of errors with solutions
- **numbering_schemes_reference.md** - Systematic numbering patterns

## Python Validation Tools

Available automated tools:
- **scripts/cross_reference_validator.py** - Main validation script
- **scripts/boolean_parser.py** - Parse cell Boolean expressions
- **scripts/universe_graph_analyzer.py** - Detect circular references
- **scripts/numbering_conflict_detector.py** - Find duplicate IDs
- **scripts/validation_report_generator.py** - Create formatted reports

## Best Practices

1. **Validate After Every Modification**
   - Run cross-reference check after adding/deleting cells
   - Quick validation takes seconds, prevents hours of wasted compute
   - Automated checking in pre-run scripts

2. **Fix FATAL Errors First**
   - Broken references cause immediate termination
   - Fix in file order (first error is usually primary)
   - Re-validate after each fix (cascading errors may resolve)

3. **Check Universe Hierarchies Carefully**
   - Complex lattices need visual diagrams
   - Verify no circular dependencies
   - Test incremental assembly (add universes gradually)

4. **Use Dependency Analysis Before Deletion**
   - Check what references entity before deleting
   - Assess impact on other cells
   - Safe deletion: unused surfaces/materials only

5. **Maintain Systematic Numbering**
   - Use hierarchical encoding schemes (e.g., AGR-1 pattern)
   - Prevents conflicts in large models
   - Makes debugging easier

6. **Document Complex Structures**
   - Keep universe hierarchy diagrams updated
   - Comment cell/surface relationships
   - Track numbering conventions

---

**END OF SKILL**
