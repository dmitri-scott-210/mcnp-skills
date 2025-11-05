# INVALID - Lattice Fill Array Dimension Mismatch

**Purpose**: Demonstrate fill array size mismatch error (very common mistake).

**Error**: Lattice declares `fill=-2:2 -2:2 0:0` (5×5×1 = 25 values) but only 20 values provided.

**Key Issues**:
- ❌ Expected: 5×5×1 = 25 values
- ❌ Actual: Only 20 values (4 rows × 5 columns)
- ❌ Missing: 1 complete row (5 values)

**Calculation**:
```
Declaration: fill=-2:2 -2:2 0:0
  i: -2 to 2 = 5 values
  j: -2 to 2 = 5 values
  k: 0 to 0 = 1 value
  Total: 5 × 5 × 1 = 25 values required

Provided:
  Row 1: 1 1 1 1 1 (5 values)
  Row 2: 1 2 2 2 1 (5 values)
  Row 3: 1 2 3 2 1 (5 values)
  Row 4: 1 2 2 2 1 (5 values)
  Total: 20 values

Missing: 5 values (1 complete row)
```

**Expected Error**:
```
Fill array dimension validation: FAIL
  Cell 100:
    Declaration: fill=-2:2 -2:2 0:0
    Expected: 25 values (5×5×1)
    Found: 20 values
    Missing: 5 values
```

**How to Fix**:
1. Add missing 5th row: `1 1 1 1 1`
2. OR change declaration to `fill=-2:2 -1:2 0:0` (5×4×1 = 20)
3. OR use comments to track array size and avoid this error
