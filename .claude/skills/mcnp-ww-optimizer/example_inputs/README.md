# Weight Window Optimization Examples

## Overview

This directory contains examples demonstrating weight window optimization workflows using WWG (weight window generator) iteration.

**Key Concept**: Weight windows are iteratively refined through multiple generations, each improving the importance function based on particle behavior in the previous run.

---

## Examples

### 01_wwg_iteration_1_generate.i

**Purpose:** Initial weight window generation from analog or poor-statistics run.

**Workflow Step:** Iteration 1 - Generate first WWG estimate

**Key Features:**
- WWG card targets F5 point detector
- MESH card defines spatial resolution for importance
- WWGE card defines energy structure
- Moderate NPS (~100k) for initial generation

**Expected Output:**
- wwout file containing mesh-based weight windows
- FOM typically 5-20× better than analog

**Usage:**
```bash
mcnp6 i=01_wwg_iteration_1_generate.i o=iter1.out
# Creates wwout file
```

---

### 02_wwg_iteration_2_refine.i

**Purpose:** Refine weight windows using previous wwout

**Workflow Step:** Iteration 2 - Improve WWG with better sampling

**Key Features:**
- Same MESH and WWGE (must match iteration 1!)
- WWP:N J J J 0 -1 reads previous wwout
- WWG card still present (generates improved wwout)
- Increased NPS (~200k) for better statistics

**Expected Output:**
- Improved wwout file
- FOM typically 2-5× better than iteration 1
- More uniform importance function

**Usage:**
```bash
# Requires wwout from iteration 1
mcnp6 i=02_wwg_iteration_2_refine.i o=iter2.out
# Creates improved wwout
```

---

### 03_wwg_production.i

**Purpose:** Production run with converged weight windows

**Workflow Step:** Final production - high statistics with converged WW

**Key Features:**
- Same MESH and WWGE (must match!)
- WWP:N J J J 0 -1 reads converged wwout
- NO WWG card (just use WW, don't regenerate)
- High NPS (~10M+) for final results

**Expected Output:**
- Final tally results with low relative error (<5%)
- Consistent FOM (should match iteration 2-3)
- All 10 statistical checks pass

**Usage:**
```bash
# Requires converged wwout from iteration 2-3
mcnp6 i=03_wwg_production.i o=production.out
```

---

## Iteration Workflow

### Complete 3-Iteration Example

**Iteration 1: Generate Initial WW**
```bash
mcnp6 i=01_wwg_iteration_1_generate.i o=iter1.out
# Result: wwout, FOM ≈ 1000 (baseline: 100)
# Improvement: 10× over analog
```

**Iteration 2: Refine WW**
```bash
# Use wwout from iteration 1
mcnp6 i=02_wwg_iteration_2_refine.i o=iter2.out
# Result: improved wwout, FOM ≈ 3000
# Improvement: 3× over iteration 1, 30× over analog
```

**Iteration 3: Verify Convergence (optional)**
```bash
# Check if FOM still improving
mcnp6 i=02_wwg_iteration_2_refine.i o=iter3.out
# Result: wwout, FOM ≈ 3200
# Improvement: 1.07× over iteration 2 → CONVERGED (<20% change)
```

**Production: High Statistics**
```bash
# Use converged wwout, remove WWG card, increase NPS
mcnp6 i=03_wwg_production.i o=production.out
# Result: FOM ≈ 3200, R < 0.05 (5%)
```

---

## Convergence Criteria

**When to stop iterating:**

1. **FOM change <20%** between iterations
   ```
   (FOM_n - FOM_n-1) / FOM_n-1 < 0.20
   ```

2. **Relative error achieves target** (typically R < 0.10)

3. **Weight windows stable** (WWN values change <10% on average)

4. **All 10 statistical checks pass**

**Typical convergence:** 2-5 iterations

---

## Mesh and Energy Structure

**MESH Definition (must be identical across all iterations):**
```
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-100 -100 -100
      IMESH=100  IINTS=20      $ 5 cm bins
      JMESH=100  JINTS=20
      KMESH=100  KINTS=20
```

**Energy Structure (must be identical):**
```
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
```

**Important:** If MESH or WWGE change between iterations, weight windows are invalid!

---

## Troubleshooting

### FOM Decreasing Between Iterations

**Problem:** FOM_iter2 < FOM_iter1

**Causes:**
1. MESH or WWGE changed (not identical)
2. Statistical noise in iteration 1
3. Tally region poorly sampled

**Solutions:**
1. Verify MESH and WWGE identical
2. Increase NPS in iteration 1
3. Refine mesh near tally

### WW Values Too High/Low

**Problem:** Weight min/max ratio >1000

**Cause:** Importance varies too much across phase space

**Solution:** Adjust WWP parameters:
```
WWP:N  10  3  5  0  -1    $ Widen window (wupn=10 instead of 5)
```

### Particles Not Reaching Tally

**Problem:** Zero scores despite WW

**Cause:** Weight windows too aggressive (overbiasing)

**Solution:**
1. Coarsen mesh (fewer IINTS)
2. Increase source importance (WNORM)
3. Start with cell importance first

---

## Advanced Usage

### Combining with Exponential Transform

**For deep penetration (>15 MFP):**

```
c Iteration 1
EXT:N  0.75  2  3  4  5        $ Exponential transform
VECT  1  0  0                  $ Toward detector
WWG  5  0  1.0                 $ Generate WW with EXT active
```

**Critical:** Run EXT + WWG together in all iterations!

### Cylindrical Mesh for Cylindrical Problems

```
MESH  GEOM=CYL  REF=0 0 0  AXS=0 0 1  VEC=1 0 0
      IMESH=50  100  150  200  IINTS=10  10  10  10
      JMESH=-100  0  100      JINTS=10  10
      KMESH=360                KINTS=12
```

---

## Integration

**These examples are templates - adapt to your problem:**

1. **Replace geometry:** Use your cell/surface definitions
2. **Replace tally:** Use your detector location/type
3. **Adjust mesh:** Match your geometry scale
4. **Adjust energy bins:** Match your problem physics
5. **Keep workflow:** Iteration structure works universally

**See Also:**
- `../mcnp-variance-reducer/example_inputs/` - Full VR problem examples
- `../mcnp-variance-reducer/advanced_vr_theory.md` - WWG algorithm details
- `../mcnp-variance-reducer/mesh_based_ww.md` - Mesh generation comprehensive guide

---

## References

**Parent Skill:**
- `../mcnp-variance-reducer/` - Comprehensive variance reduction skill
  - `advanced_vr_theory.md` - WWG algorithm, convergence theory
  - `mesh_based_ww.md` - MESH card details, resolution guidelines
  - `wwg_iteration_guide.md` - Step-by-step iteration procedures

**MCNP6 Manual:**
- Chapter 5.12.2: WWN Card (weight window lower bounds)
- Chapter 5.12.3: WWE Card (energy-dependent bounds)
- Chapter 5.12.4: WWP Card (parameters)
- Chapter 5.12.5: WWG Card (generator)
- Chapter 5.11: MESH Card (spatial mesh)
- Chapter 2.7.2.12: Weight Window Theory
