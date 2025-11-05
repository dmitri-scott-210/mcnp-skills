# Example 03: Circular Universe Reference

## Problem Demonstrated

**Before file:** `03_circular_reference_before.i`

Circular universe dependency (infinite loop):
- Cell 100: `U=1 FILL=2` → Universe 1 fills universe 2
- Cell 200: `U=2 FILL=3` → Universe 2 fills universe 3
- Cell 300: `U=3 FILL=1` → Universe 3 fills universe 1
- **Cycle:** u=1 → u=2 → u=3 → u=1 → ... (infinite loop)

## MCNP Error Message

```
FATAL ERROR: Circular universe dependency detected
         u=1 fills u=2, u=2 fills u=3, u=3 fills u=1 (infinite loop)
```

## Diagnosis

Run validation:
```bash
python scripts/universe_tree_visualizer.py 03_circular_reference_before.i
```

Output:
```
======================================================================
Circular References Detected:
======================================================================
  1 → 2 → 3 → 1
```

Or use validation script:
```bash
python scripts/validate_cells_prerun.py 03_circular_reference_before.i
```

Output:
```
[4/5] Building universe dependency tree...
  ❌ FATAL: Circular universe references detected
     1 → 2 → 3 → 1
```

## Solution

**After file:** `03_circular_reference_after.i`

Broke the cycle by making universe 3 terminal:
- Cell 300: Changed from `U=3 FILL=1` to `U=3` with material
- Now has material (M1, fuel) instead of fill
- **Hierarchy:** u=1 → u=2 → u=3 (terminal, no further fill)

## Validation

```bash
python scripts/validate_cells_prerun.py 03_circular_reference_after.i
```

Should show:
```
[4/5] Building universe dependency tree...
  ✓ No circular references
    Maximum nesting depth: 3 levels
```

## Key Learning Points

1. **Hierarchy must be acyclic:** Universes form directed acyclic graph (DAG)
2. **Terminal universes needed:** At least one universe must not fill others
3. **Detection requires graph algorithms:** Manual inspection difficult for complex cases
4. **Validation essential:** Use automated tools to detect cycles

## Common Causes

1. **Copy-paste error:**
   ```
   100  0  -100  U=1  FILL=2  IMP:N=1
   200  0  -200  U=2  FILL=1  IMP:N=1  ← Pasted and flipped accidentally
   ```

2. **Misunderstanding bidirectional relationships:**
   - Thinking: "u=1 and u=2 reference each other"
   - Reality: Must be unidirectional (u=1 → u=2 OR u=2 → u=1, not both)

3. **Complex multi-level error:**
   - u=1 → u=2 → u=3 → ... → u=10 → u=1 (cycle buried deep)

## Related Documentation

- Universe dependency procedure: `../validation_procedures.md` (Procedure 4)
- Troubleshooting: `../troubleshooting_guide.md` (Problem 3)
- Universe concepts: `../cell_concepts_reference.md`
