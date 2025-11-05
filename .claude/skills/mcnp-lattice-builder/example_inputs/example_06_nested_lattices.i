Example 06: Nested Lattices - Three-Level Hierarchy (Pin → Assembly → Core)
c =================================================================
c Description: Multi-level lattice hierarchy demonstrating nesting
c              3 levels: Pin lattice → Assembly → Core lattice
c              Shows universe hierarchy for reactor modeling
c
c Hierarchy:
c   Level 1: Pin cells (U=1 fuel, U=2 control)
c   Level 2: 5×5 pin assembly lattice (U=10)
c   Level 3: 3×3 core lattice of assemblies (U=100)
c   Real World: Core in water tank (U=0)
c
c Key Concepts:
c   - Multi-level universe nesting (up to 20 levels allowed)
c   - FILL within FILL (lattice contains lattice)
c   - Coordinate systems at each level
c   - Volume accounting across hierarchy
c
c Author: MCNP Lattice Builder Skill
c Created: 2025-11-04
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- LEVEL 1: Pin Cell Universes ---
c Universe 1: Standard Fuel Pin
1    1  -10.5  -1         U=1  IMP:N=1  VOL=0.503      $ UO2 fuel
2    0          1  -2     U=1  IMP:N=1  VOL=0.053      $ Gap
3    2  -6.5    2  -3     U=1  IMP:N=1  VOL=0.236      $ Clad
4    3  -1.0    3         U=1  IMP:N=1  VOL=1.261      $ Water
c
c Universe 2: Control Rod Position (water-filled guide tube)
11   2  -6.5   -11 12     U=2  IMP:N=1  VOL=0.310      $ Inner tube
12   3  -1.0    11         U=2  IMP:N=1  VOL=1.024      $ Water inside
13   2  -6.5    12  -13    U=2  IMP:N=1  VOL=0.265      $ Outer tube
14   3  -1.0    13         U=2  IMP:N=1  VOL=0.401      $ Water outside
c
c --- LEVEL 2: Assembly Lattice Universe (5×5 pins) ---
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  IMP:N=1  &
        FILL=0:4 0:4 0:0                               &
             1 1 1 1 1                                 &
             1 2 1 2 1                                 &
             1 1 1 1 1                                 &
             1 2 1 2 1                                 &
             1 1 1 1 1
c    Assembly pattern: 21 fuel pins + 4 control rod positions
c    Control rods at [1,1], [3,1], [1,3], [3,3] (symmetric pattern)
c
c --- LEVEL 3: Core Lattice Universe (3×3 assemblies) ---
1000 0  -100 101 -102 103 -104 105  U=100  LAT=1  FILL=10  IMP:N=1
c    All core positions filled with same assembly type (U=10)
c    In realistic model, could have different assembly types
c
c --- LEVEL 0: Real World (Universe 0) ---
c Core in cylindrical water tank
10000 0  -10000  FILL=100  IMP:N=1                    $ Core lattice
10001 3  -1.0   10000 -10001  IMP:N=1                $ Water reflector
10002 4  -7.8   10001 -10002  IMP:N=1                $ Steel tank
10003 0  10002  IMP:N=0                               $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- LEVEL 1: Pin Surfaces ---
1    CZ   0.4                                          $ Fuel radius
2    CZ   0.42                                         $ Gap outer
3    CZ   0.475                                        $ Clad outer
c
c --- LEVEL 1: Control Rod Tube Surfaces ---
11   CZ   0.56                                         $ Inner tube IR
12   CZ   0.602                                        $ Inner tube OR
13   CZ   0.613                                        $ Outer tube OR
c
c --- LEVEL 2: Assembly Lattice Element (Pin Pitch: 1.26 cm) ---
10   PX   0.0                                          $ -X
11   PX   6.3                                          $ +X (5 × 1.26)
12   PY   0.0                                          $ -Y
13   PY   6.3                                          $ +Y (5 × 1.26)
14   PZ   0.0                                          $ Bottom
15   PZ   100.0                                        $ Top (1 m active height)
c    Assembly size: 6.3 cm × 6.3 cm × 100 cm
c
c --- LEVEL 3: Core Lattice Element (Assembly Pitch: 7 cm) ---
100  PX   0.0                                          $ -X
101  PX   21.0                                         $ +X (3 × 7.0)
102  PY   0.0                                          $ -Y
103  PY   21.0                                         $ +Y (3 × 7.0)
104  PZ   -5.0                                         $ Bottom (includes reflector)
105  PZ   105.0                                        $ Top (includes reflector)
c    Core size: 21 cm × 21 cm × 110 cm (including axial reflector)
c    Inter-assembly gap: 7.0 - 6.3 = 0.7 cm water
c
c --- LEVEL 0: Real World Tank ---
10000 RCC  0 0 0  0 0 110  12.5                       $ Core boundary
10001 RCC  0 0 0  0 0 115  15.0                       $ Water tank inner
10002 RCC  0 0 0  0 0 120  15.5                       $ Tank outer

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials ---
c Material 1: UO2 Fuel (4.5% enriched)
M1   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
c Material 2: Zircaloy Cladding/Tubes
M2   40000.80c  -0.98  26000.80c  -0.01  24000.80c  -0.005  &
     28000.80c  -0.005
c Material 3: Light Water (Moderator/Reflector)
M3   1001.80c  2  8016.80c  1
MT3  LWTR.01T                                          $ S(alpha,beta)
c Material 4: Stainless Steel Tank
M4   26000.80c  -0.70  24000.80c  -0.19  28000.80c  -0.10  &
     25055.80c  -0.01
c --- Source Definition (Criticality) ---
KCODE  10000  1.0  50  200                            $ 10k/cycle, 200 cycles
KSRC   10.5 10.5 50                                   $ Initial at core center
c --- Tallies ---
c Tally fuel flux in all assemblies (9 assemblies total)
F4:N  (1 < 100 < 1000[0:2 0:2 0:0])
c     ^cell   ^pin    ^assembly lattice indices
c     Tallies fuel (cell 1) in pin lattice (U=100) in all 9 core positions
c
c Fission energy deposition in fuel
F7:N  (1 < 100 < 1000[0:2 0:2 0:0])
c --- Problem Termination ---
c KCODE controls termination
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. Three-level hierarchy structure:
c
c      Universe 0 (Real World)
c        └─ Universe 100 (Core lattice, 3×3 assemblies)
c             └─ Universe 10 (Assembly lattice, 5×5 pins)
c                  ├─ Universe 1 (Fuel pin) ← 21 per assembly
c                  └─ Universe 2 (Control tube) ← 4 per assembly
c
c   2. Coordinate systems:
c      - Universe 1/2: Pin coordinates (origin at pin center)
c      - Universe 10: Assembly coordinates (origin at assembly corner)
c      - Universe 100: Core coordinates (origin at core corner)
c      - Universe 0: Real world (tank coordinates)
c
c   3. Particle tracking example:
c      Neutron born at (10.5, 10.5, 50) in real world:
c      - U=0: Check if in filled cell 10000 → YES, enter U=100
c      - U=100: Transform to core lattice coordinates → element [1,1,0]
c      - U=100 element [1,1,0] filled with U=10 (assembly)
c      - U=10: Transform to assembly lattice coordinates → element [2,2,0]
c      - U=10 element [2,2,0] filled with U=1 (fuel pin)
c      - U=1: Check which cell within pin → cell 1 (fuel pellet)
c      - Transport in fuel, sample physics
c
c   4. Total geometry:
c      - 3×3 = 9 assemblies in core
c      - 5×5 = 25 pin positions per assembly
c      - 21 fuel + 4 control per assembly
c      - Total: 9 × 21 = 189 fuel pins
c      - Total: 9 × 4 = 36 control rod positions
c
c   5. Volume accounting:
c      - Fuel per pin: 0.503 cm³
c      - Fuel per assembly: 21 × 0.503 = 10.56 cm³
c      - Total core fuel: 189 × 0.503 = 95.07 cm³
c      - Active core volume: 21 × 21 × 100 = 44,100 cm³
c
c   6. Lattice pitch considerations:
c      - Pin pitch: 1.26 cm (P/D ratio ≈ 2.65)
c      - Assembly pitch: 7.0 cm (includes 0.7 cm water gap)
c      - Water gap allows thermal expansion, assembly handling
c
c   7. Expected physics:
c      - k-effective ≈ 1.0-1.1 (depends on enrichment, geometry)
c      - Flux peak at core center
c      - Flux depression near control rod positions
c      - Reflector savings: ~10-15% higher flux at core edge
c
c   8. Verification:
c      mcnp6 inp=example_06.i ip
c      - Plot XY at Z=50: See 3×3 core pattern
c      - Zoom to single assembly: See 5×5 pin pattern
c      - Zoom to single pin: See fuel/clad/coolant
c      - Verify water gaps between assemblies
c      - Check reflector surrounds core
c
c   9. Extensions for realism:
c      - Different assembly types (U=10, U=11, U=12) for varied enrichment
c      - Fresh vs burned assemblies (different materials)
c      - Actual control rod material (Ag-In-Cd, B4C) in U=2
c      - Partial rod insertion (split Z into multiple lattices)
c      - Grid spacers between assembly levels
c      - Fuel assembly shroud/can
c      - Burnable absorbers in some pins
c
c  10. Nesting depth:
c      This example: 4 levels (U=0 → 100 → 10 → 1)
c      MCNP allows: Up to 20 hierarchical levels
c      Practical limit: 5-7 levels (complexity management)
c
c  11. Performance considerations:
c      - Each universe crossing requires coordinate transformation
c      - 4-level hierarchy: Minimal overhead (<1% runtime impact)
c      - Geometry plotting: May be slow for large hierarchies
c      - Tallying: Can specify level explicitly (see F4 card)
c
c Verification:
c   - Plot XY at Z=50 (mid-core height)
c   - Verify 3×3 core lattice visible
c   - Zoom in: Verify 5×5 pin lattice per assembly
c   - Zoom more: Verify individual pin structure (fuel/clad/water)
c   - Run KCODE: Expect k-eff ≈ 1.0-1.1
c   - Check tally: Fuel flux should peak at core center
c   - Verify reflector effect: Flux boost at core periphery
c =================================================================
