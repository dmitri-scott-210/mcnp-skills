# MCNP Cell Checker - Universe and Lattice Theory

Theoretical foundation for understanding universe systems, lattice types, fill arrays, and nesting hierarchies in MCNP.

---

## Universe System (U and FILL Parameters)

### Universe Definitions (`u=N`)

- Assigns cell to universe N (N > 0)
- Universe 0 = "real world" (default, no u= parameter)
- Universe numbers must be unique within each cell
- Multiple cells can belong to same universe
- Creates geometric building blocks for reuse

### Universe References (`fill=N`)

- Fills a cell with all cells from universe N
- Referenced universe must be defined somewhere in input
- Creates hierarchy levels (level 0 = real world, level 1+ = filled)
- Can have up to 20 levels of nesting (typical: 3-7)

### Common Universe Patterns

**Single-level fill**:
```
1 0 -100 fill=1 imp:n=1          $ Real world cell, fill with u=1
10 1 -2.7 -200 u=1 imp:n=1       $ Universe 1 definition
```

**Multi-level fill**:
```
1 0 -100 fill=1 imp:n=1          $ Level 0 (real world)
10 0 -200 u=1 fill=2 imp:n=1     $ Level 1 (fills level 0)
20 1 -2.7 -300 u=2 imp:n=1       $ Level 2 (fills level 1)
```

**Lattice fill**:
```
100 0 -500 lat=1 u=5 fill=-3:3 -3:3 0:0 imp:n=1
    1 1 1 1 1 1 1
    1 2 2 2 2 2 1
    1 2 3 3 3 2 1
    1 2 3 4 3 2 1    $ 4 = center, 1 = edge
    1 2 3 3 3 2 1
    1 2 2 2 2 2 1
    1 1 1 1 1 1 1
```

### Validation Rules

1. Every `fill=N` must have corresponding `u=N` definition(s)
2. Universe 0 cannot be explicitly used (it's the default)
3. No circular references: u=1 fills u=2 which fills u=1 (infinite loop)
4. Negative u= indicates cell fully enclosed (performance optimization)
5. Maximum 20 nesting levels (practical limit: 10)

---

## Lattice System (LAT and FILL Arrays)

### Lattice Types

- `lat=1`: Cubic/rectangular lattice (hexahedral elements, 6 faces)
- `lat=2`: Hexagonal lattice (hexagonal prism elements, 8 faces)
- No other values allowed (lat=3, lat=0, etc. are INVALID)

### LAT=1 Cubic Lattice

**Structure**:
```
Cell card:
  200 0 -200 lat=1 u=10 fill=-5:5 -5:5 0:0 imp:n=1
      1 1 1 1 1 1 1 1 1 1 1    $ i = -5 to +5 (11 elements)
      1 2 2 2 2 2 2 2 2 2 1    $ j = -5 to +5 (11 elements)
      ...                        $ k = 0 to 0 (1 element)
      (11 lines × 11 values = 121 total values)

Surface definition:
  200 rpp -11 11 -11 11 0 10    $ Rectangular parallelepiped
```

**Indexing**:
- Element [0,0,0] is bounded by first 6 surfaces in cell geometry
- Element indices increase across surfaces in order listed
- Surface order determines lattice indexing

### LAT=2 Hexagonal Lattice

**Structure**:
```
Cell card:
  300 0 -301 -302 -303 -304 -305 -306 -307 -308
      lat=2 u=20 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1    $ Hexagonal arrangement
      1 2 2 2 2 2 1
      1 2 3 3 3 2 1
      1 2 3 4 3 2 1
      1 2 3 3 3 2 1
      1 2 2 2 2 2 1
      1 1 1 1 1 1 1

Surface definitions (hexagon with 6 sides + 2 bases):
  301 p ...    $ Six planar surfaces defining hexagon
  302 p ...
  303 p ...
  304 p ...
  305 p ...
  306 p ...
  307 pz 0     $ Bottom base
  308 pz 10    $ Top base
```

### Fill Array Dimension Validation

**Formula**:
```
Declaration: fill= i1:i2 j1:j2 k1:k2

Required values = (i2-i1+1) × (j2-j1+1) × (k2-k1+1)

Example:
fill= -7:7 -7:7 0:0
  → i: -7 to 7 = 15 values
  → j: -7 to 7 = 15 values
  → k: 0 to 0 = 1 value
  → Total required: 15 × 15 × 1 = 225 values

Must provide exactly 225 universe IDs after fill= declaration
```

### Lattice Surface Ordering

**For `lat=1`**, surface order in cell card determines lattice indexing:
- Surfaces 1-2: Define i-direction ([1,0,0] and [-1,0,0])
- Surfaces 3-4: Define j-direction ([0,1,0] and [0,-1,0])
- Surfaces 5-6: Define k-direction ([0,0,1] and [0,0,-1])

**For `lat=2`**, eight surfaces define hexagonal prism:
- Surfaces 1-6: Six sides of hexagon (i and j directions)
- Surfaces 7-8: Top and bottom bases (k direction)

### Common Lattice Errors

```
BAD: Wrong lattice type
  100 0 -100 lat=3 fill=1 imp:n=1    ✗ lat=3 doesn't exist

GOOD: Valid lattice type
  100 0 -100 lat=1 fill=1 imp:n=1    ✓ lat=1 (cubic)

BAD: Lattice without fill
  100 0 -100 lat=1 imp:n=1            ✗ LAT requires FILL

GOOD: Lattice with fill
  100 0 -100 lat=1 fill=5 imp:n=1    ✓ Fills with u=5

BAD: Dimension mismatch
  100 0 -100 lat=1 fill=-2:2 -2:2 0:0 imp:n=1
      1 2 3 4 5    ✗ Only 5 values, need 5×5×1 = 25

GOOD: Correct dimensions
  100 0 -100 lat=1 fill=-2:2 -2:2 0:0 imp:n=1
      1 1 1 1 1
      1 2 2 2 1
      1 2 3 2 1    ✓ 25 values (5×5×1)
      1 2 2 2 1
      1 1 1 1 1
```

---

## Nesting Depth and Performance

### Nesting Levels

- Level 0: Real world (u=0, implicit)
- Level 1: Cells filled into level 0
- Level 2: Cells filled into level 1
- ...
- Level N: Up to 20 allowed

### Performance Impact

**Shallow nesting (1-3 levels)**: Minimal impact
```
Example: Fuel pins in assembly in core
Level 0: Core
Level 1: Assembly
Level 2: Pins
```

**Moderate nesting (4-7 levels)**: Noticeable but acceptable
```
Example: TRISO particles in compact in fuel block in core
Level 0: Reactor vessel
Level 1: Core
Level 2: Fuel column
Level 3: Fuel block
Level 4: Fuel compact
Level 5: TRISO particle lattice
Level 6: Particle layers
```

**Deep nesting (8-10 levels)**: Performance degradation
- Particle tracking slower
- Memory usage increases
- Consider simplification

**Excessive nesting (>10 levels)**: Not recommended
- Significant performance penalty
- Difficult to debug
- May indicate over-modeling

### Optimization Recommendations

If nesting exceeds 7 levels, consider:
- Combining levels where possible
- Using negative universe numbers for enclosed cells
- Simplifying geometry representation
- Homogenizing lower levels

---

## Cell Parameter Validation

### Required Combinations

```
If cell has lat= parameter:
  → MUST have fill= parameter
  → Cannot have material/density (must be void, m=0)
  → Surfaces define [0,0,0] lattice element

If cell has fill= parameter (non-lattice):
  → Usually void (m=0), but can have material
  → Material in filled cell adds to fill universe
  → Surfaces define window boundary

If cell has u= parameter:
  → Belongs to that universe
  → Can be filled into other cells via fill=
  → Can have material or be void
```

### Parameter Conflicts

```
BAD: Lattice with material
  100 1 -2.7 -100 lat=1 fill=5 imp:n=1    ✗ Lattice must be void

GOOD: Lattice as void
  100 0 -100 lat=1 fill=5 imp:n=1         ✓ Void lattice

BAD: Lattice without fill
  100 0 -100 lat=1 imp:n=1                ✗ LAT requires FILL

GOOD: Lattice with fill array
  100 0 -100 lat=1 fill=-3:3 -3:3 0:0 imp:n=1
      1 1 1 1 1 1 1
      ...                                  ✓ Complete fill array

BAD: Undefined universe fill
  100 0 -100 fill=99 imp:n=1              ✗ u=99 not defined

GOOD: Defined universe fill
  100 0 -100 fill=5 imp:n=1               ✓ u=5 defined elsewhere
  500 1 -2.7 -500 u=5 imp:n=1             ✓ Universe 5 definition
```

---

## Best Practices

### 1. Negative Universe Optimization

**Use negative u= for fully enclosed cells**:
```
c Positive u= (default, slower):
c   MCNP checks cell against all higher-level boundaries

100 1 -2.7 -100 u=50 imp:n=1           $ Standard

c Negative u= (optimized, faster):
c   MCNP skips higher-level boundary checks (cell fully enclosed)

100 1 -2.7 -100 u=-50 imp:n=1          $ Optimized

c WARNING: Only use negative u= if cell is TRULY fully enclosed
c          Incorrect usage can cause wrong answers with no warnings!
```

### 2. Lattice Boundary Surface Standards

**LAT=1 (Cubic)**:
```
c Recommended: RPP macrobody
200 0 -200 lat=1 u=10 fill=1 imp:n=1
200 rpp -10 10 -10 10 0 20                    $ Rectangular box

c Alternative: 6 planes
200 0 -201 202 -203 204 -205 206 lat=1 u=10 fill=1 imp:n=1
201 px -10    $ i=-1 direction
202 px 10     $ i=+1 direction
203 py -10    $ j=-1 direction
204 py 10     $ j=+1 direction
205 pz 0      $ k=-1 direction
206 pz 20     $ k=+1 direction
```

**LAT=2 (Hexagonal)**:
```
c Recommended: HEX macrobody
300 0 -300 lat=2 u=20 fill=1 imp:n=1
300 rhp 0 0 0  0 0 20  5                      $ Hexagonal prism

c Alternative: 6 planes + 2 z-planes
300 0 -301 302 -303 304 -305 306 -307 308 lat=2 u=20 fill=1 imp:n=1
301 p ...    $ Hex side 1
302 p ...    $ Hex side 2
303 p ...    $ Hex side 3
304 p ...    $ Hex side 4
305 p ...    $ Hex side 5
306 p ...    $ Hex side 6
307 pz 0     $ Bottom
308 pz 20    $ Top
```

### 3. Universe Hierarchy Limits

**Recommended nesting depths**:
```
1-3 levels: Ideal (minimal overhead)
  Example: Pins → Assembly → Core

4-7 levels: Acceptable (common for reactors)
  Example: Particles → Compact → Block → Column → Core → Vessel

8-10 levels: Use with caution (performance impact)
  Consider negative u= optimization

>10 levels: Not recommended
  Simplify geometry or homogenize lower levels
```

---

**END OF UNIVERSE_LATTICE_THEORY.MD**
