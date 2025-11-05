Transformed Geometry - Rotation demonstration
c
c Example demonstrating:
c   - Transformation card (*TR) usage
c   - Surface transformation (asterisk prefix)
c   - Rotated cylinders in 3D space
c
c Cell Cards
c ==========
1    1  -10.0  -1  IMP:N=1  $ Cylinder along X-axis (transformed)
2    1  -10.0  -2  IMP:N=1  $ Cylinder along Y-axis (transformed)
3    1  -10.0  -3  IMP:N=1  $ Cylinder along Z-axis (no transform)
4    0          1 2 3 -4  IMP:N=1  $ Void between cylinders
5    0          4  IMP:N=0  $ Graveyard

c Surface Cards
c ==============
*1   CZ  5.0  $ Cylinder transformed by TR1 (X-axis)
*2   CZ  5.0  $ Cylinder transformed by TR2 (Y-axis)
3    CZ  5.0  $ Cylinder on Z-axis (not transformed)
4    SO  30.0 $ Outer boundary

c Data Cards
c ===========
MODE N
*TR1  0 0 0  0 0 1  0 1 0  1 0 0  $ Rotate to X-axis
*TR2  0 0 0  0 1 0  1 0 0  0 0 1  $ Rotate to Y-axis
SDEF  POS=0 0 0  ERG=14.1
M1   26000  1.0
NPS  10000
