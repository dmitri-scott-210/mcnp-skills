MCNP Surface Source Templates - SSW/SSR Two-Stage Calculations
c ========================================================================
c OVERVIEW: Surface source read/write for two-stage calculations
c Stage 1: Run with SSW to write surface crossing data
c Stage 2: Run with SSR to read and use surface source
c ========================================================================
c Cell Cards
c ========================================================================
c ========================================================================
c STAGE 1 GEOMETRY: Write Surface Source
c ========================================================================
c 1    1  -11.35   -1   IMP:N=1    $ Lead shield (stage 1)
c 2    2  -1.0   -2  1  IMP:N=1    $ Air gap
c 3    0           2    IMP:N=0    $ Graveyard
c ========================================================================
c STAGE 2 GEOMETRY: Read Surface Source
c ========================================================================
1    2  -1.0     -1   IMP:N=1    $ Air region (detector side)
2    3  -1.0   -2  1  IMP:N=1    $ Water phantom
3    0           2    IMP:N=0    $ Graveyard

c ========================================================================
c Surface Cards
c ========================================================================
1    PZ  0                       $ Plane at z=0 (SSW/SSR interface)
2    SO  30                      $ Outer sphere radius 30 cm

c ========================================================================
c Data Cards
c ========================================================================
MODE N P
c ========================================================================
c STAGE 1: Surface Source Write (SSW)
c ========================================================================
c Run stage 1 to write surface crossings to WSSA file
c SSW n
c   n = surface number to write crossings (positive = forward, negative = both)
c ========================================================================
c TEMPLATE 1: Write Forward Crossings on Surface 1
c ========================================================================
c Uncomment for stage 1:
c SDEF  POS=0 0 -20  ERG=1.0  PAR=N
c SSW   1            $ Write particles crossing surface 1 in +normal direction
c ========================================================================
c TEMPLATE 2: Write All Crossings (Both Directions)
c ========================================================================
c Uncomment for stage 1:
c SDEF  POS=0 0 -20  ERG=D1  PAR=N
c SI1 L 0.5  1.0  2.0  5.0   $ Neutron energies (MeV)
c SP1   0.1  0.3  0.4  0.2   $ Probabilities
c SSW   -1           $ Write both forward and backward crossings
c ========================================================================
c STAGE 2: Surface Source Read (SSR)
c ========================================================================
c Run stage 2 to read particles from RSSA file (created from stage 1 WSSA)
c SSR n NPS=m
c   n   = surface number to read from (must match SSW surface)
c   NPS = number of particles to sample from surface source
c ========================================================================
c TEMPLATE 1: Basic SSR (Read Forward Crossings)
c ========================================================================
SSR   1  NPS=50000
c Read 50,000 particles from surface 1, sample from RSSA distribution
c ========================================================================
c TEMPLATE 2: SSR with Options
c ========================================================================
c SSR   1  NPS=1e5  TR=1  COL=1
c   TR=1: Apply transformation #1 to source particles
c   COL=1: Force first collision in each history
c ========================================================================
c TEMPLATE 3: SSR Spherically Symmetric (for spherical geometry)
c ========================================================================
c SSR   AXS=0 0 1  EXT=D1  POA=D2  BCW=no
c   AXS: Axis of symmetry
c   EXT: Axial extent distribution
c   POA: Polar angle distribution
c   BCW: Backward/forward weighting (yes/no)
c ========================================================================
c Materials for Stage 1
c ========================================================================
c M1   82000.80c  1       $ Lead (for shielding calculation)
c ========================================================================
c Materials for Stage 2
c ========================================================================
M2   7014.80c   0.79     $ Nitrogen (air)
     8016.80c   0.21     $ Oxygen
M3   1001.80c   2        $ Hydrogen (water phantom)
     8016.80c   1        $ Oxygen
MT3  H-H2O.40t           $ S(alpha,beta) for water
c ========================================================================
c Stage 2 Tallies
c ========================================================================
F4:N 2                           $ Flux in water phantom
E4   0.01  0.1  0.5  1  2  5  10  20   $ Energy bins (MeV)
F6:N,P 2                         $ Heating in water phantom
c ========================================================================
c Common Settings
c ========================================================================
c For Stage 1: Uncomment SSW, comment SSR, use stage 1 geometry and SDEF
c For Stage 2: Comment SSW, uncomment SSR, use stage 2 geometry
c ========================================================================
c Workflow:
c 1. Run stage 1 with SSW → produces WSSA file
c 2. Run MCNP utility to convert WSSA to RSSA (if needed)
c 3. Run stage 2 with SSR → reads from RSSA
c ========================================================================
c Important Notes:
c - WSSA is ASCII file (large), RSSA is binary (smaller)
c - Use WSSA for portability, RSSA for efficiency
c - Surface source must be on geometry boundary
c - NPS in SSR determines how many times to sample from surface source
c - Particles are randomly sampled from recorded crossings
c ========================================================================
NPS  5e4
