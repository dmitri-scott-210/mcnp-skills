# MCNP Material Templates

Verified MCNP input file templates demonstrating correct material definitions for common reactor and shielding applications.

---

## Template Files Overview

| Template | Purpose | Materials | Use Cases |
|----------|---------|-----------|-----------|
| **water_materials_template.i** | Water and heavy water | H₂O, D₂O, hot H₂O | Moderators, coolants, reflectors |
| **fuel_materials_template.i** | Nuclear fuels | UO₂ (3%, 5%), MOX | Reactor core, criticality |
| **structural_materials_template.i** | Structural/cladding | SS-316, Zircaloy, Concrete | Structures, cladding, shielding |
| **moderator_materials_template.i** | Moderator materials | Graphite, Polyethylene, Beryllium | Moderation, reflection |

---

## 1. water_materials_template.i

**Purpose:** Demonstrates proper water material definitions with S(α,β) thermal scattering

**Materials Included:**
- **M1: Light Water (H₂O)** at 293.6 K
  - Density: 1.0 g/cm³ → -0.1003 atoms/b-cm
  - ZAID: 1001.80c (H-1), 8016.80c (O-16)
  - MT1: H-H2O.40t (thermal scattering at 293.6 K)

- **M2: Heavy Water (D₂O)** at 293.6 K
  - Density: 1.1 g/cm³ → -0.110 atoms/b-cm
  - ZAID: 1002.80c (D), 8016.80c (O-16)
  - MT2: D-D2O.40t (deuterium thermal scattering)

- **M3: Hot Light Water** at 600 K
  - Density: 0.8 g/cm³ (thermal expansion)
  - ZAID: 1001.80c, 8016.80c
  - MT3: H-H2O.43t (MUST match temperature!)

**Key Features:**
- Temperature-dependent S(α,β) tables
- TMP card correlation with MT card
- Atomic fractions (positive values)
- Proper density calculations

**When to Use:**
- PWR/BWR moderator and coolant
- Heavy water reactor (CANDU)
- Reflector regions
- Temperature effects on reactivity

---

## 2. fuel_materials_template.i

**Purpose:** Demonstrates nuclear fuel compositions with different enrichments

**Materials Included:**
- **M1: UO₂ Fuel, 3% Enriched** at 900 K
  - Density: 10.5 g/cm³ → -10.50 atoms/b-cm
  - Composition: 3% U-235, 97% U-238, 2 oxygen atoms
  - Atomic fractions: 0.03, 0.97, 2.0

- **M2: UO₂ Fuel, 5% Enriched** at 900 K
  - Density: 10.5 g/cm³
  - Composition: 5% U-235, 95% U-238, 2 oxygen atoms
  - Higher enrichment for increased reactivity

- **M3: MOX Fuel (Mixed Oxide)** at 900 K
  - Density: 10.5 g/cm³
  - Composition: Depleted U + Pu isotopes (Pu-239, Pu-240, Pu-241)
  - Typical LWR MOX: 85% U-238, 5% Pu-239, 3% Pu-240, 2% Pu-241

**Key Features:**
- Enrichment specification
- Atomic fraction format
- High-temperature fuel (TMP card)
- Continuation cards (&) for long lines

**When to Use:**
- LWR core design
- Criticality calculations
- Burnup studies (initial composition)
- MOX fuel analysis

---

## 3. structural_materials_template.i

**Purpose:** Demonstrates structural and cladding materials with weight fractions

**Materials Included:**
- **M1: Stainless Steel 316 (SS-316)** at 293.6 K
  - Density: 8.0 g/cm³
  - Composition: Fe 65%, Cr 17%, Ni 12%, Mo 2.5%, Mn 2%, Si 1%, C 0.08%
  - Weight fractions (negative values)

- **M2: Zircaloy-4 (Zr-4)** at 900 K
  - Density: 6.56 g/cm³
  - Composition: Zr 98.23%, Sn 1.45%, Fe 0.21%, Cr 0.10%, O 0.125%
  - Fuel cladding material

- **M3: Ordinary Concrete** at 293.6 K
  - Density: 2.3 g/cm³
  - Composition: 10 elements (H, C, O, Na, Mg, Al, Si, K, Ca, Fe)
  - Weight fractions for shielding

**Key Features:**
- Weight fractions (negative values)
- Multi-element alloys
- Natural element ZAIDs (e.g., 26000.80c for natural Fe)
- Continuation cards for complex compositions

**When to Use:**
- Reactor vessel materials
- Fuel cladding (Zircaloy)
- Shielding calculations (concrete)
- Structural integrity analysis

---

## 4. moderator_materials_template.i

**Purpose:** Demonstrates moderator materials with S(α,β) thermal scattering

**Materials Included:**
- **M1: Graphite (Nuclear Grade)** at 900 K
  - Density: 1.70 g/cm³
  - Composition: Natural carbon (C-12 + trace C-13)
  - MT1: GRPH.43t (graphite thermal scattering at 600 K)
  - Use: HTGR moderator

- **M2: Polyethylene (CH₂)ₙ** at 293.6 K
  - Density: 0.94 g/cm³
  - Composition: H:C atomic ratio 2:1
  - MT2: POLY.40t (polyethylene thermal scattering)
  - Use: Neutron shielding, moderation

- **M3: Beryllium Metal** at 293.6 K
  - Density: 1.85 g/cm³
  - Composition: Pure Be-9 (100% natural)
  - MT3: BE.40t (beryllium thermal scattering)
  - Use: Reflector, moderator

**Key Features:**
- S(α,β) tables for all materials
- Low absorption cross sections
- High scattering cross sections
- Temperature-appropriate thermal scattering

**When to Use:**
- HTGR designs (graphite)
- Neutron shielding (polyethylene)
- Reflector regions (beryllium)
- Fast-to-thermal spectrum transition

---

## General Usage Guidelines

### How to Use These Templates

1. **Copy template file** to your working directory
2. **Modify cell geometry** to match your problem
3. **Adjust densities** if using different temperatures or forms
4. **Verify S(α,β) tables** match your temperature (TMP card)
5. **Update SDEF and NPS** for your source and particle count
6. **Run MCNP** with verification (short NPS first)

### Important Notes

**MCNP Format Requirements:**
- All templates follow MCNP's strict format: EXACTLY 2 blank lines total
  - One blank line after cell cards block
  - One blank line after surface cards block
- NO blank lines within any block (including between materials)
- Three-block structure: Cell → Surface → Data

**Temperature Considerations:**
- TMP card value (MeV) MUST correspond to S(α,β) table temperature
- Conversion: T(MeV) = T(K) × 8.617×10⁻¹¹
- Example: 293.6 K = 2.53×10⁻⁸ MeV, 600 K = 5.17×10⁻⁸ MeV
- S(α,β) table suffix indicates temperature: .40t (293.6 K), .43t (600 K)

**Density Formats:**
- **Atomic density (positive):** Used for atomic fractions (e.g., UO₂ fuel)
- **Mass density (negative):** Direct g/cm³ value (e.g., -10.5 for UO₂)
- Conversion: ρ_atomic = ρ_mass × 0.6022 / M (where M is molecular weight)

**Fraction Types (DO NOT MIX):**
- **Atomic fractions (positive):** Number ratios (e.g., H₂O: 2 H, 1 O)
- **Weight fractions (negative):** Mass ratios, must sum to -1.0 (e.g., SS-316)

---

## Example Workflows

### Workflow 1: PWR Core Material Setup
1. Start with **water_materials_template.i** for moderator (M1: H₂O)
2. Add **fuel_materials_template.i** materials for UO₂ fuel (M1 or M2)
3. Add **structural_materials_template.i** M2 (Zircaloy cladding)
4. Verify temperatures: fuel at 900 K, moderator at 580 K (operating conditions)

### Workflow 2: HTGR Design
1. Start with **moderator_materials_template.i** M1 (Graphite at 900 K)
2. Add **fuel_materials_template.i** for TRISO fuel particles
3. Add **structural_materials_template.i** M3 (Concrete for biological shield)
4. Adjust graphite temperature to match core outlet (up to 1200 K)

### Workflow 3: Shielding Study
1. Use **structural_materials_template.i** M3 (Concrete) for primary shield
2. Add **moderator_materials_template.i** M2 (Polyethylene) for neutron shield
3. Add **water_materials_template.i** M1 (H₂O) for additional moderation
4. Use **structural_materials_template.i** M1 (Steel) for structural support

---

## Common Modifications

### Changing Enrichment
```
Original:  M1   92235.80c  0.03  92238.80c  0.97  8016.80c  2.0  $ 3% enriched
Modified:  M1   92235.80c  0.045 92238.80c  0.955 8016.80c  2.0  $ 4.5% enriched
```

### Adjusting Density for Temperature
- Water at 293.6 K: 1.0 g/cm³
- Water at 580 K: 0.715 g/cm³ (PWR operating)
- Update both cell card density and M card if using mass density

### Adding Burnable Absorbers
```
c Add boron to water for chemical shim
M1   1001.80c  2  8016.80c  1  5010.80c  0.001  5011.80c  0.004  $ Borated water
```

---

## Verification Checklist

Before using any template:
- [ ] MCNP format verified (EXACTLY 2 blank lines)
- [ ] All ZAIDs available in your xsdir
- [ ] Densities appropriate for your problem
- [ ] Temperatures consistent (TMP ↔ MT table)
- [ ] Enrichments/compositions match design
- [ ] Cell geometry matches material regions
- [ ] Source definition appropriate for problem
- [ ] NPS sufficient for statistics (start small for testing)

---

## Additional Resources

**Material Specifications:**
- See `../references/material_card_specifications.md` for M card syntax
- See `../references/thermal_scattering_reference.md` for complete S(α,β) tables
- See `../references/advanced_material_cards.md` for OTFDB, NONU, AWTAB

**Calculation Tools:**
- Use `../scripts/material_density_calculator.py` for density conversions
- Use `../scripts/zaid_library_validator.py` to verify ZAIDs before MCNP run

**Validation:**
- Always run short test (NPS 1000) to check for fatal errors
- Check kcode output for criticality problems
- Verify tally statistics for shielding calculations

---

**Version:** 1.0
**Created:** 2025-11-03
**For:** mcnp-material-builder skill v2.0

**Note:** All templates verified against MCNP6 format requirements and tested for syntax correctness.
