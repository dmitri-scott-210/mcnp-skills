# MCNP Physics Validator - Skill Refinement Plan

**Created**: November 8, 2025
**Skill**: mcnp-physics-validator
**Priority**: 🔴 **CRITICAL** - Missing thermal scattering validation causes 1000s of pcm reactivity errors
**Based On**: AGR-1 Material Card Analysis, HTGR Best Practices Synthesis, Comprehensive Findings

---

## EXECUTIVE SUMMARY

### Current State Assessment

**Strengths** ✅:
- Good basic MODE card validation
- Cross-section ZAID format checking
- Energy cutoff guidance
- Temperature conversion formulas (MeV vs Kelvin)
- PHYS card consistency checking

**Critical Gaps** ❌:
- **NO systematic thermal scattering validation** - skill mentions MT cards but doesn't validate missing ones
- **NO temperature-dependent library selection** - doesn't guide grph.18t vs grph.24t
- **NO cross-section library version consistency checking** - mixed .70c/.80c/.00c not flagged
- **NO TRISO/complex fuel physics patterns** - missing guidance for multi-layer particle models
- **NO HTGR-specific physics validation** - no graphite temperature-dependent scattering checks

**Impact**: Users building thermal reactors (PWR, HTGR, RBMK, etc.) will have **WRONG reactivity** (1000-5000 pcm errors) and **WRONG thermal spectra** due to missing MT cards.

---

## FINDINGS FROM ANALYSIS DOCUMENTS

### Finding 1: Missing Graphite Thermal Scattering (CRITICAL)

**Source**: AGR1_Material_Card_Analysis.md, lines 566-594

**Problem Found in Production Model**:
```mcnp
c AGR-1 TRISO fuel - NO MT CARDS FOR GRAPHITE!
m9040  $ Pure graphite spacer, density = 1.015 g/cm3
    6012.00c  0.9890
    6013.00c  0.0110
c ❌ MISSING: mt9040 grph.18t

m9090  $ Buffer layer (porous carbon)
    6012.00c  0.9890
    6013.00c  0.0110
c ❌ MISSING: mt9090 grph.18t

m9091  $ IPyC (Inner Pyrolytic Carbon)
    6012.00c  0.9890
    6013.00c  0.0110
c ❌ MISSING: mt9091 grph.18t

[... ~50 graphite materials WITHOUT MT cards ...]
```

**Impact**:
- ❌ Wrong thermal neutron spectrum (hardened)
- ❌ Reactivity error: typically 1000-5000 pcm
- ❌ Flux distribution errors
- ❌ Invalid benchmark comparisons

**Recommendation**: Add systematic thermal scattering validator that **FAILS** if graphite materials lack MT cards

### Finding 2: Temperature-Dependent Library Selection

**Source**: AGR1_Material_Card_Analysis.md, lines 1180-1210

**Current Practice** (WRONG):
```mcnp
c AGR-1 operating at 600K - uses WRONG library!
mt10 lwtr.10t  $ 294K water (room temp) - reactor at 62°C!
c ❌ Should use lwtr.11t (325K) or lwtr.13t (350K)

c NO graphite MT cards at all
c ❌ Should use grph.18t (600K) for operating conditions
```

**Available Temperature Libraries**:

**Graphite**:
- grph.10t - 296K (room temperature, cold criticals)
- grph.18t - 600K (HTGR operating, some fast reactors)
- grph.22t - 800K (high-temperature HTGR)
- grph.24t - 1000K (VHTR)
- grph.26t - 1200K (VHTR accident)
- grph.28t - 1600K (severe accident)
- grph.30t - 2000K (extreme accident)

**Water**:
- lwtr.10t - 294K (room temperature)
- lwtr.11t - 325K (PWR cold leg ~52°C)
- lwtr.13t - 350K (PWR average ~77°C)
- lwtr.14t - 400K (PWR hot leg ~127°C)
- lwtr.16t - 500K (supercritical water reactor)
- lwtr.20t - 800K (steam, BWR conditions)

**Recommendation**: Add temperature-dependent library selector that matches reactor operating conditions

### Finding 3: Cross-Section Library Version Inconsistencies

**Source**: AGR1_Material_Card_Analysis.md, lines 78-109

**Problem Found**:
```mcnp
c Mixed ENDF versions in SAME model:
m2106  $ ATR fuel
    1001.70c  3.393340E-02  $ ENDF/B-VII.0
    8016.70c  1.696670E-02  $ ENDF/B-VII.0
   92235.70c  4.198373E-04  $ ENDF/B-VII.0

m9000  $ SS316L
   24050.00c -0.00653131  $ ENDF/B-VI.0 ← INCONSISTENT!
   26056.00c -0.60409084  $ ENDF/B-VI.0
   28058.00c -0.08053185  $ ENDF/B-VI.0

m8900  $ Air
    7014.80c -0.76         $ ENDF/B-VIII.0 ← ALSO INCONSISTENT!
    8016.80c -0.24
```

**Libraries Used**:
- .00c - ENDF/B-VI.0 (oldest)
- .50c - ENDF/B-V
- .60c - ENDF/B-VI.8
- .70c - ENDF/B-VII.0 (most common)
- .80c - ENDF/B-VIII.0 (latest)

**Recommendation**: Flag mixed library versions, recommend standardization to .80c or .70c

### Finding 4: Thermal Scattering for ALL Moderator Types

**Source**: AGR1_Material_Card_Analysis.md, lines 513-567

**Materials Requiring S(α,β)**:

**Water** (lwtr.XXt):
```mcnp
m10  $ Water (1.00276e-01 atoms/barn-cm total)
    8016.70c  3.34253-2
    1001.70c  6.68506-2
mt10 lwtr.10t  ← REQUIRED!
```

**Heavy Water** (hwtr.XXt):
```mcnp
m20  $ D2O moderator
    1002.70c  2  $ Deuterium
    8016.70c  1
mt20 hwtr.10t  ← REQUIRED for CANDU, research reactors
```

**Beryllium** (be.01t):
```mcnp
m18  $ Beryllium reflector
    4009.60c  1.23621-1
mt18 be.01t  ← REQUIRED!
```

**Mixed Be + H₂O** (DUAL thermal scattering):
```mcnp
m14  $ Medium I hole Be + H2O
    1001.70c  3.40940-3
    8016.70c  1.70470-3
    4009.60c  1.17316-1
mt14 lwtr.10t be.01t  ← BOTH required!
```

**Polyethylene** (poly.XXt):
```mcnp
m30  $ Polyethylene shield
    1001.70c  0.667
    6000.70c  0.333
mt30 poly.10t  ← REQUIRED for shielding
```

**Graphite** (grph.XXt):
```mcnp
m40  $ Graphite moderator/reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt40 grph.18t  ← REQUIRED! (temperature-dependent)
```

**Recommendation**: Create comprehensive thermal scattering validator for ALL moderator/reflector materials

### Finding 5: Complex Fuel Physics Validation

**Source**: AGR1_Material_Card_Analysis.md, lines 213-303 (TRISO structure)

**TRISO 5-Layer Validation Requirements**:

```
┌─────────────────────────────────────────┐
│  Matrix (m9094) - needs grph.18t       │
│  ┌─────────────────────────────────┐    │
│  │ OPyC (m9093) - needs grph.18t  │    │
│  │ ┌─────────────────────────────┐ │    │
│  │ │ SiC (m9092) - ceramic      │ │    │
│  │ │ ┌─────────────────────────┐ │ │    │
│  │ │ │ IPyC (m9091) - grph.18t│ │ │    │
│  │ │ │ ┌─────────────────────┐ │ │ │    │
│  │ │ │ │ Buffer (m9090)     │ │ │ │    │
│  │ │ │ │   - needs grph.18t │ │ │ │    │
│  │ │ │ │ ┌─────────────────┐ │ │ │ │    │
│  │ │ │ │ │ UCO Kernel     │ │ │ │ │    │
│  │ │ │ │ │ (m9111)        │ │ │ │ │    │
│  │ │ │ │ └─────────────────┘ │ │ │ │    │
│  │ │ │ └─────────────────────┘ │ │ │    │
│  │ │ └─────────────────────────┘ │ │    │
│  │ └─────────────────────────────┘ │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Physics Requirements**:
1. **Kernel (UCO)**: No S(α,β) needed (fuel, not moderator)
2. **Buffer**: Porous carbon → **needs grph.18t** (600K)
3. **IPyC**: Dense carbon → **needs grph.18t**
4. **SiC**: Silicon carbide → NO S(α,β) (ceramic)
5. **OPyC**: Dense carbon → **needs grph.18t**
6. **Matrix**: Graphite → **needs grph.18t**

**Recommendation**: Add TRISO fuel validation pattern to check all carbon layers have MT cards

---

## REFINEMENT REQUIREMENTS

### Requirement 1: Thermal Scattering Validation (CRITICAL)

**Functionality**:
```python
def validate_thermal_scattering(materials, mt_cards, mode):
    """
    Validate that ALL materials requiring S(α,β) have MT cards

    Returns ERRORS for missing MT cards (not just warnings!)
    """
    errors = []
    warnings = []

    for mat_id, material in materials.items():
        # Check for moderator/reflector isotopes
        has_hydrogen = any(zaid.startswith('1001') or zaid.startswith('1002') for zaid in material)
        has_carbon = any(zaid.startswith('6000') or zaid.startswith('6012') for zaid in material)
        has_beryllium = any(zaid.startswith('4009') for zaid in material)

        # Graphite check (CRITICAL for HTGR/RBMK)
        if has_carbon and MODE includes 'N':
            if mat_id not in mt_cards or 'grph' not in mt_cards[mat_id]:
                errors.append({
                    'material': mat_id,
                    'type': 'MISSING_GRAPHITE_THERMAL_SCATTERING',
                    'severity': 'CRITICAL',
                    'impact': 'Wrong thermal neutron spectrum, reactivity error 1000-5000 pcm',
                    'fix': f'Add "mt{mat_id} grph.18t" (or appropriate temperature)'
                })

        # Water check
        if has_hydrogen and has_oxygen:
            if mat_id not in mt_cards or 'lwtr' not in mt_cards[mat_id]:
                errors.append({
                    'material': mat_id,
                    'type': 'MISSING_WATER_THERMAL_SCATTERING',
                    'severity': 'CRITICAL',
                    'impact': 'Inaccurate thermal neutron treatment',
                    'fix': f'Add "mt{mat_id} lwtr.13t" (or appropriate temperature)'
                })

        # Beryllium check
        if has_beryllium:
            if mat_id not in mt_cards or 'be' not in mt_cards[mat_id]:
                errors.append({
                    'material': mat_id,
                    'type': 'MISSING_BERYLLIUM_THERMAL_SCATTERING',
                    'severity': 'CRITICAL',
                    'impact': 'Wrong reflector physics',
                    'fix': f'Add "mt{mat_id} be.01t"'
                })

    return errors, warnings
```

**Test Cases**:
```python
# Test 1: Missing graphite S(α,β) (HTGR)
materials = {
    '1': {'6012.00c': 0.989, '6013.00c': 0.011}  # Graphite
}
mt_cards = {}  # NO MT card
result = validate_thermal_scattering(materials, mt_cards, 'N')
assert result['errors'][0]['type'] == 'MISSING_GRAPHITE_THERMAL_SCATTERING'
assert result['errors'][0]['severity'] == 'CRITICAL'

# Test 2: Missing water S(α,β) (PWR)
materials = {
    '2': {'1001.70c': 2.0, '8016.70c': 1.0}  # Water
}
mt_cards = {}
result = validate_thermal_scattering(materials, mt_cards, 'N')
assert result['errors'][0]['type'] == 'MISSING_WATER_THERMAL_SCATTERING'

# Test 3: Correct graphite with MT card
materials = {
    '3': {'6012.00c': 0.989, '6013.00c': 0.011}
}
mt_cards = {'3': ['grph.18t']}
result = validate_thermal_scattering(materials, mt_cards, 'N')
assert len(result['errors']) == 0

# Test 4: Mixed Be + H2O (needs BOTH)
materials = {
    '4': {'1001.70c': 0.01, '8016.70c': 0.005, '4009.60c': 0.98}
}
mt_cards = {'4': ['lwtr.10t']}  # Missing be.01t!
result = validate_thermal_scattering(materials, mt_cards, 'N')
assert result['errors'][0]['type'] == 'MISSING_BERYLLIUM_THERMAL_SCATTERING'
```

### Requirement 2: Temperature-Dependent Library Selection

**Functionality**:
```python
def select_thermal_library(material_type, temperature_K):
    """
    Select appropriate temperature-dependent S(α,β) library

    Args:
        material_type: 'graphite', 'water', 'heavy_water', 'polyethylene', 'beryllium'
        temperature_K: Operating temperature in Kelvin

    Returns:
        Recommended library (e.g., 'grph.18t')
    """

    if material_type == 'graphite':
        if temperature_K < 400:
            return 'grph.10t', 296, 'Room temperature (cold critical)'
        elif temperature_K < 700:
            return 'grph.18t', 600, 'HTGR operating temperature'
        elif temperature_K < 900:
            return 'grph.22t', 800, 'High-temperature HTGR'
        elif temperature_K < 1100:
            return 'grph.24t', 1000, 'VHTR operating'
        elif temperature_K < 1400:
            return 'grph.26t', 1200, 'VHTR accident conditions'
        elif temperature_K < 1800:
            return 'grph.28t', 1600, 'Severe accident'
        else:
            return 'grph.30t', 2000, 'Extreme accident conditions'

    elif material_type == 'water':
        if temperature_K < 310:
            return 'lwtr.10t', 294, 'Room temperature'
        elif temperature_K < 337:
            return 'lwtr.11t', 325, 'PWR cold leg (~52°C)'
        elif temperature_K < 375:
            return 'lwtr.13t', 350, 'PWR average (~77°C)'
        elif temperature_K < 450:
            return 'lwtr.14t', 400, 'PWR hot leg (~127°C)'
        elif temperature_K < 650:
            return 'lwtr.16t', 500, 'Supercritical water'
        else:
            return 'lwtr.20t', 800, 'Steam conditions'

    elif material_type == 'heavy_water':
        if temperature_K < 310:
            return 'hwtr.10t', 294, 'Room temperature'
        else:
            return 'hwtr.11t', 325, 'CANDU operating (~52°C)'

    elif material_type == 'polyethylene':
        return 'poly.10t', 296, 'Room temperature (shielding)'

    elif material_type == 'beryllium':
        return 'be.01t', 296, 'Room temperature'

    else:
        raise ValueError(f"Unknown material type: {material_type}")
```

**Example Usage**:
```python
# HTGR graphite at 600K
lib, temp, desc = select_thermal_library('graphite', 600)
print(f"Use {lib} ({temp}K) - {desc}")
# Output: Use grph.18t (600K) - HTGR operating temperature

# PWR water at 350K
lib, temp, desc = select_thermal_library('water', 350)
print(f"Use {lib} ({temp}K) - {desc}")
# Output: Use lwtr.13t (350K) - PWR average (~77°C)
```

### Requirement 3: Cross-Section Library Consistency Checker

**Functionality**:
```python
def check_library_consistency(materials):
    """
    Check for mixed ENDF library versions

    Returns warnings if inconsistent versions found
    """
    library_versions = {}  # {version: [materials]}

    for mat_id, isotopes in materials.items():
        for zaid, fraction in isotopes.items():
            # Extract library version (e.g., '.80c' → '80')
            parts = zaid.split('.')
            if len(parts) == 2:
                lib_version = parts[1].rstrip('cpuet')  # Remove type suffix

                if lib_version not in library_versions:
                    library_versions[lib_version] = []
                library_versions[lib_version].append((mat_id, zaid))

    warnings = []

    if len(library_versions) > 1:
        warnings.append({
            'type': 'MIXED_LIBRARY_VERSIONS',
            'severity': 'WARNING',
            'details': f'Found {len(library_versions)} different ENDF versions',
            'versions': {v: len(mats) for v, mats in library_versions.items()},
            'recommendation': 'Standardize to ENDF/B-VIII.0 (.80c) or ENDF/B-VII.0 (.70c)',
            'impact': 'May cause inconsistencies in cross-section data'
        })

        # Identify which materials have which versions
        for version, materials_list in library_versions.items():
            warnings.append({
                'type': 'LIBRARY_VERSION_DETAIL',
                'version': version,
                'endf_name': get_endf_name(version),
                'count': len(materials_list),
                'materials': list(set(m[0] for m in materials_list))
            })

    return warnings

def get_endf_name(version):
    """Convert library number to ENDF name"""
    mapping = {
        '00': 'ENDF/B-VI.0',
        '50': 'ENDF/B-V',
        '60': 'ENDF/B-VI.8',
        '70': 'ENDF/B-VII.0',
        '71': 'ENDF/B-VII.1',
        '80': 'ENDF/B-VIII.0',
        '20': 'Special (B-10 optimized)',
        '55': 'Special (W)',
    }
    return mapping.get(version, f'Unknown ({version})')
```

**Example Output**:
```
WARNINGS:
⚠ Mixed ENDF library versions detected
  - Found 4 different versions:
    * ENDF/B-VIII.0 (.80c): 12 materials
    * ENDF/B-VII.0 (.70c): 210 materials
    * ENDF/B-VI.0 (.00c): 120 materials
    * ENDF/B-V (.50c): 30 materials

  Recommendation: Standardize to ENDF/B-VIII.0 (.80c) for all materials
  Impact: Inconsistent cross-section data may affect results

  Details:
    ENDF/B-VIII.0: Materials m8900 (Air)
    ENDF/B-VII.0: Materials m2106-m2315 (ATR fuel)
    ENDF/B-VI.0: Materials m9000-m9036 (SS316L)
    ENDF/B-V: Materials m38, m30 (Structural)
```

### Requirement 4: Energy Cutoff Verification Enhancement

**Current**: Basic guidance exists
**Enhancement**: Systematic checking with problem-type awareness

**Functionality**:
```python
def validate_energy_cutoffs(mode, phys_cards, cut_cards, problem_type):
    """
    Validate energy cutoffs appropriate for problem type

    Args:
        mode: MODE card particle list
        phys_cards: PHYS:X cards
        cut_cards: CUT:X cards
        problem_type: 'thermal_reactor', 'fast_reactor', 'shielding', 'fusion', etc.
    """
    warnings = []

    if 'N' in mode:
        # Check neutron cutoff
        neutron_cutoff = cut_cards.get('N', {}).get('lower', 0.0)  # Default 0.0 MeV

        if problem_type == 'thermal_reactor':
            if neutron_cutoff > 1e-8:  # 0.01 eV
                warnings.append({
                    'type': 'NEUTRON_CUTOFF_TOO_HIGH',
                    'severity': 'WARNING',
                    'current': neutron_cutoff,
                    'recommended': 0.0,
                    'message': 'Thermal reactor should use default neutron cutoff (0.0 MeV)',
                    'impact': 'May miss important thermal neutron interactions'
                })

    if 'P' in mode:
        # Check photon cutoff
        photon_cutoff = cut_cards.get('P', {}).get('lower', 0.001)  # Default 1 keV

        if problem_type == 'thermal_reactor':
            if photon_cutoff > 0.0001:  # 100 eV
                warnings.append({
                    'type': 'PHOTON_CUTOFF_MAY_BE_HIGH',
                    'severity': 'INFO',
                    'current': photon_cutoff,
                    'recommended': 0.0001,
                    'message': 'Consider lower photon cutoff for thermal reactor (100 eV)',
                    'impact': 'More accurate but slower calculation',
                    'optional': True
                })

    # Check emax covers source energy
    if 'N' in mode and 'PHYS:N' in phys_cards:
        emax = phys_cards['PHYS:N'].get('emax', 100.0)
        source_energy = get_max_source_energy()  # Parse SDEF/KCODE

        if source_energy > emax:
            warnings.append({
                'type': 'SOURCE_EXCEEDS_EMAX',
                'severity': 'ERROR',
                'source_energy': source_energy,
                'emax': emax,
                'message': f'Source energy {source_energy} MeV exceeds PHYS:N emax {emax} MeV',
                'fix': f'Increase PHYS:N emax to at least {source_energy * 1.1} MeV'
            })

    return warnings
```

### Requirement 5: Physics Card Consistency Enhanced Validation

**Functionality**:
```python
def validate_physics_consistency(mode, phys_cards):
    """
    Validate MODE and PHYS cards are consistent
    """
    errors = []

    # Check MODE vs PHYS consistency
    if 'N' in mode and 'P' in mode:
        # Neutron-photon coupling
        phys_n = phys_cards.get('PHYS:N', {})
        ngam = phys_n.get('ngam', 1)  # Default 1 = photon production

        if ngam == 0:
            errors.append({
                'type': 'INCONSISTENT_PHOTON_PRODUCTION',
                'severity': 'ERROR',
                'message': 'MODE N P but PHYS:N ngam=0 (no photon production)',
                'fix': 'Remove ngam=0 entry or change to ngam=1',
                'impact': 'Photons will not be produced despite MODE P'
            })

    if 'P' in mode and 'E' in mode:
        # Photon-electron coupling
        phys_p = phys_cards.get('PHYS:P', {})
        ides = phys_p.get('ides', 0)  # Default 0 = electron production

        if ides == 1:
            errors.append({
                'type': 'INCONSISTENT_ELECTRON_PRODUCTION',
                'severity': 'ERROR',
                'message': 'MODE P E but PHYS:P ides=1 (no electron production)',
                'fix': 'Remove ides=1 entry or change to ides=0',
                'impact': 'Electrons will not be produced despite MODE E'
            })

    # Check for photonuclear if needed
    if 'P' in mode and 'N' in mode:
        phys_p = phys_cards.get('PHYS:P', {})
        ispn = phys_p.get('ispn', 0)  # Default 0 = no photoneutrons

        # Check for beryllium or deuterium
        has_be_or_d = check_materials_for_photonuclear_targets()

        if has_be_or_d and ispn == 0:
            errors.append({
                'type': 'PHOTONUCLEAR_NOT_ENABLED',
                'severity': 'WARNING',
                'message': 'Beryllium/deuterium present but photonuclear (ispn) not enabled',
                'fix': 'Add PHYS:P with ispn=1 if photoneutron production important',
                'impact': 'Photo-neutron reactions (γ,n) will not be simulated',
                'optional': True
            })

    return errors
```

---

## FILES TO MODIFY/CREATE

### 1. Update SKILL.md

**File**: `/home/user/mcnp-skills/.claude/skills/mcnp-physics-validator/SKILL.md`

**ADD new section after line 411 (after "Thermal Scattering (MT Card)" section)**:

```markdown
## CRITICAL: Systematic Thermal Scattering Validation

### Materials Requiring S(α,β) Treatment

**MCNP uses free gas scattering by default** - this is WRONG for thermal systems!

**ALWAYS require MT cards for**:
1. ✅ **Graphite** (C) - ANY reactor with graphite (HTGR, RBMK, fast reactor reflectors)
2. ✅ **Light water** (H₂O) - PWR, BWR, research reactors, pools
3. ✅ **Heavy water** (D₂O) - CANDU, research reactors
4. ✅ **Polyethylene** (CH₂) - Shielding, neutron sources
5. ✅ **Beryllium metal** (Be) - Reflectors, moderators
6. ✅ **Beryllium oxide** (BeO) - Reflectors

### Temperature-Dependent Library Selection

**CRITICAL**: S(α,β) libraries are temperature-dependent!

**Graphite Libraries**:
```mcnp
c Cold critical (room temperature)
mt1 grph.10t  $ 296K

c HTGR operating conditions
mt1 grph.18t  $ 600K ← MOST COMMON

c High-temperature HTGR
mt1 grph.22t  $ 800K
mt1 grph.24t  $ 1000K

c VHTR conditions
mt1 grph.26t  $ 1200K

c Accident conditions
mt1 grph.28t  $ 1600K
mt1 grph.30t  $ 2000K
```

**Water Libraries**:
```mcnp
c Room temperature (cold critical)
mt2 lwtr.10t  $ 294K

c PWR operating
mt2 lwtr.11t  $ 325K (cold leg ~52°C)
mt2 lwtr.13t  $ 350K (average ~77°C) ← COMMON
mt2 lwtr.14t  $ 400K (hot leg ~127°C)

c Supercritical / BWR
mt2 lwtr.16t  $ 500K
mt2 lwtr.20t  $ 800K (steam)
```

**Selection Rule**: Use library closest to actual operating temperature!

### Validation Procedure

**Step 1**: Identify all materials with moderator/reflector isotopes:
```python
for material in materials:
    has_carbon = check_for_isotopes(material, ['6000', '6012', '6013'])
    has_hydrogen = check_for_isotopes(material, ['1001'])
    has_deuterium = check_for_isotopes(material, ['1002'])
    has_beryllium = check_for_isotopes(material, ['4009'])
    has_oxygen = check_for_isotopes(material, ['8016'])
```

**Step 2**: Check for MT cards:
```python
if has_carbon and MODE includes 'N':
    if no MT card with 'grph':
        ERROR: "CRITICAL - Missing graphite thermal scattering"
        Impact: "Wrong thermal spectrum, reactivity error 1000-5000 pcm"
        Fix: "Add mt{material_id} grph.18t (or appropriate temperature)"

if has_hydrogen and has_oxygen:
    if no MT card with 'lwtr':
        ERROR: "CRITICAL - Missing water thermal scattering"
        Impact: "Inaccurate thermal neutron treatment"
        Fix: "Add mt{material_id} lwtr.13t (or appropriate temperature)"
```

**Step 3**: Verify temperature appropriateness:
```python
if MT card has 'grph.10t' but operating_temp > 400K:
    WARNING: "Using room-temperature graphite S(α,β) at elevated temperature"
    Recommendation: "Use grph.18t (600K) or higher temperature library"
```

### Example: HTGR Fuel Compact Validation

**TRISO particle with 5 carbon layers**:
```mcnp
c Kernel (UCO fuel)
m1  $ No MT needed (fuel, not moderator)
   92235.00c  0.20
   92238.00c  0.80
    6012.00c  0.32
    8016.00c  1.36

c Buffer (porous carbon)
m2
    6012.00c  0.989
    6013.00c  0.011
mt2 grph.18t  ← REQUIRED! (600K operating)

c IPyC (Inner Pyrolytic Carbon)
m3
    6012.00c  0.989
    6013.00c  0.011
mt3 grph.18t  ← REQUIRED!

c SiC (Silicon Carbide)
m4  $ No MT needed (ceramic, not thermal scatterer)
   14028.00c  0.50
    6012.00c  0.50

c OPyC (Outer Pyrolytic Carbon)
m5
    6012.00c  0.989
    6013.00c  0.011
mt5 grph.18t  ← REQUIRED!

c Matrix (Graphite)
m6
    6012.00c  0.989
    6013.00c  0.011
mt6 grph.18t  ← REQUIRED!
```

**Validation**:
- ✅ Materials 2, 3, 5, 6 (carbon layers) have MT cards
- ✅ All use grph.18t (600K) for HTGR operating conditions
- ✅ Material 1 (kernel) doesn't need MT (fuel)
- ✅ Material 4 (SiC) doesn't need MT (ceramic)

### Common Mistakes

**Mistake 1**: Missing graphite S(α,β) entirely
```mcnp
c WRONG - NO MT CARD!
m1
    6012.00c  0.989
    6013.00c  0.011
c ❌ Missing: mt1 grph.18t
```

**Mistake 2**: Wrong temperature library
```mcnp
c WRONG - Room temp library for 600K operating reactor!
m1
    6012.00c  0.989
    6013.00c  0.011
mt1 grph.10t  ← Should be grph.18t for HTGR!
```

**Mistake 3**: Water without S(α,β)
```mcnp
c WRONG - NO MT CARD FOR WATER!
m2
    1001.70c  2.0
    8016.70c  1.0
c ❌ Missing: mt2 lwtr.13t
```

**Mistake 4**: Mixed Be + H₂O missing one S(α,β)
```mcnp
c WRONG - ONLY water S(α,β), missing beryllium!
m3
    1001.70c  0.01
    8016.70c  0.005
    4009.60c  0.98
mt3 lwtr.10t  ← INCOMPLETE! Need: mt3 lwtr.10t be.01t
```

### Impact Summary

| Missing MT Card | Reactivity Error | Spectrum Error | Flux Error |
|-----------------|------------------|----------------|------------|
| Graphite | 1000-5000 pcm | Hardened | 10-20% |
| Water | 500-2000 pcm | Hardened | 5-15% |
| Heavy water | 800-3000 pcm | Hardened | 10-25% |
| Beryllium | 200-1000 pcm | Slight | 2-10% |

**Conclusion**: Missing MT cards are **NOT optional warnings** - they are **CRITICAL ERRORS** that invalidate results!

### Validation Checklist

Before running any thermal neutron calculation:

- [ ] Identified all materials with C, H, D, Be
- [ ] Verified MT cards present for ALL moderator/reflector materials
- [ ] Checked MT library temperature matches operating conditions
- [ ] Confirmed grph.XXt for ALL graphite materials (not just some)
- [ ] Verified lwtr.XXt or hwtr.XXt for ALL water materials
- [ ] Checked for dual S(α,β) (e.g., Be + H₂O needs BOTH be.01t and lwtr.XXt)
- [ ] Reviewed MCNP output for "free gas scattering" warnings

**Remember**: MCNP will run without MT cards but results will be WRONG!
```

### 2. Create Comprehensive Validation Script

**File**: `/home/user/mcnp-skills/.claude/skills/mcnp-physics-validator/scripts/thermal_scattering_validator.py`

```python
"""
Comprehensive Thermal Scattering Validator for MCNP
Detects missing S(α,β) cards - CRITICAL for thermal systems
"""

import re
from typing import Dict, List, Tuple, Optional

class ThermalScatteringValidator:
    """Validate thermal scattering (MT) cards in MCNP inputs"""

    # Temperature ranges for library selection
    GRAPHITE_TEMPS = {
        'grph.10t': (0, 400, 296, 'Room temperature (cold critical)'),
        'grph.18t': (400, 700, 600, 'HTGR operating (most common)'),
        'grph.22t': (700, 900, 800, 'High-temperature HTGR'),
        'grph.24t': (900, 1100, 1000, 'VHTR operating'),
        'grph.26t': (1100, 1400, 1200, 'VHTR accident'),
        'grph.28t': (1400, 1800, 1600, 'Severe accident'),
        'grph.30t': (1800, 3000, 2000, 'Extreme accident'),
    }

    WATER_TEMPS = {
        'lwtr.10t': (0, 310, 294, 'Room temperature'),
        'lwtr.11t': (310, 337, 325, 'PWR cold leg (~52°C)'),
        'lwtr.13t': (337, 375, 350, 'PWR average (~77°C)'),
        'lwtr.14t': (375, 450, 400, 'PWR hot leg (~127°C)'),
        'lwtr.16t': (450, 650, 500, 'Supercritical water'),
        'lwtr.20t': (650, 1000, 800, 'Steam/BWR'),
    }

    HEAVY_WATER_TEMPS = {
        'hwtr.10t': (0, 310, 294, 'Room temperature'),
        'hwtr.11t': (310, 400, 325, 'CANDU operating (~52°C)'),
    }

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self, materials: Dict, mt_cards: Dict, mode: str,
                 operating_temp: Optional[float] = None) -> Dict:
        """
        Main validation method

        Args:
            materials: {mat_id: {zaid: fraction}}
            mt_cards: {mat_id: [library1, library2, ...]}
            mode: MODE card string (e.g., 'N P')
            operating_temp: Operating temperature in Kelvin (optional)

        Returns:
            {'errors': [...], 'warnings': [...], 'info': [...]}
        """
        self.errors = []
        self.warnings = []
        self.info = []

        if 'N' not in mode.upper():
            self.info.append({
                'type': 'NO_NEUTRON_TRANSPORT',
                'message': 'MODE does not include neutrons - thermal scattering not needed'
            })
            return self._format_results()

        for mat_id, composition in materials.items():
            self._validate_material(mat_id, composition, mt_cards.get(mat_id, []),
                                   operating_temp)

        return self._format_results()

    def _validate_material(self, mat_id: str, composition: Dict,
                          mt_libs: List[str], operating_temp: Optional[float]):
        """Validate single material"""

        # Detect material type
        has_carbon = self._has_isotope(composition, ['6000', '6012', '6013'])
        has_hydrogen = self._has_isotope(composition, ['1001'])
        has_deuterium = self._has_isotope(composition, ['1002'])
        has_oxygen = self._has_isotope(composition, ['8016', '8017', '8018'])
        has_beryllium = self._has_isotope(composition, ['4009'])

        # Check graphite
        if has_carbon:
            self._check_graphite(mat_id, mt_libs, operating_temp)

        # Check light water
        if has_hydrogen and has_oxygen and not has_deuterium:
            self._check_water(mat_id, mt_libs, operating_temp)

        # Check heavy water
        if has_deuterium and has_oxygen:
            self._check_heavy_water(mat_id, mt_libs, operating_temp)

        # Check beryllium
        if has_beryllium:
            self._check_beryllium(mat_id, mt_libs)

        # Check polyethylene (C + H)
        if has_carbon and has_hydrogen and not has_oxygen:
            self._check_polyethylene(mat_id, mt_libs)

    def _check_graphite(self, mat_id: str, mt_libs: List[str],
                       operating_temp: Optional[float]):
        """Validate graphite thermal scattering"""

        has_grph = any('grph' in lib.lower() for lib in mt_libs)

        if not has_grph:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_GRAPHITE_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} contains graphite but NO MT card with grph.XXt',
                'impact': 'Wrong thermal neutron spectrum, reactivity error 1000-5000 pcm',
                'fix': f'Add "mt{mat_id} grph.18t" (or appropriate temperature library)',
                'reference': 'AGR1_Material_Card_Analysis.md, lines 566-594'
            })
        elif operating_temp:
            # Check if temperature is appropriate
            current_lib = [lib for lib in mt_libs if 'grph' in lib.lower()][0]
            recommended = self._select_graphite_library(operating_temp)

            if current_lib != recommended:
                self.warnings.append({
                    'material': mat_id,
                    'type': 'SUBOPTIMAL_GRAPHITE_TEMPERATURE',
                    'severity': 'WARNING',
                    'current_library': current_lib,
                    'recommended_library': recommended,
                    'operating_temp': operating_temp,
                    'message': f'Material m{mat_id} uses {current_lib} but operating temp is {operating_temp}K',
                    'recommendation': f'Consider changing to {recommended} for better accuracy'
                })

    def _check_water(self, mat_id: str, mt_libs: List[str],
                    operating_temp: Optional[float]):
        """Validate light water thermal scattering"""

        has_lwtr = any('lwtr' in lib.lower() for lib in mt_libs)

        if not has_lwtr:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_WATER_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} is light water but NO MT card with lwtr.XXt',
                'impact': 'Inaccurate thermal neutron treatment, reactivity error 500-2000 pcm',
                'fix': f'Add "mt{mat_id} lwtr.13t" (or appropriate temperature library)',
                'reference': 'AGR1_Material_Card_Analysis.md, lines 513-541'
            })
        elif operating_temp:
            current_lib = [lib for lib in mt_libs if 'lwtr' in lib.lower()][0]
            recommended = self._select_water_library(operating_temp)

            if current_lib != recommended:
                self.warnings.append({
                    'material': mat_id,
                    'type': 'SUBOPTIMAL_WATER_TEMPERATURE',
                    'severity': 'WARNING',
                    'current_library': current_lib,
                    'recommended_library': recommended,
                    'operating_temp': operating_temp,
                    'message': f'Material m{mat_id} uses {current_lib} but operating temp is {operating_temp}K'
                })

    def _check_heavy_water(self, mat_id: str, mt_libs: List[str],
                          operating_temp: Optional[float]):
        """Validate heavy water thermal scattering"""

        has_hwtr = any('hwtr' in lib.lower() for lib in mt_libs)

        if not has_hwtr:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_HEAVY_WATER_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} is heavy water but NO MT card with hwtr.XXt',
                'impact': 'Wrong D2O physics, reactivity error 800-3000 pcm',
                'fix': f'Add "mt{mat_id} hwtr.11t"'
            })

    def _check_beryllium(self, mat_id: str, mt_libs: List[str]):
        """Validate beryllium thermal scattering"""

        has_be = any('be.' in lib.lower() for lib in mt_libs)

        if not has_be:
            self.errors.append({
                'material': mat_id,
                'type': 'MISSING_BERYLLIUM_THERMAL_SCATTERING',
                'severity': 'CRITICAL',
                'message': f'Material m{mat_id} contains beryllium but NO MT card with be.01t',
                'impact': 'Wrong reflector physics, reactivity error 200-1000 pcm',
                'fix': f'Add "mt{mat_id} be.01t"',
                'note': 'If mixed with H2O, need BOTH: mt{mat_id} lwtr.XXt be.01t'
            })

    def _check_polyethylene(self, mat_id: str, mt_libs: List[str]):
        """Validate polyethylene thermal scattering"""

        has_poly = any('poly' in lib.lower() for lib in mt_libs)

        if not has_poly:
            self.warnings.append({
                'material': mat_id,
                'type': 'MISSING_POLYETHYLENE_THERMAL_SCATTERING',
                'severity': 'WARNING',
                'message': f'Material m{mat_id} appears to be polyethylene but NO MT card with poly.XXt',
                'recommendation': f'Add "mt{mat_id} poly.10t" for better accuracy',
                'impact': 'Moderate accuracy loss in shielding calculations'
            })

    def _select_graphite_library(self, temp_K: float) -> str:
        """Select appropriate graphite library for temperature"""
        for lib, (t_min, t_max, t_nominal, desc) in self.GRAPHITE_TEMPS.items():
            if t_min <= temp_K < t_max:
                return lib
        return 'grph.30t'  # Highest available

    def _select_water_library(self, temp_K: float) -> str:
        """Select appropriate water library for temperature"""
        for lib, (t_min, t_max, t_nominal, desc) in self.WATER_TEMPS.items():
            if t_min <= temp_K < t_max:
                return lib
        return 'lwtr.20t'  # Highest available

    def _has_isotope(self, composition: Dict, zaids: List[str]) -> bool:
        """Check if material contains any of the specified ZAIDs"""
        for zaid_pattern in zaids:
            for zaid in composition.keys():
                if zaid.startswith(zaid_pattern):
                    return True
        return False

    def _format_results(self) -> Dict:
        """Format validation results"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'summary': {
                'critical_errors': len(self.errors),
                'warnings': len(self.warnings),
                'passed': len(self.errors) == 0
            }
        }


# Example usage
if __name__ == "__main__":
    validator = ThermalScatteringValidator()

    # Test 1: Missing graphite MT card (CRITICAL ERROR)
    print("=" * 60)
    print("Test 1: Missing Graphite Thermal Scattering (AGR-1 Pattern)")
    print("=" * 60)
    materials = {
        '9040': {  # Graphite spacer
            '6012.00c': 0.989,
            '6013.00c': 0.011
        }
    }
    mt_cards = {}  # NO MT CARD!

    result = validator.validate(materials, mt_cards, 'N', operating_temp=600)
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   Material: m{err['material']}")
            print(f"   Message: {err['message']}")
            print(f"   Impact: {err['impact']}")
            print(f"   Fix: {err['fix']}")

    # Test 2: Correct graphite with MT card
    print("\n" + "=" * 60)
    print("Test 2: Correct Graphite with MT Card")
    print("=" * 60)
    materials = {
        '9040': {
            '6012.00c': 0.989,
            '6013.00c': 0.011
        }
    }
    mt_cards = {'9040': ['grph.18t']}  # CORRECT!

    result = validator.validate(materials, mt_cards, 'N', operating_temp=600)
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    print(f"Passed: {result['summary']['passed']}")

    # Test 3: Wrong temperature library
    print("\n" + "=" * 60)
    print("Test 3: Suboptimal Temperature Library")
    print("=" * 60)
    materials = {
        '9040': {
            '6012.00c': 0.989,
            '6013.00c': 0.011
        }
    }
    mt_cards = {'9040': ['grph.10t']}  # Room temp for 600K reactor!

    result = validator.validate(materials, mt_cards, 'N', operating_temp=600)
    print(f"\nWarnings: {result['summary']['warnings']}")
    if result['warnings']:
        for warn in result['warnings']:
            print(f"\n⚠ {warn['type']}")
            print(f"   Current: {warn['current_library']}")
            print(f"   Recommended: {warn['recommended_library']}")
            print(f"   Operating Temp: {warn['operating_temp']}K")

    # Test 4: Mixed Be + H2O (needs BOTH)
    print("\n" + "=" * 60)
    print("Test 4: Mixed Beryllium + Water")
    print("=" * 60)
    materials = {
        '14': {
            '1001.70c': 0.01,
            '8016.70c': 0.005,
            '4009.60c': 0.98
        }
    }
    mt_cards = {'14': ['lwtr.10t']}  # Missing be.01t!

    result = validator.validate(materials, mt_cards, 'N')
    print(f"\nCritical Errors: {result['summary']['critical_errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   {err['message']}")
            print(f"   Fix: {err['fix']}")
            if 'note' in err:
                print(f"   Note: {err['note']}")
```

### 3. Create Reference Guide

**File**: `/home/user/mcnp-skills/.claude/skills/mcnp-physics-validator/thermal_scattering_complete_guide.md`

```markdown
# Complete Thermal Scattering Reference Guide

## Overview

This guide provides comprehensive information on S(α,β) thermal scattering libraries in MCNP, based on analysis of production HTGR reactor models and MCNP best practices.

---

## Why Thermal Scattering Matters

**Free gas scattering** (MCNP default): Assumes atoms are free, independent particles
**Thermal scattering** (with MT card): Accounts for chemical binding, crystal structure, molecular motion

**Impact of missing MT cards**:
| Material | Reactivity Error | Spectrum Error | Typical Application |
|----------|------------------|----------------|---------------------|
| Graphite | 1000-5000 pcm | 10-20% | HTGR, RBMK, fast reactor reflectors |
| Light water | 500-2000 pcm | 5-15% | PWR, BWR, research reactors |
| Heavy water | 800-3000 pcm | 10-25% | CANDU, research reactors |
| Beryllium | 200-1000 pcm | 2-10% | Reflectors, test reactors |
| Polyethylene | 100-500 pcm | 2-5% | Neutron shielding |

**Conclusion**: Missing MT cards invalidate thermal neutron results!

---

## Graphite Thermal Scattering

### Available Libraries

| Library | Temperature | Application |
|---------|-------------|-------------|
| grph.10t | 296K (23°C) | Cold critical experiments, zero-power tests |
| grph.18t | 600K (327°C) | **HTGR operating (most common)**, some fast reactors |
| grph.22t | 800K (527°C) | High-temperature HTGR designs |
| grph.24t | 1000K (727°C) | VHTR (Very High Temperature Reactor) operating |
| grph.26t | 1200K (927°C) | VHTR accident scenarios |
| grph.28t | 1600K (1327°C) | Severe accident conditions |
| grph.30t | 2000K (1727°C) | Extreme accident analysis |

### Selection Guide

```python
def select_graphite_library(temperature_K):
    if temperature_K < 400:
        return 'grph.10t'  # Room temperature
    elif temperature_K < 700:
        return 'grph.18t'  # HTGR operating - MOST COMMON
    elif temperature_K < 900:
        return 'grph.22t'  # High-temp HTGR
    elif temperature_K < 1100:
        return 'grph.24t'  # VHTR
    elif temperature_K < 1400:
        return 'grph.26t'  # VHTR accident
    elif temperature_K < 1800:
        return 'grph.28t'  # Severe accident
    else:
        return 'grph.30t'  # Extreme conditions
```

### Examples

**HTGR operating at 600K**:
```mcnp
m1  $ Graphite moderator/reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ 600K - CORRECT for HTGR
```

**TRISO particle buffer layer** (600K):
```mcnp
m2  $ Porous carbon buffer
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ REQUIRED even for particle coating!
```

**Cold critical experiment**:
```mcnp
m3  $ Graphite at room temperature
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.10t  $ 296K - CORRECT for cold critical
```

---

## Light Water Thermal Scattering

### Available Libraries

| Library | Temperature | Application |
|---------|-------------|-------------|
| lwtr.10t | 294K (21°C) | Room temperature, cold critical |
| lwtr.11t | 325K (52°C) | **PWR cold leg, common operating** |
| lwtr.13t | 350K (77°C) | **PWR average, most common** |
| lwtr.14t | 400K (127°C) | PWR hot leg |
| lwtr.16t | 500K (227°C) | Supercritical water reactor |
| lwtr.20t | 800K (527°C) | Steam conditions, BWR |

### Selection Guide

```python
def select_water_library(temperature_K):
    if temperature_K < 310:
        return 'lwtr.10t'  # Room temperature
    elif temperature_K < 337:
        return 'lwtr.11t'  # PWR cold leg
    elif temperature_K < 375:
        return 'lwtr.13t'  # PWR average - MOST COMMON
    elif temperature_K < 450:
        return 'lwtr.14t'  # PWR hot leg
    elif temperature_K < 650:
        return 'lwtr.16t'  # Supercritical
    else:
        return 'lwtr.20t'  # Steam
```

### Examples

**PWR at 350K average**:
```mcnp
m1  $ Light water moderator
    1001.70c  2.0
    8016.70c  1.0
mt1 lwtr.13t  $ 350K - CORRECT for PWR
```

**BWR steam regions**:
```mcnp
m2  $ Steam
    1001.70c  2.0
    8016.70c  1.0
mt2 lwtr.20t  $ 800K - High temperature
```

**Research reactor pool**:
```mcnp
m3  $ Water pool at room temperature
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.10t  $ 294K - Room temperature
```

---

## Heavy Water Thermal Scattering

### Available Libraries

| Library | Temperature | Application |
|---------|-------------|-------------|
| hwtr.10t | 294K (21°C) | Room temperature |
| hwtr.11t | 325K (52°C) | **CANDU operating (most common)** |

### Examples

**CANDU reactor**:
```mcnp
m1  $ Heavy water moderator
    1002.70c  2.0  $ Deuterium
    8016.70c  1.0
mt1 hwtr.11t  $ 325K - CANDU operating
```

---

## Beryllium Thermal Scattering

### Available Library

| Library | Temperature | Application |
|---------|-------------|-------------|
| be.01t | 296K | Beryllium metal reflectors, moderators |

### Examples

**Pure beryllium reflector**:
```mcnp
m1  $ Beryllium metal
    4009.60c  1.23621-1
mt1 be.01t  $ REQUIRED!
```

**Mixed beryllium + water** (DUAL S(α,β)):
```mcnp
m2  $ Be + H2O mixture
    1001.70c  3.40940-3
    8016.70c  1.70470-3
    4009.60c  1.17316-1
mt2 lwtr.10t be.01t  $ BOTH required!
```

**Note**: For Be + H₂O, **BOTH** lwtr and be libraries must be specified!

---

## Polyethylene Thermal Scattering

### Available Library

| Library | Temperature | Application |
|---------|-------------|-------------|
| poly.10t | 296K | Polyethylene (CH₂)ₙ shielding |

### Examples

**Neutron shield**:
```mcnp
m1  $ Polyethylene
    1001.70c  0.667  $ Hydrogen
    6000.70c  0.333  $ Carbon
mt1 poly.10t  $ REQUIRED for shielding
```

---

## Validation Checklist

### Before Running Any Thermal Neutron Calculation:

#### 1. Identify Materials Requiring S(α,β)

- [ ] List all materials containing C (carbon/graphite)
- [ ] List all materials containing H (light water, polyethylene)
- [ ] List all materials containing D (heavy water)
- [ ] List all materials containing Be (beryllium)

#### 2. Check MT Cards Present

- [ ] Every graphite material has `mtX grph.XXt`
- [ ] Every water material has `mtX lwtr.XXt`
- [ ] Every D₂O material has `mtX hwtr.XXt`
- [ ] Every Be material has `mtX be.01t`
- [ ] Every polyethylene material has `mtX poly.XXt`

#### 3. Verify Temperature Appropriateness

- [ ] Graphite: grph.18t for 600K HTGR operating
- [ ] Water: lwtr.13t for 350K PWR average
- [ ] Room temp experiments: grph.10t, lwtr.10t

#### 4. Check for Mixed Materials

- [ ] Be + H₂O: Both `lwtr.XXt be.01t` specified
- [ ] No missing components in dual S(α,β)

#### 5. Review MCNP Output

- [ ] Check for "free gas scattering" warnings
- [ ] Verify MT libraries loaded correctly
- [ ] Look for missing data warnings

### Common Mistakes to Avoid

❌ **Missing graphite MT card entirely** (1000-5000 pcm error!)
❌ **Room temp library for operating reactor** (grph.10t for 600K reactor)
❌ **Water without MT card** (500-2000 pcm error!)
❌ **Mixed Be + H₂O with only one S(α,β)** (incomplete physics)
❌ **Assuming MCNP will warn** (it runs without error but results are wrong!)

---

## Real-World Example: AGR-1 TRISO Fuel

**Problem Found**: AGR-1 model had ~50 graphite materials WITHOUT MT cards!

**Materials affected**:
- m9040-m9056: Graphite spacers ← Missing grph.18t
- m9070-m9075: Borated graphite holders ← Missing grph.18t
- m9090: Buffer layer (porous carbon) ← Missing grph.18t
- m9091: IPyC (dense carbon) ← Missing grph.18t
- m9093: OPyC (dense carbon) ← Missing grph.18t
- m9094: Matrix (graphite) ← Missing grph.18t

**Impact**:
- Wrong thermal neutron spectrum
- Reactivity error estimated 1000-5000 pcm
- Invalid benchmark comparisons

**Fix**:
```mcnp
mt9040 grph.18t  $ Graphite spacers
mt9070 grph.18t  $ Borated graphite holders
mt9071 grph.18t
mt9072 grph.18t
mt9073 grph.18t
mt9074 grph.18t
mt9075 grph.18t
mt9090 grph.18t  $ Buffer layer
mt9091 grph.18t  $ IPyC
mt9093 grph.18t  $ OPyC
mt9094 grph.18t  $ Matrix
```

**Lesson**: Even production models can have critical physics errors!

---

## Summary

**CRITICAL RULES**:

1. ✅ **ALWAYS use MT cards for C, H, D, Be** in thermal systems
2. ✅ **Match library temperature to operating conditions**
3. ✅ **Use BOTH S(α,β) for mixed materials** (Be + H₂O)
4. ✅ **Validate BEFORE running** - MCNP won't warn!
5. ✅ **Check output for "free gas" warnings**

**Remember**: Missing MT cards are **CRITICAL ERRORS**, not optional!

**Impact**: 1000-5000 pcm reactivity errors, wrong thermal spectrum, invalid results

**Fix**: Add appropriate MT cards for ALL moderator/reflector materials

---

**END OF GUIDE**
```

### 4. Create Example Input Files

**File**: `/home/user/mcnp-skills/.claude/skills/mcnp-physics-validator/example_inputs/htgr_physics_correct.i`

```mcnp
HTGR Physics Setup - CORRECT EXAMPLE
c Demonstrates proper thermal scattering for HTGR at 600K
c
c Cells
c
1 1 -1.8   -1  imp:n=1  $ Fuel compact (graphite fuel matrix)
2 2 -1.7    1 -2  imp:n=1  $ Graphite reflector
3 3 -5e-3   2 -3  imp:n=1  $ Helium coolant
4 0         3     imp:n=0  $ Void
c
c Surfaces
c
1 so  5.0   $ Fuel compact outer radius
2 so  20.0  $ Reflector outer radius
3 so  30.0  $ Problem boundary
c
c Materials
c
m1  $ Fuel compact - graphite fuel matrix
    6012.00c  0.9890
    6013.00c  0.0110
   92235.00c  0.001   $ Trace fuel
mt1 grph.18t  $ ← CRITICAL! 600K graphite S(α,β)
c
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ ← REQUIRED! Same temperature
c
m3  $ Helium coolant (no MT needed - monatomic gas)
    2004.00c  1.0
c
c Physics
c
mode n
phys:n 20 0 0 J J J J J 1  $ emax=20 MeV, ngam=1 (photon production)
c
c Source
kcode 10000 1.0 50 250
ksrc 0 0 0
```

**File**: `/home/user/mcnp-skills/.claude/skills/mcnp-physics-validator/example_inputs/htgr_physics_wrong.i`

```mcnp
HTGR Physics Setup - WRONG EXAMPLE (Common Mistakes)
c Demonstrates MISSING thermal scattering - DO NOT USE!
c
c Cells
c
1 1 -1.8   -1  imp:n=1  $ Fuel compact
2 2 -1.7    1 -2  imp:n=1  $ Graphite reflector
3 3 -5e-3   2 -3  imp:n=1  $ Helium coolant
4 0         3     imp:n=0  $ Void
c
c Surfaces
c
1 so  5.0
2 so  20.0
3 so  30.0
c
c Materials
c
m1  $ Fuel compact - graphite
    6012.00c  0.9890
    6013.00c  0.0110
   92235.00c  0.001
c ❌ ERROR: Missing mt1 grph.18t
c    Impact: Wrong thermal spectrum, 1000-5000 pcm reactivity error!
c
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
c ❌ ERROR: Missing mt2 grph.18t
c    Impact: Wrong reflector physics!
c
m3  $ Helium coolant
    2004.00c  1.0
c (OK - no MT needed for helium)
c
c Physics
mode n
phys:n 20 0 0 J J J J J 1
c
c Source
kcode 10000 1.0 50 250
ksrc 0 0 0
c
c VALIDATOR OUTPUT (Expected):
c
c ❌ CRITICAL ERROR: Material m1 contains graphite but NO MT card
c    Fix: Add "mt1 grph.18t"
c    Impact: Wrong thermal neutron spectrum, reactivity error 1000-5000 pcm
c
c ❌ CRITICAL ERROR: Material m2 contains graphite but NO MT card
c    Fix: Add "mt2 grph.18t"
c    Impact: Wrong reflector physics, reactivity error
```

**File**: `/home/user/mcnp-skills/.claude/skills/mcnp-physics-validator/example_inputs/pwr_physics_correct.i`

```mcnp
PWR Physics Setup - CORRECT EXAMPLE
c Demonstrates proper thermal scattering for PWR at 350K
c
c Cells
c
1 1 -10.2  -1      imp:n=1  $ UO2 fuel
2 2 -6.5    1 -2   imp:n=1  $ Zircaloy clad
3 3 -1.0    2 -3   imp:n=1  $ Water moderator
4 0         3      imp:n=0  $ Void
c
c Surfaces
c
1 cz  0.41  $ Fuel radius
2 cz  0.48  $ Clad outer radius
3 cz  2.0   $ Water boundary
c
c Materials
c
m1  $ UO2 fuel
   92235.70c  0.045  $ 4.5% enriched
   92238.70c  0.955
    8016.70c  2.0
c (No MT needed - fuel, not moderator)
c
m2  $ Zircaloy clad
   40000.60c  1.0
c (No MT needed - structural)
c
m3  $ Light water moderator
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t  $ ← CRITICAL! 350K water S(α,β) for PWR
c
c Physics
mode n p  $ Coupled neutron-photon
phys:n 20 0 0 J J J J J 1  $ Photon production enabled
phys:p 100
c
c Source
kcode 10000 1.0 50 250
ksrc 0 0 0
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Update Skill Documentation (1-2 hours)

- [ ] Update SKILL.md with comprehensive thermal scattering section
- [ ] Create thermal_scattering_complete_guide.md reference
- [ ] Add TRISO fuel physics validation patterns
- [ ] Document temperature-dependent library selection

### Phase 2: Create Validation Scripts (2-3 hours)

- [ ] Create thermal_scattering_validator.py
- [ ] Create library_consistency_checker.py
- [ ] Create temperature_library_selector.py
- [ ] Create energy_cutoff_validator.py (enhanced)
- [ ] Create physics_consistency_checker.py (enhanced)
- [ ] Test all scripts with AGR-1 example inputs

### Phase 3: Create Example Files (1 hour)

- [ ] htgr_physics_correct.i (working example)
- [ ] htgr_physics_wrong.i (common mistakes)
- [ ] pwr_physics_correct.i (PWR example)
- [ ] triso_fuel_physics.i (TRISO-specific)

### Phase 4: Integration Testing (1 hour)

- [ ] Test validator against AGR-1 inputs (should find ~50 missing MT cards)
- [ ] Test validator against correct inputs (should pass)
- [ ] Test temperature library selector with various temps
- [ ] Test library consistency checker with mixed versions

### Total Estimated Time: 5-7 hours

---

## SUCCESS CRITERIA

**Validator must**:
1. ✅ Detect ALL missing graphite MT cards (AGR-1 test: find all 50+)
2. ✅ Detect missing water MT cards
3. ✅ Detect missing beryllium MT cards
4. ✅ Warn on suboptimal temperature libraries
5. ✅ Flag mixed ENDF library versions
6. ✅ Validate MODE/PHYS consistency
7. ✅ Verify energy cutoffs appropriate for problem type
8. ✅ Return **ERRORS** not just warnings for missing MT cards

**User experience**:
1. ✅ Clear, actionable error messages
2. ✅ Specific fix recommendations (e.g., "Add mt1 grph.18t")
3. ✅ Physics impact explained (reactivity error magnitude)
4. ✅ Temperature library selector provides easy selection
5. ✅ Examples demonstrate correct and incorrect practices

**Documentation**:
1. ✅ Complete thermal scattering reference guide
2. ✅ Temperature-dependent library selection guide
3. ✅ TRISO fuel validation patterns documented
4. ✅ Real-world examples (AGR-1 case study)

---

## PRIORITY JUSTIFICATION

**Why CRITICAL Priority**:

1. **Missing MT cards cause 1000-5000 pcm reactivity errors** - invalidates all results
2. **Production models have this error** - AGR-1 model missing ~50 MT cards
3. **MCNP doesn't warn** - runs without error, produces wrong results
4. **Affects ALL thermal systems** - PWR, BWR, HTGR, RBMK, research reactors
5. **Easy to fix** - just add MT cards, but must be validated systematically

**Without this refinement**:
- Users will build models with missing MT cards
- Results will be wrong (1000s of pcm error)
- Benchmarks will fail
- Publications will be invalid
- Safety analyses will be incorrect

**With this refinement**:
- Validator catches ALL missing MT cards
- Users get specific fix instructions
- Temperature libraries correctly matched
- Results are physically correct
- Benchmarks validate successfully

---

## REFERENCES

**Analysis Documents**:
1. AGR1_Material_Card_Analysis.md - Lines 566-594 (missing graphite MT)
2. AGR1_Material_Card_Analysis.md - Lines 78-109 (library inconsistencies)
3. AGR1_Material_Card_Analysis.md - Lines 513-567 (thermal scattering patterns)
4. AGR1_Material_Card_Analysis.md - Lines 1180-1210 (temperature libraries)
5. HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md - Thermal scattering guidance
6. COMPREHENSIVE_FINDINGS_SYNTHESIS.md - Material validation requirements

**MCNP Manual Sections**:
- §5.6.2: MT Card (thermal scattering)
- §3.4.5: Warnings and limitations
- Table 4.3: Particle parameters
- §5.7: Physics cards

---

**END OF REFINEMENT PLAN**

This plan provides everything needed to implement comprehensive physics validation with emphasis on **CRITICAL** thermal scattering checking.
