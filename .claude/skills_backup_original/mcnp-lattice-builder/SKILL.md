---
category: E
name: mcnp-lattice-builder
description: Build lattice and repeated structure geometries using U/LAT/FILL cards for fuel assemblies, detector arrays, and complex periodic geometries
version: 1.0.0
auto_activate: true
activation_keywords:
  - lattice
  - repeated structure
  - FILL
  - LAT
  - universe
  - fuel assembly
  - pin cell
  - hexagonal lattice
  - rectangular lattice
  - nested lattice
dependencies:
  - mcnp-input-builder
  - mcnp-geometry-builder
related_skills:
  - mcnp-mesh-builder
  - mcnp-burnup-builder
output_formats:
  - MCNP input cards (U/LAT/FILL/TRCL)
  - Lattice specification
  - Universe definitions
---

# mcnp-lattice-builder

**Purpose**: Build lattice and repeated structure geometries using universe/lattice/fill methodology to efficiently model fuel assemblies, detector arrays, and complex periodic geometries without duplicating cell definitions.

## What Are Lattices and Universes?

**Universe** = Self-contained geometry block that can be referenced by number and replicated multiple times.

**Lattice** = Ordered array of universes filling a parent cell in a regular pattern.

**Fill** = Mechanism to place universe(s) into a cell, with optional transformations.

### Why Use Lattices?

**Without lattices** (direct geometry):
- 100 fuel pins = 100 cell definitions
- Difficult to modify pin design (change 100 cells)
- Error-prone for large arrays

**With lattices** (universe/fill):
- 100 fuel pins = 1 pin universe × 10×10 lattice
- Modify pin design once in universe definition
- Automatic spatial arrangement

## Core Concepts

### Universe (U)

```
c Cell definition with universe assignment
1  1  -10.5  -1  U=5  IMP:N=1   $ Pin fuel (universe 5)
2  2  -6.5    1 -2  U=5  IMP:N=1   $ Pin clad (universe 5)
3  3  -1.0    2  U=5  IMP:N=1   $ Pin coolant (universe 5)
```

**Key points**:
- Universe 0 = main problem geometry (default for cells without U keyword)
- Universes 1-99999999 = available for repeated structures
- All cells in a universe must be contained (no infinite cells except background)
- Universe coordinate system starts at (0,0,0) - use TRCL to position

### Lattice (LAT)

```
c Lattice cell
10  0  -10  LAT=1  U=100  FILL=5  IMP:N=1   $ Rectangular lattice
```

**LAT values**:
- `LAT=1` = Rectangular (Cartesian) lattice in (x,y,z)
- `LAT=2` = Hexagonal lattice (hexprism elements)
- `LAT=5` = 3D hexagonal (SCALE-like)

**Lattice element**:
- Surface -10 defines one element of the lattice
- Must be a rectangular parallelepiped (LAT=1) or hexagonal prism (LAT=2)
- Element size sets spacing for all elements

### Fill (FILL)

**Simple fill** (same universe everywhere):
```
10  0  -10  LAT=1  U=100  FILL=5   $ All elements filled with universe 5
```

**Indexed fill** (different universes):
```
10  0  -10  LAT=1  U=100  FILL=0:2  0:2  0:0   $ 3×3 lattice, z=0
                            5 5 6
                            5 5 6
                            7 7 8
```

Format: `FILL=imin:imax jmin:jmax kmin:kmax <universe array>`
- Indices specify range of lattice positions
- Universe numbers listed in order (vary i fastest, then j, then k)

**Transformation fill**:
```
10  0  -10  FILL=5 (TR1)    $ Fill with universe 5, apply transformation TR1
```

## Decision Tree: Which Lattice Type?

```
START: Need repeated geometry?
│
├─→ YES: What shape are elements?
│   │
│   ├─→ Rectangular pins/boxes
│   │   └─→ LAT=1 (rectangular lattice)
│   │       - Fuel assemblies (square pins)
│   │       - Detector arrays
│   │       - Rectangular grid patterns
│   │
│   ├─→ Hexagonal pins
│   │   └─→ LAT=2 (hexagonal lattice)
│   │       - Hexagonal fuel assemblies
│   │       - VVER/RBMK reactors
│   │       - Honeycomb structures
│   │
│   ├─→ Complex 3D hexagonal
│   │   └─→ LAT=5 (3D hexagonal, SCALE-like)
│   │       - Advanced reactor designs
│   │
│   ├─→ Irregular or non-periodic
│   │   └─→ Use multiple FILL statements (not LAT)
│   │       - Ad-hoc assemblies
│   │       - Scattered objects
│   │
│   └─→ Nested lattices (lattice within lattice)
│       └─→ Multi-level universe hierarchy
│           - Fuel pins → Fuel assembly → Core
│           - Detector array → Module → System
│
└─→ NO: Use standard cell definitions (see mcnp-geometry-builder)
```

## Rectangular Lattice (LAT=1)

### Basic Rectangular Lattice

**Step-by-step construction**:

**1. Define pin universe**:
```
c --- Universe 1: Standard fuel pin ---
1  1  -10.5  -1     U=1  IMP:N=1   $ Fuel (r < 0.4 cm)
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad (0.4 < r < 0.5)
3  3  -1.0    2     U=1  IMP:N=1   $ Coolant (r > 0.5)

c --- Surfaces for pin universe ---
1  CZ  0.4   $ Fuel radius
2  CZ  0.5   $ Clad outer radius
```

**2. Define lattice element**:
```
c --- Surface for lattice element (1.26 cm pitch) ---
10  RPP  -0.63  0.63  -0.63  0.63  -100  100   $ 1.26×1.26 cm square, 200 cm tall
```

**3. Create lattice cell**:
```
c --- Lattice cell (fills region -100) ---
100  0  -10  LAT=1  U=10  FILL=1  IMP:N=1   $ Rectangular lattice of universe 1
```

**4. Fill lattice into main geometry**:
```
c --- Main geometry cells ---
1000  0  -100  FILL=10  IMP:N=1   $ Fill region with lattice universe 10
1001  0   100  IMP:N=0             $ Outside world (kill particles)

c --- Main geometry surface ---
100  RPP  -10  10  -10  10  -100  100   $ 20×20×200 cm box
```

**Result**: Infinite array of fuel pins with 1.26 cm pitch, truncated to 20×20 cm.

### Indexed Fill (Different Universes)

**Example**: 3×3 assembly with control rod in center.

**Universe definitions**:
```
c --- Universe 1: Fuel pin ---
1  1  -10.5  -1     U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -1.0    2     U=1  IMP:N=1   $ Coolant

c --- Universe 2: Control rod ---
10  4  -2.3   -1     U=2  IMP:N=1   $ B4C absorber
11  2  -6.5    1 -2  U=2  IMP:N=1   $ Clad
12  3  -1.0    2     U=2  IMP:N=1   $ Coolant

c --- Universe 3: Guide tube (empty) ---
20  3  -1.0    -2  U=3  IMP:N=1   $ Coolant only (no fuel)
21  3  -1.0     2  U=3  IMP:N=1   $ Coolant outside

c --- Surfaces (shared by all universes) ---
1  CZ  0.4   $ Fuel/absorber radius
2  CZ  0.5   $ Clad outer radius
```

**Lattice with indexed fill**:
```
c --- Lattice element ---
10  RPP  -0.63  0.63  -0.63  0.63  -100  100

c --- Lattice cell with indexed fill ---
100  0  -10  LAT=1  U=10  FILL=0:2  0:2  0:0  IMP:N=1
                            1 1 1    $ j=0 row (bottom)
                            1 2 3    $ j=1 row (middle): fuel, control rod, guide tube
                            1 1 1    $ j=2 row (top)
```

**Layout** (viewed from above, +Y up):
```
    i=0  i=1  i=2
j=2  1    1    1     (fuel  fuel  fuel)
j=1  1    2    3     (fuel  ctrl  guide)
j=0  1    1    1     (fuel  fuel  fuel)
```

### Partial Lattice (Truncation)

**Problem**: Lattice extends infinitely; how to limit extent?

**Solution**: Place lattice inside bounding surface.

**Example**: 5×5 fuel assembly in square shroud:

```
c --- 5×5 lattice ---
100  0  -10  LAT=1  U=10  FILL=0:4  0:4  0:0  IMP:N=1
                            1 1 1 1 1
                            1 1 1 1 1
                            1 1 2 1 1   $ Control rod at (2,2)
                            1 1 1 1 1
                            1 1 1 1 1

c --- Assembly shroud (limits lattice) ---
1000  0  -100  FILL=10  IMP:N=1    $ Lattice fills region -100
1001  5  -8.0   100 -101  IMP:N=1    $ Shroud
1002  0   101  IMP:N=0               $ Outside world

c --- Surfaces ---
10   RPP  -0.63  0.63  -0.63  0.63  -100  100   $ Lattice element
100  RPP  -3.15  3.15  -3.15  3.15  -100  100   $ 5×5 array (5 × 1.26 = 6.3 cm)
101  RPP  -4     4     -4     4     -101  101   $ Shroud outer
```

**Result**: Lattice fills only the region inside surface 100 (5×5 pins). Shroud surrounds assembly.

## Hexagonal Lattice (LAT=2)

### Hexagon Orientation

LAT=2 hexagons point **UP** (flat sides on left/right):
```
       /\
      /  \
     |    |
     |    |
      \  /
       \/
```

**Indexing** (i,j coordinates):
- i = column (horizontal, left-right)
- j = row (vertical, but offset every other column)
- Odd columns (i=1,3,5,...) are offset +0.5 in j direction

### Basic Hexagonal Lattice

**Step 1: Define pin universe** (same as rectangular):
```
c --- Universe 1: Fuel pin ---
1  1  -10.5  -1     U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -1.0    2     U=1  IMP:N=1   $ Coolant

1  CZ  0.4
2  CZ  0.5
```

**Step 2: Define hexagonal lattice element**:
```
c --- Hexagonal prism element (pitch = 1.26 cm) ---
10  RHP  0 0 -100  0 0 200  0.73   $ Hexagonal prism (apothem = pitch/√3)
```

Where:
- `0 0 -100` = Base center (z=-100)
- `0 0 200` = Axis vector (height = 200 cm)
- `0.73` = Apothem (perpendicular distance from center to flat side)
  - For pitch P: apothem = P / √3 ≈ P / 1.732
  - For P=1.26 cm: apothem = 1.26/1.732 = 0.728 cm

**Step 3: Create hexagonal lattice**:
```
c --- Hexagonal lattice ---
100  0  -10  LAT=2  U=10  FILL=1  IMP:N=1
```

**Step 4: Fill into main geometry**:
```
c --- Truncate lattice with cylinder ---
1000  0  -100  FILL=10  IMP:N=1
1001  0   100  IMP:N=0

100  RCC  0 0 -100  0 0 200  10   $ Cylinder, radius 10 cm
```

### Indexed Hexagonal Fill

**Example**: 7-pin hexagonal cluster (1 center + 6 surrounding).

```
c --- Hexagonal lattice with indexed fill ---
100  0  -10  LAT=2  U=10  FILL=-1:1  -1:1  0:0  IMP:N=1
                                1 2 1    $ j=-1 row
                                2 1 2    $ j=0 row (center)
                                1 2 1    $ j=1 row
```

**Layout** (hexagonal indexing):
```
       j=1:    1   2   1
           /\      /\      /\
          /  \    /  \    /  \
       j=0:  2   1   2
          \  /    \  /    \  /
           \/      \/      \/
       j=-1:   1   2   1

      i=-1   i=0   i=1
```

Where:
- Universe 1 = outer fuel pins (6 pins)
- Universe 2 = center control rod (1 pin)

### Hexagonal Assembly with Guide Tubes

**VVER-style 19-pin hexagonal assembly**:

```
c --- Universes ---
c U=1: Fuel pin
c U=2: Guide tube
c U=3: Instrumentation tube

c --- Hexagonal lattice element ---
10  RHP  0 0 -100  0 0 200  0.56   $ Pitch = 0.97 cm

c --- 19-pin hexagonal lattice ---
100  0  -10  LAT=2  U=10  FILL=-2:2  -2:2  0:0  IMP:N=1
                                  1  1  1  1  1   $ j=-2
                                1  1  1  2  1     $ j=-1
                              1  1  3  1  1       $ j=0 (center: instrumentation)
                                1  2  1  1  1     $ j=1
                                  1  1  1  1  1   $ j=2
                           i=-2 i=-1 i=0 i=1 i=2
```

## Nested Lattices (Multi-Level Hierarchy)

**Purpose**: Model complex systems with multiple scales (e.g., pins → assemblies → core).

### Example: Reactor Core (3 Levels)

**Level 1: Pin cell universe**
```
c --- Universe 1: Fuel pin ---
1  1  -10.5  -1     U=1  IMP:N=1
2  2  -6.5    1 -2  U=1  IMP:N=1
3  3  -1.0    2     U=1  IMP:N=1

1  CZ  0.4
2  CZ  0.5
```

**Level 2: Assembly lattice**
```
c --- 17×17 fuel assembly (universe 10) ---
10  RPP  -0.63  0.63  -0.63  0.63  -100  100   $ Pin cell element

100  0  -10  LAT=1  U=10  FILL=0:16  0:16  0:0  IMP:N=1
                            1 1 1 ... (17×17 = 289 entries)

c --- Assembly in shroud (universe 20) ---
1000  0  -100  FILL=10  IMP:N=1   $ Assembly lattice
1001  5  -8.0   100 -101  IMP:N=1   $ Shroud
1002  3  -1.0   101  U=20  IMP:N=1   $ Water outside shroud

100  RPP  -10.71  10.71  -10.71  10.71  -100  100   $ 17×1.26 = 21.42 cm
101  RPP  -11     11     -11     11     -101  101
```

**Level 3: Core lattice**
```
c --- 15×15 core lattice (main geometry) ---
10000  RPP  -11  11  -11  11  -101  101   $ Assembly element

100000  0  -10000  LAT=1  FILL=0:14  0:14  0:0  IMP:N=1
                            20 20 20 ... (15×15 = 225 assemblies)

c --- Core in barrel ---
1000000  0  -1000000  FILL=100000  IMP:N=1   $ Core lattice
1000001  6  -7.8   1000000 -1000001  IMP:N=1   $ Barrel
1000002  3  -1.0   1000001  U=0  IMP:N=1   $ Moderator outside barrel
1000003  0  1000002  IMP:N=0   $ Outside world

1000000  RPP  -165  165  -165  165  -101  101   $ 15×22 = 330 cm
1000001  RPP  -175  175  -175  175  -105  105
1000002  RPP  -200  200  -200  200  -110  110
```

**Hierarchy**:
```
Universe 0 (main)
  └─ Universe 100000 (core lattice)
       └─ Universe 20 (assembly + shroud)
            └─ Universe 10 (pin lattice)
                 └─ Universe 1 (pin cell)
```

## Transformations with Fill (TRCL)

### Rotating/Translating Filled Universe

**Syntax**:
```
CELL  0  -SURF  FILL=<u> (<TRn>)   $ Apply transformation TRn to universe u
```

or inline:
```
CELL  0  -SURF  FILL=<u> (x y z  o1 o2 o3  ...)   $ Inline transformation
```

**Example**: Rotate fuel assembly 45°:

```
c --- Define transformation ---
TR1  0 0 0   45 45 90   135 45 90   90 90 0   $ 45° rotation about Z

c --- Fill with rotation ---
1000  0  -100  FILL=10 (TR1)  IMP:N=1
```

**Use cases**:
- Angled assemblies
- Rotated detectors
- Off-axis positioning

### Multiple Fills with Transformations

**Example**: Four fuel assemblies at corners, each rotated differently:

```
c --- Assembly 1 (bottom-left, no rotation) ---
1001  0  -101  FILL=10  IMP:N=1

c --- Assembly 2 (bottom-right, 90° rotation) ---
1002  0  -102  FILL=10 (TR2)  IMP:N=1

c --- Assembly 3 (top-left, 180° rotation) ---
1003  0  -103  FILL=10 (TR3)  IMP:N=1

c --- Assembly 4 (top-right, 270° rotation) ---
1004  0  -104  FILL=10 (TR4)  IMP:N=1

c --- Transformations ---
TR2  10 0 0   0 90 90   90 0 90   90 90 180   $ Translate +10 cm in X, rotate 90°
TR3  0 10 0   90 0 90   0 90 0   180 90 90   $ Translate +10 cm in Y, rotate 180°
TR4  10 10 0  90 90 0   0 90 90   270 90 90   $ Translate to (+10,+10), rotate 270°
```

## Lattice Tallies (FS/SD Cards)

### Tally in Specific Lattice Element

**Problem**: Want flux in one specific pin, not whole lattice.

**Solution**: Use FS (tally segment) card.

**Example**: F4 tally in fuel region of pin at (i=5, j=5):

```
c --- Cell-averaged flux in all fuel ---
F4:N  1   $ Cell 1 = fuel (universe 1)

c --- Segment by lattice indices ---
FS4  -100 10   $ Cell 100 = lattice cell, surface 10 = lattice element

c --- Tally only (i=5, j=5, k=0) ---
c This requires TALLYX subroutine or FU card
FU4  5 5 0   $ User bin for (i,j,k) = (5,5,0)
```

**Advanced**: Use TALLYX subroutine to bin by lattice index (see User Manual Chapter 5.9.17).

### Volume Normalization for Lattice Cells

**Problem**: Lattice cell volumes are often unknown (MCNP can't calculate repeated structure volumes).

**Solution**: Manually specify volumes with SD card.

**Example**:
```
c --- Fuel pin (universe 1) ---
1  1  -10.5  -1  U=1  IMP:N=1   $ Fuel

c --- Tally ---
F4:N  1   $ Flux in fuel

c --- Volume (fuel volume per pin) ---
SD4  0.50265   $ π × 0.4² = 0.50265 cm³

c OR: Let MCNP calculate (for non-lattice cells)
SD4  1   $ Default (MCNP calculates volume)
```

## Common Use Cases

### Use Case 1: PWR 17×17 Fuel Assembly

```
c ============================================================
c PWR 17×17 Assembly with Guide Tubes and Instrument Tube
c ============================================================

c --- Material definitions ---
M1  92235 -0.04  92238 -0.96  8016 -0.12   $ UO2 fuel (4% enrichment)
M2  40000 1.0                                $ Zircaloy clad
M3  1001 2  8016 1                           $ H2O coolant
M4  5010 0.2  5011 0.8  6000 0.1             $ B4C absorber

c --- Universe 1: Standard fuel pin ---
1  1  -10.5  -1     U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -1.0    2     U=1  IMP:N=1   $ Coolant

c --- Universe 2: Guide tube (for control rod) ---
11  3  -1.0   -2  U=2  IMP:N=1   $ Coolant inside
12  2  -6.5    2 -3  U=2  IMP:N=1   $ Guide tube
13  3  -1.0    3  U=2  IMP:N=1   $ Coolant outside

c --- Universe 3: Instrumentation tube ---
21  3  -1.0   -4  U=3  IMP:N=1   $ Air/coolant inside
22  2  -6.5    4 -5  U=3  IMP:N=1   $ Instrument tube
23  3  -1.0    5  U=3  IMP:N=1   $ Coolant outside

c --- Pin surfaces ---
1  CZ  0.4096   $ Fuel radius
2  CZ  0.4178   $ Clad inner
3  CZ  0.6147   $ Guide tube outer
4  CZ  0.5715   $ Instrument tube inner
5  CZ  0.6147   $ Instrument tube outer

c --- Lattice element (1.26 cm pitch) ---
10  RPP  -0.63  0.63  -0.63  0.63  -200  200

c --- 17×17 Lattice (universe 10) ---
100  0  -10  LAT=1  U=10  FILL=0:16  0:16  0:0  IMP:N=1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 1 1 1 2 1 1 2 1 1 2 1 1 1 1 1
                            1 1 1 2 1 1 1 1 1 1 1 1 1 2 1 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 2 1 1 2 1 1 2 1 1 2 1 1 2 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 2 1 1 2 1 1 3 1 1 2 1 1 2 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 2 1 1 2 1 1 2 1 1 2 1 1 2 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 1 2 1 1 1 1 1 1 1 1 1 2 1 1 1
                            1 1 1 1 1 2 1 1 2 1 1 2 1 1 1 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
                            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

c --- Assembly in shroud (main geometry, universe 0) ---
1000  0  -100  FILL=10  IMP:N=1   $ Lattice
1001  5  -8.0   100 -101  IMP:N=1   $ Shroud
1002  3  -1.0   101 -102  IMP:N=1   $ Water outside
1003  0   102  IMP:N=0   $ Outside world

c --- Assembly surfaces ---
100  RPP  -10.71  10.71  -10.71  10.71  -200  200   $ 17×1.26 = 21.42 cm
101  RPP  -11     11     -11     11     -201  201   $ Shroud
102  RPP  -50     50     -50     50     -250  250   $ Problem boundary
```

### Use Case 2: Hexagonal VVER Assembly

```
c ============================================================
c VVER-1000 Hexagonal Assembly (19 pins)
c ============================================================

c --- Materials ---
M1  92235 -0.036  92238 -0.964  8016 -0.12   $ UO2 (3.6% enrichment)
M2  40000 1.0                                 $ Zr+1%Nb clad
M3  1001 2  8016 1  5010 1e-5                 $ H2O + boron

c --- Universe 1: Fuel pin ---
1  1  -10.5  -1     U=1  IMP:N=1   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1   $ Clad
3  3  -0.7    2     U=1  IMP:N=1   $ Coolant

c --- Universe 2: Central pin (higher enrichment) ---
11  1  -10.5  -1     U=2  IMP:N=1   $ Fuel (different enrichment in M11)
12  2  -6.5    1 -2  U=2  IMP:N=1   $ Clad
13  3  -0.7    2     U=2  IMP:N=1   $ Coolant

c --- Pin surfaces ---
1  CZ  0.386   $ Fuel radius
2  CZ  0.455   $ Clad outer

c --- Hexagonal element (pitch 1.23 cm, apothem = 1.23/√3 = 0.71 cm) ---
10  RHP  0 0 -190  0 0 380  0.71

c --- 19-pin hexagonal lattice ---
100  0  -10  LAT=2  U=10  FILL=-2:2  -2:2  0:0  IMP:N=1
                                  1  1  1  1  1   $ j=-2
                                1  1  1  1  1     $ j=-1
                              1  1  2  1  1       $ j=0 (center: enriched)
                                1  1  1  1  1     $ j=1
                                  1  1  1  1  1   $ j=2

c --- Assembly in hexagonal shroud ---
1000  0  -100  FILL=10  IMP:N=1   $ Lattice
1001  4  -7.8   100 -101  IMP:N=1   $ Steel shroud
1002  3  -0.7   101  IMP:N=1   $ Coolant outside
1003  0   102  IMP:N=0

100  RHP  0 0 -190  0 0 380  3.8   $ Hexagon containing lattice (apothem ~3.8 cm)
101  RHP  0 0 -191  0 0 382  4.0   $ Shroud outer
102  RCC  0 0 -200  0 0 400  10    $ Cylindrical boundary
```

### Use Case 3: Nested Lattice (Assembly in Core)

See "Nested Lattices" section above for complete 3-level example (pin → assembly → core).

## Troubleshooting

### Problem: "Lost particle" errors in lattice

**Cause**: Universe cells not fully contained (leak at boundaries).

**Fix**: Ensure all cells in universe are bounded. Add background cell if needed.

**Example**:
```
c WRONG: Cell 3 extends to infinity
3  3  -1.0  2  U=1  IMP:N=1   $ Coolant (r > 0.5, unbounded)

c CORRECT: Cell 3 bounded by lattice element
3  3  -1.0  2 -10  U=1  IMP:N=1   $ Coolant (0.5 < r < 0.63)
4  3  -1.0   10  U=1  IMP:N=1   $ Coolant outside pin (r > 0.63)
```

### Problem: FILL index out of range

**Cause**: Lattice FILL indices don't match element count.

**Example**:
```
c WRONG: 3×3 lattice but only 2×2 indices
100  0  -10  LAT=1  U=10  FILL=0:2  0:2  0:0   $ Expecting 3×3 = 9 values
                            1 1      $ Only 4 values!
                            1 1

c CORRECT: Provide full 3×3 array
100  0  -10  LAT=1  U=10  FILL=0:2  0:2  0:0
                            1 1 1
                            1 1 1
                            1 1 1
```

### Problem: Lattice spacing incorrect (gaps between pins)

**Cause**: Lattice element size doesn't match pitch.

**Fix**: Verify element surface matches intended pitch.

**Example**:
```
c Pitch = 1.26 cm (square)
c Element must be 1.26×1.26 cm

c WRONG: Element too small (1.0×1.0)
10  RPP  -0.5  0.5  -0.5  0.5  -100  100   $ Gaps appear

c CORRECT: Element matches pitch
10  RPP  -0.63  0.63  -0.63  0.63  -100  100   $ ±0.63 = 1.26 cm
```

### Problem: Can't tally in specific lattice element

**Solution**: Use TALLYX subroutine or FS card with lattice indices.

**Example** (FS card approach):
```
c Tally flux in fuel of pin at (i=8, j=8)
F4:N  1   $ Fuel cell (universe 1)
FS4  -100 10   $ Lattice 100, element surface 10
C4  0 0 8*8   $ Comment showing indices (not functional - needs TALLYX)
```

**Note**: For precise lattice element tallying, use TALLYX (Fortran subroutine). See User Manual §5.9.17.

### Problem: Hexagonal lattice orientations wrong

**Cause**: Hexagon orientation (LAT=2 points up).

**Fix**: Verify hexprism orientation and indexing.

**Reminder**: LAT=2 hexagons have flat sides on LEFT/RIGHT, points UP/DOWN.

### Problem: Nested lattice levels confused

**Fix**: Draw hierarchy diagram.

**Example**:
```
c Universe map:
c U=0: Main geometry (core barrel, moderator)
c U=10: Assembly lattice (17×17 pins)
c U=1: Fuel pin
c U=2: Guide tube
c U=20: Assembly + shroud (contains U=10)
c U=100: Core lattice (15×15 assemblies, contains U=20)
```

## Integration with Other Skills

### With mcnp-burnup-builder

Burn specific pins in lattice:
```
c Burn only fuel pins (universe 1)
BURN TIME=100 MAT=1 MATVOL=0.503   $ 0.503 cm³ per fuel pin
```

### With mcnp-mesh-builder

Superimpose mesh over lattice:
```
FMESH14:N GEOM=XYZ
          ORIGIN=-10.71  -10.71  -100
          IMESH=10.71  IINTS=17   $ Match lattice pitch
          JMESH=10.71  JINTS=17
          KMESH=100  KINTS=100
          OUT=xdmf
```

### With mcnp-geometry-builder

Combine lattices with complex external geometry:
```
c Core lattice (universe 100)
c Pressure vessel (main geometry)
c Biological shield (main geometry)
```

## Best Practices

1. **Universe numbering**: Use systematic scheme (U=1-99 for pins, U=100-199 for assemblies, U=1000+ for core)
2. **Always bound universes**: Ensure all cells in universe are contained (no infinite cells except background)
3. **Verify pitch**: Double-check lattice element size matches intended spacing
4. **Test single element**: Model one lattice element first, verify geometry, then create full lattice
5. **Use comments**: Label universe purpose and lattice indices
6. **Volume cards**: Provide SD volumes for lattice cells (MCNP can't calculate repeated structure volumes)
7. **Nested lattices**: Draw hierarchy diagram before building
8. **Hexagonal**: Remember LAT=2 hexagons point UP (flat sides left/right)
9. **Transformations**: Use TRCL carefully; verify with geometry plots
10. **Lost particles**: Add background cells in universes to catch leaks
11. **Programmatic Lattice Generation**:
    - For automated lattice construction and FILL array generation, see: `mcnp_lattice_builder.py`
    - Useful for complex lattice patterns, parametric lattice studies, and large-scale repeated structures

## References

- **User Manual**: Chapter 5.5 - Geometry Data Cards (U/LAT/FILL)
- **Examples**: Chapter 10.1 - Geometry Examples (Repeated Structures)
- **COMPLETE_MCNP6_KNOWLEDGE_BASE.md**: Lattice specification
- **Related skills**: mcnp-geometry-builder, mcnp-mesh-builder, mcnp-burnup-builder
