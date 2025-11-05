# MCNP Input Validation Checklists

## Overview

This document provides comprehensive validation checklists for MCNP input files at various thoroughness levels. Use these checklists systematically to ensure input quality before simulation execution.

---

## Quick Syntax Checklist (5 minutes)

**Purpose:** Basic format validation during development

**When to use:**
- Rapid iteration during input development
- Quick check after minor edits
- Learning/educational contexts

### Structure Checks

- [ ] Title card present on first line
- [ ] Exactly 2 blank lines in file
- [ ] Blank line after cell cards block
- [ ] Blank line after surface cards block
- [ ] No blank lines within any block
- [ ] All three blocks present (cells, surfaces, data)

### Basic Syntax

- [ ] Cell cards: Numeric first token
- [ ] Surface cards: Numeric first token or *macro
- [ ] Data cards: Alphabetic mnemonics
- [ ] No obvious typos in card names
- [ ] Continuation lines use & properly
- [ ] Comments use 'c' in first column

### Required Cards

- [ ] MODE card present
- [ ] NPS or CTME card present
- [ ] At least one cell defined
- [ ] At least one surface defined
- [ ] At least one material defined (unless all void)

**Estimated time:** 5 minutes manual review or <1 second automated

---

## Comprehensive Validation Checklist (30 minutes)

**Purpose:** Thorough validation before production runs

**When to use:**
- Before expensive calculations
- Production/publication runs
- Critical safety calculations
- After major input changes

### 1. File Structure (5 items)

- [ ] Title card descriptive and present
- [ ] MESSAGE card appropriate (if present)
- [ ] Exactly 2 blank lines separating blocks
- [ ] Cell cards block: Lines between title and first blank
- [ ] Surface cards block: Lines between first and second blank
- [ ] Data cards block: Lines after second blank
- [ ] No blank lines within any block
- [ ] File encoding is ASCII or UTF-8
- [ ] Line length < 128 characters (unless continued)
- [ ] No tabs in file (spaces only)

### 2. Cell Cards Validation (15 items)

- [ ] All cell numbers unique and positive
- [ ] All cell numbers < 100,000,000
- [ ] Material numbers reference existing M cards
- [ ] Void cells have m=0
- [ ] Non-void cells have material and density
- [ ] Density appropriate sign (negative=atom/b-cm, positive=g/cm³)
- [ ] Density magnitude reasonable
- [ ] Geometry expressions reference only defined surfaces
- [ ] Boolean operators valid (space, :, #)
- [ ] Parentheses balanced in geometry
- [ ] Complement operator (#) used correctly
- [ ] Cell parameters (IMP, VOL, U, FILL, etc.) valid syntax
- [ ] No duplicate cell parameters
- [ ] Universe numbers consistent
- [ ] FILL references existing universes
- [ ] TRCL references existing transformations
- [ ] No circular FILL references
- [ ] Lattice cells properly defined (LAT, FILL)

### 3. Surface Cards Validation (12 items)

- [ ] All surface numbers unique and positive
- [ ] All surface numbers < 100,000,000
- [ ] Surface types/mnemonics recognized
- [ ] Parameter count matches surface type:
  - [ ] Planes: P(4), PX/PY/PZ(1)
  - [ ] Spheres: S(4), SO(1), SX/SY/SZ(2)
  - [ ] Cylinders: C/X,C/Y,C/Z(3), CX/CY/CZ(2)
  - [ ] Cones: K/X,K/Y,K/Z(4), KX/KY/KZ(3)
  - [ ] Macrobodies: See macrobody specifications
- [ ] Transformation numbers reference existing TR cards
- [ ] Numerical parameters valid ranges
- [ ] No duplicate surface definitions
- [ ] All referenced surfaces are used in at least one cell
- [ ] Surface normals point expected direction
- [ ] Coincident surfaces handled correctly
- [ ] Reflecting surfaces (*) used appropriately
- [ ] White boundary surfaces (+) used appropriately

### 4. Material Specifications (18 items)

- [ ] All M card numbers match cell material references
- [ ] No unused material definitions (or documented why)
- [ ] ZAID format valid: ZZZAAA.XXc/p/e
- [ ] Atomic numbers (ZZZ) valid (1-118)
- [ ] Mass numbers (AAA) valid for isotope
- [ ] Library suffixes (.XXc) consistent within material
- [ ] Particle type suffix matches MODE
- [ ] ENDF library versions consistent (prefer single version)
- [ ] Fraction sum appropriate:
  - [ ] Weight fractions can be any positive values
  - [ ] Atom fractions: normalize or use negative densities
- [ ] No mixing atomic and weight fractions
- [ ] Natural isotopes use AAA=000
- [ ] MT cards present for thermal materials:
  - [ ] Water: lwtr.20t or hwtr.20t
  - [ ] Polyethylene: poly.20t
  - [ ] Graphite: grph.20t
  - [ ] Benzene: benz.20t
- [ ] TMP cards in MeV not Kelvin
- [ ] TMP values reasonable (2e-8 to 1e-6 MeV typical)
- [ ] MX cards reference valid tables
- [ ] Isotope availability verified in DATAPATH
- [ ] Material density physically reasonable
- [ ] Fissionable materials for criticality problems

### 5. Source Specification (12 items)

- [ ] Source card present (SDEF or KCODE, not both)
- [ ] Source particle type in MODE
- [ ] SDEF parameters valid:
  - [ ] POS or distribution specified
  - [ ] ERG or distribution specified
  - [ ] DIR or distribution specified (if needed)
- [ ] Source distributions properly defined:
  - [ ] SI cards match SDEF references
  - [ ] SP cards match SI cards
  - [ ] Distribution types appropriate (L, A, H)
  - [ ] Energy bins in increasing order
  - [ ] Probabilities sum to 1.0 (or normalized)
- [ ] Source position inside geometry
- [ ] Source energies within PHYS range
- [ ] For KCODE:
  - [ ] Fissionable materials present
  - [ ] KSRC or initial distribution specified
  - [ ] Particles per cycle reasonable
  - [ ] Number of cycles sufficient
  - [ ] Skip cycles appropriate

### 6. Tally Specifications (14 items)

- [ ] Tally particle types in MODE
- [ ] F1/F2/F4/F5/F6/F7/F8 syntax correct
- [ ] Tally numbers unique
- [ ] Surface tallies (F1, F2) reference existing surfaces
- [ ] Cell tallies (F4, F6, F7) reference existing cells
- [ ] Energy bins in increasing order
- [ ] Energy bins within particle range
- [ ] Multiplier cards (FM) valid:
  - [ ] Reference existing tallies
  - [ ] Material numbers exist
  - [ ] Reaction numbers valid (MT numbers)
- [ ] User bins (FU) appropriate
- [ ] Time bins (FT) in increasing order
- [ ] Cosine bins (FC) in valid range [-1, 1]
- [ ] Segment cards (FS) reference valid entities
- [ ] Tally comments (FC) present for clarity
- [ ] SD cards appropriate (for per-unit-volume/area)

### 7. Physics Settings (16 items)

- [ ] MODE card present
- [ ] MODE particles appropriate for problem
- [ ] PHYS cards present for each MODE particle
- [ ] PHYS energy ranges:
  - [ ] emax ≥ maximum source energy
  - [ ] emax covers tally energy bins
  - [ ] emin appropriate (default usually OK)
- [ ] Physics options appropriate:
  - [ ] Analog vs. implicit capture (emcnf)
  - [ ] Detailed physics (ides)
  - [ ] Secondary particle production
- [ ] CUT cards (if present) reasonable
- [ ] Energy cutoffs don't eliminate important physics
- [ ] For coupled problems:
  - [ ] Photon production enabled (PHYS:N)
  - [ ] Electron production enabled (PHYS:P)
  - [ ] Bremsstrahlung appropriate (PHYS:E)
- [ ] Cross-section library paths set (DATAPATH)
- [ ] TOTNU card appropriate for criticality
- [ ] ACT card for activation problems
- [ ] Variance reduction doesn't violate physics
- [ ] Random number seed documented (DBCN RAND)

### 8. Cross-Reference Integrity (10 items)

- [ ] All cell geometry surfaces exist
- [ ] All cell materials exist
- [ ] All tally cells/surfaces exist
- [ ] All FM card materials exist
- [ ] All TRCL transformations exist
- [ ] All FILL universes exist
- [ ] All TR card references valid
- [ ] Importance card counts match cell counts
- [ ] No orphaned definitions (unused surfaces, materials)
- [ ] No circular dependencies (FILL, U references)

### 9. Variance Reduction (8 items)

- [ ] Importance cards (IMP) present
- [ ] IMP entries match cell count exactly
- [ ] Graveyard cell has IMP=0
- [ ] Importance gradients not excessive (factor <4 between adjacent)
- [ ] Weight window cards (WWN) appropriate
- [ ] Weight window energies match problem
- [ ] DXTRAN spheres (if present) properly placed
- [ ] Forced collision (FCL) used appropriately

### 10. Output and Control (8 items)

- [ ] NPS value appropriate for statistics
- [ ] CTME reasonable if time limit used
- [ ] PRINT cards appropriate (not excessive)
- [ ] PRDMP cards for checkpoint/restart
- [ ] FILES card if non-default files needed
- [ ] DBCN cards documented if used
- [ ] LOST card appropriate (default usually OK)
- [ ] Output file size manageable

**Estimated time:** 30 minutes manual review or 1-2 seconds automated

---

## Targeted Validation Checklists

### Geometry-Focused Checklist

**Use when:** Geometry changes, complex geometry, geometry errors suspected

- [ ] All surfaces defined and used
- [ ] Cell geometry expressions valid
- [ ] Boolean logic correct
- [ ] Complement operators appropriate
- [ ] No overlapping cells
- [ ] No geometry gaps
- [ ] Graveyard properly defined
- [ ] Nested geometries (U/FILL) correct
- [ ] Transformations appropriate
- [ ] Plotted from 3 views (xy, xz, yz)
- [ ] No dashed lines in plots
- [ ] VOID card test passed

**Reference:** mcnp-geometry-checker skill

---

### Material-Focused Checklist

**Use when:** Material changes, new materials, library issues

- [ ] All isotopes valid ZAID format
- [ ] Library versions consistent
- [ ] Thermal scattering (MT) for appropriate materials
- [ ] Temperatures (TMP) in MeV
- [ ] Densities appropriate values
- [ ] Fractions sum correctly
- [ ] Cross-sections available in DATAPATH
- [ ] Natural isotopes vs. specific isotopes appropriate
- [ ] Doppler broadening considered

**Reference:** mcnp-material-builder skill

---

### Physics-Focused Checklist

**Use when:** Physics changes, MODE changes, energy range issues

- [ ] MODE appropriate for problem type
- [ ] PHYS ranges cover source and tallies
- [ ] Cross-section libraries match MODE
- [ ] Secondary production appropriate
- [ ] Energy cutoffs don't eliminate physics
- [ ] Transport approximations appropriate
- [ ] Coupled modes set up correctly

**Reference:** mcnp-physics-validator skill

---

### Criticality-Focused Checklist

**Use when:** Criticality (KCODE) problems

- [ ] KCODE card present (not SDEF)
- [ ] Fissionable materials defined
- [ ] Initial source distribution (KSRC) appropriate
- [ ] Particles per cycle sufficient (>5000)
- [ ] Active cycles sufficient (>100)
- [ ] Skip cycles appropriate (>20)
- [ ] Multiplication factor expected range
- [ ] Eigenvalue statistics converged
- [ ] Shannon entropy converged
- [ ] Source distribution converged

---

### Shielding-Focused Checklist

**Use when:** Shielding, dose calculations

- [ ] Source spectrum accurate
- [ ] Buildup factors included (FM multipliers)
- [ ] Dose conversion factors correct (ANSI/ANS-6.1.1)
- [ ] Geometry includes all shielding layers
- [ ] Material compositions accurate
- [ ] Tally locations appropriate (dose points)
- [ ] Energy bins span full spectrum
- [ ] Variance reduction optimized for deep penetration

---

## Pre-Run Validation Workflow

**Recommended sequence before any MCNP run:**

### Phase 1: Automated Validation (1 minute)

```python
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
results = validator.validate_file('input.inp')

if not results['valid']:
    print("STOP - Fix fatal errors first")
    # Display errors
    exit(1)
```

- [ ] Run automated validator
- [ ] No FATAL errors present
- [ ] Review warnings
- [ ] Note recommendations

### Phase 2: Manual Checks (5 minutes)

- [ ] Review validation warnings
- [ ] Spot-check critical parameters
- [ ] Verify problem setup makes physical sense
- [ ] Check units and magnitudes

### Phase 3: Geometry Verification (10 minutes)

- [ ] Plot geometry: `mcnp6 ip i=input.inp`
- [ ] View from xy plane
- [ ] View from xz plane
- [ ] View from yz plane
- [ ] Zoom into complex regions
- [ ] No dashed lines visible
- [ ] Materials correct in each region
- [ ] Boundaries look correct

### Phase 4: Quick Test Run (optional, 5 minutes)

- [ ] Add VOID card
- [ ] Run with NPS 100000
- [ ] Check for lost particles
- [ ] Fix any geometry errors found
- [ ] Remove VOID card

### Phase 5: Production Run Authorization

- [ ] All validation passed
- [ ] Geometry verified
- [ ] VOID test passed (if performed)
- [ ] Supervisor approval (if required)
- [ ] Documentation complete

**Total pre-run time:** 15-20 minutes (saves hours of debugging)

---

## Post-Run Validation Checklist

**After simulation completes, verify:**

- [ ] Run completed without fatal errors
- [ ] All tallies have results
- [ ] Tally relative errors < 0.05 (< 0.10 acceptable for some)
- [ ] Figure of Merit (FOM) reasonable
- [ ] No excessive lost particles (<0.01%)
- [ ] keff converged (for criticality)
- [ ] Results physically reasonable
- [ ] Results consistent with similar problems

**Reference:** mcnp-statistics-checker skill for detailed statistical validation

---

## Checklist for Modifying Existing Validated Inputs

**When modifying a previously validated input:**

### Major Changes (require full validation)

Changes affecting structure or cross-references:
- [ ] Added/removed cells → Full validation
- [ ] Added/removed surfaces → Full validation
- [ ] Changed materials → Material + cross-reference validation
- [ ] Changed MODE → Full physics validation
- [ ] Changed geometry significantly → Geometry + full validation

### Minor Changes (require targeted validation)

Changes not affecting structure:
- [ ] Changed NPS → No validation needed
- [ ] Changed tally energy bins → Tally validation
- [ ] Changed cell density → Material validation
- [ ] Changed source position → Source + geometry validation
- [ ] Changed importance values → Variance reduction validation

### Documentation Requirements

For all modifications:
- [ ] Document what changed
- [ ] Document why changed
- [ ] Document validation performed
- [ ] Document results comparison (if applicable)

---

## Integration with Builder Skills

**Before validation, ensure input built using:**

- [ ] mcnp-input-builder: Overall structure
- [ ] mcnp-geometry-builder: Cells and surfaces
- [ ] mcnp-material-builder: Material definitions
- [ ] mcnp-source-builder: Source specifications
- [ ] mcnp-tally-builder: Tally definitions
- [ ] mcnp-physics-builder: Physics settings
- [ ] mcnp-lattice-builder: Repeated structures (if applicable)

**Validation verifies that builder outputs are correct and consistent.**

---

## MCNP6 Manual Reference Checklist

**Cross-reference with manual sections:**

- [ ] §3.4.1: Problem setup checklist (22 items)
- [ ] §4.2: Input file format
- [ ] §4.4: Cross-reference requirements
- [ ] §4.7: Input error messages
- [ ] §4.8: Geometry errors
- [ ] Chapter 5: All input cards

---

## Critical Calculation Additional Requirements

**For safety-critical, licensing, or publication calculations:**

- [ ] Independent review by qualified person
- [ ] Benchmark against known solutions
- [ ] Sensitivity analysis performed
- [ ] Uncertainty quantification
- [ ] QA documentation complete
- [ ] Software version documented
- [ ] Cross-section library documented
- [ ] Random number seed documented
- [ ] Results peer-reviewed

---

## Validation Documentation Template

**For each validation performed, document:**

```
MCNP INPUT VALIDATION RECORD

File: [filename]
Date: [date]
Validator: [name]
Validation Level: [Quick / Comprehensive / Targeted]

Checklist Used: [which checklist(s)]
Automated Tools: [Yes/No, which tools]

Results:
  Fatal Errors: [count] - [PASS/FAIL]
  Warnings: [count] - [Acceptable/Addressed]
  Recommendations: [count] - [Noted/Implemented]

Geometry Verification:
  Plotted: [Yes/No]
  Views Checked: [xy/xz/yz]
  VOID Test: [Performed/Not Performed]
  Result: [PASS/FAIL]

Additional Comments:
[Any special considerations, deviations, etc.]

Approved for Run: [YES/NO]
Approver: [name, if applicable]
```

---

**END OF VALIDATION CHECKLISTS**

Use these checklists systematically to ensure high-quality MCNP inputs and reliable simulation results.
