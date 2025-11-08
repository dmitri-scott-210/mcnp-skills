# QUICK REFERENCE: TRISO PARTICLE & HTGR SPECIFICATIONS FOR MCNP

**Source:** Fairhurst-Agosta & Kozlowski (2024) - AGR-1 Shutdown Dose Rate Article
**Purpose:** Rapid lookup of key parameters for MCNP model development

---

## TRISO PARTICLE GEOMETRY (Table 5 from Article)

### Layer-by-Layer Specifications

```
Kernel (UO₂, 19.75% enriched):
  - Radius: 0.0250 cm (250 μm)
  - Density: 10.8 g/cm³
  - Material: UO₂ with ε = 19.75% U-235

Buffer (Porous Carbon):
  - Inner radius: 0.0250 cm
  - Outer radius: 0.0350 cm
  - Thickness: 0.0100 cm (100 μm)
  - Density: 0.98 g/cm³
  - Material: C (porous graphite)

IPyC (Inner Pyrolytic Carbon):
  - Inner radius: 0.0350 cm
  - Outer radius: 0.0390 cm
  - Thickness: 0.0040 cm (40 μm)
  - Density: 1.85 g/cm³
  - Material: C (dense PyC)

SiC (Silicon Carbide):
  - Inner radius: 0.0390 cm
  - Outer radius: 0.0425 cm
  - Thickness: 0.0035 cm (35 μm)
  - Density: 3.20 g/cm³
  - Material: SiC (stoichiometric)

OPyC (Outer Pyrolytic Carbon):
  - Inner radius: 0.0425 cm
  - Outer radius: 0.0465 cm
  - Thickness: 0.0040 cm (40 μm)
  - Density: 1.86 g/cm³
  - Material: C (dense PyC)

TOTAL TRISO OUTER RADIUS: 0.0465 cm (465 μm)
```

---

## MCNP CELL CARD EXAMPLE (TRISO Particle)

```mcnp
c --- TRISO Particle (Universe 1) ---
c Kernel: UO2 enriched to 19.75%
101  1  -10.8   -1001              u=1  imp:n=1  $ Kernel (UO2)
102  2  -0.98   -1002  1001        u=1  imp:n=1  $ Buffer (C)
103  3  -1.85   -1003  1002        u=1  imp:n=1  $ IPyC (C)
104  4  -3.20   -1004  1003        u=1  imp:n=1  $ SiC
105  5  -1.86   -1005  1004        u=1  imp:n=1  $ OPyC (C)
106  6  -3.20   -1006  1005        u=1  imp:n=1  $ Compact matrix (SiC)
107  0          1006              u=1  imp:n=0  $ Outside (void or next level)

c --- Surfaces for TRISO ---
1001  so  0.0250     $ Kernel outer
1002  so  0.0350     $ Buffer outer
1003  so  0.0390     $ IPyC outer
1004  so  0.0425     $ SiC outer
1005  so  0.0465     $ OPyC outer
1006  rpp -0.05 0.05 -0.05 0.05 -0.05 0.05  $ Lattice element box (adjust to pitch)
```

---

## MATERIAL CARDS

### M1: UO₂ Kernel (19.75% U-235)

Calculation for 19.75% enriched UO₂ at 10.8 g/cm³:

```
Atomic masses:
  U-235: 235.044 amu
  U-238: 238.051 amu
  O-16:  15.999 amu

Weight fraction U-235: w = 0.1975
Weight fraction U-238: 1 - w = 0.8025

Atom fraction U-235: x = (0.1975/235.044) / [(0.1975/235.044) + (0.8025/238.051)]
                        = 0.8405×10⁻³ / [0.8405×10⁻³ + 3.372×10⁻³]
                        = 0.1994 (atom fraction)

Atom fraction U-238: 1 - 0.1994 = 0.8006

UO₂ molecular weight (enriched):
  M = 0.1994×235.044 + 0.8006×238.051 + 2×15.999
  M = 46.88 + 190.55 + 32.00 = 269.43 g/mol

Atom density UO₂:
  N_total = (10.8 g/cm³ × 6.022×10²³) / (269.43 g/mol × 10²⁴)
  N_total = 0.02413 atoms/barn-cm

U-235: 0.02413 × 0.1994 / 3 = 0.001604 atoms/barn-cm
U-238: 0.02413 × 0.8006 / 3 = 0.006440 atoms/barn-cm
O-16:  0.02413 × 2 / 3      = 0.016086 atoms/barn-cm
```

**MCNP Material Card:**
```mcnp
m1    92235.80c  0.001604   $ U-235
      92238.80c  0.006440   $ U-238
       8016.80c  0.016086   $ O-16
```

### M2: Buffer Carbon (0.98 g/cm³)

```mcnp
m2    6000.80c  0.049075   $ C (N = 0.98×6.022×10²³ / 12.011×10²⁴)
```

### M3: IPyC (1.85 g/cm³)

```mcnp
m3    6000.80c  0.092688   $ C (N = 1.85×6.022×10²³ / 12.011×10²⁴)
```

### M4: SiC (3.20 g/cm³)

```
SiC stoichiometry: 1:1 (Si:C)
Molecular weight: 28.085 + 12.011 = 40.096 g/mol
Atom density: N = (3.20×6.022×10²³) / (40.096×10²⁴) = 0.04806 atoms/barn-cm
Si: 0.02403 atoms/barn-cm
C:  0.02403 atoms/barn-cm
```

```mcnp
m4   14000.80c  0.02403    $ Si
      6000.80c  0.02403    $ C
```

### M5: OPyC (1.86 g/cm³)

```mcnp
m5    6000.80c  0.093189   $ C (N = 1.86×6.022×10²³ / 12.011×10²⁴)
```

### M6: Compact Matrix SiC (3.20 g/cm³) - Same as M4

```mcnp
m6   14000.80c  0.02403    $ Si
      6000.80c  0.02403    $ C
```

### M7: Graphite (1.75 g/cm³) - Reflectors & Assemblies

```mcnp
m7    6000.80c  0.087702   $ C (N = 1.75×6.022×10²³ / 12.011×10²⁴)
mt7   grph.20t             $ Graphite thermal scattering S(α,β)
```

### M8: Stainless Steel 316L (assume 8.0 g/cm³)

**Typical SS316L composition (weight %):**
- Fe: 65%, Cr: 17%, Ni: 12%, Mo: 2.5%, Mn: 2%, Si: 1%, C: 0.03%, rest: 0.47%

```mcnp
m8   26000.80c  0.05930    $ Fe (calculated for typical SS316L)
     24000.80c  0.01665    $ Cr
     28000.80c  0.01041    $ Ni
     42000.80c  0.00133    $ Mo
     25055.80c  0.00185    $ Mn
     14000.80c  0.00182    $ Si
      6000.80c  0.00013    $ C
```
*Note: Adjust isotopic fractions for precise activation calculations*

### M9: Portland Concrete (2.3 g/cm³)

**Standard Portland concrete (simplified - use PNNL-15870 for detailed):**

```mcnp
m9    1001.80c  0.0168     $ H
      8016.80c  0.0451     $ O
     11023.80c  0.0017     $ Na
     12000.80c  0.0024     $ Mg
     13027.80c  0.0047     $ Al
     14000.80c  0.0160     $ Si
     19000.80c  0.0013     $ K
     20000.80c  0.0410     $ Ca
     26000.80c  0.0012     $ Fe
```
*Note: This is approximate; use validated concrete composition for shielding studies*

### M10: Air (80% N₂, 20% O₂ by volume)

```mcnp
m10   7014.80c  0.0000399  $ N-14 (80 vol%)
      8016.80c  0.0000100  $ O-16 (20 vol%)
```
*At 1 atm, 20°C: ρ_air ≈ 0.001205 g/cm³*

---

## μHTGR CORE GEOMETRY PARAMETERS

```
CORE CONFIGURATION:
  Total assemblies:     37 (24 fuel + 12 control + 1 shutdown)
  Assembly pitch:       30 cm
  Axial layers:         4
  Layer height:         68 cm
  Total core height:    272 cm (4 × 68)

ASSEMBLY DETAILS:
  Fuel channel radius:  1.15 cm
  Coolant channel rad:  0.775 cm
  Channel pitch:        3.2 cm
  Control rod hole:     4 cm radius (control assemblies)
  Shutdown rod hole:    6 cm radius (reserved shutdown assembly)

REFLECTOR:
  Radial radius:        134 cm
  Bottom height:        68 cm
  Top height:           68 cm
  Material:             Graphite (1.75 g/cm³)

FUEL COMPACT:
  Matrix material:      SiC (3.2 g/cm³)
  TRISO packing:        40% volume fraction
  Particle pitch:       0.1 cm (regular lattice)

SHIELDING:
  Concrete walls:       100 cm thick Portland (2.3 g/cm³)
  Wall distance:        191 cm from radial reflector
  Citadel floor:        70 cm thick concrete
  Cavity height:        700 cm (top of core to ground level)
  Cavity fill:          Air (80% N₂, 20% O₂)
```

---

## OPERATIONAL PARAMETERS

```
μHTGR MICROREACTOR:
  Thermal power:        10 MWth
  Initial k-eff:        1.26797
  Core lifetime:        16.07 years (calculated to k-eff = 1.0)
  Design target:        20 years (not achieved with simplified model)
  Fuel enrichment:      19.75% U-235
  Coolant:              Helium (assumed, not explicitly stated)
  Operating temp:       High temperature (not specified, >700°C typical)

AGR-1 EXPERIMENT:
  Host reactor:         ATR (Advanced Test Reactor, 250 MWth)
  Location:             B-10 irradiation hole
  Irradiation time:     ~3 years (13 power cycles)
  Number of capsules:   6 (stacked vertically)
  Compacts per capsule: 12 (3 columns × 4 compacts)
  Total compacts:       72
```

---

## DEPLETION/ACTIVATION CALCULATION SETUP

### MOAA Workflow (or equivalent coupling)

```
STEP 1: Neutron Transport (MCNP 6.2)
  - Calculate multi-group neutron flux
  - Extract one-group reaction cross-sections
  - Tally in each depletion region

STEP 2: Activation/Depletion (ORIGEN-S via SCALE 6.2.4)
  - COUPLE: Generate one-group libraries from flux spectrum
  - ORIGEN: Solve Bateman equations for isotope evolution
  - OPUS: Extract photon source spectra at decay times

STEP 3: Photon Transport (MCNP 6.2)
  - Fixed source: Photon energy spectra from ORIGEN
  - Source definition: SDEF with SI/SP cards (energy bins/probabilities)
  - Dose tally: F4:p with fluence-to-dose conversion (ICRP factors)
  - Output: Dose rate = F4:p × Σ(Sᵢ) × 3.6×10⁻⁹ [Sv/h]
```

### Critical MCNP Requirements for MOAA

```
1. VOLUME CARDS (VOL):
   - Must calculate and specify all depletion cell volumes
   - For repeated structures: total material volume in geometry
   - MCNP auto-calc only works for simple cells
   - Example: If 1000 TRISO kernels, each V=6.545×10⁻⁵ cm³
             → VOL 0.06545 (total fuel volume)

2. TALLY SETUP:
   - F4:n in each depletion cell (flux for ORIGEN)
   - FM card for reaction rates (n,gamma), (n,fission), etc.
   - E card for energy bins (multi-group structure)
   - SD card if not using VOL (segment divisor)

3. MATERIAL TRACKING:
   - Each depletion cell needs unique material number
   - Material cards updated by MOAA each time step
   - Initial fresh fuel composition at BOC

4. KCODE (if criticality) or SDEF (if fixed source)
   - KCODE for reactor operation: 50 10 30 (skip 50, run 10×30)
   - Increase histories for good statistics (≥10k per cycle minimum)
```

### Repeated Structure Strategy

```
GROUPING APPROACH (from verification exercise):
  - Whole core as single repeated structure: 15.6% error (NOT RECOMMENDED)
  - Grouped by flux level (4 groups): 4.3% error (BETTER)
  - Per-assembly grouping: Recommended for μHTGR

IMPLEMENTATION:
  Universe 1: Single TRISO particle (5 nested spheres)
  Universe 2: TRISO lattice in compact matrix (LAT=1, hexagonal or LAT=2, rectangular)
  Universe 3: Compact column in fuel channel
  Universe 4: Fuel assembly (lattice of fuel/coolant channels)
  Fill core with lattice of assemblies

DEPLETION REGIONS:
  - Minimum: One per assembly (37 regions for μHTGR)
  - Better: Radial zones (inner, mid, outer ring assemblies)
  - Optimal: Balance accuracy (<5% error) vs. computational cost
```

---

## DOSE RATE CALCULATION EQUATIONS

### Dose Rate Formula (from Article)

```
D-dot [Sv/h] = F4:p [pSv/src] × Σᵢ Sᵢ [γ/s] × 3.6×10⁻⁹

Where:
  D-dot = Dose rate at detector location
  F4:p  = F4 photon flux tally (with dose conversion factors)
  Sᵢ    = Total photon emission rate from source region i

Source emission rate:
  Sᵢ [γ/s] = ∫ φᵢᵞ(E) dE

  φᵢᵞ(E) = Photon source energy distribution (from ORIGEN)

Cell emission probability:
  sᵢ = Sᵢ / Σⱼ Sⱼ (normalized to 1)
```

### MCNP Source Definition (Photon Transport Step)

```mcnp
c --- Photon Source Definition ---
MODE P                           $ Photon transport only
SDEF  CEL=D1  ERG=D2  PAR=2      $ Source: cell distribution, energy spectrum, photons

c --- Source Cells (from depletion regions) ---
SI1  L  101 102 103 ...          $ List of source cell numbers
SP1     0.45 0.32 0.18 ...       $ Cell emission probabilities (sᵢ)

c --- Energy Spectrum (example - from ORIGEN output) ---
SI2  H  0.0 0.1 0.5 1.0 2.0 3.0  $ Energy bins [MeV]
SP2     0.0 0.35 0.28 0.22 0.10 0.05  $ Spectrum probabilities

c --- Dose Conversion (ICRP AP geometry factors) ---
c Use DE/DF cards or built-in dose response functions
c Example using flux-to-dose conversion factors:
F4:P  <detector_cell>            $ Flux tally in detector
DE4   0.01 0.05 0.1 0.5 1.0 2.0 5.0 10.0  $ Energy bins [MeV]
DF4   0.06 0.3  0.8 2.4 4.2 5.8 8.5 11.2  $ Dose factors [pSv-cm²]
                                           $ (Example values - use ICRP-74 or ANSI/ANS-6.1.1-1977)
```

*Note: Actual dose conversion factors depend on geometry (AP, PA, LAT, ROT, ISO)*

---

## CRITICAL MODELING BEST PRACTICES

### Geometry Verification
```
1. MCNP Plotting:
   PX 0 0.5 (cross-section at x=0, extent=0.5 cm)
   PY 0 0.5
   PZ 0 100 (axial view)
   → Visually check TRISO layers, lattice arrangement, assembly layout

2. Volume Check:
   PRINT 40 (print calculated volumes)
   Compare to VOL card entries
   Check for "volume not calculated" warnings

3. Lost Particles:
   DBCN card for debugging
   Check for geometry errors (overlaps, gaps)
   Run with VOID card to catch streaming paths
```

### Statistical Quality
```
1. Adequate histories:
   - Neutron transport: NPS 1e6 minimum (criticality)
   - Photon transport: NPS 1e7 minimum (shielding)
   - Check tally relative error < 0.05 (5%)

2. Variance reduction (photon transport):
   - DXTRAN spheres for detector locations
   - Weight windows for deep penetration
   - Energy cutoff (PHYS:P EMAX EMCPF IDES)

3. Convergence checks:
   - KCODE: Check entropy stabilization
   - Shannon entropy bins: DBCN card
   - Source convergence: plot k-eff vs. cycle
```

### Material Evolution
```
1. Time steps:
   - Fine enough to capture isotope buildup
   - Typical: 10-20 steps per year for steady operation
   - Finer near startup (flux transients)

2. Predictor-corrector:
   - Use for better accuracy (MOAA option)
   - First pass: BOC cross-sections (predictor)
   - Second pass: Mid-point cross-sections (corrector)

3. Tracking:
   - Plot k-eff vs. time (should decrease monotonically)
   - Check fission product inventory (Xe-135, Sm-149)
   - Verify actinide buildup (Pu-239, Pu-240, Pu-241)
```

---

## VALIDATION CHECKLIST

### Before Running Production Calculations:

- [ ] TRISO geometry verified (plot cross-sections, check radii)
- [ ] Material cards validated (atom densities calculated correctly)
- [ ] Volumes calculated and specified (VOL cards for all depletion cells)
- [ ] Thermal scattering included (grph.20t for graphite)
- [ ] Cross-section libraries consistent (ENDF/B-VIII.0)
- [ ] Repeated structures tested (single particle → compact → assembly)
- [ ] Statistical quality adequate (rel. error < 5% in tallies of interest)
- [ ] Geometry checked (no overlaps, no lost particles)
- [ ] Convergence verified (k-eff stable, entropy converged for KCODE)
- [ ] Depletion grouping appropriate (flux-based, < 5% error target)
- [ ] Photon source spectra extracted (ORIGEN output → SI/SP cards)
- [ ] Dose conversion factors correct (ICRP values for geometry)
- [ ] Results physically reasonable (dose decreases with distance, time)

### Comparison Benchmarks:

- [ ] AGR-1 Depletion Benchmark (if available from INL)
- [ ] Simple verification problem (article Section "Verification")
- [ ] Hand calculations (point source dose, isotope decay)
- [ ] Code-to-code comparison (Serpent, SCALE/TRITON)
- [ ] Literature values (similar HTGR designs)

---

## TYPICAL RESULTS RANGES (from Article)

### AGR-1 Dose Rates:
```
At 6 cm (capsule surface):
  1 day:    ~700 Sv/h
  30 days:  ~200 Sv/h
  1 year:   ~4 Sv/h

At 1 m (hot cell operations):
  1 day:    ~25 Sv/h
  30 days:  ~7 Sv/h
  1 year:   ~0.1 Sv/h

Conclusion: > 1 year cool-down or hot cell shielding required for PIE
```

### μHTGR Decommissioning:
```
Citadel floor (7 m above core top):
  3 months cool-down: > 40 mSv/h

Conclusion: 3-month strategy insufficient, need longer cool-down or shielding
```

### Source Intensity Evolution:
```
Total photon emission:
  1 day:    1.2×10¹⁵ γ/s
  30 days:  3.3×10¹⁴ γ/s (73% reduction)
  1 year:   1.3×10¹³ γ/s (99% reduction from 1 day)
```

### Burnup:
```
μHTGR k-eff evolution:
  BOL (fresh fuel):     1.268
  EOL (critical):       1.000
  Lifetime:             16.07 years (10 MWth)
  Excess reactivity:    ~27,000 pcm (26.8% Δk/k)
```

---

## COMMON PITFALLS AND SOLUTIONS

### Pitfall 1: Volume not specified for repeated structures
**Symptom:** MCNP calculates single cell volume, not total
**Solution:** Use VOL card with hand-calculated total material volume

### Pitfall 2: Poor statistics in deep shielding
**Symptom:** Tally relative error > 10%
**Solution:** Variance reduction (DXTRAN, weight windows), increase NPS

### Pitfall 3: Whole-core repeated structure
**Symptom:** Large errors in dose rates (15%+)
**Solution:** Flux-based grouping (per assembly minimum)

### Pitfall 4: Missing thermal scattering for graphite
**Symptom:** k-eff too low, spectrum too hard
**Solution:** Add MT card for graphite (grph.20t)

### Pitfall 5: Room-temperature cross-sections for high-temp reactor
**Symptom:** Slight k-eff bias (typically -100 to -500 pcm)
**Solution:** Use temperature-dependent libraries (.81c, .82c) or accept bias as conservative

### Pitfall 6: Lost particles in complex lattice
**Symptom:** "Lost particle" errors
**Solution:** Check geometry (IP, DEBUG cards), verify lattice boundaries, ensure proper fill

### Pitfall 7: Photon source normalization error
**Symptom:** Dose rates off by orders of magnitude
**Solution:** Verify cell emission probabilities sum to 1, check source intensity units (γ/s)

### Pitfall 8: Inadequate depletion time steps
**Symptom:** k-eff oscillates, isotope concentrations unrealistic
**Solution:** Refine time steps (especially early in cycle), use predictor-corrector

---

## QUICK CONVERSION FACTORS

```
UNITS:
  1 Sv = 100 rem
  1 mSv = 0.1 rem
  1 barn = 10⁻²⁴ cm²
  1 barn-cm = 10⁻²⁴ cm³
  atoms/barn-cm = 10²⁴ atoms/cm³

CONSTANTS:
  Avogadro: N_A = 6.022×10²³ atoms/mol

ATOM DENSITY:
  N [atoms/barn-cm] = (ρ [g/cm³] × N_A [1/mol]) / (M [g/mol] × 10²⁴)

ENRICHMENT:
  Weight % to atom % (binary mixture):
  x_atom = (w/M_235) / [(w/M_235) + ((1-w)/M_238)]

SPHERE VOLUME:
  V = (4/3)πr³
  Shell: V = (4/3)π(r_out³ - r_in³)

DOSE LIMITS (for reference):
  Occupational: 20 mSv/year (averaged over 5 years)
  Public:       1 mSv/year
  Emergency:    100 mSv (single event)
```

---

## FILE ORGANIZATION EXAMPLE

```
project_root/
├── input/
│   ├── triso_particle.i          # Single TRISO universe definition
│   ├── compact_lattice.i         # Compact with TRISO lattice
│   ├── assembly.i                # Fuel assembly geometry
│   ├── full_core_BOL.i           # Full core, beginning-of-life
│   ├── full_core_depletion.i     # Depletion configuration
│   └── shutdown_dose_rate.i      # Photon transport for dose calc
├── materials/
│   ├── uo2_kernel_19.75pct.m     # UO2 material cards
│   ├── carbon_coatings.m         # Buffer, IPyC, OPyC
│   ├── sic.m                     # SiC layer and matrix
│   ├── graphite.m                # Reflector graphite with S(a,b)
│   └── structures.m              # SS316L, concrete, air
├── tallies/
│   ├── flux_tallies.i            # Neutron flux for depletion
│   └── dose_tallies.i            # Photon dose with conversion factors
├── moaa/
│   ├── user_input_file.yml       # MOAA configuration
│   └── depletion_cells.txt       # List of cells to deplete
├── output/
│   ├── neutron_flux/             # MCNP flux results
│   ├── origen_inventory/         # Isotopic concentrations
│   ├── photon_sources/           # Decay gamma spectra
│   └── dose_rates/               # Final dose rate maps
└── validation/
    ├── benchmark_comparison.xlsx # AGR-1 benchmark results
    └── sensitivity_studies/      # Grouping, lattice, etc.
```

---

## REFERENCES AND RESOURCES

**Primary Article:**
Fairhurst-Agosta, R. & Kozlowski, T. (2024). "Shutdown dose rate calculations in high-temperature gas-cooled reactors using the MCNP-ORIGEN activation automation tool." Nuclear Science and Technology Open Research, 1:20. DOI: 10.12688/nuclscitechnolopenres.17447.2

**Code Manuals:**
- MCNP 6.2: LA-UR-17-29981 (https://mcnp.lanl.gov/)
- SCALE 6.2.4: ORNL/TM-2005/39 (https://www.ornl.gov/scale)

**Benchmark:**
- AGR-1 Depletion Benchmark: INL Technical Report (contact INL for access)

**Dose Conversion:**
- ICRP-74: "Conversion Coefficients for use in Radiological Protection against External Radiation"
- ANSI/ANS-6.1.1-1977: Neutron and Gamma-Ray Flux-to-Dose-Rate Factors

**Material Compositions:**
- PNNL-15870 Rev.1: Compendium of Material Composition Data for Radiation Transport Modeling

---

**Document Created:** 2025-11-07
**Source File:** /home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1_research_article.xml
**Analysis Tool:** MCNP Technical Documentation Analyzer
**Version:** Quick Reference v1.0
