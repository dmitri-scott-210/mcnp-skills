Rectangular Pin Array Template - LAT=1 lattice
c =================================================================
c Template for NxN rectangular array of cylindrical pins
c Replace parameters marked with <...> with actual values
c =================================================================
c
c Pin universe (U=1)
1    <mat1>  <dens1>  -1      U=1  IMP:N=1    $ Pin core
2    <mat2>  <dens2>   1  -2  U=1  IMP:N=1    $ Pin clad
3    <mat3>  <dens3>   2  -3  U=1  IMP:N=1    $ Coolant
c Lattice cell (NxN array)
10   0  -10 11 -12 13 -14 15  LAT=1  U=2  IMP:N=1
        FILL=<imin>:<imax> <jmin>:<jmax> 0:0
             <universe_array>
c Base geometry
20   0  -20  FILL=2  IMP:N=1                  $ Fill with lattice
21   0   20  IMP:N=0                          $ Graveyard

c Pin surfaces (local to U=1)
1    CZ  <r_core>                             $ Pin core radius
2    CZ  <r_clad>                             $ Clad outer radius
3    CZ  <r_cell>                             $ Pin cell boundary
c Lattice surfaces
10   PX  <x_min>                              $ X min
11   PX  <x_max>                              $ X max
12   PY  <y_min>                              $ Y min
13   PY  <y_max>                              $ Y max
14   PZ  <z_min>                              $ Z min
15   PZ  <z_max>                              $ Z max
c Outer boundary
20   RPP  <xmin> <xmax>  <ymin> <ymax>  <zmin> <zmax>

c Data Cards
MODE  N
SDEF  CEL=20  ERG=<energy>
M<mat1>  <ZAID> <frac> <ZAID> <frac>         $ Pin core material
M<mat2>  <ZAID> <frac> <ZAID> <frac>         $ Clad material
M<mat3>  <ZAID> <frac> <ZAID> <frac>         $ Coolant material
c Optional: MT<mat#>  <S(a,b)_table>
NPS   <histories>
PRINT
c =================================================================
c Instructions:
c 1. Pin dimensions: <r_core> < <r_clad> < <r_cell>
c 2. Lattice indices: For NxN array use -N/2:N/2 (e.g., -1:1 for 3x3)
c 3. FILL array: List universes reading i (X) fastest, j (Y) middle
c    Example 3x3: FILL=-1:1 -1:1 0:0
c                      1 1 1  (j=1: i=-1,0,1)
c                      1 1 1  (j=0)
c                      1 1 1  (j=-1)
c 4. Lattice boundaries: Calculate from pitch × count
c    pitch = (x_max - x_min) / (imax - imin + 1)
c 5. Pin cell radius <r_cell> should fit pitch (typically pitch/2)
c =================================================================
