Discrete Gamma-Ray Source - Co-60 Calibration
c =================================================================
c Example demonstrating:
c   - Discrete energy lines (SI L option)
c   - Multiple gamma energies (1.173 MeV, 1.332 MeV)
c   - Photon transport (MODE P)
c   - Pulse-height tally (F8)
c =================================================================
c Cell Cards
c =================================================================
1    0          -1       IMP:P=1            $ Air-filled source region
2    1  -1.18   -2  1    IMP:P=1  VOL=1e6   $ Acrylic detector (1 m³)
3    0           2       IMP:P=0            $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  5                                  $ Source boundary (5 cm)
2    RPP  -50 50  -50 50  -50 50           $ Detector box (1m × 1m × 1m)

c =================================================================
c Data Cards
c =================================================================
MODE P
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=D1  PAR=P
SI1 L 1.173  1.332                          $ Discrete energies (MeV) - Co-60
SP1   1.0    1.0                            $ Relative intensities (equal)
c --- Material Definition ---
M1   1001.80c  0.533   $ H (acrylic C5H8O2)
     6000.80c  0.333   $ C
     8016.80c  0.133   $ O
c --- Tally Definitions ---
F4:P 2                                      $ Photon flux in detector
E4   0.1  0.5  1.0  1.173  1.332  2.0      $ Energy bins (MeV)
F8:P 2                                      $ Pulse-height tally (energy deposition)
E8   0 0.01 0.1 0.5 1.0 1.173 1.332 2.0    $ Energy deposition bins (MeV)
c --- Problem Termination ---
NPS  1e5
