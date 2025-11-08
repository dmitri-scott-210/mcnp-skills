c ========================================
c PWR FUEL PIN MODEL - ANNOTATED EXAMPLE
c ========================================
c
c Description: Single PWR fuel pin with UO2 fuel, gas gap, and Zircaloy cladding
c Purpose: Demonstrate systematic numbering, commenting, and organization
c
c Author: MCNP Skills Framework
c Date: 2024-11-08
c
c GEOMETRY DESCRIPTION:
c   - Cylindrical fuel pellet (UO2, 3.5% enriched)
c   - Helium gas gap
c   - Zircaloy-4 cladding
c   - Water coolant/moderator
c   - Total height: 10 cm (representative segment)
c
c NUMBERING SCHEME:
c   Cells: 100-series (fuel pin components)
c   Surfaces: 100-series (correlated with cells)
c   Materials: 1-digit (m1=fuel, m2=clad, m3=coolant)
c
c UNITS:
c   Lengths: cm
c   Densities: g/cm³ (negative for mass fractions)
c   Energies: MeV
c
c MATERIALS:
c   m1: UO2 fuel, 3.5% U-235 enrichment, 10.2 g/cm³
c   m2: Zircaloy-4 cladding, 6.5 g/cm³
c   m3: Light water at 300K, 1.0 g/cm³
c
c PHYSICS:
c   - Neutron transport only (MODE N)
c   - Fixed source (point source at center)
c   - ENDF/B-VII.1 cross sections at 300K
c
c ========================================

c ========================================
c CELL BLOCK
c ========================================
c
c FUEL PIN COMPONENTS
c   Inner to outer: fuel, gap, clad, coolant
c
101  1  -10.2  -101  102 -103  imp:n=1  vol=52.3  $ UO2 fuel pellet
102  0         101 -102  102 -103  imp:n=1        $ He gas gap (void)
103  2  -6.5   102 -104  102 -103  imp:n=1        $ Zircaloy clad
104  3  -1.0   104       102 -103  imp:n=1        $ Water coolant
c
c OUTSIDE WORLD
c
999  0  -102:103  imp:n=0  $ Graveyard (axial or radial boundary)

c ========================================
c SURFACE BLOCK
c ========================================
c
c RADIAL SURFACES (cylinders on z-axis)
c
101  cz  0.4096  $ Fuel pellet outer radius (standard PWR, cm)
102  cz  0.4178  $ Clad inner radius (gas gap outer, cm)
104  cz  0.4750  $ Clad outer radius (standard PWR, cm)
c
c AXIAL SURFACES (planes perpendicular to z-axis)
c
102  pz   0.0    $ Bottom of fuel segment
103  pz  10.0    $ Top of fuel segment (10 cm height)

c ========================================
c DATA BLOCK
c ========================================
c
MODE N
c
c --- MATERIALS ---
c
c Material m1: UO2 fuel, 3.5% enriched, density = 10.2 g/cm³
c Temperature: 900K (fuel operating temperature)
m1
   92234.70c -0.000281  $ U-234 (0.028% by mass)
   92235.70c -0.032294  $ U-235 (3.5% enrichment, 3.23% by mass)
   92238.70c -0.855153  $ U-238 (96.5%, balance of uranium)
    8016.70c -0.112272  $ O-16 (stoichiometric UO2)
c Note: Negative fractions = mass fractions (sum to 1.0)
c
c Material m2: Zircaloy-4 cladding, density = 6.5 g/cm³
m2
   40000.70c -0.9800  $ Zr (natural, 98.0%)
   50000.70c -0.0146  $ Sn (1.46%)
   26000.70c -0.0021  $ Fe (0.21%)
   24000.70c -0.0010  $ Cr (0.10%)
   72000.70c  0.0003  $ Hf (ppm level, trace)
c
c Material m3: Light water, density = 1.0 g/cm³, 300K
m3
    1001.70c  2.0  $ H-1 (2 atoms per molecule)
    8016.70c  1.0  $ O-16 (1 atom per molecule)
mt3  lwtr.01t  $ S(α,β) thermal scattering for water at 300K
c
c --- SOURCE ---
c
c Point source at center of fuel pin
c 14.1 MeV neutrons (D-T fusion, for testing)
sdef  pos=0 0 5  erg=14.1  par=n
c      x y z (center of 10 cm segment)
c
c --- TALLIES ---
c
c Tally 4: Cell flux in fuel region
f4:n   101           $ Fuel cell
e4     0.01 0.1 1 10 14 15  $ Energy bins: thermal to 15 MeV
fc4    Fuel region neutron flux
c
c Tally 14: Cell flux in water
f14:n  104           $ Water coolant
e14    0.01 0.1 1 10
fc14   Coolant region flux
c
c --- TERMINATION ---
c
nps   1000000  $ 1 million particle histories

