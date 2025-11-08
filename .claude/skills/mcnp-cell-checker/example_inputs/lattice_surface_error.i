Lattice Surface Type Error - INVALID
c
c ERROR: LAT=2 (hexagonal) requires RHP surface, not RPP
c
c ============================================================================
c CELLS
c ============================================================================
c
c Simple fuel cell
100 1 -10.0  -100  u=10  imp:n=1  $ Fuel

c INVALID: LAT=2 with RPP surface (should be RHP for hexagonal)
c LAT=1 (rectangular) → requires RPP
c LAT=2 (hexagonal)   → requires RHP
200 0  -200  u=20 lat=2  imp:n=1  fill=-1:1 -1:1 0:0
     10 10 10
     10 10 10
     10 10 10

c Global placement
999 0  -200 fill=20  imp:n=1
1000 0  200  imp:n=0

c ============================================================================
c SURFACES
c ============================================================================
c
100 so 0.5
200 rpp -2 2 -2 2 -5 5  $ ERROR: Should be RHP for LAT=2!
c Correct would be:
c 200 rhp 0 0 -5  0 0 10  0 1.6 0  $ RHP for hexagonal lattice

c ============================================================================
c MATERIALS
c ============================================================================
c
m1 92235.70c 1.0

c ============================================================================
c PROBLEM SETUP
c ============================================================================
c
mode n
kcode 1000 1.0 10 50
ksrc 0 0 0
