# assets/ Directory

**Purpose:** Files used in OUTPUT (NOT loaded into Claude's context)

## What Goes Here

- **Template files** - Starting point MCNP inputs
- **Example input files** - Validated examples from example_files/
- **Description files** - Explanation for each example
- **Boilerplate** - Standard configurations

## Key Distinction

| Directory | Purpose | Loaded in Context? |
|-----------|---------|-------------------|
| references/ | Claude reads for information | ✅ Yes |
| scripts/ | Claude may execute | ✅ Yes (code only) |
| assets/ | Claude provides to user | ❌ No - for output |

## Subdirectories

### templates/
**Purpose:** Starting point MCNP input files

**Include:**
- `basic_template.i` - Simple problem (50-100 lines)
- `intermediate_template.i` - Moderate complexity (200-300 lines)
- `advanced_template.i` - Full-featured (500+ lines)
- `template_README.md` - Explanation of each template

**Template Requirements:**
- Valid MCNP syntax
- Commented placeholders for user customization
- Cover common use cases for this skill

### example_inputs/
**Purpose:** Validated examples from example_files/ directory

**Include:** 5-10 examples ranging from basic to advanced

**Source directories:**
- `basic_examples/` - Simple demonstrations
- `reactor-model_examples/` - Production-quality (PRIORITY)
- `variance-reduction_examples/` - VR techniques
- `unstructured-mesh_examples/` - Mesh tallies
- [Category-specific directories]

**File naming:**
- `example_01_[descriptive-name].i` - MCNP input
- `example_01_description.txt` - Explanation file

## Description File Format

For each example .i file, create matching _description.txt:

```
EXAMPLE: [Descriptive Title]
SOURCE: [Which example_files/ directory]
COMPLEXITY: [Basic / Intermediate / Advanced]

DEMONSTRATES:
- [Key feature 1]
- [Key feature 2]
- [Key feature 3]

EXPECTED RESULTS:
- [What output should show]
- [Key tally values or metrics]

KEY FEATURES:
- [Important aspect 1]
- [Important aspect 2]

RELATED SKILLS:
- [skill-1]: [Why related]
- [skill-2]: [Why related]

USAGE NOTES:
[Any special considerations for running this example]
```

## Selection Criteria

Choose examples that:
1. **Demonstrate skill-specific concepts**
2. **Range from simple to complex**
3. **Are validated** (run without fatal errors)
4. **Are reasonably sized** (<500 lines preferred)
5. **Show real-world applications**

## Priority Examples by Category

**Category A/B (Input Building):**
- Basic: 3 files from basic_examples/
- Advanced: 3-5 files from reactor-model_examples/
- Lattice: 2 files from reactor-model_examples/repeated_structures/

**Category D (Output Analysis):**
- All files from unstructured-mesh_examples/
- Output examples if available

**Category E (Advanced VR):**
- All files from variance-reduction_examples/
- Complex examples from reactor-model_examples/

**Category F (Utilities):**
- Mixed examples demonstrating utility functions

## Validation Checklist

Before adding example to assets/:
- [ ] File has valid MCNP syntax
- [ ] File runs without fatal errors (tested)
- [ ] File size reasonable (<500 lines preferred)
- [ ] Description file created
- [ ] Complexity level appropriate for skill
- [ ] Demonstrates skill-specific concepts

## User Experience

When user invokes skill, Claude can:
1. Reference example by name
2. Copy example to user's workspace
3. Explain example using description file
4. Modify template for user's specific case

Assets make skills immediately practical and useful!
