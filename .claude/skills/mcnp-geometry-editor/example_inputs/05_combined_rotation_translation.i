Combined Rotation and Translation - Fuel Pin Assembly
c
c Original geometry from mcnp-geometry-builder with vertical fuel pin
c EDITED: Added TR3 to rotate pin 30 degrees about y-axis and move to (10,0,0)
c         Simulates tilted fuel pin in experimental setup
c
c Cell Cards
c ==========
1    1  -10.2   -1       TRCL=3  IMP:N=1  VOL=31.42   $ Fuel - transformed
2    2  -6.5     1 -2    TRCL=3  IMP:N=1  VOL=94.25   $ Clad - transformed
3    3  -1.0     2 -10   IMP:N=1                      $ Water moderator
4    0           10      IMP:N=0                      $ Graveyard

c Surface Cards
c ==============
1    RCC  0 0 -5  0 0 10  0.5    $ Fuel cylinder in TR3 system
2    RCC  0 0 -5  0 0 10  0.7    $ Clad cylinder in TR3 system
10   RPP  -20 20  -20 20  -20 20 $ Problem boundary

c Data Cards
c ===========
MODE N
c Transformation: 30 deg about y + translate to (10,0,0)
*TR3  10 0 0  0 30 0  1   $ Combined rotation and translation
c Source (uniform in moderator)
SDEF  CEL=3  POS=FCEL  ERG=0.0253
c Materials
M1   92235 -0.9  92238 -0.1       $ Enriched UO2 fuel (simplified)
M2   40000  1.0                    $ Zircaloy clad (Zr)
M3   1001  2   8016  1             $ H2O
MT3  LWTR.01T
c Tally
F4:N  1 2
NPS  100000
