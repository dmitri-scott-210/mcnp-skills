Monodirectional Beam Source - Accelerator Simulation
c =================================================================
c Example demonstrating:
c   - Collimated beam along +Z axis
c   - Radial distribution (uniform over area)
c   - Directional distribution (perfectly collimated)
c   - Multi-distribution source (RAD=D1, DIR=D2)
c =================================================================
c Cell Cards
c =================================================================
1    1  -11.35  -1       IMP:N=1  VOL=15708   $ Lead shield cylinder
2    2  -1.0    -2  1    IMP:N=1  VOL=157080  $ Air region
3    0          -3  2    IMP:N=1  VOL=282743  $ Water detector
4    0           3       IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    RCC  0 0 -20  0 0 10  5                 $ Lead cylinder (R=5, H=10)
2    RCC  0 0 -10  0 0 40  10                $ Air cylinder (R=10, H=40)
3    RCC  0 0  30  0 0 20  10                $ Water detector (R=10, H=20)

c =================================================================
c Data Cards
c =================================================================
MODE N
c --- Source Definition ---
SDEF  POS=0 0 -25  AXS=0 0 1  EXT=0  RAD=D1  ERG=1.0  PAR=N  DIR=D2
SI1  0  3                                    $ Radial distribution (0 to 3 cm)
SP1  -21  1                                  $ Uniform over area (built-in function -21)
SI2  -1  1                                   $ Cosine bins for beam collimation
SP2  0  0.1                                  $ Nearly delta at cos(θ)=1 (tight beam)
c --- Material Definitions ---
M1   82000.80c  1.0                          $ Lead (Pb)
M2   7014.80c   0.79  8016.80c   0.21        $ Air (N2 + O2)
M3   1001.80c   2     8016.80c   1           $ Water (H2O)
MT3  H-H2O.40t                                $ Thermal scattering for water
c --- Tally Definitions ---
F4:N 3                                        $ Flux in water detector
E4   0.01  0.1  0.5  1.0  1.5               $ Energy bins (MeV)
F6:N 3                                        $ Heating in water detector
c --- Problem Termination ---
NPS  5e5
