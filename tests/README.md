# MCNP6 Claude Skills Test Suite

Comprehensive test suite for all 31 MCNP6 Claude Skills.

## Test Structure

```
tests/
├── parsers/              # Parser tests
│   ├── test_input_parser.py
│   └── test_output_parser.py
├── utils/                # Utility tests
│   ├── test_transformations.py
│   └── test_lattice_indexing.py
├── skills/               # Skill tests (all 31 skills)
│   ├── test_input_creation.py    (6 skills)
│   ├── test_input_editing.py     (5 skills)
│   ├── test_validation.py        (5 skills)
│   ├── test_output_analysis.py   (5 skills)
│   ├── test_advanced.py          (5 skills)
│   └── test_utilities.py         (5 skills)
├── integration/          # End-to-end workflow tests
│   └── test_end_to_end.py
├── conftest.py           # Pytest configuration and fixtures
├── test_runner.py        # Main test runner script
└── README.md             # This file
```

## Running Tests

### Install Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
python tests/test_runner.py
```

Or using pytest directly:

```bash
pytest tests/ -v
```

### Run Category Tests

Test specific skill categories:

```bash
python tests/test_runner.py category parsers
python tests/test_runner.py category input_creation
python tests/test_runner.py category validation
python tests/test_runner.py category output_analysis
python tests/test_runner.py category advanced
python tests/test_runner.py category utilities
python tests/test_runner.py category integration
```

### Quick Smoke Test

Run fast subset of tests:

```bash
python tests/test_runner.py quick
```

### Run Specific Test File

```bash
pytest tests/skills/test_input_creation.py -v
```

### Run Specific Test

```bash
pytest tests/skills/test_input_creation.py::TestMCNPInputGenerator::test_generate_simple_sphere -v
```

## Test Coverage

The test suite validates:

### Foundation Libraries
- **Input Parser** (parsers/input_parser.py)
  - Parse 1,147+ example files
  - Extract cells, surfaces, data cards
  - Round-trip conversion (parse → regenerate → parse)
  
- **Output Parser** (parsers/output_parser.py)
  - Extract tally results
  - Parse KCODE criticality data
  - Identify warnings and fatal errors

- **Transformations** (utils/transformations.py)
  - Translation, rotation, combined transformations
  - TR card parsing
  
- **Lattice Indexing** (utils/lattice_indexing.py)
  - Hexagonal ring/position to i,j conversion
  - Rectangular 3D indexing

### Category A: Input Creation (6 skills)
- Generate simple problems (sphere, slab, criticality)
- Build geometry (surfaces, cells, CSG)
- Build materials (elements, compounds, isotopes)
- Build sources (point, distributed, KCODE)
- Build tallies (F1-F8, energy bins)
- Generate templates (reactor, dosimetry, shielding)

### Category B: Input Editing (5 skills)
- Edit existing files (search, replace, comment)
- Modify geometry (density, surfaces, cells)
- Apply transformations (translation, rotation)
- Add variance reduction (importance, weight windows, DXTRAN)
- MCNP5 → MCNP6 conversion

### Category C: Validation (5 skills)
- Validate input files (structure, cross-references)
- Check geometry (unused surfaces, broken references)
- Diagnose fatal errors (sourcc, lost particles)
- Analyze warnings (prioritization)
- Build dependency graphs

### Category D: Output Analysis (5 skills)
- Analyze OUTP files (version, particles run)
- Extract tally results (values, errors, CSV export)
- Analyze KCODE (k-effective, convergence)
- Check statistics (10 tests)
- Parse MCTAL files

### Category E: Advanced Operations (5 skills)
- Burnup/depletion (BURN cards, fission products)
- Mesh tallies (rectangular, cylindrical, unstructured)
- Lattices (hexagonal, rectangular, infinite)
- Weight window optimization (WWG, iterative)
- Parallel configuration (TASKS, SLURM scripts)

### Category F: Utilities (5 skills)
- Unit conversions (length, energy, density)
- Isotope lookup (ZAID, natural elements, atomic weight)
- Cross-section management (XSDIR parsing, availability)
- Physical constants (Avogadro, c, k_B, number density)
- Example finder (search, feature-based)

### Integration Tests
- Create → Validate workflow
- Create → Edit → Validate workflow
- Full problem lifecycle (geometry + materials + source + tallies)
- Analyze existing files

## Test Data

Tests use example files from `example_files/`:
- `simple.txt` - Simplest possible MCNP input
- `src1.txt` - Point source with energy bins
- `tal01.txt` - Sphere of HEU in water with materials
- 1,147+ additional examples for comprehensive validation

## Fixtures (conftest.py)

Available fixtures:
- `test_data_dir` - Path to example_files/
- `simple_input` - Simple.txt content
- `src1_input` - Src1.txt content
- `tal01_input` - Tal01.txt content
- `all_example_files` - Generator for all 1,147+ files

## Coverage Report

After running tests with coverage:

```bash
# View terminal report
pytest tests/ --cov=. --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

## Continuous Integration

For CI/CD pipelines:

```bash
pytest tests/ \
  --cov=. \
  --cov-report=xml \
  --junitxml=test-results.xml \
  -v
```

## Test Requirements

```
pytest>=7.0.0
pytest-cov>=4.0.0
numpy>=1.20.0
```

## Notes

- Some tests require actual MCNP example files to be present
- Tests marked with `@pytest.mark.slow` can be skipped: `pytest -m "not slow"`
- Integration tests may take longer to run
- Coverage goal: >80% for all modules
