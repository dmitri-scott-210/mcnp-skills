# MCNP Comment Conventions Guide
## Professional Documentation Practices

**Purpose**: Comprehensive guide to commenting MCNP input files for maximum clarity, maintainability, and knowledge transfer.

---

## OVERVIEW

**Well-commented MCNP files**:
- Are self-documenting (minimal external documentation needed)
- Can be understood months/years later
- Enable knowledge transfer to new users
- Facilitate debugging and modification
- Document assumptions and limitations

**Two comment types in MCNP**:
1. **Block comments** (`c` in columns 1-5) - Full-line comments
2. **Inline comments** (`$` anywhere) - End-of-line comments

---

## COMMENT SYNTAX

### Block Comments (c syntax)

**Format**: `c` in columns 1-5, followed by space, then comment text

```mcnp
c This is a block comment
C This is also valid (uppercase C)
c     This comment has extra spaces (okay)
     c This is NOT valid (c not in columns 1-5)
```

**Use cases**:
- File headers
- Section dividers
- Multi-line explanations
- Subsection descriptions
- Blank separators

### Inline Comments ($ syntax)

**Format**: `$` anywhere on line, followed by comment text

```mcnp
1  1  -10.2  -100  imp:n=1  $ This is an inline comment
100  so  5.0  $ Sphere radius = 5.0 cm
m1  92235.70c  0.045  $ U-235 enrichment
```

**Use cases**:
- Cell descriptions
- Surface dimensions
- Material compositions
- Parameter explanations
- Units and values

---

## FILE HEADER DOCUMENTATION

### Comprehensive Header Template

```mcnp
c ========================================
c [MODEL NAME]
c ========================================
c
c Description: [One-line summary of what model represents]
c Purpose: [Why this model was created - physics goals]
c
c Version: [Version number or date]
c Author: [Name/Organization]
c Date Created: [YYYY-MM-DD]
c Last Modified: [YYYY-MM-DD]
c Modified By: [Name]
c
c GEOMETRY DESCRIPTION:
c   [High-level description of physical system]
c   - Key component 1
c   - Key component 2
c   - Overall dimensions and configuration
c
c NUMBERING SCHEME:
c   Cells:     [Pattern description, e.g., XYZSS]
c   Surfaces:  [Pattern description]
c   Materials: [Pattern description]
c   Universes: [Pattern description with component type encoding]
c
c RESERVED RANGES:
c   [Cell number ranges for different subsystems]
c   [Surface number ranges]
c   [Material number ranges]
c
c UNITS:
c   Lengths: cm
c   Densities: g/cm³ (negative) or atoms/barn-cm (positive)
c   Energies: MeV
c   Time: shakes (1 shake = 10^-8 s)
c   Temperature: K (in cross-section library)
c
c MATERIALS:
c   [Brief description of key materials]
c   m1: [Material name and key properties]
c   m2: [Material name and key properties]
c
c PHYSICS SETTINGS:
c   Mode: [Particle types]
c   Cross sections: [Library and temperature]
c   [Other key physics options]
c
c CALCULATION TYPE:
c   [Fixed source or criticality]
c   [Source description or KCODE parameters]
c   [Tally summary]
c   [Histories/cycles]
c
c ASSUMPTIONS:
c   1. [Key assumption 1]
c   2. [Key assumption 2]
c   3. [Key assumption 3]
c
c LIMITATIONS:
c   1. [Known limitation 1]
c   2. [Known limitation 2]
c
c REFERENCE DOCUMENTS:
c   - [Document 1 name and ID]
c   - [Document 2 name and ID]
c   - [Drawings, specifications, etc.]
c
c VALIDATION STATUS:
c   - Geometry plotted: [Date, tool]
c   - Cross-references checked: [Date, method]
c   - Physics validated: [Benchmark, comparison]
c
c REVISION HISTORY:
c   v1.0 [2024-01-15]: Initial model
c   v1.1 [2024-02-20]: Added variance reduction
c   v2.0 [2024-03-22]: Updated cross sections to ENDF/B-VIII.0
c
c ========================================
```

### Minimal Header (for simple problems)

```mcnp
c ========================================
c [MODEL NAME]
c ========================================
c
c Description: [One-line summary]
c Author: [Name]
c Date: [YYYY-MM-DD]
c
c Geometry: [Brief description]
c Materials: [List of materials]
c Calculation: [Fixed source or criticality, brief params]
c
c ========================================
```

---

## SECTION DIVIDERS

### Heavy Dividers (Major Sections)

```mcnp
c ========================================
c CELL BLOCK
c ========================================
```

```mcnp
c ========================================
c SURFACE BLOCK
c ========================================
```

```mcnp
c ========================================
c DATA BLOCK
c ========================================
```

**Use for**:
- Block transitions (cells, surfaces, data)
- Major component groups in complex models
- Top-level organization

### Medium Dividers (Subsections)

```mcnp
c --- FUEL ASSEMBLIES ---
```

```mcnp
c --- CONTROL RODS ---
```

```mcnp
c --- REFLECTOR ---
```

**Use for**:
- Component groups within blocks
- Functional subsystems
- Material categories

### Light Dividers (Component Groups)

```mcnp
c Assembly A-01: Standard fuel assembly
```

```mcnp
c TRISO particle surfaces - Capsule 1, Stack 1, Compact 1
```

**Use for**:
- Specific components
- Related card groups
- Individual assemblies/regions

---

## CELL CARD COMMENTS

### Inline Comments on Every Cell

```mcnp
c Good: Every cell has descriptive comment
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel (UO2, 19.96% enriched)
91102 9090 -1.100   91111 -91112  u=1114        $ Buffer (porous carbon)
91103 9091 -1.904   91112 -91113  u=1114        $ IPyC (inner pyrolytic carbon)
91104 9092 -3.205   91113 -91114  u=1114        $ SiC (silicon carbide barrier)
91105 9093 -1.911   91114 -91115  u=1114        $ OPyC (outer pyrolytic carbon)
```

**What to include**:
- Component name (Kernel, Buffer, etc.)
- Material type or phase (UO2, porous carbon, etc.)
- Key properties (enrichment, density type, etc.)
- Function or role (barrier, structural, etc.)

### Block Comments for Complex Sections

```mcnp
c CAPSULE 1, STACK 1, COMPACT 1 - TRISO PARTICLES
c
c Five-layer TRISO particle structure (u=1114):
c   Layer 1: Kernel (UO2, 19.96% enriched, 350 μm diameter)
c   Layer 2: Buffer (porous carbon, 100 μm thick)
c   Layer 3: IPyC (inner pyrolytic carbon, 40 μm thick)
c   Layer 4: SiC (silicon carbide, 35 μm thick)
c   Layer 5: OPyC (outer pyrolytic carbon, 40 μm thick)
c
c Total particle diameter: ~785 μm
c
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel
91102 9090 -1.100   91111 -91112  u=1114        $ Buffer
[...]
```

**Use before**:
- Complex multi-component systems
- Unusual geometry configurations
- Critical modeling decisions
- Non-obvious universe hierarchies

### Lattice Fill Comments

```mcnp
c Particle lattice (u=1116) - 15×15 hexagonal array
c Pattern: 1114=particle, 1115=matrix (random distribution, 40% packing)
c
91108 0  -91117  u=1116  lat=1  fill=-7:7 -7:7 0:0  $ Lattice container
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1115 1115 1114 1114 1114 1114 1114 1115 1115 1115 1115 1115
     [... remaining rows ...]
     $    ↑ Center row (maximum particle density)
```

**Include**:
- Array dimensions (15×15)
- Universe IDs and what they represent
- Packing fraction or pattern description
- Special features (center, edges, symmetry)

---

## SURFACE CARD COMMENTS

### Inline Comments with Dimensions

```mcnp
c Good: Dimensions and units in comments
91111 so   0.017485  $ Kernel radius (174.85 μm)
91112 so   0.027905  $ Buffer outer radius (279.05 μm)
97060 c/z  25.337  -25.337  1.51913  $ Capsule 1 holder, center at (25.337, -25.337)
98000 pz   -2.54000  $ Bottom boundary (z = -2.54 cm)
```

**Include**:
- Physical dimension with units
- What the surface bounds (outer radius, interface, etc.)
- Special features (off-axis center, calculated value, etc.)

### Calculated vs. Specified Values

```mcnp
c Compact boundaries (calculated from stack height)
98005 pz   17.81810  $ Bottom of Compact 1 (specified)
98051 pz   20.35810  $ Top of Compact 1 (calculated: 17.818 + 2.54)
98006 pz   22.89810  $ Bottom of Compact 2 (calculated: 20.358 + 2.54)
```

**Document**:
- Source of value (measured, calculated, estimated)
- Calculation method if derived
- Tolerance or uncertainty if critical

### Surface Type Grouping

```mcnp
c Concentric spherical shells (SO surfaces at origin)
91111 so  0.017485  $ Kernel
91112 so  0.027905  $ Buffer outer
91113 so  0.031785  $ IPyC outer
91114 so  0.035375  $ SiC outer
91115 so  0.039305  $ OPyC outer
c
c Off-axis cylinders centered at (25.337, -25.337) mm
97060 c/z  25.337  -25.337  1.51913  $ Compact holder
97061 c/z  25.337  -25.337  1.58750  $ Gas gap
97062 c/z  25.337  -25.337  1.62179  $ Inner capsule wall
c
c Axial segmentation planes (PZ surfaces)
98000 pz   -2.54000  $ Bottom boundary
98001 pz   13.65758  $ Bottom of Stack 1
98005 pz   17.81810  $ Bottom of Compact 1
```

**Group by**:
- Surface type (spheres, cylinders, planes)
- Geometric relationship (concentric, parallel)
- Component association

---

## MATERIAL CARD COMMENTS

### Header Comment Before Material

```mcnp
c Material m9111: UCO kernel, 19.96% enriched, density=10.924 g/cm3
c Location: Capsule 1, Stack 1, Compact 1
c Formula: UC₀.₃₂O₁.₃₆ (uranium carbide-oxide)
m9111
   92234.00c  3.34179E-03  $ U-234 (0.334% of U)
   92235.00c  1.99636E-01  $ U-235 (19.96% enrichment)
   92236.00c  1.93132E-04  $ U-236 (trace)
   92238.00c  7.96829E-01  $ U-238 (balance)
    6012.00c  0.3217217    $ C-12 (carbide component)
    6013.00c  0.0035783    $ C-13 (natural abundance)
    8016.00c  1.3613       $ O-16 (oxide component)
```

**Include before material**:
- Material ID and descriptive name
- Density value and units
- Location (if unique) or usage
- Chemical formula
- Temperature if non-standard

### Inline Comments on Isotopes

```mcnp
m1
   92234.70c  0.00030   $ U-234 (0.30% of uranium)
   92235.70c  0.03500   $ U-235 (3.5% enrichment) ← KEY ISOTOPE
   92238.70c  0.96470   $ U-238 (96.47%, balance)
    8016.70c  2.00000   $ O-16 (stoichiometric UO2)
```

**Include**:
- Isotope name and mass number
- Percentage or fraction
- Role (fissile, fertile, dominant, trace)
- Special notes (enrichment, balance, stoichiometry)

### Thermal Scattering Comments

```mcnp
m9091  $ IPyC (Inner Pyrolytic Carbon), density=1.912 g/cm3
    6012.00c  0.9890  $ C-12 (98.9%)
    6013.00c  0.0110  $ C-13 (1.1%, natural)
mt9091  grph.18t  $ ← CRITICAL: Graphite thermal scattering at 600K
                  $ Required for accurate low-energy neutron physics
```

**Include**:
- Why thermal scattering is needed
- Temperature (from library extension, e.g., .18t = 600K)
- Physics impact (accuracy, low-energy, etc.)

### Material Categories

```mcnp
c ========================================
c MATERIAL BLOCK
c ========================================
c
c --- FUEL MATERIALS ---
c
m1  $ UO2 fuel, 3.5% enriched
[...]
c
c --- STRUCTURAL MATERIALS ---
c
m10  $ Zircaloy-4 cladding
[...]
c
c --- MODERATORS/COOLANTS ---
c
m20  $ Light water at 300K
[...]
mt20  lwtr.01t  $ S(α,β) for H2O
c
c --- ABSORBERS ---
c
m30  $ Hafnium control rod
[...]
```

---

## DATA CARD COMMENTS

### Source Definition Comments

```mcnp
c ========================================
c SOURCE DEFINITION
c ========================================
c
c Fixed point source at origin
c Watt fission spectrum (U-235 thermal fission)
c Neutron energy: 0.1 to 20 MeV (99% of spectrum)
c
sdef  pos=0 0 0  erg=d1  par=n
sp1   -3  0.8  2.5  $ Watt spectrum parameters (a=0.8, b=2.5)
c
c OR for criticality:
c kcode  10000  1.0  50  150
c   10000 = histories per cycle
c   1.0   = initial k-effective guess
c   50    = inactive cycles (skip for convergence)
c   150   = total cycles (100 active for statistics)
c
c ksrc  0 0 0  $ Initial source position (center of core)
```

### Tally Comments

```mcnp
c ========================================
c TALLIES
c ========================================
c
c Tally 4: Cell flux in fuel regions
c Purpose: Normalize fission rate to power
c Units: neutrons/cm² per source particle
f4:n   10101 10102 10103  $ Fuel rods 1, 2, 3
e4     0.01 0.1 1 10      $ Energy bins: thermal, epithermal, fast
fc4    Fuel region flux for power normalization
c
c Tally 14: Cell flux in reflector
c Purpose: Assess neutron leakage and reflection
f14:n  30001 30002  $ Reflector blocks 1, 2
e14    0.01 0.1 1 10
fc14   Reflector flux
c
c Tally 24: Heating in structural components
c Purpose: Thermal analysis input
f6:n,p  40001 40002  $ Steel vessel walls (neutron + photon heating)
fc24    Heating rate in vessel walls
```

**Include**:
- Tally purpose (why this is being calculated)
- Units (with normalization info)
- Physical interpretation
- How results will be used

### Variance Reduction Comments

```mcnp
c ========================================
c VARIANCE REDUCTION
c ========================================
c
c Cell importance (geometric splitting)
c Strategy: Increase importance toward detector
c Factor of 2 per shield layer (exponential increase)
c
imp:n  1     $ Source region (reference)
      2     $ First shield layer (2× more particles)
      4     $ Second shield layer (4×)
      8     $ Third shield layer (8×)
      16    $ Fourth shield layer (16×)
      16    $ Detector region (maintain)
      0     $ Outside world (kill boundary)
c
c NOTE: Weight windows would be more efficient but require
c       iterative generation (WWG). Using importance for simplicity.
```

---

## SPECIAL SITUATIONS

### Commented-Out Cards

```mcnp
c Original source definition (replaced 2024-03-15)
c sdef  pos=0 0 0  erg=1.0  $ Old: monoenergetic 1 MeV
c
c New source definition (Watt spectrum for fission source)
sdef  pos=0 0 0  erg=d1
sp1   -3  0.8  2.5  $ Watt spectrum
```

**Include**:
- Why card was replaced
- Date of change
- Who made the change (in revision history)

### Debugging Comments

```mcnp
c DEBUG: Reduced particle count for geometry testing
c nps  100000000  $ Production run
nps   10000       $ DEBUG: Quick test (remove for production!)
```

**Mark clearly**:
- DEBUG or TEMP prefix
- What needs to be changed for production
- Warning if run with debug settings

### TODO Comments

```mcnp
c TODO: Update cross sections to ENDF/B-VIII.0 when available
c TODO: Add photon transport for heating calculation (MODE N P)
c TODO: Implement weight windows for deep penetration
```

---

## COMMENT ANTI-PATTERNS

### What NOT to Do

**DON'T: State the obvious**
```mcnp
c Bad: Comment just restates the card
1  1  -10.2  -1  imp:n=1  $ Cell 1, material 1, density -10.2
```

**DO: Provide physical context**
```mcnp
c Good: Comment adds physical meaning
1  1  -10.2  -1  imp:n=1  $ UO2 fuel pellet (3.5% enriched)
```

**DON'T: Use cryptic abbreviations**
```mcnp
c Bad: Unclear abbreviations
100  so  5.0  $ FP OR (cm)
```

**DO: Spell out or define abbreviations**
```mcnp
c Good: Clear terminology
100  so  5.0  $ Fuel pellet outer radius (5.0 cm)
```

**DON'T: Leave uncommented complex sections**
```mcnp
c Bad: No explanation for complex lattice
1 0 -1 u=10 lat=1 fill=-8:8 -8:8 0:0
  101 101 ... [289 universe IDs, no explanation]
```

**DO: Explain complex structures**
```mcnp
c Good: Document the pattern
c 17×17 PWR assembly lattice
c   101 = fuel rod
c   102 = guide tube
c   103 = instrumentation tube
c   Corners = guide tubes, center = instrumentation
1 0 -1 u=10 lat=1 fill=-8:8 -8:8 0:0
  102 101 101 ... [with clear pattern]
```

---

## COMMENT CHECKLIST

### File-Level Comments
- [ ] Comprehensive header with model description
- [ ] Numbering scheme documented
- [ ] Units specified
- [ ] Assumptions listed
- [ ] Limitations noted
- [ ] Reference documents cited
- [ ] Revision history maintained

### Block-Level Comments
- [ ] Heavy dividers for cell/surface/data blocks
- [ ] Medium dividers for major component groups
- [ ] Light dividers for subsections

### Card-Level Comments
- [ ] Inline comment on every non-trivial cell
- [ ] Surface dimensions with units
- [ ] Material densities and compositions explained
- [ ] Tally purposes documented
- [ ] Source definitions explained

### Special Comments
- [ ] Complex sections have block comments before
- [ ] Calculated values marked as such
- [ ] Changed/commented-out cards have explanations
- [ ] DEBUG/TODO items clearly marked

---

## SUMMARY

**Professional MCNP commenting practices**:
1. ✅ Comprehensive file header (model, assumptions, references)
2. ✅ Visual hierarchy (heavy/medium/light dividers)
3. ✅ Inline comments on all important cards
4. ✅ Block comments before complex sections
5. ✅ Physical context (not just restating syntax)
6. ✅ Units, dimensions, and calculations documented
7. ✅ Assumptions and limitations explicit
8. ✅ Revision history and change tracking

**Result**: Self-documenting input files that can be understood and modified years later without external documentation.

---

**END OF COMMENT CONVENTIONS GUIDE**
