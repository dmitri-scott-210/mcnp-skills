Hexagonal Lattice Example - LAT=2 with Fill Array
c =================================================================
c Demonstrates LAT=2 (hexagonal) lattice with fill array
c 7x7x1 hexagonal arrangement
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0      -1 -2 -3 -4 -5 -6 -7 -8  lat=2  u=20  fill=-3:3 -3:3 0:0  imp:n=1
           1 1 1 1 1 1 1
           1 2 2 2 2 2 1
           1 2 3 3 3 2 1
           1 2 3 4 3 2 1
           1 2 3 3 3 2 1
           1 2 2 2 2 2 1
           1 1 1 1 1 1 1
10   1  -10.5  -10    u=1       imp:n=1          $ Reflector pin
20   2  -10.5  -20    u=2       imp:n=1          $ Standard fuel
30   3  -10.5  -30    u=3       imp:n=1          $ High-enrichment fuel
40   4  -8.0   -40    u=4       imp:n=1          $ Control rod
100  0         1 2 3 4 5 6 7 8  imp:n=0          $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    P   0.866  0.5  0  0                         $ Hex side 1
2    P   0.866  -0.5 0  0                         $ Hex side 2
3    P   0      1    0  0                         $ Hex side 3
4    P   -0.866 0.5  0  0                         $ Hex side 4
5    P   -0.866 -0.5 0  0                         $ Hex side 5
6    P   0      -1   0  0                         $ Hex side 6
7    PZ  0                                        $ Bottom
8    PZ  20                                       $ Top
10   CZ  0.4                                      $ Reflector radius
20   CZ  0.4                                      $ Standard fuel radius
30   CZ  0.4                                      $ HE fuel radius
40   CZ  0.4                                      $ Control rod radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   6000  1.0                                    $ Graphite reflector
M2   92235  0.03  92238  0.97                     $ 3% enriched UO2
M3   92235  0.20  92238  0.80                     $ 20% enriched UO2
M4   48000  1.0                                   $ Cadmium control
KCODE  10000  1.0  20  120
KSRC   0 0 10
PRINT

