# MSRE Lattice Position CORRECTION

## Issue Identified

**Previous (INCORRECT) assumption:**
- Center (0,0): Sample basket or control rod
- Adjacent positions: Control rods

**Corrected configuration (USER PROVIDED):**
- Center (0,0): **NORMAL GRAPHITE STRINGER**
- Diagonal square positions: 3 control rods + 1 sample basket

---

## Corrected Central Pattern

### Lattice Indices

```
        j
        ↑
   +1   ·  ·  X  ·  X  ·  ·
        ·  ·  ·  ·  ·  ·  ·
    0   ·  X  ·  G  ·  X  ·  → i
        ·  ·  ·  ·  ·  ·  ·
   -1   ·  ·  X  ·  X  ·  ·

       -1  0  1
```

Where:
- **G** at (0,0): Graphite stringer (Universe 1)
- **X** at diagonal corners: Special positions
  - (-1,-1,0): Control rod OR sample basket
  - (-1,+1,0): Control rod OR sample basket
  - (+1,-1,0): Control rod OR sample basket
  - (+1,+1,0): Control rod OR sample basket

**Total special positions:** 4 (3 control rods + 1 sample basket)

---

## Diagonal Square Geometry

**Spacing between special positions:**
- Horizontal spacing: 2 lattice pitches = 2 × 5.084 = 10.168 cm
- Vertical spacing: 2 lattice pitches = 10.168 cm
- Diagonal (corner to corner): 10.168 × √2 = 14.38 cm

**Distance from center (0,0) to each diagonal position:**
- Distance = √[(±1)² + (±1)²] × pitch = √2 × 5.084 = 7.19 cm

This makes physical sense:
- Central stringer remains for structural support
- 4 special channels form symmetric square around center
- All 4 positions equidistant from center (7.19 cm)

---

## Universe Assignment (AWAITING USER INPUT)

### CONFIRMED Assignment (User Provided)

**Diagonal positions:**
- **(-1,+1)**: Control Rod 1 (withdrawn) - Universe 2
- **(+1,+1)**: Control Rod 2 (withdrawn) - Universe 2
- **(+1,-1)**: Sample Basket - Universe 4 ✓ **USER CONFIRMED**
- **(-1,-1)**: Regulating Rod (3% inserted) - Universe 3

**Pattern:**
```
        j
        ↑
   +1   Rod1(U2)    Rod2(U2)

    0      Graphite(U1) at center

   -1   RegRod(U3)  Basket(U4) ✓

       -1          +1  → i
```

### Option 2: Alternative (Needs Confirmation)

Any specific arrangement based on:
- ORNL-TM-728 Figure 3 (control rod layout)
- IRPhEP benchmark Figure 8
- Operational access requirements
- Thermal/neutronic symmetry

---

## Updated FILL Array Pattern

**Corrected center region (29×29 array, i,j = -14:14):**

```
FILL=-14:14 -14:14 0:0
    ...
    0 0 1 1 1 1 U 1 U 1 1 1 1 0 0  $ j=+1 (U at i=-1,+1 and i=+1,+1)
    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0  $ j=+0 (center row, all graphite)
    0 0 1 1 1 1 U 1 U 1 1 1 1 0 0  $ j=-1 (U at i=-1,-1 and i=+1,-1)
    ...
```

Where `U` = Universe number (2, 3, or 4) based on assignment above.

---

## Impact on Previous Planning

### Files Requiring Update:

1. **MSRE_Lattice_Structure_Plan.md** - Section 3.3 (central disruption)
2. **MSRE_FILL_Array.txt** - Rows j=-1, j=0, j=+1
3. **scripts/msre_lattice_analyzer.py** - Special position logic
4. **MSRE_Lattice_Planning_Summary.md** - Central pattern description

### Validation Impact:

- **Total stringers:** UNCHANGED (589 graphite stringers)
  - Previously counted 4 special positions
  - Now: Center is graphite, 4 diagonal are special
  - Net: Same number of graphite stringers ✓

- **Total special positions:** UNCHANGED (4)
  - Just repositioned from (0,0)+(adjacent) to (diagonal square)

- **Lattice statistics:** ✓ VALID (no recalculation needed)

---

## Action Required

**User input needed for universe assignment:**

Which diagonal position should be assigned to:
1. Control Rod 1 (withdrawn, Universe 2): **(-1,+1)?** **(-1,-1)?** **(+1,+1)?** **(+1,-1)?**
2. Control Rod 2 (withdrawn, Universe 2): **?**
3. Regulating Rod (3% inserted, Universe 3): **?**
4. Sample Basket (Universe 4): **?**

**OR:**

Use proposed symmetric arrangement (Option 1 above) and document as assumption?

---

## Corrected Geometry Notes

### RCC Positioning for Special Channels

Each special position needs RCC surface centered at lattice coordinates:

**For (-1,-1,0):**
- x = -1 × 5.084 = -5.084 cm
- y = -1 × 5.084 = -5.084 cm
- z = 0 (bottom of lattice)
- RCC: `0 -5.084 -5.084 0  0 0 170.311  R`

**For (-1,+1,0):**
- x = -5.084 cm
- y = +5.084 cm
- RCC: `0 -5.084 +5.084 0  0 0 170.311  R`

**For (+1,-1,0):**
- x = +5.084 cm
- y = -5.084 cm
- RCC: `0 +5.084 -5.084 0  0 0 170.311  R`

**For (+1,+1,0):**
- x = +5.084 cm
- y = +5.084 cm
- RCC: `0 +5.084 +5.084 0  0 0 170.311  R`

Where R = 2.71435 cm (for sample basket OD=5.4287 cm) or 2.54 cm (for control rod thimble OD=5.08 cm)

---

## Status

**Correction Status:** ✓ ACKNOWLEDGED

**Implementation Status:** ⏳ AWAITING UNIVERSE ASSIGNMENT

**Ready to proceed:** After universe assignment confirmed

**Updated files to commit:** MSRE_Lattice_Position_CORRECTION.md (this file)

---

**Date:** 2025-11-07
**Corrected by:** User input
**Impact:** Geometry only (statistics unchanged)
