# Example 02: Fill Array Dimension Mismatch

## Problem Demonstrated

**Before file:** `02_fill_mismatch_before.i`

Common error where fill array size doesn't match declaration:
- Declaration: `FILL=-2:2 -2:2 0:0`
- Expected: (2-(-2)+1) × (2-(-2)+1) × (0-0+1) = 5 × 5 × 1 = **25 values**
- Provided: Only **20 values** (4 complete rows + incomplete 5th row missing)

## MCNP Error Message

```
FATAL ERROR: Cell 100 fill array size incorrect
         Expected 25 values (5×5×1), found 20
```

## Diagnosis

Run validation:
```bash
python scripts/fill_array_validator.py 02_fill_mismatch_before.i
```

Output:
```
Cell 100:
  Declaration: fill= -2:2 -2:2 0:0
  Dimensions: 5 × 5 × 1
  Expected: 25 values
  Actual: 20 values
  Status: ✗ Size mismatch (-5)
  ERROR: Missing 5 values
```

## Solution

**After file:** `02_fill_mismatch_after.i`

Added the missing 5th row:
- Row 5 (j=2): `10 10 10 10 10` (5 values)
- Total now: 5 rows × 5 columns = 25 values ✓

## Validation

```bash
python scripts/fill_array_validator.py 02_fill_mismatch_after.i
```

Should show:
```
Cell 100:
  Declaration: fill= -2:2 -2:2 0:0
  Dimensions: 5 × 5 × 1
  Expected: 25 values
  Actual: 25 values
  Status: ✓ Correct size
```

## Key Learning Points

1. **Calculate expected size:** (i2-i1+1) × (j2-j1+1) × (k2-k1+1)
2. **Count carefully:** Easy to miscount in large arrays
3. **Use comments:** Document dimensions in input file
4. **Visual inspection:** Format arrays to show rows clearly
5. **Automate:** Use scripts to generate large arrays

## Prevention Strategies

Add comments to document array:
```
c Lattice: 5×5×1 array (25 values)
c Each line = 5 values (i = -2 to 2)
c Need 5 lines (j = -2 to 2)
100  0   -100      U=1  LAT=1  FILL=-2:2 -2:2 0:0  IMP:N=1
    10 10 10 10 10    $ j=-2
    10 20 20 20 10    $ j=-1
    10 20 30 20 10    $ j=0 (center)
    10 20 20 20 10    $ j=1
    10 10 10 10 10    $ j=2
c Total: 5 rows × 5 columns = 25 values ✓
```

## Related Documentation

- Fill validation procedure: `../validation_procedures.md` (Procedure 3)
- Troubleshooting: `../troubleshooting_guide.md` (Problem 2)
- Best practices: `../best_practices_detail.md` (Practice 2)
