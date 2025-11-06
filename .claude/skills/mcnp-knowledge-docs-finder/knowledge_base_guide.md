# MCNP Knowledge Base Guide

**Purpose:** Comprehensive guide to using Python knowledge base tools for searching MCNP documentation, examples, and error solutions.

---

## Overview

The knowledge base provides three Python tools to search and retrieve information from:
- **72 markdown documentation files** (theory, user manual, primers, appendices)
- **1,147+ MCNP example files** (working input files)
- **Error pattern database** (known errors with solutions)

**Three Core Tools:**
1. **doc_indexer.py**: Search documentation for theory, syntax, procedures
2. **example_finder.py**: Search example files by keyword, features, complexity
3. **error_patterns.py**: Match error messages to known patterns and fixes

---

## Tool 1: doc_indexer.py - Documentation Search

### Purpose

Index and search 72 markdown documentation files to find theory explanations, card syntax, procedures, and reference material.

### Documentation Coverage

```
markdown_docs/
├── theory_manual/       (13 files - physics, algorithms, methods)
│   ├── 01_Introduction.md
│   ├── 02_Geometry.md
│   ├── 03_Cross_Section_Treatment.md
│   ├── 04_Particle_Physics.md
│   ├── 05_Monte_Carlo_Statistics.md
│   └── ... (transport theory, tallies, VR)
│
├── user_manual/         (21 files - input reference, syntax)
│   ├── chapter_01_introduction/
│   ├── chapter_02_getting_started/
│   ├── chapter_03_overview/
│   ├── chapter_04_geometry/
│   ├── chapter_05_input_cards/
│   │   ├── 05_01_Cell_Cards.md
│   │   ├── 05_04_Source_Cards.md
│   │   ├── 05_06_Tally_Cards.md
│   │   └── 05_08_Variance_Reduction_Cards.md
│   └── ... (complete input reference)
│
├── primers/             (6 files - tutorials)
│   ├── criticality_primer/
│   ├── source_primer/
│   ├── shielding_primer/
│   └── ... (step-by-step tutorials)
│
├── appendices/          (25 files - data tables, cross sections)
│   ├── A_Atomic_Weights.md
│   ├── B_Cross_Section_Libraries.md
│   ├── C_ZAID_Tables.md
│   └── ... (reference data)
│
└── examples/            (6 files - worked examples)
    └── ... (example walkthroughs)
```

### Usage Examples

#### Example 1: Find Theory Documentation

```python
from knowledge_base.doc_indexer import DocumentationIndexer

# Initialize and index
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Search for weight window theory
results = indexer.search("weight window variance reduction", max_results=5)

for result in results:
    print(f"File: {result.file_path}")
    print(f"Section: {result.title}")
    print(f"Content preview: {result.content[:200]}...")
    print(f"Line: {result.line_number}")
    print()
```

**Expected Results:**
- theory_manual/05_Monte_Carlo_Statistics.md § Variance Reduction Methods
- user_manual/chapter_05_input_cards/05_08_Variance_Reduction_Cards.md § WWG Card
- primers/shielding_primer/05_Variance_Reduction.md

#### Example 2: Find Card Syntax Reference

```python
# Get all documentation for SDEF card
sdef_docs = indexer.get_card_documentation("SDEF")

for doc in sdef_docs:
    if "user_manual" in doc.file_path:
        print(f"Card Reference: {doc.file_path}")
        print(f"Section: {doc.title}")
```

**Result:**
- user_manual/chapter_05_input_cards/05_04_Source_Cards.md § SDEF Card

#### Example 3: Search by Category

```python
# Get all theory manual sections
theory_sections = indexer.get_by_category("theory")

# Filter for Monte Carlo methods
mc_theory = [s for s in theory_sections if 'monte carlo' in s.title.lower()]

for section in mc_theory:
    print(f"{section.title} - {section.file_path}")
```

#### Example 4: Multi-Keyword Search

```python
# Find thermal scattering documentation
thermal_docs = indexer.search("thermal scattering S(alpha,beta) LWTR")

# Find criticality safety documentation
crit_safety = indexer.search("criticality safety kcode ksrc")

# Find tally documentation
tally_docs = indexer.search("F4 flux tally cell averaging")
```

### Result Object Structure

```python
class DocumentationResult:
    file_path: str         # Path to markdown file
    title: str             # Section title (## or ### heading)
    content: str           # Section content (markdown text)
    keywords: list[str]    # Extracted keywords
    line_number: int       # Line number where section starts
    category: str          # theory/user/primers/appendices/examples
```

---

## Tool 2: example_finder.py - Example File Search

### Purpose

Index and search 1,147+ MCNP input files to find working examples by keyword, feature, complexity, or category.

### Example File Coverage

```
example_files/
├── basic/              (100+ simple demonstration problems)
│   ├── simple_sphere.i
│   ├── cylinder_source.i
│   ├── point_detector.i
│   └── ... (learning examples)
│
├── criticality/        (KCODE problems)
│   ├── godiva_bare.i
│   ├── jezebel.i
│   ├── fuel_lattice.i
│   └── ... (critical assemblies)
│
├── intermediate/       (Multi-feature problems)
│   ├── reactor_lattice.i
│   ├── shielding_vr.i
│   └── ... (combined features)
│
├── vnv/                (120+ verification & validation benchmarks)
│   ├── icsbep/         (Critical experiments)
│   ├── sinbad/         (Shielding benchmarks)
│   └── ... (validated problems)
│
├── rad-protection/     (Shielding calculations)
│   ├── point_source_shield.i
│   ├── dose_calculation.i
│   └── ... (dose, shielding)
│
├── reactor/            (Reactor models)
│   ├── pwr_core.i
│   ├── bwr_assembly.i
│   └── ... (reactor physics)
│
├── safeguards/         (Safeguards applications)
│   └── ... (safeguards)
│
├── unstructured_mesh/  (15+ UM examples)
│   └── ... (UM geometry)
│
└── variance_reduction/ (19 VR demonstrations)
    ├── importance.i
    ├── weight_windows.i
    └── ... (VR techniques)
```

### Usage Examples

#### Example 1: Keyword Search

```python
from knowledge_base.example_finder import ExampleFinder

# Initialize and index
finder = ExampleFinder("example_files")
finder.index_all()

# Search for lattice examples
results = finder.search("fuel lattice", max_results=10)

for ex in results:
    print(f"File: {ex.filename}")
    print(f"Description: {ex.description}")
    print(f"Category: {ex.category}")
    print(f"Path: {ex.file_path}")
    print(f"Criticality: {ex.has_criticality}")
    print(f"Complexity: {ex.complexity}")
    print()
```

#### Example 2: Filter by Features

```python
# Find criticality examples with variance reduction
crit_vr_examples = finder.get_by_feature(
    criticality=True,
    variance_reduction=True
)

# Find examples with tallies
tally_examples = finder.get_by_feature(tallies=True)

# Find simple geometry examples
simple = finder.get_by_feature(complexity='basic')
```

#### Example 3: Search by Category

```python
# Get all criticality examples
crit_examples = finder.get_by_category("criticality")

# Get validation benchmarks
vnv_examples = finder.get_by_category("vnv")

# Get shielding examples
shield_examples = finder.get_by_category("rad-protection")
```

#### Example 4: Find Simple Examples for Learning

```python
# Get 5 simplest examples for beginners
simple = finder.get_simple_examples(count=5)

print("Recommended starting examples:")
for i, ex in enumerate(simple, 1):
    print(f"{i}. {ex.filename}")
    print(f"   {ex.description}")
    print(f"   Complexity: {ex.complexity}")
    print()
```

#### Example 5: Complex Query

```python
# Find intermediate criticality examples with lattices
results = finder.search("lattice fuel assembly")

# Filter for criticality + intermediate complexity
filtered = [ex for ex in results
            if ex.has_criticality and
            ex.complexity == 'intermediate']

for ex in filtered[:5]:
    print(f"{ex.filename}: {ex.description}")
```

### Result Object Structure

```python
class ExampleFileResult:
    file_path: str                # Full path to .i file
    filename: str                 # File name only
    category: str                 # basic/criticality/intermediate/etc.
    description: str              # First line title comment
    has_criticality: bool         # Contains KCODE
    has_tallies: bool             # Contains F1-F8 or FMESH
    has_variance_reduction: bool  # Contains IMP/WWG/DXTRAN
    complexity: str               # basic/intermediate/advanced
```

---

## Tool 3: error_patterns.py - Error Pattern Database

### Purpose

Match MCNP error messages to known patterns and provide diagnostic information, causes, and fixes.

### Error Coverage

**Fatal Errors:**
- Geometry errors (lost particles, overlaps, gaps)
- Source errors (invalid SDEF, KCODE problems)
- Material errors (undefined materials, bad cross sections)
- Data errors (missing libraries, invalid ZAIDs)
- Physics errors (bad MODE, invalid physics options)
- Input syntax errors (malformed cards)

**Warnings:**
- Unused cells
- Volume calculation issues
- Statistical quality failures
- Convergence warnings
- Deprecated syntax

**BAD TROUBLE Messages:**
- Geometry-related BAD TROUBLE
- Source-related BAD TROUBLE
- Numerical instability BAD TROUBLE
- Weight window BAD TROUBLE

### Usage Examples

#### Example 1: Match Error Message

```python
from knowledge_base.error_patterns import ErrorPatternDatabase

# Initialize
db = ErrorPatternDatabase()

# Match error message
error_msg = "bad trouble in subroutine sourcc of mcrun"
matches = db.match_error(error_msg)

if matches:
    pattern = matches[0]
    print(f"Error Type: {pattern.category}")
    print(f"Severity: {pattern.severity}")
    print(f"\nWhat it means:")
    print(f"  {pattern.description}")
    print(f"\nWhy it happens:")
    print(f"  {pattern.cause}")
    print(f"\nHow to fix:")
    print(f"  {pattern.fix}")
    if pattern.example:
        print(f"\nExample fix:")
        print(f"  {pattern.example}")
```

#### Example 2: Get Suggested Fix

```python
# Quick fix suggestion
error_msg = "fatal error.  material   3 has not been specified"
fix = db.suggest_fix(error_msg)

print(f"Suggested fix: {fix}")
```

#### Example 3: Browse Error Database

```python
# Get all fatal errors
fatal_errors = db.get_all_fatal_errors()

print(f"Total fatal error patterns: {len(fatal_errors)}")

# Get geometry errors
geometry_errors = db.get_by_category("geometry")

for err in geometry_errors:
    print(f"Pattern: {err.pattern}")
    print(f"Description: {err.description}")
    print()
```

#### Example 4: Diagnose Lost Particle

```python
error_msg = "lost particle at   5.12 3.69 0.00"
matches = db.match_error(error_msg)

if matches:
    pattern = matches[0]
    print(f"Category: {pattern.category}")  # geometry
    print(f"Cause: {pattern.cause}")
    # "Particle lost due to geometry overlap, gap, or wrong surface sense"
    print(f"Fix procedure:")
    print(f"  {pattern.fix}")
    # "1. Use VOID card test to check geometry
    #  2. Plot geometry at lost particle location
    #  3. Check surfaces in cells near lost location"
```

### Error Pattern Object Structure

```python
class ErrorPattern:
    pattern: str         # Regex pattern to match error message
    category: str        # geometry/source/material/data/physics/syntax
    severity: str        # fatal/warning/info
    description: str     # What the error means
    cause: str           # Why it happens
    fix: str             # How to fix it
    example: str         # Code example of fix (optional)
```

---

## Integration Workflows

### Workflow 1: Implement New Feature

```python
# User asks: "How do I use weight windows?"

# Step 1: Search theory
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()
theory = indexer.search("weight window theory")

# Step 2: Find card syntax
ww_syntax = indexer.get_card_documentation("WWG")

# Step 3: Find working examples
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()
examples = finder.search("weight window")

# Step 4: Filter for simple examples
simple_ww = [ex for ex in examples if ex.complexity == 'basic']

# Now have: theory, syntax reference, and working example
```

### Workflow 2: Debug Error

```python
# MCNP fails with error message

# Step 1: Match error to pattern
from knowledge_base.error_patterns import ErrorPatternDatabase
db = ErrorPatternDatabase()
matches = db.match_error(error_message)

# Step 2: Get fix procedure
if matches:
    fix = matches[0].fix
    # Apply fix steps

# Step 3: If geometry error, find geometry examples
if matches[0].category == "geometry":
    from knowledge_base.example_finder import ExampleFinder
    finder = ExampleFinder("example_files")
    finder.index_all()
    geom_examples = finder.search("geometry simple")
```

### Workflow 3: Learn MCNP Feature

```python
# New user wants to learn KCODE

# Step 1: Find primer tutorial
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()
kcode_primer = indexer.search("KCODE criticality primer")

# Step 2: Find simple examples
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()
simple_crit = finder.get_simple_examples(count=3)
crit_only = [ex for ex in simple_crit if ex.has_criticality]

# Step 3: Get card syntax reference
kcode_syntax = indexer.get_card_documentation("KCODE")

# Now have: tutorial, examples, and syntax reference
```

---

## Best Practices

### When to Use Each Tool

**Use doc_indexer when:**
- Need theory explanation (physics, algorithms)
- Need card syntax reference
- Looking for procedures or best practices
- Want manual sections or primer chapters

**Use example_finder when:**
- Need working input file
- Want to see feature in action
- Looking for validation benchmarks
- Need template to adapt

**Use error_patterns when:**
- MCNP produces error message
- Debugging failed run
- Need quick fix guidance
- Want to understand error meaning

### Search Tips

**For doc_indexer:**
- Use specific keywords: "weight window theory" not just "variance"
- Include card names: "SDEF energy distribution"
- Search multiple variations: "flux tally", "F4 tally", "cell averaging"

**For example_finder:**
- Start broad: "criticality" then filter
- Use feature filters for precise results
- Check complexity level for appropriate examples
- Browse by category first

**For error_patterns:**
- Use exact error text when possible
- If no match, search for key phrase
- Check category to understand error type

### Performance Notes

**Indexing:**
- First call to `index_all()` takes 1-2 seconds
- Subsequent searches are fast (milliseconds)
- Re-index if files change

**Result Limits:**
- Use `max_results` parameter to limit output
- Default is usually 10-20 results
- Sort results by relevance

---

## Quick Reference

### doc_indexer.py

```python
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Main methods
results = indexer.search("query", max_results=10)
card_docs = indexer.get_card_documentation("CARD")
theory = indexer.get_by_category("theory")
user = indexer.get_by_category("user")
primers = indexer.get_by_category("primers")
```

### example_finder.py

```python
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()

# Main methods
results = finder.search("query", max_results=10)
by_cat = finder.get_by_category("criticality")
by_feat = finder.get_by_feature(criticality=True, tallies=True)
simple = finder.get_simple_examples(count=5)
```

### error_patterns.py

```python
from knowledge_base.error_patterns import ErrorPatternDatabase
db = ErrorPatternDatabase()

# Main methods
matches = db.match_error("error message")
fix = db.suggest_fix("error message")
fatal = db.get_all_fatal_errors()
category = db.get_by_category("geometry")
```

---

## References

- **knowledge_base/doc_indexer.py**: Python implementation
- **knowledge_base/example_finder.py**: Python implementation
- **knowledge_base/error_patterns.py**: Python implementation
- **markdown_docs/**: 72 documentation files
- **example_files/**: 1,147+ example files

---

**END OF KNOWLEDGE BASE GUIDE**
