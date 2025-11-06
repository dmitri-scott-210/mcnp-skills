# MCNP Criticality Analyzer - Scripts

**Purpose:** Python tools for automated analysis of KCODE criticality calculations.

---

## Available Scripts

### 1. mcnp_criticality_analyzer.py

**Purpose:** Analyze MCNP KCODE output files to extract keff, check entropy convergence, and validate statistical quality.

**Usage:**
```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

# Initialize
analyzer = MCNPCriticalityAnalyzer()

# Analyze KCODE output
results = analyzer.analyze_kcode('outp')

# Access results
print(f"keff: {results['keff']} ± {results['error']}")
print(f"Relative error: {results['relative_error']}%")
print(f"Entropy converged: {results['entropy_converged']}")
print(f"Statistical quality: {results['quality']}")
```

**Key Methods:**
- `analyze_kcode(output_file)`: Complete KCODE analysis
- `extract_keff(output_file)`: Extract keff values and uncertainty
- `check_entropy_convergence(output_file)`: Verify source convergence
- `check_statistical_quality(output_file)`: Verify 10 checks passed
- `compare_keff(keff1, sigma1, keff2, sigma2)`: Statistical comparison

**Return Dict Structure:**
```python
{
    'keff': 1.00345,              # Combined keff
    'error': 0.00087,              # 1-sigma uncertainty
    'relative_error': 0.087,       # Relative error (%)
    'collision': 1.00321,          # Collision estimator
    'absorption': 1.00368,         # Absorption estimator
    'track_length': 1.00346,       # Track-length estimator
    'entropy_converged': True,     # Source convergence status
    'entropy_cycle': 45,           # Cycle where entropy plateaued
    'statistical_checks': 10,      # Number of checks passed (0-10)
    'quality': 'EXCELLENT',        # POOR/FAIR/GOOD/EXCELLENT
    'vov': 0.054,                  # Variance of variance
    'cycles_active': 100,          # Number of active cycles
    'cycles_inactive': 50,         # Number of inactive cycles
}
```

### Integration Examples

#### Example 1: Basic KCODE Analysis

```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

analyzer = MCNPCriticalityAnalyzer()
results = analyzer.analyze_kcode('output_file')

if results['entropy_converged']:
    print(f"✓ Source converged at cycle {results['entropy_cycle']}")
else:
    print(f"✗ Source not converged - increase nskip")

if results['statistical_checks'] == 10:
    print(f"✓ All statistical checks passed")
    print(f"keff = {results['keff']} ± {results['error']}")
else:
    print(f"✗ Only {results['statistical_checks']}/10 checks passed")
    print(f"Quality: {results['quality']}")
```

#### Example 2: Compare Two Configurations

```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

analyzer = MCNPCriticalityAnalyzer()

# Analyze two runs
run1 = analyzer.analyze_kcode('rods_out.outp')
run2 = analyzer.analyze_kcode('rods_in.outp')

# Compare keff values
comparison = analyzer.compare_keff(
    run1['keff'], run1['error'],
    run2['keff'], run2['error']
)

print(f"Configuration 1: keff = {run1['keff']} ± {run1['error']}")
print(f"Configuration 2: keff = {run2['keff']} ± {run2['error']}")
print(f"Difference: Δk = {comparison['delta_k']}")
print(f"Significance: {comparison['num_sigma']:.1f} σ")

if comparison['num_sigma'] > 3:
    print("Difference is statistically significant (>3σ)")
    print(f"Reactivity worth: {comparison['reactivity_pcm']} pcm")
```

#### Example 3: Batch Processing

```python
import glob
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

analyzer = MCNPCriticalityAnalyzer()

# Analyze all output files in directory
for outp_file in glob.glob("results/*.outp"):
    results = analyzer.analyze_kcode(outp_file)

    print(f"\n{outp_file}:")
    print(f"  keff = {results['keff']} ± {results['error']}")
    print(f"  Quality: {results['quality']}")

    if not results['entropy_converged']:
        print(f"  WARNING: Entropy not converged!")

    if results['statistical_checks'] < 10:
        print(f"  WARNING: {10-results['statistical_checks']} checks failed")
```

#### Example 4: Convergence Diagnostics

```python
from mcnp_criticality_analyzer import MCNPCriticalityAnalyzer

analyzer = MCNPCriticalityAnalyzer()

# Get detailed entropy analysis
entropy_data = analyzer.extract_entropy_history('outp')

print("Entropy Convergence Analysis:")
print(f"  Initial entropy (cycle 1): {entropy_data['initial']}")
print(f"  Final entropy: {entropy_data['final']}")
print(f"  Plateau cycle: {entropy_data['plateau_cycle']}")
print(f"  Max variation after plateau: {entropy_data['variation']}")

if entropy_data['oscillating']:
    print(f"  WARNING: Oscillating with period {entropy_data['period']} cycles")
    print(f"  Likely dominance ratio: ~{entropy_data['estimated_dr']}")
    print(f"  Recommended nskip: >{entropy_data['recommended_nskip']}")
```

---

## Future Enhancements

### 1. entropy_plotter.py (Planned)

**Purpose:** Generate entropy vs cycle plots automatically

**Features:**
- Plot entropy convergence
- Identify plateau region
- Detect oscillations
- Suggest optimal nskip

**Usage:**
```python
from entropy_plotter import EntropyPlotter

plotter = EntropyPlotter()
plotter.plot_entropy('outp', output='entropy_plot.png')
# Generates: Visual plot showing convergence behavior
```

### 2. keff_comparator.py (Planned)

**Purpose:** Compare multiple keff values with statistical tests

**Features:**
- Multi-case comparison
- Reactivity worth calculations
- Temperature coefficient analysis
- Sensitivity analysis

**Usage:**
```python
from keff_comparator import KeffComparator

comparator = KeffComparator()
cases = {
    'base': analyzer.analyze_kcode('base.outp'),
    'perturbed': analyzer.analyze_kcode('pert.outp'),
}
comparison = comparator.compare_all(cases)
```

### 3. dominance_ratio_estimator.py (Planned)

**Purpose:** Estimate dominance ratio from entropy oscillations

**Features:**
- Fourier analysis of entropy history
- DR estimation from oscillation period
- Convergence time prediction
- nskip recommendation

---

## Best Practices

### When to Use Automated Analysis

**Good Use Cases:**
- Initial screening of results
- Batch processing many runs
- Quick quality checks
- Extracting data for further analysis

**When Manual Review Needed:**
- Unexpected results
- Boundary cases (keff very close to 1.0)
- High-consequence calculations (safety analysis)
- Benchmark validation

### Validation Workflow

```python
# Step 1: Automated analysis
analyzer = MCNPCriticalityAnalyzer()
results = analyzer.analyze_kcode('outp')

# Step 2: Check quality
if results['quality'] in ['GOOD', 'EXCELLENT']:
    # Proceed to use results
    report_keff(results)
else:
    # Manual review needed
    manual_review_required(results)

# Step 3: Verify entropy
if not results['entropy_converged']:
    recommend_longer_nskip(results['entropy_cycle'])
```

---

## Error Handling

### Common Issues and Solutions

**Issue 1: Output File Not Found**
```python
try:
    results = analyzer.analyze_kcode('missing.outp')
except FileNotFoundError:
    print("Output file not found - check path")
```

**Issue 2: Incomplete KCODE Run**
```python
try:
    results = analyzer.analyze_kcode('incomplete.outp')
except ValueError as e:
    print(f"Incomplete output: {e}")
    # Output may not contain final keff table
```

**Issue 3: No Entropy Data**
```python
results = analyzer.analyze_kcode('no_entropy.outp')

if results['entropy_converged'] is None:
    print("No entropy data in output")
    print("Add PRDMP card to enable entropy tracking")
```

---

## References

- **kcode_analysis_guide.md**: Complete KCODE analysis procedures
- **entropy_convergence_guide.md**: Source convergence diagnostics
- **MCNP User Manual**: Chapter 5.8 (KCODE output format)

---

**END OF SCRIPTS README**
