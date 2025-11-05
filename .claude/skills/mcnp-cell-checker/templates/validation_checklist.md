# MCNP Cell Card Validation Checklist

Use this checklist before every MCNP run to ensure cell cards are properly configured.

## Input File Information

- **File name:** `_______________________`
- **Date:** `_______________________`
- **Author:** `_______________________`
- **Description:** `_______________________`

---

## Pre-Validation Checks

### Step 1: Universe References

- [ ] All `fill=` references have corresponding `u=` definitions
- [ ] No universe 0 explicitly defined (`u=0` or `fill=0`)
- [ ] Universe numbers are unique (no duplicate `u=` definitions)
- [ ] Unused universes identified (warning only)

**Command:**
```bash
python scripts/validate_cells_prerun.py input.inp
# Check "[1/5] Checking universe references..."
```

**Results:**
- Defined universes: `_______`
- Used universes: `_______`
- Undefined references: `_______`
- Status: ☐ PASS ☐ FAIL

---

### Step 2: Lattice Specifications

- [ ] All `lat=` values are either 1 or 2 (no other values)
- [ ] All lattice cells have `fill=` parameter
- [ ] All lattice cells are void (material 0)
- [ ] LAT=1 cells have appropriate surfaces (6 minimum)
- [ ] LAT=2 cells have appropriate surfaces (8 minimum)

**Command:**
```bash
python scripts/validate_cells_prerun.py input.inp
# Check "[2/5] Validating lattice specifications..."
```

**Results:**
- Lattice cells found: `_______`
- LAT=1 (cubic): `_______`
- LAT=2 (hexagonal): `_______`
- Errors: `_______`
- Status: ☐ PASS ☐ FAIL

---

### Step 3: Fill Array Dimensions

- [ ] All fill array sizes match lattice declarations
- [ ] Array dimensions calculated correctly: (i2-i1+1) × (j2-j1+1) × (k2-k1+1)
- [ ] All universe IDs in arrays are defined
- [ ] No non-integer values in arrays

**Command:**
```bash
python scripts/fill_array_validator.py input.inp
```

**Results:**
- Fill arrays found: `_______`
- All dimensions correct: ☐ YES ☐ NO
- Mismatches: `_______`
- Status: ☐ PASS ☐ FAIL

---

### Step 4: Universe Dependency Tree

- [ ] No circular universe references
- [ ] All universes reachable from real world (u=0)
- [ ] Nesting depth is acceptable (<10 levels recommended)
- [ ] No orphaned universes (unreachable from real world)

**Command:**
```bash
python scripts/universe_tree_visualizer.py input.inp -o tree.txt
```

**Results:**
- Maximum nesting depth: `_______` levels
- Circular references: ☐ NONE ☐ DETECTED
- Unreachable universes: `_______`
- Status: ☐ PASS ☐ FAIL

---

### Step 5: Lattice Boundary Surfaces

- [ ] LAT=1 cells use RPP macrobody or 6 planes
- [ ] LAT=2 cells use RHP macrobody or 8 planes (6 P + 2 PZ)
- [ ] Boundary surfaces are appropriate for lattice type

**Command:**
```bash
python scripts/validate_cells_prerun.py input.inp
# Check "[5/5] Checking lattice boundary surfaces..."
```

**Results:**
- Standard boundaries: `_______`
- Non-standard boundaries: `_______`
- Recommendations: `_______`
- Status: ☐ PASS ☐ FAIL

---

## Overall Validation Status

### Summary

- [ ] **Step 1: Universe references** - PASS
- [ ] **Step 2: Lattice specifications** - PASS
- [ ] **Step 3: Fill array dimensions** - PASS
- [ ] **Step 4: Universe dependency tree** - PASS
- [ ] **Step 5: Lattice boundaries** - PASS

### Final Checklist

- [ ] All validation steps passed
- [ ] No fatal errors detected
- [ ] Warnings reviewed and addressed (or accepted)
- [ ] Input file backed up before MCNP run
- [ ] Ready for MCNP execution

### MCNP Execution Command

```bash
mcnp6 i=input.inp o=output.txt
```

---

## Performance Considerations

### Nesting Depth Analysis

- **Depth:** `_______` levels
- **Status:**
  - ☐ 1-3 levels: Optimal (no optimization needed)
  - ☐ 4-7 levels: Acceptable (consider negative universe optimization)
  - ☐ 8-10 levels: Caution (apply negative universe optimization)
  - ☐ >10 levels: Action required (simplify geometry)

### Optimization Applied

- [ ] Negative universe numbers used for levels 3+ (`u=-N`)
- [ ] Universe hierarchy documented in input file
- [ ] Performance tested with reduced particle count

---

## Documentation

### Universe Reference Map

Document universe hierarchy:

```
u=0 (real world):
  → fills: [list universes]

u=N:
  → Purpose: [description]
  → Cells: [count]
  → Fills: [list]
  → Level: [number]
```

### Fill Array Documentation

For each lattice cell, document:

```
Cell [number]: [description]
  Declaration: fill= i1:i2 j1:j2 k1:k2
  Dimensions: i_size × j_size × k_size = total
  Universe legend:
    [universe_id] = [description] ([count] occurrences)
```

---

## Sign-Off

- **Validation performed by:** `_______________________`
- **Date:** `_______________________`
- **Time:** `_______________________`
- **Status:** ☐ APPROVED FOR MCNP RUN ☐ REVISIONS NEEDED

### Notes

```
[Add any additional notes, warnings, or observations here]
```

---

**END OF VALIDATION CHECKLIST**
