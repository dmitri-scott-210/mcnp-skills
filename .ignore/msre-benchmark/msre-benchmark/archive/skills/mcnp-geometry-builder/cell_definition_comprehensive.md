# MCNP Cell Card Definition - Comprehensive Reference

Cell cards define the geometric regions in MCNP and assign physical properties (material, density) to each region. Cells are the fundamental building blocks where particles transport and interact.

## Cell Card Format

**Format:** `j  m  d  geom  params`

**Fields:**
- `j`: Cell number (1-99,999,999, unique)
- `m`: Material number (references M card, 0 for void)
- `d`: Density specification
- `geom`: Geometry description (Boolean expression of surfaces)
- `params`: Optional cell parameters (IMP, VOL, U, TRCL, etc.)

**Example:**
```
1    1  -10.5  -1 2 -3  IMP:N=1  VOL=100.0  $ Fuel region
```

---

## Cell Number (j)

**Valid range:** 1-99,999,999

**Requirements:**
- Must be unique across all cells
- Positive integers only
- No gaps required (can skip numbers)

**Organizational Schemes:**

**Scheme 1: Sequential by region**
```
1-99:    Core regions
100-199: Reflector
200-299: Shield
300-399: Detector regions
9999:    Graveyard (common convention)
```

**Scheme 2: Hierarchical (reactor)**
```
1000s: Pin level (1001-1050)
2000s: Assembly level (2001-2010)
3000s: Core level (3001-3005)
9999:  External void
```

**Best Practices:**
- Use consistent numbering scheme throughout model
- Reserve high numbers (9000+) for boundary/graveyard cells
- Document numbering scheme in comments
- Leave gaps for future expansion

---

## Material Number (m)

**Valid values:**
- Positive integer (1-99,999,999): References material M card
- Zero (0): Void cell (no material, no interactions except geometry)

**Material Reference:**
```
Cell card:    1  1  -10.5  -1  IMP:N=1    $ Material 1
Data block:   M1  92235  0.9  92238  0.1  $ Material definition
```

**Void Cells:**
```
2  0        1  IMP:N=0                    $ Graveyard (terminates particles)
3  0       -2 #1  IMP:N=1                 $ Void region (particles pass through)
```

**Common Patterns:**
- M1: Fuel
- M2: Cladding
- M3: Coolant/moderator
- M4: Structural material
- M5: Absorber
- M0: Void (for cells with m=0, no M0 card needed)

**Cross-Reference Check:**
- Every non-zero material number in cell cards MUST have corresponding M card
- M card can exist without being used in cells (warning, but not error)

---

## Density Specification (d)

**Three forms:**

### 1. Positive Density: Atomic Density
**Units:** atoms/barn-cm

**Example:**
```
1  1  0.08  -1  IMP:N=1    $ 0.08 atoms/barn-cm
```

**Use when:**
- Working with pure elements or isotopes
- Matching cross-section benchmark specifications
- Direct from cross-section libraries

### 2. Negative Density: Mass Density
**Units:** g/cm³ (absolute value)

**Example:**
```
1  1  -10.5  -1  IMP:N=1    $ 10.5 g/cm³
```

**Use when:**
- More intuitive for engineering (common convention)
- Material specifications give mass density
- **Most common in practice**

**Conversion:**
Atomic density (atoms/barn-cm) = (mass density × Avogadro) / (atomic weight)

### 3. Zero Density: Void
**Must have m=0:**

**Example:**
```
2  0  -1  IMP:N=0    $ Graveyard (density omitted or zero)
```

**Note:** For void cells (m=0), density is typically omitted entirely

---

## Geometry Description (geom)

The geometry field uses Boolean operations to combine surfaces. This creates the region where the cell exists.

**Format:** Surface numbers with operators (space, :, #, parentheses)

**See:** `boolean_operations_guide.md` for comprehensive Boolean logic

**Quick examples:**
```
-1              $ Inside surface 1
-1 2            $ Inside surf 1 AND outside surf 2
-1 : -2         $ Inside surf 1 OR inside surf 2
-1 2 -3         $ Inside 1, outside 2, inside 3 (intersection)
(-1 2) : (-3 4) $ Union of two intersections
#10             $ Complement of cell 10 (all space not in cell 10)
```

**Surface Sense:**
- Negative number (-n): Negative side of surface (typically "inside")
- Positive number (+n or n): Positive side of surface (typically "outside")

**Determining surface sense:**
- Check surface equation: f(x,y,z) - D = 0
- If f(x,y,z) < 0: negative side
- If f(x,y,z) > 0: positive side
- Test with specific point or use geometry plotter

---

## Cell Parameters (params)

Optional parameters specified after geometry. Can be on cell card or in data block (but NOT both for same parameter).

**Common parameters:**
- `IMP:N=1` - Neutron importance (variance reduction)
- `VOL=100.0` - Volume (cm³)
- `U=1` - Universe number (for FILL/LAT)
- `TRCL=5` - Transformation (rotation/translation)
- `LAT=1` - Lattice type (1=rectangular, 2=hexagonal)
- `FILL=1` - Fill with universe 1
- `TMP=2.53e-8` - Temperature (MeV)

**See:** `cell_parameters_reference.md` for complete list of all 18 parameters

---

## LIKE n BUT Feature

**Purpose:** Cell inheritance - create new cell by copying another and changing specific fields

**Format:** `j  LIKE n  BUT  field=value  field=value  ...`

**Changeable fields:**
- `MAT=m` - Change material
- `RHO=d` - Change density
- Cell parameters (IMP, VOL, U, etc.)

**Example:**
```
1  1  -10.5  -1  IMP:N=1  VOL=100.0     $ Original cell
2  LIKE 1 BUT  MAT=2  RHO=-8.0          $ Copy cell 1, change material and density
3  LIKE 1 BUT  IMP:N=2                  $ Copy cell 1, change importance only
```

**Restrictions:**
- Cannot change cell number (j)
- Cannot change geometry (geom field)
- New cell inherits all parameters from original unless overridden

**Use Cases:**
- Similar cells with different materials (fuel assemblies with varying enrichment)
- Importance regions with same geometry
- Repeated structures with parameter variations

---

## Material/Void Combinations

### Void Cell (m=0, no material)

**Graveyard (IMP=0):**
```
9999  0      1  IMP:N=0    $ Particle termination boundary
```
- Particles entering are killed (no longer tracked)
- Must surround entire problem geometry
- Typically outermost cell

**Void region (IMP>0):**
```
10  0  -5 6 #20 #30  IMP:N=1    $ Void between components
```
- Particles pass through (no interactions)
- Geometry still tracked
- Use for air gaps, vacuum, space between components

### VOID Card vs m=0

**VOID card (data block):**
```
VOID  10  20  30    $ Treat cells 10, 20, 30 as voids for geometry testing
```
- Temporary debugging tool
- Used with external source flood testing
- Finds gaps/overlaps before expensive simulation
- Does NOT change cell material permanently

**m=0 (cell card):**
- Permanent void assignment
- Part of normal problem definition
- Can have importance (IMP) assigned

---

## Cross-References

### Cell → Surface
Every surface number in geometry field MUST be defined in surface card block.

**Error example:**
```
1  1  -10.5  -1 2 -3  IMP:N=1    $ Cell references surfaces 1, 2, 3
c Surface card block:
1  SO  10.0                       $ Surface 1 defined
2  PZ  0.0                        $ Surface 2 defined
c ERROR: Surface 3 not defined!
```

### Cell → Material
Every non-zero material number (m) MUST have corresponding M card in data block.

**Error example:**
```
1  1  -10.5  -1  IMP:N=1          $ Cell uses material 1
c Data block:
MODE N
M2  1001  2  8016  1              $ ERROR: M1 not defined, only M2
```

### Cell → Transformation
TRCL parameter must reference existing *TR card or use inline matrix.

**Correct examples:**
```
*TR5  10 0 0  1 0 0  0 1 0  0 0 1    $ Transformation definition
1  1  -10.5  -1  TRCL=5              $ References TR5

2  1  -10.5  -2  TRCL=(10 0 0  1 0 0  0 1 0  0 0 1)  $ Inline transformation
```

### Cell → Universe
U parameter specifies universe, FILL parameter fills with universe.

**Example:**
```
1  1  -10.5  -1  U=1  IMP:N=1       $ Cell in universe 1
2  0  -2  FILL=1  IMP:N=1           $ Cell filled with universe 1
```

---

## 10 Progressively Complex Examples

### Example 1: Simple sphere (basic)
```
1  1  -10.5  -1  IMP:N=1           $ Inside sphere
2  0         1   IMP:N=0           $ Outside sphere (graveyard)

1  SO  10.0                         $ Sphere radius 10 cm
```

### Example 2: Spherical shell (intersection)
```
1  1  -10.5  -1 2  IMP:N=1         $ Inside surf 2, outside surf 1
2  0         -2 1  IMP:N=0         $ Inside surf 1, graveyard
3  0          2    IMP:N=0         $ Outside surf 2, graveyard

1  SO  8.0                          $ Inner sphere
2  SO  10.0                         $ Outer sphere
```

### Example 3: Multiple shells (repeated pattern)
```
1  1  -10.0  -1     IMP:N=1  $ Innermost region
2  2  -8.0    1 -2  IMP:N=1  $ First shell
3  3  -6.0    2 -3  IMP:N=1  $ Second shell
4  0          3     IMP:N=0  $ Graveyard

1  SO  5.0
2  SO  8.0
3  SO  10.0
```

### Example 4: Cylinder with end caps (three surfaces)
```
1  1  -10.0  -1 -2 3  IMP:N=1     $ Inside cylinder, between end caps
2  0          1:2:-3  IMP:N=0     $ Outside (union of three regions)

1  CZ  5.0                         $ Cylinder radius
2  PZ  0.0                         $ Bottom end cap
3  PZ  100.0                       $ Top end cap
```

### Example 5: Fuel pin (four regions)
```
c Four-region fuel pin (fuel, gap, clad, coolant)
1  1  -10.5  -1       IMP:N=1  $ Fuel
2  0         1 -2     IMP:N=1  $ Gap (void)
3  2  -6.5    2 -3    IMP:N=1  $ Cladding
4  3  -1.0    3 -4 -5 6  IMP:N=1  $ Coolant (finite height)
5  0          4:5:-6  IMP:N=0  $ Graveyard

1  CZ  0.4095                    $ Fuel outer radius
2  CZ  0.4180                    $ Gap outer radius
3  CZ  0.4750                    $ Clad outer radius
4  CZ  0.6500                    $ Pin cell boundary
5  PZ  0.0                       $ Bottom
6  PZ  365.76                    $ Top (active height)
```

### Example 6: Box with cylindrical hole (complement)
```
c Rectangular block with cylindrical hole through center
1  1  -10.0  -1 2 -3 4 -5 6 #10  IMP:N=1  $ Box minus cylinder
2  0         -10               IMP:N=1  $ Cylinder (void)
3  0          1:-2:3:-4:5:-6   IMP:N=0  $ Graveyard

c Surfaces
1  PX  -10.0                     $ Box boundaries
2  PX   10.0
3  PY  -10.0
4  PY   10.0
5  PZ  -20.0
6  PZ   20.0

c Cell 10 (referenced by complement in cell 1)
10  0  -7 -5 6  IMP:N=1  $ Cylinder void

7  CZ  3.0                       $ Cylinder radius
```

### Example 7: Union of two spheres
```
c Two overlapping spheres, material fills union
1  1  -10.0  -1 : -2  IMP:N=1   $ Inside sphere 1 OR inside sphere 2
2  0          1 2     IMP:N=0   $ Outside both spheres

1  S  -5 0 0  8.0                $ Sphere at (-5, 0, 0), R=8
2  S   5 0 0  8.0                $ Sphere at ( 5, 0, 0), R=8
```

### Example 8: Complex Boolean expression
```
c Demonstrates order of operations
1  1  -10.0  (-1 2 : -3 4) (5 : 6)  IMP:N=1
c            ^^^^^^^^^^^ ^^^^^^^^^
c            Union 1     Intersect with Union 2
2  0         1:-2:-3:-4:-5:-6      IMP:N=0

c Interpretation: (Intersect1 OR Intersect2) AND (Union of 5,6)
```

### Example 9: Using LIKE n BUT
```
c Pin lattice with varying enrichments
1  1  -10.41  -1  U=1  IMP:N=1     $ Pin universe (4.5% enrichment)
2  2  -6.5     1 -2  U=1  IMP:N=1  $ Clad
3  3  -1.0     2 -3  U=1  IMP:1    $ Water

c Create 3.5% enrichment pin by copying
4  LIKE 1 BUT  U=2  RHO=-10.15     $ Lower enrichment, new universe
5  LIKE 2 BUT  U=2                 $ Same clad
6  LIKE 3 BUT  U=2                 $ Same water

1  CZ  0.4095
2  CZ  0.4750
3  CZ  0.6500
```

### Example 10: Lattice cell with transformation
```
c Pin universe defined in local coordinates
1  1  -10.5  -1  U=1  IMP:N=1     $ Pin in universe 1

c Lattice cell using pin universe
2  0  -2 -3 4  LAT=1  U=2  FILL=1  IMP:N=1  $ 3x3 array

c Assembly cell with transformation
3  0  -5  FILL=2  TRCL=10  IMP:N=1  $ Rotate assembly 90 degrees

1  CZ  0.5                          $ Pin radius
2  PX  -1.5                         $ Lattice boundaries
3  PX   1.5
4  PY  -1.5                         $ (3 cells × 1 cm pitch)

5  RPP  -10 10  -10 10  0 100      $ Assembly boundary

*TR10  0 0 0  0 1 0  -1 0 0  0 0 1  $ 90° rotation about z
```

---

## Common Mistakes and Fixes

**Mistake 1: Undefined surface**
```
1  1  -10.5  -1 2 -3  IMP:N=1    $ ERROR: Surface 3 not defined
```
**Fix:** Define all surfaces in surface block

**Mistake 2: Material number mismatch**
```
1  1  -10.5  -1  IMP:N=1         $ Uses material 1
M2  1001  2  8016  1             $ ERROR: Only M2 defined
```
**Fix:** Define M1 or change cell to use m=2

**Mistake 3: Wrong density sign**
```
1  1  10.5  -1  IMP:N=1          $ Positive mass density (atomic interpreted)
```
**Fix:** Use -10.5 for mass density

**Mistake 4: Void cell with density**
```
1  0  -1.0  -1  IMP:N=1          $ ERROR: Void with density
```
**Fix:** Omit density for void cells: `1  0  -1  IMP:N=1`

**Mistake 5: Graveyard without IMP:N=0**
```
9999  0  1  IMP:N=1              $ ERROR: Should terminate particles
```
**Fix:** Use IMP:N=0 for graveyard

**Mistake 6: Duplicate cell numbers**
```
1  1  -10.5  -1  IMP:N=1
1  2  -8.0   -2  IMP:N=1         $ ERROR: Cell 1 defined twice
```
**Fix:** Use unique cell numbers

**Mistake 7: LIKE n BUT with non-existent cell**
```
2  LIKE 10 BUT MAT=2             $ ERROR: Cell 10 doesn't exist
```
**Fix:** Reference existing cell number

**Mistake 8: Missing IMP parameter**
```
1  1  -10.5  -1                  $ WARNING: No importance (defaults to 1)
```
**Fix:** Always explicitly specify IMP:N (or other particles)

---

**References:**
- MCNP6 User Manual, Chapter 5.02: Cell Cards
- See also: boolean_operations_guide.md for geometry field details
- See also: cell_parameters_reference.md for complete parameter list
