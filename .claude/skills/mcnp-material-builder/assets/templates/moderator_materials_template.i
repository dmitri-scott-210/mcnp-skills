Moderator Material Templates for MCNP
c ==================================================================
c Purpose: Demonstrate common moderator materials (graphite,
c          polyethylene, beryllium) with proper S(alpha,beta)
c ==================================================================
c Cell Cards
1    1  -1.70   -1  IMP:N=1  TMP=6.2e-8     $ Graphite (nuclear grade), 900 K
2    2  -0.94   -2  IMP:N=1  TMP=2.53e-8    $ Polyethylene (CH2), 293.6 K
3    3  -1.85   -3  IMP:N=1  TMP=2.53e-8    $ Beryllium metal, 293.6 K
4    0            4  IMP:N=0                $ Void (graveyard)

c Surface Cards
1    SO  10.0                 $ Graphite sphere (10 cm radius)
2    SO  20.0                 $ Polyethylene sphere (20 cm radius)
3    SO  30.0                 $ Beryllium sphere (30 cm radius)
4    SO  100.0                $ Outer boundary

c Data Cards
MODE  N
c Material 1: Graphite (Nuclear Grade), 900 K
c Composition: Pure carbon with natural isotopic composition (C-12 + trace C-13)
c Density: 1.70 g/cm3, nuclear grade graphite moderator
c Excellent moderator for high-temperature gas reactors (HTGRs)
M1   6000.80c  1.0                                        $ Natural carbon
MT1  GRPH.43t                                              $ Graphite S(alpha,beta) at 600 K
c Material 2: Polyethylene (CH2)n, 293.6 K
c Composition: (CH2)n polymer, hydrogen-rich material
c Density: 0.94 g/cm3, commonly used for neutron shielding and moderation
c High hydrogen content provides excellent neutron slowing-down power
M2   1001.80c  2.0  6000.80c  1.0                         $ H:C atomic ratio 2:1
MT2  POLY.40t                                              $ Polyethylene S(alpha,beta) at 293.6 K
c Material 3: Beryllium Metal, 293.6 K
c Composition: Pure Be-9 (100% natural abundance)
c Density: 1.85 g/cm3, excellent neutron reflector and moderator
c Low absorption cross section, high scattering cross section
M3   4009.80c  1.0                                        $ Be-9
MT3  BE.40t                                                $ Beryllium S(alpha,beta) at 293.6 K
SDEF  POS=0 0 0  ERG=1.0
NPS  10000
PRINT
