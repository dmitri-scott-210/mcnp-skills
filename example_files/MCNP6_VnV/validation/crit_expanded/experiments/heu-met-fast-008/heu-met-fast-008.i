Bare HEU Sphere, VNIITF: HEU-MET-FAST-008
1   0             -1 -10              $ cavity
2   0             12  -2              $ cav
3   1  4.7319e-2   1  -3   7 -10      $ bottom inner U
4   1  4.7319e-2   2  -4   8  12  16  $ top inner U
5   2  4.8146e-2   3  -5 -10  16      $ bottom outer U
6   2  4.8146e-2   4  -6  12  16      $ top outer U
7   0              1  -3  -7 -10      $ bottom groove
8   0              2  -4  -8  12      $ top groove
9   0             10 -11 -15          $ gap
10  3  8.1174e-2  11 -12 -20  17      $ diaphragm Fe
11  0              5 -15 -10  13      $ bottom outside
12  0              6 -15  12          $ top outside
13  4  8.2365e-2  18  -9 -13 -10      $ Cu cup
14  3  8.1174e-2   9  19 -14 -10      $ Fe cylinder
15  0              9 -15 14 -13 -10   $ void under Cu cup
16  0              3  -5 -16 -10      $ bottom polar hole
17  0              2  -6 -16  12      $ top polar hole
18  0             11 -12 -17          $ diaphr hole
19  0              5 -13 -18 -10      $ gap over cup
20  0            -14 -15 -19          $ void under cyl
21  0             11 -12 -15 20       $ void outside diaphragm
22  0             15                  $ outside

1   so     2
2   sz     1.207    2
3   so     9.15
4   sz     1.207    9.15
5   so    10.15
6   sz     1.207   10.15
7   cy     0.6
8   c/y    0        1.207     0.6
9   so    10.44
10  pz     0
11  pz     1.007
12  pz     1.207
13  cz     8.7
14  cz     2.5
15  so    16
16  cz     1.1
17  cz     9.8
18  so    10.29
19  pz   -14.74
20  cz    15

imp:n  1 20r 0
totnu
kcode  10000 1. 100 600
ksrc   0 0 -3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
