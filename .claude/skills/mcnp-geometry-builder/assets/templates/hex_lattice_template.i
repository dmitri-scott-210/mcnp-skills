Hexagonal Lattice Template - LAT=2 with RHP macrobody
c =================================================================
c Template for hexagonal fuel assembly using LAT=2 lattice
c Replace parameters marked with <...> with actual values
c =================================================================
c
c Pin universe (U=1) - Single fuel pin
1    <mat1>  <dens1>  -1     U=1  IMP:N=1    $ Pin fuel
2    <mat2>  <dens2>   1 -2  U=1  IMP:N=1    $ Pin clad
3    <mat3>  <dens3>   2     U=1  IMP:N=1    $ Coolant (fills to hex boundary)
c Lattice cell (Hexagonal array with LAT=2)
10   0  -10  LAT=2  U=2  IMP:N=1
        FILL=<ring_min>:<ring_max>
             <universe_array>
c Base geometry
20   0  -20  FILL=2  IMP:N=1                  $ Fill with lattice
21   0   20  IMP:N=0                          $ Graveyard

c Pin surfaces (local to U=1)
1    CZ  <r_fuel>                             $ Pin fuel radius
2    CZ  <r_clad>                             $ Clad outer radius
c Lattice boundary (hexagonal prism using RHP with 9 values)
10   RHP  0 0 <z_min>  0 0 <height>  <apothem_x> <apothem_y> <apothem_z>
c Outer boundary
20   RHP  0 0 <z_outer_min>  0 0 <height_outer>  <apothem_outer_x> <apothem_outer_y> <apothem_outer_z>

c Data Cards
MODE  N
SDEF  CEL=20  ERG=<energy>
M<mat1>  <ZAID> <frac> <ZAID> <frac>         $ Pin fuel material
M<mat2>  <ZAID> <frac> <ZAID> <frac>         $ Clad material
M<mat3>  <ZAID> <frac> <ZAID> <frac>         $ Coolant material
c Optional: MT<mat#>  <S(a,b)_table>
NPS   <histories>
PRINT
c =================================================================
c CRITICAL INSTRUCTIONS:
c
c 1. RHP SPECIFICATION (9 VALUES - APOTHEM VECTOR):
c    RHP  vx vy vz  h1 h2 h3  r1 r2 r3
c    - vx vy vz: Base center coordinates
c    - h1 h2 h3: Height vector (e.g., 0 0 100 for 100 cm along z)
c    - r1 r2 r3: APOTHEM VECTOR (NOT scalar!)
c
c 2. APOTHEM VECTOR EXAMPLES:
c    For hexagon with flat-to-flat distance = 2p (pitch):
c    - Flat perpendicular to x: r1 r2 r3 = p 0 0
c    - Flat perpendicular to y: r1 r2 r3 = 0 p 0
c    - Apothem = perpendicular distance from center to face midpoint
c
c 3. EXAMPLE RHP SPECIFICATION:
c    10   RHP  0 0 0  0 0 100  0 5.0 0
c    Creates hex prism:
c    - Base at (0, 0, 0)
c    - Height 100 cm along z
c    - Apothem 5.0 cm perpendicular to y-axis
c    - Flat-to-flat distance = 10 cm
c
c 4. LAT=2 INDEXING (Ring/Position):
c    - Ring 0: Central element (1 element)
c    - Ring 1: 6 elements around center (positions 1-6)
c    - Ring 2: 12 elements around ring 1 (positions 1-12)
c    - Ring n: 6n elements
c
c 5. FILL ARRAY FOR LAT=2:
c    FILL=-ring_max:ring_max
c         <u_center>        $ Ring 0 (1 value)
c         <u1> ... <u6>     $ Ring 1 (6 values, counterclockwise from +x)
c         <u1> ... <u12>    $ Ring 2 (12 values)
c
c 6. EXAMPLE 7-ELEMENT ASSEMBLY (1 center + 6 ring):
c    FILL=0:1
c         1        $ Ring 0: central pin (universe 1)
c         1 1 1 1 1 1    $ Ring 1: 6 outer pins (all universe 1)
c
c 7. PIN CELL SIZING:
c    - Pin clad radius < hex pitch / sqrt(3)
c    - Leaves gap for coolant between pins
c
c 8. COMMON CONFIGURATIONS:
c    - 7 pins: FILL=0:1 (1 center + 6 ring 1)
c    - 19 pins: FILL=0:2 (1 center + 6 ring 1 + 12 ring 2)
c    - 37 pins: FILL=0:3 (1 + 6 + 12 + 18)
c    - 61 pins: FILL=0:4 (1 + 6 + 12 + 18 + 24)
c =================================================================
