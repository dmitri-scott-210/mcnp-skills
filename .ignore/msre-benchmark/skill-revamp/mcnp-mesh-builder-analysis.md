# mcnp-mesh-builder Skill Revamp Analysis

**Date:** 2025-11-06
**Session:** Session-20251106-120000-Phase2
**Current Status:** Analysis phase

---

## Current State Assessment

**File:** `.claude/skills/mcnp-mesh-builder/SKILL.md`
**Lines:** 662 lines
**Version:** 1.0.0 (needs update to 2.0.0)
**Word Count:** ~4,200 words (within target range)

### Strengths

1. ✅ Clear decision tree for mesh type selection
2. ✅ Comprehensive FMESH syntax coverage
3. ✅ Good TMESH legacy format documentation
4. ✅ 5 practical use cases with complete examples
5. ✅ Troubleshooting section with common problems
6. ✅ Good integration section structure
7. ✅ Best practices list (11 items)

### Critical Issues (ZERO TOLERANCE)

1. ❌ **Broken Python module references** (lines 592-637):
   - `skills.output_analysis.mcnp_tally_analyzer` - does NOT exist
   - `skills.visualization.mcnp_plotter` - does NOT exist
   - `skills.variance_reduction.mcnp_ww_optimizer` - does NOT exist
   - `mcnp_mesh_builder.py` (line 652) - referenced but not bundled

2. ❌ **Missing unstructured mesh (UM) content** - MAJOR GAP:
   - NO coverage of EMBED command
   - NO coverage of external mesh files (ABAQUS, CGAL, GMSH, VTK)
   - NO coverage of unstructured mesh geometry
   - NO coverage of UM tallies
   - NO um_post_op utility documentation

3. ❌ **No bundled Python scripts**:
   - Script referenced (line 652) but not provided
   - No mesh generation utilities
   - No mesh visualization tools

---

## Documentation Cross-Reference

### Phase 2 Documentation Read (Previous Session)

**Relevant files for mcnp-mesh-builder:**

1. **Chapter 8: Unstructured Mesh** (~12k tokens)
   - UM geometry definition
   - EMBED command syntax
   - MESHGEO card
   - External mesh file integration

2. **Appendix A: Mesh File Formats** (~5k tokens)
   - ABAQUS format (.inp)
   - CGAL format
   - GMSH format (.msh)
   - VTK format (.vtk)
   - Format conversion guidance

3. **Appendix D.4: Mesh Tally XDMF** (~5k tokens)
   - XDMF format for structured mesh (FMESH)
   - HDF5 binary data structure
   - ParaView integration

4. **Appendix D.6: Unstructured Mesh HDF5** (~7k tokens)
   - HDF5 format for UM tallies
   - Dataset organization
   - UM-specific output structure

5. **Appendix D.7: Unstructured Mesh Legacy** (~4k tokens)
   - EEOUT format (legacy UM output)
   - ASCII UM output
   - Backward compatibility

6. **Appendix E.11: UM Post-Processing** (~5k tokens)
   - um_post_op utility (7 operations)
   - Visualization workflows
   - Data extraction methods

**Total relevant content:** ~38k tokens worth of unstructured mesh documentation

---

## Major Gaps Identified

### Gap 1: Unstructured Mesh (UM) Coverage

**Current:** ZERO coverage of UM in SKILL.md
**Should have:** Complete UM section with:
- EMBED command syntax
- External mesh file formats (ABAQUS, CGAL, GMSH, VTK)
- UM geometry specification
- UM tally setup
- UM output processing

**Evidence from docs:**
- Chapter 8 has 12k tokens of UM content
- Appendix A covers 4 mesh file formats
- Appendices D.6, D.7 cover UM output
- Appendix E.11 covers um_post_op utility

**Impact:** Users won't know how to use unstructured meshes (critical for complex geometry)

**Fix:** Create `unstructured_mesh_guide.md` at ROOT level with comprehensive UM coverage

### Gap 2: External Mesh Files

**Current:** No mention of external mesh generation tools
**Should have:** Guidance on:
- GMSH workflow (generate mesh → export → MCNP)
- ABAQUS format integration
- Format conversion tools
- Mesh quality requirements

**Evidence:** Appendix A documents all formats

**Impact:** Users can't use CAD-generated meshes

**Fix:** Create `external_mesh_formats.md` at ROOT level

### Gap 3: um_post_op Utility

**Current:** No coverage of post-processing tools
**Should have:** Complete um_post_op documentation:
- 7 operations (extract, combine, average, etc.)
- Command-line syntax
- Workflow examples

**Evidence:** Appendix E.11 documents entire utility

**Impact:** Users can't process UM output files

**Fix:** Add section to `unstructured_mesh_guide.md`

### Gap 4: Python Scripts

**Current:** References `mcnp_mesh_builder.py` (line 652) but script doesn't exist
**Should have:** Bundled scripts for:
- FMESH card generation (programmatic)
- Mesh visualization
- Mesh refinement utilities
- Format conversion

**Impact:** Users can't automate mesh generation

**Fix:** Create scripts in `scripts/` at ROOT level:
- `fmesh_generator.py` - Generate FMESH cards programmatically
- `mesh_visualizer.py` - Plot mesh geometry
- `mesh_converter.py` - Convert between formats

### Gap 5: Broken Integration References

**Current:** References non-existent Python modules (lines 592-637)
**Should have:** Valid cross-references to:
- mcnp-output-parser (for reading mesh output)
- mcnp-plotter (for visualization)
- mcnp-tally-analyzer (for analysis)
- mcnp-ww-optimizer (for VR)

**Impact:** Code examples won't work, confuse users

**Fix:** Replace with clear skill boundary descriptions + workflow guidance

---

## Skill Revamp Plan

### Step 1: Extract Content to ROOT Level Reference Files

**Create at `.claude/skills/mcnp-mesh-builder/` (ROOT level):**

1. **`unstructured_mesh_guide.md`** (~1,200 lines)
   - EMBED command comprehensive syntax
   - External mesh file integration (ABAQUS, CGAL, GMSH, VTK)
   - UM geometry specification
   - UM tally setup (FMESH with EMBED)
   - um_post_op utility documentation (7 operations)
   - UM output formats (HDF5, legacy EEOUT)
   - Complete workflow examples

2. **`mesh_file_formats.md`** (~600 lines)
   - ABAQUS format (.inp) specification
   - CGAL format details
   - GMSH format (.msh) specification
   - VTK format (.vtk) specification
   - Format comparison table
   - Conversion guidance

3. **`mesh_optimization_guide.md`** (~400 lines)
   - Mesh resolution strategies
   - Adaptive refinement techniques
   - Statistical quality vs mesh size
   - Performance considerations (MSHMF algorithms)
   - Best practices for mesh design

### Step 2: Create Bundled Python Scripts

**Create at `.claude/skills/mcnp-mesh-builder/scripts/` (ROOT level):**

1. **`fmesh_generator.py`** (~250 lines)
   - Programmatic FMESH card generation
   - Support XYZ and RZT geometries
   - Automatic binning optimization
   - Energy/time bin helpers

2. **`mesh_visualizer.py`** (~200 lines)
   - Plot mesh geometry (matplotlib)
   - Show mesh overlay on problem geometry
   - Quick validation tool

3. **`mesh_converter.py`** (~150 lines)
   - Convert between mesh formats
   - GMSH → ABAQUS
   - VTK → GMSH
   - Format validation

4. **`README.md`** (~100 lines)
   - Script descriptions
   - Usage examples
   - Dependencies (h5py, numpy, matplotlib)

**Total scripts:** ~700 lines

### Step 3: Add Example Files

**Create at `.claude/skills/mcnp-mesh-builder/example_inputs/` (ROOT level):**

1. **`01_simple_fmesh_cartesian.i`** - Basic XYZ mesh
2. **`02_fmesh_cylindrical.i`** - RZT mesh for cylindrical geometry
3. **`03_fmesh_with_energy_bins.i`** - Multi-group flux
4. **`04_fmesh_time_dependent.i`** - Time-binned mesh
5. **`05_fmesh_reaction_rate.i`** - FM card for isotopic reactions
6. **`06_tmesh_legacy.i`** - TMESH format example
7. **`07_unstructured_mesh_embed.i`** - UM with EMBED command
8. **`08_external_gmsh_mesh.i`** - Using external GMSH file

**Each with corresponding `.md` description file**

### Step 4: Update SKILL.md

**Changes to make:**

1. **Remove broken Python references** (lines 592-637)
2. **Add UM section** to decision tree
3. **Update integration section** with skill boundaries (not code examples)
4. **Add references** to new bundled resources
5. **Update version** to 2.0.0
6. **Add UM use case** (Use Case 6)
7. **Update best practices** to include UM guidance

**Target:** Keep SKILL.md at ~800 lines (currently 662)
**Approach:** Add UM overview, reference detailed docs for specifics

### Step 5: Fix Integration Section

**Replace Python code examples with:**
- Clear skill boundary descriptions
- Workflow guidance (which skill to use when)
- Conceptual integration patterns
- References to other skills' capabilities

**Example:**
```markdown
### With mcnp-output-parser

After running MCNP with mesh tallies:
1. Use mcnp-output-parser to read meshtal.xdmf or MCTAL files
2. Extract mesh tally data for analysis
3. See mcnp-output-parser documentation for HDF5/XDMF parsing

For detailed mesh data analysis, see mcnp-tally-analyzer.
```

### Step 6: Quality Validation

**26-item checklist:**
- [ ] 1-5: YAML frontmatter (update version to 2.0.0)
- [ ] 6-15: SKILL.md structure (add UM section)
- [ ] 16-17: Reference files at ROOT (unstructured_mesh_guide.md, etc.)
- [ ] 18-19: Scripts bundled and functional
- [ ] 20: example_inputs/ at ROOT with 8 examples
- [ ] 21: No templates needed for this skill
- [ ] 22: Each example has .md description
- [ ] 23: **NO assets/ directory** (ZERO TOLERANCE)
- [ ] 24-26: Content quality (MCNP syntax, cross-references, docs)

---

## Token Budget Estimate

**For mcnp-mesh-builder revamp:**

1. Analysis (this document): ~2k tokens ✅
2. Create reference files (3 files): ~6k tokens
3. Create scripts (4 files): ~4k tokens
4. Create examples (8 files + descriptions): ~5k tokens
5. Update SKILL.md: ~3k tokens
6. Validation and testing: ~2k tokens

**Total:** ~22k tokens (well within budget)

**Reusing:** Phase 2 docs already read (~0k tokens)

---

## Next Steps

1. ✅ Complete this analysis
2. ⏭️ Create `unstructured_mesh_guide.md` (extract from Chapter 8, Appendices D.6, D.7, E.11)
3. ⏭️ Create `mesh_file_formats.md` (extract from Appendix A)
4. ⏭️ Create `mesh_optimization_guide.md` (extract from performance sections)
5. ⏭️ Create 4 Python scripts in `scripts/`
6. ⏭️ Create 8 example files + descriptions in `example_inputs/`
7. ⏭️ Update SKILL.md (add UM, fix references, update version)
8. ⏭️ Run 26-item quality checklist
9. ⏭️ Mark mcnp-mesh-builder COMPLETE

---

**Status:** Analysis complete, ready for execution
**Estimated completion:** ~22k tokens (2/6 remaining Phase 2 budget)
