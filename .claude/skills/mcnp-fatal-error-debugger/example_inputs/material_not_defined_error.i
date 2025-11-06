Material Not Defined Error - Example
c =================================================================
c Cell Cards
c =================================================================
c
1  1  -1.0   -1  IMP:N=1              $ Cell 1, material 1 (OK)
2  2  -2.3   1 -2  IMP:N=1            $ Cell 2, material 2 (OK)
5  3  -11.3  2 -3  IMP:N=1            $ Cell 5, material 3 (ERROR: M3 not defined)
999  0  3  IMP:N=0                    $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
c
1  SO  10                              $ Sphere R=10
2  SO  20                              $ Sphere R=20
3  SO  30                              $ Sphere R=30

c =================================================================
c Data Cards
c =================================================================
c
MODE  N
M1  1001.80c  2  8016.80c  1          $ Water (OK)
M2  6000.80c  1                       $ Carbon (OK)
c M3 not defined!                     $ ERROR: Material 3 missing
SDEF  POS=0 0 0  ERG=14.1
NPS  1000
c
c ERROR: fatal error.  material   3 has not been specified but is used in cell    5.
c
c FIX: Add M3 card with appropriate composition
c M3  82000.80c  1.0                  $ Lead
