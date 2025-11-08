# Actinide Chains for Burnup Calculations
**Capture/Decay Pathways, Branching Ratios, and Tracking Requirements**

## Purpose

This reference provides comprehensive data on actinide production and destruction chains for MCNP burnup calculations, from U-234 through Cm-245. Includes minimum and extended tracking requirements based on burnup level and reactor type.

---

## Overview

### Production Mechanisms

**Neutron capture**: A + n → A+1 + γ

**Beta decay**: Neutron-rich nucleus → proton + electron + antineutrino

**Alpha decay**: Heavy nucleus → daughter + He-4

**Fission**: Heavy nucleus → 2 fission products + 2-3 neutrons + energy

### Chain Structure

```
U-234 → U-235 → U-236 → U-237 → Np-237 → Np-238 → Pu-238
                         ↓                          ↓
                      U-238 ─→ U-239 ─→ Np-239 ─→ Pu-239 ─→ Pu-240 ─→ Pu-241 ─→ Pu-242
                                  ↓         ↓        ↓         ↓         ↓         ↓
                               (β⁻)      (β⁻)    (fission) (fission)  Am-241  Am-242
                                                                         ↓         ↓
                                                                       Cm-242  Am-243
                                                                         ↓         ↓
                                                                       Pu-238  Cm-243
                                                                                 ↓
                                                                               Cm-244
```

---

## Minimum Actinide Set (7 isotopes)

**Use for**: Standard LWR burnup (<60 GWd/MTU), low-burnup research reactors

**Required isotopes**:

### U-234

**Nuclear Data**:
- ZAID: 92234
- Half-life: 245,500 years
- Decay mode: α to Th-230 (λ = 8.95×10⁻¹⁴ s⁻¹)

**Production**:
- Natural abundance in enriched uranium (0.01-0.03%)
- Pu-238 alpha decay (minor)

**Destruction**:
- (n,γ) → U-235 (σ_thermal = 100 barn)
- (n,f) fission (σ_thermal = 0.07 barn, negligible)
- Alpha decay (very slow, negligible during burnup)

**MCNP Material Card**:
```mcnp
   92234.70c  <density>  $ U-234
```

**Typical densities**:
- Fresh LEU (4.5%): 3.6×10⁻⁴ atoms/barn-cm
- Depleted fuel (60 GWd/MTU): 1.2×10⁻⁴ atoms/barn-cm (decreased via capture)

---

### U-235

**Nuclear Data**:
- ZAID: 92235
- Half-life: 704 million years
- Decay mode: α to Th-231 (negligible during burnup)

**Production**:
- Enrichment (natural 0.72% → 3-5% LEU, or 20% HEU, or 93% weapon-grade)
- U-234 (n,γ) (small contribution)

**Destruction**:
- (n,f) fission: σ_thermal = 585 barn **PRIMARY**
- (n,γ) → U-236: σ_thermal = 99 barn
- Ratio: 85% fission, 15% capture (thermal spectrum)

**MCNP Material Card**:
```mcnp
   92235.70c  <density>  $ U-235 (PRIMARY FISSILE)
```

**Typical densities**:
- Fresh LEU (4.5%): 4.5×10⁻² atoms/barn-cm (45% of total U)
- Depleted fuel (60 GWd/MTU): 8.0×10⁻³ atoms/barn-cm (depleted to 0.8%)

**Critical**: NEVER omit U-235

---

### U-236

**Nuclear Data**:
- ZAID: 92236
- Half-life: 23.4 million years
- Decay mode: α (negligible)

**Production**:
- U-235 (n,γ) **PRIMARY**
- Small amount in fresh fuel from enrichment process

**Destruction**:
- (n,γ) → U-237: σ_thermal = 5.2 barn
- (n,f) fission: σ_thermal = 0.07 barn (negligible)

**MCNP Material Card**:
```mcnp
   92236.70c  <density>  $ U-236 (capture product)
```

**Typical densities**:
- Fresh LEU: 2.1×10⁻⁶ atoms/barn-cm (trace from enrichment)
- Depleted fuel (60 GWd/MTU): 5.0×10⁻³ atoms/barn-cm (built up from U-235 captures)

---

### U-238

**Nuclear Data**:
- ZAID: 92238
- Half-life: 4.47 billion years
- Decay mode: α (negligible)

**Production**:
- Natural uranium (99.3%)
- Depletes slightly via fission and capture

**Destruction**:
- (n,γ) → U-239: σ_thermal = 2.7 barn **PRIMARY** (Pu production)
- (n,f) fission: σ_fast = 0.5 barn (fast fission, ~5% of fissions)
- Fast/(Fast+Thermal) fission ratio important for Pu production

**MCNP Material Card**:
```mcnp
   92238.70c  <density>  $ U-238 (FERTILE, Pu breeding)
```

**Typical densities**:
- Fresh LEU (4.5%): 9.55×10⁻¹ atoms/barn-cm (95.5% of U)
- Depleted fuel: 9.40×10⁻¹ atoms/barn-cm (decreased ~1-2% from fission/capture)

**Critical**: Source of Pu-239 (bred fissile)

---

### Np-237

**Nuclear Data**:
- ZAID: 93237
- Half-life: 2.14 million years
- Decay mode: α to Pa-233

**Production**:
- U-237 (β⁻, 6.75 day) from U-236 (n,γ)
- Am-241 (n,2n) (minor)

**Destruction**:
- (n,γ) → Np-238: σ_thermal = 175 barn
- (n,f) fission: σ_thermal = 0.02 barn (negligible)

**Reaction chain**:
```
U-236 + n → U-237 (6.75 day β⁻) → Np-237
```

**MCNP Material Card**:
```mcnp
   93237.70c  <density>  $ Np-237 (from U-237 decay)
```

**Typical densities**:
- Fresh fuel: 0 (no Np initially)
- Depleted fuel (60 GWd/MTU): 6.0×10⁻⁴ atoms/barn-cm

**Note**: Include U-237 if tracking short-lived precursors

---

### Pu-239

**Nuclear Data**:
- ZAID: 94239
- Half-life: 24,110 years
- Decay mode: α to U-235

**Production**:
- U-238 (n,γ) → U-239 (β⁻, 23.5 min) → Np-239 (β⁻, 2.36 day) → Pu-239 **PRIMARY**

**Destruction**:
- (n,f) fission: σ_thermal = 748 barn **FISSILE**
- (n,γ) → Pu-240: σ_thermal = 271 barn
- Ratio: 73% fission, 27% capture

**Reaction chain**:
```
U-238 + n → U-239 (23.5 min β⁻) → Np-239 (2.36 day β⁻) → Pu-239
```

**MCNP Material Card**:
```mcnp
   94239.70c  <density>  $ Pu-239 (BRED FISSILE)
```

**Typical densities**:
- Fresh fuel: 0 (no Pu initially)
- Depleted fuel (60 GWd/MTU): 6.0×10⁻³ atoms/barn-cm (replaces depleted U-235)

**Critical**: Major bred fissile isotope, essential for burnup

---

### Pu-240

**Nuclear Data**:
- ZAID: 94240
- Half-life: 6,561 years
- Decay mode: α to U-236

**Production**:
- Pu-239 (n,γ) **PRIMARY**

**Destruction**:
- (n,γ) → Pu-241: σ_thermal = 290 barn
- (n,f) fission: σ_thermal = 0.06 barn (negligible, NOT fissile)
- Spontaneous fission (neutron source, important for safeguards)

**MCNP Material Card**:
```mcnp
   94240.70c  <density>  $ Pu-240 (from Pu-239 capture)
```

**Typical densities**:
- Fresh fuel: 0
- Depleted fuel (60 GWd/MTU): 3.0×10⁻³ atoms/barn-cm

**Note**: Spontaneous fission neutron source (important for subcriticality monitoring)

---

### Pu-241

**Nuclear Data**:
- ZAID: 94241
- Half-life: 14.3 years
- Decay mode: β⁻ to Am-241 (λ = 1.54×10⁻⁹ s⁻¹)

**Production**:
- Pu-240 (n,γ) **PRIMARY**

**Destruction**:
- (n,f) fission: σ_thermal = 1,011 barn **FISSILE**
- (n,γ) → Pu-242: σ_thermal = 363 barn
- β⁻ decay to Am-241 (14.3 yr, important during cooling)

**MCNP Material Card**:
```mcnp
   94241.70c  <density>  $ Pu-241 (FISSILE, decays to Am-241)
```

**Typical densities**:
- Fresh fuel: 0
- Depleted fuel (60 GWd/MTU): 2.0×10⁻³ atoms/barn-cm
- After 10 years cooling: 1.3×10⁻³ (decayed ~35%)

**Critical**: Decays to Am-241 (strong neutron absorber), important for spent fuel

---

## Extended Actinide Set (16 isotopes)

**Use for**: High burnup (>60 GWd/MTU), MOX fuel, multiple recycles, long irradiation

**Add these to minimum set**:

### Pu-238

**Nuclear Data**:
- ZAID: 94238
- Half-life: 87.7 years
- Decay mode: α to U-234

**Production**:
- Cm-242 (α, 163 day) **PRIMARY**
- Np-238 (β⁻, 2.1 day) from Np-237 (n,γ)

**Destruction**:
- (n,f) fission: σ_thermal = 18 barn (fissile)
- (n,γ) → Pu-239: σ_thermal = 560 barn
- Alpha decay (87.7 yr, heat source)

**MCNP Material Card**:
```mcnp
   94238.70c  <density>  $ Pu-238 (heat source, from Cm-242 α)
```

**Typical densities**:
- Fresh fuel: 0
- High burnup (80 GWd/MTU): 2.3×10⁻⁵ atoms/barn-cm

**Note**: Major heat source (560 W/kg), important for decay heat

---

### Pu-242

**Nuclear Data**:
- ZAID: 94242
- Half-life: 375,000 years
- Decay mode: α to U-238

**Production**:
- Pu-241 (n,γ) **PRIMARY**

**Destruction**:
- (n,γ) → Pu-243: σ_thermal = 19 barn
- (n,f) fission: σ_thermal = 0.001 barn (negligible)

**MCNP Material Card**:
```mcnp
   94242.70c  <density>  $ Pu-242 (from Pu-241 capture)
```

**Typical densities**:
- Depleted fuel (60 GWd/MTU): 8.0×10⁻⁴ atoms/barn-cm
- High burnup (80 GWd/MTU): 2.0×10⁻³ atoms/barn-cm

---

### Am-241

**Nuclear Data**:
- ZAID: 95241
- Half-life: 432 years
- Decay mode: α to Np-237

**Production**:
- Pu-241 (β⁻, 14.3 yr) **PRIMARY** (during cooling)
- Pu-240 (n,γ) → Pu-241 → Am-241 (chain)

**Destruction**:
- (n,γ) → Am-242m/Am-242: σ_thermal = 684 barn **STRONG ABSORBER**
- (n,f) fission: σ_thermal = 3.1 barn
- Alpha decay (432 yr)

**MCNP Material Card**:
```mcnp
   95241.70c  <density>  $ Am-241 (from Pu-241 decay, STRONG ABSORBER)
```

**Typical densities**:
- Fresh fuel: 0
- Depleted fuel immediately after discharge: ~0 (Pu-241 hasn't decayed yet)
- After 10 years cooling: 1.0×10⁻⁴ atoms/barn-cm (from Pu-241 decay)

**Critical**: Builds up during storage, major absorber penalty for spent fuel recycling

---

### Am-242m (Metastable)

**Nuclear Data**:
- ZAID: 95242 or 95642 (metastable)
- Half-life: 141 years (metastable state)
- Decay modes: Internal transition to Am-242 (99.5%), α to Np-238 (0.5%)

**Production**:
- Am-241 (n,γ) → Am-242m (metastable) + Am-242 (ground state)
- Branching ratio: ~10% metastable, 90% ground state

**Destruction**:
- (n,f) fission: σ_thermal = 6,400 barn **HIGHLY FISSILE**
- (n,γ): σ_thermal = 200 barn
- Internal transition to Am-242 (ground state, 16 hr)

**MCNP Material Card**:
```mcnp
   95642.70c  <density>  $ Am-242m (metastable, fissile)
```

**Note**: Sometimes tracked as separate isotope, sometimes lumped with Am-242

---

### Am-243

**Nuclear Data**:
- ZAID: 95243
- Half-life: 7,370 years
- Decay mode: α to Np-239

**Production**:
- Am-242 (n,γ)
- Pu-242 (n,γ) → Pu-243 (β⁻, 5 hr) → Am-243

**Destruction**:
- (n,γ) → Am-244: σ_thermal = 75 barn
- (n,f) fission: σ_thermal = 0.2 barn

**MCNP Material Card**:
```mcnp
   95243.70c  <density>  $ Am-243
```

**Typical densities**:
- High burnup (80 GWd/MTU): 2.0×10⁻⁵ atoms/barn-cm

---

### Cm-242

**Nuclear Data**:
- ZAID: 96242
- Half-life: 162.8 days
- Decay mode: α to Pu-238 (major heat source)

**Production**:
- Am-241 (n,γ) → Am-242 (β⁻, 16 hr) → Cm-242

**Destruction**:
- (n,γ) → Cm-243: σ_thermal = 16 barn
- Alpha decay to Pu-238 (163 day, **PRIMARY**)
- Spontaneous fission (neutron source)

**MCNP Material Card**:
```mcnp
   96242.70c  <density>  $ Cm-242 (α → Pu-238, heat)
```

**Decay chain**:
```
Am-241 + n → Am-242 (16 hr β⁻) → Cm-242 (163 day α) → Pu-238
```

**Typical densities**:
- Immediately after discharge: 1.5×10⁻⁶ atoms/barn-cm
- After 2 years cooling: ~0 (decayed to Pu-238)

---

### Cm-243

**Nuclear Data**:
- ZAID: 96243
- Half-life: 29.1 years
- Decay mode: α to Pu-239

**Production**:
- Pu-242 (n,γ) → Pu-243 (β⁻, 5 hr) → Am-243 (n,γ) → Am-244 (β⁻, 10 hr) → Cm-244
- Cm-242 (n,γ)

**Destruction**:
- (n,γ) → Cm-244: σ_thermal = 130 barn
- (n,f) fission: σ_thermal = 617 barn (fissile)
- Alpha decay (29.1 yr)

**MCNP Material Card**:
```mcnp
   96243.70c  <density>  $ Cm-243 (fissile)
```

---

### Cm-244

**Nuclear Data**:
- ZAID: 96244
- Half-life: 18.1 years
- Decay mode: α to Pu-240 (major heat source)

**Production**:
- Cm-243 (n,γ) **PRIMARY**
- Am-243 (n,γ) → Am-244 (β⁻, 10 hr) → Cm-244

**Destruction**:
- (n,γ) → Cm-245: σ_thermal = 16 barn
- Alpha decay (18.1 yr, **MAJOR HEAT SOURCE**, 2.8 W/g)
- Spontaneous fission (major neutron source)

**MCNP Material Card**:
```mcnp
   96244.70c  <density>  $ Cm-244 (heat, neutron source)
```

**Typical densities**:
- High burnup (80 GWd/MTU): 8.0×10⁻⁶ atoms/barn-cm

**Critical**: Dominant decay heat source at 10-100 years, spontaneous fission neutron source

---

### Cm-245

**Nuclear Data**:
- ZAID: 96245
- Half-life: 8,500 years
- Decay mode: α to Pu-241

**Production**:
- Cm-244 (n,γ)

**Destruction**:
- (n,f) fission: σ_thermal = 2,145 barn **HIGHLY FISSILE**
- (n,γ): σ_thermal = 383 barn

**MCNP Material Card**:
```mcnp
   96245.70c  <density>  $ Cm-245 (highly fissile)
```

**Note**: Usually negligible, include for completeness in very high burnup

---

## Actinide Tracking by Reactor Type

### PWR/BWR (LEU, <60 GWd/MTU)

**Minimum** (7 isotopes):
```mcnp
   92234.70c
   92235.70c
   92236.70c
   92238.70c
   93237.70c
   94239.70c
   94240.70c
   94241.70c
```

**Recommended** (10 isotopes, add):
```mcnp
   94242.70c  $ Pu-242
   95241.70c  $ Am-241 (for spent fuel storage)
```

### High-Burnup LWR (>60 GWd/MTU)

**Extended** (14 isotopes, add):
```mcnp
   94238.70c  $ Pu-238 (decay heat)
   96242.70c  $ Cm-242 → Pu-238
   95243.70c  $ Am-243
   96244.70c  $ Cm-244 (decay heat, neutron source)
```

### MOX Fuel (Pu-based)

**Extended+** (16 isotopes, all above plus):
```mcnp
   95242.70c  $ Am-242/Am-242m
   96243.70c  $ Cm-243
```

### Fast Reactor (SFR, high Pu content)

**Complete** (all 16+ isotopes):
- Fast spectrum enhances (n,2n) and (n,f) reactions
- Higher actinides more important
- Include Cm-245, Cm-246 for completeness

### Research Reactor (HEU fuel)

**Minimum** (6 isotopes, can omit Pu chain):
```mcnp
   92234.70c
   92235.70c
   92236.70c
   92238.70c
   93237.70c
   94239.70c  $ Small Pu production from U-238
```

---

## Important Decay Chains

### Pu-238 Production Chain

```
Np-237 + n → Np-238 (2.1 d β⁻) → Pu-238
             OR
Am-241 + n → Am-242 (16 hr β⁻) → Cm-242 (163 d α) → Pu-238
```

**Must track**: Np-237, Am-241, Cm-242 to get correct Pu-238

### Am-241 Production Chain

```
Pu-239 + n → Pu-240 + n → Pu-241 (14.3 yr β⁻) → Am-241
```

**Time-dependent**: Am-241 builds up during storage, not during irradiation

**Important**: If analyzing spent fuel after 5-20 years cooling, Am-241 is major absorber

### Cm-244 Production Chain

```
Pu-241 + n → Pu-242 + n → Pu-243 (5 hr β⁻) → Am-243 + n → Am-244 (10 hr β⁻) → Cm-244
```

**Must track**: Pu-242, Am-243 to get correct Cm-244

**Importance**: Cm-244 dominates decay heat at 10-100 years post-discharge

---

## Validation Checks

### Plutonium Vector

**Pu isotopic composition** (mass fractions):
```
Typical PWR (45 GWd/MTU):
  Pu-238: 1-2%
  Pu-239: 55-60%
  Pu-240: 23-26%
  Pu-241: 11-14%
  Pu-242: 4-6%
```

**Check**: Sum should be 100%, Pu-239 dominant

### Heavy Metal Mass Balance

```python
# Total HM approximately constant
HM_initial = sum([N_U234, N_U235, N_U238]) × A_U
HM_final = sum([all U, Pu, Np, Am, Cm]) × A_avg - fission_mass

ratio = HM_final / HM_initial
print(f"HM mass ratio: {ratio:.3f}")
# Should be 0.95-0.98 (some mass lost to fission products and neutrons)
```

### Fissile Inventory

```python
# Track fissile isotopes
fissile_BOL = N_U235_initial
fissile_EOL = N_U235 + N_Pu239 + N_Pu241 + N_Am242m + N_Cm243 + N_Cm245

# Fissile bred from fertile
fissile_bred = N_Pu239 + N_Pu241
print(f"Fissile bred/consumed ratio: {fissile_bred / (fissile_BOL - N_U235):.3f}")
# Typical PWR: 0.6-0.8 (60-80% of consumed U-235 replaced by Pu)
```

---

## MCNP Material Card Templates

### Fresh LEU Fuel (4.5% U-235)

```mcnp
m1  $ Fresh UO2, 4.5% enriched
   92234.70c  3.6e-4   $ Natural in enriched U
   92235.70c  0.045    $ Enrichment
   92236.70c  2.1e-6   $ Trace from enrichment
   92238.70c  0.955    $ Balance
    8016.70c  2.0      $ Oxygen
```

### Depleted LEU (after 3 cycles, 60 GWd/MTU)

```mcnp
m1  $ Depleted UO2, extended actinide tracking
c Uranium
   92234.70c  1.2e-4
   92235.70c  0.008
   92236.70c  0.005
   92238.70c  0.940
c Plutonium
   94238.70c  2.3e-5
   94239.70c  0.006
   94240.70c  0.003
   94241.70c  0.002
   94242.70c  8.0e-4
c Minor actinides
   93237.70c  6.0e-4
   95241.70c  1.0e-4
   95243.70c  2.0e-5
   96242.70c  1.5e-6
   96244.70c  8.0e-6
c Oxygen
    8016.70c  2.0
```

### MOX Fuel (fresh)

```mcnp
m2  $ Fresh MOX, 7% Pu
c Uranium (depleted)
   92234.70c  5.0e-6
   92235.70c  0.002    $ 0.2% U-235
   92236.70c  1.0e-6
   92238.70c  0.928    $ Balance
c Plutonium (7% Pu, typical vector)
   94238.70c  1.4e-3   $ 2% of Pu
   94239.70c  3.9e-2   $ 56% of Pu
   94240.70c  1.8e-2   $ 26% of Pu
   94241.70c  8.4e-3   $ 12% of Pu
   94242.70c  2.8e-3   $ 4% of Pu
c Minor actinides
   95241.70c  2.0e-3   $ From Pu-241 in feed
c Oxygen
    8016.70c  2.0
```

---

## References

- ENDF/B-VIII.0 decay and fission yield data
- OECD/NEA burnup credit benchmark specifications
- SCALE ORIGEN-S actinide library
- IAEA TECDOC-1013: Spent fuel composition database
- "Physics of Nuclear Reactors" by Weston Stacey
