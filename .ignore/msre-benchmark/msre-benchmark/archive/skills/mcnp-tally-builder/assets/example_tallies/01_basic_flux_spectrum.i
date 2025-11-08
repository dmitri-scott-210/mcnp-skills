Basic Flux Spectrum - F4 Tally with Energy Bins
c
c Example demonstrating:
c   - F4 track-length flux tally
c   - E4 energy bins for spectrum
c   - SD4 volume specification for normalization
c   - Simple water sphere geometry
c
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0   -1        IMP:N=1  VOL=4188.79    $ Water sphere
2    0          1        IMP:N=0                  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0           $ Sphere R=10 cm

c =================================================================
c Data Cards
c =================================================================
MODE N
c Source - 14.1 MeV point source at origin
SDEF  POS=0 0 0  ERG=14.1
c Material - Light water
M1   1001  2  8016  1                             $ H2O
MT1  LWTR.01T                                      $ S(a,b) thermal scattering
c Tally - Cell flux with energy bins
F4:N  1                                            $ Flux in cell 1
E4    1E-10 1E-8 1E-6 1E-4 0.01 0.1 1 10 14 15   $ Energy bins (MeV)
SD4   4188.79                                      $ Volume (cm^3) for normalization
c Termination
NPS   1000000
