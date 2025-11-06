# MCNP Knowledge Base Documentation Map

**Location:** `C:\Users\dman0\Desktop\AI_Training_Docs\MCNP6\markdown_docs\`
**Total:** 72 markdown files, 4.2 MB
**Source:** must-read-docs.md (authoritative mapping)

---

## Directory Structure

```
markdown_docs/
├── user_manual/
│   ├── 03_Introduction_to_MCNP_Usage.md (~15k tokens)
│   ├── 04_Description_of_MCNP6_Input.md (~20k tokens)
│   ├── chapter_05_input_cards/ (12 files, ~40k tokens total)
│   └── 08_Unstructured_Mesh.md (~10k tokens)
├── appendices/
│   ├── AppendixA_Mesh_File_Formats.md
│   ├── AppendixD_* (D.3-D.9: Mesh/output formats)
│   └── AppendixE_* (E.1-E.12: Utility tools)
├── examples/chapter_10/ (5 files, ~5k tokens total)
├── theory_manual/chapter_02/
│   └── 02_07_Variance_Reduction.md (~8k tokens)
└── primers/
```

---

## Documentation by Category (per must-read-docs.md)

### Category A & B: Input Creation & Editing (16 skills)

**Required Reading:** 20 files, ~80k tokens

**Core Files:**
1. `user_manual/03_Introduction_to_MCNP_Usage.md` (15k tokens)
2. `user_manual/04_Description_of_MCNP6_Input.md` (20k tokens)

**Chapter 5 - Input Cards (12 files, ~40k tokens):**
3. `chapter_05_input_cards/05_01_Geometry_Specification_Intro.md`
4. `chapter_05_input_cards/05_02_Cell_Cards.md` - Cell definitions
5. `chapter_05_input_cards/05_03_Surface_Cards.md` - All surface types
6. `chapter_05_input_cards/05_05_Geometry_Data_Cards.md` - TR, U, LAT, FILL
7. `chapter_05_input_cards/05_06_Material_Data_Cards.md` - M, MT, ZAID
8. `chapter_05_input_cards/05_07_Physics_Data_Cards.md` - MODE, PHYS, CUT
9. `chapter_05_input_cards/05_08_Source_Data_Cards.md` - SDEF, KCODE, SI/SP
10. `chapter_05_input_cards/05_09_Tally_Data_Cards.md` - F1-F8, FM, DE/DF
11. `chapter_05_input_cards/05_10_Tally_Perturbations.md` - PERT
12. `chapter_05_input_cards/05_11_Mesh_Tallies.md` - FMESH, TMESH
13. `chapter_05_input_cards/05_12_Variance_Reduction_Cards.md` - IMP, WWN, EXT
14. `chapter_05_input_cards/05_13_Output_Control_Misc.md` - NPS, PRINT, FILES

**Chapter 10 - Examples (5 files, ~5k tokens):**
15. `examples/chapter_10/10_01_Geometry_Examples.md`
16. `examples/chapter_10/10_02_Tally_Examples.md`
17. `examples/chapter_10/10_03_Source_Examples.md`
18. `examples/chapter_10/10_05_Physics_Models.md`
19. `examples/chapter_10/10_06_Variance_Reduction_Examples.md`

**Skills Using:** input-builder, geometry-builder, material-builder, source-builder, tally-builder, physics-builder, lattice-builder, geometry-editor, input-editor, input-validator, cell-checker, cross-reference-checker, geometry-checker, physics-validator, transform-editor, variance-reducer

**Token Cost:** 80k tokens (read ONCE for all 16 skills)

---

### Category C: Validation & Debugging (5 skills)

**Required Reading:** 2 files, ~35k tokens

1. `user_manual/03_Introduction_to_MCNP_Usage.md` (~15k tokens)
2. `user_manual/04_Description_of_MCNP6_Input.md` (~20k tokens)
   - **§4.7 Input Error Messages** (CRITICAL)
   - **§4.8 Geometry Errors** (CRITICAL)

**Optional:**
- `primers/source_primer/05_Known_Source_Errors.md`
- `user_manual/chapter_05_input_cards/05_13_Output_Control_Misc.md` (error tables)

**Skills Using:** input-validator, geometry-checker, cross-reference-checker, fatal-error-debugger, warning-analyzer

**Token Cost:** ~35k tokens

---

### Category D: Output Analysis (6 skills)

**Required Reading:** 10 files, ~42k tokens

1. `user_manual/08_Unstructured_Mesh.md` (~10k tokens)
2. `appendices/AppendixA_Mesh_File_Formats.md` (~3k tokens)

**Appendix D - Output Formats (7 files, ~26k tokens):**
3. `appendices/AppendixD_03_Particle_Track_Output.md` (PTRAC format)
4. `appendices/AppendixD_04_Mesh_Tally_XDMF.md` (XDMF structure)
5. `appendices/AppendixD_05_Fission_Matrix.md`
6. `appendices/AppendixD_06_Unstructured_Mesh_HDF5.md` (HDF5 structure)
7. `appendices/AppendixD_07_Unstructured_Mesh_Legacy.md`
8. `appendices/AppendixD_08_HDF5_Script.md`
9. `appendices/AppendixD_09_inxc_File_Structure.md`

**Post-Processing:**
10. `appendices/AppendixE_11_UM_Post_Processing.md` (~3k tokens)

**Skills Using:** output-parser, mctal-processor, mesh-builder, plotter, tally-analyzer (partial), statistics-checker (partial)

**Token Cost:** ~42k tokens (read ONCE for all 6 skills)

---

### Category E: Advanced Operations (4 skills)

**Required Reading:** All Category D docs + 3 additional files, ~50k tokens

**Category D docs:** 42k tokens (if not already read)

**Additional:**
11. `theory_manual/chapter_02/02_07_Variance_Reduction.md` (~8k tokens)
12. `user_manual/chapter_05_input_cards/05_12_Variance_Reduction_Cards.md` (included in A/B)
13. `examples/chapter_10/10_06_Variance_Reduction_Examples.md` (included in A/B)

**Skills Using:** variance-reducer (complete), ww-optimizer, tally-analyzer (complete), statistics-checker (complete)

**Token Cost:** ~50k tokens (worst case if D docs not cached)

---

### Category F: Utilities (6 skills)

**Required Reading:** 12 files, ~29k tokens

**Appendix E - Utility Tools (12 files):**
1. `appendices/AppendixE_01_Doppler_Broadening.md` (~2k tokens)
2. `appendices/AppendixE_02_Event_Log_Analyzer.md` (~2k tokens)
3. `appendices/AppendixE_03_Doppler_Fitting.md` (~2k tokens)
4. `appendices/AppendixE_04_Gridconv.md` (~2k tokens)
5. `appendices/AppendixE_05_Cross_Section_Tool.md` (~3k tokens)
6. `appendices/AppendixE_06_Merge_ASCII_Tally.md` (~2k tokens)
7. `appendices/AppendixE_07_Merge_Mesh_Tally.md` (~2k tokens)
8. `appendices/AppendixE_08_Parameter_Study_Tool.md` (~3k tokens)
9. `appendices/AppendixE_09_Simple_ACE_Tools.md` (~2k tokens)
10. `appendices/AppendixE_10_UM_Converter.md` (~3k tokens)
11. `appendices/AppendixE_11_UM_Post_Processing.md` (~3k tokens)
12. `appendices/AppendixE_12_UM_Pre_Processing.md` (~3k tokens)

**Note:** Appendix E provides IDEAS for utility skills, not strict requirements
**Purpose:** Help Claude understand MCNP utility ecosystem
**Usage:** Reference for utility skill concepts, not prescriptive

**Skills Using:** unit-converter, physical-constants, isotope-lookup, cross-section-manager, parallel-configurator, template-generator

**Token Cost:** ~29k tokens (read ONCE for all 6 skills)

---

## Documentation Sharing Matrix

| Category | Skills | Shared Docs | Token Cost | Savings vs Sequential |
|----------|--------|-------------|------------|----------------------|
| A & B | 16 | Chapters 3,4,5,10 | 80k | 1,200k (94%) |
| C | 5 | Chapters 3,4 | 35k | 140k (80%) |
| D | 6 | Ch 8, App D | 42k | 210k (83%) |
| E | 4 | D + VR theory | 50k | 150k (75%) |
| F | 6 | Appendix E | 29k | 145k (83%) |

**Total Savings:** 1,845k tokens (85% reduction)

---

## Key Documentation Files

### Most Referenced (Read for Multiple Categories)

1. **03_Introduction_to_MCNP_Usage.md** - Categories A, B, C
2. **04_Description_of_MCNP6_Input.md** - Categories A, B, C
3. **05_12_Variance_Reduction_Cards.md** - Categories A, B, E
4. **10_06_Variance_Reduction_Examples.md** - Categories A, B, E

### Category-Specific Critical Files

**Geometry:** 05_01, 05_02, 05_03, 10_01
**Materials:** 05_06
**Sources:** 05_08, 10_03
**Tallies:** 05_09, 05_10, 05_11, 10_02
**Physics:** 05_07, 10_05
**Variance Reduction:** 05_12, 10_06, 02_07
**Output:** 08, AppendixD (all), AppendixA
**Utilities:** AppendixE (all)

---

## Reading Strategy

### Phase 1 (Category A/B) - Read Order:
1. Chapter 3 (Introduction) - Foundation
2. Chapter 4 (Input Description) - Structure
3. Chapter 5 files in order 01→13 - Systematic card coverage
4. Chapter 10 files - Examples for context

**Time estimate:** 2-3 hours to read all docs
**Take notes:** Capture key concepts in PHASE-1-PROJECT-STATUS.md (or current phase status document)
**Purpose:** Deep understanding for 16 skills

### Phase 2 (Category D) - Read Order:
1. Chapter 8 (Unstructured Mesh) - Overview
2. Appendix A (Mesh Formats) - File structure
3. Appendix D files sequentially - Output formats

**Time estimate:** 1-1.5 hours

### Phase 3 (Category E) - Read Order:
1. Review Category D docs (if not cached)
2. Chapter 02_07 (VR Theory) - Mathematical foundation
3. Review 05_12 and 10_06 (if not cached) - Practical VR

**Time estimate:** 1 hour

### Phase 4 (Category F) - Read Order:
1. Appendix E files sequentially - Utility tool ecosystem

**Time estimate:** 1 hour

### Phase 5 (Category C) - Read Order:
1. Chapter 3 and 4 (if not cached)
2. Focus on §4.7 and §4.8 - Error messages

**Time estimate:** 0.5-1 hour (mostly review)

---

## Documentation Quality Notes

**Comprehensive Coverage:**
- ✅ All MCNP6 capabilities documented
- ✅ Examples for every card type
- ✅ Error patterns catalogued
- ✅ File formats fully specified

**Well-Organized:**
- ✅ Consistent chapter structure
- ✅ Clear section headings
- ✅ Cross-references between chapters
- ✅ Progressive complexity (intro → details → examples)

**Token-Efficient:**
- ✅ Most files 2-5k tokens
- ✅ Largest files ~10k tokens (manageable)
- ✅ Can read in chunks with offset/limit if needed

---

## Usage Guidelines

### For Skill Revamp:

**Before starting a category/phase:**
1. Check must-read-docs.md for required files
2. Read ALL files for that category ONCE at phase start
3. Take comprehensive notes in phase-specific status document (e.g., PHASE-1-PROJECT-STATUS.md)
4. Reference notes during skill processing (don't re-read)

**During skill processing:**
1. Cross-reference current SKILL.md against doc notes
2. Identify gaps/discrepancies
3. Extract appropriate content to root-level reference .md files (NOT in subdirectories)
4. Link to documentation in References section

**CRITICAL STRUCTURE (Lesson #16):**
- Reference .md files go DIRECTLY at root level of skill directory
- NO `references/` subdirectory
- NO `assets/` subdirectory
- Use `example_inputs/` and `templates/` DIRECTLY at root level

**Documentation citations:**
```markdown
## References

**MCNP6 User Manual:**
- Cell card syntax: Chapter 5.2
- Surface types: Chapter 5.3
- Material specifications: Chapter 5.6

**MCNP6 Examples:**
- Geometry examples: Chapter 10.1
- Tally examples: Chapter 10.2
```

---

## Conclusion

The markdown_docs/ knowledge base is:
- ✅ Comprehensive (72 files, 4.2 MB)
- ✅ Well-organized (clear structure)
- ✅ Batching-friendly (clear category sharing)
- ✅ Already converted to markdown (no additional work needed)

**Critical Success Factor:** Read documentation ONCE per category in batched approach
**Token Savings:** 1,845k tokens (85% vs sequential)
**Reference:** must-read-docs.md is authoritative mapping

**Critical Structure Requirements:**
- Extract content to root-level reference .md files (NOT references/ subdirectory)
- Use phase-specific status documents (PHASE-1-PROJECT-STATUS.md, etc.)
- NO assets/ subdirectory per Lesson #16
- All subdirectories (example_inputs/, templates/, scripts/) DIRECTLY at root level

**Next Steps:** Follow must-read-docs.md strictly during phase execution and maintain zero tolerance for assets/ subdirectory.
