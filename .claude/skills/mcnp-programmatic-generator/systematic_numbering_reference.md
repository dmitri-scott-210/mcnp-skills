# Systematic Numbering Reference
## Conflict-Free ID Assignment for Complex Geometries

This reference provides proven numbering schemes for programmatic MCNP generation.

---

## Core Principle

**Encode position information directly into ID numbers**

Instead of sequential numbering (1, 2, 3, ...), encode location:
- Layer number
- Assembly number
- Component type

**Result**: Zero numbering conflicts, human-readable IDs

---

## Scheme 1: Layer + Assembly Encoding

### Basic Pattern

```python
def calculate_base_id(layer, number):
    """
    layer: 1-4 (axial layers)
    number: '01'-'36' (assembly position)

    Returns: base ID (e.g., 215 for layer 2, assy 15)
    """
    return int(f"{layer+1}{number}")
```

### ID Ranges

**Layer 1, Assembly 01**: Base = 101
- Cells: 10101, 10102, 10103, ...
- Surfaces: 1011, 1012, 1013, ...
- Materials: 1011, 1012, 1013, ...
- Universes: 1010, 1014, 1018, ...

**Layer 2, Assembly 15**: Base = 215
- Cells: 21501, 21502, 21503, ...
- Surfaces: 2151, 2152, 2153, ...
- Materials: 2151, 2152, 2153, ...
- Universes: 2150, 2154, 2158, ...

**Layer 4, Assembly 36**: Base = 536
- Cells: 53601, 53602, 53603, ...
- Surfaces: 5361, 5362, 5363, ...
- Materials: 5361, 5362, 5363, ...
- Universes: 5360, 5364, 5368, ...

### Implementation

```python
def fuel_assembly(layer, number):
    """
    Generate fuel assembly with systematic numbering
    """
    n = f"{layer+1}{number:02d}"  # Base string

    # Cell numbers: add 2 digits (01-99)
    cells = f"""c Fuel Assembly {layer}-{number}
{n}01 {n}1 -10.2  -{n}01  u={n}0  imp:n=1  $ Fuel
{n}02 {n}2 -6.5   {n}01 -{n}02  u={n}0  imp:n=1  $ Clad
{n}03 {n}3 -1.0   {n}02  u={n}0  imp:n=1  $ Coolant
"""

    # Surface numbers: add 1 digit (1-9)
    surfaces = f"""c Assembly surfaces
{n}1 cz  0.41
{n}2 cz  0.48
"""

    # Material numbers: add 1 digit
    materials = f"""m{n}1  $ Fuel material
m{n}2  $ Clad material
m{n}3  $ Coolant material
"""

    return cells, surfaces, materials
```

**Capacity**:
- 9 layers × 99 assemblies = 891 assemblies
- 99 cells per assembly
- 9 surfaces per assembly
- 9 materials per assembly

---

## Scheme 2: Hierarchical Encoding

### For Multi-Level Structures

```python
def calculate_nested_id(layer, stack, compact):
    """
    layer: 1-4 (axial layer)
    stack: 1-31 (compact stack)
    compact: 1-15 (compact in stack)

    Returns: base ID
    """
    return int(f"{layer+1}{stack:02d}{compact:02d}")
```

### Example: TRISO Compact Structure

**Layer 2, Stack 15, Compact 07**: Base = 21507

- Particle cells: 2150701, 2150702, 2150703, ...
- Particle surfaces: 215071, 215072, 215073, ...
- Particle materials: 215071, 215072, ...

**Layer 3, Stack 01, Compact 03**: Base = 30103

- Particle cells: 3010301, 3010302, 3010303, ...
- Particle surfaces: 301031, 301032, 301033, ...

### Implementation

```python
def triso_compact(layer, stack, compact):
    """
    Generate TRISO compact with multi-level numbering
    """
    n = f"{layer+1}{stack:02d}{compact:02d}"

    # 5-layer TRISO particle
    cells = f"""c TRISO particle {layer}-{stack}-{compact}
{n}1 {n}1 -10.4  -{n}1  u={n}  imp:n=1  $ Kernel
{n}2 {n}2 -1.1   {n}1 -{n}2  u={n}  imp:n=1  $ Buffer
{n}3 {n}3 -1.9   {n}2 -{n}3  u={n}  imp:n=1  $ IPyC
{n}4 {n}4 -3.2   {n}3 -{n}4  u={n}  imp:n=1  $ SiC
{n}5 {n}5 -1.9   {n}4 -{n}5  u={n}  imp:n=1  $ OPyC
{n}6 {n}6 -1.7   {n}5  u={n}  imp:n=1  $ Matrix
"""

    surfaces = f"""c TRISO surfaces
{n}1 so  0.0250   $ Kernel
{n}2 so  0.0350   $ Buffer
{n}3 so  0.0390   $ IPyC
{n}4 so  0.0425   $ SiC
{n}5 so  0.0465   $ OPyC
"""

    # Materials use same base
    materials = f"""m{n}1  $ Kernel
m{n}2  $ Buffer
m{n}3  $ IPyC
m{n}4  $ SiC
m{n}5  $ OPyC
m{n}6  $ Matrix
"""

    return cells, surfaces, materials
```

**Capacity**: 9 layers × 99 stacks × 99 compacts = 87,813 unique positions

---

## Scheme 3: Reserved Ranges

### Global Components

Reserve specific ranges for non-assembly components:

```python
# Global numbering scheme
ASSEMBLY_RANGE = (1000, 8999)    # Assemblies: 1XXX-8XXX
REFLECTOR_RANGE = (9000, 9099)   # Reflectors: 9000-9099
SHIELD_RANGE = (9100, 9199)      # Shields: 9100-9199
VOID_RANGE = (9200, 9299)        # Void boundaries: 9200-9299
DETECTOR_RANGE = (9300, 9399)    # Detectors: 9300-9399
```

### Implementation

```python
def reflector():
    """Radial reflector - uses reserved range"""
    cells = f"""c Radial reflector
9001 9001 -1.7  -9001 9002  imp:n=1
"""
    surfaces = f"""c Reflector surfaces
9001 cz  180.0
9002 cz  150.0
"""
    materials = f"""m9001  $ Graphite
    6012.00c  0.9890
"""
    return cells, surfaces, materials


def shield():
    """Concrete shield - uses reserved range"""
    cells = f"""c Concrete shield
9101 9101 -2.35  -9101 9102  imp:n=1
"""
    surfaces = f"""c Shield surfaces
9101 cz  250.0
9102 cz  180.0
"""
    materials = f"""m9101  $ Concrete
[...]
"""
    return cells, surfaces, materials
```

**Benefits**:
- Clear separation of component types
- Easy to identify component from number
- No possibility of overlap

---

## Scheme 4: Universe Encoding

### Universe Numbering Strategy

**Problem**: Multiple universe levels need unique IDs

**Solution**: Encode level in universe number

```python
def calculate_universe_ids(base):
    """
    Generate universe IDs from base assembly ID

    Returns: dict of universe IDs for each level
    """
    return {
        'assembly': int(f"{base}0"),   # Level 0: assembly
        'pin': int(f"{base}4"),        # Level 1: pin
        'lattice': int(f"{base}8"),    # Level 2: lattice
        'particle': int(f"{base}6"),   # Level 1: particle (alternative)
    }
```

### Example

**Assembly 215** (Layer 2, Position 15):
- Assembly universe: 2150
- Pin universe: 2154
- Lattice universe: 2158
- Particle universe: 2156

### Implementation

```python
def pin_lattice_assembly(layer, number):
    """
    Multi-level universe structure
    """
    base = int(f"{layer+1}{number:02d}")
    u = calculate_universe_ids(base)

    # Pin universe (fills lattice)
    cells = f"""c Pin universe
{base}01 {base}1 -10.2  -{base}1  u={u['pin']}  imp:n=1  $ Fuel
{base}02 {base}2 -6.5   {base}1 -{base}2  u={u['pin']}  imp:n=1  $ Clad
{base}03 {base}3 -1.0   {base}2  u={u['pin']}  imp:n=1  $ Water
c
c Lattice universe (fills assembly)
{base}10 0  -{base}10  u={u['lattice']} lat=1  fill=-8:8 -8:8 0:0
     {' '.join([str(u['pin'])] * 17)}\n     ...
c
c Assembly universe (placed in core)
{base}20 0  -{base}20  u={u['assembly']}  fill={u['lattice']}  imp:n=1
"""

    surfaces = f"""c Surfaces
{base}1 cz  0.41
{base}2 cz  0.48
{base}10 rpp -10.71 10.71 -10.71 10.71 -180 180
{base}20 rpp -21.5 21.5 -21.5 21.5 -200 200
"""

    materials = """[...]"""

    return cells, surfaces, materials
```

**Benefits**:
- Clear hierarchy visible in numbers
- No universe conflicts
- Easy to debug (can identify level from ID)

---

## Scheme 5: Component Type Encoding

### Encode Component Type in ID

```python
def calculate_component_ids(layer, number, component_type):
    """
    component_type: 'fuel', 'control', 'reflector', 'instrumentation'

    Returns: base ID with type encoding
    """
    type_offsets = {
        'fuel': 0,
        'control': 100,
        'reflector': 200,
        'instrumentation': 300,
    }

    base = int(f"{layer+1}{number:02d}")
    return base + type_offsets[component_type]
```

### Example

**Layer 2, Position 15**:
- Fuel assembly: 215 (base)
- Control assembly: 315 (base + 100)
- Reflector: 415 (base + 200)
- Instrumentation: 515 (base + 300)

**Benefit**: Assembly type immediately visible from cell number

---

## Validation Tools

### Check for Numbering Conflicts

```python
def validate_numbering_scheme(cells_str):
    """
    Validate that numbering scheme produces no conflicts
    """
    cell_nums = []
    surf_nums = []
    mat_nums = []

    for line in cells_str.split('\n'):
        # Extract cell numbers
        parts = line.strip().split()
        if parts and not parts[0].startswith('c'):
            try:
                cell_nums.append(int(parts[0]))
            except ValueError:
                pass

    # Check for duplicates
    cell_dups = [n for n in cell_nums if cell_nums.count(n) > 1]

    if cell_dups:
        print(f"❌ CONFLICT: Duplicate cells: {set(cell_dups)}")
        return False
    else:
        print(f"✓ No conflicts ({len(cell_nums)} unique cells)")
        return True
```

### Decode ID to Position

```python
def decode_cell_id(cell_id):
    """
    Decode cell ID to position information

    Args:
        cell_id: MCNP cell number

    Returns:
        dict with layer, assembly, component info
    """
    cell_str = str(cell_id)

    # Extract components
    layer = int(cell_str[0]) - 1  # First digit - 1
    assembly = int(cell_str[1:3])  # Next 2 digits
    component = int(cell_str[3:])  # Remaining digits

    return {
        'layer': layer,
        'assembly': assembly,
        'component': component,
        'description': f"Layer {layer}, Assembly {assembly:02d}, Component {component}"
    }


# Example usage
info = decode_cell_id(21503)
print(info['description'])
# Output: "Layer 2, Assembly 15, Component 03"
```

### Generate Numbering Report

```python
def generate_numbering_report(cells_str):
    """
    Generate report of numbering usage
    """
    cell_nums = extract_cell_numbers(cells_str)

    # Analyze ranges
    min_id = min(cell_nums)
    max_id = max(cell_nums)
    total = len(cell_nums)

    # Count by layer
    by_layer = {}
    for cell_id in cell_nums:
        layer = str(cell_id)[0]
        by_layer[layer] = by_layer.get(layer, 0) + 1

    print("Numbering Report")
    print("=" * 60)
    print(f"Total cells: {total}")
    print(f"ID range: {min_id} - {max_id}")
    print(f"Capacity used: {total} / {max_id - min_id + 1}")
    print()
    print("By layer:")
    for layer, count in sorted(by_layer.items()):
        print(f"  Layer {int(layer)-1}: {count} cells")
```

---

## Best Practices

### 1. Choose Appropriate Depth

**Simple core (1 level)**:
```python
n = f"{layer+1}{number:02d}"  # 3 digits: LNN
```

**Complex core (2 levels)**:
```python
n = f"{layer+1}{ring:02d}{position:02d}"  # 5 digits: LRRPP
```

**Particle fuel (3 levels)**:
```python
n = f"{layer+1}{stack:02d}{compact:02d}"  # 5 digits: LSSCC
```

### 2. Document Your Scheme

```python
"""
Numbering Scheme Documentation

Base ID: LANN (4 digits)
  L = Layer + 1 (2-5 for layers 1-4)
  A = Assembly type offset (0=fuel, 1=control)
  NN = Assembly position (01-36)

Cell IDs: LANNCC (6 digits)
  CC = Component number (01-99)

Surface IDs: LANNC (5 digits)
  C = Surface number (1-9)

Material IDs: LANNC (5 digits)
  C = Material number (1-9)

Universe IDs: LANNU (5 digits)
  U = Universe level (0, 4, 8)

Examples:
  Layer 2, Fuel Assembly 15:
    Base: 2015
    Cells: 201501, 201502, 201503, ...
    Surfaces: 20151, 20152, 20153, ...
    Materials: 20151, 20152, 20153, ...
    Universes: 20150 (assembly), 20154 (pin), 20158 (lattice)
"""
```

### 3. Reserve Expansion Room

```python
# Leave gaps for future growth
ASSEMBLY_RANGE = (1000, 7999)    # Current assemblies
FUTURE_RANGE = (8000, 8999)      # Reserved for expansion
GLOBAL_RANGE = (9000, 9999)      # Global components
```

### 4. Validate During Generation

```python
def fuel_assembly(layer, number):
    # Validate inputs
    if not 1 <= layer <= 4:
        raise ValueError(f"Layer {layer} out of range (1-4)")

    if not 1 <= int(number) <= 36:
        raise ValueError(f"Assembly {number} out of range (01-36)")

    # Generate with confidence
    n = f"{layer+1}{number:02d}"
    # ...
```

---

## Common Pitfalls

### Pitfall 1: Insufficient Digits

**Problem**: `n = f"{layer}{number}"` → Conflict for layer 1, assy 23 vs. layer 12, assy 3

**Fix**: Pad with zeros: `n = f"{layer+1}{number:02d}"`

### Pitfall 2: Overlapping Ranges

**Problem**: Assemblies use 1-999, reflector uses 100-200

**Fix**: Reserve non-overlapping ranges (assemblies 1000-8999, global 9000+)

### Pitfall 3: Inconsistent Encoding

**Problem**: Some functions use `f"{layer}{number}"`, others use `f"{layer+1}{number}"`

**Fix**: Standardize across all functions

### Pitfall 4: Missing Components

**Problem**: Cell 21501 exists, but surface 21501 and material 21501 not generated

**Fix**: Ensure all cards use same base numbering

---

## Examples by Reactor Type

### PWR (4 layers × 36 assemblies)
```python
n = f"{layer+1}{number:02d}"  # Range: 101-536
```

### HTGR (4 layers × 31 stacks × 15 compacts)
```python
n = f"{layer+1}{stack:02d}{compact:02d}"  # Range: 10101-53115
```

### Fast Reactor (hexagonal, 6 rings × 60 positions)
```python
n = f"{ring:01d}{position:02d}"  # Range: 101-660
```

### Microreactor (4 layers × 100 assemblies)
```python
n = f"{layer+1}{number:03d}"  # Range: 1001-5100
```

---

**Systematic numbering eliminates conflicts and makes complex models maintainable.**
