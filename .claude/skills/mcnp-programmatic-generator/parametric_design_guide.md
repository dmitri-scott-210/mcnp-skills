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

    3: [  # Layer 3
        '01', '02', '03', '04_C', '05', '06',
        '07', '08', '09_C', '10', '11', '12',
        '13_C', '14', '15', '16', '17_C', '18',
        '19', '20', '21', '22_C', '23', '24',
        '25_C', '26', '27', '28', '29', '30_C',
        '31', '32', '33', '34', '35', '36',
    ],

    4: [  # Layer 4 (top)
        '01', '02_C', '03', '04', '05', '06',
        '07', '08', '09', '10_C', '11', '12',
        '13', '14', '15', '16_C', '17', '18',
        '19_C', '20', '21', '22', '23', '24',
        '25', '26', '27_C', '28', '29', '30',
        '31', '32_C', '33', '34', '35', '36',
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
    ('2', '07_C'): 'withdrawn',
    ('2', '12_C'): 'withdrawn',
    ('2', '15_C'): 'inserted',
    ('2', '20_C'): 'withdrawn',
    ('2', '23_C'): 'withdrawn',
    ('2', '26_C'): 'inserted',
    ('2', '34_C'): 'withdrawn',

    # Layer 3
    ('3', '04_C'): 'withdrawn',
    ('3', '09_C'): 'inserted',
    ('3', '13_C'): 'withdrawn',
    ('3', '17_C'): 'withdrawn',
    ('3', '22_C'): 'inserted',
    ('3', '25_C'): 'withdrawn',
    ('3', '30_C'): 'withdrawn',

    # Layer 4
    ('4', '02_C'): 'inserted',
    ('4', '10_C'): 'withdrawn',
    ('4', '16_C'): 'withdrawn',
    ('4', '19_C'): 'withdrawn',
    ('4', '27_C'): 'inserted',
    ('4', '32_C'): 'withdrawn',
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

## Step 7: Run Workflow

```bash
# Generate models
python generate_criticality.py
python generate_shielding.py

# Validate
python validate_models.py

# Optional: Parameter sweep
python parameter_sweep.py
```

**Expected Output**:
```
✓ Generated: smr_criticality.i
✓ Generated: smr_shielding.i

============================================================
Model Validation
============================================================

1. Checking numbering conflicts...
✓ smr_criticality.i: No conflicts (146 unique cells)
✓ smr_shielding.i: No conflicts (149 unique cells)

2. Comparing core geometry consistency...
✓ Core geometry IDENTICAL between smr_criticality.i and smr_shielding.i

3. Validating parameters...
✓ All enrichments valid

============================================================
Validation complete
============================================================
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

---

## Common Modifications

### Changing Enrichment

**Edit `input_definition.py`**:
```python
fuel_enrichments = {
    '15': 6.0,  # Changed from 5.5%
    # ...
}
```

**Regenerate**:
```bash
python generate_criticality.py
python generate_shielding.py
```

**Result**: Both models updated with new enrichment

### Adding New Assembly Type

**Edit `geometry_functions.py`**:
```python
def instrumentation_assembly(layer, number):
    """New assembly type"""
    n = f"{layer+1}{number:02d}"

    cells = f"""c Instrumentation Assembly
{n}01 0  -{n}01  u={n}0  imp:n=1  $ Void tube
"""

    surfaces = f"""c Instrumentation surfaces
{n}01 cz  0.50
"""

    materials = ""  # No materials

    return cells, surfaces, materials
```

**Edit `input_definition.py`**:
```python
assemblies = {
    1: ['01', '02', '03_I', ...],  # '03_I' = instrumentation
    # ...
}
```

**Edit generation scripts** to handle `'_I'` suffix

**Regenerate**: All models updated

### Modifying Core Layout

**Edit `input_definition.py`**:
```python
assemblies = {
    1: ['01', '02', '03', ..., '48'],  # Changed to 48 assemblies
    # ...
}
```

**Regenerate**: Core automatically expands

---

## Advanced Techniques

### Conditional Assembly Generation

```python
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        # Skip certain positions
        if asse == '18':
            continue  # Leave void

        # Generate normally
        # ...
```

### Assembly-Specific Modifications

```python
for layer, asse_list in indef.assemblies.items():
    for asse in asse_list:
        # Central assembly gets special treatment
        if asse == '18' or asse == '19':
            c, s, m = geom.fuel_assembly(layer, asse, enrichment=7.0)
        else:
            # Normal enrichment
            c, s, m = geom.fuel_assembly(layer, asse)
```

### Dynamic Material Assignment

```python
def fuel_assembly(layer, number, burnup=0.0):
    """Enrichment varies with burnup"""

    # Fresh fuel: high enrichment
    # Burned fuel: lower effective enrichment
    effective_enrich = 4.5 * (1.0 - burnup / 50.0)  # Simplified

    # Generate with effective enrichment
    # ...
```

---

## Troubleshooting

### Problem: Numbering Conflicts

**Symptom**: `validate_models.py` reports duplicate cell numbers

**Cause**: Inconsistent numbering scheme

**Fix**:
```python
# Ensure all functions use same scheme
n = f"{layer+1}{number:02d}"  # 2-digit layer, 2-digit number
```

### Problem: Core Geometry Differs

**Symptom**: Validation reports core geometry mismatch

**Cause**: Different generation code in two scripts

**Fix**: Extract core generation to shared function:
```python
# shared_generation.py
def generate_core():
    cells, surfaces, materials = "", "", ""
    for layer, asse_list in indef.assemblies.items():
        # ... (shared code)
    return cells, surfaces, materials

# Use in both scripts
from shared_generation import generate_core
cells, surfaces, materials = generate_core()
```

### Problem: Parameter Not Updating

**Symptom**: Changed enrichment doesn't appear in output

**Cause**: Using cached default instead of parameter

**Fix**:
```python
# WRONG:
enrichment = 4.5  # Hardcoded

# RIGHT:
enrichment = indef.fuel_enrichments.get(asse_num, indef.default_enrichment)
```

---

**This workflow ensures maintainable, consistent, and validated MCNP models for complex parametric reactor designs.**
