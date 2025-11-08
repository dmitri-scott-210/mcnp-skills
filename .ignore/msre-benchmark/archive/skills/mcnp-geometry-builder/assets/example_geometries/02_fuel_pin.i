Cylindrical Fuel Pin - Four-region PWR fuel pin geometry
c
c Example demonstrating:
c   - Cylindrical surfaces (CZ card)
c   - Planar surfaces (PZ card) for axial boundaries
c   - Multi-region cylindrical geometry (fuel, gap, clad, coolant)
c   - Union operator (:) for graveyard definition
c
c Cell Cards
c ==========
1    1  -10.41  -1  -10  11    IMP:N=1  VOL=192.3    $ UO2 fuel
2    0            1  -2  -10  11    IMP:N=1  VOL=12.5     $ Gap (void)
3    2  -6.56    2  -3  -10  11    IMP:N=1  VOL=55.4     $ Zircaloy clad
4    3  -0.74    3  -4  -10  11    IMP:N=1  VOL=400.0    $ Water coolant
5    0           (4 : 10 : -11)    IMP:N=0                $ Graveyard

c Surface Cards
c ==============
1    CZ   0.4095         $ Fuel outer radius (cm)
2    CZ   0.4180         $ Gap outer radius
3    CZ   0.4750         $ Clad outer radius
4    CZ   0.6350         $ Pin cell boundary (1.27 cm pitch)
10   PZ   0.0            $ Bottom of active fuel
11   PZ   365.76         $ Top of active fuel (12 ft)

c Data Cards
c ===========
MODE N
c Uniform source throughout fuel volume
SDEF  CEL=1  ERG=2.0    $ Fission spectrum approximation
c Materials
M1   92235  -0.04  92238  -0.96  8016  -2.0    $ UO2, 4% enriched
M2   40000  1.0                                 $ Zircaloy (Zr)
M3   1001   2.0    8016   1.0                   $ H2O (water)
     MT3   lwtr.10t                             $ S(a,b) for water
NPS  50000
