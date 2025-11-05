# Example 4: Temperature-Dependent Physics with DBRC

## Purpose
Demonstrates temperature-dependent cross sections using TMP and DBRC cards for accurate high-temperature reactor physics.

## Key Features
- **TMP cards**: Different temperatures for fuel, cladding, and coolant
- **DBRC card**: Doppler Broadening Rejection Correction for U-238 resonances
- **Geometry**: Fuel pin cell (fuel pellet, cladding, coolant)
- **Materials**: UO₂ fuel (3% enriched), Zircaloy cladding, light water
- **Source**: Watt fission spectrum
- **Tallies**: Flux in fuel, cladding, and coolant regions

## Physics Settings Explained

### TMP Card - Temperature Specification

**TMP Format**: Temperature in MeV (not Kelvin!)
```
Temperature [MeV] = Temperature [K] × 8.617×10⁻¹¹
```

**This Example**:
- `TMP1 2.533e-8`: Fuel at 900K (high operating temperature)
- `TMP2 2.92e-8`: Cladding at 900K (assumes no temperature drop)
- `TMP3 2.533e-8`: Water at 293K (room temperature, error - should be ~600K for PWR)

**Temperature Conversion Table**:
| Kelvin | MeV (k×T) | Application |
|--------|-----------|-------------|
| 293 K  | 2.53×10⁻⁸ | Room temperature |
| 600 K  | 5.17×10⁻⁸ | Hot coolant (PWR) |
| 900 K  | 7.76×10⁻⁸ | Fuel operating temperature |
| 1200 K | 1.03×10⁻⁷ | High burnup fuel |

### DBRC Card - Enhanced Resonance Treatment

**DBRC Format**: Lists isotopes requiring enhanced Doppler broadening
```
DBRC endf=80 emax=2.1e-7
```

**Parameters**:
- `endf=80`: ENDF/B-VIII.0 library identifier
- `emax=2.1e-7`: Maximum energy for DBRC (210 eV)
  - DBRC applied in resolved resonance region (typically <10 keV)
  - emax=210 eV covers U-238 dominant resonances

**Why DBRC for U-238**:
- U-238 has strong resonances between 5-100 eV
- Temperature significantly affects resonance widths (Doppler broadening)
- Standard treatment uses 0K cross sections with approximations
- DBRC: Rejection correction on-the-fly for exact temperature-dependent physics

## Physical Effects

### Temperature Impact on Cross Sections

1. **Doppler Broadening**:
   - Higher temperature → atoms have higher thermal motion
   - Cross-section resonances become wider and lower peaks
   - Net effect: Increased resonance absorption (negative temperature coefficient)

2. **Thermal Scattering**:
   - Water S(α,β) depends strongly on temperature
   - MT card must match TMP temperature
   - Example: LWTR.01T (293K), LWTR.04T (600K), LWTR.12T (900K)

### Criticality Impact
- Fuel temperature coefficient: -1 to -3 pcm/K (negative, stabilizing)
- Coolant temperature coefficient: -10 to -30 pcm/K (negative, stabilizing)
- DBRC improves accuracy by ~50-200 pcm (0.05-0.2% Δk/k)

## When to Use TMP and DBRC

### Always Use TMP When:
- Material temperature ≠ 293K (room temperature)
- High-temperature applications (>600K)
- Accurate criticality calculations required
- Reactor physics (fuel, coolant, moderator all at different temperatures)
- Temperature coefficient calculations

### Use DBRC When:
- High-temperature fuel (>600K)
- Accurate criticality calculations (keff uncertainty <50 pcm)
- U-238, Pu-240, or other resonance-dominated isotopes present
- Reactor physics benchmarks or validation

### Skip DBRC When:
- Shielding problems (small keff impact)
- Fast spectrum (resonances less important)
- Computational time critical and accuracy requirements relaxed

## Important Consistency Requirements

### TMP and MT Must Match
```
c WRONG:
M1  1001  2  8016  1
MT1  H-H2O.40t             $ S(α,β) at 293K
TMP1  5.17e-8              $ Temperature = 600K (MISMATCH!)

c CORRECT:
M1  1001  2  8016  1
MT1  H-H2O.43t             $ S(α,β) at 600K
TMP1  5.17e-8              $ Temperature = 600K (consistent)
```

### Available S(α,β) Temperatures
Water (H-H2O):
- .40t → 293.6K
- .41t → 350K
- .42t → 400K
- .43t → 450K
- .44t → 500K
- .45t → 550K
- .46t → 600K
- .47t → 650K
- .48t → 800K

## Expected Behavior
- Fuel at 900K: Broadened U-238 resonances increase absorption slightly
- DBRC improves accuracy in resolved resonance region (1 eV - 10 keV)
- Coolant at 293K (should be 600K for realism): Thermal scattering appropriate
- Flux tallies show spatially-dependent spectrum (hardening in fuel, thermalization in water)

## Computational Cost
- TMP card: Negligible cost (uses temperature-dependent tables)
- DBRC: ~10-20% slower (rejection correction sampling)
- Trade-off: Improved accuracy justifies modest cost for criticality calculations
