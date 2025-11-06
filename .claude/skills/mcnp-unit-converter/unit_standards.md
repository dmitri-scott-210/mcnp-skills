# MCNP Unit Standards by Card Type

Quick reference guide for expected units on each MCNP card. Use this to ensure correct unit specifications when building or checking MCNP inputs.

---

## Cell Cards (Block 1)

### Format
```
cell_num  mat_num  density  geometry
```

### Density Units

| Sign | Unit | Example | Notes |
|------|------|---------|-------|
| **Negative** | g/cm³ | `-7.85` | Mass density (steel) |
| **Positive** | atom/b-cm | `0.0602` | Atomic density (Al) |
| **Zero** | void | `0` | No material |

**Important:** Sign determines interpretation!

---

## Material Cards (Data Block)

### M Card - Material Definition

**Format:** `Mn  ZAID₁  frac₁  ZAID₂  frac₂  ...`

| Fraction Sign | Meaning | Range | Example |
|---------------|---------|-------|---------|
| **Negative** | Weight fraction | -1.0 to 0 | `-0.98` (98% by weight) |
| **Positive** | Atom fraction | 0 to ~1.0 | `0.562` (56.2% of atoms) |

**Note:** Fractions normalized automatically by MCNP

### MT Card - Thermal Scattering

**Format:** `MTn  S(α,β)_ID`

**Units:** None (identifier only)

---

## Source Cards (Data Block)

### SDEF Card - Source Definition

| Parameter | Unit | Valid Range | Example | Notes |
|-----------|------|-------------|---------|-------|
| **ERG** | MeV | 10⁻¹¹ to 100 | `ERG=0.0141` | 14.1 keV neutron |
| **POS** | cm | any | `POS=0 0 0` | Source position |
| **VEC** | unit vector | -1 to +1 | `VEC=0 0 1` | Direction (normalized) |
| **DIR** | cosine or flag | -1 to +1 or d1 | `DIR=1` | Beam (1) or iso |
| **WGT** | particles/source | > 0 | `WGT=7.4E10` | Source weight |
| **AXS** | cm (unit vector) | -1 to +1 | `AXS=0 0 1` | Reference axis |
| **EXT** | cm | any | `EXT=d1` | Spatial extent |

### SI/SP Cards - Source Distributions

| Card | Parameter | Unit | Example |
|------|-----------|------|---------|
| **SI** (energy) | Energy | MeV | `SI1  L  0.662  1.173` |
| **SP** (probability) | Probability | 0–1 or pdf | `SP1  0.5  0.5` |
| **SI** (position) | Length | cm | `SI2  H  0  100  200` |
| **SI** (direction) | Cosine | -1 to +1 | `SI3  -1  1` |

**Distribution Types:**
- `L` = discrete list
- `H` = histogram
- `A` = continuous (pdf)
- `S` = special functions

---

## Energy & Physics Cards

### TMP Card - Temperature

**Format:** `TMP  value(s)`

| Unit | Range | Example | When to Use |
|------|-------|---------|-------------|
| **Kelvin** | 0.1–10,000 | `TMP  600` | Common, intuitive |
| **MeV** | 10⁻¹¹–10⁻⁶ | `TMP  5.17E-8` | Equivalent to K |

**Conversion:** T(MeV) = k_B × T(K) = 8.617×10⁻¹¹ × T(K)

### PHYS Card - Physics Options

| Parameter | Unit | Typical Range | Example |
|-----------|------|---------------|---------|
| EMAX | MeV | 1–100 | `PHYS:N  100` |
| EMCNF | MeV | 10⁻⁴–10⁻¹ | `PHYS:N  100  0.001` |

### CUT Card - Cutoff Energies

**Format:** `CUT:p  Emin  Emax  ...`

| Parameter | Unit | Example | Notes |
|-----------|------|---------|-------|
| Energy cutoffs | MeV | `CUT:N  1E-10  100` | Min and max energy |
| Time cutoff | shake | `CUT:N  J  J  1E6` | J = no cutoff |

---

## Tally Cards

### Fn Cards - Tally Specification

| Tally | Type | Unit (default) | Normalized by |
|-------|------|----------------|---------------|
| **F1** | Surface current | particles | Source particle |
| **F2** | Surface flux | particles/cm² | Source particle |
| **F4** | Track-length flux | particles/cm² | Source particle |
| **F5** | Point detector | particles/cm² | Source particle |
| **F6** | Energy deposition | MeV/g | Source particle |
| **F7** | Fission energy | MeV | Source particle |
| **F8** | Energy distribution | pulses | Source particle |

**Note:** All tallies "per source particle" unless multiplied

### En Card - Energy Bins

**Format:** `En  E₁  E₂  E₃  ...`

**Unit:** MeV

**Example:** `E4  0  0.01  0.1  1.0  20`

### Tn Card - Time Bins

**Format:** `Tn  t₁  t₂  t₃  ...`

**Unit:** shake (10⁻⁸ s)

**Example:** `T4  0  1  10  100  1000` (0 to 10 μs)

### FM Card - Tally Multiplier

**Format:** `FMn  C  mat_num  rxn_MT`

| Parameter | Unit | Example | Notes |
|-----------|------|---------|-------|
| **C** | multiplier | `-1.0` | Negative = multiply by atom density |
| **mat_num** | material | `1` | From M card |
| **rxn_MT** | reaction | `-6` | MT number (e.g., -6 = fission) |

---

## Geometry Cards (Block 2)

### Surface Cards

All geometric parameters in **centimeters (cm)**

| Surface | Parameters | Unit | Example |
|---------|------------|------|---------|
| **P/PX/PY/PZ** | D or coordinate | cm | `10  PZ  0` |
| **SO/S** | R or x y z R | cm | `20  SO  250` |
| **CX/CY/CZ** | R | cm | `30  CZ  150` |
| **C/X** | x y z R | cm | `40  C/X  0 0 100` |
| **SX/SY/SZ** | x/y/z R | cm | `50  SZ  0 200` |
| **K/X** | x y z R² +/-1 | cm, cm² | `60  K/Z  0 0 0.5 1` |
| **SQ** | A B C D E F G x y z | cm⁻², cm⁻¹, cm | Complex |
| **GQ** | A B C D E F G H J K | cm⁻², cm⁻¹, 1 | Most general |
| **TX** | x y z R R R | cm | Elliptical torus |
| **BOX** | Vx Vy Vz A1 A2 A3 B1 B2 B3 C1 C2 C3 | cm | `BOX  0 0 0  10 0 0  0 10 0  0 0 10` |
| **RPP** | xmin xmax ymin ymax zmin zmax | cm | `RPP  -10 10 -10 10 0 100` |
| **SPH** | x y z R | cm | `SPH  0 0 0 50` |
| **RCC** | x y z Hx Hy Hz R | cm | `RCC  0 0 0  0 0 100  25` |

### TR Card - Transformation

**Format:** `TRn  displacement rotation`

| Parameter | Unit | Example | Notes |
|-----------|------|---------|-------|
| **Displacement** | cm | `TR1  10 20 30` | Translation (dx, dy, dz) |
| **Rotation** | degrees | `TR1  ... 45 0 0` | Optional angles |
| **Matrix** | direction cosines | `TR1  ... 1 0 0  0 1 0  0 0 1` | Alternative to angles |

---

## Variance Reduction Cards

### IMP Card - Cell Importance

**Format:** `IMPn  i₁  i₂  i₃  ...`

**Unit:** Dimensionless (relative importance)

**Values:** 0 (kill) to large positive (>1000 not recommended)

### WWN/WWE Card - Weight Windows

| Parameter | Unit | Notes |
|-----------|------|-------|
| **Lower bounds** | Dimensionless | Particle weight threshold |
| **Energy bins** | MeV | Energy-dependent windows |
| **Time bins** | shake | Time-dependent windows |

---

## Mesh Tally Cards

### FMESH / TMESH Cards

| Parameter | Unit | Example | Notes |
|-----------|------|---------|-------|
| **GEOM** | Type | `GEOM=XYZ` or `=CYL` | Coordinate system |
| **ORIGIN** | cm | `ORIGIN=0 0 0` | Mesh origin |
| **IMESH** | cm | `IMESH=100 200 300` | X-boundaries |
| **JMESH** | cm | `JMESH=100 200` | Y-boundaries |
| **KMESH** | cm | `KMESH=0 50 100 150` | Z-boundaries |
| **IINTS** | bins | `IINTS=10` | # intervals between boundaries |
| **EMESH** | MeV | `EMESH=0.1 1 20` | Energy bins |

---

## Control Cards

### NPS Card - Number of Histories

**Format:** `NPS  n`

**Unit:** Particles (integer)

**Example:** `NPS  1000000`

### KCODE Card - Criticality Source

**Format:** `KCODE  nsrck  rkk  ikz  kct`

| Parameter | Unit | Example | Notes |
|-----------|------|---------|-------|
| **nsrck** | particles/cycle | `5000` | Source per cycle |
| **rkk** | keff guess | `1.0` | Initial estimate |
| **ikz** | cycles to skip | `50` | Skip for source convergence |
| **kct** | total cycles | `250` | Active + skipped |

### PRDMP Card - Checkpoint/Restart

**Format:** `PRDMP  npp  ndd  ndm  ...`

| Parameter | Unit | Example | Notes |
|-----------|------|---------|-------|
| **npp** | particles | `10000000` | Dump after n particles |
| **ndd** | dumps | `10` | Max dumps to keep |
| **ndm** | dumps | `2` | Minimum dumps |
| **mct** | minutes | `-1` | Time-based dump |

### PRINT/DBCN Cards

**Unit:** None (control flags only)

---

## Summary of MCNP Units

| Physical Quantity | MCNP Standard | Alternative | Conversion |
|-------------------|---------------|-------------|------------|
| **Energy** | MeV | eV, keV, J | 1 keV = 0.001 MeV |
| **Length** | cm | m, mm | 1 m = 100 cm |
| **Density (mass)** | g/cm³ (neg) | kg/m³ | 1000 kg/m³ = 1 g/cm³ |
| **Density (atomic)** | atom/b-cm (pos) | atom/cm³ | N = ρN_A/(A×10²⁴) |
| **Temperature** | K or MeV | °C | T(K) = °C + 273.15 |
| **Time** | shake | s, μs | 1 μs = 100 shakes |
| **Cross section** | barn | cm² | 1 b = 10⁻²⁴ cm² |
| **Activity** | Bq or Ci | mCi | 1 Ci = 3.7×10¹⁰ Bq |
| **Mass** | amu | g | 1 amu = 1.661×10⁻²⁴ g |

---

## Common Errors & Fixes

### Error 1: Wrong Density Units
```mcnp
c WRONG
10  1  -7850  -100   $ kg/m³ used directly

c CORRECT
10  1  -7.85  -100   $ Converted to g/cm³
```

### Error 2: Energy in keV
```mcnp
c WRONG
SDEF  ERG=14.1       $ keV not converted

c CORRECT
SDEF  ERG=0.0141     $ Converted to MeV
```

### Error 3: Temperature in Celsius
```mcnp
c WRONG
TMP  500             $ °C without conversion

c CORRECT
TMP  773.15          $ Converted to K (500+273.15)
```

### Error 4: Time in Seconds
```mcnp
c WRONG
T4  0  1  2  3       $ Seconds (way too short)

c CORRECT
T4  0  1E8  2E8  3E8  $ Converted to shakes
```

---

**Quick Reference:** When in doubt, MCNP uses **CGS-based units** (cm, g, s) for geometry and materials, but **MeV** for energy and **shakes** for time!

**Last Updated:** 2025-11-06
**Source:** MCNP 6.3 User Manual, Chapters 2–5
