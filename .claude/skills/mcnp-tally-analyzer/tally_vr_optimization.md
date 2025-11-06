# Tally Optimization with Variance Reduction

**Phase 3 Addition - Coupling Tally Analysis with VR**

## Overview

This reference shows how to analyze tally results to guide variance reduction optimization. Use these techniques to identify which VR methods will be most effective and how to tune them.

**Workflow:** Tally Analysis → VR Recommendations → Improved Results

---

## Analysis-Driven VR Selection

### Decision Matrix

Based on tally characteristics, select appropriate VR technique:

| Tally Characteristic | Best VR Method | Expected Improvement |
|---------------------|----------------|---------------------|
| **Simple geometry (<20 cells)** | Cell importance (IMP) | 5-50× |
| **Complex geometry (>20 cells)** | Weight windows (WWG) | 50-500× |
| **Deep penetration (>15 MFP)** | Exponential transform (EXT) + WWG | 500-5000× |
| **Point detector in void** | DXTRAN sphere | 20-200× |
| **Energy spectrum issues** | Energy-dependent WW (WWE/WWGE) | 10-100× |
| **Spatial mesh tally** | Mesh-based WWG | 20-200× |
| **Time-dependent** | Time splitting + WW | 5-50× |
| **Multiple scattered paths** | Forced collisions (FCL) | 10-100× |

### Diagnostic-Specific Recommendations

**From tally error patterns:**

**Pattern 1: Uniform high error everywhere**
```
All cells/bins: R = 30-50%

Diagnosis: Global under-sampling
VR Solution: Cell importance (simple) or WWG (complex)
Priority: HIGH - Fundamental sampling issue
```

**Pattern 2: High error in specific energy range**
```
E < 1 keV:   R = 5%  ✓
E = 1-10 keV: R = 45% ✗
E > 10 keV:  R = 8%  ✓

Diagnosis: Energy-specific under-sampling
VR Solution: WWGE card with refined bins in 1-10 keV
Priority: MEDIUM - Targeted energy fix
```

**Pattern 3: High error in distant cells**
```
Near source:  R = 3%  ✓
Mid-range:    R = 12% ✓
Far region:   R = 85% ✗

Diagnosis: Deep penetration problem
VR Solution: WWG (auto-generate importance function)
           Or: Exponential transform if >15 MFP
Priority: HIGH - Critical for far-field tallies
```

**Pattern 4: Point detector has huge error**
```
F5 detector: R = 250% (essentially zero scores)

Diagnosis: Point in void/low-importance region
VR Solution: DXTRAN sphere around detector
Priority: CRITICAL - Without DXTRAN, point detector unusable
```

---

## Tally-Based WWG Setup

### Using Tally to Drive Weight Windows

**Most effective tally types for WWG:**

1. **F5 (point detector)** - Best for localized targets
   ```
   F5:N 100 0 0  0.5       $ Point detector at (100,0,0)
   WWG 5 0 1.0              $ Generate WW targeting F5
   ```

2. **F4 (cell flux)** - Good for volume-averaged regions
   ```
   F4:N 50                  $ Flux in detector cell
   WWG 4 0 1.0              $ Generate WW targeting F4
   ```

3. **FMESH** - Excellent for spatial distributions
   ```
   FMESH4:N GEOM=XYZ ...
   WWG 4 0 1.0              $ Generate mesh-based WW
   ```

**Avoid using for WWG:**
- F1 tallies (surface current) - Often create unbalanced WW
- F8 tallies (pulse height) - Energy deposition is secondary effect

### WWGE Energy Structure from Spectrum

**Analyze energy spectrum → Design WWGE bins:**

**Example - Thermal reactor spectrum:**
```
F4 energy analysis shows:
  - Thermal peak at 0.025 eV (45% of flux)
  - Resonance region 1-100 eV (15%)
  - Fast tail >1 keV (40%)

Optimized WWGE for this problem:
WWGE:N  1e-10  $ Lower bound
        1e-9   $ Thermal range (fine bins)
        1e-8
        1e-7
        1e-6   $ 1 eV
        1e-5   $ Epithermal (coarser)
        1e-3   $ 1 keV
        0.1    $ Fast (coarse)
        1
        10
        20     $ Upper bound

Result: Fine resolution where flux is high, coarse where low
```

**General rule:** More WWGE bins in energy ranges with:
- High flux contribution (>10%)
- High relative error (>15%)
- Strong physics effects (resonances, thresholds)

---

## Importance Function Design

### From Tally Spatial Distribution

**Use radial/axial flux profiles to set importance:**

**Example - Cylindrical shielding problem:**
```
Flux profile from F4 tallies:
  r = 0-10 cm:   φ = 1.2e-3  (source region)
  r = 10-30 cm:  φ = 4.5e-4  (shield)
  r = 30-50 cm:  φ = 8.7e-5  (outer shield)
  r = 50-70 cm:  φ = 1.2e-5  (detector region)

Flux ratio source/detector = 1.2e-3 / 1.2e-5 = 100

Cell importance setup:
IMP:N  1        $ Source cells
       10       $ Inner shield (√100 = 10)
       100      $ Outer shield + detector

Reasoning: Importance ∝ 1/flux
          Want ~10× importance per decade of flux drop
```

**Geometric progression rule:**
```
If flux drops by factor F over N cells:
  Use importance increase of F^(1/N) per cell

Example: Flux drops 1000× over 10 cells
  Importance multiplier = 1000^(1/10) ≈ 2.0 per cell
  IMP:N 1 2 4 8 16 32 64 128 256 512 1024
```

---

## Iterative VR Optimization

### Feedback Loop

**Cycle 1: Baseline**
```bash
# Run analog (no VR) to establish baseline
mcnp6 i=problem.inp o=analog.out

# Analyze tallies:
#   - FOM_baseline = 12
#   - Worst tally: F4:14 with R=75%
#   - Spatial issue: far cells under-sampled
```

**Cycle 2: Initial VR**
```bash
# Add WWG targeting worst tally
# Modify input: Add WWG 14 0 1.0

mcnp6 i=problem_vr1.inp o=vr1.out

# Analyze:
#   - FOM_vr1 = 87 (7.2× improvement ✓)
#   - F4:14 now R=18% (improved!)
#   - But F4:12 now worst at R=45%
```

**Cycle 3: Refine VR**
```bash
# Iterate WWG (read previous wwout, regenerate)
# Add: WWP:N J J J 0 -1

mcnp6 i=problem_vr2.inp o=vr2.out

# Analyze:
#   - FOM_vr2 = 152 (1.7× over vr1)
#   - All tallies now R <20%
#   - Converged! (FOM change <2×)
```

**Cycle 4: Production**
```bash
# Remove WWG, keep WWP (use final wwout, don't regenerate)
# Increase NPS 10×

mcnp6 i=problem_prod.inp o=prod.out

# Result:
#   - FOM_prod = 148 (stable ✓)
#   - All tallies R <5%
#   - All 10 checks passed
```

### Convergence Criteria for Iteration

**Stop iterating when:**
1. **FOM change < 20%** between iterations
2. **All tallies** achieve target R (typically <10%)
3. **Weight window bounds** stabilize (WWN values change <10%)
4. **FOM starts decreasing** (overbiasing! Use previous iteration)

---

## Problem-Specific Optimization

### Shielding Calculations

**Tally characteristics:**
- F2 or F4 on far side of shield
- Exponential attenuation
- Deep penetration (>10 MFP common)

**VR Strategy:**
```
1. Check mean free path (MFP):
     λ = 1/Σ_total

   If shield thickness > 15 MFP:
     → Use exponential transform (EXT)

2. Set up EXT + WWG:
     EXT:N 0.75 [list of shield cells]
     VECT  [direction toward detector]
     WWG [tally] 0 1.0

3. Iterate WWG 3-5 times

Expected FOM improvement: 100-5000×
```

### Reactor Core Calculations

**Tally characteristics:**
- F7 fission energy distribution
- Uniform over core
- Complex geometry

**VR Strategy:**
```
1. Analog run usually sufficient for core tallies (high importance naturally)

2. If peripheral detectors needed:
     → Use mesh-based WWG
     MESH GEOM=XYZ ...  $ Cover full core + external regions
     WWG [peripheral tally] 0 1.0

3. No EXT needed (not deep penetration)

Expected FOM improvement: 5-50× for peripheral tallies
```

### Activation Calculations

**Tally characteristics:**
- F4 with FM card (reaction rate)
- Specific isotopes
- Often low reaction rates

**VR Strategy:**
```
1. Identify rate-limiting factor:
   - Flux magnitude? → Standard WWG
   - Specific energy range? → WWGE with fine bins
   - Spatial distribution? → Mesh-based WW

2. For threshold reactions (e.g., (n,2n)):
     WWGE:N 0 5 8 10 12 14 16 18 20  $ Fine bins near threshold
     WWG [tally] 0 1.0

3. Monitor FM-multiplied tally, not base flux

Expected FOM improvement: 10-200×
```

### Dose Calculations

**Tally characteristics:**
- F2/F4 flux converted to dose
- Often at distant locations
- Energy-dependent dose coefficients

**VR Strategy:**
```
1. Use DE/DF dose function in tally:
     F4:N [detector cell]
     DE4 [energy bins]
     DF4 [dose conversion factors from ICRP-74]

2. WWG targets dose tally (not flux):
     WWG 4 0 1.0

3. WWGE structure should match DE bins

4. If point detector:
     Add DXTRAN sphere + WWG

Expected FOM improvement: 20-500×
```

---

## VR Tuning from Tally Feedback

### Adjusting WWP Parameters

**Default:** `WWP:N J J J 0 -1` (uses defaults wupn=5, wsurvn=3)

**When to adjust:**

**High VOV (>0.10) despite good FOM:**
```
Problem: Few high-weight particles

Solution: Widen window
  WWP:N 10 3 5 0 -1
        ^wupn=10 (was 5)

Effect: Particles survive longer before splitting/roulette
        Reduces weight variance
```

**FOM good but some tallies still high R:**
```
Problem: Under-sampling specific regions

Solution: Lower survival weight (more aggressive splitting)
  WWP:N 5 2 5 0 -1
         ^wsurvn=2 (was 3)

Effect: More particles created in low-importance regions
        Better sampling at cost of more particles
```

**Weight ratio >1E6:**
```
Problem: Extreme weight variation

Solution: Combination approach
  WWP:N 15 4 5 0 -1
        ^wupn=15 (wider window)
          ^wsurvn=4 (less aggressive)

Effect: Gentler importance changes
```

### Adjusting EXT Parameter

**Theory:** EXT parameter p ∈ [0, 1]
- p = 0: No biasing
- p = 1: Maximum biasing (risky!)

**Tuning:**

**Start conservative:**
```
EXT:N 0.7 [cells]

Run → Check:
  - FOM improved? → Increase p
  - VOV >0.10? → Decrease p
```

**Typical optimal values:**
- Neutrons in concrete: p = 0.75-0.85
- Photons in lead: p = 0.85-0.95
- Neutrons in water: p = 0.70-0.80

**Warning signs p is too high:**
- VOV > 0.10
- Weight ratio > 1E6
- Statistical checks failing despite low R
- FOM decreasing

### Mesh Resolution Optimization

**For mesh-based WWG:**

**Too fine:**
- WWG slow to generate
- Weight windows vary too rapidly
- Particles split/roulette frequently

**Too coarse:**
- Importance function not detailed enough
- Limited FOM improvement

**Optimal mesh sizing:**
```
Rule of thumb:
  Mesh size ≈ 2-3 × mean free path

Example - Concrete shield (λ ≈ 5 cm):
  MESH spacing: 10-15 cm
  → 10-20 bins across 1-2 m shield
```

**Test mesh convergence:**
```
Run 1: IINTS=10 (10 cm bins) → FOM = 250
Run 2: IINTS=20 (5 cm bins)  → FOM = 267 (7% improvement)
Run 3: IINTS=40 (2.5 cm bins) → FOM = 271 (1.5% improvement)

Conclusion: 20 bins sufficient (diminishing returns)
           Use IINTS=20 for production
```

---

## Automated VR Optimization Script

```python
def optimize_vr_from_tally_analysis(output_file):
    """
    Analyze tally results and recommend VR improvements

    Returns: dict with VR recommendations
    """
    from mcnp_tally_analyzer import MCNPTallyAnalyzer

    analyzer = MCNPTallyAnalyzer()
    results = analyzer.get_all_tallies(output_file)

    recommendations = []

    for tally_num, data in results.items():
        error = data.get('relative_error', 999)
        tally_type = data.get('type', 'unknown')

        # High error → needs VR
        if error > 0.20:
            if tally_type == 'F5':
                recommendations.append({
                    'tally': tally_num,
                    'issue': f'Point detector has R={error:.1%}',
                    'vr_method': 'DXTRAN',
                    'card': f'DXT:N x y z 5 20  $ Adjust inner/outer radii',
                    'expected_improvement': '20-200×'
                })
            elif tally_type in ['F2', 'F4']:
                # Check if deep penetration
                cell_data = data.get('cells', [])
                if cell_data:
                    recommendations.append({
                        'tally': tally_num,
                        'issue': f'{tally_type} has R={error:.1%}',
                        'vr_method': 'WWG',
                        'card': f'WWG {tally_num} 0 1.0',
                        'expected_improvement': '50-500×'
                    })

        # Check energy spectrum if available
        energy_data = data.get('energy_bins', [])
        if energy_data:
            # Find bins with high error
            high_error_bins = [i for i, e in enumerate(data.get('errors', []))
                             if e > 0.30]

            if high_error_bins:
                energy_ranges = [energy_data[i] for i in high_error_bins]
                recommendations.append({
                    'tally': tally_num,
                    'issue': f'High error in energy bins: {energy_ranges}',
                    'vr_method': 'WWGE',
                    'card': f'WWGE:N  [refine energy structure in problem ranges]',
                    'expected_improvement': '10-100×'
                })

    return {
        'analysis_file': output_file,
        'recommendations': recommendations,
        'next_steps': [
            '1. Implement highest-priority VR method',
            '2. Run short test (NPS~1e5)',
            '3. Compare FOM improvement',
            '4. Iterate if FOM change >20%',
            '5. Production run when converged'
        ]
    }
```

---

## Quick Reference: Tally → VR Mapping

| Tally Issue | VR Solution | Setup Effort | Expected FOM Gain |
|-------------|-------------|--------------|-------------------|
| Global high R | Cell IMP or WWG | Low (IMP) / Medium (WWG) | 5-50× / 50-500× |
| Energy-specific high R | WWGE with refined bins | Low | 10-100× |
| Spatial gradient | Mesh-based WWG | Medium | 20-200× |
| Point detector R>100% | DXTRAN sphere | Low | 20-200× |
| Deep penetration (>15 MFP) | EXT + WWG | High | 500-5000× |
| Multiple scattered paths | FCL (forced collisions) | Medium | 10-100× |
| Time-dependent poor R | Time splitting | Low | 5-50× |

---

## Integration with Skills

**Use this skill in conjunction with:**
- **mcnp-variance-reducer** - Implement VR recommendations
- **mcnp-ww-optimizer** - Iterative weight window refinement
- **mcnp-statistics-checker** - Validate VR effectiveness
- **mcnp-output-parser** - Extract detailed tally data

---

## References

**VR Theory:**
- ../mcnp-variance-reducer/SKILL.md - Comprehensive VR techniques
- ../mcnp-variance-reducer/advanced_vr_theory.md - Optimization strategies
- ../mcnp-variance-reducer/wwg_iteration_guide.md - WWG workflows

**VR Optimization:**
- ../mcnp-ww-optimizer/SKILL.md - Weight window tuning
- ./vr_effectiveness_analysis.md - Measuring VR performance

**Statistical Validation:**
- ../mcnp-statistics-checker/SKILL.md - Quality checks
