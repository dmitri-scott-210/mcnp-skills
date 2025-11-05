Non-Uniform Scaling - Box Stretched in Z Direction
c
c Original geometry from mcnp-geometry-builder with cubic box
c EDITED: Changed RPP dimensions to stretch in z by factor 2x
c         Creates elongated geometry for beam study
c         Volume updated from 1000 to 2000 cm^3
c
c Cell Cards
c ==========
1    1  -1.0    -1       IMP:N=1  VOL=2000.0    $ Box - stretched in z
2    0          1  -2    IMP:N=1                 $ Void
3    0          2        IMP:N=0                 $ Graveyard

c Surface Cards
c ==============
1    RPP  -5 5  -5 5  -10 10    $ Box stretched: was -5 5  -5 5  -5 5
2    RPP  -20 20  -20 20  -25 25 $ Problem boundary

c Data Cards
c ===========
MODE N
c Beam source along z-axis
SDEF  POS=0 0 -15  AXS=0 0 1  EXT=0  ERG=1.0
c Material
M1   1001  2   8016  1    $ H2O
MT1  LWTR.01T
c Tallies (check flux distribution along z)
F4:N  1
FM4  -1 1 -6           $ Reaction rate tally
E4    0.01 0.1 1.0 10.0
NPS  500000
