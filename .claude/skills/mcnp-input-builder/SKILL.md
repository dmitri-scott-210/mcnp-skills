---
name: mcnp-input-builder
description: "Create MCNP6 input files from scratch with proper three-block structure, formatting conventions, and card organization for fixed-source and criticality problems"
version: "2.0.0"
---

# MCNP Input Builder

## Overview

The MCNP Input Builder skill guides users in creating properly structured MCNP6 input files with correct formatting, card organization, and syntax conventions. MCNP inputs follow a strict three-block structure (cell cards, surface cards, data cards) separated by blank lines. This skill covers the essential formatting rules, common card types, and organizational best practices needed to create working input files.

Understanding proper input structure is fundamental to MCNP usage. The three-block format must be followed exactly: cell cards define spatial regions and materials, surface cards define geometric boundaries, and data cards specify physics, sources, tallies, and problem control. Errors in formatting, continuation rules, or card order will prevent MCNP from running.

This skill provides templates, decision trees, and use cases for common problem types including fixed-source calculations, criticality problems, shielding analyses, and detector simulations. It emphasizes proper formatting to avoid the most common "fatal" and "bad trouble" errors that terminate simulations.

## When to Use This Skill

- Creating a new MCNP input file from scratch for any problem type
- Understanding the three-block input structure (cells, surfaces, data)
- Fixing input formatting errors (missing blank lines, tabs, card continuation)
- Organizing complex multi-region simulations with proper structure
- Converting inputs between MCNP versions or from other codes
- Troubleshooting "bad trouble" syntax errors reported by MCNP
- Learning proper card formatting and continuation rules
- Setting up basic templates for common problem types (fixed-source, criticality)

## Decision Tree

```
START: Need to create MCNP input file
  |
  +--> Have existing geometry/materials?
       |
       +--[YES]--> Modify existing input (use mcnp-input-editor skill)
       |
       +--[NO]---> Build from scratch (use this skill)
                   |
                   +--> What problem type?
                        |
                        +--[Fixed Source]---> Three-block structure
                        |                     ├─> Template: basic_fixed_source_template.i
                        |                     ├─> Add: MODE, M, SDEF, F, NPS
                        |                     └─> Validate: mcnp-input-validator
                        |
                        +--[Criticality]-----> KCODE structure
                        |                     ├─> Template: kcode_criticality_template.i
                        |                     ├─> Add: MODE N, KCODE, KSRC, fissile M
                        |                     └─> Validate: mcnp-geometry-checker
                        |
                        +--[Shielding]-------> Multi-region + VR
                        |                     ├─> Template: shielding_template.i
                        |                     ├─> Add: IMP cards, possibly WWE/WWN
                        |                     └─> Check: penetration depth adequate
                        |
                        +--[Detector]--------> Source + detector tally
                                              ├─> Template: detector_template.i
                                              ├─> Add: F4/F5 tallies, energy bins
                                              └─> Validate: source in correct cell
```

## Quick Reference

### Essential Input Structure
```
Title Card (one line)
c === Optional comments ===

c === BLOCK 1: Cell Cards ===
j  m  d  geom  params         $ j=cell#, m=mat#, d=density
...
<BLANK LINE>

c === BLOCK 2: Surface Cards ===
j  type  parameters            $ j=surf#, type=SO/PX/CY/etc.
...
<BLANK LINE>

c === BLOCK 3: Data Cards ===
MODE  N                        $ Must be first data card
M1   ...                       $ Materials
SDEF ...                       $ Source (or KCODE)
F4:N ...                       $ Tallies
NPS  1000000                   $ Termination
<BLANK LINE>
```

### Essential Cards Reference

| Card | Purpose | Example | Notes |
|------|---------|---------|-------|
| **Cell** | Define region | `1 1 -1.0 -10 IMP:N=1` | j m d geom params |
| **Surface** | Boundary | `10 SO 5.0` | j type params |
| **MODE** | Particles | `MODE N P` | Must be first data card |
| **M** | Material | `M1 1001 2 8016 1` | ZAID pairs |
| **SDEF** | Fixed source | `SDEF POS=0 0 0 ERG=14.1` | Position, energy |
| **KCODE** | Criticality | `KCODE 10000 1.0 50 150` | Nsrc k0 Nskip Ncyc |
| **F4** | Cell flux | `F4:N 1 2 3` | Volume-averaged |
| **F5** | Point detector | `F5:N 10 0 0 0.5` | x y z R |
| **IMP** | Importance | `IMP:N 1 1 0` | Per cell or in cell card |
| **NPS** | Histories | `NPS 1000000` | Problem termination |

### Formatting Rules Summary

- **Line length:** ≤128 characters (recommend ≤80 for readability)
- **Blank lines:** Required between blocks and at end of file
- **Continuation:** 5+ leading spaces, `&` at line end, or repeat card name
- **Comments:** `C` in columns 1-5 + space (full line) or `$` (inline)
- **Tabs:** NEVER use tabs (always use spaces)
- **Units:** cm (length), MeV (energy), shakes (time), g/cm³ or atoms/(barn·cm) (density)

## Use Cases

### Use Case 1: Simple Fixed-Source Problem

**Scenario:** Calculate neutron flux in water sphere from 14.1 MeV point source at center.

**Goal:** Basic three-block input with source, material, and tally.

**Implementation:**
```
Simple Water Sphere - 14.1 MeV Neutron Source
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0      -1           IMP:N=1  VOL=4188.79  $ Water sphere
2    0            1            IMP:N=0               $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0                                       $ Sphere R=10 cm

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Material ---
M1   1001  2   8016  1                              $ H2O
MT1  LWTR.01T                                        $ Light water S(α,β)
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1                            $ 14.1 MeV point source
c --- Tally ---
F4:N  1                                              $ Volume flux in cell 1
E4    0.01 0.1 1 10 14 15                          $ Energy bins (MeV)
c --- Termination ---
NPS   1000000
PRINT
```

**Key Points:**
- Three blocks clearly separated by blank lines
- MODE N must be first data card
- MT1 for thermal scattering in water
- VOL specified in cell card for F4 normalization
- IMP:N=0 in graveyard (cell 2) kills particles
- Energy bins (E4) focused around source energy
- Blank line at end of file required

### Use Case 2: Multi-Material Shielding

**Scenario:** Point neutron source with steel, polyethylene, and lead shielding layers. Calculate flux in each layer.

**Goal:** Multi-region geometry with realistic material densities.

**Implementation:**
```
Multi-Layer Shielding: Steel/Poly/Lead
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0         -1              IMP:N=1              $ Source void
10   1  -7.86   1  -2          IMP:N=1              $ Steel (10 cm)
20   2  -0.94   2  -3          IMP:N=1              $ Poly (20 cm)
30   3  -11.34  3  -4          IMP:N=1              $ Lead (15 cm)
40   0          4  -5          IMP:N=1              $ Detector
999  0          5              IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0                                      $ Source boundary
2    SO   20.0                                      $ Steel outer
3    SO   40.0                                      $ Poly outer
4    SO   55.0                                      $ Lead outer
5    SO   60.0                                      $ Detector outer

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Materials ---
M1   26000  -0.695   24000  -0.190   28000  -0.095  $ Steel (Fe/Cr/Ni)
     25055  -0.020
M2   1001   -0.143   6000   -0.857                  $ Polyethylene (CH2)
MT2  POLY.01T                                        $ S(α,β) for poly
M3   82000  1.0                                      $ Lead (natural)
c --- Source ---
SDEF  POS=0 0 0  ERG=D1
SP1   -3  0.8  2.5                                   $ Watt fission spectrum
c --- Tallies ---
F4:N  10 20 30 40                                    $ Flux in all layers
E4    0.01 0.1 1 10                                  $ Energy bins
c --- Termination ---
NPS   10000000
CTME  120                                            $ 120 min time limit
PRINT
```

**Key Points:**
- Multiple materials with realistic densities (g/cm³)
- MT2 specifies thermal scattering for polyethylene
- Watt spectrum source (fission-like) using SP1 card
- Single F4 tally for multiple cells (10, 20, 30, 40)
- CTME sets 2-hour run time limit
- Energy bins span thermal to fast neutrons

### Use Case 3: Criticality (KCODE) Problem

**Scenario:** Bare sphere of Pu-239 metal, calculate k-effective.

**Goal:** KCODE criticality calculation with proper source initialization.

**Implementation:**
```
Bare Pu-239 Metal Sphere - Criticality
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -19.816   -1           IMP:N=1              $ Pu-239 metal
2    0            1            IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   6.385                                     $ Critical radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Material ---
M1   94239  1.0                                     $ Pu-239 (pure)
c --- KCODE Parameters ---
KCODE  10000  1.0  50  150                          $ Nsrc k0 Nskip Ncyc
c      Nsrc=10000 histories per cycle
c      k0=1.0 initial guess
c      Nskip=50 inactive cycles (skip for convergence)
c      Ncyc=150 total cycles (100 active)
KSRC   0 0 0                                        $ Starting source point
c --- Termination ---
c (KCODE controls termination, no NPS needed)
PRINT
```

**Key Points:**
- KCODE replaces SDEF and NPS for criticality problems
- KSRC provides initial source positions (MCNP will iterate)
- KCODE format: `Nsrc k_initial Nskip Ntotal`
  - 10,000 histories per cycle
  - 1.0 = initial k guess
  - 50 = inactive cycles (discarded for convergence)
  - 150 = total cycles (100 active for statistics)
- No explicit NPS card needed (cycles control termination)
- Use mcnp-criticality-analyzer skill to interpret output

### Use Case 4: Point Detector (F5 Tally)

**Scenario:** Void geometry with point source and detector at distance. Calculate flux at detector location.

**Goal:** Demonstrate F5 point detector tally (next-event estimator).

**Implementation:**
```
Point Detector Example - F5 Tally
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0         -1              IMP:N=1              $ Problem void
2    0         1               IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   200.0                                     $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Source ---
SDEF  POS=0 0 0  ERG=1.0                            $ 1 MeV at origin
c --- Point Detector Tally ---
F5:N  100 0 0  0.5                                  $ Detector at x=100
c     ^x  ^y ^z ^R (R = exclusion sphere radius)
E5    0.1 0.5 0.9 1.0 1.1 1.5 2.0                   $ Energy bins
c --- Termination ---
NPS   1000000
PRINT
```

**Key Points:**
- F5 format: `F5:N x y z R` where (x,y,z) is location, R is exclusion radius
- R = exclusion sphere (particles within R are ignored)
- F5 gives flux at a point (not volume-averaged like F4)
- Void geometry simplifies (no scattering, first-flight calculation)
- Energy bins around source energy (1 MeV)
- Use F5 for detectors, F4 for volume-averaged flux

## Integration with Other Skills

### Typical Workflow
1. **mcnp-input-builder** (this skill) → Create basic three-block structure
2. **mcnp-geometry-builder** → Add detailed cells and surfaces
3. **mcnp-material-builder** → Add material definitions (M/MT cards)
4. **mcnp-source-builder** → Add source specification (SDEF/KCODE)
5. **mcnp-tally-builder** → Add tallies and energy bins
6. **mcnp-physics-builder** → Add physics options (PHYS, CUT)
7. **mcnp-input-validator** → Validate syntax before running

### Complementary Skills
- **mcnp-geometry-builder:** Detailed geometry construction (cells, surfaces, Boolean logic)
- **mcnp-material-builder:** Material cards (M, MT, MX), ZAID format, densities
- **mcnp-source-builder:** Source definitions (SDEF, KCODE, distributions)
- **mcnp-tally-builder:** Tally specification (F1-F8, energy bins, multipliers)
- **mcnp-input-editor:** Modify existing inputs (systematic changes)
- **mcnp-input-validator:** Pre-run validation (three-block check, blank lines, MODE card)

### Example Complete Workflow
```
Project Goal: Shielding analysis for neutron source

Step 1: mcnp-input-builder - Create basic structure (this skill)
Step 2: mcnp-geometry-builder - Define shield layers and geometry
Step 3: mcnp-material-builder - Add concrete, steel, poly materials
Step 4: mcnp-source-builder - Define fission or point source
Step 5: mcnp-tally-builder - Add F4 flux tallies with energy bins
Step 6: mcnp-variance-reducer - Add importance cards for deep penetration
Step 7: mcnp-input-validator - Validate before running
Result: Working input file ready for MCNP execution
```

## References

### Detailed Documentation
See **root skill directory** for additional comprehensive information:

- **Input Format Specifications** (`input_format_specifications.md`)
  - Card continuation rules (5-space, &, vertical format)
  - Comment syntax and best practices
  - Input shortcuts (R, I, M, J, LOG, ILOG)
  - Numerical limitations (cell/surface/material ranges)
  - Default units (cm, MeV, shakes, densities)
  - Message block format and termination

- **Particle Designators Reference** (`particle_designators_reference.md`)
  - Complete 37-particle type table
  - Particle masses, charges, lifetimes, cutoffs
  - Common particle types (:N, :P, :E, :|, :H)
  - Coupled transport (N-P, N-P-E)
  - Energy cutoffs by particle type

- **Error Catalog** (`error_catalog.md`)
  - Error message hierarchy (FATAL, BAD TROUBLE, WARNING, COMMENT)
  - 7 common formatting errors with solutions
  - Geometry errors (lost particles, gaps, overlaps)
  - Material and data card errors
  - Validation checklist

- **Advanced Techniques** (`advanced_techniques.md`)
  - Programmatic input generation (Python scripts)
  - Input file modularization (READ command, multi-file)
  - Restart capabilities (CONTINUE, runtpe.h5)
  - Version compatibility (MCNP5 vs MCNP6)
  - Large simulation best practices

### Templates and Examples
Example files and templates:

- **Templates** (`templates/`)
  - basic_fixed_source_template.i
  - kcode_criticality_template.i
  - shielding_template.i
  - detector_template.i
  - README.md (template usage guide)

- **Example Inputs** (`example_inputs/`)
  - 10 validated examples (basic → advanced)
  - Each with description file
  - Source files from basic_examples/ and reactor-model_examples/

### Automation Tools
See `scripts/` subdirectory:

- **mcnp_input_generator.py** - Template-based input generation
- **validate_input_structure.py** - Pre-MCNP validation script
- **README.md** - Script usage documentation

### External Documentation
- MCNP6 User Manual, Chapter 3: Introduction to MCNP Usage
- MCNP6 User Manual, Chapter 4: Description of MCNP6 Input
- MCNP6 User Manual, Chapter 10: Examples

## Best Practices

1. **Always Use Three-Block Structure**
   - Block 1: Cell cards (geometry and materials)
   - Block 2: Surface cards (geometric boundaries)
   - Block 3: Data cards (MODE first, NPS/CTME last)
   - Separate blocks with blank lines, end file with blank line

2. **Use Spaces, Never Tabs**
   - MCNP treats tabs as single spaces (breaks alignment)
   - Configure editor to convert tabs to spaces
   - Use "Insert spaces for tabs" option

3. **Organize with Comment Headers**
   - Use visual separators (`c ===...`)
   - Group related cards with descriptive comments
   - Document non-obvious choices (e.g., why specific density used)

4. **Follow Logical Card Order**
   - MODE → Materials → Source → Tallies → VR → Physics → Output → Termination
   - Keep related cards together (F4, E4, FM4 sequential)
   - Document rationale for unusual ordering

5. **Always Include Particle Designators**
   - Use `:N`, `:P`, `:E` explicitly on all relevant cards
   - Never rely on defaults (clarity over brevity)
   - Example: `F4:N` not `F4`, `IMP:N` not `IMP`

6. **Validate Before Running**
   - Check three-block structure
   - Verify blank lines present
   - Confirm MODE is first data card
   - Plot geometry (mcnp6 inp=file.i ip)
   - Use mcnp-input-validator skill

7. **Use Templates for Common Problems**
   - Start with basic_fixed_source_template.i or similar
   - Modify template rather than starting from blank
   - Maintain library of working templates

8. **Document Inline**
   - Use `$` for inline comments on every important card
   - Explain parameter choices (e.g., `$ 120 min time limit`)
   - Include units when ambiguous (e.g., `$ R=10 cm`)

9. **Build Incrementally**
   - Start simple (sphere, single material)
   - Add complexity gradually (multi-region, multiple materials)
   - Validate at each step (plot geometry, check for errors)

10. **Keep Backups of Working Versions**
    - Version control inputs (input_v1.i, input_v2.i, etc.)
    - Document changes in comments
    - Ability to revert if errors introduced

---

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

**End of MCNP Input Builder Skill**
