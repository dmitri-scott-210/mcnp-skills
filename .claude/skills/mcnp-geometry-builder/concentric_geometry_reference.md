# Concentric Geometry Reference
## Patterns for Nested Spherical and Cylindrical Structures

## Overview

Concentric geometries are fundamental in reactor modeling:
- **TRISO particles**: 5-layer spherical coating
- **Fuel pins**: Fuel/gap/clad/coolant cylinders
- **Capsules**: Multi-layer containment structures
- **Shielding**: Nested spherical or cylindrical shields
- **Detectors**: Concentric detector layers

This reference provides templates, volume calculations, and debugging guidance.

---

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
- **R1 < R2 < R3 < ... < RN** (strictly increasing)
- Cell J bounded by surfaces J and J+1
- Inner cell uses `-1`
- Shell cells use `J -(J+1)`
- Outer cell uses `N` (positive = outside)

### Example 1: TRISO Particle (5-Layer Coating)

**Specifications**:
- Kernel (UO2): 500 μm diameter (R = 0.0250 cm)
- Buffer (porous C): 100 μm thick (R = 0.0350 cm)
- IPyC (dense PyC): 40 μm thick (R = 0.0390 cm)
- SiC (ceramic): 35 μm thick (R = 0.0425 cm)
- OPyC (dense PyC): 40 μm thick (R = 0.0465 cm)

**Complete Definition**:
```mcnp
c Cell Cards (universe u=100 for repeated structure)
1  1  -10.8   -1       u=100  vol=6.545e-5   $ Kernel (250 μm radius)
2  2  -0.98    1  -2   u=100  vol=1.139e-4   $ Buffer (100 μm thick)
3  3  -1.85    2  -3   u=100  vol=4.676e-5   $ IPyC (40 μm thick)
4  4  -3.20    3  -4   u=100  vol=4.315e-5   $ SiC (35 μm thick)
5  5  -1.86    4  -5   u=100  vol=5.339e-5   $ OPyC (40 μm thick)
6  6  -1.75    5       u=100                 $ Matrix (graphite)

c Surface Cards (SO - centered at origin for universe)
1  so  0.02500    $ Kernel radius (250 μm = 0.0250 cm)
2  so  0.03500    $ Buffer outer (350 μm)
3  so  0.03900    $ IPyC outer (390 μm)
4  so  0.04250    $ SiC outer (425 μm)
5  so  0.04650    $ OPyC outer (465 μm)
```

**Volume Calculations** (for verification):
```python
import math

def sphere_volume(r):
    return (4/3) * math.pi * r**3

def shell_volume(r_inner, r_outer):
    return sphere_volume(r_outer) - sphere_volume(r_inner)

# TRISO volumes
v_kernel = sphere_volume(0.02500)           # 6.545e-5 cm³
v_buffer = shell_volume(0.02500, 0.03500)   # 1.139e-4 cm³
v_ipyc   = shell_volume(0.03500, 0.03900)   # 4.676e-5 cm³
v_sic    = shell_volume(0.03900, 0.04250)   # 4.315e-5 cm³
v_opyc   = shell_volume(0.04250, 0.04650)   # 5.339e-5 cm³

print(f"Kernel: {v_kernel:.3e} cm³")
print(f"Buffer: {v_buffer:.3e} cm³")
print(f"IPyC:   {v_ipyc:.3e} cm³")
print(f"SiC:    {v_sic:.3e} cm³")
print(f"OPyC:   {v_opyc:.3e} cm³")
```

### Example 2: Bare Sphere Critical Assembly (3 layers)

**Specifications**:
- Core (Pu): 4.5 cm radius
- Reflector (Be): 5.0 cm outer radius
- Shield (Pb): 15.0 cm outer radius

```mcnp
c Cell Cards
1  1  -19.8   -1          imp:n=1  vol=381.7    $ Plutonium core
2  2  -1.85    1  -2      imp:n=2  vol=142.4    $ Beryllium reflector
3  3  -11.35   2  -3      imp:n=2  vol=13533.8  $ Lead shield
4  0          3           imp:n=0               $ Graveyard

c Surface Cards
1  so  4.5     $ Core outer
2  so  9.5     $ Reflector outer (4.5 + 5.0)
3  so  15.0    $ Shield outer

c Data Cards
mode n
sdef pos=0 0 0  erg=2.0
m1  94239.70c  1.0    $ Plutonium-239
m2  4009.70c   1.0    $ Beryllium-9
m3  82000.50c  1.0    $ Lead (natural)
nps 100000
```

**Key Pattern**:
- Core: `-1` (inside surface 1)
- Reflector: `1 -2` (outside 1, inside 2)
- Shield: `2 -3` (outside 2, inside 3)
- Graveyard: `3` (outside 3)

### Example 3: Detector Calibration (5-layer)

**Application**: Multi-layer detector with different scintillators

```mcnp
c Detector universe u=200
1  1  -1.032   -1       u=200  $ Plastic scintillator (inner)
2  2  -8.0      1  -2   u=200  $ Lead absorber
3  3  -3.67     2  -3   u=200  $ NaI(Tl) crystal
4  4  -2.7      3  -4   u=200  $ Aluminum housing
5  5  -1.2e-3   4  -5   u=200  $ Air gap
6  6  -2.7      5       u=200  $ Outer aluminum

c Surfaces
1  so  2.0     $ Inner scintillator
2  so  2.5     $ Lead layer
3  so  7.5     $ NaI crystal
4  so  7.8     $ Inner housing
5  so  8.0     $ Air gap
```

---

## Nested Cylinders (Axial Symmetry)

### Pattern 2: N-Layer Cylindrical Shell (Centered)

**Applications**: Fuel pins, coolant channels, pipes, cylindrical detectors

**General Template (CZ - centered on Z-axis)**:
```mcnp
c Cells
1    1  -D1   -1  zmin -zmax      u=U  $ Core
2    2  -D2    1  -2  zmin -zmax  u=U  $ Layer 1
3    3  -D3    2  -3  zmin -zmax  u=U  $ Layer 2
...
N    N  -DN   (N-1) -N  zmin -zmax  u=U  $ Layer N-1
N+1  0        N      zmin -zmax     u=U  $ Exterior

c Radial Surfaces
1   cz  R1
2   cz  R2
3   cz  R3
...
N   cz  RN

c Axial Surfaces
zmin  pz  Z1
zmax  pz  Z2
```

**Constraints**:
- **R1 < R2 < R3 < ... < RN** (strictly increasing)
- Same axial bounds (zmin, zmax) for all layers
- Use PZ surfaces (shared across cells)

### Example 4: PWR Fuel Pin (4 regions)

**Specifications**:
- Fuel pellet: 0.4095 cm radius
- Gap: 0.0083 cm thick (total R = 0.4178 cm)
- Cladding: 0.0572 cm thick (total R = 0.4750 cm)
- Height: 366 cm active fuel length

```mcnp
c Cell Cards (universe u=10)
1  1  -10.5  -1  -10 11     u=10  imp:n=1  $ UO2 fuel
2  0         1  -2  -10 11  u=10  imp:n=1  $ Helium gap
3  2  -6.5   2  -3  -10 11  u=10  imp:n=1  $ Zircaloy clad
4  3  -1.0   3      -10 11  u=10  imp:n=1  $ Water coolant

c Radial Surfaces
1   cz  0.4095     $ Fuel pellet outer
2   cz  0.4178     $ Gap outer (clad inner)
3   cz  0.4750     $ Clad outer

c Axial Surfaces (shared)
10  pz  0.0        $ Bottom
11  pz  366.0      $ Top (active fuel length)

c Materials
m1  $ UO2 fuel (4.5% enriched)
    92234.70c  3.80e-4
    92235.70c  0.0450
    92238.70c  0.9550
     8016.70c  2.0000
m2  $ Zircaloy-4
    40000.60c  0.9821
    26000.50c  0.0022
m3  $ Light water
     1001.70c  2.0
     8016.70c  1.0
mt3 lwtr.13t
```

**Volume Calculation**:
```python
import math

def cylinder_shell_volume(r_inner, r_outer, height):
    return math.pi * height * (r_outer**2 - r_inner**2)

h = 366.0  # cm

v_fuel = math.pi * (0.4095**2) * h          # 192.5 cm³
v_gap  = cylinder_shell_volume(0.4095, 0.4178, h)  # 3.74 cm³
v_clad = cylinder_shell_volume(0.4178, 0.4750, h)  # 36.2 cm³

print(f"Fuel volume: {v_fuel:.1f} cm³")
print(f"Gap volume:  {v_gap:.2f} cm³")
print(f"Clad volume: {v_clad:.1f} cm³")
```

### Example 5: BWR Fuel Pin with Inner Water Channel

**Specifications**:
- Inner water channel: 0.25 cm radius
- Inner clad: 0.30 cm inner, 0.35 cm outer
- Fuel (annular): 0.35 cm inner, 0.55 cm outer
- Gap: 0.55 cm inner, 0.60 cm outer
- Outer clad: 0.60 cm inner, 0.65 cm outer

```mcnp
c Cell Cards (universe u=11)
1  3  -1.0   -1          -10 11  u=11  $ Inner water
2  2  -6.5    1  -2      -10 11  u=11  $ Inner clad
3  1  -10.5   2  -3      -10 11  u=11  $ Fuel (annular)
4  0          3  -4      -10 11  u=11  $ Gap
5  2  -6.5    4  -5      -10 11  u=11  $ Outer clad
6  3  -1.0    5          -10 11  u=11  $ Coolant

c Radial Surfaces (all CZ - centered)
1  cz  0.25    $ Inner water outer
2  cz  0.30    $ Inner clad inner
3  cz  0.35    $ Inner clad outer / fuel inner
4  cz  0.55    $ Fuel outer / gap inner
5  cz  0.60    $ Gap outer / outer clad inner
6  cz  0.65    $ Outer clad outer

c Axial Surfaces
10  pz  0.0
11  pz  380.0
```

**Key Pattern**: Annular fuel region bounded by surfaces 2 and 3

---

## Off-Axis Concentric Cylinders (C/Z)

### Pattern 3: N-Layer Cylindrical Shell (Off-Axis)

**Applications**: Multi-stack assemblies, off-axis experiments, capsule structures

**General Template (C/Z - off-axis)**:
```mcnp
c Cells (all centered at x0, y0)
1    1  -D1   -1              zmin -zmax  $ Core
2    2  -D2    1  -2          zmin -zmax  $ Layer 1
3    3  -D3    2  -3          zmin -zmax  $ Layer 2
...
N    N  -DN   (N-1) -N       zmin -zmax  $ Layer N-1
N+1  0        N               zmin -zmax  $ Exterior

c Radial Surfaces (all c/z with SAME center x0, y0)
1   c/z  x0  y0  R1
2   c/z  x0  y0  R2
3   c/z  x0  y0  R3
...
N   c/z  x0  y0  RN

c Axial Surfaces (shared)
zmin  pz  Z1
zmax  pz  Z2
```

**Critical Requirement**: ALL C/Z surfaces must have **same (x0, y0) center**

### Example 6: AGR-1 Capsule Structure (7 layers, off-axis)

**Specifications**:
- Center: (25.337, -25.337) cm
- Fuel compact: 6.35 mm radius
- Gas gap: 0.6 mm thick
- Graphite holder: 15.19 mm outer radius
- Gap: 6.8 mm thick
- SS wall: 3.4 mm thick
- Hf shroud: 2.5 mm thick
- Outer wall: 13.8 mm thick
- Height: 129.54 cm

```mcnp
c Cell Cards (all centered at 25.337, -25.337)
1  1  -10.9   -1              -10 11  imp:n=1  $ Fuel compact
2  0          1  -2           -10 11  imp:n=1  $ Gas gap (0.6 mm)
3  2  -1.75   2  -3           -10 11  imp:n=1  $ Graphite holder
4  0          3  -4           -10 11  imp:n=1  $ Gap (6.8 mm)
5  3  -8.0    4  -5           -10 11  imp:n=1  $ SS wall (3.4 mm)
6  4  -13.3   5  -6           -10 11  imp:n=1  $ Hafnium shroud (2.5 mm)
7  3  -8.0    6  -7           -10 11  imp:n=1  $ Outer wall (13.8 mm)
8  5  -1.2e-3 7              -10 11  imp:n=1  $ Air outside
9  0          11                      imp:n=0  $ Graveyard

c Radial Surfaces (all c/z with SAME center: 25.337, -25.337)
1   c/z  25.337  -25.337  0.6350    $ Compact (6.35 mm)
2   c/z  25.337  -25.337  0.6413    $ Gas gap outer (6.41 mm)
3   c/z  25.337  -25.337  1.5191    $ Holder outer (15.19 mm)
4   c/z  25.337  -25.337  1.5875    $ Gap outer (15.88 mm)
5   c/z  25.337  -25.337  1.6218    $ SS wall outer (16.22 mm)
6   c/z  25.337  -25.337  1.6472    $ Hf shroud outer (16.47 mm)
7   c/z  25.337  -25.337  1.7856    $ Outer wall outer (17.86 mm)

c Axial Surfaces (shared)
10  pz  0.0
11  pz  129.54

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
m4  $ Hafnium
   72000.60c  1.0
m5  $ Air
    7014.70c  0.8
    8016.70c  0.2
```

**Verification**:
- Check all C/Z have same center (25.337, -25.337) ✓
- Check radii strictly increasing (0.635 < 0.641 < ... < 1.786) ✓
- Check thin gaps (0.6 mm may cause tracking issues) ⚠

---

## Multiple Concentric Systems (Different Centers)

### Pattern 4: Multiple Independent Concentric Systems

**Application**: Multi-stack assemblies, detector arrays, independent experiments

**Example 7: Three Fuel Stacks in Triangular Arrangement**

**Specifications**:
- Stack 1 center: (25.547, -24.553)
- Stack 2 center: (24.553, -25.547)
- Stack 3 center: (25.911, -25.911)
- All stacks: 6.35 mm compact radius, 6.41 mm channel radius
- Shared outer capsule center: (25.337, -25.337), R = 17.86 mm

```mcnp
c Stack 1 (centered at 25.547, -24.553)
11  1  -10.9  -11         -10 12  imp:n=1  $ Compact
12  0         11  -12     -10 12  imp:n=1  $ Gap

c Stack 2 (centered at 24.553, -25.547)
21  1  -10.9  -21         -10 12  imp:n=1  $ Compact
22  0         21  -22     -10 12  imp:n=1  $ Gap

c Stack 3 (centered at 25.911, -25.911)
31  1  -10.9  -31         -10 12  imp:n=1  $ Compact
32  0         31  -32     -10 12  imp:n=1  $ Gap

c Graphite filler (between stacks)
100 2  -1.75  12 -100  (11:21:31)  imp:n=1  $ Graphite (not in stacks)

c Outer capsule (centered at 25.337, -25.337)
200 3  -8.0   100  -200  -10 12  imp:n=1  $ Capsule wall
999 0         200                 imp:n=0  $ Graveyard

c Stack 1 surfaces (center: 25.547, -24.553)
11  c/z  25.547  -24.553  0.6350    $ Compact
12  c/z  25.547  -24.553  0.6413    $ Channel

c Stack 2 surfaces (center: 24.553, -25.547)
21  c/z  24.553  -25.547  0.6350    $ Compact
22  c/z  24.553  -25.547  0.6413    $ Channel

c Stack 3 surfaces (center: 25.911, -25.911)
31  c/z  25.911  -25.911  0.6350    $ Compact
32  c/z  25.911  -25.911  0.6413    $ Channel

c Shared surfaces
100 c/z  25.337  -25.337  1.5191    $ Graphite holder
200 c/z  25.337  -25.337  1.7856    $ Capsule outer
10  pz   0.0                        $ Bottom (shared)
12  pz   129.54                     $ Top (shared)
```

**Geometric Relationships**:
```python
import math

# Stack centers
s1 = (25.547, -24.553)
s2 = (24.553, -25.547)
s3 = (25.911, -25.911)
capsule = (25.337, -25.337)

# Distance from capsule center to each stack
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

d1 = distance(capsule, s1)  # 0.849 cm
d2 = distance(capsule, s2)  # 0.849 cm
d3 = distance(capsule, s3)  # 0.812 cm

print(f"Stack 1 distance: {d1:.3f} cm")
print(f"Stack 2 distance: {d2:.3f} cm")
print(f"Stack 3 distance: {d3:.3f} cm")

# Verify stacks don't overlap (distance > 2 × R_compact)
d12 = distance(s1, s2)  # 1.405 cm
d23 = distance(s2, s3)  # 1.698 cm
d31 = distance(s3, s1)  # 0.514 cm

min_sep = 2 * 0.6350  # 1.27 cm (compact diameter)
print(f"\nStack separation:")
print(f"1-2: {d12:.3f} cm (min: {min_sep:.3f}) {'✓' if d12 > min_sep else '✗'}")
print(f"2-3: {d23:.3f} cm (min: {min_sep:.3f}) {'✓' if d23 > min_sep else '✗'}")
print(f"3-1: {d31:.3f} cm (min: {min_sep:.3f}) {'✗ WARNING: stacks overlap!'}")
```

**Pattern**: Each stack independently defined, enclosed by common outer boundary.

---

## Common Errors and Fixes

### Error 1: Overlapping Cylinders
**Symptom**: BAD TROUBLE 1000, overlapping cells
**Cause**: Radii not strictly increasing OR different centers

**Example of Error**:
```mcnp
c WRONG - radii not increasing
1  c/z  5 5  1.5    $ R = 1.5
2  c/z  5 5  1.2    $ R = 1.2 < 1.5  ← ERROR
3  c/z  5 5  2.0    $ R = 2.0
```

**Fix**:
```mcnp
c CORRECT - radii strictly increasing
1  c/z  5 5  1.2    $ R = 1.2
2  c/z  5 5  1.5    $ R = 1.5
3  c/z  5 5  2.0    $ R = 2.0
```

### Error 2: Different Centers
**Symptom**: Unexpected geometry, particles lost
**Cause**: C/Z surfaces don't share same center

**Example of Error**:
```mcnp
c WRONG - different centers
1  c/z  5.0  5.0  1.0
2  c/z  5.1  5.0  1.5    $ x = 5.1 ≠ 5.0  ← ERROR
3  c/z  5.0  5.0  2.0
```

**Fix**:
```mcnp
c CORRECT - all same center
1  c/z  5.0  5.0  1.0
2  c/z  5.0  5.0  1.5
3  c/z  5.0  5.0  2.0
```

### Error 3: Lost Particles in Thin Gaps
**Symptom**: "Lost particle" warnings, bad statistics
**Cause**: Gap thickness < 0.01 cm (100 μm) causes tracking precision issues

**Example**:
```mcnp
c Thin gap (0.06 mm = 0.006 cm) - may cause issues
1  c/z  25.337  -25.337  0.6350
2  c/z  25.337  -25.337  0.6356    $ Only 0.06 mm gap  ← RISKY
```

**Fixes**:
1. **Increase gap** (if physically reasonable):
   ```mcnp
   2  c/z  25.337  -25.337  0.6450    $ 1.0 mm gap ✓
   ```

2. **Combine thin regions** (homogenize):
   ```mcnp
   c Combine compact + thin gap into single cell (effective density)
   1  1  -10.7  -2    $ Homogenized compact+gap (weighted density)
   2  c/z  25.337  -25.337  0.6413
   ```

3. **Use importance weighting** (reduce particles in gap):
   ```mcnp
   c Cells
   1  1  -10.9  -1      imp:n=1    $ Compact
   2  0         1  -2   imp:n=0.1  $ Gap (low importance)
   3  2  -1.75  2       imp:n=1    $ Holder
   ```

### Error 4: Missing Axial Bounds
**Symptom**: "Infinite cell" or particles escape
**Cause**: Forgot PZ surfaces for axial extent

**Example of Error**:
```mcnp
c WRONG - no axial bounds
1  1  -10.5  -1    $ Infinite cylinder
```

**Fix**:
```mcnp
c CORRECT - add axial bounds
1  1  -10.5  -1  -10 11    $ Bounded cylinder

10  pz  0.0
11  pz  100.0
```

### Error 5: Wrong Surface Sense
**Symptom**: Void where material expected, or vice versa
**Cause**: Incorrect + or - sign on surface

**Example of Error**:
```mcnp
c WRONG - senses reversed
1  1  -10.5   1  -2    $ Should be -1 (inside surf 1)
2  2  -6.5    2  -3    $ Should be outside surf 1
```

**Fix**:
```mcnp
c CORRECT - proper senses
1  1  -10.5  -1       $ Inside surface 1
2  2  -6.5    1  -2   $ Outside 1, inside 2
3  3  -1.0    2  -3   $ Outside 2, inside 3
```

---

## Volume Calculations

### Spherical Shells

**Formula**:
```
V_shell = (4/3) π (R_outer³ - R_inner³)
```

**Python Function**:
```python
import math

def sphere_shell_volume(r_inner, r_outer):
    """
    Calculate volume of spherical shell in cm³

    Args:
        r_inner: Inner radius (cm)
        r_outer: Outer radius (cm)

    Returns:
        Volume (cm³)
    """
    if r_outer <= r_inner:
        raise ValueError("Outer radius must be > inner radius")

    return (4/3) * math.pi * (r_outer**3 - r_inner**3)

# Example: TRISO buffer layer
v_buffer = sphere_shell_volume(0.0250, 0.0350)
print(f"Buffer volume: {v_buffer:.6e} cm³")  # 1.139e-04
```

### Cylindrical Shells

**Formula**:
```
V_shell = π h (R_outer² - R_inner²)
```

**Python Function**:
```python
import math

def cylinder_shell_volume(r_inner, r_outer, height):
    """
    Calculate volume of cylindrical shell in cm³

    Args:
        r_inner: Inner radius (cm)
        r_outer: Outer radius (cm)
        height: Cylinder height (cm)

    Returns:
        Volume (cm³)
    """
    if r_outer <= r_inner:
        raise ValueError("Outer radius must be > inner radius")

    return math.pi * height * (r_outer**2 - r_inner**2)

# Example: PWR fuel pin gap
v_gap = cylinder_shell_volume(0.4095, 0.4178, 366.0)
print(f"Gap volume: {v_gap:.3f} cm³")  # 3.74
```

### Mass Calculation

**From Volume and Density**:
```python
def mass_from_volume(volume_cm3, density_g_cm3):
    """
    Calculate mass from volume and density

    Args:
        volume_cm3: Volume (cm³)
        density_g_cm3: Density (g/cm³)

    Returns:
        Mass (grams)
    """
    return volume_cm3 * density_g_cm3

# Example: TRISO kernel mass
v_kernel = (4/3) * math.pi * (0.0250**3)  # 6.545e-5 cm³
rho_uo2 = 10.8  # g/cm³
m_kernel = mass_from_volume(v_kernel, rho_uo2)
print(f"Kernel mass: {m_kernel:.6e} g")  # 7.069e-04 g = 0.707 mg
```

---

## Debugging and Validation

### Visual Inspection (MCNP Plotter)

```bash
# Interactive plot
mcnp6 inp=concentric.i ip

# In plotter, use:
origin 25.337 -25.337 64.77    # Center of capsule
extent 5 5 130                  # View range
basis 1 0 0  0 1 0              # XY view (looking down Z)
```

**Expected**: Concentric circles (XY view) or rectangles (XZ/YZ view)

### Numerical Checks

**Python script to verify radii**:
```python
def check_concentric_cylinders(surfaces):
    """
    Verify C/Z surfaces have same center and increasing radii

    Args:
        surfaces: List of tuples (name, cx, cy, r)

    Returns:
        True if valid, False otherwise
    """
    if len(surfaces) < 2:
        return True

    # Check same center
    cx0, cy0 = surfaces[0][1], surfaces[0][2]
    for name, cx, cy, r in surfaces:
        if abs(cx - cx0) > 1e-6 or abs(cy - cy0) > 1e-6:
            print(f"ERROR: {name} has different center ({cx}, {cy}) vs ({cx0}, {cy0})")
            return False

    # Check increasing radii
    radii = [s[3] for s in surfaces]
    if radii != sorted(radii):
        print(f"ERROR: Radii not increasing: {radii}")
        return False

    print(f"✓ All cylinders concentric at ({cx0}, {cy0})")
    print(f"✓ Radii increasing: {radii}")
    return True

# Example: AGR-1 capsule
surfaces = [
    ("Compact", 25.337, -25.337, 0.6350),
    ("Gap",     25.337, -25.337, 0.6413),
    ("Holder",  25.337, -25.337, 1.5191),
    ("Gap2",    25.337, -25.337, 1.5875),
    ("SS",      25.337, -25.337, 1.6218),
    ("Hf",      25.337, -25.337, 1.6472),
    ("Outer",   25.337, -25.337, 1.7856),
]

check_concentric_cylinders(surfaces)
```

### MCNP VOID Check

```mcnp
c Add to data cards to check for voids
void
```

**Interpretation**:
- MCNP floods geometry with particles
- Reports any voids (undefined regions)
- Fix any reported voids before production runs

---

## Advanced Patterns

### Concentric Cylinders with Axial Segmentation

**Example**: Fuel pin with burnup zones

```mcnp
c Cell Cards (9 axial zones × 4 radial regions = 36 cells)
c Zone 1 (bottom)
1   1  -10.5  -1  -10 11   u=10  $ Fuel zone 1
2   0         1  -2  -10 11  u=10  $ Gap zone 1
3   2  -6.5    2  -3  -10 11  u=10  $ Clad zone 1
4   3  -1.0    3      -10 11  u=10  $ Coolant zone 1

c Zone 2
11  1  -10.5  -1  -11 12   u=10  $ Fuel zone 2
12  0         1  -2  -11 12  u=10  $ Gap zone 2
13  2  -6.5    2  -3  -11 12  u=10  $ Clad zone 2
14  3  -1.0    3      -11 12  u=10  $ Coolant zone 2

[... 7 more zones ...]

c Radial surfaces (shared by all zones)
1  cz  0.4095
2  cz  0.4178
3  cz  0.4750

c Axial surfaces (10 planes for 9 zones)
10  pz  0.0
11  pz  40.67
12  pz  81.33
13  pz  122.0
[... etc ...]
```

**Pattern**: Radial surfaces shared, axial surfaces divide into zones

---

## Python Generator Tool

**See**: `scripts/concentric_geometry_generator.py` for automated generation

**Usage**:
```bash
python scripts/concentric_geometry_generator.py \
  --type sphere \
  --radii 0.025 0.035 0.039 0.0425 0.0465 \
  --materials 1 2 3 4 5 6 \
  --densities -10.8 -0.98 -1.85 -3.20 -1.86 -1.75 \
  --universe 100
```

**Output**: Complete MCNP cell and surface cards

---

## Summary

### Quick Reference

**Nested Spheres**:
- Surface type: **SO** (centered) or **S** (positioned)
- Cell pattern: Inner `-1`, shells `J -(J+1)`, outer `N`
- Volume: `(4/3)π(R_outer³ - R_inner³)`

**Nested Cylinders (Centered)**:
- Surface type: **CZ** (on Z-axis)
- Cell pattern: Same as spheres + axial bounds
- Volume: `πh(R_outer² - R_inner²)`

**Nested Cylinders (Off-Axis)**:
- Surface type: **C/Z x y R**
- **Critical**: All C/Z must have same (x, y) center
- Radii strictly increasing
- Share PZ for axial bounds

**Multi-Stack**:
- Each stack: Independent concentric C/Z at its center
- Outer boundary: Common surface (larger radius)
- Filler: Boolean NOT of all stacks

### Common Mistakes
- ❌ Using C/Z with different centers
- ❌ Radii not strictly increasing
- ❌ Forgetting axial bounds (PZ)
- ❌ Thin gaps (< 0.01 cm)
- ❌ Wrong surface sense (+/-)

### Best Practices
- ✅ Use SO/CZ in universes (fastest)
- ✅ Share PZ surfaces across cells
- ✅ Verify radii monotonically increasing
- ✅ Calculate volumes for cross-check
- ✅ Plot geometry before running

---

**See Also**:
- `surface_selection_patterns.md` - When to use SO vs S, CZ vs C/Z
- `reactor_assembly_templates.md` - Complete reactor examples
- `scripts/concentric_geometry_generator.py` - Automated generation

**Version**: 1.0.0 (2025-11-08)
**Part of**: mcnp-geometry-builder skill refinement
