# Cell Card Concepts Reference

This document provides detailed technical reference for MCNP cell card features related to universes, lattices, and fill arrays.

## Universe System (U and FILL Parameters)

### Universe Definitions (u=N)

**Purpose:** Assigns cell to universe N, creating geometric building blocks for reuse.

**Syntax:**
```
cell_number  material  density  geometry  u=N  other_params
```

**Rules:**
- Universe N must be a positive integer (N > 0)
- Universe 0 = "real world" (default, no u= parameter needed)
- Universe numbers must be unique per cell
- Multiple cells can belong to same universe
- Negative universe numbers (u=-N) indicate fully enclosed cells (performance optimization)

**Examples:**
```
c Real world cells (u=0 implicit)
1 0 -100 fill=1 imp:n=1                    $ Real world, fills with u=1
999 0 100 imp:n=0                           $ Outside world (graveyard)

c Universe 1 definition
10 1 -2.7 -200 u=1 imp:n=1                 $ Aluminum cell in universe 1
11 0 200 -201 u=1 imp:n=1                  $ Void cell in universe 1

c Universe 2 definition (optimized)
20 1 -10.5 -300 u=-2 imp:n=1               $ Negative u= (fully enclosed, faster)
```

### Universe References (fill=N)

**Purpose:** Fills a cell with all cells from universe N.

**Syntax:**
```
cell_number  0  geometry  fill=N  imp:n=1    $ Simple fill
cell_number  0  geometry  lat=1 fill=...     $ Lattice fill (array)
```

**Rules:**
- Referenced universe must be defined somewhere in input
- Creates hierarchy levels: level 0 (real world) → level 1+ (filled)
- Maximum 20 levels of nesting (practical limit: 10)
- fill=0 is invalid (universe 0 is the real world)

**Hierarchy Example:**
```
c Level 0: Real world
1 0 -100 fill=1 imp:n=1              $ Fill with universe 1

c Level 1: Fills into level 0
10 0 -200 u=1 fill=2 imp:n=1         $ Universe 1, fills with universe 2

c Level 2: Fills into level 1
20 1 -2.7 -300 u=2 imp:n=1           $ Universe 2 (terminal, has material)
```

### Universe Validation Rules

1. **Every fill=N must have corresponding u=N definition(s)**
   - MCNP will fatal error if fill references undefined universe
   - Check: defined_universes ⊇ used_universes

2. **Universe 0 cannot be explicitly used**
   - It's the default "real world"
   - Never write u=0 or fill=0

3. **No circular references**
   - u=1 fills u=2 which fills u=1 = infinite loop
   - Causes MCNP fatal error
   - Must form directed acyclic graph (DAG)

4. **Negative universe optimization**
   - u=-N indicates cell is fully enclosed
   - MCNP skips higher-level boundary checks (faster)
   - WARNING: Only use if truly enclosed; incorrect usage gives wrong answers with no warnings

5. **Maximum nesting depth**
   - MCNP allows up to 20 levels
   - Practical limit: 10 levels (performance)
   - Deep nesting (>10) causes significant slowdown

## Lattice System (LAT and FILL Arrays)

### Lattice Types

MCNP supports exactly two lattice types:

**LAT=1: Cubic/Rectangular Lattice**
- Hexahedral elements (6 faces)
- Cartesian coordinate system
- Element [0,0,0] bounded by first 6 surfaces in cell geometry
- Surface order determines indexing: i-direction (surfaces 1-2), j-direction (3-4), k-direction (5-6)

**LAT=2: Hexagonal Lattice**
- Hexagonal prism elements (8 faces: 6 sides + 2 bases)
- Element [0,0,0] at center
- Requires 8 surfaces: 6 for hexagon sides, 2 for top/bottom bases
- Special indexing for hexagonal arrangement

**Invalid:** LAT=0, LAT=3, LAT=4, etc. do not exist and will cause fatal error.

### LAT=1 (Cubic) Lattice Specification

**Complete Syntax:**
```
cell_number  0  geometry  lat=1  u=N  fill=i1:i2 j1:j2 k1:k2  imp:n=1
    universe_id_values...
```

**Requirements:**
- Material must be 0 (void)
- Must have fill= parameter (lattice without fill is invalid)
- Geometry surfaces define [0,0,0] lattice element
- Fill array provides universe IDs for each lattice position

**Example:**
```
c Cubic lattice: 3×3×1 array
100 0 -100 lat=1 u=10 fill=-1:1 -1:1 0:0 imp:n=1
    1 1 1    $ j=-1: i=-1,0,1
    1 2 1    $ j=0:  i=-1,0,1  (center = u=2)
    1 1 1    $ j=1:  i=-1,0,1

c Boundary surface
100 rpp -3 3 -3 3 0 10    $ Rectangular parallelepiped

c Universe definitions
10 1 -2.7 -200 u=1 imp:n=1       $ Standard fuel
20 2 -6.5 -201 u=2 imp:n=1       $ Control rod
```

**Surface Ordering for LAT=1:**
```
cell  0  -s1 s2 -s3 s4 -s5 s6  lat=1  fill=...

s1, s2: Define i-direction (x-axis, [±1,0,0])
s3, s4: Define j-direction (y-axis, [0,±1,0])
s5, s6: Define k-direction (z-axis, [0,0,±1])
```

### LAT=2 (Hexagonal) Lattice Specification

**Complete Syntax:**
```
cell_number  0  geometry  lat=2  u=N  fill=i1:i2 j1:j2 k1:k2  imp:n=1
    universe_id_values...
```

**Requirements:**
- Material must be 0 (void)
- Must have fill= parameter
- Typically 8 surfaces: 6 planar (hexagon) + 2 PZ (top/bottom)
- Alternative: HEX or RHP macrobody

**Example:**
```
c Hexagonal lattice: 3×3×1 array
200 0 -200 lat=2 u=20 fill=-1:1 -1:1 0:0 imp:n=1
    1 1 1
    1 2 1
    1 1 1

c Boundary surface (HEX macrobody)
200 rhp 0 0 0  0 0 20  5    $ Origin, height vector, apothem

c Universe definitions (same as above)
```

### Fill Array Dimension Validation

**Critical Rule:** Array size must match declared range exactly.

**Formula:**
```
Declaration: fill= i1:i2 j1:j2 k1:k2
Required values = (i2 - i1 + 1) × (j2 - j1 + 1) × (k2 - k1 + 1)
```

**Examples:**

```
✓ CORRECT:
fill= -2:2 -2:2 0:0
  → i: -2,-1,0,1,2 = 5 values
  → j: -2,-1,0,1,2 = 5 values
  → k: 0 = 1 value
  → Total: 5 × 5 × 1 = 25 values required
Provide exactly 25 universe IDs

✗ WRONG:
fill= -7:7 -7:7 0:0
  → Expected: 15 × 15 × 1 = 225 values
  → Provided: 210 values
  → MCNP FATAL ERROR: Array size mismatch
```

### Fill Array Formatting

**Recommended format for readability:**

```
c Document dimensions
c Lattice: 7×7×1 cubic array (49 values)
c Each line = 7 values (i = -3 to 3)
c Need 7 lines (j = -3 to 3)
100 0 -100 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1    $ j=-3
    1 2 2 2 2 2 1    $ j=-2
    1 2 3 3 3 2 1    $ j=-1
    1 2 3 4 3 2 1    $ j=0  (center row)
    1 2 3 3 3 2 1    $ j=1
    1 2 2 2 2 2 1    $ j=2
    1 1 1 1 1 1 1    $ j=3
```

**Benefits:**
- Visual verification of symmetry
- Easy to count rows and columns
- Comments help track position
- Errors are immediately obvious

### Lattice Surface Recommendations

**For LAT=1 (Cubic):**

**Option A: RPP Macrobody (Recommended)**
```
100 0 -100 lat=1 fill=... imp:n=1
100 rpp xmin xmax ymin ymax zmin zmax    $ Rectangular box
```

**Option B: Six Planes**
```
100 0 -101 102 -103 104 -105 106 lat=1 fill=... imp:n=1
101 px xmin      $ i-direction lower
102 px xmax      $ i-direction upper
103 py ymin      $ j-direction lower
104 py ymax      $ j-direction upper
105 pz zmin      $ k-direction lower
106 pz zmax      $ k-direction upper
```

**For LAT=2 (Hexagonal):**

**Option A: RHP Macrobody (Recommended)**
```
200 0 -200 lat=2 fill=... imp:n=1
200 rhp vx vy vz  hx hy hz  r1 r2 r3    $ Hexagonal prism
```

**Option B: Eight Planes**
```
200 0 -201 202 -203 204 -205 206 -207 208 lat=2 fill=... imp:n=1
201-206 p ...    $ Six planar surfaces defining hexagon
207 pz zmin      $ Bottom base
208 pz zmax      $ Top base
```

## Nesting Depth and Performance

### Hierarchy Levels

**Level Definition:**
- Level 0: Real world (u=0, implicit)
- Level 1: Cells with fill= in level 0
- Level 2: Cells with fill= in level 1
- ...
- Level N: Maximum 20 allowed by MCNP

**Example Hierarchy:**
```
Level 0: Reactor vessel (real world)
  └─ Level 1: Core region (fill=1)
       └─ Level 2: Fuel assembly lattice (u=1, fill=2)
            └─ Level 3: Pin cell lattice (u=2, fill=3)
                 └─ Level 4: Fuel pin layers (u=3)
```

### Performance Impact by Depth

**Shallow Nesting (1-3 levels): Minimal Impact**
- Typical: Pins → Assembly → Core
- Performance overhead: <5%
- Recommended for most simulations

**Moderate Nesting (4-7 levels): Acceptable**
- Typical: TRISO → Compact → Block → Column → Core → Vessel
- Performance overhead: 10-30%
- Common for advanced reactor designs
- Consider negative universe optimization

**Deep Nesting (8-10 levels): Use with Caution**
- Performance overhead: 30-60%
- Particle tracking significantly slower
- Memory usage increases
- Requires careful geometry design
- Strongly recommend negative universe optimization

**Excessive Nesting (>10 levels): Not Recommended**
- Performance overhead: >60%
- Very slow particle tracking
- Difficult to debug
- May indicate over-modeling
- Consider simplification or homogenization

### Optimization Strategies

**Strategy 1: Negative Universe Numbers**
```
c Standard (slower):
500 1 -10.5 -500 u=50 imp:n=1

c Optimized (faster):
500 1 -10.5 -500 u=-50 imp:n=1
$ Negative u= tells MCNP cell is fully enclosed
$ Skips boundary checks with higher-level universes
```

**WARNING:** Only use negative universes if cell is TRULY fully enclosed. Incorrect usage can produce wrong answers with no error messages.

**Strategy 2: Combine Levels**
```
c Before (12 levels):
u=0 → u=1 → u=2 → u=3 → u=4 → u=5 → u=6 → u=7 → u=8 → u=9 → u=10 → u=11

c After (4 levels):
u=0 → u=1 → u=5 → u=10
$ Eliminated intermediate levels by combining similar regions
```

**Strategy 3: Homogenization**
```
c Instead of modeling every TRISO particle (5 levels deep):
Replace particle lattice with homogenized fuel compact material
$ Reduces nesting by 3-4 levels
$ Acceptable for many analysis types
```

## Cell Parameter Validation

### Required Parameter Combinations

**Cell with LAT parameter:**
```
MUST have:
  - fill= parameter (lattice requires fill)
  - material = 0 (lattice must be void)
  - Appropriate boundary surfaces (6 for LAT=1, 8 for LAT=2)

cell_number  0  geometry  lat=1  u=N  fill=...  imp:n=1
```

**Cell with FILL parameter (non-lattice):**
```
USUALLY:
  - material = 0 (void)
  - Can have material (adds to fill universe)
  - Surfaces define "window" boundary

cell_number  0  geometry  fill=N  imp:n=1    $ Simple fill
```

**Cell with U parameter:**
```
CAN have:
  - Any material (or void)
  - fill= parameter (creates hierarchy)
  - Standard cell parameters

cell_number  M  rho  geometry  u=N  imp:n=1
```

### Parameter Conflicts (Common Errors)

**Error 1: Lattice with Material**
```
✗ WRONG:
100 1 -2.7 -100 lat=1 fill=5 imp:n=1
$ Lattice cells must be void (material 0)

✓ CORRECT:
100 0 -100 lat=1 fill=5 imp:n=1
```

**Error 2: Lattice without Fill**
```
✗ WRONG:
100 0 -100 lat=1 imp:n=1
$ LAT requires FILL

✓ CORRECT:
100 0 -100 lat=1 fill=5 imp:n=1
```

**Error 3: Undefined Universe Fill**
```
✗ WRONG:
100 0 -100 fill=99 imp:n=1
$ u=99 not defined anywhere

✓ CORRECT:
100 0 -100 fill=5 imp:n=1
500 1 -2.7 -500 u=5 imp:n=1    $ Universe 5 defined
```

**Error 4: Universe 0 Misuse**
```
✗ WRONG:
100 0 -100 u=0 imp:n=1
$ Cannot explicitly define u=0

✗ WRONG:
100 0 -100 fill=0 imp:n=1
$ Cannot fill with universe 0

✓ CORRECT:
100 0 -100 imp:n=1              $ u=0 is implicit (real world)
100 0 -100 fill=1 imp:n=1       $ Fill with defined universe
```

## Advanced Concepts

### Multi-Level Fill Example

**Complete 4-level hierarchy:**
```
c =================================================================
c LEVEL 0: REAL WORLD
c =================================================================
1 0 -100 fill=1 imp:n=1                 $ Core vessel
999 0 100 imp:n=0                        $ Outside world

c =================================================================
c LEVEL 1: CORE (fills into level 0)
c =================================================================
100 0 -200 u=1 lat=1 fill=-5:5 -5:5 0:0 imp:n=1
    2 2 2 2 2 2 2 2 2 2 2
    2 2 2 2 2 2 2 2 2 2 2
    2 2 2 3 3 3 3 3 2 2 2
    2 2 3 3 3 3 3 3 3 2 2
    2 2 3 3 3 3 3 3 3 2 2
    2 2 3 3 3 3 3 3 3 2 2
    2 2 3 3 3 3 3 3 3 2 2
    2 2 3 3 3 3 3 3 3 2 2
    2 2 2 3 3 3 3 3 2 2 2
    2 2 2 2 2 2 2 2 2 2 2
    2 2 2 2 2 2 2 2 2 2 2

c =================================================================
c LEVEL 2: FUEL ASSEMBLY (fills into level 1)
c =================================================================
200 0 -300 u=2 imp:n=1                  $ Reflector assembly
300 0 -400 u=3 lat=1 fill=-8:8 -8:8 0:0 imp:n=1
    4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
    ... (17×17 pin lattice)

c =================================================================
c LEVEL 3: PIN CELL (fills into level 2)
c =================================================================
400 1 -10.5 -500 u=4 imp:n=1            $ Fuel pellet
401 2 -6.5 500 -501 u=4 imp:n=1         $ Cladding
402 3 -1.0 501 -502 u=4 imp:n=1         $ Coolant
```

### Universe Reference Mapping

**Good practice: Document universe hierarchy at top of input:**
```
c =================================================================
c UNIVERSE REFERENCE MAP
c =================================================================
c u=0:  Real world (1 cell: core vessel)
c   fills: [1]
c
c u=1:  Core region (1 cell: assembly lattice)
c   fills: [2, 3]
c   filled by: [0]
c   level: 1
c
c u=2:  Reflector assembly (1 cell: graphite block)
c   fills: []
c   filled by: [1]
c   level: 2
c
c u=3:  Fuel assembly (1 cell: pin lattice)
c   fills: [4]
c   filled by: [1]
c   level: 2
c
c u=4:  Fuel pin (3 cells: pellet, clad, coolant)
c   fills: []
c   filled by: [3]
c   level: 3
c =================================================================
```

## References

- **MCNP6 Manual Chapter 5.2:** Complete cell card syntax
- **MCNP6 Manual Chapter 5.5.5:** Repeated structures (U/LAT/FILL)
- **MCNP6 Manual Chapter 5.5.5.1:** Universe keyword (U)
- **MCNP6 Manual Chapter 5.5.5.2:** Lattice keyword (LAT)
- **MCNP6 Manual Chapter 5.5.5.3:** Fill keyword (FILL)
- **MCNP6 Manual Chapter 10.1.3:** Repeated structures examples

---

**END OF CELL CONCEPTS REFERENCE**
