# Example 01: Undefined Universe References

## Problem Demonstrated

**Before file:** `01_universe_errors_before.i`

Shows a common error where a fill array references a universe that is not defined:
- Cell 100 has a 3×3×1 lattice fill array
- Array contains universe IDs: 10, 10, 10, 10, **50**, 10, 10, 10, 10
- Universe 10 is defined (cell 1000)
- **Universe 50 is NOT defined** → MCNP fatal error

## MCNP Error Message

```
FATAL ERROR: Universe 50 not found
         Cell 100 references fill=50 but no cell has u=50
```

## Diagnosis

Run validation:
```bash
python scripts/validate_cells_prerun.py 01_universe_errors_before.i
```

Output will show:
```
[1/5] Checking universe references...
  ❌ FATAL: Undefined universe references
     Universe 50 referenced in FILL but not defined
```

## Solution

**After file:** `01_universe_errors_after.i`

Added definition for universe 50:
- Cell 1500: Control rod fuel pin with `U=50`
- Surface 1500: Control rod radius
- Material M2: Different enrichment for control rod

## Validation

```bash
python scripts/validate_cells_prerun.py 01_universe_errors_after.i
```

Should show:
```
[1/5] Checking universe references...
  ✓ All 2 universe references valid
    2 universes defined
```

## Key Learning Points

1. **Every fill= must have u=:** All universe IDs in fill arrays must be defined
2. **Array validation:** Check every value in large fill arrays
3. **Early detection:** Use validation scripts before running MCNP
4. **Common cause:** Copy-paste errors or typos (50 instead of 5)

## Related Documentation

- Universe validation procedure: `../validation_procedures.md` (Procedure 1)
- Troubleshooting: `../troubleshooting_guide.md` (Problem 1)
- Universe concepts: `../cell_concepts_reference.md`
