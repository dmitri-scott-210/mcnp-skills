MCNP Criticality Templates - KCODE, KSRC, and KOPTS
c ========================================================================
c Cell Cards
c ========================================================================
c ========================================================================
c TEMPLATE 1: Bare Sphere (Godiva-like)
c ========================================================================
c Uncomment for unreflected HEU sphere
c 1    1  -18.75   -1   IMP:N=1    $ U-235 metal sphere
c 2    0            1   IMP:N=0    $ Graveyard
c ========================================================================
c TEMPLATE 2: Water-Reflected Sphere
c ========================================================================
c Uncomment for water-reflected critical sphere
c 1    1  -18.75   -1   IMP:N=1    $ U-235 metal sphere (core)
c 2    2  -1.0   -2  1  IMP:N=1    $ Water reflector
c 3    0           2    IMP:N=0    $ Graveyard
c ========================================================================
c TEMPLATE 3: Multi-Region Assembly
c ========================================================================
c Example: Fuel-moderator-reflector configuration
1    1  -10.0    -1   IMP:N=1    $ Fuel region (UO2)
2    2  -1.0   -2  1  IMP:N=1    $ Moderator (water)
3    3  -2.7   -3  2  IMP:N=1    $ Reflector (aluminum)
4    0           3    IMP:N=0    $ Graveyard

c ========================================================================
c Surface Cards
c ========================================================================
1    SO  8.5                     $ Fuel sphere radius 8.5 cm
2    SO  20.0                    $ Moderator outer radius 20 cm
3    SO  25.0                    $ Reflector outer radius 25 cm

c ========================================================================
c Data Cards
c ========================================================================
MODE N
c ========================================================================
c Criticality Source Definition: KCODE Card
c ========================================================================
c KCODE nsrck rkk ikz kct
c   nsrck = number of source histories per cycle
c   rkk   = initial guess for k-eff (typically 1.0)
c   ikz   = number of cycles to skip before accumulating statistics
c   kct   = total number of cycles to run
c ========================================================================
c TEMPLATE 1: Basic KCODE (Small Problem)
c ========================================================================
KCODE  5000  1.0  50  150
c Run 150 cycles total, skip first 50, 5000 histories per cycle
c ========================================================================
c TEMPLATE 2: Production KCODE (Large Problem)
c ========================================================================
c KCODE  50000  1.0  100  500
c Run 500 cycles total, skip first 100, 50000 histories per cycle
c ========================================================================
c Initial Source Distribution: KSRC Card
c ========================================================================
c KSRC x1 y1 z1  x2 y2 z2  x3 y3 z3 ...
c Specify initial source points (at least 1 required)
c ========================================================================
c TEMPLATE 1: Single Point Source at Origin
c ========================================================================
KSRC  0 0 0
c ========================================================================
c TEMPLATE 2: Multiple Points Distributed in Fuel
c ========================================================================
c KSRC  0 0 0  5 0 0  -5 0 0  0 5 0  0 -5 0  0 0 5  0 0 -5
c Seven points: center + 6 on axes at radius 5 cm
c ========================================================================
c TEMPLATE 3: Grid of Points (3x3x3 = 27 points)
c ========================================================================
c KSRC  -4 -4 -4  -4 -4  0  -4 -4  4
c       -4  0 -4  -4  0  0  -4  0  4
c       -4  4 -4  -4  4  0  -4  4  4
c        0 -4 -4   0 -4  0   0 -4  4
c        0  0 -4   0  0  0   0  0  4
c        0  4 -4   0  4  0   0  4  4
c        4 -4 -4   4 -4  0   4 -4  4
c        4  0 -4   4  0  0   4  0  4
c        4  4 -4   4  4  0   4  4  4
c ========================================================================
c Advanced Criticality Options: KOPTS Card
c ========================================================================
c KOPTS keyword=value keyword=value ...
c Options: KINETICS=yes, PRECURSOR=yes, FMESH=yes, etc.
c ========================================================================
c TEMPLATE 1: Point Kinetics Parameters
c ========================================================================
c KOPTS  KINETICS=yes  PRECURSOR=yes
c Calculate fission matrix and delayed neutron precursors
c ========================================================================
c TEMPLATE 2: Mesh-Based Source
c ========================================================================
c KOPTS  FMESH=101
c Use mesh tally 101 for source convergence diagnostics
c ========================================================================
c Material Definitions
c ========================================================================
c ========================================================================
c Material 1: Fuel (10% enriched UO2, 10 g/cm3)
c ========================================================================
M1   92235.80c  -0.10   $ U-235 (10% enrichment)
     92238.80c  -0.90   $ U-238
     8016.80c   -0.12   $ Oxygen
c ========================================================================
c Material 2: Moderator (Light Water)
c ========================================================================
M2   1001.80c   2       $ Hydrogen
     8016.80c   1       $ Oxygen
MT2  H-H2O.40t          $ S(alpha,beta) thermal scattering
c ========================================================================
c Material 3: Reflector (Aluminum)
c ========================================================================
M3   13027.80c  1       $ Aluminum-27
c ========================================================================
c Tally Specifications
c ========================================================================
F4:N 1                           $ Flux in fuel region
E4   1e-10  1e-6  0.1  1  20    $ Energy bins (MeV)
F6:N 1                           $ Heating in fuel region
c ========================================================================
c Source Importance and Convergence
c ========================================================================
c IMP:N=1 in active regions ensures neutrons tracked everywhere
c Use PRDMP to print k-eff after each cycle for convergence monitoring
PRDMP  2J  -1                    $ Print k-eff each cycle
