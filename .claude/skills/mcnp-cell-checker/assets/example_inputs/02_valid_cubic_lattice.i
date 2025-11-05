Valid Cubic Lattice (LAT=1) - Cell Checker Example
c =================================================================
c Demonstrates correct LAT=1 specification with fill array
c 3x3x1 cubic lattice with proper dimension match
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0         -1      fill=10  IMP:N=1            $ Real world
100  0         -100    lat=1  u=10  IMP:N=1        $ Lattice cell
                       fill=-1:1 -1:1 0:0
                       1 1 1
                       1 2 1
                       1 1 1
200  1  -1.0  -200    u=1  IMP:N=1                 $ Pin type 1 (water)
300  2  -2.7  -300    u=2  IMP:N=1                 $ Pin type 2 (aluminum)
999  0         1           IMP:N=0                 $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                                     $ Outer boundary
100  RPP  -15 15 -15 15 0 10                       $ Lattice box
200  CZ   2.0                                      $ Pin 1 radius
300  CZ   2.0                                      $ Pin 2 radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                             $ Water
M2   13027  1.0                                    $ Aluminum
SDEF POS=0 0 5  ERG=1.0
F4:N 100
NPS  1000
PRINT
