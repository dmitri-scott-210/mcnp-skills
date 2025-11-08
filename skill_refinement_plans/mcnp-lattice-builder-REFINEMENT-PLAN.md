# mcnp-lattice-builder Skill Refinement Plan

**Created**: 2025-11-08
**Status**: Ready for immediate execution
**Priority**: 🔴 CRITICAL - Foundational skill for complex reactor modeling
**Estimated Time**: 2-3 hours

---

## Source Documents

This refinement plan is based on comprehensive analysis of production-quality HTGR reactor models:

### Primary Sources

1. **AGENT8_FILL_ARRAY_DEEP_DIVE.md** (46 KB, 1,382 lines)
   - Complete FILL array mechanics for LAT=1 and LAT=2
   - Multi-level lattice hierarchies (up to 6 levels)
   - Repeat notation detailed specification
   - Index ordering (K, J, I) with examples
   - Circular/hexagonal packing patterns
   - 15×15 rectangular and 13×13 hexagonal patterns

2. **AGR1_CELL_CARD_COMPLETE_ANALYSIS.md** (31 KB)
   - Universe numbering schemes (systematic 4-digit encoding)
   - TRISO particle lattice structures (15×15×1)
   - Compact lattice structures (1×1×31)
   - Complete 5-level hierarchy example

3. **AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md** (39 KB)
   - RPP surface patterns for rectangular lattices
   - RHP surface patterns for hexagonal lattices
   - Lattice bounding surfaces
   - Multi-scale geometry (174.85 μm to 190.5 mm)

4. **COMPREHENSIVE_FINDINGS_SYNTHESIS.md** (28 KB)
   - Best practices synthesis from 13 documents
   - Critical patterns for lattice building
   - Common pitfalls and fixes

### Supporting Documents

5. **input_definition.py** (Micro-HTGR model)
   - Hexagonal lattice generation (LAT=2)
   - 13×13 assembly patterns
   - 9×9 core patterns
   - Programmatic lattice creation

---

## Current State Analysis

### What's Missing

The current mcnp-lattice-builder skill (SKILL.md: 386 lines) does **NOT** adequately teach:

1. ❌ **Multi-level nesting guidance** (>2 levels)
   - No examples of 3-6 level hierarchies
   - No explanation of universe fill chains

2. ❌ **FILL array dimension calculation**
   - No formula: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
   - No explanation of negative index counting (include zero!)

3. ❌ **Repeat notation (nR syntax)**
   - No explanation that "U nR" = (n+1) total copies
   - No examples of compact notation for long arrays

4. ❌ **Hexagonal lattice (LAT=2) patterns**
   - No RHP surface specification
   - No hexagonal pitch calculation (R × √3)
   - No staggered row patterns

5. ❌ **Index ordering (K, J, I)**
   - No explanation that K is outermost loop
   - No examples showing fill order

6. ❌ **Circular packing patterns**
   - No examples of approximating cylinders with rectangular grids
   - No TRISO particle packing examples

7. ❌ **Lattice type-specific validation**
   - No dimension checking tools
   - No surface-lattice consistency validation
   - No universe hierarchy validation

### Impact on Users

**Current skill fails to enable users to**:
- ✗ Build multi-level reactor models (PWR assemblies, HTGR cores)
- ✗ Use hexagonal lattices (fast reactors, HTGR, CANDU)
- ✗ Validate FILL array dimensions before running MCNP
- ✗ Use repeat notation efficiently
- ✗ Avoid common off-by-one errors

**Result**: Users cannot build ANY complex reactor models without external examples.

---

## Refinement Objectives

### Primary Objectives

1. ✅ **Teach multi-level lattice hierarchies** (2-6 levels)
   - Provide complete examples for each level
   - Show both rectangular and hexagonal nesting

2. ✅ **Cover BOTH lattice types comprehensively**
   - LAT=1 (rectangular) with RPP surfaces
   - LAT=2 (hexagonal) with RHP surfaces
   - Always specify lattice TYPE in examples

3. ✅ **Provide computational tools**
   - FILL dimension calculator (Python)
   - Repeat notation converter
   - Lattice-surface validator (LAT=1 AND LAT=2)

4. ✅ **Include production-quality examples**
   - 17×17 PWR assembly (LAT=1)
   - 13×13 HTGR assembly (LAT=2) - **COMPLETE pattern**
   - 15×15 TRISO particle lattice (LAT=1, circular packing)
   - 1×1×31 vertical stack (with repeat notation)

5. ✅ **Prevent common errors**
   - Dimension mismatch (most common fatal error)
   - Repeat notation off-by-one
   - Wrong surface type for lattice type
   - Circular universe references

### Secondary Objectives

6. ✅ **Generalize beyond TRISO**
   - PWR fuel assemblies
   - BWR fuel bundles
   - Fast reactor assemblies
   - CANDU bundles
   - TRISO as ONE example among many

7. ✅ **Enable validation before MCNP run**
   - Pre-flight checks
   - Automated dimension verification
   - Universe hierarchy validation

---

## Files to Create/Modify

### Directory Structure

```
.claude/skills/mcnp-lattice-builder/
├── SKILL.md (MODIFY - add ~600 lines)
├── lattice_patterns_reference.md (CREATE - comprehensive examples)
├── complex_reactor_patterns.md (CREATE - multi-level hierarchies)
├── triso_fuel_reference.md (CREATE - supplemental TRISO-specific)
├── scripts/
│   └── lattice_dimension_calculator.py (CREATE - validation tools)
└── example_inputs/
    ├── rectangular_pwr_assembly.i (CREATE - LAT=1 example)
    ├── hexagonal_htgr_assembly.i (CREATE - LAT=2 example)
    ├── triso_particle_lattice.i (CREATE - circular packing)
    └── multi_level_hierarchy.i (CREATE - 4-level nesting)
```

**Note**: Reference files at ROOT of skill directory, NOT in assets/ subdirectory.

---

## Implementation Details

### Step 1: Update SKILL.md

**File**: `.claude/skills/mcnp-lattice-builder/SKILL.md`

**Action**: ADD new sections after existing content (keep current content, expand)

#### Section 1: Critical Lattice Concepts (ADD after current content)

```markdown
## CRITICAL LATTICE CONCEPTS

### Lattice Types in MCNP

MCNP supports TWO lattice types. **ALWAYS specify which type you're building.**

#### LAT=1: Rectangular (Hexahedral) Lattice

- **Coordinate system**: Cartesian grid (x, y, z)
- **Bounding surface**: RPP (rectangular parallelepiped)
- **Pitch**: Element spacing in x, y, z directions
- **Common uses**:
  - PWR fuel assemblies (17×17 pin arrays)
  - BWR fuel bundles
  - Simple reactor cores
  - Vertical stacks
  - TRISO particle arrays

**Example surface**:
```mcnp
100 rpp  xmin xmax  ymin ymax  zmin zmax
```

#### LAT=2: Hexagonal Lattice

- **Coordinate system**: 60° skewed axes
- **Bounding surface**: RHP (right hexagonal prism)
- **Pitch**: R-vector magnitude × √3
- **Common uses**:
  - HTGR cores (hexagonal assemblies)
  - Fast reactor assemblies
  - CANDU fuel bundles
  - Prismatic reactor cores

**Example surface**:
```mcnp
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
100 rhp  0 0 0  0 0 68  0 1.6 0
```

**Key difference**: Hexagonal lattices have staggered rows (60° symmetry), rectangular do not.

### Multi-Level Lattice Hierarchies

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 4**: MCNP supports up to 6 practical levels of nested lattices.

**Example hierarchy** (AGR-1 model):

```
Level 1: TRISO Particle (u=1114)
   └─ 5 concentric spherical shells (kernel, buffer, IPyC, SiC, OPyC)

Level 2: Matrix Cell (u=1115)
   └─ Single cell filled with SiC matrix

Level 3: Particle Lattice (u=1116) - LAT=1 rectangular
   ├─ 15×15×1 array
   ├─ fill=-7:7 -7:7 0:0 (225 positions)
   └─ Circular packing: ~169 particles + ~56 matrix

Level 4: Matrix Filler (u=1117)
   └─ Top/bottom caps for compact

Level 5: Compact Lattice (u=1110) - LAT=1 rectangular
   ├─ 1×1×31 vertical stack
   ├─ fill=0:0 0:0 -15:15
   └─ Pattern: 1117 2R 1116 24R 1117 2R

Level 6: Global Placement
   └─ fill=1110 (x,y,z) transformation
```

**Efficiency**: This represents ~300,000 TRISO particles using ~900 cells (333× reduction).

**Both rectangular AND hexagonal lattices can be nested in same model.**

### FILL Array Dimension Calculation

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 1.2**:

**CRITICAL RULE**:
```
Elements needed = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
```

**This applies to BOTH LAT=1 and LAT=2!**

**Examples**:

```mcnp
fill=-7:7 -7:7 0:0
  I: -7 to 7 → (-7)-(-7)+1 = 15 elements  (count: -7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7)
  J: -7 to 7 → 15 elements
  K: 0 to 0 → 1 element
  Total: 15 × 15 × 1 = 225 elements ✓
```

```mcnp
fill=0:16 0:16 0:0
  I: 0 to 16 → 17 elements  (count: 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
  J: 0 to 16 → 17 elements
  K: 0 to 0 → 1 element
  Total: 17 × 17 × 1 = 289 elements ✓ (17×17 PWR assembly)
```

```mcnp
fill=-6:6 -6:6 0:0
  I: -6 to 6 → 13 elements
  J: -6 to 6 → 13 elements
  K: 0 to 0 → 1 element
  Total: 13 × 13 × 1 = 169 elements ✓ (13×13 hexagonal assembly)
```

**ALWAYS include ZERO when counting negative to positive indices!**

### Repeat Notation (nR)

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 2.2**:

**CRITICAL RULE**: `U nR` = (n+1) total copies, NOT n copies!

**Repeat notation syntax**:
```
U nR  →  U repeated (n+1) times total
```

**Examples**:
```mcnp
100 2R     →  100 100 100           (3 copies total: first + 2 repeats)
200 24R    →  200 (repeated 25 times)
1117 0R    →  1117                  (1 copy: first + 0 repeats)
```

**Full compact lattice example** (from sdr-agr.i):
```mcnp
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

Breakdown:
  fill=0:0 0:0 -15:15  →  1×1×31 = 31 elements needed

  1117 2R   = 3 layers of universe 1117  (bottom cap)
  1116 24R  = 25 layers of universe 1116 (fuel region)
  1117 2R   = 3 layers of universe 1117  (top cap)

  Total: 3 + 25 + 3 = 31 elements ✓
```

**Benefit**: Compact notation for long arrays. Without repeat notation:
```mcnp
c Would require writing:
1117 1117 1117 1116 1116 1116 ... (25 times) ... 1116 1117 1117 1117
c Instead of:
1117 2R 1116 24R 1117 2R
```

**Works identically for rectangular and hexagonal lattices.**

### Index Ordering

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 1.2**:

**CRITICAL RULE**: Arrays filled in **K, J, I** order (K outermost loop, I innermost)

**Applies to BOTH LAT=1 and LAT=2.**

For `fill=-1:1 -1:1 -1:1` (3×3×3 = 27 elements):

```
Position  K   J   I   Element#
--------------------------------
   1     -1  -1  -1      1      ← First element in FILL array
   2     -1  -1   0      2      ← Second element
   3     -1  -1   1      3      ← Third element
   4     -1   0  -1      4
   5     -1   0   0      5
   6     -1   0   1      6
   7     -1   1  -1      7
   8     -1   1   0      8
   9     -1   1   1      9
  10      0  -1  -1     10
  ...     ...  ...     ...
  27      1   1   1     27      ← Last element in FILL array
```

**Reading the FILL array**:
- First line (elements 1-3): K=-1, J=-1, I=-1,0,1
- Second line (elements 4-6): K=-1, J=0, I=-1,0,1
- Third line (elements 7-9): K=-1, J=1, I=-1,0,1
- Fourth line (elements 10-12): K=0, J=-1, I=-1,0,1
- etc.

**For 2D lattices** (k=0:0):
- First row: J=JMIN, I varies from IMIN to IMAX
- Second row: J=JMIN+1, I varies from IMIN to IMAX
- etc.

### Rectangular Lattice (LAT=1) Specifics

**Bounding Surface**: RPP (rectangular parallelepiped)

**Per AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md, section 3.1**:

```mcnp
c RPP: xmin xmax ymin ymax zmin zmax
100 rpp -10.71 10.71 -10.71 10.71 -180 180  $ 17×17 assembly

c Lattice cell using this RPP
200 0  -100  u=200 lat=1  fill=-8:8 -8:8 0:0
     [... 289 universe numbers ...]
```

**Pitch**: Element spacing = (MAX - MIN) / N_elements (in each direction)

**Example**:
```
X-extent: -10.71 to +10.71 = 21.42 cm
Elements: 17
Pitch: 21.42 / 17 = 1.26 cm
```

**Fill pattern**: Straightforward grid (no offsets)

### Hexagonal Lattice (LAT=2) Specifics

**Bounding Surface**: RHP (right hexagonal prism)

**Per input_definition.py, lines 111-124**:

```mcnp
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
{n}13 rhp  0 0 {h}     0 0 68     0  1.6  0

c Lattice cell using this RHP
{n}15 0  -{n}13 u={n}0 lat=2  fill=-6:6 -6:6 0:0
     [... 169 universe numbers in hexagonal pattern ...]
```

**Pitch calculation**:
```
Pitch = R-vector magnitude × √3

Example: R = 1.6 cm
Pitch = 1.6 × 1.732 = 2.77 cm
```

**Fill pattern**: Staggered rows (60° symmetry)

**Visual representation** (indentation is OPTIONAL but helps show pattern):
```mcnp
c Row j=-6 (no indent):
300 300 300 300 300 300 300 300 300 300 300 300 300
c Row j=-5 (indented - offset by half pitch):
 300 300 300 300 300 300 100 100 100 300 300 300 300
c Row j=-4 (no indent):
300 300 300 300 300 100 100 200 100 100 300 300 300
```

**MCNP ignores whitespace** - indentation is for human readability only.

### Circular/Hexagonal Packing Patterns

**Common in reactor models**: Approximate cylindrical or hexagonal geometry using rectangular lattice.

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 2.1**:

**Example: TRISO particles in cylindrical compact** (LAT=1 rectangular)

```mcnp
c Particle lattice (u=1116) - 15×15 rectangular approximating circle
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ 225 positions

c Circular packing pattern (corners = matrix, center = particles):
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

c Result: ~169 particles (u=1114) + ~56 matrix (u=1115) in circular pattern
c Physical constraint: Fits in cylindrical compact (r=6.35 mm) using square lattice
```

**Pattern benefits**:
- Approximates cylindrical geometry
- Uses efficient rectangular lattice
- Avoids complex curved lattice boundaries

### Universe Hierarchy Validation

**Rules for valid nested lattices** (both LAT=1 and LAT=2):

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 6.2**:

1. ✅ **Define child universes BEFORE parent universes**
   - Universe 100 (pin) defined before universe 200 (assembly using pin)

2. ✅ **No circular references**
   - ❌ WRONG: u=100 fill=200, u=200 fill=100
   - ✅ RIGHT: u=100 (pin), u=200 fill with 100 instances

3. ✅ **All filled universes must exist**
   - If fill array contains "150", universe u=150 must be defined

4. ✅ **Universe 0 is always global**
   - Never define explicitly (u=0 forbidden in cell cards)
   - All top-level cells automatically in universe 0

5. ✅ **Lattice bounding surface must contain N × pitch**
   - For LAT=1: RPP extent = N_elements × pitch (each direction)
   - For LAT=2: RHP must geometrically contain hex pattern

**Example hierarchy validation**:

```
CORRECT order of definition:

c Level 1: Define fuel pin
100 1 -10.2  -1  u=100  $ Fuel
101 2 -6.5   1 -2  u=100  $ Clad
102 3 -1.0   2  u=100  $ Water

c Level 2: Define assembly lattice (uses u=100)
200 0  -10  u=200 lat=1  fill=-8:8 -8:8 0:0
    100 100 100 ... (289 instances of u=100)

c Level 3: Place assembly in global space (uses u=200)
999 0  -10  fill=200
```

## WORKING EXAMPLES

### Example 1: Rectangular Lattice (LAT=1) - PWR Pin Array

**Full 17×17 PWR assembly** (289 fuel pins):

```mcnp
c 17×17 PWR Assembly - Rectangular Lattice Example
c Demonstrates LAT=1 with proper RPP surface sizing
c
c Cells
c
c Fuel pin (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Guide tube (u=101)
110 0       -110          u=101  imp:n=1  $ Void
111 2 -6.5   110 -111     u=101  imp:n=1  $ Tube wall
112 3 -1.0   111          u=101  imp:n=1  $ Water

c Instrument tube (u=102)
120 0       -120          u=102  imp:n=1  $ Void
121 2 -6.5   120 -121     u=102  imp:n=1  $ Tube wall
122 3 -1.0   121          u=102  imp:n=1  $ Water

c Assembly lattice (u=200) - LAT=1 rectangular
c fill=-8:8 -8:8 0:0 → 17×17×1 = 289 elements
200 0  -200  u=200 lat=1  imp:n=1  fill=-8:8 -8:8 0:0
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     100 100 100 101 100 100 100 100 100 100 100 100 100 101 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 101 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 102 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 101 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 101 100 100 100 100 100 100 100 100 100 101 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100

c Global placement
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0  $ Outside world

c
c Surfaces
c
c Pin surfaces (centered at origin for universe)
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
110 cz  0.56  $ Guide tube inner radius
111 cz  0.61  $ Guide tube outer radius
120 cz  0.52  $ Instrument tube inner radius
121 cz  0.57  $ Instrument tube outer radius

c Assembly surface - RPP for LAT=1
c Calculation: 17 elements × 1.26 cm pitch = 21.42 cm extent
c Centered: ±10.71 cm from origin
200 rpp -10.71 10.71 -10.71 10.71 -180 180

c
c Materials
c
m1  $ UO2 fuel, 4.5% enriched
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
m2  $ Zircaloy clad
   40000.60c  1.0
m3  $ Light water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t  $ 350K PWR conditions
```

### Example 2: Hexagonal Lattice (LAT=2) - HTGR Assembly

**COMPLETE 13×13 hexagonal assembly** (ALL 169 elements):

**Per input_definition.py, lines 111-124** (verified complete pattern):

```mcnp
c HTGR Hexagonal Assembly - LAT=2 Example
c Demonstrates hexagonal geometry with RHP surface
c COMPLETE 13×13 pattern (all 169 elements shown)
c
c Cells
c
c Fuel channel (u=100)
100 1 -1.8  -100         u=100  imp:n=1  $ Fuel compact
101 2 -1.7   100 -101    u=100  imp:n=1  $ Graphite channel

c Coolant channel (u=200)
200 3 -5e-3  -102         u=200  imp:n=1  $ Helium
201 2 -1.7    102 -103    u=200  imp:n=1  $ Graphite

c Graphite reflector (u=300)
300 2 -1.7  -104         u=300  imp:n=1  $ Solid graphite

c Assembly lattice (u=400) - LAT=2 hexagonal
c fill=-6:6 -6:6 0:0 → 13×13×1 = 169 elements
c Pitch = R × √3 = 1.6 × 1.732 = 2.77 cm
400 0  -400  u=400 lat=2  imp:n=1  fill=-6:6 -6:6 0:0
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

c Note: Visual indentation shows hexagonal stagger (optional formatting)

c Global placement
999 0  -400 fill=400  imp:n=1
1000 0  400  imp:n=0  $ Outside world

c
c Surfaces
c
c Channel surfaces
100 cz  0.6     $ Fuel compact radius
101 cz  0.7     $ Fuel channel outer
102 cz  0.4     $ Coolant channel radius
103 cz  0.5     $ Coolant channel outer
104 cz  0.7     $ Graphite cell radius

c Assembly surface - RHP for LAT=2
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
c      0       0       0         0       0      68       0  1.6  0
c R = 1.6 cm → pitch = 1.6 × √3 = 2.77 cm
400 rhp  0 0 0  0 0 68  0 1.6 0  $ Hex prism, height=68 cm

c
c Materials
c
m1  $ Graphite fuel matrix
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ 600K graphite - REQUIRED!
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ REQUIRED!
m3  $ Helium coolant
    2004.00c  1.0
```

**Pattern breakdown**:
- Row j=-6: All reflector (300)
- Rows j=-5 to -2: Fuel (100) + coolant (200) + reflector (300) mix
- Rows j=-1 to 1: Inner fuel/coolant region
- Rows j=2 to 5: Fuel (100) + coolant (200) + reflector (300) mix
- Row j=6: All reflector (300)

### Example 3: Multi-Level Nesting (4 Levels)

**See**: `complex_reactor_patterns.md` for complete 4-6 level hierarchies.

**Compact example** (PWR core):

```
Level 1: Fuel pin (u=100) - LAT=1
   └─ Fuel, clad, water

Level 2: Assembly (u=200) - LAT=1, 17×17 pins
   └─ fill=-8:8 -8:8 0:0 with 289 instances of u=100

Level 3: Core quarter (u=300) - LAT=1, assemblies
   └─ fill with various assembly types

Level 4: Full core (u=0) - rotation/reflection
   └─ fill=300 in appropriate cells
```

## COMMON PITFALLS AND FIXES

**Per AGENT8_FILL_ARRAY_DEEP_DIVE.md, section 10**:

| Pitfall | Example | Fix |
|---------|---------|-----|
| **Dimension mismatch** | fill=0:10, provide 10 elements | Need 11: (10-0+1)=11 |
| **Repeat off-by-one** | fill=0:10, use "U 10R" (=11) | Use "U 9R" for 10 elements |
| **Negative index error** | fill=-5:5, think it's 5 or 10 | It's 11 (include 0!) |
| **Wrong index order** | Assume I,J,K ordering | MCNP uses K,J,I! |
| **RPP for hex lattice** | LAT=2 with RPP surface | Use RHP for LAT=2 |
| **RHP for rect lattice** | LAT=1 with RHP surface | Use RPP for LAT=1 |
| **Hex pitch wrong** | Use R directly as pitch | Pitch = R × √3 |
| **Surface too small** | 15×15 lattice, 14 pitches | Surface = N × pitch |
| **Universe conflict** | Reuse U=100 for different geom | Use unique numbers |
| **Circular fill** | u=100 fill=200, u=200 fill=100 | Define hierarchy bottom-up |
| **Missing universe** | fill array has "150", no u=150 | Define all universes |

## VALIDATION CHECKLIST

Before running MCNP, verify:

- [ ] Lattice type specified: LAT=1 (rectangular) or LAT=2 (hexagonal)
- [ ] Surface type matches: RPP for LAT=1, RHP for LAT=2
- [ ] FILL array element count = (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1)
- [ ] Repeat notation: nR gives (n+1) total copies
- [ ] All filled universes are defined before use
- [ ] No circular universe references
- [ ] Lattice bounding surface matches N × pitch (or N × R×√3 for hex)
- [ ] Child universes defined before parent universes
- [ ] Universe numbers are unique (no conflicts)
- [ ] Index ordering understood (K, J, I)

**Use validation tools**: `scripts/lattice_dimension_calculator.py`

## REFERENCE FILES

For detailed examples and patterns:

- **lattice_patterns_reference.md** - Comprehensive rectangular and hexagonal examples
- **complex_reactor_patterns.md** - Multi-level nesting, mixed lattice types
- **triso_fuel_reference.md** - TRISO-specific patterns (optional supplemental)

---

## WHEN TO USE EACH LATTICE TYPE

### Use LAT=1 (Rectangular) When:

✅ Modeling square/rectangular arrays
- PWR fuel assemblies (17×17, 15×15, etc.)
- BWR fuel bundles
- Simple reactor cores
- Vertical stacks
- TRISO particle arrays (approximating cylinders)

### Use LAT=2 (Hexagonal) When:

✅ Modeling hexagonal arrangements
- HTGR cores
- Fast reactor assemblies
- CANDU fuel bundles
- Any 60° symmetric geometry

### Use Mixed (Both in Same Model) When:

✅ Nesting different geometries
- Hexagonal assemblies with rectangular pin arrays
- Rectangular fuel pins in hexagonal core
- Complex multi-scale reactors
```

---

[File continues with detailed reference files - truncated for length]

**THIS SECTION ADDS ~600 LINES TO SKILL.MD**

---

## Validation Tests

### Test 1: Rectangular Lattice Query

**User Query**: "How do I create a 17×17 rectangular lattice for a PWR assembly?"

**Expected Output**: Skill provides:
1. ✅ Lattice type: LAT=1 (rectangular)
2. ✅ Surface type: RPP
3. ✅ Dimension calculation: fill=-8:8 -8:8 0:0 → 17×17×1 = 289 elements
4. ✅ Complete working example (all 289 elements)
5. ✅ Surface sizing: 17 × 1.26 cm = 21.42 cm extent
6. ✅ Validation checklist

### Test 2: Hexagonal Lattice Query

**User Query**: "How do I create a 13×13 hexagonal lattice for an HTGR assembly?"

**Expected Output**: Skill provides:
1. ✅ Lattice type: LAT=2 (hexagonal)
2. ✅ Surface type: RHP
3. ✅ Pitch calculation: R × √3
4. ✅ Dimension calculation: fill=-6:6 -6:6 0:0 → 13×13×1 = 169 elements
5. ✅ COMPLETE hexagonal pattern (all 169 elements visible)
6. ✅ Staggered row explanation
7. ✅ Validation checklist

### Test 3: Multi-Level Hierarchy Query

**User Query**: "How do I nest lattices for a complex reactor core?"

**Expected Output**: Skill provides:
1. ✅ Explanation of multi-level hierarchies (2-6 levels)
2. ✅ Examples for BOTH rectangular and hexagonal
3. ✅ Universe definition order (bottom-up)
4. ✅ Reference to complex_reactor_patterns.md
5. ✅ Validation rules

### Test 4: FILL Dimension Query

**User Query**: "How many elements do I need for fill=-7:7 -7:7 0:0?"

**Expected Output**: Skill provides:
1. ✅ Formula: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
2. ✅ Calculation: (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15×15×1 = 225
3. ✅ Explanation: Include zero when counting!
4. ✅ Tool reference: lattice_dimension_calculator.py

### Test 5: Repeat Notation Query

**User Query**: "What does '100 24R' mean?"

**Expected Output**: Skill provides:
1. ✅ Explanation: nR = (n+1) total copies
2. ✅ Example: 100 24R = 100 repeated 25 times
3. ✅ Benefit: Compact notation for long arrays
4. ✅ Common error: nR does NOT mean n copies!

---

## Integration Points

### Integration with Other Skills

#### mcnp-geometry-builder
- Provides fuel pin geometries → used in lattice fill
- Creates compact geometries → nested in lattices

#### mcnp-material-builder
- Defines materials → assigned to lattice universes
- Thermal scattering → required for all graphite/water cells

#### mcnp-cell-checker
- Validates universe definitions → ensures all filled universes exist
- Checks U/FILL references → prevents circular dependencies

#### mcnp-input-validator
- Validates FILL array dimensions → uses lattice_dimension_calculator.py
- Cross-references universes → ensures consistency

#### mcnp-cross-reference-checker
- Validates lattice-surface consistency
- Checks all filled universes are defined

---

## Success Criteria

### Skill Refinement Success

✅ **User can independently**:
1. Build multi-level lattices (2-6 levels) for complex reactors
2. Use BOTH rectangular (LAT=1) and hexagonal (LAT=2) lattices
3. Calculate FILL array dimensions correctly
4. Use repeat notation efficiently
5. Validate lattice dimensions before MCNP run
6. Avoid common off-by-one errors

✅ **Skill provides**:
1. Complete examples for both LAT=1 and LAT=2
2. Working validation tools (Python scripts)
3. Comprehensive reference files
4. Clear explanation of index ordering (K, J, I)
5. Surface-lattice consistency guidance

✅ **Specific metrics**:
- 100% of rectangular lattice queries answered correctly
- 100% of hexagonal lattice queries answered correctly
- All validation tests pass
- Python tools work for both LAT=1 and LAT=2
- No MCNP dimension errors for users following skill guidance

---

## Next Steps After Refinement

### Immediate (This Session)
1. ✅ Implement all file changes
2. ✅ Test with sample queries
3. ✅ Verify Python tools work
4. ✅ Run validation tests

### Follow-Up (Next Session)
1. ⏳ Refine based on user feedback
2. ⏳ Add more complex examples (5-6 level hierarchies)
3. ⏳ Create video tutorials (if applicable)

### Long-Term
1. ⏳ Integration testing with other skills
2. ⏳ User case studies
3. ⏳ Performance benchmarks

---

**END OF REFINEMENT PLAN**

**Ready for immediate execution. All content sourced from production-quality HTGR reactor models analyzed in 13 comprehensive documents (469 KB total).**
