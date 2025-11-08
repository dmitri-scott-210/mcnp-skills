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

---

## STRATEGIC CELL SELECTION FOR DEPLETION TRACKING

### The Fundamental Trade-Off

**Challenge**: Reactor models have 1,000s of cells, but tracking all cells is computationally prohibitive.

**Solution**: Strategic selection of ~100-200 cells that matter for physics.

### Cell Selection Criteria

**ALWAYS track these cell types**:

1. **Fuel Cells** (CRITICAL)
   - All fissile material regions
   - High flux regions (>1E13 n/cm²/s)
   - Spatial resolution: by assembly, axial zone, radial zone
   - Example: 72 fuel kernels in AGR-1 (6 capsules × 3 stacks × 4 compacts)

2. **Control Materials** (CRITICAL)
   - Burnable absorbers (B-10, Gd-155/157)
   - Control rods (Ag-In-Cd, B4C, hafnium)
   - Shim rods, safety rods
   - These burn out and change reactivity

3. **Structural Materials Near Core** (IMPORTANT)
   - Stainless steel (activation: Fe-55, Co-60, Mn-54)
   - Zircaloy cladding (activation products)
   - Graphite reflectors (C-14 production)
   - These become dose sources after shutdown

**MAY track if computationally feasible**:

4. **Moderator/Reflector Regions**
   - Graphite blocks near fuel
   - Water/heavy water in high flux
   - Beryllium reflectors

**DO NOT track**:

5. **Low-Flux Regions**
   - Outer reflectors (flux < 1E10 n/cm²/s)
   - Biological shields
   - External structures
   - Coolant far from core
   - Minimal physics impact, waste computational resources

### Cell Selection Methodology

**Step 1: Identify High-Flux Regions**
```mcnp
c Run initial MCNP calculation with F4 tallies
F4:n  100 101 102 103  $ Test cells
```

**Step 2: Rank by Flux Magnitude**
- Flux > 1E14 n/cm²/s: MUST track
- Flux 1E13-1E14 n/cm²/s: SHOULD track (fuel, absorbers)
- Flux 1E12-1E13 n/cm²/s: MAY track (structural)
- Flux < 1E12 n/cm²/s: DO NOT track

**Step 3: Group by Similarity**
- Cells with similar flux spectra can be grouped
- Reduces total tracked cells while preserving accuracy
- Example: 4 identical fuel assemblies → track 1, apply to all 4

### Example: AGR-1 Cell Selection

**Total model**: ~1,600 cells

**Tracked cells** (~150 total):
```
Fuel kernels (72 cells):
  - 6 capsules × 3 stacks × 4 compacts = 72 unique fuel regions
  - Each has different flux history → must track separately

Structural steel (30 cells):
  - Capsule walls, supports, holders
  - Activation products important for dose rates

Graphite (20 cells):
  - Spacers above/below compacts
  - C-14 production important

Borated graphite (10 cells):
  - Burnable poison holders
  - B-10 depletion affects reactivity

Hafnium shrouds (10 cells):
  - Control material
  - Hf-177 burnout critical

Coolant/void (0 cells):
  - Not tracked, minimal burnup
```

**Result**: ~10% of cells tracked, captures >99% of physics

---

## FISSION PRODUCT SELECTION

### Why Fission Products Matter

**Three Critical Impacts**:

1. **Reactivity Effects**
   - Strong absorbers poison the reactor (Xe-135, Sm-149, Gd-155/157)
   - Typical reactivity worth: -1000 to -5000 pcm

2. **Decay Heat**
   - Beta/gamma emission after shutdown
   - Safety-critical for cooling requirements

3. **Dose Rates**
   - Photon sources for shielding calculations
   - Decommissioning planning

### Systematic FP Selection Strategy

**TIER 1: ALWAYS Include (Strong Absorbers)**

```
Xe-135   (3.5 Mbarn thermal) - Peak ~9 hours after shutdown
Sm-149   (40 kbarn thermal) - Stable, builds up over time
Sm-151   (15 kbarn thermal) - Long-lived (90 yr)
Gd-155   (61 kbarn thermal) - Builds from Eu-155 decay
Gd-157   (254 kbarn thermal) - Strongest absorber
Pm-147   (Decays to Sm-147) - Precursor
Pm-149   (Decays to Sm-149) - Precursor
```

**TIER 2: SHOULD Include (Significant Absorbers)**

```
Cd-113   (20 kbarn thermal)
Eu-153   (312 barn thermal)
Eu-155   (3.7 kbarn thermal)
Rh-103   (150 barn thermal)
Tc-99    (20 barn thermal)
Cs-133   (30 barn thermal)
```

**TIER 3: MAY Include (Decay Heat/Dose)**

```
Cs-137   (Beta/gamma emitter, 30 yr half-life)
Sr-90    (Beta emitter, 29 yr)
Ba-140   (Gamma, short-lived)
La-140   (Gamma, 1.7 day)
Ce-141   (Gamma, 32 day)
Pr-143   (Beta, 13.6 day)
```

**TIER 4: Optional (Completeness)**

```
Kr-83    (Stable noble gas)
Xe-131   (Stable)
Xe-133   (5.2 day, dose important)
Mo-95    (Stable)
Ru-101   (Stable)
Nd-143   (Stable)
Nd-145   (Stable)
```

### MCNP Material Card Example

**Depleted fuel with FP tracking**:
```mcnp
m100  $ UO2 fuel after 3 cycles, cell 100
c Actinides
   92234.70c  5.873407E-06  $ U-234
   92235.70c  4.198373E-04  $ U-235 (depleted from fresh)
   92236.70c  1.517056E-05  $ U-236 (capture product)
   92238.70c  3.057844E-05  $ U-238
   93237.70c  1.886031E-07  $ Np-237
   94239.70c  3.962382E-07  $ Pu-239 (bred)
   94240.70c  3.184477E-08  $ Pu-240
   94241.70c  1.038741E-08  $ Pu-241
c TIER 1 FPs (strong absorbers)
   54135.70c  5.732034E-10  $ Xe-135 (equilibrium)
   62149.70c  2.657344E-08  $ Sm-149 (CRITICAL)
   62151.70c  7.853828E-08  $ Sm-151
   64155.70c  8.234521E-09  $ Gd-155
   64157.70c  1.440627E-10  $ Gd-157 (STRONGEST)
c TIER 2 FPs (significant absorbers)
   48113.70c  7.621751E-10  $ Cd-113
   63153.70c  1.027083E-07  $ Eu-153
   63155.70c  1.247127E-08  $ Eu-155
   45103.70c  3.635464E-07  $ Rh-103
   55133.70c  2.445752E-06  $ Cs-133
c TIER 3 FPs (decay heat, optional)
   55137.70c  1.234567E-06  $ Cs-137 (gamma source)
   38090.70c  9.876543E-07  $ Sr-90 (beta source)
c TIER 4 FPs (completeness, optional)
   36083.70c  2.749474E-07  $ Kr-83
   54131.70c  9.237888E-07  $ Xe-131
   42095.70c  9.415301E-08  $ Mo-95
   44101.70c  2.720314E-06  $ Ru-101
   60143.70c  1.325206E-06  $ Nd-143
   60145.70c  2.037404E-06  $ Nd-145
```

**Typical count**:
- Minimum: 7-10 isotopes (actinides + Tier 1 FPs)
- Standard: 20-30 isotopes (+ Tier 2)
- Comprehensive: 40-60 isotopes (+ Tier 3 + Tier 4)

---

## ACTINIDE CHAIN REQUIREMENTS

### Minimum Actinide Tracking

**ALWAYS include these 7 isotopes** (captures major chains):

```
U-234   - Decay product of Pu-238
U-235   - Primary fissile (if LEU/HEU)
U-236   - U-235 + n capture
U-238   - Primary fertile, Pu production
Np-237  - U-237 beta decay
Pu-239  - U-238 + n, primary bred fissile
Pu-240  - Pu-239 + n capture
Pu-241  - Pu-240 + n, fissile
```

### Extended Actinide Tracking

**For high-burnup or long-irradiation** (add these):

```
Pu-238  - Cm-242 alpha decay, heat source
Pu-242  - Pu-241 + n capture
Am-241  - Pu-241 beta decay (432 yr)
Am-242m - Am-241 + n, isomer
Am-243  - Am-242 + n or Pu-242 + n
Cm-242  - Am-241 + n + beta decay
Cm-243  - Pu-242 + n
Cm-244  - Cm-243 + n, spontaneous fission
Cm-245  - Cm-244 + n, fissile
```

### Capture/Decay Chains

**U-238 neutron capture chain**:
```
U-238 + n → U-239 (β⁻, 23 min) → Np-239 (β⁻, 2.4 day) → Pu-239
Pu-239 + n → Pu-240 + n → Pu-241 + n → Pu-242
```

**Am-241 production**:
```
Pu-241 (β⁻, 14 yr) → Am-241
Am-241 + n → Am-242m (β⁻) → Cm-242 (α, 163 day) → Pu-238
```

**Critical insight**: Must include precursors to get correct buildup!

### Example: Fresh vs. Depleted Fuel

**Fresh UO₂ (BOL - Beginning of Life)**:
```mcnp
m1  $ Fresh UO2, 4.5% enriched
   92234.70c  3.6e-4   $ Natural abundance in enriched U
   92235.70c  0.045    $ Enrichment
   92236.70c  2.1e-6   $ Trace from enrichment process
   92238.70c  0.955    $ Remainder
    8016.70c  2.0      $ Oxygen (stoichiometric)
```

**Depleted UO₂ (EOL - End of Life, 60 GWd/MTU)**:
```mcnp
m1  $ Depleted UO2 after ~3 cycles
c Uranium (depleted U-235, built up U-236)
   92234.70c  1.2e-4   $ Decreased
   92235.70c  0.008    $ Depleted from 4.5% → 0.8%
   92236.70c  0.005    $ Built up from captures
   92238.70c  0.940    $ Slightly decreased from fission
c Plutonium (bred from U-238)
   94238.70c  2.3e-5   $ From Cm-242 alpha decay
   94239.70c  0.006    $ Major bred fissile
   94240.70c  0.003    $ From Pu-239 captures
   94241.70c  0.002    $ Fissile, from Pu-240 captures
   94242.70c  8.0e-4   $ From Pu-241 captures
c Minor actinides
   93237.70c  6.0e-4   $ From U-237 decay chain
   95241.70c  1.0e-4   $ From Pu-241 beta decay
   95242.70c  2.0e-7   $ From Am-241 + n
   95243.70c  2.0e-5   $ From Pu-242 + n
   96242.70c  1.5e-6   $ From Am-241 + n chain
   96244.70c  8.0e-6   $ From Cm-243 + n
c Fission products (Tier 1 + Tier 2, 20+ isotopes)
   [... see Fission Product Selection section ...]
c Oxygen
    8016.70c  2.0      $ Approximately constant
```

---

## ORIGEN COUPLING WORKFLOW

### The Three-Step Process

**Production workflow from AGR-1/μHTGR**:

```
Step 1: MCNP Neutron Transport (Burnup Calculation)
  ├─ Calculate neutron flux in all cells
  ├─ Identify cells for depletion tracking (~150 cells)
  ├─ Extract cell-wise flux spectra
  └─ Output: Flux spectra, reaction rates → ORIGEN input

Step 2: ORIGEN Depletion Calculation
  ├─ Read MCNP flux/spectrum data
  ├─ Calculate isotopic evolution using Bateman equations
  ├─ Track actinides + fission products + activation products
  ├─ Apply operational history (power, time steps)
  └─ Output: Cell-wise isotopic inventories vs. time

Step 3: MCNP Photon Transport (Shutdown Dose Rate)
  ├─ Read ORIGEN isotopic inventories at decay time
  ├─ Generate photon source from decays (Ci → photons/sec)
  ├─ Define SDEF using isotopic distributions
  ├─ Calculate dose rates using F4:p + dose function
  └─ Output: 3D dose rate map for decommissioning
```

### MCNP → ORIGEN Data Handoff

**MCNP provides** (via BURN card or external coupling):
1. Cell-wise flux magnitude (n/cm²/s)
2. Energy spectrum (multi-group or continuous)
3. One-group cross-sections for major reactions
4. Irradiation time steps
5. Power normalization

**ORIGEN needs**:
1. One-group flux (or spectrum)
2. Fuel composition (actinides, initial enrichment)
3. Irradiation/decay times
4. Cross-section library (matched to spectrum)

### Manual ORIGEN Coupling (Step-by-Step)

**Step 1: Extract flux from MCNP**
```mcnp
F4:n  100  $ Cell 100 flux tally
E4    1e-10 20  $ Energy bins (thermal to fast)
```

MCNP output:
```
Cell 100 flux: 5.23e13 n/cm²/s
Spectrum: 40% thermal, 35% epithermal, 25% fast
```

**Step 2: Create ORIGEN input**
```
-1
RDA  Set title, library, flux
LIB 0 1 2 3 9 3 9 3 9  $ PWR library
TIT Fuel Cell 100 - Cycle 1
FLU 5.23e13  $ Flux from MCNP
HED 1 1 1   $ Headers
BAS 1.0e6   $ 1 MTU fuel basis
INP 1 1 1 0 0 0  $ Input options

Isotopic composition (from MCNP material m1):
  92234  3.6e-4
  92235  0.045
  92236  2.1e-6
  92238  0.955
   8016  2.0
  0 0 0

Irradiation steps (days):
IRP  100  3400  1  2  4  $ 100 days at 3400 MW
IRP  100  3400  1  2  4
IRP  100  3400  1  2  4
IRP  100  3400  1  2  4
IRP  100  3400  1  2  4
DEC  60   1  2  4  $ 60 day shutdown
...
END
```

**Step 3: Run ORIGEN**
```bash
origen < input_cell100.txt > output_cell100.txt
```

**Step 4: Extract isotopic inventory**

ORIGEN output (after 500 days irradiation + 30 days decay):
```
ISOTOPE  GRAMS   CURIES
U-234    1.2e2   6.2e-3
U-235    8.0e3   1.7e-2
U-236    5.0e3   3.2e-2
U-238    9.4e5   3.2e-1
Pu-239   6.0e3   3.7e2
Pu-240   3.0e3   6.8e2
Pu-241   2.0e3   2.1e5
...
Cs-137   1.2e3   8.7e4  $ Major gamma source
Sr-90    9.5e2   1.2e5
Sm-149   2.7e1   0.0    $ Stable absorber
```

**Step 5: Create MCNP photon source**
```mcnp
c Shutdown dose rate calculation
c Use ORIGEN isotopics as source

SDEF  CEL=D1  ERG=D2  PAR=2  $ Photon source, energy distribution

SI1  L  100 101 102 103  $ Source cells
SP1     0.25 0.25 0.25 0.25  $ Equal probability (adjust by activity)

c Energy distribution (from ORIGEN gamma spectrum)
SI2  H  0.05 0.1 0.2 0.5 1.0 2.0  $ MeV bins
SP2  D  0    1.2e15 3.4e15 5.6e15 2.1e15 0.8e15  $ Photons/sec per bin
```

### Multi-Cycle Calculations

**Challenge**: Compositions change each cycle, requiring iteration.

**Workflow**:
```
Cycle 1:
  1. MCNP with BOL compositions → flux
  2. ORIGEN with flux → EOC compositions
  3. Update MCNP materials to EOC
  4. Re-run MCNP → verify k_eff

Shutdown 1:
  5. ORIGEN decay (no flux) → compositions after 60 days

Cycle 2:
  6. MCNP with updated compositions → new flux
  7. ORIGEN with new flux → EOC compositions
  ...

Repeat for all cycles.
```

**Convergence**: Iterate until k_eff stable cycle-to-cycle.

---

## TIME-DEPENDENT OPERATIONAL HISTORY

### Power History Integration

**Real reactors have variable power**:
- Startup ramps
- Load following
- Forced outages
- Refueling shutdowns

**MCNP/ORIGEN approach**: Time-weighted averaging

**Example from AGR-1**:

**Raw operational data** (616 time steps over 138 days):
```
Time (h)  Power (MW)
0         3.2
2.5       5.1
5.0       6.8
...
138       4.9
```

**Time-weighted average**:
```python
ave_power = (power * time_interval).sum() / total_time
ave_power = 5.23 MW  # Representative for this cycle
```

**MCNP input**:
```mcnp
BURN  TIME=138  MAT=1  POWER=5.23  PFRAC=1.0
```

**Accuracy**: Typically within 5% of detailed time-step calculation.

### Control Rod History

**Control positions vary during cycle** (reactivity compensation):

**Example**: Outer Safety Control Cylinder (OSCC) rotation
```
Time (h)  Angle (°)
0         150  $ Withdrawn
24        125
48        100
...
138       60   $ Inserted
```

**Time-weighted average**:
```python
ave_angle = (angle * time_interval).sum() / total_time
ave_angle = 87.3°

# Find closest tabulated position
available = [0, 25, 40, 50, 60, 65, 75, 80, 85, 100, 120, 125, 150]
closest = 85°  # Use for MCNP geometry
```

**MCNP geometry update** (rotate surfaces for 85° position):
```mcnp
c OSCC surfaces rotated 85° from reference
1001  px  5.234   $ Calculated for 85° rotation
1002  py  3.876
...
```

---

## VALIDATION STRATEGIES

### Experimental Benchmark Data

**What to validate against**:

1. **Critical configurations**
   - k_eff for fresh core (should be ~1.000)
   - k_eff vs. burnup (reactivity loss)
   - Critical boron concentration (PWRs)

2. **Burnup measurements**
   - FIMA (Fissions per Initial Metal Atom)
   - Burnup monitors (Nd-148, Cs-137)
   - Isotopic assays (destructive analysis)

3. **Dose rate measurements**
   - Contact dose rates on fuel
   - Dose rates at detector locations
   - Time evolution (decay verification)

**AGR-1 example**:

Experimental data: MOAA_burnup_FIMA.csv
```
Capsule  Stack  Compact  FIMA_measured  FIMA_calculated  Difference
1        1      1        0.1123         0.1145           +1.96%
1        1      2        0.1089         0.1102           +1.19%
...
```

**Acceptance criteria**: Typically <5% difference for burnup, <20% for dose rates

### Code-to-Code Comparisons

**Cross-check with other codes**:

1. **MCNP vs. Serpent** (Monte Carlo)
2. **ORIGEN vs. SCALE** (depletion)
3. **MCNP vs. PARTISN** (deterministic transport)

**Example**:
```
k_eff comparison (fresh core):
  MCNP:    1.1834 ± 0.0012
  Serpent: 1.1842 ± 0.0010
  Difference: 80 pcm (within statistical uncertainty)
```

### Internal Consistency Checks

**Physics-based validation**:

1. **Reactivity balance**:
   - BOL k_eff - EOL k_eff = total burnup reactivity loss
   - Should equal: fissile depletion + FP buildup + Pu buildup

2. **Isotope mass balance**:
   - Total heavy metal mass approximately constant
   - Total actinide mass = initial U - fissioned U + bred Pu

3. **Power normalization**:
   - Fission energy × fission rate = reactor power
   - Verify MCNP power matches ORIGEN input

4. **Decay verification**:
   - Short-lived isotopes (I-135, Xe-135) approach zero during long shutdown
   - Long-lived isotopes (Pu-239, Cs-137) approximately constant

---

## COMPUTATIONAL COMPLEXITY MANAGEMENT

### The Scaling Problem

**Computational cost** scales roughly as:
```
CPU_time ∝ N_cells × N_isotopes × N_timesteps × N_iterations

Example:
  150 cells × 40 isotopes × 20 timesteps × 3 iterations
  = 360,000 ORIGEN runs (if brute-force approach)
```

**Production approach**: Intelligent reduction strategies

### Strategy 1: Cell Grouping by Flux

**Observation**: Cells with similar flux spectra have similar depletion.

**Approach**:
1. Run initial MCNP with many F4 tallies
2. Cluster cells by spectrum similarity
3. Track 1 representative cell per cluster
4. Apply results to all cells in cluster

**Example**:
```
Initial: 1000 fuel pins → 1000 tracked cells

After grouping:
  Cluster 1 (inner core, high flux): 120 pins → 1 tracked
  Cluster 2 (mid-core, medium flux): 450 pins → 1 tracked
  Cluster 3 (outer core, low flux): 380 pins → 1 tracked
  Cluster 4 (corner, lowest flux): 50 pins → 1 tracked

Result: 4 tracked cells instead of 1000 (250× reduction)
Error: <3% in k_eff, <8% in local burnup
```

### Strategy 2: Isotope Pruning

**Remove negligible isotopes**:

**Rule**: If atom density < 1E-15 atoms/barn-cm, omit from tracking.

**BURN card OMIT option**:
```mcnp
BURN  MAT=1  OMIT=54133 57140 58141 59143 61147 61149 61151
```

**Example**:
```
Initial: Tracking 250 fission products

After pruning:
  - Omit short-lived (t½ < 1 day) after equilibrium: -80 isotopes
  - Omit ultra-low abundance (<1E-15): -120 isotopes
  - Keep only: 50 isotopes

Result: 50 instead of 250 (5× reduction)
Error: <1% in k_eff (negligible isotopes have negligible impact)
```

### Strategy 3: Adaptive Time Stepping

**Variable time step sizing**:

```
BOL (0-100 days): 10-day steps (10 steps)
  - Rapid buildup of Pu, FPs
  - Fine resolution needed

Mid-life (100-400 days): 50-day steps (6 steps)
  - Approaching equilibrium
  - Coarser acceptable

EOL (400-500 days): 100-day steps (1 step)
  - Near equilibrium
  - Large steps acceptable

Shutdown (500-530 days): Variable
  - First 24 hours: 1-hour steps (24 steps)
  - Next 6 days: 1-day steps (6 steps)
  - After: exponential spacing

Total: 47 steps instead of uniform 100 (2× reduction)
```

### Strategy 4: Parallel Execution

**Cells are independent** → embarrassingly parallel

**Approach**:
```bash
# Split cells across compute nodes
node1: ORIGEN for cells 1-50
node2: ORIGEN for cells 51-100
node3: ORIGEN for cells 101-150
...

# Aggregate results
combine_results.py
```

**Speedup**: ~Linear with number of nodes (150 cells on 10 nodes = 15× faster)

---

## COMMON PITFALLS AND SOLUTIONS

### Pitfall 1: Tracking Too Many Cells

**Problem**: User tracks all 5,000 cells in model
```mcnp
BURN  MAT=1 2 3 4 ... 5000  $ Don't do this!
```

**Impact**:
- Runtime: weeks or months
- Memory: exhausted
- Output files: terabytes
- Minimal physics benefit

**Solution**: Strategic selection (~150 cells)
```mcnp
BURN  MAT=101 102 103 ... 250  $ Fuel cells only
     MAT=301 302 ... 330        $ Structural near core
     MAT=401 402 ... 410        $ Control materials
```

### Pitfall 2: Missing Critical Fission Products

**Problem**: User omits Sm-149 from tracking

**Impact**:
- k_eff too high by 2000-3000 pcm
- Reactivity predictions completely wrong
- Cycle length miscalculated

**Solution**: Always include TIER 1 FPs (Xe-135, Sm-149, Gd-155/157)

### Pitfall 3: Incorrect Volume Normalization

**Problem**: Volume in BURN card doesn't match actual cell volume

**Example**:
```
Cell volume: 1.5e5 cm³ (correct)
BURN MATVOL: 1.5e4 cm³ (wrong - off by 10×)

Result:
  - Atom densities wrong by 10×
  - Reactivity wrong
  - Isotope masses wrong
```

**Solution**: Calculate volumes carefully
```python
import numpy as np

r = 0.41  # cm, fuel radius
h = 365   # cm, fuel height
vol = np.pi * r**2 * h
print(f"Volume: {vol:.2e} cm³")
```

### Pitfall 4: Time Step Too Coarse

**Problem**: Single 500-day time step for entire cycle

**Impact**:
- Miss Xe-135 transients
- Miss Sm-149 buildup dynamics
- Flux-weighted averages incorrect

**Solution**: 50-100 day intervals during irradiation

### Pitfall 5: Forgetting Decay Periods

**Problem**: Continuous irradiation assumed, no shutdowns

**Impact**:
- Short-lived FPs too high (I-135, Xe-135)
- Dose rates immediately after shutdown too high
- Unrealistic operational history

**Solution**: Explicit decay steps
```mcnp
BURN  TIME=500  POWER=3400  $ Cycle 1
BURN  TIME=560  POWER=0     $ 60-day shutdown
BURN  TIME=1060 POWER=3400  $ Cycle 2
```

---

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
