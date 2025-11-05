PNL-3 18" Cadmium-covered Bare Sphere of Pu Nitrate, 22.35 gPu/l, 4.2 wt% Pu-240
c  PU-SOL-THERM-011 Case 18-1 and CSEWG T-15
1   1   1.004758e-1  -1      imp:n=1   $ Pu(NO3)4 Solution
2   2   8.6914e-2     1 -2   imp:n=1   $ SS347 Sphere
3   3   4.6340e-2     2 -3   imp:n=1   $ Cadmium Cover 
4   0                 3      imp:n=0   $ Outside Everything

1   so   22.6974   $ Sphere Inner Radius
2   so   22.8244   $ Sphere Outer Radius
3   so   22.8752   $ Cadmium Cover Outer Radius

mode    n
kcode   10000 1. 100 600
sdef    pos 0.0 0.0 0.0  rad d1
sc1     Spherical Source about origin 
si1     22.6973
read file=m-cards-endf71
totnu
prdmp  999999  999999  1  1  999999
