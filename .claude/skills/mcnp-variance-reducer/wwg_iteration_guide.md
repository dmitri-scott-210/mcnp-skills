# WWG Iteration Guide - Weight Window Optimization Workflow

## Overview

This guide provides step-by-step procedures for iterative weight window generation and optimization using MCNP's WWG (Weight Window Generator) capability.

---

## Basic Two-Stage Process

### Stage 1: Generate Weight Windows

**Purpose:** Create initial wwout file with weight window values

**Input File (input_wwg.i):**
```
Point Detector Shielding with WWG Generation
c
c =============================
c Cell Cards
c =============================
c
1  1  -1.0    -1         IMP:N=1     $ Source region
2  2  -7.8    1 -2       IMP:N=1     $ Shield 1
3  3  -11.3   2 -3       IMP:N=1     $ Shield 2
4  0         3 -4       IMP:N=1     $ Detector region
999  0       4          IMP:N=0     $ Graveyard

c =============================
c Surface Cards
c =============================
c
1  SO  10                              $ Source sphere
2  SO  30                              $ Shield 1 outer
3  SO  50                              $ Shield 2 outer
4  SO  60                              $ Outer boundary

c =============================
c Data Cards
c =============================
c
MODE  N
c
c --- Spatial mesh for importance ---
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-60 -60 -60
      IMESH=60  IINTS=12
      JMESH=60  JINTS=12
      KMESH=60  KINTS=12
c
c --- Energy bins for weight windows ---
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c --- Point detector ---
F5:N  55 0 0  0.5
c
c --- Generate weight windows from F5 tally ---
WWG  5  0  1.0
c    ^tally ^mesh ^target
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- Moderate statistics for WWG generation ---
NPS  1e5
```

**Run Command:**
```bash
mcnp6 inp=input_wwg.i outp=wwg_stage1.o runtpe=wwg_stage1.r
```

**Output:**
- `wwout` file (binary weight window file)
- `wwg_stage1.o` (check FOM, relative error)

**Validation:**
- Check detector tally relative error <30%
- Verify wwout file size >0 bytes
- Note baseline FOM value

---

### Stage 2: Production Run with Weight Windows

**Purpose:** Use generated weight windows for high-statistics run

**Input File (input_prod.i):**
```
Point Detector Shielding with Weight Windows
c
c =============================
c Cell Cards
c =============================
c
[... same geometry as Stage 1 ...]

c =============================
c Data Cards
c =============================
c
MODE  N
c
c --- Read weight windows from wwout file ---
WWP:N  J  J  J  0  -1
c      ^default params  ^read wwout
c
c --- Energy bins (must match WWG) ---
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c --- Point detector ---
F5:N  55 0 0  0.5
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- High statistics for production ---
NPS  1e7
```

**Run Command:**
```bash
mcnp6 inp=input_prod.i outp=prod_stage2.o runtpe=prod_stage2.r
```

**Validation:**
- FOM should be much higher than Stage 1
- Relative error <10% (target <5%)
- All 10 statistical tests PASS
- FOM remains constant throughout run

---

## Iterative Optimization (3-5 Iterations)

### Iteration Workflow

**Goal:** Progressively improve weight windows until FOM converges

### Iteration 1: Initial WWG

**Input:** Analog simulation or simple cell importance

```
c --- Iteration 1: Generate initial WW ---
WWG  5  0  1.0
NPS  1e5
```

**Expected Result:**
- FOM_1 ≈ 10-50× analog FOM
- Relative error ≈ 20-30%

**Output:**
- `wwout` (initial weight windows)

---

### Iteration 2: Use WW, Regenerate

**Input:** Use previous wwout, generate improved WW

```
c --- Iteration 2: Use WW and regenerate ---
WWP:N  J  J  J  0  -1           $ Use previous wwout
WWG  5  0  1.0                  $ Generate improved wwout
NPS  2e5                        $ More statistics
```

**Expected Result:**
- FOM_2 ≈ 2-5× FOM_1
- Relative error ≈ 10-20%

**Output:**
- Improved `wwout` (overwrites previous)

**Monitoring:**
```bash
# Extract FOM from output
grep "tally.*5" prod_iter2.o | grep "fom"
```

---

### Iteration 3: Continue Iteration

**Input:** Continue using and regenerating

```
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  5e5                        $ Even more statistics
```

**Expected Result:**
- FOM_3 ≈ 1.2-2× FOM_2
- Relative error ≈ 5-10%

**Convergence Check:**
- If (FOM_3 - FOM_2) / FOM_2 < 0.20 → Converging
- If relative error <10% → Good enough
- Continue if need better statistics

---

### Iteration 4: Final Convergence

**Input:**
```
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  1e6
```

**Expected Result:**
- FOM_4 ≈ 1.05-1.15× FOM_3
- Relative error <5%
- **Converged:** FOM change <20%

**Decision:**
- ✅ If converged → Proceed to final production run
- ⏸️ If not converged → Continue iteration

---

### Final Production Run (No WWG)

**Input:** Use final wwout, remove WWG card

```
c --- Final production: Use optimized WW ---
WWP:N  J  J  J  0  -1           $ Use final wwout
c No WWG card - just use WW
c
NPS  5e7                        $ Very high statistics
```

**Purpose:**
- Achieve target relative error <1%
- Maximize computational efficiency
- No overhead from WWG generation

---

## Convergence Monitoring

### FOM Tracking Table

Create tracking table to monitor convergence:

```
Iteration | NPS    | Time (min) | FOM      | Rel. Err | FOM Ratio
----------|--------|------------|----------|----------|----------
Analog    | 1e6    | 100        | 100      | 0.10     | 1.0×
Iter 1    | 1e5    | 10         | 1,000    | 0.30     | 10×
Iter 2    | 2e5    | 20         | 3,000    | 0.18     | 30×
Iter 3    | 5e5    | 50         | 4,500    | 0.09     | 45×
Iter 4    | 1e6    | 100        | 5,000    | 0.05     | 50×  ← Converged
Final     | 5e7    | 500        | 5,100    | 0.01     | 51×
```

### Convergence Criteria

**Primary:**
- FOM improvement <20% between iterations
- Example: (FOM_n - FOM_{n-1}) / FOM_{n-1} < 0.20

**Secondary:**
- Relative error reaches target (<5% good, <10% acceptable)
- Weight window values stable (extract from wwout comparison)

**Typical:** 2-5 iterations needed for convergence

---

## Command-Line Workflow

### Bash Script Example

```bash
#!/bin/bash
# WWG iteration automation

# Iteration 1: Generate initial WW
echo "=== Iteration 1: Generate initial WW ==="
mcnp6 inp=input_iter1.i outp=out_iter1.o runtpe=run_iter1.r
cp wwout wwout_iter1  # Archive

# Iteration 2: Use WW, regenerate
echo "=== Iteration 2: Use and regenerate ==="
mcnp6 inp=input_iter2.i outp=out_iter2.o runtpe=run_iter2.r
cp wwout wwout_iter2

# Iteration 3: Continue
echo "=== Iteration 3: Continue iteration ==="
mcnp6 inp=input_iter3.i outp=out_iter3.o runtpe=run_iter3.r
cp wwout wwout_iter3

# Check convergence
python3 check_fom_convergence.py out_iter*.o

# If converged, run final production
echo "=== Final production run ==="
mcnp6 inp=input_final.i outp=out_final.o runtpe=run_final.r
```

### FOM Extraction Script

```bash
#!/bin/bash
# Extract FOM values from output files

for file in out_iter*.o; do
    echo "=== $file ==="
    grep "tally.*5" $file | tail -1 | awk '{print "FOM:", $NF}'
done
```

---

## WWG Target Parameter Tuning

### Effect of Target Value

**Target = 0.1 (Low):**
- Lower particle weights
- More particles in simulation
- More splitting/roulette operations
- **Use when:** Need very high statistics, willing to pay computational cost

**Target = 1.0 (Medium, Default):**
- Balanced particle weights
- Moderate particle population
- **Use when:** Standard optimization

**Target = 10.0 (High):**
- Higher particle weights
- Fewer particles in simulation
- Less splitting/roulette overhead
- **Use when:** Too many splits/roulettes with lower target

### Tuning Strategy

1. **Start with target=1.0** (default)
2. **Monitor particle population:**
   ```
   c Check output for weight window statistics:
   c - Number of splits
   c - Number of roulette kills
   ```
3. **Adjust if needed:**
   - If excessive splits → Increase target to 5.0 or 10.0
   - If poor statistics → Decrease target to 0.5 or 0.1

---

## Troubleshooting WWG Iterations

### Problem: FOM Not Improving

**Symptoms:**
- FOM_iter2 ≈ FOM_iter1 (no improvement)
- Or FOM decreasing

**Causes:**
1. WWG run too short (high relative error)
2. Detector tally zero or near-zero
3. Geometry issues (lost particles)

**Fixes:**
```
c Increase WWG run statistics
NPS  5e5                        $ Was 1e5

c Check detector tally in WWG run
c Should have relative error <30%

c Verify detector location correct
F5:N  100 0 0  0.5              $ Double-check coordinates
```

---

### Problem: FOM Decreasing Over Iterations

**Symptoms:**
- FOM_iter3 < FOM_iter2 < FOM_iter1
- Getting worse, not better

**Causes:**
1. Weight windows too aggressive
2. Geometry mismatch between WWG and production
3. Energy bins wrong

**Fixes:**
```
c Widen weight window bounds
WWP:N  10  5  5  0  -1          $ wupn=10 (was 5)

c Verify WWGE consistent across all runs
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c       ^must be identical in WWG and production runs

c Check mesh alignment with geometry
```

---

### Problem: All Particles Killed

**Symptoms:**
- Tally result zero
- Warning: "All particles killed by weight windows"

**Causes:**
- Weight windows too restrictive
- WWN values too low

**Fixes:**
```
c Increase target weight
WWG  5  0  10.0                 $ Was 1.0

c Widen window bounds
WWP:N  10  5  10  0  -1         $ wupn=10, mxspln=10

c Or use simpler VR (cell importance)
IMP:N  1  2  4  8  0            $ Instead of WW
```

---

## Advanced: Multi-Tally WWG

### Multiple Detectors

**Challenge:** Optimize for multiple tallies simultaneously

**Strategy 1 - Primary Tally:**
```
F5:N   100 0 0  0.5             $ Detector 1 (optimize for this)
F15:N  0 100 0  0.5             $ Detector 2 (secondary)
c
WWG  5  0  1.0                  $ Optimize for F5 only
```

**Strategy 2 - Mesh Tally:**
```
FMESH4:N  GEOM=XYZ  ORIGIN=0 0 0
          IMESH=100  IINTS=10
          JMESH=100  JINTS=10
          KMESH=100  KINTS=10
c
WWG  4  1  1.0                  $ Optimize for entire mesh
```

---

## Archiving and Reproducibility

### Save wwout Files

```bash
# Archive each iteration
cp wwout wwout_iter1_baseline
cp wwout wwout_iter2_improved
cp wwout wwout_iter3_optimized
cp wwout wwout_final_converged

# Document in README
echo "wwout_final_converged: FOM=5000, 4 iterations, target=1.0" >> WW_README.txt
```

### Recreate Weight Windows

```bash
# To use archived wwout
cp wwout_final_converged wwout
mcnp6 inp=input_prod.i outp=out.o
```

---

## Quick Reference: Iteration Checklist

**Before Starting:**
- [ ] Analog run completed (baseline FOM established)
- [ ] Detector tally defined and validated
- [ ] MESH card appropriate for geometry
- [ ] WWGE energy bins match problem physics

**Iteration N:**
- [ ] Previous wwout exists (if N>1)
- [ ] WWP card includes switchn=-1 (read wwout)
- [ ] WWG card present with appropriate target
- [ ] NPS sufficient (increases each iteration)
- [ ] Run completes successfully

**After Iteration N:**
- [ ] Extract FOM from output
- [ ] Check relative error
- [ ] Archive wwout (cp wwout wwout_iterN)
- [ ] Calculate FOM improvement ratio
- [ ] Check convergence: (FOM_N - FOM_{N-1})/FOM_{N-1} < 0.20?

**Final Production:**
- [ ] Use converged wwout
- [ ] Remove WWG card (production doesn't regenerate)
- [ ] High NPS for target relative error
- [ ] Archive final results

---

## Example: Complete 4-Iteration Workflow

### Setup Files

**input_iter1.i** (Initial WWG):
```
WWG  5  0  1.0
NPS  1e5
```

**input_iter2.i** (Use + Regenerate):
```
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  2e5
```

**input_iter3.i** (Continue):
```
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  5e5
```

**input_iter4.i** (Final iteration):
```
WWP:N  J  J  J  0  -1
WWG  5  0  1.0
NPS  1e6
```

**input_final.i** (Production):
```
WWP:N  J  J  J  0  -1
c No WWG card
NPS  5e7
```

### Run Sequence

```bash
# Run all iterations
mcnp6 inp=input_iter1.i outp=o1.o runtpe=r1.r && cp wwout ww1
mcnp6 inp=input_iter2.i outp=o2.o runtpe=r2.r && cp wwout ww2
mcnp6 inp=input_iter3.i outp=o3.o runtpe=r3.r && cp wwout ww3
mcnp6 inp=input_iter4.i outp=o4.o runtpe=r4.r && cp wwout ww4

# Check convergence
for f in o*.o; do
    echo "=== $f ==="
    grep "tally  5" $f | tail -1
done

# If converged, run final
mcnp6 inp=input_final.i outp=final.o runtpe=final.r
```

---

## References

**See Also:**
- `variance_reduction_theory.md` - WWG algorithm theory
- `card_specifications.md` - WWG/WWP/WWN card syntax
- `error_catalog.md` - WWG troubleshooting

**MCNP6 Manual:**
- Chapter 5.12.7: WWG Card
- Chapter 5.12.4: WWP Card
- Appendix D: Weight Window File Format
