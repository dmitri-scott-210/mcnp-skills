# Complex Geometry Patterns - Advanced Reference

This reference provides advanced Boolean geometry patterns for complex MCNP models. Each pattern includes complete cell and surface definitions with explanations.

## Pattern 1: Annular Regions (Shells)

**Use case:** Layered shields, spherical shells, cylindrical shells

### Spherical Shells

**Geometry:** Concentric spherical layers
```
c Five-region spherical shell (core → shield → detector → void → graveyard)
1  1  -19.0  -1        IMP:N=1  VOL=33.51    $ Core (innermost)
2  2  -10.5   1 -2     IMP:N=2  VOL=268.08   $ First shield layer
3  3  -8.0    2 -3     IMP:N=4  VOL=636.67   $ Second shield layer
4  4  -2.0    3 -4     IMP:N=8  VOL=1205.89  $ Detector region
5  0         -5 4      IMP:N=8  VOL=1000.0   $ Void around detector
6  0          5        IMP:N=0                $ Graveyard

1  SO  2.0                                    $ Core radius
2  SO  4.0                                    $ Shield 1 outer
3  SO  6.0                                    $ Shield 2 outer
4  SO  8.0                                    $ Detector outer
5  SO  20.0                                   $ Problem boundary
```

**Key features:**
- Each shell: inside outer sphere AND outside inner sphere
- Importance increases with depth (variance reduction)
- Volumes calculated analytically: V = (4/3)π(R₂³ - R₁³)

### Cylindrical Shells

**Geometry:** Concentric cylindrical layers (finite height)
```
c Four-region cylindrical shell
1  1  -10.0  -1 -5 6       IMP:N=1  $ Inner cylinder
2  2  -8.0    1 -2 -5 6    IMP:N=1  $ First shell
3  3  -6.0    2 -3 -5 6    IMP:N=1  $ Second shell
4  4  -2.0    3 -4 -5 6    IMP:N=1  $ Outer shell
5  0          4:5:-6       IMP:N=0  $ Graveyard

1  CZ  2.0                          $ Inner radius
2  CZ  4.0                          $ Shell 1 outer
3  CZ  6.0                          $ Shell 2 outer
4  CZ  8.0                          $ Shell 3 outer
5  PZ  0.0                          $ Bottom
6  PZ  100.0                        $ Top
```

**Key features:**
- Truncation with end planes (-5 6)
- Graveyard uses union: outside radial boundary OR below bottom OR above top

**Pitfalls:**
- Forgetting end plane truncation (infinite cylinder)
- Incorrect volume calculation (must account for shell vs solid cylinder)

---

## Pattern 2: Sectored Geometries (Pie Slices)

**Use case:** Angular sectors, wedges, segmented detectors

### Quarter Circle (90° sector)

**Geometry:** One quadrant of cylinder
```
c Quarter-circle sector in +x, +y quadrant
1  1  -10.0  -1 -2 -3 -4 5  IMP:N=1  $ Sector (0° to 90°)
2  0          1:2:3:4:-5    IMP:N=0  $ Graveyard

1  CZ  10.0                          $ Outer radius
2  PY  0.0                           $ y = 0 plane (xz plane)
3  PX  0.0                           $ x = 0 plane (yz plane)
4  PZ  0.0                           $ Bottom
5  PZ  100.0                         $ Top
```

**Cell 1 logic:**
- `-1`: Inside cylinder
- `-2`: Above xz plane (y > 0)
- `-3`: Above yz plane (x > 0)
- `-4 5`: Between bottom and top planes

### Arbitrary Angular Sector

**Geometry:** 30° wedge using rotated planes
```
c 30° sector from 0° to 30° in xy plane
1  1  -10.0  -1 -2 3 -4 5  IMP:N=1  $ Wedge
2  0          1:2:-3:4:-5   IMP:N=0

1  CZ  10.0                          $ Radius
2  PX  0.0                           $ 0° boundary
3  P  0.866 -0.5 0  0                $ 30° boundary (cos30, -sin30, 0)
4  PZ  0.0                           $ Bottom
5  PZ  100.0                         $ Top
```

**Key features:**
- Plane normal: (cos θ, -sin θ, 0) for angle θ from +x axis
- For 30°: (0.866, -0.5, 0)
- Cell is bounded by two radial planes

---

## Pattern 3: Multi-Region Assemblies

**Use case:** Fuel pins, control rods, detector assemblies

### Fuel Pin (Four Regions)

**Geometry:** Fuel, gap, cladding, coolant
```
c Typical LWR fuel pin (PWR)
1  1  -10.41  -1 -10 11      IMP:N=1  $ UO₂ fuel
2  0           1 -2 -10 11   IMP:N=1  $ Helium gap (void)
3  2  -6.56    2 -3 -10 11   IMP:N=1  $ Zircaloy clad
4  3  -0.74    3 -4 -10 11   IMP:N=1  $ Water coolant
5  0           4:10:-11      IMP:N=0  $ Graveyard

1  CZ  0.4095                         $ Fuel radius
2  CZ  0.4180                         $ Gap outer radius
3  CZ  0.4750                         $ Clad outer radius
4  CZ  0.6300                         $ Pin cell boundary (square pitch/√2)
10  PZ  0.0                           $ Bottom (inactive region)
11  PZ  365.76                        $ Top (active fuel length)
```

**Common use cases:**
- Vary enrichment: Change M1 density
- Different pin types: LIKE n BUT with different materials
- Fill into lattice: Assign U=1, use in LAT cell

### Control Rod Assembly

**Geometry:** Absorber, gap, steel guide tube, water
```
c Control rod (cruciform or circular)
1  1  -10.2   -1 -10 11      IMP:N=1  $ B₄C absorber
2  0           1 -2 -10 11   IMP:N=1  $ Gap
3  2  -8.0     2 -3 -10 11   IMP:N=1  $ Stainless steel guide tube
4  3  -1.0     3 -4 -10 11   IMP:N=1  $ Water surrounding
5  0           4:10:-11      IMP:N=0

1  CZ  0.4500                         $ Absorber radius
2  CZ  0.4650                         $ Gap outer
3  CZ  0.5400                         $ Guide tube outer
4  CZ  0.6300                         $ Cell boundary
10  PZ  0.0
11  PZ  400.0                         $ Full core height
```

**Variants:**
- Cruciform: Use box surfaces instead of cylinders
- Segmented: Multiple axial regions with different materials
- Movable: Use different universe positions in FILL array

---

## Pattern 4: Void Regions and Cutouts

**Use case:** Holes in structures, beam ports, access tunnels

### Box with Cylindrical Hole (Through)

**Geometry:** Rectangular block with hole
```
c Concrete block with beam port
1  1  -2.3  -1 2 -3 4 -5 6 #10  IMP:N=1  VOL=7600  $ Block minus hole
2  0        -10              IMP:N=1            $ Hole (air/vacuum)
3  0         1:-2:3:-4:5:-6  IMP:N=0            $ Graveyard

c Block boundaries
1  PX  -10.0
2  PX   10.0
3  PY  -10.0
4  PY   10.0
5  PZ  -20.0
6  PZ   20.0

c Hole (cylinder through entire block)
c Defined in separate cell 10, referenced by complement in cell 1
10  0  -7 -5 6  IMP:N=1  $ Cylinder

7  CZ  3.0                   $ Hole radius
```

**Key features:**
- `#10` in cell 1: Excludes cell 10 from block
- Cell 10 must be defined
- Hole can have different importance (particle streaming)

### Multiple Cutouts (Union of Holes)

**Geometry:** Three holes in block
```
c Block with three access ports
1  1  -2.3  -1 2 -3 4 -5 6 #10 #20 #30  IMP:N=1  $ Block minus three holes
2  0        -10                       IMP:N=1  $ Hole 1
3  0        -20                       IMP:N=1  $ Hole 2
4  0        -30                       IMP:N=1  $ Hole 3
5  0         1:-2:3:-4:5:-6           IMP:N=0

1  PX  -20.0
2  PX   20.0
3  PY  -20.0
4  PY   20.0
5  PZ  -30.0
6  PZ   30.0

10  0  -11 -5 6  IMP:N=1  $ Hole 1 (cylinder)
20  0  -12 -5 6  IMP:N=1  $ Hole 2
30  0  -13 -5 6  IMP:N=1  $ Hole 3

11  C/X  0 0   3.0         $ Hole 1 (along x-axis)
12  C/Y  5 0   2.0         $ Hole 2 (along y-axis)
13  C/Z  -5 -5  1.5        $ Hole 3 (along z-axis)
```

---

## Pattern 5: Nested Structures (Without Universes)

**Use case:** When universe hierarchy isn't needed, simple nesting

### Sphere in Cylinder in Box

**Geometry:** Three nested levels, different materials
```
c Sphere inside cylinder inside box
1  1  -19.0  -1            IMP:N=1  $ Innermost sphere (dense material)
2  2  -10.0   1 -2 -3 4    IMP:N=1  $ Cylinder around sphere (minus sphere)
3  3  -2.3   (-5 6 -7 8 -9 10) #1 #2  IMP:N=1  $ Box minus cyl minus sphere
4  0          5:-6:7:-8:9:-10   IMP:N=0  $ Graveyard

1  SO  5.0                           $ Sphere radius
2  CZ  8.0                           $ Cylinder radius
3  PZ  -15.0                         $ Cylinder bottom
4  PZ   15.0                         $ Cylinder top
5  PX  -20.0                         $ Box boundaries
6  PX   20.0
7  PY  -20.0
8  PY   20.0
9  PZ  -20.0
10  PZ   20.0
```

**Key features:**
- Cell 2: Cylinder region excluding sphere (1 -2 = outside 1, inside 2)
- Cell 3: Box excluding both inner cells (#1 #2)
- Three materials, three geometric levels

**When to use vs universes:**
- Simple nesting (2-3 levels): Direct nesting OK
- Repeated structures: Use universes
- Complex hierarchy (>3 levels): Use universes

---

## Pattern 6: Symmetric Geometries

**Use case:** Reduce model size using symmetry

### Quarter-Symmetry Model (Reflecting Boundaries)

**Geometry:** Model one quadrant, reflect for full geometry
```
c Quarter-symmetric reactor model (use 1/4 of geometry)
c Reflecting boundaries at x=0 and y=0
1  1  -10.5  -1 -2 -3 -4 5  IMP:N=1  $ Active region (one quadrant)
2  0          1:2:3:4:-5    IMP:N=0  $ Graveyard

*1  PX  0.0                           $ Reflecting boundary (x=0)
*2  PY  0.0                           $ Reflecting boundary (y=0)
3  PX  100.0                          $ Physical boundary (+x)
4  PY  100.0                          $ Physical boundary (+y)
5  PZ  100.0                          $ Top

c * prefix on surfaces 1 and 2 creates specular reflecting boundaries
```

**Key features:**
- `*` prefix: Specular reflection (mirror)
- Particles crossing x=0 or y=0 reflect back
- Model 1/4 of geometry, get full-geometry results
- Source must respect symmetry (place in modeled quadrant)

### Eighth-Symmetry Model

**Geometry:** Three reflecting planes (xyz octant)
```
c Eighth-symmetric model (one octant)
1  1  -10.5  -1 -2 -3 -4 -5 6  IMP:N=1  $ +x, +y, +z octant
2  0          1:2:3:4:5:-6     IMP:N=0

*1  PX  0.0                             $ Reflect at yz plane
*2  PY  0.0                             $ Reflect at xz plane
*3  PZ  0.0                             $ Reflect at xy plane
4  PX  100.0                            $ Physical boundary
5  PY  100.0
6  PZ  100.0
```

**Advantages:**
- 8x speedup (1/8 geometry tracked)
- Memory savings
- Same statistical quality with fewer particles

**Restrictions:**
- Geometry must be truly symmetric
- Source must be in modeled octant
- Results must be interpreted per full geometry

---

## Pattern 7: Irregular Boundaries

**Use case:** Custom shapes, approximating curves

### Staircase Approximation (Curved with Planes)

**Geometry:** Approximate cylinder with planes
```
c Eight-sided polygon approximating cylinder
1  1  -10.5  -1 -2 -3 -4 -5 -6 -7 -8 -10 11  IMP:N=1  $ Octagonal "cylinder"
2  0          1:2:3:4:5:6:7:8:10:-11        IMP:N=0

c Eight planes forming octagon (inscribed in circle R=10)
1  P   0.924  0.383 0  10.0    $ Plane 1 (22.5°)
2  P   0.383  0.924 0  10.0    $ Plane 2 (67.5°)
3  P  -0.383  0.924 0  10.0    $ Plane 3 (112.5°)
4  P  -0.924  0.383 0  10.0    $ Plane 4 (157.5°)
5  P  -0.924 -0.383 0  10.0    $ Plane 5 (202.5°)
6  P  -0.383 -0.924 0  10.0    $ Plane 6 (247.5°)
7  P   0.383 -0.924 0  10.0    $ Plane 7 (292.5°)
8  P   0.924 -0.383 0  10.0    $ Plane 8 (337.5°)
10  PZ  0.0                     $ Bottom
11  PZ  100.0                   $ Top
```

**When to use:**
- Complex curve not available as MCNP surface
- CAD import (faceted geometry)
- Higher-order surfaces not supported

**Trade-offs:**
- More surfaces = more processing time
- Better approximation = more planes needed
- For cylinder: Just use CZ! (example shows technique)

### Point-Defined Surface (Custom Profile)

**Geometry:** Axisymmetric vessel with varying radius
```
c Pressure vessel with bulge (axisymmetric about z-axis)
1  1  -7.8  -1 -2 3  IMP:N=1  $ Vessel wall
2  0        1 -2 3   IMP:N=1  $ Interior void
3  0        2:-3     IMP:N=0  $ Graveyard

1  Z   0 50  50 60  100 55  150 50  $ Point-defined surface (4 points)
c     z  r   z  r   z   r   z   r
c     At z=0, r=50; z=50, r=60 (bulge); z=100, r=55; z=150, r=50
2  PZ  0.0                              $ Bottom
3  PZ  150.0                            $ Top
```

**Key features:**
- Z card: Creates surface of revolution (rotate about z-axis)
- 2 points: Linear interpolation (cone/cylinder)
- 3 points: Quadratic interpolation (smooth curve)
- 4+ points: Piecewise interpolation

---

## Complete Example 1: Reactor Core Slice

**Geometry:** 3×3 pin array with water gaps and reflector

```
c Simple 3x3 PWR assembly section (single axial level)

c Pin cells (9 pins with varying enrichment)
1  1  -10.41  -101 -10 11  U=1  IMP:N=1  $ 4.5% enrichment fuel
2  0           101 -102 -10 11  U=1  IMP:N=1  $ Gap
3  2  -6.56    102 -103 -10 11  U=1  IMP:N=1  $ Clad
4  3  -0.74    103 -104 -10 11  U=1  IMP:N=1  $ Water

c Lower enrichment pin (use LIKE BUT)
5  LIKE 1 BUT  U=2  RHO=-10.15  $ 3.5% enrichment
6  LIKE 2 BUT  U=2
7  LIKE 3 BUT  U=2
8  LIKE 4 BUT  U=2

c Lattice cell (3×3 array)
20  0  -200 -10 11  LAT=1  U=3  FILL=-1:1 -1:1 0:0
                                     1 1 2
                                     1 1 1
                                     2 1 1  IMP:N=1

c Assembly with water gap and reflector
30  3  -0.74  -300 200 -10 11  IMP:N=1  $ Water between assemblies
40  4  -2.3   -400 300 -10 11  IMP:N=1  $ Reflector
50  0          400:10:-11      IMP:N=0  $ Graveyard

c Pin surfaces
101  CZ  0.4095      $ Fuel radius
102  CZ  0.4180      $ Gap
103  CZ  0.4750      $ Clad
104  CZ  0.6300      $ Pin cell boundary (1.26 cm pitch)

c Lattice boundary (3 pins × 1.26 cm = 3.78 cm)
200  RPP  -1.89 1.89  -1.89 1.89  0 10  $ Lattice extent

c Assembly boundaries
300  RPP  -2.5 2.5  -2.5 2.5  0 10      $ Water gap
400  RPP  -10 10  -10 10  0 10          $ Reflector outer

c Axial limits
10  PZ  0.0
11  PZ  10.0

c Materials
M1   92235  0.045  92238  0.955         $ 4.5% enriched fuel (simplified)
M2   40000  1.0                         $ Zircaloy (simplified)
M3   1001  2  8016  1                   $ Water
M4   26000  1                           $ Iron (reflector)
```

---

## Complete Example 2: Shielding Wall with Penetration

**Geometry:** Multi-layer shield with duct

```
c Three-layer shield wall with rectangular duct penetration

c Duct void (straight-through penetration)
1  0  -1 2 -3 4 -10 11  IMP:N=1  $ Duct interior (air)

c Shield layers (minus duct)
2  1  -7.8   -5 -10 11 #1  IMP:N=1  $ Steel layer (minus duct)
3  2  -2.3    5 -6 -10 11 #1  IMP:N=2  $ Concrete layer 1
4  3  -11.3   6 -7 -10 11 #1  IMP:N=4  $ Lead layer
5  2  -2.3    7 -8 -10 11 #1  IMP:N=8  $ Concrete layer 2
6  4  -1.6    8 -9 -10 11 #1  IMP:N=16  $ Polyethylene layer

c Source room and detector room
7  0  -5 -10 11  IMP:N=1  $ Source room (before shield)
8  0   9 -10 11  IMP:N=16  $ Detector room (after shield)

c Boundaries
9  0  10:-11  IMP:N=0  $ Graveyard

c Duct surfaces (rectangular, 20cm × 30cm)
1  PY  -10.0           $ Duct bottom
2  PY   10.0           $ Duct top
3  PX  -15.0           $ Duct left
4  PX   15.0           $ Duct right

c Shield layer interfaces (perpendicular to z-axis)
5  PZ  100.0           $ Source room boundary
6  PZ  110.0           $ Steel/concrete interface (10 cm steel)
7  PZ  140.0           $ Concrete/lead interface (30 cm concrete)
8  PZ  145.0           $ Lead/concrete interface (5 cm lead)
9  PZ  175.0           $ Final concrete/polyethylene (30 cm concrete)

c Overall boundaries
10  PZ  0.0            $ Behind source room
11  PZ  200.0          $ Beyond detector room

c Materials (simplified)
M1   26000  1          $ Steel
M2   20000  1          $ Concrete (simplified)
M3   82000  1          $ Lead
M4   1001  2  6000  1  $ Polyethylene (CH₂)
```

---

## When to Use vs Universes/Lattices

**Use direct Boolean patterns when:**
- Unique geometry (not repeated)
- 2-3 nesting levels
- Simple combinations
- No symmetry to exploit

**Use universes/lattices when:**
- Repeated structures (>3 instances)
- Deep nesting (>3 levels)
- Regular arrays
- Complex assemblies filled into larger structure

**Decision tree:**
1. Is structure repeated? → Universes
2. Regular array? → LAT + FILL
3. >3 nesting levels? → Universes
4. Otherwise → Direct Boolean

---

## Common Pitfalls

1. **Over-complicating**: Simple geometry doesn't need complement operators
2. **Missing boundaries**: Gaps between regions cause lost particles
3. **Overlaps**: Two cells claiming same space (BAD TROUBLE 1000)
4. **Wrong surface sense**: Inverted geometry (inside becomes outside)
5. **Forgotten truncation**: Infinite surfaces need bounding planes
6. **Complement loops**: Cell A uses #B, cell B uses #A (ERROR)
7. **Volume calculation**: Forgetting to account for cutouts/holes

---

**References:**
- MCNP6 User Manual, Chapter 5.02: Cell Cards - Boolean Operations
- See also: boolean_operations_guide.md for operator precedence
- See also: cell_definition_comprehensive.md for cell format
- See also: lattice_geometry_reference.md for universe/LAT alternatives
