c ===================================================================
c TEMPLATE: Spherical Shielding Problem  
c ===================================================================
c DESCRIPTION: Point isotropic source in center of spherical shield
c PARAMETERS TO CUSTOMIZE:
c   Shield radius: 10.0 cm
c   Source strength: 1.0E10 particles/s
c   Shield material: Lead (adjust M1 card as needed)
c ===================================================================

c Cell Cards
1  1  -11.3  -1  IMP:N=1  $ Shield (lead)
2  0        1    IMP:N=0  $ Void outside

c Surface Cards  
1  SO  10.0  $ Shield outer surface (10 cm radius)

c Data Cards
MODE  N
SDEF  POS=0 0 0  ERG=1.0  $ 1 MeV point source at origin
M1  82000.80c  1.0  $ Lead (natural)
F2:N  1  $ Current at shield surface
F4:N  2  $ Flux beyond shield
NPS  1000000  $ 1 million particles
