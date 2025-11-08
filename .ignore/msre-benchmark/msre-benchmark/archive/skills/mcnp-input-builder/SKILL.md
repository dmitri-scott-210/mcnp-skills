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
See `assets/` subdirectory:

- **Templates** (`assets/templates/`)
  - basic_fixed_source_template.i
  - kcode_criticality_template.i
  - shielding_template.i
  - detector_template.i
  - README.md (template usage guide)

- **Example Inputs** (`assets/example_inputs/`)
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

**End of MCNP Input Builder Skill**
