WWG Production Run - Converged Weight Windows
c ===============================================
c  This template shows Production: using converged weight windows
c  Key: WWP reads wwout, NO WWG (just use WW, don't regenerate)
c ===============================================
c
c --- Cell Cards ---
c [Insert your geometry here - MUST BE IDENTICAL to iterations]
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
c STEP 1: Define importance mesh (MUST MATCH iterations!)
MESH  GEOM=XYZ  REF=0 0 0  ORIGIN=-120 -120 -120
      IMESH=120  IINTS=24
      JMESH=120  JINTS=24
      KMESH=120  KINTS=24
c     CRITICAL: Must be IDENTICAL to all iterations
c
c STEP 2: Define energy structure (MUST MATCH iterations!)
WWGE:N  1e-10  1e-8  1e-6  1e-4  0.01  0.1  1  10  20
c       CRITICAL: Must be IDENTICAL to all iterations
c
c STEP 3: Read converged weight windows
WWP:N  J  J  J  0  -1
c      ^read lower bounds from wwout file
c
c CRITICAL: NO WWG card in production run!
c           Just use weight windows, don't regenerate them.
c
c STEP 4: Define tally
F5:N  100 0 0  0.5
c
c --- Source ---
SDEF  POS=0 0 0  ERG=14.1
c
c --- Statistics ---
NPS  1e7                       $ High statistics for final results
c
c --- Output ---
c  Production results with low relative error
c  FOM should match iteration 2-3 (converged value)
c  All 10 statistical checks should pass
c  Target: Relative error < 5%
