Steel Reflected IEU sphere (36 wt.%), VNIIEF; IEU-MET-FAST-005
C ENDF/B-V cross sections, W splitup by atmomic abundance
C W-180 fraction added to W-182 because of cross sections
C All Mn taken to Mn-55, the only stable isotope
C Cell Cards
1   0               -1
2   1   4.7948e-2    1 -2
3   2   8.1601e-2    2 -3
4   3   8.2736e-2    3 -4
5   0                4

C Surface Cards
1   so    2.686
2   so   13.25
3   so   15.00
4   so   21.50

C Data Cards
imp:n 1 1 1 1 0
totnu
kcode 10000 1. 100 600
ksrc  3 0 0
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
