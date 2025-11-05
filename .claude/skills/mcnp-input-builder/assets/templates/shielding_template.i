Multi-Layer Shielding Template
c =================================================================
c Template for shielding calculations with multiple layers
c Replace parameters marked with <...> with actual values
c =================================================================

c =================================================================
c Cell Cards
c =================================================================
1    0             -1              IMP:N=1          $ Source void
10   <mat1>  <d1>   1  -2          IMP:N=<imp1>    $ Shield layer 1
20   <mat2>  <d2>   2  -3          IMP:N=<imp2>    $ Shield layer 2
30   <mat3>  <d3>   3  -4          IMP:N=<imp3>    $ Shield layer 3
40   0              4  -5          IMP:N=1          $ Detector region
999  0              5              IMP:N=0          $ Graveyard

c =================================================================
c Surface Cards
c =================================================================
1    SO   <r_source>                              $ Source boundary
2    SO   <r_shield1>                             $ Shield 1 outer
3    SO   <r_shield2>                             $ Shield 2 outer
4    SO   <r_shield3>                             $ Shield 3 outer
5    SO   <r_detector>                            $ Detector outer

c =================================================================
c Data Cards
c =================================================================
MODE  N
c --- Shield Materials ---
c Layer 1: <material_name_1>
M<mat1>  <ZAID> <frac> <ZAID> <frac>
c Optional: MT<mat1>  <S(a,b)_table>
c
c Layer 2: <material_name_2>
M<mat2>  <ZAID> <frac> <ZAID> <frac>
c Optional: MT<mat2>  <S(a,b)_table>
c
c Layer 3: <material_name_3>
M<mat3>  <ZAID> <frac> <ZAID> <frac>
c
c Common shielding materials:
c   Concrete: 1001, 6000, 8016, 11023, 13027, 14000, 20000, 26000
c   Steel: 26000, 24000, 28000, 25055
c   Polyethylene: 1001, 6000 (needs POLY.01T S(a,b))
c   Lead: 82000
c   Water: 1001, 8016 (needs LWTR.01T S(a,b))
c --- Source Definition ---
SDEF  POS=0 0 0  ERG=<energy>
c Optional: Directional source
c SDEF  POS=0 0 0  ERG=<energy>  DIR=1  VEC=1 0 0
c --- Tallies ---
F4:N  10 20 30 40                                 $ Flux in all layers
E4    <E1> <E2> <E3> <E4>                        $ Energy bins
c Optional: F2:N  <surface#>                      $ Surface flux
c Optional: F6:N  10 20 30                        $ Heating in shields
c --- Variance Reduction (Importance) ---
c IMP:N  1 <imp1> <imp2> <imp3> 1 0              $ Cell-based importance
c Note: Increase importance through shield (e.g., 1 2 4 8)
c --- Problem Termination ---
NPS   <histories>
CTME  <minutes>                                   $ Recommended for deep penetration
PRINT

c =================================================================
c Template Instructions:
c =================================================================
c 1. Replace <mat#> with material numbers (1, 2, 3, etc.)
c 2. Replace <d#> with densities (g/cm³)
c 3. Replace radii <r_*> to define layer thicknesses
c 4. Replace <imp#> with importance values
c    - Start with 1 for all layers
c    - If poor statistics in detector: try 1, 2, 4, 8, ...
c 5. Define shield materials with realistic compositions
c 6. Add S(a,b) tables (MT cards) for light materials
c 7. Choose appropriate energy bins for source spectrum
c 8. Set NPS high for deep penetration (10^7 - 10^9)
c 9. Use CTME for long runs (120-480 minutes typical)
c =================================================================
