# MCNP Input Editor - Scripts

This directory contains Python automation scripts for systematic MCNP input file editing.

## Scripts Overview

### 1. input_editor.py - General Purpose Editor

**Purpose:** Versatile editor for common editing tasks (find/replace, cell edits, validation).

**Features:**
- Find and replace (literal or regex)
- Edit specific cell parameters (density, etc.)
- Validate file structure
- File statistics

**Examples:**
```bash
# Change cell 100 density
python input_editor.py input.i --cell 100 --density -1.2

# Batch find/replace
python input_editor.py input.i --find "IMP:N=2" --replace "IMP:N=1"

# Regex replace for library update
python input_editor.py input.i --find "\\.70c" --replace ".80c" --regex

# Preview changes before applying
python input_editor.py input.i --find "IMP:N=2" --replace "IMP:N=1" --preview

# Validate file structure
python input_editor.py input.i --validate

# Get file statistics
python input_editor.py input.i --stats
```

---

### 2. batch_importance_editor.py - Importance Management

**Purpose:** Specialized editor for neutron importance values with smart graveyard handling.

**Features:**
- Set all importances to single value
- Change specific importance values
- Set importances by material type
- Preview importance distribution
- Automatic IMP:N=0 (graveyard) protection

**Examples:**
```bash
# Set all importances to 1 (except graveyard)
python batch_importance_editor.py input.i --set-all 1

# Change all IMP:N=2 to IMP:N=1
python batch_importance_editor.py input.i --old 2 --new 1

# Set by material: mat 1→imp 1, mat 2→imp 2, mat 10→imp 4
python batch_importance_editor.py input.i --by-material 1:1 2:2 10:4

# Preview current importance distribution
python batch_importance_editor.py input.i --preview

# Include graveyard cells (use with caution!)
python batch_importance_editor.py input.i --set-all 1 --include-zero
```

---

### 3. library_converter.py - Cross-Section Library Updates

**Purpose:** Convert ZAID cross-section library identifiers between ENDF versions.

**Features:**
- Batch library conversion (.70c → .80c, etc.)
- Selective conversion (specific isotopes only)
- List all ZAIDs in file
- Check thermal scattering (MT) card compatibility
- Preview mode

**Examples:**
```bash
# Convert all .70c to .80c (ENDF/B-VII → ENDF/B-VIII)
python library_converter.py input.i --old 70c --new 80c

# Preview changes
python library_converter.py input.i --old 70c --new 80c --preview

# Convert only specific isotopes
python library_converter.py input.i --old 70c --new 80c --zaids 1001 8016 92235

# List all ZAIDs in file
python library_converter.py input.i --list

# Check thermal scattering libraries (MT cards)
python library_converter.py input.i --check-mt
```

**Common Library Identifiers:**
- `.70c` - ENDF/B-VII.0 (continuous energy neutron)
- `.80c` - ENDF/B-VIII.0 (continuous energy neutron)
- `.31c` - ENDF/B-VI.8 (continuous energy neutron)
- `.24c` - ENDF/B-VI (continuous energy neutron)

---

### 4. large_file_indexer.py - Large File Handler

**Purpose:** Efficient editing of large MCNP files (9,000+ lines) via indexing.

**Features:**
- Build index of card locations
- Fast random access to specific cells/surfaces
- Targeted editing without loading full file
- File statistics from index

**Examples:**
```bash
# Build index (do this first for large files)
python large_file_indexer.py large_reactor.i --build-index

# Find cell location
python large_file_indexer.py large_reactor.i --find-cell 1234

# Edit cell using index (very fast)
python large_file_indexer.py large_reactor.i --edit-cell 500 --density -1.2

# Get file statistics
python large_file_indexer.py large_reactor.i --stats
```

**Performance:**
- Files <1,000 lines: Use input_editor.py
- Files 1,000-5,000 lines: Either tool works
- Files >5,000 lines: Use large_file_indexer.py for best performance

**Index File:**
- Automatically saved as `filename.idx.json`
- Reused for subsequent operations
- Rebuild if input file changes

---

## Installation & Requirements

### Python Version
- Python 3.7 or later

### Dependencies
- Standard library only (no external packages required)

### Installation
```bash
# Clone or download scripts to local directory
cd /path/to/scripts/

# Make executable (Linux/Mac)
chmod +x *.py

# Test installation
python input_editor.py --help
```

---

## Workflow Examples

### Workflow 1: ENDF Library Upgrade

**Task:** Update reactor model from ENDF/B-VII.0 to ENDF/B-VIII.0

```bash
# 1. Backup original
cp reactor.i reactor_backup.i

# 2. Preview changes
python library_converter.py reactor.i --old 70c --new 80c --preview

# 3. Check thermal libraries
python library_converter.py reactor.i --check-mt

# 4. Apply conversion
python library_converter.py reactor.i --old 70c --new 80c

# 5. Validate
python input_editor.py reactor.i --validate

# 6. Test run
mcnp6 i=reactor.i n=test_run. tasks 4
```

### Workflow 2: Importance Optimization

**Task:** Simplify variance reduction by setting uniform importances

```bash
# 1. Review current distribution
python batch_importance_editor.py input.i --preview

# 2. Set all to 1 (analog transport)
python batch_importance_editor.py input.i --set-all 1

# 3. Run MCNP and analyze FOM
mcnp6 i=input.i n=run_analog.

# 4. If needed, apply material-based strategy
python batch_importance_editor.py input.i --by-material 1:1 2:2 10:4

# 5. Compare FOM
mcnp6 i=input.i n=run_optimized.
```

### Workflow 3: Large File Editing

**Task:** Modify specific cells in 12,000-line full core model

```bash
# 1. Build index (one time)
python large_file_indexer.py full_core.i --build-index

# 2. Get statistics
python large_file_indexer.py full_core.i --stats

# 3. Find target cell
python large_file_indexer.py full_core.i --find-cell 4567

# 4. Edit density
python large_file_indexer.py full_core.i --edit-cell 4567 --density -10.2

# 5. Edit more cells (uses same index - fast!)
python large_file_indexer.py full_core.i --edit-cell 4568 --density -10.2
python large_file_indexer.py full_core.i --edit-cell 4569 --density -10.2
```

---

## Safety & Best Practices

### Always Backup First
```bash
cp input.i input_backup_$(date +%Y%m%d).i
```

### Use Preview Mode
```bash
# Preview changes before applying
python input_editor.py input.i --find "X" --replace "Y" --preview
python library_converter.py input.i --old 70c --new 80c --preview
```

### Validate After Editing
```bash
# Check file structure
python input_editor.py input.i --validate

# Run MCNP fatal check
mcnp6 i=input.i z

# Test with short run
mcnp6 i=input.i n=test. tasks 1
```

### Version Control
```bash
# Use git for tracking
git add input.i
git commit -m "Updated cross-section libraries to ENDF/B-VIII"

# Or manual versioning
cp input.i input_v1.0.i  # Baseline
# ... make edits ...
cp input.i input_v1.1.i  # After edits
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Ensure Python 3.7+ is installed
```bash
python --version  # Should be 3.7 or later
```

### Issue: "File not found"
**Solution:** Use absolute paths or verify working directory
```bash
python input_editor.py /full/path/to/input.i --stats
```

### Issue: "Index not found"
**Solution:** Build index first for large files
```bash
python large_file_indexer.py large_file.i --build-index
```

### Issue: Unexpected changes
**Solution:** Always use preview mode first
```bash
python input_editor.py input.i --find "X" --replace "Y" --preview
# Review output, then run without --preview if correct
```

---

## Additional Resources

### Related Skills
- **mcnp-input-builder** - Creating input files
- **mcnp-input-validator** - Validating edited files
- **mcnp-geometry-editor** - Specialized geometry editing
- **mcnp-material-builder** - Material composition management

### Reference Documentation
- **detailed_examples.md** - Extended use cases
- **error_catalog.md** - Common editing errors
- **regex_patterns_reference.md** - Regex patterns for MCNP
- **advanced_techniques.md** - Automation workflows

### External Documentation
- MCNP6 User Manual - Chapter 4 (Input Format)
- MCNP6 User Manual - Chapter 5 (Input Cards)

---

**END OF README**

For questions or issues, refer to SKILL.md or detailed_examples.md.
