Simple Translation - Component Moved Along Axis
c
c Original geometry from mcnp-geometry-builder with detector at origin
c EDITED: Added TR2 to translate detector sphere to x=50 cm
c         Allows placement away from source region
c
c Cell Cards
c ==========
1    0         -1        IMP:N=1                  $ Source void
2    1  -1.0    -2       TRCL=2  IMP:N=1  VOL=33.51  $ Detector - translated
3    0          1  2 -3  IMP:N=1                  $ Air gap
4    0          3         IMP:N=0                  $ Graveyard

c Surface Cards
c ==============
1    SO   5.0             $ Source boundary
2    SO   2.0             $ Detector sphere (at origin of TR2 system)
3    SO   100.0           $ Problem boundary

c Data Cards
c ===========
MODE N
c Transformation: translation only
*TR2  50 0 0              $ Move detector to x=50 cm
c Source at origin
SDEF  POS=0 0 0  ERG=14.1
c Material (He-3 detector)
M1   2003  1.0            $ He-3
c Tally in detector
F4:N  2
E4    0.001 0.01 0.1 1.0 10.0 15.0
NPS  1000000
