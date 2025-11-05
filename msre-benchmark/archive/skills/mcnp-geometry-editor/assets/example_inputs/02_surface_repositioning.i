Surface Repositioning - Moving Sphere from Origin
c
c Original geometry from mcnp-geometry-builder with sphere at origin
c EDITED: Changed SO (sphere at origin) to S (general sphere)
c         Repositioned to x=10 cm to avoid source region
c
c Cell Cards
c ==========
1    1  -1.0    -1        IMP:N=1  VOL=4188.79    $ Water sphere - repositioned
2    0          1  -2    IMP:N=1                  $ Air region
3    0          2         IMP:N=0                  $ Graveyard

c Surface Cards
c ==============
1    S  10 0 0  10.0      $ Sphere at (10,0,0) R=10 - was SO 10.0
2    SO   30.0            $ Problem boundary

c Data Cards
c ===========
MODE N
c Source at origin (sphere now offset)
SDEF  POS=0 0 0  ERG=1.0
c Material
M1   1001  2   8016  1    $ H2O
MT1  LWTR.01T              $ Light water S(a,b)
c Tally in moved sphere
F4:N  1
E4    0.01 0.1 1.0
NPS  100000
