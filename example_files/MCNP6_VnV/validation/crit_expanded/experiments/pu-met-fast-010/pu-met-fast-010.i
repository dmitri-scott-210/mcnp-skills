PU-MET-FAST-010:  Pu sphere reflected by normal uranium
1    1   -15.778  -1         imp:n=1
2    2   -18.92  1 -2        imp:n=1
3    0   2                   imp:n=0

1   so   5.0419
2   so   9.1694

mode   n
ksrc   0 0 0
kcode 10000  1.  100  600
totnu
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
