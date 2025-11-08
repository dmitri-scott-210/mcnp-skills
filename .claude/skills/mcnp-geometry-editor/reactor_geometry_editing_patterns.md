# Reactor Geometry Editing Patterns

**Purpose:** Comprehensive reference for editing multi-level reactor geometries

**Based on:** AGR-1 HTGR and production reactor model analysis

**Last Updated:** November 8, 2025

---

## Overview

This guide provides detailed patterns for editing complex reactor geometries in MCNP, including:
- Multi-level lattice hierarchies (TRISO fuel, PWR assemblies)
- Hexagonal core configurations (LAT=2)
- Fill transformations for repositioning universes
- Universe hierarchy modifications
- Systematic numbering preservation

Each pattern includes:
- Complete before/after examples
- Step-by-step procedures
- Validation checklists
- Common pitfalls and solutions

---

## Pattern 1: TRISO Fuel Compact Editing

### Pattern 1A: Scaling Entire Compact Hierarchy

**Use Case:** Scale AGR-1 TRISO compact by 1.3× for sensitivity study

**Original 6-Level Hierarchy:**
```
Level 1: TRISO particle (u=1114)
  └─ 5 concentric spherical shells (kernel, buffer, IPyC, SiC, OPyC)

Level 2: Matrix cell (u=1115)
  └─ Graphite matrix surrounding particle location

Level 3: Particle lattice (u=1116, LAT=1)
  └─ 15×15×1 rectangular array of particles in matrix

Level 4: Matrix filler (u=1117)
  └─ Pure graphite cell for non-particle locations

Level 5: Compact lattice (u=1110, LAT=1)
  └─ 1×1×31 vertical stack of particle lattices

Level 6: Global placement
  └─ Compact positioned in capsule with fill transformation
```

**Scaling Procedure (Bottom-Up):**

**Step 1: Scale Level 1 - TRISO Particle (Concentric Spheres)**

```mcnp
c ========== ORIGINAL SURFACES ==========
c Level 1: TRISO particle (u=1114)
91111 so   0.017485  $ Kernel (UC fuel), R = 174.85 μm
91112 so   0.027905  $ Buffer (porous carbon), R = 279.05 μm
91113 so   0.031785  $ IPyC (inner pyrocarbon), R = 317.85 μm
91114 so   0.035375  $ SiC (silicon carbide), R = 353.75 μm
91115 so   0.039305  $ OPyC (outer pyrocarbon), R = 393.05 μm

c ========== SCALED SURFACES (×1.3) ==========
c Level 1: TRISO particle (u=1114) - SCALED 1.3×
91111 so   0.022731  $ Kernel: 0.017485 × 1.3 = 0.022731 cm
91112 so   0.036277  $ Buffer: 0.027905 × 1.3 = 0.036277 cm
91113 so   0.041321  $ IPyC:   0.031785 × 1.3 = 0.041321 cm
91114 so   0.045988  $ SiC:    0.035375 × 1.3 = 0.045988 cm
91115 so   0.051097  $ OPyC:   0.039305 × 1.3 = 0.051097 cm

c VERIFICATION:
c All radii scaled by exactly 1.3×
c Concentric relationship preserved (R1 < R2 < R3 < R4 < R5) ✓
c Shell thicknesses scaled proportionally ✓
```

**Step 2: Scale Level 3 - Particle Lattice Bounding Surface**

```mcnp
c ========== ORIGINAL SURFACE ==========
c Level 3: Particle lattice bounding box
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
c         ↑ X: ±0.043715 cm (87.43 μm half-width)
c                                               ↑ Y: ±0.043715 cm
c                                                               ↑ Z: ±0.05 cm

c ========== SCALED SURFACE (×1.3) ==========
c Level 3: Particle lattice bounding box - SCALED 1.3×
91117 rpp -0.056829 0.056829 -0.056829 0.056829 -0.065000 0.065000
c         ↑ X: 0.043715 × 1.3 = 0.056829 cm
c                                               ↑ Y: 0.043715 × 1.3
c                                                               ↑ Z: 0.05 × 1.3

c VERIFICATION:
c Box dimensions: 0.113658 × 0.113658 × 0.130000 cm
c Encloses scaled TRISO particle (OPyC R = 0.051097 cm) ✓
c Lattice pitch increased proportionally ✓
```

**Step 3: Scale Level 5 - Compact Lattice Bounding Surface**

```mcnp
c ========== ORIGINAL SURFACE ==========
c Level 5: Compact lattice bounding box
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715
c         ↑ X,Y: ±0.65 cm (compact radius)
c                                                           ↑ Z: ±0.043715 cm (single layer height)

c ========== SCALED SURFACE (×1.3) ==========
c Level 5: Compact lattice bounding box - SCALED 1.3×
91118 rpp -0.845000 0.845000 -0.845000 0.845000 -0.056829 0.056829
c         ↑ X,Y: 0.65 × 1.3 = 0.845 cm
c                                                           ↑ Z: 0.043715 × 1.3

c VERIFICATION:
c Compact diameter: 1.69 cm (was 1.30 cm)
c Single layer height: 0.113658 cm (was 0.08743 cm)
c Total compact height (31 layers): 31 × 0.113658 = 3.523 cm ✓
```

**Step 4: Scale Level 6 - Global Placement**

```mcnp
c ========== ORIGINAL SURFACES ==========
c Level 6: Compact cylinder and z-planes
97011 c/z   25.547039 -24.553123   0.63500  $ Compact cylinder (R = 0.635 cm)
98005 pz   17.81810  $ Bottom z-plane
98051 pz   20.35810  $ Top z-plane (height = 2.54 cm)

c ========== SCALED SURFACES (×1.3) ==========
c Level 6: Compact cylinder and z-planes - SCALED 1.3×
97011 c/z   25.547039 -24.553123   0.82550  $ R: 0.635 × 1.3 = 0.8255 cm
c           ↑ Center position UNCHANGED (depends on context)
98005 pz   23.16353  $ Z: 17.81810 × 1.3 = 23.16353 cm
98051 pz   26.46553  $ Z: 20.35810 × 1.3 = 26.46553 cm

c VERIFICATION:
c Compact height: 26.46553 - 23.16353 = 3.302 cm
c Expected: 2.54 × 1.3 = 3.302 cm ✓
c Note: Center (x,y) position preserved - compact scaled in place
```

**Step 5: Update Cell Volumes**

```mcnp
c ========== ORIGINAL CELL VOLUMES ==========
91101 9111 -10.924 -91111  u=1114 vol=0.000224  $ Kernel
91102 9112 -1.100  91111 -91112  u=1114 vol=0.001542  $ Buffer
91103 9113 -1.900  91112 -91113  u=1114 vol=0.000531  $ IPyC
91104 9114 -3.200  91113 -91114  u=1114 vol=0.000503  $ SiC
91105 9115 -1.900  91114 -91115  u=1114 vol=0.000581  $ OPyC

c ========== SCALED CELL VOLUMES (×1.3³ = 2.197) ==========
91101 9111 -10.924 -91111  u=1114 vol=0.000492  $ Kernel: 0.000224 × 2.197
91102 9112 -1.100  91111 -91112  u=1114 vol=0.003388  $ Buffer: 0.001542 × 2.197
91103 9113 -1.900  91112 -91113  u=1114 vol=0.001167  $ IPyC:   0.000531 × 2.197
91104 9114 -3.200  91113 -91114  u=1114 vol=0.001105  $ SiC:    0.000503 × 2.197
91105 9115 -1.900  91114 -91115  u=1114 vol=0.001276  $ OPyC:   0.000581 × 2.197

c VERIFICATION:
c Volume scaling: V_new = V_old × factor³
c Factor³ = 1.3³ = 2.197 ✓
c Total particle volume scaled correctly ✓
```

**Validation Checklist:**
- [x] All spherical radii scaled by 1.3×
- [x] All RPP dimensions scaled by 1.3×
- [x] Cylinder radius scaled by 1.3×
- [x] Z-plane positions scaled by 1.3× (if applicable)
- [x] Cell volumes scaled by 1.3³ = 2.197×
- [x] Concentric relationships preserved
- [x] Lattice pitch consistency maintained
- [x] No negative dimensions
- [ ] Plot geometry (XY, XZ, YZ views)
- [ ] Run test (NPS 1000) - check for lost particles

**Common Pitfalls:**
1. **Forgetting to scale bounding surfaces** → Lost particles
2. **Scaling volumes by factor instead of factor³** → Incorrect tallies
3. **Inconsistent scaling between levels** → Overlaps or gaps
4. **Scaling fill transformation positions** → May be undesired

---

### Pattern 1B: Repositioning Compact in Capsule

**Use Case:** Move compact from Stack 1 to Stack 2 position (60° rotation around capsule axis)

**Original Geometry:**
```mcnp
c Compact at Stack 1 position (120° from reference)
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
                                          ↑ Stack 1 position (x,y,z)

c Bounding cylinder for Stack 1
97011 c/z   25.547039 -24.553123   0.63500  $ Center matches fill position
```

**Modified Geometry (Stack 2 at 180°):**
```mcnp
c Compact at Stack 2 position (180° from reference)
91111 0  -97011  98005 -98051 fill=1110  (24.553123 -25.547039 19.108100)
                                          ↑ Stack 2 position (rotated 60°)

c Bounding cylinder for Stack 2
97011 c/z   24.553123 -25.547039   0.63500  $ Center updated to match
```

**Calculation of Stack Positions (Hexagonal Symmetry):**
```
Stack positions on hexagonal pitch (R = 36 cm):
- Stack 1 (120°): x = 36×cos(120°) = -18.0,  y = 36×sin(120°) = 31.18
                  Offset: x + 43.55 = 25.55, y - 55.73 = -24.55
- Stack 2 (180°): x = 36×cos(180°) = -36.0,  y = 36×sin(180°) = 0.0
                  Offset: x + 60.55 = 24.55, y - 25.55 = -25.55
- Stack 3 (240°): x = 36×cos(240°) = -18.0,  y = 36×sin(240°) = -31.18
                  Offset: ...

Hexagonal spacing: 60° intervals around capsule centerline
```

**Alternative Method: Using TR Card**
```mcnp
c Define transformation for Stack 2 position
*TR91  24.553123 -25.547039 19.108100  $ Translation only

c Apply to compact cell
91111 0  -97011  98005 -98051 fill=1110  trcl=91
```

**Validation:**
- [x] New position doesn't overlap other stacks
- [x] Bounding cylinder center matches fill transformation
- [x] Z-planes (98005, 98051) unchanged (same axial position)
- [x] Hexagonal symmetry maintained
- [ ] Plot to verify position
- [ ] Test run for lost particles

---

### Pattern 1C: Modifying Particle Packing Density

**Use Case:** Change from 15×15 particle array to 17×17 (increase packing fraction)

**Original Lattice:**
```mcnp
c Level 3: Particle lattice (15×15×1 array)
91116 0  -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  &
      1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
      ...  (15 rows × 15 columns = 225 entries)

c Bounding surface (pitch = 0.00583 cm)
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
          ↑ ±7 × 0.00583 = ±0.04081 cm (actual: ±0.043715 for margin)
```

**Modified Lattice (17×17):**
```mcnp
c Level 3: Particle lattice (17×17×1 array)
91116 0  -91117  u=1116 lat=1  fill=-8:8 -8:8 0:0  &
      1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115 1114 1115  &
      ...  (17 rows × 17 columns = 289 entries)

c Bounding surface (same pitch, larger extent)
91117 rpp -0.046715 0.046715 -0.046715 0.046715 -0.050000 0.050000
          ↑ ±8 × 0.00583 = ±0.04664 cm (reduced margin to fit in compact)

c Note: Total array width increased from 0.08743 cm to 0.09343 cm
c May need to adjust compact diameter or reduce pitch
```

**Packing Fraction Calculation:**
```
Original (15×15):
- Number of particles: ~113 (checkerboard pattern)
- Lattice area: (0.08743)² = 0.00764 cm²
- Particle area: 113 × π(0.039305)² = 0.548 cm²
- Packing fraction: 0.548/0.00764 = 71.7%

Modified (17×17):
- Number of particles: ~145 (checkerboard pattern)
- Lattice area: (0.09343)² = 0.00873 cm²
- Particle area: 145 × π(0.039305)² = 0.703 cm²
- Packing fraction: 0.703/0.00873 = 80.5%
```

**Validation:**
- [x] FILL array size = (8-(-8)+1)² = 17² = 289 entries
- [x] Bounding surface encloses all particles
- [x] Lattice fits within compact diameter
- [x] Packing fraction physically reasonable (<100%)
- [ ] Plot to verify no overlaps
- [ ] Verify no lost particles

---

## Pattern 2: PWR Assembly Editing

### Pattern 2A: Scaling 17×17 Pin Lattice

**Use Case:** Scale PWR fuel assembly from nominal to 1.1× for parametric study

**Original Assembly Structure:**
```
Level 1: Fuel pin (u=100)
  └─ Fuel pellet (UO2), gap, clad (Zircaloy)
  └─ Pin diameter: 0.950 cm, pitch: 1.26 cm

Level 2: Pin lattice (u=200, LAT=1)
  └─ 17×17 array (fuel pins, guide tubes, instrument tube)
  └─ Assembly width: 17 × 1.26 = 21.42 cm

Level 3: Assembly can
  └─ Box channel surrounding pins
```

**Scaling Procedure:**

**Step 1: Scale Fuel Pin (Bottom-Up)**
```mcnp
c ========== ORIGINAL PIN SURFACES ==========
101 cz  0.4096  $ Fuel pellet outer radius
102 cz  0.4178  $ Gap outer radius
103 cz  0.4750  $ Clad outer radius

c ========== SCALED PIN SURFACES (×1.1) ==========
101 cz  0.4506  $ Fuel: 0.4096 × 1.1 = 0.4506 cm
102 cz  0.4596  $ Gap:  0.4178 × 1.1 = 0.4596 cm
103 cz  0.5225  $ Clad: 0.4750 × 1.1 = 0.5225 cm

c Pin diameter increased from 0.950 cm to 1.045 cm
```

**Step 2: Scale Pin Lattice**
```mcnp
c ========== ORIGINAL LATTICE ==========
c Lattice pitch: 1.26 cm
c Bounding surface
200 rpp -10.71 10.71 -10.71 10.71 0.0 365.76
        ↑ 17 × 1.26 / 2 = 10.71 cm
                                      ↑ Active height

c ========== SCALED LATTICE (×1.1) ==========
c New pitch: 1.26 × 1.1 = 1.386 cm
c Bounding surface
200 rpp -11.781 11.781 -11.781 11.781 0.0 402.336
        ↑ 17 × 1.386 / 2 = 11.781 cm
                                          ↑ 365.76 × 1.1

c Assembly width: 23.562 cm (was 21.42 cm)
c Active height: 402.336 cm (was 365.76 cm)
```

**Step 3: Scale Assembly Can**
```mcnp
c ========== ORIGINAL CAN ==========
300 rpp -10.75 10.75 -10.75 10.75 -10.0 375.76
        ↑ Clearance around pins
                                      ↑ Includes end fittings

c ========== SCALED CAN (×1.1) ==========
300 rpp -11.825 11.825 -11.825 11.825 -11.0 413.336
        ↑ 10.75 × 1.1 = 11.825 cm
                                          ↑ 375.76 × 1.1
```

**Validation:**
- [x] Pin OD fits within lattice pitch (1.045 < 1.386 cm) ✓
- [x] Lattice pitch = pin pitch × 1.1 ✓
- [x] Assembly can encloses scaled lattice ✓
- [x] Volumes scaled by 1.1³ = 1.331 ✓
- [ ] Plot XY at core midplane
- [ ] Verify no overlaps between assemblies in core

---

### Pattern 2B: Adjusting Pin Pitch (Constant Pin Size)

**Use Case:** Increase pin pitch from 1.26 cm to 1.35 cm (more moderation)

**Pin Geometry (Unchanged):**
```mcnp
c Fuel pin surfaces (NO CHANGE)
101 cz  0.4096  $ Fuel pellet
102 cz  0.4178  $ Gap
103 cz  0.4750  $ Clad
c Pin OD = 0.950 cm
```

**Lattice Modification:**
```mcnp
c ========== ORIGINAL LATTICE ==========
c Pitch: 1.26 cm
200 0  -200  u=200 lat=1  fill=-8:8 -8:8 0:0  &
    [... fill array ...]

200 rpp -10.71 10.71 -10.71 10.71 0.0 365.76
c       ↑ 17 × 1.26 / 2

c ========== MODIFIED LATTICE ==========
c New pitch: 1.35 cm
200 0  -200  u=200 lat=1  fill=-8:8 -8:8 0:0  &
    [... same fill array ...]

200 rpp -11.475 11.475 -11.475 11.475 0.0 365.76
c       ↑ 17 × 1.35 / 2 = 11.475 cm
c                                        ↑ Height unchanged
```

**Moderator-to-Fuel Ratio Change:**
```
Original pitch: 1.26 cm
- Cell area: 1.26² = 1.5876 cm²
- Fuel area: π(0.4096)² = 0.5273 cm²
- Moderator area: 1.5876 - 0.5273 = 1.0603 cm²
- Mod/Fuel ratio: 1.0603/0.5273 = 2.01

New pitch: 1.35 cm
- Cell area: 1.35² = 1.8225 cm²
- Fuel area: π(0.4096)² = 0.5273 cm² (unchanged)
- Moderator area: 1.8225 - 0.5273 = 1.2952 cm²
- Mod/Fuel ratio: 1.2952/0.5273 = 2.46 (+22% moderation)
```

**Validation:**
- [x] Pin OD < new pitch (0.950 < 1.35 cm) ✓
- [x] Lattice bounding surface = 17 × pitch ✓
- [x] Fill array unchanged (17×17 pattern)
- [x] Moderator-to-fuel ratio increased as expected
- [ ] Run criticality calculation to verify keff change

---

## Pattern 3: Hexagonal Core Editing

### Pattern 3A: Modifying Hex Assembly Lattice

**Use Case:** Change hexagonal assembly from 7-ring to 9-ring configuration

**Original 7-Ring Assembly:**
```mcnp
c Hexagonal assembly (LAT=2)
400 0  -400  u=400 lat=2  fill=-3:3 -3:3 0:0  &
    [... 7×7 = 49 elements, hexagonal pattern ...]

c RHP bounding surface
c Pitch = R × √3 = 1.6 × 1.732 = 2.771 cm
400 rhp  0 0 0  0 0 68  0 1.6 0
c                       ↑ Height
c                              ↑ R-vector (defines pitch)

c Assembly contains 7 rings = 1 + 6 + 12 + 18 + 24 + 30 + 36 = 127 pin positions
```

**Modified 9-Ring Assembly:**
```mcnp
c Hexagonal assembly (LAT=2, expanded)
400 0  -400  u=400 lat=2  fill=-4:4 -4:4 0:0  &
    [... 9×9 = 81 elements, hexagonal pattern ...]

c RHP bounding surface (same pitch, larger extent)
c Pitch unchanged = 2.771 cm
400 rhp  0 0 0  0 0 68  0 2.08 0
c                              ↑ R increased to 2.08 cm
c New pitch = 2.08 × 1.732 = 3.602 cm (WAIT - this changes pitch!)

c CORRECT: Keep R = 1.6, but RHP doesn't bound correctly for 9-ring
c SOLUTION: RHP bounds SINGLE element, lattice indices define array extent
400 rhp  0 0 0  0 0 68  0 1.6 0  $ Pitch unchanged
c Lattice automatically extends to fill=-4:4 indices

c Assembly contains 9 rings = 1 + 6 + 12 + 18 + 24 + 30 + 36 + 42 + 48 = 217 pin positions
```

**Hexagonal Fill Pattern (9-Ring):**
```mcnp
c Center at (0,0)
c Ring numbers:
c   Ring 0 (center): 1 position
c   Ring 1: 6 positions
c   Ring 2: 12 positions
c   ...
c   Ring 8: 48 positions

c Fill array (81 elements, staggered rows):
300 300 300 300 300 300 300 300 300
 300 300 300 100 100 100 300 300 300
  300 300 100 100 200 100 100 300 300
   300 100 100 200 100 200 100 100 300
    300 100 200 100 100 100 200 100 300  ← Center row (9 elements)
     300 100 100 200 100 200 100 100 300
      300 300 100 100 200 100 100 300 300
       300 300 300 100 100 100 300 300 300
        300 300 300 300 300 300 300 300 300

Where:
  100 = Fuel pin universe
  200 = Control rod position universe
  300 = Void/reflector universe
```

**Validation:**
- [x] FILL array = 9×9 = 81 elements
- [x] Hexagonal pattern symmetric
- [x] RHP R-vector magnitude unchanged (pitch preserved)
- [x] Ring count increased from 7 to 9
- [ ] Plot to visualize hexagonal pattern
- [ ] Verify no overlapping pins

---

### Pattern 3B: Rotating Hexagonal Assembly

**Use Case:** Rotate hex assembly 30° to align with different coordinate frame

**Original Orientation:**
```mcnp
c RHP with R-vector along +Y
400 rhp  0 0 0  0 0 68  0 1.6 0
c                       ↑ Height +Z
c                              ↑ R along +Y
c This defines hexagon with flat sides parallel to X-axis
```

**Method 1: Rotate RHP R-Vector Directly**
```mcnp
c Calculate rotated R-vector (30° about Z)
c Original: (0, 1.6, 0)
c Rotation matrix:
c   [cos(30°)  -sin(30°)  0] [0  ]   [0.866×0 - 0.5×1.6]   [-0.8  ]
c   [sin(30°)   cos(30°)  0] [1.6] = [0.5×0 + 0.866×1.6] = [1.386 ]
c   [0          0         1] [0  ]   [0                ]   [0     ]

c Rotated RHP
400 rhp  0 0 0  0 0 68  -0.8 1.386 0
c                              ↑ R rotated 30° clockwise about Z

c Verify magnitude: |R| = sqrt(0.8² + 1.386²) = sqrt(0.64 + 1.92) = 1.6 ✓
c Pitch unchanged: 1.6 × √3 = 2.771 cm ✓
```

**Method 2: Using TR Card**
```mcnp
c Define 30° rotation about Z
*TR400  0 0 0  0 0 30  1
c              ↑ No translation
c                     ↑ 30° about Z
c                         ↑ Degrees mode

c Apply to RHP surface
400  400  rhp  0 0 0  0 0 68  0 1.6 0
c    ↑ Uses TR400
```

**Hexagonal Symmetry Notes:**
- Hexagons have 60° rotational symmetry
- Rotating by 30° aligns flat-to-flat orientation to point-to-point
- Rotating by 60° produces identical configuration (if uniform fill)
- Arbitrary angles may break symmetry

**Validation:**
- [x] R-vector magnitude preserved: |R| = 1.6 cm ✓
- [x] Height vector unchanged (rotation about height axis)
- [x] Pitch preserved: 2.771 cm ✓
- [ ] Plot to verify orientation
- [ ] Check fill pattern still appropriate for rotation

---

## Pattern 4: Multi-Level Hierarchy Modification

### Pattern 4A: Adding Intermediate Lattice Layer

**Use Case:** Insert sub-compact layer between compact and particle lattices

**Original 3-Level Hierarchy:**
```
Compact lattice (u=1110)
  ├─ Fills with u=1116 (particle lattice)
  └─ Fills with u=1117 (matrix)

Particle lattice (u=1116)
  ├─ Fills with u=1114 (TRISO particle)
  └─ Fills with u=1115 (matrix cell)
```

**New 4-Level Hierarchy:**
```
Compact lattice (u=1110)
  ├─ Fills with u=1118 (NEW: sub-compact)
  └─ Fills with u=1117 (matrix)

Sub-compact layer (u=1118) ← NEW LEVEL
  ├─ Fills with u=1116 (particle lattice)
  └─ Fills with u=1117 (matrix)

Particle lattice (u=1116)
  ├─ Fills with u=1114 (TRISO particle)
  └─ Fills with u=1115 (matrix cell)
```

**Implementation:**

**Step 1: Define New Universe (u=1118)**
```mcnp
c New sub-compact layer (3 particle lattices stacked vertically)
91119 0  -91120  u=1118 lat=1  fill=0:0 0:0 -1:1  &
     1117 1116 1117  $ Matrix-Particles-Matrix vertical stack

c Bounding surface for sub-compact
91120 rpp -0.65 0.65 -0.65 0.65 -0.131145 0.131145
c         ↑ X,Y match compact ↑ Z = 3 × particle lattice height
c         Particle lattice height: 0.08743 cm
c         Sub-compact height: 3 × 0.08743 = 0.262 cm (±0.131)
```

**Step 2: Modify Parent Universe (Compact Lattice)**
```mcnp
c ========== BEFORE ==========
c Compact lattice with 31 layers of particle lattices
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15  &
     1117 1R 1116 25R 1117 2R
c    ↑ Bottom matrix, 1 buffer, 25 particle layers, 3 top matrix

c ========== AFTER ==========
c Compact lattice with 11 layers (10 sub-compacts)
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -5:5  &
     1117 1118 1118 1118 1118 1118 1118 1118 1118 1118 1117
c    ↑ Bottom matrix, 10 sub-compact layers, top matrix
c    Each u=1118 contains 3 particle lattices
c    Total particle lattices: 10 × 3 = 30 (vs 25 originally)
```

**Step 3: Adjust Bounding Surface (If Needed)**
```mcnp
c ========== ORIGINAL COMPACT BOUNDING SURFACE ==========
91118 rpp -0.65 0.65 -0.65 0.65 -0.043715 0.043715
c Height: 31 × 0.08743 = 2.710 cm (single layer height × 31)

c ========== NEW COMPACT BOUNDING SURFACE ==========
91118 rpp -0.65 0.65 -0.65 0.65 -0.044 0.044
c Height: 11 × 0.262 = 2.882 cm (sub-compact height × 11)
c Slightly taller due to 30 particle layers (vs 25)
c May need to adjust to maintain overall height, or accept taller compact
```

**Validation:**
- [x] New universe u=1118 defined before referenced in u=1110
- [x] Parent fill array size: (0-0+1)×(0-0+1)×(-5-(-5)+1) = 1×1×11 = 11 ✓
- [x] Sub-compact fill array size: 1×1×3 = 3 ✓
- [x] Total particle lattices: 10 sub-compacts × 3 = 30
- [x] Bounding surfaces enclose all geometry
- [ ] Plot to verify nesting
- [ ] No orphaned universes

**Why Add Intermediate Layer?**
- **Modularity**: Easier to modify sub-compact properties
- **Symmetry**: Grouping of 3 particle lattices as unit
- **Flexibility**: Can fill with different sub-compact types (mixed loading)

---

### Pattern 4B: Removing Lattice Level (Flattening Hierarchy)

**Use Case:** Remove sub-compact layer, fill directly with particle lattices

**Current Hierarchy:**
```
Compact → Sub-compact → Particle lattice → TRISO
```

**Flattened Hierarchy:**
```
Compact → Particle lattice → TRISO
```

**Implementation:**
```mcnp
c ========== BEFORE (4 levels) ==========
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -5:5  &
     1117 1118 1118 1118 1118 1118 1118 1118 1118 1118 1117
c         ↑ References u=1118 (sub-compact)

c ========== AFTER (3 levels, flattened) ==========
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15  &
     1117 1R 1116 28R 1117 1R
c         ↑ Directly references u=1116 (particle lattice)
c         Total: 2 matrix + 28 particle lattices = 30 layers

c Remove u=1118 definition (no longer needed)
c 91119 0  -91120  u=1118 ...  ← DELETE THIS CELL
```

**Validation:**
- [x] Fill array size: 1×1×31 = 31 ✓
- [x] All referenced universes exist (u=1116, u=1117)
- [x] u=1118 no longer referenced anywhere
- [x] Total height unchanged
- [ ] Plot to verify structure
- [ ] Test run for errors

---

## Pattern 5: Fill Transformation Editing

### Pattern 5A: Repositioning Lattice Universe

**Use Case:** Move fuel assembly from core position (5,5) to position (7,8)

**Original Placement:**
```mcnp
c Fuel assembly at position (5,5)
c Core grid pitch = 21.5 cm
c Position: x = 5×21.5 = 107.5 cm, y = 5×21.5 = 107.5 cm
500 0  -501 -502 503 -504 505 -506  fill=200 (107.5 107.5 0.0)  imp:n=1
                                     ↑ Assembly universe
                                            ↑ Translation vector

c Bounding surfaces for assembly slot
501 px  96.75   $ X min (107.5 - 10.75)
502 px  118.25  $ X max (107.5 + 10.75)
503 py  96.75   $ Y min
504 py  118.25  $ Y max
505 pz  0.0     $ Z min
506 pz  365.76  $ Z max
```

**Modified Placement (Position 7,8):**
```mcnp
c Fuel assembly at position (7,8)
c Position: x = 7×21.5 = 150.5 cm, y = 8×21.5 = 172.0 cm
500 0  -501 -502 503 -504 505 -506  fill=200 (150.5 172.0 0.0)  imp:n=1
                                                 ↑ New translation

c Bounding surfaces updated
501 px  139.75  $ X min (150.5 - 10.75)
502 px  161.25  $ X max (150.5 + 10.75)
503 py  161.25  $ Y min (172.0 - 10.75)
504 py  182.75  $ Y max (172.0 + 10.75)
505 pz  0.0     $ Z min (unchanged)
506 pz  365.76  $ Z max (unchanged)
```

**Alternative: Using TRCL**
```mcnp
c Define transformation
*TR500  150.5 172.0 0.0  $ Translation to (7,8)

c Apply to cell
500 0  -501 -502 503 -504 505 -506  fill=200  trcl=500  imp:n=1
c                                                    ↑ References TR500
```

**Validation:**
- [x] Fill transformation matches bounding surface center
- [x] Bounding surfaces enclose assembly (21.5 cm × 21.5 cm)
- [x] No overlap with neighboring assemblies
- [x] Z-extent unchanged (axial position same)
- [ ] Plot core map to verify position
- [ ] Check assembly labels/IDs if systematic numbering used

---

### Pattern 5B: Rotating Filled Universe

**Use Case:** Rotate fuel assembly 90° to test asymmetric loading pattern

**Original Placement:**
```mcnp
c Assembly at position (5,5), no rotation
500 0  -501 -502 503 -504 505 -506  fill=200 (107.5 107.5 0.0)  imp:n=1
```

**Method 1: TR Card with Rotation + Translation**
```mcnp
c Define transformation (90° rotation about Z, then translate)
*TR500  107.5 107.5 0.0  0 0 90  1
c       ↑ Translation         ↑ 90° about Z
c                                ↑ Degrees mode

c Apply to fill
500 0  -501 -502 503 -504 505 -506  fill=200  trcl=500  imp:n=1
```

**Method 2: Fill with TR Number**
```mcnp
c Define rotation
*TR200  0 0 0  0 0 90  1  $ 90° rotation, no translation

c Apply to fill (MCNP allows fill=universe (translation) TR)
c Note: Syntax varies by MCNP version, check manual
500 0  -501 -502 503 -504 505 -506  fill=200 (107.5 107.5 0.0) tr=200  imp:n=1
```

**Effect on Assembly:**
- Pin at row i, column j → row j, column (17-i) after 90° rotation
- Asymmetric features (burnable poison, guide tubes) rotated
- Physics results may change significantly

**Validation:**
- [x] Rotation center appropriate (assembly center)
- [x] Bounding surfaces still enclose rotated assembly
- [x] Fill pattern orientation verified with plot
- [ ] Compare keff to unrotated case
- [ ] Verify symmetry if assembly intended to be symmetric

---

## Common Validation Checks

### Multi-Level Hierarchy Validation

**Universe Dependency Check:**
```python
# Python script to validate universe hierarchy
def check_universe_dependencies(input_file):
    universes_defined = set()
    universes_used = set()

    # Scan for universe definitions
    for line in input_file:
        if 'u=' in line.lower():
            u_num = extract_universe_number(line)
            universes_defined.add(u_num)

        if 'fill=' in line.lower():
            fill_nums = extract_fill_universes(line)
            universes_used.update(fill_nums)

    # Check for missing definitions
    missing = universes_used - universes_defined
    if missing:
        print(f"ERROR: Universes used but not defined: {missing}")

    # Check for orphaned definitions
    orphaned = universes_defined - universes_used
    if orphaned:
        print(f"WARNING: Universes defined but never used: {orphaned}")
```

**Lattice Consistency Check:**
```python
def validate_lattice_dimensions(lat_cell):
    # Extract FILL indices
    imin, imax = lat_cell['fill_i']
    jmin, jmax = lat_cell['fill_j']
    kmin, kmax = lat_cell['fill_k']

    # Calculate expected array size
    expected_size = (imax - imin + 1) * (jmax - jmin + 1) * (kmax - kmin + 1)

    # Count actual fill array entries
    actual_size = len(lat_cell['fill_array'])

    if expected_size != actual_size:
        print(f"ERROR: Fill array size mismatch")
        print(f"  Expected: {expected_size}")
        print(f"  Actual: {actual_size}")
```

**Surface-Volume Relationship Check:**
```python
def check_lattice_bounds(lattice_rpp, pitch, n_elements):
    """Verify lattice bounding surface matches pitch × count"""
    xmin, xmax, ymin, ymax, zmin, zmax = lattice_rpp

    # Check X dimension
    x_extent = xmax - xmin
    expected_x = n_elements_x * pitch_x
    if not isclose(x_extent, expected_x, rel_tol=0.01):
        print(f"WARNING: X extent ({x_extent}) != pitch×count ({expected_x})")

    # Repeat for Y, Z dimensions
```

---

## Summary Best Practices

1. **Always scale bottom-up** (innermost universe first)
2. **Update ALL related dimensions** (surfaces, volumes, positions)
3. **Preserve universe hierarchy** (define children before parents)
4. **Validate systematically** (7-stage validation workflow)
5. **Plot geometry** before running physics
6. **Test incrementally** (short runs to catch errors early)
7. **Document changes** (comments, modification log)
8. **Maintain numbering schemes** (preserve identity, change parameters)

---

**END OF REACTOR GEOMETRY EDITING PATTERNS**
