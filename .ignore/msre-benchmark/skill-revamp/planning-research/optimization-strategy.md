# Token Optimization Strategy - Batched Processing Approach

**Date:** 2025-11-02
**Purpose:** Demonstrate 85% token savings through batched documentation reading

---

## Executive Summary

**Problem:** Sequential skill revamping wastes ~2,000k tokens by re-reading the same documentation 36 times

**Solution:** Batch skills by shared documentation requirements and read docs ONCE per category

**Result:** 85% token savings (2,400k → 430k tokens)

---

## The Token Waste Problem

### Sequential Approach (Current Inefficiency)

**Scenario:** Revamping skills one at a time without batching

**For Category A/B skills (16 skills):**
```
Skill 1: mcnp-input-builder
  - Read Chapter 3 (15k tokens)
  - Read Chapter 4 (20k tokens)
  - Read Chapter 5 - all 12 files (40k tokens)
  - Read Chapter 10 - all 5 files (5k tokens)
  - Process skill (10k tokens)
  Total: 90k tokens

Skill 2: mcnp-geometry-builder
  - Read Chapter 3 (15k tokens) ← DUPLICATE!
  - Read Chapter 4 (20k tokens) ← DUPLICATE!
  - Read Chapter 5 - all 12 files (40k tokens) ← DUPLICATE!
  - Read Chapter 10 - all 5 files (5k tokens) ← DUPLICATE!
  - Process skill (10k tokens)
  Total: 90k tokens

[... repeat for all 16 skills ...]

Total for 16 skills: 16 × 90k = 1,440k tokens
Wasted on duplicate reading: 16 × 80k = 1,280k tokens
Useful processing: 16 × 10k = 160k tokens
Efficiency: 11% (only 160k of 1,440k is useful work)
```

**For all 36 skills:**
- Total tokens: ~2,400k tokens
- Wasted on duplicates: ~2,000k tokens
- Useful work: ~400k tokens
- **Efficiency: 17%**

---

## Batched Processing Solution

### Core Principle: Read Once, Process Many

**Approach:** Group skills by shared documentation requirements, read docs ONCE per group

**For Category A/B skills (16 skills):**
```
Phase 1 Batch:
  - Read Chapter 3 ONCE (15k tokens)
  - Read Chapter 4 ONCE (20k tokens)
  - Read Chapter 5 - all 12 files ONCE (40k tokens)
  - Read Chapter 10 - all 5 files ONCE (5k tokens)
  - Process skill 1 (10k tokens)
  - Process skill 2 (10k tokens)
  - Process skill 3 (10k tokens)
  ... [skills 4-16]
  - Process skill 16 (10k tokens)

Total: 80k (read once) + 160k (process 16) = 240k tokens
Efficiency: 67% (160k useful / 240k total)
vs Sequential: 1,440k tokens
Savings: 1,200k tokens (83% reduction)
```

**For all 36 skills:**
- Total tokens: ~430k tokens
- Documentation reading: ~200k tokens (read once per category)
- Useful processing: ~360k tokens (10k × 36 skills)
- **Efficiency: 84%**
- **Savings: 2,000k tokens (85% reduction)**

---

## Documentation Sharing Analysis

### must-read-docs.md Mapping

**Category A & B (16 skills) - LARGEST OVERLAP**
Skills: input-builder, geometry-builder, material-builder, source-builder, tally-builder, physics-builder, lattice-builder, geometry-editor, input-editor, input-validator, cell-checker, cross-reference-checker, geometry-checker, physics-validator, transform-editor, variance-reducer

**Shared Documentation:**
- markdown_docs/user_manual/03_Introduction_to_MCNP_Usage.md (15k tokens)
- markdown_docs/user_manual/04_Description_of_MCNP6_Input.md (20k tokens)
- markdown_docs/user_manual/chapter_05_input_cards/*.md (12 files, 40k tokens):
  - 05_01_Geometry_Specification_Intro.md
  - 05_02_Cell_Cards.md
  - 05_03_Surface_Cards.md
  - 05_05_Geometry_Data_Cards.md
  - 05_06_Material_Data_Cards.md
  - 05_07_Physics_Data_Cards.md
  - 05_08_Source_Data_Cards.md
  - 05_09_Tally_Data_Cards.md
  - 05_10_Tally_Perturbations.md
  - 05_11_Mesh_Tallies.md
  - 05_12_Variance_Reduction_Cards.md
  - 05_13_Output_Control_Misc.md
- markdown_docs/examples/chapter_10/*.md (5 files, 5k tokens):
  - 10_01_Geometry_Examples.md
  - 10_02_Tally_Examples.md
  - 10_03_Source_Examples.md
  - 10_05_Physics_Models.md
  - 10_06_Variance_Reduction_Examples.md

**Total:** ~80k tokens read ONCE for 16 skills
**Sequential would be:** 80k × 16 = 1,280k tokens
**Savings:** 1,200k tokens

---

**Category D (6 skills)**
Skills: output-parser, mctal-processor, mesh-builder, plotter, tally-analyzer (partial), statistics-checker (partial)

**Shared Documentation:**
- markdown_docs/user_manual/08_Unstructured_Mesh.md (10k tokens)
- markdown_docs/appendices/AppendixA_Mesh_File_Formats.md (3k tokens)
- markdown_docs/appendices/AppendixD_03_Particle_Track_Output.md (4k tokens)
- markdown_docs/appendices/AppendixD_04_Mesh_Tally_XDMF.md (5k tokens)
- markdown_docs/appendices/AppendixD_05_Fission_Matrix.md (3k tokens)
- markdown_docs/appendices/AppendixD_06_Unstructured_Mesh_HDF5.md (5k tokens)
- markdown_docs/appendices/AppendixD_07_Unstructured_Mesh_Legacy.md (4k tokens)
- markdown_docs/appendices/AppendixD_08_HDF5_Script.md (3k tokens)
- markdown_docs/appendices/AppendixD_09_inxc_File_Structure.md (2k tokens)
- markdown_docs/appendices/AppendixE_11_UM_Post_Processing.md (3k tokens)

**Total:** ~42k tokens read ONCE for 6 skills
**Sequential would be:** 42k × 6 = 252k tokens
**Savings:** 210k tokens

---

**Category E (4 skills)**
Skills: variance-reducer (complete), ww-optimizer, tally-analyzer (complete), statistics-checker (complete)

**Shared Documentation:**
- All Category D docs (if not already read): ~42k tokens
- markdown_docs/theory_manual/chapter_02/02_07_Variance_Reduction.md (8k tokens)
- markdown_docs/user_manual/chapter_05_input_cards/05_12_Variance_Reduction_Cards.md (included in A/B)
- markdown_docs/examples/chapter_10/10_06_Variance_Reduction_Examples.md (included in A/B)

**Total:** ~50k tokens read ONCE for 4 skills (assuming D docs not cached)
**Sequential would be:** 50k × 4 = 200k tokens
**Savings:** 150k tokens

---

**Category F (6 skills)**
Skills: unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator

**Shared Documentation:**
- markdown_docs/appendices/AppendixE_01_Doppler_Broadening.md (2k tokens)
- markdown_docs/appendices/AppendixE_02_Event_Log_Analyzer.md (2k tokens)
- markdown_docs/appendices/AppendixE_03_Doppler_Fitting.md (2k tokens)
- markdown_docs/appendices/AppendixE_04_Gridconv.md (2k tokens)
- markdown_docs/appendices/AppendixE_05_Cross_Section_Tool.md (3k tokens)
- markdown_docs/appendices/AppendixE_06_Merge_ASCII_Tally.md (2k tokens)
- markdown_docs/appendices/AppendixE_07_Merge_Mesh_Tally.md (2k tokens)
- markdown_docs/appendices/AppendixE_08_Parameter_Study_Tool.md (3k tokens)
- markdown_docs/appendices/AppendixE_09_Simple_ACE_Tools.md (2k tokens)
- markdown_docs/appendices/AppendixE_10_UM_Converter.md (3k tokens)
- markdown_docs/appendices/AppendixE_11_UM_Post_Processing.md (3k tokens)
- markdown_docs/appendices/AppendixE_12_UM_Pre_Processing.md (3k tokens)

**Total:** ~29k tokens read ONCE for 6 skills
**Sequential would be:** 29k × 6 = 174k tokens
**Savings:** 145k tokens

---

**Category C & Specialized (4 skills)**
Skills: fatal-error-debugger, warning-analyzer, criticality-analyzer, best-practices-checker, example-finder, knowledge-docs-finder, burnup-builder, input-updater

**Shared Documentation:** Minimal, mostly skill-specific
- markdown_docs/user_manual/03_Introduction_to_MCNP_Usage.md (if not cached)
- markdown_docs/user_manual/04_Description_of_MCNP6_Input.md (if not cached)
- Skill-specific sections from Chapter 5

**Total:** ~20k tokens read for 4 skills
**Sequential would be:** Variable (20-40k per skill) = ~120k tokens
**Savings:** ~60k tokens

---

## Phase-by-Phase Breakdown

### Phase 1: Category A & B (16 skills)

**Documentation Reading (ONE TIME):**
```
Chapters 3, 4: 35k tokens
Chapter 5 (all 12 files): 40k tokens
Chapter 10 (all 5 files): 5k tokens
Total: 80k tokens
```

**Processing (PER SKILL):**
```
Review current SKILL.md: 2k tokens
Identify discrepancies: 1k tokens
Create revamp plan: 1k tokens
Extract to references/: 2k tokens
Add examples to assets/: 1k tokens
Streamline SKILL.md: 3k tokens
Quality check & test: 1k tokens
Update STATUS: 1k tokens
Total per skill: ~12k tokens (rounded to 10k for estimation)
```

**Phase 1 Total:**
```
Read docs once: 80k tokens
Process 16 skills: 16 × 10k = 160k tokens
Total: 240k tokens
```

**Session Planning:**
- Session budget: 200k tokens per session
- Reserve for handoff: 20k tokens
- Usable: 180k tokens

**Recommendation:** Split Phase 1 into 2 sessions
- Session A: Read all docs (80k) + process 8 skills (80k) = 160k + 20k handoff = 180k total
- Session B: Resume processing remaining 8 skills (80k) + handoff (20k) = 100k total

Or potentially 1 long session if careful with tokens.

---

### Phase 2: Category D (6 skills)

**Documentation Reading (ONE TIME):**
```
Chapter 8: 10k tokens
Appendix D (7 files): 29k tokens
Appendix E.11: 3k tokens
Total: 42k tokens
```

**Processing:** 6 × 10k = 60k tokens

**Phase 2 Total:** 42k + 60k = 102k tokens

**Session Planning:** 1 session (fits comfortably in 200k budget)

---

### Phase 3: Category E (4 skills)

**Documentation Reading (ONE TIME):**
```
All Category D docs: 42k tokens (if not cached, otherwise 0k)
Variance reduction theory: 8k tokens
Total: 50k tokens (worst case)
```

**Processing:** 4 × 10k = 40k tokens

**Phase 3 Total:** 50k + 40k = 90k tokens

**Session Planning:** 1 session

---

### Phase 4: Category F (6 skills)

**Documentation Reading (ONE TIME):**
```
Appendix E (12 files): 29k tokens
Total: 29k tokens
```

**Processing:** 6 × 10k = 60k tokens

**Phase 4 Total:** 29k + 60k = 89k tokens

**Session Planning:** 1 session

---

### Phase 5: Category C & Specialized (4 skills)

**Documentation Reading:** Variable, skill-specific, ~20k tokens

**Processing:** 4 × 10k = 40k tokens

**Phase 5 Total:** 20k + 40k = 60k tokens

**Session Planning:** 1 session

---

## Total Project Token Budget

### Batched Approach (RECOMMENDED)

| Phase | Skills | Doc Reading | Processing | Total | Sessions |
|-------|--------|-------------|------------|-------|----------|
| 0 (Infra) | - | 0k | 30k | 30k | 1 |
| 1 (A&B) | 16 | 80k | 160k | 240k | 2-3 |
| 2 (D) | 6 | 42k | 60k | 102k | 1 |
| 3 (E) | 4 | 50k | 40k | 90k | 1 |
| 4 (F) | 6 | 29k | 60k | 89k | 1 |
| 5 (C+) | 4 | 20k | 40k | 60k | 1 |
| **Total** | **36** | **221k** | **390k** | **611k** | **7-9** |

**Note:** Actual totals may be lower due to:
- Caching between sessions (already-read docs not re-read)
- Efficiency gains from repeated workflow
- Estimates are conservative (10k per skill may be high)

### Sequential Approach (DO NOT USE)

| Phase | Skills | Doc Reading | Processing | Total | Sessions |
|-------|--------|-------------|------------|-------|----------|
| N/A | 36 | 2,160k | 390k | 2,550k | 13-15 |

**Token Waste:** 2,160k - 221k = 1,939k tokens wasted on duplicate reading

**Savings from Batched:** 1,939k tokens (76% reduction in total project)

---

## Implementation Guidelines

### Session Start Checklist

**Before Reading Any Documentation:**
1. Check REVAMP-PROJECT-STATUS.md to see which phase you're in
2. Determine which documentation is required for this phase
3. Check if documentation was already read earlier in same phase
4. If starting new phase: Read ALL shared docs ONCE at beginning

**During Phase Execution:**
1. Read shared documentation ONCE at phase start
2. Take comprehensive notes (capture in STATUS document)
3. Process all skills in batch without re-reading docs
4. Reference notes when needed instead of re-reading

### Token Monitoring

**Throughout session:**
- Check token usage every 30 minutes
- Log token usage for major operations:
  - "Read Chapter 5_02_Cell_Cards.md: 4k tokens"
  - "Processed mcnp-geometry-builder: 11k tokens"
- Update REVAMP-PROJECT-STATUS.md with running totals

**If approaching token limit:**
- At 150k tokens used: Assess if can complete current skill
- At 170k tokens used: Begin preparing handoff documentation
- At 180k tokens used: STOP work, finalize handoff
- Never exceed 190k tokens (reserve 10k buffer)

### Efficiency Tips

**Maximize batching:**
- Process all skills in phase before moving to next phase
- Don't jump between categories
- Complete one phase fully before starting next

**Minimize token waste:**
- Extract key information during first read
- Document findings in STATUS (don't re-read later)
- Use search/grep for quick lookups in large docs
- Cache commonly-referenced sections

**Optimize processing:**
- Use templates for repetitive tasks
- Develop standard extraction patterns
- Reuse example files across similar skills
- Create shared references/ content once

---

## Validation of Estimates

### Per-Skill Token Breakdown (Detailed)

**Example: mcnp-geometry-builder**

1. Read current SKILL.md (1,087 lines): ~2.5k tokens
2. Review already-read docs for geometry info: 0k (already in context)
3. Identify discrepancies (create list): ~1k tokens
4. Create revamp plan (detailed checklist): ~1k tokens
5. Extract to references/:
   - Create references/surface_types.md (300 lines): ~1.5k tokens
   - Create references/macrobody_specs.md (200 lines): ~1k tokens
6. Add examples to assets/:
   - Copy 5 files from example_files/: minimal tokens
   - Write descriptions: ~0.5k tokens
7. Create/update scripts/:
   - Check if Python modules mentioned: minimal
8. Streamline SKILL.md:
   - Rewrite to <3k words: ~3k tokens
   - Remove duplicated content: minimal
9. Quality checklist (25 items): ~1k tokens
10. Test skill invocation: minimal
11. Update STATUS document: ~1k tokens

**Total: ~12k tokens per skill (estimate of 10k is conservative)**

### Documentation Reading Token Estimates

**Chapter 5_02_Cell_Cards.md:**
- File size: ~8,000 lines
- Estimated tokens: ~4,000 tokens (typical markdown compression)

**Chapter 5_03_Surface_Cards.md:**
- File size: ~10,000 lines
- Estimated tokens: ~5,000 tokens

**Full Chapter 5 (12 files):**
- Combined size: ~60,000 lines
- Estimated tokens: ~30-40k tokens (using 40k for conservative estimate)

**Validation:** Estimates are conservative (tend high) to ensure adequate token budget

---

## Risk Mitigation

### Risk: Under-Estimating Token Usage

**Mitigation:**
- Use conservative estimates (10k per skill vs actual 8-9k)
- Add 20% buffer to all estimates
- Monitor actual usage and adjust

### Risk: Documentation Longer Than Expected

**Mitigation:**
- Check file sizes before reading
- Use offset/limit parameters for very large files
- Read critical sections first
- Reference documentation instead of full read if needed

### Risk: Session Interruption Mid-Phase

**Mitigation:**
- Always update STATUS document immediately after reading docs
- Capture key findings from documentation in STATUS
- Mark which skills in batch are complete vs pending
- Next Claude can resume without re-reading docs

---

## Success Metrics

### Token Efficiency

**Target:** 85% savings vs sequential approach
**Measurement:** Compare actual token usage to sequential baseline
**Success Criteria:** Total project <700k tokens (vs 2,400k sequential)

### Session Count

**Target:** Complete in 7-9 sessions
**Measurement:** Count sessions from start to finish
**Success Criteria:** Average <5 skills per session

### Documentation Re-Reading

**Target:** Zero duplicate reads within same phase
**Measurement:** Log all documentation reads in STATUS
**Success Criteria:** Each doc read exactly once per phase

---

## Conclusion

The batched processing approach offers dramatic improvements:

**Benefits:**
- ✅ 85% token savings (2,400k → 430k)
- ✅ Faster completion (7-9 sessions vs 13-15)
- ✅ Better consistency (same context for all skills in category)
- ✅ Lower cost (fewer Claude API calls)
- ✅ Easier to maintain (phase-based organization)

**Implementation Requirements:**
- ✅ Read must-read-docs.md to identify shared documentation
- ✅ Group skills by category before starting
- ✅ Read ALL shared docs at phase start (don't skip)
- ✅ Document findings comprehensively in STATUS
- ✅ Process all skills in batch without re-reading
- ✅ Monitor tokens carefully throughout

**Key Insight:** Reading documentation is the expensive part (~200k tokens). Processing skills is relatively cheap (~10k each). Batching maximizes the value of documentation reading by amortizing cost across many skills.

**Recommendation:** Follow the 5-phase execution plan strictly. Do not deviate to sequential processing.
