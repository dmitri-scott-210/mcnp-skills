Hexagonal Assembly Rotation Example - 60° Rotation
c ================================================================
c This example demonstrates rotating a hexagonal fuel assembly
c by 60° about the vertical (Z) axis.
c
c Configuration:
c   - Hexagonal lattice (LAT=2)
c   - 7-ring pattern (127 fuel positions)
c   - RHP bounding surface with R-vector rotation
c   - Assembly height: 68 cm
c   - Hexagonal pitch: 2.771 cm (R = 1.6 cm)
c
c ORIGINAL orientation: R-vector along +Y (flat sides ∥ to X-Z)
c ROTATED orientation: R-vector rotated 60° CCW about Z
c
c 60° rotation is special: hexagons have 6-fold symmetry,
c so rotated assembly looks identical (if uniform fill)
c ================================================================
c
c ========== CELL CARDS ==========
c
c --- Fuel Pin (u=100) ---
c
100 1 -10.4 -101  u=100  $ UO2 fuel pellet
101 2 -6.5  101 -102  u=100  $ Zircaloy clad
102 3 -1.0  102  u=100  $ Water (outside pin)
c
c --- Control Rod Position (u=200) ---
c
200 4 -2.7  -201  u=200  $ B4C absorber
201 2 -6.5  201 -202  u=200  $ Stainless steel clad
202 3 -1.0  202  u=200  $ Water
c
c --- Void/Reflector (u=300) ---
c
300 3 -1.0  -301  u=300  $ Water reflector
c
c --- ORIGINAL Hexagonal Assembly (u=400, LAT=2) ---
c
400 0  -400  u=400 lat=2  fill=-3:3 -3:3 0:0  &
    300 300 300 300 300 300 300  &
     300 300 100 100 100 300 300  &
      300 100 100 200 100 100 300  &
       300 100 200 100 200 100 300  &
        300 100 100 200 100 100 300  &
         300 300 100 100 100 300 300  &
          300 300 300 300 300 300 300
c 7×7 hexagonal fill pattern
c Center row (4th): 7 elements
c 100 = fuel, 200 = control rod, 300 = reflector
c
c --- Global Cell (Assembly in Core) ---
c
500 0  -500  fill=400  imp:n=1  $ Assembly cell
c
c --- Graveyard ---
c
999 0  500  imp:n=0
c
c ========== SURFACE CARDS ==========
c
c --- Fuel Pin Surfaces (u=100) ---
c
101 cz  0.4750  $ Fuel pellet radius
102 cz  0.5500  $ Clad outer radius
c
c --- Control Rod Surfaces (u=200) ---
c
201 cz  0.6000  $ Absorber radius
202 cz  0.7000  $ Clad outer radius
c
c --- Reflector Surface (u=300) ---
c
301 rpp -0.5 0.5 -0.5 0.5 0.0 68.0  $ Small box (placeholder)
c
c --- ORIGINAL RHP Surface (R-vector along +Y) ---
c
400 rhp  0 0 0  0 0 68  0 1.6 0
c    Origin at (0,0,0)
c    Height vector: (0, 0, 68) → 68 cm along +Z
c    R-vector: (0, 1.6, 0) → 1.6 cm along +Y
c    Pitch = 1.6 × √3 = 2.771 cm
c    Orientation: Flat sides parallel to X-Z plane
c
c --- ROTATED RHP Surface (60° CCW about Z) ---
c
c R-vector calculation:
c   Original: (0, 1.6, 0)
c   Rotation matrix (60° about Z):
c     [cos(60°)  -sin(60°)  0] [0  ]   [0.5×0 - 0.866×1.6]   [-1.386]
c     [sin(60°)   cos(60°)  0] [1.6] = [0.866×0 + 0.5×1.6] = [ 0.8  ]
c     [0          0         1] [0  ]   [0                ]   [ 0    ]
c
c 400 rhp  0 0 0  0 0 68  -1.386 0.8 0
c     ↑ Origin unchanged
c              ↑ Height unchanged (rotation about Z)
c                          ↑ R-vector rotated 60°
c     Magnitude: |R| = sqrt(1.386² + 0.8²) = 1.6 ✓
c     Pitch preserved: 1.6 × √3 = 2.771 cm ✓
c
c --- ALTERNATIVE: Using TR Card ---
c
c *TR400  0 0 0  0 0 60  1  $ 60° rotation about Z
c 400  400  rhp  0 0 0  0 0 68  0 1.6 0
c      ↑ References TR400
c
c --- Assembly Bounding Surface (Global) ---
c
500 rhp  0 0 0  0 0 70  0 10 0  $ Large hex prism to enclose assembly
c
c ========== DATA CARDS ==========
c
c --- Materials ---
c
m1 92235.80c 0.05  92238.80c 0.95  $ UO2 fuel (5% enriched)
m2 40000.80c 1.0  $ Zircaloy
m3 1001.80c 2.0  8016.80c 1.0  $ Water (H2O)
m4 5010.80c 1.0  6000.80c 1.0  $ B4C (boron carbide)
c
c --- Source (uniform in assembly) ---
c
sdef pos 0 0 34  erg=2.0
c
c --- Tallies ---
c
f4:n 100  $ Flux in fuel
c
c --- Problem Parameters ---
c
mode n
nps 1000
c
c ================================================================
c END OF HEXAGONAL ASSEMBLY ROTATION EXAMPLE
c
c TO IMPLEMENT ROTATION:
c Method 1 (Direct R-vector edit):
c   1. Uncomment ROTATED RHP surface (line with -1.386 0.8 0)
c   2. Comment out ORIGINAL RHP surface
c
c Method 2 (TR card):
c   1. Uncomment *TR400 line
c   2. Uncomment ALTERNATIVE RHP line with TR reference
c   3. Comment out ORIGINAL RHP surface
c
c VALIDATION CHECKS:
c - R-vector magnitude preserved: |R| = 1.6 cm
c - Pitch unchanged: 2.771 cm
c - Height unchanged: 68 cm
c - Plot geometry to visualize rotation
c - For 60° rotation: assembly looks identical (6-fold symmetry)
c
c NOTES:
c - Hexagons have 60° rotational symmetry
c - Rotating 60° × N (N=1,2,3,4,5,6) gives same orientation
c - Rotating 30° changes flat-to-flat to point-to-point
c - Fill pattern orientation should match rotated geometry
c ================================================================
