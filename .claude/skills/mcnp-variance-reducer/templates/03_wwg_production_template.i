Weight Window Production Template (WWG Stage 2)
c
c =================================================================
c Cell Cards
c =================================================================
c
1  1  -1.0    -1         IMP:N=1     $ Source region
2  2  -7.8    1 -2       IMP:N=1     $ Shield 1
3  3  -11.3   2 -3       IMP:N=1     $ Shield 2
4  0         3 -4       IMP:N=1     $ Detector region
999  0       4          IMP:N=0     $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
c
1  SO  10                          $ Source sphere
2  SO  30                          $ Shield 1 outer
3  SO  50                          $ Shield 2 outer
4  SO  60                          $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c
MODE  N
c
c --- Read weight windows from wwout file ---
WWP:N  J  J  J  0  -1
c      ^default params  ^read wwout from Stage 1
c
c --- Energy bins (must match WWG stage) ---
WWGE:N  1e-10  1e-6  1e-4  0.01  0.1  1  10  20
c
c --- Point detector ---
F5:N  55 0 0  0.5
c
c --- Materials ---
M1  1001  2  8016  1               $ Water
M2  26000  1                       $ Iron
M3  82000  1                       $ Lead
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- High statistics for production ---
NPS  1e7
c
c REQUIRES: wwout file from Stage 1 (WWG generation)
