c ================================================================
c Multi-Zone Core Burnup Example
c
c Purpose: Demonstrate strategic cell selection and radial power distribution
c Model: 3-zone reactor core with differential burnup
c Zones: Inner (high flux), Middle (medium flux), Outer (low flux)
c
c Based on: AGR-1 cell selection methodology (150 cells from 1600)
c Production practice: Track ~10% of cells, capture >99% of physics
c ================================================================

c ----------------------------------------------------------------
c CELL CARDS
c ----------------------------------------------------------------
c Core divided into 3 radial zones + structural materials

c --- ZONE 1: Inner Core (High Flux) ---
1  1  -10.4  -1  IMP:N=1  VOL=500.0    $ Inner fuel (high power)
2  2  -6.5    1 -2  IMP:N=1            $ Inner clad

c --- ZONE 2: Middle Core (Medium Flux) ---
3  3  -10.4  -3  2  IMP:N=1  VOL=800.0 $ Middle fuel
4  4  -6.5    3 -4  IMP:N=1            $ Middle clad

c --- ZONE 3: Outer Core (Low Flux) ---
5  5  -10.4  -5  4  IMP:N=1  VOL=1200.0 $ Outer fuel (low power)
6  6  -6.5    5 -6  IMP:N=1             $ Outer clad

c --- Structural Materials (Near Core) ---
7  7  -7.9   -7  6  IMP:N=1  VOL=300.0  $ SS-316 core barrel (activation)
8  8  -1.65  -8  7  IMP:N=1  VOL=2000.0 $ Graphite reflector (C-14)

c --- Control Rod (Burnable Absorber) ---
9  9  -1.77  -9  IMP:N=1  VOL=150.0    $ Borated graphite holder

c --- Coolant ---
10 10 -0.74  -10 8 9  IMP:N=1          $ Water coolant/moderator

c --- Outside ---
11 0   10  IMP:N=0                     $ Void

c ----------------------------------------------------------------
c SURFACE CARDS
c ----------------------------------------------------------------
c Concentric cylindrical zones (Z-axis aligned)

1  CZ   5.0   $ Inner fuel outer radius
2  CZ   5.5   $ Inner clad outer
3  CZ  10.0   $ Middle fuel outer
4  CZ  10.5   $ Middle clad outer
5  CZ  15.0   $ Outer fuel outer
6  CZ  15.5   $ Outer clad outer
7  CZ  18.0   $ Core barrel outer
8  CZ  25.0   $ Graphite reflector outer
9  CZ   2.0   $ Control rod radius
10 CZ  30.0   $ Coolant boundary

c ----------------------------------------------------------------
c DATA CARDS
c ----------------------------------------------------------------

c ================================================================
c MATERIAL CARDS (Fresh fuel - Beginning of Life)
c ================================================================

c --- Zone 1: Inner Fuel (same composition, different burnup) ---
M1  $ Fresh UO2, 4.5% enriched, zone 1
   92234.70c  3.600E-04
   92235.70c  4.500E-02
   92236.70c  2.100E-06
   92238.70c  9.550E-01
    8016.70c  2.000E+00

c --- Zone 1: Inner Clad ---
M2  $ Zircaloy-4
   40000.60c  0.98
   26000.50c  0.002
   24000.50c  0.001
   28000.50c  0.001

c --- Zone 2: Middle Fuel (identical to M1 initially) ---
M3  $ Fresh UO2, 4.5% enriched, zone 2
   92234.70c  3.600E-04
   92235.70c  4.500E-02
   92236.70c  2.100E-06
   92238.70c  9.550E-01
    8016.70c  2.000E+00

c --- Zone 2: Middle Clad ---
M4  $ Zircaloy-4
   40000.60c  0.98
   26000.50c  0.002
   24000.50c  0.001
   28000.50c  0.001

c --- Zone 3: Outer Fuel (identical to M1 initially) ---
M5  $ Fresh UO2, 4.5% enriched, zone 3
   92234.70c  3.600E-04
   92235.70c  4.500E-02
   92236.70c  2.100E-06
   92238.70c  9.550E-01
    8016.70c  2.000E+00

c --- Zone 3: Outer Clad ---
M6  $ Zircaloy-4
   40000.60c  0.98
   26000.50c  0.002
   24000.50c  0.001
   28000.50c  0.001

c --- Material 7: Stainless Steel 316L (Core Barrel) ---
M7  $ SS-316L, density = 7.9 g/cm³
c Isotopic composition for activation tracking
   26054.70c  0.038      $ Fe-54
   26056.70c  0.604      $ Fe-56 (dominant)
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

c --- Material 8: Graphite Reflector ---
M8  $ Pure graphite, density = 1.65 g/cm³
    6012.00c  0.989      $ C-12 (98.9%)
    6013.00c  0.011      $ C-13 (1.1%)
MT8  grph.10t            $ Graphite thermal scattering (CRITICAL!)

c --- Material 9: Borated Graphite (Burnable Absorber) ---
M9  $ Borated graphite, 6% B, density = 1.77 g/cm³
    6012.00c  8.430E-02  $ C-12 (matrix)
    5010.20c  1.080E-03  $ B-10 (19.8% of boron, STRONG absorber)
    5011.00c  4.348E-03  $ B-11 (80.2% of boron)
MT9  grph.10t            $ Graphite thermal scattering

c --- Material 10: Light Water ---
M10 $ H2O, density = 0.74 g/cm³
    1001.70c  2.0
    8016.70c  1.0
MT10 lwtr.10t

c ================================================================
c SOURCE DEFINITION
c ================================================================

KCODE  10000  1.0  50  150
KSRC  0 0 0  7 0 0  -7 0 0  0 12 0  0 -12 0  $ 5 source points

c ================================================================
c BURNUP SPECIFICATION (Multi-Zone with Different Power Fractions)
c ================================================================

c CRITICAL FEATURE: MCNP automatically calculates power fractions
c based on fission rate in each material. We specify materials to
c burn and total reactor power.

c Strategy: Track 6 cells (3 fuel zones + structural + graphite + absorber)
c Total: 6 materials tracked out of 11 cells
c Percentage: 55% tracked (high for demonstration, normally ~10%)

c Single-cycle burnup: 540 days
BURN  TIME=100 200 300 400 500 540
      POWER=3400                     $ Total core power (MW)
      PFRAC=1.0                      $ Continuous operation
      MAT=1 3 5 7 8 9                $ Burn: Inner fuel, Middle fuel, Outer fuel,
                                     $       SS barrel, Graphite, Borated graphite
      MATVOL=500.0 800.0 1200.0 300.0 2000.0 150.0  $ Volumes (cm³)
      BOPT=1.0, -2, 1                $ Q=1.0, Tier 2 FPs (higher fidelity)

c ================================================================
c OMIT CARDS (One for each burned material)
c ================================================================

OMIT  1, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244  $ Inner fuel
      3, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244  $ Middle fuel
      5, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244  $ Outer fuel
      7, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244  $ SS barrel
      8, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244  $ Graphite
      9, 8, 6014, 7016, 8018, 9018, 90234, 91232, 95240, 95244  $ Borated graphite

c ================================================================
c OUTPUT CONTROL
c ================================================================

PRINT  110 126 210 211 212 213 214 215  $ Detailed burnup output

c PRINT 210: Overall burnup summary
c PRINT 211-215: Individual material burnup (M1, M3, M5, M7, M8)

c ================================================================
c EXPECTED RESULTS
c ================================================================

c Power Fractions (MCNP will calculate, typical values):
c   Inner zone (M1):  ~45% (highest flux, smallest volume)
c   Middle zone (M3): ~35% (medium flux, medium volume)
c   Outer zone (M5):  ~20% (lowest flux, largest volume)
c   Total fuel power: 100% (structural materials don't fission)

c Differential Burnup:
c   Inner zone: ~60 GWd/MTU (highest specific power)
c   Middle zone: ~45 GWd/MTU
c   Outer zone: ~25 GWd/MTU (lowest specific power)

c Activation Products (SS barrel):
c   Fe-55: X-ray source (2.7 yr half-life)
c   Co-60: Dominant γ source (5.27 yr, 1.17 & 1.33 MeV)
c   Mn-54: Short-term γ source (312 day)

c C-14 Production (Graphite):
c   From C-13(n,γ)C-14 and O-17(n,α)C-14
c   Long-lived β emitter (5730 yr)
c   Important for waste disposal classification

c Burnable Absorber (Borated graphite):
c   BOL: Strong negative reactivity (-3000 to -5000 pcm)
c   B-10 depletion: Linear with flux × time
c   EOL: Mostly depleted, small residual poison

c ================================================================
c CELL SELECTION RATIONALE
c ================================================================

c TRACKED (6 materials):
c   1. Inner fuel (M1):  HIGH PRIORITY - High flux, max burnup
c   2. Middle fuel (M3): HIGH PRIORITY - Significant power fraction
c   3. Outer fuel (M5):  HIGH PRIORITY - Completes radial profile
c   4. SS barrel (M7):   MEDIUM PRIORITY - Activation for dose rates
c   5. Graphite (M8):    LOW PRIORITY - C-14 production tracking
c   6. Borated C (M9):   HIGH PRIORITY - Burnable poison depletion

c NOT TRACKED (5 materials):
c   - Clad materials (M2, M4, M6): Low importance, minimal activation
c   - Water (M10): Transient activation only (N-16, short-lived)
c   - Void (M11): No material to burn

c This demonstrates STRATEGIC CELL SELECTION:
c - Track high-importance cells (fuel, absorbers, structural near core)
c - Skip low-importance cells (clad, coolant)
c - Result: 55% of cells tracked, >95% of physics captured

c Production reactors: Track ~10% of cells (e.g., 150 from 1600 in AGR-1)

c ================================================================
c VALIDATION CHECKS (Post-Run)
c ================================================================

c 1. Power Fraction Sum:
c    Check PRINT Table 211-215: Sum of material power fractions ≈ 1.0
c    Typical tolerance: ±0.01

c 2. Reactivity Trend:
c    k_eff should decrease monotonically with burnup
c    BOL: ~1.25-1.30, EOL: ~1.00-1.05

c 3. Differential Burnup:
c    Inner zone burnup > Middle zone > Outer zone
c    Ratio: Inner/Outer ≈ 2-3× (depends on flux profile)

c 4. B-10 Depletion:
c    Check M9 (borated graphite) B-10 atom density vs. time
c    Should decrease to ~10-20% of initial by EOL

c 5. Activation Products:
c    Check M7 (SS-316) for Co-60, Fe-55, Mn-54
c    Co-60 should be dominant γ source after ~1 year decay

c ================================================================
c USAGE NOTES
c ================================================================

c 1. To run this input:
c    mcnp6 i=core_burnup_multizone.i o=core_burnup_multizone.o

c 2. Runtime estimate (single 3.0 GHz core):
c    ~2-4 hours (6 materials, 6 time steps, Tier 2 FPs)

c 3. Memory requirement:
c    ~1-2 GB (moderate complexity)

c 4. Post-processing:
c    Extract power fractions: grep "power fraction" output.o
c    Extract burnup: grep "burnup" output.o
c    Extract k_eff: grep "keff" output.o

c 5. Extension to full core:
c    - Use lattice fills for repeated assemblies
c    - Group similar assemblies (same enrichment, position)
c    - Scale to ~100-200 tracked materials for production core

c ================================================================
c END OF INPUT
c ================================================================
