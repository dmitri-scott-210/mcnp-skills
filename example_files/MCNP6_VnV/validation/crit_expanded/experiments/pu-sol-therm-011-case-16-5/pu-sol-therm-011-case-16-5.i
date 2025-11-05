PNL-5  16" Bare Sphere, 43.43g Pu/l, 4.17 wt% Pu-240  PU-SOL-THERM-011 Case 16-5
c   CSEWG: T-17
1   1   1.002582e-1   -1      imp:n=1   $ Pu(NO3)4 Solution 
2   2   8.6914e-2      1 -2   imp:n=1   $ SS347 Sphere 
3   0                  2      imp:n=0   $ Outside Everything 

1   so   20.1206   $ Sphere Inner Radius
2   so   20.2476   $ Sphere Outer Radius

mode   n 
kcode  10000 1. 100 600
sdef   pos 0.0 0.0 0.0  rad d1
sc1    Spherical Source about origin
si1    20.1205
read file=m-cards-endf71
totnu 
prdmp  999999  999999  1  1  999999
