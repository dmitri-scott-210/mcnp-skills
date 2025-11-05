Sphere of 4.9 wt.% UO2F2-H2O reflected by Water  LEU-SOL-THERM-002  Case 1
1    1    0.099063     -1                        $ UO2F2D2O Solution
2    2    0.060317      1   -2                   $ Alumninum 1100 Shell
3    3    0.099988      2   -3                   $ Water Reflector
4    0                  3

1    so   34.3990                                $ OR of Solution
2    so   34.5578                                $ OR of Shell
3    so   49.5578                                $ OR of Reflector

mode n
totnu
kcode   10000  1.0  100  600
imp:n   1   1   1   0
sdef    cel=1  erg=d1
sp1     -3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
