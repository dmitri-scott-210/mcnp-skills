# Fission Product Database for Burnup Calculations
**Complete Properties, Cross-Sections, and Selection Criteria**

## Purpose

This database provides comprehensive data on fission product isotopes for MCNP burnup calculations, organized by importance tier (1-4) based on neutron absorption cross-sections, decay heat, and dose rate contributions.

---

## Classification System

### TIER 1: ALWAYS Include (Strong Neutron Absorbers)

**Definition**: σ_thermal > 10,000 barn OR critical for reactivity

**Usage**: MUST be included in all reactor burnup calculations

**Count**: 7 isotopes

### TIER 2: SHOULD Include (Significant Absorbers)

**Definition**: σ_thermal > 100 barn OR important for dose rates

**Usage**: Include for accurate reactivity predictions

**Count**: 6-10 isotopes

### TIER 3: MAY Include (Decay Heat/Dose Sources)

**Definition**: Important β/γ emitters for shutdown dose and decay heat

**Usage**: Include if decay heat or dose rate calculations needed

**Count**: 10-20 isotopes

### TIER 4: Optional (Completeness)

**Definition**: Stable or long-lived FPs with moderate yields

**Usage**: Include for high-fidelity burnup (research, benchmarking)

**Count**: 20+ isotopes

---

## TIER 1: Critical Fission Products

### Xe-135 (Xenon-135)

**Nuclear Data**:
- ZAID: 54135
- Half-life: 9.14 hours
- Decay mode: β⁻ to Cs-135
- Fission yield (U-235 thermal): 6.3%
- Precursor: I-135 (6.57 hr half-life, 6.3% yield)

**Cross-Sections**:
- σ_thermal (0.0253 eV): 2.65×10⁶ barn (2.65 Mbarn)
- σ_epithermal (resonance integral): 8×10⁵ barn
- σ_fast (1 MeV): ~0.1 barn

**Reactivity Impact**:
- Peak xenon: ~9 hours after shutdown (I-135 decay → Xe-135 buildup)
- Equilibrium xenon worth: -2000 to -3000 pcm (typical PWR)
- Xenon oscillations in large cores (spatial instability)

**Burnup Behavior**:
- Builds up rapidly during operation (hours)
- Equilibrium: production = destruction + decay
- After shutdown: peaks at ~9 hr, then decays to zero by ~3 days

**MCNP Material Card**:
```mcnp
   54135.70c  <density>  $ Xe-135 (equilibrium or time-dependent)
```

**Critical Notes**:
- NEVER omit Xe-135 from fuel burnup calculations
- Use BURN card with fine time steps (<12 hr) during startup/shutdown
- Equilibrium density: N_Xe = (γ_Xe × Σ_f × φ) / (λ_Xe + σ_Xe × φ)

---

### Sm-149 (Samarium-149)

**Nuclear Data**:
- ZAID: 62149
- Half-life: Stable
- Fission yield (U-235 thermal): 1.1% direct + Pm-149 decay
- Precursor: Pm-149 (2.21 day half-life, 1.1% yield)

**Cross-Sections**:
- σ_thermal (0.0253 eV): 40,140 barn (40.1 kbarn)
- σ_epithermal (resonance integral): 3,360 barn
- σ_fast (1 MeV): ~2 barn

**Reactivity Impact**:
- Equilibrium Sm-149 worth: -600 to -1200 pcm (typical PWR)
- Builds up over weeks to months
- Permanent poison (stable, doesn't decay)

**Burnup Behavior**:
- Indirect production: Nd-149 (β⁻, 1.73 hr) → Pm-149 (β⁻, 2.21 day) → Sm-149
- Equilibrium: production from Pm-149 decay = destruction by (n,γ)
- After shutdown: continues to build for ~2 weeks (Pm-149 decay)

**MCNP Material Card**:
```mcnp
   62149.70c  <density>  $ Sm-149 (CRITICAL ABSORBER)
```

**Critical Notes**:
- Second most important fission product (after Xe-135)
- Omitting Sm-149 causes 1000-2000 pcm error in k_eff
- Include Pm-149 as precursor (if using detailed FP tracking)

---

### Sm-151 (Samarium-151)

**Nuclear Data**:
- ZAID: 62151
- Half-life: 90 years
- Decay mode: β⁻ to Eu-151
- Cumulative fission yield: ~0.5%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 15,000 barn (15 kbarn)
- σ_epithermal (resonance integral): 3,000 barn

**Reactivity Impact**:
- Modest reactivity worth: -100 to -300 pcm
- Builds up slowly over multiple cycles

**MCNP Material Card**:
```mcnp
   62151.70c  <density>  $ Sm-151 (long-lived absorber)
```

---

### Gd-155 (Gadolinium-155)

**Nuclear Data**:
- ZAID: 64155
- Half-life: Stable
- Cumulative fission yield: ~0.03%
- Production: primarily from Eu-155 decay

**Cross-Sections**:
- σ_thermal (0.0253 eV): 60,900 barn (61 kbarn)
- σ_epithermal (resonance integral): 1,560 barn

**Reactivity Impact**:
- Small direct fission yield, but high cross-section
- Buildup from Eu-155 decay important at high burnup
- Worth: -50 to -200 pcm (depending on burnup)

**MCNP Material Card**:
```mcnp
   64155.70c  <density>  $ Gd-155 (from Eu-155 decay)
```

---

### Gd-157 (Gadolinium-157)

**Nuclear Data**:
- ZAID: 64157
- Half-life: Stable
- Cumulative fission yield: ~0.02%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 254,000 barn (254 kbarn) **HIGHEST**
- σ_epithermal (resonance integral): 7,800 barn

**Reactivity Impact**:
- Strongest known thermal neutron absorber
- Small fission yield, but extreme cross-section
- Worth: -20 to -100 pcm

**MCNP Material Card**:
```mcnp
   64157.70c  <density>  $ Gd-157 (STRONGEST ABSORBER)
```

**Critical Notes**:
- Often used in burnable absorbers (Gd₂O₃ mixed with UO₂)
- Include if Gd used as burnable poison OR for completeness

---

### Pm-147 (Promethium-147)

**Nuclear Data**:
- ZAID: 61147
- Half-life: 2.62 years
- Decay mode: β⁻ to Sm-147 (σ_thermal = 57 barn, low)
- Cumulative fission yield: ~2.3%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 168 barn
- Decays to Sm-147 (low absorption)

**Reactivity Impact**:
- Direct absorption: small
- Decay product (Sm-147): also low absorption
- Worth: ~-10 pcm

**MCNP Material Card**:
```mcnp
   61147.70c  <density>  $ Pm-147 (decays to Sm-147)
```

**Critical Notes**:
- Include for completeness (moderate yield)
- Important for decay heat calculations

---

### Pm-149 (Promethium-149)

**Nuclear Data**:
- ZAID: 61149
- Half-life: 2.21 days
- Decay mode: β⁻ to Sm-149 (σ_thermal = 40 kbarn)
- Cumulative fission yield: ~1.1%

**Cross-Sections**:
- σ_thermal (0.0253 eV): ~2,000 barn
- Decays to Sm-149 (STRONG absorption)

**Reactivity Impact**:
- Precursor to Sm-149 (critical)
- Worth: Indirect via Sm-149 production

**MCNP Material Card**:
```mcnp
   61149.70c  <density>  $ Pm-149 → Sm-149 (CRITICAL CHAIN)
```

**Critical Notes**:
- MUST include if tracking Sm-149 buildup accurately
- Important during shutdown (Pm-149 decay → Sm-149 increase)

---

## TIER 2: Significant Fission Products

### Cd-113 (Cadmium-113)

**Nuclear Data**:
- ZAID: 48113
- Half-life: Stable
- Cumulative fission yield: ~0.01%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 20,600 barn (20.6 kbarn)
- σ_epithermal (resonance integral): 320 barn

**Reactivity Impact**: -20 to -50 pcm

**MCNP Material Card**:
```mcnp
   48113.70c  <density>  $ Cd-113 (strong absorber)
```

---

### Eu-153 (Europium-153)

**Nuclear Data**:
- ZAID: 63153
- Half-life: Stable
- Cumulative fission yield: ~0.1%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 312 barn
- σ_epithermal (resonance integral): 1,400 barn

**Reactivity Impact**: -10 to -30 pcm

**MCNP Material Card**:
```mcnp
   63153.70c  <density>  $ Eu-153
```

---

### Eu-155 (Europium-155)

**Nuclear Data**:
- ZAID: 63155
- Half-life: 4.76 years
- Decay mode: β⁻ to Gd-155 (σ_thermal = 61 kbarn)
- Cumulative fission yield: ~0.03%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 3,760 barn (3.76 kbarn)
- Decays to Gd-155 (strong absorber)

**Reactivity Impact**: -20 to -80 pcm (including Gd-155 daughter)

**MCNP Material Card**:
```mcnp
   63155.70c  <density>  $ Eu-155 → Gd-155 (important chain)
```

---

### Rh-103 (Rhodium-103)

**Nuclear Data**:
- ZAID: 45103
- Half-life: Stable
- Cumulative fission yield: ~3.0%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 150 barn
- σ_epithermal (resonance integral): 1,100 barn

**Reactivity Impact**: -50 to -150 pcm

**MCNP Material Card**:
```mcnp
   45103.70c  <density>  $ Rh-103
```

---

### Tc-99 (Technetium-99)

**Nuclear Data**:
- ZAID: 43099
- Half-life: 211,000 years (essentially stable)
- Cumulative fission yield: ~6.1%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 20 barn
- σ_epithermal (resonance integral): 350 barn

**Reactivity Impact**: -20 to -60 pcm (high yield compensates for low cross-section)

**MCNP Material Card**:
```mcnp
   43099.70c  <density>  $ Tc-99 (long-lived)
```

**Environmental Note**: Long-lived radionuclide, important for waste disposal

---

### Cs-133 (Cesium-133)

**Nuclear Data**:
- ZAID: 55133
- Half-life: Stable
- Cumulative fission yield: ~6.7%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 30 barn
- σ_epithermal (resonance integral): 420 barn

**Reactivity Impact**: -30 to -100 pcm (high yield)

**MCNP Material Card**:
```mcnp
   55133.70c  <density>  $ Cs-133 (stable)
```

---

## TIER 3: Decay Heat and Dose Sources

### Cs-137 (Cesium-137)

**Nuclear Data**:
- ZAID: 55137
- Half-life: 30.17 years
- Decay mode: β⁻ to Ba-137m (γ emitter, 661.7 keV)
- Cumulative fission yield: ~6.2%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 0.25 barn (negligible absorption)

**Decay Heat Contribution**: Major (10-20% of total at 1 year post-shutdown)

**Dose Rate**: Dominant γ source (661.7 keV) for 10-300 years

**MCNP Material Card**:
```mcnp
   55137.70c  <density>  $ Cs-137 (MAJOR DOSE SOURCE)
```

**Critical Notes**:
- Essential for shutdown dose rate calculations
- Include if photon transport or decay heat needed
- Negligible neutron absorption

---

### Sr-90 (Strontium-90)

**Nuclear Data**:
- ZAID: 38090
- Half-life: 28.8 years
- Decay mode: β⁻ to Y-90 (β⁻, 64 hr) → Zr-90
- Cumulative fission yield: ~5.8%

**Cross-Sections**:
- σ_thermal (0.0253 eV): 0.8 barn (negligible)

**Decay Heat Contribution**: Major (5-10% at 1 year)

**Dose Rate**: β source, minimal γ (bremsstrahlung only)

**MCNP Material Card**:
```mcnp
   38090.70c  <density>  $ Sr-90 (decay heat)
```

---

### Additional Tier 3 Isotopes

**Ba-140** (12.8 day, γ source):
```mcnp
   56140.70c  <density>  $ Ba-140 (short-term dose)
```

**La-140** (1.68 day, strong γ):
```mcnp
   57140.70c  <density>  $ La-140 (shutdown dose)
```

**Ce-141** (32.5 day):
```mcnp
   58141.70c  <density>  $ Ce-141
```

**Pr-143** (13.6 day):
```mcnp
   59143.70c  <density>  $ Pr-143
```

**I-131** (8.02 day, medical/environmental):
```mcnp
   53131.70c  <density>  $ I-131 (thyroid hazard)
```

**Ru-106** (1.02 yr, β/γ):
```mcnp
   44106.70c  <density>  $ Ru-106
```

---

## TIER 4: Stable/Completeness Isotopes

### Noble Gases (Stable, Released in Accidents)

**Kr-83**:
```mcnp
   36083.70c  <density>  $ Kr-83 (stable noble gas)
```

**Xe-131**:
```mcnp
   54131.70c  <density>  $ Xe-131 (stable)
```

**Xe-133** (5.2 day, dose):
```mcnp
   54133.70c  <density>  $ Xe-133 (environmental dose)
```

### Stable High-Yield Isotopes

**Mo-95**:
```mcnp
   42095.70c  <density>  $ Mo-95 (stable, 6.5% yield)
```

**Ru-101**:
```mcnp
   44101.70c  <density>  $ Ru-101 (stable, 5.1% yield)
```

**Nd-143**:
```mcnp
   60143.70c  <density>  $ Nd-143 (stable, 5.9% yield)
```

**Nd-145**:
```mcnp
   60145.70c  <density>  $ Nd-145 (stable, 3.9% yield)
```

**Zr-93** (1.5 Myr, burnup monitor):
```mcnp
   40093.70c  <density>  $ Zr-93 (very long-lived)
```

---

## Fission Product Selection by Application

### Reactivity-Only Calculations

**Minimum set** (7 isotopes):
```mcnp
c TIER 1 only (strong absorbers)
   54135.70c  <Xe-135>
   62149.70c  <Sm-149>
   62151.70c  <Sm-151>
   64155.70c  <Gd-155>
   64157.70c  <Gd-157>
   61147.70c  <Pm-147>
   61149.70c  <Pm-149>
```

**Recommended set** (15 isotopes, add Tier 2):
```mcnp
c TIER 1 + TIER 2
   [... Tier 1 above ...]
   48113.70c  <Cd-113>
   63153.70c  <Eu-153>
   63155.70c  <Eu-155>
   45103.70c  <Rh-103>
   43099.70c  <Tc-99>
   55133.70c  <Cs-133>
```

### Decay Heat Calculations

**Add Tier 3** (25 isotopes):
```mcnp
c TIER 1 + TIER 2 + TIER 3 (decay heat)
   [... Tiers 1-2 above ...]
   55137.70c  <Cs-137>
   38090.70c  <Sr-90>
   56140.70c  <Ba-140>
   57140.70c  <La-140>
   58141.70c  <Ce-141>
   59143.70c  <Pr-143>
   44106.70c  <Ru-106>
```

### Shutdown Dose Rates

**Focus on γ emitters** (Tier 1 + 3):
```mcnp
c Strong absorbers + gamma sources
   54135.70c  <Xe-135>  (short-term)
   62149.70c  <Sm-149>
   55137.70c  <Cs-137>  (DOMINANT γ, 661 keV)
   56140.70c  <Ba-140>  (short-term γ)
   57140.70c  <La-140>  (short-term γ)
```

### Benchmark/Research (High Fidelity)

**Add Tier 4** (40+ isotopes):
- Include all stable FPs with yield >0.5%
- Include all isotopes with σ_thermal > 10 barn
- Include complete decay chains (I-135 → Xe-135, etc.)

---

## MCNP BURN Card Fission Product Tier Settings

MCNP's BURN card includes built-in fission product tiers via BOPT keyword:

```mcnp
BOPT = Q-value, FP_tier, output_control, ...

FP_tier options:
  -4 = ALL fission products (~3400 isotopes) - VERY SLOW
  -3 = Tier 3 (~1000 isotopes) - SLOW
  -2 = Tier 2 (~500 isotopes) - MEDIUM
  -1 = Tier 1 (~200 isotopes) - FAST (RECOMMENDED)
   0 = NO fission products (actinides only) - TESTING ONLY
```

**Recommendation**: Use `BOPT=1.0, -1` for routine work (Tier 1, ~200 FPs)

**Custom selection**: Use OMIT keyword to exclude specific isotopes from transport

---

## Cross-Section Energy Dependence

**Thermal absorbers** (1/v behavior):
- Xe-135, Sm-149, Gd-157: σ ∝ 1/√E at low energies
- Very strong in thermal reactors (PWR, BWR, HTGR)
- Moderate in epithermal (CANDU)
- Weak in fast reactors (SFR)

**Resonance absorbers**:
- Rh-103, Tc-99, Eu-155: σ peaks at epithermal energies (1-100 eV)
- Important in all reactor types
- Must use detailed cross-section libraries

**Fast spectrum**:
- All FP cross-sections very small (<10 barn) above 1 keV
- FP poisoning negligible in fast reactors

---

## Fission Yield Data Sources

**ENDF/B-VIII.0** (latest):
- Fission yields for U-233, U-235, U-238, Pu-239, Pu-241
- Thermal, fast, and 14 MeV neutron-induced fission
- Independent and cumulative yields

**JEFF-3.3** (European):
- Alternative yield evaluations
- Often agrees within 10% with ENDF

**Typical yields** (U-235 thermal fission):
- Xe-135: 6.3% (cumulative, via I-135)
- Sm-149: 1.1% (cumulative, via Pm-149)
- Cs-137: 6.2%
- Sr-90: 5.8%
- Tc-99: 6.1%

---

## Quality Assurance Checks

### After burnup calculation, verify FP inventory:

**Mass balance**:
```python
# Total FP mass ≈ fissioned U mass
M_FP = sum([mass_i for all FPs])
M_U_fissioned = (N_U235_initial - N_U235_final) × A_U235 / N_A

ratio = M_FP / M_U_fissioned
print(f"FP/Fission mass ratio: {ratio:.3f}")
# Should be ~0.95-1.0 (some mass lost to neutrons)
```

**Fission yield check**:
```python
# Nd-148 is stable burnup monitor (not destroyed by neutrons)
N_Nd148 = measured_Nd148_density
fissions = N_Nd148 / yield_Nd148
print(f"Total fissions: {fissions:.2e}")

# Compare to:
fissions_from_burnup = burnup_GWd_MTU × conversion_factor
```

**Reactivity sanity check**:
```python
# Sm-149 + Xe-135 should contribute -2000 to -4000 pcm
rho_Sm = -N_Sm149 × sigma_Sm149 × ...
rho_Xe = -N_Xe135 × sigma_Xe135 × ...
rho_total_FP = rho_Sm + rho_Xe + ...
print(f"Total FP reactivity worth: {rho_total_FP:.0f} pcm")
# Typical PWR: -4000 to -6000 pcm at equilibrium
```

---

## References

- ENDF/B-VIII.0 Nuclear Data Library
- JEFF-3.3 Fission Yield Evaluations
- OECD/NEA burnup credit criticality benchmarks
- SCALE ORIGEN-S fission product library
- MCNP6 manual, Appendix I (Burnup isotopes)
