# MCNP Variance Reducer - Python Scripts

## Overview

This directory contains Python automation scripts for MCNP variance reduction setup, optimization, and analysis. These scripts complement the mcnp-variance-reducer skill by providing command-line tools for common VR tasks.

---

## Scripts

### 1. importance_calculator.py

**Purpose:** Calculate optimal cell importance values for IMP cards

**Features:**
- Geometric progression (×2, ×4, etc.)
- Distance-based importance (inverse distance law)
- Importance ratio checking (detect violations of ≤4× guideline)
- Automatic optimization (insert intermediate cells)

**Usage:**

```bash
# Geometric progression (5 cells, ratio 2.0)
python importance_calculator.py --cells 5 --progression 2.0

# Distance-based (cells at 10, 30, 50 cm; detector at 100 cm)
python importance_calculator.py --distances 10 30 50 --detector-distance 100

# Check for ratio violations
python importance_calculator.py --cells 5 --progression 4.0 --check-ratios

# Optimize to fix violations
python importance_calculator.py --cells 5 --progression 4.0 --optimize
```

**Example Output:**

```
Geometric Progression (ratio=2.0, start=1.0):

Cell  Importance
--------------------
   1        1.00
   2        2.00
   3        4.00
   4        8.00
   5       16.00
   6        0.00  (graveyard)

All importance ratios ≤ 4.0 ✓

MCNP IMP Card:
IMP:N  1  2  4  8  16  0
```

**Options:**

- `--cells N`: Number of cells (geometric progression)
- `--distances D1 D2 ...`: Cell distances from source (distance-based)
- `--progression R`: Geometric ratio (default: 2.0)
- `--start S`: Starting importance (default: 1.0)
- `--detector-distance D`: Distance to detector (required for distance-based)
- `--particle P`: Particle type (default: N)
- `--check-ratios`: Check for ratio violations
- `--max-ratio R`: Maximum ratio threshold (default: 4.0)
- `--optimize`: Optimize to satisfy max ratio

---

### 2. fom_tracker.py

**Purpose:** Track Figure of Merit across multiple WWG iterations

**Features:**
- Extract FOM from MCNP output files
- Compare multiple iterations
- Check convergence (<20% change)
- ASCII plot of FOM trend

**Usage:**

```bash
# Track all tallies in multiple files
python fom_tracker.py out1.o out2.o out3.o

# Track specific tally
python fom_tracker.py --tally 5 out_iter*.o

# With convergence plot
python fom_tracker.py --tally 5 --plot out_iter1.o out_iter2.o out_iter3.o
```

**Example Output:**

```
FOM Tracking for Tally 5
================================================================================
File                          NPS         Mean    Error          FOM    Ratio
--------------------------------------------------------------------------------
out_analog.o              1000000   2.4500e-04   0.1000        100.0     1.0×
out_iter1.o               1000000   2.4800e-04   0.0500       1000.0    10.0×
out_iter2.o               2000000   2.4600e-04   0.0300       3333.3    33.3×
out_iter3.o               5000000   2.4700e-04   0.0200       5000.0    50.0×
--------------------------------------------------------------------------------
Convergence: ✓ CONVERGED (last change: 18.2%)

FOM Trend (Tally 5):
======================================================================
Run 1         100.0 ██████
Run 2        1000.0 ████████████████████████████████████████████████████████████
Run 3        3333.3 ████████████████████████████████████████████████████████████
Run 4        5000.0 ████████████████████████████████████████████████████████████
======================================================================
```

**Options:**

- `--tally N`: Specific tally number to track
- `--plot`: Display ASCII plot of FOM trend
- `--convergence-threshold T`: Convergence threshold (default: 0.20 = 20%)

---

### 3. ww_parameter_optimizer.py

**Purpose:** Suggest optimal WWP card parameters based on weight statistics

**Features:**
- Extract weight min/max/avg from output
- Analyze splitting/roulette statistics
- Suggest wupn, wsurvn, mxspln values
- Suggest WWG target weight

**Usage:**

```bash
# Analyze weight window performance
python ww_parameter_optimizer.py output.o

# Suggest WWG target weight
python ww_parameter_optimizer.py --suggest-target output.o

# Provide current parameters for comparison
python ww_parameter_optimizer.py --current-wupn 5 --current-wsurvn 3 output.o
```

**Example Output:**

```
Weight Window Statistics:
============================================================
Minimum weight:    5.234000e-02
Maximum weight:    8.123000e+01
Average weight:    1.234000e+00
Weight ratio:      155.23 (max/min)
Splits:            45,231
Roulettes:         12,456
Particles killed:  3,421

Performance Analysis:
============================================================
⚠️  WARNING: Weight ratio >50 - consider widening weight windows

Parameter Suggestions:
============================================================
Current:  WWP:N  5  3  5  0  -1
Suggested: WWP:N  10  5  5  0  -1

Reasoning:
  wupn:    Weight ratio (155.2) large - widen window
  wsurvn:  Half of wupn (standard practice)
  mxspln:  Split rate (45/1000) acceptable

WWG Target Weight Suggestion:
============================================================
Target:  2.0
Reason:  Match average weight (1.23)

WWG card: WWG  <tally>  <mesh>  2.0
```

**Options:**

- `--current-wupn W`: Current wupn value (default: 5.0)
- `--current-wsurvn W`: Current wsurvn value (default: 3.0)
- `--current-mxspln M`: Current mxspln value (default: 5)
- `--suggest-target`: Suggest WWG target weight
- `--particle P`: Particle type for WWP card (default: N)

---

### 4. dxtran_sphere_locator.py

**Purpose:** Calculate optimal DXTRAN sphere location and parameters

**Features:**
- Suggest radius based on detector distance
- Suggest MAX contributions
- Verify DXTRAN/detector alignment
- Generate complete DXTRAN/F5 cards

**Usage:**

```bash
# Basic DXTRAN for detector at (100, 0, 0)
python dxtran_sphere_locator.py --detector 100 0 0

# Custom radius and max contributions
python dxtran_sphere_locator.py --detector 100 0 0 --radius 2.0 --max 1000

# Verify existing DXTRAN alignment
python dxtran_sphere_locator.py --detector 100 0 0 --dxtran-center 95 0 0 --dxtran-radius 1.0

# Include source location
python dxtran_sphere_locator.py --detector 100 0 0 --source 0 0 0
```

**Example Output:**

```
DXTRAN Sphere Configuration
======================================================================
Source location:    (0.00, 0.00, 0.00)
Detector location:  (100.00, 0.00, 0.00)
Distance:           100.00 cm

Suggested radius:   2.00 cm (Far detector (50-100 cm) - larger radius)
Suggested MAX:      1000 (Far detector - many contributions needed)

MCNP Data Cards:
======================================================================
c
c --- Point detector ---
F5:N  100.00 0.00 0.00  0.50
c
c --- DXTRAN sphere (must match detector location) ---
DXTRAN  2.00  100.00 0.00 0.00  1000
c
c --- DXC: Which cells contribute to DXTRAN ---
c Option 1: All cells contribute (default)
c DXC  J  J  J
c
c Option 2: Only specific cells contribute
c DXC  1  2  3  4  J  J  J        $ Cells 1-4 + rest

Usage Notes:
======================================================================
1. DXTRAN center MUST match detector location for optimal performance
2. Radius should encompass detector but not be excessive
3. MAX prevents memory overflow - increase if contributions limited
4. DXC limits which cells contribute (default: all cells)
5. Combine with weight windows for best results

Expected Benefits:
======================================================================
- FOM improvement: 50-200× (medium distance)
- Reduces variance at point detector significantly
- Most effective when source → detector path is complex
```

**Options:**

- `--detector X Y Z`: Detector coordinates (required)
- `--source X Y Z`: Source coordinates (default: 0 0 0)
- `--radius R`: DXTRAN sphere radius (auto-calculate if not provided)
- `--max M`: MAX contributions (auto-calculate if not provided)
- `--nps N`: Number of source particles (default: 1000000)
- `--particle P`: Particle type (default: N)
- `--detector-radius R`: F5 detector radius (default: 0.5 cm)
- `--dxtran-center X Y Z`: Verify existing DXTRAN center
- `--dxtran-radius R`: Verify existing DXTRAN radius

---

## Installation

### Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

### Setup

```bash
# Make scripts executable (Linux/macOS)
chmod +x *.py

# Or run with python command
python script_name.py [arguments]
```

---

## Workflow Examples

### Example 1: Initial VR Setup

**Goal:** Set up variance reduction for shielding problem

**Steps:**

1. **Calculate cell importances:**
   ```bash
   python importance_calculator.py --cells 5 --progression 2.0 > imp_cards.txt
   ```

2. **Run analog simulation:**
   ```bash
   mcnp6 inp=input_analog.i outp=analog.o
   ```

3. **Track baseline FOM:**
   ```bash
   python fom_tracker.py --tally 5 analog.o
   ```

4. **Add IMP cards to input, run WWG:**
   ```bash
   # (Edit input file to include IMP cards)
   mcnp6 inp=input_wwg.i outp=wwg1.o
   ```

5. **Optimize WWP parameters:**
   ```bash
   python ww_parameter_optimizer.py wwg1.o
   ```

---

### Example 2: WWG Iteration Optimization

**Goal:** Iteratively optimize weight windows until converged

**Steps:**

1. **Generate initial WW:**
   ```bash
   mcnp6 inp=iter1_wwg.i outp=iter1.o
   ```

2. **Use WW, regenerate:**
   ```bash
   mcnp6 inp=iter2_wwg.i outp=iter2.o
   ```

3. **Check convergence:**
   ```bash
   python fom_tracker.py --tally 5 --plot iter1.o iter2.o
   ```

4. **If not converged, continue:**
   ```bash
   mcnp6 inp=iter3_wwg.i outp=iter3.o
   python fom_tracker.py --tally 5 --plot iter1.o iter2.o iter3.o
   ```

5. **Monitor until FOM change <20%**

---

### Example 3: DXTRAN Setup for Point Detector

**Goal:** Add DXTRAN for far point detector

**Steps:**

1. **Calculate DXTRAN parameters:**
   ```bash
   python dxtran_sphere_locator.py --detector 100 0 0 --source 0 0 0
   ```

2. **Add cards to input file:**
   ```
   F5:N  100.00 0.00 0.00  0.50
   DXTRAN  2.00  100.00 0.00 0.00  1000
   ```

3. **Run simulation:**
   ```bash
   mcnp6 inp=input_dxtran.i outp=dxtran.o
   ```

4. **Compare FOM improvement:**
   ```bash
   python fom_tracker.py --tally 5 analog.o dxtran.o
   ```

---

## Troubleshooting

### Script Won't Run

**Problem:** `python: command not found`

**Solution:**
```bash
# Try python3
python3 script_name.py [arguments]

# Or install Python from python.org
```

### No Statistics Found

**Problem:** `Error: Could not extract weight statistics`

**Solution:**
- Ensure MCNP output file is complete (not truncated)
- Check that VR methods (WWN/WWP) were actually used in simulation
- Verify output file format is standard MCNP6

### Import Errors

**Problem:** `ImportError: No module named 'xyz'`

**Solution:**
- These scripts use only Python standard library
- Ensure Python version ≥ 3.6
- Check Python installation is complete

---

## Integration with MCNP Workflow

### Typical VR Development Cycle

```
1. Analog run → Baseline FOM
   ↓
2. importance_calculator.py → Generate IMP cards
   ↓
3. Run with IMP → Check improvement
   ↓
4. Add WWG → Generate weight windows
   ↓
5. ww_parameter_optimizer.py → Optimize WWP parameters
   ↓
6. Iterate WWG (2-5 times)
   ↓
7. fom_tracker.py → Monitor convergence
   ↓
8. dxtran_sphere_locator.py → Add DXTRAN if needed
   ↓
9. Final production run → Achieve target statistics
```

---

## Advanced Usage

### Batch Processing

```bash
# Process multiple files
for file in out_iter*.o; do
    python ww_parameter_optimizer.py "$file" > "${file%.o}_optimization.txt"
done

# Track all iterations
python fom_tracker.py --tally 5 --plot out_iter*.o > fom_tracking.txt
```

### Custom Scripts

These scripts can be imported as Python modules:

```python
from importance_calculator import geometric_progression, check_importance_ratios

importances = geometric_progression(num_cells=5, ratio=2.0)
violations = check_importance_ratios(importances, max_ratio=4.0)
```

---

## References

**See Also:**
- `../variance_reduction_theory.md` - VR theory and FOM calculation
- `../card_specifications.md` - VR card syntax
- `../wwg_iteration_guide.md` - Manual WWG iteration procedures
- `../error_catalog.md` - Common VR problems

**MCNP6 Manual:**
- Chapter 5.12: Variance Reduction Cards
- Chapter 2.7: Variance Reduction Theory

---

## Support

For issues or questions about these scripts:
1. Check error message for specific guidance
2. Verify Python version ≥ 3.6
3. Ensure MCNP output file is complete and valid
4. Refer to script-specific `--help` output
5. Consult MCNP variance reducer skill documentation

---

## Version History

**v1.0.0** (2025-11-04)
- Initial release
- 4 automation scripts
- Comprehensive usage examples
- Integration with mcnp-variance-reducer skill

---

**END OF README.md**
