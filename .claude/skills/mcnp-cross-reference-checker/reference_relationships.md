# MCNP Cross-Reference Relationships - Complete Specification

**Version:** 2.0.0
**Skill:** mcnp-cross-reference-checker
**Purpose:** Detailed technical specifications for all cross-reference types in MCNP inputs

---

## Overview

MCNP input files contain numerous cross-references where cards reference entities defined elsewhere. This document provides complete specifications for identifying, parsing, and validating all reference relationship types.

**Reference Categories:**
1. Cell → Surface (geometry expressions)
2. Cell → Material (M card numbers)
3. Cell → Transformation (TRCL parameter)
4. Cell → Universe (U and FILL parameters)
5. Tally → Cell/Surface (F card specifications)
6. FM Card → Material (tally multipliers)
7. Importance → Cell Count (parameter card matching)
8. Data Cards → Entity Counts (general validation)

---

## 1. Cell → Surface References

**Source:** Chapter 5.2 (Cell Cards)
**Format:** `j m d geom params`

### Geometry Expression Syntax

**Basic operators:**
- **Intersection (space):** `1 2 3` = inside surfaces 1 AND 2 AND 3
- **Union (colon):** `1:2:3` = inside surface 1 OR 2 OR 3
- **Complement (hash):** `#5` = NOT in cell 5
- **Parentheses:** `(1 2):(3 4)` = grouping

**Sense notation:**
- **Positive:** `5` = positive sense of surface 5
- **Negative:** `-5` = negative sense of surface 5

### Example References

```
Cell Definition:
10 1 -2.7  -1 2 -3 (4:5:6) #8

References extracted:
- Surface 1 (negative sense)
- Surface 2 (positive sense)
- Surface 3 (negative sense)
- Surface 4 (positive sense in union)
- Surface 5 (positive sense in union)
- Surface 6 (positive sense in union)
- Cell 8 (complement operator)
```

### Parsing Algorithm

```
1. Extract geometry expression (everything after density)
2. Remove cell parameters (IMP, VOL, TRCL, etc.)
3. Parse expression:
   a. Split by operators (space, :, #, parentheses)
   b. Extract all numeric values
   c. Remove sign (-, +) to get entity number
   d. Classify as surface or cell based on context
4. For each surface number:
   a. Check if defined in Surface Cards block
   b. Record reference: cell_num → surface_num
```

### Special Cases

**Macrobodies:**
```
*10 1 -2.7  -1 2 -3
         ↑
   Asterisk indicates macrobody facets will be auto-generated
   References: surfaces 1, 2, 3 (macrobody surfaces)
```

**Repeated structures:**
```
10 0  -1 2 -3  U=5  FILL=10
               ↓         ↓
         References:     References:
         surfaces 1,2,3  universe 10
```

### Validation Rules

**FATAL if:**
- Any referenced surface number not defined in Surface Cards block
- Surface number outside valid range (1 to 99,999,999)

**WARNING if:**
- Surface defined but never referenced (unused surface)

---

## 2. Cell → Material References

**Source:** Chapter 5.2 (Cell Cards), Chapter 5.6 (Material Cards)
**Format:** `j m d geom params`

### Material Number Field (m)

**Syntax:**
- `m = 0`: Void (no material needed)
- `m > 0`: Material number (must have corresponding M card)
- `m` range: 1 to 99,999,999

### Example References

```
Cell Card:
15 5 -8.0  -10 11 -12
   ↓
   Material 5 must be defined

Required:
M5  26000.80c  0.70   ← Iron-56
    24000.80c  0.18   ← Chromium
    28000.80c  0.12   ← Nickel
```

### Special Cases

**Void cells:**
```
20 0  10 -11 12
   ↓
   m=0, no material needed (no M card required)
```

**Material in universe:**
```
c Universe 5
30 3 -7.8  -5 6 -7  U=5
   ↓
   Material 3 must exist in base universe (universe 0)
```

### Validation Rules

**FATAL if:**
- `m > 0` but no corresponding M card exists
- Material number outside valid range

**OK if:**
- `m = 0` (void, no material needed)

**WARNING if:**
- Material defined (M card exists) but never used in any cell

---

## 3. Cell → Transformation References

**Source:** Chapter 5.5 (TR Cards), Chapter 5.2 (TRCL Parameter)
**Format:** `TRCL=n` or `*TRCL=n`

### TRCL Syntax

**Basic form:**
```
10 1 -2.7  -1 2 -3  TRCL=5
                         ↓
                    References TR5

Required:
TR5  1.0 2.0 3.0  0 0 0 ...
```

**Degree specification:**
```
10 1 -2.7  -1 2 -3  *TRCL=5
                    ↑
            Asterisk: transformation matrix in degrees (not cosines)
```

### Transformation Number Ranges

**Cell transformations:**
- Range: 1 to 99,999,999
- Unlimited number of transformations

**Surface transformations:**
- Range: 1 to 999
- Max 999 transformations total

### Validation Rules

**FATAL if:**
- TRCL references transformation number not defined (no TR card)
- Transformation number outside valid range

**WARNING if:**
- TR card defined but never referenced

---

## 4. Universe and Fill References

**Source:** Chapter 5.5 (U, LAT, FILL Parameters)

### Universe System

**Universe definition (U parameter):**
```
c Define universe 5
10 1 -2.7  -1 2 -3  U=5
                    ↓
            Creates universe 5 containing this cell
```

**Universe filling (FILL parameter):**
```
c Fill cell with universe 5
20 0  -10 11 -12  FILL=5
                       ↓
              References universe 5 (must exist)
```

### Simple Fill References

```
Cell Definition:
30 0  -15 16 -17 18  FILL=10

Validation:
1. Check if universe 10 exists (cells with U=10)
2. Verify universe 10 is not circular (doesn't fill itself)
3. Confirm universe hierarchy is valid
```

### Lattice Fill References

**Hexagonal lattice example:**
```
c Lattice fill cell
40 0  -20 21 -22  LAT=2  FILL=-2:2 -3:3 0:0
                                    5 5 5 10 10
                                    5 5 10 10 10
                                    5 10 10 10 15
                                    10 10 10 15 15
                                    10 10 15 15 15

References:
- Universe 5 (appears multiple times)
- Universe 10 (appears multiple times)
- Universe 15 (appears multiple times)

Validation:
- All universes 5, 10, 15 must exist
- Array dimensions must match LAT specification
```

### Validation Rules

**FATAL if:**
- FILL references undefined universe
- Circular universe dependencies detected
- Lattice array count mismatch (wrong number of universe IDs)

**WARNING if:**
- Universe defined but never used (never filled anywhere)

---

## 5. Tally → Cell/Surface References

**Source:** Chapter 5.9 (Tally Specification Cards)

### Tally Type Dependencies

**Surface tallies (reference surfaces):**
```
F1:N  10 20 30      ← Surface current on surfaces 10, 20, 30
F2:P  5 10 15       ← Surface flux on surfaces 5, 10, 15

Validation: Verify surfaces 10, 20, 30, 5, 15 exist
```

**Cell tallies (reference cells):**
```
F4:N  2 4 6 8       ← Cell flux in cells 2, 4, 6, 8
F6:N  10            ← Energy deposition in cell 10
F7:N  2 5 8         ← Fission energy in cells 2, 5, 8

Validation: Verify cells 2, 4, 6, 8, 10, 5 exist
```

**Point detectors (no references):**
```
F5:P  0 0 0 0.1     ← Point at (0,0,0), radius 0.1
F15:N 10 5 8 0.05   ← Point at (10,5,8), radius 0.05

Validation: None needed (coordinates, not references)
```

### Tally Reference Table

| Tally Type | References | Entity Type | Required Cards |
|------------|------------|-------------|----------------|
| F1, F2     | Surfaces   | Surface IDs | Surface cards  |
| F4         | Cells      | Cell IDs    | Cell cards     |
| F5         | None       | Coordinates | None           |
| F6, F7     | Cells      | Cell IDs    | Cell cards     |
| F8         | Cells      | Cell IDs    | Cell cards     |
| FMESH      | None       | Mesh coords | None           |

### Validation Rules

**FATAL if:**
- F1/F2 references undefined surface
- F4/F6/F7/F8 references undefined cell

**WARNING if:**
- Tally references deleted cell/surface (stale reference after modification)

---

## 6. FM Card → Material References

**Source:** Chapter 5.9.10 (FM Tally Multiplier Card)

### FM Card Format

```
FM<tally_num>  c  m1 r1  m2 r2  m3 r3  ...

where:
  c = normalization constant
  m = material number (-1 for cell material)
  r = reaction MT number
```

### Example References

```
Tally:
F4:N 10 20 30

Multiplier:
FM4  1.0  5 -6  2 -2
          ↓     ↓
     Material 5  Material 2
     (must exist) (must exist)

Validation:
- M5 card must be defined
- M2 card must be defined
```

### Special Material Reference

```
FM14  1.0  -1 -6
           ↓
   Special: -1 means "use cell's material"
   No validation needed (cell already validated)
```

### Validation Rules

**FATAL if:**
- `m > 0` and material m not defined (no M card)
- Material number outside valid range

**OK if:**
- `m = -1` (uses tally cell's material)

---

## 7. Importance Card → Cell Count Matching

**Source:** Chapter 3.2.5.2 (Cell and Surface Parameter Cards)

### Critical Counting Rule

**Number of IMP entries MUST equal number of cells (FATAL if mismatch)**

### Example Validation

```
c Cell Cards (5 cells)
1 1 -2.7  -1
2 1 -2.7  1 -2
3 0      2 -3
4 2 -8.0  3 -4
5 0      4

c Must have EXACTLY 5 entries
IMP:N 1 1 1 1 0    ← CORRECT (5 entries for 5 cells)

IMP:N 1 1 1        ← WRONG (only 3 entries)
                      Error: "IMP:N has 3 entries, 5 cells exist"

IMP:N 1 1 1 1 0 0  ← WRONG (6 entries)
                      Error: "too many entries on IMP:N card"
```

### Validation Algorithm

```
1. Count total cells in Cell Cards block
2. Parse IMP card entries (split by whitespace)
3. Count IMP entries
4. Compare:
   if IMP_count < cell_count:
       WARNING (MCNP assumes 0 for missing)
   if IMP_count > cell_count:
       FATAL ERROR (MCNP terminates)
   if IMP_count == cell_count:
       PASS
```

### Multi-Particle Importance

```
c 5 cells
IMP:N  1 1 1 1 0    ← Neutrons (5 entries) ✓
IMP:P  2 2 2 2 0    ← Photons (5 entries) ✓
IMP:E  0 0 0 0 0    ← Electrons (5 entries) ✓

Each particle type must have exactly 5 entries
```

### Validation Rules

**FATAL if:**
- IMP entries > cell count (too many)

**WARNING if:**
- IMP entries < cell count (too few, assumes 0)

**PASS if:**
- IMP entries = cell count (exact match)

---

## 8. Other Data Card References

### Volume Card (VOL)

**Format:** `VOL  v1 v2 v3 ... vN`
**Rule:** N entries must equal N cells

```
c 5 cells
VOL  100.5 200.3 150.8 75.2 1e6    ← 5 entries ✓

VOL  100.5 200.3                    ← 2 entries for 5 cells ✗
```

### Area Card (AREA)

**Format:** `AREA  a1 a2 a3 ... aN`
**Rule:** N entries must equal N surfaces

### PWR Card (Power)

**Format:** `PWR  p1 p2 p3 ... pN`
**Rule:** N entries must equal N cells with fissionable material

---

## Parsing Guidelines

### General Cross-Reference Extraction

**Step 1: Identify card type**
- Cell card → Extract surfaces, material, transformation
- Tally card → Extract cells or surfaces
- FM card → Extract materials
- IMP/VOL/AREA → Count entries

**Step 2: Parse reference fields**
- Use regex patterns for each card type
- Extract numeric IDs
- Handle continuations (& character)

**Step 3: Build reference maps**
- Create dictionaries: {source → [targets]}
- Track all references for validation

**Step 4: Validate references**
- Check each target exists
- Record broken references
- Flag unused entities

### Error Reporting Format

**Broken reference:**
```
Source: Cell 10, line 45
Reference type: Cell → Surface
Referenced entity: Surface 203
Status: UNDEFINED (not found in Surface Cards block)
Impact: FATAL - MCNP will terminate
Fix: Add surface 203 definition or correct cell 10 geometry
```

**Unused entity:**
```
Entity: Surface 99, line 72
Type: Unused surface
Status: Defined but never referenced in any cell
Impact: WARNING - Clutters input, may indicate incomplete geometry
Action: Remove if not needed, or verify should be used
```

---

## Integration with Validation Workflow

**Order of validation:**
1. Syntax validation (input-validator)
2. Cross-reference validation (THIS SKILL)
3. Geometry validation (geometry-checker)
4. Physics validation (physics-validator)

**Cross-reference checking is required before geometry validation** because broken references cause immediate FATAL errors, while geometry issues may be subtler.

---

**END OF REFERENCE_RELATIONSHIPS.MD**
