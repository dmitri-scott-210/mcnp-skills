Lattice Expansion - 3x3 Expanded to 5x5
c
c Original geometry from mcnp-geometry-builder with 3x3 pin lattice
c EDITED: Expanded FILL indices from -1:1 to -2:2 (3x3 to 5x5)
c         Updated bounding surface from 3.78 to 6.30 cm half-width
c         Expanded FILL array from 9 to 25 elements
c
c Cell Cards
c ==========
c --- Universe 0 (main) ---
100  0  -100  LAT=1  FILL=-2:2 -2:2 0:0  &
            1 1 1 1 1  &
            1 1 2 1 1  &
            1 2 2 2 1  &
            1 1 2 1 1  &
            1 1 1 1 1  IMP:N=1
c         ^5x5 lattice - was 3x3 with FILL=-1:1 -1:1 0:0
200  0   100 -200  IMP:N=1        $ Surrounding water
999  0   200       IMP:N=0        $ Graveyard
c --- Universe 1 (standard pin) ---
1    1  -10.2  -10       U=1  IMP:N=1  $ Fuel
2    2  -6.5    10 -11   U=1  IMP:N=1  $ Clad
3    3  -1.0    11       U=1  IMP:N=1  $ Moderator
c --- Universe 2 (guide tube) ---
4    0         -10       U=2  IMP:N=1  $ Void
5    2  -6.5    10 -11   U=2  IMP:N=1  $ Clad
6    3  -1.0    11       U=2  IMP:N=1  $ Moderator

c Surface Cards
c ==============
c Lattice boundary (expanded from ±1.89 to ±3.15)
100  RPP  -6.30 6.30  -6.30 6.30  -10 10  $ 5x1.26=6.30 (was 3x1.26=3.78)
200  RPP  -15 15  -15 15  -15 15           $ Outer boundary
c Pin surfaces (pitch 1.26 cm)
10   CZ   0.5                               $ Fuel radius
11   CZ   0.7                               $ Clad outer

c Data Cards
c ===========
MODE N
c Source
KCODE  10000  1.0  50  150
KSRC   0 0 0  1.26 0 0  -1.26 0 0  0 1.26 0  0 -1.26 0
c Materials
M1   92235 -0.04  92238 -0.96  8016 -0.12   $ UO2 fuel
M2   40000  1.0                              $ Zircaloy
M3   1001  2   8016  1                       $ H2O
MT3  LWTR.01T
