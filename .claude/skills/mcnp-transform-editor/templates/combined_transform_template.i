Combined Translation and Rotation TR Card Template
c =================================================================
c Demonstrates combined translation + rotation transformation
c Component moved AND reoriented (most general case)
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0  -1      IMP:N=1  $ Original cylinder (axis along +x)
2    1  -1.0  -2      IMP:N=1  $ Transformed cylinder using TR1
3    0         3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RCC  0 0 0  10 0 0  2                    $ Cylinder at origin, along +x
2    1 RCC  0 0 0  10 0 0  2                  $ Cylinder transformed by TR1
3    SO   100.0                                $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
*TR1  <dx> <dy> <dz>  <a11> <a12> <a13>  <a21> <a22> <a23>  <a31> <a32> <a33>
c Example: Move to (20, 10, 0) and rotate 90° about z-axis
c *TR1  20 10 0  0 -1 0  1 0 0  0 0 1
c Result: Cylinder center at (20, 10, 0), axis reoriented to +y direction
c Example: Move to (15, 0, 0) and rotate 45° about z-axis
c *TR1  15 0 0  0.707 -0.707 0  0.707 0.707 0  0 0 1
c Alternative (degree input for rotation):
c *TR1  <dx> <dy> <dz>  <theta_x> <theta_y> <theta_z>  1
c Example: Move to (20, 10, 0) and rotate 90° about z
c *TR1  20 10 0  0 0 90  1
c --- Particle Mode ---
MODE  N
c --- Material Definition ---
M1    13027.80c  1                            $ Aluminum
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0                      $ Point source at origin
c --- Problem Termination ---
NPS   10000
PRINT
c =================================================================
c Template Instructions:
c =================================================================
c 1. Replace <dx> <dy> <dz> with translation vector
c 2. Replace <aij> with rotation matrix elements OR use degree input
c 3. Order of operations:
c    - Rotation is applied FIRST (about origin)
c    - Translation is applied SECOND (moves rotated object)
c 4. For complex rotations:
c    - Use scripts/rotation_matrix_generator.py to create matrix
c    - Validate with scripts/tr_matrix_validator.py
c 5. Surface 2 uses TR1 (indicated by "1" in second field)
c 6. Matrix requirements (if using explicit form):
c    - Orthonormal (row norms = 1)
c    - Orthogonal (rows perpendicular)
c    - Determinant = ±1
c =================================================================
c Workflow for Complex Transformations:
c =================================================================
c Step 1: Define desired rotation
c   - Axis-angle: python rotation_matrix_generator.py --axis 1 1 1 --angle 30 --degrees
c   - Euler angles: python rotation_matrix_generator.py --euler 30 45 60 --degrees
c Step 2: Validate generated matrix
c   - python tr_matrix_validator.py <matrix elements>
c Step 3: Add translation vector
c   - Combine rotation matrix with translation: dx dy dz
c Step 4: Insert into TR card above
c Step 5: Verify geometry with MCNP plotter
c =================================================================
