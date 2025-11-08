# MCNP Numbering Schemes Reference
## Professional Patterns from Production Reactor Models

**Purpose**: Comprehensive guide to systematic numbering schemes that prevent conflicts and enable maintainability in complex MCNP models.

---

## PHILOSOPHY

**Bad approach**: Sequential numbering
```mcnp
1, 2, 3, 4, 5...  $ Where is this? What is it?
```

**Professional approach**: Hierarchical encoding
```mcnp
11234  $ Instantly know: Component 1, Sub 1, Layer 2, Sequence 34
```

**Benefits**:
- Zero numbering conflicts
- Instant location identification
- Enables automated generation
- Simplifies debugging
- Scales to millions of cells

---

## SCHEME 1: HIERARCHICAL POSITION ENCODING

**Template: XYZSS**

```python
cell_id = X*10000 + Y*1000 + Z*100 + SS

# X = Major component (1-9)
# Y = Sub-component (0-9)
# Z = Layer/level (0-9)
# SS = Sequence within layer (00-99)
```

**Example: AGR-1 Capsule Model**

```mcnp
c Cell numbering: 9XYZW
c 9 = AGR experiment prefix
c X = Capsule (1-6)
c Y = Stack (1-3)
c Z = Compact (1-4)
c W = Sequence (0-9)

91101  $ 9=AGR, 1=Capsule1, 1=Stack1, 0=Compact1, 1=Cell1
91234  $ 9=AGR, 1=Capsule1, 2=Stack2, 3=Compact3, 4=Cell4
93417  $ 9=AGR, 3=Capsule3, 4=Stack4 (impossible, only 3 stacks)
```

**Application**:
- Capsules in vertical stack
- Fuel assemblies in core
- Control rod banks
- Layered shields

---

## SCHEME 2: FUNCTIONAL SUBSYSTEM RANGES

**Reserve 10,000-number blocks for major subsystems**

```mcnp
c SUBSYSTEM NUMBERING PLAN
c
c  10000-19999: Fuel assemblies
c  20000-29999: Control elements
c  30000-39999: Reflector components
c  40000-49999: Biological shield
c  50000-59999: Coolant regions
c  60000-69999: Structural components
c  70000-79999: Instrumentation
c  80000-89999: Experimental positions
c  90000-99999: Room/building
```

**Example: PWR Core**

```mcnp
c Fuel assembly A-14
11401 1 -10.2  -11401  imp:n=1  $ Fuel pin 01, Assembly A-14
11402 1 -10.2  -11402  imp:n=1  $ Fuel pin 02, Assembly A-14
...
11517 0       -11517  fill=115  $ Assembly A-14, lattice cell 17
c
c Control rod bank C
20101 4 -8.5   -20101  imp:n=1  $ Hafnium absorber, Rod C-01
20201 4 -8.5   -20201  imp:n=1  $ Hafnium absorber, Rod C-02
c
c Radial reflector
30001 5 -2.7   -30001  imp:n=1  $ Graphite reflector block 01
30002 5 -2.7   -30002  imp:n=1  $ Graphite reflector block 02
```

**Benefits**:
- No conflicts: fuel can't collide with control rods
- Instant identification: "23456 = control element"
- Easy expansion: room for 9999 components per subsystem

---

## SCHEME 3: UNIVERSE COMPONENT ENCODING

**Template: XYZW where W encodes component type**

```python
universe_id = position*10 + component_type

# Component type indicators (W):
# 0 = Lattice container
# 1 = Primary component (e.g., fuel)
# 2 = Secondary component (e.g., coolant)
# 3 = Structural element
# 4 = Special (e.g., particle, pellet)
# 5 = Matrix/filler
# 6 = Sub-lattice
# 7 = Alternative filler
# 8 = Void/gap
# 9 = Boundary/interface
```

**Example: TRISO Particle Compact**

```mcnp
c Position encoding: XYZ = Capsule + Stack + Compact
c Component type: W
c
c Capsule 1, Stack 1, Compact 1:
c   Base position = 111
c
1114  $ Position 111, Component type 4 = TRISO particle
1115  $ Position 111, Component type 5 = Matrix filler
1116  $ Position 111, Component type 6 = Particle lattice
1117  $ Position 111, Component type 7 = Matrix filler (alternative)
1110  $ Position 111, Component type 0 = Compact lattice container
c
c Capsule 2, Stack 3, Compact 4:
c   Base position = 234
c
2344  $ Position 234, Component type 4 = TRISO particle
2345  $ Position 234, Component type 5 = Matrix filler
2346  $ Position 234, Component type 6 = Particle lattice
2340  $ Position 234, Component type 0 = Compact lattice container
```

**Critical**: Universe numbers MUST be unique across entire model!

---

## SCHEME 4: CORRELATED ENTITY NUMBERING

**Use related numbers for cell, surface, material of same component**

**Pattern**:
```mcnp
c Base number: 11234
c Cell:     11234
c Surface:  11234 (or 1123X for multiple surfaces)
c Material: 1123 (or 112 for less precision)
```

**Example 1: One-to-one correlation**

```mcnp
c Fuel pin 15 in assembly A-12
c
c Cell
11215 1 -10.2  -11215  imp:n=1  $ Fuel pin 15
      ^          ^^^^^
      Material   Surface
c
c Surface
11215 cz  0.41  $ Fuel pin 15 outer radius
      ^^^^^
      Same number
c
c Material
m1  $ UO2 fuel (shared by all fuel pins)
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
```

**Example 2: Multiple surfaces per component**

```mcnp
c TRISO particle (5 layers = 5 surfaces)
c Base: 91101
c
c Cell
91101 9111 -10.924 -91101  u=1114  $ Kernel
91102 9090 -1.100   91101 -91102  u=1114  $ Buffer
91103 9091 -1.904   91102 -91103  u=1114  $ IPyC
91104 9092 -3.205   91103 -91104  u=1114  $ SiC
91105 9093 -1.911   91104 -91105  u=1114  $ OPyC
      ^^^^                  ^^^^^
      Material              Surface (incremented)
c
c Surfaces (sequential from base)
91101 so  0.017485  $ Kernel radius
91102 so  0.027905  $ Buffer radius
91103 so  0.031785  $ IPyC radius
91104 so  0.035375  $ SiC radius
91105 so  0.039305  $ OPyC radius
c
c Materials
m9111  $ Kernel (unique per compact)
m9090  $ Buffer (shared)
m9091  $ IPyC (shared)
m9092  $ SiC (shared)
m9093  $ OPyC (shared)
```

**Benefits**:
- Fast cross-referencing (cell 11234 → surface 11234)
- Debug errors faster (know which components connect)
- Automated generation simpler

---

## SCHEME 5: SURFACE NUMBERING BY GEOMETRY TYPE

**Group surfaces by type for clarity**

```mcnp
c SURFACE NUMBERING PLAN
c
c   1-999:      Fuel pin surfaces (cylinders, planes)
c   1000-1999:  Assembly surfaces (RPP, hexagonal prisms)
c   2000-2999:  Core boundary surfaces
c   3000-3999:  Reflector surfaces
c   10000+:     Correlated with cells (see Scheme 4)
c
c OR organize by surface type:
c   100-199:    Cylinders (CZ, C/Z)
c   200-299:    Planes (PX, PY, PZ, P)
c   300-399:    Spheres (SO, S)
c   400-499:    Special surfaces (RHP, RPP, etc.)
```

**Example**:

```mcnp
c Fuel pin cylinders
100 cz  0.41   $ Fuel radius
101 cz  0.48   $ Clad outer radius
c
c Assembly boundaries (RPP)
400 rpp -10.71 10.71 -10.71 10.71 -180 180  $ Assembly box
c
c Axial planes
200 pz   0.0    $ Bottom of active core
210 pz  15.24   $ Axial zone 1/2 boundary
220 pz  30.48   $ Axial zone 2/3 boundary
```

---

## SCHEME 6: MATERIAL NUMBERING

**Pattern 1: Sequential by category**

```mcnp
c MATERIAL NUMBERING PLAN
c
c  1-9:      Fuels (UO2, MOX, UCO)
c  10-19:    Moderators (graphite, water, heavy water)
c  20-29:    Coolants (water, helium, sodium)
c  30-39:    Structural (steel, zircaloy, aluminum)
c  40-49:    Absorbers (hafnium, boron, gadolinium)
c  50-59:    Reflectors (beryllium, graphite)
c  60-99:    Special materials
c  100+:     Depleted/burned materials (one per cell)
```

**Pattern 2: Correlated with geometry**

```mcnp
c Material numbers match geometry encoding
c
c Capsule 1, Stack 1, Compact 1 → m9111 (kernel)
c Capsule 2, Stack 3, Compact 4 → m9234 (kernel)
c
c Shared coating materials: m9090-m9094
```

---

## IMPLEMENTATION GUIDELINES

### Step 1: Document the Scheme

**At top of input file**:

```mcnp
c ========================================
c NUMBERING SCHEME DOCUMENTATION
c ========================================
c
c CELLS: XYZSS
c   X = Capsule/Assembly number (1-9)
c   Y = Stack/Position (0-9)
c   Z = Compact/Layer (0-9)
c   SS = Sequence (00-99)
c
c SURFACES: Correlated with cells + type grouping
c   Cell 11234 → Surface 11234 (or 1123X for multiple)
c
c MATERIALS: Category-based
c   1-9:    Fuel materials
c   10-19:  Moderators
c   20-29:  Coolants
c   90-99:  Special (unique compositions)
c
c UNIVERSES: XYZW
c   XYZ = Position encoding (same as cells)
c   W = Component type (0=container, 4=particle, etc.)
c
c RESERVED RANGES:
c   10000-19999: Reserved for future expansion
c   90000-99999: AGR experiment components
c
c ========================================
```

### Step 2: Create Lookup Tables

**Maintain external documentation**:

```
Cell Range    | Component Description        | Materials Used | Universes
-------------|------------------------------|----------------|------------
11000-11999  | Capsule 1, Stack 1, Compact 1| 9111, 9090-94  | 1114-1110
12000-12999  | Capsule 1, Stack 2, Compact 1| 9121, 9090-94  | 1214-1210
21000-21999  | Capsule 2, Stack 1, Compact 1| 9211, 9090-94  | 2114-2110
```

### Step 3: Enforce Consistency

**Automated checks**:

```python
# Check that cell/surface/material numbers follow scheme
def validate_numbering(cell_id):
    capsule = (cell_id // 1000) % 10
    stack   = (cell_id // 100) % 10
    compact = (cell_id // 10) % 10

    if capsule > 6:
        raise ValueError(f"Cell {cell_id}: Invalid capsule {capsule} (max 6)")
    if stack > 3:
        raise ValueError(f"Cell {cell_id}: Invalid stack {stack} (max 3)")
    if compact > 4:
        raise ValueError(f"Cell {cell_id}: Invalid compact {compact} (max 4)")
```

---

## REAL-WORLD EXAMPLE: AGR-1 MODEL

**Complete numbering system**:

```mcnp
c AGR-1 ADVANCED GAS REACTOR EXPERIMENT
c
c CELL NUMBERING: 9XYZW
c   9 = AGR experiment prefix
c   X = Capsule (1-6)
c   Y = Stack (1-3)
c   Z = Compact (1-4), encoded as Z*10
c   W = Sequence (0-9)
c
c Examples:
c   91101 = Capsule 1, Stack 1, Compact 1, Cell 01 (Kernel)
c   91102 = Capsule 1, Stack 1, Compact 1, Cell 02 (Buffer)
c   93347 = Capsule 3, Stack 3, Compact 4, Cell 07 (Matrix)
c
c SURFACE NUMBERING: 9XYZn
c   Correlated with cells
c   91111 = TRISO particle surface set for C1S1C1
c
c MATERIAL NUMBERING: 9XYZ (kernels) or 909X (shared coatings)
c   9111 = Kernel material for Capsule 1, Stack 1, Compact 1
c   9090 = Buffer (shared across all compacts)
c   9091 = IPyC (shared)
c   9092 = SiC (shared)
c   9093 = OPyC (shared)
c   9094 = Matrix (shared)
c
c UNIVERSE NUMBERING: XYZW
c   XYZ = Position (Capsule + Stack + Compact)
c   W = Component type:
c     0 = Compact lattice container
c     4 = TRISO particle
c     5 = Matrix filler cell
c     6 = Particle lattice
c     7 = Matrix filler universe
c
c Examples:
c   1114 = Capsule 1, Stack 1, Compact 1, TRISO particle
c   1116 = Capsule 1, Stack 1, Compact 1, Particle lattice (15×15)
c   1110 = Capsule 1, Stack 1, Compact 1, Compact lattice (1×1×31)
c
c RESULT: 1,607 cells, ZERO numbering conflicts!
```

**Application**: This scheme enabled:
- 6 capsules × 3 stacks × 4 compacts × ~10 cells = ~720 cells
- Plus lattice definitions, capsule hardware
- Total: 1,607 cells with instant traceability

---

## VALIDATION CHECKLIST

Before finalizing numbering scheme:

- [ ] Scheme documented at top of input file
- [ ] Number ranges reserved for each subsystem
- [ ] Hierarchical encoding consistent throughout
- [ ] No numbering conflicts (automated check)
- [ ] Universe numbers unique across entire model
- [ ] Correlated entities use related numbers
- [ ] Scheme allows for future expansion
- [ ] External lookup table created (optional but recommended)

---

## COMMON MISTAKES

### Mistake 1: Random Sequential Numbering

**DON'T**:
```mcnp
1, 2, 3, 17, 42, 101, 137...  $ No pattern, can't tell what these are
```

**DO**:
```mcnp
11101, 11102, 11103...  $ Clear: Component 1, Sub 1, Layer 1, sequences 1-3
```

### Mistake 2: Numbering Conflicts

**DON'T**:
```mcnp
c Cell for fuel pin
100 1 -10.2  -100  imp:n=1
c
c Cell for control rod (CONFLICT!)
100 2 -8.0   -100  imp:n=1  $ Same cell number! ERROR
```

**DO**:
```mcnp
c Fuel pins: 10000-19999
11001 1 -10.2  -11001  imp:n=1  $ Fuel pin 1
c
c Control rods: 20000-29999
20001 2 -8.0   -20001  imp:n=1  $ Control rod 1
```

### Mistake 3: Expanding Beyond Reserved Range

**DON'T**:
```mcnp
c Reserved 100-199 for fuel pins
100, 101, ..., 199  $ Full!
200  $ Oops, this was reserved for control rods!
```

**DO**:
```mcnp
c Reserve larger ranges
c Fuel pins: 10000-19999 (room for 10,000 pins)
c Control rods: 20000-29999
```

### Mistake 4: Inconsistent Correlation

**DON'T**:
```mcnp
c Cell 11234 uses surface 5678 and material 92
c No relationship! Hard to debug
```

**DO**:
```mcnp
c Cell 11234 uses surface 11234 and material 1123
c Clear correlation!
```

---

## SUMMARY

**Professional numbering schemes**:
1. ✅ Encode hierarchy in numbers (XYZSS)
2. ✅ Reserve ranges for subsystems (10000 blocks)
3. ✅ Use correlated numbering (cells ↔ surfaces ↔ materials)
4. ✅ Document the scheme (top of file + external tables)
5. ✅ Validate automatically (check conflicts, ranges)
6. ✅ Allow room for expansion (don't use full range)

**Result**: Maintainable, debuggable, scalable reactor models with ZERO numbering conflicts.

---

**END OF REFERENCE FILE**
