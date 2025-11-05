---
name: mcnp-input-validator
description: "Validates MCNP input files for syntax errors, cross-references, formatting, and physics settings before simulations. Use when checking .i/.inp files or debugging MCNP errors."
version: "2.0.0"
dependencies: "python>=3.8, mcnp-input-builder, mcnp-geometry-builder, mcnp-material-builder"
---

# MCNP Input Validator

## Overview

Validate MCNP input files comprehensively before simulation execution to catch errors early and prevent wasted computational time. This skill performs systematic checks for syntax errors, cross-reference integrity, physics consistency, and format compliance based on standards from completed builder skills.

Input validation cannot detect geometry errors (overlaps/gaps) - those require geometry plotting and VOID card testing. Validation ensures the input file is syntactically correct and internally consistent before particles are transported.

Use this skill as the first step in the pre-run quality assurance workflow, followed by geometry verification and test runs.

## When to Use This Skill

- Validating MCNP input file before expensive simulation
- Debugging MCNP fatal errors or warnings
- Checking input file after major modifications
- Learning MCNP format requirements
- Pre-production quality assurance
- Peer review of input files
- Systematic error prevention
- Integration testing of builder skill outputs
- Verification after batch editing operations
- Quality control for critical calculations

## Decision Tree

```
User has MCNP input file
  ↓
Validation needed?
  ├─→ Just edited file → Quick validation (block structure)
  ├─→ Before test run → Standard validation (full checks)
  └─→ Before production → Comprehensive + geometry plot + VOID test
       ↓
Run validation (this skill)
       ↓
Results?
  ├─→ FATAL errors → Fix in order → Re-validate
  ├─→ Warnings → Review → Decide if acceptable
  └─→ Passed → MUST plot geometry (not optional)
       ↓
Geometry valid?
  ├─→ No (dashed lines) → Fix geometry → Re-validate from start
  └─→ Yes (clean plots) → VOID test (recommended)
       ↓
VOID test clean?
  ├─→ Lost particles → Fix geometry → Re-validate
  └─→ Clean → Ready for production run
```

## Quick Reference

| Check Category | Fatal? | Examples | Tool |
|----------------|--------|----------|------|
| **Block Structure** | Yes | Missing blank lines, extra blanks within blocks | `block_structure_validator.py` |
| **Cross-References** | Yes | Undefined surface, undefined material, IMP count mismatch | `cross_reference_checker.py` |
| **Card Syntax** | Yes | Invalid ZAID format, wrong parameter count, unrecognized mnemonic | `mcnp_input_validator.py` |
| **Physics Consistency** | Warning | MODE missing, PHYS cards absent, mixed libraries | `physics_consistency_checker.py` |
| **Best Practices** | Recommendation | Plot geometry, VOID test, check statistics | All validators |

## Use Cases

### Use Case 1: Pre-Run Validation (Standard Workflow)

**Scenario:** Have MCNP input file ready to run, want to catch errors before expensive simulation.

**Goal:** Verify input is syntactically correct and internally consistent.

**Implementation:**
```python
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
results = validator.validate_file('reactor.inp')

if not results['valid']:
    print("CANNOT RUN - Fix errors first:")
    for error in results['errors']:
        print(f"  • {error}")
    exit(1)

print("✓ Validation passed")
print("Next: Plot geometry (mcnp6 ip i=reactor.inp)")
```

**Key Points:**
- Run validation BEFORE executing MCNP
- Fix FATAL errors in order presented
- Review warnings for potential issues
- Always plot geometry even if validation passes
- Validation does not replace geometry verification

**Expected Results:** Clear pass/fail with specific error locations and fixes

---

### Use Case 2: Debugging MCNP Fatal Error

**Scenario:** MCNP run terminated with fatal error, need to identify and fix issue.

**Goal:** Quickly locate and understand the error.

**Implementation:**
1. Run validator on input file
2. Check for matching error in validator results
3. Reference error_catalog.md for detailed fix
4. Correct input file
5. Re-validate before running MCNP again

**Key Points:**
- Validator catches most common fatal errors
- Error catalog provides detailed fixes
- Fix errors before re-running MCNP (don't waste compute time)
- Some errors only appear when particles run (geometry issues)

---

### Use Case 3: Learning MCNP Format

**Scenario:** New to MCNP, learning input format requirements, making frequent mistakes.

**Goal:** Understand MCNP format rules through validation feedback.

**Implementation:**
- Edit input file
- Run quick validation after each change
- Read error messages and references
- Consult validation_checklists.md for systematic learning
- Build understanding incrementally

**Key Points:**
- Validator is educational tool
- Error messages reference manual sections
- Examples show before/after corrections
- Checklists explain requirements systematically

---

### Use Case 4: Production Run Quality Assurance

**Scenario:** Critical calculation for publication/licensing, must ensure input quality.

**Goal:** Comprehensive validation with documentation.

**Implementation:**
1. Run comprehensive validation (all checks)
2. Document validation results
3. Peer review with validation report
4. Plot geometry from 3 views
5. Run VOID test with high NPS
6. Document all QA steps
7. Proceed only if all checks pass

**Key Points:**
- Use comprehensive validation checklist
- Document every check performed
- Independent peer review
- Zero tolerance for unresolved warnings
- Create audit trail for critical work

---

### Use Case 5: Batch Input File Validation

**Scenario:** Modified multiple input files, need to validate all before running campaign.

**Goal:** Systematic validation of many files efficiently.

**Implementation:**
```python
import glob
from mcnp_input_validator import MCNPInputValidator

validator = MCNPInputValidator()
input_files = glob.glob("*.inp")

failed_files = []
for input_file in input_files:
    results = validator.validate_file(input_file)
    if not results['valid']:
        failed_files.append((input_file, results['errors']))
        print(f"✗ {input_file}: FAILED")
    else:
        print(f"✓ {input_file}: PASSED")

if failed_files:
    print("\nFailed files require fixes:")
    for filename, errors in failed_files:
        print(f"\n{filename}:")
        for error in errors:
            print(f"  • {error}")
```

**Key Points:**
- Automated validation for multiple files
- Identifies all failures before any runs
- Efficient use of computational resources
- Systematic quality control

---

## Integration with Other Skills

**Pre-Validation (Builder Skills):**
```
mcnp-input-builder      → Overall structure standards
mcnp-geometry-builder   → Cell/surface format standards
mcnp-material-builder   → Material definition standards
mcnp-source-builder     → Source card standards
mcnp-tally-builder      → Tally card standards
mcnp-physics-builder    → Physics settings standards
        ↓
mcnp-input-validator    → Validate against all standards
```

**Post-Validation (Checker Skills):**
```
mcnp-input-validator    → Basic validation
        ↓ (if validation passed)
mcnp-geometry-checker   → Detailed geometry analysis
mcnp-cross-reference-checker → Dependency mapping
mcnp-physics-validator  → Detailed physics review
mcnp-cell-checker       → Cell parameter optimization
```

**Complete Workflow:**
1. Build input with builder skills
2. Validate with this skill (mcnp-input-validator)
3. If PASSED → Plot geometry (ESSENTIAL)
4. If complex → Use specialized checkers
5. Run VOID test (RECOMMENDED)
6. Execute MCNP simulation
7. Validate output with mcnp-statistics-checker

## References

**Detailed Validation Procedures:**
- `validation_procedures.md` - 5-step validation algorithm, check procedures
- `error_catalog.md` - Complete error taxonomy with fixes (F-001 through W-005)
- `validation_checklists.md` - Quick, comprehensive, and targeted checklists
- `integration_guide.md` - Integration with builder and checker skills

**Automated Validation Scripts:**
- `scripts/mcnp_input_validator.py` - Main validation engine
- `scripts/block_structure_validator.py` - Block structure checks
- `scripts/cross_reference_checker.py` - Cross-reference validation
- `scripts/physics_consistency_checker.py` - Physics consistency
- `scripts/README.md` - Complete usage documentation

**Example Files:**
- `assets/example_inputs/01-04_*_INVALID.i` - Common error examples
- `assets/example_inputs/01-04_*_FIXED.i` - Corrected versions
- `assets/example_inputs/*_description.txt` - Error explanations

**External Documentation:**
- MCNP6 Manual Chapter 4: Input File Format
- MCNP6 Manual §4.4: Cross-Reference Requirements
- MCNP6 Manual §4.7: Input Error Messages
- MCNP6 Manual §4.8: Geometry Errors

**Related Skills:**
- mcnp-input-builder: Overall structure standards
- mcnp-geometry-builder: Cell/surface validation standards
- mcnp-geometry-checker: Detailed geometry analysis
- mcnp-cross-reference-checker: Comprehensive dependency checking
- mcnp-physics-validator: Detailed physics settings review
- mcnp-best-practices-checker: Comprehensive best practices audit

## Best Practices

1. **Validate before every MCNP run** - Catches 90% of errors before expensive simulation, saves hours of debugging time

2. **Fix errors in order presented** - First error is always real; subsequent errors may cascade from first issue

3. **Use appropriate validation level** - Quick validation during development, comprehensive before production runs

4. **Always plot geometry after validation passes** - Validation cannot detect overlaps/gaps; geometry plotting is MANDATORY not optional

5. **Run VOID card test for critical work** - Quickly finds geometry errors that plotting might miss, especially in complex regions

6. **Review all warnings before production** - Warnings indicate unconventional settings that may cause incorrect results

7. **Document validation results** - For critical calculations, create audit trail showing all validation steps performed

8. **Integrate validation into workflow** - Add validation to job submission scripts, pre-commit hooks, or CI/CD pipelines

9. **Use completed builder skills as standards** - Validator checks against mcnp-input-builder, mcnp-geometry-builder, etc. for consistent quality

10. **Escalate to specialized checkers when needed** - For complex inputs, use mcnp-geometry-checker, mcnp-cross-reference-checker after basic validation
