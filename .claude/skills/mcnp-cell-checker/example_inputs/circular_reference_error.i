Circular Reference Error Example - INVALID
c Demonstrates circular universe fill chain
c This will cause MCNP to fail with infinite recursion
c
c ERROR: u=100 fills u=200, u=200 fills u=100 (circular!)
c
c ============================================================================
c CELLS
c ============================================================================
c
c Circular reference: 100→200→100
100 0 -10  u=100  fill=200  imp:n=1  $ Fills with u=200
200 0 -20  u=200  fill=100  imp:n=1  $ Fills with u=100 - CIRCULAR!

c Global placement
999 0  -10 fill=100  imp:n=1
1000 0  10  imp:n=0

c ============================================================================
c SURFACES
c ============================================================================
c
10 rpp -5 5 -5 5 -5 5
20 rpp -3 3 -3 3 -3 3

c ============================================================================
c MATERIALS
c ============================================================================
c
c No materials needed for this error demonstration

c ============================================================================
c PROBLEM SETUP
c ============================================================================
c
mode n
sdef
nps 100
