# Validation Procedures Reference

This document provides detailed algorithms and procedures for validating MCNP cell card features.

## Overview

Cell card validation involves five primary procedures:

1. **Universe Reference Validation** - Verify all fill= references have corresponding u= definitions
2. **Lattice Type Validation** - Check LAT parameter values are valid (1 or 2 only)
3. **Fill Array Dimension Validation** - Ensure array sizes match lattice declarations
4. **Universe Dependency Tree Construction** - Build hierarchy and detect circular references
5. **Lattice Boundary Surface Validation** - Check appropriate surfaces for lattice types

Each procedure includes detailed steps, pseudocode, and expected outputs.

---

## Procedure 1: Universe Reference Validation

### Goal

Ensure all `fill=` references have corresponding `u=` definitions.

### Algorithm

**Step 1: Parse all cell cards and extract universe information**

```python
# Initialize sets
defined_universes = set()
used_universes = set()

# Parse input file
cells = parse_input_file('input.inp')

for cell in cells:
    # Collect universe definitions
    if 'u' in cell.parameters:
        u_num = cell.parameters['u']

        # Check for duplicates
        if u_num in defined_universes:
            error(f"Duplicate universe definition: u={u_num} in cell {cell.number}")

        # Positive or negative, both define universe |u_num|
        defined_universes.add(abs(u_num))

    # Collect universe references
    if 'fill' in cell.parameters:
        fill_value = cell.parameters['fill']

        if isinstance(fill_value, int):
            # Simple fill: fill=5
            used_universes.add(fill_value)

        elif isinstance(fill_value, dict):
            # Array fill: fill= -3:3 -3:3 0:0  1 2 3 4 ...
            for u in fill_value['array_values']:
                if u != 0:  # 0 means void element (no fill)
                    used_universes.add(u)
```

**Step 2: Find undefined references**

```python
undefined = used_universes - defined_universes

if undefined:
    print("❌ FATAL: Undefined universe references")
    for u in sorted(undefined):
        print(f"  Universe {u} referenced in FILL but not defined with u={u}")

        # Find which cells use this undefined universe
        for cell in cells:
            if 'fill' in cell.parameters:
                fill_val = cell.parameters['fill']
                if isinstance(fill_val, int) and fill_val == u:
                    print(f"    Used in cell {cell.number}: fill={u}")
                elif isinstance(fill_val, dict):
                    if u in fill_val['array_values']:
                        print(f"    Used in cell {cell.number}: lattice fill array")
    return False
else:
    print(f"✓ All {len(used_universes)} universe references valid")
```

**Step 3: Check for unused definitions (warning only)**

```python
unused = defined_universes - used_universes

if unused:
    print(f"⚠ WARNING: {len(unused)} unused universe definitions: {sorted(unused)}")
    print("  These universes are defined but never used in FILL")

    # List cells defining unused universes
    for u in sorted(unused):
        for cell in cells:
            if 'u' in cell.parameters:
                if abs(cell.parameters['u']) == u:
                    print(f"    Cell {cell.number}: u={cell.parameters['u']}")
```

**Step 4: Check for universe 0 misuse**

```python
# Check definitions
for cell in cells:
    if 'u' in cell.parameters:
        if cell.parameters['u'] == 0:
            error(f"Cell {cell.number}: Universe 0 cannot be explicitly defined")
            print("  Universe 0 is the default 'real world'")

# Check references
for cell in cells:
    if 'fill' in cell.parameters:
        fill_val = cell.parameters['fill']

        if isinstance(fill_val, int) and fill_val == 0:
            error(f"Cell {cell.number}: Cannot fill with universe 0")
            print("  Universe 0 is the real world (cannot be filled into cells)")

        elif isinstance(fill_val, dict):
            if 0 in fill_val['array_values']:
                # Note: 0 in fill array is allowed (means void element)
                pass
```

### Expected Output

```
✓ Universe validation passed
  • 15 universes defined: [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
  • 15 universes referenced in FILL
  • 0 undefined references
  • 2 unused definitions: [300, 400] (warning)
    Cell 350: u=300
    Cell 450: u=400
```

---

## Procedure 2: Lattice Type Validation

### Goal

Verify LAT parameter values are valid (1 or 2 only) and lattice cells meet requirements.

### Algorithm

**Step 1: Find all lattice cells and validate LAT value**

```python
lattice_cells = []
errors = []

for cell in cells:
    if 'lat' in cell.parameters:
        lat_value = cell.parameters['lat']
        cell_errors = []

        # Check valid values (only 1 or 2 allowed)
        if lat_value not in [1, 2]:
            cell_errors.append(
                f"Invalid LAT={lat_value} (must be 1 for cubic or 2 for hexagonal)"
            )

        # Check FILL requirement
        if 'fill' not in cell.parameters:
            cell_errors.append(
                "LAT specified without FILL (lattice requires fill parameter)"
            )

        # Check material (should be void)
        if cell.material != 0:
            cell_errors.append(
                f"Lattice cell has material {cell.material} (must be void: material 0)"
            )

        if cell_errors:
            print(f"❌ Cell {cell.number} (LAT={lat_value}):")
            for err in cell_errors:
                print(f"  • {err}")
            errors.extend(cell_errors)
        else:
            print(f"✓ Cell {cell.number} (LAT={lat_value}): Valid")

        lattice_cells.append((cell, lat_value))
```

**Step 2: Validate surface count for each lattice type**

```python
for cell, lat_value in lattice_cells:
    surfaces = extract_surfaces_from_geometry(cell.geometry)
    surface_count = len(surfaces)

    if lat_value == 1:
        # Cubic lattice: recommend 6 bounding surfaces
        if surface_count < 6:
            print(f"⚠ Cell {cell.number} (LAT=1): Has {surface_count} surfaces")
            print(f"  Cubic lattice typically needs 6 surfaces for proper indexing")
            print(f"  Surfaces: {surfaces}")
        elif surface_count == 6:
            print(f"✓ Cell {cell.number} (LAT=1): Proper 6 surfaces")
        else:
            print(f"ℹ Cell {cell.number} (LAT=1): {surface_count} surfaces (unusual)")

    elif lat_value == 2:
        # Hexagonal lattice: recommend 8 surfaces (6 sides + 2 bases)
        if surface_count < 8:
            print(f"⚠ Cell {cell.number} (LAT=2): Has {surface_count} surfaces")
            print(f"  Hexagonal lattice typically needs 8 surfaces")
            print(f"  (6 for hexagon sides, 2 for top/bottom)")
        elif surface_count == 8:
            print(f"✓ Cell {cell.number} (LAT=2): Proper 8 surfaces")
        else:
            print(f"ℹ Cell {cell.number} (LAT=2): {surface_count} surfaces")
```

### Expected Output

```
✓ Lattice type validation passed
  • Cell 200 (LAT=1): Valid - 6 surfaces (cubic)
  • Cell 500 (LAT=2): Valid - 8 surfaces (hexagonal)
  • Cell 800 (LAT=1): Valid - 6 surfaces (cubic)

  Found 3 lattice cells, all specifications valid
```

---

## Procedure 3: Fill Array Dimension Validation

### Goal

Ensure fill array size matches lattice declaration exactly.

### Algorithm

**Step 1: Parse fill declarations and calculate expected sizes**

```python
for cell in lattice_cells:
    fill_params = cell.parameters['fill']

    if isinstance(fill_params, dict):  # Array fill
        # Extract ranges: fill= i1:i2 j1:j2 k1:k2
        i_range = fill_params['i_range']  # (i1, i2)
        j_range = fill_params['j_range']  # (j1, j2)
        k_range = fill_params['k_range']  # (k1, k2)

        # Calculate dimensions
        i_size = i_range[1] - i_range[0] + 1
        j_size = j_range[1] - j_range[0] + 1
        k_size = k_range[1] - k_range[0] + 1

        # Expected total size
        expected_size = i_size * j_size * k_size

        # Count actual values provided
        actual_values = fill_params['array_values']
        actual_size = len(actual_values)

        # Compare
        print(f"\nCell {cell.number} Fill Array Analysis:")
        print(f"  Declaration: fill= {i_range[0]}:{i_range[1]} "
              f"{j_range[0]}:{j_range[1]} {k_range[0]}:{k_range[1]}")
        print(f"  Dimensions: {i_size} × {j_size} × {k_size}")
        print(f"  Expected: {expected_size} values")
        print(f"  Actual: {actual_size} values")

        if actual_size == expected_size:
            print(f"  Status: ✓ Correct size")
        else:
            difference = actual_size - expected_size
            print(f"  Status: ✗ Size mismatch ({difference:+d})")
            print(f"  ERROR: Array has wrong number of values")

            if actual_size < expected_size:
                print(f"  Missing {expected_size - actual_size} values")
            else:
                print(f"  Extra {actual_size - expected_size} values")
```

**Step 2: Validate universe IDs in array**

```python
# Check that all values are valid integers
for i, val in enumerate(actual_values):
    if not isinstance(val, int):
        error(f"Cell {cell.number}: Non-integer value in fill array at position {i}: {val}")

    # Check if universe is defined (0 is OK - means void)
    if val != 0 and val not in defined_universes:
        error(f"Cell {cell.number}: Fill array references undefined universe {val}")
        print(f"  Position {i} in array (0-indexed)")

# Statistical analysis
if actual_values:
    unique_universes = set(actual_values) - {0}
    print(f"\n  Array composition:")
    print(f"    Unique universes used: {sorted(unique_universes)}")

    for u in sorted(unique_universes):
        count = actual_values.count(u)
        percentage = (count / len(actual_values)) * 100
        print(f"    u={u}: {count} times ({percentage:.1f}%)")
```

### Expected Output

```
✓ Fill array dimensions validated

Cell 200 Fill Array Analysis:
  Declaration: fill= -7:7 -7:7 0:0
  Dimensions: 15 × 15 × 1
  Expected: 225 values
  Actual: 225 values
  Status: ✓ Correct size

  Array composition:
    Unique universes used: [1, 2, 3]
    u=1: 196 times (87.1%)
    u=2: 24 times (10.7%)
    u=3: 5 times (2.2%)

Cell 500 Fill Array Analysis:
  Declaration: fill= -11:11 -11:11 0:0
  Dimensions: 23 × 23 × 1
  Expected: 529 values
  Actual: 529 values
  Status: ✓ Correct size
```

---

## Procedure 4: Universe Dependency Tree Construction

### Goal

Build complete universe hierarchy and detect circular references.

### Algorithm

**Step 1: Initialize data structures**

```python
universe_info = {}

# Include universe 0 (real world)
all_universes = {0} | defined_universes

for u in all_universes:
    universe_info[u] = {
        'cells': [],           # Cell numbers belonging to this universe
        'fills': [],           # Universes that this universe fills (children)
        'filled_by': [],       # Universes that fill this one (parents)
        'level': None,         # Hierarchy level (0 = real world)
    }
```

**Step 2: Build parent-child relationships**

```python
for cell in cells:
    # Determine which universe this cell belongs to
    u_num = abs(cell.parameters.get('u', 0))  # Default to 0 (real world)
    universe_info[u_num]['cells'].append(cell.number)

    # Check if this cell fills other universes
    if 'fill' in cell.parameters:
        fill_val = cell.parameters['fill']

        if isinstance(fill_val, int):
            # Simple fill: current universe fills into fill_val
            universe_info[u_num]['fills'].append(fill_val)
            universe_info[fill_val]['filled_by'].append(u_num)

        elif isinstance(fill_val, dict):
            # Array fill: get unique universe IDs
            unique_fills = set(fill_val['array_values']) - {0}

            for f_u in unique_fills:
                if f_u not in universe_info[u_num]['fills']:
                    universe_info[u_num]['fills'].append(f_u)
                if u_num not in universe_info[f_u]['filled_by']:
                    universe_info[f_u]['filled_by'].append(u_num)
```

**Step 3: Calculate hierarchy levels using breadth-first search**

```python
from collections import deque

# Start with real world (level 0)
queue = deque([(0, 0)])  # (universe_num, level)
visited = {0}

while queue:
    u, level = queue.popleft()
    universe_info[u]['level'] = level

    # Process universes this one fills (children)
    for filled_u in universe_info[u]['fills']:
        if filled_u not in visited:
            visited.add(filled_u)
            queue.append((filled_u, level + 1))

# Find maximum depth
max_level = max(
    info['level'] for info in universe_info.values()
    if info['level'] is not None
)

print(f"Universe hierarchy depth: {max_level} levels")

# Check for unreachable universes
unreachable = [u for u, info in universe_info.items()
               if info['level'] is None and u != 0]

if unreachable:
    print(f"⚠ WARNING: {len(unreachable)} unreachable universes: {unreachable}")
    print("  These universes are defined but not connected to real world")
```

**Step 4: Detect circular references using depth-first search**

```python
def find_cycles(u, visited, rec_stack, path, cycles):
    """
    DFS to find cycles in universe dependency graph

    u: current universe
    visited: set of all visited universes
    rec_stack: set of universes in current recursion stack
    path: list tracking current path
    cycles: list to store found cycles
    """
    visited.add(u)
    rec_stack.add(u)
    path.append(u)

    for filled_u in universe_info[u]['fills']:
        if filled_u not in visited:
            find_cycles(filled_u, visited, rec_stack, path, cycles)

        elif filled_u in rec_stack:
            # Found cycle
            cycle_start = path.index(filled_u)
            cycle = path[cycle_start:] + [filled_u]
            cycles.append(cycle)

    rec_stack.remove(u)
    path.pop()

# Check for cycles starting from real world
cycles = []
find_cycles(0, set(), set(), [], cycles)

if cycles:
    print("\n❌ FATAL: Circular universe references detected")
    for cycle in cycles:
        print(f"  {' → '.join(map(str, cycle))}")
    return False
else:
    print("✓ No circular references detected")
```

**Step 5: Display hierarchy tree**

```python
def print_tree(u, indent=0):
    """Recursively print universe tree"""
    info = universe_info[u]
    indent_str = "  " * indent

    # Format universe info
    if u == 0:
        name = "u=0 (real world)"
    else:
        name = f"u={u}"

    cell_count = len(info['cells'])
    fills_str = str(info['fills']) if info['fills'] else "none"

    print(f"{indent_str}{name}: {cell_count} cells, fills={fills_str}")

    # Recursively print children
    for child_u in sorted(info['fills']):
        print_tree(child_u, indent + 1)

print("\nUniverse Hierarchy:")
print_tree(0)
```

### Expected Output

```
✓ Universe dependency tree constructed
  • Max nesting depth: 6 levels
  • No circular references detected

Universe Hierarchy:
u=0 (real world): 2 cells, fills=[1, 2]
  u=1 (level 1): 3 cells, fills=[10, 20]
    u=10 (level 2): 2 cells, fills=[100]
      u=100 (level 3): 1 cell, fills=[200]
        u=200 (level 4): 1 cell, fills=[300]
          u=300 (level 5): 5 cells, fills=[]
    u=20 (level 2): 1 cell, fills=[]
  u=2 (level 1): 2 cells, fills=[30]
    u=30 (level 2): 1 cell, fills=[]

Performance Analysis:
  ✓ Nesting depth (6 levels) is acceptable
  ⚠ Consider negative universe optimization for level 4+ cells
```

---

## Procedure 5: Lattice Boundary Surface Validation

### Goal

Check that lattice cells have appropriate boundary surfaces for their lattice type.

### Algorithm

**Step 1: Validate LAT=1 (cubic) lattice boundaries**

```python
for cell, lat_value in lattice_cells:
    if lat_value == 1:
        surfaces = extract_surfaces_from_geometry(cell.geometry)
        surface_types = [get_surface_type(s) for s in surfaces]

        # Check for macrobodies (optimal)
        has_rpp = 'RPP' in surface_types
        has_box = 'BOX' in surface_types

        # Count plane types
        plane_count = sum(1 for st in surface_types
                         if st in ['P', 'PX', 'PY', 'PZ'])

        print(f"\nCell {cell.number} (LAT=1 Cubic):")
        print(f"  Surfaces: {surfaces}")
        print(f"  Types: {surface_types}")

        if has_rpp or has_box:
            print(f"  ✓ Using macrobody (optimal for cubic lattice)")
            print(f"    {'RPP' if has_rpp else 'BOX'} provides clean boundaries")

        elif plane_count >= 6:
            print(f"  ✓ Using {plane_count} planar surfaces")
            print(f"    Adequate for cubic lattice definition")

        else:
            print(f"  ⚠ Unusual boundary surfaces for cubic lattice")
            print(f"  Recommendations:")
            print(f"    • Use RPP macrobody: rpp xmin xmax ymin ymax zmin zmax")
            print(f"    • Or use 6 planes: PX, PY, PZ (2 each for x, y, z)")
```

**Step 2: Validate LAT=2 (hexagonal) lattice boundaries**

```python
for cell, lat_value in lattice_cells:
    if lat_value == 2:
        surfaces = extract_surfaces_from_geometry(cell.geometry)
        surface_types = [get_surface_type(s) for s in surfaces]

        # Check for hexagonal macrobodies (optimal)
        has_hex = 'HEX' in surface_types
        has_rhp = 'RHP' in surface_types

        # Count plane types
        p_count = surface_types.count('P')
        pz_count = surface_types.count('PZ')

        print(f"\nCell {cell.number} (LAT=2 Hexagonal):")
        print(f"  Surfaces: {surfaces}")
        print(f"  Types: {surface_types}")

        if has_hex or has_rhp:
            print(f"  ✓ Using hexagonal macrobody (optimal)")
            print(f"    {'HEX' if has_hex else 'RHP'} defines hexagonal prism")

        elif p_count >= 6 and pz_count >= 2:
            print(f"  ✓ Using {p_count} P-planes + {pz_count} PZ-planes")
            print(f"    Adequate for hexagonal lattice definition")

        else:
            print(f"  ⚠ Unusual boundary surfaces for hexagonal lattice")
            print(f"  Recommendations:")
            print(f"    • Use RHP macrobody: rhp vx vy vz hx hy hz r1 r2 r3")
            print(f"    • Or use 8 planes: 6 P-planes (hex sides) + 2 PZ (top/bottom)")
```

### Expected Output

```
✓ Lattice boundary surfaces checked

Cell 200 (LAT=1 Cubic):
  Surfaces: [200]
  Types: ['RPP']
  ✓ Using macrobody (optimal for cubic lattice)
    RPP provides clean boundaries

Cell 500 (LAT=2 Hexagonal):
  Surfaces: [500]
  Types: ['RHP']
  ✓ Using hexagonal macrobody (optimal)
    RHP defines hexagonal prism

Cell 800 (LAT=1 Cubic):
  Surfaces: [801, 802, 803, 804, 805, 806]
  Types: ['PX', 'PX', 'PY', 'PY', 'PZ', 'PZ']
  ✓ Using 6 planar surfaces
    Adequate for cubic lattice definition

Cell 850 (LAT=2 Hexagonal):
  Surfaces: [851, 852, 853]
  Types: ['CZ', 'PZ', 'PZ']
  ⚠ Unusual boundary surfaces for hexagonal lattice
  Recommendations:
    • Use RHP macrobody: rhp vx vy vz hx hy hz r1 r2 r3
    • Or use 8 planes: 6 P-planes (hex sides) + 2 PZ (top/bottom)
```

---

## Complete Validation Workflow

### Integrated Validation Script

```python
def validate_all_cell_features(input_file):
    """
    Complete cell card validation workflow
    Runs all 5 procedures in sequence
    """
    print(f"=" * 70)
    print(f"Cell Card Validation: {input_file}")
    print(f"=" * 70)

    all_valid = True

    # Procedure 1: Universe References
    print("\n[1/5] Validating universe references...")
    if not validate_universes(input_file):
        all_valid = False
        print("  ❌ Universe validation FAILED")
    else:
        print("  ✓ Universe validation passed")

    # Procedure 2: Lattice Types
    print("\n[2/5] Validating lattice types...")
    if not validate_lattice_types(input_file):
        all_valid = False
        print("  ❌ Lattice type validation FAILED")
    else:
        print("  ✓ Lattice type validation passed")

    # Procedure 3: Fill Array Dimensions
    print("\n[3/5] Validating fill array dimensions...")
    if not validate_fill_dimensions(input_file):
        all_valid = False
        print("  ❌ Fill dimension validation FAILED")
    else:
        print("  ✓ Fill dimension validation passed")

    # Procedure 4: Universe Dependency Tree
    print("\n[4/5] Building universe dependency tree...")
    if not build_and_validate_tree(input_file):
        all_valid = False
        print("  ❌ Dependency tree validation FAILED")
    else:
        print("  ✓ Dependency tree validation passed")

    # Procedure 5: Lattice Boundaries
    print("\n[5/5] Checking lattice boundary surfaces...")
    boundary_warnings = check_lattice_boundaries(input_file)
    if boundary_warnings:
        print(f"  ⚠ {len(boundary_warnings)} boundary recommendations")
    else:
        print("  ✓ All lattice boundaries appropriate")

    # Final summary
    print(f"\n" + "=" * 70)
    if all_valid:
        print("✓ CELL CARD VALIDATION PASSED")
        print("  All checks completed successfully")
        print("  Ready for MCNP execution")
    else:
        print("✗ CELL CARD VALIDATION FAILED")
        print("  Fix errors above before running MCNP")
    print("=" * 70)

    return all_valid
```

## References

- **MCNP6 Manual Chapter 5.2:** Cell card syntax and parameters
- **MCNP6 Manual Chapter 5.5.5:** Repeated structures validation
- **MCNP6 Manual Chapter 3.4.1:** Best practices for geometry setup

---

**END OF VALIDATION PROCEDURES REFERENCE**
