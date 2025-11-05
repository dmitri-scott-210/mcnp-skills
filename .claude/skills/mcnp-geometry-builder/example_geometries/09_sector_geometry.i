Angular Sector - Quarter-cylinder demonstration
c
c Example demonstrating:
c   - Angular sectors using planes
c   - Symmetric geometry modeling
c   - Reflecting boundaries
c
c Cell Cards
c ==========
1    1  -10.0  -1 -2 3 4  IMP:N=1  $ Quarter cylinder (0-90 degrees)
2    0          1:2:-3:-4  IMP:N=0  $ Graveyard

c Surface Cards
c ==============
1    CZ  10.0         $ Cylinder radius
2    PZ  20.0         $ Top
3    PZ  0.0          $ Bottom
4    P   1 0 0  0     $ Plane at X=0 (YZ plane)
5    P   0 1 0  0     $ Plane at Y=0 (XZ plane) - not used but shows concept

c Data Cards
c ===========
MODE N
SDEF  POS=5 5 10  ERG=14.1
M1   26000  1.0
NPS  10000
