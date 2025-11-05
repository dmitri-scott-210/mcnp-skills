INVALID - Lattice Fill Array Dimension Mismatch - Cell Checker Example
c =================================================================
c ERROR: Lattice declares 5x5x1=25 values but only 20 provided
c This will cause FATAL ERROR in MCNP
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    0         -1      fill=10  IMP:N=1            $ Real world
100  0         -100    lat=1  u=10  IMP:N=1        $ Lattice cell
                       fill=-2:2 -2:2 0:0
                       1 1 1 1 1
                       1 2 2 2 1
                       1 2 3 2 1
                       1 2 2 2 1
c ERROR: Missing 5th row! Need 25 values total
200  1  -1.0  -200    u=1  IMP:N=1                 $ Standard fuel
300  2  -2.0  -300    u=2  IMP:N=1                 $ Control rod
400  3  -3.0  -400    u=3  IMP:N=1                 $ Burnable absorber
999  0         1           IMP:N=0                 $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   50.0                                     $ Outer boundary
100  RPP  -25 25 -25 25 0 10                       $ Lattice box
200  CZ   2.0                                      $ Fuel radius
300  CZ   2.0                                      $ Control rod radius
400  CZ   2.0                                      $ Absorber radius

c =================================================================
c Data Cards
c =================================================================
MODE  N
M1   92235  1.0                                    $ U-235
M2   5010  1.0                                     $ B-10 absorber
M3   64155  1.0                                    $ Gd-155 absorber
SDEF POS=0 0 5  ERG=1.0
F4:N 100
NPS  1000
PRINT
