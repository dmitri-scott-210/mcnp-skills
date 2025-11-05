Example 03: Rectangular Lattice with Array FILL - Mixed Universe Pattern
c =================================================================
c Description: 5×5 rectangular lattice with FILL array specification
c              Different universes in different positions (fuel vs control rods)
c              Demonstrates Fortran array ordering for FILL card
c
c Lattice Type: LAT=1 (rectangular)
c Dimensions: 5×5×1 = 25 elements
c Element Pitch: 1.26 cm square
c Fill Pattern: Mixed fuel (U=1) and control rod (U=2) positions
c
c Key Concepts:
c   - FILL array specification with dimensions
c   - Fortran ordering: i-index varies FASTEST
c   - Multiple universes in single lattice
c   - Cross-shaped control rod pattern
c
c Author: MCNP Lattice Builder Skill
c Created: 2025-11-04
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Universe 1: Fuel Pin Cell ---
1    1  -10.5  -1         U=1  IMP:N=1  VOL=0.503      $ UO2 fuel
2    0          1  -2     U=1  IMP:N=1  VOL=0.053      $ Gap (void)
3    2  -6.5    2  -3     U=1  IMP:N=1  VOL=0.236      $ Zircaloy clad
4    3  -1.0    3         U=1  IMP:N=1  VOL=1.261      $ Water coolant
c
c --- Universe 2: Control Rod Cell ---
11   4  -10.2  -11        U=2  IMP:N=1  VOL=0.503      $ B4C absorber
12   2  -6.5   11  -12    U=2  IMP:N=1  VOL=0.289      $ Zircaloy tube
13   3  -1.0   12         U=2  IMP:N=1  VOL=1.208      $ Water coolant
c
c --- Universe 10: 5×5 Lattice with Mixed FILL ---
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  IMP:N=1  &
        FILL=0:4 0:4 0:0                               &
             1 1 2 1 1                                 &
             1 1 2 1 1                                 &
             2 2 2 2 2                                 &
             1 1 2 1 1                                 &
             1 1 2 1 1
c        FILL array interpretation:
c        Row 1 (j=0): i=0,1,2,3,4 → 1 1 2 1 1
c        Row 2 (j=1): i=0,1,2,3,4 → 1 1 2 1 1
c        Row 3 (j=2): i=0,1,2,3,4 → 2 2 2 2 2
c        Row 4 (j=3): i=0,1,2,3,4 → 1 1 2 1 1
c        Row 5 (j=4): i=0,1,2,3,4 → 1 1 2 1 1
c
c        Pattern: Cross-shaped control rod arrangement
c                 2 = control rod (U=2)
c                 1 = fuel pin (U=1)
c
c        Visual layout (looking down from +Z):
c        j=4:  F F C F F
c        j=3:  F F C F F
c        j=2:  C C C C C  ← Horizontal bar of cross
c        j=1:  F F C F F
c        j=0:  F F C F F
c              ↑
c              i=0 1 2 3 4
c                    ↑
c                  Vertical bar of cross
c
c --- Real World: Container ---
1000 0  -1000  FILL=10  IMP:N=1                        $ Fill with lattice
1001 3  -1.0   1000 -1001  IMP:N=1                    $ Water reflector
1002 0  1001  IMP:N=0                                  $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Fuel Pin Surfaces (Universe 1) ---
1    CZ   0.4                                          $ Fuel radius
2    CZ   0.42                                         $ Gap outer radius
3    CZ   0.475                                        $ Clad outer radius
c
c --- Control Rod Surfaces (Universe 2) ---
11   CZ   0.4                                          $ Absorber radius
12   CZ   0.5                                          $ Tube outer radius
c
c --- Lattice Element Boundaries (Universe 10) ---
c    5×5 array with 1.26 cm pitch
c    Total size: 6.3 cm × 6.3 cm × 100 cm
10   PX   0.0                                          $ -X boundary (i=0)
11   PX   6.3                                          $ +X boundary (i=4 outer)
12   PY   0.0                                          $ -Y boundary (j=0)
13   PY   6.3                                          $ +Y boundary (j=4 outer)
14   PZ   0.0                                          $ -Z boundary (k=0)
15   PZ   100.0                                        $ +Z boundary (k=0 outer)
c    Lattice pitch: 6.3/5 = 1.26 cm per element
c    Element [i,j,0] spans: X=[1.26*i, 1.26*(i+1)], Y=[1.26*j, 1.26*(j+1)]
c
c --- Container Boundaries (Real World) ---
1000 RPP  -1.0  7.3  -1.0  7.3  -1.0  101.0           $ Inner container
1001 RPP  -5.0  11.3  -5.0  11.3  -5.0  105.0         $ Outer boundary

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials ---
c Material 1: UO2 Fuel (4.5% enriched)
M1   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
c Material 2: Zircaloy-4 Cladding/Tubing
M2   40000.80c  -0.98  26000.80c  -0.01  24000.80c  -0.005  &
     28000.80c  -0.005
c Material 3: Light Water Coolant/Moderator/Reflector
M3   1001.80c  2  8016.80c  1
MT3  LWTR.01T                                          $ S(alpha,beta) at 293 K
c Material 4: B4C Absorber (natural boron)
M4   5010.80c  0.2  5011.80c  0.8  6000.80c  1.0
c --- Source Definition ---
KCODE  10000  1.0  50  150                            $ Criticality calculation
KSRC   3.15 3.15 50                                   $ Initial source at center
c --- Tallies ---
F4:N  (1 < 100[0:4 0:4 0:0])                          $ Flux in all fuel pins
F7:N  (1 < 100[0:4 0:4 0:0])                          $ Fission energy in fuel
c --- Problem Termination ---
c KCODE controls termination (150 cycles total)
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. FILL array format: FILL=imin:imax jmin:jmax kmin:kmax
c      Then list universe numbers in Fortran order:
c      - i varies FASTEST (innermost loop)
c      - j varies MIDDLE (middle loop)
c      - k varies SLOWEST (outermost loop)
c
c   2. Array layout verification:
c      Element [i,j,k] contains universe specified at:
c      position = i + (j-jmin)*(imax-imin+1) + (k-kmin)*(imax-imin+1)*(jmax-jmin+1)
c
c   3. Cross-shaped control rod pattern:
c      - Vertical bar: All j at i=2 (center column)
c      - Horizontal bar: All i at j=2 (center row)
c      - 16 fuel pins + 9 control rods = 25 total elements
c
c   4. Expected physics:
c      - Control rods suppress reactivity
c      - Flux depression in control rod positions
c      - Flux peaking between control rods
c      - k-effective < 1.0 (subcritical with this pattern)
c
c   5. Volumes:
c      - Fuel pins: 16 × 0.503 = 8.05 cm³ UO2
c      - Control rods: 9 × 0.503 = 4.53 cm³ B4C
c
c   6. Verify geometry: mcnp6 inp=example_03.i ip
c      - Plot XY at Z=50 to see cross pattern
c      - Display lattice indices to verify FILL array
c      - Check control rods (red/dark) form cross shape
c
c   7. Modifying FILL pattern:
c      - Change universe numbers in array
c      - Keep Fortran ordering (i fastest)
c      - Total entries must equal (imax-imin+1)×(jmax-jmin+1)×(kmax-kmin+1)
c
c Verification:
c   - Plot XY at Z=50 with material coloring
c   - Verify cross pattern: vertical + horizontal control rods
c   - Count elements: 9 control (B4C), 16 fuel (UO2)
c   - Check flux distribution shows depression at control rods
c   - Run KCODE to verify subcritical (k-eff < 1.0)
c =================================================================
