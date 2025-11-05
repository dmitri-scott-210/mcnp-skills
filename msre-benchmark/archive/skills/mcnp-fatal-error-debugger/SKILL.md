---
category: C
name: mcnp-fatal-error-debugger
description: Diagnose and fix MCNP fatal errors including geometry errors, input syntax errors, source problems, and BAD TROUBLE messages
activation_keywords:
  - fatal error
  - bad trouble
  - mcnp crashed
  - lost particle
  - geometry error
  - debug error
  - fix error
  - error message
  - mcnp failed
---

# MCNP Fatal Error Debugger Skill

## Purpose

This skill guides users in diagnosing and fixing fatal errors in MCNP simulations. Fatal errors terminate MCNP before or during particle transport, preventing completion of the calculation. This skill covers input validation errors, geometry errors (lost particles, overlaps, gaps), source specification errors, BAD TROUBLE messages, and systematic debugging procedures to identify and correct issues efficiently.

## When to Use This Skill

- MCNP terminates with "fatal error" message before running particles
- Simulation crashes with "BAD TROUBLE" message during execution
- Particles get lost due to geometry errors (overlaps or gaps)
- Source specification produces "impossible source variable dependencies"
- Material or cross-section errors prevent startup
- Input syntax errors block execution
- MCNP terminates unexpectedly without completing
- Need to systematically debug complex input files
- Geometry plotting shows dashed lines (potential issues)
- Event log indicates particle tracking problems

## Prerequisites

- **mcnp-input-validator**: Understanding of input structure validation
- **mcnp-geometry-checker**: Geometry validation concepts
- **mcnp-input-builder**: Basic input file structure
- Ability to read MCNP output file (outp)
- Understanding of MCNP error message types (fatal, warning, comment, BAD TROUBLE)

## Core Concepts

### Error Message Hierarchy

**Fatal Errors**:
- Terminate MCNP before running any particles
- Printed to terminal and OUTP file
- First fatal error is always real
- Subsequent fatal errors may be artifacts of first error
- **Action**: Fix first fatal error, then re-run to check if others remain

**BAD TROUBLE Messages**:
- Terminate MCNP immediately before catastrophic failure
- Usually indicate:
  - Divide by zero
  - Array bounds exceeded
  - Invalid memory access
  - User input errors causing code instability
- **Action**: Examine BAD TROUBLE message, fix root cause in input

**Warning Messages**:
- Non-fatal but require attention
- Indicate unconventional parameters or conditions
- May cause incorrect results if ignored
- **Action**: Understand significance, verify intentional

**Comment Messages**:
- Informational only
- Relay useful additional information
- **Action**: Read and understand, usually no action needed

### Geometry Error Types

**Lost Particle**:
- Particle cannot determine which cell it occupies
- Caused by:
  - Overlapping cells (two cells claim same space)
  - Gaps between cells (no cell defined for space)
  - Incorrect surface sense
  - Transformation errors

**Overlapping Cells**:
- Two or more cells define the same physical space
- Particle enters region claimed by multiple cells
- Code cannot determine correct cell

**Gaps Between Cells**:
- Space exists but no cell is defined there
- Particle enters undefined region
- Often at cell boundaries or complex intersections

**Dashed Lines in Plots**:
- Indicate potential geometry issues
- Appear when not exactly one cell on each side of surface
- May also appear for legitimate reasons (plot plane coincident, DXTRAN spheres)

### Error Detection Timing

**Input Processing Phase** (before particle transport):
- Syntax errors
- Invalid card names or parameters
- Cross-reference errors (material not defined, surface not found)
- Particle mode issues

**Particle Transport Phase** (during execution):
- Geometry errors (lost particles)
- Numerical instabilities
- Weight window issues
- Tally errors

## Decision Tree: Debugging Fatal Errors

```
START: MCNP Fatal Error Occurred
  |
  +--> Error before any particles run?
  |      |
  |      +--> YES: Input Phase Error
  |      |      ├─> Read first fatal error in OUTP
  |      |      ├─> Check error type:
  |      |      |    ├─> Syntax error → Fix card format (§5.X reference)
  |      |      |    ├─> Cross-reference error → Verify material/surface numbers
  |      |      |    ├─> Material error → Check ZAID in xsdir
  |      |      |    ├─> Source error → Verify SDEF dependencies
  |      |      |    └─> Mode/physics error → Check MODE, PHYS cards
  |      |      ├─> Fix first error
  |      |      ├─> Re-run
  |      |      └─> Repeat until all fatal errors resolved
  |      |
  |      +--> NO: Transport Phase Error (BAD TROUBLE or Lost Particle)
  |           |
  |           +--> Is it a "lost particle" error?
  |           |      |
  |           |      +--> YES: Geometry Error
  |           |      |      ├─> Examine event log (particle path)
  |           |      |      ├─> Note coordinates where particle lost
  |           |      |      ├─> Plot geometry at lost location
  |           |      |      ├─> Look for:
  |           |      |      |    ├─> Dashed lines (overlaps/gaps)
  |           |      |      |    ├─> Incorrect surface sense
  |           |      |      |    ├─> Missing cells
  |           |      |      |    └─> Transformation errors
  |           |      |      ├─> Fix geometry issue
  |           |      |      └─> Use VOID card test to verify fix
  |           |      |
  |           |      +--> NO: Other BAD TROUBLE
  |           |           ├─> Read BAD TROUBLE message
  |           |           ├─> Check for:
  |           |           |    ├─> Divide by zero (check source, tallies)
  |           |           |    ├─> Invalid parameters (negative values)
  |           |           |    ├─> Array overflow (too many particles)
  |           |           |    └─> Memory issues (reduce problem size)
  |           |           ├─> Fix root cause
  |           |           └─> Re-run
  |           |
  +--> Still having issues after fixes?
         ├─> Simplify input (remove features one by one)
         ├─> Test geometry with VOID card
         ├─> Check similar working examples
         ├─> Consult MCNP manual for specific card
         └─> Ask for help with minimal reproducing example
```

## Tool Invocation

This skill includes a Python implementation that uses the error pattern database to automatically diagnose fatal errors.

### Importing the Tool

```python
from mcnp_fatal_error_debugger import MCNPFatalErrorDebugger

# Initialize the debugger
debugger = MCNPFatalErrorDebugger()
```

### Basic Usage

**Diagnose Errors from Output File**:
```python
# Analyze MCNP output file for fatal errors
result = debugger.diagnose_error('outp')

# Print error count
print(f"Found {result['count']} fatal errors")

# Display each error with suggested fix
for error in result['errors']:
    print(f"Error: {error['message']}")
    print(f"Fix: {error['fix']}")
    if error['example']:
        print(f"Example: {error['example']}")
```

**Match Specific Error Message**:
```python
# Get fix for a specific error message
error_msg = "bad trouble in subroutine sourcc"
fix = debugger.suggest_fix(error_msg)
print(fix)
# Output: "Source position is outside geometry or in void cell..."
```

**Get Common Fatal Errors**:
```python
# Retrieve list of all known fatal error patterns
common_errors = debugger.get_common_errors()

for pattern in common_errors:
    print(f"Category: {pattern.category}")
    print(f"Pattern: {pattern.pattern}")
    print(f"Fix: {pattern.fix}")
```

### Integration with Error Resolution Workflow

```python
from mcnp_fatal_error_debugger import MCNPFatalErrorDebugger

# Automated error diagnosis after MCNP run
debugger = MCNPFatalErrorDebugger()
result = debugger.diagnose_error('path/to/outp')

if result['count'] > 0:
    print(f"Fatal errors detected: {result['count']}")

    # Focus on first error (others may be cascades)
    first_error = result['errors'][0]
    print(f"\nPrimary Error:")
    print(f"  Message: {first_error['message']}")
    print(f"  Category: {first_error['pattern'].category}")
    print(f"  Suggested Fix: {first_error['fix']}")

    # Apply fix and re-run
else:
    print("No fatal errors found!")
```

---

## Use Case 1: Fatal Error - Material Not Defined

**Scenario**: Fatal error because cell references undefined material

**Error Message**:
```
fatal error.  material   3 has not been specified but is used in cell    5.
```

**Problematic Input**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1              $ Cell 1, material 1
2  2  -2.3   1 -2  IMP:N=1            $ Cell 2, material 2
5  3  -11.3  2 -3  IMP:N=1            $ Cell 5, material 3 (ERROR: M3 not defined)
999  0  3  IMP:N=0                    $ Graveyard

Surface Cards
1  SO  10
2  SO  20
3  SO  30

Data Cards
MODE  N
M1  1001.80c  2  8016.80c  1          $ Water
M2  6000.80c  1                       $ Carbon
c M3 not defined!                     $ ERROR: Material 3 missing
SDEF  POS=0 0 0  ERG=14.1
NPS  1e6
```

**Fix**:
```
Data Cards
MODE  N
M1  1001.80c  2  8016.80c  1          $ Water
M2  6000.80c  1                       $ Carbon
M3  82000.80c  1                      $ Lead (ADDED)
SDEF  POS=0 0 0  ERG=14.1
NPS  1e6
```

**Diagnostic Steps**:
1. Read first fatal error: "material 3 has not been specified"
2. Search input for "M3" card
3. Realize M3 card missing
4. Add M3 card with appropriate composition
5. Re-run

**Key Points**:
- First fatal error is the real one
- Check all cell material numbers have corresponding M cards
- Material numbers must match exactly (M3 for material 3)

## Use Case 2: Fatal Error - Surface Not Found

**Scenario**: Cell references non-existent surface

**Error Message**:
```
fatal error.  surface    15 of cell    2 is not defined in the surface card section.
```

**Problematic Input**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1
2  1  -1.0   1 -15  IMP:N=1          $ ERROR: Surface 15 not defined
999  0  15  IMP:N=0

Surface Cards
1  SO  10
c Surface 15 missing!

Data Cards
[...]
```

**Fix**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1
2  1  -1.0   1 -2  IMP:N=1           $ FIXED: Changed 15 to 2
999  0  2  IMP:N=0                   $ FIXED: Changed 15 to 2

Surface Cards
1  SO  10
2  SO  20                             $ ADDED: Surface 2
```

**Alternative Fix** (if 15 was intended):
```
Surface Cards
1  SO  10
15  SO  20                            $ ADDED: Define surface 15
```

**Key Points**:
- Verify all surface numbers in cells are defined
- Typos in surface numbers are common (15 vs 1, 5)
- Check both positive and negative surface senses

## Use Case 3: Lost Particle - Geometry Overlap

**Scenario**: Particle lost due to overlapping cells

**Error Message (in outp)**:
```
  bad trouble in subroutine track of mcrun
    source particle no.       1234

    particle lost at point:
      x =   5.12345
      y =   3.67890
      z =   0.00000

    in cell    2

  lost particle at   5.12345  3.67890  0.00000

  event log of particle        1234
    surface     cell    mat     nps
                  1      1        1234
        1         2      2        1234

  particle   1234 lost.
```

**Problematic Geometry**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1              $ Sphere, R=10
2  2  -2.3   -2  IMP:N=1              $ Sphere, R=12 (OVERLAPS cell 1!)
999  0  1 2  IMP:N=0                  $ Outside both

Surface Cards
1  SO  10                             $ Sphere R=10
2  SO  12                             $ Sphere R=12 (encloses 1, creates overlap!)

Data Cards
MODE  N
[...]
```

**Problem**: Cell 2 completely encloses cell 1, creating overlap

**Fix**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1              $ Inner sphere, R=10
2  2  -2.3   1 -2  IMP:N=1            $ Shell between R=10 and R=12 (FIXED)
999  0  2  IMP:N=0                    $ Outside R=12

Surface Cards
1  SO  10
2  SO  12
```

**Diagnostic Steps**:
1. Note lost particle coordinates: (5.12, 3.68, 0.00)
2. Examine event log: particle crossed surface 1 into cell 2
3. Plot geometry at (5.12, 3.68, 0.00):
   ```
   IP  5.12 3.68 0  EX 10
   ```
4. Observe cell 1 and cell 2 overlap
5. Fix cell 2 definition to exclude cell 1 (add `1` to geometry)

**Key Points**:
- Lost particle coordinates show where error occurred
- Event log shows particle path leading to error
- Plot at lost location to visualize issue
- Shells need inner surface positive, outer surface negative

## Use Case 4: Lost Particle - Gap in Geometry

**Scenario**: Particle enters undefined region (gap between cells)

**Error Message**:
```
  bad trouble in subroutine track of mcrun
    particle lost at point:
      x =  10.00001
      y =   0.00000
      z =   0.00000

    in cell    ?

  no cell found at position   10.00001   0.00000   0.00000
```

**Problematic Geometry**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1              $ Inner sphere, R=10
2  2  -2.3   2  IMP:N=1               $ Outer region, outside R=12
999  0  1 -2  IMP:N=0                 $ Outside world (WRONG!)

Surface Cards
1  SO  10
2  SO  12

Data Cards
[...]
```

**Problem**: Cell 999 is outside 1 AND inside 2, but cells 1 and 999 don't cover region between surfaces 1 and 2 (gap from R=10 to R=12)

**Fix**:
```
Cell Cards
1  1  -1.0   -1  IMP:N=1              $ Inner sphere, R=10
2  2  -2.3   1 -2  IMP:N=1            $ Shell, R=10 to R=12 (ADDED)
999  0  2  IMP:N=0                    $ Outside R=12 (FIXED)

Surface Cards
1  SO  10
2  SO  12
```

**Alternative Fix** (if gap was air):
```
Cell Cards
1  1  -1.0   -1  IMP:N=1              $ Inner sphere
2  0        1 -2  IMP:N=1             $ Air gap (void)
3  2  -2.3  2  IMP:N=1                $ Outer region
999  0  -1:2  IMP:N=0                 $ Outside (FIXED)
```

**Key Points**:
- "No cell found" indicates gap in geometry
- Every point in geometry must belong to exactly one cell
- Check surface senses carefully (positive vs negative)
- Plot to visualize cell coverage

## Use Case 5: Source Error - Impossible Dependencies

**Scenario**: SDEF has incompatible dependent variables

**Error Message**:
```
fatal error. impossible source variable dependencies.
```

**Problematic Input**:
```
SDEF  POS=D1  AXS=FPOS=D2  RAD=D3
SI1   L  0 0 0  10 0 0  20 0 0      $ Position distribution
DS2   S  3 4 5                      $ AXS depends on position (INVALID!)
SI3   L  0 1 0
SI4   L  1 0 0
SI5   L  0 0 1
SP3   1
SP4   1
SP5   1
SI6   0  5
SP6   -21  1
```

**Problem**: AXS (axis) cannot depend on POS (position) - invalid dependency

**Fix Option 1** (Remove dependency):
```
SDEF  POS=D1  AXS=0 0 1  RAD=D3     $ AXS fixed, not dependent
SI1   L  0 0 0  10 0 0  20 0 0
SI3   0  5
SP3   -21  1
```

**Fix Option 2** (Different approach):
```
SDEF  CEL=D1  AXS=0 0 1  RAD=D2     $ Source in specific cells
SI1   L  1  2  3                    $ Cell numbers
SP1      1  1  1
SI2   0  5
SP2   -21  1
```

**Common Invalid Dependencies** (from Source Primer Chapter 5):
- AXS = FPOS (axis as function of position)
- SUR = FPOS (surface as function of position)

**Key Points**:
- MCNP detects source dependency errors at input processing
- Review SDEF, SI, SP, DS cards for logical consistency
- Some combinations physically invalid (axis can't change with position)

## Use Case 6: BAD TROUBLE - Divide by Zero

**Scenario**: Zero in denominator during calculation

**Error Message**:
```
  bad trouble    in subroutine source of mcrun
      floating point exception - divide by zero

    nps =        5678
```

**Possible Causes**:
1. Zero volume in volume source
2. Zero area in surface source
3. Zero energy range
4. Invalid tally normalization

**Example Problem**:
```
SDEF  CEL=1  ERG=D1
SI1   H  0  0  1                     $ Energy histogram (INVALID: zero bin width!)
SP1      0  1
```

**Fix**:
```
SDEF  CEL=1  ERG=D1
SI1   H  0  0.1  1  10               $ Valid energy bins
SP1      0  1    1  0                $ Histogram probabilities
```

**Diagnostic Steps**:
1. Note NPS where error occurred (particle 5678)
2. Check source definition for zero values
3. Verify energy distributions have non-zero bin widths
4. Check volume/area calculations if using CEL or SUR

**Key Points**:
- BAD TROUBLE shows which subroutine failed
- NPS indicates how far calculation progressed
- Zero denominators often in source or tally specifications

## Use Case 7: ZAID Not in xsdir

**Scenario**: Cross-section library not found

**Error Message**:
```
warning.  nuclide  92235.80c is not available on the xsdir file.
fatal error.  stopping in subroutine mcrun.
```

**Causes**:
1. ZAID not installed (library missing)
2. Typo in ZAID
3. Wrong library suffix (.80c vs .70c)
4. xsdir file not found

**Check Installation**:
```bash
# Check DATAPATH environment variable
echo $DATAPATH
# Expected: path to directory containing xsdir

# Search xsdir for ZAID
grep "92235.80c" $DATAPATH/xsdir
```

**Fix Option 1** (Use different library):
```
M1  92235.70c  0.03  92238.70c  0.97  $ Use ENDF/B-VII.0 instead
```

**Fix Option 2** (Use version-agnostic):
```
M1  92235.00c  0.03  92238.00c  0.97  $ Use latest available
```

**Fix Option 3** (Install library):
```
# Contact system administrator to install ENDF/B-VIII.0 libraries
# Or download from MCNP data website
```

**Key Points**:
- Check xsdir file for available ZAIDs before using
- .80c = ENDF/B-VIII.0, .70c = ENDF/B-VII.0, .00c = latest
- Neutron libraries end in 'c', photon in 'p'

## Use Case 8: Systematic Geometry Debugging with VOID Card

**Scenario**: Complex geometry with suspected overlaps/gaps, need comprehensive test

**Test Procedure**:

**Step 1**: Save original input as `original.i`

**Step 2**: Create test input `test_geom.i`:
```
Geometry Test with VOID Card
c Cell Cards (ORIGINAL)
[... keep original cell definitions ...]

c Add outer sphere to flood geometry
998  0  -998  999  IMP:N=1           $ Region between system and flood sphere
999  0  998  IMP:N=0                 $ Outside flood sphere

c Surface Cards (ORIGINAL)
[... keep original surfaces ...]

c Add flood surface
998  SO  1000                         $ Large sphere enclosing system
999  SO  100                          $ System outer boundary (approximate)

c Data Cards
VOID                                  $ Override materials, make all void
MODE  N
IMP:N  1  1  1  1  ...  1  1  0      $ All cells IMP=1 except graveyard (last entry 0)
SDEF  SUR=998  NRM=-1                $ Inward directed surface source
NPS  10000                            $ Short run to test geometry
```

**Step 3**: Run test
```bash
mcnp6 inp=test_geom.i outp=test.o
```

**Step 4**: Examine results
- If particles get lost → geometry error exists, check event log for location
- If all particles track successfully → geometry likely correct
- Check output for lost particle messages

**Step 5**: Fix any issues found, repeat until clean

**Step 6**: Remove VOID card, restore original materials, run production

**Key Points**:
- VOID card makes all cells void (no collisions → more tracks)
- Short run generates many particle paths
- Flooding from outside tests all boundaries
- Very effective for finding hidden geometry errors

## Common Errors and Troubleshooting

### Error 1: Multiple Fatal Errors Reported

**Symptom**: MCNP prints 10-20 fatal error messages

**Cause**: First fatal error causes cascading failures

**Example**:
```
fatal error.  material   3 not defined.
fatal error.  cell   5 has invalid material.
fatal error.  importance not set for cell 5.
fatal error.  [... many more ...]
```

**Fix**:
```
c Fix ONLY the first error (material 3 not defined)
M3  82000.80c  1.0                    $ Add missing material

c Re-run → subsequent errors likely disappear
```

**Key Point**: Always fix first fatal error only, then re-run

### Error 2: Particle Lost at Cell Boundary

**Symptom**: Particle lost at exact boundary between cells

**Cause**: Numerical precision issue or incorrect surface sense

**Example**:
```
  particle lost at   10.00000  0.00000  0.00000
  on surface     1
```

**Check**:
```
c Verify cells on both sides of surface 1 defined correctly
1  1  -1.0   -1  IMP:N=1              $ Inside surface 1
2  2  -2.3   1   IMP:N=1              $ Outside surface 1 (should be +1)
```

**Fix if wrong**:
```
c If cell 2 should be outside surface 1:
2  2  -2.3   1  IMP:N=1               $ Correct: positive sense

c If cell 2 should be something else:
2  2  -2.3   1 -2  IMP:N=1            $ Between surfaces 1 and 2
```

### Error 3: Lost Particle in Transformation

**Symptom**: Particle lost in transformed geometry

**Cause**: Transformation matrix incorrect or applied to wrong surface

**Example**:
```
*TR1  10 0 0  0 1 0  1 0 0  0 0 1    $ Rotation + translation
...
10  1  SO  5                          $ Surface 10 transformed by TR1
...
  particle lost at  15.00000  0.00000  0.00000
```

**Check**:
```
c Verify transformation matrix orthonormal
c Row 1: (0, 1, 0) → length = 1 ✓
c Row 2: (1, 0, 0) → length = 1 ✓
c Row 3: (0, 0, 1) → length = 1 ✓
c Rows orthogonal ✓

c Check if transformation actually needed
c Try removing transformation to isolate issue
10  SO  5                             $ Test without transformation
```

### Error 4: BAD TROUBLE in Weight Windows

**Symptom**: BAD TROUBLE related to weight windows during transport

**Cause**: Weight window values incorrect or incompatible

**Fix**:
```
c Remove weight windows temporarily to test
c WWP:N  J  J  J  0  -1               $ Comment out
c WWN:N  ...                          $ Comment out

c If problem resolves, regenerate weight windows
c If problem persists, issue elsewhere
```

### Error 5: Tally Specification Error

**Symptom**: Fatal error related to tally card

**Example**:
```
fatal error.  surface   10 on f2:n tally not defined.
```

**Fix**:
```
c Either define surface 10:
10  PX  50

c Or correct tally to reference existing surface:
F2:N  1                               $ Use surface 1 instead of 10
```

### Error 6: Geometry Error Only with Variance Reduction

**Symptom**: No lost particles in analog, but lost with importance sampling

**Cause**: Particles split/roulette into undefined regions

**Diagnostic**:
```
c Run analog first (IMP:N=1 everywhere)
IMP:N  1  1  1  1  1  0               $ All equal importance

c If successful, add VR gradually
IMP:N  1  2  4  8  16  0              $ Geometric importance
```

**If still failing**:
```
c Issue likely in geometry near importance boundaries
c Plot at lost particle location
c Check cells adjacent to importance changes
```

## Integration with Other Skills

### 1. **mcnp-input-validator**

Validator catches many errors before running MCNP.

**Workflow**:
```
1. input-validator: Check syntax, cross-references
2. Fix issues found
3. Run MCNP
4. If fatal error → fatal-error-debugger
5. Fix → re-run validator
6. Repeat until clean
```

### 2. **mcnp-geometry-checker**

Geometry-checker validates geometry before running.

**Pattern**:
```
1. geometry-checker: Validate cells, surfaces, definitions
2. If issues → fix
3. Run MCNP
4. If lost particle → fatal-error-debugger
5. Use VOID card test
6. Fix geometry → re-validate with geometry-checker
```

### 3. **mcnp-output-parser**

Parser extracts error messages from output for analysis.

**Example**:
```python
# Parse output for errors
errors = output_parser.extract_fatal_errors('outp')
for error in errors:
    print(f"Line {error.line}: {error.message}")
    # Apply fatal-error-debugger procedures
```

### 4. **mcnp-material-builder**

Material-builder ensures correct material definitions.

**Workflow**:
```
1. material-builder: Create materials
2. Run MCNP
3. If "ZAID not in xsdir" → fatal-error-debugger
4. Check library availability
5. Update material-builder with correct ZAIDs
```

### 5. **mcnp-source-builder**

Source-builder creates valid source definitions.

**Pattern**:
```
1. source-builder: Create SDEF
2. Run MCNP
3. If "impossible source variable dependencies" → fatal-error-debugger
4. Identify invalid dependency
5. Fix source-builder logic
```

## Validation Checklist

Before reporting error fixed:

- [ ] First fatal error identified and fixed
- [ ] Input file re-validated (no syntax errors)
- [ ] MCNP runs without fatal errors
- [ ] If geometry error:
  - [ ] Lost particle location identified
  - [ ] Geometry plotted at lost location
  - [ ] Overlap or gap identified and fixed
  - [ ] VOID card test passed
- [ ] If source error:
  - [ ] Invalid dependency identified
  - [ ] Source redefined without dependency
  - [ ] Source particles generated successfully
- [ ] If material error:
  - [ ] ZAID availability confirmed in xsdir
  - [ ] Material composition correct
- [ ] Test run completes successfully (even if short)
- [ ] Results physically reasonable

## Advanced Topics

### 1. Event Log Analysis

**Event Log Structure**:
```
  event log of particle        1234
    surface     cell    mat     nps
                  1      1        1234    ← Start in cell 1
        10        2      2        1234    ← Cross surf 10 to cell 2
        15        3      3        1234    ← Cross surf 15 to cell 3
        15        ?      ?        1234    ← Lost crossing surf 15 again
```

**Interpretation**:
- Each line shows surface crossed and resulting cell
- Last line with "?" indicates where lost
- Backtrack path to understand particle trajectory
- Plot surfaces involved

### 2. Geometry Plotting for Debugging

**Plot at Lost Location**:
```
c Particle lost at (5.12, 3.68, 0.00)
IP  5.12 3.68 0                       $ Origin at lost location
BA  10                                $ Extent 10 cm
PX  1 0 0                             $ Look along +x direction
```

**Interactive Plotting**:
```bash
mcnp6 IP
# In interactive plotter:
# - Move origin to lost particle location
# - Rotate view to see problematic region
# - Look for dashed lines (geometry errors)
# - Zoom in to suspected overlap/gap area
```

### 3. Incremental Complexity Testing

**Strategy**: Build geometry incrementally, test at each stage

**Example**:
```
c Stage 1: Simple sphere (test)
1  1  -1.0  -1  IMP:N=1
999  0  1  IMP:N=0
1  SO  10

c Stage 2: Add inner sphere (test)
1  1  -1.0  -1  IMP:N=1
2  2  -2.0  1 -2  IMP:N=1
999  0  2  IMP:N=0
1  SO  5
2  SO  10

c Stage 3: Add complexity... (test at each stage)
```

### 4. Debugging with FATAL Option

**FATAL Execution Option**:
```bash
# Forces MCNP to run despite fatal errors (DANGEROUS!)
mcnp6 inp=input.i FATAL
```

**Use Cases**:
- Investigating nature of fatal error
- Testing if fatal error actually prevents results
- **WARNING**: Results may be incorrect, use with extreme caution

**When NOT to use**:
- Production calculations
- Geometry errors (will produce wrong results)
- Material definition errors

### 5. Lost Particle Retry Logic

**MCNP Behavior**:
- First lost particle → rerun with event logging
- Print detailed diagnostics
- Subsequent lost particles → summary only

**Suppression** (if intentional, rare):
```
LOST  100                             $ Allow up to 100 lost particles
```

**Never recommended except**:
- Debugging specific lost particle issue
- Testing if error is systematic or random
- Understanding pattern of lost particles

## Quick Reference: Common Fatal Errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| "material X not defined" | M card missing | Add MX card with composition |
| "surface X not defined" | Surface card missing | Add surface X definition |
| "particle lost" | Geometry overlap/gap | Plot at location, fix geometry |
| "impossible source variable dependencies" | Invalid SDEF dependency | Remove AXS=FPOS or SUR=FPOS |
| "ZAID not in xsdir" | Library not available | Use different library (.70c vs .80c) |
| "divide by zero" | Zero denominator in calculation | Check source bins, volumes, areas |
| "bad trouble in track" | Geometry error during transport | Use VOID card test, fix geometry |
| "cell X importance not set" | IMP card missing entry | Add IMP:N entry for all cells |

## Best Practices

1. **Fix First Error Only**: Subsequent errors often artifacts
   ```
   fatal error #1: material 3 not defined  ← FIX THIS
   fatal error #2: cell 5 invalid          ← Likely resolves after #1
   ```

2. **Always Plot Geometry**: Visual inspection prevents many errors
   ```bash
   mcnp6 IP
   # Check from multiple angles
   # Look for dashed lines
   ```

3. **Use VOID Card Test**: Comprehensive geometry validation
   ```
   VOID
   SDEF SUR=998 NRM=-1
   NPS 10000
   ```

4. **Start Simple, Add Complexity**: Test at each stage
   ```
   Stage 1: Basic geometry → test
   Stage 2: + materials → test
   Stage 3: + variance reduction → test
   ```

5. **Read Event Log Carefully**: Shows particle path to error
   ```
   Start → surf 1 → cell 2 → surf 10 → LOST
   (Plot surfaces 1 and 10, cells 2 and neighbors)
   ```

6. **Check xsdir Before Using ZAIDs**: Prevent library errors
   ```bash
   grep "92235.80c" $DATAPATH/xsdir || echo "Not available"
   ```

7. **Keep Backup of Working Input**: Easy rollback if changes break
   ```bash
   cp working.i working_backup.i
   # Make changes to working.i
   # If breaks, restore from backup
   ```

8. **Document Fixes**: Note what was wrong for future reference
   ```
   c FIXED 2024-10-31: Cell 5 was missing positive sense on surface 2
   c   Original: 5  1  -1.0  -1  2  IMP:N=1
   c   Fixed:    5  1  -1.0  -1 -2  IMP:N=1
   ```

9. **Test After Each Fix**: Verify fix resolves issue
   ```
   fix → run → check output → next issue
   ```

10. **Ask for Help with Minimal Example**: If stuck
    ```
    # Create minimal reproducing input
    # Post to forum/ask colleague
    # Include error message and relevant cards only
    ```

## References

- **Documentation**:
  - Chapter 3: Introduction to MCNP Usage
  - Chapter 4: §4.7 Input Error Messages, §4.8 Geometry Errors
  - Source Primer Chapter 5: Known Source Errors
  - Chapter 5.13: Output Control (error tables)
- **Related Skills**:
  - mcnp-input-validator (pre-run validation)
  - mcnp-geometry-checker (geometry validation)
  - mcnp-output-parser (error extraction)
  - mcnp-material-builder (material validation)
  - mcnp-source-builder (source validation)
- **User Manual**:
  - Chapter 4.7: Input Error Messages
  - Chapter 4.8: Geometry Errors
  - Chapter 3: Sample Problem (debugging examples)

---

**End of MCNP Fatal Error Debugger Skill**
