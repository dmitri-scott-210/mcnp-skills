# MCNP Input Validator Scripts

## Overview

This directory contains Python scripts for automated MCNP input file validation. These scripts implement the validation procedures described in the skill reference files.

**Version:** 2.0.0
**Python Required:** 3.8+

---

## Scripts

### 1. mcnp_input_validator.py (Main Engine)

**Purpose:** Comprehensive MCNP input validation

**Features:**
- Block structure validation
- Card syntax checking
- Cross-reference validation
- Physics consistency checking
- Best practice recommendations

**Usage:**

```python
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
results = validator.validate_file('input.inp')

if results['valid']:
    print("✓ Validation passed")
else:
    for error in results['errors']:
        print(f"ERROR: {error}")
```

**Command Line:**

```bash
python mcnp_input_validator.py input.inp
```

**Output:**

```
============================================================
MCNP INPUT VALIDATOR v2.0.0
============================================================
Validating: input.inp

============================================================
FATAL ERRORS (must fix before running)
============================================================
1. FATAL: Invalid blank line count. Expected 2, found 3...

============================================================
STATUS: FAILED - Fix errors before running
============================================================
```

---

### 2. block_structure_validator.py

**Purpose:** Specialized validation for three-block structure

**Features:**
- Checks for exactly 2 blank lines
- Verifies title card present
- Ensures three blocks non-empty
- Reports block boundaries

**Usage:**

```python
from block_structure_validator import validate_block_structure

errors = validate_block_structure('input.inp')
if errors:
    for error in errors:
        print(f"ERROR: {error}")
```

**Command Line:**

```bash
python block_structure_validator.py input.inp
```

**Output:**

```
Validating block structure: input.inp
============================================================
✓ Block structure valid

Block boundaries:
  Cell Cards:    Lines 1-45
  Surface Cards: Lines 47-78
  Data Cards:    Lines 80-150
```

---

### 3. cross_reference_checker.py

**Purpose:** Validate cross-references between entities

**Features:**
- Cell geometry → Surface definitions
- Cell material → Material definitions
- Reports undefined references

**Usage:**

```python
from cross_reference_checker import check_cross_references

errors = check_cross_references('input.inp')
if errors:
    for error in errors:
        print(f"ERROR: {error}")
```

**Command Line:**

```bash
python cross_reference_checker.py input.inp
```

**Output:**

```
Checking cross-references: input.inp
============================================================
CROSS-REFERENCE ERRORS:
1. FATAL: Cell 10 geometry references undefined surface 203
2. FATAL: Cell 8 uses material 5, but M5 card not defined
```

---

### 4. physics_consistency_checker.py

**Purpose:** Validate physics settings consistency

**Features:**
- MODE card presence
- PHYS cards for MODE particles
- Cross-section library consistency
- Reports warnings, not fatal errors

**Usage:**

```python
from physics_consistency_checker import check_physics_consistency

warnings = check_physics_consistency('input.inp')
for warning in warnings:
    print(f"WARNING: {warning}")
```

**Command Line:**

```bash
python physics_consistency_checker.py input.inp
```

**Output:**

```
Checking physics consistency: input.inp
============================================================
PHYSICS WARNINGS:
1. WARNING: PHYS:P card missing - MCNP will use defaults
2. WARNING: Mixed cross-section libraries detected: {'70', '80'}
```

---

## Complete Validation Workflow

**Recommended usage integrating all scripts:**

```python
from mcnp_input_validator import MCNPInputValidator
from block_structure_validator import validate_block_structure
from cross_reference_checker import check_cross_references
from physics_consistency_checker import check_physics_consistency

def complete_validation(input_file):
    """
    Run complete validation pipeline.
    """
    print("="*60)
    print(f"Complete Validation: {input_file}")
    print("="*60)

    # Step 1: Block structure
    print("\n1. Checking block structure...")
    structure_errors = validate_block_structure(input_file)
    if structure_errors:
        print("  FAILED - Fix structure errors first")
        for error in structure_errors:
            print(f"    {error}")
        return False
    print("  ✓ PASSED")

    # Step 2: Cross-references
    print("\n2. Checking cross-references...")
    xref_errors = check_cross_references(input_file)
    if xref_errors:
        print("  FAILED - Fix cross-reference errors")
        for error in xref_errors:
            print(f"    {error}")
        return False
    print("  ✓ PASSED")

    # Step 3: Physics consistency
    print("\n3. Checking physics consistency...")
    physics_warnings = check_physics_consistency(input_file)
    if physics_warnings:
        print("  WARNINGS detected:")
        for warning in physics_warnings:
            print(f"    {warning}")
    else:
        print("  ✓ PASSED")

    # Step 4: Comprehensive validation
    print("\n4. Running comprehensive validation...")
    validator = MCNPInputValidator()
    results = validator.validate_file(input_file)

    if not results['valid']:
        print("  FAILED")
        return False

    print("  ✓ PASSED")

    # Print recommendations
    if results['recommendations']:
        print("\nRECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  • {rec}")

    print("\n" + "="*60)
    print("VALIDATION COMPLETE - Input file ready for geometry verification")
    print("="*60)
    print("\nNEXT STEPS:")
    print("1. Plot geometry: mcnp6 ip i=" + input_file)
    print("2. Run VOID test (recommended)")
    print("3. Execute MCNP simulation")

    return True

# Example usage
if __name__ == '__main__':
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.inp'
    success = complete_validation(input_file)
    sys.exit(0 if success else 1)
```

---

## Integration with MCNP Workflow

### Pre-Run Validation Script

```python
#!/usr/bin/env python3
"""
Pre-run validation script for MCNP inputs.
Use before expensive simulations.
"""

from mcnp_input_validator import MCNPInputValidator
import sys

def pre_run_check(input_file):
    """Validate input before MCNP execution."""
    validator = MCNPInputValidator()
    results = validator.validate_file(input_file)

    if not results['valid']:
        print("\n❌ VALIDATION FAILED")
        print("\nCannot run MCNP until these errors are fixed:")
        for error in results['errors']:
            print(f"  • {error}")
        return False

    if results['warnings']:
        print("\n⚠ WARNINGS detected:")
        for warning in results['warnings']:
            print(f"  • {warning}")
        print("\nReview warnings before production run.")

    print("\n✓ VALIDATION PASSED")
    print(f"\nReady to run: mcnp6 i={input_file}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pre_run_check.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    success = pre_run_check(input_file)
    sys.exit(0 if success else 1)
```

**Usage:**

```bash
python pre_run_check.py reactor.inp && mcnp6 i=reactor.inp
```

This ensures MCNP only runs if validation passes.

---

## Installation

**No external dependencies required** - uses Python standard library only.

**Verify Python version:**

```bash
python --version  # Should be 3.8 or higher
```

**Make scripts executable (Unix/Linux/Mac):**

```bash
chmod +x *.py
```

---

## Error Codes

**Fatal Errors (prevent execution):**
- F-001: Missing/extra blank lines
- F-002: Blank lines within blocks
- F-003: Missing title card
- F-004: Undefined surface reference
- F-005: Undefined material reference
- F-006: IMP card entry count mismatch

**Warnings (should review):**
- W-001: Missing thermal scattering
- W-002: TMP appears to be in Kelvin
- W-003: No importance cards
- W-004: PHYS energy range issues
- W-005: Mixed cross-section libraries

**See:** `../error_catalog.md` for complete error reference

---

## Validation Levels

### Quick Validation (< 1 second)

```python
from block_structure_validator import validate_block_structure

errors = validate_block_structure('input.inp')
```

**Checks:**
- Block structure only
- Fastest validation
- Use during active development

---

### Standard Validation (1-2 seconds)

```python
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
results = validator.validate_file('input.inp')
```

**Checks:**
- Block structure
- Cross-references
- Basic physics
- Use before test runs

---

### Comprehensive Validation (2-5 seconds)

```python
# Use complete_validation() function above
complete_validation('input.inp')
```

**Checks:**
- All standard checks
- Detailed physics analysis
- Best practice recommendations
- Use before production runs

---

## Testing

**Test the validator scripts:**

```bash
# Test with invalid input (should fail)
python mcnp_input_validator.py ../assets/example_inputs/01_missing_blank_line_INVALID.i

# Test with fixed input (should pass)
python mcnp_input_validator.py ../assets/example_inputs/01_missing_blank_line_FIXED.i
```

**Expected output for INVALID file:**

```
FATAL ERRORS (must fix before running)
1. FATAL: Invalid blank line count. Expected 2, found 0...

STATUS: FAILED - Fix errors before running
```

**Expected output for FIXED file:**

```
STATUS: PASSED - Input validation successful

READY FOR NEXT STEPS:
1. Plot geometry (ESSENTIAL)
2. Run VOID test (RECOMMENDED)
3. Execute MCNP simulation
```

---

## Extension and Customization

**To add custom validation checks:**

1. Create new checker class following existing pattern
2. Implement `check_file(filepath)` method
3. Return list of errors/warnings
4. Integrate into `MCNPInputValidator.validate_file()`

**Example:**

```python
class CustomChecker:
    def check_file(self, filepath):
        errors = []
        # Add custom checks here
        return errors
```

---

## Troubleshooting

### Script won't run

**Problem:** `python: command not found`
**Solution:** Use `python3` instead of `python`

**Problem:** `ModuleNotFoundError`
**Solution:** Ensure scripts are in same directory or adjust PYTHONPATH

### Validation fails on valid input

**Problem:** Known good input fails validation
**Solution:**
1. Check MCNP version compatibility
2. Verify manual reference version matches
3. Report issue with example file

### Performance issues

**Problem:** Validation takes >30 seconds
**Solution:**
1. Check file size (>100,000 lines unusual)
2. Use quick validation for large files
3. Profile code to identify bottleneck

---

## References

**Skill References:**
- `../validation_procedures.md` - Detailed validation algorithms
- `../error_catalog.md` - Complete error reference
- `../validation_checklists.md` - Manual validation checklists
- `../integration_guide.md` - Integration with other skills

**MCNP6 Manual:**
- Chapter 4: Input File Format
- §4.4: Cross-Reference Requirements
- §4.7: Input Error Messages

**Related Skills:**
- mcnp-input-builder: Input structure standards
- mcnp-geometry-builder: Cell/surface standards
- mcnp-material-builder: Material standards

---

## Support

For issues or questions:
1. Check `../error_catalog.md` for error explanations
2. Review `../validation_procedures.md` for detailed algorithms
3. Consult MCNP6 Manual referenced sections
4. Contact skill maintainer

---

**END OF SCRIPTS README**

Use these scripts systematically before every MCNP run to catch errors early and save computational time.
