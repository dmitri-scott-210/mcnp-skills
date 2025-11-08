Macrobody Example - RPP and RCC demonstration
c
c Example demonstrating:
c   - Macrobody usage (RPP, RCC)
c   - Macrobody facet references (.1, .2, etc.)
c   - When to use macrobodies vs primitive surfaces
c
c Cell Cards
c ==========
1    1  -10.0  -1  IMP:N=1    $ Box (RPP macrobody)
2    2  -8.0   -2  IMP:N=1    $ Cylinder (RCC macrobody)
3    0          1 2  IMP:N=0  $ Graveyard

c Surface Cards
c ==============
1    RPP  -10 10  -10 10  0 20    $ Rectangular parallelepiped
2    RCC  0 0 30  0 0 10  5      $ Right circular cylinder

c Data Cards
c ===========
MODE N
SDEF  POS=0 0 10  ERG=14.1
M1   26000  1.0
M2   82000  1.0
NPS  10000
