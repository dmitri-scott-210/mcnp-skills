# Cell Selection Guide for Depletion Tracking
**Comprehensive Criteria and Examples**

## Purpose

This guide provides detailed criteria for selecting which cells to track during MCNP burnup calculations, based on production HTGR reactor models (AGR-1, μHTGR) and best practices.

---

## The Selection Problem

**Challenge**: Reactor models commonly have 1,000-10,000 cells, but tracking all cells for burnup is computationally infeasible.

**Example Scaling**:
```
5,000 cells × 40 isotopes × 20 time steps × 3 MCNP/ORIGEN iterations
= 12,000,000 ORIGEN calculations
= ~6 months runtime on typical cluster
```

**Solution**: Strategic selection of ~100-200 high-importance cells can capture >99% of the physics while reducing runtime by 95-99%.

---

## Selection Criteria

### Priority 1: MUST TRACK (Critical for Physics)

#### 1.1 Fuel Cells

**Criteria**:
- Contains fissile material (U-235, Pu-239, U-233)
- Neutron flux > 1E13 n/cm²/s
- Contributes >0.1% of total fission power

**Rationale**:
- Fuel composition drives reactivity
- Fissile depletion and Pu buildup are primary burnup effects
- Fission product poisoning (Xe-135, Sm-149) critical for criticality

**Examples**:
- PWR: All fuel pin cells in core (or grouped by assembly/zone)
- HTGR: TRISO fuel kernels in compacts
- Fast reactor: MOX fuel pins
- Research reactor: HEU fuel plates

**Typical count**: 50-100 cells (or groups)

#### 1.2 Burnable Absorbers

**Criteria**:
- Contains B-10, Gd-155/157, or Er-167
- Located in high neutron flux (>1E12 n/cm²/s)
- Designed to burn out over time

**Rationale**:
- Burnout changes reactivity significantly (-1000 to -5000 pcm)
- Controls power distribution and cycle length
- Depletion is intentional and must be tracked

**Examples**:
- Gadolinia rods (UO₂-Gd₂O₃)
- Borosilicate glass rods
- Integral fuel burnable absorbers (IFBA)
- Borated graphite holders (HTGR)

**Typical count**: 10-30 cells

#### 1.3 Control Rods

**Criteria**:
- Contains strong absorbers: Ag-In-Cd, B₄C, Hf
- Inserted for significant fraction of cycle
- Flux > 1E11 n/cm²/s when inserted

**Rationale**:
- Absorber depletion reduces control worth
- Affects shutdown margin
- Activation products may impact dose rates

**Examples**:
- PWR Ag-In-Cd control rods
- BWR B₄C blades
- HTGR hafnium shrouds
- Fast reactor tantalum rods

**Typical count**: 5-15 cells (per rod assembly)

---

### Priority 2: SHOULD TRACK (Important for Activation/Dose)

#### 2.1 Structural Materials Near Core

**Criteria**:
- Stainless steel, zircaloy, or nickel alloys
- Flux > 1E12 n/cm²/s
- Located within 50 cm of fuel

**Rationale**:
- Activation products (Co-60, Fe-55, Mn-54, Ni-63)
- Become major dose sources after shutdown
- Important for decommissioning planning

**Examples**:
- PWR core barrel, baffle plates
- Fuel assembly spacer grids
- HTGR capsule walls
- Reactor pressure vessel inner wall

**Typical count**: 20-50 cells

#### 2.2 Graphite/Beryllium Reflectors Near Core

**Criteria**:
- Carbon or beryllium
- Flux > 1E11 n/cm²/s
- Adjacent to fuel or high-flux regions

**Rationale**:
- C-14 production (long-lived, β-emitter)
- Tritium production (beryllium)
- Low-level waste characterization

**Examples**:
- HTGR graphite reflector blocks
- Gas-cooled reactor moderator
- Research reactor beryllium reflector

**Typical count**: 10-30 cells

---

### Priority 3: MAY TRACK (If Resources Permit)

#### 3.1 Moderator in Moderate Flux

**Criteria**:
- Water, heavy water, or graphite
- Flux 1E10-1E12 n/cm²/s
- Not adjacent to fuel

**Rationale**:
- Tritium production (for environmental monitoring)
- Minor activation of impurities
- Generally low impact on core physics

**Examples**:
- PWR lower plenum water
- CANDU moderator away from fuel
- Graphite far from core

**Typical count**: 0-10 cells (often skipped)

#### 3.2 Coolant in High Flux

**Criteria**:
- Water, sodium, or helium
- Flux > 1E12 n/cm²/s
- Flowing through core

**Rationale**:
- N-16 production (water, short-lived)
- Na-24 production (sodium, dose during operation)
- Usually tracked for dose estimation, not physics

**Examples**:
- PWR coolant channels (for N-16 activity)
- SFR sodium coolant (Na-22, Na-24)

**Typical count**: 0-5 cells (often use separate activation calculation)

---

### Priority 4: DO NOT TRACK (Negligible Impact)

#### 4.1 Low-Flux Regions

**Criteria**:
- Flux < 1E10 n/cm²/s
- Any material type

**Rationale**:
- Negligible burnup/activation in reasonable irradiation times
- Wastes computational resources
- No impact on reactivity or dose

**Examples**:
- Outer biological shield
- Reactor building structures
- Coolant inlet/outlet far from core
- Concrete shielding

#### 4.2 External Structures

**Criteria**:
- Located >2 m from core center
- Separated by thick shielding

**Rationale**:
- Essentially zero flux
- No physics relevance
- Would require thousands of years to see any effect

**Examples**:
- Containment building
- Auxiliary systems
- Steam generators (unless adjacent to core)

#### 4.3 Void Regions

**Criteria**:
- Air, vacuum, or very low-density gas
- Any flux level

**Rationale**:
- No material to deplete
- No activation products
- Physically meaningless

**Examples**:
- Air gaps
- Void cells for geometry
- Gas plenums (helium, void)

---

## Flux-Based Ranking System

**Use F4 tallies to rank cells** before burnup calculation:

### Step 1: Initial MCNP Run

```mcnp
c Flux survey run
F4:n  100 101 102 103 104 ... 999  $ All candidate cells
```

Run MCNP (no burnup) to get flux in all cells of interest.

### Step 2: Extract and Rank Fluxes

```python
import numpy as np
import pandas as pd

# Read MCNP output flux tallies
fluxes = pd.read_csv('flux_survey.csv')  # cell_id, flux, rel_error

# Rank by flux
fluxes_sorted = fluxes.sort_values('flux', ascending=False)

# Define thresholds
fuel_threshold = 1e13
absorber_threshold = 1e12
structural_threshold = 1e11

# Categorize
fuel_cells = fluxes_sorted[fluxes_sorted['flux'] > fuel_threshold]
absorber_cells = fluxes_sorted[(fluxes_sorted['flux'] > absorber_threshold) &
                                 (fluxes_sorted['flux'] <= fuel_threshold)]
structural_cells = fluxes_sorted[(fluxes_sorted['flux'] > structural_threshold) &
                                   (fluxes_sorted['flux'] <= absorber_threshold)]

print(f"Fuel cells (φ > 1E13): {len(fuel_cells)}")
print(f"Absorber cells (1E12 < φ < 1E13): {len(absorber_cells)}")
print(f"Structural cells (1E11 < φ < 1E12): {len(structural_cells)}")
print(f"Total to track: {len(fuel_cells) + len(absorber_cells) + len(structural_cells)}")
```

### Step 3: Group Similar Cells

**For repeated structures** (lattices, identical assemblies):

```python
# Group cells with similar flux and geometry
def group_cells_by_similarity(cells, flux_tolerance=0.1):
    """
    Group cells with similar flux spectra
    flux_tolerance: fraction difference allowed (0.1 = 10%)
    """
    groups = []
    ungrouped = cells.copy()

    while len(ungrouped) > 0:
        # Take first cell as group representative
        rep = ungrouped.iloc[0]
        group = [rep]

        # Find similar cells
        for idx, cell in ungrouped.iterrows():
            if abs(cell['flux'] - rep['flux']) / rep['flux'] < flux_tolerance:
                group.append(cell)

        groups.append(group)
        ungrouped = ungrouped.drop([c.name for c in group])

    return groups

# Apply grouping
fuel_groups = group_cells_by_similarity(fuel_cells)
print(f"Reduced {len(fuel_cells)} fuel cells to {len(fuel_groups)} groups")
```

---

## Real-World Examples

### Example 1: AGR-1 HTGR Test

**Total cells**: ~1,600

**Selected cells** (152 total):
1. **Fuel kernels**: 72 cells
   - 6 capsules × 3 stacks × 4 compacts = 72 unique regions
   - Each has different flux/temperature history
   - Cannot be grouped (experimental requirement)

2. **Stainless steel structures**: 36 cells
   - Capsule walls (6 cells)
   - Holders and supports (18 cells)
   - Thermocouples and sensors (12 cells)
   - Activation important for dose rates

3. **Graphite spacers**: 24 cells
   - Above/below fuel compacts
   - 2 per capsule × 6 capsules × 2 positions = 24
   - C-14 production tracked

4. **Borated graphite holders**: 12 cells
   - 2 per capsule × 6 capsules = 12
   - B-10 depletion affects reactivity

5. **Hafnium shrouds**: 8 cells
   - Control material
   - Hf-177 burnout critical

**Not tracked** (~1,448 cells):
- ATR driver fuel (separate calculation)
- Coolant water (transient activation)
- Outer reflectors
- Beryllium blocks (low flux)
- Support structures
- Shielding

**Result**: 9.5% of cells tracked, >99% physics captured

### Example 2: Typical PWR Core

**Total cells**: ~50,000 (detailed pin-by-pin model)

**Selected cells** (264 total):
1. **Fuel pins**: 192 cells
   - 193 assemblies in core
   - Group by enrichment and position:
     * Fresh fuel, inner core (48 assemblies → 1 rep)
     * Fresh fuel, outer core (48 assemblies → 1 rep)
     * Once-burned, inner (48 assemblies → 1 rep)
     * Once-burned, outer (48 assemblies → 1 rep)
   - Result: 4 groups instead of 48,000 pins

2. **Burnable absorbers**: 48 cells
   - Gadolinia rods in fresh assemblies
   - Cannot group (different positions burn differently)

3. **Control rods**: 16 cells
   - 4 control banks × 4 axial zones = 16
   - Ag-In-Cd absorber

4. **Structural**:  8 cells
   - Core barrel (SS-304)
   - Baffle plates

**Not tracked**:
- Individual coolant channels (49,000+ cells)
- Cladding (tracked with fuel)
- Grid spacers (lumped into structural)
- Pressure vessel
- Steam generators
- Containment

**Result**: 0.5% of cells tracked, 98% physics captured

### Example 3: Fast Reactor (SFR)

**Total cells**: ~5,000

**Selected cells** (120 total):
1. **Driver fuel**: 60 cells
   - MOX pins, inner/outer core
   - 20 assemblies × 3 radial zones = 60

2. **Blanket assemblies**: 30 cells
   - Depleted U-238 for Pu breeding
   - 15 assemblies × 2 zones = 30

3. **Control rods**: 18 cells
   - B₄C absorber
   - 6 rods × 3 axial positions = 18

4. **Reflector**: 12 cells
   - Stainless steel
   - Activation tracking

**Not tracked**:
- Sodium coolant (separate activation calculation)
- Shield assemblies
- Reactor vessel
- Guard vessel

**Result**: 2.4% of cells tracked

---

## Validation of Cell Selection

**After running burnup calculation**, verify selection was adequate:

### Check 1: Reactivity Balance

```python
# Total reactivity change should equal tracked contributions
rho_total = k_BOL - k_EOL
rho_fuel = delta_k_from_fuel_depletion
rho_FP = delta_k_from_FP_buildup
rho_Pu = delta_k_from_Pu_buildup
rho_absorbers = delta_k_from_absorber_burnout

error = abs(rho_total - (rho_fuel + rho_FP + rho_Pu + rho_absorbers))
print(f"Reactivity balance error: {error:.1f} pcm")

# Acceptable if error < 100 pcm
```

### Check 2: Power Distribution

```python
# Fission power from tracked cells should equal total power
tracked_power = sum([P_i for i in tracked_cells])
total_power = reactor_thermal_power

fraction = tracked_power / total_power
print(f"Tracked power fraction: {fraction:.1%}")

# Should be >98% for fuel cells
```

### Check 3: Dose Rate Contributions

```python
# After shutdown, check which cells contribute most to dose
dose_contributions = calculate_dose_from_each_cell()
tracked_dose = sum([dose_contributions[i] for i in tracked_cells])
total_dose = sum(dose_contributions.values())

fraction = tracked_dose / total_dose
print(f"Tracked dose rate fraction: {fraction:.1%}")

# Should be >80% (some untracked activation is acceptable)
```

---

## Common Mistakes

### Mistake 1: Tracking Everything

**Problem**: User tracks all 5,000 cells

**Impact**:
- Runtime: 6-12 months
- Cost: $100,000+ in computing time
- Benefit: <1% improvement in accuracy

**Fix**: Use flux-based ranking, track only high-importance cells

### Mistake 2: Omitting Absorbers

**Problem**: User tracks fuel but forgets burnable absorbers

**Impact**:
- k_eff prediction wrong by 2000-5000 pcm
- Cycle length wrong
- Power distribution wrong

**Fix**: Always track burnable absorbers

### Mistake 3: Grouping Non-Similar Cells

**Problem**: User groups inner and outer fuel assemblies

**Impact**:
- Inner cells over-depleted (higher flux)
- Outer cells under-depleted (lower flux)
- Reactivity error 500-1000 pcm

**Fix**: Only group cells with <10% flux difference

### Mistake 4: Tracking Coolant Channels

**Problem**: User tracks 40,000 coolant cells

**Impact**:
- No physics benefit (coolant doesn't deplete)
- Massive runtime increase
- Wasted resources

**Fix**: Skip coolant cells, or use single representative for activation only

---

## Cell Selection Checklist

Before running burnup calculation:

- [ ] Run flux survey (F4 tallies on all candidate cells)
- [ ] Rank cells by flux magnitude
- [ ] Identify all fuel cells (φ > 1E13): MUST track
- [ ] Identify all burnable absorbers: MUST track
- [ ] Identify control rods: SHOULD track if inserted >50% of time
- [ ] Identify structural materials (φ > 1E12): SHOULD track for activation
- [ ] Group similar cells (flux difference <10%)
- [ ] Verify total tracked cells <200 (if more, consider additional grouping)
- [ ] Document selection rationale
- [ ] Verify power balance after first burnup step
- [ ] Adjust selection if reactivity balance poor

---

## Automation Script

See `cell_selector.py` in the scripts directory for automated cell selection based on flux tallies.

**Usage**:
```bash
python cell_selector.py --flux-file mcnp_output.o --threshold 1e12 --output selected_cells.txt
```

---

**References**:
- AGR-1 HTGR Benchmark Model
- SCALE depletion analysis methodology
- OECD/NEA burnup benchmark specifications
