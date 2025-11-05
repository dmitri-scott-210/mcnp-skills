# MCNP Input Editor - Advanced Techniques

This document covers advanced editing techniques, automation, and integration with development tools.

---

## Programmatic Editing with Python

### Basic Editor Framework

```python
class MCNPInputEditor:
    """Framework for programmatic MCNP input editing"""

    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.cell_block_start = 0
        self.surface_block_start = 0
        self.data_block_start = 0
        self.load()

    def load(self):
        """Load and index MCNP input file"""
        with open(self.filename, 'r') as f:
            self.lines = f.readlines()

        blank_count = 0
        for i, line in enumerate(self.lines):
            if line.strip() == '':
                blank_count += 1
                if blank_count == 1:
                    self.cell_block_start = i + 1
                    self.surface_block_start = i + 1
                elif blank_count == 2:
                    self.data_block_start = i + 1

    def save(self, output_filename=None):
        """Save modified input file"""
        filename = output_filename or self.filename
        with open(filename, 'w') as f:
            f.writelines(self.lines)

    def find_cell(self, cell_num):
        """Find line number for specific cell"""
        for i in range(self.cell_block_start, self.surface_block_start - 1):
            parts = self.lines[i].split()
            if len(parts) > 0 and parts[0] == str(cell_num):
                return i
        return None

    def edit_cell_density(self, cell_num, new_density):
        """Change density of specific cell"""
        line_num = self.find_cell(cell_num)
        if line_num is None:
            print(f"Cell {cell_num} not found")
            return False

        parts = self.lines[line_num].split()
        parts[2] = str(new_density)
        self.lines[line_num] = '  '.join(parts) + '\n'
        return True

    def batch_importance_change(self, old_imp, new_imp):
        """Change all importances from old to new"""
        import re
        pattern = f'IMP:N={old_imp}'
        replacement = f'IMP:N={new_imp}'

        for i in range(self.cell_block_start, self.surface_block_start - 1):
            if pattern in self.lines[i] and old_imp != 0:
                self.lines[i] = self.lines[i].replace(pattern, replacement)

# Usage example
editor = MCNPInputEditor('input.i')
editor.edit_cell_density(100, -1.2)
editor.batch_importance_change(2, 1)
editor.save('input_modified.i')
```

### Scripted Workflow Example

```python
def parametric_study(base_input, parameter_values):
    """Generate multiple inputs for parametric study"""

    for i, value in enumerate(parameter_values):
        editor = MCNPInputEditor(base_input)

        # Modify parameter (e.g., enrichment)
        editor.edit_material_fraction('M2', '92235.80c', value)

        # Save with unique name
        output = f'input_enrichment_{value:.3f}.i'
        editor.save(output)
        print(f"Created {output}")

# Generate inputs for enrichment study
enrichments = [0.030, 0.032, 0.034, 0.036, 0.038, 0.040]
parametric_study('base_input.i', enrichments)
```

---

## Version Control Integration

### Git Workflow for MCNP Inputs

**Initial Setup:**
```bash
cd mcnp_project/
git init
git add input.i
git commit -m "Initial input file for PWR fuel assembly"
```

**Track Changes:**
```bash
# Before making edits
git status
git diff input.i

# After editing
git add input.i
git commit -m "Increased U-235 enrichment from 3.0% to 3.2%"

# View history
git log --oneline
```

**Branching for Alternatives:**
```bash
# Create branch for alternative design
git checkout -b high_enrichment
# Make edits
git add input.i
git commit -m "High enrichment variant (4.5%)"

# Switch back to main
git checkout main

# Compare versions
git diff main high_enrichment input.i
```

**Tagging Validated Versions:**
```bash
# After successful MCNP run and validation
git tag -a v1.0 -m "Validated input, keff=1.0023±0.0005"
git tag -a v1.1 -m "Updated cross-section libraries to ENDF/B-VIII"

# List tags
git tag -l

# Checkout specific version
git checkout v1.0
```

### Git Diff for MCNP Files

**Configuration for better diffs:**
```bash
# .gitattributes file
*.i diff=mcnp
*.inp diff=mcnp

# .git/config
[diff "mcnp"]
    xfuncname = "^c.*|^[0-9]+ .*"
```

This shows cell/surface numbers in diff context.

---

## Diff-Based Editing

### Creating Patch Files

**Generate patch:**
```bash
# Make edits to input.i
# Create patch file
diff -u input_original.i input_modified.i > changes.patch
```

**Patch file example:**
```diff
--- input_original.i
+++ input_modified.i
@@ -10,7 +10,7 @@
-100  1  -1.0  -1  IMP:N=1
+100  1  -1.2  -1  IMP:N=1
@@ -45,7 +45,7 @@
-M1   92235.70c  0.03  92238.70c  0.97
+M1   92235.80c  0.032  92238.80c  0.968
```

**Apply patch:**
```bash
# Apply to another similar file
patch new_input.i < changes.patch

# Dry run (test without applying)
patch --dry-run new_input.i < changes.patch

# Reverse patch (undo changes)
patch -R input.i < changes.patch
```

### Use Case: Apply Same Edit to Multiple Files

```bash
# Create patch from first file
diff -u core_quarter1_old.i core_quarter1_new.i > enrichment_update.patch

# Apply to other quarters
patch core_quarter2.i < enrichment_update.patch
patch core_quarter3.i < enrichment_update.patch
patch core_quarter4.i < enrichment_update.patch
```

---

## Conditional Editing

### Rule-Based Editing

**Concept:** Apply different edits based on conditions

```python
def conditional_importance(editor):
    """Set importance based on material type"""

    for i in range(editor.cell_block_start, editor.surface_block_start - 1):
        parts = editor.lines[i].split()
        if len(parts) < 3:
            continue

        cell_num = int(parts[0])
        mat_num = int(parts[1])

        # Rules based on material
        if mat_num == 0:
            new_imp = 0  # Void cells
        elif mat_num == 1:
            new_imp = 1  # Water (moderator)
        elif mat_num in [2, 3]:
            new_imp = 2  # Structural materials
        elif mat_num >= 10:
            new_imp = 4  # Fuel (high importance)
        else:
            new_imp = 1  # Default

        # Apply importance
        if 'IMP:N' in editor.lines[i]:
            editor.lines[i] = re.sub(r'IMP:N=\d+', f'IMP:N={new_imp}', editor.lines[i])
        else:
            editor.lines[i] = editor.lines[i].rstrip() + f'  IMP:N={new_imp}\n'
```

### Material-Dependent Density Scaling

```python
def scale_densities_by_material(editor, scale_factors):
    """Scale densities differently for each material

    scale_factors: {mat_num: scale_factor}
    Example: {1: 0.95, 2: 1.0, 3: 1.02}
    """

    for i in range(editor.cell_block_start, editor.surface_block_start - 1):
        parts = editor.lines[i].split()
        if len(parts) < 3:
            continue

        mat_num = int(parts[1])
        if mat_num in scale_factors:
            old_density = float(parts[2])
            new_density = old_density * scale_factors[mat_num]
            parts[2] = f"{new_density:.4f}"
            editor.lines[i] = '  '.join(parts) + '\n'

# Usage
scale_factors = {
    1: 0.95,   # Reduce water density 5%
    2: 1.00,   # Keep structural materials same
    10: 1.02   # Increase fuel density 2%
}
scale_densities_by_material(editor, scale_factors)
```

---

## Stream Processing for Large Files

### Memory-Efficient Editing

**Problem:** Loading 20,000-line file uses too much memory

**Solution:** Stream processing - edit in chunks

```python
def stream_edit_large_file(input_file, output_file, edit_function):
    """Process large file in chunks without loading all"""

    chunk_size = 100  # Process 100 lines at a time

    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        chunk = []

        for line in fin:
            chunk.append(line)

            if len(chunk) >= chunk_size:
                # Edit chunk
                edited_chunk = edit_function(chunk)
                fout.writelines(edited_chunk)
                chunk = []

        # Process remaining lines
        if chunk:
            edited_chunk = edit_function(chunk)
            fout.writelines(edited_chunk)

def importance_edit_function(lines):
    """Edit function for chunk processing"""
    edited = []
    for line in lines:
        if 'IMP:N=2' in line:
            line = line.replace('IMP:N=2', 'IMP:N=1')
        edited.append(line)
    return edited

# Usage
stream_edit_large_file('huge_input.i', 'huge_input_modified.i',
                       importance_edit_function)
```

### Indexed Editing for Random Access

```python
class IndexedEditor:
    """Editor with index for fast random access"""

    def __init__(self, filename):
        self.filename = filename
        self.index = self._build_index()

    def _build_index(self):
        """Build index: {cell_num: byte_offset}"""
        index = {}
        with open(self.filename, 'rb') as f:
            offset = 0
            in_cell_block = False
            blank_count = 0

            for line in f:
                if line.strip() == b'':
                    blank_count += 1
                    if blank_count == 1:
                        in_cell_block = True
                    elif blank_count == 2:
                        break  # End of cell block

                elif in_cell_block:
                    parts = line.split()
                    if len(parts) > 0 and parts[0].isdigit():
                        cell_num = int(parts[0])
                        index[cell_num] = offset

                offset += len(line)

        return index

    def edit_cell_at_offset(self, cell_num, edit_func):
        """Edit specific cell without loading full file"""
        if cell_num not in self.index:
            return False

        offset = self.index[cell_num]

        # Read all (in production, use mmap for true random access)
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        # Calculate line number from offset
        # (Simplified - real implementation uses byte offset)
        line_num = offset // 80  # Approximate

        # Edit line
        lines[line_num] = edit_func(lines[line_num])

        # Write back
        with open(self.filename, 'w') as f:
            f.writelines(lines)

        return True
```

---

## Automated Editing Workflows

### Pre-Run Preparation Script

```bash
#!/bin/bash
# prepare_mcnp_run.sh

INPUT_FILE="$1"
RUN_NAME="$2"

# 1. Backup original
cp "$INPUT_FILE" "${INPUT_FILE}.backup"

# 2. Update NPS for production run
sed -i 's/NPS.*/NPS  1000000/' "$INPUT_FILE"

# 3. Update PRDMP for checkpoint frequency
sed -i 's/PRDMP.*/PRDMP  2J 1  1  2J -100/' "$INPUT_FILE"

# 4. Add PTRAC card if not present
if ! grep -q "PTRAC" "$INPUT_FILE"; then
    echo "PTRAC  FILE=ASC  EVENT=SUR  TYPE=N" >> "$INPUT_FILE"
fi

# 5. Create run directory
mkdir -p "runs/${RUN_NAME}"
cp "$INPUT_FILE" "runs/${RUN_NAME}/input.i"

echo "Prepared ${INPUT_FILE} for run: ${RUN_NAME}"
```

### Post-Processing Automation

```python
def update_input_from_results(input_file, output_file):
    """Update input based on MCNP output analysis"""

    # Read MCNP output
    with open(output_file, 'r') as f:
        output_text = f.read()

    # Extract keff (example)
    import re
    match = re.search(r'final estimated.*?keff.*?=\s+([\d.]+)', output_text)
    if match:
        keff = float(match.group(1))

        # If subcritical, increase enrichment
        if keff < 0.99:
            editor = MCNPInputEditor(input_file)
            # Increase enrichment logic here
            editor.save(input_file.replace('.i', '_adjusted.i'))

# Usage in automated workflow
update_input_from_results('input.i', 'output.txt')
```

---

## Integration with Analysis Tools

### Extract Geometry for Visualization

```python
def extract_geometry_for_plot(input_file, output_json):
    """Extract geometry to JSON for external plotting"""
    import json

    editor = MCNPInputEditor(input_file)

    cells = []
    surfaces = []

    # Extract cell information
    for i in range(editor.cell_block_start, editor.surface_block_start - 1):
        parts = editor.lines[i].split()
        if len(parts) >= 3:
            cells.append({
                'number': int(parts[0]),
                'material': int(parts[1]),
                'density': float(parts[2]) if parts[2] != '0' else 0,
                'geometry': ' '.join(parts[3:])
            })

    # Extract surface information
    for i in range(editor.surface_block_start, editor.data_block_start - 1):
        parts = editor.lines[i].split()
        if len(parts) >= 2:
            surfaces.append({
                'number': int(parts[0]),
                'type': parts[1],
                'parameters': [float(p) for p in parts[2:] if p.replace('.', '').replace('-', '').isdigit()]
            })

    # Save to JSON
    with open(output_json, 'w') as f:
        json.dump({'cells': cells, 'surfaces': surfaces}, f, indent=2)

# Usage
extract_geometry_for_plot('input.i', 'geometry.json')
```

### Interface with Optimization Tools

```python
def optimize_parameters(base_input, parameter_ranges, objective_function):
    """Optimize MCNP input parameters

    parameter_ranges: {param_name: (min, max, step)}
    objective_function: function(results) -> score
    """
    import itertools

    best_score = float('inf')
    best_params = {}

    # Generate parameter combinations
    param_names = list(parameter_ranges.keys())
    param_values = [
        list(np.arange(r[0], r[1], r[2]))
        for r in parameter_ranges.values()
    ]

    for combination in itertools.product(*param_values):
        params = dict(zip(param_names, combination))

        # Create modified input
        editor = MCNPInputEditor(base_input)
        for param_name, value in params.items():
            # Apply parameter changes
            # (Implementation depends on parameter type)
            pass

        temp_input = f'temp_input_{hash(str(params))}.i'
        editor.save(temp_input)

        # Run MCNP (simplified - real implementation uses subprocess)
        # results = run_mcnp(temp_input)

        # Evaluate
        # score = objective_function(results)

        # Track best
        # if score < best_score:
        #     best_score = score
        #     best_params = params

    return best_params, best_score
```

---

## Advanced Find/Replace Techniques

### Context-Aware Replacement

```python
def context_aware_replace(line, find, replace, context):
    """Replace only if context conditions met"""

    # Example: Only replace in cell block
    if context == 'cell_block':
        if len(line.split()) >= 3 and line.split()[0].isdigit():
            return line.replace(find, replace)

    # Example: Only replace in data block
    elif context == 'data_block':
        if line.strip() and line.strip()[0].isalpha():
            return line.replace(find, replace)

    return line  # No replacement
```

### Multi-Pass Editing

```python
def multi_pass_edit(input_file, edit_passes):
    """Apply multiple editing passes in sequence

    edit_passes: list of (description, edit_function) tuples
    """
    current_file = input_file

    for i, (description, edit_func) in enumerate(edit_passes):
        print(f"Pass {i+1}: {description}")

        temp_file = f"temp_pass_{i}.i"
        edit_func(current_file, temp_file)
        current_file = temp_file

    # Final output
    os.rename(current_file, input_file.replace('.i', '_edited.i'))

# Usage
passes = [
    ("Update libraries", library_update_function),
    ("Scale geometry", geometry_scale_function),
    ("Adjust importances", importance_adjust_function)
]
multi_pass_edit('input.i', passes)
```

---

## Best Practices for Automation

### 1. Always Validate After Automated Edits

```python
def safe_automated_edit(input_file, edit_function):
    """Wrapper that validates after editing"""

    # Backup
    backup = input_file + '.backup'
    shutil.copy(input_file, backup)

    try:
        # Edit
        edit_function(input_file)

        # Validate
        if not validate_mcnp_input(input_file):
            print("Validation failed, restoring backup")
            shutil.copy(backup, input_file)
            return False

        return True

    except Exception as e:
        print(f"Error during edit: {e}")
        shutil.copy(backup, input_file)
        return False
```

### 2. Log All Changes

```python
def logged_edit(input_file, edit_function, log_file):
    """Edit with comprehensive logging"""

    with open(log_file, 'a') as log:
        timestamp = datetime.now().isoformat()
        log.write(f"\n{timestamp}: Starting edit\n")

        # Calculate hash before
        hash_before = calculate_file_hash(input_file)

        # Edit
        result = edit_function(input_file)

        # Calculate hash after
        hash_after = calculate_file_hash(input_file)

        log.write(f"  Before: {hash_before}\n")
        log.write(f"  After:  {hash_after}\n")
        log.write(f"  Result: {result}\n")
```

### 3. Test on Small Sample First

```python
def test_edit_on_sample(edit_function, sample_size=10):
    """Test editing function on small sample"""

    # Create sample file with first N lines
    with open('input.i', 'r') as f:
        sample_lines = [f.readline() for _ in range(sample_size)]

    with open('sample.i', 'w') as f:
        f.writelines(sample_lines)

    # Test on sample
    try:
        edit_function('sample.i')
        print("Sample edit successful, review sample.i")
        return True
    except Exception as e:
        print(f"Sample edit failed: {e}")
        return False
```

---

**END OF ADVANCED TECHNIQUES**

For basic editing workflows, see SKILL.md.
For detailed examples, see detailed_examples.md.
For error handling, see error_catalog.md.
For regex patterns, see regex_patterns_reference.md.
