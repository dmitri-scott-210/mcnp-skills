Bare HEU Cylinder, VNIITF: HEU-MET-FAST-015
1   1   4.7832e-2   (5  -8  -1) #2     imp:n=1   $ bottom U
2   0                4  -6  -1         imp:n=1   $ source cavity
3   0                1  -8  -2         imp:n=1   $ gap
4   2   4.7767e-2    2  -8  -3   7     imp:n=1   $ top U
5   0                2  -7  -3         imp:n=1   $ top axial hole
6   3   8.1133e-2   11 -10  -5         imp:n=1   $ steel plate
7   0               11  10  -8  -5     imp:n=1   $ bot hollows
8   3   8.1133e-2    2 -12   8 -13     imp:n=1   $ diaphragm
9   0              (-9 -11):(-9 -2 8)  imp:n=1   $ inner OUTSIDE 1
10  0              (-9 3):(-9 8 12)    imp:n=1   $ inner outside 2
11  0                2  -9 -12  13     imp:n=1   $ outside diaphr
12  0                9                 imp:n=0   $ outer OUTSIDE

1   pz    0
2   pz    0.05
3   pz    5.22
4   pz   -1.0
5   pz   -5.96
6   cz    0.6
7   cz    1.75
8   cz    9.995
9   so   15
10  cz    9.8
11  pz   -6.17
12  pz    0.26
13  cz   13

mode n
totnu
kcode 10000 1. 100 600
ksrc  0  0 -2
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
