Undefined Material in Cell - INVALID
c =================================================================
c Cell Cards
c =================================================================
c
1    1    -2.7    -1         $ Uses material 1
2    5    -8.9     1 -2      $ Uses material 5 - NOT DEFINED!
3    0           2           $ Void
c

c =================================================================
c Surface Cards
c =================================================================
c
1    SO     5               $ Inner sphere
2    SO    10               $ Outer sphere
c

c =================================================================
c Data Cards
c =================================================================
c
MODE N
M1   13027.80c  1.0          $ Aluminum - Only M1 defined
c M5 is MISSING but referenced in cell 2!
IMP:N  1 1 0
NPS  10000
c
