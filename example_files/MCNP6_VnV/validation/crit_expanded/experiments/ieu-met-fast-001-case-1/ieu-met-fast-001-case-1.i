Jemima #1, Idealized Model; IEU-MET-FAST-001 Case 1
c
c Lower uranium pole.
1 5 4.55477e-02 101 -129 -2
c Lower uranium disks (without fillers).
51 4 4.79550e-02 101 -105 2 -12
52 3 4.80424e-02 105 -106 2 -12
53 4 4.79550e-02 106 -109 2 -12
54 3 4.80424e-02 109 -110 2 -12
55 4 4.79550e-02 110 -113 2 -12
56 3 4.80424e-02 113 -114 2 -12
57 4 4.79550e-02 114 -117 2 -12
58 3 4.80424e-02 117 -118 2 -12
59 4 4.79550e-02 118 -121 2 -12
60 3 4.80424e-02 121 -122 2 -12
61 4 4.79550e-02 122 -125 2 -12
62 3 4.80424e-02 125 -126 2 -12
63 4 4.79550e-02 126 -129 2 -12
c Upper Tu and Oy disks (homogenized).
64 3 4.80424e-02 129 -131 -10 $** tailored Tu disk **
65 4 4.79550e-02 131 -134 -12
66 3 4.80424e-02 134 -136 -12
67 4 4.79550e-02 136 -138 -12
68 3 4.80424e-02 138 -140 -12
69 4 4.79550e-02 140 -142 -12
70 3 4.80424e-02 142 -144 -12
71 4 4.79550e-02 144 -146 -12
c Extra tuballoy on top (disk equiv. to 1 pie + 1 filler).
72 3 4.80424e-02 146 -161 -12
c Cells defining support structures for uranium disks.
103 1 6.02041e-02 129 -131 10 -17
106 0 201 -101 -8
107 0 202 -201 3 -8
108 1 6.02041e-02 202 -101 8 -18
110 1 6.02041e-02 203 -201 -3
111 1 6.02041e-02 205 -203 -7
112 1 6.02041e-02 204 -202 12 -14
113 0 (204 -202 3 -12) (203: 7)
114 0 204 -202 14 -21
118 1 6.02041e-02 205 -204 11 -19
119 0 205 -204 7 -11
120 2 8.63195e-02 206 -205 -20
121 0 (202 -161 12 -21) (-129: 131: 17) (101: 18)
122 0 205 -204 19 -21
123 0 206 -205 20 -21
c External cell.
200 0 -206: 161: 21

c Cylindrical surfaces defining uranium disks and surrounding supports.
2 cz 1.11125 $** inner radius of uranium disks **
3 cz 1.74625 $** rad. of upper Al filler support cylinder **
7 cz 4.60375 $** rad. of lower Al filler support cylinder **
8 cz 12.06500 $** inner radius of lower Al support ring **
10 cz 12.66939 $** idlzd. Tu/Al bndry in upper supp. ring **
11 cz 12.70000 $** o.r. unique Tu disk; i.r. spacer platform **
12 cz 13.33500 $** outer radius of uranium disks **
14 cz 13.67711 $** outer rad. of idealized Al rect. spacers **
17 cz 15.29416 $** outer edge of idlzd. Al upper supp. ring **
18 cz 15.82055 $** outer rad. of idealized lower Al ring **
19 cz 17.19650 $** outer rad. of idealized Al platform spacer **
20 cz 19.22627 $** rad. of cyl. equiv. to 12"x15" Fe plate **
21 cz 21.00000 $** inner rad. ext. cell (idealized models) **
c Horizontal planes defining uranium disks and fillers.
101 pz 0.000 $** lower surface of bottom uranium disk **
105 pz 0.804
106 pz 1.408
109 pz 2.212
110 pz 2.816
113 pz 3.620
114 pz 4.224
117 pz 5.028
118 pz 5.632
121 pz 6.436
122 pz 7.040
125 pz 7.844
126 pz 8.448
129 pz 9.252 $** parting plane **
131 pz 9.856
134 pz 10.660
136 pz 11.264
138 pz 12.068
140 pz 12.672
142 pz 13.476
144 pz 14.080
146 pz 14.884
161 pz 14.9631
c Horizontal planes defining structural support below uranium disks.
201 pz -0.3175
202 pz -0.9525
203 pz -3.1750
204 pz -4.7625
205 pz -6.0325
206 pz -8.5725

kcode 10000 1. 100 600
ksrc 8. 0. 00.402 0. 8. 00.402 -8. 0. 00.402 0. -8. 00.402&
0. 0. 00.402&
8. 0. 01.810 0. 8. 01.810 -8. 0. 01.810 0. -8. 01.810&
0. 0. 01.810&
8. 0. 03.218 0. 8. 03.218 -8. 0. 03.218 0. -8. 03.218&
0. 0. 03.218&
8. 0. 04.626 0. 8. 04.626 -8. 0. 04.626 0. -8. 04.626&
0. 0. 04.626&
8. 0. 06.034 0. 8. 06.034 -8. 0. 06.034 0. -8. 06.034&
0. 0. 06.034&
8. 0. 07.442 0. 8. 07.442 -8. 0. 07.442 0. -8. 07.442&
0. 0. 07.442&
8. 0. 08.850 0. 8. 08.850 -8. 0. 08.850 0. -8. 08.850&
0. 0. 08.850&
8. 0. 10.258 0. 8. 10.258 -8. 0. 10.258 0. -8. 10.258&
0. 0. 10.258&
8. 0. 11.666 0. 8. 11.666 -8. 0. 11.666 0. -8. 11.666&
0. 0. 11.666&
8. 0. 13.074 0. 8. 13.074 -8. 0. 13.074 0. -8. 13.074&
0. 0. 13.074&
8. 0. 14.482 0. 8. 14.482 -8. 0. 14.482 0. -8. 14.482&
0. 0. 14.482
imp:n 1 37r 0
totnu
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
