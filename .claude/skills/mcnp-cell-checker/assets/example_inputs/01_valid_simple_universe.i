Valid Simple Universe Fill - Cell Checker Example
c =================================================================
c Demonstrates correct universe definition and reference
c Universe 1 filled into cell 1 (real world cell)
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0            -1      fill=1  IMP:N=1           $ Real world, fill with u=1
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
