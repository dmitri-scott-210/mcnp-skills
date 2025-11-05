# Cell Card Troubleshooting Guide

This document provides detailed problem-solving guidance for common MCNP cell card errors related to universes, lattices, and fill arrays.

## Overview

Cell card errors are among the most common and difficult-to-debug issues in MCNP modeling. This guide covers six major problem types with symptoms, diagnosis procedures, root causes, and complete solutions.

---

## Problem 1: Undefined Universe Reference

### Symptoms

**MCNP Fatal Error Message:**
```
FATAL ERROR: Universe 50 not found
         Cell 200 references fill=50 but no cell has u=50
```

**Or:**
```
ERROR: FILL references undefined universe
     Cell 300: fill= array contains universe 75
     No cell with u=75 found in input
```

### Diagnosis Procedure

**Step 1: Run universe validation**
```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
universe_check = checker.validate_universes('input.inp')

print(f"Defined universes: {universe_check['defined']}")
print(f"Used universes: {universe_check['used']}")
print(f"Undefined: {universe_check['undefined']}")
```

**Step 2: Locate the reference**
```bash
# Search for fill= statements in input
grep -n "fill=" input.inp

# Search for specific universe
grep -n "fill=50" input.inp
grep -n "u=50" input.inp
```

### Root Causes

1. **Typo in universe number**
   - Defined: `u=5`
   - Referenced: `fill=50`
   - Off-by-one or extra digit

2. **Deleted cell definition**
   - Previously had cell with `u=50`
   - Cell was deleted but fill references remain
   - Incomplete edit operation

3. **Copy-paste from different input**
   - Copied cell card from another model
   - Universe numbering scheme different
   - References don't match current file

4. **Off-by-one in lattice fill array**
   - Array value should be `5` but entered `50`
   - Especially common in large arrays

5. **Universe defined in wrong file**
   - Multi-file MCNP setup
   - Universe in different include file
   - Include file not loaded or wrong path

### Solutions

**Solution 1: Define the missing universe**

```
✗ BEFORE (error):
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 50 3 2 1    ← u=50 referenced but not defined
    1 2 3 3 3 2 1
    1 2 2 2 2 2 1
    1 2 2 2 2 2 1
    1 1 1 1 1 1 1

✓ AFTER (fixed):
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 50 3 2 1    ← Now u=50 is defined below
    1 2 3 3 3 2 1
    1 2 2 2 2 2 1
    1 2 2 2 2 2 1
    1 1 1 1 1 1 1

c Universe 50 definition (added)
500 1 -10.5 -500 u=50 imp:n=1         $ Control rod fuel
501 2 -6.5 500 -501 u=50 imp:n=1      $ Control rod clad
502 3 -1.0 501 -502 u=50 imp:n=1      $ Coolant
```

**Solution 2: Fix the typo**

```
✗ BEFORE (typo):
200 0 -200 fill=50 imp:n=1             ← Should be fill=5
50 1 -10.5 -50 u=5 imp:n=1             ← Defined as u=5

✓ AFTER (corrected):
200 0 -200 fill=5 imp:n=1              ← Fixed to match definition
50 1 -10.5 -50 u=5 imp:n=1
```

**Solution 3: Remove unused reference**

```
✗ BEFORE (orphaned reference):
200 0 -200 fill=99 imp:n=1             ← u=99 no longer exists
c Cell 990 with u=99 was deleted

✓ AFTER (removed):
c Cell 200 removed because u=99 no longer exists
c or re-designed to not need universe fill
```

**Solution 4: Search and replace in fill array**

```
✗ BEFORE (wrong value in array):
300 0 -300 lat=1 fill=-10:10 -10:10 0:0 imp:n=1
    1 1 1 ... 1 1 1
    ... multiple lines ...
    1 1 50 1 1 1 ...    ← Should be 5, not 50
    ... more lines ...

✓ AFTER (corrected):
300 0 -300 lat=1 fill=-10:10 -10:10 0:0 imp:n=1
    1 1 1 ... 1 1 1
    ... multiple lines ...
    1 1 5 1 1 1 ...     ← Fixed to correct universe
    ... more lines ...
```

### Prevention Strategies

1. **Create universe reference map at top of input**
```
c =================================================================
c UNIVERSE REFERENCE MAP
c =================================================================
c u=1:  Standard fuel pin
c u=2:  Guide tube
c u=3:  Instrumentation tube
c u=5:  Fuel pin with burnable poison
c u=50: Control rod (withdrawn)
c u=51: Control rod (inserted)
c =================================================================
```

2. **Use consistent numbering scheme**
```
c Pin types: 1-9
c Assembly types: 10-99
c Core regions: 100-999
c Vessel components: 1000-9999
```

3. **Validate before every run**
```bash
python scripts/validate_cells_prerun.py input.inp
```

---

## Problem 2: Fill Array Dimension Mismatch

### Symptoms

**MCNP Fatal Error:**
```
FATAL ERROR: Cell 200 fill array size incorrect
         Expected 225 values (15×15×1), found 210
```

**Or:**
```
ERROR: Fill array dimensions don't match declaration
     Cell 500: fill= -11:11 -11:11 0:0
     Expected: 529 values (23×23×1)
     Found: 482 values
     Missing: 47 values
```

### Diagnosis Procedure

**Step 1: Run fill dimension validator**
```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
fill_check = checker.check_fill_dimensions('input.inp')

for cell, result in fill_check.items():
    if result['expected_size'] != result['actual_size']:
        print(f"Cell {cell}:")
        print(f"  Expected: {result['expected_size']}")
        print(f"  Actual: {result['actual_size']}")
        print(f"  Difference: {result['expected_size'] - result['actual_size']}")
        print(f"  Declaration: {result['declaration']}")
```

**Step 2: Manual verification**
```bash
# Extract fill array from input
sed -n '/^200.*lat=1.*fill=/,/^[0-9]/p' input.inp > cell200_fill.txt

# Count values in array
wc -w cell200_fill.txt

# Calculate expected
# For fill= -7:7 -7:7 0:0
# i: -7 to 7 = 15 values
# j: -7 to 7 = 15 values
# k: 0 to 0 = 1 value
# Total: 15 × 15 × 1 = 225
```

### Root Causes

1. **Miscounted array values**
   - Manually created large array
   - Lost track of rows/columns
   - Common with 15×15 or larger

2. **Wrong range in fill declaration**
   - Intended: `fill= -7:7` (15 values)
   - Typed: `fill= -7:6` (14 values)
   - Array has correct 210 values for 14×15, but declaration wrong

3. **Copy-paste missing lines**
   - Copied array from another input
   - Copy didn't capture all lines
   - Missing final rows

4. **Editor line wrapping**
   - Text editor wrapped long lines
   - Appeared complete but values missing
   - Line continuation issues

5. **Off-by-one in range calculation**
   - Thought -7:7 = 14 values (subtraction)
   - Actually = 15 values (inclusive range)

### Solutions

**Solution 1: Complete the array**

```
✗ BEFORE (incomplete - 210 values):
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40    $ j=-7 (15 values)
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40    $ j=-6 (15 values)
    40 40 40 40 40 50 50 50 50 50 40 40 40 40 40    $ j=-5
    ... (only 14 lines total = 210 values)

✓ AFTER (complete - 225 values):
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40    $ j=-7
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40    $ j=-6
    40 40 40 40 40 50 50 50 50 50 40 40 40 40 40    $ j=-5
    40 40 40 40 50 50 50 50 50 50 50 40 40 40 40    $ j=-4
    40 40 40 50 50 50 50 50 50 50 50 50 40 40 40    $ j=-3
    40 40 50 50 50 50 50 50 50 50 50 50 50 40 40    $ j=-2
    40 40 50 50 50 50 50 50 50 50 50 50 50 40 40    $ j=-1
    40 50 50 50 50 50 50 50 50 50 50 50 50 50 40    $ j=0 (center)
    40 40 50 50 50 50 50 50 50 50 50 50 50 40 40    $ j=1
    40 40 50 50 50 50 50 50 50 50 50 50 50 40 40    $ j=2
    40 40 40 50 50 50 50 50 50 50 50 50 40 40 40    $ j=3
    40 40 40 40 50 50 50 50 50 50 50 40 40 40 40    $ j=4
    40 40 40 40 40 50 50 50 50 50 40 40 40 40 40    $ j=5
    40 40 40 40 40 40 40 50 40 40 40 40 40 40 40    $ j=6
    40 40 40 40 40 40 40 40 40 40 40 40 40 40 40    $ j=7
c (Now 15 lines = 225 values)
```

**Solution 2: Correct the range declaration**

```
✗ BEFORE (range doesn't match array):
200 0 -200 lat=1 fill=-7:7 -7:7 0:0 imp:n=1
    ... (actually 14 lines × 15 values = 210 total)

✓ AFTER (corrected range to match actual array):
200 0 -200 lat=1 fill=-7:6 -7:7 0:0 imp:n=1
    ... (14 lines × 15 values = 210 total)
c (Changed j-range from -7:7 to -7:6)
```

**Solution 3: Use script to generate array**

```python
# generate_fill_array.py
def create_fill_array(i_range, j_range, k_range, pattern_func):
    """Generate fill array with correct dimensions"""
    i1, i2 = i_range
    j1, j2 = j_range
    k1, k2 = k_range

    array = []
    for k in range(k1, k2+1):
        for j in range(j1, j2+1):
            row = []
            for i in range(i1, i2+1):
                u = pattern_func(i, j, k)
                row.append(u)
            array.append(row)

    # Format output
    i_size = i2 - i1 + 1
    j_size = j2 - j2 + 1
    k_size = k2 - k1 + 1
    total = i_size * j_size * k_size

    print(f"c Fill array: {i_size}×{j_size}×{k_size} = {total} values")
    print(f"fill= {i1}:{i2} {j1}:{j2} {k1}:{k2}")

    for row in array:
        print("    " + " ".join(map(str, row)))

# Example usage
def my_pattern(i, j, k):
    """Define universe pattern"""
    dist = (i**2 + j**2)**0.5
    if dist < 3:
        return 50  # Center region
    elif dist < 7:
        return 40  # Middle region
    else:
        return 30  # Outer region

create_fill_array((-7, 7), (-7, 7), (0, 0), my_pattern)
```

### Prevention Strategies

1. **Always document dimensions**
```
c LATTICE CELL 200: 15×15×1 cubic array
c Declaration: fill= -7:7 -7:7 0:0
c i-direction: -7 to 7 (15 elements)
c j-direction: -7 to 7 (15 elements)
c k-direction: 0 to 0 (1 element)
c Total values required: 15 × 15 × 1 = 225
c Each line below = 15 values (i=-7 to i=7)
c Need exactly 15 lines (j=-7 to j=7)
```

2. **Add row/column labels**
```
200 0 -200 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1    $ j=-3 (7 values)
    1 2 2 2 2 2 1    $ j=-2
    1 2 3 3 3 2 1    $ j=-1
    1 2 3 4 3 2 1    $ j=0 (center)
    1 2 3 3 3 2 1    $ j=1
    1 2 2 2 2 2 1    $ j=2
    1 1 1 1 1 1 1    $ j=3 (last row)
```

3. **Validate with checker**
```bash
python scripts/fill_array_validator.py input.inp
```

---

## Problem 3: Circular Universe Reference

### Symptoms

**MCNP Fatal Error:**
```
FATAL ERROR: Circular universe dependency detected
         u=1 fills u=2, u=2 fills u=1 (infinite loop)
```

**Or:**
```
ERROR: Infinite universe loop
     u=1 → u=2 → u=3 → u=1
     Cannot resolve hierarchy
```

### Diagnosis Procedure

**Step 1: Build dependency tree**
```python
from mcnp_cell_checker import MCNPCellChecker

checker = MCNPCellChecker()
tree = checker.build_universe_tree('input.inp')

if tree['circular_refs']:
    print("Circular references detected:")
    for cycle in tree['circular_refs']:
        print(f"  {' → '.join(map(str, cycle))}")
```

**Step 2: Visualize hierarchy**
```python
from universe_tree_visualizer import visualize_tree

visualize_tree('input.inp', output='universe_tree.txt')
```

**Step 3: Manual inspection**
```bash
# Find all fill= statements
grep -n "fill=" input.inp

# For each universe N, check what it fills
grep "u=1" input.inp | grep "fill="
grep "u=2" input.inp | grep "fill="
grep "u=3" input.inp | grep "fill="
```

### Root Causes

1. **Copy-paste error creating loop**
   - Copied cell with `u=1 fill=2`
   - Pasted and changed to `u=2 fill=1`
   - Created circular dependency

2. **Misunderstanding universe hierarchy**
   - Thought universes could reference each other bidirectionally
   - Expected: u=1 ↔ u=2 (bidirectional)
   - Reality: Must be u=1 → u=2 (unidirectional, acyclic)

3. **Editing error during restructuring**
   - Changed fill references without updating hierarchy
   - Broke previously valid structure

4. **Indirect circular reference**
   - u=1 → u=2 → u=3 → u=1
   - Not obvious from looking at any single cell
   - Requires dependency analysis

### Solutions

**Solution 1: Break the cycle (direct)**

```
✗ BEFORE (circular):
100 0 -100 u=1 fill=2 imp:n=1    ← u=1 fills u=2
200 0 -200 u=2 fill=1 imp:n=1    ← u=2 fills u=1 (CIRCULAR!)

✓ AFTER (linear):
100 0 -100 u=1 fill=2 imp:n=1    ← u=1 fills u=2
200 0 -200 u=2 imp:n=1           ← u=2 is terminal (no fill)
c or
200 1 -2.7 -200 u=2 imp:n=1      ← u=2 has material (terminal)
```

**Solution 2: Restructure hierarchy (indirect cycle)**

```
✗ BEFORE (indirect circular):
100 0 -100 u=1 fill=2 imp:n=1    ← u=1 → u=2
200 0 -200 u=2 fill=3 imp:n=1    ← u=2 → u=3
300 0 -300 u=3 fill=1 imp:n=1    ← u=3 → u=1 (CIRCULAR!)

✓ AFTER (linear hierarchy):
100 0 -100 u=1 fill=2 imp:n=1    ← u=1 → u=2
200 0 -200 u=2 fill=3 imp:n=1    ← u=2 → u=3
300 1 -2.7 -300 u=3 imp:n=1      ← u=3 terminal (has material)
```

**Solution 3: Redesign with proper levels**

```
✗ BEFORE (confused structure):
c Trying to have pins fill assemblies AND assemblies fill pins
100 0 -100 u=1 fill=10 imp:n=1   ← Assembly fills pins
1000 0 -1000 u=10 fill=1 imp:n=1 ← Pin fills assembly (WRONG!)

✓ AFTER (correct hierarchy):
c Level 0: Real world
1 0 -1 fill=1 imp:n=1                    ← Core fills with assemblies

c Level 1: Assembly lattice
100 0 -100 u=1 lat=1 fill=... imp:n=1   ← Assembly lattice fills with pins

c Level 2: Pin cells
1000 1 -10.5 -1000 u=10 imp:n=1          ← Pin (terminal)
```

### Prevention Strategies

1. **Design hierarchy before coding**
```
Level 0: Real world → fills with u=1
Level 1: Core (u=1) → fills with u=10, u=20
Level 2: Assemblies (u=10, u=20) → fill with u=100
Level 3: Pins (u=100) → terminal (no fill)
```

2. **Check after every edit**
```bash
python scripts/validate_cells_prerun.py input.inp
# Look for "Circular reference detected"
```

3. **Use visualization**
```bash
python scripts/universe_tree_visualizer.py input.inp
# Visual inspection of hierarchy
```

---

## Problem 4: Invalid Lattice Type

### Symptoms

**MCNP Fatal Error:**
```
FATAL ERROR: Invalid LAT value
         Cell 200 has lat=3 (must be 1 or 2)
```

### Diagnosis & Solutions

See `validation_procedures.md` for complete lattice validation.

**Common mistakes:**
```
✗ lat=0  (doesn't exist)
✗ lat=3  (doesn't exist)
✗ lat=-1 (doesn't exist)

✓ lat=1  (cubic/rectangular)
✓ lat=2  (hexagonal)
```

---

## Problem 5: Lattice Cell with Material

### Symptoms

**MCNP Warning:**
```
WARNING: Lattice cell has material
         Cell 200 has lat=1 but material 1
         Lattice cells should be void (material 0)
```

### Solutions

```
✗ WRONG:
200 1 -2.7 -200 lat=1 fill=5 imp:n=1

✓ CORRECT:
200 0 -200 lat=1 fill=5 imp:n=1
```

---

## Problem 6: Deep Nesting Performance

### Symptoms

- Very slow particle tracking
- High memory usage
- Long computation times

### Diagnosis

```python
tree = checker.build_universe_tree('input.inp')
print(f"Max depth: {tree['max_depth']} levels")

if tree['max_depth'] > 10:
    print("⚠ Deep nesting detected - performance impact expected")
```

### Solutions

See `best_practices_detail.md` for optimization strategies.

---

**END OF TROUBLESHOOTING GUIDE**
