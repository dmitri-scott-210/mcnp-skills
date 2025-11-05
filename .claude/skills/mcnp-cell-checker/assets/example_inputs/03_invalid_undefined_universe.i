INVALID - Undefined Universe Reference - Cell Checker Example
c =================================================================
c ERROR: Cell 1 references fill=5 but no cell has u=5
c This will cause FATAL ERROR in MCNP
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0            -1      fill=5  IMP:N=1           $ ERROR: u=5 not defined!
100  1  -1.0     -100    u=1     IMP:N=1           $ Universe 1: water sphere
999  0            1               IMP:N=0           $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   20.0                                      $ Outer boundary
100  SO   10.0                                      $ Inner water sphere

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                              $ H2O
MT1  LWTR.01T
SDEF POS=0 0 0  ERG=1.0
F4:N 100
NPS  1000
PRINT
