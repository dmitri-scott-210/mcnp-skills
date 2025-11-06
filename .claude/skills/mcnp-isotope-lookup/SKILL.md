---
name: mcnp-isotope-lookup
description: "Look up isotope properties including ZAID format, atomic masses, natural abundances, decay data, and cross-section library availability for MCNP material and source definitions"
version: "2.0.0"
dependencies: "mcnp-material-builder, mcnp-source-builder, mcnp-cross-section-manager, mcnp-physical-constants"
---

# MCNP Isotope Lookup

## Overview

This utility skill provides comprehensive isotope property lookup for MCNP simulations, including ZAID identifiers, atomic masses, natural abundances, decay data, and cross-section library availability. The skill includes extensive reference documentation, Python lookup tools, and quick-reference data files for efficient isotope selection and material definition.

ZAID (Z and A IDentifier) format is fundamental to MCNP material cards, source definitions, and library selection. This skill bridges nuclear data with practical MCNP input requirements, providing both interactive Python tools for detailed lookup and quick-reference tables for common isotopes.

## When to Use This Skill

- Finding ZAID identifiers for isotopes (e.g., U-235 → 92235.80c)
- Looking up atomic masses for density calculations
- Determining natural isotopic abundances for element definitions
- Identifying decay modes and half-lives for source terms
- Verifying cross-section library availability in xsdir
- Converting element names to ZAID format
- Selecting isotopes for shielding, fuel, or structural materials
- Determining fission product compositions
- Identifying activation products in irradiated materials
- Checking temperature-dependent library availability

## Quick Reference Tables

### ZAID Format Structure

```
ZZZAAA.nnX

Components:
  ZZZ = Atomic number (Z) - 1 to 3 digits
  AAA = Mass number (A) - 1 to 3 digits
  nn  = Library identifier (80, 81, 82, etc.)
  X   = Library type (c, d, p, e, t, etc.)

Examples:
  1001.80c   → H-1 (protium) with ENDF/B-VIII.0
  92235.80c  → U-235 with ENDF/B-VIII.0
  6000.80c   → Natural carbon mix
  82000.80c  → Natural lead
```

### Common Library Suffixes

| Suffix | Description | Temperature | Use Case |
|--------|-------------|-------------|----------|
| .80c | ENDF/B-VIII.0 | 293.6 K | Room temp, most recent |
| .81c | ENDF/B-VIII.0 | 600 K | Moderate temp reactors |
| .82c | ENDF/B-VIII.0 | 900 K | High temp reactors |
| .70c | ENDF/B-VII.0 | 293.6 K | Legacy, benchmarks |
| .80p | Photoatomic | 293.6 K | Photon transport |
| .80t | Thermal S(α,β) | Varies | Bound atoms (H in H₂O) |

### Commonly Used Isotopes

| Isotope | ZAID | Mass (amu) | Abundance/Half-life | Application |
|---------|------|------------|---------------------|-------------|
| H-1 | 1001.80c | 1.00783 | 99.99% | Water moderator |
| B-10 | 5010.80c | 10.01294 | 19.9% | Neutron absorber |
| C-12 | 6012.80c | 12.00000 | 98.93% | Graphite |
| O-16 | 8016.80c | 15.99491 | 99.76% | Oxide fuel |
| Fe-56 | 26056.80c | 55.93494 | 91.75% | Steel structural |
| Zr-90 | 40090.80c | 89.90470 | 51.45% | Cladding |
| Pb-208 | 82208.80c | 207.97666 | 52.4% | Shielding |
| U-235 | 92235.80c | 235.04393 | 0.72% (nat), t₁/₂=7×10⁸ yr | Fissile fuel |
| U-238 | 92238.80c | 238.05079 | 99.27% (nat), t₁/₂=4.5×10⁹ yr | Fertile fuel |
| Pu-239 | 94239.80c | 239.05216 | t₁/₂=24,110 yr | Fissile fuel |

**For complete isotope data:** See `isotope_database.md`

**For ZAID format details:** See `zaid_format_guide.md`

**For library availability:** See `library_availability.md`

**For decay data:** See `decay_data.md`

## Decision Tree

```
User needs isotope information?
    │
    ├─ ZAID identifier?
    │  ├─> Know element symbol and mass number?
    │  │   └─> Use: python zaid_lookup.py --isotope "U-235"
    │  │       Result: 92235.80c
    │  ├─> Natural element mix?
    │  │   └─> Use ZZZ000 format (e.g., 6000.80c for natural C)
    │  └─> Parse existing ZAID?
    │      └─> Use: python zaid_lookup.py --zaid "92235.80c"
    │
    ├─ Atomic mass?
    │  ├─> Specific isotope?
    │  │   └─> Use: python isotope_properties.py --mass "U-235"
    │  │       Result: 235.04393 amu
    │  └─> Natural element average?
    │      └─> Use: python isotope_properties.py --element "Fe"
    │          Result: 55.845 amu (average)
    │
    ├─ Natural abundance?
    │  └─> Use: python isotope_properties.py --element "Cl" --abundance
    │      Result: Cl-35 (75.76%), Cl-37 (24.24%)
    │      See: natural_abundances.csv
    │
    ├─ Library availability?
    │  └─> Use: python library_checker.py --zaid "92235.80c"
    │      Or check entire input: --file input.i
    │      Requires: $DATAPATH set to MCNP data directory
    │
    └─ Decay data?
       └─> See: decay_data.md for half-lives, decay modes
           Use: isotope_properties.py --halflife "Co-60"
```

## Use Cases

### Use Case 1: Look Up ZAID for Shielding Material (Lead)

**Scenario:** Need to define lead shielding, find appropriate ZAID

**Solution:**

```bash
# Option 1: Use Python tool
python scripts/zaid_lookup.py --element "Pb"

# Result: Natural ZAID: 82000.80c

# Option 2: Look up in quick reference
# See common_isotopes.csv or zaid_format_guide.md
```

**MCNP Material Card (Natural lead - recommended):**
```
c Lead shielding (natural isotopic composition)
c ρ = 11.34 g/cm³
M1  82000.80c  1.0         $ Natural lead
10  1  -11.34  -100        $ Lead shield
```

**Alternative (explicit isotopes):**
```
c Lead shielding (explicit isotopes)
M2  82204.80c  0.014       $ Pb-204 (1.4%)
    82206.80c  0.241       $ Pb-206 (24.1%)
    82207.80c  0.221       $ Pb-207 (22.1%)
    82208.80c  0.524       $ Pb-208 (52.4%)
```

**When to use natural vs. individual:**
- **Natural (82000):** Most shielding, simplicity, minor isotope effects
- **Individual isotopes:** Isotope-specific studies, enriched materials, high precision

### Use Case 2: Find Atomic Mass for Density Calculation

**Scenario:** Calculate atom density for borated water (1000 ppm B-10 by weight)

**Solution:**

```bash
# Get B-10 atomic mass
python scripts/isotope_properties.py --mass "B-10"
# Result: 10.01294 amu

# Get H2O average masses
# H: 1.008 amu, O: 15.999 amu
```

**Calculation:**
```
Composition:
  B-10: 1000 ppm = 0.001 weight fraction
  H₂O:  0.999 weight fraction

Atom densities (ρ_total = 1.0 g/cm³):
  N_B10 = (0.001 × 6.022×10²³) / (10.013 × 10²⁴)
        = 6.015 × 10⁻⁵ atoms/b-cm

  N_H2O = (0.999 × 6.022×10²³) / (18.015 × 10²⁴)
        = 0.03342 atoms/b-cm

  N_H = 2 × N_H2O = 0.06684 atoms/b-cm
  N_O = N_H2O = 0.03342 atoms/b-cm
```

**MCNP Material Card:**
```
c Borated water: 1000 ppm B-10 by weight
M1  5010.80c   6.015E-5    $ B-10
    1001.80c   0.06684     $ H-1
    8016.80c   0.03342     $ O-16
```

### Use Case 3: Determine Natural Isotopic Composition (Uranium)

**Scenario:** Define natural uranium material, need isotopic abundances

**Solution:**

```bash
# Get natural uranium composition
python scripts/isotope_properties.py --element "U" --abundance

# Result:
#   U-234: 0.0054% (trace)
#   U-235: 0.7204%
#   U-238: 99.2742%
```

**MCNP Material Cards:**

**Option 1 - Natural mix (simplest):**
```
c Natural uranium metal
c ρ = 19.05 g/cm³
M1  92000.80c  1.0          $ Natural uranium
10  1  -19.05  -100         $ Uranium metal
```

**Option 2 - Explicit isotopes:**
```
c Natural uranium (explicit)
M2  92234.80c  0.000054     $ U-234 (0.0054%)
    92235.80c  0.007204     $ U-235 (0.7204%)
    92238.80c  0.992742     $ U-238 (99.2742%)
c Verify: sum = 1.000000 ✓
```

**Option 3 - Ignore U-234 (common approximation):**
```
c Natural uranium (U-234 ignored)
M3  92235.80c  0.0072       $ U-235 (0.72%)
    92238.80c  0.9928       $ U-238 (99.28%)
```

**When to include U-234:** High-precision criticality, long-term burnup, isotopic inventory; usually negligible for shielding

### Use Case 4: Verify Cross-Section Library Availability

**Scenario:** Want to use Am-241, verify library available before running

**Solution:**

```bash
# Set DATAPATH (if not already set)
export DATAPATH=/path/to/mcnp/data

# Check availability
python scripts/library_checker.py --zaid "95241.80c"

# Result (if available):
# ZAID: 95241.80c
# Status: AVAILABLE ✓
# Atomic weight: 241.05683 amu
# File: endf80/Am/95241.800nc

# Check entire input file
python scripts/library_checker.py --file my_input.i

# Result:
# Total ZAIDs found: 15
# Available: 15
# Missing: 0
# All ZAIDs are available ✓
```

**If isotope NOT available:**
```
Options:
1. Use natural element mix: 95000.80c (if available)
2. Use older library: 95241.70c (ENDF/B-VII.0)
3. Use nearby isotope: 95243.80c (approximation, document clearly)
4. Process evaluation with NJOY (advanced users)
```

**MCNP Material Card:**
```
c Am-241 source (alpha emitter)
M1  95241.80c  1.0          $ Am-241 (verify available)
    8016.80c   2.0          $ O-16 (AmO₂ oxide form)
```

### Use Case 5: Look Up Thermal Scattering for Water

**Scenario:** Model light water moderated reactor, need thermal scattering library

**Solution:**

Thermal scattering required for bound atoms at thermal energies (E < ~4 eV). Critical for accurate keff in thermal systems.

```bash
# Check available thermal scattering libraries
python scripts/library_checker.py --search "lwtr"

# Result:
#   lwtr.80t  (293.6 K)
#   lwtr.81t  (323.6 K)
#   lwtr.82t  (373.6 K)
#   ...
#   lwtr.87t  (623.6 K)
```

**MCNP Material Card with Thermal Scattering:**
```
c Light water moderator at 580 K
M1  1001.80c  2.0          $ Hydrogen in H₂O
    8016.80c  1.0          $ Oxygen
MT1 lwtr.86t               $ S(α,β) at 573.6 K (closest to 580 K)
TMP  580                   $ Exact temperature
c
10  1  -1.0  -100 IMP:N=1  $ Water cell
```

**Important notes:**
- MT card number matches M card number (M1 → MT1)
- Thermal scattering REQUIRED for accurate thermal reactor keff (error >500-2000 pcm without)
- Select library temperature closest to system temperature
- Common thermal materials: lwtr (H₂O), hwtr (D₂O), grph (graphite), poly (CH₂), be, beo

**See `library_availability.md` for complete thermal scattering library list**

## Integration with Other Skills

### Supports Material Builder
**mcnp-material-builder** uses this skill for ZAID selection, atomic masses for density calculations, and natural abundance data for isotopic composition.

**Workflow:**
```
1. User specifies: "stainless steel 316"
2. material-builder determines composition (Fe, Cr, Ni, Mo)
3. isotope-lookup provides ZAIDs and atomic masses
4. material-builder creates M card with correct densities
```

### Supports Source Builder
**mcnp-source-builder** uses decay data for radioactive sources (Co-60, Cs-137, etc.), including half-lives, gamma energies, and decay modes.

**Workflow:**
```
1. User specifies: "1 Ci Cs-137 source"
2. source-builder needs decay information
3. isotope-lookup provides: t₁/₂=30.17 yr, γ=0.662 MeV
4. source-builder creates SDEF card
```

### Uses Cross-Section Manager
**mcnp-cross-section-manager** uses library availability checking to verify isotopes exist in xsdir before simulation.

### Uses Physical Constants
**mcnp-physical-constants** provides Avogadro's number, AMU conversion, and Boltzmann constant used in density and temperature calculations.

## Python Tools

This skill includes three Python tools in the `scripts/` directory:

### zaid_lookup.py
Interactive and command-line ZAID conversion tool.

**Quick start:**
```bash
# Interactive mode
python scripts/zaid_lookup.py

# Convert isotope to ZAID
python scripts/zaid_lookup.py --isotope "U-235" --library "80c"

# Parse ZAID
python scripts/zaid_lookup.py --zaid "92235.80c"

# Validate ZAID format
python scripts/zaid_lookup.py --validate "92235.80c"
```

### isotope_properties.py
Atomic mass, natural abundance, and decay data lookup.

**Quick start:**
```bash
# Interactive mode
python scripts/isotope_properties.py

# Get atomic mass
python scripts/isotope_properties.py --mass "U-235"

# Get natural abundances
python scripts/isotope_properties.py --element "Cl" --abundance

# Get half-life
python scripts/isotope_properties.py --isotope "Co-60" --halflife
```

### library_checker.py
Check cross-section library availability in xsdir file.

**Quick start:**
```bash
# Set DATAPATH first
export DATAPATH=/path/to/mcnp/data

# Check single ZAID
python scripts/library_checker.py --zaid "92235.80c"

# Check entire input file
python scripts/library_checker.py --file input.i

# Search for isotopes
python scripts/library_checker.py --search "^92"
```

**See `scripts/README.md` for complete tool documentation.**

## References

### Bundled Resources

**Reference Documentation (at ROOT level):**
- `zaid_format_guide.md` - ZAID format specification, library suffixes, thermal scattering
- `isotope_database.md` - Atomic masses, natural abundances, element properties
- `library_availability.md` - Cross-section libraries, xsdir checking, temperature libraries
- `decay_data.md` - Decay modes, half-lives, fission products, activation products

**Python Tools (scripts/):**
- `zaid_lookup.py` - ZAID conversion and validation
- `isotope_properties.py` - Isotope data retrieval
- `library_checker.py` - xsdir availability checking
- `README.md` - Complete tool documentation and examples

**Data Files (example_inputs/):**
- `common_isotopes.csv` - 48 commonly used isotopes with properties
- `natural_abundances.csv` - Natural isotopic compositions for multi-isotope elements
- `library_temperatures.csv` - Temperature-dependent library reference

### External References

**Nuclear Data Sources:**
- NIST Atomic Weights and Isotopic Compositions: https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions
- NNDC (National Nuclear Data Center): https://www.nndc.bnl.gov/
- IAEA Nuclear Data Services: https://www-nds.iaea.org/
- Chart of the Nuclides: https://www.nndc.bnl.gov/nudat3/

**ENDF/B Libraries:**
- ENDF/B-VIII.0: https://www.nndc.bnl.gov/endf-b8.0/
- OECD/NEA Data Bank: https://www.oecd-nea.org/

**Related MCNP Skills:**
- mcnp-material-builder - Uses ZAIDs and atomic masses
- mcnp-source-builder - Uses decay data
- mcnp-cross-section-manager - Manages libraries
- mcnp-physical-constants - Fundamental constants
- mcnp-unit-converter - Unit conversions

## Best Practices

1. **Always Verify ZAID Format** - Use validation: `ZZZAAA.nnX` with correct Z, A, library, and type

2. **Check Library Availability** - Before running, verify all ZAIDs exist in xsdir:
   ```bash
   python scripts/library_checker.py --file input.i
   ```

3. **Document Isotope Choices** - Use comments to explain natural vs. individual isotopes
   ```
   c Lead shielding (using natural mix for simplicity)
   M1  82000.80c  1.0
   ```

4. **Verify Abundance Normalization** - Always check Σ fᵢ = 1.0 for multi-isotope materials

5. **Use Correct Atomic Mass** - Isotopic mass for specific isotopes, average mass for natural elements, weighted average for enriched materials

6. **Include Thermal Scattering** - REQUIRED for H in H₂O, D in D₂O, C in graphite, Be in Be/BeO at thermal energies
   ```
   M1  1001.80c  2.0
       8016.80c  1.0
   MT1 lwtr.80t              $ REQUIRED for accurate keff
   ```

7. **Match Temperature Libraries** - Use library closest to system temperature:
   - T < 400 K: .80c + TMP
   - 400-800 K: .81c
   - 800-1100 K: .82c
   - 1100-1800 K: .83c

8. **Use Consistent Library Version** - All isotopes in calculation should use same ENDF/B version (.80c, .70c, etc.)

9. **Distinguish Stable vs. Radioactive** - Check half-life for activation and decay studies; use stable isotopes for long-term shielding

10. **Test Before Production** - Run quick test to verify ZAIDs found, no fatal errors, expected keff range

---

**For detailed isotope data, decay properties, and library information, see bundled reference documentation. For calculations, use Python tools in scripts/.**
