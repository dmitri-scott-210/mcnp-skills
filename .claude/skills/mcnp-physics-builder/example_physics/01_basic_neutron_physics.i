Basic Neutron Physics - PHYS:N and CUT:N Example
c =================================================================
c Demonstrates:
c   - PHYS:N card with emax and implicit capture
c   - CUT:N card for transport cutoff
c   - Typical reactor neutron physics settings
c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7    -1   IMP:N=1  VOL=33.51  $ Aluminum sphere
2    0           1   IMP:N=0             $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  2                                $ 2 cm radius sphere

c =================================================================
c Data Cards
c =================================================================
MODE N
c --- Physics Settings ---
PHYS:N 20 0                              $ emax=20 MeV, implicit capture everywhere
CUT:N  J 5J 0.001                        $ Transport cutoff 0.001 MeV (1 keV)
c --- Material Definition ---
M1   13027.80c  1                        $ Aluminum-27
c --- Source Definition ---
SDEF POS=0 0 0 ERG=14.1 PAR=N           $ 14.1 MeV point source
c --- Tally Definitions ---
F4:N 1                                   $ Volume-averaged flux
E4   0.001 0.01 0.1 1 5 10 14 15        $ Energy bins (MeV)
c --- Problem Termination ---
NPS  1e5
PRDMP 2J 1
