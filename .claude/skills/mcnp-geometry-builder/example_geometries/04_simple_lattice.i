Simple 3x3 Pin Lattice - Rectangular array demonstration
c
c Example demonstrating:
c   - Universe (U) parameter for repeated structures
c   - LAT=1 rectangular lattice
c   - FILL parameter with index ordering
c   - Multiple pin types in lattice
c
c Pin universe (U=1) - Fuel pin
c ===================================
1    1  -10.5  -1     U=1  IMP:N=1    $ Fuel
2    2  -6.5    1 -2  U=1  IMP:N=1    $ Clad
3    3  -1.0    2 -3  U=1  IMP:N=1    $ Water
c Pin universe (U=2) - Control rod
c ===================================
10   4  -2.0   -1     U=2  IMP:N=1    $ Absorber
11   2  -6.5    1 -2  U=2  IMP:N=1    $ Clad
12   3  -1.0    2 -3  U=2  IMP:N=1    $ Water
c Lattice cell (3x3 array)
c ===================================
20   0  -10 11 -12 13 -14 15  LAT=1  U=3  IMP:N=1
        FILL=-1:1 -1:1 0:0
             1 1 2
             1 1 1
             2 1 1
c Base geometry
c ===================================
30   0  -20  FILL=3  IMP:N=1         $ Fill with lattice
31   0   20  IMP:N=0                 $ Graveyard

c Pin surfaces (local to universes 1 and 2)
c ===========================================
1    CZ  0.5                         $ Pin radius
2    CZ  0.55                        $ Clad outer
3    CZ  0.707                       $ Pin cell boundary (sqrt(2)/2 for 1cm pitch)
c Lattice surfaces
c ===========================================
10   PX  -1.5                        $ X min (3 cells × 1cm pitch)
11   PX   1.5                        $ X max
12   PY  -1.5                        $ Y min
13   PY   1.5                        $ Y max
14   PZ   0.0                        $ Z min
15   PZ  100.0                       $ Z max
c Outer boundary
c ===========================================
20   RPP  -5 5  -5 5  -5 105         $ Problem boundary

c Data Cards
c ===========
MODE N
SDEF  CEL=30  ERG=2.0                $ Source in filled cell
M1   92235  -0.04  92238  -0.96  8016  -2.0    $ UO2 fuel
M2   40000  1.0                                 $ Zircaloy
M3   1001   2.0    8016   1.0                   $ Water
     MT3   lwtr.10t
M4   48000  1.0                                 $ Cadmium absorber
NPS  50000
