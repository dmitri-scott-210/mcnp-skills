Nested Spheres Template - Concentric spherical shells
c =================================================================
c Template for multi-layer spherical geometry
c Replace parameters marked with <...> with actual values
c =================================================================
c
c Cell Cards
1    <mat1>  <dens1>  -1           IMP:N=1  VOL=<vol1>  $ Core
2    <mat2>  <dens2>   1  -2       IMP:N=1  VOL=<vol2>  $ Shell 1
3    <mat3>  <dens3>   2  -3       IMP:N=1  VOL=<vol3>  $ Shell 2
4    <mat4>  <dens4>   3  -4       IMP:N=1  VOL=<vol4>  $ Shell 3
5    0                 4  -5       IMP:N=1  VOL=<vol5>  $ Void region
6    0                 5           IMP:N=0               $ Graveyard

c Surface Cards
1    SO   <r1>                     $ Core radius (cm)
2    SO   <r2>                     $ Shell 1 outer radius
3    SO   <r3>                     $ Shell 2 outer radius
4    SO   <r4>                     $ Shell 3 outer radius
5    SO   <r_boundary>             $ Problem boundary

c Data Cards
MODE  N
c --- Source ---
SDEF  POS=0 0 0  ERG=<energy>     $ Point source at origin (MeV)
c --- Materials ---
M<mat1>  <ZAID> <frac> <ZAID> <frac>    $ Core material
M<mat2>  <ZAID> <frac> <ZAID> <frac>    $ Shell 1 material
M<mat3>  <ZAID> <frac> <ZAID> <frac>    $ Shell 2 material
M<mat4>  <ZAID> <frac> <ZAID> <frac>    $ Shell 3 material
c Optional: MT<mat#>  <S(a,b)_table>
c --- Tallies (optional) ---
c F4:N  1 2 3 4 5                         $ Flux in each region
c E4    <E1> <E2> <E3>                    $ Energy bins
c --- Termination ---
NPS   <histories>
PRINT
c =================================================================
c Instructions:
c 1. Replace <mat#> with material numbers (1, 2, 3, 4)
c 2. Replace <dens#> with densities (negative for g/cm³)
c 3. Replace <r1> through <r_boundary> with radii (increasing order)
c 4. Calculate volumes: V = (4/3)π(r_outer³ - r_inner³)
c 5. Replace <ZAID> with isotope IDs (e.g., 92235, 82000)
c 6. Replace <frac> with atomic fractions
c 7. Replace <energy> with source energy in MeV
c 8. Replace <histories> with NPS count (e.g., 100000)
c =================================================================
