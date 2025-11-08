# MCNP Input File Organization Guide
## Professional Structure and Formatting Standards

**Purpose**: Comprehensive guide to organizing MCNP input files for maximum readability, maintainability, and correctness.

---

## OVERVIEW

Professional MCNP input files are characterized by:
1. **Clear three-block structure** (cells, surfaces, data)
2. **Visual hierarchy** (dividers, headers, blank lines)
3. **Comprehensive comments** (both inline and block)
4. **Logical grouping** (related cards together)
5. **Consistent formatting** (alignment, spacing)

**Result**: Files that are self-documenting, easy to debug, and maintainable over years.

---

## THE THREE-BLOCK STRUCTURE

### Mandatory Format

```mcnp
[Title Card - exactly one line]
c [Optional header comments]

c === BLOCK 1: CELL CARDS ===
[cell cards]
[blank line required]

c === BLOCK 2: SURFACE CARDS ===
[surface cards]
[blank line required]

c === BLOCK 3: DATA CARDS ===
[data cards starting with MODE]
[blank line required at end of file]
```

**Critical Rules**:
1. Title card is ALWAYS the first line (cannot start with 'c')
2. Blank lines MUST separate the three blocks
3. Blank line MUST end the file
4. MODE card MUST be first data card
5. Order within blocks can be flexible, but logical grouping improves readability

---

## BLOCK 1: CELL CARD ORGANIZATION

### Hierarchical Structure

```mcnp
c ========================================
c CELL BLOCK
c ========================================
c
c MAJOR COMPONENT 1: [Name]
c   Description of this component group
c
c Subsystem A: [Specific component]
[related cells with inline comments]
c
c Subsystem B: [Another component]
[related cells with inline comments]
c
c MAJOR COMPONENT 2: [Name]
c   Description of this component group
...
```

### Example: Reactor Core Organization

```mcnp
c ========================================
c CELL BLOCK
c ========================================
c
c FUEL ASSEMBLIES
c   PWR 17×17 assemblies with UO2 fuel
c
c Assembly A-01: Standard fuel assembly
10101 1 -10.2  -10101  u=101  imp:n=1  vol=190.5  $ Fuel rod 01
10102 1 -10.2  -10102  u=101  imp:n=1  vol=190.5  $ Fuel rod 02
...
10117 0        -10117  u=101  imp:n=1  fill=1     $ Guide tube
c
c Assembly lattice (17×17 array)
10100 0  -10100  u=100  lat=1  fill=-8:8 -8:8 0:0  $ Assembly container
      101 101 101 101 101 101 101 101 101 101 101 101 101 101 101 101 101
      [... 17 rows of universe IDs ...]
c
c CONTROL RODS
c   Hafnium absorber rods, insertable
c
c Control rod C-01: Bank position
20101 4 -13.3  -20101  imp:n=1  vol=125.6  $ Hafnium absorber
20102 2 -6.5   20101 -20102  imp:n=1      $ Stainless cladding
20103 3 -1.0   20102  imp:n=1             $ Water gap
c
c REFLECTOR
c   Graphite radial reflector
c
30001 5 -2.7   -30001  imp:n=1  $ Reflector block 1
30002 5 -2.7   -30002  imp:n=1  $ Reflector block 2
c
c OUTSIDE WORLD
c
99999 0  30002  imp:n=0  $ Particle termination boundary
```

**Key features**:
- Major sections clearly marked with heavy dividers
- Subsections identified with descriptive headers
- Related cells grouped together
- Blank comment lines separate logical groups
- Inline comments on every cell
- Volume specifications where appropriate
- Universe hierarchy visible (u=101 in cells, fill=1 in lattice)

### Grouping Strategies

**Strategy 1: By physical location**
```mcnp
c Core region (cells 10000-19999)
c Reflector region (cells 20000-29999)
c Shield region (cells 30000-39999)
```

**Strategy 2: By component type**
```mcnp
c Fuel pins (cells 101-117)
c Guide tubes (cells 201-217)
c Control rods (cells 301-317)
```

**Strategy 3: By universe hierarchy**
```mcnp
c Universe definitions (smallest first)
c   u=1: TRISO particle (5 cells)
c   u=2: Compact matrix (1 cell)
c   u=3: Particle lattice (1 cell)
c   u=4: Compact (1 cell)
```

---

## BLOCK 2: SURFACE CARD ORGANIZATION

### Grouping by Geometry Type

```mcnp
c ========================================
c SURFACE BLOCK
c ========================================
c
c SPHERICAL SURFACES
c   Concentric spheres for TRISO particles
c
91111 so  0.01748  $ Kernel radius (174.8 μm)
91112 so  0.02791  $ Buffer outer radius (279.1 μm)
91113 so  0.03179  $ IPyC outer radius (317.9 μm)
91114 so  0.03537  $ SiC outer radius (353.7 μm)
91115 so  0.03930  $ OPyC outer radius (393.0 μm)
c
c CYLINDRICAL SURFACES
c   Fuel pins and control rods
c
10101 cz  0.4096  $ Fuel pellet radius (standard PWR)
10102 cz  0.4750  $ Clad outer radius (standard PWR)
c
c Off-axis cylinders: Capsule positions
97060 c/z  25.337  -25.337  1.5191  $ Capsule 1 holder
97061 c/z  25.337  -25.337  1.5875  $ Capsule 1 gas gap
c
c PLANAR SURFACES
c   Axial segmentation
c
98000 pz    0.00    $ Bottom of active core
98010 pz   36.58    $ Axial zone 1/2 interface
98020 pz   73.15    $ Axial zone 2/3 interface
98030 pz  365.76    $ Top of active core
c
c RECTANGULAR BOXES
c   Assembly boundaries
c
10100 rpp -10.71 10.71 -10.71 10.71 -180 180  $ Assembly box
```

**Organization principles**:
1. Group by surface type (SO, CZ, C/Z, PZ, RPP, etc.)
2. Within type, order logically (concentric, axial progression)
3. Include dimensions in comments with units
4. Note special features (off-axis centers, calculated values)
5. Use blank comment lines to separate groups

### Alternative: Group by Component

```mcnp
c ========================================
c SURFACE BLOCK
c ========================================
c
c TRISO PARTICLE SURFACES
c   All surfaces for particle u=1114
c
91111 so  0.01748  $ Kernel radius
91112 so  0.02791  $ Buffer outer
91113 so  0.03179  $ IPyC outer
91114 so  0.03537  $ SiC outer
91115 so  0.03930  $ OPyC outer
c
c FUEL PIN SURFACES
c   Cylindrical fuel rods
c
10101 cz  0.4096  $ Fuel radius
10102 cz  0.4178  $ Gap outer
10103 cz  0.4750  $ Clad outer
```

---

## BLOCK 3: DATA CARD ORGANIZATION

### Standard Ordering

```mcnp
c ========================================
c DATA BLOCK
c ========================================
c
c 1. MODE (REQUIRED FIRST)
MODE N P
c
c 2. MATERIALS
c
c Fuel materials
m1  $ UO2 fuel, 3.5% enriched
   92234.70c  0.00030
   92235.70c  0.03500
   92238.70c  0.96470
    8016.70c  2.00000
c
c Moderator/coolant
m2  $ Light water at 300K
    1001.70c  2.0
    8016.70c  1.0
mt2  lwtr.01t  $ S(α,β) thermal scattering
c
c Structural materials
m3  $ Zircaloy-4 cladding
   40000.70c  0.9800
   50000.70c  0.0146
   [...]
c
c 3. SOURCE DEFINITION
c
c Fixed source (or KCODE for criticality)
sdef  pos=0 0 0  erg=d1  par=n
sp1   -3  0.8  2.5  $ Watt fission spectrum
c
c OR for criticality:
c kcode  10000  1.0  50  150
c ksrc   0 0 0
c
c 4. TALLIES
c
c Cell flux tallies
f4:n   10101 10102 10103  $ Fuel regions
e4     0.01 0.1 1 10      $ Energy bins (MeV)
c
c Point detector
f5:n   100 0 0  0.5       $ Detector at x=100 cm
e5     0.01 0.1 1 10
c
c Surface current
f1:n   10100               $ Current through surface
c
c 5. VARIANCE REDUCTION (if needed)
c
c Cell importance
imp:n  1 1 1 0  $ Last cell is graveyard (imp=0)
c
c OR weight windows
c wwn:n  ...
c
c 6. PHYSICS OPTIONS
c
c Energy cutoffs
cut:n  j j j j  $ Use default cutoffs
c
c Physics model controls
phys:n  20.0  $ Max neutron energy (MeV)
c
c 7. OUTPUT CONTROL
c
c Print controls
print  10 30 40 50 110  $ Standard output tables
c
c 8. TERMINATION
c
c Particle history limit
nps    10000000
c
c OR time limit
c ctme   120  $ 120 minutes
```

**Ordering rationale**:
1. **MODE** - Required first, sets particle types
2. **Materials** - Needed before tallies (for normalization)
3. **Source** - Defines particle generation
4. **Tallies** - What to calculate
5. **Variance reduction** - How to improve efficiency
6. **Physics** - Advanced options
7. **Output** - What to print
8. **Termination** - When to stop

### Grouping Related Cards

Keep related cards together:

```mcnp
c Tally 4: Cell flux in fuel
f4:n   10101 10102 10103   $ Fuel cells
e4     0.01 0.1 1 10       $ Energy bins
fc4    Fuel region flux    $ Tally comment
fm4    -1 1 -6             $ Fission multiplier
sd4    190.5 190.5 190.5   $ Segment divisor (volumes)
c
c Tally 14: Cell flux in reflector
f14:n  30001 30002          $ Reflector cells
e14    0.01 0.1 1 10        $ Energy bins
fc14   Reflector flux       $ Tally comment
```

---

## VISUAL HIERARCHY

### Section Dividers

**Heavy dividers** for major sections:
```mcnp
c ========================================
c MAJOR SECTION NAME
c ========================================
```

**Medium dividers** for subsections:
```mcnp
c --- Subsection Name ---
```

**Light dividers** for related groups:
```mcnp
c Grouping comment
```

### Example of Full Hierarchy

```mcnp
c ========================================
c CELL BLOCK
c ========================================
c
c --- FUEL ASSEMBLIES ---
c
c Assembly A-01: Standard 17×17
[cells]
c
c Assembly A-02: Standard 17×17
[cells]
c
c --- CONTROL RODS ---
c
c Bank C: Hafnium absorbers
[cells]
```

---

## FORMATTING STANDARDS

### Alignment

**Align cell cards** for readability:

```mcnp
c Good: Aligned columns
10101  1  -10.20  -10101        u=101  imp:n=1  vol=190.5   $ Fuel rod 01
10102  1  -10.20  -10102        u=101  imp:n=1  vol=190.5   $ Fuel rod 02
10117  0          -10117        u=101  imp:n=1              $ Guide tube
20101  4  -13.30  -20101               imp:n=1  vol=125.6   $ Hafnium
```

**Align surface cards**:

```mcnp
c Good: Aligned parameters
91111  so    0.017485   $ Kernel radius
91112  so    0.027905   $ Buffer outer radius
97060  c/z   25.337  -25.337   1.51913   $ Off-axis cylinder
98000  pz     0.00      $ Bottom boundary
```

**Align material cards**:

```mcnp
m1  $ UO2 fuel
   92234.70c  0.00030   $ U-234
   92235.70c  0.03500   $ U-235 (3.5% enriched)
   92238.70c  0.96470   $ U-238 (balance)
    8016.70c  2.00000   $ O-16 (stoichiometric)
```

### Spacing

**Use blank comment lines** to separate groups:

```mcnp
c Fuel pins
[fuel pin cells]
c
c Guide tubes
[guide tube cells]
c
c Instrumentation
[instrument cells]
```

**Use blank lines** (NOT blank comment lines) only between blocks:

```mcnp
[last cell card]

[first surface card]
```

---

## CONTINUATION LINES

### Five-Space Indentation

For long cards, indent continuation lines by 5+ spaces:

```mcnp
f4:n  10101 10102 10103 10104 10105 10106 10107 10108 10109 10110
      10111 10112 10113 10114 10115 10116 10117
```

### Ampersand (&) Method

```mcnp
f4:n  10101 10102 10103 10104 10105 10106 10107 10108 10109 10110 &
      10111 10112 10113 10114 10115 10116 10117
```

### Lattice Fill Arrays

Align lattice fills for visual clarity:

```mcnp
c 15×15 particle lattice (u=1116)
91108 0  -91117  u=1116  lat=1  fill=-7:7 -7:7 0:0
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1115 1115 1114 1114 1114 1114 1114 1115 1115 1115 1115 1115
     1115 1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115 1115
     1115 1115 1115 1115 1115 1114 1114 1114 1114 1114 1115 1115 1115 1115 1115
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
```

---

## FILE HEADER DOCUMENTATION

### Comprehensive Header Template

```mcnp
c ========================================
c MODEL NAME AND PURPOSE
c ========================================
c
c Model: AGR-1 HTGR Experiment Capsule 1
c Description: TRISO fuel compact irradiation test
c Purpose: Neutronics analysis for fission rate and burnup
c
c Version: 2.1
c Author: [Name/Organization]
c Date Created: 2024-01-15
c Last Modified: 2024-03-22
c
c GEOMETRY DESCRIPTION:
c   - 6 capsules in vertical stack
c   - Each capsule contains 12 fuel compacts
c   - Compacts contain TRISO particles in graphite matrix
c   - Five-layer TRISO coating (Buffer/IPyC/SiC/OPyC)
c
c NUMBERING SCHEME:
c   Cells:     9XYZW (9=AGR, X=capsule, Y=stack, Z=compact, W=seq)
c   Surfaces:  9XYZn (correlated with cells)
c   Materials: 9XYZ (kernels) or 909X (shared coatings)
c   Universes: XYZW (XYZ=position, W=component type)
c
c RESERVED RANGES:
c   90000-96999: Capsule hardware and structures
c   97000-97999: Capsule surfaces (cylinders, planes)
c   98000-98999: Axial segmentation planes
c   91000-91999: Capsule 1 cells
c   92000-92999: Capsule 2 cells
c   [etc.]
c
c UNIVERSE COMPONENT TYPES (W digit):
c   0 = Lattice container
c   4 = TRISO particle (5-layer structure)
c   5 = Matrix filler (no particle)
c   6 = Particle lattice (15×15)
c   7 = Alternative matrix
c
c UNITS:
c   Lengths: cm
c   Densities: g/cm³ (negative) or atoms/barn-cm (positive)
c   Energies: MeV
c   Temperatures: K (in cross-section library extensions)
c
c MATERIALS:
c   m9111-m9641: UCO kernels (unique per compact)
c   m9090: Buffer carbon (shared)
c   m9091: IPyC (shared)
c   m9092: SiC (shared)
c   m9093: OPyC (shared)
c   m9094: Matrix graphite (shared)
c   m9000-9010: Structural materials (steel, graphite)
c
c REFERENCE DOCUMENTS:
c   - AGR-1 Irradiation Experiment Test Plan, INL/EXT-05-00593
c   - TRISO Fuel Specification, INL/EXT-10-17686
c   - Capsule Design Drawings, DWG-AGR-1-001 through DWG-AGR-1-012
c
c PHYSICS SETTINGS:
c   - Neutron transport only (MODE N)
c   - Continuous energy (no multigroup)
c   - ENDF/B-VII.1 cross sections at 900K for fuel
c   - S(α,β) thermal scattering for graphite (grph.18t = 600K)
c
c CALCULATION TYPE:
c   - Fixed source (fission neutron spectrum)
c   - 100 million histories (NPS 100000000)
c   - Tallies: F4 (cell flux), F6 (heating), F7 (fission)
c
c ASSUMPTIONS:
c   1. Room temperature (300K) for structural materials
c   2. No depletion (fresh fuel, no burnup)
c   3. Particle locations random (stochastic lattice)
c   4. No fuel failure (all coatings intact)
c
c KNOWN LIMITATIONS:
c   1. No temperature feedback (fixed T)
c   2. No xenon or fission products
c   3. Simplified particle packing (lattice vs. random)
c
c VALIDATION STATUS:
c   - Geometry plotted and verified (no overlaps/gaps)
c   - Material densities checked against specifications
c   - Universe hierarchy validated (no circular refs)
c   - Cross-references validated (all entities defined)
c
c ========================================
```

**This header provides**:
- Model identification and purpose
- Versioning and authorship
- Complete numbering scheme documentation
- Units and conventions
- Reference documentation
- Physics settings
- Assumptions and limitations
- Validation status

---

## QUALITY CHECKLIST

### Before Finalizing Input File

**Structure**:
- [ ] Title card is first line (not a comment)
- [ ] Three blocks clearly separated by blank lines
- [ ] Blank line at end of file
- [ ] MODE card is first data card

**Organization**:
- [ ] Major sections have heavy dividers
- [ ] Subsections have descriptive headers
- [ ] Related cards grouped together
- [ ] Logical ordering within blocks

**Formatting**:
- [ ] Consistent alignment (columns line up)
- [ ] Spaces only (NO TABS)
- [ ] Continuation lines properly indented (5+ spaces)
- [ ] Lattice fills aligned for clarity

**Comments**:
- [ ] File header with comprehensive documentation
- [ ] Inline comments on all non-trivial cards
- [ ] Section dividers and headers
- [ ] Blank comment lines separate groups
- [ ] Units specified where needed

**Validation**:
- [ ] All referenced entities exist (surfaces, materials, universes)
- [ ] Numbering scheme documented
- [ ] No numbering conflicts
- [ ] Universe hierarchy correct (child before parent)

---

## COMMON ORGANIZATION MISTAKES

### Mistake 1: No Visual Structure

**BAD**:
```mcnp
[title]
1 1 -10.2 -1 imp:n=1
2 2 -8.0 -2 imp:n=1
3 3 -1.0 -3 imp:n=1
999 0 3 imp:n=0

1 so 5
2 so 10
3 so 15

mode n
m1 ...
m2 ...
nps 1000000
```

**GOOD**:
```mcnp
[title with description]
c ========================================
c CELL BLOCK
c ========================================
c
c Fuel sphere
1  1  -10.2  -1  imp:n=1  vol=523.6  $ UO2 fuel
c
c Structural layers
2  2  -8.0    1 -2  imp:n=1  $ Steel shell
3  3  -1.0    2 -3  imp:n=1  $ Water moderator
c
c Outside world
999  0  3  imp:n=0  $ Particle graveyard

c ========================================
c SURFACE BLOCK
c ========================================
c
c Concentric spheres
1  so   5.0   $ Fuel outer radius (cm)
2  so  10.0   $ Steel outer radius
3  so  15.0   $ Water outer boundary

c ========================================
c DATA BLOCK
c ========================================
c
MODE N
c
c Materials
m1  [...]  $ UO2 fuel
m2  [...]  $ Stainless steel
m3  [...]  $ Water
c
c Termination
NPS 1000000
```

### Mistake 2: Inconsistent Grouping

**BAD**: Cells scattered by number
```mcnp
1 1 -10.2 -1 imp:n=1  $ Fuel pin 1
100 2 -8.0 -100 imp:n=1  $ Control rod
2 1 -10.2 -2 imp:n=1  $ Fuel pin 2
101 2 -8.0 -101 imp:n=1  $ Control rod 2
```

**GOOD**: Cells grouped by component
```mcnp
c Fuel pins
1 1 -10.2 -1 imp:n=1  $ Fuel pin 1
2 1 -10.2 -2 imp:n=1  $ Fuel pin 2
c
c Control rods
100 2 -8.0 -100 imp:n=1  $ Control rod 1
101 2 -8.0 -101 imp:n=1  $ Control rod 2
```

### Mistake 3: Poor Data Card Ordering

**BAD**: Random order
```mcnp
nps 1000000
f4:n 1
m1 ...
mode n
e4 0.1 1 10
sdef ...
```

**GOOD**: Logical order
```mcnp
mode n
m1 ...
sdef ...
f4:n 1
e4 0.1 1 10
nps 1000000
```

---

## SUMMARY

**Professional input file organization requires**:
1. ✅ Clear three-block structure with blank line separators
2. ✅ Visual hierarchy (heavy/medium/light dividers)
3. ✅ Logical grouping (by location, component, or hierarchy)
4. ✅ Consistent formatting (alignment, spacing)
5. ✅ Comprehensive header documentation
6. ✅ Inline and block comments throughout
7. ✅ Standard data card ordering (MODE → Materials → Source → Tallies → Termination)

**Result**: Self-documenting files that are easy to understand, debug, and maintain.

---

**END OF ORGANIZATION GUIDE**
