HTGR Physics Setup - CORRECT EXAMPLE
c Demonstrates proper thermal scattering for HTGR at 600K
c This is a REFERENCE example showing correct physics setup
c
c ===================================================================
c CELL CARDS
c ===================================================================
c
1 1 -1.8   -1  imp:n=1  $ Fuel compact (graphite fuel matrix)
2 2 -1.7    1 -2  imp:n=1  $ Graphite reflector
3 3 -5e-3   2 -3  imp:n=1  $ Helium coolant
4 0         3     imp:n=0  $ Void

c ===================================================================
c SURFACE CARDS
c ===================================================================
c
1 so  5.0   $ Fuel compact outer radius
2 so  20.0  $ Reflector outer radius
3 so  30.0  $ Problem boundary

c ===================================================================
c DATA CARDS
c ===================================================================
c
c -------------------- MATERIALS --------------------
c
m1  $ Fuel compact - graphite fuel matrix
    6012.00c  0.9890
    6013.00c  0.0110
   92235.00c  0.001   $ Trace fuel
mt1 grph.18t  $ ← CRITICAL! 600K graphite S(α,β)
c
c ✓ CORRECT: Graphite material has MT card
c ✓ CORRECT: Using grph.18t (600K) for HTGR operating conditions
c
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ ← REQUIRED! Same temperature
c
c ✓ CORRECT: Reflector graphite also has MT card
c
m3  $ Helium coolant (no MT needed - monatomic gas)
    2004.00c  1.0
c
c ✓ CORRECT: Helium doesn't need MT card (monatomic gas)
c
c -------------------- PHYSICS SETTINGS --------------------
c
mode n
c Transport neutrons only (criticality calculation)
c
phys:n 20 0 0 J J J J J 1
c emax = 20 MeV (sufficient for fission spectrum)
c ngam = 1 (photon production enabled, even though not transported)
c
c ✓ CORRECT: emax=20 MeV covers fission neutrons
c ✓ CORRECT: ngam=1 enables photon production
c
c -------------------- SOURCE --------------------
c
kcode 10000 1.0 50 250
c 10000 histories per cycle
c k_initial = 1.0
c 50 cycles skipped for source convergence
c 250 active cycles
c
ksrc 0 0 0
c Initial source position at origin
c
c ===================================================================
c VALIDATION NOTES
c ===================================================================
c
c ✓ MODE card: N (neutron transport)
c ✓ All graphite materials have MT cards (grph.18t)
c ✓ Temperature library appropriate (600K for HTGR)
c ✓ PHYS:N emax covers source energy
c ✓ No missing thermal scattering
c
c Expected validator output: PASS (no errors)
c
c ===================================================================
c END OF INPUT
c ===================================================================
