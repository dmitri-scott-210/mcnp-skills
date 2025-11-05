HEU Reflected Pu Sphere, VNIITF: MIX-MET-FAST-003
1   0               -1                   $ central cavity
2   1   4.2162e-2    1  -5               $ Pu
3   0                5  -6  12           $ crescent gap
4   0                5  -2  11 -12       $ diaphragm gap
5   2   4.74202e-2   5  -7 -10  15       $ bottom U
6   2   4.74202e-2   3   6  -8  12  16   $ top U
7   0                5  -7 -10 -15       $ bottom groove in U
8   0                6  -8  12 -16       $ top groove in U
9   0                5  10 -11 -17       $ critical gap
10  5   6.0426e-2    2  11 -12 -17       $ diaphragm
11  0                7 -10  13 -17       $ bottom void
12  0                8  12 -17           $ top void
13  4   8.2365e-2    7  -9 -13 -10       $ cup
14  3   8.1174e-2    9 -10 -14 -17       $ shaft
15  0                9 -10 -13  14 -17   $ void under cup
16  0               -3   6  -8  12       $ hole in top U
17  0               17                   $ outer void

1   so    1
2   cz    5.5
3   cz    1.1
5   so    5.35
6   sz    1.225   5.35
7   so    7.55
8   sz    1.225   7.55
9   so    7.7
10  pz    0
11  pz    1.025
12  pz    1.225
13  cz    6.5
14  cz    2.5
15  cy    0.6
16  c/y   0       1.225    0.6
17  so   14

imp:n 1 15r 0
kcode 10000 1. 100 600
ksrc 0 0 -2
totnu
read file=m-cards-endf71
c  print
prdmp  999999  999999  1  1  999999
