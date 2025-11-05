90-Degree Rotation Example - Cylinder Reorientation
c =================================================================
c Demonstrates rotation-only TR card (no translation)
c Rotate cylinder 90° CCW about z-axis
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7  -1      IMP:N=1  $ Original cylinder (along +x)
2    1  -2.7  -2      IMP:N=1  $ Rotated cylinder (along +y)
3    0         3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RCC  0 0 0  10 0 0  2      $ Cylinder: origin, axis +x, R=2 cm, H=10 cm
2    1 RCC  0 0 0  10 0 0  2   $ Same cylinder with TR1 applied
3    SO   20.0                  $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
*TR1  0 0 0  0 -1 0  1 0 0  0 0 1    $ Rotation: 90° CCW about z-axis
c Alternative (degree input): *TR1  0 0 0  0 0 90  1
c Matrix interpretation:
c   Row 1: (0, -1, 0)  = new x-axis direction in old coordinates
c   Row 2: (1,  0, 0)  = new y-axis direction in old coordinates
c   Row 3: (0,  0, 1)  = new z-axis direction in old coordinates
c Result: Cylinder axis rotates from +x to +y direction
c --- Particle Mode ---
MODE  N
c --- Material Definition ---
M1    26000.80c  1              $ Iron
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0        $ Point source at origin
c --- Tally Definition ---
F4:N  1 2                       $ Flux in both cylinders
c --- Problem Termination ---
NPS   50000
PRINT
