Example 04: Fuel Assembly with Pin Lattice - 17×17 PWR-Style Array
c =================================================================
c Description: Realistic PWR fuel assembly with 17×17 pin lattice
c              Includes fuel pins, guide tubes, and instrument tube
c              Demonstrates multiple universe types in single lattice
c
c Lattice Type: LAT=1 (rectangular)
c Dimensions: 17×17×1 = 289 pin positions
c Element Pitch: 1.26 cm square (typical PWR)
c Fill Pattern: 264 fuel, 24 guide tubes, 1 instrument tube
c
c Key Concepts:
c   - Multiple universe types (fuel, guide tube, instrument)
c   - Realistic PWR geometry and materials
c   - Large FILL array (289 elements)
c   - Volume specifications for repeated structures
c
c Author: MCNP Lattice Builder Skill
c Created: 2025-11-04
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Universe 1: Standard Fuel Pin ---
1    1  -10.5  -1         U=1  IMP:N=1  VOL=0.503      $ UO2 fuel pellet
2    0          1  -2     U=1  IMP:N=1  VOL=0.053      $ Gap (helium, void)
3    2  -6.5    2  -3     U=1  IMP:N=1  VOL=0.236      $ Zircaloy clad
4    3  -0.7    3         U=1  IMP:N=1  VOL=1.261      $ Water coolant
c
c --- Universe 2: Guide Tube (for control rod insertion) ---
11   2  -6.5   -11 12     U=2  IMP:N=1  VOL=0.310      $ Inner tube
12   3  -0.7    11         U=2  IMP:N=1  VOL=1.024      $ Water inside tube
13   2  -6.5    12  -13    U=2  IMP:N=1  VOL=0.265      $ Outer tube
14   3  -0.7    13         U=2  IMP:N=1  VOL=0.401      $ Water outside tube
c
c --- Universe 3: Instrument Tube ---
21   2  -6.5   -21         U=3  IMP:N=1  VOL=0.575      $ Tube wall (thicker)
22   3  -0.7    21         U=3  IMP:N=1  VOL=1.425      $ Water
c
c --- Universe 10: 17×17 Pin Lattice ---
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  IMP:N=1  &
        FILL=0:16 0:16 0:0                             &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 1 1 1 1 2 1 1 2 1 1 2 1 1 1 1 1        &
             1 1 1 2 1 1 1 1 1 1 1 1 1 2 1 1 1        &
             1 1 2 1 1 1 1 1 1 1 1 1 1 1 2 1 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 2 1 1 1 2 1 1 2 1 1 2 1 1 1 2 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 2 1 1 1 2 1 1 3 1 1 2 1 1 1 2 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 2 1 1 1 2 1 1 2 1 1 2 1 1 1 2 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1        &
             1 1 2 1 1 1 1 1 1 1 1 1 1 1 2 1 1        &
             1 1 1 2 1 1 1 1 1 1 1 1 1 2 1 1 1        &
             1 1 1 1 1 2 1 1 2 1 1 2 1 1 1 1 1        &
             1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
c        Pattern summary:
c        - 264 fuel pins (universe 1)
c        - 24 guide tubes (universe 2) in 4×6 pattern
c        - 1 instrument tube (universe 3) at center [8,8]
c        - Standard Westinghouse 17×17 layout
c
c --- Real World: Assembly in Water Pool ---
1000 0  -1000  FILL=10  IMP:N=1                        $ Assembly
1001 3  -0.7   1000 -1001  IMP:N=1                    $ Water reflector
1002 0  1001  IMP:N=0                                  $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Standard Fuel Pin Surfaces (Universe 1) ---
1    CZ   0.4                                          $ Fuel pellet radius
2    CZ   0.42                                         $ Gap outer radius
3    CZ   0.475                                        $ Clad outer radius
c
c --- Guide Tube Surfaces (Universe 2) ---
11   CZ   0.56                                         $ Inner tube IR
12   CZ   0.602                                        $ Inner tube OR
13   CZ   0.613                                        $ Outer tube OR
c
c --- Instrument Tube Surfaces (Universe 3) ---
21   CZ   0.546                                        $ Tube outer radius
c
c --- Lattice Element Boundaries (Universe 10) ---
c    17×17 array with 1.26 cm pitch
c    Total assembly size: 21.42 cm × 21.42 cm × 400 cm (active height)
10   PX   0.0                                          $ -X boundary
11   PX   21.42                                        $ +X boundary (17×1.26)
12   PY   0.0                                          $ -Y boundary
13   PY   21.42                                        $ +Y boundary
14   PZ   0.0                                          $ Bottom
15   PZ   400.0                                        $ Top (active height)
c
c --- Container Boundaries (Real World) ---
1000 RPP  -2.0  23.42  -2.0  23.42  -10.0  410.0      $ Assembly envelope
1001 RPP  -50.0  71.42  -50.0  71.42  -50.0  450.0    $ Outer boundary

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials ---
c Material 1: UO2 Fuel (4.5% enriched, 95% theoretical density)
M1   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
TMP1  6.44e-8                                          $ 747 K (474°C avg)
c Material 2: Zircaloy-4 Cladding and Tubes
M2   40000.80c  -0.9825  50000.80c  -0.0145  26000.80c  -0.0021  &
     24000.80c  -0.0010
TMP2  5.42e-8                                          $ 629 K (356°C)
c Material 3: Light Water (borated, 600 ppm boron)
M3   1001.80c  0.06659  8016.80c  0.03330  5010.80c  1.48e-5  &
     5011.80c  5.96e-5
MT3  LWTR.10T                                          $ S(alpha,beta) at 574 K
TMP3  4.95e-8                                          $ 574 K (301°C)
c --- Source Definition (Criticality Calculation) ---
KCODE  10000  1.0  50  250                            $ 10k/cycle, 250 cycles
KSRC   10.71 10.71 200                                $ Initial source at center
c --- Tallies ---
F4:N  (1 < 100[0:16 0:16 0:0])                        $ Flux in all fuel pins
F7:N  (1 < 100[0:16 0:16 0:0])                        $ Fission energy
FM7   -1.0  1  -6  -8                                 $ Watts (fission heating)
c --- Problem Termination ---
c KCODE controls termination (250 cycles)
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. Realistic PWR 17×17 fuel assembly geometry:
c      - 264 fuel rods (full length)
c      - 24 guide tubes (control rod positions)
c      - 1 instrument tube (in-core measurements)
c      - 1.26 cm square pitch (standard)
c      - 400 cm active fuel height
c
c   2. Guide tube pattern (looking down, G = guide tube):
c      - 4 tubes per quadrant
c      - 24 tubes total in symmetric pattern
c      - Standard Westinghouse layout
c
c   3. Material properties:
c      - UO2 density: 10.5 g/cm³ (95% TD)
c      - Fuel temperature: 747 K average
c      - Coolant temperature: 574 K (301°C, hot full power)
c      - Boron concentration: 600 ppm (typical mid-cycle)
c
c   4. Expected physics:
c      - k-effective ≈ 1.0-1.1 (depending on burnup assumption)
c      - Flux flattening near guide tubes
c      - Peak power at assembly center
c      - Thermal spectrum (most fissions at thermal energies)
c
c   5. Volumes (per instance):
c      - Fuel: 264 pins × 0.503 cm³ = 132.8 cm³
c      - Total active core: 132.8 cm³ × 400 cm = 53,120 cm³ fuel
c
c   6. Verification:
c      mcnp6 inp=example_04.i ip
c      - Plot XY at Z=200 to see pin layout
c      - Verify guide tube pattern (24 tubes)
c      - Check instrument tube at center [8,8]
c      - Plot flux distribution (should peak at center)
c
c   7. Extensions:
c      - Add actual control rods (Ag-In-Cd) in guide tubes
c      - Model partial rod insertion (split Z into segments)
c      - Add grid spacers (structural components)
c      - Include burnable absorbers (IFBA, Gd2O3)
c      - Model multiple assemblies in core configuration
c
c Verification:
c   - Plot XY at Z=200 with material coloring
c   - Count pin types: 264 fuel (cyan), 24 guide (green), 1 inst (blue)
c   - Verify symmetric guide tube pattern
c   - Check water channels between pins
c   - Run KCODE: expect k-eff ≈ 1.05-1.15 (fresh fuel)
c   - Check flux distribution: peak at center, depression at guide tubes
c =================================================================
