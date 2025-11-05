Transformed Geometry Template - TR card transformations
c =================================================================
c Template for geometry using coordinate transformations (TR cards)
c Replace parameters marked with <...> with actual values
c =================================================================
c
c Cell Cards
1    <mat1>  <dens1>  -1        IMP:N=1  $ Object 1 (untransformed)
2    <mat2>  <dens2>  -11       IMP:N=1  $ Object 2 (transformed, surface 1 with TR1)
3    <mat3>  <dens3>  -21       IMP:N=1  $ Object 3 (transformed, surface 1 with TR2)
4    0                1 11 21 -99  IMP:N=1  $ Void region
5    0                99       IMP:N=0  $ Graveyard

c Surface Cards
1    <surf_type>  <params>                   $ Base surface (untransformed)
11   1  <surf_type>  <params>                $ Same surface with TR1 transformation
21   2  <surf_type>  <params>                $ Same surface with TR2 transformation
99   SO   <r_boundary>                       $ Problem boundary

c Data Cards
MODE  N
SDEF  POS=0 0 0  ERG=<energy>
c --- Transformation Cards ---
TR1   <o1> <o2> <o3>                         $ Translation only (displacement vector)
*TR2  <o1> <o2> <o3>  <θx'> <θy'> <θz'>  1   $ Translation + rotation (angles in degrees)
c --- Materials ---
M<mat1>  <ZAID> <frac> <ZAID> <frac>
M<mat2>  <ZAID> <frac> <ZAID> <frac>
M<mat3>  <ZAID> <frac> <ZAID> <frac>
NPS   <histories>
PRINT
c =================================================================
c TR CARD INSTRUCTIONS:
c
c 1. TR CARD FORMAT:
c    TR n  o1 o2 o3  [matrix entries]  [m]
c    - n: Transformation number (1-999 for surface TR, unlimited for TRCL)
c    - o1 o2 o3: Displacement vector
c    - matrix: Rotation matrix (optional)
c    - m: Origin flag (1 = default, -1 = reverse)
c
c 2. TRANSLATION ONLY:
c    TR1  10 0 0
c    Translates auxiliary origin to (10, 0, 0) in main system
c
c 3. ROTATION WITH *TR (ANGLES IN DEGREES):
c    *TR2  0 0 0  90 0 0  0 90 0  0 0 90
c    Angles: xx' yx' zx'  xy' yy' zy'  xz' yz' zz'
c    - xx' = angle between main x-axis and auxiliary x'-axis
c
c 4. ROTATION WITH TR (DIRECTION COSINES):
c    TR3  0 0 0  0 1 0  -1 0 0  0 0 1
c    Cosines: xx' yx' zx'  xy' yy' zy'  xz' yz' zz'
c    90° rotation about z-axis
c
c 5. COMMON PATTERNS:
c    a) All 9 matrix elements (required for left/right hand systems)
c    b) 6 elements (two vectors) - MCNP creates third by cross product
c    c) 5 elements (one vector each way) - MCNP fills via Eulerian angles
c    d) 3 elements (one vector) - MCNP creates others arbitrarily
c    e) 0 elements (identity) - translation only
c
c 6. SURFACE TRANSFORMATION USAGE:
c    Format:  j  n  <surf_mnemonic>  <params>
c    Example: 10  5  CZ  2.0
c    - Surface 10 references TR5 transformation
c    - Define cylinder in auxiliary system (simple: CZ centered on z')
c    - TR5 positions/orients it in main system
c
c 7. CELL TRANSFORMATION (TRCL):
c    Cell format:  j  m  d  geom  TRCL=n
c    Example: 10  1  -2.7  -1  TRCL=5
c    - Cell 10 surfaces defined in main system
c    - Cell positioned using TR5 transformation
c    - TRCL allows unlimited transformation numbers
c
c 8. ROTATION EXAMPLES:
c    a) 90° about z-axis:
c       *TR1  0 0 0  90 0 90  0 90 0  90 90 0
c       (x' along y, y' along -x, z' along z)
c
c    b) 180° about x-axis:
c       *TR2  0 0 0  0 0 0  0 180 90  0 90 180
c       (x' along x, y' along -y, z' along -z)
c
c    c) 45° about z-axis:
c       *TR3  0 0 0  45 45 90  135 45 90  90 90 0
c
c 9. DISPLACEMENT VECTOR ORIGIN (m parameter):
c    m = 1 (default): o1 o2 o3 = location of auxiliary origin in main system
c    m = -1: o1 o2 o3 = location of main origin in auxiliary system
c
c 10. EXAMPLE - SKEWED CYLINDER:
c     Instead of complex GQ surface:
c     10  7  CX  1.0          $ Simple cylinder on x'-axis in auxiliary system
c     *TR7  6 1 -1.732  0 30 60  $ Position/orient in main system
c
c 11. RESTRICTIONS:
c     - Periodic boundaries cannot use TR
c     - Cell transformations can generate surfaces: number = surf + 1000×cell
c     - Surface TR limited to n ≤ 999
c     - Original surfaces with TR must have j ≤ 999
c
c 12. DEBUGGING:
c     - Plot geometry to verify transformation
c     - Check that rotation matrix is orthogonal (rows/columns orthonormal)
c     - Use *TR with degrees for intuitive angle specification
c =================================================================
