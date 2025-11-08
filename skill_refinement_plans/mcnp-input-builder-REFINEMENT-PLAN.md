# MCNP-INPUT-BUILDER SKILL REFINEMENT PLAN
## Systematic Input File Organization and Numbering Schemes

**Created**: November 8, 2025
**Priority**: 🟡 **MEDIUM** (Phase 2)
**Based On**: AGR-1 HTGR reactor model analysis (250,000+ lines analyzed)

---

## EXECUTIVE SUMMARY

Current **mcnp-input-builder** skill teaches basic input file structure but LACKS critical patterns found in professional reactor models:

1. ❌ **No systematic numbering schemes** (hierarchical encoding)
2. ❌ **No cross-reference validation guidance**
3. ❌ **No comment conventions** (inline descriptive style)
4. ❌ **No organization best practices** (grouping, blank lines)
5. ❌ **No volume calculation guidance**
6. ❌ **No universe hierarchy planning**

**Impact**: Users can create simple inputs but CANNOT build maintainable complex reactor models with thousands of cells/surfaces/materials.

**What was learned from AGR-1 analysis**:
- 1,607 cells organized with **systematic 5-digit numbering** (9XYZW)
- 725+ surfaces using **hierarchical encoding** (component/position)
- 385 materials with **correlation to geometry** (same numbering basis)
- **Zero numbering conflicts** across all entities
- **Instant debuggability** (number tells you location/function)

---

## PART 1: CRITICAL GAPS IDENTIFIED

### Gap 1: Systematic Numbering Schemes

**Current state**: Skill suggests "use sequential numbers" with no structure

**Professional practice** (from AGR-1):
```python
# Hierarchical encoding embeds location/function in number itself
cell_id = 90000 + capsule*1000 + stack*100 + compact*20 + sequence
surface_id = 9000 + capsule*100 + stack*10 + compact
material_id = 9000 + capsule*100 + stack*10 + compact
universe_id = capsule*1000 + stack*100 + compact*10 + component_type
```

**Benefits**:
- Zero numbering conflicts (automatic separation)
- Instant identification of location from number
- Enables automated generation
- Simplifies debugging (know where to look)
- Scalable to large models

### Gap 2: Three-Block Organization

**Current state**: Basic mention of cell/surface/material blocks

**Professional practice**:
```mcnp
c ========================================
c CELL BLOCK
c ========================================
c
c Capsule 1, Stack 1, Compact 1 - TRISO Particles
c
91101 9111 -10.924 -91111         u=1114 vol=0.092522  $ Kernel
91102 9090 -1.100  91111 -91112  u=1114              $ Buffer
...

c ========================================
c SURFACE BLOCK
c ========================================
c
c TRISO Particle Surfaces - Capsule 1, Stack 1, Compact 1
c
91111 so   0.017485  $ Kernel radius
91112 so   0.027905  $ Buffer outer radius
...

c ========================================
c MATERIAL BLOCK
c ========================================
c
c UCO Fuel Kernels
c
m9111  $ kernel, UCO: density=10.924 g/cm3, Capsule 1 Stack 1 Compact 1
   92235.00c  1.99636E-01
   92238.00c  7.96829E-01
...
```

**Key patterns**:
- Heavy use of comment dividers (`c ===...`)
- Inline comments with `$` on EVERY important line
- Blank comment lines (`c`) for visual separation
- Descriptive headers for each section
- Comments BEFORE complex sections (not just inline)

### Gap 3: Cross-Reference Consistency

**Current state**: No validation guidance

**Professional requirements**:
1. Every surface referenced in cell MUST be defined
2. Every material referenced in cell MUST be defined
3. Every universe referenced in fill MUST be defined
4. Every universe filled MUST be defined BEFORE use
5. Universe 0 is global (never explicitly defined)
6. No circular universe references

**Example validation needed**:
```mcnp
91111 0  -97011  98005 -98051 fill=1110  (25.547 -24.553 19.108)
      ^   ^^^^^  ^^^^^  ^^^^^       ^^^^
      |     |      |      |           |
      |     |      |      |           └─ Universe 1110 must exist
      |     |      |      └─ Surface 98051 must exist
      |     |      └─ Surface 98005 must exist
      |     └─ Surface 97011 must exist
      └─ Material 0 is valid (void for fill)
```

### Gap 4: Volume Specifications

**Current state**: Not mentioned

**Professional practice**:
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel
                                   ^^^^^^^^^^^^
                                   Pre-calculated volume
```

**When to specify volumes**:
- ✅ Fuel kernels/pellets (tally normalization)
- ✅ Small important regions (variance reduction)
- ✅ Repeated structures (one calculation serves all)
- ❌ Large simple regions (MCNP can calculate)
- ❌ Lattice containers (ignored by MCNP)

**Benefits**:
- Faster MCNP execution (skip stochastic volume calc)
- More accurate reaction rate tallies
- Enables power normalization
- Required for some depletion codes

### Gap 5: Importance Specifications

**Current state**: Not mentioned in input building context

**Professional practice**:
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522  imp:n=1  $ Kernel
                                                 ^^^^^^^^
                                                 Neutron importance
```

**Standard patterns**:
- `imp:n=1` - normal transport region
- `imp:n=0` - particle termination boundary (outside world)
- `imp:n=10` - variance reduction (10× more particles)
- `imp:n,p=1 1` - neutron AND photon importance

**Best practice**: Always specify importance (no default assumption)

---

## PART 2: REFINEMENT SPECIFICATIONS

### 2.1 Update SKILL.md

**File**: `.claude/skills/mcnp-input-builder/SKILL.md`
**Current length**: ~400 lines (can expand significantly)

**ADD new major section after existing content**:

```markdown
## SYSTEMATIC NUMBERING SCHEMES

### Why Systematic Numbering Matters

**Problem with sequential numbering**:
```mcnp
c Bad: Sequential with no structure
1 1 -10.2  -1  imp:n=1  $ What is this?
2 1 -10.2  -2  imp:n=1  $ Where is this?
3 2 -6.5   -3  imp:n=1  $ What component?
...
```

**Professional approach - hierarchical encoding**:
```mcnp
c Good: Encoded location/function
11101 1 -10.2  -11101  imp:n=1  $ Capsule 1, Stack 1, Compact 1, Cell 01
11102 1 -10.2  -11102  imp:n=1  $ Capsule 1, Stack 1, Compact 1, Cell 02
12101 1 -10.2  -12101  imp:n=1  $ Capsule 1, Stack 2, Compact 1, Cell 01
```

**From the number alone**: 11101 → Capsule 1, Stack 1, Compact 1, sequence 01

### Pattern 1: Hierarchical Position Encoding

**For multi-level geometries** (assemblies, compacts, layers):

```python
# Template: XYZSS
# X = Major component (1-9)
# Y = Sub-component (0-9)
# Z = Layer/level (0-9)
# SS = Sequence (00-99)

cell_id = X*10000 + Y*1000 + Z*100 + sequence

# Examples:
11101 = Component 1, Sub 1, Layer 1, sequence 01
23407 = Component 2, Sub 3, Layer 4, sequence 07
```

**Apply to cells, surfaces, materials, universes consistently!**

### Pattern 2: Functional Subsystem Ranges

**Reserve number blocks for subsystems**:

```mcnp
c Fuel elements: 10000-19999
c Control rods:  20000-29999
c Reflector:     30000-39999
c Shield:        40000-49999
c Coolant:       50000-59999
c Structures:    60000-69999
```

**Benefits**:
- No conflicts between subsystems
- Instant identification: "cell 23456 = control rod component"
- Easy to add components within subsystem
- Clear organization in large files

### Pattern 3: Universe Component Encoding

**For repeated structures** (lattices, assemblies):

```python
# Template: XYZW
# XYZ = Location/position encoding
# W = Component type indicator

universe_id = position*10 + component_type

# Component types:
# 0 = Lattice container
# 1 = Fuel region
# 2 = Coolant channel
# 3 = Structural element
# 4 = Special (e.g., TRISO particle)
# 5 = Matrix/filler
# 6 = Sub-lattice
# 7 = Alternative filler

# Examples:
1114 = Position 111, TRISO particle (type 4)
1115 = Position 111, Matrix filler (type 5)
1116 = Position 111, Particle lattice (type 6)
1110 = Position 111, Compact lattice container (type 0)
```

**Critical**: Same position uses same XYZ digits, different W for different components

### Pattern 4: Correlated Numbering

**Use SAME encoding for related entities**:

```mcnp
c Cell, surface, material for same component share base number
c
c Cell 11101 uses surface 11101 and material 111
11101 111 -10.5  -11101  u=1114  imp:n=1  $ Fuel kernel
      ^^^   ^^^^^
      Mat   Surface (same base: 111)
```

**Enables instant cross-referencing**:
- Cell 11101 → look for surface 11101 and material 111
- Debug errors faster (know which components connect)
- Automated generation simpler

### Validation Checklist for Numbering

Before finalizing input file:

- [ ] Numbering scheme documented (comment at top)
- [ ] No number reuse across entity types (cell 100 ≠ surface 100 OK, but clarify)
- [ ] Hierarchical encoding consistent throughout
- [ ] Reserved ranges respected (no overlap)
- [ ] Universe numbers unique (critical!)
- [ ] Correlated entities use related numbers

## THREE-BLOCK STRUCTURE BEST PRACTICES

### Block 1: Cell Cards

**Organization pattern**:

```mcnp
c ========================================
c CELL BLOCK
c ========================================
c
c SECTION: Major Component Name
c Subsection: Specific sub-component
c
c Description of what these cells represent
c
[cells with inline comments]
c
c [blank comment for visual separation]
c
c SECTION: Next Major Component
...
```

**Example from AGR-1 model**:

```mcnp
c ========================================
c CELL BLOCK
c ========================================
c
c CAPSULE 1, STACK 1, COMPACT 1 - TRISO PARTICLES
c
c Five-layer TRISO particle structure (u=1114)
91101 9111 -10.924 -91111         u=1114 vol=0.092522  $ Kernel (UO2)
91102 9090 -1.100  91111 -91112  u=1114              $ Buffer (porous C)
91103 9091 -1.904  91112 -91113  u=1114              $ IPyC (dense C)
91104 9092 -3.205  91113 -91114  u=1114              $ SiC (barrier)
91105 9093 -1.911  91114 -91115  u=1114              $ OPyC (dense C)
91106 9094 -1.344  91115         u=1114              $ SiC Matrix
c
c Matrix filler cell (u=1115)
91107 9094 -1.344 -91116         u=1115              $ Matrix (no particle)
c
c Particle lattice (u=1116) - 15×15 array
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice container
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     [... 15 rows total ...]
```

**Key patterns**:
1. Heavy dividers (`c ===...`) for major sections
2. Descriptive section headers (capitalized)
3. Sub-headers for components
4. Blank comment lines (`c`) between logical groups
5. Inline `$` comments on EVERY non-trivial cell
6. Volume specifications where appropriate
7. Universe specifications clearly visible
8. Lattice fills have dimension comments

### Block 2: Surface Cards

**Organization pattern**:

```mcnp
c ========================================
c SURFACE BLOCK
c ========================================
c
c SECTION: Geometry subsystem
c
c Description of surface group
c
[surfaces with inline comments including dimensions]
```

**Example**:

```mcnp
c ========================================
c SURFACE BLOCK
c ========================================
c
c TRISO PARTICLE SURFACES - Capsule 1, Stack 1, Compact 1
c
c Concentric spherical shells (SO surfaces centered at origin)
91111 so   0.017485  $ Kernel radius (174.85 μm)
91112 so   0.027905  $ Buffer outer radius (279.05 μm)
91113 so   0.031785  $ IPyC outer radius (317.85 μm)
91114 so   0.035375  $ SiC outer radius (353.75 μm)
91115 so   0.039305  $ OPyC outer radius (393.05 μm)
c
c Lattice element bounding surfaces
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
                  $ Particle lattice element (0.87×0.87×1.0 mm)
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
                  $ Compact lattice element (13×13×0.87 mm)
c
c Cylindrical compact boundary
91119 c/z  0.0  0.0   0.6500  $ Compact outer radius (6.35 mm)
c
c CAPSULE CONCENTRIC CYLINDERS
c
c Off-axis cylinders centered at (25.337, -25.337) mm
97060 c/z   25.337    -25.337      1.51913  $ Compact holder outer R
97061 c/z   25.337    -25.337      1.58750  $ Gas gap outer R
97062 c/z   25.337    -25.337      1.62179  $ Inner capsule wall outer R
97063 c/z   25.337    -25.337      1.64719  $ Hf shroud outer R
97064 c/z   25.337    -25.337      1.64846  $ Gas gap outer R
97065 c/z   25.337    -25.337      1.78562  $ Capsule wall outer R
97066 c/z   25.337    -25.337      1.90500  $ B-10 channel outer R
c
c AXIAL SEGMENTATION PLANES
c
98000 pz   -2.54000      $ Bottom boundary
98001 pz   13.65758      $ Bottom of Stack 1
98005 pz   17.81810      $ Bottom of Compact 1
98051 pz   20.35810      $ Top of Compact 1 (calculated)
98006 pz   22.89810      $ Bottom of Compact 2
```

**Critical elements**:
1. Units in comments (μm, mm, cm)
2. Calculated vs. specified values noted
3. Off-axis centers documented
4. Physical meaning (not just numbers)
5. Grouping by geometry type (spheres, cylinders, planes)

### Block 3: Material Cards

**Organization pattern**:

```mcnp
c ========================================
c MATERIAL BLOCK
c ========================================
c
c SECTION: Material category
c
c Material ID: Description, density, source
c
[material composition]
[thermal scattering if needed]
```

**Example**:

```mcnp
c ========================================
c MATERIAL BLOCK
c ========================================
c
c UCO FUEL KERNELS
c
c Material m9111: UCO kernel, 19.96% enriched, density=10.924 g/cm3
c Location: Capsule 1, Stack 1, Compact 1
m9111
   92234.00c  3.34179E-03  $ U-234 (0.334% of U)
   92235.00c  1.99636E-01  $ U-235 (19.96% enrichment)
   92236.00c  1.93132E-04  $ U-236 (trace)
   92238.00c  7.96829E-01  $ U-238 (balance)
    6012.00c  0.3217217    $ C-12 (carbide)
    6013.00c  0.0035783    $ C-13 (natural abundance)
    8016.00c  1.3613       $ O-16 (oxide)
c Formula: UC₀.₃₂O₁.₃₆ (uranium carbide-oxide)
c
c TRISO COATING LAYERS (shared across all particles)
c
c Material m9090: Buffer layer, porous carbon, density=1.10 g/cm3
m9090
    6012.00c  0.9890  $ C-12 (98.9%)
    6013.00c  0.0110  $ C-13 (1.1%, natural)
c
c Material m9091: IPyC (Inner Pyrolytic Carbon), density=1.912 g/cm3
m9091
    6012.00c  0.9890  $ C-12
    6013.00c  0.0110  $ C-13
mt9091  grph.18t  $ ← CRITICAL: Graphite thermal scattering at 600K
c
c Material m9092: SiC (Silicon Carbide), density=3.207 g/cm3
m9092
   14028.00c  0.4610  $ Si-28 (92.2% of Si)
   14029.00c  0.0235  $ Si-29 (4.7%)
   14030.00c  0.0155  $ Si-30 (3.1%)
    6012.00c  0.4950  $ C-12 (98.9% of C, stoichiometric SiC)
    6013.00c  0.0055  $ C-13 (1.1%)
mt9092  grph.18t  $ Graphite S(α,β) for carbon component
c
c STAINLESS STEEL STRUCTURES
c
c Material m9000: SS316L, density=8.03 g/cm3 (mass fractions)
m9000
   24050.00c -0.00653131  $ Cr-50
   24052.00c -0.14263466  $ Cr-52 (dominant Cr isotope)
   24053.00c -0.01730730  $ Cr-53
   24054.00c -0.00352673  $ Cr-54
   25055.00c -0.02000000  $ Mn-55
   26054.00c -0.03799186  $ Fe-54
   26056.00c -0.60409084  $ Fe-56 (dominates, 60.4% by mass)
   26057.00c -0.01336731  $ Fe-57
   28058.00c -0.08053185  $ Ni-58 (major Ni isotope)
   [... complete isotopic breakdown ...]
c Note: Negative numbers = mass fractions (sum to 1.0)
```

**Critical patterns**:
1. Density in comment BEFORE material definition
2. Location/purpose in comment
3. Enrichment percentages noted
4. Dominant isotopes marked
5. MT cards immediately after material
6. Chemical formula provided
7. Physical phase (solid, liquid, gas)
8. Temperature conditions

## CROSS-REFERENCE VALIDATION

### Rule 1: All Referenced Entities Must Exist

**Check surfaces**:
```mcnp
60106 2106 7.97E-02  1111 -1118  74 -29  53  100 -110
                     ^^^^ ^^^^^  ^^  ^^  ^^  ^^^  ^^^
                     All these surface numbers MUST be defined
```

**Check materials**:
```mcnp
60106 2106 7.97E-02  [geometry]
      ^^^^
      Material m2106 MUST be defined
```

**Check universes**:
```mcnp
91111 0  -97011  98005 -98051 fill=1110  (25.547 -24.553 19.108)
                               ^^^^
                               Universe u=1110 MUST be defined
```

### Rule 2: Universe Hierarchy

**Define child before parent**:
```mcnp
c CORRECT order:
c 1. Define u=1114 (TRISO particle)
c 2. Define u=1115 (matrix cell)
c 3. Define u=1116 (lattice) - fills with 1114, 1115
c 4. Define u=1110 (compact) - fills with 1116
c 5. Use fill=1110 in global cell

c WRONG order:
c Trying to fill with u=1110 before defining it → ERROR
```

**No circular references**:
```mcnp
c WRONG:
100 0  -100  u=200 fill=300
200 0  -200  u=300 fill=200  $ ← Circular! 300 fills 200, 200 fills 300
```

### Rule 3: Material-Density Correlation

**Atom density (positive)**:
```mcnp
m1
    1001.70c  0.0667  $ Fractions in material card
    8016.70c  0.0333
c
c Cell uses TOTAL density
1 1 0.1000  [geometry]  $ Total = 0.1 atoms/barn-cm
```

**Mass density (negative)**:
```mcnp
m2
   26056.00c -0.604  $ Mass fractions (sum to 1.0)
   24052.00c -0.143
c
c Cell uses mass density
2 2 -8.03  [geometry]  $ -8.03 g/cm³
```

**CRITICAL**: Positive density → atom fractions, Negative density → mass fractions

## VOLUME SPECIFICATIONS

### When to Specify Volumes

**DO specify volumes for**:
1. ✅ Fuel kernels/pellets (repeated many times)
2. ✅ Small critical regions (absorbers, detectors)
3. ✅ Tally normalization cells (reaction rate → power)
4. ✅ Regions where stochastic volume calc is slow

**DON'T specify volumes for**:
1. ❌ Large simple regions (MCNP calculates fast)
2. ❌ Lattice containers (volume ignored)
3. ❌ Void cells (no material)
4. ❌ Cells where volume uncertain

### Volume Calculation Examples

**Spherical kernel**:
```mcnp
c Kernel radius r = 0.017485 cm
c Volume = (4/3) × π × r³ = (4/3) × π × (0.017485)³ = 2.240E-05 cm³

91101 9111 -10.924 -91111  u=1114 vol=2.240E-05  $ Kernel
```

**Cylindrical fuel pin**:
```mcnp
c Fuel radius r = 0.41 cm, height h = 360 cm
c Volume = π × r² × h = π × (0.41)² × 360 = 190.07 cm³

100 1 -10.2  -100  vol=190.07  $ UO2 fuel pellet
```

**Rectangular region**:
```mcnp
c Box: 10 × 10 × 20 cm
c Volume = 10 × 10 × 20 = 2000 cm³

200 2 -2.7  -200  vol=2000  $ Graphite block
```

**For repeated structures (lattice elements)**:
```mcnp
c One particle, volume specified
91101 9111 -10.924 -91111  u=1114 vol=2.240E-05  $ Kernel
c
c This same volume applies to ALL 4,000 instances of universe 1114
c Total fuel volume = 4000 × 2.240E-05 = 0.0896 cm³
```

## IMPORTANCE SPECIFICATIONS

### Standard Patterns

**Normal transport region**:
```mcnp
100 1 -10.2  -100  imp:n=1  $ Standard importance
```

**Outside world (kill boundary)**:
```mcnp
999 0  100  imp:n=0  $ Particles terminate here
```

**Multi-particle importance**:
```mcnp
100 1 -10.2  -100  imp:n=1 imp:p=1  $ Neutron and photon
c Or shorthand:
100 1 -10.2  -100  imp:n,p=1 1
```

**Variance reduction** (advanced):
```mcnp
c Increase importance toward detector
100 1 -10.2  -100  imp:n=1    $ Source region
200 2 -8.0   -200  imp:n=4    $ Shield region 1
300 2 -8.0   -300  imp:n=16   $ Shield region 2
400 0        -400  imp:n=64   $ Near detector (64× more particles)
500 3 -0.001 -500  imp:n=64   $ Detector region
999 0         500  imp:n=0    $ Kill boundary
```

**Best practice**: Always specify importance explicitly (don't rely on defaults)

## COMMENT CONVENTIONS

### Inline Comments ($ syntax)

**Every important line**:
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel (UO2, 19.96% enriched)
      ^^^^  ^^^^^^^  ^^^^^   ^^^^      ^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      Mat   Density  Geom    Univ      Volume    ← Descriptive comment
```

**What to include in inline comments**:
- Physical component name
- Material phase/type
- Key dimensions or properties
- Location (if not obvious from numbering)
- Special notes (calculated, estimated, critical)

### Block Comments (c syntax)

**Section dividers**:
```mcnp
c ========================================
c MAJOR SECTION NAME
c ========================================
```

**Subsection headers**:
```mcnp
c SUBSECTION: Component Name
c
c Brief description of what follows
```

**Blank separators**:
```mcnp
[group of related cards]
c
[next group]
```

**Multi-line descriptions**:
```mcnp
c This is a complex geometry section
c Multiple lines of explanation
c Critical notes about modeling assumptions
[cards]
```

### Top-of-File Documentation

**Standard header template**:
```mcnp
c ========================================
c MODEL NAME AND PURPOSE
c ========================================
c
c Description: [What this model represents]
c Version: [Version number or date]
c Author: [Name/organization]
c Date: [Creation/modification date]
c
c NUMBERING SCHEME:
c   Cells:     XYZSS (X=component, Y=sub, Z=layer, SS=sequence)
c   Surfaces:  XYZn (correlated with cells)
c   Materials: XYZ (base numbering)
c   Universes: XYZW (W=component type: 0=container, 4=particle, etc.)
c
c RESERVED RANGES:
c   10000-19999: Fuel assemblies
c   20000-29999: Control elements
c   30000-39999: Reflector
c   40000-49999: Shield
c
c UNITS:
c   Lengths: cm
c   Densities: g/cm³ (negative) or atoms/barn-cm (positive)
c   Energies: MeV
c
c REFERENCE DOCUMENTS:
c   [List key references, drawings, data sources]
c
c ========================================
```

## INPUT FILE CHECKLIST

Before running MCNP:

### Structure
- [ ] Three-block organization (cells, surfaces, materials)
- [ ] Header with model description and numbering scheme
- [ ] Section dividers for major components
- [ ] Blank comment lines for visual separation

### Numbering
- [ ] Systematic numbering scheme applied consistently
- [ ] No numbering conflicts within entity types
- [ ] Universe numbers unique across entire model
- [ ] Correlated numbering (cells ↔ surfaces ↔ materials)

### Cross-References
- [ ] All surfaces referenced in cells are defined
- [ ] All materials referenced in cells are defined
- [ ] All universes referenced in fills are defined
- [ ] Universe hierarchy is valid (child before parent)
- [ ] No circular universe references

### Specifications
- [ ] Volumes specified for important cells
- [ ] Importance specified for all cells (imp:n)
- [ ] Particle termination boundary exists (imp:n=0)
- [ ] Density signs correct (negative=g/cm³, positive=atoms/barn-cm)

### Comments
- [ ] Inline comments on all non-trivial cards
- [ ] Section headers for major components
- [ ] Units specified in comments
- [ ] Physical descriptions (not just numbers)
- [ ] Critical notes documented

### Materials
- [ ] Thermal scattering (MT cards) for graphite, water, etc.
- [ ] Temperature-appropriate libraries
- [ ] Isotopic vs. natural element selection documented
- [ ] Density values and units commented

### Quality
- [ ] Consistent formatting (alignment, spacing)
- [ ] No orphaned cards (references to non-existent entities)
- [ ] Reasonable physical values (check densities, dimensions)
- [ ] Model purpose and assumptions documented

## COMMON PITFALLS AND FIXES

### Pitfall 1: Unstructured Numbering

**WRONG**:
```mcnp
c Random sequential numbers
1 1 -10.2  -1  imp:n=1  $ Some cell
2 2 -8.0   -2  imp:n=1  $ Another cell
17 1 -10.2  -17  imp:n=1  $ Wait, what?
```

**RIGHT**:
```mcnp
c Systematic: 100-series = fuel, 200-series = clad, 300-series = coolant
101 1 -10.2  -101  imp:n=1  $ Fuel pin 1
102 1 -10.2  -102  imp:n=1  $ Fuel pin 2
201 2 -6.5   -201  imp:n=1  $ Clad pin 1
202 2 -6.5   -202  imp:n=1  $ Clad pin 2
301 3 -1.0   -301  imp:n=1  $ Coolant pin 1
```

### Pitfall 2: Missing Comments

**WRONG**:
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522
```

**RIGHT**:
```mcnp
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel (UO2, 19.96% enriched)
```

### Pitfall 3: Undefined References

**WRONG**:
```mcnp
c Cell references surface 100, but surface 100 not defined
1 1 -10.2  -100  imp:n=1
c
c Surfaces
99 cz  0.5
101 cz  0.6  $ Forgot surface 100!
```

**RIGHT**:
```mcnp
c Cell references surface 100
1 1 -10.2  -100  imp:n=1
c
c Surfaces
100 cz  0.5  $ ← Surface 100 defined
101 cz  0.6
```

### Pitfall 4: Circular Universe References

**WRONG**:
```mcnp
c Universe 100 fills universe 200
100 0  -100  u=100 fill=200
c
c Universe 200 fills universe 100  ← CIRCULAR!
200 0  -200  u=200 fill=100
```

**RIGHT**:
```mcnp
c Universe 100 (child, defined first)
100 1 -10.2  -100  u=100  $ Fuel pin
c
c Universe 200 (parent, fills with child)
200 0  -200  u=200 fill=100  $ Assembly fills with pins
c
c Global cell fills with assembly
999 0  -999  fill=200
```

### Pitfall 5: Volume on Lattice Cell

**WRONG**:
```mcnp
c Volume specification ignored for lattice cells
100 0  -100  u=200 lat=1  vol=1000  fill=-8:8 -8:8 0:0  $ vol ignored!
```

**RIGHT**:
```mcnp
c Volume specified on individual cells WITHIN universe
10 1 -10.2  -10  u=100  vol=50.3  $ Fuel pin volume
c
c Lattice cell has no volume specification
100 0  -100  u=200 lat=1  fill=-8:8 -8:8 0:0  $ Lattice container
```

### Pitfall 6: Material-Density Mismatch

**WRONG**:
```mcnp
m1  $ Atom fractions
    1001.70c  2.0
    8016.70c  1.0
c
c Using negative density with atom fractions → ERROR
1 1 -1.0  -1  imp:n=1  $ Negative density requires MASS fractions!
```

**RIGHT (Option 1: Total atom density)**:
```mcnp
m1
    1001.70c  0.0667  $ Atom fractions sum to 1.0
    8016.70c  0.0333
c
c Positive density in cell
1 1 0.1000  -1  imp:n=1  $ Total atom density (atoms/barn-cm)
```

**RIGHT (Option 2: Mass fractions)**:
```mcnp
m1
    1001.70c  -0.112  $ Mass fractions (negative)
    8016.70c  -0.888
c
c Negative density in cell
1 1 -1.0  -1  imp:n=1  $ Mass density (g/cm³)
```

## REFERENCE FILES

Detailed examples and templates:

- **numbering_schemes_reference.md** - Comprehensive numbering patterns
- **input_organization_guide.md** - Structure and formatting standards
- **cross_reference_validation.md** - Validation rules and checks
- **comment_conventions_guide.md** - Professional commenting practices
- **example_inputs/** - Complete annotated examples

---

## END OF SKILL REFINEMENT CONTENT
```

**END OF SECTION 2.1**

---

### 2.2 Create numbering_schemes_reference.md

**File**: `.claude/skills/mcnp-input-builder/numbering_schemes_reference.md`

```markdown
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
```

**END OF SECTION 2.2**

---

## PART 3: VALIDATION & TESTING

### Test 1: User Asks About Numbering

**Query**: "How should I number cells in a complex reactor model with multiple assemblies?"

**Expected Response**:
1. ✅ Explain hierarchical encoding (XYZSS pattern)
2. ✅ Provide functional subsystem ranges
3. ✅ Give concrete example (PWR or HTGR)
4. ✅ Reference numbering_schemes_reference.md
5. ✅ Show validation checklist
6. ✅ Warn about common pitfalls

### Test 2: User Asks About File Structure

**Query**: "What's the proper way to organize an MCNP input file?"

**Expected Response**:
1. ✅ Explain three-block structure
2. ✅ Show section dividers and headers
3. ✅ Demonstrate inline comments ($ syntax)
4. ✅ Provide complete example
5. ✅ Reference input_organization_guide.md

### Test 3: User Asks About Validation

**Query**: "How do I check my input file for errors before running MCNP?"

**Expected Response**:
1. ✅ Cross-reference validation rules
2. ✅ Universe hierarchy checks
3. ✅ Material-density correlation
4. ✅ Provide validation checklist
5. ✅ Suggest automated tools (if available)

---

## PART 4: IMPLEMENTATION CHECKLIST

### Files to Create/Modify:

- [ ] `.claude/skills/mcnp-input-builder/SKILL.md` (UPDATE - add ~1500 lines)
- [ ] `.claude/skills/mcnp-input-builder/numbering_schemes_reference.md` (NEW - ~800 lines)
- [ ] `.claude/skills/mcnp-input-builder/input_organization_guide.md` (NEW - ~600 lines)
- [ ] `.claude/skills/mcnp-input-builder/cross_reference_validation.md` (NEW - ~400 lines)
- [ ] `.claude/skills/mcnp-input-builder/comment_conventions_guide.md` (NEW - ~300 lines)
- [ ] `.claude/skills/mcnp-input-builder/example_inputs/annotated_pwr_input.i` (NEW - full example)
- [ ] `.claude/skills/mcnp-input-builder/example_inputs/annotated_htgr_input.i` (NEW - full example)

### Content Creation Status:

- [x] Section 2.1: SKILL.md major update (complete content provided)
- [x] Section 2.2: numbering_schemes_reference.md (complete content provided)
- [ ] Section 2.3: input_organization_guide.md (outline provided, full content TBD)
- [ ] Section 2.4: cross_reference_validation.md (outline provided, full content TBD)
- [ ] Section 2.5: comment_conventions_guide.md (outline provided, full content TBD)
- [ ] Section 2.6: Example input files (TBD)

---

## PART 5: SUCCESS CRITERIA

**Updated skill must enable users to**:

1. ✅ Apply systematic numbering schemes (hierarchical encoding)
2. ✅ Organize inputs with professional structure (three blocks, dividers, comments)
3. ✅ Validate cross-references (all entities exist)
4. ✅ Specify volumes appropriately (when and where)
5. ✅ Set importance correctly (variance reduction prep)
6. ✅ Comment comprehensively (inline + block comments)
7. ✅ Build maintainable files (1000+ cells, debuggable)

**Quality indicators**:

- ✅ User can identify component from cell number alone
- ✅ User avoids all numbering conflicts
- ✅ User creates well-organized, readable inputs
- ✅ User validates cross-references before MCNP run
- ✅ User applies professional comment conventions

---

## PART 6: INTEGRATION WITH OTHER SKILLS

**mcnp-input-builder** works with:

- **mcnp-lattice-builder**: Provides universe numbers for lattice fills
- **mcnp-geometry-builder**: Provides surface numbers for cell definitions
- **mcnp-material-builder**: Provides material numbers for cell specifications
- **mcnp-input-validator**: Uses validation rules from this skill
- **mcnp-cross-reference-checker**: Implements cross-reference validation

**Key integration points**:

1. Numbering schemes must be compatible across skills
2. Cross-reference validation must check all entity types
3. Comment conventions should be consistent
4. Example inputs should demonstrate integration

---

## EXECUTION PRIORITY

**Priority**: 🟡 **MEDIUM** (Phase 2)

**Rationale**: While important, this skill depends on:
- mcnp-lattice-builder (provides universes)
- mcnp-material-builder (provides materials)
- mcnp-geometry-builder (provides surfaces)

**Recommendation**: Complete Phase 1 skills FIRST, then implement this in Phase 2.

---

## ESTIMATED EFFORT

**Content creation**: ~6 hours
- SKILL.md update: 2 hours
- Reference files (4 new): 3 hours
- Example inputs (2 files): 1 hour

**Testing**: ~1 hour
- Test queries with revised skill
- Verify reference file accuracy

**Total**: ~7 hours

---

## END OF REFINEMENT PLAN

**Next Steps**:
1. Complete Phase 1 skills (lattice, material, validator, geometry)
2. Return to this plan for Phase 2 implementation
3. Create all reference files listed
4. Develop example inputs
5. Test with user queries
6. Integrate with other skills

**Document Status**: ✅ **COMPLETE** - Ready for Phase 2 execution
