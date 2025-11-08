Union Operator Example - Two overlapping spheres
c
c Example demonstrating:
c   - Union operator (:) for OR logic
c   - Overlapping regions merged into single cell
c
c Cell Cards
c ==========
1    1  -10.0  -1 : -2  IMP:N=1    $ Inside sphere 1 OR sphere 2
2    0          1 2     IMP:N=0    $ Outside both

c Surface Cards
c ==============
1    S  -5 0 0  8.0    $ Sphere at (-5,0,0), R=8
2    S   5 0 0  8.0    $ Sphere at (5,0,0), R=8

c Data Cards
c ===========
MODE N
SDEF  POS=0 0 0  ERG=14.1
M1   26000  1.0
NPS  10000
