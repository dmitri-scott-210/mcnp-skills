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

## Pattern 6: TRISO Particle Assembly

```python
def triso_particle(layer, stack, particle):
    """
    Generate TRISO particle with 5-layer coating

    Args:
        layer: Axial layer (1-4)
        stack: Compact stack number (1-31)
        particle: Particle number (for unique ID)
    """
    # Unique numbering: layer_stack_particle
    n = f"{layer+1}{stack:02d}{particle:03d}"

    cells = f"""c TRISO particle {layer}-{stack}-{particle}
{n}1 {n}1 -10.4  -{n}1  u={n}  imp:n=1  $ Kernel (UO2)
{n}2 {n}2 -1.1   {n}1 -{n}2  u={n}  imp:n=1  $ Buffer (porous C)
{n}3 {n}3 -1.9   {n}2 -{n}3  u={n}  imp:n=1  $ IPyC
{n}4 {n}4 -3.2   {n}3 -{n}4  u={n}  imp:n=1  $ SiC
{n}5 {n}5 -1.9   {n}4 -{n}5  u={n}  imp:n=1  $ OPyC
{n}6 {n}6 -1.7   {n}5  u={n}  imp:n=1  $ Graphite matrix
"""

    surfaces = f"""c TRISO particle surfaces
{n}1 so  0.0250   $ Kernel (250 μm)
{n}2 so  0.0350   $ Buffer
{n}3 so  0.0390   $ IPyC
{n}4 so  0.0425   $ SiC
{n}5 so  0.0465   $ OPyC
"""

    materials = f"""m{n}1  $ UO2 kernel (19.7% enriched)
   92235.70c  4.816186e-03
   92238.70c  1.932238e-02
    8016.70c  4.896846e-02
c
m{n}2  $ Porous carbon buffer
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}2 grph.18t
c
m{n}3  $ Inner PyC
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}3 grph.18t
c
m{n}4  $ SiC coating
   14028.70c  0.9223
   14029.70c  0.0468
   14030.70c  0.0309
    6012.00c  1.0
c
m{n}5  $ Outer PyC
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}5 grph.18t
c
m{n}6  $ Graphite matrix
    6012.00c  0.9890
    6013.00c  0.0110
mt{n}6 grph.18t
"""

    return cells, surfaces, materials
```

**When to use**: TRISO fuel particles, coated particles

---

## Pattern 7: Reflector Components

```python
def radial_reflector(thickness=30.0, core_radius=150.0, material='graphite'):
    """
    Generate radial reflector

    Args:
        thickness: Reflector thickness (cm)
        core_radius: Core outer radius (cm)
        material: 'graphite', 'water', 'beryllium'
    """
    cells = f"""c Radial reflector
9001 9001 -DENSITY  -9001 9002  imp:n=1  $ Reflector
"""

    surfaces = f"""c Reflector surfaces
9001 cz  {core_radius + thickness:.1f}  $ Reflector outer
9002 cz  {core_radius:.1f}  $ Core outer
"""

    if material == 'graphite':
        cells = cells.replace('-DENSITY', '-1.7')
        materials = f"""m9001  $ Graphite reflector
    6012.00c  0.9890
    6013.00c  0.0110
mt9001 grph.18t
"""
    elif material == 'water':
        cells = cells.replace('-DENSITY', '-1.0')
        materials = f"""m9001  $ Water reflector
    1001.70c  2.0
    8016.70c  1.0
mt9001 lwtr.13t
"""
    elif material == 'beryllium':
        cells = cells.replace('-DENSITY', '-1.85')
        materials = f"""m9001  $ Beryllium reflector
    4009.70c  1.0
mt9001 be.60t
"""
    else:
        raise ValueError(f"Unknown reflector material: {material}")

    return cells, surfaces, materials
```

**When to use**: Core boundary reflectors

---

## Pattern 8: Shield and Containment

```python
def concrete_shield(inner_radius=180.0, thickness=70.0):
    """
    Generate concrete biological shield

    Args:
        inner_radius: Shield inner radius (cm)
        thickness: Shield thickness (cm)
    """
    outer_radius = inner_radius + thickness

    cells = f"""c Concrete biological shield
9010 9010 -2.35  -9010 9011  imp:n=1  imp:p=1  $ Concrete
9020 9020 -1.164e-03  -9020 9010  imp:n=1  imp:p=1  $ Air gap
9999  0   9020  imp:n=0  imp:p=0  $ Outside world
"""

    surfaces = f"""c Shield surfaces
9010 cz  {outer_radius:.1f}  $ Shield outer
9011 cz  {inner_radius:.1f}  $ Shield inner
9020 cz  {outer_radius + 50:.1f}  $ Room boundary
"""

    materials = f"""m9010  $ Ordinary concrete (ORNL-02)
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
m9020  $ Air (dry, sea level)
    7014.80c  -0.755636
    8016.80c  -0.231475
   18000.59c  -0.012889
"""

    return cells, surfaces, materials
```

**When to use**: Shielding models, dose rate calculations

---

## Usage Guidelines

### Choosing the Right Pattern

1. **Simple cylindrical assembly** → Pattern 1 (Basic)
2. **Assembly with moving parts** → Pattern 2 (Multi-Component)
3. **Pin bundle assembly** → Pattern 3 (Lattice-Based)
4. **Hexagonal reactor** → Pattern 4 (Hexagonal)
5. **Detailed fuel pin** → Pattern 5 (Multi-Level Nesting)
6. **Particle fuel** → Pattern 6 (TRISO)
7. **Core boundaries** → Pattern 7 (Reflector) or Pattern 8 (Shield)

### Combining Patterns

```python
def complete_reactor():
    """Combine multiple patterns"""

    # Core (Pattern 3: lattice assemblies)
    core_cells, core_surf, core_mat = generate_core_lattice()

    # Reflector (Pattern 7)
    refl_cells, refl_surf, refl_mat = radial_reflector()

    # Shield (Pattern 8)
    shield_cells, shield_surf, shield_mat = concrete_shield()

    # Combine
    return (
        core_cells + refl_cells + shield_cells,
        core_surf + refl_surf + shield_surf,
        core_mat + refl_mat + shield_mat
    )
```

### Testing Each Pattern

```python
def test_pattern(pattern_func, *args, **kwargs):
    """Generic pattern validator"""
    c, s, m = pattern_func(*args, **kwargs)

    assert isinstance(c, str), "Cells must be string"
    assert isinstance(s, str), "Surfaces must be string"
    assert isinstance(m, str), "Materials must be string"

    assert len(c) > 0, "Cells cannot be empty"

    print(f"✓ {pattern_func.__name__} validated")
    return True
```

---

**All patterns follow the consistent (cells, surfaces, materials) return interface for maximum composability.**
