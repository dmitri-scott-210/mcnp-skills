# MCNP Input Validator - Integration Guide

## Overview

This guide explains how mcnp-input-validator integrates with other MCNP skills and validation tools to provide comprehensive input quality assurance.

---

## Integration Philosophy

**mcnp-input-validator serves as:**
1. **First-line validation:** Pre-run syntax and format checking
2. **Integration hub:** Connects builder and checker skills
3. **Standards enforcer:** Uses builder skill outputs as validation standards
4. **Workflow coordinator:** Routes to specialized validators when needed

**Key principle:** Validation uses completed builder skills as the "source of truth" for correct format.

---

## Integration with Builder Skills

### Using Builder Skills as Validation Standards

**Before validating any MCNP content, the validator:**

1. **References completed builder skills** to understand correct format:
   - mcnp-input-builder: Three-block structure
   - mcnp-geometry-builder: Cell/surface syntax
   - mcnp-material-builder: M/MT/MX format
   - mcnp-source-builder: SDEF/KCODE format
   - mcnp-tally-builder: Tally card syntax
   - mcnp-physics-builder: MODE/PHYS requirements
   - mcnp-lattice-builder: U/LAT/FILL patterns

2. **Validates against builder standards:**
   ```
   Input File → Validator → Compares to Builder Standards → Report
   ```

3. **Uses builder reference files** for detailed specifications:
   - card_specifications.md from each builder
   - Example files for format patterns
   - Templates for expected structure

---

### mcnp-input-builder Integration

**Purpose:** Validate overall file structure

**Validation checks using input-builder standards:**
- Three-block structure (cells → blank → surfaces → blank → data)
- Exactly 2 blank lines total
- Title card present and valid
- No blank lines within blocks
- Cards in correct blocks

**How validator uses input-builder:**
```python
# Validator references input-builder templates
template = read_template('mcnp-input-builder/assets/templates/basic_template.i')
expected_structure = parse_structure(template)

# Compare user input to standard structure
if user_structure != expected_structure:
    report_error("Block structure mismatch")
```

**Reference files used:**
- `mcnp-input-builder/input_structure_reference.md`
- `mcnp-input-builder/assets/templates/*.i`

---

### mcnp-geometry-builder Integration

**Purpose:** Validate cell and surface cards

**Validation checks using geometry-builder standards:**
- Cell card format: `j m d geom params`
- Surface card format: `n type/mnemonic params`
- Boolean logic operators
- Complement operator usage
- Macrobody parameter counts

**How validator uses geometry-builder:**
```python
# Load surface specifications from geometry-builder
surface_specs = load_specs('mcnp-geometry-builder/surface_types_comprehensive.md')

# Validate user surface against specs
for surface in user_surfaces:
    type = surface.get_type()
    params = surface.get_params()
    expected = surface_specs[type]['param_count']

    if len(params) != expected:
        report_error(f"Surface {surface.num}: {type} requires {expected} params")
```

**Reference files used:**
- `mcnp-geometry-builder/surface_types_comprehensive.md`
- `mcnp-geometry-builder/macrobodies_reference.md`
- `mcnp-geometry-builder/boolean_logic_reference.md`

---

### mcnp-material-builder Integration

**Purpose:** Validate material definitions

**Validation checks using material-builder standards:**
- ZAID format: ZZZAAA.XXc
- Library suffixes appropriate
- Thermal scattering (MT) for light materials
- TMP in MeV not Kelvin
- Density values reasonable

**How validator uses material-builder:**
```python
# Load ZAID validation rules from material-builder
zaid_rules = load_rules('mcnp-material-builder/zaid_format_reference.md')

# Validate user materials
for material in user_materials:
    for isotope in material.isotopes:
        if not validate_zaid(isotope, zaid_rules):
            report_error(f"Invalid ZAID: {isotope}")

        # Check thermal scattering
        if is_thermal_material(isotope):
            if not has_MT_card(material):
                report_warning(f"M{material.num} needs MT card")
```

**Reference files used:**
- `mcnp-material-builder/zaid_format_reference.md`
- `mcnp-material-builder/thermal_scattering_guide.md`
- `mcnp-material-builder/material_libraries/*.txt`

---

### mcnp-source-builder Integration

**Purpose:** Validate source specifications

**Validation checks using source-builder standards:**
- SDEF vs KCODE usage
- Distribution card syntax (SI/SP/SB)
- Energy/spatial/directional distributions
- KCODE parameters for criticality

**How validator uses source-builder:**
```python
# Load source card specifications from source-builder
source_specs = load_specs('mcnp-source-builder/sdef_card_reference.md')

# Validate user source
if user_has_sdef:
    validate_sdef_params(user_sdef, source_specs)
    validate_distributions(user_distributions, source_specs)
elif user_has_kcode:
    validate_kcode_params(user_kcode, source_specs)
else:
    report_error("No source specification (SDEF or KCODE required)")
```

**Reference files used:**
- `mcnp-source-builder/sdef_card_reference.md`
- `mcnp-source-builder/distribution_types_reference.md`
- `mcnp-source-builder/kcode_guide.md`

---

### mcnp-tally-builder Integration

**Purpose:** Validate tally specifications

**Validation checks using tally-builder standards:**
- Tally type syntax (F1-F8)
- Energy/time/cosine binning
- Multiplier cards (FM)
- Segmentation cards (FS)

**How validator uses tally-builder:**
```python
# Load tally specifications from tally-builder
tally_specs = load_specs('mcnp-tally-builder/tally_types_reference.md')

# Validate user tallies
for tally in user_tallies:
    type = tally.get_type()  # F4, F6, etc.

    # Check syntax against tally-builder standards
    validate_tally_syntax(tally, tally_specs[type])

    # Check energy bins
    if tally.has_energy_bins():
        validate_energy_bins(tally.energy_bins)

    # Check multipliers
    if tally.has_multiplier():
        validate_multiplier(tally.multiplier, user_materials)
```

**Reference files used:**
- `mcnp-tally-builder/tally_types_reference.md`
- `mcnp-tally-builder/multiplier_card_reference.md`
- `mcnp-tally-builder/segmentation_reference.md`

---

### mcnp-physics-builder Integration

**Purpose:** Validate physics settings

**Validation checks using physics-builder standards:**
- MODE card appropriate
- PHYS cards for each particle
- Energy ranges cover problem
- Cross-section consistency

**How validator uses physics-builder:**
```python
# Load physics specifications from physics-builder
physics_specs = load_specs('mcnp-physics-builder/physics_card_reference.md')

# Validate MODE card
mode_particles = parse_mode(user_mode_card)
validate_mode(mode_particles, physics_specs)

# Validate PHYS cards
for particle in mode_particles:
    if not user_has_phys_card(particle):
        report_warning(f"PHYS:{particle} card missing - using defaults")
    else:
        validate_phys_params(user_phys[particle], physics_specs)
```

**Reference files used:**
- `mcnp-physics-builder/physics_card_reference.md`
- `mcnp-physics-builder/transport_modes_reference.md`

---

### mcnp-lattice-builder Integration

**Purpose:** Validate repeated structures

**Validation checks using lattice-builder standards:**
- U/LAT/FILL relationships
- Universe numbering
- Lattice dimensions
- Nested universe hierarchy

**How validator uses lattice-builder:**
```python
# Load lattice specifications from lattice-builder
lattice_specs = load_specs('mcnp-lattice-builder/lattice_specifications.md')

# Validate lattice structures
for cell in user_cells:
    if cell.has_lat_param():
        validate_lattice_cell(cell, lattice_specs)
        check_universe_definition(cell.universe_num, user_cells)

    if cell.has_fill_param():
        validate_fill_reference(cell.fill_num, user_cells)
```

**Reference files used:**
- `mcnp-lattice-builder/lattice_specifications.md`
- `mcnp-lattice-builder/universe_hierarchy_guide.md`

---

## Integration with Checker Skills

**When to escalate from validator to specialized checkers:**

### mcnp-geometry-checker

**Escalate when:**
- Validation passes but geometry complexity high
- User needs detailed geometry analysis
- Overlap/gap detection required
- Volume calculations needed

**Validator → Geometry-Checker workflow:**
```
1. Validator: Pass syntax and cross-reference checks
2. Validator: Recommend geometry checking
3. User invokes: mcnp-geometry-checker
4. Geometry-checker: Detailed geometric analysis
```

**Validation report includes:**
```
RECOMMENDATIONS:
✓ Input syntax valid - ready for geometry check
  Next step: Use mcnp-geometry-checker for:
    - Overlap/gap detection
    - Volume calculations
    - Geometry complexity analysis
    - Optimization suggestions
```

---

### mcnp-cross-reference-checker

**Escalate when:**
- Complex cell/universe hierarchies
- Many material references
- Dependency mapping needed
- Unused entities to identify

**Validator → Cross-Reference-Checker workflow:**
```
1. Validator: Basic cross-reference validation (undefined references)
2. Validator: Detect complex dependencies
3. Recommend: mcnp-cross-reference-checker for detailed analysis
4. Cross-ref-checker: Build dependency graph, identify issues
```

**What validator checks vs. cross-reference-checker:**

**Validator checks:**
- Fatal: Undefined surface in cell geometry
- Fatal: Undefined material in cell
- Fatal: Undefined universe in FILL

**Cross-reference-checker adds:**
- Dependency graphs
- Circular dependency detection
- Unused entity identification
- Complex lattice hierarchy analysis

---

### mcnp-physics-validator

**Escalate when:**
- Coupled transport modes
- Complex physics models
- Energy-dependent issues
- Detailed physics review needed

**Validator → Physics-Validator workflow:**
```
1. Validator: Basic physics consistency (MODE, PHYS ranges)
2. Validator: Detect complex physics settings
3. Recommend: mcnp-physics-validator for detailed review
4. Physics-validator: Detailed physics analysis
```

---

### mcnp-cell-checker

**Escalate when:**
- Many cells with complex parameters
- Cell parameter optimization needed
- Systematic cell review required

---

## Complete Validation Pipeline

**Recommended workflow integrating all skills:**

### Stage 1: Input Construction (Builder Skills)

```
User Need → Builder Skills → Draft Input

mcnp-input-builder       → Overall structure
mcnp-geometry-builder    → Cells & surfaces
mcnp-material-builder    → Materials
mcnp-source-builder      → Source
mcnp-tally-builder       → Tallies
mcnp-physics-builder     → Physics settings
mcnp-lattice-builder     → Repeated structures (if needed)

Output: Draft input file
```

---

### Stage 2: Pre-Run Validation (This Skill)

```
Draft Input → mcnp-input-validator → Validation Report

Checks:
  - Syntax against builder standards
  - Cross-references
  - Physics consistency
  - Format compliance

Outputs:
  - FATAL errors (must fix)
  - Warnings (should review)
  - Recommendations (best practices)

If PASSED → Stage 3
If FAILED → Fix errors → Re-validate Stage 2
```

---

### Stage 3: Detailed Checking (Checker Skills)

```
Validated Input → Specialized Checkers → Detailed Reports

mcnp-geometry-checker         → Geometry analysis
mcnp-cross-reference-checker  → Dependency analysis
mcnp-physics-validator        → Physics review
mcnp-cell-checker            → Cell parameter review

Output: Detailed analysis reports
```

---

### Stage 4: Geometry Verification

```
Checked Input → Geometry Plotting → Visual Verification

Command: mcnp6 ip i=input.inp
Actions:
  - Plot from multiple views
  - Look for dashed lines (errors)
  - Verify material assignments
  - Check boundary locations

If issues found → Fix → Re-validate from Stage 2
```

---

### Stage 5: Pre-Production Testing

```
Plotted Input → VOID Card Test → Lost Particle Check

Add VOID card
Run: mcnp6 i=input.inp
Check: Lost particles in output

If lost particles → Fix geometry → Re-validate from Stage 2
If clean → Ready for production
```

---

### Stage 6: Production Run

```
Tested Input → MCNP Execution → Results

Run: mcnp6 i=input.inp o=output.txt
Monitor: Execution progress
```

---

### Stage 7: Post-Run Validation

```
Completed Run → Statistical Validation → Quality Check

mcnp-statistics-checker → Tally quality
mcnp-tally-analyzer    → Result analysis

Check:
  - Relative errors < 0.05
  - FOM reasonable
  - Convergence achieved
  - Results physically reasonable

If issues → Adjust input → Re-run
If good → Document results
```

---

## Validation Automation Integration

**Python script integrating full pipeline:**

```python
from mcnp_input_validator import MCNPInputValidator
from mcnp_geometry_checker import MCNPGeometryChecker
from mcnp_cross_reference_checker import MCNPCrossRefChecker
import subprocess

def complete_validation_pipeline(input_file):
    """
    Complete MCNP input validation pipeline
    """

    # Stage 2: Pre-run validation
    print("Stage 2: Running mcnp-input-validator...")
    validator = MCNPInputValidator()
    val_results = validator.validate_file(input_file)

    if not val_results['valid']:
        print("FATAL ERRORS FOUND - Fix before continuing")
        for error in val_results['errors']:
            print(f"  ERROR: {error}")
        return False

    print("✓ Validation passed")

    # Stage 3: Detailed checking
    print("\nStage 3: Running specialized checkers...")

    # Geometry check
    geo_checker = MCNPGeometryChecker()
    geo_results = geo_checker.check_geometry(input_file)

    if geo_results['warnings']:
        print("Geometry warnings found:")
        for warning in geo_results['warnings']:
            print(f"  WARNING: {warning}")

    # Cross-reference check
    xref_checker = MCNPCrossRefChecker()
    xref_results = xref_checker.check_dependencies(input_file)

    print(f"✓ Found {len(xref_results['unused_surfaces'])} unused surfaces")

    # Stage 4: Geometry plotting
    print("\nStage 4: Geometry verification")
    print("Run: mcnp6 ip i=" + input_file)
    print("Manually verify:")
    print("  - No dashed lines in plots")
    print("  - Material assignments correct")
    print("  - Boundaries in expected locations")

    # Stage 5: VOID test recommendation
    print("\nStage 5: Pre-production testing")
    print("Recommended VOID card test:")
    print("  1. Add 'VOID' to data cards")
    print("  2. Run: mcnp6 i=" + input_file)
    print("  3. Check for lost particles")
    print("  4. Remove VOID card after clean run")

    print("\n" + "="*60)
    print("VALIDATION PIPELINE COMPLETE")
    print("Input ready for production run (after geometry plot & VOID test)")
    print("="*60)

    return True

# Example usage
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.inp"
    complete_validation_pipeline(input_file)
```

---

## Integration Best Practices

### 1. Always Use Builder Skills First

**Don't:** Write MCNP input from scratch, then validate
**Do:** Use builder skills → Validate builder output

### 2. Validate Incrementally

**Don't:** Build entire input, then validate once
**Do:** Validate after each major addition:
  - Add cells → Validate
  - Add materials → Validate
  - Add source → Validate
  - etc.

### 3. Use Appropriate Checker Depth

**Don't:** Always run all checkers for every change
**Do:** Match checker depth to change scope:
  - Minor changes → Quick validation only
  - Major changes → Full validation pipeline

### 4. Document Validation Results

**Don't:** Just note "validation passed"
**Do:** Record:
  - Which validation performed
  - What was checked
  - Any warnings addressed
  - Deviations from recommendations

### 5. Integrate into Workflow Tools

**Don't:** Manual validation as separate step
**Do:** Integrate into:
  - Pre-commit hooks (for version control)
  - CI/CD pipelines
  - Job submission scripts
  - Batch processing workflows

---

## Troubleshooting Integration Issues

### Issue: Validator disagrees with builder output

**Possible causes:**
- Builder skill not updated to latest standards
- Validator using outdated reference files
- Legitimate difference in interpretation

**Resolution:**
1. Check builder skill version
2. Check validator version
3. Review MCNP6 manual section
4. Report discrepancy to skill maintainer

---

### Issue: Validation passes but MCNP run fails

**Possible causes:**
- Geometry errors (overlap/gap) - not detectable by syntax validation
- Cross-section library not in DATAPATH
- Excessive memory requirements
- Operating system limitations

**Resolution:**
1. Plot geometry (ESSENTIAL - validator cannot detect geometry errors)
2. Run VOID test
3. Check DATAPATH environment variable
4. Review MCNP output file for specific error

---

### Issue: Too many false positive warnings

**Possible causes:**
- Validator too conservative
- Unconventional but valid technique
- Validator not aware of advanced features

**Resolution:**
1. Review warnings for false positives
2. Document why warning is acceptable
3. Consider updating validator rules
4. Use targeted validation to skip irrelevant checks

---

## Future Integration Enhancements

**Planned improvements:**
- Automated geometry plotting integration
- Direct MCNP6 parser integration
- Real-time validation during editing
- Web-based validation service
- Integration with MCNP Visual Editor

---

**END OF INTEGRATION GUIDE**

Use this integration approach to ensure comprehensive MCNP input quality through coordinated use of builder, validator, and checker skills.
