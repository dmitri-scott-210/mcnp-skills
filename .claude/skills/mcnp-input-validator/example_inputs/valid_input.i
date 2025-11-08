Valid MCNP Input - Should Pass All Validation Checks
c Rectangular lattice with correct FILL array
c
c Cells
c
c Fuel pin (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Pin lattice (u=200) - LAT=1 rectangular
c 3×3 = 9 elements
200 0  -200  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100 100

c Global cell
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0

c
c Surfaces
c
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
200 rpp -1.5 1.5 -1.5 1.5 -100 100  $ Assembly box (3×1.0 cm)

c
c Materials
c
m1  $ UO2 fuel
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
c
m2  $ Zircaloy
   40000.60c  1.0
c
m3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t  $ Thermal scattering for water

c
c Source
kcode 1000 1.0 10 50
ksrc 0 0 0
