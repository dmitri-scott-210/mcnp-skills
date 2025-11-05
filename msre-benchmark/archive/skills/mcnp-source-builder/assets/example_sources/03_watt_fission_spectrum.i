Watt Fission Spectrum Source - U-235 Thermal Fission
c =================================================================
c Example demonstrating:
c   - Watt spectrum (built-in function -3)
c   - Realistic fission neutron energy distribution
c   - U-235 thermal fission parameters (a=0.988, b=2.249)
c   - Energy-dependent flux tallies
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0    -1   IMP:N=1  VOL=33510.3   $ Water moderator sphere
2    2  -2.7    -2  1 IMP:N=1  VOL=20944    $ Aluminum reflector
3    0           2   IMP:N=0                $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO  20                                 $ Water boundary
2    SO  25                                 $ Aluminum outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE N
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=D1  PAR=N
SI1  -3                                     $ Watt spectrum (built-in function -3)
SP1   0.988  2.249                          $ Parameters: a=0.988 MeV, b=2.249 MeV^-1
c --- Material Definitions ---
M1   1001.80c  2  8016.80c  1              $ Light water (H2O)
MT1  H-H2O.40t                              $ S(alpha,beta) thermal scattering
M2   13027.80c  1.0                         $ Aluminum-27
c --- Tally Definitions ---
F4:N 1                                      $ Flux in water region
E4   1e-10  1e-6  0.01  0.1  1  5  10  20  $ Energy bins (MeV)
F2:N 1                                      $ Surface flux at water boundary
E2   0.01  0.1  1  5  10                   $ Energy bins (MeV)
c --- Problem Termination ---
NPS  1e6
