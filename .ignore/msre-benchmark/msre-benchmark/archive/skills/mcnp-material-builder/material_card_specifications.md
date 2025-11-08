# Material Card Specifications Reference

## Purpose
Comprehensive reference for M card keywords, library identifiers, and target formats.

---

## M Card Complete Syntax

```
Mm  ZAID₁  fraction₁  ZAID₂  fraction₂  ...  keyword=value
```

**Fields:**
- **m:** Material number (0-99,999,999). When m=0, keywords apply to all M cards.
- **ZAID:** Nuclide identifier (target or table identifier)
- **fraction:** Atomic (positive) or weight (negative) fraction
- **keywords:** Optional material-specific properties

---

## Complete M Card Keywords Reference

### Library Selection Keywords (xLIB)

| Keyword | Particle Type | Description | Example |
|---------|---------------|-------------|---------|
| **NLIB=x** | Neutron | Default neutron library | NLIB=80c |
| **PLIB=x** | Photon (photoatomic) | Default photon library | PLIB=04p |
| **PNLIB=x** | Photonuclear | Default photonuclear library | PNLIB=24u |
| **ELIB=x** | Electron | Default electron library | ELIB=03e |
| **HLIB=x** | Proton | Default proton library | HLIB=24h |
| **ALIB=x** | Alpha | Default alpha library | ALIB=84a |
| **SLIB=x** | Helion (³He) | Default helion library | SLIB=31s |
| **TLIB=x** | Triton (³H) | Default triton library | TLIB=31t |
| **DLIB=x** | Deuteron (²H) | Default deuteron library | DLIB=31d |

**Example (Multi-particle problem):**
```
MODE  N H P E
M1   1001  2  8016  1  NLIB=80c  PLIB=04p  HLIB=24h  ELIB=03e
```

---

### Electron Transport Keywords

| Keyword | Description | Values | Default |
|---------|-------------|--------|---------|
| **GAS=value** | Density-effect correction to electron stopping power | 0=condensed state, 1=gaseous state | 0 |
| **ESTEP=n** | Number of electron sub-steps per energy step | n ≥ built-in default | Internally set |
| **HSTEP=n** | Number of proton/heavy-ion sub-steps per energy step | n ≥ built-in default | ESTEP value if specified |

**Example (Electron transport in air):**
```
MODE  N E
M1   7014  -0.7552  8016  -0.2315  18000  -0.0133  GAS=1  ESTEP=10
```

**Use Case:** GAS=1 for low-density materials (air, gases); GAS=0 for solids/liquids.

---

### Optical Properties Keywords

| Keyword | Description | Format | Units |
|---------|-------------|--------|-------|
| **REFI=A** | Constant refractive index | Single value | Dimensionless |
| **REFC=A B C D** | Cauchy coefficients for wavelength-dependent refractive index | Four coefficients | Micrometers |
| **REFS=B₁ C₁ B₂ C₂ B₃ C₃** | Sellmeier coefficients for refractive index | Six coefficients | Dimensionless |

**Formulas:**
- **Cauchy:** n(λ) = A + B/λ² + C/λ⁴ + D/λ⁶
- **Sellmeier:** n²(λ) = 1 + B₁λ²/(λ² - C₁) + B₂λ²/(λ² - C₂) + B₃λ²/(λ² - C₃)

**Example (Water with constant refractive index):**
```
M1   1001  2  8016  1  REFI=1.3199
```

**Example (Borosilicate glass with Sellmeier coefficients):**
```
M1   14028  1  8016  2  REFS=1.0396 6e-3 0.2318 2.0018e-2 1.0104 1.0356e2
```

---

### Electron Conduction State Keyword

| Keyword | Description | Values |
|---------|-------------|--------|
| **COND=value** | Material conduction state (EL03 electron transport only) | <0: non-conductor<br>0: mixed (DEFAULT)<br>>0: conductor |

**Example (Metal as conductor):**
```
M1   26000  1.0  COND=1      $ Iron as conductor
```

---

## M0 Card: Default Library Settings

The **M0** card sets default library identifiers for **all materials** in the problem.

**Format:**
```
M0   NLIB=80c  PLIB=04p  ELIB=03e
```

**Use Cases:**

1. **Project-wide library standardization:**
```
M0   NLIB=80c  PLIB=04p     $ All materials use ENDF/B-VIII.0 by default

M1   1001  2  8016  1        $ Water: uses .80c automatically
M2   92235  1  92238  9      $ Uranium: uses .80c automatically
M3   26000  1                $ Iron: uses .80c automatically
```

2. **Override specific materials:**
```
M0   NLIB=80c                $ Default: ENDF/B-VIII.0

M1   1001.80c  2  8016.80c  1     $ Water: uses default .80c
M2   92235.70c  1  92238.70c  9   $ Uranium: explicitly uses .70c (overrides M0)
```

**Priority Hierarchy:**
When multiple library specifications exist, MCNP uses this priority order:
1. **MX card** (nuclide substitution for specific particle type)
2. **Full table identifier on M card** (e.g., 1001.80c)
3. **xLIB keyword on M card** (e.g., NLIB=80c)
4. **xLIB keyword on M0 card** (project-wide default)

---

## Library Loading Priority Hierarchy

MCNP resolves library identifiers in this order (highest to lowest priority):

```
PRIORITY 1 (Highest)
├─> MX card with full table identifier
│   Example: MX1:P  6012.24u  8016.24u
│
PRIORITY 2
├─> M card with full table identifier
│   Example: M1  1001.80c  2  8016.80c  1
│
PRIORITY 3
├─> xLIB keywords on M card
│   Example: M1  1001  2  8016  1  NLIB=80c  PLIB=04p
│
PRIORITY 4 (Lowest)
└─> xLIB keywords on M0 card
    Example: M0  NLIB=80c  PLIB=04p
```

**Example (Demonstrating priority):**
```
M0   NLIB=70c                       $ Priority 4: Default .70c for all materials

M1   1001  2  8016.80c  1  NLIB=80c  $ H-1: Priority 3 (.80c via NLIB)
                                     $ O-16: Priority 2 (.80c via full identifier)

MX1:P  1000.04p  8000.04p           $ Priority 1: Photoatomic uses .04p for both
```

**Result:**
- Neutron: H-1 uses .80c (Priority 3), O-16 uses .80c (Priority 2)
- Photon: H uses .04p (Priority 1), O uses .04p (Priority 1)

---

## Target Identifier Formats

MCNP supports multiple target identifier formats (all resolve to same nuclide):

| Format | Example | Interpretation | Usage |
|--------|---------|----------------|-------|
| **ZZZAAA** | 1001 | H-1 (Z=1, A=1) | Most compact |
| **ZZZAAA.nnX** | 1001.80c | H-1 with ENDF/B-VIII.0 neutron library | Most explicit |
| **Symbol-A** | H-1 | H-1 | Most readable |
| **Symbol-A.nnX** | H-1.80c | H-1 with ENDF/B-VIII.0 | Readable + library |
| **ZZZAAA+S×400** | 47510 | Ag-110m (metastable, S=1) | Older metastable format |
| **Symbol-Am** | Ag-110m | Ag-110m (modern metastable) | Modern metastable |

**Examples:**
```
M1   1001  1          $ H-1 using ZZZAAA
M2   H-1  1           $ H-1 using Symbol-A
M3   1001.80c  1      $ H-1 using ZZZAAA.nnX
M4   H-1.80c  1       $ H-1 using Symbol-A.nnX
M5   Ag-110m  1       $ Ag-110m metastable (modern)
M6   47510  1         $ Ag-110m metastable (older format, equivalent to above)
```

**Recommendation:** Use **Symbol-A.nnX** format for readability and explicitness.

---

## Natural Isotopes (AAA=000)

For natural isotopic mixtures, use AAA=000 or Symbol-0:

```
M1   26000  1.0       $ Fe-natural (ZZZAAA format)
M2   Fe-0  1.0        $ Fe-natural (Symbol-A format, equivalent)
```

MCNP automatically weights isotopes by natural abundance from xsdir.

---

## Material Composition: Atomic vs Weight Fractions

| Specification | Fraction Sign | Density Sign in Cell Card | Interpretation |
|---------------|---------------|---------------------------|----------------|
| **Atomic fractions** | Positive | Negative | Ratio of atoms (e.g., H₂O = 2:1) |
| **Weight fractions** | Negative | Positive | Fraction by mass (must sum to 1.0 or -1.0) |

**Example (Water - both methods):**
```
c Method 1: Atomic fractions
M1   1001  2  8016  1             $ Atomic ratio 2:1
c Cell card:
1    1  -0.1003  -1  IMP:N=1      $ ρ=0.1003 atoms/b-cm (negative = atomic)

c Method 2: Weight fractions
M2   1001  -0.1119  8016  -0.8881 $ Weight fractions (sum = -1.0)
c Cell card:
2    2  1.0  -2  IMP:N=1          $ ρ=1.0 g/cm³ (positive = mass)
```

**CRITICAL RULE:** Density sign in cell card MUST match M card fraction type:
- **Atomic fractions** → **Negative density** (atoms/b-cm)
- **Weight fractions** → **Positive density** (g/cm³)

---

## Fraction Normalization

MCNP normalizes fractions if they don't sum to 1.0 (or -1.0).

**Examples:**
```
c Unnormalized (MCNP will renormalize):
M1   1001  2  8016  1              $ Sums to 3 → normalized to 2/3 and 1/3

c Pre-normalized (recommended):
M2   1001  0.6667  8016  0.3333    $ Already normalized
```

**Best Practice:** Always normalize fractions yourself for clarity and verification.

---

## BURN Card Nuclides

For BURN (burnup) calculations, nuclides added through transmutation use:
- **xLIB keywords** from M card (Priority 3) or M0 card (Priority 4)
- **First library in xsdir** if no xLIB specified

**Example (Burnup problem with library control):**
```
M0   NLIB=80c                      $ Ensure transmutation products use .80c
M1   92235  0.03  92238  0.97  8016  2.0
BURN  TIME=0 100 500 1000          $ Transmutation occurs
```

Without M0 or xLIB, transmutation products may use inconsistent libraries.

---

## Keywords Not Allowed to Separate Pairs

**WARNING:** M card keywords may appear anywhere among target-fraction pairs, **but must not separate a pair**.

**WRONG:**
```
M1   1001  NLIB=80c  2  8016  1   $ WRONG: Keyword separates 1001 from its fraction
```

**CORRECT:**
```
M1   1001  2  8016  1  NLIB=80c   $ Correct: Keyword after all pairs
M1   NLIB=80c  1001  2  8016  1   $ Correct: Keyword before all pairs
```

---

## See Also

- **Thermal Scattering:** `thermal_scattering_reference.md` for MT, MT0 cards
- **Advanced Cards:** `advanced_material_cards.md` for OTFDB, NONU, AWTAB, XS cards
- **Error Troubleshooting:** `material_error_catalog.md`
- **MCNP Documentation:** Chapter 5.6 (Material Data Cards)

---

**Version:** 1.0
**Created:** 2025-11-03
**For:** mcnp-material-builder skill v2.0
