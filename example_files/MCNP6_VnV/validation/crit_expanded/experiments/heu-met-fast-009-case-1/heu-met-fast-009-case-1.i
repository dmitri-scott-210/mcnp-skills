Be-Reflected HEU Sphere, Keff=0.9992+-0.0015: HEU-MET-FAST-009
1   0            -17  -3                  $ equ hole
2   0            -16   6  -8  12          $ polar hole in Refl
3   1  4.7328-2   -3  17                  $ U sphere
4   0              3  -4  12              $ spheric crit gap
5   1  4.7328-2    3  -5 -10  17          $ bottom U
6   1  4.7328-2    4  -6  12  18          $ top U
7   2  1.2103-1    5  -7 -19              $ bot refl
8   2  1.2103-1    6  -8  20  16          $ top refl
9   0              3  10 -11 -15          $ crit gap
10  3  8.1174-2    2  11 -12 -15          $ diaphr
11  0              7 -15 -10  13  21      $ bot void
12  0              8 -15  12 -22          $ top void
13  4  8.2365-2    7  -9 -13 -10          $ Cu cup
14  3  8.1174-2    9 -15 -14 -10  21      $ Fe shaft
15  0              9 -15  14 -13 -10  21  $ bot void 2
16  0              3  -2  11 -12          $ void in diaphr
17  0              5  -7  19 -10          $ bot Be cut
18  0              6  -8  12 -20          $ top Be cut
19  0            -10   3  -5 -17          $ bot U groove
20  0              4  -6  12 -18          $ top U groove
23  0             15:-21:22               $ out

2   cz    7.75
3   so    7.55
4   sz    2.06   7.55
5   so    8.35
6   sz    2.06   8.35
7   so   11
8   sz    2.06  11
9   so   11.15
10  pz    0
11  pz    1.86
12  pz    2.06
13  cz    9.7
14  cz    2.5
15  cz   14
16  cz    1.1
17  cy    0.6
18  c/y   0      2.06   0.6
19  pz   -0.15
20  pz    2.21
21  pz  -14.15
22  pz   14

imp:n 1 19r 0
kcode 10000 1. 100 600
ksrc  0 0 3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
