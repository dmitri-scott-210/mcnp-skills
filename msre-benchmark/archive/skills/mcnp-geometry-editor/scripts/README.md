# MCNP Geometry Editor Scripts

**Purpose:** Automation tools for geometry editing operations

---

## Overview

This directory contains Python scripts for programmatic geometry editing operations:

1. **geometry_analyzer.py** - Parse and analyze existing geometry
2. **transformation_calculator.py** - Calculate TR card values
3. **volume_calculator.py** - Calculate volumes after scaling (TO BE CREATED)
4. **surface_editor.py** - Programmatic surface editing (TO BE CREATED)

---

## 1. geometry_analyzer.py

**Purpose:** Parse MCNP input and extract geometry structure

**Usage:**
```bash
python geometry_analyzer.py input.i
```

**Output:**
- Cell count and types
- Surface count and types
- Transformation cards detected
- Lattice structures
- Bounding box estimate

**Example:**
```bash
$ python geometry_analyzer.py simple_sphere.i

==============================================================
MCNP Geometry Analysis: simple_sphere.i
==============================================================

Title: Simple Sphere Model

Cells: 3
Surfaces: 2
Transformations: 0
Lattices: 0

--------------------------------------------------------------
CELLS
--------------------------------------------------------------
Cell 1: mat=1, rho=-1.0
Cell 2: mat=2, rho=-2.3
Cell 3: mat=0, rho=0.0

--------------------------------------------------------------
SURFACES
--------------------------------------------------------------
Surface 1: SO params=10.0
Surface 2: SO params=20.0

--------------------------------------------------------------
BOUNDING BOX ESTIMATE
--------------------------------------------------------------
Could not determine bounding box from SO surfaces (centered at origin)
```

**Use Case:**
- Before editing: Understand current geometry structure
- Identify all surfaces that need scaling
- Check for TR cards and dependencies
- Verify lattice structures before expansion

---

## 2. transformation_calculator.py

**Purpose:** Calculate MCNP *TR card values from rotations and translations

**Usage:**
```bash
# Translation only
python transformation_calculator.py --translate 10 0 0

# Rotation about single axis
python transformation_calculator.py --rotate-y 30

# Euler angles
python transformation_calculator.py --euler 30 45 60

# Combined rotation + translation
python transformation_calculator.py --euler 0 30 0 --translate 5 0 0

# Verify matrix validity
python transformation_calculator.py --euler 30 45 60 --verify
```

**Arguments:**
- `--tr N`: TR number (default: 1)
- `--translate DX DY DZ`: Translation vector
- `--euler RX RY RZ`: Euler angles (degrees)
- `--rotate-x ANGLE`: Rotation about x-axis (degrees)
- `--rotate-y ANGLE`: Rotation about y-axis (degrees)
- `--rotate-z ANGLE`: Rotation about z-axis (degrees)
- `--verify`: Verify rotation matrix validity

**Example:**
```bash
$ python transformation_calculator.py --euler 0 30 0 --translate 5 0 0 --tr 1

Euler angles: Roll=0°, Pitch=30°, Yaw=0°
Translation: dx=5, dy=0, dz=0

==============================================================
MCNP TR CARD
==============================================================

*TR1  5 0 0  0 30 0  1

Full Matrix Representation:
*TR1  5 0 0  \
       0.866025 0.000000 0.500000  \
       0.000000 1.000000 0.000000  \
       -0.500000 0.000000 0.866025
```

**Use Case:**
- Calculate TR card for component rotation
- Verify rotation matrix is valid (det=+1, orthonormal)
- Convert between Euler angles and matrix representation
- Quick reference for standard rotations

---

## 3. volume_calculator.py (TO BE CREATED)

**Purpose:** Calculate cell volumes after scaling

**Planned Usage:**
```bash
python volume_calculator.py input.i --scale 1.5
```

**Planned Features:**
- Parse cell definitions
- Calculate volumes for simple geometries
- Apply scale factor (uniform or non-uniform)
- Update VOL parameters automatically
- Generate modified input with updated volumes

---

## 4. surface_editor.py (TO BE CREATED)

**Purpose:** Programmatic batch editing of surfaces

**Planned Usage:**
```bash
# Scale all surfaces uniformly
python surface_editor.py input.i --scale 1.5 -o input_scaled.i

# Scale specific surface types
python surface_editor.py input.i --surface-type SO --scale-radius 2.0

# Translate all surfaces
python surface_editor.py input.i --translate 10 0 0
```

**Planned Features:**
- Scale individual or all surfaces
- Translate surfaces
- Batch parameter editing
- Validate edits before writing
- Generate backup of original

---

## Dependencies

All scripts require Python 3.6+ with NumPy:

```bash
pip install numpy
```

---

## Integration with MCNP Workflow

### Typical Editing Workflow:

```bash
# 1. Analyze current geometry
python geometry_analyzer.py original.i

# 2. Calculate required transformation
python transformation_calculator.py --euler 0 30 0 --translate 10 0 0 --tr 1

# 3. (Manual step) Edit input file with calculated TR card

# 4. (Future) Apply scaling programmatically
python surface_editor.py modified.i --scale 1.5 -o modified_scaled.i

# 5. (Future) Update volumes
python volume_calculator.py modified_scaled.i --scale 1.5

# 6. Run MCNP to verify
mcnp6 inp=modified_scaled.i ip  # Plot geometry
mcnp6 inp=modified_scaled.i n=1000  # Short test run
```

---

## Integration with mcnp-geometry-builder

These scripts are designed to work with outputs from **mcnp-geometry-builder**:

1. **geometry_analyzer.py** parses geometry created by geometry-builder
2. **transformation_calculator.py** calculates TR cards for repositioning geometry-builder outputs
3. **surface_editor.py** (planned) applies systematic edits to geometry-builder outputs
4. **volume_calculator.py** (planned) updates volumes after scaling geometry-builder outputs

**Example workflow:**
```
1. Use mcnp-geometry-builder to create initial geometry
2. Use geometry_analyzer.py to understand structure
3. Use transformation_calculator.py to calculate needed transformations
4. Edit geometry using calculated TR cards
5. Use surface_editor.py to apply batch modifications
6. Use volume_calculator.py to update VOL parameters
7. Verify with MCNP plot
```

---

## Error Handling

All scripts include basic error handling:
- Invalid file paths
- Malformed MCNP syntax
- Invalid transformation matrices (det ≠ +1)
- Missing required parameters

**Best Practice:** Always verify script output with MCNP geometry plot before running simulations.

---

## Contributing

When adding new scripts:
1. Follow Python naming conventions
2. Include docstring with usage examples
3. Add command-line interface with argparse
4. Update this README with usage documentation
5. Test with variety of MCNP inputs

---

## Future Enhancements

Planned additions:
- Boolean expression simplifier
- Lattice array generator
- Parametric geometry generator
- Geometry difference detector (compare two inputs)
- Surface sense validator

---

## References

- MCNP6 Manual Chapter 5: Geometry Specification
- mcnp-geometry-builder skill documentation
- transformation_specifications.md (in references/)
- surface_editing_guide.md (in references/)

---

**END OF README**
