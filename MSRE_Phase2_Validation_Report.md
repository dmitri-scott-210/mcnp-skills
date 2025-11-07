# MSRE Phase 2 Input Validation Report

**File:** `MSRE_Phase2.inp`
**Date:** 2025-11-07
**Validation Method:** 5-skill comprehensive cascade

---

## Executive Summary

**OVERALL STATUS:** ✓ SYNTAX VALID - ⚠ GEOMETRY VERIFICATION PENDING

The MSRE Phase 2 input file has passed all syntax, cross-reference, physics, and structural validations. However, **CRITICAL geometry verification steps (plotting + VOID test) must be completed before proceeding to MCNP execution.** These are not optional suggestions - they are requirements from the MCNP best practices checklist (Chapter 3.4).

---

## Validation Results by Skill

### 1. Input Validator ✓ PASSED

**Block Structure:**
- ✓ 3 blank lines correctly placed (lines 153, 221, 293)
- ✓ Cell block: Lines 1-152
- ✓ Surface block: Lines 154-220
- ✓ Data block: Lines 222-293

**Cross-References:**
- ✓ All 5 materials (M1-M5) defined and referenced
- ✓ All 40 surfaces defined and referenced
- ✓ No undefined references

**Format:**
- ✓ Zero tabs (all spaces)
- ✓ Proper continuation (5-space method)
- ✓ No inline comments on separate lines
- ✓ Compliant with MCNP format specifications

---

### 2. Cell Checker ✓ PASSED

**Universe System:**
- ✓ Universes defined: U=0, 1, 2, 3, 4, 10
- ✓ Universe references (FILL): FILL=10
- ✓ All FILL references resolved
- ✓ No circular dependencies
- ✓ Nesting depth: 2 levels (acceptable)

**Lattice Specification:**
- ✓ LAT=1 (cubic lattice) - VALID
- ✓ Lattice cell 100 is void (material 0) - CORRECT
- ✓ Proper lattice boundaries (-50 51 -52 53 -54 55)

**FILL Array:**
- Declaration: `FILL=-14:14 -14:14 0:0`
- Expected: (29) × (29) × (1) = 841 values
- Actual: 841 values
- ✓ **FILL array size CORRECT**

---

### 3. Geometry Checker ✓ STRUCTURE VALID / ⚠ VERIFICATION PENDING

**Surface Definitions:**
- ✓ All planes (PX, PY, PZ) properly defined
- ✓ All macrobodies (RCC) with 7 parameters
- ✓ Lattice boundaries complete

**Boolean Operators:**
- ✓ Cell 5: Uses complement operator (#1 #2 #3 #4)
- ✓ Cells 13, 25, 33: Proper intersection operators
- ✓ No circular dependencies

**Complexity:**
- Total cells: 32 (17 real world + 15 universe)
- Lattice elements: 841 positions (593 active)
- Nesting depth: 2 levels
- ✓ Within MCNP limits

**CRITICAL PENDING ACTIONS:**
1. ✗ **GEOMETRY PLOTTING** (Best Practice Item 1.2)
   - Command: `mcnp6 ip i=MSRE_Phase2.inp`
   - Views: XY at Z=85, XZ at Y=0, YZ at X=0
   - Check: Dashed lines = gaps/errors

2. ✗ **VOID TEST** (Best Practice Item 1.10)
   - Add VOID card to data block
   - Run: NPS 1000 (quick test)
   - Expected: VOID = 0.00000E+00
   - Non-zero = FATAL overlaps exist

---

### 4. Physics Validator ✓ PASSED

**MODE Card:**
- ✓ MODE N (neutron transport)
- ✓ Appropriate for criticality calculation

**KCODE Settings:**
- ✓ 10,000 histories/cycle (good for Phase 2)
- ✓ 50 inactive cycles
- ✓ 200 total cycles (150 active)
- ✓ KSRC at (0, 0, 85) - core center

**Cross-Section Libraries:**
- ✓ All ZAIDs use .80c (ENDF/B-VIII.0)
- ✓ Consistent library version
- ✓ Proper neutron suffix (.c)

**Thermal Scattering:**
- ✓ MT2 grph.87t (S(α,β) for graphite at 923 K)
- ⚠ Note: Closest available to 911 K (acceptable)

**Temperature:**
- ✓ TMP1: 7.8501E-08 MeV
- ✓ Conversion: 911 K × 8.617E-11 = 7.85E-08 MeV
- ✓ Applied to M1-M5

**Critical Parameters Verified:**
- ✓ Li-6 depletion: 0.005% (CRITICAL for reactivity)
- ✓ Boron in graphite: 0.8 ppm (CRITICAL for absorption)

---

### 5. Best Practices Checker ✓ 15/22 PHASE 1 ITEMS

**Phase 1 Setup (22 items):**

**Completed (15 items):**
- ✓ Geometry picture drawn
- ✓ Sufficient detail
- ✓ Simple cells/surfaces
- ✓ Minimal # operator
- ✓ Built incrementally
- ✓ Cross-sections verified
- ✓ No excessive VR
- ✓ PRINT card included
- ✓ Quality input

**CRITICAL Missing (2 items):**
- ✗ Geometry plotting (Item 1.2)
- ✗ VOID test (Item 1.10)

**Pending - Requires MCNP Run (5 items):**
- ⚠ Volume comparison
- ⚠ Source tables check
- ⚠ Warning review
- ⚠ Shannon entropy convergence
- ⚠ Keff behavior

**Phase 4 Criticality (5 items):**
- ✓ Large histories/cycle (10,000)
- ✓ Adequate active cycles (150)
- ⚠ Inactive cycles (verify after test run)
- ⚠ Keff behavior (verify after test run)
- ⚠ Convergence recheck (after production)

---

## Validation Summary

| Category | Status | Details |
|----------|--------|---------|
| **Syntax** | ✓ PASSED | 3 blocks, proper formatting |
| **Cross-References** | ✓ PASSED | All materials & surfaces defined |
| **Universe/Lattice** | ✓ PASSED | 841-value FILL array correct |
| **Physics** | ✓ PASSED | MODE N, KCODE, .80c libraries |
| **Geometry Structure** | ✓ PASSED | Valid Boolean operators |
| **Geometry Verification** | ⚠ PENDING | VOID test + plotting required |
| **Best Practices** | ⚠ 15/22 | 2 CRITICAL items pending |

---

## CRITICAL NEXT STEPS

**MANDATORY BEFORE Step 2.7 (MCNP Run):**

### Step 1: Geometry Plotting (30 min)

```bash
# Launch MCNP geometry plotter
mcnp6 ip i=MSRE_Phase2.inp

# In plotter, execute these commands:
plot origin=0 0 85 basis=xy extent=100 100   # Top view at mid-height
plot origin=0 0 85 basis=xz extent=100 200   # Side view (vertical)
plot origin=0 0 85 basis=yz extent=100 200   # Front view (vertical)

# CHECK FOR:
# - Dashed lines = GAPS (geometry error)
# - Color overlaps = OVERLAPS (fatal error)
# - Verify lattice pattern visible (29×29 grid)
# - Verify control rods at correct positions
```

**Expected:** Clean solid lines, no dashed lines, visible lattice structure

### Step 2: VOID Test (15 min)

Create `MSRE_Phase2_VOID_Test.inp`:
```
[Copy entire MSRE_Phase2.inp]
[Add before PRINT card:]
VOID
[Change KCODE to:]
KCODE  1000  1.0  10  10
```

Run test:
```bash
mcnp6 i=MSRE_Phase2_VOID_Test.inp o=void_test.out
grep -i void void_test.out
```

**Expected Output:**
```
void     0.00000E+00
```

**If VOID ≠ 0:** OVERLAPS EXIST (FATAL - must fix before production)

---

## Recommendations

1. **DO NOT SKIP** geometry plotting and VOID test
   - These catch 90% of errors before expensive runs
   - Non-negotiable per MCNP Chapter 3.4

2. **After VOID test passes:**
   - Proceed to Step 2.7 (Initial MCNP Run)
   - Use modest NPS first (KCODE 1000 1.0 25 50)
   - Review ALL warnings in output

3. **Volume Verification (after first run):**
   - Compare VOL card values to MCNP calculated volumes
   - >5% difference indicates geometry error

4. **Shannon Entropy Plot (after test run):**
   - Verify source converged in inactive cycles
   - Should be flat in final 30% of inactive cycles

---

## Files Generated

- `MSRE_Phase2.inp` - Main validated input (293 lines)
- `MSRE_Phase2_Validation_Report.md` - This document

## Next File to Create

- `MSRE_Phase2_VOID_Test.inp` - Geometry overlap test
- `MSRE_Phase2_Plotting_Instructions.txt` - Detailed plotting guide

---

**END OF VALIDATION REPORT**

**Status:** Ready for geometry verification (plotting + VOID test)
**Next Step:** Create VOID test input and plotting instructions
