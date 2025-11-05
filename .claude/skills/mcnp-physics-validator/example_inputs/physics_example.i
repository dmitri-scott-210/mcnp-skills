Physics Validation Example
c =================================================================
c Demonstrates correct physics setup
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    1  -2.7     -1              IMP:N=1 IMP:P=1  $ Water
2    0           1               IMP:N=0 IMP:P=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0

c =================================================================
c Data Cards
c =================================================================
MODE  N P                                      $ Coupled N-P (MODE first!)
M1   1001.80c  2   8016.80c  1                $ Water with 80c library
MT1  H-H2O.40t                                 $ Thermal scattering
TMP  2.53e-8                                   $ Room temperature (293K)
PHYS:N 20                                      $ Neutron physics, 20 MeV
PHYS:P 20                                      $ Photon physics, 20 MeV
CUT:N 1e-8                                     $ 0.01 eV cutoff (thermal OK)
SDEF  POS=0 0 0  ERG=1.0
F4:N 1
NPS   1000
PRINT
