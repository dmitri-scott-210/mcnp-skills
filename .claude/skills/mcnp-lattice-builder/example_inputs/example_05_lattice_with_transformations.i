Example 05: Lattice with Coordinate Transformations - Multiple Positioned Arrays
c =================================================================
c Description: Four 3×3 lattices at different positions with rotations
c              Demonstrates TRCL transformations with filled cells
c              Shows how to position multiple lattice instances
c
c Lattice Type: LAT=1 (rectangular)
c Dimensions: 4 lattices, each 3×3×1 = 9 elements
c Element Pitch: 1.26 cm square
c Transformations: 4 different positions with 0°, 90°, 180°, 270° rotations
c
c Key Concepts:
c   - TR card definitions for transformations
c   - FILL with TRCL parameter (inline and reference)
c   - Rotation + translation composition
c   - Multiple instances of same lattice universe
c
c Author: MCNP Lattice Builder Skill
c Created: 2025-11-04
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Universe 1: Fuel Pin Cell ---
1    1  -10.5  -1         U=1  IMP:N=1  VOL=0.503      $ UO2 fuel
2    0          1  -2     U=1  IMP:N=1  VOL=0.053      $ Gap
3    2  -6.5    2  -3     U=1  IMP:N=1  VOL=0.236      $ Clad
4    3  -1.0    3         U=1  IMP:N=1  VOL=1.261      $ Coolant
c
c --- Universe 10: 3×3 Lattice (reused 4 times with transformations) ---
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
c    Single universe (1) fills all 9 elements
c
c --- Real World: Four Lattices at Corners ---
c Quadrant 1: Bottom-left (-10, -10, 0), no rotation
1001 0  -1001  FILL=10 (1 -10 -10 0)  IMP:N=1
c
c Quadrant 2: Bottom-right (+10, -10, 0), 90° rotation about Z
1002 0  -1002  FILL=10 (*TR1)  IMP:N=1
c
c Quadrant 3: Top-left (-10, +10, 0), 270° rotation about Z
1003 0  -1003  FILL=10 (1 -10 10 0  0 0 270)  IMP:N=1
c
c Quadrant 4: Top-right (+10, +10, 0), 180° rotation about Z
1004 0  -1004  FILL=10 (*TR2)  IMP:N=1
c
c Water between lattices and outer boundary
2001 3  -1.0  1001 1002 1003 1004 -2001  IMP:N=1     $ Water
2002 0  2001  IMP:N=0                                 $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Fuel Pin Surfaces (Universe 1) ---
1    CZ   0.4                                          $ Fuel radius
2    CZ   0.42                                         $ Gap outer
3    CZ   0.475                                        $ Clad outer
c
c --- Lattice Element Boundaries (Universe 10) ---
c    3×3 array with 1.26 cm pitch
c    Lattice size: 3.78 cm × 3.78 cm × 100 cm
10   PX   0.0                                          $ -X boundary
11   PX   3.78                                         $ +X boundary
12   PY   0.0                                          $ -Y boundary
13   PY   3.78                                         $ +Y boundary
14   PZ   0.0                                          $ Bottom
15   PZ   100.0                                        $ Top
c
c --- Filled Cell Boundaries (Real World) ---
c    Each lattice contained in RPP box at different position
1001 RPP  -11.89  -8.11  -11.89  -8.11  0  100        $ Quadrant 1 (BL)
1002 RPP    8.11  11.89   -11.89  -8.11  0  100       $ Quadrant 2 (BR)
1003 RPP  -11.89  -8.11    8.11  11.89  0  100        $ Quadrant 3 (TL)
1004 RPP    8.11  11.89    8.11  11.89  0  100        $ Quadrant 4 (TR)
c
c --- Outer Boundary ---
2001 RPP  -20  20  -20  20  -10  110                  $ Problem boundary

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials ---
c Material 1: UO2 Fuel
M1   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
c Material 2: Zircaloy Clad
M2   40000.80c  -0.98  26000.80c  -0.01  24000.80c  -0.005  &
     28000.80c  -0.005
c Material 3: Light Water
M3   1001.80c  2  8016.80c  1
MT3  LWTR.01T
c --- Transformations ---
c TR1: Translate to (+10, -10, 0) and rotate 90° about Z
*TR1  1  10 -10 0  0 0 90
c      ^O  ^displacement   ^rotation angles (Z first)
c      O=1: displacement in main coordinate system
c
c TR2: Translate to (+10, +10, 0) and rotate 180° about Z
*TR2  1  10 10 0  0 0 180
c
c Note: Quadrant 1 uses inline transformation (no TR card)
c Note: Quadrant 3 uses inline transformation (no TR card)
c --- Source Definition ---
SDEF  POS=0 0 50  ERG=2.0                             $ Point source at center
c --- Tallies ---
F4:N  (1 < 100 < 1001)                                $ Flux in quad 1 fuel
      (1 < 100 < 1002)                                $ Flux in quad 2 fuel
      (1 < 100 < 1003)                                $ Flux in quad 3 fuel
      (1 < 100 < 1004)                                $ Flux in quad 4 fuel
c     Tally fuel cells in all four lattice instances
E4    0.1 1.0 2.0 3.0                                 $ Energy bins
c --- Problem Termination ---
NPS   1000000
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. Transformation application order (CRITICAL):
c      a) Rotation applied FIRST (about origin of universe)
c      b) Translation applied SECOND (in main coordinate system)
c
c      Example for TR1:
c        - Universe 10 rotated 90° about its origin (0,0,0)
c        - Rotated universe translated to (+10, -10, 0) in main system
c
c   2. TR card formats:
c      *TR1  O  Bx By Bz  θx θy θz
c      - O=1: Displacement in main system (most common)
c      - O=0: Displacement in auxiliary system (after rotation)
c      - θx, θy, θz: Rotation angles (degrees)
c        Order: Z rotation first, then Y, then X (ZYX sequence)
c
c   3. TRCL usage options:
c      a) Reference TR card: FILL=10 (*TR1)
c         - Reusable transformation
c         - Clean, organized
c      b) Inline: FILL=10 (1 10 -10 0  0 0 90)
c         - Self-contained
c         - Not reusable
c
c   4. Coordinate transformations visualized:
c
c      Before transformation (Universe 10 at origin):
c        +Y
c         |  [0,2]  [1,2]  [2,2]
c         |  [0,1]  [1,1]  [2,1]
c         |  [0,0]  [1,0]  [2,0]
c         +-------------------------> +X
c
c      After 90° Z rotation:
c         +Y
c         |  [2,0]  [2,1]  [2,2]
c         |  [1,0]  [1,1]  [1,2]
c         |  [0,0]  [0,1]  [0,2]
c         +-------------------------> +X
c
c      After translation to (+10, -10, 0):
c         (entire rotated lattice moved to quadrant 2)
c
c   5. Physical layout (XY view from +Z):
c
c         Y
c         ^
c         |  [Q3: 270°]    [Q4: 180°]
c         |
c      ---+------------------------> X
c         |
c         |  [Q1: 0°]      [Q2: 90°]
c
c      Each quadrant contains 3×3 lattice, total 36 pins
c
c   6. Expected flux distribution:
c      - Central source at (0, 0, 50)
c      - Symmetric flux in all quadrants (equal distance)
c      - Rotation doesn't affect physics (geometry invariant)
c
c   7. Volumes:
c      - 4 lattices × 9 pins × 0.503 cm³ = 18.1 cm³ total fuel
c
c   8. Verification:
c      mcnp6 inp=example_05.i ip
c      - Plot XY at Z=50
c      - Verify 4 lattices at corners
c      - Check rotations: pins oriented differently in each quadrant
c      - Confirm water fills space between lattices
c
c   9. Extensions:
c      - Add different lattice types per quadrant (U=10, U=11, etc.)
c      - Include absorber plates between quadrants
c      - Model experimental setup with detector array
c      - Add reflector shells around entire configuration
c
c Verification:
c   - Plot XY at Z=50 with material coloring
c   - Verify 4 separate 3×3 lattices at corners
c   - Check rotations visible in pin arrangement
c   - Confirm water (blue) between lattices
c   - Run simulation: flux should be symmetric across quadrants
c   - Compare F4 tallies: should be similar (geometric symmetry)
c =================================================================
