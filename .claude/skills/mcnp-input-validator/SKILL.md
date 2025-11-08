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
- `example_inputs/01-04_*_INVALID.i` - Common error examples
- `example_inputs/01-04_*_FIXED.i` - Corrected versions
- `example_inputs/*_description.txt` - Error explanations

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

---

## CRITICAL VALIDATION CATEGORIES

### 1. FILL Array Validation (LAT=1 AND LAT=2)

**Purpose**: Prevent fatal "wrong number of lattice fill entries" errors

**Checks performed:**
- ✅ Dimension calculation: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
- ✅ Repeat notation expansion: `U nR` = (n+1) total copies
- ✅ Element count matches declared fill range
- ✅ All filled universes are defined
- ✅ Lattice type matches surface type (LAT=1→RPP, LAT=2→RHP)

**Example error caught:**
```mcnp
c INVALID - dimension mismatch
100 0 -1 u=200 lat=1 fill=-7:7 -7:7 0:0  $ Need 15×15×1=225 elements
    [... only 200 universe numbers provided ...]  $ ← ERROR: 25 missing!
```

**Tool**: `scripts/fill_array_validator.py`

---

### 2. Universe Cross-Reference Validation

**Purpose**: Prevent circular references, undefined universe errors, geometry failures

**Checks performed:**
- ✅ All filled universes are defined before use
- ✅ No circular dependencies (A→B, B→A or longer cycles)
- ✅ Universe 0 never explicitly defined
- ✅ Fill references point to valid LAT cells or simple cells
- ✅ Hierarchy depth reasonable (<10 levels)

**Example error caught:**
```mcnp
c INVALID - circular reference
100 0 -1 u=10 fill=20  $ u=10 fills with u=20
200 0 -2 u=20 fill=10  $ ← ERROR: u=20 fills with u=10 (circular!)
```

**Tool**: `scripts/universe_cross_reference_checker.py`

---

### 3. Numbering Conflict Detection

**Purpose**: Prevent duplicate IDs causing ambiguous definitions

**Checks performed:**
- ✅ No duplicate cell IDs
- ✅ No duplicate surface IDs
- ✅ No duplicate material IDs
- ✅ No duplicate universe IDs
- ✅ Optional: Systematic numbering pattern verification
- ✅ Optional: Cell-material-surface correlation warnings

**Example error caught:**
```mcnp
c INVALID - duplicate cell ID
100 1 -10.0 -1 u=10  $ Cell 100
...
100 2 -6.5 -2 u=20   $ ← ERROR: Cell 100 defined twice!
```

**Tool**: `scripts/numbering_conflict_detector.py`

---

### 4. Thermal Scattering Verification

**Purpose**: Catch missing MT cards that cause 1000-5000 pcm reactivity errors

**Materials requiring S(α,β) libraries:**

| Material | Detection | Required MT Card | Temperature Options |
|----------|-----------|------------------|---------------------|
| **Graphite** | ZAID 6000, 6012, 6013 | `grph.XXt` | 10t (296K), 18t (600K), 22t (800K), ... |
| **Light water** | H-1 + O-16 | `lwtr.XXt` | 10t (294K), 11t (325K), 13t (350K), 14t (400K), ... |
| **Heavy water** | H-2 + O-16 | `hwtr.XXt` | 10t (294K), 11t (325K) |
| **Polyethylene** | H-1 + C (ratio ~2:1) | `poly.XXt` | 10t (296K), 20t (350K) |
| **Beryllium metal** | ZAID 4009 | `be.XXt` | 10t (296K), 20t (400K), ... |
| **Beryllium oxide** | Be + O | `beo.XXt` | 10t (296K), 20t (400K), ... |

**Checks performed:**
- ✅ Scan all materials for thermal scatterers
- ✅ Verify MT card exists for each
- ✅ Warn if temperature-inappropriate (e.g., grph.10t for 900K reactor)
- ✅ Flag missing MT cards as CRITICAL errors

**Example error caught:**
```mcnp
c CRITICAL ERROR - missing thermal scattering
m1  $ Graphite moderator
    6012.00c  0.9890
    6013.00c  0.0110
c ← MISSING: mt1 grph.18t  $ Will cause wrong thermal spectrum!
```

**Tool**: `scripts/thermal_scattering_validator.py`

**Impact:** Missing MT cards cause:
- ❌ Wrong thermal neutron spectrum (hardened)
- ❌ Incorrect reactivity (1000-5000 pcm error typical)
- ❌ Wrong spatial flux distribution
- ❌ Invalid benchmark comparisons

---

### 5. Surface-Cell Consistency Checks

**Purpose**: Prevent "surface XXX not found" fatal errors

**Checks performed:**
- ✅ Parse all surface references from cell boolean expressions
- ✅ Verify all surfaces defined in surfaces section
- ✅ Check material references (all materials defined)
- ✅ Detect common typos (e.g., 1000 vs 100)
- ✅ Warn about unreferenced surfaces (dead geometry)

**Example error caught:**
```mcnp
c INVALID - undefined surface
100 1 -10.0  -1000 2000  $ References surfaces 1000, 2000
...
c Surfaces section:
100 so 5.0   $ ← ERROR: surface 1000 undefined (typo?)
200 pz 10.0  $ ← ERROR: surface 2000 undefined
```

**Tool**: `scripts/surface_cell_consistency.py`

---

## VALIDATION WORKFLOW

### Pre-Run Validation Process

```
1. Parse MCNP input file
   ├─ Identify cells, surfaces, materials, universes
   └─ Extract LAT specifications and FILL arrays

2. Run all validators in sequence:
   ├─ Fill array validator (LAT=1 and LAT=2)
   ├─ Universe cross-reference checker
   ├─ Numbering conflict detector
   ├─ Thermal scattering verifier
   └─ Surface-cell consistency checker

3. Report results:
   ├─ CRITICAL errors (must fix before running)
   ├─ WARNINGS (should fix, but may run)
   └─ SUGGESTIONS (best practices)

4. Generate validation report
   └─ Save to input_filename_validation_report.txt
```

### Usage Examples

**Command-line usage:**
```bash
# Validate single file
python scripts/fill_array_validator.py bench_138B.i

# Check specific validation category
python scripts/thermal_scattering_validator.py bench_138B.i
python scripts/universe_cross_reference_checker.py bench_138B.i
```

**Python API usage:**
```python
from scripts.fill_array_validator import FillArrayValidator

# Validate fill arrays
validator = FillArrayValidator('bench_138B.i')
validator.print_report()

# Or get results programmatically
results = validator.validate()
if results['errors']:
    print("CRITICAL ERRORS FOUND:")
    for error in results['errors']:
        print(f"  - {error}")
else:
    print("✓ No critical errors detected")
```

---

## VALIDATION SEVERITY LEVELS

### CRITICAL (Must fix before running):
- ❌ FILL array dimension mismatch
- ❌ Circular universe references
- ❌ Duplicate numbering (cells, surfaces, materials, universes)
- ❌ Undefined surface references
- ❌ Undefined material references
- ❌ Missing thermal scattering for graphite, water, etc.

### WARNING (Should fix):
- ⚠️ Universe hierarchy depth >6 levels
- ⚠️ Unreferenced surfaces (dead geometry)
- ⚠️ Temperature-inappropriate S(α,β) library
- ⚠️ Non-systematic numbering (hard to maintain)

### SUGGESTION (Best practice):
- 💡 Use repeat notation for long fill arrays
- 💡 Add comments documenting universe hierarchy
- 💡 Use systematic numbering scheme
- 💡 Specify volumes for tally cells
