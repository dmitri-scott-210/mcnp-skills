# Lattice Fundamentals - U/LAT/FILL Card System

**Reference for:** mcnp-lattice-builder skill
**Source:** MCNP6.3.1 Manual Chapters 5.02 and 5.05
**Purpose:** Comprehensive reference for universe/lattice/fill methodology

---

## Universe Concept (U Card)

### What is a Universe?

A **universe** is a self-contained geometry block that can be referenced by number and instantiated multiple times in different locations. Think of it as a geometry "template" or "stamp" that can be repeated without duplicating cell definitions.

**Key properties:**
- Universe 0 = main problem geometry (default for all cells without U parameter)
- Universes 1-99999999 = available for repeated structures
- Universe coordinate system origin at (0,0,0) by default
- Can contain any number of cells
- Can be nested within other universes (multi-level hierarchy)

### U Card Syntax

```
CELL  MAT  DENS  GEOM  U=n  PARAMS
```

**Where:**
- `U=n` assigns cell to universe n
- If U not specified, cell belongs to universe 0 (main geometry)
- All cells with same U number belong to same universe

**Example:**
```
c Universe 1: Fuel pin geometry
1  1  -10.5  -10         U=1  IMP:N=1   $ Fuel region
2  2  -6.5    10 -11     U=1  IMP:N=1   $ Clad region
3  3  -1.0    11         U=1  IMP:N=1   $ Coolant region

c Surfaces for universe 1
10  CZ  0.4   $ Fuel radius
11  CZ  0.5   $ Clad outer radius
```

### Universe Containment Rules

**CRITICAL:** All cells in a universe (except optional background cell) must be fully contained. No infinite cells allowed except the outermost background cell.

**Wrong:**
```
3  3  -1.0  11  U=1  IMP:N=1   $ Extends to infinity - WILL CAUSE LOST PARTICLES
```

**Correct:**
```
3  3  -1.0  11 -12  U=1  IMP:N=1   $ Bounded by surface 12
4  3  -1.0  12      U=1  IMP:N=1   $ Background cell (contains everything else)

12  RPP  -0.63  0.63  -0.63  0.63  -100  100   $ Lattice element boundary
```

### Universe Nesting

Universes can contain other universes, creating hierarchical geometry:

**Level 0:** Main geometry (Universe 0)
**Level 1:** Assembly lattice (Universe 10) containing...
**Level 2:** Pin lattice (Universe 100) containing...
**Level 3:** Pin geometry (Universe 1)

**Maximum nesting depth:** 20 levels (MCNP6 limit)

### Negative Universe Optimization

**Advanced feature:** Negative universe number creates "negative geometry" where universe is defined by its ABSENCE rather than presence.

```
CELL  0  -SURF  U=-5  $ Cell OUTSIDE universe 5
```

**Use case:** Memory optimization for large systems
**WARNING:** Use with extreme caution - incorrect usage causes silent errors
**Requirement:** Cell must be fully enclosed, never truncated by boundaries

---

## Lattice Concept (LAT Card)

### What is a Lattice?

A **lattice** is an ordered, infinite array of identical elements filling a cell in a regular pattern. Each element can be filled with a different universe.

**Types:**
- `LAT=1`: Rectangular (Cartesian) lattice - elements are rectangular parallelepipeds
- `LAT=2`: Hexagonal lattice - elements are hexagonal prisms
- `LAT=5`: 3D hexagonal lattice (SCALE-like, rarely used)

### LAT=1 Rectangular Lattice

**Lattice element:** Rectangular parallelepiped (RPP) that tiles space

**Syntax:**
```
CELL  0  -SURF  LAT=1  U=n  FILL=...  PARAMS
```

**Surface requirements:**
- Surface must define ONE lattice element (RPP)
- Element size determines spacing for entire lattice
- Surface defines element centered at origin

**Example:**
```
c Lattice cell - infinite array of 1.26×1.26 cm elements
100  0  -10  LAT=1  U=10  FILL=1  IMP:N=1

c Surface 10 defines lattice element size
10  RPP  -0.63  0.63  -0.63  0.63  -100  100   $ 1.26 cm pitch (±0.63)
```

**Indexing:** Elements indexed as (i, j, k) in Cartesian coordinates
- i = index in x-direction
- j = index in y-direction
- k = index in z-direction
- Origin element = (0, 0, 0)

**Surface ordering:**
For RPP: `RPP xmin xmax ymin ymax zmin zmax`
- First pair (xmin, xmax) → i-direction (+x)
- Second pair (ymin, ymax) → j-direction (+y)
- Third pair (zmin, zmax) → k-direction (+z)

For general surfaces on LAT cell card: **ORDER MATTERS**
- Surface order defines index directions
- First surface pair → i-direction
- Second surface pair → j-direction
- Third surface pair → k-direction

### LAT=2 Hexagonal Lattice

**Lattice element:** Hexagonal prism (RHP) that tiles space

**Syntax:**
```
CELL  0  -SURF  LAT=2  U=n  FILL=...  PARAMS
```

**Surface requirements:**
- Surface must be hexagonal prism (RHP macrobody)
- Hexagon orientation: Flat sides LEFT/RIGHT, points UP/DOWN
- Element size determines spacing

**RHP syntax:**
```
SURF  RHP  x y z  Hx Hy Hz  R
```

**Where:**
- (x, y, z) = base center
- (Hx, Hy, Hz) = axis vector (height direction)
- R = apothem (perpendicular distance from center to flat side)

**Apothem calculation:**
```
For hexagonal pitch P:
Apothem R = P / √3 ≈ P / 1.732
```

**Example:**
```
c Hexagonal lattice with 1.26 cm pitch
100  0  -10  LAT=2  U=10  FILL=1  IMP:N=1

10  RHP  0 0 -100  0 0 200  0.73   $ R = 1.26/1.732 = 0.728 cm
```

**Indexing:** (i, j, k) but with hexagonal offset
- i = column (horizontal)
- j = row (vertical with offset)
- **ODD columns (i=1,3,5...) are offset +0.5 in j direction**
- k = axial (same as LAT=1)

**Hexagonal layout:**
```
     j=1:    1   2   1        Column 0 at j=0, 1, 2
         /\      /\      /\    Column 1 at j=0.5, 1.5, 2.5 (offset!)
        /  \    /  \    /  \   Column 2 at j=0, 1, 2
     j=0:  2   1   2
        \  /    \  /    \  /
         \/      \/      \/
     j=-1:   1   2   1

    i=-1   i=0   i=1
```

---

## Fill Concept (FILL Card)

### Simple Fill (Uniform Universe)

**Syntax:**
```
CELL  0  -SURF  FILL=u  PARAMS
```

**Behavior:** Entire cell filled with universe u

**Use case:** Place single universe instance (non-lattice)

**Example:**
```
c Fill assembly (universe 10) into main geometry
1000  0  -100  FILL=10  IMP:N=1

100  RPP  -10  10  -10  10  -100  100   $ Assembly region
```

### Array Fill (Multiple Universes)

**Syntax:**
```
CELL  0  -SURF  LAT=1  U=n  FILL=imin:imax jmin:jmax kmin:kmax
                             u1 u2 u3 ...
                             PARAMS
```

**Array specification:**
- Indices define range of lattice positions
- Universe numbers listed in Fortran ordering: **i varies fastest, then j, then k**
- Number of values must equal (imax-imin+1) × (jmax-jmin+1) × (kmax-kmin+1)

**Example: 3×3 array**
```
100  0  -10  LAT=1  U=10  FILL=0:2  0:2  0:0  IMP:N=1
                            1 1 1    $ j=0, i=0,1,2
                            1 2 3    $ j=1, i=0,1,2
                            1 1 1    $ j=2, i=0,1,2
```

**Fortran Ordering CRITICAL:**
```
Array read left-to-right, line-by-line:
Position [0]: i=0, j=0, k=0 → universe 1
Position [1]: i=1, j=0, k=0 → universe 1
Position [2]: i=2, j=0, k=0 → universe 1
Position [3]: i=0, j=1, k=0 → universe 1
Position [4]: i=1, j=1, k=0 → universe 2
Position [5]: i=2, j=1, k=0 → universe 3
...
```

**Shorthand notation:**
```
FILL=0:2  0:2  0:0
     1 3R   $ Same as: 1 1 1 1
     5 2R 6 $ Same as: 5 5 5 6
```

Format: `value nR` means repeat value (n+1) times total
- `5 2R` = `5 5 5` (3 instances total)
- `10 9R` = `10 10 10 10 10 10 10 10 10 10` (10 instances total)

### Fill with Transformation

**Syntax:**
```
CELL  0  -SURF  FILL=u (TRn)  PARAMS
```

or inline:

```
CELL  0  -SURF  FILL=u (x y z)  PARAMS                      $ Translation only
CELL  0  -SURF  FILL=u (x y z  o1 o2 o3  ...)  PARAMS       $ Translation + rotation
```

**Transformation application:**
- Universe u coordinate system transformed before filling
- Origin of universe u moves to (x, y, z)
- Rotation matrix applied if specified

**Example:**
```
c Fill assembly at (10, 20, 0) with 45° rotation about z
1000  0  -100  FILL=10 (TR5)  IMP:N=1

TR5  10 20 0  45 45 90  135 45 90  90 90 0   $ Transformation card
```

### FILL Special Values

**FILL=0:** Cell remains void (no universe filled)

**Use case:** Create non-rectangular array patterns

**Example: L-shaped array**
```
100  0  -10  LAT=1  U=10  FILL=0:2  0:2  0:0  IMP:N=1
                            1 1 0    $ No universe at (2,0,0)
                            1 1 0    $ No universe at (2,1,0)
                            1 1 1    $ Full row
```

**FILL with negative universe:**
```
CELL  0  -SURF  FILL=-u  PARAMS   $ Fill with negative universe -u
```

**Use case:** Advanced optimization (use with caution)

---

## Lattice Element Requirements

### Convexity Requirement

**CRITICAL:** Lattice elements must be **convex** (no concave regions)

**Convex shapes (OK):**
- Rectangular parallelepiped (RPP)
- Hexagonal prism (RHP)
- Cylinder (RCC) - rarely used for lattices
- Any shape where line between any two points stays inside shape

**Non-convex shapes (NOT ALLOWED):**
- L-shapes
- T-shapes
- Shapes with indentations

### Opposite Sides Parallel

For rectangular lattices (LAT=1):
- Opposite faces must be parallel
- Faces must be perpendicular to coordinate axes (or aligned with surface ordering)

For hexagonal lattices (LAT=2):
- Hexagonal prism automatically satisfies requirements

### Element Size Determines Spacing

**The lattice element surface defines:**
- Size of each element
- Spacing between elements
- Alignment with coordinate system

**Example:**
```
c Lattice element: 1.5 cm × 1.5 cm × 200 cm
10  RPP  -0.75  0.75  -0.75  0.75  -100  100

c Creates lattice with:
c - 1.5 cm pitch in x and y
c - 200 cm height in z
c - Elements at (1.5i, 1.5j, 0) for integers i, j
```

---

## Truncation and Bounding

### Infinite Lattice Problem

**By default:** Lattice extends infinitely in all directions

**Problem:** Most problems need finite lattice

**Solution:** Place lattice inside bounding surface

### Truncation Methods

**Method 1: Bounding surface in main geometry**

```
c Lattice (infinite)
100  0  -10  LAT=1  U=10  FILL=1  IMP:N=1

c Truncate with bounding surface
1000  0  -100  FILL=10  IMP:N=1    $ Lattice fills region -100
1001  0   100  IMP:N=0              $ Outside lattice

100  RPP  -10  10  -10  10  -100  100   $ Bounding box
```

**Result:** Lattice fills only region inside surface 100

**Method 2: FILL array with limited indices**

```
c Define only 5×5 elements
100  0  -10  LAT=1  U=10  FILL=0:4  0:4  0:0  IMP:N=1
                            1 1 1 1 1
                            1 1 1 1 1
                            1 1 1 1 1
                            1 1 1 1 1
                            1 1 1 1 1
```

**Result:** Lattice contains only specified elements (5×5)

**Outside defined range:** Treated as void (particles killed or return to parent geometry)

---

## Coordinate Systems and Transformations

### Universe Local Coordinates

**Each universe has its own coordinate system:**
- Origin at (0, 0, 0) by default
- Independent of parent geometry
- Surfaces defined relative to universe origin

**Example:**
```
c Pin universe (local coordinates)
1  1  -10.5  -1  U=1  $ Fuel centered at (0,0,0) in universe 1

1  CZ  0.4   $ Cylinder at origin of universe 1
```

### TRCL (Transformation of Cell)

**Inline transformation:**
```
CELL  0  -SURF  FILL=u (x y z)  $ Translate origin to (x,y,z)
```

**Transformation card reference:**
```
CELL  0  -SURF  FILL=u (TRn)    $ Apply transformation TRn

TRn  x y z  [rotation matrix]   $ Transformation definition
```

**Transformation application order:**
1. Origin of universe u moves to (x, y, z)
2. Rotation matrix applied (if specified)
3. Universe geometry transformed accordingly

**Example:**
```
c Fill pin lattice at (5, 10, 0)
1000  0  -100  FILL=10 (5 10 0)  IMP:N=1

c Universe 10 origin now at (5, 10, 0) in main geometry
```

### TR Card Format

**Full syntax:**
```
TRn  x y z  o11 o21 o31  o12 o22 o32  o13 o23 o33  [m]
```

**Where:**
- (x, y, z) = displacement vector
- oij = rotation matrix elements (9 values)
- m = optional flag for origin interpretation

**Rotation matrix:**
```
   | o11  o12  o13 |
R =| o21  o22  o23 |
   | o31  o32  o33 |
```

**Shortcuts:**
- 9 elements: Full matrix
- 6 elements: Direction cosines (MCNP completes matrix)
- 5 elements: (θ, φ, ψ) Euler angles + 2 direction cosines
- 3 elements: Rotation axis direction cosines
- 0 elements: Translation only (no rotation)

**Example: 90° rotation about z-axis**
```
TR1  0 0 0  0 90 90  90 0 90  90 90 0
```

---

## No Speed Benefit - Memory and Input Only

**IMPORTANT:** Repeated structures provide **NO computational speed benefit**

**Benefits:**
- **Memory savings:** One universe definition vs thousands of cells
- **Input file size:** Smaller, more manageable input
- **Modification ease:** Change universe once, affects all instances
- **Error reduction:** Less duplication = fewer errors

**NOT benefits:**
- ❌ Faster particle tracking
- ❌ Reduced computation time
- ❌ Better performance

**Reason:** MCNP tracks particles through each instance individually - no shortcut in tracking algorithm

---

## Integration with MCNP Features

### Importance (IMP Card)

**Inheritance:** Universes inherit importance from filled cell

```
c Lattice cell importance
100  0  -10  LAT=1  U=10  FILL=1  IMP:N=1

c All instances of universe 1 have IMP:N=1
```

**Override:** Can specify different importance in universe

```
c Universe with different importance
1  1  -10.5  -1  U=1  IMP:N=2   $ Higher importance in universe
```

### Volume Specification (VOL Card)

**Problem:** MCNP cannot calculate volumes for repeated structure cells

**Solution:** Specify volumes manually on cell card or with SD tally card

**On cell card:**
```
1  1  -10.5  -1  U=1  VOL=0.503  IMP:N=1   $ Volume per instance
```

**With SD card:**
```
F4:N  1   $ Tally in cell 1 (universe 1)
SD4  0.503   $ Volume per instance (cm³)
```

**CRITICAL:** Volume should be per-instance, not total. MCNP counts instances automatically.

### Tallies in Lattices

**Challenge:** Tally applies to ALL instances of universe cell

**Example:**
```
F4:N  1   $ Flux in cell 1 - ALL instances averaged together
```

**Solution for specific elements:** Use TALLYX subroutine or FS card (advanced, see User Manual §5.9.17)

---

## Best Practices Summary

1. **Always bound universes** - No infinite cells except optional background cell
2. **Verify surface ordering** - For LAT cells, order defines index directions
3. **Check element size** - Must match intended pitch exactly
4. **Use consistent numbering** - Systematic universe numbering scheme (e.g., U=1-99 pins, U=100-999 assemblies)
5. **Test single element first** - Verify universe geometry before creating full lattice
6. **Specify volumes** - VOL or SD cards required for repeated structure cells
7. **Document hierarchy** - Comment universe nesting structure clearly
8. **Plot geometry** - Visual verification essential before running
9. **FILL array ordering** - Remember Fortran ordering (i fastest)
10. **Transformation verification** - Plot transformed universes to confirm position/orientation

---

**END OF LATTICE FUNDAMENTALS REFERENCE**

For application guidance, see main SKILL.md. For reactor modeling, see reactor_to_mcnp_workflow.md.
