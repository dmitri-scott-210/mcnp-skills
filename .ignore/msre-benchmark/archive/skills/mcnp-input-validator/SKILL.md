---
name: "MCNP Input Validator"
description: "Validates MCNP input files for syntax errors, cross-references, formatting, and physics settings before expensive simulations. Use when analyzing .inp files or before running MCNP."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Input Validator

## Overview

When a user has an MCNP input file that needs validation before running, or when they're experiencing errors, use this skill to comprehensively check the input for:
- Syntax errors (card format, block structure, delimiters)
- Cross-reference integrity (undefined surfaces, materials, cells)
- Physics settings (MODE, PHYS cards, cross-section libraries)
- Best practices violations (geometry complexity, importance cards)
- Common pitfalls (temperature in Kelvin instead of MeV, etc.)

This skill prevents costly computational time wasted on invalid inputs and helps users understand MCNP's strict format requirements.

## Workflow Decision Tree

### When to Invoke This Skill
- User asks to "check", "validate", or "verify" an MCNP input file
- User mentions MCNP errors or problems
- User is about to run a simulation (proactive validation)
- User is new to MCNP and learning input format
- User has modified an existing input file

### Validation Approach
**Quick Syntax Check:**
- Parse input file structure
- Check block delimiters
- Verify card format basics
→ Use if user just needs basic format validation

**Comprehensive Validation** (recommended default):
- All syntax checks
- Cross-reference validation
- Physics settings check
- Best practices review
→ Use for production runs or when user says "full check"

**Targeted Validation:**
- User specifies specific concern (e.g., "check my materials")
- Focus validation on that aspect
- Still run basic syntax checks
→ Use when user has specific question

## Tool Invocation

This skill includes a Python implementation for automated pre-run validation of MCNP input files.

### Importing the Tool

```python
from mcnp_input_validator import MCNPInputValidator

# Initialize the validator
validator = MCNPInputValidator()
```

### Basic Usage

**Validate Input File**:
```python
# Run comprehensive validation
results = validator.validate_file('path/to/input.inp')

# Check if input is valid
if results['valid']:
    print("✓ Input file passed all validation checks")
else:
    print(f"✗ Found {len(results['errors'])} fatal errors")

# Display all findings
for error in results['errors']:
    print(f"FATAL: {error}")

for warning in results['warnings']:
    print(f"WARNING: {warning}")

for rec in results['recommendations']:
    print(f"RECOMMENDATION: {rec}")
```

**Check Specific Issues**:
```python
# Validate and focus on errors
results = validator.validate_file('reactor.inp')

# Check for cross-reference errors
cross_ref_errors = [e for e in results['errors'] if 'undefined' in e.lower()]
if cross_ref_errors:
    print("Cross-reference issues found:")
    for err in cross_ref_errors:
        print(f"  - {err}")

# Check for material issues
material_errors = [e for e in results['errors'] if 'material' in e.lower()]
if material_errors:
    print("Material definition issues:")
    for err in material_errors:
        print(f"  - {err}")
```

**Pre-Run Quality Check**:
```python
# Validate before submitting expensive calculation
validator = MCNPInputValidator()
results = validator.validate_file('production_run.inp')

if not results['valid']:
    print("CANNOT RUN - Fix these errors first:")
    for i, error in enumerate(results['errors'], 1):
        print(f"{i}. {error}")
    exit(1)

if results['warnings']:
    print("WARNINGS detected - Review before running:")
    for warning in results['warnings']:
        print(f"  ⚠ {warning}")

print("\n✓ Input validation passed - safe to run MCNP")
print(f"Recommendations: {len(results['recommendations'])} suggestions")
for rec in results['recommendations']:
    print(f"  • {rec}")
```

### Integration with MCNP Workflow

```python
from mcnp_input_validator import MCNPInputValidator
import sys

def pre_run_validation(input_file):
    """Validate MCNP input before expensive simulation"""
    print(f"Validating {input_file}...")
    print("=" * 60)

    validator = MCNPInputValidator()
    results = validator.validate_file(input_file)

    # Report fatal errors
    if results['errors']:
        print("\n❌ FATAL ERRORS (must fix before running):")
        for i, error in enumerate(results['errors'], 1):
            print(f"  {i}. {error}")
        print("\n✗ Validation FAILED - cannot run MCNP")
        return False

    # Report warnings
    if results['warnings']:
        print("\n⚠ WARNINGS (should review):")
        for warning in results['warnings']:
            print(f"  • {warning}")

    # Report recommendations
    if results['recommendations']:
        print("\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  • {rec}")

    print("\n✓ Validation PASSED - input file ready")
    print("=" * 60)
    return True

# Example usage
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.inp"

    if pre_run_validation(input_file):
        print(f"\nReady to run: mcnp6 i={input_file}")
    else:
        print("\nFix errors before running MCNP")
        sys.exit(1)
```

---

## Validation Procedure

### Step 1: Initial Assessment
Ask user for context:
- "What input file needs validation?" (get file path)
- "Is this for a production run or learning?"
- "Any specific concerns or errors you're seeing?"
- "Have you plotted the geometry yet?"

### Step 2: Read Reference Materials
**MANDATORY - READ ENTIRE FILE**: Before performing validation, read:
- `.claude/commands/mcnp-input-validator.md` - Complete validation procedures and checklists
- If needed: `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Quick reference for card formats

### Step 3: Run Validation
Use the Python validation module (see **Tool Invocation** section above for detailed usage):

```python
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
results = validator.validate_file('path/to/input.inp')

# Results structure:
# {
#     'errors': [list of FATAL errors],
#     'warnings': [list of warnings],
#     'recommendations': [best practice suggestions],
#     'valid': boolean
# }
```

### Step 4: Report Findings
Organize results by severity:

**FATAL ERRORS** (must fix before running):
- List all fatal errors first
- Explain each error clearly
- Show how to fix with examples
- Reference manual sections

**WARNINGS** (should review):
- Unconventional settings
- Potential issues
- Explain why it matters

**RECOMMENDATIONS** (best practices):
- Geometry plotting suggestions
- VOID card testing
- Statistical quality improvements

### Step 5: Guide User to Fix
For each error:
- Explain what's wrong
- Show correct syntax
- Reference chapter/section
- Offer to help implement fix

## Common Validation Checks

### Block Structure (Chapter 4)
```
MESSAGE: [optional]
[blank line]
TITLE CARD
[cell cards...]
[blank line]
[surface cards...]
[blank line]
[data cards...]
[optional blank line terminator]
```

**Common errors:**
- No blank line between blocks → FATAL
- Extra blank lines → Cards ignored
- Missing title card → FATAL
- Cards in wrong block → FATAL

### Cross-References (Chapter 4.4)
Check all references resolve:
- Cells → Surfaces (geometry expressions)
- Cells → Materials (M card numbers)
- Tallies → Cells/Surfaces
- FM cards → Materials
- TRCL → TR cards
- FILL → Universe numbers
- IMP cards → Match cell count

**Example check:**
```python
# Cell 10 has geometry: -1 2 -3 (4:5)
# Verify surfaces 1, 2, 3, 4, 5 are all defined
```

### Physics Settings (Chapter 4.5 & 5.7)
**MODE Card:**
- Check particle types appropriate for problem
- MODE N P → Neutron with photon production
- MODE P E → Coupled photon-electron

**PHYS Cards:**
- Energy ranges cover source energies
- Secondary production enabled when needed
- Physics approximations appropriate

**Cross Sections:**
- ZAID format: ZZZAAA or ZZZAAA.XXc
- Library suffixes match particle types:
  - .80c = ENDF/B-VIII.0 (neutron)
  - .24p = Photoatomic
  - .03e = Electron

**Example validation:**
```python
# If MODE N P, check:
# 1. Neutron cross sections (.XXc)
# 2. Photoatomic data (.XXp) if needed
# 3. PHYS:N emax ≥ max source energy
# 4. Photon production enabled (ngam on PHYS:N)
```

### Importance Cards (Chapter 3.2.5.2)
**Critical rule:** One entry per cell
```
IMP:N 1 1 1 0  # Must have exactly N entries for N cells
```

**Common errors:**
- Count mismatch → FATAL (or WARNING with zeros assumed)
- No importance cards → Particles trapped
- All zeros → No particles transported

### Material Specifications (Chapter 5.6)
Check materials:
- All used materials defined (M cards)
- Density specified for non-void cells
- ZAID format valid
- Fractions don't mix atomic/weight
- TMP in MeV not Kelvin!

**Example:**
```
c CORRECT:
M1 92235.80c 1      $ U-235, ENDF/B-VIII.0
   92238.80c 4      $ U-238

c WRONG:
M1 92235 1          $ Missing library suffix
   92238.70c 4      $ Inconsistent libraries
```

### Geometry Errors (Chapter 4.8)
**Cannot detect until particles run, but check for:**
- Unused surfaces (may indicate incomplete geometry)
- Overly complex Boolean expressions
- Excessive # operators
- Missing outside world cell (IMP=0)

**Recommend:**
- Geometry plotting from 3 views
- VOID card testing
- Pre-calculated volumes comparison

## Error Severity Levels

### FATAL (Terminates before running particles)
- Missing/extra blank line delimiters
- Card name in wrong columns
- Undefined cross-references
- Invalid card syntax
- Block structure violations

→ **Must fix before ANY run**

### WARNING (Unconventional, may need attention)
- No importance cards
- Zero importance without escape
- Unusual physics settings
- Missing thermal scattering

→ **Should understand before production**

### COMMENT (Informational)
- Code notes about defaults
- Conversion notifications
- Feature usage notes

→ **Review but often okay**

### RECOMMENDATION (Best practices)
- Plot geometry before running
- Use VOID card for testing
- Pre-calculate masses/volumes
- Check cross-section datasets

→ **Follow for reliable results**

## Integration with Other Skills

After validation, recommend:
- **mcnp-geometry-checker**: For detailed geometry analysis
- **mcnp-physics-validator**: For detailed physics settings
- **mcnp-cross-reference-checker**: For dependency mapping
- **mcnp-best-practices-checker**: For comprehensive best practices

## Example Validation Workflow

```
User: "Can you validate my reactor input file?"

Claude: I'll comprehensively validate your MCNP input file for syntax, cross-references, and physics settings.

[Reads .claude/commands/mcnp-input-validator.md]
[Uses MCNPInputValidator Python module]

**Validation Results for reactor.inp:**

FATAL ERRORS (must fix before running):
❌ 1. Line 45: Cell 10 references undefined surface 203
   Location: Cell geometry "-1 2 -203 4"
   Fix: Add surface definition for 203, or correct cell 10 geometry
   Reference: Chapter 5.3 (Surface Cards)

❌ 2. Line 78: Material 5 used in cell 8 but M5 card not defined
   Location: Cell card "8 5 -2.7 -10 11 -12 13"
   Fix: Add M5 material specification in data block
   Reference: Chapter 5.6 (Material Specification)

❌ 3. IMP:N card has 14 entries but 15 cells exist
   Missing: Importance for cell 15
   Fix: Add 15th entry to IMP:N card (suggest value 0 if outside world)
   Reference: Chapter 3.2.5.2 (Cell Parameters)

WARNINGS (should review):
⚠ 1. No MT (thermal scattering) card for water
   Issue: Cell 5 is H2O but no S(α,β) thermal scattering
   Impact: Inaccurate for thermal neutrons
   Fix: Add "MT5 lwtr.20t" for light water thermal scattering
   Reference: §5.6.2 (MT Card)

⚠ 2. Default photon cutoff 1 keV may be high
   Consideration: If tallying low-energy photons
   Optional fix: CUT:P J J -0.001 (for 100 eV cutoff)
   Reference: §5.13 (CUT Card)

RECOMMENDATIONS (best practices):
✓ 1. Plot geometry before running (ESSENTIAL)
   Command: mcnp6 ip i=reactor.inp
   Look for: Dashed lines indicating geometry errors
   Reference: Chapter 6 (Plotting), §3.4.1 item #2

✓ 2. Test with VOID card (recommended)
   Purpose: Quickly find geometry overlaps/gaps
   How: Add VOID card, run with high NPS
   Reference: §3.2.8 (VOID Card Testing)

✓ 3. Verify cross-section libraries in output
   Check: All isotopes loaded from ENDF/B-VIII.0
   Why: Mixed libraries can cause inconsistencies
   Reference: §3.4.1 item #14

**Overall Assessment: NOT VALID**
- 3 FATAL errors must be fixed
- 2 warnings should be addressed
- After fixes, MUST plot geometry

Would you like me to:
1. Help fix these errors?
2. Generate corrected input file?
3. Run detailed geometry check?
4. Check physics settings in detail?
```

## Important Validation Principles

1. **First error is real; subsequent may cascade**
   - Fix errors in order presented
   - Re-validate after each major fix
   - Don't trust all errors if first one is structural

2. **Validation ≠ geometry verification**
   - Input validation checks syntax/format
   - Geometry errors (overlaps/gaps) only found when particles run
   - ALWAYS plot geometry even if validation passes

3. **Cross-section datasets matter**
   - Validation checks format, not data quality
   - User must verify correct libraries loaded
   - Check output file for loaded datasets

4. **Statistics not validated pre-run**
   - Can't check convergence until run completes
   - Recommend NPS values based on problem type
   - Point to statistical validation after run

5. **Best practices are not optional**
   - They exist because people got wrong answers
   - Geometry plotting is MANDATORY
   - VOID testing saves expensive debugging time

## Code Style Guidelines

When using the validation module:
- Run full validation by default
- Present errors before warnings
- Group related issues
- Always provide references to manual
- Offer to help fix, not just identify
- Be specific with line numbers when possible

## Dependencies

Required components:
- Python module: `skills/validation/mcnp_input_validator.py`
- Input parser: `parsers/input_parser.py`
- Geometry evaluator: `utils/geometry_evaluator.py`
- Reference: `.claude/commands/mcnp-input-validator.md` (detailed procedures)

## References

**Primary References:**
- `.claude/commands/mcnp-input-validator.md` - Detailed validation procedures, error catalog
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Quick reference for all input cards
- Chapter 3: Introduction to MCNP Usage (error types, validation methods)
- Chapter 4: Description of MCNP6 Input (card format, structure, limitations)

**Key Sections:**
- §3.4.1: Problem setup checklist (22 items)
- §4.7: Input error messages and types
- §4.8: Geometry errors and detection
- Table 4.1: Code option limitations
- Table 4.2: Numerical limitations on card labels

**Related Skills:**
- mcnp-geometry-checker: Detailed geometry validation
- mcnp-physics-validator: Physics settings deep-dive
- mcnp-cross-reference-checker: Dependency analysis
- mcnp-best-practices-checker: Comprehensive best practices review
