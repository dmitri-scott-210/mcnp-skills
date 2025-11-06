Simple Cartesian FMESH Example - 20x20x20 cm cube
c =================================================================
c Cell Cards
c =================================================================
1    1  -1.0  -1   IMP:N=1    $ Water sphere
2    0         1   IMP:N=0    $ Void (graveyard)
c
c =================================================================
c Surface Cards
c =================================================================
1    SO  20                    $ Sphere radius 20 cm
c
c =================================================================
c Data Cards
c =================================================================
MODE N
c
c --- Material: Water ---
M1   1001.80c  2  8016.80c  1
c
c --- Source: 14 MeV neutrons at origin ---
SDEF  POS=0 0 0  ERG=14
c
c --- Cartesian mesh tally (flux) ---
FMESH4:N  GEOM=XYZ
          ORIGIN=-10 -10 -10
          IMESH=10  IINTS=20
          JMESH=10  JINTS=20
          KMESH=10  KINTS=20
          OUT=xdmf
c
c Total bins: 20x20x20 = 8,000
c
NPS  1e7
