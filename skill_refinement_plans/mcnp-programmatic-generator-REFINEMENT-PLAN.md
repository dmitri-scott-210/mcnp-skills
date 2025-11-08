# MCNP PROGRAMMATIC GENERATOR SKILL - REFINEMENT PLAN
## NEW SKILL: Function-Based MCNP Input Generation

**Created**: November 8, 2025
**Based On**: Microreactor programmatic model analysis + AGR-1 workflow findings
**Priority**: 🟡 **MEDIUM-HIGH** - Critical for complex reactor model development
**Execution Time Estimate**: 2-3 hours for initial implementation

---

## EXECUTIVE SUMMARY

This plan creates a NEW skill for **programmatic (function-based) MCNP input generation**, complementing the template-based approach. Based on analysis of production microreactor models, this approach is essential for:

- ✅ **Parametric reactor designs** (varying geometry, materials, configurations)
- ✅ **Multi-variant generation** (burnup vs. shielding models from same codebase)
- ✅ **Systematic assembly replication** (100+ fuel assemblies with variations)
- ✅ **Maintainable reactor models** (changes propagate automatically)
- ✅ **Design space exploration** (automated parameter sweeps)

**Key Distinction**:
- **Template-based** (mcnp-template-generator): Best for multi-cycle time-series with fixed geometry
- **Programmatic** (mcnp-programmatic-generator): Best for parametric designs with geometric variations

---

## COMPARISON: TEMPLATE vs. PROGRAMMATIC APPROACHES

### Template-Based (Jinja2 + CSV)
```
bench.template (13,727 lines)
  + power.csv
  + oscc.csv
  + neck_shim.csv
  + create_inputs.py
  → 13 cycle-specific inputs
```
**Best for**: Time-series, multi-cycle burnup, operational history

### Programmatic (Function-Based)
```
input_definition.py (461 lines)
  + generate_burnup.py
  + generate_sdr.py
  → Multiple model variants
```
**Best for**: Parametric designs, assembly variations, model variants

**BOTH approaches are essential for professional reactor modeling.**

---

## CRITICAL PATTERNS FROM MICROREACTOR ANALYSIS

### Pattern 1: Consistent Function Return Interface

**ALL geometry functions return the SAME structure**:

```python
def fuel(layer, number):
    """Generate fuel assembly geometry"""

    # Calculate positions, numbering
    # ...

    # Generate MCNP cards
    cells = f"""c Fuel assembly {layer}-{number}
{cell_id} {mat_id} -10.8  -{surf_id}  u={univ_id}  imp:n=1
"""

    surfaces = f"""c Fuel assembly surfaces
{surf_id} so  0.0250    $ Kernel
{surf_id+1} c/z  0 0  1.150 $ Fuel channel
"""

    materials = f"""m{mat_id}  $ UO2 kernel
     92235.00c   4.816186e-03
     92238.00c   1.932238e-02
"""

    return cells, surfaces, materials  # ALWAYS THIS TUPLE
```

**Benefits**:
- Predictable interface for loop generation
- Easy composition (accumulate strings)
- Clear separation of concerns

### Pattern 2: Parametric Assembly Definitions

**External configuration file drives generation**:

```python
# input_definition.py
assemblies = {
    1: ['01', '02', '03', ..., '36'],  # Layer 1: 36 assemblies
    2: ['01', '02_C', '03', ..., '36_C'],  # Layer 2: fuel + control
    3: ['01', '02', '03_C', ..., '36'],  # Layer 3: different pattern
    4: ['01_C', '02', '03', ..., '36_C'],  # Layer 4: control positions
}
```

**Assembly naming convention**:
- `'01'` = fuel assembly #01
- `'02_C'` = control assembly #02
- `'R'` suffix = reflector position

**Benefits**:
- Core configuration separate from geometry code
- Easy variant creation (change dictionary, regenerate)
- Visual pattern representation

### Pattern 3: Loop-Based Core Generation

**Systematic assembly over all positions**:

```python
cells = ""
surfaces = ""
materials = ""

for layer, asse_list in assemblies.items():
    for asse in asse_list:
        # Parse assembly type
        sp = asse.split('_')

        if len(sp) == 2 and sp[1] == 'C':
            # Control assembly
            c, s, m = control(layer, sp[0])
        else:
            # Fuel assembly
            c, s, m = fuel(layer, sp[0])

        # Accumulate
        cells += c
        surfaces += s
        materials += m
```

**Result**: 144 assemblies generated from 4 functions

### Pattern 4: Systematic Numbering Encoding

**Hierarchy embedded in numbers**:

```python
def fuel(layer, number):
    n = f"{layer+1}{number:02d}"  # e.g., "201" for layer 2, assy 01

    # Cell numbers: n001, n002, ...
    # Surface numbers: n01, n02, ...
    # Material numbers: n1, n2, ...
    # Universe numbers: n0, n1, n4, n8, ...
```

**Example**:
- Layer 2, Assembly 15 → `n = "215"`
- Kernel cell: `21501`
- Kernel surface: `21501`
- Kernel material: `2151`
- Kernel universe: `2154`

**Benefits**:
- Zero numbering conflicts
- Location instantly identifiable
- Enables automated generation

### Pattern 5: Model Variant Generation

**SAME core geometry, DIFFERENT boundary conditions**:

```python
# generate_burnup.py
# Core generation (IDENTICAL)
for layer, asse_list in assemblies.items():
    for asse in asse_list:
        c, s, m = fuel_or_control(layer, asse)
        cells += c
        surfaces += s
        materials += m

# Boundary: reflector only
cells += reflector_cells
materials += reflector_materials
# NO SHIELD

# generate_sdr.py
# Core generation (IDENTICAL - same code!)
for layer, asse_list in assemblies.items():
    for asse in asse_list:
        c, s, m = fuel_or_control(layer, asse)
        cells += c
        surfaces += s
        materials += m

# Boundary: reflector + shield + room
cells += reflector_cells + shield_cells + room_cells
materials += reflector_materials + shield_materials + air
```

**Benefits**:
- Core geometry guaranteed consistent
- Changes propagate to all variants
- Single source of truth

---

## SKILL STRUCTURE

### Location
```
.claude/skills/mcnp-programmatic-generator/
├── SKILL.md
├── function_patterns_reference.md
├── parametric_design_guide.md
├── systematic_numbering_reference.md
├── scripts/
│   ├── assembly_template_generator.py
│   └── numbering_scheme_validator.py
└── example_inputs/
    ├── simple_core_parametric/
    │   ├── input_definition.py
    │   ├── generate_model.py
    │   └── README.md
    └── microreactor_example/
        ├── input_definition.py
        ├── generate_burnup.py
        ├── generate_sdr.py
        └── README.md
```

### Why This Skill Is Essential

**Current Gap**: Users have NO guidance on:
- How to structure function-based geometry generation
- How to create maintainable parametric designs
- How to generate multiple model variants consistently
- How to systematically number complex geometries

**Skills Ecosystem**:
```
mcnp-template-generator    → Time-series, operational history
mcnp-programmatic-generator → Parametric designs, model variants (THIS SKILL)
mcnp-geometry-builder      → Individual geometry components
mcnp-lattice-builder       → Lattice structures
mcnp-material-builder      → Material definitions
```

---

## SKILL.md CONTENT

### File: `.claude/skills/mcnp-programmatic-generator/SKILL.md`

```markdown
# MCNP Programmatic Generator

Generate MCNP inputs using Python functions for parametric reactor designs and model variants.

## When to Use This Skill

**Use programmatic generation when**:
- ✅ Building parametric reactor designs (geometry varies with parameters)
- ✅ Creating multiple model variants (burnup, shielding, criticality from same core)
- ✅ Systematic assembly replication (100+ fuel assemblies)
- ✅ Design space exploration (automated parameter sweeps)
- ✅ Maintaining consistency across related models

**Use template-based generation when**:
- ✅ Multi-cycle time-series (reactor operational history)
- ✅ Fixed geometry with time-varying parameters
- ✅ External data drives input (CSV files)

**Many projects use BOTH approaches together.**

## Core Concepts

### 1. Consistent Function Interface

**CRITICAL PATTERN**: All geometry functions return `(cells, surfaces, materials)` tuple

```python
def fuel_assembly(layer, number, enrichment=4.5):
    """
    Generate fuel assembly geometry

    Args:
        layer: Axial layer number (1-4)
        number: Assembly number in layer (01-36)
        enrichment: U-235 enrichment (%)

    Returns:
        (cells_str, surfaces_str, materials_str)
    """
    # Calculate numbering
    n = f"{layer+1}{number:02d}"

    # Generate MCNP cards
    cells = f"""c Fuel assembly L{layer} N{number}
{n}01 {n}1 -10.2  -{n}01  u={n}0  imp:n=1  $ UO2 fuel
{n}02 {n}2 -6.5   {n}01 -{n}02  u={n}0  imp:n=1  $ Clad
{n}03 {n}3 -1.0   {n}02  u={n}0  imp:n=1  $ Coolant
"""

    surfaces = f"""c Fuel assembly surfaces
{n}01 cz  0.41   $ Fuel radius
{n}02 cz  0.48   $ Clad radius
"""

    # Calculate isotopic fractions from enrichment
    u235_frac = enrichment / 100.0
    u238_frac = 1.0 - u235_frac

    materials = f"""m{n}1  $ UO2, {enrichment}% enriched
   92235.70c  {u235_frac:.6f}
   92238.70c  {u238_frac:.6f}
    8016.70c  2.0
c
m{n}2  $ Zircaloy clad
   40000.60c  1.0
c
m{n}3  $ Water coolant
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials
```

**Why this pattern?**
- Predictable: All functions work the same way
- Composable: Easy to accumulate in loops
- Testable: Each function can be validated independently
- Clear: Separation of cells, surfaces, materials

### 2. Parametric Assembly Definitions

**External configuration drives core layout**:

```python
# input_definition.py

# Core configuration
assemblies = {
    1: ['01', '02', '03', '04', '05_C', '06', ..., '36'],  # 36 assemblies
    2: ['01', '02_C', '03', '04', '05', '06_C', ..., '36'],
    3: ['01', '02', '03_C', '04', '05', '06', ..., '36_C'],
    4: ['01_C', '02', '03', '04_C', '05', '06', ..., '36'],
}

# Assembly-specific parameters
fuel_enrichments = {
    '01': 4.5,  # %
    '02': 4.5,
    '03': 5.0,  # Higher enrichment
    # ...
}

control_positions = {
    '05_C': 'withdrawn',
    '02_C': 'inserted',
    # ...
}

# Geometry parameters
fuel_radius = 0.41  # cm
clad_radius = 0.48  # cm
pitch = 1.26  # cm
```

**Benefits**:
- Visual core layout representation
- Easy to modify (change enrichment, swap fuel/control)
- Version control friendly (text file)
- Non-programmers can understand structure

### 3. Loop-Based Generation

**Systematic core assembly**:

```python
# generate_model.py
import input_definition as indef

# Initialize
cells = """c
c Cells
c
"""
surfaces = """c
c Surfaces
c
"""
materials = """c
c Materials
c
"""

# Generate all assemblies
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        # Parse assembly type
        sp = asse.split('_')
        asse_num = sp[0]
        asse_type = sp[1] if len(sp) > 1 else 'F'  # F=fuel, C=control

        if asse_type == 'C':
            # Control assembly
            c, s, m = indef.control_assembly(layer, asse_num)
        else:
            # Fuel assembly
            enrich = indef.fuel_enrichments.get(asse_num, 4.5)  # Default 4.5%
            c, s, m = indef.fuel_assembly(layer, asse_num, enrich)

        # Accumulate
        cells += c
        surfaces += s
        materials += m

# Add reflector, boundaries, etc.
c_refl, s_refl, m_refl = indef.reflector()
cells += c_refl
surfaces += s_refl
materials += m_refl

# Write output
with open('reactor_model.i', 'w') as f:
    f.write(indef.header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(indef.physics)
```

**Result**: Full reactor model from compact parameter file

### 4. Systematic Numbering Schemes

**Encode hierarchy in ID numbers**:

```python
def calculate_ids(layer, number):
    """
    Generate systematic numbering for assembly

    Args:
        layer: 1-4 (axial layers)
        number: '01'-'36' (assembly position)

    Returns:
        dict with cell, surface, material, universe base IDs
    """
    base = int(f"{layer+1}{number}")  # e.g., 215 for layer 2, assy 15

    return {
        'cell_base': base * 100,      # 21500-21599
        'surface_base': base * 10,    # 2150-2159
        'material_base': base,        # 215
        'universe_fuel': base * 10,   # 2150
        'universe_pin': base * 10 + 4,  # 2154
    }
```

**Example Numbering**:
```
Layer 2, Assembly 15:
  Cells: 21501, 21502, 21503, ...
  Surfaces: 21501, 21502, 21503, ...
  Materials: 2151, 2152, 2153, ...
  Universes: 2150 (assembly), 2154 (pin), 2158 (lattice)
```

**Benefits**:
- Human readable (can decode by inspection)
- No conflicts (systematic assignment)
- Scalable (works for 1000+ assemblies)
- Debuggable (easy to find component from number)

### 5. Model Variant Generation

**Same core, different boundaries**:

```python
# generate_burnup.py
from core_geometry import generate_core, generate_reflector

cells, surfaces, materials = generate_core()
c_refl, s_refl, m_refl = generate_reflector()

# Burnup model: reflector only
with open('burnup_model.i', 'w') as f:
    f.write(header)
    f.write(cells + c_refl)
    f.write(surfaces + s_refl)
    f.write(materials + m_refl)
    f.write(physics_criticality)


# generate_shielding.py
from core_geometry import generate_core, generate_reflector
from shield_geometry import generate_shield, generate_room

cells, surfaces, materials = generate_core()
c_refl, s_refl, m_refl = generate_reflector()
c_shield, s_shield, m_shield = generate_shield()
c_room, s_room, m_room = generate_room()

# Shielding model: reflector + shield + room
with open('shielding_model.i', 'w') as f:
    f.write(header)
    f.write(cells + c_refl + c_shield + c_room)
    f.write(surfaces + s_refl + s_shield + s_room)
    f.write(materials + m_refl + m_shield + m_room)
    f.write(physics_fixed_source)
```

**Benefits**:
- Core geometry guaranteed identical
- Changes to fuel design propagate to all models
- Single source of truth
- Easy to add new variants

## Complete Working Example

See `example_inputs/simple_core_parametric/` for a complete 4-layer core model demonstrating all patterns.

## Advanced Patterns

### Hexagonal Lattice Assembly

```python
def hex_assembly(layer, number):
    """Generate hexagonal fuel assembly"""
    n = f"{layer+1}{number:02d}"

    # Hexagonal lattice of pins
    cells = f"""c Hex assembly {layer}-{number}
{n}00 0  -{n}00  u={n}0 lat=2  imp:n=1  fill=-6:6 -6:6 0:0
     {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4
      {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4
       ... (hexagonal pattern)
"""

    # Fuel pin universe
    cells += f"""c
{n}01 {n}1 -10.2  -{n}01  u={n}4  imp:n=1  $ Fuel
{n}02 {n}2 -6.5   {n}01 -{n}02  u={n}4  imp:n=1  $ Clad
{n}03 {n}3 -1.0   {n}02  u={n}4  imp:n=1  $ Coolant
"""

    surfaces = f"""c Pin surfaces
{n}01 cz  0.41
{n}02 cz  0.48
c
c Assembly boundary (RHP for hexagonal)
{n}00 rhp  0 0 0  0 0 68  0 1.6 0  $ Hex prism
"""

    materials = f"""m{n}1  $ UO2 fuel
[...]
"""

    return cells, surfaces, materials
```

### Multi-Level Nesting

```python
def triso_compact(layer, stack, compact):
    """Generate TRISO compact with particle lattice"""

    # Level 1: TRISO particle (5 shells)
    c_particle, s_particle, m_particle = triso_particle(layer, stack, compact)

    # Level 2: Particle lattice (15×15)
    c_lattice = generate_particle_lattice(layer, stack, compact)

    # Level 3: Compact vertical stack (1×1×31)
    c_compact = generate_compact_stack(layer, stack, compact)

    # Combine
    cells = c_particle + c_lattice + c_compact
    surfaces = s_particle
    materials = m_particle

    return cells, surfaces, materials
```

## Common Patterns Library

### Pattern 1: Parameter Sweep
```python
enrichments = [3.0, 4.0, 5.0, 6.0]

for enrich in enrichments:
    cells, surfaces, materials = generate_core(enrichment=enrich)

    with open(f'core_enrich_{enrich:.1f}.i', 'w') as f:
        f.write(header + cells + surfaces + materials + physics)
```

### Pattern 2: Assembly Variations
```python
def fuel_assembly(layer, number, variant='standard'):
    """Generate fuel assembly with variant types"""

    variants = {
        'standard': {'pitch': 1.26, 'fuel_r': 0.41, 'clad_r': 0.48},
        'compact': {'pitch': 1.10, 'fuel_r': 0.38, 'clad_r': 0.45},
        'extended': {'pitch': 1.40, 'fuel_r': 0.44, 'clad_r': 0.51},
    }

    params = variants[variant]

    # Use params to generate geometry
    # ...

    return cells, surfaces, materials
```

### Pattern 3: Conditional Geometry
```python
def control_assembly(layer, number, position='withdrawn'):
    """Generate control assembly with rod position"""

    if position == 'withdrawn':
        # Water in guide tube
        cells = f"{n}05 3 -1.0  -{n}05  u={n}0  imp:n=1  $ Water"
    elif position == 'inserted':
        # Control rod material (B4C)
        cells = f"{n}05 5 -2.5  -{n}05  u={n}0  imp:n=1  $ B4C"
    else:
        # Partially inserted (more complex)
        cells = generate_partial_insertion(position)

    # Surfaces, materials, ...

    return cells, surfaces, materials
```

## Validation and Testing

### Function Unit Tests
```python
def test_fuel_assembly():
    """Validate fuel assembly function"""
    c, s, m = fuel_assembly(1, '01', enrichment=4.5)

    # Check return types
    assert isinstance(c, str)
    assert isinstance(s, str)
    assert isinstance(m, str)

    # Check cell cards generated
    assert '10101' in c  # Expected cell number

    # Check material enrichment
    assert '4.5' in m or '0.045' in m

    print("✓ fuel_assembly() validated")

test_fuel_assembly()
```

### Numbering Conflict Detection
```python
def check_numbering_conflicts(cells_str):
    """Detect duplicate cell numbers"""
    cell_numbers = []
    for line in cells_str.split('\n'):
        if line.strip() and not line.strip().startswith('c'):
            parts = line.split()
            if parts:
                try:
                    cell_numbers.append(int(parts[0]))
                except ValueError:
                    pass

    duplicates = [n for n in cell_numbers if cell_numbers.count(n) > 1]
    if duplicates:
        print(f"ERROR: Duplicate cell numbers: {set(duplicates)}")
        return False

    print(f"✓ No conflicts ({len(cell_numbers)} unique cells)")
    return True
```

### Model Comparison
```python
def compare_models(file1, file2):
    """Compare core geometry in two model variants"""

    # Extract core cells from both files
    core1 = extract_core_cells(file1)
    core2 = extract_core_cells(file2)

    # Should be identical for consistency
    if core1 == core2:
        print("✓ Core geometry consistent between variants")
    else:
        print("ERROR: Core geometry differs!")
        show_differences(core1, core2)
```

## Best Practices

### 1. Separation of Concerns
```
input_definition.py    → Parameters, configuration
geometry_functions.py  → Geometry generation functions
generate_model.py      → Assembly script
```

### 2. Docstrings for All Functions
```python
def fuel_assembly(layer, number, enrichment=4.5):
    """
    Generate fuel assembly geometry

    Args:
        layer (int): Axial layer (1-4)
        number (str): Assembly position ('01'-'36')
        enrichment (float): U-235 enrichment (%)

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)

    Example:
        >>> c, s, m = fuel_assembly(2, '15', enrichment=5.0)
        >>> '21501' in c  # Cell 21501 generated
        True
    """
```

### 3. Consistent Formatting
```python
# Always use f-strings for readability
cells = f"""c Component description
{cell_id} {mat_id} {density}  -{surf_id}  u={univ_id}  imp:n=1
"""

# NOT:
cells = str(cell_id) + " " + str(mat_id) + " " + ...
```

### 4. Parametric Defaults
```python
def fuel_assembly(layer, number,
                  enrichment=4.5,
                  fuel_radius=0.41,
                  clad_radius=0.48,
                  clad_thickness=0.07):
    """Provide sensible defaults for all parameters"""
    # ...
```

### 5. Error Checking
```python
def fuel_assembly(layer, number, enrichment=4.5):
    # Validate inputs
    if not 1 <= layer <= 4:
        raise ValueError(f"Layer must be 1-4, got {layer}")

    if not 0.0 < enrichment < 100.0:
        raise ValueError(f"Enrichment must be 0-100%, got {enrichment}")

    # Generate geometry
    # ...
```

## Integration with Other Skills

### With mcnp-lattice-builder
```python
from mcnp_lattice_builder import calculate_fill_dimensions

def pin_lattice(n_pins_x, n_pins_y):
    # Use lattice skill's calculator
    dims = calculate_fill_dimensions(0, n_pins_x-1, 0, n_pins_y-1, 0, 0)

    cells = f"""
{cell_id} 0  -{surf_id}  u={univ_id} lat=1  fill={dims['fill_spec']}
     {' '.join(['100'] * dims['total_elements'])}
"""

    return cells, surfaces, materials
```

### With mcnp-material-builder
```python
from mcnp_material_builder import generate_uo2_material

def fuel_assembly(layer, number, enrichment):
    # Use material skill's generators
    mat_str = generate_uo2_material(
        mat_id=f"{layer+1}{number}1",
        enrichment=enrichment,
        density=10.2
    )

    materials = mat_str
    # ...
```

### With mcnp-geometry-builder
```python
from mcnp_geometry_builder import concentric_cylinders

def fuel_pin(pin_id):
    # Use geometry skill's templates
    cells, surfaces = concentric_cylinders(
        center=(0, 0),
        radii=[0.41, 0.48],
        materials=[f"{pin_id}1", f"{pin_id}2"],
        universe=f"{pin_id}4"
    )
    # ...
```

## Common Pitfalls and Fixes

| Pitfall | Problem | Fix |
|---------|---------|-----|
| **Inconsistent returns** | Some functions return dict, others tuple | Always return `(cells, surfaces, materials)` |
| **Numbering conflicts** | Duplicate IDs across assemblies | Use systematic encoding (layer + number) |
| **Hardcoded values** | Constants embedded in functions | Use parameter dictionaries |
| **String accumulation inefficiency** | `s = s + new` in loops | Use f-strings or list+join |
| **Missing validation** | No input checking | Add range checks, type checks |
| **Poor modularity** | One giant function | Break into components (pin → assembly → core) |
| **No testing** | Functions never validated | Add unit tests for each function |

## Reference Files

For detailed examples and advanced patterns:
- **function_patterns_reference.md** - Function design patterns catalog
- **parametric_design_guide.md** - Complete design workflow
- **systematic_numbering_reference.md** - Numbering scheme examples

## Example Files

### Simple Core (4 Layers, 144 Assemblies)
`example_inputs/simple_core_parametric/`

### Microreactor (HTGR-style)
`example_inputs/microreactor_example/`

## Success Criteria

After using this skill, you should be able to:
- ✅ Design function-based geometry generators
- ✅ Create parametric reactor models
- ✅ Generate multiple model variants consistently
- ✅ Implement systematic numbering schemes
- ✅ Build maintainable, scalable reactor models
- ✅ Validate generated inputs programmatically

---

**This skill is essential for complex reactor modeling where parametric variation and model consistency are critical.**
```

---

## FUNCTION PATTERNS REFERENCE

### File: `.claude/skills/mcnp-programmatic-generator/function_patterns_reference.md`

```markdown
# Function Patterns Reference
## Catalog of Proven Geometry Generation Patterns

This reference provides tested patterns for function-based MCNP generation.

---

## Pattern 1: Basic Assembly Function

```python
def fuel_assembly(layer, number, enrichment=4.5):
    """
    Generate standard fuel assembly

    Returns: (cells, surfaces, materials)
    """
    # 1. Calculate numbering
    n = f"{layer+1}{number:02d}"

    # 2. Generate cells
    cells = f"""c Fuel Assembly L{layer} N{number}
{n}01 {n}1 -10.2  -{n}01  u={n}0  imp:n=1  $ UO2 fuel
{n}02 {n}2 -6.5   {n}01 -{n}02  u={n}0  imp:n=1  $ Zr clad
{n}03 {n}3 -1.0   {n}02  u={n}0  imp:n=1  $ Water
"""

    # 3. Generate surfaces
    surfaces = f"""c Assembly surfaces
{n}01 cz  0.41   $ Fuel radius
{n}02 cz  0.48   $ Clad radius
"""

    # 4. Generate materials
    u235 = enrichment / 100.0
    u238 = 1.0 - u235

    materials = f"""m{n}1  $ UO2 {enrichment}% enriched
   92235.70c  {u235:.6f}
   92238.70c  {u238:.6f}
    8016.70c  2.0
c
m{n}2  $ Zircaloy clad
   40000.60c  1.0
c
m{n}3  $ Light water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials
```

**When to use**: Standard fuel assemblies with parametric enrichment

---

## Pattern 2: Multi-Component Assembly

```python
def control_assembly(layer, number, position='withdrawn'):
    """
    Generate control assembly with multiple components

    position: 'withdrawn', 'inserted', or float 0-100 (% insertion)
    """
    n = f"{layer+1}{number:02d}"

    # Guide tube (always present)
    cells = f"""c Control Assembly L{layer} N{number}
{n}01 {n}2 -6.5  -{n}01 {n}02  u={n}0  imp:n=1  $ Guide tube
"""

    surfaces = f"""c Control assembly surfaces
{n}01 cz  0.55   $ Guide tube inner
{n}02 cz  0.62   $ Guide tube outer
"""

    materials = f"""m{n}2  $ Stainless steel guide tube
   26000.50c  0.65
   24000.50c  0.18
   28000.50c  0.12
"""

    # Control rod (position-dependent)
    if position == 'inserted':
        cells += f"""{n}03 {n}4 -2.5  -{n}01  -{n}10  u={n}0  imp:n=1  $ B4C absorber
{n}04 {n}3 -1.0  -{n}01   {n}10  u={n}0  imp:n=1  $ Water above
"""
        surfaces += f"""{n}10 pz  150.0  $ Control rod tip
"""
        materials += f"""m{n}4  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    elif position == 'withdrawn':
        cells += f"""{n}03 {n}3 -1.0  -{n}01  u={n}0  imp:n=1  $ Water
"""
        materials += f"""m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    else:
        # Partial insertion (0-100%)
        insertion_cm = position * 2.0  # 200 cm full stroke
        cells += f"""{n}03 {n}4 -2.5  -{n}01  -{n}10  u={n}0  imp:n=1  $ B4C
{n}04 {n}3 -1.0  -{n}01   {n}10  u={n}0  imp:n=1  $ Water
"""
        surfaces += f"""{n}10 pz  {insertion_cm:.2f}  $ Partial insertion
"""
        materials += f"""m{n}4  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials
```

**When to use**: Assemblies with conditional geometry (control rods, instrumentation, etc.)

---

## Pattern 3: Lattice-Based Assembly

```python
def pin_lattice_assembly(layer, number, n_pins=17, pitch=1.26):
    """
    Generate assembly with pin lattice

    17×17 PWR-style assembly
    """
    n = f"{layer+1}{number:02d}"

    # Pin universe (u=n4)
    cells = f"""c Pin universe
{n}01 {n}1 -10.2  -{n}01  u={n}4  imp:n=1  $ Fuel
{n}02 {n}2 -6.5   {n}01 -{n}02  u={n}4  imp:n=1  $ Clad
{n}03 {n}3 -1.0   {n}02  u={n}4  imp:n=1  $ Water
c
c Pin lattice (u=n0)
{n}10 0  -{n}10  u={n}0 lat=1  imp:n=1  fill=-8:8 -8:8 0:0
"""

    # Generate 17×17 fill pattern (289 elements)
    fill_pattern = f"     {' '.join([f'{n}4'] * 17)}\n" * 17
    cells += fill_pattern

    # Calculate surface dimensions
    assy_half_width = n_pins * pitch / 2.0

    surfaces = f"""c Pin surfaces
{n}01 cz  0.41
{n}02 cz  0.48
c
c Lattice boundary
{n}10 rpp -{assy_half_width:.2f} {assy_half_width:.2f} -{assy_half_width:.2f} {assy_half_width:.2f} -180 180
"""

    materials = f"""m{n}1  $ UO2 fuel
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
c
m{n}2  $ Zircaloy
   40000.60c  1.0
c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials
```

**When to use**: Assemblies with repeated pin structures

---

## Pattern 4: Hexagonal Assembly

```python
def hex_assembly(layer, number, pitch=2.77, height=68):
    """
    Generate hexagonal assembly (HTGR-style)

    Args:
        layer: Axial layer
        number: Assembly number
        pitch: Hexagonal pitch (cm)
        height: Assembly height (cm)
    """
    n = f"{layer+1}{number:02d}"

    # Channel universe (u=n4)
    cells = f"""c Fuel channel universe
{n}01 {n}1 -1.8  -{n}01  u={n}4  imp:n=1  $ Fuel compact
{n}02 {n}2 -1.7   {n}01 -{n}02  u={n}4  imp:n=1  $ Graphite
c
c Hex lattice (u=n0)
{n}10 0  -{n}10  u={n}0 lat=2  imp:n=1  fill=-6:6 -6:6 0:0
"""

    # Hexagonal fill pattern (13×13)
    # Central region: fuel channels (u=n4)
    # Peripheral: graphite (u=n5)
    fill_pattern = f"""     {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5
      {n}5 {n}5 {n}5 {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5 {n}5 {n}5 {n}5
       {n}5 {n}5 {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5 {n}5 {n}5
        {n}5 {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5 {n}5
         {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5
          {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4
           {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5
            {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5
             {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5
              {n}5 {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5 {n}5
               {n}5 {n}5 {n}5 {n}4 {n}4 {n}4 {n}4 {n}4 {n}5 {n}5 {n}5
                {n}5 {n}5 {n}5 {n}5 {n}4 {n}4 {n}4 {n}5 {n}5 {n}5 {n}5
                 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5 {n}5
"""
    cells += fill_pattern

    # Graphite filler universe (u=n5)
    cells += f"""c
{n}20 {n}2 -1.7  -{n}02  u={n}5  imp:n=1  $ Graphite filler
"""

    # RHP surface for hexagonal boundary
    R = pitch / 1.732050808  # R from pitch

    surfaces = f"""c Channel surfaces
{n}01 cz  0.6   $ Fuel compact
{n}02 cz  0.7   $ Channel outer
c
c Hex boundary (RHP)
{n}10 rhp  0 0 0  0 0 {height}  0 {R:.3f} 0
"""

    materials = f"""m{n}1  $ Fuel compact (graphite matrix + fuel)
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}1 grph.18t
c
m{n}2  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}2 grph.18t
"""

    return cells, surfaces, materials
```

**When to use**: Hexagonal assemblies (HTGR, fast reactors, CANDU)

---

## Pattern 5: Multi-Level Nesting

```python
def nested_assembly(layer, number):
    """
    Generate assembly with 3 levels of nesting

    Level 1: Pellet
    Level 2: Pin
    Level 3: Assembly lattice
    """
    n = f"{layer+1}{number:02d}"

    # Level 1: Pellet universe (u=n6)
    cells = f"""c Pellet universe (Level 1)
{n}01 {n}1 -10.2  -{n}01  u={n}6  imp:n=1  $ UO2 pellet
{n}02  0         {n}01 -{n}02  u={n}6  imp:n=1  $ Gap
"""

    # Level 2: Pin universe (u=n4)
    cells += f"""c
c Pin universe (Level 2)
{n}10 0  -{n}10  u={n}4  fill={n}6  imp:n=1  $ Pellet stack
{n}11 {n}2 -6.5  {n}10 -{n}11  u={n}4  imp:n=1  $ Clad
{n}12 {n}3 -1.0  {n}11  u={n}4  imp:n=1  $ Coolant
"""

    # Level 3: Assembly lattice (u=n0)
    cells += f"""c
c Assembly lattice (Level 3)
{n}20 0  -{n}20  u={n}0 lat=1  imp:n=1  fill=-8:8 -8:8 0:0
"""

    # 17×17 pattern
    fill_pattern = f"     {' '.join([f'{n}4'] * 17)}\n" * 17
    cells += fill_pattern

    surfaces = f"""c Pellet surfaces
{n}01 cz  0.40   $ Pellet radius
{n}02 cz  0.41   $ Gap
c
c Pin surfaces
{n}10 cz  0.41   $ Fuel stack radius
{n}11 cz  0.48   $ Clad outer
c
c Assembly surface
{n}20 rpp -10.71 10.71 -10.71 10.71 -180 180
"""

    materials = f"""m{n}1  $ UO2 pellet
   92235.70c  0.045
   92238.70c  0.955
    8016.70c  2.0
c
m{n}2  $ Zircaloy clad
   40000.60c  1.0
c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials
```

**When to use**: Complex geometries requiring multiple levels of detail

---

[Additional patterns for TRISO, reflectors, shields, etc.]
```

---

## PARAMETRIC DESIGN GUIDE

### File: `.claude/skills/mcnp-programmatic-generator/parametric_design_guide.md`

```markdown
# Parametric Design Guide
## Complete Workflow for Function-Based Reactor Models

This guide walks through a complete parametric reactor design from concept to validated MCNP input.

---

## Step 1: Define Requirements

**Example: Small Modular Reactor (SMR)**
- 4 axial layers
- 36 assemblies per layer (6×6 grid)
- Mix of fuel and control assemblies
- Parametric enrichment (3-6%)
- Multiple model variants (criticality, shielding)

---

## Step 2: Create Parameter File

**File: `input_definition.py`**

```python
"""
SMR Parameter Definition
4 layers × 36 assemblies = 144 total positions
"""

# Core configuration
# Format: 'NN' = fuel assembly, 'NN_C' = control assembly
assemblies = {
    1: [  # Layer 1 (bottom)
        '01', '02', '03', '04', '05', '06',
        '07', '08_C', '09', '10', '11_C', '12',
        '13', '14', '15', '16', '17', '18',
        '19', '20', '21_C', '22', '23', '24',
        '25', '26', '27', '28', '29_C', '30',
        '31', '32', '33', '34', '35', '36',
    ],

    2: [  # Layer 2
        '01', '02', '03_C', '04', '05', '06',
        '07_C', '08', '09', '10', '11', '12_C',
        '13', '14', '15_C', '16', '17', '18',
        '19', '20_C', '21', '22', '23_C', '24',
        '25', '26_C', '27', '28', '29', '30',
        '31', '32', '33', '34_C', '35', '36',
    ],

    3: [  # Layer 3 (similar pattern)
        # ... 36 assemblies
    ],

    4: [  # Layer 4 (top, similar pattern)
        # ... 36 assemblies
    ],
}

# Assembly-specific parameters
fuel_enrichments = {
    # Central region: higher enrichment
    '15': 5.5, '16': 5.5, '21': 5.5, '22': 5.5,

    # Peripheral: lower enrichment
    '01': 3.5, '06': 3.5, '31': 3.5, '36': 3.5,

    # Default: 4.5%
}

control_positions = {
    # Layer 1
    ('1', '08_C'): 'withdrawn',
    ('1', '11_C'): 'withdrawn',
    ('1', '21_C'): 'inserted',
    ('1', '29_C'): 'withdrawn',

    # Layer 2
    ('2', '03_C'): 'inserted',
    # ... etc.
}

# Geometry parameters
fuel_radius = 0.41  # cm
clad_radius = 0.48  # cm
pellet_height = 1.0  # cm
active_height = 200  # cm
assembly_pitch = 21.5  # cm

# Material parameters
default_enrichment = 4.5  # %
uo2_density = 10.2  # g/cm³
zr_density = 6.5
water_temp = 350  # K

# Physics parameters
criticality_mode = True
fixed_source_mode = False
```

---

## Step 3: Create Geometry Functions

**File: `geometry_functions.py`**

```python
"""
Geometry generation functions for SMR
All functions return (cells, surfaces, materials)
"""

def fuel_assembly(layer, number, enrichment=None, params=None):
    """
    Generate fuel assembly

    Args:
        layer: 1-4
        number: '01'-'36'
        enrichment: U-235 % (default from params)
        params: Parameter dictionary (from input_definition)
    """
    import input_definition as indef

    if enrichment is None:
        enrichment = indef.fuel_enrichments.get(number, indef.default_enrichment)

    if params is None:
        params = indef

    # Calculate numbering
    n = f"{layer+1}{number:02d}"

    # Generate cells (simplified - single pin)
    cells = f"""c Fuel Assembly L{layer} N{number} E={enrichment}%
{n}01 {n}1 -{params.uo2_density:.1f}  -{n}01  u={n}0  imp:n=1  $ UO2 fuel
{n}02 {n}2 -{params.zr_density:.1f}   {n}01 -{n}02  u={n}0  imp:n=1  $ Zr clad
{n}03 {n}3 -1.0   {n}02  u={n}0  imp:n=1  $ Water coolant
"""

    # Generate surfaces
    surfaces = f"""c Assembly {layer}-{number} surfaces
{n}01 cz  {params.fuel_radius:.2f}
{n}02 cz  {params.clad_radius:.2f}
"""

    # Generate materials
    u235_frac = enrichment / 100.0
    u238_frac = 1.0 - u235_frac

    materials = f"""m{n}1  $ UO2 {enrichment:.1f}% enriched
   92235.70c  {u235_frac:.6f}
   92238.70c  {u238_frac:.6f}
    8016.70c  2.0
c
m{n}2  $ Zircaloy-4 clad
   40000.60c  0.98
   50000.42c  0.015
   26000.50c  0.005
c
m{n}3  $ Water at {params.water_temp}K
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials


def control_assembly(layer, number, position='withdrawn', params=None):
    """
    Generate control assembly with rod position

    position: 'withdrawn', 'inserted', or float 0-100 (%)
    """
    import input_definition as indef
    if params is None:
        params = indef

    n = f"{layer+1}{number:02d}"

    # Guide tube (always present)
    cells = f"""c Control Assembly L{layer} N{number} pos={position}
{n}01 {n}2 -8.0  -{n}01 {n}02  u={n}0  imp:n=1  $ SS guide tube
"""

    surfaces = f"""c Control assembly surfaces
{n}01 cz  0.55
{n}02 cz  0.62
"""

    materials = f"""m{n}2  $ SS304 guide tube
   26000.50c  0.70
   24000.50c  0.19
   28000.50c  0.10
"""

    # Control rod (position-dependent)
    if position == 'inserted':
        cells += f"""{n}03 {n}4 -2.5  -{n}01  u={n}0  imp:n=1  $ B4C absorber
"""
        materials += f"""c
m{n}4  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
"""

    elif position == 'withdrawn':
        cells += f"""{n}03 {n}3 -1.0  -{n}01  u={n}0  imp:n=1  $ Water
"""
        materials += f"""c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    else:
        # Partial insertion (0-100%)
        insertion_fraction = float(position) / 100.0
        insertion_height = insertion_fraction * params.active_height

        cells += f"""{n}03 {n}4 -2.5  -{n}01  -{n}10  u={n}0  imp:n=1  $ B4C
{n}04 {n}3 -1.0  -{n}01   {n}10  u={n}0  imp:n=1  $ Water above
"""
        surfaces += f"""{n}10 pz  {insertion_height:.2f}  $ Rod tip
"""
        materials += f"""c
m{n}4  $ B4C absorber
    5010.70c  0.72
    5011.70c  2.88
    6012.00c  1.0
c
m{n}3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt{n}3 lwtr.13t
"""

    return cells, surfaces, materials


def reflector(thickness=30.0):
    """Generate radial reflector"""

    cells = f"""c Radial reflector
9001 9001 -1.7  -9001 9002  imp:n=1  $ Graphite reflector
"""

    surfaces = f"""c Reflector surfaces
9001 cz  {150 + thickness:.1f}  $ Reflector outer radius
9002 cz  150.0  $ Core outer radius
"""

    materials = f"""m9001  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt9001 grph.18t
"""

    return cells, surfaces, materials


def shield_and_room():
    """Generate shield and containment (for SDR model only)"""

    cells = f"""c Shield and room
9010 9010 -2.35  -9010 9011  imp:n=1  imp:p=1  $ Concrete shield
9020 9020 -1.164e-03  -9020 9010  imp:n=1  imp:p=1  $ Air gap
9999  0   9020  imp:n=0  imp:p=0  $ Outside world
"""

    surfaces = f"""c Shield surfaces
9010 cz  250.0  $ Shield outer
9011 cz  180.0  $ Shield inner
9020 cz  300.0  $ Room boundary
"""

    materials = f"""m9010  $ Concrete (ORNL-02)
    1001.70c  0.0221
    6000.70c  0.002484
    8016.70c  0.5748
   11023.70c  0.01541
   12000.60c  0.002565
   13027.70c  0.01996
   14000.60c  0.3045
   19000.60c  0.01068
   20000.70c  0.04266
   26000.55c  0.00524
c
m9020  $ Air
    7014.80c  -0.755636
    8016.80c  -0.231475
   18000.59c  -0.012889
"""

    return cells, surfaces, materials
```

---

## Step 4: Create Generation Scripts

**File: `generate_criticality.py`**

```python
"""
Generate criticality (burnup) model
Core + reflector only
"""

import input_definition as indef
import geometry_functions as geom

# Initialize
header = """SMR Criticality Model
c Programmatically generated
c 4 layers × 36 assemblies = 144 positions
c
"""

cells = """c
c Cells
c
"""

surfaces = """c
c Surfaces
c
"""

materials = """c
c Materials
c
"""

# Generate all assemblies
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        # Parse assembly type
        sp = asse.split('_')
        asse_num = sp[0]
        asse_type = sp[1] if len(sp) > 1 else 'F'

        if asse_type == 'C':
            # Control assembly
            position = indef.control_positions.get((str(layer), asse), 'withdrawn')
            c, s, m = geom.control_assembly(layer, asse_num, position)
        else:
            # Fuel assembly
            enrich = indef.fuel_enrichments.get(asse_num, indef.default_enrichment)
            c, s, m = geom.fuel_assembly(layer, asse_num, enrich)

        cells += c
        surfaces += s
        materials += m

# Add reflector
c_refl, s_refl, m_refl = geom.reflector()
cells += c_refl
surfaces += s_refl
materials += m_refl

# Add physics cards
physics = """c
c Physics
c
mode n
kcode 10000 1.0 50 250
ksrc 0 0 0  10 10 50  -10 -10 -50
"""

# Write output
output_file = 'smr_criticality.i'
with open(output_file, 'w') as f:
    f.write(header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(physics)

print(f"✓ Generated: {output_file}")
```

**File: `generate_shielding.py`**

```python
"""
Generate shielding (SDR) model
Core + reflector + shield + room
"""

import input_definition as indef
import geometry_functions as geom

# Initialize (same as criticality)
header = """SMR Shielding Model
c Programmatically generated
c 4 layers × 36 assemblies + shield + room
c
"""

cells = """c
c Cells
c
"""

surfaces = """c
c Surfaces
c
"""

materials = """c
c Materials
c
"""

# Generate core (IDENTICAL to criticality model)
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        sp = asse.split('_')
        asse_num = sp[0]
        asse_type = sp[1] if len(sp) > 1 else 'F'

        if asse_type == 'C':
            position = indef.control_positions.get((str(layer), asse), 'withdrawn')
            c, s, m = geom.control_assembly(layer, asse_num, position)
        else:
            enrich = indef.fuel_enrichments.get(asse_num, indef.default_enrichment)
            c, s, m = geom.fuel_assembly(layer, asse_num, enrich)

        cells += c
        surfaces += s
        materials += m

# Add reflector
c_refl, s_refl, m_refl = geom.reflector()
cells += c_refl
surfaces += s_refl
materials += m_refl

# Add shield and room (different from criticality)
c_shield, s_shield, m_shield = geom.shield_and_room()
cells += c_shield
surfaces += s_shield
materials += m_shield

# Different physics (fixed source, photon transport)
physics = """c
c Physics
c
mode n p
sdef  pos=0 0 0  erg=2.0
f4:p  9020  $ Dose at room boundary
de4   0.01  0.03  0.1  0.3  1.0  3.0  10.0
df4   3.7e-6  5.3e-6  9.2e-6  1.5e-5  2.7e-5  3.8e-5  4.9e-5
"""

# Write output
output_file = 'smr_shielding.i'
with open(output_file, 'w') as f:
    f.write(header)
    f.write(cells)
    f.write(surfaces)
    f.write(materials)
    f.write(physics)

print(f"✓ Generated: {output_file}")
```

---

## Step 5: Validate Generated Inputs

**File: `validate_models.py`**

```python
"""
Validation script for generated models
"""

def extract_cell_numbers(filename):
    """Extract all cell numbers from MCNP input"""
    cell_nums = []
    in_cells = False

    with open(filename) as f:
        for line in f:
            stripped = line.strip()

            # Detect cell block
            if 'c Cells' in stripped or 'c cells' in stripped:
                in_cells = True
                continue

            # Detect surface block (end of cells)
            if 'c Surfaces' in stripped or 'c surfaces' in stripped:
                in_cells = False

            if in_cells and stripped and not stripped.startswith('c'):
                parts = stripped.split()
                if parts:
                    try:
                        cell_nums.append(int(parts[0]))
                    except ValueError:
                        pass

    return cell_nums


def check_numbering_conflicts(filename):
    """Check for duplicate cell numbers"""
    cell_nums = extract_cell_numbers(filename)

    duplicates = [n for n in cell_nums if cell_nums.count(n) > 1]

    if duplicates:
        print(f"❌ {filename}: CONFLICTS found: {set(duplicates)}")
        return False
    else:
        print(f"✓ {filename}: No conflicts ({len(cell_nums)} unique cells)")
        return True


def compare_core_geometry(file1, file2):
    """Verify core geometry is identical in two models"""

    def extract_core_cells(filename):
        """Extract core assembly cells (2XXX-5XXX range)"""
        core_lines = []

        with open(filename) as f:
            for line in f:
                parts = line.strip().split()
                if parts and not parts[0].startswith('c'):
                    try:
                        cell_num = int(parts[0])
                        if 2000 <= cell_num < 6000:
                            core_lines.append(line.strip())
                    except ValueError:
                        pass

        return sorted(core_lines)

    core1 = extract_core_cells(file1)
    core2 = extract_core_cells(file2)

    if core1 == core2:
        print(f"✓ Core geometry IDENTICAL between {file1} and {file2}")
        return True
    else:
        print(f"❌ Core geometry DIFFERS!")
        print(f"   {file1}: {len(core1)} core cells")
        print(f"   {file2}: {len(core2)} core cells")

        # Show first difference
        for i, (line1, line2) in enumerate(zip(core1, core2)):
            if line1 != line2:
                print(f"   First difference at line {i}:")
                print(f"     {file1}: {line1}")
                print(f"     {file2}: {line2}")
                break

        return False


def validate_enrichments():
    """Check enrichments are in valid range"""
    import input_definition as indef

    errors = []
    for asse_num, enrich in indef.fuel_enrichments.items():
        if not 0.0 < enrich < 20.0:
            errors.append(f"Assembly {asse_num}: enrichment {enrich}% out of range")

    if errors:
        print("❌ Enrichment errors:")
        for e in errors:
            print(f"   {e}")
        return False
    else:
        print("✓ All enrichments valid")
        return True


# Run validations
print("=" * 60)
print("Model Validation")
print("=" * 60)

print("\n1. Checking numbering conflicts...")
check_numbering_conflicts('smr_criticality.i')
check_numbering_conflicts('smr_shielding.i')

print("\n2. Comparing core geometry consistency...")
compare_core_geometry('smr_criticality.i', 'smr_shielding.i')

print("\n3. Validating parameters...")
validate_enrichments()

print("\n" + "=" * 60)
print("Validation complete")
print("=" * 60)
```

---

## Step 6: Parameter Sweep (Optional)

**File: `parameter_sweep.py`**

```python
"""
Generate multiple models with varying enrichment
"""

import input_definition as indef
import geometry_functions as geom

enrichments = [3.0, 4.0, 5.0, 6.0]

for base_enrich in enrichments:
    # Override default enrichment
    indef.default_enrichment = base_enrich

    # Regenerate (same code as generate_criticality.py)
    cells = ""
    surfaces = ""
    materials = ""

    for layer, asse_list in indef.assemblies.items():
        for asse in asse_list:
            sp = asse.split('_')
            asse_num = sp[0]
            asse_type = sp[1] if len(sp) > 1 else 'F'

            if asse_type == 'C':
                position = indef.control_positions.get((str(layer), asse), 'withdrawn')
                c, s, m = geom.control_assembly(layer, asse_num, position)
            else:
                # Use sweep enrichment (unless specific override)
                enrich = indef.fuel_enrichments.get(asse_num, base_enrich)
                c, s, m = geom.fuel_assembly(layer, asse_num, enrich)

            cells += c
            surfaces += s
            materials += m

    c_refl, s_refl, m_refl = geom.reflector()
    cells += c_refl
    surfaces += s_refl
    materials += m_refl

    # Write output
    filename = f'smr_enrich_{base_enrich:.1f}.i'
    with open(filename, 'w') as f:
        f.write(f"SMR Model - {base_enrich:.1f}% Base Enrichment\nc\n")
        f.write(cells)
        f.write(surfaces)
        f.write(materials)
        f.write("c\nmode n\nkcode 10000 1.0 50 250\nksrc 0 0 0\n")

    print(f"✓ Generated: {filename}")

print(f"\n✓ Parameter sweep complete: {len(enrichments)} models generated")
```

---

## Success Criteria

After completing this workflow, you should have:

- ✅ Parametric core definition (input_definition.py)
- ✅ Reusable geometry functions (geometry_functions.py)
- ✅ Multiple model variants (criticality, shielding)
- ✅ Validated inputs (no numbering conflicts)
- ✅ Guaranteed core consistency across variants
- ✅ Ability to generate parameter sweeps
- ✅ Maintainable, scalable codebase

**All changes propagate automatically from parameter file to all generated models.**
```

---

## EXAMPLE FILES

### File: `.claude/skills/mcnp-programmatic-generator/example_inputs/simple_core_parametric/README.md`

```markdown
# Simple Core Parametric Example

Demonstrates basic programmatic generation for a simple 4-layer reactor core.

## Files

- `input_definition.py` - Core parameters and configuration
- `geometry_functions.py` - Fuel and control assembly functions
- `generate_model.py` - Main generation script
- `validate.py` - Validation script

## Usage

```bash
python generate_model.py
python validate.py
```

## Model Details

- 4 axial layers
- 36 assemblies per layer (144 total)
- Mix of fuel (enrichment varies) and control assemblies
- Systematic numbering: layer+1 + number (e.g., 215 for layer 2, assy 15)

## Validation

Run `validate.py` to check:
- No numbering conflicts
- All enrichments in valid range
- Cell/surface/material cross-references
```

[Include complete working example files]

---

## SCRIPTS

### File: `.claude/skills/mcnp-programmatic-generator/scripts/assembly_template_generator.py`

```python
"""
Generate assembly function templates
Helps users create new assembly types quickly
"""

def generate_assembly_template(assembly_name, description=""):
    """
    Create a template function for a new assembly type

    Args:
        assembly_name: Name for the assembly (e.g., "fuel", "control", "reflector")
        description: Brief description of assembly

    Returns:
        Python function template as string
    """

    template = f'''def {assembly_name}_assembly(layer, number, **kwargs):
    """
    Generate {assembly_name} assembly

    {description}

    Args:
        layer (int): Axial layer (1-N)
        number (str): Assembly number ('01'-'NN')
        **kwargs: Additional parameters

    Returns:
        tuple: (cells_str, surfaces_str, materials_str)

    Example:
        >>> c, s, m = {assembly_name}_assembly(2, '15')
    """
    # Calculate numbering
    n = f"{{layer+1}}{{number:02d}}"

    # TODO: Define geometry parameters
    radius_1 = 0.41  # cm
    radius_2 = 0.48  # cm

    # Generate cells
    cells = f"""c {{assembly_name.capitalize()}} Assembly L{{layer}} N{{number}}
{{n}}01 {{n}}1 -10.0  -{{n}}01  u={{n}}0  imp:n=1  $ Component 1
{{n}}02 {{n}}2 -5.0   {{n}}01 -{{n}}02  u={{n}}0  imp:n=1  $ Component 2
{{n}}03 0     {{n}}02  u={{n}}0  imp:n=1  $ Outer region
"""

    # Generate surfaces
    surfaces = f"""c {{assembly_name.capitalize()}} assembly surfaces
{{n}}01 cz  {{radius_1:.2f}}  $ Inner radius
{{n}}02 cz  {{radius_2:.2f}}  $ Outer radius
"""

    # Generate materials
    materials = f"""m{{n}}1  $ Material 1 description
   [TODO: Add isotopes]
c
m{{n}}2  $ Material 2 description
   [TODO: Add isotopes]
"""

    return cells, surfaces, materials
'''

    return template


def generate_input_definition_template(n_layers, n_assemblies_per_layer):
    """
    Generate input_definition.py template

    Args:
        n_layers: Number of axial layers
        n_assemblies_per_layer: Assemblies per layer
    """

    template = f'''"""
Reactor Parameter Definition
{n_layers} layers × {n_assemblies_per_layer} assemblies = {n_layers * n_assemblies_per_layer} total positions
"""

# Core configuration
# Format: 'NN' = fuel, 'NN_C' = control, 'NN_R' = reflector
assemblies = {{
'''

    for layer in range(1, n_layers + 1):
        assy_list = [f"'{i:02d}'" for i in range(1, n_assemblies_per_layer + 1)]
        template += f"    {layer}: [{', '.join(assy_list)}],\n"

    template += '''}

# Assembly-specific parameters
fuel_enrichments = {
    # Example: higher enrichment in center
    '15': 5.5,
    '16': 5.5,
    # Default: 4.5%
}

# Geometry parameters
fuel_radius = 0.41  # cm
clad_radius = 0.48  # cm
active_height = 200  # cm
assembly_pitch = 21.5  # cm

# Material parameters
default_enrichment = 4.5  # %
uo2_density = 10.2  # g/cm³
water_temp = 350  # K
'''

    return template


# Example usage
if __name__ == "__main__":
    print("Assembly Template Generator")
    print("=" * 60)

    # Generate fuel assembly template
    fuel_template = generate_assembly_template(
        "fuel",
        "Standard UO2 fuel assembly with clad and coolant"
    )

    print("\nFuel Assembly Function Template:")
    print(fuel_template)

    # Generate input definition template
    input_def = generate_input_definition_template(4, 36)

    print("\n" + "=" * 60)
    print("\nInput Definition Template:")
    print(input_def)
```

---

## VALIDATION TESTS

### Test 1: Basic Function Interface

**User asks**: "How do I create geometry functions for my reactor model?"

**Expected output**:
1. ✅ Explanation of consistent return interface: `(cells, surfaces, materials)`
2. ✅ Example fuel assembly function
3. ✅ Example control assembly function
4. ✅ Systematic numbering guidance
5. ✅ Reference to function_patterns_reference.md

### Test 2: Model Variant Generation

**User asks**: "I need to create both criticality and shielding models from the same core geometry"

**Expected output**:
1. ✅ Explanation of shared core generation
2. ✅ Example showing identical core code
3. ✅ Different boundary conditions (reflector vs. shield+room)
4. ✅ Different physics cards
5. ✅ Validation approach (compare core geometry)

### Test 3: Parameter Sweep

**User asks**: "How do I generate multiple models with different enrichments?"

**Expected output**:
1. ✅ Parameter sweep loop structure
2. ✅ Override default parameters
3. ✅ File naming convention
4. ✅ Example sweep script
5. ✅ Batch validation approach

---

## INTEGRATION WITH OTHER SKILLS

### mcnp-lattice-builder
- Use lattice dimension calculator in assembly functions
- Reference lattice patterns for pin arrays
- Validate lattice specifications

### mcnp-material-builder
- Use material generation functions for fuel, clad, coolant
- Apply thermal scattering automatically
- Generate burnup tracking materials

### mcnp-geometry-builder
- Use concentric cylinder generators for pins
- Apply geometric transformations
- Create complex assembly shapes

### mcnp-input-validator
- Validate numbering schemes
- Check cross-references
- Detect conflicts

---

## SUCCESS METRICS

After implementing this skill, users should be able to:

1. ✅ Design function-based geometry generators with consistent interfaces
2. ✅ Create parametric reactor core definitions
3. ✅ Generate multiple model variants from single codebase
4. ✅ Implement systematic numbering schemes (0 conflicts)
5. ✅ Perform parameter sweeps automatically
6. ✅ Validate generated inputs programmatically
7. ✅ Maintain complex reactor models efficiently
8. ✅ Scale to 1000+ assemblies without performance issues

**Overall**: Users can build and maintain production-quality reactor models using programmatic generation, complementing template-based approaches for complete workflow coverage.

---

**END OF REFINEMENT PLAN**
