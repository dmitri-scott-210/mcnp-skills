Example 02: Hexagonal Lattice - Basic LAT=2 Demonstration
c =================================================================
c Description: Basic hexagonal prism lattice (LAT=2)
c              7-element hex array with central fuel pin
c              Demonstrates LAT=2 surface ordering and indexing
c
c Lattice Type: LAT=2 (hexagonal prism)
c Dimensions: 7 elements (1 center + 6 surrounding)
c Element Pitch: 1.26 cm (flat-to-flat across hexagon)
c Fill Pattern: All elements contain universe 1 (fuel pin)
c
c Key Concepts:
c   - LAT=2 requires 8 surfaces (6 for hex, 2 for top/bottom)
c   - Hexagon orientation: FLAT sides LEFT/RIGHT, POINTS UP/DOWN
c   - Hexagonal indexing follows specific pattern (see manual)
c
c Author: MCNP Lattice Builder Skill
c Created: 2025-11-04
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Universe 1: Fuel Pin Cell (repeated in all lattice elements) ---
1    1  -10.5  -1         U=1  IMP:N=1  VOL=0.503      $ UO2 fuel
2    0          1  -2     U=1  IMP:N=1  VOL=0.053      $ Gap (void)
3    2  -6.5    2  -3     U=1  IMP:N=1  VOL=0.236      $ Zircaloy clad
4    3  -1.0    3         U=1  IMP:N=1  VOL=0.940      $ Water coolant
c
c --- Universe 10: Hexagonal Lattice Cell (7-element array) ---
100  0  -10 11 -12 13 -14 15 -16 17  U=10  LAT=2  FILL=1  IMP:N=1
c        ^  ^   ^  ^   ^  ^   ^  ^
c        8 surfaces required for LAT=2 hexagonal prism:
c        Surfaces 10-15: Six sides of hexagonal prism (in specific order)
c        Surfaces 16-17: Bottom and top of prism (Z-direction)
c
c --- Real World: Cylindrical Container ---
1000 0  -1000  FILL=10  IMP:N=1                        $ Fill with lattice
1001 0   1000 -1001  IMP:N=1                           $ Water outside lattice
1002 0   1001  IMP:N=0                                 $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Fuel Pin Surfaces (Universe 1) ---
1    CZ   0.4                                          $ Fuel radius
2    CZ   0.42                                         $ Gap outer radius
3    CZ   0.475                                        $ Clad outer radius
c
c --- Hexagonal Lattice Element Boundaries (Universe 10) ---
c    Hexagonal prism with flat-to-flat distance = 1.26 cm
c    Regular hexagon: 6 planes at 60° intervals
c    Orientation: Flat sides on LEFT/RIGHT (MCNP convention for LAT=2)
c
c    Hexagon side planes (perpendicular distances from origin)
10   P    0.866025  0.5  0  -0.63                     $ Side 1 (+30°)
11   P    0.0       1.0  0  -0.63                     $ Side 2 (+90°)
12   P   -0.866025  0.5  0  -0.63                     $ Side 3 (+150°)
13   P   -0.866025 -0.5  0  -0.63                     $ Side 4 (-150°)
14   P    0.0      -1.0  0  -0.63                     $ Side 5 (-90°)
15   P    0.866025 -0.5  0  -0.63                     $ Side 6 (-30°)
c    Prism top/bottom
16   PZ   0.0                                          $ Bottom (k=0)
17   PZ   100.0                                        $ Top (k=0, 100 cm height)
c
c    Note: LAT=2 lattice extends automatically to fill surrounding hex elements
c    Central element at origin, 6 surrounding elements in hex pattern
c
c --- Container Boundaries (Real World) ---
1000 RCC  0 0 0  0 0 100  2.5                         $ Cylinder R=2.5 cm, H=100
1001 RCC  0 0 0  0 0 105  3.0                         $ Outer cylinder

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials ---
c Material 1: UO2 Fuel (4.5% enriched)
M1   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
c Material 2: Zircaloy-4 Cladding
M2   40000.80c  -0.98  26000.80c  -0.01  24000.80c  -0.005  &
     28000.80c  -0.005
c Material 3: Light Water Coolant/Moderator
M3   1001.80c  2  8016.80c  1
MT3  LWTR.01T                                          $ S(alpha,beta) at 293 K
c --- Source Definition ---
SDEF  POS=0 0 50  ERG=2.0                             $ 2 MeV at lattice center
c --- Tallies ---
F4:N  (1 < 100)                                       $ Flux in all fuel cells
E4    0.01 0.1 1.0 2.0 2.5 3.0                        $ Energy bins (MeV)
F2:N  1000.1                                          $ Leakage current
c --- Problem Termination ---
NPS   100000
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. LAT=2 hexagonal lattice orientation:
c      - Flat sides on LEFT and RIGHT (X = ±0.63 cm)
c      - Pointed ends UP and DOWN (Y direction)
c      - This is MCNP convention and cannot be changed
c
c   2. Hexagonal indexing pattern (for 7-element array):
c      - Element [0,0,0]: Center
c      - Element [1,0,0]: +X direction (right)
c      - Element [0,1,0]: +Y direction (up-right)
c      - Element [-1,1,0]: -X,+Y (up-left)
c      - Element [-1,0,0]: -X direction (left)
c      - Element [0,-1,0]: -Y direction (down-left)
c      - Element [1,-1,0]: +X,-Y (down-right)
c
c   3. Surface ordering CRITICAL for LAT=2:
c      8 surfaces in specific order (6 hex sides + 2 top/bottom)
c      Order determines how indices map to physical positions
c
c   4. Total fuel volume: 7 pins × 0.503 cm³ = 3.52 cm³
c
c   5. Verify geometry: mcnp6 inp=example_02.i ip
c      - Plot XY at Z=50 to see hexagonal pattern
c      - Display lattice indices to verify arrangement
c
c   6. For different orientation (e.g., points left/right):
c      Use coordinate transformation (TRCL) on filled cell
c
c Verification:
c   - Plot XY at Z=50 (mid-height) with LAT=1 option
c   - Verify 7-element hex pattern visible
c   - Check hexagon has flat sides on left/right
c   - Confirm water fills space between hex elements and cylinder
c =================================================================
