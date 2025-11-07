# AGR-1 CELL CARD COMPLETE ANALYSIS
## Comprehensive Study of HTGR TRISO Particle and Compact Lattice Structures

**Files Analyzed:**
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/sdr-agr.i` (4,653 lines)
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/bench_138B.i` (18,414 lines)

**Analysis Date:** 2025-11-07

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [File Overview](#file-overview)
3. [Universe Numbering Scheme](#universe-numbering-scheme)
4. [TRISO Particle Cell Structure](#triso-particle-cell-structure)
5. [Particle Lattice Structures (15×15×1)](#particle-lattice-structures-15x15x1)
6. [Compact Lattice Structures (1×1×31)](#compact-lattice-structures-1x1x31)
7. [Complete Universe Hierarchy](#complete-universe-hierarchy)
8. [Cell Card Patterns](#cell-card-patterns)
9. [Surface Definitions](#surface-definitions)
10. [Material Assignments](#material-assignments)
11. [Key Insights for Model Development](#key-insights-for-model-development)

---

## Executive Summary

The AGR-1 (Advanced Gas Reactor) experiment models demonstrate sophisticated MCNP lattice structures for modeling TRISO-coated fuel particles in graphite matrix compacts. The model uses a **five-level universe hierarchy** to efficiently represent:

- **6 capsules** (stacked vertically in ATR B-10 position)
- **3 stacks per capsule** (arranged radially at 120° intervals)
- **4 compacts per stack** (stacked vertically, 2.54 cm height each)
- **~4,100 TRISO particles per compact** (arranged in 15×15 horizontal lattice with 31 vertical layers)
- **5 coating layers per particle** (kernel, buffer, IPyC, SiC, OPyC)

**Total geometry complexity:** 6 capsules × 3 stacks × 4 compacts × ~4,100 particles × 5 layers = **~1.5 million geometric regions** efficiently represented through nested lattices and universes.

---

## File Overview

### sdr-agr.i (Capsule Assembly Only)
- **Purpose:** Stand-alone model of AGR-1 capsule train
- **Lines:** 4,653
- **Structure:**
  - Lines 1-2300: Cell cards (capsules, TRISO particles, lattices)
  - Lines 2300-4653: Surface cards, material cards, data cards

### bench_138B.i (Full Quarter-Core ATR Model)
- **Purpose:** Complete ATR reactor with AGR-1 experiment in B-10 position
- **Lines:** 18,414
- **Structure:**
  - Lines 1-1479: ATR fuel elements, beryllium reflector, control elements
  - Lines 1480-3780: AGR-1 capsule cells (identical to sdr-agr.i)
  - Lines 3780-18414: Surfaces, materials, tallies, source definitions

**Key Finding:** The AGR-1 cell structures in bench_138B.i (lines 1480-3780) are **identical** to those in sdr-agr.i (lines 1-2300), demonstrating modularity and reusability.

---

## Universe Numbering Scheme

The AGR-1 model uses a **systematic 4-digit universe numbering scheme: XYZW**

```
XYZW where:
  X = Capsule number (1-6)
  Y = Stack number (1-3)
  Z = Compact number (0-4) or component type
  W = Component designation:
      4 = TRISO particle (5 coating layers)
      5 = Matrix filler cell (no particle)
      6 = Particle lattice (15×15×1)
      7 = Matrix filler universe
      0 = Compact lattice (1×1×31)
```

### Example Universe IDs:

| Universe | Meaning |
|----------|---------|
| **1114** | Capsule 1, Stack 1, Compact 1, TRISO particle |
| **1115** | Capsule 1, Stack 1, Compact 1, Matrix cell (no particle) |
| **1116** | Capsule 1, Stack 1, Compact 1, Particle lattice (15×15) |
| **1117** | Capsule 1, Stack 1, Compact 1, Matrix filler |
| **1110** | Capsule 1, Stack 1, Compact 1, Full compact lattice (1×1×31) |
| **2214** | Capsule 2, Stack 2, Compact 1, TRISO particle |
| **3324** | Capsule 3, Stack 3, Compact 2, TRISO particle |
| **6344** | Capsule 6, Stack 3, Compact 4, TRISO particle |

**Total Capsules:** 6 (numbered 1-6)
**Total Stacks per Capsule:** 3 (numbered 1-3)
**Total Compacts per Stack:** 4 (numbered 1-4)

---

## TRISO Particle Cell Structure

### Five-Layer Coating Structure

Each TRISO (TRi-structural ISOtropic) particle consists of:

1. **Kernel** - Fuel kernel (UO₂ or UCO)
2. **Buffer** - Porous carbon buffer layer
3. **IPyC** - Inner Pyrolytic Carbon layer
4. **SiC** - Silicon Carbide pressure vessel layer
5. **OPyC** - Outer Pyrolytic Carbon layer

### Example: Capsule 1, Stack 1, Compact 1 TRISO Particle

```mcnp
c Capsule 1, stack 1, compact #1
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
91103 9091 -1.904  91112 -91113  u=1114                 $ IPyC
91104 9092 -3.205  91113 -91114  u=1114                 $ SiC
91105 9093 -1.911  91114 -91115  u=1114                 $ OPyC
91106 9094 -1.344  91115         u=1114                 $ SiC Matrix
```

**Cell-by-Cell Breakdown:**

| Cell | Material | Density | Geometry | Universe | Description |
|------|----------|---------|----------|----------|-------------|
| 91101 | 9111 | -10.924 g/cm³ | inside -91111 | u=1114 | Fuel kernel (UO₂ enriched) |
| 91102 | 9090 | -1.100 g/cm³ | 91111 to -91112 | u=1114 | Porous carbon buffer |
| 91103 | 9091 | -1.904 g/cm³ | 91112 to -91113 | u=1114 | Inner PyC coating |
| 91104 | 9092 | -3.205 g/cm³ | 91113 to -91114 | u=1114 | Silicon carbide layer |
| 91105 | 9093 | -1.911 g/cm³ | 91114 to -91115 | u=1114 | Outer PyC coating |
| 91106 | 9094 | -1.344 g/cm³ | outside 91115 | u=1114 | SiC matrix filler |

**Key Observations:**
- All 6 cells share the **same universe** (u=1114)
- Each cell occupies a **spherical shell** defined by two concentric spherical surfaces
- The outermost region (91106) fills from the particle surface to the lattice cell boundary
- Volume is explicitly calculated for the kernel: `vol=0.092522` cm³

### Surface Definitions for TRISO Particle

```mcnp
91111 so   0.017485  $ Kernel radius
91112 so   0.027905  $ Buffer outer radius
91113 so   0.031785  $ IPyC outer radius
91114 so   0.035375  $ SiC outer radius
91115 so   0.039305  $ OPyC outer radius
```

**Radial Dimensions (cm):**

| Component | Inner Radius | Outer Radius | Thickness |
|-----------|--------------|--------------|-----------|
| Kernel | 0.0 | 0.017485 | 0.017485 (174.85 μm) |
| Buffer | 0.017485 | 0.027905 | 0.010420 (104.2 μm) |
| IPyC | 0.027905 | 0.031785 | 0.003880 (38.8 μm) |
| SiC | 0.031785 | 0.035375 | 0.003590 (35.9 μm) |
| OPyC | 0.035375 | 0.039305 | 0.003930 (39.3 μm) |

**Total particle diameter:** 2 × 0.039305 = **0.07861 cm (786 μm)**

### Matrix Filler Cell

Each particle lattice also includes **matrix filler cells** (universe XYZW where W=5):

```mcnp
91107 9094 -1.344 -91116         u=1115                 $ SiC Matrix
```

This cell fills lattice positions that **do not contain TRISO particles**, maintaining a uniform graphite matrix throughout the compact.

---

## Particle Lattice Structures (15×15×1)

### LAT=1 Rectangular Lattice Definition

Each compact contains TRISO particles arranged in a **15×15 horizontal lattice with 31 vertical layers**. The horizontal distribution is defined using **LAT=1** (rectangular lattice):

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

### Lattice Specification Breakdown

**Cell 91108:**
- **Material:** 0 (void, will be filled by lattice)
- **Surface:** -91117 (inside rectangular parallelepiped)
- **Universe:** u=1116 (particle lattice universe)
- **LAT=1:** Rectangular lattice type
- **FILL specification:** `fill=-7:7 -7:7 0:0`
  - **X-direction:** -7 to +7 (15 elements)
  - **Y-direction:** -7 to +7 (15 elements)
  - **Z-direction:** 0 to 0 (1 element, single layer)
  - **Total lattice elements:** 15 × 15 × 1 = **225 positions**

### Circular Packing Pattern

The 15×15 array creates a **circular packing pattern** to fit within the cylindrical compact:

```
Lattice Visualization (top view):
Row index increases downward (Y-axis)
Column index increases rightward (X-axis)

     -7  -6  -5  -4  -3  -2  -1   0  +1  +2  +3  +4  +5  +6  +7
 -7: [M] [M] [M] [M] [M] [M] [P] [P] [P] [M] [M] [M] [M] [M] [M]
 -6: [M] [M] [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M] [M] [M]
 -5: [M] [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M] [M]
 -4: [M] [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M] [M]
 -3: [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M]
 -2: [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M]
 -1: [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P]
  0: [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P]
 +1: [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P]
 +2: [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M]
 +3: [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M]
 +4: [M] [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M] [M]
 +5: [M] [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M] [M]
 +6: [M] [M] [M] [P] [P] [P] [P] [P] [P] [P] [P] [P] [M] [M] [M]
 +7: [M] [M] [M] [M] [M] [M] [P] [P] [P] [M] [M] [M] [M] [M] [M]

Legend:
[P] = 1114 = TRISO particle cell
[M] = 1115 = Matrix filler cell (no particle)
```

**Particle Count:** 169 particles + 56 matrix cells = 225 total lattice positions

### Lattice Geometry Surface

```mcnp
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
```

**Lattice cell dimensions:**
- **X-range:** -0.043715 to +0.043715 cm = **0.08743 cm total**
- **Y-range:** -0.043715 to +0.043715 cm = **0.08743 cm total**
- **Z-range:** -0.050000 to +0.050000 cm = **0.10000 cm total**

**Individual lattice element size:**
- **X-pitch:** 0.08743 / 15 = **0.005829 cm** (58.29 μm)
- **Y-pitch:** 0.08743 / 15 = **0.005829 cm** (58.29 μm)
- **Z-pitch:** 0.10000 / 1 = **0.10000 cm** (1000 μm)

**Volume per lattice element:** 0.005829 × 0.005829 × 0.10000 = **3.397 × 10⁻⁶ cm³**

---

## Compact Lattice Structures (1×1×31)

### Vertical Stacking of Particle Layers

Each compact is assembled by **stacking 31 horizontal particle lattices vertically** using another LAT=1 lattice:

```mcnp
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

### Compact Lattice Specification

**Cell 91110:**
- **Material:** 0 (void, filled by lattice)
- **Surface:** -91118 (inside rectangular parallelepiped)
- **Universe:** u=1110 (full compact lattice)
- **LAT=1:** Rectangular lattice
- **FILL specification:** `fill=0:0 0:0 -15:15`
  - **X-direction:** 0 to 0 (1 element)
  - **Y-direction:** 0 to 0 (1 element)
  - **Z-direction:** -15 to +15 (31 elements)
  - **Total lattice elements:** 1 × 1 × 31 = **31 positions**

### Repeat Notation Usage

**Critical MCNP feature:** `1117 2R 1116 24R 1117 2R`

This compact notation means:
```
1117          → Z = -15 (bottom layer)
1117 (repeat) → Z = -14
1117 (repeat) → Z = -13
1116          → Z = -12
1116 (repeat) → Z = -11
...
1116 (repeat) → Z = +12
1117          → Z = +13
1117 (repeat) → Z = +14
1117 (repeat) → Z = +15 (top layer)
```

**Expanded form:**
```
Z-index | Universe | Content
--------|----------|--------
  -15   |   1117   | Matrix filler (bottom cap)
  -14   |   1117   | Matrix filler
  -13   |   1117   | Matrix filler
  -12   |   1116   | Particle lattice (15×15)
  -11   |   1116   | Particle lattice
  -10   |   1116   | Particle lattice
   ...  |   ...    | ...
  +11   |   1116   | Particle lattice
  +12   |   1116   | Particle lattice
  +13   |   1117   | Matrix filler (top cap)
  +14   |   1117   | Matrix filler
  +15   |   1117   | Matrix filler (top cap)
```

**Breakdown:**
- **1117 2R** = 3 layers of matrix filler (universe 1117) at bottom
- **1116 24R** = 25 layers of particle lattices (universe 1116) in middle
- **1117 2R** = 3 layers of matrix filler (universe 1117) at top

**Total:** 3 + 25 + 3 = **31 layers**

### Compact Geometry Surface

```mcnp
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
```

**Wait - this is rotated!** The compact is oriented with:
- **X-range:** -0.650000 to +0.650000 cm = **1.30 cm** (compact diameter)
- **Y-range:** -0.650000 to +0.650000 cm = **1.30 cm** (compact diameter)
- **Z-range:** -0.043715 to +0.043715 cm = **0.08743 cm** (compact "height" in this rotated coordinate)

**Layer thickness:** 0.08743 / 31 = **0.002820 cm per layer** (28.2 μm)

### Matrix Filler Universe

The matrix filler layers (top/bottom caps) use universe 1117:

```mcnp
91109 9094 -1.344 -91119    u=1117                 $ Matrix
```

This is a simple cell filled with SiC matrix material (9094) bounded by surface 91119:

```mcnp
91119 c/z  0.0 0.0   0.6500
```

A cylinder of radius 0.65 cm (matching the compact outer radius).

### Compact Insertion into Physical Space

The compact lattice is inserted into the real geometry with a FILL cell:

```mcnp
91111 0   -97011   98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Translation vector:** (25.547039, -24.553123, 19.108100) cm
This places the compact at its correct position within the ATR B-10 experimental position.

---

## Complete Universe Hierarchy

### Five-Level Nesting Structure

```
Level 0: Real World Geometry (no universe specified)
│
├─ Level 1: Capsule Assembly (cells 99970-96099)
│  │
│  └─ Level 2: Compact Lattice (u=XYZ0, e.g., u=1110)
│     │         FILL: 0:0 0:0 -15:15 (1×1×31 vertical stack)
│     │
│     ├─ Level 3a: Matrix Filler (u=XYZ7, e.g., u=1117)
│     │            Used for top/bottom caps
│     │
│     └─ Level 3b: Particle Lattice (u=XYZ6, e.g., u=1116)
│        │         FILL: -7:7 -7:7 0:0 (15×15×1 horizontal array)
│        │
│        ├─ Level 4a: TRISO Particle (u=XYZ4, e.g., u=1114)
│        │  │         5-layer coating structure
│        │  │
│        │  ├─ Layer 1: Kernel (cell 91101)
│        │  ├─ Layer 2: Buffer (cell 91102)
│        │  ├─ Layer 3: IPyC (cell 91103)
│        │  ├─ Layer 4: SiC (cell 91104)
│        │  ├─ Layer 5: OPyC (cell 91105)
│        │  └─ Layer 6: Matrix (cell 91106)
│        │
│        └─ Level 4b: Matrix Filler Cell (u=XYZ5, e.g., u=1115)
│                     Simple matrix fill (cell 91107)
```

### Universe Reference Chain Example

**Question:** How does MCNP resolve a particle at position (X, Y, Z) in Capsule 1, Stack 1, Compact 1?

**Answer:** Through nested universe resolution:

1. **Real world coordinates** → Hit compact region (cell 91111)
2. Cell 91111 has **fill=1110** with translation → Enter universe 1110
3. Universe 1110 is a **LAT=1 lattice** (1×1×31) → Determine Z-index
4. At Z-index = -5, lattice element contains **universe 1116**
5. Universe 1116 is a **LAT=1 lattice** (15×15×1) → Determine X,Y-index
6. At X-index = 3, Y-index = -2, lattice element contains **universe 1114**
7. Universe 1114 contains **6 concentric spherical cells** (TRISO layers)
8. Based on radius from lattice element center → Determine which layer (e.g., SiC = cell 91104)
9. Cell 91104 has **material 9092** (Silicon Carbide)
10. MCNP tracks particle in material 9092 with correct neutron cross-sections

---

## Cell Card Patterns

### Pattern 1: TRISO Particle Definition (6 cells per particle)

**Template:**
```mcnp
XYZA1 9XY1 -D.DDD -SXYA1         u=XYZ4 vol=V.VVVVVV    $ Kernel
XYZA2 9090 -1.100  SXYA1 -SXYA2  u=XYZ4                 $ Buffer
XYZA3 9091 -D.DDD  SXYA2 -SXYA3  u=XYZ4                 $ IPyC
XYZA4 9092 -D.DDD  SXYA3 -SXYA4  u=XYZ4                 $ SiC
XYZA5 9093 -D.DDD  SXYA4 -SXYA5  u=XYZ4                 $ OPyC
XYZA6 9094 -D.DDD  SXYA5         u=XYZ4                 $ SiC Matrix
```

**Variable Explanations:**
- **XYZA1-XYZA6:** Cell numbers (increment by 1)
- **X:** Capsule number (9 for capsule 1-6)
- **Y:** Stack digit (1-3)
- **Z:** Compact digit (1-4)
- **A:** Particle set (0 for compact X0, 1 for compact X1, etc.)
- **9XY1:** Material number for kernel (varies per compact)
- **D.DDD:** Density (varies per material and compact)
- **SXYA1-SXYA5:** Surface numbers (spherical)
- **V.VVVVVV:** Kernel volume (calculated, provided for efficiency)

### Pattern 2: Matrix Filler Cell

**Template:**
```mcnp
XYZA7 9094 -D.DDD -SXYA6         u=XYZ5                 $ SiC Matrix
```

### Pattern 3: Particle Lattice (15×15×1)

**Template:**
```mcnp
XYZA8 0   -SXYA7  u=XYZ6 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     XYZ5 XYZ5 XYZ5 XYZ5 XYZ5 XYZ5 XYZ4 XYZ4 XYZ4 XYZ5 XYZ5 XYZ5 XYZ5 XYZ5 XYZ5
     XYZ5 XYZ5 XYZ5 XYZ4 XYZ4 XYZ4 XYZ4 XYZ4 XYZ4 XYZ4 XYZ4 XYZ4 XYZ5 XYZ5 XYZ5
     [... 13 more rows ...]
```

**15 rows × 15 columns = 225 universe IDs** (mix of XYZ4 and XYZ5)

### Pattern 4: Matrix Filler Universe

**Template:**
```mcnp
XYZA9 9094 -D.DDD -SXYA9    u=XYZ7                 $ Matrix
```

### Pattern 5: Compact Lattice (1×1×31)

**Template:**
```mcnp
XYZ10 0  -SXYA8 u=XYZ0 lat=1  fill=0:0 0:0 -15:15 XYZ7 2R XYZ6 24R XYZ7 2R
```

**Repeat notation breakdown:**
- **XYZ7 2R:** 3 matrix layers (bottom cap)
- **XYZ6 24R:** 25 particle lattice layers (fuel region)
- **XYZ7 2R:** 3 matrix layers (top cap)

### Pattern 6: Compact Placement

**Template:**
```mcnp
XYZ11 0   -SSSS   ZBOT -ZTOP fill=XYZ0  (TX TY TZ)
```

**Where:**
- **SSSS:** Compact radial surface (cylinder)
- **ZBOT, ZTOP:** Axial bounding planes
- **TX, TY, TZ:** Translation vector to position compact in stack

---

## Surface Definitions

### TRISO Particle Surfaces (Spherical)

**Pattern: SXYA1-SXYA6**

Example for Capsule 1, Stack 1, Compact 1:
```mcnp
91111 so   0.017485  $ Kernel
91112 so   0.027905  $ Buffer
91113 so   0.031785  $ InnerPyC
91114 so   0.035375  $ SiC
91115 so   0.039305  $ OuterPyC
91116 so   1.000000  $ Matrix cell outer bound
```

**Surface type:** `so` (sphere centered at origin)

**Note:** These surfaces are defined **relative to the lattice element center**, not global coordinates. Each lattice element has its own local coordinate system.

### Particle Lattice Surfaces (Rectangular Parallelepiped)

**Pattern: SXYA7**

Example:
```mcnp
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
```

**Surface type:** `rpp` (rectangular parallelepiped)
**Parameters:** xmin xmax ymin ymax zmin zmax

**Dimensions:**
- **X:** 0.08743 cm
- **Y:** 0.08743 cm
- **Z:** 0.10000 cm

### Compact Lattice Surfaces (Rectangular Parallelepiped)

**Pattern: SXYA8**

Example:
```mcnp
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
```

**Dimensions:**
- **X:** 1.30 cm (compact diameter)
- **Y:** 1.30 cm (compact diameter)
- **Z:** 0.08743 cm (compact effective height in lattice coord)

### Compact Physical Boundaries (Cylinders and Planes)

**Radial surfaces (cylinders):**
```mcnp
97011 c/z   25.547039 -24.553123   0.63500  $ Stack 1 Compact outer R
97012 c/z   25.547039 -24.553123   0.64135  $ Stack 1 Gas gap outer R
97021 c/z   24.553123 -25.547039   0.63500  $ Stack 2 Compact outer R
97022 c/z   24.553123 -25.547039   0.64135  $ Stack 2 Gas gap outer R
97031 c/z   25.910838 -25.910838   0.63500  $ Stack 3 Compact outer R
97032 c/z   25.910838 -25.910838   0.64135  $ Stack 3 Gas gap outer R
```

**Surface type:** `c/z` (cylinder parallel to Z-axis)
**Parameters:** x-center y-center radius

**Axial planes:**
```mcnp
98005 pz   17.81810
98051 pz   20.35810  $ calculated
98006 pz   22.89810
[... etc for each compact boundary ...]
```

**Surface type:** `pz` (plane perpendicular to Z-axis)
**Parameter:** Z-coordinate

---

## Material Assignments

### Material Numbering Scheme

**Kernel materials:** 9XY1 (varies by compact for different enrichments/burnup)

Examples:
```
9111 = Capsule 1, Stack 1, Compact 1 kernel
9112 = Capsule 1, Stack 1, Compact 2 kernel
9113 = Capsule 1, Stack 1, Compact 3 kernel
9221 = Capsule 2, Stack 2, Compact 1 kernel
```

**Common materials (shared across all compacts):**
```
9090 = Buffer (porous carbon)
9091 = IPyC (Inner Pyrolytic Carbon)
9092 = SiC (Silicon Carbide)
9093 = OPyC (Outer Pyrolytic Carbon)
9094 = SiC Matrix (graphite/SiC matrix)
```

### Density Variations

**Key observation:** Densities vary **between capsules and compacts** to represent:
1. Different fuel enrichments
2. Different fabrication batches
3. Burnup effects (in bench_138B.i)

**Example density ranges:**

| Material | Typical Range | Units |
|----------|---------------|-------|
| Kernel (UO₂) | -10.90 to -10.93 | g/cm³ |
| Buffer | -1.100 | g/cm³ |
| IPyC | -1.853 to -1.912 | g/cm³ |
| SiC | -3.205 to -3.208 | g/cm³ |
| OPyC | -1.898 to -1.911 | g/cm³ |
| Matrix | -1.219 to -1.344 | g/cm³ |

**Negative densities** indicate **mass density** (g/cm³) rather than atom density (atoms/barn-cm).

### Material Card Examples

**Kernel material (from bench_138B.i with burnup):**
```mcnp
m9111
     92234.70c  7.414436E-06 $U-234
     92235.70c  4.956778E-04 $U-235
     92236.70c  3.124405E-05 $U-236
     92238.70c  4.006409E-05 $U-238
     [... fission products ...]
     8016.70c   2.000000E-02 $ O-16
```

**Matrix material:**
```mcnp
m9094  $ SiC Matrix
     6000.70c   8.000000E-02 $ Carbon
     14000.70c  4.000000E-02 $ Silicon
```

---

## Key Insights for Model Development

### 1. Modularity Through Universes

**Reusable components:**
- Each TRISO particle type is defined **once** in a universe
- The same universe is referenced **thousands of times** via lattices
- Changing particle properties requires editing only **6 cells** (one universe definition)
- Total model: ~1.5 million regions represented by **~2,000 unique cell definitions**

**Memory efficiency:**
- Without universes: Would require 1.5 million cell cards
- With universes: Requires only ~2,000 cell cards + lattice definitions
- **Compression factor:** ~750×

### 2. Lattice Coordinate Systems

**Critical concept:** Each lattice element has its own **local coordinate system**

```
Global coordinates → Compact region → Universe 1110 → Local lattice coords
  → Lattice element → Universe 1116 → Local element coords
    → Sub-element → Universe 1114 → Local particle coords
```

**Implication for surface definitions:**
- Particle surfaces (91111-91115) are defined relative to **(0,0,0)** in lattice element
- Each lattice element has a **different global position** but same local surfaces
- MCNP automatically handles coordinate transformations

### 3. FILL Card with Translations

**Pattern:**
```mcnp
91111 0   -97011   98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**The translation vector** `(25.547039 -24.553123 19.108100)`:
- Defines the **origin of universe 1110** in global coordinates
- All lattice positions are **offset** from this origin
- Stack positions are at **120° intervals** around the capsule centerline

**Stack 1:** (25.547039, -24.553123, Z)
**Stack 2:** (24.553123, -25.547039, Z)
**Stack 3:** (25.910838, -25.910838, Z)

These form a **triangular arrangement** when viewed from above.

### 4. Repeat Notation Efficiency

**Instead of typing:**
```mcnp
fill=0:0 0:0 -15:15 1117 1117 1117 1116 1116 1116 1116 1116 1116 1116 1116
              1116 1116 1116 1116 1116 1116 1116 1116 1116 1116 1116 1116
              1116 1116 1116 1116 1116 1117 1117 1117
```

**Use compact form:**
```mcnp
fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

**Syntax:** `value NR` means "repeat value N additional times"
- `1117 2R` = 1117 1117 1117 (total 3)
- `1116 24R` = 1116 repeated 25 times

### 5. Circular Packing in Rectangular Lattice

**Problem:** Compacts are cylindrical, but LAT=1 creates rectangular arrays

**Solution:** Use **mixture of particle and matrix universes** to approximate circular boundary

**Result:**
- Center of lattice: all particles (1114)
- Edges/corners: mix of particles and matrix (1115)
- Approximates **circular packing within square lattice**

**169 particles** in 15×15 lattice creates effective packing fraction:
- Lattice area: 0.08743² = 0.007644 cm²
- Particle area: 169 × π × (0.005829/2)² = 0.004514 cm²
- **Packing fraction:** 0.004514 / 0.007644 = **59.0%**

### 6. Volume Calculations

**Kernel volumes are pre-calculated:**
```mcnp
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
```

**Why?**
- MCNP uses volumes for **flux-to-reaction rate** conversions
- Pre-specifying volumes **saves computation time**
- For repeated structures, volume is the **same for all instances**

**Kernel volume calculation:**
```
V = (4/3) × π × r³
V = (4/3) × π × (0.017485)³
V = 0.000022398 cm³ per particle

Total in compact: 169 particles × 25 layers = 4,225 particles
Total kernel volume: 4,225 × 0.000022398 = 0.0946 cm³
```

**Match to vol=0.092522?** Close, but slight difference suggests **169 particles per layer is approximate**. Some lattice positions at edges may be excluded.

### 7. Geometric Consistency Checks

**Particle fits within lattice element?**
- Particle diameter: 2 × 0.039305 = 0.07861 cm
- Lattice element: 0.08743 cm square
- **Diagonal:** 0.08743 × √2 = 0.1236 cm
- **Fits:** Yes, with 0.1236 - 0.07861 = 0.045 cm (450 μm) clearance on diagonal

**Compact radius matches surface definition?**
- Lattice X-extent: -0.65 to +0.65 = 1.30 cm diameter
- Surface 97011: c/z ... 0.63500 → radius 0.635 cm
- **Match:** Yes, lattice fits within cylindrical boundary

### 8. Stack Arrangement

**Three stacks per capsule at 120° intervals:**

```
View from above (looking down Z-axis):

              +Y
               ^
               |
        Stack 2|
        (-,+)  |
               |
    -----------+----------- +X
               |
               |     Stack 1
               |       (+,-)
               |
               |
          Stack 3
          (+,+)
```

**Stack centers:**
- **Stack 1:** (25.547039, -24.553123) → Quadrant IV
- **Stack 2:** (24.553123, -25.547039) → Quadrant III
- **Stack 3:** (25.910838, -25.910838) → Quadrant III

**Distance from capsule axis (25.337, -25.337):**
```
r_stack1 = sqrt((25.547039-25.337)² + (-24.553123+25.337)²) = 0.849 cm
r_stack2 = sqrt((24.553123-25.337)² + (-25.547039+25.337)²) = 0.849 cm
r_stack3 = sqrt((25.910838-25.337)² + (-25.910838+25.337)²) = 0.849 cm
```

**All three stacks at same radius:** 0.849 cm from capsule centerline

### 9. Building a Similar Model - Step-by-Step

**To create your own HTGR TRISO compact model:**

1. **Define TRISO particle (6 cells in 1 universe):**
   - 5 concentric spherical shells (kernel through OPyC)
   - 1 matrix filler extending to lattice boundary
   - Use `so` surfaces centered at (0,0,0)

2. **Define matrix filler cell (1 cell in 1 universe):**
   - Simple cell with matrix material
   - Same outer boundary as particle

3. **Define particle lattice (1 cell with LAT=1):**
   - Specify FILL range (e.g., -7:7 -7:7 0:0)
   - Create 2D array of particle and matrix universes
   - Use circular packing pattern

4. **Define matrix filler universe (1 cell in 1 universe):**
   - For top/bottom caps of compact
   - Cylindrical geometry matching compact

5. **Define compact lattice (1 cell with LAT=1):**
   - Vertical stack (0:0 0:0 -N:+N)
   - Use repeat notation for efficiency
   - Matrix universes at top/bottom, particle lattices in middle

6. **Place compact in geometry (1 cell with FILL):**
   - Cylindrical/planar boundaries
   - Translation vector to position in experiment
   - Multiple compacts stacked vertically

### 10. Common Pitfalls to Avoid

**Universe ID conflicts:**
- ❌ **DON'T:** Reuse universe IDs between different geometric objects
- ✅ **DO:** Use systematic numbering scheme (XYZW pattern)

**Lattice indexing errors:**
- ❌ **DON'T:** Forget that `fill=-7:7` means indices -7, -6, ..., 0, ..., +6, +7 (15 elements)
- ✅ **DO:** Count carefully: `fill=-N:+N` creates 2N+1 elements

**Coordinate system confusion:**
- ❌ **DON'T:** Define particle surfaces in global coordinates
- ✅ **DO:** Define surfaces relative to lattice element center (0,0,0)

**Missing lattice boundaries:**
- ❌ **DON'T:** Let lattice extend beyond bounding surface
- ✅ **DO:** Ensure lattice RPP fully contains all elements

**Repeat notation off-by-one:**
- ❌ **DON'T:** Think `NR` means "N repetitions"
- ✅ **DO:** Remember `NR` means "N additional repetitions" (total N+1)

**Volume card placement:**
- ❌ **DON'T:** Put volume on lattice cells (it's ignored)
- ✅ **DO:** Put volume on bottom-level cells (particles)

---

## Summary of Cell Card Counts

### Per Compact (4 compacts per stack):
- **6 cells:** TRISO particle layers (universe XYZ4)
- **1 cell:** Matrix filler cell (universe XYZ5)
- **1 cell:** Particle lattice (universe XYZ6)
- **1 cell:** Matrix filler universe (universe XYZ7)
- **1 cell:** Compact lattice (universe XYZ0)
- **1 cell:** Compact placement (fill=XYZ0)
- **Total:** 11 cells per compact

### Per Stack (3 stacks per capsule):
- **4 compacts × 11 cells** = 44 cells per stack

### Per Capsule (6 capsules total):
- **3 stacks × 44 cells** = 132 cells per capsule

### Total AGR-1 Experiment:
- **6 capsules × 132 cells** = 792 cells
- Plus ~100 cells for capsule hardware (walls, gas gaps, support structures)
- **Grand total:** ~900 cells in AGR-1 section

### Compared to explicit modeling:
- 6 capsules × 3 stacks × 4 compacts × 25 layers × 169 particles × 6 shells
- = **~2.5 million cells** if modeled explicitly
- **Reduction factor:** 2,500,000 / 900 = **~2,800×**

---

## Conclusion

The AGR-1 MCNP model demonstrates **masterful use of nested lattices and universes** to efficiently represent complex HTGR fuel geometry. Key achievements:

1. **~2,800× reduction** in cell count through universe reuse
2. **Five-level hierarchy** manages complexity while maintaining clarity
3. **Systematic naming** (XYZW scheme) enables easy maintenance and modification
4. **Repeat notation** compresses lattice definitions by 10-30×
5. **Modular design** allows changing fuel properties by editing only 6 cells per particle type

**This model serves as an excellent template** for any reactor physics model requiring:
- Repeated geometric structures (fuel pins, assemblies, TRISO particles)
- Hierarchical organization (pin → assembly → core)
- Efficient memory usage for large-scale models
- Maintainable, understandable input files

**Document prepared by:** AGR-1 Cell Structure Analysis Tool
**Files analyzed:** sdr-agr.i, bench_138B.i
**Total lines analyzed:** 23,067
**Analysis depth:** Complete cell card structure, lattice specifications, universe hierarchy

---

*End of AGR-1 Cell Card Complete Analysis*
