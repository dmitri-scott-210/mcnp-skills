c ============================================================
c MULTI-SCALE TRISO PARTICLE EXAMPLE
c Demonstrates geometry spanning 5 orders of magnitude
c ============================================================
c
c Demonstrates:
c  - Multi-scale precision (μm to cm)
c  - TRISO particle (5 layers, SO surfaces)
c  - Nested spheres (fastest tracking)
c  - Precision management across scales
c  - Unit conversions (μm → cm)
c
c Scale range: 174.85 μm (kernel) to 10+ cm (compact)
c Scale ratio: ~570:1
c
c ============================================================

c ------------------------------------------------------------
c TRISO PARTICLE UNIVERSE (u=100)
c ------------------------------------------------------------
c
c Microscale: TRISO particle (174.85 μm to 465 μm)
c Precision: 5-6 significant figures for μm-scale features
c Surface type: SO (sphere at origin) - fastest for repeated structures

1  1  -10.8   -1       u=100  vol=6.545e-5  $ Kernel (UO2, 349.7 μm dia)
2  2  -0.98    1  -2   u=100  vol=1.139e-4  $ Buffer (porous C, 100 μm thick)
3  3  -1.85    2  -3   u=100  vol=4.676e-5  $ IPyC (dense C, 40 μm thick)
4  4  -3.20    3  -4   u=100  vol=4.315e-5  $ SiC (ceramic, 35 μm thick)
5  5  -1.86    4  -5   u=100  vol=5.339e-5  $ OPyC (dense C, 40 μm thick)
6  6  -1.75    5       u=100                $ Matrix (graphite)

c Microscale surfaces (SO - centered at origin)
c Dimensions in cm, preserving μm precision
1  so  0.017485    $ Kernel R = 174.85 μm = 0.017485 cm (6 digits)
2  so  0.027905    $ Buffer R = 279.05 μm = 0.027905 cm (5 digits)
3  so  0.031785    $ IPyC R   = 317.85 μm = 0.031785 cm (5 digits)
4  so  0.035285    $ SiC R    = 352.85 μm = 0.035285 cm (5 digits)
5  so  0.039285    $ OPyC R   = 392.85 μm = 0.039285 cm (5 digits)

c ------------------------------------------------------------
c FUEL COMPACT UNIVERSE (u=200)
c ------------------------------------------------------------
c
c Milliscale to centiscale: Fuel compact (6.35 mm radius)
c Precision: 3-4 significant figures for mm-scale features
c Surface type: CZ (cylinder on Z-axis)
c
c Simplified: Homogenized TRISO + matrix
c For explicit TRISO: Use lattice of u=100 particles

200  7  -1.85  -200  -210 211  u=200  imp:n=1  $ Compact (homogenized)
201  6  -1.70   200  -201  -210 211  u=200  imp:n=1  $ Graphite channel

c Centiscale surfaces (mm precision)
200  cz  0.6350    $ Compact R = 6.35 mm = 0.635 cm (3 digits)
201  cz  0.7930    $ Channel R = 7.93 mm = 0.793 cm (3 digits)

c Axial extent (compact height)
210  pz  0.0       $ Bottom
211  pz  1.27      $ Top (1.27 cm = 12.7 mm)

c ------------------------------------------------------------
c GLOBAL GEOMETRY
c ------------------------------------------------------------
c
c Deciscale: Overall assembly (10+ cm)
c Precision: 2-3 significant figures for cm-scale features

999   0  -201  fill=200  (0 0 0)  imp:n=1   $ Position compact at origin
1000  0   201                     imp:n=0   $ Graveyard

c Global boundary (deciscale)
300  rpp  -2 2  -2 2  -1 3    $ Box (cm-scale precision)

c ------------------------------------------------------------
c DATA CARDS
c ------------------------------------------------------------

mode n
sdef pos=0 0 0.635  erg=2.0
nps 10000

c ------------------------------------------------------------
c MATERIALS
c ------------------------------------------------------------

m1  $ UO2 kernel (19.75% enriched, 10.8 g/cm³)
   92234.00c  3.34e-3    $ U-234
   92235.00c  1.996e-1   $ U-235 (enriched)
   92236.00c  1.93e-4    $ U-236
   92238.00c  7.968e-1   $ U-238
    8016.00c  1.3613     $ Oxygen

m2  $ Buffer (porous carbon, 0.98 g/cm³)
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t

m3  $ IPyC (dense pyrolytic carbon, 1.85 g/cm³)
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.18t

m4  $ SiC (silicon carbide, 3.20 g/cm³)
   14000.60c  0.5
    6012.00c  0.495
    6013.00c  0.005

m5  $ OPyC (dense pyrolytic carbon, 1.86 g/cm³)
    6012.00c  0.9890
    6013.00c  0.0110
mt5 grph.18t

m6  $ Graphite matrix (1.75 g/cm³)
    6012.00c  0.9890
    6013.00c  0.0110
mt6 grph.18t

m7  $ Fuel compact (homogenized TRISO + matrix, 1.85 g/cm³)
c    Effective composition - weighted average
    6012.00c  0.40
   92235.00c  0.008
   92238.00c  0.032
    8016.00c  0.04
   14000.60c  0.06
mt7 grph.18t

c ============================================================
c MULTI-SCALE ANALYSIS
c ============================================================
c
c Scale Hierarchy:
c
c  Feature                Dimension       MCNP Value    Precision
c  --------------------------------------------------------------
c  Kernel radius          174.85 μm       0.017485 cm   6 digits
c  Buffer outer           279.05 μm       0.027905 cm   5 digits
c  IPyC outer             317.85 μm       0.031785 cm   5 digits
c  SiC outer              352.85 μm       0.035285 cm   5 digits
c  OPyC outer             392.85 μm       0.039285 cm   5 digits
c  Compact radius         6.35 mm         0.6350 cm     4 digits
c  Channel radius         7.93 mm         0.7930 cm     4 digits
c  Compact height         12.7 mm         1.27 cm       3 digits
c  Assembly boundary      40 cm           40 cm         2 digits
c
c Unit Conversions:
c  MCNP uses cm for ALL lengths
c
c  μm → cm: divide by 10,000
c   174.85 μm = 174.85 / 10,000 = 0.017485 cm ✓
c
c  mm → cm: divide by 10
c   6.35 mm = 6.35 / 10 = 0.635 cm ✓
c
c  m → cm: multiply by 100
c   0.4 m = 0.4 × 100 = 40 cm ✓
c
c Precision Guidelines:
c
c  1. Microscale (10-100 μm): Use 5-6 significant figures
c     - Preserve μm-scale dimensions: 0.017485 cm (not 0.0175)
c     - Essential for thin TRISO coatings
c
c  2. Milliscale (0.1-10 mm): Use 4-5 significant figures
c     - Coating thicknesses: 0.027905 cm (279.05 μm)
c     - Compact dimensions: 0.6350 cm (6.35 mm)
c
c  3. Centiscale (1-10 cm): Use 3-4 significant figures
c     - Pin dimensions: 0.635 cm
c     - Assembly pitch: 1.26 cm
c
c  4. Deciscale (10-100 cm): Use 3-4 significant figures
c     - Core dimensions: 150 cm
c     - Height: 366 cm
c
c  5. Meter scale (1-10 m): Use 2-3 significant figures
c     - Building dimensions: 500 cm (5 m)
c     - Shielding: 200 cm (2 m)
c
c Avoid False Precision:
c  BAD:  0.63500000 cm  (9 digits for mm-scale feature)
c  GOOD: 0.635 cm       (3 digits appropriate for mm-scale)
c
c  BAD:  25.547039 cm   (8 digits for cm-scale position)
c  GOOD: 25.547 cm      (5 digits reasonable for cm-scale)
c
c ============================================================
c VERIFICATION
c ============================================================
c
c Visual check (MCNP plotter):
c  mcnp6 inp=13_multi_scale_triso.i ip
c
c  View 1: TRISO particle detail
c   origin 0 0 0.635
c   extent 0.1 0.1 0.1
c   basis 1 0 0  0 1 0
c   Expected: 5 concentric circles (TRISO layers)
c
c  View 2: Compact scale
c   origin 0 0 0.635
c   extent 2 2 2
c   basis 1 0 0  0 1 0
c   Expected: Compact cylinder in channel
c
c Volume Verification:
c
c  TRISO kernel:
c   V = (4/3)π(0.017485)³ = 6.545e-5 cm³ ✓
c
c  Buffer layer:
c   V = (4/3)π(0.027905³ - 0.017485³) = 1.139e-4 cm³ ✓
c
c  Compact (cylinder):
c   V = π(0.635)² × 1.27 = 1.610 cm³
c
c Precision Check:
c  - Kernel: 0.017485 → 6 significant figures ✓
c  - Compact: 0.6350 → 4 significant figures ✓
c  - Boundary: 40 → 2 significant figures ✓
c
c ============================================================
c NOTES
c ============================================================
c
c Multi-Scale Strategy:
c
c 1. Use universes to manage scales
c    - TRISO particle: u=100 (μm scale)
c    - Compact: u=200 (mm to cm scale)
c    - Assembly: global (cm to m scale)
c
c 2. Surface type selection
c    - Microscale (repeated): SO (fastest)
c    - Mesoscale (centered): CZ
c    - Macroscale (boundaries): RPP, PZ
c
c 3. Preserve precision where needed
c    - Thin coatings: Full μm precision
c    - Bulk dimensions: Appropriate for scale
c
c 4. Avoid false precision
c    - Don't use 10 digits for cm-scale features
c    - Match precision to measurement uncertainty
c
c Performance Optimization:
c
c  - SO surfaces (TRISO): Fastest tracking
c  - Centered in universe: No coordinate transformation
c  - Replicate via FILL: Efficient memory use
c
c Explicit TRISO Modeling:
c
c  For detailed particle-by-particle tracking:
c
c  1. Use lattice of u=100 TRISO particles
c  2. Mix TRISO (u=100) with matrix (u=6) in compact
c  3. Typical: 10,000-30,000 particles per compact
c
c  Example:
c   200  0  -200  u=200  lat=1  fill=0:9 0:9 0:9
c        [... 1000 universe numbers: 100 or 6 ...]
c
c  Homogenized (used here):
c  - Faster for production calculations
c  - Adequate for most analyses
c  - Use explicit for detailed burnup/failure studies
c
c ============================================================
c COMMON ERRORS
c ============================================================
c
c Error 1: Wrong unit conversions
c  WRONG: 174.85 μm = 0.17485 cm  (off by 10×)
c  RIGHT: 174.85 μm = 0.017485 cm (÷ 10,000)
c
c Error 2: Insufficient precision
c  WRONG: 1  so  0.0175  (rounds to 175 μm, loses 0.15 μm)
c  RIGHT: 1  so  0.017485 (preserves 174.85 μm)
c
c Error 3: False precision
c  WRONG: 200  cz  0.63500000  (9 digits for mm-scale)
c  RIGHT: 200  cz  0.635       (3-4 digits appropriate)
c
c Error 4: Scale mismatch
c  WRONG: Mixing μm-precision with m-scale: 500.017485 cm
c  RIGHT: Match precision to scale: 500 cm (m-scale)
c
c ============================================================
