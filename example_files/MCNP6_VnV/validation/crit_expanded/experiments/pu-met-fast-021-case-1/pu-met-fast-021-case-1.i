PU CYLINDER REFLECTED BY BE, ASSEMBLY 50 (#2115): PU-MET-FAST-021 case 1
1   2   7.6215e-2    11  -7  -1           imp:n=1   $ Fe
2   1   4.6924e-2    12  -7 -11           imp:n=1   $ Pu
3   2   7.6215e-2    13  -7 -12           imp:n=1   $ Fe
4   1   4.6924e-2    14  -7 -13           imp:n=1   $ Pu
5   2   7.6215e-2    15  -7 -14           imp:n=1   $ Fe
6   1   4.6924e-2    16  -7 -15           imp:n=1   $ Pu
7   2   7.6215e-2    17  -7 -16           imp:n=1   $ Fe
8   1   4.6924e-2    18  -7 -17           imp:n=1   $ Pu
9   2   7.6215e-2    19  -7 -18           imp:n=1   $ Fe
10  1   4.6924e-2    20  -7 -19           imp:n=1   $ Pu
11  2   7.6215e-2     5  -7 -20           imp:n=1   $ Fe
12  0                 1 -32  -2           imp:n=1   $ vacuum
13  2   7.6215e-2     2  -7 -21           imp:n=1   $ Fe
14  1   4.6924e-2    21  -7 -22           imp:n=1   $ Pu
15  2   7.6215e-2    22  -7 -23           imp:n=1   $ Fe
16  1   4.6924e-2    23  -7 -24           imp:n=1   $ Pu
17  2   7.6215e-2    24  -7 -25           imp:n=1   $ Fe
18  1   4.6924e-2    25  -7 -26           imp:n=1   $ Pu
19  2   7.6215e-2    26  -7 -27           imp:n=1   $ Fe
20  1   4.6924e-2    27  -7 -28           imp:n=1   $ Pu
21  2   7.6215e-2    28  -7 -29           imp:n=1   $ Fe
22  1   4.6924e-2    29  -7 -30           imp:n=1   $ Pu
23  2   7.6215e-2    30  -7  -3           imp:n=1   $ Fe
24  2   7.6215e-2     5   7  -8  -1       imp:n=1   $ Fe
25  2   7.6215e-2     2   7  -8  -3       imp:n=1   $ Fe
26  3   1.2204e-1     6  -9  -5           imp:n=1   $ Be
27  3   1.2204e-1    31  -9  -4           imp:n=1   $ Be
28  0                34  32  -9 -33       imp:n=1   $ vacuum
29  0               -10  #(6 -9 -4)       imp:n=1   $ OUTSIDE
30  4   3.9462e-2    -1   5   8 -32       imp:n=1   $ Al centric rings
31  4   9.0639e-3     2   8 -31 -32       imp:n=1   $ Al basket
32  0                 3  -8 -31           imp:n=1   $ top clearance
33  4   6.0426e-2    -9 -31  32  33       imp:n=1   $ Al top support rings
34  4   6.0426e-2     5  -9  32 -34       imp:n=1   $ Al bott centring ring
35  0                10                   imp:n=0   $ OUTSIDE

1   pz 0.
2   pz     0.01
3   pz     2.46
4   pz    17.375
5   pz    -2.45
6   pz   -17.345
7   cz     5.995
8   cz     6.063
9   cz     9.995
10  so    22
11  pz    -0.02
12  pz    -0.47
13  pz    -0.51
14  pz    -0.96
15  pz   -1.0
16  pz   -1.45
17  pz   -1.49
18  pz   -1.94
19  pz   -1.98
20  pz   -2.43
21  pz    0.03
22  pz    0.48
23  pz    0.52
24  pz    0.97
25  pz    1.01
26  pz    1.46
27  pz    1.5
28  pz    1.95
29  pz    1.99
30  pz    2.44
31  pz    2.48
32  cz    6.263
33  pz    2.28
34  pz   -2.25

mode    n
kcode   10000  1.  100  600
ksrc    0  0  -0.2
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
