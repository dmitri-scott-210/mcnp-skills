# Lattice Patterns Reference

**Purpose**: Comprehensive examples for both rectangular (LAT=1) and hexagonal (LAT=2) lattices

**Source**: Based on AGENT8_FILL_ARRAY_DEEP_DIVE.md and AGR1_CELL_CARD_COMPLETE_ANALYSIS.md

---

## Rectangular Lattice (LAT=1) Patterns

### Pattern 1: Small 3×3 Array

```mcnp
c Simple 3×3 test lattice
100 0  -100  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     101 102 103
     104 105 106
     107 108 109

c Calculation: fill=-1:1 -1:1 0:0
c   I: (-1)-(1)+1 = 3 elements
c   J: (-1)-(1)+1 = 3 elements
c   K: 0-0+1 = 1 element
c   Total: 3×3×1 = 9 elements
```

### Pattern 2: PWR-Style 17×17 Assembly

```mcnp
c 17×17 PWR fuel assembly
c fill=0:16 0:16 0:0 → 17×17×1 = 289 elements
200 0  -200  u=300 lat=1  imp:n=1  fill=0:16 0:16 0:0
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     [... remaining 14 rows ...]

c Surface: RPP must accommodate 17 × pitch
c If pitch = 1.26 cm, RPP extent = 17 × 1.26 = 21.42 cm
200 rpp -10.71 10.71 -10.71 10.71 -180 180
```

### Pattern 3: Vertical Stack with Repeat Notation

```mcnp
c 1×1×31 vertical stack using repeat notation
c Demonstrates efficient specification for long arrays
300 0  -300  u=400 lat=1  imp:n=1  fill=0:0 0:0 -15:15
     401 2R 402 24R 401 2R

c Breakdown:
c   401 2R  = 3 copies of universe 401 (bottom)
c   402 24R = 25 copies of universe 402 (middle)
c   401 2R  = 3 copies of universe 401 (top)
c   Total: 3 + 25 + 3 = 31 elements ✓
```

### Pattern 4: Circular Packing (15×15 Approximating Cylinder)

```mcnp
c 15×15 lattice approximating cylindrical region
c fill=-7:7 -7:7 0:0 → 225 elements
400 0  -400  u=500 lat=1  imp:n=1  fill=-7:7 -7:7 0:0
     501 501 501 501 501 501 500 500 500 501 501 501 501 501 501
     501 501 501 500 500 500 500 500 500 500 500 500 501 501 501
     501 501 500 500 500 500 500 500 500 500 500 500 500 501 501
     501 501 500 500 500 500 500 500 500 500 500 500 500 501 501
     501 500 500 500 500 500 500 500 500 500 500 500 500 500 501
     501 500 500 500 500 500 500 500 500 500 500 500 500 500 501
     500 500 500 500 500 500 500 500 500 500 500 500 500 500 500
     500 500 500 500 500 500 500 500 500 500 500 500 500 500 500
     500 500 500 500 500 500 500 500 500 500 500 500 500 500 500
     501 500 500 500 500 500 500 500 500 500 500 500 500 500 501
     501 500 500 500 500 500 500 500 500 500 500 500 500 500 501
     501 501 500 500 500 500 500 500 500 500 500 500 500 501 501
     501 501 500 500 500 500 500 500 500 500 500 500 500 501 501
     501 501 501 500 500 500 500 500 500 500 500 500 501 501 501
     501 501 501 501 501 501 500 500 500 501 501 501 501 501 501

c u=500: Active region (fuel particles)
c u=501: Filler matrix (corners outside cylinder)
c Result: ~169 active + ~56 filler
```

---

## Hexagonal Lattice (LAT=2) Patterns

### Pattern 1: Small 7×7 Hexagonal

```mcnp
c 7×7 hexagonal lattice
c fill=-3:3 -3:3 0:0 → 49 elements
100 0  -100  u=200 lat=2  imp:n=1  fill=-3:3 -3:3 0:0
     300 300 300 300 300 300 300
      300 300 300 200 300 300 300
       300 300 200 200 200 300 300
        300 200 200 100 200 200 300
         300 300 200 200 200 300 300
          300 300 300 200 300 300 300
           300 300 300 300 300 300 300

c Optional indentation shows hexagonal stagger
c MCNP ignores whitespace

c RHP surface for this lattice
c Pitch = R × √3
100 rhp  0 0 0  0 0 50  0 1.0 0
```

### Pattern 2: Complete 13×13 HTGR Assembly

```mcnp
c Full 13×13 hexagonal assembly (ALL 169 elements)
c fill=-6:6 -6:6 0:0 → 169 elements
c Pitch = 1.6 × √3 = 2.77 cm
200 0  -200  u=300 lat=2  imp:n=1  fill=-6:6 -6:6 0:0
     300 300 300 300 300 300 300 300 300 300 300 300 300
      300 300 300 300 300 300 100 100 100 300 300 300 300
       300 300 300 300 300 100 100 200 100 100 300 300 300
        300 300 300 100 100 100 100 100 100 100 100 300 300
         300 300 100 100 100 100 100 100 100 100 100 100 300
          300 100 100 200 100 100 200 100 100 200 100 100 300
           300 100 100 100 100 100 100 100 100 100 100 300 300
            300 100 200 100 100 200 100 100 200 100 300 300 300
             300 100 100 100 100 100 100 100 100 300 300 300 300
              300 100 100 200 100 100 200 100 100 300 300 300 300
               300 100 100 100 100 100 100 100 300 300 300 300 300
                300 300 100 100 100 100 100 300 300 300 300 300 300
                 300 300 300 100 100 100 300 300 300 300 300 300 300

c u=100: Fuel channels
c u=200: Coolant channels (helium)
c u=300: Graphite reflector
c Pattern: Fuel and coolant in center, reflector at edges

200 rhp  0 0 0  0 0 68  0 1.6 0  $ R=1.6 cm
```

### Pattern 3: 9×9 Fast Reactor Core

```mcnp
c 9×9 hexagonal core layout
c fill=-4:4 -4:4 0:0 → 81 elements
300 0  -300  u=400 lat=2  imp:n=1  fill=-4:4 -4:4 0:0
     400 400 400 400 400 400 400 400 400
      400 400 400 100 100 100 400 400 400
       400 400 100 100 200 100 100 400 400
        400 100 100 200 100 200 100 100 400
         400 100 200 100 300 100 200 100 400
          400 100 100 200 100 200 100 100 400
           400 400 100 100 200 100 100 400 400
            400 400 400 100 100 100 400 400 400
             400 400 400 400 400 400 400 400 400

c u=100: Driver fuel assemblies
c u=200: Control assemblies
c u=300: Test assembly (center)
c u=400: Radial reflector

c RHP surface
300 rhp  0 0 0  0 0 365  0 10.0 0  $ Large core, R=10 cm
```

---

## Index Ordering Examples

### Understanding K, J, I Order

For `fill=-1:1 -1:1 -1:1` (3×3×3 = 27 elements):

```
Element    K    J    I   | Position Description
-----------------------------------------------
   1      -1   -1   -1   | Bottom level, back-left
   2      -1   -1    0   | Bottom level, back-center
   3      -1   -1    1   | Bottom level, back-right
   4      -1    0   -1   | Bottom level, middle-left
   5      -1    0    0   | Bottom level, middle-center
   6      -1    0    1   | Bottom level, middle-right
   7      -1    1   -1   | Bottom level, front-left
   8      -1    1    0   | Bottom level, front-center
   9      -1    1    1   | Bottom level, front-right
  10       0   -1   -1   | Middle level, back-left
  ...     ...  ...  ...  | ...
  27       1    1    1   | Top level, front-right
```

**Key insight**: I varies fastest (innermost loop), K varies slowest (outermost loop)

---

## Validation Examples

### Example 1: Dimension Mismatch (ERROR)

```mcnp
c WRONG: fill=0:10 0:10 0:0 but only 100 elements provided
c Need: (10-0+1) × (10-0+1) × (0-0+1) = 11×11×1 = 121 elements
c Provided: 100 elements
c Result: MCNP FATAL ERROR - dimension mismatch
```

### Example 2: Repeat Notation Error

```mcnp
c WRONG: fill=0:0 0:0 0:9 with "100 9R"
c Need: 1×1×10 = 10 elements
c "100 9R" gives: 10 elements (correct!)
c But user might think "9R" means 9 copies (WRONG - it means 9 repeats = 10 total)
```

### Example 3: Negative Index Error

```mcnp
c WRONG: fill=-5:5 0:0 0:0, user thinks "5 elements"
c CORRECT: (-5)-(5)+1 = 11 elements (includes -5,-4,-3,-2,-1,0,1,2,3,4,5)
c ALWAYS COUNT ZERO when range crosses zero!
```

---

## Quick Reference Table

| Lattice Type | Surface | Pitch Formula | Fill Order | Common Use |
|--------------|---------|---------------|------------|------------|
| LAT=1 | RPP | Element spacing | K, J, I | PWR, BWR, vertical stacks |
| LAT=2 | RHP | R × √3 | K, J, I | HTGR, fast reactors, CANDU |

**Both use same K,J,I index ordering!**

---

**Use this reference** when building complex reactor lattices to ensure correct dimensions and patterns.
