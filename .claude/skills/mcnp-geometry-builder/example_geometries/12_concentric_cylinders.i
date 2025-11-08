c ============================================================
c CONCENTRIC CYLINDER EXAMPLE
c 7-layer capsule structure (AGR-1 pattern)
c ============================================================
c
c Demonstrates:
c  - Multiple concentric cylinders (C/Z off-axis)
c  - Thin gap regions (< 1 mm)
c  - Shared axial planes
c  - Realistic reactor component geometry
c
c Based on: AGR-1 HTGR irradiation experiment
c
c ============================================================

c ------------------------------------------------------------
c CELLS
c ------------------------------------------------------------

c Concentric layers (all centered at 25.337, -25.337)
1   1  -10.9   -1              -10 11  imp:n=1  $ Fuel compact
2   0          1  -2           -10 11  imp:n=1  $ Gas gap (0.6 mm)
3   2  -1.75   2  -3           -10 11  imp:n=1  $ Graphite holder
4   0          3  -4           -10 11  imp:n=1  $ Gap (6.8 mm)
5   3  -8.0    4  -5           -10 11  imp:n=1  $ SS wall (3.4 mm)
6   4  -13.3   5  -6           -10 11  imp:n=1  $ Hafnium shroud (2.5 mm)
7   3  -8.0    6  -7           -10 11  imp:n=1  $ Outer wall (13.8 mm)
8   5  -1.2e-3 7              -10 11  imp:n=1  $ Air outside
9   0          11                      imp:n=0  $ Graveyard

c ------------------------------------------------------------
c SURFACES
c ------------------------------------------------------------

c Concentric cylinders (all c/z with same center)
c Critical: ALL surfaces MUST have same (x,y) center
1   c/z  25.337  -25.337  0.6350    $ Compact (6.35 mm)
2   c/z  25.337  -25.337  0.6413    $ Gas gap outer (6.41 mm)
3   c/z  25.337  -25.337  1.5191    $ Holder outer (15.19 mm)
4   c/z  25.337  -25.337  1.5875    $ Gap outer (15.88 mm)
5   c/z  25.337  -25.337  1.6218    $ SS wall outer (16.22 mm)
6   c/z  25.337  -25.337  1.6472    $ Hf shroud outer (16.47 mm)
7   c/z  25.337  -25.337  1.7856    $ Outer wall outer (17.86 mm)

c Axial planes (shared by all cylinders)
10  pz  0.0       $ Bottom
11  pz  50.0      $ Top

c ------------------------------------------------------------
c DATA CARDS
c ------------------------------------------------------------

mode n
sdef pos=25.337 -25.337 25  erg=2.0
nps 10000

c Materials
m1  $ Fuel compact (UCO simplified)
   92235.00c  0.20
   92238.00c  0.80
    6012.00c  0.50
    8016.00c  1.50

m2  $ Graphite holder
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t

m3  $ Stainless steel 316L
   26000.50c  0.65
   24000.50c  0.17
   28000.50c  0.12
   42000.60c  0.025
   25055.70c  0.020
   14000.60c  0.010
   15031.70c  0.005

m4  $ Hafnium
   72000.60c  1.0

m5  $ Air
    7014.70c  0.8
    8016.70c  0.2

c ============================================================
c VERIFICATION
c ============================================================
c
c Visual check (MCNP plotter):
c  mcnp6 inp=12_concentric_cylinders.i ip
c  origin 25.337 -25.337 25
c  extent 5 5 50
c  basis 1 0 0  0 1 0
c
c Expected: 7 concentric circles in XY view
c
c Numerical verification:
c  - All C/Z surfaces have same center: (25.337, -25.337) ✓
c  - Radii strictly increasing:
c    0.6350 < 0.6413 < 1.5191 < 1.5875 < 1.6218 < 1.6472 < 1.7856 ✓
c  - Axial planes shared: -10 and 11 used by all cells ✓
c
c Gap thicknesses:
c  Gas gap: 0.6413 - 0.6350 = 0.0063 cm = 0.63 mm
c  Inner gap: 1.5875 - 1.5191 = 0.0684 cm = 6.84 mm
c  SS wall: 1.6218 - 1.5875 = 0.0343 cm = 3.43 mm
c  Hf shroud: 1.6472 - 1.6218 = 0.0254 cm = 2.54 mm
c  Outer wall: 1.7856 - 1.6472 = 0.1384 cm = 13.84 mm
c
c Volume calculations (verification):
c  V_shell = π h (R_outer² - R_inner²)
c  V_compact = π × 50.0 × (0.6350)² = 63.38 cm³
c  V_gas = π × 50.0 × (0.6413² - 0.6350²) = 0.251 cm³
c  V_holder = π × 50.0 × (1.5191² - 0.6413²) = 298.1 cm³
c
c ============================================================
c NOTES
c ============================================================
c
c Key Features:
c 1. All C/Z surfaces share center (25.337, -25.337)
c    - This is CRITICAL for concentric geometry
c    - Different centers → overlapping/non-concentric regions
c
c 2. Radii strictly increasing (6.35 → 17.86 mm)
c    - MCNP will error if radii not monotonic
c    - Check: R1 < R2 < R3 < ... < R7
c
c 3. Thin gaps carefully sized
c    - Gas gap: 0.63 mm (may cause tracking issues if < 0.1 mm)
c    - Consider homogenizing very thin gaps
c
c 4. Axial planes shared across all layers
c    - Single PZ surface bounds all cells at same Z
c    - Easier to modify (change one line, not 7)
c    - Enables clean axial tallies
c
c 5. Off-axis positioning
c    - Center at (25.337, -25.337) enables multiple stacks
c    - Could add more stacks at different (x,y) positions
c    - Each stack independent, share PZ planes
c
c Pattern Recognition:
c  Cell 1: -1 (inside surf 1)
c  Cell 2:  1 -2 (outside 1, inside 2)
c  Cell 3:  2 -3 (outside 2, inside 3)
c  Cell 4:  3 -4 (outside 3, inside 4)
c  Cell 5:  4 -5 (outside 4, inside 5)
c  Cell 6:  5 -6 (outside 5, inside 6)
c  Cell 7:  6 -7 (outside 6, inside 7)
c  Cell 8:  7 (outside 7)
c
c This pattern generalizes to N layers.
c
c ============================================================
c COMMON ERRORS AND FIXES
c ============================================================
c
c Error 1: Different centers
c  WRONG: 1  c/z  25.337  -25.337  0.635
c         2  c/z  25.340  -25.337  0.641  ← x coordinate differs!
c  FIX:   Use SAME (x,y) for all C/Z surfaces
c
c Error 2: Radii not increasing
c  WRONG: 1  c/z  25.337  -25.337  1.519
c         2  c/z  25.337  -25.337  0.641  ← R2 < R1 ERROR
c  FIX:   Order surfaces by increasing radius
c
c Error 3: Missing axial bounds
c  WRONG: 1  1  -10.9  -1    ← Infinite cylinder!
c  FIX:   Add axial planes: 1  1  -10.9  -1  -10 11
c
c Error 4: Lost particles in thin gaps
c  SYMPTOM: "Lost particle" warnings in 0.63 mm gas gap
c  FIX 1:  Increase gap (if physically reasonable)
c  FIX 2:  Homogenize thin gap into adjacent region
c  FIX 3:  Reduce particle importance in gap (IMP:N=0.1)
c
c ============================================================
