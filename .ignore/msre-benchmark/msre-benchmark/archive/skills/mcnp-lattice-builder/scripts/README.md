# MCNP Lattice Builder - Scripts

## Overview

This directory contains Python helper scripts for MCNP lattice construction, verification, and validation. These tools assist with common lattice-related tasks that are tedious or error-prone when done manually.

## Scripts

### 1. lattice_index_calculator.py
**Purpose:** Calculate and visualize lattice indices based on surface ordering

**Usage:**
```bash
python lattice_index_calculator.py --type LAT1 --surfaces "10 11 12 13 14 15"
```

**Features:**
- LAT=1 (rectangular) and LAT=2 (hexagonal) support
- Visualizes index scheme (i, j, k directions)
- Identifies surface order from cell card
- Generates ASCII diagram of indices

**Example Output:**
```
LAT=1 Rectangular Lattice:
- Surface 10: -X direction (i=0 boundary)
- Surface 11: +X direction (i varies here)
- Surface 12: -Y direction (j=0 boundary)
- Surface 13: +Y direction (j varies here)
- Surface 14: -Z direction (k=0 boundary)
- Surface 15: +Z direction (k varies here)

Index increases: i in X, j in Y, k in Z
```

---

### 2. fill_array_generator.py
**Purpose:** Generate FILL array syntax from structured input

**Usage:**
```bash
python fill_array_generator.py --dims "0:2 0:2 0:0" --pattern "1 1 2 1 2 1 1 1 1"
```

**Features:**
- Validates array dimensions match value count
- Formats with Fortran ordering (i-fastest)
- Generates proper MCNP continuation lines
- Adds comments showing pattern

**Example Output:**
```
FILL=0:2 0:2 0:0
     1 1 2    $ j=0: i=0,1,2
     1 2 1    $ j=1: i=0,1,2
     1 1 1    $ j=2: i=0,1,2
```

---

### 3. universe_hierarchy_visualizer.py
**Purpose:** Parse MCNP input and visualize universe nesting

**Usage:**
```bash
python universe_hierarchy_visualizer.py input.i
```

**Features:**
- Extracts universe assignments (U parameter)
- Identifies FILL references
- Generates ASCII tree diagram
- Detects circular references (errors)
- Shows nesting depth

**Example Output:**
```
Universe Hierarchy:
U=0 (Real World)
 ├── U=100 (Core Lattice, LAT=1)
 │    └── U=10 (Assembly, LAT=1)
 │         ├── U=1 (Fuel Pin)
 │         └── U=2 (Guide Tube)
 └── U=200 (Reflector)

Maximum nesting depth: 4 levels
Total universes: 5
```

---

### 4. lattice_volume_checker.py
**Purpose:** Verify volume specifications for repeated structures

**Usage:**
```bash
python lattice_volume_checker.py input.i
```

**Features:**
- Identifies VOL parameters in universe cells
- Calculates total volume across all instances
- Compares per-instance vs total specifications
- Warns if volumes seem incorrect
- Estimates total fuel/material inventory

**Example Output:**
```
Cell 1 (Fuel, U=1):
  VOL specified: 0.503 cm³ (per instance) ✓
  Lattice instances: 289 (17×17×1)
  Total volume: 145.37 cm³

Warning: Typical fuel pin volume ~0.5 cm³, specified 0.503 ✓
```

---

### 5. surface_order_validator.py
**Purpose:** Check surface ordering on LAT cell cards

**Usage:**
```bash
python surface_order_validator.py input.i --cell 100
```

**Features:**
- Extracts surface list from LAT cell card
- Validates LAT=1 has 6 surfaces, LAT=2 has 8
- Interprets surface order as index directions
- Suggests corrections if ordering wrong
- Generates test plots commands

**Example Output:**
```
Cell 100: U=10 LAT=1
Surfaces: -10 11 -12 13 -14 15

Interpretation:
  Surfaces 10, 11 → i-index (X direction)
  Surfaces 12, 13 → j-index (Y direction)
  Surfaces 14, 15 → k-index (Z direction)

Index scheme: i varies FASTEST (in X)
               j varies MIDDLE (in Y)
               k varies SLOWEST (in Z)

Verification command:
  mcnp6 inp=file.i ip
  Plot: origin 0 0 50, extent -20 20 -20 20, LAT=1
```

---

### 6. reactor_spec_to_lattice.py
**Purpose:** Template generator for reactor lattice from design specifications

**Usage:**
```bash
python reactor_spec_to_lattice.py --pitch 1.26 --assembly-size 17 --enrichment 4.5
```

**Features:**
- Generates MCNP lattice skeleton
- Calculates surface positions from pitch
- Creates material card templates
- Suggests volume specifications
- Outputs complete lattice structure

**Example Output:**
```
c Generated Lattice for 17×17 Assembly, 1.26 cm pitch
c
c Cell Cards
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=1  IMP:N=1
c
c Surface Cards (17×17 lattice, 1.26 cm pitch)
10   PX   0.0
11   PX   21.42        $ 17 × 1.26 cm
12   PY   0.0
13   PY   21.42
14   PZ   0.0
15   PZ   400.0        $ Typical active height
c
c Material Card (4.5% enriched UO2)
M1   92235.80c  0.045  92238.80c  0.955  8016.80c  2.0
c
c User must fill in:
c   - Pin universe definition (fuel, clad, coolant)
c   - FILL array if mixed universe pattern
c   - Actual geometry specifications
```

---

## Installation

**Requirements:**
- Python 3.7+
- No external dependencies (uses standard library only)

**Setup:**
```bash
cd .claude/skills/mcnp-lattice-builder/scripts
chmod +x *.py
```

---

## Common Workflows

### Workflow 1: Building New Lattice
```bash
# Step 1: Generate template from specs
python reactor_spec_to_lattice.py --pitch 1.26 --assembly-size 17 > template.i

# Step 2: Validate surface ordering
python surface_order_validator.py template.i --cell 100

# Step 3: Generate FILL array
python fill_array_generator.py --dims "0:16 0:16 0:0" --pattern "..." >> template.i

# Step 4: Check volumes
python lattice_volume_checker.py template.i
```

### Workflow 2: Debugging Existing Lattice
```bash
# Step 1: Visualize hierarchy
python universe_hierarchy_visualizer.py problem.i

# Step 2: Check surface ordering
python surface_order_validator.py problem.i --cell 100

# Step 3: Verify volumes
python lattice_volume_checker.py problem.i

# Step 4: Calculate indices
python lattice_index_calculator.py --from-file problem.i --cell 100
```

### Workflow 3: Understanding Index Scheme
```bash
# For LAT=1 (rectangular)
python lattice_index_calculator.py --type LAT1 --surfaces "10 11 12 13 14 15"

# For LAT=2 (hexagonal)
python lattice_index_calculator.py --type LAT2 --surfaces "10 11 12 13 14 15 16 17"
```

---

## Error Prevention

These scripts help prevent common lattice errors:

1. **Surface ordering mistakes** → surface_order_validator.py
2. **FILL array indexing errors** → fill_array_generator.py
3. **Volume specification wrong** → lattice_volume_checker.py
4. **Universe nesting confusion** → universe_hierarchy_visualizer.py
5. **Index direction mistakes** → lattice_index_calculator.py

---

## Notes

- Scripts parse MCNP input format (cards starting at column 1-5)
- Comment lines (c, C, $) are ignored
- Continuation lines (5+ spaces, &, vertical format) are handled
- Scripts are read-only (do not modify input files)
- Output can be redirected to files or piped

---

## Future Enhancements

Planned features (contributions welcome):
- Interactive mode for fill array generation
- Graphical visualization of lattice indices
- Automatic error detection and suggestions
- Integration with MCNP6 plotter
- Batch processing for multiple files
- Export to other formats (OpenMC, Serpent)

---

## Support

For issues or questions:
1. Check example files in `../assets/example_inputs/`
2. Review reference documentation in `../references/`
3. Consult MCNP6 Manual Chapter 5 (Cell and Surface Cards)
4. See SKILL.md for integration with other tools

---

**Version:** 1.0.0
**Last Updated:** 2025-11-04
**Part of:** mcnp-lattice-builder skill v2.0.0
