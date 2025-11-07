MSRE First Criticality - VOID Test (Geometry Overlap Detection)
c ===================================================================
c Purpose: Detect overlapping cells before production run
c Method: VOID card test with 1000 particles
c Expected: VOID = 0.00000E+00 (no overlaps)
c If VOID ≠ 0: OVERLAPS EXIST (FATAL - must fix before production)
c
c Reference: MCNP Best Practices Chapter 3.4.1, Item 10
c ===================================================================
c
c ===================================================================
c BLOCK 1: CELL CARDS
c ===================================================================
c
c -------------------------------------------------------------------
c Universe 1: Graphite Stringer (589 positions)
c -------------------------------------------------------------------
c 5.084 × 5.084 cm graphite with 4 machined grooves
c Each groove: 1.018 cm wide × 1.5265 cm deep
c Adjacent grooves form 3.053 cm fuel channels
c
1   1  -2.3275  -10 11 -12 13 54 -55  U=10  IMP:N=1  VOL=265.7    $ North groove
2   1  -2.3275  -16 17 -18 19 54 -55  U=10  IMP:N=1  VOL=265.7    $ East groove
3   1  -2.3275  -20 21 -22 23 54 -55  U=10  IMP:N=1  VOL=265.7    $ South groove
4   1  -2.3275  -24 25 -26 27 54 -55  U=10  IMP:N=1  VOL=265.7    $ West groove
5   2  -1.86    50 -51 52 -53 54 -55  #1 #2 #3 #4  U=10  IMP:N=1  VOL=3337.3  $ Graphite
c
c -------------------------------------------------------------------
c Universe 2: Control Rod - Withdrawn (2 positions at -1,+1 and +1,+1)
c -------------------------------------------------------------------
c Thimble: 5.08 cm OD, 0.1651 cm wall
c Poison withdrawn above core (z > 129.54 cm)
c
11  1  -2.3275  -30  54 -55  U=2  IMP:N=1  VOL=3011.3    $ Inner fuel salt
12  3  -8.7745  30 -31  54 -55  U=2  IMP:N=1  VOL=263.4  $ INOR-8 thimble
13  1  -2.3275  31 50 -51 52 -53  54 -55  U=2  IMP:N=1  VOL=944.4  $ Outer salt
c
c -------------------------------------------------------------------
c Universe 3: Regulating Rod - 3% Inserted (1 position at -1,-1)
c -------------------------------------------------------------------
c Poison at z = 41.287 to 118.364 cm (3% insertion = 5.11 cm)
c
21  1  -2.3275  -40  54 -42  U=3  IMP:N=1  VOL=731.0     $ Fuel below poison
22  4  -5.873   -40  42 -43  U=3  IMP:N=1  VOL=1364.5    $ Poison region
23  1  -2.3275  -40  43 -55  U=3  IMP:N=1  VOL=916.2     $ Fuel above poison
24  3  -8.7745  40 -41  54 -55  U=3  IMP:N=1  VOL=263.4  $ INOR-8 thimble
25  1  -2.3275  41 50 -51 52 -53  54 -55  U=3  IMP:N=1  VOL=944.4  $ Outer salt
c
c -------------------------------------------------------------------
c Universe 4: Sample Basket (1 position at +1,-1) USER CONFIRMED
c -------------------------------------------------------------------
c Basket: 5.4287 cm OD, 0.079 cm wall
c Contents: Homogenized (17.4% graphite + 5.8% INOR + 76.8% fuel)
c
31  5  -2.6206  -60  54 -55  U=4  IMP:N=1  VOL=3717.6    $ Homogenized interior
32  3  -8.7745  60 -61  54 -55  U=4  IMP:N=1  VOL=131.9  $ INOR-8 basket wall
33  1  -2.3275  61 50 -51 52 -53  54 -55  U=4  IMP:N=1  VOL=531.6  $ Outer salt
c
c -------------------------------------------------------------------
c Universe 1: Lattice Array (28×28×1)
c -------------------------------------------------------------------
c Core radius: 70.285 cm, Pitch: 5.084 cm → 28×28 array
c THIS universe contains the LAT=1 lattice with FILL array
c
100  0  -1000  U=1 LAT=1  FILL=-13:14 -13:14 0:0  IMP:N=1  $ Lattice cell
             0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
             0 0 0 0 0 0 0 0 0 0 10 10 10 10 10 10 10 10 10 0 0 0 0 0 0 0 0 0
             0 0 0 0 0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0 0 0 0 0
             0 0 0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0 0 0
             0 0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0 0
             0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0
             0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0
             0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0
             0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0
             0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 2 10 2 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 3 10 4 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
             0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0
             0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0
             0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0
             0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0
             0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0
             0 0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0 0
             0 0 0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0 0 0
             0 0 0 0 0 0 0 0 10 10 10 10 10 10 10 10 10 10 10 10 10 0 0 0 0 0 0 0
             0 0 0 0 0 0 0 0 0 0 10 10 10 10 10 10 10 10 10 0 0 0 0 0 0 0 0 0
c
c Central pattern in lattice:
c   (0,0):   Universe 10 (graphite stringer with grooves)
c   (-1,+1): Universe 2 (control rod withdrawn)
c   (+1,+1): Universe 2 (control rod withdrawn)
c   (-1,-1): Universe 3 (regulating rod 3% inserted)
c   (+1,-1): Universe 4 (sample basket)
c
c -------------------------------------------------------------------
c Real World Geometry (Universe 0)
c -------------------------------------------------------------------
c
c === Core Lattice Region ===
1000  0  -1000  FILL=1  IMP:N=1                            $ Fill with lattice universe
c
c === Core Can (INOR-8) ===
1010  3  -8.7745  1000 -1001    IMP:N=1            $ Core can
c
c === Downcomer Annulus (void at criticality) ===
1020  0  1001 -1002  1010 -1011  IMP:N=1           $ Void annulus
c
c === Reactor Vessel (INOR-8) ===
1100  3  -8.7745  1002 -1003  1010 -1051  IMP:N=1  $ Vessel wall
c
c === Lower Plenum ===
1200  1  -2.3275  -1002  1050 -1010  IMP:N=1       $ Fuel salt below
1201  3  -8.7745  -1003  1050 -1010  IMP:N=1       $ Vessel bottom head
c
c === Upper Plenum ===
1300  1  -2.3275  -1002  1011 -1012  IMP:N=1       $ Fuel salt above
1301  3  -8.7745  -1003  1012 -1051  IMP:N=1       $ Vessel top head
c
c === Outer Boundaries ===
1900  0  1003 -1999  1050 -1051  IMP:N=1           $ Void outside
1999  0  1999  IMP:N=0                             $ Graveyard

c ===================================================================
c BLOCK 2: SURFACE CARDS
c ===================================================================
c
c -------------------------------------------------------------------
c Universe 10: Lattice Element Boundaries (5.084 cm pitch)
c -------------------------------------------------------------------
50  PX  -2.542                          $ -X (i min)
51  PX   2.542                          $ +X (i max)
52  PY  -2.542                          $ -Y (j min)
53  PY   2.542                          $ +Y (j max)
54  PZ   0.0                            $ Bottom (k=0)
55  PZ  170.311                         $ Top (core height)
c
c -------------------------------------------------------------------
c Universe 1: Graphite Stringer Groove Surfaces
c -------------------------------------------------------------------
c North groove (on +Y face)
10  PX  -0.509                          $ North groove -X
11  PX   0.509                          $ North groove +X
12  PY   1.0155                         $ North groove -Y
13  PY   2.542                          $ North groove +Y
c East groove (on +X face)
16  PX   1.0155                         $ East groove -X
17  PX   2.542                          $ East groove +X
18  PY  -0.509                          $ East groove -Y
19  PY   0.509                          $ East groove +Y
c South groove (on -Y face)
20  PX  -0.509                          $ South groove -X
21  PX   0.509                          $ South groove +X
22  PY  -2.542                          $ South groove -Y
23  PY  -1.0155                         $ South groove +Y
c West groove (on -X face)
24  PX  -2.542                          $ West groove -X
25  PX  -1.0155                         $ West groove +X
26  PY  -0.509                          $ West groove -Y
27  PY   0.509                          $ West groove +Y
c
c -------------------------------------------------------------------
c Universe 2 & 3: Control Rod Thimbles
c -------------------------------------------------------------------
30  RCC  0 0 0  0 0 170.311  2.3749    $ Control rod inner
31  RCC  0 0 0  0 0 170.311  2.54      $ Control rod outer
40  RCC  0 0 0  0 0 170.311  2.3749    $ Regulating rod inner
41  RCC  0 0 0  0 0 170.311  2.54      $ Regulating rod outer
42  PZ  41.287                          $ Poison bottom
43  PZ  118.364                         $ Poison top (3% insertion)
c
c -------------------------------------------------------------------
c Universe 4: Sample Basket
c -------------------------------------------------------------------
60  RCC  0 0 0  0 0 170.311  2.63535   $ Basket inner
61  RCC  0 0 0  0 0 170.311  2.71435   $ Basket outer
c
c -------------------------------------------------------------------
c Universe 0: Base Geometry Surfaces
c -------------------------------------------------------------------
1000  RCC  0 0 0  0 0 170.311  70.285  $ Lattice boundary
1001  RCC  0 0 0  0 0 170.311  71.737  $ Core can outer
1002  RCC  0 0 -51  0 0 271  74.299    $ Vessel inner
1003  RCC  0 0 -51  0 0 271  76.862    $ Vessel outer
1010  PZ  0.0                           $ Lattice bottom
1011  PZ  170.311                       $ Lattice top
1012  PZ  220.0                         $ Upper plenum top
1050  PZ  -51.0                         $ Lower plenum bottom
1051  PZ  220.0                         $ Vessel top
1999  RCC  0 0 -100  0 0 400  150      $ Graveyard

c ===================================================================
c BLOCK 3: DATA CARDS
c ===================================================================
MODE  N
c
c -------------------------------------------------------------------
c VOID Test Configuration (Fast Overlap Detection)
c -------------------------------------------------------------------
c CRITICAL: Reduced cycles for quick geometry test
c Production file uses: KCODE 10000 1.0 50 200
c KSRC in North fuel groove: X=0, Y=1.78 (middle of groove), Z=85
c
KCODE  1000  1.0  10  10               $ Quick test: 10 cycles total
KSRC   -1.78 0 85                          $ Core center
        1.78 0 85
        0 -1.78 85
        0 -1.78 85
c
c -------------------------------------------------------------------
c VOID CARD - Overlap Detector
c -------------------------------------------------------------------
c Expected: VOID = 0.00000E+00 (NO overlaps)
c If VOID ≠ 0: Overlaps exist - MUST FIX before production
c Reference: MCNP Best Practices Chapter 3.4.1, Item 10
c
VOID
c
c -------------------------------------------------------------------
c Materials
c -------------------------------------------------------------------
c
c M1: Fuel Salt (LiF-BeF2-ZrF4-UF4) at 911 K
c Density: 2.3275 g/cm³
c CRITICAL: Li-6 depleted to 0.005% (NOT 7.5% natural)
M1   3006.80c  1.367E-08               $ Li-6  (0.005%)
     3007.80c  2.733E-05               $ Li-7  (99.995%)
     4009.80c  5.219E-05               $ Be-9
     9019.80c  1.734E-04               $ F-19
     40000.80c 8.556E-06               $ Zr (natural)
     92234.80c 4.436E-09               $ U-234
     92235.80c 6.397E-08               $ U-235 (1.409 wt%)
     92236.80c 2.923E-09               $ U-236
     92238.80c 4.465E-07               $ U-238
c
c M2: Graphite at 911 K
c Density: 1.86 g/cm³
c CRITICAL: 0.8 ppm boron impurity (MUST include)
M2   6000.80c  0.09321                 $ Natural carbon
     5010.80c  6.457E-9                $ B-10 (19.9% of boron)
     5011.80c  2.598E-8                $ B-11 (80.1% of boron)
MT2  grph.87t                          $ S(α,β) at 923 K
c
c M3: INOR-8 (Hastelloy-N) at 911 K
c Density: 8.7745 g/cm³
M3   28000.80c -0.69951                $ Ni (70%)
     42000.80c -0.16988                $ Mo (17%)
     24000.80c -0.06995                $ Cr (7%)
     26000.80c -0.04997                $ Fe (5%)
     6000.80c  -0.00070                $ C  (0.07%)
     25055.80c -0.00500                $ Mn (0.5%)
     14000.80c -0.00499                $ Si (0.5%)
c
c M4: Control Rod Poison (70% Gd2O3, 30% Al2O3)
c Density: 5.873 g/cm³
M4   64000.80c  0.158498               $ Gd (natural)
     13027.80c  0.241502               $ Al-27
     8016.80c   0.600000               $ O-16
c
c M5: Homogenized Sample Basket
c Density: 2.6206 g/cm³ (calculated from components)
c Composition: 17.4% graphite + 5.8% INOR-8 + 76.8% fuel salt
M5   3006.80c  1.367E-08               $ Li-6  (from fuel)
     3007.80c  2.733E-05               $ Li-7
     4009.80c  5.219E-05               $ Be-9
     9019.80c  1.734E-04               $ F-19
     40000.80c 8.556E-06               $ Zr
     92234.80c 4.436E-09               $ U-234
     92235.80c 6.397E-08               $ U-235
     92236.80c 2.923E-09               $ U-236
     92238.80c 4.465E-07               $ U-238
     6000.80c  0.01621                 $ C (from graphite samples)
     28000.80c 5.114E-04               $ Ni (from INOR-8 samples)
c
c Temperature Cards (911 K = 7.8501E-08 MeV)
TMP1  7.8501E-08  7.8501E-08  7.8501E-08  7.8501E-08  7.8501E-08  $ M1-M5
c
PRINT
