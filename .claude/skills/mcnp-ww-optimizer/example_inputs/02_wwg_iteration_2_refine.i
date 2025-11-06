WWG Iteration 2 - Refine Weight Windows
c ===============================================
c  This template shows Iteration 2: refining weight windows
c  Key: WWP reads previous wwout, WWG regenerates improved wwout
c ===============================================
c
c --- Cell Cards ---
c [Insert your geometry here - MUST BE IDENTICAL to iteration 1]
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
c STEP 1: Define importance mesh (MUST MATCH iteration 1!)
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-120 -120 -120
      IMESH=120  IINTS=24
      JMESH=120  JINTS=24
      KMESH=120  KINTS=24
c     CRITICAL: Must be IDENTICAL to iteration 1
c
c STEP 2: Define energy structure (MUST MATCH iteration 1!)
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c       CRITICAL: Must be IDENTICAL to iteration 1
c
c STEP 3: Read weight windows from iteration 1
WWP:N  J  J  J  0  -1
c      ^read lower bounds from wwout file
c         ^default wupn and wsurvn
c               ^check WW at collisions and surfaces
c                     ^read from wwout file (switchn=-1)
c
c ALTERNATE: Adjust parameters if needed
c WWP:N  10  3  5  0  -1    $ Widen window (wupn=10)
c
c STEP 4: Define tally (same as iteration 1)
F5:N  100 0 0  0.5
c
c STEP 5: Regenerate improved weight windows
WWG  5  0  1.0
c    CRITICAL: WWG still present → generates NEW wwout
c              (overwrites previous wwout)
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- Statistics ---
NPS  2e5                       $ Increased for better WW
c
c --- Output ---
c  This run creates IMPROVED wwout file
c  Expected FOM: 2-5× improvement over iteration 1
c  Check FOM change: if <20%, converged!
