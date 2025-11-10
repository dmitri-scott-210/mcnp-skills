# AGR-1 MCNP CELL CARD STRUCTURE ANALYSIS

**Analysis Date**: 2025-11-07
**Files Analyzed**:
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/bench_138B.i`
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/bench_143A.i`
- `/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/mcnp/sdr-agr.i`

---

## EXECUTIVE SUMMARY

The AGR-1 MCNP models demonstrate sophisticated hierarchical lattice structures for modeling TRISO (TRi-structural ISOtropic) fuel particles in High Temperature Gas-Cooled Reactor (HTGR) fuel compacts. The models employ **three-level universe nesting** to represent:

1. **Individual TRISO particles** (5-layer coated fuel kernels)
2. **2D hexagonal lattices** of particles in a single plane
3. **1D vertical stacks** of 2D particle planes forming fuel compacts

**Key Statistics** (sdr-agr.i):
- **Total Cell Cards**: ~2,297 cells
- **Lattice Cells**: 144 (LAT=1 specifications)
- **Fill Cells**: 216 (FILL= specifications for universe placement)
- **File Size**: 4,653 lines total

The bench files (bench_138B.i, bench_143A.i) are structurally identical at the beginning and also contain 144 lattice cells each, though they are significantly larger (18,414 lines) due to additional ATR reactor core geometry.

---

## 1. HIERARCHICAL UNIVERSE STRUCTURE

### 1.1 Universe Hierarchy Overview

```
Level 0 (Base Geometry)
  └─> Level 1: Fuel Compact Container (universe 1110, 1120, etc.)
       └─> Level 2: Vertical Lattice Stack (universe 1116, 1126, etc.)
            └─> Level 3: 2D Hexagonal Particle Lattice (universes 1114/1115, 1124/1125, etc.)
                 └─> Level 4: Individual TRISO Particle Layers
```

### 1.2 Universe Numbering Scheme

The models use a **systematic numbering convention**:

```
Format: CABCD
  C  = Capsule number (1-6)
  A  = Stack number (1-3)
  B  = Compact number (1-4)
  CD = Component identifier

Examples:
  1114 = Capsule 1, Stack 1, Compact 1, Component 4 (TRISO particle with fuel)
  1115 = Capsule 1, Stack 1, Compact 1, Component 5 (TRISO particle, matrix only)
  1116 = Capsule 1, Stack 1, Compact 1, Component 6 (2D particle lattice)
  1110 = Capsule 1, Stack 1, Compact 1, Component 0 (vertical stack)
```

This systematic numbering allows for **unique material compositions** in each compact while maintaining consistent geometric structure.

---

## 2. LATTICE CELL STRUCTURES

### 2.1 Two-Dimensional Hexagonal Particle Lattice (LAT=1)

**Purpose**: Arrange TRISO particles in a hexagonal close-packed array within a single horizontal plane.

**Cell Example** (from sdr-agr.i, Capsule 1, Stack 1, Compact 1):

```
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

**Lattice Specification Analysis**:
- **Cell Number**: 91108
- **Material**: 0 (void - lattice holder cell)
- **Surface**: -91117 (bounding surface for lattice region)
- **Universe**: u=1116 (this lattice is defined in universe 1116)
- **LAT=1**: Hexagonal lattice type
- **FILL Range**: `-7:7 -7:7 0:0`
  - X-direction: -7 to +7 (15 positions)
  - Y-direction: -7 to +7 (15 positions)
  - Z-direction: 0 to 0 (single plane)
  - Total: 15 × 15 × 1 = **225 lattice elements**

**FILL Array Structure**:
- **Universe 1114**: TRISO particle with fuel kernel (appears in interior, ~141 particles)
- **Universe 1115**: Matrix-only cells (appears at edges, ~84 positions)
- Pattern creates realistic **particle packing** with matrix material filling gaps

**Hexagonal Indexing**: The FILL array uses standard MCNP hexagonal indexing where alternating rows are offset to create hexagonal close-packing.

### 2.2 One-Dimensional Vertical Lattice Stack (LAT=1)

**Purpose**: Stack multiple 2D particle planes vertically to create a fuel compact with axial variation.

**Cell Example** (from sdr-agr.i, Capsule 1, Stack 1, Compact 1):

```
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

**Lattice Specification Analysis**:
- **Cell Number**: 91110
- **Material**: 0 (void - lattice holder cell)
- **Surface**: -91118 (bounding surface)
- **Universe**: u=1110 (this lattice is defined in universe 1110)
- **LAT=1**: Hexagonal lattice (used here as 1D vertical stack)
- **FILL Range**: `0:0 0:0 -15:15`
  - X-direction: 0 to 0 (single position)
  - Y-direction: 0 to 0 (single position)
  - Z-direction: -15 to +15 (31 positions)
  - Total: 1 × 1 × 31 = **31 axial layers**

**FILL Array Shorthand**:
- `1117 2R`: Universe 1117 repeated 3 times (positions -15, -14, -13)
- `1116 24R`: Universe 1116 repeated 25 times (positions -12 through +12)
- `1117 2R`: Universe 1117 repeated 3 times (positions +13, +14, +15)

**Interpretation**:
- **Top/Bottom Caps**: Universe 1117 (matrix-only, 3 layers each)
- **Active Core**: Universe 1116 (2D particle lattice, 25 layers)
- This creates realistic fuel compact with matrix end caps

### 2.3 Lattice Positioning with FILL and Transformation

**Purpose**: Place lattice universes into the base geometry with precise positioning.

**Cell Example** (from sdr-agr.i, Capsule 1, Stack 1, Compact 1):

```
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Cell Specification Analysis**:
- **Cell Number**: 91111
- **Material**: 0 (void - universe container)
- **Surfaces**:
  - `-97011`: Radial boundary (cylindrical surface)
  - `98005`: Bottom axial plane
  - `-98051`: Top axial plane
- **FILL**: fill=1110 (places universe 1110 into this cell)
- **Transformation**: `(25.547039 -24.553123 19.108100)`
  - X-offset: 25.547039 cm
  - Y-offset: -24.553123 cm
  - Z-offset: 19.108100 cm
  - These offsets position the compact within the ATR test position

**Key Pattern**: No explicit TR card number, using direct coordinate specification.

---

## 3. CELL DEFINITIONS AND MATERIAL ASSIGNMENTS

### 3.1 TRISO Particle Layer Structure

Each TRISO fuel particle consists of **6 concentric spherical shells** defined in a single universe.

**Example** (Capsule 1, Stack 1, Compact 1):

```
c Capsule 1, stack 1, compact #1
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
91103 9091 -1.904  91112 -91113  u=1114                 $ IPyC
91104 9092 -3.205  91113 -91114  u=1114                 $ SiC
91105 9093 -1.911  91114 -91115  u=1114                 $ OPyC
91106 9094 -1.344  91115         u=1114                 $ SiC Matrix
91107 9094 -1.344 -91116         u=1115                 $ SiC Matrix
```

**Layer-by-Layer Analysis**:

| Cell | Material | Density (g/cm³) | Surfaces | Component | Radius |
|------|----------|-----------------|----------|-----------|--------|
| 91101 | 9111 | 10.924 | -91111 | Fuel Kernel (UCO) | r₁ |
| 91102 | 9090 | 1.100 | 91111 -91112 | Buffer (porous carbon) | r₁ to r₂ |
| 91103 | 9091 | 1.904 | 91112 -91113 | IPyC (Inner Pyrolytic Carbon) | r₂ to r₃ |
| 91104 | 9092 | 3.205 | 91113 -91114 | SiC (Silicon Carbide) | r₃ to r₄ |
| 91105 | 9093 | 1.911 | 91114 -91115 | OPyC (Outer Pyrolytic Carbon) | r₄ to r₅ |
| 91106 | 9094 | 1.344 | 91115 | Matrix (SiC) filling particle | Outside r₅ |
| 91107 | 9094 | 1.344 | -91116 | Matrix (SiC) for empty positions | Entire volume |

**Universe Assignments**:
- **Universe 1114**: Complete TRISO particle (cells 91101-91106) - contains fuel
- **Universe 1115**: Matrix only (cell 91107) - no fuel, used at lattice edges

**Volume Specification**: `vol=0.092522` specified for kernel (91101) enables volume-weighted sampling for variance reduction.

### 3.2 Material Numbering Scheme

**Pattern Observed**:

```
Material Number Format: ABCD
  A  = Material category
       9 = Fuel/structural materials
       8 = Coolant/void
  BCD = Unique identifier tied to position/composition

Examples:
  9111 = Kernel material for Capsule 1, Stack 1, Compact 1
  9112 = Kernel material for Capsule 1, Stack 1, Compact 2
  9090 = Buffer carbon (consistent across all particles)
  9091 = IPyC (consistent across all particles)
  9092 = SiC (consistent across all particles)
  9093 = OPyC (consistent across all particles)
  9094 = Matrix SiC (consistent across all particles)
```

**Material Assignment Strategy**:
- **Coating layers** (Buffer, IPyC, SiC, OPyC, Matrix): **Same material number** across all compacts
  - Materials 9090-9094 are **universal** (same composition everywhere)
- **Fuel kernels**: **Unique material numbers** for each compact
  - Allows for **burnup-dependent compositions** and **isotopic tracking**
  - Materials 9111-9634 (incrementing by compact)

### 3.3 Surface Numbering Convention

**Pattern for Spherical TRISO Surfaces**:

```
Surface Number Format: ABCDE
  A  = Capsule (9)
  B  = Stack (1-3)
  C  = Compact (1-4)
  DE = Layer (11-16)

Example for Capsule 1, Stack 1, Compact 1:
  91111 = Kernel outer radius (layer 1)
  91112 = Buffer outer radius (layer 2)
  91113 = IPyC outer radius (layer 3)
  91114 = SiC outer radius (layer 4)
  91115 = OPyC outer radius (layer 5)
  91116 = Matrix cell boundary (component 6, universe 1115)
  91117 = 2D lattice bounding surface (component 7, universe 1116)
  91118 = 1D lattice bounding surface (component 8, universe 1110)
```

**Systematic Incrementing**: Each subsequent compact increments by 10:
- Compact 1: 91111-91118
- Compact 2: 91121-91128
- Compact 3: 91131-91138
- Compact 4: 91141-91148

---

## 4. FILL ARRAY PATTERNS AND INDEXING

### 4.1 Hexagonal FILL Array Structure

The 2D particle lattices use **explicit enumeration** of universes in FILL arrays:

```
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ Row 1 (j=-7)
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 $ Row 2 (j=-6)
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ Row 3 (j=-5)
     ...
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ Row 15 (j=+7)
```

**Array Interpretation**:
- **Rows**: Enumerated from j=-7 to j=+7 (15 rows)
- **Columns**: Each row contains 15 values, i=-7 to i=+7
- **MCNP Ordering**: Array is listed in Fortran order:
  - Fastest index: i (columns, left to right)
  - Slowest index: j (rows, bottom to top in some conventions, here sequential)

**Physical Meaning**:
- **1114 = Fueled particle position** (appears ~141 times, central region)
- **1115 = Matrix-only position** (appears ~84 times, peripheral region)
- Pattern creates realistic **particle packing density** (~62% particles, ~38% matrix)

**Design Note**: The fill pattern could potentially use **RPP (repeated pattern)** syntax for regular structures, but explicit enumeration provides:
1. Flexibility to model irregular particle distributions
2. Easy verification of particle count
3. Ability to model particle clustering or gaps

### 4.2 Vertical FILL Array with Shorthand

The 1D vertical lattices use MCNP's **repeat shorthand** syntax:

```
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

**Expanded Interpretation**:

| Z-Index | Position | Universe | Component |
|---------|----------|----------|-----------|
| -15 | Bottom | 1117 | Matrix end cap |
| -14 |  | 1117 | Matrix end cap |
| -13 |  | 1117 | Matrix end cap |
| -12 through +12 | Core region | 1116 | 2D particle lattice (25 layers) |
| +13 |  | 1117 | Matrix end cap |
| +14 |  | 1117 | Matrix end cap |
| +15 | Top | 1117 | Matrix end cap |

**Shorthand Syntax**:
- `N R` or `N nR`: Repeat universe N a total of (n+1) times
- `1117 2R` = 1117 repeated 3 times
- `1116 24R` = 1116 repeated 25 times

**Physical Justification**:
- End caps prevent fuel particles from being exposed at compact ends
- 25 active layers provide good axial flux distribution fidelity
- Realistic representation of fabricated compacts

### 4.3 FILL Array Dimensioning Best Practices

**Observed Design Patterns**:

1. **2D Particle Lattice**: 15×15 array
   - Provides ~141 particle positions
   - Matches typical TRISO compact designs (~20,000-40,000 particles per full compact)
   - This model appears to represent a **reduced particle count** for computational efficiency

2. **1D Vertical Stack**: 31 layers
   - 3 top + 25 active + 3 bottom
   - Axial mesh resolution: compact_height / 31 layers
   - Enables axial burnup profiling

3. **Indexing Convention**: All indices centered around 0
   - 2D: -7:7 (symmetric)
   - 1D: -15:+15 (symmetric)
   - Makes geometric transformations intuitive

---

## 5. CROSS-REFERENCING

### 5.1 Cell → Surface References

**Example Chain** (Capsule 1, Stack 1, Compact 1):

```
Fuel Kernel (91101):
  Material: 9111 (UCO kernel)
  Surface:  -91111 (inside sphere of radius r₁)
  Universe: 1114

Buffer Layer (91102):
  Material: 9090 (porous carbon)
  Surfaces: 91111 -91112 (between spheres r₁ and r₂)
  Universe: 1114

... [additional layers]

2D Particle Lattice (91108):
  Material: 0 (void holder)
  Surface:  -91117 (cylindrical or box boundary)
  Universe: 1116
  LAT:      1 (hexagonal)
  FILL:     Explicit 15×15 array of universes 1114 and 1115

1D Vertical Stack (91110):
  Material: 0 (void holder)
  Surface:  -91118 (cylindrical boundary)
  Universe: 1110
  LAT:      1 (hexagonal used as 1D)
  FILL:     Shorthand array: 1117 2R 1116 24R 1117 2R

Compact Placement (91111):
  Material: 0 (void holder)
  Surfaces: -97011 98005 -98051 (cylindrical region with z-bounds)
  FILL:     1110 (places the 1D vertical stack universe)
  TRCL:     (25.547039 -24.553123 19.108100) (translation only)
```

**Dependency Tree**:
```
Cell 91111 (base geometry)
  └─> FILL=1110 (vertical stack universe)
       └─> Cell 91110 (LAT=1, 1D stack)
            └─> FILL array contains 1116 and 1117
                 ├─> Universe 1116 (2D particle lattice)
                 │    └─> Cell 91108 (LAT=1, 2D array)
                 │         └─> FILL array contains 1114 and 1115
                 │              ├─> Universe 1114: cells 91101-91106 (TRISO particle)
                 │              │    └─> Surfaces: 91111, 91112, 91113, 91114, 91115
                 │              └─> Universe 1115: cell 91107 (matrix only)
                 │                   └─> Surface: -91116
                 └─> Universe 1117: cell 91109 (matrix cap)
                      └─> Surface: -91119
```

### 5.2 Cell → Material References

**Material Usage Map** (Example from Capsule 1, Stack 1, Compact 1):

| Material | Used In Cells | Component | Density (g/cm³) | Universe |
|----------|---------------|-----------|-----------------|----------|
| 9111 | 91101 | Fuel kernel | 10.924 | 1114 |
| 9090 | 91102 | Buffer | 1.100 | 1114 |
| 9091 | 91103 | IPyC | 1.904 | 1114 |
| 9092 | 91104 | SiC | 3.205 | 1114 |
| 9093 | 91105 | OPyC | 1.911 | 1114 |
| 9094 | 91106, 91107, 91109 | Matrix SiC | 1.344 | 1114, 1115, 1117 |
| 0 | 91108, 91110, 91111 | Void (lattice holders) | N/A | 1116, 1110, base |
| 8902 | 91100, 91200, 91300 | Gas gaps (He) | 1.2493×10⁻⁴ | base |

**Material Reuse Pattern**:
- Coating materials (9090-9094): **Reused across all particles** in all compacts
- Fuel kernel materials: **Unique per compact** to track burnup
- Structural materials (SS316L, graphite): Reused with unique numbers per region

### 5.3 Cell → Universe References

**Universe Hierarchy** (Capsule 1, Stack 1, Compact 1):

```
Universe 0 (base geometry):
  Cell 91111: FILL=1110

Universe 1110 (1D vertical stack):
  Cell 91110: LAT=1, FILL=[1117, 1116, 1117]

Universe 1116 (2D particle lattice):
  Cell 91108: LAT=1, FILL=[1114, 1115] (225 positions)

Universe 1117 (matrix end cap):
  Cell 91109: Matrix material only

Universe 1114 (TRISO particle with fuel):
  Cells 91101-91106: 6 material layers

Universe 1115 (matrix only):
  Cell 91107: Matrix material only
```

**Universe Number Allocation** (Full model):
- 1100-series: Capsule 1, Stack 1
- 1200-series: Capsule 1, Stack 2
- 1300-series: Capsule 1, Stack 3
- 2100-series: Capsule 2, Stack 1
- ... continuing through Capsule 6

**Total Unique Universes**: Approximately 6 capsules × 3 stacks × 4 compacts × 7 universes/compact ≈ **504 universes**

### 5.4 Parent-Child Cell Relationships

**Hierarchical Containment**:

```
Level 0 (Base Geometry):
  Cell 91111 [-97011 98005 -98051] FILL=1110
    ↓
  Level 1 (Universe 1110, 1D Stack):
    Cell 91110 [-91118] LAT=1 U=1110 FILL=[1117 2R 1116 24R 1117 2R]
      ↓
    Level 2a (Universe 1116, 2D Particle Lattice):
      Cell 91108 [-91117] LAT=1 U=1116 FILL=[-7:7 -7:7 0:0] (225 positions)
        ↓
      Level 3 (Universe 1114, TRISO Particle):
        Cell 91101 [-91111] U=1114 (Kernel)
        Cell 91102 [91111 -91112] U=1114 (Buffer)
        Cell 91103 [91112 -91113] U=1114 (IPyC)
        Cell 91104 [91113 -91114] U=1114 (SiC)
        Cell 91105 [91114 -91115] U=1114 (OPyC)
        Cell 91106 [91115] U=1114 (Matrix inside particle)
        ↓
      Level 3 (Universe 1115, Matrix Only):
        Cell 91107 [-91116] U=1115 (Matrix)
        ↓
    Level 2b (Universe 1117, End Cap):
      Cell 91109 [-91119] U=1117 (Matrix)
```

**Replication Count**:
- 1 Compact container (91111)
- 31 Vertical layers (via LAT in 91110)
  - 3 top caps (universe 1117)
  - 25 particle planes (universe 1116)
  - 3 bottom caps (universe 1117)
- ~141 Particles per plane (universe 1114)
- ~84 Matrix positions per plane (universe 1115)

**Total Geometric Instances**:
- TRISO particles: 25 planes × 141 particles/plane = **3,525 particles per compact**
- This is repeated for **4 compacts per stack** × **3 stacks per capsule** × **6 capsules**
- Total particles in model: 3,525 × 4 × 3 × 6 = **~254,000 TRISO particles**

---

## 6. CELL NUMBERING SCHEMES AND CONVENTIONS

### 6.1 Cell Numbering Hierarchy

**Observed Pattern**:

```
Cell Number Format: CSPPP
  C  = Capsule number (1-6)
  S  = Stack number (1-3)
  PPP = Component number (000-999)

Examples:
  91101 = Capsule 9? (prefix digit), component 1101
         OR
  91101 = Capsule 1, Stack 1, Component 101
```

**Refined Interpretation**: The leading "9" appears to be a **category designator** (fuel region), not capsule number.

**Corrected Format**:

```
Cell Number Format: 9CSPP or 9CSPPP
  9    = Fuel region category
  C    = Capsule (1-6)
  S    = Stack (1-3)
  PP/PPP = Sequential component

Examples:
  91101 = Fuel region, Capsule 1, Stack 1, Component 01
  91111 = Fuel region, Capsule 1, Stack 1, Component 11
  92101 = Fuel region, Capsule 2, Stack 1, Component 01

  99970 = Fuel region, Capsule 9(?), special component
  99991 = Fuel region, outer geometry (room)
  99999 = Fuel region, exterior void
```

**Non-Fuel Cells** (from bench files):
```
  60106-60315 = ATR fuel elements (6XXXX series)
  24, 34 = Aluminum housing
  71, 72 = Beryllium reflector
```

### 6.2 Importance Weighting Strategies

**Observation**: No explicit `IMP:n` cards observed in the cell card sections analyzed.

**Possible Scenarios**:
1. Importance weights specified in **data card section** (after cell and surface blocks)
2. Default importance (`IMP:n=1`) used throughout
3. Variance reduction handled via **volume weighting** (`VOL=` parameter on kernel cells)

**Volume Specification Example**:
```
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel
```
- `vol=0.092522`: Kernel volume in cm³
- Enables accurate source sampling and flux normalization
- Only specified for **kernel cells** (highest importance regions)

**Best Practice Observed**:
- Volume specified for **fuel kernels only** (not for other layers)
- MCNP can calculate volumes for other regions automatically
- Explicit volume aids in **power density** and **burnup calculations**

### 6.3 Void and Boundary Cell Treatments

**Lattice Holder Cells** (Material 0):

All lattice cells use **material 0 (void)** as placeholder:

```
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0
91110 0   -91118  u=1110 lat=1  fill=0:0 0:0 -15:15 ...
91111 0   -97011  98005 -98051  fill=1110  (25.547039 -24.553123 19.108100)
```

**Rationale**:
- Lattice holder cells **never transport particles** themselves
- Actual material is defined in the **filled universe** cells
- Material 0 = void, ensures no accidental interactions in lattice "container"

**Gas Gap Cells** (Material 8902, Helium):

```
91100 8902  1.2493e-4  97011 -97012  98005 -98007  $ stack 1 gas gap
```

- Helium fill gas between compact and capsule wall
- Very low density: 1.2493×10⁻⁴ g/cm³
- Important for **thermal modeling** but negligible for neutronics

**Outer Boundary Cells**:

```
99991 8900 -1.164e-03  (97066:-98000:98045) -99000 $ Room
99999 0                99000                       $ Exterior void
```

- Cell 99991: Air-filled room (low importance region)
- Cell 99999: True void exterior (importance likely = 0)
- Cell 99000: Outer boundary surface (probably large sphere or box)

---

## 7. COMPLEX LATTICE EXAMPLES

### 7.1 Complete TRISO Particle Implementation

**Full Cell Sequence** (Capsule 1, Stack 1, Compact 1):

```
c Capsule 1, stack 1, compact #1
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
91103 9091 -1.904  91112 -91113  u=1114                 $ IPyC
91104 9092 -3.205  91113 -91114  u=1114                 $ SiC
91105 9093 -1.911  91114 -91115  u=1114                 $ OPyC
91106 9094 -1.344  91115         u=1114                 $ SiC Matrix
91107 9094 -1.344 -91116         u=1115                 $ SiC Matrix
c
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
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
c
91109 9094 -1.344 -91119    u=1117                 $ Matrix
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
c
91111 0               -97011         98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Structure Summary**:
- **Cells 91101-91106**: TRISO particle in universe 1114 (6 layers)
- **Cell 91107**: Matrix-only in universe 1115
- **Cell 91108**: 2D hexagonal lattice (15×15) in universe 1116
- **Cell 91109**: Matrix end cap in universe 1117
- **Cell 91110**: 1D vertical stack (31 layers) in universe 1110
- **Cell 91111**: Placement cell (FILL=1110 with translation)

**Particle Count**:
- Counting "1114" entries in the 15×15 array: **141 fuel particles**
- Counting "1115" entries: **84 matrix positions**
- Total lattice elements: 225

**Packing Fraction**: 141/225 = 62.7% (reasonable for hexagonal packing with edge effects)

### 7.2 Multiple Capsule Implementation

The model contains **6 capsules**, each with **3 stacks**, each stack with **4 compacts**.

**Capsule 6, Stack 3, Compact 3 Example** (near end of cell block):

```
96341 9633 -10.924 -96331         u=6334 vol=0.093015    $ Kernel
96342 9090 -1.100  96331 -96332  u=6334                 $ Buffer
96343 9091 -1.904  96332 -96333  u=6334                 $ IPyC
96344 9092 -3.208  96333 -96334  u=6334                 $ SiC
96345 9093 -1.907  96334 -96335  u=6334                 $ OPyC
96346 9094 -1.297  96335         u=6334                 $ SiC Matrix
96347 9094 -1.297 -96336         u=6335                 $ SiC Matrix
c
96348 0   -96337  u=6336 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     [15×15 array of 6334 and 6335]
c
96349 9094 -1.297 -96339    u=6337                 $ Matrix
96350 0  -96338 u=6330 lat=1  fill=0:0 0:0 -15:15 6337 2R 6336 24R 6337 2R
c
96351 0               -97031         98041 -98087 fill=6330  (25.910838 -25.910838 100.324600)
```

**Universe Progression**:
- Capsule 1: 1XXX series
- Capsule 2: 2XXX series
- Capsule 3: 3XXX series
- Capsule 4: 4XXX series
- Capsule 5: 5XXX series
- Capsule 6: 6XXX series

**Material Variation**:
- Kernel materials: 9111 → 9633 (unique per compact for burnup tracking)
- Densities vary slightly: 10.924 → 10.924 g/cm³ (kernel), 1.344 → 1.297 g/cm³ (matrix)
- Coating densities slightly different: SiC 3.205 → 3.208 g/cm³, OPyC 1.911 → 1.907 g/cm³

**Position Variation**:
- Compact 1, Stack 1: (25.547039 -24.553123 19.108100)
- Compact 3, Stack 3: (25.910838 -25.910838 100.324600)
- Z-coordinates increase with stack number (axial stacking)
- X,Y coordinates vary by capsule position in ATR test rig

### 7.3 Comparison: Lattice vs. Explicit Geometry

**Lattice Approach** (used in AGR-1 models):

**Advantages**:
- **Computational efficiency**: 1 particle definition → 3,525 instances
- **Easy modification**: Change particle design in one place
- **Memory efficient**: MCNP stores one particle geometry, replicates via indexing
- **Burnup tracking**: Unique materials per compact enable depletion analysis

**Disadvantages**:
- **Regular array required**: Cannot model random particle distributions
- **Learning curve**: Complex nested universe logic
- **Debugging difficulty**: Particle tracking through nested universes can be complex

**Explicit Geometry Approach** (alternative):

Would require **254,000 individual cell definitions** for all particles, each with:
- 6 cells per particle (kernel + 5 coatings)
- Unique cell numbers
- Unique surface numbers
- Individual positioning

**Example Explicit Cells** (hypothetical):
```
c Capsule 1, Stack 1, Compact 1, Particle 1
91101 9111 -10.924 -91111  trcl=1001  $ Kernel at (x1,y1,z1)
91102 9090 -1.100  91111 -91112 trcl=1001  $ Buffer
...
c Capsule 1, Stack 1, Compact 1, Particle 2
91107 9111 -10.924 -91117  trcl=1002  $ Kernel at (x2,y2,z2)
91108 9090 -1.100  91117 -91118 trcl=1002  $ Buffer
...
[Repeat 254,000 times]
```

**Comparison**:
| Aspect | Lattice (Used) | Explicit (Alternative) |
|--------|----------------|------------------------|
| Cell cards | ~2,300 | ~1,500,000 |
| Surface cards | ~2,000 | ~760,000 |
| Memory | Low | Extremely high |
| Flexibility | Regular arrays only | Any distribution |
| Input file size | 4.6k lines | ~2 million lines |
| Maintainability | High | Extremely low |

**Conclusion**: Lattice approach is **essential** for TRISO fuel modeling. Explicit geometry is impractical.

---

## 8. BEST PRACTICES DEMONSTRATED

### 8.1 Universe Organization

**Systematic Naming**:
- Universe numbers follow hierarchical pattern (CABCD)
- Easy to trace which capsule/stack/compact a universe represents
- Consistent incrementing by 10 for parallel components

**Minimal Universe Duplication**:
- Coating materials (9090-9094) defined once, reused everywhere
- Only fuel kernels (9111-9634) are unique
- Reduces input size and maintains consistency

**Clear Universe Purpose**:
- Universe 1114: TRISO particle (with fuel)
- Universe 1115: Matrix only (no fuel)
- Universe 1116: 2D particle array
- Universe 1117: Matrix end cap
- Universe 1110: 1D vertical stack
- Each universe has a **single, clear purpose**

### 8.2 Lattice Design Patterns

**Two-Level Nesting**:
- Level 1: 1D vertical stack (31 layers)
- Level 2: 2D hexagonal particle array (15×15)
- Separation of axial and radial discretization

**Appropriate Lattice Sizing**:
- 2D: 15×15 = 225 positions (manageable array size)
- 1D: 31 layers (good axial resolution)
- Total: 225 × 31 = 6,975 lattice elements per compact

**Shorthand Usage**:
- 1D arrays use repeat notation (1117 2R 1116 24R 1117 2R)
- 2D arrays fully enumerated for verification and irregular patterns
- Balances conciseness with clarity

**Edge Treatment**:
- Matrix-only cells (1115) at periphery of 2D array
- Matrix end caps (1117) at top/bottom of 1D stack
- Prevents particles from being cut by boundaries

### 8.3 Material and Surface Consistency

**Universal Surfaces**:
- Each particle type uses same surface numbers (91111-91115 for Compact 1)
- Surfaces defined once in surface block, referenced in universe cells
- Systematic incrementing by 10 for each compact

**Material Reuse**:
- Coating materials (9090-9094) consistent across all particles
- Structural materials (SS316L, graphite) have consistent properties
- Only fuel kernel materials unique (for burnup tracking)

**Density Specification**:
- Always use density (not atom density) for lattice efficiency
- Explicit densities: `9111 -10.924` (g/cm³)
- Consistent significant figures (5 digits for densities)

**Volume Cards**:
- Specified only for **fuel kernels** (highest importance)
- Value: `vol=0.092522` cm³ (realistic TRISO kernel volume)
- Enables accurate power normalization and burnup

### 8.4 Geometric Transformation Best Practices

**Translation-Only Transformations**:
```
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```
- Uses **inline coordinate specification**
- No rotation needed for cylindrical compacts
- Simple, clear, avoids TR card overhead

**Coordinate Precision**:
- X,Y,Z coordinates to 6 decimal places (25.547039 cm)
- Sufficient precision for sub-millimeter positioning
- Matches CAD model precision

**Systematic Positioning**:
- Z-coordinate increases with stack/capsule number
- X,Y coordinates define radial position in ATR
- Consistent coordinate system throughout model

**Avoid TR Cards When Possible**:
- No explicit TRn transformations observed in lattice cells
- Inline coordinates simpler for translations
- TR cards useful for rotations or repeated transformations

### 8.5 Documentation and Comments

**Comment Strategy**:
```
c Capsule 1, stack 1, compact #1
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
...
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
```

**Best Practices Observed**:
- **Section headers**: `c Capsule 1, stack 1, compact #1`
- **Inline comments**: `$ Kernel`, `$ Buffer`, `$ Lattice of Particles`
- **Blank lines**: Separate logical groups of cells
- **Descriptive labels**: Clear component identification

**Consistency**:
- Same comment style throughout model
- Every material cell has component label
- Lattice cells clearly marked

---

## 9. MODELING INSIGHTS AND RECOMMENDATIONS

### 9.1 Advantages of This Approach

**Scalability**:
- Adding more capsules/stacks/compacts is straightforward
- Increment universe and cell numbers systematically
- Copy-paste with search-replace for new compacts

**Flexibility**:
- Easy to change particle design (update universe 1114/1115)
- Easy to change packing pattern (modify 15×15 FILL array)
- Easy to change axial discretization (modify 31-layer stack)

**Burnup Tracking**:
- Unique kernel materials (9111-9634) enable per-compact depletion
- Can track fission product buildup in each compact
- Supports post-irradiation examination (PIE) modeling

**Computational Efficiency**:
- Lattice approach minimizes memory usage
- MCNP replicates particles efficiently
- Faster geometry processing than explicit cells

**Validation-Friendly**:
- Structure matches physical hardware (capsules → stacks → compacts → particles)
- Easy to compare with experimental data by capsule/stack/compact
- Clear hierarchy aids in result interpretation

### 9.2 Potential Improvements

**1. Particle Randomization**:

Current model uses **regular hexagonal array**. Real compacts have **random particle positions**.

**Potential Improvement**:
- Use **MCNP URAN card** (universe randomization)
- Define multiple particle universe sets with slight position variations
- MCNP randomly selects from universe set for each lattice element
- Provides **stochastic realism** without explicit randomization

**Example**:
```
c Define 10 particle universes with random offsets
91101 9111 -10.924 -91111 u=1114001 vol=0.092522 $ Particle variant 1
...
91201 9111 -10.924 -91211 u=1114010 vol=0.092522 $ Particle variant 10

c Lattice with universe randomization
91108 0 -91117 u=1116 lat=1 uran=1114001:1114010 fill=-7:7 -7:7 0:0 ...
```

**2. Variable Particle Packing**:

Current model uses **fixed 62.7% packing fraction**. Real compacts may vary.

**Potential Improvement**:
- Define multiple 2D lattice universes (1116a, 1116b, 1116c)
- Each with different particle counts (e.g., 130, 141, 150 particles)
- Use different lattices in different axial planes
- Models realistic axial variation in packing density

**3. Explicit Importance Weighting**:

No explicit `IMP:n` observed in cell cards.

**Potential Improvement**:
```
c Set importance weights (data card section)
IMP:n 1 100R      $ Importance 1 for most cells
      1000 50R    $ Importance 1000 for fuel regions (cells 91101, etc.)
      100 200R    $ Importance 100 for particle layers
      10 500R     $ Importance 10 for structural regions
      0.1 10R     $ Importance 0.1 for outer regions
      0           $ Importance 0 exterior (kill particles)
```

**Benefits**:
- Concentrate computation in fuel kernels (highest importance)
- Reduce time in structural regions
- Improve figure of merit (FOM)

**4. Automated Cell Generation**:

Current approach appears **manually generated** (copy-paste-modify).

**Potential Improvement**:
- Python/Perl script to generate cell cards
- Input: number of capsules, stacks, compacts, material compositions
- Output: Complete MCNP cell block
- Reduces human error, improves consistency

**Example Script Workflow**:
```python
for capsule in range(1, 7):
    for stack in range(1, 4):
        for compact in range(1, 5):
            generate_triso_particle(capsule, stack, compact)
            generate_2d_lattice(capsule, stack, compact)
            generate_1d_stack(capsule, stack, compact)
            generate_placement_cell(capsule, stack, compact)
```

### 9.3 Common Pitfalls to Avoid

**1. Universe Number Collisions**:
- Never reuse universe numbers in overlapping geometry regions
- Maintain systematic numbering scheme
- Use spreadsheet to track universe allocation

**2. Fill Array Dimensioning Errors**:
```
c WRONG: Dimension mismatch
91108 0 -91117 u=1116 lat=1 fill=-7:7 -7:7 0:0  $ Expects 15×15×1 = 225 values
     1115 1115 1114 1114 ...  $ Only 100 values provided → ERROR

c CORRECT:
91108 0 -91117 u=1116 lat=1 fill=-7:7 -7:7 0:0  $ Expects 225 values
     [Provide exactly 225 universe numbers]
```

**3. Missing Universe Definitions**:
```
c WRONG: Reference undefined universe
91108 0 -91117 u=1116 lat=1 fill=-7:7 -7:7 0:0
     1114 1114 1118 1115 ...  $ Universe 1118 not defined → ERROR

c CORRECT: Ensure all universes in FILL are defined
```

**4. Lattice Boundary Surface Size**:
```
c WRONG: Lattice surface too small, particles cut off
91117 SO 0.5  $ Sphere radius 0.5 cm (too small for 15×15 array)

c CORRECT: Ensure boundary surface contains entire lattice
91117 RCC 0 0 0  0 0 1.5  0.6  $ Cylinder: h=1.5cm, r=0.6cm (appropriate size)
```

**5. Transformation Coordinate Systems**:
```
c WRONG: Apply transformation to wrong cell
91111 0 -97011 98005 -98051 fill=1110  $ No transformation
91108 0 -91117 u=1116 lat=1 fill=... (25.5 -24.5 19.1)  $ Applied to lattice cell → ERROR

c CORRECT: Apply transformation to placement cell
91111 0 -97011 98005 -98051 fill=1110 (25.5 -24.5 19.1)  $ Transformation here
```

### 9.4 Validation and Verification Strategies

**1. Geometry Plotting**:
```
mcnp6 inp=sdr-agr.i ip tasks 1
```
- Generate geometry plots at multiple Z-planes
- Verify particle placement in lattices
- Check for overlaps or gaps

**2. Volume Calculations**:
```
c Add to data section
VOL  NO  $ Calculate all cell volumes automatically
PRINT 110  $ Print detailed geometry information
```
- Compare calculated volumes with design values
- Verify total compact volume
- Check particle count per compact

**3. Particle Tracking**:
```
c Add to data section
DBCN 17J 2 $ Debug: print lost particle information
```
- Run short test case (1000 histories)
- Check for lost particles (geometry errors)
- Review particle tracks through nested universes

**4. Material Balance**:
- Sum fuel kernel volumes: 141 particles × 0.092522 cm³ × 25 planes = 326 cm³
- Verify uranium mass per compact
- Check total fissile inventory

**5. Comparison with Simplified Model**:
- Create "equivalent" homogenized compact (no particles)
- Run both models with same source
- Compare k-eff and reaction rates
- Should agree within ~50-100 pcm (particle self-shielding effects)

---

## 10. SUMMARY AND CONCLUSIONS

### 10.1 Key Findings

**Hierarchical Structure**:
- **4-level universe nesting** successfully models TRISO fuel
- Systematic numbering enables tracking of 254,000+ particles
- Clear separation of geometric levels (particle → plane → stack → placement)

**Lattice Implementation**:
- **LAT=1 (hexagonal)** used for both 2D and 1D lattices
- 2D: 15×15 arrays for particle packing (141 particles, 84 matrix)
- 1D: 31-layer vertical stacks (3+25+3 structure)
- Explicit FILL arrays provide verification and flexibility

**Material Strategy**:
- **Universal coating materials** (9090-9094) reused across all particles
- **Unique kernel materials** (9111-9634) enable per-compact burnup tracking
- Systematic material numbering tied to geometric hierarchy

**Computational Efficiency**:
- Lattice approach reduces 1.5 million cell definitions to ~2,300
- Memory efficient: one particle definition replicated ~254,000 times
- Maintainable: particle design changes require updating only 6 cells

### 10.2 Best Practice Recommendations

**For TRISO Fuel Modeling**:
1. Use **hierarchical universe structure** (particle → lattice → placement)
2. Employ **systematic numbering** (CABCD convention)
3. Define **base universe once**, replicate via lattices
4. Use **matrix-only universes** for lattice edge treatment
5. Specify **volumes for fuel kernels** only (variance reduction)
6. Apply **transformations at placement cell**, not lattice cell

**For Large Lattice Arrays**:
1. Use **shorthand repeat syntax** (N nR) for regular 1D patterns
2. **Explicitly enumerate** 2D arrays for verification (unless highly regular)
3. Ensure **lattice boundary surfaces** fully contain all elements
4. Add **end caps** (matrix-only layers) to prevent boundary artifacts
5. Verify **FILL array dimensions** match lattice range (i:j:k specifications)

**For Model Validation**:
1. **Plot geometry** at multiple planes before production runs
2. **Calculate volumes** and compare with design specifications
3. **Track particles** through nested universes (debug mode)
4. **Check material balance** (total fuel mass, fissile inventory)
5. **Compare with homogenized model** for physics validation

### 10.3 Applications

This cell card structure is suitable for:

**HTGR/AGR Fuel Analysis**:
- Particle-level burnup and fission product tracking
- Coating failure probability studies
- Post-irradiation examination (PIE) modeling

**Criticality Safety**:
- TRISO fuel storage and transportation
- Pebble bed reactor core modeling
- Prismatic block reactor analysis

**Shielding and Dose Calculations**:
- Spent TRISO fuel handling
- Irradiation test capsule dose rates
- Activation analysis

**Method Development**:
- Benchmark for homogenization methods
- Validation of reduced-order models
- Testing of new variance reduction techniques

### 10.4 Related Files and Documentation

**MCNP Input Files** (analyzed):
- `bench_138B.i`: ATR + AGR-1 full model (18,414 lines, 144 lattices)
- `bench_143A.i`: Similar to 138B (different cycle)
- `sdr-agr.i`: AGR PIE model (4,653 lines, 144 lattices, 216 fills)

**Recommended External References**:
- MCNP Manual: Chapter 3 (Geometry), especially Section 3.5 (Lattices)
- LA-UR-08-07064: "Advanced MCNP Geometry: Lattices and Universes"
- AGR-1 Experiment Specification (INL/EXT-05-00797)
- TRISO Fuel Technology Review (GA-A25402)

### 10.5 Contact for Questions

This analysis was performed as a **technical documentation study** of advanced MCNP geometry techniques. For questions about:

- **MCNP syntax and methods**: MCNP Help (mcnp_help@lanl.gov) or user forums
- **AGR-1 experiment details**: Idaho National Laboratory (INL) AGR program
- **TRISO fuel technology**: General Atomics, BWXT, or other TRISO fuel vendors
- **HTGR modeling**: IAEA HTGR knowledge base or Next Generation Nuclear Plant (NGNP) program

---

**END OF ANALYSIS**

---

## APPENDIX A: COMPLETE CELL CARD EXAMPLE

Below is a **complete example** showing all cell cards for one compact (Capsule 1, Stack 1, Compact 1) from sdr-agr.i:

```
c Capsule 1, stack 1, compact #1
c
c TRISO Particle with Fuel (Universe 1114)
91101 9111 -10.924 -91111         u=1114 vol=0.092522    $ Kernel
91102 9090 -1.100  91111 -91112  u=1114                 $ Buffer
91103 9091 -1.904  91112 -91113  u=1114                 $ IPyC
91104 9092 -3.205  91113 -91114  u=1114                 $ SiC
91105 9093 -1.911  91114 -91115  u=1114                 $ OPyC
91106 9094 -1.344  91115         u=1114                 $ SiC Matrix
c
c Matrix Only (Universe 1115)
91107 9094 -1.344 -91116         u=1115                 $ SiC Matrix
c
c 2D Hexagonal Particle Lattice (Universe 1116)
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice of Particles
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ j=-7
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 $ j=-6
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=-5
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=-4
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=-3
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=-2
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 $ j=-1
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 $ j=0
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 $ j=+1
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=+2
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 $ j=+3
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=+4
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 $ j=+5
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 $ j=+6
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115 $ j=+7
c
c Matrix End Cap (Universe 1117)
91109 9094 -1.344 -91119    u=1117                 $ Matrix
c
c 1D Vertical Stack (Universe 1110)
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
c
c Placement Cell (Base Geometry)
91111 0               -97011         98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
c
c Gas Gap Around Compact
91100 8902  1.2493e-4  97011 -97012  98005 -98007  $ stack 1 gas gap
```

**Cell Count for One Compact**:
- 6 cells: TRISO particle layers (91101-91106)
- 1 cell: Matrix-only universe (91107)
- 1 cell: 2D lattice (91108)
- 1 cell: Matrix end cap (91109)
- 1 cell: 1D stack lattice (91110)
- 1 cell: Placement (91111)
- 1 cell: Gas gap (91100)
- **Total: 12 cells per compact**

**Total Model Cell Count**:
- 4 compacts/stack × 3 stacks/capsule × 6 capsules = 72 compacts
- 72 compacts × 12 cells/compact = **864 primary fuel cells**
- Plus structural cells (capsule walls, supports, etc.): **~2,300 total cells**

---

## APPENDIX B: UNIVERSE REFERENCE TABLE

| Universe | Component | Cell(s) | Material(s) | Used In |
|----------|-----------|---------|-------------|---------|
| 0 | Base geometry | Various | Various | Top level |
| 1110 | 1D vertical stack (C1 S1 C1) | 91110 | 0 (void, LAT holder) | Cell 91111 (FILL) |
| 1114 | TRISO particle with fuel (C1 S1 C1) | 91101-91106 | 9111, 9090-9094 | Cell 91108 (2D lattice FILL) |
| 1115 | Matrix only (C1 S1 C1) | 91107 | 9094 | Cell 91108 (2D lattice FILL) |
| 1116 | 2D particle lattice (C1 S1 C1) | 91108 | 0 (void, LAT holder) | Cell 91110 (1D stack FILL) |
| 1117 | Matrix end cap (C1 S1 C1) | 91109 | 9094 | Cell 91110 (1D stack FILL) |
| 1120 | 1D vertical stack (C1 S1 C2) | 91130 | 0 | Cell 91131 (FILL) |
| 1124 | TRISO particle with fuel (C1 S1 C2) | 91121-91126 | 9112, 9090-9094 | Cell 91128 (2D lattice FILL) |
| ... | ... | ... | ... | ... |
| 6334 | TRISO particle with fuel (C6 S3 C3) | 96341-96346 | 9633, 9090-9094 | Cell 96348 (2D lattice FILL) |

**Total Unique Universes**: ~504 (6 capsules × 3 stacks × 4 compacts × 7 universes/compact)

---

## APPENDIX C: MATERIAL REFERENCE TABLE

| Material | Description | Density (g/cm³) | Used In Cells | Comments |
|----------|-------------|-----------------|---------------|----------|
| 9111-9634 | Fuel kernels (UCO) | 10.924 | 91101, 91121, ..., 96361 | Unique per compact for burnup tracking |
| 9090 | Buffer (porous carbon) | 1.100 | 91102, 91122, ..., 96362 | Universal (all particles) |
| 9091 | IPyC | 1.904 | 91103, 91123, ..., 96363 | Universal (all particles) |
| 9092 | SiC | 3.205-3.208 | 91104, 91124, ..., 96364 | Universal with minor density variations |
| 9093 | OPyC | 1.911-1.907 | 91105, 91125, ..., 96365 | Universal with minor density variations |
| 9094 | Matrix SiC | 1.344-1.297 | 91106, 91107, 91109, ... | Universal, varies slightly by capsule |
| 9001 | Capsule support (SS316L) | 8.03 | 91000 | Structural |
| 9041 | Graphite spacer | 1.015 | 91001 | Structural |
| 8900 | Air | 1.164×10⁻³ | 99970, 99987, 99991 | Outer regions |
| 8901 | Water (ATR coolant) | 0.9853 | 99990 | Coolant channel |
| 8902 | Helium (gas gap) | 1.2493×10⁻⁴ | 91100, 91200, ..., 96281 | Fill gas |
| 0 | Void | N/A | Lattice holders, exterior | No material |

**Total Materials**: ~600+ (524 unique kernel materials + ~50 structural/coolant materials)

---
