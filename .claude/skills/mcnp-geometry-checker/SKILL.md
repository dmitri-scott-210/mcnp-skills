---
name: mcnp-geometry-checker
description: "Validates MCNP geometry definitions for overlaps, gaps, Boolean errors, and surface issues. Use when analyzing geometry or debugging lost particles."
version: "2.0.0"
dependencies: "python>=3.8, mcnp-input-validator, mcnp-cross-reference-checker"
---

# MCNP Geometry Checker

## Overview

Geometry errors are the most common cause of MCNP simulation failures. This skill validates geometry definitions for overlaps (multiple cells claiming the same space), gaps (space belonging to no cell), incorrect Boolean operators, surface definition errors, and lost particle issues. These problems cause "bad trouble" errors, incorrect physics, or wasted compute time.

Proper geometry validation prevents lost particles, ensures physical correctness, and saves debugging time. MCNP's geometry plotter and VOID card test are essential tools for verification. This skill provides systematic checking procedures, automated validation scripts, and debugging workflows for complex geometries including lattices and repeated structures.

Use this skill after geometry modifications, before production runs, when debugging lost particles, or when setting up complex multi-region models. It integrates with MCNP's plotting tools and provides interpretation of geometry error messages.

## When to Use This Skill

- Getting "lost particle" errors or "bad trouble" messages from MCNP
- After modifying geometry (adding/deleting cells or surfaces)
- Before production runs (proactive geometry validation)
- Setting up complex geometries (lattices, nested structures)
- Need help with geometry plotting and visualization
- Interpreting dashed lines in MCNP plots
- VOID card test setup and interpretation
- Debugging overlapping cell issues

## Decision Tree

```
User has geometry problem
      ↓
What type of check needed?
      ├─→ [Quick Syntax Check]
      │   └─→ Verify surfaces exist, basic Boolean validation
      │       └─→ Issues found? → Fix syntax errors first
      │
      ├─→ [Comprehensive Validation]
      │   └─→ Generate VOID test, plot commands, analyze Boolean
      │       └─→ Run VOID test:
      │           ├─→ Non-zero result → Overlaps exist (FATAL)
      │           └─→ Zero result → No overlaps (OK)
      │
      ├─→ [Lost Particle Debugging]
      │   └─→ Parse lost particle event from output
      │       └─→ Plot geometry at lost particle location
      │           └─→ Identify: Gap? Overlap? Boolean error?
      │
      └─→ [Visualization Help]
          └─→ Generate plot commands for multiple views
              └─→ Interpret dashed lines, cell colors
```

## Quick Reference

### Geometry Error Types

| Error Type | Symptom | Cause | Severity |
|------------|---------|-------|----------|
| Overlap | VOID test non-zero | Multiple cells claim space | FATAL |
| Gap | Lost particles | Space belongs to no cell | FATAL |
| Boolean Error | Wrong regions | Operator precedence wrong | FATAL |
| Surface Sense | Cell in wrong half-space | Wrong +/- sign | FATAL |
| Lost Particle | "lost particle" message | Gap or bad surface | FATAL |

### MCNP Geometry Tools

| Tool | Command | Purpose |
|------|---------|---------|
| Plot Mode | `mcnp6 ip i=file.inp` | Interactive geometry plotting |
| VOID Test | Add `VOID` card | Detects overlapping cells |
| Lost Particle Log | Check output file | Find where particles lost |
| Cross Section | `plot basis=xy` | View XY cross-section |

### Validation Workflow

```
1. mcnp-input-validator     → Syntax check
2. mcnp-cross-reference-checker → References valid
3. mcnp-geometry-checker    → Geometry valid (THIS SKILL)
4. VOID test                → Overlap detection
5. Geometry plotting        → Visual verification
```

## Use Cases

### Use Case 1: VOID Card Test for Overlaps

**Scenario:** Need to verify no overlapping cells before production run.

**Goal:** Use VOID card to detect any overlaps in geometry.

**Implementation:**
```
Step 1: Add VOID card to input file

Add to Data Cards block:
VOID

Step 2: Run MCNP with minimal histories
NPS 1000   $ Quick test

Step 3: Check output for VOID result
Search output for: "void"

Result interpretation:
- VOID = 0.00000E+00 → NO overlaps (PASS) ✓
- VOID ≠ 0 → Overlaps exist (FAIL) ✗

Step 4: If overlaps found:
- Identify overlapping cells from output
- Plot geometry in overlap region
- Fix Boolean expressions or surface definitions
```

**Key Points:**
- VOID test is most reliable overlap detector
- Always run before production (saves compute time)
- Non-zero VOID means physics is WRONG (results invalid)
- See geometry_validation_procedures.md for complete workflow

### Use Case 2: Lost Particle Debugging

**Scenario:** MCNP output shows "lost particle" errors.

**Goal:** Find where particles are lost and fix the geometry gap.

**Implementation:**
```
Step 1: Extract lost particle info from output

From MCNP output:
lost particle at x=10.5 y=2.3 z=15.8
  in cell 0 (void)
  surface 25

Step 2: Plot geometry at lost particle location

mcnp6 ip i=input.inp
plot origin=10.5 2.3 15.8 extent=5 5 basis=xy

Step 3: Identify the problem
- Dashed line → Gap between cells
- Multiple cell colors at point → Overlap
- No cell at location → Geometry incomplete

Step 4: Fix geometry
- Gap → Extend cell or add new cell
- Overlap → Fix Boolean operators
- Incomplete → Add missing cells
```

**Key Points:**
- Lost particles indicate gaps in geometry (space with no cell)
- Plot at exact lost particle coordinates
- Dashed lines in plot show gaps/undefined regions
- See lost_particle_debugging.md for systematic procedure

### Use Case 3: Multi-View Geometry Plotting

**Scenario:** Complex 3D geometry, need to verify from multiple angles.

**Goal:** Generate plots from XY, XZ, and YZ views to fully visualize.

**Implementation:**
```bash
# Launch MCNP plotter
mcnp6 ip i=reactor.inp

# In plotter, use these commands:
plot origin=0 0 0 basis=xy extent=50 50    # Top view (Z-axis out)
plot origin=0 0 0 basis=xz extent=50 50    # Side view (Y-axis out)
plot origin=0 0 0 basis=yz extent=50 50    # Front view (X-axis out)

# Interpret plot:
- Solid lines → Cell boundaries (surfaces)
- Dashed lines → Gaps or undefined regions
- Different colors → Different cells
- White/void → No cell defined
```

**Key Points:**
- View from 3 orthogonal directions (XY, XZ, YZ)
- Adjust origin to center of interest region
- Extent controls plot size (cm)
- See plotting_guide.md for advanced visualization

## Integration with Other Skills

**Typical Validation Pipeline:**
1. **mcnp-input-validator** → Basic syntax
2. **mcnp-cross-reference-checker** → References valid
3. **mcnp-geometry-checker** (THIS SKILL) → Geometry validated
4. **mcnp-physics-validator** → Physics settings

**Complementary Skills:**
- **mcnp-geometry-builder:** Create correct geometry from start
- **mcnp-input-validator:** Pre-geometry validation
- **mcnp-fatal-error-debugger:** Interpret geometry error messages

**Workflow Example:**
```
Project: Shield geometry modification

Step 1: Modify geometry (add shield layers)
Step 2: mcnp-cross-reference-checker → Verify references
Step 3: mcnp-geometry-checker → Run VOID test
Step 4: Plot geometry (verify visually)
Step 5: Run MCNP (if VOID=0)
Result: Validated geometry ready for simulation
```

## References

**Detailed Procedures:**
- **geometry_validation_procedures.md** - Complete validation workflows
- **lost_particle_debugging.md** - Systematic debugging procedures
- **plotting_guide.md** - Geometry visualization techniques

**Examples:**
- **example_inputs/** - Geometry error examples
  - overlap_example.i (demonstrates cell overlap)
  - gap_example.i (demonstrates geometry gap)
  - Description files for each

**Automation Tools:**
- **scripts/mcnp_geometry_checker.py** - Automated validation
- **scripts/README.md** - Complete documentation

**External Documentation:**
- MCNP6 Manual Chapter 3.3 (Geometry specification)
- MCNP6 Manual Chapter 5.2 (Cell cards and Boolean operators)
- MCNP6 Manual Chapter 5.3 (Surface cards)
- MCNP6 Manual Appendix B (Geometry plotting)

## Best Practices

1. **Always Run VOID Test Before Production**
   - Add VOID card to Data Cards block
   - Run with NPS 1000 for quick check
   - VOID=0 required (non-zero means overlaps exist)

2. **Plot Geometry from Multiple Views**
   - XY, XZ, YZ planes (orthogonal views)
   - Center plot origin on region of interest
   - Look for dashed lines (gaps) and color overlaps

3. **Fix Overlaps Immediately**
   - Overlaps cause incorrect physics (wrong materials)
   - Use VOID test to detect
   - Plot overlap region to visualize problem

4. **Debug Lost Particles Systematically**
   - Extract coordinates from output
   - Plot at exact location
   - Identify gap or overlap causing issue

5. **Test Complex Geometries Incrementally**
   - Build geometry in stages
   - Validate each stage (VOID test + plot)
   - Add complexity gradually

6. **Use Geometry Plotter Interactively**
   - `mcnp6 ip` mode for interactive plotting
   - Pan, zoom, rotate to inspect details
   - Color coding helps identify cells

7. **Understand Boolean Operator Precedence**
   - Intersection (space) binds tighter than union (:)
   - Use parentheses to clarify
   - Test complex Boolean expressions with plots

8. **Check Surface Sense Carefully**
   - Negative (-) vs positive (+) matters
   - Plot to verify cells on correct side
   - Common error: wrong sense flips half-space

9. **Validate After Every Geometry Change**
   - Adding/deleting cells → re-run VOID test
   - Modifying surfaces → check for gaps
   - Prevents compound errors

10. **Document Geometry Assumptions**
    - Note coordinate system orientation
    - Document surface numbering scheme
    - Explain complex Boolean expressions

---

**END OF SKILL**
