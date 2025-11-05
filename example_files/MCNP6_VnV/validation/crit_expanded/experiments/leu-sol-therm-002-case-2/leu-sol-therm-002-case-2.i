 Bare Sphere of 4.9 wt.% UO2F2-H2O  LEU-SOL-THERM-002  Case 2
1    1    0.098748     -1                        $ UO2F2D2O Solution
2    2    0.060317      1   -2                   $ Alumninum 1100 Shell
3    0                  2

1    so   34.4995                                $ OR of Solution
2    so   34.6583                                $ OR of Shell

mode n
totnu
kcode   10000  1.0  100  600
imp:n   1   1   0
sdef    cel=1  erg=d1
sp1     -3
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
