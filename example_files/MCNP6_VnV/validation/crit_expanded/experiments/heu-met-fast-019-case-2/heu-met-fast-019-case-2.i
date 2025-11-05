Graphite Reflected HEU Sphere, VNIIEF;  HEU-MET-FAST-019 case 2
C W-180 fraction added to W-182 because of cross sections
C Graphite thermal S(alpha,Beta) treatment applied at 300K
C Cell Cards
1   0               -1
2   1   4.8493e-2    1  -2
3   2   7.6716e-2    2  -3
4   0                3

C Surface Cards
1   so   4.029
2   so   9.150
3   so   12.60

C Data Cards
imp:n 1 1 1 0
totnu
kcode 10000 1. 100 600
ksrc 6 0 0
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
