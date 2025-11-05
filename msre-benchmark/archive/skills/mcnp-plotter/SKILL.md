---
name: "MCNP Plotter"
description: "Generates visualizations of MCNP geometry, tally results, and cross sections. Creates plots for verification, analysis, and publication. Use when visualizing simulation results."
version: "1.0.0"
dependencies: "python>=3.8, matplotlib, numpy, h5py"
---

# MCNP Plotter

## Overview

When a user needs to visualize MCNP simulation results or verify geometry, use this skill to create plots for:

- **Geometry verification** (PLOTG): cells, surfaces, materials from input file
- **Tally visualization** (MCPLOT): energy spectra, spatial distributions, convergence
- **Mesh tally visualization** (ParaView/VisIt): 3D spatial distributions with XDMF format
- **Statistical convergence**: mean/error/FOM vs NPS trends
- **Cross sections**: reaction cross sections vs energy
- **Publication-quality figures**: Custom matplotlib/plotly plots for reports/papers

This skill helps users:
1. Verify geometry is correct before running (catches 90% of errors)
2. Understand tally results physically through visualization
3. Identify spatial patterns and anomalies
4. Validate statistical convergence
5. Create figures for documentation and publication

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User asks to "plot", "visualize", "show", or "graph" anything MCNP-related
- User mentions "geometry plot", "PLOTG", "MCPLOT"
- User wants to "see" flux distribution, energy spectrum, spatial distribution
- User mentions ParaView, VisIt, or 3D visualization
- User asks about geometry errors (dashed lines indicate need to plot)
- User wants publication-quality figures
- User mentions convergence plots or statistical trends

**Context Clues:**
- "What does my geometry look like?"
- "Show me the flux spectrum..."
- "Visualize the dose distribution..."
- "Plot convergence..."
- "I need figures for a paper..."
- "How do I check for geometry errors?"

### Visualization Type Decision Tree

**Step 1: Determine What to Plot**

```
User request → Select plot type:
├── Geometry verification → PLOTG interactive or batch
├── Tally results → MCPLOT or Python custom
├── Mesh tallies (3D) → ParaView/VisIt with XDMF
├── Statistical convergence → TFC data extraction + plotting
├── Cross sections → XS plotting mode
└── Custom analysis → Python with matplotlib/plotly
```

**Step 2: Choose Visualization Tool**

```
Geometry plots:
├── Interactive verification → mcnp6 ip i=input.inp (PLOTG)
├── Batch plots → Command file for multiple views
└── Geometry errors → Inspect for dashed lines

Tally plots:
├── Quick visualization → MCPLOT (mcnp6 z mctal=mctal)
├── Publication quality → Python matplotlib scripts
├── 3D mesh data → ParaView/VisIt XDMF workflow
└── Statistical analysis → Custom Python plots

Convergence plots:
├── Extract TFC data from output
├── Plot mean vs NPS
├── Plot error vs NPS (log-log with 1/√N reference)
└── Plot FOM vs NPS

Custom requirements:
├── Multi-panel figures → matplotlib subplots
├── Animations → matplotlib animation or ParaView
├── Interactive → plotly or bokeh
└── Comparison plots → overlay multiple tallies/runs
```

## Visualization Procedures

### Step 1: Initial Assessment

**Ask user for context:**
- "What do you want to visualize?" (geometry, tallies, convergence, cross sections)
- "Do you have specific files?" (input.inp, mctal, output.o, runtpe.h5)
- "What's the purpose?" (verification, analysis, publication)
- "Do you need interactive or static plots?"
- "Any specific format requirements?" (PNG, PDF, EPS for publication)

### Step 2: Read Reference Materials

**MANDATORY - READ ENTIRE FILE**: Before plotting, read:
- `.claude/commands/mcnp-plotter.md` - Complete plotting procedures for all types
- If ParaView: Review Appendix D.4 (XDMF format)

### Step 3: Geometry Plotting (PLOTG)

**Purpose:** Verify geometry correctness BEFORE running expensive simulations

**Critical rule from Chapter 3:** ALWAYS plot geometry from multiple directions before production runs. Dashed lines indicate errors.

**Interactive Mode:**
```bash
# Start interactive plotting
mcnp6 ip i=input.inp
```

**Interactive Commands:**
```
# Basic viewing planes
plot origin=0 0 0 basis=xy extent=100 100    # Top view (XY plane)
plot origin=0 0 0 basis=xz extent=100 100    # Side view (XZ plane)
plot origin=0 0 0 basis=yz extent=100 100    # Front view (YZ plane)

# Cylindrical coordinates (for cylindrical geometry)
plot origin=0 0 0 basis=rz extent=100 100    # R-Z plane
plot origin=0 0 0 basis=rt extent=100 100    # R-Theta plane

# Zoom and labels
plot scales=0.5        # Zoom in (smaller extent)
plot scales=2.0        # Zoom out (larger extent)
plot label=1           # Show cell/surface numbers
plot label=0           # Hide labels

# Color control
plot color=on          # Color by material/importance
plot color=off         # Wire frame mode (clearer for complex geometry)

# Click to inspect
px=X                   # Click at position X
py=Y                   # Click at position Y
# Displays: cell number, material, density at clicked point

# Save and exit
end                    # Exit plotting
```

**What to look for:**
- **Solid lines**: Correct geometry boundaries
- **Dashed lines**: ⚠️ GEOMETRY ERRORS (overlaps, gaps, undefined regions)
- **Colors**: Different for each material/cell (if color=on)
- **Symmetry**: Verify expected geometric symmetry
- **Dimensions**: Check sizes match design

**Common geometry errors:**
```
Dashed lines indicate:
- Cell overlaps (two cells claim same space)
- Gaps in geometry (undefined regions)
- Surface equation errors
- Incorrect Boolean algebra
```

**Batch mode (non-interactive):**
```bash
# Create plot command file: plot_commands.txt
plot origin=0 0 0 basis=xy extent=100 100
plot origin=0 0 0 basis=xz extent=100 100
plot origin=0 0 0 basis=yz extent=100 100
end

# Run batch
mcnp6 ip i=input.inp < plot_commands.txt
```

### Step 4: Tally Plotting (MCPLOT)

**Purpose:** Visualize tally results (energy spectra, spatial distributions, convergence)

**Execution:**
```bash
# Plot from MCTAL file
mcnp6 z mctal=mctal

# Or from restart file
mcnp6 z r=runtpe
```

**Interactive Commands:**
```
# Select tally
tally 4                 # Select F4 tally

# Plot types
vs energy               # Flux vs energy bins
vs time                 # Response vs time bins
vs cosine               # Angular distribution
vs segment              # Spatial distribution (if FS card used)

# Scale options
lin                     # Linear scale
log                     # Log scale
loglog                  # Log-log scale

# Display options
errors on               # Show error bars
errors off              # Hide error bars
overlay                 # Compare multiple tallies
grid                    # Toggle grid

# Save plot
print filename.ps       # Save to PostScript
# Convert: ps2pdf filename.ps (if needed)

# Navigation
next                    # Next tally
prev                    # Previous tally
quit                    # Exit
```

**Example MCPLOT session:**
```
mcnp6 z mctal=mctal

> tally 4              # Select F4 neutron flux tally
> vs energy            # Plot flux vs energy
> loglog               # Use log-log scale (good for wide energy range)
> errors on            # Show error bars
> print f4_spectrum.ps # Save to file
> quit
```

**Interpreting MCPLOT graphs:**
- **Flux vs energy**: Energy spectrum shape (thermal peak, fission spectrum, fast tail)
- **Error bars**: Statistical uncertainty (should be small compared to value)
- **Smooth curve**: Good statistics
- **Noisy/jagged**: Poor statistics, need more histories

### Step 5: Mesh Tally Visualization (ParaView/VisIt)

**Purpose:** 3D visualization of spatial distributions from FMESH tallies

**Setup in MCNP input:**
```
FMESH14:N              $ Neutron flux mesh tally
  GEOM=xyz             $ Cartesian coordinates
  ORIGIN=0 0 0         $ Mesh origin
  IMESH=50 IINTS=20    $ X: 0→50 cm, 20 bins
  JMESH=50 JINTS=20    $ Y: 0→50 cm, 20 bins
  KMESH=100 KINTS=40   $ Z: 0→100 cm, 40 bins
  OUT=xdmf             $ Generate XDMF format for ParaView/VisIt
```

**Output files:**
- `meshtal.xdmf` - XML descriptor (small, text)
- `runtpe.h5` - HDF5 data file (large, binary)

**ParaView Workflow:**

1. **Open file:**
   - File → Open → Select `meshtal.xdmf`
   - Click "Apply" in Properties panel

2. **Basic visualization:**
   - Change "Representation" from "Outline" to "Surface"
   - In "Coloring" dropdown, select field (e.g., "flux", "error")
   - Color legend appears automatically

3. **Slicing:**
   - Filters → Slice
   - Set normal (X, Y, or Z)
   - Drag slice plane or enter origin
   - Shows 2D cross-section through 3D data

4. **Iso-surfaces:**
   - Filters → Contour
   - Enter iso-value (e.g., flux = 1E-4)
   - Shows 3D surface where flux equals specified value

5. **Threshold:**
   - Filters → Threshold
   - Set min/max values
   - Shows only regions above/below threshold

6. **Volume rendering:**
   - Change representation to "Volume"
   - Adjust opacity transfer function
   - Shows 3D translucent volume

7. **Export:**
   - File → Save Screenshot (PNG, JPEG)
   - File → Save Animation (AVI, MP4)
   - File → Export Scene (for other tools)

**VisIt workflow:** Similar to ParaView, optimized for very large datasets

### Step 6: Statistical Convergence Plotting

**Purpose:** Verify tally convergence and statistical quality

**Extract data from Tally Fluctuation Chart:**
```python
import re

def parse_tfc(output_file, tally_num):
    """Extract TFC data from OUTP file"""

    with open(output_file, 'r') as f:
        content = f.read()

    # Find TFC section for specified tally
    pattern = rf'tally\s+{tally_num}\s*\n.*?nps.*?mean.*?error.*?vov.*?slope.*?fom\s*\n(.*?)(?=tally|$)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return None

    lines = match.group(1).strip().split('\n')
    nps, mean, error, vov, slope, fom = [], [], [], [], [], []

    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            nps.append(float(parts[0]))
            mean.append(float(parts[1]))
            error.append(float(parts[2]))
            vov.append(float(parts[3]))
            slope.append(float(parts[4]))
            fom.append(float(parts[5]))

    return {
        'nps': nps,
        'mean': mean,
        'error': error,
        'vov': vov,
        'slope': slope,
        'fom': fom
    }

# Usage:
tfc_data = parse_tfc('output.o', tally_num=4)
```

**Create convergence plots:**
```python
import matplotlib.pyplot as plt
import numpy as np

def plot_convergence(tfc_data, tally_num, save_path='convergence.png'):
    """Create 4-panel convergence plot"""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    nps = np.array(tfc_data['nps'])
    mean = np.array(tfc_data['mean'])
    error = np.array(tfc_data['error'])
    vov = np.array(tfc_data['vov'])
    fom = np.array(tfc_data['fom'])

    # Panel 1: Mean vs NPS
    ax1.plot(nps, mean, 'b-o', markersize=4)
    ax1.axhline(mean[-1], color='k', linestyle='--', alpha=0.5, label='Final mean')
    ax1.set_xlabel('Number of Histories')
    ax1.set_ylabel('Tally Mean')
    ax1.set_title(f'Tally {tally_num}: Mean Convergence')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Panel 2: Relative Error vs NPS (log-log)
    ax2.loglog(nps, error, 'r-o', markersize=4, label='Actual')
    # Theoretical 1/√N line
    theory = error[0] * np.sqrt(nps[0] / nps)
    ax2.loglog(nps, theory, 'k--', label='1/√N theory')
    ax2.set_xlabel('Number of Histories')
    ax2.set_ylabel('Relative Error')
    ax2.set_title('Error Convergence')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # Panel 3: VOV vs NPS
    ax3.semilogy(nps, vov, 'g-o', markersize=4)
    ax3.axhline(0.1, color='r', linestyle='--', alpha=0.5, label='VOV=0.1 limit')
    ax3.set_xlabel('Number of Histories')
    ax3.set_ylabel('Variance of Variance (VOV)')
    ax3.set_title('VOV Convergence')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    # Panel 4: FOM vs NPS
    ax4.plot(nps, fom, 'm-o', markersize=4)
    ax4.axhline(fom[-1], color='k', linestyle='--', alpha=0.5, label='Final FOM')
    ax4.set_xlabel('Number of Histories')
    ax4.set_ylabel('Figure of Merit')
    ax4.set_title('FOM Stability')
    ax4.grid(True, alpha=0.3)
    ax4.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Convergence plot saved to {save_path}")

    return fig

# Usage:
plot_convergence(tfc_data, tally_num=4)
```

**Interpreting convergence plots:**
- **Mean panel**: Should stabilize (plateau) - if still drifting, not converged
- **Error panel**: Should follow 1/√N line - if parallel, good convergence
- **VOV panel**: Should decrease toward 0 - if >0.1, poor convergence
- **FOM panel**: Should be constant - if decreasing, efficiency degrading

### Step 7: Energy Spectrum Plotting

**From MCTAL or output parsing:**
```python
import matplotlib.pyplot as plt
import numpy as np

def plot_energy_spectrum(energy_bins, flux, errors, particle='neutron',
                         save_path='spectrum.png'):
    """Create publication-quality energy spectrum plot"""

    fig, ax = plt.subplots(figsize=(10, 7))

    # Calculate bin centers for plotting
    e_centers = np.sqrt(energy_bins[:-1] * energy_bins[1:])  # Geometric mean

    # Calculate absolute uncertainties
    abs_errors = flux * errors

    # Plot with error bars
    ax.errorbar(e_centers, flux, yerr=abs_errors,
                fmt='o-', markersize=5, capsize=3, capthick=1,
                label=f'{particle.capitalize()} flux')

    # Formatting
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Energy (MeV)', fontsize=12)
    ax.set_ylabel('Flux (particles/cm² per source particle)', fontsize=12)
    ax.set_title(f'{particle.capitalize()} Energy Spectrum', fontsize=14, fontweight='bold')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=11)

    # Add thermal/fast markers for neutrons
    if particle.lower() == 'neutron':
        ax.axvline(1e-6, color='b', linestyle='--', alpha=0.5, label='Thermal (1 eV)')
        ax.axvline(1e-3, color='g', linestyle='--', alpha=0.5, label='Epi-thermal (1 keV)')
        ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Spectrum plot saved to {save_path}")

    return fig

# Usage:
plot_energy_spectrum(energy_bins, flux, errors, particle='neutron')
```

### Step 8: Cross-Section Plotting

**MCNP XS plotting mode:**
```bash
mcnp6 ixz
```

**Input format:**
```
Cross-section plot for U-235 fission
1 0 -1              $ Dummy cell
1 so 1              $ Dummy surface

mode n
m1 92235.80c 1
plot n 92235 1 0 1 20    $ Plot total XS from 0-20 MeV
```

**Plot parameters:**
```
plot particle isotope MT Emin Emax npoints

particle: n, p, e, etc.
isotope: ZZZAAA (e.g., 92235 for U-235)
MT: Reaction number (1=total, 2=elastic, 18=fission, 102=capture)
Emin, Emax: Energy range (MeV)
npoints: Number of points to plot
```

**Common reactions:**
- MT=1: Total cross section
- MT=2: Elastic scattering
- MT=18: Fission
- MT=102: (n,γ) capture
- MT=16: (n,2n)
- MT=103-107: (n,p), (n,d), (n,t), (n,He3), (n,α)

## Python Plotting Best Practices

### Publication-Quality Figure Settings

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Publication settings
mpl.rcParams['font.size'] = 11
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']
mpl.rcParams['axes.labelsize'] = 12
mpl.rcParams['axes.titlesize'] = 14
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['figure.titlesize'] = 14
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 6

# For LaTeX rendering (if available)
# mpl.rcParams['text.usetex'] = True

# Color schemes
# For print (colorblind-friendly):
colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC', '#CA9161', '#949494']

# For presentation (high contrast):
# colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00']
```

### Multi-Panel Comparison Plots

```python
def compare_tallies(tallies_data, tally_labels, title='Tally Comparison'):
    """Create multi-panel comparison of multiple tallies"""

    n_tallies = len(tallies_data)
    fig, axes = plt.subplots(n_tallies, 1, figsize=(10, 3*n_tallies), sharex=True)

    if n_tallies == 1:
        axes = [axes]

    for ax, data, label in zip(axes, tallies_data, tally_labels):
        e_centers = np.sqrt(data['energy_bins'][:-1] * data['energy_bins'][1:])
        flux = data['flux']
        errors = data['errors']

        ax.errorbar(e_centers, flux, yerr=flux*errors,
                    fmt='o-', markersize=4, capsize=2, label=label)

        ax.set_yscale('log')
        ax.set_ylabel('Flux (n/cm²)', fontsize=11)
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=10)

    axes[-1].set_xlabel('Energy (MeV)', fontsize=12)
    axes[-1].set_xscale('log')

    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()

    return fig
```

### Animated Plots (Time-Dependent Tallies)

```python
import matplotlib.animation as animation

def animate_time_evolution(mesh_data_time_series, time_bins):
    """Create animation of time-dependent mesh tally"""

    fig, ax = plt.subplots(figsize=(8, 6))

    # Initial frame
    im = ax.imshow(mesh_data_time_series[0], origin='lower',
                   extent=[xmin, xmax, ymin, ymax],
                   cmap='viridis', aspect='auto')

    colorbar = plt.colorbar(im, ax=ax, label='Flux (n/cm²)')
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    title = ax.set_title(f'Time = {time_bins[0]:.2e} shakes')

    def update(frame):
        im.set_data(mesh_data_time_series[frame])
        title.set_text(f'Time = {time_bins[frame]:.2e} shakes')
        return [im, title]

    ani = animation.FuncAnimation(fig, update, frames=len(time_bins),
                                  interval=200, blit=True)

    ani.save('flux_evolution.mp4', writer='ffmpeg', fps=5, dpi=150)
    print("Animation saved to flux_evolution.mp4")

    return ani
```

## Common Plotting Tasks

### Task 1: Pre-Run Geometry Verification

**Critical step - ALWAYS do this:**
```bash
# Plot from 3 orthogonal directions
mcnp6 ip i=input.inp

# In PLOTG:
plot origin=0 0 0 basis=xy extent=100 100
plot origin=0 0 0 basis=xz extent=100 100
plot origin=0 0 0 basis=yz extent=100 100

# Zoom into complex regions
plot scales=0.3
# Check for dashed lines

# If dashed lines found:
#   1. Note location (use px, py to click)
#   2. Fix geometry (surfaces or cell definitions)
#   3. Re-plot to verify fix
#   4. Repeat until no dashed lines
```

### Task 2: Energy Spectrum Analysis

**Extract and plot spectrum:**
```python
# 1. Extract from MCTAL or output
# 2. Create log-log plot
# 3. Identify thermal/epithermal/fast regions
# 4. Compare to expected spectrum

# For neutrons:
#   Thermal peak: ~0.025 eV (room temperature)
#   Fission spectrum: ~1 MeV peak
#   Source energy: 14 MeV (D-T fusion), 2 MeV (Cf-252), etc.
```

### Task 3: Spatial Distribution Visualization

**For mesh tallies:**
```
1. Ensure input has: OUT=xdmf on FMESH card
2. Run MCNP (generates meshtal.xdmf + runtpe.h5)
3. Open in ParaView
4. Create slices through regions of interest
5. Identify hot spots, gradients, shielding effectiveness
6. Export images for documentation
```

### Task 4: Statistical Quality Verification

**Always check before trusting results:**
```python
# 1. Extract TFC data from output
# 2. Plot mean vs NPS → should stabilize
# 3. Plot error vs NPS → should follow 1/√N
# 4. Plot VOV vs NPS → should decrease to <0.1
# 5. Plot FOM vs NPS → should be constant

# If trends bad:
#   - Mean drifting → not converged, run longer
#   - Error not following 1/√N → variance reduction issues
#   - VOV high → few histories dominating, improve VR
#   - FOM decreasing → efficiency degrading, fix VR
```

### Task 5: Multi-Run Comparison (Parameter Study)

**Compare results from multiple runs:**
```python
import matplotlib.pyplot as plt

runs = ['baseline', 'case1', 'case2', 'case3']
fluxes = []
errors = []

for run in runs:
    # Extract total flux from each MCTAL
    data = parse_mctal(f'{run}/mctal', tally_num=4)
    fluxes.append(data['total_flux'])
    errors.append(data['total_error'])

# Bar plot with error bars
fig, ax = plt.subplots(figsize=(10, 6))
x_pos = np.arange(len(runs))

ax.bar(x_pos, fluxes, yerr=np.array(fluxes)*np.array(errors),
       capsize=5, alpha=0.7, edgecolor='black')

ax.set_xticks(x_pos)
ax.set_xticklabels(runs)
ax.set_ylabel('Total Flux (n/cm²)')
ax.set_title('Flux Comparison Across Parameter Study')
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('parameter_study.png', dpi=300)
```

## Integration with Other Skills

After plotting:

- **mcnp-geometry-checker**: If geometry plot shows errors (dashed lines), use to diagnose
- **mcnp-tally-analyzer**: Interpret physical meaning of plotted spectrum shapes
- **mcnp-statistics-checker**: If convergence plots show issues, validate in detail
- **mcnp-variance-reducer**: If FOM plot decreasing or convergence poor, improve VR

## Important Plotting Principles

1. **Geometry plotting is mandatory**
   - ALWAYS plot geometry before expensive runs
   - Dashed lines = errors, must fix
   - Plot from 3 orthogonal views minimum

2. **Log scales for wide ranges**
   - Energy spectra: log-log (spans eV to MeV)
   - Spatial flux: log if high dynamic range
   - Convergence: log-log for error vs NPS

3. **Error bars are essential**
   - Always show uncertainties on data plots
   - Error bars should be visible but not dominate
   - If error bars larger than data, statistics poor

4. **Color choices matter**
   - Use colorblind-friendly palettes for publication
   - High contrast for presentations
   - Sequential colormaps (viridis, plasma) for continuous data
   - Diverging colormaps (RdBu) for signed data

5. **Resolution and format**
   - Publication: 300 DPI minimum (PNG, PDF, or EPS)
   - Presentation: 150 DPI acceptable (PNG, JPEG)
   - Vector formats (PDF, SVG, EPS) for line plots
   - Raster (PNG) for mesh/image data

6. **Labels and titles**
   - Always label axes with units
   - Descriptive titles
   - Legend when multiple datasets
   - Annotations for important features

7. **Verify physical reasonableness**
   - Thermal peak at 0.025 eV for room temperature
   - Flux decreases with shielding
   - Spatial gradients smooth (unless interfaces)
   - Energy conservation (source energy matches max)

8. **Statistical convergence before interpretation**
   - Don't plot unconverged data without warning
   - Show convergence plots alongside results
   - Flag poor statistics prominently

9. **Documentation**
   - Save plot scripts for reproducibility
   - Record plot parameters (scales, ranges)
   - Include date, run ID, parameters in titles/filenames

10. **Automation for efficiency**
    - Write scripts for standard plots
    - Batch process multiple tallies/runs
    - Template plots for consistency

## Example Workflows

### Example 1: Geometry Verification Workflow

```
User: "I need to check if my reactor geometry is correct"

Claude: I'll help you verify your geometry using MCNP's interactive plotting tool. This is critical - we must check for geometry errors before running.

**Step 1: Launch Interactive Plotter**

Run this command:
```bash
mcnp6 ip i=reactor.inp
```

**Step 2: Create Standard Views**

In the PLOTG prompt, execute these commands:

```
# Top view (XY plane at Z=0)
plot origin=0 0 0 basis=xy extent=200 200
# Look for: radial fuel arrangement, control rod positions

# Side view (XZ plane at Y=0)
plot origin=0 0 0 basis=xz extent=200 300
# Look for: axial fuel stack, reflector top/bottom

# Front view (YZ plane at X=0)
plot origin=0 0 0 basis=yz extent=200 300
# Look for: symmetry verification

# Enable colors and labels
plot color=on
plot label=1
# Different colors show different materials/cells
```

**Step 3: Check for Errors**

⚠️ **CRITICAL**: Look for **dashed lines**

**If you see SOLID lines only:**
✓ Geometry is topologically correct
✓ No overlaps or gaps
✓ Proceed to detailed inspection

**If you see DASHED lines:**
❌ Geometry has ERRORS
❌ Must fix before running

To diagnose dashed lines:
1. Click on dashed region:
   ```
   px=50
   py=30
   # Shows which cells overlap or have undefined regions
   ```

2. Note cell numbers where dashed lines appear

3. Check those cells in input:
   - Surface definitions correct?
   - Boolean algebra correct?
   - Missing surfaces?

**Step 4: Zoom Into Complex Regions**

```
# Zoom to fuel assembly
plot origin=10 10 50 basis=xy extent=20 20 scales=0.5

# Check control rod insertion
plot origin=0 0 100 basis=xz extent=50 150
```

**Step 5: Verify Materials**

```
plot color=on
# Different colors should show:
# - Fuel (one color)
# - Moderator (another color)
# - Reflector (another color)
# - Void/coolant (another color)

# Click to verify:
px=position
py=position
# Confirms: cell=X, material=Y, density=Z
```

**Assessment:**

✓ No dashed lines found
✓ All 3 views checked
✓ Materials appear correct
✓ Symmetry verified

**Result: GEOMETRY VERIFIED - Ready to run**

Would you like me to:
1. Generate batch plot commands for documentation?
2. Create a plot script for future verification?
3. Help fix any geometry errors found?
```

### Example 2: Energy Spectrum Analysis

```
User: "Plot the neutron energy spectrum from my shielding calculation"

Claude: I'll create a publication-quality energy spectrum plot from your MCTAL file.

[Extracts tally data from MCTAL]

**Energy Spectrum Analysis - F4:N Neutron Flux**

[Generates Python plot]

```python
# Python script generated:
import matplotlib.pyplot as plt
import numpy as np

# Extracted data
energy_bins = np.array([1e-10, 1e-6, 1e-3, 0.1, 1.0, 10.0, 14.0])  # MeV
flux = np.array([1.23e-4, 5.67e-5, 3.45e-5, 1.89e-5, 8.23e-6, 2.34e-6])  # n/cm²
errors = np.array([0.05, 0.08, 0.10, 0.12, 0.15, 0.18])  # relative

# Calculate bin centers (geometric mean for log scale)
e_centers = np.sqrt(energy_bins[:-1] * energy_bins[1:])
abs_errors = flux * errors

# Create figure
fig, ax = plt.subplots(figsize=(10, 7))

ax.errorbar(e_centers, flux, yerr=abs_errors,
            fmt='o-', markersize=6, capsize=3, capthick=1.5,
            color='#0173B2', ecolor='gray', label='MCNP Calculation')

# Formatting
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Energy (MeV)', fontsize=13)
ax.set_ylabel('Flux (n/cm² per source neutron)', fontsize=13)
ax.set_title('Neutron Energy Spectrum - Behind 50 cm Concrete Shield',
             fontsize=14, fontweight='bold')

# Add reference lines
ax.axvline(1e-6, color='b', linestyle='--', alpha=0.3, label='Thermal (1 eV)')
ax.axvline(1e-3, color='g', linestyle='--', alpha=0.3, label='Epithermal (1 keV)')
ax.axvline(1.0, color='r', linestyle='--', alpha=0.3, label='Fast (1 MeV)')

# Energy group shading
ax.axvspan(1e-10, 1e-6, alpha=0.1, color='blue', label='Thermal region')
ax.axvspan(1e-6, 1e-3, alpha=0.1, color='green')
ax.axvspan(1e-3, 14, alpha=0.1, color='orange')

ax.grid(True, which='both', alpha=0.3, linestyle=':')
ax.legend(fontsize=10, loc='best')

plt.tight_layout()
plt.savefig('neutron_spectrum_publication.png', dpi=300, bbox_inches='tight')
plt.savefig('neutron_spectrum_publication.pdf', bbox_inches='tight')
print("Plots saved: PNG and PDF formats")

plt.show()
```

**Physical Interpretation:**

Thermal region (E < 1 eV): 1.23E-04 n/cm² (45% of total)
  → Significant thermalization from concrete moderation

Epithermal region (1 eV - 1 keV): 5.67E-05 n/cm² (21% of total)
  → Slowing-down neutrons

Fast region (E > 1 keV): Sum = 9.24E-05 n/cm² (34% of total)
  → Streaming fast neutrons from 14 MeV source

**Analysis:**
- Thermal peak confirms concrete acting as moderator
- Fast component shows incomplete moderation (expected for 50 cm)
- Spectrum shape consistent with D-T fusion source (14 MeV) attenuated by concrete
- Error bars small (<15%) indicates good statistics

**Recommendations:**
- For dose calculations: Focus on fast component (highest dose coefficients)
- To reduce fast flux: Add 20-30 cm more concrete OR add 5 cm borated polyethylene
- Thermal flux suitable for activation calculations

Would you like me to:
1. Create dose rate calculation from this spectrum?
2. Compare with analytical formula (e.g., point kernel)?
3. Plot spatial distribution (if you have mesh tally)?
```

## Code Style Guidelines

When creating plots:
- Use descriptive variable names
- Comment plot parameters
- Save plots before showing (prevents loss)
- Save in multiple formats (PNG for preview, PDF for publication)
- Use consistent color schemes within a project
- Include metadata in filenames (date, run ID, tally number)

## Dependencies

**Required Python packages:**
- `matplotlib` - Main plotting library
- `numpy` - Array operations
- `h5py` - For reading HDF5 mesh tally files

**Optional packages:**
- `plotly` - Interactive plots
- `scipy` - Curve fitting, smoothing
- `pandas` - Data organization
- `seaborn` - Statistical visualizations

**External tools:**
- ParaView - 3D mesh tally visualization (free)
- VisIt - Alternative 3D visualization (free)
- Gnuplot - Alternative plotting tool

**Required components:**
- Reference: `.claude/commands/mcnp-plotter.md` (detailed procedures)

## References

**Primary References:**
- `.claude/commands/mcnp-plotter.md` - Complete plotting procedures
- Chapter 6: Plotting (geometry, tallies, cross sections)
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Plotting section

**Geometry Plotting:**
- §6.1: PLOTG geometry plotting
- §3.4.1 item 2: Mandatory geometry plotting before runs
- Appendix: PLOTG command reference

**Tally Plotting:**
- §6.2: MCPLOT tally plotting
- Chapter 5.9: Tally specifications

**Mesh Tallies:**
- Appendix D.4: Mesh Tally XDMF format
- Chapter 8.5: Mesh tally output

**External Resources:**
- ParaView documentation: https://www.paraview.org/documentation/
- VisIt tutorials: https://visit-dav.github.io/visit-website/
- Matplotlib gallery: https://matplotlib.org/stable/gallery/

**Related Skills:**
- mcnp-geometry-checker: Diagnose geometry errors from plots
- mcnp-tally-analyzer: Interpret plotted results
- mcnp-statistics-checker: Validate convergence plots
- mcnp-mesh-builder: Create mesh tallies for 3D visualization
