Simple Universe Example - 2-Level Hierarchy
c =================================================================
c Demonstrates basic universe definition and fill
c Universe 0 (real world) contains universe 1
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0       -1    fill=1  imp:n=1                  $ Real world cell, fills u=1
10   1  -2.7 -10   u=1     imp:n=1                  $ Universe 1: Aluminum sphere
11   0       10    u=1     imp:n=1                  $ Universe 1: Void outside
999  0       1            imp:n=0                  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                                      $ Real world boundary
10   SO   5.0                                       $ U=1 sphere radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   13027  1.0                                     $ Aluminum-27
SDEF POS=0 0 0  ERG=1.0                             $ 1 MeV point source
F4:N 10                                             $ Flux in universe 1
NPS  10000
PRINT

