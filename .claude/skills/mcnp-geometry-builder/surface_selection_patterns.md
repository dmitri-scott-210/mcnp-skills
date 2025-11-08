# Surface Selection Patterns for Complex Geometries

## Overview

Choosing the correct surface type in MCNP is critical for:
1. **Performance** - SO/CZ track 10-100× faster than general surfaces
2. **Accuracy** - Centered surfaces avoid numerical precision issues
3. **Simplicity** - Simpler surfaces = easier debugging
4. **Compatibility** - Some features require specific surface types (lattices)

This guide provides decision trees and patterns for common reactor modeling scenarios.

---

## Decision Trees for Common Applications

### Reactor Fuel Modeling

#### TRISO Particle Fuel
**Requirement**: 5-layer spherical coating structure
**Surfaces**: SO (spheres at origin in universe)
**Reason**: Fastest tracking, particle replicated thousands of times

```mcnp
c Universe u=100 (TRISO particle)
c Surfaces (centered at origin for universe)
1  so  0.02500    $ Kernel (250 μm)
2  so  0.03500    $ Buffer (350 μm)
3  so  0.03900    $ IPyC (390 μm)
4  so  0.04250    $ SiC (425 μm)
5  so  0.04650    $ OPyC (465 μm)

c Cell Cards
1  1  -10.8   -1       u=100  $ Kernel (UO2)
2  2  -0.98    1  -2   u=100  $ Buffer (porous C)
3  3  -1.85    2  -3   u=100  $ IPyC (dense C)
4  4  -3.20    3  -4   u=100  $ SiC (ceramic)
5  5  -1.86    4  -5   u=100  $ OPyC (dense C)
6  6  -1.75    5       u=100  $ Matrix (graphite)
```

**Why SO not S?**
- SO is 10× faster (optimized tracking algorithm)
- Particle centered at origin in universe U=100
- Universe translated/filled to position particles

#### PWR Fuel Pin
**Requirement**: Cylindrical fuel/gap/clad/coolant
**Surfaces**: CZ (cylinders on Z-axis in universe)
**Reason**: Axial symmetry, simple tracking

```mcnp
c Universe u=10 (fuel pin)
c Surfaces
1  cz  0.4095    $ Fuel pellet radius
2  cz  0.4178    $ Gap outer radius
3  cz  0.4750    $ Clad outer radius

c Cell Cards
1  1  -10.5  -1       u=10  $ Fuel
2  0         1  -2    u=10  $ Gap
3  2  -6.5    2  -3   u=10  $ Clad
4  3  -1.0    3       u=10  $ Coolant
```

**Why CZ not C/Z?**
- CZ is 5× faster (axis-aligned)
- Pin centered at origin in universe
- Universe filled in lattice or translated to position

#### BWR Fuel Pin (Water Rod)
**Requirement**: Similar to PWR but with central water channel
**Surfaces**: CZ (concentric cylinders on Z-axis)
**Reason**: Multiple concentric regions, all centered

```mcnp
c Universe u=11 (BWR fuel pin with inner water channel)
c Surfaces
1  cz  0.250     $ Inner water channel
2  cz  0.300     $ Inner clad inner
3  cz  0.350     $ Inner clad outer / fuel inner
4  cz  0.550     $ Fuel outer
5  cz  0.600     $ Outer clad inner (gap)
6  cz  0.650     $ Outer clad outer

c Cell Cards
1  3  -1.0   -1          u=11  $ Inner water
2  2  -6.5    1  -2      u=11  $ Inner clad
3  1  -10.5   2  -3      u=11  $ Fuel (inner annulus)
4  1  -10.5   3  -4      u=11  $ Fuel (outer annulus) - same material
5  0          4  -5      u=11  $ Gap
6  2  -6.5    5  -6      u=11  $ Outer clad
7  3  -1.0    6          u=11  $ Coolant
```

#### Multi-Stack Assembly
**Requirement**: Multiple parallel fuel channels
**Surfaces**: C/Z (off-axis cylinders)
**Reason**: Each stack at different (x,y) position

```mcnp
c Stack 1 at (5.0, 0.0)
11  c/z  5.0  0.0  0.5    $ Stack 1 compact
12  c/z  5.0  0.0  0.6    $ Stack 1 channel

c Stack 2 at (-5.0, 0.0)
21  c/z  -5.0  0.0  0.5   $ Stack 2 compact
22  c/z  -5.0  0.0  0.6   $ Stack 2 channel

c Stack 3 at (0.0, 5.0)
31  c/z  0.0  5.0  0.5    $ Stack 3 compact
32  c/z  0.0  5.0  0.6    $ Stack 3 channel
```

**Why C/Z not CZ?**
- Stacks at different (x,y) positions
- C/Z allows off-axis positioning
- All stacks share same Z extent (use PZ for axial bounds)

---

### Lattice Boundary Selection

#### Rectangular Lattice (LAT=1)
**Requirement**: Square or rectangular pin array
**Surface**: RPP (rectangular parallelepiped)
**Reason**: LAT=1 **requires** RPP boundary

```mcnp
c Lattice cell (3×3 array)
100  0  -100  u=200  lat=1  fill=-1:1 -1:1 0:0
     10 10 10
     10 10 10
     10 10 10

c Surface (MUST be RPP for LAT=1)
100  rpp  -1.5 1.5  -1.5 1.5  0 10    $ 3×3 array, 1 cm pitch, 10 cm height
```

**Pitch Calculation**:
- Pitch = 1.0 cm
- Array: -1:1 in X (3 positions), -1:1 in Y (3 positions)
- X extent: 3 × 1.0 = 3.0 cm → -1.5 to +1.5
- Y extent: 3 × 1.0 = 3.0 cm → -1.5 to +1.5
- Z extent: explicit (0 to 10 cm)

**Common Error**: Using PX/PY/PZ instead of RPP
```mcnp
c WRONG - will not work with LAT=1
100  px  -1.5
101  px   1.5
102  py  -1.5
103  py   1.5
104  pz   0
105  pz   10
```

#### Hexagonal Lattice (LAT=2)
**Requirement**: Hexagonal pin array
**Surface**: RHP (hexagonal prism) with 9 values
**Reason**: LAT=2 **requires** RHP boundary

```mcnp
c Hexagonal lattice (19-element assembly)
200  0  -200  u=300  lat=2  fill=-2:2 -2:2 0:0
     [... 25 universe values in hexagonal pattern ...]

c Surface (MUST be RHP with 9 values for LAT=2)
c Format: RHP vx vy vz  hx hy hz  Rx Ry Rz
200  rhp  0 0 0   0 0 68   0 1.6 0    $ Hex block, height=68 cm, R=1.6 cm
```

**RHP 9-Value Specification**:
- **vx vy vz**: Origin (usually 0 0 0)
- **hx hy hz**: Height vector (0 0 68 for 68 cm tall)
- **Rx Ry Rz**: Radius vector (0 1.6 0 for 1.6 cm pitch)

**Pitch Calculation**:
- R = 1.6 cm (specified in Ry)
- Hexagonal pitch = R × √3 = 1.6 × 1.732 = 2.77 cm

**Common Error**: Using 4-value RHP (old syntax)
```mcnp
c WRONG - old syntax, does not work in MCNP6
200  rhp  0 0 0  1.6    $ 4 values - DEPRECATED
```

---

### Axial Segmentation

#### Shared Axial Planes
**Requirement**: Multiple cells sharing same Z-boundaries
**Surface**: PZ (plane perpendicular to Z)
**Reason**: Single PZ referenced by many cells

```mcnp
c Three concentric cylinders, all with same height
1  1  -10.5  -1   -10 11   $ Fuel
2  0         1 -2  -10 11   $ Gap
3  2  -6.5    2 -3  -10 11   $ Clad

c Radial surfaces
1  cz  0.41
2  cz  0.42
3  cz  0.48

c Axial surfaces (shared by all cells)
10  pz  0.0      $ Bottom (shared)
11  pz  360.0    $ Top (shared)
```

**Why PZ not macrobody?**
- Single PZ can bound hundreds of cells
- Easier to change (one line vs. many)
- Enables axial tallies on specific planes

#### Axial Zones with Different Materials
**Requirement**: Stack with different zones (plenum, fuel, plenum)
**Surfaces**: Multiple PZ planes
**Pattern**: Use PZ to segment, CZ for radial

```mcnp
c Fuel pin with 5 axial zones
1  0         -1  -101 102   $ Lower plenum (void)
2  1  -10.5  -1   102 103   $ Fuel zone 1
3  1  -10.5  -1   103 104   $ Fuel zone 2
4  1  -10.5  -1   104 105   $ Fuel zone 3
5  0         -1   105 106   $ Upper plenum (void)
6  2  -6.5    1 -2  -101 106   $ Clad (full height)
7  3  -1.0    2    -101 106   $ Coolant

c Radial surfaces
1  cz  0.41    $ Fuel radius
2  cz  0.48    $ Clad outer

c Axial surfaces
101  pz  0.0      $ Bottom
102  pz  10.0     $ End of lower plenum
103  pz  130.0    $ End of fuel zone 1
104  pz  250.0    $ End of fuel zone 2
105  pz  370.0    $ End of fuel zone 3
106  pz  380.0    $ Top
```

---

## Performance Optimization

### Tracking Speed Ranking

**Fastest to Slowest** (approximate relative performance):

1. **SO, CZ, PX/PY/PZ** (1.0×) - optimized tracking
   - Use for universe-centered geometry
   - Example: TRISO particles, fuel pins

2. **SX, SY, SZ** (1.2×) - axis-aligned spheres
   - Rarely needed (use SO in universe instead)

3. **S** (2.0×) - general sphere
   - Use when SO not applicable
   - Example: Detector at arbitrary position

4. **C/X, C/Y, C/Z** (2.5×) - off-axis cylinders
   - Essential for multi-stack geometries
   - Example: Three fuel stacks in capsule

5. **P** (5.0×) - general plane
   - Use only when PX/PY/PZ inadequate
   - Example: Slanted surfaces, non-orthogonal geometry

6. **Macrobodies** (10.0×) - expand to multiple facets
   - RPP → 6 plane facets
   - RCC → 3 facets (cone sides + 2 planes)
   - RHP → 8 facets (6 sides + 2 planes)
   - Use judiciously

**Performance Example**:
```mcnp
c Fast: Centered sphere in universe
1  so  10.0    u=100    $ Tracking: 1.0× baseline

c Slow: General sphere at position
1  s  5.7 -3.2 8.1  10.0    $ Tracking: 2.0× baseline

c Better: Use SO in universe, translate universe
1  so  10.0    u=100
100  0  -100  fill=100  (5.7 -3.2 8.1)    $ Tracking: 1.0× baseline + negligible fill overhead
```

### When to Use Macrobodies vs Primitives

#### Use Macrobodies (RPP, RCC, RHP) when:
- ✅ Input file simplicity more important than performance
- ✅ Prototyping or teaching (easier to visualize)
- ✅ No need for separate facet tallies (F2, F4:S)
- ✅ Not using SSR/SSW/PTRAC (facet restrictions apply)
- ✅ One-time calculation (not production runs)

**Example: Simple shielding problem**
```mcnp
c Room geometry (macrobodies OK here)
1  1  -2.35  -1       $ Concrete room
2  0         1  -2    $ Air inside
3  0         2        $ Outside (graveyard)

1  rpp  -500 500  -500 500  0 300    $ Room
2  rpp  -450 450  -450 450  10 290   $ Interior
```

#### Use Primitives (P, CZ, SO) when:
- ✅ Need surface-specific tallies
- ✅ Using SSR (surface source read) or SSW (write)
- ✅ Complex Boolean operations (easier with primitives)
- ✅ Production calculations (performance critical)
- ✅ Need to reference specific facets

**Example: Detailed reactor model**
```mcnp
c Core geometry (primitives for performance)
1  px  -150    $ West boundary
2  px   150    $ East boundary
3  py  -150    $ South boundary
4  py   150    $ North boundary
5  pz    0     $ Bottom
6  pz   400    $ Top

c Cells (use primitives for speed)
100  1  -10.5  -1 2 -3 4 -5 6    $ Core (6 plane intersections)
101  0          (1:-2:3:-4:5:-6)  $ Outside
```

---

## Complete Decision Matrix

### Surface Selection by Geometry Type

| Geometry | Centered? | Surface Type | Performance | Use Case |
|----------|-----------|--------------|-------------|----------|
| **Sphere** | Yes (universe) | SO | Fastest | TRISO particles, repeated spheres |
| | Yes (X-axis) | SX | Fast | Rarely needed |
| | Yes (Y-axis) | SY | Fast | Rarely needed |
| | Yes (Z-axis) | SZ | Fast | Rarely needed |
| | Arbitrary | S | Medium | Detectors, non-repeated |
| | Box (macro) | SPH | Slow | Simple cases only |
| **Cylinder** | Z-axis (universe) | CZ | Fastest | Fuel pins, centered channels |
| | X-axis (universe) | CX | Fast | Horizontal pipes |
| | Y-axis (universe) | CY | Fast | Horizontal pipes |
| | Off-axis (any) | C/X, C/Y, C/Z | Medium | Multi-stack assemblies |
| | Macro | RCC | Slow | Simple cases only |
| **Plane** | X = const | PX | Fastest | Slab geometry, lattice bounds |
| | Y = const | PY | Fastest | Slab geometry, lattice bounds |
| | Z = const | PZ | Fastest | Axial zones (use for all axial) |
| | General | P | Slow | Slanted surfaces only |
| **Box** | Axis-aligned | RPP | Medium | Lattice boundaries (LAT=1) |
| | Macro | BOX | Slow | Avoid (use RPP) |
| **Hex Prism** | Lattice | RHP (9 val) | Medium | Hexagonal lattice (LAT=2) |
| | Macro | HEX | Slow | Avoid (use RHP 9-value) |

---

## Common Patterns by Reactor Type

### PWR (Pressurized Water Reactor)

**Fuel Pin Universe**:
```mcnp
c Universe u=10 (centered at origin)
c Surfaces (all CZ - fastest)
1  cz  0.4095    $ Fuel
2  cz  0.4178    $ Gap
3  cz  0.4750    $ Clad

c Cells
1  1  -10.5  -1       u=10  $ Fuel
2  0         1  -2    u=10  $ Gap
3  2  -6.5    2  -3   u=10  $ Clad
4  3  -1.0    3       u=10  $ Water
```

**Lattice Boundary**:
```mcnp
c MUST use RPP for LAT=1
100  rpp  -10.71 10.71  -10.71 10.71  0 366    $ 17×17 assembly
```

**Axial Segmentation**:
```mcnp
c Use PZ (shared across all pins)
1000  pz  0.0      $ Bottom
1001  pz  60.96    $ Zone 1
1002  pz  121.92   $ Zone 2
...
1006  pz  365.76   $ Top
```

### BWR (Boiling Water Reactor)

**Similar to PWR but**:
- Some pins have water rods (use CZ for concentric inner channel)
- Control blade channels (use C/Z or guide tubes)
- Lower void fraction in coolant

### VVER (Russian PWR)

**Hexagonal Assembly**:
```mcnp
c MUST use RHP (9 values) for LAT=2
100  rhp  0 0 0   0 0 350   0 1.45 0    $ 312-element assembly
```

### HTGR (High-Temperature Gas Reactor)

**TRISO Particle**:
```mcnp
c Universe u=100 (SO - fastest)
1  so  0.02500    $ Kernel
2  so  0.03500    $ Buffer
3  so  0.03900    $ IPyC
4  so  0.04250    $ SiC
5  so  0.04650    $ OPyC
```

**Compact (fuel compacts in channels)**:
```mcnp
c Universe u=200 (CZ if centered)
1  cz  0.635     $ Compact radius
2  cz  0.793     $ Channel radius
```

**Hexagonal Block**:
```mcnp
c RHP (9 values) for LAT=2
100  rhp  0 0 0   0 0 79.3   0 1.8796 0    $ Prismatic block
```

**Multi-Stack Capsule (AGR-1 style)**:
```mcnp
c Three stacks at different positions (C/Z - off-axis)
11  c/z  25.547  -24.553  0.635    $ Stack 1
21  c/z  24.553  -25.547  0.635    $ Stack 2
31  c/z  25.911  -25.911  0.635    $ Stack 3
```

### Fast Reactor (Sodium-Cooled)

**Hexagonal Duct**:
```mcnp
c RHP (9 values) for hex assembly
100  rhp  0 0 0   0 0 200   0 6.5 0    $ Sodium-cooled assembly
```

**Fuel Pin** (similar to PWR):
```mcnp
c CZ (centered in universe)
1  cz  0.292    $ Fuel (UO2 or MOX)
2  cz  0.300    $ Gap
3  cz  0.336    $ Clad (often thicker for fast spectrum)
```

---

## Special Cases

### Detector Positioning

**Fixed detector at known location**:
```mcnp
c Use S (general sphere) - flexibility over speed
100  s  50.0 0.0 100.0  5.0    $ Detector at (50, 0, 100), R=5 cm
```

**Detector array** (use universes):
```mcnp
c Detector universe u=500 (SO - fastest)
1  so  5.0    u=500

c Position detectors by filling universes
c Fill at (50, 0, 100)
100  0  -100  fill=500  (50 0 100)
c Fill at (-50, 0, 100)
101  0  -101  fill=500  (-50 0 100)

c Bounding surfaces (RPP)
100  rpp  45 55  -5 5  95 105
101  rpp  -55 -45  -5 5  95 105
```

### Shielding Layers

**Concentric spherical shields**:
```mcnp
c Use SO if possible (center at origin)
1  so  10.0     $ Source region
2  so  15.0     $ Shield layer 1
3  so  25.0     $ Shield layer 2
4  so  50.0     $ Outer boundary
```

**Slab shields**:
```mcnp
c Use PX/PY/PZ (fastest)
1  px  0.0      $ Source side
2  px  10.0     $ Shield 1 (concrete)
3  px  12.0     $ Shield 2 (steel)
4  px  20.0     $ Outer boundary
```

---

## Debugging Surface Selection

### Check Surface Usage
```bash
# Count surface types in input file
grep -E "^\s*[0-9]+\s+(so|s|cz|c/z|px|py|pz|p\s)" input.i | \
  awk '{print $2}' | sort | uniq -c
```

### Plot Surfaces
```bash
# Interactive plot to verify surface types
mcnp6 inp=input.i ip

# In plotter:
# - origin X Y Z (center view)
# - extent EX EY EZ (zoom)
# - basis U1 U2 U3  V1 V2 V3 (rotate view)
```

### Performance Test
```bash
# Compare performance of different surface types
# Run same problem with:
# 1. SO/CZ in universes (fast)
# 2. S/C/Z global (slow)
# Check MCNP output for "average time per history"
```

---

## Summary

### Quick Selection Guide

1. **Sphere**:
   - Repeated/universe → **SO**
   - Single/global → **S**

2. **Cylinder**:
   - Centered/universe → **CZ** (or CX, CY)
   - Off-axis → **C/Z** (or C/X, C/Y)

3. **Plane**:
   - Axis-aligned → **PX, PY, PZ**
   - General → **P** (only if needed)

4. **Lattice Boundary**:
   - Rectangular → **RPP** (required for LAT=1)
   - Hexagonal → **RHP 9-value** (required for LAT=2)

5. **Macrobodies**:
   - Prototyping → OK
   - Production → Use primitives

### Performance Rules
- ✅ Use centered surfaces (SO, CZ) in universes
- ✅ Use positioned surfaces (S, C/Z) sparingly
- ✅ Share surfaces (PZ) when possible
- ✅ Avoid macrobodies in tight loops
- ✅ Test performance if uncertain

### Common Mistakes
- ❌ Using S instead of SO for repeated structures
- ❌ Using C/Z when CZ would work (universe)
- ❌ Using primitives for lattice boundaries (use RPP/RHP)
- ❌ Using 4-value RHP (old syntax)
- ❌ Using macrobodies for surface-specific tallies

---

**See Also**:
- `surface_types_comprehensive.md` - All 25+ surface types with equations
- `concentric_geometry_reference.md` - Nested sphere/cylinder patterns
- `lattice_geometry_reference.md` - LAT=1 and LAT=2 specifications

**Version**: 1.0.0 (2025-11-08)
**Part of**: mcnp-geometry-builder skill refinement
