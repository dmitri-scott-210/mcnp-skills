# MCNP Knowledge Documentation Finder - Scripts

**Purpose:** Python tools for searching MCNP documentation, examples, and error patterns from the knowledge base.

---

## Overview

The knowledge base provides three Python tools located in the parent `knowledge_base/` directory:

1. **doc_indexer.py** - Search 72 markdown documentation files
2. **example_finder.py** - Search 1,147+ MCNP example files
3. **error_patterns.py** - Match error messages to known patterns

These tools enable Claude to find authoritative information instead of guessing or inventing content.

---

## Tool 1: doc_indexer.py

### Purpose

Search and retrieve sections from MCNP documentation (theory manual, user manual, primers, appendices).

### Basic Usage

```python
from knowledge_base.doc_indexer import DocumentationIndexer

# Initialize with documentation directory
indexer = DocumentationIndexer("markdown_docs")

# Index all documentation files (do this once)
indexer.index_all()

# Search for documentation
results = indexer.search("weight window theory", max_results=5)

# Process results
for result in results:
    print(f"File: {result.file_path}")
    print(f"Section: {result.title}")
    print(f"Content: {result.content[:200]}...")
```

### Key Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `index_all()` | Index all markdown files | `indexer.index_all()` |
| `search(query, max_results=10)` | Search by keywords | `indexer.search("SDEF source")` |
| `get_card_documentation(card)` | Find card syntax | `indexer.get_card_documentation("F4")` |
| `get_by_category(category)` | Get sections by category | `indexer.get_by_category("theory")` |

### Categories

- `"theory"` - Theory manual (physics, algorithms)
- `"user"` - User manual (card syntax, input reference)
- `"primers"` - Primers (tutorials, step-by-step guides)
- `"appendices"` - Appendices (data tables, cross sections)
- `"examples"` - Examples (worked problems)

### Use Cases

**Find Theory Explanation:**
```python
# Search for Monte Carlo theory
theory_results = indexer.search("monte carlo sampling random number")

# Filter for theory manual only
theory_only = [r for r in theory_results if r.category == "theory"]
```

**Find Card Syntax:**
```python
# Get SDEF card documentation
sdef_docs = indexer.get_card_documentation("SDEF")

# Get all source card documentation
source_docs = indexer.search("source card SDEF SI SP")
```

**Find Primer Tutorial:**
```python
# Find criticality primer sections
crit_primer = indexer.search("criticality kcode primer")

# Filter for primer sections only
primer_sections = [r for r in crit_primer if r.category == "primers"]
```

---

## Tool 2: example_finder.py

### Purpose

Search and retrieve MCNP example input files by keyword, feature, category, or complexity.

### Basic Usage

```python
from knowledge_base.example_finder import ExampleFinder

# Initialize with example directory
finder = ExampleFinder("example_files")

# Index all example files (do this once)
finder.index_all()

# Search for examples
results = finder.search("fuel lattice", max_results=10)

# Process results
for ex in results:
    print(f"File: {ex.filename}")
    print(f"Description: {ex.description}")
    print(f"Category: {ex.category}")
    print(f"Path: {ex.file_path}")
```

### Key Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `index_all()` | Index all example files | `finder.index_all()` |
| `search(query, max_results=10)` | Search by keywords | `finder.search("lattice")` |
| `get_by_category(category)` | Get examples by category | `finder.get_by_category("criticality")` |
| `get_by_feature(**kwargs)` | Filter by features | `finder.get_by_feature(criticality=True)` |
| `get_simple_examples(count=5)` | Get simplest examples | `finder.get_simple_examples(5)` |

### Categories

- `"basic"` - Simple demonstration problems
- `"criticality"` - KCODE problems
- `"intermediate"` - Multi-feature problems
- `"vnv"` - Validation & verification benchmarks
- `"rad-protection"` - Shielding calculations
- `"reactor"` - Reactor models
- `"safeguards"` - Safeguards applications
- `"unstructured_mesh"` - UM examples
- `"variance_reduction"` - VR demonstrations

### Feature Filters

```python
# Examples with criticality
crit = finder.get_by_feature(criticality=True)

# Examples with variance reduction
vr = finder.get_by_feature(variance_reduction=True)

# Examples with tallies
tallies = finder.get_by_feature(tallies=True)

# Combined filters
crit_vr = finder.get_by_feature(
    criticality=True,
    variance_reduction=True
)
```

### Complexity Levels

- `"basic"` - Simple, single-feature examples
- `"intermediate"` - Multi-feature examples
- `"advanced"` - Complex, realistic problems

```python
# Get basic examples only
basic = [ex for ex in results if ex.complexity == "basic"]
```

### Use Cases

**Find Learning Examples:**
```python
# Get 5 simplest examples for beginners
simple = finder.get_simple_examples(count=5)

for i, ex in enumerate(simple, 1):
    print(f"{i}. {ex.filename}: {ex.description}")
```

**Find Feature-Specific Examples:**
```python
# Find criticality examples with lattices
crit = finder.get_by_feature(criticality=True)
lattice_crit = [ex for ex in crit if 'lattice' in ex.description.lower()]

# Find shielding examples with dose tallies
shield = finder.get_by_category("rad-protection")
dose = [ex for ex in shield if 'dose' in ex.description.lower()]
```

**Find Validation Benchmarks:**
```python
# Get V&V benchmarks
vnv = finder.get_by_category("vnv")

# Filter for specific benchmark type
icsbep = [ex for ex in vnv if 'icsbep' in ex.file_path.lower()]
```

---

## Tool 3: error_patterns.py

### Purpose

Match MCNP error messages to known patterns and provide diagnostic information, causes, and fixes.

### Basic Usage

```python
from knowledge_base.error_patterns import ErrorPatternDatabase

# Initialize database
db = ErrorPatternDatabase()

# Match error message
error_msg = "bad trouble in subroutine sourcc"
matches = db.match_error(error_msg)

# Get information
if matches:
    pattern = matches[0]
    print(f"Category: {pattern.category}")
    print(f"Severity: {pattern.severity}")
    print(f"Cause: {pattern.cause}")
    print(f"Fix: {pattern.fix}")
```

### Key Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `match_error(error_msg)` | Match error to patterns | `db.match_error("lost particle")` |
| `suggest_fix(error_msg)` | Get quick fix suggestion | `db.suggest_fix("material not defined")` |
| `get_all_fatal_errors()` | Get all fatal error patterns | `db.get_all_fatal_errors()` |
| `get_by_category(category)` | Get errors by category | `db.get_by_category("geometry")` |

### Error Categories

- `"geometry"` - Geometry errors (lost particles, overlaps, gaps)
- `"source"` - Source errors (SDEF, KCODE problems)
- `"material"` - Material errors (undefined materials, bad cross sections)
- `"data"` - Data errors (missing libraries, invalid ZAIDs)
- `"physics"` - Physics errors (bad MODE, invalid options)
- `"syntax"` - Input syntax errors (malformed cards)

### Severity Levels

- `"fatal"` - Fatal errors (stop execution)
- `"warning"` - Warnings (run continues)
- `"info"` - Informational messages

### Use Cases

**Quick Error Diagnosis:**
```python
# Get quick fix for error
error_msg = "fatal error.  material   3 has not been specified"
fix = db.suggest_fix(error_msg)
print(f"Fix: {fix}")
```

**Detailed Error Analysis:**
```python
# Get full error information
matches = db.match_error(error_msg)

if matches:
    pattern = matches[0]
    print(f"Error Type: {pattern.category}")
    print(f"Severity: {pattern.severity}")
    print(f"\nWhat it means: {pattern.description}")
    print(f"\nWhy it happens: {pattern.cause}")
    print(f"\nHow to fix: {pattern.fix}")
    if pattern.example:
        print(f"\nExample: {pattern.example}")
```

**Browse Error Database:**
```python
# Get all geometry errors
geom_errors = db.get_by_category("geometry")

for err in geom_errors:
    print(f"Pattern: {err.pattern}")
    print(f"Fix: {err.fix}")
    print()
```

---

## Integration Examples

### Example 1: Complete Feature Implementation Workflow

```python
# User asks: "How do I implement weight windows?"

# Step 1: Find theory
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()
theory = indexer.search("weight window theory", max_results=3)

print("Theory references:")
for t in theory:
    print(f"  {t.file_path} - {t.title}")

# Step 2: Find card syntax
ww_syntax = indexer.get_card_documentation("WWG")
print("\nCard syntax:")
for s in ww_syntax:
    print(f"  {s.file_path}")

# Step 3: Find working examples
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()
examples = finder.search("weight window", max_results=5)

print("\nWorking examples:")
for ex in examples:
    print(f"  {ex.filename}: {ex.description}")
```

### Example 2: Error Debugging Workflow

```python
# MCNP run failed with error

error_message = "bad trouble in subroutine sourcc of mcrun"

# Step 1: Match error to pattern
from knowledge_base.error_patterns import ErrorPatternDatabase
db = ErrorPatternDatabase()
matches = db.match_error(error_message)

if matches:
    pattern = matches[0]
    print(f"Error: {pattern.category}")
    print(f"Fix: {pattern.fix}")

    # Step 2: Find relevant documentation
    from knowledge_base.doc_indexer import DocumentationIndexer
    indexer = DocumentationIndexer("markdown_docs")
    indexer.index_all()

    # Search for source documentation
    if pattern.category == "source":
        source_docs = indexer.search("SDEF source definition")
        print("\nRelevant docs:")
        for doc in source_docs[:3]:
            print(f"  {doc.file_path}")
```

### Example 3: Learning Workflow for Beginners

```python
# New user wants to learn MCNP

# Step 1: Get simple examples
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()
simple = finder.get_simple_examples(count=5)

print("Start with these examples:")
for i, ex in enumerate(simple, 1):
    print(f"{i}. {ex.filename}")
    print(f"   {ex.description}")
    print(f"   Path: {ex.file_path}")

# Step 2: Get getting started documentation
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()
getting_started = indexer.search("getting started tutorial")

print("\nRead these sections:")
for doc in getting_started[:3]:
    print(f"  {doc.title} - {doc.file_path}")
```

---

## Best Practices

### Search Strategy

1. **Start with doc_indexer** for understanding
2. **Use example_finder** for implementation patterns
3. **Use error_patterns** only when debugging

### Keyword Tips

- Use specific terms: "weight window" not just "variance"
- Include card names: "SDEF energy distribution"
- Try multiple phrasings: "flux tally", "F4", "cell averaging"

### Result Management

- Use `max_results` to limit output
- Filter results by category or features
- Sort by relevance or complexity

### Performance

- Call `index_all()` only once per session
- Searches are fast after initial indexing
- Re-index if files are added or changed

---

## Future Enhancements

1. **Semantic Search**: Use embeddings for better relevance
2. **Code Extraction**: Extract code snippets from documentation
3. **Cross-Referencing**: Link related docs, examples, errors
4. **Learning Paths**: Generate tutorial sequences
5. **Versioning**: Track MCNP version compatibility

---

## References

- **knowledge_base_guide.md**: Comprehensive guide to all three tools
- **knowledge_base/doc_indexer.py**: Documentation search implementation
- **knowledge_base/example_finder.py**: Example file search implementation
- **knowledge_base/error_patterns.py**: Error pattern database implementation
- **markdown_docs/**: 72 documentation files
- **example_files/**: 1,147+ example files

---

**END OF SCRIPTS README**
