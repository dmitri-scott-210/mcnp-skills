PNL-11  PU-SOL-THERM-018 case 9  42.9 wt.% Pu-240  Water-Reflected
c  tank with plutonium nitrate solution with traces of Am and Gd
1    1  0.100115  -104 126 -128        $ Fissile Solution
2    2  0.086320   100 -110 120 -122   $ Bottom of Reflector Tank
3    2  0.086320   100 -102 122 -124   $ Support Pipe
4    2  0.086320  -106 124 -126        $ Bottom of Solution Tank
5    2  0.086320   104 -106 126 -130   $ Wall of Solution Tank
6    2  0.086320  -106 130 -132        $ Top of Solution Tank
7    2  0.086320   108 -110 122 -134   $ Wall of Reflector Tank
8    3  0.100037   102 -108 122 -124   $ Water Surrounding Pipe
9    3  0.100037   106 -108 124 -132   $ Water Surrounding Tank
10   0            -100 120 -124        $ Center of Support Pipe
11   0            -104 128 -130        $ Void In Solution Tank
12   0            -108 132 -134        $ Void Above Solution Tank
13   0             110:-120:134

100   cz     2.555                  $ Pipe Inner Radius
102   cz     2.860                  $ Pipe Outer Radius
104   cz    30.514                  $ Solution Tank Inner Radius
106   cz    30.593                  $ Solution Tank Outer Radius
108   cz    50.523                  $ Reflector Tank Inner Radius
110   cz    50.800                  $ Reflector Tank Outer Radius
120   pz     0                      $ Bottom of Reflector Tank
122   pz     0.277                  $ Bottom of Water Reflector
124   pz    21.227                  $ Top of Support Pipe
126   pz    22.177                  $ Bottom of Solution Tank
128   pz   103.097                  $ Fissile Solution Height
130   pz   127.828                  $ Top of Solution Tank
132   pz   127.907                  $ Water Reflector Height
134   pz   143.000                  $ Top of Reflector Tank

kcode  10000  1.0  100 600
imp:n    1.0  11r  0.0
sdef   cel=1  erg=d1  rad=d2  pos 0.0 0.0 62.6
sp1    -3
si2    0.0  30.0
totnu
read file=m-cards-endf71
prdmp  999999  999999  1  1  999999
