Multi-Level Hierarchy Modification Example
c ================================================================
c This example demonstrates adding an intermediate lattice layer
c between compact and particle lattices without breaking nesting.
c
c ORIGINAL Hierarchy (3 levels):
c   Compact lattice (u=1110)
c     └─ Fills with u=1116 (particle lattice) and u=1117 (matrix)
c
c   Particle lattice (u=1116)
c     └─ Fills with u=1114 (particle) and u=1115 (matrix cell)
c
c   TRISO particle (u=1114)
c
c NEW Hierarchy (4 levels, insert intermediate layer):
c   Compact lattice (u=1110)
c     └─ Fills with u=1118 (NEW: sub-compact layer)
c
c   Sub-compact layer (u=1118) ← NEW LEVEL
c     └─ Fills with u=1116 (particle lattice) and u=1117 (matrix)
c
c   Particle lattice (u=1116)
c     └─ Fills with u=1114 (particle) and u=1115 (matrix cell)
c
c   TRISO particle (u=1114)
c ================================================================
c
c ========== CELL CARDS ==========
c
c --- Level 1: TRISO Particle (u=1114) ---
c
91101 9111 -10.4 -91111  u=1114  $ Fuel kernel
91102 9112 -1.1  91111 -91112  u=1114  $ Buffer
91103 9113 -1.9  91112 -91113  u=1114  $ Coating
c
c --- Level 2: Matrix Cell (u=1115) ---
c
91115 9117 -1.7 -91117  u=1115  $ Graphite matrix
c
c --- Level 3: ORIGINAL Particle Lattice (u=1116, LAT=1) ---
c
91116 0  -91117  u=1116 lat=1  fill=-1:1 -1:1 0:0  &
     1115 1114 1115  &
     1114 1115 1114  &
     1115 1114 1115
c 3×3 checkerboard pattern (simplified from 15×15 for example)
c
c --- Level 4: Matrix Filler (u=1117) ---
c
91117 9117 -1.7 -91118  u=1117  $ Pure graphite
c
c --- NEW LEVEL: Sub-Compact Layer (u=1118, LAT=1) ---
c This universe groups 3 particle lattices vertically
c
91119 0  -91120  u=1118 lat=1  fill=0:0 0:0 -1:1  &
     1117 1116 1117
c Matrix - Particles - Matrix (3 vertical layers)
c
c --- Level 5: ORIGINAL Compact Lattice (u=1110, LAT=1) ---
c
c BEFORE: Fills directly with u=1116 (particle lattice)
c
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -4:4  &
     1117 1117 1116 1116 1116 1117 1117 1117 1117
c 9 layers total (simplified from 31)
c
c --- AFTER: Fills with u=1118 (sub-compact layer) ---
c
c 91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -1:1  &
c      1117 1118 1117
c 3 layers total: matrix, sub-compact, matrix
c Each u=1118 contains 3 particle lattices
c Total particle lattices: 3 (vs 5 in original)
c
c --- Global Placement ---
c
91111 0  -97011  98005 -98051  fill=1110  imp:n=1  $ Compact
c
99999 0  97011 : -98005 : 98051  imp:n=0  $ Graveyard
c
c ========== SURFACE CARDS ==========
c
c --- TRISO Particle Surfaces (u=1114) ---
c
91111 so   0.0175  $ Kernel
91112 so   0.0280  $ Buffer
91113 so   0.0320  $ Coating
c
c --- Particle Lattice Bounding Surface (u=1116) ---
c
91117 rpp -0.05 0.05 -0.05 0.05 -0.05 0.05
c ±0.05 cm (simplified)
c
c --- Compact Lattice ORIGINAL Bounding Surface (u=1110) ---
c
91118 rpp -0.65 0.65 -0.65 0.65 -0.40 0.40
c Height: 9 layers × ~0.09 cm/layer ≈ 0.8 cm (±0.4)
c
c --- Sub-Compact Bounding Surface (u=1118) ---
c NEW surface for intermediate layer
c
91120 rpp -0.65 0.65 -0.65 0.65 -0.15 0.15
c Height: 3 layers × 0.1 cm = 0.3 cm (±0.15)
c
c --- Compact Lattice NEW Bounding Surface (u=1110) ---
c Adjusted for new hierarchy
c
c 91118 rpp -0.65 0.65 -0.65 0.65 -0.15 0.15
c Height: 3 layers (sub-compacts) × 0.3 cm = 0.9 cm
c Slightly taller than original due to 3×3 structure
c
c --- Global Placement Surfaces ---
c
97011 cz  0.70  $ Compact cylinder
98005 pz  0.0   $ Bottom
98051 pz  1.0   $ Top
c
c ========== DATA CARDS ==========
c
c --- Materials ---
c
m9111 92235.80c 1.0  $ Fuel kernel
m9112 6000.80c 1.0  $ Buffer carbon
m9113 6000.80c 1.0  $ Coating carbon
m9117 6000.80c 1.0  $ Graphite matrix
c
c --- Source ---
c
sdef pos 0 0 0.5  erg=2.0
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
c END OF MULTI-LEVEL HIERARCHY MODIFICATION EXAMPLE
c
c TO IMPLEMENT NEW HIERARCHY:
c
c Step 1: Define new universe u=1118 (already shown above)
c   - Creates 1×1×3 vertical sub-compact
c   - Fills with u=1116 (particle lattice) and u=1117 (matrix)
c
c Step 2: Modify parent universe u=1110
c   - Uncomment NEW compact lattice cell (line ~70)
c   - Comment out ORIGINAL compact lattice cell (line ~60)
c   - Changes fill from u=1116 to u=1118
c   - Reduces fill indices from -4:4 (9) to -1:1 (3)
c
c Step 3: Update bounding surface (if needed)
c   - Uncomment NEW surface 91118 (line ~115)
c   - Comment out ORIGINAL surface 91118 (line ~105)
c   - Adjusts height for new layer count
c
c VALIDATION CHECKS:
c - [x] New universe u=1118 defined (line ~55)
c - [ ] Parent fill array updated: -4:4 → -1:1
c - [ ] Fill array size matches: 3 elements
c - [ ] Bounding surface encloses new hierarchy
c - [ ] No orphaned universes (u=1116 now only in u=1118)
c - [ ] Plot geometry to verify nesting
c - [ ] Child universes u=1114, u=1115 unchanged
c
c HIERARCHY DIAGRAM:
c
c BEFORE:
c u=1110 (compact, 9 layers)
c   ├─ 1117 1117 1116 1116 1116 1117 1117 1117 1117
c   │         ↑ u=1116 (particle lattice)
c   │            └─ u=1114 (particle) + u=1115 (matrix)
c
c AFTER:
c u=1110 (compact, 3 layers)
c   ├─ 1117 1118 1117
c   │        ↑ u=1118 (NEW sub-compact)
c   │           └─ 1117 1116 1117
c   │                   ↑ u=1116 (particle lattice)
c   │                      └─ u=1114 (particle) + u=1115 (matrix)
c
c WHY ADD INTERMEDIATE LAYER?
c - Modularity: Easier to modify sub-compact properties
c - Grouping: Natural unit of 3 particle lattices
c - Flexibility: Can fill with different sub-compact types
c - Simplified indexing: 3 layers vs 9 layers
c ================================================================
