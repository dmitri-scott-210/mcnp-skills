---
category: C
name: mcnp-fatal-error-debugger
description: "Diagnose and fix MCNP fatal errors including geometry errors, input syntax errors, source problems, and BAD TROUBLE messages using systematic debugging procedures"
version: "2.0.0"
---

# MCNP Fatal Error Debugger

## Overview

This skill provides systematic procedures for diagnosing and fixing fatal errors in MCNP simulations. Fatal errors terminate MCNP before or during particle transport, preventing calculation completion. This skill covers input validation errors, geometry errors (lost particles, overlaps, gaps), source specification errors, BAD TROUBLE messages, and comprehensive debugging workflows.

The skill emphasizes the "first error first" principle: fix only the first fatal error, then re-run, as subsequent errors are often cascading artifacts. Comprehensive reference files provide detailed error catalogs, geometry debugging procedures, source error patterns, BAD TROUBLE recovery, and systematic workflows including the powerful VOID card test for geometry validation.

## When to Use This Skill

- MCNP terminates with "fatal error" message before running particles
- Simulation crashes with "BAD TROUBLE" message during execution
- Particles get lost due to geometry errors (overlaps or gaps)
- Source specification produces "impossible source variable dependencies"
- Material or cross-section errors prevent startup (ZAID not in xsdir)
- Input syntax errors block execution
- MCNP terminates unexpectedly without completing
- Need to systematically debug complex input files
- Geometry plotting shows dashed lines (potential geometry issues)

## Decision Tree: Debugging Fatal Errors

```
START: MCNP Fatal Error Occurred
  |
  +--> Error before any particles run?
  |      |
  |      +--> YES: Input Phase Error
  |      |      ├─> Read first fatal error in OUTP
  |      |      ├─> Check error type:
  |      |      |    ├─> Syntax error → Fix card format (see fatal_error_catalog.md)
  |      |      |    ├─> Cross-reference error → Verify material/surface numbers exist
  |      |      |    ├─> Material error → Check ZAID in xsdir (fatal_error_catalog.md)
  |      |      |    ├─> Source error → Verify SDEF dependencies (source_error_guide.md)
  |      |      |    └─> Mode/physics error → Check MODE, PHYS cards compatibility
  |      |      ├─> Fix ONLY first error
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
  |           |      |      ├─> Plot geometry at lost location (IP command)
  |           |      |      ├─> Look for:
  |           |      |      |    ├─> Dashed lines (overlaps/gaps)
  |           |      |      |    ├─> Incorrect surface sense (+ vs -)
  |           |      |      |    ├─> Missing cells (gaps in geometry)
  |           |      |      |    └─> Transformation errors
  |           |      |      ├─> Fix geometry issue (see geometry_error_guide.md)
  |           |      |      └─> Use VOID card test to verify fix (debugging_workflow.md)
  |           |      |
  |           |      +--> NO: Other BAD TROUBLE
  |           |           ├─> Read BAD TROUBLE message (see bad_trouble_guide.md)
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
         ├─> Test geometry with VOID card (debugging_workflow.md)
         ├─> Check similar working examples
         ├─> Consult detailed references below
         └─> Ask for help with minimal reproducing example
```

## Quick Reference: Most Common Fatal Errors

| Error Pattern | Likely Cause | First Action | Detailed Reference |
|---------------|--------------|--------------|-------------------|
| "material X not defined" | Missing M card | Add MX card | fatal_error_catalog.md §2.1 |
| "surface X not defined" | Missing surface | Add surface X or fix cell reference | fatal_error_catalog.md §2.2 |
| "particle lost" | Geometry overlap or gap | Plot at location, use VOID test | geometry_error_guide.md |
| "impossible source variable dependencies" | Invalid SDEF dependency | Remove AXS=FPOS or SUR=FPOS | source_error_guide.md §1 |
| "ZAID not in xsdir" | Library not available | Try .70c or .00c suffix | fatal_error_catalog.md §3.1 |
| "divide by zero" | Zero bin width or volume | Check SI histograms and volumes | bad_trouble_guide.md §3.1 |
| "bad trouble in track" | Geometry error during transport | Use VOID card test | geometry_error_guide.md |
| "importance not set" | IMP card missing entries | Add IMP entries for all cells | fatal_error_catalog.md §6.1 |

## Use Case 1: Material Not Defined Error

**Scenario:** Fatal error because cell references undefined material.

**Error Message:**
```
fatal error.  material   3 has not been specified but is used in cell    5.
```

**Diagnostic Steps:**
1. Read first fatal error: "material 3 has not been specified"
2. Search input for "M3" card → not found
3. Add M3 card with appropriate composition

**Fix:**
```
M3  82000.80c  1.0                    $ Lead (add to Data Cards)
```

**Key Points:**
- First fatal error is the real one
- Check all cell material numbers have corresponding M cards
- Material numbers must match exactly (M3 for material 3)

**Example File:** See `example_inputs/material_not_defined_error.i`

## Use Case 2: Lost Particle - Geometry Overlap

**Scenario:** Particle lost due to overlapping cells.

**Error Message:**
```
bad trouble in subroutine track of mcrun
  particle lost at point:  x = 5.12  y = 3.68  z = 0.00  in cell    2
```

**Problematic Geometry:**
```
1  1  -1.0   -1  IMP:N=1              $ Sphere, R=10
2  2  -2.3   -2  IMP:N=1              $ Sphere, R=12 (OVERLAPS cell 1!)
```

**Problem:** Cell 2 completely encloses cell 1, creating overlap.

**Fix:**
```
2  2  -2.3   1 -2  IMP:N=1            $ Shell between R=10 and R=12 (add +1 sense)
```

**Diagnostic Procedure:**
1. Note lost particle coordinates: (5.12, 3.68, 0.00)
2. Examine event log: particle crossed surface 1 into cell 2
3. Plot geometry at (5.12, 3.68, 0.00): `IP  5.12 3.68 0`
4. Observe cell 1 and cell 2 overlap
5. Fix cell 2 definition to exclude cell 1 (add `1` to geometry)

**Detailed Guide:** See `geometry_error_guide.md` for comprehensive overlap/gap debugging.

## Use Case 3: Source Error - Impossible Dependencies

**Scenario:** SDEF has incompatible dependent variables.

**Error Message:**
```
fatal error. impossible source variable dependencies.
```

**Problematic Input:**
```
SDEF  POS=D1  AXS=FPOS=D2  RAD=D3    $ AXS cannot depend on position!
```

**Problem:** AXS (axis) cannot depend on POS (position) - invalid dependency.

**Fix:**
```
SDEF  POS=D1  AXS=0 0 1  RAD=D3      $ Fixed axis, not dependent
```

**Common Invalid Dependencies:**
- AXS = FPOS → Axis cannot depend on position
- SUR = FPOS → Surface cannot depend on position

**Valid Dependencies:** ERG = FCEL (energy depends on cell), DIR = FPOS (direction depends on position)

**Detailed Guide:** See `source_error_guide.md` for complete source error patterns and valid dependencies.

## Use Case 4: VOID Card Test for Geometry Validation

**Scenario:** Complex geometry with suspected overlaps/gaps needing comprehensive validation.

**Procedure:**

1. **Create test input** `test_geom.i`:
```
VOID                                  $ Override materials, make all void
IMP:N  1  1  1  1  ...  1  1  0      $ All cells IMP=1 except graveyard
SDEF  SUR=998  NRM=-1                $ Inward directed surface source
NPS  10000                            $ Short test run
```

2. **Add flood geometry:**
```
998  0  -998 999  IMP:N=1             $ Between system and flood sphere
999  0  998  IMP:N=0                  $ Outside flood sphere
998  SO  1000                         $ Large sphere enclosing system
```

3. **Run test:** If particles get lost → geometry error exists (check event log). If all track successfully → geometry likely correct.

4. **Fix issues:** Plot at lost locations, identify overlaps/gaps, correct geometry.

5. **Remove VOID card:** Restore original materials, run production.

**Why VOID Test Works:**
- No collisions → particles stream through → more tracks → better geometry coverage
- Flooding from outside → tests all boundaries systematically
- Very effective for finding hidden geometry errors

**Complete Procedure:** See `debugging_workflow.md` for step-by-step VOID test workflow.

## Integration with Other Skills

### 1. mcnp-input-validator
Pre-run validation catches many errors before running MCNP.
```
Workflow: input-validator → fix issues → run MCNP → if fatal error → fatal-error-debugger
```

### 2. mcnp-geometry-checker
Validates geometry before running, catching cell/surface definition errors.
```
Workflow: geometry-checker → fix → run MCNP → if lost particle → fatal-error-debugger
```

### 3. mcnp-output-parser
Extracts error messages from output for automated analysis.
```python
errors = output_parser.extract_fatal_errors('outp')
for error in errors:
    # Apply fatal-error-debugger procedures
```

### 4. mcnp-material-builder
Ensures correct material definitions.
```
Workflow: material-builder → run MCNP → if "ZAID not in xsdir" → fatal-error-debugger
```

### 5. mcnp-source-builder
Creates valid source definitions.
```
Workflow: source-builder → run MCNP → if "impossible dependencies" → fatal-error-debugger
```

## References

### Comprehensive Error Catalogs
- **fatal_error_catalog.md:** Complete catalog of all fatal error types, organized by category (input syntax, cross-reference, material, source, geometry, physics)
- **geometry_error_guide.md:** Detailed geometry debugging (lost particles, overlaps, gaps, event log analysis, plotting techniques)
- **source_error_guide.md:** Source specification errors (SDEF, KCODE, SI/SP/DS cards, invalid dependencies)
- **bad_trouble_guide.md:** BAD TROUBLE messages, causes, and recovery procedures
- **debugging_workflow.md:** Systematic workflows (VOID test, incremental complexity, event log analysis, binary search)

### Python Scripts
- **scripts/README.md:** Script documentation and usage
- **scripts/mcnp_fatal_error_debugger.py:** Automated error diagnosis using pattern database
- **scripts/error_parser.py:** (Future) Parse OUTP files for errors
- **scripts/lost_particle_analyzer.py:** (Future) Analyze lost particle events

### Example Files
- **example_inputs/material_not_defined_error.i:** Demonstrates material cross-reference error
- Additional examples: (Create as needed for specific error types)

### MCNP Documentation
- Chapter 4 §4.7: Input Error Messages
- Chapter 4 §4.8: Geometry Errors
- Chapter 3: Sample Problems (debugging examples)
- Source Primer Chapter 5: Known Source Errors

## Best Practices

1. **Fix First Error Only:** Subsequent errors often artifacts of first error
2. **Always Plot Geometry:** Visual inspection prevents many errors
3. **Use VOID Card Test:** Comprehensive geometry validation technique
4. **Start Simple, Add Complexity:** Test at each stage, isolate errors incrementally
5. **Read Event Log Carefully:** Shows exact particle path to error location
6. **Check xsdir Before Using ZAIDs:** Prevent library errors (grep ZAID in $DATAPATH/xsdir)
7. **Keep Backup of Working Input:** Easy rollback if changes break geometry
8. **Document Fixes:** Note what was wrong for future reference in comments
9. **Test After Each Fix:** Verify fix resolves issue before moving to next
10. **Ask for Help with Minimal Example:** If stuck, create minimal reproducing case for forum/colleagues

## Validation Checklist

Before reporting error fixed:
- [ ] First fatal error identified and fixed
- [ ] Input file re-validated (no syntax errors)
- [ ] MCNP runs without fatal errors
- [ ] If geometry error: Lost particle location identified, geometry plotted, overlap/gap fixed, VOID test passed
- [ ] If source error: Invalid dependency identified, source redefined, source particles generated successfully
- [ ] If material error: ZAID availability confirmed in xsdir, material composition correct
- [ ] Test run completes successfully (even if short)
- [ ] Results physically reasonable

---

**END OF MCNP FATAL ERROR DEBUGGER SKILL**

For detailed information on specific error types and debugging procedures, consult the reference files listed above.
