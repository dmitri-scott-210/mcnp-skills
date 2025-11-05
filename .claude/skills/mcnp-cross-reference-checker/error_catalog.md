# MCNP Cross-Reference Errors - Complete Catalog

**Version:** 2.0.0
**Skill:** mcnp-cross-reference-checker
**Purpose:** Comprehensive catalog of cross-reference errors, causes, fixes, and prevention

---

## Error Classification

**Severity Levels:**
- **FATAL:** MCNP terminates with error message
- **WARNING:** MCNP issues warning but may continue
- **INFO:** Potential issues flagged by checker

**Error Categories:**
1. Undefined Entity References
2. Count Mismatches
3. Invalid Reference Values
4. Circular Dependencies
5. Unused Entities
6. Cascading Errors

---

## ERROR 1: Undefined Surface Reference

### Error Message
```
fatal error.  surface     203 in cell       10 is not defined.
```

### Cause
Cell geometry expression references a surface number that doesn't exist in the Surface Cards block.

### Example
```
c Cell Cards
10 1 -2.7  -1 2 -203 4    ← References surface 203
15 2 -8.0  1 -5

c Surface Cards
1 PZ 0
2 PZ 10
4 CZ 5
5 CZ 8
c Surface 203 is MISSING!
```

### Diagnosis
1. Locate cell with error (cell 10 in example)
2. Extract geometry expression: `-1 2 -203 4`
3. Parse for surface numbers: 1, 2, 203, 4
4. Check Surface Cards block
5. Identify missing: 203

### Fix Options

**Option A: Add missing surface**
```
c Add surface 203 definition
203 PZ 20.5    ← Add appropriate surface type and parameters
```

**Option B: Correct geometry (if typo)**
```
c Was 203 a typo? Check if meant:
- Surface 103 (transposed digits)
- Surface 201, 230 (nearby numbers)
- Surface 3 (extra digit)

c If meant surface 3:
10 1 -2.7  -1 2 -3 4    ← Changed 203 to 3
```

**Option C: Remove reference (if not needed)**
```
c If surface 203 constraint not actually needed:
10 1 -2.7  -1 2 4    ← Removed -203 entirely
```

### Prevention
- Use cross-reference checker before running MCNP
- Maintain surface numbering scheme
- Document surface numbers in comments
- Use sequential numbering (1, 2, 3...) to avoid gaps

---

## ERROR 2: Undefined Material Reference

### Error Message
```
material         5 for cell       15 is not defined.
```

### Cause
Cell specifies material number but corresponding M card doesn't exist.

### Example
```
c Cell Cards
10 1 -2.7  -1 2 -3
15 5 -8.0  3 -4 5    ← Uses material 5
20 0  4 -6

c Data Cards
MODE N
M1  1001.80c  2  8016.80c  1    ← Material 1 defined
MT1 H-H2O.40t
c Material 5 is MISSING!
```

### Diagnosis
1. Locate cell with error (cell 15)
2. Extract material number: 5
3. Search Data Cards for M5
4. Confirm missing

### Fix Options

**Option A: Add material definition**
```
c Add material 5 (example: stainless steel)
M5  26000.80c  0.70    ← Iron
    24000.80c  0.18    ← Chromium
    28000.80c  0.12    ← Nickel
```

**Option B: Change to correct material**
```
c If meant to use existing material 1:
15 1 -8.0  3 -4 5    ← Changed material 5 to 1
```

**Option C: Change to void**
```
c If should be void:
15 0  3 -4 5    ← Changed to void (m=0)
```

### Prevention
- Define all materials before assigning to cells
- Use material library templates
- Document material numbering scheme
- Cross-check material assignments

---

## ERROR 3: Importance Count Mismatch

### Error Message
```
too many entries on imp:n card.  15 cells.  16 entries.
```

OR

```
warning.  only     4 imp:n entries provided for    15 cells.
         remaining entries assumed to be  0.00000E+00
```

### Cause
Number of IMP card entries doesn't match number of cells.

### Example
```
c Cell Cards (5 cells total)
1 1 -2.7  -1
2 1 -2.7  1 -2
3 0      2 -3
4 2 -8.0  3 -4
5 0      4

c Data Cards
MODE N
IMP:N 1 1 1 0    ← Only 4 entries for 5 cells! WRONG
```

### Diagnosis
1. Count cells in Cell Cards block: 5
2. Parse IMP:N entries: 1 1 1 0 = 4 entries
3. Compare: 4 ≠ 5 → MISMATCH

### Fix
```
c Add one more entry (for cell 5)
IMP:N 1 1 1 0 0    ← Now 5 entries for 5 cells ✓
```

### Special Cases

**Too many entries (FATAL):**
```
IMP:N 1 1 1 0 0 0    ← 6 entries for 5 cells = FATAL ERROR
```

**Too few entries (WARNING):**
```
IMP:N 1 1    ← 2 entries for 5 cells = WARNING
                Cells 3,4,5 assumed importance 0 (killed)
```

### Prevention
- Count cells before writing IMP card
- Use formula: `IMP entries = cell count`
- Verify after adding/deleting cells
- Automated checking with scripts

---

## ERROR 4: Tally References Undefined Cell

### Error Message
```
warning.  cell        25 in f4 tally        4 is not defined.
         tally will be made on any neutron collision in cell   25
```

### Cause
Tally card references cell number that doesn't exist.

### Example
```
c Cell Cards
10 1 -2.7  -1 2
15 2 -8.0  2 -3
20 0  3

c Data Cards
F4:N 10 15 25    ← References cells 10, 15, 25
                    But cell 25 doesn't exist!
```

### Diagnosis
1. Parse F4 tally cells: 10, 15, 25
2. Check if each cell exists
3. Identify missing: 25

### Fix Options

**Option A: Remove undefined cell from tally**
```
F4:N 10 15    ← Removed cell 25
```

**Option B: Add missing cell**
```
c Add cell 25 if it should exist:
25 3 -7.0  3 -4 5
```

**Option C: Correct to intended cell**
```
c If meant cell 20:
F4:N 10 15 20    ← Changed 25 to 20
```

### Prevention
- Update tallies when modifying cells
- Use cell naming scheme
- Document tally-cell relationships
- Automated dependency tracking

---

## ERROR 5: Transformation Not Defined

### Error Message
```
fatal error.  trcl card        8 specified on cell       50 not found.
```

### Cause
Cell TRCL parameter references transformation number not defined.

### Example
```
c Cell Cards
50 2 -7.8  -100 101 -102  TRCL=8    ← References TR8

c Data Cards
MODE N
TR5 0 0 0 ...    ← TR5 defined
TR10 1 1 1 ...   ← TR10 defined
c TR8 is MISSING!
```

### Diagnosis
1. Locate cell with TRCL: cell 50
2. Extract transformation number: 8
3. Search for TR8 card
4. Confirm missing

### Fix Options

**Option A: Add transformation**
```
TR8 1.0 2.0 3.0  0 0 0 ...    ← Add TR8 definition
```

**Option B: Use existing transformation**
```
c If meant TR5:
50 2 -7.8  -100 101 -102  TRCL=5    ← Changed to TR5
```

**Option C: Remove transformation**
```
c If transformation not needed:
50 2 -7.8  -100 101 -102    ← Removed TRCL parameter
```

### Prevention
- Define transformations before using
- Sequential numbering (TR1, TR2, TR3...)
- Document transformation purposes
- Template files with common transformations

---

## ERROR 6: Universe Fill References Undefined Universe

### Error Message
```
fatal error.  universe       10 referenced on fill card not defined.
```

### Cause
Cell FILL parameter references universe number that doesn't exist.

### Example
```
c Cell Cards
20 0  -10 11 -12  FILL=10    ← References universe 10

c But no cells with U=10!
30 1 -2.7  -1 2  U=5    ← Only universe 5 defined
```

### Diagnosis
1. Parse FILL parameter: universe 10
2. Search for cells with U=10
3. Confirm no cells define universe 10

### Fix Options

**Option A: Define universe**
```
c Add cells in universe 10:
40 2 -8.0  -5 6  U=10    ← Define universe 10
```

**Option B: Correct FILL reference**
```
c If meant universe 5:
20 0  -10 11 -12  FILL=5    ← Changed to universe 5
```

### Prevention
- Define universes before filling
- Universe numbering scheme
- Document universe hierarchy
- Visual universe tree diagrams

---

## ERROR 7: FM Card References Undefined Material

### Error Message
```
warning.  material        3 on fm card        4 is not defined.
```

### Cause
FM tally multiplier references material number that doesn't exist.

### Example
```
c Tally
F4:N 10 20 30

c Multiplier
FM4 1.0  3 -6    ← References material 3

c Materials
M1 1001.80c 2  8016.80c 1
M2 6000.80c 1
c Material 3 is MISSING!
```

### Diagnosis
1. Parse FM4 material references: 3
2. Check for M3 card
3. Confirm missing

### Fix Options

**Option A: Add material**
```
M3 92235.80c 1    ← Add material 3 definition
```

**Option B: Change FM reference**
```
c If meant material 2:
FM4 1.0  2 -6    ← Changed to material 2
```

**Option C: Use cell material**
```
c Use tally cell's material:
FM4 1.0  -1 -6    ← -1 means "cell material"
```

### Prevention
- Define materials before FM cards
- Document FM card material dependencies
- Match material numbers across input

---

## ERROR 8: Circular Universe Dependencies

### Error Message
```
bad trouble in subroutine chkcel of imcn
   universe       5 contains itself.
```

### Cause
Universe hierarchy creates circular reference (universe fills itself directly or indirectly).

### Example - Direct Circular
```
c Cell in universe 5 fills itself:
10 0  -1 2  U=5  FILL=5    ← U=5 fills U=5 = CIRCULAR!
```

### Example - Indirect Circular
```
c Universe 5 fills universe 10
c Universe 10 fills universe 5

20 0  -10 11  U=5  FILL=10    ← U=5 → U=10
30 0  -20 21  U=10 FILL=5     ← U=10 → U=5 = CIRCULAR!
```

### Diagnosis
1. Build universe dependency graph
2. Traverse hierarchy
3. Detect cycles in graph

### Fix
```
c Break circular dependency:
c Universe 5 should fill universe 10
c Universe 10 should fill universe 15 (not 5)

20 0  -10 11  U=5  FILL=10    ← U=5 → U=10
30 0  -20 21  U=10 FILL=15    ← U=10 → U=15 (new leaf universe)

c Define universe 15:
40 1 -2.7  -1 2  U=15
```

### Prevention
- Draw universe hierarchy diagram
- Unidirectional fills (parent → child, never child → parent)
- Automated cycle detection
- Hierarchical numbering (U=1, U=10, U=100 for levels)

---

## Cascading Errors

### Concept
One broken reference can cause multiple error messages. **Always fix the FIRST error first.**

### Example Cascade
```
Primary Error:
  Cell 10 references undefined surface 203

Cascading Errors:
  IMP card count wrong (if cell 10 deleted to "fix")
  Tally F4 references cell 10 (now deleted)
  FM4 references material from cell 10 (now deleted)
```

### Fix Strategy
1. Read ALL error messages
2. Identify PRIMARY error (first in file order)
3. Fix primary error
4. Re-run validation
5. Check if cascading errors resolved
6. Repeat until clean

---

## Unused Entity Detection

### Unused Surface

**Detection:**
```
Surface 99 defined but never referenced in any cell geometry
```

**Causes:**
- Leftover from deleted cells
- Copy-paste from other input
- Incomplete geometry construction
- Typo in cell geometry (referenced wrong number)

**Action:**
- Review if surface should be used
- Remove if truly not needed
- May indicate incomplete work

### Unused Material

**Detection:**
```
Material 4 defined but no cells use material 4
```

**Causes:**
- Changed cell materials to different number
- Copied from template/other input
- Prepared material but didn't assign

**Action:**
- Verify not needed
- Remove to reduce clutter
- Check for copy-paste errors

---

## Troubleshooting Flowchart

```
MCNP Error Encountered
      ↓
Is it cross-reference related?
  ├─→ Yes → Continue
  └─→ No → Use mcnp-fatal-error-debugger skill
      ↓
Run cross-reference checker
      ↓
Broken references found?
  ├─→ Yes → Fix broken references first
  └─→ No → Continue to unused entities
      ↓
Fix broken references
      ↓
Re-run checker
      ↓
Count mismatches found?
  ├─→ Yes → Fix IMP/VOL/AREA counts
  └─→ No → Continue
      ↓
Unused entities found?
  ├─→ Yes (warning only) → Review and optionally remove
  └─→ No → All references valid
      ↓
Proceed to geometry-checker
```

---

## Error Prevention Best Practices

1. **Use sequential numbering** - Easier to track what's defined
2. **Document reference relationships** - Comments in input
3. **Validate after every modification** - Catch errors early
4. **Use templates** - Pre-validated structures
5. **Automated checking** - Run scripts before MCNP
6. **Version control** - Roll back if references break
7. **Reference maps** - Visual diagrams of dependencies
8. **Consistent naming** - Systematic numbering schemes
9. **Comments** - Explain what each entity references
10. **Test incrementally** - Add entities one at a time

---

**END OF ERROR_CATALOG.MD**
