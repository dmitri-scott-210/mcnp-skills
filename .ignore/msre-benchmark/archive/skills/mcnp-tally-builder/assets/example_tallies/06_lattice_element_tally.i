Lattice Element Tally - F4 with Bracket Notation
c
c Example demonstrating:
c   - F4 flux tally in repeated structures
c   - Bracket notation for lattice elements
c   - Simple 3x3 fuel pin array
c   - Individual element tallies
c
c =================================================================
c Cell Cards
c =================================================================
c Lattice cell (filled by universe 1)
1    0         -1        LAT=1  IMP:N=1  U=1  FILL=-1:1 -1:1 0:0  1 3r
c              ^Lattice boundary
c Fuel pin unit cell (universe 1)
10   1  -10.0  -10       IMP:N=1  U=1              $ Fuel pellet
11   2  -6.5    10 -11   IMP:N=1  U=1              $ Cladding
12   3  -1.0    11 -12   IMP:N=1  U=1              $ Coolant
c Problem boundary
20   0          1  -2    IMP:N=1  FILL=1           $ Container for lattice
99   0          2        IMP:N=0                   $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RCC  0 0 0  0 0 10  5.0                       $ Lattice container
2    SO   50.0                                     $ Problem boundary
c Lattice element surfaces
10   CZ   0.4                                      $ Fuel radius
11   CZ   0.45                                     $ Clad outer
12   RCC  0 0 0  0 0 10  0.6                       $ Pin cell boundary

c =================================================================
c Data Cards
c =================================================================
MODE N
c Source - Uniform in lattice
SDEF  POS=0 0 5  ERG=2.0  RAD=D1
SI1   0  4                                         $ Radius distribution
SP1  -21  1                                        $ Power 1 (uniform area)
c Materials
M1   92235  1.0                                    $ Fuel (U-235)
M2   40000  1.0                                    $ Clad (Zr)
M3   1001  2  8016  1                              $ Coolant (H2O)
MT3  LWTR.01T
c Lattice element tallies using bracket notation
F4:N  (10<1[-1 -1 0])                              $ Bottom-left fuel
      (10<1[ 0  0 0])                              $ Center fuel
      (10<1[ 1  1 0])                              $ Top-right fuel
c     ^cell ^univ ^lattice indices [i j k]
c Termination
NPS   1000000
