Point Isotropic Neutron Source - D-T Fusion (14.1 MeV)
c =================================================================
c Example demonstrating:
c   - Simplest possible source: point isotropic
c   - Single energy (14.1 MeV D-T fusion)
c   - Basic flux and heating tallies
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0    -1   IMP:N=1  VOL=113097.3  $ Water sphere (30 cm radius)
2    0           1   IMP:N=0                $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  30                                 $ Outer boundary sphere

c =================================================================
c Data Cards
c =================================================================
MODE N
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=14.1  PAR=N           $ Point at origin, 14.1 MeV neutrons
c --- Material Definition ---
M1   1001.80c  2  8016.80c  1              $ Light water (H2O)
MT1  H-H2O.40t                              $ S(alpha,beta) thermal scattering
c --- Tally Definitions ---
F4:N 1                                      $ Flux in water sphere
E4   0.01  0.1  1  5  10  14  15           $ Energy bins (MeV)
F6:N 1                                      $ Heating in water sphere (MeV/g)
c --- Problem Termination ---
NPS  1e5
PRDMP 2J 1
