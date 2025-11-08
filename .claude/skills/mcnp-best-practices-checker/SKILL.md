---
category: C
name: mcnp-best-practices-checker
description: "Review MCNP inputs against the 57-item best practices checklist from Chapter 3.4 to ensure correct and efficient simulations before running"
version: "2.0.0"
---

# MCNP Best Practices Checker

## Overview

This skill systematically reviews MCNP inputs against the comprehensive best practices checklist from Chapter 3.4, extended with professional reactor modeling standards. These practices exist because users got wrong answers by skipping them - they are requirements for reliable results, not optional suggestions.

The checklist is organized into five phases:
- **Phase 0: Professional Modeling Standards** (15 items - BEFORE input creation)
- **Phase 1: Problem Setup** (30 items - before first run, including 8 reactor-specific)
- **Phase 2: Preproduction** (20 items - during test runs)
- **Phase 3: Production** (10 items - during long runs)
- **Phase 4: Criticality** (5 items - additional for KCODE)

**Extension for Reactor Models:** Phase 0 and the reactor-specific Phase 1 items are CRITICAL for professional reactor modeling (HTGRs, PWRs, fast reactors). They prevent maintenance nightmares, ensure reproducibility, and catch reactor-specific errors like missing thermal scattering.

## When to Use This Skill

- **Before ANY MCNP run** (proactive quality assurance)
- After input creation but before running production
- When results seem questionable or unexpected
- Before criticality (KCODE) production runs
- When preparing inputs for publication or licensing
- As final review in validation workflow

## The Extended Checklist

### Phase 0: Professional Modeling Standards (PRE-SETUP) - 15 Items

**BEFORE creating input file - prevents maintenance and reproducibility issues**

**Critical for:** Reactor models, automated generation, publication/licensing, collaboration

**Project Organization (Items 1-5):**

1. **Version control from start** (git, hg, or svn) - **CRITICAL**
   - Track all input files, generation scripts, data
   - Enables rollback and collaboration
   - Required for reproducible research
   - Action: `git init && git add . && git commit -m "Initial model"`

2. **Design numbering scheme BEFORE implementation**
   - Allocate digit ranges by entity type
   - Encode hierarchy in numbers (cell 91234 → capsule 9, stack 1, etc.)
   - Document scheme in input header
   - Prevents conflicts in large models (1000+ cells)

3. **Separate data from logic**
   - External data in CSV/JSON files (not hardcoded)
   - Parameters in separate definition files
   - Enables systematic parameter studies
   - Makes validation easier

4. **Document provenance of ALL values**
   - Each number traceable to source (paper, handbook, measurement)
   - Include references in comments
   - Required for validation and licensing
   - Example: `c Density from ORNL/TM-2006/12, Table 3.2`

5. **README with complete workflow**
   - How to regenerate inputs from scratch
   - Software dependencies and versions
   - Expected outputs and validation criteria
   - Single command regeneration goal

**Geometry Design (Items 6-9):**

6. **Plan universe hierarchy BEFORE coding**
   - Draw containment tree diagram
   - Identify all nested levels (typically 3-6 for reactors)
   - Allocate universe number ranges
   - Prevents circular references

7. **Choose lattice types appropriately**
   - LAT=1 (rectangular) for: PWR assemblies, vertical stacks, regular grids
   - LAT=2 (hexagonal) for: HTGR cores, fast reactor assemblies, hex fuel
   - Mixed types allowed in same model
   - Document choice rationale

8. **Validate lattice dimensions mathematically**
   - Element count = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
   - Surface extent = N × pitch (rectangular) or matches hex pattern
   - ALWAYS account for zero in index ranges!
   - Pre-calculate before coding

9. **Use systematic cell/surface correlation**
   - Cell 1234 uses surfaces 1234X, material m1234
   - Immediate identification of relationships
   - Simplifies debugging
   - Document pattern in header

**Materials (Items 10-12):**

10. **Thermal scattering REQUIRED for** - **CRITICAL**
    - ALL graphite (any reactor type)
    - ALL water (light or heavy)
    - Polyethylene, beryllium, BeO
    - Impact: 1000-5000 pcm error if missing
    - Choose temperature-appropriate library (grph.10t @ 294K vs grph.18t @ 600K)
    - Example: `mt9040 grph.18t $ 600K for operating HTGR`

11. **Temperature-consistent cross sections**
    - Match S(α,β) temperature to physics temperature
    - Use same library family (.70c, .80c, NOT mixed .70c and .21c)
    - Document temperature assumptions in comments
    - Example: All .80c for consistency

12. **Material density specifications consistent**
    - Negative = g/cm³, positive = atoms/barn-cm
    - Document which convention in comments
    - Validate atom fractions sum to expected range
    - Check against handbook values

**Automation (Items 13-15):**

13. **Automate for ≥3 similar cases**
    - Template-based (Jinja2) OR programmatic (Python functions)
    - Reduces copy-paste errors
    - Enables rapid parameter variations
    - Maintain templates with inputs

14. **Validate generated outputs**
    - Compare to reference case
    - Check numbering conflicts (duplicate IDs)
    - Verify all cross-references exist
    - Automated validation script recommended

15. **Reproducible generation**
    - Single command regenerates all inputs
    - Scripts version-controlled with inputs
    - External data frozen at known versions
    - Document in README

**Why Phase 0 Matters:**
- Professional reactor models have 1000-10,000+ cells
- Manual editing at this scale is error-prone and unmaintainable
- These practices are REQUIRED for publication, licensing, collaboration
- Following these saves weeks/months on large projects
- 30 minutes on Phase 0 saves days debugging 10,000-line files

### Phase 1: Problem Setup (§3.4.1) - 30 Items (22 Standard + 8 Reactor-Specific)

**Before first run - prevents basic errors**

**Geometry (Items 1-7):**
1. Draw geometry picture on paper
2. **ALWAYS plot geometry** (mcnp6 ip) - **CRITICAL**
3. Model in sufficient detail (not too simple, not too complex)
4. Use simple cells (avoid complex Boolean expressions)
5. Use simplest surfaces (prefer RPP, SPH, RCC macrobodies)
6. Avoid excessive # operator (sign of over-complexity)
7. Build incrementally (test each addition)

**Organization (Items 8-9):**
8. Use READ card for common components
9. Pre-calculate volumes/masses (compare with MCNP VOL output)

**Validation (Items 10-13):**
10. **Use VOID card test** - **CRITICAL** (finds overlaps/gaps quickly)
11. Check source (Tables 10, 110, 170)
12. Check source with mesh tally (visual verification)
13. Understand physics approximations and limitations

**Cross Sections & Tallies (Items 14-16):**
14. Cross-section sets matter! (verify libraries in output)
15. Separate tallies for fluctuation (don't combine too much)
16. Conservative variance reduction (start simple)

**General (Items 17-22):**
17. Don't use too many VR techniques (diminishing returns)
18. Balance user vs computer time (don't over-optimize)
19. **Study ALL warnings** - **CRITICAL**
20. Generate best output (PRINT card for detailed tables)
21. Recheck INP file (materials, source, tallies correct?)
22. Garbage in = garbage out (MCNP will run bad inputs!)

**Reactor Model Specifics (Items 23-30):**

23. **Multi-level lattice validation**
    - All child universes defined BEFORE parent fills with them
    - No circular references (u=100 fill=200, u=200 fill=100)
    - Lattice bounding surface matches N × pitch
    - FILL array element count matches declared bounds
    - Test: Extract all universe IDs, verify no cycles

24. **Repeat notation validation** (nR syntax)
    - Remember: `U nR` gives (n+1) total copies, NOT n!
    - Example: `100 2R` = 100 100 100 (3 copies)
    - Validate: sum of pattern = (KMAX-KMIN+1) × (JMAX-JMIN+1) × (IMAX-IMIN+1)
    - Common error: Off by one in element count

25. **Hexagonal lattice specifics** (if LAT=2 used)
    - Bounding surface is RHP (right hexagonal prism), NOT RPP
    - Pitch = R × √3 (R from RHP definition)
    - Staggered row pattern in FILL array
    - Cannot use rectangular bounding surface with LAT=2

26. **Cross-reference completeness**
    - Every cell references DEFINED surfaces only
    - Every material cell references DEFINED material
    - Every fill references DEFINED universe
    - No orphaned surfaces (defined but never used)
    - Use mcnp-cross-reference-checker skill

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
    - Example: `91234 10 -1.0 -91234 imp:n=1 $ Capsule 1, Stack 2, Compact 3, Kernel`

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

**Detailed Explanations:** See `checklist_reference.md` for why each matters and consequences

### Phase 2: Preproduction (§3.4.2) - 20 Items

**During short test runs (10k-100k particles)**

**Understanding (Items 1-3):**
1. Don't use as black box (understand Monte Carlo theory)
2. Run short calculations first (10k-100k for testing)
3. Examine outputs carefully (read entire output)

**Statistics (Items 4-7):**
4. Study summary tables (activity, collisions, tracks)
5. **Study statistical checks** (all 10 must pass) - **CRITICAL**
6. Study FOM and VOV trends (should be stable)
7. Consider collisions/particle (typical: 100-10,000)

**Efficiency (Items 8-12):**
8. Examine track populations (particles getting where needed?)
9. Scan mean-free-path column (identify problem regions)
10. Check detector diagnostics (F5, DXTRAN effectiveness)
11. Understand large contributions (no single particle dominance)
12. Reduce unimportant tracks (kill in unimportant regions)

**Physics (Items 13-14):**
13. Check secondary production (expected numbers?)
14. Back-of-envelope check (does answer make sense?)

**Remaining Items:** See `checklist_reference.md` for Items 15-20

### Phase 3: Production (§3.4.3) - 10 Items

**During long production runs**

**Files (Items 1-2):**
1. Save RUNTPE (for analysis and restarts)
2. Limit RUNTPE size with PRDMP (balance restart vs disk)

**Statistics (Items 3-8):**
3. Check FOM stability (should be roughly constant)
4. Answers seem reasonable (physics intuition)
5. **Examine 10 statistical checks** (ALL must pass) - **CRITICAL**
6. Form valid confidence intervals (understand error bars)
7. Continue-run if necessary (until converged)
8. Verify errors decrease 1/√N (theory validation)

**Final (Items 9-10):**
9. Accuracy has multiple factors (not just statistics!)
10. Adequately sample all cells (check track populations)

### Phase 4: Criticality (§3.4.4) - 5 Items

**Additional for KCODE problems**

1. **Determine inactive cycles** (plot keff and Shannon entropy) - **CRITICAL**
2. Large histories/cycle (minimum 10,000 for production)
3. Examine keff behavior (stable after inactive cycles)
4. At least 100 active cycles (for confidence intervals)
5. Recheck convergence after run (verify inactive sufficient)

## Reactor Modeling Best Practices

**Purpose:** Guidance for professional reactor model development based on production HTGR/PWR/fast reactor experience

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

**See:** `automation_guide.md` for detailed workflows and examples

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

**See:** `thermal_scattering_reference.md` for complete library guide

### Cross-Referencing Validation

**Critical Validations (automate these!):**

**Use mcnp-cross-reference-checker skill OR:**
- All cell-referenced surfaces are defined
- All material cells reference defined materials
- All fill cells reference defined universes
- No orphaned surfaces (defined but never used)
- No circular universe references
- No duplicate IDs (cells, surfaces, materials, universes)

**Automated validation recommended for:**
- Models with >100 cells
- Multi-level lattice hierarchies
- Programmatically generated inputs
- Before production runs

### Reproducibility Standards

**Essential for Professional Work:**

1. **Version Control All Source Files**
   ```bash
   git init
   git add *.py *.csv *.template README.md
   git commit -m "Initial reactor model - baseline configuration"
   git tag v1.0-baseline
   ```

2. **Document Dependencies**
   ```
   # requirements.txt
   python==3.11.0
   numpy==1.24.0
   pandas==2.0.0
   jinja2==3.1.2

   # MCNP version: MCNP6.2 (build 2020-02-14)
   # Cross sections: ENDF/B-VII.1 (xsdir from 2018-05-01)
   ```

3. **README with Complete Workflow**
   - Single command to regenerate all inputs
   - Software dependencies and versions
   - Expected outputs and validation criteria
   - Data provenance documentation

**See:** `reproducibility_checklist.md` for complete requirements

## Use Case 1: Pre-Production Review

**Scenario:** User ready to run expensive production calculation

**Workflow:**

**Step 1: Phase 1 Review**
```
Critical Items Check:
✗ Item 2: Geometry not plotted yet
  Action: MUST run `mcnp6 ip i=input.inp` NOW
  Why: Catches 90% of errors before expensive run

✗ Item 10: VOID test not performed
  Action: Run VOID card test with 1M particles
  Why: Quickly finds overlaps/gaps

✓ Item 14: Consistent cross sections (all .80c)
✓ Item 19: No warnings in test run
✓ Item 20: PRINT card included

Assessment: 3/22 critical items incomplete
Action Required: STOP - Complete plotting and VOID test first
Estimated Time: 30 minutes to complete Phase 1
```

**Step 2: Recommendations**
```
BEFORE ANY PRODUCTION RUN:

1. Plot geometry (MANDATORY):
   mcnp6 ip i=input.inp
   # Plot from 3 views minimum (XY, XZ, YZ)
   # Look for dashed lines = errors

2. Run VOID test (MANDATORY):
   [Generate test input with VOID card]
   # If particles lost → geometry error
   # Must pass before production

3. Pre-calculate volumes:
   Expected: ~50,000 cm³ (from drawings)
   Compare: VOL card output after test
   # Large difference (>5%) = geometry error
```

**Step 3: Next Phase**
```
After Phase 1 complete:
→ Run 100k particle test (Phase 2)
→ Check all 10 statistical tests pass
→ Verify FOM stable
→ If passes → Proceed to production
```

## Use Case 2: KCODE Production Setup

**Scenario:** Criticality calculation needs validation

**Additional Checks (Phase 4):**
```
Criticality-Specific Requirements:

1. Shannon entropy convergence:
   Status: Trending upward through cycle 50
   Problem: Source not converged
   Action: Increase inactive cycles to 100

2. Histories per cycle:
   Current: 5,000
   Minimum: 10,000 for production
   Action: Increase to 20,000

3. Active cycles:
   Current: 50
   Minimum: 100
   Action: Increase to 150

KCODE Recommendation:
  Current: KCODE  5000  1.0  50  100
  Required: KCODE  20000  1.0  100  250
```

## Use Case 3: Results Seem Wrong

**Scenario:** Production run complete but results questionable

**Diagnostic Checklist:**
```
Phase 1 Retroactive Check:
□ Was geometry plotted? (Item 2)
□ Was VOID test performed? (Item 10)
□ Were volumes pre-calculated? (Item 9)
□ Were all warnings studied? (Item 19)

Phase 2/3 Statistical Check:
□ Do all 10 statistical tests pass? (Items 2.5, 3.5)
□ Is FOM stable? (Items 2.6, 3.3)
□ Are errors decreasing as 1/√N? (Item 3.8)
□ Back-of-envelope reasonable? (Item 2.14)

If Critical Items Missed:
→ Cannot trust results
→ Must go back and complete checks
→ Rerun after validation
```

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

## Integration with Other Skills

**Extended Validation Workflow for Reactor Models**

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

## References

### Comprehensive Guides
- **checklist_reference.md:** Complete 57-item checklist with detailed explanations, why each matters, and consequences of skipping
- **scripts/README.md:** Automated checking tools and workflow guidance

### MCNP Documentation
- **Chapter 3.4:** Tips for Correct and Efficient Problems (source of checklist)
  - §3.4.1: Problem Setup (22 items)
  - §3.4.2: Preproduction (20 items)
  - §3.4.3: Production (10 items)
  - §3.4.4: Criticality (5 items)
- **Chapter 2.6.9:** Tally statistics theory
- **Chapter 6:** Geometry plotting

### Related Skills
- mcnp-input-validator (syntax checking)
- mcnp-geometry-checker (geometry validation)
- mcnp-statistics-checker (statistical quality)
- mcnp-warning-analyzer (warning interpretation)

## Best Practices

1. **Not Optional:** These are requirements, not suggestions
2. **Fix First Error First:** Don't skip validation steps
3. **30 Minutes Now Saves Days Later:** Time spent on validation pays off
4. **"I'm in a Hurry" Not an Excuse:** Wrong faster ≠ better
5. **Document Everything:** Track what you checked and when
6. **Iterative Process:** Expect to revise and revalidate
7. **When in Doubt:** Over-validate rather than under-validate
8. **Phase Order Matters:** Don't skip to Phase 3 without completing Phase 1-2
9. **Critical Items Are Critical:** Items marked CRITICAL must not be skipped
10. **MCNP Will Run Bad Inputs:** You are responsible for validation

## Critical Reminders

**Never Skip:**
- Geometry plotting (Item 1.2) - 90% of errors found here
- VOID card test (Item 1.10) - Finds overlaps/gaps quickly
- All warnings studied (Item 1.19) - May indicate serious issues
- All 10 statistical checks (Items 2.5, 3.5) - Results validity requirement
- Shannon entropy converged (Item 4.1) - Keff reliability requirement

**Remember:**
- MCNP doesn't check physics reasonableness
- No error message ≠ correct answer
- Statistical convergence ≠ accuracy
- You are responsible for ensuring results are right

## Validation Checklist

Before declaring input ready for production:
- [ ] Phase 1 complete (all 22 items addressed)
- [ ] Critical items verified: plotting (2), VOID test (10), warnings (19)
- [ ] Phase 2 test run completed (10k-100k particles)
- [ ] All 10 statistical checks passed
- [ ] FOM stable (±10%)
- [ ] Back-of-envelope check reasonable
- [ ] For KCODE: Shannon entropy converged (flat in final 30% of inactive)
- [ ] For KCODE: At least 100 active cycles planned
- [ ] Documentation complete (what checked, what found, what fixed)

---

**END OF MCNP BEST PRACTICES CHECKER SKILL**

For detailed explanations of each checklist item, consequences, and examples, see checklist_reference.md.
