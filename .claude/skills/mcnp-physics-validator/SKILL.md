---
name: "MCNP Physics Validator"
description: "Validates MCNP physics settings including MODE, PHYS cards, cross-section libraries, energy cutoffs, and particle production. Use when checking physics setup."
version: "1.0.0"
dependencies: "python>=3.8"
---

# MCNP Physics Validator

## Overview

Physics settings control what particles are transported, how they interact, and what approximations are used. Incorrect physics can produce meaningless results even with perfect geometry. This skill validates:

- MODE card (particle types to transport)
- PHYS cards (physics options for each particle)
- Cross-section library specifications (ZAID format, library versions)
- Energy cutoffs and ranges
- Secondary particle production settings
- Physics model vs tabular data usage
- Temperature-dependent cross sections

Use this when users need to verify their physics setup is appropriate for their problem type (thermal reactor, shielding, medical physics, high-energy, etc.).

## Workflow Decision Tree

### When to Invoke
- User asks about physics settings or "is my physics correct?"
- Before criticality calculations (KCODE)
- When results seem unphysical
- Switching between problem types (thermal ↔ fast, neutron-only ↔ coupled)
- After modifying MODE or PHYS cards

### Validation Approach

**Quick Physics Check:**
- Verify MODE appropriate for problem
- Check cross-section library formats
- Confirm energy ranges
→ Fast check for obvious issues

**Comprehensive Physics Validation** (recommended):
- All quick checks
- Detailed PHYS card analysis
- Secondary production verification
- Library version consistency
- Temperature settings
→ Use before production runs

**Problem-Specific Validation:**
- Thermal reactor physics
- Fast neutron systems
- Photon/electron transport
- High-energy particle transport
→ Tailored checks for specific problem types

## Physics Validation Procedure

### Step 1: Understand the Problem
Ask user about physics requirements:
- "What particles need to be transported?" (n, p, e, ions?)
- "What energy range?" (thermal, MeV, GeV?)
- "What phenomena are important?" (fission, photon production, bremsstrahlung?)
- "Is this thermal or fast system?"
- "Do you need photoneutrons?" (for beryllium, deuterium)

### Step 2: Read Reference Materials
**MANDATORY - READ ENTIRE FILE**: Read `.claude/commands/mcnp-physics-validator.md` for:
- Complete physics validation procedures
- MODE and PHYS card specifications
- Cross-section library requirements
- Energy cutoff guidelines
- Common physics errors and fixes

### Step 3: Validate Physics Settings

```python
from parsers.input_parser import MCNPInputParser

parser = MCNPInputParser()
parsed = parser.parse_file('input.inp')

# Extract physics cards
mode_card = parsed['data_cards'].get('mode')
phys_cards = {k: v for k, v in parsed['data_cards'].items() 
              if k.startswith('phys')}
materials = {k: v for k, v in parsed['data_cards'].items()
             if k.startswith('m') and k[1:].isdigit()}

# Validate each component
# (Use manual validation logic or dedicated validator)
```

### Step 4: Report Physics Issues

Organize by component:
1. **MODE card** - Particle types
2. **PHYS cards** - Physics options
3. **Cross sections** - Library specifications
4. **Energy settings** - Cutoffs and ranges
5. **Secondary production** - Particle generation
6. **Recommendations** - Best practices

### Step 5: Guide User to Correct Setup

For each issue:
- Explain what's wrong/missing
- Show correct syntax with example
- Explain physics implications
- Reference manual sections

## MODE Card Validation (Chapter 4.5)

### Particle Designators (Table 4.3)

**Most common:**
- **N** - Neutron
- **P** - Photon (gamma rays)
- **E** - Electron (includes positrons with F designation)
- **H** - Proton
- **#** - Heavy ions

**Proper MODE specifications:**
```
MODE N          ← Neutron-only (default if omitted)
MODE N P        ← Neutron + photon production
MODE P E        ← Photon + electron (coupled)
MODE N P E      ← Full n-p-e coupling
MODE H          ← Proton transport
MODE N P H      ← Neutron + photon + proton
```

### Common MODE Mistakes

**Problem:** MODE N but need photon transport
```
c WRONG - Only neutrons transported
MODE N
c Photons from (n,γ) not transported!

c CORRECT - Transport both
MODE N P
c Now photons from neutron reactions are transported
```

**Problem:** Electron/positron confusion
```
c Positrons still need MODE E
MODE F          ← WRONG - not recognized
MODE E          ← CORRECT - includes positrons
```

### Physics Implications

**MODE N only:**
- Neutron transport
- Photons produced but NOT transported
- Fast, but misses photon contributions

**MODE N P:**
- Neutron transport
- Photons from (n,γ), (n,n'), etc. transported
- More realistic but slower
- Photo-neutrons NOT included (unless ISPN on PHYS:P)

**MODE P E:**
- Photon transport
- Electrons from Compton, pair production transported
- Bremsstrahlung photons transported
- Needed for accurate dose in electron fields

## PHYS Card Validation

### PHYS:N (Neutron Physics)

**Format:**
```
PHYS:N emax emcnf iunr J J J coilf cutn ngam J J i_int_model i_els_model
```

**Key parameters:**
- **emax** (default 100 MeV): Upper energy limit
  - MUST exceed maximum source energy
  - Example: 14 MeV source → emax ≥ 14 MeV

- **ngam** (default 1): Photon production
  - 0 = No photon production
  - 1 = From tables (standard)
  - 2 = From models (high energy)

**Validation checks:**
```python
# Check emax covers source energy
source_energy = get_max_source_energy(parsed)
phys_n = parsed['data_cards'].get('phys:n')
if phys_n:
    emax = phys_n.entries[0] if phys_n.entries else 100.0
    if source_energy > emax:
        ERROR: "Source energy exceeds PHYS:N emax"
```

### PHYS:P (Photon Physics)

**Format:**
```
PHYS:P emcpf ides nocoh ispn nodop J fism
```

**Key parameters:**
- **ides** (default 0): Electron generation
  - 0 = Electrons produced (needed for MODE P E)
  - 1 = No electrons (photon-only)

- **ispn** (default 0): Photonuclear
  - -1 = Analog (unbiased)
  - 0 = OFF (default, no photo-neutrons)
  - 1 = Biased (for variance reduction)

**Common issue:**
```
MODE P E
PHYS:P J 1     ← ides=1, NO ELECTRONS!

Problem: MODE says transport electrons,
         but PHYS:P says don't produce them!
         
Fix: PHYS:P J 0  (or omit, 0 is default)
```

### PHYS:E (Electron Physics)

**Key considerations:**
- Bremsstrahlung production
- Energy deposition
- Substep settings (ESTEP on M card)

## Cross-Section Validation

### ZAID Format

**Proper format:** ZZZAAA.XXc

Where:
- **ZZZ** = Atomic number (1-118)
- **AAA** = Mass number (0 for natural, or specific isotope)
- **XX** = Library version
- **c** = Library type suffix

**Examples:**
```
92235.80c    ← U-235, ENDF/B-VIII.0, neutron
1001.71c     ← H-1, ENDF/B-VII.1, neutron
6000.80c     ← Natural carbon, ENDF/B-VIII.0
1001.24p     ← H-1, photoatomic (for MODE P)
26000.03e    ← Natural iron, electron
```

### Library Suffix Validation

**Must match particle type:**

| Suffix | Type | Used with |
|--------|------|-----------|
| .XXc | Neutron | MODE N |
| .XXp | Photoatomic | MODE P |
| .XXu | Photonuclear | MODE P with ISPN≠0 |
| .XXe | Electron | MODE E |
| .XXt | Thermal S(α,β) | MT card |

**Common errors:**
```
MODE N
M1 92235.80c 1    ← CORRECT (.c for neutrons)

MODE P
M1 6000.80c 1     ← WRONG! (.c is neutron, need .p)
M1 6000.24p 1     ← CORRECT (.p for photons)
```

### Library Version Consistency

**Problem:** Mixed library versions
```
M1 92235.80c 1     ← ENDF/B-VIII.0
   92238.70c 4     ← ENDF/B-VII.0 

WARNING: Inconsistent libraries may cause issues
Better: Use same version for all isotopes in material
```

**Recommended libraries (2025):**
- **ENDF/B-VIII.0** (.80c) - Latest, use when available
- **ENDF/B-VII.1** (.71c) - Widely validated
- **ENDF/B-VII.0** (.70c) - Older, still acceptable

## Energy Cutoff Validation (Table 4.3)

### Default Cutoffs

| Particle | Low Cutoff | Default Cutoff |
|----------|------------|----------------|
| Neutron | 0.0 MeV | 0.0 MeV |
| Photon | 1 eV | 1 keV |
| Electron | 10 eV | 1 keV |
| Proton | 1 keV | 1 MeV |

### Validation Checks

**Photon cutoff vs problem:**
```
c Thermal system, need low-energy gammas
Default cutoff: 1 keV may be too high

Recommendation:
CUT:P J J -0.001   ← 100 eV cutoff

c High-energy problem
Default cutoff: 1 keV is fine
```

**Energy range vs source:**
```
SDEF ERG=14.0      ← 14 MeV source
PHYS:N 10          ← emax = 10 MeV

ERROR: Source energy exceeds physics limit!
Fix: PHYS:N 20 (or higher)
```

## Secondary Particle Production

### Neutron → Photon

Controlled by **ngam** on PHYS:N:
```
MODE N P
PHYS:N J J J J J J J J 1    ← ngam=1, photons from tables

Common mistake:
MODE N P
PHYS:N J J J J J J J J 0    ← ngam=0, NO PHOTONS!

Result: MODE says transport photons,
        but PHYS says don't produce them!
```

### Photon → Electron

Controlled by **ides** on PHYS:P:
```
MODE P E
PHYS:P J 0     ← ides=0, electrons produced (correct)

Wrong:
MODE P E
PHYS:P J 1     ← ides=1, NO electrons produced
```

### Photon → Neutron

Controlled by **ispn** on PHYS:P:
```
c For beryllium photodisintegration
MODE N P
PHYS:P J J J 1     ← ispn=1, photo-neutrons ON

c Need photonuclear libraries (.XXu)
M1 4009.24u 1      ← Be-9 photonuclear
```

## Temperature-Dependent Cross Sections

### TMP Card (Chapter 5.6)

**CRITICAL:** Temperature in MeV, NOT Kelvin!

**Conversion:**
```
MeV = k_B × T_Kelvin
k_B = 8.617333×10⁻⁵ eV/K = 8.617333×10⁻¹¹ MeV/K

Examples:
293.6 K (room temp) = 2.53×10⁻⁸ MeV
600 K = 5.17×10⁻⁸ MeV
```

**Common mistake:**
```
TMP 300        ← WRONG! This is 300 MeV (insanely hot!)
TMP 2.53E-8    ← CORRECT (300 K in MeV)
```

### Thermal Scattering (MT Card)

**For thermal neutrons in moderators:**
```
c Light water thermal scattering
M1 1001.80c 2
   8016.80c 1
MT1 lwtr.20t    ← S(α,β) for H in H2O

c Heavy water
MT1 hwtr.20t    ← S(α,β) for D in D2O

c Graphite
MT1 grph.20t    ← S(α,β) for C in graphite
```

**Without MT card:**
- Free gas thermal scattering (less accurate)
- Acceptable for fast systems
- Important for thermal systems

## Integration with Other Skills

**Workflow:**
1. mcnp-input-validator (overall syntax)
2. mcnp-physics-validator (detailed physics) ← YOU ARE HERE
3. mcnp-material-builder (if need to fix materials)
4. mcnp-cross-section-manager (library management)

**Related skills:**
- mcnp-material-builder: Creating material specifications
- mcnp-cross-section-manager: Finding/managing libraries
- mcnp-isotope-lookup: ZAID lookups

## Example Physics Validation Workflow

```
User: "Check my thermal reactor physics setup"

Claude: I'll validate your physics settings for thermal reactor calculations.

[Reads .claude/commands/mcnp-physics-validator.md]
[Analyzes input file]

**Physics Validation Results:**

CORRECT SETTINGS:
✓ MODE N P - Neutron and photon transport enabled
✓ Cross sections: All use .80c (ENDF/B-VIII.0)
✓ PHYS:N emax=20 MeV - Covers potential source energies
✓ Photon production enabled (ngam=1)

ERRORS:
❌ Missing S(α,β) thermal scattering
   Problem: Light water moderator without MT card
   Impact: Inaccurate thermal neutron treatment
   Fix: Add "MT1 lwtr.20t" after M1 card
   Reference: §5.6.2 (MT Card)

❌ TMP card value suspicious
   Current: TMP 600
   Problem: This is 600 MeV (physically impossible!)
   Should be: TMP 5.17E-8 (for 600 K)
   Conversion: MeV = 8.617E-11 × T_Kelvin
   Reference: §5.6 (Material cards, temperature)

WARNINGS:
⚠ Default photon cutoff 1 keV
   Consideration: May be too high for thermal gammas
   Optional: CUT:P J J -0.001 (100 eV cutoff)
   Impact: More accurate but slower

RECOMMENDATIONS:
1. Add thermal scattering (CRITICAL):
   ```
   M1 1001.80c 2
      8016.80c 1
   MT1 lwtr.20t
   ```

2. Fix temperature (CRITICAL):
   ```
   c For 600 K:
   TMP 5.17E-8
   ```

3. Consider lower photon cutoff:
   ```
   CUT:P J J -0.001
   ```

4. Verify in output file:
   - Check loaded cross-section libraries
   - Confirm lwtr.20t loaded
   - Check for any missing data warnings

Would you like me to:
1. Generate corrected material cards?
2. Explain thermal scattering physics?
3. Help calculate TMP values for other temperatures?
```

## Important Principles

1. **MODE and PHYS must be consistent** - Can't transport what you don't produce
2. **Cross-section libraries must match particles** - .c for neutrons, .p for photons
3. **Temperature in MeV, not Kelvin** - Most common mistake!
4. **Thermal systems need S(α,β)** - MT card critical for accuracy
5. **Check output for loaded libraries** - Validation confirms format, not availability
6. **Energy ranges must cover sources** - emax ≥ source energy

## Code Style

When validating physics:
- Check MODE first (determines what else to check)
- Verify cross-section formats carefully
- Calculate temperature conversions explicitly
- Provide corrected cards, not just errors
- Reference physics implications, not just syntax

## Dependencies

Required components:
- Input parser: `parsers/input_parser.py`
- ZAID database: `utils/zaid_database.py`
- Reference: `.claude/commands/mcnp-physics-validator.md`
- Physical constants: `skills/utilities/mcnp_physical_constants.py`

## References

**Primary References:**
- `.claude/commands/mcnp-physics-validator.md` - Detailed procedures
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - Physics cards quick reference
- Chapter 3.2.5.1: MODE card
- Chapter 4.5: Particle designators
- Table 4.3: Particle parameters and cutoffs
- §5.6: Material specification (M, MT, TMP cards)
- §5.7: Physics cards (PHYS, CUT, ELPT)
- §3.4.5: Warnings and limitations

**Key Topics:**
- ZAID format and library suffixes
- Temperature units (MeV vs Kelvin)
- Secondary particle production
- Thermal scattering libraries
- Energy cutoff selection

**Related Skills:**
- mcnp-material-builder
- mcnp-cross-section-manager
- mcnp-isotope-lookup
- mcnp-unit-converter
