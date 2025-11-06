# MCNP Warning Analyzer - Scripts

**Purpose:** Python scripts for automated warning analysis, categorization, and prioritization.

---

## Available Scripts

### 1. mcnp_warning_analyzer.py

**Purpose:** Main class for warning extraction, categorization, and prioritization from MCNP output files.

**Usage:**
```python
from mcnp_warning_analyzer import MCNPWarningAnalyzer

# Initialize
analyzer = MCNPWarningAnalyzer()

# Analyze warnings
warnings = analyzer.analyze_warnings('outp')

# Review by category
for category, messages in warnings.items():
    if messages:
        print(f"\n{category.upper()} Warnings:")
        for msg in messages:
            print(f"  - {msg}")
```

**Key Methods:**
- `analyze_warnings(output_file)`: Extract and categorize all warnings
- `prioritize_warnings(warnings)`: Order warnings by severity
- `get_critical_warnings(warnings)`: Filter for critical warnings only

### 2. warning_prioritizer.py (Future)

**Purpose:** Advanced prioritization based on warning correlation and context.

**Planned Features:**
- Correlate related warnings
- Assign severity based on context
- Generate prioritized action list
- Track warning trends across runs

**Usage (Planned):**
```python
from warning_prioritizer import WarningPrioritizer

prioritizer = WarningPrioritizer()
action_list = prioritizer.create_action_list('outp')

for action in action_list:
    print(f"Priority {action.priority}: {action.description}")
```

### 3. statistical_analyzer.py (Future)

**Purpose:** Deep analysis of statistical check failures.

**Planned Features:**
- Parse tally fluctuation charts
- Analyze which of 10 checks failed
- Recommend specific fixes
- Estimate particles needed for convergence

---

## Integration Examples

### Example 1: Post-Run Warning Analysis

```python
from mcnp_warning_analyzer import MCNPWarningAnalyzer

def analyze_run(output_file):
    """Automated warning analysis after MCNP run."""
    analyzer = MCNPWarningAnalyzer()
    warnings = analyzer.analyze_warnings(output_file)

    # Generate report
    print("=" * 60)
    print("MCNP WARNING ANALYSIS")
    print("=" * 60)

    critical = []
    important = []
    info = []

    for cat, msgs in warnings.items():
        if cat in ['geometry', 'material', 'source']:
            critical.extend([(cat, m) for m in msgs])
        elif cat in ['tally', 'physics']:
            important.extend([(cat, m) for m in msgs])
        else:
            info.extend([(cat, m) for m in msgs])

    if critical:
        print("\n*** CRITICAL WARNINGS ***")
        for cat, msg in critical:
            print(f"  [{cat}] {msg}")

    if important:
        print("\n*** IMPORTANT WARNINGS ***")
        for cat, msg in important:
            print(f"  [{cat}] {msg}")

    if info:
        print(f"\n*** INFO ({len(info)} warnings) ***")

    print("\n" + "=" * 60)
    return len(critical), len(important), len(info)

# Usage
critical_count, important_count, info_count = analyze_run('outp')
```

### Example 2: Batch Processing

```python
import glob
from mcnp_warning_analyzer import MCNPWarningAnalyzer

def analyze_all_runs(directory):
    """Analyze warnings from multiple MCNP runs."""
    analyzer = MCNPWarningAnalyzer()

    for outp_file in glob.glob(f"{directory}/*outp"):
        print(f"\nAnalyzing: {outp_file}")
        warnings = analyzer.analyze_warnings(outp_file)

        critical = sum(len(v) for k, v in warnings.items()
                      if k in ['geometry', 'material'])

        if critical > 0:
            print(f"  ⚠ {critical} critical warnings")
        else:
            print(f"  ✓ No critical warnings")

# Usage
analyze_all_runs('/path/to/runs')
```

---

## Development Notes

### Adding New Warning Patterns

Warning patterns are defined in the MCNPWarningAnalyzer class. To add new patterns:

1. Identify warning message pattern
2. Determine category (geometry, material, source, tally, physics, other)
3. Add to appropriate detection method
4. Test with known warning cases

### Testing

Create test output files with known warnings:
```python
# Test case
test_warnings = {
    'material': 'warning.  1 materials had unnormalized fractions',
    'statistical': 'tally did not pass  3 of the 10 statistical checks',
    'entropy': 'Shannon entropy appears not to be converged'
}

for category, warning in test_warnings.items():
    # Verify correct categorization
    result = analyzer.categorize_warning(warning)
    assert result == category
```

---

## Future Enhancements

1. **Machine Learning:** Train classifier for warning severity
2. **Visualization:** Plot warning trends over multiple runs
3. **Auto-fix:** Suggest input modifications to resolve warnings
4. **Integration:** Direct integration with MCNP workflow tools
5. **Reporting:** Generate PDF/HTML warning analysis reports

---

## References

- **warning_catalog.md:** Complete warning reference
- **statistical_checks_guide.md:** Statistical check details
- **MCNP Manual:** Official warning documentation

---

**END OF SCRIPTS README**
