# MCNP Lattice Geometry - Complete Reference

Lattices are MCNP's method for efficiently modeling repeated structures (fuel assemblies, detector arrays, hexagonal cores). Instead of defining hundreds of identical pins individually, you define ONE pin in a local universe and fill an array with it.

## Core Concepts

**Three components required:**
1. **Universe (U)** - Define repeated unit in local coordinates
2. **Lattice cell (LAT)** - Define array structure (rectangular or hexagonal)
3. **Fill (FILL)** - Specify which universes fill array positions

**Workflow:**
1. Define base geometry in universe (U=1, U=2, etc.)
2. Create lattice cell with LAT parameter
3. Fill lattice with universes using FILL parameter
4. Optionally nest lattices (universe with lattice fills another universe)

---

## Universe (U) Parameter

**Purpose:** Assign cell to local coordinate system that can be instanced elsewhere

**Syntax:** `U=n` (on cell card)

**Values:**
- `U=0` - Base universe (default, main geometry) - all cells without U parameter
- `U>0` - Local universe (can be filled into other cells)

**Example - Pin universe:**
```
c Define fuel pin in universe 1 (local coordinate system)
1  1  -10.5  -1     U=1  IMP:N=1    $ Fuel (origin-centered)
2  0         1 -2   U=1  IMP:N=1    $ Gap
3  2  -6.5    2 -3  U=1  IMP:N=1    $ Clad

1  CZ  0.41                          $ Fuel radius (local origin)
2  CZ  0.42                          $ Gap outer
3  CZ  0.48                          $ Clad outer (defines pin boundary)
```

**Key concept:** Universe 1 exists in its own LOCAL coordinate system centered at (0,0,0). When filled into a lattice, it's replicated at each lattice position.

---

## LAT=1: Rectangular Lattices

**Purpose:** Cartesian grid of repeated universes (square or rectangular pitch)

**Requirements:**
1. Cell must have `LAT=1` parameter
2. Cell must have `U=n` (universe assignment)
3. Cell must have `FILL` parameter (what fills array)
4. Cell geometry must be appropriate for rectangular lattice

### Geometry Requirements for LAT=1

**The lattice cell geometry MUST be an axis-aligned box** (six planes perpendicular to x, y, z):

**Correct LAT=1 geometry (axis-aligned box):**
```
10  0  -10 -11 12  LAT=1  U=2  FILL=1  IMP:N=1

10  PX  -5.0              $ x_min (must be PX, not rotated plane)
11  PX   5.0              $ x_max
12  PY  -5.0              $ y_min (must be PY)
13  PY   5.0              $ y_max
14  PZ   0.0              $ z_min (must be PZ)
15  PZ  100.0             $ z_max
```

**Incorrect LAT=1 geometry (will fail):**
```
10  0  -10  LAT=1  U=2  FILL=1  IMP:N=1
10  RPP  -5 5  -5 5  0 100   $ ERROR: RPP not allowed for LAT=1
```

**Why this matters:** MCNP calculates lattice pitch from plane positions. For X direction: pitch = (x_max - x_min) / (i_max - i_min + 1)

### Index Ordering for LAT=1

**Critical:** LAT=1 uses **(i, j, k)** indices corresponding to **(X, Y, Z)** axes

**Index ranges:**
- `i` varies along X axis (i_min to i_max)
- `j` varies along Y axis (j_min to j_max)
- `k` varies along Z axis (k_min to k_max)

**FILL array format:**
```
FILL  i_min:i_max  j_min:j_max  k_min:k_max
      universe_list (k_min, j_min, i_min) to (k_max, j_max, i_max)
```

**Reading order (CRITICAL):**
1. **i (X) varies FASTEST** (innermost loop)
2. **j (Y) varies MIDDLE** (middle loop)
3. **k (Z) varies SLOWEST** (outermost loop)

Think: `for k in [k_min:k_max]: for j in [j_min:j_max]: for i in [i_min:i_max]: universe[k][j][i]`

### Example 1: Simple 3×3 LAT=1 Lattice

```
c Pin universe (U=1)
1  1  -10.5  -1  U=1  IMP:N=1    $ Fuel pin
2  3  -1.0    1 -2  U=1  IMP:N=1 $ Water around pin

c Control rod universe (U=2)
3  4  -2.0   -1  U=2  IMP:N=1    $ Absorber
4  3  -1.0    1 -2  U=2  IMP:N=1 $ Water around rod

c 3×3 lattice (9 positions, single layer in Z)
10  0  -10 11 -12 13 -14 15  LAT=1  U=3  IMP:N=1
            FILL=-1:1 -1:1 0:0
                 1 1 2        $ j=1 (Y=top row): fuel, fuel, control rod
                 1 1 1        $ j=0 (Y=middle row): all fuel
                 2 1 1        $ j=-1 (Y=bottom row): control rod, fuel, fuel
c Reading order: k=0, j=-1: i=-1 (U=2), i=0 (U=1), i=1 (U=1)
c               k=0, j=0:  i=-1 (U=1), i=0 (U=1), i=1 (U=1)
c               k=0, j=1:  i=-1 (U=1), i=0 (U=1), i=1 (U=2)

c Pin and lattice surfaces
1   CZ  0.5                    $ Pin/rod radius
2   CZ  0.707                  $ Hexagon for pin cell (~1.26 cm pitch)
10  PX  -1.89                  $ Lattice X min (3 × 1.26 cm pitch)
11  PX   1.89                  $ Lattice X max
12  PY  -1.89                  $ Lattice Y min
13  PY   1.89                  $ Lattice Y max
14  PZ   0.0                   $ Lattice Z min
15  PZ  100.0                  $ Lattice Z max
```

**Pitch calculation:**
- X pitch: (1.89 - (-1.89)) / (1 - (-1) + 1) = 3.78 / 3 = 1.26 cm
- Y pitch: (1.89 - (-1.89)) / (1 - (-1) + 1) = 3.78 / 3 = 1.26 cm
- Z pitch: (100 - 0) / (0 - 0 + 1) = 100 cm (single layer)

### Example 2: 2×2×2 Three-Dimensional LAT=1

```
c Simple cell universe
1  1  -10.0  -1  U=1  IMP:N=1
1  RPP  -0.5 0.5  -0.5 0.5  -0.5 0.5   $ 1 cm cube

c 2×2×2 lattice (8 positions)
10  0  -10 11 -12 13 -14 15  LAT=1  U=2  IMP:N=1
            FILL=0:1 0:1 0:1
                 1 1        $ k=0, j=0: i=0 (U=1), i=1 (U=1)
                 1 1        $ k=0, j=1: i=0 (U=1), i=1 (U=1)
                 1 1        $ k=1, j=0: i=0 (U=1), i=1 (U=1)
                 1 1        $ k=1, j=1: i=0 (U=1), i=1 (U=1)
c All 8 positions filled with universe 1

10  PX  0.0
11  PX  2.0                   $ 2 cm in X (2 cells × 1 cm)
12  PY  0.0
13  PY  2.0                   $ 2 cm in Y
14  PZ  0.0
15  PZ  2.0                   $ 2 cm in Z
```

### Example 3: Large Reactor Core (17×17 Assembly)

```
c Fuel pin (U=1)
1  1  -10.4  -101     U=1  IMP:N=1
2  0        101 -102  U=1  IMP:N=1
3  2  -6.5   102 -103 U=1  IMP:N=1
4  3  -0.7   103 -104 U=1  IMP:N=1

c Guide tube pin (U=2)
5  3  -0.7   -102     U=2  IMP:N=1
6  2  -6.5   102 -103 U=2  IMP:N=1
7  3  -0.7   103 -104 U=2  IMP:N=1

c 17×17 PWR assembly (289 positions, 24 guide tubes + 1 instrument tube)
20  0  -201 202 -203 204 -205 206  LAT=1  U=3  IMP:N=1
       FILL=-8:8 -8:8 0:0
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1    $ j=8
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 2 1 1 2 1 1 2 1 1 1 1 1    $ j=6: guide tubes at i=-5,0,5
            1 1 1 2 1 1 1 1 1 1 1 1 1 2 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 2 1 1 2 1 1 2 1 1 2 1 1 2 1 1    $ j=3: 5 guide tubes
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 2 1 1 2 1 1 2 1 1 2 1 1 2 1 1    $ j=0: center, instrument tube at i=0
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 2 1 1 2 1 1 2 1 1 2 1 1 2 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 2 1 1 1 1 1 1 1 1 1 2 1 1 1
            1 1 1 1 1 2 1 1 2 1 1 2 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

101  CZ  0.4095        $ Fuel radius
102  CZ  0.4180        $ Gap outer
103  CZ  0.4750        $ Clad outer
104  CZ  0.6350        $ Pin cell boundary (1.27 cm pitch)

201  PX  -10.795       $ Assembly X min (17 × 1.27 cm)
202  PX   10.795       $ Assembly X max
203  PY  -10.795       $ Assembly Y min
204  PY   10.795       $ Assembly Y max
205  PZ   0.0          $ Assembly bottom
206  PZ  365.76        $ Assembly top (active height)
```

---

## LAT=2: Hexagonal Lattices

**Purpose:** Hexagonal array of repeated universes (triangular/hexagonal pitch)

**Requirements:** Same as LAT=1, but with LAT=2 and different geometry

### Geometry Requirements for LAT=2

**The lattice cell geometry MUST be a hexagonal prism** parallel to Z-axis:

**Option 1: Use six planes forming hexagon + two z-planes:**
```
10  0  -10 -11 -12 -13 -14 -15 -16 17  LAT=2  U=2  FILL=1  IMP:N=1

c Hexagon planes (60° angles, forming regular hexagon)
10  P   0.866  0.5  0  5.0    $ Side 1 (rotated 30° from X)
11  P   0.866 -0.5  0  5.0    $ Side 2
12  P   0.0   -1.0  0  5.0    $ Side 3
13  P  -0.866 -0.5  0  5.0    $ Side 4
14  P  -0.866  0.5  0  5.0    $ Side 5
15  P   0.0    1.0  0  5.0    $ Side 6
16  PZ  0.0                   $ Bottom
17  PZ  100.0                 $ Top
```

**Option 2: Use RHP macrobody (easier):**
```
10  0  -10 -11 12  LAT=2  U=2  FILL=1  IMP:N=1

10  RHP  0 0 0  0 0 100  5 0 0  0 0 60    $ Hex prism (inradius 5 cm, height 100 cm)
```

### Index Ordering for LAT=2

**Critical:** LAT=2 uses **ring/position** indexing, NOT (i,j,k)

**Hexagonal coordinate system:**
- Position (0, 0, 0) is CENTER of lattice
- Positions arranged in hexagonal rings around center
- Each ring has 6n positions (n = ring number)
  - Ring 0: 1 position (center)
  - Ring 1: 6 positions
  - Ring 2: 12 positions
  - Ring 3: 18 positions

**FILL array format:**
```
FILL  i_min:i_max  j_min:j_max  k_min:k_max
      universe_list (ring 0, then ring 1 positions 1-6, then ring 2 positions 1-12, ...)
```

**For LAT=2:**
- `i` and `j` define hexagonal position using **axial coordinates** (not Cartesian!)
- `k` is still Z-axis (vertical layers)
- Index ranges must form valid hexagon: |i| + |j| ≤ max_ring

**Position numbering (ring 1 as example):**
- Position 1: i=1, j=0 (right of center, along +X direction)
- Position 2: i=0, j=1 (upper-right, 60° from +X)
- Position 3: i=-1, j=1 (upper-left, 120° from +X)
- Position 4: i=-1, j=0 (left, 180° from +X)
- Position 5: i=0, j=-1 (lower-left, 240° from +X)
- Position 6: i=1, j=-1 (lower-right, 300° from +X)

### Example 4: Simple 3-Ring Hexagonal Lattice (LAT=2)

```
c Fuel pin universe (U=1)
1  1  -10.5  -1     U=1  IMP:N=1
2  3  -1.0    1 -2  U=1  IMP:N=1

c Control rod universe (U=2)
3  4  -2.0   -1     U=2  IMP:N=1
4  3  -1.0    1 -2  U=2  IMP:N=1

c Hexagonal lattice (3 rings = 1 + 6 + 12 = 19 positions)
10  0  -10 -11 12  LAT=2  U=3  IMP:N=1
       FILL=-2:2 -2:2 0:0
            0 0 2 0 0       $ j=2: positions outside hex (0 = not used)
            0 1 1 2 0       $ j=1: 3 positions (i=-1,0,1 at j=1)
            2 1 1 1 2       $ j=0: 5 positions (i=-2,-1,0,1,2 at j=0) - center row
            0 1 1 2 0       $ j=-1: 3 positions
            0 0 2 0 0       $ j=-2
c Reading: center (0,0), ring 1 (6 positions), ring 2 (12 positions)
c U=0 means position not in lattice (outside hexagonal boundary)

1   CZ  0.5
2   CZ  0.6            $ Pin cell radius

10  RHP  0 0 0  0 0 100  3.6 0 0  0 0 60   $ Hex prism (inradius ~3.6 cm, 3 rings × 1.2 cm pitch)
11  PZ  0.0
12  PZ  100.0
```

**Pitch:** Distance between adjacent hex centers = 2 × inradius / (2 × n_rings + 1)

---

## LAT=1 vs LAT=2 Comparison

| Feature | LAT=1 (Rectangular) | LAT=2 (Hexagonal) |
|---------|---------------------|-------------------|
| **Grid type** | Cartesian (square/rectangular) | Hexagonal (60° angles) |
| **Coordinate system** | (i, j, k) → (X, Y, Z) | (i, j, k) hexagonal axial + Z |
| **Index ordering** | i varies fastest, j middle, k slowest | Ring-based, complex ordering |
| **Geometry requirement** | Six axis-aligned planes (box) | Hexagonal prism (6 planes or RHP) |
| **Pitch definition** | X and Y pitch from plane positions | Inradius from hexagon geometry |
| **Common uses** | PWR cores, square arrays | VVER cores, HTGR, hexagonal assemblies |
| **Ease of use** | Simpler (Cartesian intuition) | More complex (hex indexing) |
| **Efficiency** | Good for square grids | Better for circular/hex geometry |

---

## Nested Lattices

**Purpose:** Hierarchical geometry (pins → assembly → core)

**Concept:** A lattice cell (with LAT parameter) is assigned to a universe (U=n), which can then fill another lattice.

**Three-level hierarchy example:**

### Example 5: Nested Lattice (Pin → Assembly → Core)

```
c === Level 1: Pin geometry (universe 1) ===
1  1  -10.5  -101     U=1  IMP:N=1    $ Fuel
2  0        101 -102  U=1  IMP:N=1    $ Gap
3  2  -6.5   102 -103 U=1  IMP:N=1    $ Clad
4  3  -1.0   103      U=1  IMP:N=1    $ Water

c === Level 2: Assembly (universe 2, contains 3×3 lattice of pins) ===
10  0  -201 202 -203 204 -205 206  LAT=1  U=2  IMP:N=1
       FILL=-1:1 -1:1 0:0
            1 1 1
            1 1 1
            1 1 1
c Assembly contains 9 pins from universe 1

c === Level 3: Core (universe 0, contains 2×2 array of assemblies) ===
20  0  -301 302 -303 304 -305 306  LAT=1  U=3  IMP:N=1
       FILL=0:1 0:1 0:0
            2 2
            2 2
c Core contains 4 assemblies from universe 2
c Each assembly contains 9 pins → 36 pins total

c === Level 4: Base geometry (universe 0, surrounds core) ===
30  0  -30  FILL=3  IMP:N=1         $ Fill with universe 3 (core)
31  0   30  IMP:N=0                 $ Graveyard

c === Surface definitions ===
c Pin surfaces (universe 1, local coordinates)
101  CZ  0.41
102  CZ  0.42
103  CZ  0.48

c Assembly surfaces (universe 2)
201  PX  -1.89        $ 3 pins × 1.26 cm pitch
202  PX   1.89
203  PY  -1.89
204  PY   1.89
205  PZ   0.0
206  PZ  100.0

c Core lattice surfaces (universe 3)
301  PX  0.0          $ 2 assemblies × 3.78 cm width
302  PX  7.56
303  PY  0.0
304  PY  7.56
305  PZ  0.0
306  PZ  100.0

c Outer boundary (universe 0)
30  RPP  -10 20  -10 20  -10 110
```

**Hierarchy:**
- Universe 1 (pin): 4 cells, local origin
- Universe 2 (assembly): LAT=1 lattice filled with U=1, becomes single unit
- Universe 3 (core): LAT=1 lattice filled with U=2, becomes single unit
- Universe 0 (base): Fills cell 30 with U=3, adds graveyard

**Key insight:** Each lattice acts as a "compressed" geometry - once filled, it's treated as a single unit at the next level.

---

## TRCL with FILL: Transforming Filled Universes

**Purpose:** Rotate or translate a filled universe (not the fill cell itself)

**Syntax:**
```
cell_number  0  geometry  FILL=n  TRCL=m  IMP:N=1
```

**Use case:** Rotate hexagonal assembly in square lattice, translate assemblies

### Example 6: Rotated Hexagonal Assembly in Square Core

```
c Hexagonal pin (U=1)
1  1  -10.5  -1  U=1  IMP:N=1
1  CZ  0.5

c Hexagonal assembly (U=2, LAT=2 with 19 positions)
10  0  -10  LAT=2  U=2  FILL=-1:1 -1:1 0:0  ... IMP:N=1
10  RHP  0 0 0  0 0 100  3.6 0 0  0 0 60

c Square core lattice (universe 3) with rotated assemblies
c Assembly at (0,0): no rotation
20  0  -20  FILL=2  IMP:N=1

c Assembly at (1,0): rotated 30 degrees
21  0  -21  FILL=2  TRCL=1  IMP:N=1

c Assembly at (0,1): rotated 60 degrees
22  0  -22  FILL=2  TRCL=2  IMP:N=1

20  RPP  -5 5  -5 5  0 100
21  RPP   5 15  -5 5  0 100
22  RPP  -5 5   5 15  0 100

*TR1  0 0 0  0.866 0.5 0  -0.5 0.866 0  0 0 1   $ 30° rotation
*TR2  0 0 0  0.5 0.866 0  -0.866 0.5 0  0 0 1   $ 60° rotation
```

**Effect:** Each hexagonal assembly (U=2) is filled into a square cell with different rotations, allowing hex assemblies in square core grid.

---

## Common Lattice Patterns

### PWR 17×17 Assembly
- 289 positions (17×17)
- 264 fuel pins + 24 guide tubes + 1 instrument tube
- Square pitch: 1.26-1.27 cm
- Index range: -8:8 in X and Y

### BWR 8×8 Assembly
- 64 positions (8×8)
- ~60 fuel pins + water rods
- Square pitch: ~1.63 cm
- Index range: 0:7 or -3:4

### VVER-1000 Hexagonal Assembly
- 312 fuel pins in hexagonal array
- Hexagonal pitch: ~1.2 cm
- Typically modeled with LAT=2 or explicit geometry

### HTGR Prismatic Core
- Hexagonal fuel blocks with fuel channels
- Two-level: channels in block (LAT=1), blocks in core (LAT=2)

---

## Index Ordering Best Practices

1. **LAT=1: Always remember i-j-k = X-Y-Z**
   - Test with 2×2×1 array first to verify ordering

2. **LAT=2: Draw the hexagon first**
   - Mark center (0,0), then ring 1 positions
   - Use U=0 for positions outside hexagonal boundary

3. **FILL array layout:**
   - Use consistent indentation (one row per j value for LAT=1)
   - Comment critical positions (center, control rods, etc.)

4. **Verify with geometry plots:**
   - Always plot X-Y, X-Z, Y-Z slices
   - Check lattice positions match expected pattern

5. **Universe numbering scheme:**
   - U=1-99: Pin types
   - U=100-199: Assembly types
   - U=200-299: Core arrangements

---

## Debugging Lattice Geometry

**Common errors:**

1. **Wrong index ordering** - Filled array doesn't match expected pattern
   - Fix: Remember i varies fastest for LAT=1

2. **Pitch mismatch** - Gaps or overlaps between lattice elements
   - Fix: Verify lattice boundary matches (i_max - i_min + 1) × pitch

3. **Universe not found** - FILL references undefined universe
   - Fix: Ensure all universes in FILL array are defined

4. **Lattice geometry wrong shape** - Cell geometry doesn't match LAT type
   - Fix: LAT=1 needs box (6 planes), LAT=2 needs hexagonal prism

5. **Lost particles at lattice boundaries**
   - Fix: Ensure universe geometry fills entire local cell (no gaps)

**Debugging workflow:**
1. Define and test single universe (U=1) in isolation
2. Create minimal lattice (2×2 or 3×3)
3. Plot geometry (ip card): `ip  1 200 200  1 600 600` for detailed plot
4. Verify lattice positions with labels: `label 1 2` in plot command
5. Expand to full lattice size once minimal case works

---

## 10 Examples from Simple to Complex

### 1. Single universe fill (no lattice)
```
1  1  -10.5  -1  U=1  IMP:N=1
2  0  -2  FILL=1  IMP:N=1         $ Fill cell 2 with universe 1
1  CZ  5.0
2  CZ  10.0
```

### 2. 2×2 LAT=1 (simplest lattice)
```
1  1  -10.5  -1  U=1  IMP:N=1
2  0  -10 11 -12 13 -14 15  LAT=1  U=2  IMP:N=1  FILL=0:1 0:1 0:0  1 1  1 1
1  CZ  0.5
10  PX  0.0
11  PX  2.0
12  PY  0.0
13  PY  2.0
14  PZ  0.0
15  PZ  10.0
```

### 3. 3×3 LAT=1 with two universe types
(See Example 1 above)

### 4. Single-layer hex lattice (LAT=2)
(See Example 4 above)

### 5. 2×2×2 three-dimensional LAT=1
(See Example 2 above)

### 6. 17×17 PWR assembly
(See Example 3 above)

### 7. Nested lattice (pin → assembly → core)
(See Example 5 above)

### 8. Rotated hexagonal assembly
(See Example 6 above)

### 9. Heterogeneous core (multiple assembly types)
```
c Fuel assembly (U=10)
... define 17×17 lattice with fuel pins ...

c MOX assembly (U=20)
... define 17×17 lattice with MOX pins ...

c Reflector assembly (U=30)
... define solid reflector ...

c Core (2×2 assemblies)
100  0  -100 101 -102 103 -104 105  LAT=1  U=40  IMP:N=1
        FILL=0:1 0:1 0:0
             10 20        $ j=1: fuel and MOX
             30 30        $ j=0: two reflectors

100  PX  0.0
101  PX  43.18          $ 2 assemblies × 21.59 cm
102  PY  0.0
103  PY  43.18
104  PZ  0.0
105  PZ  365.76
```

### 10. Multi-level nested with transformations
```
c Pin (U=1)
1  1  -10.5  -1  U=1  IMP:N=1
1  CZ  0.5

c Assembly (U=2, 3×3 pins)
10  0  -10 11 -12 13 -14 15  LAT=1  U=2  FILL=-1:1 -1:1 0:0  1 1 1  1 1 1  1 1 1  IMP:N=1

c Core with four rotated assemblies
20  0  -20  FILL=2  IMP:N=1           $ No rotation
21  0  -21  FILL=2  TRCL=1  IMP:N=1   $ 90° rotation
22  0  -22  FILL=2  TRCL=2  IMP:N=1   $ 180° rotation
23  0  -23  FILL=2  TRCL=3  IMP:N=1   $ 270° rotation

20  RPP  -5 5   -5 5   0 100
21  RPP   5 15  -5 5   0 100
22  RPP   5 15   5 15  0 100
23  RPP  -5 5    5 15  0 100

*TR1  0 0 0  0 1 0  -1 0 0  0 0 1     $ 90° Z-axis rotation
*TR2  0 0 0  -1 0 0  0 -1 0  0 0 1    $ 180° rotation
*TR3  0 0 0  0 -1 0  1 0 0  0 0 1     $ 270° rotation
```

---

## Best Practices

1. **Start simple** - Test universe in isolation before lattice
2. **Comment FILL arrays** - Note what each position contains
3. **Use consistent universe numbering** - U=1-99 pins, U=100+ assemblies
4. **Always plot geometry** - Verify lattice matches expectation
5. **Check boundary calculations** - Lattice size must match pitch × count
6. **Test with minimal lattice first** - 2×2 before 17×17
7. **Document index ordering** - Note i-j-k convention in comments
8. **Use TRCL for rotations** - Don't redefine rotated universes
9. **Verify no gaps in universe** - Local geometry must fill entire cell
10. **Consider computational cost** - Lattices are efficient, but nested lattices add tracking complexity

---

**References:**
- MCNP6 User Manual, Chapter 5.02: Cell Cards - LAT and FILL parameters
- MCNP6 User Manual, Chapter 5.02: Universe and TRCL
- LA-UR-17-29981: MCNP6.2 User Guide on Lattice Geometry
