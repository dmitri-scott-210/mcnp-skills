# MCNP Cell Card Error Catalog

**Purpose:** Common cell card problems with symptoms, diagnosis, and solutions

---

## Problem 1: Undefined Universe Reference

### Symptoms

```
FATAL ERROR: Universe 50 not found
         Cell 200 references fill=50 but no cell has u=50
```

### Diagnosis

```python
# Check universe definitions
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
universe_check = checker.validate_universes('input.inp')

undefined = universe_check['undefined']
print(f"Undefined universes: {undefined}")  # [50]
```

### Root Causes

1. Typo in universe number (u=50 vs u=5)
2. Deleted cell that defined u=50
3. Copy-paste error from different input
4. Off-by-one error in lattice fill array

### Solutions

**BAD: Reference without definition**
```
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 50 3 2 1    ✗ u=50 not defined
    ...
```

**GOOD: Define the universe**
```
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 50 3 2 1    ✓ u=50 defined below
    ...
500 1 -10.5 -500 u=50 imp:n=1    ✓ Universe 50 definition
```

**GOOD: Fix the typo**
```
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 5 3 2 1     ✓ Changed 50 → 5
    ...
50 1 -10.5 -50 u=5 imp:n=1       ✓ u=5 already defined
```

---

## Problem 2: Fill Array Dimension Mismatch

### Symptoms

```
FATAL ERROR: Cell 200 fill array size incorrect
         Expected 225 values (15×15×1), found 210
```

### Diagnosis

```python
# Check fill dimensions
fill_check = checker.check_fill_dimensions('input.inp')

for cell, result in fill_check.items():
    if result['expected_size'] != result['actual_size']:
        print(f"Cell {cell}:")
        print(f"  Expected: {result['expected_size']}")
        print(f"  Actual: {result['actual_size']}")
        print(f"  Missing: {result['expected_size'] - result['actual_size']}")
```

### Root Causes

1. Miscounted array values
2. Wrong range in fill declaration
3. Copy-paste missing lines
4. Off-by-one in range calculation

### Solutions

**BAD: Missing values**
```
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
    ... (only 210 lines, missing 15)
✗ Expected 15×15×1 = 225 values, found 210
```

**GOOD: Complete array**
```
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40
    ... (all 15 lines present)
✓ Expected 15×15×1 = 225 values, found 225
```

**GOOD: Correct the range**
```
200 0 -200 lat=1 fill=-6:7 -7:7 0:0 imp:n=1
    ... (210 values)
✓ Expected 14×15×1 = 210 values, found 210
```

### Prevention

Use comments to track array size:
```
c Lattice cell 200: 15×15×1 cubic array (225 values)
c Each line = 15 values (i = -7 to 7)
c Need 15 lines (j = -7 to 7)
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40  $ j=-7
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40  $ j=-6
    ...
```

---

## Problem 3: Circular Universe Reference

### Symptoms

```
FATAL ERROR: Circular universe dependency detected
         u=1 fills u=2, u=2 fills u=1 (infinite loop)
```

### Diagnosis

```python
# Build dependency tree
tree = checker.build_universe_tree('input.inp')

if tree['circular_refs']:
    print("Circular references detected:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))} → (loops back)")
```

### Root Causes

1. Recursive fill structure
2. Copy-paste error creating loop
3. Misunderstanding universe hierarchy

### Solutions

**BAD: Direct circular reference**
```
100 0 -100 u=1 fill=2 imp:n=1    ✗ u=1 fills u=2
200 0 -200 u=2 fill=1 imp:n=1    ✗ u=2 fills u=1 (circular!)
```

**GOOD: Hierarchical structure**
```
100 0 -100 u=1 fill=2 imp:n=1    ✓ u=1 fills u=2
200 0 -200 u=2 imp:n=1           ✓ u=2 is terminal (no fill)
```

**BAD: Indirect circular reference**
```
100 0 -100 u=1 fill=2 imp:n=1    ✗ u=1 → u=2
200 0 -200 u=2 fill=3 imp:n=1    ✗ u=2 → u=3
300 0 -300 u=3 fill=1 imp:n=1    ✗ u=3 → u=1 (circular!)
```

**GOOD: Linear hierarchy**
```
100 0 -100 u=1 fill=2 imp:n=1    ✓ u=1 → u=2
200 0 -200 u=2 fill=3 imp:n=1    ✓ u=2 → u=3
300 1 -2.7 -300 u=3 imp:n=1      ✓ u=3 terminal (has material)
```

---

## Problem 4: Invalid Lattice Type

### Symptoms

```
FATAL ERROR: Invalid LAT value
         Cell 200 has lat=3 (must be 1 or 2)
```

### Diagnosis

```python
# Validate lattice types
lattice_results = checker.validate_lattices('input.inp')

for cell, result in lattice_results.items():
    if result['errors']:
        for err in result['errors']:
            print(f"Cell {cell}: {err}")
```

### Root Causes

1. Typo (lat=3 instead of lat=1)
2. Confusion about lattice types
3. Trying to use non-existent lattice type

### Solutions

**BAD: Invalid LAT value**
```
200 0 -200 lat=3 fill=1 imp:n=1    ✗ lat=3 doesn't exist
```

**GOOD: Cubic lattice**
```
200 0 -200 lat=1 fill=1 imp:n=1    ✓ lat=1 (cubic)
```

**GOOD: Hexagonal lattice**
```
200 0 -200 lat=2 fill=1 imp:n=1    ✓ lat=2 (hexagonal)
```

**BAD: Lattice without FILL**
```
200 0 -200 lat=1 imp:n=1           ✗ LAT requires FILL
```

**GOOD: Lattice with FILL**
```
200 0 -200 lat=1 fill=5 imp:n=1    ✓ Complete specification
```

---

## Problem 5: Lattice Cell with Material

### Symptoms

```
WARNING: Lattice cell has material
         Cell 200 has lat=1 but material 1 (should be void)
```

### Diagnosis

```python
for cell in cells:
    if 'lat' in cell.parameters:
        if cell.material != 0:
            warning(f"Cell {cell.number}: Lattice cell should be void, "
                   f"has material {cell.material}")
```

### Root Causes

1. Misunderstanding lattice structure
2. Trying to add background material
3. Copy-paste from non-lattice cell

### Solutions

**BAD: Lattice with material**
```
200 1 -2.7 -200 lat=1 fill=5 imp:n=1    ✗ Material in lattice cell
```

**GOOD: Void lattice**
```
200 0 -200 lat=1 fill=5 imp:n=1         ✓ Lattice cell is void
```

**If you want background material:**
```
200 0 -200 lat=1 fill=5 imp:n=1         ✓ Lattice (void)
300 1 -2.7 -300 u=5 imp:n=1             ✓ Background in universe 5
400 2 -8.0 -400 u=5 imp:n=1             ✓ Embedded objects
```

---

## Problem 6: Deep Nesting Performance

### Symptoms

```
WARNING: Universe nesting depth is 12 levels
         This may cause performance degradation
```

### Diagnosis

```python
tree = checker.build_universe_tree('input.inp')

if tree['max_depth'] > 10:
    warning(f"Deep nesting detected: {tree['max_depth']} levels\n"
            f"  Performance may be impacted\n"
            f"  Consider simplification or negative universe optimization")
```

### Solutions

**Strategy 1: Use negative universe numbers for enclosed cells**
```
BAD:
  500 1 -10.5 -500 u=50 imp:n=1    ✗ Positive u (slower)

GOOD:
  500 1 -10.5 -500 u=-50 imp:n=1   ✓ Negative u (faster)
  $ Negative indicates fully enclosed, no higher-level checks
```

**Strategy 2: Combine universe levels**
```
BAD: Excessive levels
  u=1 → u=2 → u=3 → u=4 → u=5 → u=6 → u=7 → u=8 → u=9 → u=10 → u=11 → u=12

GOOD: Consolidated
  u=1 → u=2 → u=5 → u=10                    ✓ 4 levels instead of 12
```

**Strategy 3: Homogenize lower levels**
```
Instead of modeling every detail:
  Replace detailed TRISO particle structure with homogenized material
```

---

**END OF ERROR CATALOG**
