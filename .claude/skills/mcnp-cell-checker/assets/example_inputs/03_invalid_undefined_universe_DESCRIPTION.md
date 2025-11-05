# INVALID - Undefined Universe Reference

**Purpose**: Demonstrate undefined universe reference error (common mistake).

**Error**: Cell 1 has `fill=5` but no cell defines `u=5`.

**Key Issues**:
- ❌ Universe 5 used in fill= (cell 1)
- ❌ Universe 5 NOT defined anywhere
- ✓ Universe 1 defined but unused (orphan)

**Validation Checks**:
- ❌ FATAL: Universe 5 referenced but not defined
- ⚠ WARNING: Universe 1 defined but never used

**Expected Error**:
```
Universe validation: FAIL
  Defined: [1]
  Used: [5]
  Undefined: [5]  ← FATAL ERROR

Error: Universe 5 referenced in FILL (cell 1) but not defined with u=5
```

**How to Fix**:
1. Change `fill=5` to `fill=1` (use existing universe)
2. OR add cell with `u=5` (define the missing universe)
3. OR create separate universe 5 definition
