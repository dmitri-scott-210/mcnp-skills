# Current MCNP Skills Assessment

**Date:** 2025-11-02
**Skills Analyzed:** 36 total (31 required + 5 bonus)
**Purpose:** Document current state and gaps vs Anthropic standards

---

## Executive Summary

All 36 MCNP skills are well-structured with good content but **universally lack** the progressive disclosure structure required by Anthropic standards:
- ❌ No references/ subdirectories
- ❌ No scripts/ subdirectories
- ❌ No assets/ subdirectories
- ❌ Example files from example_files/ never incorporated
- ⚠️ SKILL.md files borderline too long (1,000-1,200 lines each)

**What's working well:**
- ✅ Decision trees present
- ✅ Integration sections
- ✅ Good use cases
- ✅ Clear "When to Use" sections

---

## Detailed Analysis

**See REVAMP-PROJECT-STATUS.md "COMPREHENSIVE RESEARCH FINDINGS Section 2" for:**
- Individual skill reviews (mcnp-input-builder, mcnp-geometry-builder, mcnp-output-parser, mcnp-variance-reducer)
- Common quality patterns across all 36 skills
- Category distribution
- Specific missing elements per skill type

---

## Universal Gaps (All 36 Skills)

### 1. No references/ Subdirectories
**Issue:** All detailed content embedded in SKILL.md
**Impact:** SKILL.md files too long, hard to navigate
**Examples of content that should be in references/:**
- Card specifications (05_02 Cell Cards, 05_03 Surface Cards, etc.)
- Surface type details (30+ geometric surfaces)
- Error catalogs (all fatal/warning patterns)
- Detailed examples (10-15 per skill)
- Theory/derivations

### 2. No scripts/ Subdirectories
**Issue:** Python modules mentioned but not bundled
**Examples:**
- mcnp-output-parser mentions "mcnp_output_parser.py" but file not included
- mcnp-input-validator mentions "validator.py" but not bundled
- All utilities skills mention automation but scripts missing

**Impact:** Users can't execute automation, reduces skill value

### 3. No assets/ Subdirectories
**Issue:** No templates, no examples from example_files/
**Critical Gap:** 1,107 example MCNP files available in example_files/ but ZERO incorporated
**Impact:**
- No starting templates for users
- Miss opportunity to show real-world examples
- Reduces practical utility

### 4. YAML Frontmatter Inconsistencies
**Issues:**
- Some use `activation_keywords:` (non-standard)
- Some use `category:` (non-standard)
- Variable description quality (some too vague)

**Example:**
```yaml
---
name: mcnp-input-builder
description: Build MCNP input files  # Too vague
activation_keywords:  # Non-standard field
  - input
  - build
category: A  # Non-standard field
---
```

**Should be:**
```yaml
---
name: mcnp-input-builder
description: "Use when creating new MCNP input files with proper three-block structure, cell/surface cards, and material specifications"
version: "2.0.0"
---
```

---

## Category-Specific Issues

### Category A & B (Input Building/Editing - 16 skills)
**Strengths:**
- Comprehensive card coverage
- Good Boolean logic explanations
- Clear geometry examples

**Gaps:**
- Card specifications should be in references/card_specs.md
- Surface types should be in references/surface_types.md
- Macrobody details should be in references/macrobodies.md
- Missing templates in assets/
- Missing examples from basic_examples/ and reactor-model_examples/

### Category D (Output Analysis - 6 skills)
**Strengths:**
- Multiple file format support
- Good parsing examples
- Python integration shown

**Gaps:**
- File format specs should be in references/file_formats.md
- HDF5 structure details should be in references/hdf5_structure.md
- Python modules should be in scripts/
- Missing output examples in assets/

### Category E (Advanced - 5 skills)
**Strengths:**
- Comprehensive VR coverage
- Good theory explanations
- Practical examples

**Gaps:**
- VR theory should be in references/vr_theory.md
- Statistical tests should be in references/statistical_tests.md
- WWG algorithms should be in references/wwg_algorithms.md
- Missing VR examples from variance-reduction_examples/

### Category F (Utilities - 6 skills)
**Strengths:**
- Clear conversion tables
- Good lookup information

**Gaps:**
- Complete databases should be in references/
- Automation should be in scripts/
- Missing isotope database, conversion tables as assets/

---

## Recommended Extraction Strategy

For typical 1,100-line SKILL.md:

**Extract ~500 lines to references/:**
- Detailed specifications
- Theory sections
- Large error catalogs
- Comprehensive examples (keep 3-5 in SKILL.md, rest in references/)

**Add to assets/ (~5-10 files):**
- Template MCNP inputs (basic, intermediate, advanced)
- 5-10 validated examples from example_files/
- Description files for each example

**Bundle in scripts/ (if applicable):**
- Python modules currently only mentioned
- Validation tools
- Automation helpers

**Result:** SKILL.md streamlined to ~500-600 lines (~2,500-3,000 words)

---

## Skills Priority for Revamp

**High Priority (Most Used):**
1. mcnp-input-builder - Foundational
2. mcnp-geometry-builder - Core functionality
3. mcnp-material-builder - Core functionality
4. mcnp-output-parser - Frequently used
5. mcnp-tally-builder - Essential
6. mcnp-variance-reducer - High complexity

**Medium Priority:**
- All remaining Category A/B skills
- Category D skills

**Lower Priority:**
- Category F utilities
- Category C specialized

---

##Conclusion

Current MCNP skills have **good content quality** but **poor structure** compared to Anthropic standards. All 36 skills need:
1. Content extraction to references/
2. Script bundling in scripts/
3. Example incorporation in assets/
4. SKILL.md streamlining to <3k words
5. YAML frontmatter standardization

**Estimated effort:** 10k tokens per skill × 36 skills = 360k tokens (processing only)

**With batched reading:** 430k total tokens (vs 2,400k sequential)

See optimization-strategy.md for token savings analysis.
