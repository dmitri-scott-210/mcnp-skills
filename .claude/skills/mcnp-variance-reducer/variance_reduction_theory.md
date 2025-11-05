# Variance Reduction Theory and Fundamentals

## Overview

This reference provides the theoretical foundation for variance reduction (VR) in Monte Carlo particle transport simulations. Understanding these concepts is essential for effective VR implementation and optimization.

---

## Figure of Merit (FOM)

### Definition

The Figure of Merit quantifies the efficiency of a Monte Carlo simulation:

```
FOM = 1 / (R² × T)
```

**Where:**
- `R` = Relative error of tally (σ/mean)
- `T` = Computer time (minutes)
- `FOM` = Figure of Merit (particles²/minute)

### Interpretation

**FOM Values:**
- **Baseline (analog):** FOM_analog (no variance reduction)
- **Good VR:** FOM = 10-100× FOM_analog
- **Excellent VR:** FOM = 100-1000× FOM_analog
- **Poor VR:** FOM < FOM_analog (variance reduction made things worse!)

**Key Properties:**
1. **FOM should remain constant** as simulation runs longer
2. If FOM decreases → VR parameters incorrect
3. If FOM increases initially then stabilizes → VR converging

**Example:**
```
Analog run:    R=0.10, T=100 min → FOM = 1/(0.01×100) = 100
VR run:        R=0.10, T=1 min   → FOM = 1/(0.01×1) = 10,000
Improvement:   100× better efficiency
```

### FOM and Statistical Uncertainty

To achieve target relative error R_target in time T:

```
T = 1 / (FOM × R_target²)
```

**Example:**
- Target: R = 0.01 (1%)
- FOM = 10,000
- Time needed: T = 1/(10,000 × 0.0001) = 1 minute

---

## Splitting and Russian Roulette

### Fundamental Principle

Monte Carlo conserves **expected particle weight**, not particle count. Variance reduction manipulates particle population while maintaining correct expected values.

### Splitting (Entering Higher Importance Region)

**When:** Particle moves from cell with importance I_old to cell with I_new where I_new > I_old

**Process:**
1. Calculate split ratio: `N = I_new / I_old`
2. Create N particles from original
3. Each new particle has weight: `w_new = w_original / N`

**Example:**
```
Particle: weight = 1.0, in cell with IMP:N=1
Moves to: cell with IMP:N=4
Split ratio: N = 4/1 = 4
Result: 4 particles, each with weight = 1.0/4 = 0.25
Expected weight: 4 × 0.25 = 1.0 ✓ (conserved)
```

**Effect:**
- More particles in important regions
- Each carries less weight
- Reduces variance in tally statistics

### Russian Roulette (Entering Lower Importance Region)

**When:** Particle moves from cell with importance I_old to cell with I_new where I_new < I_old

**Process:**
1. Calculate survival probability: `P_survive = I_new / I_old`
2. Generate random number: `ξ ∈ [0,1]`
3. If `ξ < P_survive`: Particle survives with weight `w_new = w_original / P_survive`
4. If `ξ ≥ P_survive`: Particle killed (weight = 0)

**Example:**
```
Particle: weight = 1.0, in cell with IMP:N=4
Moves to: cell with IMP:N=1
Survival probability: P = 1/4 = 0.25
Outcome 1 (25% chance): Survives with weight = 1.0/0.25 = 4.0
Outcome 2 (75% chance): Killed (weight = 0)
Expected weight: 0.25×4.0 + 0.75×0 = 1.0 ✓ (conserved)
```

**Effect:**
- Fewer particles in unimportant regions
- Survivors carry more weight
- Reduces computation in low-importance regions

### Weight Conservation Proof

**Splitting:**
```
E[w_after] = N × (w/N) = w = E[w_before] ✓
```

**Russian Roulette:**
```
E[w_after] = P_survive × (w/P_survive) + (1-P_survive) × 0
           = w ✓
```

---

## Weight Window Mechanics

### Weight Window Bounds

For each phase space region (position, energy, time), define:

```
w_lower = WWN value (lower bound)
w_upper = w_lower × wupn (upper bound)
w_survive = w_lower × wsurvn (survival weight target)
```

**Default MCNP Parameters:**
- `wupn = 5` (upper bound multiplier)
- `wsurvn = 3` (survival weight multiplier)
- `mxspln = 5` (maximum splits per event)

### Weight Window Actions

**Case 1: w < w_lower (Underweight)**
- **Action:** Russian Roulette
- **Survival probability:** `P = w / w_survive`
- **New weight (if survives):** `w_new = w_survive`
- **Purpose:** Cull weak particles, boost survivors to target weight

**Case 2: w > w_upper (Overweight)**
- **Action:** Splitting
- **Number of splits:** `N ≈ w / w_survive` (rounded to integer)
- **New weight (each particle):** `w_new ≈ w_survive`
- **Purpose:** Break up heavy particles to target weight

**Case 3: w_lower ≤ w ≤ w_upper (In Window)**
- **Action:** None (particle weight acceptable)
- **Purpose:** Minimize computational overhead

### Example Weight Window Bounds

```
WWN (w_lower) = 1.0
wupn = 5 → w_upper = 1.0 × 5 = 5.0
wsurvn = 3 → w_survive = 1.0 × 3 = 3.0

Particle weight = 0.5:
  - Below w_lower (1.0)
  - Russian roulette: P = 0.5/3.0 = 16.7%
  - If survives: w_new = 3.0

Particle weight = 8.0:
  - Above w_upper (5.0)
  - Split: N ≈ 8.0/3.0 ≈ 3 particles
  - Each: w_new ≈ 8.0/3 ≈ 2.67

Particle weight = 2.5:
  - In window [1.0, 5.0]
  - No action
```

### Optimal Weight Window Strategy

**Goal:** Keep all particle weights near `w_survive` for minimum variance

**Theory:**
```
Variance ∝ Σ(w_i - w_avg)²
```

Minimized when all weights equal → target all particles to w_survive

---

## Importance Function

### Theoretical Definition

The importance function I(r⃗, E, t) represents:

```
I(r⃗, E, t) = Expected contribution to tally per unit weight
             at phase space point (position r⃗, energy E, time t)
```

**Physical Interpretation:**
- **High importance:** Particle likely to contribute to detector
- **Low importance:** Particle unlikely to reach detector

### Relationship to Weight Windows

Optimal weight window values inversely proportional to importance:

```
w_optimal(r⃗, E, t) = C / I(r⃗, E, t)
```

Where C is normalization constant.

**Intuition:**
- **Near detector (high importance):**
  - I is large → w_optimal is small
  - Split particles → many low-weight particles
  - Good statistics at detector

- **Far from detector (low importance):**
  - I is small → w_optimal is large
  - Russian roulette → few high-weight particles
  - Don't waste computation far from detector

### Practical Estimation Methods

**Method 1 - WWG (Weight Window Generator):**
```
I(r⃗,E) ≈ Φ(r⃗,E) / Φ_detector(E)
```
- Run forward simulation
- Estimate flux Φ everywhere
- Ratio to detector flux gives importance

**Method 2 - Manual Geometric:**
```
I(r) ≈ (1/r²) × transmission(r→detector)
```
- For simple geometries
- Cell importance ∝ inverse distance squared

**Method 3 - Adjoint (Advanced):**
```
I(r⃗,E) = Φ†(r⃗,E)
```
- Adjoint flux IS the importance
- Requires adjoint solver (ADVANTG, etc.)
- Near-optimal for complex problems

---

## WWG (Weight Window Generator) Algorithm

### Overview

WWG automatically generates weight window values from forward simulation results.

### Algorithm Steps

**Step 1: Run Forward Simulation with Detector Tally**
```
F5:N  100 0 0  0.5        $ Point detector
WWG   5  0  1.0           $ Generate WW from tally 5
MESH  GEOM=XYZ ...        $ Define spatial mesh
WWGE:N 1e-8 0.1 1 10 20   $ Define energy bins
```

**Step 2: Estimate Importance from Flux**

For each mesh cell (i) and energy group (g):
```
I(i,g) ≈ Φ(i,g) / Φ_detector(g)
```

Where:
- Φ(i,g) = flux in mesh cell i, energy group g
- Φ_detector(g) = flux at detector, energy group g

**Step 3: Calculate Weight Window Lower Bounds**
```
WWN(i,g) = target × Φ_detector(g) / Φ(i,g)
```

Where:
- `target` = third parameter of WWG card (default 1.0)
- Controls overall weight scale

**Step 4: Write to wwout File**

MCNP writes binary wwout file containing:
- Weight window values for all mesh cells
- Energy group structure
- Geometry parameters

**Step 5: Use in Subsequent Runs**
```
WWP:N  J  J  J  0  -1     $ switchn=-1: read wwout
```

### Iteration and Convergence

**Iteration Process:**
1. Run 1: WWG generation (analog or simple VR)
2. Run 2: Use wwout, regenerate improved WWG
3. Run 3: Use improved wwout, regenerate again
4. Repeat until converged (typically 2-5 iterations)

**Convergence Indicators:**
- FOM improvement <20% between iterations
- WWN values change <10%
- Detector relative error <10%

### WWG Target Parameter

**Effect of Target Value:**
- `target = 0.1`: Lower weights → more particles
- `target = 1.0`: Moderate (default)
- `target = 10.0`: Higher weights → fewer particles

**Selection Guide:**
- Start with target = 1.0
- If too many splits/roulettes → increase target
- If poor statistics → decrease target

---

## Advanced Theory Topics

### Variance Reduction Effectiveness

**Ideal VR:**
```
Variance_VR / Variance_analog = 1 / N_eff
```

Where N_eff is effective particle multiplication factor.

**FOM Relationship:**
```
FOM_VR / FOM_analog = N_eff / (1 + overhead)
```

Overhead from splitting/roulette operations typically 10-20%.

### Energy-Dependent Importance

For energy-dependent problems:
```
I(r⃗,E) ≠ I_spatial(r⃗) × I_energy(E)
```

Importance is coupled → need energy-dependent weight windows (WWE).

### Time-Dependent Importance

For time-dependent problems (pulses, decay):
```
I(r⃗,E,t) varies with time
```

Need time-dependent weight windows (WWT).

---

## Statistical Considerations

### Tally Variance with VR

```
σ²_tally = (1/N) × Σ[w_i × score_i]² - (mean)²
```

Variance depends on:
1. Particle count N (more is better)
2. Weight distribution (narrow is better)
3. Score distribution (physics-dependent)

### Weight Distribution

**Optimal:** All particles same weight (minimum variance)

**Reality:** Weight windows keep distribution narrow

**Monitor:** Check output for weight statistics
```
minimum weight:  0.05
average weight:  1.0
maximum weight:  5.0
```

If max/min > 100 → weight windows may need adjustment

---

## References

**See Also:**
- `card_specifications.md` - VR card syntax and parameters
- `wwg_iteration_guide.md` - Practical WWG workflows
- `error_catalog.md` - Common VR problems and solutions

**MCNP6 Manual:**
- Chapter 2.7: Variance Reduction Theory
- Chapter 5.12: Variance Reduction Cards
- Appendix D: Weight Windows

**Literature:**
- Cooper & Larsen, "Automated Weight Window Generation" (2001)
- Haghighat & Wagner, "CADIS Method" (2003)
- MCNP6 User Manual, LA-CP-13-00634
