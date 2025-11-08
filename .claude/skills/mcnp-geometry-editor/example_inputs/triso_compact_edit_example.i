TRISO Compact Scaling Example - Before and After 1.2× Scale
c ================================================================
c This example demonstrates scaling a TRISO particle compact
c from original to 1.2× size, maintaining all hierarchy levels.
c
c Hierarchy:
c   Level 1: TRISO particle (u=1114) - 5 concentric shells
c   Level 3: Particle lattice (u=1116, LAT=1) - 15×15 array
c   Level 5: Compact lattice (u=1110, LAT=1) - 1×1×31 vertical
c   Level 6: Global placement with fill transformation
c
c ORIGINAL geometry shown first, SCALED (1.2×) shown after
c ================================================================
c
c ========== CELL CARDS ==========
c
c --- ORIGINAL TRISO Particle (u=1114) ---
c
91101 9111 -10.924 -91111  u=1114 vol=0.000224  $ Kernel (UC)
91102 9112 -1.100  91111 -91112  u=1114 vol=0.001542  $ Buffer
91103 9113 -1.900  91112 -91113  u=1114 vol=0.000531  $ IPyC
91104 9114 -3.200  91113 -91114  u=1114 vol=0.000503  $ SiC
91105 9115 -1.900  91114 -91115  u=1114 vol=0.000581  $ OPyC
c
c --- SCALED TRISO Particle (u=1114) - volumes × 1.2³ = 1.728 ---
c
c 91101 9111 -10.924 -91111  u=1114 vol=0.000387  $ Kernel (scaled)
c 91102 9112 -1.100  91111 -91112  u=1114 vol=0.002664  $ Buffer (scaled)
c 91103 9113 -1.900  91112 -91113  u=1114 vol=0.000918  $ IPyC (scaled)
c 91104 9114 -3.200  91113 -91114  u=1114 vol=0.000869  $ SiC (scaled)
c 91105 9115 -1.900  91114 -91115  u=1114 vol=0.001004  $ OPyC (scaled)
c
c --- Matrix Cell (u=1115) ---
c
91115 9117 -1.700 -91117  u=1115  $ Graphite matrix
c
c --- Particle Lattice (u=1116, LAT=1) ---
c
91116 0  -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
     1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114  &
     1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115
c 15×15 checkerboard pattern (particle/matrix alternating)
c
c --- Matrix Filler (u=1117) ---
c
91117 9117 -1.700 -91118  u=1117  $ Pure graphite cell
c
c --- Compact Lattice (u=1110, LAT=1) ---
c
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15  &
     1117 1117 1116 24R 1117 1117 1117
c 31 layers: 2 matrix bottom, 25 particle layers, 4 matrix top
c
c --- Global Placement ---
c
91111 0  -97011  98005 -98051  fill=1110  (25.547039 -24.553123 19.108100)  &
     imp:n=1  $ Compact at Stack 1 position
c
99999 0  97011 : -98005 : 98051  imp:n=0  $ Graveyard
c
c ========== SURFACE CARDS ==========
c
c --- ORIGINAL TRISO Particle Surfaces (u=1114) ---
c
91111 so   0.017485  $ Kernel, R = 174.85 μm
91112 so   0.027905  $ Buffer, R = 279.05 μm
91113 so   0.031785  $ IPyC, R = 317.85 μm
91114 so   0.035375  $ SiC, R = 353.75 μm
91115 so   0.039305  $ OPyC, R = 393.05 μm
c
c --- SCALED TRISO Particle Surfaces (×1.2) ---
c
c 91111 so   0.020982  $ Kernel: 0.017485 × 1.2
c 91112 so   0.033486  $ Buffer: 0.027905 × 1.2
c 91113 so   0.038142  $ IPyC: 0.031785 × 1.2
c 91114 so   0.042450  $ SiC: 0.035375 × 1.2
c 91115 so   0.047166  $ OPyC: 0.039305 × 1.2
c
c --- ORIGINAL Particle Lattice Bounding Surface (u=1116) ---
c
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
c     ±87.43 μm (X,Y), ±100 μm (Z)
c
c --- SCALED Particle Lattice Bounding Surface (×1.2) ---
c
c 91117 rpp -0.052458 0.052458 -0.052458 0.052458 -0.060000 0.060000
c
c --- ORIGINAL Compact Lattice Bounding Surface (u=1110) ---
c
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
c     ±0.65 cm (X,Y), ±0.043715 cm (Z, single layer)
c
c --- SCALED Compact Lattice Bounding Surface (×1.2) ---
c
c 91118 rpp -0.780000 0.780000 -0.780000 0.780000 -0.052458 0.052458
c
c --- ORIGINAL Global Placement Surfaces ---
c
97011 c/z   25.547039 -24.553123   0.63500  $ Compact cylinder
98005 pz   17.81810  $ Bottom Z-plane
98051 pz   20.35810  $ Top Z-plane (compact height = 2.54 cm)
c
c --- SCALED Global Placement Surfaces (×1.2) ---
c
c 97011 c/z   25.547039 -24.553123   0.76200  $ R: 0.635 × 1.2
c 98005 pz   21.38172  $ Z: 17.818 × 1.2
c 98051 pz   24.42972  $ Z: 20.358 × 1.2
c
c ========== DATA CARDS ==========
c
c --- Materials ---
c
m9111 92235.80c 1.0  $ UC kernel (enriched uranium carbide)
m9112 6000.80c 1.0  $ Porous carbon buffer
m9113 6000.80c 1.0  $ IPyC (inner pyrolytic carbon)
m9114 14000.80c 1.0  $ SiC (silicon carbide)
m9115 6000.80c 1.0  $ OPyC (outer pyrolytic carbon)
m9117 6000.80c 1.0  $ Graphite matrix
c
c --- Source (neutron point source at compact center) ---
c
sdef pos 25.547039 -24.553123 19.108100  erg=2.0
c
c --- Tallies ---
c
f4:n 91101  $ Flux in kernel
c
c --- Problem Parameters ---
c
mode n
nps 1000
c
c ================================================================
c END OF TRISO COMPACT SCALING EXAMPLE
c
c TO IMPLEMENT SCALING:
c 1. Uncomment SCALED cells (c → space)
c 2. Comment out ORIGINAL cells (space → c)
c 3. Uncomment SCALED surfaces
c 4. Comment out ORIGINAL surfaces
c 5. Update SDEF position if entire compact scaled
c 6. Run MCNP and plot to verify
c
c VALIDATION CHECKS:
c - All radii scaled by 1.2
c - Volumes scaled by 1.2³ = 1.728
c - Lattice bounding surfaces scaled in all dimensions
c - Concentric relationship preserved (R1 < R2 < R3 < R4 < R5)
c - No lost particles
c ================================================================
