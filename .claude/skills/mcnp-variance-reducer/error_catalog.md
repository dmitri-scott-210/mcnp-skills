# Variance Reduction Error Catalog

## Overview

This catalog documents common variance reduction errors, their symptoms, root causes, diagnosis methods, and fixes. Use this as a troubleshooting reference when VR implementations don't work as expected.

---

## Error 1: Decreasing Figure of Merit

### Symptoms

- FOM decreases steadily as simulation progresses
- Final FOM < analog FOM (baseline without VR)
- Tally fluctuation chart shows downward trend
- Results unreliable despite long run time

### Example Output

```
nps    mean      error     vov    fom
1e5    2.45e-4   0.1500   0.024   98
2e5    2.48e-4   0.1200   0.031   145
5e5    2.51e-4   0.1150   0.042   120
1e6    2.47e-4   0.1180   0.055   95   ← Decreasing!
```

### Root Causes

1. **Weight windows too aggressive:**
   - wupn too small (narrow window)
   - Excessive splitting/roulette overhead

2. **WWG generation insufficient:**
   - WWG run too short
   - Detector tally had poor statistics
   - Weight window mesh too coarse

3. **Incorrect VR parameters:**
   - Energy bins (WWE) don't match problem
   - DXTRAN sphere misaligned
   - Importance discontinuities

### Diagnosis

**Step 1: Check weight window statistics in output**
```
number of particles with weight exceeding window: 4523  ← High?
number of particles with weight below window:     8921  ← High?
```

**Step 2: Examine tally fluctuation chart**
```
c Look for FOM trend:
c - FOM should be horizontal line
c - If sloping down → VR problem
```

**Step 3: Check WWG generation output**
```
c In WWG run output, check detector tally:
tally 5:  relative error = 0.35  ← Too high! (should be <0.30)
```

### Fixes

**Fix 1: Widen weight window bounds**
```
c Before:
WWP:N  5  3  5  0  -1           $ Standard

c After:
WWP:N  10  5  5  0  -1          $ Wider window (wupn=10)
```

**Fix 2: Regenerate weight windows with more statistics**
```
c Increase WWG run length
NPS  5e5                        $ Was 1e5
```

**Fix 3: Adjust WWG target weight**
```
c Increase target for higher overall weights
WWG  5  0  10.0                 $ Was 1.0
```

**Fix 4: Simplify VR approach**
```
c Remove aggressive VR methods
c Comment out DXTRAN or EXT
c c DXTRAN  1.0  100 0 0  1000  $ Removed temporarily
c
c Use simpler cell importance
IMP:N  1  2  4  8  16  0        $ Geometric progression
```

---

## Error 2: No Particles Reaching Detector

### Symptoms

- Detector tally result: 0.00000 (or near-zero)
- Warning: "tally had 0 particles contributing"
- All 10 statistical tests FAIL
- Message: "problem summary - run terminated when X particles got cutoff"

### Example Output

```
tally   5
         tally type 5    point detector
         number of histories used for normalizing tallies =   1000000
         nps    mean       error      vov
         1e6    0.00000    0.0000    0.0000  ← Zero result!
```

### Root Causes

1. **Weight windows too restrictive:**
   - WWN values too low
   - All particles killed by Russian roulette
   - Never reach detector

2. **Importance map incorrect:**
   - IMP values decrease toward detector (backwards!)
   - Weight windows inverted

3. **Geometry issues:**
   - Detector location unreachable
   - Graveyard cells blocking path
   - Void cells without importance

### Diagnosis

**Step 1: Check particle population**
```
c Output summary:
tracks    weight     energy
1000000   0.00       0.0      ← All particles killed!
```

**Step 2: Check PRINT table for importance**
```
c Cell importance table (PRINT 40):
cell  imp:n
1     1          ← Source
2     0.5        ← Wrong! Decreasing toward detector
3     0.25       ← Should be increasing!
```

**Step 3: Enable diagnostic output**
```
c Add to input:
PRDMP  1e4  1e4  1  J  J  1    $ Print every 1e4 histories
```

### Fixes

**Fix 1: Increase weight window target**
```
c Higher target = higher weights = less roulette
WWG  5  0  10.0                 $ Was 1.0
```

**Fix 2: Widen weight window bounds**
```
WWP:N  10  5  10  0  -1         $ wupn=10, mxspln=10
c      ^wide window ^fewer kills
```

**Fix 3: Fix importance direction**
```
c Before (WRONG):
IMP:N  8  4  2  1  0            $ Decreasing!

c After (CORRECT):
IMP:N  1  2  4  8  0            $ Increasing toward detector
```

**Fix 4: Verify detector location accessible**
```
c Check geometry with visual plot
c Verify detector not in void or graveyard
F5:N  100 0 0  0.5              $ Verify coordinates
```

**Fix 5: Start with analog, add VR incrementally**
```
c Remove all VR temporarily
c IMP:N  1  1  1  1  0          $ All cells IMP=1
c c WWP:N  ...                  $ Commented out
c
c Verify particles reach detector in analog mode
c Then re-add VR one method at a time
```

---

## Error 3: Weight Window Generation Failed

### Symptoms

- wwout file size = 0 bytes (or doesn't exist)
- No improvement from WWG (FOM same as analog)
- Warning: "weight window generator did not produce output"
- Error: "tally has insufficient statistics for WWG"

### Example Output

```
$ ls -lh wwout
-rw-r--r--  1 user  group  0B  Nov  4 12:00 wwout  ← Zero size!
```

### Root Causes

1. **WWG run too short:**
   - Detector tally relative error >50%
   - Flux estimate too noisy

2. **Detector tally never scored:**
   - Tally definition error
   - No particles reached detector in WWG run

3. **Mesh configuration error:**
   - MESH card syntax error
   - Mesh doesn't encompass geometry

4. **Energy bins mismatch:**
   - WWGE energy bins inappropriate
   - Too many or too few groups

### Diagnosis

**Step 1: Check WWG run output for detector tally**
```
tally   5
         nps    mean       error      vov
         1e5    2.45e-4    0.45      0.18   ← Error too high!
```
Target: relative error <0.30 for reliable WWG

**Step 2: Verify wwout file created**
```bash
ls -lh wwout
# Should be >1 KB
# If 0 bytes → WWG failed
```

**Step 3: Check for WWG-specific errors**
```
c Search output for:
grep -i "weight window" output.o
grep -i "wwg" output.o
```

### Fixes

**Fix 1: Increase WWG run statistics**
```
c Before:
NPS  1e5                        $ Too short

c After:
NPS  5e5                        $ More statistics for WWG
```

**Fix 2: Simplify energy structure**
```
c Before (too many groups):
WWGE:N  0 1e-10 1e-9 1e-8 ...  $ 20 groups

c After (fewer groups):
WWGE:N  0  1e-8  1e-6  1e-4  0.01  0.1  1  20  $ 7 groups
```

**Fix 3: Verify mesh encompasses geometry**
```
c Check mesh bounds include all geometry
MESH  GEOM=XYZ  ORIGIN=-100 -100 -100
      IMESH=100  IINTS=10    $ Full geometry coverage
      JMESH=100  JINTS=10
      KMESH=100  KINTS=10
```

**Fix 4: Use cell-based WW instead of mesh**
```
c If mesh WWG failing, try cell-based
c Remove MESH and WWG cards
c Use manual WWN with conservative values
WWN:N  1.0  0.8  0.6  0.4  0.2
```

---

## Error 4: DXTRAN Not Improving FOM

### Symptoms

- DXTRAN card added, but FOM unchanged
- DXTRAN statistics in output: 0 contributions
- Point detector FOM same as without DXTRAN

### Example Output

```
dxtran diagnostics
  dxtran contributions:    0        ← No contributions!
  source particles:        1000000
```

### Root Causes

1. **DXTRAN sphere misaligned:**
   - Sphere center ≠ detector location
   - Coordinates mismatch

2. **DXTRAN sphere too small:**
   - Doesn't encompass detector
   - R parameter too small

3. **DXC cells wrong:**
   - Important cells excluded from DXC list
   - No collisions in contributing cells

4. **MAX parameter too small:**
   - Contributions limited prematurely
   - Need higher MAX value

### Diagnosis

**Step 1: Verify DXTRAN and detector coordinates match**
```
c Detector:
F5:N  100 0 0  0.5              $ At (100, 0, 0)

c DXTRAN:
DXTRAN  1.0  100 0 0  1000      $ Should match ✓

c WRONG example:
c DXTRAN  1.0  90 0 0  1000     $ Misaligned! ✗
```

**Step 2: Check DXTRAN statistics in output**
```
grep -A 5 "dxtran" output.o
c Should show non-zero contributions
```

**Step 3: Verify sphere encompasses detector**
```
c Distance from sphere center to detector:
c d = sqrt((x_det - x_dxt)² + (y_det - y_dxt)² + (z_det - z_dxt)²)
c Should be: d < R_dxtran
```

### Fixes

**Fix 1: Align DXTRAN with detector**
```
c Match coordinates exactly
F5:N  100 0 0  0.5
DXTRAN  1.0  100 0 0  1000      $ Exact match
```

**Fix 2: Increase sphere radius**
```
c Before:
DXTRAN  0.5  100 0 0  1000      $ R = 0.5 cm

c After:
DXTRAN  5.0  100 0 0  1000      $ R = 5 cm (larger)
```

**Fix 3: Adjust DXC cell list**
```
c Ensure important cells contribute
DXC  1  2  3  4  J  J  J        $ First 4 cells + all others
c    ^shield cells   ^rest
```

**Fix 4: Increase MAX parameter**
```
c Before:
DXTRAN  1.0  100 0 0  100       $ MAX = 100

c After:
DXTRAN  1.0  100 0 0  5000      $ MAX = 5000 (more contributions)
```

---

## Error 5: Importance Discontinuity Issues

### Symptoms

- Warning: "large importance ratio between cells X and Y"
- Warning: "splitting efficiency poor"
- Excessive particle population
- Memory issues from too many splits

### Example Output

```
warning:  importance ratio of 100.0 between cell 5 and 6
          splitting may be inefficient

number of particles banked:  125000  ← Very high!
```

### Root Causes

1. **Importance jumps too large:**
   - IMP ratio >10× between adjacent cells
   - Causes excessive splitting

2. **Geometric progression too aggressive:**
   - IMP: 1, 4, 16, 64, 256... (powers of 4)
   - Should use powers of 2: 1, 2, 4, 8, 16...

3. **Missing intermediate cells:**
   - Large gap between source and detector
   - Need more granular importance

### Diagnosis

**Step 1: Check importance ratios**
```
c Review cell importance definitions
IMP:N  1  2  4  8  16  32  64  128  256  0
c         ^^  Adjacent cells
c         Ratio = 4/2 = 2 ✓ (OK)

c BAD example:
c IMP:N  1  100  0
c         ^  ^^^ Ratio = 100! (Too large)
```

**Step 2: Look for warning messages**
```
grep -i "importance" output.o
grep -i "splitting" output.o
```

### Fixes

**Fix 1: Smooth importance gradient**
```
c Before (BAD):
IMP:N  1  100  0                $ 100× jump!

c After (GOOD):
IMP:N  1  2  4  8  16  32  64  0  $ Gradual (2× steps)
```

**Fix 2: Add intermediate cells**
```
c Before: Source → Shield → Detector (2 cells)
1  1  -1.0  -1      IMP:N=1
2  2  -7.8  1 -2    IMP:N=100   $ Too large!

c After: Source → Shield1 → Shield2 → Shield3 → Detector (4 cells)
1  1  -1.0  -1      IMP:N=1
2  2  -7.8  1 -2    IMP:N=3
3  2  -7.8  2 -3    IMP:N=10
4  2  -7.8  3 -4    IMP:N=30
5  0        4 -5    IMP:N=100
```

**Fix 3: Limit to 2× or 4× progression**
```
c Recommended: 2× progression
IMP:N  1  2  4  8  16  32  0

c Acceptable: 4× progression (for very simple geometries)
IMP:N  1  4  16  64  0

c AVOID: Larger jumps
c IMP:N  1  10  100  1000  0    ← Too aggressive
```

---

## Error 6: Energy-Dependent VR Not Working

### Symptoms

- Some energy ranges have good statistics, others poor
- Relative error varies wildly across energy bins
- WWE/WWN cards present but ineffective

### Example Output

```
energy bin    flux        rel. error
1e-8 - 1e-6   2.45e-4     0.05        ✓ Good
1e-6 - 1e-4   3.12e-5     0.45        ✗ Poor!
1e-4 - 0.01   1.87e-4     0.08        ✓ Good
```

### Root Causes

1. **Energy bins don't match problem:**
   - Thermal problem with fast neutron bins
   - Missing important energy range

2. **WWN values not energy-dependent:**
   - All energy groups have same WWN
   - Should vary by energy importance

3. **Energy bins too broad or too narrow:**
   - Single bin covers 8 decades
   - Or 50 bins with poor statistics each

### Diagnosis

**Step 1: Review energy structure vs. problem physics**
```
c Thermal problem needs fine thermal structure:
WWE:N  0  1e-10  1e-8  1e-6  1e-4  0.01  20  ✓
c      ^fine thermal structure

c Not this:
c WWE:N  0  1e-6  20  ✗
c      ^no thermal resolution
```

**Step 2: Check WWN has energy-dependent values**
```
c GOOD (energy-dependent):
WWE:N  0  1e-8  1e-6  0.01  20
WWN:N  1.0  0.9  0.8  0.7  &   $ Cell 1, varies by energy
       0.8  0.7  0.6  0.5      $ Cell 2, varies by energy

c BAD (not energy-dependent):
WWN:N  1.0  1.0  1.0  1.0  &   $ All same! ✗
```

### Fixes

**Fix 1: Match energy structure to physics**
```
c For thermal problem:
WWE:N  0  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  20
c      ^thermal  ^epithermal  ^fast

c For fast problem:
WWE:N  0  0.1  1  5  10  14  20
c      ^slow    ^fast energy range
```

**Fix 2: Use WWG to generate energy-dependent WW**
```
c Let WWG calculate optimal energy dependence
WWGE:N  0  1e-8  1e-6  1e-4  0.01  0.1  1  20
WWG  5  0  1.0
c Will automatically create energy-dependent WWN
```

**Fix 3: Adjust number of energy groups**
```
c Too many groups (poor statistics):
c WWE:N  0  1e-10  1e-9  1e-8  ...  $ 20 groups ✗

c Reasonable (good balance):
WWE:N  0  1e-8  1e-6  1e-4  0.01  0.1  1  10  20  $ 8 groups ✓
```

---

## Error Prevention Checklist

### Before Running VR Simulation

**Baseline:**
- [ ] Analog run completed (baseline FOM recorded)
- [ ] Target FOM improvement determined (10-100×)

**Cell Importance:**
- [ ] All cells have IMP defined (no defaults)
- [ ] Graveyard has IMP=0
- [ ] Importance ratios ≤4× between adjacent cells
- [ ] Importance increases toward detector

**Weight Windows:**
- [ ] WWG run completed successfully (relative error <30%)
- [ ] wwout file exists and size >0 bytes
- [ ] WWE energy bins match problem physics
- [ ] WWP parameters reasonable (wupn=5, wsurvn=3)

**DXTRAN:**
- [ ] Sphere center matches detector location
- [ ] Radius encompasses detector (R = 1-10 cm)
- [ ] MAX parameter sufficient (100-1000)
- [ ] DXC cells include important contributors

**General:**
- [ ] MODE card includes all particle types
- [ ] Source definition correct (SDEF or KCODE)
- [ ] Geometry complete (no void cells without IMP)

---

## Quick Diagnosis Flowchart

```
VR Problem?
  |
  +-> FOM decreasing?
  |     YES → Error 1: Weight windows too aggressive
  |     NO → Continue
  |
  +-> Tally result zero?
  |     YES → Error 2: Particles not reaching detector
  |     NO → Continue
  |
  +-> wwout file missing/empty?
  |     YES → Error 3: WWG generation failed
  |     NO → Continue
  |
  +-> DXTRAN not helping?
  |     YES → Error 4: DXTRAN misaligned
  |     NO → Continue
  |
  +-> Warning about importance ratios?
  |     YES → Error 5: Importance discontinuity
  |     NO → Continue
  |
  +-> Energy-dependent statistics poor?
        YES → Error 6: Energy bins mismatch
        NO → Check other issues
```

---

## References

**See Also:**
- `variance_reduction_theory.md` - Theory behind VR methods
- `card_specifications.md` - Correct syntax for VR cards
- `wwg_iteration_guide.md` - WWG optimization workflows

**MCNP6 Manual:**
- Chapter 2: Problem Messages and Warnings
- Chapter 5.12: Variance Reduction Cards
- Appendix D: Output Tables and Interpretation
