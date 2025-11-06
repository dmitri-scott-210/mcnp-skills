WWG Iteration 1 - Initial Weight Window Generation
c ===============================================
c  This template shows Iteration 1: generating initial weight windows
c  Key: WWG card present, no WWP (no existing wwout to read)
c ===============================================
c
c --- Cell Cards ---
c [Insert your geometry here]
1   1  -7.85  -1   IMP:N=1    $ Source region
2   2  -2.3   1 -2  IMP:N=1    $ Shield
3   0        2 -3  IMP:N=1    $ Detector region
4   0        3     IMP:N=0    $ Graveyard
c
c --- Surface Cards ---
1   SO  10         $ Source sphere
2   SO  100        $ Shield outer
3   SO  120        $ Outer boundary
c
c --- Data Cards ---
MODE  N
c
c STEP 1: Define importance mesh
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-120 -120 -120
      IMESH=120  IINTS=24      $ 24 bins (5 cm each)
      JMESH=120  JINTS=24
      KMESH=120  KINTS=24
c     Total: 24^3 = 13,824 mesh cells
c
c STEP 2: Define energy structure for weight windows
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c       8 energy groups → 13,824 × 8 = 110,592 WW entries
c
c STEP 3: Define tally (WWG targets this)
F5:N  100 0 0  0.5            $ Point detector at (100,0,0)
c
c STEP 4: Generate weight windows from F5
WWG  5  0  1.0
c    ^tally 5  ^time group 0  ^target weight 1.0
c
c CRITICAL: No WWP card in iteration 1 (no existing wwout)
c          Weight window parameters use defaults:
c          - wupn = 5 (upper bound = 5 × lower bound)
c          - wsurvn = 3 (survival weight = 3 × lower bound)
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- Statistics ---
NPS  1e5                       $ Moderate for WWG generation
c
c --- Output ---
c  This run creates wwout file containing mesh-based weight windows
c  Expected FOM: 10-50× improvement over analog
