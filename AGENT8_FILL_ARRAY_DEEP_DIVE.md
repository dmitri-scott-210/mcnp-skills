# AGENT 8: COMPREHENSIVE DEEP DIVE - FILL ARRAYS AND LATTICE STRUCTURES

## Executive Summary

This document provides an exhaustive analysis of FILL array mechanics and lattice structures in MCNP based on examination of:
- **sdr-agr.i** (4,653 lines) - AGR-1 TRISO fuel experiment model
- **bench_*.i files** (13 files, 18,414 lines each) - ATR reactor benchmark models
- **input_definition.py** - Micro-HTGR model generation script
- Multiple validation benchmark files

**Key Finding**: These models demonstrate **MULTI-LEVEL LATTICE HIERARCHIES** with up to 4 nested levels, combining both rectangular (LAT=1) and hexagonal (LAT=2) lattices with sophisticated FILL array techniques including repeat notation and complex indexing.

---

## 1. FILL ARRAY MECHANICS - DETAILED SPECIFICATION

### 1.1 Fundamental Syntax

```
CELL_ID  0  -SURFACE  u=UNIV  lat=TYPE  fill=IMIN:IMAX JMIN:JMAX KMIN:KMAX
    UNIVERSE_LIST
```

**Critical Rules:**
1. **Dimensions MUST match exactly**: If `fill=-7:7 -7:7 0:0`, you need (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15×15×1 = 225 universe numbers
2. **Index ordering**: Arrays are filled in **K, J, I order** (rightmost varies fastest)
3. **Zero-based vs range-based**: Indices can start at any integer (positive, negative, or zero)
4. **No gaps allowed**: Every lattice position MUST be filled

### 1.2 Index Ordering - THE CRITICAL CONCEPT

**MCNP fills lattice arrays in this order: outermost K loop, middle J loop, innermost I loop**

For `fill=-1:1 -1:1 -1:1` (3×3×3 = 27 elements):

```
Position  K   J   I   Element#
--------------------------------
   1     -1  -1  -1      1
   2     -1  -1   0      2
   3     -1  -1   1      3
   4     -1   0  -1      4
   5     -1   0   0      5
   6     -1   0   1      6
   7     -1   1  -1      7
   8     -1   1   0      8
   9     -1   1   1      9
  10      0  -1  -1     10
  11      0  -1   0     11
  ...     ...  ...     ...
  27      1   1   1     27
```

**Reading the FILL array in the input file:**
- First line (elements 1-3): K=-1, J=-1, I=-1,0,1
- Second line (elements 4-6): K=-1, J=0, I=-1,0,1
- Third line (elements 7-9): K=-1, J=1, I=-1,0,1
- Fourth line (elements 10-12): K=0, J=-1, I=-1,0,1
- etc.

---

## 2. RECTANGULAR LATTICES (LAT=1)

### 2.1 Example 1: 2D Particle Lattice (15×15×1)

**Source**: sdr-agr.i, lines 22-37

```mcnp
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ Layer
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
```

**Analysis:**
- **Dimensions**: i: -7→7 (15), j: -7→7 (15), k: 0→0 (1) = **15×15×1 = 225 elements**
- **Surface 91117**: RPP bounding box for one lattice element
  ```mcnp
  91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
  ```
  Element pitch: X=0.08743 cm, Y=0.08743 cm, Z=0.1 cm

- **Universe mapping**:
  - **U=1114**: TRISO particle (5-layer coating structure)
  - **U=1115**: Matrix material (SiC)

- **Physical representation**: TRISO particles arranged in a circular pattern within a graphite compact
- **Pattern**: Circular arrangement approximated on rectangular grid (corners are matrix-only)

**Verification**: Count = 225 universe numbers (verified via grep)

### 2.2 Example 2: 1D Axial Lattice with Repeat Notation (1×1×31)

**Source**: sdr-agr.i, line 40

```mcnp
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

**Analysis:**
- **Dimensions**: i: 0→0 (1), j: 0→0 (1), k: -15→15 (31) = **1×1×31 = 31 elements**
- **Repeat notation**:
  - `1117 2R` = `1117 1117 1117` (3 elements total: first one + 2 repeats)
  - `1116 24R` = 25 copies of 1116 (first one + 24 repeats)
  - Total: 3 + 25 + 3 = 31 ✓

- **Surface 91118**: RPP bounding box for axial lattice element
  ```mcnp
  91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
  ```
  Element pitch: X=1.3 cm, Y=1.3 cm, Z=0.08743 cm

- **Universe mapping**:
  - **U=1116**: Particle lattice (from Example 2.1 above) - contains 225 TRISO particles
  - **U=1117**: Pure matrix (no particles)

- **Physical representation**: Axial stack forming a fuel compact
  - Bottom 3 layers: Matrix only (end cap)
  - Middle 25 layers: Particle lattice (active fuel region)
  - Top 3 layers: Matrix only (end cap)

**Critical insight**: This is a **NESTED LATTICE** - each element of U=1110 contains U=1116, which itself is a lattice containing 225 sub-elements.

### 2.3 Example 3: Large 1D Axial Lattice (1×1×669)

**Source**: input_definition.py, line 103

```mcnp
{n}09 0  -{n}08 u={n}8 lat=1 imp:n=1 fill=0:0 0:0 -335:335 {n}7 1R {n}6 666R {n}7 1R
```

**Analysis:**
- **Dimensions**: i: 0→0 (1), j: 0→0 (1), k: -335→335 (671) = **671 elements**
- **Repeat notation**:
  - `{n}7 1R` = 2 elements
  - `{n}6 666R` = 667 elements
  - `{n}7 1R` = 2 elements
  - Total: 2 + 667 + 2 = 671 ✓

- **Physical representation**: Tall fuel column (micro-HTGR)
  - Bottom 2 layers: Matrix
  - Middle 667 layers: Particle lattice
  - Top 2 layers: Matrix

**Performance note**: Using repeat notation is CRITICAL for large lattices - writing out 671 universe numbers would be impractical.

---

## 3. HEXAGONAL LATTICES (LAT=2)

### 3.1 Hexagonal Lattice Fundamentals

**Key differences from rectangular lattices:**
1. **Staggered rows**: Each row is offset by half a pitch in the X direction
2. **FILL array indentation**: Input file formatting shows the hexagonal pattern
3. **Coordinate system**: Uses skewed axes (60° angle between I and J)
4. **Pitch specification**: Only ONE pitch value (distance between hex centers)

### 3.2 Example 4: Assembly Hex Lattice (13×13×1)

**Source**: input_definition.py, lines 111-124

```mcnp
{n}15 0                  -{n}13 u={n}0 lat=2 imp:n=1 fill=-6:6 -6:6 0:0
     {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2
      {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}1 {n}1 {n}2 {n}2 {n}2
       {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2
        {n}2 {n}2 {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2
         {n}2 {n}2 {n}2 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}2
          {n}2 {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2
           {n}2 {n}2 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}2 {n}2
            {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2 {n}2
             {n}2 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}2 {n}2 {n}2
              {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2 {n}2 {n}2
               {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2
                {n}2 {n}2 {n}2 {n}1 {n}1 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2
                 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2
```

**Analysis:**
- **Dimensions**: i: -6→6 (13), j: -6→6 (13), k: 0→0 (1) = **13×13×1 = 169 elements**
- **Indentation pattern**: Each line is indented by one space to show hexagonal geometry
- **Surface 13**: Right hexagonal prism (RHP)
  ```mcnp
  {n}13 rhp  0 0 {h}     0 0 68     0  1.6  0
  ```
  Height: 68 cm, Hex side: 1.6 cm

- **Universe mapping**:
  - **U={n}1**: Fuel channel hex cell (with particle lattice inside)
  - **U={n}2**: Graphite hex cell (moderator blocks)
  - **U={n}3**: Coolant channel hex cell

- **Pattern interpretation**:
  - Line 1 (j=-6): All {n}2 (graphite reflector)
  - Lines 2-12: Mixed fuel, coolant, graphite in hexagonal arrangement
  - Line 13 (j=6): All {n}2 (graphite reflector)

**Index ordering for hexagonal**: Same as rectangular (K, J, I), but spatial arrangement follows hex geometry

### 3.3 Example 5: Core Hex Lattice (9×9×1)

**Source**: input_definition.py, lines 331-340

```mcnp
9901 0                  -9001   u=901 lat=2 imp:n=1 fill=-4:4 -4:4 0:0
      1001 1001 1001 1001 1001 1001 1001 1001 1001
       1001 1001 1001 1001 2430 2440 2450 2460 1001
        1001 1001 1001 2420 2190 2200 2210 2470 1001
         1001 1001 2410 2180 2050 2060 2220 2480 1001
          1001 2400 2170 2040 1001 2010 2110 2310 1001
           1001 2390 2160 2030 2020 2120 2320 1001 1001
            1001 2380 2150 2140 2130 2330 1001 1001 1001
             1001 2370 2360 2350 2340 1001 1001 1001 1001
              1001 1001 1001 1001 1001 1001 1001 1001 1001
```

**Analysis:**
- **Dimensions**: i: -4→4 (9), j: -4→4 (9), k: 0→0 (1) = **9×9×1 = 81 elements**
- **Universe mapping**:
  - **U=1001**: Reflector (outside active core)
  - **U=20XX**: Assembly positions (fuel assemblies)

- **Physical representation**: Reactor core with fuel assemblies arranged in hexagonal pattern, surrounded by reflector

---

## 4. MULTI-LEVEL LATTICE HIERARCHIES

### 4.1 Complete Hierarchy - AGR-1 Model

**4-Level Nesting Structure:**

```
LEVEL 0: Global Universe (U=0)
    └─ Contains placement cells with FILL={LEVEL 1 universe} + TRCL

LEVEL 1: Compact Lattice (U=1110, 1120, 1130, etc.)
    ├─ LAT=1, 1×1×31 axial lattice
    ├─ Surface: RPP -0.65 to 0.65 (cm) in X,Y; -0.043715 to 0.043715 (cm) in Z
    ├─ FILL=0:0 0:0 -15:15 with pattern: Matrix | Particle Lattice | Matrix
    └─ Contains: U=1116 (particle lattice) and U=1117 (matrix)

LEVEL 2: Particle Lattice (U=1116, 1126, 1136, etc.)
    ├─ LAT=1, 15×15×1 rectangular lattice
    ├─ Surface: RPP -0.043715 to 0.043715 (cm) in X,Y; -0.05 to 0.05 (cm) in Z
    ├─ FILL=-7:7 -7:7 0:0 with 225 elements
    └─ Contains: U=1114 (TRISO particle) and U=1115 (matrix)

LEVEL 3: TRISO Particle (U=1114, 1124, 1134, etc.)
    ├─ NOT a lattice (just nested cells)
    ├─ 5 concentric spherical layers + matrix:
    │   ├─ Kernel (U235O2): SO 0.017485
    │   ├─ Buffer (porous carbon): SO 0.027905
    │   ├─ IPyC (inner pyrocarbon): SO 0.031785
    │   ├─ SiC (silicon carbide): SO 0.035375
    │   ├─ OPyC (outer pyrocarbon): SO 0.039305
    │   └─ Matrix (SiC): filling to SO 1.0
    └─ Total particle radius: ~1.0 cm (including matrix)

LEVEL 4: Placement in Global Space
    ├─ Cell with FILL=1110 and TRCL=(x, y, z)
    └─ Example:
        91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Cell-by-cell example for one compact:**

```mcnp
c LEVEL 3: TRISO Particle Definition (U=1114)
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
91103 9091 -1.904  91112 -91113  u=1114                 $ IPyC
91104 9092 -3.205  91113 -91114  u=1114                 $ SiC
91105 9093 -1.911  91114 -91115  u=1114                 $ OPyC
91106 9094 -1.344  91115         u=1114                 $ SiC Matrix

c Matrix-only element (U=1115)
91107 9094 -1.344 -91116         u=1115                 $ SiC Matrix

c LEVEL 2: Particle Lattice (U=1116)
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     [... 13 more rows for total of 15 rows ...]

c Matrix for compact ends (U=1117)
91109 9094 -1.344 -91119    u=1117                 $ Matrix

c LEVEL 1: Compact Lattice (U=1110)
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

c LEVEL 0: Placement in global universe
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Total particle count in one compact:**
- Particle lattice (U=1116): ~135 positions contain U=1114 (estimated from circular pattern)
- Axial layers with particles: 25
- Total particles per compact: ~135 × 25 = ~3,375 TRISO particles

### 4.2 Complete Hierarchy - Micro-HTGR Model

**5-Level Nesting Structure:**

```
LEVEL 0: Global Universe

LEVEL 1: Core Lattice (U=901, 902, 903, 904)
    ├─ LAT=2 (hexagonal), 9×9×1
    ├─ Contains assembly positions

LEVEL 2: Assembly Lattice (U={n}0, where n=assembly number)
    ├─ LAT=2 (hexagonal), 13×13×1
    ├─ Contains fuel/coolant/graphite hex cells

LEVEL 3: Fuel Channel (U={n}1)
    ├─ Contains compact lattice U={n}8 with TRCL for centering

LEVEL 4: Compact Lattice (U={n}8)
    ├─ LAT=1 (rectangular), 1×1×669
    ├─ FILL=0:0 0:0 -335:335 with pattern: Matrix | Particle Lattice (667 layers) | Matrix

LEVEL 5: Particle Lattice (U={n}6)
    ├─ LAT=1 (rectangular), 23×23×1
    ├─ FILL=-11:11 -11:11 0:0 with 529 elements
    └─ Contains: U={n}4 (TRISO particle) and U={n}5 (matrix)
```

**Particle count in micro-HTGR fuel channel:**
- Particle lattice: ~380 particles (estimated from circular pattern in 23×23 grid)
- Axial layers: 667
- **Total: ~253,460 particles per fuel channel**
- Multiple fuel channels per assembly
- Multiple assemblies in core
- **Grand total: MILLIONS of TRISO particles in full core**

---

## 5. FILL ARRAY DIMENSION MATCHING - PITFALL AVOIDANCE

### 5.1 Common Errors and How to Avoid Them

**ERROR 1: Dimension Mismatch**

```mcnp
❌ WRONG:
1 0 -10 u=100 lat=1 fill=-1:1 -1:1 0:0
  10 11 12
  13 14 15
  16 17 18
$ Only 9 elements provided, but fill=-1:1 -1:1 0:0 requires 3×3×1=9 ✓
$ BUT if written on one line: 10 11 12 13 14 15 16 17 18 - hard to verify!

✓ CORRECT:
1 0 -10 u=100 lat=1 fill=-1:1 -1:1 0:0
  10 11 12    $ j=-1, i=-1:1
  13 14 15    $ j=0,  i=-1:1
  16 17 18    $ j=1,  i=-1:1
$ With comments showing j index, easier to verify
```

**ERROR 2: Wrong Index Range**

```mcnp
❌ WRONG:
fill=0:2 0:2 0:0
$ This requires 3×3×1=9 elements, NOT 2×2×1=4

✓ CORRECT:
fill=0:2 0:2 0:0  $ Need 9 elements: indices 0,1,2 in both i and j
  u1 u2 u3
  u4 u5 u6
  u7 u8 u9
```

**ERROR 3: Repeat Notation Miscalculation**

```mcnp
❌ WRONG:
fill=0:0 0:0 0:10  $ Need 11 elements
  10 5R 20 5R
$ This gives: 10 10 10 10 10 10 20 20 20 20 20 20 = 12 elements! FATAL ERROR

✓ CORRECT:
fill=0:0 0:0 0:10  $ Need 11 elements
  10 4R 20 5R
$ This gives: 10 10 10 10 10 (5 total) + 20 20 20 20 20 20 (6 total) = 11 ✓
```

**ERROR 4: Forgetting Negative Indices**

```mcnp
❌ WRONG (conceptually):
fill=-5:5 -5:5 0:0  $ Student thinks this is 5×5=25 elements

✓ CORRECT understanding:
fill=-5:5 -5:5 0:0  $ This is 11×11×1=121 elements!
$ Because: -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5 = 11 indices
```

### 5.2 Verification Checklist

**Before running MCNP, always verify:**

1. **Count elements needed**: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
2. **Count elements provided**:
   - Count universe numbers manually
   - Account for repeat notation: `U nR` = n+1 total copies
3. **Check index ranges**:
   - Negative to positive: include zero in count
   - Zero-based: remember (0:N) is N+1 elements, not N
4. **Verify surface dimensions match lattice pitch**

**Shell command for verification:**
```bash
# Count 4-digit universe numbers in a FILL array
sed -n 'START,ENDp' file.i | grep -o '[0-9]\{4\}' | wc -l
```

---

## 6. UNIVERSE HIERARCHY AND NUMBERING SCHEMES

### 6.1 Universe Numbering Patterns in AGR-1 Model

**Systematic numbering scheme:**

```
Capsule 1, Stack 1:
  Compact 1:
    - Particle lattice: U=1116
    - Compact lattice: U=1110
    - TRISO particle: U=1114
    - Matrix element: U=1115, 1117

  Compact 2:
    - Particle lattice: U=1126
    - Compact lattice: U=1120
    - TRISO particle: U=1124
    - Matrix element: U=1125, 1127

  Compact 3:
    - Particle lattice: U=1136
    - Compact lattice: U=1130
    - TRISO particle: U=1134
    - Matrix element: U=1135, 1137
```

**Pattern recognition:**
- First digit: Capsule number (1, 2, 3, ...)
- Second digit: Stack number (1, 2, 3)
- Third/fourth digits: Component type
  - X1X0: Compact lattice
  - X1X6: Particle lattice
  - X1X4: TRISO particle
  - X1X5, X1X7: Matrix elements

**Benefits of systematic numbering:**
1. Easy to identify which compact/stack/capsule
2. Prevents universe number conflicts
3. Enables programmatic generation
4. Facilitates troubleshooting

### 6.2 Universe Reuse Patterns

**Universe reuse is POWERFUL but requires careful management:**

**Example of CORRECT reuse:**
```mcnp
c Define TRISO particle once
10 92235.80c -10.5 -1 u=100  $ Fuel kernel
11 6000.80c   -1.0  1 -2 u=100  $ Buffer
...

c Use same particle definition in multiple lattices
20 0 -10 u=200 lat=1 fill=0:5 0:5 0:0
   100 100 100 100 100 100
   100 100 100 100 100 100
   ...

30 0 -11 u=201 lat=1 fill=0:5 0:5 0:0
   100 100 100 100 100 100  $ Same U=100 reused
   ...
```

**When NOT to reuse:**
- Different material compositions (e.g., different fuel enrichments)
- Different burnup states
- Different temperatures (if using temperature-dependent data)

**AGR-1 model approach:**
- DOES NOT reuse TRISO particle universes between compacts
- Each compact has unique particle universe (U=1114, 1124, 1134, ...)
- Reason: Each compact has different fuel composition and burnup tracking

---

## 7. LATTICE ELEMENT POSITIONING AND PITCH

### 7.1 Rectangular Lattice Element Centers

For `LAT=1` with surface RPP defined as:
```mcnp
10 rpp  XMIN XMAX  YMIN YMAX  ZMIN ZMAX
```

**Element pitch (spacing between centers):**
- X pitch: XMAX - XMIN
- Y pitch: YMAX - YMIN
- Z pitch: ZMAX - ZMIN

**Element center positions** for `fill=IMIN:IMAX JMIN:JMAX KMIN:KMAX`:

```
X_center(i) = 0.5 * (XMIN + XMAX) * i
Y_center(j) = 0.5 * (YMIN + YMAX) * j
Z_center(k) = 0.5 * (ZMIN + ZMAX) * k
```

**Example from AGR-1 particle lattice:**
```mcnp
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000

Pitch: X=0.08743 cm, Y=0.08743 cm, Z=0.1 cm

For fill=-7:7 -7:7 0:0:
  Element (i=-7, j=-7, k=0) centered at: (-0.612, -0.612, 0)
  Element (i=0, j=0, k=0) centered at:   (0, 0, 0)
  Element (i=7, j=7, k=0) centered at:   (0.612, 0.612, 0)
```

### 7.2 Hexagonal Lattice Element Centers

For `LAT=2` with surface RHP defined as:
```mcnp
SURF rhp  VX VY VZ   HX HY HZ   RX RY RZ
```
Where:
- V = base point
- H = height vector
- R = hex side vector

**Pitch**: Distance between hex centers = 2 * |R| * cos(30°) = |R| * √3

**Element center positions** follow hexagonal close-packed geometry:
```
X_center(i,j) = i * pitch + j * pitch * 0.5
Y_center(i,j) = j * pitch * (√3/2)
Z_center(k) = k * height
```

**Example from micro-HTGR:**
```mcnp
{n}13 rhp  0 0 {h}     0 0 68     0  1.6  0

Hex side: 1.6 cm
Pitch: 1.6 × √3 = 2.771 cm
Height: 68 cm

For fill=-6:6 -6:6 0:0:
  Element (i=0, j=0) at (0, 0)
  Element (i=1, j=0) at (2.771, 0)
  Element (i=0, j=1) at (1.386, 2.400)
  Element (i=1, j=1) at (4.157, 2.400)
```

---

## 8. COMPLEX EXAMPLES - ANNOTATED DISSECTION

### 8.1 Most Complex Example: Full AGR-1 Compact

**Complete cell definitions with universe hierarchy:**

```mcnp
c ============================================================================
c LEVEL 3: TRISO PARTICLE DEFINITION
c ============================================================================
c Cell 91101: Fuel kernel (UO2)
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
c Material 9111 is UO2 with specific enrichment
c Surface 91111: SO 0.017485 (sphere, r=0.017485 cm = 174.85 microns)
c Universe 1114 will be placed in lattice U=1116

c Cell 91102: Buffer layer (porous carbon)
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
c Between sphere 91111 (kernel outer) and 91112 (buffer outer)
c Thickness: 0.027905 - 0.017485 = 0.01042 cm = 104.2 microns

c Cell 91103: Inner Pyrocarbon (IPyC)
91103 9091 -1.904  91112 -91113  u=1114                 $ IPyC
c Thickness: 0.031785 - 0.027905 = 0.00388 cm = 38.8 microns

c Cell 91104: Silicon Carbide (SiC)
91104 9092 -3.205  91113 -91114  u=1114                 $ SiC
c Thickness: 0.035375 - 0.031785 = 0.00359 cm = 35.9 microns

c Cell 91105: Outer Pyrocarbon (OPyC)
91105 9093 -1.911  91114 -91115  u=1114                 $ OPyC
c Thickness: 0.039305 - 0.035375 = 0.00393 cm = 39.3 microns

c Cell 91106: Matrix surrounding particle
91106 9094 -1.344  91115         u=1114                 $ SiC Matrix
c From OPyC outer (91115) to lattice element boundary
c Fills space from r=0.039305 cm to r=1.0 cm

c Matrix-only element (no particle)
91107 9094 -1.344 -91116         u=1115                 $ SiC Matrix
c Entire element is matrix (used in corners of particle lattice)
c Surface 91116: SO 1.0 (sphere, r=1 cm)

c ============================================================================
c LEVEL 2: PARTICLE LATTICE (15×15×1)
c ============================================================================
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
c Surface 91117: RPP -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
c Element pitch: X=0.08743 cm, Y=0.08743 cm, Z=0.1 cm
c Total lattice size: 15×0.08743 = 1.31 cm square, 0.1 cm thick

c FILL array: 15 rows (j=-7 to 7) × 15 columns (i=-7 to 7) × 1 layer (k=0)
c Each row below represents constant j, varying i from -7 to 7

     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ j=-7
c    i=-7  -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6    7
c    Corners are matrix (1115), center region has particles (1114)

     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 $ j=-6
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=-5
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=-4
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=-3
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=-2
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 $ j=-1
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 $ j=0
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 $ j=1
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=2
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=3
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=4
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=5
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 $ j=6
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ j=7

c Approximate circular pattern:
c   - ~135 positions have U=1114 (TRISO particles)
c   - ~90 positions have U=1115 (matrix only, in corners)

c ============================================================================
c LEVEL 1: COMPACT AXIAL LATTICE (1×1×31)
c ============================================================================
c Matrix end cap element
91109 9094 -1.344 -91119    u=1117                 $ Matrix
c Surface 91119: C/Z 0 0 0.65 (cylinder, r=0.65 cm)

c Compact lattice: 1×1 in X,Y, 31 layers in Z
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
c Surface 91118: RPP -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
c Element pitch: X=1.3 cm, Y=1.3 cm, Z=0.08743 cm
c Total compact height: 31 × 0.08743 = 2.710 cm

c FILL array breakdown:
c   1117 2R     = 1117 1117 1117              (3 elements, k=-15,-14,-13)
c   1116 24R    = 1116 (repeated 25 times)    (25 elements, k=-12 to 12)
c   1117 2R     = 1117 1117 1117              (3 elements, k=13,14,15)
c Total: 3 + 25 + 3 = 31 elements ✓

c Axial structure:
c   Bottom 3 layers: Pure matrix (no particles)
c   Middle 25 layers: Particle lattice (135 particles × 25 = 3,375 particles)
c   Top 3 layers: Pure matrix (no particles)

c ============================================================================
c LEVEL 0: PLACEMENT IN GLOBAL UNIVERSE
c ============================================================================
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
c Surface 97011: Cylinder defining compact outer boundary
c Surfaces 98005, 98051: Axial planes defining compact height
c FILL=1110: Places entire compact lattice here
c TRCL=(x,y,z): Translation to position compact in experiment rig
```

**Complete particle tracking through hierarchy:**

1. **Neutron born** in global universe (U=0)
2. **Enters cell 91111**: Geometry sense tells MCNP to look in universe 1110
3. **Inside U=1110** (compact lattice): Determine which lattice element (i, j, k)
   - Say neutron is at Z position corresponding to k=0 (middle layer)
   - Lattice element k=0 contains U=1116 (particle lattice)
4. **Inside U=1116** (particle lattice): Determine which lattice element (i, j, k)
   - Say neutron is at position corresponding to (i=0, j=0, k=0) (center)
   - Lattice element (0, 0, 0) contains U=1114 (TRISO particle)
5. **Inside U=1114** (TRISO particle): Track through layers
   - Test against surfaces 91111, 91112, 91113, 91114, 91115
   - Determine if in kernel, buffer, IPyC, SiC, OPyC, or matrix
6. **Collision**: Sample physics in appropriate material

### 8.2 Hexagonal Lattice with Indentation

**Source**: input_definition.py, lines 237-250 (control assembly)

```mcnp
{n}15 0                  -{n}13 u={n}9 lat=2 imp:n=1 fill=-6:6 -6:6 0:0
c                                              i: -6 to 6 (13 elements)
c                                              j: -6 to 6 (13 elements)
c                                              k: 0 to 0 (1 element)
c                                              Total: 13×13×1 = 169 elements

c Row-by-row breakdown with hex geometry visualization:

     {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2  $ j=-6
c    i:  -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6
c    All reflector (U={n}2) at outer edge

      {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}1 {n}1 {n}2 {n}2 {n}2  $ j=-5
c      -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6
c     Reflector  |  Beginning of fuel region |  Reflector
c     First fuel elements appear at i=2,3 (positions 8,9 in this row)

       {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2  $ j=-4
c       -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6
c      More fuel ({n}1) and first coolant channel ({n}3) appears

        {n}2 {n}2 {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2  $ j=-3
c        -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6
c       Pattern: Fuel surrounding coolant channels

         {n}2 {n}2 {n}2 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}2  $ j=-2
c         -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6

          {n}2 {n}2 {n}2 {n}1 {n}1 {n}3 {n}2 {n}2 {n}3 {n}1 {n}1 {n}2 {n}2  $ j=-1
c          -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6
c         CONTROL RODS appear: {n}2 at i=0,1 are graphite (no fuel)
c         This is the difference between fuel and control assemblies

           {n}2 {n}2 {n}1 {n}3 {n}1 {n}2 {n}2 {n}2 {n}1 {n}3 {n}1 {n}2 {n}2  $ j=0
c           -6   -5   -4   -3   -2   -1    0    1    2    3    4    5    6
c          Control rod positions (no fuel) at i=-1,0,1

            {n}2 {n}2 {n}1 {n}1 {n}3 {n}2 {n}2 {n}3 {n}1 {n}1 {n}2 {n}2 {n}2  $ j=1
             {n}2 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}2 {n}2 {n}2  $ j=2
              {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2 {n}2 {n}2  $ j=3
               {n}2 {n}2 {n}1 {n}1 {n}3 {n}1 {n}1 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2  $ j=4
                {n}2 {n}2 {n}2 {n}1 {n}1 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2  $ j=5
                 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2 {n}2  $ j=6
c                Back to all reflector at outer edge
```

**Hexagonal geometry interpretation:**
- Each line is indented to show the staggered row pattern
- Even j-rows align vertically
- Odd j-rows are offset by half a pitch horizontally
- This creates the characteristic hexagonal close-packed pattern

**Control vs Fuel assemblies:**
- Fuel assemblies (lines 111-124): All {n}1 (fuel) or {n}3 (coolant) in active region
- Control assemblies (lines 237-250): Some {n}2 (graphite) in central positions for control rods

---

## 9. BOUNDARY CONDITIONS AND EDGE HANDLING

### 9.1 Lattice Boundaries

**Lattice elements only exist within the bounding surface:**

```mcnp
10 0 -100 u=50 lat=1 fill=0:5 0:5 0:0  $ 6×6×1 lattice
   ...

100 rpp -3 3 -3 3 -0.5 0.5  $ Defines extent of lattice universe
```

**What happens at the boundary:**
1. Particle tracked through lattice elements while inside surface 100
2. When particle crosses surface 100, it **exits the lattice universe**
3. MCNP returns to parent universe to determine next cell
4. If parent universe also has surface at same location, particle continues in new cell

**AGR-1 compact boundary example:**

```mcnp
c Compact lattice boundary
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715

c Placement in global universe
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)

97011: Cylinder r=0.65 cm (matches 91118 X,Y extent exactly)
98005, 98051: Planes matching 91118 Z extent

c Gas gap outside compact
91200 8902  1.2493e-4  97011 -97012  98005 -98007  $ stack 1 gas gap
```

**Critical alignment:**
- Lattice bounding surface 91118 has X,Y extent ±0.65 cm
- Global placement surface 97011 is cylinder r=0.65 cm
- **Exact match ensures no gap or overlap at boundary**

### 9.2 Handling Variations at Lattice Edges

**Problem**: What if you want different elements at lattice edges?

**Solution 1: Include edge elements in FILL array**

```mcnp
c 5×5 lattice with different edge elements
10 0 -100 u=50 lat=1 fill=0:4 0:4 0:0
   99 99 99 99 99  $ j=0: All edges are U=99
   99 10 10 10 99  $ j=1: Edges U=99, interior U=10
   99 10 10 10 99  $ j=2
   99 10 10 10 99  $ j=3
   99 99 99 99 99  $ j=4: All edges are U=99
```

**Solution 2: Nested lattices with different fills**

```mcnp
c Inner 3×3 lattice (U=10)
10 0 -100 u=10 lat=1 fill=0:2 0:2 0:0
   1 1 1
   1 1 1
   1 1 1

c Outer 5×5 lattice uses U=10 in center, U=99 at edges
20 0 -101 u=20 lat=1 fill=0:4 0:4 0:0
   99 99 99 99 99
   99 10 10 10 99  $ U=10 is itself a lattice!
   99 10 10 10 99
   99 10 10 10 99
   99 99 99 99 99
```

---

## 10. COMMON PITFALLS - EXPANDED CATALOG

### 10.1 FILL Dimension Errors

**Symptom**: Fatal error: "Universe ... expected but not found in fill card"

**Cause**: Wrong number of elements in FILL array

**Fix**:
1. Calculate required elements: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
2. Count provided elements (including repeat notation expansion)
3. Add/remove elements or adjust fill range

**Prevention**:
```mcnp
c ALWAYS add comment with element count verification
10 0 -100 u=50 lat=1 fill=-3:3 -3:3 0:0  $ 7×7×1=49 elements
c ... 49 universe numbers follow ...
```

### 10.2 Universe Number Conflicts

**Symptom**: Geometry errors, particles getting lost, wrong materials

**Cause**: Same universe number used for different geometries

**Example of ERROR:**
```mcnp
c Compact 1 - CORRECT
10 92235.80c -10.5 -1 u=100  $ Kernel in compact 1
11 6000.80c  -1.0  1 -2 u=100  $ Buffer in compact 1

c Compact 2 - ERROR: Reusing U=100 with DIFFERENT geometry
20 92238.80c -10.5 -3 u=100  $ Different material in U=100!
21 6000.80c  -1.0  3 -4 u=100  $ Surfaces 3,4 differ from 1,2
```

**Fix**: Use unique universe numbers for each distinct geometry
```mcnp
c Compact 1
10 92235.80c -10.5 -1 u=100
11 6000.80c  -1.0  1 -2 u=100

c Compact 2
20 92238.80c -10.5 -3 u=200  $ U=200, not U=100
21 6000.80c  -1.0  3 -4 u=200
```

### 10.3 Surface-Lattice Size Mismatch

**Symptom**: Gaps or overlaps in geometry

**Cause**: Lattice bounding surface doesn't match total lattice extent

**Example of ERROR:**
```mcnp
10 0 -100 u=50 lat=1 fill=0:4 0:4 0:0  $ 5×5 lattice
   ...

100 rpp -1 1 -1 1 -0.5 0.5  $ Element pitch should be 0.4, not 0.5!

c If element RPP is:
101 rpp -0.25 0.25 -0.25 0.25 -0.25 0.25

c Then 5 elements should span: 5 × 0.5 = 2.5, not 2!
c Surface 100 should be: rpp -1.25 1.25 -1.25 1.25 -0.5 0.5
```

**Fix**: Ensure lattice surface spans exact multiple of element pitch

### 10.4 Repeat Notation Off-by-One

**Symptom**: "Too many/too few entries in fill card"

**Cause**: Forgetting that `U nR` means n+1 copies total

**Example of ERROR:**
```mcnp
fill=0:0 0:0 0:20  $ Need 21 elements

10 10R 20 10R  $ WRONG: This is 11+11=22 elements!
```

**Fix**:
```mcnp
10 9R 20 10R  $ CORRECT: 10+10+1=21 elements
c Breakdown: 10 (once) + 9 repeats = 10 total
c            20 (once) + 10 repeats = 11 total
c            Grand total: 10+11=21 ✓
```

### 10.5 Hexagonal Fill Orientation Confusion

**Symptom**: Hexagonal lattice pattern rotated or mirrored from intended

**Cause**: Misunderstanding hexagonal i,j indexing

**Key rule**: For LAT=2:
- Increasing I moves along first hex axis (0°)
- Increasing J moves along second hex axis (60° from first)
- Physical X,Y depend on RHP surface orientation

**Fix**:
1. Draw hex lattice on paper
2. Number positions with (i,j) indices
3. Verify fill array matches drawn pattern
4. Check RHP R-vector points in intended direction

---

## 11. BEST PRACTICES - LATTICE-BUILDING WISDOM

### 11.1 Design Principles

**1. Start Simple, Add Complexity**
```mcnp
c Step 1: Test single element
1 0 -10 u=100  $ Simple single-cell universe

c Step 2: Test small lattice
2 0 -20 u=200 lat=1 fill=0:1 0:1 0:0
  100 100
  100 100

c Step 3: Expand to full size
3 0 -30 u=300 lat=1 fill=0:10 0:10 0:0
  100 100 100 ... (121 elements)
```

**2. Use Systematic Numbering**
```mcnp
c Universe numbering scheme:
c   ABCD format:
c     A = assembly row
c     B = assembly column
c     C = component type (0=lattice, 1=fuel, 2=coolant, etc.)
c     D = variant number

c Example:
c   U=1110 = Assembly (1,1), lattice (0), variant 0
c   U=1211 = Assembly (1,2), fuel (1), variant 1
c   U=2320 = Assembly (2,3), coolant (2), variant 0
```

**3. Comment Extensively**
```mcnp
c ============================================================================
c FUEL ASSEMBLY 1-1 (Row 1, Column 1)
c ============================================================================
c Contains:
c   - Particle lattice (23×23×1) with ~380 TRISO particles per layer
c   - Axial lattice (1×1×669) with 667 active layers
c   - Total particles: ~254,000
c ----------------------------------------------------------------------------

100 0 -1000 u=1100 lat=1 fill=-11:11 -11:11 0:0  $ Particle lattice
    1101 1101 1101 ...  $ j=-11: ...
    ...
```

**4. Verify at Each Level**
```mcnp
c After defining each lattice level:
c   1. Run MCNP with minimal history count (e.g., 1000 histories)
c   2. Check output for geometry errors
c   3. Use geometry plots (px, py, pz commands) to visualize
c   4. Verify no lost particles
c   5. Check cell volumes if specified
```

**5. Use Repeat Notation Wisely**
```mcnp
c GOOD: Clear pattern with repeat notation
fill=0:0 0:0 0:50
  10 5R 20 39R 10 5R  $ End caps + active region + end caps

c BAD: Overuse makes it hard to verify
fill=0:0 0:0 0:50
  10 1R 10 1R 10 1R 20 2R 20 2R ...  $ Hard to count total!
```

### 11.2 Debugging Techniques

**Technique 1: Progressive Lattice Building**

```mcnp
c Version 1: Test single lattice element
1 0 -10 u=100 lat=1 fill=0:0 0:0 0:0
  200

c Version 2: Test 2×2 lattice
1 0 -10 u=100 lat=1 fill=0:1 0:1 0:0
  200 200
  200 200

c Version 3: Test with variation
1 0 -10 u=100 lat=1 fill=0:1 0:1 0:0
  200 201
  201 200

c Version 4: Full size with all variations
1 0 -10 u=100 lat=1 fill=0:10 0:10 0:0
  [Full 11×11 array]
```

**Technique 2: Geometry Plotting**

```mcnp
c Add plot cards to visualize lattice
c XY plot through lattice center
px  0  $ Shows i,j lattice structure

c XZ plot through lattice
py  0  $ Shows i,k lattice structure

c YZ plot through lattice
pz  0  $ Shows j,k lattice structure
```

**Technique 3: Volume Checking**

```mcnp
c Specify volumes for verification
10 92235.80c -10.5 -1 u=100 vol=0.0224  $ Kernel volume (cm³)

c After run, check "volume of cells" in output
c MCNP will report if calculated volume differs significantly
```

**Technique 4: Reduced Model Testing**

```mcnp
c Instead of full 15×15 particle lattice, test 3×3
91108 0 -91117 u=1116 lat=1 fill=-1:1 -1:1 0:0  $ 3×3 test
     1115 1114 1115
     1114 1114 1114
     1115 1114 1115

c Instead of 31 axial layers, test 5
91110 0 -91118 u=1110 lat=1 fill=0:0 0:0 -2:2  $ 5 layers test
     1117 1116 1116 1116 1117
```

### 11.3 Performance Optimization

**1. Balance Lattice Size vs Particle Tracking Efficiency**

Large lattices (>100×100 elements) can slow down geometry lookups.
Consider using:
- Nested smaller lattices instead of one huge lattice
- Simplified geometries at outer regions

**2. Use Repeated Universes When Possible**

```mcnp
c EFFICIENT: Reuse same universe
fill=0:100 0:100 0:0
  100 100R  $ 101 copies of same universe

c INEFFICIENT: Unique universes for identical geometry
fill=0:100 0:100 0:0
  100 101 102 103 ... 200  $ 101 identical geometries, different U numbers
```

**3. Minimize Nesting Depth**

Each level of nesting adds computational overhead.
Try to limit to 3-4 levels maximum when possible.

**4. Consider Homogenization for Deep Analysis**

For very large models (millions of particles):
- Use explicit lattices for initial runs
- Derive homogenized cross-sections
- Use simplified geometry for production runs

---

## 12. ADVANCED TECHNIQUES

### 12.1 Mixed Lattice Type Systems

**Rectangular lattice containing hexagonal sub-lattices:**

```mcnp
c Level 1: Rectangular array of hexagonal assemblies
100 0 -1000 u=1000 lat=1 fill=0:2 0:2 0:0
    101 102 103
    104 105 106
    107 108 109

c Level 2: Each assembly is hexagonal lattice
101 0 -1010 u=101 lat=2 fill=-3:3 -3:3 0:0
    [Hexagonal fill pattern for assembly 1]

102 0 -1020 u=102 lat=2 fill=-3:3 -3:3 0:0
    [Hexagonal fill pattern for assembly 2]

c Etc...
```

**Applications:**
- PWR core: Square lattice of assemblies, hexagonal pin arrangement within
- Prismatic HTGR: Hexagonal core, hexagonal assemblies, rectangular compacts

### 12.2 Partial Lattice Filling

**Using void/outer cells to create partial fills:**

```mcnp
c Define special "empty" universe
999 0 -999 u=999 imp:n=0  $ Void universe
    999 so 999  $ Sphere of nothing

c Lattice with empty positions
100 0 -1000 u=100 lat=1 fill=0:4 0:4 0:0
    999 999 999 999 999
    999 10  10  10  999
    999 10  10  10  999
    999 10  10  10  999
    999 999 999 999 999

c Particles entering U=999 are terminated (imp:n=0)
c Creates effectively a 3×3 lattice within 5×5 array
```

**Alternative: Use negative importance**

```mcnp
100 0 -1000 u=100 lat=1 fill=0:4 0:4 0:0
    0 0 0 0 0  $ U=0 with imp:n=0 kills particles
    0 10 10 10 0
    0 10 10 10 0
    0 10 10 10 0
    0 0 0 0 0
```

### 12.3 Transformation with FILL

**Rotating filled universes:**

```mcnp
c Define universe to be rotated
10 92235.80c -10.5 -1 u=100  $ Fuel cell with specific orientation
   1 cz 1  $ Cylinder along Z axis

c Fill with rotation
20 0 -2 fill=100 (*1)  $ Fill with U=100, apply transformation 1

c Transformation rotates about X axis
*1 0 0 0  90 0 0  $ Rotate 90° about X
c Now cylinder is along Y axis instead of Z
```

**Translating filled universes (already seen in AGR-1 model):**

```mcnp
91111 0 -97011 98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
c TRCL = (x, y, z) translation positions compact at specific coordinates
```

---

## 13. SUMMARY - KEY TAKEAWAYS

### 13.1 Essential Rules (Memorize These)

1. **FILL array size** = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

2. **Index ordering**: Arrays filled in **K, J, I** order (K outermost loop)

3. **Repeat notation**: `U nR` means **(n+1) total copies** (first + n repeats)

4. **Lattice pitch**: Determined by bounding surface dimensions
   - RPP: Pitch = (MAX - MIN) for each axis
   - RHP: Pitch = 2|R|cos(30°) = |R|√3

5. **Universe numbers**: MUST be unique for each distinct geometry

6. **Negative indices**: fill=-5:5 is **11 elements**, not 5 or 10

7. **Hexagonal indentation**: Input formatting shows structure, but isn't required

### 13.2 Common Patterns to Reuse

**Pattern 1: Particles in Matrix**
```mcnp
u=PARTICLE: Multi-layer sphere
u=MATRIX: Single material filling element
u=LATTICE: 2D rectangular array with circular particle distribution
```

**Pattern 2: Axial Stack**
```mcnp
u=AXIAL_LATTICE: 1×1×N array using repeat notation
  END_CAP nR  ACTIVE mR  END_CAP nR
```

**Pattern 3: Hexagonal Assembly**
```mcnp
u=HEX_LATTICE: LAT=2 with (-N:N, -N:N, 0:0) dimensions
  Reflector/moderator at edges
  Fuel + coolant in hexagonal pattern
```

**Pattern 4: Nested Lattices**
```mcnp
u=OUTER_LATTICE: Contains positions filled with u=INNER_LATTICE
u=INNER_LATTICE: Contains detailed sub-structure
```

### 13.3 Most Common Errors (Avoid These)

| Error | Symptom | Fix |
|-------|---------|-----|
| Wrong fill count | "Expected but not found" | Recalculate (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1) |
| Repeat notation off-by-one | Fill count wrong | Remember: U nR = n+1 total copies |
| Surface size mismatch | Gaps/overlaps | Match lattice surface to N×pitch |
| Universe conflict | Wrong materials | Use unique U numbers |
| Index range error | Unexpected positions | Check if range includes negative indices |
| Hexagonal orientation | Pattern rotated | Verify RHP R-vector direction |

### 13.4 File References for Further Study

**AGR-1 TRISO Fuel Model:**
- File: `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/sdr-agr.i`
- Lines 14-42: Complete TRISO + particle lattice + compact lattice hierarchy
- Lines 22-37: 15×15 particle lattice FILL array
- Line 40: 1×1×31 compact lattice with repeat notation
- Lines 2381-2419: Surface definitions for particle and compact geometries

**Micro-HTGR Model:**
- File: `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/micro/input_definition.py`
- Lines 76-99: 23×23 particle lattice
- Line 103: 1×1×669 compact lattice with 667 active layers
- Lines 111-124: Hexagonal assembly lattice (fuel configuration)
- Lines 237-250: Hexagonal assembly lattice (control configuration)
- Lines 331-379: Hexagonal core lattices for all 4 axial layers

**Validation Benchmarks:**
- Directory: `/home/user/mcnp-skills/example_files/MCNP6_VnV/validation/crit_expanded/experiments/`
- Various simple lattice examples in critical experiment models

---

## 14. QUICK REFERENCE CARD

### Syntax Summary

```mcnp
CELL_ID  MAT  DENS  GEOMETRY  u=UNIV  [vol=VOL]  imp:n=IMP
CELL_ID  0    GEOMETRY  u=UNIV  lat=TYPE  fill=IMIN:IMAX JMIN:JMAX KMIN:KMAX
    UNIVERSE_LIST

CELL_ID  0    GEOMETRY  fill=UNIV  [TRCL=(x y z)]
```

### LAT Types

| LAT | Type | Coordinate System | Typical Applications |
|-----|------|-------------------|---------------------|
| 1 | Rectangular | Cartesian (X,Y,Z) | Pin arrays, compacts, axial stacks |
| 2 | Hexagonal | 60° skewed axes | Prismatic reactors, close-packed assemblies |

### FILL Dimension Calculation

```
Required elements = (IMAX - IMIN + 1) × (JMAX - JMIN + 1) × (KMAX - KMIN + 1)

For fill=-7:7 -7:7 0:0:
  I: -7 to 7 = 15 elements
  J: -7 to 7 = 15 elements
  K: 0 to 0 = 1 element
  Total: 15 × 15 × 1 = 225 elements
```

### Repeat Notation

```
U nR  =  U repeated (n+1) times total

Examples:
  10 2R     =  10 10 10        (3 elements)
  20 5R     =  20 20 20 20 20 20   (6 elements)
  10 0R     =  10              (1 element, no repeats)
```

### Index Ordering (CRITICAL)

```
For fill=I1:I2 J1:J2 K1:K2, MCNP fills in this order:

for k = K1 to K2:
    for j = J1 to J2:
        for i = I1 to I2:
            element[k][j][i] = next universe number

Rightmost index (I) varies fastest!
```

### Lattice Pitch from Surfaces

```
LAT=1 with RPP XMIN XMAX YMIN YMAX ZMIN ZMAX:
  X pitch = XMAX - XMIN
  Y pitch = YMAX - YMIN
  Z pitch = ZMAX - ZMIN

LAT=2 with RHP VX VY VZ  HX HY HZ  RX RY RZ:
  Pitch = |R| × √3
  Height = |H|
```

---

## CONCLUSION

FILL arrays and lattice structures are the backbone of complex MCNP reactor models. Mastering these techniques enables modeling of:

- **Millions of TRISO particles** in pebble bed or prismatic reactors
- **Complex core configurations** with multiple assembly types
- **Multi-scale physics** from micron-scale particle coatings to meter-scale reactor cores
- **Efficient geometry** with minimal input file size using repeat notation and universe reuse

The AGR-1 and micro-HTGR models demonstrate PRODUCTION-QUALITY lattice implementations that have been validated against experimental data. Study these examples, apply the best practices documented here, and verify your models at each level of complexity.

**Key to success**: Start simple, verify at each step, use systematic numbering, comment extensively, and always double-check your FILL array dimensions!

---

**Document prepared by**: AGENT 8 - Technical Documentation Analysis Specialist
**Analysis date**: 2025-11-07
**Files analyzed**: 14 MCNP input files + 1 Python generation script
**Total lines analyzed**: ~245,000 lines of MCNP code
