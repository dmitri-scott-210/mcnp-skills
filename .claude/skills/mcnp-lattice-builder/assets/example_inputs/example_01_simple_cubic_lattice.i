Example 01: Simple 3x3x3 Cubic Lattice - Basic LAT=1 Demonstration
c =================================================================
c Description: Basic rectangular lattice (LAT=1) with 27 elements
c              All elements filled with same fuel pin universe
c              Demonstrates simplest lattice usage
c
c Lattice Type: LAT=1 (hexahedral/rectangular)
c Dimensions: 3×3×3 = 27 elements
c Element Pitch: 1.5 cm (X, Y, Z directions)
c Fill Pattern: All elements contain universe 1 (fuel pin)
c
c Key Concepts:
c   - Single universe fills all lattice elements (FILL=1)
c   - Surface ordering defines lattice indexing
c   - LAT=1 requires 6 surfaces (±X, ±Y, ±Z pairs)
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
4    3  -1.0    3         U=1  IMP:N=1  VOL=6.275      $ Water coolant
c
c --- Universe 10: Lattice Cell (3×3×3 array) ---
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
c        ^  ^   ^  ^   ^  ^
c        -X +X  -Y +Y  -Z +Z (surface order defines indices)
c        i varies in X direction (fastest index)
c        j varies in Y direction (middle index)
c        k varies in Z direction (slowest index)
c        Lattice spans: i=0:2, j=0:2, k=0:2 (27 elements total)
c
c --- Real World: Container Filled with Lattice ---
1000 0  -1000  FILL=10  IMP:N=1                        $ Fill with lattice
1001 0   1000  IMP:N=0                                 $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Fuel Pin Surfaces (Universe 1) ---
1    CZ   0.4                                          $ Fuel radius
2    CZ   0.42                                         $ Gap outer radius
3    CZ   0.475                                        $ Clad outer radius
c
c --- Lattice Element Boundaries (Universe 10) ---
c    Element size: 1.5 cm × 1.5 cm × 1.5 cm (cubic)
10   PX   0.0                                          $ -X boundary (i=0)
11   PX   4.5                                          $ +X boundary (i=2 outer)
12   PY   0.0                                          $ -Y boundary (j=0)
13   PY   4.5                                          $ +Y boundary (j=2 outer)
14   PZ   0.0                                          $ -Z boundary (k=0)
15   PZ   4.5                                          $ +Z boundary (k=2 outer)
c    Lattice pitch: (4.5-0.0)/3 = 1.5 cm per element
c
c --- Container Boundary (Real World) ---
1000 RPP  -1.0  5.5  -1.0  5.5  -1.0  5.5              $ Container (1 cm margins)

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
SDEF  POS=2.25 2.25 2.25  ERG=2.0                     $ 2 MeV at lattice center
c --- Tallies ---
F4:N  (1 < 100[0:2 0:2 0:2])                          $ Flux in all fuel cells
c     Tally fuel (cell 1) in all 27 lattice elements
E4    0.01 0.1 1.0 2.0 2.5 3.0                        $ Energy bins (MeV)
c --- Problem Termination ---
NPS   100000
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. FILL=1 means all lattice elements filled with universe 1
c   2. Surface order (-10 11 -12 13 -14 15) critical:
c      - Surfaces 10,11 define X-direction (i-index)
c      - Surfaces 12,13 define Y-direction (j-index)
c      - Surfaces 14,15 define Z-direction (k-index)
c   3. Element [i,j,k] center location:
c      X = 0.75 + 1.5*i
c      Y = 0.75 + 1.5*j
c      Z = 0.75 + 1.5*k
c   4. Total fuel volume: 27 pins × 0.503 cm³ = 13.58 cm³
c   5. Verify geometry: mcnp6 inp=example_01.i ip
c
c Verification:
c   - Plot XY at Z=2.25 to see 3×3 array
c   - Plot XZ at Y=2.25 to see 3×3 vertical array
c   - Check lattice indices displayed correctly
c =================================================================
