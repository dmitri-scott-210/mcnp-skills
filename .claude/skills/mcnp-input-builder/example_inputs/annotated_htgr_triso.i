c ========================================
c HTGR TRISO PARTICLE MODEL - ANNOTATED EXAMPLE
c ========================================
c
c Description: Single TRISO-coated fuel particle in graphite matrix
c Purpose: Demonstrate hierarchical numbering, universe encoding, and lattice structure
c
c Author: MCNP Skills Framework
c Date: 2024-11-08
c
c GEOMETRY DESCRIPTION:
c   - UCO fuel kernel (350 μm diameter)
c   - Buffer layer (porous carbon, 100 μm thick)
c   - IPyC layer (inner pyrolytic carbon, 40 μm thick)
c   - SiC layer (silicon carbide, 35 μm thick)
c   - OPyC layer (outer pyrolytic carbon, 40 μm thick)
c   - Graphite matrix surrounding particle
c   - Total particle diameter: ~785 μm
c
c NUMBERING SCHEME:
c   Cells:     111XX (Position 1-1-1, sequence XX)
c              Position encoding: Compact 1, Row 1, Column 1
c   Surfaces:  111XX (correlated with cells)
c   Materials: 11X (position-based) or 90X (shared coatings)
c   Universes: 111W where W = component type
c              W=4: TRISO particle, W=5: Matrix filler
c
c UNIVERSE COMPONENT TYPES:
c   1114 = TRISO particle (5-layer structure)
c   1115 = Matrix filler (no particle)
c
c UNITS:
c   Lengths: cm (convert from μm: 1 μm = 1e-4 cm)
c   Densities: g/cm³ (negative for mass fractions)
c   Energies: MeV
c
c MATERIALS:
c   m111:  UCO kernel, 19.96% enriched, 10.924 g/cm³
c   m901:  Buffer carbon, porous, 1.10 g/cm³
c   m902:  IPyC, dense carbon, 1.904 g/cm³
c   m903:  SiC, silicon carbide, 3.205 g/cm³
c   m904:  OPyC, dense carbon, 1.911 g/cm³
c   m905:  Matrix, graphite, 1.73 g/cm³
c
c REFERENCE:
c   - AGR-1 HTGR experiment (simplified single particle)
c   - TRISO fuel specification INL/EXT-10-17686
c
c ========================================

c ========================================
c CELL BLOCK
c ========================================
c
c TRISO PARTICLE UNIVERSE (u=1114)
c   Five concentric spherical layers
c
11101  111  -10.924  -11101              u=1114  vol=2.240e-05  $ Kernel (UCO)
11102  901   -1.100  11101 -11102       u=1114  vol=1.507e-04  $ Buffer (porous C)
11103  902   -1.904  11102 -11103       u=1114  vol=8.530e-05  $ IPyC (dense C)
11104  903   -3.205  11103 -11104       u=1114  vol=6.240e-05  $ SiC (barrier)
11105  904   -1.911  11104 -11105       u=1114  vol=7.710e-05  $ OPyC (dense C)
11106  905   -1.730  11105               u=1114                 $ Matrix around particle
c
c MATRIX FILLER UNIVERSE (u=1115)
c   Pure graphite matrix (no particle)
c
11107  905   -1.730  -11107              u=1115                 $ Matrix only
c
c GLOBAL UNIVERSE (u=0)
c   Contains one TRISO particle for demonstration
c
1  0  -1  fill=1114  imp:n=1  $ Global cell filled with TRISO particle
c
c OUTSIDE WORLD
c
999  0  1  imp:n=0  $ Graveyard

c ========================================
c SURFACE BLOCK
c ========================================
c
c TRISO PARTICLE SURFACES
c   Concentric spheres (SO = sphere at origin)
c   Dimensions from AGR-1 specification (converted μm → cm)
c
11101  so  0.017485  $ Kernel radius (174.85 μm = 0.017485 cm)
11102  so  0.027905  $ Buffer outer (279.05 μm, +100 μm thickness)
11103  so  0.031785  $ IPyC outer (317.85 μm, +40 μm thickness)
11104  so  0.035375  $ SiC outer (353.75 μm, +35 μm thickness)
11105  so  0.039305  $ OPyC outer (393.05 μm, +40 μm thickness)
11107  so  0.050000  $ Matrix element boundary (500 μm half-width)
c
c GLOBAL BOUNDARY
c
1  so  0.1  $ Outer boundary (1 mm sphere for demonstration)

c ========================================
c DATA BLOCK
c ========================================
c
MODE N
c
c --- MATERIALS ---
c
c Material m111: UCO kernel, 19.96% enriched, density = 10.924 g/cm³
c Formula: UC₀.₃₂O₁.₃₆ (uranium carbide-oxide)
c Temperature: 900K (fuel operating temperature)
m111
   92234.00c  3.34179e-03  $ U-234 (0.334% of uranium)
   92235.00c  1.99636e-01  $ U-235 (19.96% enrichment, fissile)
   92236.00c  1.93132e-04  $ U-236 (trace)
   92238.00c  7.96829e-01  $ U-238 (balance, fertile)
    6012.00c  0.3217217    $ C-12 (carbide component, 98.9% of C)
    6013.00c  0.0035783    $ C-13 (natural abundance 1.1%)
    8016.00c  1.3613       $ O-16 (oxide component)
c Note: Positive fractions = atom fractions
c
c Material m901: Buffer layer, porous carbon, density = 1.10 g/cm³
c Purpose: Accommodate fission gas release, low density
m901
    6012.00c  0.9890  $ C-12 (98.9%)
    6013.00c  0.0110  $ C-13 (1.1%, natural)
c
c Material m902: IPyC, dense pyrolytic carbon, density = 1.904 g/cm³
c Purpose: Inner coating, gas retention
m902
    6012.00c  0.9890  $ C-12
    6013.00c  0.0110  $ C-13
mt902  grph.18t  $ Graphite S(α,β) at 600K (critical for thermal neutrons!)
c
c Material m903: SiC, silicon carbide, density = 3.205 g/cm³
c Purpose: Primary fission product barrier (critical layer)
m903
   14028.00c  0.4610  $ Si-28 (92.2% of natural Si)
   14029.00c  0.0235  $ Si-29 (4.7%)
   14030.00c  0.0155  $ Si-30 (3.1%)
    6012.00c  0.4950  $ C-12 (stoichiometric SiC, 98.9% of C)
    6013.00c  0.0055  $ C-13 (1.1%)
mt903  grph.18t  $ S(α,β) for carbon component
c
c Material m904: OPyC, outer pyrolytic carbon, density = 1.911 g/cm³
c Purpose: Outer coating, structural support
m904
    6012.00c  0.9890  $ C-12
    6013.00c  0.0110  $ C-13
mt904  grph.18t  $ Graphite S(α,β) at 600K
c
c Material m905: Matrix graphite, density = 1.73 g/cm³
c Purpose: Structural matrix, moderator
m905
    6012.00c  0.9890  $ C-12
    6013.00c  0.0110  $ C-13
mt905  grph.18t  $ Graphite S(α,β) at 600K
c
c --- SOURCE ---
c
c Isotropic point source at origin (center of kernel)
c Watt fission spectrum (U-235 thermal fission)
sdef  pos=0 0 0  erg=d1  par=n
sp1   -3  0.8  2.5  $ Watt spectrum parameters
c
c --- TALLIES ---
c
c Tally 4: Cell flux in kernel (for fission rate)
f4:n   11101        $ Kernel cell
e4     0.01 0.1 1 10  $ Thermal to fast neutrons
fc4    UCO kernel neutron flux
c
c Tally 14: Cell flux in SiC layer (for damage)
f14:n  11104        $ SiC barrier layer
e14    0.01 0.1 1 10
fc14   SiC barrier layer flux
c
c Tally 24: Cell flux in matrix (for moderation)
f24:n  11106        $ Graphite matrix
e24    0.01 0.1 1 10
fc24   Graphite matrix flux
c
c --- TERMINATION ---
c
nps   10000000  $ 10 million histories (high stats for small kernel)

