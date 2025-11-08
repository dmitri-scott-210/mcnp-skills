Invalid MCNP Input - FILL Array Dimension Mismatch
c Should trigger error: Need 9 elements but only 8 provided
c
c Cells
c
100 1 -10.2  -100         u=100  imp:n=1
101 0  -200  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100
c ← ERROR: Only 8 elements, need 9!

999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0

c Surfaces
100 cz 0.5
200 rpp -1.5 1.5 -1.5 1.5 -10 10

c Materials
m1 92235.70c 1.0
