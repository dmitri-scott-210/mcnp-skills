Nested Universe Example - Three-level hierarchy
c
c Example demonstrating:
c   - Three-level nesting (pin -> assembly -> core)
c   - FILL without LAT for single universe
c   - Universe hierarchy (U=0, U=1, U=2, U=3)
c
c Level 1: Pin (U=1)
1    1  -10.5  -1     U=1  IMP:N=1    $ Fuel
2    2  -6.5    1 -2  U=1  IMP:N=1    $ Clad
3    0          2     U=1  IMP:N=1    $ Void outside pin
c Level 2: Assembly (U=2) - contains pin
10   0  -10  FILL=1  U=2  IMP:N=1     $ Fill with pin universe
c Level 3: Core (U=3) - contains assembly
20   0  -20  FILL=2  U=3  IMP:N=1     $ Fill with assembly
c Level 4: Base geometry (U=0) - contains core
30   0  -30  FILL=3  IMP:N=1          $ Fill with core
31   0   30  IMP:N=0                  $ Graveyard

c Pin surfaces (local to U=1)
1    CZ  0.5
2    CZ  0.6
c Assembly boundary (local to U=2)
10   RPP  -2 2  -2 2  0 10
c Core boundary (local to U=3)
20   RPP  -5 5  -5 5  -2 12
c Outer boundary (U=0)
30   RPP  -10 10  -10 10  -5 15

c Data Cards
MODE N
SDEF  CEL=30  ERG=2.0
M1   92235  -0.04  92238  -0.96  8016  -2.0
M2   40000  1.0
NPS  10000
