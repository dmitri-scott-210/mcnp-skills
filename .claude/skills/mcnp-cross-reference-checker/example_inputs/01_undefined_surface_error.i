Cross-Reference Error Example: Undefined Surface
c =================================================================
c This example demonstrates: Cell references undefined surface
c Error: "fatal error. surface 203 in cell 10 is not defined"
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7     -1 2 -3            IMP:N=1  $ Valid cell
10   2  -8.0     -1 2 -203 4        IMP:N=1  $ ERROR: Surface 203 undefined!
15   0           1                  IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    PZ   0.0                                $ Bottom plane
2    PZ   10.0                               $ Top plane
3    CZ   5.0                                $ Outer cylinder
4    CZ   8.0                                $ Larger cylinder
c Surface 203 is MISSING - this causes FATAL error

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                       $ Water
M2   26000 1                                 $ Iron
SDEF  POS=0 0 5  ERG=1.0
NPS   1000
PRINT
