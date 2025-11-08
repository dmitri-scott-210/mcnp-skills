PWR Physics Setup - CORRECT EXAMPLE
c Demonstrates proper thermal scattering for PWR at 350K
c Shows neutron-photon coupling for reactor calculations
c
c ===================================================================
c CELL CARDS
c ===================================================================
c
1 1 -10.2  -1      imp:n=1 imp:p=1  $ UO2 fuel
2 2 -6.5    1 -2   imp:n=1 imp:p=1  $ Zircaloy clad
3 3 -1.0    2 -3   imp:n=1 imp:p=1  $ Water moderator
4 0         3      imp:n=0 imp:p=0  $ Void

c ===================================================================
c SURFACE CARDS
c ===================================================================
c
1 cz  0.41  $ Fuel radius
2 cz  0.48  $ Clad outer radius
3 cz  2.0   $ Water boundary

c ===================================================================
c DATA CARDS
c ===================================================================
c
c -------------------- MATERIALS --------------------
c
m1  $ UO2 fuel
   92235.70c  0.045  $ 4.5% enriched U-235
   92238.70c  0.955  $ U-238
    8016.70c  2.0    $ Oxygen
c (No MT needed - fuel, not moderator)
c
c ✓ CORRECT: Fuel doesn't need MT card
c
m2  $ Zircaloy clad
   40000.60c  1.0    $ Natural zirconium
c (No MT needed - structural)
c
c ✓ CORRECT: Structural material doesn't need MT card
c
m3  $ Light water moderator
    1001.70c  2.0    $ Hydrogen-1
    8016.70c  1.0    $ Oxygen-16
mt3 lwtr.13t  $ ← CRITICAL! 350K water S(α,β) for PWR
c
c ✓ CORRECT: Water has MT card
c ✓ CORRECT: Using lwtr.13t (350K) for PWR average temperature
c
c -------------------- PHYSICS SETTINGS --------------------
c
mode n p
c Transport neutrons AND photons (coupled)
c
c ✓ CORRECT: MODE N P for coupled neutron-photon transport
c
phys:n 20 0 0 J J J J J 1
c emax = 20 MeV (covers fission neutrons)
c ngam = 1 (photon production ENABLED)
c
c ✓ CORRECT: ngam=1 enables photon production (consistent with MODE N P)
c
phys:p 100
c emax = 100 MeV for photons
c ides = 0 (default, electron production - though MODE E not used)
c
c ✓ CORRECT: Photon physics card present
c
c -------------------- SOURCE --------------------
c
kcode 10000 1.0 50 250
c 10000 histories per cycle
c k_initial = 1.0
c 50 cycles skipped
c 250 active cycles
c
ksrc 0 0 0
c Initial source at origin (center of fuel)

c ===================================================================
c VALIDATION NOTES
c ===================================================================
c
c ✓ MODE card: N P (neutron-photon coupling)
c ✓ Water moderator has MT card (lwtr.13t)
c ✓ Temperature library appropriate (350K for PWR average)
c ✓ PHYS:N emax=20 MeV covers fission spectrum
c ✓ PHYS:N ngam=1 (photon production enabled, consistent with MODE P)
c ✓ PHYS:P card present for photon transport
c ✓ No missing thermal scattering
c ✓ Fuel and clad correctly have no MT cards
c
c Expected validator output: PASS (no errors)
c
c Physics Consistency:
c ✓ Neutron-photon coupling: CONSISTENT
c   - MODE includes P (photon transport)
c   - PHYS:N has ngam=1 (photon production enabled)
c   - Result: Photons from (n,γ) reactions will be transported
c
c ===================================================================
c TEMPERATURE NOTES
c ===================================================================
c
c PWR operating temperatures:
c - Cold leg: ~325K (52°C) → lwtr.11t
c - Average: ~350K (77°C) → lwtr.13t ← USED HERE
c - Hot leg: ~400K (127°C) → lwtr.14t
c
c This model uses lwtr.13t (350K) representing average PWR temperature.
c For more detailed models, different regions could use different libraries:
c - Cold leg regions: lwtr.11t
c - Hot leg regions: lwtr.14t
c
c ===================================================================
c COMPARISON WITH HTGR
c ===================================================================
c
c Key differences from HTGR model:
c 1. Moderator: Light water (lwtr.13t) vs Graphite (grph.18t)
c 2. Temperature: 350K vs 600K
c 3. MODE: N P (coupled) vs N (neutron-only often sufficient)
c 4. Fuel: UO2 vs UCO/TRISO
c
c Similarities:
c 1. Both need MT cards for moderator
c 2. Both are thermal reactors (need low neutron cutoffs)
c 3. Both use criticality calculation (KCODE)
c
c ===================================================================
c END OF INPUT
c ===================================================================
