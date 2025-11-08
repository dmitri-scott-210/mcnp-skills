---
category: B
name: mcnp-input-editor
description: Edit existing MCNP input files with search/replace, batch modifications, and selective updates while preserving formatting
activation_keywords:
  - edit input
  - modify input
  - change input
  - update input
  - search replace
  - batch edit
  - input modification
  - edit cells
  - edit materials
---

# MCNP Input Editor Skill

## Purpose

This skill guides users in editing existing MCNP input files through targeted modifications, search and replace operations, batch updates, and selective editing while preserving file structure, formatting, and comments. It handles files of any size efficiently, including large reactor models with 9,000+ lines.

## When to Use This Skill

- Modifying existing MCNP input files without recreating from scratch
- Performing search and replace operations across cells, surfaces, or data cards
- Batch updating parameters (e.g., change all densities, all importances)
- Correcting errors in existing input files
- Updating material compositions or cross-section libraries
- Adjusting geometry dimensions systematically
- Converting between MCNP versions (MCNP5 → MCNP6)
- Applying systematic changes to large reactor models
- Preserving comments and formatting while making targeted edits
- Making incremental improvements to validated inputs

## Prerequisites

- **mcnp-input-builder**: Understanding of MCNP input structure
- **mcnp-input-validator**: Ability to validate edits
- Basic text editing concepts (search, replace, regex)
- Understanding of MCNP card syntax

## Core Concepts

### Input File Structure Preservation

**Critical Rule**: MCNP input files have strict structure that must be maintained

**Three-Block Structure**:
```
[Message Block]
<blank line>
[Cell Cards Block]
<blank line>
[Surface and Data Cards Block]
<blank line>
```

**Editing Constraints**:
- Must preserve blank line separators
- Must maintain card order within blocks
- Comments (C, $) should be preserved
- Continuation lines (&) must remain valid
- Column formatting should be preserved where possible

### Selective vs Batch Editing

**Selective Editing**:
- Modify specific cards by number (e.g., cell 100, surface 5)
- Change individual parameters
- Targeted fixes
- Use when: Small number of changes, specific cards identified

**Batch Editing**:
- Apply same change to multiple cards
- Pattern-based replacements
- Systematic updates
- Use when: Many similar changes, systematic modifications

### Search and Replace Patterns

**Literal Search**:
```
Find: "IMP:N=1"
Replace: "IMP:N=2"
```

**Regular Expression Search**:
```
Find: "IMP:N=\d+"
Replace: "IMP:N=1"
(Changes all neutron importances to 1)
```

**Card-Type Specific**:
```
Find in cell cards only: density values
Find in M cards only: ZAID numbers
```

### Large File Handling

**Challenge**: Files with 9,000+ lines (e.g., full reactor cores)

**Strategies**:
1. **Index-based editing**: Locate card by number, edit only that section
2. **Stream processing**: Read/write in chunks, don't load entire file
3. **Targeted extraction**: Pull specific section, edit, reinsert
4. **Line-range editing**: Edit lines N to M without touching rest

**Performance Targets**:
- Parse 10,000-line file: < 5 seconds
- Single card edit: < 1 second
- Batch edit (100 cards): < 5 seconds

### Change Tracking

**Best Practice**: Document all changes made

**Methods**:
1. **Comment additions**: Add inline comments describing changes
2. **Change log**: Maintain separate file listing modifications
3. **Version control**: Use git or similar for tracking
4. **Backup**: Always create backup before editing

**Example**:
```
c MODIFIED 2025-10-31: Changed U-235 enrichment from 3% to 3.2%
M1  92235  0.032  92238  0.968  $ Was: 0.03 / 0.97
```

---

## Decision Tree: Input Editing Workflow

```
START: Need to edit existing MCNP input
  |
  +--> What type of edit?
       |
       +--[Single Card]---------> Locate card by number
       |                         └─> Edit specific parameter
       |                             └─> Validate syntax
       |
       +--[Multiple Cards]-------> Batch or selective?
       |                         |
       |                         +--[Selective (few)]---> Edit each individually
       |                         +--[Batch (many)]------> Use search/replace
       |
       +--[Systematic Change]---> Apply pattern across file
       |                         ├─> Search for pattern
       |                         ├─> Preview changes
       |                         └─> Apply replacements
       |
       +--[Large File]----------> Use efficient method
                                 ├─> Index card locations
                                 ├─> Stream processing
                                 └─> Avoid full file load
  |
  +--> After editing:
       ├─> Validate syntax (mcnp-input-validator)
       ├─> Check block structure intact
       ├─> Verify blank lines preserved
       └─> Test run MCNP (optional but recommended)
```

---

## Use Case 1: Edit Single Cell Density

**Scenario**: Change density of cell 100 from -1.0 to -1.2 g/cm³

**Original Input**:
```
100  1  -1.0  -10  11  -12  IMP:N=1  VOL=1000  $ Water cell
```

**Editing Steps**:

1. **Locate the cell**:
```
Search for: "^100\s+"
(Finds line starting with "100" followed by whitespace)
```

2. **Identify density field**:
```
Current: 100  1  -1.0  -10...
Position:    ^cell ^mat ^density
```

3. **Make replacement**:
```
Find: "100  1  -1.0"
Replace: "100  1  -1.2"
```

4. **Verify result**:
```
100  1  -1.2  -10  11  -12  IMP:N=1  VOL=1000  $ Water cell
```

**Alternative Method (Selective)**:
```
1. Read line containing cell 100
2. Parse fields: j=100, m=1, d=-1.0, geom="-10 11 -12", params="IMP:N=1 VOL=1000"
3. Modify: d=-1.2
4. Reconstruct: "100  1  -1.2  -10  11  -12  IMP:N=1  VOL=1000"
5. Write back to file
```

**Key Points**:
- Preserve spacing and alignment
- Keep comment intact
- Maintain card parameters unchanged
- Validate density value (negative = atomic density)

---

## Use Case 2: Batch Change All Neutron Importances

**Scenario**: Set all neutron importances to 1 (remove splitting)

**Original Input** (excerpt):
```
1    1  -1.0   -1       IMP:N=1  IMP:P=1
2    2  -2.3   1  -2    IMP:N=2  IMP:P=1
3    3  -11.3  2  -3    IMP:N=4  IMP:P=1
4    0         3  -4    IMP:N=8  IMP:P=0
5    0         4        IMP:N=0  IMP:P=0
```

**Editing Steps**:

1. **Define search pattern (regex)**:
```
Pattern: IMP:N=\d+
(Matches "IMP:N=" followed by one or more digits)
```

2. **Define replacement**:
```
Replace: IMP:N=1
```

3. **Preview changes** (show what will change):
```
Line 1: IMP:N=1 → IMP:N=1 (no change)
Line 2: IMP:N=2 → IMP:N=1 ✓
Line 3: IMP:N=4 → IMP:N=1 ✓
Line 4: IMP:N=8 → IMP:N=1 ✓
Line 5: IMP:N=0 → IMP:N=1 ✗ (graveyard, should stay 0)
```

4. **Refine pattern to exclude IMP:N=0**:
```
Pattern: IMP:N=[1-9]\d*
(Matches IMP:N= followed by non-zero number)
```

5. **Apply replacement**:
```
1    1  -1.0   -1       IMP:N=1  IMP:P=1
2    2  -2.3   1  -2    IMP:N=1  IMP:P=1
3    3  -11.3  2  -3    IMP:N=1  IMP:P=1
4    0         3  -4    IMP:N=1  IMP:P=0
5    0         4        IMP:N=0  IMP:P=0  ✓ (unchanged)
```

**Key Points**:
- Always preview batch changes before applying
- Be careful with regex to avoid unintended matches
- Preserve IMP:N=0 for graveyard cells
- Consider using negative lookahead: `IMP:N=(?!0\b)\d+`

---

## Use Case 3: Update Material ZAIDs (Library Change)

**Scenario**: Change all ZAIDs from .70c to .80c (ENDF/B-VII to ENDF/B-VIII)

**Original Input**:
```
M1   1001.70c  2   8016.70c  1        $ Water
MT1  LWTR.01T
M2   92235.70c  0.03  92238.70c  0.97  $ LEU fuel
M3   6000.70c  1.0                     $ Graphite
MT3  GRPH.01T
```

**Editing Steps**:

1. **Search for pattern**:
```
Pattern: \.70c
(Matches ".70c" library identifier)
```

2. **Replace**:
```
Replace: .80c
```

3. **Apply to all M cards**:
```
M1   1001.80c  2   8016.80c  1        $ Water
MT1  LWTR.01T
M2   92235.80c  0.03  92238.80c  0.97  $ LEU fuel
M3   6000.80c  1.0                     $ Graphite
MT3  GRPH.01T
```

4. **Verify thermal scattering libraries**:
```
Check that LWTR.01T and GRPH.01T are compatible with .80c data
(May need to update to LWTR.20T if temperature differs)
```

**Advanced: Selective by Isotope**:
```
Change only U-235 and U-238:
Pattern: 9223[58]\.\d+c
Replace: Match found → check digit → 92235.80c or 92238.80c
```

**Key Points**:
- Batch library changes are common
- Verify cross-section library availability (check xsdir)
- Update MT cards if thermal library versions changed
- Test with short run to ensure libraries load correctly

---

## Use Case 4: Scale Geometry (Change Dimensions)

**Scenario**: Scale entire geometry by factor of 1.1 (10% larger)

**Original Input**:
```
c Surface Cards
1    SO   10.0                  $ Inner sphere R=10 cm
2    SO   20.0                  $ Outer sphere R=20 cm
3    PZ   0.0                   $ Bottom plane
4    PZ   50.0                  $ Top plane
5    CZ   5.0                   $ Cylinder R=5 cm
```

**Editing Steps**:

1. **Manual method** (small number of surfaces):
```
For each surface:
- Identify dimension parameters
- Multiply by 1.1
- Update value

Results:
1    SO   11.0                  $ Inner sphere R=11 cm
2    SO   22.0                  $ Outer sphere R=22 cm
3    PZ   0.0                   $ Bottom plane (unchanged)
4    PZ   55.0                  $ Top plane
5    CZ   5.5                   $ Cylinder R=5.5 cm
```

2. **Automated method** (many surfaces):
```
For surfaces with numeric parameters:
a. Parse surface type (SO, PZ, CZ, etc.)
b. Extract numeric values
c. Apply scale factor (except origin points for some types)
d. Reconstruct surface card

Caution: Some values should NOT be scaled:
- Plane coefficients (A, B, C in P card)
- Direction cosines (GQ coefficients)
- Origin coordinates (sometimes)
```

3. **Add documentation**:
```
c Surface Cards
c SCALED by 1.1 from original geometry (2025-10-31)
1    SO   11.0                  $ Inner sphere R=11 cm (was 10.0)
2    SO   22.0                  $ Outer sphere R=22 cm (was 20.0)
```

**Key Points**:
- Geometry scaling is complex (not all parameters scale equally)
- Consider using TR transformations instead for uniform scaling
- Document original dimensions in comments
- Verify with MCNP plot after scaling
- Check for lost particles in test run

---

## Use Case 5: Add Parameter to All Cells

**Scenario**: Add VOL parameter to all cells that don't have it

**Original Input**:
```
1    1  -1.0   -1       IMP:N=1
2    2  -2.3   1  -2    IMP:N=1  VOL=500
3    3  -11.3  2  -3    IMP:N=1
4    0         3        IMP:N=0
```

**Editing Steps**:

1. **Identify cells without VOL**:
```
Search for cell cards NOT containing "VOL="
Regex: ^(\d+\s+\d+\s+-?[\d.eE+-]+\s+.*?)(\s+IMP:)
(Captures cell card up to IMP, checks no VOL present)
```

2. **Insert VOL parameter** (method depends on volume):
```
Option 1: Add VOL=1 (placeholder, MCNP will calculate):
1    1  -1.0   -1       IMP:N=1  VOL=1
3    3  -11.3  2  -3    IMP:N=1  VOL=1

Option 2: Calculate actual volumes and insert:
(Requires geometry analysis or MCNP PRINT card output)
```

3. **Alternative: Add as separate VOL card**:
```
c Cell Cards (unchanged)
1    1  -1.0   -1       IMP:N=1
2    2  -2.3   1  -2    IMP:N=1
3    3  -11.3  2  -3    IMP:N=1
4    0         3        IMP:N=0

<blank line>

c Surface Cards
...

c Data Cards
VOL  1000  500  800  NO    $ Volumes for cells 1-4
```

**Key Points**:
- VOL parameter can be on cell card OR separate VOL data card
- VOL=1 tells MCNP to calculate (may be slow for complex cells)
- Actual volumes improve F4 tally normalization
- Void cells (m=0) don't need VOL
- Use MCNP PRINT card to extract calculated volumes

---

## Use Case 6: Comment All Cells (Documentation)

**Scenario**: Add descriptive inline comments to all cell cards

**Original Input**:
```
1    1  -1.0   -1
2    2  -2.3   1  -2
3    3  -11.3  2  -3
4    0         3  -4
5    0         4
```

**Editing Steps**:

1. **Add material-based comments**:
```
1    1  -1.0   -1       $ Water (material 1)
2    2  -2.3   1  -2    $ Concrete (material 2)
3    3  -11.3  2  -3    $ Lead (material 3)
4    0         3  -4    $ Air gap (void)
5    0         4        $ Graveyard (outside world)
```

2. **Add geometric description**:
```
1    1  -1.0   -1       IMP:N=1  $ Inner sphere (R<10 cm)
2    2  -2.3   1  -2    IMP:N=1  $ Shell 1 (10<R<20 cm)
3    3  -11.3  2  -3    IMP:N=1  $ Shell 2 (20<R<30 cm)
4    0         3  -4    IMP:N=1  $ Outer void (30<R<40 cm)
5    0         4        IMP:N=0  $ Graveyard (R>40 cm)
```

3. **Automated comment generation**:
```
For each cell:
- Parse material number m
- Look up material name from M cards
- Parse geometry (surfaces, boolean ops)
- Generate descriptive comment
- Append with $ delimiter
```

**Key Points**:
- Comments start with $ (inline) or C (full line)
- Keep comments concise (<40 characters)
- Document special features (importances, fills, transformations)
- Update comments when editing geometry or materials
- Consistent format improves readability

---

## Use Case 7: Fix Common Errors in Batch

**Scenario**: Fix multiple common errors identified by mcnp-input-validator

**Error List**:
```
1. Duplicate cell numbers: 150, 151 (both exist twice)
2. Undefined surface 999 referenced in cell 200
3. Material 15 not defined but used in cell 300
4. Missing IMP:N parameter in cells 400-410
```

**Editing Steps**:

**Fix 1: Renumber duplicate cells**:
```
Find: ^150\s+
Replace: 1500  (for second occurrence)

Find: ^151\s+
Replace: 1510  (for second occurrence)
```

**Fix 2: Remove invalid surface reference**:
```
Find cell 200:
Original: 200  5  -1.0  -10  11  999  IMP:N=1
Issue: Surface 999 doesn't exist

Options:
a. Remove 999: 200  5  -1.0  -10  11  IMP:N=1
b. Replace with valid surface: 200  5  -1.0  -10  11  -12  IMP:N=1
c. Create surface 999 (if intended)
```

**Fix 3: Add missing material**:
```
Option 1: Define material 15
M15  1001  2  8016  1  $ Water (add to data cards)

Option 2: Change cell to use existing material
Cell 300: M=15 → M=1 (if material 1 is water)
```

**Fix 4: Add IMP:N to cells 400-410**:
```
Method 1: Individual edits
400  ...  → 400  ...  IMP:N=1
401  ...  → 401  ...  IMP:N=1
...

Method 2: Regex batch
Find: ^(40\d)\s+(\d+\s+-?[\d.eE+-]+\s+.*?)$
Replace: $1  $2  IMP:N=1
(Adds IMP:N=1 to end of cells 400-409)
```

**Key Points**:
- Address errors in order of severity (fatal first)
- Validate after each fix
- Document what was changed and why
- Re-run validator to confirm all errors resolved
- Test with short MCNP run

---

## Use Case 8: Large File Editing (9,000+ Lines)

**Scenario**: Edit specific cell in 9,000-line reactor model without loading entire file

**Challenge**: Full file load is slow, memory-intensive

**Solution: Indexed Editing**

**Step 1: Build Index**:
```
Scan file once to create index:
Line 1-50: Message block
Line 51: Blank
Line 52-4500: Cell cards
  Cell 1: Line 52
  Cell 100: Line 151
  Cell 500: Line 551
  ...
Line 4501: Blank
Line 4502-5200: Surface cards
Line 5201: Blank
Line 5202-9000: Data cards
```

**Step 2: Targeted Edit**:
```
Task: Edit cell 500 (line 551)

1. Seek to line 551
2. Read line
3. Make edit
4. Write back to line 551
5. Done (never loaded full file)
```

**Step 3: Batch Edit in Chunks**:
```
Task: Change all IMP:N=2 to IMP:N=1 in cells

1. Load cell block index (lines 52-4500)
2. Process in chunks of 100 lines
3. For each chunk:
   - Load 100 lines
   - Apply edits
   - Write back
   - Free memory
4. Repeat until done
```

**Implementation**:
```python
def edit_large_file(filename, cell_num, new_density):
    # Build index
    index = build_cell_index(filename)

    # Find cell line
    line_num = index[cell_num]

    # Read/edit/write single line
    with open(filename, 'r+') as f:
        f.seek_line(line_num)  # Seek to specific line
        line = f.readline()
        edited_line = edit_density(line, new_density)
        f.seek_line(line_num)  # Seek back
        f.write(edited_line)
```

**Key Points**:
- Index once, edit many times
- Stream processing for batch edits
- Don't load full file into memory
- Performance: < 1s for single edit, < 10s for 1000 edits
- Critical for large reactor models (HFIR, full PWR core, etc.)

---

## Common Errors and Troubleshooting

### Error 1: "Blank line separator lost"

**Symptom**: After editing, MCNP reports "bad trouble" due to missing blank lines

**Cause**: Edit removed or corrupted blank line between blocks

**Fix**:
```
Verify structure:
[Cell cards]
<BLANK LINE - CRITICAL>
[Surface cards]
<BLANK LINE - CRITICAL>
[Data cards]
<BLANK LINE - END>

Restore blank lines if missing:
c Last cell card
1000  0  999  IMP:N=0

<--- ENSURE BLANK LINE HERE

c First surface card
1  SO  10.0
```

**Prevention**: When editing, preserve empty lines or explicitly check for them

---

### Error 2: "Continuation line broken"

**Symptom**: Long card no longer continues correctly

**Original**:
```
F4:N  1 2 3 4 5 6 7 8 9 10 &
      11 12 13 14 15
```

**Broken after edit**:
```
F4:N  1 2 3 4 5 6 7 8 9 10
      11 12 13 14 15
(Missing & at end of line 1)
```

**Fix**:
```
Re-add continuation character:
F4:N  1 2 3 4 5 6 7 8 9 10 &
      11 12 13 14 15
```

**Prevention**: When editing multi-line cards, preserve & or 5-space indent

---

### Error 3: "Regex replaced too much"

**Symptom**: Search/replace changed unintended text

**Example**:
```
Intended: Change cell 1 density
Regex: 1\s+-1.0
Problem: Also matches cell 10, 100, 1000, etc.

Result:
Cell 1: 1  -1.2  -1  (correct)
Cell 10: 10  -1.2  -1  (wrong! was -2.0)
Cell 100: 100  -1.2  -1  (wrong! was -5.0)
```

**Fix**: Use more specific regex
```
Correct regex: ^1\s+\d+\s+-1\.0
(^ = start of line, ensures exact cell 1)
```

**Prevention**:
- Always preview batch edits before applying
- Test regex on small sample first
- Use anchors (^, $, \b) for exact matches

---

### Error 4: "Comment accidentally edited"

**Symptom**: Comment text was modified, breaking meaning

**Example**:
```
Original:
1  1  -1.0  -1  $ Water density = 1.0 g/cm³

After batch "1.0 → 1.2" replacement:
1  1  -1.2  -1  $ Water density = 1.2 g/cm³
                  (comment incorrectly auto-updated)
```

**Fix**: Exclude comments from search
```
Regex to match density but not in comments:
^(\d+\s+\d+\s+)(-1\.0)(\s+-\d+.*?)(\$|$)
         Group 1    ^density  ^geom     ^stop before $

Replace: $1-1.2$3$4
```

**Prevention**: Use regex groups to preserve comments explicitly

---

### Error 5: "Card order scrambled"

**Symptom**: After editing, cards are out of order

**Cause**: Edit operation resorted or moved lines

**Fix**:
```
Cell cards MUST remain in cell block (lines 52-4500)
Surface cards MUST remain in surface block (lines 4502-5200)
Data cards MUST remain in data block (lines 5202-9000)

If scrambled, manually restore:
1. Extract all cell cards → sort by cell number → place in block 1
2. Extract all surface cards → sort by surface number → place in block 2
3. Extract all data cards → preserve order → place in block 3
```

**Prevention**: Edit in-place, don't move cards between blocks

---

### Error 6: "Whitespace issues after edit"

**Symptom**: Extra spaces, tabs, or missing spaces cause parsing errors

**Common Issues**:
```
Issue 1: Tab characters (MCNP treats as single space)
100  1  -1.0\t-10  → Invalid (tab breaks spacing)

Issue 2: Multiple spaces collapsed
100  1  -1.0   -10  → 100 1 -1.0 -10  (wrong alignment)

Issue 3: Missing space
IMP:N=1IMP:P=1 → Should be: IMP:N=1  IMP:P=1
```

**Fix**:
```
Standardize whitespace:
- Convert tabs to spaces (set editor to spaces, not tabs)
- Preserve alignment (column-based)
- Ensure space between parameters
```

**Prevention**: Configure editor:
- Use spaces, not tabs
- Show whitespace characters
- Set consistent indentation (2 or 4 spaces)

---

## Integration with Other Skills

### 1. **mcnp-input-validator**
How it integrates: Validates edits before and after modifications

**Workflow**:
```
1. mcnp-input-validator → Validate original file (baseline)
2. THIS SKILL → Make edits
3. mcnp-input-validator → Validate edited file (check for new errors)
4. If errors: THIS SKILL → Fix issues
5. Repeat until validated
```

**Example**:
```
validator: "Cell 100 references undefined surface 999"
THIS SKILL: Remove surface 999 from cell 100 geometry
validator: "No errors found" ✓
```

---

### 2. **mcnp-input-builder**
How it integrates: Builder creates, Editor modifies

**Workflow**:
```
1. mcnp-input-builder → Create initial input
2. Run MCNP
3. Analyze results
4. THIS SKILL → Adjust parameters based on results
5. Repeat until optimized
```

**Example**:
```
builder: Create geometry with estimated dimensions
Run: keff = 0.95 (too low)
THIS SKILL: Increase U-235 enrichment from 3% to 3.2%
Run: keff = 1.00 ✓
```

---

### 3. **mcnp-geometry-editor**
How it integrates: Specialized geometry editing, this is general editing

**Workflow**:
```
THIS SKILL: General text editing, search/replace
mcnp-geometry-editor: Geometry-aware editing (transformations, scaling, rotations)

Use THIS SKILL for: Simple text changes
Use geometry-editor for: Complex geometric transformations
```

---

### 4. **mcnp-material-builder**
How it integrates: Builder creates materials, Editor updates them

**Workflow**:
```
1. mcnp-material-builder → Create material definitions
2. THIS SKILL → Update ZAID libraries, adjust fractions
3. mcnp-material-builder → Verify composition sums to 1.0
```

---

### 5. **mcnp-variance-reducer**
How it integrates: Variance reduction requires iterative editing

**Workflow**:
```
1. Run initial calculation
2. mcnp-variance-reducer → Analyze, recommend IMP changes
3. THIS SKILL → Apply recommended importance changes
4. Re-run, evaluate FOM
5. Repeat until optimized
```

---

### Typical Workflow: Iterative Input Improvement

```
1. mcnp-input-builder     → Create initial input
2. mcnp-input-validator   → Validate syntax
3. [Run MCNP]
4. [Analyze results]
5. Identify needed changes (e.g., geometry, materials, VR)
6. THIS SKILL             → Make edits
7. mcnp-input-validator   → Re-validate
8. [Run MCNP again]
9. Repeat steps 5-8 until satisfied
10. DONE ✓
```

---

## Validation Checklist

After editing, verify:

### File Structure
- [ ] Three blocks intact (Message, Cells, Surfaces+Data)
- [ ] Blank lines preserved between blocks
- [ ] No stray text outside blocks
- [ ] Last line is blank

### Card Syntax
- [ ] All cell cards have valid format (j m d geom params)
- [ ] All surface cards have valid format (j type params)
- [ ] Continuation lines intact (& or 5-space indent)
- [ ] Comments preserved ($ inline, C full-line)

### References
- [ ] All surface numbers in cells exist as surface cards
- [ ] All material numbers in cells exist as M cards
- [ ] All transformation numbers (TRCL, TR) are defined
- [ ] All universe numbers (U, FILL) are consistent

### Edits Applied Correctly
- [ ] Intended changes present
- [ ] No unintended changes
- [ ] Numerical values reasonable (no typos)
- [ ] Units correct (cm, MeV, g/cm³)

### Testing
- [ ] Run mcnp-input-validator (no errors)
- [ ] Test run MCNP (short NPS) to verify runs
- [ ] Check output for warnings related to edits
- [ ] Compare results to baseline (if applicable)

---

## Advanced Topics

### 1. Programmatic Editing (Scripting)

**Python Script Example**:
```python
def batch_change_importances(input_file, old_val, new_val):
    """Change all IMP:N=old_val to IMP:N=new_val"""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    modified = []
    for line in lines:
        if f'IMP:N={old_val}' in line and old_val != 0:
            line = line.replace(f'IMP:N={old_val}', f'IMP:N={new_val}')
        modified.append(line)

    with open(input_file, 'w') as f:
        f.writelines(modified)

    print(f"Batch edit complete: IMP:N={old_val} → IMP:N={new_val}")

# Usage
batch_change_importances('input.i', 2, 1)
```

---

### 2. Version Control Integration

**Git Workflow**:
```bash
# Before editing
git add input.i
git commit -m "Baseline input v1.0"

# Make edits
[edit input.i]

# Check changes
git diff input.i

# Commit edits
git add input.i
git commit -m "Increased U-235 enrichment to 3.2% for criticality"

# Revert if needed
git checkout input.i  # Undo all changes
git revert HEAD       # Undo last commit
```

---

### 3. Diff-Based Editing

**Generate Edit Patch**:
```bash
# Create patch file
diff -u original.i edited.i > changes.patch

# Apply patch to another file
patch new_file.i < changes.patch
```

**Use Case**: Apply same edits to multiple similar files

---

### 4. Conditional Editing

**Edit Based on Conditions**:
```
IF cell material = 1 (water):
    Set IMP:N=1
ELSE IF cell material = 2 (concrete):
    Set IMP:N=2
ELSE IF cell material = 3 (lead):
    Set IMP:N=4
```

**Implementation**: Parse material number, apply logic, edit accordingly

---

## Best Practices

### 1. **Always Backup Before Editing**
```bash
cp input.i input.i.backup
# Or with timestamp
cp input.i input.i.$(date +%Y%m%d_%H%M%S)
```

### 2. **Preview Before Batch Edits**
```
Step 1: Show what will change (dry run)
Step 2: Review changes
Step 3: Apply only if confirmed correct
```

### 3. **Edit Incrementally**
```
Bad: Make 50 changes at once, test
Good: Make 5 changes, test, repeat 10 times
```

### 4. **Document All Changes**
```
Add comments:
c EDITED 2025-10-31: Changed enrichment 3.0% → 3.2%
c EDITED 2025-10-31: Updated all ZAIDs from .70c to .80c
```

### 5. **Use Consistent Formatting**
```
Align columns:
1    1  -1.0   -1       IMP:N=1  VOL=100
10   2  -2.3   1  -2    IMP:N=1  VOL=200
100  3  -11.3  2  -3    IMP:N=1  VOL=300
```

### 6. **Test After Each Major Edit**
```
1. Edit
2. Validate (mcnp-input-validator)
3. Test run (short NPS)
4. If OK, continue; if not, revert and fix
```

### 7. **Keep Change Log**
```
Separate file: input_changelog.txt

2025-10-31 10:00: Increased U-235 enrichment to 3.2%
2025-10-31 10:15: Changed all ZAIDs .70c → .80c
2025-10-31 11:00: Added VOL parameters to cells 1-100
```

### 8. **Use Version Numbering**
```
input_v1.0.i  (baseline)
input_v1.1.i  (enrichment change)
input_v1.2.i  (library update)
input_v2.0.i  (major geometry revision)
```

### 9. **Programmatic Input Editing**

For automated input file modifications and batch editing, see: `mcnp_input_editor.py`

This tool is useful for:
- Systematic parameter updates across multiple inputs
- Automated card replacements and modifications
- Scripted editing workflows for parametric studies

---

## References

**Documentation Summary**:
- **Section 1-4**: Input structure, blocks, formatting
- **Section 5**: All card types (cells, surfaces, data)
- **Section 6**: Geometry transformations
- **Section 7**: Material definitions

**Related Skills**:
- **mcnp-input-builder**: Creating new inputs (use builder, then edit)
- **mcnp-input-validator**: Validating edits (always validate after editing)
- **mcnp-geometry-editor**: Specialized geometry modifications
- **mcnp-transform-editor**: Transformation (TR card) editing
- **mcnp-material-builder**: Material creation/modification

**User Manual References**:
- Chapter 4: Input File Description (structure requirements)
- Chapter 5: Input Cards (syntax for all card types)

**Slash Command**:
- `.claude/commands/mcnp-input-editor.md`: Quick reference for editing tasks

---

**End of MCNP Input Editor Skill**
