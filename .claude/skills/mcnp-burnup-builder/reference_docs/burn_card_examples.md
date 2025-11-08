# BURN Card Examples for Production-Quality Calculations
**Complete Templates and Best Practices**

## Purpose

This document provides production-quality BURN card examples for common reactor burnup scenarios, with detailed annotations and best practices derived from AGR-1 and production reactor models.

---

## Basic Templates

### Template 1: Single-Cycle PWR Fuel Burnup

**Scenario**: Standard PWR fuel pin, 18-month cycle (540 days), 100 days/step

```mcnp
c ================================================================
c Single-Cycle PWR Fuel Pin Burnup
c Total irradiation: 540 EFPD at 40 kW/kg specific power
c ================================================================

c --- Cells ---
1  1  -10.4  -1  IMP:N=1  VOL=193.0   $ UO2 fuel (r=0.41 cm, h=100 cm)
2  2  -6.5    1 -2  IMP:N=1  VOL=42.5 $ Zircaloy clad
3  3  -0.74   2 -3  IMP:N=1           $ H2O coolant
4  0   3  IMP:N=0                     $ Outside

c --- Surfaces ---
1  CZ  0.41   $ Fuel radius
2  CZ  0.48   $ Clad outer
3  CZ  0.75   $ Coolant boundary

c --- Materials (Fresh fuel BOL) ---
M1  $ UO2 fuel, 4.5% enriched, 10.4 g/cm3
   92234.70c  3.600E-04  $ U-234
   92235.70c  4.500E-02  $ U-235 (4.5% enrichment)
   92236.70c  2.100E-06  $ U-236 (trace)
   92238.70c  9.550E-01  $ U-238
    8016.70c  2.000E+00  $ O-16 (stoichiometric)

M2  $ Zircaloy-4 clad
   40000.60c  0.98
   26000.50c  0.002
   24000.50c  0.001
   28000.50c  0.001

M3  $ Light water moderator
    1001.70c  2.0
    8016.70c  1.0
MT3  lwtr.10t

c --- Source (criticality) ---
KCODE  10000  1.0  50  150
KSRC  0 0 0

c --- Burnup Specification ---
BURN  TIME=100 200 300 400 500 540  $ 6 steps, 540 days total
      POWER=7.72                    $ 7.72 kW total (40 kW/kg × 0.193 kg)
      PFRAC=1.0                     $ Continuous operation
      MAT=1                         $ Burn material 1 (fuel)
      MATVOL=193.0                  $ Fuel volume (cm³)
      BOPT=1.0, -1, 1               $ Q=1.0, Tier 1 FPs, standard output
      OMIT=1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244

c --- OMIT explanation ---
c Material 1, reason 8 (no cross-sections), isotope list:
c   6014 (C-14), 7016 (N-16), 8018 (O-18), 9018 (F-18)
c   90234 (Th-234), 91232 (Pa-232), 95240 (Am-240), 95244 (Am-244)
```

**Output**: Keff and burnup at 100, 200, 300, 400, 500, 540 days

**Typical results**:
- BOL keff: 1.25-1.30 (fresh fuel, excess reactivity)
- EOL keff: 1.00-1.05 (depleted to critical)
- Burnup: ~40 GWd/MTU

---

### Template 2: Multi-Cycle with Shutdowns

**Scenario**: 3 cycles (18 months each) with 60-day shutdowns

```mcnp
c ================================================================
c Three-Cycle PWR Fuel with Refueling Shutdowns
c Cycle 1: 540 days → 60 day shutdown
c Cycle 2: 540 days → 60 day shutdown
c Cycle 3: 540 days → Final shutdown (5 years)
c ================================================================

[... geometry and materials same as Template 1 ...]

c --- Multi-Cycle Burnup ---
c CYCLE 1: 540 EFPD
BURN  TIME=100 200 300 400 500 540
      POWER=7.72
      PFRAC=1.0
      MAT=1
      MATVOL=193.0
      BOPT=1.0, -1, 1

c SHUTDOWN 1: 60 days decay
BURN  TIME=600           $ 540 + 60 = 600 days cumulative
      POWER=0            $ No power during shutdown
      PFRAC=0            $ Ignored when POWER=0
      MAT=1
      MATVOL=193.0
      BOPT=1.0, -1, 1

c CYCLE 2: 540 EFPD
BURN  TIME=700 800 900 1000 1100 1140  $ Resume irradiation
      POWER=7.72
      PFRAC=1.0
      MAT=1
      MATVOL=193.0
      BOPT=1.0, -1, 1

c SHUTDOWN 2: 60 days
BURN  TIME=1200          $ 1140 + 60 = 1200 days
      POWER=0
      MAT=1
      MATVOL=193.0
      BOPT=1.0, -1, 1

c CYCLE 3: 540 EFPD
BURN  TIME=1300 1400 1500 1600 1700 1740
      POWER=7.72
      PFRAC=1.0
      MAT=1
      MATVOL=193.0
      BOPT=1.0, -1, 1

c FINAL SHUTDOWN: 5 years cooling (1825 days)
BURN  TIME=3565          $ 1740 + 1825 = 3565 days
      POWER=0
      MAT=1
      MATVOL=193.0
      BOPT=1.0, -1, 1

c OMIT list (same for all BURN cards)
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      [repeat OMIT for each BURN card]
```

**Key features**:
- Decay periods: POWER=0, PFRAC ignored
- Cumulative time: Always increasing
- Isotopic decay during shutdowns: Xe-135 decays, Pm-149→Sm-149, Pu-241→Am-241

**Typical results**:
- End-of-cycle 3 burnup: ~120 GWd/MTU
- Am-241 builds up during shutdowns (from Pu-241 decay)
- Xe-135 poisoning peaks ~9 hours after shutdown, then decays

---

### Template 3: Multi-Zone Core (Radial Power Distribution)

**Scenario**: 3-zone reactor core with different power fractions

```mcnp
c ================================================================
c Three-Zone Core with Radial Power Distribution
c Inner zone: High power (45%)
c Middle zone: Medium power (35%)
c Outer zone: Low power (20%)
c ================================================================

c --- Cells ---
1  1  -10.4  -1  IMP:N=1  VOL=500.0   $ Inner fuel (high flux)
2  2  -10.4  -2 1  IMP:N=1  VOL=800.0 $ Middle fuel
3  3  -10.4  -3 2  IMP:N=1  VOL=1200.0 $ Outer fuel (low flux)
[... clad, coolant, etc. ...]

c --- Materials (all fresh fuel BOL) ---
M1  $ Inner zone fuel (same as M2, M3 initially)
   [... 4.5% UO2 ...]
M2  $ Middle zone fuel
   [... 4.5% UO2 ...]
M3  $ Outer zone fuel
   [... 4.5% UO2 ...]

c --- Burnup (power fractions by zone) ---
BURN  TIME=100 200 300 400 500 540
      POWER=3400                     $ 3400 MW total core power
      PFRAC=1.0
      MAT=1 2 3                      $ Burn all three zones
      MATVOL=500.0 800.0 1200.0      $ Volumes for each zone
      BOPT=1.0, -1, 1

c OMIT for each material
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      2, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      3, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**Important**: MCNP automatically calculates power fractions per material

**Output** (PRINT Table 211-219):
```
Material 1: Power fraction ~0.45 (inner zone, highest flux)
Material 2: Power fraction ~0.35 (middle zone)
Material 3: Power fraction ~0.20 (outer zone, lowest flux)
```

**Verification**: Sum of power fractions ≈ 1.0

---

### Template 4: Burnable Absorber Depletion

**Scenario**: Fuel + Gadolinia burnable absorber

```mcnp
c ================================================================
c Fuel Pin with Gd2O3 Burnable Absorber
c Track fuel and absorber separately
c ================================================================

c --- Cells ---
1  1  -10.4  -1  IMP:N=1  VOL=193.0   $ UO2 fuel
2  2  -9.8   -2  IMP:N=1  VOL=12.5    $ UO2-Gd2O3 (5 wt% Gd2O3)
[... clad, coolant ...]

c --- Materials ---
M1  $ Standard UO2 fuel
   92234.70c  3.600E-04
   92235.70c  4.500E-02
   92238.70c  9.550E-01
    8016.70c  2.000E+00

M2  $ UO2 with 5% Gd2O3 (poison)
   92234.70c  3.420E-04  $ Reduced by 5% for Gd
   92235.70c  4.275E-02
   92238.70c  9.073E-01
   64155.70c  2.500E-03  $ Gd-155 (STRONG absorber, 61 kbarn)
   64157.70c  1.500E-03  $ Gd-157 (STRONGEST, 254 kbarn)
   64158.70c  5.000E-04  $ Gd-158 (low absorption)
   64160.70c  3.000E-04  $ Gd-160 (low absorption)
    8016.70c  2.000E+00

c --- Burnup (track both materials) ---
BURN  TIME=50 100 150 200 250 300 350 400 450 500 540
      POWER=8.5                      $ Slightly higher power (includes absorber)
      PFRAC=1.0
      MAT=1 2                        $ Burn both fuel and absorber
      MATVOL=193.0 12.5              $ Respective volumes
      BOPT=1.0, -1, 1

OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      2, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**Expected behavior**:
- BOL: Low keff (Gd poisoning, -3000 to -5000 pcm)
- 0-200 days: Gd-155, Gd-157 burn out, keff increases
- >200 days: Gd depleted, keff peaks then decreases (normal fuel burnup)

---

### Template 5: Activation Calculation (Structural Steel)

**Scenario**: Activate stainless steel in reactor for 5 years, decay for 30 years

```mcnp
c ================================================================
c Stainless Steel Activation and Decay
c Irradiation: 5 years (1825 days)
c Decay: 30 years (10950 days)
c ================================================================

c --- Cells ---
1  1  -7.9   -1  IMP:N=1  VOL=1000.0  $ SS-316 plate
2  2  -1.0    1 -2  IMP:N=1           $ Water (moderator/coolant)
3  0   2  IMP:N=0

c --- Surfaces ---
1  RCC  0 0 0  0 0 10  5   $ Cylinder r=5, h=10
2  RCC  0 0 0  0 0 15  20

c --- Materials ---
M1  $ Stainless Steel 316L
   26054.70c  0.038      $ Fe-54
   26056.70c  0.604      $ Fe-56 (major component)
   26057.70c  0.013      $ Fe-57
   26058.70c  0.002      $ Fe-58
   24050.70c  0.007      $ Cr-50
   24052.70c  0.143      $ Cr-52
   24053.70c  0.017      $ Cr-53
   24054.70c  0.004      $ Cr-54
   28058.70c  0.081      $ Ni-58
   28060.70c  0.032      $ Ni-60
   28061.70c  0.001      $ Ni-61
   28062.70c  0.005      $ Ni-62
   28064.70c  0.001      $ Ni-64
   42092.70c  0.004      $ Mo-92
   42094.70c  0.002      $ Mo-94
   42095.70c  0.004      $ Mo-95
   42096.70c  0.004      $ Mo-96
   42097.70c  0.002      $ Mo-97
   42098.70c  0.006      $ Mo-98
   42100.70c  0.003      $ Mo-100

M2  $ Water
    1001.70c  2.0
    8016.70c  1.0
MT2  lwtr.10t

c --- Source (external flux, not critical) ---
SDEF  POS=0 0 -10  AXS=0 0 1  ERG=1.0  PAR=N  RAD=d1
SI1  0 20
SP1  -21 1

c --- Burnup (activation + decay) ---
c IRRADIATION: 5 years at reactor flux
BURN  TIME=365 730 1095 1460 1825  $ 1, 2, 3, 4, 5 years
      POWER=0.001                  $ Small power (flux normalization)
      PFRAC=1.0
      MAT=1
      MATVOL=1000.0
      BOPT=1.0, -1, 1
      OMIT=1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244

c DECAY: 30 years (stepwise for dose tracking)
BURN  TIME=1860   POWER=0  MAT=1  MATVOL=1000.0  BOPT=1.0,-1,1  $ +35 days
BURN  TIME=1955   POWER=0  MAT=1  MATVOL=1000.0  BOPT=1.0,-1,1  $ +90 days
BURN  TIME=2190   POWER=1  MAT=1  MATVOL=1000.0  BOPT=1.0,-1,1  $ +1 year
BURN  TIME=2920   POWER=0  MAT=1  MATVOL=1000.0  BOPT=1.0,-1,1  $ +3 years
BURN  TIME=5475   POWER=0  MAT=1  MATVOL=1000.0  BOPT=1.0,-1,1  $ +10 years
BURN  TIME=12775  POWER=0  MAT=1  MATVOL=1000.0  BOPT=1.0,-1,1  $ +30 years

MODE  N
NPS  100000
```

**Key activation products**:
- Co-60 (5.27 yr): Dominant γ source, from Ni-59(n,γ)Co-60 and Co-59(n,γ)Co-60
- Fe-55 (2.7 yr): X-ray source
- Mn-54 (312 day): γ source (short-term)
- Ni-63 (100 yr): β source (long-term)

---

### Template 6: HTGR TRISO Fuel (AGR-1 Based)

**Scenario**: TRISO fuel compact with UCO kernels

```mcnp
c ================================================================
c HTGR TRISO Fuel Compact Burnup (AGR-1 style)
c Fuel: UCO kernels (19.7% enriched)
c Irradiation: Time-averaged power history
c ================================================================

c --- Cells (simplified) ---
1  1  -10.924  -1  U=10  IMP:N=1  VOL=0.092  $ UCO kernel
2  2  -1.100    1 -2  U=10  IMP:N=1          $ Buffer (porous C)
3  3  -1.912    2 -3  U=10  IMP:N=1          $ IPyC
4  4  -3.207    3 -4  U=10  IMP:N=1          $ SiC
5  5  -1.901    4 -5  U=10  IMP:N=1          $ OPyC
6  6  -1.256    5     U=10  IMP:N=1          $ Graphite matrix
[... lattice fill with universe 10 repeated ...]

c --- Materials ---
M1  $ UCO kernel, 19.7% enriched
   92234.00c  3.342E-03  $ U-234
   92235.00c  1.996E-01  $ U-235 (19.7% enrichment)
   92236.00c  1.931E-04  $ U-236
   92238.00c  7.968E-01  $ U-238
    6012.00c  3.217E-01  $ C-12 (carbide)
    6013.00c  3.578E-03  $ C-13
    8016.00c  1.361E+00  $ O-16 (oxide)

M2  $ Buffer layer (porous carbon)
    6012.00c  0.989
    6013.00c  0.011

M3  $ IPyC
    6012.00c  0.989
    6013.00c  0.011

M4  $ SiC
   14028.00c  0.922      $ Si-28
   14029.00c  0.047      $ Si-29
   14030.00c  0.031      $ Si-30
    6012.00c  0.989      $ C-12 (in SiC)
    6013.00c  0.011      $ C-13

M5  $ OPyC
    6012.00c  0.989
    6013.00c  0.011

M6  $ Graphite matrix
    6012.00c  0.989
    6013.00c  0.011

c --- Time-averaged power from operational history ---
c AGR-1 actual: 616 time steps over 138 days
c Time-averaged: 5.23 MW average power

c --- Burnup ---
BURN  TIME=35 70 105 138                   $ 138 days total (AGR-1 cycle)
      POWER=5.23                           $ Time-averaged power (MW)
      PFRAC=1.0
      MAT=1                                $ Burn kernel only (UCO)
      MATVOL=0.092                         $ Kernel volume
      BOPT=1.0, -2, 1                      $ Tier 2 FPs (higher fidelity)
      OMIT=1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244

c --- Optional: Track graphite matrix for C-14 production ---
c Uncomment to track C-14 activation:
c MAT=1 6
c MATVOL=0.092  [matrix volume]
```

**Key features**:
- High enrichment (19.7% vs. 4.5% for LWR)
- UCO fuel (UC + UO₂ mixed oxide/carbide)
- Graphite thermal scattering (should add: MT1 grph.18t, MT2-6 grph.18t)
- Time-averaged power (simplifies complex operational history)

---

## Advanced Features

### Adaptive Time Stepping

**BOL (rapid changes)**: Fine steps
**Mid-life (approaching equilibrium)**: Coarse steps
**EOL (equilibrium)**: Very coarse steps

```mcnp
c Adaptive time stepping
BURN  TIME=10 20 30 40 50             $ BOL: 10-day steps (rapid Pu buildup)
      POWER=7.72  PFRAC=1.0  MAT=1  MATVOL=193.0  BOPT=1.0,-1,1

BURN  TIME=100 150 200 250 300 350    $ Mid: 50-day steps
      POWER=7.72  PFRAC=1.0  MAT=1  MATVOL=193.0  BOPT=1.0,-1,1

BURN  TIME=450 540                    $ EOL: 90-day steps
      POWER=7.72  PFRAC=1.0  MAT=1  MATVOL=193.0  BOPT=1.0,-1,1

OMIT  1, 8, [...]
```

### Material Modification (MATMOD)

**Scenario**: Add boron poison at mid-cycle

```mcnp
c Initial burnup
BURN  TIME=100 200 270
      POWER=7.72  PFRAC=1.0  MAT=1  MATVOL=193.0  BOPT=1.0,-1,1

c Insert boron at step 4 (270 days)
BURN  TIME=370 470 540
      POWER=7.72  PFRAC=1.0  MAT=1  MATVOL=193.0  BOPT=1.0,-1,1
      MATMOD=4, 1, 5010, 1.0E-6    $ At step 4, material 1, add B-10 at 1E-6
```

---

## Best Practices Summary

### 1. Time Steps

**During irradiation**: 50-100 day intervals

**During shutdown**: Finer resolution for short-lived isotopes
- First 24 hours: Hourly steps (Xe-135 decay)
- 1-7 days: Daily steps
- >1 week: Weekly or monthly steps

### 2. Power Specification

**Fixed power**: Use POWER keyword (MW)

**Variable power**: Use time-weighted average

**Decay only**: POWER=0, PFRAC ignored

### 3. Volume Accuracy

**Critical**: MATVOL must match actual cell volume

**Verification**:
```python
# Calculate volume from geometry
V_cylinder = np.pi * r**2 * h
# Compare to VOL card in cell definition
# Compare to MATVOL in BURN card
# All three MUST agree
```

### 4. OMIT Lists

**Always omit**:
- Isotopes without cross-section data
- Short-lived isotopes with t½ < 1 hour (unless tracking transients)
- Isotopes with density < 1E-20 atoms/barn-cm

**Repeat for each material**:
```mcnp
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      2, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      3, 8, [...]
```

### 5. Fission Product Tiers

**Tier 1** (`BOPT=1.0, -1`): ~200 isotopes, FAST, routine work

**Tier 2** (`BOPT=1.0, -2`): ~500 isotopes, MEDIUM, final calculations

**Tier 3** (`BOPT=1.0, -3`): ~1000 isotopes, SLOW, benchmarking

**Tier 4** (`BOPT=1.0, -4`): ~3400 isotopes, VERY SLOW, research only

---

## Troubleshooting Checklist

Before running:
- [ ] MATVOL matches cell VOL
- [ ] TIME values are cumulative (always increasing)
- [ ] POWER units are MW (not W or kW)
- [ ] MAT numbers match actual material cards
- [ ] OMIT lists include all problematic isotopes
- [ ] BOPT tier appropriate for problem (-1 or -2 recommended)
- [ ] KCODE or SDEF source defined
- [ ] NPS or KCODE particle count sufficient

After running:
- [ ] Check keff trend (should decrease with burnup)
- [ ] Verify power fractions sum to ~1.0
- [ ] Check for warning messages in output
- [ ] Verify isotopic inventories are reasonable
- [ ] Compare burnup (GWd/MTU) to expected value

---

## References

- MCNP6 User Manual, Section 3.4 (BURN card)
- AGR-1 HTGR Benchmark Input Files
- OECD/NEA Burnup Credit Benchmarks
- SCALE/ORIGEN Validation Suite
