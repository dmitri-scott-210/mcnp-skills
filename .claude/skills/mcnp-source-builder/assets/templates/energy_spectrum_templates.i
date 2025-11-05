MCNP Energy Spectrum Templates - Watt, Maxwell, Discrete, and Histogram
c ========================================================================
c Cell Cards
c ========================================================================
1    1  -1.0    -1   IMP:N=1    $ Water sphere (detector region)
2    0           1   IMP:N=0    $ Graveyard

c ========================================================================
c Surface Cards
c ========================================================================
1    SO  30                     $ Sphere radius 30 cm

c ========================================================================
c Data Cards
c ========================================================================
MODE N
c ========================================================================
c TEMPLATE 1: Watt Fission Spectrum (U-235 Thermal Fission)
c ========================================================================
c Watt spectrum: p(E) = exp(-E/a) * sinh(sqrt(b*E))
c Default parameters for U-235: a=0.988 MeV, b=2.249 MeV^-1
c Uncomment this section:
c SDEF  POS=0 0 0  ERG=D1  PAR=N
c SI1  -3          $ Built-in Watt spectrum (function -3)
c SP1   0.988  2.249   $ Parameters: a, b
c ========================================================================
c TEMPLATE 2: Maxwellian Spectrum
c ========================================================================
c Maxwellian spectrum: p(E) = sqrt(E) * exp(-E/T)
c Temperature T=1.29 MeV (typical for fast reactor)
c Uncomment this section:
c SDEF  POS=0 0 0  ERG=D2  PAR=N
c SI2  -30         $ Built-in Maxwellian spectrum (function -30)
c SP2   1.29       $ Temperature parameter T (MeV)
c ========================================================================
c TEMPLATE 3: Discrete Gamma Lines (Co-60)
c ========================================================================
c Two gamma rays: 1.173 MeV and 1.332 MeV with equal intensity
c Uncomment this section and change MODE to MODE P for photons:
c SDEF  POS=0 0 0  ERG=D3  PAR=P
c SI3 L 1.173  1.332   $ List of discrete energies (MeV)
c SP3   1.0    1.0     $ Relative intensities (will be normalized)
c ========================================================================
c TEMPLATE 4: Discrete Gamma Lines (Cs-137)
c ========================================================================
c Primary gamma: 0.662 MeV
c Uncomment this section and change MODE to MODE P:
c SDEF  POS=0 0 0  ERG=0.662  PAR=P
c ========================================================================
c TEMPLATE 5: Histogram Energy Spectrum
c ========================================================================
c Custom histogram with 4 energy bins
c Uncomment this section:
c SDEF  POS=0 0 0  ERG=D4  PAR=N
c SI4 H 0.1  0.5  1.0  2.0  5.0   $ Energy bin boundaries (MeV)
c SP4     0.1  0.2  0.4  0.3      $ Probabilities (4 bins, must sum to 1.0)
c ========================================================================
c TEMPLATE 6: Arbitrary Tabular Spectrum
c ========================================================================
c Linear interpolation between specified (E, P(E)) points
c Uncomment this section:
c SDEF  POS=0 0 0  ERG=D5  PAR=N
c SI5 A 0.5  1.0  2.0  5.0  10.0   $ Energy points (MeV)
c SP5     0.1  0.4  0.8  0.5  0.1  $ Probability density at each point
c ========================================================================
c TEMPLATE 7: Line Spectrum with Biasing (SB card)
c ========================================================================
c Discrete spectrum with importance biasing for variance reduction
c Uncomment this section:
c SDEF  POS=0 0 0  ERG=D6  PAR=N
c SI6 L 0.5  1.0  2.0  5.0     $ Energies (MeV)
c SP6   0.1  0.3  0.4  0.2     $ Source probabilities
c SB6   1.0  2.0  5.0  10.0    $ Biasing factors (higher = sample more often)
c ========================================================================
c TEMPLATE 8: Gaussian Energy Spectrum
c ========================================================================
c Gaussian: p(E) = exp(-(E-E0)^2 / (2*sigma^2))
c Mean E0=2.5 MeV, sigma=0.2 MeV
c Uncomment this section:
c SDEF  POS=0 0 0  ERG=D7  PAR=N
c SI7  -41         $ Built-in Gaussian (function -41)
c SP7   2.5  0.2   $ Parameters: E0, sigma
c ========================================================================
c Common Data Cards
c ========================================================================
M1   1001.80c  2  8016.80c  1   $ Water (H2O)
F4:N 1                           $ Flux tally in sphere
E4   0.01  0.1  0.5  1  2  5  10  20   $ Energy bins (MeV)
F8:P 1                           $ Pulse-height tally (for photons)
E8   0 0.1 0.5 1.0 1.5           $ Energy deposition bins (MeV)
NPS  1e5                         $ Number of source particles
