# MCNP Input Builder Scripts

Python automation tools for MCNP input file generation and validation.

## Available Scripts

### 1. mcnp_input_generator.py
**Purpose:** Generate MCNP input files from templates and parameters

**Features:**
- Interactive mode with guided prompts
- JSON parameter file mode for automation
- Generates properly formatted three-block structure
- Handles cells, surfaces, materials, sources, tallies
- Automatic comment alignment and formatting

**Usage:**

**Interactive Mode (Recommended for Learning):**
```bash
python mcnp_input_generator.py --interactive
```
- Prompts for problem parameters
- Creates input file automatically
- Good for simple sphere problems

**Parameters File Mode (Recommended for Automation):**
```bash
python mcnp_input_generator.py --params params.json --output input.i
```

**Example params.json:**
```json
{
  "title": "Water Sphere Problem",
  "cells": [
    {"id": 1, "mat": 1, "dens": -1.0, "geom": "-1", "imp": 1, "vol": 4188.79, "comment": "Water"},
    {"id": 2, "mat": 0, "dens": 0, "geom": "1", "imp": 0, "comment": "Graveyard"}
  ],
  "surfaces": [
    {"id": 1, "type": "SO", "params": "10.0", "comment": "R=10 cm"}
  ],
  "materials": [
    {"id": 1, "composition": "1001 2 8016 1", "comment": "H2O", "thermal": "LWTR.01T"}
  ],
  "source": {
    "type": "SDEF",
    "spec": "POS=0 0 0 ERG=14.1"
  },
  "tallies": [
    {"type": 4, "cells": "1", "comment": "Flux", "energy_bins": "0.01 0.1 1 10"}
  ],
  "nps": 1000000
}
```

**Requirements:**
- Python 3.8 or later
- No external dependencies (standard library only)

---

### 2. validate_input_structure.py
**Purpose:** Pre-MCNP validation of input file structure and formatting

**Features:**
- Checks three-block structure (cells, surfaces, data)
- Validates blank line separators
- Detects tab characters (MCNP issue)
- Confirms MODE card is first data card
- Warns about missing particle designators
- Checks continuation line formatting
- Validates comment syntax
- Detects lines exceeding 128 characters

**Usage:**

**Basic Validation:**
```bash
python validate_input_structure.py input.i
```

**Verbose Mode (Show All Checks):**
```bash
python validate_input_structure.py input.i --verbose
```

**Exit Codes:**
- `0`: Validation passed (ready to run MCNP)
- `1`: Validation failed (errors found)
- `2`: File error (not found or empty)

**Example Output:**
```
Validating: input.i
======================================================================
[ERROR] Line 25: Missing blank line between cell cards and surface cards
  → Suggestion: Add a blank line after the last cell card

[WARNING] Line 47: F4 card may need particle designator (:N, :P, :E, etc.)
  → Suggestion: Add particle designator: F4:N (for neutrons)

======================================================================
✗ FAILED with 1 error(s), 1 warning(s)

Errors must be fixed before running MCNP.
```

**Integration with Workflow:**
```bash
# 1. Create input (manually or with generator)
python mcnp_input_generator.py --interactive

# 2. Validate structure
python validate_input_structure.py my_problem.i

# 3. Plot geometry
mcnp6 inp=my_problem.i ip

# 4. Run simulation
mcnp6 inp=my_problem.i outp=my_problem.o
```

**Requirements:**
- Python 3.8 or later
- No external dependencies (standard library only)

---

## Installation

No installation needed! Scripts use Python standard library only.

**Requirements:**
- Python 3.8 or later (check: `python --version`)

**Make scripts executable (Linux/Mac):**
```bash
chmod +x mcnp_input_generator.py
chmod +x validate_input_structure.py
```

**Run directly (Linux/Mac):**
```bash
./mcnp_input_generator.py --interactive
./validate_input_structure.py input.i
```

**Run with Python (Windows/Linux/Mac):**
```bash
python mcnp_input_generator.py --interactive
python validate_input_structure.py input.i
```

---

## Common Workflows

### Workflow 1: Quick Interactive Input
```bash
# Create input interactively
python mcnp_input_generator.py --interactive
# Prompts for: radius, material, energy, etc.
# Creates: interactive_problem.i

# Validate
python validate_input_structure.py interactive_problem.i

# Run
mcnp6 inp=interactive_problem.i
```

### Workflow 2: Automated Batch Generation
```bash
# Create parameter file (params.json)
cat > params.json << EOF
{
  "title": "Batch Problem 1",
  ...
}
EOF

# Generate input
python mcnp_input_generator.py --params params.json --output problem1.i

# Validate
python validate_input_structure.py problem1.i

# Run
mcnp6 inp=problem1.i
```

### Workflow 3: Parametric Study
```bash
# Loop over parameters
for radius in 5 10 15 20; do
  # Modify params.json with new radius
  python update_params.py --radius $radius --output params_r${radius}.json

  # Generate input
  python mcnp_input_generator.py \
    --params params_r${radius}.json \
    --output sphere_r${radius}.i

  # Validate
  python validate_input_structure.py sphere_r${radius}.i

  # Run
  mcnp6 inp=sphere_r${radius}.i &
done
```

---

## Error Messages

### Generator Errors
- **"Error: Parameters file not found"** - Check file path
- **"Error: Invalid JSON format"** - Validate JSON syntax
- **"Error: Missing required parameter"** - Check params.json completeness

### Validator Errors
- **"Missing blank line between blocks"** - Add blank line after cell/surface cards
- **"Tab character found"** - Replace tabs with spaces
- **"MODE card must be first"** - Move MODE before other data cards
- **"Missing particle designator"** - Add `:N`, `:P`, etc. to card

---

## Extending the Scripts

### Adding New Templates
Edit `mcnp_input_generator.py`:
```python
def create_shielding_input(params: Dict[str, Any], output_file: Path) -> None:
    """Create multi-layer shielding input."""
    # Implementation here
```

### Adding New Validation Checks
Edit `validate_input_structure.py`:
```python
def check_custom_rule(lines: List[str]) -> List[ValidationError]:
    """Check custom validation rule."""
    errors = []
    # Implementation here
    return errors
```

Then add to `validate_input_file()`:
```python
all_errors.extend(check_custom_rule(lines))
```

---

## Troubleshooting

**Problem:** "python: command not found"
**Solution:** Try `python3` instead of `python`

**Problem:** Scripts don't execute on Windows
**Solution:** Use `python script.py` instead of `./script.py`

**Problem:** "Permission denied" on Linux/Mac
**Solution:** Run `chmod +x script_name.py`

**Problem:** Validator reports false positives
**Solution:** Use `--verbose` flag to see all checks, report issues if persistent

---

## Further Help

- **Skill:** mcnp-input-builder - Complete input file creation guide
- **Templates:** `../templates/` - Template input files
- **Examples:** `../example_inputs/` - Real example files
- **References:** `../` - Format specifications

---

**Last Updated:** 2025-11-02 (Session 6 - Skill Revamp)
