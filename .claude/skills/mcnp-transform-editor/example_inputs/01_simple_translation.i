Simple Translation Example - Two Detectors
c =================================================================
c Demonstrates translation-only TR card
c Move detector from origin to x=15 cm
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7  -1      IMP:N=1  $ Detector 1 at origin
2    1  -2.7  -2      IMP:N=1  $ Detector 2 translated to x=15 cm
3    2  -1.0  -3 1 2  IMP:N=1  $ Water surrounding detectors
4    0          3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   5.0                   $ Detector 1: sphere at origin, R=5 cm
2    1 SO  5.0                  $ Detector 2: sphere with TR1
3    SO   50.0                  $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
*TR1  15 0 0                    $ Translation: move +15 cm in x-direction
c --- Particle Mode ---
MODE  N
c --- Material Definitions ---
M1    13027.80c  1              $ Aluminum (detector material)
M2    1001.80c  2  8016.80c  1  $ Water (H2O)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0        $ Point source at origin, 1 MeV neutrons
c --- Tally Definition ---
F4:N  1 2                       $ Average flux in both detectors
E4    0.1 0.5 1.0 5.0           $ Energy bins (MeV)
c --- Problem Termination ---
NPS   100000
PRINT
