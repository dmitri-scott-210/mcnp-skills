# Physical Unit Systems for MCNP

Overview of SI, CGS, and Imperial/US unit systems and their relationship to MCNP conventions. Understanding these systems helps prevent unit conversion errors.

---

## Overview of Unit Systems

### SI Units (Système International)

**Base Units:**
- Length: meter (m)
- Mass: kilogram (kg)
- Time: second (s)
- Temperature: kelvin (K)
- Electric current: ampere (A)
- Amount of substance: mole (mol)
- Luminous intensity: candela (cd)

**Derived Units:**
- Force: newton (N) = kg·m/s²
- Energy: joule (J) = kg·m²/s² = N·m
- Power: watt (W) = J/s
- Pressure: pascal (Pa) = N/m²

**Used in:** International standard, most scientific work

### CGS Units (Centimeter-Gram-Second)

**Base Units:**
- Length: centimeter (cm)
- Mass: gram (g)
- Time: second (s)

**Derived Units:**
- Force: dyne (dyn) = g·cm/s²
- Energy: erg = g·cm²/s² = dyn·cm
- Power: erg/s
- Pressure: barye (Ba) = dyn/cm²

**Used in:** Older physics texts, some nuclear engineering

### Imperial/US Customary Units

**Base Units:**
- Length: inch, foot, yard, mile
- Mass: pound-mass (lbm), slug
- Time: second (s)
- Temperature: Fahrenheit (°F) or Rankine (°R)

**Derived Units:**
- Force: pound-force (lbf)
- Energy: British thermal unit (BTU), foot-pound
- Power: horsepower (hp)
- Pressure: pounds per square inch (psi)

**Used in:** United States engineering, some industrial applications

---

## MCNP Unit System

MCNP uses a **hybrid system**, primarily based on CGS with nuclear physics conventions:

| Quantity | MCNP Choice | System Origin | Rationale |
|----------|-------------|---------------|-----------|
| Length | **cm** | CGS | Typical nuclear dimensions |
| Mass | **g or amu** | CGS / Nuclear | Material specifications |
| Time | **shake (10⁻⁸ s)** | Nuclear | Neutron generation time |
| Energy | **MeV** | Nuclear | Particle energies |
| Temperature | **K or MeV** | SI / Nuclear | Both accepted |
| Density (mass) | **g/cm³** | CGS | Standard materials |
| Density (atomic) | **atom/(b-cm)** | Nuclear | Cross sections |
| Cross section | **barn (10⁻²⁴ cm²)** | Nuclear | Nuclear interaction scale |
| Activity | **Bq or Ci** | SI / Historical | Radioactivity |

**Philosophy:** MCNP chooses units that are most natural for the physics being modeled while maintaining consistency within calculations.

---

## Conversion Between Systems

### Length Conversions

| From SI (m) | To CGS (cm) | To Imperial (in) |
|-------------|-------------|------------------|
| × 100 | = cm | × 39.37 = inches |
| 1 m | 100 cm | 39.37 in |
| 0.01 m | 1 cm | 0.3937 in |
| 0.0254 m | 2.54 cm | 1 in |

**MCNP Example:**
- Reactor vessel diameter: 4.5 m → **450 cm** (for MCNP)

### Mass Conversions

| From SI (kg) | To CGS (g) | To Imperial (lbm) |
|--------------|------------|-------------------|
| × 1000 | = g | × 2.205 = lbm |
| 1 kg | 1000 g | 2.205 lbm |
| 0.001 kg | 1 g | 0.002205 lbm |
| 0.4536 kg | 453.6 g | 1 lbm |

**MCNP Example:**
- Fuel mass: 50 kg → **50,000 g** (if needed)
- Typically use amu or densities instead

### Energy Conversions

| From SI (J) | To Nuclear (MeV) | To CGS (erg) | To Imperial (BTU) |
|-------------|------------------|--------------|-------------------|
| × 6.242×10¹² | = MeV | × 10⁷ = erg | × 9.478×10⁻⁴ = BTU |
| 1 J | 6.242×10¹² MeV | 10⁷ erg | 9.478×10⁻⁴ BTU |
| 1.602×10⁻¹³ J | 1 MeV | 1.602×10⁻⁶ erg | 1.519×10⁻¹⁶ BTU |

**MCNP Example:**
- Thermal energy at 300 K: 0.0259 eV → **2.59×10⁻⁸ MeV** (for TMP card)

### Density Conversions

| From SI (kg/m³) | To CGS (g/cm³) | To Imperial (lbm/ft³) |
|-----------------|----------------|-----------------------|
| × 0.001 | = g/cm³ | × 0.06243 = lbm/ft³ |
| 1000 kg/m³ | 1 g/cm³ | 62.43 lbm/ft³ |
| 7850 kg/m³ | 7.85 g/cm³ | 489.9 lbm/ft³ |

**MCNP Example:**
- Steel: 7850 kg/m³ → **-7.85 g/cm³** (negative for mass density)

### Temperature Conversions

| From SI (K) | To Imperial (°F) | To Nuclear (MeV) |
|-------------|------------------|------------------|
| × 9/5 - 459.67 | = °F | × 8.617×10⁻¹¹ = MeV |
| 273.15 K | 32 °F | 2.35×10⁻⁸ MeV |
| 293.15 K | 68 °F | 2.53×10⁻⁸ MeV |
| 373.15 K | 212 °F | 3.21×10⁻⁸ MeV |

**From °C to K:** K = °C + 273.15
**From °F to K:** K = (°F + 459.67) × 5/9

**MCNP Example:**
- Operating temperature: 300°C → **573.15 K** (for TMP card)

---

## System Comparison Table

### Base Quantities

| Quantity | SI | CGS | Imperial | MCNP |
|----------|-----|-----|----------|------|
| Length | m | cm | ft | **cm** |
| Mass | kg | g | lbm | **g or amu** |
| Time | s | s | s | **s or shake** |
| Temperature | K | K | °F/°R | **K or MeV** |
| Electric current | A | esu/s | A | **not used** |
| Substance amount | mol | mol | mol | **mol (rare)** |

### Derived Quantities

| Quantity | SI | CGS | MCNP |
|----------|-----|-----|------|
| Area | m² | cm² | **cm²** |
| Volume | m³ | cm³ | **cm³** |
| Velocity | m/s | cm/s | **cm/s** |
| Acceleration | m/s² | cm/s² | **cm/s²** |
| Force | N | dyn | **not used** |
| Energy | J | erg | **MeV** |
| Power | W | erg/s | **MeV/s or W** |
| Pressure | Pa | Ba | **atm (rare)** |
| Density | kg/m³ | g/cm³ | **g/cm³** |
| Current density | A/m² | esu/(cm²·s) | **particles/cm²** |

---

## Nuclear Physics Units

### Special Units for Nuclear Phenomena

| Unit | Value | Quantity | Usage |
|------|-------|----------|-------|
| **MeV** | 1.602×10⁻¹³ J | Energy | Particles, reactions |
| **barn (b)** | 10⁻²⁴ cm² | Cross section | Interaction probability |
| **amu (u)** | 931.494 MeV/c² | Mass | Atomic/nuclear masses |
| **shake** | 10⁻⁸ s | Time | Neutron lifetimes |
| **Curie (Ci)** | 3.7×10¹⁰ Bq | Activity | Radioactive sources |
| **Becquerel (Bq)** | 1 s⁻¹ | Activity | SI radioactivity |
| **fermis (fm)** | 10⁻¹⁵ m = 10⁻¹³ cm | Length | Nuclear dimensions |

### Why These Units?

**MeV:** Convenient for particle energies
- Thermal neutron: 0.025 eV
- Fission neutron: ~2 MeV
- Avoids tiny numbers in joules (10⁻¹³ to 10⁻¹⁹ range)

**barn:** Natural scale for nuclear cross sections
- Nuclear radius: ~10⁻¹² cm → area ~10⁻²⁴ cm²
- Typical cross sections: 1–10,000 barns

**shake:** Natural time scale for neutron reactions
- Neutron speed at 1 MeV: ~1.4×10⁹ cm/s
- Mean free path ~2.5 cm → transit time ~2 shakes

---

## Dimensional Analysis

### Fundamental Dimensions

| Quantity | SI Dimensions | CGS Dimensions | MCNP Dimensions |
|----------|---------------|----------------|-----------------|
| Length [L] | m | cm | cm |
| Mass [M] | kg | g | g or amu |
| Time [T] | s | s | shake or s |
| Temperature [Θ] | K | K | K or MeV |
| Energy [E] | kg·m²/s² | g·cm²/s² | MeV |

### Derived Dimensions

| Quantity | Dimensions | SI | CGS | MCNP |
|----------|------------|-----|-----|------|
| Velocity | [L]/[T] | m/s | cm/s | cm/s |
| Acceleration | [L]/[T]² | m/s² | cm/s² | cm/s² |
| Force | [M][L]/[T]² | N = kg·m/s² | dyn = g·cm/s² | - |
| Energy | [M][L]²/[T]² | J = kg·m²/s² | erg = g·cm²/s² | MeV |
| Power | [M][L]²/[T]³ | W = J/s | erg/s | MeV/s |
| Density | [M]/[L]³ | kg/m³ | g/cm³ | g/cm³ |
| Flux | 1/([L]²[T]) | n/(m²·s) | n/(cm²·s) | n/(cm²·s) |
| Cross section | [L]² | m² | cm² | barn = 10⁻²⁴ cm² |

---

## Common Conversion Pitfalls

### Pitfall 1: Inconsistent Length Units

**Problem:** Mixing meters and centimeters in geometry

**Example (BAD):**
```mcnp
c Cylinder: radius 2.5 m, height 5 m
10  CZ   2.5          $ Wrong! This is 2.5 cm
20  PZ   500          $ This is correct (500 cm = 5 m)
```

**Fix:**
```mcnp
c Cylinder: radius 2.5 m = 250 cm, height 5 m = 500 cm
10  CZ   250          $ Correct
20  PZ   500          $ Correct
```

### Pitfall 2: Density System Confusion

**Problem:** Using kg/m³ directly instead of converting to g/cm³

**Example (BAD):**
```mcnp
c Steel at 7850 kg/m³
10  1  -7850  -100    $ Wrong! This interprets as 7850 g/cm³ (impossible)
```

**Fix:**
```mcnp
c Steel: 7850 kg/m³ = 7.85 g/cm³
10  1  -7.85  -100    $ Correct
```

### Pitfall 3: Energy Unit Mismatch

**Problem:** Using eV or keV without converting to MeV

**Example (BAD):**
```mcnp
c 14.1 keV neutron source
SDEF  ERG=14.1        $ Wrong! This is 14.1 MeV
```

**Fix:**
```mcnp
c 14.1 keV = 0.0141 MeV
SDEF  ERG=0.0141      $ Correct
```

### Pitfall 4: Temperature Scales

**Problem:** Using Celsius without converting to Kelvin

**Example (BAD):**
```mcnp
c Material at 300°C
TMP  300              $ Wrong if you meant °C (this is 300 K ≈ 27°C)
```

**Fix:**
```mcnp
c 300°C = 573.15 K
TMP  573.15           $ Correct
```

---

## Best Practices for Unit Consistency

### 1. Choose One System and Stick to It

**Recommended for MCNP:**
- Geometry: **cm**
- Mass density: **g/cm³**
- Energy: **MeV**
- Temperature: **K**
- Time: **shakes** (for time bins)

### 2. Document Conversions

```mcnp
c ========================================
c UNIT CONVERSIONS
c ========================================
c Tank dimensions:
c   Original: 4.5 m diameter, 10 m height
c   MCNP: 450 cm diameter, 1000 cm height
c Material density:
c   Original: 7850 kg/m³ (steel)
c   MCNP: 7.85 g/cm³
c Source energy:
c   Original: 14.1 keV
c   MCNP: 0.0141 MeV
c ========================================
```

### 3. Use Conversion Tools

- **Automated:** Use `unit_converter.py` (in scripts/ directory)
- **Manual:** Use conversion_tables.md for reference
- **Validation:** Use `mcnp_unit_checker.py` to catch errors

### 4. Verify Dimensional Consistency

Before running MCNP, check that:
- All lengths in geometry are in **cm**
- All densities follow sign convention (negative = g/cm³, positive = atom/b-cm)
- All energies are in **MeV**
- All temperatures are in **K** or **MeV**
- All time bins are in **shakes**

### 5. Cross-Check with Physical Intuition

**Does the result make sense?**
- Density: 0.001–25 g/cm³ (air to osmium)
- Energy: 10⁻⁸ to 100 MeV (thermal to high energy)
- Dimensions: reasonable for problem scale

---

## Quick Reference: System Conversions

### SI → MCNP

| SI Unit | × Factor | MCNP Unit |
|---------|----------|-----------|
| m | 100 | cm |
| kg/m³ | 0.001 | g/cm³ |
| J | 6.242×10¹² | MeV |
| K | 1 | K (same) |
| K | 8.617×10⁻¹¹ | MeV |

### CGS → MCNP

| CGS Unit | × Factor | MCNP Unit |
|----------|----------|-----------|
| cm | 1 | cm (same) |
| g/cm³ | 1 | g/cm³ (same) |
| erg | 6.242×10⁵ | MeV |
| K | 1 | K (same) |

### Imperial → MCNP

| Imperial Unit | × Factor | MCNP Unit |
|---------------|----------|-----------|
| inch | 2.54 | cm |
| ft | 30.48 | cm |
| lbm/ft³ | 0.01602 | g/cm³ |
| BTU | 6.585×10¹⁵ | MeV |

---

## Summary

**Key Takeaways:**
1. MCNP uses a **hybrid** system: CGS-like for geometry/materials, nuclear units for energy
2. Always convert to MCNP standard units **before** creating input
3. Document all conversions in comments
4. Use tools (unit_converter.py, mcnp_unit_checker.py) to prevent errors
5. When in doubt, stick to **cm, g/cm³, MeV, K, shakes**

**Remember:** Unit errors are among the most common MCNP mistakes! Double-check conversions and use validation tools.

---

**Last Updated:** 2025-11-06
**References:**
- MCNP 6.3 User Manual (units conventions)
- NIST Guide to the SI (SI units)
- CRC Handbook of Chemistry and Physics (conversions)
