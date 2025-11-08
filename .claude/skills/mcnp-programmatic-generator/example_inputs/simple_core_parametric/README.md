# Simple Core Parametric Example

Demonstrates basic programmatic generation for a simple 4-layer reactor core.

## Overview

This example shows how to build a parametric reactor model using function-based generation:
- **4 axial layers**
- **36 assemblies per layer** (144 total)
- **Mix of fuel and control assemblies**
- **Parametric enrichment** (3.5% to 5.5%)
- **Systematic numbering** scheme

## Files

- `input_definition.py` - Core parameters and configuration
- `geometry_functions.py` - Fuel and control assembly functions
- `generate_model.py` - Main generation script
- `validate.py` - Validation script

## Usage

### Generate the model

```bash
python generate_model.py
```

Output: `simple_core.i`

### Validate the model

```bash
python validate.py
```

Expected output:
```
============================================================
Model Validation
============================================================

1. Checking numbering conflicts...
✓ simple_core.i: No conflicts (146 unique cells)

2. Validating parameters...
✓ All enrichments valid

============================================================
Validation complete
============================================================
```

## Model Details

### Core Configuration

- **Layer 1 (bottom)**: 36 assemblies, 4 control rods
- **Layer 2**: 36 assemblies, 8 control rods
- **Layer 3**: 36 assemblies, 7 control rods
- **Layer 4 (top)**: 36 assemblies, 6 control rods

### Numbering Scheme

**Format**: `LNNCC`
- `L` = Layer + 1 (2-5 for layers 1-4)
- `NN` = Assembly number (01-36)
- `CC` = Component number (01-03)

**Examples**:
- Layer 2, Assembly 15: Cells 21501-21503
- Layer 3, Assembly 22: Cells 32201-32203

### Enrichment Zones

- **Central (assemblies 15, 16, 21, 22)**: 5.5%
- **Peripheral (assemblies 01, 06, 31, 36)**: 3.5%
- **Standard (all others)**: 4.5%

### Control Rod Positions

Mix of inserted and withdrawn rods for realistic control configuration.

## Modifying the Model

### Change enrichment

Edit `input_definition.py`:
```python
fuel_enrichments = {
    '15': 6.0,  # Changed from 5.5%
    # ...
}
```

Regenerate:
```bash
python generate_model.py
```

### Add new assembly

Edit `input_definition.py`:
```python
assemblies = {
    1: ['01', '02', '03', ..., '36', '37'],  # Added assembly 37
    # ...
}
```

Regenerate and the new assembly will be included.

### Change control rod position

Edit `input_definition.py`:
```python
control_positions = {
    ('1', '08_C'): 'inserted',  # Changed from 'withdrawn'
    # ...
}
```

## Key Patterns Demonstrated

1. **Consistent Function Interface**: All geometry functions return `(cells, surfaces, materials)`
2. **Parametric Configuration**: External parameter file drives generation
3. **Loop-Based Assembly**: Systematic iteration over all positions
4. **Systematic Numbering**: Encoded position information in IDs
5. **Input Validation**: Automatic conflict detection

## Next Steps

- Try modifying enrichments and regenerating
- Add new assembly types in `geometry_functions.py`
- Create variant models (e.g., different control configurations)
- Scale up to more assemblies

See the parent directory's documentation for more advanced patterns.
