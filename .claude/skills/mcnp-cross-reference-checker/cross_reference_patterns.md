# Cross-Reference Patterns Reference
## Based on AGR-1 HTGR Model Analysis

This reference documents cross-referencing patterns observed in production MCNP models.

## Pattern 1: Simple Cell → Surface

**Example**:
```mcnp
100 1 -10.2  -100         u=100  $ Fuel pellet
101 2 -6.5   100 -101     u=100  $ Clad
```

**Cross-References**:
- Cell 100 uses surface 100 (negative sense)
- Cell 101 uses surfaces 100 (positive) and 101 (negative)
- Both surfaces must be defined

## Pattern 2: Complex Boolean Expressions

**Example**:
```mcnp
60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110
```

**Cross-References**:
- 7 surfaces referenced: 1111, 1118, 74, 29, 53, 100, 110
- All must be defined
- Boolean logic: +1111 AND -1118 AND +74 AND -29 AND +53 AND +100 AND -110

## Pattern 3: Surface Reuse

**Example**:
```mcnp
60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110  $ Zone 1
60107 2107 7.967400E-02  1111 -1118 74 -29 53 110 -120  $ Zone 2
60108 2108 7.965632E-02  1111 -1118 74 -29 53 120 -130  $ Zone 3
```

**Pattern**:
- Surfaces 1111, 1118, 74, 29, 53 shared by all 3 cells
- Only axial surfaces (100, 110, 120, 130) differ
- Surface 110 used by cells 60106 (upper bound) and 60107 (lower bound)

## Pattern 4: Concentric Shells (TRISO)

**Example**:
```mcnp
91101 9111 -10.924 -91111         u=1114  $ Kernel
91102 9090 -1.100  91111 -91112  u=1114  $ Buffer
91103 9091 -1.904  91112 -91113  u=1114  $ IPyC
91104 9092 -3.205  91113 -91114  u=1114  $ SiC
91105 9093 -1.911  91114 -91115  u=1114  $ OPyC
```

**Pattern**:
- Surfaces used in order: 91111 < 91112 < 91113 < 91114 < 91115
- Each surface used twice: as outer bound of inner cell, inner bound of outer cell
- Creates "onion" structure with no gaps

## Pattern 5: Universe Fill Hierarchy

**Example**:
```mcnp
c TRISO particle (u=1114)
91101 9111 -10.924 -91111  u=1114  $ Kernel
...

c Particle lattice (u=1116)
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0
     1115 1115 1115 ... 1114 1114 1114 ... 1115 1115 1115
     [225 elements total]

c Compact lattice (u=1110)
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

c Global placement
91111 0  -97011  98005 -98051 fill=1110  (25.547 -24.553 19.108)
```

**Cross-Reference Chain**:
```
Cell 91111 (base) → fill=1110 → Universe 1110 defined? ✓
Universe 1110 lattice → fill contains 1116, 1117 → Both defined? ✓
Universe 1116 lattice → fill contains 1114, 1115 → Both defined? ✓
Universes 1114, 1115, 1117 → Terminal (no further fills) ✓
```

**Validation**: All universes in chain must be declared before use

## Pattern 6: Systematic Numbering

**AGR-1 Encoding**:
```python
# Cell 91234 breakdown:
#   9     = AGR experiment
#   1     = Capsule 1
#   2     = Stack 2
#   3     = Compact 2 (encoded as 2×10)
#   4     = Sequence 4

# Surface 9123 breakdown:
#   91    = Capsule 1, Stack 2
#   2     = Compact 2
#   3     = Layer 3 (IPyC)

# Material 9123 breakdown:
#   91    = Capsule 1, Stack 2
#   23    = Compact 2, subpart 3

# Universe 1234 breakdown:
#   1     = Capsule 1
#   2     = Stack 2
#   3     = Compact 3
#   4     = Level 4 (TRISO particle)
```

**Benefit**: Zero conflicts across 1500+ entities

## Pattern 7: Void Cell Types

**Lattice Container**:
```mcnp
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0
      ^                  ^^^^^
      Void OK            Lattice
```

**Fill Target**:
```mcnp
91111 0  -97011  98005 -98051 fill=1110
      ^                        ^^^^^^^^^
      Void OK                  Fill
```

**True Void**:
```mcnp
99999 0  99000
      ^
      Void OK (terminates particles)
```

**Validation Rule**: Only non-void cells (M≠0) require material definition check

## Statistics from AGR-1 Analysis

**Model**: bench_138B.i (18,414 lines)

**Cross-Reference Statistics**:
- Total cells: 1,607
- Total surfaces: 725
- Total materials: 385
- Total universes: 288

**Surface Reuse**:
- Surface 100 (axial plane): Referenced by 52 cells
- Surface 110 (axial plane): Referenced by 48 cells
- Surface 1111 (TRISO sphere): Referenced by 6 cells

**Universe Hierarchy**:
- Maximum depth: 5 levels
- Terminal universes: 72 (TRISO particles)
- Lattice universes: 144 (particle arrays + compact stacks)
- Fill universes: 72 (compact placements)

**Numbering Ranges**:
- Cells: 60000-69999 (ATR), 90000-99999 (AGR)
- Surfaces: 1-999 (global), 9000-9999 (compact), 97000-98999 (capsule)
- Materials: 2000-2999 (ATR fuel), 9000-9999 (AGR materials)
- Universes: 100-999 (AGR structures)
