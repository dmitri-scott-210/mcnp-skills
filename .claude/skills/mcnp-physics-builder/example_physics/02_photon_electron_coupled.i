Coupled Photon-Electron Physics - PHYS:P and PHYS:E Example
c =================================================================
c Demonstrates:
c   - PHYS:P card with detailed photon physics
c   - PHYS:E card for electron transport
c   - Coupled photon-electron problem
c =================================================================
c Cell Cards
c =================================================================
1    1  -11.35  -1   IMP:P,E=1  VOL=33.51  $ Lead sphere
2    0           1   IMP:P,E=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  2                                  $ 2 cm radius sphere

c =================================================================
c Data Cards
c =================================================================
MODE P E
c --- Physics Settings ---
PHYS:P 10 0 J 1 0                         $ emax=10 MeV, detailed physics, coherent off
PHYS:E 10 0 J 1 J 1                       $ emax=10 MeV, detailed physics, straggling on
c --- Material Definition ---
M1   82000.80c  1                          $ Natural lead
c --- Source Definition ---
SDEF POS=0 0 0 ERG=2.0 PAR=P              $ 2 MeV photon source
c --- Tally Definitions ---
F4:P 1                                     $ Photon flux
F14:E 1                                    $ Electron flux
E4   0.01 0.1 0.5 1 1.5 2                 $ Photon energy bins (MeV)
E14  0.01 0.1 0.5 1 1.5 2                 $ Electron energy bins (MeV)
F6:P,E 1                                   $ Energy deposition (MeV/g)
c --- Problem Termination ---
NPS  1e5
PRDMP 2J 1
