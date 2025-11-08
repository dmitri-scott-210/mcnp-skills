# MCNP-GEOMETRY-EDITOR SKILL REFINEMENT PLAN

**Created:** November 8, 2025
**Based on:** AGR-1 reactor model analysis (469 KB of findings)
**Priority:** 🟡 MEDIUM - Skill exists but lacks complex reactor geometry editing patterns
**Estimated Effort:** 2-3 hours

---

## EXECUTIVE SUMMARY

The mcnp-geometry-editor skill currently provides excellent coverage of **basic geometric transformations** (scaling, rotation, translation, TR cards). However, analysis of production reactor models (AGR-1 HTGR, μHTGR) reveals critical gaps in **complex reactor geometry editing**, specifically:

1. ❌ **Lattice geometry modification** - No guidance on editing fill transformations, repositioning lattices
2. ❌ **Multi-level universe hierarchy editing** - No patterns for modifying nested structures
3. ❌ **Hexagonal geometry editing** - Limited LAT=2 support
4. ❌ **Geometry validation for physics preservation** - No checks for consistency after edits
5. ❌ **Systematic numbering preservation** - No guidance on maintaining numbering schemes

**Impact:** Users can perform basic edits but struggle with reactor-scale modifications that preserve complex hierarchies and physics consistency.

---

## GAPS IDENTIFIED FROM AGR-1 ANALYSIS

### Gap 1: Lattice Geometry Modification

**Finding:** AGR-1 model uses **fill transformations** to position compact lattices:
```mcnp
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
                                          ↑ Translation vector
```

**Current Skill:** No guidance on:
- Editing fill transformation vectors
- Repositioning lattice universes
- Modifying lattice orientations
- Validating fill transformations after edits

**Required Addition:** Complete workflow for lattice geometry editing.

---

### Gap 2: Multi-Level Universe Hierarchy Preservation

**Finding:** AGR-1 uses **6-level hierarchy**:
```
Level 1: TRISO particle (u=1114) - 5 concentric shells
Level 2: Matrix cell (u=1115)
Level 3: Particle lattice (u=1116, LAT=1) - 15×15 array
Level 4: Matrix filler (u=1117)
Level 5: Compact lattice (u=1110, LAT=1) - 1×1×31 vertical
Level 6: Global placement - fill with transformation
```

**Current Skill:** Basic TR cards, but no guidance on:
- Editing geometry within nested universes
- Preserving universe relationships during edits
- Validating hierarchy consistency
- Scaling multi-level structures
- Rotating assemblies without breaking nesting

**Required Addition:** Universe-aware editing patterns and validation.

---

### Gap 3: Hexagonal Geometry Editing

**Finding:** HTGR cores use **LAT=2 hexagonal lattices** with RHP surfaces:
```mcnp
c Hexagonal assembly lattice
400 0  -400  u=400 lat=2  fill=-6:6 -6:6 0:0
    [... hexagonal pattern ...]

c RHP surface (right hexagonal prism)
400 rhp  0 0 0  0 0 68  0 1.6 0
```

**Current Skill:** Focused on rectangular (RPP) geometries, minimal hex support.

**Required Addition:**
- Hexagonal geometry transformation patterns
- RHP surface editing
- Hexagonal pitch calculations (R × √3)
- LAT=2 modification examples

---

### Gap 4: Geometry Validation for Physics Preservation

**Finding:** Complex reactor models require **multi-stage validation**:
- Surface relationships preserved (concentric spheres stay concentric)
- Universe references intact
- Lattice dimensions match bounding surfaces
- Material assignments unchanged (unless intended)
- Volumes updated for scaled geometries
- Numbering schemes preserved

**Current Skill:** Basic validation checklist, but no automated checks.

**Required Addition:** Comprehensive validation workflow with Python tools.

---

### Gap 5: Systematic Numbering Preservation

**Finding:** AGR-1 uses **hierarchical numbering** (9XYZW scheme):
```
Cell:     91234 = 9 (AGR) + 1 (capsule) + 2 (stack) + 3 (compact) + 4 (sequence)
Surface:  9123  = 9 (AGR) + 1 (capsule) + 2 (stack) + 3 (compact)
Universe: 1234  = 1 (capsule) + 2 (stack) + 3 (compact) + 4 (component type)
Material: 9123  = 9 (AGR) + 1 (capsule) + 2 (stack) + 3 (compact)
```

**Current Skill:** No guidance on preserving or extending numbering schemes.

**Required Addition:** Patterns for maintaining systematic numbering during edits.

---

## DETAILED REFINEMENT PLAN

### PHASE 1: Update SKILL.md Core Content

**File:** `.claude/skills/mcnp-geometry-editor/SKILL.md`

**Location for Additions:** After existing "Use Case 8" (line ~632)

**New Content to Add:**

```markdown
---

## Use Case 9: Modify Lattice Fill Transformation

**Scenario**: Reposition compact lattice to new location in capsule

**Original Geometry**:
```mcnp
c Compact lattice at original position
91111 0  -97011  98005 -98051 fill=1110  (25.547039 -24.553123 19.108100)
                                          ↑ Stack 1 position
```

**Editing Task**: Move to Stack 2 position at (24.553123, -25.547039, same Z)

**Method 1: Direct Edit of Translation Vector**

1. **Identify current transformation**:
```
Original: (25.547039, -24.553123, 19.108100)
New:      (24.553123, -25.547039, 19.108100)  ← Stack 2 position
```

2. **Update fill card**:
```mcnp
c Modified compact lattice
91111 0  -97011  98005 -98051 fill=1110  (24.553123 -25.547039 19.108100)
```

3. **Update bounding surface** (if off-axis cylinder):
```mcnp
c Original
97011 c/z   25.547039 -24.553123   0.63500  $ Stack 1 center

c Modified
97011 c/z   24.553123 -25.547039   0.63500  $ Stack 2 center
```

**Method 2: Using TR Card with TRCL**

```mcnp
c Define transformation
*TR91  24.553123 -25.547039 19.108100  $ Stack 2 position

c Apply to cell
91111 0  -97011  98005 -98051 fill=1110  trcl=91
```

**Validation Steps**:
- [ ] Check that new position doesn't overlap other components
- [ ] Verify bounding surface (97011) matches new center
- [ ] Confirm Z-planes (98005, 98051) still apply
- [ ] Plot geometry to visualize new position
- [ ] Test with short run (NPS 1000) to check for lost particles

**Key Points**:
- Fill transformations position entire universe at translated location
- Update off-axis surfaces (c/z) to match new position
- Hexagonal or triangular patterns: verify angular spacing (120°, 60°, etc.)
- Lattice orientation NOT affected by translation (only position changes)

---

## Use Case 10: Scale Multi-Level Lattice Hierarchy

**Scenario**: Scale AGR-1 TRISO particle compact by 1.2× (all levels)

**Original Hierarchy**:
```
Level 1: TRISO particle (u=1114)
  - Kernel: R = 0.017485 cm
  - Buffer: R = 0.027905 cm
  - IPyC:   R = 0.031785 cm
  - SiC:    R = 0.035375 cm
  - OPyC:   R = 0.039305 cm

Level 3: Particle lattice (u=1116)
  - Bounding RPP: ±0.043715 cm (X,Y), ±0.05 cm (Z)
  - 15×15×1 array

Level 5: Compact lattice (u=1110)
  - Bounding RPP: ±0.65 cm (X,Y), ±0.043715 cm (Z)
  - 1×1×31 vertical stack

Global: Compact placement
  - Cylinder 97011: c/z 25.547 -24.553  0.63500
  - Z-planes: 98005 (17.818), 98051 (20.358)
```

**Scaling Procedure (Bottom-Up)**:

**Step 1: Scale Level 1 (TRISO Particle)**
```mcnp
c Original surfaces
91111 so   0.017485  $ Kernel
91112 so   0.027905  $ Buffer
91113 so   0.031785  $ IPyC
91114 so   0.035375  $ SiC
91115 so   0.039305  $ OPyC

c Scaled surfaces (×1.2)
91111 so   0.020982  $ Kernel (0.017485 × 1.2)
91112 so   0.033486  $ Buffer (0.027905 × 1.2)
91113 so   0.038142  $ IPyC
91114 so   0.042450  $ SiC
91115 so   0.047166  $ OPyC
```

**Step 2: Scale Level 3 (Particle Lattice Bounding Surface)**
```mcnp
c Original
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000

c Scaled (×1.2)
91117 rpp -0.052458 0.052458 -0.052458 0.052458 -0.060000 0.060000
          ↑ 0.043715 × 1.2          ↑ 0.043715 × 1.2  ↑ 0.05 × 1.2
```

**Step 3: Scale Level 5 (Compact Lattice Bounding Surface)**
```mcnp
c Original
91118 rpp -0.650000 0.650000 -0.650000 0.650000 -0.043715 0.043715

c Scaled (×1.2)
91118 rpp -0.780000 0.780000 -0.780000 0.780000 -0.052458 0.052458
```

**Step 4: Scale Global Placement**
```mcnp
c Original cylinder
97011 c/z   25.547039 -24.553123   0.63500

c Scaled cylinder (radius only, center position depends on context)
97011 c/z   25.547039 -24.553123   0.76200  $ 0.635 × 1.2

c Original z-planes
98005 pz   17.81810
98051 pz   20.35810

c Scaled z-planes (if entire assembly scaled)
98005 pz   21.38172  $ 17.81810 × 1.2
98051 pz   24.42972  $ 20.35810 × 1.2

c Compact height increased from 2.54 cm to 3.048 cm
```

**Step 5: Update Cell Volumes**
```mcnp
c Original kernel volume
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Kernel

c Scaled kernel volume (V_new = V_old × scale³)
c 0.092522 × 1.2³ = 0.092522 × 1.728 = 0.159878
91101 9111 -10.924 -91111  u=1114 vol=0.159878  $ Scaled kernel
```

**Validation Checklist**:
- [ ] All spherical surfaces scaled by same factor
- [ ] RPP surfaces scaled in all 3 dimensions
- [ ] Cylinder radii scaled
- [ ] Z-plane positions scaled (if applicable)
- [ ] Fill transformation updated (if global scaling)
- [ ] Cell volumes updated: V_new = V_old × factor³
- [ ] Lattice pitch consistency: surface extent = N × pitch
- [ ] Plot all 3 views (XY, XZ, YZ) to verify
- [ ] No lost particles in test run

**Key Points**:
- Scale **bottom-up** (innermost universe first)
- **All related dimensions** must scale together
- Volumes scale by **factor³** (1.2³ = 1.728)
- Lattice bounding surfaces must scale to contain scaled elements
- Fill transformations may need adjustment depending on context
- Document scale factor prominently in comments

---

## Use Case 11: Rotate Hexagonal Assembly

**Scenario**: Rotate hexagonal fuel assembly 60° about vertical axis

**Original Geometry**:
```mcnp
c Hexagonal assembly (u=400, LAT=2)
400 0  -400  u=400 lat=2  fill=-6:6 -6:6 0:0
    [... hexagonal fill pattern ...]

c RHP bounding surface
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
400 rhp  0 0 0  0 0 68  0 1.6 0  $ Height along +Z, R along +Y
```

**Method 1: Rotation via TR Card**

1. **Create 60° rotation about Z**:
```mcnp
c 60° rotation about Z-axis
*TR400  0 0 0  0.5 0.866 0  -0.866 0.5 0  0 0 1  1
        ↑ No translation
                ↑ cos(60°)=0.5, sin(60°)=0.866
                                    ↑ Z-axis unchanged
                                                      ↑ Degrees mode
```

2. **Apply to RHP surface**:
```mcnp
c Original surface with TR
400  400  rhp  0 0 0  0 0 68  0 1.6 0  $ Uses TR400
     ↑ TR number
```

**Method 2: Direct RHP Rotation (R-vector)**

1. **Calculate rotated R-vector**:
```
Original R-vector: (0, 1.6, 0) = along +Y
Rotation matrix (60° about Z):
[cos(60°)  -sin(60°)  0] [0  ]   [-1.386]
[sin(60°)   cos(60°)  0] [1.6] = [ 0.8  ]
[0          0         1] [0  ]   [ 0    ]

Rotated R-vector: (-1.386, 0.8, 0)
```

2. **Update RHP surface**:
```mcnp
c Rotated RHP surface
400 rhp  0 0 0  0 0 68  -1.386 0.8 0  $ R-vector rotated 60°
```

**Hexagonal Symmetry Consideration**:
- Hexagonal lattices have **60° rotational symmetry**
- Rotating 60° produces identical lattice pattern (if uniform fill)
- For mixed patterns, verify fill array matches rotated positions

**Validation**:
- [ ] R-vector magnitude unchanged: |R| = 1.6 ✓
- [ ] Height vector unchanged (rotation about Z)
- [ ] Hexagonal pitch unchanged: pitch = R × √3 = 2.77 cm
- [ ] Plot geometry to verify orientation
- [ ] Lattice fill pattern consistent with rotation

**Key Points**:
- RHP rotation modifies R-vector, NOT height vector (if rotating about height axis)
- Hexagonal pitch = |R| × √3 (magnitude preserved in rotation)
- 60° rotation is special for hex lattices (symmetry)
- Arbitrary angles may break hexagonal symmetry

---

## Use Case 12: Modify Universe Hierarchy Without Breaking Nesting

**Scenario**: Add additional lattice layer between compact and particle lattice

**Original Hierarchy** (3 levels):
```
Level 5: Compact lattice (u=1110)
  └─ Fills with u=1116 (particle lattice) and u=1117 (matrix)

Level 3: Particle lattice (u=1116)
  └─ Fills with u=1114 (particle) and u=1115 (matrix cell)

Level 1: TRISO particle (u=1114)
```

**New Hierarchy** (4 levels, insert intermediate layer):
```
Level 5: Compact lattice (u=1110)
  └─ Fills with u=1118 (NEW: sub-compact layer)

Level 4: Sub-compact layer (u=1118) ← NEW LEVEL
  └─ Fills with u=1116 (particle lattice) and u=1117 (matrix)

Level 3: Particle lattice (u=1116)
  └─ Fills with u=1114 (particle) and u=1115 (matrix cell)

Level 1: TRISO particle (u=1114)
```

**Modification Procedure**:

**Step 1: Create New Universe (u=1118)**
```mcnp
c New intermediate layer universe
91119 0  -91120  u=1118 lat=1  fill=0:0 -1:1 0:0  &
     1117 1116 1117  $ 1×3 vertical sub-stack
c Matrix - Particles - Matrix

c New bounding surface
91120 rpp -0.65 0.65 -0.65 0.65 -0.131145 0.131145
c Height = 3 × original particle lattice height (3 × 0.08743)
```

**Step 2: Modify Parent Universe (u=1110) to Reference New Child**
```mcnp
c BEFORE: Compact lattice fills directly with particle lattice
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -15:15  &
     1117 2R 1116 24R 1117 2R  $ OLD: fills with u=1116

c AFTER: Compact lattice fills with new intermediate layer
91110 0  -91118 u=1110 lat=1  fill=0:0 0:0 -5:5  &
     1117 1118 1118 1118 1118 1118 1118 1118 1118 1118 1117
c NEW: 11 layers, 10 of u=1118, top/bottom u=1117
c Adjust FILL indices: -15:15 (31) → -5:5 (11)
```

**Step 3: Update Bounding Surface (if needed)**
```mcnp
c Check if compact lattice height unchanged
c Original: 31 layers × 0.08743 cm/layer = 2.710 cm
c New: 11 layers × 0.262 cm/layer = 2.882 cm ← slightly taller!

c May need to adjust compact lattice RPP or renormalize
```

**Validation**:
- [ ] New universe (u=1118) defined before used in parent
- [ ] Parent fill array updated to reference new universe
- [ ] Fill array dimensions match new structure (11 not 31)
- [ ] Bounding surfaces enclose new hierarchy
- [ ] No orphaned universes (old u=1116 no longer referenced in u=1110)
- [ ] Plot geometry to verify nesting
- [ ] Child universes (u=1114, u=1115) unchanged

**Key Points**:
- Define new universes **before** modifying parents
- Update **all references** to modified universes
- Verify **fill array dimensions** match new structure
- Preserve **child universes** if still used elsewhere
- Document hierarchy change clearly

---

## GEOMETRY EDITING VALIDATION WORKFLOW

### Validation Workflow for Complex Reactor Geometries

After any geometric modification to multi-level structures:

**Stage 1: Surface Validation**
```
1. Check surface parameters:
   - [ ] No negative radii (SO, S, C/Z, CZ)
   - [ ] RPP/RHP bounds: xmin < xmax, ymin < ymax, zmin < zmax
   - [ ] Concentric surfaces: R1 < R2 < R3 (nested)
   - [ ] Plane positions reasonable

2. Check surface relationships:
   - [ ] Off-axis cylinders (c/z): centers unchanged (unless intentional)
   - [ ] Vertical planes (pz): sequential (z1 < z2 < z3)
   - [ ] Lattice bounding surfaces: extent = N × pitch
```

**Stage 2: Cell Validation**
```
3. Check cell geometry:
   - [ ] All surface references exist
   - [ ] Boolean expressions valid (no undefined surfaces)
   - [ ] Material assignments unchanged (unless intentional)
   - [ ] Importance (IMP) consistent

4. Check volumes:
   - [ ] VOL parameters updated if geometry scaled
   - [ ] Volume scaling: V_new = V_old × factor³
```

**Stage 3: Universe Validation**
```
5. Check universe hierarchy:
   - [ ] All filled universes exist
   - [ ] No circular references (A fills B, B fills A)
   - [ ] Child universes defined before parents
   - [ ] Universe numbers unique (no conflicts)

6. Check lattice consistency:
   - [ ] FILL array size = (imax-imin+1) × (jmax-jmin+1) × (kmax-kmin+1)
   - [ ] All universe IDs in FILL array exist
   - [ ] Lattice bounding surface matches N × pitch
   - [ ] LAT type matches surface (LAT=1 → RPP, LAT=2 → RHP)
```

**Stage 4: Transformation Validation**
```
7. Check transformations:
   - [ ] TR matrices orthonormal (if manual)
   - [ ] Determinant = +1 (no reflections unless intended)
   - [ ] Translation vectors reasonable
   - [ ] TRCL references valid TR cards
   - [ ] Fill transformations place lattices within bounds
```

**Stage 5: Numbering Validation**
```
8. Check systematic numbering (if applicable):
   - [ ] Cell numbers follow scheme (e.g., 9XYZW)
   - [ ] Surface numbers consistent with hierarchy
   - [ ] Material numbers match cell assignments
   - [ ] Universe numbers follow convention
```

**Stage 6: Visual Validation**
```
9. MCNP geometry plots:
   - [ ] XY plot at representative Z
   - [ ] XZ plot at representative Y
   - [ ] YZ plot at representative X
   - [ ] Color by cell: check overlaps
   - [ ] Color by material: verify assignments
   - [ ] Zoom on critical regions (lattices, boundaries)
```

**Stage 7: Physics Validation**
```
10. Test run:
    - [ ] Run NPS 1000 to check for lost particles
    - [ ] Check for geometry errors in output
    - [ ] Verify tallies in expected locations
    - [ ] Compare results to pre-edit (if applicable)
```

---

## SYSTEMATIC NUMBERING PRESERVATION

### Maintaining Hierarchical Numbering Schemes During Edits

**Common Reactor Numbering Schemes**:

**1. AGR-1 Style (XYZW Hierarchy)**:
```
Cells:     9XYZW
           9 = Experiment ID
           X = Capsule (1-6)
           Y = Stack (1-3)
           Z = Compact (1-4)
           W = Sequence (0-9)

Surfaces:  9XYZn
           Similar hierarchy, n = surface number

Universes: XYZW
           X = Capsule
           Y = Stack
           Z = Compact
           W = Component type (0,4,5,6,7)
```

**2. PWR Assembly Style (RZA)**:
```
Cells:     ERAAZZ
           E = Element (1-9)
           R = Radial zone (1-3)
           AA = Axial zone (01-07)
           ZZ = Sub-region (00-99)

Example: 610155 = Element 6, Radial 1, Axial 01, Sub 55
```

**Editing Workflow to Preserve Numbering**:

**Step 1: Document Current Scheme**
```mcnp
c NUMBERING SCHEME:
c Cells:     9XYZW (9=AGR, X=capsule, Y=stack, Z=compact, W=seq)
c Surfaces:  9XYZn (9=AGR, X=capsule, Y=stack, Z=compact, n=ID)
c Universes: XYZW (X=capsule, Y=stack, Z=compact, W=type)
c Materials: 9XYZ (9=AGR, X=capsule, Y=stack, Z=compact)
```

**Step 2: Reserve Number Ranges**
```mcnp
c RESERVED RANGES:
c Cells:     91000-91999 (Capsule 1)
c            92000-92999 (Capsule 2)
c            [... etc ...]
c Surfaces:  9100-9199 (Capsule 1, Stack 1)
c            9200-9299 (Capsule 1, Stack 2)
```

**Step 3: When Adding New Geometry**
```mcnp
c Adding Capsule 7 (new)
c Use next available range: 97000-97999

c NEW CELLS (follow scheme):
97101 9711 -10.924 -97111  u=9714 vol=0.092522  $ Capsule 7, Stack 1, Compact 1
                    ↑ Follows surface numbering
              ↑ Follows material numbering
                                   ↑ Follows universe numbering
```

**Step 4: When Modifying Existing Geometry**
```mcnp
c BEFORE: Stack 1, Compact 2
91131 9112 -10.924 -91211  u=1124 vol=0.092522  $ Original

c AFTER: Modified radius, PRESERVE numbering
91131 9112 -10.924 -91211  u=1124 vol=0.110000  $ Modified volume
↑ Cell number UNCHANGED
      ↑ Material UNCHANGED
                   ↑ Surface UNCHANGED
                          ↑ Universe UNCHANGED
                                 ↑ Volume UPDATED
```

**Step 5: When Scaling Entire Assembly**
```mcnp
c All cells/surfaces/universes in capsule 1 retain numbers
c Only PARAMETERS change (radii, positions, volumes)

c Surfaces (capsule 1, stack 1, compact 1):
91111 so   0.020982  $ Kernel (scaled from 0.017485)
91112 so   0.033486  $ Buffer (scaled from 0.027905)
↑ Surface numbers PRESERVED, radii CHANGED
```

**Key Points**:
- Number assignments are **permanent identity** of geometric elements
- When editing, **preserve numbers**, change **parameters**
- When adding, use **next available number in reserved range**
- Document numbering scheme prominently
- Validate: no number conflicts, scheme consistent

---

## HEXAGONAL GEOMETRY EDITING SPECIFICS

### Special Considerations for LAT=2 Hexagonal Lattices

**Hexagonal Geometry Parameters**:
```mcnp
c RHP surface definition
c RHP: origin_x origin_y origin_z  height_x height_y height_z  R_x R_y R_z
100 rhp  0 0 0  0 0 68  0 1.6 0

Parameters:
  Origin: (0, 0, 0)
  Height vector: (0, 0, 68) → 68 cm along +Z
  R vector: (0, 1.6, 0) → 1.6 cm along +Y
  Hexagonal pitch: |R| × √3 = 1.6 × 1.732 = 2.771 cm
```

**Editing Hexagonal Pitch**:

**Method 1: Scale R-Vector**
```mcnp
c Original (pitch = 2.771 cm)
100 rhp  0 0 0  0 0 68  0 1.6 0

c Scaled 1.2× (new pitch = 3.325 cm)
100 rhp  0 0 0  0 0 68  0 1.92 0
                              ↑ 1.6 × 1.2
```

**Method 2: Rotate R-Vector**
```mcnp
c Original (R along +Y)
100 rhp  0 0 0  0 0 68  0 1.6 0

c Rotated 30° about Z
c R_new = R × rotation_matrix(30°, Z-axis)
c (0, 1.6, 0) → (1.386, 0.8, 0)
100 rhp  0 0 0  0 0 68  1.386 0.8 0
```

**Editing Hexagonal Assembly Height**:
```mcnp
c Original (68 cm height)
100 rhp  0 0 0  0 0 68  0 1.6 0

c Scaled 1.5× (102 cm height)
100 rhp  0 0 0  0 0 102  0 1.6 0
                      ↑ 68 × 1.5
```

**Hexagonal Lattice Fill Editing**:

**Original 7×7 hex pattern** (fill=-3:3 -3:3 0:0 = 49 elements):
```mcnp
c 7 rows, staggered
300 300 300 300 300 300 300
 300 300 100 100 100 300 300
  300 100 100 200 100 100 300
   300 100 200 100 200 100 300  ← Center row
    300 100 100 200 100 100 300
     300 300 100 100 100 300 300
      300 300 300 300 300 300 300
```

**Expanded to 9×9 hex pattern** (fill=-4:4 -4:4 0:0 = 81 elements):
```mcnp
c 9 rows, staggered
300 300 300 300 300 300 300 300 300
 300 300 300 100 100 100 300 300 300
  300 300 100 100 200 100 100 300 300
   300 100 100 200 100 200 100 100 300
    300 100 200 100 200 100 200 100 300  ← Center row
     300 100 100 200 100 200 100 100 300
      300 300 100 100 200 100 100 300 300
       300 300 300 100 100 100 300 300 300
        300 300 300 300 300 300 300 300 300
```

**Validation for Hexagonal Edits**:
- [ ] R-vector magnitude: |R| = sqrt(R_x² + R_y² + R_z²)
- [ ] Height vector perpendicular to R-vector (usually)
- [ ] Hexagonal pitch = |R| × √3
- [ ] Lattice extent ≈ (max_index) × pitch (approximate for hex)
- [ ] Fill pattern symmetric (if uniform hex)
- [ ] No overlaps in hex packing

**Key Points**:
- RHP has **2 vectors**: height and R
- Hexagonal pitch = **|R| × √3**, NOT |R|
- R-vector can point in any direction (defines hex orientation)
- Height vector usually perpendicular to R (but not required)
- Hex fill patterns are **staggered rows** (60° symmetry)

---
```

**End of new Use Cases to add to SKILL.md**

---

### PHASE 2: Create New Reference File (Reactor Geometry Editing Patterns)

**File:** `.claude/skills/mcnp-geometry-editor/reactor_geometry_editing_patterns.md`

**Purpose:** Comprehensive examples for editing complex reactor geometries (TRISO, PWR assemblies, hex cores)

**Content Outline:**

```markdown
# Reactor Geometry Editing Patterns

Comprehensive reference for editing multi-level reactor geometries.

## Pattern 1: TRISO Fuel Compact Editing
### Scaling entire compact hierarchy
### Repositioning compacts in capsule
### Modifying particle packing density

## Pattern 2: PWR Assembly Editing
### Scaling 17×17 pin lattice
### Rotating assembly to new orientation
### Adjusting pin pitch

## Pattern 3: Hexagonal Core Editing
### Modifying hex assembly lattice
### Scaling hexagonal pitch
### Rotating hexagonal assemblies

## Pattern 4: Multi-Level Hierarchy Modification
### Adding intermediate lattice layers
### Removing lattice levels
### Re-nesting universe structures

## Pattern 5: Fill Transformation Editing
### Repositioning lattice universes
### Rotating filled universes
### Array positioning with transformations
```

---

### PHASE 3: Create Python Validation Tool

**File:** `.claude/skills/mcnp-geometry-editor/scripts/geometry_edit_validator.py`

**Purpose:** Automated validation of complex geometry edits

**Functions:**
1. `validate_concentric_surfaces()` - Check spherical shell consistency
2. `validate_lattice_bounds()` - Verify lattice surface = N × pitch
3. `validate_universe_hierarchy()` - Check universe references
4. `validate_fill_transformations()` - Verify fill placements
5. `validate_numbering_scheme()` - Check systematic numbering
6. `validate_hex_geometry()` - LAT=2 specific checks

---

### PHASE 4: Create Example Files

**File 1:** `.claude/skills/mcnp-geometry-editor/example_inputs/triso_compact_edit_example.i`
- Before/after comparison
- Scaled TRISO compact (1.2×)
- All surfaces, volumes updated

**File 2:** `.claude/skills/mcnp-geometry-editor/example_inputs/hex_assembly_rotation_example.i`
- Hexagonal assembly rotated 60°
- RHP surface edited
- Fill transformation applied

**File 3:** `.claude/skills/mcnp-geometry-editor/example_inputs/multi_level_hierarchy_modification.i`
- Adding intermediate lattice layer
- Universe hierarchy updated
- Before/after comparison

---

### PHASE 5: Update Related Reference Files

**File:** `.claude/skills/mcnp-geometry-editor/transformation_specifications.md`

**Add Section:**
```markdown
## Fill Transformations for Lattice Positioning

[Detailed explanation of fill with transformation vectors]
[Examples from AGR-1 model]
[Validation criteria]
```

**File:** `.claude/skills/mcnp-geometry-editor/surface_editing_guide.md`

**Add Section:**
```markdown
## Hexagonal Geometry Surface Editing

[RHP surface parameters]
[R-vector vs height-vector]
[Pitch calculations]
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: SKILL.md Update (Priority 1)
- [ ] Add Use Case 9: Modify Lattice Fill Transformation
- [ ] Add Use Case 10: Scale Multi-Level Lattice Hierarchy
- [ ] Add Use Case 11: Rotate Hexagonal Assembly
- [ ] Add Use Case 12: Modify Universe Hierarchy Without Breaking Nesting
- [ ] Add Geometry Editing Validation Workflow section
- [ ] Add Systematic Numbering Preservation section
- [ ] Add Hexagonal Geometry Editing Specifics section

### Phase 2: Reference Files (Priority 1)
- [ ] Create reactor_geometry_editing_patterns.md (comprehensive examples)
- [ ] Update transformation_specifications.md (add fill transformations)
- [ ] Update surface_editing_guide.md (add hex geometry section)

### Phase 3: Python Tools (Priority 2)
- [ ] Create scripts/geometry_edit_validator.py
  - [ ] validate_concentric_surfaces()
  - [ ] validate_lattice_bounds()
  - [ ] validate_universe_hierarchy()
  - [ ] validate_fill_transformations()
  - [ ] validate_numbering_scheme()
  - [ ] validate_hex_geometry()

### Phase 4: Example Files (Priority 2)
- [ ] Create example_inputs/triso_compact_edit_example.i
- [ ] Create example_inputs/hex_assembly_rotation_example.i
- [ ] Create example_inputs/multi_level_hierarchy_modification.i

### Phase 5: Integration Testing (Priority 3)
- [ ] Test editing TRISO compact geometry
- [ ] Test editing hexagonal assembly
- [ ] Test multi-level hierarchy modification
- [ ] Validate all examples run without errors
- [ ] Verify plots show correct geometry

---

## VALIDATION TESTS

### Test 1: TRISO Compact Scaling

**User Query:** "I need to scale my TRISO compact by 1.3×. How do I preserve the multi-level lattice hierarchy?"

**Expected Skill Response:**
1. ✅ Provides Use Case 10 (Scale Multi-Level Lattice Hierarchy)
2. ✅ Explains bottom-up scaling procedure
3. ✅ Lists all surfaces to update (spheres, RPPs)
4. ✅ Explains volume updating (V × 1.3³ = 2.197V)
5. ✅ Provides validation checklist
6. ✅ References reactor_geometry_editing_patterns.md

---

### Test 2: Hexagonal Assembly Rotation

**User Query:** "How do I rotate a hexagonal fuel assembly 60° about the vertical axis?"

**Expected Skill Response:**
1. ✅ Provides Use Case 11 (Rotate Hexagonal Assembly)
2. ✅ Explains RHP surface R-vector rotation
3. ✅ Shows TR card method
4. ✅ Shows direct calculation method
5. ✅ Notes 60° symmetry property of hex lattices
6. ✅ Provides validation steps
7. ✅ References hexagonal geometry editing specifics section

---

### Test 3: Fill Transformation Editing

**User Query:** "I need to reposition a compact lattice to a new location in my model."

**Expected Skill Response:**
1. ✅ Provides Use Case 9 (Modify Lattice Fill Transformation)
2. ✅ Shows direct edit method (fill transformation vector)
3. ✅ Shows TR card method (TRCL)
4. ✅ Explains updating bounding surfaces (c/z centers)
5. ✅ Provides validation checklist
6. ✅ References fill transformation documentation

---

### Test 4: Universe Hierarchy Modification

**User Query:** "I want to add an intermediate lattice layer between my compact and particle lattices without breaking the existing structure."

**Expected Skill Response:**
1. ✅ Provides Use Case 12 (Modify Universe Hierarchy)
2. ✅ Shows step-by-step procedure (create new universe first)
3. ✅ Explains updating parent universe FILL array
4. ✅ Shows how to preserve child universes
5. ✅ Provides validation checklist (no orphaned universes)
6. ✅ References reactor_geometry_editing_patterns.md

---

## INTEGRATION WITH OTHER SKILLS

**mcnp-lattice-builder:**
- Geometry-editor now handles MODIFYING existing lattices
- Lattice-builder handles CREATING new lattices
- Workflow: lattice-builder → (test) → geometry-editor → (optimize)

**mcnp-transform-editor:**
- Geometry-editor uses TR cards for high-level operations
- Transform-editor handles low-level TR card details
- Geometry-editor references transform-editor for TR syntax

**mcnp-input-validator:**
- Geometry-editor modifications → validator checks
- Validation workflow integrated into editing use cases
- Python tool (geometry_edit_validator.py) complements input-validator

**mcnp-geometry-checker:**
- Geometry-checker validates CORRECTNESS (overlaps, gaps)
- Geometry-editor validates CONSISTENCY (numbering, hierarchy)
- Both used in post-edit validation

---

## SUCCESS CRITERIA

**Skill is successfully refined when:**

1. ✅ User can scale multi-level lattice hierarchies without breaking nesting
2. ✅ User can edit hexagonal geometries (RHP surfaces, LAT=2 lattices)
3. ✅ User can modify fill transformations to reposition lattice universes
4. ✅ User can add/remove lattice layers while preserving universe hierarchy
5. ✅ User can maintain systematic numbering schemes during edits
6. ✅ Validation workflow catches common reactor geometry edit errors
7. ✅ Python tool automates validation of complex edits
8. ✅ All examples run successfully in MCNP6
9. ✅ Integration with mcnp-lattice-builder, mcnp-transform-editor is clear

**Specific Metrics:**
- [ ] All 4 new use cases (9-12) added to SKILL.md
- [ ] 3 new sections added (validation workflow, numbering, hex editing)
- [ ] reactor_geometry_editing_patterns.md created (>5000 words)
- [ ] geometry_edit_validator.py created (6 validation functions)
- [ ] 3 example input files created and tested
- [ ] 2 existing reference files updated
- [ ] 4 validation tests pass

---

## ESTIMATED EFFORT

**Phase 1 (SKILL.md):** 60 minutes
- Write 4 new use cases (~300 lines each)
- Write 3 new sections (~200 lines each)
- Total: ~1800 new lines

**Phase 2 (Reference Files):** 45 minutes
- reactor_geometry_editing_patterns.md (~800 lines)
- Update 2 existing files (~200 lines each)
- Total: ~1200 lines

**Phase 3 (Python Tool):** 60 minutes
- geometry_edit_validator.py (~400 lines)
- 6 validation functions
- Testing and debugging

**Phase 4 (Example Files):** 30 minutes
- 3 example MCNP inputs (~200 lines each)
- Testing with MCNP6

**Phase 5 (Testing):** 15 minutes
- Run 4 validation tests
- Verify integration

**Total Estimated Effort:** 3.5 hours

---

## PRIORITY JUSTIFICATION

**Medium Priority (🟡) because:**

**High Impact:**
- Reactor modeling requires frequent geometry modifications
- Multi-level hierarchies are COMMON in production models
- Errors in editing complex geometry are EXPENSIVE (lost time, incorrect results)

**Moderate Urgency:**
- Current skill handles basic edits adequately
- Users CAN work around gaps with manual editing
- NOT blocking (unlike missing lattice-builder functionality)

**Complements High-Priority Skills:**
- Builds on mcnp-lattice-builder (HIGH priority)
- Integrates with mcnp-material-builder (HIGH priority)
- Essential for workflow, but not foundational

**Recommendation:** Implement AFTER high-priority skills (lattice-builder, material-builder, input-validator) but BEFORE low-priority enhancements.

---

## EXECUTION NOTES

**Best Practices for Implementation:**

1. **Start with SKILL.md updates** - This provides immediate value to users
2. **Use AGR-1 examples** - Proven production-quality patterns
3. **Generalize beyond TRISO** - Applicable to PWR, BWR, fast reactors, HTGR
4. **Emphasize validation** - Every edit should be validated rigorously
5. **Provide before/after examples** - Show transformation clearly
6. **Test all examples** - Run in MCNP6 to verify correctness

**Key Principles:**
- **Preserve structure** - Editing should maintain hierarchy
- **Validate rigorously** - Complex edits need multi-stage validation
- **Document clearly** - Numbering schemes, transformations must be obvious
- **Enable iteration** - Users should be able to edit-test-refine easily

---

## REVISION HISTORY

**Version 1.0** - November 8, 2025
- Initial refinement plan created
- Based on AGR-1 analysis findings
- Focuses on multi-level lattice editing, hexagonal geometry, fill transformations
- Estimated 3.5 hours implementation

---

**END OF MCNP-GEOMETRY-EDITOR REFINEMENT PLAN**

**Next Steps:**
1. Review and approve plan
2. Begin Phase 1 (SKILL.md updates)
3. Implement Phases 2-4 sequentially
4. Test and validate
5. Mark skill as refined in tracking document
