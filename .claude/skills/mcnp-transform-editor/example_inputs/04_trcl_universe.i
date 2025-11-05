TRCL Universe Placement Example - Four Detectors
c =================================================================
c Demonstrates TRCL usage for placing universes
c Same detector universe placed at four positions
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
c --- Main geometry (universe 0) ---
10   0  -10  FILL=1  TRCL=1  IMP:N=1  $ Detector at (+10, +10, 0)
11   0  -11  FILL=1  TRCL=2  IMP:N=1  $ Detector at (-10, +10, 0)
12   0  -12  FILL=1  TRCL=3  IMP:N=1  $ Detector at (+10, -10, 0)
13   0  -13  FILL=1  TRCL=4  IMP:N=1  $ Detector at (-10, -10, 0)
20   2  -1.0  -20 (10:11:12:13)  IMP:N=1  $ Water surrounding detectors
30   0   20  IMP:N=0  $ Graveyard
c --- Detector universe (universe 1) ---
1    1  -2.7  -1  U=1  IMP:N=1  $ Detector material
2    0         1  U=1  IMP:N=0  $ Outside detector (within universe)

c =================================================================
c Surface Cards
c =================================================================
c --- Detector surfaces (universe 1, defined at origin) ---
1    SO   3.0                   $ Detector sphere, R=3 cm
c --- Bounding cells for each detector placement ---
10   SO   3.0                   $ Bound for cell 10
11   SO   3.0                   $ Bound for cell 11
12   SO   3.0                   $ Bound for cell 12
13   SO   3.0                   $ Bound for cell 13
20   SO   30.0                  $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definitions ---
*TR1  10  10  0                $ First detector: NE quadrant
*TR2  -10  10  0               $ Second detector: NW quadrant
*TR3  10  -10  0               $ Third detector: SE quadrant
*TR4  -10  -10  0              $ Fourth detector: SW quadrant
c Note: Translation-only transformations (no rotation needed)
c --- Particle Mode ---
MODE  N
c --- Material Definitions ---
M1    13027.80c  1              $ Aluminum (detector)
M2    1001.80c  2  8016.80c  1  $ Water (moderator)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0        $ Point source at center
c --- Tally Definition ---
F4:N  (1<10<20) (1<11<20) (1<12<20) (1<13<20)  $ Flux in all 4 detectors
E4    0.1 0.5 1.0 5.0           $ Energy bins
c --- Problem Termination ---
NPS   200000
PRINT
