# TRISO Fuel Reference - Supplemental

**Purpose**: TRISO-specific lattice patterns as ONE example of complex reactor fuel

**Note**: TRISO patterns are supplemental. The lattice concepts apply to ALL complex reactor models (PWR, BWR, HTGR, fast reactors, etc.)

**Source**: Based on AGR-1_Technical_Analysis_Report.md and QUICK_REFERENCE_TRISO_SPECS.md

---

## TRISO Particle Specifications (AGR-1)

### Geometry

```
Layer          Material    Thickness   Outer Radius
-----------------------------------------------------
Kernel         UO2         350 μm dia  175 μm
Buffer         Porous C    100 μm      275 μm
IPyC           PyC         40 μm       315 μm
SiC            SiC         35 μm       350 μm
OPyC           PyC         40 μm       390 μm
Total diameter                         780 μm
```

### Densities

```
UO2 kernel:       10.4-10.8 g/cm³
Buffer (porous):  0.95-1.10 g/cm³
IPyC:            1.85-1.90 g/cm³
SiC:             3.18-3.21 g/cm³
OPyC:            1.85-1.90 g/cm³
Matrix (SiC):    1.60-1.75 g/cm³
```

---

## TRISO Lattice Hierarchy (AGR-1 Model)

### Full 6-Level Hierarchy

```
Level 1: TRISO Particle (u=1114)
   └─ 5 concentric spherical shells + matrix filler

Level 2: Matrix Cell (u=1115)
   └─ Graphite matrix without particle (for corners)

Level 3: Particle Lattice (u=1116) - LAT=1 rectangular
   ├─ 15×15×1 array (225 positions)
   └─ Circular packing: ~169 particles + ~56 matrix

Level 4: Matrix End Caps (u=1117)
   └─ Top/bottom graphite caps

Level 5: Compact Stack (u=1110) - LAT=1 rectangular
   ├─ 1×1×31 vertical array
   └─ Pattern: 3 caps + 25 fuel + 3 caps

Level 6: Capsule/Global
   └─ Stack placement with transformations
```

### Efficiency Calculation

```
Explicit modeling:
  ~4,225 TRISO particles per compact
  × 25 compacts per stack
  × 12 stacks per capsule
  = ~1,267,500 particles

Using lattices:
  ~150 cell definitions total
  = 8,450× reduction in input size
```

---

## TRISO Particle Cell Definitions

### Complete 5-Layer TRISO (u=1114)

```mcnp
c TRISO coated particle (AGR-1 specifications)
c
1  1 -10.8  -1      u=1114  imp:n=1  vol=2.24e-5  $ UO2 kernel (350 μm dia)
2  2 -0.98   1  -2  u=1114  imp:n=1  vol=6.71e-5  $ Buffer (100 μm)
3  3 -1.85   2  -3  u=1114  imp:n=1  vol=2.45e-5  $ IPyC (40 μm)
4  4 -3.20   3  -4  u=1114  imp:n=1  vol=2.90e-5  $ SiC (35 μm)
5  5 -1.86   4  -5  u=1114  imp:n=1  vol=2.65e-5  $ OPyC (40 μm)
6  6 -1.70   5      u=1114  imp:n=1  vol=3.11e-4  $ Matrix filler

c Surfaces (all spheres centered at particle origin)
1  so  0.01750  $ Kernel:  350 μm / 2 = 175 μm = 0.01750 cm
2  so  0.02750  $ Buffer:  +100 μm    = 275 μm = 0.02750 cm
3  so  0.03150  $ IPyC:    +40 μm     = 315 μm = 0.03150 cm
4  so  0.03500  $ SiC:     +35 μm     = 350 μm = 0.03500 cm
5  so  0.03900  $ OPyC:    +40 μm     = 390 μm = 0.03900 cm

c Materials
m1   92235.80c 0.19908  92238.80c 0.80092  8016.80c 2.0000  $ 19.7% enriched UO2
m2   6000.80c 1.0                                           $ Buffer carbon
mt2  grph.18t                                               $ 600K graphite
m3   6000.80c 1.0                                           $ IPyC
mt3  grph.18t
m4   6000.80c 0.50  14028.80c 0.50                         $ SiC (stoichiometric)
m5   6000.80c 1.0                                           $ OPyC
mt5  grph.18t
m6   6012.00c 0.9890  6013.00c 0.0110                      $ Matrix graphite
mt6  grph.18t
```

### Matrix-Only Cell (u=1115)

```mcnp
c Graphite matrix cell without TRISO (for corners of lattice)
c
10  6 -1.70  -10  u=1115  imp:n=1  vol=3.93e-4  $ SiC matrix

10  so  0.03900  $ Same outer radius as TRISO

c Material (same as m6 above)
```

---

## Particle Lattice (15×15 Circular Packing)

### Lattice Cell Definition (u=1116)

```mcnp
c 15×15 particle lattice approximating cylindrical compact
c fill=-7:7 -7:7 0:0 → 225 total positions
c ~169 particles (u=1114) + ~56 matrix filler (u=1115)
c
20  0  -20  u=1116  lat=1  imp:n=1  fill=-7:7 -7:7 0:0
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115

c Lattice bounding surface (RPP for LAT=1)
c Must contain 15 × 15 array with 780 μm pitch
c 15 × 0.078 cm = 1.17 cm extent
20  rpp  -0.5865 0.5865 -0.5865 0.5865 -0.048 0.048

c Note: RPP z-extent is small (1 layer of particles)
c This lattice gets repeated vertically in compact stack
```

### Circular Packing Pattern Analysis

```
Corner counts (u=1115 matrix):
  Row 1: 6 matrix cells
  Row 2: 4 matrix cells
  Row 3: 2 matrix cells
  Row 4: 2 matrix cells
  Row 5: 1 matrix cell
  (symmetric for bottom half)

Center counts (u=1114 particles):
  Row 7-9: 15 particles each (full rows)
  Row 6,10: 14 particles each
  Row 5,11: 14 particles each
  (symmetric)

Total:
  u=1114 (particles): ~169
  u=1115 (matrix):     ~56
  TOTAL: 225 ✓
```

---

## Compact Stack (1×1×31)

### Vertical Stack with Repeat Notation (u=1110)

```mcnp
c Fuel compact stack: 25 fuel compacts + 6 matrix caps
c fill=0:0 0:0 -15:15 → 1×1×31 = 31 elements
c
40  0  -40  u=1110  lat=1  imp:n=1  fill=0:0 0:0 -15:15
     1117 2R 1116 24R 1117 2R

c Breakdown:
c   1117 2R  = 3 graphite matrix caps (bottom)
c   1116 24R = 25 fuel compacts (particle lattices)
c   1117 2R  = 3 graphite matrix caps (top)
c   Total: 3 + 25 + 3 = 31 ✓

c Stack bounding surface
c 1 × 1 × 31 array with 0.492 cm height per element
40  rpp  -0.635 0.635 -0.635 0.635 -7.62 7.62
```

### Matrix End Caps (u=1117)

```mcnp
c Solid graphite end caps (top/bottom of stack)
c
30  6 -1.70  -30  u=1117  imp:n=1  vol=0.788  $ Graphite

30  rpp  -0.635 0.635 -0.635 0.635 -0.246 0.246
```

---

## Key Lessons from TRISO Model

### 1. Circular Packing in Rectangular Lattice

**Technique**: Use LAT=1 (rectangular) to approximate cylindrical geometry

**Benefit**: Avoids complex curved lattice boundaries

**Applicability**: ANY cylindrical arrangement (fuel pellets, detector arrays, etc.)

### 2. Repeat Notation for Long Arrays

**Usage**: `1117 2R 1116 24R 1117 2R` instead of 31 separate numbers

**Benefit**: Compact, readable, maintainable

**Applicability**: ANY vertical stack or repeated pattern

### 3. Multi-Level Efficiency

**6 levels** allows modeling **millions** of particles with **hundreds** of cells

**Applicability**: Any hierarchical reactor structure

---

## TRISO vs. General Reactor Modeling

### TRISO-Specific Features

- Spherical particle geometry (5 concentric shells)
- Circular packing in rectangular lattice
- Vertical stacking with repeat notation

### Universal Features (Apply to ALL Reactors)

✅ **FILL dimension calculation**: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

✅ **Repeat notation**: nR = (n+1) total copies

✅ **Index ordering**: K, J, I (outermost to innermost)

✅ **Multi-level hierarchies**: Up to 6 practical levels

✅ **Bottom-up definition**: Child before parent

✅ **Both LAT=1 and LAT=2**: Can be mixed in same model

**The lattice concepts are universal** - TRISO is just one application!

---

## Other Fuel Types Using Same Concepts

### PWR/BWR Fuel Pins

```
Level 1: Fuel pellet stack (u=100)
Level 2: Pin bundle (u=200, LAT=1, 17×17)
Level 3: Core (u=300, assembly array)
```

### Fast Reactor MOX Fuel

```
Level 1: MOX pin (u=100)
Level 2: Pin bundle (u=200, LAT=2 hexagonal, 271 pins)
Level 3: Core (u=300, LAT=2 hexagonal, assemblies)
```

### CANDU Bundle

```
Level 1: Fuel element (u=100)
Level 2: Bundle ring (u=200, LAT=1 circular)
Level 3: Bundle stack (u=300, LAT=1 vertical)
```

**Same lattice mechanics, different applications!**

---

**This reference shows TRISO as ONE example**. Use the same techniques for ANY complex reactor fuel.
