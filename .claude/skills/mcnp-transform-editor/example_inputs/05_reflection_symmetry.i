Reflection Symmetry Example - Mirrored Shielding Blocks
c =================================================================
c Demonstrates reflection transformation for symmetric geometry
c Shield block in +X reflected to -X across YZ plane
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -11.35  -1      IMP:N=1  $ Original lead block (+X side)
2    1  -11.35  -2      IMP:N=1  $ Reflected lead block (-X side)
3    2  -1.0    -3 1 2  IMP:N=1  $ Water between and around blocks
4    0            3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    BOX  5 -2 -2  3 0 0  0 4 0  0 0 4    $ Box: corner (5,-2,-2), 3×4×4 cm
2    1 BOX  5 -2 -2  3 0 0  0 4 0  0 0 4  $ Same box with TR1 (reflected)
3    SO   20.0                             $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
*TR1  0 0 0  -1 0 0  0 1 0  0 0 1    $ Reflection across YZ plane
c Reflection matrix explanation:
c   Row 1: (-1,  0,  0) → new x = -old x (flipped)
c   Row 2: ( 0,  1,  0) → new y = old y (unchanged)
c   Row 3: ( 0,  0,  1) → new z = old z (unchanged)
c Determinant = (-1)·(1)·(1) - 0 - 0 = -1 (improper rotation)
c Result:
c   Original box center: (6.5, 0, 0)
c   Reflected box center: (-6.5, 0, 0)
c   Perfect mirror symmetry across YZ plane
c --- Particle Mode ---
MODE  N
c --- Material Definitions ---
M1    82000.80c  1              $ Lead (Pb)
M2    1001.80c  2  8016.80c  1  $ Water (H2O)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0        $ Point source at center (YZ plane)
c --- Tally Definition ---
F4:N  1 2                       $ Flux in both shield blocks
c --- Problem Termination ---
NPS   100000
PRINT
