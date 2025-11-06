---
name: "MCNP Tally Analyzer"
description: "Analyzes MCNP tally results to extract physics information, validate statistical quality, convert units, and interpret physical meaning. Use when analyzing simulation results."
version: "1.0.0"
dependencies: "python>=3.8, numpy, pandas"
---

# MCNP Tally Analyzer

## Overview

When a user needs to understand, interpret, or analyze MCNP tally results, use this skill to:

- Extract tally values with uncertainties from output files
- Validate statistical quality using 10 statistical checks
- Interpret results physically (flux, dose, reaction rates)
- Convert to practical units (Sv/hr, W, reactions/sec)
- Analyze energy/time/spatial distributions
- Compare multiple tallies for validation
- Identify trends and anomalies
- Guide uncertainty reduction strategies

This skill bridges raw simulation output and meaningful physical insights, helping users understand what their results mean and whether they can be trusted.

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User asks to "analyze", "interpret", or "understand" tally results
- User mentions tally numbers: "F4", "tally 14", "flux tally"
- User wants to know "what does this mean?"
- User asks about dose, reaction rates, power, heating
- User wants to convert units or normalize results
- User asks if results are "reliable" or "converged"
- User needs to compare tallies or validate calculations
- User mentions energy spectrum, spatial distribution
- **Phase 3:** User asks about variance reduction effectiveness
- **Phase 3:** User wants to compare analog vs VR results
- **Phase 3:** User asks "is my VR working?"

**Context Clues:**
- "Is my flux result reasonable?"
- "Convert this to dose rate..."
- "What's the energy spectrum showing?"
- "Compare F2 and F4..."
- "Can I trust these results?"
- "How many fissions per second?"
- **Phase 3:** "Did my weight windows help?"
- **Phase 3:** "Why is FOM not improving?"

### Analysis Approach Decision Tree

**Step 1: Identify Analysis Type**

```
User request → Determine goal:
├── Statistical validation → Check 10 quality metrics
├── Physical interpretation → Explain what tally measures
├── Unit conversion → Convert to practical units
├── Spectrum analysis → Analyze energy/time bins
├── Spatial analysis → Analyze position distribution
├── Tally comparison → Cross-validate results
└── Trend analysis → Identify patterns, anomalies
```

**Step 2: Select Tally Type**

```
Tally type determines analysis:
├── F1 (surface current) → Leakage, transmission analysis
├── F2 (surface flux) → Surface dose, particle flow
├── F4 (cell flux) → Volume-averaged flux, reaction rates
├── F5 (point detector) → Localized flux, dose at point
├── F6 (energy deposition) → Heating, dose, power
├── F7 (fission energy) → Fission power distribution
├── F8 (pulse height) → Detector response, spectroscopy
└── FMESH (mesh tally) → 3D spatial distributions
```

**Step 3: Determine Analysis Depth**

```
Quick assessment:
├── Tally value with uncertainty
├── Statistical quality (pass/fail)
└── Basic physical interpretation

Comprehensive analysis:
├── All 10 statistical checks
├── Energy spectrum breakdown
├── Spatial/temporal trends
├── Cross-validation with other tallies
├── Unit conversions
├── Physical reasonableness check
└── Recommendations for improvement

Specialized analysis:
├── Spectral indices (thermal/fast ratio)
├── Dose coefficients
├── Perturbation analysis
├── Sensitivity studies
└── Benchmark comparisons

Phase 3 - VR effectiveness analysis:
├── FOM improvement measurement (analog vs VR)
├── Convergence diagnostics (CLT compliance)
├── Under-sampling identification
├── VR artifact detection (overbiasing)
├── WWG iteration convergence tracking
└── VR optimization recommendations
```

## Tool Invocation

This skill includes a Python implementation for automated tally analysis.

### Importing the Tool

```python
from mcnp_tally_analyzer import MCNPTallyAnalyzer
analyzer = MCNPTallyAnalyzer()
```

### Basic Usage

```python
# Analyze specific tally
analysis = analyzer.analyze_tally('outp', tally_num=4)
print(f"F4: {analysis['value']:.4e} ± {analysis['rel_error']:.1%}")
```

### Integration with MCNP Workflow

```python
from mcnp_tally_analyzer import MCNPTallyAnalyzer

analyzer = MCNPTallyAnalyzer()
results = analyzer.get_all_tallies("outp")

for tally_num, data in results.items():
    print(f"F{tally_num}: {data['quality']} - {data['value']:.4e}")
```

---

## Analysis Procedures

### Step 1: Initial Assessment

**Ask user for context:**
- "Which tally results do you want to analyze?" (tally number)
- "What are you measuring?" (flux, dose, heating, reaction rate)
- "What do you need to know?" (value, uncertainty, spectrum, validation)
- "Are you comparing multiple runs or tallies?"
- "Do you need results in specific units?"

### Step 2: Read Reference Materials

**MANDATORY - READ ENTIRE FILE**: Before performing analysis, read:
- `.claude/commands/mcnp-tally-analyzer.md` - Complete analysis procedures
- If needed: `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Tally types and units

### Step 3: Extract Tally Data

Use the Python module to extract tally results:

```python
from skills.output_analysis.mcnp_tally_analyzer import MCNPTallyAnalyzer

analyzer = MCNPTallyAnalyzer()

# Extract all tallies
all_tallies = analyzer.extract_tally_results('output.o')

# Extract specific tally
tally_4 = analyzer.get_tally_by_number('output.o', tally_num=4)

# Structure:
# {
#     'number': 4,
#     'type': 'F4',  # track length flux
#     'particle': 'neutron',
#     'cells': [10, 11, 12],
#     'values': [array of values],
#     'errors': [array of relative errors],
#     'energy_bins': [bin boundaries],
#     'time_bins': [bin boundaries],
#     'statistics': {
#         'mean': value,
#         'vov': variance_of_variance,
#         'fom': figure_of_merit,
#         'slope': history_score_slope,
#         'tests_passed': '9/10' or '10/10'
#     }
# }

# Find tally with worst uncertainty
worst_tally, worst_error = analyzer.get_worst_error('output.o')
print(f"Tally F{worst_tally} has worst error: {worst_error:.1%}")
```

### Step 4: Validate Statistical Quality

**The 10 Statistical Checks (Chapter 3.4.2.4):**

```python
def validate_statistical_quality(tally_stats):
    """Check all 10 MCNP statistical quality indicators"""

    checks = []

    # Check 1: Mean should not change significantly in last half
    # MCNP tracks mean(x) behavior over run
    checks.append({
        'name': 'Mean stability',
        'status': tally_stats.get('mean_stable', True),
        'criterion': 'Mean stable in last 50% of histories'
    })

    # Check 2: Relative error R < 0.10 (10%)
    rel_error = tally_stats.get('relative_error', 999)
    checks.append({
        'name': 'Relative error',
        'value': rel_error,
        'status': rel_error < 0.10,
        'criterion': 'R < 0.10 (good); R < 0.05 (excellent)'
    })

    # Check 3: Variance of Variance (VOV) < 0.10
    vov = tally_stats.get('vov', 999)
    checks.append({
        'name': 'Variance of variance',
        'value': vov,
        'status': vov < 0.10,
        'criterion': 'VOV < 0.10'
    })

    # Check 4: Figure of Merit (FOM) constant within 10%
    fom_constant = tally_stats.get('fom_constant', False)
    checks.append({
        'name': 'FOM stability',
        'status': fom_constant,
        'criterion': 'FOM varies <10% over last half'
    })

    # Check 5: FOM > 100 for reliable results
    fom = tally_stats.get('fom', 0)
    checks.append({
        'name': 'FOM magnitude',
        'value': fom,
        'status': fom > 100,
        'criterion': 'FOM > 100 (higher is better)'
    })

    # Check 6: Slope of history score fits 3.0-10.0 range
    slope = tally_stats.get('slope', 0)
    checks.append({
        'name': 'History slope',
        'value': slope,
        'status': 3.0 <= slope <= 10.0,
        'criterion': '3.0 ≤ slope ≤ 10.0'
    })

    # Check 7: No zero or negative tally bins
    has_negative = tally_stats.get('has_negative_bins', False)
    checks.append({
        'name': 'Non-negative bins',
        'status': not has_negative,
        'criterion': 'All bins ≥ 0'
    })

    # Check 8: All 10 tests passed (from TFC chart)
    tests_passed = tally_stats.get('tests_passed', '0/10')
    all_passed = tests_passed == '10/10'
    checks.append({
        'name': 'TFC tests',
        'value': tests_passed,
        'status': all_passed,
        'criterion': '10/10 tests passed'
    })

    # Check 9: Relative error decreasing as ~1/√N
    error_trend_ok = tally_stats.get('error_trend_ok', True)
    checks.append({
        'name': 'Error trend',
        'status': error_trend_ok,
        'criterion': 'R ∝ 1/√NPS'
    })

    # Check 10: PDF shows reasonable distribution
    pdf_ok = tally_stats.get('pdf_reasonable', True)
    checks.append({
        'name': 'PDF distribution',
        'status': pdf_ok,
        'criterion': 'PDF bell-shaped, centered'
    })

    # Summary
    n_passed = sum(1 for c in checks if c['status'])
    overall_quality = 'EXCELLENT' if n_passed >= 9 else \
                     'GOOD' if n_passed >= 7 else \
                     'MARGINAL' if n_passed >= 5 else 'POOR'

    return {
        'checks': checks,
        'passed': n_passed,
        'total': 10,
        'quality': overall_quality
    }
```

**Present validation results:**
```
STATISTICAL QUALITY ASSESSMENT

✓ Check 1: Mean stability - PASS
✓ Check 2: Relative error = 3.2% - PASS (excellent, <5%)
✓ Check 3: VOV = 0.0045 - PASS (<0.10)
✓ Check 4: FOM stability - PASS
✓ Check 5: FOM = 1234.5 - PASS (>100)
✓ Check 6: Slope = 4.2 - PASS (in range 3-10)
✓ Check 7: No negative bins - PASS
✓ Check 8: TFC tests = 10/10 - PASS
✓ Check 9: Error trend - PASS
✓ Check 10: PDF distribution - PASS

OVERALL QUALITY: EXCELLENT (10/10 checks passed)

RECOMMENDATION: Results are statistically reliable for quantitative analysis.
```

### Step 5: Interpret Physically

**Tally Type Interpretations:**

**F1 - Surface Current (particles per source particle)**
```
Physical meaning:
- Number of particles crossing surface
- Not normalized by area
- Directional (+/- for forward/backward)

Units: particles (or MeV if *F1)

Common uses:
- Leakage from system
- Transmission through shield
- Particle flow between regions

Conversion to rate:
  Particle rate = F1 × Source rate (particles/sec)
```

**F2 - Surface Flux (particles/cm²)**
```
Physical meaning:
- Average flux over surface area
- Track length estimator on surface
- Area-normalized

Units: particles/cm² (or MeV/cm² if *F2)

Common uses:
- Surface dose rates
- Detector response at boundary
- Flux entering/leaving region

Conversion to dose rate:
  Dose rate (Sv/hr) = F2 × Flux-to-dose × Source rate × 3600
  (See dose conversion tables, e.g., ICRP-74)
```

**F4 - Cell Flux (particles/cm²)**
```
Physical meaning:
- Volume-averaged flux in cell
- Track length estimator: ∫(track length / volume)
- Most common tally type

Units: particles/cm² (or MeV/cm² if *F4)

Common uses:
- Reaction rates: R = F4 × Σ × V × S
- Activation calculations
- Spectrum analysis
- Average dose in volume

Conversion to reaction rate:
  R = F4 × Σ_reaction × Volume × Source rate

  where Σ = N × σ (macroscopic XS)
        N = atom density (atoms/b-cm)
        σ = microscopic XS (barns)
```

**F5 - Point Detector (particles/cm²)**
```
Physical meaning:
- Flux at specific point
- Next-event estimator (deterministic)
- Can include ring detector averaging

Units: particles/cm² (or MeV/cm² if *F5)

Common uses:
- Dose at detector location
- Flux in void or low-importance region
- Measurement point calculations

Cautions:
- Can have large variance if not well positioned
- Sensitive to geometry near detector
- Use PD card to improve statistics

Conversion to dose rate:
  Dose rate = F5 × Flux-to-dose × Source rate × 3600
```

**F6 - Energy Deposition (MeV/g)**
```
Physical meaning:
- Energy deposited per unit mass
- Collision heating (energy locally deposited)
- Per source particle

Units: MeV/g (or jerks/g if PRINT card)

Common uses:
- Heating in components
- Dose to materials/tissue
- Power density
- Radiation damage

Conversion to power:
  Power (W) = F6 × Mass × Source rate × 1.602E-13
  (1 MeV = 1.602E-13 J)

Conversion to dose (for tissue):
  Dose (Gy) = F6 × 1.602E-13 J/MeV / (1 g × 1 J/kg/Gy)
            = F6 × 1.602E-13 Gy per source particle

  Dose rate (Gy/hr) = F6 × Source rate × 3600 × 1.602E-13

  For Sieverts: multiply by quality factor Q
  (Q = 1 for photons/electrons, ~10 for neutrons)
```

**F7 - Fission Energy (MeV/g, neutrons only)**
```
Physical meaning:
- Energy deposition from fission only
- Includes prompt gamma, fission fragments
- Neutrons only (MODE N)

Units: MeV/g

Common uses:
- Fission power distribution in fuel
- Reactor power profiles
- Fission heating calculations

Conversion to fission power:
  Power (W) = F7 × Mass × Source rate × 1.602E-13

Note: Total energy per fission ≈ 200 MeV
      F7 measures only locally deposited component
```

**F8 - Pulse Height (pulses or MeV)**
```
Physical meaning:
- Energy deposited in detector cell
- Histogram of pulse heights
- Simulates detector response

Units: pulses (or MeV if *F8)

Common uses:
- Gamma spectroscopy
- Detector response functions
- Count rate predictions

Energy bins = pulse height spectrum

Conversion to count rate:
  Count rate (cps) = F8 × Source rate
  (in specific energy window)
```

### Step 6: Analyze Energy Spectrum

For tallies with energy binning:

```python
def analyze_energy_spectrum(tally_data):
    """Analyze energy-dependent tally results"""

    energy_bins = tally_data['energy_bins']
    values = tally_data['values']
    errors = tally_data['errors']

    # Calculate bin contributions
    total = sum(values)
    contributions = [v/total for v in values]

    # Categorize by energy range (for neutrons)
    thermal_fraction = 0  # E < 1 eV
    epithermal_fraction = 0  # 1 eV < E < 1 keV
    fast_fraction = 0  # E > 1 keV

    for i, (e_low, e_high) in enumerate(energy_bins):
        e_mid = (e_low + e_high) / 2
        contrib = contributions[i]

        if e_mid < 1e-6:  # MeV → 1 eV
            thermal_fraction += contrib
        elif e_mid < 1e-3:  # MeV → 1 keV
            epithermal_fraction += contrib
        else:
            fast_fraction += contrib

    # Spectral indices
    thermal_fast_ratio = thermal_fraction / fast_fraction if fast_fraction > 0 else 0

    # Find peak energy
    peak_idx = values.index(max(values))
    peak_energy = energy_bins[peak_idx]

    return {
        'total_flux': total,
        'thermal_fraction': thermal_fraction,
        'epithermal_fraction': epithermal_fraction,
        'fast_fraction': fast_fraction,
        'thermal_fast_ratio': thermal_fast_ratio,
        'peak_energy': peak_energy,
        'peak_value': values[peak_idx]
    }
```

**Present spectrum analysis:**
```
ENERGY SPECTRUM ANALYSIS - F4:N Tally

Total flux: 2.73E-04 n/cm² per source neutron

Energy group contributions:
  Thermal (E < 1 eV):        1.23E-04 (45.1%)
  Epithermal (1 eV - 1 keV): 5.74E-05 (21.0%)
  Fast (E > 1 keV):          9.28E-05 (33.9%)

Spectral indices:
  Thermal/Fast ratio: 1.33
  Peak energy: 0.025 eV (thermal peak)

Physical interpretation:
  - Thermal-dominated spectrum indicates significant moderation
  - 45% thermal suggests water or graphite moderator present
  - Fast component (34%) likely from source or fission neutrons
  - Peak at 0.025 eV is Maxwellian thermal distribution

Energy bin details:
  E (MeV)           Flux (n/cm²)    Rel Err    % Total
  0.0 - 1.0E-6      1.23E-04        0.05       45.1%
  1.0E-6 - 1.0E-3   5.74E-05        0.08       21.0%
  1.0E-3 - 0.1      4.12E-05        0.10       15.1%
  0.1 - 1.0         2.89E-05        0.12       10.6%
  1.0 - 10.0        2.27E-05        0.15       8.3%
  Total             2.73E-04        0.03       100.0%
```

### Step 7: Perform Unit Conversions

**Common conversions:**

**Flux to dose rate (for neutrons):**
```python
def flux_to_dose_rate(flux_per_source, source_rate_per_sec, particle='neutron'):
    """
    Convert flux tally to dose rate

    Args:
        flux_per_source: F2 or F4 result (particles/cm²)
        source_rate_per_sec: Source strength (particles/sec)
        particle: 'neutron', 'photon', or 'electron'

    Returns:
        dose_rate_sv_per_hr: Ambient dose equivalent rate (Sv/hr)
    """

    # Flux-to-dose conversion factors (Sv·cm² per particle)
    # From ICRP-74 or NCRP-38, energy-averaged
    conversion_factors = {
        'neutron_thermal': 5.0e-15,  # ~0.025 eV
        'neutron_1MeV': 4.0e-14,     # 1 MeV
        'neutron_14MeV': 6.0e-14,    # 14 MeV (DT fusion)
        'photon_0.1MeV': 2.0e-15,    # 100 keV
        'photon_1MeV': 5.0e-15,      # 1 MeV
        'photon_10MeV': 1.2e-14      # 10 MeV
    }

    # Use appropriate factor (example: 1 MeV neutrons)
    fluence_to_dose = conversion_factors.get('neutron_1MeV', 4.0e-14)

    # Calculate dose rate
    flux_total = flux_per_source * source_rate_per_sec  # particles/(cm²·sec)
    dose_rate_sv_per_sec = flux_total * fluence_to_dose  # Sv/sec
    dose_rate_sv_per_hr = dose_rate_sv_per_sec * 3600  # Sv/hr

    return dose_rate_sv_per_hr

# Example usage:
flux_f4 = 2.73e-4  # n/cm² per source neutron
source_rate = 1e10  # neutrons/sec

dose_rate = flux_to_dose_rate(flux_f4, source_rate, 'neutron')
print(f"Dose rate: {dose_rate:.2e} Sv/hr = {dose_rate*1e6:.2f} µSv/hr")
```

**Flux to reaction rate:**
```python
def flux_to_reaction_rate(flux_per_source, volume_cm3, atom_density_per_b_cm,
                          microscopic_xs_barns, source_rate_per_sec):
    """
    Convert F4 flux to reaction rate

    Args:
        flux_per_source: F4 result (n/cm²)
        volume_cm3: Cell volume (cm³)
        atom_density_per_b_cm: N (atoms per barn-cm)
        microscopic_xs_barns: σ (barns)
        source_rate_per_sec: Source strength (n/sec)

    Returns:
        reaction_rate_per_sec: Reactions per second
    """

    # Macroscopic cross section (cm⁻¹)
    macro_xs = atom_density_per_b_cm * microscopic_xs_barns  # atoms/b-cm × barns = cm⁻¹

    # Reaction rate per source particle
    reaction_per_source = flux_per_source * macro_xs * volume_cm3  # reactions/source

    # Total reaction rate
    reaction_rate = reaction_per_source * source_rate_per_sec  # reactions/sec

    return reaction_rate

# Example: U-235 fission in 1000 cm³ fuel
flux_f4 = 2.73e-4  # n/cm²
volume = 1000  # cm³
N_U235 = 0.024  # atoms/(b-cm) [from atom density calculation]
sigma_fission = 585  # barns (thermal)
source_rate = 1e10  # n/sec

fission_rate = flux_to_reaction_rate(flux_f4, volume, N_U235, sigma_fission, source_rate)
print(f"Fission rate: {fission_rate:.2e} fissions/sec")

# Convert to power
energy_per_fission = 200  # MeV
power_watts = fission_rate * energy_per_fission * 1.602e-13  # W
print(f"Fission power: {power_watts:.2e} W = {power_watts/1000:.2f} kW")
```

**F6 to power:**
```python
def f6_to_power(f6_result_mev_per_g, mass_grams, source_rate_per_sec):
    """
    Convert F6 energy deposition to power

    Args:
        f6_result_mev_per_g: F6 tally result (MeV/g per source particle)
        mass_grams: Mass of the cell (g)
        source_rate_per_sec: Source strength (particles/sec)

    Returns:
        power_watts: Heating power (W)
    """

    # Energy per source particle
    energy_per_source_mev = f6_result_mev_per_g * mass_grams  # MeV

    # Total energy deposition rate
    energy_rate_mev_per_sec = energy_per_source_mev * source_rate_per_sec  # MeV/sec

    # Convert to watts (1 MeV = 1.602E-13 J)
    power_watts = energy_rate_mev_per_sec * 1.602e-13  # W

    return power_watts

# Example: Shield heating
f6_result = 1.23e-5  # MeV/g
mass = 50000  # grams (50 kg shield)
source_rate = 1e12  # particles/sec

power = f6_to_power(f6_result, mass, source_rate)
print(f"Heating power: {power:.2f} W")

# Temperature rise estimate
specific_heat = 0.5  # J/(g·°C) for steel
temp_rise_per_hour = (power * 3600) / (mass * specific_heat)  # °C/hr
print(f"Temperature rise: {temp_rise_per_hour:.2f} °C/hr (no cooling)")
```

### Step 8: Compare Tallies

**Cross-validation strategies:**

**Same quantity, different estimators:**
```python
# F2 surface flux vs F4 cell flux at boundary
# Should agree within statistical uncertainty

f2_surface = 3.45e-4  # particles/cm²
f2_error = 0.05      # 5% relative error

f4_adjacent_cell = 3.52e-4  # particles/cm²
f4_error = 0.03      # 3% relative error

# Check agreement
difference = abs(f2_surface - f4_adjacent_cell)
combined_error = (f2_surface * f2_error)**2 + (f4_adjacent_cell * f4_error)**2
combined_error = combined_error ** 0.5

sigma_difference = difference / combined_error

if sigma_difference < 2:
    print("✓ F2 and F4 agree within 2σ - CONSISTENT")
else:
    print(f"⚠ F2 and F4 differ by {sigma_difference:.1f}σ - CHECK GEOMETRY")
```

**Particle balance check:**
```python
# For neutrons: source = absorption + leakage
# Use F1 tallies on all surfaces + absorption in cells

source_strength = 1.0  # normalized

# Leakage (F1 tallies on all outer surfaces)
leakage = sum([f1_top, f1_bottom, f1_sides])  # particles

# Absorption (from FM4 with MT=-2 for total absorption)
absorption = sum(f4_absorption_all_cells)  # particles

total_accounted = leakage + absorption

balance_error = abs(total_accounted - source_strength) / source_strength

if balance_error < 0.05:
    print(f"✓ Particle balance: {balance_error:.1%} error - GOOD")
else:
    print(f"⚠ Particle balance: {balance_error:.1%} error - CHECK IMPORTANCE")
```

**Energy conservation check:**
```python
# Source energy = escaping energy + deposited energy

source_energy = 14.0  # MeV (DT fusion neutrons)

# Escaping energy (*F1 tallies)
escaping_energy = sum(star_f1_all_surfaces)  # MeV

# Deposited energy (F6 tallies)
deposited_energy = sum(f6_all_cells)  # MeV (normalized to per particle)

total_energy = escaping_energy + deposited_energy

energy_balance = abs(total_energy - source_energy) / source_energy

if energy_balance < 0.10:
    print(f"✓ Energy balance: {energy_balance:.1%} error - GOOD")
else:
    print(f"⚠ Energy balance: {energy_balance:.1%} error - CHECK PHYSICS")
```

## Tally Multiplier (FM Card) Analysis

**When FM card is used:**

The FM card converts flux tallies to reaction rates by multiplying by cross sections.

**FM card format:**
```
FM4 C M R
```
- C = constant multiplier
- M = material number (negative = use cell material)
- R = reaction MT number (negative = ENDF MT number)

**Common reactions (MT numbers):**
```
-1  = total cross section
-2  = absorption (capture + fission)
-6  = (n,γ) disappearance cross section
1   = total
2   = elastic scatter
16  = (n,2n)
18  = fission
102 = (n,γ) capture
103 = (n,p)
104 = (n,d)
105 = (n,t)
```

**Example FM card:**
```
F4:N 10                    $ Neutron flux in cell 10
FM4 1.0 -1 18              $ Multiply by fission cross section
```

**Result interpretation:**
```
Without FM: F4 = 2.73E-04 n/cm²
With FM4:   F4 = 1.37E-05 fissions/cm³ per source neutron

To get fissions per second:
  Fission rate = 1.37E-05 fissions/cm³ × Volume × Source rate
```

**Multiple FM cards:**
```
F4:N 10
FM4 (1.0 -1 18)      $ Fission
    (1.0 -1 102)     $ Radiative capture
    (1.0 -1 16)      $ (n,2n)

Result: Three sets of values (one per reaction)
```

## Advanced Analysis Techniques

### Spectral Indices

**Thermal-to-fast flux ratio:**
```python
# Indicator of moderation
thermal_flux = sum(flux[E < 1 eV])
fast_flux = sum(flux[E > 100 keV])
ratio = thermal_flux / fast_flux

# Typical values:
# ratio > 10: Well-thermalized (graphite reactor)
# ratio 1-10: Partially thermalized (water reactor)
# ratio < 1: Fast spectrum (fast reactor, fusion)
```

**Cadmium ratio:**
```python
# Ratio of gold activation with/without cadmium cover
# Cadmium absorbs thermal neutrons (E < 0.5 eV)

flux_total = f4_bare_gold
flux_epithermal = f4_cadmium_covered_gold

cadmium_ratio = flux_total / flux_epithermal

# Typical values:
# CR > 100: Very thermal
# CR 10-100: Thermal
# CR < 10: Epithermal/fast
```

**Average energy:**
```python
# Energy-weighted flux divided by total flux
star_f4_result = sum(E_i * flux_i)  # From *F4 tally
f4_result = sum(flux_i)

average_energy = star_f4_result / f4_result  # MeV

print(f"Average neutron energy: {average_energy:.3f} MeV")
```

### Spatial Distribution Analysis

**Radial profiles:**
```python
# F4 tallies in concentric cells or FMESH with cylindrical mesh

radii = [5, 10, 15, 20, 25]  # cm
fluxes = [1.2e-3, 8.5e-4, 4.2e-4, 1.8e-4, 5.3e-5]  # n/cm²

# Peak-to-average ratio
peak = max(fluxes)
average = sum(fluxes) / len(fluxes)
peak_to_avg = peak / average

print(f"Peak/average flux ratio: {peak_to_avg:.2f}")

# Flux drop-off rate
import numpy as np
fit = np.polyfit(radii, np.log(fluxes), 1)  # exponential fit
relaxation_length = -1 / fit[0]  # cm

print(f"Flux relaxation length: {relaxation_length:.1f} cm")
```

**Axial distributions:**
```python
# Power distribution in reactor fuel
# F7 fission heating tallies at different axial positions

z_positions = [-100, -50, 0, 50, 100]  # cm
power_density = [0.8, 1.1, 1.3, 1.0, 0.7]  # arbitrary units

# Form factor (peak/average for cosine distribution)
peak_power = max(power_density)
avg_power = sum(power_density) / len(power_density)
form_factor = peak_power / avg_power

print(f"Axial power form factor: {form_factor:.2f}")
```

### Time-Dependent Analysis

**Pulsed source response:**
```python
# F4 tally with time bins (T card)

time_bins = [0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4]  # seconds (shakes × 1e-8)
flux_vs_time = [5.2e-3, 3.1e-3, 1.2e-3, 3.4e-4, 8.1e-5]

# Decay constant
import numpy as np
fit = np.polyfit(time_bins[:-1], np.log(flux_vs_time), 1)
decay_constant = -fit[0]  # 1/sec

half_life = 0.693 / decay_constant  # sec

print(f"Effective decay half-life: {half_life:.2e} seconds")
```

## Integration with Other Skills

After tally analysis, recommend:

- **mcnp-statistics-checker**: For comprehensive statistical validation if quality questionable
- **mcnp-plotter**: For automated plotting of spectra and distributions
- **mcnp-variance-reducer**: If uncertainties too large, improve variance reduction
- **mcnp-output-parser**: If need to extract raw data for custom analysis
- **mcnp-mesh-builder**: If spatial resolution insufficient, add mesh tallies

**Phase 3 - VR Integration:**
- **mcnp-variance-reducer**: Implement VR based on tally analysis findings
- **mcnp-ww-optimizer**: Iteratively refine weight windows to improve tally statistics
- **mcnp-statistics-checker**: Validate VR effectiveness using advanced convergence theory
- Use tally feedback to guide VR optimization (see `tally_vr_optimization.md`)

## Important Analysis Principles

1. **Statistical quality first, always**
   - Never interpret results with R > 0.20 (20%)
   - Check all 10 statistical tests
   - Unreliable statistics = meaningless physics

2. **Understand your tally type**
   - F4 averages over volume; F5 is at a point
   - F2 is on surface; F1 integrates over surface
   - Track-length estimators (F2, F4, F7) vs collision (F6)

3. **Units matter critically**
   - F6 is MeV/g, not dose (need conversion)
   - Flux is per cm², not per cm³
   - Relative error is fractional (0.05 = 5%, NOT 0.05%)
   - All results are per source particle

4. **Energy spectrum gives physical insight**
   - Thermal peak indicates moderation
   - Fast tail shows high-energy source/fission
   - Resonances reveal specific materials

5. **Cross-validation is essential**
   - One tally is a measurement
   - Two tallies are validation
   - Use different estimators for same quantity

6. **Physical reasonableness check**
   - Does flux decrease with shielding?
   - Is thermal flux higher in moderator?
   - Does fission occur only in fuel?
   - Is dose rate plausible?

7. **FM cards change interpretation**
   - Results become reaction rates, not flux
   - Units change from particles/cm² to reactions/cm³
   - Always check for FM card before interpreting

8. **Binning affects statistics**
   - More bins = more variance per bin
   - Total tally often most reliable
   - Finest bin may have large uncertainty

9. **Source normalization**
   - All tallies are per source particle
   - Multiply by source rate for absolute quantities
   - Verify source definition (SDEF or KCODE)

10. **Temperature effects**
    - Cross sections are temperature-dependent
    - TMP card affects Doppler broadening
    - Check if thermal treatment appropriate

## Example Workflows

### Example 1: F4 Flux Analysis

```
User: "Analyze my F4 neutron flux tally in cell 10"

Claude: I'll extract and analyze the F4 neutron flux tally from your output file.

[Reads .claude/commands/mcnp-tally-analyzer.md]
[Uses MCNPTallyAnalyzer]

**F4:N Tally Analysis - Cell 10**

**Tally Results:**
Total flux: 2.73E-04 n/cm² per source neutron
Relative error: 3.2% ✓

**Statistical Quality: EXCELLENT**
✓ All 10 statistical checks passed
✓ Relative error: 3.2% (excellent, <5%)
✓ VOV: 0.0045 (well below 0.10 limit)
✓ FOM: 1234.5 (stable, >100)
✓ Slope: 4.2 (in acceptable range 3-10)

**Energy Spectrum:**
Thermal (E < 1 eV):        1.23E-04 n/cm² (45.1%)
Epithermal (1 eV - 1 keV): 5.74E-05 n/cm² (21.0%)
Fast (E > 1 keV):          9.28E-05 n/cm² (33.9%)

Thermal/Fast ratio: 1.33

**Energy Bin Detail:**
E Range (MeV)     Flux (n/cm²)    Rel Err    Contribution
0.0 - 1.0E-6      1.23E-04        5.0%       45.1% ████████████████████
1.0E-6 - 1.0E-3   5.74E-05        8.0%       21.0% █████████
1.0E-3 - 0.1      4.12E-05       10.0%       15.1% ██████
0.1 - 1.0         2.89E-05       12.0%       10.6% ████
1.0 - 10.0        2.27E-05       15.0%        8.3% ███
TOTAL             2.73E-04        3.2%      100.0%

**Physical Interpretation:**
- Thermal-dominated spectrum (45% thermal) indicates significant moderation
- Likely water or graphite moderator present
- Fast component (34%) from fission or high-energy source
- Peak at thermal energy (0.025 eV) shows Maxwellian distribution

**Reaction Rate Calculation (Example):**
For U-235 fission in this cell:
  Volume: 1000 cm³
  U-235 density: 0.024 atoms/(b-cm)
  Thermal fission XS: 585 barns
  Source rate: 1.0E10 n/sec

  Fission rate = 2.73E-04 × (0.024 × 585) × 1000 × 1.0E10
               = 3.83E12 fissions/sec

  Power = 3.83E12 × 200 MeV/fission × 1.602E-13 W/(MeV/sec)
        = 122.7 W

Would you like me to:
1. Plot the energy spectrum?
2. Convert to dose rate?
3. Compare with other tallies?
4. Calculate specific reaction rates?
```

### Example 2: F6 Heating Analysis

```
User: "What's the heating in my lead shield from F6 tally?"

Claude: I'll analyze your F6 energy deposition tally to calculate heating power.

[Reads .claude/commands/mcnp-tally-analyzer.md]
[Extracts F6 tally]

**F6 Energy Deposition Analysis - Lead Shield**

**Tally Results:**
F6 result: 1.23E-05 MeV/g per source particle
Relative error: 2.8% ✓ (good)

**Statistical Quality: GOOD**
✓ 9/10 statistical checks passed
✓ Relative error acceptable (<5%)
✓ Results reliable for analysis

**Shield Parameters (from input):**
Material: Lead (Pb, Z=82, ρ=11.34 g/cm³)
Volume: 5000 cm³
Mass: 56,700 g (56.7 kg)

**Source Parameters:**
Source type: Photons
Source rate: 1.0E12 photons/sec
Average energy: 1.0 MeV

**Power Calculation:**

Energy per source particle:
  E = 1.23E-05 MeV/g × 56,700 g = 0.697 MeV

Total energy deposition rate:
  Ė = 0.697 MeV/particle × 1.0E12 particles/sec
    = 6.97E11 MeV/sec

Power:
  P = 6.97E11 MeV/sec × 1.602E-13 J/MeV
    = 111.7 W

**Temperature Rise (No Cooling):**

Lead specific heat: c_p = 0.128 J/(g·°C)

Temperature rise rate:
  dT/dt = P / (m × c_p)
        = 111.7 W / (56,700 g × 0.128 J/(g·°C))
        = 0.0154 °C/sec
        = 0.92 °C/min
        = 55.4 °C/hr

**Dose Rate (If Shield Contains Tissue):**

Absorbed dose per particle:
  D = 1.23E-05 MeV/g × 1.602E-13 J/MeV
    = 1.97E-18 Gy

Dose rate:
  Ḋ = 1.97E-18 Gy/particle × 1.0E12 particles/sec
    = 1.97E-06 Gy/sec
    = 7.09 mGy/hr

For tissue (assume quality factor Q=1 for photons):
  Ḣ = 7.09 mSv/hr

**Assessment:**
⚠ Significant heating: 112 W in small shield
⚠ Temperature rise: 55°C/hr requires active cooling
✓ Dose rate: 7 mSv/hr is measurable but manageable

**Recommendations:**
1. Add cooling if continuous operation
2. Monitor temperature in experiments
3. Check thermal expansion effects
4. Verify shield doesn't degrade at elevated temperatures

Would you like me to:
1. Analyze spatial heating distribution (if mesh tally)?
2. Calculate steady-state temperature with cooling?
3. Compare with other energy deposition tallies?
```

### Example 3: Tally Comparison

```
User: "Compare my F2 and F4 flux tallies to make sure they agree"

Claude: I'll extract both tallies and perform a cross-validation check.

[Reads .claude/commands/mcnp-tally-analyzer.md]
[Extracts F2 and F4 tallies]

**Tally Comparison: F2 vs F4**

**F2 Surface Flux (surface 10):**
Value: 3.45E-04 n/cm²
Relative error: 5.0%
Absolute uncertainty: 1.73E-05 n/cm²

**F4 Cell Flux (cell 12, adjacent to surface 10):**
Value: 3.52E-04 n/cm²
Relative error: 3.0%
Absolute uncertainty: 1.06E-05 n/cm²

**Statistical Comparison:**

Difference: |F2 - F4| = 7.0E-06 n/cm²
             Relative difference: 2.0%

Combined uncertainty:
  σ_combined = √(σ_F2² + σ_F4²)
             = √((1.73E-05)² + (1.06E-05)²)
             = 2.03E-05 n/cm²

Significance:
  Δ/σ = 7.0E-06 / 2.03E-05 = 0.34σ

**Result: ✓ EXCELLENT AGREEMENT**

The tallies agree within 0.34 standard deviations. This is well within statistical
uncertainty (expect ~68% of comparisons within 1σ, ~95% within 2σ).

**Interpretation:**
- Both estimators (F2 surface, F4 volume) give consistent results
- Validates geometry at cell-surface interface
- Confirms no geometry errors (overlaps/gaps) at boundary
- Statistical quality sufficient for comparison

**Physical Consistency:**
F4 slightly higher (2%) than F2 is reasonable:
  - F4 averages over cell volume (may include higher flux regions)
  - F2 is specifically at surface (could be at flux minimum)
  - Difference within expected physical variation

✓ Cross-validation PASSED
✓ Results are trustworthy
✓ Can proceed with confidence

Would you like me to:
1. Compare additional tally pairs?
2. Check particle balance (source vs absorption + leakage)?
3. Validate energy conservation?
```

## Code Style Guidelines

When using tally analysis:
- Always report uncertainties with values
- Use scientific notation for small/large numbers
- Convert relative errors to percentages for users (×100)
- Provide physical interpretation, not just numbers
- Cross-validate when possible
- Flag suspicious results proactively
- Offer unit conversions without being asked
- Explain statistical quality clearly

## Dependencies

**Required Python packages:**
- `numpy` - Array operations and statistics
- `pandas` - Data organization (optional)
- Standard library: `csv`, `math`

**Required components:**
- Python module: `skills/output_analysis/mcnp_tally_analyzer.py`
- Output parser: `parsers/output_parser.py`
- Reference: `.claude/commands/mcnp-tally-analyzer.md` (detailed procedures)

**Optional packages:**
- `matplotlib` - Plotting spectra
- `scipy` - Curve fitting, statistical tests

## References

**Primary References (Phase 2):**
- `.claude/commands/mcnp-tally-analyzer.md` - Complete analysis procedures
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Tally types, units, FM cards
- Chapter 5.9: Tally Specification (F cards)
- Chapter 5.10: Tally Modifications (E, T, C, FS bins, FM multipliers)
- Chapter 2: Tallies and Output (theory and estimators)

**Statistical Quality:**
- §3.4.2.4: Ten statistical checks for tally reliability
- §3.4.3: Production phase checks
- Figure 3.1: Tally fluctuation chart interpretation

**Conversion Factors:**
- ICRP-74: Fluence-to-dose conversion coefficients
- NCRP-38: Neutron flux-to-dose conversions
- Table 5.1: Tally types and units

**Reaction Data:**
- Appendix G: ENDF MT reaction numbers
- §5.9.10: FM card (tally multipliers)
- Cross-section libraries: ENDF/B-VIII.0

**Phase 3 - VR Integration:**
- `vr_effectiveness_analysis.md` - FOM analysis, under-sampling detection, VR artifacts
- `convergence_diagnostics.md` - CLT validation, trend analysis, required histories prediction
- `tally_vr_optimization.md` - VR selection from tally analysis, tuning guidance
- `example_inputs/` - VR effectiveness examples (analog vs VR comparisons)

**Related Skills:**
- mcnp-output-parser: Extracting raw tally data
- mcnp-statistics-checker: Detailed statistical validation
- mcnp-plotter: Automated spectrum/distribution plots
- mcnp-unit-converter: Additional unit conversions
- **Phase 3:** mcnp-variance-reducer: Implement VR recommendations
- **Phase 3:** mcnp-ww-optimizer: Refine weight windows based on tally feedback
