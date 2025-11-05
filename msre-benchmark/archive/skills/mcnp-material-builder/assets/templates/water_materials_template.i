Water Material Templates for MCNP
c ==================================================================
c Purpose: Demonstrate H2O and D2O material definitions
c          with proper S(alpha,beta) thermal scattering
c ==================================================================
c Cell Cards
1    1  -0.1003  -1  IMP:N=1  TMP=2.53e-8    $ Light water (H2O), 293.6 K
2    2  -0.110   -2  IMP:N=1  TMP=2.53e-8    $ Heavy water (D2O), 293.6 K
3    3  -0.08    -3  IMP:N=1  TMP=5.17e-8    $ Hot water (H2O), 600 K
4    0            4  IMP:N=0                 $ Void (graveyard)

c Surface Cards
1    SO  10.0                $ Sphere R=10 cm (light water)
2    SO  20.0                $ Sphere R=20 cm (heavy water shell)
3    SO  30.0                $ Sphere R=30 cm (hot water shell)
4    SO  100.0               $ Outer boundary

c Data Cards
MODE  N
c Material 1: Light Water (H2O) at 293.6 K
c Density: 1.0 g/cm3 → 0.1003 atoms/b-cm, M=18 g/mol
M1   1001.80c  2  8016.80c  1                        $ H2O: 2H + 1O (atomic)
MT1  H-H2O.40t                                        $ S(alpha,beta) at 293.6 K
c Material 2: Heavy Water (D2O) at 293.6 K
c Density: 1.1 g/cm3 → 0.110 atoms/b-cm, M=20 g/mol
M2   1002.80c  2  8016.80c  1                        $ D2O: 2D + 1O
MT2  D-D2O.40t                                        $ S(alpha,beta) for deuterium
c Material 3: Hot Light Water at 600 K
c Density: 0.8 g/cm3 (lower due to thermal expansion)
M3   1001.80c  2  8016.80c  1                        $ H2O at elevated temperature
MT3  H-H2O.43t                                        $ S(alpha,beta) at 600 K (MUST match TMP!)
SDEF  POS=0 0 0  ERG=1.0
NPS  10000
PRINT
