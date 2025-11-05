Hexagonal Lattice Template - LAT=2 Basic Structure
c =================================================================
c Template for LAT=2 (hexagonal prism) lattice
c Note: Hexagon has FLAT sides on LEFT/RIGHT (MCNP convention)
c User must fill in: radii, hex dimensions, materials, source
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Universe 1: Pin Cell (repeated element) ---
1    <mat#>  <density>  -1     U=1  IMP:N=1  VOL=<calc>  $ Core
2    <mat#>  <density>   1     U=1  IMP:N=1  VOL=<calc>  $ Background

c --- Universe 10: Hexagonal Lattice ---
100  0  -10 11 -12 13 -14 15 -16 17  U=10  LAT=2  FILL=1  IMP:N=1
c    8 surfaces required: 6 hex sides + 2 top/bottom

c --- Real World: Container ---
1000 0  -1000  FILL=10  IMP:N=1
1001 0  1000  IMP:N=0

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Pin Surfaces (Universe 1) ---
1    CZ   <radius>

c --- Hexagonal Prism Surfaces (Universe 10) ---
c    Regular hexagon with flat-to-flat distance = D
c    6 planes at 60° intervals, distance D/2 from origin
10   P    0.866025  0.5  0  <-D/2>        $ Side 1 (+30°)
11   P    0.0       1.0  0  <-D/2>        $ Side 2 (+90°)
12   P   -0.866025  0.5  0  <-D/2>        $ Side 3 (+150°)
13   P   -0.866025 -0.5  0  <-D/2>        $ Side 4 (-150°)
14   P    0.0      -1.0  0  <-D/2>        $ Side 5 (-90°)
15   P    0.866025 -0.5  0  <-D/2>        $ Side 6 (-30°)
16   PZ   <zmin>                           $ Bottom
17   PZ   <zmax>                           $ Top

c --- Container (Cylindrical recommended for hex lattice) ---
1000 RCC  0 0 <zmin>  0 0 <H>  <R>

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
M<#>  ...
c SDEF  ...
c F4:N  ...
NPS   <#>
PRINT

