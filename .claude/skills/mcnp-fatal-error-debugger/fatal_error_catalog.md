# MCNP Fatal Error Catalog

**Purpose:** Comprehensive reference of MCNP fatal error messages, their causes, and fixes.

**Companion to:** mcnp-fatal-error-debugger SKILL.md

---

## Error Message Hierarchy

MCNP error messages follow a four-level hierarchy that determines severity and required action.

### Fatal Errors

**Characteristics:**
- Terminate MCNP before running any particles
- Printed to terminal and OUTP file
- First fatal error is always the real issue
- Subsequent fatal errors often artifacts of first error

**Action Required:**
1. Fix the **first** fatal error only
2. Re-run MCNP to check if others remain
3. Repeat until all resolved

**Example:**
```
fatal error.  material   3 has not been specified but is used in cell    5.
fatal error.  cell   5 has invalid material specification.
fatal error.  importance not set for cell 5.
```
Fix first error (add M3 card) → subsequent errors likely disappear.

### BAD TROUBLE Messages

**Characteristics:**
- Terminate MCNP immediately before catastrophic failure
- Occur during particle transport
- Usually indicate serious input errors or code instability

**Common Causes:**
- Divide by zero (zero volume, zero energy bin width)
- Array bounds exceeded (too many particles, invalid indices)
- Invalid memory access (corrupted geometry, transformation errors)
- Numerical instabilities

**Action Required:**
1. Examine BAD TROUBLE message for subroutine name
2. Identify input specification causing instability
3. Fix root cause in input
4. Re-run

### Warning Messages

**Characteristics:**
- Non-fatal but require attention
- Indicate unconventional parameters or questionable conditions
- May cause incorrect results if ignored

**Action Required:**
1. Read warning message
2. Understand significance
3. Verify parameter is intentional
4. If unintentional, correct input

### Comment Messages

**Characteristics:**
- Informational only
- Relay useful additional information
- No action required

**Example:**
```
comment.  total fission nubar used.
comment.  universe map (non-default) for cell   1:  u=  10
```

---

## Fatal Error Categories

### Category 1: Input Syntax Errors

Errors detected during input file parsing phase.

#### 1.1 Invalid Card Name

**Error:**
```
fatal error.  unrecognized data card name:  SDEFF
```

**Cause:** Typo in card name (SDEFF instead of SDEF)

**Fix:**
```
c WRONG:
SDEFF  POS=0 0 0  ERG=14.1

c CORRECT:
SDEF  POS=0 0 0  ERG=14.1
```

#### 1.2 Invalid Card Format

**Error:**
```
fatal error.  bad format on card line    45.
```

**Cause:** Card format doesn't match specification (wrong number of parameters, invalid syntax)

**Fix:** Verify card format against Chapter 5 specification for that card type.

#### 1.3 Invalid Parameter Value

**Error:**
```
fatal error.  negative volume specified for cell   3.
```

**Cause:** Parameter value outside valid range

**Fix:**
```
c WRONG:
VOL  -10  20  30

c CORRECT:
VOL  10  20  30
```

### Category 2: Cross-Reference Errors

Errors where one card references undefined entity.

#### 2.1 Material Not Defined

**Error:**
```
fatal error.  material   3 has not been specified but is used in cell    5.
```

**Cause:** Cell 5 references material 3, but M3 card missing

**Fix:**
```
c Add missing material card:
M3  82000.80c  1.0                      $ Lead
```

**Common Variations:**
- `material   0 is specified for cell X` → Should be void (density 0) or material number
- `material  X  has been specified more than once` → Duplicate M card

#### 2.2 Surface Not Found

**Error:**
```
fatal error.  surface    15 of cell    2 is not defined in the surface card section.
```

**Cause:** Cell references non-existent surface

**Fix Option 1** (Surface typo):
```
c WRONG: Cell references surface 15 (doesn't exist)
2  1  -1.0  1 -15  IMP:N=1

c CORRECT: Change to surface 2
2  1  -1.0  1 -2  IMP:N=1
```

**Fix Option 2** (Define missing surface):
```
c Add missing surface definition:
15  SO  20
```

#### 2.3 Tally References Undefined Entity

**Error:**
```
fatal error.  surface   10 on f2:n tally not defined.
```

**Cause:** F2 tally references surface 10, which doesn't exist

**Fix:**
```
c Either define surface 10:
10  PX  50

c Or correct tally to use existing surface:
F2:N  1                                 $ Use surface 1
```

#### 2.4 Transformation Not Defined

**Error:**
```
fatal error.  transformation    5 has not been specified but is used.
```

**Cause:** Surface or cell uses *TR5 or TR5, but TR5/TRCL5 card missing

**Fix:**
```
c Add missing transformation:
*TR5  10 0 0  0 1 0  1 0 0  0 0 1      $ Translation + rotation
```

### Category 3: Material and Cross-Section Errors

Errors related to material definitions and nuclear data.

#### 3.1 ZAID Not in xsdir

**Error:**
```
warning.  nuclide  92235.80c is not available on the xsdir file.
fatal error.  stopping in subroutine mcrun.
```

**Causes:**
1. ZAID not installed (library missing)
2. Typo in ZAID (92235.80c vs 92235.08c)
3. Wrong library suffix (.80c vs .70c)
4. DATAPATH environment variable incorrect

**Diagnosis:**
```bash
# Check DATAPATH
echo $DATAPATH

# Search xsdir for ZAID
grep "92235.80c" $DATAPATH/xsdir
```

**Fix Option 1** (Use different library):
```
M1  92235.70c  0.03  92238.70c  0.97    $ ENDF/B-VII.0
```

**Fix Option 2** (Version-agnostic):
```
M1  92235.00c  0.03  92238.00c  0.97    $ Latest available
```

**Fix Option 3** (Install library):
Contact administrator to install ENDF/B-VIII.0 libraries.

#### 3.2 Invalid ZAID Format

**Error:**
```
fatal error.  invalid zaid  920350.80c on material card.
```

**Cause:** ZAID format incorrect (920350 vs 92235)

**Fix:**
```
c WRONG:
M1  920350.80c  1.0

c CORRECT:
M1  92235.80c  1.0
```

ZAID format: ZZZAAA.XXy
- ZZZ = atomic number (92 for U)
- AAA = mass number (235 for U-235)
- XX = library version (80 = ENDF/B-VIII.0)
- y = particle type (c = continuous-energy neutron)

#### 3.3 Invalid Material Fraction

**Error:**
```
fatal error.  sum of material fractions does not equal unity.
```

**Cause:** Atom or weight fractions don't sum to 1.0

**Fix:**
```
c WRONG:
M1  1001.80c  2.0  8016.80c  1.5       $ Sum = 3.5

c CORRECT (normalize):
M1  1001.80c  0.667  8016.80c  0.333   $ Sum = 1.0
```

### Category 4: Source Specification Errors

Errors in SDEF, KCODE, and source distribution cards.

#### 4.1 Impossible Source Variable Dependencies

**Error:**
```
fatal error. impossible source variable dependencies.
```

**Cause:** Invalid dependency in SDEF (e.g., AXS=FPOS, SUR=FPOS)

**Fix:**
```
c WRONG:
SDEF  POS=D1  AXS=FPOS=D2             $ AXS can't depend on POS

c CORRECT:
SDEF  POS=D1  AXS=0 0 1               $ Fixed axis
```

**Invalid Dependencies:**
- AXS = FPOS(POS) → Axis cannot depend on position
- SUR = FPOS(POS) → Surface cannot depend on position
- Many others documented in Source Primer

#### 4.2 Source Outside Geometry

**Error:**
```
fatal error. source particle not in any cell.
bad trouble in subroutine sourcc of mcrun
```

**Cause:** SDEF position is outside geometry or in void cell

**Diagnosis:**
```
c Check SDEF position:
SDEF  POS=100 200 300  ERG=14.1        $ Is (100,200,300) inside geometry?
```

**Fix:**
```
c Verify source position is inside defined cell:
SDEF  POS=0 0 0  ERG=14.1              $ Check if (0,0,0) is in a cell
```

**Verification with MCNP Plotter:**
```
IP  0 0 0                               $ Plot at source location
# Verify point is inside a defined cell
```

#### 4.3 Invalid Energy Distribution

**Error:**
```
fatal error. energy distribution has zero bin width.
bad trouble in subroutine source - divide by zero
```

**Cause:** SI histogram has adjacent identical energies

**Fix:**
```
c WRONG:
SI1  H  0  0  1                        $ Zero width bin (0 to 0)

c CORRECT:
SI1  H  0  0.1  1  10                  $ Non-zero widths
SP1     0  1    1  0
```

#### 4.4 Source on Surface Ambiguity

**Error:**
```
fatal error. source position on surface   1 is ambiguous.
```

**Cause:** Source positioned exactly on surface boundary

**Fix:**
```
c WRONG:
SDEF  POS=10 0 0  ERG=14.1             $ Exactly on sphere surface (R=10)
1  SO  10

c CORRECT (offset slightly):
SDEF  POS=10.001 0 0  ERG=14.1         $ Just inside or outside

c OR use surface source:
SDEF  SUR=1  NRM=-1  ERG=14.1          $ Explicit surface source
```

### Category 5: Geometry Errors

Errors detected during particle transport due to geometry issues.

#### 5.1 Lost Particle - Overlap

**Error:**
```
bad trouble in subroutine track of mcrun
  source particle no.       1234
  particle lost at point:
    x =   5.12345
    y =   3.67890
    z =   0.00000
  in cell    2
```

**Cause:** Two or more cells claim same physical space (overlap)

**Diagnosis:**
1. Note lost particle coordinates
2. Examine event log for particle path
3. Plot geometry at lost location:
   ```
   IP  5.12 3.69 0
   ```
4. Look for overlapping cell definitions

**Common Patterns:**
```
c WRONG (cell 2 encloses cell 1 - overlap):
1  1  -1.0  -1  IMP:N=1                $ Sphere R=10
2  2  -2.3  -2  IMP:N=1                $ Sphere R=12 (overlaps!)

c CORRECT (cell 2 is shell):
1  1  -1.0  -1  IMP:N=1                $ Inner sphere
2  2  -2.3  1 -2  IMP:N=1              $ Shell between R=10 and R=12
```

#### 5.2 Lost Particle - Gap

**Error:**
```
bad trouble in subroutine track of mcrun
  particle lost at point:
    x =  10.00001
    y =   0.00000
    z =   0.00000
  no cell found at position   10.00001   0.00000   0.00000
```

**Cause:** Space exists but no cell defined there (gap in geometry)

**Diagnosis:**
1. "No cell found" = gap (vs "in cell X" = overlap)
2. Note coordinates of gap
3. Plot geometry at location
4. Identify missing cell definition

**Fix:**
```
c WRONG (gap between R=10 and R=12):
1  1  -1.0  -1  IMP:N=1                $ Inside R=10
2  2  -2.3  2  IMP:N=1                 $ Outside R=12 (GAP: R=10 to R=12)

c CORRECT (add cell for gap region):
1  1  -1.0  -1  IMP:N=1                $ Inside R=10
2  0        1 -2  IMP:N=1              $ Gap region (void)
3  2  -2.3  2  IMP:N=1                 $ Outside R=12
```

#### 5.3 Lost Particle - Wrong Surface Sense

**Error:**
```
particle lost at   10.00000   0.00000   0.00000
on surface     1
```

**Cause:** Cell definition has incorrect surface sense (+ vs -)

**Fix:**
```
c WRONG (both cells inside surface 1):
1  1  -1.0  -1  IMP:N=1                $ Inside R=10
2  2  -2.3  -1 -2  IMP:N=1             $ Also inside R=10? (WRONG)

c CORRECT (cell 2 outside surface 1):
1  1  -1.0  -1  IMP:N=1                $ Inside R=10
2  2  -2.3  1 -2  IMP:N=1              $ Between R=10 and R=20
```

### Category 6: Importance and Particle Transport Errors

#### 6.1 Importance Not Set

**Error:**
```
fatal error.  importance not set for cell   5.
```

**Cause:** IMP:N (or other particle) card missing entry for cell 5

**Fix:**
```
c WRONG (only 4 entries, but cell 5 exists):
IMP:N  1  2  4  0

c CORRECT (add entry for cell 5):
IMP:N  1  2  4  8  0                   $ Added importance 8 for cell 5
```

**Note:** Number of IMP entries must equal number of cells (including graveyard).

#### 6.2 Weight Window Error

**Error:**
```
bad trouble in subroutine wwg of mcrun
  particle weight exceeds weight window bounds
```

**Cause:** Weight window values incompatible or incorrectly specified

**Temporary Fix** (test if VR is problem):
```
c Comment out weight windows:
c WWP:N  J  J  J  0  -1
c WWN:N  [values]
```

**Permanent Fix:**
- Regenerate weight windows with correct settings
- Verify WWN/WWE/WWP cards consistent
- Check mesh dimensions match geometry

### Category 7: MODE and Physics Errors

#### 7.1 Inconsistent MODE

**Error:**
```
fatal error.  particle mode includes photons but no material uses photon cross sections.
```

**Cause:** MODE includes particle type not supported by materials

**Fix:**
```
c WRONG:
MODE  N P                              $ Neutron + photon
M1  1001.80c  2  8016.80c  1          $ Only neutron xsecs

c CORRECT (add photon xsecs):
MODE  N P
M1  1001.80c  2  8016.80c  1          $ Neutron
     1000.04p  2  8000.04p  1          $ Photon (added)
```

#### 7.2 Invalid PHYS Card

**Error:**
```
fatal error.  invalid parameter on phys:n card.
```

**Cause:** PHYS card parameter out of valid range

**Fix:**
```
c WRONG:
PHYS:N  50                             $ Energy cutoff too high

c CORRECT:
PHYS:N  20                             $ Valid range typically 1-20 MeV
```

---

## Quick Reference: Most Common Fatal Errors

| Error Pattern | Likely Cause | First Action |
|---------------|--------------|--------------|
| "material X not defined" | Missing M card | Add MX card |
| "surface X not defined" | Missing surface | Add surface X or fix cell reference |
| "particle lost" | Geometry overlap or gap | Plot at lost location |
| "impossible source variable dependencies" | Invalid SDEF dependency | Remove AXS=FPOS or SUR=FPOS |
| "ZAID not in xsdir" | Library not available | Try .70c or .00c suffix |
| "divide by zero" | Zero bin width or volume | Check SI histograms and volumes |
| "bad trouble in track" | Geometry error during transport | Use VOID card test |
| "importance not set" | IMP card missing entries | Add IMP entries for all cells |
| "no cell found at position" | Gap in geometry | Define cell for that region |
| "unrecognized data card" | Typo in card name | Fix card name spelling |

---

## Error Frequency Analysis

Based on common user experiences:

**Most Frequent (>50% of fatal errors):**
1. Material not defined (M card missing)
2. Surface not defined (typo or missing)
3. Lost particle (geometry overlap/gap)
4. ZAID not in xsdir (library version issue)

**Moderately Frequent (20-50%):**
5. Importance not set (IMP card incomplete)
6. Source outside geometry (SDEF position wrong)
7. Invalid dependencies (source specification)
8. Tally references undefined surface/cell

**Less Frequent (<20%):**
9. BAD TROUBLE divide by zero
10. Transformation errors
11. MODE/physics inconsistencies
12. Card format errors

---

## Cascading Errors

**Key Principle:** First fatal error is real, subsequent may be artifacts.

**Example Cascade:**
```
fatal error.  material   3 has not been specified but is used in cell    5.
fatal error.  cell   5 has invalid material specification.
fatal error.  importance not set for cell 5.
fatal error.  volume not calculated for cell 5.
[... 10 more errors ...]
```

**Root Cause:** Only first error (M3 missing)

**Fix:** Add M3 card → all subsequent errors disappear

**Strategy:**
1. Read ONLY first fatal error
2. Fix that one issue
3. Re-run MCNP
4. Check if other errors remain
5. Repeat until clean

---

## Platform-Specific Errors

### Windows-Specific

**Error:**
```
fatal error.  could not open file: C:\path\to\xsdir
```

**Cause:** Path contains spaces or special characters

**Fix:**
```
# Use 8.3 format or quotes:
DATAPATH="C:\Program Files\MCNP\data"
```

### Linux-Specific

**Error:**
```
fatal error.  DATAPATH not set
```

**Cause:** Environment variable not defined

**Fix:**
```bash
export DATAPATH=/usr/local/mcnp/data
```

### Cluster/Parallel Specific

**Error:**
```
fatal error.  MPI initialization failed
```

**Cause:** Parallel execution environment not configured

**Fix:**
```bash
# Check MPI installation
which mpirun

# Use correct MPI wrapper
mpirun -np 8 mcnp6 inp=input.i
```

---

## References

**MCNP Documentation:**
- Chapter 4 §4.7: Input Error Messages
- Chapter 4 §4.8: Geometry Errors
- Chapter 3: Sample Problems (debugging examples)
- Source Primer Chapter 5: Known Source Errors

**Related Files:**
- geometry_error_guide.md (detailed geometry debugging)
- source_error_guide.md (SDEF error details)
- bad_trouble_guide.md (BAD TROUBLE messages)
- debugging_workflow.md (systematic procedures)

**Related Skills:**
- mcnp-input-validator (pre-run validation)
- mcnp-geometry-checker (geometry validation)
- mcnp-output-parser (error extraction)

---

**END OF FATAL ERROR CATALOG**
