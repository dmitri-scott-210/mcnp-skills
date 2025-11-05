Multi-Layer Slab Geometry - Five-layer shielding problem
c
c Example demonstrating:
c   - One-dimensional slab geometry (planes only)
c   - Multi-layer shielding calculation
c   - Infinite lateral extent (no X or Y boundaries)
c   - Importance increasing with depth
c
c Cell Cards
c ==========
1    0           -1         IMP:N=1              $ Source region (void)
2    1  -1.0      1  -2     IMP:N=1  VOL=1000    $ Water layer 1
3    2  -11.35    2  -3     IMP:N=2  VOL=500     $ Lead layer
4    1  -1.0      3  -4     IMP:N=4  VOL=1000    $ Water layer 2
5    3  -2.35     4  -5     IMP:N=8  VOL=500     $ Concrete layer
6    0             5  -6    IMP:N=8  VOL=2000    $ Detector region
7    0             6        IMP:N=0              $ Graveyard

c Surface Cards
c ==============
1    PZ   0.0            $ Source plane
2    PZ   10.0           $ 10 cm water
3    PZ   15.0           $ 5 cm lead
4    PZ   25.0           $ 10 cm water
5    PZ   30.0           $ 5 cm concrete
6    PZ   50.0           $ Detector region end

c Data Cards
c ===========
MODE N
c Planar source at z=0, directed toward +z
SDEF  POS=0 0 0  ERG=14.1  VEC=0 0 1  DIR=1
c Materials
M1   1001   2.0    8016   1.0     $ H2O (water)
     MT1   lwtr.10t
M2   82000  1.0                    $ Lead (Pb)
M3   1001   0.168  8016  0.562  20000  0.100  14000  0.095  $ Concrete (simplified)
     26000  0.050  11000  0.025
     MT3   lwtr.10t
c Tallies
F4:N  6                            $ Average flux in detector region
E4    0.0  0.1  1.0  10.0  15.0   $ Energy bins (MeV)
NPS   100000
