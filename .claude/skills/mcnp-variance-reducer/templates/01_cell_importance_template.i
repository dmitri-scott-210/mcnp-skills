Cell Importance Variance Reduction Template
c
c =================================================================
c Cell Cards
c =================================================================
c
1  1  -1.0    -1         IMP:N=1     $ Source region
2  2  -7.8    1 -2       IMP:N=2     $ Shield 1
3  3  -11.3   2 -3       IMP:N=4     $ Shield 2
4  4  -2.7    3 -4       IMP:N=8     $ Shield 3
5  0         4 -5       IMP:N=16    $ Detector region
999  0       5          IMP:N=0     $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
c
1  SO  10                          $ Source sphere
2  SO  30                          $ Shield 1 outer
3  SO  50                          $ Shield 2 outer
4  SO  70                          $ Shield 3 outer
5  SO  80                          $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c
MODE  N
c
c --- Materials ---
M1  1001  2  8016  1               $ Water (source region)
M2  26000  1                       $ Iron (shield 1)
M3  82000  1                       $ Lead (shield 2)
M4  13027  1                       $ Aluminum (shield 3)
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1          $ 14.1 MeV neutron at origin
c
c --- Detector tally ---
F4:N  5                            $ Flux in detector region
c
c --- Simulation control ---
NPS  1e6
