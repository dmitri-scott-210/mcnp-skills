Cross-Reference Fixed: Material 5 Added
c =================================================================
c This example shows the FIX for undefined material error
c Fix: Add M5 material definition
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7     -1 2 -3            IMP:N=1  $ Uses material 1 (OK)
10   2  -8.0     1 -2 4             IMP:N=1  $ Uses material 2 (OK)
15   5  -7.0     2 -3 4             IMP:N=1  $ Now valid with material 5
20   0           3                  IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    PZ   0.0
2    PZ   5.0
3    PZ   10.0
4    CZ   8.0

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                       $ Water
M2   26000 1                                 $ Iron
M5   6000  1                                 $ ADDED - Carbon (fixes error)
SDEF  POS=0 0 2  ERG=1.0
NPS   1000
PRINT
