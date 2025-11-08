Invalid MCNP Input - Circular Universe Reference
c u=10 fills with u=20, u=20 fills with u=10 (circular!)
c
c Cells
c
100 0 -1 u=10 fill=20  imp:n=1
200 0 -2 u=20 fill=10  imp:n=1  $ ← ERROR: circular reference!

999 0  -1 fill=10  imp:n=1
1000 0  1  imp:n=0

c Surfaces
1 so 10
2 so 5
