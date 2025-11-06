# MCNP Fatal Error Debugger - Scripts

**Purpose:** Python scripts for automated error diagnosis and analysis.

---

## Available Scripts

### 1. mcnp_fatal_error_debugger.py

**Purpose:** Main class for fatal error diagnosis using error pattern database.

**Usage:**
```python
from mcnp_fatal_error_debugger import MCNPFatalErrorDebugger

# Initialize
debugger = MCNPFatalErrorDebugger()

# Diagnose errors from output file
result = debugger.diagnose_error('outp')
print(f"Found {result['count']} fatal errors")

for error in result['errors']:
    print(f"Error: {error['message']}")
    print(f"Fix: {error['fix']}")
```

**Dependencies:**
- Requires error_patterns.py from knowledge_base (parent directory)
- Accesses ErrorPatternDatabase for pattern matching

**Key Methods:**
- `diagnose_error(output_file)`: Parse OUTP file for fatal errors
- `suggest_fix(error_message)`: Get fix suggestion for specific error
- `get_common_errors()`: Retrieve all known fatal error patterns

### 2. error_parser.py (Future)

**Purpose:** Parse MCNP output files to extract error messages, warnings, and diagnostic information.

**Planned Features:**
- Extract fatal error messages
- Extract warning messages
- Extract BAD TROUBLE messages
- Parse event logs for lost particles
- Generate error summary reports

**Usage (Planned):**
```python
from error_parser import MCNPOutputParser

parser = MCNPOutputParser()
errors = parser.parse_output('outp')

# Get fatal errors
fatal = errors.get_fatal_errors()

# Get warnings
warnings = errors.get_warnings()

# Get lost particle events
lost = errors.get_lost_particles()
```

### 3. lost_particle_analyzer.py (Future)

**Purpose:** Analyze lost particle events to identify geometry error patterns.

**Planned Features:**
- Parse event logs
- Identify problematic surfaces
- Suggest plotting commands
- Detect common patterns (overlaps vs gaps)
- Generate geometry debugging commands

**Usage (Planned):**
```python
from lost_particle_analyzer import LostParticleAnalyzer

analyzer = LostParticleAnalyzer()
analysis = analyzer.analyze_outp('outp')

# Get lost particle locations
locations = analysis.get_lost_locations()

# Get suggested plot commands
plot_commands = analysis.suggest_plots()

# Identify pattern (overlap, gap, wrong sense)
pattern = analysis.identify_pattern()
```

---

## Integration Examples

### Example 1: Automated Error Diagnosis

```python
from mcnp_fatal_error_debugger import MCNPFatalErrorDebugger

def diagnose_run(output_file):
    """Diagnose MCNP run and print recommendations"""
    debugger = MCNPFatalErrorDebugger()
    result = debugger.diagnose_error(output_file)

    if result['count'] == 0:
        print("No fatal errors found!")
        return

    # Focus on first error
    first_error = result['errors'][0]
    print(f"Primary Fatal Error:")
    print(f"  Message: {first_error['message']}")
    print(f"  Suggested Fix: {first_error['fix']}")

    if first_error['example']:
        print(f"  Example: {first_error['example']}")

    if result['count'] > 1:
        print(f"\nNote: {result['count']-1} additional errors detected.")
        print("These may be cascading from the first error.")
        print("Fix the first error and re-run before addressing others.")

# Usage
diagnose_run('path/to/outp')
```

### Example 2: Batch Processing

```python
import glob
from mcnp_fatal_error_debugger import MCNPFatalErrorDebugger

def diagnose_all_runs(directory):
    """Diagnose all MCNP runs in directory"""
    debugger = MCNPFatalErrorDebugger()

    for outp_file in glob.glob(f"{directory}/*outp"):
        print(f"\nAnalyzing: {outp_file}")
        result = debugger.diagnose_error(outp_file)

        if result['count'] > 0:
            print(f"  Errors found: {result['count']}")
            print(f"  First error: {result['errors'][0]['message']}")
        else:
            print("  No errors")

# Usage
diagnose_all_runs('/path/to/mcnp/runs')
```

---

## Development Notes

### Adding New Error Patterns

Error patterns are managed by the ErrorPatternDatabase in the parent knowledge_base module. To add new patterns:

1. Identify error message pattern
2. Determine fix procedure
3. Add to error_patterns.py database
4. Test with known error cases

### Testing

Create test cases with known errors:
```python
# Test material not defined
test_cases = {
    'material_missing': 'fatal error.  material   3 has not been specified',
    'surface_missing': 'fatal error.  surface    15 not defined',
    'lost_particle': 'particle lost at   5.12 3.69 0.00'
}

for test_name, error_msg in test_cases.items():
    fix = debugger.suggest_fix(error_msg)
    print(f"{test_name}: {fix}")
```

---

## Future Enhancements

1. **GUI Interface:** Visual interface for error diagnosis
2. **Plot Generation:** Automatic geometry plot creation at lost particle locations
3. **Fix Automation:** Automatic correction of common errors
4. **Learning System:** Machine learning to improve error pattern recognition
5. **Integration:** Direct integration with MCNP workflow tools

---

## References

- **fatal_error_catalog.md:** Complete error catalog
- **geometry_error_guide.md:** Geometry debugging procedures
- **source_error_guide.md:** Source error details
- **MCNP Manual:** Official documentation

---

**END OF SCRIPTS README**
