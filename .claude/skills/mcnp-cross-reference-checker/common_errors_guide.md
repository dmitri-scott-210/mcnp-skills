# Common Cross-Reference Errors Guide
## Catalog of Errors with Solutions

## Error 1: Undefined Surface Reference

### MCNP Error Message
```
bad trouble in subroutine trackan.    surface       500 does not exist.
```

### Root Cause
Cell references surface 500, but surface 500 not defined in surfaces block

### Example
```mcnp
c Cells
100 1 -8.0  -500 501  $ References surface 500

c Surfaces
c ... surface 500 missing ...
501 pz  10.0
```

### Detection
```python
Cell 100 references surface 500
Surface 500 NOT found in surfaces block
```

### Solutions

**Solution 1: Define Missing Surface**
```mcnp
c Surfaces
500 pz  5.0   $ Add missing surface
501 pz  10.0
```

**Solution 2: Correct Typo**
```mcnp
c Cells
100 1 -8.0  -501 502  $ Correct 500 → 501
```

**Solution 3: Remove Incorrect Reference**
If surface 500 was mistakenly added to cell definition, remove it.

### Prevention
- Use systematic numbering (allocate ranges)
- Define all surfaces before cells
- Use validation tools before running MCNP

---

## Error 2: Undefined Material Reference

### MCNP Error Message
```
material   50 is not an input material.
```

### Root Cause
Cell references material 50, but m50 not defined in materials block

### Example
```mcnp
c Cells
200 50 0.08  -100  $ References material 50

c Data cards
m1  $ Material 1 defined
   92235.70c  0.05
   92238.70c  0.95
    8016.70c  2.0
c ... material 50 missing ...
```

### Detection
```python
Cell 200 references material 50
Material m50 NOT found in data cards
```

### Solutions

**Solution 1: Define Missing Material**
```mcnp
c Data cards
m50  $ Add missing material
   [composition here]
```

**Solution 2: Correct Material ID**
```mcnp
c Cells
200 1 0.08  -100  $ Use material 1 instead
```

### Prevention
- Keep material definitions organized
- Use comments to document material IDs
- Validate before running

---

## Error 3: Undefined Universe in Fill

### MCNP Error Message
```
universe    1234 is used in fill but is not defined.
```

### Root Cause
Cell fills with universe 1234, but no cells declare u=1234

### Example
```mcnp
c Cells
300 0  -200  fill=1234  $ Fills with universe 1234

c ... no cells with u=1234 ...
```

### Detection
```python
Cell 300 fills with universe 1234
Universe 1234 NOT declared (no cells with u=1234)
```

### Solutions

**Solution 1: Define Missing Universe**
```mcnp
c Define universe 1234
1000 1 -8.0  -100  u=1234  $ Declare universe 1234
1001 2 -2.7   100  u=1234
```

**Solution 2: Correct Universe Number**
```mcnp
c Cells
300 0  -200  fill=1230  $ Use existing universe
```

### Prevention
- Define child universes before parent
- Use systematic universe numbering
- Validate universe fill chains

---

## Error 4: Circular Universe Reference

### MCNP Error Message
```
bad trouble in subroutine readlattice.
universe recursion detected.
```

### Root Cause
Universe A fills with universe B, and universe B fills with universe A

### Example
```mcnp
c Cells
100 0  -10  u=100 fill=200  $ Universe 100 → 200
200 0  -20  u=200 fill=100  $ Universe 200 → 100 (CYCLE!)
```

### Detection
```python
Fill graph:
  100 → [200]
  200 → [100]
Cycle detected: 100 → 200 → 100
```

### Solutions

**Solution 1: Restructure Hierarchy**
```mcnp
c Break cycle by introducing intermediate universe
100 0  -10  u=100 fill=300  $ 100 → 300
200 1 -8.0  -20  u=200       $ 200 is now terminal
300 0  -30  u=300 fill=200  $ 300 → 200
```

**Solution 2: Remove One Fill**
```mcnp
c Make one universe terminal
100 0  -10  u=100 fill=200
200 1 -8.0  -20  u=200       $ Remove fill=100
```

### Prevention
- Plan universe hierarchy BEFORE implementation
- Draw hierarchy diagram
- Validate fill chains before running

---

## Error 5: Lattice Fill Array Size Mismatch

### MCNP Error Message
```
warning.  lattice with wrong number of elements.
```

### Root Cause
Lattice fill array has wrong number of elements for declared bounds

### Example
```mcnp
c Lattice with fill=-7:7 -7:7 0:0
400 0  -400 u=400 lat=1  fill=-7:7 -7:7 0:0
     100 100 100 ... [only 224 elements, need 225!]
```

### Detection
```python
Fill bounds: -7:7 -7:7 0:0
Expected: (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15×15×1 = 225
Actual: 224 elements provided
Mismatch: 1 element short
```

### Solutions

**Solution 1: Add Missing Elements**
```mcnp
400 0  -400 u=400 lat=1  fill=-7:7 -7:7 0:0
     100 100 100 ... [225 elements total] ✓
```

**Solution 2: Fix Bounds**
```mcnp
c Adjust bounds to match array size
400 0  -400 u=400 lat=1  fill=-7:7 -7:6 0:0  $ 15×14×1 = 210
     100 100 100 ... [210 elements]
```

### Prevention
- Calculate dimensions: (max-min+1) for each axis
- Include zero when counting negative to positive
- Validate before running

---

## Error 6: Repeat Notation Off-By-One

### MCNP Error Message
```
warning.  lattice with wrong number of elements.
```

### Root Cause
Misunderstanding "nR" repeat notation (nR = n+1 copies, not n copies)

### Example
```mcnp
c Need 31 elements for fill=0:0 0:0 -15:15
400 0  -400 u=400 lat=1  fill=0:0 0:0 -15:15
     100 3R 200 25R 100 3R  $ WRONG: 4 + 26 + 4 = 34 (3 too many!)
```

### Detection
```python
Expected: 31 elements
Repeat notation: "100 3R 200 25R 100 3R"
Expanded: 100 (4 times) + 200 (26 times) + 100 (4 times) = 34
Error: 3 elements too many
```

### Solution
```mcnp
c Correct repeat notation: nR = n+1 copies
400 0  -400 u=400 lat=1  fill=0:0 0:0 -15:15
     100 2R 200 24R 100 2R  $ RIGHT: 3 + 25 + 3 = 31 ✓
```

### Key Rule
**"U nR" means n+1 total copies of U**

Examples:
- `100 0R` = 1 copy of 100
- `100 1R` = 2 copies of 100
- `100 2R` = 3 copies of 100
- `100 9R` = 10 copies of 100

### Prevention
- Remember: nR = n+1 copies
- Always validate expanded array size
- Use calculator or script to expand notation

---

## Error 7: Duplicate Cell ID

### MCNP Error Message
```
duplicate cell card number      100
```

### Root Cause
Two cells have same ID

### Example
```mcnp
c Cells
100 1 -8.0  -10  $ First cell 100
...
100 2 -2.7  -20  $ Duplicate cell 100!
```

### Detection
```python
Cell ID 100 appears at:
  Line 45: 100 1 -8.0  -10
  Line 234: 100 2 -2.7  -20
Duplicate detected
```

### Solutions

**Solution 1: Renumber Second Cell**
```mcnp
100 1 -8.0  -10
...
101 2 -2.7  -20  $ Changed to 101
```

**Solution 2: Use Systematic Numbering**
```python
# Allocate ranges
# Fuel cells: 100-199
# Clad cells: 200-299
# Coolant cells: 300-399
```

### Prevention
- Plan numbering scheme before building model
- Use systematic/hierarchical numbering
- Validate IDs before running

---

## Error 8: Missing Surface Sense

### MCNP Error Message
```
bad trouble in subroutine makelsn.    cell    100 has no volume.
```

### Root Cause
Cell Boolean expression doesn't define a closed volume (e.g., missing +/- on surface)

### Example
```mcnp
c Cells
100 1 -8.0  -10 11  $ Missing sense on surface 11!

c Surfaces
10 cz  5.0
11 pz  10.0
```

### Problem
- `-10` = inside cylinder 10 (infinite height)
- `11` = which side of plane 11? (ambiguous!)

### Solution
```mcnp
c Cells
100 1 -8.0  -10 -11  $ Inside cylinder, below plane
```

### Prevention
- Always specify +/- for surface sense
- Visualize geometry to verify
- Test with lost particle check

---

## Error 9: Overlapping Cells (Geometry Error)

### MCNP Error Message
```
overlap of cells   100   200
```

### Root Cause
Two cells claim ownership of same region in space

### Example
```mcnp
c Cells
100 1 -8.0  -10        $ Inside cylinder 10
200 2 -2.7  -11        $ Inside cylinder 11

c Surfaces
10 cz  5.0
11 cz  5.5  $ Cylinder 11 contains cylinder 10 → overlap!
```

### Detection
MCNP finds particles in regions claimed by both cells 100 and 200

### Solutions

**Solution 1: Proper Nesting**
```mcnp
c Cells
100 1 -8.0  -10        $ Inside 10
200 2 -2.7   10 -11    $ Between 10 and 11 (outside 10, inside 11)
```

**Solution 2: Union Operator**
```mcnp
c Cells
100 1 -8.0  -10        $ Inside 10
200 2 -2.7  -11 (#100) $ Inside 11, but NOT in cell 100
```

### Prevention
- Carefully design Boolean expressions
- Visualize with MCNP plotter
- Use complement operator when needed

---

## Error 10: Gap in Geometry (Lost Particles)

### MCNP Error Message
```
10 particles got lost
```

### Root Cause
Geometry has gaps not covered by any cell

### Example
```mcnp
c Cells
100 1 -8.0  -10 11 -12  $ Between plane 11 and 12
200 0       10          $ Outside cylinder 10

c Surfaces
10 cz  5.0
11 pz  0.0
12 pz  10.0
c GAP: What about inside cylinder 10, below plane 11?
```

### Detection
Particles track into undefined region → lost

### Solutions

**Solution 1: Add Missing Cell**
```mcnp
c Fill the gap
100 1 -8.0  -10  11 -12
150 2 -2.7  -10 -11     $ Add cell for gap region
200 0        10
```

**Solution 2: Expand Existing Cell**
```mcnp
c Extend cell 100 to cover gap
100 1 -8.0  -10     -12  $ Removed 11 (now covers below 11 too)
200 0        10
```

### Prevention
- Plot geometry before running
- Run test with few particles first
- Check for lost particles in output

---

## Summary: Top 10 Cross-Reference Errors

| Rank | Error Type | Frequency | Detection | Prevention |
|------|-----------|-----------|-----------|------------|
| 1 | Undefined surface | Very High | Parse cell geometry | Define all surfaces |
| 2 | Undefined material | High | Check material refs | Systematic numbering |
| 3 | Undefined universe | High | Trace fill chains | Define before use |
| 4 | Lattice size mismatch | High | Calculate elements | Validate array size |
| 5 | Repeat notation error | Medium | Expand notation | Remember nR=n+1 |
| 6 | Circular universe | Medium | Build fill graph | Plan hierarchy |
| 7 | Duplicate IDs | Medium | Track all IDs | Allocate ranges |
| 8 | Geometry overlap | Low | MCNP check | Careful Boolean |
| 9 | Geometry gap | Low | Lost particles | Plot geometry |
| 10 | Wrong surface sense | Low | Volume check | Always specify +/- |

**Key Takeaway**: **Pre-run validation catches 90% of these errors!**
