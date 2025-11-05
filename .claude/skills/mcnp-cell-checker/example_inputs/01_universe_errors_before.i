Example 01 BEFORE: Undefined Universe References
c =================================================================
c This input has undefined universe references that will cause
c MCNP fatal error. Cell 100 references fill=50 but u=50 is not
c defined anywhere in the input.
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0   -1        FILL=1  IMP:N=1       $ Fill with universe 1
100  0   -100      U=1  LAT=1  FILL=-1:1 -1:1 0:0  IMP:N=1
    10 10 10
    10 50 10
    10 10 10
c     ^ u=50 referenced but NOT defined
1000 1  -10.5  -1000  U=10  IMP:N=1      $ Fuel pin (u=10 defined)
1001 0   1000         IMP:N=0            $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                            $ Outer sphere
100  RPP  -3 3 -3 3 0 6                  $ Lattice boundary
1000 CZ   0.5                             $ Fuel pin

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   92235.80c  0.05  92238.80c  0.95  8016.80c  2.0
SDEF  POS=0 0 0  ERG=2.0
F4:N  1
NPS   10000
PRINT

