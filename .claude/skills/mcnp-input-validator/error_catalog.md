# MCNP Input Validation Error Catalog

## Overview

This document catalogs common MCNP input validation errors, their causes, fixes, and prevention strategies. Errors are organized by severity level and category.

---

## Error Severity Levels

### FATAL Errors

**Definition:** Errors that prevent MCNP from running or will cause immediate termination.

**Response Required:** MUST fix before any simulation attempt.

**Characteristics:**
- Violate MCNP format requirements
- Prevent parser from reading input
- Cause immediate fatal error messages
- No particles transported

---

### WARNING Conditions

**Definition:** Unconventional settings or potential issues that may need attention.

**Response Required:** Should understand implications before production runs.

**Characteristics:**
- Input is valid but unusual
- May cause unexpected results
- May indicate user error
- MCNP will run but results may be wrong

---

### RECOMMENDATIONS

**Definition:** Best practice suggestions for reliable results.

**Response Required:** Strongly recommended but not required for execution.

**Characteristics:**
- Improve result reliability
- Catch geometry errors early
- Prevent common mistakes
- Based on accumulated user experience

---

## FATAL ERRORS

### F-001: Missing Blank Line Between Blocks

**Error Message:**
```
FATAL: Missing blank line separator between [block1] and [block2]
Expected 2 blank lines in input file, found [N]
```

**Cause:**
MCNP requires EXACTLY 2 blank lines in input file:
- One after Cell Cards block
- One after Surface Cards block

**Example (WRONG):**
```
Simple geometry
1  1  -2.7  -1       $ cell - no blank line following
1  SO  10            $ surface starts immediately
```

**Example (CORRECT):**
```
Simple geometry
1  1  -2.7  -1       $ cell card

1  SO  10            $ blank line before surfaces

MODE N               $ blank line before data cards
```

**Fix:**
1. Count blank lines in input file
2. Identify missing separator
3. Insert blank line at appropriate location
4. Verify exactly 2 blank lines total

**Prevention:**
- Use template files with correct structure
- Validate after every edit
- Use visual markers (comment headers) not blank lines for readability

**Reference:** MCNP6 Manual §4.2

---

### F-002: Extra Blank Lines Within Block

**Error Message:**
```
FATAL: Extra blank lines detected in [block] block
Lines [N1, N2, ...] are blank - MCNP will ignore subsequent cards
```

**Cause:**
Blank lines within a block cause MCNP to stop reading that block. Cards after the blank line are ignored or misinterpreted.

**Example (WRONG):**
```
1  1  -2.7  -1
2  2  -1.0  1 -2

3  0  2             $ This line will be ignored due to blank above
```

**Example (CORRECT):**
```
1  1  -2.7  -1
2  2  -1.0  1 -2
3  0  2             $ No blank line above
```

**Fix:**
1. Identify blank lines within blocks
2. Remove all blank lines within each block
3. Use comment lines (c) for visual separation if needed

**Prevention:**
- Never use blank lines for readability within blocks
- Use comment headers instead: `c ==================`
- Validate after editing

**Reference:** MCNP6 Manual §4.2, Lesson #11 in LESSONS-LEARNED.md

---

### F-003: Missing Title Card

**Error Message:**
```
FATAL: Title card missing
First line of input must be title card
```

**Cause:**
MCNP requires a title card as the first line (or first line after MESSAGE card).

**Example (WRONG):**
```
1  1  -2.7  -1      $ Missing title - starts with cell card
```

**Example (CORRECT):**
```
Simple Sphere Geometry
1  1  -2.7  -1      $ Title present on line 1
```

**Fix:**
1. Add descriptive title as first line
2. Title can be any text (not blank)
3. No continuation allowed on title

**Prevention:**
- Always start with title card
- Make title descriptive for future reference

**Reference:** MCNP6 Manual §4.2.1

---

### F-004: Undefined Surface in Cell Geometry

**Error Message:**
```
FATAL: Cell [N] geometry references undefined surface [M]
Location: Cell [N] definition
Geometry expression contains surface [M] but no surface card exists
```

**Cause:**
Cell geometry expression references a surface number that has no corresponding surface card definition.

**Example (WRONG):**
```
10  1  -2.7  -1 2 -3   $ References surfaces 1, 2, 3

1  PZ  0
2  PZ  10              $ Surface 3 is MISSING
```

**Example (CORRECT):**
```
10  1  -2.7  -1 2 -3

1  PZ  0
2  PZ  10
3  CZ  5               $ Surface 3 defined
```

**Fix:**
1. Identify missing surface number from error
2. Add surface card definition
3. Verify surface type and parameters appropriate
4. Re-validate cross-references

**Prevention:**
- Build geometry systematically
- Define all surfaces before referencing in cells
- Use cross-reference checker

**Reference:** MCNP6 Manual §4.4, mcnp-geometry-builder skill

---

### F-005: Undefined Material in Cell Definition

**Error Message:**
```
FATAL: Cell [N] uses material [M], but M[M] card not defined
Location: Cell [N] has m=[M] but no M[M] material specification
```

**Cause:**
Cell specifies a material number but no M card exists for that material.

**Example (WRONG):**
```
10  5  -2.7  -1        $ Uses material 5

M1  92235.80c  1.0     $ Only M1 defined, M5 missing
```

**Example (CORRECT):**
```
10  5  -2.7  -1        $ Uses material 5

M1  92235.80c  1.0
M5  13027.80c  1.0     $ M5 defined
```

**Fix:**
1. Identify missing material number
2. Add M card for that material
3. Define appropriate isotopes and fractions
4. Add MT card if thermal material

**Prevention:**
- Define all materials before assignment
- Use material library builder
- Validate cross-references

**Reference:** MCNP6 Manual §5.6, mcnp-material-builder skill

---

### F-006: IMP Card Entry Count Mismatch

**Error Message:**
```
FATAL: IMP:[particle] card has [N] entries but [M] cells exist
Missing importance for cells: [list]
```

**Cause:**
Importance card must have exactly one entry per cell. Count mismatch is fatal.

**Example (WRONG):**
```
1  1  -2.7  -1
2  2  -1.0  1 -2
3  0  2               $ 3 cells

IMP:N  1 1            $ Only 2 entries - FATAL
```

**Example (CORRECT):**
```
1  1  -2.7  -1
2  2  -1.0  1 -2
3  0  2               $ 3 cells

IMP:N  1 1 0          $ 3 entries - correct
```

**Fix:**
1. Count cells in input
2. Count IMP card entries
3. Add missing entries (or remove extra)
4. For graveyard: IMP=0
5. For active regions: IMP=1 (or higher for variance reduction)

**Prevention:**
- Update IMP cards when adding/removing cells
- Use systematic cell numbering
- Use R (repeat) shortcut: `IMP:N  1 5R 0` = 1 1 1 1 1 1 0

**Reference:** MCNP6 Manual §3.2.5.2

---

### F-007: Undefined Universe in FILL

**Error Message:**
```
FATAL: Cell [N] FILL=[M] references undefined universe [M]
No cells have U=[M] parameter
```

**Cause:**
FILL card references a universe number but no cells have been assigned to that universe.

**Example (WRONG):**
```
1  0  -1  FILL=5      $ References universe 5

10  1  -2.7  -2  U=1  $ Only universe 1 defined, not 5
```

**Example (CORRECT):**
```
1  0  -1  FILL=5      $ References universe 5

10  1  -2.7  -2  U=5  $ Universe 5 defined
```

**Fix:**
1. Identify referenced universe number
2. Verify cells with that U parameter exist
3. Or correct FILL reference to existing universe

**Prevention:**
- Define universe cells before filling
- Use systematic universe numbering
- Validate lattice structures thoroughly

**Reference:** MCNP6 Manual §5.5.2, mcnp-lattice-builder skill

---

### F-008: Undefined Transformation Reference

**Error Message:**
```
FATAL: TRCL=[N] references undefined transformation [N]
No TR[N] or *TR[N] card exists
```

**Cause:**
Cell or surface references a transformation number that has no TR card definition.

**Example (WRONG):**
```
10  1  -2.7  -1  TRCL=5   $ References TR5

TR1  0 0 0               $ Only TR1 defined, not TR5
```

**Example (CORRECT):**
```
10  1  -2.7  -1  TRCL=5   $ References TR5

TR5  10 0 0              $ TR5 defined
```

**Fix:**
1. Identify referenced transformation number
2. Add TR card with appropriate parameters
3. Or correct TRCL reference

**Prevention:**
- Define transformations before use
- Use systematic TR numbering
- Document transformation purpose

**Reference:** MCNP6 Manual §5.5.1, mcnp-transform-editor skill

---

### F-009: MODE Card Missing

**Error Message:**
```
FATAL: MODE card missing
Must specify particle type(s) for transport
```

**Cause:**
Every MCNP input must have MODE card specifying particle types.

**Example (WRONG):**
```
c Data cards
NPS  10000            $ MODE missing - FATAL
```

**Example (CORRECT):**
```
c Data cards
MODE N                $ MODE specified
NPS  10000
```

**Fix:**
1. Add MODE card in data block
2. Specify appropriate particle(s):
   - MODE N (neutron)
   - MODE P (photon)
   - MODE N P (coupled)
   - MODE E (electron)
   - MODE N P E (all three)

**Prevention:**
- Use template with MODE card
- MODE should be early in data block

**Reference:** MCNP6 Manual §5.7.1, mcnp-physics-builder skill

---

### F-010: Invalid ZAID Format

**Error Message:**
```
FATAL: Invalid ZAID format in material [N]: [ZAID]
Format must be ZZZAAA.XXc (e.g., 92235.80c)
```

**Cause:**
Material specification uses invalid isotope identifier format.

**Example (WRONG):**
```
M1  92235  1.0        $ Missing library suffix
M2  92235.80  1.0     $ Missing particle type (c)
M3  U235.80c  1.0     $ Element symbol not allowed
```

**Example (CORRECT):**
```
M1  92235.80c  1.0    $ ZZZ=92 (U), AAA=235, library=80, type=c
M2  92238.80c  4.0
```

**Fix:**
1. Identify invalid ZAID
2. Convert to ZZZAAA.XXc format:
   - ZZZ = atomic number (1-118)
   - AAA = mass number (235, 238, etc.) or 000 for natural
   - XX = library version (80, 70, etc.)
   - c = particle type (c=neutron, p=photon, e=electron)

**Prevention:**
- Use material builder skill
- Reference isotope tables
- Consistent library versions

**Reference:** MCNP6 Manual §5.6.1, mcnp-material-builder skill

---

## WARNING CONDITIONS

### W-001: No Thermal Scattering for Light Materials

**Warning Message:**
```
WARNING: Material [N] appears to contain hydrogen but no MT[N] card
Recommend adding S(α,β) thermal scattering for accurate thermal results
```

**Cause:**
Materials with hydrogen (especially water, polyethylene) should have thermal scattering treatment for thermal neutron problems.

**Example (NEEDS MT CARD):**
```
M1  1001.80c  2       $ H in H2O
    8016.80c  1       $ O in H2O
c Missing: MT1  lwtr.20t
```

**Example (CORRECT):**
```
M1  1001.80c  2       $ H in H2O
    8016.80c  1       $ O in H2O
MT1  lwtr.20t         $ Light water thermal scattering
```

**Impact:**
- Underestimate thermal neutron scattering
- Incorrect reaction rates at low energies
- Wrong flux spectrum in thermal regions

**Fix:**
Add appropriate MT card:
- `lwtr.20t` - Light water (H2O)
- `hwtr.20t` - Heavy water (D2O)
- `poly.20t` - Polyethylene
- `grph.20t` - Graphite

**Reference:** MCNP6 Manual §5.6.2, mcnp-material-builder skill

---

### W-002: TMP Card Value Looks Like Kelvin

**Warning Message:**
```
WARNING: TMP[N]=[value] - Temperature should be in MeV, not Kelvin
Did you mean [converted value] MeV (for [value] K)?
```

**Cause:**
Common mistake: TMP card expects MeV but users often input Kelvin.

**Example (WRONG):**
```
M1  92235.80c  1.0
TMP1  300             $ This is 300 MeV (227 MILLION Kelvin!)
```

**Example (CORRECT):**
```
M1  92235.80c  1.0
TMP1  2.53e-8         $ 300 K = 2.53e-8 MeV (kT at 300K)
```

**Conversion:**
```
kT (MeV) = k * T(K) / (e * 1e6)
         = 8.617e-5 * T(K) / 1e6
         = 8.617e-11 * T(K)

For 300 K: 8.617e-11 * 300 = 2.585e-8 MeV
```

**Common temperatures:**
- 300 K = 2.53e-8 MeV (room temperature)
- 600 K = 5.17e-8 MeV
- 900 K = 7.76e-8 MeV

**Fix:**
1. If value > 1: Likely Kelvin, convert to MeV
2. Use formula: MeV = 8.617e-11 * K

**Reference:** MCNP6 Manual §5.6.3

---

### W-003: No Importance Cards Specified

**Warning Message:**
```
WARNING: No importance cards (IMP) found
Particles may be trapped in geometry with no escape
```

**Cause:**
Without importance cards, all cells have default importance=1, including graveyard. Particles cannot escape.

**Impact:**
- Simulation may never terminate
- No particles reach tallies
- Waste computation in unimportant regions

**Fix:**
Add importance cards for all particle types:
```
IMP:N  1 1 1 0       $ Last cell (graveyard) has IMP=0
IMP:P  1 1 1 0       $ If MODE N P
```

**Reference:** MCNP6 Manual §3.2.5.2, mcnp-variance-reducer skill

---

### W-004: PHYS Energy Range May Not Cover Source

**Warning Message:**
```
WARNING: PHYS:[particle] emax=[value] may be less than source maximum energy
Verify source energies are within physics range
```

**Cause:**
Source can emit particles above the physics energy cutoff, causing immediate termination.

**Example (QUESTIONABLE):**
```
SDEF  ERG=14.1        $ 14.1 MeV source
PHYS:N  10            $ emax = 10 MeV - too low!
```

**Example (CORRECT):**
```
SDEF  ERG=14.1        $ 14.1 MeV source
PHYS:N  20            $ emax = 20 MeV - adequate
```

**Fix:**
Set PHYS emax ≥ maximum source energy (with margin).

**Reference:** MCNP6 Manual §5.7.2, mcnp-physics-builder skill

---

### W-005: Mixed Cross-Section Libraries

**Warning Message:**
```
WARNING: Materials use mixed cross-section libraries
M[N1] uses .80c, M[N2] uses .70c
Recommend consistent library version for all materials
```

**Cause:**
Mixing ENDF/B-VII.0 (.70c) and ENDF/B-VIII.0 (.80c) can cause inconsistencies.

**Impact:**
- Potential physics inconsistencies
- Difficult to defend results
- Different thermal scattering treatments

**Fix:**
Use consistent library version:
```
c CORRECT - All .80c:
M1  92235.80c  1.0
M2  1001.80c   2.0
M3  8016.80c   1.0
```

**Reference:** MCNP6 Manual §5.6.1

---

## RECOMMENDATIONS

### R-001: Plot Geometry Before Running

**Recommendation:**
```
ESSENTIAL: Plot geometry from multiple views before running simulation
Command: mcnp6 ip i=input.inp
```

**Reason:**
Geometry errors (overlaps, gaps) cannot be detected by input validation. Plotting shows:
- Dashed lines indicate geometry errors
- Cell boundaries and materials
- Overall geometry sanity check

**How to plot:**
1. Run: `mcnp6 ip i=input.inp`
2. Opens MCNP plotter
3. View from multiple angles (xy, xz, yz planes)
4. Look for dashed lines (indicate errors)
5. Zoom into complex regions

**Reference:** MCNP6 Manual Chapter 6, §3.4.1 item #2

---

### R-002: Use VOID Card for Geometry Testing

**Recommendation:**
```
Test geometry with VOID card before production run
Add: VOID
Run with high NPS to find overlaps/gaps quickly
```

**Reason:**
VOID card causes MCNP to terminate immediately when particle enters undefined space or overlap. Fast way to find geometry errors.

**How to use:**
1. Add `VOID` card to data block
2. Run with `NPS 100000` or higher
3. Check output for lost particles
4. Fix any geometry errors found
5. Remove VOID card for production

**Reference:** MCNP6 Manual §3.2.8

---

### R-003: Verify Cross-Section Library Loading

**Recommendation:**
```
After run starts, check output file for loaded cross-sections
Verify all isotopes loaded from intended library version
```

**Reason:**
MCNP searches DATAPATH for cross-sections. May load wrong version if path not set correctly.

**What to check:**
```
Look in output file for:
  Tables from file /path/to/endf80/...
Verify all materials loaded from correct library
```

**Reference:** MCNP6 Manual §3.4.1 item #14

---

### R-004: Pre-Calculate Volumes/Masses

**Recommendation:**
```
Calculate expected cell volumes and masses before running
Compare with MCNP-calculated values for verification
```

**Reason:**
Significant discrepancy indicates geometry error (overlap, gap, wrong dimensions).

**How to use:**
1. Calculate analytical volumes
2. Add `VOL` card or let MCNP calculate
3. Compare results
4. Investigate if difference > 1%

**Reference:** MCNP6 Manual §3.4.1 item #3

---

### R-005: Check Statistical Quality After Run

**Recommendation:**
```
After run completes, check tally statistics
Verify relative error < 0.05 for reliable results
Use mcnp-statistics-checker skill
```

**Reason:**
Input validation cannot predict convergence. Must check output statistics.

**Reference:** mcnp-statistics-checker skill

---

## Error Prevention Strategies

### Strategy 1: Use Template Files

Start from validated templates with correct structure:
- Three-block format
- Correct blank line count
- Basic required cards (MODE, IMP, NPS)

### Strategy 2: Incremental Validation

Validate after each major edit:
- Add new cells → validate geometry
- Change materials → validate cross-references
- Modify physics → validate consistency

### Strategy 3: Systematic Build Process

Follow builder skill workflows:
1. Use mcnp-input-builder for overall structure
2. Use mcnp-geometry-builder for cells/surfaces
3. Use mcnp-material-builder for materials
4. Use mcnp-source-builder for sources
5. Use mcnp-tally-builder for tallies
6. Use mcnp-physics-builder for physics settings
7. Validate before running

### Strategy 4: Automated Validation

Use Python validation scripts before every run:
```python
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
results = validator.validate_file('input.inp')

if not results['valid']:
    print("FIX ERRORS BEFORE RUNNING")
    exit(1)
```

### Strategy 5: Peer Review

For critical calculations:
- Have colleague review input
- Run validation checklist
- Verify against similar validated inputs
- Document assumptions

---

## Validation Workflow Integration

**Recommended workflow:**

```
1. Build input using builder skills
2. Validate with mcnp-input-validator
3. Fix any FATAL errors
4. Review warnings
5. Plot geometry (ESSENTIAL)
6. Run with VOID card (RECOMMENDED)
7. Fix any geometry errors
8. Run production calculation
9. Check output statistics
```

---

**END OF ERROR CATALOG**
