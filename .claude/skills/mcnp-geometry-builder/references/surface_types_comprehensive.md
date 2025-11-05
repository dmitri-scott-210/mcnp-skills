# MCNP Surface Types - Comprehensive Reference

This document provides detailed specifications for all MCNP surface types, including mathematical equations, parameter descriptions, and common use cases.

## Surface Card Format

```
j  [n]  mnemonic  entry₁  entry₂  ...
```

**Fields:**
- `j`: Surface number (1-99,999,999, unique)
- `n`: Transformation number (optional)
  - Positive: References *TRn transformation card
  - Negative: Creates periodic boundary with surface n
  - Omitted: No transformation
- `mnemonic`: Surface type identifier (SO, PX, C/Z, etc.)
- `entry`: Geometric parameters (depends on surface type)

**Special Prefixes:**
- `*j`: Specular reflecting boundary (mirror reflection)
- `+j`: White reflecting boundary (isotropic return)

---

## Planes

### P - General Plane

**Format:** `P  A  B  C  D`

**Equation:** Ax + By + Cz - D = 0

**Parameters:**
- A, B, C: Direction cosines (normal vector components)
- D: Distance parameter

**Examples:**
```
1  P  1 0 0  5          $ Plane at x = 5 (normal = +x direction)
2  P  0 1 0  -3         $ Plane at y = -3 (normal = +y direction)
3  P  1 1 0  0          $ x + y = 0 (45° diagonal plane)
4  P  0.707 0.707 0  10 $ Angled plane
```

**Alternative: Three-Point Definition**
```
1  P  x₁ y₁ z₁  x₂ y₂ z₂  x₃ y₃ z₃
```
Three points define the plane. Surface sense determined by right-hand rule or origin location.

### PX, PY, PZ - Axis-Aligned Planes

**Format:**
- `PX  D` → Plane at x = D (perpendicular to x-axis)
- `PY  D` → Plane at y = D (perpendicular to y-axis)
- `PZ  D` → Plane at z = D (perpendicular to z-axis)

**Equations:**
- PX: x - D = 0
- PY: y - D = 0
- PZ: z - D = 0

**Examples:**
```
1  PX  5.0              $ x = 5
2  PY  -3.0             $ y = -3
3  PZ  10.0             $ z = 10
```

**Common Uses:**
- Slab geometries (layered shields)
- Box boundaries (combine 6 planes for rectangular box)
- Splitting regions along coordinate axes
- Infinite planes for half-space problems

---

## Spheres

### SO - Sphere at Origin

**Format:** `SO  R`

**Equation:** x² + y² + z² - R² = 0

**Parameters:**
- R: Radius (cm)

**Example:**
```
1  SO  10.0             $ Sphere centered at origin, R = 10 cm
```

### S - General Sphere

**Format:** `S  x  y  z  R`

**Equation:** (x - x₀)² + (y - y₀)² + (z - z₀)² - R² = 0

**Parameters:**
- x, y, z: Center coordinates (cm)
- R: Radius (cm)

**Example:**
```
1  S  5 0 0  10.0       $ Center (5, 0, 0), R = 10 cm
```

### SX, SY, SZ - Spheres Centered on Axis

**Format:**
- `SX  x₀  R` → Center (x₀, 0, 0)
- `SY  y₀  R` → Center (0, y₀, 0)
- `SZ  z₀  R` → Center (0, 0, z₀)

**Equations:**
- SX: (x - x₀)² + y² + z² - R² = 0
- SY: x² + (y - y₀)² + z² - R² = 0
- SZ: x² + y² + (z - z₀)² - R² = 0

**Examples:**
```
1  SX  5  10.0          $ Center (5, 0, 0), R = 10
2  SY  3  8.0           $ Center (0, 3, 0), R = 8
3  SZ  -2  5.0          $ Center (0, 0, -2), R = 5
```

**Common Uses:**
- Point source geometries (nested concentric spheres)
- Spherical shells (multi-layer shielding)
- Importance splitting regions (variance reduction)
- Simple test problems

---

## Cylinders

### C/X, C/Y, C/Z - Cylinders Parallel to Axis

**Format:**
- `C/X  y₀  z₀  R` → Axis parallel to x (all x values)
- `C/Y  x₀  z₀  R` → Axis parallel to y (all y values)
- `C/Z  x₀  y₀  R` → Axis parallel to z (all z values)

**Equations:**
- C/X: (y - y₀)² + (z - z₀)² - R² = 0
- C/Y: (x - x₀)² + (z - z₀)² - R² = 0
- C/Z: (x - x₀)² + (y - y₀)² - R² = 0

**Examples:**
```
1  C/X  0 0  10.0       $ Cylinder along x-axis, R = 10
2  C/Y  0 0  5.0        $ Cylinder along y-axis, R = 5
3  C/Z  0 0  8.0        $ Cylinder along z-axis, R = 8 (most common)
4  C/Z  2.5 3.0  1.0    $ Off-axis cylinder, center (2.5, 3.0), R = 1
```

### CX, CY, CZ - Infinite Cylinders on Axis

**Format:**
- `CX  R` → Cylinder on x-axis (y² + z² = R²)
- `CY  R` → Cylinder on y-axis (x² + z² = R²)
- `CZ  R` → Cylinder on z-axis (x² + y² = R²)

**Equations:**
- CX: y² + z² - R² = 0
- CY: x² + z² - R² = 0
- CZ: x² + y² - R² = 0

**Examples:**
```
1  CX  10.0             $ On x-axis, R = 10
2  CY  5.0              $ On y-axis, R = 5
3  CZ  8.0              $ On z-axis, R = 8
```

**Common Uses:**
- Fuel pins/rods (C/Z or CZ, truncated with PZ planes)
- Pipes, ducts, coolant channels
- Cylindrical detectors
- Reactor cores (z-axis alignment most common)
- Beamlines, collimators

**Truncation Note:** Infinite cylinders (C/X, C/Y, C/Z, CX, CY, CZ) must be truncated with planes to create finite cylinders. For explicit finite cylinders, use RCC macrobody.

---

## Cones

### K/X, K/Y, K/Z - Cones Parallel to Axis

**Format:**
- `K/X  y₀  z₀  x₀  t²  [±1]`
- `K/Y  x₀  z₀  y₀  t²  [±1]`
- `K/Z  x₀  y₀  z₀  t²  [±1]`

**Equations (for K/Z):**
(x - x₀)² + (y - y₀)² - t²(z - z₀)² = 0

Where t² = (r/h)² = tan²(θ)

**Parameters:**
- x₀, y₀, z₀: Apex coordinates
- t²: Tangent squared of cone half-angle
- ±1: Sheet selector (optional, default both sheets)
  - +1: Single sheet (cone opening in positive direction)
  - -1: Single sheet (cone opening in negative direction)
  - Omit: Both sheets (double cone)

**Examples:**
```
1  K/Z  0 0 1  1        $ Cone apex (0,0,1), t²=1, opens along z
2  K/Z  0 0 0  0.25  1  $ Cone at origin, t²=0.25 (θ=26.6°), upper sheet only
```

### KX, KY, KZ - Cones on Axis

**Format:**
- `KX  x₀  t²  [±1]` → Apex on x-axis at (x₀, 0, 0)
- `KY  y₀  t²  [±1]` → Apex on y-axis at (0, y₀, 0)
- `KZ  z₀  t²  [±1]` → Apex on z-axis at (0, 0, z₀)

**Examples:**
```
1  KZ  5  1  1          $ Apex (0, 0, 5), t²=1, upper cone only
2  KX  0  0.25         $ Apex at origin, t²=0.25, both sheets
```

**Common Uses:**
- Nozzles, funnels
- Beam collimators
- Hopper geometries
- Truncate with planes for finite cones

---

## Tori (Fourth-Degree Surfaces)

### TX, TY, TZ - Elliptical Tori

**Format:**
- `TX  x₀  y₀  z₀  A  B  C`
- `TY  x₀  y₀  z₀  A  B  C`
- `TZ  x₀  y₀  z₀  A  B  C`

**Equations (for TZ - axis along z):**
[(√(x² + y²) - A)² / B² + z² / C²] - 1 = 0

**Parameters:**
- x₀, y₀, z₀: Center coordinates
- A: Major radius (distance from axis to tube center)
- B: Minor radius in x-y plane
- C: Minor radius in z direction

**Example:**
```
1  TZ  0 0 0  10  2  3   $ Elliptical torus, major R=10, minor ellipse 2×3
```

**Notes:**
- Tori are fourth-degree surfaces (more complex than quadrics)
- Used for specialized geometries (tokamak plasma chambers, pipes with bends)
- Can create "apple" shape (A < B+C) or "lemon" shape (A > B+C)
- Rarely needed in typical reactor analysis

**Common Uses:**
- Tokamak/stellarator plasma boundaries
- Curved pipes and elbows
- Toroidal magnetic confinement devices
- Specialized optical surfaces

---

## Quadric Surfaces

### GQ - General Quadric

**Format:** `GQ  A  B  C  D  E  F  G  H  J  K`

**Equation:**
Ax² + By² + Cz² + Dxy + Eyz + Fzx + Gx + Hy + Jz + K = 0

**Parameters:** 10 coefficients (A through K)

**Examples:**
```
1  GQ  1 1 -1  0 0 0  0 0 0  -100    $ Hyperboloid
2  GQ  1 1 0  0 0 0  0 0 -2  1       $ Paraboloid
```

### SQ - Special Quadric (A = B = C)

**Format:** `SQ  A  D  E  F  G  H  J  K`

**Equation:**
A(x² + y² + z²) + Dxy + Eyz + Fzx + Gx + Hy + Jz + K = 0

**Example:**
```
1  SQ  1  0 0 0  0 0 0  -100         $ Sphere: x² + y² + z² = 100
```

**Common Uses:**
- Exotic shapes not covered by standard surfaces
- Hyperboloids, paraboloids, ellipsoids
- Optical surfaces (lenses, mirrors)
- Custom geometries for specialized applications

---

## Point-Defined Surfaces (Axisymmetric)

### X, Y, Z - Surfaces Defined by Coordinate Points

**Format:**
- `X  coord₁  [coord₂]  [coord₃]`
- `Y  coord₁  [coord₂]  [coord₃]`
- `Z  coord₁  [coord₂]  [coord₃]`

**Surface Type Depends on Number of Coordinate Pairs:**

**1 pair → Plane perpendicular to axis:**
```
1  X  5.0               $ Plane at x = 5 (same as PX 5.0)
2  Y  -3.0              $ Plane at y = -3 (same as PY -3.0)
3  Z  10.0              $ Plane at z = 10 (same as PZ 10.0)
```

**2 pairs → Linear surface (cone or cylinder):**
```
1  Z  0 5  10 8         $ At z=0, r=5; at z=10, r=8 (truncated cone)
```
Defines a surface of revolution: linear interpolation between points

**3 pairs → Quadratic surface (paraboloid, etc.):**
```
1  Z  0 5  5 7  10 8    $ At z=0, r=5; z=5, r=7; z=10, r=8
```
Defines a surface of revolution: quadratic interpolation through 3 points

**Common Uses:**
- Axisymmetric geometries (vessels with varying radius)
- Gradual transitions between radii
- Simplified specification for complex axisymmetric shapes
- Alternative to explicit cones or paraboloids

**Notes:**
- Coordinates define (position along axis, radius at that position)
- Surface is generated by rotating profile around the specified axis
- More intuitive than mathematical equations for some geometries

---

## Surface Sense and Boolean Operations

### Surface Sense (Half-Spaces)

Every surface divides 3D space into two half-spaces:

- **Negative sense (`-n`)**: f(x,y,z) < 0 (typically "inside")
- **Positive sense (`+n` or `n`)**: f(x,y,z) > 0 (typically "outside")

**Examples:**
```
1  SO  10.0             $ Sphere surface

Cell 1:  -1             $ Inside sphere (r < 10)
Cell 2:   1             $ Outside sphere (r > 10)
```

### Boolean Operators in Cell Geometry

- **Intersection** (space or implicit AND): `-1 2 -3`
- **Union** (colon `:`): `-1 : -2`
- **Complement** (hash `#`): `#10` (not in cell 10)
- **Parentheses** for grouping: `(-1 2) : (-3 4)`

**Order of Operations:**
1. Complement (#) evaluated first
2. Intersection (space) evaluated second
3. Union (:) evaluated last

---

## Reflecting and Periodic Boundaries

### Specular Reflection (Mirror)

**Format:** `*j  type  params`

Particles reflect with angle of incidence = angle of reflection (mirror bounce)

**Example:**
```
*1  PX  0.0             $ Reflecting boundary at x = 0
```

**Use:** Quarter-symmetry models (reflect across x=0 and y=0)

### White Reflection (Isotropic)

**Format:** `+j  type  params`

Particles reflect with isotropic (random) direction distribution

**Example:**
```
+1  PZ  0.0             $ White boundary at z = 0
```

**Use:** Approximate reflection when exact angle doesn't matter

### Periodic Boundaries

**Format:** Surface with negative transformation number

```
1  n  PX  5.0           $ Surface with transformation n
2  -n PX  -5.0          $ Periodic boundary linked to surface 1
```

Particles crossing surface 2 re-enter at surface 1 (and vice versa), creating infinite repetition

**Use:** Infinite lattice approximations

---

## Summary Table: Surface Selection Guide

| Geometry Type | Surface Type | When to Use |
|---------------|--------------|-------------|
| Box (axis-aligned) | RPP macrobody or 6 PX/PY/PZ | Simple rectangular volumes |
| Sphere | SO, S, or SPH macrobody | Point sources, shells |
| Finite cylinder | RCC macrobody or C/Z + PZ | Fuel rods, most cylinders |
| Infinite cylinder | CZ, C/Z | When truncation by other surfaces is clear |
| Cone | K/Z or TRC macrobody | Tapered structures |
| Torus | TX/TY/TZ | Curved pipes, tokamaks |
| Angled plane | P (3-point form) | Non-axis-aligned cuts |
| Axisymmetric | X/Y/Z (2 or 3 pairs) | Vessels with varying radius |
| Complex custom | GQ or SQ | When standard surfaces don't fit |

---

## Best Practices

1. **Use simplest surface type** - PX instead of P when axis-aligned
2. **Use macrobodies for composite shapes** - RCC instead of C/Z + 2×PZ
3. **Check surface sense** - Plot geometry to verify inside/outside
4. **Avoid redundant surfaces** - Reuse surfaces when possible
5. **Use transformations** - Rotate standard surface instead of GQ
6. **Document complex surfaces** - Inline comments for GQ, tori
7. **Test incrementally** - Add surfaces gradually, validate at each step

---

**References:**
- MCNP6 User Manual, Chapter 5.03: Surface Cards
- MCNP6 User Manual, Chapter 5.05: Geometry Data Cards (Transformations)
