# PHASE 1 PROJECT STATUS - PART 5 (MCNP-LATTICE-BUILDER FOCUS)

**Phase:** 1 of 5 (Category A & B Skills)
**Part:** 5 (Created when Part 4 exceeded 900 lines)
**Session:** 15
**Date:** 2025-11-04
**Skills Complete:** 6/16 (25.0%)

---

## CRITICAL NOTE ON mcnp-lattice-builder PRIORITY

**User Assessment:** mcnp-lattice-builder is ONE OF THE MOST CRITICAL MCNP skills, not "medium" priority

**Rationale:**
- Significant amounts of reactor models use lattices
- Lattice geometry is heavily utilized by nuclear engineering professionals
- Essential for reactor-to-MCNP translation capability
- Ultimate integration test goal: Build full reactor models from design specs alone
- Without robust lattice capability, integration testing will fail

**Priority Elevation:** HIGH → CRITICAL

---

## SUMMARY OF PREVIOUS PARTS

### Part 1 (Sessions 3-8)
- ✅ mcnp-input-builder (Completed Session 8)
- ✅ mcnp-geometry-builder (Completed Session 8)

### Part 2 (Sessions 9-10)
- ✅ mcnp-material-builder (Completed Session 10)

### Part 3 (Sessions 11-13)
- ✅ mcnp-source-builder (Completed Session 13)

### Part 4 (Session 14)
- 🚧 mcnp-tally-builder (40% complete - Steps 5-11 remaining)
  - Steps 1-4 completed in Session 14
  - Created CHAPTER-5-09-SUMMARY.md (2,425 words)
  - Created 7 detailed reference files (~8,500 words total)
  - Token-optimized workflow achieved 20% efficiency gain

**Part 4 Status:** Archived at 1,055 lines, active work continues in next session

---

## PART 5 FOCUS: MCNP-LATTICE-BUILDER

### Why Special Treatment

**User Directive:** Different approach than standard 11-step workflow

**Special Requirements:**
1. Read Chapter 5.02 (Cell Cards) and 5.05 (Geometry Data Cards)
2. Extract lattice-specific information
3. Parse AGR-1 research article for reactor modeling context
4. Create comprehensive skill revamp plan
5. Emphasize reactor-to-MCNP translation capability

**Documentation Created (Session 15):**
- ✅ LATTICE-INFO-SUMMARY.md (comprehensive lattice reference)
- ✅ AGR-1-KEY-INFO.md (reactor modeling example)
- ✅ PHASE-1-PROJECT-STATUS-PART-5.md (this document)

---

## LATTICE-INFO-SUMMARY.MD CONTENTS

**File:** `skill-revamp/LATTICE-INFO-SUMMARY.md`
**Word Count:** ~6,400 words
**Source:** Chapters 5.02 and 5.05 from MCNP6.3.1 manual

**Sections Covered:**
1. Overview of MCNP repeated structures
2. Cell card fundamentals (Form 1, Form 2 LIKE BUT)
3. Boolean operators and complement shortcuts
4. Universe concept (U card)
5. Lattice card (LAT - two types)
6. Lattice indexing (surface order critical)
7. FILL card (single fill, array fill, special values)
8. Coordinate transformations (TR and TRCL)
9. Repeated structures workflow
10. Practical examples (3 detailed examples)
11. Lattice design checklist
12. Common pitfalls and solutions (6 major pitfalls)
13. Computational considerations
14. Integration with other MCNP features
15. Summary of key takeaways (10 points)

**Key Insights Extracted:**
- Surface order on LAT cell card defines lattice indexing
- Two lattice types: Hexahedral (LAT=1) and Hexagonal prism (LAT=2)
- FILL flexibility: Single universe OR array specification
- Negative universe optimization (use with extreme caution)
- No speed benefit (only memory/input savings)
- Volume specification must account for ALL instances

---

## AGR-1-KEY-INFO.MD CONTENTS

**File:** `skill-revamp/AGR-1-KEY-INFO.md`
**Word Count:** ~5,100 words
**Source:** Research article on AGR-1 experiment (Fairhurst-Agosta & Kozlowski, 2024)

**Sections Covered:**
1. Project overview (AGR-1 TRISO irradiation test in ATR)
2. Reactor facility (Advanced Test Reactor configuration)
3. AGR-1 test train geometry (6 capsules, 72 compacts)
4. Capsule types and variants (baseline, variant 1, 2, 3)
5. Modeling simplifications (regular lattice for TRISO)
6. TRISO fuel particle structure (5 layers)
7. Photon source contributions (time evolution)
8. Dose rate results
9. Repeated structures approach methodology
10. μHTGR microreactor example
11. Critical insights for lattice builder
12. Translation from literature to MCNP
13. Benchmark calculations
14. Lessons for future MCNP modeling

**Key Insights for Lattice Builder:**
- Regular lattice assumption: Trade-off between accuracy and feasibility
- Flux-based grouping essential (not whole core as single universe)
- Multi-level hierarchies: Core → Assembly → Fuel channel → TRISO
- Verification exercise: 15.6% error for whole-core grouping, 4.3% for flux-based
- Volume specification critical for repeated structures
- AGR-1: 6 capsules × 3 columns × 4 compacts × ~thousands of TRISO particles each

---

## SKILL REVAMP PLAN FOR MCNP-LATTICE-BUILDER

### Step 1: Review Current SKILL.md

**Current File:** `.claude/skills/mcnp-lattice-builder/SKILL.md`

**Action Required:** Read and analyze current structure

**Expected Findings:**
- Current word count estimate: ~900 lines
- Likely contains some lattice basics
- May lack comprehensive reactor modeling context
- Probably missing AGR-1-style complex examples
- May not emphasize reactor-to-MCNP translation workflow

**Status:** ⏸️ Pending (Next session)

---

### Step 2: Cross-Reference with Documentation

**Documentation Now in Context (Session 15):**
- ✅ LATTICE-INFO-SUMMARY.md (comprehensive reference)
- ✅ AGR-1-KEY-INFO.md (reactor modeling example)

**Additional Documentation to Review:**
- Chapter 5.02: Cell Cards (partial - read lines 1-59 in session)
- Chapter 5.05: Geometry Data Cards (read lines 1-700, 701-1378 in session)

**Documentation Assessment:**
- Comprehensive lattice theory covered
- Practical examples included
- Reactor modeling context established
- Flux-based grouping strategies documented

**Status:** ✅ Complete

---

### Step 3: Identify Discrepancies and Gaps

**Expected Gaps (to be confirmed in next session):**

**Content Coverage:**
1. Missing comprehensive U/LAT/FILL card interaction documentation
2. Likely lacks flux-based grouping strategy discussion
3. Probably missing reactor-to-MCNP translation workflow
4. May not include AGR-1-style hierarchical lattice examples
5. Likely missing HTGR double heterogeneity discussion
6. Probably lacks TRISO particle lattice modeling guidance
7. May not emphasize surface ordering for lattice indexing
8. Likely missing common pitfalls specific to lattices
9. Probably lacks multi-level hierarchy examples (3+ levels)
10. May not include verification strategies for complex lattices

**Example Files:**
1. Missing reactor-model examples from example_files/
2. Likely lacks AGR-1-style complex hierarchical examples
3. Probably missing HTGR core examples
4. May not have hexagonal lattice examples (LAT=2)
5. Likely missing transformation with lattice examples

**Scripts:**
1. Probably no lattice index calculation script
2. Likely no lattice volume calculation helper
3. Probably no universe hierarchy visualization tool
4. May not have fill array generator script

**Status:** ⏸️ Pending detailed analysis (Next session)

---

### Step 4: Create Detailed Skill Revamp Plan (REFINED FROM GAP ANALYSIS)

**Gap Analysis Complete:** See `LATTICE-BUILDER-GAP-ANALYSIS.md` for detailed findings

**Summary of Gaps:**
- CRITICAL: Missing reactor modeling workflow
- CRITICAL: Missing flux-based grouping strategy (15.6% vs 4.3% errors)
- CRITICAL: Missing HTGR double heterogeneity discussion
- HIGH: Surface ordering not sufficiently emphasized
- HIGH: Volume specification for repeated structures needs emphasis
- Word count too high: 5,800 words → target <3,000 words

---

**Content to Extract to references/ (FROM Current SKILL.md):**

**Priority 1: Core Lattice Theory**

- [ ] `lattice_fundamentals.md` (~2,500 words)
  **Extract from current SKILL.md:**
  - Lines 56-70: Universe concept
  - Lines 72-88: Lattice concept (LAT=1, LAT=2)
  - Lines 90-111: Fill concept (simple, indexed, transformation)
  - Lines 148-263: Rectangular lattice detailed construction
  - Lines 265-375: Hexagonal lattice orientation and indexing
  **Add from LATTICE-INFO-SUMMARY.md:**
  - Boolean operators and complement shortcuts
  - Surface ordering schemes (critical addition)
  - FILL array Fortran ordering conventions
  - Lattice element requirements (convex, opposite sides parallel)

- [ ] `transformations_for_lattices.md` (~1,800 words)
  **Extract from current SKILL.md:**
  - Lines 439-489: Transformations with FILL examples
  **Add from LATTICE-INFO-SUMMARY.md:**
  - TR card full syntax (displacement vector, rotation matrix)
  - TRCL card formats (reference vs inline)
  - Rotation matrix shortcuts (9, 6, 5, 3, 0 elements)
  - m parameter (origin interpretation)
  - Coordinate system relationships

- [ ] `universe_hierarchy_guide.md` (~1,500 words)
  **Extract from current SKILL.md:**
  - Lines 377-437: Nested lattices (3-level reactor example)
  **Add from LATTICE-INFO-SUMMARY.md:**
  - Universe 0 vs filled universes
  - Multi-level hierarchies (up to 20 levels)
  - Negative universe optimization (with STRONG warnings)
  - Importance inheritance in universes
  - Universe nesting design principles

**Priority 2: Reactor Modeling Context (NEW CONTENT - CRITICAL)**

- [ ] `reactor_to_mcnp_workflow.md` (~2,000 words)
  **Source: AGR-1-KEY-INFO.md**
  - Translating reactor design specs to MCNP lattices
  - Information typically available in literature (geometric specs, materials, power)
  - Information often missing (exact densities, gap dimensions, detailed geometry)
  - Making reasonable assumptions
  - Documenting assumptions clearly
  - Sensitivity analysis approach
  - Validation against published values

- [ ] `htgr_double_heterogeneity.md` (~1,500 words)
  **Source: AGR-1-KEY-INFO.md**
  - TRISO particle 5-layer structure (kernel, buffer, IPyC, SiC, OPyC)
  - Double heterogeneity concept (particle-level + compact-level)
  - Regular lattice vs stochastic (URAN card) trade-offs
  - Computational necessity for regular lattices (millions of particles)
  - Multi-level hierarchy: Core → Assembly → Fuel channel → Compact → TRISO
  - AGR-1 example: 6 capsules × 3 columns × 4 compacts × thousands of TRISO

- [ ] `flux_based_grouping_strategies.md` (~1,200 words)
  **Source: AGR-1-KEY-INFO.md verification exercise**
  - Why whole-core single universe fails: 15.6% error (unacceptable)
  - Assembly-level grouping: 4.3% error (acceptable)
  - Explicit cells: 0% error (reference, but impractical for large systems)
  - Rule: Group by flux zone, not geometric convenience
  - Determining appropriate group size (balance accuracy vs cost)
  - Each group = independent depletion (accuracy improvement)
  - When to use finer grouping (strong spatial flux gradients)

**Priority 3: Advanced Topics**

- [ ] `lattice_verification_methods.md` (~1,000 words)
  **Source: AGR-1-KEY-INFO.md + LATTICE-INFO-SUMMARY.md**
  - Geometry plotting with index labels (essential tool)
  - Volume calculation verification
  - Simplified reference case comparison
  - Cross-section through lattice planes
  - Particle tracking verification
  - Checking for flux spatial effects
  - Verifying gamma source intensities
  - Cross-checking at multiple conditions

- [ ] `common_lattice_errors.md` (~1,500 words)
  **Extract from current SKILL.md:**
  - Lines 663-676: Lost particle errors (universe cells not contained)
  - Lines 678-693: FILL index out of range
  - Lines 697-712: Lattice spacing incorrect
  - Lines 714-726: Can't tally in specific element
  - Lines 728-735: Hexagonal orientation wrong
  - Lines 737-749: Nested lattice levels confused
  **Add from LATTICE-INFO-SUMMARY.md:**
  - Incorrect surface ordering (index mismatch) - MOST COMMON
  - Non-convex cross-sections
  - Missing FILL card
  - Array index mismatch
  - Transformation confusion
  - Negative universe misuse (silent errors)

**Total references/ content: ~13,000 words**

---

---

**Examples to Add to assets/:**

**Priority 1: Basic Examples**
- [ ] `example_01_simple_cubic_lattice.i`
  - 3×3×3 cubic lattice
  - Single universe fills all elements
  - Demonstrates LAT=1 basic usage
  - Description: ~200 words

- [ ] `example_02_hexagonal_lattice.i`
  - Hexagonal prism lattice (LAT=2)
  - Demonstrates 8-surface indexing
  - Single universe fill
  - Description: ~200 words

- [ ] `example_03_array_fill_rectangular.i`
  - Rectangular lattice with array FILL
  - Different universes in different positions
  - Non-rectangular array (some elements = 0)
  - Description: ~300 words

**Priority 2: Intermediate Examples**
- [ ] `example_04_fuel_assembly_pins.i`
  - Fuel assembly with pin lattice
  - Control rod positions
  - Multiple material types
  - Source: basic_examples/ or reactor-model_examples/
  - Description: ~400 words

- [ ] `example_05_lattice_with_transformations.i`
  - Multiple identical lattices at different positions
  - TRCL transformations
  - Demonstrates coordinate system relationships
  - Description: ~350 words

- [ ] `example_06_nested_lattices.i`
  - 2-level hierarchy
  - Lattice of lattices
  - Demonstrates universe nesting
  - Description: ~450 words

**Priority 3: Advanced Examples (Reactor Modeling)**
- [ ] `example_07_htgr_compact_triso_hierarchy.i`
  - 3-level hierarchy: Compact → Column → TRISO particles
  - Regular TRISO lattice
  - Demonstrates flux-based grouping concept
  - Source: Based on AGR-1 structure
  - Description: ~600 words

- [ ] `example_08_reactor_core_assembly_lattice.i`
  - Core lattice of fuel assemblies
  - Each assembly = universe with internal structure
  - Demonstrates reactor-level modeling
  - Source: reactor-model_examples/ (potentially HTGR or similar)
  - Description: ~700 words

- [ ] `example_09_agr1_simplified_capsule.i`
  - Simplified AGR-1 single capsule
  - 3 columns × 4 compacts arrangement
  - TRISO particles in regular lattice
  - Demonstrates literature-to-MCNP translation
  - Source: Based on AGR-1-KEY-INFO.md
  - Description: ~800 words

- [ ] `example_10_verification_exercise.i`
  - Based on verification exercise from AGR-1 paper
  - 8×8 pin array with flux-based grouping
  - Includes reference case for comparison
  - Description: ~500 words

**Total examples: 10 files (~4,500 words descriptions)**

---

**Scripts to Create in scripts/:**

**Priority 1: Lattice Helpers**
- [ ] `lattice_index_calculator.py`
  - Calculate lattice indices from surface ordering
  - Visualize index scheme for hexahedral or hexagonal
  - Input: Surface list, lattice type
  - Output: Index diagram, neighbor relationships
  - ~200 lines

- [ ] `fill_array_generator.py`
  - Generate FILL array syntax from structured input
  - Handle dimension declarations
  - Format array values correctly
  - Input: Array dimensions, universe assignments
  - Output: MCNP FILL card syntax
  - ~150 lines

- [ ] `universe_hierarchy_visualizer.py`
  - Parse MCNP input and extract universe tree
  - Visualize hierarchy (ASCII art or graph)
  - Identify universe nesting levels
  - Input: MCNP input file
  - Output: Hierarchy diagram, statistics
  - ~250 lines

**Priority 2: Verification Tools**
- [ ] `lattice_volume_checker.py`
  - Verify volume specifications for repeated structures
  - Calculate total volume across all instances
  - Compare against user specification
  - Input: MCNP input file with lattice
  - Output: Volume report, warnings if mismatch
  - ~180 lines

- [ ] `surface_order_validator.py`
  - Check surface ordering on LAT cell cards
  - Verify indexing matches intent
  - Identify potential ordering errors
  - Input: MCNP cell card definition
  - Output: Index scheme interpretation, warnings
  - ~150 lines

**Priority 3: Reactor Modeling Helpers**
- [ ] `reactor_spec_to_lattice.py`
  - Template generator for reactor lattice from specs
  - Input: Assembly pitch, core dimensions, fuel specs
  - Output: MCNP lattice skeleton (user fills details)
  - ~300 lines

- [ ] `README.md`
  - Usage documentation for all scripts
  - Examples for each script
  - Installation requirements
  - ~800 words

**Total scripts: 7 files (~1,230 lines + README)**

---

**Templates for assets/templates/:**

- [ ] `rectangular_lattice_template.i`
  - LAT=1 template with placeholders
  - Comments explaining each section
  - Surface order marked clearly
  - FILL examples included
  - ~150 lines

- [ ] `hexagonal_lattice_template.i`
  - LAT=2 template with placeholders
  - 8-surface ordering clearly marked
  - Hexagonal prism geometry setup
  - ~150 lines

- [ ] `nested_lattice_template.i`
  - 2-level hierarchy template
  - Universe nesting clearly shown
  - FILL within FILL example
  - ~200 lines

- [ ] `reactor_core_template.i`
  - Core → Assembly → Pin hierarchy
  - Flux-based grouping example
  - Transformation examples
  - ~250 lines

- [ ] `template_README.md`
  - Explanation of each template
  - How to customize for specific use case
  - Common modifications
  - ~600 words

**Total templates: 5 files**

---

**SKILL.md Streamlining Plan:**

**Current estimated word count:** ~2,700 words (estimate based on ~900 lines)

**Target word count:** <3,000 words (preferred), <5,000 words (maximum)

**Structure per Anthropic Standards:**

```markdown
---
name: mcnp-lattice-builder
description: "Constructs MCNP repeated structures (U/LAT/FILL) for reactor cores, fuel assemblies, and complex geometries with hierarchical organization."
version: "2.0.0"
dependencies: "mcnp-geometry-builder, mcnp-material-builder"
---

# MCNP Lattice Builder

## Overview
[3 paragraphs: What, Why, How]
- What: Build U/LAT/FILL repeated structures
- Why: Essential for reactor modeling, millions of repeated elements
- How: Hierarchical universes, lattice indexing, FILL specifications

## When to Use This Skill
[8-10 bulleted trigger conditions]
- Building reactor core with repeated fuel assemblies
- Modeling HTGR with TRISO particles
- Creating pin-by-pin fuel assembly geometry
- Translating reactor design specs to MCNP
- Setting up multi-level hierarchical structures
- Optimizing large repeated geometries for memory
- Verifying lattice indexing and universe nesting
- Troubleshooting lattice-related geometry errors

## Decision Tree
[ASCII workflow diagram]
```
User needs repeated geometry
    ↓
Single repeated element or array?
    ├→ Single → Use U + FILL (single universe)
    └→ Array → Continue
         ↓
    Rectangular or hexagonal?
         ├→ Rectangular → LAT=1 (6 surfaces)
         └→ Hexagonal → LAT=2 (8 surfaces)
              ↓
         All elements same?
              ├→ Yes → FILL = n (single universe)
              └→ No → FILL array (i1:i2 j1:j2 k1:k2...)
                   ↓
              Need transformations?
                   ├→ Yes → Add TRCL to filled cell
                   └→ No → Continue
                        ↓
                   Multiple levels?
                        ├→ Yes → Nested universes (U/FILL recursion)
                        └→ No → Complete
                             ↓
                        Verify lattice indices
                             └→ Use geometry plotter with labels
```

## Quick Reference

| Concept | Card | Example | Notes |
|---------|------|---------|-------|
| Universe | U=n | U=1 | Assign cell to universe |
| Lattice type | LAT=n | LAT=1 | 1=hexahedral, 2=hex prism |
| Fill single | FILL=n | FILL=2 | All elements = universe 2 |
| Fill array | FILL=i1:i2... | FILL=0:2 0:1 0:0 <br> 1 2 3 <br> 4 5 6 | i varies fastest |
| Transform | TRCL=n | TRCL=5 | Reference TR5 card |
| Surface order LAT=1 | Cell card | 1 0 -1 -2 -3 4 -5 6 U=1 LAT=1 | Sfc 1→[1,0,0], 2→[-1,0,0], ... |
| Surface order LAT=2 | Cell card | 2 0 -1 -2 -3 4 -5 6 -7 8 U=1 LAT=2 | 8 surfaces for hex prism |

## Use Cases

### Use Case 1: Simple Cubic Fuel Assembly

**Scenario:** Need to create 3×3 array of fuel pins in water

**Goal:** Model fuel assembly with 9 identical pins

**Approach:**
1. Define fuel pin geometry in universe 1 (cell, surfaces)
2. Define water background in universe 1
3. Create lattice cell with LAT=1, U=2
4. FILL=1 (all elements filled with universe 1)
5. Container cell with FILL=2

**Implementation:**
```
c Fuel pin (universe 1)
1  1  -10.0  -10      U=1  $ Fuel
2  2  -1.0    10      U=1  $ Water

c Lattice cell (universe 2)
3  0  -11 12 -13 14 -15 16  U=2  LAT=1  FILL=1

c Container
4  0  -20               FILL=2
5  0  20                IMP:N=0

c Surfaces
10  CZ  0.5           $ Fuel pin radius
11  PX  0             $ Lattice boundaries
12  PX  4.5
13  PY  0
14  PY  4.5
15  PZ  0
16  PZ  100
20  RPP -1 6 -1 6 -1 110  $ Container
```

**Key Points:**
- Surface order on cell 3 defines indices: 11→[1,0,0], 12→[-1,0,0], ...
- Lattice elements [0,0,0] through [2,2,0] exist (3×3×1)
- All filled with same universe (uniform array)

**Expected Results:** 9 fuel pins in 3×3 arrangement

### Use Case 2: Reactor Core with Different Assembly Types

**Scenario:** Core with fuel assemblies and control assemblies in specific pattern

**Goal:** Model full reactor core with mixed assembly types

**Approach:**
1. Define fuel assembly as universe 1
2. Define control assembly as universe 2
3. Create core lattice with LAT=1
4. Use FILL array to place assemblies

**Implementation:**
```
c Core lattice
10  0  -100 101 -102 103 -104 105  U=5  LAT=1
      FILL=-3:3 -3:3 0:0
           2 1 1 1 1 1 2    $ j=-3, i=-3:3
           1 1 2 1 2 1 1    $ j=-2
           1 2 1 1 1 2 1    $ j=-1
           1 1 1 2 1 1 1    $ j=0
           1 2 1 1 1 2 1    $ j=1
           1 1 2 1 2 1 1    $ j=2
           2 1 1 1 1 1 2    $ j=3

c Fuel assembly (universe 1) - simplified
100  1  -10.0  -200  U=1  $ Fuel region
101  2  -1.0    200  U=1  $ Moderator

c Control assembly (universe 2) - simplified
102  3  -8.0   -200  U=2  $ Control material
103  2  -1.0    200  U=2  $ Moderator

[... surfaces ...]
```

**Key Points:**
- FILL array: 7×7×1 = 49 assemblies
- Pattern shows control assemblies (2) at corners and strategic positions
- Fuel assemblies (1) fill majority of core
- i-index varies fastest in array specification

### Use Case 3: HTGR TRISO Particle Lattice

**Scenario:** Fuel compact with thousands of TRISO particles in regular lattice

**Goal:** Model TRISO particles explicitly using repeated structures

**Approach:**
1. Define single TRISO particle (5-layer structure) in universe 10
2. Create compact lattice in universe 20
3. Create assembly with multiple compacts in universe 30
4. Use flux-based grouping (one universe per compact for independent depletion)

**Implementation:**
```
c TRISO particle (universe 10)
1   1  10.8   -1              U=10  $ Kernel (UO2)
2   2  0.98    1 -2           U=10  $ Buffer (C)
3   3  1.85    2 -3           U=10  $ IPyC
4   4  3.20    3 -4           U=10  $ SiC
5   5  1.86    4 -5           U=10  $ OPyC
6   6  3.20    5              U=10  $ Matrix (SiC)

c Compact lattice (universe 20)
10  0  -10 11 -12 13 -14 15   U=20  LAT=1  FILL=10  VOL=<total>

c Single compact cell in assembly
20  0  -20  FILL=20  TRCL=(0 0 0)    $ Compact 1
21  0  -21  FILL=21  TRCL=(0 0 6.8)  $ Compact 2
... [more compacts]

c Surfaces
1   SO  0.025        $ Kernel radius
2   SO  0.035        $ Buffer
3   SO  0.039        $ IPyC
4   SO  0.0425       $ SiC
5   SO  0.0465       $ OPyC
10  PX  0            $ Lattice cell
11  PX  0.1
12  PY  0
13  PY  0.1
14  PZ  0
15  PZ  0.1
20  RCC 0 0 0  0 0 6.8  1.15   $ Compact 1 cylinder
21  RCC 0 0 6.8  0 0 6.8  1.15  $ Compact 2 cylinder
```

**Key Points:**
- 5-layer TRISO structure explicitly modeled
- Regular lattice with 0.1 cm pitch (example)
- Each compact = separate universe (flux-based grouping)
- VOL must specify total volume of all TRISO particles × matrix

**Expected Results:** Thousands of TRISO particles in compact, suitable for depletion/activation

### Use Case 4: Translating Reactor Design Specs to MCNP

**Scenario:** Given reactor design paper with assembly pitch, core dimensions, fuel specifications

**Goal:** Create MCNP lattice model from literature specifications

**Information Available (typical):**
- Core layout: 24 fuel assemblies, 12 control, hexagonal arrangement
- Assembly pitch: 30 cm
- Fuel channel radius: 1.15 cm
- Coolant channel radius: 0.775 cm
- Channel pitch: 3.2 cm

**Approach:**
1. Design universe hierarchy: Core (level 0) → Assembly (level 1) → Channel (level 2)
2. Create channel lattice within each assembly
3. Create assembly lattice for core
4. Group assemblies by expected flux level

**Implementation Strategy:**
```
c Level 2: Single channel cell (universe 5 = fuel, universe 6 = coolant)
c Level 1: Assembly lattice (universe 10)
c    - LAT=2 (hexagonal) for channels
c    - FILL array for fuel vs coolant pattern
c Level 0: Core lattice (real world)
c    - LAT=2 (hexagonal) for assemblies
c    - FILL array for fuel vs control assemblies

c Grouping strategy:
c    - Inner ring assemblies: Universe 10 (high flux)
c    - Middle ring assemblies: Universe 11 (medium flux)
c    - Outer ring assemblies: Universe 12 (lower flux)
c    - Control assemblies: Universe 20
```

**Key Points:**
- Start from smallest repeated unit (channel)
- Build hierarchy level by level
- Group by flux zones (not geometric convenience)
- Verify dimensions and indices at each level

**Expected Results:** Full core model ready for neutronics analysis

### Use Case 5: Debugging Lattice Index Mismatch

**Scenario:** Lattice elements appearing in wrong positions

**Goal:** Fix surface ordering to match intended index scheme

**Diagnostic Process:**
1. Run geometry plotter with lattice index labels
2. Compare shown indices with intended scheme
3. Check surface order on LAT cell card
4. Identify which surfaces need reordering

**Solution Approach:**
- For LAT=1: Surfaces must be in pairs (±x, ±y, ±z directions)
- For LAT=2: Surfaces follow specific 8-surface convention
- Reorder surfaces on cell card to match intended indices
- Verify again with plotter

**Key Points:**
- Surface order ≠ surface numbering
- Order on cell card determines index directions
- Geometry plotter is essential verification tool

## Integration with Other Skills

**Typical Workflow:**
1. **mcnp-geometry-builder** → Create base element geometry (cells, surfaces)
2. **mcnp-material-builder** → Define materials for lattice elements
3. **mcnp-lattice-builder** (THIS SKILL) → Organize into repeated structures
4. **mcnp-source-builder** → Define source in lattice geometry
5. **mcnp-tally-builder** → Set up tallies on lattice elements
6. **mcnp-input-validator** → Verify complete input

**Complementary Skills:**
- **mcnp-geometry-checker:** Verify no overlaps in lattice elements
- **mcnp-cell-checker:** Validate U/FILL references
- **mcnp-transform-editor:** Adjust TRCL transformations
- **mcnp-input-editor:** Modify large lattice specifications efficiently

**Example Complete Workflow:**
```
Project Goal: Model HTGR core with explicit TRISO particles

Step 1: mcnp-geometry-builder - Define TRISO 5-layer structure
Step 2: mcnp-material-builder - Define UO2, C, SiC materials
Step 3: mcnp-lattice-builder - Create TRISO lattice → Compact → Assembly → Core
Step 4: mcnp-source-builder - Define neutron source in core
Step 5: mcnp-tally-builder - Set up flux, heating tallies
Step 6: mcnp-input-validator - Check U/FILL references, volumes
Result: Full HTGR model ready for KCODE or fixed-source calculation
```

## References

**Detailed Information:**
- Lattice fundamentals: See `references/lattice_fundamentals.md`
- Transformations: See `references/transformations_for_lattices.md`
- Universe hierarchy: See `references/universe_hierarchy_guide.md`
- Reactor modeling: See `references/reactor_to_mcnp_workflow.md`
- HTGR double heterogeneity: See `references/htgr_double_heterogeneity.md`
- Flux-based grouping: See `references/flux_based_grouping_strategies.md`
- Verification methods: See `references/lattice_verification_methods.md`
- Common errors: See `references/common_lattice_errors.md`

**Templates and Examples:**
- Lattice templates: See `assets/templates/`
- Simple examples: See `assets/example_inputs/example_01-06*.i`
- Advanced examples: See `assets/example_inputs/example_07-10*.i`
- AGR-1 reference: See `../../skill-revamp/AGR-1-KEY-INFO.md`

**Automation Tools:**
- Index calculator: `scripts/lattice_index_calculator.py`
- FILL generator: `scripts/fill_array_generator.py`
- Hierarchy visualizer: `scripts/universe_hierarchy_visualizer.py`
- Volume checker: `scripts/lattice_volume_checker.py`
- Surface validator: `scripts/surface_order_validator.py`
- Reactor template: `scripts/reactor_spec_to_lattice.py`
- Usage guide: `scripts/README.md`

**External Documentation:**
- MCNP6 Manual Chapter 5.2: Cell Cards
- MCNP6 Manual Chapter 5.5: Geometry Data Cards
- MCNP6 Manual Chapter 10.1.3: Repeated Structures Examples

## Best Practices

1. **Always verify surface order on LAT cell card** - This defines your index scheme. Use geometry plotter with index labels to confirm before proceeding with complex models.

2. **Group by flux zones, not geometric convenience** - Whole-core as single universe can produce 15%+ errors. Group assemblies/regions with similar flux levels for independent depletion.

3. **Start simple and build hierarchy incrementally** - Test each level (channel → compact → assembly → core) separately before combining. Easier to debug in stages.

4. **Specify volumes carefully for repeated structures** - Volume must account for ALL instances, not single element. Critical for source intensities and tally normalization.

5. **Use negative universe only when absolutely certain** - Cell must be fully enclosed, never truncated by higher-level boundaries. Plot thoroughly and run VOID check. Wrong usage produces silent errors.

6. **Plot, plot, plot** - Geometry plotter is your best verification tool. Multiple views, different angles, with lattice indices displayed. Catch errors before expensive runs.

7. **Document universe hierarchy clearly** - Use comments to show nesting structure. Future you (or colleague) will thank you. Example: "U=1 (fuel pin) → U=10 (assembly) → U=0 (core)".

8. **FILL arrays follow Fortran ordering** - First index varies fastest. Write out explicit pattern in comments to avoid confusion later.

9. **For reactor models: Use flux-based independent depletion groups** - Each assembly (or zone) = separate universe for independent flux/depletion. Critical for activation/burnup accuracy.

10. **Verify with simplified reference case** - Before modeling millions of TRISO particles, test approach with 10-pin array. Compare explicit vs repeated structures to validate methodology.

---

## TODOS FOR MCNP-LATTICE-BUILDER REVAMP

### Documentation Review (Step 1)
- [ ] Read current SKILL.md completely
- [ ] Note current word count and structure
- [ ] Identify strengths to preserve
- [ ] List areas for improvement
- [ ] Determine if reactor modeling context is present
- [ ] Check for AGR-1-style examples
- [ ] Assess discussion of flux-based grouping
- [ ] Verify surface ordering emphasis

### Gap Analysis (Step 3)
- [ ] Document missing U/LAT/FILL card documentation
- [ ] Identify flux-based grouping discussion gaps
- [ ] Check reactor-to-MCNP workflow presence
- [ ] Assess hierarchical examples (3+ levels)
- [ ] Evaluate HTGR double heterogeneity coverage
- [ ] Review TRISO particle lattice guidance
- [ ] Check surface ordering emphasis
- [ ] Assess common lattice pitfalls coverage
- [ ] Evaluate verification strategy discussion
- [ ] Review example complexity progression

### Content Extraction (Step 5)
- [ ] Create lattice_fundamentals.md (~2,500 words)
- [ ] Create transformations_for_lattices.md (~1,800 words)
- [ ] Create universe_hierarchy_guide.md (~1,500 words)
- [ ] Create reactor_to_mcnp_workflow.md (~2,000 words)
- [ ] Create htgr_double_heterogeneity.md (~1,500 words)
- [ ] Create flux_based_grouping_strategies.md (~1,200 words)
- [ ] Create lattice_verification_methods.md (~1,000 words)
- [ ] Create common_lattice_errors.md (~1,500 words)

### Example Files (Step 6)
- [ ] Identify source files from example_files/reactor-model_examples/
- [ ] Create example_01_simple_cubic_lattice.i + description
- [ ] Create example_02_hexagonal_lattice.i + description
- [ ] Create example_03_array_fill_rectangular.i + description
- [ ] Create example_04_fuel_assembly_pins.i + description (from examples)
- [ ] Create example_05_lattice_with_transformations.i + description
- [ ] Create example_06_nested_lattices.i + description
- [ ] Create example_07_htgr_compact_triso_hierarchy.i + description (AGR-1 based)
- [ ] Create example_08_reactor_core_assembly_lattice.i + description (from examples)
- [ ] Create example_09_agr1_simplified_capsule.i + description (AGR-1 based)
- [ ] Create example_10_verification_exercise.i + description (8×8 pins)

### Script Creation (Step 7)
- [ ] Create lattice_index_calculator.py (~200 lines)
- [ ] Create fill_array_generator.py (~150 lines)
- [ ] Create universe_hierarchy_visualizer.py (~250 lines)
- [ ] Create lattice_volume_checker.py (~180 lines)
- [ ] Create surface_order_validator.py (~150 lines)
- [ ] Create reactor_spec_to_lattice.py (~300 lines)
- [ ] Create scripts/README.md (~800 words)

### Template Creation (Step 6 continued)
- [ ] Create rectangular_lattice_template.i (~150 lines)
- [ ] Create hexagonal_lattice_template.i (~150 lines)
- [ ] Create nested_lattice_template.i (~200 lines)
- [ ] Create reactor_core_template.i (~250 lines)
- [ ] Create assets/templates/template_README.md (~600 words)

### SKILL.md Streamlining (Step 8)
- [ ] Restructure to Anthropic standard format
- [ ] Write Overview section (3 paragraphs)
- [ ] Write When to Use This Skill section (8-10 conditions)
- [ ] Create ASCII Decision Tree
- [ ] Create Quick Reference table
- [ ] Write Use Case 1: Simple Cubic Fuel Assembly
- [ ] Write Use Case 2: Reactor Core with Different Assembly Types
- [ ] Write Use Case 3: HTGR TRISO Particle Lattice
- [ ] Write Use Case 4: Translating Reactor Design Specs to MCNP
- [ ] Write Use Case 5: Debugging Lattice Index Mismatch
- [ ] Write Integration with Other Skills section
- [ ] Write References section (point to bundled resources)
- [ ] Write Best Practices section (10 numbered items)
- [ ] Verify word count <3,000 words (preferred) or <5,000 (max)
- [ ] Ensure no duplication with references/ content

### YAML Frontmatter (Step 9)
- [ ] Set name: mcnp-lattice-builder
- [ ] Write third-person trigger-specific description
- [ ] Set version: "2.0.0"
- [ ] Add dependencies: "mcnp-geometry-builder, mcnp-material-builder"
- [ ] Remove non-standard fields if present

### Quality Validation (Step 9)
- [ ] YAML: name matches directory
- [ ] YAML: description is third-person and trigger-specific
- [ ] YAML: no non-standard fields
- [ ] YAML: version 2.0.0
- [ ] YAML: dependencies listed
- [ ] SKILL.md: Overview section (2-3 paragraphs)
- [ ] SKILL.md: When to Use section with bullets
- [ ] SKILL.md: Decision tree (ASCII)
- [ ] SKILL.md: Quick reference table
- [ ] SKILL.md: 5 use cases with standard format
- [ ] SKILL.md: Integration section
- [ ] SKILL.md: References section
- [ ] SKILL.md: Best practices (10 items)
- [ ] SKILL.md: Word count <5k (ideally <3k)
- [ ] SKILL.md: No duplication with references/
- [ ] Resources: references/ directory exists
- [ ] Resources: Large content extracted (>500 words)
- [ ] Resources: scripts/ directory with functional tools
- [ ] Resources: assets/ directory with examples
- [ ] Resources: assets/templates/ with templates
- [ ] Resources: Each example has description
- [ ] Content: All MCNP syntax valid
- [ ] Content: Cross-references accurate
- [ ] Content: Documentation paths correct

### Testing (Step 10)
- [ ] Invoke mcnp-lattice-builder skill with Claude Code
- [ ] Verify skill activates correctly
- [ ] Test references/ files load when referenced
- [ ] Test scripts/ execute without errors
- [ ] Verify examples in assets/ are accessible
- [ ] Check integration links work
- [ ] Document any issues found

### Status Update (Step 11)
- [ ] Move skill from "Currently Active" to "Completed Skills"
- [ ] Create completion entry with summary
- [ ] List structure: references/ [X files], scripts/ [Y files], assets/ [Z examples]
- [ ] Note validation: 25-item checklist passed
- [ ] Record word count
- [ ] Update progress counters (5/16 Phase 1, 5/36 total)

---

## SESSION 15 PROGRESS SUMMARY

### Completed Work

**Documentation Created:**
1. ✅ **AGR-Literature-MCNP-BUILD-REVIEW.md** (~16,000 words)
   - Comprehensive connection between AGR-1 literature and sdr-agr.i MCNP model
   - 16 major sections covering structure, TRISO implementation, lattice hierarchy
   - Detailed analysis of 4-level nesting, flux-based grouping, and material organization
   - Critical lessons and recommended examples identified

2. ✅ **references/lattice_fundamentals.md** (~4,200 words)
   - Universe concept (U card) with containment rules
   - Lattice concept (LAT=1 rectangular, LAT=2 hexagonal)
   - Fill concept (simple, array, transformation)
   - Surface ordering for lattice indexing
   - Fortran ordering for FILL arrays
   - No speed benefit clarification

3. ✅ **references/reactor_to_mcnp_workflow.md** (~3,800 words)
   - Information typically available vs missing in literature
   - 9-step translation workflow (extract → hierarchy → implement → validate)
   - Assumption documentation requirements
   - Flux-based grouping integration
   - AGR-1 complete translation example

4. ✅ **references/flux_based_grouping_strategies.md** (~3,200 words)
   - AGR-1 verification exercise results (15.6% vs 4.3% error)
   - The Rule: Group by flux zone, not geometric convenience
   - Determining appropriate group size
   - Implementation strategy (unique materials per group)
   - When whole-core grouping fails

5. ✅ **references/htgr_double_heterogeneity.md** (~4,900 words)
   - TRISO 5-layer structure (kernel/buffer/IPyC/SiC/OPyC)
   - Double heterogeneity concept (particle + compact level)
   - 4-level hierarchy implementation (particle → lattice → compact → channel)
   - Regular vs stochastic distribution trade-offs
   - Common pitfalls (volume specs, matrix filler, infinite cells)

**Gap Analysis Completed:**
- Current SKILL.md: 804 lines, ~2,700 words (borderline length)
- CRITICAL gaps identified: Reactor modeling workflow, flux-based grouping, HTGR/TRISO
- YAML issues: Non-standard fields need removal
- Strengths preserved: Decision tree, PWR/VVER examples, troubleshooting

**Files Read:**
- AGR-1 MCNP model (sdr-agr.i): 4653 lines in 8 parallel chunks
- AGR-1-KEY-INFO.md: 515 lines
- Current SKILL.md: 804 lines
- CLAUDE-SESSION-REQUIREMENTS.md: 1152 lines

### Remaining Work for mcnp-lattice-builder

**Step 5: Extract Content to references/ (4 MORE files needed)**

Priority reference files still needed:
1. **common_lattice_errors.md** (~1,500 words)
   - Extract from current SKILL.md lines 663-749
   - Add from LATTICE-INFO-SUMMARY.md pitfalls
   - Surface ordering errors (MOST COMMON)
   - Universe containment failures
   - FILL index mismatches
   - Lattice spacing errors
   - Hexagonal orientation issues

2. **transformations_for_lattices.md** (~1,800 words)
   - TR card full syntax (9, 6, 5, 3, 0 element shortcuts)
   - TRCL formats (reference vs inline)
   - Rotation matrix conventions
   - m parameter (origin interpretation)
   - Examples from current SKILL.md lines 439-489

3. **universe_hierarchy_guide.md** (~1,500 words)
   - Extract from current SKILL.md lines 377-437
   - Universe 0 vs filled universes
   - Multi-level hierarchies (up to 20 levels)
   - Negative universe optimization (with warnings)
   - Importance inheritance

4. **lattice_verification_methods.md** (~1,000 words)
   - Geometry plotting with index labels
   - Volume calculation verification
   - Cross-section visualization
   - Particle tracking verification
   - Methods from AGR-1 analysis

**Step 6: Add Example Files to assets/ (10 examples needed)**

Directory: `.claude/skills/mcnp-lattice-builder/assets/example_inputs/`

Basic examples (1-3):
- example_01_simple_cubic_lattice.i (~200 lines)
- example_02_hexagonal_lattice.i (~200 lines)
- example_03_array_fill_rectangular.i (~300 lines)

Intermediate examples (4-6):
- example_04_fuel_assembly_pins.i (~400 lines)
- example_05_lattice_with_transformations.i (~350 lines)
- example_06_nested_lattices.i (~450 lines)

Advanced examples (7-10) - CRITICAL for reactor modeling:
- example_07_htgr_compact_triso_hierarchy.i (~600 lines) - Based on AGR-1
- example_08_reactor_core_assembly_lattice.i (~700 lines)
- example_09_agr1_simplified_capsule.i (~800 lines) - Key validation example
- example_10_verification_exercise.i (~500 lines) - Flux grouping demonstration

**MANDATORY:** Invoke mcnp-input-builder skill BEFORE writing any example files

**Step 7: Create/Bundle Scripts in scripts/ (6 scripts needed)**

Directory: `.claude/skills/mcnp-lattice-builder/scripts/`

Priority 1 scripts:
1. **lattice_index_calculator.py** (~200 lines)
   - Calculate indices from surface ordering
   - Visualize LAT=1 and LAT=2 schemes
   - Input: Surface list, lattice type
   - Output: Index diagram

2. **fill_array_generator.py** (~150 lines)
   - Generate FILL array syntax
   - Handle dimension declarations
   - Format with Fortran ordering

3. **universe_hierarchy_visualizer.py** (~250 lines)
   - Parse MCNP input
   - Extract universe tree
   - ASCII art or graph visualization

Priority 2 scripts:
4. **lattice_volume_checker.py** (~180 lines)
   - Verify volume specifications
   - Calculate total across instances
   - Compare against user specs

5. **surface_order_validator.py** (~150 lines)
   - Check surface ordering on LAT cells
   - Verify indexing matches intent
   - Identify potential errors

6. **reactor_spec_to_lattice.py** (~300 lines)
   - Template generator from specs
   - Input: Pitch, dimensions, fuel specs
   - Output: MCNP lattice skeleton

7. **README.md** (~800 words)
   - Usage for each script
   - Examples and installation

**Step 8: Streamline SKILL.md**

Target: <3,000 words (currently ~2,700, but needs MAJOR restructuring)

**Critical additions needed:**
- Reactor modeling workflow section (NEW)
- Flux-based grouping emphasis (NEW)
- HTGR/TRISO use case (NEW)
- Surface ordering as CRITICAL point (EMPHASIZE)

**Structure per Anthropic standards:**
- Overview (2-3 paragraphs)
- When to Use This Skill (8-10 trigger conditions including reactor modeling)
- Decision Tree (preserve current, excellent)
- Quick Reference (table format)
- Use Cases (5 total):
  1. Simple cubic fuel assembly (keep current)
  2. Reactor core with different assembly types (keep current)
  3. HTGR TRISO particle lattice (NEW - CRITICAL)
  4. Translating reactor design specs to MCNP (NEW - CRITICAL)
  5. Debugging lattice index mismatch (NEW or adapt)
- Integration with Other Skills (preserve)
- References section (point to all 8 reference files)
- Best Practices (10 items, emphasize surface ordering and flux grouping)

**Step 9: Fix YAML Frontmatter**

Remove:
- category: E
- auto_activate: true
- activation_keywords: [...]
- related_skills: [...]
- output_formats: [...]

Set:
- version: "2.0.0"
- description: Third-person, trigger-specific
- Keep: name, dependencies

**Step 10: Validate Quality (25-item checklist)**

**Step 11: Test Skill Invocation**

## TOKEN TRACKING

**Session 15 actual usage:**
- Startup: 0 tokens (skipped per user request)
- AGR-1 MCNP model reading (8 parallel chunks): ~25k tokens
- AGR-1-KEY-INFO.md reading: ~2k tokens
- AGR-Literature-MCNP-BUILD-REVIEW.md writing: ~10k tokens (direct write)
- Current SKILL.md reading: ~5k tokens
- 4 reference files writing: ~20k tokens (direct write)
- CLAUDE-SESSION-REQUIREMENTS.md reading: ~5k tokens
- Status updates and planning: ~3k tokens
- **Total used:** ~70k tokens

**Session 15 remaining:** ~130k tokens (66.5k shown in last system message)

**Optimization applied:**
- ✅ Parallel reads (8 MCNP chunks + AGR-1-KEY-INFO in single message)
- ✅ Direct file creation (no content drafting in responses)
- ✅ Structured extraction (5 reference files created)
- ✅ User directive: Comprehensive references over shortened versions

**Next session (16) budget estimate:**
- Startup documents: ~10k tokens (shorter startup, already familiar)
- Create 4 remaining reference files: ~15k tokens (comprehensive, direct write)
- Create 10 example files + descriptions: ~25k tokens (MCNP format verification required)
- Create 6 scripts + README: ~15k tokens (direct write)
- Create 4 templates: ~8k tokens (MCNP format verification required)
- Streamline SKILL.md: ~10k tokens
- Fix YAML: ~1k tokens
- Quality validation: ~5k tokens
- Testing: ~3k tokens
- Status update: ~3k tokens
- **Estimated total:** ~95k tokens
- **Buffer:** ~20k for overhead, iterations
- **Total need:** ~115k tokens (well within 200k budget)

---

## CRITICAL CONTEXT FOR SESSION 16

### Current State Summary

**mcnp-lattice-builder revamp status: ~40% complete**

**Completed (Session 15):**
- ✅ Gap analysis between current SKILL.md and comprehensive documentation
- ✅ 4 of 8 reference files created (16,100 words total)
- ✅ AGR-1 literature-to-MCNP analysis document (16,000 words)
- ✅ Todo list established with clear priorities

**Critical context documents created:**
- AGR-Literature-MCNP-BUILD-REVIEW.md (literature → MCNP translation example)
- references/lattice_fundamentals.md (U/LAT/FILL core concepts)
- references/reactor_to_mcnp_workflow.md (9-step translation process)
- references/flux_based_grouping_strategies.md (15.6% vs 4.3% error lessons)
- references/htgr_double_heterogeneity.md (TRISO modeling in 4-level hierarchy)

**Remaining work: Steps 5-11 (60% remaining)**
- 4 more reference files
- 10 example MCNP files
- 6 Python scripts + README
- 4 templates
- SKILL.md streamline
- YAML fix
- Quality validation
- Testing

### START HERE - Session 16 Instructions

**⚠️ MANDATORY FIRST STEPS:**

1. **Verify working directory:**
   ```bash
   pwd  # Must be c:\Users\dman0\mcnp_projects
   ```

2. **Read TOKEN-OPTIMIZATION-BEST-PRACTICES.md FIRST** (MANDATORY)
   - Apply all 5 techniques throughout session
   - Parallel tool calls for independent operations
   - Direct file creation (no drafting)

3. **Resume from Step 5 (continued):**
   - Create 4 remaining reference files (see lines 1050-1081 above for specifications)
   - Extract content from current SKILL.md lines indicated
   - Comprehensive content (~1,000-1,800 words each)

4. **BEFORE any MCNP file creation (Step 6):**
   ```
   MANDATORY: Invoke mcnp-input-builder skill
   MANDATORY: Read at least 2 examples from mcnp-input-builder/assets/
   MANDATORY: Verify three-block structure (Title → Cells → blank → Surfaces → blank → Data)
   MANDATORY: Exactly 2 blank lines total in complete inputs, 0 in snippets
   ```

5. **Step 6: Create 10 example files**
   - Create directory: `.claude/skills/mcnp-lattice-builder/assets/example_inputs/`
   - Follow specifications in lines 1083-1103 above
   - Examples 7-10 are CRITICAL for reactor modeling capability
   - Each example needs description/explanation .md file

6. **Step 7: Create 6 Python scripts + README**
   - Create directory: `.claude/skills/mcnp-lattice-builder/scripts/`
   - Follow specifications in lines 1105-1144 above
   - Functional, tested code
   - Comprehensive README with usage examples

7. **Step 8: Streamline SKILL.md**
   - Target: <3,000 words
   - Follow structure in lines 1146-1169 above
   - ADD: Reactor modeling use cases (CRITICAL)
   - ADD: HTGR TRISO use case (CRITICAL)
   - EMPHASIZE: Surface ordering and flux-based grouping
   - Preserve: Excellent decision tree, troubleshooting section

8. **Step 9: Fix YAML** (lines 1171-1183)

9. **Step 10: Run 25-item quality checklist** (CLAUDE-SESSION-REQUIREMENTS.md lines 603-641)

10. **Step 11: Test skill invocation**

### Key Insights to Preserve

**From AGR-1 analysis:**
- 4-level hierarchy: TRISO → Particle lattice → Compact → Stack
- 72 independent universes for flux-based grouping
- Surface ordering CRITICAL for lattice indexing
- Volume specification: per-instance, not total
- Fortran ordering: i-index varies fastest

**From verification exercise:**
- Whole-core grouping: 15.6% error (UNACCEPTABLE)
- Assembly-level grouping: 4.3% error (ACCEPTABLE)
- **Rule: Group by flux zone, not geometric convenience**

**CRITICAL gaps addressed:**
- Reactor modeling workflow (NEW capability)
- Flux-based grouping (Essential for accuracy)
- HTGR/TRISO systems (Major reactor type)
- Surface ordering emphasis (Most common error)

### Files and Locations

**Reference materials available:**
- `c:\Users\dman0\mcnp_projects\skill-revamp\AGR-Literature-MCNP-BUILD-REVIEW.md`
- `c:\Users\dman0\mcnp_projects\skill-revamp\AGR-1-KEY-INFO.md`
- `c:\Users\dman0\mcnp_projects\skill-revamp\LATTICE-INFO-SUMMARY.md`
- Current SKILL.md: `c:\Users\dman0\mcnp_projects\.claude\skills\mcnp-lattice-builder\SKILL.md`
- References directory (4 files): `c:\Users\dman0\mcnp_projects\.claude\skills\mcnp-lattice-builder\references\`

**AGR-1 MCNP model for examples:**
- Full model: `c:\Users\dman0\mcnp_projects\example_files\reactor-model_examples\htgr-model-burnup-and-doserates\agr-1\mcnp\sdr-agr.i`

**Completed skills for reference:**
- mcnp-input-builder (MANDATORY reference before MCNP files)
- mcnp-geometry-builder
- mcnp-material-builder

### Success Criteria

**mcnp-lattice-builder is complete when:**
- [ ] 8 reference files in references/ directory
- [ ] 10 example files in assets/example_inputs/ (with descriptions)
- [ ] 6 scripts + README in scripts/ directory
- [ ] SKILL.md <3,000 words with reactor modeling content
- [ ] YAML frontmatter compliant (no non-standard fields)
- [ ] All 25 quality checklist items pass
- [ ] Skill invokes successfully
- [ ] Can translate reactor literature specs to MCNP lattice model

**Integration test readiness:**
- Skill can guide building AGR-1-style model from literature alone
- Flux-based grouping strategy clear and implementable
- Surface ordering verification explicit
- TRISO particle modeling comprehensive

### Token Budget

**Estimated Session 16 needs: ~115k tokens**
- Well within 200k budget
- Use parallel tool calls aggressively
- Direct file creation (no drafting)
- Comprehensive content over multiple short revisions

### What NOT to Do

❌ Don't create short/incomplete reference files
❌ Don't skip MCNP format verification before examples
❌ Don't omit reactor modeling use cases
❌ Don't forget flux-based grouping emphasis
❌ Don't skip quality checklist
❌ Don't write to wrong directory (verify pwd first!)

### Expected Completion

**After Session 16:**
- mcnp-lattice-builder: 100% complete ✅
- Phase 1 progress: 5/16 skills (31.25%)
- Ready to move to next Phase 1 skill

---

**Session 15 completed artifacts:**
- ✅ AGR-Literature-MCNP-BUILD-REVIEW.md (16,000 words)
- ✅ 4 comprehensive reference files (16,100 words total)
- ✅ Gap analysis and detailed plan
- ✅ Todo list with clear priorities

---

## INTEGRATION TESTING CONSIDERATION

**Ultimate Goal:** Claude must be able to build full reactor models from design specifications alone

**mcnp-lattice-builder's Role:**
- Core → Assembly → Fuel channel → TRISO hierarchy
- Flux-based grouping for independent depletion
- Translation from literature specs to MCNP syntax
- Verification of complex nested structures

**Integration Test Scenario (Future):**
1. Provide Claude with reactor design paper (e.g., HTGR specifications)
2. Claude invokes mcnp-lattice-builder skill
3. Claude creates full MCNP model with proper lattice hierarchy
4. Model is geometrically correct, runs without errors
5. Results match expected physics (k-eff, flux distributions)

**Success Criteria:**
- ✅ Proper universe hierarchy (3+ levels)
- ✅ Correct surface ordering for lattice indices
- ✅ Flux-based grouping implemented
- ✅ Volume specifications correct for repeated structures
- ✅ Model runs and produces reasonable results
- ✅ Geometry plots show correct structure

**If mcnp-lattice-builder fails integration test:**
- Entire skill suite considered incomplete
- Revamp effort not meeting ultimate objective
- Additional skill revisions required

**Therefore:** mcnp-lattice-builder MUST be comprehensive, robust, and thoroughly tested

---

**END OF PHASE-1-PROJECT-STATUS-PART-5.MD**

**Next Session (16):** Execute mcnp-lattice-builder revamp Steps 1-11
