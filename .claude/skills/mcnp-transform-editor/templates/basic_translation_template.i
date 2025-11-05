Basic Translation-Only TR Card Template
c =================================================================
c Demonstrates simple translation transformation
c Component moved from origin to specified position
c =================================================================
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0  -1      IMP:N=1  $ Original component at origin
2    1  -1.0  -2      IMP:N=1  $ Translated component using TR1
3    0         3      IMP:N=0  $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   5.0                   $ Sphere at origin, R=5 cm
2    1 SO  5.0                  $ Sphere transformed by TR1
3    SO   100.0                 $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
c --- Transformation Definition ---
*TR1  <dx> <dy> <dz>             $ Translation vector (cm)
c Example values:
c *TR1  20 0 0                   $ Move +20 cm in x-direction
c *TR1  0 15 0                   $ Move +15 cm in y-direction
c *TR1  10 10 -5                 $ Move +10 x, +10 y, -5 z
c --- Particle Mode ---
MODE  N
c --- Material Definition ---
M1    1001.80c  2  8016.80c  1  $ Water (H2O)
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=1.0         $ Point source at origin, 1 MeV
c --- Problem Termination ---
NPS   10000
PRINT
c =================================================================
c Template Instructions:
c =================================================================
c 1. Replace <dx> <dy> <dz> with translation vector components
c 2. Positive values move in positive axis direction
c 3. Surface 2 uses TR1 (indicated by "1" in second field)
c 4. Resulting sphere center: (dx, dy, dz)
c 5. No rotation applied (translation only)
c =================================================================
