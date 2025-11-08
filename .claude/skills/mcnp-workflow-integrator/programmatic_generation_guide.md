# Programmatic Generation Guide

Building MCNP inputs from scratch using Python functions.

## Overview

Programmatic generation builds MCNP inputs entirely from code, with no base template. This approach provides complete flexibility and is ideal for:
- Building models from scratch
- Algorithmic geometry (lattices, assemblies, symmetric patterns)
- Tight coupling between parameters
- Automated model variations

**Key Advantage**: Complete control over every aspect of the model.

---

## When to Use Programmatic Generation

✅ **Use programmatic approach when**:
- Building model from scratch
- Geometry follows algorithmic patterns
- Parameters are tightly coupled (changing one affects many)
- Need complete flexibility
- Model structure varies significantly between cases
- Extensive use of repeated structures/universes

❌ **Don't use programmatic when**:
- Large manual model already exists and works
- Only parameters change (use templates instead)
- Team unfamiliar with programming
- Simple one-off model

---

## Function-Based Geometry Generation

### Basic Pattern

**Core Principle**: Each geometric component is a function that returns (cells, surfaces, materials)

```python
def fuel_pin(number, x, y, radius=0.4095, enrichment=4.5):
    """
    Generate complete geometry for one fuel pin.

    Args:
        number: Pin identifier (for numbering)
        x, y: Pin center coordinates
        radius: Pin radius (cm)
        enrichment: U-235 enrichment (%)

    Returns:
        Tuple of (cells_str, surfaces_str, materials_str)
    """
    # Calculate material fractions
    u235_frac, u238_frac, o16_frac = calculate_uo2_fractions(enrichment)

    # Generate surfaces
    surfaces = f"""c Fuel pin {number}
{100 + number} c/z {x:.4f} {y:.4f} {radius:.4f}  $ Pin {number}
"""

    # Generate cells
    cells = f"""c Fuel pin {number}
{100 + number} {100 + number} -10.8  -{100 + number}  imp:n=1  $ Fuel pin {number}
"""

    # Generate materials
    materials = f"""m{100 + number}  $ UO2 fuel - Pin {number} ({enrichment}% U-235)
     92235.00c  {u235_frac:.6e}
     92238.00c  {u238_frac:.6e}
      8016.00c  {o16_frac:.6e}
"""

    return cells, surfaces, materials


def calculate_uo2_fractions(enrichment):
    """Calculate UO2 atom fractions for given enrichment."""
    # Simplified calculation
    u_total_atoms = 1.0
    o_atoms = 2.0

    u235_atoms = u_total_atoms * (enrichment / 100.0)
    u238_atoms = u_total_atoms * (1.0 - enrichment / 100.0)

    total = u235_atoms + u238_atoms + o_atoms

    return u235_atoms/total, u238_atoms/total, o_atoms/total
```

### Assembly Logic

**Build complex assemblies from component functions**:

```python
def hexagonal_fuel_assembly(assembly_id, center_x, center_y, pitch=1.26):
    """
    Generate hexagonal fuel assembly.

    Args:
        assembly_id: Assembly identifier (100s)
        center_x, center_y: Assembly center
        pitch: Pin-to-pin spacing

    Returns:
        Tuple of (cells, surfaces, materials)
    """
    cells_list = []
    surfaces_list = []
    materials_list = []

    # Generate pin positions (hexagonal array)
    pin_positions = generate_hex_positions(center_x, center_y, pitch, rings=3)

    # Generate each pin
    for i, (x, y) in enumerate(pin_positions):
        pin_id = assembly_id * 100 + i + 1

        c, s, m = fuel_pin(
            number=pin_id,
            x=x,
            y=y,
            radius=0.4095,
            enrichment=4.5
        )

        cells_list.append(c)
        surfaces_list.append(s)
        materials_list.append(m)

    # Assembly boundary
    hex_radius = pitch * 3.5  # Approximate
    assembly_surf = f"{assembly_id} rhp {center_x} {center_y} 0  0 0 100  0 {hex_radius} 0\n"
    surfaces_list.append(assembly_surf)

    # Assembly container cell
    assembly_cell = f"{assembly_id} 0  -{assembly_id}  fill={assembly_id}u  imp:n=1  $ Assembly {assembly_id}\n"
    cells_list.append(assembly_cell)

    # Combine all
    cells = ''.join(cells_list)
    surfaces = ''.join(surfaces_list)
    materials = ''.join(materials_list)

    return cells, surfaces, materials


def generate_hex_positions(center_x, center_y, pitch, rings):
    """
    Generate hexagonal array of positions.

    Args:
        center_x, center_y: Array center
        pitch: Spacing between positions
        rings: Number of hexagonal rings

    Returns:
        List of (x, y) tuples
    """
    positions = [(center_x, center_y)]  # Center position

    for ring in range(1, rings + 1):
        for i in range(6 * ring):  # 6 sides, ring positions per side
            angle = i * 60.0 / ring
            radius = ring * pitch

            x = center_x + radius * np.cos(np.radians(angle))
            y = center_y + radius * np.sin(np.radians(angle))

            positions.append((x, y))

    return positions
```

---

## TRISO Particle Model Example

**Complete hierarchical universe structure**:

```python
class TRISOParticle:
    """Generate TRISO particle geometry with multi-level universes."""

    def __init__(self, base_id, variant='baseline'):
        """
        Initialize TRISO particle generator.

        Args:
            base_id: Base numbering (e.g., 111 for capsule 1, stack 1, compact 1)
            variant: Particle variant ('baseline', 'variant1', 'variant2', 'variant3')
        """
        self.base_id = base_id
        self.variant = variant

        # Variant-specific parameters
        self.params = self._get_variant_params(variant)

    def _get_variant_params(self, variant):
        """Get variant-specific parameters."""
        variants = {
            'baseline': {
                'kernel_radius': 0.0250,
                'buffer_thickness': 0.0100,
                'ipyc_thickness': 0.0040,
                'sic_thickness': 0.0035,
                'opyc_thickness': 0.0040,
                'n_particles': 4154,
                'compact_radius': 0.6225,
                'compact_height': 2.54
            },
            'variant1': {
                'kernel_radius': 0.0175,
                'buffer_thickness': 0.0100,
                'ipyc_thickness': 0.0040,
                'sic_thickness': 0.0035,
                'opyc_thickness': 0.0040,
                'n_particles': 10510,
                'compact_radius': 0.6225,
                'compact_height': 2.54
            }
            # ... other variants
        }
        return variants[variant]

    def generate(self):
        """
        Generate complete TRISO particle hierarchy.

        Returns:
            Tuple of (cells, surfaces, materials)
        """
        # Level 1: TRISO particle (5 layers)
        particle_cells, particle_surfs, particle_mats = self._generate_particle()

        # Level 2: Matrix cell
        matrix_cells, matrix_surfs, matrix_mats = self._generate_matrix()

        # Level 3: Particle lattice (23×23×1)
        lattice_cells = self._generate_particle_lattice()

        # Level 4: Compact lattice (vertical stack)
        compact_cells = self._generate_compact_lattice()

        # Combine all
        cells = particle_cells + matrix_cells + lattice_cells + compact_cells
        surfaces = particle_surfs + matrix_surfs
        materials = particle_mats + matrix_mats

        return cells, surfaces, materials

    def _generate_particle(self):
        """Generate TRISO particle (Level 1: u=XXX4)."""
        p = self.params

        # Calculate radii
        r1 = p['kernel_radius']
        r2 = r1 + p['buffer_thickness']
        r3 = r2 + p['ipyc_thickness']
        r4 = r3 + p['sic_thickness']
        r5 = r4 + p['opyc_thickness']

        # Surface numbers
        s1 = f"{self.base_id}01"
        s2 = f"{self.base_id}02"
        s3 = f"{self.base_id}03"
        s4 = f"{self.base_id}04"
        s5 = f"{self.base_id}05"

        # Universe number
        u_particle = f"{self.base_id}4"

        surfaces = f"""c TRISO particle {self.base_id} ({self.variant})
{s1} so {r1:.4f}  $ Kernel
{s2} so {r2:.4f}  $ Buffer
{s3} so {r3:.4f}  $ IPyC
{s4} so {r4:.4f}  $ SiC
{s5} so {r5:.4f}  $ OPyC
"""

        cells = f"""c TRISO particle {self.base_id}
{self.base_id}01 {self.base_id}1 -10.8  -{s1}  u={u_particle} imp:n=1  $ Kernel
{self.base_id}02 {self.base_id}2  -1.1   {s1} -{s2}  u={u_particle} imp:n=1  $ Buffer
{self.base_id}03 {self.base_id}3  -1.9   {s2} -{s3}  u={u_particle} imp:n=1  $ IPyC
{self.base_id}04 {self.base_id}4  -3.2   {s3} -{s4}  u={u_particle} imp:n=1  $ SiC
{self.base_id}05 {self.base_id}5  -1.9   {s4} -{s5}  u={u_particle} imp:n=1  $ OPyC
{self.base_id}06 0                       {s5}        u={u_particle} imp:n=1  $ Outside
"""

        materials = f"""m{self.base_id}1  $ UO2 kernel
     92235.00c  4.816186e-03
     92238.00c  1.932238e-02
      8016.00c  4.827713e-02
m{self.base_id}2  $ Buffer (porous carbon)
      6000.00c  1.0
m{self.base_id}3  $ IPyC (pyrolytic carbon)
      6000.00c  1.0
m{self.base_id}4  $ SiC (silicon carbide)
     14028.00c  5.000e-01
      6000.00c  5.000e-01
m{self.base_id}5  $ OPyC (pyrolytic carbon)
      6000.00c  1.0
"""

        return cells, surfaces, materials

    def _generate_matrix(self):
        """Generate matrix cell (Level 2: u=XXX5)."""
        u_matrix = f"{self.base_id}5"

        cells = f"""c Matrix cell {self.base_id}
{self.base_id}10 {self.base_id}6 -1.73  u={u_matrix} imp:n=1  $ SiC matrix
"""

        materials = f"""m{self.base_id}6  $ SiC matrix
     14028.00c  5.000e-01
      6000.00c  5.000e-01
"""

        surfaces = ""  # No additional surfaces needed

        return cells, surfaces, materials

    def _generate_particle_lattice(self):
        """Generate particle lattice (Level 3: u=XXX6, lat=1)."""
        p = self.params

        # Calculate lattice pitch
        # Packing fraction = (n_particles * V_particle) / V_compact
        r_particle = p['kernel_radius'] + p['buffer_thickness'] + \
                     p['ipyc_thickness'] + p['sic_thickness'] + p['opyc_thickness']

        v_particle = (4.0/3.0) * np.pi * r_particle**3
        v_compact = np.pi * p['compact_radius']**2 * p['compact_height']

        packing_fraction = (p['n_particles'] * v_particle) / v_compact

        # Cubic lattice cell volume
        v_cubic_cell = v_particle / packing_fraction
        lattice_pitch = v_cubic_cell**(1.0/3.0)

        u_lattice = f"{self.base_id}6"
        u_particle = f"{self.base_id}4"
        u_matrix = f"{self.base_id}5"

        cells = f"""c Particle lattice {self.base_id} (23×23×1 cubic)
{self.base_id}20 0  u={u_lattice} lat=1 fill=-11:11 -11:11 0:0
         {' '.join([u_particle]*23*23*1)}  $ All cells contain particles
{self.base_id}21 0  u={u_lattice}7 lat=1 fill=-11:11 -11:11 0:0
         {' '.join([u_matrix]*23*23*1)}   $ Matrix cells (for boundary)
"""

        return cells

    def _generate_compact_lattice(self):
        """Generate compact lattice (Level 4: u=XXX8, vertical stack)."""
        p = self.params

        # Vertical lattice for compact stack
        u_compact = f"{self.base_id}8"
        u_lattice = f"{self.base_id}6"

        # Number of layers (simplified)
        n_layers = int(p['compact_height'] / 0.01)  # 1mm per layer

        cells = f"""c Compact lattice {self.base_id} (vertical stack)
{self.base_id}30 0  u={u_compact} lat=1 fill=0:0 0:0 -{n_layers//2}:{n_layers//2}
         {' '.join([u_lattice]*n_layers)}  $ Vertical stack of particle layers
"""

        return cells


def generate_complete_compact(capsule, stack, compact, variant='baseline'):
    """
    Generate complete compact geometry.

    Args:
        capsule, stack, compact: Compact identifiers
        variant: TRISO variant

    Returns:
        Tuple of (cells, surfaces, materials)
    """
    # Base numbering: capsule*100 + stack*10 + compact
    base_id = capsule*100 + stack*10 + compact

    # Generate TRISO hierarchy
    triso = TRISOParticle(base_id, variant)
    cells, surfaces, materials = triso.generate()

    # Add compact container
    compact_cells = f"""c Fuel compact {capsule}-{stack}-{compact}
{base_id}00 0  -{base_id}00  u={capsule}{stack}  fill={base_id}8  imp:n=1  $ Compact container
"""

    compact_surfaces = f"""c Compact {capsule}-{stack}-{compact} boundary
{base_id}00 c/z 0 0 0.6225  $ Compact radius
"""

    cells = compact_cells + cells
    surfaces = compact_surfaces + surfaces

    return cells, surfaces, materials
```

---

## Complete Model Generation

**Micro Reactor Example**:

```python
#!/usr/bin/env python3
"""
Generate Micro Reactor MCNP input.

Complete programmatic generation from parameters.
"""

import numpy as np
from pathlib import Path
from datetime import datetime


class MicroReactorGenerator:
    """Generate complete Micro Reactor MCNP model."""

    def __init__(self, config_file='input_definition.py'):
        """Load configuration parameters."""
        # Import configuration
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_file)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)

        self.config = config

        # Storage for accumulated geometry
        self.all_cells = []
        self.all_surfaces = []
        self.all_materials = []

    def generate(self, output_file='micro_reactor.i'):
        """Generate complete MCNP input."""

        print("Generating Micro Reactor MCNP input...")

        # Header
        self._add_header()

        # Geometry
        print("  Generating geometry...")
        self._generate_core()
        self._generate_reflector()
        self._generate_boundaries()

        # Data cards
        print("  Adding data cards...")
        self._add_data_cards()

        # Write output
        self._write_output(output_file)

        print(f"✓ Generated: {output_file}")

    def _add_header(self):
        """Add title and comment header."""
        header = f"""Micro Reactor Core Model
c
c Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
c Script: micro_reactor_generator.py
c Configuration: {self.config.REACTOR_NAME}
c
c Core: {self.config.N_LAYERS} axial layers × {self.config.N_ASSEMBLIES_PER_LAYER} assemblies
c Fuel: TRISO particles in graphite matrix
c
"""
        self.all_cells.append(header)

    def _generate_core(self):
        """Generate reactor core (4 layers × 36 assemblies)."""

        for layer in range(self.config.N_LAYERS):
            print(f"    Layer {layer+1}...")

            for assembly in range(self.config.N_ASSEMBLIES_PER_LAYER):
                # Determine assembly type (fuel, control, or reflector)
                asm_type = self._get_assembly_type(layer, assembly)

                if asm_type == 'fuel':
                    c, s, m = self._fuel_assembly(layer, assembly)
                elif asm_type == 'control':
                    c, s, m = self._control_assembly(layer, assembly)
                else:
                    c, s, m = self._reflector_assembly(layer, assembly)

                self.all_cells.append(c)
                self.all_surfaces.append(s)
                self.all_materials.append(m)

    def _fuel_assembly(self, layer, assembly):
        """Generate fuel assembly."""
        # Assembly numbering: (layer+1)*1000 + assembly
        asm_id = (layer + 1) * 1000 + assembly

        # Position
        x, y = self._get_assembly_position(layer, assembly)
        z = layer * self.config.LAYER_HEIGHT

        # Generate TRISO compact
        compact = generate_complete_compact(
            capsule=layer+1,
            stack=assembly//12,  # Simplified
            compact=assembly%4,
            variant='baseline'
        )

        # Wrap in assembly
        # ... (implementation continues)

        return cells, surfaces, materials

    def _control_assembly(self, layer, assembly):
        """Generate control assembly."""
        # Similar structure to fuel, but with control material
        # ... (implementation)
        pass

    def _reflector_assembly(self, layer, assembly):
        """Generate reflector assembly."""
        # Simplified - just graphite block
        # ... (implementation)
        pass

    def _get_assembly_type(self, layer, assembly):
        """Determine assembly type from configuration."""
        # Read from configuration matrix
        return self.config.CORE_LAYOUT[layer][assembly]

    def _get_assembly_position(self, layer, assembly):
        """Calculate assembly center position."""
        # Hexagonal packing
        pitch = self.config.ASSEMBLY_PITCH

        # ... hexagonal geometry calculation
        return x, y

    def _generate_reflector(self):
        """Generate radial reflector."""
        # Outer graphite reflector
        # ... (implementation)
        pass

    def _generate_boundaries(self):
        """Generate model boundaries."""
        # Outermost cells
        # ... (implementation)
        pass

    def _add_data_cards(self):
        """Add data cards section."""
        data_cards = f"""
c
c DATA CARDS
c
mode n
kcode 10000 1.0 50 250
ksrc {self.config.SOURCE_X} {self.config.SOURCE_Y} {self.config.SOURCE_Z}
c
c Tallies
f4:n ({' '.join(self.config.TALLY_CELLS)})
f7:n ({' '.join(self.config.TALLY_CELLS)})
"""
        self.all_cells.append(data_cards)

    def _write_output(self, output_file):
        """Write complete MCNP input to file."""

        # Combine all sections
        cells_block = '\n'.join(self.all_cells)
        surfaces_block = '\n'.join(self.all_surfaces)
        materials_block = '\n'.join(self.all_materials)

        # Write file
        with open(output_file, 'w') as f:
            f.write(cells_block)
            f.write("\n\nc\nc SURFACES\nc\n")
            f.write(surfaces_block)
            f.write("\n\nc\nc MATERIALS\nc\n")
            f.write(materials_block)


# Configuration file (input_definition.py)
"""
Micro Reactor Configuration Parameters
"""

REACTOR_NAME = "Micro HTGR"

# Core geometry
N_LAYERS = 4
N_ASSEMBLIES_PER_LAYER = 36
LAYER_HEIGHT = 68.0  # cm
ASSEMBLY_PITCH = 16.0  # cm (flat-to-flat)

# Core layout (F=fuel, C=control, R=reflector)
CORE_LAYOUT = [
    ['F']*36,  # Layer 1: all fuel
    ['F']*30 + ['C']*6,  # Layer 2: fuel + control
    ['F']*30 + ['C']*6,  # Layer 3: fuel + control
    ['F']*36   # Layer 4: all fuel
]

# Source position
SOURCE_X = 0.0
SOURCE_Y = 0.0
SOURCE_Z = 0.0

# Tally cells
TALLY_CELLS = ['1001', '1002', '1003']  # Example


# Execute
if __name__ == "__main__":
    generator = MicroReactorGenerator(config_file='input_definition.py')
    generator.generate(output_file='micro_reactor.i')
```

---

## Validation and Error Checking

**Built-in validation during generation**:

```python
def validate_triso_geometry(params):
    """Validate TRISO geometry parameters."""

    # Check radii increase monotonically
    radii = [
        params['kernel_radius'],
        params['kernel_radius'] + params['buffer_thickness'],
        # ... etc
    ]

    for i in range(len(radii)-1):
        assert radii[i] < radii[i+1], \
            f"Radius {i} not less than radius {i+1}: {radii[i]} >= {radii[i+1]}"

    # Check packing fraction < 1
    pf = calculate_packing_fraction(params)
    assert 0 < pf < 1, f"Invalid packing fraction: {pf}"

    # Check particle count > 0
    assert params['n_particles'] > 0, "Particle count must be positive"

    print("✓ TRISO geometry validated")


def calculate_packing_fraction(params):
    """Calculate and return packing fraction."""
    r_particle = (params['kernel_radius'] + params['buffer_thickness'] +
                  params['ipyc_thickness'] + params['sic_thickness'] +
                  params['opyc_thickness'])

    v_particle = (4.0/3.0) * np.pi * r_particle**3
    v_compact = np.pi * params['compact_radius']**2 * params['compact_height']

    pf = (params['n_particles'] * v_particle) / v_compact

    return pf
```

---

## Best Practices

### 1. Consistent Function Signatures

✅ **Good**:
```python
def fuel(layer, number):
    return cells, surfaces, materials

def control(layer, number):
    return cells, surfaces, materials

def reflector(layer, number):
    return cells, surfaces, materials
```

All functions return same structure → easy to use in loops.

### 2. Centralized Numbering

```python
class Numbering:
    """Centralized numbering system."""

    @staticmethod
    def cell(layer, assembly, component):
        return (layer+1)*10000 + assembly*100 + component

    @staticmethod
    def surface(layer, assembly, component):
        return (layer+1)*10000 + assembly*100 + component

    @staticmethod
    def material(layer, assembly):
        return (layer+1)*1000 + assembly

    @staticmethod
    def universe(layer, assembly, level):
        return (layer+1)*100 + assembly*10 + level


# Use consistent numbering
cell_num = Numbering.cell(layer=0, assembly=5, component=1)  # 1051
```

### 3. Parameter Validation

```python
def generate_assembly(layer, number, **kwargs):
    """Generate assembly with parameter validation."""

    # Validate inputs
    assert 0 <= layer < 4, f"Invalid layer: {layer}"
    assert 0 <= number < 36, f"Invalid assembly number: {number}"

    for key in kwargs:
        if key == 'enrichment':
            assert 0 < kwargs[key] < 100, f"Invalid enrichment: {kwargs[key]}"
        elif key == 'radius':
            assert kwargs[key] > 0, f"Radius must be positive: {kwargs[key]}"

    # Generate geometry
    # ...
```

### 4. Defensive Programming

```python
def generate_lattice_fill(dimensions, fill_pattern):
    """Generate lattice fill with dimension checking."""

    nx, ny, nz = dimensions

    expected_elements = nx * ny * nz
    actual_elements = len(fill_pattern)

    if expected_elements != actual_elements:
        raise ValueError(
            f"FILL dimension mismatch: "
            f"dimensions {dimensions} require {expected_elements} elements, "
            f"but {actual_elements} provided"
        )

    # Generate FILL card
    # ...
```

### 5. Comprehensive Comments

```python
def generate_surfaces(params):
    """
    Generate surface definitions.

    Args:
        params: Dictionary with keys:
            - 'radii': List of radii (increasing)
            - 'center': Tuple (x, y, z)
            - 'base_number': Starting surface number

    Returns:
        String with MCNP surface definitions

    Example:
        params = {
            'radii': [0.5, 1.0, 1.5],
            'center': (0, 0, 0),
            'base_number': 1000
        }
        surfaces = generate_surfaces(params)
    """
    # Implementation
    pass
```

---

## Summary

**Programmatic Approach**:

**Strengths**:
- Complete flexibility
- Algorithmic geometry natural (lattices, arrays)
- Tight parameter coupling handled elegantly
- Version control of logic, not just geometry
- Easy to generate variants

**Limitations**:
- Higher learning curve
- Requires programming expertise
- Harder to understand for non-programmers
- More complex debugging

**Best For**:
- New models built from scratch
- Algorithmic geometry (HTGR cores, lattices)
- Research codes requiring flexibility
- When model structure varies significantly

**Key Tools**:
- **Python**: Core language
- **numpy**: Numerical calculations
- **pathlib**: File management

**Next Steps**:
1. Define parameter structure (centralized configuration)
2. Create component functions (fuel, control, reflector)
3. Build assembly logic (combine components)
4. Implement validation (check all constraints)
5. Test with simple case first
6. Generate complete model
