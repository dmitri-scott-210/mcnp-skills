Source-Detector Template with Point Detector
c =================================================================
c Template for source-detector problems using F5 point detector
c Replace parameters marked with <...> with actual values
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    <mat#>  <dens>  -1  2       IMP:N=1  VOL=<vol>  $ Medium region
2    0               1  -3       IMP:N=1              $ Detector void
999  0               3           IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   <r_inner>                               $ Inner boundary
2    CZ   <r_cylinder>                            $ Cylindrical boundary (optional)
3    SO   <r_outer>                               $ Outer boundary

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Medium Material (optional) ---
c For void geometry: Comment out material and set mat#=0 in cell 1
M<mat#>  <ZAID> <frac> <ZAID> <frac>             $ Medium material
c Optional: MT<mat#>  <S(a,b)_table>
c --- Source Definition ---
SDEF  POS=<x> <y> <z>  ERG=<energy>
c Optional: Directional source toward detector
c SDEF  POS=<x> <y> <z>  ERG=<energy>  DIR=1  VEC=<ux> <uy> <uz>
c Optional: Energy distribution
c SDEF  POS=<x> <y> <z>  ERG=D1
c SI1   H  <E1> <E2> <E3>                         $ Energy histogram
c SP1   D  <P1> <P2> <P3>                         $ Probabilities
c --- Point Detector Tally ---
F5:N  <x_det> <y_det> <z_det>  <R_exclusion>
c     Detector location: (<x_det>, <y_det>, <z_det>)
c     Exclusion radius: <R_exclusion> (typically 0.1-1.0 cm)
c     Particles within R_exclusion are excluded from tally
c
E5    <E1> <E2> <E3> <E4>                        $ Energy bins
c
c Optional: Add F4 cell flux for comparison
c F4:N  1                                         $ Cell flux in medium
c E4    <E1> <E2> <E3> <E4>
c
c Optional: Ring detectors for angular dependence
c F15:N  <x> <y> <z>  <R>                        $ Ring detector 1
c F25:N  <x> <y> <z>  <R>                        $ Ring detector 2
c --- Problem Termination ---
NPS   <histories>
PRINT

c =================================================================
c Template Instructions:
c =================================================================
c 1. Define geometry:
c    - For void: Set mat#=0 in cell 1, comment out M card
c    - For scattering medium: Define material with M card
c 2. Source position (<x>, <y>, <z>):
c    - Typical: (0, 0, 0) at origin
c    - Ensure inside active geometry (IMP>0)
c 3. Detector position (<x_det>, <y_det>, <z_det>):
c    - Place at measurement location
c    - Common: (distance, 0, 0) along x-axis
c 4. Exclusion radius <R_exclusion>:
c    - Prevents overestimation from nearby particles
c    - Typical: 0.5-1.0 cm for point sources
c    - Smaller for distant detectors (0.1-0.5 cm)
c 5. Energy bins:
c    - Focus around source energy
c    - Add bins for scattered energies if needed
c 6. Number of histories:
c    - F5 converges faster than F4
c    - 10^5 - 10^6 typical for point detectors
c    - 10^6 - 10^7 for scattering media
c =================================================================
