Box with Cylindrical Hole - Complement operator demonstration
c
c Example demonstrating:
c   - Complement operator (#) usage
c   - Boolean logic for complex cutouts
c   - Macrobody RPP vs primitive surfaces
c
c Cell Cards
c ==========
1    1  -10.0  -1 2 -3 4 -5 6 #10  IMP:N=1  VOL=7200  $ Box minus cylinder
2    0         -10               IMP:N=1              $ Cylinder void
3    0          1:-2:3:-4:5:-6   IMP:N=0              $ Graveyard
c Cylinder cell (referenced by #10)
10   0  -7 -5 6                  IMP:N=1              $ Cylinder geometry

c Surface Cards
c ==============
1    PX  -10.0                   $ Box boundaries
2    PX   10.0
3    PY  -10.0
4    PY   10.0
5    PZ  -20.0
6    PZ   20.0
7    CZ   3.0                    $ Cylinder radius

c Data Cards
c ===========
MODE N
SDEF  POS=0 0 0  ERG=14.1
M1   26000  1.0                  $ Iron
NPS  10000
