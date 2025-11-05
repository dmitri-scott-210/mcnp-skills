---
category: F
name: mcnp-knowledge-docs-finder
description: Use knowledge_base Python tools (doc_indexer.py, example_finder.py, error_patterns.py) to search and retrieve MCNP documentation, examples, and error solutions when deeper context is needed
activation_keywords:
  - find documentation
  - search docs
  - need context
  - documentation for
  - find example
  - error help
  - knowledge base
---

# MCNP Knowledge Documentation Finder Skill

## Purpose

This utility skill teaches Claude how to use the existing knowledge_base Python tools to search and retrieve MCNP documentation, example files, and error solutions. Instead of guessing or creating content, Claude should use these tools to access the authoritative 72 markdown documentation files and 1,147+ example files.

## When to Use This Skill

- Need detailed theory or physics explanation from documentation
- Looking for specific card syntax reference
- Searching for working example files
- Need to understand error messages and fixes
- Want to find documentation by keyword or topic
- Need to locate specific manual chapters or sections
- Looking for examples with specific features (criticality, VR, etc.)
- Need context from primers or appendices

## Prerequisites

- Python 3.x available in environment
- knowledge_base/ directory with helper scripts
- markdown_docs/ directory with 72 documentation files
- example_files/ directory with 1,147+ MCNP examples
- Basic Python execution capability

## Core Concepts

### Available Knowledge Base Tools

**1. doc_indexer.py** - Documentation Search
```
Purpose: Index and search 72 markdown documentation files
Coverage:
  - Theory manual (13 files)
  - User manual (21 files)
  - Examples (6 files)
  - Primers (6 files)
  - Appendices (25 files)

Features:
  - Keyword search across all docs
  - Search by category (theory, user, primers, appendices)
  - Search by card type (SDEF, F4, M, etc.)
  - Returns relevant sections with file paths
```

**2. example_finder.py** - Example File Search
```
Purpose: Index and search 1,147+ MCNP example input files
Coverage:
  - Basic examples (100+)
  - Criticality examples
  - Intermediate examples
  - V&V benchmarks (120+)
  - Radiation protection examples
  - Reactor models
  - Safeguards examples
  - Unstructured mesh examples (15+)
  - Variance reduction examples (19)

Features:
  - Search by keyword
  - Filter by category
  - Filter by complexity (basic, intermediate, advanced)
  - Filter by features (criticality, tallies, VR)
  - Find simplest examples for beginners
```

**3. error_patterns.py** - Error Database
```
Purpose: Database of known MCNP errors with solutions
Coverage:
  - Fatal errors (geometry, source, data, physics)
  - Warnings (unused cells, overlaps, statistics)
  - Statistical quality failures

Features:
  - Match error message to known patterns
  - Get suggested fixes
  - Filter by category or severity
  - Get error cause and explanation
```

### Documentation Structure (markdown_docs/)

```
markdown_docs/
├── theory_manual/       (13 files - physics, algorithms)
├── user_manual/         (21 files - input reference, syntax)
├── primers/             (6 files - tutorials)
├── appendices/          (25 files - cross sections, data tables)
└── examples/            (6 files - worked examples)
```

### Example Files Structure (example_files/)

```
example_files/
├── basic/              (Simple demonstration problems)
├── criticality/        (KCODE problems)
├── intermediate/       (Multi-feature problems)
├── vnv/                (Validation & verification)
├── rad-protection/     (Shielding calculations)
├── reactor/            (Reactor models)
├── safeguards/         (Safeguards applications)
├── unstructured_mesh/  (UM examples)
└── variance_reduction/ (VR demonstrations)
```

## How to Use the Knowledge Base Tools

### Using doc_indexer.py

**Basic Usage**:
```python
from knowledge_base.doc_indexer import DocumentationIndexer

# Initialize
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Search by keyword
results = indexer.search("weight window", max_results=5)

# Each result has:
#   - file_path: Location of documentation
#   - title: Section title
#   - content: Section content
#   - keywords: Extracted keywords
#   - line_number: Where section starts

# Access specific category
theory_sections = indexer.get_by_category("theory")
user_sections = indexer.get_by_category("user")

# Get card documentation
sdef_docs = indexer.get_card_documentation("SDEF")
```

**Example Query** - "Find weight window theory":
```python
results = indexer.search("weight window theory")
# Returns sections from:
#   - theory_manual/05_Monte_Carlo_Statistics.md
#   - user_manual/chapter_05_input_cards/05_08_Variance_Reduction_Cards.md
```

### Using example_finder.py

**Basic Usage**:
```python
from knowledge_base.example_finder import ExampleFinder

# Initialize
finder = ExampleFinder("example_files")
finder.index_all()

# Search examples
results = finder.search("lattice fuel", max_results=10)

# Each result has:
#   - file_path: Location of example file
#   - filename: File name
#   - category: Example category
#   - description: Title line description
#   - has_criticality: Boolean
#   - has_tallies: Boolean
#   - has_variance_reduction: Boolean
#   - complexity: basic/intermediate/advanced

# Get by category
crit_examples = finder.get_by_category("criticality")

# Get by complexity
simple_examples = finder.get_by_complexity("basic")

# Get by features
vr_examples = finder.get_by_feature(variance_reduction=True)

# Get simplest examples for learning
beginner = finder.get_simple_examples(count=5)
```

**Example Query** - "Find criticality examples with lattices":
```python
crit = finder.get_by_feature(criticality=True)
lattice_crit = [ex for ex in crit if 'lattice' in ex.description.lower()]
```

### Using error_patterns.py

**Basic Usage**:
```python
from knowledge_base.error_patterns import ErrorPatternDatabase

# Initialize
db = ErrorPatternDatabase()

# Match error message
error_msg = "bad trouble in subroutine sourcc"
matches = db.match_error(error_msg)

# Each match has:
#   - pattern: Regex pattern
#   - category: Error category (source, geometry, material, etc.)
#   - severity: fatal/warning/info
#   - description: What the error means
#   - cause: Why it happens
#   - fix: How to fix it
#   - example: Code example of fix

# Get suggested fix
fix = db.suggest_fix(error_msg)

# Get all fatal errors
fatal_errors = db.get_all_fatal_errors()

# Get by category
geometry_errors = db.get_by_category("geometry")
```

**Example Query** - "Diagnose lost particle error":
```python
error_msg = "lost particle in cell 10"
matches = db.match_error(error_msg)

if matches:
    pattern = matches[0]
    print(f"Category: {pattern.category}")
    print(f"Cause: {pattern.cause}")
    print(f"Fix: {pattern.fix}")
```

## Use Cases

### Use Case 1: Find Theory Documentation for Feature

**Problem**: Need to understand weight window theory before implementing

**Solution using doc_indexer**:
```python
from knowledge_base.doc_indexer import DocumentationIndexer

indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Search for weight window theory
results = indexer.search("weight window theory", max_results=5)

for result in results:
    print(f"Found in: {result.file_path}")
    print(f"Section: {result.title}")
    print(f"Content preview: {result.content[:200]}...")

# Read full section from file_path for complete context
```

**Expected Results**:
- theory_manual/05_Monte_Carlo_Statistics.md § Variance Reduction
- user_manual/.../05_08_Variance_Reduction_Cards.md § WWG card

### Use Case 2: Find Example File for Problem Type

**Problem**: Need example of fuel assembly with lattice

**Solution using example_finder**:
```python
from knowledge_base.example_finder import ExampleFinder

finder = ExampleFinder("example_files")
finder.index_all()

# Search for lattice examples
lattice_examples = finder.search("lattice fuel assembly")

# Filter for criticality + intermediate complexity
crit_lattice = [ex for ex in lattice_examples
                if ex.has_criticality and
                ex.complexity in ['intermediate', 'advanced']]

# Show results
for ex in crit_lattice[:5]:
    print(f"File: {ex.filename}")
    print(f"Description: {ex.description}")
    print(f"Path: {ex.file_path}")
    print()

# Can then read the file to see implementation
```

### Use Case 3: Diagnose Error Message

**Problem**: MCNP gives "bad trouble in subroutine sourcc"

**Solution using error_patterns**:
```python
from knowledge_base.error_patterns import ErrorPatternDatabase

db = ErrorPatternDatabase()

error_msg = "bad trouble in subroutine sourcc"
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
else:
    print("Error not in database - check MCNP manual")
```

### Use Case 4: Find Card Syntax Documentation

**Problem**: Need detailed SDEF card syntax reference

**Solution using doc_indexer**:
```python
from knowledge_base.doc_indexer import DocumentationIndexer

indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Get SDEF card documentation
sdef_docs = indexer.get_card_documentation("SDEF")

for doc in sdef_docs:
    if "user_manual" in doc.file_path:
        print(f"Found SDEF reference:")
        print(f"  File: {doc.file_path}")
        print(f"  Section: {doc.title}")
        # Can then read the file for full syntax details
```

### Use Case 5: Find Simple Examples for Learning

**Problem**: New user needs simple examples to learn MCNP basics

**Solution using example_finder**:
```python
from knowledge_base.example_finder import ExampleFinder

finder = ExampleFinder("example_files")
finder.index_all()

# Get 5 simplest examples
simple = finder.get_simple_examples(count=5)

print("Recommended starting examples:")
for i, ex in enumerate(simple, 1):
    print(f"{i}. {ex.filename}")
    print(f"   {ex.description}")
    print(f"   Path: {ex.file_path}")
    print()
```

## Integration with Other Skills

### All MCNP Skills Use This

**Typical Workflow**:
```
1. User asks: "Implement weight windows for shielding"
2. mcnp-variance-reducer: Needs WW context
3. knowledge-docs-finder: Executes doc_indexer search
   → Finds theory and card reference
4. Claude reads: Relevant documentation sections
5. mcnp-variance-reducer: Implements with full understanding

6. User wants: "Show me example"
7. knowledge-docs-finder: Executes example_finder search
   → Finds VR examples
8. Claude: Presents example file locations
9. User can examine actual working examples
```

### Works With Error Debugging

**Error Resolution Workflow**:
```
1. MCNP fails with error message
2. mcnp-fatal-error-debugger: Needs error context
3. knowledge-docs-finder: Uses error_patterns database
   → Matches error, provides fix
4. mcnp-fatal-error-debugger: Applies fix
```

## Best Practices

1. **Always Use Tools for Context**: Don't guess, search the knowledge base
2. **Check Documentation First**: Use doc_indexer before answering theory questions
3. **Find Examples, Don't Invent**: Use example_finder for real working code
4. **Leverage Error Database**: Check error_patterns before debugging
5. **Read Multiple Sources**: Cross-reference theory, user manual, examples
6. **Provide File Paths**: Tell user exactly where to find information
7. **Show Tool Usage**: Demonstrate how to use Python tools
8. **Keep Tools Updated**: Note if knowledge base seems incomplete

## When NOT to Use

- Don't use Python tools for simple unit conversions (use unit-converter skill)
- Don't search docs for isotope data (use isotope-lookup skill)
- Don't search docs for physical constants (use physical-constants skill)
- Use these tools specifically for:
  - Documentation content search
  - Example file location
  - Error pattern matching

## Tool Invocation Template

**For Documentation Search**:
```python
# Template for finding documentation
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()
results = indexer.search("your search query", max_results=10)

# Access results
for r in results:
    print(f"{r.file_path} - {r.title}")
```

**For Example Search**:
```python
# Template for finding examples
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()

# Method 1: Keyword search
results = finder.search("lattice criticality")

# Method 2: Feature filter
results = finder.get_by_feature(
    criticality=True,
    variance_reduction=True
)

# Method 3: Category
results = finder.get_by_category("criticality")
```

**For Error Diagnosis**:
```python
# Template for error diagnosis
from knowledge_base.error_patterns import ErrorPatternDatabase
db = ErrorPatternDatabase()

# Match error message
matches = db.match_error("your error message")

# Get suggested fix
fix = db.suggest_fix("your error message")
```

## Quick Reference

| Need | Tool | Method |
|------|------|--------|
| Theory explanation | doc_indexer | search("theory topic") |
| Card syntax | doc_indexer | get_card_documentation("CARD") |
| User manual section | doc_indexer | get_by_category("user") |
| Working example | example_finder | search("problem type") |
| Simple example | example_finder | get_simple_examples(5) |
| Criticality example | example_finder | get_by_feature(criticality=True) |
| Error diagnosis | error_patterns | match_error("error msg") |
| Error fix | error_patterns | suggest_fix("error msg") |

## References

- **knowledge_base/doc_indexer.py**: Documentation search tool
- **knowledge_base/example_finder.py**: Example file search tool
- **knowledge_base/error_patterns.py**: Error pattern database
- **markdown_docs/**: 72 documentation markdown files
- **example_files/**: 1,147+ MCNP example files
- **Related Skills**: All MCNP skills benefit from this utility

---

**End of MCNP Knowledge Documentation Finder Skill**
