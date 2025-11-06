# MCNP Plotter Scripts

**Purpose:** Python utilities for MCNP visualization (convergence, spectra, geometry).

**Location:** `.claude/skills/mcnp-plotter/scripts/`

---

## Scripts Overview

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `plot_convergence.py` | Statistical convergence plots | MCNP output file | 4-panel PNG plot |
| `plot_spectrum.py` | Energy spectrum visualization | Energy bins + flux data | Publication-quality plot |

---

## Installation

```bash
pip install numpy matplotlib
```

---

## Script 1: plot_convergence.py

**Purpose:** Extract and visualize Tally Fluctuation Chart (TFC) data for convergence assessment.

### Features

- Parses TFC data from MCNP output files
- Creates 4-panel convergence plot (mean, error, VOV, FOM)
- Assesses convergence quality with automated checks
- Identifies convergence issues

### Usage

**Basic:**
```bash
python plot_convergence.py output.o --tally 4
```

**Custom output:**
```bash
python plot_convergence.py output.o --tally 14 --output f14_convergence.png
```

**Summary only (no plot):**
```bash
python plot_convergence.py output.o --tally 4 --summary
```

### Output

**Plot panels:**
1. **Mean vs NPS** - Should stabilize (plateau)
2. **Error vs NPS** - Should follow 1/√N line (log-log)
3. **VOV vs NPS** - Should decrease toward 0 (< 0.1 target)
4. **FOM vs NPS** - Should be constant

**Terminal summary:**
```
============================================================
CONVERGENCE SUMMARY - Tally 4
============================================================

Final Statistics:
  NPS:          1.00e+08
  Mean:         1.234567e-04
  Rel. Error:   0.0487 (4.87%)
  VOV:          0.0234
  FOM:          4.32e+05

Convergence Assessment:
  Mean stable:     ✓ YES
  Error < 10%:     ✓ YES
  VOV < 0.1:       ✓ YES
  FOM stable:      ✓ YES

Overall: ✓ CONVERGED
============================================================
```

### Interpreting Results

**Good convergence:**
- Mean stable (last 3 points within 5%)
- Error following 1/√N line
- VOV < 0.1
- FOM constant (±20%)

**Poor convergence (need more histories):**
- Mean still drifting
- Error not following 1/√N
- VOV > 0.1
- FOM decreasing

---

## Script 2: plot_spectrum.py

**Purpose:** Create publication-quality energy spectrum plots.

### Features

- Log-log plotting for wide energy ranges
- Automatic bin center calculation
- Error bar visualization
- Reference lines for neutrons (thermal, epithermal, fast)
- Saves both PNG and PDF formats

### Usage

**From command-line data:**
```bash
python plot_spectrum.py \
  --energy 1e-10 1e-6 0.1 1 14 \
  --flux 1.2e-4 5.6e-5 3.4e-5 1.8e-5 8.2e-6 \
  --error 0.05 0.08 0.10 0.12 0.15
```

**From file:**
```bash
# Create data file (space or comma separated)
cat > spectrum.txt << EOF
# Energy (MeV)  Flux  RelError
1e-10  1.23e-4  0.05
1e-6   5.67e-5  0.08
0.1    3.45e-5  0.10
1.0    1.89e-5  0.12
14.0   8.23e-6  0.15
EOF

python plot_spectrum.py --file spectrum.txt
```

**Custom options:**
```bash
python plot_spectrum.py --file spectrum.txt \
  --particle photon \
  --title "Photon Energy Spectrum - 50 cm Concrete" \
  --output photon_spectrum.png
```

### Output

- `spectrum.png` - 300 DPI raster image
- `spectrum.pdf` - Vector format (publication)

**Terminal summary:**
```
============================================================
ENERGY SPECTRUM SUMMARY
============================================================

Energy Bins: 5
Energy Range: 1.00e-10 - 1.40e+01 MeV

Bin-by-Bin Data:
E_low (MeV)     E_high (MeV)    Flux            Error (%)
------------------------------------------------------------
1.000e-10       1.000e-06       1.230e-04       5.00
1.000e-06       1.000e-01       5.670e-05       8.00
1.000e-01       1.000e+00       3.450e-05       10.00
1.000e+00       1.400e+01       1.890e-05       12.00

Total Integrated Flux: 2.337e-04
Mean Relative Error: 0.0875 (8.75%)
Max Relative Error: 0.1200 (12.00%)
============================================================
```

---

## Common Workflows

### Workflow 1: Check Convergence After Run

```bash
# 1. Run MCNP
mcnp6 i=input.i o=output.o

# 2. Check convergence for all tallies
python plot_convergence.py output.o --tally 4
python plot_convergence.py output.o --tally 14
python plot_convergence.py output.o --tally 24

# 3. If not converged, increase NPS and re-run
```

### Workflow 2: Publication-Quality Spectrum

```bash
# 1. Extract tally data from MCTAL (use mcnp-output-parser)
# 2. Create spectrum file
# 3. Plot
python plot_spectrum.py --file spectrum_data.txt \
  --title "Neutron Spectrum - PWR Core" \
  --output pwr_spectrum.png

# Result: pwr_spectrum.png and pwr_spectrum.pdf
```

### Workflow 3: Batch Processing Multiple Tallies

```bash
#!/bin/bash
# Plot convergence for all tallies

for tally in 4 14 24 34 44; do
    python plot_convergence.py output.o --tally $tally --output f${tally}_conv.png
done
```

---

## Integration with Other Skills

**With mcnp-output-parser:**
- Use mcnp-output-parser to extract tally data from MCTAL
- Pass extracted data to plot_spectrum.py

**With mcnp-statistics-checker:**
- plot_convergence.py automates convergence checking
- Use for quick visual assessment before detailed statistical validation

**With mcnp-tally-analyzer:**
- Plot spectra after interpretation with tally-analyzer
- Combine physical interpretation with visualization

---

## Python API

Both scripts can be imported as modules:

```python
from plot_convergence import parse_tfc, plot_convergence, print_summary

# Parse output
tfc_data = parse_tfc('output.o', tally_num=4)

# Print summary
print_summary(tfc_data, tally_num=4)

# Create plot
fig = plot_convergence(tfc_data, tally_num=4, save_path='my_plot.png')
```

```python
from plot_spectrum import plot_energy_spectrum
import numpy as np

# Your data
energy_bins = np.array([1e-10, 1e-6, 0.1, 1, 14])
flux = np.array([1.2e-4, 5.6e-5, 3.4e-5, 1.8e-5])
errors = np.array([0.05, 0.08, 0.10, 0.12])

# Plot
fig = plot_energy_spectrum(energy_bins, flux, errors,
                           particle='neutron',
                           title='My Spectrum',
                           save_path='my_spectrum.png')
```

---

## Troubleshooting

### Error: "Tally X not found in output file"

**Cause:** Tally number doesn't exist or output file incomplete

**Fix:**
1. Check output file has "tally fluctuation charts" section
2. Verify tally number is correct (F4 → tally 4)
3. Ensure MCNP run completed successfully

### Error: "Flux array length must be one less than energy bins"

**Cause:** Mismatch between energy bins and flux data

**Fix:**
- If N energy bins, need N-1 flux values (one per interval)
- Example: 5 bins → 4 flux values

### Warning: "No data points found"

**Cause:** TFC section empty or parsing failed

**Fix:**
1. Check MCNP output has tally fluctuation chart
2. Ensure enough histories run (>100 histories minimum)
3. Check file format is plain text (not binary)

---

## Tips

1. **Convergence plots first** - Always check convergence before trusting results
2. **Save scripts** - Keep plotting scripts with simulation files for reproducibility
3. **Batch processing** - Use loops for multiple tallies
4. **Publication format** - PDF output is vector (scales perfectly)
5. **Energy groups** - Use 4-6 bins for cleaner plots (thermal, epithermal, fast)

---

## Related Skills

- **mcnp-output-parser** - Extract data from MCTAL/output files
- **mcnp-statistics-checker** - Detailed statistical validation
- **mcnp-tally-analyzer** - Physical interpretation of results
- **mcnp-mesh-builder** - Create mesh tallies for 3D visualization

---

**END OF README**
