Invalid MCNP Input - Missing Thermal Scattering for Graphite
c
c Cells
c
100 1 -1.8 -1 imp:n=1
1000 0  1  imp:n=0

c Surfaces
1 so 10

c Materials
m1  $ Graphite - MISSING MT CARD!
    6012.00c  0.9890
    6013.00c  0.0110
c ← ERROR: Should have mt1 grph.18t
