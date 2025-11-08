# MCNP Programmatic Generator

Generate MCNP inputs using Python functions for parametric reactor designs and model variants.

## When to Use This Skill

**Use programmatic generation when**:
- Building parametric reactor designs (geometry varies with parameters)
- Creating multiple model variants (burnup, shielding, criticality from same core)
- Systematic assembly replication (100+ fuel assemblies)
- Design space exploration (automated parameter sweeps)
- Maintaining consistency across related models

**Use template-based generation when**:
- Multi-cycle time-series (reactor operational history)
- Fixed geometry with time-varying parameters
- External data drives input (CSV files)

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
- Design function-based geometry generators
- Create parametric reactor models
- Generate multiple model variants consistently
- Implement systematic numbering schemes
- Build maintainable, scalable reactor models
- Validate generated inputs programmatically

---

**This skill is essential for complex reactor modeling where parametric variation and model consistency are critical.**
