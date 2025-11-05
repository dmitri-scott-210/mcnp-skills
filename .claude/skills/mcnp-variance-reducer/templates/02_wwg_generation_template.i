Weight Window Generation Template (WWG Stage 1)
c
c =================================================================
c Cell Cards
c =================================================================
c
1  1  -1.0    -1         IMP:N=1     $ Source region
2  2  -7.8    1 -2       IMP:N=1     $ Shield 1
3  3  -11.3   2 -3       IMP:N=1     $ Shield 2
4  0         3 -4       IMP:N=1     $ Detector region
999  0       4          IMP:N=0     $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
c
1  SO  10                          $ Source sphere
2  SO  30                          $ Shield 1 outer
3  SO  50                          $ Shield 2 outer
4  SO  60                          $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c
MODE  N
c
c --- Spatial mesh for importance ---
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-60 -60 -60
      IMESH=60  IINTS=12
      JMESH=60  JINTS=12
      KMESH=60  KINTS=12
c
c --- Energy bins for weight windows ---
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c --- Point detector ---
F5:N  55 0 0  0.5
c
c --- Generate weight windows from F5 tally ---
WWG  5  0  1.0
c    ^tally ^mesh ^target
c
c --- Materials ---
M1  1001  2  8016  1               $ Water
M2  26000  1                       $ Iron
M3  82000  1                       $ Lead
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- Moderate statistics for WWG generation ---
NPS  1e5
c
c OUTPUT: wwout file (use in Stage 2 production run)
