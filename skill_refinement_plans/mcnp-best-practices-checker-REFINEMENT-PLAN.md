# MCNP Best Practices Checker - Refinement Plan

**Date:** November 8, 2025
**Priority:** HIGH - Extends core validation skill with professional reactor modeling practices
**Estimated Effort:** 3-4 hours
**Dependencies:** Requires mcnp-lattice-builder, mcnp-cross-reference-checker refinements

---

## EXECUTIVE SUMMARY

The current mcnp-best-practices-checker skill provides excellent coverage of the core 57-item checklist from Chapter 3.4. However, analysis of production-quality HTGR reactor models reveals **additional critical best practices** for professional reactor modeling that should be integrated into the checker:

**Key Gaps Identified:**
1. ❌ No automation/reproducibility validation
2. ❌ No multi-level lattice hierarchy checks
3. ❌ No systematic numbering scheme validation
4. ❌ No cross-referencing validation guidance
5. ❌ No professional workflow integration checks
6. ❌ No thermal scattering requirement checks
7. ❌ No reactor-specific geometry patterns validation

**Impact:** Users can pass all 57 items but still create unmaintainable, non-reproducible, or physically incorrect reactor models.

**Solution:** Extend the checklist with **Phase 0: Professional Modeling Standards** (15 additional items) and integrate reactor-specific validation guidance throughout.

---

## PROPOSED ENHANCEMENTS

### Enhancement 1: Add Phase 0 - Professional Modeling Standards (NEW)

**Rationale:** The HTGR analysis revealed that professional reactor models require systematic practices BEFORE the standard MCNP validation begins.

**New Section for SKILL.md:**

```markdown
### Phase 0: Professional Modeling Standards (PRE-SETUP) - 15 Items

**Before creating input file - prevents maintenance and reproducibility issues**

**Project Organization (Items 1-5):**
1. **Version control from start** (git, hg, or svn) - **CRITICAL**
   - Track all input files, generation scripts, data
   - Enables rollback and collaboration
   - Required for reproducible research

2. **Design numbering scheme BEFORE implementation**
   - Allocate digit ranges by entity type
   - Encode hierarchy in numbers (cell 91234 → capsule 9, stack 1, etc.)
   - Document scheme in input header
   - Prevents conflicts in large models

3. **Separate data from logic**
   - External data in CSV/JSON files (not hardcoded)
   - Parameters in separate definition files
   - Enables systematic parameter studies

4. **Document provenance of ALL values**
   - Each number traceable to source (paper, handbook, measurement)
   - Include references in comments
   - Required for validation and licensing

5. **README with complete workflow**
   - How to regenerate inputs from scratch
   - Software dependencies and versions
   - Expected outputs and validation criteria

**Geometry Design (Items 6-9):**
6. **Plan universe hierarchy BEFORE coding**
   - Draw containment tree diagram
   - Identify all nested levels (typically 3-6 for reactors)
   - Allocate universe number ranges

7. **Choose lattice types appropriately**
   - LAT=1 (rectangular) for: PWR assemblies, vertical stacks, regular grids
   - LAT=2 (hexagonal) for: HTGR cores, fast reactor assemblies, hex fuel
   - Mixed types allowed in same model

8. **Validate lattice dimensions mathematically**
   - Element count = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
   - Surface extent = N × pitch (rectangular) or matches hex pattern
   - ALWAYS account for zero in index ranges!

9. **Use systematic cell/surface correlation**
   - Cell 1234 uses surfaces 1234X, material m1234
   - Immediate identification of relationships
   - Simplifies debugging

**Materials (Items 10-12):**
10. **Thermal scattering REQUIRED for** - **CRITICAL**
    - ✅ ALL graphite (any reactor type)
    - ✅ ALL water (light or heavy)
    - ✅ Polyethylene, beryllium, BeO
    - ⚠️ Impact: 1000-5000 pcm error if missing
    - ⚠️ Choose temperature-appropriate library (grph.10t @ 294K vs grph.18t @ 600K)

11. **Temperature-consistent cross sections**
    - Match S(α,β) temperature to physics temperature
    - Use same library family (.70c, .80c, NOT mixed .70c and .21c)
    - Document temperature assumptions

12. **Material density specifications consistent**
    - Negative = g/cm³, positive = atoms/barn-cm
    - Document which convention in comments
    - Validate atom fractions sum to expected range

**Automation (Items 13-15):**
13. **Automate for ≥3 similar cases**
    - Template-based (Jinja2) OR programmatic (Python functions)
    - Reduces copy-paste errors
    - Enables rapid parameter variations

14. **Validate generated outputs**
    - Compare to reference case
    - Check numbering conflicts (duplicate IDs)
    - Verify all cross-references exist

15. **Reproducible generation**
    - Single command regenerates all inputs
    - Scripts version-controlled with inputs
    - External data frozen at known versions
```

**Why This Phase Matters:**
- Professional reactor models have 1000-10,000+ cells
- Manual editing at this scale is error-prone and unmaintainable
- These practices are REQUIRED for publication, licensing, collaboration
- Following these saves weeks/months on large projects

---

### Enhancement 2: Extend Phase 1 with Reactor-Specific Checks

**Addition to existing Phase 1 (items 23-30):**

```markdown
**Reactor Model Specifics (Items 23-30):**

23. **Multi-level lattice validation**
    - All child universes defined BEFORE parent fills with them
    - No circular references (u=100 fill=200, u=200 fill=100)
    - Lattice bounding surface matches N × pitch
    - FILL array element count matches declared bounds

24. **Repeat notation validation** (nR syntax)
    - Remember: `U nR` gives (n+1) total copies, NOT n!
    - Example: `100 2R` = 100 100 100 (3 copies)
    - Validate: sum of pattern = (KMAX-KMIN+1)

25. **Hexagonal lattice specifics** (if LAT=2 used)
    - Bounding surface is RHP (right hexagonal prism), NOT RPP
    - Pitch = R × √3 (R from RHP definition)
    - Staggered row pattern in FILL array

26. **Cross-reference completeness**
    - Every cell references DEFINED surfaces only
    - Every material cell references DEFINED material
    - Every fill references DEFINED universe
    - No orphaned surfaces (defined but never used)

27. **Numbering scheme conflicts**
    - No duplicate cell IDs
    - No duplicate surface IDs
    - No duplicate material IDs
    - No duplicate universe IDs
    - Use ranges to prevent (9000s for cells, 8000s for materials)

28. **Systematic comment conventions**
    - EVERY cell has descriptive comment ($)
    - EVERY surface documented with purpose
    - EVERY material has composition note
    - Section headers clearly mark blocks

29. **Volume specifications** (VOL cards)
    - Critical cells have VOL= specified
    - Enables mass/inventory validation
    - Provides independent geometry check
    - Compare MCNP calculated vs specified (should agree <5%)

30. **Transformation validation** (if used)
    - TRCL or *TRCL cards validated
    - Coordinate systems match physical intent
    - Test with geometry plots from multiple angles
    - Verify no unintended rotations/reflections
```

---

### Enhancement 3: Add Reactor Modeling Best Practices Section

**New section to insert after Phase 4:**

```markdown
## Reactor Modeling Best Practices

### Complex Lattice Hierarchies

**Common Reactor Patterns:**

**PWR Core (4 levels):**
```
Level 1: Fuel pin (u=100) - concentric cylinders
Level 2: Assembly (u=200, LAT=1) - 17×17 pin array
Level 3: Core quarter (u=300, LAT=1) - assembly array
Level 4: Full core (reflection/rotation)
```

**HTGR Core (6 levels):**
```
Level 1: TRISO particle (u=XXX4) - 5 concentric shells
Level 2: Particle array (u=XXX6, LAT=1) - 15×15 rectangular
Level 3: Compact stack (u=XXX0, LAT=1) - vertical 1×1×31
Level 4: Fuel channel (u=XXX1) - filled cylinder
Level 5: Assembly (u=XXX0, LAT=2) - hexagonal lattice
Level 6: Core - multiple assemblies
```

**Fast Reactor (5 levels):**
```
Level 1: Fuel pin (u=100)
Level 2: Pin bundle (u=200, LAT=2) - hexagonal
Level 3: Assembly duct (u=300)
Level 4: Core (u=400, LAT=2) - hex assembly array
Level 5: Vessel/reflector
```

**Validation Checklist for Hierarchies:**
- [ ] Drew containment tree diagram before implementation
- [ ] Each level has unique universe number range
- [ ] No universe appears in its own fill chain
- [ ] All universes defined before first use
- [ ] Tested small (2×2) lattice before full scale
- [ ] Plotted geometry from 3+ angles

### Systematic Numbering Examples

**HTGR AGR-1 Pattern (proven in production):**
```python
# Cell numbering: 9[capsule][stack][2×compact][sequence]
cell_id = 90000 + cap*1000 + stack*100 + 2*(comp-1)*10 + seq

# Surface numbering: 9[capsule][stack][compact][layer]
surf_id = 9000 + cap*100 + stack*10 + comp

# Material numbering: 9[capsule][stack][compact]
mat_id = 9000 + cap*100 + stack*10 + comp

# Universe numbering: [capsule][stack][compact][level]
univ_id = cap*100 + stack*10 + comp + level_digit

Example: Cell 91234 = Capsule 1, Stack 2, Compact 2, Sequence 4
         Links to: Surface 9122, Material m912, Universe 1224
```

**Benefits:**
- Zero numbering conflicts across 1500+ entities
- Instant location identification
- Enables automated generation
- Simplifies debugging

**Microreactor Parametric Pattern:**
```python
# Layer-Assembly-Component encoding
def fuel(layer, assembly_number):
    n = f"{layer+1}{assembly_number:02d}"  # "201" for layer 2, assy 01

    cell_ids = f"{n}01", f"{n}02", ...  # 20101, 20102, ...
    surf_ids = f"{n}01", f"{n}02", ...  # 20101, 20102, ...
    mat_ids = f"{n}1", f"{n}2", ...     # 2011, 2012, ...
```

**Subsystem Ranges:**
- 2000-2999: Layer 1 assemblies
- 3000-3999: Layer 2 assemblies
- 8000-8999: Shield/shutdown dose components
- 9000-9999: Reflector

### Automation Patterns

**When to Automate:**
✅ **Automate When:**
- More than 3 similar cases needed
- Parameters change frequently
- Geometry follows algorithmic pattern
- Human error risk in manual entry
- Reproducibility critical (licensing, publication)

❌ **Don't Automate When:**
- One-time model
- Highly irregular geometry
- Automation effort > manual effort × expected revisions
- Debugging complexity outweighs benefit

**Template-Based (Jinja2) - Good For:**
- Large stable base model + parametric insertions
- Experiment in host reactor (AGR-1 in ATR)
- Multiple cycles with varying conditions
- Preserving complex validated geometry

**Example workflow:**
```python
from jinja2 import Environment, FileSystemLoader

# Load template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('base_reactor.template')

# Render with parameters
output = template.render(
    power=ave_power,
    control_positions=oscc_angles,
    fuel_cells=generated_fuel_geometry
)

# Write to file
with open('cycle_138B.i', 'w') as f:
    f.write(output)
```

**Programmatic (Python Functions) - Good For:**
- Model built from scratch
- Regular/symmetric geometry (lattices, assemblies)
- Algorithmic complexity
- Tight parameter coupling

**Example workflow:**
```python
def fuel_assembly(layer, number, variant):
    """Generate complete assembly geometry.

    Returns: (cells, surfaces, materials) as formatted strings
    """
    # Validate inputs
    assert 0 <= layer < 4, "Invalid layer"

    # Calculate positions
    cells = generate_cells(layer, number)
    surfaces = generate_surfaces(layer, number)
    materials = generate_materials(layer, number, variant)

    # Validate outputs
    assert_no_conflicts(cells, surfaces, materials)

    return cells, surfaces, materials

# Build entire model
cells = ""
surfaces = ""
materials = ""

for layer in range(4):
    for assy in assemblies[layer]:
        c, s, m = fuel_assembly(layer, assy, variant='baseline')
        cells += c
        surfaces += s
        materials += m

# Write output
write_mcnp_input('reactor.i', cells, surfaces, materials)
```

**Quality Assurance for Automated Generation:**
```python
def validate_generated_input(input_file):
    """Check automated generation output."""
    checks = {
        'dimension_match': check_lattice_dimensions(),
        'cross_refs': check_all_references_exist(),
        'numbering': check_no_duplicate_ids(),
        'physics': check_thermal_scattering(),
        'geometry': check_volumes_reasonable()
    }

    for check, result in checks.items():
        if not result['passed']:
            print(f"FAIL: {check} - {result['message']}")
            return False

    return True
```

### Material Best Practices

**Thermal Scattering - CRITICAL REQUIREMENTS:**

**ALWAYS Required:**
```mcnp
c Graphite moderator (HTGR, RBMK, MSR)
m1  6012.00c 0.9890  6013.00c 0.0110
mt1 grph.18t  $ 600K - REQUIRED! Omission = 1000+ pcm error

c Light water (PWR, BWR, research reactors)
m2  1001.70c 2.0  8016.70c 1.0
mt2 lwtr.13t  $ 350K PWR conditions - REQUIRED!

c Heavy water (CANDU)
m3  1002.70c 2.0  8016.70c 1.0
mt3 hwtr.11t  $ 325K - REQUIRED!
```

**Temperature Selection:**
| Reactor Type | Temperature (K) | Library | Use Case |
|--------------|----------------|---------|----------|
| HTGR operating | 600-1000 | grph.18t - grph.24t | Normal operation |
| HTGR cold critical | 294 | grph.10t | Startup physics |
| PWR operating | 350-400 | lwtr.13t - lwtr.14t | Normal operation |
| PWR cold leg | 325 | lwtr.11t | Specific analysis |
| Research reactor | 294 | lwtr.10t, grph.10t | Room temperature |

**Library Consistency:**
```mcnp
c GOOD: Consistent ENDF/B-VII.0
m1  92235.70c ...  92238.70c ...  8016.70c ...

c BAD: Mixed libraries (AVOID!)
m2  92235.70c ...  92238.21c ...  8016.80c ...
   # Different evaluations may have inconsistent data
```

**Common Fuel Compositions:**

**UO₂ (PWR/BWR):**
```mcnp
m1  $ UO2, 4.5% enriched, 10.5 g/cm³
   92234.70c  3.6e-4    $ U-234
   92235.70c  0.045     $ U-235 enrichment
   92238.70c  0.955     $ U-238
    8016.70c  2.0       $ O-16 (stoichiometric)
```

**UCO (TRISO kernels):**
```mcnp
m2  $ UCO, 19.75% enriched, 10.924 g/cm³
   92234.00c  3.34179e-03
   92235.00c  1.99636e-01
   92236.00c  1.93132e-04
   92238.00c  7.96829e-01
    6012.00c  0.3217     $ C-12 (UC phase)
    6013.00c  0.0036     $ C-13
    8016.00c  1.3613     $ O-16 (UO2 phase)
```

**MOX (Pu-bearing):**
```mcnp
m3  $ MOX, ~7% Pu, 10.4 g/cm³
   92235.70c  0.002      $ Depleted U
   92238.70c  0.928
   94238.70c  0.001      $ Pu isotopes
   94239.70c  0.050
   94240.70c  0.015
   94241.70c  0.003
   94242.70c  0.001
    8016.70c  2.0        $ O-16
```

### Cross-Referencing Validation

**Critical Validations (automate these!):**

**1. Surface Reference Check:**
```python
def check_surface_references(input_file):
    """Ensure all cell-referenced surfaces are defined."""
    defined_surfaces = extract_surface_ids(input_file)
    referenced_surfaces = extract_cell_surface_refs(input_file)

    missing = referenced_surfaces - defined_surfaces
    if missing:
        print(f"ERROR: Undefined surfaces: {missing}")
        return False
    return True
```

**2. Material Reference Check:**
```python
def check_material_references(input_file):
    """Ensure all cell materials are defined."""
    defined_materials = extract_material_ids(input_file)
    referenced_materials = extract_cell_material_refs(input_file)

    # Exclude material 0 (void)
    referenced_materials.discard(0)

    missing = referenced_materials - defined_materials
    if missing:
        print(f"ERROR: Undefined materials: {missing}")
        return False
    return True
```

**3. Universe Fill Validation:**
```python
def check_universe_fill_chain(input_file):
    """Ensure no circular universe references."""
    fill_graph = build_universe_graph(input_file)

    # Topological sort to detect cycles
    try:
        sorted_universes = topological_sort(fill_graph)
    except CycleError as e:
        print(f"ERROR: Circular universe reference: {e}")
        return False

    return True
```

**4. Lattice Dimension Validation:**
```python
def check_lattice_dimensions(input_file):
    """Validate FILL array counts match declared bounds."""
    lattices = extract_lattice_cards(input_file)

    for lat in lattices:
        # Parse fill bounds
        i_count = lat['imax'] - lat['imin'] + 1
        j_count = lat['jmax'] - lat['jmin'] + 1
        k_count = lat['kmax'] - lat['kmin'] + 1
        expected = i_count * j_count * k_count

        # Count fill entries (account for nR notation)
        actual = count_fill_entries(lat['fill_array'])

        if actual != expected:
            print(f"ERROR: Lattice {lat['cell']} has {actual} entries, "
                  f"expected {expected} from bounds")
            return False

    return True
```

**5. Numbering Conflict Detection:**
```python
def check_numbering_conflicts(input_file):
    """Find duplicate IDs."""
    cells = extract_cell_ids(input_file)
    surfaces = extract_surface_ids(input_file)
    materials = extract_material_ids(input_file)
    universes = extract_universe_ids(input_file)

    conflicts = []

    if len(cells) != len(set(cells)):
        conflicts.append(f"Duplicate cells: {find_duplicates(cells)}")

    if len(surfaces) != len(set(surfaces)):
        conflicts.append(f"Duplicate surfaces: {find_duplicates(surfaces)}")

    if len(materials) != len(set(materials)):
        conflicts.append(f"Duplicate materials: {find_duplicates(materials)}")

    if len(universes) != len(set(universes)):
        conflicts.append(f"Duplicate universes: {find_duplicates(universes)}")

    if conflicts:
        for c in conflicts:
            print(f"ERROR: {c}")
        return False

    return True
```

### Reproducibility Standards

**Essential for Professional Work:**

1. **Version Control All Source Files:**
   ```bash
   git init
   git add *.py *.csv *.template README.md
   git commit -m "Initial reactor model - baseline configuration"
   git tag v1.0-baseline
   ```

2. **Document Dependencies:**
   ```
   # requirements.txt
   python==3.11.0
   numpy==1.24.0
   pandas==2.0.0
   jinja2==3.1.2
   matplotlib==3.7.0

   # MCNP version: MCNP6.2 (build 2020-02-14)
   # Cross sections: ENDF/B-VII.1 (xsdir from 2018-05-01)
   ```

3. **README with Complete Workflow:**
   ````markdown
   # Reactor Model Generation

   ## Regeneration from Scratch
   ```bash
   # Generate all cycle inputs
   cd agr-1/
   python create_inputs.py

   # Verify outputs
   python validate_inputs.py

   # Expected: 13 inputs in mcnp/ directory
   # Expected: No validation errors
   ```

   ## Input Files
   - `power.csv`: Experimental power history (source: ECAR-3569)
   - `oscc.csv`: Control drum positions (source: ATR operations)
   - `bench.template`: Base ATR quarter-core model (13,727 lines)

   ## Outputs
   - `mcnp/bench_*.i`: Cycle-specific inputs (13 files)

   ## Validation
   - Geometry plotted: `mcnp6 ip i=mcnp/bench_138B.i`
   - VOID test: Passed with 0 lost particles
   - Volume check: MCNP calculated vs CAD: <2% difference
   ````

4. **Frozen External Data:**
   ```python
   # Don't fetch live data that might change
   # BAD:
   power_df = pd.read_csv('http://server.com/latest_power.csv')

   # GOOD: Snapshot with known version
   power_df = pd.read_csv('data/power_20240315_v2.csv')
   # File hash (SHA256): a1b2c3d4...
   ```

5. **Permanent Identifier (DOI):**
   - Archive complete repository on Zenodo
   - Receive DOI (e.g., 10.5281/zenodo.1234567)
   - Cite in publications
   - Enables exact reproduction years later

**Reproducibility Checklist:**
- [ ] All source files version controlled (git/hg/svn)
- [ ] Generation scripts included and documented
- [ ] External data files included with provenance
- [ ] Dependencies documented (software versions)
- [ ] README explains complete workflow
- [ ] Single command regenerates all inputs
- [ ] Validation criteria specified
- [ ] Expected outputs documented
- [ ] License specified (MIT, Apache, CC0, etc.)
- [ ] DOI assigned (Zenodo, figshare, institutional repository)

```

---

### Enhancement 4: Extended Validation Workflow

**Update the "Integration with Other Skills" section:**

```markdown
## Extended Validation Workflow for Reactor Models

**Complete Professional Workflow:**

1. **Phase 0: Professional Setup** ← **START HERE for reactor models**
   - Design numbering scheme
   - Set up version control
   - Separate data from logic
   - Document provenance

2. **mcnp-input-builder / mcnp-template-generator**
   - Generate inputs from templates or programmatically
   - Validate numbering conflicts
   - Check cross-references

3. **mcnp-lattice-builder** (if lattices used)
   - Validate FILL array dimensions
   - Check universe hierarchy (no circular refs)
   - Verify surface/pitch matching

4. **mcnp-material-builder**
   - Verify thermal scattering for graphite/water/Be
   - Check temperature-appropriate libraries
   - Validate density specifications

5. **mcnp-input-validator** → Syntax and structure

6. **mcnp-geometry-checker** → Geometry validity
   - CRITICAL: Plot from 3+ angles
   - CRITICAL: VOID card test
   - Volume pre-calculation vs MCNP

7. **mcnp-cross-reference-checker**
   - All surfaces defined
   - All materials defined
   - All universes defined
   - No orphaned entities

8. **mcnp-physics-validator** → Physics settings

9. **mcnp-best-practices-checker** → Comprehensive review ← **YOU ARE HERE**
   - Phase 0: Professional standards (15 items)
   - Phase 1: Setup (30 items including reactor-specific)
   - Phase 2: Preproduction test
   - Phase 3: Production validation
   - Phase 4: Criticality (if KCODE)

10. **Run simulation**

11. **mcnp-statistics-checker** → Results quality

12. **mcnp-warning-analyzer** → Warning significance

13. **mcnp-tally-analyzer** → Results interpretation

**Reactor Model Emphasis:**
- Phases 0 and 1 are MORE IMPORTANT for large reactor models
- 30 minutes on Phase 0 saves weeks on 10,000-line model
- Automation is REQUIRED, not optional, for complex geometries
- Reproducibility is REQUIRED for publication and licensing
```

---

### Enhancement 5: Add Reactor-Specific Use Cases

**New use cases to add:**

```markdown
## Use Case 4: HTGR Multi-Level Lattice Validation

**Scenario:** 6-level TRISO particle model with 72 compacts

**Phase 0 Professional Standards Check:**
```
Repository Structure:
✓ Version control initialized (git)
✓ README documents workflow
✓ CSV data files with provenance
✓ Python generation script
✓ Numbering scheme designed (9XYZW encoding)

Automation Check:
✓ Programmatic generation (create_inputs.py)
✓ Validation script (validate_inputs.py)
✓ Single command regenerates all
✓ No hardcoded parameters

Material Check:
✗ Missing thermal scattering for graphite!
  Action: Add mt9040 grph.18t for moderator
  Action: Add mt9090-mt9094 grph.18t for TRISO coatings
  Impact: ~2000 pcm reactivity error without this

Assessment: 14/15 items complete, 1 CRITICAL error
Action Required: STOP - Fix thermal scattering before ANY runs
```

**Phase 1 Reactor-Specific Check:**
```
Multi-Level Lattice Validation:

Level 1: TRISO particle (u=1114) - 6 cells
  ✓ Concentric spheres (SO surfaces)
  ✓ No gaps (r1 < r2 < r3 < r4 < r5)
  ✓ Material 9111 defined
  ✓ Volume specified (vol=0.092522)

Level 2: Particle lattice (u=1116, LAT=1)
  ✓ Dimension: fill=-7:7 -7:7 0:0 → 15×15×1 = 225 elements
  ✓ Element count: 169 particles + 56 matrix = 225 ✓
  ✓ Bounding surface: RPP matches lattice pitch
  ✓ Fills with u=1114, u=1115 (both defined)

Level 3: Compact stack (u=1110, LAT=1)
  ✓ Dimension: fill=0:0 0:0 -15:15 → 1×1×31 = 31 elements
  ✓ Pattern: 1117 2R 1116 24R 1117 2R = 3+25+3 = 31 ✓
  ✓ Bounding surface: RPP vertical extent correct
  ✓ Fills with u=1116, u=1117 (both defined)

Level 4-6: Capsule hierarchy
  ✓ Transformation (x,y,z) positions validated
  ✓ No circular universe references
  ✓ All 72 compacts generated systematically

Cross-Reference Validation:
  ✓ All 1607 cells reference defined surfaces
  ✓ All materials (385 total) defined
  ✓ No numbering conflicts (9XYZW scheme prevents)
  ✓ Comments on all entities

Geometry Plot:
  ✓ Plotted from XY, XZ, YZ views
  ✓ No dashed lines (no errors)
  ✓ Visual inspection confirms TRISO particles visible
  ✓ Capsule positions correct

VOID Test:
  ✓ 1M particles, 0 lost
  ✓ Geometry is watertight

Assessment: ALL Phase 1 reactor checks pass
Proceed to: Phase 2 test run (100k particles)
```

## Use Case 5: PWR Assembly Parametric Study

**Scenario:** Generate 20 inputs varying enrichment and burnable poison

**Phase 0 Check:**
```
Automation Requirements:
  Cases: 20 (5 enrichments × 4 BP loadings)

  Automation Decision: ✓ REQUIRED (≥3 cases)

  Approach: Template-based (Jinja2)
    - Base assembly geometry stable (17×17 lattice)
    - Parameters: enrichment, BP positions
    - Template variables: {{enrichment}}, {{bp_pattern}}

Generation Script:
  #!/usr/bin/env python3
  from jinja2 import Environment, FileSystemLoader

  enrichments = [3.5, 4.0, 4.5, 5.0, 5.5]
  bp_patterns = ['none', 'grid16', 'grid24', 'checkerboard']

  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template('pwr_assembly.template')

  for enr in enrichments:
      for bp in bp_patterns:
          output = template.render(
              enrichment=enr,
              bp_pattern=bp,
              case_name=f"enr{enr}_bp{bp}"
          )
          with open(f"inputs/case_enr{enr}_bp{bp}.i", 'w') as f:
              f.write(output)

Validation:
  ✓ Script generates all 20 inputs
  ✓ No numbering conflicts
  ✓ All cross-references valid
  ✓ README documents parameter ranges

Reproducibility:
  ✓ Template version controlled
  ✓ Generation script version controlled
  ✓ Parameters documented in CSV
  ✓ Single command: python generate_all.py

Assessment: Professional standards met
Proceed to: Phase 1 validation of ONE case, then generate all
```

## Use Case 6: Hexagonal Fast Reactor Core

**Scenario:** LAT=2 hexagonal assembly lattice validation

**Phase 0 & 1 Combined Check:**
```
Lattice Type Validation:

Assembly Choice: LAT=2 (hexagonal) ✓ Appropriate for fast reactor

Surface Type:
  ✗ Found: RPP (rectangular parallelepiped)
  ✓ Required: RHP (right hexagonal prism)

  ERROR: LAT=2 requires RHP surface, not RPP!

  Fix Required:
    WRONG: 200 rpp -10 10 -10 10 0 68
    RIGHT: 200 rhp  0 0 0  0 0 68  0 1.6 0

    Where:
      (0,0,0) = origin
      (0,0,68) = height vector (68 cm tall)
      (0,1.6,0) = R-vector (1.6 cm apothem)

Hexagonal Pitch:
  R = 1.6 cm (from RHP)
  Pitch = R × √3 = 1.6 × 1.732 = 2.77 cm

  Validation: Assembly spacing should be ~2.77 cm

Fill Array:
  Specified: fill=-6:6 -6:6 0:0
  Elements: (6-(-6)+1) × (6-(-6)+1) × 1 = 13 × 13 × 1 = 169

  ✓ Count matches (169 universe numbers provided)

  Pattern: Hexagonal symmetry visible in fill
    Row j=-6:  300 300 300 300 300 300 100 100 100 300 300 300 300
    Row j=-5:   300 300 300 100 100 100 100 100 100 100 300 300 300
    (Note: Indentation optional but helps visualize hex pattern)

Assessment: 1 CRITICAL error (RPP vs RHP)
Action: Fix surface type, then revalidate
```
```

---

### Enhancement 6: Add Automated Checking Tools

**New file:** `.claude/skills/mcnp-best-practices-checker/scripts/reactor_model_checker.py`

```python
#!/usr/bin/env python3
"""
Automated Reactor Model Best Practices Checker

Validates MCNP inputs against Phase 0 (Professional Standards)
and reactor-specific Phase 1 extensions.

Usage:
    python reactor_model_checker.py input.i
    python reactor_model_checker.py --all-inputs mcnp/*.i
    python reactor_model_checker.py --config checks.yaml input.i
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class MCNPInputParser:
    """Parse MCNP input file into structured data."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.cells = {}
        self.surfaces = {}
        self.materials = {}
        self.universes = set()
        self.lattices = []
        self.parse()

    def parse(self):
        """Parse MCNP input file."""
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        # Identify blocks (cells, surfaces, materials)
        blocks = self._identify_blocks(lines)

        # Parse each block
        self._parse_cells(blocks['cells'])
        self._parse_surfaces(blocks['surfaces'])
        self._parse_materials(blocks['materials'])

    def _identify_blocks(self, lines: List[str]) -> Dict[str, List[str]]:
        """Identify cell, surface, material blocks."""
        # Implementation details...
        pass

    def _parse_cells(self, lines: List[str]):
        """Extract cell definitions."""
        # Implementation details...
        pass

    def _parse_surfaces(self, lines: List[str]):
        """Extract surface definitions."""
        # Implementation details...
        pass

    def _parse_materials(self, lines: List[str]):
        """Extract material definitions."""
        # Implementation details...
        pass


class Phase0Checker:
    """Phase 0: Professional Modeling Standards"""

    def __init__(self, input_parser: MCNPInputParser, repo_path: Path):
        self.parser = input_parser
        self.repo_path = repo_path
        self.results = []

    def check_all(self) -> List[Dict]:
        """Run all Phase 0 checks."""
        self.check_version_control()
        self.check_numbering_scheme()
        self.check_data_separation()
        self.check_provenance()
        self.check_readme()
        self.check_thermal_scattering()
        self.check_automation()
        return self.results

    def check_version_control(self):
        """Item 1: Version control from start."""
        git_dir = self.repo_path / '.git'
        if git_dir.exists():
            self.results.append({
                'item': '0.1',
                'name': 'Version Control',
                'status': 'PASS',
                'message': 'Git repository detected'
            })
        else:
            self.results.append({
                'item': '0.1',
                'name': 'Version Control',
                'status': 'FAIL',
                'message': 'No version control (.git not found)',
                'action': 'Run: git init && git add . && git commit -m "Initial commit"'
            })

    def check_numbering_scheme(self):
        """Item 2: Systematic numbering scheme."""
        # Check for documented numbering scheme in header
        with open(self.parser.filepath, 'r') as f:
            header = ''.join(f.readlines()[:50])  # First 50 lines

        keywords = ['numbering', 'scheme', 'convention', 'cell id', 'surface id']
        has_documentation = any(kw in header.lower() for kw in keywords)

        if has_documentation:
            self.results.append({
                'item': '0.2',
                'name': 'Numbering Scheme Documentation',
                'status': 'PASS',
                'message': 'Numbering scheme documented in header'
            })
        else:
            self.results.append({
                'item': '0.2',
                'name': 'Numbering Scheme Documentation',
                'status': 'WARN',
                'message': 'Numbering scheme not documented in header',
                'action': 'Add comments explaining cell/surface/material ID structure'
            })

    def check_thermal_scattering(self):
        """Item 10: Thermal scattering for graphite/water."""
        issues = []

        # Check for graphite without MT card
        for mat_id, mat_data in self.parser.materials.items():
            has_carbon = 'c' in mat_data['isotopes'].lower() or '6000' in mat_data['isotopes']
            has_mt = mat_id in self.parser.mt_cards

            if has_carbon and not has_mt:
                issues.append(f"Material {mat_id} contains carbon but NO MT card")

        # Check for hydrogen (water) without MT card
        for mat_id, mat_data in self.parser.materials.items():
            has_hydrogen = 'h' in mat_data['isotopes'].lower() or '1001' in mat_data['isotopes']
            has_mt = mat_id in self.parser.mt_cards

            if has_hydrogen and not has_mt:
                issues.append(f"Material {mat_id} contains hydrogen but NO MT card")

        if issues:
            self.results.append({
                'item': '0.10',
                'name': 'Thermal Scattering',
                'status': 'FAIL',
                'message': f"Missing thermal scattering: {issues}",
                'action': 'Add MT cards (grph.XXt for C, lwtr.XXt for H2O, hwtr.XXt for D2O)',
                'impact': 'CRITICAL: 1000-5000 pcm reactivity error!'
            })
        else:
            self.results.append({
                'item': '0.10',
                'name': 'Thermal Scattering',
                'status': 'PASS',
                'message': 'All carbon/hydrogen materials have MT cards'
            })

    # Additional check methods...


class Phase1ReactorChecker:
    """Phase 1 Extensions: Reactor-Specific Checks"""

    def __init__(self, input_parser: MCNPInputParser):
        self.parser = input_parser
        self.results = []

    def check_all(self) -> List[Dict]:
        """Run all reactor-specific Phase 1 checks."""
        self.check_lattice_dimensions()
        self.check_repeat_notation()
        self.check_hex_lattice_surfaces()
        self.check_cross_references()
        self.check_numbering_conflicts()
        self.check_universe_hierarchy()
        self.check_volume_specs()
        return self.results

    def check_lattice_dimensions(self):
        """Item 1.23: Multi-level lattice validation."""
        for lat in self.parser.lattices:
            # Calculate expected elements
            i_count = lat['imax'] - lat['imin'] + 1
            j_count = lat['jmax'] - lat['jmin'] + 1
            k_count = lat['kmax'] - lat['kmin'] + 1
            expected = i_count * j_count * k_count

            # Count actual elements (handle nR notation)
            actual = self._count_fill_entries(lat['fill_array'])

            if actual == expected:
                self.results.append({
                    'item': '1.23',
                    'name': f"Lattice {lat['cell']} Dimensions",
                    'status': 'PASS',
                    'message': f"{actual} elements matches bounds {lat['bounds']}"
                })
            else:
                self.results.append({
                    'item': '1.23',
                    'name': f"Lattice {lat['cell']} Dimensions",
                    'status': 'FAIL',
                    'message': f"{actual} elements but expected {expected} from {lat['bounds']}",
                    'action': f"Fix FILL array: need {expected} elements",
                    'impact': 'CRITICAL: MCNP will fatal error'
                })

    def check_repeat_notation(self):
        """Item 1.24: Repeat notation validation."""
        for lat in self.parser.lattices:
            fill_str = lat['fill_array']

            # Find all nR patterns
            repeat_pattern = r'(\d+)\s+(\d+)R'
            repeats = re.findall(repeat_pattern, fill_str, re.IGNORECASE)

            warnings = []
            for universe, n in repeats:
                # nR gives n+1 copies
                actual_copies = int(n) + 1
                warnings.append(f"{universe} {n}R = {actual_copies} copies (not {n}!)")

            if warnings:
                self.results.append({
                    'item': '1.24',
                    'name': f"Lattice {lat['cell']} Repeat Notation",
                    'status': 'INFO',
                    'message': 'Repeat notation found: ' + ', '.join(warnings),
                    'note': 'Verify intended: nR gives n+1 total copies'
                })

    def check_hex_lattice_surfaces(self):
        """Item 1.25: Hexagonal lattice specifics."""
        for lat in self.parser.lattices:
            if lat['lat_type'] == 2:  # Hexagonal
                surf_id = lat['bounding_surface']
                surf_def = self.parser.surfaces.get(surf_id, {})
                surf_type = surf_def.get('type', '')

                if surf_type.upper() != 'RHP':
                    self.results.append({
                        'item': '1.25',
                        'name': f"Hex Lattice {lat['cell']} Surface",
                        'status': 'FAIL',
                        'message': f"LAT=2 uses {surf_type} but requires RHP",
                        'action': f"Change surface {surf_id} to RHP (right hexagonal prism)",
                        'impact': 'CRITICAL: Geometry will be incorrect'
                    })
                else:
                    self.results.append({
                        'item': '1.25',
                        'name': f"Hex Lattice {lat['cell']} Surface",
                        'status': 'PASS',
                        'message': 'LAT=2 correctly uses RHP surface'
                    })

    def check_cross_references(self):
        """Item 1.26: Cross-reference completeness."""
        errors = []

        # Check all cell-referenced surfaces are defined
        for cell_id, cell in self.parser.cells.items():
            for surf_ref in cell['surfaces']:
                surf_id = abs(surf_ref)  # Remove sign
                if surf_id not in self.parser.surfaces:
                    errors.append(f"Cell {cell_id} references undefined surface {surf_id}")

        # Check all material cells reference defined materials
        for cell_id, cell in self.parser.cells.items():
            mat_id = cell['material']
            if mat_id > 0 and mat_id not in self.parser.materials:
                errors.append(f"Cell {cell_id} references undefined material {mat_id}")

        # Check all fill cells reference defined universes
        for cell_id, cell in self.parser.cells.items():
            if 'fill' in cell:
                fill_u = cell['fill']
                if fill_u > 0 and fill_u not in self.parser.universes:
                    errors.append(f"Cell {cell_id} fill={fill_u} but universe not defined")

        if errors:
            self.results.append({
                'item': '1.26',
                'name': 'Cross-Reference Completeness',
                'status': 'FAIL',
                'message': f"{len(errors)} undefined references found",
                'details': errors,
                'impact': 'CRITICAL: MCNP will fatal error'
            })
        else:
            self.results.append({
                'item': '1.26',
                'name': 'Cross-Reference Completeness',
                'status': 'PASS',
                'message': 'All references valid'
            })

    def check_numbering_conflicts(self):
        """Item 1.27: Numbering scheme conflicts."""
        conflicts = []

        # Check for duplicate cell IDs
        cell_ids = list(self.parser.cells.keys())
        if len(cell_ids) != len(set(cell_ids)):
            duplicates = [cid for cid in cell_ids if cell_ids.count(cid) > 1]
            conflicts.append(f"Duplicate cell IDs: {set(duplicates)}")

        # Check for duplicate surface IDs
        surf_ids = list(self.parser.surfaces.keys())
        if len(surf_ids) != len(set(surf_ids)):
            duplicates = [sid for sid in surf_ids if surf_ids.count(sid) > 1]
            conflicts.append(f"Duplicate surface IDs: {set(duplicates)}")

        # Check for duplicate material IDs
        mat_ids = list(self.parser.materials.keys())
        if len(mat_ids) != len(set(mat_ids)):
            duplicates = [mid for mid in mat_ids if mat_ids.count(mid) > 1]
            conflicts.append(f"Duplicate material IDs: {set(duplicates)}")

        if conflicts:
            self.results.append({
                'item': '1.27',
                'name': 'Numbering Conflicts',
                'status': 'FAIL',
                'message': 'Duplicate IDs found',
                'details': conflicts,
                'action': 'Renumber conflicting entities',
                'impact': 'CRITICAL: Later definition overwrites earlier'
            })
        else:
            self.results.append({
                'item': '1.27',
                'name': 'Numbering Conflicts',
                'status': 'PASS',
                'message': 'No duplicate IDs'
            })

    def check_universe_hierarchy(self):
        """Item 1.23: Universe fill chain validation."""
        # Build directed graph of universe fills
        fill_graph = defaultdict(set)

        for cell_id, cell in self.parser.cells.items():
            if 'universe' in cell and 'fill' in cell:
                parent_u = cell['universe']
                child_u = cell['fill']
                fill_graph[parent_u].add(child_u)

        # Detect cycles using DFS
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in fill_graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        visited = set()
        rec_stack = set()
        cycles_found = []

        for node in fill_graph:
            if node not in visited:
                if has_cycle(node, visited, rec_stack):
                    cycles_found.append(node)

        if cycles_found:
            self.results.append({
                'item': '1.23',
                'name': 'Universe Hierarchy',
                'status': 'FAIL',
                'message': f"Circular universe references detected: {cycles_found}",
                'action': 'Restructure universe nesting to eliminate cycles',
                'impact': 'CRITICAL: MCNP will fatal error'
            })
        else:
            self.results.append({
                'item': '1.23',
                'name': 'Universe Hierarchy',
                'status': 'PASS',
                'message': 'No circular universe references'
            })

    def _count_fill_entries(self, fill_str: str) -> int:
        """Count elements in FILL array accounting for nR notation."""
        # Implementation to handle: "100 2R 200 24R 100 2R" → 3+25+3 = 31
        pass


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Reactor Model Best Practices Checker'
    )
    parser.add_argument('input_file', type=Path, help='MCNP input file')
    parser.add_argument('--repo-path', type=Path, default=Path.cwd(),
                       help='Repository root path (for version control check)')
    parser.add_argument('--phase', choices=['0', '1', 'all'], default='all',
                       help='Which phase to check')
    parser.add_argument('--output', choices=['text', 'json', 'markdown'], default='text',
                       help='Output format')

    args = parser.parse_args()

    # Parse input file
    print(f"Parsing MCNP input: {args.input_file}")
    mcnp_parser = MCNPInputParser(args.input_file)

    all_results = []

    # Run Phase 0 checks
    if args.phase in ['0', 'all']:
        print("\n" + "="*70)
        print("PHASE 0: PROFESSIONAL MODELING STANDARDS (15 items)")
        print("="*70)

        phase0 = Phase0Checker(mcnp_parser, args.repo_path)
        results0 = phase0.check_all()
        all_results.extend(results0)

        print_results(results0)

    # Run Phase 1 reactor checks
    if args.phase in ['1', 'all']:
        print("\n" + "="*70)
        print("PHASE 1: REACTOR-SPECIFIC EXTENSIONS (8 items)")
        print("="*70)

        phase1 = Phase1ReactorChecker(mcnp_parser)
        results1 = phase1.check_all()
        all_results.extend(results1)

        print_results(results1)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    total = len(all_results)
    passed = sum(1 for r in all_results if r['status'] == 'PASS')
    failed = sum(1 for r in all_results if r['status'] == 'FAIL')
    warned = sum(1 for r in all_results if r['status'] in ['WARN', 'INFO'])

    print(f"Total checks: {total}")
    print(f"  ✓ PASS: {passed}")
    print(f"  ✗ FAIL: {failed}")
    print(f"  ⚠ WARN: {warned}")

    if failed > 0:
        print("\n" + "!"*70)
        print("CRITICAL FAILURES FOUND - INPUT NOT READY FOR PRODUCTION")
        print("!"*70)
        print("\nFix all FAIL items before running MCNP.")
        sys.exit(1)
    elif warned > 0:
        print("\n" + "!"*70)
        print("WARNINGS FOUND - REVIEW RECOMMENDED")
        print("!"*70)
        print("\nConsider addressing WARN items for best practices.")
        sys.exit(0)
    else:
        print("\n" + "✓"*70)
        print("ALL CHECKS PASSED - INPUT READY FOR PHASE 2 TESTING")
        print("✓"*70)
        sys.exit(0)


def print_results(results: List[Dict]):
    """Print check results in formatted output."""
    for r in results:
        status_symbol = {
            'PASS': '✓',
            'FAIL': '✗',
            'WARN': '⚠',
            'INFO': 'ℹ'
        }.get(r['status'], '?')

        print(f"\n[{r['item']}] {status_symbol} {r['name']}")
        print(f"    Status: {r['status']}")
        print(f"    {r['message']}")

        if 'action' in r:
            print(f"    Action: {r['action']}")

        if 'impact' in r:
            print(f"    Impact: {r['impact']}")

        if 'details' in r:
            for detail in r['details']:
                print(f"      - {detail}")


if __name__ == '__main__':
    main()
```

---

## IMPLEMENTATION PLAN

### Step 1: Update SKILL.md (30 minutes)

**File:** `.claude/skills/mcnp-best-practices-checker/SKILL.md`

**Actions:**
1. Insert new "Phase 0: Professional Modeling Standards" section after Overview
2. Extend Phase 1 with items 23-30 (reactor-specific)
3. Add "Reactor Modeling Best Practices" section after Phase 4
4. Update "Integration with Other Skills" with extended workflow
5. Add Use Cases 4-6 (reactor-specific examples)

**Testing:**
- User asks: "Check my HTGR model for best practices"
- Expected: Skill mentions Phase 0 items (version control, thermal scattering, numbering)
- Expected: Skill checks multi-level lattice hierarchy

### Step 2: Create reactor_model_checker.py Script (60 minutes)

**File:** `.claude/skills/mcnp-best-practices-checker/scripts/reactor_model_checker.py`

**Complete implementation with:**
- MCNPInputParser class (parse cells/surfaces/materials/lattices)
- Phase0Checker class (15 items automated)
- Phase1ReactorChecker class (8 reactor-specific items)
- CLI interface with JSON/markdown output options
- Test suite with sample inputs

**Testing:**
```bash
# Test with HTGR model
python reactor_model_checker.py /path/to/sdr-agr.i

# Expected output:
# PHASE 0: 14/15 PASS, 1 FAIL (missing MT cards)
# PHASE 1: 8/8 PASS (if thermal scattering fixed)
```

### Step 3: Create Reference Files (45 minutes)

**Files to create:**

1. **reactor_patterns_reference.md**
   - Multi-level lattice hierarchies (PWR, HTGR, fast reactor)
   - Systematic numbering examples (AGR-1, microreactor)
   - Complete with diagrams

2. **automation_guide.md**
   - When to automate decision tree
   - Template-based vs programmatic comparison
   - Example workflows
   - Quality assurance checklist

3. **thermal_scattering_reference.md**
   - Complete MT card library
   - Temperature selection guide
   - Common errors and fixes

4. **reproducibility_checklist.md**
   - Professional standards requirements
   - DOI assignment process
   - Version control best practices

### Step 4: Update checklist_reference.md (15 minutes)

**File:** `.claude/skills/mcnp-best-practices-checker/checklist_reference.md`

**Add:**
- Phase 0 items with detailed explanations
- Phase 1 items 23-30 detailed explanations
- Examples from HTGR analysis

### Step 5: Create Example Validation Reports (30 minutes)

**File:** `.claude/skills/mcnp-best-practices-checker/examples/htgr_validation_report.md`

Show complete validation of AGR-1 model:
- Phase 0: ALL items checked
- Phase 1: Standard + reactor-specific items
- Example output from automated checker
- Annotated with explanations

**File:** `.claude/skills/mcnp-best-practices-checker/examples/pwr_validation_report.md`

PWR assembly validation example

### Step 6: Integration Testing (30 minutes)

**Test scenarios:**

1. **HTGR model without thermal scattering:**
   - Should FAIL Phase 0 Item 10
   - Should recommend mt9040 grph.18t

2. **PWR assembly with LAT=2 + RPP surface:**
   - Should FAIL Phase 1 Item 25
   - Should recommend changing to RHP

3. **Model with circular universe references:**
   - Should FAIL Phase 1 Item 23
   - Should identify cycle

4. **Well-constructed reactor model:**
   - Should PASS all Phase 0 and Phase 1 items
   - Should provide green light for Phase 2

---

## VALIDATION TESTS

### Test 1: Thermal Scattering Detection

**Input:** MCNP file with graphite material, no MT card

**Expected Output:**
```
[0.10] ✗ Thermal Scattering
    Status: FAIL
    Missing thermal scattering: Material m9040 contains carbon but NO MT card
    Action: Add MT cards (grph.XXt for C, lwtr.XXt for H2O)
    Impact: CRITICAL: 1000-5000 pcm reactivity error!
```

### Test 2: Lattice Dimension Validation

**Input:** fill=-7:7 -7:7 0:0 with only 220 elements (missing 5)

**Expected Output:**
```
[1.23] ✗ Lattice 91108 Dimensions
    Status: FAIL
    220 elements but expected 225 from fill=-7:7 -7:7 0:0
    Action: Fix FILL array: need 225 elements
    Impact: CRITICAL: MCNP will fatal error
```

### Test 3: Hexagonal Lattice Surface Type

**Input:** LAT=2 lattice with RPP bounding surface

**Expected Output:**
```
[1.25] ✗ Hex Lattice 200 Surface
    Status: FAIL
    LAT=2 uses RPP but requires RHP
    Action: Change surface 200 to RHP (right hexagonal prism)
    Impact: CRITICAL: Geometry will be incorrect
```

### Test 4: Professional Standards - No Version Control

**Input:** Model file in directory without .git

**Expected Output:**
```
[0.1] ✗ Version Control
    Status: FAIL
    No version control (.git not found)
    Action: Run: git init && git add . && git commit -m "Initial commit"
```

### Test 5: Circular Universe Reference

**Input:** u=100 fill=200, u=200 fill=100

**Expected Output:**
```
[1.23] ✗ Universe Hierarchy
    Status: FAIL
    Circular universe references detected: [100, 200]
    Action: Restructure universe nesting to eliminate cycles
    Impact: CRITICAL: MCNP will fatal error
```

---

## SUCCESS CRITERIA

**Skill refinement successful when:**

1. ✅ User asking "validate my HTGR model" gets Phase 0 + reactor-specific checks
2. ✅ Missing thermal scattering is FLAGGED as CRITICAL error
3. ✅ Multi-level lattice hierarchies are validated (dimensions, circular refs)
4. ✅ Hexagonal lattice surface types are checked (LAT=2 requires RHP)
5. ✅ Numbering scheme documentation is encouraged
6. ✅ Automation/reproducibility standards are enforced
7. ✅ Automated checker script works on real reactor models
8. ✅ Professional workflow integration guidance provided
9. ✅ Reference materials cover common reactor patterns
10. ✅ All examples from HTGR analysis incorporated

---

## ESTIMATED TIMELINE

| Task | Time | Dependencies |
|------|------|--------------|
| Update SKILL.md | 30 min | None |
| Create reactor_model_checker.py | 60 min | Parser implementation |
| Create reference files (4 files) | 45 min | None |
| Update checklist_reference.md | 15 min | SKILL.md complete |
| Create example reports (2) | 30 min | None |
| Integration testing | 30 min | Script complete |
| Documentation review | 10 min | All complete |

**Total:** ~3.5 hours

---

## DEPENDENCIES

**Requires completion/updates of:**
- mcnp-lattice-builder (lattice dimension validation logic)
- mcnp-cross-reference-checker (cross-ref validation patterns)
- mcnp-material-builder (thermal scattering requirements)

**Provides validation for:**
- All reactor modeling skills
- mcnp-input-builder
- mcnp-template-generator
- mcnp-programmatic-generator

---

## NOTES

**Key Insights from HTGR Analysis:**

1. **Phase 0 is Critical:** Professional models REQUIRE systematic practices before MCNP validation
2. **Thermal Scattering Non-Negotiable:** Missing MT cards for graphite/water = 1000+ pcm error
3. **Automation Not Optional:** 10,000-line reactor models cannot be manually maintained
4. **Reproducibility Required:** Publication and licensing demand complete workflow documentation
5. **Multi-Level Lattices Common:** Reactor models routinely use 4-6 levels of nesting
6. **Systematic Numbering Essential:** Prevents conflicts and enables debugging
7. **Cross-Referencing Complex:** Automated validation catches errors humans miss

**This enhancement transforms the skill from "general best practices" to "professional reactor modeling standards" while preserving the core 57-item checklist.**

---

**END OF REFINEMENT PLAN**

Ready for immediate implementation. All content based on proven patterns from production HTGR models.
