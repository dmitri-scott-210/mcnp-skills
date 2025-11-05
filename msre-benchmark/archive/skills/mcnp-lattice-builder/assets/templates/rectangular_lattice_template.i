Rectangular Lattice Template - LAT=1 Basic Structure
c =================================================================
c Template for LAT=1 (hexahedral/rectangular) lattice
c User must fill in: radii, dimensions, materials, source
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Universe 1: Pin Cell (repeated element) ---
1    <mat#>  <density>  -1     U=1  IMP:N=1  VOL=<calc>  $ Core/fuel
2    <mat#>  <density>   1 -2  U=1  IMP:N=1  VOL=<calc>  $ Shell/clad
3    <mat#>  <density>   2     U=1  IMP:N=1  VOL=<calc>  $ Background

c --- Universe 10: Lattice Cell (NxNxN array) ---
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
c    For array FILL, replace FILL=1 with:
c    FILL=imin:imax jmin:jmax kmin:kmax
c         <list universe numbers in Fortran order: i fastest>

c --- Real World: Container ---
1000 0  -1000  FILL=10  IMP:N=1
1001 0  1000  IMP:N=0

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- Pin Surfaces (Universe 1) ---
1    CZ   <r1>
2    CZ   <r2>

c --- Lattice Element Boundaries (Universe 10) ---
c    CRITICAL: Surface order defines index directions!
c    Order below: i in X, j in Y, k in Z
10   PX   <xmin>                        $ -X (i=imin boundary)
11   PX   <xmax>                        $ +X (i=imax boundary)
12   PY   <ymin>                        $ -Y (j=jmin boundary)
13   PY   <ymax>                        $ +Y (j=jmax boundary)
14   PZ   <zmin>                        $ -Z (k=kmin boundary)
15   PZ   <zmax>                        $ +Z (k=kmax boundary)

c --- Container ---
1000 RPP  <xmin-margin>  <xmax+margin>  <ymin-margin>  <ymax+margin>  <zmin-margin>  <zmax+margin>

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials (User must define) ---
M<#>  ...
c --- Source ---
c SDEF  ...  or  KCODE ...
c --- Tallies ---
c F4:N  ...
c --- Termination ---
NPS   <#>
PRINT

