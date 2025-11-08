Pulse-Height Detector - F8 with Zero/Epsilon Bins
c
c Example demonstrating:
c   - F8 pulse-height tally (energy deposition)
c   - Zero and epsilon bins (CRITICAL for F8)
c   - Energy bins representing detector response
c   - NaI scintillator detector
c
c =================================================================
c Cell Cards
c =================================================================
1    0         -1  2     IMP:P=1                   $ Void (source region)
10   1  -3.67  -2        IMP:P=1  VOL=78.54       $ NaI detector
20   0          1  -3    IMP:P=1                   $ Void (outside)
99   0          3        IMP:P=0                   $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   5.0            $ Source boundary
2    RCC  10 0 0  5 0 0  2.5                      $ Detector cylinder (x-axis)
3    SO   50.0           $ Problem boundary

c =================================================================
c Data Cards
c =================================================================
MODE P
c Source - 662 keV gamma (Cs-137)
SDEF  POS=0 0 0  ERG=0.662  PAR=2
c Material - NaI detector
M1   11023  1  53127  1                            $ NaI (sodium iodide)
c Pulse-height tally
F8:P  10                                           $ Energy deposition in detector
E8    0  1E-5  0.1 0.2 0.3 0.4 0.5 0.6 0.65 0.67 0.7 0.8 1.0  $ Energy bins (MeV)
c     ^ZERO ^EPSILON        ^Source energy region
c     Zero bin: No energy deposition (particles that don't interact)
c     Epsilon bin: Very small depositions (computational artifacts)
c     Physical bins: Actual pulse-height distribution
c Termination
NPS   1000000
