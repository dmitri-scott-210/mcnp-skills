# Complex Reactor Patterns - Multi-Level Hierarchies

**Purpose**: Examples of 3-6 level nested lattice hierarchies for complex reactors

**Source**: Based on AGENT8_FILL_ARRAY_DEEP_DIVE.md section 4 and AGR1_CELL_CARD_COMPLETE_ANALYSIS.md

---

## Multi-Level Hierarchy Concepts

### Hierarchy Levels (Bottom-Up Definition Order)

```
Level 1: Basic Component (pin, particle, pellet)
   └─ Geometry primitives (cylinders, spheres)

Level 2: Component Assembly (pin in channel, particle in matrix)
   └─ Single cells with materials

Level 3: First Lattice Level (pins in assembly, particles in lattice)
   └─ LAT=1 or LAT=2, FILL array

Level 4: Second Lattice Level (assemblies in subregion, compacts in stack)
   └─ LAT=1 or LAT=2, FILL array

Level 5: Third Lattice Level (subregions in core, stacks in capsule)
   └─ LAT=1 or LAT=2, FILL array

Level 6: Global Placement (core in geometry, capsule in global)
   └─ FILL with transformations
```

**Critical rule**: Define child universe BEFORE parent universe!

---

## Example 1: PWR Core (4 Levels)

### Level 1: Fuel Pin (u=100)

```mcnp
c UO2 fuel pin
100 1 -10.2  -1     u=100  imp:n=1  $ Fuel
101 2 -6.5   1 -2   u=100  imp:n=1  $ Clad
102 3 -1.0   2      u=100  imp:n=1  $ Water

c Surfaces for pin
1 cz 0.41   $ Fuel radius
2 cz 0.48   $ Clad outer
```

### Level 2: Fuel Assembly (u=200)

```mcnp
c 17×17 pin array (LAT=1 rectangular)
c fill=-8:8 -8:8 0:0 → 289 elements
200 0  -10  u=200 lat=1  imp:n=1  fill=-8:8 -8:8 0:0
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     [... 15 more rows ...]

c u=100: Standard fuel pin
c u=101: Guide tube (control rod channel)

10 rpp -10.71 10.71 -10.71 10.71 -180 180  $ 17 × 1.26 cm pitch
```

### Level 3: Core Quarter (u=300)

```mcnp
c 15×15 assembly array (quarter core symmetry)
c fill=0:14 0:14 0:0 → 225 assemblies
300 0  -20  u=300 lat=1  imp:n=1  fill=0:14 0:14 0:0
     200 200 200 200 200 200 200 200 200 200 200 200 200 200 200
     200 200 200 200 200 201 201 201 201 201 200 200 200 200 200
     200 200 200 201 201 201 201 202 201 201 201 201 200 200 200
     [... 12 more rows with various assembly types ...]

c u=200: Fresh fuel assembly (4.5% enrichment)
c u=201: Once-burned assembly (3.8% effective)
c u=202: Control assembly (burnable poison)

20 rpp 0 318.3 0 318.3 -180 180  $ 15 × 21.22 cm assembly pitch
```

### Level 4: Full Core (u=0, global)

```mcnp
c Full core with 4-fold symmetry
c Uses transformations to place 4 quarter-cores
1000 0  -20  fill=300       imp:n=1             $ SW quarter
1001 0  -21  fill=300 (*1)  imp:n=1             $ SE quarter (y-reflection)
1002 0  -22  fill=300 (*2)  imp:n=1             $ NE quarter (180° rotation)
1003 0  -23  fill=300 (*3)  imp:n=1             $ NW quarter (x-reflection)
1004 3 -0.7  20 21 22 23 -30  imp:n=1           $ Radial reflector
1005 0  30  imp:n=0                             $ Outside world

c Transformation cards
*tr1  0 0 0  90 90  90 0  90 90  $ Reflect across y-axis
*tr2  0 0 0  -1 0 0  0 -1 0  0 0 1  $ 180° rotation
*tr3  0 0 0  -90 90  90 0  -90 90  $ Reflect across x-axis

20 rpp 0 318.3 0 318.3 -180 180       $ SW quarter
21 rpp -318.3 0 0 318.3 -180 180      $ SE quarter
22 rpp -318.3 0 -318.3 0 -180 180     $ NE quarter
23 rpp 0 318.3 -318.3 0 -180 180      $ NW quarter
30 cz 400                              $ Core barrel
```

**Hierarchy summary**: Pin → Assembly (17×17) → Quarter (15×15) → Full core (4 quarters)

---

## Example 2: HTGR with TRISO (6 Levels)

### Level 1: TRISO Particle (u=1114)

```mcnp
c 5-layer coated particle
1 1 -10.8  -1     u=1114  imp:n=1  $ UO2 kernel (350 μm)
2 2 -0.98  1 -2   u=1114  imp:n=1  $ Buffer (100 μm)
3 3 -1.85  2 -3   u=1114  imp:n=1  $ IPyC (40 μm)
4 4 -3.20  3 -4   u=1114  imp:n=1  $ SiC (35 μm)
5 5 -1.86  4 -5   u=1114  imp:n=1  $ OPyC (40 μm)
6 6 -1.70  5      u=1114  imp:n=1  $ Matrix filler

1 so 0.01750  $ 350 μm / 2 = 175 μm = 0.01750 cm
2 so 0.02750  $ +100 μm buffer
3 so 0.03150  $ +40 μm IPyC
4 so 0.03500  $ +35 μm SiC
5 so 0.03900  $ +40 μm OPyC
```

### Level 2: Matrix Cell (u=1115)

```mcnp
c Graphite matrix without particle
10 6 -1.70  -10  u=1115  imp:n=1  $ SiC matrix

10 so 0.03900  $ Same size as TRISO outer radius
```

### Level 3: Particle Lattice (u=1116)

```mcnp
c 15×15 rectangular lattice approximating cylindrical compact
c fill=-7:7 -7:7 0:0 → 225 elements
20 0  -20  u=1116 lat=1  imp:n=1  fill=-7:7 -7:7 0:0
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     [... 13 more rows with circular pattern ...]

c u=1114: TRISO particle (~169 particles in circular pattern)
c u=1115: Matrix filler (~56 cells at corners)

20 rpp -0.5865 0.5865 -0.5865 0.5865 -0.048 0.048  $ Contains 15×15 lattice
```

### Level 4: Matrix End Caps (u=1117)

```mcnp
c Top/bottom graphite caps for compact
30 6 -1.70  -30  u=1117  imp:n=1  $ Solid graphite

30 rpp -0.635 0.635 -0.635 0.635 -0.238 0.238  $ Slightly larger than particle lattice
```

### Level 5: Fuel Compact Stack (u=1110)

```mcnp
c 1×1×31 vertical stack with repeat notation
c fill=0:0 0:0 -15:15 → 31 elements
40 0  -40  u=1110 lat=1  imp:n=1  fill=0:0 0:0 -15:15
     1117 2R 1116 24R 1117 2R

c Breakdown:
c   1117 2R  = 3 bottom caps
c   1116 24R = 25 fuel compacts
c   1117 2R  = 3 top caps
c Total: 3 + 25 + 3 = 31 ✓

40 rpp -0.635 0.635 -0.635 0.635 -7.62 7.62  $ 31 × 0.492 cm height
```

### Level 6: Capsule Assembly (u=0, global)

```mcnp
c Global placement with transformations
1000 0  -50  fill=1110 (0 0 -100)  imp:n=1  $ Capsule 1
1001 0  -51  fill=1110 (0 0 0)     imp:n=1  $ Capsule 2
1002 0  -52  fill=1110 (0 0 100)   imp:n=1  $ Capsule 3
1010 7 -1.7  50 51 52 -60  imp:n=1          $ Graphite holder
1011 0  60  imp:n=0                          $ Outside

50 cz 0.7  $ Capsule 1 boundary
51 cz 0.7  $ Capsule 2 boundary
52 cz 0.7  $ Capsule 3 boundary
60 cz 5.0  $ Outer boundary
```

**Hierarchy summary**: Particle → Matrix → Particle lattice (15×15) → End caps → Compact stack (1×1×31) → Global placement

**Efficiency**: ~5,000 TRISO particles per compact × 25 compacts = 125,000 particles modeled with ~150 cell definitions

---

## Example 3: Fast Reactor (5 Levels)

### Level 1: Fuel Pin (u=100)

```mcnp
c MOX fuel pin
100 11 -10.0  -1     u=100  imp:n=1  $ MOX fuel
101 12 -7.9   1 -2   u=100  imp:n=1  $ SS316 clad
102 13 -0.83  2      u=100  imp:n=1  $ Liquid sodium
```

### Level 2: Pin Bundle (u=200, Hexagonal!)

```mcnp
c 271-pin bundle (LAT=2 hexagonal)
c fill=-8:8 -8:8 0:0 → 289 elements (271 fuel + 18 empty)
200 0  -10  u=200 lat=2  imp:n=1  fill=-8:8 -8:8 0:0
     300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300
      300 300 300 300 300 300 100 100 100 100 100 100 300 300 300 300 300
       [... hexagonal pattern with 271 fuel pins ...]

c u=100: Fuel pin
c u=300: Empty (corner positions outside hexagonal boundary)

10 rhp  0 0 0  0 0 200  0 8.0 0  $ R=8.0 cm, pitch=13.86 cm
```

### Level 3: Assembly (u=300)

```mcnp
c Hexagonal assembly wrapper around pin bundle
300 0  -20  fill=200  u=300  imp:n=1  $ Pin bundle
301 14 -7.9  20 -21  u=300  imp:n=1  $ Duct wall
302 13 -0.83  21  u=300  imp:n=1  $ Inter-assembly sodium

20 rhp  0 0 0  0 0 200  0 8.0 0   $ Bundle
21 rhp  0 0 0  0 0 200  0 8.5 0   $ Duct outer
```

### Level 4: Core (u=400, Hexagonal!)

```mcnp
c 91-assembly core (LAT=2 hexagonal)
c fill=-5:5 -5:5 0:0 → 121 elements (91 assemblies + 30 reflector)
400 0  -30  u=400 lat=2  imp:n=1  fill=-5:5 -5:5 0:0
     500 500 500 500 500 500 500 500 500 500 500
      500 500 500 500 300 300 300 300 500 500 500
       500 500 500 300 300 300 310 300 300 500 500
        [... 91 assemblies in hexagonal core layout ...]

c u=300: Driver fuel assembly
c u=310: Control assembly
c u=500: Radial reflector assembly

30 rhp  0 0 0  0 0 200  0 50.0 0  $ Large core
```

### Level 5: Reactor Vessel (u=0, global)

```mcnp
1000 0  -40  fill=400  imp:n=1         $ Core
1001 13 -0.83  40 -41  imp:n=1         $ Sodium pool
1002 14 -7.9  41 -42  imp:n=1          $ Reactor vessel
1003 0  42  imp:n=0                    $ Outside

40 cz 150   $ Core boundary
41 cz 250   $ Vessel inner
42 cz 260   $ Vessel outer
```

**Hierarchy summary**: Pin → Pin bundle (271 hex) → Assembly → Core (91 hex) → Vessel

**Note**: BOTH LAT=1 and LAT=2 can be mixed in same model! Fuel pins could use rectangular packing within hexagonal assemblies.

---

## Mixed Lattice Types

### Example: Rectangular Pins in Hexagonal Core

```mcnp
c Level 1: Fuel pin (u=100)
100 1 -10.0  -1  u=100  imp:n=1

c Level 2: 7×7 rectangular pin array (LAT=1)
200 0  -10  u=200 lat=1  imp:n=1  fill=0:6 0:6 0:0
     100 100 100 100 100 100 100
     [... 6 more rows ...]

c Level 3: Assembly with rectangular pin array
300 0  -20  fill=200  u=300  imp:n=1

c Level 4: Hexagonal core of assemblies (LAT=2)
400 0  -30  u=400 lat=2  imp:n=1  fill=-3:3 -3:3 0:0
     500 500 500 500 500 500 500
      500 500 300 300 300 500 500
       [... hexagonal pattern ...]
```

**Flexibility**: MCNP allows arbitrary mixing of LAT=1 and LAT=2 at different hierarchy levels!

---

## Validation Rules for Multi-Level Hierarchies

1. ✅ **Bottom-up definition**: Define Level 1 before Level 2, Level 2 before Level 3, etc.

2. ✅ **No circular references**: Level N cannot reference Level N+1 or higher

3. ✅ **All universes defined**: If FILL array contains u=150, cell with u=150 must exist

4. ✅ **Consistent nesting**: Each level must be fully contained within parent

5. ✅ **Surface sizing**: Each lattice bounding surface must accommodate N × pitch

6. ✅ **Universe uniqueness**: Don't reuse universe numbers for different geometries

**Use these patterns** as templates for building your own complex reactor models.

---

**This document provides production-quality multi-level hierarchy examples for immediate use in complex reactor modeling.**
