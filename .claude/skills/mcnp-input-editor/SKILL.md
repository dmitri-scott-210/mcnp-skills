---
name: mcnp-input-editor
description: "Performs systematic editing of existing MCNP input files through find/replace operations, batch parameter updates, and selective card modifications while preserving file structure and formatting"
version: "3.0.0"
dependencies: "mcnp-input-builder, mcnp-input-validator"
---

# MCNP Input Editor

## Overview

The MCNP Input Editor skill provides systematic editing techniques for modifying existing MCNP input files without recreating them from scratch. It handles targeted modifications, batch updates, search-and-replace operations, and selective editing while preserving the critical three-block structure, formatting, and inline comments. This skill efficiently handles files of any size, from small test cases to large reactor models with 9,000+ lines, using appropriate editing strategies for each scale.

Editing existing inputs is essential for iterative design, parametric studies, error correction, and optimization workflows. This skill emphasizes safe editing practices that maintain MCNP input validity and provides both manual techniques and automated scripting approaches.

## When to Use This Skill

- Modifying existing MCNP input files without complete reconstruction
- Performing search-and-replace operations across cells, surfaces, or data cards
- Batch updating parameters (densities, importances, volumes, cross-section libraries)
- Correcting errors identified by validation or MCNP fatal checks
- Updating material compositions or ZAID library identifiers (.70c → .80c)
- Adjusting geometry dimensions systematically
- Converting between MCNP versions (MCNP5 → MCNP6)
- Applying systematic changes to large reactor models (>5,000 lines)
- Making incremental improvements to validated baseline inputs
- Implementing variance reduction adjustments based on run results

## Decision Tree

```
User needs to modify existing MCNP input
  |
  +--> What type of edit?
       |
       +--[Single Card]---------> Locate card by number
       |                         └─> Edit specific parameter
       |                             └─> Validate syntax (mcnp-input-validator)
       |
       +--[Multiple Cards]-------> Batch or selective?
       |                         |
       |                         +--[Few cards]---> Edit individually
       |                         +--[Many cards]---> Use search/replace or script
       |
       +--[Systematic Change]---> Apply pattern across file
       |                         ├─> Define search pattern (literal or regex)
       |                         ├─> Preview changes
       |                         └─> Apply replacements
       |
       +--[Large File (>5,000)]-> Use efficient method
                                 ├─> Build index (large_file_indexer.py)
                                 ├─> Stream processing
                                 └─> Avoid full file load
  |
  +--> After editing:
       ├─> Validate structure (mcnp-input-validator)
       ├─> Check blank lines preserved (exactly 2)
       ├─> Verify cross-references intact
       └─> Test run MCNP (short NPS recommended)
```

## Quick Reference

| Edit Type | Method | Tool/Technique | Example |
|-----------|--------|----------------|---------|
| Single cell density | Find & replace specific line | Manual or `input_editor.py` | `100  1  -1.0` → `100  1  -1.2` |
| Batch importance | Regex pattern | `batch_importance_editor.py` | All `IMP:N=2` → `IMP:N=1` |
| ZAID library conversion | Pattern replace | `library_converter.py` | `.70c` → `.80c` throughout file |
| Add cell parameter | Selective insertion | Script or manual | Add `VOL=1` to cells lacking it |
| Scale geometry | Dimension multiplication | Calculate + replace | Multiply all radii by 1.1 |
| Fix validation errors | Targeted corrections | Manual with validator feedback | Remove undefined surface refs |
| Large file (>9,000 lines) | Indexed editing | `large_file_indexer.py` | Edit cell 5000 without loading full file |
| **Multi-file batch edit** | **Consistent changes across files** | **`batch_multi_file_editor.py`** | **Update 13 cycle inputs simultaneously** |
| **Template vs. regenerate** | **Decision guidance** | **Template analysis** | **Edit template.i not 13 generated files** |
| **Lattice fill array** | **Dimension-preserving edits** | **`lattice_editor.py`** | **Replace universe 100→101 in 225-element array** |
| **Material batch update** | **Systematic material edits** | **`batch_material_editor.py`** | **Update 385 materials m9000-m9385** |

## Use Case 1: Edit Single Cell Density

**Scenario:** Change density of cell 100 from -1.0 to -1.2 g/cm³

**Original:**
```
100  1  -1.0  -10  11  -12  IMP:N=1  VOL=1000  $ Water cell
```

**Editing Methods:**

**Method A: Direct find/replace**
```
Find: "100  1  -1.0"
Replace: "100  1  -1.2"
```

**Method B: Using script**
```bash
python scripts/input_editor.py input.i --cell 100 --density -1.2
```

**Method C: Selective parsing**
1. Locate line containing cell 100
2. Parse fields: j=100, m=1, d=-1.0, geom="-10 11 -12", params="IMP:N=1 VOL=1000"
3. Modify density field: d=-1.2
4. Reconstruct line preserving spacing and comment

**Result:**
```
100  1  -1.2  -10  11  -12  IMP:N=1  VOL=1000  $ Water cell
```

**Key Points:**
- Preserve inline comment (after $)
- Maintain column alignment
- Verify density sign (negative = mass density in g/cm³)
- Validate after edit using mcnp-input-validator

---

## Use Case 2: Batch Change All Neutron Importances

**Scenario:** Set all neutron importances to 1 (remove splitting/roulette)

**Original (excerpt):**
```
1    1  -1.0   -1       IMP:N=1  IMP:P=1
2    2  -2.3   1  -2    IMP:N=2  IMP:P=1
3    3  -11.3  2  -3    IMP:N=4  IMP:P=1
4    0         3  -4    IMP:N=8  IMP:P=0
5    0         4        IMP:N=0  IMP:P=0  $ Graveyard
```

**Editing Steps:**

**1. Define regex pattern (exclude graveyard)**
```
Pattern: IMP:N=(?!0\b)[1-9]\d*
(Matches IMP:N= followed by non-zero number)
```

**2. Define replacement**
```
Replace: IMP:N=1
```

**3. Preview changes**
```bash
python scripts/batch_importance_editor.py input.i --set-all 1 --preview
```

**4. Apply**
```bash
python scripts/batch_importance_editor.py input.i --set-all 1
```

**Result:**
```
1    1  -1.0   -1       IMP:N=1  IMP:P=1
2    2  -2.3   1  -2    IMP:N=1  IMP:P=1
3    3  -11.3  2  -3    IMP:N=1  IMP:P=1
4    0         3  -4    IMP:N=1  IMP:P=0
5    0         4        IMP:N=0  IMP:P=0  $ Graveyard (unchanged)
```

**Key Points:**
- Always preview batch changes before applying
- Preserve `IMP:N=0` for graveyard cells (fatal if changed)
- Use negative lookahead `(?!0\b)` to exclude zero
- Verify change count matches expectations

**Alternative Method: Material-Based Importances**
```bash
# Set importances by material type
python scripts/batch_importance_editor.py input.i --by-material 1:1 2:2 10:4
# Water (mat 1) → IMP:N=1
# Concrete (mat 2) → IMP:N=2
# Fuel (mat 10) → IMP:N=4
```

---

## Use Case 3: Multi-File Batch Editing

**Scenario:** Update library from .70c to .80c across 13 cycle-specific inputs

### Decision Tree: Edit Multiple Files or Regenerate?

```
Need to change multiple generated inputs
  |
  +--> Is change in CSV data or template?
       |
       +--[CSV data]--------> Regenerate all inputs from template
       |                     (Don't edit 13 files individually!)
       |
       +--[Template]--------> Edit template → Regenerate all
       |
       +--[Neither]---------> Proceed with multi-file batch edit
                             |
                             +--> Same change in all files?
                                  |
                                  +--[Yes]---> Use batch script
                                  +--[No]----> Edit individually
```

### Example 1: Library Update Across All Cycle Inputs

**Situation**: Update ALL materials from .70c to .80c in 13 cycle files

**Approach**:
```bash
# 1. Backup files
git add mcnp/bench_*.i
git commit -m "Before library update"

# 2. Preview changes
python scripts/batch_multi_file_editor.py \
  --files "mcnp/bench_*.i" \
  --find ".70c" \
  --replace ".80c" \
  --preview

# Expected: ~385 materials × 13 files = 5,005 replacements

# 3. Apply if count is correct
python scripts/batch_multi_file_editor.py \
  --files "mcnp/bench_*.i" \
  --find ".70c" \
  --replace ".80c"

# 4. Validate ALL files after batch edit
for f in mcnp/bench_*.i; do
  python input_editor.py "$f" --validate
done

# 5. Test run one file with MCNP
mcnp6 i=bench_138B.i n=test. tasks 1
```

### Example 2: Fix Validation Error in Multiple Files

**Situation**: Validator finds "Surface 9999 referenced but not defined" in 6 files

**Approach**:
```bash
# 1. Identify affected files
for f in mcnp/bench_*.i; do
  grep -l "9999" "$f"
done

# 2. Option A: Remove references (if surface was mistake)
python scripts/batch_multi_file_editor.py \
  --files "mcnp/bench_138B.i mcnp/bench_139A.i ..." \
  --find "-9999" \
  --replace "" \
  --validate-after

# Option B: Add missing surface to all files
python scripts/batch_multi_file_editor.py \
  --files "mcnp/bench_*.i" \
  --insert-surface "9999 pz 100  $ Added missing plane"
```

### Best Practices for Multi-File Editing

1. **Always use version control** (git) before bulk edits
   ```bash
   git add mcnp/bench_*.i
   git commit -m "Before library update"
   ```

2. **Preview on ONE file first**
   ```bash
   # Test on single file
   python input_editor.py bench_138B.i --find "X" --replace "Y" --preview

   # If good, apply to all
   python batch_multi_file_editor.py --files "bench_*.i" --find "X" --replace "Y"
   ```

3. **Count expected changes**
   ```bash
   # If updating 385 materials in 13 files:
   # Expected: 385 × 13 = 5,005 changes
   # Actual count from preview should match
   ```

4. **Validate ALL files after batch edit**
   ```bash
   for f in mcnp/bench_*.i; do
     python input_editor.py "$f" --validate
   done
   ```

5. **Test run one file with MCNP**
   ```bash
   mcnp6 i=bench_138B.i n=test. tasks 1
   # Check for fatal errors before running all 13
   ```

**Key Points:**
- Multi-file editing is for changes NOT in CSV data or template
- If CSV or template changed, REGENERATE instead of editing
- Always preview, count changes, and validate
- Use git for safety and rollback capability

**See Also**: `multi_file_editing_guide.md` for comprehensive workflows and rollback procedures

---

## Use Case 4: Template-Based Input Management

**Scenario:** Decide whether to edit template, CSV data, or generated input files

### Understanding Template Workflows

Many reactor models use **template-based generation**:
```
Template (bench.template) + Data (CSV files) → Generated Inputs (bench_138B.i, ...)
```

**Key Principle**: Edit the SOURCE (template/CSV), not the OUTPUT (generated inputs)

### Decision Tree: Edit Template, CSV, or Generated Input?

```
Need to change parameter in generated input
  |
  +--> Is parameter in CSV data?
       |
       +--[Yes]------------> Edit CSV → Regenerate all
       |                    Examples: power, control positions, time steps
       |
       +--[No]----------+
                        |
                        +--> Is parameter in template?
                             |
                             +--[Yes, static]-----> Edit template → Regenerate all
                             |                     Examples: geometry, materials, physics cards
                             |
                             +--[Yes, variable]---> Check if template variable
                             |                     If {{variable}}, edit generation script
                             |
                             +--[No]-------------> Edit generated input directly
                                                   Examples: one-off corrections, experiments
```

### Example 1: Correcting CSV Data (REGENERATE)

**Situation**: Power value at timestep 312 was wrong in power.csv

**WRONG approach**:
```bash
# DON'T edit 13 files individually!
python input_editor.py bench_138B.i --find "power=23.45" --replace "power=23.78"
python input_editor.py bench_139A.i --find "power=24.12" --replace "power=24.35"
... (11 more files)
```

**RIGHT approach**:
```bash
# 1. Fix CSV data
vim power.csv  # Correct timestep 312: 23.45 → 23.78

# 2. Regenerate all inputs
python create_inputs.py

# 3. Validate first output
python input_editor.py bench_138B.i --validate
```

**Why**: CSV data drives generation. Editing generated files loses traceability.

### Example 2: Adding Control Drum Angle (EDIT TEMPLATE)

**Situation**: Need to add 130° position to control drum library

**WRONG approach**:
```bash
# DON'T manually edit all 13 generated files to add 130° surfaces!
```

**RIGHT approach**:
```python
# 1. Edit create_inputs.py
angles = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 130, 150]  # Added 130

# 2. Add surface definitions for 130°
ne_surfaces.append(surf_130deg)

# 3. Regenerate all inputs
python create_inputs.py
```

### Example 3: One-Time Experiment (EDIT DIRECTLY)

**Situation**: Test sensitivity with 3.2% enrichment (was 3.0%)

**Approach**:
```bash
# Edit single generated file for experiment
python input_editor.py bench_138B.i --find "92235.70c 0.030" --replace "92235.70c 0.032"

# Add note in file
c MANUAL EDIT 2025-11-08: Increased enrichment 3.0→3.2% for sensitivity test
c NOTE: This file modified AFTER generation, regenerating will overwrite!
```

### Identifying Template-Generated Inputs

**Clues that input was template-generated**:
1. Multiple similar files with systematic names (`bench_138B.i`, `bench_139A.i`, ...)
2. Presence of `.template` file in directory
3. Presence of generation script (`create_inputs.py`)
4. Presence of CSV data files (`power.csv`, `oscc.csv`)
5. Comment in input: `c Generated by create_inputs.py on 2025-11-07`

**If template-generated, DON'T edit individual outputs!**

### When Direct Editing is OK

**Edit generated input directly when**:
1. One-time experiment (testing sensitivity)
2. Quick fix for immediate run (will regenerate later)
3. Parameter not in template or CSV
4. Template/script no longer available
5. Change only affects ONE input, not all

**Always note in file if editing manually**:
```mcnp
c MANUAL EDIT 2025-11-08: Increased enrichment 3.0→3.2% for sensitivity test
c NOTE: This file modified AFTER generation, regenerating will overwrite!
m10  92235.70c 0.032  92238.70c 0.968  $ Was 0.030/0.970
```

**Key Points:**
- Template + CSV generates multiple related inputs
- Edit SOURCE (template/CSV), not OUTPUT (generated files)
- Only edit generated files for one-off experiments
- Document manual edits to prevent confusion

**See Also**: `template_editing_guide.md` for template anatomy, Jinja2 patterns, and troubleshooting

---

## Use Case 5: Editing Lattice Fill Arrays

**Scenario:** Replace universe 100 with 101 in lattice without breaking dimension constraints

### CRITICAL WARNING

Lattice fill arrays have **EXACT dimension requirements**:
```mcnp
fill=-7:7 -7:7 0:0  ← Requires (7-(-7)+1)×(7-(-7)+1)×(0-0+1) = 15×15×1 = 225 elements!
```

**If you edit the universe numbers, element count MUST stay exactly 225.**

### Scenario 1: Change One Universe in Pattern

**Task**: Replace universe 100 with 101 in position (i=0, j=0, k=0)

**Safe approach**:
```bash
# 1. Understand current layout
python scripts/lattice_analyzer.py input.i --cell 200

# Output shows:
#   Cell 200: LAT=1, fill=-7:7 -7:7 0:0 (225 elements)
#   Center position (i=0,j=0,k=0): Universe 100

# 2. Edit that specific universe number
python scripts/lattice_editor.py input.i --cell 200 \
  --lattice-edit i=0 j=0 k=0 --universe 101

# 3. Validate
python scripts/lattice_editor.py input.i --cell 200 --validate
```

**WRONG approach**:
```bash
# DON'T use simple find/replace on lattice!
# This could change the wrong 100!
python input_editor.py input.i --find "100" --replace "101"  # ← DANGEROUS!
```

### Scenario 2: Replace All of One Universe Type

**Task**: Change all universe 100 to universe 101 in lattice

**Safe approach**:
```bash
# Use lattice-aware replacement
python scripts/lattice_editor.py input.i --cell 200 --replace-universe 100 101

# This:
# 1. Parses fill array correctly
# 2. Preserves dimension (still 225 elements)
# 3. Only changes within this lattice cell
# 4. Validates element count after
```

### Scenario 3: Edit Repeat Notation

**Task**: Change compact lattice from 25 fuel layers to 27

**Original**:
```mcnp
fill=0:0 0:0 -15:15 100 2R 200 24R 100 2R
$ 3 + 25 + 3 = 31 elements for indices -15 to +15
```

**Modified**:
```mcnp
fill=0:0 0:0 -16:16 100 2R 200 26R 100 2R
$ 3 + 27 + 3 = 33 elements for indices -16 to +16
```

**Safe approach**:
```bash
# 1. Understand repeat notation
#    nR = n+1 copies
#    24R = 25 copies (NOT 24!)

# 2. Calculate new counts
#    Old: -15 to +15 = 31 positions
#    New: -16 to +16 = 33 positions
#    Added 2 positions → need 2 more universe 200

# 3. Edit
python scripts/lattice_editor.py input.i --cell 300 \
  --expand-k -15:15 -16:16 \
  --fill-pattern "100 2R 200 26R 100 2R"

# 4. Verify
#    3 + 27 + 3 = 33 ✓
```

### Validation After Lattice Edits

**Always check**:
1. **Element count matches dimensions**
   ```bash
   python scripts/lattice_editor.py input.i --cell 200 --validate
   # Checks: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1) = element count
   ```

2. **Repeat notation correct**
   ```python
   # Verify: "U nR" really gives n+1 copies
   # 100 2R = 3 copies ✓
   # 200 24R = 25 copies ✓
   ```

3. **Surface dimensions match**
   ```python
   # For LAT=1 (rectangular): RPP should contain N × pitch
   # For LAT=2 (hexagonal): RHP should contain N × (R×√3)
   ```

4. **All referenced universes exist**
   ```bash
   python mcnp-input-validator/cross_reference_checker.py input.i
   ```

### Common Lattice Editing Errors

| Error | Symptom | Fix |
|-------|---------|-----|
| **Element count mismatch** | Fatal: "Wrong number of entries in FILL card" | Recount elements, verify (IMAX-IMIN+1)×... |
| **Repeat off-by-one** | Wrong number of layers | Remember: nR = n+1 copies |
| **Surface too small** | Fatal: "Lattice element outside surface" | Resize RPP/RHP: N × pitch |
| **Universe not defined** | Fatal: "Universe U not found" | Define universe before use in fill |
| **Corrupted continuation** | Parse error | Verify & or 5-space indent on next line |

**Key Points:**
- Lattice dimensions are EXACT: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)
- Repeat notation: nR = n+1 copies (24R = 25 copies!)
- Use lattice_editor.py for safe editing
- Always validate dimension match after edits
- Works for both LAT=1 (rectangular) and LAT=2 (hexagonal)

**See Also**: `lattice_editor.py` script for dimension-preserving edits

---

## Use Case 6: Batch Material Updates

**Scenario:** Update 385 materials from .70c to .80c while preserving systematic numbering

### Preserving Systematic Numbering

**CRITICAL**: Many models use systematic material numbering

**Example from AGR-1**:
```
Material numbering scheme: m9XYZ
  9 = AGR experiment
  X = Capsule (1-6)
  Y = Stack (1-3)
  Z = Compact (1-4)

m9111 = Capsule 1, Stack 1, Compact 1
m9623 = Capsule 6, Stack 2, Compact 3
```

**When editing, preserve this numbering!**

### Example 1: Library Migration (385 Materials)

**Situation**: Update ALL materials from ENDF/B-VII.0 (.70c) to VIII.0 (.80c)

**Safe approach**:
```bash
# 1. Count materials to update
grep -c "\.70c" input.i
# Output: 385

# 2. Preview changes
python scripts/library_converter.py input.i --old 70c --new 80c --preview

# Output shows:
#   Material m1: 5 ZAIDs to update
#   Material m2: 8 ZAIDs to update
#   ...
#   Total: 385 materials, 2,340 ZAIDs

# 3. Apply if count looks right
python scripts/library_converter.py input.i --old 70c --new 80c

# 4. Validate
grep "\.70c" input.i  # Should return nothing
grep -c "\.80c" input.i  # Should be 2,340
```

### Example 2: Selective ZAID Update

**Situation**: Update only uranium isotopes to .80c, leave others as .70c

**Approach**:
```bash
python scripts/library_converter.py input.i \
  --old 70c --new 80c \
  --zaids 92234 92235 92236 92238 \
  --preview

# This updates only:
#   92234.70c → 92234.80c
#   92235.70c → 92235.80c
#   92236.70c → 92236.80c
#   92238.70c → 92238.80c
# Leaves other isotopes unchanged
```

### Example 3: Density Correction in Material Range

**Situation**: Graphite density should be 1.85 g/cm³ in materials m9040-m9094

**Approach**:
```bash
python scripts/batch_material_editor.py input.i \
  --materials "9040-9094" \
  --set-density -1.85 \
  --preview

# This:
# 1. Identifies materials m9040 through m9094
# 2. Changes density (negative mass density)
# 3. Preserves all isotopes and fractions
# 4. Validates density sign is correct
```

### Example 4: Add Missing MT Cards

**Situation**: Add graphite thermal scattering to 50 materials

**Approach**:
```bash
python scripts/batch_material_editor.py input.i \
  --materials "9040-9094" \
  --add-mt "grph.18t" \
  --preview

# This:
# 1. Finds all materials in range
# 2. Checks if MT card already exists
# 3. Adds: mt9040 grph.18t, mt9041 grph.18t, ..., mt9094 grph.18t
# 4. Validates S(α,β) library exists
```

### Validation After Material Updates

**Always check**:
1. **Material numbers unchanged**
   ```bash
   # Extract material numbers before and after
   grep "^m[0-9]" input_old.i | awk '{print $1}' | sort > mats_old.txt
   grep "^m[0-9]" input_new.i | awk '{print $1}' | sort > mats_new.txt
   diff mats_old.txt mats_new.txt  # Should be identical
   ```

2. **Fractions still sum to 1.0** (or correct stoichiometry)
   ```bash
   python scripts/validate_materials.py input.i --check-sums
   ```

3. **All ZAIDs exist in libraries**
   ```bash
   mcnp6 i=input.i tasks 1  # Quick run to check library
   # Look for: "Warning: ZAID XXXXX not found"
   ```

4. **MT cards match materials**
   ```bash
   python scripts/validate_materials.py input.i --check-mt
   # Verifies: mt9040 exists for m9040, etc.
   ```

### Material Editing Best Practices

1. **Always preserve material numbers**
   - Material numbers are often referenced elsewhere (cells, tallies)
   - Changing m100 → m101 breaks all cell cards using m100

2. **Update entire material definition**
   - Don't edit just one ZAID line in multi-line material
   - Edit complete material to maintain consistency

3. **Validate fractions**
   - Atom fractions should sum to 1.0 (or stoichiometric ratio for compounds)
   - Weight fractions should sum to 1.0 exactly

4. **Match MT card numbers**
   - mt100 must correspond to m100
   - mt9111 must correspond to m9111

5. **Document changes**
   ```mcnp
   c UPDATED 2025-11-08: All materials .70c → .80c (ENDF/B-VIII.0)
   m1  92235.80c 0.04  92238.80c 0.96  8016.80c 2.0  $ Was .70c
   ```

**Key Points:**
- Preserve systematic material numbering schemes
- Use library_converter.py for ZAID library updates
- Use batch_material_editor.py for density/MT card updates
- Always validate material numbers unchanged
- Check that fractions still sum correctly

**See Also**: `batch_material_editor.py` for density and MT card updates

---

## Core Concepts

### Input Structure Preservation

MCNP input files have strict three-block structure that **must** be maintained:

```
[Title Card]
c
[Cell Cards Block]
c
<EXACTLY ONE BLANK LINE>
c
[Surface Cards Block]
c
<EXACTLY ONE BLANK LINE>
c
[Data Cards Block]
c
```

**Critical Rules:**
- Exactly 2 blank lines total (after cells, after surfaces)
- Maintain card order within blocks
- Preserve inline comments ($ delimiter)
- Keep continuation lines valid (& or 5-space indent)

**Validation:**
```bash
# Count blank lines (must equal 2)
grep -c "^$" input.i

# Validate structure
python scripts/input_editor.py input.i --validate
```

### Selective vs. Batch Editing

**Selective Editing** (few changes):
- Modify specific cards by number
- Change individual parameters
- Targeted error fixes
- Use when: <10 changes, specific cards identified

**Batch Editing** (many changes):
- Apply same change to multiple cards
- Pattern-based replacements (regex)
- Systematic updates
- Use when: >10 similar changes, systematic modification

### Safe Editing Practices

**1. Always backup before editing**
```bash
cp input.i input_backup_$(date +%Y%m%d).i
```

**2. Preview changes before applying**
```bash
python scripts/input_editor.py input.i --find "X" --replace "Y" --preview
```

**3. Validate after editing**
```bash
python scripts/input_editor.py input.i --validate
# Or use mcnp-input-validator skill
```

**4. Test with short run**
```bash
mcnp6 i=input.i n=test. tasks 1
# Check for fatal errors and warnings
```

**5. Document changes**
```
c EDITED 2025-11-04: Changed U-235 enrichment 3.0% → 3.2%
M2  92235.80c  0.032  92238.80c  0.968  $ Was: 0.030 / 0.970
```

---

## Integration with Other Skills

### Typical Editing Workflow

```
1. mcnp-input-builder     → Create initial input
2. [Run MCNP]
3. [Analyze results]
4. Identify needed changes
5. THIS SKILL             → Make systematic edits
6. mcnp-input-validator   → Validate edited file
7. [Run MCNP again]
8. Repeat 4-7 until optimized
```

### Skill Connections

**mcnp-input-builder**
- Builder creates, Editor modifies
- Use builder for structure understanding
- Use editor for iterative refinement

**mcnp-input-validator**
- Always validate before and after edits
- Use validator feedback to guide corrections
- Workflow: Validate → Edit → Re-validate

**mcnp-geometry-editor**
- Geometry-editor handles complex geometric transformations
- Input-editor handles simple text-based changes
- Use geometry-editor for: rotations, transformations, scaling
- Use input-editor for: parameter updates, find/replace

**mcnp-material-builder**
- Material-builder creates compositions
- Input-editor updates ZAIDs and fractions
- Use material-builder to verify composition sums to 1.0

**mcnp-variance-reducer**
- VR analysis recommends importance changes
- Input-editor applies recommended changes
- Iterative workflow: Run → Analyze → Edit importances → Re-run

---

## References

### Bundled Resources

**Reference Documentation** (root skill directory):
- `detailed_examples.md` - Extended use cases 3-8 (library updates, geometry scaling, parameter addition, commenting, error fixing, large files)
- `error_catalog.md` - Common editing errors and troubleshooting (blank lines, continuation breaks, regex over-matching, comment corruption, card scrambling, whitespace issues)
- `regex_patterns_reference.md` - Regex patterns for MCNP editing (cell patterns, surface patterns, material patterns, parameter patterns, safe practices)
- `advanced_techniques.md` - Automation and integration (programmatic editing, version control, diff-based editing, conditional editing, stream processing)
- **`multi_file_editing_guide.md`** - Multi-file batch editing workflows, decision matrices, rollback procedures **(NEW v3.0)**
- **`template_editing_guide.md`** - Template-based input management, Jinja2 patterns, template anatomy, troubleshooting **(NEW v3.0)**

**Scripts** (`scripts/` directory):
- `input_editor.py` - General purpose editor (find/replace, cell edits, validation, statistics)
- `batch_importance_editor.py` - Importance management with graveyard protection
- `library_converter.py` - ZAID library conversion (.70c → .80c, etc.) with selective ZAID support
- `large_file_indexer.py` - Efficient editing for files >5,000 lines
- **`batch_multi_file_editor.py`** - Multi-file batch editing with preview, validation, and rollback **(NEW v3.0)**
- **`lattice_editor.py`** - Dimension-preserving lattice fill array editing (LAT=1 and LAT=2) **(NEW v3.0)**
- **`batch_material_editor.py`** - Batch material updates (density, MT cards) with numbering preservation **(NEW v3.0)**
- `README.md` - Script usage, workflows, examples

**Example Files** (`` directory):
- Examples demonstrating before/after editing operations
- Editing workflows and techniques

### External Documentation

**MCNP Manual References:**
- Chapter 4: Input File Description (structure requirements)
- Chapter 5: Input Cards (card syntax specifications)

**Related Skills:**
- mcnp-input-builder (creating inputs)
- mcnp-input-validator (validating edits)
- mcnp-geometry-editor (geometric transformations)
- mcnp-material-builder (material compositions)
- mcnp-variance-reducer (importance optimization)

---

## Best Practices

1. **Always backup before editing** - Use dated backups or version control (git)

2. **Preview batch changes** - Use `--preview` flag to see effects before applying

3. **Edit incrementally** - Make small changes, test, repeat (not 50 changes at once)

4. **Validate after every edit** - Structure check, cross-reference validation, syntax verification

5. **Preserve comments** - Comments document intent; update them when editing related cards

6. **Use appropriate tools** - Manual for 1-5 edits, scripts for >10 edits, indexing for large files

7. **Test with short runs** - Quick MCNP run (low NPS) to catch fatal errors early

8. **Document all changes** - Inline comments, change log file, or git commit messages

9. **Maintain formatting** - Consistent spacing, column alignment improves readability

10. **Know when to rebuild** - If edits become too complex, use mcnp-input-builder to recreate cleanly

---

**END OF SKILL**
