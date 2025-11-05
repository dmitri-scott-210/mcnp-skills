Cross-Reference Fixed: Surface 203 Added
c =================================================================
c This example shows the FIX for undefined surface error
c Fix: Add surface 203 definition
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7     -1 2 -3            IMP:N=1  $ Valid cell
10   2  -8.0     -1 2 -203 4        IMP:N=1  $ Now valid with surface 203
15   0           1                  IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    PZ   0.0                                $ Bottom plane
2    PZ   10.0                               $ Top plane
3    CZ   5.0                                $ Outer cylinder
4    CZ   8.0                                $ Larger cylinder
203  PZ   20.5                               $ ADDED - fixes the error

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                       $ Water
M2   26000 1                                 $ Iron
SDEF  POS=0 0 5  ERG=1.0
NPS   1000
PRINT
