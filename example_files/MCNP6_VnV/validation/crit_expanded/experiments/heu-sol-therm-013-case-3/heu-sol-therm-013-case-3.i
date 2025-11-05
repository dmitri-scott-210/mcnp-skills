c  ORNL-3 Uranyl nitrate in H2O Sphere;  HEU-SOL-THERM-013  case #3
c  and CSEWG: T-3
1 1 9.985904038e-2 -1    imp:n=1
2 2 6.0317237e-2    1 -2 imp:n=1
3 0                 2    imp:n=0

1 so 34.5948
2 so 34.9148

mode n
kcode 10000 1. 100 600
sdef  pos 0.0 0.0 0.0  rad d1
sc1   Spherical Source
si1   34.5
read file=m-cards-endf71
totnu
c  print
prdmp  999999  999999  1  1  999999
