Steel Reflected HEU Sphere, VNIIEF:  HEU-MET-FAST-021 case 2
C W-180 fraction added to W-182 becasuse of cross sections
C Cell Cards
1   0               -1
2   1   4.8246e-2    1  -2
3   2   8.1737e-2    2  -3
4   3   8.1354e-2    3  -4
5   0                4

C Surface Cards
1   so    0.890
2   so    7.550
3   so   11.00
4   so   17.25

C Data Cards
imp:n 1 1 1 1 0
totnu
kcode 10000 1. 100 600
ksrc  2 0 0
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
