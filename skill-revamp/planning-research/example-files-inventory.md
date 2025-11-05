# MCNP Example Files Inventory

**Location:** `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\example_files\`
**Total Files:** 1,107 MCNP input files (.i and .txt formats)
**Critical Gap:** ZERO examples incorporated in current skills

---

## Directory Structure

```
example_files/
├── basic_examples/ (~100 files)
├── intermediate_examples/
├── criticality_examples/
├── reactor-model_examples/ ⭐ MOST COMPREHENSIVE
│   └── htgr-model-burnup-and-doserates/
│       ├── agr-1/mcnp/ (14+ production reactor files)
│       ├── verification/
│       └── repeated_structures/
├── rad-protection_examples/
├── safeguards_examples/
├── unstructured-mesh_examples/
├── variance-reduction_examples/
└── MCNP6_VnV/
```

---

## Category Descriptions

### 1. basic_examples/ (~100 files)
**Format:** .txt files
**Complexity:** Simple, single-concept demonstrations
**Examples:**
- shield.txt - Simple shielding
- tal01.txt - Basic tally setup
- src1.txt - Point source
- puc1.txt - Plutonium criticality

**Use for Skills:**
- Category A/B (input building) - Templates
- Category C (validation) - Test cases
- Learning and quick validation

**Recommendation:** Extract 10-15 files for assets/templates/

### 2. intermediate_examples/
**Complexity:** Multi-component problems
**Use for:** Skills requiring moderate examples

### 3. criticality_examples/
**Focus:** KCODE problems, k-effective calculations
**Use for Skills:**
- mcnp-criticality-analyzer
- mcnp-source-builder (KCODE)
- mcnp-burnup-builder

### 4. reactor-model_examples/ ⭐ **HIGHEST VALUE**
**Location:** `htgr-model-burnup-and-doserates/`
**Source:** Research article at https://nstopenresearch.org/articles/1-20/v2
**Complexity:** Production-quality, real-world reactor modeling

**Subdirectories:**

**agr-1/mcnp/ (14+ files):**
- bench_*.i files - Benchmark calculations
- Real HTGR (High-Temperature Gas-cooled Reactor) models
- Complex geometries with repeated structures
- Burnup calculations
- Dose rate analysis

**verification/:**
- Test cases with reference solutions
- Validation examples

**repeated_structures/:**
- Lattice examples
- Universe/fill demonstrations
- Hexagonal lattice patterns

**Use for Skills:**
- mcnp-lattice-builder - Real lattice examples
- mcnp-geometry-builder - Complex geometry
- mcnp-burnup-builder - Burnup workflows
- mcnp-variance-reducer - Production VR setups
- mcnp-mesh-builder - Realistic mesh tallies
- **ALL Category A/B skills** - Show real-world complexity

**Recommendation:** HIGHEST PRIORITY for incorporation
- Extract 5-10 representative examples
- Include in assets/ with detailed descriptions
- Reference in multiple skills

### 5. rad-protection_examples/
**Focus:** Shielding, dose calculations
**Use for Skills:**
- mcnp-tally-builder (dose tallies)
- mcnp-variance-reducer (deep penetration)
- mcnp-physics-builder (photon/electron transport)

### 6. safeguards_examples/
**Focus:** Specialized applications
**Use for:** Advanced users, specialized skills

### 7. unstructured-mesh_examples/
**Focus:** FMESH with XDMF output, HDF5 format
**Use for Skills:**
- mcnp-mesh-builder
- mcnp-output-parser (mesh output)
- mcnp-plotter (mesh visualization)

**Recommendation:** Extract all examples for Category D skills

### 8. variance-reduction_examples/
**Focus:** WWG, importance sampling, DXTRAN
**Use for Skills:**
- mcnp-variance-reducer
- mcnp-ww-optimizer
- mcnp-statistics-checker

**Recommendation:** Extract all examples for Category E skills

### 9. MCNP6_VnV/
**Focus:** Verification and validation cases
**Use for:** Testing, benchmarking, validation

---

## Strategic Incorporation Plan

### Phase 1: Category A & B (16 skills)
**Extract from:**
- basic_examples/ (10 files) - Simple templates
- reactor-model_examples/agr-1/mcnp/ (3-5 files) - Complex examples
- reactor-model_examples/repeated_structures/ (2-3 files) - Lattice demos

**Per skill:** 5-10 examples in assets/example_inputs/
**Total:** ~80-160 example files

### Phase 2: Category D (6 skills)
**Extract from:**
- unstructured-mesh_examples/ (all files)
- reactor-model_examples/ (output files if available)

**Per skill:** 3-7 examples

### Phase 3: Category E (4 skills)
**Extract from:**
- variance-reduction_examples/ (all files)
- reactor-model_examples/agr-1/mcnp/ (VR setups)

**Per skill:** 5-8 examples

### Phase 4: Category F (6 skills)
**Extract from:**
- basic_examples/ (for unit conversion demonstrations)
- Mixed sources for utility demos

**Per skill:** 2-5 examples

### Phase 5: Category C & Specialized
**Extract from:**
- criticality_examples/ (for criticality-analyzer)
- Error examples (if available)

**Per skill:** Variable

---

## Example File Requirements

For each example added to assets/:
1. **Source file:** example_name.i (MCNP input)
2. **Description file:** example_name_description.txt containing:
   - Purpose/what it demonstrates
   - Key features (geometry, materials, tallies, VR techniques)
   - Expected results (k-eff, tally values, etc.)
   - Complexity level (basic/intermediate/advanced)
   - Related skills
   - Source (which directory)

**Example description format:**
```
EXAMPLE: Sphere Shielding Problem
SOURCE: basic_examples/shield.txt
COMPLEXITY: Basic
DEMONSTRATES:
- Simple spherical geometry (SO surface)
- Single material (water)
- Point neutron source at origin
- Surface current tally (F1)
EXPECTED RESULTS:
- Tally 1: Surface current ~0.5 n/cm²/src neutron
KEY FEATURES:
- Boolean complement for void region
- IMP card for importance
RELATED SKILLS:
- mcnp-geometry-builder
- mcnp-material-builder
- mcnp-source-builder
- mcnp-tally-builder
```

---

## Validation Strategy

Before incorporating examples:
1. **Verify syntax:** Each .i file must be valid MCNP input
2. **Test execution:** Run examples to ensure no fatal errors
3. **Document results:** Capture expected output
4. **Size check:** Files should be reasonable size (<500 lines preferred)
5. **Relevance:** Example must demonstrate skill-specific concepts

---

## Priority Examples

**MUST INCLUDE (Top 20):**

From basic_examples/:
1. shield.txt - Sphere shielding
2. tal01.txt - Basic tally
3. src1.txt - Point source
4. puc1.txt - Criticality
5. var01.txt - Simple VR
6. [5 more from basic]

From reactor-model_examples/:
11. bench_001.i - Full reactor model
12. bench_002.i - Lattice structure
13. [specific repeated_structures example]
14. [specific verification example]
15. [3 more production examples]

From variance-reduction_examples/:
18. [WWG example]
19. [Importance sampling example]
20. [DXTRAN example]

**Secondary (Add as tokens allow):**
- All unstructured-mesh examples
- All criticality examples
- Selected rad-protection examples

---

## Token Cost Estimate

**Per example incorporation:**
- Copy file to assets/: minimal tokens
- Write description file: ~0.5k tokens
- Reference in SKILL.md: minimal

**Total for 36 skills × 5-10 examples each:**
- ~200 example files
- ~100k tokens for descriptions and integration

**Benefit:** Massive improvement in skill practical utility

---

## Conclusion

The example_files/ directory contains a **treasure trove** of 1,107 validated MCNP examples that were **completely unused** in original skill development. Incorporating these examples is:

1. **CRITICAL** for skill quality
2. **HIGH VALUE** for users (real-world examples)
3. **REQUIRED** by Anthropic standards (assets/ subdirectory)
4. **EFFICIENT** token-wise (~0.5k per example)

**Priority Order:**
1. reactor-model_examples/ - Production quality, must include
2. variance-reduction_examples/ - For Category E skills
3. unstructured-mesh_examples/ - For Category D skills
4. basic_examples/ - For templates and learning

**Next Steps:** During each skill revamp, systematically incorporate 5-10 relevant examples from appropriate directories.
