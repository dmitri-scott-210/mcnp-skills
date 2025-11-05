# MCNP Input Editor - Error Catalog

This document catalogs common errors encountered during MCNP input file editing and provides troubleshooting guidance.

---

## Error 1: Blank Line Separator Lost

### Symptom
After editing, MCNP reports "bad trouble" due to missing blank lines between blocks.

### Cause
Edit operation removed or corrupted blank line between cell/surface/data blocks.

### Diagnosis
Check file structure:
```
[Cell cards]
<BLANK LINE - CRITICAL>     ← Must be present
[Surface cards]
<BLANK LINE - CRITICAL>     ← Must be present
[Data cards]
<BLANK LINE - optional>
```

### Fix
Restore blank lines if missing:
```
c Last cell card
1000  0  999  IMP:N=0

<--- ENSURE BLANK LINE HERE

c First surface card
1  SO  10.0
```

### Prevention
- When editing, explicitly preserve empty lines
- Check blank line count before/after editing
- Use scripts that respect block structure
- Validate with: `grep -c "^$" input.i` (should return at least 2)

### MCNP Error Messages
```
bad trouble in subroutine xxx of mcrun
   invalid blank line terminator
```

---

## Error 2: Continuation Line Broken

### Symptom
Long card no longer continues correctly across multiple lines.

### Cause
Removed or corrupted continuation character (`&`) or 5-space indent.

### Original (Correct)
```
F4:N  1 2 3 4 5 6 7 8 9 10 &
      11 12 13 14 15
```

### Broken After Edit
```
F4:N  1 2 3 4 5 6 7 8 9 10
      11 12 13 14 15
(Missing & at end of line 1)
```

### Fix
Re-add continuation character:
```
F4:N  1 2 3 4 5 6 7 8 9 10 &
      11 12 13 14 15
```

OR use 5-space indent method:
```
F4:N  1 2 3 4 5 6 7 8 9 10
     11 12 13 14 15
(5 spaces at start of line 2)
```

### Prevention
- When editing multi-line cards, preserve & character
- Preserve 5-space indent on continuation lines
- Use regex that captures full card including continuations
- Consider finding card, editing as unit, then replacing as unit

### MCNP Error Messages
```
warning.  card image has     15 entries vs.      0 allowed.
fatal error.  too many entries on card.
```

---

## Error 3: Regex Replaced Too Much

### Symptom
Search/replace changed unintended text (over-matching pattern).

### Example
**Intended:** Change cell 1 density
```
Regex: 1\s+-1.0
Problem: Also matches cell 10, 100, 1000, etc.
```

**Result:**
```
Cell 1: 1  -1.2  -1  (correct)
Cell 10: 10  -1.2  -1  (WRONG! was -2.0)
Cell 100: 100  -1.2  -1  (WRONG! was -5.0)
```

### Fix
Use more specific regex with anchors:
```
Correct regex: ^1\s+\d+\s+-1\.0
(^ = start of line, ensures exact cell 1)
```

### Prevention Techniques

**1. Use anchors:**
- `^` = start of line
- `$` = end of line
- `\b` = word boundary

**2. Use lookahead/lookbehind:**
```
Positive lookahead: IMP:N=(?=1\b)
(Only IMP:N=1, not IMP:N=10 or IMP:N=100)

Negative lookahead: IMP:N=(?!0\b)
(IMP:N with any value EXCEPT 0)
```

**3. Always preview before applying:**
```
Step 1: Run regex with match highlighting
Step 2: Review all matches
Step 3: Verify no unintended matches
Step 4: Apply replacement
```

**4. Test on small sample first:**
```
Create test file with 10-line sample
Run regex on test file
Verify results
Then apply to full file
```

### MCNP Error Messages
Usually causes runtime physics errors, not input errors:
```
warning. material   1 has   12 nuclides with
         unresolved resonance probability table treatment.
(If wrong density applied to wrong material)
```

---

## Error 4: Comment Accidentally Edited

### Symptom
Comment text was modified, breaking meaning or documentation.

### Example
**Original:**
```
1  1  -1.0  -1  $ Water density = 1.0 g/cm³
```

**After batch "1.0 → 1.2" replacement:**
```
1  1  -1.2  -1  $ Water density = 1.2 g/cm³
                  ^^^^^^^^^^^^^^^^^^^^^^^^
                  Comment incorrectly auto-updated
```

### Problem
The comment should remain "1.0" for documentation (shows original value) or be manually updated with edit reason.

### Fix
Use regex to match field but exclude comments:
```
Regex: ^(\d+\s+\d+\s+)(-1\.0)(\s+-\d+.*?)(\$|$)
       ^Group 1      ^density ^geom    ^stop before $

Replace: $1-1.2$3$4
(Changes density, preserves comment)
```

### Better Approach
Manually update comments to document changes:
```
1  1  -1.2  -1  $ Water (changed from -1.0 to -1.2 on 2025-11-04)
```

### Prevention
- Use regex groups to preserve comments explicitly
- Match up to $ character, then preserve rest of line
- Consider separate pass for updating comments manually
- Add change documentation in separate comment lines

### Example Safe Pattern
```python
import re

def safe_density_change(line, old_dens, new_dens):
    """Change density without modifying comments"""
    # Split at comment
    if '$' in line:
        main, comment = line.split('$', 1)
    else:
        main, comment = line, ''

    # Only modify main part
    main = main.replace(str(old_dens), str(new_dens))

    # Reconstruct
    if comment:
        return main + '$' + comment
    return main
```

---

## Error 5: Card Order Scrambled

### Symptom
After editing, cards are out of order or in wrong blocks.

### Cause
Edit operation resorted lines or moved cards between blocks.

### Correct Structure
```
Cell cards MUST be in cell block (lines 52-4500)
Surface cards MUST be in surface block (lines 4502-5200)
Data cards MUST be in data block (lines 5202-9000)
```

### Symptoms of Scrambled Order
```
- Surface card appears before cell block blank line
- M card appears in cell block
- Cell card appears after first blank line
```

### Fix: Manual Restoration
```
1. Extract all cell cards → sort by cell number → place in block 1
2. Extract all surface cards → sort by surface number → place in block 2
3. Extract all data cards → preserve order → place in block 3
4. Ensure EXACTLY 2 blank lines (after cells, after surfaces)
```

### Fix Script
```python
def restore_block_structure(input_file):
    """Restore proper block structure"""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cells = []
    surfaces = []
    data = []
    title = lines[0] if lines else "Title\n"

    for line in lines[1:]:
        parts = line.split()
        if len(parts) == 0:
            continue

        # Cell card: j m d geom
        if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
            cells.append(line)

        # Surface card: j type params (j is digit, type is 1-2 letters)
        elif len(parts) >= 2 and parts[0].isdigit() and len(parts[1]) <= 3:
            surfaces.append(line)

        # Data card: starts with letter
        elif parts[0][0].isalpha():
            data.append(line)

    # Reconstruct file
    with open(input_file, 'w') as f:
        f.write(title)
        for cell in sorted(cells):
            f.write(cell)
        f.write('\n')  # Blank line
        for surf in sorted(surfaces):
            f.write(surf)
        f.write('\n')  # Blank line
        for d in data:
            f.write(d)
```

### Prevention
- Edit in-place, don't move cards between blocks
- Never sort entire file (only within blocks)
- Use block-aware editing tools
- Validate block structure after editing

---

## Error 6: Whitespace Issues After Edit

### Symptom
Extra spaces, tabs, or missing spaces cause parsing errors.

### Common Issues

**Issue 1: Tab characters**
```
MCNP treats tabs as single space - can break formatting

100  1  -1.0\t-10  → Invalid (tab breaks spacing)
Fix: Replace tabs with spaces
```

**Issue 2: Multiple spaces collapsed**
```
100  1  -1.0   -10  → 100 1 -1.0 -10  (wrong - fields merged)
Fix: Preserve original spacing
```

**Issue 3: Missing space between parameters**
```
IMP:N=1IMP:P=1 → Should be: IMP:N=1  IMP:P=1
Fix: Add space between parameters
```

**Issue 4: Trailing whitespace**
```
Some editors remove trailing spaces, can break continuation
```

### Fixes

**Convert tabs to spaces:**
```python
def detab_file(filename):
    """Replace tabs with spaces"""
    with open(filename, 'r') as f:
        content = f.read()
    content = content.replace('\t', '  ')
    with open(filename, 'w') as f:
        f.write(content)
```

**Standardize spacing:**
```python
def standardize_cell_spacing(line):
    """Standardize spacing in cell cards"""
    parts = line.split()
    if len(parts) >= 3:
        j = parts[0]
        m = parts[1]
        d = parts[2]
        rest = ' '.join(parts[3:])
        return f"{j:6s} {m:3s} {d:8s}  {rest}\n"
    return line
```

### Prevention
- Configure editor to use spaces (not tabs)
- Show whitespace characters in editor
- Set consistent indentation (2 or 4 spaces)
- Use Python string formatting for consistent spacing
- Test file after editing with: `cat -A input.i` (shows tabs as ^I)

### MCNP Error Messages
```
bad trouble in subroutine xxx of mcrun
   format error on card
```

---

## Error 7: Undefined Reference After Edit

### Symptom
Cell references surface/material/universe that doesn't exist after edit.

### Example
**Before edit:**
```
Cell cards:
100  1  -1.0  -10  11  IMP:N=1

Surface cards:
10  SO  5.0
11  SO  10.0
```

**After deleting surface 11:**
```
Cell cards:
100  1  -1.0  -10  11  IMP:N=1  ← References undefined surface 11!

Surface cards:
10  SO  5.0
(Surface 11 deleted)
```

### Fix
**Option 1: Remove reference**
```
100  1  -1.0  -10  IMP:N=1
```

**Option 2: Replace with valid surface**
```
100  1  -1.0  -10  12  IMP:N=1
(Add surface 12)
```

**Option 3: Restore deleted surface**
```
11  SO  10.0
```

### Prevention
- Before deleting surface/material/universe, search for all references
- Use cross-reference checker before and after edits
- Consider commenting out instead of deleting
- Maintain dependency map during complex edits

### Detection Script
```python
def find_undefined_references(input_file):
    """Find cells referencing undefined surfaces"""
    # Parse surface definitions
    defined_surfs = set()
    cell_refs = {}

    with open(input_file, 'r') as f:
        in_surf_block = False
        in_cell_block = False

        for line in f:
            parts = line.split()
            if len(parts) == 0:
                if in_cell_block:
                    in_surf_block = True
                    in_cell_block = False
                elif in_surf_block:
                    break
                else:
                    in_cell_block = True
                continue

            # Collect surface definitions
            if in_surf_block and parts[0].isdigit():
                defined_surfs.add(int(parts[0]))

            # Collect cell surface references
            if in_cell_block and parts[0].isdigit():
                cell_num = int(parts[0])
                # Extract surface numbers from geometry
                # (Simplified - real parser more complex)
                for part in parts[3:]:
                    if part.lstrip('-').isdigit():
                        surf_ref = int(part.lstrip('-'))
                        if cell_num not in cell_refs:
                            cell_refs[cell_num] = []
                        cell_refs[cell_num].append(surf_ref)

    # Find undefined references
    for cell, refs in cell_refs.items():
        for ref in refs:
            if ref not in defined_surfs:
                print(f"Cell {cell} references undefined surface {ref}")
```

### MCNP Error Messages
```
fatal error.  surface    11 is not defined but is referenced on cell    100 card.
```

---

## Error 8: Loss of Precision in Numeric Values

### Symptom
After editing, numeric values have reduced precision or scientific notation changed.

### Example
**Original:**
```
M1  92235.80c  3.2E-4  92238.80c  2.38E-2
```

**After careless edit:**
```
M1  92235.80c  0.00032  92238.80c  0.0238
(Lost scientific notation - may have insufficient precision)
```

### Fix
Preserve original format:
```
M1  92235.80c  3.2E-4  92238.80c  2.38E-2
```

### Prevention
```python
def preserve_format_edit(line, changes):
    """Edit while preserving number formatting"""
    # Use string replacement, not float conversion
    for old, new in changes.items():
        line = line.replace(old, new)
    return line

# Instead of:
def bad_edit(line):
    parts = line.split()
    parts[2] = str(float(parts[2]) * 1.1)  # Loses format!
    return ' '.join(parts)
```

---

## Troubleshooting Workflow

### General Debugging Procedure

**1. Identify symptom**
- MCNP error message
- Unexpected behavior
- Visual inspection

**2. Locate problem**
- Which block (cells/surfaces/data)?
- Which card(s) affected?
- Line numbers

**3. Determine cause**
- Compare to backup/original
- Check recent edits
- Review edit method

**4. Apply fix**
- Use appropriate technique from above
- Test fix incrementally
- Validate with mcnp-input-validator

**5. Verify**
- Test run MCNP (short NPS)
- Check for warnings
- Compare output to baseline

**6. Document**
- Log what was changed
- Note root cause
- Update prevention steps

---

**END OF ERROR CATALOG**

For editing techniques, see SKILL.md.
For detailed examples, see detailed_examples.md.
For regex patterns, see regex_patterns_reference.md.
