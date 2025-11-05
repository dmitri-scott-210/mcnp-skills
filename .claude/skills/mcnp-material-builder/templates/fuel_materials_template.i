Fuel Material Templates for MCNP
c ==================================================================
c Purpose: Demonstrate UO2 and MOX fuel definitions with proper
c          enrichment, density, and temperature specifications
c ==================================================================
c Cell Cards
1    1  -10.50  -1  IMP:N=1  TMP=6.2e-8     $ UO2 3% enriched, 900 K
2    2  -10.50  -2  IMP:N=1  TMP=6.2e-8     $ UO2 5% enriched, 900 K
3    3  -10.50  -3  IMP:N=1  TMP=6.2e-8     $ MOX fuel, 900 K
4    0            4  IMP:N=0                $ Void (graveyard)

c Surface Cards
1    SO  1.0                  $ Fuel pellet 1 (1 cm radius)
2    SO  2.0                  $ Fuel pellet 2 (2 cm radius)
3    SO  3.0                  $ Fuel pellet 3 (3 cm radius)
4    SO  100.0                $ Outer boundary

c Data Cards
MODE  N
c Material 1: UO2 Fuel, 3% U-235 Enrichment, 900 K
c Density: 10.5 g/cm3 → -10.50 atoms/b-cm, M=270 g/mol (U + 2O)
c Atomic fractions: U-235: 0.03, U-238: 0.97, O-16: 2.0
M1   92235.80c  0.03  92238.80c  0.97  8016.80c  2.0  $ 3% enriched UO2
c Material 2: UO2 Fuel, 5% U-235 Enrichment, 900 K
c Density: 10.5 g/cm3 → -10.50 atoms/b-cm
c Higher enrichment for increased reactivity
M2   92235.80c  0.05  92238.80c  0.95  8016.80c  2.0  $ 5% enriched UO2
c Material 3: MOX Fuel (Mixed Oxide: Depleted U + Pu), 900 K
c Density: 10.5 g/cm3, typical LWR MOX composition
c Contains plutonium isotopes from reprocessed spent fuel
M3   92238.80c  0.85  94239.80c  0.05  94240.80c  0.03  &
     94241.80c  0.02  8016.80c  2.0                     $ Depleted U + Pu isotopes
SDEF  POS=0 0 0  ERG=1.0
NPS  10000
PRINT
