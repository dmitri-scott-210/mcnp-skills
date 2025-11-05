PNL-1  PU-SOL-THERM-021 case 1  Unreflected sphere of plutonium-nitrate solution
c  CSEWG T13
1    1    0.100785  -1          $ Plutonium-nitrate solution
2    2    0.086240   1  -2      $ Stainless steel shell
3    0               2

1    so  19.3304                $ Outer radius of solution
2    so  19.4523                $ Outer radius of shell

kcode  10000 1. 100 600
imp:n  1  1  0
sdef   pos 0.0 0.0 0.0  rad d1
sc1    Spherical Source
si1    19.3
totnu
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
