Example 02 AFTER: Fill Array Dimension Mismatch FIXED
c =================================================================
c Fixed version: Added missing row to fill array.
c Declaration: -2:2 -2:2 0:0 = 5×5×1 = 25 values
c Now provides all 25 values (5 rows × 5 columns)
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0   -1        FILL=1  IMP:N=1       $ Fill with lattice
100  0   -100      U=1  LAT=1  FILL=-2:2 -2:2 0:0  IMP:N=1
    10 10 10 10 10
    10 20 20 20 10
    10 20 30 20 10
    10 20 20 20 10
    10 10 10 10 10
c     ^ Added missing 5th row (FIXED)
1000 1  -10.5  -1000  U=10  IMP:N=1      $ Fuel (u=10)
1100 2  -6.5   -1100  U=20  IMP:N=1      $ Reflector (u=20)
1200 3  -8.0   -1200  U=30  IMP:N=1      $ Control rod (u=30)
1300 0   1300         IMP:N=0            $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                            $ Outer sphere
100  RPP  -5 5 -5 5 0 2                  $ Lattice boundary
1000 CZ   0.4                             $ Fuel radius
1100 CZ   0.45                            $ Reflector radius
1200 CZ   0.5                             $ Control rod radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   92235.80c  0.05  92238.80c  0.95  8016.80c  2.0
M2   6000.80c  1.0
M3   94239.80c  1.0
SDEF  POS=0 0 0  ERG=2.0
F4:N  1
NPS   10000
PRINT

