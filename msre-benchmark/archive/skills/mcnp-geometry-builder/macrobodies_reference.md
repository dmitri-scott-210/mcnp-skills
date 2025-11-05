# MCNP Macrobodies Reference

Macrobodies are high-level geometric primitives that MCNP internally decomposes into multiple surface cards. They simplify input file creation for common complex shapes.

## Overview

**Advantages:**
- Fewer input lines (one macrobody vs many surfaces)
- Less error-prone (no manual Boolean expressions)
- More intuitive parameter specification
- Automatically creates all necessary surfaces

**Disadvantages:**
- Less flexible than primitive surfaces
- Generated facets have usage restrictions
- Slightly longer MCNP processing time (decomposition)

---

## Macrobody Facets

When MCNP decomposes a macrobody, it creates numbered facets:

**Format:** `j.1`, `j.2`, `j.3`, etc.

Where `j` is the macrobody surface number.

**Example:**
```
1  RPP  -5 5  -5 5  0 10     $ Box (macrobody #1)

c MCNP creates facets:
c 1.1 = x_min face (x = -5)
c 1.2 = x_max face (x = +5)
c 1.3 = y_min face (y = -5)
c 1.4 = y_max face (y = +5)
c 1.5 = z_min face (z = 0)
c 1.6 = z_max face (z = +10)
```

### Facet Usage

**CAN use facets for:**
- Cell geometry definitions
- Tally surfaces (F1, F2)
- SDEF source surfaces

**CANNOT use facets for:**
- SSR (surface source read)
- SSW (surface source write)
- SF (source file)
- PTRAC (particle track)
- MCTAL (tally file output)

**Workaround:** If you need facets for restricted uses, define primitive surfaces instead of macrobody.

---

## BOX - Rectangular Parallelepiped (General Orientation)

**Format:** `BOX  vx vy vz  v₁x v₁y v₁z  v₂x v₂y v₂z  v₃x v₃y v₃z`

**Parameters:**
- `vx vy vz`: Corner point coordinates
- `v₁x v₁y v₁z`: Vector from corner along first edge
- `v₂x v₂y v₂z`: Vector from corner along second edge
- `v₃x v₃y v₃z`: Vector from corner along third edge

**Geometry:** Vectors define three edges emanating from corner point

**Examples:**
```
1  BOX  0 0 0  10 0 0  0 5 0  0 0 8    $ 10×5×8 cm box at origin (axis-aligned)
2  BOX  0 0 0  10 0 0  0 8 6  0 0 12   $ Skewed box (non-orthogonal edges)
```

**Facets Created:** 6 facets (six faces of parallelepiped)

**Common Uses:**
- Rotated boxes
- Skewed volumes
- General parallelepipeds

**Tip:** Use RPP for axis-aligned boxes (simpler specification)

---

## RPP - Right Parallelepiped (Axis-Aligned Box)

**Format:** `RPP  xmin xmax  ymin ymax  zmin zmax`

**Parameters:** Six values defining extent along each axis

**Examples:**
```
1  RPP  -5 5  -5 5  0 10     $ 10×10×10 cm box
2  RPP  0 100  0 50  0 200   $ 100×50×200 cm rectangular block
3  RPP  -10 -5  0 10  -20 20 $ Offset box (x from -10 to -5, etc.)
```

**Facets Created:** 6 facets
- .1 = x_min plane
- .2 = x_max plane
- .3 = y_min plane
- .4 = y_max plane
- .5 = z_min plane
- .6 = z_max plane

**Common Uses:**
- Rooms, buildings (shielding studies)
- Storage containers, casks
- Detector blocks
- Void regions for lattice boundaries
- Most common macrobody (simplest axis-aligned box)

---

## SPH - Sphere

**Format:** `SPH  x y z  R`

**Parameters:**
- x, y, z: Center coordinates
- R: Radius

**Example:**
```
1  SPH  0 0 0  10.0          $ Same as SO 10.0
2  SPH  10 5 0  8.0          $ Same as S 10 5 0  8.0
```

**Facets Created:** 1 facet (spherical surface)

**Common Uses:**
- Alternative to SO/S (more explicit)
- Preferred when consistent macrobody syntax desired
- Rare in practice (SO/S equally simple)

---

## RCC - Right Circular Cylinder

**Format:** `RCC  vx vy vz  hx hy hz  R`

**Parameters:**
- vx vy vz: Base center coordinates
- hx hy hz: Height vector (direction and magnitude)
- R: Radius

**Equation:** Cylinder from base (vx,vy,vz) along vector (hx,hy,hz)

**Examples:**
```
1  RCC  0 0 0  0 0 100  5.0  $ Cylinder h=100 cm, R=5 cm along z
2  RCC  0 0 0  100 0 0  3.0  $ Cylinder h=100 cm, R=3 cm along x
3  RCC  5 5 0  0 0 50  2.0   $ Off-center cylinder
```

**Facets Created:** 3 facets
- .1 = Cylindrical side surface
- .2 = Bottom end cap (circular)
- .3 = Top end cap (circular)

**Common Uses:**
- Fuel rods with explicit end caps
- Finite pipes, ducts
- Cylindrical detectors
- Most common for finite cylinders (simpler than C/Z + 2×PZ)

---

## RHP - Right Hexagonal Prism

**Format:** `RHP  vx vy vz  h1 h2 h3  r1 r2 r3  [s1 s2 s3  t1 t2 t3]`

**Parameters:**
- `vx vy vz`: Base center coordinates
- `h1 h2 h3`: Height vector (from bottom to top of prism)
- `r1 r2 r3`: **Apothem vector** - vector from axis to center of first facet
- `s1 s2 s3`: (Optional) Vector to center of second facet (required for irregular hexagons)
- `t1 t2 t3`: (Optional) Vector to center of third facet (required for irregular hexagons)

**Minimum 9 values** for regular hexagons, **15 values** for irregular hexagons.

**Regular Hexagon Example:**
```
1  RHP  4.5 0 -1.5  0 0 3  0 0.5 0
c       ^base       ^height ^apothem vector (0.5 cm perpendicular to y-axis)
c Creates regular hexagon with 0.5 cm apothem (flat-to-flat distance = 1.0 cm)
```

**Irregular Hexagon Example:**
```
2  RHP  6.0 2 -1.5  0 0 3  0.5 0 0  0.4 0.69282 0.0  -0.4 0.69282 0.0
c       ^base       ^height ^r1      ^s1            ^t1
c Three vectors define three alternating facet centers (other 3 are opposite)
```

**Key Concept:** The apothem is the perpendicular distance from the hexagon center to the midpoint of any side. For a regular hexagon with pitch `p`, the apothem = `p/2`.

**Facets Created:** 6 or 8 facets
- Facets 1-6: Six side planes (hexagon faces)
- Facets 7-8: Top and bottom end caps (created unless height vector ≥ 10⁶ cm)

---

## HEX - Right Hexagonal Prism (Synonym for RHP)

**Format:** `HEX  vx vy vz  h1 h2 h3  r1 r2 r3  [s1 s2 s3  t1 t2 t3]`

**Parameters:** Identical to RHP (HEX and RHP are synonyms in MCNP)
- `vx vy vz`: Base center coordinates
- `h1 h2 h3`: Height vector
- `r1 r2 r3`: **Apothem vector** - vector from axis to center of first facet
- `s1 s2 s3`: (Optional) Vector to center of second facet (required for irregular hexagons)
- `t1 t2 t3`: (Optional) Vector to center of third facet (required for irregular hexagons)

**Regular Hexagon Example:**
```
1  HEX  6.0 0 -1.5  0 0 3  0.5 0 0
c       ^base       ^height ^apothem vector (0.5 cm perpendicular to x-axis)
c Creates regular hexagon with flat-to-flat distance = 1.0 cm
```

**Irregular Hexagon Example:**
```
2  HEX  6.0 4 -1.5  0 0 3  0.5 0 0  0.4 0.69282 0.0  -0.5 0.85 0.0
c       ^base       ^height ^r1      ^s1            ^t1
```

**Facets Created:** 6 or 8 facets (same as RHP)
- Facets 1-6: Six side planes
- Facets 7-8: Top and bottom end caps

**Common Uses:**
- Hexagonal fuel assemblies (VVER, AGR, some research reactors)
- Hexagonal lattice elements (LAT=2)
- Graphite blocks (prismatic HTGR)

**Note:** HEX and RHP are **identical** - both keywords use the same format and produce the same geometry. Use whichever name is clearer for your application.

---

## TRC - Truncated Right-Angle Cone

**Format:** `TRC  vx vy vz  hx hy hz  R₁  R₂`

**Parameters:**
- vx vy vz: Base center coordinates
- hx hy hz: Height vector (axis direction and magnitude)
- R₁: Base radius
- R₂: Top radius

**Examples:**
```
1  TRC  0 0 0  0 0 100  10  5   $ Cone: R=10 at base, R=5 at top (tapered)
2  TRC  0 0 0  0 0 50  8  8     $ Cylinder (R₁ = R₂, same as RCC)
3  TRC  0 0 0  0 0 100  0  10   $ Cone with apex at base
```

**Facets Created:** 3 facets
- .1 = Conical side surface
- .2 = Bottom end cap (circular, radius R₁)
- .3 = Top end cap (circular, radius R₂)

**Common Uses:**
- Tapered structures (hoppers, nozzles)
- Conical transitions between pipes
- Collimators with varying aperture
- Beam shaping elements

---

## WED - Wedge

**Format:** `WED  vx vy vz  v₁x v₁y v₁z  v₂x v₂y v₂z  v₃x v₃y v₃z`

**Parameters:**
- vx vy vz: Corner point (base vertex)
- v₁x v₁y v₁z: Vector along first base edge
- v₂x v₂y v₂z: Vector along second base edge (perpendicular to v₁)
- v₃x v₃y v₃z: Height vector (perpendicular to base)

**Geometry:** Triangular prism with rectangular face opposite the apex edge

**Example:**
```
1  WED  0 0 0  10 0 0  0 5 0  0 0 8
c       ^corner ^v1    ^v2    ^height
```

**Facets Created:** 5 facets (2 triangular ends + 3 rectangular faces)

**Common Uses:**
- Angled blocks, ramps
- Building corners, roof sections
- Geometric transitions

---

## ARB - Arbitrary Polyhedron

**Format:** `ARB  x₁ y₁ z₁  x₂ y₂ z₂  x₃ y₃ z₃  x₄ y₄ z₄  x₅ y₅ z₅  x₆ y₆ z₆  x₇ y₇ z₇  x₈ y₈ z₈  f₁ f₂ f₃ f₄ f₅ f₆`

**Parameters:**
- x₁...x₈, y₁...y₈, z₁...z₈: Up to 8 vertices (use duplicates if fewer needed)
- f₁...f₆: Face connectivity (4-digit codes specifying which vertices form each face)

**Face Specification:** Each face is defined by 4 vertices (use duplicate vertex for triangle)
- f₁ = `v₁v₂v₃v₄` (e.g., 1234 means face uses vertices 1, 2, 3, 4)

**Example - Tetrahedron:**
```
1  ARB  0 0 0  10 0 0  5 8.66 0  5 2.89 8.16  &
        0 0 0  0 0 0  0 0 0  0 0 0  &
        1234  124  143  234
c       ^base  ^face1 ^face2 ^face3 (triangular faces use repeated vertex)
```

**Facets Created:** Up to 6 facets (planar faces)

**Common Uses:**
- Custom polyhedra
- Odd-angled geometries not covered by standard macrobodies
- Imported CAD geometries (approximated with facets)
- Last resort when other primitives don't fit

**Complexity:** Most difficult macrobody to specify correctly

---

## REC - Right Elliptical Cylinder

**Format:** `REC  vx vy vz  hx hy hz  v₁x v₁y v₁z  v₂x v₂y v₂z`

**Parameters:**
- vx vy vz: Base center
- hx hy hz: Height vector
- v₁x v₁y v₁z: Major axis vector (base ellipse)
- v₂x v₂y v₂z: Minor axis vector (base ellipse, perpendicular to v₁)

**Example:**
```
1  REC  0 0 0  0 0 100  10 0 0  0 5 0  $ Elliptical cylinder (a=10, b=5)
```

**Facets Created:** 3 facets (elliptical side + 2 elliptical ends)

**Common Uses:**
- Elliptical ducts
- Specialized geometries (rare)

---

## ELL - Ellipsoid

**Format:** `ELL  v1x v1y v1z  v2x v2y v2z  r`

**Two Forms (determined by sign of r):**

### Form 1: r > 0 (Focal Point Definition)
**Parameters:**
- `v1x v1y v1z`: Coordinates of first focus
- `v2x v2y v2z`: Coordinates of second focus
- `r`: Major radius length (positive value)

**Example:**
```
1  ELL  13.5 0.5 0  13.5 -0.5 0  0.75
c       ^focus1     ^focus2      ^major radius
c Distance between foci = 1.0 cm, major radius = 0.75 cm
```

### Form 2: r < 0 (Center-Axis Definition)
**Parameters:**
- `v1x v1y v1z`: Coordinates of ellipsoid center
- `v2x v2y v2z`: Major axis vector (from center through focus to vertex)
- `r`: Negative minor radius length (e.g., r = -0.5 means minor radius = 0.5 cm)

**Example:**
```
2  ELL  12.0 0 0  0 1 0  -0.5
c       ^center   ^major axis (along y)  ^minor radius (0.5 cm)
c Major axis length defined by vector magnitude
```

**Notes:**
- Major and minor radii are half the lengths of major and minor axes
- The ellipsoid is a surface of revolution about the major axis
- Major radius may be smaller than minor radius (oblate ellipsoid)

**Facets Created:** 1 facet (ellipsoidal surface)

**Common Uses:**
- Ellipsoidal volumes (rare in reactor physics)
- Optical surfaces
- Specialized detector geometries

---

## Macrobody Selection Guide

| Geometry | Macrobody | Alternative | Recommendation |
|----------|-----------|-------------|----------------|
| Axis-aligned box | RPP | 6 × PX/PY/PZ | Use RPP (simpler) |
| Rotated box | BOX | 6 × P | Use BOX if rotation needed |
| Finite cylinder (z-axis) | RCC | C/Z + 2×PZ | Use RCC (cleaner) |
| Tapered cylinder | TRC | K/Z + planes | Use TRC |
| Hex prism (z-axis) | HEX | 6 planes + 2×PZ | Use HEX for LAT=2 |
| Hex prism (any axis) | RHP | Multiple planes | Use RHP if needed |
| Sphere | SO or S | SPH | Use SO/S (simpler) |
| Wedge | WED | 5 planes | Use WED (cleaner) |
| Custom polyhedron | ARB | Multiple planes | Use planes if possible (simpler) |

---

## Best Practices

1. **Use macrobodies for clarity** - One RCC vs C/Z + 2×PZ is cleaner
2. **Avoid macrobodies for SSR/SSW** - Facets don't work, use primitives
3. **Check facet numbering** - Plot geometry to verify which facet is which
4. **Document orientation** - Add comments for BOX, RHP, ARB (non-obvious)
5. **Use RPP for simple boxes** - Most common and simplest
6. **Prefer primitives for flexibility** - Easier to modify individual surfaces
7. **Test incrementally** - Add one macrobody, plot, verify

---

## Decomposition Example

**Input:**
```
1  RPP  -5 5  -5 5  0 10
```

**MCNP Internal Decomposition:**
```
c MCNP creates 6 planes:
c 1.1:  PX  -5
c 1.2:  PX   5
c 1.3:  PY  -5
c 1.4:  PY   5
c 1.5:  PZ   0
c 1.6:  PZ  10

c Cell reference:
1  1  -1.0  -1  IMP:N=1    $ Inside RPP (automatically uses all 6 facets)
```

---

## Troubleshooting

### Error: "Macrobody degenerate"
**Cause:** Zero-length vector, zero radius, or invalid parameters
**Fix:** Check all parameters are non-zero and geometrically valid

### Error: "Cannot use macrobody facet with SSW"
**Cause:** Trying to write surface source on macrobody facet (e.g., 1.2)
**Fix:** Replace macrobody with primitive surfaces

### Issue: Unexpected geometry
**Cause:** Misunderstanding of vector directions or facet ordering
**Fix:** Plot geometry (`mcnp6 inp=file.i ip`), check facet sense

---

**References:**
- MCNP6 User Manual, Chapter 5.03: Surface Cards (Macrobodies section)
- MCNP6 User Manual, Chapter 5.03: Macrobody facet restrictions
