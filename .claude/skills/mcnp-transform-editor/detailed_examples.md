# Detailed TR Card Examples

## Example 1: Multiple Component Placement

### Scenario
Place 6 fuel assemblies in a hexagonal pattern, each at radius 15 cm, separated by 60°.

### Approach
Calculate positions using polar coordinates, create TR card for each position.

### Calculations
```
For assembly i (i = 0 to 5):
  angle_i = i × 60° = i × π/3 rad
  x_i = R × cos(angle_i) = 15 × cos(i × π/3)
  y_i = R × sin(angle_i) = 15 × sin(i × π/3)

Assembly 0 (0°):   x = 15.000, y = 0.000
Assembly 1 (60°):  x = 7.500,  y = 12.990
Assembly 2 (120°): x = -7.500, y = 12.990
Assembly 3 (180°): x = -15.000, y = 0.000
Assembly 4 (240°): x = -7.500, y = -12.990
Assembly 5 (300°): x = 7.500,  y = -12.990
```

### Implementation
```
c Fuel assembly universe (defined elsewhere)
c Universe 1: Single fuel assembly at origin

c Transformation cards for hexagonal placement
*TR1   15.000   0.000  0    $ Assembly 0 (3 o'clock)
*TR2    7.500  12.990  0    $ Assembly 1 (1 o'clock)
*TR3   -7.500  12.990  0    $ Assembly 2 (11 o'clock)
*TR4  -15.000   0.000  0    $ Assembly 3 (9 o'clock)
*TR5   -7.500 -12.990  0    $ Assembly 4 (7 o'clock)
*TR6    7.500 -12.990  0    $ Assembly 5 (5 o'clock)

c Place assemblies using FILL + TRCL
10  0  -100  FILL=1  TRCL=1  IMP:N=1    $ Assembly 0
11  0  -100  FILL=1  TRCL=2  IMP:N=1    $ Assembly 1
12  0  -100  FILL=1  TRCL=3  IMP:N=1    $ Assembly 2
13  0  -100  FILL=1  TRCL=4  IMP:N=1    $ Assembly 3
14  0  -100  FILL=1  TRCL=5  IMP:N=1    $ Assembly 4
15  0  -100  FILL=1  TRCL=6  IMP:N=1    $ Assembly 5

c Surface 100 defines the region for each assembly
100  RCC  0 0 0  0 0 100  8    $ Cylinder for assembly, R=8 cm, H=100 cm
```

### Key Points
- Translation-only transformations (no rotation needed)
- Each assembly placed at calculated position
- Same universe (FILL=1) used for all positions
- Cells use different transformation numbers (TRCL=1 through 6)

---

## Example 2: Detector Array with Rotation

### Scenario
Create 4 detectors around a source, each rotated to "point" toward center.

### Configuration
- Detectors at (±20, ±20, 0) in XY plane
- Each detector oriented with its axis toward origin
- Detector is 5 cm diameter × 10 cm height cylinder

### Approach
1. Define detector universe at origin, oriented along +x axis
2. Create TR cards that translate AND rotate each detector

### Detector Universe Definition
```
c Universe 2: Detector at origin, axis along +x
c Assume detector is in positive x region
1  1  -2.7  -1  U=2  IMP:N=1    $ Detector material (Al)
2  0         1  U=2  IMP:N=0    $ Outside detector

1  RCC  0 0 0  10 0 0  2.5      $ Cylinder: origin, 10 cm along +x, R=2.5
```

### Transformation Calculations

**Detector 1: Position (+20, +20, 0), point toward origin**
```
Translation: (20, 20, 0)
Direction to origin: (-20, -20, 0) → normalize → (-0.707, -0.707, 0)
Detector axis should point this direction

Original axis: +x = (1, 0, 0)
Target axis: (-0.707, -0.707, 0)
Rotation: 135° CCW about z-axis

Rz(135°) = [cos(135°)  -sin(135°)  0]   = [-0.707  -0.707   0]
           [sin(135°)   cos(135°)  0]     [ 0.707  -0.707   0]
           [    0           0      1]     [   0       0     1]
```

**TR card:**
```
*TR1  20 20 0  -0.707 -0.707 0  0.707 -0.707 0  0 0 1
```

**Detector 2: Position (-20, +20, 0)**
```
Translation: (-20, 20, 0)
Target axis: (20, -20, 0) → (0.707, -0.707, 0)
Rotation: 45° CW about z = -45° CCW = 315° CCW

Rz(-45°) = [0.707   0.707  0]
           [-0.707  0.707  0]
           [0       0      1]

*TR2  -20 20 0  0.707 0.707 0  -0.707 0.707 0  0 0 1
```

**Detector 3: Position (-20, -20, 0)**
```
Translation: (-20, -20, 0)
Target axis: (0.707, 0.707, 0)
Rotation: 45° CCW about z

Rz(45°) = [0.707  -0.707  0]
          [0.707   0.707  0]
          [0       0      1]

*TR3  -20 -20 0  0.707 -0.707 0  0.707 0.707 0  0 0 1
```

**Detector 4: Position (+20, -20, 0)**
```
Translation: (20, -20, 0)
Target axis: (-0.707, 0.707, 0)
Rotation: 135° CCW about z

Rz(135°) = [-0.707  -0.707  0]
           [ 0.707  -0.707  0]
           [   0       0    1]

*TR4  20 -20 0  -0.707 -0.707 0  0.707 -0.707 0  0 0 1
```

### Complete Implementation
```
c Detector placement cells
10  0  -10  FILL=2  TRCL=1  IMP:N=1    $ Detector 1 (NE quadrant)
11  0  -11  FILL=2  TRCL=2  IMP:N=1    $ Detector 2 (NW quadrant)
12  0  -12  FILL=2  TRCL=3  IMP:N=1    $ Detector 3 (SW quadrant)
13  0  -13  FILL=2  TRCL=4  IMP:N=1    $ Detector 4 (SE quadrant)

c Bounding cylinders for detector cells
10  RCC  20  20 0  10 0 0  2.5
11  RCC -20  20 0  10 0 0  2.5
12  RCC -20 -20 0  10 0 0  2.5
13  RCC  20 -20 0  10 0 0  2.5
```

### Key Points
- Combined translation + rotation transformations
- Each detector rotated to point toward origin
- TRCL applies transformation to filled universe
- Rotation matrices calculated from desired orientation

---

## Example 3: Layered Shield with Gaps

### Scenario
Create 5-layer shield with varying gap sizes between layers, using transformations to position each layer.

### Configuration
- Layer 1 (innermost): Lead, thickness 5 cm
- Gap 1: 2 cm air
- Layer 2: Steel, thickness 3 cm
- Gap 2: 5 cm air
- Layer 3: Concrete, thickness 10 cm
- Gap 3: 3 cm air
- Layer 4: Polyethylene, thickness 8 cm
- Gap 4: 1 cm air
- Layer 5 (outermost): Aluminum, thickness 2 cm

### Approach
Define each layer as concentric spherical shells using surface transformations.

### Radius Calculations
```
Layer 1 outer: R1 = 50 cm
Gap 1: 2 cm → Layer 2 inner: 52 cm
Layer 2 thickness: 3 cm → Layer 2 outer: 55 cm
Gap 2: 5 cm → Layer 3 inner: 60 cm
Layer 3 thickness: 10 cm → Layer 3 outer: 70 cm
Gap 3: 3 cm → Layer 4 inner: 73 cm
Layer 4 thickness: 8 cm → Layer 4 outer: 81 cm
Gap 4: 1 cm → Layer 5 inner: 82 cm
Layer 5 thickness: 2 cm → Layer 5 outer: 84 cm
```

### Implementation (Without TR Cards)
```
c This case doesn't actually need TR cards
c Shown here to contrast with transformation-based approach

c Surfaces
1   SO  50    $ Layer 1 outer
2   SO  52    $ Layer 2 inner
3   SO  55    $ Layer 2 outer
4   SO  60    $ Layer 3 inner
5   SO  70    $ Layer 3 outer
6   SO  73    $ Layer 4 inner
7   SO  81    $ Layer 4 outer
8   SO  82    $ Layer 5 inner
9   SO  84    $ Layer 5 outer

c Cells
1   1  -11.35   -1        IMP:N=1    $ Layer 1: Lead
2   0            1  -2    IMP:N=1    $ Gap 1: Air (void)
3   2  -7.85     2  -3    IMP:N=1    $ Layer 2: Steel
4   0            3  -4    IMP:N=1    $ Gap 2: Air
5   3  -2.30     4  -5    IMP:N=1    $ Layer 3: Concrete
6   0            5  -6    IMP:N=1    $ Gap 3: Air
7   4  -0.92     6  -7    IMP:N=1    $ Layer 4: Polyethylene
8   0            7  -8    IMP:N=1    $ Gap 4: Air
9   5  -2.70     8  -9    IMP:N=1    $ Layer 5: Aluminum
10  0            9        IMP:N=0    $ Outer void (graveyard)
```

### Alternative: Using TR Cards for Offset Shields
If shields need to be offset from origin or rotated:

```
*TR1  25 0 0    $ Offset entire shield assembly by 25 cm in +x

c Surfaces (defined at origin)
1   1  SO  50
2   1  SO  52
3   1  SO  55
...
9   1  SO  84

c All surfaces use TR1 to shift assembly
```

### Key Points
- Spherical concentric shells don't require TR cards
- TR cards useful when entire assembly needs translation/rotation
- All surfaces can share same TR number for rigid transformation
- Gaps maintained in transformed geometry

---

## Example 4: Beam Port Rotation

### Scenario
Neutron beam port at 30° from horizontal, pointing toward target.

### Configuration
- Beam port: 5 cm diameter, 100 cm length cylindrical void
- Points from position (-150, 0, 0) toward origin
- Elevated 30° above XY plane

### Calculation

**Start and end points:**
```
Start: (-150, 0, 0) + rotation
End: near origin

For 30° elevation:
- XY plane component: cos(30°) = 0.866
- Z component: sin(30°) = 0.5

Start point in rotated frame:
- Distance from origin: 150 cm
- Elevation: 30°
- X: -150 × cos(30°) = -129.9 cm
- Y: 0
- Z: 150 × sin(30°) = 75 cm

Actually, let me reconsider: beam PORT location at (-150, 0, 0), elevated 30°.

Start: (-150, 0, 75)  [elevated 75 cm at x=-150]
Direction toward origin: (150, 0, -75) → normalize → (0.894, 0, -0.447)
```

### Define Beam Port at Origin Along +X
```
c Universe 3: Beam port along +x axis
1  0  -1  U=3  IMP:N=1    $ Void cylinder for beam

1  RCC  0 0 0  100 0 0  2.5    $ Cylinder along +x, R=2.5 cm, L=100 cm
```

### Transformation to Final Position

**Translation:** Start point = (-150, 0, 75)

**Rotation:** Align +x axis with direction (0.894, 0, -0.447)

This is rotation in XZ plane. The new x-axis is (0.894, 0, -0.447).

For a rotation that takes (1,0,0) → (0.894, 0, -0.447):
```
Rotation about y-axis by -30° (or 330°):

Ry(-30°) = [ cos(-30°)  0  sin(-30°)]   = [ 0.866  0  -0.5]
           [     0      1      0     ]     [   0    1    0 ]
           [-sin(-30°)  0  cos(-30°)]     [ 0.5    0   0.866]

Wait, let me verify:
[0.866  0  -0.5] × [1]   = [0.866]
[  0    1    0 ]   [0]     [  0  ]
[0.5    0  0.866]   [0]     [0.5  ]

This gives (0.866, 0, 0.5), but we want (0.894, 0, -0.447).

Let me recalculate. Direction toward origin from (-150, 0, 75):
(150, 0, -75) → normalize: √(150² + 75²) = √(22500 + 5625) = √28125 = 167.7
(150/167.7, 0, -75/167.7) = (0.894, 0, -0.447) ✓

For Ry(θ) to map (1,0,0) → (0.894, 0, -0.447):
cos(θ) = 0.894 → θ = -26.57° (since z-component is negative)

Actually: (0.894, 0, -0.447) suggests  arctan(-0.447/0.894) = arctan(-0.5) ≈ -26.57°

So rotation about y-axis by approximately -26.57° or let's use -30° for simplicity.
```

Wait, let me use the exact angle. If direction is (0.894, 0, -0.447), and we want to rotate (1,0,0) to this:

```
Angle = atan2(-0.447, 0.894) = atan(-0.5) = -26.565°

But in the problem statement, elevation is 30°. Let me redefine.

Actually, "elevated 30° above XY plane" means the beam makes 30° angle with XY plane.
If beam points from (-150, 0, h) toward (0, 0, 0):
tan(30°) = h/150
h = 150 × tan(30°) = 150 × 0.577 = 86.6 cm

So start point: (-150, 0, 86.6)
Direction: (150, 0, -86.6) → normalize: (0.866, 0, -0.5)

Rotation angle: -30° about y-axis

Ry(-30°) = [ 0.866  0  -0.5]
           [   0    1    0 ]
           [ 0.5    0  0.866]

Verification:
[0.866  0  -0.5] × [1]   = [0.866]
[  0    1    0 ]   [0]     [  0  ]
[0.5    0  0.866]   [0]     [0.5  ]

This gives (0.866, 0, 0.5), but we want (0.866, 0, -0.5). Need +30° rotation!

Ry(+30°) = [ 0.866  0   0.5]
           [   0    1    0 ]
           [-0.5    0  0.866]

Check:
[0.866  0   0.5] × [1]   = [0.866]
[  0    1    0 ]   [0]     [  0  ]
[-0.5    0  0.866]   [0]     [-0.5 ]

Perfect! (0.866, 0, -0.5) ✓
```

### TR Card
```
*TR1  -150 0 86.6  0.866 0 0.5  0 1 0  -0.5 0 0.866
```

### Complete Implementation
```
c Beam port cell
10  0  -10  FILL=3  TRCL=1  IMP:N=1

c Bounding surface
10  RCC  -150 0 86.6  86.6 0 -50  2.5    $ Approx cylinder along beam direction
```

### Key Points
- Combined translation to start point + rotation to align axis
- Rotation calculated from desired beam direction
- TRCL applies transformation to beam port universe

---

## Example 5: Symmetric Components via Reflection

### Scenario
Create 4 symmetric detector banks using reflections.

### Configuration
- Original detector bank in +X, +Y quadrant
- Mirror across XZ plane → +X, -Y quadrant
- Mirror across YZ plane → -X, +Y quadrant
- Mirror across both → -X, -Y quadrant

### Original Detector Bank Universe
```
c Universe 4: Detector bank at (+10, +10, 0)
c (Detailed geometry omitted for brevity)
```

### Transformation Cards

**Original (no transformation needed):**
```
10  0  -10  FILL=4  IMP:N=1    $ +X, +Y quadrant (no TRCL)
```

**Mirror across XZ plane (y → -y):**
```
*TR1  0 0 0  1 0 0  0 -1 0  0 0 1
11  0  -11  FILL=4  TRCL=1  IMP:N=1    $ +X, -Y quadrant
```

**Mirror across YZ plane (x → -x):**
```
*TR2  0 0 0  -1 0 0  0 1 0  0 0 1
12  0  -12  FILL=4  TRCL=2  IMP:N=1    $ -X, +Y quadrant
```

**Mirror across both (x → -x, y → -y):**
```
*TR3  0 0 0  -1 0 0  0 -1 0  0 0 1
13  0  -13  FILL=4  TRCL=3  IMP:N=1    $ -X, -Y quadrant
```

### Key Points
- Reflections use determinant = -1 matrices
- Original universe appears in 4 positions via mirroring
- MCNP handles reflections correctly for particle transport
- Efficient way to create symmetric geometry

### Note on Reflections
Reflections are improper rotations. Verify that the geometry makes physical sense when mirrored (e.g.,螺 螺旋structures may not mirror correctly).

---

## Example 6: Transformation Composition for Complex Placement

### Scenario
Place component that requires: (1) Rotate 45° about its own axis, (2) Move to position (30, 0, 0), (3) Rotate entire assembly 90° about Z-axis.

### Approach
Compose three transformations: TR1 ∘ TR2 ∘ TR3

### Individual Transformations

**TR_local:** Rotate component 45° about its own Z-axis
```
R1 = Rz(45°) = [0.707  -0.707  0]
               [0.707   0.707  0]
               [  0       0    1]
d1 = (0, 0, 0)
```

**TR_translate:** Move to (30, 0, 0)
```
R2 = I
d2 = (30, 0, 0)
```

**TR_global:** Rotate entire assembly 90° about Z
```
R3 = Rz(90°) = [0  -1  0]
               [1   0  0]
               [0   0  1]
d3 = (0, 0, 0)
```

### Composition Calculation

**Step 1:** TR_translate ∘ TR_local
```
R12 = R2 · R1 = I · R1 = R1
d12 = d2 + R2·d1 = (30, 0, 0) + 0 = (30, 0, 0)
```

**Step 2:** TR_global ∘ TR12
```
R_final = R3 · R12 = Rz(90°) · Rz(45°)

= [0  -1  0] · [0.707  -0.707  0]
  [1   0  0]   [0.707   0.707  0]
  [0   0  1]   [  0       0    1]

= [0·0.707 + (-1)·0.707 + 0·0    0·(-0.707) + (-1)·0.707 + 0·0    0]
  [1·0.707 +   0·0.707 + 0·0    1·(-0.707) +   0·0.707 + 0·0    0]
  [  0·0.707 +   0·0.707 + 1·0      0·(-0.707) +   0·0.707 + 1·0    1]

= [-0.707   -0.707   0]
  [ 0.707   -0.707   0]
  [   0        0     1]

d_final = d3 + R3·d12 = (0,0,0) + [0  -1  0]·[30]   = [ 0]
                                   [1   0  0] [ 0]     [30]
                                   [0   0  1] [ 0]     [ 0]
```

### Final TR Card
```
*TR1  0 30 0  -0.707 -0.707 0  0.707 -0.707 0  0 0 1
```

### Implementation
```
10  0  -10  FILL=5  TRCL=1  IMP:N=1
```

### Verification
Use scripts/tr_composition.py to verify composition calculation.

### Key Points
- Complex transformations composed from simpler ones
- Matrix multiplication order: right to left (last applied first in reading order)
- Translation composition includes rotation: d_final = d3 + R3·(d2 + R2·d1)
- Validate final matrix with tr_matrix_validator.py
