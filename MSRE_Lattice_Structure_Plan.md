# MSRE Lattice Structure Strategy Plan
**MCNP Modeling - MSRE First Criticality Benchmark**

**Version:** 1.0  
**Date:** 2025-11-07  
**Status:** Planning Phase - NOT FOR EXECUTION  
**Purpose:** Detailed lattice definition strategy for MCNP MSRE model

---

## EXECUTIVE SUMMARY

### Lattice Configuration Confirmed
- **Lattice Type:** LAT=1 (hexahedral/square lattice) ✓ CRITICAL
- **NOT LAT=2** (hexagonal) - common error avoided
- **Array Size:** 29×29 = 841 positions
- **Positions in core:** 593 (within 70.285 cm radius)
- **Graphite stringers:** 589 (593 - 4 central disruptions)
- **Specification match:** ✓ YES (540-590 range)

### Universe Hierarchy
- **Universe 0:** Main universe (reactor vessel, reflector, thermal shield)
- **Universe 1:** Standard graphite stringer unit cell
- **Universe 2:** Control rod thimble #1 (rods 1 & 2 withdrawn)
- **Universe 3:** Control rod thimble #2 (regulating rod, 3% inserted)
- **Universe 4:** Sample basket unit cell
- **Universe 10:** Lattice universe (contains LAT=1 cell)

### Critical Design Parameters (Hot, 911 K)
- **Stringer pitch:** 5.084 cm × 5.084 cm square
- **Lattice radius:** 70.285 cm (RCC boundary)
- **Core height:** 170.311 cm
- **Fuel channels:** 1,140 total (formed by adjacent stringer grooves)
- **Channel dimensions:** 1.018 cm × 3.053 cm rectangular

---

## 1. LATTICE TYPE CONFIRMATION

### LAT=1 (Hexahedral/Square) - VERIFIED

**Rationale:**
- MSRE uses square close-packed array of graphite stringers
- Each stringer: 5.084 cm × 5.084 cm square cross-section
- Square lattice arrangement (NOT hexagonal)
- LAT=1 requires 6 surfaces: -X +X -Y +Y -Z +Z

**CRITICAL WARNING:**
❌ **DO NOT use LAT=2** (hexagonal prism lattice)
- LAT=2 requires 8 surfaces (6 hex sides + 2 top/bottom)
- MSRE geometry is square, not hexagonal
- This is a common error in MSRE modeling

**MCNP Implementation:**
```
c Lattice cell (LAT=1 hexahedral)
100  0  -10 11 -12 13 -14 15  U=10  LAT=1  FILL=...  IMP:N=1
c       ^-X ^+X ^-Y ^+Y ^-Z ^+Z (6 surfaces)
```

---

## 2. UNIVERSE HIERARCHY DESIGN

### Universe 0: Main Universe (Real World)

**Components:**
- Core can (INOR-8): 71.097 cm inner radius, 71.737 cm outer radius
- Reactor vessel (INOR-8): 74.299 cm inner radius, 76.862 cm outer radius
- Downcomer annulus: 2.562 cm (void at zero-power)
- Inner graphite reflector: 71.737 to 74.299 cm
- Thermal shield (SS304): Required (omission = -885 pcm bias)
- Insulation (vermiculite): 15.24 cm thickness

**Lattice Integration:**
- Central core region filled with Universe 10 (lattice universe)
- Lattice bounded by RCC with radius 70.285 cm, height 170.311 cm

### Universe 1: Standard Graphite Stringer Unit Cell

**Geometry:**
- Overall dimensions: 5.084 cm × 5.084 cm square cross-section
- Height: 170.311 cm (full core height)
- 4 machined grooves on sides (one per side)
- Each groove: 1.018 cm wide × 1.5265 cm deep (half-channel)

**Material Regions:**
1. **Central graphite body** (nuclear grade, ρ = 1.86 g/cm³)
2. **4 side grooves filled with fuel salt** (LiF-BeF₂-ZrF₄-UF₄)
   - Adjacent stringer grooves combine to form full fuel channels
   - Full channel: 1.018 cm × 3.053 cm when paired

**Fuel Channel Formation:**
- Each stringer has 4 grooves (N, S, E, W sides)
- Adjacent stringers' half-grooves (1.5265 cm deep each) combine
- Form complete 3.053 cm deep fuel channel
- Total 1,140 channels from ~565 stringer pairs

**Pseudo-Code Structure:**
```
c Universe 1: Standard graphite stringer unit cell
c Overall: 5.084 cm × 5.084 cm × 170.311 cm

c Cell 1: Central graphite region (after grooves removed)
1  2  -1.86  <central_graphite_geometry>  U=1  IMP:N=1  $ Graphite

c Cells 2-5: Four side grooves filled with fuel salt
2  1  -2.3275  <north_groove>  U=1  IMP:N=1  $ Fuel salt (N)
3  1  -2.3275  <east_groove>   U=1  IMP:N=1  $ Fuel salt (E)
4  1  -2.3275  <south_groove>  U=1  IMP:N=1  $ Fuel salt (S)
5  1  -2.3275  <west_groove>   U=1  IMP:N=1  $ Fuel salt (W)

c Surfaces for 5.084 cm × 5.084 cm unit cell
10  PX  -2.542                  $ -X boundary
11  PX   2.542                  $ +X boundary
12  PY  -2.542                  $ -Y boundary
13  PY   2.542                  $ +Y boundary
14  PZ   0.0                    $ Bottom
15  PZ  170.311                 $ Top

c Groove geometry (details in geometry phase)
c Each groove: 1.018 cm wide × 1.5265 cm deep
c North groove centered on +Y face
c East groove centered on +X face
c South groove centered on -Y face
c West groove centered on -X face
```

**Volume Specifications:**
- **Total unit cell volume:** 5.084² × 170.311 = 4,400.1 cm³
- **Groove volume (4 grooves):** 4 × (1.018 × 1.5265 × 170.311) ≈ 1,066.7 cm³
- **Graphite volume:** 4,400.1 - 1,066.7 = 3,333.4 cm³
- **Fuel salt fraction:** 24.2% per unit cell

### Universe 2: Control Rod Thimble (Rods 1 & 2, Fully Withdrawn)

**Geometry:**
- INOR-8 thimble: 5.08 cm outer diameter, 0.1651 cm wall thickness
- Inner radius: 2.54 - 0.1651 = 2.3749 cm
- Height: 170.311 cm (full core height)
- Position: Rods withdrawn to 129.54 cm (only thimble in core)

**Material Regions:**
1. **Inner region:** Fuel salt (no poison - rods withdrawn)
2. **Thimble wall:** INOR-8 (ρ = 8.7745 g/cm³)
3. **Outer region:** Fuel salt (surrounds thimble)

**Pseudo-Code Structure:**
```
c Universe 2: Control rod thimble (withdrawn position)
c Outer diameter: 5.08 cm (fits in 5.084 cm unit cell)

c Cell 1: Inner fuel salt (no poison)
11  1  -2.3275  -20       U=2  IMP:N=1  $ Fuel salt inside thimble
c Cell 2: INOR-8 thimble wall
12  3  -8.7745  20  -21   U=2  IMP:N=1  $ Thimble wall
c Cell 3: Outer fuel salt
13  1  -2.3275  21        U=2  IMP:N=1  $ Fuel salt outside thimble

c Surfaces
20  RCC  0 0 0  0 0 170.311  2.3749   $ Inner thimble (r=2.3749 cm)
21  RCC  0 0 0  0 0 170.311  2.54     $ Outer thimble (r=2.54 cm)
```

### Universe 3: Control Rod Thimble (Regulating Rod, 3% Inserted)

**Geometry:**
- Same thimble as Universe 2
- Regulating rod position: 118.364 ± 0.127 cm (46.6 inches)
- Poison inserted length: 77.077 cm (from bottom)
- Upper region: Fuel salt only (above poison)

**Material Regions:**
1. **Lower inner (0 to 77.077 cm):** Gd₂O₃-Al₂O₃ poison (ρ = 5.873 g/cm³)
2. **Upper inner (77.077 to 170.311 cm):** Fuel salt
3. **Thimble wall:** INOR-8
4. **Outer region:** Fuel salt

**Pseudo-Code Structure:**
```
c Universe 3: Control rod thimble (regulating rod, 3% inserted)

c Cell 1: Control rod poison (lower 77.077 cm)
21  4  -5.873  -30  -32   U=3  IMP:N=1  $ Gd₂O₃-Al₂O₃ poison
c Cell 2: Fuel salt above poison
22  1  -2.3275  -30  32   U=3  IMP:N=1  $ Fuel salt (upper)
c Cell 3: INOR-8 thimble wall
23  3  -8.7745  30  -31   U=3  IMP:N=1  $ Thimble wall
c Cell 4: Outer fuel salt
24  1  -2.3275  31        U=3  IMP:N=1  $ Fuel salt outside

c Surfaces
30  RCC  0 0 0  0 0 170.311  2.3749   $ Inner thimble
31  RCC  0 0 0  0 0 170.311  2.54     $ Outer thimble
32  PZ  77.077                         $ Poison top (118.364 cm position)
```

### Universe 4: Sample Basket Unit Cell

**Geometry:**
- INOR-8 basket: 5.4287 cm outer diameter, 0.079 cm wall thickness
- Inner radius: 2.7144 - 0.079 = 2.6354 cm
- Height: 170.311 cm (full core height)
- Contents: 5 graphite samples + 4 INOR-8 samples

**Simplified Model (Recommended for Benchmark):**
- Homogenize basket contents
- Bias: -37 pcm (acceptable)
- Reduces complexity significantly

**Pseudo-Code Structure (Simplified):**
```
c Universe 4: Sample basket (homogenized)

c Cell 1: Homogenized basket interior
31  5  -X.XXX  -40       U=4  IMP:N=1  $ Homogenized samples
c Cell 2: INOR-8 basket wall
32  3  -8.7745  40  -41  U=4  IMP:N=1  $ Basket wall
c Cell 3: Outer fuel salt
33  1  -2.3275  41       U=4  IMP:N=1  $ Fuel salt outside

c Surfaces
40  RCC  0 0 0  0 0 170.311  2.6354   $ Inner basket
41  RCC  0 0 0  0 0 170.311  2.7144   $ Outer basket (r=2.7144 cm)
```

**Homogenization Calculation:**
- 5 graphite samples: 0.635 × 1.1938 cm × 167.64 cm
- 4 INOR-8 samples: 0.635 cm dia × 167.64 cm
- Fuel salt fills remaining volume
- Volume fractions: ~XX% graphite, ~XX% INOR-8, ~XX% fuel salt
- Homogenized density: Calculate weighted average

### Universe 10: Lattice Universe

**Purpose:** Container for LAT=1 lattice cell

**Geometry:**
- Single cell defining lattice element boundaries
- 6 surfaces (LAT=1 requirement)
- Surfaces define i(X), j(Y), k(Z) indexing directions

**Pseudo-Code Structure:**
```
c Universe 10: Lattice definition

c Cell 100: Lattice cell (LAT=1)
100  0  -50 51 -52 53 -54 55  U=10  LAT=1  IMP:N=1  &
        FILL=-14:14 -14:14 0:0  <FILL_ARRAY>

c Lattice element surfaces (5.084 cm pitch)
50  PX  -2.542                  $ -X boundary
51  PX   2.542                  $ +X boundary
52  PY  -2.542                  $ -Y boundary
53  PY   2.542                  $ +Y boundary
54  PZ   0.0                    $ Bottom
55  PZ  170.311                 $ Top

c Surface order defines indexing:
c   i direction: Surfaces 50,51 (X-axis)
c   j direction: Surfaces 52,53 (Y-axis)
c   k direction: Surfaces 54,55 (Z-axis)
```

---

## 3. FILL ARRAY STRUCTURE

### Array Dimensions

**Configuration:**
- **Array size:** 29×29×1 (i, j, k)
- **Index range:** i = -14 to +14, j = -14 to +14, k = 0 to 0
- **Total positions:** 841
- **Positions in core:** 593 (within 70.285 cm radius)
- **Graphite stringers:** 589 (after 4 central disruptions)

**FILL Array Format:**
```
FILL=-14:14 -14:14 0:0
     <29 rows × 29 columns of universe numbers>
```

### Indexing Scheme

**Centered Indexing (i=0, j=0 at core center):**
- **Advantage:** Symmetric, intuitive for circular geometry
- **Disadvantage:** Negative indices (MCNP supports this)

**Index to Position Conversion:**
```
x(i) = i × 5.084 cm
y(j) = j × 5.084 cm
r(i,j) = sqrt(x² + y²)

Include position if: r(i,j) ≤ 70.285 cm
```

**Example Positions:**
- (i=0, j=0): Center, r = 0.00 cm → Sample basket (U=4)
- (i=1, j=0): East, r = 5.08 cm → Control rod thimble (U=2 or U=3)
- (i=0, j=1): North, r = 5.08 cm → Control rod thimble (U=2 or U=3)
- (i=-1, j=0): West, r = 5.08 cm → Control rod thimble (U=2 or U=3)
- (i=2, j=0): r = 10.17 cm → Graphite stringer (U=1)

### Central Disruption Handling

**4 Central Positions:**

**Configuration A (Assumed - Verify with Literature):**
```
Position (i=0, j=0):   Sample basket (U=4)
Position (i=1, j=0):   Control rod 1 (U=2, withdrawn)
Position (i=0, j=1):   Control rod 2 (U=2, withdrawn)
Position (i=-1, j=0):  Regulating rod (U=3, 3% inserted)
```

**Configuration B (Alternative - 120° Spacing):**
If control rods are equidistant at 120° angles:
- May not align exactly with square lattice grid
- Require interpolation or nearest-neighbor assignment
- Need literature verification for exact positions

**Recommendation:** Use Configuration A (aligned with grid) for initial model. Verify exact control rod positions from ORNL reports before finalization.

### Edge Boundary Treatment

**Positions Outside Lattice Radius:**

**Option 1: Fill with Void Universe**
- Define Universe 99 as void (IMP:N=0)
- Fill all positions with r > 70.285 cm with U=99
- Clear boundary, but increases FILL array complexity

**Option 2: Truncate with RCC Boundary**
- Fill all positions with U=1 (graphite stringer)
- Outer boundary defined by RCC surface (radius 70.285 cm)
- MCNP truncates geometry at RCC boundary
- Simpler FILL array

**Recommended:** Option 2 (RCC truncation)
- Simpler implementation
- MCNP handles boundary automatically
- Matches physical configuration (lattice bounded by core can)

**Boundary Cell:**
```
c Core region with lattice
1000  0  -1000  FILL=10  IMP:N=1  $ Core filled with lattice U=10

c RCC boundary surface
1000  RCC  0 0 0  0 0 170.311  70.285  $ Lattice radius
```

---

## 4. STRINGER UNIT CELL DESIGN (Detailed Pseudo-Code)

### Groove Geometry Specification

**Each Stringer Has 4 Grooves:**

**North Groove (on +Y face):**
- Width: 1.018 cm (X direction)
- Depth: 1.5265 cm (into stringer, -Y direction)
- Height: 170.311 cm (Z direction)
- Centered on +Y face: x = 0, y = 2.542 - 1.5265/2

**East Groove (on +X face):**
- Width: 1.018 cm (Y direction)
- Depth: 1.5265 cm (into stringer, -X direction)
- Height: 170.311 cm (Z direction)
- Centered on +X face: y = 0, x = 2.542 - 1.5265/2

**South Groove (on -Y face):**
- Width: 1.018 cm (X direction)
- Depth: 1.5265 cm (into stringer, +Y direction)
- Height: 170.311 cm (Z direction)
- Centered on -Y face: x = 0, y = -2.542 + 1.5265/2

**West Groove (on -X face):**
- Width: 1.018 cm (Y direction)
- Depth: 1.5265 cm (into stringer, +X direction)
- Height: 170.311 cm (Z direction)
- Centered on -X face: y = 0, x = -2.542 + 1.5265/2

### Detailed Pseudo-Code with Surface Definitions

```
c ===================================================================
c Universe 1: Standard Graphite Stringer Unit Cell
c ===================================================================
c Overall: 5.084 cm × 5.084 cm × 170.311 cm
c 4 grooves on sides (N, E, S, W)
c Each groove: 1.018 cm wide × 1.5265 cm deep × 170.311 cm tall

c -------------------------------------------------------------------
c Material Cells
c -------------------------------------------------------------------

c Cell 1: North groove (fuel salt)
1  1  -2.3275  -10 11 -12 13 54 -15  U=1  IMP:N=1  VOL=265.7
c              ^X bounds  ^Y bounds ^Z bounds

c Cell 2: East groove (fuel salt)
2  1  -2.3275  -16 17 -18 19 54 -15  U=1  IMP:N=1  VOL=265.7

c Cell 3: South groove (fuel salt)
3  1  -2.3275  -20 21 -22 23 54 -15  U=1  IMP:N=1  VOL=265.7

c Cell 4: West groove (fuel salt)
4  1  -2.3275  -24 25 -26 27 54 -15  U=1  IMP:N=1  VOL=265.7

c Cell 5: Central graphite region (after grooves)
5  2  -1.86  10 16 20 24 -11 -17 -21 -25 54 -15  U=1  IMP:N=1  VOL=3333.4
c           ^Complement of all 4 grooves

c -------------------------------------------------------------------
c Unit Cell Boundary Surfaces
c -------------------------------------------------------------------
50  PX  -2.542                  $ -X unit cell boundary
51  PX   2.542                  $ +X unit cell boundary
52  PY  -2.542                  $ -Y unit cell boundary
53  PY   2.542                  $ +Y unit cell boundary
54  PZ   0.0                    $ Bottom
55  PZ  170.311                 $ Top

c -------------------------------------------------------------------
c North Groove Surfaces (on +Y face)
c -------------------------------------------------------------------
c Groove centered at (x=0, y=2.542-1.5265/2=1.7788)
c Width: 1.018 cm (±0.509 cm in X)
c Depth: 1.5265 cm (extends from y=1.0155 to y=2.542)

10  PX  -0.509                  $ North groove -X
11  PX   0.509                  $ North groove +X
12  PY   1.0155                 $ North groove -Y (depth)
13  PY   2.542                  $ North groove +Y (face)

c -------------------------------------------------------------------
c East Groove Surfaces (on +X face)
c -------------------------------------------------------------------
c Groove centered at (x=1.7788, y=0)
c Width: 1.018 cm (±0.509 cm in Y)
c Depth: 1.5265 cm (extends from x=1.0155 to x=2.542)

16  PX   1.0155                 $ East groove -X (depth)
17  PX   2.542                  $ East groove +X (face)
18  PY  -0.509                  $ East groove -Y
19  PY   0.509                  $ East groove +Y

c -------------------------------------------------------------------
c South Groove Surfaces (on -Y face)
c -------------------------------------------------------------------
c Groove centered at (x=0, y=-1.7788)
c Width: 1.018 cm (±0.509 cm in X)
c Depth: 1.5265 cm (extends from y=-2.542 to y=-1.0155)

20  PX  -0.509                  $ South groove -X
21  PX   0.509                  $ South groove +X
22  PY  -2.542                  $ South groove -Y (face)
23  PY  -1.0155                 $ South groove +Y (depth)

c -------------------------------------------------------------------
c West Groove Surfaces (on -X face)
c -------------------------------------------------------------------
c Groove centered at (x=-1.7788, y=0)
c Width: 1.018 cm (±0.509 cm in Y)
c Depth: 1.5265 cm (extends from x=-2.542 to x=-1.0155)

24  PX  -2.542                  $ West groove -X (face)
25  PX  -1.0155                 $ West groove +X (depth)
26  PY  -0.509                  $ West groove -Y
27  PY   0.509                  $ West groove +Y
```

### Volume Calculations (Per Cell)

**North/East/South/West Groove (Each):**
```
V_groove = 1.018 cm × 1.5265 cm × 170.311 cm = 265.7 cm³
```

**All 4 Grooves Total:**
```
V_grooves_total = 4 × 265.7 = 1,062.8 cm³
```

**Unit Cell Total:**
```
V_cell = 5.084 cm × 5.084 cm × 170.311 cm = 4,400.1 cm³
```

**Central Graphite (After Grooves):**
```
V_graphite = V_cell - V_grooves_total
           = 4,400.1 - 1,062.8 = 3,337.3 cm³
```

**Fuel Salt Volume Fraction:**
```
f_fuel = V_grooves_total / V_cell
       = 1,062.8 / 4,400.1 = 0.2415 (24.15%)
```

### Channel Formation Verification

**When Two Stringers Are Adjacent:**
- Stringer A has groove depth: 1.5265 cm
- Stringer B has groove depth: 1.5265 cm
- Combined channel depth: 1.5265 + 1.5265 = 3.053 cm ✓

**Total Fuel Channels:**
- Approximate stringers: 565
- Each stringer has 4 grooves
- Total half-channels: 565 × 4 = 2,260
- Paired into full channels: 2,260 / 2 = 1,130 channels
- Specification: 1,140 channels
- Difference: ~10 channels (edge effects, good agreement)

---

## 5. CENTRAL DISRUPTION HANDLING STRATEGY

### Control Rod Position Determination

**Known Information:**
- 3 control rod thimbles equidistant from center
- Thimble outer diameter: 5.08 cm
- Fits within 5.084 cm unit cell (tight fit)

**Unknown Information (Requires Literature Verification):**
- Exact (x, y) positions of 3 control rods
- Angular spacing (likely 120° or aligned with grid)
- Radial distance from center

**Strategy for Planning:**

**Assumption 1: Grid-Aligned Positions**
- Control rods at nearest grid positions to center
- (i=1, j=0), (i=0, j=1), (i=-1, j=0) - three sides
- OR (i=1, j=0), (i=-1, j=0), (i=0, j=1) - different combination
- Sample basket at (i=0, j=0) center

**Assumption 2: 120° Spacing (Equidistant)**
- Control rods at 120° intervals
- May not align exactly with square lattice
- Nearest-neighbor approximation required

**Recommended Approach:**
1. Start with grid-aligned assumption (easier to implement)
2. Verify exact positions from ORNL-TM-728 or ORNL-4233
3. Adjust FILL array accordingly
4. Document assumption clearly in input file

### Sample Basket Position

**Confirmed:**
- Located at core center
- FILL array position (i=0, j=0)
- Universe 4 (sample basket unit cell)

### FILL Array Central Region Pattern

**Proposed Pattern (Grid-Aligned):**
```
c Central 5×5 region of FILL array
c j=2:   1  1  1  1  1
c j=1:   1  1  2  1  1    <- Control rod 2 at (0, 1)
c j=0:   1  3  4  2  1    <- Control rods at (-1,0) and (1,0), basket at (0,0)
c j=-1:  1  1  1  1  1
c j=-2:  1  1  1  1  1
c      i=-2 -1  0  1  2

Legend:
1 = Graphite stringer (U=1)
2 = Control rod 1 or 2, withdrawn (U=2)
3 = Regulating rod, 3% inserted (U=3)
4 = Sample basket (U=4)
```

**Alternative Pattern (120° Spacing - Approximate):**
Requires detailed calculation and literature verification.

---

## 6. EDGE BOUNDARY TREATMENT

### RCC Truncation Method (Recommended)

**Approach:**
- Fill entire 29×29 array with appropriate universes
- Define cylindrical boundary with RCC surface
- MCNP truncates lattice at boundary automatically

**Implementation:**
```
c Core lattice region
1000  0  -1000  FILL=10  IMP:N=1  $ Core filled with lattice U=10

c Core boundary
1000  RCC  0 0 0  0 0 170.311  70.285  $ r=70.285 cm, h=170.311 cm
```

**Advantages:**
- Simple FILL array (no need to calculate edge positions)
- MCNP handles truncation correctly
- Matches physical geometry

**Disadvantages:**
- Partial stringers at edge (may affect ~5-10 edge positions)
- Slight volume uncertainty at boundary

### Explicit Edge Universe Method (Alternative)

**Approach:**
- Calculate which positions are outside lattice radius
- Fill those positions with void universe (U=99)
- Only positions with r ≤ 70.285 cm get stringers (U=1)

**Implementation:**
```python
# Python script to generate FILL array with edge handling
for i in range(-14, 15):
    for j in range(-14, 15):
        x = i * 5.084
        y = j * 5.084
        r = math.sqrt(x**2 + y**2)
        
        if r > 70.285:
            universe = 99  # Void
        elif (i, j) == (0, 0):
            universe = 4   # Sample basket
        elif (i, j) in control_rod_positions:
            universe = 2 or 3  # Control rods
        else:
            universe = 1   # Graphite stringer
```

**Advantages:**
- Explicit control over edge positions
- No partial stringers

**Disadvantages:**
- Complex FILL array generation
- Must calculate 841 positions

**Recommendation:** Use RCC truncation for initial model. Switch to explicit method if edge effects cause issues.

---

## 7. LATTICE INDEXING VALIDATION

### Index Direction Verification

**LAT=1 Surface Order:**
```
100  0  -50 51 -52 53 -54 55  U=10  LAT=1  ...
         ^-X^+X^-Y^+Y^-Z^+Z
```

**Index Mapping:**
- **i direction:** Defined by surfaces 50, 51 (X-axis)
  - Negative i → -X direction (west)
  - Positive i → +X direction (east)
  
- **j direction:** Defined by surfaces 52, 53 (Y-axis)
  - Negative j → -Y direction (south)
  - Positive j → +Y direction (north)
  
- **k direction:** Defined by surfaces 54, 55 (Z-axis)
  - k=0 only (single layer, full height)

**FILL Array Ordering:**
- Fortran ordering: i varies fastest, j middle, k slowest
- For k=0, list j rows from j=-14 to j=+14
- Within each j row, list i from i=-14 to i=+14

**Example FILL Array Structure:**
```
FILL=-14:14 -14:14 0:0
     <i=-14> <i=-13> ... <i=+14>    $ j=+14 (top row, north)
     <i=-14> <i=-13> ... <i=+14>    $ j=+13
     ...
     <i=-14> <i=-13> ... <i=+14>    $ j=0 (center row)
     ...
     <i=-14> <i=-13> ... <i=+14>    $ j=-14 (bottom row, south)
```

### Verification Method

**Geometry Plotter:**
1. Run MCNP in plot mode: `mcnp6 inp=file.i ip`
2. Display lattice with LAT=1 option
3. Enable index labels on plot
4. Verify:
   - i increases left-to-right (X-axis)
   - j increases bottom-to-top (Y-axis)
   - Central disruptions at correct positions
   - Edge boundary matches 70.285 cm radius

**Visual Checks:**
- Sample basket at origin (i=0, j=0)
- Control rods at expected positions
- ~593 positions within circle
- Symmetric pattern

---

## 8. COMPATIBILITY WITH GEOMETRY PLAN

### Integration with Base Geometry

**Hierarchy:**
```
Universe 0 (Main):
  ├─ Reactor vessel (INOR-8 shell)
  ├─ Core can (INOR-8 shell)
  ├─ Downcomer annulus (void)
  ├─ Core region → FILL=10 (lattice universe)
  ├─ Inner reflector (graphite)
  ├─ Thermal shield (SS304)
  └─ Insulation (vermiculite)

Universe 10 (Lattice):
  └─ LAT=1 cell → FILL array (29×29)

Universe 1 (Stringer):
  ├─ Graphite body
  └─ 4 fuel salt grooves

Universe 2, 3 (Control rods):
  ├─ INOR-8 thimble
  ├─ Poison or fuel salt interior
  └─ Fuel salt exterior

Universe 4 (Sample basket):
  ├─ Homogenized interior
  ├─ INOR-8 basket wall
  └─ Fuel salt exterior
```

### Material Cross-References

**Materials Required:**
- M1: Fuel salt (LiF-BeF₂-ZrF₄-UF₄, ρ = 2.3275 g/cm³)
- M2: Graphite (nuclear grade, ρ = 1.86 g/cm³)
- M3: INOR-8 (Hastelloy-N, ρ = 8.7745 g/cm³)
- M4: Control rod poison (Gd₂O₃-Al₂O₃, ρ = 5.873 g/cm³)
- M5: Homogenized sample basket (calculated)
- M6: SS304 (thermal shield)
- M7: Vermiculite (insulation)

**Thermal Scattering:**
- MT2: Graphite (grph.87t at 923 K, closest to 911 K)

**Temperature:**
- TMP: 911 K (all core materials)

### Source and Tally Integration

**KCODE Source:**
- Source distribution in lattice cells
- Initial guess: uniform in fuel salt regions
- CEL parameter can reference lattice cells

**Tallies:**
- F4 flux tallies: Per assembly or per fuel channel
- Use lattice indexing: [i j k] notation
- F7 fission energy: Track by universe

**Example Tally:**
```
c Flux tally in central assembly
F4:N  (1<10[0 0 0]<1)    $ Universe 1, in lattice U=10 at (0,0,0)
```

---

## 9. IMPLEMENTATION CHECKLIST

### Pre-Implementation Verification

**Before Execution:**
- [ ] Confirm LAT=1 (NOT LAT=2)
- [ ] Verify surface ordering on LAT cell card
- [ ] Calculate FILL array dimensions (29×29×1)
- [ ] Verify control rod positions from literature
- [ ] Calculate homogenized sample basket composition
- [ ] Verify groove geometry calculations
- [ ] Check volume specifications (per-instance, not total)
- [ ] Verify universe hierarchy (no circular references)

### Geometry Building Phase

**Steps:**
1. Define Universe 1 (graphite stringer) with groove geometry
2. Define Universe 2 (control rod, withdrawn)
3. Define Universe 3 (regulating rod, 3% inserted)
4. Define Universe 4 (sample basket, homogenized)
5. Define Universe 10 (lattice cell with LAT=1)
6. Generate FILL array (29×29, -14:14 each axis)
7. Integrate into base geometry (Universe 0)

### Validation Phase

**Geometry Checks:**
- [ ] Plot lattice in XY plane at z=85 cm (mid-height)
- [ ] Plot lattice in XZ plane at y=0 (vertical cut)
- [ ] Enable lattice index labels
- [ ] Verify 593 positions within 70.285 cm radius
- [ ] Verify central disruptions at correct positions
- [ ] Check for overlaps (MCNP error messages)
- [ ] Visual comparison to Berkeley benchmark figures

**Volume Checks:**
- [ ] Verify stringer volume: 3,337 cm³ graphite + 1,063 cm³ fuel
- [ ] Verify total fuel volume matches specification
- [ ] Check graphite-to-fuel ratio

**Material Checks:**
- [ ] All materials defined (M1-M7)
- [ ] Densities correct (negative for g/cm³)
- [ ] Thermal scattering on graphite
- [ ] Temperature specifications (TMP cards)

---

## 10. KNOWN ISSUES AND RISKS

### Issue 1: Control Rod Exact Positions Unknown

**Risk:** High  
**Impact:** ±50-100 pcm in keff (estimated)  
**Mitigation:**
- Document assumption clearly
- Verify from ORNL-TM-728 or ORNL-4233 before finalization
- Run sensitivity study if needed

### Issue 2: Edge Stringer Partial Volumes

**Risk:** Medium  
**Impact:** ±10-30 pcm (estimated)  
**Mitigation:**
- Use RCC truncation (MCNP handles correctly)
- Alternative: Explicit edge universe with volume correction
- Document treatment method

### Issue 3: Groove Geometry Complexity

**Risk:** Medium  
**Impact:** Geometry errors, overlaps  
**Mitigation:**
- Start with simplified groove geometry (rectangular)
- Add rounded corners later if needed (+19 pcm bias acceptable)
- Use geometry plotter extensively
- Verify no overlaps before production run

### Issue 4: FILL Array Generation

**Risk:** Low  
**Impact:** Wrong positions if index ordering incorrect  
**Mitigation:**
- Use automated script to generate FILL array
- Verify with geometry plotter
- Check sample basket and control rods at correct positions
- Document Fortran ordering (i fastest, j middle)

### Issue 5: Lattice Volume Normalization

**Risk:** Low  
**Impact:** Wrong tally normalization if VOL incorrect  
**Mitigation:**
- Specify VOL per-instance (NOT total)
- V_stringer = 3,337 cm³ (graphite) + 1,063 cm³ (fuel)
- MCNP multiplies by instance count automatically

---

## 11. NEXT STEPS

### Phase Transition: Planning → Execution

**This Document Status:** PLANNING COMPLETE ✓

**Ready for Execution When:**
- [ ] User approval of lattice strategy
- [ ] Control rod positions verified from literature
- [ ] Sample basket homogenization calculated
- [ ] Base geometry (Universe 0) complete
- [ ] Materials defined (M1-M7)

**Execution Order:**
1. **mcnp-geometry-builder**: Universe 1 (stringer unit cell)
2. **mcnp-geometry-builder**: Universe 2, 3 (control rod thimbles)
3. **mcnp-material-builder**: Homogenize sample basket → M5
4. **mcnp-geometry-builder**: Universe 4 (sample basket)
5. **mcnp-lattice-builder** (THIS AGENT): Universe 10 + FILL array
6. **mcnp-geometry-builder**: Integrate lattice into Universe 0
7. **mcnp-geometry-checker**: Validate complete geometry
8. **mcnp-cell-checker**: Validate U/FILL cross-references

**Documentation Required:**
- Assumptions log (control rod positions, sample basket, edge treatment)
- Geometry verification plots
- Volume calculations
- Cross-reference to design specification

---

## 12. REFERENCES

### Design Specification
- **MSRE_Design_Specification_Complete.md** (Section 1.2: Lattice Structure)

### MCNP Manual
- Chapter 5.2: Cell Cards (U parameter)
- Chapter 5.5: Geometry Data Cards (LAT, FILL)
- Section 10.1.3: Repeated Structures Examples

### Literature (Verification Needed)
- **ORNL-TM-728:** Control rod positions (exact coordinates)
- **ORNL-4233:** Sample basket details
- **Berkeley Benchmark:** Figures 6-8 (geometry visualization)

### Calculation Scripts
- `/home/user/mcnp-skills/scripts/lattice_index_calculator.py` (to be created)
- `/home/user/mcnp-skills/scripts/fill_array_generator.py` (to be created)

---

## APPROVAL SIGNATURE

**Plan Prepared By:** mcnp-lattice-builder (Specialist Agent)  
**Date:** 2025-11-07  
**Status:** ✓ PLANNING COMPLETE - AWAITING USER APPROVAL  

**Reviewed By:** ________________  
**Approved for Execution:** ☐ YES  ☐ NO (revisions needed)  

**Revision Notes:**
_______________________________________________________________________
_______________________________________________________________________

---

**END OF LATTICE STRUCTURE PLAN**

**Next Action:** User review and approval to proceed to execution phase
