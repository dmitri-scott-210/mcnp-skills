HTGR Physics Setup - WRONG EXAMPLE (Common Mistakes)
c Demonstrates MISSING thermal scattering - DO NOT USE!
c This file shows common physics errors found in real models
c
c ===================================================================
c CELL CARDS
c ===================================================================
c
1 1 -1.8   -1  imp:n=1  $ Fuel compact
2 2 -1.7    1 -2  imp:n=1  $ Graphite reflector
3 3 -5e-3   2 -3  imp:n=1  $ Helium coolant
4 0         3     imp:n=0  $ Void

c ===================================================================
c SURFACE CARDS
c ===================================================================
c
1 so  5.0
2 so  20.0
3 so  30.0

c ===================================================================
c DATA CARDS
c ===================================================================
c
c -------------------- MATERIALS --------------------
c
m1  $ Fuel compact - graphite
    6012.00c  0.9890
    6013.00c  0.0110
   92235.00c  0.001
c ❌ ERROR: Missing mt1 grph.18t
c    Impact: Wrong thermal spectrum, 1000-5000 pcm reactivity error!
c    Fix: Add "mt1 grph.18t" after this material card
c
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
c ❌ ERROR: Missing mt2 grph.18t
c    Impact: Wrong reflector physics!
c    Fix: Add "mt2 grph.18t" after this material card
c
m3  $ Helium coolant
    2004.00c  1.0
c (OK - no MT needed for helium)

c -------------------- PHYSICS SETTINGS --------------------
c
mode n
phys:n 20 0 0 J J J J J 1

c -------------------- SOURCE --------------------
c
kcode 10000 1.0 50 250
ksrc 0 0 0

c ===================================================================
c EXPECTED VALIDATOR OUTPUT:
c ===================================================================
c
c ❌ CRITICAL ERROR: Material m1 contains graphite but NO MT card
c    Type: MISSING_GRAPHITE_THERMAL_SCATTERING
c    Fix: Add "mt1 grph.18t"
c    Impact: Wrong thermal neutron spectrum, reactivity error 1000-5000 pcm
c    Reference: AGR1_Material_Card_Analysis.md
c
c ❌ CRITICAL ERROR: Material m2 contains graphite but NO MT card
c    Type: MISSING_GRAPHITE_THERMAL_SCATTERING
c    Fix: Add "mt2 grph.18t"
c    Impact: Wrong reflector physics, reactivity error
c
c Summary: 2 CRITICAL ERRORS - Input is INVALID for thermal reactor!
c
c ===================================================================
c HOW TO FIX:
c ===================================================================
c
c Add these two lines after the material cards:
c
c mt1 grph.18t  $ After m1 card
c mt2 grph.18t  $ After m2 card
c
c Then this input will be correct!
c
c ===================================================================
c IMPORTANT NOTE:
c ===================================================================
c
c MCNP will RUN this input without errors, but results will be WRONG!
c This is why systematic validation is CRITICAL before running.
c Missing MT cards are NOT optional - they are REQUIRED for accuracy.
c
c ===================================================================
c END OF INPUT
c ===================================================================
