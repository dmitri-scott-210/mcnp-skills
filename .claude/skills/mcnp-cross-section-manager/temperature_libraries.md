# Temperature-Dependent Cross-Section Libraries

## Overview

Cross-section data depends on temperature due to Doppler broadening of resonances. MCNP provides temperature-specific libraries for accurate high-temperature calculations. Understanding temperature library selection is critical for reactor physics and high-temperature systems.

## Standard Temperature Libraries

| Library | Temperature (K) | Temperature (°C) | kT (eV) | Typical Application |
|---------|----------------|------------------|---------|---------------------|
| .80c    | 293.6 K        | 20.4°C          | 0.0253  | Room temperature, cold critical |
| .81c    | 600 K          | 327°C           | 0.0517  | Moderate temp reactors |
| .82c    | 900 K          | 627°C           | 0.0776  | PWR/BWR operating conditions |
| .83c    | 1200 K         | 927°C           | 0.1034  | High temp gas reactors |
| .84c    | 2500 K         | 2227°C          | 0.2154  | Very high temp systems |

Additional variants (.85c, .86c, .87c) available for some isotopes at intermediate temperatures.

## Temperature Effects

### Doppler Broadening

**Physical Effect:**
- Higher temperature → increased thermal motion
- Resonances broaden (width increases)
- Peak cross sections decrease
- Integral cross sections approximately constant

**Impact on Reactivity:**
```
U-238 Resonance Capture:
  T increases → Resonances broader → More capture
  Result: Negative temperature coefficient (safety feature)

Example:
  300 K: σ_capture(peak) = 10,000 b
  900 K: σ_capture(peak) = 8,500 b (broader, lower peak)
```

### Temperature Coefficient

**Doppler Coefficient:**
```
αT = (1/k) × (∂k/∂T)

Typical values:
  PWR: αT ≈ -3 to -5 pcm/K (negative = stable)
  Fast reactor: αT ≈ -0.5 to -1 pcm/K
```

## Library Availability

### Well-Covered Isotopes

**Fissile/Fertile (Full temperature range):**
- U-233, U-234, U-235, U-238
- Pu-238, Pu-239, Pu-240, Pu-241, Pu-242
- Th-232

**Structural Materials:**
- Fe, Cr, Ni (stainless steel components)
- Zr (cladding)
- O-16 (oxide fuels)

### Limited Coverage

**Fission Products:** Often only .80c available
**Minor Actinides:** Variable coverage
**Light Elements:** Generally .80c to .84c

## Selection Guidelines

### Temperature Range Recommendations

```
System Temperature     Recommended Library    Alternative
─────────────────     ───────────────────    ───────────
T < 400 K             .80c                   .80c + TMP
400 K ≤ T < 750 K     .81c                   .82c or .80c + TMP
750 K ≤ T < 1050 K    .82c                   .83c or .81c + TMP
1050 K ≤ T < 1800 K   .83c                   .84c or .82c + TMP
T ≥ 1800 K            .84c                   .83c + TMP

General rule: Use library closest to system temperature
```

### TMP Card Interpolation

**When to Use TMP:**
```
1. Exact temperature library not available
2. System temperature between library points
3. Minor temperature adjustment (<100 K)

Example:
M1  92235.80c  1.0     $ 293.6 K library
TMP  400               $ MCNP interpolates to 400 K
```

**Limitations:**
```
- Less accurate than native library
- Interpolation errors increase with distance
- Do NOT extrapolate beyond library range
- TMP does NOT affect thermal scattering (S(α,β))
```

## Use Case Examples

### PWR Operating Conditions
```
Core: 580 K (307°C)
Reflector: 550 K (277°C)

Fuel (high importance):
M1  92235.82c  0.045   $ U-235 at 900 K
    92238.82c  0.955   $ U-238 at 900 K (conservative)
    8016.82c   2.0     $ O-16 at 900 K
TMP  580               $ Adjust to exact temperature

Reflector (lower sensitivity):
M2  1001.80c  2.0      $ H-1 (room temp OK)
    8016.80c  1.0      $ O-16
MT2  lwtr.86t          $ Use 573.6 K thermal (closest)
TMP  550               $ Neutron adjust to 550 K
c Note: TMP does NOT affect lwtr.86t
```

### HTGR (High Temperature Gas Reactor)
```
Core: 1200 K (927°C)

Fuel:
M1  92235.83c  0.20    $ U-235 at 1200 K (exact)
    92238.83c  0.80    $ U-238 at 1200 K

Graphite:
M2  6000.83c  1.0      $ C at 1200 K
MT2  grph.83t          $ Graphite S(α,β) at 1200 K (if available)
```

## Checking Availability

### Bash Method
```bash
# Check what temperatures available for U-235
grep "92235\." $DATAPATH/xsdir | awk '{print $1, $NF}'

# Output:
# 92235.80c  2.5301E-08  (293.6 K)
# 92235.81c  5.1704E-08  (600 K)
# 92235.82c  7.7559E-08  (900 K)
# 92235.83c  1.0341E-07  (1200 K)
```

### Python Method
```python
def find_temperature_libraries(isotope_zaid, datapath):
    """Find all temperature variants for isotope"""
    base = isotope_zaid.split('.')[0]  # e.g., '92235'
    lib_type = isotope_zaid[-1]  # e.g., 'c'

    xsdir_path = os.path.join(datapath, 'xsdir')
    variants = []

    with open(xsdir_path, 'r') as f:
        for line in f:
            if line.startswith(base) and line.endswith(lib_type):
                parts = line.split()
                zaid = parts[0]
                temp_mev = float(parts[7])
                temp_k = temp_mev / 8.617333e-11

                variants.append({
                    'zaid': zaid,
                    'temperature_k': temp_k,
                    'temperature_c': temp_k - 273.15
                })

    return sorted(variants, key=lambda x: x['temperature_k'])
```

## Thermal Scattering Temperature

**Critical Distinction:**
```
NEUTRON libraries (.nnc):    Affected by TMP card
THERMAL libraries (.nnT):    NOT affected by TMP card

Must select correct .nnT temperature explicitly
```

**Example (Water at 580 K):**
```
WRONG:
M1  1001.80c  2.0
    8016.80c  1.0
MT1  lwtr.80t          $ 293.6 K (WRONG!)
TMP  580               $ TMP does NOT change lwtr.80t

RIGHT:
M1  1001.80c  2.0
    8016.80c  1.0
MT1  lwtr.86t          $ 573.6 K (closest to 580 K)
TMP  580               $ Only affects .80c, not lwtr.86t
```

## Best Practices

1. **Use Native Libraries** - Prefer exact temperature over TMP interpolation
2. **Prioritize Important Isotopes** - Fuel isotopes more critical than structural
3. **Match Moderator Temps** - Use correct .nnT temperature for thermal scattering
4. **Document Choices** - Comment temperature selection rationale
5. **Stay Within Range** - Don't interpolate beyond library bounds
6. **Test Sensitivity** - Check if temperature library choice affects results
7. **Consistent Versions** - All .82c or all .83c, not mixed
8. **Validate keff** - Compare with/without temperature effects

## Temperature Conversion

```
Kelvin to Celsius:    T(°C) = T(K) - 273.15
Celsius to Kelvin:    T(K) = T(°C) + 273.15
Fahrenheit to Kelvin: T(K) = (T(°F) - 32) × 5/9 + 273.15

kT (eV) to Kelvin:    T(K) = kT(eV) / 8.617333E-5
Kelvin to kT (eV):    kT(eV) = T(K) × 8.617333E-5

xsdir temperature:    kT(MeV) = kT(eV) × 1E-6
```

## Troubleshooting

**Issue: Temperature library not available**
```
Solution 1: Use closest available + TMP
M1  92238.82c  1.0     $ 900 K library
TMP  1000              $ Interpolate to 1000 K

Solution 2: Check if alternate version has it
grep "92238.*c" xsdir  # Check all versions
```

**Issue: Mixed temperatures in problem**
```
Different regions at different temperatures - OK!

Core (900 K):
M1  92235.82c  1.0
TMP  900

Reflector (600 K):
M2  1001.81c  2.0
TMP  600
```

**Issue: Thermal scattering at wrong temperature**
```
Symptom: keff off by 1-3%
Cause: lwtr.80t (293 K) used but water at 580 K
Fix: Use lwtr.86t (573.6 K)
```

---

**See also:**
- `library_types.md` - Library type reference
- `xsdir_format.md` - Temperature encoding in xsdir
- `troubleshooting_libraries.md` - Temperature-related errors
