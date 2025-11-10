# CROSS-REFERENCING VISUAL DIAGRAMS

## 1. AGR-1 MODEL STRUCTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                    BASE UNIVERSE (0)                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ATR REACTOR CORE                                         │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │  CAPSULE 1 (fill=1110 at x1,y1,z1)                   │ │  │
│  │  │  ┌────────────────────────────────────────────────┐  │ │  │
│  │  │  │  Stack 1                                       │  │ │  │
│  │  │  │  ┌──────────────────────────────────────────┐  │  │ │  │
│  │  │  │  │ Compact 1 (Universe 1110, lat=1)        │  │  │ │  │
│  │  │  │  │ ┌────────────────────────────────────┐  │  │  │ │  │
│  │  │  │  │ │ Matrix Layer (u=1117)              │  │  │  │ │  │
│  │  │  │  │ └────────────────────────────────────┘  │  │  │ │  │
│  │  │  │  │ ┌────────────────────────────────────┐  │  │  │ │  │
│  │  │  │  │ │ Particle Layer (u=1116, 15×15)     │  │  │  │ │  │
│  │  │  │  │ │  ┌──────────────────────────────┐  │  │  │  │ │  │
│  │  │  │  │ │  │ TRISO Particle (u=1114)      │  │  │  │  │ │  │
│  │  │  │  │ │  │  ┌─ Kernel (9111, -10.924)   │  │  │  │  │ │  │
│  │  │  │  │ │  │  ├─ Buffer (9090, -1.100)    │  │  │  │  │ │  │
│  │  │  │  │ │  │  ├─ IPyC (9091, -1.904)      │  │  │  │  │ │  │
│  │  │  │  │ │  │  ├─ SiC (9092, -3.205)       │  │  │  │  │ │  │
│  │  │  │  │ │  │  ├─ OPyC (9093, -1.911)      │  │  │  │  │ │  │
│  │  │  │  │ │  │  └─ Matrix (9094, -1.344)    │  │  │  │  │ │  │
│  │  │  │  │ │  └──────────────────────────────┘  │  │  │  │ │  │
│  │  │  │  │ │  ┌──────────────────────────────┐  │  │  │  │ │  │
│  │  │  │  │ │  │ Matrix Only (u=1115)         │  │  │  │  │ │  │
│  │  │  │  │ │  └──────────────────────────────┘  │  │  │  │ │  │
│  │  │  │  │ └────────────────────────────────────┘  │  │  │ │  │
│  │  │  │  │ ┌────────────────────────────────────┐  │  │  │ │  │
│  │  │  │  │ │ Matrix Layer (u=1117)              │  │  │  │ │  │
│  │  │  │  │ └────────────────────────────────────┘  │  │  │ │  │
│  │  │  │  └──────────────────────────────────────────┘  │  │ │  │
│  │  │  │  [Compacts 2, 3, 4 repeat similar structure]  │  │ │  │
│  │  │  └────────────────────────────────────────────────┘  │ │  │
│  │  │  [Stacks 2, 3 repeat similar structure]              │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │  [Capsules 2-6 repeat similar structure]                  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. NUMBERING SCHEME STRUCTURE

### Cell Number Anatomy: 91234

```
    9  1  2  3  4
    │  │  │  │  │
    │  │  │  │  └─── Sequence within compact (0-9)
    │  │  │  └────── Compact identifier
    │  │  │           0 = Compact 1
    │  │  │           2 = Compact 2
    │  │  │           4 = Compact 3
    │  │  │           6 = Compact 4
    │  │  └─────────── Stack number (1-3)
    │  └────────────── Capsule number (1-6)
    └───────────────── AGR experiment identifier
```

### Surface Number Anatomy: 91234

```
    9  1  2  3  4
    │  │  │  │  │
    │  │  │  │  └─── Layer identifier
    │  │  │  │       1 = Kernel surface
    │  │  │  │       2 = Buffer surface
    │  │  │  │       3 = IPyC surface
    │  │  │  │       4 = SiC surface
    │  │  │  │       5 = OPyC surface
    │  │  │  │       6 = Matrix sphere
    │  │  │  │       7 = Lattice box
    │  │  │  │       8 = Compact box
    │  │  │  │       9 = Compact cylinder
    │  │  │  └────── Compact number (1-4)
    │  │  └─────────── Stack number (1-3)
    │  └────────────── Capsule number (1-6)
    └───────────────── AGR surface identifier
```

### Material Number Anatomy: 9123

```
    9  1  2  3
    │  │  │  │
    │  │  │  └────── Compact number (1-4)
    │  │  └─────────── Stack number (1-3)
    │  └────────────── Capsule number (1-6)
    └───────────────── Fuel material identifier
```

### Universe Number Anatomy: 1234

```
    1  2  3  4
    │  │  │  │
    │  │  │  └────── Structure level
    │  │  │          0 = Full compact assembly
    │  │  │          4 = TRISO particle
    │  │  │          5 = Matrix-only cell
    │  │  │          6 = Particle lattice
    │  │  │          7 = Matrix block
    │  │  └─────────── Compact number (1-4)
    │  └────────────── Stack number (1-3)
    └───────────────── Capsule number (1-6)
```

---

## 3. CROSS-REFERENCE FLOW DIAGRAM

### Complete Reference Chain for One TRISO Particle

```
CELL 91101                    SURFACE 91111               MATERIAL 9111
┌─────────────────┐          ┌─────────────────┐        ┌─────────────────┐
│ ID: 91101       │───uses──>│ ID: 91111       │        │ ID: 9111        │
│ Mat: 9111       │─────────────────────────────────────>│ Composition:    │
│ Dens: -10.924   │          │ Type: so        │        │  92234  3.34E-3 │
│ Geom: -91111    │          │ Radius: 0.01748 │        │  92235  1.99E-1 │
│ Univ: u=1114    │          │ Comment: Kernel │        │  92238  7.97E-1 │
│ Vol: 0.092522   │          └─────────────────┘        │  6012   0.322   │
└─────────────────┘                                      │  6013   0.0036  │
         │                                               │  8016   1.361   │
         │                                               └─────────────────┘
         │ belongs to
         v
UNIVERSE 1114
┌──────────────────────────────────────────┐
│ Contains 6 cells:                        │
│  91101 (kernel)    - surface 91111       │
│  91102 (buffer)    - surfaces 91111,91112│
│  91103 (IPyC)      - surfaces 91112,91113│
│  91104 (SiC)       - surfaces 91113,91114│
│  91105 (OPyC)      - surfaces 91114,91115│
│  91106 (matrix)    - surface 91115       │
└──────────────────────────────────────────┘
         │ used in
         v
LATTICE (Universe 1116)
┌──────────────────────────────────────────┐
│ Type: lat=1 (rectangular)                │
│ Dimensions: 15×15×1                      │
│ Fill pattern:                            │
│  1114 (TRISO) at fuel positions          │
│  1115 (matrix) at edge positions         │
└──────────────────────────────────────────┘
         │ used in
         v
COMPACT STACK (Universe 1110)
┌──────────────────────────────────────────┐
│ Type: lat=1 (rectangular)                │
│ Dimensions: 1×1×31                       │
│ Fill pattern:                            │
│  1117 (matrix) - 3 bottom layers         │
│  1116 (particles) - 24 middle layers     │
│  1117 (matrix) - 3 top layers            │
└──────────────────────────────────────────┘
         │ filled into
         v
BASE UNIVERSE CELL 91111
┌──────────────────────────────────────────┐
│ ID: 91111                                │
│ Mat: 0 (void)                            │
│ Geom: -97011 98005 -98051               │
│ Fill: fill=1110 (25.547 -24.553 19.108) │
└──────────────────────────────────────────┘
```

---

## 4. BOOLEAN EXPRESSION VISUALIZATION

### Example: Spherical Shell Cell

```
Cell: 91102 9090 -1.100  91111 -91112  u=1114

Surfaces:
  91111: so 0.01748  (sphere, radius 0.01748 cm)
  91112: so 0.02763  (sphere, radius 0.02763 cm)

Boolean Expression:  91111 -91112
                     (inside 91112) ∩ (outside 91111)

Visual:
               ┌─────────────────────────┐
               │  Surface 91112          │
               │  (outer boundary)       │
               │   ┌─────────────┐       │
               │   │ Surface     │       │
               │   │ 91111       │       │
               │   │ (inner)     │       │
               │   │   KERNEL    │       │
               │   └─────────────┘       │
               │    ╱╱╱╱╱╱╱╱╱╱╱╱╱╱       │
               │   ╱  THIS REGION ╱      │
               │  ╱   IS BUFFER  ╱       │
               │ ╱   (cell 91102)╱       │
               │╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱        │
               └─────────────────────────┘
```

### Example: Complex Boolean Expression

```
Cell: 60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110

Decomposition:
  1111      → Inside surface 1111 (radial inner)
  -1118     → Outside surface 1118 (radial outer)
  74        → Inside surface 74 (diagonal plane 1)
  -29       → Outside surface 29 (diagonal plane 2)
  53        → Inside surface 53 (diagonal plane 3)
  100       → Inside surface 100 (bottom axial plane)
  -110      → Outside surface 110 (top axial plane)

Combined: Intersection of all 7 conditions
         Creates a wedge-shaped segment of an annular cylinder

3D Visualization:

              z ↑
                │     ╱╱╱╱╱╱╱╱╱╱╱╱
                │    ╱  Surface  ╱
              110 ─ ╱    -110   ╱
                │  ╱╱╱╱╱╱╱╱╱╱╱╱╱╱
                │  │           │
                │  │   CELL    │  ← Bounded by all surfaces
                │  │  60106    │
                │  │           │
              100 ─ ╲╲╲╲╲╲╲╲╲╲╲╲╲╲
                │    ╲ Surface ╲
                │     ╲   100   ╲
                └─────╲╲╲╲╲╲╲╲╲╲╲╲──> r
                       │    │
                     1111  1118
                   (inner)(outer)
                    radial boundaries
```

---

## 5. LATTICE STRUCTURE VISUALIZATION

### 15×15 TRISO Particle Lattice (Universe 1116)

```
Fill: -7:7 -7:7 0:0 (indices from -7 to +7 in x and y)

    -7  -6  -5  -4  -3  -2  -1   0  +1  +2  +3  +4  +5  +6  +7
    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
-7  │ M │ M │ M │ M │ M │ M │ P │ P │ P │ M │ M │ M │ M │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
-6  │ M │ M │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
-5  │ M │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
-4  │ M │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
-3  │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
-2  │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
-1  │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 0  │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+1  │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+2  │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+3  │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+4  │ M │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+5  │ M │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+6  │ M │ M │ M │ P │ P │ P │ P │ P │ P │ P │ P │ P │ M │ M │ M │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
+7  │ M │ M │ M │ M │ M │ M │ P │ P │ P │ M │ M │ M │ M │ M │ M │
    └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘

    Legend: P = TRISO Particle (u=1114)
            M = Matrix Only (u=1115)

    Total elements: 15 × 15 = 225
    TRISO particles: ~145
    Matrix-only cells: ~80
```

### Vertical Compact Stack (Universe 1110)

```
Fill: 0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

Pattern decoding:
  1117 2R  → 1117, 1117, 1117 (3 elements)
  1116 24R → 1116, 1116, ... (25 times)
  1117 2R  → 1117, 1117, 1117 (3 elements)
  Total: 3 + 25 + 3 = 31 elements (matches -15 to +15)

z-direction layout:
    ┌────────────────┐ +15
    │  Matrix (1117) │
    ├────────────────┤ +13
    │  Matrix (1117) │
    ├────────────────┤ +11
    │  Matrix (1117) │  ← Top end cap
    ├────────────────┤ +9
    │ Particles      │
    │  (1116)        │
    ├────────────────┤ +7
    │ Particles      │
    │  (1116)        │
    ├────────────────┤ +5
    │ Particles      │
    │  (1116)        │
    ├────────────────┤
    │      ...       │  ← Main fuel region
    │ 25 layers of   │     (24 with particles)
    │ particle       │
    │ lattices       │
    ├────────────────┤
    │ Particles      │
    │  (1116)        │
    ├────────────────┤ -9
    │ Particles      │
    │  (1116)        │
    ├────────────────┤ -11
    │  Matrix (1117) │
    ├────────────────┤ -13
    │  Matrix (1117) │  ← Bottom end cap
    ├────────────────┤
    │  Matrix (1117) │
    └────────────────┘ -15
```

---

## 6. MATERIAL-GEOMETRY CORRELATION MAP

### Complete Capsule 1, Stack 1, Compact 1

```
┌───────────────────────────────────────────────────────────────┐
│                      CELL HIERARCHY                           │
├──────────┬─────────┬──────────┬──────────┬───────────────────┤
│ Cell ID  │ Mat ID  │ Density  │ Surfaces │ Universe          │
├──────────┼─────────┼──────────┼──────────┼───────────────────┤
│ 91101    │ 9111    │ -10.924  │ -91111   │ u=1114 (particle) │
│ 91102    │ 9090    │ -1.100   │ 91111    │ u=1114            │
│          │         │          │ -91112   │                   │
│ 91103    │ 9091    │ -1.904   │ 91112    │ u=1114            │
│          │         │          │ -91113   │                   │
│ 91104    │ 9092    │ -3.205   │ 91113    │ u=1114            │
│          │         │          │ -91114   │                   │
│ 91105    │ 9093    │ -1.911   │ 91114    │ u=1114            │
│          │         │          │ -91115   │                   │
│ 91106    │ 9094    │ -1.344   │ 91115    │ u=1114            │
│ 91107    │ 9094    │ -1.344   │ -91116   │ u=1115 (matrix)   │
│ 91108    │ 0       │ void     │ -91117   │ u=1116 (lat=1)    │
│ 91109    │ 9094    │ -1.344   │ -91119   │ u=1117 (matrix)   │
│ 91110    │ 0       │ void     │ -91118   │ u=1110 (lat=1)    │
│ 91111    │ 0       │ void     │ -97011   │ fill=1110         │
│          │         │          │ 98005    │ (base universe)   │
│          │         │          │ -98051   │                   │
└──────────┴─────────┴──────────┴──────────┴───────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                    SURFACE DEFINITIONS                        │
├──────────┬──────────┬──────────────────────────────────────┬──┤
│ Surf ID  │ Type     │ Definition               │ Purpose    │
├──────────┼──────────┼──────────────────────────┼────────────┤
│ 91111    │ so       │ 0.017485                 │ Kernel OR  │
│ 91112    │ so       │ 0.027635                 │ Buffer OR  │
│ 91113    │ so       │ 0.031585                 │ IPyC OR    │
│ 91114    │ so       │ 0.035115                 │ SiC OR     │
│ 91115    │ so       │ 0.039215                 │ OPyC OR    │
│ 91116    │ so       │ 1.000000                 │ Matrix     │
│ 91117    │ rpp      │ ±0.065 ... ±0.05         │ Lattice box│
│ 91118    │ rpp      │ ±0.65 ... ±0.065         │ Compact box│
│ 91119    │ c/z      │ 0.0 0.0 0.6500           │ Compact cyl│
│ 97011    │ c/z      │ 25.547 -24.553 0.635     │ Stack cyl  │
│ 98005    │ pz       │ 17.81810                 │ Bottom     │
│ 98051    │ pz       │ 20.35810                 │ Top        │
└──────────┴──────────┴──────────────────────────┴────────────┘

┌───────────────────────────────────────────────────────────────┐
│                   MATERIAL COMPOSITIONS                       │
├──────────┬────────────────────────────────────────────────────┤
│ Mat ID   │ Composition                                        │
├──────────┼────────────────────────────────────────────────────┤
│ 9111     │ UCO Kernel: U-234,235,236,238 + C + O             │
│          │ Density: 10.924 g/cm³                              │
├──────────┼────────────────────────────────────────────────────┤
│ 9090     │ Buffer: C-12, C-13                                 │
│          │ Density: 1.100 g/cm³                               │
├──────────┼────────────────────────────────────────────────────┤
│ 9091     │ IPyC: C-12, C-13                                   │
│          │ Density: 1.904 g/cm³                               │
├──────────┼────────────────────────────────────────────────────┤
│ 9092     │ SiC: Si-28,29,30 + C-12,13                        │
│          │ Density: 3.205 g/cm³                               │
├──────────┼────────────────────────────────────────────────────┤
│ 9093     │ OPyC: C-12, C-13                                   │
│          │ Density: 1.911 g/cm³                               │
├──────────┼────────────────────────────────────────────────────┤
│ 9094     │ Matrix: C-12, C-13                                 │
│          │ Density: 1.344 g/cm³                               │
└──────────┴────────────────────────────────────────────────────┘
```

---

## 7. VALIDATION FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│               PRE-RUN VALIDATION CHECKS                     │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            v                               v
┌────────────────────────┐     ┌────────────────────────┐
│  Surface Validation    │     │  Material Validation   │
│                        │     │                        │
│  For each cell:        │     │  For each cell:        │
│  • Extract surf list   │     │  • Extract mat ID      │
│  • Check each surf     │     │  • Search materials    │
│    exists in surf blk  │     │    block for mID       │
│  • Report undefined    │     │  • Report undefined    │
└────────┬───────────────┘     └───────────┬────────────┘
         │                                 │
         │                                 │
         v                                 v
┌────────────────────────┐     ┌────────────────────────┐
│  Universe Validation   │     │  Lattice Validation    │
│                        │     │                        │
│  For each fill:        │     │  For each lat=1:       │
│  • Extract univ ID     │     │  • Extract fill bounds │
│  • Search for u=ID     │     │  • Count fill entries  │
│  • Check defined       │     │  • Calculate expected  │
│    before use          │     │    (x_max-x_min+1) ×   │
│  • Build fill graph    │     │    (y_max-y_min+1) ×   │
│  • Check for cycles    │     │    (z_max-z_min+1)     │
└────────┬───────────────┘     │  • Compare counts      │
         │                     └───────────┬────────────┘
         │                                 │
         └────────────┬────────────────────┘
                      │
                      v
            ┌──────────────────┐
            │  All checks pass? │
            └─────────┬─────────┘
                      │
          ┌───────────┴────────────┐
          │                        │
        Yes                       No
          │                        │
          v                        v
┌──────────────────┐     ┌──────────────────────┐
│ Geometry Check   │     │ Report Errors        │
│ • Run plotter    │     │ • List undefined     │
│ • Visual inspect │     │   references         │
│ • Test 100 hist  │     │ • List conflicts     │
│ • Check for lost │     │ • Exit before run    │
│   particles      │     └──────────────────────┘
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Ready to run!    │
└──────────────────┘
```

---

## 8. ERROR DETECTION TREE

```
           Lost Particles Detected
                    │
        ┌───────────┴───────────┐
        │                       │
    Geometry Gap           Overlap
        │                       │
        v                       v
┌───────────────┐       ┌───────────────┐
│ Find gap:     │       │ Find overlap: │
│ • Plot geom   │       │ • Run with    │
│ • Look for    │       │   vol card    │
│   white space │       │ • Check warn  │
│ • Add cell to │       │ • Fix boolean │
│   fill gap    │       │   expressions │
└───────────────┘       └───────────────┘

     Surface Not Found
            │
     ┌──────┴──────┐
     │             │
  Typo         Missing Definition
     │             │
     v             v
Fix cell        Add surface
reference       to surfaces
                   block

    Material Not Found
            │
     ┌──────┴──────┐
     │             │
  Typo         Missing Definition
     │             │
     v             v
Fix cell        Add material
reference       to materials
                   block

   Universe Recursion
         │
         v
   Map fill chain
         │
         v
   Find cycle A→B→A
         │
         v
   Restructure hierarchy
         │
         v
   Break cycle with
   intermediate universe
```

---

## 9. PYTHON GENERATION LOGIC DIAGRAM

```
                    Start Generation
                          │
                          v
            ┌─────────────────────────┐
            │ Define numbering scheme │
            │  c = f(cap,stack,comp)  │
            │  s = f(cap,stack,comp)  │
            │  m = f(cap,stack,comp)  │
            │  u = f(cap,stack,comp)  │
            └────────────┬────────────┘
                         │
                         v
            ┌────────────────────────┐
            │ Initialize empty       │
            │ strings:               │
            │  cells = ""            │
            │  surfaces = ""         │
            │  materials = ""        │
            └────────┬───────────────┘
                     │
                     v
        ┌────────────────────────────┐
        │ for cap in range(1, 7):    │
        └────────┬───────────────────┘
                 │
                 v
        ┌────────────────────────────┐
        │ for stack in range(1, 4):  │
        └────────┬───────────────────┘
                 │
                 v
        ┌────────────────────────────┐
        │ for comp in range(1, 5):   │
        └────────┬───────────────────┘
                 │
                 v
        ┌────────────────────────────┐
        │ Calculate IDs:             │
        │  c = 90000 + cap*1000 +    │
        │      stack*100 +            │
        │      2*(comp-1)*10          │
        │  s = 9000 + cap*100 +      │
        │      stack*10 + comp        │
        │  Similar for m, u          │
        └────────┬───────────────────┘
                 │
                 v
        ┌────────────────────────────┐
        │ Generate cells:            │
        │  cells += compact_cells()  │
        │                            │
        │ Generate surfaces:         │
        │  surfaces +=               │
        │    compact_surfaces()      │
        │                            │
        │ Generate materials:        │
        │  materials +=              │
        │    fuel_material()         │
        └────────┬───────────────────┘
                 │
                 v
        ┌────────────────────────────┐
        │ Loop complete?             │
        └────────┬───────────────────┘
                 │
        ┌────────┴────────┐
       No               Yes
        │                │
        v                v
   Next iteration   Assemble final
   (increment)      input file
                         │
                         v
                ┌────────────────┐
                │ Write to file  │
                └────────────────┘
                         │
                         v
                  Complete!

   Benefits of this approach:
   • No manual numbering
   • Guaranteed consistency
   • Easy to modify (change function)
   • Scalable (72 compacts generated)
   • No copy-paste errors
```

---

**END OF VISUAL DIAGRAMS**
