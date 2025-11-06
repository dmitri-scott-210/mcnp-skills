# Variance Reduction Example Inputs

## Overview

This directory contains representative MCNP input files demonstrating variance reduction techniques for common problem types. Each example shows baseline (analog) configuration and can be modified to demonstrate VR methods.

**Source:** MCNP6 Variance Reduction Workshop examples (LANL)

---

## Examples

### 01_duct_streaming.i

**Problem Type:** Concrete duct with streaming path

**Geometry:**
- 19 concrete cells (10 cm thick each, 180 cm total length)
- Cylindrical duct (radius 10 cm)
- Source at one end, detector at far end
- Neutron and photon transport

**Baseline Configuration:**
- Analog (all cells IMP:N = IMP:P = 1)
- F1:P tally at far end (surface 19)

**VR Techniques to Demonstrate:**
1. **Cell Importance (IMP):**
   - Change `IMP:N 1 18r 0 0` to `IMP:N 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 0 0`
   - Geometric progression along duct
   - Expected FOM improvement: 50-200×

2. **Weight Windows (WWG):**
   - Add `WWG 1 0 1.0` (generate from F1 tally)
   - Add `WWGE:P 0 0.1 1 10 20` (energy bins)
   - First run: generate wwout
   - Second run: replace WWG with `WWP:P J J J 0 -1`
   - Expected FOM improvement: 100-500×

3. **Mesh-Based WW:**
   - Add MESH card:
     ```
     MESH GEOM=CYL REF=-22 0 0 AXS=0 1 0 VEC=1 0 0 ORIGIN=-22 0 -10
          IMESH=10 IINTS=1
          JMESH=180 JINTS=18
          KMESH=360 KINTS=1
     ```
   - Use with WWG for automatic mesh-based importance

**Physics:**
- 2 MeV and 14 MeV source photons (90/10 mix)
- Concrete composition typical for shielding

---

### 02_room_geometry.i

**Problem Type:** Complex room geometry with multiple regions

**Geometry:**
- Multi-room configuration
- Various materials (concrete, air, steel)
- Realistic shielding scenario

**Baseline Configuration:**
- Analog transport
- Multiple detector locations

**VR Techniques to Demonstrate:**
1. **Cell Importance:**
   - Manual importance assignment by region
   - Higher importance near detectors

2. **Weight Window Generator:**
   - Automatic importance from tally distribution
   - Mesh-based generation for complex geometry

**Applications:**
- Facility dose calculations
- Multi-room transport problems
- Scattered radiation assessment

---

### 03_maze_penetration.i

**Problem Type:** Deep penetration through maze geometry

**Geometry:**
- Multiple legs with turns (dogleg configuration)
- Concrete walls
- Long streaming paths

**Baseline Configuration:**
- Analog (poor statistics expected)

**VR Techniques to Demonstrate:**
1. **Weight Windows with WWG:**
   - Essential for this geometry
   - Automatic importance through maze paths
   - Iterate 3-5 times for convergence

2. **Exponential Transform (Advanced):**
   - Apply in straight sections
   - Use with WW to control weights
   - Parameter: p = 0.7-0.8 for neutrons in concrete

**Challenge:**
- Particles must navigate multiple turns
- Rare events (very low transmission)
- Excellent test of VR effectiveness

**Expected FOM Improvement:**
- Without VR: FOM ~ 0 (essentially no tallies)
- With WWG: FOM improves by 1000-10,000×

---

### 04_iron_detector.i

**Problem Type:** Point detector in iron shield

**Geometry:**
- Iron shielding
- Point detector configuration

**Baseline Configuration:**
- Analog transport
- Point detector tally (F5)

**VR Techniques to Demonstrate:**
1. **DXTRAN Sphere:**
   - Deterministic transport to detector
   - Inner/outer sphere optimization
   - DXC cards to control particle creation

2. **Weight Windows:**
   - Control DXTRAN particle weights
   - Prevent weight fluctuations

3. **Combined DXTRAN + WWG:**
   - DXTRAN creates particles at detector
   - WWG optimizes importance throughout geometry
   - Synergistic effect: 100-500× improvement

**Point Detector Considerations:**
- R0 parameter (radius for last flight)
- Flux vs. current formulation
- Energy binning

---

### 05_gamma_lead_shield.i

**Problem Type:** Photon transport through lead shielding

**Geometry:**
- High-Z material (lead)
- Deep penetration problem

**Baseline Configuration:**
- Analog transport
- Photon-only MODE

**VR Techniques to Demonstrate:**
1. **Exponential Transform:**
   - Optimal for photons in high-Z
   - Parameter: p = 0.85-0.95
   - Must use with weight windows

2. **Weight Windows:**
   - Control EXT weight variation
   - Essential for reliable results

3. **Implicit Capture:**
   - Automatically ON with weight cutoff
   - Survival biasing reduces absorption variance

**Physics:**
- Photoelectric absorption dominant at low E
- Compton scattering at medium E
- Pair production at high E

**Expected FOM Improvement:**
- EXT alone (no WW): Unreliable (don't do this!)
- EXT + WW: 500-2000× improvement

---

### 06_dogleg_geometry.i

**Problem Type:** Bent duct (dogleg) configuration

**Geometry:**
- Two-leg duct with 90° bend
- Concrete shielding
- Streaming followed by scattering

**Baseline Configuration:**
- Analog transport

**VR Techniques to Demonstrate:**
1. **Cell Importance:**
   - Different importance in each leg
   - Higher importance after bend

2. **Weight Windows:**
   - Automatic handling of bend geometry
   - WWG estimates importance around corner

3. **Source Biasing:**
   - Bias source direction toward duct entrance
   - Reduce wasted particles

**Challenge:**
- Particles must scatter around corner
- Direct streaming only in first leg
- Tests VR robustness for directional changes

---

## Usage Workflow

### Baseline (Analog) Run

**Purpose:** Establish baseline FOM before applying VR.

```bash
mcnp6 i=01_duct_streaming.i o=duct_analog.out
```

**Extract FOM:**
- Look for "tally fluctuation charts" in output
- Note final FOM value
- Check if relative error achievable in reasonable time

### VR Method Testing

**Step 1: Apply VR technique**
- Modify input file (add IMP, WWG, EXT, etc.)
- Keep same NPS initially for fair comparison

**Step 2: Run and compare**
```bash
mcnp6 i=01_duct_streaming_vr.i o=duct_vr.out
```

**Step 3: Evaluate**
- Compare FOM_vr / FOM_analog (goal: >10×)
- Check all 10 statistical tests pass
- Verify weight statistics reasonable

### WWG Iteration Workflow

**Iteration 1 (Generate):**
```bash
# Input: Add WWG card
mcnp6 i=problem_wwg1.i o=wwg1.out
# Output: wwout file created
```

**Iteration 2 (Refine):**
```bash
# Input: Replace WWG with WWP:N J J J 0 -1, add WWG back
mcnp6 i=problem_wwg2.i o=wwg2.out
# Output: improved wwout
```

**Iteration 3+ (Converge):**
- Repeat until FOM change <20%
- Typical: 2-5 iterations

**Production:**
```bash
# Input: Use converged wwout, remove WWG card, increase NPS 10-100×
mcnp6 i=problem_production.i o=production.out
```

---

## Modification Guide

### Adding Cell Importance

```
Before:
imp:n 1 18r 0 0

After (geometric progression):
imp:n 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 0 0
```

### Adding Weight Window Generator

```
# Add after tally definition
WWG 1 0 1.0
c   ^tally number  ^time group  ^target weight

# Optional: Add energy bins
WWGE:N 0 1e-9 1e-6 1e-3 0.1 1 10 20
```

### Adding Exponential Transform

```
# Add after mode card
EXT:N 0.75 2 3 4 5
c     ^p value  ^cells
c
VECT 0 1 0
c    ^preferred direction (+y for these examples)
c
# MUST also add weight windows!
WWG 1 0 1.0
```

### Adding DXTRAN Sphere

```
# Add after tally definition
DXT:N 0 180 0 10 50
c     ^detector location  ^inner radius  ^outer radius
c
# Optional: Control contribution probability by cell
DXC:N 1 0.5 0.1 0.01
c     ^cells 1-4 with decreasing probability
```

---

## Common VR Combinations

### Simple Geometry: Cell Importance Only
- Fast to set up
- Effective for <10 regions
- FOM improvement: 5-50×

### Complex Geometry: WWG Automatic
- Mesh-based generation
- Iterate 2-5 times
- FOM improvement: 20-500×

### Deep Penetration: WWG + EXT
- Exponential transform for direction
- Weight windows for weight control
- FOM improvement: 100-5000×

### Point Detector: DXTRAN + WWG
- DXTRAN to detector sphere
- WWG for importance throughout
- FOM improvement: 50-500×

---

## Troubleshooting

### FOM Decreasing
- VR parameters incorrect
- Overbiasing problem regions
- **Solution:** Remove VR, test incrementally

### Statistical Checks Failing
- High-weight particles causing variance
- Insufficient sampling in some regions
- **Solution:** Add/widen weight windows

### No Improvement
- VR not addressing true problem
- Wrong tally targeted by WWG
- **Solution:** Analyze analog run, understand particle paths

---

## References

**See Main Skill Documentation:**
- `../variance_reduction_theory.md` - FOM, splitting/RR fundamentals
- `../advanced_vr_theory.md` - WWG algorithm, optimization strategies
- `../mesh_based_ww.md` - Mesh-based weight window generation
- `../advanced_techniques.md` - EXT, FCL, specialized methods
- `../wwg_iteration_guide.md` - Step-by-step WWG workflows

**MCNP6 Manual:**
- Chapter 2.7: Variance Reduction Theory
- Chapter 5.12: Variance Reduction Cards
- Chapter 10.6: Variance Reduction Examples
