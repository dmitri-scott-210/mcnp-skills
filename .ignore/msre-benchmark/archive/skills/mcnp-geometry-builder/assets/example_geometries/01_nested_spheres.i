Simple Nested Spheres - Three concentric spherical shells
c
c Example demonstrating:
c   - Basic cell definitions with material assignment
c   - Spherical surfaces (SO card)
c   - Simple intersection geometry (inside one, outside another)
c   - Graveyard cell with IMP:N=0
c
c Cell Cards
c ==========
1    1  -19.0   -1        IMP:N=1  VOL=33.51    $ Core (tungsten)
2    2  -10.5    1  -2    IMP:N=2  VOL=268.08   $ Shield 1 (lead)
3    3  -8.0     2  -3    IMP:N=4  VOL=636.67   $ Shield 2 (iron)
4    0           3  -4    IMP:N=4  VOL=1000.0   $ Void region
5    0           4         IMP:N=0                $ Graveyard

c Surface Cards
c ==============
1    SO   2.0            $ Core radius
2    SO   4.0            $ Shield 1 outer
3    SO   6.0            $ Shield 2 outer
4    SO   20.0           $ Problem boundary

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
