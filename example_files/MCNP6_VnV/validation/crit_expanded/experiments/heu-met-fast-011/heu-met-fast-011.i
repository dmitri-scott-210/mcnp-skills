CH2 Reflected HEU sphere: HEU-MET-FAST-011
1   0              -2              $ central cavity
3   1   4.7392-2    2  -3          $ core
4   0               3  -4  11      $ spheric gap
5   0               3  -5   6 -11  $ diaphr void
6   0               3  -6  10 -14  $ gap
7   2   1.1714-1    3  -7 -10      $ bottom refl
8   2   1.1714-1    4  -8  11      $ top refl
9   3   8.1174-2    5   6 -11 -14  $ diaphr
11  0               7 -10 -14      $ bot void
12  0               8  11 -14      $ top void
15  0              14              $ outer
 
2   so    2
3   so    7.55
4   sz    1.96   7.55
5   cz    8.5
6   pz    1.66
7   so   18
8   sz    1.96  18
10  pz    0
11  pz    1.96
14  so   21.5
 
imp:n 1 9r 0
kcode 10000 1. 100 600
ksrc  0 0 -3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
