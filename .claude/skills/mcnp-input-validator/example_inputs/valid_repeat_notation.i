Valid MCNP Input - Demonstrates Repeat Notation
c Shows correct use of repeat notation: nR = (n+1) total copies
c
c Cells
c
c Fuel pin (u=100) and void pin (u=101)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 0  -100              u=101  imp:n=1  $ Void pin

c 5×5 lattice using repeat notation
c fill=-2:2 -2:2 0:0 = 5×5×1 = 25 elements
200 0  -200  u=200 lat=1  imp:n=1  fill=-2:2 -2:2 0:0
     101 100 100 100 101
     100 100 2R 100
     100 3R 100
     100 100 2R 100
     101 100 100 100 101
c Note: "100 2R" = [100, 100, 100] = 3 elements (100 + 2 more)

c Global cell
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0

c
c Surfaces
c
100 cz  0.41  $ Pin radius
200 rpp -2.5 2.5 -2.5 2.5 -100 100  $ Assembly box

c
c Materials
c
m1  $ UO2 fuel
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0

c
c Source
kcode 1000 1.0 10 50
ksrc 0 0 0
