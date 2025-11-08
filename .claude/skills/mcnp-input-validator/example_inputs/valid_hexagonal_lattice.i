Valid MCNP Input - Hexagonal Lattice (LAT=2)
c Demonstrates correct FILL array for LAT=2 hexagonal lattice
c
c Cells
c
c Fuel pin (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 0  100               u=100  imp:n=1  $ Void outside

c Hexagonal lattice (u=200) - LAT=2
c 3×3 = 9 elements (same formula as LAT=1)
200 0  -200  u=200 lat=2  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100 100

c Global cell
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0

c
c Surfaces
c
100 cz  0.41  $ Pin radius
200 rhp 0 0 0  0 0 100  1.5 1.5 1.5  0 0 0  $ Hexagonal prism

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
