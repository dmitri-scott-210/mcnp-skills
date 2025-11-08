MCNP Fixed Source Templates - Point, Beam, Surface, and Volume Sources
c ========================================================================
c Cell Cards
c ========================================================================
1    1  -1.0    -1   IMP:N=1    $ Water sphere (target region)
2    0          -2 1 IMP:N=1    $ Void shell (for beam demonstration)
3    0           2   IMP:N=0    $ Graveyard

c ========================================================================
c Surface Cards
c ========================================================================
1    SO  10                     $ Inner sphere radius 10 cm
2    SO  50                     $ Outer sphere radius 50 cm

c ========================================================================
c Data Cards
c ========================================================================
MODE N
c ========================================================================
c TEMPLATE 1: Point Isotropic Source
c ========================================================================
c Uncomment this section for point isotropic neutron source at origin
c SDEF  POS=0 0 0  ERG=14.1  PAR=N
c ========================================================================
c TEMPLATE 2: Monodirectional Beam Along +Z Axis
c ========================================================================
c Uncomment this section for 1 MeV neutron beam along +Z
c SDEF  POS=0 0 -40  AXS=0 0 1  EXT=0  RAD=D1  ERG=1.0  PAR=N  DIR=D2
c SI1  0  5          $ Radial distribution (0 to 5 cm)
c SP1  -21 1         $ Uniform over area (built-in function -21)
c SI2  -1  1         $ Cosine bins for beam collimation
c SP2  0  0.5        $ Delta function at cos(θ)=1 (perfectly collimated)
c ========================================================================
c TEMPLATE 3: Surface Source on Sphere
c ========================================================================
c Uncomment this section for isotropic surface source on inner sphere
c SDEF  SUR=1  NRM=-1  ERG=2.0  PAR=N
c ========================================================================
c TEMPLATE 4: Volume Source in Sphere
c ========================================================================
c Uncomment this section for uniform volume source in inner sphere
c SDEF  CEL=1  ERG=D1  PAR=N
c SI1 L 0.5 1.0 2.0 5.0  $ Discrete energies (MeV)
c SP1   0.1 0.3 0.4 0.2  $ Probabilities (must sum to 1.0)
c ========================================================================
c TEMPLATE 5: Ring Source (Cylindrical)
c ========================================================================
c Uncomment this section for ring source at z=0, radius 5-10 cm
c SDEF  POS=0 0 0  AXS=0 0 1  RAD=D1  EXT=0  ERG=1.5  PAR=N
c SI1 H 5 10         $ Histogram: radii from 5 to 10 cm
c SP1   1            $ Uniform probability
c ========================================================================
c Common Data Cards
c ========================================================================
M1   1001.80c  2  8016.80c  1   $ Water (H2O)
F4:N 1                           $ Flux tally in water sphere
E4   0.1 0.5 1 2 5 10 20        $ Energy bins (MeV)
NPS  1e5                         $ Number of source particles
