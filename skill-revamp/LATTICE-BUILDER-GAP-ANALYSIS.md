# MCNP-LATTICE-BUILDER GAP ANALYSIS

**Current SKILL.md:** 804 lines, ~5,800 words
**Target:** <3,000 words (preferred) or <5,000 words (maximum)
**Date:** 2025-11-04 (Session 15)

---

## YAML FRONTMATTER ISSUES

### Non-Standard Fields (Remove)
- ❌ `category: E` → Remove (non-Anthropic standard)
- ❌ `auto_activate: true` → Remove (non-Anthropic standard)
- ❌ `activation_keywords:` → Remove (non-Anthropic standard)
- ❌ `related_skills:` → Remove (non-Anthropic standard)
- ❌ `output_formats:` → Remove (non-Anthropic standard)

### Required Updates
- ❌ `version: 1.0.0` → Update to `version: "2.0.0"`
- ✅ `name:` present and correct
- ⚠️ `description:` needs improvement - not sufficiently trigger-specific
  - Current: "Build lattice and repeated structure geometries using U/LAT/FILL cards for fuel assemblies, detector arrays, and complex periodic geometries"
  - Better: "Constructs MCNP repeated structures (U/LAT/FILL) for reactor cores, fuel assemblies, and complex geometries with hierarchical organization when modeling thousands of repeated elements."

---

## CONTENT COVERAGE GAPS

### 1. Missing Reactor Modeling Workflow ⚠️ CRITICAL

**What's Missing:**
- No guidance on translating reactor design specs to MCNP lattices
- No discussion of information typically available vs missing in literature
- No workflow for going from paper → MCNP model
- No discussion of assumptions needed when specs incomplete

**Why Critical:**
- User stated ultimate goal: Build full reactor models from design specs
- Without this workflow, skill cannot support integration testing
- AGR-1 example shows this is realistic and achievable

**Where to Add:**
- Extract to `references/reactor_to_mcnp_workflow.md` (~2,000 words)
- Summarize in SKILL.md Use Case 4
- Include AGR-1 as example of successful translation

### 2. Missing Flux-Based Grouping Strategy ⚠️ CRITICAL

**What's Missing:**
- No discussion of why whole-core single universe fails
- No quantitative error data (15.6% vs 4.3% from verification exercise)
- No guidance on determining appropriate group size
- No discussion of flux spatial variation effects on depletion

**Current Content:**
- Brief mention in nested lattices: "Universe 20 (assembly + shroud)" shows grouping
- No explicit discussion of flux-based rationale
- No error magnitudes or verification approach

**Why Critical:**
- Wrong grouping → 15%+ errors in activation/burnup calculations
- Critical for HTGR modeling (millions of TRISO particles)
- Directly impacts decommissioning dose rate accuracy

**Where to Add:**
- Extract to `references/flux_based_grouping_strategies.md` (~1,200 words)
- Add to SKILL.md Best Practices #2 (currently missing)
- Include in Use Case 3 (HTGR modeling)

### 3. Missing HTGR Double Heterogeneity ⚠️ CRITICAL

**What's Missing:**
- No discussion of TRISO particle structure (5 layers)
- No explanation of double heterogeneity concept
- No guidance on regular lattice vs stochastic (URAN card)
- No discussion of computational necessity for regular lattices

**Current Content:**
- Nested lattices example shows hierarchy but not TRISO-specific
- No HTGR fuel particle details
- No discussion of millions-of-particles challenge

**Why Critical:**
- HTGR is major advanced reactor type
- TRISO modeling is complex and requires special approaches
- AGR-1 example demonstrates successful methodology

**Where to Add:**
- Extract to `references/htgr_double_heterogeneity.md` (~1,500 words)
- Add Use Case 3: "HTGR TRISO Particle Lattice" to SKILL.md
- Include example_07 from AGR-1 structure

### 4. Missing Surface Ordering Emphasis ⚠️ HIGH

**What's Missing:**
- No explicit section on surface ordering defining indices
- Brief mention but not emphasized as critical
- No verification approach using geometry plotter with indices
- No troubleshooting for index mismatch

**Current Content:**
- Decision tree mentions "Rectangular pins/boxes → LAT=1"
- Implicit in examples but not explicitly taught
- No discussion of surface 1→[1,0,0], 2→[-1,0,0] convention

**Why Important:**
- Surface ordering errors → wrong lattice layout
- Common source of errors for beginners
- Essential for complex multi-level lattices

**Where to Add:**
- Extract detailed surface ordering to `references/lattice_fundamentals.md`
- Add to SKILL.md Best Practice #1
- Add Use Case 5: "Debugging Lattice Index Mismatch"
- Include in Quick Reference table

### 5. Missing Volume Specification Emphasis ⚠️ HIGH

**What's Missing:**
- Only brief mention in "Volume Normalization for Lattice Cells"
- No discussion of total volume across ALL instances requirement
- No guidance on calculating volumes for repeated structures
- No examples showing volume specification

**Current Content:**
- Line 529: "SD4 0.50265 $ π × 0.4² = 0.50265 cm³"
- Comment shows single pin volume, not total
- No explicit statement about ALL instances requirement

**Why Important:**
- Wrong volumes → incorrect source intensities
- Critical for activation/burnup calculations
- Common source of errors

**Where to Add:**
- Add to `references/lattice_fundamentals.md`
- Emphasize in SKILL.md Best Practice #4
- Add to SKILL.md Use Cases with volume calculations
- Create `scripts/lattice_volume_checker.py`

### 6. Missing Verification Strategies ⚠️ MEDIUM

**What's Missing:**
- No systematic verification approach
- No guidance on using geometry plotter effectively
- No discussion of simplified reference cases
- No validation methodology

**Current Content:**
- Brief mention: "Test single element"
- No comprehensive verification workflow

**Where to Add:**
- Extract to `references/lattice_verification_methods.md` (~1,000 words)
- Add to Best Practices
- Include verification in Use Cases

### 7. Missing Multi-Level Hierarchy Examples ⚠️ MEDIUM

**Current Content:**
- Lines 382-437: 3-level hierarchy (pin → assembly → core)
- Good structure but only one example
- No HTGR-style 4-level (TRISO → compact → assembly → core)

**What's Needed:**
- AGR-1-style example (capsule → compact → TRISO)
- More discussion of universe hierarchy design
- Guidance on determining hierarchy levels

**Where to Add:**
- Keep current 3-level in SKILL.md
- Add AGR-1 4-level to example_09
- Add hierarchy diagram to `references/universe_hierarchy_guide.md`

### 8. Missing Transformation Details ⚠️ MEDIUM

**Current Content:**
- Lines 439-489: Basic transformations with FILL
- Brief examples only

**What's Missing:**
- Detailed TR card syntax
- Rotation matrix entries explanation
- Displacement vector origin interpretation
- m parameter discussion

**Where to Add:**
- Extract to `references/transformations_for_lattices.md` (~1,800 words)
- Keep simple examples in SKILL.md
- Add transformation scripts for calculation

### 9. Missing Common Lattice-Specific Errors ⚠️ LOW

**Current Content:**
- Lines 660-749: Good troubleshooting section (6 issues)
- Specific to lattice problems

**What Could Improve:**
- More systematic error catalog
- Error codes and messages
- Solutions with examples

**Where to Add:**
- Extract to `references/common_lattice_errors.md` (~1,500 words)
- Keep top 3-5 in SKILL.md Troubleshooting
- Reference detailed catalog

---

## STRUCTURAL ISSUES

### 1. Word Count Too High

**Current:** ~5,800 words
**Target:** <3,000 (preferred) or <5,000 (maximum)
**Reduction Needed:** 800-2,800 words

**Content to Extract:**
- Detailed card specifications → `references/lattice_fundamentals.md`
- All transformation details → `references/transformations_for_lattices.md`
- Extended troubleshooting → `references/common_lattice_errors.md`
- Detailed theory → `references/universe_hierarchy_guide.md`

**Content to Keep in SKILL.md:**
- Overview (3 paragraphs)
- When to Use (8-10 bullets)
- Decision Tree (current is good)
- Quick Reference table (needs expansion)
- 5 Use Cases (condensed, ~500 words each)
- Integration section (condense)
- Best Practices (10 items, current has 11)
- References section (new, points to extracted content)

### 2. Missing Progressive Disclosure Structure

**Current:** Monolithic SKILL.md with all content
**Needed:** SKILL.md + references/ + scripts/ + assets/

**To Create:**
- `references/` directory (8 files, ~13,000 words total)
- `scripts/` directory (7 files + README)
- `assets/templates/` (5 templates)
- `assets/example_inputs/` (10 examples with descriptions)

### 3. Quick Reference Table Incomplete

**Current:** No Quick Reference table in SKILL.md

**Needed:**
```markdown
| Concept | Card | Example | Notes |
|---------|------|---------|-------|
| Universe | U=n | U=1 | Assign cell to universe |
| Lattice type | LAT=n | LAT=1 | 1=hexahedral, 2=hex prism |
| Fill single | FILL=n | FILL=2 | All elements = universe 2 |
| Fill array | FILL=i1:i2... | (see table) | i varies fastest |
| Transform | TRCL=n | TRCL=5 | Reference TR5 card |
| Surface order LAT=1 | Cell card | (see table) | Sfc 1→[1,0,0], 2→[-1,0,0], ... |
| Surface order LAT=2 | Cell card | (see table) | 8 surfaces for hex prism |
```

---

## EXAMPLES ASSESSMENT

### Current Examples (in SKILL.md)

**Use Case 1: PWR 17×17 Fuel Assembly (lines 538-607)**
- ✅ Comprehensive (70 lines)
- ✅ Shows indexed FILL with guide tubes
- ✅ Real-world relevant
- ⚠️ Could be condensed for SKILL.md, move details to example file

**Use Case 2: VVER Hexagonal Assembly (lines 609-655)**
- ✅ Good hexagonal example (47 lines)
- ✅ Shows LAT=2 usage
- ⚠️ Could be condensed, move details to example file

**Use Case 3: Nested Lattice Reference (line 657)**
- ⚠️ Only reference to earlier section
- ❌ Should be standalone use case

### Needed Examples (Not Present)

**Missing Use Case: Translating Reactor Specs to MCNP**
- Critical for reactor modeling workflow
- Should show literature → MCNP process
- Include assumptions and verification

**Missing Use Case: HTGR TRISO Lattice**
- Essential for advanced reactor modeling
- Shows double heterogeneity handling
- Demonstrates flux-based grouping

**Missing Use Case: Debugging Lattice Issues**
- Practical troubleshooting walkthrough
- Surface ordering verification
- Index mismatch diagnosis

**Missing Example Files:**
- Simple examples (1-3): Basic lattices for learning
- Intermediate examples (4-6): Fuel assemblies with variations
- Advanced examples (7-10): Reactor cores, HTGR, AGR-1

---

## BEST PRACTICES ASSESSMENT

### Current Best Practices (11 items)

**Good:**
1. Universe numbering scheme ✅
2. Always bound universes ✅
3. Verify pitch ✅
4. Test single element ✅
5. Use comments ✅
6. Volume cards ✅
7. Nested lattices diagram ✅
8. Hexagonal orientation ✅
9. Transformations carefully ✅
10. Lost particles background cells ✅
11. Programmatic generation reference ✅

**Missing Critical Practices:**
- ❌ Surface ordering verification (most important!)
- ❌ Flux-based grouping for reactor models
- ❌ Geometry plotter with index labels
- ❌ Simplified reference case validation

**Recommended Updates:**
1. **Surface ordering verification** (move to #1, most important)
2. **Flux-based grouping** (add as #2, critical for reactors)
3. Universe numbering scheme (keep)
4. Always bound universes (keep)
5. Test incrementally (expand current #4)
6. Volume specification (emphasize ALL instances)
7. Geometry plotting (expand)
8. Document hierarchy (expand current #5)
9. FILL array ordering (add)
10. Verification with reference case (add)

---

## INTEGRATION SECTION ASSESSMENT

### Current Integration (lines 751-780)

**Covered:**
- mcnp-burnup-builder ✅
- mcnp-mesh-builder ✅
- mcnp-geometry-builder ✅

**Good Points:**
- Shows skill connections
- Practical examples

**Missing:**
- mcnp-input-validator (for U/FILL verification)
- mcnp-cell-checker (for lattice cell validation)
- mcnp-source-builder (source in lattices)
- mcnp-tally-builder (tallies on lattice elements)
- Complete workflow example

**Needed:**
```markdown
**Typical Workflow:**
1. mcnp-geometry-builder → Create base element
2. mcnp-material-builder → Define materials
3. mcnp-lattice-builder (THIS SKILL) → Organize lattices
4. mcnp-source-builder → Define source
5. mcnp-tally-builder → Set up tallies
6. mcnp-input-validator → Verify complete input
```

---

## WRITING STYLE ISSUES

### Second-Person Usage (Should Be Imperative/Infinitive)

**Examples Found:**
- Line 495: "Want flux in one specific pin" → Should be "To tally flux in specific pin"
- General tone could be more objective

**Fix:**
- Review all text for "you/your" language
- Convert to imperative form: "To accomplish X, do Y"
- Maintain technical, instructional tone

---

## SCRIPTS AND AUTOMATION

### Current State
- Line 795: References `mcnp_lattice_builder.py`
- ❌ No scripts/ directory exists
- ❌ Script is mentioned but not bundled

### Needed Scripts
1. `lattice_index_calculator.py` - Calculate indices from surface order
2. `fill_array_generator.py` - Generate FILL syntax
3. `universe_hierarchy_visualizer.py` - Visualize universe tree
4. `lattice_volume_checker.py` - Verify volume specifications
5. `surface_order_validator.py` - Check surface ordering
6. `reactor_spec_to_lattice.py` - Template from reactor specs
7. `scripts/README.md` - Usage documentation

---

## REFERENCES SECTION

### Current State
- Lines 799-803: Brief references to manual and related skills
- ❌ No references/ directory
- ❌ No detailed reference files

### Needed References Section in SKILL.md
```markdown
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
- Simple examples: See `assets/example_inputs/example_01-03*.i`
- Intermediate examples: See `assets/example_inputs/example_04-06*.i`
- Advanced examples: See `assets/example_inputs/example_07-10*.i`

**Automation Tools:**
- Index calculator: `scripts/lattice_index_calculator.py`
- FILL generator: `scripts/fill_array_generator.py`
- Hierarchy visualizer: `scripts/universe_hierarchy_visualizer.py`
- Volume checker: `scripts/lattice_volume_checker.py`
- Surface validator: `scripts/surface_order_validator.py`
- Reactor template: `scripts/reactor_spec_to_lattice.py`
- Usage guide: `scripts/README.md`
```

---

## PRIORITY RANKINGS

### CRITICAL (Must Fix)
1. ✅ YAML frontmatter (remove non-standard fields)
2. ✅ Add reactor modeling workflow (references/ + Use Case)
3. ✅ Add flux-based grouping strategy (references/ + Best Practice)
4. ✅ Add HTGR double heterogeneity (references/ + Use Case)
5. ✅ Surface ordering emphasis (Best Practice #1)
6. ✅ Create progressive disclosure structure (references/, scripts/, assets/)

### HIGH (Should Fix)
7. ✅ Volume specification emphasis (Best Practice, Use Cases)
8. ✅ Verification strategies (references/ + Best Practice)
9. ✅ Expand Quick Reference table
10. ✅ Streamline SKILL.md to <5k words
11. ✅ Create 10 example files with descriptions
12. ✅ Create 7 scripts + README

### MEDIUM (Good to Fix)
13. ✅ Add more multi-level hierarchy examples
14. ✅ Expand transformation details in references/
15. ✅ Improve Integration section with complete workflow
16. ✅ Create 5 template files
17. ✅ Fix second-person language

### LOW (Nice to Have)
18. ⚠️ Expand troubleshooting catalog in references/
19. ⚠️ Add more hexagonal lattice examples

---

## EXTRACTION PLAN

### Content to Extract FROM Current SKILL.md TO references/

**From "Core Concepts" section (lines 54-111):**
→ `references/lattice_fundamentals.md`
- Universe concept (lines 56-70)
- Lattice concept (lines 72-88)
- Fill concept (lines 90-111)

**From "Rectangular Lattice" section (lines 148-263):**
→ `references/lattice_fundamentals.md`
- Detailed step-by-step construction
- Keep condensed version in SKILL.md Use Case

**From "Hexagonal Lattice" section (lines 265-375):**
→ `references/lattice_fundamentals.md`
- Hexagon orientation details
- Indexing schemes
- Keep condensed version in SKILL.md Use Case

**From "Transformations" section (lines 439-489):**
→ `references/transformations_for_lattices.md`
- All transformation details
- TR card syntax
- Keep simple examples in SKILL.md

**From "Troubleshooting" section (lines 660-749):**
→ `references/common_lattice_errors.md`
- Extract all 6 issues with details
- Keep top 3 in SKILL.md
- Reference full catalog

**From "Best Practices" section (lines 782-796):**
- Reorganize and expand
- Keep 10 items in SKILL.md
- Details in references/

---

## CONTENT TO ADD (Not in Current SKILL.md)

### New Content from LATTICE-INFO-SUMMARY.md
1. Boolean operators and complement shortcuts
2. Lattice indexing surface order schemes
3. Negative universe optimization (with warnings)
4. FILL array syntax conventions (Fortran ordering)
5. Lattice design checklist
6. Computational considerations

### New Content from AGR-1-KEY-INFO.md
1. Reactor modeling workflow (literature → MCNP)
2. Information typically available vs missing
3. Flux-based grouping strategy with quantitative errors
4. TRISO particle structure (5 layers)
5. Multi-level hierarchy (capsule → compact → TRISO)
6. Regular lattice vs stochastic trade-offs
7. Verification exercise results (15.6% vs 4.3%)

---

## SUMMARY STATISTICS

### Content Reduction
- **Current SKILL.md:** ~5,800 words
- **Target SKILL.md:** ~3,000 words (preferred) or ~5,000 (max)
- **Content to Extract:** ~2,800-3,800 words
- **Content to Add (new):** ~1,000 words
- **Net Reduction:** ~1,800-2,800 words

### New Files to Create
- **references/:** 8 files (~13,000 words total)
- **scripts/:** 7 Python files + README (~1,230 lines + docs)
- **assets/templates/:** 5 files (~750 lines)
- **assets/example_inputs/:** 10 files + descriptions (~4,500 words descriptions)

### Quality Improvements
- ✅ Progressive disclosure structure
- ✅ Reactor modeling context
- ✅ Flux-based grouping strategy
- ✅ HTGR double heterogeneity
- ✅ Surface ordering emphasis
- ✅ Verification strategies
- ✅ Volume specification clarity
- ✅ Example progression (basic → advanced)
- ✅ Automation tools bundled

---

**END OF GAP ANALYSIS**

**Next Step:** Create detailed skill revamp plan (Step 4) incorporating all identified gaps.
