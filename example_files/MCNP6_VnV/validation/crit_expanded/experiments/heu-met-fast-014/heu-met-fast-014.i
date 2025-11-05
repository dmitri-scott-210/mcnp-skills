D38 Depleted Uranium Reflected HEU sphere: HEU-MET-FAST-014
1   0               -1 -10              $ bottom central cavity
2   0               12  -2              $ top centr cav
3   1   4.7330e-2    1  -3 -10  16  18  $ bot core
4   1   4.7330e-2    2  -4  12  16  19  $ top core
5   2   4.7065e-2    3  -5 -10  17      $ bot inn refl
6   2   4.7065e-2    4  -6  12  17      $ top inn
7   2   4.7065e-2    5  -7 -10          $ bot outer refl
8   2   4.7065e-2    6  -8  12  20      $ top out refl
9   0               10 -11 -15          $ gap
10  3   8.1174e-2   11 -12 -15          $ diaphr
11  0                7 -15 -10  13
12  0                8 -15  12
13  4   6.0426e-2    7  -9 -13 -10      $ Dural Cup
14  4   6.0426e-2    9 -15 -14 -10      $ Dural shaft
15  0                9 -15  14 -13 -10
16  0                1  -3 -10 -16
17  0                2  -4  12 -16
18  0                3  -5 -17 -10
19  0                4  -6  12 -17
20  0                1  -3 -10  16 -18
21  0                2  -4  12  16 -19
22  0                6  -8  12 -20
23  0               15
 
1   so      3.15
2   sz      0.64   3.15
3   so      8.35
4   sz      0.64   8.35
5   so      9.15
6   sz      0.64   9.15
7   so     13
8   sz      0.64  13
9   so     13.2
10  pz      0
11  pz      0.44
12  pz      0.64
13  cz     11
14  cz      2.5
15  so     16
16  cz      1.1
17  cz      1.75
18  cy      0.6
19  c/y     0      0.64    0.6
20  cz      0.5
 
imp:n 1 21r 0
kcode 10000 1. 100 600
ksrc  3 3 -3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
