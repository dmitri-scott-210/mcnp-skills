Combined Translation and Rotation Example - Fuel Pin Placement
c =================================================================
c Demonstrates combined transformation: rotation + translation
c Fuel pin rotated 90° about y-axis and moved to (20, 15, 0)
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -10.5  -1      IMP:N=1  $ Original fuel pin (vertical)
2    1  -10.5  -2      IMP:N=1  $ Transformed fuel pin (horizontal, offset)
3    2  -1.0   -3 1 2  IMP:N=1  $ Water moderator
4    0           3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RCC  0 0 0  0 0 10  0.5    $ Vertical pin: origin, axis +z, R=0.5, H=10
2    1 RCC  0 0 0  0 0 10  0.5  $ Same pin with TR1 applied
3    BOX  -10 -10 -10  60 0 0  0 60 0  0 0 60    $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
*TR1  20 15 0  0 0 1  0 1 0  -1 0 0    $ Rotate 90° y-axis, translate (20,15,0)
c Breakdown:
c   Translation: (20, 15, 0) = final position offset
c   Rotation matrix (90° about y):
c     Row 1: ( 0,  0,  1) = new x-axis = old +z direction
c     Row 2: ( 0,  1,  0) = new y-axis = old +y direction
c     Row 3: (-1,  0,  0) = new z-axis = old -x direction
c Result:
c   1. Pin rotates: vertical (0,0,0)→(0,0,10) becomes horizontal (0,0,0)→(10,0,0)
c   2. Pin translates: (0,0,0)→(10,0,0) becomes (20,15,0)→(30,15,0)
c --- Particle Mode ---
MODE  N
c --- Material Definitions ---
M1    92235.80c  0.04  92238.80c  0.96    $ UO2 fuel (simplified)
      8016.80c   2.0
M2    1001.80c   2  8016.80c  1           $ Water moderator
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0                  $ Point source at origin
c --- Tally Definition ---
F4:N  1 2                                 $ Flux in both fuel pins
c --- Problem Termination ---
NPS   100000
PRINT
