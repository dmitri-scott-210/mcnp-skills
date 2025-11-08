KCODE Criticality Calculation - Water-Reflected UO2 Sphere
c =================================================================
c Example demonstrating:
c   - KCODE criticality source
c   - KSRC initial source distribution
c   - Water-reflected enriched UO2 fuel
c   - K-effective calculation
c =================================================================
c Cell Cards
c =================================================================
1    1  -10.0   -1   IMP:N=1  VOL=3054      $ UO2 fuel sphere (10% enriched)
2    2  -1.0    -2  1 IMP:N=1  VOL=29845    $ Water reflector
3    0           2   IMP:N=0                $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  9.0                                $ Fuel boundary
2    SO  20.0                               $ Reflector outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE N
c --- Criticality Source Definition ---
KCODE  10000  1.0  50  200                  $ 10k/cycle, k_init=1.0, skip 50, run 200
KSRC   0 0 0  5 0 0  -5 0 0  0 5 0  0 -5 0 $ Initial source points in fuel
c --- Material Definitions ---
M1   92235.80c  -0.10                       $ U-235 (10% enrichment)
     92238.80c  -0.90                       $ U-238
     8016.80c   -0.12                       $ Oxygen (UO2)
M2   1001.80c   2                           $ Hydrogen (water)
     8016.80c   1                           $ Oxygen
MT2  H-H2O.40t                              $ Thermal scattering for water
c --- Tally Definitions ---
F4:N 1                                      $ Flux in fuel
E4   1e-10  1e-6  0.01  0.1  1  10  20     $ Energy bins (MeV)
F6:N 1                                      $ Heating in fuel (MeV/g)
c --- Output Control ---
PRDMP  2J  -1                               $ Print k-eff each cycle
