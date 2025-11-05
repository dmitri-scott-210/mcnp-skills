B&W Criticals  Core XI Load 11  1384 PPM  LEU-COMP-THERM-008 case 11
c    Axially uniform quadrant
1     1   0.068525    -18                 u=1                 $ Fuel Pin
2     2   0.055323     18  -19            u=1                 $ Cladding
3     3   0.10018      19                 u=1                 $ Water
4     4   0.038393    -24                 u=2                 $ Al2O3 Rod
5     5   0.058854     24  -25            u=2                 $ Al2O3 Cladding
6     3   0.10018      25                 u=2                 $ Water
7     0                20  -21   22  -23  u=3  lat=1  fill=1  $ Fuel Pin Cell
c    15x15 Assembly Lattice
8     3   0.10018     -21   20  -23   22  u=4  lat=1  
      fill=-7:7 -7:7 0:0
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  1  1  1  2  1  1  1  2  1  1  1  1  1
      1  1  1  2  1  1  1  1  1  1  1  2  1  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  2  1  1  2  1  1  1  2  1  1  2  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  1  1  1  1  1  4  1  1  1  1  1  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  2  1  1  2  1  1  1  2  1  1  2  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  1  2  1  1  1  1  1  1  1  2  1  1  1
      1  1  1  1  1  2  1  1  1  2  1  1  1  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
      1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
9     0                26  -27   28  -29  u=5 lat=1  fill=4   $ Assemblies
10    0                 1   -2    3    4   -8  -14   fill=5   $ Inner Core
11    0                 1   -2    3    8  -11  -12   fill=3   $ Buffer Zone
12    0                 1   -2    8  -10   12  -13   fill=3   $ Buffer Zone
13    0                 1   -2    8   -9   13  -14   fill=3   $ Buffer Zone
14    0                 1   -2    4   -9   14  -15   fill=3   $ Buffer Zone
15    0                 1   -2    4   -7   15  -16   fill=3   $ Buffer Zone
16    0                 1   -2    4   -6   16  -17   fill=3   $ Buffer Zone
17    3   0.10018       1   -2    3   -5   11                 $ Reflector
18    3   0.10018       1   -2   -5   10  -11   12            $ Reflector
19    3   0.10018       1   -2   -5    9  -10   13            $ Reflector
20    3   0.10018       1   -2   -5    7   -9   15            $ Reflector
21    3   0.10018       1   -2   -5    6   -7   16            $ Reflector
22    3   0.10018       1   -2    4   -5   -6   17            $ Reflector
23    0                -1:2:-3:-4:5

c     Problem Boundaries
1     pz    -81.662                                           $ Bottom
2     pz     81.662                                           $ Top
*3    py      0.0                                             $ Front Edge
*4    px      0.0                                             $ Left Edge
5     cz     76.200                                           $ Tank IR
c     Interior Boundaries
6     px     17.17540                                         $ Buffer
7     px     33.53300                                         $ Buffer
8     px     36.80460                                         $ Inner Core
9     px     49.89060                                         $ Buffer
10    px     58.06940                                         $ Buffer
11    px     66.24820                                         $ Buffer
12    py     17.17540                                         $ Buffer
13    py     33.53300                                         $ Buffer
14    py     36.80460                                         $ Inner Core
15    py     49.89060                                         $ Buffer
16    py     58.06940                                         $ Buffer
17    py     66.24820                                         $ Buffer
c     Pin Cell Boundaries
18    cz      0.514858                                        $ Pellet OR
19    cz      0.602996                                        $ Cladding OR
20    px     -0.81788                                         $ Left Edge
21    px      0.81788                                         $ Right Edge
22    py     -0.81788                                         $ Front Edge
23    py      0.81788                                         $ Back Edge
c     Pyrex Rod Coundaries
24    cz      0.46650                                         $ Al2O3 Rod OD
25    cz      0.55550                                         $ Al2O3 Clad OD
c     Assembly Boundaries
26    px    -12.26820                                         $ Left Edge
27    px     12.26820                                         $ Right Edge
28    py    -12.26820                                         $ Front Edge
29    py     12.26820                                         $ Back Edge

mode      n
kcode    10000    1.0   100   600
imp:n    1.0  21r  0.0
sdef     x=d1  y=d2  z=d3
si1       0.1     49.8
sp1        0        1
si2       0.1     49.8 
sp2        0        1
si3     -81.6     81.6
sp3        0        1
read file=m-cards-endf71
totnu
prdmp  999999  999999  1  1  999999
