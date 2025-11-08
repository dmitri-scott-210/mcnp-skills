---
name: mcnp-geometry-builder
version: 2.0.0
description: Build MCNP geometry definitions with cells, surfaces, Boolean operations, transformations, and lattices. Comprehensive reference files included.
triggers:
  - geometry definition
  - cell cards
  - surface cards
  - Boolean operations
  - lattice geometry
  - universe hierarchy
  - coordinate transformations
---

# MCNP Geometry Builder

## Purpose
Build MCNP geometry using cell and surface cards with Boolean operations, transformations, universes, and lattices.

## When to Use
- Defining spatial regions (cells) for particle transport
- Creating geometric boundaries (surfaces: planes, spheres, cylinders, macrobodies)
- Complex geometries with Boolean operations
- Repeated structures (LAT=1 rectangular, LAT=2 hexagonal)
- Coordinate transformations (TR cards)
- Multi-component systems (universes, FILL)
- Debugging lost particles or geometry errors

## Prerequisites
- MCNP input structure (three blocks: Cell → Surface → Data)
- 3D coordinate systems and Boolean logic
- Reference: `mcnp-input-builder` skill for file format

---

## Core Concepts

### Constructive Solid Geometry (CSG)
MCNP geometry = Boolean combinations of **half-spaces** (regions on one side of surfaces).

**Surface Sense:**
- `-n` = **Inside/negative** side of surface n
- `+n` or `n` = **Outside/positive** side of surface n

**Example:**
```
1  SO  10.0              $ Sphere radius 10 cm at origin

c Inside sphere:
1  1  -1.0  -1  IMP:N=1  $ Material 1, inside surface 1

c Outside sphere:
2  0       1  IMP:N=0    $ Void, outside surface 1 (graveyard)
```

### Cell Card Format
```
j  m  d  geometry  params
```
- **j:** Cell number (1-99,999,999, unique)
- **m:** Material (0=void, references M card in data block)
- **d:** Density (negative=g/cm³, positive=atoms/b-cm, omit for void)
- **geometry:** Boolean expression of surfaces
- **params:** IMP:N, VOL, TMP, U, TRCL, LAT, FILL, etc.

### Surface Card Format
```
j  [n]  type  params
```
- **j:** Surface number (1-99,999,999, unique)
- **n:** (Optional) Transformation number (references *TRn)
- **type:** Mnemonic (SO, PX, C/Z, RPP, RCC, etc.)
- **params:** Geometric parameters

### Boolean Operators
- **Intersection** (space): `-1 2 -3` = inside 1 AND outside 2 AND inside 3
- **Union** (`:`): `-1 : -2` = inside 1 OR inside 2
- **Complement** (`#`): `#10` = NOT in cell 10
- **Parentheses:** `(-1 2) : (-3 4)` = (inside 1 AND outside 2) OR (inside 3 AND outside 4)

**Evaluation Order:** Complement **first**, Intersection **second**, Union **third** (parentheses override)

---

## Multi-Scale Geometry Modeling

### Scale Range in Reactor Models

Complex reactor models often span **5 orders of magnitude**:

| Scale | Example Feature | Typical Dimension | Precision |
|-------|----------------|-------------------|-----------|
| **Microscale** | TRISO fuel kernel | 10-100 μm | 5-6 digits |
| **Milliscale** | Fuel pellet, TRISO coating | 0.1-10 mm | 4-5 digits |
| **Centiscale** | Fuel pin, compact | 1-10 cm | 3-4 digits |
| **Deciscale** | Assembly, capsule | 10-100 cm | 3-4 digits |
| **Meter scale** | Core, shielding | 1-10 m | 2-3 digits |

**Example: HTGR Fuel Hierarchy**
```
TRISO kernel:     0.017485 cm  (174.85 μm)  ← 6 digits
Buffer coating:   0.027905 cm  (279.05 μm)  ← 5 digits
Compact radius:   0.6500 cm    (6.50 mm)    ← 4 digits
Capsule channel:  1.90500 cm   (19.05 mm)   ← 5 digits
```

### Precision Requirements

**General Rule**: Use enough significant figures to capture smallest feature at each scale.

**Surface Definitions**:
```mcnp
c Microscale (TRISO particles)
1    so   0.017485    $ Kernel radius (174.85 μm)
2    so   0.027905    $ Buffer outer (279.05 μm)
3    so   0.031785    $ IPyC outer (317.85 μm)

c Centiscale (compacts, assemblies)
10   c/z  25.547  -24.553  0.635    $ Compact (6.35 mm)
11   c/z  25.337  -25.337  1.519    $ Holder (15.19 mm)

c Meter scale (core boundaries)
100  rpp  -150 150  -150 150  -200 200    $ Core box
```

**Key Principle**: Preserve precision where needed, but avoid false precision (0.017485 is meaningful, 25.547039 may be overkill for cm-scale).

### Units Management

**MCNP uses cm for ALL lengths**. Always convert:
- μm → cm: divide by 10,000
- mm → cm: divide by 10
- m → cm: multiply by 100

**Example Conversions**:
```
174.85 μm = 0.017485 cm  ✓
6.5 mm    = 0.65 cm      ✓
1.9 m     = 190 cm       ✓
```

---

## Decision Tree

```
Geometry Complexity?
  |
  +--[Simple: 1-5 regions]----> Direct cell/surface definitions
  |                             Use planes, spheres, cylinders
  |
  +--[Moderate: 5-20 regions]--> Macrobodies + numbering scheme
  |                             Group by function (1-99=core, 100-199=reflector)
  |
  +--[Complex: 20+ regions]----> Universes + modular design
  |                             Define reusable components (U parameter)
  |
  +--[Repeated Structure]------> Lattices
                                 LAT=1 (rectangular) or LAT=2 (hexagonal)
```

---

## Quick Reference

### Common Surface Types
| Type | Mnemonic | Parameters | Example |
|------|----------|------------|---------|
| Plane (x) | PX | D | `1 PX 5.0` (x=5) |
| Plane (y) | PY | D | `2 PY -3.0` (y=-3) |
| Plane (z) | PZ | D | `3 PZ 10.0` (z=10) |
| Sphere (origin) | SO | R | `1 SO 10.0` (R=10) |
| Sphere (general) | S | x y z R | `2 S 5 0 0 10` |
| Cylinder (z-axis) | CZ | R | `1 CZ 2.0` (R=2) |
| Cylinder (general) | C/Z | x y R | `2 C/Z 5 0 3.0` |

**Complete surface types:** See `surface_types_comprehensive.md`

### Surface Type Selection Decision Tree

```
Geometry Type?
  |
  +--[Sphere centered at origin (universe)]----> SO R
  |                                               Fastest, use in repeated structures
  |
  +--[Sphere at arbitrary location]------------> S x y z R
  |                                               More flexible
  |
  +--[Cylinder on axis (universe)]--------------> CZ R
  |                                               Fastest for axial symmetry
  |
  +--[Cylinder off-axis]------------------------> C/Z x y R
  |                                               Essential for multi-stack assemblies
  |
  +--[Rectangular lattice boundary]-------------> RPP xmin xmax ymin ymax zmin zmax
  |                                               LAT=1 requires RPP
  |
  +--[Hexagonal lattice boundary]---------------> RHP vx vy vz hx hy hz Rx Ry Rz
  |                                               LAT=2 requires RHP (9 values)
  |
  +--[Axial segmentation]-----------------------> PZ z
                                                  Shared across multiple cells
```

### Performance Considerations

**Fastest to Slowest**:
1. **SO** (sphere at origin) - optimized tracking
2. **CZ** (cylinder on Z-axis) - axial symmetry
3. **PX, PY, PZ** (axis-aligned planes) - simple checks
4. **S, C/Z** (general sphere/cylinder) - coordinate transformation
5. **P** (general plane) - full equation evaluation
6. **Macrobodies** (RPP, RCC, RHP) - expand to facets

**Best Practice**: Use centered surfaces (SO, CZ) in universes, positioned surfaces (S, C/Z) in global geometry.

### Surface Type by Application

| Application | Recommended Surface | Example |
|-------------|---------------------|---------|
| **TRISO particle layers** | SO (in universe) | `1 so 0.01748` |
| **Fuel pin (centered)** | CZ (in universe) | `10 cz 0.41` |
| **Assembly stacks (off-axis)** | C/Z | `100 c/z 25.5 -24.5 0.635` |
| **Rectangular lattice boundary** | RPP | `200 rpp -10 10 -10 10 0 180` |
| **Hexagonal lattice boundary** | RHP (9 values) | `300 rhp 0 0 0  0 0 68  0 1.6 0` |
| **Axial zones** | PZ (shared) | `1000 pz 60.96` |
| **Concentric shells (centered)** | SO or CZ | `1 so 10  2 so 15  3 so 20` |
| **Concentric cylinders (off-axis)** | C/Z (same center) | `10 c/z 5 5 1.0  11 c/z 5 5 1.5` |

**See**: `surface_selection_patterns.md` for complete decision trees and 20+ examples.

### Common Macrobodies
| Macro | Description | Values | Use Case |
|-------|-------------|--------|----------|
| RPP | Axis-aligned box | 6 (xmin xmax ymin ymax zmin zmax) | Buildings, rooms |
| RCC | Right circular cylinder | 7 (vx vy vz hx hy hz R) | Fuel rods, pipes |
| RHP/HEX | Hexagonal prism | 9 min (vx vy vz h1 h2 h3 r1 r2 r3) | VVER assemblies |
| SPH | Sphere | 4 (x y z R) | Alternative to SO/S |

**Complete macrobodies:** See `macrobodies_reference.md`

---

## Concentric Geometry Patterns

### Nested Spherical Shells

**Common in**: Particle fuel, bare sphere assemblies, detector calibration

**Pattern**: Multiple SO surfaces with increasing radii

**Example: TRISO Particle (5 layers)**
```mcnp
c Cell Cards (in universe u=100)
1  1  -10.8   -1          u=100  $ Kernel (UO2)
2  2  -0.98    1  -2      u=100  $ Buffer (porous C)
3  3  -1.85    2  -3      u=100  $ IPyC (dense C)
4  4  -3.20    3  -4      u=100  $ SiC (ceramic)
5  5  -1.86    4  -5      u=100  $ OPyC (dense C)
6  6  -1.75    5          u=100  $ Matrix (graphite)

c Surface Cards (centered at origin for universe)
1  so  0.02500    $ Kernel radius (250 μm)
2  so  0.03500    $ Buffer outer (350 μm)
3  so  0.03900    $ IPyC outer (390 μm)
4  so  0.04250    $ SiC outer (425 μm)
5  so  0.04650    $ OPyC outer (465 μm)
```

**Key Pattern**:
- Surface N bounds cells N and N+1
- Inner cell: `-N`
- Shell cell: `N -N+1`
- Outer cell: `N_max`

**Volume Calculation**:
```
V_shell = (4/3)π(R_outer³ - R_inner³)
```

### Concentric Cylinders (Same Axis)

**Common in**: Fuel pins, capsule structures, pipes

**Pattern - Centered (CZ)**:
```mcnp
c Fuel pin (4 regions)
1  1  -10.5  -1          u=10  $ Fuel
2  0         1  -2       u=10  $ Gap
3  2  -6.5    2  -3      u=10  $ Clad
4  3  -1.0    3          u=10  $ Coolant

c Surfaces
1  cz  0.409    $ Fuel outer
2  cz  0.418    $ Gap outer
3  cz  0.475    $ Clad outer
```

**Pattern - Off-Axis (C/Z)**:
```mcnp
c Capsule structure (7 layers, off-axis)
c All centered at (25.337, -25.337)
1  1  -10.9   -1              $ Compact (fuel)
2  0          1  -2           $ Gas gap
3  2  -1.75   2  -3           $ Graphite holder
4  0          3  -4           $ Gap
5  3  -8.0    4  -5           $ SS wall
6  4  -13.3   5  -6           $ Hafnium shroud
7  3  -8.0    6  -7           $ Outer wall
8  0          7               $ Outside

c Surfaces (all c/z with same center)
1  c/z  25.337  -25.337  0.635    $ Compact
2  c/z  25.337  -25.337  0.641    $ Gap
3  c/z  25.337  -25.337  1.519    $ Holder
4  c/z  25.337  -25.337  1.588    $ Gap
5  c/z  25.337  -25.337  1.622    $ SS wall
6  c/z  25.337  -25.337  1.647    $ Hf shroud
7  c/z  25.337  -25.337  1.786    $ Outer wall
```

**Key Principles**:
1. Use **same center coordinates** for all C/Z surfaces
2. **Monotonically increasing radii** (R1 < R2 < R3 < ...)
3. **Gap management**: Thin regions (< 0.1 mm) may cause tracking issues
4. **Off-axis placement**: Enables multiple stacks at different positions

**Volume Calculation**:
```
V_shell = π(R_outer² - R_inner²) × height
```

### Multiple Concentric Systems (Different Centers)

**Common in**: Multi-stack assemblies, detector arrays

**Example: Three fuel stacks at 120° intervals**
```mcnp
c Stack 1 (centered at 25.547, -24.553)
11  c/z  25.547  -24.553  0.635    $ Compact
12  c/z  25.547  -24.553  0.641    $ Gap

c Stack 2 (centered at 24.553, -25.547)
21  c/z  24.553  -25.547  0.635    $ Compact
22  c/z  24.553  -25.547  0.641    $ Gap

c Stack 3 (centered at 25.911, -25.911)
31  c/z  25.911  -25.911  0.635    $ Compact
32  c/z  25.911  -25.911  0.641    $ Gap

c Shared outer containment (centered at 25.337, -25.337)
100 c/z  25.337  -25.337  1.786    $ Capsule outer
```

**Pattern**: Each stack has concentric surfaces at its own center, enclosed by common outer boundary.

**See**: `concentric_geometry_reference.md` for 15+ patterns and templates.

---

## Use Cases

### 1. Nested Spherical Shells
**Application:** Bare sphere critical assembly, detector calibration

```
c Cell Cards
1    1  -19.0  -1      IMP:N=1  VOL=33.51    $ Core (tungsten)
2    2  -10.5   1 -2   IMP:N=2  VOL=268.08   $ Shield (lead)
3    0          2      IMP:N=0               $ Graveyard

c Surface Cards
1    SO  2.0            $ Core R=2 cm
2    SO  6.0            $ Shield outer R=6 cm

c Data Cards
MODE N
SDEF  POS=0 0 0  ERG=14.1
M1   74000  1.0          $ Tungsten
M2   82000  1.0          $ Lead
NPS  10000
```

**Key Points:**
- Spherical symmetry simplifies modeling
- Volume = (4/3)π(R_outer³ - R_inner³)
- See `example_geometries/01_nested_spheres.i`

### 2. Rectangular Pin Lattice (LAT=1)
**Application:** PWR fuel assembly, detector array

```
c Pin universe (U=1)
1    1  -10.5  -1     U=1  IMP:N=1    $ Fuel
2    2  -6.5    1 -2  U=1  IMP:N=1    $ Clad
3    3  -1.0    2     U=1  IMP:N=1    $ Water

c Lattice (3×3 array)
10   0  -10  LAT=1  U=2  IMP:N=1
        FILL=-1:1 -1:1 0:0
             1 1 1    $ j=1 (top row)
             1 1 1    $ j=0 (middle)
             1 1 1    $ j=-1 (bottom)

c Base geometry
20   0  -20  FILL=2  IMP:N=1         $ Fill with lattice
21   0   20  IMP:N=0                  $ Graveyard

c Surfaces
1    CZ  0.4                           $ Fuel R
2    CZ  0.5                           $ Clad outer R
10   RPP  -1.5 1.5  -1.5 1.5  0 10    $ Lattice boundary
20   RPP  -2 2  -2 2  -1 11            $ Outer boundary
```

**Key Points:**
- **LAT=1 indexing:** i (X) fastest, j (Y) middle, k (Z) slowest
- FILL array lists universes by (k, j, i)
- See `lattice_geometry_reference.md` and `templates/cylinder_array_template.i`

### 3. Fill Transformations and Off-Axis Placement
**Application:** Lattice positioning, multi-assembly cores, off-axis experiments

#### Pattern 1: Simple Fill Translation

**Example: Position lattice at specific location**
```mcnp
c Lattice universe (u=100) - defined at origin
1  0  -1  u=100 lat=1  fill=-1:1 -1:1 0:0  $ 3×3 array
      10 10 10
      10 10 10
      10 10 10

c Global placement - shift lattice to (5, -3, 20)
100  0  -100  fill=100  (5 -3 20)

c Surfaces
1    rpp  -1.5 1.5  -1.5 1.5  0 10     $ Lattice boundary (local coords)
100  rpp   3.5 6.5  -4.5 -1.5  20 30   $ Global boundary (shifted)
```

**Key Points**:
- Lattice defined with origin at (0,0,0) in local universe
- Fill translation `(x,y,z)` moves origin to global coordinates
- Surface 100 bounds the SHIFTED lattice

#### Pattern 2: Multiple Lattices at Different Positions

**Example: Three fuel stacks in capsule**
```mcnp
c Compact lattice universe (u=1110) - vertical stack
1110  0  -1  u=1110 lat=1  fill=0:0 0:0 -15:15  $ 1×1×31
      [... 31 universe numbers ...]

c Stack 1 placement (at 25.547, -24.553, starting z=19.108)
111  0  -11  98005 -98051  fill=1110  (25.547039 -24.553123 19.108100)

c Stack 2 placement (at 24.553, -25.547, same z)
121  0  -21  98005 -98051  fill=1120  (24.553123 -25.547039 19.108100)

c Stack 3 placement (at 25.911, -25.911, same z)
131  0  -31  98005 -98051  fill=1130  (25.910838 -25.910838 19.108100)

c Surfaces (off-axis cylinders)
11   c/z  25.547039  -24.553123  0.635    $ Stack 1 boundary
21   c/z  24.553123  -25.547039  0.635    $ Stack 2 boundary
31   c/z  25.910838  -25.910838  0.635    $ Stack 3 boundary
98005 pz  17.81810                        $ Bottom plane (shared)
98051 pz  20.35810                        $ Top plane (shared)
```

**Pattern**:
1. Define lattice universe at origin
2. Create fill cells with translations for each position
3. Use off-axis C/Z surfaces to bound each stack
4. Share axial planes (PZ) across all stacks

#### Pattern 3: Transformation + Rotation (Advanced)

**Example: Rotated assembly**
```mcnp
c Assembly universe (u=200)
[... assembly definition ...]

c Global placement with translation AND rotation
100  0  -100  fill=200  (*1)

c Transformation card (rotate 30° about Z, then translate)
*tr1  10 0 0    $ Translation (x,y,z)
      30         $ Rotation angle about Z-axis (degrees)
```

**Syntax Options for TRCL/Fill**:
1. **Translation only**: `(x y z)`
2. **Transformation reference**: `(*n)` references `*TRn` card
3. **Inline transformation**: Full 13-value specification on TRCL line

**See**: `transformations_reference.md` for rotation matrices and detailed examples.

### 4. Macrobody Example
**Application:** Complex shapes with fewer cards

```
c Cells
1    1  -7.8  -1       IMP:N=1    $ Box (iron)
2    2  -1.0  -2  1    IMP:N=1    $ Cylinder with box cutout (water)
3    0         2  -99  IMP:N=1    $ Void
4    0         99      IMP:N=0    $ Graveyard

c Surfaces
1    RPP  -10 10  -10 10  0 20    $ Box (macrobody, 6 facets)
2    RCC  0 0 0  0 0 20  3.0      $ Cylinder (macrobody, 3 facets)
99   SO   50.0                     $ Boundary

c Data Cards
MODE N
SDEF  POS=0 0 0  ERG=1.0
M1   26000  1.0                    $ Iron
M2   1001  2.0  8016  1.0          $ Water
NPS  10000
```

**Key Points:**
- RPP creates 6 plane facets (j.1 through j.6)
- RCC creates 3 facets (j.1=side, j.2=bottom, j.3=top)
- **Facet restrictions:** Cannot use with SSR/SSW/PTRAC
- See `macrobodies_reference.md` and `example_geometries/07_macrobody_example.i`

---

## Integration with Other Skills

### Geometry → Materials
After defining cells with material numbers:
```
1  1  -10.5  -1  IMP:N=1    $ Cell 1, material 1
```
Use `mcnp-material-builder` to define M1 card:
```
M1  92235  -0.04  92238  -0.96  8016  -2.0    $ UO₂ fuel
```

### Geometry → Source
After defining cells:
```
10  0  -10  FILL=2  IMP:N=1    $ Lattice cell
```
Use `mcnp-source-builder` to specify volumetric source:
```
SDEF  CEL=10  ERG=2.0
```

### Geometry → Tallies
After defining cells/surfaces:
```
SDEF  POS=0 0 0  ERG=14.1
F4:N  1 2 3              $ Flux tally in cells 1, 2, 3
F2:N  1.1 1.2            $ Current tally on RPP facets
```

### Geometry → Validation
Before running MCNP:
1. Use `scripts/geometry_validator.py input.inp` (pre-MCNP validation)
2. Plot geometry: `mcnp6 inp=file.i ip` (interactive)
3. Use `scripts/geometry_plotter_helper.py input.inp` (automated plots)

---

## Comprehensive References

**Surface Specifications:**
- `surface_types_comprehensive.md` - All 25+ surface types with equations
- `macrobodies_reference.md` - 11 macrobody types, facet numbering, restrictions

**Cell Definitions (Most Critical - Where Errors Occur):**
- `cell_definition_comprehensive.md` - Cell format, numbering, LIKE n BUT
- `cell_parameters_reference.md` - All 18 cell parameters (IMP, VOL, TMP, U, TRCL, LAT, FILL, etc.)
- `boolean_operations_guide.md` - Intersection, union, complement, precedence rules, 11 examples
- `complex_geometry_patterns.md` - Advanced patterns, 10+ complete examples

**System Components:**
- `transformations_reference.md` - TR cards, rotation matrices, inline TRCL, periodic boundaries
- `lattice_geometry_reference.md` - LAT=1/LAT=2, indexing, nested universes, 10 examples
- `geometry_debugging.md` - VOID card, lost particles, 10 error patterns, validation workflow

**Assets:**
- `example_geometries/` - 10 working examples with documentation
- `templates/` - 4 templates (nested spheres, rectangular array, hexagonal lattice, transformations)
- `scripts/` - 2 Python helpers (validator, plotter)

---

## Best Practices

1. **Start simple** - Test basic geometry before adding complexity
2. **Plot early, plot often** - Use `ip` mode: `mcnp6 inp=file.i ip`
3. **Number systematically** - Group by function (1-99=core, 100-199=reflector, etc.)
4. **Validate before running** - Use `scripts/geometry_validator.py`
5. **Use macrobodies judiciously** - Simpler than primitives but less flexible
6. **Document Boolean expressions** - Add comments explaining complex geometry
7. **Check blank lines** - EXACTLY 2 blank lines total (after cells, after surfaces)
8. **Test incrementally** - Add one feature, plot, verify, repeat
9. **Use VOID card for testing** - Flood geometry to find gaps/overlaps
10. **Reference documentation** - Check `` for detailed specifications

---

## Troubleshooting

### Lost Particle
**Symptom:** "Lost particle" errors in output
**Causes:** Geometry gaps, overlaps, undefined surfaces, Boolean errors
**Fix:**
1. Read lost particle location from output
2. Plot at that location: `origin X Y Z`
3. Check Boolean expression for that cell
4. See `geometry_debugging.md`

### Undefined Surface
**Symptom:** "Surface X undefined"
**Fix:** Cell references surface X, but X not defined in surface block

### BAD TROUBLE 1000
**Symptom:** Overlapping cells
**Fix:** Check Boolean expressions - cells may occupy same space

### Volume Calculation Failed
**Symptom:** "Cannot calculate volume for cell X"
**Fix:** Add `VOL=` parameter or use stochastic volume calculation

**Complete error catalog:** See `geometry_debugging.md`

---

## Examples and Templates

**10 Example Files** (with documentation):
- 01_nested_spheres.i/md - Concentric shells
- 02_fuel_pin.i/md - Four-region PWR pin
- 03_slab_geometry.i/md - Multi-layer shielding
- 04_simple_lattice.i/md - 3×3 rectangular array
- 05_complement_example.i/md - Box with cylindrical void
- 06_transformed_geometry.i/md - Rotated cylinders
- 07_macrobody_example.i/md - RPP and RCC
- 08_union_example.i/md - Overlapping spheres
- 09_sector_geometry.i/md - Angular sector
- 10_nested_universe.i/md - Three-level hierarchy

**4 Templates:**
- nested_spheres_template.i - Shielding configurations
- cylinder_array_template.i - LAT=1 pin arrays
- hex_lattice_template.i - LAT=2 hex assemblies (with correct RHP 9-value specification)
- transformed_geometry_template.i - TR card applications

**2 Python Scripts:**
- geometry_validator.py - Pre-MCNP validation
- geometry_plotter_helper.py - Automated plot generation

**See** `templates/README.md` and `scripts/README.md` for complete usage guides.

---

## Quick Start

1. **Identify regions** - What cells do you need?
2. **Define surfaces** - What boundaries define cells?
3. **Write cell cards** - Boolean combinations of surfaces
4. **Write surface cards** - Use simplest type (planes, spheres first)
5. **Validate format** - `python scripts/geometry_validator.py file.inp`
6. **Plot geometry** - `mcnp6 inp=file.i ip`
7. **Test run** - Low NPS (1000) to check for lost particles
8. **Iterate** - Fix errors, re-plot, re-test

**See decision tree above for complexity-specific approaches.**

---

**Version:** 2.0.0 (Session 8, 2025-11-03)
**Documentation:** 9 reference files, 10 examples, 4 templates
**Total Assets:** ~26,000 words in references + examples + templates
