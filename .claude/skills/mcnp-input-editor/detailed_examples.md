# MCNP Input Editor - Detailed Examples

This document contains extended use cases and examples for systematic MCNP input file editing. For basic examples, see SKILL.md Use Cases 1-2.

---

## Use Case 3: Update Material ZAIDs (Library Change)

**Scenario**: Change all ZAIDs from .70c to .80c (ENDF/B-VII to ENDF/B-VIII)

### Original Input
```
M1   1001.70c  2   8016.70c  1        $ Water
MT1  LWTR.01T
M2   92235.70c  0.03  92238.70c  0.97  $ LEU fuel
M3   6000.70c  1.0                     $ Graphite
MT3  GRPH.01T
```

### Editing Steps

**Step 1: Search for pattern**
```
Pattern: \.70c
(Matches ".70c" library identifier)
```

**Step 2: Replace**
```
Replace: .80c
```

**Step 3: Apply to all M cards**
```
M1   1001.80c  2   8016.80c  1        $ Water
MT1  LWTR.01T
M2   92235.80c  0.03  92238.80c  0.97  $ LEU fuel
M3   6000.80c  1.0                     $ Graphite
MT3  GRPH.01T
```

**Step 4: Verify thermal scattering libraries**
```
Check that LWTR.01T and GRPH.01T are compatible with .80c data
(May need to update to LWTR.20T if temperature differs)
```

### Advanced: Selective by Isotope

Change only U-235 and U-238:
```
Pattern: 9223[58]\.\d+c
Replace: Match found → check digit → 92235.80c or 92238.80c
```

### Implementation Script

```python
def update_library(input_file, old_lib, new_lib):
    """Change all ZAIDs from old to new library"""
    with open(input_file, 'r') as f:
        content = f.read()

    # Simple replacement
    updated = content.replace(f'.{old_lib}c', f'.{new_lib}c')

    with open(input_file, 'w') as f:
        f.write(updated)

    print(f"Updated all .{old_lib}c → .{new_lib}c")

# Usage
update_library('input.i', '70', '80')
```

### Key Points
- Batch library changes are common when upgrading MCNP versions
- Verify cross-section library availability (check xsdir file)
- Update MT cards if thermal library versions changed
- Test with short run to ensure libraries load correctly
- Check for compatibility issues between old/new libraries

---

## Use Case 4: Scale Geometry (Change Dimensions)

**Scenario**: Scale entire geometry by factor of 1.1 (10% larger)

### Original Input
```
c Surface Cards
1    SO   10.0                  $ Inner sphere R=10 cm
2    SO   20.0                  $ Outer sphere R=20 cm
3    PZ   0.0                   $ Bottom plane
4    PZ   50.0                  $ Top plane
5    CZ   5.0                   $ Cylinder R=5 cm
```

### Manual Method (Small Number of Surfaces)

For each surface:
- Identify dimension parameters
- Multiply by 1.1
- Update value

**Results:**
```
1    SO   11.0                  $ Inner sphere R=11 cm
2    SO   22.0                  $ Outer sphere R=22 cm
3    PZ   0.0                   $ Bottom plane (unchanged)
4    PZ   55.0                  $ Top plane
5    CZ   5.5                   $ Cylinder R=5.5 cm
```

### Automated Method (Many Surfaces)

For surfaces with numeric parameters:
1. Parse surface type (SO, PZ, CZ, etc.)
2. Extract numeric values
3. Apply scale factor (except origin points for some types)
4. Reconstruct surface card

**Caution**: Some values should NOT be scaled:
- Plane coefficients (A, B, C in P card)
- Direction cosines (GQ coefficients)
- Origin coordinates (sometimes)

### Add Documentation
```
c Surface Cards
c SCALED by 1.1 from original geometry (2025-11-04)
1    SO   11.0                  $ Inner sphere R=11 cm (was 10.0)
2    SO   22.0                  $ Outer sphere R=22 cm (was 20.0)
```

### Implementation Script

```python
def scale_surface(surface_line, factor):
    """Scale numeric parameters in surface card"""
    parts = surface_line.split()
    if len(parts) < 3:
        return surface_line  # Invalid format

    surf_num = parts[0]
    surf_type = parts[1]

    # Simple spheres (SO)
    if surf_type.upper() == 'SO':
        radius = float(parts[2]) * factor
        return f"{surf_num}    {surf_type}   {radius:.1f}\n"

    # Cylinders (CZ)
    elif surf_type.upper() == 'CZ':
        radius = float(parts[2]) * factor
        return f"{surf_num}    {surf_type}   {radius:.1f}\n"

    # Add more surface types as needed
    else:
        return surface_line  # Don't modify unknown types
```

### Alternative: Use TR Transformations

Instead of modifying surface cards directly, consider using TR (transformation) cards for uniform scaling:

```
TR1  0 0 0  1.1 1.1 1.1  $ Scale by 1.1 in all directions
```

Then apply to cells:
```
1  1  -1.0  -1  *TRCL=1  $ Cell with transformation applied
```

### Key Points
- Geometry scaling is complex (not all parameters scale equally)
- Consider using TR transformations instead for uniform scaling
- Document original dimensions in comments
- Verify with MCNP plot after scaling
- Check for lost particles in test run
- Some surface types have parameters that should NOT scale

---

## Use Case 5: Add Parameter to All Cells

**Scenario**: Add VOL parameter to all cells that don't have it

### Original Input
```
1    1  -1.0   -1       IMP:N=1
2    2  -2.3   1  -2    IMP:N=1  VOL=500
3    3  -11.3  2  -3    IMP:N=1
4    0         3        IMP:N=0
```

### Method 1: Add VOL=1 Placeholder

**Identify cells without VOL:**
```
Search for cell cards NOT containing "VOL="
Regex: ^(\d+\s+\d+\s+-?[\d.eE+-]+\s+.*?)(IMP:)
(Captures cell card up to IMP, checks no VOL present)
```

**Insert VOL parameter:**
```
1    1  -1.0   -1       IMP:N=1  VOL=1
3    3  -11.3  2  -3    IMP:N=1  VOL=1
```

VOL=1 tells MCNP to calculate volume automatically.

### Method 2: Calculate Actual Volumes

Requires geometry analysis or MCNP PRINT card output:

```python
def add_volumes(input_file, volumes_dict):
    """Add VOL parameter based on calculated volumes

    volumes_dict: {cell_num: volume_value}
    Example: {1: 1000.0, 3: 800.0}
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()

    modified = []
    for line in lines:
        parts = line.split()
        if len(parts) > 0 and parts[0].isdigit():
            cell_num = int(parts[0])
            if cell_num in volumes_dict and 'VOL=' not in line:
                # Add VOL before newline
                line = line.rstrip() + f"  VOL={volumes_dict[cell_num]}\n"
        modified.append(line)

    with open(input_file, 'w') as f:
        f.writelines(modified)
```

### Method 3: Add as Separate VOL Card

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

### Key Points
- VOL parameter can be on cell card OR separate VOL data card
- VOL=1 tells MCNP to calculate (may be slow for complex cells)
- Actual volumes improve F4 tally normalization
- Void cells (m=0) don't need VOL
- Use MCNP PRINT 110 card to extract calculated volumes
- Separate VOL card useful when many cells need volumes

---

## Use Case 6: Comment All Cells (Documentation)

**Scenario**: Add descriptive inline comments to all cell cards

### Original Input
```
1    1  -1.0   -1
2    2  -2.3   1  -2
3    3  -11.3  2  -3
4    0         3  -4
5    0         4
```

### Method 1: Material-Based Comments

```
1    1  -1.0   -1       $ Water (material 1)
2    2  -2.3   1  -2    $ Concrete (material 2)
3    3  -11.3  2  -3    $ Lead (material 3)
4    0         3  -4    $ Air gap (void)
5    0         4        $ Graveyard (outside world)
```

### Method 2: Geometric Description

```
1    1  -1.0   -1       IMP:N=1  $ Inner sphere (R<10 cm)
2    2  -2.3   1  -2    IMP:N=1  $ Shell 1 (10<R<20 cm)
3    3  -11.3  2  -3    IMP:N=1  $ Shell 2 (20<R<30 cm)
4    0         3  -4    IMP:N=1  $ Outer void (30<R<40 cm)
5    0         4        IMP:N=0  $ Graveyard (R>40 cm)
```

### Automated Comment Generation

```python
def add_cell_comments(input_file, material_names):
    """Add comments to cell cards based on material

    material_names: {mat_num: 'Material Name'}
    Example: {1: 'Water', 2: 'Concrete', 3: 'Lead'}
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()

    modified = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[0].isdigit():
            cell_num = int(parts[0])
            mat_num = int(parts[1])

            # Add comment if not present
            if '$' not in line:
                if mat_num == 0:
                    comment = " $ Void"
                elif mat_num in material_names:
                    comment = f" $ {material_names[mat_num]}"
                else:
                    comment = f" $ Material {mat_num}"

                line = line.rstrip() + comment + "\n"

        modified.append(line)

    with open(input_file, 'w') as f:
        f.writelines(modified)
```

### Key Points
- Comments start with $ (inline) or C (full line)
- Keep comments concise (<40 characters)
- Document special features (importances, fills, transformations)
- Update comments when editing geometry or materials
- Consistent format improves readability
- Consider adding purpose, not just restating card content

---

## Use Case 7: Fix Common Errors in Batch

**Scenario**: Fix multiple common errors identified by mcnp-input-validator

### Error List
```
1. Duplicate cell numbers: 150, 151 (both exist twice)
2. Undefined surface 999 referenced in cell 200
3. Material 15 not defined but used in cell 300
4. Missing IMP:N parameter in cells 400-410
```

### Fix 1: Renumber Duplicate Cells

```
Find: ^150\s+
Replace: 1500  (for second occurrence)

Find: ^151\s+
Replace: 1510  (for second occurrence)
```

**Manual approach:**
1. Search for first "^150 " → Note line number
2. Search for second "^150 " → Edit this one
3. Repeat for cell 151

### Fix 2: Remove Invalid Surface Reference

**Find cell 200:**
```
Original: 200  5  -1.0  -10  11  999  IMP:N=1
Issue: Surface 999 doesn't exist
```

**Options:**
- a. Remove 999: `200  5  -1.0  -10  11  IMP:N=1`
- b. Replace with valid surface: `200  5  -1.0  -10  11  -12  IMP:N=1`
- c. Create surface 999 (if intended): Add `999  PZ  50.0` to surface block

### Fix 3: Add Missing Material

**Option 1: Define material 15**
```
Add to data cards:
M15  1001  2  8016  1  $ Water (added to fix error)
```

**Option 2: Change cell to use existing material**
```
Cell 300: M=15 → M=1  (if material 1 is suitable replacement)
```

### Fix 4: Add IMP:N to Cells 400-410

**Method 1: Individual edits**
```
400  ...  → 400  ...  IMP:N=1
401  ...  → 401  ...  IMP:N=1
...
```

**Method 2: Regex batch**
```
Find: ^(40\d)\s+(\d+\s+-?[\d.eE+-]+\s+.*?)$
Replace: $1  $2  IMP:N=1
(Adds IMP:N=1 to end of cells 400-409)
```

### Implementation Script

```python
def batch_fix_errors(input_file):
    """Fix common validation errors"""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    modified = []
    cell_nums_seen = {}

    for line in lines:
        parts = line.split()
        if len(parts) > 0 and parts[0].isdigit():
            cell_num = int(parts[0])

            # Fix 1: Renumber duplicates
            if cell_num in cell_nums_seen:
                new_num = cell_num * 10
                line = line.replace(f"{cell_num} ", f"{new_num} ", 1)
            else:
                cell_nums_seen[cell_num] = True

            # Fix 4: Add IMP:N if missing (cells 400-410)
            if 400 <= cell_num <= 410 and 'IMP:N' not in line:
                line = line.rstrip() + "  IMP:N=1\n"

        modified.append(line)

    with open(input_file, 'w') as f:
        f.writelines(modified)
```

### Key Points
- Address errors in order of severity (fatal first)
- Validate after each fix
- Document what was changed and why
- Re-run validator to confirm all errors resolved
- Test with short MCNP run
- Consider root cause (why did error occur?)

---

## Use Case 8: Large File Editing (9,000+ Lines)

**Scenario**: Edit specific cell in 9,000-line reactor model without loading entire file

### Challenge
Full file load is slow and memory-intensive for large reactor models (full PWR core, HFIR, etc.)

### Solution: Indexed Editing

**Step 1: Build Index**

Scan file once to create index of card locations:
```
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

**Step 2: Targeted Edit**

Task: Edit cell 500 (line 551)

```
1. Seek to line 551
2. Read line
3. Make edit
4. Write back to line 551
5. Done (never loaded full file)
```

**Step 3: Batch Edit in Chunks**

Task: Change all IMP:N=2 to IMP:N=1 in cells

```
1. Load cell block index (lines 52-4500)
2. Process in chunks of 100 lines
3. For each chunk:
   - Load 100 lines
   - Apply edits
   - Write back
   - Free memory
4. Repeat until done
```

### Implementation

```python
def build_cell_index(filename):
    """Build index of cell locations in large file"""
    index = {}
    with open(filename, 'r') as f:
        line_num = 0
        in_cell_block = False

        for line in f:
            line_num += 1
            parts = line.split()

            # Detect cell block start (after first blank line)
            if not in_cell_block and line.strip() == '':
                in_cell_block = True
                continue

            # Detect cell block end (second blank line)
            if in_cell_block and line.strip() == '':
                break

            # Index cell cards
            if in_cell_block and len(parts) > 0 and parts[0].isdigit():
                cell_num = int(parts[0])
                index[cell_num] = line_num

    return index

def edit_cell_in_large_file(filename, cell_num, new_density):
    """Edit single cell without loading full file"""
    # Build index
    index = build_cell_index(filename)

    if cell_num not in index:
        print(f"Cell {cell_num} not found")
        return

    target_line = index[cell_num]

    # Read all lines (in production, use seek for true streaming)
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Edit target line
    old_line = lines[target_line - 1]
    parts = old_line.split()
    parts[2] = str(new_density)  # Density field
    lines[target_line - 1] = '  '.join(parts) + '\n'

    # Write back
    with open(filename, 'w') as f:
        f.writelines(lines)

    print(f"Cell {cell_num} density updated to {new_density}")

# Usage
edit_cell_in_large_file('large_reactor.i', 500, -1.2)
```

### Performance Targets
- Index building: < 5 seconds (9,000-line file)
- Single card edit: < 1 second
- Batch edit (100 cards): < 5 seconds
- Total for complex edit sequence: < 30 seconds

### Key Points
- Index once, edit many times (amortize indexing cost)
- Stream processing for batch edits
- Don't load full file into memory
- Critical for large reactor models (HFIR, full PWR core, etc.)
- Consider using databases for very large models (>20,000 lines)
- Maintain index file separately for repeated edits

---

**END OF DETAILED EXAMPLES**

For basic examples, see SKILL.md Use Cases 1-2.
For error troubleshooting, see error_catalog.md.
For regex patterns, see regex_patterns_reference.md.
