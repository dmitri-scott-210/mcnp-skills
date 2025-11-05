Al Reflected HEU Sphere: HEU-MET-FAST-012
1   0               -1 -14  16          $ source cavity
2   0               -1   3  -5 -10      $ bottom equat hollow
3   1   4.7297e-2   -3  #1              $ core
4   0                3  -4  11          $ crescent gap
5   1   4.7297e-2    1   3  -5 -10      $ bot shell
6   1   4.7297e-2    4  -6  11  18      $ top shell
7   2   5.8566e-2    5  -7 -10          $ bott refl
8   2   5.8566e-2    6  -8  11          $ top shell
9   0  -2            3 -11  17          $ diaphr void
10  3   8.1174e-2    2 -11 -15  17      $ diaphragm
11  0                7 -10  12 -15      $ bot void
12  0                8  11 -15          $ top void
13  4   8.2365e-2    7  -9 -10 -12      $ cup
14  3   8.1174e-2    9 -10 -13 -15      $ shaft
15  0                9 -10 -12  13 -15  $ under cup
16  0                4  -6  11 -18      $ top equa hollow
17  0                3  10 -15 -17      $ gap
18  0               15
 
1   cy   0.6
2   cz   7.75
3   so   7.55
4   sz   1.17   7.55
5   so   9.15
6   sz   1.17   9.15
7   so  10
8   sz   1.17  12
9   so  10.15
10  pz   0
11  pz   1.17
12  cz   8.7
13  cz   2.5
14  py   0.5
15  so  14
16  py  -0.5
17  pz   0.97
18  c/y  0      1.17    0.6
 
imp:n 1 16r 0
kcode 10000 1. 100 600
ksrc  0 0 -1
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
