Temperature-Dependent Physics - TMP and DBRC Example
c =================================================================
c Demonstrates:
c   - TMP card for temperature-dependent cross sections
c   - DBRC card for Doppler broadening rejection correction
c   - High-temperature reactor fuel
c =================================================================
c Cell Cards
c =================================================================
1    1  -10.2   -1   IMP:N=1  VOL=50.27   $ UO2 fuel pellet
2    2  -6.5    1 -2 IMP:N=1  VOL=23.55   $ Zircaloy cladding
3    3  -1.0    2 -3 IMP:N=1  VOL=100.53  $ Water coolant
4    0           3   IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    CZ  0.4                                $ Fuel outer radius
2    CZ  0.46                               $ Cladding outer radius
3    CZ  0.6                                $ Coolant outer radius

c =================================================================
c Data Cards
c =================================================================
MODE N
c --- Physics Settings ---
PHYS:N 20 0                                 $ emax=20 MeV, implicit capture
c --- Temperature Settings ---
TMP  2.533e-8  2.92e-8  2.533e-8           $ Fuel=900K, Clad=900K, Water=293K
c --- DBRC for Resonance Isotopes ---
DBRC endf=80 emax=2.1e-7                   $ U-238 DBRC up to 210 eV
c --- Material Definitions ---
M1   92235.80c  0.005  92238.80c  0.217    $ UO2 fuel (3% enriched)
     8016.80c   0.445
M2   40000.80c  1                           $ Natural zirconium (Zircaloy)
M3   1001.80c   2  8016.80c  1             $ Light water
MT3  H-H2O.40t                               $ Thermal scattering for water
c --- Source Definition ---
SDEF POS=0 0 0 ERG=D1 PAR=N                $ Watt fission spectrum
SI1  H  0 20                                $ Histogram from 0-20 MeV
SP1  D  0 exp(-E) sinh(sqrt(2*E))          $ Watt spectrum approximation
c --- Tally Definitions ---
F4:N 1                                      $ Fuel flux
F14:N 2                                     $ Cladding flux
F24:N 3                                     $ Coolant flux
E0   1e-11 1e-9 1e-7 1e-5 0.001 0.1 1 10   $ Energy bins (MeV)
c --- Problem Termination ---
NPS  1e5
PRDMP 2J 1
