Example 07: HTGR Compact with TRISO Particle Lattice - 4-Level Hierarchy
c =================================================================
c Description: High Temperature Gas Reactor (HTGR) fuel compact
c              TRISO particles in regular cubic lattice
c              Demonstrates 4-level hierarchy and double heterogeneity
c
c Hierarchy:
c   Level 1: TRISO particle 5-layer structure (U=1)
c   Level 2: TRISO particle lattice (U=10, 10×10×68 = 6800 particles)
c   Level 3: Fuel compact (U=20)
c   Real World: Compact in graphite block (U=0)
c
c Key Concepts:
c   - HTGR double heterogeneity (particle-level + compact-level)
c   - 5-layer TRISO particle (kernel/buffer/IPyC/SiC/OPyC)
c   - Regular lattice approximation for TRISO (vs stochastic)
c   - Volume specification per instance critical
c   - Computational necessity: millions of particles
c
c Author: MCNP Lattice Builder Skill
c Created: 2025-11-04
c Based on: AGR-1 experiment geometry and analysis
c =================================================================

c =================================================================
c BLOCK 1: Cell Cards
c =================================================================
c --- LEVEL 1: TRISO Particle Universe (5-layer coated particle) ---
c Universe 1: Single TRISO particle (850 μm diameter)
1    1  -10.8  -1         U=1  IMP:N=1  VOL=6.54e-6    $ Kernel (UO2)
2    2  -0.98   1  -2     U=1  IMP:N=1  VOL=1.47e-5    $ Buffer (porous C)
3    3  -1.85   2  -3     U=1  IMP:N=1  VOL=4.19e-6    $ IPyC (inner pyrocarbon)
4    4  -3.20   3  -4     U=1  IMP:N=1  VOL=5.76e-6    $ SiC (silicon carbide)
5    5  -1.86   4  -5     U=1  IMP:N=1  VOL=4.56e-6    $ OPyC (outer pyrocarbon)
6    6  -1.70   5         U=1  IMP:N=1  VOL=5.03e-4    $ Matrix (graphite filler)
c    Total TRISO + matrix volume: 5.38e-4 cm³ per lattice element
c
c --- LEVEL 2: TRISO Particle Lattice (Regular 3D Array) ---
c Universe 10: 10×10×68 lattice of TRISO particles
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
c    Lattice pitch: 0.105 cm (1.05 mm)
c    Total particles: 10×10×68 = 6,800 TRISO particles
c    Regular lattice approximation (vs stochastic: URAN card)
c    Justified by: Computational necessity (millions of particles in full compact)
c
c --- LEVEL 3: Fuel Compact Universe ---
c Universe 20: Cylindrical compact containing TRISO lattice
200  0  -200       FILL=10  U=20  IMP:N=1              $ TRISO lattice region
201  6  -1.70  200 -201  U=20  IMP:N=1  VOL=1.12      $ Matrix shell (no TRISO)
c    Compact: 1.245 cm radius × 7.14 cm height
c    Matrix density same as in TRISO (graphite)
c
c --- LEVEL 0: Real World - Compact in Graphite Block ---
1000 0  -1000  FILL=20  IMP:N=1                        $ Fuel compact
1001 7  -1.74  1000 -1001  IMP:N=1                    $ Graphite block
1002 8  -0.001  1001 -1002  IMP:N=1                   $ Helium coolant
1003 0  1002  IMP:N=0                                  $ Graveyard

c =================================================================
c BLOCK 2: Surface Cards
c =================================================================
c --- LEVEL 1: TRISO Particle Layer Surfaces (5 concentric spheres) ---
1    SO  0.01750                                       $ Kernel radius (350 μm dia)
2    SO  0.02750                                       $ Buffer outer (550 μm dia)
3    SO  0.03150                                       $ IPyC outer (630 μm dia)
4    SO  0.03500                                       $ SiC outer (700 μm dia)
5    SO  0.03850                                       $ OPyC outer (770 μm dia)
c    Total TRISO diameter: 770 μm (0.077 cm)
c    Lattice element: 1050 μm cube (contains TRISO + matrix)
c
c --- LEVEL 2: TRISO Lattice Element Boundaries ---
10   PX   0.0                                          $ -X
11   PX   1.05                                         $ +X (10 × 0.105 cm)
12   PY   0.0                                          $ -Y
13   PY   1.05                                         $ +Y (10 × 0.105 cm)
14   PZ   0.0                                          $ Bottom
15   PZ   7.14                                         $ Top (68 × 0.105 cm)
c    Lattice: 10×10×68 = 6,800 particles
c    Total lattice volume: 1.05 × 1.05 × 7.14 = 7.86 cm³
c    Fuel volume: 6,800 × 6.54e-6 = 0.0445 cm³ UO2
c
c --- LEVEL 3: Fuel Compact Surfaces ---
200  RCC  0 0 0  0 0 7.14  1.05                       $ Lattice cylinder (inscribed)
201  RCC  0 0 0  0 0 7.14  1.245                      $ Compact outer (12.45 mm R)
c    Compact volume: π × 1.245² × 7.14 = 34.75 cm³
c    Packing fraction: 7.86/34.75 = 22.6% (lattice region/total compact)
c
c --- LEVEL 0: Graphite Block and Coolant Channel ---
1000 RCC  0 0 -1  0 0 9.14  1.27                      $ Compact hole (with margin)
1001 RCC  0 0 -2  0 0 11.14  6.35                     $ Graphite block (hexagon approx)
1002 RCC  0 0 -3  0 0 13.14  7.0                      $ Coolant channel

c =================================================================
c BLOCK 3: Data Cards
c =================================================================
MODE  N
c --- Materials ---
c Material 1: UO2 Kernel (19.7% enriched, AGR-1 typical)
M1   92235.80c  0.197  92238.80c  0.803  8016.80c  2.0
TMP1  1.12e-7                                          $ 1300 K (peak fuel temp)
c Material 2: Buffer Layer (Porous Carbon, 50% TD)
M2   6000.80c  1.0
TMP2  1.12e-7                                          $ 1300 K
c Material 3: IPyC (Inner PyroCarbon)
M3   6000.80c  1.0
TMP3  1.12e-7
c Material 4: SiC (Silicon Carbide)
M4   14000.80c  1.0  6000.80c  1.0
TMP4  1.12e-7
c Material 5: OPyC (Outer PyroCarbon)
M5   6000.80c  1.0
TMP5  1.12e-7
c Material 6: Graphite Matrix in TRISO Lattice
M6   6000.80c  1.0
TMP6  1.12e-7
c Material 7: Graphite Block (IG-110, higher density)
M7   6000.80c  1.0
MT7  GRPH.10T                                          $ S(alpha,beta) for graphite
TMP7  1.03e-7                                          $ 1200 K (block temperature)
c Material 8: Helium Coolant (7 MPa)
M8   2004.80c  1.0                                     $ He-4
TMP8  9.48e-8                                          $ 1100 K (coolant temperature)
c --- Source Definition ---
KCODE  5000  1.0  25  125                             $ 5k/cycle, 125 cycles
KSRC   0 0 3.57                                       $ Initial source at compact center
c     Low histories per cycle due to large geometry (6800 particles!)
c --- Tallies ---
F4:N  (1 < 100 < 200)                                 $ Flux in all fuel kernels
c     Tally kernel (cell 1) in TRISO lattice (U=100) in compact (U=200)
F7:N  (1 < 100 < 200)                                 $ Fission energy in kernels
FM7   -1.0  1  -6  -8                                 $ Convert to Watts
c --- Problem Termination ---
c KCODE controls termination
PRINT

c =================================================================
c END OF INPUT
c =================================================================
c Notes:
c   1. HTGR Double Heterogeneity:
c      - First heterogeneity: TRISO particle (5 layers)
c      - Second heterogeneity: TRISO distribution in compact
c      - Each level requires special treatment for accurate physics
c
c   2. TRISO Particle Structure (5 layers):
c      Layer          Material    Density    Function
c      -----          --------    -------    --------
c      Kernel         UO2         10.8       Fuel
c      Buffer         C (porous)  0.98       Fission gas volume
c      IPyC           PyC         1.85       Pressure vessel
c      SiC            SiC         3.20       Fission product barrier
c      OPyC           PyC         1.86       Protects SiC
c
c   3. Regular Lattice vs Stochastic:
c      - REGULAR (this example): Deterministic, periodic arrangement
c        Advantages: Simple, computationally efficient
c        Disadvantages: Not physically accurate (TRISO randomly distributed)
c
c      - STOCHASTIC (URAN card): Random positions per history
c        Advantages: Physically accurate
c        Disadvantages: Extremely slow (regenerate geometry each history)
c
c      - TRADE-OFF: Regular lattice acceptable for most analyses
c        Errors typically <1-2% for bulk properties
c        Essential for large systems (millions of particles)
c
c   4. AGR-1 Context:
c      - AGR-1 experiment: 6 capsules, 72 compacts total
c      - Each compact: ~4,100 TRISO particles (actual, irregular)
c      - This example: 6,800 particles in regular 10×10×68 lattice
c      - Full AGR-1 model: 72 × 4,100 = ~295,000 particles!
c      - Computational necessity: Regular lattice essential
c
c   5. Lattice Pitch Selection:
c      - 1.05 mm pitch chosen to match packing fraction
c      - TRISO diameter: 0.77 mm
c      - Packing fraction: (4/3π×0.385³)/(1.05³) ≈ 20.7%
c      - Actual AGR-1: ~25% packing (denser, irregular)
c      - Adjust pitch to match desired packing
c
c   6. Volume Specifications CRITICAL:
c      - VOL in universe cell = SINGLE instance volume
c      - Kernel: 6.54e-6 cm³ per particle
c      - MCNP multiplies by 6,800 instances automatically
c      - Total kernel volume: 6,800 × 6.54e-6 = 0.0445 cm³
c
c   7. Temperature Distribution:
c      - Kernel peak: 1300 K (centerline)
c      - Graphite block: 1200 K (average)
c      - Helium coolant: 1100 K (outlet)
c      - In reality: Radial and axial temperature gradients
c      - Simplified here: Uniform per region
c
c   8. Expected Physics:
c      - k-effective: Dependent on enrichment and geometry
c      - 19.7% enrichment: k-eff > 1.0 (critical possible)
c      - Flux spectrum: Epithermal peak (HTGR characteristic)
c      - Graphite moderation: Soften spectrum, enhance fission
c      - SiC layer: Absorbs some thermal neutrons
c
c   9. Verification Steps:
c      mcnp6 inp=example_07.i ip
c      - Plot XY at Z=3.57 (mid-compact height)
c      - Zoom to single TRISO: Verify 5-layer structure
c      - Plot flux distribution: Should peak in compact center
c      - Check particle count: 10×10×68 = 6,800
c      - Verify matrix fills space between particles
c
c  10. Common Errors (HTGR-specific):
c      - Wrong volume specification (per-instance vs total)
c      - Missing matrix filler (space between TRISO)
c      - Infinite cells in TRISO universe (lost particles)
c      - Lattice pitch too small (particle overlap)
c      - Lattice pitch too large (unrealistic packing)
c
c  11. Extensions:
c      - Multiple compacts in stack (U=30 with vertical lattice)
c      - Flux-based grouping (separate universe per compact)
c      - Failed particles (different material in some TRISO)
c      - Burnable absorber particles (Er2O3 instead of UO2)
c      - Depletion calculation with BURN card
c      - Temperature feedback (link TMP to power)
c
c  12. Computational Considerations:
c      - 6,800 particles: Manageable for modern computers
c      - Geometry plotting: Slow due to hierarchy depth
c      - Particle tracking: Minimal overhead per universe level
c      - Run time: ~10× slower than equivalent homogeneous
c      - Memory: ~500 MB for this geometry
c
c  13. Literature-to-MCNP Translation:
c      Information from AGR-1 paper → MCNP implementation:
c      - TRISO dimensions (table) → Surface radii (cards 1-5)
c      - Layer densities (text) → Material densities (M1-M5)
c      - Compact dimensions (table) → RCC parameters (201)
c      - Particle count (~4100) → Lattice dimensions (10×10×68)
c      - Temperature profiles (figure) → TMP cards (approx)
c
c Verification:
c   - Plot XY at Z=3.57: See TRISO lattice cross-section
c   - Zoom to element [5,5,34]: See single TRISO 5-layer structure
c   - Plot flux: Peak should be in fuel kernels (layer 1)
c   - Count total fuel volume: 6800 × 6.54e-6 = 0.0445 cm³
c   - Check criticality: k-eff depends on enrichment (19.7% → supercritical)
c   - Verify no lost particles (TRISO fully contained in matrix)
c =================================================================
