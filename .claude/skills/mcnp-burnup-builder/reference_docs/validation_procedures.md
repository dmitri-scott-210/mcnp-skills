# Burnup Calculation Validation Procedures
**Quality Assurance for Depletion and Dose Rate Calculations**

## Purpose

This document provides comprehensive validation procedures for MCNP burnup calculations, including experimental benchmarks, code-to-code comparisons, and internal consistency checks based on production reactor analysis methods.

---

## Validation Philosophy

**Three-Level Approach**:

1. **Internal Consistency** - Physics-based sanity checks
2. **Code-to-Code Comparison** - Cross-validation with other tools
3. **Experimental Benchmark** - Comparison to measured data

**Acceptance Criteria** (typical):
- Burnup: < 5% error vs. experiment
- k_eff: < 300 pcm error vs. experiment/benchmark
- Isotopic composition: < 10% error for major isotopes
- Dose rates: < 20% error (higher tolerance due to measurement uncertainty)

---

## Level 1: Internal Consistency Checks

### Check 1: Reactivity Balance

**Principle**: Total reactivity loss = sum of individual contributions

**Calculation**:
```python
import numpy as np

# Reactivity values (pcm)
rho_total = (k_BOL - k_EOL) / k_BOL / k_EOL * 1e5  # Total burnup reactivity

# Individual contributions
rho_U235_depletion = calculate_delta_k_U235()      # U-235 consumed
rho_Pu_buildup = calculate_delta_k_Pu()            # Pu-239, Pu-241 bred
rho_U238_depletion = calculate_delta_k_U238()      # U-238 fissions
rho_FP_poison = calculate_delta_k_FP()             # Xe-135, Sm-149, etc.
rho_absorber_burnout = calculate_delta_k_absorbers()  # Gd, B-10 (if present)

# Sum of components
rho_sum = (rho_U235_depletion + rho_Pu_buildup +
           rho_U238_depletion + rho_FP_poison + rho_absorber_burnout)

# Error
error = abs(rho_total - rho_sum)
error_percent = error / abs(rho_total) * 100

print(f"Total reactivity loss: {rho_total:.0f} pcm")
print(f"Sum of components: {rho_sum:.0f} pcm")
print(f"Error: {error:.0f} pcm ({error_percent:.1f}%)")

# PASS if error < 500 pcm (< 5% typical)
assert error < 500, "Reactivity balance error too large"
```

**Typical PWR values** (45 GWd/MTU):
- Total reactivity loss: -15,000 to -20,000 pcm
- U-235 depletion: -25,000 pcm
- Pu buildup: +8,000 pcm
- FP poisoning: -3,000 pcm
- Net: ~-20,000 pcm

**PASS**: Error < 500 pcm
**WARNING**: Error 500-1000 pcm (check FP selection, Pu tracking)
**FAIL**: Error > 1000 pcm (major error in calculation)

---

### Check 2: Heavy Metal Mass Balance

**Principle**: Total heavy metal mass ≈ constant (minor decrease from fission)

```python
# Initial heavy metal (kg)
HM_initial = mass_U234 + mass_U235 + mass_U236 + mass_U238

# Final heavy metal (kg)
HM_final = (mass_U234 + mass_U235 + mass_U236 + mass_U238 +
            mass_Np237 + mass_Pu238 + mass_Pu239 + mass_Pu240 +
            mass_Pu241 + mass_Pu242 + mass_Am241 + mass_Am243 +
            mass_Cm242 + mass_Cm244)

# Fissioned mass (from burnup)
burnup_GWd_MTU = 45.0
fissions_per_MTU = burnup_GWd_MTU * 1.05e24  # fissions per GWd
mass_fissioned = fissions_per_MTU * 235 / 6.022e23 / 1000  # kg/MTU

# Expected final HM
HM_expected = HM_initial - mass_fissioned

# Error
error_percent = abs(HM_final - HM_expected) / HM_initial * 100

print(f"Initial HM: {HM_initial:.1f} kg/MTU")
print(f"Final HM: {HM_final:.1f} kg/MTU")
print(f"Expected (accounting for fission): {HM_expected:.1f} kg/MTU")
print(f"Error: {error_percent:.2f}%")

# PASS if < 2%
assert error_percent < 2.0, "Heavy metal mass balance error"
```

**Typical values**:
- Initial: 1000 kg U/MTU
- Fissioned: 45 kg (for 45 GWd/MTU)
- Final: 955 kg HM/MTU
- Error: < 1%

---

### Check 3: Power Normalization

**Principle**: Fission power = fission rate × energy per fission

```python
# From MCNP output
total_fission_rate = 1.234e20  # fissions/sec (from FM4 tally)
energy_per_fission = 200.5     # MeV (Q-value from BOPT)

# Calculate power
power_calculated = (total_fission_rate * energy_per_fission *
                    1.602e-13 / 1e6)  # MW

# Specified power
power_specified = 3400  # MW (from BURN card)

# Error
error_percent = abs(power_calculated - power_specified) / power_specified * 100

print(f"Specified power: {power_specified:.1f} MW")
print(f"Calculated power: {power_calculated:.1f} MW")
print(f"Error: {error_percent:.2f}%")

# PASS if < 5%
assert error_percent < 5.0, "Power normalization error"
```

**Common issues**:
- MATVOL incorrect → wrong fission rate density
- KCODE not converged → wrong flux normalization
- Q-value wrong (should be ~200 MeV for U-235)

---

### Check 4: Fissile Inventory

**Principle**: Bred fissile partially replaces consumed fissile

```python
# Beginning of life
fissile_BOL = N_U235_initial

# End of life
fissile_EOL = N_U235 + N_Pu239 + N_Pu241 + N_Am242m + N_Cm243 + N_Cm245

# Bred fissile
fissile_bred = N_Pu239 + N_Pu241  # Primary bred isotopes

# Conversion ratio (bred / consumed)
fissile_consumed = fissile_BOL - N_U235
conversion_ratio = fissile_bred / fissile_consumed

print(f"BOL fissile: {fissile_BOL:.4e} atoms/barn-cm")
print(f"EOL fissile: {fissile_EOL:.4e} atoms/barn-cm")
print(f"Conversion ratio: {conversion_ratio:.3f}")

# Typical PWR: 0.5-0.8 (50-80% of consumed U-235 replaced by Pu)
assert 0.4 < conversion_ratio < 0.9, "Conversion ratio out of range"
```

**Typical values**:
- PWR: 0.6-0.7 (thermal spectrum, good U-238 conversion)
- BWR: 0.5-0.6 (lower conversion due to void)
- HTGR: 0.4-0.5 (graphite-moderated, harder spectrum)
- Fast reactor: 1.0-1.3 (breeding ratio > 1)

---

### Check 5: Plutonium Vector

**Principle**: Pu isotopic ratios should match reactor type

```python
# Extract Pu masses
Pu238_mass = 2.3e1  # grams
Pu239_mass = 6.0e3
Pu240_mass = 3.0e3
Pu241_mass = 2.0e3
Pu242_mass = 8.0e2

total_Pu = Pu238_mass + Pu239_mass + Pu240_mass + Pu241_mass + Pu242_mass

# Calculate vector (mass percentages)
vector = {
    'Pu238': Pu238_mass / total_Pu * 100,
    'Pu239': Pu239_mass / total_Pu * 100,
    'Pu240': Pu240_mass / total_Pu * 100,
    'Pu241': Pu241_mass / total_Pu * 100,
    'Pu242': Pu242_mass / total_Pu * 100
}

print("Plutonium vector:")
for iso, pct in vector.items():
    print(f"  {iso}: {pct:.1f}%")

# Typical PWR (45 GWd/MTU):
assert 1 < vector['Pu238'] < 3, "Pu-238 out of range"
assert 50 < vector['Pu239'] < 65, "Pu-239 out of range"
assert 20 < vector['Pu240'] < 28, "Pu-240 out of range"
assert 10 < vector['Pu241'] < 16, "Pu-241 out of range"
assert 3 < vector['Pu242'] < 8, "Pu-242 out of range"
```

**Reference vectors**:

| Reactor Type | Burnup (GWd/MTU) | Pu-238 | Pu-239 | Pu-240 | Pu-241 | Pu-242 |
|--------------|------------------|--------|--------|--------|--------|--------|
| PWR          | 45               | 2%     | 56%    | 24%    | 12%    | 6%     |
| BWR          | 40               | 1%     | 60%    | 24%    | 11%    | 4%     |
| CANDU (natural U) | 8           | 1%     | 65%    | 26%    | 6%     | 2%     |
| HTGR (HEU)   | 100              | 5%     | 50%    | 25%    | 12%    | 8%     |

---

### Check 6: Fission Product Yield

**Principle**: FP inventory should match fission yields

```python
# Total fissions from burnup
burnup_GWd_MTU = 45.0
total_fissions = burnup_GWd_MTU * 1.05e24  # fissions/GWd/MTU

# Example: Nd-148 (stable burnup monitor)
yield_Nd148 = 0.0165  # 1.65% cumulative yield for U-235 thermal
N_Nd148_expected = total_fissions * yield_Nd148

# Measured from MCNP/ORIGEN
N_Nd148_calculated = 1.325e-6  # atoms/barn-cm (from output)

# Convert to atoms per MTU
vol_per_MTU = 1.0e6 / (10.4 * 6.022e23 / 238)  # cm³/MTU for UO2
N_Nd148_calculated_total = N_Nd148_calculated * vol_per_MTU

error_percent = abs(N_Nd148_calculated_total - N_Nd148_expected) / N_Nd148_expected * 100

print(f"Expected Nd-148: {N_Nd148_expected:.2e} atoms/MTU")
print(f"Calculated Nd-148: {N_Nd148_calculated_total:.2e} atoms/MTU")
print(f"Error: {error_percent:.1f}%")

# PASS if < 10%
assert error_percent < 10, "Fission product yield error"
```

---

### Check 7: Decay Heat

**Principle**: Decay heat should match standard correlations

**ANS-5.1 decay heat standard** (approximate):

```python
# Decay heat power (MW/MTU) vs. time after shutdown
def ans_51_decay_heat(time_since_shutdown_days, burnup_GWd_MTU, power_MW_MTU):
    """
    ANS-5.1 decay heat correlation (simplified)
    time_since_shutdown_days: days since reactor shutdown
    burnup_GWd_MTU: burnup in GWd/MTU
    power_MW_MTU: specific power in MW/MTU
    """
    t = time_since_shutdown_days * 86400  # Convert to seconds

    # Simplified correlation (actual ANS-5.1 more complex)
    P_decay = power_MW_MTU * (0.0622 * t**(-0.2) +
                               0.00277 * burnup_GWd_MTU / power_MW_MTU)

    return P_decay

# Example
burnup = 45.0  # GWd/MTU
power = 40.0   # MW/MTU
time = 30      # days post-shutdown

P_decay_expected = ans_51_decay_heat(time, burnup, power)
print(f"Expected decay heat (ANS-5.1): {P_decay_expected:.4f} MW/MTU")

# From ORIGEN output (sum of all isotope decay powers)
P_decay_calculated = 0.0125  # MW/MTU (from ORIGEN)

error_percent = abs(P_decay_calculated - P_decay_expected) / P_decay_expected * 100

print(f"Calculated decay heat (ORIGEN): {P_decay_calculated:.4f} MW/MTU")
print(f"Error: {error_percent:.1f}%")

# PASS if < 15% (decay heat has large uncertainty)
assert error_percent < 15, "Decay heat error out of range"
```

**Typical decay heat** (PWR, 45 GWd/MTU):
- At shutdown: 6.5% of operating power
- 1 day: 1.5%
- 30 days: 0.5%
- 1 year: 0.2%
- 10 years: 0.05%

---

## Level 2: Code-to-Code Comparisons

### Comparison 1: MCNP vs. Serpent

**Setup**: Run identical problem with Serpent Monte Carlo code

**MCNP input**: input_mcnp.i

**Serpent equivalent**: input_serpent.i

```serpent
% Serpent 2 input (equivalent to MCNP)
set title "PWR Pin Burnup - Serpent Validation"

% Geometry (identical to MCNP)
surf 1 cyl 0 0 0.41
surf 2 cyl 0 0 0.48
cell 1 0 fuel  -1
cell 2 0 clad   1 -2
cell 3 0 void   2

% Materials
mat fuel -10.4
92234.70c  3.6e-4
92235.70c  0.045
92238.70c  0.955
 8016.70c  2.0

% Burnup
dep daystep 100 100 100 100 100 40
set power 7.72  % MW

% Source
set nps 10000 100 20
```

**Run both**:
```bash
mcnp6 i=input_mcnp.i o=output_mcnp.o
sss2 input_serpent.i
```

**Compare results**:
```python
# k_eff comparison
k_mcnp = [1.2500, 1.1800, 1.1200, 1.0750, 1.0523]
k_serpent = [1.2512, 1.1810, 1.1195, 1.0745, 1.0530]

for i, (km, ks) in enumerate(zip(k_mcnp, k_serpent)):
    diff_pcm = (km - ks) / (km * ks) * 1e5
    print(f"Step {i}: MCNP={km:.4f}, Serpent={ks:.4f}, Δ={diff_pcm:.0f} pcm")

# PASS if all differences < 200 pcm (within statistical uncertainty)
```

**Typical agreement**: ± 100-200 pcm (statistical + nuclear data differences)

---

### Comparison 2: ORIGEN vs. SCALE/TRITON

**Setup**: Run SCALE/TRITON depletion sequence

**SCALE input**: triton_validation.inp

```scale
=t-depl parm=(centrm)
PWR Pin Burnup - SCALE TRITON Validation
v7-238
read comp
  uo2 1 den=10.4 1 900 92235 4.5 92238 95.5 end
  zirc4 2 1 622 end
  h2o 3 den=0.74 1 579 end
end comp
read celldata
  latticecell squarepitch fueld=0.82 1 cladd=0.96 2 gapd=0.84 0 pitch=1.26 3 end
end celldata
read depletion
  1
end depletion
read burndata
  power=40.0 burn=540 nlib=8 end
end burndata
read model
  read materials
    1 den=10.4 1 900 end
  end materials
end model
end
```

**Compare**:
- k_eff vs. burnup
- Isotopic compositions (Pu-239, Pu-240, Pu-241)
- Fission product inventories

**Typical agreement**: < 1% for isotopes, < 100 pcm for k_eff

---

### Comparison 3: MCNP vs. CASMO/SIMULATE

**Setup**: Lattice physics code comparison (for PWR assemblies)

**CASMO-5 equivalent**: casmo_validation.inp

```casmo
* PWR 17x17 Assembly Burnup
TTL 'MCNP Validation Case'
TFU 900  $ Fuel temperature (K)
TMO 579  $ Moderator temperature (K)
PDE 40.0 $ Power density (kW/kgU)
BOR 0    $ Boron concentration (ppm)

* Geometry
PIN 1
  UO2/4.5  0.4095  /  ZR  0.4180 0.4750
END

* Lattice
LPI 1 1 1 1 ... (17x17 pattern)

* Burnup
DEP -10 10000 20000 30000 40000 50000 54000

* Output
STA
```

**Compare**:
- Assembly k_inf vs. burnup
- Pin power distribution
- Isotopic compositions

**Typical agreement**: < 200 pcm, < 5% pin powers

---

## Level 3: Experimental Benchmarks

### Benchmark 1: Critical Experiment (k_eff)

**Example**: PNL-33 Critical Experiment (ICSBEP Handbook)

**Description**: Array of fuel rods at various spacings, critical configuration

**MCNP model**: Use benchmark specification exactly

**Comparison**:
```
Experiment:  k_eff = 1.0000 ± 0.0010 (by definition, critical)
MCNP calc:   k_eff = 1.0015 ± 0.0008

Difference: 150 pcm (within experimental + calculational uncertainty)

C/E ratio: 1.0015 / 1.0000 = 1.0015

PASS if 0.995 < C/E < 1.005 (± 500 pcm)
```

---

### Benchmark 2: Burnup Measurement (Isotopic Assay)

**Example**: ARIANE Program (PWR spent fuel assays)

**Measured data**: Destructive isotopic analysis of spent fuel samples

**Comparison**:
```python
# Measured vs. calculated isotopic composition (atoms/initial U atom)

isotope_comparison = {
    'U-235': {'measured': 0.0083, 'calculated': 0.0080, 'error%': -3.6},
    'U-236': {'measured': 0.0051, 'calculated': 0.0050, 'error%': -2.0},
    'U-238': {'measured': 0.9410, 'calculated': 0.9400, 'error%': -0.1},
    'Pu-239': {'measured': 0.0061, 'calculated': 0.0060, 'error%': -1.6},
    'Pu-240': {'measured': 0.0031, 'calculated': 0.0030, 'error%': -3.2},
    'Pu-241': {'measured': 0.0021, 'calculated': 0.0020, 'error%': -4.8},
    'Pu-242': {'measured': 0.00083, 'calculated': 0.00080, 'error%': -3.6},
    'Nd-148': {'measured': 1.32e-6, 'calculated': 1.30e-6, 'error%': -1.5},
    'Cs-137': {'measured': 1.25e-6, 'calculated': 1.23e-6, 'error%': -1.6}
}

for iso, data in isotope_comparison.items():
    print(f"{iso:8s}: Meas={data['measured']:.4e}, "
          f"Calc={data['calculated']:.4e}, Error={data['error%']:.1f}%")

# PASS if all errors < 10% (typical for destructive assay)
```

**Acceptance**: < 5% for major isotopes, < 10% for minor isotopes

---

### Benchmark 3: Dose Rate Measurement

**Example**: AGR-1 Post-Irradiation Examination

**Measured data**: Contact dose rates on capsules after decay

**Comparison**:
```
Measurement location: Capsule 3, 30 days post-discharge
Measured dose rate:  12.5 ± 2.5 mSv/hr (thermoluminescent dosimeter)
Calculated (MCNP):   11.8 ± 0.6 mSv/hr (statistical uncertainty)

C/E ratio: 11.8 / 12.5 = 0.94
Error: -5.6%

PASS if C/E between 0.8 and 1.2 (± 20%)
(Dose rates have large measurement uncertainty)
```

**Dominant contributors**:
- Cs-137 (661 keV gamma): 85%
- Ba-140 (short-lived): 10%
- Co-60 (structural activation): 5%

---

### Benchmark 4: Burnup Monitor (FIMA)

**Example**: AGR-1 FIMA (Fissions per Initial Metal Atom)

**Measured**: From Nd-148 analysis (stable fission product)

**Calculated**: From MCNP/ORIGEN burnup

**Comparison**:
```
Capsule  Compact  FIMA_meas   FIMA_calc   C/E     Error%
-------  -------  ----------  ----------  ------  ------
1        1        0.1123      0.1145      1.020   +2.0%
1        2        0.1089      0.1102      1.012   +1.2%
2        1        0.1456      0.1478      1.015   +1.5%
2        2        0.1423      0.1441      1.013   +1.3%
3        1        0.1789      0.1821      1.018   +1.8%
3        2        0.1756      0.1783      1.015   +1.5%

Average C/E: 1.016
Standard deviation: 0.003

PASS: All within 5%, average bias < 2%
```

---

## Validation Report Template

**Document**: `burnup_validation_report.md`

```markdown
# Burnup Calculation Validation Report

**Project**: [Project name]
**Date**: [Date]
**Analyst**: [Name]

## Summary

This report documents the validation of MCNP/ORIGEN burnup calculations for [reactor type] fuel at [burnup] GWd/MTU.

## Internal Consistency Checks

| Check | Target | Result | Status |
|-------|--------|--------|--------|
| Reactivity balance | < 500 pcm | 234 pcm | PASS |
| HM mass balance | < 2% | 0.8% | PASS |
| Power normalization | < 5% | 1.2% | PASS |
| Conversion ratio | 0.5-0.8 | 0.63 | PASS |
| Pu vector | See ranges | Within | PASS |

## Code-to-Code Comparison

| Code | k_eff (BOL) | k_eff (EOL) | Pu-239 (%) | Status |
|------|-------------|-------------|------------|--------|
| MCNP | 1.2500 ± 0.0008 | 1.0523 ± 0.0008 | 56.2 | Reference |
| Serpent | 1.2512 ± 0.0010 | 1.0530 ± 0.0010 | 56.0 | PASS (< 200 pcm) |
| SCALE | 1.2485 ± 0.0015 | 1.0510 ± 0.0015 | 55.8 | PASS |

## Experimental Benchmark

| Parameter | Measured | Calculated | C/E | Status |
|-----------|----------|------------|-----|--------|
| Burnup (GWd/MTU) | 45.2 ± 1.5 | 45.0 ± 0.5 | 0.996 | PASS |
| U-235 depletion | 82.3% | 82.2% | 0.999 | PASS |
| Pu-239 buildup (g/MTU) | 6020 ± 300 | 6000 ± 50 | 0.997 | PASS |

## Conclusion

All validation criteria met. Calculation suitable for [intended application].

**Limitations**:
- Burnup range: 0-60 GWd/MTU
- Enrichment range: 3-5% U-235
- Reactor type: PWR only

**Recommendation**: APPROVED for use
```

---

## References

- OECD/NEA: Spent Fuel Isotopic Composition Database
- ICSBEP: International Criticality Safety Benchmark Evaluation Project
- SFCOMPO: Spent Fuel Composition Database
- ARIANE Programme: PWR UO₂ Fuel Isotopic Assays
- AGR-1 NGNP Fuel Test PIE Report (INL/EXT-15-35597)
- ANS-5.1: Decay Heat Power in Light Water Reactors
- NUREG/CR-6801: Burnup Credit Criticality Benchmarks
