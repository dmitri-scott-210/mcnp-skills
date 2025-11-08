# Multi-File Editing Guide

Comprehensive guidance for editing multiple MCNP input files consistently.

## Decision Matrix: Edit vs. Regenerate

| Change Needed | Location | Action | Tool |
|--------------|----------|--------|------|
| CSV data corrected | power.csv, oscc.csv | **Regenerate all** | `create_inputs.py` |
| Template structure | bench.template | **Edit template → regenerate** | Edit template |
| All files same change | Generated inputs | **Batch edit** | `batch_multi_file_editor.py` |
| Library update | All inputs | **Batch edit** | `library_converter.py` + batch |
| Individual file fix | One input | **Edit single file** | `input_editor.py` |

## Workflow Patterns

### Pattern 1: CSV Data Correction

**Situation**: Operational data in CSV was wrong

**Steps**:
1. Update CSV file (power.csv, oscc.csv, etc.)
2. Regenerate ALL inputs: `python create_inputs.py`
3. Validate: Check plots and first input
4. Replace old inputs with new

**DO NOT** try to edit 13 individual files manually!

### Pattern 2: Library Migration

**Situation**: Update from ENDF/B-VII.0 (.70c) to ENDF/B-VIII.0 (.80c)

**Steps**:
1. Backup: `git commit -m "Before library update"`
2. Preview: `batch_multi_file_editor.py --files "*.i" --find ".70c" --replace ".80c" --preview`
3. Check count: Should match total number of ZAIDs across all files
4. Apply: Remove `--preview` flag
5. Validate: Test run one file
6. Test run: MCNP on one input to verify libraries exist

### Pattern 3: Validation Error in Multiple Files

**Situation**: Same error in subset of files

**Steps**:
1. Identify affected files: `for f in *.i; do grep -l "error" "$f"; done`
2. Fix in ONE file manually
3. Test that fix works
4. Apply to remaining files: `batch_multi_file_editor.py --files "list" --find "X" --replace "Y"`

## Complex Scenarios

### Scenario 1: Different Changes per File

**Problem**: 13 cycle inputs need different power values (can't use simple find/replace)

**Solution**: Use CSV-driven updates (regenerate from template + CSV)

### Scenario 2: Conditional Edits

**Problem**: Only change materials m9000-m9099, leave others untouched

**Solution**: Use regex with boundaries
```bash
python batch_multi_file_editor.py --files "*.i" \
  --find "m90[0-9]{2}\s" --replace "m80XX " --regex
```

### Scenario 3: Structural Changes

**Problem**: Add VOL cards to cells that don't have them

**Solution**: Use `insert_parameter` mode
```bash
batch_multi_file_editor.py --files "*.i" \
  --insert-parameter "VOL" --value "1000" --cells "100-199"
```

## Safety Checklist

Before batch editing multiple files:

- [ ] Files are under version control (git)
- [ ] Tested edit on ONE file successfully
- [ ] Preview shows expected replacement count
- [ ] Backups will be created automatically
- [ ] Have validator ready to check results
- [ ] Have MCNP ready to test one file
- [ ] Understand how to rollback if needed

## Rollback Procedure

If batch edit goes wrong:

**Option A: Use git** (if committed before editing)
```bash
git diff HEAD bench_138B.i  # Check what changed
git checkout HEAD -- bench_*.i  # Restore all
```

**Option B: Use .bak files** (created by script)
```bash
for f in bench_*.i.bak; do
  mv "$f" "${f%.bak}"  # Remove .bak extension
done
```

**Option C: Regenerate** (if template-generated)
```bash
python create_inputs.py  # Regenerate from source
```

## Performance Considerations

**Large files (>10,000 lines)**:
- Use `--regex` sparingly (slower)
- Process in batches (10 files at a time)
- Use `large_file_indexer.py` for very large files

**Many files (>50)**:
- Consider parallel processing
- Use file patterns instead of listing all
- Monitor disk space (backups double storage)

## Example Workflows

### Workflow 1: Update 13 Cycle Inputs After CSV Correction

```bash
# 1. User discovers error in power.csv at timestep 312
vim power.csv  # Fix: 23.45 → 23.78 MW

# 2. Regenerate all 13 inputs
python create_inputs.py

# 3. Validate first input
python input_editor.py bench_138B.i --validate

# 4. Verify in output
grep "power" bench_138B.i
# Should show updated average power
```

### Workflow 2: Library Migration Across All Files

```bash
# 1. Backup files
git add mcnp/bench_*.i
git commit -m "Before library update"

# 2. Preview changes
python batch_multi_file_editor.py \
  --files "mcnp/bench_*.i" \
  --find ".70c" \
  --replace ".80c" \
  --preview

# Expected: ~385 materials × 13 files = 5,005 replacements

# 3. Apply
python batch_multi_file_editor.py \
  --files "mcnp/bench_*.i" \
  --find ".70c" \
  --replace ".80c"

# 4. Test one file
mcnp6 i=bench_138B.i n=test. tasks 1
# Check for library errors

# 5. If good, commit
git add mcnp/bench_*.i
git commit -m "Library update: .70c → .80c (ENDF/B-VIII.0)"
```

### Workflow 3: Fix Validation Error in Multiple Files

```bash
# 1. Validator identifies missing surface
python mcnp-input-validator/validate.py bench_138B.i
# ERROR: Surface 9999 referenced but not defined

# 2. Check which files have the error
for f in mcnp/bench_*.i; do
  grep -l "9999" "$f"
done
# Output: 6 files

# 3. Option A: Remove references (if surface was mistake)
python batch_multi_file_editor.py \
  --files "mcnp/bench_138B.i mcnp/bench_139A.i ..." \
  --find "-9999" \
  --replace "" \
  --validate-after

# Option B: Add missing surface to all files
python batch_multi_file_editor.py \
  --files "mcnp/bench_*.i" \
  --insert-surface "9999 pz 100  $ Added missing plane"
```

## Best Practices

1. **Always use version control** - Commit before any batch operation
2. **Preview on ONE file first** - Test strategy on single file before batch
3. **Count expected changes** - Verify preview count matches expectations
4. **Validate ALL files after** - Use for loop to validate each file
5. **Test run one file** - Quick MCNP run to catch fatal errors
6. **Document changes** - Git commit messages or change log
7. **Keep backups** - Script creates .bak files automatically
8. **Monitor disk space** - Backups can consume significant space

## Common Pitfalls

### Pitfall 1: Editing When Should Regenerate

**Symptom**: Manual edits to 13 files when CSV data changed

**Fix**: Always regenerate from template + CSV for data-driven changes

### Pitfall 2: Over-Matching with Regex

**Symptom**: Changed "100" in cell numbers when only wanted material 100

**Fix**: Use word boundaries `\b100\b` or more specific patterns

### Pitfall 3: Forgetting to Validate

**Symptom**: Batch edit completes, but files have syntax errors

**Fix**: Always run validator on ALL files after batch edit

### Pitfall 4: No Backups

**Symptom**: Batch edit went wrong, can't recover

**Fix**: Always commit to git or verify .bak files created

## Troubleshooting

### Problem: Preview count doesn't match expectations

**Symptoms**: Expected 385 changes, preview shows 412

**Causes**:
1. Pattern matching more than intended
2. Comments or other lines matched
3. Duplicate entries

**Fix**: Refine pattern, use `--regex` with word boundaries

### Problem: Validation fails after batch edit

**Symptoms**: Some files pass validation, others fail

**Causes**:
1. Inconsistent file structure
2. Pattern matched different things in different files
3. Corruption during edit

**Fix**: Compare failed files to successful ones, identify pattern

### Problem: Files too large for batch processing

**Symptoms**: Script runs out of memory

**Causes**: Loading all large files into memory at once

**Fix**: Use `large_file_indexer.py` or process files in smaller batches

## Advanced Techniques

### Parallel Processing

For many files (>20), consider parallel processing:

```bash
# Using GNU parallel
parallel python input_editor.py {} --find ".70c" --replace ".80c" ::: bench_*.i
```

### Conditional Editing Based on File Content

```bash
# Only edit files that contain certain pattern
for f in bench_*.i; do
  if grep -q "LAT=1" "$f"; then
    python input_editor.py "$f" --find "X" --replace "Y"
  fi
done
```

### Batch Edit with Different Replacements

```bash
# Read replacements from file
while IFS=',' read -r file find replace; do
  python input_editor.py "$file" --find "$find" --replace "$replace"
done < replacements.csv
```

---

**END OF GUIDE**
