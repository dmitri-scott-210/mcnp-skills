Transformation Composition Example - Sequential Operations
c =================================================================
c Demonstrates composing two transformations
c TR3 = TR2 ∘ TR1 (apply TR1 first, then TR2)
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -7.85  -1      IMP:N=1  $ Original cylinder (vertical)
2    1  -7.85  -2      IMP:N=1  $ Cylinder with TR3 (composed transformation)
3    0         -3 1 2  IMP:N=1  $ Void around cylinders
4    0           3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RCC  0 0 0  0 0 8  1.5      $ Vertical cylinder: origin, axis +z, R=1.5, H=8
2    3 RCC  0 0 0  0 0 8  1.5    $ Same cylinder with TR3 applied
3    SO   30.0                    $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definitions ---
c TR1: Rotate 90° CCW about z-axis
*TR1  0 0 0  0 -1 0  1 0 0  0 0 1
c TR2: Translate +10 cm in x-direction
*TR2  10 0 0
c TR3: Composition TR3 = TR2 ∘ TR1 (rotate first, then translate)
*TR3  10 0 0  0 -1 0  1 0 0  0 0 1
c Composition calculation:
c   R3 = R2 · R1 = I · R1 = R1 (identity rotation × R1 = R1)
c   d3 = d2 + R2·d1 = (10,0,0) + I·(0,0,0) = (10,0,0)
c Result TR3:
c   Translation: (10, 0, 0)
c   Rotation: Same as TR1 (90° about z)
c Effect on cylinder:
c   1. Rotate: vertical (0,0,0)→(0,0,8) becomes horizontal (0,0,0)→(0,8,0)
c   2. Translate: (0,0,0)→(0,8,0) becomes (10,0,0)→(10,8,0)
c Final: Horizontal cylinder along +y, center at (10, 4, 0)
c Verification:
c   Use scripts/tr_composition.py to verify composition
c   - Input TR1: 0 0 0  0 -1 0  1 0 0  0 0 1
c   - Input TR2: 10 0 0
c   - Output TR3 should match above
c --- Particle Mode ---
MODE  N
c --- Material Definition ---
M1    26000.80c  1              $ Iron (steel cylinder)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0        $ Point source at origin
c --- Tally Definition ---
F4:N  1 2                       $ Flux in both cylinders
c --- Problem Termination ---
NPS   100000
PRINT
