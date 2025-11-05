Uniform Scaling - Nested Spheres Scaled 1.5x from geometry-builder
c
c Original geometry from mcnp-geometry-builder nested spheres example
c EDITED: All dimensions scaled by factor 1.5
c   Original R: 2, 4, 6, 20 cm
c   Scaled R:   3, 6, 9, 30 cm
c   Volumes updated (factor 1.5^3 = 3.375)
c
c Cell Cards
c ==========
1    1  -19.0   -1        IMP:N=1  VOL=113.10     $ Core (tungsten) - was 33.51
2    2  -10.5    1  -2    IMP:N=2  VOL=904.78     $ Shield 1 (lead) - was 268.08
3    3  -8.0     2  -3    IMP:N=4  VOL=2148.76    $ Shield 2 (iron) - was 636.67
4    0           3  -4    IMP:N=4  VOL=3375.00    $ Void region - was 1000.0
5    0           4         IMP:N=0                 $ Graveyard

c Surface Cards
c ==============
1    SO   3.0            $ Core radius (scaled from 2.0)
2    SO   6.0            $ Shield 1 outer (scaled from 4.0)
3    SO   9.0            $ Shield 2 outer (scaled from 6.0)
4    SO   30.0           $ Problem boundary (scaled from 20.0)

c Data Cards
c ===========
MODE N
c Point isotropic source at origin
SDEF  POS=0 0 0  ERG=14.1
c Materials
M1   74000  1.0           $ Tungsten (W)
M2   82000  1.0           $ Lead (Pb)
M3   26000  1.0           $ Iron (Fe)
NPS  10000
