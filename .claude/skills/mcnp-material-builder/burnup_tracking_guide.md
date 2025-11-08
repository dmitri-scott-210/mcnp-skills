# Burnup Tracking Guide
## Which Isotopes to Track in Depletion Calculations and Why

**Purpose**: Help users select appropriate isotopes for burnup/depletion modeling
**Scope**: Actinide chains, fission products, activation products

---

## WHY TRACK SPECIFIC ISOTOPES?

Depletion calculations solve Bateman equations for isotope evolution during irradiation:

```
dN_i/dt = Σ_j (λ_j→i N_j + σ_j→i φ N_j) - (λ_i + σ_i φ) N_i

where:
  N_i = number density of isotope i
  λ_i = decay constant
  σ_i = reaction cross-section (capture, fission)
  φ = neutron flux
```

**Impact on reactor physics**:
- **Reactivity**: Fission products absorb neutrons (negative reactivity)
- **Spectrum**: Pu buildup hardens spectrum
- **Shutdown dose**: Activation products determine post-shutdown radiation
- **Fuel cycle**: Pu inventory affects reprocessing economics

**Trade-off**:
- More isotopes → better accuracy, longer computation time
- Fewer isotopes → faster, but may miss important physics

---

## MINIMUM ISOTOPE SET (20-25 isotopes)

### Actinides (Minimum: 8 isotopes)

**ALWAYS track**:
```mcnp
92234.70c  ...  $ U-234 (from U-235 decay, alpha source)
92235.70c  ...  $ U-235 (primary fissile, depletes)
92236.70c  ...  $ U-236 (from U-235 capture, parasitic absorber)
92238.70c  ...  $ U-238 (primary fertile, breeds Pu-239)
93237.70c  ...  $ Np-237 (from U-235 fission, Pu precursor)
94239.70c  ...  $ Pu-239 (bred from U-238, fissile)
94240.70c  ...  $ Pu-240 (from Pu-239 capture, parasitic)
94241.70c  ...  $ Pu-241 (fissile, important for reactivity)
```

**Why these**:
- U-235: Primary fissile, depletes monotonically
- U-238: Fertile material, breeds Pu-239 via (n,γ) then β⁻ decay
- Pu-239: Builds up from U-238, becomes dominant fissile after ~15 GWd/MTU
- Pu-240: Parasitic absorber, high spontaneous fission neutron source
- Pu-241: Fissile, important for reactivity but decays to Am-241
- Others: Complete chain from U-235 → Np-237 → Pu-238/239/240/241

**Reactivity impact**: Pu buildup compensates for U-235 depletion, extends fuel life

### Fission Products (Minimum: 10-12 isotopes)

**Strong absorbers (MUST track)**:
```mcnp
54135.70c  ...  $ Xe-135 (highest thermal σ_abs ≈ 2.65×10⁶ barn, equilibrium poison)
62149.70c  ...  $ Sm-149 (σ_abs ≈ 4.1×10⁴ barn, equilibrium + residual)
64157.70c  ...  $ Gd-157 (σ_abs ≈ 2.54×10⁵ barn, depletes slowly)
64155.70c  ...  $ Gd-155 (σ_abs ≈ 6.1×10⁴ barn, depletes)
```

**Medium absorbers**:
```mcnp
47109.70c  ...  $ Ag-109 (control rod material, if present)
61147.70c  ...  $ Pm-147 (β⁻ emitter, precursor)
61148.70c  ...  $ Pm-148 (β⁻ emitter)
61149.70c  ...  $ Pm-149 (precursor to Sm-149)
63151.70c  ...  $ Eu-151 (σ_abs ≈ 9,000 barn)
63153.70c  ...  $ Eu-153 (σ_abs ≈ 312 barn)
```

**Stable fission products** (for mass balance):
```mcnp
42095.70c  ...  $ Mo-95 (stable, high yield)
44101.70c  ...  $ Ru-101 (stable)
55133.70c  ...  $ Cs-133 (stable, high yield)
60143.70c  ...  $ Nd-143 (stable)
60145.70c  ...  $ Nd-145 (stable)
```

**Why these**:
- Xe-135: Equilibrium poison, huge cross-section, load-following transients
- Sm-149: Equilibrium + residual poison, doesn't decay, builds up
- Gd: Ultra-strong absorbers, used in burnable poisons
- Stable FPs: ~30-40% of fission products, affect spectrum

**Reactivity impact**: Fission products cause ~3000-5000 pcm negative reactivity after equilibrium

---

## COMPREHENSIVE ISOTOPE SET (40-60 isotopes)

### Extended Actinides (Add 6 more)

```mcnp
94242.70c  ...  $ Pu-242 (from Pu-241 capture, minor actinide)
95241.70c  ...  $ Am-241 (from Pu-241 decay, strong absorber)
95242.70c  ...  $ Am-242 (short-lived, from Am-241 capture)
95243.70c  ...  $ Am-243 (from Am-242 capture)
96242.70c  ...  $ Cm-242 (from Pu-241 beta decay, alpha emitter)
96244.70c  ...  $ Cm-244 (from Cm-242 capture chain, heat source)
```

**Why**:
- Am-241: Builds from Pu-241 decay (14.4 yr half-life), strong absorber
- Cm-242/244: Heat sources for spent fuel, important for decay heat
- Pu-242: Minor actinide, small but measurable impact

### Extended Fission Products (Add 20-30 more)

**Noble gases** (for release analysis):
```mcnp
36083.70c  ...  $ Kr-83 (stable, high yield)
54131.70c  ...  $ Xe-131 (stable, high yield)
54133.70c  ...  $ Xe-133 (radioactive, 5.2 day, release monitor)
```

**Absorbers**:
```mcnp
43099.70c  ...  $ Tc-99 (long-lived, absorber)
45103.70c  ...  $ Rh-103 (stable, moderate σ)
45105.70c  ...  $ Rh-105 (radioactive)
46105.70c  ...  $ Pd-105 (stable)
46107.70c  ...  $ Pd-107 (stable)
46108.70c  ...  $ Pd-108 (stable)
```

**High-yield stable isotopes**:
```mcnp
40093.70c  ...  $ Zr-93 (stable, cladding activation)
50117.70c  ...  $ Sn-117 (stable)
52130.70c  ...  $ Te-130 (stable)
56138.70c  ...  $ Ba-138 (stable, high yield)
57139.70c  ...  $ La-139 (stable)
58140.70c  ...  $ Ce-140 (stable, highest single FP yield ~6%)
59141.70c  ...  $ Pr-141 (stable)
```

**Why**:
- Better mass balance (track 60-70% of FP inventory)
- Activation products for dose calculations
- Release fractions for safety analysis

---

## BURNUP CALCULATION SETUP EXAMPLE

### Fresh Fuel (BOL)

```mcnp
c ========================================================================
c Material 1: Fresh UO2 fuel, 4.5% enriched
c ========================================================================
M1   92234.70c  3.6e-4   $ U-234 (~0.8% of U-235 content)
     92235.70c  0.045    $ U-235 (enrichment)
     92238.70c  0.955    $ U-238 (balance)
      8016.70c  2.0      $ O-16 (stoichiometric)
c Cell card:
1    1  -10.4  -1  IMP:N=1  TMP=8.62e-8  VOL=1000.0  $ Specify volume for tallies
```

**Key points**:
- VOL card REQUIRED for depletion tallies (normalize flux per unit volume)
- Only initial composition specified
- Depletion code (ORIGEN, CINDER) adds tracked isotopes

### Mid-Burnup Fuel (30 GWd/MTU)

**After depletion calculation**:
```mcnp
c ========================================================================
c Material 2: Depleted UO2 fuel at 30 GWd/MTU
c ========================================================================
M2   92234.70c  2.1e-4   $ U-234 (depleted)
     92235.70c  0.010    $ U-235 (depleted from 4.5%)
     92236.70c  0.0051   $ U-236 (built up from U-235 capture)
     92238.70c  0.9405   $ U-238 (slightly depleted)
     93237.70c  5.2e-4   $ Np-237 (from U-235 fission)
     94238.70c  2.1e-5   $ Pu-238
     94239.70c  0.0054   $ Pu-239 (bred from U-238)
     94240.70c  0.0024   $ Pu-240 (bred from Pu-239)
     94241.70c  0.0015   $ Pu-241 (bred from Pu-240)
     94242.70c  5.8e-4   $ Pu-242
     95241.70c  6.2e-5   $ Am-241 (from Pu-241 decay)
     54135.70c  1.2e-8   $ Xe-135 (equilibrium concentration)
     62149.70c  8.7e-9   $ Sm-149 (equilibrium + residual)
     64155.70c  3.1e-10  $ Gd-155
     64157.70c  2.4e-10  $ Gd-157
     42095.70c  6.8e-4   $ Mo-95 (stable FP)
     44101.70c  5.2e-4   $ Ru-101
     55133.70c  7.1e-4   $ Cs-133
     60143.70c  5.9e-4   $ Nd-143
     60145.70c  4.1e-4   $ Nd-145
      8016.70c  2.0      $ O-16 (constant)
c Cell card:
2    2  -10.1  -2  IMP:N=1  TMP=9.48e-8  VOL=1000.0
```

**Observations**:
- U-235 dropped from 4.5% → 1.0% (major depletion)
- Pu-239 built up to 0.54% (comparable to remaining U-235)
- Xe-135, Sm-149 at equilibrium (very small concentrations but huge cross-sections)
- Minor actinides (Np, Am) present at trace levels
- Stable FPs accumulating (mass balance)

---

## DEPLETION CALCULATION WORKFLOW

### Step 1: MCNP Neutron Transport

**Calculate neutron flux in depletion zones**:
```mcnp
c Tallies for depletion (one per depletion cell)
F4:N  (1 2 3 4 5 6 7 8 9 10)  $ Flux in each fuel pin
FM4   (-1 1 -6)                $ Total fission rate
SD4   1 10R                    $ Segment divisors (or use VOL card)
E4    1e-10 20                 $ Full energy range
```

**Output**: Neutron flux spectrum and reaction rates per cell

### Step 2: ORIGEN/CINDER Depletion

**Input to ORIGEN**:
- Flux spectrum from MCNP F4 tally
- One-group cross-sections (calculated from spectrum)
- Initial isotopic inventory
- Power level and time steps

**Calculation**:
- Solve Bateman equations for ~3000 isotopes
- Condense to tracked isotopes (~25-60)
- Output new composition at each time step

**Time steps** (typical PWR):
```
BOL → 1 day → 1 week → 1 month → 3 months → 6 months → 1 year → ...
Fine steps early (flux transients)
Coarser steps later (slow evolution)
```

### Step 3: Update MCNP Materials

**Replace material card with depleted composition**:
```bash
# Automated workflow (MOAA, VESTA, etc.)
mcnp6 i=input_BOL.i runtpe=BOL.r
extract_flux BOL.r → flux_spectrum.txt
origen < origen_input.txt > output.txt
extract_composition output.txt → depleted_material.m
update_input depleted_material.m → input_step2.i
mcnp6 i=input_step2.i runtpe=step2.r
# Repeat for multiple steps
```

### Step 4: Photon Transport (Shutdown Dose)

**At decay time t after shutdown**:
```mcnp
c Photon source from decaying isotopes (from ORIGEN output)
MODE P
SDEF  CEL=D1  ERG=D2  PAR=2
SI1  L  1 2 3 4 5       $ Source cells (fuel pins)
SP1     0.2 0.2 0.2 0.2 0.2  $ Cell probabilities
SI2  H  0.01 0.1 0.5 1.0 2.0 3.0  $ Photon energies [MeV]
SP2     0.0  0.35 0.28 0.22 0.10 0.05  $ Spectrum from ORIGEN
c Dose tally
F4:P  100                $ Detector cell
DE4   <ICRP energy bins>
DF4   <ICRP dose factors>
```

---

## ISOTOPE IMPORTANCE BY APPLICATION

### Criticality Safety

**Focus**: k-eff accuracy, minimal isotope set
```
Track: U-235, U-238, Pu-239, Pu-240, Pu-241
Skip: Minor actinides, most FPs (unless credit for burnup)
```

### Reactor Physics / Core Design

**Focus**: Reactivity coefficients, power distribution
```
Track: Full actinide chain (U-234→Cm-244)
       Strong FP absorbers (Xe-135, Sm-149, Gd-155/157)
       Stable FPs for spectrum effects
```

### Spent Fuel Characterization

**Focus**: Isotopic inventory for safeguards, waste
```
Track: All actinides (Pu vector, Am, Cm)
       Long-lived FPs (Tc-99, I-129, Cs-135/137, Sr-90)
       Heat-generating isotopes (Cs-137, Sr-90, Cm-244)
```

### Shutdown Dose Rate

**Focus**: Gamma/neutron sources after shutdown
```
Track: Co-60 (structure activation)
       Mn-54 (steel activation)
       Short-lived FPs (Ba-140, La-140, Ce-144)
       Actinides (alpha→n from Cm-244, Pu-240)
```

---

## VALIDATION

### Check Isotope Mass Balance

**Sum of all isotopes should equal total heavy metal**:
```
Σ(N_i × A_i) ≈ Initial heavy metal mass

Example: 1 kg UO2 @ 4.5% enrichment
Initial U: ~882 g
Final (after 30 GWd/MTU):
  U-235: ~88 g  (depleted)
  U-238: ~832 g (slightly depleted)
  Pu-239: ~47 g (bred)
  Pu-240: ~21 g
  Pu-241: ~13 g
  Minor actinides: ~5 g
  Fission products: ~35 g
  O-16: ~118 g (constant)
  Total: ~1159 g (includes FP mass)
```

**Fission product mass** ≈ Burnup × 0.95 g/GWd per kg initial HM

### Check Reactivity Evolution

**k-eff should decrease monotonically**:
```
BOL: k ≈ 1.30 (excess reactivity for burnup)
5 GWd/MTU: k ≈ 1.25
15 GWd/MTU: k ≈ 1.15 (Pu buildup compensates)
30 GWd/MTU: k ≈ 1.05
EOL: k ≈ 1.00 (critical, discharge)
```

**Non-monotonic behavior indicates**:
- Missing important isotope (Xe-135, Sm-149)
- Time step too coarse
- Flux spectrum mismatch (MCNP vs ORIGEN)

---

## BEST PRACTICES

1. **Start with minimum set** (20-25 isotopes), validate against measured data
2. **Add isotopes incrementally** if reactivity or mass balance errors >1%
3. **ALWAYS track Xe-135 and Sm-149** for thermal reactors (even if equilibrium assumption used)
4. **Track full Pu vector** (238-242) for burnup credit, safeguards
5. **Use fine time steps early** (first week), coarser later (after 1 month)
6. **Validate with measured data** (gamma spectroscopy, destructive assay) if available
7. **Document isotope selection** in input comments (why included/excluded)

---

## COMMON MISTAKES

### Mistake 1: Missing Xe-135 and Sm-149

**Impact**: k-eff 1000-3000 pcm too high
**Fix**: Always include equilibrium poisons

### Mistake 2: Incomplete Pu Chain

**Impact**: Underestimate Pu inventory, wrong spectrum
**Fix**: Track Pu-238 through Pu-242 minimum

### Mistake 3: Too Few FPs

**Impact**: Wrong neutron spectrum (too soft), reactivity error
**Fix**: Include at least 10 stable FPs for mass balance

### Mistake 4: Time Steps Too Coarse

**Impact**: Oscillating k-eff, unrealistic isotope concentrations
**Fix**: Use <1 week steps for first month, <1 month thereafter

---

## REFERENCES

**For depletion workflows**:
- MOAA (MCNP-ORIGEN Activation Automation): ORNL/TM-2018/1014
- VESTA: Verified, Efficient Simulation and Transport Analysis
- FISPACT-II: Inventory code for activation

**For isotope data**:
- JANIS: https://www.oecd-nea.org/janis/
- KAERI Table of Nuclides: https://atom.kaeri.re.kr/

**For fission yields**:
- ENDF/B-VIII.0 Fission Product Yields
- JEFF-3.3 Yield Library

**Integration**:
- mcnp-burnup-builder skill - Complete depletion setup
- mcnp-isotope-lookup skill - Find ZAIDs, cross-sections, yields

---

**Version:** 1.0
**Created:** 2025-11-08
**For:** mcnp-material-builder skill v2.0
