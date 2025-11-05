---
name: mcnp-input-editor
description: "Performs systematic editing of existing MCNP input files through find/replace operations, batch parameter updates, and selective card modifications while preserving file structure and formatting"
version: "2.0.0"
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

**Scripts** (`scripts/` directory):
- `input_editor.py` - General purpose editor (find/replace, cell edits, validation, statistics)
- `batch_importance_editor.py` - Importance management with graveyard protection
- `library_converter.py` - ZAID library conversion (.70c → .80c, etc.)
- `large_file_indexer.py` - Efficient editing for files >5,000 lines
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
