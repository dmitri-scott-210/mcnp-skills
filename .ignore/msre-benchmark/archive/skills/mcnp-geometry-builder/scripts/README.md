# MCNP Geometry Builder - Python Scripts

This directory contains Python helper scripts for geometry validation and visualization.

## Available Scripts

### 1. geometry_validator.py
Pre-MCNP validation for catching geometry errors before running expensive simulations.

### 2. geometry_plotter_helper.py
Automated generation of MCNP plot commands for comprehensive geometry visualization.

---

## Script 1: geometry_validator.py

### Purpose
Validates MCNP geometry input files for common errors **before** running MCNP. Catches structural errors, cross-reference issues, and syntax problems that would cause MCNP to fail.

### Usage
```bash
python geometry_validator.py input_file.inp
```

### Validation Checks

**1. File Structure (CRITICAL)**
- ✅ Verifies EXACTLY 2 blank lines (one after Cell Cards, one after Surface Cards)
- ✅ Detects illegal blank lines WITHIN blocks (common error from Session 7!)
- ✅ Checks title card presence
- ✅ Validates 3-block format

**2. Cross-Reference Validation**
- ✅ Cell → Material references (checks M cards exist)
- ✅ Cell → Surface references (basic validation)
- ✅ Surface → Transformation references (TR cards)
- ✅ Identifies undefined materials, surfaces, transformations

**3. Syntax Checks**
- ✅ Line length (128 character MCNP limit)
- ✅ Tab character detection (should use spaces)
- ✅ RHP/HEX macrobody validation (minimum 9 values)
- ✅ Comment syntax validation

### Output

**Exit Codes:**
- `0` - Validation passed (no errors)
- `1` - Errors found (fix before running MCNP)
- `2` - File not found or invalid format

**Report Format:**
```
======================================================================
MCNP Geometry Validation Report: example.inp
======================================================================

❌ ERRORS (2):
  1. CRITICAL: MCNP requires EXACTLY 2 blank lines (found 4)...
  2. Cell 10 references undefined material M5

⚠️  WARNINGS (1):
  1. Line 45 exceeds 128 characters (MCNP limit)

ℹ️  INFO:
  - Title: Simple PWR Pin Cell Model
  - Cell cards: 15 lines
  - Surface cards: 22 lines
  - Data cards: 45 lines
  - Defined cells: [1, 2, 3, 4, 5]
  - Defined surfaces: [1, 2, 3, 4, 10, 20, 99]
  - Defined materials: [1, 2, 3, 4]
  - Defined transformations: []

======================================================================
❌ VALIDATION FAILED - Fix errors before running MCNP
```

### Example Workflow
```bash
# 1. Create MCNP input file
vim reactor_model.inp

# 2. Validate before running MCNP
python geometry_validator.py reactor_model.inp

# 3. Fix any errors reported

# 4. Re-validate until clean
python geometry_validator.py reactor_model.inp
# ✅ VALIDATION PASSED - No errors found

# 5. NOW run MCNP (expensive simulation)
mcnp6 inp=reactor_model.inp outp=reactor.out
```

### Common Errors Detected

**1. Blank Line Errors (Most Common)**
```
❌ CRITICAL: MCNP requires EXACTLY 2 blank lines (found 5)
❌ ILLEGAL: Blank lines found WITHIN blocks
```
**Fix:** Remove all blank lines except those between blocks.

**2. Undefined References**
```
❌ Cell 10 references undefined material M5
```
**Fix:** Add `M5` card in data block or correct cell 10 material number.

**3. RHP/HEX Format Errors**
```
❌ Surface card line 12: RHP/HEX requires minimum 9 values (found 7)
```
**Fix:** RHP format is `vx vy vz h1 h2 h3 r1 r2 r3` (9 values, not 7).

---

## Script 2: geometry_plotter_helper.py

### Purpose
Generates MCNP plot commands for comprehensive geometry visualization. Creates both batch plotting files (.comin) and interactive command references.

### Usage
```bash
# Basic usage (default: 3 slices per axis)
python geometry_plotter_helper.py input_file.inp

# Custom slices and origin
python geometry_plotter_helper.py input_file.inp --slices 5 --origin 0 0 50

# Custom extent and output file
python geometry_plotter_helper.py input_file.inp --extent 100 --output my_plots.comin
```

### Options
```
--slices N           Number of slices along each axis (default: 3)
--origin X Y Z       Plot origin coordinates (default: 0 0 0)
--extent E           Plot extent in cm (default: auto-detect)
--output FILE        Output file for plot commands (default: geometry_plots.comin)
```

### Generated Files

**1. geometry_plots.comin** - Batch plot commands
- Multi-slice plots along all three axes
- Cell-labeled and material-labeled views
- Ready to use with: `mcnp6 inp=file.i com=geometry_plots.comin`

**2. geometry_plots_interactive.txt** - Interactive commands
- Copy-paste commands for interactive plotter (`mcnp6 inp=file.i ip`)
- Includes useful plotter commands reference

### Output Example
```bash
$ python geometry_plotter_helper.py reactor.inp --slices 3

Found 25 cells and 35 surfaces
✅ Plot commands saved to: geometry_plots.comin
   Run with: mcnp6 inp=reactor.inp com=geometry_plots.comin
✅ Interactive commands saved to: geometry_plots_interactive.txt

======================================================================
📊 Plot Generation Complete!
======================================================================

Usage:
  1. Batch plotting:  mcnp6 inp=reactor.inp com=geometry_plots.comin
  2. Interactive:     mcnp6 inp=reactor.inp ip
     Then copy commands from: geometry_plots_interactive.txt

Tip: Use 'label 1 1 cel' for cell numbers, 'label 1 1 mat' for materials
```

### Generated Plot Structure

For `--slices 3`, generates:
- **XY slices:** 3 plots perpendicular to Z-axis (Z_min, Z_center, Z_max)
- **XZ slices:** 3 plots perpendicular to Y-axis
- **YZ slices:** 3 plots perpendicular to X-axis
- **Total:** 18 plots (3 × 3 axes × 2 label types [cell + material])

### Example Workflow

**Batch Plotting (Automated):**
```bash
# 1. Generate plot commands
python geometry_plotter_helper.py fuel_assembly.inp --slices 5

# 2. Run batch plotting
mcnp6 inp=fuel_assembly.inp com=geometry_plots.comin

# 3. View generated plot files (*.ps PostScript files)
# Use viewer or convert to PDF/PNG
```

**Interactive Plotting (Manual Exploration):**
```bash
# 1. Generate interactive commands
python geometry_plotter_helper.py fuel_assembly.inp

# 2. Start interactive plotter
mcnp6 inp=fuel_assembly.inp ip

# 3. In MCNP plotter, copy commands from geometry_plots_interactive.txt
#    Example commands:
origin 0 0 0
extent 50
px 0 0 0
label 1 1 cel
# ... etc
```

### Interactive Plotter Commands Reference

**Basic Navigation:**
```
origin X Y Z     - Set plot center
extent E         - Set plot size
scale F          - Zoom (F < 1 = zoom in, F > 1 = zoom out)
```

**Plot Planes:**
```
px X Y Z         - XY plane perpendicular to X-axis passing through (X,Y,Z)
py X Y Z         - XZ plane perpendicular to Y-axis
pz X Y Z         - YZ plane perpendicular to Z-axis
```

**Labels and Colors:**
```
label 1 1 cel    - Show cell numbers
label 1 1 mat    - Show material numbers
label 1 0        - Hide labels
color N R G B    - Set cell N color (RGB values 0-255)
```

**Basis Vectors (Advanced):**
```
basis U V        - Set plot orientation using basis vectors
```

**Other:**
```
plot             - Generate plot with current settings
end              - Exit plotter
```

---

## Integration with Claude Code Skill

These scripts are designed to be used with the `mcnp-geometry-builder` skill:

### Validation Integration
```python
# User asks: "Validate my geometry before running"
# Claude invokes skill, then:

# Step 1: Use geometry_validator.py
validator_result = run_bash("python scripts/geometry_validator.py user_file.inp")

# Step 2: Report results to user
if validator_result.exit_code == 0:
    print("✅ Validation passed! Safe to run MCNP.")
else:
    print("❌ Errors found. Please fix before running MCNP.")
    print(validator_result.stdout)
```

### Plotting Integration
```python
# User asks: "Generate plot commands for my geometry"
# Claude invokes skill, then:

# Generate plot commands
plot_result = run_bash("python scripts/geometry_plotter_helper.py user_file.inp --slices 5")

# Inform user
print("📊 Plot commands generated:")
print("   Batch: mcnp6 inp=user_file.inp com=geometry_plots.comin")
print("   Interactive: mcnp6 inp=user_file.inp ip")
```

---

## Installation Requirements

**Python Version:** Python 3.6+

**Dependencies:** None (uses only standard library)
- `sys`, `re`, `pathlib`, `typing`, `dataclasses`, `argparse`

**No pip install required!**

---

## Troubleshooting

### geometry_validator.py

**Issue: "File not found"**
```bash
❌ File not found: example.inp
```
**Fix:** Check file path, ensure .inp file exists

**Issue: "Cannot parse blocks: insufficient blank line delimiters"**
**Fix:** MCNP file must have 2 blank lines (one after cells, one after surfaces)

### geometry_plotter_helper.py

**Issue: No plots generated**
**Fix:** Ensure MCNP6 is installed and in PATH. Run: `mcnp6 inp=file.i com=plots.comin`

**Issue: Plots show wrong extent**
**Fix:** Use `--extent` option: `python geometry_plotter_helper.py file.inp --extent 200`

---

## Extending the Scripts

### Adding New Validation Checks

Edit `geometry_validator.py`, add method to `MCNPGeometryValidator` class:

```python
def _check_new_feature(self):
    """Check for new feature"""
    for line in self.cell_cards:
        # Your validation logic
        if condition:
            self.results.errors.append("Error message")
```

Then call from `validate()` method:
```python
def validate(self) -> ValidationResult:
    # ... existing checks ...
    self._check_new_feature()  # Add your check
    return self.results
```

### Customizing Plot Generation

Edit `geometry_plotter_helper.py`, modify `generate_slice_plots()`:

```python
def generate_slice_plots(self) -> List[str]:
    commands = []
    # Add custom plot commands
    commands.append("c My custom plot")
    commands.append("px 0 0 10")
    commands.append("color 1 255 0 0")  # Cell 1 = red
    # ...
    return commands
```

---

## Future Enhancements

**Planned Features:**
1. **Advanced cross-reference validation** - Detect complex surface reference errors
2. **Universe/FILL validation** - Check LAT=1/LAT=2 consistency
3. **Geometry bounds detection** - Auto-detect extent from surface definitions
4. **3D visualization** - Generate VTK files for ParaView
5. **Comparison tool** - Diff two input files for geometry changes

**Contributions Welcome:** These scripts are starting points for geometry workflow automation.

---

## References

- **MCNP6 User Manual, Chapter 4:** Input file format specifications
- **MCNP6 User Manual, Chapter 5:** Cell and surface card syntax
- **MCNP6 User Manual, Chapter 6:** Geometry plotting commands

---

**Last Updated:** Session 8 (2025-11-03)
**Skill Version:** mcnp-geometry-builder v2.0.0
