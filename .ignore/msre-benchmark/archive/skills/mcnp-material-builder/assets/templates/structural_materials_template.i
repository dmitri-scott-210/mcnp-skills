Structural Material Templates for MCNP
c ==================================================================
c Purpose: Demonstrate common structural materials (steel, cladding,
c          concrete) with proper weight fractions and densities
c ==================================================================
c Cell Cards
1    1  -8.00   -1  IMP:N=1  TMP=2.53e-8    $ Stainless steel 316, 293.6 K
2    2  -6.56   -2  IMP:N=1  TMP=6.2e-8     $ Zircaloy-4 cladding, 900 K
3    3  -2.30   -3  IMP:N=1  TMP=2.53e-8    $ Ordinary concrete, 293.6 K
4    0            4  IMP:N=0                $ Void (graveyard)

c Surface Cards
1    SO  10.0                 $ SS-316 sphere (10 cm radius)
2    SO  20.0                 $ Zircaloy sphere (20 cm radius)
3    SO  30.0                 $ Concrete sphere (30 cm radius)
4    SO  100.0                $ Outer boundary

c Data Cards
MODE  N
c Material 1: Stainless Steel 316 (SS-316), 293.6 K
c Composition (weight %): Fe 65%, Cr 17%, Ni 12%, Mo 2.5%, Mn 2%, Si 1%, C 0.08%
c Density: 8.0 g/cm3, typical reactor structural material
M1   26000.80c  -0.65  24000.80c  -0.17  28000.80c  -0.12  &
     42000.80c  -0.025  25055.80c  -0.02  14000.80c  -0.01  &
     6000.80c  -0.0008                                        $ Weight fractions
c Material 2: Zircaloy-4 (Zr-4), 900 K
c Composition (weight %): Zr 98.23%, Sn 1.45%, Fe 0.21%, Cr 0.10%, O 0.125%
c Density: 6.56 g/cm3, typical fuel cladding material
c Low neutron absorption cross section makes it ideal for fuel cladding
M2   40000.80c  -0.9823  50000.80c  -0.0145  26000.80c  -0.0021  &
     24000.80c  -0.0010  8016.80c  -0.00125                  $ Weight fractions
c Material 3: Ordinary Concrete, 293.6 K
c Composition (weight %): H 1.0%, C 0.1%, O 52.9%, Na 1.6%, Mg 0.2%,
c                         Al 3.4%, Si 33.7%, K 1.3%, Ca 4.4%, Fe 1.4%
c Density: 2.3 g/cm3, typical shielding and structural material
M3   1001.80c  -0.01  6000.80c  -0.001  8016.80c  -0.529  &
     11023.80c  -0.016  12000.80c  -0.002  13027.80c  -0.034  &
     14000.80c  -0.337  19000.80c  -0.013  20000.80c  -0.044  &
     26000.80c  -0.014                                        $ Weight fractions for concrete
SDEF  POS=0 0 0  ERG=1.0
NPS  10000
PRINT
