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
version: "2.0.0"
---

# MCNP Knowledge Documentation Finder Skill

## Purpose

Use existing Python knowledge base tools to search and retrieve MCNP documentation, examples, and error solutions. Instead of guessing or inventing content, access the authoritative sources: 72 markdown documentation files and 1,147+ example files.

## When to Use This Skill

- Need detailed theory or physics explanation from documentation
- Looking for specific card syntax reference
- Searching for working example files by features
- Need to understand error messages and fixes
- Want to find documentation by keyword or topic
- Need context from primers or appendices
- Looking for validation benchmarks

## Prerequisites

- **knowledge_base_guide.md**: Comprehensive guide to all three Python tools
- **scripts/README.md**: Quick reference and integration examples
- Python 3.x in environment
- knowledge_base/ directory with helper scripts
- markdown_docs/ (72 files) and example_files/ (1,147+ files)

## Core Concepts

### Three Knowledge Base Tools

**1. doc_indexer.py** - Documentation Search
```
Purpose: Search 72 markdown documentation files
Coverage: Theory manual (13), User manual (21), Primers (6), Appendices (25)
Use for: Theory, card syntax, procedures, best practices
```

**2. example_finder.py** - Example File Search
```
Purpose: Search 1,147+ MCNP example input files
Coverage: Basic (100+), Criticality, V&V (120+), Reactor, VR (19), etc.
Use for: Working code, templates, validation benchmarks
```

**3. error_patterns.py** - Error Database
```
Purpose: Match error messages to known patterns with fixes
Coverage: Fatal errors, warnings, BAD TROUBLE messages
Use for: Quick error diagnosis and fix suggestions
```

**See knowledge_base_guide.md** for detailed documentation of all three tools.

### Documentation Structure

| Source | Files | Content |
|--------|-------|---------|
| theory_manual/ | 13 | Physics, algorithms, Monte Carlo theory |
| user_manual/ | 21 | Card syntax, input reference, procedures |
| primers/ | 6 | Tutorials (Criticality, Source, Shielding) |
| appendices/ | 25 | Cross sections, ZAIDs, data tables |
| examples/ | 6 | Worked example walkthroughs |

### Example File Categories

| Category | Count | Content |
|----------|-------|---------|
| basic/ | 100+ | Simple demonstration problems |
| criticality/ | Many | KCODE problems (Godiva, Jezebel, etc.) |
| vnv/ | 120+ | Validation & verification benchmarks |
| variance_reduction/ | 19 | VR technique demonstrations |
| reactor/ | Many | Reactor models (PWR, BWR, etc.) |
| unstructured_mesh/ | 15+ | UM geometry examples |

## Decision Tree: Which Tool to Use

```
START: Need information from knowledge base
  |
  +--> What type of information?
  |      |
  |      +--> Theory or explanation
  |      |      → Use doc_indexer
  |      |      → Search: "theory keywords"
  |      |      → Get: Theory manual sections
  |      |
  |      +--> Card syntax reference
  |      |      → Use doc_indexer
  |      |      → Method: get_card_documentation("CARD")
  |      |      → Get: User manual syntax sections
  |      |
  |      +--> Working example code
  |      |      → Use example_finder
  |      |      → Search: "problem type keywords"
  |      |      → Get: .i input files
  |      |
  |      +--> Error diagnosis
  |      |      → Use error_patterns
  |      |      → Method: match_error("error message")
  |      |      → Get: Cause, fix, example
  |      |
  |      └─> Learning tutorial
  |             → Use doc_indexer for primers
  |             → Use example_finder for simple examples
  |             → Get: Step-by-step guides + basic examples
  |
  +--> Execute Python tool
  |      ├─> Initialize tool
  |      ├─> Call index_all() (first time)
  |      └─> Execute search method
  |
  └─> Process results
         ├─> Read relevant files
         ├─> Extract needed information
         └─> Provide to user with file paths
```

## Tool Invocation

### Using doc_indexer.py

```python
from knowledge_base.doc_indexer import DocumentationIndexer

# Initialize and index
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Search by keyword
results = indexer.search("weight window theory", max_results=5)

# Get card syntax
sdef_docs = indexer.get_card_documentation("SDEF")

# Get by category
theory = indexer.get_by_category("theory")
primers = indexer.get_by_category("primers")
```

### Using example_finder.py

```python
from knowledge_base.example_finder import ExampleFinder

# Initialize and index
finder = ExampleFinder("example_files")
finder.index_all()

# Search by keyword
results = finder.search("fuel lattice", max_results=10)

# Get by features
crit_vr = finder.get_by_feature(criticality=True, variance_reduction=True)

# Get simple examples
simple = finder.get_simple_examples(count=5)

# Get by category
vnv = finder.get_by_category("vnv")
```

### Using error_patterns.py

```python
from knowledge_base.error_patterns import ErrorPatternDatabase

# Initialize
db = ErrorPatternDatabase()

# Match error
matches = db.match_error("bad trouble in subroutine sourcc")

# Get quick fix
fix = db.suggest_fix("material not defined")

# Browse errors
fatal = db.get_all_fatal_errors()
geometry_errors = db.get_by_category("geometry")
```

**See scripts/README.md** for detailed API documentation and integration examples.

---

## Use Case 1: Find Theory Documentation

**Problem**: Need to understand weight window theory before implementing

**Solution**:
```python
from knowledge_base.doc_indexer import DocumentationIndexer

indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()

# Search for theory
results = indexer.search("weight window variance reduction theory")

for r in results:
    print(f"File: {r.file_path}")
    print(f"Section: {r.title}")
```

**Expected Results:**
- theory_manual/05_Monte_Carlo_Statistics.md § Variance Reduction
- user_manual/.../05_08_Variance_Reduction_Cards.md § WWG Card
- primers/shielding_primer/05_Variance_Reduction.md

## Use Case 2: Find Working Example

**Problem**: Need example of fuel assembly with lattice

**Solution**:
```python
from knowledge_base.example_finder import ExampleFinder

finder = ExampleFinder("example_files")
finder.index_all()

# Search for lattice examples
lattice = finder.search("fuel lattice assembly")

# Filter for criticality + intermediate complexity
crit_lattice = [ex for ex in lattice
                if ex.has_criticality and
                ex.complexity in ['intermediate', 'advanced']]

for ex in crit_lattice[:3]:
    print(f"File: {ex.filename}")
    print(f"Description: {ex.description}")
    print(f"Path: {ex.file_path}")
```

## Use Case 3: Diagnose Error

**Problem**: MCNP gives "bad trouble in subroutine sourcc"

**Solution**:
```python
from knowledge_base.error_patterns import ErrorPatternDatabase

db = ErrorPatternDatabase()

error_msg = "bad trouble in subroutine sourcc"
matches = db.match_error(error_msg)

if matches:
    pattern = matches[0]
    print(f"Category: {pattern.category}")
    print(f"Cause: {pattern.cause}")
    print(f"Fix: {pattern.fix}")
```

## Use Case 4: Complete Implementation Workflow

**Problem**: Implement weight windows for shielding calculation

**Solution** (multi-tool workflow):
```python
# Step 1: Get theory (doc_indexer)
from knowledge_base.doc_indexer import DocumentationIndexer
indexer = DocumentationIndexer("markdown_docs")
indexer.index_all()
theory = indexer.search("weight window theory")

# Step 2: Get card syntax (doc_indexer)
ww_syntax = indexer.get_card_documentation("WWG")

# Step 3: Find working examples (example_finder)
from knowledge_base.example_finder import ExampleFinder
finder = ExampleFinder("example_files")
finder.index_all()
examples = finder.search("weight window")

# Now have: theory, syntax, and working examples
```

## Integration with Other Skills

### All MCNP Skills Use This

**Typical Workflow:**
```
1. User asks: "Implement weight windows"
2. mcnp-variance-reducer: Needs WW context
3. knowledge-docs-finder: Executes doc_indexer search
4. Claude reads: Relevant documentation sections
5. mcnp-variance-reducer: Implements with full understanding
6. User wants: "Show me example"
7. knowledge-docs-finder: Executes example_finder search
8. Claude presents: Working example file locations
```

### Error Debugging Integration

```
1. MCNP fails with error message
2. mcnp-fatal-error-debugger: Needs error context
3. knowledge-docs-finder: Uses error_patterns database
4. Claude provides: Error cause, fix, example
5. mcnp-fatal-error-debugger: Applies fix
```

## Quick Reference

| Need | Tool | Method | Example |
|------|------|--------|---------|
| Theory | doc_indexer | search() | `search("monte carlo theory")` |
| Card syntax | doc_indexer | get_card_documentation() | `get_card_documentation("F4")` |
| Primer tutorial | doc_indexer | search() | `search("criticality primer")` |
| Working example | example_finder | search() | `search("lattice fuel")` |
| Simple examples | example_finder | get_simple_examples() | `get_simple_examples(5)` |
| Benchmarks | example_finder | get_by_category() | `get_by_category("vnv")` |
| Error diagnosis | error_patterns | match_error() | `match_error("lost particle")` |
| Error fix | error_patterns | suggest_fix() | `suggest_fix(error_msg)` |

**Always consult knowledge_base_guide.md for comprehensive tool documentation.**

## Best Practices

1. **Use Tools, Don't Guess**: Always search knowledge base for authoritative information
2. **Check Documentation First**: Use doc_indexer before answering theory questions
3. **Find Examples, Don't Invent**: Use example_finder for real working code
4. **Leverage Error Database**: Check error_patterns before manual debugging
5. **Read Multiple Sources**: Cross-reference theory, user manual, examples
6. **Provide File Paths**: Tell user exactly where to find information
7. **Index Once**: Call `index_all()` once per session, then search fast
8. **Use Result Limits**: Set `max_results` to avoid overwhelming output

## When NOT to Use

- Simple unit conversions → Use **mcnp-unit-converter**
- Isotope data lookup → Use **mcnp-isotope-lookup**
- Physical constants → Use **mcnp-physical-constants**
- Example catalogs → Use **mcnp-example-finder** (for cataloged examples)

Use knowledge-docs-finder specifically for:
- Searching indexed documentation content
- Finding specific example files by features
- Matching error messages to known patterns

## References

- **knowledge_base_guide.md**: Comprehensive guide to all three Python tools
- **scripts/README.md**: API reference and integration examples
- **knowledge_base/doc_indexer.py**: Documentation search implementation
- **knowledge_base/example_finder.py**: Example file search implementation
- **knowledge_base/error_patterns.py**: Error pattern database implementation
- **markdown_docs/**: 72 documentation files (theory, user, primers, appendices)
- **example_files/**: 1,147+ MCNP example files (basic, criticality, vnv, etc.)

---

**End of MCNP Knowledge Documentation Finder Skill**
