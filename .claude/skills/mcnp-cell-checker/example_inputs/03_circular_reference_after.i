Example 03 AFTER: Circular Universe Reference FIXED
c =================================================================
c Fixed version: Broke circular dependency by making u=3 terminal.
c Now: u=1 → u=2 → u=3 (linear hierarchy, u=3 has material)
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0   -1        FILL=1  IMP:N=1       $ Fill with u=1
100  0   -100      U=1  FILL=2  IMP:N=1  $ u=1 fills u=2
200  0   -200      U=2  FILL=3  IMP:N=1  $ u=2 fills u=3
300  1  -10.5  -300   U=3  IMP:N=1       $ u=3 terminal (has material, FIXED)
999  0   999       IMP:N=0               $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                            $ Outer sphere
100  SO   40.0                            $ u=1 boundary
200  SO   30.0                            $ u=2 boundary
300  SO   20.0                            $ u=3 boundary (fuel sphere)
999  SO   60.0                            $ Graveyard boundary

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   92235.80c  0.05  92238.80c  0.95  8016.80c  2.0  $ Fuel (ADDED)
SDEF  POS=0 0 0  ERG=2.0
F4:N  1
NPS   10000
PRINT

