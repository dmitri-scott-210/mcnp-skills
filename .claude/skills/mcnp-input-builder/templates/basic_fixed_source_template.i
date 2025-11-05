Basic Fixed-Source Template - Sphere Geometry
c =================================================================
c Template for simple fixed-source problems
c Replace parameters marked with <...> with actual values
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    <mat#>  <density>  -1      IMP:N=1  VOL=<volume>  $ Active region
2    0                   1      IMP:N=0                $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   <radius>                                     $ Sphere radius (cm)

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Material Definition ---
M<mat#>  <ZAID>  <fraction>  <ZAID>  <fraction>      $ Material composition
c Optional: MT<mat#>  <S(a,b)_table>                  $ Thermal scattering
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=<energy>                         $ Point source, energy (MeV)
c Optional: SDEF  POS=0 0 0  ERG=D1
c           SI1   <E1> <E2> <E3>                      $ Discrete energies
c           SP1   <P1> <P2> <P3>                      $ Probabilities
c --- Tally Definition ---
F4:N  1                                               $ Volume-averaged flux
E4    <E1> <E2> <E3> <E4>                            $ Energy bins (MeV)
c Optional: F2:N  1                                   $ Surface flux
c Optional: F5:N  <x> <y> <z> <R>                    $ Point detector
c --- Problem Termination ---
NPS   <histories>                                     $ Number of histories
c Optional: CTME  <minutes>                           $ Time limit
PRINT

c =================================================================
c Template Instructions:
c =================================================================
c 1. Replace <mat#> with material number (e.g., 1)
c 2. Replace <density> with density:
c    - Positive: g/cm³ (e.g., 1.0 for water)
c    - Negative: atoms/(barn·cm) (e.g., -0.1)
c 3. Replace <radius> with sphere radius in cm
c 4. Replace <ZAID> with isotope identifiers (e.g., 1001, 8016)
c 5. Replace <fraction> with atomic fractions
c 6. Replace <energy> with source energy in MeV
c 7. Replace <histories> with number of particles (e.g., 1000000)
c 8. Delete or uncomment optional cards as needed
c =================================================================
