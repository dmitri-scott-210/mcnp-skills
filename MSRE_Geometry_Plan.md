# MSRE Geometry Definition Plan for MCNP Modeling
**Version:** 1.0  
**Date:** 2025-11-07  
**Status:** Planning Phase - NOT FOR EXECUTION  
**Purpose:** Strategic geometry definition plan for MSRE first criticality benchmark

---

## EXECUTIVE SUMMARY

This plan defines the systematic approach to building MSRE geometry in MCNP using:
- **RCC macrobodies** for all cylindrical components (NO infinite surfaces)
- **LAT=1 lattice** for graphite stringer array (~540-590 stringers)
- **Hierarchical numbering** to avoid conflicts and improve maintainability
- **Concentric geometry** with z-axis symmetry (origin at bottom of lattice)

**Key Design Principle:** All geometry bounded by finite RCC macrobodies - no infinite PZ planes or cylinders extending to infinity.

---

## 1. COORDINATE SYSTEM DEFINITION

### 1.1 Origin and Reference Frame

**Origin (0, 0, 0):**
- Located at **bottom center of horizontal graphite lattice**
- z=0 plane at bottom of active fuel region
- All hot dimensions (911 K) used directly

**Coordinate System:**
- **X-axis:** Horizontal (arbitrary orientation, perpendicular to axis)
- **Y-axis:** Horizontal (perpendicular to X and Z)
- **Z-axis:** Vertical (upward positive)
- **Symmetry:** Cylindrical (radial symmetry about z-axis)

### 1.2 Key Elevation Reference Points (z-coordinates)

| Component | z-coordinate (cm) | Notes |
|-----------|-------------------|-------|
| Lattice bottom | 0.0 | Origin, bottom of fuel region |
| Lattice top | 170.311 | Top of graphite stringers |
| Vessel bottom | TBD | Below lattice (lower plenum) |
| Vessel top | 272.113 | Total vessel height from bottom |
| Control rod tips (withdrawn) | 129.54 | Rods 1 & 2 position |
| Regulating rod tip | 118.364 | Critical position (3% insertion) |

**Note:** Exact vessel bottom elevation depends on lower plenum geometry (not fully specified - may require assumption or additional reference).

---

## 2. SURFACE NUMBERING SCHEME

### 2.1 Hierarchical Numbering Strategy

**Design Philosophy:**
- Group surfaces by system/function
- Reserve ranges for future expansion
- Clear association between number and component
- Avoid conflicts in complex nested geometries

### 2.2 Complete Surface Number Allocation

| Range | System/Component | Typical Surface Types | Notes |
|-------|------------------|----------------------|-------|
| **1-99** | **Core Geometry** | RCC, CZ, PZ | Primary fuel region |
| 1-19 | Graphite lattice boundaries | RCC macrobody | Cylindrical boundary at R=70.285 cm |
| 20-39 | Core can (INOR-8) | RCC macrobody | Inner R=71.097, outer R=71.737 cm |
| 40-59 | Fuel salt regions | PZ planes (if needed) | Horizontal subdivisions |
| 60-79 | Lattice cell boundaries | PX, PY planes | Square lattice unit cell |
| 80-99 | Reserved core surfaces | - | Future refinements |
| **100-199** | **Reflector System** | RCC, CZ | Radial and axial reflectors |
| 100-119 | Inner graphite reflector | RCC macrobody | Between core can and vessel |
| 120-139 | Axial reflectors | PZ, RCC | Top/bottom graphite regions |
| 140-159 | Downcomer annulus | RCC macrobody | 2.562 cm void gap |
| 160-199 | Reserved reflector | - | Future additions |
| **200-299** | **Vessel System** | RCC macrobodies | INOR-8 containment |
| 200-219 | Vessel inner wall | RCC (R=74.299 cm) | Main containment boundary |
| 220-239 | Vessel outer wall | RCC (R=76.862 cm) | Outer structural boundary |
| 240-259 | Torispherical heads | Ellipsoid/torus surfaces | Top/bottom vessel heads |
| 260-279 | Inlet/outlet penetrations | CZ, transformed surfaces | Pipe connections |
| 280-299 | Reserved vessel | - | Nozzles, flanges |
| **300-399** | **Control Rod System** | RCC, CZ | 3 control rods + thimbles |
| 300-319 | Control rod thimble 1 | RCC (OD=5.08 cm) | INOR-8 guide tube |
| 320-339 | Control rod thimble 2 | RCC (OD=5.08 cm) | INOR-8 guide tube |
| 340-359 | Control rod thimble 3 | RCC (OD=5.08 cm) | INOR-8 guide tube |
| 360-379 | Poison sections | PZ planes | Segmented poison elements |
| 380-399 | Drive mechanism surfaces | - | Simplified or omitted |
| **400-499** | **Sample Basket System** | RCC, CZ | Center channel |
| 400-419 | Sample basket channel | RCC (OD=5.4287 cm) | INOR-8 basket tube |
| 420-439 | Graphite samples | CZ cylinders | 5 samples per basket |
| 440-459 | INOR-8 samples | CZ cylinders | 4 samples per basket |
| 460-499 | Reserved samples | - | Future experiments |
| **500-599** | **Thermal Shield** | RCC macrobodies | Stainless steel shield |
| 500-519 | Shield inner surface | RCC (ID=236.22 cm) | Type 304 SS |
| 520-539 | Shield outer surface | RCC (OD~317.5 cm) | Outer boundary |
| 540-559 | Shield top/bottom | PZ planes | Axial extent |
| 560-599 | Reserved shield | - | Cooling channels, supports |
| **600-699** | **Insulation System** | RCC, PZ | Vermiculite layer |
| 600-619 | Insulation inner surface | RCC | 15.24 cm thickness |
| 620-639 | Insulation outer surface | RCC | Between vessel and shield |
| 640-699 | Reserved insulation | - | Gaps, supports |
| **700-799** | **External Boundaries** | RCC, RPP, SO | Problem geometry limits |
| 700-719 | Outer problem boundary | RCC or SO | Graveyard surface |
| 720-739 | Void regions | - | External vacuum |
| 740-799 | Reserved external | - | Future expansions |
| **800-899** | **Transformation Surfaces** | Any type with *TR | Rotated/translated components |
| 800-819 | Control rod positioning | RCC with TR | Off-axis rod positions |
| 820-839 | Sample basket positioning | - | If off-center |
| 840-899 | Reserved transforms | - | Complex assemblies |
| **900-999** | **Auxiliary Surfaces** | PX, PY, PZ, P | Helper surfaces |
| 900-919 | Symmetry planes | PX, PY, PZ | If quarter/half model |
| 920-939 | Diagnostic surfaces | - | Tally boundaries |
| 940-999 | Reserved auxiliary | - | Future use |

**Total Surface Count Estimate:** 100-150 surfaces for full-detail model

---

## 3. SURFACE DEFINITIONS PLAN

### 3.1 Core Geometry Surfaces (1-99)

#### 3.1.1 Graphite Lattice Boundary (Surfaces 1-19)

**Surface 1: Lattice Cylinder**
```
c Graphite lattice cylindrical boundary (R=70.285 cm, H=170.311 cm)
1  RCC  0 0 0  0 0 170.311  70.285
c       ^vx vy vz  ^hx hy hz    ^R (all hot dimensions at 911 K)
```

**Facet Numbering (RCC):**
- 1.1 = Cylinder side (R=70.285 cm)
- 1.2 = Bottom base (z=0)
- 1.3 = Top base (z=170.311 cm)

**Purpose:** Bounds the infinite square lattice to cylindrical core geometry

#### 3.1.2 Core Can (INOR-8) (Surfaces 20-39)

**Surface 20: Core Can Inner Wall**
```
c Core can inner wall (INOR-8, R=71.097 cm)
20  RCC  0 0 0  0 0 170.311  71.097
c        Inner radius = 71.097 cm (hot)
```

**Surface 21: Core Can Outer Wall**
```
c Core can outer wall (INOR-8, R=71.737 cm, thickness=0.642 cm)
21  RCC  0 0 0  0 0 170.311  71.737
c        Outer radius = 71.737 cm (hot)
```

**Facet Numbering:**
- 20.1/21.1 = Cylinder sides (inner/outer)
- 20.2/21.2 = Bottom bases
- 20.3/21.3 = Top bases

**Material Region:** Between surfaces 20 and 21 = INOR-8 core can (material 3)

#### 3.1.3 Lattice Unit Cell Boundaries (Surfaces 60-79)

**For LAT=1 (hexahedral/square) lattice:**

**Surface 60: X-direction pitch boundary**
```
c Unit cell X-boundary at ±2.542 cm (half-pitch = 5.084/2)
60  PX  2.542
c       Square stringer half-width
```

**Surface 61: X-direction opposite boundary**
```
61  PX  -2.542
```

**Surface 62: Y-direction pitch boundary**
```
62  PY  2.542
```

**Surface 63: Y-direction opposite boundary**
```
63  PY  -2.542
```

**Purpose:** Define unit cell for graphite stringer in LAT=1 lattice (5.084 × 5.084 cm)

**Note:** These may be defined in universe U=1 (lattice unit cell universe), NOT in base geometry

### 3.2 Reflector System Surfaces (100-199)

#### 3.2.1 Inner Graphite Reflector (Surfaces 100-119)

**Surface 100: Reflector Inner Boundary**
```
c Inner reflector boundary = core can outer (reference surface 21)
c OR defined as separate RCC if different height
100  RCC  0 0 0  0 0 170.311  71.737
c         Same as core can outer radius
```

**Surface 101: Reflector Outer Boundary**
```
c Reflector outer boundary = vessel inner wall (R=74.299 cm)
101  RCC  0 0 0  0 0 170.311  74.299
c         Thickness = 74.299 - 71.737 = 2.562 cm
```

**Material Region:** Between 100 and 101 = Graphite reflector (material 2)

**Note:** This region may be VOID at criticality (downcomer annulus with no salt flow) - CHECK specification interpretation

#### 3.2.2 Downcomer Annulus (Surfaces 140-159)

**Surface 140: Downcomer Inner Wall**
```
c Downcomer annulus inner (core can outer)
140  RCC  0 0 0  0 0 170.311  71.737
```

**Surface 141: Downcomer Outer Wall**
```
c Downcomer annulus outer (vessel inner)
141  RCC  0 0 0  0 0 170.311  74.299
```

**Material Region:** Between 140 and 141 = VOID (material 0) at zero-power criticality

**Width:** 74.299 - 71.737 = 2.562 cm (matches specification)

### 3.3 Vessel System Surfaces (200-299)

#### 3.3.1 Main Vessel Walls (Surfaces 200-239)

**Surface 200: Vessel Inner Wall**
```
c Reactor vessel inner wall (INOR-8, R=74.299 cm, full height)
200  RCC  0 0 -Z_BOTTOM  0 0 272.113  74.299
c             ^Extends below z=0 to lower plenum
c                            ^Total vessel height
```

**Surface 201: Vessel Outer Wall**
```
c Reactor vessel outer wall (R=76.862 cm, wall thickness=2.56 cm)
201  RCC  0 0 -Z_BOTTOM  0 0 272.113  76.862
```

**Material Region:** Between 200 and 201 = INOR-8 vessel (material 3)

**CRITICAL NOTE:** Z_BOTTOM value not specified in design document - requires assumption or calculation based on lower plenum geometry

#### 3.3.2 Torispherical Heads (Surfaces 240-259)

**Option 1: Simplified (Flat Heads)**
```
c Bottom head (simplified as flat)
240  PZ  -Z_BOTTOM
c Top head (simplified as flat)
241  PZ  (272.113 - Z_BOTTOM)
```

**Bias:** +243 pcm (acceptable for initial model)

**Option 2: Exact (Ellipsoidal/Torus Surfaces)**
```
c Bottom torispherical head (ellipsoid + torus combination)
240  TZ  ... (parameters from ASME head geometry)
c Top torispherical head
241  TZ  ... (parameters from ASME head geometry)
```

**Recommendation:** Start with simplified, refine later if needed

### 3.4 Control Rod System Surfaces (300-399)

#### 3.4.1 Control Rod Thimbles (Surfaces 300-359)

**Control Rod 1 Thimble (Surfaces 300-319):**

**Surface 300: Thimble 1 Outer Wall**
```
c Control rod thimble 1 outer (INOR-8, OD=5.08 cm, positioned with TR)
300  1  RCC  0 0 0  0 0 170.311  2.54
c    ^TR1 applied (positions rod off-axis)
c                              ^R = OD/2 = 5.08/2 = 2.54 cm
```

**Surface 301: Thimble 1 Inner Wall**
```
c Control rod thimble 1 inner (wall thickness=0.1651 cm)
301  1  RCC  0 0 0  0 0 170.311  2.3749
c                                 ^R_inner = 2.54 - 0.1651 = 2.3749 cm
```

**Transformation TR1:**
```
*TR1  X1 Y1 0  1 0 0  0 1 0  0 0 1
c     ^Position rod 1 at (X1, Y1) - equidistant from center
c     ^Identity rotation (no angular rotation)
```

**Position Calculation (Equilateral Triangle):**
- 3 rods equidistant from center at radius R_rod
- Angles: 0°, 120°, 240° (or similar spacing)
- **Requires:** R_rod value from specification (NOT provided - NEEDS CLARIFICATION)

**Control Rod 2 and 3:** Repeat with surfaces 320-339 and 340-359, using TR2 and TR3

#### 3.4.2 Poison Sections (Surfaces 360-379)

**Surface 360: Regulating Rod Poison Bottom**
```
c Regulating rod poison bottom (3% insertion = 118.364 cm from bottom)
360  PZ  (118.364 - 77.077)
c          ^Rod tip at 118.364, poison length 77.077 cm
c          Bottom of poison = 118.364 - 77.077 = 41.287 cm
```

**Surface 361: Regulating Rod Poison Top**
```
c Regulating rod poison top
361  PZ  118.364
c          Critical position (46.6 inches from bottom)
```

**Rods 1 & 2 (Fully Withdrawn):**
```
c Poison sections above z=129.54 cm (outside active core)
```

### 3.5 Sample Basket System Surfaces (400-499)

#### 3.5.1 Sample Basket Channel (Surfaces 400-419)

**Surface 400: Basket Outer Wall**
```
c Sample basket channel outer (INOR-8, OD=5.4287 cm, at center)
400  RCC  0 0 0  0 0 170.311  2.71435
c                              ^R = OD/2 = 5.4287/2
```

**Surface 401: Basket Inner Wall**
```
c Sample basket inner wall (wall thickness=0.079 cm)
401  RCC  0 0 0  0 0 170.311  2.63535
c                              ^R_inner = 2.71435 - 0.079
```

**Material Region:** Between 400 and 401 = INOR-8 basket (material 3)

#### 3.5.2 Sample Geometry (Surfaces 420-459)

**Option 1: Simplified (Homogenized Basket)**
```
c Homogenized samples inside basket
c Region: -401 = Homogenized INOR-8 + graphite mixture
```

**Bias:** -37 pcm (acceptable for benchmark)

**Option 2: Explicit Sample Geometry**
```
c Graphite samples (5 per basket, 0.635 × 1.1938 cm cross-section)
420  RCC  X1 Y1 0  0 0 167.64  R_sample
c    (Positioned within basket, 5 instances)

c INOR-8 samples (4 per basket, 0.635 cm diameter)
440  RCC  X5 Y5 0  0 0 167.64  0.3175
c    (Positioned within basket, 4 instances)
```

**Recommendation:** Use simplified for initial model

### 3.6 Thermal Shield Surfaces (500-599)

#### 3.6.1 Shield Main Surfaces (Surfaces 500-539)

**Surface 500: Thermal Shield Inner Wall**
```
c Thermal shield inner (Type 304 SS, ID=236.22 cm)
500  RCC  0 0 Z_SHIELD_BOTTOM  0 0 383.54  118.11
c                                       ^H    ^R = ID/2 = 236.22/2
```

**Surface 501: Thermal Shield Outer Wall**
```
c Thermal shield outer (OD~317.5 cm estimated)
501  RCC  0 0 Z_SHIELD_BOTTOM  0 0 383.54  158.75
c                                             ^R = OD/2 (approximate)
```

**Material Region:** Between 500 and 501 = Type 304 SS (material 5, TMP=305 K)

**CRITICAL NOTE:** Shield bottom elevation Z_SHIELD_BOTTOM not specified - likely below vessel bottom

#### 3.6.2 Insulation Layer (Surfaces 600-639)

**Surface 600: Insulation Inner Wall**
```
c Insulation inner (vermiculite, 15.24 cm thickness)
600  RCC  0 0 Z_INS_BOTTOM  0 0 H_INS  R_INS_INNER
c         ^Surrounds vessel, thickness 15.24 cm
```

**Surface 601: Insulation Outer Wall**
```
c Insulation outer
601  RCC  0 0 Z_INS_BOTTOM  0 0 H_INS  (R_INS_INNER + 15.24)
```

**Material Region:** Between 600 and 601 = Vermiculite (material 6, homogenized)

**NOTES:**
- R_INS_INNER likely = vessel outer radius + gap
- Gap between vessel and insulation not specified - assume small (0-5 cm)

### 3.7 External Boundaries (Surfaces 700-799)

#### 3.7.1 Problem Boundary (Surfaces 700-719)

**Surface 700: Outer Graveyard Boundary**
```
c Outer boundary (graveyard, large enough to contain shield)
700  RCC  0 0 -100  0 0 600  200
c         ^Extends well beyond all components
c         ^z from -100 to +500 cm, R=200 cm (larger than shield)
```

**OR Spherical Boundary:**
```
c Spherical outer boundary (alternative)
700  SO  300
c        ^R=300 cm (encompasses all geometry)
```

**Material Region:** Outside 700 = Graveyard (material 0, IMP:N=0)

**Purpose:** Problem termination boundary for particle transport

---

## 4. LATTICE STRUCTURE PLAN

### 4.1 LAT=1 (Hexahedral/Square) Configuration

**Critical Specification:**
- **Lattice type:** LAT=1 (NOT LAT=2)
- **Stringer cross-section:** 5.084 cm × 5.084 cm square
- **Total stringers:** ~540-590 (close-packed square array)
- **Fuel channels:** 1,140 equivalent full-size (4 grooves per stringer)

### 4.2 Universe Hierarchy

**Universe 0 (Base Universe):**
- Contains vessels, reflectors, thermal shield
- Contains lattice cell at core (FILL=2)

**Universe 1 (Graphite Stringer Unit Cell):**
- 5.084 cm × 5.084 cm square stringer
- 4 machined grooves on sides (half-channels)
- When adjacent stringers assembled, grooves form full channels

**Universe 2 (Lattice Array Universe):**
- LAT=1 cell containing FILL array
- Array dimensions: ~23×23×1 (estimated for ~540 stringers)
- Central 4 positions: control rods (U=3) + sample basket (U=4)
- Bounded by lattice radius RCC surface 1

**Universe 3 (Control Rod Unit Cell):**
- Replaces graphite stringer at control rod positions
- Contains thimble, poison, fuel salt

**Universe 4 (Sample Basket Unit Cell):**
- Replaces graphite stringer at center
- Contains basket, samples

### 4.3 Lattice Indexing (LAT=1)

**FILL Array Format:**
```
FILL=i_min:i_max j_min:j_max k_min:k_max
     universe_array (by k, j, i - CRITICAL ORDER)
```

**Example (Simplified 5×5 Array):**
```
10  0  -1  LAT=1  U=2  FILL=-2:2 -2:2 0:0
     1 1 1 1 1    $ j=2 (top row)
     1 1 1 1 1    $ j=1
     1 1 3 1 1    $ j=0 (center row, U=3 at center)
     1 1 1 1 1    $ j=-1
     1 1 1 1 1    $ j=-2 (bottom row)
```

**Actual Array:** ~23×23 stringers in circular core

### 4.4 Lattice Bounding Strategy

**Critical Design Constraint:** Lattice must be bounded by RCC surface

**Implementation:**
```
c Lattice cell (infinite square array, bounded by RCC)
20  0  -1  FILL=2  IMP:N=1  $ Cell containing lattice, bounded by surface 1 (R=70.285)
c      ^Inside lattice boundary RCC
```

**Lattice Universe 2:**
```
c Lattice array universe
10  0  -60 61 -62 63  LAT=1  U=2  FILL=-11:11 -11:11 0:0
     <array of 1s with central control rod positions as 3 or 4>
```

**Key Point:** Infinite LAT=1 array is "windowed" by cell 20 boundary (surface 1)

---

## 5. COORDINATE TRANSFORMATIONS

### 5.1 Control Rod Positioning (TR1, TR2, TR3)

**Equilateral Triangle Configuration:**

Assume control rods positioned at radius R_rod from center (VALUE NEEDS CLARIFICATION):

**TR1 (Rod 1 at 0°):**
```
*TR1  R_rod 0 0  1 0 0  0 1 0  0 0 1
c     ^X-displacement only
c     ^No rotation (identity matrix)
```

**TR2 (Rod 2 at 120°):**
```
*TR2  (R_rod*cos(120°)) (R_rod*sin(120°)) 0  1 0 0  0 1 0  0 0 1
c     ^X = -0.5*R_rod, Y = 0.866*R_rod
```

**TR3 (Rod 3 at 240°):**
```
*TR3  (R_rod*cos(240°)) (R_rod*sin(240°)) 0  1 0 0  0 1 0  0 0 1
c     ^X = -0.5*R_rod, Y = -0.866*R_rod
```

**Sample Basket:** Positioned at (0, 0, 0) - center, no transformation needed

**CRITICAL DATA NEED:** Control rod radial position R_rod not specified in design document

### 5.2 Sample Basket Positioning (if off-center)

**If sample basket is NOT at exact center:**
```
*TR4  X_basket Y_basket 0  1 0 0  0 1 0  0 0 1
```

**Specification indicates:** "Center of core" - likely (0, 0, 0), no transformation

---

## 6. GEOMETRY COMPATIBILITY WITH LATTICE

### 6.1 Lattice-to-Boundary Interface

**Challenge:** LAT=1 infinite square array bounded by cylindrical RCC

**Solution:**
1. Define lattice universe (U=2) with LAT=1 and FILL array
2. Create base universe cell that fills with U=2 and bounds by RCC surface 1
3. Stringers outside circular boundary are "cut off" by RCC

**Cell Hierarchy:**
```
c Base universe
20  0  -1  FILL=2  IMP:N=1  $ Cell filled with lattice U=2, inside RCC surf 1
21  2  -1.86  1 -20  IMP:N=1  $ Graphite reflector (outside lattice, inside core can)
...
```

**Lattice universe U=2:**
```
c Lattice definition (infinite, windowed by cell 20)
10  0  <lattice boundaries>  LAT=1  U=2  FILL=...
```

### 6.2 Control Rod Integration

**Control Rod Cell (Universe 3):**
```
c Control rod universe (replaces graphite stringer)
c Thimble outer wall (transformed by TR1, TR2, or TR3)
31  3  -8.7745  -300  U=3  IMP:N=1  $ INOR-8 thimble wall
32  1  -2.3275  301 -360  U=3  IMP:N=1  $ Fuel salt below poison
33  4  -5.873   301 -361 360  U=3  IMP:N=1  $ Poison section
34  1  -2.3275  301 361  U=3  IMP:N=1  $ Fuel salt above poison
35  0  300  U=3  IMP:N=1  $ Outside thimble (fuel/graphite homogenized?)
```

**Integration into Lattice:**
```
FILL=-11:11 -11:11 0:0
     1 1 1 ... 1 1 1
     ...
     1 1 3 1 4 1 3 1 1    $ Center row: control rods at positions
     ...
```

### 6.3 Edge Treatment (Partial Stringers)

**Issue:** Stringers at lattice periphery cut by RCC boundary

**Options:**

**Option 1: Ignore (Conservative)**
- Full stringers only in FILL array
- Void or fuel salt fills gaps at periphery
- Simplest approach

**Option 2: Explicit Edge Cells**
- Define partial stringer geometries
- Requires detailed edge mapping
- High complexity

**Recommendation:** Use Option 1 for initial model (benchmark uses this approach)

---

## 7. CRITICAL DESIGN NOTES AND CONCERNS

### 7.1 Missing Geometric Data

**CRITICAL NEEDS (from specification analysis):**

1. **Control Rod Radial Position (R_rod):**
   - Specification states "equidistant from center" but gives NO radius value
   - **ACTION REQUIRED:** Search ORNL-TM-728 or IRPhEP Handbook
   - **Workaround:** Estimate from lattice pitch (~10-15 cm radius?)

2. **Vessel Bottom Elevation (Z_BOTTOM):**
   - Total vessel height = 272.113 cm specified
   - Lattice height = 170.311 cm
   - Lower plenum geometry not detailed
   - **ACTION REQUIRED:** Check design drawings
   - **Workaround:** Assume symmetric (z=0 at vessel vertical center?)

3. **Thermal Shield Bottom Elevation:**
   - Shield height = 383.54 cm specified
   - Relative position to vessel not given
   - **Workaround:** Assume extends beyond vessel top/bottom by equal margins

4. **Insulation Inner Radius:**
   - Thickness = 15.24 cm specified
   - Inner boundary (vessel outer + gap?) not specified
   - **Workaround:** Assume minimal gap (1 cm?)

### 7.2 Geometry Simplification Options

**For Initial Model (Gate 2):**

| Component | Detailed Model | Simplified Model | Bias (pcm) |
|-----------|---------------|------------------|------------|
| Torispherical heads | Ellipsoid + torus | Flat planes | +243 |
| Fuel channels | Rounded corners (R=0.508 cm) | Sharp rectangular | +19 |
| Sample baskets | Explicit samples | Homogenized | -37 |
| Lower plenum | Detailed piping | Homogenized 90.8:9.2 salt:INOR-8 | Small |
| Edge stringers | Partial geometry | Full stringers only | TBD |

**Recommendation:** Use simplifications except torispherical heads (large bias)

### 7.3 Lattice Array Size Calculation

**Estimate Stringer Count:**

Given:
- Lattice radius R = 70.285 cm
- Stringer pitch = 5.084 cm
- Square lattice (LAT=1)

**Array Dimensions:**
- Diameter = 2 × 70.285 = 140.57 cm
- Stringers across diameter = 140.57 / 5.084 ≈ 27.6
- Use array: -13:13 (27×27 = 729 positions)
- Circular cutoff reduces to ~540-590 stringers (matches specification ✓)

**FILL Array:**
```
FILL=-13:13 -13:13 0:0
     <27×27 array of universe numbers>
```

### 7.4 Macrobody vs. Explicit Surface Trade-offs

**Macrobody (RCC) Advantages:**
- Fewer surface cards
- Automatic facet generation
- Easier to modify (change 1 parameter vs. 3 surfaces)

**Macrobody Restrictions:**
- Cannot use facets with SSR/SSW/PTRAC (not an issue for this benchmark)
- Slightly less flexible for complex geometry

**Decision:** Use RCC macrobodies throughout (design constraint)

---

## 8. VALIDATION AND VERIFICATION PLAN

### 8.1 Pre-Execution Geometry Checks

**Before MCNP run:**

1. **Surface Numbering Audit:**
   - [ ] No duplicate surface numbers
   - [ ] All surfaces in allocated ranges
   - [ ] Transformation numbers match *TR definitions

2. **Dimensional Verification:**
   - [ ] Core can: R_inner=71.097, R_outer=71.737 cm
   - [ ] Vessel: R_inner=74.299, R_outer=76.862 cm
   - [ ] Lattice: R=70.285 cm, H=170.311 cm
   - [ ] Downcomer width: 74.299 - 71.737 = 2.562 cm ✓
   - [ ] Core can thickness: 71.737 - 71.097 = 0.640 cm (spec=0.642 cm, close ✓)

3. **RCC Macrobody Format:**
   - [ ] All RCC surfaces: `j RCC vx vy vz hx hy hz R`
   - [ ] 7 values (vertex + height vector + radius)
   - [ ] Heights in z-direction: hy=hz=0, hz=height

4. **Coordinate System Consistency:**
   - [ ] Origin at z=0 (bottom of lattice) ✓
   - [ ] All z-coordinates referenced to origin
   - [ ] All hot dimensions (911 K) used

### 8.2 Plot Mode Validation

**Interactive Plotting (mcnp6 inp=file.i ip):**

1. **XY Plane (z=85 cm, mid-core):**
   - [ ] Circular lattice boundary visible at R=70.285 cm
   - [ ] Core can at R=71.097 and 71.737 cm
   - [ ] Vessel at R=74.299 and 76.862 cm
   - [ ] ~540-590 graphite stringers visible
   - [ ] 3 control rod thimbles at equilateral positions
   - [ ] 1 sample basket at center
   - [ ] Thermal shield at R=118.11 cm

2. **XZ Plane (y=0, vertical cross-section):**
   - [ ] Lattice height 0 to 170.311 cm
   - [ ] Vessel extends below z=0 (lower plenum)
   - [ ] Regulating rod poison tip at z=118.364 cm
   - [ ] Thermal shield extends beyond vessel
   - [ ] No dashed lines (geometry errors)

3. **YZ Plane (x=0):**
   - [ ] Same as XZ (cylindrical symmetry)

### 8.3 VOID Card Test

**Add to data block:**
```
VOID  -1
```

**Run NPS 10000:**
- [ ] Zero lost particles (MUST be 0)
- [ ] Check for overlapping cells
- [ ] Check for gaps in geometry

**Remove VOID after validation**

### 8.4 Automation Tools

**Use mcnp-geometry-checker skill:**
```bash
python /home/user/mcnp-skills/.claude/skills/mcnp-geometry-builder/scripts/geometry_validator.py MSRE_input.i
```

**Use mcnp-geometry-plotter:**
```bash
python /home/user/mcnp-skills/.claude/skills/mcnp-geometry-builder/scripts/geometry_plotter_helper.py MSRE_input.i
```

---

## 9. SURFACE CARD PSEUDO-CODE SUMMARY

### 9.1 Complete Surface Block Template

```mcnp
c ===================================================================
c SURFACE CARDS - MSRE First Criticality Benchmark
c All dimensions HOT (911 K)
c Origin: z=0 at bottom of horizontal graphite lattice
c Coordinate system: z-axis vertical (upward positive)
c ===================================================================

c --- Core Geometry (1-99) ---

c Graphite lattice boundary (R=70.285 cm, H=170.311 cm)
1    RCC  0 0 0  0 0 170.311  70.285
c         ^Vertex at origin  ^Height vector (z-direction)  ^Radius

c Core can (INOR-8)
20   RCC  0 0 0  0 0 170.311  71.097    $ Inner wall
21   RCC  0 0 0  0 0 170.311  71.737    $ Outer wall

c Lattice unit cell boundaries (for U=1, if needed)
60   PX   2.542    $ +X boundary (half-pitch)
61   PX  -2.542    $ -X boundary
62   PY   2.542    $ +Y boundary
63   PY  -2.542    $ -Y boundary

c --- Reflector System (100-199) ---

c Inner graphite reflector (or downcomer annulus)
100  RCC  0 0 0  0 0 170.311  71.737    $ Inner boundary (core can outer)
101  RCC  0 0 0  0 0 170.311  74.299    $ Outer boundary (vessel inner)

c --- Vessel System (200-299) ---

c Reactor vessel (INOR-8) - NEEDS Z_BOTTOM VALUE
200  RCC  0 0 -Z_BOTTOM  0 0 272.113  74.299    $ Inner wall
201  RCC  0 0 -Z_BOTTOM  0 0 272.113  76.862    $ Outer wall

c Vessel heads (simplified)
240  PZ  -Z_BOTTOM                $ Bottom head (flat)
241  PZ  (272.113 - Z_BOTTOM)     $ Top head (flat)

c --- Control Rod System (300-399) ---

c Control rod thimble 1 (with TR1) - NEEDS R_rod FOR POSITIONING
300  1  RCC  0 0 0  0 0 170.311  2.54      $ Outer wall (OD=5.08 cm)
301  1  RCC  0 0 0  0 0 170.311  2.3749    $ Inner wall (thickness=0.1651)

c Control rod thimble 2 (with TR2)
320  2  RCC  0 0 0  0 0 170.311  2.54
321  2  RCC  0 0 0  0 0 170.311  2.3749

c Control rod thimble 3 (with TR3)
340  3  RCC  0 0 0  0 0 170.311  2.54
341  3  RCC  0 0 0  0 0 170.311  2.3749

c Regulating rod poison section
360  PZ  41.287     $ Poison bottom (118.364 - 77.077)
361  PZ  118.364    $ Poison top (critical position)

c --- Sample Basket System (400-499) ---

c Sample basket channel (at center, no transformation)
400  RCC  0 0 0  0 0 170.311  2.71435    $ Outer wall (OD=5.4287)
401  RCC  0 0 0  0 0 170.311  2.63535    $ Inner wall (thickness=0.079)

c --- Thermal Shield (500-599) ---

c Thermal shield (Type 304 SS) - NEEDS Z_SHIELD_BOTTOM VALUE
500  RCC  0 0 Z_SHIELD_BOTTOM  0 0 383.54  118.11    $ Inner (ID=236.22)
501  RCC  0 0 Z_SHIELD_BOTTOM  0 0 383.54  158.75    $ Outer (OD~317.5, estimated)

c --- Insulation System (600-699) ---

c Insulation (vermiculite, 15.24 cm thickness) - NEEDS POSITIONS
600  RCC  0 0 Z_INS_BOTTOM  0 0 H_INS  R_INS_INNER
601  RCC  0 0 Z_INS_BOTTOM  0 0 H_INS  (R_INS_INNER + 15.24)

c --- External Boundaries (700-799) ---

c Problem boundary (graveyard)
700  RCC  0 0 -100  0 0 600  200    $ Large cylinder containing all geometry

c ===================================================================
c TRANSFORMATION CARDS
c ===================================================================

c Control rod positioning (equilateral triangle) - NEEDS R_rod VALUE
*TR1  R_rod 0 0  1 0 0  0 1 0  0 0 1        $ Rod 1 at 0° (EXAMPLE)
*TR2  X2 Y2 0  1 0 0  0 1 0  0 0 1          $ Rod 2 at 120°
*TR3  X3 Y3 0  1 0 0  0 1 0  0 0 1          $ Rod 3 at 240°
```

---

## 10. RECOMMENDATIONS AND NEXT STEPS

### 10.1 Critical Actions Before Execution

**HIGH PRIORITY (MUST RESOLVE):**

1. **Obtain Control Rod Radial Position (R_rod):**
   - Search ORNL-TM-728 Section 3.2 or 4.1
   - Check IRPhEP Handbook Figure 6 or Table 3
   - If unavailable, estimate from lattice pitch and request confirmation

2. **Determine Vessel Bottom Elevation (Z_BOTTOM):**
   - Calculate from lower plenum volume or height
   - Check design drawings (ORNL-TM-728 Appendix A)
   - Worst case: Assume symmetric placement (z=0 at vessel center?)

3. **Clarify Downcomer Annulus Function:**
   - Specification says "void at criticality" but also "graphite reflector"
   - Confirm if region 71.737-74.299 cm is void or graphite
   - Berkeley benchmark likely has answer

**MEDIUM PRIORITY (CAN ESTIMATE):**

4. Thermal shield and insulation elevations (extend beyond vessel ±50 cm?)
5. Insulation inner radius (vessel outer + 1 cm gap?)
6. Edge stringer treatment (full stringers only, acceptable)

### 10.2 Phased Implementation Strategy

**Phase 1: Core Region Only (Days 1-2)**
- Surfaces 1-99 (lattice, core can)
- LAT=1 lattice with graphite stringers (U=1)
- Control rods and sample basket (U=3, U=4)
- Graveyard boundary
- **Validation:** Plot mode, zero lost particles

**Phase 2: Reflector and Vessel (Day 3)**
- Surfaces 100-299 (reflector, vessel, heads)
- Downcomer annulus
- Vessel walls and boundaries
- **Validation:** Dimensional checks, material assignments

**Phase 3: External Systems (Day 4)**
- Surfaces 500-699 (thermal shield, insulation)
- External boundaries
- **Validation:** Complete geometry plot

**Phase 4: Refinement (Day 5)**
- Replace flat heads with torispherical (if needed)
- Add lower plenum details
- Optimize surface numbering
- **Validation:** Final VOID test, MCNP run

### 10.3 Integration with Material and Source Building

**After Geometry Complete:**

1. **Invoke mcnp-material-builder:**
   - Define M1 (fuel salt with Li enrichment)
   - Define M2 (graphite with B impurity)
   - Define M3 (INOR-8)
   - Define M4 (control rod poison)
   - Define M5 (thermal shield SS)
   - Define M6 (insulation vermiculite)
   - Apply thermal scattering (MT2 grph.87t)

2. **Invoke mcnp-source-builder:**
   - KCODE definition (KCODE 10000 1.0 50 200)
   - Initial source placement (likely uniform in core)

3. **Invoke mcnp-tally-builder:**
   - F7:N tally for fission distribution
   - F4:N tally for flux profile

4. **Invoke mcnp-physics-validator:**
   - Verify KCODE parameters
   - Check thermal scattering libraries
   - Validate cross-section availability

### 10.4 Expected Outcome

**Complete Surface Block:**
- 50-100 surface cards (depending on detail level)
- Systematic numbering (no conflicts)
- All dimensions hot (911 K)
- All RCC macrobodies (no infinite surfaces)
- Ready for cell card definition

**Cell Block (Subsequent Task):**
- ~50-100 cell cards
- Material assignments (M1-M6)
- Importance (IMP:N) on all cells
- Universe hierarchy (U=0, U=1, U=2, U=3, U=4)
- LAT=1 lattice with FILL array

**Validation Target:**
- Zero lost particles
- Geometry matches Berkeley Figures 6-8
- Dimensional accuracy within ±0.01 cm
- Ready for KCODE execution

---

## 11. SURFACE NUMBERING QUICK REFERENCE TABLE

| Surface | Component | Type | Key Dimension | Notes |
|---------|-----------|------|---------------|-------|
| 1 | Lattice boundary | RCC | R=70.285 cm | Bounds square lattice |
| 20-21 | Core can | RCC | R=71.097, 71.737 cm | INOR-8, 0.642 cm thick |
| 60-63 | Lattice unit cell | PX/PY | ±2.542 cm | 5.084 cm pitch |
| 100-101 | Reflector/downcomer | RCC | R=71.737, 74.299 cm | 2.562 cm thick |
| 200-201 | Vessel walls | RCC | R=74.299, 76.862 cm | 2.56 cm thick, H=272.113 |
| 240-241 | Vessel heads | PZ | z=bottom, top | Flat (simplified) |
| 300-301 | Control rod 1 thimble | RCC+TR1 | R=2.54, 2.3749 cm | OD=5.08, wall=0.1651 |
| 320-321 | Control rod 2 thimble | RCC+TR2 | Same | Positioned with TR2 |
| 340-341 | Control rod 3 thimble | RCC+TR3 | Same | Positioned with TR3 |
| 360-361 | Regulating rod poison | PZ | z=41.287, 118.364 cm | 3% insertion |
| 400-401 | Sample basket | RCC | R=2.71435, 2.63535 cm | OD=5.4287, wall=0.079 |
| 500-501 | Thermal shield | RCC | R=118.11, 158.75 cm | Type 304 SS, H=383.54 |
| 600-601 | Insulation | RCC | R=TBD, TBD+15.24 cm | Vermiculite, 15.24 thick |
| 700 | Graveyard boundary | RCC/SO | R=200 cm | Problem termination |

---

**END OF GEOMETRY PLAN**

**Status:** Ready for expert review and missing data resolution  
**Next Action:** Resolve R_rod and Z_BOTTOM values, then proceed to surface card drafting  
**Estimated Time to Execution:** 3-5 days (pending data clarification)
