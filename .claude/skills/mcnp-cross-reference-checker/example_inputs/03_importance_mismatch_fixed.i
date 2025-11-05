Cross-Reference Fixed: IMP Entries Corrected
c =================================================================
c This example shows the FIX for IMP count mismatch
c Fix: IMP:N now has exactly 7 entries for 7 cells
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7     -1 2 -3            $ Cell 1
2    1  -2.7     1 -4 5             $ Cell 2
3    2  -8.0     4 -6               $ Cell 3
4    2  -8.0     6 -7               $ Cell 4
5    0           7 -8               $ Cell 5 (void)
6    3  -11.3    8 -9               $ Cell 6
7    0           9                  $ Cell 7 (graveyard)
c Total: 7 cells defined

c =================================================================
c Surface Cards
c =================================================================
1    PZ   0.0
2    PZ   5.0
3    CZ   3.0
4    PZ   10.0
5    CZ   6.0
6    PZ   15.0
7    PZ   20.0
8    PZ   25.0
9    PZ   30.0

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   1001  2   8016  1                       $ Water
M2   26000 1                                 $ Iron
M3   82000 1                                 $ Lead
SDEF  POS=0 0 2  ERG=1.0
c FIXED: Exactly 7 entries for 7 cells
IMP:N  1 1 1 1 1 1 0
NPS   1000
PRINT
