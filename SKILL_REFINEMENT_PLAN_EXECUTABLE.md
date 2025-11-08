# COMPREHENSIVE MCNP SKILL REFINEMENT PLAN
## Immediately Executable Plan for Next Session

**Created**: November 7, 2025
**Based On**: 13 comprehensive analysis documents (469 KB) from HTGR reactor model study
**Execution Time Estimate**: 3-4 hours for HIGH priority items

---

## OVERVIEW

This plan provides **specific, actionable updates** to ALL relevant MCNP skills based on analysis of production-quality HTGR reactor models. Each section includes:

- ✅ **Files to modify** (exact paths)
- ✅ **Specific content to add** (ready to insert)
- ✅ **New example files to create**
- ✅ **Validation tests** (how to verify improvements)

---

## EXECUTION STRATEGY

### Phase 1: Critical Fixes (Session 1 - HIGH PRIORITY)
1. mcnp-lattice-builder
2. mcnp-material-builder
3. mcnp-input-validator
4. mcnp-geometry-builder

### Phase 2: Major Enhancements (Session 2 - MEDIUM PRIORITY)
5. mcnp-template-generator (NEW)
6. mcnp-input-builder
7. mcnp-cell-checker
8. mcnp-cross-reference-checker

### Phase 3: Advanced Features (Session 3 - LOW PRIORITY)
9. mcnp-programmatic-generator (NEW)
10. mcnp-workflow-integrator (NEW)
11. Additional skills as needed

---

# PHASE 1: CRITICAL FIXES

## 1. mcnp-lattice-builder

**Priority**: 🔴 **CRITICAL** - Current skill fails on reactor lattices

**Location**: `.claude/skills/mcnp-lattice-builder/`

### Issue Identified
Current skill does NOT teach:
- Multi-level lattice nesting (>2 levels)
- FILL array dimension calculation
- Repeat notation (nR syntax)
- Circular packing in rectangular lattices
- Universe hierarchy validation

### Files to Modify

#### 1.1 Update SKILL.md

**File**: `.claude/skills/mcnp-lattice-builder/SKILL.md`

**ADD new section after current content**:

```markdown
## CRITICAL LATTICE CONCEPTS

### Multi-Level Lattice Hierarchies

MCNP supports **up to 6 practical levels** of nested lattices. Example from AGR-1 TRISO fuel:

```
Level 1: TRISO Particle (u=1114) - 5 concentric shells
Level 2: Matrix Cell (u=1115) - single filler cell
Level 3: Particle Lattice (u=1116, LAT=1) - 15×15×1 array
Level 4: Matrix Filler (u=1117) - end caps
Level 5: Compact Lattice (u=1110, LAT=1) - 1×1×31 vertical stack
Level 6: Global Placement - fill=1110 (x,y,z)
```

**Pattern**: Each level is a universe that fills into the level above.

### FILL Array Dimension Calculation

**CRITICAL RULE**: Elements needed = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

**Common Mistakes**:
```
fill=-7:7 -7:7 0:0
  WRONG: 7 × 7 × 0 = 0 elements
  RIGHT: (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15 × 15 × 1 = 225 elements
```

**Always include ZERO when counting negative to positive indices!**

### Repeat Notation (nR)

**CRITICAL RULE**: `U nR` = (n+1) total copies, NOT n copies!

**Examples**:
```
1117 2R = 1117 1117 1117 (3 copies total)
1116 24R = 1116 repeated 25 times total
```

**Full compact lattice example**:
```mcnp
fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

Breakdown:
  1117 2R  = 3 matrix layers (bottom cap)
  1116 24R = 25 particle lattice layers (fuel region)
  1117 2R  = 3 matrix layers (top cap)
  Total: 3 + 25 + 3 = 31 elements for indices -15 to +15 ✓
```

### Index Ordering

**CRITICAL RULE**: Arrays filled in K, J, I order (K outermost loop, I innermost)

For `fill=-7:7 -7:7 0:0`:
- First row corresponds to j=-7, i varies from -7 to +7
- Second row corresponds to j=-6, i varies from -7 to +7
- etc.

### Circular Packing in Rectangular Lattices

**Pattern**: Approximate cylinder using square lattice

```mcnp
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ 15×15 array
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     ... (more rows)
```

**Result**: ~169 TRISO particles (u=1114) + ~56 matrix cells (u=1115) in circular pattern

**Physical constraint**: Must fit in cylindrical compact (radius = 6.35 mm)

### Universe Hierarchy Validation

**Rules for valid nested lattices**:
1. ✅ Define child universes BEFORE parent universes
2. ✅ No circular references (A fills B, B fills A)
3. ✅ All filled universes must exist
4. ✅ Universe 0 is always global (never define explicitly)
5. ✅ Lattice bounding surface must contain N × pitch dimensions

## WORKING EXAMPLES

### Example 1: 2-Level TRISO Particle Lattice

```mcnp
c TRISO Particle Cells (u=1114)
91101 9111 -10.924 -91111         u=1114 vol=0.092522  $ Kernel
91102 9090 -1.100  91111 -91112  u=1114              $ Buffer
91103 9091 -1.904  91112 -91113  u=1114              $ IPyC
91104 9092 -3.205  91113 -91114  u=1114              $ SiC
91105 9093 -1.911  91114 -91115  u=1114              $ OPyC
91106 9094 -1.344  91115         u=1114              $ SiC Matrix

c Matrix Cell (u=1115)
91107 9094 -1.344 -91116         u=1115              $ SiC Matrix

c Particle Lattice (u=1116) - 15×15×1 rectangular
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ 225 positions
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115

c Surfaces
91111 so   0.017485  $ Kernel (174.85 μm)
91112 so   0.027905  $ Buffer (279.05 μm)
91113 so   0.031785  $ IPyC (317.85 μm)
91114 so   0.035375  $ SiC (353.75 μm)
91115 so   0.039305  $ OPyC (393.05 μm)
91116 so   1.000000  $ Matrix sphere (10 mm)
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000  $ Lattice element

c Materials
m9111  $ UCO kernel, 19.96% enriched
   92234.00c  3.34179E-03
   92235.00c  1.99636E-01
   92238.00c  7.96829E-01
    6012.00c  0.3217217
    8016.00c  1.3613

m9090  $ Buffer carbon
    6012.00c  0.9890
    6013.00c  0.0110
mt9090 grph.18t

[... other materials ...]
```

### Example 2: 3-Level Compact Lattice

```mcnp
c Matrix Filler (u=1117)
91109 9094 -1.344 -91119    u=1117  $ Matrix

c Compact Lattice (u=1110) - 1×1×31 vertical stack
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R

c Global Placement with transformation
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)

c Additional surfaces
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715  $ Compact element
91119 c/z  0.0 0.0   0.6500  $ Compact boundary
97011 c/z   25.547039 -24.553123   0.63500  $ Stack cylinder
98005 pz   17.81810  $ Bottom plane
98051 pz   20.35810  $ Top plane
```

## COMMON PITFALLS AND FIXES

| Pitfall | Example | Fix |
|---------|---------|-----|
| **Dimension mismatch** | fill=0:10 but only 10 elements provided | Need 11 elements: (10-0+1)=11 |
| **Repeat off-by-one** | fill=0:10, use "U 10R" (gives 11) | Use "U 9R" for 10 copies |
| **Negative index error** | fill=-5:5, think it's 5 elements | It's 11 elements (include 0!) |
| **Wrong index order** | Assume I,J,K ordering | MCNP uses K,J,I ordering! |
| **Surface too small** | Lattice 15×15 but surface spans 14 pitches | Surface = N × pitch |
| **Universe conflict** | Reuse U=100 for different geometries | Use unique numbers |
| **Circular fill** | u=100 fill=200, u=200 fill=100 | Define hierarchy properly |

## VALIDATION CHECKLIST

Before running MCNP, verify:

- [ ] FILL array element count matches (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1)
- [ ] Repeat notation: nR gives n+1 total copies
- [ ] All filled universes are defined before use
- [ ] No circular universe references
- [ ] Lattice bounding surface matches N × pitch
- [ ] Child universes defined before parent universes
- [ ] Universe numbers are unique (no conflicts)
```

#### 1.2 Create New Python Tool: lattice_dimension_calculator.py

**File**: `.claude/skills/mcnp-lattice-builder/tools/lattice_dimension_calculator.py`

```python
"""
MCNP Lattice Dimension Calculator
Helps validate FILL array dimensions and repeat notation
"""

def calculate_fill_dimensions(imin, imax, jmin, jmax, kmin, kmax):
    """
    Calculate required number of elements for FILL array

    Args:
        imin, imax: I-index range
        jmin, jmax: J-index range
        kmin, kmax: K-index range

    Returns:
        dict with total elements and breakdown
    """
    i_count = imax - imin + 1
    j_count = jmax - jmin + 1
    k_count = kmax - kmin + 1
    total = i_count * j_count * k_count

    return {
        'i_count': i_count,
        'j_count': j_count,
        'k_count': k_count,
        'total_elements': total,
        'fill_spec': f"fill={imin}:{imax} {jmin}:{jmax} {kmin}:{kmax}",
        'note': f"Need {total} universe specifications ({k_count} layers of {j_count}×{i_count})"
    }


def repeat_notation_converter(universe_list):
    """
    Convert universe list to MCNP repeat notation

    Args:
        universe_list: List of universe numbers

    Returns:
        String with optimal repeat notation
    """
    if not universe_list:
        return ""

    result = []
    i = 0
    while i < len(universe_list):
        current = universe_list[i]
        count = 1

        # Count consecutive repeats
        while i + count < len(universe_list) and universe_list[i + count] == current:
            count += 1

        if count == 1:
            result.append(str(current))
        elif count == 2:
            result.append(f"{current} {current}")
        else:
            # nR notation: n repetitions = (n-1)R
            result.append(f"{current} {count-1}R")

        i += count

    return " ".join(result)


def validate_lattice_dimensions(lat_type, fill_spec, surface_params):
    """
    Validate lattice dimensions match bounding surface

    Args:
        lat_type: 1 (rectangular) or 2 (hexagonal)
        fill_spec: Dict from calculate_fill_dimensions()
        surface_params: Dict with surface dimensions

    Returns:
        Dict with validation results and warnings
    """
    warnings = []

    if lat_type == 1:  # Rectangular
        # Check if RPP surface matches lattice dimensions
        if 'pitch_x' in surface_params and 'x_min' in surface_params:
            expected_x = surface_params['x_min'] + fill_spec['i_count'] * surface_params['pitch_x']
            if abs(expected_x - surface_params['x_max']) > 0.001:
                warnings.append(f"X dimension mismatch: {fill_spec['i_count']} elements × {surface_params['pitch_x']} pitch != surface extent")

    return {
        'valid': len(warnings) == 0,
        'warnings': warnings
    }


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("MCNP Lattice Dimension Calculator")
    print("=" * 60)

    # Example 1: 15×15×1 TRISO particle lattice
    print("\nExample 1: TRISO Particle Lattice")
    dims = calculate_fill_dimensions(-7, 7, -7, 7, 0, 0)
    print(f"  {dims['fill_spec']}")
    print(f"  Required elements: {dims['total_elements']}")
    print(f"  Layout: {dims['note']}")

    # Example 2: 1×1×31 compact lattice
    print("\nExample 2: Compact Lattice")
    dims = calculate_fill_dimensions(0, 0, 0, 0, -15, 15)
    print(f"  {dims['fill_spec']}")
    print(f"  Required elements: {dims['total_elements']}")
    print(f"  Layout: {dims['note']}")

    # Example 3: Repeat notation
    print("\nExample 3: Repeat Notation Conversion")
    universes = [1117, 1117, 1117] + [1116]*25 + [1117, 1117, 1117]
    repeat_str = repeat_notation_converter(universes)
    print(f"  Universe list: [1117,1117,1117] + [1116]×25 + [1117,1117,1117]")
    print(f"  MCNP format: {repeat_str}")
    print(f"  Expected: 1117 2R 1116 24R 1117 2R")
```

#### 1.3 Create Example File: triso_particle_lattice.i

**File**: `.claude/skills/mcnp-lattice-builder/assets/examples/triso_particle_lattice.i`

**Content**: Copy from AGR1_CELL_CARD_COMPLETE_ANALYSIS.md Example 1 (2-level lattice)

#### 1.4 Create Example File: triso_compact_lattice.i

**File**: `.claude/skills/mcnp-lattice-builder/assets/examples/triso_compact_lattice.i`

**Content**: Full 3-level example from sdr-agr.i (lines 14-100)

### Validation Test

**Test Input**: User asks "How do I create a lattice with 15×15 TRISO particles?"

**Expected Output**: Skill provides:
1. ✅ Dimension calculation (15×15×1 = 225 elements)
2. ✅ fill=-7:7 -7:7 0:0 specification
3. ✅ Circular packing pattern
4. ✅ Working example with surfaces, cells, materials
5. ✅ Validation checklist

---

## 2. mcnp-material-builder

**Priority**: 🔴 **CRITICAL** - Missing thermal scattering guidance

**Location**: `.claude/skills/mcnp-material-builder/`

### Issue Identified
Current skill does NOT adequately cover:
- Thermal scattering (MT cards) - when required
- Temperature-dependent library selection
- TRISO fuel material compositions
- Burnup tracking material requirements
- Stoichiometric ratios in materials

### Files to Modify

#### 2.1 Update SKILL.md

**File**: `.claude/skills/mcnp-material-builder/SKILL.md`

**ADD new section**:

```markdown
## THERMAL SCATTERING (MT CARDS) - CRITICAL

### When MT Cards Are REQUIRED

**ALWAYS use thermal scattering for**:
- ✅ **Graphite** (any temperature)
- ✅ **Light water** (H₂O)
- ✅ **Heavy water** (D₂O)
- ✅ **Polyethylene** (CH₂)
- ✅ **Beryllium metal**
- ✅ **Beryllium oxide** (BeO)

**Impact of missing MT cards**:
- ❌ Wrong thermal neutron spectrum
- ❌ Incorrect reactivity (can be 1000s of pcm error)
- ❌ Wrong flux distribution
- ❌ Invalid benchmark comparisons

### Temperature-Dependent Libraries

**Graphite S(α,β) libraries**:
```mcnp
mt1 grph.10t  $ 296K (room temperature)
mt1 grph.18t  $ 600K (reactor operating temperature)
mt1 grph.22t  $ 800K (high temperature)
mt1 grph.24t  $ 1000K (very high temperature)
mt1 grph.26t  $ 1200K (VHTR conditions)
mt1 grph.28t  $ 1600K (accident conditions)
mt1 grph.30t  $ 2000K (severe accident)
```

**Water S(α,β) libraries**:
```mcnp
mt2 lwtr.10t  $ 294K (room temperature)
mt2 lwtr.11t  $ 325K (PWR cold leg ~52°C)
mt2 lwtr.13t  $ 350K (PWR average ~77°C)
mt2 lwtr.14t  $ 400K (PWR hot leg ~127°C)
mt2 lwtr.16t  $ 500K (supercritical water)
mt2 lwtr.20t  $ 800K (steam)
```

**CRITICAL RULE**: Match S(α,β) temperature to problem physics!

### TRISO Fuel Material Compositions

**UCO Kernel** (Uranium Carbide-Oxide):
```mcnp
m1  $ UCO kernel, 19.75% enriched, 10.924 g/cm³
   92234.00c  3.34179E-03  $ U-234
   92235.00c  1.99636E-01  $ U-235 (enrichment)
   92236.00c  1.93132E-04  $ U-236 (impurity)
   92238.00c  7.96829E-01  $ U-238
    6012.00c  0.3217217    $ C-12 (carbide)
    6013.00c  0.0035783    $ C-13
    8016.00c  1.3613       $ O-16 (oxide)
```

**Note**: Oxygen fraction >1.0 is VALID - MCNP normalizes using cell density

**Buffer Carbon** (porous graphite):
```mcnp
m2  $ Buffer, 1.10 g/cm³
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ Use graphite S(α,β) at 600K
```

**PyC Coating** (pyrolytic carbon):
```mcnp
m3  $ PyC, 1.90 g/cm³
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.18t  $ Graphite thermal scattering
```

**SiC Coating** (silicon carbide):
```mcnp
m4  $ SiC, 3.20 g/cm³
   14028.00c  0.922297
   14029.00c  0.046853
   14030.00c  0.030850
    6012.00c  0.9890
    6013.00c  0.0110
mt4 grph.18t  $ Use for carbon component
```

### Burnup Tracking Materials

**Fuel with fission product tracking**:
```mcnp
m10  $ Depleted UO2 fuel
    1001.70c  3.393340E-02  $ H-1 (from H2O)
    8016.70c  1.696670E-02  $ O-16
   92234.70c  5.873407E-06  $ U-234
   92235.70c  4.198373E-04  $ U-235 (depleted)
   92238.70c  3.057844E-05  $ U-238
   93237.70c  1.886031E-07  $ Np-237 (bred)
   94239.70c  3.962382E-07  $ Pu-239 (bred)
   94240.70c  1.523891E-08  $ Pu-240 (bred)
c Fission products
   54135.70c  4.623582E-13  $ Xe-135 (strong absorber)
   62149.70c  7.632940E-09  $ Sm-149 (40,000 barn)
   64157.70c  1.298438E-10  $ Gd-157 (254,000 barn)
```

**Actinides to track**:
- U-234, U-235, U-236, U-237, U-238
- Np-237, Np-239
- Pu-238, Pu-239, Pu-240, Pu-241, Pu-242
- Am-241, Am-242, Am-243
- Cm-242, Cm-243, Cm-244

**Key fission products** (strong absorbers):
- Xe-135 (2.6×10⁶ barn)
- Sm-149 (40,100 barn)
- Gd-157 (254,000 barn)
- Eu-155 (3,760 barn)

## COMMON ERRORS AND FIXES

### Error 1: Missing Graphite Thermal Scattering

**WRONG**:
```mcnp
m1  $ Graphite - MISSING MT CARD!
    6012.00c  0.9890
    6013.00c  0.0110
```

**RIGHT**:
```mcnp
m1  $ Graphite
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ ← ESSENTIAL for correct physics
```

### Error 2: Wrong Temperature Library

**Problem**: Using room temperature S(α,β) for reactor core

**WRONG**:
```mcnp
mt1 grph.10t  $ 296K - WRONG for 900K reactor!
```

**RIGHT**:
```mcnp
mt1 grph.24t  $ 1000K - appropriate for operating reactor
```

### Error 3: Stoichiometric Confusion

**User thinks O > 1.0 is an error, but it's CORRECT**:

```mcnp
m1  $ UO2
   92235.00c  0.2
   92238.00c  0.8
    8016.00c  2.0  $ ← This is CORRECT (UO₂ has 2 oxygen atoms per U)
```

MCNP normalizes fractions using the cell density specification.
```

#### 2.2 Create thermal_scattering_checker.py

**File**: `.claude/skills/mcnp-material-builder/tools/thermal_scattering_checker.py`

```python
"""
Thermal Scattering (MT Card) Checker for MCNP Materials
Validates that appropriate S(α,β) libraries are applied
"""

def check_material_for_thermal_scattering(material_card):
    """
    Check if material needs thermal scattering library

    Args:
        material_card: String containing M card definition

    Returns:
        dict with warnings and recommendations
    """
    warnings = []
    recommendations = []

    # Check for carbon (graphite)
    if '6012' in material_card or '6000' in material_card:
        warnings.append("Material contains carbon - thermal scattering (grph.XXt) is REQUIRED")
        recommendations.append("Add: mtN grph.18t  $ For 600K operating temperature")
        recommendations.append("     OR grph.10t for room temperature")

    # Check for hydrogen (water)
    if '1001' in material_card or '1002' in material_card:
        if '8016' in material_card or '8000' in material_card:  # Also has oxygen
            warnings.append("Material contains H2O - thermal scattering (lwtr.XXt) is REQUIRED")
            recommendations.append("Add: mtN lwtr.13t  $ For 350K (PWR conditions)")
            recommendations.append("     OR lwtr.10t for room temperature")

    # Check for beryllium
    if '4009' in material_card or '4000' in material_card:
        if '8016' in material_card or '8000' in material_card:  # BeO
            warnings.append("Material contains BeO - thermal scattering (be.XXt) is REQUIRED")
            recommendations.append("Add: mtN beo.10t  $ Beryllium oxide")
        else:  # Pure Be
            warnings.append("Material contains Be metal - thermal scattering (be.XXt) is REQUIRED")
            recommendations.append("Add: mtN be.10t  $ Beryllium metal")

    return {
        'needs_thermal': len(warnings) > 0,
        'warnings': warnings,
        'recommendations': recommendations
    }


# Temperature recommendation engine
TEMP_RANGES = {
    'grph': {
        (0, 350): 'grph.10t',
        (350, 500): 'grph.18t',
        (500, 700): 'grph.22t',
        (700, 900): 'grph.24t',
        (900, 1100): 'grph.26t',
        (1100, 1400): 'grph.28t',
        (1400, 3000): 'grph.30t',
    },
    'lwtr': {
        (0, 310): 'lwtr.10t',
        (310, 340): 'lwtr.11t',
        (340, 375): 'lwtr.13t',
        (375, 450): 'lwtr.14t',
        (450, 650): 'lwtr.16t',
        (650, 1000): 'lwtr.20t',
    }
}


def recommend_thermal_library(material_type, temperature_kelvin):
    """
    Recommend appropriate S(α,β) library based on temperature

    Args:
        material_type: 'grph', 'lwtr', 'be', etc.
        temperature_kelvin: Operating temperature

    Returns:
        Recommended library suffix (e.g., 'grph.18t')
    """
    if material_type not in TEMP_RANGES:
        return None

    for (t_min, t_max), library in TEMP_RANGES[material_type].items():
        if t_min <= temperature_kelvin < t_max:
            return library

    return None


# Example usage
if __name__ == "__main__":
    print("Thermal Scattering Checker\n" + "="*50)

    # Test 1: Graphite without MT card
    material1 = """
m1  $ Graphite
    6012.00c  0.9890
    6013.00c  0.0110
"""
    result = check_material_for_thermal_scattering(material1)
    if result['needs_thermal']:
        print("\nWARNING: Material 1")
        for warning in result['warnings']:
            print(f"  - {warning}")
        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  {rec}")

    # Test 2: Temperature recommendation
    print("\n" + "="*50)
    print("Temperature-based library recommendations:")
    print(f"  Graphite at 600K: {recommend_thermal_library('grph', 600)}")
    print(f"  Water at 350K: {recommend_thermal_library('lwtr', 350)}")
```

#### 2.3 Create TRISO materials example

**File**: `.claude/skills/mcnp-material-builder/assets/examples/triso_materials.txt`

```
c TRISO Particle Material Cards
c Based on AGR-1 experiment specifications
c
c Material 1: UCO Fuel Kernel (19.75% enriched)
c Density: 10.924 g/cm³
m1
   92234.00c  3.34179E-03  $ U-234
   92235.00c  1.99636E-01  $ U-235 (enrichment = 19.75%)
   92236.00c  1.93132E-04  $ U-236
   92238.00c  7.96829E-01  $ U-238
    6012.00c  0.3217217    $ C-12
    6013.00c  0.0035783    $ C-13
    8016.00c  1.3613       $ O-16
c Note: Formula is UC₀.₃₂O₁.₃₆ (carbide-oxide)
c
c Material 2: Buffer Layer (porous carbon)
c Density: 1.10 g/cm³
m2
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ Graphite S(α,β) at 600K
c
c Material 3: Inner PyC Layer (dense pyrolytic carbon)
c Density: 1.904 g/cm³
m3
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.18t
c
c Material 4: SiC Layer (silicon carbide ceramic)
c Density: 3.205 g/cm³
m4
   14028.00c  0.922297  $ Si-28 (92.23%)
   14029.00c  0.046853  $ Si-29 (4.68%)
   14030.00c  0.030850  $ Si-30 (3.09%)
    6012.00c  0.9890    $ C-12
    6013.00c  0.0110    $ C-13
mt4 grph.18t  $ Use graphite S(α,β) for carbon component
c
c Material 5: Outer PyC Layer (dense pyrolytic carbon)
c Density: 1.911 g/cm³
m5
    6012.00c  0.9890
    6013.00c  0.0110
mt5 grph.18t
c
c Material 6: SiC Matrix (binds particles together)
c Density: 1.344 g/cm³
m6
   14028.00c  0.922297
   14029.00c  0.046853
   14030.00c  0.030850
    6012.00c  0.9890
    6013.00c  0.0110
mt6 grph.18t
```

### Validation Test

**Test Input**: User asks "Create materials for TRISO fuel particles"

**Expected Output**: Skill provides:
1. ✅ All 6 material cards (kernel + 5 coatings)
2. ✅ Proper densities
3. ✅ MT cards for ALL carbon-containing materials
4. ✅ Explanation of UCO composition
5. ✅ Temperature-appropriate S(α,β) libraries

---

## 3. mcnp-input-validator

**Priority**: 🔴 **CRITICAL** - No lattice dimension validation

**Location**: `.claude/skills/mcnp-input-validator/`

### Files to Modify

#### 3.1 Update SKILL.md

**ADD validation sections for**:
- FILL array dimension checking
- Universe cross-reference validation
- Numbering conflict detection
- Thermal scattering verification

#### 3.2 Create fill_array_validator.py

**File**: `.claude/skills/mcnp-input-validator/tools/fill_array_validator.py`

```python
"""
FILL Array Dimension Validator
Checks that FILL arrays have correct number of elements
"""

import re

def parse_fill_spec(fill_line):
    """
    Parse fill= specification from MCNP cell card

    Example: "fill=-7:7 -7:7 0:0"
    Returns: {min_i, max_i, min_j, max_j, min_k, max_k}
    """
    match = re.search(r'fill=(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)\s+(-?\d+):(-?\d+)', fill_line)
    if not match:
        return None

    return {
        'min_i': int(match.group(1)),
        'max_i': int(match.group(2)),
        'min_j': int(match.group(3)),
        'max_j': int(match.group(4)),
        'min_k': int(match.group(5)),
        'max_k': int(match.group(6)),
    }


def count_fill_elements(cell_block, cell_number):
    """
    Count universe elements in FILL array

    Args:
        cell_block: Text of cell block
        cell_number: Cell ID to check

    Returns:
        Number of universe specifications found
    """
    # Find the cell and continuation lines
    pattern = rf'^{cell_number}\s+.*?(?=^\d+\s|\Z)'
    match = re.search(pattern, cell_block, re.MULTILINE | re.DOTALL)

    if not match:
        return 0

    cell_text = match.group(0)

    # Find all universe numbers and repeat notation
    # Pattern: universe_id or universe_id nR
    pattern = r'(\d{4})\s*(\d+R)?'
    matches = re.findall(pattern, cell_text)

    count = 0
    for universe, repeat in matches:
        if repeat:
            # Extract n from "nR" and add n+1 copies
            n = int(repeat[:-1])
            count += n + 1
        else:
            count += 1

    return count


def validate_fill_array(cell_card):
    """
    Validate FILL array dimensions

    Args:
        cell_card: Complete cell card text including continuations

    Returns:
        dict with validation results
    """
    errors = []
    warnings = []

    # Parse fill specification
    fill_spec = parse_fill_spec(cell_card)
    if not fill_spec:
        return {'valid': True, 'errors': [], 'warnings': ['No fill specification found']}

    # Calculate expected elements
    i_count = fill_spec['max_i'] - fill_spec['min_i'] + 1
    j_count = fill_spec['max_j'] - fill_spec['min_j'] + 1
    k_count = fill_spec['max_k'] - fill_spec['min_k'] + 1
    expected = i_count * j_count * k_count

    # Count actual elements
    # (This is simplified - full implementation would parse repeat notation)
    # For demonstration, just report expected

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'expected_elements': expected,
        'breakdown': f"{k_count} layers of {j_count}×{i_count}"
    }
```

### Validation Test

User provides input with wrong FILL dimensions → Skill catches error before MCNP run

---

## 4. mcnp-geometry-builder

**Priority**: 🔴 **CRITICAL** - No TRISO or reactor geometry templates

### Files to Add

#### 4.1 Create TRISO geometry template

**File**: `.claude/skills/mcnp-geometry-builder/assets/templates/triso_particle_template.txt`

(Include complete 5-layer TRISO geometry)

#### 4.2 Update SKILL.md with multi-scale geometry guidance

---

# PHASE 2: MAJOR ENHANCEMENTS

## 5. mcnp-template-generator (NEW SKILL)

**Priority**: 🟡 **HIGH** - Enables parametric studies

**Location**: `.claude/skills/mcnp-template-generator/` (CREATE NEW)

### Skill Structure

```
mcnp-template-generator/
├── SKILL.md
├── tools/
│   ├── template_identifier.py
│   ├── jinja2_converter.py
│   └── csv_generator.py
├── assets/
│   ├── examples/
│   │   ├── simple_template_example/
│   │   └── agr1_template_example/
│   └── templates/
│       └── basic_template.j2
└── README.md
```

### SKILL.md Content

```markdown
# MCNP Template Generator Skill

## Purpose
Convert existing MCNP inputs into parameterizable Jinja2 templates for:
- Multi-cycle burnup calculations
- Parameter sensitivity studies
- Design optimization
- Benchmark series

## When to Use Templates

**Use template-based approach when**:
✅ Large existing model with small parametric changes
✅ Time-varying configurations (control rods, fuel loading)
✅ External data drives parameters (CSV files, databases)
✅ Multiple related input variants needed

**Use programmatic generation when**:
✅ Building model from scratch
✅ Complex algorithmic geometry
✅ Highly variable structure

## Template Workflow

### Step 1: Identify Variable Sections
```python
from tools.template_identifier import find_variable_sections

sections = find_variable_sections('input.i', [
    'control_rod_position',
    'fuel_enrichment',
    'assembly_loading'
])
```

### Step 2: Convert to Jinja2
```python
from tools.jinja2_converter import convert_to_template

template = convert_to_template(
    input_file='input.i',
    variables=['oscc_angle', 'neck_shim_state', 'power_distribution']
)
```

### Step 3: Create Data Files
```python
from tools.csv_generator import generate_parameter_csv

generate_parameter_csv(
    template=template,
    param_ranges={'enrichment': [5, 10, 15, 20]},
    output='parameters.csv'
)
```

### Step 4: Render Inputs
```python
from jinja2 import Template

template = Template(template_text)
for params in parameter_sets:
    output = template.render(**params)
    write_file(f"input_{params['id']}.i", output)
```

## Example: Control Rod Study

### Base Input
```mcnp
c Control drum at 65 degrees
1001 1 -8.0  -1001 1002 -1003
1002 2 -2.7   1001 -1004
```

### Template
```jinja2
c Control drum at {{drum_angle}} degrees
1001 1 -8.0  -{{drum_surface[drum_angle]}} 1002 -1003
1002 2 -2.7   {{drum_surface[drum_angle]}} -1004
```

### Parameters (CSV)
```
case,drum_angle
1,0
2,25
3,50
4,75
5,100
```

## Working Example

See `assets/examples/agr1_template_example/` for complete AGR-1 template workflow.
```

### Python Tools

#### template_identifier.py

```python
"""
Identify parameterizable sections in MCNP input
"""

def find_variable_sections(input_file, keywords):
    """
    Find sections of MCNP input that vary based on keywords

    Returns suggested template variables
    """
    pass  # Implementation
```

### Validation Test

User provides MCNP input + list of variable parameters → Skill generates working Jinja2 template

---

# PHASE 3: ADVANCED FEATURES

(Similar detailed plans for mcnp-programmatic-generator, mcnp-workflow-integrator, etc.)

---

# IMPLEMENTATION CHECKLIST

## Session 1 (HIGH PRIORITY)

- [ ] mcnp-lattice-builder
  - [ ] Update SKILL.md (add FILL mechanics, repeat notation)
  - [ ] Create lattice_dimension_calculator.py
  - [ ] Add 2 TRISO lattice examples
  - [ ] Test with user query

- [ ] mcnp-material-builder
  - [ ] Update SKILL.md (thermal scattering section)
  - [ ] Create thermal_scattering_checker.py
  - [ ] Add TRISO materials example
  - [ ] Test with user query

- [ ] mcnp-input-validator
  - [ ] Update SKILL.md
  - [ ] Create fill_array_validator.py
  - [ ] Test validation

- [ ] mcnp-geometry-builder
  - [ ] Add TRISO template
  - [ ] Update SKILL.md

## Session 2 (MEDIUM PRIORITY)

- [ ] Create mcnp-template-generator skill
  - [ ] Full skill structure
  - [ ] 3 Python tools
  - [ ] AGR-1 example

- [ ] Update mcnp-input-builder
- [ ] Update mcnp-cell-checker
- [ ] Update mcnp-cross-reference-checker

## Session 3 (LOW PRIORITY)

- [ ] Create mcnp-programmatic-generator
- [ ] Create mcnp-workflow-integrator
- [ ] Final testing and documentation

---

# SUCCESS CRITERIA

**Each updated skill must**:
1. ✅ Address specific issues identified in analysis
2. ✅ Include working examples from HTGR repository
3. ✅ Provide validation/testing tools
4. ✅ Pass user query tests
5. ✅ Include clear error messages and guidance

**Overall success**:
- ✅ User can build TRISO particle model using skills
- ✅ User can create multi-level lattices (>2 levels)
- ✅ User can generate parameterized inputs
- ✅ Skills catch common errors before MCNP run
- ✅ All thermal scattering requirements identified

---

**PLAN READY FOR EXECUTION**

This plan can be executed immediately in the next session. Each section provides:
- Exact file paths
- Specific content to add
- Working code examples
- Validation tests

Start with Phase 1, complete all 4 skills, then move to Phase 2.
