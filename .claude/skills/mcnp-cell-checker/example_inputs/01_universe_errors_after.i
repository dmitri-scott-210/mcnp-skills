Example 01 AFTER: Undefined Universe References FIXED
c =================================================================
c Fixed version: Added definition for universe 50 that was
c referenced in the fill array but not defined.
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0   -1        FILL=1  IMP:N=1       $ Fill with universe 1
100  0   -100      U=1  LAT=1  FILL=-1:1 -1:1 0:0  IMP:N=1
    10 10 10
    10 50 10
    10 10 10
c     ^ u=50 now defined below
1000 1  -10.5  -1000  U=10  IMP:N=1      $ Standard fuel pin (u=10)
1500 2  -11.0  -1500  U=50  IMP:N=1      $ Control rod fuel (u=50 ADDED)
1501 0   1500         IMP:N=0            $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                            $ Outer sphere
100  RPP  -3 3 -3 3 0 6                  $ Lattice boundary
1000 CZ   0.5                             $ Fuel pin radius
1500 CZ   0.6                             $ Control rod radius (ADDED)

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   92235.80c  0.05  92238.80c  0.95  8016.80c  2.0
M2   92235.80c  0.10  92238.80c  0.90  8016.80c  2.0  $ Control rod (ADDED)
SDEF  POS=0 0 0  ERG=2.0
F4:N  1
NPS   10000
PRINT

