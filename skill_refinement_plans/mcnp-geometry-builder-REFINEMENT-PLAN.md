# mcnp-geometry-builder REFINEMENT PLAN
## Comprehensive Skill Enhancement for Complex Reactor Modeling

**Created**: 2025-11-08
**Based On**: AGR-1 HTGR analysis (23,000+ lines MCNP code, 6-level hierarchies, 5 orders of magnitude geometry)
**Priority**: 🟡 **MEDIUM-HIGH** - Critical for reactor modeling, but depends on mcnp-lattice-builder fixes
**Estimated Time**: 2-3 hours

---

## EXECUTIVE SUMMARY

The AGR-1 HTGR model analysis reveals sophisticated geometry building patterns not adequately covered in the current mcnp-geometry-builder skill:

1. **Multi-scale geometry** (174 μm TRISO kernels to 190 mm capsule channels)
2. **Surface type selection** (RPP vs RHP for lattices, SO vs CZ for nested regions)
3. **Concentric cylinder hierarchies** (7-layer capsule structure)
4. **Fill transformations** for off-axis placement
5. **Reactor assembly templates** (rectangular pin arrays, hexagonal assemblies)

**Impact**: Users building complex reactor models lack guidance on surface selection, multi-scale precision, and concentric geometry patterns.

---

## CURRENT STATE ANALYSIS

### What's Already Covered (Well)
✅ Basic cell/surface formats
✅ Boolean operations
✅ Simple lattice concepts (LAT=1, LAT=2 mentioned)
✅ Transformation basics (TR cards)
✅ Macrobodies (RPP, RCC, RHP)
✅ Example files (10 examples + 4 templates)

### Critical Gaps Identified

#### Gap 1: Multi-Scale Geometry Guidance
**Issue**: No guidance on handling 5+ orders of magnitude in same model
**Example from AGR-1**:
- TRISO kernel radius: 0.017485 cm (174.85 μm)
- Capsule channel: 1.90500 cm (19.05 mm)
- Scale ratio: **109:1**

**Missing**:
- Precision requirements by scale
- Surface type selection for different scales
- Units management across scales

#### Gap 2: Surface Type Selection Patterns
**Issue**: No systematic guidance on WHEN to use which surface type
**Examples from AGR-1**:
- SO (sphere at origin) for TRISO particles in universes
- C/Z (off-axis cylinder) for stack positions
- RPP (rectangular parallelepiped) for lattice boundaries
- RHP (hexagonal prism) for hexagonal assemblies
- PZ (plane perpendicular to Z) for axial segmentation

**Missing**:
- Decision tree for surface type selection
- Performance implications (SO vs S, CZ vs C/Z)
- Lattice-specific requirements

#### Gap 3: Concentric Geometry Patterns
**Issue**: Limited guidance on nested cylindrical structures
**Example from AGR-1 (7-layer capsule)**:
```
97011 c/z   25.547 -24.553   0.63500  $ Compact outer
97012 c/z   25.547 -24.553   0.64135  $ Gas gap
97060 c/z   25.337 -25.337   1.51913  $ Holder
97061 c/z   25.337 -25.337   1.58750  $ Gap
97062 c/z   25.337 -25.337   1.62179  $ SS wall
97063 c/z   25.337 -25.337   1.64719  $ Hf shroud
97065 c/z   25.337 -25.337   1.78562  $ Outer wall
```

**Missing**:
- Concentric cylinder templates
- Off-axis concentric structures
- Gap management (thin regions)

#### Gap 4: Fill Transformations
**Issue**: Limited examples of fill with translation
**Example from AGR-1**:
```mcnp
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
```

**Missing**:
- Off-axis lattice placement
- Multiple lattices at different positions
- Transformation syntax variations

#### Gap 5: Reactor Assembly Templates
**Issue**: Limited reactor-specific geometry patterns
**Needed**:
- PWR pin cell template (fuel/gap/clad/coolant)
- Hexagonal assembly template (HTGR, fast reactor)
- TRISO particle template (5-layer coating)
- Concentric sphere/cylinder generators

---

## REFINEMENT PLAN

### Phase 1: Core SKILL.md Updates

#### 1.1 Add Multi-Scale Geometry Section

**Location**: After "Core Concepts", before "Decision Tree"

**New Section**:
```markdown
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
```

#### 1.2 Add Surface Type Selection Guide

**Location**: After "Common Surface Types" table in Quick Reference

**New Section**:
```markdown
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
```

#### 1.3 Add Concentric Geometry Section

**Location**: After Surface Type Selection, before "Use Cases"

**New Section**:
```markdown
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
```

#### 1.4 Add Fill Transformation Section

**Location**: Enhance existing "Coordinate Transformations" use case

**Replace/Enhance Section 3 with**:
```markdown
### 3. Fill Transformations and Off-Axis Placement
**Application**: Lattice positioning, multi-assembly cores, off-axis experiments

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

**See**: `transformations_reference.md` (already exists) for rotation matrices and detailed examples.
```

### Phase 2: New Reference Files

#### 2.1 Create surface_selection_patterns.md

**File**: `.claude/skills/mcnp-geometry-builder/surface_selection_patterns.md`

**Content**:
```markdown
# Surface Selection Patterns for Complex Geometries

## Decision Trees for Common Applications

### Reactor Fuel Modeling

#### TRISO Particle Fuel
**Requirement**: 5-layer spherical coating structure
**Surfaces**: SO (spheres at origin in universe)
**Reason**: Fastest tracking, particle replicated thousands of times

```mcnp
c Universe u=100 (TRISO particle)
1  so  0.02500    $ Kernel
2  so  0.03500    $ Buffer
3  so  0.03900    $ IPyC
4  so  0.04250    $ SiC
5  so  0.04650    $ OPyC
```

#### PWR Fuel Pin
**Requirement**: Cylindrical fuel/gap/clad/coolant
**Surfaces**: CZ (cylinders on Z-axis in universe)
**Reason**: Axial symmetry, simple tracking

```mcnp
c Universe u=10 (fuel pin)
1  cz  0.409    $ Fuel
2  cz  0.418    $ Gap
3  cz  0.475    $ Clad
```

#### Multi-Stack Assembly
**Requirement**: Multiple parallel fuel channels
**Surfaces**: C/Z (off-axis cylinders)
**Reason**: Each stack at different (x,y) position

```mcnp
c Stack 1 at (5, 0)
11  c/z  5 0  0.5

c Stack 2 at (-5, 0)
21  c/z  -5 0  0.5
```

[... continue with 15 more patterns ...]

## Performance Optimization

### Tracking Speed Ranking
1. SO, CZ, PX/PY/PZ (fastest)
2. S, C/X, C/Y (coordinate transformation)
3. C/Z (off-axis, 2D transformation)
4. P (general plane, full equation)
5. Macrobodies (expanded to facets)

### When to Use Macrobodies vs Primitives

**Use Macrobodies (RPP, RCC, RHP) when**:
- ✅ Input file simplicity more important than facet flexibility
- ✅ No need for separate facet tallies (F2, F4:S)
- ✅ Not using SSR/SSW/PTRAC (facet restrictions)
- ✅ Prototyping or teaching

**Use Primitives (P, CZ, SO) when**:
- ✅ Need surface-specific tallies
- ✅ Using SSR (surface source read) or SSW (write)
- ✅ Complex Boolean operations (easier with primitives)
- ✅ Production calculations

## Complete Decision Matrix

[... table with 25+ surface types, applications, pros/cons ...]

```

#### 2.2 Create concentric_geometry_reference.md

**File**: `.claude/skills/mcnp-geometry-builder/concentric_geometry_reference.md`

**Content**:
```markdown
# Concentric Geometry Reference
## Patterns for Nested Spherical and Cylindrical Structures

## Nested Spheres (Radial Symmetry)

### Pattern 1: N-Layer Spherical Shell
**Applications**: TRISO particles, bare sphere assemblies, detector calibration, shielding

**General Template**:
```mcnp
c Cells (N layers)
1    1  -D1   -1         u=U  $ Core
2    2  -D2    1  -2     u=U  $ Layer 1
3    3  -D3    2  -3     u=U  $ Layer 2
...
N    N  -DN   (N-1) -N  u=U  $ Layer N-1
N+1  0        N           u=U  $ Exterior (if in universe)

c Surfaces
1  so  R1
2  so  R2
3  so  R3
...
N  so  RN
```

**Constraints**:
- R1 < R2 < R3 < ... < RN (strictly increasing)
- Cell J bounded by surfaces J and J+1

**Example: 5-Layer TRISO Particle**
```mcnp
c Cells
1  1  -10.8   -1       u=100  vol=6.545e-5   $ Kernel (250 μm)
2  2  -0.98    1  -2   u=100                 $ Buffer
3  3  -1.85    2  -3   u=100                 $ IPyC
4  4  -3.20    3  -4   u=100                 $ SiC
5  5  -1.86    4  -5   u=100                 $ OPyC
6  6  -1.75    5       u=100                 $ Matrix

c Surfaces
1  so  0.02500
2  so  0.03500
3  so  0.03900
4  so  0.04250
5  so  0.04650
```

**Volume Calculations**:
```
V_core = (4/3) π R1³
V_shell_i = (4/3) π (R_i+1³ - R_i³)
```

[... 10 more nested sphere patterns ...]

## Nested Cylinders (Axial Symmetry)

### Pattern 2: N-Layer Cylindrical Shell (Centered)

**Applications**: Fuel pins, coolant channels, pipes

**General Template**:
```mcnp
c Cells
1    1  -D1   -1  zmin -zmax      u=U  $ Core
2    2  -D2    1  -2  zmin -zmax  u=U  $ Layer 1
...
N+1  0        N   zmin -zmax      u=U  $ Exterior

c Surfaces
1   cz  R1
2   cz  R2
...
N   cz  RN
zmin pz  Z1
zmax pz  Z2
```

**Example: PWR Fuel Pin**
```mcnp
c Cells
1  1  -10.5  -1  -10 11     u=10  $ Fuel
2  0         1  -2  -10 11  u=10  $ Gap
3  2  -6.5   2  -3  -10 11  u=10  $ Clad
4  3  -1.0   3      -10 11  u=10  $ Coolant

c Surfaces
1   cz  0.409     $ Fuel outer
2   cz  0.418     $ Gap outer
3   cz  0.475     $ Clad outer
10  pz  0.0       $ Bottom
11  pz  360.0     $ Top
```

[... continue with off-axis patterns, multi-stack examples ...]

### Pattern 3: Concentric Cylinders (Off-Axis)

**Applications**: Multi-stack assemblies, off-axis experiments, capsule structures

**Example: 7-Layer Capsule**
```mcnp
c Cells (all centered at x=25.337, y=-25.337)
1  1  -10.9   -1              -10 11  $ Fuel compact
2  0          1  -2           -10 11  $ Gas gap (0.6 mm)
3  2  -1.75   2  -3           -10 11  $ Graphite holder
4  0          3  -4           -10 11  $ Gap
5  3  -8.0    4  -5           -10 11  $ Stainless steel wall
6  4  -13.3   5  -6           -10 11  $ Hafnium shroud
7  3  -8.0    6  -7           -10 11  $ Outer wall
8  0          7               -10 11  $ Outside capsule

c Surfaces (all c/z with same center)
1   c/z  25.337  -25.337  0.6350    $ Compact (6.35 mm)
2   c/z  25.337  -25.337  0.6413    $ Gas gap (6.41 mm)
3   c/z  25.337  -25.337  1.5191    $ Holder (15.19 mm)
4   c/z  25.337  -25.337  1.5875    $ Gap (15.88 mm)
5   c/z  25.337  -25.337  1.6218    $ SS wall (16.22 mm)
6   c/z  25.337  -25.337  1.6472    $ Hf shroud (16.47 mm)
7   c/z  25.337  -25.337  1.7856    $ Outer wall (17.86 mm)
10  pz  0.0
11  pz  129.54
```

**Key Pattern**:
- All surfaces share **same (x,y) center**
- Radii **strictly increasing**
- Axial planes **shared** across all layers

[... continue with gap management, thin region handling ...]

## Multiple Concentric Systems

### Pattern 4: Three Concentric Systems at Different Centers

**Example: Three fuel stacks in triangular arrangement**
```mcnp
c Stack 1 (center: 25.547, -24.553)
11  c/z  25.547  -24.553  0.635
12  c/z  25.547  -24.553  0.641

c Stack 2 (center: 24.553, -25.547)
21  c/z  24.553  -25.547  0.635
22  c/z  24.553  -25.547  0.641

c Stack 3 (center: 25.911, -25.911)
31  c/z  25.911  -25.911  0.635
32  c/z  25.911  -25.911  0.641

c Shared outer boundary (center: 25.337, -25.337)
100 c/z  25.337  -25.337  1.905
```

**Geometric Calculation**:
```
Stack spacing from center:
d1 = sqrt((25.547-25.337)² + (-24.553+25.337)²) = 0.849 cm
d2 = sqrt((24.553-25.337)² + (-25.547+25.337)²) = 0.849 cm
d3 = sqrt((25.911-25.337)² + (-25.911+25.337)²) = 0.849 cm

→ Equilateral triangle with R = 0.849 cm
```

[... continue with positioning calculations, verification methods ...]

## Common Errors and Fixes

### Error 1: Overlapping Cylinders
**Symptom**: BAD TROUBLE, overlapping cells
**Cause**: Radii not strictly increasing or wrong centers
**Fix**: Verify R1 < R2 < R3 and all c/z have same center

### Error 2: Lost Particles in Thin Gaps
**Symptom**: Particles lost in gap regions
**Cause**: Gap thickness < 0.01 cm (100 μm) causes tracking issues
**Fix**: Either increase gap or use importance weighting

[... continue with 10 common errors ...]

## Volume Calculations

### Spherical Shells
```
V = (4/3) π (R_outer³ - R_inner³)
```

### Cylindrical Shells
```
V = π h (R_outer² - R_inner²)
```

### Python Helper
```python
import math

def sphere_shell_volume(r_inner, r_outer):
    """Calculate volume of spherical shell in cm³"""
    return (4/3) * math.pi * (r_outer**3 - r_inner**3)

def cylinder_shell_volume(r_inner, r_outer, height):
    """Calculate volume of cylindrical shell in cm³"""
    return math.pi * height * (r_outer**2 - r_inner**2)

# Example: TRISO kernel
v_kernel = sphere_shell_volume(0, 0.02500)
print(f"Kernel volume: {v_kernel:.6e} cm³")  # 6.545e-05

# Example: Fuel pin gap
v_gap = cylinder_shell_volume(0.409, 0.418, 360.0)
print(f"Gap volume: {v_gap:.3f} cm³")  # 8.19
```

[... continue with complete reference ...]
```

#### 2.3 Create reactor_assembly_templates.md

**File**: `.claude/skills/mcnp-geometry-builder/reactor_assembly_templates.md`

**Content**:
```markdown
# Reactor Assembly Templates
## Production-Ready Geometry Patterns for Common Reactor Types

## PWR Fuel Pin Assembly

### Standard 17×17 Assembly Template

**Specifications**:
- Fuel pins: 264 positions (17×17 - 25 guide tubes)
- Guide tubes: 24 positions + 1 instrumentation
- Pin pitch: 1.26 cm
- Assembly pitch: 21.50 cm

**Complete Template**:
```mcnp
c ============================================================
c PWR 17×17 FUEL ASSEMBLY
c ============================================================

c ------------------------------------------------------------
c UNIVERSE DEFINITIONS
c ------------------------------------------------------------

c Fuel pin universe (u=100)
100  1  -10.5   -100        u=100  imp:n=1  $ UO2 fuel
101  0          100  -101   u=100  imp:n=1  $ Gas gap
102  2  -6.5    101  -102   u=100  imp:n=1  $ Zircaloy clad
103  3  -0.7    102         u=100  imp:n=1  $ Water coolant

c Guide tube universe (u=101)
110  3  -0.7   -110        u=101  imp:n=1  $ Water inside
111  2  -6.5    110  -111  u=101  imp:n=1  $ Guide tube wall
112  3  -0.7    111        u=101  imp:n=1  $ Water outside

c Instrumentation tube universe (u=102)
120  0         -120        u=102  imp:n=1  $ Void
121  2  -6.5    120  -121  u=102  imp:n=1  $ Instrument tube
122  3  -0.7    121        u=102  imp:n=1  $ Water

c ------------------------------------------------------------
c LATTICE ASSEMBLY (u=200)
c ------------------------------------------------------------
c 17×17 array with guide tube positions
200  0  -200  u=200  lat=1  imp:n=1  fill=-8:8 -8:8 0:0
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=8
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100  $j=7
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=6
     101 100 101 100 100 100 101 100 100 100 101 100 100 100 101 100 101  $j=5
     100 100 100 100 100 101 100 100 100 101 100 100 100 100 100 100 100  $j=4
     100 100 100 100 101 100 100 100 100 100 101 100 100 100 100 100 100  $j=3
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=2
     101 100 101 100 100 100 101 100 102 100 101 100 100 100 101 100 101  $j=1
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100  $j=0
     101 100 101 100 100 100 101 100 100 100 101 100 100 100 101 100 101  $j=-1
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=-2
     100 100 100 100 101 100 100 100 100 100 101 100 100 100 100 100 100  $j=-3
     100 100 100 100 100 101 100 100 100 101 100 100 100 100 100 100 100  $j=-4
     101 100 101 100 100 100 101 100 100 100 101 100 100 100 101 100 101  $j=-5
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=-6
     100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100  $j=-7
     100 100 100 101 100 100 100 101 100 100 100 101 100 100 100 100 100  $j=-8

c ------------------------------------------------------------
c GLOBAL PLACEMENT
c ------------------------------------------------------------
999   0  -200  fill=200  imp:n=1    $ Assembly
1000  0   200   imp:n=0             $ Outside world

c ============================================================
c SURFACES
c ============================================================

c Pin surfaces (in universe, centered at origin)
100   cz  0.4095    $ Fuel pellet radius
101   cz  0.4178    $ Inner clad radius
102   cz  0.4750    $ Outer clad radius

c Guide tube surfaces
110   cz  0.5715    $ Guide tube inner
111   cz  0.6121    $ Guide tube outer

c Instrumentation tube surfaces
120   cz  0.5590    $ Instrument tube inner
121   cz  0.6121    $ Instrument tube outer

c Assembly boundary
c 17 × 1.26 cm pitch = 21.42 cm → ±10.71 cm
200   rpp  -10.71 10.71  -10.71 10.71  0 366    $ Active height 366 cm

c ============================================================
c MATERIALS
c ============================================================

m1   $ UO2 fuel, 4.5% enriched
    92234.70c  3.80e-4
    92235.70c  0.0450
    92238.70c  0.9550
     8016.70c  2.0000

m2   $ Zircaloy-4 clad
    40000.60c  0.9821
    26000.50c  0.0022
    24000.50c  0.0010
    50000.35c  0.0147

m3   $ Light water (typical PWR density)
     1001.70c  2.0
     8016.70c  1.0
mt3  lwtr.13t    $ 350K (typical PWR)

c ============================================================
c PROBLEM SPECIFICATION
c ============================================================

mode n
kcode 10000 1.0 50 250
ksrc 0 0 180
```

**Usage Notes**:
- Modify enrichment in M1 as needed (3-5% typical)
- Adjust water density for hot vs. cold conditions
- Guide tube pattern is standard for Westinghouse 17×17
- See `templates/pwr_17x17_assembly.i` for full file

[... continue with BWR, VVER, CANDU templates ...]

## HTGR Hexagonal Assembly

### Prismatic Block Template

**Specifications**:
- Hexagonal graphite block
- Fuel channels: 6-31 per block (design dependent)
- Coolant channels: interspersed
- Pitch: 1.88-3.6 cm (design dependent)

**Template**:
```mcnp
c ============================================================
c HTGR HEXAGONAL FUEL ASSEMBLY
c ============================================================

c ------------------------------------------------------------
c UNIVERSE DEFINITIONS
c ------------------------------------------------------------

c Fuel compact universe (u=100)
100  1  -1.75   -100        u=100  imp:n=1  $ Fuel compact
101  2  -1.70    100  -101  u=100  imp:n=1  $ Graphite channel

c Coolant channel universe (u=200)
200  3  -5e-3   -200        u=200  imp:n=1  $ Helium coolant
201  2  -1.70    200  -201  u=200  imp:n=1  $ Graphite

c Graphite cell universe (u=300)
300  2  -1.70   -300        u=300  imp:n=1  $ Solid graphite

c ------------------------------------------------------------
c LATTICE ASSEMBLY (u=400) - LAT=2 HEXAGONAL
c ------------------------------------------------------------
c 13×13 hexagonal pattern (R = 1.6 cm → pitch = 2.77 cm)
400  0  -400  u=400  lat=2  imp:n=1  fill=-6:6 -6:6 0:0
     300 300 300 300 300 300 300 300 300 300 300 300 300  $j=6
      300 300 300 300 300 300 100 100 100 300 300 300 300  $j=5
       300 300 300 300 300 100 100 200 100 100 300 300 300  $j=4
        300 300 300 100 100 100 100 100 100 100 100 300 300  $j=3
         300 300 100 100 100 100 100 100 100 100 100 100 300  $j=2
          300 100 100 200 100 100 200 100 100 200 100 100 300  $j=1
           300 100 100 100 100 100 100 100 100 100 100 300  $j=0
            300 100 200 100 100 200 100 100 200 100 300  $j=-1
             300 100 100 100 100 100 100 100 100 300  $j=-2
              300 100 100 200 100 100 200 100 100 300  $j=-3
               300 100 100 100 100 100 100 100 300  $j=-4
                300 300 100 100 100 100 100 300 300  $j=-5
                 300 300 300 100 100 100 300 300 300  $j=-6

c ------------------------------------------------------------
c GLOBAL PLACEMENT
c ------------------------------------------------------------
999   0  -400  fill=400  imp:n=1
1000  0   400   imp:n=0

c ============================================================
c SURFACES
c ============================================================

c Channel surfaces (in universe, centered at origin)
100   cz  0.635     $ Fuel compact radius
101   cz  0.793     $ Fuel channel outer
200   cz  0.476     $ Coolant channel radius
201   cz  0.635     $ Coolant channel outer
300   cz  0.793     $ Graphite cell radius

c Assembly boundary (RHP - 9 values)
c origin(3) height_vector(3) R_vector(3)
400   rhp  0 0 0   0 0 68   0 1.6 0    $ Hex block, height=68 cm, R=1.6 cm

c ============================================================
c MATERIALS
c ============================================================

m1   $ Fuel compact (homogenized - or use explicit TRISO)
     6012.00c  0.40    $ Carbon (40% from matrix)
    92235.00c  0.008   $ U-235 (enriched)
    92238.00c  0.032   $ U-238
     8016.00c  0.04    $ Oxygen
    14000.60c  0.06    $ Silicon (from SiC)
mt1  grph.18t         $ 600K graphite thermal scattering

m2   $ Graphite block
     6012.00c  0.9890
     6013.00c  0.0110
mt2  grph.18t

m3   $ Helium coolant
     2004.00c  1.0

c ============================================================
c PROBLEM SPECIFICATION
c ============================================================

mode n
kcode 10000 1.0 50 250
ksrc 0 0 34
```

**Usage Notes**:
- RHP surface: **MUST use 9 values** (origin + height vector + R vector)
- Hexagonal pitch = R × √3 = 1.6 × 1.732 = 2.77 cm
- Thermal scattering (MT) **ESSENTIAL** for graphite
- See `templates/htgr_hex_assembly.i` for full file

[... continue with pebble bed, fast reactor hex assemblies ...]

## TRISO Particle Template (Supplemental)

### 5-Layer Coating Structure

**Application**: Detailed fuel modeling in HTGR compacts

```mcnp
c TRISO particle universe (u=100)
1  1  -10.8   -1       u=100  vol=6.545e-5  $ Kernel (UO2, 500 μm dia)
2  2  -0.98    1  -2   u=100                $ Buffer (100 μm thick)
3  3  -1.85    2  -3   u=100                $ IPyC (40 μm)
4  4  -3.20    3  -4   u=100                $ SiC (35 μm)
5  5  -1.86    4  -5   u=100                $ OPyC (40 μm)
6  6  -1.75    5       u=100                $ Matrix

c Surfaces
1  so  0.02500    $ Kernel
2  so  0.03500    $ Buffer
3  so  0.03900    $ IPyC
4  so  0.04250    $ SiC
5  so  0.04650    $ OPyC
```

**Materials**:
```mcnp
m1  $ UO2 kernel (19.75% enriched)
   92234.00c  3.34e-3
   92235.00c  1.996e-1
   92236.00c  1.93e-4
   92238.00c  7.968e-1
    8016.00c  1.3613

m2  $ Buffer (porous carbon)
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t

m3  $ IPyC (dense PyC)
    6012.00c  0.9890
    6013.00c  0.0110
mt3 grph.18t

m4  $ SiC
   14000.60c  0.5
    6012.00c  0.495
    6013.00c  0.005

m5  $ OPyC (dense PyC)
    6012.00c  0.9890
    6013.00c  0.0110
mt5 grph.18t

m6  $ SiC matrix
   14000.60c  0.5
    6012.00c  0.495
    6013.00c  0.005
```

[... continue with fast reactor, CANDU templates ...]

## Complete Assembly Examples

[... full working examples for each reactor type ...]

## References

- PWR: Westinghouse AP1000 design
- HTGR: Prismatic modular reactor designs
- Fast reactor: EBR-II, FFTF designs
- TRISO: AGR-1 experiment specifications
```

### Phase 3: Example Files

#### 3.1 Create example_geometries/12_concentric_cylinders.i

**File**: `.claude/skills/mcnp-geometry-builder/example_geometries/12_concentric_cylinders.i`

```mcnp
c ============================================================
c CONCENTRIC CYLINDER EXAMPLE
c 7-layer capsule structure (AGR-1 pattern)
c ============================================================
c
c Demonstrates:
c  - Multiple concentric cylinders (C/Z off-axis)
c  - Thin gap regions (< 1 mm)
c  - Shared axial planes
c  - Realistic reactor component geometry
c
c ============================================================

c ------------------------------------------------------------
c CELLS
c ------------------------------------------------------------

c Concentric layers (all centered at 25.337, -25.337)
1   1  -10.9   -1              -10 11  imp:n=1  $ Fuel compact
2   0          1  -2           -10 11  imp:n=1  $ Gas gap (0.6 mm)
3   2  -1.75   2  -3           -10 11  imp:n=1  $ Graphite holder
4   0          3  -4           -10 11  imp:n=1  $ Gap (7 mm)
5   3  -8.0    4  -5           -10 11  imp:n=1  $ SS wall (3.4 mm)
6   4  -13.3   5  -6           -10 11  imp:n=1  $ Hafnium shroud (2.5 mm)
7   3  -8.0    6  -7           -10 11  imp:n=1  $ Outer wall (13.8 mm)
8   5  -1.2e-3 7              -10 11  imp:n=1  $ Air outside
9   0          11                      imp:n=0  $ Graveyard

c ------------------------------------------------------------
c SURFACES
c ------------------------------------------------------------

c Concentric cylinders (all c/z with same center)
1   c/z  25.337  -25.337  0.6350    $ Compact (6.35 mm)
2   c/z  25.337  -25.337  0.6413    $ Gas gap outer (6.41 mm)
3   c/z  25.337  -25.337  1.5191    $ Holder outer (15.19 mm)
4   c/z  25.337  -25.337  1.5875    $ Gap outer (15.88 mm)
5   c/z  25.337  -25.337  1.6218    $ SS wall outer (16.22 mm)
6   c/z  25.337  -25.337  1.6472    $ Hf shroud outer (16.47 mm)
7   c/z  25.337  -25.337  1.7856    $ Outer wall outer (17.86 mm)

c Axial planes (shared by all cylinders)
10  pz  0.0       $ Bottom
11  pz  50.0      $ Top

c ------------------------------------------------------------
c DATA CARDS
c ------------------------------------------------------------

mode n
sdef pos=25.337 -25.337 25  erg=2.0
nps 10000

c Materials
m1  $ Fuel compact (UCO simplified)
   92235.00c  0.20
   92238.00c  0.80
    6012.00c  0.50
    8016.00c  1.50

m2  $ Graphite holder
    6012.00c  0.9890
    6013.00c  0.0110
mt2 grph.18t

m3  $ Stainless steel 316L
   26000.50c  0.65
   24000.50c  0.17
   28000.50c  0.12
   42000.60c  0.025
   25055.70c  0.020
   14000.60c  0.010
   15031.70c  0.005

m4  $ Hafnium
   72000.60c  1.0

m5  $ Air
    7014.70c  0.8
    8016.70c  0.2

c ============================================================
c NOTES
c ============================================================
c
c Key Features:
c 1. All C/Z surfaces share center (25.337, -25.337)
c 2. Radii strictly increasing (6.35 → 17.86 mm)
c 3. Thin gaps (0.6 mm, 7 mm) carefully sized
c 4. Axial planes shared across all layers
c
c Verification:
c  - Plot: mcnp6 inp=12_concentric_cylinders.i ip
c  - Origin: 25.337 -25.337 25
c  - Extent: 5 5 50
c  - Basis: 1 0 0  0 1 0
c
c Expected: 7 concentric circles in XY view
c
c ============================================================
```

#### 3.2 Create example_geometries/13_multi_scale_triso.i

**File**: `.claude/skills/mcnp-geometry-builder/example_geometries/13_multi_scale_triso.i`

**Content**: Complete TRISO particle example showing μm to cm scale...

### Phase 4: Python Tools

#### 4.1 Create scripts/concentric_geometry_generator.py

**File**: `.claude/skills/mcnp-geometry-builder/scripts/concentric_geometry_generator.py`

```python
"""
Concentric Geometry Generator for MCNP
Generate nested sphere or cylinder cell/surface cards
"""

def generate_concentric_spheres(radii, materials, densities, universe=None):
    """
    Generate MCNP cell and surface cards for concentric spheres

    Args:
        radii: List of radii (cm), increasing order
        materials: List of material numbers
        densities: List of densities (negative for g/cm³)
        universe: Universe number (optional)

    Returns:
        tuple: (cell_cards, surface_cards)
    """

    # Validate inputs
    if len(radii) != len(materials) or len(radii) != len(densities):
        raise ValueError("radii, materials, and densities must have same length")

    if radii != sorted(radii):
        raise ValueError("radii must be in increasing order")

    n = len(radii)
    cell_cards = []
    surface_cards = []

    # Generate cells
    u_spec = f"  u={universe}" if universe else ""

    # Inner sphere
    cell_cards.append(f"1    {materials[0]}  {densities[0]:.3f}  -1{u_spec}  $ Core")

    # Intermediate shells
    for i in range(1, n):
        cell_cards.append(
            f"{i+1}    {materials[i]}  {densities[i]:.3f}  {i} -{i+1}{u_spec}  $ Layer {i}"
        )

    # Exterior (if universe, no exterior cell; if global, add void)
    if not universe:
        cell_cards.append(f"{n+1}    0  {n}  $ Exterior")
    else:
        cell_cards.append(f"{n+1}    {materials[-1]}  {densities[-1]:.3f}  {n}{u_spec}  $ Exterior")

    # Generate surfaces
    for i, r in enumerate(radii, start=1):
        surface_cards.append(f"{i}    so  {r:.6f}    $ R = {r*10000:.1f} μm")

    cells = "\n".join(cell_cards)
    surfaces = "\n".join(surface_cards)

    return cells, surfaces


def generate_concentric_cylinders(radii, height, materials, densities,
                                  center=(0, 0), universe=None, z_planes=None):
    """
    Generate MCNP cell and surface cards for concentric cylinders

    Args:
        radii: List of radii (cm), increasing order
        height: Cylinder height (cm) or (z_min, z_max) tuple
        materials: List of material numbers
        densities: List of densities (negative for g/cm³)
        center: (x, y) center coordinates (default origin)
        universe: Universe number (optional)
        z_planes: (z_min_surf, z_max_surf) surface numbers (optional)

    Returns:
        tuple: (cell_cards, surface_cards)
    """

    # Validate inputs
    if len(radii) != len(materials) or len(radii) != len(densities):
        raise ValueError("radii, materials, and densities must have same length")

    if radii != sorted(radii):
        raise ValueError("radii must be in increasing order")

    # Parse height
    if isinstance(height, tuple):
        z_min, z_max = height
    else:
        z_min, z_max = 0, height

    # Parse z-planes
    if z_planes:
        z_min_surf, z_max_surf = z_planes
        z_spec = f"  -{z_min_surf} {z_max_surf}"
    else:
        z_min_surf = 1000
        z_max_surf = 1001
        z_spec = f"  -{z_min_surf} {z_max_surf}"

    n = len(radii)
    cell_cards = []
    surface_cards = []

    cx, cy = center
    u_spec = f"  u={universe}" if universe else ""

    # Determine surface type
    if cx == 0 and cy == 0:
        surf_type = "cz"
        surf_params = lambda r: f"{r:.4f}"
    else:
        surf_type = "c/z"
        surf_params = lambda r: f"{cx:.6f}  {cy:.6f}  {r:.4f}"

    # Generate cells
    # Inner cylinder
    cell_cards.append(f"1    {materials[0]}  {densities[0]:.3f}  -1{z_spec}{u_spec}  $ Core")

    # Intermediate shells
    for i in range(1, n):
        cell_cards.append(
            f"{i+1}    {materials[i]}  {densities[i]:.3f}  {i} -{i+1}{z_spec}{u_spec}  $ Layer {i}"
        )

    # Exterior
    if not universe:
        cell_cards.append(f"{n+1}    0  {n}{z_spec}  $ Exterior")
    else:
        cell_cards.append(f"{n+1}    {materials[-1]}  {densities[-1]:.3f}  {n}{z_spec}{u_spec}  $ Exterior")

    # Generate surfaces
    for i, r in enumerate(radii, start=1):
        surface_cards.append(f"{i}    {surf_type}  {surf_params(r)}    $ R = {r*10:.1f} mm")

    # Z-planes if not provided
    if not z_planes:
        surface_cards.append(f"{z_min_surf}    pz  {z_min:.4f}    $ Bottom")
        surface_cards.append(f"{z_max_surf}    pz  {z_max:.4f}    $ Top")

    cells = "\n".join(cell_cards)
    surfaces = "\n".join(surface_cards)

    return cells, surfaces


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("MCNP Concentric Geometry Generator")
    print("="*60)

    # Example 1: TRISO particle (concentric spheres)
    print("\nExample 1: TRISO Particle (5 layers)")
    print("-"*60)

    radii = [0.02500, 0.03500, 0.03900, 0.04250, 0.04650]
    materials = [1, 2, 3, 4, 5, 6]  # kernel, buffer, ipyc, sic, opyc, matrix
    densities = [-10.8, -0.98, -1.85, -3.20, -1.86, -1.75]

    cells, surfaces = generate_concentric_spheres(radii, materials, densities, universe=100)

    print("c Cells (u=100):")
    print(cells)
    print("\nc Surfaces:")
    print(surfaces)

    # Example 2: Fuel pin (concentric cylinders, centered)
    print("\n\nExample 2: PWR Fuel Pin (concentric cylinders)")
    print("-"*60)

    radii = [0.4095, 0.4178, 0.4750]
    materials = [1, 0, 2, 3]  # fuel, gap, clad, coolant
    densities = [-10.5, 0, -6.5, -1.0]

    cells, surfaces = generate_concentric_cylinders(
        radii, 360.0, materials, densities, universe=10
    )

    print("c Cells (u=10):")
    print(cells)
    print("\nc Surfaces:")
    print(surfaces)

    # Example 3: Capsule (off-axis cylinders)
    print("\n\nExample 3: Off-Axis Capsule (7 layers)")
    print("-"*60)

    radii = [0.6350, 0.6413, 1.5191, 1.5875, 1.6218, 1.6472, 1.7856]
    materials = [1, 0, 2, 0, 3, 4, 3, 5]  # compact, gap, graphite, gap, SS, Hf, SS, air
    densities = [-10.9, 0, -1.75, 0, -8.0, -13.3, -8.0, -1.2e-3]
    center = (25.337, -25.337)

    cells, surfaces = generate_concentric_cylinders(
        radii, (0, 129.54), materials, densities, center=center
    )

    print("c Cells:")
    print(cells)
    print("\nc Surfaces:")
    print(surfaces)
```

---

## SUCCESS CRITERIA

### After Phase 1 (SKILL.md updates)
- [ ] User asks "How do I model a fuel pin with 4 concentric layers?"
  - ✅ Skill provides surface type guidance (CZ vs C/Z)
  - ✅ Skill shows complete cell/surface pattern
  - ✅ Skill explains when to use universe

- [ ] User asks "I need to model TRISO particles (μm scale) and a core (meter scale)"
  - ✅ Skill provides precision guidelines
  - ✅ Skill shows unit conversion examples
  - ✅ Skill references multi-scale section

- [ ] User asks "How do I position lattices at different locations?"
  - ✅ Skill shows fill transformation syntax
  - ✅ Skill provides off-axis cylinder example
  - ✅ Skill explains translation vectors

### After Phase 2 (Reference files)
- [ ] User searches for "concentric cylinder pattern"
  - ✅ Finds concentric_geometry_reference.md
  - ✅ Gets 10+ complete examples
  - ✅ Understands C/Z vs CZ selection

- [ ] User needs "PWR assembly template"
  - ✅ Finds reactor_assembly_templates.md
  - ✅ Gets production-ready 17×17 template
  - ✅ Can modify for different enrichment/design

### After Phase 3 (Example files)
- [ ] User runs example_geometries/12_concentric_cylinders.i
  - ✅ MCNP plots show 7 concentric circles
  - ✅ No lost particles
  - ✅ User understands pattern for own model

### After Phase 4 (Python tools)
- [ ] User runs concentric_geometry_generator.py
  - ✅ Generates correct TRISO cell/surface cards
  - ✅ Generates fuel pin geometry
  - ✅ Handles off-axis positioning

### Overall Integration Test
- [ ] User builds AGR-1-style model from scratch
  - ✅ Uses multi-scale precision guidance
  - ✅ Uses concentric cylinder templates
  - ✅ Uses fill transformations for stacks
  - ✅ Validates geometry without errors

---

## DEPENDENCIES

**Depends On**:
- mcnp-lattice-builder (MUST be fixed first for fill guidance)
- mcnp-material-builder (for thermal scattering in examples)

**Blocks**:
- None (other skills can proceed independently)

---

## ESTIMATED EFFORT

| Phase | Time | Priority |
|-------|------|----------|
| Phase 1: SKILL.md updates | 1.0 hour | HIGH |
| Phase 2: Reference files (3 files) | 1.5 hours | HIGH |
| Phase 3: Example files (2 files) | 0.5 hour | MEDIUM |
| Phase 4: Python tool | 0.5 hour | MEDIUM |
| **TOTAL** | **3.5 hours** | - |

---

## EXECUTION ORDER

1. ✅ Read current mcnp-geometry-builder/SKILL.md (DONE)
2. ⬜ Update SKILL.md with 4 new sections (Phase 1)
3. ⬜ Create surface_selection_patterns.md (Phase 2.1)
4. ⬜ Create concentric_geometry_reference.md (Phase 2.2)
5. ⬜ Create reactor_assembly_templates.md (Phase 2.3)
6. ⬜ Create example_geometries/12_concentric_cylinders.i (Phase 3.1)
7. ⬜ Create example_geometries/13_multi_scale_triso.i (Phase 3.2)
8. ⬜ Create scripts/concentric_geometry_generator.py (Phase 4)
9. ⬜ Test with user queries
10. ⬜ Validate examples run without errors

---

## NOTES

**Relation to REVISED plan**:
- This plan complements mcnp-lattice-builder refinement
- Focuses on geometry building PATTERNS not lattice mechanics
- Provides reactor-specific templates (both rectangular and hexagonal assemblies)
- Generalizes to ALL complex reactor models (not just TRISO-specific)

**Key Improvements**:
1. Multi-scale precision guidance (μm to meters)
2. Surface type selection decision trees
3. Concentric geometry patterns (spheres and cylinders)
4. Reactor assembly templates (PWR, HTGR, fast reactors)
5. Fill transformation examples (off-axis positioning)

**File Organization**:
- All files in skill root directory (no assets/ subdirectory)
- References at root: `surface_selection_patterns.md`, etc.
- Examples in `example_geometries/`
- Scripts in `scripts/`
- Templates in `templates/`

---

**END OF REFINEMENT PLAN**

**Next Action**: Execute Phase 1 (SKILL.md updates) immediately after mcnp-lattice-builder is complete.
