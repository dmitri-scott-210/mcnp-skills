VOID Test Example - Geometry Validation
c =================================================================
c Demonstrates VOID card test for overlap detection
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7     -1 2 -3            IMP:N=1  $ Water region
2    2  -8.0     1 -4               IMP:N=1  $ Steel shield
3    0           4                  IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    CZ   5.0                                $ Inner cylinder
2    PZ   0.0                                $ Bottom plane
3    PZ   20.0                               $ Top plane
4    CZ   15.0                               $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                       $ Water
M2   26000 1                                 $ Iron
SDEF  POS=0 0 10  ERG=1.0
VOID                                          $ Overlap test
NPS   1000
PRINT
