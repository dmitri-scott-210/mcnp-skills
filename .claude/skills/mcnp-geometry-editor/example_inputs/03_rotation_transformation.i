Rotation Transformation - Cylinder Rotated 45 Degrees
c
c Original geometry from mcnp-geometry-builder with cylinder along x-axis
c EDITED: Added TR1 card to rotate cylinder 45 degrees about z-axis
c         Cylinder now points from +x toward +y direction
c
c Cell Cards
c ==========
1    1  -1.0    -1        IMP:N=1  VOL=628.32     $ Water cylinder - rotated
2    0          1  -2    IMP:N=1                  $ Void
3    0          2         IMP:N=0                  $ Graveyard

c Surface Cards
c ==============
1    1  RCC  0 0 0  10 0 0  2.0    $ Cylinder uses TR1 for 45deg rotation
2    SO   20.0                      $ Problem boundary

c Data Cards
c ===========
MODE N
c Transformation: 45 degree rotation about z-axis
*TR1  0 0 0  0 0 45  1    $ No translation, z-axis rotation, degrees mode
c Source
SDEF  POS=0 0 0  ERG=14.1
c Material
M1   1001  2   8016  1    $ H2O
MT1  LWTR.01T              $ Light water S(a,b)
c Tally
F4:N  1
NPS  50000
