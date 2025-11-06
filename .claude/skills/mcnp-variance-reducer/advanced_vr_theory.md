# Advanced Variance Reduction Theory

## Overview

This reference provides advanced theoretical concepts for variance reduction optimization, including the weight window generator algorithm, VR strategy development, and troubleshooting pathological cases.

**Prerequisites:** Read `variance_reduction_theory.md` for fundamental concepts (FOM, splitting/RR).

---

## VR Strategy Development

### General Principles (§2.7.1.4)

Successful variance reduction requires understanding both the **physical problem** and the **VR techniques** available.

**Key Questions to Answer:**
1. **Why are tallying particles special?**
   - Specific scattering directions?
   - Rare reactions or energy ranges?
   - Geometric pathways to detector?

2. **What makes sampling difficult?**
   - Deep penetration (>10 MFP)?
   - Angular dependence?
   - Energy-dependent importance?

3. **Which VR method addresses this challenge?**
   - Geometry splitting → spatial importance
   - Weight windows → phase space importance
   - DXTRAN → deterministic transport to small volumes
   - Exponential transform → directional biasing

### Strategy Workflow

**Step 1: Understand the Physics**
- Run short analog calculation
- Identify particle transport paths to detector
- Determine what fraction of source particles tally
- Note energy/direction/position of tallying particles

**Step 2: Select VR Techniques**
- Match technique to physical challenge
- Start conservative (underbiasing better than overbiasing)
- Test one method at a time before combining

**Step 3: Supply Parameters**
- Use analog run data for initial guesses
- Conservative biasing initially (e.g., IMP ratio = 2-4 vs. 10-100)
- Err on side of too little biasing

**Step 4: Monitor Short Calculation**
- Check FOM table for erratic behavior
- Verify VR improves sampling of tallying particles
- Ensure methods work cooperatively
- Look for obviously ridiculous results

**Step 5: Iterate and Refine**
- Adjust parameters based on output
- Use WWG for automatic importance function
- Continue until sampling no longer improves
- Typically 2-5 iterations for WWG convergence

---

## Erratic Error Estimates (§2.7.1.5)

### Causes

**High-weight particles** in **important regions** that are **poorly sampled**.

**Definition:** A high-weight particle carries a nontrivial fraction of all weight that has tallied from that region across all histories.

**Common Examples:**
1. **Point detector:** Particle collides very close to detector
   - Few previous collisions that close → high relative contribution
   - Causes jump in relative error estimate for that history

2. **Coherent photon scattering:** Strongly peaked angular distribution toward detector
   - High-weight contribution when coherent scatter occurs

3. **Rare pathway:** Only a few particles reach important region
   - Each particle carries large weight → large variance

### Diagnosis

**Symptoms:**
- FOM not constant (increases or decreases erratically)
- Relative error estimate jumps between histories
- Statistical checks fail (especially checks 3-10)
- Large disparity in tally contributions across histories

**Analysis:**
- Examine Tally Fluctuation Chart (TFC) table
- Check 10 statistical tests (§2.6.9.2.3)
- Identify histories causing large tally contributions
- Use event logs (PTRAC) to track high-weight particles

### Solutions

**Primary Strategy: Sample Important Regions Better**

1. **Increase particle population in important regions**
   - Use splitting (IMP or weight windows)
   - Direct particles toward detector (DXTRAN, source biasing)
   - Reduce Russian roulette in critical regions

2. **Minimize weight fluctuations**
   - Use weight windows to bound particle weights
   - Avoid large importance ratio jumps (>4× between cells)
   - Balance splitting with weight control

3. **Never discard high-weight particles!**
   - Their large contribution indicates importance
   - Instead, modify VR to sample more of them
   - Adjust parameters to reduce their weight (split earlier)

**Example Fix:**
```
Problem: High-weight particle near point detector causes erratic error
Solution 1: Weight window around detector (split particles before arrival)
Solution 2: DXTRAN sphere → creates many low-weight particles reaching detector
Solution 3: Reduce detector contribution cutoff → sample more collisions near detector
```

---

## Avoiding Overbiasing (§2.7.1.6)

### The Danger

**Overbiasing** heavily suppresses some random walks, potentially missing important physics.

**Risk:** For a given computer time, some walks are sampled **much less frequently** than in analog → might never be sampled if not enough particles run.

### Example: Cell 23 Importance Too Low

**Scenario:**
- Analog: 1 in 1 million particles enters Cell 23
- Typical calculation: 100,000 particles
- Analog probability: ~0 particles in Cell 23 per run
- True answer: 10% should come from Cell 23

**Overbiased Case:**
- User sets importance such that Cell 23 has very low IMP
- Still ~0 particles enter Cell 23
- User gets 90% of true tally with 1% error
- **No indication anything is wrong!**

**Properly Biased Case:**
- Importance set such that 1 in 10,000 particles enters Cell 23
- ~10 particles enter Cell 23 in 100,000 particle run
- Tally severely affected by high-weight particles from Cell 23
- Tally closer to truth, larger/erratic error → **indicates problem exists**

### Key Principle

**"Always sample all regions enough to be certain they are unimportant."**

Following 10 tracks into Cell 23:
- Costs little computer time
- Ensures estimated error cannot be misleadingly low
- Reveals true importance of the region

### Conservative Biasing Guidelines

1. **Start with modest importance ratios** (2-4× between cells, not 100×)
2. **Ensure all cells are sampled** in short test runs
3. **Check weight balance table** in output (weight created vs. lost)
4. **Monitor FOM constantly** as simulation progresses
5. **Run convergence tests** with different random seeds
6. **Compare to analog** for simple benchmarks

---

## Weight Window Generator Algorithm (§2.7.2.12.2)

### Theory (§2.7.2.12.3)

**Importance Definition:**
The importance of a particle at point P in phase space equals the **expected score a unit weight particle will generate**.

**Cell Importance Estimation:**
```
I_cell = (Total score from particles entering cell) / (Total weight entering cell)
```

**Bookkeeping for WWG:**
```
For each phase space cell i:
  - Track: weight entering cell (W_in,i)
  - Track: tally contribution after entering cell (T_i)
  - Estimate: I_i = T_i / W_in,i
```

**Weight Window Assignment:**
After estimating importance, MCNP assigns weight windows **inversely proportional** to importance:
```
WWN_i = C / I_i
```
where C is a normalization constant (set on WWG card).

**Goal:** Ensure `weight × importance ≈ constant` throughout phase space.
- High importance region → low weight bound → many particles, low weight
- Low importance region → high weight bound → few particles, high weight

### Limitations (§2.7.2.12.4)

**1. Statistical Nature**

Weight windows are **estimates** subject to statistical error.

**Problem:** Unless phase space region is sampled adequately:
- No importance estimate OR
- Unreliable importance estimate

**Solution:** Need crude initial importance function to get **any** tallies.

**2. Convergence Requirements**

- First set of generated WW → used in subsequent calculation
- Generates better WW → iterate
- Typically need **2-5 iterations** for convergence
- Each iteration improves sampling → better importance estimates

**3. Bad Importance Estimates**

**Causes:**
- Insufficient sampling of phase space region
- Statistical flukes in low-probability regions
- Phase space too finely subdivided

**Detection:**
- MCNP flags WW more than 4× different from adjacent cells
- User must scrutinize flagged regions
- Manual adjustment often necessary

**Example:**
```
Adjacent cell lower bounds: 0.5, 0.3, 0.9, 0.05, 0.03, 0.02
                                       ^^^
Problem: 0.9 is 18× larger than 0.05 (adjacent)
Fix: Change 0.9 to ~0.1 to fit pattern
```

**4. Phase Space Subdivision**

**Too coarse:**
- Single WW bound represents region with varying importance
- No single bound is optimal
- Solution: Subdivide geometry or use importance mesh

**Too fine:**
- Individual cells not sampled adequately
- Statistical noise dominates
- Solution: Coarsen mesh or combine cells

**Mesh-Based WW:**
- Superimposed mesh grid (rectangular or cylindrical)
- Independent of MCNP cell structure
- Can refine mesh in important regions only
- Warning: Resist temptation to create mesh cells too small

---

## Convergence Criteria

### WWG Iteration Convergence

**When to stop iterating:**

**Quantitative Criteria:**
1. **FOM improvement <20%** between iterations
   ```
   (FOM_n - FOM_n-1) / FOM_n-1 < 0.20
   ```

2. **WW values change <10%** on average
   ```
   Mean|(WWN_n - WWN_n-1) / WWN_n-1| < 0.10
   ```

3. **Tally relative error <10%** (target precision achieved)

**Qualitative Criteria:**
1. **FOM stable** across iterations (roughly constant)
2. **No large WW adjustments** flagged by MCNP
3. **All 10 statistical checks pass**
4. **Weight statistics reasonable** (min/max weight ratio <100)

### Typical Convergence Pattern

**Iteration 1 (Crude WW):**
- FOM = 10× analog (moderate improvement)
- Some regions still poorly sampled
- Many flagged WW adjustments

**Iteration 2:**
- FOM = 30× analog (3× improvement over iter 1)
- Better sampling across phase space
- Fewer flagged adjustments

**Iteration 3:**
- FOM = 35× analog (16% improvement → converging)
- Minimal flagged adjustments
- Statistical checks passing

**Iteration 4:**
- FOM = 36× analog (3% improvement → converged!)
- Ready for production run

**Production Run:**
- Use converged WW (no WWG card)
- High statistics (10-100× more particles)
- Final results with low uncertainty

---

## Combining Multiple VR Methods

### Compatibility Matrix

| Primary Method | Compatible With | Conflicts/Issues |
|----------------|-----------------|------------------|
| Weight Windows | IMP, EXT, FCL, DXTRAN | Can control weight fluctuations from other methods |
| Cell Importance | WWN (if WW turned off in cells), FCL | Weight windows override IMP |
| WWG | Any method | Estimates importance regardless of other VR |
| Exponential Transform | WWN | MCNP warns if EXT without WW (unreliable) |
| DXTRAN | WWN | Weight windows control DXTRAN particle weights |
| Forced Collisions | WWN, IMP | WW interacts with FCL weight adjustment |

### Best Practices for Combining

**1. Test Individually First**
- Implement each VR method alone
- Verify each works correctly
- Measure FOM improvement separately
- Then combine methods

**2. Weight Windows as Coordinator**
- Use WW to control weight fluctuations from other methods
- Prevents high-weight particles from biasing (EXT, FCL, source biasing)
- Essential for EXT (exponential transform)

**3. Common Combinations**

**WWG + DXTRAN (far detector):**
```
Step 1: Set up DXTRAN sphere around detector
Step 2: Run WWG targeting detector tally
Step 3: Use generated WW in production run with DXTRAN
Effect: DXTRAN creates particles on sphere, WW controls their weights
```

**WWG + EXT (deep penetration):**
```
Step 1: Set up exponential transform (p = 0.7-0.9 for penetration)
Step 2: Add weight window (WWG generated or manual)
Step 3: Iterate WWG with EXT active
Effect: EXT biases direction, WW prevents high-weight particle pathology
```

**WWG + FCL (thin regions):**
```
Step 1: Force collisions in thin cells (air gaps, detectors)
Step 2: Generate WW with FCL active
Step 3: Set WW bounds to bracket FCL particle weights
Effect: FCL ensures collisions happen, WW controls resulting weights
```

### Warning Signs of Incompatibility

- FOM decreases when combining methods
- Statistical checks fail
- Extremely large weight ratios (>1000)
- Excessive splitting or rouletting (>90% particles killed)
- Weight balance table shows large imbalance

**Solution:** Remove one method, test independently, then reintroduce carefully.

---

## References

**MCNP6 Theory Manual:**
- §2.7.1.4: Strategy for VR technique selection
- §2.7.1.5: Erratic error estimates and high-weight particles
- §2.7.1.6: Dangers of overbiasing
- §2.7.2.12.2: Weight window generator algorithm
- §2.7.2.12.3: WWG theory and importance estimation
- §2.7.2.12.4: WWG limitations and convergence

**See Also:**
- `variance_reduction_theory.md` - Fundamental concepts
- `wwg_iteration_guide.md` - Step-by-step WWG workflow
- `error_catalog.md` - Common VR problems and solutions
- `mesh_based_ww.md` - Mesh-based weight window generation
