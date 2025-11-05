# MCNP Input Validation Procedures

## Overview

This document provides detailed algorithms and procedures for validating MCNP input files before simulation execution. These procedures are implemented in the Python validation scripts and form the systematic approach for comprehensive input validation.

---

## 5-Step Validation Procedure

### Step 1: Initial Assessment and Context Gathering

**Purpose:** Understand validation scope and user requirements

**Actions:**
1. Identify input file path and accessibility
2. Determine validation level needed:
   - Quick syntax check (basic format only)
   - Comprehensive validation (all checks)
   - Targeted validation (specific concern)
3. Understand problem context:
   - Production run vs. learning exercise
   - Known issues or specific concerns
   - Previous validation attempts
4. Check if geometry has been plotted
5. Determine output detail level needed

**Outputs:**
- Validation scope definition
- User context for result interpretation
- Priority areas for validation

---

### Step 2: Block Structure Validation

**Purpose:** Verify three-block MCNP input structure and delimiters

**Algorithm:**

```
1. Read entire input file
2. Identify blank lines (empty or whitespace-only)
3. Count total blank lines
4. Identify block boundaries:
   - Title card (line 1 or after MESSAGE)
   - First blank line → end of Cell Cards block
   - Second blank line → end of Surface Cards block
   - Remaining lines → Data Cards block
5. Validate structure:
   - Exactly 2 blank lines in file
   - Title card present
   - Each block has content
   - No cards in wrong block
```

**Checks:**

1. **Title Card Validation**
   - Present on first line (or after MESSAGE)
   - Not blank
   - Single line (no continuation allowed)

2. **Blank Line Count**
   - FATAL if ≠ 2 blank lines
   - Report location of extra/missing blank lines
   - Identify which block separation is affected

3. **Block Content**
   - Cell Cards block: Lines between title and first blank
   - Surface Cards block: Lines between first and second blank
   - Data Cards block: Lines after second blank
   - FATAL if any block empty

4. **Card Type Verification**
   - Cell cards: Numeric first token (cell number)
   - Surface cards: Numeric first token (surface number) or *macro
   - Data cards: Alphabetic mnemonic or special keywords
   - FATAL if card type in wrong block

**Common Errors:**
- Extra blank lines between cards within a block
- Missing blank line between blocks
- Cards in wrong block (e.g., MODE in surface block)
- No title card

**References:**
- MCNP6 Manual Chapter 4: Input File Format
- mcnp-input-builder skill: Three-block structure standards

---

### Step 3: Card Syntax Validation

**Purpose:** Verify individual card format and syntax

**Algorithm:**

```
For each card in input:
1. Identify card type (cell, surface, or data)
2. Parse card mnemonic/number
3. Check continuation lines (& character)
4. Validate parameter count and types
5. Check for deprecated syntax
6. Verify special characters and delimiters
```

**Cell Card Validation:**

```
Format: j  m  d  geom  params

Where:
  j = cell number (integer)
  m = material number (integer) or 0 for void
  d = density (real) - negative for atom/b-cm, positive for g/cm³
  geom = Boolean geometry expression
  params = optional cell parameters (IMP, VOL, U, FILL, etc.)
```

**Checks:**
1. Cell number j is unique and positive
2. Material number m exists (M card defined) or is 0
3. Density d appropriate sign and magnitude
4. Geometry expression valid:
   - References only defined surfaces
   - Valid Boolean operators (space=intersection, :=union)
   - Proper use of complement operator (#)
   - Parentheses balanced
5. Cell parameters have valid syntax
6. No duplicate cell parameters

**Surface Card Validation:**

```
Format: n  type/mnemonic  [tr]  parameters

Where:
  n = surface number (integer)
  type/mnemonic = surface type or macrobody name
  tr = optional transformation number
  parameters = geometry parameters (varies by type)
```

**Checks:**
1. Surface number n is unique and positive
2. Type/mnemonic is valid:
   - Plane: P, PX, PY, PZ
   - Sphere: S, SX, SY, SZ, SO
   - Cylinder: C/X, C/Y, C/Z, CX, CY, CZ
   - Cone: K/X, K/Y, K/Z, KX, KY, KZ
   - Quadric: GQ, SQ
   - Torus: TX, TY, TZ
   - Macrobodies: BOX, RPP, SPH, RCC, RHP, HEX, etc.
3. Parameter count matches surface type requirements
4. Transformation number (if present) is defined
5. Numerical parameters are valid

**Data Card Validation:**

```
Format: MNEMONIC  parameters

Where:
  MNEMONIC = card identifier (MODE, M, SDEF, etc.)
  parameters = card-specific parameters
```

**Checks:**
1. Mnemonic is recognized MCNP keyword
2. Parameter count and types appropriate
3. Cross-references valid (materials, cells, surfaces)
4. Numerical ranges appropriate
5. Required cards present (MODE, NPS/CTME)
6. Card ordering follows requirements

**Common Syntax Errors:**
- Missing required parameters
- Wrong parameter types (string vs. number)
- Invalid mnemonics or surface types
- Unbalanced parentheses in geometry
- Missing continuation character (&)
- Parameters on wrong card type

**References:**
- MCNP6 Manual Chapter 5: Input Cards
- Skill references: card_specifications.md files from builder skills

---

### Step 4: Cross-Reference Validation

**Purpose:** Verify all references resolve to defined entities

**Algorithm:**

```
1. Build symbol tables:
   - Cells: {cell_number: cell_definition}
   - Surfaces: {surface_number: surface_definition}
   - Materials: {material_number: material_definition}
   - Universes: {universe_number: cells_in_universe}
   - Transformations: {tr_number: tr_definition}

2. Check cell → surface references:
   For each cell geometry expression:
     Extract all surface numbers
     Verify each exists in surfaces table

3. Check cell → material references:
   For each cell with m ≠ 0:
     Verify M card exists for material m

4. Check tally references:
   For each F-type tally:
     Verify referenced cells/surfaces exist

5. Check multiplier references:
   For each FM card:
     Verify material numbers exist

6. Check transformation references:
   For each TR/TRCL reference:
     Verify TR card exists

7. Check universe/fill references:
   For each FILL card:
     Verify universe number exists

8. Check importance cards:
   Verify IMP card entries match cell count
```

**Cross-Reference Types:**

**1. Cell Geometry → Surfaces**
```
Example:
  Cell: 10  1  -2.7  -1 2 -3 (4:5)
  Must verify: Surfaces 1, 2, 3, 4, 5 are defined
```

**2. Cell Material → Material Definitions**
```
Example:
  Cell: 10  5  -2.7  -1 2 -3
  Must verify: M5 card exists
```

**3. Tally → Cells/Surfaces**
```
Example:
  F4:N  10 20 30
  Must verify: Cells 10, 20, 30 exist

  F2:N  1 2 3
  Must verify: Surfaces 1, 2, 3 exist
```

**4. FM Multiplier → Materials**
```
Example:
  FM4  1.0 5 102
  Must verify: Material 5 exists
```

**5. TRCL → Transformation**
```
Example:
  Cell: 10  1  -2.7  -1 2 -3  TRCL=5
  Must verify: TR5 or *TR5 card exists
```

**6. FILL → Universe**
```
Example:
  Cell: 20  0  -10 11 -12  FILL=5
  Must verify: Universe 5 exists (cells with U=5)
```

**7. Importance Count → Cell Count**
```
Example:
  15 cells defined
  IMP:N  1 1 1 1 1 1 1 1 1 1 0 0 0 0 0
  Must verify: Exactly 15 entries
```

**Common Cross-Reference Errors:**
- Undefined surface in cell geometry
- Undefined material in cell definition
- Tally references non-existent cell
- FILL references undefined universe
- IMP card entry count mismatch
- TRCL references undefined transformation

**Error Messages:**
```
FATAL: Cell 10 geometry references undefined surface 203
FATAL: Cell 8 uses material 5, but M5 card not defined
FATAL: Tally F4:N references undefined cell 25
WARNING: IMP:N has 14 entries but 15 cells exist
FATAL: Cell 20 FILL=5 but universe 5 not defined
```

**References:**
- MCNP6 Manual §4.4: Cross-Reference Requirements
- mcnp-cross-reference-checker skill: Detailed dependency analysis

---

### Step 5: Physics Consistency Validation

**Purpose:** Verify physics settings are consistent and appropriate

**Algorithm:**

```
1. Check MODE card:
   - Particle types appropriate for problem
   - Required physics cards present

2. Check PHYS cards:
   - Energy ranges cover source energies
   - Physics options appropriate

3. Check cross-section libraries:
   - ZAID formats valid
   - Library suffixes consistent
   - Libraries match MODE particles

4. Check source-physics consistency:
   - Source energies within physics ranges
   - Source particle types in MODE

5. Check tally-physics consistency:
   - Tally particle types in MODE
   - Energy bins within physics ranges

6. Check material-physics consistency:
   - Thermal scattering for thermal problems
   - Appropriate libraries for particle types
```

**MODE Card Validation:**

**Valid MODE combinations:**
- `MODE N` - Neutron transport only
- `MODE P` - Photon transport only
- `MODE E` - Electron transport only
- `MODE N P` - Coupled neutron-photon
- `MODE P E` - Coupled photon-electron
- `MODE N P E` - All three particles
- `MODE H` - Proton transport
- And others...

**Checks:**
1. MODE card present (FATAL if missing)
2. Particle types are valid
3. Coupled mode implications understood
4. Required PHYS cards present for each particle

**PHYS Card Validation:**

**Format:** `PHYS:N  emax  emcnf  ides  nocoh  ispn  nodop`

**Checks:**
1. PHYS card exists for each MODE particle
2. `emax` (max energy) ≥ maximum source energy
3. Energy range covers tally bins
4. Physics options appropriate for problem:
   - `emcnf`: Analog vs. implicit capture
   - `ides`: Detailed physics on/off
   - `nocoh`: Coherent scattering
   - `ispn`: Photon-induced fission
   - `nodop`: Doppler broadening

**Cross-Section Library Validation:**

**ZAID Format:** `ZZZAAA.XXc/p/e/h/...`
- `ZZZ` = atomic number (1-118)
- `AAA` = mass number (0 for natural mix)
- `XX` = library version
- `c/p/e/h` = particle type suffix

**Checks:**
1. ZAID format valid: `92235.80c` ✓, `92235` ✗
2. Library suffixes consistent within material
3. Particle suffix matches MODE:
   - MODE N → .XXc (neutron)
   - MODE P → .XXp (photoatomic)
   - MODE E → .XXe (electron)
   - MODE H → .XXh (proton)
4. Library versions consistent (prefer same ENDF version)
5. Isotopes exist in specified library

**Common inconsistencies:**
- Mixed ENDF libraries (.70c and .80c in same problem)
- Wrong particle type (.80c in MODE P problem)
- Missing library suffix (.80c vs bare 92235)

**Source-Physics Consistency:**

```
Example:
  MODE N
  SDEF  ERG=14.1
  PHYS:N  20  $ emax = 20 MeV

Check: 14.1 MeV source < 20 MeV physics range ✓
```

**Checks:**
1. Source particle type in MODE
2. Source energies < PHYS emax
3. For distributions: maximum energy < PHYS emax
4. Energy cutoffs don't eliminate source particles

**Tally-Physics Consistency:**

```
Example:
  MODE N P
  F4:N  10
  F7:P  20

Check: Both N and P in MODE ✓
```

**Checks:**
1. Tally particle types in MODE
2. Tally energy bins within PHYS range
3. Energy cutoffs don't eliminate tallies

**Material-Physics Consistency:**

**Thermal neutron problems:**
```
M1   1001.80c  2      $ H in H2O
     8016.80c  1      $ O in H2O
MT1  lwtr.20t         $ Thermal scattering required ✓

WARNING if MT card missing for thermal materials
```

**Checks:**
1. Water materials have S(α,β) thermal scattering
2. Thermal materials (hydrogen, graphite) have MT cards
3. Temperature cards (TMP) in MeV not Kelvin
4. Photon production enabled if MODE N P

**Common Physics Errors:**
- MODE card missing
- PHYS emax < source energy
- Missing thermal scattering for water
- TMP in Kelvin instead of MeV (300 vs 2.53e-8)
- Library suffix mismatch with MODE

**Error Messages:**
```
FATAL: MODE card missing
FATAL: PHYS:N emax=10 but source energy=14.1 MeV
WARNING: Material 1 appears to be H2O but no MT1 card
WARNING: TMP1=300 - should this be 2.53e-8 MeV (300K)?
ERROR: Material uses .80p library but MODE is N (need .80c)
```

**References:**
- MCNP6 Manual Chapter 5.7: Physics Data Cards
- mcnp-physics-builder skill: Physics settings standards
- mcnp-physics-validator skill: Detailed physics validation

---

## Validation Reporting

### Report Structure

**Standard validation report format:**

```
========================================
MCNP INPUT VALIDATION REPORT
========================================
File: [filename]
Date: [timestamp]
Validator: mcnp-input-validator v2.0.0

SUMMARY:
  Status: [PASSED / FAILED]
  Fatal Errors: [count]
  Warnings: [count]
  Recommendations: [count]

========================================
FATAL ERRORS (must fix before running)
========================================
[If none: "None - input is valid"]

1. [Error description]
   Location: [file location/line number]
   Issue: [what's wrong]
   Fix: [how to correct]
   Reference: [manual section]

[Repeat for each error]

========================================
WARNINGS (should review)
========================================
[If none: "None"]

1. [Warning description]
   Consideration: [why this matters]
   Optional fix: [how to address]
   Reference: [manual section]

[Repeat for each warning]

========================================
RECOMMENDATIONS (best practices)
========================================
[Always include at minimum:]

1. Plot geometry before running (ESSENTIAL)
   Command: mcnp6 ip i=[filename]
   Look for: Dashed lines indicating errors

2. Test with VOID card (recommended)
   Purpose: Find geometry overlaps/gaps quickly

[Additional recommendations as appropriate]

========================================
NEXT STEPS
========================================
[Guidance based on validation results]

If FAILED:
  1. Fix fatal errors in order listed
  2. Re-validate after each major fix
  3. Plot geometry after errors resolved

If PASSED:
  1. Review warnings
  2. MUST plot geometry (not optional)
  3. Consider VOID card testing
  4. Ready to run MCNP

========================================
```

### Error Prioritization

**Priority 1: Block Structure**
- Must fix first - cascading errors likely
- Re-validate after fixing

**Priority 2: Cross-References**
- Fix in order encountered
- May reveal additional issues

**Priority 3: Physics Settings**
- Check after structure/references valid
- May affect convergence, not validity

**Priority 4: Warnings & Recommendations**
- Address after all FATAL errors fixed
- May improve results, not required for execution

---

## Validation Principles

### Principle 1: First Error is Real

The first reported error is always genuine. Subsequent errors may be:
- Real additional problems
- Cascade effects from first error
- Parser confusion due to first error

**Best practice:** Fix errors in order, re-validate after each major fix

### Principle 2: Validation ≠ Geometry Verification

Input validation checks:
- Syntax and format
- Cross-reference integrity
- Physics consistency

Input validation CANNOT detect:
- Geometry overlaps (two cells occupy same space)
- Geometry gaps (no cell defines space)
- Incorrect geometry (sphere when meant cylinder)

**Mandatory:** ALWAYS plot geometry even if validation passes 100%

### Principle 3: Context Matters

Validation must consider problem context:
- Quick check during development vs. pre-production validation
- Learning exercise vs. production run
- Known good template vs. new input

Adjust thoroughness and reporting based on context.

### Principle 4: Help Fix, Don't Just Report

Effective validation includes:
- Clear error descriptions
- Specific fix instructions
- Examples of correct syntax
- Manual section references
- Offer to implement fixes

### Principle 5: Integrate with Completed Skills

Validation should reference and use standards from completed skills:
- mcnp-input-builder: File structure standards
- mcnp-geometry-builder: Cell/surface format standards
- mcnp-material-builder: Material definition standards
- mcnp-source-builder: Source card standards
- mcnp-tally-builder: Tally card standards
- mcnp-physics-builder: Physics settings standards

---

## Special Validation Cases

### Lattice Problems (U/LAT/FILL)

**Additional checks:**
1. Cells with LAT parameter have U parameter
2. FILL references valid universe numbers
3. Lattice dimensions appropriate (not excessive)
4. Filled cells don't have material (m=0)

**Reference:** mcnp-lattice-builder skill for lattice validation standards

### Criticality Problems (KCODE)

**Additional checks:**
1. KCODE card present (not SDEF)
2. Fissionable materials present
3. Initial source specification appropriate
4. KSRC or starting distribution specified
5. Particle count per cycle sufficient

**Reference:** mcnp-source-builder skill for KCODE standards

### Weight Window Problems

**Additional checks:**
1. WWN card parameters consistent
2. Weight windows defined for all cells
3. Weight window energies match problem
4. Generator parameters appropriate if using WWG

**Reference:** mcnp-variance-reducer skill for weight window standards

---

## Validation Automation

The validation procedures in this document are implemented in:
- `scripts/mcnp_input_validator.py` - Main validation engine
- `scripts/block_structure_validator.py` - Block structure checks
- `scripts/cross_reference_checker.py` - Cross-reference validation
- `scripts/physics_consistency_checker.py` - Physics checks

See `scripts/README.md` for usage documentation.

---

**END OF VALIDATION PROCEDURES**
