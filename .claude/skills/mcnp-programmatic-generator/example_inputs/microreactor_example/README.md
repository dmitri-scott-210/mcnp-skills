# Microreactor Example (HTGR-style)

Demonstrates programmatic generation for an HTGR-style microreactor with TRISO fuel.

## Overview

This example shows advanced programmatic patterns:
- **TRISO particle fuel** (5-layer coated particles)
- **Hexagonal lattices** (fuel channels in graphite blocks)
- **Multi-level nesting** (particle → compact → assembly)
- **Model variants** (burnup vs. shielding models)
- **Hierarchical numbering** (layer-stack-compact encoding)

## Files

- `input_definition.py` - Core parameters and assembly layout
- `generate_burnup.py` - Generate burnup (criticality) model
- `generate_sdr.py` - Generate shielding/dose rate model
- `README.md` - This file

## Key Patterns

### Pattern 1: TRISO Particle Generation

```python
def triso_particle(layer, stack, compact):
    """5-layer coated particle"""
    n = f"{layer+1}{stack:02d}{compact:02d}"

    # Kernel, buffer, IPyC, SiC, OPyC
    cells = f"""c TRISO particle
{n}1 {n}1 -10.4  -{n}1  u={n}  imp:n=1  $ Kernel
{n}2 {n}2 -1.1   {n}1 -{n}2  u={n}  imp:n=1  $ Buffer
{n}3 {n}3 -1.9   {n}2 -{n}3  u={n}  imp:n=1  $ IPyC
{n}4 {n}4 -3.2   {n}3 -{n}4  u={n}  imp:n=1  $ SiC
{n}5 {n}5 -1.9   {n}4 -{n}5  u={n}  imp:n=1  $ OPyC
"""

    surfaces = f"""c TRISO surfaces
{n}1 so  0.0250   $ Kernel (250 μm)
{n}2 so  0.0350   $ Buffer
{n}3 so  0.0390   $ IPyC
{n}4 so  0.0425   $ SiC
{n}5 so  0.0465   $ OPyC
"""

    return cells, surfaces, materials
```

### Pattern 2: Hexagonal Lattice Assembly

```python
def hex_fuel_block(layer, number):
    """Hexagonal fuel block with channels"""

    # Hexagonal lattice (lat=2)
    cells = f"""{n}10 0  -{n}10  u={n}0 lat=2  fill=-6:6 -6:6 0:0
     {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4
      {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4 {n}4
       ...
"""

    # RHP surface for hexagonal boundary
    surfaces = f"""{n}10 rhp  0 0 0  0 0 68  0 1.6 0
"""

    return cells, surfaces, materials
```

### Pattern 3: Model Variants

**Burnup Model** (burnup.py):
```python
# Core generation (identical in both models)
cells, surfaces, materials = generate_core()

# Boundary: reflector only
cells += reflector_cells
materials += reflector_materials

# Physics: criticality
physics = """mode n
kcode 10000 1.0 50 250
"""
```

**Shielding Model** (sdr.py):
```python
# Core generation (IDENTICAL code)
cells, surfaces, materials = generate_core()

# Boundary: reflector + shield + room
cells += reflector_cells + shield_cells + room_cells
materials += reflector_materials + shield_materials + air

# Physics: fixed source + photons
physics = """mode n p
sdef  pos=0 0 0  erg=2.0
"""
```

## Systematic Numbering

**Hierarchical encoding**: `LSSCC`
- `L` = Layer (1-4)
- `SS` = Stack number (01-31)
- `CC` = Compact number (01-15)

**Examples**:
- Layer 2, Stack 15, Compact 07: Base = 21507
  - Cells: 2150701, 2150702, 2150703, ...
  - Surfaces: 215071, 215072, 215073, ...

## Benefits of This Approach

1. **Guaranteed Consistency**: Core geometry IDENTICAL in both models
2. **Automatic Propagation**: Changes to fuel design update all variants
3. **Zero Conflicts**: Systematic numbering prevents ID collisions
4. **Scalable**: Handles 1000+ assemblies efficiently
5. **Maintainable**: Single source of truth for geometry

## Comparison with Template Approach

### This Example (Programmatic)
```
input_definition.py (100 lines)
  + generate_burnup.py (50 lines)
  + generate_sdr.py (50 lines)
  → 2 model variants, guaranteed consistent
```

**Best for**: Parametric designs, model variants, geometric variations

### Template Approach
```
bench.template (13,727 lines)
  + power.csv
  + create_inputs.py
  → 13 cycle-specific inputs
```

**Best for**: Time-series, operational history, fixed geometry

**Professional workflow**: Use BOTH approaches together

## Usage

### Generate burnup model

```bash
python generate_burnup.py
```

Output: `microreactor_burnup.i`

### Generate shielding model

```bash
python generate_sdr.py
```

Output: `microreactor_sdr.i`

### Verify consistency

```python
# Core geometry should be identical
core1 = extract_core_cells('microreactor_burnup.i')
core2 = extract_core_cells('microreactor_sdr.i')
assert core1 == core2  # ✓ PASS
```

## Key Lessons

1. **Function-based generation enables parametric designs**
2. **Systematic numbering eliminates conflicts**
3. **Shared core code guarantees consistency**
4. **Model variants from single codebase**
5. **Hierarchical numbering for complex structures**

See parent directory documentation for complete patterns and guides.
