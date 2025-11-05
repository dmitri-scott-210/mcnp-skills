Segmented Tally - F4 with FS Card
c
c Example demonstrating:
c   - F4 flux tally
c   - FS card for spatial segmentation
c   - SD card for segment volumes
c   - Subdividing cell without extra geometry
c
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0   -1        IMP:N=1  VOL=4188.79    $ Water sphere
2    0          1        IMP:N=0                  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   10.0           $ Outer sphere
c Additional surfaces for segmentation (not in cell definitions)
10   PZ   -5.0           $ Bottom plane
11   PZ    0.0           $ Midplane
12   PZ    5.0           $ Top plane

c =================================================================
c Data Cards
c =================================================================
MODE N
c Source - Point source at bottom
SDEF  POS=0 0 -8  ERG=14.1
c Material
M1   1001  2  8016  1                             $ H2O
MT1  LWTR.01T
c Segmented flux tally
F4:N  1                                            $ Flux in cell 1
FS4   -10 11 12  T                                 $ Segment by surfaces 10,11,12 + Total
c FS creates 4 bins:
c   Bin 1: Everything on negative side of surface 10 (z < -5)
c   Bin 2: Positive side of surf 11, excluding bin 1 (-5 < z < 0)
c   Bin 3: Positive side of surf 12, excluding bins 1&2 (0 < z < 5)
c   Bin 4: Everything else (z > 5)
c   Bin 5: Total (T option)
SD4   698.13  1396.26  1396.26  698.13  4188.79  $ Volumes for each segment
c     ^bin1   ^bin2    ^bin3    ^bin4   ^total
E4    0.01 1 5 10 14 15                           $ Energy bins
c Termination
NPS   2000000
