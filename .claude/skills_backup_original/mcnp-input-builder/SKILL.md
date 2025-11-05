---
category: A
name: mcnp-input-builder
description: Build basic MCNP6 input file structure with proper formatting, card organization, and syntax conventions
activation_keywords:
  - input file
  - input structure
  - MCNP format
  - basic input
  - file structure
  - card format
  - input syntax
---

# MCNP Input Builder Skill

## Purpose
This skill guides users in creating properly structured MCNP6 input files with correct formatting, card organization, and syntax conventions. It covers the three-block structure, continuation rules, comment syntax, and common patterns for organizing complex inputs.

## When to Use This Skill
- Creating a new MCNP input file from scratch
- Understanding MCNP input file structure and conventions
- Fixing input formatting errors
- Organizing complex multi-part simulations
- Converting inputs between MCNP versions
- Troubleshooting "bad trouble" syntax errors

## Prerequisites
- Basic understanding of Monte Carlo particle transport
- Text editor for creating input files
- MCNP6 installation (for validation)

## Core Concepts

### Three-Block Input Structure
MCNP input files consist of three mandatory blocks separated by blank lines:

**Block 1: Message Block (Optional)**
- Optional title/comment text
- Anything before the first cell card
- Terminated by blank line

**Block 2: Cell Cards Block (Required)**
- Defines spatial regions (cells)
- One card per cell
- Format: `j  m  d  geom  params`
  - j = cell number (1-99999999)
  - m = material number (0 for void)
  - d = density (g/cm³ if positive, atom/b-cm if negative)
  - geom = geometric specification (Boolean expressions of surfaces)
  - params = cell parameters (IMP, VOL, TMP, etc.)
- Terminated by blank line

**Block 3: Surface and Data Cards Block (Required)**
- Surface cards define geometric boundaries
- Data cards specify physics, sources, tallies, materials, etc.
- Terminated by blank line (end of file)

### Basic Input Template
```
MCNP6 Input File Title - Problem Description
c =================================================================
c Block 1: Message Block (optional, descriptive text)
c =================================================================

c =================================================================
c Block 2: Cell Cards
c =================================================================
1    1  -1.0      -1           IMP:N=1       $ Water sphere
2    0            1  -2        IMP:N=1       $ Void shell
3    0            2            IMP:N=0       $ Graveyard

c =================================================================
c Block 3: Surface Cards
c =================================================================
1    SO   10.0                               $ Sphere R=10 cm
2    SO   20.0                               $ Sphere R=20 cm

c =================================================================
c Data Cards - Materials
c =================================================================
MODE  N
M1   1001  2  8016  1                        $ Water
c =================================================================
c Data Cards - Source
c =================================================================
SDEF  POS=0 0 0  ERG=14.1                    $ 14.1 MeV point source
c =================================================================
c Data Cards - Tallies
c =================================================================
F4:N  1                                       $ Flux in cell 1
c =================================================================
c Data Cards - Problem Termination
c =================================================================
NPS  1000000
```

### Card Continuation Rules

**Single-Line Card** (≤80 columns):
```
F4:N  1 2 3 4 5
```

**Multi-Line Continuation** (using ampersand `&`):
```
F4:N  1 2 3 4 5 6 7 8 9 10 &
      11 12 13 14 15 16 17
```

**Continuation Without `&`** (5 spaces + card name):
```
F4:N  1 2 3 4 5 6 7 8 9 10
      11 12 13 14 15 16 17
```

**Tab Key Limitation**:
- MCNP treats tabs as single spaces (NOT multiples)
- Use spaces for indentation to maintain alignment
- Recommendation: Configure editor to convert tabs to spaces

### Comment Syntax

**Full-Line Comment** (starts with `C` or `$`):
```
C This is a comment line
$ This is also a comment line
c Lowercase 'c' works too
```

**Inline Comment** (using `$`):
```
F4:N  1                                       $ Flux in cell 1
M1   1001  2  8016  1                        $ Water H2O
```

**Multi-Line Comments**:
```
C =================================================================
C  This is a comment block
C  Useful for organizing sections
C =================================================================
```

### Card Naming Conventions

**Cell Cards**:
- Integer identifiers: 1, 2, 3, ... 99999999
- No gaps required (can use 1, 5, 10, 100, etc.)
- Recommendation: Group by region (1-99 = core, 100-199 = reflector, etc.)

**Surface Cards**:
- Integer identifiers: 1, 2, 3, ... 99999999
- No gaps required
- Can use same numbers as cells (different namespace)
- Recommendation: Match numbering scheme (10-19 = inner surfaces, 20-29 = outer, etc.)

**Data Cards**:
- Alphabetic mnemonics (MODE, SDEF, F4, M1, etc.)
- Particle designators: `:N` (neutron), `:P` (photon), `:E` (electron)
- Numbered variants: F4, F14, F24 (tallies); M1, M2, M3 (materials)

### Input File Organization Best Practices

**1. Hierarchical Structure**:
```
Title Line
c =================================================================
c PROBLEM DESCRIPTION
c =================================================================
c  Problem type: Shielding calculation
c  Geometry: Concrete wall + void regions
c  Source: 14.1 MeV point source
c  Tallies: F4 flux, F6 heating
c  NPS: 10^7 histories
c =================================================================

c =================================================================
c CELL CARDS - Geometry Definition
c =================================================================
c --- Source Region ---
1    0         -1              IMP:N=1  VOL=1000    $ Source void
c --- Shielding ---
10   1  -2.3   1  -2          IMP:N=1              $ Concrete wall
c --- Detector Region ---
20   0         2  -3          IMP:N=1  VOL=500     $ Detector void
c --- Graveyard ---
999  0         3              IMP:N=0              $ Outside world

c =================================================================
c SURFACE CARDS - Geometric Boundaries
c =================================================================
c --- Source Region Boundary ---
1    SO   50.0                                     $ R=50 cm sphere
c --- Concrete Boundaries ---
2    SO   150.0                                    $ R=150 cm (100 cm thick)
c --- Outer Boundary ---
3    SO   200.0                                    $ R=200 cm

c =================================================================
c DATA CARDS - Problem Specifications
c =================================================================
MODE  N

c --- Materials ---
M1   1001  -0.01    6000  -0.001   8016  -0.53    $ Concrete (simplified)
     11023 -0.016   13027 -0.034   14000 -0.337
     20000 -0.044   26000 -0.014

c --- Source Definition ---
SDEF  POS=0 0 0  ERG=14.1                          $ 14.1 MeV point source

c --- Tallies ---
F4:N  20                                            $ Flux in detector
E4    0.01 0.1 1 10 14                             $ Energy bins (MeV)
F6:N  10                                            $ Heating in concrete
FM6   (-1 1 -6)                                     $ Total heating

c --- Cutoffs and Termination ---
NPS   10000000
CTME  120                                           $ 120 minutes max
PRINT
```

**2. Comment Sections with Visual Separators**:
```
c =================================================================
c SECTION TITLE
c =================================================================
c  Subsection description
c  - Detail 1
c  - Detail 2
c -----------------------------------------------------------------
```

**3. Inline Documentation**:
```
M1   1001  2   8016  1                             $ H2O water
     &                                              $ - H-1: 2 atoms
     &                                              $ - O-16: 1 atom
MT1  LWTR.01T                                       $ S(α,β) at 300K
```

### Common Card Orders

**Recommended Data Card Order**:
1. MODE (particle types)
2. Materials (M, MT, MX cards)
3. Source definition (SDEF, KCODE, SSR)
4. Tallies (F, E, T, C, FU, TF, SD, CF, FS, FM cards)
5. Variance reduction (IMP from cells, WWN, WWE, WWP, etc.)
6. Physics options (PHYS, CUT, TMP)
7. Output control (PRINT, PRDMP, DBCN)
8. Termination (NPS, CTME)

**Example**:
```
MODE  N P
M1    ...
MT1   ...
SDEF  ...
F4:N  ...
E4    ...
IMP:N  ...
IMP:P  ...
PHYS:N  ...
PHYS:P  ...
PRINT
NPS   1000000
CTME  60
```

### Particle Designators

**Common Particle Types**:
- `:N` = Neutron
- `:P` = Photon
- `:E` = Electron
- `:|` = Proton
- `:H` = Deuteron, triton, He-3, He-4 (combined)
- `:A` = All particles

**Examples**:
```
MODE  N P                                          $ Neutron + photon transport
IMP:N  1 1 0                                       $ Neutron importance
IMP:P  1 1 0                                       $ Photon importance
F4:N   1                                           $ Neutron flux
F4:P   1                                           $ Photon flux
PHYS:N  100 J J 1                                  $ Neutron physics options
```

### Default Units

**MCNP Standard Units**:
- Length: centimeters (cm)
- Energy: MeV
- Time: shakes (1 shake = 10⁻⁸ seconds)
- Temperature: MeV (k*T, where k = Boltzmann constant)
- Density: g/cm³ (positive) or atoms/barn-cm (negative)
- Angle: degrees (for some cards), cosines (for others)
- Cross sections: barns

**Examples**:
```
1    1  -1.0   -1   TMP=2.53e-8                   $ T=293K (room temp)
1    SO  10.0                                      $ R=10 cm
SDEF  POS=0 0 0  ERG=1.0                           $ E=1 MeV
```

## Decision Tree: Input File Creation

```
START: Need to create MCNP input file
  |
  +--> Do you have existing geometry/materials?
       |
       +--[YES]--> Use existing blocks, focus on source/tally setup
       |
       +--[NO]---> Build from scratch (full three-block structure)
                   |
                   +--> What problem type?
                        |
                        +--[Fixed Source]---> Basic structure (cells + surfaces + SDEF)
                        |                     ├─> Use template: "Fixed Source Template"
                        |                     └─> Add MODE, M, SDEF, F, NPS cards
                        |
                        +--[Criticality]-----> KCODE structure (fissile geometry)
                        |                     ├─> Use template: "KCODE Criticality Template"
                        |                     └─> Add MODE N, KCODE, KSRC, fissile M cards
                        |
                        +--[Shielding]-------> Multi-region + deep penetration
                        |                     ├─> Use template: "Shielding Template"
                        |                     └─> Add importance cells, possibly VR
                        |
                        +--[Detector]--------> Source + detector geometry
                                              ├─> Use template: "Detector Template"
                                              └─> Add F4/F5 tallies, energy bins
```

## Use Case 1: Simple Fixed-Source Problem (Sphere)

**Scenario**: 14.1 MeV point neutron source at center of water sphere (R=10 cm), calculate flux.

**Complete Input**:
```
Simple Fixed-Source Problem - Neutron Flux in Water Sphere
c =================================================================
c 14.1 MeV point source at center, water sphere R=10 cm
c Calculate neutron flux using F4 tally
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
c --- Material Definition ---
M1   1001  2   8016  1                              $ H2O
MT1  LWTR.01T                                        $ Light water S(α,β)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=14.1                            $ Point source, 14.1 MeV
c --- Tally Definition ---
F4:N  1                                              $ Volume-averaged flux
E4    0.01 0.1 1 10 13 14 15                        $ Energy bins (MeV)
c --- Termination ---
NPS   1000000                                        $ 10^6 histories
PRINT
```

**Key Points**:
- Three blocks clearly separated by blank lines
- VOL specified in cell card (for F4 normalization)
- IMP:N=0 in graveyard (particles killed)
- MT1 for thermal scattering in water
- Energy bins focused around source energy (14.1 MeV)

## Use Case 2: Multi-Material Shielding Problem

**Scenario**: Point source, three shielding layers (steel, polyethylene, lead), calculate flux in each.

**Complete Input**:
```
Multi-Layer Shielding Problem
c =================================================================
c Point source --> Steel --> Polyethylene --> Lead --> Detector
c Calculate flux in each layer
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
c --- Source Region ---
1    0         -1              IMP:N=1              $ Source void
c --- Shielding Layers ---
10   1  -7.86   1  -2          IMP:N=1              $ Steel (10 cm)
20   2  -0.94   2  -3          IMP:N=1              $ Polyethylene (20 cm)
30   3  -11.34  3  -4          IMP:N=1              $ Lead (15 cm)
c --- Detector Region ---
40   0          4  -5          IMP:N=1  VOL=1000    $ Detector void
c --- Graveyard ---
999  0          5              IMP:N=0              $ Outside

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
c Steel (AISI 304)
M1   26000  -0.695   24000  -0.190   28000  -0.095  $ Fe, Cr, Ni
     25055  -0.020
c Polyethylene (CH2)
M2   1001   -0.143   6000   -0.857                  $ H, C
MT2  POLY.01T                                        $ Polyethylene S(α,β)
c Lead
M3   82000  1.0                                      $ Pb-natural
c --- Source ---
SDEF  POS=0 0 0  ERG=D1
SP1   -3  0.8  2.5                                   $ Watt fission spectrum
c --- Tallies ---
F4:N  10 20 30 40                                    $ Flux in all layers
E4    0.01 0.1 1 10                                  $ Energy bins (MeV)
c --- Termination ---
NPS   10000000
CTME  120
PRINT
```

**Key Points**:
- Multiple material regions with realistic densities
- MT2 for polyethylene thermal scattering
- Watt spectrum source (fission-like)
- Multiple tallies in single F4 card (cells 10, 20, 30, 40)
- CTME for time limit (2 hours)

## Use Case 3: Criticality (KCODE) Problem

**Scenario**: Bare sphere of Pu-239 metal, calculate keff.

**Complete Input**:
```
Bare Pu-239 Metal Sphere - Criticality Calculation
c =================================================================
c Bare plutonium-239 metal sphere
c Calculate keff using KCODE
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
c --- Material Definition ---
M1   94239  1.0                                     $ Pu-239 (pure)
c --- KCODE Parameters ---
KCODE  10000  1.0  50  150                          $ Nper, k_guess, N_skip, N_total
KSRC   0 0 0                                        $ Starting source point
c --- Termination ---
c (KCODE controls termination via 150 cycles)
PRINT
```

**Key Points**:
- KCODE replaces SDEF + NPS for criticality problems
- KSRC provides initial source positions (MCNP will iterate)
- KCODE format: `KCODE Nsrc k0 Nskip Ncycles`
  - 10000 = histories per cycle
  - 1.0 = initial k guess
  - 50 = inactive cycles (skip for convergence)
  - 150 = total cycles (100 active)
- No explicit NPS card needed

## Use Case 4: Source-Detector Geometry (F5 Tally)

**Scenario**: Point source, calculate flux at detector location using F5 (point detector).

**Complete Input**:
```
Source-Detector Problem with F5 Point Detector
c =================================================================
c Point source at origin, detector at (100, 0, 0)
c Void geometry (no scattering)
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
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0                            $ 1 MeV point source
c --- Tally Definition ---
F5:N  100 0 0  0.5                                  $ Point detector at x=100
c      ^x  ^y ^z ^R                                 $ R=0.5 cm (exclusion sphere)
E5    0.1 0.5 0.9 1.0 1.1 1.5 2.0                   $ Energy bins
c --- Termination ---
NPS   1000000
PRINT
```

**Key Points**:
- F5 format: `F5:N x y z R`
  - (x,y,z) = detector location
  - R = exclusion sphere radius (particles within R ignored)
- F5 gives flux at a point (not volume-averaged like F4)
- Energy bins around source energy (1 MeV)
- Void geometry simplifies first-flight calculation

## Use Case 5: Complex Input with Transformations

**Scenario**: Repeated geometry (lattice preview), two offset spheres.

**Complete Input**:
```
Two Offset Spheres Using Coordinate Transformations
c =================================================================
c Two water spheres at different locations
c Demonstrates use of TRCL (transformation card)
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
c --- Sphere 1 (at origin) ---
1    1  -1.0   -1             IMP:N=1  VOL=4188.79  $ Water sphere 1
c --- Sphere 2 (offset via TRCL) ---
2    1  -1.0   -2  TRCL=1     IMP:N=1  VOL=4188.79  $ Water sphere 2
c --- Void Between ---
3    0         1  2  -3       IMP:N=1               $ Void gap
c --- Graveyard ---
999  0         3              IMP:N=0               $ Outside

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0                                      $ Sphere 1 (R=10)
2    SO   10.0                                      $ Sphere 2 (R=10, transformed)
3    SO   50.0                                      $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Transformation (move sphere 2 to x=30) ---
*TR1  30 0 0                                        $ Translation: dx=30 cm
c --- Material Definition ---
M1   1001  2   8016  1                              $ H2O
MT1  LWTR.01T                                        $ Light water S(α,β)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=14.1                           $ Source at origin
c --- Tallies ---
F4:N  1 2                                           $ Flux in both spheres
c --- Termination ---
NPS   1000000
PRINT
```

**Key Points**:
- TRCL references transformation card *TRn
- *TR1 format: `*TR1 dx dy dz` (translation only)
- Full format: `*TR1 dx dy dz  a11 a12 a13  a21 a22 a23  a31 a32 a33` (rotation matrix)
- Surface 2 is defined at origin but applied at transformed location
- Simplifies repeated geometry (don't redefine surfaces)

## Use Case 6: Input with External Files (Read Command)

**Scenario**: Large material library stored externally, source from file.

**Complete Input**:
```
Problem Using External Input Files
c =================================================================
c Demonstrates READ command for external files
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0      -1           IMP:N=1              $ Water cell
2    0            1            IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Read Material Definitions from File ---
READ  FILE=materials.txt
c --- Source from WSSA File ---
SSR  OLD=-1
c --- Tally ---
F4:N  1
E4    0.01 0.1 1 10
c --- Termination ---
NPS   1000000
PRINT
```

**External File: materials.txt**:
```
c =================================================================
c Material Library
c =================================================================
M1   1001  2   8016  1                              $ H2O
MT1  LWTR.01T
M2   26000  1.0                                      $ Iron
M3   82000  1.0                                      $ Lead
```

**Key Points**:
- READ command includes external file at that location
- Format: `READ FILE=filename`
- Useful for:
  - Shared material libraries
  - Large surface definitions
  - Generated inputs (scripts)
- SSR reads source from surface source write (WSSA) file
  - OLD=-1 uses file "wssa" (default name)

## Integration with Other Skills

This skill integrates with:

### 1. **mcnp-geometry-builder**
- Input structure provides framework
- Geometry builder fills Block 2 (cells) and Block 3 (surfaces)
- Proper card order ensures clean geometry definition

### 2. **mcnp-material-builder**
- Materials go in Block 3 (data cards)
- M, MT, MX cards follow MODE card
- Material numbers referenced in Block 2 (cell cards)

### 3. **mcnp-source-builder**
- Source cards (SDEF, KCODE, SSR) go in Block 3
- SDEF for fixed-source, KCODE for criticality
- Position references geometry from Block 2

### 4. **mcnp-tally-builder**
- Tallies (F4, F5, F6, etc.) go in Block 3 after source
- Energy bins (E), time bins (T), multipliers (FM) follow
- Cell/surface numbers reference Block 2 geometry

### 5. **mcnp-physics-builder**
- Physics cards (MODE, PHYS, CUT) go in Block 3
- MODE must be first data card
- PHYS and CUT fine-tune transport parameters

### 6. **mcnp-validation-checker**
- Checks three-block structure compliance
- Validates card continuation rules
- Verifies blank line separators

### Workflow Example:
```
1. mcnp-input-builder   → Create basic structure
2. mcnp-geometry-builder → Add cells + surfaces
3. mcnp-material-builder → Add materials
4. mcnp-source-builder   → Add source definition
5. mcnp-tally-builder    → Add tallies
6. mcnp-physics-builder  → Add physics options
7. mcnp-validation-checker → Verify syntax
```

## Common Errors and Troubleshooting

### Error 1: Missing Blank Line Between Blocks
**Symptom**:
```
bad trouble in subroutine getcl of mcrun
   cell card not terminated by blank line.
```

**Cause**: No blank line after cell card block

**Solution**:
```
c Cell Cards
1    1  -1.0   -1   IMP:N=1
2    0         1    IMP:N=0
<--- BLANK LINE REQUIRED HERE
c Surface Cards
1    SO   10.0
```

### Error 2: Tab Character Issues
**Symptom**: Misaligned continuation lines, cards not recognized

**Cause**: MCNP treats tabs as single spaces

**Solution**: Configure editor to convert tabs to spaces
```
c BAD (using tabs):
F4:N	1	2	3    (tabs between entries)

c GOOD (using spaces):
F4:N  1  2  3        (spaces between entries)
```

### Error 3: Card Out of Order
**Symptom**:
```
bad trouble in subroutine mcrun
   mode card must precede all data cards.
```

**Cause**: MODE card not first in data block

**Solution**: Ensure MODE is first data card:
```
c CORRECT ORDER:
MODE  N
M1    ...
SDEF  ...
F4:N  ...
```

### Error 4: Missing Particle Designator
**Symptom**:
```
warning.  tally or card may need a particle designator.
```

**Cause**: Card requires `:N` or `:P` but none provided

**Solution**:
```
c BAD:
F4  1          $ Missing :N

c GOOD:
F4:N  1        $ Neutron flux tally
```

### Error 5: Continuation Line Incorrect
**Symptom**: Card reads incorrectly, extra entries ignored

**Cause**: Improper indentation or missing `&`

**Solution**:
```
c METHOD 1 (5+ leading spaces):
F4:N  1 2 3 4 5
      6 7 8 9 10

c METHOD 2 (ampersand):
F4:N  1 2 3 4 5 &
      6 7 8 9 10

c METHOD 3 (explicit card name):
F4:N  1 2 3 4 5
F4:N  6 7 8 9 10
```

### Error 6: Unterminated Input
**Symptom**: MCNP hangs or reads past end of file

**Cause**: No blank line at end of file

**Solution**: Add blank line after last data card:
```
NPS   1000000
PRINT
<--- BLANK LINE REQUIRED HERE
```

### Error 7: Comment Character in Wrong Column
**Symptom**: Card not recognized, treated as comment

**Cause**: `C` or `$` in column 1-5 of non-comment line

**Solution**:
```
c BAD:
C    F4:N  1        $ This is treated as comment

c GOOD:
     F4:N  1        $ Proper card with inline comment
```

## Validation Checklist

Before running MCNP input:

- [ ] **Three-block structure**:
  - [ ] Optional message block (or title line only)
  - [ ] Cell cards block (all cells defined)
  - [ ] Blank line after cell cards
  - [ ] Surface cards (all surfaces referenced)
  - [ ] Data cards (MODE first, NPS/CTME last)
  - [ ] Blank line at end of file

- [ ] **Card formatting**:
  - [ ] No tabs used (only spaces)
  - [ ] Continuation lines properly indented (5+ spaces or `&`)
  - [ ] Particle designators where needed (`:N`, `:P`, etc.)
  - [ ] Inline comments use `$` (not `C`)

- [ ] **Geometry consistency**:
  - [ ] All cell surfaces defined in surface block
  - [ ] All cells have importance (IMP:N, IMP:P)
  - [ ] Graveyard cell exists with IMP=0
  - [ ] No overlapping cells (run geometry plot to verify)

- [ ] **Material/Source/Tally**:
  - [ ] Materials referenced in cells are defined (M cards)
  - [ ] Source position inside non-zero importance cell
  - [ ] Tally cells/surfaces exist in geometry

- [ ] **Termination**:
  - [ ] NPS or KCODE specified
  - [ ] Optional: CTME for time limit

## Advanced Topics

### 1. Input Generation from Scripts
**Python Example**:
```python
def write_mcnp_input(cells, surfaces, materials, source, tallies):
    with open('input.i', 'w') as f:
        f.write("MCNP Input Generated by Script\n")
        f.write("c " + "="*60 + "\n\n")

        # Cell cards
        for cell in cells:
            f.write(f"{cell['id']}  {cell['mat']}  {cell['dens']}  "
                    f"{cell['geom']}  IMP:N={cell['imp']}\n")
        f.write("\n")

        # Surface cards
        for surf in surfaces:
            f.write(f"{surf['id']}  {surf['type']}  {surf['params']}\n")
        f.write("\n")

        # Data cards
        f.write("MODE  N\n")
        for mat in materials:
            f.write(f"M{mat['id']}  {mat['composition']}\n")
        f.write(f"SDEF  {source}\n")
        for tally in tallies:
            f.write(f"F{tally['type']}:N  {tally['cells']}\n")
        f.write("NPS  1000000\n")
        f.write("\n")

# Usage
cells = [
    {'id': 1, 'mat': 1, 'dens': -1.0, 'geom': '-1', 'imp': 1},
    {'id': 2, 'mat': 0, 'dens': '', 'geom': '1', 'imp': 0}
]
surfaces = [{'id': 1, 'type': 'SO', 'params': '10.0'}]
materials = [{'id': 1, 'composition': '1001  2  8016  1'}]
source = 'POS=0 0 0  ERG=14.1'
tallies = [{'type': 4, 'cells': '1'}]

write_mcnp_input(cells, surfaces, materials, source, tallies)
```

### 2. Input File Modularization
**Directory Structure**:
```
project/
├── input.i                  # Main input
├── geometry/
│   ├── core.txt            # Core region cells/surfaces
│   ├── reflector.txt       # Reflector cells/surfaces
│   └── shielding.txt       # Shielding cells/surfaces
├── materials/
│   ├── fuel.txt            # Fuel compositions
│   └── structural.txt      # Structural materials
└── tallies/
    └── detectors.txt       # Detector tallies
```

**Main Input (input.i)**:
```
Modular Input File Example
c =================================================================
c READ geometry from external files
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
READ  FILE=geometry/core.txt
READ  FILE=geometry/reflector.txt
READ  FILE=geometry/shielding.txt
999  0  999  IMP:N=0                               $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
999  SO  500.0                                      $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE  N
READ  FILE=materials/fuel.txt
READ  FILE=materials/structural.txt
KCODE  10000  1.0  50  150
KSRC   0 0 0
READ  FILE=tallies/detectors.txt
PRINT
```

### 3. Version-Specific Considerations

**MCNP5 vs MCNP6 Differences**:
- **MCNP6** supports extended features:
  - Burnup (BURN card)
  - Mesh tallies (FMESH with XDMF output)
  - Enhanced S(α,β) libraries
  - Unstructured mesh (UMESH)
- **MCNP5** compatibility:
  - Avoid FMESH with OUT=xdmf
  - Use TMESH instead of FMESH (if needed)
  - Check library availability (.70c, .01t, etc.)

**Backward Compatibility Tips**:
```
c MCNP6-only feature (FMESH with XDMF):
FMESH14:N  GEOM=XYZ  ORIGIN=0 0 0  IMESH=10  IINTS=10  OUT=xdmf

c MCNP5-compatible alternative (TMESH):
TMESH
      RMESH1:N  FLUX
      CORA1     -10  10  10I
      CORB1     -10  10  10I
      CORC1     -10  10  10I
ENDMD
```

## Best Practices Summary

1. **Structure**:
   - Always use three-block structure (cells, surface, data)
   - Separate blocks with blank lines
   - End file with blank line

2. **Formatting**:
   - Use spaces (not tabs)
   - Consistent indentation (5 spaces for continuation)
   - Inline comments with `$` (not `C`)

3. **Organization**:
   - Group related cards with comment headers
   - Use visual separators (`c ===...`)
   - Logical card order (MODE → Materials → Source → Tallies → Termination)

4. **Documentation**:
   - Title line describes problem
   - Inline comments explain non-obvious choices
   - Include units where ambiguous

5. **Modularity**:
   - Use READ for large shared sections
   - External material libraries
   - Script-generated repetitive geometry

6. **Validation**:
   - Check syntax before running (use validation checker skill)
   - Plot geometry (MCNP geometry plotter)
   - Review output for warnings

7. **Programmatic Input Generation**:
   - For automated input file creation, see: `mcnp_input_generator.py`
   - Useful for parametric studies, batch generation, and template-based workflows

## Quick Reference: Essential Cards

| Card    | Purpose                  | Example                              |
|---------|--------------------------|--------------------------------------|
| MODE    | Particle types           | `MODE  N P`                          |
| M       | Material composition     | `M1  1001  2  8016  1`               |
| SDEF    | Fixed source             | `SDEF  POS=0 0 0  ERG=14.1`          |
| KCODE   | Criticality source       | `KCODE  10000  1.0  50  150`         |
| F4      | Volume flux              | `F4:N  1 2 3`                        |
| F5      | Point detector flux      | `F5:N  10 0 0  0.5`                  |
| NPS     | Number of histories      | `NPS  1000000`                       |
| CTME    | Time limit (minutes)     | `CTME  120`                          |
| IMP     | Cell importance          | `IMP:N=1` (in cell card)             |
| PRINT   | Output control           | `PRINT`                              |

## References and Further Reading

- **User Manual**: Chapter 3 (Introduction to MCNP Usage), Chapter 4 (Input Description)
- **Related Skills**:
  - mcnp-geometry-builder (Cell/Surface cards)
  - mcnp-material-builder (M/MT cards)
  - mcnp-source-builder (SDEF/KCODE)
  - mcnp-tally-builder (F4/F5/F6)
  - mcnp-physics-builder (MODE/PHYS/CUT)
  - mcnp-validation-checker (Syntax verification)

---

**End of MCNP Input Builder Skill**
