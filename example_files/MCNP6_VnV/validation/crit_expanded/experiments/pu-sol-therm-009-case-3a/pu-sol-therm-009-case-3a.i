PU-SOL-THERM-009  Case 3A  Plutonium Nitrate Solution in Al-1100 Sphere
1    1  0.100416    -1
2    2  0.060325    -2   1
3    0                   2

1   so  60.964
2   so  61.734

kcode    10000    1.0    100   600
sdef   cel=1     erg=d1    rad=d2    pos=0.0 0.0 0.0
sp1    -3
si2    0.0   60.9
sp2    -21    2
totnu
imp:n   1.0 1.0 0.0
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
