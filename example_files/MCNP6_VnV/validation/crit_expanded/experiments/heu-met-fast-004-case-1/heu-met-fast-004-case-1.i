HEU-MET-FAST-004 case 1  Idealized Oy sphere (97.675 w/o) on Lucite ring in H2O
c  Transactions of ANS 27, 412 (11/77)
1        1   0.048143       -1                           $ oralloy sphere
2        2   0.10827         5    -6    -7     8         $ seat as hollow cyl.
3        3   0.10021         1     2    -3    -4
                            #2                           $ water
6        0                  -2:3:4
 
1        so      6.5537                          $ radius of oralloy sphere
2        pz    -32.500                           $ lower surface of water
3        cz     30.000                           $ outer radius of water
4        pz     23.054                           $ upper surface of water
5        cz      3.974                           $ inner radius of seat
6        cz     12.700                           $ outer radius of seat
7        pz     -5.212                           $ top of seat
8        pz     -7.752                           $ bottom of seat
 
mode     n
kcode    10000   1.0   100   600
imp:n    1.0    2r   0.0
sdef     cel=1    erg=d1   rad=d2   pos=0.0 0.0 0.0
sp1      -3
si2      0.0    0.65537
sp2      -21    2
read file=m-cards-endf71
totnu
prdmp  999999  999999  1  1  999999
