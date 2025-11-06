# MCNP ZAID Format Guide

## Overview

This guide provides comprehensive documentation of the MCNP ZAID (Z and A IDentifier) format used to specify nuclides in MCNP input files. The ZAID format is fundamental to material definitions, source specifications, and cross-section library references.

## ZAID Structure

### Basic Format

```
ZZZAAA.nnX

Components:
  ZZZ = Atomic number (Z) - 1 to 3 digits
  AAA = Mass number (A) - 1 to 3 digits
  nn  = Library identifier (e.g., 80, 81, 82)
  X   = Library type character
```

### Component Details

**Atomic Number (ZZZ)**:
- Range: 1 to 118 (known elements)
- Can be 1, 2, or 3 digits
- Examples: 1 (H), 92 (U), 94 (Pu)
- Leading zeros optional but recommended for alignment

**Mass Number (AAA)**:
- Range: 1 to ~300
- Can be 1, 2, or 3 digits
- Represents total nucleons (protons + neutrons)
- Examples: 1 (H-1), 235 (U-235), 239 (Pu-239)
- Use 000 for natural element mix

**Library Identifier (nn)**:
- Two-digit code identifying cross-section library version
- Common values: 80, 70, 66, 60 (ENDF/B versions)
- Temperature variants: 81, 82, 83, 84, 85, 86, 87
- Format: Always two digits (e.g., 80, not 8)

**Library Type (X)**:
- Single character specifying data type
- Common types detailed in next section

## Library Type Characters

### Standard Types

```
c = Continuous energy neutron data
    Most common for neutron transport
    Examples: 92235.80c, 1001.80c

d = Discrete energy data
    Legacy format, rarely used
    Examples: 92235.80d

p = Photoatomic data
    For photon interactions
    Examples: 82000.80p (lead photon data)

e = Electron data
    For electron transport
    Examples: 82000.03e

t = Thermal scattering data
    For bound nuclei at thermal energies
    Examples: lwtr.80t, grph.80t

h = Dosimetry data
    For dose calculations
    Examples: ansi.01h

m = Multigroup data
    For multigroup transport
    Examples: 92235.50m
```

### Special Library Types

```
y = Photonuclear data
    For photon-induced nuclear reactions

u = Photonuclear data (alternate)
    Some implementations use 'u'

v = Neutron displacement damage
    For radiation damage calculations
```

## ZAID Examples

### Common Isotopes

```
Hydrogen:
  1001.80c   → H-1 (protium) continuous energy
  1002.80c   → H-2 (deuterium)
  1003.80c   → H-3 (tritium)

Carbon:
  6000.80c   → Natural carbon mix
  6012.80c   → C-12 (98.93% of natural)
  6013.80c   → C-13

Oxygen:
  8016.80c   → O-16 (most common)
  8017.80c   → O-17
  8018.80c   → O-18

Iron:
  26000.80c  → Natural iron mix
  26054.80c  → Fe-54
  26056.80c  → Fe-56 (91.75% of natural)
  26057.80c  → Fe-57
  26058.80c  → Fe-58

Uranium:
  92000.80c  → Natural uranium mix
  92234.80c  → U-234
  92235.80c  → U-235 (fissile)
  92238.80c  → U-238 (fertile)

Plutonium:
  94239.80c  → Pu-239 (fissile)
  94240.80c  → Pu-240
  94241.80c  → Pu-241
```

### Photon and Electron Data

```
Photon data (p):
  1000.80p   → Hydrogen photoatomic
  6000.80p   → Carbon photoatomic
  82000.80p  → Lead photoatomic (common shielding)

Electron data (e):
  6000.03e   → Carbon electron data
  82000.03e  → Lead electron data
```

## Special Cases

### Natural Element Mix

**Format**: ZZZ000.nnX

**Usage**: When using natural isotopic composition

```
Examples:
  6000.80c   → Natural carbon (98.93% C-12, 1.07% C-13)
  17000.80c  → Natural chlorine (75.76% Cl-35, 24.24% Cl-37)
  82000.80c  → Natural lead (4 stable isotopes)
  92000.80c  → Natural uranium (0.72% U-235, 99.27% U-238)

MCNP Usage:
  M1  6000.80c  1.0      $ Natural carbon

Equivalent to explicit isotopes:
  M1  6012.80c  0.9893   $ C-12
      6013.80c  0.0107   $ C-13
```

**When to Use Natural Mix**:
- Shielding materials (Fe, Pb, concrete ingredients)
- Structural materials with no isotopic importance
- When isotopic effects are negligible
- Simplicity preferred over detail

**When to Use Individual Isotopes**:
- Enriched materials (LEU, HEU)
- Isotope-specific physics important
- Activation analysis (need specific isotope reactions)
- Criticality calculations requiring precision

### Metastable States

**Notation**: ZZZAAA + 300, 400, etc.

**Background**: Some isotopes have long-lived excited nuclear states (isomers)

```
Examples:
  Tc-99m (metastable):
    Ground state: 43099 (t₁/₂ = 211,000 yr)
    Metastable:   43399 (t₁/₂ = 6.01 hr)

  Am-242m (metastable):
    Ground state: 95242 (t₁/₂ = 16.02 hr)
    Metastable:   95642 (t₁/₂ = 141 yr)
```

**MCNP Handling**:
- Most MCNP cross-section libraries do NOT distinguish metastable states
- Use standard ZAID (43099.80c) for both Tc-99 and Tc-99m
- For activation studies, may need to manually track metastable production
- Burnup calculations may have separate treatment

### Element Symbols

**Limited Use in MCNP**:
```
NOT recommended:
  M1  U-235.80c  1.0     $ WRONG - don't use symbols

Correct:
  M1  92235.80c  1.0     $ RIGHT - use numeric ZAID
```

**Exception**: Some plotting utilities accept element symbols

## Cross-Section Library Identifiers

### ENDF/B Library Versions

```
.80c → ENDF/B-VIII.0 (2018)
  - Most recent major release
  - Improved evaluations for many isotopes
  - Recommended for new calculations

.70c → ENDF/B-VII.0 (2006)
  - Widely used and validated
  - Good for benchmark comparisons

.66c → ENDF/B-VI.6 (1998)
  - Legacy, but still available

.60c → ENDF/B-VI.0 (1990)
  - Historical, rarely used
```

### Temperature-Dependent Libraries

**Standard Temperatures**:
```
.80c → 293.6 K  (20.44°C)  Room temperature
.81c → 600 K    (327°C)    Moderate high temp
.82c → 900 K    (627°C)    High temperature
.83c → 1200 K   (927°C)    Very high temp
.84c → 2500 K   (2227°C)   Ultra-high temp

Additional temperatures (some isotopes):
.85c → 523.6 K
.86c → 573.6 K
.87c → 623.6 K
```

**Usage Guidelines**:
```
Temperature Range          Recommended Library
─────────────────          ───────────────────
T < 400 K                  .80c with TMP card
400 K < T < 800 K          .81c or .80c + TMP
800 K < T < 1500 K         .82c
T > 1500 K                 .83c or .84c

Example:
  M1  92235.82c  1.0       $ U-235 at 900 K
  TMP  900                  $ Temperature card (optional if using .82c)
```

**TMP Card Interpolation**:
- MCNP can interpolate between library temperatures
- Use TMP card to specify actual temperature
- MCNP will use closest library or interpolate

```
Example (interpolation):
  M1  92235.80c  1.0       $ 293.6 K library
  TMP  500                  $ MCNP interpolates to 500 K

Better (exact library):
  M1  92235.81c  1.0       $ 600 K library (closer)
  TMP  500                  $ Less interpolation needed
```

## Thermal Scattering Libraries

### Purpose

For bound atoms at thermal energies (E < ~4 eV), neutron scattering depends on molecular/crystalline structure. Thermal scattering libraries (S(α,β) data) provide accurate low-energy physics.

### Format

```
name.nnT

Components:
  name = Material identifier (4 characters, lowercase)
  nn   = Library version (same as neutron libraries)
  T    = 'T' for thermal (uppercase)
```

### Common Thermal Scattering Materials

**Water**:
```
lwtr.80t → Light water (H₂O) at 293.6 K
hwtr.80t → Heavy water (D₂O) at 293.6 K

Temperature variants for light water:
  lwtr.80t → 293.6 K
  lwtr.81t → 323.6 K
  lwtr.82t → 373.6 K
  lwtr.83t → 423.6 K
  lwtr.84t → 473.6 K
  lwtr.85t → 523.6 K
  lwtr.86t → 573.6 K
  lwtr.87t → 623.6 K
```

**Moderators**:
```
grph.80t → Graphite (carbon)
graph.80t → Graphite (alternate name)
be.80t   → Beryllium metal
beo.80t  → Beryllium oxide
```

**Hydrides**:
```
zrzh.80t → Zirconium hydride (ZrH₁.₆ to ZrH₂)
zrh.80t  → Zirconium hydride (alternate)
yzh.80t  → Yttrium hydride
```

**Organics**:
```
poly.80t → Polyethylene (CH₂)
benz.80t → Benzene (C₆H₆)
```

**Ice**:
```
ice.80t  → Ice (solid H₂O)
```

### MCNP Usage with MT Card

```
Basic syntax:
  M1   1001.80c  2.0      $ H-1
       8016.80c  1.0      $ O-16
  MT1  lwtr.80t           $ Thermal scattering for M1

Important notes:
  - MT card number matches M card number (M1 → MT1)
  - Thermal scattering applies to entire material
  - Only affects low-energy neutrons (typically E < 4 eV)
  - REQUIRED for accurate keff in thermal systems
```

**Complete Example**:
```
c Light water moderated reactor
c Water at 300 K
M1  1001.80c  2.0          $ Hydrogen in H₂O
    8016.80c  1.0          $ Oxygen
MT1 lwtr.80t               $ S(α,β) for H in H₂O
c
10  1  -1.0  -100 IMP:N=1  $ Water cell (ρ = 1.0 g/cm³)
```

**Graphite Example**:
```
c Graphite moderator
M2  6000.80c  1.0          $ Natural carbon
MT2 grph.80t               $ S(α,β) for C in graphite
c
20  2  -1.6  -200          $ Graphite block
```

**Polyethylene Example**:
```
c Polyethylene shield (CH₂)
M3  1001.80c  2.0          $ Hydrogen
    6000.80c  1.0          $ Carbon
MT3 poly.80t               $ S(α,β) for CH₂
c
30  3  -0.92  -300         $ Polyethylene
```

### When Thermal Scattering is Critical

**REQUIRED**:
- Thermal reactors (keff calculation)
- Neutron thermalization studies
- Critical assemblies with thermal spectrum
- Precise flux distributions in thermal systems

**IMPORTANT**:
- Shielding calculations with thermal neutrons
- Reactor physics benchmarks
- Neutron activation in thermal flux

**OPTIONAL** (but recommended):
- Fast reactors (small thermal component)
- High-energy shielding (MeV neutrons dominate)
- Quick scoping calculations

## Library Verification

### Checking xsdir File

**xsdir file**: Master index of available cross-section data

**Location**: $DATAPATH/xsdir (environment variable)

**Search for ZAID**:
```bash
# Check if specific isotope available
grep "92235.80c" $DATAPATH/xsdir

# Check all uranium isotopes in .80c library
grep "92[0-9][0-9][0-9].80c" $DATAPATH/xsdir

# Check thermal scattering libraries
grep "\.80t" $DATAPATH/xsdir
```

**xsdir Entry Format**:
```
ZAID  atomic_weight  filename  access_route  file_length  ...

Example:
92235.80c  235.04393  endf80/U/92235.800nc  0  1  4687  0  0  2.53e-08
│         │           │                     │  │  │
│         │           │                     │  │  └─ Number of energy points
│         │           │                     │  └─ File type
│         │           │                     └─ Access route
│         │           └─ Data file path
│         └─ Atomic weight (amu)
└─ ZAID identifier
```

### Common Availability Issues

**Isotope Not in Library**:
```
Problem: grep "95255" xsdir returns nothing
Solution options:
  1. Use natural element (if available): 95000.80c
  2. Use nearby isotope: 95254.80c
  3. Use older library: 95255.70c
  4. Process evaluation with NJOY (advanced)
```

**Wrong Library Version**:
```
Problem: Input uses .80c but only .70c available
Solution:
  - Change ZAID in input: 92235.70c
  - Or install .80c library
```

**Missing Thermal Scattering**:
```
Problem: "lwtr.80t" not found
Solution:
  - Check library installation
  - Verify DATAPATH environment variable
  - May need separate thermal scattering library package
```

## ZAID Format Validation

### Validation Checklist

- [ ] Format is ZZZAAA.nnX (6-9 characters)
- [ ] Z matches element (92 for U, 94 for Pu, etc.)
- [ ] A matches isotope (235 for U-235, 239 for Pu-239)
- [ ] Library identifier is two digits (80, not 8)
- [ ] Library type is single character (c, p, e, t)
- [ ] No hyphens or element symbols (92235, not 92-235 or U-235)
- [ ] ZAID exists in xsdir file
- [ ] Temperature library appropriate for problem

### Common Format Errors

```
WRONG:                    RIGHT:
U-235.80c                 92235.80c    (no symbols)
92-235.80c                92235.80c    (no hyphens)
235.80c                   92235.80c    (include Z)
92235.8c                  92235.80c    (two-digit library)
92235.80C                 92235.80c    (lowercase type)
92235.80                  92235.80c    (include type)
92235 .80c                92235.80c    (no spaces)
```

### Validation Example

```python
def validate_zaid(zaid_str):
    """Validate ZAID format"""
    import re

    # Pattern: ZZZAAA.nnX
    pattern = r'^(\d{1,3})(\d{3})\.(\d{2})([a-z])$'
    match = re.match(pattern, zaid_str)

    if not match:
        return False, "Invalid ZAID format"

    z, a, lib, typ = match.groups()
    z, a = int(z), int(a)

    # Validate Z range
    if z < 1 or z > 118:
        return False, f"Invalid atomic number: {z}"

    # Validate A range
    if a < 0 or a > 300:
        return False, f"Invalid mass number: {a}"

    # Check common library types
    valid_types = ['c', 'd', 'p', 'e', 't', 'h', 'm', 'y', 'u', 'v']
    if typ not in valid_types:
        return False, f"Unknown library type: {typ}"

    return True, "Valid ZAID"

# Examples
validate_zaid("92235.80c")  # → True, "Valid ZAID"
validate_zaid("U-235.80c")  # → False, "Invalid ZAID format"
validate_zaid("92235.8c")   # → False, "Invalid ZAID format"
```

## Best Practices

### 1. Use Consistent Library Version

```
Good:
  M1  92235.80c  1.0
      92238.80c  1.0
  M2  1001.80c   2.0
      8016.80c   1.0
  MT2 lwtr.80t

Bad (mixing versions):
  M1  92235.80c  1.0
      92238.70c  1.0      ← Different version
```

### 2. Document ZAID Choices

```
c Natural lead shielding
c Using 82000 (natural) rather than individual isotopes
c Pb-204 (1.4%), Pb-206 (24.1%), Pb-207 (22.1%), Pb-208 (52.4%)
M1  82000.80c  1.0
```

### 3. Verify Library Temperature

```
c High-temperature reactor (900 K)
c Using .82c library for accurate Doppler broadening
M1  92235.82c  1.0       $ U-235 at 900 K
M2  8016.82c   1.0       $ O-16 at 900 K
TMP  900                 $ System temperature
```

### 4. Always Include MT Card for Light Elements

```
c Water moderator - MUST include thermal scattering
M1  1001.80c  2.0        $ H-1
    8016.80c  1.0        $ O-16
MT1 lwtr.80t             $ REQUIRED for accurate keff
```

### 5. Check xsdir Before Running

```bash
# Verify all isotopes available before submitting job
for zaid in 92235.80c 92238.80c 8016.80c 1001.80c; do
    grep -q "$zaid" $DATAPATH/xsdir && echo "$zaid OK" || echo "$zaid MISSING"
done
```

## References

**MCNP Documentation**:
- MCNP6 User Manual, Chapter 5.2 (Material Cards)
- Appendix G (ZAID Cross-Section Library Tables)
- LA-UR-17-29981 (MCNP6.2 Release Notes)

**Cross-Section Libraries**:
- ENDF/B-VIII.0: https://www.nndc.bnl.gov/endf-b8.0/
- ENDF/B-VII.0: https://www.nndc.bnl.gov/endf-b7.0/

**Nuclear Data**:
- NNDC (National Nuclear Data Center): www.nndc.bnl.gov
- IAEA Nuclear Data Services: www-nds.iaea.org

---

**For isotope properties and atomic data, see `isotope_database.md`**
**For library availability checking, see `library_availability.md`**
**For decay data and activation, see `decay_data.md`**
