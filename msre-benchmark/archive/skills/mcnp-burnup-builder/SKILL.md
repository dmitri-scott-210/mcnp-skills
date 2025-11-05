---
category: E
name: mcnp-burnup-builder
description: Build burnup/depletion calculations using BURN card for fuel evolution, activation, and isotopic inventory tracking with CINDER90 integration
version: 1.0.0
auto_activate: true
activation_keywords:
  - burnup
  - depletion
  - BURN card
  - CINDER90
  - fuel evolution
  - activation
  - isotopic inventory
  - fission products
  - transmutation
  - decay
dependencies:
  - mcnp-input-builder
  - mcnp-lattice-builder
related_skills:
  - mcnp-tally-analyzer
  - mcnp-mesh-builder
output_formats:
  - MCNP input cards (BURN)
  - Isotopic inventory tables
  - Burnup analysis
---

# mcnp-burnup-builder

**Purpose**: Build burnup/depletion calculations using the BURN card to model fuel evolution, activation, fission product buildup, and transmutation over time by coupling MCNP6 neutron transport with CINDER90 depletion solver.

## What Is Burnup?

**Burnup** = Process of nuclear fuel/material composition changing over time due to:
- **Fission** (heavy isotopes → fission products)
- **Neutron capture** (transmutation to heavier isotopes)
- **Radioactive decay** (unstable isotopes → decay products)

**MCNP6 Burnup Capability**:
- Integrates MCNP6 (transport) + CINDER90 (depletion)
- Iterative: MCNP calculates flux → CINDER burns material → update composition → repeat
- Tracks 3,400+ isotopes (actinides + fission products)
- Outputs time-dependent inventories, activities, decay heat

### Applications

- **Reactor physics**: Fuel burnup, criticality evolution, reactivity coefficients
- **Spent fuel**: Isotopic inventory, decay heat, radiation source terms
- **Activation**: Material activation in reactor components
- **Transmutation**: Minor actinide burning, waste reduction
- **Medical isotope production**: Mo-99, I-131, etc.

## Core Concepts

### Burnup Cycle

```
1. MCNP Transport Run
   ↓
   Calculate flux/reaction rates in burnable materials
   ↓
2. CINDER Depletion Step
   ↓
   Solve Bateman equations: dN/dt = Production - Loss
   ↓
   Update material compositions (add/remove isotopes)
   ↓
3. Check Time Step Complete?
   ├─ NO → Return to step 1 (iterate with new compositions)
   └─ YES → Output results, advance to next time step
```

**Time steps**: User-specified intervals (days, years) for burning or decaying.

**Substeps**: MCNP/CINDER iterations within each time step (for convergence).

### BURN Card Syntax

```
BURN  TIME=<t1>,<t2>,...<tn>
      POWER=<power>
      PFRAC=<pf1>,<pf2>,...<pfn>
      MAT=<m1> <m2> ...
      MATVOL=<v1> <v2> ...
      BOPT=<options>
      OMIT=<isotope_list>
      AFMIN=<threshold>
      MATMOD=<modifications>
```

**Keywords**:

- **TIME**: Time step durations (days) - commaseparated list
- **POWER**: Total system power (MW) - normalization
- **PFRAC**: Power fraction per time step (1.0 = 100%, 0 = decay only)
- **MAT**: Material numbers to burn (from Mn cards)
- **MATVOL**: Material volumes (cm³) - required for reaction rate normalization
- **BOPT**: Burn options (Q-value, fission product tiers, output control)
- **OMIT**: Isotopes to omit from transport (use CINDER only)
- **AFMIN**: Minimum atom fraction threshold (default: 1E-32)
- **MATMOD**: Manual isotope modifications at specific time steps

## Decision Tree: Burnup Setup

```
START: Need burnup calculation?
│
├─→ YES: What are you burning?
│   │
│   ├─→ Reactor fuel (fission)
│   │   - MAT = fuel materials (UO2, MOX, etc.)
│   │   - POWER = fission power (MW)
│   │   - PFRAC = 1.0 (continuous burn)
│   │   - TIME = burn cycles (days)
│   │   - BOPT = Q-value, fission product tiers
│   │
│   ├─→ Structural materials (activation only)
│   │   - MAT = structural materials (steel, Al, etc.)
│   │   - POWER = 0 (or small flux normalization)
│   │   - PFRAC = 0 (decay only after irradiation)
│   │   - TIME = irradiation time, decay time
│   │
│   ├─→ Target for isotope production (Mo-99, etc.)
│   │   - MAT = target material
│   │   - POWER = beam power or flux normalization
│   │   - TIME = irradiation + decay times
│   │
│   └─→ Spent fuel decay (no fission)
│       - MAT = spent fuel composition
│       - POWER = 0
│       - PFRAC = 0 (all decay)
│       - TIME = cooling times
│
└─→ NO: Use standard MCNP transport (no BURN card)
```

## Basic Burnup Example

### Example 1: Simple Fuel Pin Burnup

**Problem**: Burn UO2 fuel pin for 100 days at 1 MW.

```
c ============================================================
c Simple Fuel Pin Burnup (100 days, 1 MW)
c ============================================================

c --- Cell Cards ---
1  1  -10.5  -1  IMP:N=1  VOL=50.27   $ Fuel (r < 0.4 cm, h=100 cm)
2  2  -6.5    1 -2  IMP:N=1            $ Clad
3  3  -1.0    2 -3  IMP:N=1            $ Coolant
4  0   3  IMP:N=0                      $ Outside

c --- Surface Cards ---
1  CZ  0.4    $ Fuel radius
2  CZ  0.5    $ Clad radius
3  CZ  5.0    $ Coolant boundary

c --- Material Cards ---
M1  92235.80c  0.04    $ UO2 fuel (4% enrichment)
    92238.80c  0.96
    8016.80c   2.0
M2  40000.80c  1.0     $ Zircaloy clad
M3  1001.80c   2       $ H2O coolant
    8016.80c   1

c --- Source (criticality source for fuel burnup) ---
KCODE  10000  1.0  25  125   $ 10K/cycle, keff=1.0, skip 25, run 125
KSRC  0 0 0   $ Initial source guess

c --- Burnup Specification ---
BURN  TIME=100             $ Burn for 100 days
      POWER=1.0            $ 1 MW total power
      PFRAC=1.0            $ 100% power (continuous burn)
      MAT=1                $ Burn material 1 (fuel)
      MATVOL=50.27         $ Fuel volume (π × 0.4² × 100 = 50.27 cm³)
      BOPT=1.0, -1         $ Q-value=1.0 (default), Tier 1 fission products

c --- Omit isotopes without transport cross sections ---
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244

c --- Problem Termination ---
c (KCODE runs automatically for burnup)
```

**Output** (PRINT Table 210-220):
- **Time 0**: Initial composition (U-235, U-238, O-16)
- **Time 100 days**: Evolved composition (fission products, Pu isotopes, minor actinides)
- **Keff**: Criticality at each time step
- **Burnup**: GWd/MTU
- **Activity**: Curies of each isotope

### Example 2: Burn and Decay (Irradiation + Cooling)

**Problem**: Burn fuel for 50 days, then decay for 10 days (shutdown).

```
BURN  TIME=50, 10          $ 50 days burn, 10 days decay
      POWER=1.0            $ 1 MW
      PFRAC=1.0, 0.0       $ Burn at 100%, then decay at 0%
      MAT=1
      MATVOL=50.27
      BOPT=1.0, -1
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**Interpretation**:
- **Step 1** (0-50 days): Burn at 1 MW (PFRAC=1.0)
- **Step 2** (50-60 days): Decay only (PFRAC=0.0, POWER is ignored)

**Output**: Isotopic inventory after irradiation and after 10-day cooling.

### Example 3: Multiple Burn Cycles

**Problem**: 3 burn cycles of 100 days each, with decay between.

```
BURN  TIME=100, 10, 100, 10, 100, 10   $ 3 cycles: burn-decay-burn-decay-burn-decay
      POWER=1.0
      PFRAC=1.0, 0, 1.0, 0, 1.0, 0     $ Alternate burn and decay
      MAT=1
      MATVOL=50.27
      BOPT=1.0, -1
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**Total time**: 100+10+100+10+100+10 = 330 days.

## Advanced Burn Options (BOPT Keyword)

### BOPT Syntax

```
BOPT=<Q-value>, <FP_tier>, <output>, <xsec_type>, <decay>, <gamma>, ...
```

**Common options**:

**Position 1: Q-value multiplier** (default: 1.0)
- Adjusts energy release per fission
- Usually leave at 1.0

**Position 2: Fission product tier** (default: 0)
- `-4` = All fission products (3400+ isotopes, SLOW)
- `-3` = Tier 3 fission products (medium detail)
- `-2` = Tier 2 fission products (good balance)
- `-1` = Tier 1 fission products (fast, commonly used)
- `0` = No fission products (actinides only, for testing)

**Position 3: Output control**
- `0` = Minimal output
- `1` = Standard output (burnup summary)
- `2` = Detailed output (isotope inventory per step)

**Position 4: Cross section type**
- `0` = Continuous-energy (default, accurate)
- `1` = Tabular transport (requires omitting isotopes without tables)

**Position 5: Decay calculation**
- `0` = Include decay
- `1` = Ignore decay (transport only, for testing)

**Examples**:

```
BOPT=1.0, -1         $ Default: Tier 1 FP, standard output

BOPT=1.0, -2, 2      $ Tier 2 FP, detailed output

BOPT=1.0, -1, 1, 1   $ Tier 1, standard, tabular xsec (requires OMIT)
```

### Fission Product Tiers Explained

| Tier | Isotopes | Speed | Use Case |
|------|----------|-------|----------|
| 0 | Actinides only | Fast | Testing, pure transmutation |
| 1 | ~200 FP | Fast | Routine fuel burnup |
| 2 | ~500 FP | Medium | High-fidelity burnup |
| 3 | ~1000 FP | Slow | Research, benchmarking |
| 4 | ~3400 FP | Very slow | Maximum fidelity |

**Recommendation**: Use **Tier 1** for routine work, **Tier 2** for final calculations.

## Burning Multiple Materials

### Example 4: Two Materials (Different Fuels)

**Problem**: Burn two fuel regions with different enrichments.

```
c --- Materials ---
M1  92235.80c  0.04    $ Fuel 1 (4% enrichment)
    92238.80c  0.96
    8016.80c   2.0
M2  92235.80c  0.05    $ Fuel 2 (5% enrichment)
    92238.80c  0.95
    8016.80c   2.0

c --- Burnup ---
BURN  TIME=100
      POWER=2.0            $ 2 MW total
      PFRAC=1.0
      MAT=1 2              $ Burn both materials
      MATVOL=50.27  50.27  $ Volumes for M1 and M2
      BOPT=1.0, -1
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
      1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**OMIT list**: Each material gets separate omit list (repeat for M1, M2).

**Power fractions**: MCNP calculates fission power fraction automatically for each material.

**Output** (PRINT Table 210):
- Individual material burnup (GWd/MTU)
- Power fraction per material
- Keff evolution

### Example 5: Lattice with Repeated Fuel Pins

**Problem**: 17×17 lattice, burn all fuel pins.

```
c --- Lattice universe (U=1: fuel pin) ---
1  1  -10.5  -1  U=1  IMP:N=1  VOL=50.27   $ Fuel
2  2  -6.5    1 -2  U=1  IMP:N=1           $ Clad
3  3  -1.0    2     U=1  IMP:N=1           $ Coolant

c --- Lattice cell (17×17 = 289 pins) ---
100  0  -10  LAT=1  FILL=0:16 0:16 0:0  IMP:N=1
                    1 1 1 ... (289 entries, all U=1)

c --- Main geometry ---
1000  0  -100  FILL=100  IMP:N=1   $ Fill with lattice

c --- Materials ---
M1  92235.80c  0.04
    92238.80c  0.96
    8016.80c   2.0

c --- Burnup ---
BURN  TIME=100
      POWER=289.0          $ 1 MW per pin × 289 pins = 289 MW
      PFRAC=1.0
      MAT=1
      MATVOL=14528.03      $ 50.27 cm³/pin × 289 pins = 14528.03 cm³
      BOPT=1.0, -1
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**MATVOL calculation**: Volume × number of repeated instances.

**Note**: MCNP burns the **prototype universe** (U=1), which represents all instances in the lattice.

## Material Modification (MATMOD Keyword)

**Purpose**: Manually adjust isotope concentrations at specific time steps (e.g., control rod insertion, poison addition).

### MATMOD Syntax

```
MATMOD=<step>, <mat>, <ZAID>, <density>
       <step>, <mat>, <ZAID>, <density>
       ...
```

Where:
- `<step>` = Time step number (1, 2, 3, ...)
- `<mat>` = Material number
- `<ZAID>` = Isotope ZAID (e.g., 94238 = Pu-238)
- `<density>` = New atom density (atoms/b-cm)

### Example 6: Manual Isotope Adjustment

**Problem**: Add boron poison to fuel at step 2.

```
BURN  TIME=50, 10, 50         $ Step 1, step 2, step 3
      POWER=1.0
      PFRAC=1.0, 0, 1.0
      MAT=1
      MATVOL=50.27
      BOPT=1.0, -1
      MATMOD=2, 1, 5010, 1.0e-6   $ At step 2, add B-10 to M1
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**Effect**: At the start of step 2 (after 50 days), B-10 is added to material 1 at 1E-6 atoms/b-cm.

### Example 7: Multiple Modifications

**Problem**: Adjust Pu-238 in two materials at different steps.

```
MATMOD=1, 4, 94238, 1.0e-6    $ Step 1, M4, Pu-238 → 1E-6
       2, 1, 94238, 1.0e-6    $ Step 2, M1, Pu-238 → 1E-6
       2, 4, 94238, 1.0e-6    $ Step 2, M4, Pu-238 → 1E-6 (again)
```

## Activation Calculations

### Example 8: Structural Material Activation

**Problem**: Activate aluminum target in reactor for 30 days, then decay for 100 days.

```
c --- Geometry ---
1  1  -2.7  -1  IMP:N=1  VOL=100   $ Al target
2  2  -1.0   1 -2  IMP:N=1         $ Water
3  0   2  IMP:N=0

1  RCC  0 0 0  0 0 10  2   $ Al cylinder (r=2, h=10)
2  RCC  0 0 0  0 0 15  10

c --- Materials ---
M1  13027.80c  1.0   $ Pure Al-27
M2  1001.80c   2
    8016.80c   1

c --- Source (external beam or reactor flux) ---
SDEF  POS=0 0 -5  AXS=0 0 1  ERG=2  PAR=N

c --- Burnup (activation + decay) ---
BURN  TIME=30, 100       $ 30 days irradiation, 100 days cooling
      POWER=0.001        $ Small power (flux normalization)
      PFRAC=1.0, 0.0     $ Irradiate, then decay
      MAT=1
      MATVOL=100         $ 100 cm³ Al
      BOPT=1.0, -1
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244

MODE  N
IMP:N  1 1 0
NPS  100000
```

**Output**: Activation products (Al-28, Na-24, etc.) and decay curves.

## Volume Specification (MATVOL)

### Calculating Material Volumes

**For simple geometries**:
```
Cylinder: V = π r² h
Sphere:   V = (4/3) π r³
Box:      V = l × w × h
```

**For lattices**: Volume × number of repeated instances.

**For complex geometries**: Use MCNP volume calculation (VOL card on cell) or external tools.

### VOL Card vs MATVOL

**VOL card** (on cell definition):
```
1  1  -10.5  -1  IMP:N=1  VOL=50.27   $ MCNP uses for tally normalization
```

**MATVOL** (on BURN card):
```
MATVOL=50.27   $ CINDER uses for reaction rate → density conversion
```

**Best practice**: Set both to same value.

```
c Cell definition
1  1  -10.5  -1  IMP:N=1  VOL=50.27

c Burnup
BURN  ...
      MATVOL=50.27   $ Must match VOL
```

### Repeated Structures

For lattices or fills:
```
MATVOL = single_instance_volume × number_of_instances
```

**Example** (17×17 lattice):
```
c Single fuel pin volume
VOL=50.27   $ One pin

c Lattice burnup
MATVOL=14528.03   $ 50.27 × 289 pins
```

## OMIT Keyword (Isotope Exclusions)

**Purpose**: Exclude isotopes from transport that lack cross section data, but include in depletion.

### Why OMIT?

CINDER generates 3,400+ isotopes. Many lack MCNP cross section tables (e.g., short-lived fission products).

**Solution**: List isotopes to omit from transport. CINDER still tracks them, but MCNP doesn't transport them.

### Syntax

```
OMIT=<mat>, <reason>, <ZAID1>, <ZAID2>, ...
     <mat>, <reason>, <ZAID1>, <ZAID2>, ...
```

Where:
- `<mat>` = Material number (matches MAT keyword)
- `<reason>` = Exclusion code (usually 8 = "no cross section data")
- `<ZAID>` = Isotope ZAIDs to omit

### Common Omit List

```
OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244
```

**Isotopes commonly omitted**:
- 6014 (C-14)
- 7016 (N-16)
- 8018 (O-18)
- 9018 (F-18)
- 90234 (Th-234)
- 91232 (Pa-232)
- 95240 (Am-240)
- 95244 (Am-244)

**For each burned material**, repeat the omit list.

### AFMIN (Minimum Atom Fraction)

```
AFMIN=1.0e-32   $ Default
```

**Purpose**: Omit isotopes below threshold atom fraction from transport.

**Effect**: Reduces material complexity, speeds up transport.

**Typical values**:
- `1e-32` (default): Very inclusive
- `1e-20`: Exclude trace isotopes
- `1e-10`: Exclude minor isotopes

## Burnup Output Interpretation

### PRINT Table 210: Burnup Summary

```
   step   duration (days)   time (days)   power (MW)   keff   flux   nu_bar   Q_rec   burnup (GWd/MTU)   source
      0         0.000          0.000         1.000      1.020  2.1e14  2.45     200.5         0.000         1.97e6
      1        50.000         50.000         1.000      1.015  2.0e14  2.46     200.3         7.205         1.95e6
      2        10.000         60.000         0.000      1.014  0.0e00  2.46     200.3         7.205         0.00e0
      3        50.000        110.000         1.000      1.008  1.9e14  2.48     200.1        14.650         1.92e6
```

**Columns**:
- **step**: Time step number
- **duration**: Step length (days)
- **time**: Cumulative time (days)
- **power**: Fission power (MW)
- **keff**: Criticality eigenvalue
- **flux**: Average flux (n/cm²/s)
- **nu_bar**: Average neutrons per fission
- **Q_rec**: Recoverable energy per fission (MeV)
- **burnup**: Fuel burnup (GWd/MTU = gigawatt-days per metric ton uranium)
- **source**: Fission source strength (fissions/s)

### Individual Material Burnup (PRINT Table 211-219)

```
Individual Material Burnup
Material #: 1
step   duration (days)   time (days)   power fraction   burnup (GWd/MTU)
   0         0.000          0.000          0.5015             0.000
   1        50.000         50.000          0.5016             7.205
   2        10.000         60.000          0.5002             7.205  (no burn)
   3        50.000        110.000          0.5002            14.650
```

**power fraction** = Fission power in this material / Total fission power

### Isotope Inventory (PRINT Table 220)

```
actinide inventory for material 1 at end of step 1, time 50.000 (days), power 1.000 (MW)

no.  zaid      mass (gm)   activity (Ci)   spec.act. (Ci/gm)   atom den. (a/b-cm)   atom fr.   mass fr.
  1  90231     1.286E-09   6.837E-04       5.315E+05           8.718E-15            3.832E-13  3.723E-13
  2  90232     2.394E-08   2.625E-15       1.097E-07           1.616E-13            7.100E-12  6.929E-12
  3  92234     2.150E+01   1.324E-01       6.158E-03           1.438E-04            6.323E-03  6.227E-03
  4  92235     3.305E+02   7.131E-02       2.157E-04           2.201E-03            9.679E-02  9.574E-02
  5  92236     1.812E+01   1.176E-03       6.491E-05           1.202E-04            5.283E-03  5.247E-03
  6  92238     3.289E+03   1.097E-02       3.335E-06           2.174E-02            9.562E-01  9.524E-01
...
totals        3.455E+03   2.584E+05       7.479E+01           2.275E-02            1.000E+00  1.000E+00
```

**Columns**:
- **zaid**: Isotope ZAID (e.g., 92235 = U-235)
- **mass**: Mass (grams)
- **activity**: Radioactivity (Curies)
- **spec.act.**: Specific activity (Ci/g)
- **atom den.**: Atomic density (atoms/b-cm)
- **atom fr.**: Atom fraction (within actinides or FP group)
- **mass fr.**: Mass fraction

## Troubleshooting

### Problem: BURN card not recognized

**Cause**: MCNP6 version doesn't support burnup, or BURN not in data cards section.

**Fix**: Ensure MCNP6.2+ and BURN card is after geometry/materials.

### Problem: "material volume not specified"

**Cause**: Missing MATVOL keyword.

**Fix**:
```
BURN  ...
      MATVOL=50.27   $ Required for all burned materials
```

### Problem: "isotope has no cross section data"

**Cause**: Generated isotope (from CINDER) lacks MCNP cross section table.

**Fix**: Add to OMIT list.
```
OMIT  1, 8, <ZAID>   $ Add problem isotope to omit list
```

### Problem: Keff drops dramatically during burnup

**Causes**:
1. Fission product poisoning (Xe-135, Sm-149)
2. Fuel depletion (U-235 burned, replaced by Pu)
3. Insufficient fission product tiers (use tier -1 or -2)

**Fix**: Use appropriate fission product tier.
```
BOPT=1.0, -1   $ Tier 1 (includes Xe-135, Sm-149)
```

### Problem: Burnup calculation very slow

**Causes**:
1. Too many fission product tiers
2. Many time steps
3. Large number of materials

**Fix**:
```
c Reduce FP tier
BOPT=1.0, -1   $ Tier 1 (fast) instead of -3 or -4

c Fewer time steps
BURN  TIME=100, 200, 300   $ Instead of TIME=10,20,30,...,300

c Burn fewer materials
MAT=1   $ Instead of MAT=1 2 3 4 5
```

### Problem: Power fractions don't sum to 1.0

**Explanation**: Normal. Power fractions are calculated separately for each material based on fission rates.

**Verification**: Check PRINT Table 211-219 - sum of material power fractions should be ~1.0.

## Integration with Other Skills

### With mcnp-lattice-builder

Burn lattice fuels:
```
c Use lattice-builder to create 17×17 assembly
c Then burn with MATVOL = single_pin_volume × number_of_pins
BURN  MAT=1
      MATVOL=14528.03   $ 50.27 cm³ × 289 pins
```

### With mcnp-tally-analyzer

Extract isotopic inventory:
```python
from skills.output_analysis.mcnp_tally_analyzer import BurnupAnalyzer

analyzer = BurnupAnalyzer('output.o')

# Get isotopic inventory at step 3
inventory = analyzer.get_inventory(material=1, step=3)

# Get activity
activity = analyzer.get_activity(material=1, step=3, isotope='94239')  # Pu-239
```

### With mcnp-plotter

Visualize burnup evolution:
```python
from skills.visualization.mcnp_plotter import BurnupPlotter

plotter = BurnupPlotter('output.o')

# Plot keff vs time
plotter.plot_keff_evolution()

# Plot isotope buildup
plotter.plot_isotope_evolution(material=1, isotopes=['92235', '94239', '94241'])
```

## Best Practices

1. **Start simple**: Test with short times, Tier 0 (no FP), verify setup
2. **Use Tier 1 FP**: Good balance of speed and accuracy for routine work
3. **Specify volumes carefully**: MATVOL must match actual material volume
4. **OMIT list**: Always include common isotopes without cross sections
5. **Check keff**: Verify criticality evolution is physically reasonable
6. **Power normalization**: For reactor problems, use KCODE with fission power normalization
7. **Decay steps**: Use PFRAC=0 for cooling periods
8. **Lattices**: MATVOL = single volume × number of instances
9. **Verify output**: Check PRINT Table 210-220 for consistency
10. **Iterate**: Start coarse (few steps), refine (more steps, higher tier)
11. **Programmatic Burnup Setup**:
    - For automated BURN card generation and depletion chain setup, see: `mcnp_burnup_builder.py`
    - Useful for burnup step optimization, multi-region depletion scenarios, and fuel cycle analyses

## References

- **User Manual**: Chapter 3.4 - BURN Card
- **Examples**: Chapter 10.3.3 - Burning Multiple Materials in Repeated Structures
- **Theory Manual**: Depletion methodology
- **COMPLETE_MCNP6_KNOWLEDGE_BASE.md**: Burnup calculations
- **Related skills**: mcnp-lattice-builder, mcnp-tally-analyzer, mcnp-mesh-builder
