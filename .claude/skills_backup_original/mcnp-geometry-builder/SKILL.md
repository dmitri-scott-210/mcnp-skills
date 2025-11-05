---
category: A
name: mcnp-geometry-builder
description: Build MCNP geometry using cell and surface cards with Boolean operations, transformations, and lattices
activation_keywords:
  - geometry
  - cell card
  - surface card
  - Boolean
  - lattice
  - universe
  - transformation
  - TRCL
---

# MCNP Geometry Builder Skill

## Purpose
This skill guides users in creating MCNP geometry definitions using cell and surface cards. It covers Boolean operations, surface types (planes, spheres, cylinders, macrobodies), transformations, universes, and lattices for complex repeated structures.

## When to Use This Skill
- Defining spatial regions (cells) for particle transport
- Creating geometric boundaries (surfaces)
- Building complex geometry with Boolean operations
- Implementing repeated structures (lattices, arrays)
- Transforming geometry (rotation, translation)
- Organizing multi-component systems (universes)
- Troubleshooting "lost particle" or geometry errors

## Prerequisites
- MCNP input structure understanding (mcnp-input-builder skill)
- Basic 3D geometry and coordinate systems
- Understanding of Boolean logic (AND, OR, NOT)

## Core Concepts

### Constructive Solid Geometry (CSG)
MCNP uses CSG: geometry defined by Boolean combinations of half-spaces.

**Half-Space**: Region on one side of a surface
- **Negative sense** (`-n`): "Inside" surface n
- **Positive sense** (`+n`): "Outside" surface n

**Example (Sphere)**:
```
1  SO  10.0              $ Sphere radius 10 cm

c Cell inside sphere:
1  1  -1.0  -1  IMP:N=1  $ -1 = inside sphere 1

c Cell outside sphere:
2  0       1  IMP:N=0    $ 1 = outside sphere 1 (+ implied)
```

### Cell Card Format
```
j  m  d  geometry  param₁  param₂  ...
```

**Fields**:
- `j`: Cell number (1-99999999, unique)
- `m`: Material number (0=void, 1-99999999=defined material)
- `d`: Density
  - Positive: g/cm³ (mass density)
  - Negative: atoms/(b·cm) (atomic density)
  - Omit for void (m=0)
- `geometry`: Boolean expression of surfaces
- `param`: Cell parameters (IMP, VOL, TMP, U, FILL, TRCL, etc.)

**Example**:
```
1  1  -1.0  -1  2  -3  IMP:N=1  VOL=1000  $ Water cell
c  ^  ^    ^    ^         ^         ^
c  j  m    d    geom      imp       volume
```

### Surface Card Format
```
j  n  mnemonic  entry₁  entry₂  ...
```

**Fields**:
- `j`: Surface number (1-99999999, unique)
- `n`: Transformation number (optional, references *TRn)
- `mnemonic`: Surface type (SO, PX, C/Z, etc.)
- `entry`: Geometric parameters

**Example**:
```
1  SO  10.0              $ Sphere at origin, R=10
2  PX  5.0               $ Plane at x=5
3  C/Z  0 0  2.0         $ Cylinder along z, R=2
```

### Boolean Operators

**Intersection** (space or blank):
```
-1  2  -3     $ Inside 1 AND outside 2 AND inside 3
```

**Union** (colon `:`):
```
-1 : -2       $ Inside 1 OR inside 2
```

**Complement** (`#`):
```
#10           $ NOT in cell 10 (everything except cell 10)
```

**Parentheses** (grouping):
```
(-1  2) : (-3  4)    $ (Inside 1 AND outside 2) OR (Inside 3 AND outside 4)
```

### Coordinate System (Default: Cartesian)
- Origin: (0, 0, 0)
- Axes: x, y, z (right-handed)
- Units: cm (all lengths)

---

## Decision Tree: Geometry Construction

```
START: Need to define geometry
  |
  +--> What type of geometry?
       |
       +--[Simple (1-5 regions)]---> Direct cell/surface definition
       |                             ├─> Identify regions (cells)
       |                             ├─> Define boundaries (surfaces)
       |                             └─> Write Boolean expressions
       |
       +--[Moderate (5-20 regions)]-> Group by material/function
       |                             ├─> Number scheme (1-99=core, 100-199=reflector)
       |                             ├─> Use macrobodies for complex shapes
       |                             └─> Comment sections clearly
       |
       +--[Complex (20+ regions)]---> Use universes + modular design
       |                             ├─> Define reusable components (universes)
       |                             ├─> Main geometry fills universes
       |                             └─> Consider lattices for arrays
       |
       +--[Repeated Structure]-------> Use lattice (LAT=1 or LAT=2)
                                      ├─> LAT=1: Rectangular array
                                      ├─> LAT=2: Hexagonal array
                                      └─> Index fill with universe numbers
```

---

## Surface Types

### Planes

**P** (General plane: Ax + By + Cz - D = 0):
```
1  P  1 0 0  5          $ x = 5
2  P  0 1 0  -3         $ y = -3
3  P  1 1 0  0          $ x + y = 0 (45° diagonal)
```

**PX, PY, PZ** (Axis-aligned planes):
```
1  PX  5.0              $ Plane at x = 5
2  PY  -3.0             $ Plane at y = -3
3  PZ  10.0             $ Plane at z = 10
```

**Usage**:
- Slab geometries
- Box boundaries
- Splitting regions along axes

### Spheres

**SO** (Sphere at origin):
```
1  SO  10.0             $ x² + y² + z² = 100
```

**S** (General sphere):
```
1  S  5 0 0  10.0       $ Center (5,0,0), R=10
```

**SX, SY, SZ** (Spheres centered on axis):
```
1  SX  5  10.0          $ Center (5,0,0), R=10
2  SY  3  8.0           $ Center (0,3,0), R=8
3  SZ  -2  5.0          $ Center (0,0,-2), R=5
```

**Usage**:
- Point source geometries
- Spherical shells (nested spheres)
- Importance splitting regions

### Cylinders

**C/X** (Cylinder parallel to x-axis):
```
1  C/X  0 0  10.0       $ y² + z² = 100 (all x)
```

**C/Y** (Cylinder parallel to y-axis):
```
2  C/Y  0 0  5.0        $ x² + z² = 25 (all y)
```

**C/Z** (Cylinder parallel to z-axis):
```
3  C/Z  0 0  8.0        $ x² + y² = 64 (all z)
```

**CX, CY, CZ** (Infinite cylinders on axis):
```
1  CX  10.0             $ On x-axis, R=10
2  CY  5.0              $ On y-axis, R=5
3  CZ  8.0              $ On z-axis, R=8
```

**Usage**:
- Fuel pins/rods
- Pipes, ducts
- Cylindrical detectors
- Reactor cores (z-axis alignment)

### Cones

**K/X, K/Y, K/Z** (Cone, axis parallel to x/y/z):
```
1  K/Z  0 0 1  1        $ Apex (0,0,1), t²=1, opens along z
c       ^y ^z ^h ^t²
```

**KX, KY, KZ** (Cone at origin on axis):
```
1  KZ  5  1             $ Apex (0,0,5), t²=1
c      ^z₀ ^t²
```

**Usage**:
- Nozzles, funnels
- Beam collimators
- Truncated with planes for finite cones

### General Quadric

**GQ** (General quadratic):
```
GQ  A B C D E F G H J K
c   Ax² + By² + Cz² + Dxy + Eyz + Fzx + Gx + Hy + Jz + K = 0
```

**Example (Hyperboloid)**:
```
1  GQ  1 1 -1  0 0 0  0 0 0  -100
```

**SQ** (Special quadric, A=B=C):
```
1  SQ  1  0 0 0  0 0 0  -100         $ Sphere x²+y²+z²=100
```

**Usage**:
- Exotic shapes (hyperboloids, paraboloids)
- Optical surfaces
- Custom geometries not covered by standard types

---

## Macrobodies (Shortcuts)

Macrobodies simplify complex shapes by defining them with fewer parameters.

### BOX (Rectangular Parallelepiped)
```
BOX  x y z  v₁x v₁y v₁z  v₂x v₂y v₂z  v₃x v₃y v₃z
     ^corner ^vector1    ^vector2     ^vector3
```

**Example**:
```
1  BOX  0 0 0  10 0 0  0 5 0  0 0 8  $ 10×5×8 cm box at origin
```

### RPP (Right Parallelepiped, axis-aligned)
```
RPP  xmin xmax  ymin ymax  zmin zmax
```

**Example**:
```
1  RPP  -5 5  -5 5  0 10     $ 10×10×10 cm box
2  RPP  0 100  0 50  0 200   $ Rectangular block
```

**Usage**: Most common for axis-aligned boxes (rooms, blocks, slabs)

### SPH (Sphere)
```
SPH  x y z  R
```

**Example**:
```
1  SPH  0 0 0  10.0          $ Same as SO 10.0
2  SPH  10 5 0  8.0          $ Same as S 10 5 0  8.0
```

**Usage**: Alternative to SO/S, more explicit

### RCC (Right Circular Cylinder)
```
RCC  x y z  vx vy vz  R
     ^base  ^axis     ^radius
```

**Example**:
```
1  RCC  0 0 0  0 0 100  5.0  $ Cylinder h=100, R=5 along z
2  RCC  0 0 0  100 0 0  3.0  $ Cylinder h=100, R=3 along x
```

**Usage**: Finite cylinders (fuel rods, pipes with end caps)

### RHP (Right Hexagonal Prism)
```
RHP  x y z  vx vy vz  ux uy uz  s
     ^base  ^axis     ^side-vec ^inradius
```

**Example**:
```
1  RHP  0 0 0  0 0 100  1 0 0  5.0
c       ^base  ^height(z) ^side(x) ^R_in=5
```

**HEX** (Simplified hexprism on z-axis):
```
1  HEX  0 0 0  0 0 100  5.0  $ Same as above if aligned
```

**Usage**: Hexagonal fuel assemblies (VVER, some research reactors)

### TRC (Truncated Right-Angle Cone)
```
TRC  x y z  vx vy vz  R₁  R₂
     ^base  ^axis     ^R_base ^R_top
```

**Example**:
```
1  TRC  0 0 0  0 0 100  10  5   $ Cone: R=10 at base, R=5 at top
```

**Usage**: Tapered structures, conical transitions

### WED (Wedge)
```
WED  x y z  v₁x v₁y v₁z  v₂x v₂y v₂z  v₃x v₃y v₃z
     ^corner ^vec1       ^vec2        ^vec3(height)
```

**Example**:
```
1  WED  0 0 0  10 0 0  0 5 0  0 0 8
```

**Usage**: Angled blocks, ramps

### ARB (Arbitrary Polyhedron, up to 8 vertices)
```
ARB  x₁ y₁ z₁  x₂ y₂ z₂ ... x₈ y₈ z₈  f₁ f₂ f₃ f₄ f₅ f₆
     ^vertices (up to 8)              ^face connectivity
```

**Example (Tetrahedron)**:
```
1  ARB  0 0 0  10 0 0  5 8.66 0  5 2.89 8.16  &
        0 0 0  0 0 0  0 0 0  0 0 0  &
        1234  124  143  234
```

**Usage**: Custom polyhedra (complex structures, odd angles)

---

## Use Case 1: Nested Spherical Shells

**Scenario**: Source at center, three concentric spherical shells (water, concrete, lead).

**Geometry**:
```
c =================================================================
c Nested Spherical Shells
c =================================================================

c --- Cell Cards ---
1    1  -1.0   -1           IMP:N=1  VOL=4188.79    $ Water (R<10)
2    2  -2.3   1  -2        IMP:N=1                 $ Concrete (10<R<20)
3    3  -11.34  2  -3       IMP:N=1                 $ Lead (20<R<30)
4    0         3            IMP:N=0                 $ Graveyard

c --- Surface Cards ---
1    SO  10.0                                       $ R = 10 cm
2    SO  20.0                                       $ R = 20 cm
3    SO  30.0                                       $ R = 30 cm
```

**Key Points**:
- Surface sense: `-1` (inside), `1` (outside)
- Cell 2 geometry: `1 -2` = outside surf 1 AND inside surf 2
- VOL specified for cell 1 (F4 tally normalization)
- Graveyard (IMP:N=0) kills escaping particles

---

## Use Case 2: Rectangular Box with Cylindrical Void

**Scenario**: Aluminum block with cylindrical hole through center along z-axis.

**Geometry**:
```
c =================================================================
c Box with Cylindrical Void
c =================================================================

c --- Cell Cards ---
1    1  -2.7   -1  2        IMP:N=1                 $ Aluminum (box minus cylinder)
2    0         -2           IMP:N=1                 $ Void cylinder
3    0         1            IMP:N=0                 $ Graveyard

c --- Surface Cards ---
1    RPP  -10 10  -10 10  -20 20                    $ Box (20×20×40 cm)
2    C/Z  0 0  5                                    $ Cylinder R=5 along z
```

**Key Points**:
- Cell 1: `-1 2` = inside box AND outside cylinder
- RPP macrobody: axis-aligned box (simpler than 6 planes)
- C/Z: infinite cylinder (truncated by box in this case)
- Cell 2: Pure void inside cylinder (could be source region)

---

## Use Case 3: Multi-Layer Slab Geometry

**Scenario**: Planar layers (steel, polyethylene, lead) for shielding study.

**Geometry**:
```
c =================================================================
c Multi-Layer Slab Geometry
c =================================================================

c --- Cell Cards ---
1    0          -1         IMP:N=1                  $ Source void (x<0)
10   1  -7.86   1  -2      IMP:N=2                  $ Steel (0<x<10)
20   2  -0.94   2  -3      IMP:N=4                  $ Polyethylene (10<x<30)
30   3  -11.34  3  -4      IMP:N=8                  $ Lead (30<x<45)
40   0          4  -5      IMP:N=16                 $ Detector void (45<x<50)
999  0          -1:5       IMP:N=0                  $ Graveyard (x<-1 or x>50)

c --- Surface Cards ---
1    PX  0.0                                        $ x = 0
2    PX  10.0                                       $ x = 10
3    PX  30.0                                       $ x = 30
4    PX  45.0                                       $ x = 45
5    PX  50.0                                       $ x = 50
```

**Key Points**:
- PX surfaces: planes perpendicular to x-axis
- Cell 10: `1 -2` = between x=0 and x=10
- Graveyard uses union: `-1:5` = x<0 OR x>50
- Importance increases through layers (variance reduction)

---

## Use Case 4: Fuel Pin (Cylindrical)

**Scenario**: UO₂ fuel pellet, zircaloy cladding, water coolant.

**Geometry**:
```
c =================================================================
c Fuel Pin (Cylindrical Geometry)
c =================================================================

c --- Cell Cards ---
1    1  -10.5  -1  -3      IMP:N=1                  $ Fuel (R<0.5, |z|<100)
2    2  -6.5   1  -2  -3   IMP:N=1                  $ Clad (0.5<R<0.6)
3    3  -1.0   2  -3       IMP:N=1                  $ Coolant (R>0.6)
4    0         3           IMP:N=0                  $ Graveyard (|z|>100)

c --- Surface Cards ---
1    C/Z  0 0  0.5                                  $ Fuel outer radius
2    C/Z  0 0  0.6                                  $ Clad outer radius
3    PZ   100                                       $ Top plane
3    PZ  -100                                       $ Bottom plane (same number, union)

c --- Alternate with RCC ---
c 1    RCC  0 0 -100  0 0 200  0.5                 $ Fuel (macrobody)
c 2    RCC  0 0 -100  0 0 200  0.6                 $ Clad outer (macrobody)
```

**Key Points**:
- C/Z: infinite cylinder, truncated by PZ planes
- Cell 1: `-1 -3` = inside fuel radius AND below z=100
- Cell 2: `1 -2 -3` = outside fuel AND inside clad AND below z=100
- Alternative: Use RCC macrobodies for finite cylinders

---

## Use Case 5: Lattice (3×3 Pin Array)

**Scenario**: 3×3 array of fuel pins in square lattice.

**Geometry**:
```
c =================================================================
c 3×3 Pin Lattice
c =================================================================

c --- Pin Universe (U=1) ---
1    1  -10.5  -1  U=1  IMP:N=1                    $ Fuel
2    2  -6.5   1 -2  U=1  IMP:N=1                  $ Clad
3    3  -1.0   2  U=1  IMP:N=1                     $ Coolant

c --- Lattice Element Surface ---
10   RPP  -0.63  0.63  -0.63  0.63  -100  100      $ Pin pitch (1.26 cm)

c --- Lattice Cell (U=2) ---
100  0  -10  LAT=1  U=2  FILL=-1:1  -1:1  0:0  &
                          1 1 1  &
                          1 1 1  &
                          1 1 1  IMP:N=1

c --- Main Geometry ---
1000  0  -100  FILL=2  IMP:N=1                     $ Fill with lattice universe
9999  0  100   IMP:N=0                             $ Graveyard

c --- Pin Surfaces ---
1    C/Z  0 0  0.5                                 $ Fuel radius
2    C/Z  0 0  0.6                                 $ Clad outer

c --- Lattice Surfaces ---
100  RPP  -1.89 1.89  -1.89 1.89  -100 100         $ Lattice boundary (3×1.26)

c --- Data Cards ---
MODE  N
M1   92235  0.03  92238  0.97  8016  2.0
M2   40000  1.0
M3   1001   2     8016   1
KCODE  10000  1.0  50  150
KSRC   0 0 0
```

**Key Points**:
1. **Universe 1**: Pin definition (fuel + clad + coolant)
2. **Surface 10**: Lattice element boundary (RPP for square pitch)
3. **Cell 100**: Lattice cell (`LAT=1` for rectangular)
   - `FILL=-1:1 -1:1 0:0`: Indices from -1 to 1 in x, y (3×3), z=0 (single plane)
   - `1 1 1 ...`: Fill all positions with universe 1
4. **Cell 1000**: Main geometry filled with lattice (universe 2)
5. **Surface 100**: Outer boundary containing entire lattice

**LAT=1 Indexing**:
```
FILL=-1:1  -1:1  0:0
     ^i    ^j    ^k (index ranges)

     1 1 1      $ j=1  (top row)
     1 1 1      $ j=0  (middle row)
     1 1 1      $ j=-1 (bottom row)
```

---

## Use Case 6: Hexagonal Lattice (VVER-Style)

**Scenario**: Hexagonal fuel assembly (7-pin cluster).

**Geometry**:
```
c =================================================================
c Hexagonal Lattice (7 pins)
c =================================================================

c --- Pin Universe (U=1) ---
1    1  -10.5  -1  U=1  IMP:N=1                    $ Fuel
2    2  -6.5   1 -2  U=1  IMP:N=1                  $ Clad
3    3  -1.0   2  U=1  IMP:N=1                     $ Coolant

c --- Hexprism Lattice Element ---
10   HEX  0 0 -100  0 0 200  0.63                  $ Hex element (R_in=0.63)

c --- Lattice Cell (U=2, LAT=2) ---
100  0  -10  LAT=2  U=2  FILL=-1:1  -1:1  0:0  &
                          1 1 0  &
                          1 1 1  &
                          0 1 1  IMP:N=1
c                         ^7 hexprisms (6 outer + 1 center)

c --- Main Geometry ---
1000  0  -100  FILL=2  IMP:N=1
9999  0  100   IMP:N=0

c --- Pin Surfaces ---
1    C/Z  0 0  0.5
2    C/Z  0 0  0.6

c --- Outer Boundary ---
100  RCC  0 0 -100  0 0 200  2.0                   $ Cylinder containing lattice
```

**Key Points**:
- `LAT=2`: Hexagonal lattice (hexprisms, points UP)
- HEX macrobody: Hexprism element
- Fill pattern: 7 pins (center + 6 surrounding)
  - `0` = void (no universe)
  - `1` = universe 1 (pin)

**LAT=2 Indexing** (Hexagonal coordinates):
```
       1 1 0       $ j=1
       1 1 1       $ j=0
       0 1 1       $ j=-1
```

---

## Transformations (TR Cards)

### Translation Only
```
*TR1  dx dy dz
```

**Example**:
```
*TR1  10 0 0                $ Translate +10 cm in x
1  1  SPH  0 0 0  5         $ Sphere at (10, 0, 0) due to TR1
```

### Rotation + Translation
```
*TRn  dx dy dz  a₁₁ a₁₂ a₁₃  a₂₁ a₂₂ a₂₃  a₃₁ a₃₂ a₃₃  m
      ^translation  ^rotation matrix (direction cosines) ^1=degrees
```

**Example (90° rotation about z, then translate)**:
```
*TR2  5 5 0  0 1 0  -1 0 0  0 0 1  1
c            ^new-x ^new-y ^new-z  ^input in degrees (convert internally)
1  2  C/Z  0 0  3                   $ Cylinder rotated and translated
```

**Usage in Cell** (TRCL parameter):
```
1  1  -1.0  -1  TRCL=2  IMP:N=1     $ Cell uses transformation TR2
```

**Usage in Surface** (transformation number):
```
1  2  SO  5.0                       $ Surface uses transformation TR2
c  ^TR number
```

---

## Universes and FILL

### Universe Definition (U parameter in cell)
```
1  1  -1.0  -1  U=5  IMP:N=1        $ Cell belongs to universe 5
```

### Simple Fill (Single Universe)
```
10  0  -10  FILL=5  IMP:N=1         $ Fill cell 10 with universe 5
```

### Indexed Fill (Array of Universes)
```
100  0  -10  LAT=1  U=2  FILL=0:2  0:2  0:0  &
                          1 2 3  &
                          4 5 6  &
                          7 8 9  IMP:N=1
```

**Interpretation**: 3×3 array
- Position (0,0,0): Universe 1
- Position (1,0,0): Universe 2
- Position (2,2,0): Universe 9

### Nested Universes
```
c Level 1: Pin (U=1)
1  1  -10.0  -1  U=1  IMP:N=1

c Level 2: Assembly (U=2, contains U=1)
10  0  -10  LAT=1  U=2  FILL=0:16 0:16 0:0  (17×17 array of U=1)

c Level 3: Core (U=0, contains U=2)
100  0  -100  FILL=2  IMP:N=1
```

---

## Reflecting Boundaries

### Specular Reflection (Perfect Mirror)
```
*1  PX  0.0             $ Reflecting boundary at x=0 (asterisk prefix)
```

**Usage**: Model quarter or half symmetry
```
c Quarter-core model with reflecting boundaries
1  1  -1.0  -1  2  3  IMP:N=1       $ Core (x>0, y>0)
2  0        1  IMP:N=0              $ Graveyard

1  PX  0.0                          $ Outer x boundary
*2  PX  0.0                         $ Reflecting x=0
*3  PY  0.0                         $ Reflecting y=0
```

### White Boundary (Isotropic Return)
```
+1  PX  0.0             $ White boundary (plus prefix)
```

**Difference**:
- **Specular** (`*`): Mirror reflection (angle in = angle out)
- **White** (`+`): Isotropic return (random direction)

---

## Common Errors and Troubleshooting

### Error 1: Lost Particle
**Symptom**:
```
lost particle
  x,y,z = 5.00000  3.00000  0.00000
  cell = 10
```

**Causes**:
1. **Gap in geometry** (undefined region)
2. **Overlapping cells** (ambiguous location)
3. **Surface sense error** (wrong +/-)

**Debugging**:
1. Plot geometry: `mcnp6 inp=input.i ip` → `plot` command
2. Check cell overlaps: Look for visual artifacts
3. Verify all surfaces referenced in cells are defined
4. Check Boolean expressions (parentheses, sense)

**Fix Example (Gap)**:
```
c BAD: Gap between R=10 and R=20
1  1  -1.0  -1  IMP:N=1             $ R<10
2  0         2  IMP:N=0             $ R>20 (GAP: 10<R<20 undefined!)

c GOOD: No gap
1  1  -1.0  -1  IMP:N=1             $ R<10
2  2  -2.0  1 -2  IMP:N=1           $ 10<R<20
3  0        2  IMP:N=0              $ R>20
```

### Error 2: Cell Overlap
**Symptom**: Particles behave erratically, unexpected tallies

**Cause**: Two cells claim the same space

**Fix**:
```
c BAD: Overlap (both cells include -1  2 region)
1  1  -1.0  -1  2  IMP:N=1          $ Includes -1  2
2  2  -2.0  -1  3  IMP:N=1          $ Also includes -1  2 (OVERLAP!)

c GOOD: Use union or subdivide
1  1  -1.0  -1  2  -3  IMP:N=1      $ Exclude region 3
2  2  -2.0  -1  3  IMP:N=1          $ Separate region
```

### Error 3: Surface Undefined
**Symptom**:
```
bad trouble in subroutine getcl
   surface 10 has not been defined.
```

**Cause**: Cell references surface 10, but no surface card exists

**Fix**: Define surface 10 in surface block
```
c Cell block
1  1  -1.0  -10  IMP:N=1

c Surface block
10  SO  5.0                         $ ADD THIS
```

### Error 4: Lattice Index Out of Bounds
**Symptom**: Lost particle in lattice

**Cause**: Particle escapes defined lattice indices

**Fix**: Ensure lattice boundary surface encloses all indices
```
c LAT=1, FILL=0:5 0:5 0:0 (6×6 array, pitch=1.5 cm)
c Boundary must be ≥ 6×1.5 = 9 cm

1  RPP  -4.5 4.5  -4.5 4.5  -100 100  $ Correct (9×9 cm)
c NOT: RPP -3 3 -3 3 ... (only 6×6 cm, TOO SMALL!)
```

### Error 5: Improper Boolean Expression
**Symptom**: Geometry not as expected, lost particles

**Cause**: Parentheses or operators incorrect

**Fix**:
```
c BAD (ambiguous precedence):
1  1  -1.0  -1 : -2  3  IMP:N=1     $ Parsed as: (-1) OR (-2 AND 3)

c GOOD (explicit grouping):
1  1  -1.0  (-1 : -2)  3  IMP:N=1   $ (Inside 1 OR inside 2) AND outside 3
```

---

## Integration with Other Skills

### 1. **mcnp-input-builder**
- Geometry fills Block 2 (cells) and Block 3 (surfaces)
- Proper cell numbering and organization
- Material numbers (m) reference M cards from mcnp-material-builder

### 2. **mcnp-material-builder**
- Cell card material number (m) references M card number
- Density (d) must match material type (positive for g/cm³, negative for atoms/b-cm)

### 3. **mcnp-source-builder**
- Source position (SDEF POS or CEL) must be in non-zero importance cell
- Volume sources (SDEF CEL=n) require cell n to exist
- Surface sources (SDEF SUR=n) require surface n to exist

### 4. **mcnp-tally-builder**
- F4 tallies reference cell numbers
- F1/F2 tallies reference surface numbers
- F5 point detectors must be in non-zero importance region

### 5. **mcnp-lattice-builder** (Category E)
- This skill (geometry-builder) covers lattice basics
- mcnp-lattice-builder provides advanced patterns (17×17 PWR, hex VVER)

### 6. **mcnp-validation-checker**
- Checks geometry completeness (no gaps, no overlaps)
- Validates surface references (all surfaces defined)
- Verifies importance in all cells

### Workflow:
```
1. mcnp-input-builder   → Basic structure
2. mcnp-geometry-builder → Define cells + surfaces (THIS SKILL)
3. mcnp-material-builder → M cards for materials
4. mcnp-source-builder   → Source in geometry
5. mcnp-tally-builder    → Tallies on cells/surfaces
6. mcnp-validation-checker → Check geometry consistency
```

---

## Validation Checklist

Before running:

- [ ] **All cells defined**:
  - [ ] Every spatial region has a cell card
  - [ ] No gaps (undefined regions)
  - [ ] No overlaps (ambiguous regions)

- [ ] **All surfaces defined**:
  - [ ] Every surface referenced in cell cards exists in surface block
  - [ ] Surface numbers unique

- [ ] **Boolean expressions correct**:
  - [ ] Surface sense correct (+/-)
  - [ ] Operators valid (space, `:`, `#`)
  - [ ] Parentheses balanced

- [ ] **Importance specified**:
  - [ ] All cells have IMP:N (or IMP:P, etc.)
  - [ ] Graveyard cell exists (IMP=0)

- [ ] **Lattice (if used)**:
  - [ ] Universe definitions complete (U parameter)
  - [ ] LAT=1 or LAT=2 specified
  - [ ] FILL indices match lattice boundary
  - [ ] Lattice element surface encloses unit

- [ ] **Transformations (if used)**:
  - [ ] *TRn cards defined for all referenced transformations
  - [ ] TRCL in cell card or transformation number in surface card

- [ ] **Geometry visualization**:
  - [ ] Run MCNP plotter: `mcnp6 inp=input.i ip` → `plot`
  - [ ] Check for visual gaps/overlaps
  - [ ] Verify lattice pattern correct

---

## Advanced Topics

### 1. Cell Complement for Complex Voids
```
c Define multiple solid regions, then one "everything else" cell
1   1  -1.0  -1  IMP:N=1             $ Solid 1 (sphere)
2   2  -2.0  -2  IMP:N=1             $ Solid 2 (box)
100 0        #1  #2  -100  IMP:N=1   $ Void (NOT in 1, NOT in 2, inside 100)
999 0        100  IMP:N=0            $ Graveyard
```

### 2. Nested Lattices (Pin → Assembly → Core)
```
c Level 1: Pin (U=1)
1  1  -10.0  -1  U=1  IMP:N=1

c Level 2: Pin array (U=2, LAT=1, 17×17)
10  0  -10  LAT=1  U=2  FILL=0:16 0:16 0:0  (289 entries of U=1)

c Level 3: Assembly array (U=3, LAT=1, 3×3)
100  0  -100  LAT=1  U=3  FILL=0:2 0:2 0:0  2 2 2  2 2 2  2 2 2

c Level 4: Core (main geometry, U=0)
1000  0  -1000  FILL=3  IMP:N=1
```

### 3. Rotated Geometry (Angled Components)
```
c Define rotation: 45° about z-axis
*TR1  0 0 0  0.707 0.707 0  -0.707 0.707 0  0 0 1  1
c            ^cos45 ^sin45  ^-sin45 ^cos45

c Surface using transformation
1  1  RPP  -5 5  -1 1  0 10         $ Rotated box

c Cell using transformation
1  1  -1.0  -1  TRCL=1  IMP:N=1
```

### 4. LIKE BUT (Copy and Modify Cells)
```
c Define base cell
1  1  -1.0  -1  U=1  IMP:N=1  TMP=2.53e-8

c Create similar cells with modifications
2  LIKE 1  BUT  U=2                 $ Same, different universe
3  LIKE 1  BUT  MAT=2  RHO=-0.05    $ Different material/density
4  LIKE 1  BUT  TMP=4.0e-8          $ Different temperature
```

### 5. Programmatic Geometry Generation

For automated geometry construction and parametric studies, a Python implementation is available: `mcnp_geometry_builder.py`

This tool can be used to:
- Generate complex geometries programmatically
- Create parametric geometry for optimization studies
- Automate repetitive geometry tasks
- Build geometry from CAD/external data sources

See the co-located Python script for API documentation and usage examples.

---

## Quick Reference: Common Patterns

### Concentric Spheres
```
1  SO  r₁
2  SO  r₂
3  SO  r₃

1  m  d  -1        $ R < r₁
2  m  d  1 -2      $ r₁ < R < r₂
3  m  d  2 -3      $ r₂ < R < r₃
4  0     3         $ R > r₃ (graveyard)
```

### Slab Layers
```
1  PX  x₁
2  PX  x₂
3  PX  x₃

1  m  d  -1        $ x < x₁
2  m  d  1 -2      $ x₁ < x < x₂
3  m  d  2 -3      $ x₂ < x < x₃
4  0     3         $ x > x₃
```

### Cylinder with End Caps
```
1  C/Z  0 0  R
2  PZ   h_top
3  PZ   h_bottom

1  m  d  -1  -2  3     $ Inside cylinder, between end caps
2  0         1:-2:3    $ Outside cylinder OR beyond end caps
```

### Box with Void
```
1  RPP  xmin xmax  ymin ymax  zmin zmax
2  SO  R

1  m  d  -1  2         $ Inside box, outside sphere
2  0        -2         $ Inside sphere (void)
3  0        1          $ Outside box
```

### 3×3 Lattice
```
c Pin universe (U=1)
1  m  d  -1  U=1

c Lattice element
10  RPP  -p/2  p/2  -p/2  p/2  -h  h

c Lattice cell (U=2)
100  0  -10  LAT=1  U=2  FILL=-1:1 -1:1 0:0  1 1 1  1 1 1  1 1 1

c Main geometry
1000  0  -100  FILL=2
```

---

## Best Practices

1. **Numbering Scheme**:
   - Group by function: 1-99 (core), 100-199 (reflector), 200-299 (shield)
   - Consistent with materials: Cell 10 uses M10, Cell 20 uses M20

2. **Comment Generously**:
   ```
   1  1  -1.0  -1  IMP:N=1  VOL=1000    $ Water sphere, R=10 cm
   ```

3. **Visualization Early**:
   - Plot geometry before full run: `mcnp6 ip` → `plot`
   - Check for gaps, overlaps, lost particles

4. **Modular Design**:
   - Use universes for repeated components
   - External READ files for large geometries

5. **Simplify with Macrobodies**:
   - RPP for boxes (simpler than 6 PX/PY/PZ)
   - RCC for finite cylinders (simpler than C/Z + PZ)

6. **Test Incrementally**:
   - Start simple (sphere, box)
   - Add complexity gradually (lattices, transformations)
   - Validate each step with geometry plots

---

## References
- **Documentation Summary**: `CATEGORIES_AB_DOCUMENTATION_SUMMARY.md` (Sections 3-6, 13)
- **Related Skills**: mcnp-input-builder, mcnp-material-builder, mcnp-lattice-builder (Category E)
- **User Manual**: Chapters 5.1-5.3, 5.5 (Geometry cards)

---

**End of MCNP Geometry Builder Skill**
