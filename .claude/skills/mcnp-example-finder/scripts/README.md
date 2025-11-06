# MCNP Example Finder - Scripts

**Purpose:** Python tools for searching and locating MCNP examples from documentation sources.

---

## Available Scripts

### 1. mcnp_example_finder.py

**Purpose:** Search for MCNP examples by keyword, problem type, or feature.

**Usage:**
```python
from mcnp_example_finder import MCNPExampleFinder

# Initialize finder
finder = MCNPExampleFinder()

# Search for examples
examples = finder.search_examples('lattice')

for ex in examples:
    print(f"{ex['name']}: {ex['description']}")
    print(f"  Location: {ex['location']}")
    print(f"  File: {ex['file']}")
```

**Key Methods:**
- `search_examples(keyword)`: Search by keyword (lattice, source, dose, etc.)
- `search_by_category(category)`: Search by category (criticality, shielding, geometry)
- `get_primer_examples(primer_name)`: Get all examples from specific primer
- `find_card_examples(card_name)`: Find examples using specific MCNP card

**Dependencies:**
- Requires access to example_catalog.md (parent directory)
- May require doc_indexer.py from knowledge_base for deep searches

### 2. doc_indexer.py (Future)

**Purpose:** Index MCNP documentation files for fast searching.

**Planned Features:**
- Build searchable index of primer chapters
- Extract example code blocks from markdown
- Create keyword mapping for quick lookup
- Generate example metadata (problem type, features used)
- Export examples to standalone input files

**Usage (Planned):**
```python
from doc_indexer import DocumentIndexer

indexer = DocumentIndexer()
indexer.index_directory('markdown_docs/primers/')

# Search indexed content
results = indexer.search('control rod insertion')

for result in results:
    print(f"Found in: {result['file']}")
    print(f"Section: {result['section']}")
    print(f"Example code: {result['code_snippet']}")
```

### 3. example_extractor.py (Future)

**Purpose:** Extract complete MCNP input examples from documentation.

**Planned Features:**
- Parse markdown code blocks for MCNP inputs
- Validate extracted inputs for completeness
- Add comments explaining key features
- Save examples to standalone .i files
- Generate example library for offline use

**Usage (Planned):**
```python
from example_extractor import ExampleExtractor

extractor = ExampleExtractor()

# Extract all lattice examples
lattice_examples = extractor.extract_by_category('lattice')

for ex in lattice_examples:
    # Save to file
    extractor.save_example(ex, f"examples/{ex['name']}.i")
```

---

## Integration Examples

### Example 1: Find Relevant Example for User Problem

```python
from mcnp_example_finder import MCNPExampleFinder

def find_example_for_problem(problem_description):
    """Find most relevant example for user's problem"""
    finder = MCNPExampleFinder()

    # Extract keywords from problem description
    keywords = extract_keywords(problem_description)

    # Search for examples
    all_examples = []
    for keyword in keywords:
        examples = finder.search_examples(keyword)
        all_examples.extend(examples)

    # Rank by relevance
    ranked = rank_by_relevance(all_examples, keywords)

    # Return top 3
    return ranked[:3]

# Usage
problem = "Need to model PWR fuel assembly with control rods"
examples = find_example_for_problem(problem)

for ex in examples:
    print(f"Suggested example: {ex['name']}")
    print(f"  {ex['description']}")
    print(f"  Location: {ex['location']}")
```

### Example 2: Interactive Example Browser

```python
from mcnp_example_finder import MCNPExampleFinder

def interactive_example_browser():
    """Interactive CLI for browsing examples"""
    finder = MCNPExampleFinder()

    print("MCNP Example Browser")
    print("=" * 50)

    # Show categories
    categories = finder.get_categories()
    print("\nCategories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")

    # Get user selection
    choice = input("\nSelect category (number): ")
    category = categories[int(choice) - 1]

    # Show examples
    examples = finder.search_by_category(category)
    print(f"\nExamples in {category}:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex['name']}")

    # Get example details
    choice = input("\nSelect example (number or 'q' to quit): ")
    if choice != 'q':
        example = examples[int(choice) - 1]
        print(f"\n{example['name']}")
        print(f"Description: {example['description']}")
        print(f"Location: {example['location']}")
        print(f"Features: {', '.join(example['features'])}")

# Usage
interactive_example_browser()
```

### Example 3: Automated Example Suggestion

```python
from mcnp_example_finder import MCNPExampleFinder

def suggest_examples_for_input(input_file):
    """Analyze MCNP input and suggest relevant examples"""
    finder = MCNPExampleFinder()

    # Parse input to identify features
    features = parse_input_features(input_file)

    suggestions = {}

    # Find examples for each feature
    if 'LAT' in features:
        suggestions['lattice'] = finder.search_examples('lattice')

    if 'KCODE' in features:
        suggestions['criticality'] = finder.search_by_category('criticality')

    if 'SDEF' in features:
        suggestions['source'] = finder.search_examples('source definition')

    if 'F5' in features or 'F4' in features:
        suggestions['tally'] = finder.search_examples('tally')

    return suggestions

# Usage
suggestions = suggest_examples_for_input('my_input.i')

for category, examples in suggestions.items():
    print(f"\n{category.upper()} Examples:")
    for ex in examples[:3]:  # Show top 3
        print(f"  - {ex['name']}: {ex['description']}")
```

---

## Example Catalog Integration

The scripts work with **example_catalog.md** (parent directory) which contains:

- **Documentation Sources**: Primers, User Manual, Test Suite
- **Examples by Problem Type**: Reactor physics, shielding, geometry, sources, tallies
- **Quick Reference Tables**: Feature → Documentation mapping

### Catalog Structure:

```markdown
## Documentation Sources
1. Criticality Primer → Lattice examples, KCODE setup
2. Source Primer → SDEF card usage, energy distributions
3. Shielding Primer → Dose tallies, variance reduction
4. User Manual → Complete card syntax, simple examples

## Examples by Category
- Reactor Physics: Godiva, fuel lattices, control rods
- Shielding: Point sources, dose conversion, deep penetration
- Geometry: Lattices, transformations, repeated structures
- Sources: Point, surface, volume, fusion
- Tallies: F1-F8, mesh tallies, dose tallies
```

---

## Development Notes

### Adding New Examples to Catalog

When new primers or documentation are added:

1. Review documentation for example problems
2. Extract key information:
   - Example name/description
   - Problem type
   - Features demonstrated
   - Location in documentation
3. Add to example_catalog.md in appropriate category
4. Update scripts to recognize new keywords

### Testing

Create test cases for search functionality:

```python
# Test keyword searches
test_cases = {
    'lattice': ['Example 9', 'Fuel assembly', 'LAT=1'],
    'dose': ['Dose conversion', 'DE/DF cards', 'Shielding'],
    'kcode': ['Godiva', 'Criticality', 'KSRC'],
}

for keyword, expected_terms in test_cases.items():
    results = finder.search_examples(keyword)
    for term in expected_terms:
        assert any(term in str(r) for r in results), f"Expected '{term}' in results"
```

---

## Future Enhancements

1. **Machine Learning**: Learn from user selections to improve relevance ranking
2. **Full-Text Search**: Index complete primer text, not just example summaries
3. **Code Extraction**: Automatically extract complete input files from documentation
4. **Visualization**: Show example thumbnails (geometry plots)
5. **Interactive Tutor**: Step-by-step walkthrough of example features
6. **Version Tracking**: Track example compatibility with MCNP versions

---

## References

- **example_catalog.md**: Complete catalog of examples
- **MCNP Primers**: Source documentation for examples
- **User Manual**: Chapter 3 (examples and usage)

---

**END OF SCRIPTS README**
