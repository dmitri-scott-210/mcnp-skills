# MCNP Cell Checker - Validation Procedures

Complete procedures for validating cell card features: universe references, lattice types, fill arrays, dependency trees, and boundary surfaces.

---

## Procedure 1: Universe Reference Validation

**Goal**: Ensure all `fill=` references have corresponding `u=` definitions

**Steps**:

1. **Parse all cell cards** and extract universe information:
   ```python
   cells = parse_input_file('input.inp')

   defined_universes = set()
   used_universes = set()

   for cell in cells:
       # Collect definitions
       if 'u' in cell.parameters:
           u_num = cell.parameters['u']
           if u_num in defined_universes:
               error(f"Duplicate universe definition: u={u_num}")
           defined_universes.add(u_num)

       # Collect references
       if 'fill' in cell.parameters:
           fill_value = cell.parameters['fill']
           if isinstance(fill_value, int):
               # Simple fill: fill=5
               used_universes.add(fill_value)
           elif isinstance(fill_value, list):
               # Array fill: fill= -3:3 ... 1 2 3 4 ...
               for u in fill_value['array_values']:
                   used_universes.add(u)
   ```

2. **Find undefined references**:
   ```python
   undefined = used_universes - defined_universes

   if undefined:
       for u in undefined:
           error(f"Universe {u} referenced in FILL but not defined with u={u}")
   ```

3. **Check for unused definitions** (warning only):
   ```python
   unused = defined_universes - used_universes

   if unused:
       warning(f"Unused universe definitions: {unused}")
   ```

4. **Check for universe 0 misuse**:
   ```python
   if 0 in defined_universes:
       error("Universe 0 cannot be explicitly defined (it is the default)")

   if 0 in used_universes:
       error("Universe 0 cannot be used in FILL (it is the real world)")
   ```

**Expected Output**:
```
✓ Universe validation passed
  • 15 universes defined: [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
  • 15 universes referenced
  • 0 undefined references
  • 2 unused definitions: [300, 400] (warning)
```

---

## Procedure 2: Lattice Type Validation

**Goal**: Verify LAT parameter values are valid (1 or 2 only)

**Steps**:

1. **Find all lattice cells**:
   ```python
   for cell in cells:
       if 'lat' in cell.parameters:
           lat_value = cell.parameters['lat']

           # Check valid values
           if lat_value not in [1, 2]:
               error(f"Cell {cell.number}: Invalid LAT={lat_value} "
                     "(must be 1 or 2)")

           # Check FILL requirement
           if 'fill' not in cell.parameters:
               error(f"Cell {cell.number}: LAT specified without FILL "
                     "(lattice requires fill)")

           # Check material (should be void)
           if cell.material != 0:
               error(f"Cell {cell.number}: Lattice cell must be void "
                     f"(has material {cell.material})")
   ```

2. **Validate surface count**:
   ```python
   if lat_value == 1:
       # Cubic lattice needs 6 bounding surfaces minimum
       surfaces = extract_surfaces(cell.geometry)
       if len(surfaces) < 6:
           warning(f"Cell {cell.number}: LAT=1 typically needs 6 surfaces "
                   f"for proper indexing (found {len(surfaces)})")

   elif lat_value == 2:
       # Hexagonal lattice needs 8 surfaces (6 sides + 2 bases)
       surfaces = extract_surfaces(cell.geometry)
       if len(surfaces) < 8:
           warning(f"Cell {cell.number}: LAT=2 typically needs 8 surfaces "
                   f"for hexagonal prism (found {len(surfaces)})")
   ```

**Expected Output**:
```
✓ Lattice type validation passed
  • Cell 200 (LAT=1): ✓ Cubic lattice, 6 surfaces
  • Cell 500 (LAT=2): ✓ Hexagonal lattice, 8 surfaces
  • Cell 800 (LAT=1): ✓ Cubic lattice, 6 surfaces
```

---

## Procedure 3: Fill Array Dimension Validation

**Goal**: Ensure fill array size matches lattice declaration

**Steps**:

1. **Parse fill declaration**:
   ```python
   for cell in lattice_cells:
       fill_params = cell.parameters['fill']

       if isinstance(fill_params, dict):  # Array fill
           # Extract range: fill= i1:i2 j1:j2 k1:k2
           i_range = fill_params['i_range']  # (i1, i2)
           j_range = fill_params['j_range']  # (j1, j2)
           k_range = fill_params['k_range']  # (k1, k2)

           # Calculate expected size
           i_size = i_range[1] - i_range[0] + 1
           j_size = j_range[1] - j_range[0] + 1
           k_size = k_range[1] - k_range[0] + 1
           expected_size = i_size * j_size * k_size

           # Count actual values
           actual_values = fill_params['array_values']
           actual_size = len(actual_values)

           # Compare
           if actual_size != expected_size:
               error(f"Cell {cell.number}: Fill array size mismatch\n"
                     f"  Declaration: fill= {i_range[0]}:{i_range[1]} "
                     f"{j_range[0]}:{j_range[1]} {k_range[0]}:{k_range[1]}\n"
                     f"  Expected: {i_size}×{j_size}×{k_size} = {expected_size} values\n"
                     f"  Found: {actual_size} values\n"
                     f"  Difference: {actual_size - expected_size}")
   ```

2. **Validate universe IDs in array**:
   ```python
   # Check that all values are integers
   for val in actual_values:
       if not isinstance(val, int):
           error(f"Cell {cell.number}: Non-integer value in fill array: {val}")

       # Values should be defined universe numbers
       if val != 0 and val not in defined_universes:
           error(f"Cell {cell.number}: Fill array references undefined "
                 f"universe {val}")
   ```

**Expected Output**:
```
✓ Fill array dimensions validated
  • Cell 200: 15×15×1 = 225 values (expected 225, found 225) ✓
  • Cell 500: 23×23×1 = 529 values (expected 529, found 529) ✓
  • Cell 800: 7×7×3 = 147 values (expected 147, found 147) ✓
```

---

## Procedure 4: Universe Dependency Tree Construction

**Goal**: Build complete universe hierarchy and detect circular references

**Steps**:

1. **Initialize data structures**:
   ```python
   universe_info = {}
   for u in all_universe_numbers:
       universe_info[u] = {
           'cells': [],           # Cells belonging to this universe
           'fills': [],           # Universes that this universe fills
           'filled_by': [],       # Universes that fill this one
           'level': None,         # Hierarchy level (0 = real world)
       }
   ```

2. **Build relationships**:
   ```python
   for cell in cells:
       u_num = cell.parameters.get('u', 0)  # Default = real world
       universe_info[u_num]['cells'].append(cell.number)

       if 'fill' in cell.parameters:
           fill_val = cell.parameters['fill']

           if isinstance(fill_val, int):
               # Simple fill
               universe_info[u_num]['fills'].append(fill_val)
               universe_info[fill_val]['filled_by'].append(u_num)

           elif isinstance(fill_val, dict):
               # Array fill - get unique universe IDs
               unique_fills = set(fill_val['array_values'])
               for f_u in unique_fills:
                   universe_info[u_num]['fills'].append(f_u)
                   universe_info[f_u]['filled_by'].append(u_num)
   ```

3. **Calculate hierarchy levels** (breadth-first search):
   ```python
   from collections import deque

   # Start with real world (level 0)
   queue = deque([(0, 0)])  # (universe_num, level)
   visited = {0}

   while queue:
       u, level = queue.popleft()
       universe_info[u]['level'] = level

       # Process universes this one fills
       for filled_u in universe_info[u]['fills']:
           if filled_u not in visited:
               visited.add(filled_u)
               queue.append((filled_u, level + 1))

   max_level = max(info['level'] for info in universe_info.values()
                   if info['level'] is not None)
   ```

4. **Detect circular references**:
   ```python
   def find_cycles(u, visited, rec_stack, path):
       """DFS to find cycles in universe dependency graph"""
       visited.add(u)
       rec_stack.add(u)
       path.append(u)

       for filled_u in universe_info[u]['fills']:
           if filled_u not in visited:
               if find_cycles(filled_u, visited, rec_stack, path):
                   return True
           elif filled_u in rec_stack:
               # Found cycle
               cycle_start = path.index(filled_u)
               cycle = path[cycle_start:] + [filled_u]
               error(f"Circular universe reference: "
                     f"{' → '.join(map(str, cycle))}")
               return True

       rec_stack.remove(u)
       path.pop()
       return False

   # Check for cycles starting from real world
   find_cycles(0, set(), set(), [])
   ```

**Expected Output**:
```
✓ Universe dependency tree constructed
  • Max nesting depth: 6 levels
  • No circular references detected

  Hierarchy:
    u=0 (real world): 5 cells, fills=[1, 2]
      u=1 (level 1): 3 cells, fills=[10, 20]
        u=10 (level 2): 2 cells, fills=[100]
          u=100 (level 3): 1 cell, fills=[200]
            u=200 (level 4): 1 cell, fills=[300]
              u=300 (level 5): 5 cells, fills=[]
        u=20 (level 2): 1 cell, fills=[]
      u=2 (level 1): 2 cells, fills=[30]
        u=30 (level 2): 1 cell, fills=[]
```

---

## Procedure 5: Lattice Boundary Surface Validation

**Goal**: Check that lattice cells have appropriate boundary surfaces

**Steps**:

1. **For LAT=1 (cubic) lattices**:
   ```python
   for cell in cubic_lattice_cells:
       surfaces = extract_surfaces(cell.geometry)
       surface_types = [get_surface_type(s) for s in surfaces]

       # Recommend RPP (right parallelepiped) or 6 planes
       has_rpp = 'RPP' in surface_types
       has_box = 'BOX' in surface_types
       plane_count = surface_types.count('P') + surface_types.count('PX') + \
                     surface_types.count('PY') + surface_types.count('PZ')

       if has_rpp or has_box:
           info(f"Cell {cell.number} (LAT=1): Using macrobody (optimal)")
       elif plane_count >= 6:
           info(f"Cell {cell.number} (LAT=1): Using {plane_count} planes")
       else:
           warning(f"Cell {cell.number} (LAT=1): Unusual boundary surfaces\n"
                   f"  Recommend: RPP macrobody or 6 planes\n"
                   f"  Found: {surface_types}")
   ```

2. **For LAT=2 (hexagonal) lattices**:
   ```python
   for cell in hex_lattice_cells:
       surfaces = extract_surfaces(cell.geometry)
       surface_types = [get_surface_type(s) for s in surfaces]

       # Recommend HEX macrobody or 6 planes + 2 z-planes
       has_hex = 'HEX' in surface_types
       has_rhp = 'RHP' in surface_types
       p_count = surface_types.count('P')
       pz_count = surface_types.count('PZ')

       if has_hex or has_rhp:
           info(f"Cell {cell.number} (LAT=2): Using hexagonal macrobody (optimal)")
       elif p_count >= 6 and pz_count >= 2:
           info(f"Cell {cell.number} (LAT=2): Using {p_count} planes + "
                f"{pz_count} z-planes")
       else:
           warning(f"Cell {cell.number} (LAT=2): Unusual boundary surfaces\n"
                   f"  Recommend: HEX macrobody or 6 P surfaces + 2 PZ surfaces\n"
                   f"  Found: {surface_types}")
   ```

**Expected Output**:
```
✓ Lattice boundary surfaces checked
  • Cell 200 (LAT=1): Using RPP macrobody (optimal)
  • Cell 500 (LAT=2): Using HEX macrobody (optimal)
  • Cell 800 (LAT=1): Using 6 planes

  ⚠ 1 recommendation:
    • Cell 850 (LAT=2): Using cylinders instead of hexagonal prism
      Recommend: HEX macrobody or 6 P + 2 PZ surfaces
```

---

**END OF VALIDATION_PROCEDURES.MD**
