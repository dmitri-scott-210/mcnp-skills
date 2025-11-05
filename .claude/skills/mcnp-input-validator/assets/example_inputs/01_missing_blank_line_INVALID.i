Missing Blank Line Between Blocks - INVALID
c =================================================================
c Cell Cards
c =================================================================
c
1    1    -2.7    -1         $ Sphere with material 1
2    0          1            $ Outside world (void)
c =================================================================
c Surface Cards - NO BLANK LINE ABOVE (ERROR!)
c =================================================================
c
1    SO    10               $ Sphere radius 10 cm
c
c MISSING BLANK LINE BETWEEN SURFACES AND DATA (ERROR!)
c =================================================================
c Data Cards
c =================================================================
c
MODE N
M1   13027.80c  1.0          $ Aluminum
IMP:N  1 0
NPS  10000
c
