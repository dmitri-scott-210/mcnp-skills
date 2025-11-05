Reaction Rates - F4 with FM Multiplier
c
c Example demonstrating:
c   - F4 flux tally
c   - FM multiplier card for reaction rates
c   - Multiple reaction types (fission, capture, n,2n)
c   - U-235 fuel cell
c
c =================================================================
c Cell Cards
c =================================================================
1    1  -19.1  -1        IMP:N=1  VOL=33.51       $ U-235 metal sphere
2    0          1  -2    IMP:N=1                   $ Void region
3    0          2        IMP:N=0                   $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   2.0            $ Fuel radius
2    SO   50.0           $ Problem boundary

c =================================================================
c Data Cards
c =================================================================
MODE N
c Source - 2 MeV point source at origin
SDEF  POS=0 0 0  ERG=2.0
c Material - U-235 metal
M1   92235  1.0                                    $ Pure U-235
c Flux tally with reaction rate multipliers
F4:N  1                                            $ Flux in fuel cell
FM4   (-1 1 -6)                                    $ Bin 1: Fission rate
      (-1 1 -2)                                    $ Bin 2: Capture rate
      (-1 1 16)                                    $ Bin 3: (n,2n) rate
      (-1 1 102)                                   $ Bin 4: (n,gamma) rate
c      ^c ^m ^R  where c=atom density, m=material, R=reaction MT number
SD4   33.51                                        $ Volume for normalization
c Energy bins
E4    0.01 0.1 1 2 3 5 10                         $ Energy bins (MeV)
c Termination
NPS   5000000
