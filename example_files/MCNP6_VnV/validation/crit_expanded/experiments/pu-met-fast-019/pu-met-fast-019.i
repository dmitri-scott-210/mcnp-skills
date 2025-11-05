Be-REFLECTED PU SPHERE [VNIITF FACILITY]: PU-MET-FAST-019
1   0               -1                  $ cavity
2   1   4.2157e-2    1  -3              $ Pu Core
3   0                3  -4  12
4   0                3  -5  11 -12
5   2   1.2105e-1    3  -7 -16          $ Bottom Reflector
6   2   1.2105e-1    4   6  -8  12      $ top reflector
7   0                3  10 -11 -15
8   3   8.1174e-2    5  11 -12 -15      $ diaphragm
9   0                7 -10  13 -15
10  0                8  12 -15
11  4   8.2365e-2    7  -9 -13 -10      $ copper cup
12  3   8.1174e-2    9 -10 -14 -15      $ shaft
13  0                9 -10 -13  14 -15
14  0                3  -7 -10  16
15  0                4  -6  -8  12      $ polar hole in Top Reflector
16  0               15

1   so    1.4
3   so    5.35
4   sz    1.05    5.35
5   cz    5.50
6   cz    1.1
7   so   11
8   sz    1.05   11
9   so   11.15
10  pz    0
11  pz    1
12  pz    1.20
13  cz    9.7
14  cz    2.5
15  so   14
16  pz   -0.15

imp:n   1  14r  0
kcode   10000  1.  100  600
ksrc    0  0 -1.41
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
