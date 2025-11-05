MSRE Benchmark - Zero Power First Critical (U-235, 33% enriched)
c =================================================================
c Molten Salt Reactor Experiment (ORNL, 1965-1969)
c Based on IRPhEP Benchmark: MSRE-MSR-RESR-001
c Configuration: Zero-power critical with homogenized core
c Generated from literature using MCNP Skills Framework
c Expected k-eff: 1.020 +/- 0.003 (2% high due to carbon XS)
c =================================================================
c Created: 2025-11-01
c MCNP Version: MCNP6.2
c =================================================================
c BLOCK 1: CELL CARDS
c =================================================================
c Cell structure (homogenized core approach):
c   100 - Core region (homogenized fuel-graphite)
c   200 - Lower plenum (void)
c   300 - Upper plenum (void)
c   400 - Vessel (Hastelloy-N)
c   999 - Outside world (graveyard)
c =================================================================
c --- Core Region (homogenized fuel-graphite) ---
100  1  -2.15    -100  102  -103       imp:n=1   $ Core: R=70.485, H=163.37 cm
c --- Lower Plenum (void below core) ---
200  0           -100  101  -102       imp:n=1   $ Lower plenum: H=12.954 cm
c --- Upper Plenum (void above core) ---
300  0           -100  103  -104       imp:n=1   $ Upper plenum: H=21.336 cm
c --- Hastelloy-N Vessel ---
400  3  -8.89    100  -105  101  -104  imp:n=1   $ Vessel wall: 2 cm thick
c --- Outside World (graveyard) ---
999  0           105:-101:104          imp:n=0   $ Graveyard (importance 0)

c =================================================================
c BLOCK 2: SURFACE CARDS
c =================================================================
c Cylindrical geometry (Z-axis vertical):
c   100 - Core radius (70.485 cm)
c   101 - Bottom of lower plenum (Z=0)
c   102 - Top of lower plenum / bottom of core (Z=12.954)
c   103 - Top of core (Z=12.954+163.37=176.324)
c   104 - Top of upper plenum (Z=197.66)
c   105 - Vessel outer radius (72.485 cm)
c =================================================================
100  CZ   70.485                                  $ Core radius
101  PZ   0.0                                     $ Bottom of lower plenum
102  PZ   12.954                                  $ Top of lower plenum (core bottom)
103  PZ   176.324                                 $ Top of core
104  PZ   197.660                                 $ Top of upper plenum
105  CZ   72.485                                  $ Vessel outer radius

c =================================================================
c BLOCK 3: DATA CARDS
c =================================================================
c --- Particle Mode ---
MODE  N
c --- Material 1: Homogenized Fuel-Graphite Core ---
c Composition: 22.5% fuel salt + 77.5% graphite by volume
c Fuel salt: LiF-BeF2-ZrF4-UF4 (65-29.1-5-0.9 mol%)
c   - Li-7 enriched to 99.99% (minimize parasitic absorption)
c   - U-235 enriched to 33%
c Graphite: CGB grade, 1.84 g/cm3
c Homogenized density: 0.225*2.27 + 0.775*1.84 = 1.937 g/cm3
c Temperature: 650C (923K) - using 800K thermal scattering (closest)
c =================================================================
M1   3007.70c  0.004862    $ Li-7 (22.5% of fuel salt value)
     4009.70c  0.002177    $ Be-9
     9019.70c  0.010982    $ F-19
     40090.70c 0.000374    $ Zr-90 (dominant isotope, 51%)
     92235.70c 0.000022    $ U-235 (33% enriched)
     92238.70c 0.000045    $ U-238 (67%)
     6000.70c  0.071448    $ C-12 (77.5% of graphite value)
MT1  grph.20t                                     $ Graphite thermal scattering
TMP1  7.95e-8                                     $ Temperature: 650C = 7.95e-8 MeV
c --- Material 2: Reserved for future use ---
c --- Material 3: Hastelloy-N Vessel ---
c Composition: 71% Ni, 16% Mo, 7% Cr, 5% Fe, 1% Mn
c Density: 8.89 g/cm3
c Temperature: 650C (923K)
c =================================================================
M3  28058.70c  0.067635    $ Ni-58 (68% abundant, approx for 71 wt% Ni)
     42098.70c 0.009336    $ Mo-98 (24% abundant, approx for 16 wt% Mo)
     24052.70c 0.007529    $ Cr-52 (84% abundant, approx for 7 wt% Cr)
     26056.70c 0.005008    $ Fe-56 (92% abundant, approx for 5 wt% Fe)
     25055.70c 0.001018    $ Mn-55 (100% abundant, 1 wt%)
TMP3  7.95e-8                                     $ Temperature: 650C
c --- Criticality Source ---
KCODE  5000  1.0  50  500                         $ 5000 neutrons, k-guess=1.0,
                                                   $ 50 skip, 500 active cycles
KSRC   0 0 90                                     $ Initial source at core center
       0 0 80
       0 0 100
       10 10 90
       -10 -10 90
c --- Physics and Cross-sections ---
c Using ENDF/B-VII.1 cross-sections (.80c)
c Thermal treatment for graphite (grph.80t)
c --- Output Control ---
PRINT
c --- Termination ---
c Runtime controlled by KCODE cycles (500 active)
