Mirror Geometry - Symmetric Shield Configuration
c
c Original geometry from mcnp-geometry-builder with single-sided shield
c EDITED: Added mirrored copy of shield cell on opposite side
c         Creates symmetric configuration using explicit geometry
c         Original at x>0, mirror at x<0
c
c Cell Cards
c ==========
1    0         -10       IMP:N=1                 $ Source void
c Original shield (x > 0)
10   1  -2.3    10 -11  -20  IMP:N=1  VOL=628.32 $ Concrete shield +x side
c Mirrored shield (x < 0)
11   1  -2.3   -10  11 -20  IMP:N=1  VOL=628.32 $ Concrete shield -x side
c Surrounding regions
20   0          20 -30   IMP:N=1                 $ Detector regions
99   0          30        IMP:N=0                 $ Graveyard

c Surface Cards
c ==============
c Source region
10   PX   5.0             $ Inner shield boundary +x
c Shield boundaries
11   PX  -5.0             $ Inner shield boundary -x (mirror of surf 10)
20   CZ  15.0             $ Shield outer radius
30   SO  50.0             $ Problem boundary

c Data Cards
c ===========
MODE N
c Isotropic point source at origin
SDEF  POS=0 0 0  ERG=14.1
c Material (concrete)
M1   1001   -0.01   &    $ H
     6000   -0.001  &    $ C
     8016   -0.529  &    $ O
     11023  -0.016  &    $ Na
     12000  -0.002  &    $ Mg
     13027  -0.034  &    $ Al
     14000  -0.337  &    $ Si
     20000  -0.044  &    $ Ca
     26000  -0.014       $ Fe
c Tallies (flux beyond each shield)
F5:N  25 0 0  0.5         $ Detector +x side
F15:N -25 0 0  0.5        $ Detector -x side (mirror)
E5    0.1 1.0 10.0 15.0
E15   0.1 1.0 10.0 15.0
NPS  1000000
