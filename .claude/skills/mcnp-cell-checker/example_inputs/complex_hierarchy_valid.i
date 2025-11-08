Complex Universe Hierarchy - VALID Example
c Demonstrates 4-level nesting with proper validation
c Based on AGR-1 HTGR model patterns
c
c Level 1: Fuel pin (u=100)
c Level 2: Pin lattice (u=200, LAT=1, 3×3)
c Level 3: Assembly (u=300, LAT=1, 2×2)
c Level 4: Global placement
c
c ============================================================================
c CELLS
c ============================================================================
c
c Level 1: Fuel pin universe (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Level 2: Pin lattice (u=200, 3×3×1 = 9 elements)
200 0  -200  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100 100

c Level 3: Assembly lattice (u=300, 2×2×1 = 4 elements)
300 0  -300  u=300 lat=1  imp:n=1  fill=0:1 0:1 0:0
     200 200
     200 200

c Level 4: Global placement
999 0  -400 fill=300  imp:n=1
1000 0  400  imp:n=0  $ Outside world

c ============================================================================
c SURFACES
c ============================================================================
c
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
200 rpp -0.63 0.63 -0.63 0.63 -180 180  $ Pin cell box (1.26 cm pitch)
300 rpp -1.26 1.26 -1.26 1.26 -180 180  $ Assembly box (2×1.26 cm pitch)
400 rpp -2.0 2.0 -2.0 2.0 -200 200  $ Global boundary

c ============================================================================
c MATERIALS
c ============================================================================
c
m1  $ UO2
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
m2  $ Zircaloy
   40000.60c  1.0
m3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t

c ============================================================================
c PROBLEM SETUP
c ============================================================================
c
kcode 1000 1.0 10 50
ksrc 0 0 0
