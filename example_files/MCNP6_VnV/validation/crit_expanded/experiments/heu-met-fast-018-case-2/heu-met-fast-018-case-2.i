Simplified Bare HEU Sphere, VNIIEF; HEU-MET-FAST-018 case 2
C W-180 fraction added to W-182 because of cross sections
C Cell Cards
1   0                -1
2   1    4.8302e-2    1  -2
3   0                 2

C Surface Cards
1   so   1.000
2   so   9.154

C Data Cards
imp:n 1 1 0
totnu
kcode 10000 1. 100 600
ksrc  2 0 0
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
