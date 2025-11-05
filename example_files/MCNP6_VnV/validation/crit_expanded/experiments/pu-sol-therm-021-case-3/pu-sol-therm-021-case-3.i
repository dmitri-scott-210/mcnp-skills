PNL-6  PU-SOL-THERM-021 Case 3  15.2-inch Sphere of Plutonium Nitrate
c  CSEWG: T-14
1    1  0.099270         -1            $ Plutonium Nitrate Solution
2    2  0.086240         -2   1        $ Stainless Steel Container
3    0                    2

1   so  19.3163
2   so  19.4382

kcode    10000    1.0    100   600
imp:n   1.0  1.0  0.0
sdef   cel=1  erg=d1
sp1    -3
read file=m-cards-endf71
totnu
prdmp  999999  999999  1  1  999999
