---
name: "MCNP Geometry Checker"
description: "Validates MCNP geometry definitions for overlaps, gaps, Boolean errors, and surface issues. Use when analyzing geometry or debugging lost particles."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Geometry Checker

## Overview

Geometry errors are the most common MCNP problem. This skill helps users find and fix:
- Overlapping cells (multiple cells claim same space)
- Gaps between cells (space belongs to no cell)
- Incorrect Boolean operators (precedence errors, excessive # usage)
- Surface definition errors (wrong sense, undefined surfaces)
- Lost particle issues (particles escape valid geometry)

Use this skill when users report lost particles, want to verify geometry before running, or need help with geometry plotting and visualization.

## Workflow Decision Tree

### When to Invoke
- User mentions "lost particles" or geometry errors
- Before production runs (proactive checking)
- After geometry modifications
- When setting up complex geometries
- User asks about geometry plotting

### Validation Approach

**Quick Syntax Check:**
- Verify surfaces referenced in cells exist
- Check for unused surfaces
- Basic Boolean expression validation
→ Fast preliminary check

**Comprehensive Geometry Validation** (recommended):
- All syntax checks
- Generate plotting commands
- Create VOID test setup
- Analyze Boolean operators
→ Use before production runs

**Lost Particle Debugging:**
- Parse lost particle event log from output
- Plot geometry at lost particle location
- Identify probable cause
→ Use when particles already getting lost

**Visualization Assistance:**
- Generate plot commands for multiple views
- Explain what dashed lines mean
- Help interpret geometry plots
→ Use when user needs plotting help

## Tool Invocation

This skill includes a Python implementation for automated geometry validation and analysis.

### Importing the Tool

```python
from mcnp_geometry_checker import MCNPGeometryChecker

# Initialize the checker
checker = MCNPGeometryChecker()
```

### Basic Usage

**Check Geometry for Issues**:
```python
# Run geometry analysis
issues = checker.check_geometry('path/to/input.inp')

# Review all issues
for issue in issues:
    issue_type = issue['type']  # 'error', 'warning', 'info', 'recommendation'
    message = issue['message']
    print(f"[{issue_type.upper()}] {message}")
```

**Categorize Issues by Severity**:
```python
# Analyze geometry
issues = checker.check_geometry('reactor.inp')

# Group by type
errors = [i for i in issues if i['type'] == 'error']
warnings = [i for i in issues if i['type'] == 'warning']
recommendations = [i for i in issues if i['type'] == 'recommendation']

print(f"❌ Errors: {len(errors)}")
for err in errors:
    print(f"  - {err['message']}")

print(f"\n⚠ Warnings: {len(warnings)}")
for warn in warnings:
    print(f"  - {warn['message']}")

print(f"\n💡 Recommendations: {len(recommendations)}")
for rec in recommendations:
    print(f"  - {rec['message']}")
```

**Generate Plotting Commands**:
```python
# Check geometry and generate visualization commands
checker = MCNPGeometryChecker()
issues = checker.check_geometry('input.inp')

# Get recommended plot commands
plot_cmds = checker.generate_plot_commands()

print("Recommended geometry plots:")
for cmd in plot_cmds:
    print(f"  {cmd}")

# Output:
# plot origin=0 0 0 basis=xy extent=50 50  (top view)
# plot origin=0 0 0 basis=xz extent=50 50  (side view)
# plot origin=0 0 0 basis=yz extent=50 50  (front view)
```

**Generate VOID Test Input**:
```python
# Create VOID card test setup
checker = MCNPGeometryChecker()
void_test = checker.generate_void_test_input()

print(void_test)
# Outputs complete VOID test instructions
```

### Integration with MCNP Workflow

```python
from mcnp_geometry_checker import MCNPGeometryChecker

def validate_geometry(input_file):
    """Complete geometry validation workflow"""
    print(f"Checking geometry for: {input_file}")
    print("=" * 60)

    checker = MCNPGeometryChecker()
    issues = checker.check_geometry(input_file)

    # Separate issues by type
    errors = [i for i in issues if i['type'] == 'error']
    warnings = [i for i in issues if i['type'] == 'warning']
    infos = [i for i in issues if i['type'] == 'info']
    recommendations = [i for i in issues if i['type'] == 'recommendation']

    # Report errors
    if errors:
        print("\n❌ GEOMETRY ERRORS (must fix):")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err['message']}")

    # Report warnings
    if warnings:
        print("\n⚠ WARNINGS (should review):")
        for warn in warnings:
            print(f"  • {warn['message']}")

    # Report info
    if infos:
        print("\n📝 INFO:")
        for info in infos:
            print(f"  • {info['message']}")

    # Generate visualization commands
    print("\n📊 RECOMMENDED PLOTTING COMMANDS:")
    plot_cmds = checker.generate_plot_commands()
    print("  mcnp6 ip i=" + input_file)
    print("  Then in plotter:")
    for cmd in plot_cmds:
        print(f"    {cmd}")

    # Provide VOID test
    print("\n🧪 VOID CARD TEST (recommended):")
    void_test = checker.generate_void_test_input()
    print(void_test)

    # Provide recommendations
    if recommendations:
        print("\n💡 GEOMETRY CHECKING RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"  • {rec['message']}")

    print("\n" + "=" * 60)

    # Return validation status
    return len(errors) == 0

# Example usage
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.inp"

    if validate_geometry(input_file):
        print("\n✓ Geometry syntax checks passed")
        print("⚠ IMPORTANT: Always plot geometry and run VOID test!")
    else:
        print("\n✗ Geometry errors found - fix before running")
```

---

## Geometry Validation Procedure

### Step 1: Understand User's Geometry
Ask clarifying questions:
- "What type of geometry? (simple sphere, reactor, complex CAD import?)"
- "Are you getting lost particles, or just want to verify?"
- "Have you plotted the geometry yet?"
- "Any specific regions you're concerned about?"

### Step 2: Read Reference Materials
**MANDATORY - READ ENTIRE FILE**: Read `.claude/commands/mcnp-geometry-checker.md` for:
- Complete geometry checking procedures
- Boolean operator rules and precedence
- VOID card testing methodology
- Lost particle debugging techniques

### Step 3: Run Geometry Analysis

Use the Python checker (see **Tool Invocation** section above for detailed usage):

```python
from mcnp_geometry_checker import MCNPGeometryChecker

checker = MCNPGeometryChecker()
issues = checker.check_geometry('input.inp')

# Issues structure: list of dicts with 'type' and 'message'
# types: 'error', 'warning', 'info', 'recommendation'

# Generate plotting commands
plot_cmds = checker.generate_plot_commands()

# Generate VOID test input
void_test = checker.generate_void_test_input()
```

### Step 4: Report Findings Clearly

Group by severity:
1. **ERRORS** - Will cause problems
2. **WARNINGS** - Should review
3. **RECOMMENDATIONS** - Essential practices

### Step 5: Help Fix Geometry

For each issue:
- Explain the problem clearly
- Show how to visualize it (plotting)
- Provide fix with example
- Verify fix resolves issue

## Common Geometry Errors

### Boolean Operator Errors (Chapter 4)

**Precedence** (highest to lowest):
1. **# (complement)** - NOT operation
2. **space (intersection)** - AND operation
3. **: (union)** - OR operation

**Example confusion:**
```
-1 2 : 3 4    ← means: (-1 AND 2) OR (3 AND 4)
NOT: -1 AND (2 OR 3) AND 4

Use parentheses for clarity:
-1 (2:3) 4    ← means: -1 AND (2 OR 3) AND 4
```

**Excessive complement operator (#):**
```
Cell defined as: #1 #2 #3 #4 #5

Problem: Very complex, hard to debug
Better: Use explicit surface definitions
```

### Surface Sense Errors

**Surface sense (+/-):**
- **-N** = inside surface N (negative sense)
- **+N** = outside surface N (positive sense)

**Common mistake:**
```
1 SO 10    ← Sphere radius 10 centered at origin

Cell 1 0  -1   ← INSIDE sphere (correct for sphere)
Cell 2 0   1   ← OUTSIDE sphere

User often confuses signs!
```

### Overlapping Cells

**Problem:** Two cells both claim same space
```
Cell 1: -1        ← Inside sphere 1
Cell 2: -2        ← Inside sphere 2

If spheres overlap → GEOMETRY ERROR
```

**Detection:** Particles get lost at overlap boundary

**Fix:**
- Make cells mutually exclusive: `-1 2` (inside 1, outside 2)
- Or use cell complement: `#1 -2` (not in cell 1, inside 2)

### Gaps in Geometry

**Problem:** Space belongs to no cell
```
Cell 1: -1        ← Inside sphere r=5
Cell 2:  1 -2     ← Between sphere 1 and 2 (r=5 to r=10)
Cell 3:  2        ← Outside sphere 2 (r>10)

No gap if spheres share boundary at r=5 and r=10
Gap exists if spheres don't touch!
```

**Detection:** Particles get lost in gap

**Fix:**
- Ensure cells form complete partitioning of space
- Use VOID card test to flood geometry

## Geometry Plotting (Chapter 6)

### Interactive Plotting

**Command:**
```bash
mcnp6 ip i=input.inp
```

**Basic plot commands:**
```
# Three orthogonal views
plot origin=0 0 0 basis=xy extent=50 50  # Top view
plot origin=0 0 0 basis=xz extent=50 50  # Side view  
plot origin=0 0 0 basis=yz extent=50 50  # Front view

# Control options
plot label=1        # Show cell numbers
plot color=off      # Wire frame (clearer for errors)
plot scales=0.5     # Zoom in (2x)
plot scales=2.0     # Zoom out (0.5x)
```

### Interpreting Plots

**Dashed lines indicate:**
- ❌ Geometry error (overlap or gap)
- Plot plane coincides with geometry plane
- Cookie-cutter cells present
- DXTRAN spheres present

**Solid lines indicate:**
- ✓ Correct geometry (one cell each side)

**If you see dashed lines:**
1. Note location of dashed line
2. Zoom in to that region
3. Turn color off for clarity
4. Identify which cells/surfaces involved
5. Fix the geometry error

## VOID Card Testing (Chapter 3.2.8)

### Purpose
Flood geometry with particles to quickly find overlaps/gaps without physics calculations.

### Procedure

**1. Modify input file:**
```
c Add to data block:
VOID
```

**2. Create surface source:**
```
c Add large sphere around geometry
999 SO 1000    ← Surface card

c Split outside world
997 0  998 -999    ← Space between geometry and sphere
998 0  999         ← Outside new sphere (IMP=0)

c Modify original outside world cell to be inside 999

c Add inward-directed source
SDEF SUR=999 NRM=-1
NPS 1000000
```

**3. Run short test:**
```bash
mcnp6 i=input_void.inp
```

**4. Check for lost particles:**
- No lost particles = geometry likely OK
- Lost particles = geometry errors exist at loss locations

**5. Remove VOID card** after geometry verified

## Lost Particle Debugging

### When Particles Get Lost

MCNP automatically:
1. Reruns history with event logging ON
2. Shows all surface crossings
3. Prints position/direction at loss

### Debugging Procedure

**1. Find lost particle info in output:**
```
 particle 12345 got lost at:
   x=1.23 y=4.56 z=7.89
   u=0.1 v=0.2 w=0.97
   energy=2.5 MeV
```

**2. Plot geometry at that location:**
```bash
mcnp6 ip i=input.inp

# In plotter:
plot origin=1.23 4.56 7.89 basis=xy extent=10 10
plot color=off    # See structure clearly
```

**3. Look for:**
- Dashed lines near particle location
- Gaps between cells
- Overlapping cell boundaries
- Surface definition errors

**4. Common causes:**
- Cells don't form closed volumes
- Boolean operator precedence wrong
- Surface sense backwards (+/- swapped)
- Numerical precision issues (surfaces nearly coincident)

### Event Log Analysis

**Event log shows:**
```
event   cell  surf  type
  1      10    15    3
  2      12    15   -3
  3      12    20    2
lost at cell 12, surface 20
```

**Interpret:**
- Type 3/-3 = entering/exiting surface
- Lost at surface 20 in cell 12
- Check geometry definition of cell 12 near surface 20

## Geometry Building Best Practices (§3.4.1)

### Prevention is Best Medicine

**Before creating geometry:**
1. ✓ Draw geometry on paper first
2. ✓ Start simple, add complexity incrementally
3. ✓ Use simplest possible surfaces (RPP, SPH, RCC)
4. ✓ Avoid excessive # operator
5. ✓ Test each addition before continuing

**While building:**
1. ✓ Plot after each major addition
2. ✓ Use simple cell definitions
3. ✓ Break complex cells into multiple simple cells
4. ✓ Add comments explaining geometry logic

**Before production run:**
1. ✓ Plot from 3 orthogonal views MINIMUM
2. ✓ Run VOID card test
3. ✓ Pre-calculate volumes, compare with VOL card
4. ✓ Short test run (10k histories) to catch any remaining errors

## Integration with Other Skills

**Related skills:**
- **mcnp-input-validator**: Overall syntax validation (use first)
- **mcnp-geometry-builder**: Help create geometry correctly from start
- **mcnp-plotter**: Advanced visualization and plotting
- **mcnp-best-practices-checker**: Comprehensive problem setup review

**Workflow:**
1. Run mcnp-input-validator (basic checks)
2. Run mcnp-geometry-checker (detailed geometry)
3. Plot geometry interactively
4. Fix any issues
5. Run VOID test
6. Proceed to production

## Example Geometry Check Workflow

```
User: "I'm getting lost particles in my reactor model"

Claude: I'll help debug your geometry errors. Let me analyze your input file.

[Reads .claude/commands/mcnp-geometry-checker.md]
[Uses MCNPGeometryChecker]

**Geometry Analysis Results:**

ERRORS:
❌ Cell 15: Excessive use of complement operator (#)
   Geometry: #10 #11 #12 #13 #14
   Problem: Very complex, difficult to verify
   Fix: Redefine using explicit surfaces instead of complements
   Reference: §3.4.1 item #6

WARNINGS:
⚠ Surface 42 defined but never used
   Issue: May indicate incomplete cell definitions
   Action: Verify surface 42 should be used, or remove it

**Lost Particle Debugging:**

From your output file, particles lost at:
- Position: x=15.3, y=20.1, z=5.8
- Cell: 15
- Surface: 50

**Recommended Actions:**

1. **Plot geometry at loss location:**
   ```bash
   mcnp6 ip i=reactor.inp
   
   # In plotter:
   plot origin=15.3 20.1 5.8 basis=xy extent=20 20
   plot color=off
   plot label=1
   ```
   Look for dashed lines near the loss point.

2. **Simplify cell 15 geometry:**
   Current: #10 #11 #12 #13 #14
   Suggest: Define explicitly with surfaces
   
   Example fix:
   ```
   c Define bounding box for cell 15
   105 PX 10
   106 PX 20
   107 PY 15
   108 PY 25
   109 PZ 0
   110 PZ 10
   
   c Redefine cell 15
   15 5 -2.7  105 -106 107 -108 109 -110
   ```

3. **Run VOID test:**
   [Generates VOID test setup]
   
   This will quickly identify all geometry errors.

4. **After fixes, verify:**
   - Replot geometry from 3 views
   - Run short test (10k particles)
   - Check for any remaining lost particles

Would you like me to:
1. Help fix the cell 15 geometry definition?
2. Generate complete VOID test input?
3. Create plotting script for all suspect regions?
```

## Important Principles

1. **ALWAYS plot before running** - Catches 90% of geometry errors
2. **Dashed lines = problems** - Don't ignore them
3. **VOID testing is essential** - Fast way to verify geometry
4. **Simple is better** - Complex geometry = complex debugging
5. **Incremental building** - Test each addition before continuing
6. **Event logs are your friend** - Show exact path to error

## Code Style

When using geometry checker:
- Generate multiple plot commands (3 views minimum)
- Provide specific fixes, not just "fix geometry"
- Show VOID test setup completely
- Explain Boolean operators clearly
- Reference manual sections for learning

## Dependencies

Required components:
- Python module: `skills/validation/mcnp_geometry_checker.py`
- Geometry evaluator: `utils/geometry_evaluator.py`
- Input parser: `parsers/input_parser.py`
- Reference: `.claude/commands/mcnp-geometry-checker.md`

## References

**Primary References:**
- `.claude/commands/mcnp-geometry-checker.md` - Detailed procedures
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Surface types, Boolean operators
- Chapter 3.2.8: VOID card testing and geometry checking
- Chapter 3.4.1: Problem setup (items 1-7 on geometry)
- Chapter 4.8: Geometry errors and detection
- Chapter 6: Plotting geometry

**Key Sections:**
- §5.2: Cell cards (geometry specification)
- §5.3: Surface cards (all surface types)
- Boolean operator precedence rules
- Lost particle debugging procedures

**Related Skills:**
- mcnp-input-validator
- mcnp-geometry-builder
- mcnp-plotter
- mcnp-best-practices-checker
