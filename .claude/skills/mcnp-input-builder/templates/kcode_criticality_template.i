KCODE Criticality Template - Sphere Geometry
c =================================================================
c Template for simple criticality calculations
c Replace parameters marked with <...> with actual values
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    <mat#>  <density>  -1      IMP:N=1              $ Fissile region
2    0                   1      IMP:N=0              $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   <radius>                                   $ Sphere radius (cm)

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Fissile Material Definition ---
M<mat#>  <ZAID>  <fraction>  <ZAID>  <fraction>    $ Fissile material
c Common fissile isotopes:
c   92235 = U-235
c   92233 = U-233
c   94239 = Pu-239
c   94241 = Pu-241
c --- KCODE Parameters ---
KCODE  <Nsrc>  <k_initial>  <Nskip>  <Ntotal>
c      Nsrc      = histories per cycle (e.g., 10000)
c      k_initial = initial k-eff guess (e.g., 1.0)
c      Nskip     = inactive cycles to skip (e.g., 50)
c      Ntotal    = total cycles (e.g., 150, giving 100 active)
c --- Starting Source Position(s) ---
KSRC   0 0 0
c Optional: Add multiple starting positions for complex geometry
c KSRC   <x1> <y1> <z1>
c        <x2> <y2> <z2>
c        <x3> <y3> <z3>
c --- Optional: Tallies ---
c F4:N  1                                            $ Flux in fissile region
c F7:N  1                                            $ Fission energy deposition
c --- Termination ---
c (KCODE controls termination, no NPS card needed)
PRINT

c =================================================================
c Template Instructions:
c =================================================================
c 1. Replace <mat#> with material number (e.g., 1)
c 2. Replace <density> with fissile material density:
c    - U metal: ~19 g/cm³
c    - Pu metal: ~19.8 g/cm³
c    - UO2: ~10.4 g/cm³
c 3. Replace <radius> with critical or near-critical radius
c 4. Replace <ZAID> with fissile isotope (e.g., 92235 for U-235)
c 5. Replace KCODE parameters:
c    - Nsrc: 5000-20000 typical
c    - k_initial: 1.0 is good starting guess
c    - Nskip: 30-100 for convergence
c    - Ntotal: Nskip + 100-300 active cycles
c 6. Adjust KSRC positions to cover fissile region
c =================================================================
