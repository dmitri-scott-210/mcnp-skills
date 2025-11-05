STACY-30  Uranyl Nitrate  9.97 wt.% Enr  290.7 g/l U  54.20 cm
c  LEU-SOL-THERM-007  Case 30
1    1    0.086845     1   -2    4   -6           $ Tank Wall
2    1    0.086845    -2    3   -4                $ Tank Bottom
3    1    0.086845    -2    6   -7                $ Tank Top
4    2    0.098564    -1    4   -5                $ Uranyl Nitrate Solution
5    3    4.9425e-5   -1    5   -6                $ Air inside Tank
6    0                 2:-3:7

1   cz   29.5                                     $ Inner Radius of Tank
2   cz   29.8                                     $ Outer Radius of Tank
3   pz   -2.0                                     $ Bottom of Tank
4   pz    0.0                                     $ Bottom of Uranyl Nitrate
5   pz   54.20                                    $ Top of Uranyl Nitrate
6   pz  150.0                                     $ Top of Air
7   pz  152.5                                     $ Top of Tank

kcode    10000    1.0   100   600
imp:n   1.0   4r  0.0
totnu
sdef   cel=4  erg=d1  pos= 0 0 40
sp1    -3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
