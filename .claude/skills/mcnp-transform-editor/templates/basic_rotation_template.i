Basic Rotation-Only TR Card Template
c =================================================================
c Demonstrates rotation transformation (no translation)
c Useful for reorienting components about origin
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0  -1      IMP:N=1  $ Original box (oriented along axes)
2    1  -1.0  -2      IMP:N=1  $ Rotated box using TR1
3    0         3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    BOX  -2 -2 -2  4 0 0  0 4 0  0 0 4        $ Box at origin
2    1 BOX  -2 -2 -2  4 0 0  0 4 0  0 0 4     $ Box transformed by TR1
3    SO   20.0                                 $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
c Method 1: Explicit rotation matrix (9 additional parameters)
*TR1  0 0 0  <a11> <a12> <a13>  <a21> <a22> <a23>  <a31> <a32> <a33>
c Method 2: Degree input mode (3 angles + m=1 flag)
c *TR1  0 0 0  <theta_x> <theta_y> <theta_z>  1
c Example values (90° CCW rotation about z-axis):
c *TR1  0 0 0  0 -1 0  1 0 0  0 0 1           $ Matrix form
c *TR1  0 0 0  0 0 90  1                      $ Degree form
c Common single-axis rotations (90° CCW):
c About x: *TR1  0 0 0  1 0 0  0 0 -1  0 1 0
c About y: *TR1  0 0 0  0 0 1  0 1 0  -1 0 0
c About z: *TR1  0 0 0  0 -1 0  1 0 0  0 0 1
c --- Particle Mode ---
MODE  N
c --- Material Definition ---
M1    26000.80c  1                            $ Iron
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0                      $ Point source at origin
c --- Problem Termination ---
NPS   10000
PRINT
c =================================================================
c Template Instructions:
c =================================================================
c 1. Choose Method 1 (matrix) OR Method 2 (degrees), not both
c 2. For Method 1: Replace <aij> with rotation matrix elements
c    - Matrix must be orthonormal (rows are unit vectors)
c    - Rows must be perpendicular to each other
c    - Determinant must equal ±1
c 3. For Method 2: Replace <theta_x/y/z> with rotation angles
c    - Angles in degrees (flag m=1 indicates degree mode)
c    - MCNP applies: Rx(theta_x) · Ry(theta_y) · Rz(theta_z)
c 4. Translation is zero (rotation about origin)
c 5. Use scripts/rotation_matrix_generator.py to create matrices
c 6. Validate with scripts/tr_matrix_validator.py before use
c =================================================================
