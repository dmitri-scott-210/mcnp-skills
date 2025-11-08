# MCNP Input Builder - Validation Tools

This directory contains Python validation tools for MCNP input files.

---

## validate_numbering.py

### Overview

Validates that MCNP input files follow systematic numbering schemes for cells, surfaces, materials, and universes.

**Checks performed**:
1. **Hierarchical encoding** (XYZSS pattern) - position-based numbering
2. **Subsystem ranges** (10000-blocks) - functional grouping
3. **Universe component encoding** (XYZW pattern) - component type indicators
4. **Correlated numbering** - related entities use related numbers
5. **No conflicts** - unique numbers within each entity type

### Installation

**Requirements**:
- Python 3.6 or higher (no external dependencies)

**Make executable**:
```bash
chmod +x validate_numbering.py
```

### Usage

**Basic usage**:
```bash
python validate_numbering.py input_file.i
```

**With specific scheme**:
```bash
python validate_numbering.py input_file.i --scheme hierarchical
```

**Scheme types**:
- `hierarchical` - Check XYZSS position encoding (5-digit cells)
- `subsystem` - Check 10000-block functional ranges
- `universe` - Check XYZW component encoding
- `auto` - Attempt to detect scheme from file (default)

### Examples

**Example 1: Validate PWR model**
```bash
$ python validate_numbering.py pwr_assembly.i

============================================================
# MCNP NUMBERING SCHEME VALIDATION
# File: pwr_assembly.i
============================================================

Parsed:
  289 cells
  156 surfaces
  12 materials
  3 universes

============================================================
Validating Hierarchical Encoding (XYZSS)
============================================================

✓ Found 289 cells with 5-digit encoding

  Component ranges:
    X (Major): [1, 2]
    Y (Sub):   [0, 1, 2, 3, 4, 5, 6, 7, 8]
    Z (Layer): [0, 1, 2]

============================================================
Validating Subsystem Ranges (10000-blocks)
============================================================

✓ Found 2 distinct 10000-blocks:
    10000-19999:  245 cells
    20000-29999:   44 cells

============================================================
Validating Universe Component Encoding (XYZW)
============================================================

✓ Found 3 universe definitions

  3 universes with 4-digit encoding (XYZW):
    Position 101: u=1010(W=0), u=1011(W=1)
    Position 102: u=1020(W=0)

============================================================
Checking for Numbering Conflicts
============================================================

✓ No duplicate cell numbers (289 cells)
✓ No duplicate surface numbers (156 surfaces)
✓ No duplicate material numbers (12 materials)
✓ No duplicate universe numbers (3 universes)

============================================================
VALIDATION SUMMARY
============================================================

✓ ALL CHECKS PASSED - No errors or warnings

============================================================
```

**Example 2: Detect errors**
```bash
$ python validate_numbering.py bad_input.i

[... parsing output ...]

============================================================
Checking for Numbering Conflicts
============================================================

✗ ERROR: Duplicate cell numbers found: [101, 205]
✗ CRITICAL ERROR: Duplicate universe numbers: [10]

============================================================
VALIDATION SUMMARY
============================================================

✗ ERRORS (2):
  - Duplicate cell numbers: [101, 205]
  - CRITICAL: Duplicate universe numbers: [10]

⚠ WARNINGS (1):
  - Cell 90000: X=9 in XYZSS encoding might be reserved

✗ VALIDATION FAILED - Fix 2 errors before running MCNP

============================================================
```

### Output Interpretation

**Success indicators**:
- ✓ = Check passed
- No errors or warnings

**Warning indicators**:
- ⚠ = Warning (non-critical, but review recommended)
- Examples: Unusual patterns, potential issues

**Error indicators**:
- ✗ = Error (critical, must fix before running)
- Examples: Duplicate numbers, out-of-range values

### What It Validates

#### 1. Hierarchical Encoding (XYZSS)

Checks for 5-digit cell numbers encoding position:
- X = Major component (1-9)
- Y = Sub-component (0-9)
- Z = Layer/level (0-9)
- SS = Sequence (00-99)

**Example**: Cell 11234 → Component 1, Sub 1, Layer 2, Sequence 34

**Validates**:
- X is 1-9 (not 0)
- All digits are single-digit
- Consistent usage across model

#### 2. Subsystem Ranges (10000-blocks)

Checks for functional grouping in 10000-number blocks:
- 10000-19999: Fuel assemblies
- 20000-29999: Control rods
- 30000-39999: Reflector
- etc.

**Validates**:
- Cells grouped into distinct blocks
- No mixing of subsystems
- Clear functional separation

#### 3. Universe Component Encoding (XYZW)

Checks universe numbering with component type indicator:
- XYZ = Position (same as cell encoding)
- W = Component type (0-9)

**Common W values**:
- 0 = Lattice container
- 1 = Primary component (fuel)
- 4 = Special (TRISO particle)
- 5 = Matrix/filler
- 6 = Sub-lattice

**Validates**:
- Same position uses same XYZ, different W
- W is single digit (0-9)
- No duplicate universes

#### 4. Correlated Numbering

Checks if related entities use related numbers:
- Cell 11234 → Surface 11234 → Material 1123

**Validates**:
- Cell/surface correlation
- Cell/material base number correlation
- Logical grouping

#### 5. No Conflicts

Critical check for duplicate numbers:

**MUST be unique**:
- Cell numbers (within global model)
- Surface numbers (within global model)
- Material numbers (within global model)
- **Universe numbers (CRITICAL - MUST be globally unique!)**

**Can be reused** (but discouraged):
- Cell 100 and Surface 100 are different entities (okay but confusing)

### Common Error Messages

#### "Duplicate cell numbers"
```
✗ ERROR: Duplicate cell numbers: [101, 205]
```
**Fix**: Renumber cells to ensure uniqueness

#### "Duplicate universe numbers"
```
✗ CRITICAL ERROR: Duplicate universe numbers: [10]
```
**Fix**: Universes MUST be unique - this is a FATAL MCNP error

#### "X=0 in XYZSS encoding"
```
⚠ WARNING: Cell 10123: X=0 in XYZSS encoding (should be 1-9)
```
**Fix**: Consider renumbering to use X=1-9 (0 is valid but breaks pattern)

### Limitations

**Current limitations**:
1. Does not validate surface references (use cross_reference_validator.py)
2. Does not check material references
3. Does not parse continuation lines
4. Does not validate comment conventions
5. Basic parsing (may miss complex card formats)

**Future enhancements**:
1. Cross-reference validation
2. Continuation line support
3. More sophisticated scheme detection
4. Custom scheme configuration file
5. HTML report generation

### Integration with Other Tools

**Workflow**:
1. **validate_numbering.py** - Check numbering scheme (this tool)
2. **validate_cross_references.py** - Check all entities exist
3. **mcnp6 ip** - Plot geometry visually
4. **mcnp6 (small NPS)** - Run quick test

**Use with mcnp-input-validator skill**:
This tool complements the mcnp-input-validator skill:
- **This tool**: Validates numbering conventions
- **Validator skill**: Validates MCNP syntax, three-block structure, etc.

### Exit Codes

- `0` = Success (no errors, warnings okay)
- `1` = Failure (errors found, must fix)

**Use in scripts**:
```bash
#!/bin/bash
if python validate_numbering.py input.i; then
    echo "Numbering validation passed"
    mcnp6 i=input.i
else
    echo "Fix numbering errors before running MCNP"
    exit 1
fi
```

---

## Future Tools (Planned)

### validate_cross_references.py
- Check surface/material/universe references
- Validate universe hierarchy
- Detect circular references

### generate_numbering_template.py
- Generate numbering scheme from specification
- Auto-number cells/surfaces based on pattern
- Renumber existing files to new scheme

### analyze_numbering_scheme.py
- Reverse-engineer numbering scheme from file
- Generate documentation of detected scheme
- Suggest improvements

---

## Contributing

To add new validation checks:

1. Edit `validate_numbering.py`
2. Add new method `validate_NEW_CHECK(self)`
3. Call from `validate_all()` method
4. Update this README with new check description
5. Add test cases

---

## Questions and Issues

If the validator:
- **Gives false positives**: Check if file uses non-standard scheme
- **Misses errors**: Report specific case for improvement
- **Crashes**: Check Python version (needs 3.6+)

For complex numbering schemes not detected, consider:
- Adding scheme config in file header (c NUMBERING SCHEME: ...)
- Using `--scheme` flag to specify type explicitly
- Modifying script for custom patterns

---

**Last Updated**: 2024-11-08
**Version**: 1.0
**Python Requirements**: 3.6+
