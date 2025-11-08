# Quality Assurance Workflows

Implementing validation checkpoints in multi-physics workflows.

## Overview

Quality assurance in MCNP workflows prevents costly errors by catching problems early:
- **Pre-Run Validation**: Find errors before running (saves computation time)
- **Mid-Run Monitoring**: Detect issues during execution
- **Post-Run Validation**: Verify results make physical sense

**Philosophy**: Fail fast, fail loudly, provide actionable error messages.

---

## Pre-Run Validation

### Input File Syntax Checking

**Purpose**: Catch syntax errors, dimension mismatches, undefined references

**Implementation**:

```python
def validate_mcnp_input(filename):
    """
    Comprehensive MCNP input validation.

    Args:
        filename: Path to MCNP input file

    Returns:
        dict with 'valid' (bool) and 'issues' (list of strings)
    """
    issues = []

    # Read file
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return {'valid': False, 'issues': [f'File not found: {filename}']}

    # 1. Check three-block structure
    if not _has_three_block_structure(content):
        issues.append("Missing proper three-block structure (cells/surfaces/data)")

    # 2. Check FILL arrays
    lattice_cells = _extract_lattice_cells(content)
    for cell in lattice_cells:
        expected, actual = _check_fill_dimensions(cell)
        if expected != actual:
            issues.append(
                f"Cell {cell['number']}: FILL array dimension mismatch - "
                f"expected {expected} elements, found {actual}"
            )

    # 3. Check cross-references
    defined_surfaces = _extract_defined_surfaces(content)
    referenced_surfaces = _extract_referenced_surfaces(content)
    undefined_surfs = referenced_surfaces - defined_surfaces
    if undefined_surfs:
        issues.append(f"Undefined surfaces referenced: {sorted(undefined_surfs)}")

    defined_materials = _extract_defined_materials(content)
    referenced_materials = _extract_referenced_materials(content)
    undefined_mats = referenced_materials - defined_materials
    if undefined_mats:
        issues.append(f"Undefined materials referenced: {sorted(undefined_mats)}")

    # 4. Check for numbering conflicts
    all_cell_nums = _extract_cell_numbers(content)
    duplicates = _find_duplicates(all_cell_nums)
    if duplicates:
        issues.append(f"Duplicate cell numbers: {sorted(duplicates)}")

    all_surf_nums = _extract_surface_numbers(content)
    duplicates = _find_duplicates(all_surf_nums)
    if duplicates:
        issues.append(f"Duplicate surface numbers: {sorted(duplicates)}")

    # 5. Check physical constraints
    materials = _extract_materials(content)
    for mat_num, composition in materials.items():
        total_frac = sum(comp['fraction'] for comp in composition)
        if abs(total_frac - 1.0) > 0.01:
            issues.append(
                f"Material m{mat_num}: atom fractions sum to {total_frac:.4f}, "
                f"expected 1.0"
            )

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': []  # Could add non-fatal warnings
    }


def _check_fill_dimensions(cell):
    """
    Check FILL array dimensions match lattice specification.

    Args:
        cell: Dictionary with 'lat_spec' and 'fill_data'

    Returns:
        Tuple of (expected_elements, actual_elements)
    """
    # Parse lattice specification
    # Example: "lat=1 fill=-11:11 -11:11 0:0"
    import re
    match = re.search(r'fill=(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)', cell['definition'])

    if not match:
        return None, None

    x1, x2, y1, y2, z1, z2 = map(int, match.groups())

    nx = x2 - x1 + 1
    ny = y2 - y1 + 1
    nz = z2 - z1 + 1

    expected = nx * ny * nz

    # Count fill elements
    fill_data = cell.get('fill_data', '')
    actual = len(fill_data.split())

    return expected, actual


# Helper functions
def _extract_defined_surfaces(content):
    """Extract set of defined surface numbers."""
    surfaces = set()

    in_surface_block = False
    for line in content.split('\n'):
        # Detect surface block start
        if re.match(r'^\s*$', line):
            in_surface_block = True
            continue

        # Detect data block start (end of surfaces)
        if in_surface_block and line.strip().lower().startswith(('mode', 'kcode', 'sdef')):
            break

        # Extract surface number
        if in_surface_block:
            match = re.match(r'^\s*(\d+)', line)
            if match:
                surfaces.add(int(match.group(1)))

    return surfaces


def _extract_referenced_surfaces(content):
    """Extract set of referenced surface numbers from cell cards."""
    surfaces = set()

    # Parse cell cards
    # Example: "1 1 -10.8  -1001 1002 #3  imp:n=1"
    for line in content.split('\n'):
        # Skip comment lines
        if line.strip().startswith('c'):
            continue

        # Extract surface references (numbers with optional - or #)
        matches = re.findall(r'[#-]?(\d+)', line)
        for match in matches:
            surfaces.add(int(match))

    return surfaces
```

### FILL Array Validation

**Specific validator for lattice fills**:

```python
def validate_fill_arrays(filename):
    """
    Validate all FILL arrays in file.

    Returns detailed report of each lattice.
    """
    with open(filename, 'r') as f:
        content = f.read()

    lattice_cells = _extract_lattice_cells(content)

    results = []

    for cell in lattice_cells:
        cell_num = cell['number']
        lat_type = cell['lat_type']
        dimensions = cell['dimensions']
        fill_data = cell['fill_data']

        # Calculate expected elements
        if lat_type == 1:  # Rectangular
            nx, ny, nz = dimensions
            expected = nx * ny * nz
        elif lat_type == 2:  # Hexagonal
            # Hexagonal calculation more complex
            expected = _calculate_hex_fill_elements(dimensions)
        else:
            results.append({
                'cell': cell_num,
                'status': 'ERROR',
                'message': f'Unknown lattice type: {lat_type}'
            })
            continue

        # Count actual elements
        actual = len(fill_data)

        # Check match
        if expected == actual:
            results.append({
                'cell': cell_num,
                'status': 'PASS',
                'expected': expected,
                'actual': actual
            })
        else:
            results.append({
                'cell': cell_num,
                'status': 'FAIL',
                'expected': expected,
                'actual': actual,
                'message': f'Dimension mismatch: need {expected}, have {actual}'
            })

    return results


def print_fill_validation_report(results):
    """Print formatted validation report."""
    print("\nFILL Array Validation Report")
    print("=" * 60)

    pass_count = sum(1 for r in results if r['status'] == 'PASS')
    fail_count = sum(1 for r in results if r['status'] == 'FAIL')
    error_count = sum(1 for r in results if r['status'] == 'ERROR')

    print(f"Total Cells: {len(results)}")
    print(f"  PASS:  {pass_count}")
    print(f"  FAIL:  {fail_count}")
    print(f"  ERROR: {error_count}")
    print()

    if fail_count > 0 or error_count > 0:
        print("Issues Found:")
        for result in results:
            if result['status'] in ['FAIL', 'ERROR']:
                print(f"  Cell {result['cell']}: {result['message']}")


# Example usage
if __name__ == "__main__":
    results = validate_fill_arrays('input.i')
    print_fill_validation_report(results)
```

### Geometry Visualization

**Automated MCNP plotter**:

```python
import subprocess
import os

def visualize_geometry(input_file, plots=None):
    """
    Generate MCNP plotter images for geometry verification.

    Args:
        input_file: MCNP input file
        plots: List of plot dictionaries, each with:
               {'basis': 'xy', 'origin': (0,0,0), 'extent': 100, 'pixels': 400}
    """
    if plots is None:
        # Default plots
        plots = [
            {'basis': 'xy', 'origin': (0, 0, 0), 'extent': 100, 'pixels': 400},
            {'basis': 'xz', 'origin': (0, 0, 0), 'extent': 100, 'pixels': 400},
            {'basis': 'yz', 'origin': (0, 0, 0), 'extent': 100, 'pixels': 400}
        ]

    plot_dir = 'plots'
    os.makedirs(plot_dir, exist_ok=True)

    for i, plot_spec in enumerate(plots):
        # Create plotter command file
        cmd_file = f'plot_{i}.cmd'
        with open(cmd_file, 'w') as f:
            f.write(f"basis {plot_spec['basis']}\n")
            f.write(f"origin {plot_spec['origin'][0]} {plot_spec['origin'][1]} {plot_spec['origin'][2]}\n")
            f.write(f"extent {plot_spec['extent']}\n")
            f.write(f"pixels {plot_spec['pixels']}\n")
            f.write("color mat\n")
            f.write("plot\n")
            f.write("end\n")

        # Run MCNP plotter
        output_file = f"{plot_dir}/geometry_{plot_spec['basis']}.ps"
        subprocess.run([
            'mcnp6', 'ip',
            f'i={input_file}',
            f'com={cmd_file}',
            # Additional plotter options
        ])

        print(f"Generated plot: {output_file}")

        # Clean up
        os.remove(cmd_file)

    print(f"\n✓ Generated {len(plots)} geometry plots in {plot_dir}/")
```

### Parameter Verification Plots

**Diagnostic plots for input parameters**:

```python
import matplotlib.pyplot as plt
import pandas as pd

def create_parameter_verification_plots(cycle_params, output_dir='verification_plots'):
    """
    Create diagnostic plots showing time-dependent parameters
    and their time-weighted averages.

    Args:
        cycle_params: Dictionary of cycle parameters
        output_dir: Directory for plots
    """
    os.makedirs(output_dir, exist_ok=True)

    # Power history plot
    fig, ax = plt.subplots(figsize=(10, 6))

    for cycle in cycle_params.keys():
        power_data = cycle_params[cycle]['power_data']
        times = power_data['Time_h']
        power = power_data['Power_MW']
        avg_power = cycle_params[cycle]['avg_power_MW']

        ax.step(times, power, where='post', label=f"Cycle {cycle}", alpha=0.7)
        ax.axhline(avg_power, color='k', linestyle='--', alpha=0.3)

    ax.set_xlabel('Time (hours)', fontsize=12)
    ax.set_ylabel('Power (MW)', fontsize=12)
    ax.set_title('Power History and Time-Weighted Averages', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/power_history.png', dpi=300)
    print(f"Saved: {output_dir}/power_history.png")
    plt.close()

    # Control position plot
    fig, ax = plt.subplots(figsize=(10, 6))

    cycles = sorted(cycle_params.keys())
    discrete_angles = [cycle_params[c]['selected_angle'] for c in cycles]
    continuous_angles = [cycle_params[c]['avg_angle_continuous'] for c in cycles]

    x = range(len(cycles))
    ax.scatter(x, discrete_angles, marker='o', s=100, label='Selected (discrete)', zorder=3)
    ax.plot(x, continuous_angles, marker='x', linestyle='--',
            label='Average (continuous)', alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(cycles, rotation=45)
    ax.set_xlabel('Cycle', fontsize=12)
    ax.set_ylabel('OSCC Angle (degrees)', fontsize=12)
    ax.set_title('Control Drum Positions', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/control_positions.png', dpi=300)
    print(f"Saved: {output_dir}/control_positions.png")
    plt.close()

    print(f"\n✓ Created {2} verification plots in {output_dir}/")
```

---

## Mid-Run Monitoring

### Statistical Convergence Checks

**Monitor keff convergence during MCNP run**:

```python
import time
import re

def monitor_keff_convergence(output_file, check_interval=60):
    """
    Monitor keff convergence during MCNP run.

    Args:
        output_file: MCNP output file being written
        check_interval: Seconds between checks
    """
    print(f"Monitoring keff convergence in {output_file}")
    print("Press Ctrl+C to stop monitoring\n")

    keff_history = []

    try:
        while True:
            # Read current output
            if not os.path.exists(output_file):
                print("Waiting for output file...")
                time.sleep(check_interval)
                continue

            with open(output_file, 'r') as f:
                content = f.read()

            # Extract current keff
            # Look for "keff results" section
            matches = re.findall(r'keff\s+results.*?(\d+\.\d+)\s+(\d+\.\d+)', content, re.DOTALL)
            if matches:
                latest_keff = float(matches[-1][0])
                latest_uncert = float(matches[-1][1])

                keff_history.append({
                    'time': time.time(),
                    'keff': latest_keff,
                    'uncertainty': latest_uncert
                })

                # Print update
                print(f"[{time.strftime('%H:%M:%S')}] "
                      f"keff = {latest_keff:.5f} ± {latest_uncert:.5f}")

                # Check convergence
                if len(keff_history) >= 5:
                    recent = [k['keff'] for k in keff_history[-5:]]
                    std = np.std(recent)
                    if std < 0.0001:
                        print("\n✓ keff appears converged (std < 0.0001 over last 5 checks)")

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

    return keff_history
```

### Lost Particle Tracking

**Check for lost particles (geometry errors)**:

```python
def check_lost_particles(output_file):
    """
    Check MCNP output for lost particles.

    Returns:
        Dictionary with lost particle information
    """
    with open(output_file, 'r') as f:
        content = f.read()

    # Search for lost particle messages
    lost_particles = []

    for match in re.finditer(r'lost particle.*?at x,y,z\s+(\S+)\s+(\S+)\s+(\S+)', content, re.IGNORECASE):
        x, y, z = map(float, match.groups())
        lost_particles.append({
            'position': (x, y, z),
            'message': match.group(0)
        })

    if lost_particles:
        print(f"\n⚠ WARNING: {len(lost_particles)} lost particles detected")
        print("\nFirst 5 lost particle positions:")
        for i, lp in enumerate(lost_particles[:5], 1):
            print(f"  {i}. ({lp['position'][0]:.3f}, {lp['position'][1]:.3f}, {lp['position'][2]:.3f})")

        return {
            'count': len(lost_particles),
            'positions': [lp['position'] for lp in lost_particles]
        }
    else:
        print("✓ No lost particles detected")
        return {'count': 0, 'positions': []}
```

---

## Post-Run Validation

### Result Sanity Checks

**Verify results are physically reasonable**:

```python
def validate_results(output_file, expected_ranges=None):
    """
    Validate MCNP results for physical reasonableness.

    Args:
        output_file: MCNP output file
        expected_ranges: Dict of expected value ranges
                        {'keff': (0.9, 1.1), 'flux_max': (1e13, 1e15)}

    Returns:
        Validation results dictionary
    """
    issues = []

    # Extract results
    keff, keff_uncert = extract_keff(output_file)

    # 1. Check keff is physical
    if keff < 0:
        issues.append(f"Negative keff: {keff}")
    if keff > 3.0:
        issues.append(f"Unrealistically high keff: {keff}")

    # 2. Check uncertainty
    if keff_uncert > 0.01:
        issues.append(f"Poor statistical quality: keff uncertainty {keff_uncert:.4f} > 0.01")

    # 3. Check against expected ranges
    if expected_ranges:
        if 'keff' in expected_ranges:
            min_keff, max_keff = expected_ranges['keff']
            if not (min_keff <= keff <= max_keff):
                issues.append(
                    f"keff {keff:.5f} outside expected range [{min_keff}, {max_keff}]"
                )

    # 4. Check tally statistics
    tally_stats = extract_tally_statistics(output_file)
    for tally_num, stats in tally_stats.items():
        rel_err = stats['relative_error']
        if rel_err > 0.10:
            issues.append(
                f"Tally {tally_num}: poor statistics (rel err {rel_err:.4f} > 0.10)"
            )

    # 5. Check for warnings
    warnings = extract_warnings(output_file)
    if warnings:
        for warning in warnings[:5]:  # First 5
            issues.append(f"MCNP warning: {warning}")

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'keff': keff,
        'keff_uncertainty': keff_uncert
    }


def extract_warnings(output_file):
    """Extract warning messages from MCNP output."""
    with open(output_file, 'r') as f:
        content = f.read()

    warnings = []

    for line in content.split('\n'):
        if 'warning' in line.lower():
            warnings.append(line.strip())

    return warnings
```

### Benchmark Comparison

**Compare to experimental/reference data**:

```python
def compare_to_benchmark(results, benchmark_file):
    """
    Compare MCNP results to benchmark data.

    Args:
        results: Dictionary of calculated results
        benchmark_file: CSV file with benchmark data

    Returns:
        Comparison statistics
    """
    benchmark = pd.read_csv(benchmark_file)

    comparisons = []

    for case in results.keys():
        if case not in benchmark['Case'].values:
            print(f"Warning: Case {case} not in benchmark data")
            continue

        calc_keff = results[case]['keff']
        calc_uncert = results[case]['uncertainty']

        bench_row = benchmark[benchmark['Case'] == case].iloc[0]
        bench_keff = bench_row['keff']
        bench_uncert = bench_row['uncertainty']

        # Calculate difference
        diff = calc_keff - bench_keff

        # Combined uncertainty
        combined_uncert = np.sqrt(calc_uncert**2 + bench_uncert**2)

        # Statistical significance
        sigma = abs(diff) / combined_uncert

        comparisons.append({
            'case': case,
            'calculated': calc_keff,
            'benchmark': bench_keff,
            'difference': diff,
            'sigma': sigma,
            'status': 'PASS' if sigma < 3.0 else 'FAIL'
        })

    # Print report
    print("\nBenchmark Comparison Report")
    print("=" * 70)
    print(f"{'Case':<10} {'Calculated':<12} {'Benchmark':<12} {'Diff':<10} {'Sigma':<8} {'Status'}")
    print("-" * 70)

    for comp in comparisons:
        print(f"{comp['case']:<10} {comp['calculated']:<12.5f} {comp['benchmark']:<12.5f} "
              f"{comp['difference']:<10.4f} {comp['sigma']:<8.2f} {comp['status']}")

    pass_count = sum(1 for c in comparisons if c['status'] == 'PASS')
    print(f"\nPassed: {pass_count}/{len(comparisons)}")

    return comparisons
```

---

## Continuous Integration

**GitHub Actions example for MCNP validation**:

```yaml
# .github/workflows/validate-inputs.yml
name: Validate MCNP Inputs

on:
  push:
    paths:
      - 'scripts/**'
      - 'data/**'
  pull_request:
    paths:
      - 'scripts/**'
      - 'data/**'

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install pandas numpy jinja2 matplotlib

      - name: Generate MCNP inputs
        run: |
          python scripts/create_inputs.py

      - name: Validate generated inputs
        run: |
          python scripts/validate_inputs.py

      - name: Check for errors
        run: |
          if [ -f validation_errors.txt ]; then
            cat validation_errors.txt
            exit 1
          fi

      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: validation-report
          path: validation_report.html
```

---

## Complete QA Workflow Script

**Bringing it all together**:

```python
#!/usr/bin/env python3
"""
Complete quality assurance workflow for MCNP inputs.

Usage:
    python qa_workflow.py input.i
"""

import sys
import os

def run_qa_workflow(input_file):
    """Run complete QA workflow."""

    print("=" * 60)
    print("MCNP Input Quality Assurance Workflow")
    print("=" * 60)
    print(f"Input file: {input_file}\n")

    # Stage 1: Pre-Run Validation
    print("Stage 1: Pre-Run Validation")
    print("-" * 60)

    validation_result = validate_mcnp_input(input_file)

    if not validation_result['valid']:
        print("❌ VALIDATION FAILED")
        for issue in validation_result['issues']:
            print(f"  - {issue}")
        print("\nFix issues before proceeding.")
        return False

    print("✓ Input syntax validated")

    # Stage 2: FILL Array Validation
    fill_results = validate_fill_arrays(input_file)
    print_fill_validation_report(fill_results)

    if any(r['status'] == 'FAIL' for r in fill_results):
        print("\n❌ FILL array validation failed")
        return False

    # Stage 3: Geometry Visualization
    print("\nStage 2: Geometry Visualization")
    print("-" * 60)

    visualize_geometry(input_file)
    print("✓ Review geometry plots in plots/ directory")

    # Stage 4: Parameter Verification
    print("\nStage 3: Parameter Verification")
    print("-" * 60)

    # Generate verification plots
    # (Requires cycle_params data)
    print("✓ Generate parameter verification plots manually")

    print("\n" + "=" * 60)
    print("QA Workflow Complete")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review geometry plots")
    print("  2. If all checks pass, proceed with MCNP execution")
    print("  3. Monitor run with: python monitor_run.py output.o")

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python qa_workflow.py input.i")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    success = run_qa_workflow(input_file)

    sys.exit(0 if success else 1)
```

---

## Summary

**Quality Assurance Principles**:

1. **Fail Fast**: Catch errors before expensive computation
2. **Fail Loudly**: Clear, actionable error messages
3. **Automate**: QA checks should be scripted, not manual
4. **Document**: Record validation results
5. **Continuous**: QA throughout workflow, not just at end

**Three-Stage Approach**:
- **Pre-Run**: Syntax, dimensions, cross-references
- **Mid-Run**: Convergence, lost particles, progress
- **Post-Run**: Physical reasonableness, benchmarks, statistics

**Key Tools**:
- Python validation scripts
- MCNP plotter for geometry
- Matplotlib for diagnostics
- Continuous integration (GitHub Actions)

**Next Steps**:
- Adapt validation functions to your model
- Create benchmark comparison datasets
- Implement automated QA in your workflow
- Document expected value ranges
