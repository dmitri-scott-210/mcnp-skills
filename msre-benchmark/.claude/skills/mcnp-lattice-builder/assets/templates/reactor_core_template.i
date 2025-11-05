Reactor Core Template - Flux-Based Grouping Example
c =================================================================
c Template for reactor core with flux-based grouping
c Demonstrates proper universe assignment by flux zone
c User must fill in: dimensions, materials, enrichments by zone
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- Pin Cells (Universe 1-3 by flux zone) ---
c Universe 1: High flux zone (center, fresh fuel)
1    1  <dens>  -1     U=1  IMP:N=1  VOL=<calc>  $ Fuel (high enrichment)
2    2  <dens>   1     U=1  IMP:N=1  VOL=<calc>  $ Clad/water
c Universe 2: Medium flux zone (middle ring)
11   1  <dens>  -1     U=2  IMP:N=1  VOL=<calc>  $ Fuel (medium burn)
12   2  <dens>   1     U=2  IMP:N=1  VOL=<calc>  $ Clad/water
c Universe 3: Low flux zone (outer ring)
21   1  <dens>  -1     U=3  IMP:N=1  VOL=<calc>  $ Fuel (high burn)
22   2  <dens>   1     U=3  IMP:N=1  VOL=<calc>  $ Clad/water

c --- Assembly Lattices (Universe 10-12 by zone) ---
c    Each zone gets independent universe for flux/depletion
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1  $ High flux assy
110  0  -10 11 -12 13 -14 15  U=11  LAT=1  FILL=2  IMP:N=1  $ Med flux assy
120  0  -10 11 -12 13 -14 15  U=12  LAT=1  FILL=3  IMP:N=1  $ Low flux assy

c --- Core Lattice (Universe 100) ---
1000 0  -100 101 -102 103 -104 105  U=100  LAT=1  IMP:N=1  &
        FILL=<imin>:<imax> <jmin>:<jmax> 0:0                &
             <pattern: 12 at edges, 11 in middle, 10 at center>
c
c    Example 3×3 core:
c    FILL=0:2 0:2 0:0
c         12 11 12    $ j=0 (bottom row): outer, middle, outer
c         11 10 11    $ j=1 (middle row): middle, center, middle
c         12 11 12    $ j=2 (top row): outer, middle, outer
c
c    Rule: GROUP BY FLUX ZONE, NOT GEOMETRIC CONVENIENCE
c    Fresh fuel (U=10) at center (highest flux)
c    Burned fuel (U=11,12) at periphery (lower flux)

c --- Real World ---
10000 0  -10000  FILL=100  IMP:N=1                    $ Core
10001 <mat#>  <dens>  10000 -10001  IMP:N=1          $ Reflector
10002 <mat#>  <dens>  10001 -10002  IMP:N=1          $ Barrel
10003 0  10002  IMP:N=0

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
1    CZ   <pin_radius>

10   PX   0.0
11   PX   <N*pin_pitch>
12   PY   0.0
13   PY   <N*pin_pitch>
14   PZ   0.0
15   PZ   <height>

100  PX   0.0
101  PX   <M*assembly_pitch>
102  PY   0.0
103  PY   <M*assembly_pitch>
104  PZ   <zmin>
105  PZ   <zmax>

10000 RCC  0 0 0  0 0 <H>  <R_core>
10001 RCC  0 0 0  0 0 <H>  <R_reflector>
10002 RCC  0 0 0  0 0 <H>  <R_barrel>

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials (Different by burnup zone) ---
c Mat 1: Fuel (User must specify enrichment/composition by zone)
M1   92235.80c  <frac_zone1>  92238.80c  <frac>  8016.80c  2.0
c M1 for U=1 (fresh), different M for U=2,3 (burned) in real model
c Mat 2: Clad/water
M2   ...
c --- Criticality Source ---
KCODE  10000  1.0  50  200
KSRC   <center_x> <center_y> <center_z>
c --- Tallies (by flux zone) ---
F4:N  (1 < 100 < 1000[<center_indices>])    $ High flux zone
F14:N (11 < 110 < 1000)                      $ Med flux zone
F24:N (21 < 120 < 1000)                      $ Low flux zone
c --- Termination ---
PRINT

c CRITICAL: Flux-based grouping prevents 15.6% error
c See AGR-1 verification: whole-core = 15.6% error, flux-based = 4.3%
