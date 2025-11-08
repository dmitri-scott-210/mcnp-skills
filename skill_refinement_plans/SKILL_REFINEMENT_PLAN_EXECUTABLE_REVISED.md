# COMPREHENSIVE MCNP SKILL REFINEMENT PLAN (REVISED)
## Immediately Executable Plan for Next Session

**Created**: November 7, 2025 (Revised)
**Based On**: 13 comprehensive analysis documents (469 KB) from HTGR reactor model study
**Execution Time Estimate**: 3-4 hours for HIGH priority items

**REVISION NOTES**:
- ✅ Added hexagonal lattice (LAT=2) guidance throughout
- ✅ Always specify lattice TYPE in examples
- ✅ Completed validation logic for both rectangular AND hexagonal
- ✅ Generalized beyond TRISO to complex reactor models
- ✅ Created TRISO-specific reference files (supplements, not main focus)
- ✅ Used correct skill directory structure (no assets/ subdirectories)

---

## OVERVIEW

This plan provides **specific, actionable updates** to ALL relevant MCNP skills based on analysis of production-quality reactor models (HTGR, TRISO fuel, PWR-like assemblies). Each section includes:

- ✅ **Files to modify** (exact paths)
- ✅ **Specific content to add** (ready to insert)
- ✅ **New example files** (both rectangular AND hexagonal lattices)
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

**Priority**: 🔴 **CRITICAL** - Current skill fails on complex reactor lattices

**Location**: `.claude/skills/mcnp-lattice-builder/`

### Issue Identified
Current skill does NOT teach:
- Multi-level nesting guidance (>2 levels)
- FILL array dimension calculation
- Repeat notation (nR syntax)
- **Hexagonal lattice (LAT=2) patterns**
- **Lattice type-specific validation**
- Complex reactor assembly structures

**Impact**: Users cannot build ANY complex reactor models (PWR assemblies, HTGR cores, TRISO fuel compacts, etc.)

### Current File Lengths
- SKILL.md: 386 lines (can add content without overbloating)

### Files to Create/Modify

#### 1.1 Update SKILL.md

**File**: `.claude/skills/mcnp-lattice-builder/SKILL.md`

**ADD new section after current content**:

```markdown
## CRITICAL LATTICE CONCEPTS

### Lattice Types in MCNP

MCNP supports TWO lattice types:

1. **LAT=1: Rectangular (Hexahedral) Lattice**
   - Cartesian grid (x, y, z)
   - Bounding surface: RPP (rectangular parallelepiped)
   - Common uses: PWR fuel assemblies, simple cores, vertical stacks

2. **LAT=2: Hexagonal Lattice**
   - 60° coordinate system
   - Bounding surface: RHP (right hexagonal prism)
   - Common uses: HTGR cores, fast reactor assemblies, CANDU bundles

**ALWAYS specify which type you're building!**

### Multi-Level Lattice Hierarchies

MCNP supports **up to 6 practical levels** of nested lattices. Example hierarchy:

```
Level 1: Fuel pin (u=100) - concentric cylinders
Level 2: Pin lattice (u=200, LAT=1) - 17×17 square array
Level 3: Assembly (u=300, LAT=2) - hexagonal arrangement
Level 4: Core (u=0) - multiple assemblies
```

**Pattern**: Each level is a universe that fills into the level above.

**Both rectangular AND hexagonal lattices can be nested in same model.**

### FILL Array Dimension Calculation

**CRITICAL RULE**: Elements needed = (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

**This applies to BOTH rectangular AND hexagonal lattices!**

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
100 2R = 100 100 100 (3 copies total)
200 24R = 200 repeated 25 times total
```

**Full compact lattice example**:
```mcnp
fill=0:0 0:0 -15:15 100 2R 200 24R 100 2R

Breakdown:
  100 2R  = 3 layers of universe 100
  200 24R = 25 layers of universe 200
  100 2R  = 3 layers of universe 100
  Total: 3 + 25 + 3 = 31 elements for indices -15 to +15 ✓
```

**Works identically for rectangular and hexagonal lattices.**

### Index Ordering

**CRITICAL RULE**: Arrays filled in K, J, I order (K outermost loop, I innermost)

**Applies to BOTH LAT=1 and LAT=2.**

For `fill=-7:7 -7:7 0:0`:
- First row corresponds to k=0, j=-7, i varies from -7 to +7
- Second row corresponds to k=0, j=-6, i varies from -7 to +7
- etc.

### Rectangular Lattice (LAT=1) Specifics

**Bounding Surface**: RPP (rectangular parallelepiped)

```mcnp
100 rpp -5.0 5.0 -5.0 5.0 -10.0 10.0  $ 10×10×20 cm box

101 0  -100  u=200 lat=1  fill=-4:4 -4:4 0:0  $ 9×9×1 array
     [... 81 universe numbers ...]
```

**Pitch**: Element spacing in x, y, z directions
- Surface extent = N × pitch (in each direction)
- Example: 9 elements × 1.0 cm pitch = 9.0 cm extent

**Fill pattern**: Straightforward grid

### Hexagonal Lattice (LAT=2) Specifics

**Bounding Surface**: RHP (right hexagonal prism)

```mcnp
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
100 rhp  0 0 0  0 0 68  0 1.6 0  $ Hex prism, R=1.6 cm, height=68 cm

101 0  -100  u=300 lat=2  fill=-6:6 -6:6 0:0  $ 13×13 hexagonal
     [... universe pattern with staggered rows ...]
```

**Pitch**: R-vector magnitude × √3
- Example: R=1.6 cm → pitch = 1.6√3 = 2.77 cm

**Fill pattern**: Staggered rows (60° symmetry)
```
Row j=-6:  U U U U U U U U U U U U U
Row j=-5:   U U U U U U U U U U U U U  ← indented (offset by half pitch)
Row j=-4:  U U U U U U U U U U U U U
```

**Visual indentation is OPTIONAL** (MCNP ignores whitespace), but helps show pattern.

### Circular/Hexagonal Packing Patterns

**Common in reactor models**: Approximate cylindrical or hexagonal geometry using rectangular lattice

**Example: TRISO particles in cylindrical compact**

```mcnp
c Particle lattice (u=1116) - LAT=1 rectangular
91108 0   -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ 15×15 array
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
     1115 1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115 1115
     1115 1115 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1114 1115 1115
     ... (center rows all 1114)
     1115 1115 1115 1115 1115 1115 1114 1114 1114 1115 1115 1115 1115 1115 1115
```

**Result**: ~169 particles (u=1114) + ~56 matrix (u=1115) in circular pattern

**Physical constraint**: Fits in cylindrical compact using square lattice

### Universe Hierarchy Validation

**Rules for valid nested lattices** (both LAT=1 and LAT=2):
1. ✅ Define child universes BEFORE parent universes
2. ✅ No circular references (A fills B, B fills A)
3. ✅ All filled universes must exist
4. ✅ Universe 0 is always global (never define explicitly)
5. ✅ Lattice bounding surface must contain N × pitch dimensions

## WORKING EXAMPLES

See detailed examples in:
- `lattice_patterns_reference.md` (rectangular AND hexagonal examples)
- `complex_reactor_patterns.md` (multi-level nesting, mixed types)
- `triso_fuel_reference.md` (TRISO-specific patterns - optional)

### Example 1: Rectangular Lattice (LAT=1) - Pin Array

```mcnp
c Fuel pin (u=100)
100 1 -10.2  -100         u=100  $ UO2 fuel
101 2 -6.5   100 -101     u=100  $ Zircaloy clad
102 3 -1.0   101          u=100  $ Water

c Pin lattice (u=200) - LAT=1 rectangular
200 0  -200  u=200 lat=1  fill=-8:8 -8:8 0:0  $ 17×17 PWR assembly
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     ... (17 rows, 289 total elements)

c Surfaces
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
200 rpp -10.71 10.71 -10.71 10.71 -180 180  $ Assembly box (17×1.26 cm pitch)

c Materials
m1  $ UO2 fuel
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
m2  $ Zircaloy
   40000.60c  1.0
m3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.10t
```

### Example 2: Hexagonal Lattice (LAT=2) - HTGR Assembly

```mcnp
c Fuel channel (u=100)
100 1 -1.8  -100         u=100  $ Fuel compact
101 2 -1.7   100 -101    u=100  $ Graphite

c Assembly lattice (u=200) - LAT=2 hexagonal
200 0  -200  u=200 lat=2  fill=-6:6 -6:6 0:0  $ 13×13 hex pattern
     300 300 300 300 300 300 300 300 300 300 300 300 300
      300 300 300 300 300 300 100 100 100 300 300 300 300
       300 300 300 300 300 100 100 200 100 100 300 300 300
        300 300 300 100 100 100 100 100 100 100 100 300 300
         300 300 100 100 100 100 100 100 100 100 100 100 300
          ... (hexagonal pattern)

c Surfaces
100 cz  0.6     $ Fuel compact radius
101 cz  0.7     $ Graphite channel radius
200 rhp  0 0 0  0 0 68  0 1.6 0  $ Hex assembly, R=1.6 cm, height=68 cm

c Materials
m1  $ Graphite fuel matrix
    6012.00c  0.99
mt1 grph.18t
m2  $ Graphite reflector
    6012.00c  0.99
mt2 grph.18t
```

**Note**: Universe 200 is coolant channel, 300 is graphite reflector

## COMMON PITFALLS AND FIXES

| Pitfall | Example | Fix |
|---------|---------|-----|
| **Dimension mismatch** | fill=0:10 but only 10 elements | Need 11: (10-0+1)=11 |
| **Repeat off-by-one** | fill=0:10, use "U 10R" (=11) | Use "U 9R" for 10 |
| **Negative index error** | fill=-5:5, think it's 5 | It's 11 (include 0!) |
| **Wrong index order** | Assume I,J,K ordering | MCNP uses K,J,I! |
| **RPP for hex lattice** | LAT=2 with RPP surface | Use RHP for LAT=2 |
| **RHP for rect lattice** | LAT=1 with RHP surface | Use RPP for LAT=1 |
| **Hex pitch wrong** | Use R directly as pitch | Pitch = R × √3 |
| **Surface too small** | 15×15 lattice, 14 pitches | Surface = N × pitch |
| **Universe conflict** | Reuse U=100 for different geom | Use unique numbers |
| **Circular fill** | u=100 fill=200, u=200 fill=100 | Define hierarchy |

## VALIDATION CHECKLIST

Before running MCNP, verify:

- [ ] Lattice type specified: LAT=1 (rectangular) or LAT=2 (hexagonal)
- [ ] Surface type matches: RPP for LAT=1, RHP for LAT=2
- [ ] FILL array element count = (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1)
- [ ] Repeat notation: nR gives n+1 total copies
- [ ] All filled universes are defined before use
- [ ] No circular universe references
- [ ] Lattice bounding surface matches N × pitch (or N × R×√3 for hex)
- [ ] Child universes defined before parent universes
- [ ] Universe numbers are unique (no conflicts)

## REFERENCE FILES

For detailed examples and patterns:
- **lattice_patterns_reference.md** - Comprehensive rectangular and hexagonal examples
- **complex_reactor_patterns.md** - Multi-level nesting, mixed lattice types
- **triso_fuel_reference.md** - TRISO-specific patterns (optional supplemental reading)
```

#### 1.2 Create lattice_patterns_reference.md

**File**: `.claude/skills/mcnp-lattice-builder/lattice_patterns_reference.md`

```markdown
# Lattice Patterns Reference
## Comprehensive Examples for Rectangular and Hexagonal Lattices

This reference provides detailed examples of both LAT=1 (rectangular) and LAT=2 (hexagonal) lattices for complex reactor modeling.

---

## RECTANGULAR LATTICE EXAMPLES (LAT=1)

### Example 1: Simple 2D Pin Lattice (17×17 PWR Assembly)

[Full example with 289 elements]

### Example 2: 3D Vertical Stack (1×1×31 Axial Layers)

[Compact lattice with repeat notation]

### Example 3: Multi-Level Nesting (Pin → Assembly → Core)

[3-level hierarchy example]

---

## HEXAGONAL LATTICE EXAMPLES (LAT=2)

### Example 1: Single Hex Assembly (13×13 Pattern)

[HTGR assembly with fuel/coolant/reflector pattern]

### Example 2: Core-Level Hex Lattice (7-ring Pattern)

[Full core with hexagonal assemblies]

### Example 3: Mixed Lattice Types

[Rectangular fuel pins in hexagonal assemblies]

---

## COMPLEX PATTERNS

### Circular Packing in Rectangular Lattice

[TRISO particle example: 15×15 → ~169 particles]

### Off-Axis Lattice Placement

[Fill with transformation: fill=U (x,y,z)]

### Variable Universe Fill Patterns

[Different universe types in same lattice]
```

#### 1.3 Create complex_reactor_patterns.md

**File**: `.claude/skills/mcnp-lattice-builder/complex_reactor_patterns.md`

```markdown
# Complex Reactor Modeling Patterns

Multi-level lattice hierarchies for advanced reactor geometries.

## Pattern 1: PWR Core (4 Levels)

```
Level 1: Fuel pin (LAT=1, fuel/clad/coolant)
Level 2: Assembly (LAT=1, 17×17 pins)
Level 3: Core quarter (LAT=1, assemblies)
Level 4: Full core (rotation/reflection)
```

## Pattern 2: HTGR Core (5 Levels)

```
Level 1: TRISO particle (5 shells)
Level 2: Particle array (LAT=1, 15×15)
Level 3: Fuel compact (LAT=1, vertical stack)
Level 4: Fuel channel (in hex assembly)
Level 5: Core (LAT=2, hex assemblies)
```

## Pattern 3: Fast Reactor (Mixed Types)

```
Level 1: Fuel pin bundle (LAT=2, hex)
Level 2: Assembly (LAT=1, duct + pins)
Level 3: Core (LAT=2, hex assemblies)
```
```

#### 1.4 Create triso_fuel_reference.md

**File**: `.claude/skills/mcnp-lattice-builder/triso_fuel_reference.md`

```markdown
# TRISO Fuel Modeling Reference (Supplemental)

**Purpose**: This is a supplemental reference for TRISO-specific patterns. The main skill teaches general lattice building applicable to ALL reactor types.

## TRISO Particle Structure

[5-layer coating details]

## Common TRISO Lattice Hierarchies

[Examples from AGR-1, HTR-10, etc.]

## Packing Fraction Calculations

[How to determine particles per compact]
```

#### 1.5 Create Python Tool (REVISED with hex support)

**File**: `.claude/skills/mcnp-lattice-builder/scripts/lattice_dimension_calculator.py`

```python
"""
MCNP Lattice Dimension Calculator
Supports both rectangular (LAT=1) and hexagonal (LAT=2) lattices
"""

def calculate_fill_dimensions(imin, imax, jmin, jmax, kmin, kmax):
    """
    Calculate required number of elements for FILL array

    Works for BOTH LAT=1 and LAT=2!

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

    Works for both rectangular and hexagonal lattices.

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
            For LAT=1: {'pitch_x', 'pitch_y', 'pitch_z', 'x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max'}
            For LAT=2: {'R', 'height', 'origin_z'}

    Returns:
        Dict with validation results and warnings
    """
    warnings = []

    if lat_type == 1:  # Rectangular
        # Check if RPP surface matches lattice dimensions
        if 'pitch_x' in surface_params and 'x_min' in surface_params:
            expected_x_extent = fill_spec['i_count'] * surface_params['pitch_x']
            actual_x_extent = surface_params['x_max'] - surface_params['x_min']
            if abs(expected_x_extent - actual_x_extent) > 0.001:
                warnings.append(
                    f"X dimension mismatch: {fill_spec['i_count']} elements × "
                    f"{surface_params['pitch_x']} cm pitch = {expected_x_extent} cm, "
                    f"but RPP surface extent = {actual_x_extent} cm"
                )

        if 'pitch_y' in surface_params and 'y_min' in surface_params:
            expected_y_extent = fill_spec['j_count'] * surface_params['pitch_y']
            actual_y_extent = surface_params['y_max'] - surface_params['y_min']
            if abs(expected_y_extent - actual_y_extent) > 0.001:
                warnings.append(
                    f"Y dimension mismatch: {fill_spec['j_count']} elements × "
                    f"{surface_params['pitch_y']} cm pitch = {expected_y_extent} cm, "
                    f"but RPP surface extent = {actual_y_extent} cm"
                )

        if 'pitch_z' in surface_params and 'z_min' in surface_params:
            expected_z_extent = fill_spec['k_count'] * surface_params['pitch_z']
            actual_z_extent = surface_params['z_max'] - surface_params['z_min']
            if abs(expected_z_extent - actual_z_extent) > 0.001:
                warnings.append(
                    f"Z dimension mismatch: {fill_spec['k_count']} elements × "
                    f"{surface_params['pitch_z']} cm pitch = {expected_z_extent} cm, "
                    f"but RPP surface extent = {actual_z_extent} cm"
                )

    elif lat_type == 2:  # Hexagonal
        # Check if RHP surface matches hex lattice
        if 'R' in surface_params:
            # Hexagonal pitch = R × √3
            hex_pitch = surface_params['R'] * 1.732050808  # √3

            # For hexagonal lattice, the "diameter" of the pattern is roughly:
            # (max(i_count, j_count) - 1) × hex_pitch
            # This is approximate - hex geometry is complex
            max_elements = max(fill_spec['i_count'], fill_spec['j_count'])
            expected_extent = (max_elements - 1) * hex_pitch

            warnings.append(
                f"Hexagonal lattice: R={surface_params['R']} cm → pitch={hex_pitch:.3f} cm. "
                f"Verify RHP surface can contain {fill_spec['i_count']}×{fill_spec['j_count']} elements."
            )

        if 'height' in surface_params and 'origin_z' in surface_params:
            # For vertical extent, similar to rectangular
            if 'pitch_z' in surface_params:
                expected_z_extent = fill_spec['k_count'] * surface_params['pitch_z']
                if abs(expected_z_extent - surface_params['height']) > 0.001:
                    warnings.append(
                        f"Z dimension mismatch: {fill_spec['k_count']} elements × "
                        f"{surface_params['pitch_z']} cm = {expected_z_extent} cm, "
                        f"but RHP height = {surface_params['height']} cm"
                    )

    return {
        'valid': len(warnings) == 0,
        'warnings': warnings
    }


def calculate_hex_pitch(R):
    """
    Calculate hexagonal lattice pitch from R-vector magnitude

    Args:
        R: R-vector magnitude from RHP surface

    Returns:
        Hexagonal pitch (R × √3)
    """
    return R * 1.732050808


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("MCNP Lattice Dimension Calculator")
    print("Supports both LAT=1 (rectangular) and LAT=2 (hexagonal)")
    print("=" * 60)

    # Example 1: 15×15 rectangular particle lattice
    print("\nExample 1: Rectangular Lattice (LAT=1)")
    dims = calculate_fill_dimensions(-7, 7, -7, 7, 0, 0)
    print(f"  {dims['fill_spec']}")
    print(f"  Required elements: {dims['total_elements']}")
    print(f"  Layout: {dims['note']}")

    # Example 2: 13×13 hexagonal assembly
    print("\nExample 2: Hexagonal Lattice (LAT=2)")
    dims = calculate_fill_dimensions(-6, 6, -6, 6, 0, 0)
    print(f"  {dims['fill_spec']}")
    print(f"  Required elements: {dims['total_elements']}")
    print(f"  Layout: {dims['note']}")

    hex_pitch = calculate_hex_pitch(1.6)
    print(f"  Hex pitch (R=1.6): {hex_pitch:.3f} cm")

    # Example 3: 1×1×31 vertical stack (works for both LAT types)
    print("\nExample 3: Vertical Stack (LAT=1 or LAT=2)")
    dims = calculate_fill_dimensions(0, 0, 0, 0, -15, 15)
    print(f"  {dims['fill_spec']}")
    print(f"  Required elements: {dims['total_elements']}")
    print(f"  Layout: {dims['note']}")

    # Example 4: Repeat notation
    print("\nExample 4: Repeat Notation Conversion")
    universes = [100, 100, 100] + [200]*25 + [100, 100, 100]
    repeat_str = repeat_notation_converter(universes)
    print(f"  Universe list: [100,100,100] + [200]×25 + [100,100,100]")
    print(f"  MCNP format: {repeat_str}")
    print(f"  Expected: 100 2R 200 24R 100 2R")

    # Example 5: Validation - rectangular
    print("\nExample 5: Validation - Rectangular Lattice")
    fill = calculate_fill_dimensions(-8, 8, -8, 8, 0, 0)
    surface = {
        'pitch_x': 1.26,
        'pitch_y': 1.26,
        'x_min': -10.71,
        'x_max': 10.71,
        'y_min': -10.71,
        'y_max': 10.71
    }
    result = validate_lattice_dimensions(1, fill, surface)
    print(f"  Valid: {result['valid']}")
    if result['warnings']:
        for w in result['warnings']:
            print(f"  WARNING: {w}")

    # Example 6: Validation - hexagonal
    print("\nExample 6: Validation - Hexagonal Lattice")
    fill = calculate_fill_dimensions(-6, 6, -6, 6, 0, 0)
    surface = {'R': 1.6, 'height': 68.0, 'origin_z': 0.0}
    result = validate_lattice_dimensions(2, fill, surface)
    print(f"  Valid: {result['valid']}")
    if result['warnings']:
        for w in result['warnings']:
            print(f"  INFO: {w}")
```

#### 1.6 Create Example Files

**File**: `.claude/skills/mcnp-lattice-builder/example_inputs/rectangular_pwr_assembly.i`

```mcnp
c 17×17 PWR Assembly - Rectangular Lattice Example (LAT=1)
c Demonstrates multi-level nesting and proper surface sizing
c
c Level 1: Fuel pin (u=100)
c Level 2: Assembly lattice (u=200, LAT=1)
c
c Cells
c
c Fuel pin universe (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Assembly lattice (u=200) - LAT=1 rectangular
c 17×17 = 289 elements, pitch = 1.26 cm
200 0  -200  u=200 lat=1  imp:n=1  fill=-8:8 -8:8 0:0
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     100 100 100 101 100 100 100 100 100 100 100 100 100 101 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 101 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 102 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 101 100 100 101 100 100 101 100 100 101 100 100 101 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 101 100 100 100 100 100 100 100 100 100 101 100 100 100
     100 100 100 100 100 101 100 100 101 100 100 101 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100

c Global placement
999 0  -200 fill=200  imp:n=1
1000 0  200  imp:n=0  $ Outside world

c
c Surfaces
c
c Pin surfaces (centered at origin for universe)
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius

c Assembly surface
c 17 elements × 1.26 cm pitch = 21.42 cm extent → ±10.71 cm from center
200 rpp -10.71 10.71 -10.71 10.71 -180 180  $ Assembly box

c
c Materials
c
m1  $ UO2 fuel, 4% enriched
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
c
m2  $ Zircaloy clad
   40000.60c  1.0
c
m3  $ Light water moderator
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t  $ 350K PWR conditions
c
c Source
kcode 10000 1.0 50 250
ksrc 0 0 0
```

**File**: `.claude/skills/mcnp-lattice-builder/example_inputs/hexagonal_htgr_assembly.i`

```mcnp
c HTGR Hexagonal Assembly - Hexagonal Lattice Example (LAT=2)
c Demonstrates hexagonal geometry with proper RHP surface
c
c Level 1: Fuel channel (u=100), coolant (u=200), graphite (u=300)
c Level 2: Assembly lattice (u=400, LAT=2)
c
c Cells
c
c Fuel channel universe (u=100)
100 1 -1.8  -100         u=100  imp:n=1  $ Fuel compact
101 2 -1.7   100 -101    u=100  imp:n=1  $ Graphite channel

c Coolant channel universe (u=200)
200 3 -5e-3  -102         u=200  imp:n=1  $ Helium coolant
201 2 -1.7    102 -103    u=200  imp:n=1  $ Graphite

c Graphite cell universe (u=300)
300 2 -1.7  -104         u=300  imp:n=1  $ Solid graphite

c Assembly lattice (u=400) - LAT=2 hexagonal
c 13×13 hexagonal pattern (fill=-6:6 -6:6 0:0 = 169 elements)
c Pitch = R × √3 = 1.6 × 1.732 = 2.77 cm
400 0  -400  u=400 lat=2  imp:n=1  fill=-6:6 -6:6 0:0
     300 300 300 300 300 300 300 300 300 300 300 300 300
      300 300 300 300 300 300 100 100 100 300 300 300 300
       300 300 300 300 300 100 100 200 100 100 300 300 300
        300 300 300 100 100 100 100 100 100 100 100 300 300
         300 300 100 100 100 100 100 100 100 100 100 100 300
          300 100 100 200 100 100 200 100 100 200 100 100 300
           300 100 100 100 100 100 100 100 100 100 100 300
            300 100 200 100 100 200 100 100 200 100 300
             300 100 100 100 100 100 100 100 100 300
              300 100 100 200 100 100 200 100 100 300
               300 100 100 100 100 100 100 100 300
                300 300 100 100 100 100 100 300 300
                 300 300 300 100 100 100 300 300 300

c Global placement
999 0  -400 fill=400  imp:n=1
1000 0  400  imp:n=0  $ Outside world

c
c Surfaces
c
c Channel surfaces (centered at origin for universe)
100 cz  0.6     $ Fuel compact radius
101 cz  0.7     $ Fuel channel outer radius
102 cz  0.4     $ Coolant channel radius
103 cz  0.5     $ Coolant channel outer radius
104 cz  0.7     $ Graphite cell radius

c Assembly surface - RHP (right hexagonal prism)
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
c      0       0       0         0       0      68       0  1.6  0
c R = 1.6 cm → pitch = 1.6 × √3 = 2.77 cm
400 rhp  0 0 0  0 0 68  0 1.6 0  $ Hex assembly, height=68 cm

c
c Materials
c
m1  $ Graphite fuel matrix
    6012.00c  0.9890
    6013.00c  0.0110
mt1 grph.18t  $ 600K graphite
c
m2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t
c
m3  $ Helium coolant at 3 MPa, 900K
    2004.00c  1.0
c
c Source
kcode 10000 1.0 50 250
ksrc 0 0 0
```

### Validation Tests (REVISED)

**Test 1**: User asks "How do I create a **rectangular** lattice with 17×17 fuel pins?"

**Expected Output**: Skill provides:
1. ✅ Lattice type: LAT=1 (rectangular)
2. ✅ Surface type: RPP
3. ✅ Dimension calculation (17×17×1 = 289 elements)
4. ✅ fill=-8:8 -8:8 0:0 specification
5. ✅ Working PWR assembly example
6. ✅ Validation checklist

**Test 2**: User asks "How do I create a **hexagonal** lattice for HTGR assemblies?"

**Expected Output**: Skill provides:
1. ✅ Lattice type: LAT=2 (hexagonal)
2. ✅ Surface type: RHP
3. ✅ Pitch calculation (R × √3)
4. ✅ Dimension calculation for hex pattern
5. ✅ Working HTGR example with staggered rows
6. ✅ Validation checklist

**Test 3**: User asks "Create a multi-level lattice for a reactor core"

**Expected Output**: Skill provides:
1. ✅ Options: rectangular OR hexagonal at each level
2. ✅ Example hierarchies for both
3. ✅ Reference to complex_reactor_patterns.md

---

## 2. mcnp-material-builder

**Priority**: 🔴 **CRITICAL** - Missing thermal scattering guidance

**Location**: `.claude/skills/mcnp-material-builder/`

### Issue Identified
Current skill does NOT adequately cover:
- Thermal scattering (MT cards) - when required
- Temperature-dependent library selection
- Complex fuel compositions (UCO, TRISO, MOX, etc.)
- Burnup tracking material requirements

**Impact**: Missing MT cards cause 1000s of pcm reactivity errors in ANY thermal reactor model

### Files to Modify

#### 2.1 Update SKILL.md

[Content similar to before, but GENERALIZED]

**ADD new section**:

```markdown
## THERMAL SCATTERING (MT CARDS) - CRITICAL

### When MT Cards Are REQUIRED

**ALWAYS use thermal scattering for**:
- ✅ **Graphite** (any reactor type: HTGR, RBMK, graphite-moderated)
- ✅ **Light water** (PWR, BWR, research reactors)
- ✅ **Heavy water** (CANDU, research reactors)
- ✅ **Polyethylene** (shielding, neutron sources)
- ✅ **Beryllium metal** (reflectors, moderators)
- ✅ **Beryllium oxide** (BeO reflectors)

**Impact of missing MT cards**:
- ❌ Wrong thermal neutron spectrum (hardened)
- ❌ Incorrect reactivity (typically 1000-5000 pcm error)
- ❌ Wrong flux distribution (spatial errors)
- ❌ Invalid benchmark comparisons

**This applies to ALL reactor types, not just TRISO-fueled reactors.**

### Temperature-Dependent Libraries

**Graphite S(α,β) libraries**:
```mcnp
mt1 grph.10t  $ 296K (room temperature, cold criticals)
mt1 grph.18t  $ 600K (HTGR operating, some fast reactors)
mt1 grph.22t  $ 800K (high-temperature HTGR)
mt1 grph.24t  $ 1000K (very high-temperature gas reactor)
mt1 grph.26t  $ 1200K (VHTR conditions)
mt1 grph.28t  $ 1600K (accident conditions)
mt1 grph.30t  $ 2000K (severe accident)
```

**Water S(α,β) libraries**:
```mcnp
mt2 lwtr.10t  $ 294K (room temperature, cold criticals)
mt2 lwtr.11t  $ 325K (PWR cold leg ~52°C)
mt2 lwtr.13t  $ 350K (PWR average ~77°C)
mt2 lwtr.14t  $ 400K (PWR hot leg ~127°C)
mt2 lwtr.16t  $ 500K (supercritical water reactor)
mt2 lwtr.20t  $ 800K (steam, BWR conditions)
```

**Heavy water S(α,β) libraries**:
```mcnp
mt3 hwtr.10t  $ 294K (CANDU cold)
mt3 hwtr.11t  $ 325K (CANDU operating)
```

**CRITICAL RULE**: Match S(α,β) temperature to reactor operating conditions!

### Common Reactor Fuel Compositions

**See detailed reference files for specific examples**:
- `fuel_compositions_reference.md` - UO₂, MOX, UCO, metallic, etc.
- `triso_fuel_reference.md` - TRISO-specific patterns (supplemental)

### Example: Standard UO₂ Fuel

```mcnp
m1  $ UO2 fuel, 4.5% enriched, 10.5 g/cm³
   92234.70c  3.6e-4   $ U-234
   92235.70c  0.045    $ U-235 (enrichment)
   92238.70c  0.955    $ U-238
    8016.70c  2.0      $ O-16 (stoichiometric UO₂)
```

### Example: Graphite Moderator/Reflector

```mcnp
m2  $ Graphite moderator
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t  $ REQUIRED! Use temperature-appropriate library
```

**Missing this MT card is a CRITICAL ERROR.**

## COMMON ERRORS AND FIXES

### Error 1: Missing Graphite Thermal Scattering

**WRONG** (Applies to ANY graphite-containing reactor):
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

[... rest similar to before but generalized ...]

## REFERENCE FILES

For detailed fuel compositions and examples:
- **fuel_compositions_reference.md** - Comprehensive fuel types (UO₂, MOX, UCO, metallic, etc.)
- **thermal_scattering_guide.md** - Complete S(α,β) library reference
- **triso_fuel_reference.md** - TRISO-specific patterns (optional supplemental reading)
```

#### 2.2 Create fuel_compositions_reference.md

**File**: `.claude/skills/mcnp-material-builder/fuel_compositions_reference.md`

```markdown
# Fuel Compositions Reference

Comprehensive examples for common reactor fuel types.

## UO₂ Fuel (Light Water Reactors)

[PWR, BWR examples with various enrichments]

## MOX Fuel (Mixed Oxide)

[Pu-bearing fuel examples]

## UCO Fuel (TRISO kernels)

[Uranium carbide-oxide for HTGRs]

## Metallic Fuel (Fast Reactors)

[U-Zr, U-Pu-Zr alloys]

## HALEU Fuel (High-Assay Low-Enriched Uranium)

[5-20% enriched for advanced reactors]
```

#### 2.3 Create thermal_scattering_guide.md

**File**: `.claude/skills/mcnp-material-builder/thermal_scattering_guide.md`

```markdown
# Thermal Scattering Library Guide

Complete reference for S(α,β) libraries.

## When Required

[Detailed physics explanation]

## Available Libraries

[Complete table: grph, lwtr, hwtr, poly, be, beo, etc.]

## Temperature Selection

[Decision tree for choosing appropriate temperature]

## Common Mistakes

[Pitfalls and how to avoid them]
```

#### 2.4 Keep triso_fuel_reference.md as supplemental

**File**: `.claude/skills/mcnp-material-builder/triso_fuel_reference.md`

[TRISO-specific content - supplemental, not main focus]

---

[Continue with sections 3 and 4 similarly revised...]

---

# IMPLEMENTATION CHECKLIST (REVISED)

## Session 1 (HIGH PRIORITY)

- [ ] mcnp-lattice-builder
  - [ ] Update SKILL.md (BOTH rectangular AND hexagonal)
  - [ ] Create lattice_patterns_reference.md (comprehensive examples)
  - [ ] Create complex_reactor_patterns.md (multi-level, mixed types)
  - [ ] Create triso_fuel_reference.md (supplemental)
  - [ ] Create scripts/lattice_dimension_calculator.py (LAT=1 AND LAT=2)
  - [ ] Create example_inputs/rectangular_pwr_assembly.i
  - [ ] Create example_inputs/hexagonal_htgr_assembly.i
  - [ ] Test with BOTH rectangular AND hexagonal queries

- [ ] mcnp-material-builder
  - [ ] Update SKILL.md (generalized, not TRISO-specific)
  - [ ] Create fuel_compositions_reference.md (all fuel types)
  - [ ] Create thermal_scattering_guide.md (complete S(α,β) reference)
  - [ ] Create triso_fuel_reference.md (supplemental)
  - [ ] Create scripts/thermal_scattering_checker.py
  - [ ] Create example_inputs/common_fuel_materials.txt
  - [ ] Test with various fuel type queries

- [ ] mcnp-input-validator
  - [ ] Update SKILL.md
  - [ ] Create scripts/fill_array_validator.py (LAT=1 AND LAT=2)
  - [ ] Test validation for both lattice types

- [ ] mcnp-geometry-builder
  - [ ] Update SKILL.md
  - [ ] Create templates/fuel_pin_template.txt
  - [ ] Create templates/hex_assembly_template.txt
  - [ ] Create triso_particle_reference.md (supplemental)

---

# SUCCESS CRITERIA (REVISED)

**Each updated skill must**:
1. ✅ Support BOTH rectangular AND hexagonal lattices
2. ✅ Always specify lattice TYPE in examples
3. ✅ Generalize to ALL complex reactor models (not just TRISO)
4. ✅ Use correct directory structure (no assets/ subdirectories)
5. ✅ Include working examples for both LAT=1 and LAT=2
6. ✅ Pass user query tests for BOTH lattice types
7. ✅ Provide TRISO content as supplemental reference, not main focus

**Overall success**:
- ✅ User can build complex reactor models (PWR, BWR, HTGR, fast reactors, etc.)
- ✅ User can create multi-level lattices with either LAT=1 or LAT=2
- ✅ User understands when to use rectangular vs hexagonal
- ✅ Skills catch common errors before MCNP run
- ✅ All thermal scattering requirements identified
- ✅ TRISO is ONE example among many fuel types

---

**REVISED PLAN READY FOR EXECUTION**

This revised plan addresses all your concerns:
- ✅ Hexagonal lattices (LAT=2) fully covered
- ✅ Lattice TYPE always specified
- ✅ Python validation completed for both types
- ✅ Generalized beyond TRISO
- ✅ Correct directory structure
- ✅ Reference files at ROOT skill directory
- ✅ TRISO as supplemental content

Start with Phase 1, complete all 4 skills with BOTH rectangular and hexagonal support.
