Proton Physics - PHYS:H Example
c =================================================================
c Demonstrates:
c   - PHYS:H card for proton transport
c   - Higher emax for proton therapy energies
c   - Coupled proton-neutron-photon problem
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0    -1   IMP:H,N,P=1  VOL=268.08  $ Water phantom
2    0           1   IMP:H,N,P=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RPP  -4 4  -4 4  0 8                     $ 8×8×8 cm³ water box

c =================================================================
c Data Cards
c =================================================================
MODE H N P
c --- Physics Settings ---
PHYS:H 250 0 1                                $ emax=250 MeV (therapy range), tables ON
PHYS:N 250 0                                  $ emax=250 MeV for secondary neutrons
PHYS:P 250 0                                  $ emax=250 MeV for secondary photons
c --- Material Definition ---
M1   1001.80c  2  8016.80c  1                 $ Light water (H2O)
MT1  H-H2O.40t                                 $ S(alpha,beta) thermal scattering
c --- Source Definition ---
SDEF POS=0 0 -2 ERG=150 PAR=H DIR=1 VEC=0 0 1  $ 150 MeV proton beam along +z
c --- Tally Definitions ---
F4:H 1                                         $ Proton flux
F14:N 1                                        $ Neutron flux (secondaries)
E4   1 10 50 100 150 160                      $ Proton energy bins (MeV)
E14  0.001 0.1 1 10 50                        $ Neutron energy bins (MeV)
F6:H,N,P 1                                     $ Total energy deposition (MeV/g)
c --- Problem Termination ---
NPS  5e4
PRDMP 2J 1
