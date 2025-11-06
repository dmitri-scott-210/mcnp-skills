# Advanced Variance Reduction Techniques

## Overview

This reference covers advanced variance reduction methods beyond basic cell importance and weight windows: exponential transform (EXT), forced collisions (FCL), energy/time splitting and roulette, and specialized techniques for challenging problems.

**Prerequisites:** Understand basic VR (IMP, WWN, WWG) from `variance_reduction_theory.md`.

---

## Exponential Transform (EXT)

### Theory (§2.7.2.13)

The exponential transform biases particle transport in a preferred direction by modifying the distance-to-collision sampling.

**Analog Sampling:**
```
Distance to collision: s = -ln(ξ) / Σ_t
```

**Transformed Sampling:**
```
Fictitious cross section: Σ*_t = Σ_t(1 - p·μ)
Distance to collision:    s = -ln(ξ) / Σ*_t
Weight adjustment:        w' = w · exp(-p·μ·Σ_t·s)
```

**Where:**
- `p` = Transform parameter (0 < p < 1)
- `μ` = Cosine of angle between particle direction and preferred direction
- `Σ_t` = Total cross section
- `ξ` = Random number

**Effect:**
- `μ = +1` (toward preferred direction): Σ*_t reduced → longer flights
- `μ = -1` (away from preferred direction): Σ*_t increased → shorter flights
- Weight adjusted to preserve expected behavior

### EXT Card Syntax

```
EXT:p  p_value  I_cell₁  I_cell₂  ...  I_cellₙ
```

**Parameters:**
- `p` = Particle type (N, P, etc.)
- `p_value` = Transform parameter (typically 0.5-0.95)
  - 0 = No biasing (analog)
  - ~0.7 = Moderate (neutrons in concrete/earth)
  - ~0.9 = Strong (photons in high-Z materials)
  - ≥1.0 = Invalid (causes negative cross sections)
- `I_cellᵢ` = Cell numbers where EXT applied

**Preferred Direction:**
Specified on separate VECT card or defaults to +x direction.

### VECT Card (Preferred Direction)

```
VECT  u_x  u_y  u_z
```

Defines unit vector for preferred direction:
- (1,0,0) = +x direction (default)
- (0,0,1) = +z direction
- Any unit vector allowed

### Example: Deep Penetration Shielding

```
c Neutron source at origin, detector at x=500 (deep penetration)
c
MODE  N
c
c Exponential transform in all shield cells
EXT:N  0.75  2  3  4
c      ^^p value  ^^shield cells
c
c Preferred direction toward detector
VECT  1  0  0
c     ^^+x direction
c
c Source
SDEF  POS=0 0 0  ERG=14.1  VEC=1 0 0  DIR=D1
SI1  -1  0.9999              $ Cone toward +x
SP1   0  1
c
c CRITICAL: Use weight window with EXT
WWG  5  0  1.0
c
F5:N  500 0 0  0.5           $ Detector
NPS  1e6
```

### EXT Parameter Selection

**Underbiasing (p → 0):**
- Few particles penetrate
- Those that do have weight ≈ 1
- Low scoring efficiency, large variance from few scores

**Optimal (p ≈ 0.5-0.9):**
- Good penetration rate
- Moderate weight variation
- Best FOM

**Overbiasing (p → 1):**
- Many particles penetrate
- Large weight variation (some extremely high weight)
- High variance from weight dispersion

**Guidelines:**
- Neutron penetration (concrete/earth): p = 0.6-0.8
- Photon penetration (high-Z): p = 0.8-0.95
- Highly absorbing media: higher p values
- Scattering media: lower p values

### EXT Best Practices

1. **ALWAYS use weight windows with EXT**
   - EXT causes large weight variation
   - WW prevents pathological high-weight particles
   - MCNP warns if EXT without WW

2. **One-dimensional geometry preferred**
   - EXT works best for directional streaming
   - Multi-dimensional problems more complex

3. **Highly absorbing media**
   - EXT most effective
   - Can set p = Σ_a/Σ_t for implicit capture along flight path

4. **Test parameter values**
   - Start with p = 0.7
   - Increase if penetration still poor
   - Decrease if weight variation excessive

5. **Monitor weight statistics**
   - Check max/min weight ratio in output
   - Ratio >1000 indicates problems
   - Adjust WWP parameters to widen window

---

## Forced Collisions (FCL)

### Theory (§2.7.2.15)

Forced collisions increase sampling in specified cells by splitting particles into collided and uncollided components.

**Process:**
1. **Uncollided particle:** Reaches cell boundary with weight `w₀·exp(-Σ_t·d)`
2. **Collided particle:** Forced to collide within cell with weight `w₀·(1-exp(-Σ_t·d))`

Both particles are tracked, preserving expected weight.

**Collision Site Sampling:**
Conditional on collision occurring within distance d to boundary:
```
s = -ln(1 - ξ·(1 - exp(-Σ_t·d))) / Σ_t
```

### FCL Card Syntax

```
FCL:p  f₁  f₂  f₃  ...  fₙ
```

**Parameters:**
- `p` = Particle type
- `fᵢ` = Forced collision parameter for cell i
  - `0` = No forced collisions
  - `+value` = Force collisions, subsequent collisions also forced
  - `-value` = Force collisions, subsequent collisions normal
  - `value` = Fraction of time to create forced collision (0 < value ≤ 1)

**Typical Values:**
- `1` = Always force collision (100%)
- `0.5` = Force collision 50% of time (reduces overhead)
- `0.1` = Force collision 10% of time (very thin cells)

### When to Use FCL

**Ideal Applications:**
- **Thin cells** (<0.1 mean free path thick)
  - Air gaps in shields
  - Detector foils
  - Thin absorbers

- **Low-density regions**
  - Streaming paths through voids
  - Duct penetrations
  - Very low probability of collision

- **Reaction rate tallies**
  - Need collisions for F4 or F6 tallies
  - Thin activation foils

**Not Recommended:**
- Thick cells (>1 MFP) → no benefit
- Regions already well-sampled
- Combined with DXTRAN in same cell

### Example: Thin Detector Foil

```
c Gold foil detector (very thin, 0.001 cm)
c
c Cell Cards
10  10  -19.3  -10  IMP:N=1     $ Gold foil (0.001 cm thick)
c
c Data Cards
MODE  N
c
c Force collisions in thin foil
FCL:N  0  0  0  0  0  0  0  0  0  1
c                                 ^^cell 10
c
c Reaction rate tally in foil
F4:N  10
FM4  -1  10  (197079.80c -2)    $ 197Au(n,γ) reaction
c
c Weight window to control FCL particle weights
WWP:N  5  3  5  0  -1
WWG  4  0  1.0                   $ Generate WW from F4
c
NPS  1e6
```

### FCL Options (Positive vs. Negative)

**Positive Entry (+1):**
- First forced collision created
- Subsequent collisions in same cell also forced
- Particle may undergo multiple forced collisions
- Use when: Cell is path-length (multiple collisions expected)

**Negative Entry (-1):**
- First forced collision created
- Subsequent collisions sampled normally
- Only one forced collision per cell entry
- Use when: Cell is very thin (only one collision likely)

### FCL with Weight Windows

**Critical Interaction:**
- FCL creates particles with reduced weight
- Weight may fall below WWN lower bound
- MCNP has special handling:
  - WW game NOT played on surface entering FCL cell
  - After forced collision: WW or weight cutoff applied

**WW Setup for FCL:**
Two strategies:

**Strategy 1 (Negative FCL entry):**
```
FCL:N  0  0  -1        $ Cell 3, negative entry
WWN:N  1  1  0.01      $ Low bound in cell 3 for FCL particle weight
```
Set WWN to expected FCL particle weight or zero (turn off WW).

**Strategy 2 (Positive FCL entry):**
```
FCL:N  0  0  +1        $ Cell 3, positive entry
WWN:N  1  1  1         $ Normal bound in cell 3
```
Set WWN to bracket weights entering cell (subsequent FC will adjust).

---

## Energy Splitting and Roulette (ESPLT)

### Theory (§2.7.2.8)

Energy-dependent splitting/roulette controls particle population based on energy, independent of spatial cell.

**Applications:**
- Build up thermal neutron population (fission tallies)
- Build up low-energy photon population (fluorescence)
- Reduce fast particle population (if unimportant)

### ESPLT Card Syntax

```
ESPLT:p  E_split  N_split  E_roul  P_survive  I_cell₁  I_cell₂  ...
```

**Parameters:**
- `p` = Particle type
- `E_split` = Energy below which to split
- `N_split` = Split ratio (creates N particles of weight w/N)
- `E_roul` = Energy below which to play roulette
- `P_survive` = Survival probability
- `I_cellᵢ` = Cells where ESPLT active

**Example - Thermal Neutron Buildup:**
```
c Split neutrons falling below 0.1 eV into 3 particles
ESPLT:N  1e-7  3  0  0  1  2  3  4
c        ^^E_split ^^N_split ^^no roulette
c
c F4 tally for thermal fission in U-235
F4:N  1                        $ Fuel cell
FM4  -1  1  (92235.80c -6)     $ 235U fission
E4   0  1e-7  20               $ Thermal bin
```

**Example - Low-energy Photon Roulette:**
```
c Roulette photons below 10 keV with 10% survival
ESPLT:P  0  0  0.01  0.1  1  2  3  4
c        ^^no split ^^E_roul  ^^P_survive
```

### Energy Splitting/Roulette vs. Weight Windows

**Prefer Weight Windows When:**
- Importance varies with space AND energy
- Complex phase space
- Automatic generation desired

**ESPLT Advantages:**
- Simple to specify
- Energy-only dependence
- No mesh/WWN cards needed

---

## Time Splitting and Roulette (TSPLT)

### Theory (§2.7.2.10)

Time-dependent splitting/roulette similar to ESPLT, but based on particle time.

**Note:** Particle time can only increase (unlike energy which can up-scatter).

### TSPLT Card Syntax

```
TSPLT:p  T_split  N_split  T_roul  P_survive  I_cell₁  I_cell₂  ...
```

Parameters identical to ESPLT, but for time instead of energy.

**Example - Late-time Buildup:**
```
c Split particles after t = 1 μs into 2 particles
TSPLT:N  1e-6  2  0  0  1  2  3  4
c
c Tally late-time dose
F4:N  5
T4   0  1e-6  2e-6  5e-6  1e-5  1e-4
```

---

## Weight Cutoff Advanced Usage

### Theory (§2.7.2.11)

Weight cutoff plays Russian roulette when particle weight drops below threshold.

**Cell-dependent Cutoff:**
```
w_cutoff,j = (I_source / I_j) · w_c,2
w_survive,j = (I_source / I_j) · w_c,1
```

Where `I_j` = importance of cell j.

### CUT Card Syntax

```
CUT:p  w_c,1  w_c,2  -E_cutoff  -T_cutoff  I_cell₁  I_cell₂  ...
```

**Parameters:**
- `w_c,1` = Survival weight (if roulette won)
- `w_c,2` = Weight below which to play roulette
- `-E_cutoff` = Energy cutoff (optional, negative value)
- `-T_cutoff` = Time cutoff (optional, negative value)
- `I_cellᵢ` = Cells (optional, default = all)

**Interaction with IMP:**
- Weight cutoffs scale with cell importance
- High importance → lower cutoff threshold
- Automatic adjustment for geometry splitting

**Example:**
```
c Weight cutoff with cell importance
IMP:N  1  2  4  8  0
c
CUT:N  0.25  0.1
c      ^^survive weight ^^cutoff threshold
c
c Effective cutoffs by cell:
c   Cell 1 (IMP=1): cutoff = 0.1/1 = 0.1,   survive = 0.25/1 = 0.25
c   Cell 2 (IMP=2): cutoff = 0.1/2 = 0.05,  survive = 0.25/2 = 0.125
c   Cell 3 (IMP=4): cutoff = 0.1/4 = 0.025, survive = 0.25/4 = 0.0625
```

---

## Implicit Capture

### Theory (§2.7.2.14)

Implicit capture (survival biasing) avoids sampling absorption—particle always survives collision with weight reduced by non-absorption probability.

**Analog:**
- Sample absorption with probability σ_a/σ_t
- If absorbed: weight = 0, history ends
- If survives: weight unchanged

**Implicit Capture:**
- Particle always survives
- Weight multiplied by (1 - σ_a/σ_t) = σ_s/σ_t

**Activation:**
Implicit capture is automatically ON when `w_c,1 > 0` on CUT card (except detailed photon physics).

**Advantages:**
1. Particles reaching detector are not absorbed just before tally
2. Variance reduced (no 0/W sampling, use expected weight)

**Disadvantages:**
1. Weight fluctuation introduced
2. Time per history increased

**Best Practice:**
Use with weight cutoff to remove very low-weight particles.

---

## Source Variable Biasing

### Overview (§2.7.2.16)

Bias source sampling to start more particles in important regions/directions/energies.

**Methods:**
1. Explicit sampling frequencies (SB card)
2. Built-in prescriptions (directional, spatial)

### Directional Biasing

**Exponential Distribution:**
```
SDEF  POS=0 0 0  ERG=14.1  DIR=D1
SI1  -1  1                  $ Cosine bins
SP1   0  1                  $ Isotropic (analog)
SB1   0  C  K               $ Exponential biasing
c        ^^K parameter
```

**K Values:**
- K = 0.01: Almost isotropic
- K = 1: Moderate biasing (half in 64° cone)
- K = 3.5: Strong biasing (half in 23° cone)

**Cone Biasing:**
```
SDEF  POS=0 0 0  ERG=14.1  DIR=D1
SI1  H  -1  0.8  1          $ Histogram: (-1 to 0.8), (0.8 to 1)
SP1     0.1  0.9            $ Analog: 90% isotropic, 10% in cone
SB1     0.5  0.5            $ Biased: 50% each bin
```

### Energy Biasing

**Standard Analytic Functions:**
```
SDEF  ERG=D1
SI1  L  1e-7  0.1  1  14    $ Energy bins
SP1    0.1  0.2  0.3  0.4   $ Analog distribution
SB1    0.25  0.25  0.25  0.25  $ Uniform biasing
```

---

## Combining Advanced Techniques

### EXT + WWG (Deep Penetration)

**Best Practices:**
1. Set up EXT first (choose p value)
2. Run WWG with EXT active
3. Iterate WWG 2-3 times
4. Production: EXT + converged WW

**Synergy:**
- EXT biases direction
- WWG controls weights
- Together: 100-1000× FOM improvement

### FCL + WWG (Thin Regions)

**Best Practices:**
1. Identify thin cells (<0.1 MFP)
2. Set FCL for those cells
3. Run WWG with FCL active
4. Set WWN to expected FCL weights

### ESPLT + WWG (Energy-dependent)

**Best Practices:**
1. Set up ESPLT for energy range
2. Use energy-dependent WW (WWE)
3. WWG generates energy-dependent bounds
4. Iterate

---

## References

**MCNP6 Theory Manual:**
- §2.7.2.13: Exponential Transform
- §2.7.2.14: Implicit Capture
- §2.7.2.15: Forced Collisions
- §2.7.2.8: Energy Splitting/Roulette
- §2.7.2.10: Time Splitting/Roulette
- §2.7.2.11: Weight Cutoff
- §2.7.2.16: Source Biasing

**MCNP6 User Manual:**
- Chapter 5.12: Variance Reduction Cards

**See Also:**
- `card_specifications.md` - EXT, FCL, ESPLT, TSPLT, CUT syntax
- `advanced_vr_theory.md` - VR strategy and combining methods
- `wwg_iteration_guide.md` - WWG workflows with advanced techniques
