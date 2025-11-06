# MCNP Output Parser - Integration Plan

**Date:** 2025-11-06
**Session:** Session-20251106-043233-Phase2
**Skill:** mcnp-output-parser
**Status:** Analysis Complete - Ready for Implementation

---

## Executive Summary

**Current Status:** mcnp-output-parser has strong foundational content (1231 lines) but has CRITICAL DEFICIENCIES that violate Phase 2 requirements:

- ⚠️ **CRITICAL:** NO bundled Python scripts (ZERO TOLERANCE violation)
- ⚠️ **CRITICAL:** References non-existent external modules (`skills/output_analysis/`)
- Missing um_post_op utility documentation (Appendix E.11)
- Missing inxc file structure details (Appendix D.9)
- Missing HDF5 hierarchy script bundling (Appendix D.8)
- Incomplete EEOUT legacy format coverage (Appendix D.7)

**Estimated Work:** 6-8 steps of 11-step workflow, ~15k tokens

---

## Skill Boundary Analysis

### What mcnp-output-parser SHOULD DO:
✓ Extract raw data from ALL MCNP output formats (OUTP, MCTAL, HDF5, XDMF, PTRAC, MESHTAL, EEOUT, inxc)
✓ Provide data in usable Python structures (dicts, arrays, DataFrames)
✓ Basic validation (warnings, errors, termination status, file integrity)
✓ Document all output format structures comprehensively
✓ Bundle essential parsing scripts at ROOT `scripts/` level
✓ Provide working examples for each format

### What mcnp-output-parser should NOT DO:
✗ Merging/combining MCTAL files → **mcnp-mctal-processor**
✗ Export to CSV/Excel/JSON → **mcnp-mctal-processor**
✗ Statistical combinations/weighted averages → **mcnp-mctal-processor**
✗ Creating plots/visualizations → **mcnp-plotter**
✗ Creating mesh tally inputs → **mcnp-mesh-builder**

### Overlap Resolution:
- **mcnp-output-parser**: Basic MCTAL parsing for data extraction
- **mcnp-mctal-processor**: Advanced MCTAL processing, merging, export
- **Clear handoff**: "For advanced MCTAL processing (merging, export), see mcnp-mctal-processor"

---

## Current Content Assessment

### Strengths (Keep/Enhance):
1. ✓ Comprehensive OUTP format documentation
2. ✓ Detailed HDF5 structure (Appendices D.3-D.6 content)
3. ✓ PTRAC format coverage
4. ✓ XDMF format explanation
5. ✓ Fission matrix CSR format
6. ✓ Workflow decision trees
7. ✓ Statistical quality checks overview
8. ✓ Integration examples

### Weaknesses (Fix/Add):
1. ❌ **CRITICAL:** No actual bundled Python scripts
2. ❌ References to non-existent `skills/output_analysis/` modules
3. ❌ Missing um_post_op utility documentation (Appendix E.11)
4. ❌ Missing inxc file structure (Appendix D.9)
5. ❌ Missing HDF5 hierarchy script (Appendix D.8)
6. ❌ Incomplete EEOUT legacy format (Appendix D.7)
7. ❌ No clear skill boundary explanations
8. ❌ Some examples lack MCNP format compliance

---

## Documentation Gaps Analysis

### Gap 1: um_post_op Utility (Appendix E.11)

**What's Missing:**
- Legacy EEOUT post-processing utility documentation
- Command-line options and usage patterns
- When to use vs modern HDF5 workflow

**Content to Add:**
```markdown
### Legacy EEOUT Processing (um_post_op)

**Deprecation Notice:** EEOUT format deprecated in MCNP6.3+, replaced by HDF5.
Use um_post_op only for legacy file processing.

**Command-line options:**
- `-m <files>` - Merge multiple EEOUT files
- `-a <files>` - Add EEOUT files
- `-bc <file>` - Convert binary ↔ ASCII
- `-vtk <file>` - Generate VTK output for ParaView
- `-ta <file>` - Create pseudo-tallies
- `-wse <edit>` - Write single edit
- `-eh` - Generate error histograms

**Example workflows:**
```bash
# Merge parallel run results
um_post_op -m eeout1 eeout2 eeout3 -o merged_eeout

# Convert to VTK for visualization
um_post_op -vtk eeout -o mesh_data.vtk

# Extract specific edit
um_post_op -wse 14 eeout -o edit14.txt
```

**Migration to modern format:**
Use FMESH with OUT=xdmf instead - direct HDF5/XDMF output.
```

### Gap 2: inxc File Structure (Appendix D.9)

**What's Missing:**
- 128-column card format specification
- Cross-section editing output interpretation
- Parsing guidance

**Content to Add:**
```markdown
### inxc File Format (Cross-Section Editing Output)

**Purpose:** Output from inxc cross-section editing utility

**Format:** 128-column card-based format (fixed width)

**Structure:**
- Card 1: 80-character problem title
- Card 2: ncase, kplot, l_res
  - ncase: Number of double-differential XS edits
  - kplot: If nonzero, write to MCTAL
  - l_res: If nonzero, perform residual nuclei edit

For each case:
- Card 3: 128-character case title
- Card 4: nerg, nang, ntype, fnorm, imom, iyield
  - nerg: Energy bin boundaries
  - nang: Angle bin boundaries (cosine or degrees)
  - ntype: Particle types to tally
  - fnorm: Normalization factor
  - imom: If nonzero, momentum bins (MeV/c)
  - iyield: If nonzero, differential multiplicities

- Card 5: Energy/momentum bin boundaries
- Card 6: Angle bin boundaries
- Card 7: Particle type flags (Table D.22)

**Particle type flags:**
- 1 = neutron, 2 = photon, 3 = electron, 4 = positron
- 5 = proton, 6-11 = pions/muons/neutrinos
- -1 = elastic scattered projectile
- -2 = elastic recoil nucleus

**Parsing strategy:**
Use fixed-width field parsing for 128-column cards.
```

### Gap 3: HDF5 Hierarchy Script (Appendix D.8)

**What's Missing:**
- Bundled Python script for HDF5 structure exploration
- Usage examples
- Integration with parsing workflow

**Content to Add:**
1. Create `scripts/h5_dirtree.py` (complete script from D.8)
2. Add usage section:
```markdown
### HDF5 Structure Exploration

**Tool:** `scripts/h5_dirtree.py`

**Purpose:** Generate hierarchical tree view of HDF5 file structure

**Usage:**
```bash
python scripts/h5_dirtree.py runtpe.h5
python scripts/h5_dirtree.py runtpe.h5 --group /results
python scripts/h5_dirtree.py runtpe.h5 -g /particle_1
```

**Example output:**
```
/
  .2 config_control (group)
  .2 problem_info (group)
    .3 title (dataset)
    .3 nps (dataset)
  .2 results (group)
    .3 mesh_tally_14 (group)
      .4 energy_total (group)
        .5 time_total (group)
          .6 values (dataset)
          .6 errors (dataset)
```
```

### Gap 4: EEOUT Legacy Format (Appendix D.7)

**What's Missing:**
- Detailed EEOUT structure documentation
- Binary vs ASCII differences
- Deprecation guidance

**Content to Add:**
```markdown
### EEOUT Legacy Format (Deprecated)

**Status:** ⚠️ DEPRECATED in MCNP6.3+ (use HDF5 instead)

**Purpose:** Legacy unstructured mesh output format

**File types:**
- EEOUT: Binary format (default)
- EEOUT_ASCII: Text format (use `-bc` to convert)

**Structure:**
- Header: Problem info, mesh dimensions
- Geometry: Node coordinates, element connectivity
- Data: Tally values, errors per element
- Footer: Metadata, version info

**Why deprecated:**
- Non-portable binary format
- Limited visualization tool support
- Large file sizes
- No compression

**Migration path:**
1. Use FMESH with OUT=xdmf for new work
2. Convert legacy EEOUT to VTK: `um_post_op -vtk eeout -o mesh.vtk`
3. Import VTK to ParaView for visualization

**If you must parse EEOUT:**
- Use um_post_op utility for processing
- Binary format requires Fortran unformatted read
- ASCII format parseable but inefficient
```

---

## Scripts to Bundle

### Priority 1: Core Parsing Scripts (MUST CREATE)

#### 1. `scripts/mcnp_output_parser.py`
**Purpose:** Parse OUTP file for warnings, errors, tallies, statistics

**Key functions:**
- `parse_output(filepath)` → dict with header, tallies, warnings, errors
- `extract_warnings(filepath)` → list of warning messages
- `extract_errors(filepath)` → list of fatal errors
- `check_termination(filepath)` → bool (normal termination?)
- `extract_tally(filepath, tally_num)` → tally data dict
- `get_statistical_checks(filepath, tally_num)` → 10 checks dict

**Design:** Standalone, no external dependencies beyond stdlib

#### 2. `scripts/mcnp_hdf5_inspector.py`
**Purpose:** Inspect and navigate HDF5 output files

**Key functions:**
- `list_structure(h5_file, group='/')` → hierarchical tree
- `extract_mesh_tally(h5_file, tally_num)` → numpy arrays
- `extract_ptrac(h5_file, particle_num)` → trajectory data
- `get_attributes(h5_file, path)` → metadata dict
- `extract_fission_matrix(h5_file)` → CSR sparse matrix

**Dependencies:** h5py, numpy

#### 3. `scripts/ptrac_parser.py`
**Purpose:** Parse PTRAC ASCII or HDF5 files

**Key functions:**
- `parse_ptrac_hdf5(h5_file, particle_num)` → trajectory dict
- `filter_by_event(ptrac_data, event_type)` → filtered data
- `get_trajectory(ptrac_data, history_num)` → single history
- `export_to_csv(ptrac_data, output_file)`

**Dependencies:** h5py, numpy

### Priority 2: Utility Scripts

#### 4. `scripts/h5_dirtree.py`
**Purpose:** Visualize HDF5 file structure (from Appendix D.8)

**Complete script from documentation - already specified**

#### 5. `scripts/mctal_basic_parser.py`
**Purpose:** Basic MCTAL parsing for output-parser use

**Note:** Advanced MCTAL processing in mcnp-mctal-processor
**Key functions:**
- `parse_mctal_header(mctal_file)` → header dict
- `extract_tally_basic(mctal_file, tally_num)` → values, errors
- `list_tallies(mctal_file)` → list of tally numbers

**Design:** Lightweight, no advanced features (merging, export)

---

## MCNP Format Compliance

### Issues to Fix:

1. **Python code blocks:** Need proper comment lines
   - Add "c" comments for readability
   - Proper spacing

2. **MCNP input examples:** Ensure 2 blank lines for complete files

3. **Code snippets:** 0 blank lines

---

## Implementation Steps (Workflow 5-11)

### Step 5: Extract and Integrate Documentation Content
- Add um_post_op section (from E.11)
- Add inxc structure section (from D.9)
- Expand EEOUT section (from D.7)
- Reference Lesson #14 (use completed skills first)

### Step 6: Add Working Examples
- Complete end-to-end workflow examples
- OUTP parsing → data extraction → analysis
- HDF5 navigation → mesh extraction → array processing
- PTRAC parsing → trajectory analysis

### Step 7: Bundle Python Scripts (**CRITICAL**)
- Create all 5 scripts listed above
- Test each script standalone
- Add usage examples to SKILL.md
- Verify no external paths (`skills/output_analysis/`)

### Step 8: Streamline and Organize
- Consolidate redundant sections
- Improve flow and readability
- Add clear skill boundary explanations
- Update "Integration with Other Skills" section

### Step 9: Validate Against Checklist
- Run through 26-item quality checklist
- Verify YAML frontmatter
- Check bundled resources
- Validate format compliance
- Test all examples

### Step 10: Test All Examples
- Run Python scripts
- Verify output correctness
- Test edge cases (missing files, corrupted data)

### Step 11: Update Status
- Update PHASE-2-PROJECT-STATUS.md
- Mark mcnp-output-parser as complete
- Document lessons learned

---

## Token Budget Estimate

**Current file:** 1231 lines (~12k tokens to read)
**Documentation to add:** ~3k tokens
**Scripts to create:** ~5k tokens
**Revisions and testing:** ~2k tokens
**Total estimated:** ~22k tokens

**Buffer:** ~8k tokens for iteration
**Grand total:** ~30k tokens for complete mcnp-output-parser processing

---

## Success Criteria

✅ All 5 Python scripts bundled and functional
✅ No references to external paths (`skills/output_analysis/`)
✅ um_post_op documented (Appendix E.11)
✅ inxc structure documented (Appendix D.9)
✅ EEOUT legacy format documented (Appendix D.7)
✅ HDF5 hierarchy script bundled (Appendix D.8)
✅ Clear skill boundaries with other skills
✅ All examples MCNP format compliant
✅ 26-item checklist passes
✅ All examples tested and working

---

## Next Actions

1. ✅ COMPLETED: Gap analysis and integration plan
2. ⏭️ NEXT: Begin Step 5 (Extract and integrate documentation content)
3. After Step 5: Create Python scripts (Step 7 - CRITICAL)
4. After scripts: Streamline and validate (Steps 8-11)

---

**Plan Status:** ✅ COMPLETE - Ready for implementation
**Estimated completion:** Steps 5-11 (~30k tokens)
