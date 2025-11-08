Activation and Delayed Particles - ACT Card Example
c =================================================================
c Demonstrates:
c   - ACT card for delayed particle production
c   - Delayed neutrons in criticality (KCODE)
c   - Fission=both (delayed neutrons and photons)
c =================================================================
c Cell Cards
c =================================================================
1    1  -18.7   -1   IMP:N,P=1  VOL=56.52   $ Bare U-235 sphere
2    0           1   IMP:N,P=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  2.4                                  $ Critical radius ~2.4 cm

c =================================================================
c Data Cards
c =================================================================
MODE N P
c --- Physics Settings ---
PHYS:N 20 0                                  $ emax=20 MeV for neutrons
PHYS:P 20 0                                  $ emax=20 MeV for photons
c --- Activation Settings ---
ACT fission=both                             $ Both delayed neutrons and photons
c --- Material Definition ---
M1   92235.80c  1                            $ Pure U-235
c --- Criticality Source ---
KCODE 1000  1.0  25  125                     $ 1000/cycle, keff=1.0, skip=25, total=125
KSRC  0 0 0                                  $ Initial source at center
c --- Tally Definitions ---
F4:N 1                                        $ Neutron flux
F14:P 1                                       $ Photon flux
E4   1e-9 1e-7 1e-5 0.001 0.1 1 10           $ Neutron energy bins (MeV)
E14  0.01 0.1 0.5 1 2 5 10                   $ Photon energy bins (MeV)
c --- Problem Termination ---
c (NPS not used with KCODE)
PRDMP 2J 1
