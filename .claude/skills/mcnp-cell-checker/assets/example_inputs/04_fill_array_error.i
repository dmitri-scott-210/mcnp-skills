Fill Array Dimension Error Example - BEFORE FIX
c =================================================================
c This file demonstrates a fill array dimension mismatch error
c Declared range requires 25 values but only 20 are provided
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0       -1         lat=1  u=10  fill=-2:2 -2:2 0:0  imp:n=1
            1 1 1 1 1
            1 2 2 2 1
            1 2 3 2 1
            1 2 2 2 1
10   1  -10.5 -10      u=1       imp:n=1          $ Fuel pin
20   2  -1.0  -20      u=2       imp:n=1          $ Moderator pin
30   3  -8.0  -30      u=3       imp:n=1          $ Control rod
100  0       1                   imp:n=0          $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RPP  -10 10 -10 10 0 20                      $ Lattice boundary
10   CZ   0.5                                      $ Fuel pin radius
20   CZ   0.5                                      $ Moderator pin radius
30   CZ   0.5                                      $ Control rod radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   92235  1.0                                    $ U-235 fuel
M2   1001  2  8016  1                              $ H2O moderator
MT2  LWTR.01T                                      $ Light water S(a,b)
M3   5010  1.0                                     $ B-10 absorber
KCODE  10000  1.0  20  120
KSRC   0 0 10
PRINT

