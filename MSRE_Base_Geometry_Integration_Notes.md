# MSRE Base Geometry (Universe 0) - Integration Notes

**Date:** 2025-11-07  
**Version:** 1.0  
**Status:** Ready for Integration with Lattice

---

## EXECUTIVE SUMMARY

Base geometry (Universe 0) for MSRE first criticality benchmark has been completed with:

✓ **Core lattice region** with FILL=10 (ready for lattice integration)  
✓ **Radial reflector system** (downcomer annulus, void at criticality)  
✓ **Reactor vessel** (INOR-8, simplified flat heads)  
✓ **Upper and lower plenums** (fuel salt regions)  
✓ **Graveyard boundary** (particle termination)

**Coordinate System:** z=0 at bottom of graphite lattice (origin at core bottom center)

---

## GEOMETRY OVERVIEW

### Radial Structure (from center outward)

| Region | Inner R (cm) | Outer R (cm) | Material | Cell | Surface |
|--------|--------------|--------------|----------|------|---------|
| **Core lattice** | 0.0 | 70.285 | FILL=10 | 1000 | 1000 |
| **Core can** | 70.285 | 71.737 | INOR-8 (m3) | 1010 | 1001 |
| **Downcomer annulus** | 71.737 | 74.299 | Void (m0) | 1020 | 1002 |
| **Vessel wall** | 74.299 | 76.862 | INOR-8 (m3) | 1100 | 1003 |
| **Outer void** | 76.862 | 150.0 | Void (m0) | 1900 | 1999 |
| **Graveyard** | 150.0 | ∞ | Void (IMP=0) | 1999 | - |

**Key Dimensions:**
- Core can thickness: 71.737 - 70.285 = **1.452 cm**
- Downcomer width: 74.299 - 71.737 = **2.562 cm** (matches spec ✓)
- Vessel wall thickness: 76.862 - 74.299 = **2.563 cm** (spec: 2.56 cm ✓)

### Axial Structure (bottom to top)

| Region | z-min (cm) | z-max (cm) | Height (cm) | Material | Cell |
|--------|------------|------------|-------------|----------|------|
| **Graveyard (below)** | -100 | -51 | - | Void (IMP=0) | 1999 |
| **Lower plenum** | -51 | 0 | 51 | Fuel salt (m1) | 1200 |
| **Active core** | 0 | 170.311 | 170.311 | FILL=10 | 1000 |
| **Upper plenum** | 170.311 | 220 | 49.689 | Fuel salt (m1) | 1300 |
| **Graveyard (above)** | 220 | 300 | - | Void (IMP=0) | 1999 |

**Key Dimensions:**
- Lower plenum depth: **51 cm** (spec: ~51 cm ✓)
- Core height: **170.311 cm** (spec: 170.311 cm ✓)
- Upper plenum height: **49.689 cm** (approximate, adjustable)
- Total vessel height: 51 + 170.311 + 49.689 = **271 cm** (spec: 272.113 cm, close ✓)

---

## SURFACE DEFINITIONS

### Core and Vessel Surfaces (RCC Macrobodies)

**Surface 1000: Graphite Lattice Boundary**
```
1000  RCC  0 0 0  0 0 170.311  70.285
```
- **Type:** Right circular cylinder (RCC)
- **Vertex:** (0, 0, 0) - lattice bottom center
- **Height vector:** (0, 0, 170.311) - upward along z-axis
- **Radius:** 70.285 cm
- **Purpose:** Bounds the LAT=1 lattice, defines core volume for FILL=10

**Surface 1001: Core Can Outer Wall**
```
1001  RCC  0 0 0  0 0 170.311  71.737
```
- **Radius:** 71.737 cm
- **Purpose:** Outer boundary of INOR-8 core can

**Surface 1002: Vessel Inner Wall**
```
1002  RCC  0 0 -51  0 0 271  74.299
```
- **Vertex:** (0, 0, -51) - vessel bottom
- **Height:** 271 cm (z = -51 to 220 cm)
- **Radius:** 74.299 cm
- **Purpose:** Inner boundary of reactor vessel

**Surface 1003: Vessel Outer Wall**
```
1003  RCC  0 0 -51  0 0 271  76.862
```
- **Radius:** 76.862 cm
- **Purpose:** Outer boundary of reactor vessel

### Axial Planes (Plenum Boundaries)

| Surface | z (cm) | Description |
|---------|--------|-------------|
| 1050 | -51.0 | Lower plenum bottom / vessel bottom |
| 1010 | 0.0 | Lattice bottom / lower plenum top |
| 1011 | 170.311 | Lattice top / upper plenum bottom |
| 1012 | 220.0 | Upper plenum top / vessel top |
| 1051 | 220.0 | Vessel top (duplicate for vessel wall) |

### Graveyard Boundary

**Surface 1999: Outer Boundary**
```
1999  RCC  0 0 -100  0 0 400  150
```
- **Radius:** 150 cm (large enough to contain vessel + margin)
- **z-range:** -100 to 300 cm
- **Purpose:** Problem termination boundary

---

## CELL DEFINITIONS

### Cell 1000: Core Lattice Region
```
1000  0  -1000  FILL=10  IMP:N=1
```
- **Material:** 0 (void - placeholder for filled universe)
- **Geometry:** Inside surface 1000 (R < 70.285 cm, 0 < z < 170.311 cm)
- **FILL:** Universe 10 (lattice universe)
- **Importance:** 1 (active tracking region)

**Integration Point:** This cell is where Universe 10 (your lattice) will be loaded.

### Cell 1010: Core Can Wall
```
1010  3  -8.7745  1000 -1001  IMP:N=1
```
- **Material:** 3 (INOR-8, ρ = 8.7745 g/cm³)
- **Geometry:** Between surfaces 1000 and 1001 (shell from 70.285 to 71.737 cm)
- **Importance:** 1

### Cell 1020: Downcomer Annulus
```
1020  0  1001 -1002  IMP:N=1
```
- **Material:** 0 (void - no salt flow at zero-power)
- **Geometry:** Between surfaces 1001 and 1002 (annulus from 71.737 to 74.299 cm)
- **Importance:** 1
- **Note:** This is VOID at criticality per specification (no salt circulation)

### Cell 1100: Vessel Wall
```
1100  3  -8.7745  1002 -1003 -1051  IMP:N=1
```
- **Material:** 3 (INOR-8, ρ = 8.7745 g/cm³)
- **Geometry:** Shell between vessel inner and outer, full height
- **Importance:** 1

### Cell 1200: Lower Plenum
```
1200  1  -2.3275  -1002 1050 -1010  IMP:N=1
```
- **Material:** 1 (fuel salt, ρ = 2.3275 g/cm³)
- **Geometry:** Inside vessel, z = -51 to 0 cm
- **Importance:** 1

### Cell 1300: Upper Plenum
```
1300  1  -2.3275  -1002 1011 -1012  IMP:N=1
```
- **Material:** 1 (fuel salt, ρ = 2.3275 g/cm³)
- **Geometry:** Inside vessel, z = 170.311 to 220 cm
- **Importance:** 1

### Cell 1999: Graveyard
```
1999  0  1999  IMP:N=0
```
- **Material:** 0 (void)
- **Geometry:** Outside surface 1999
- **Importance:** 0 (particle termination region)

---

## MATERIAL REQUIREMENTS

### Materials Used in Base Geometry

**M1: Fuel Salt** (LiF-BeF₂-ZrF₄-UF₄)
- **Density:** 2.3275 g/cm³ (hot, 911 K)
- **Temperature:** 911 K
- **Used in:** Lower plenum (1200), Upper plenum (1300)
- **Composition:** See MSRE_Design_Specification_Complete.md Section 2.1
- **Critical:** Li must be enriched (0.005% ⁶Li, NOT natural)

**M3: INOR-8** (Hastelloy-N)
- **Density:** 8.7745 g/cm³ (hot, 911 K)
- **Temperature:** 911 K
- **Used in:** Core can (1010), Vessel wall (1100), Vessel heads (1201, 1301)
- **Composition:** See MSRE_Design_Specification_Complete.md Section 2.6
  - ~70% Ni, 17% Mo, 7% Cr, 5% Fe, 0.07% C

### Materials Required in Lattice Universes

**M2: Graphite** (nuclear grade)
- **Density:** 1.86 g/cm³ (hot, 911 K)
- **Temperature:** 911 K
- **Thermal scattering:** MT2 grph.87t (923 K, closest to 911 K)
- **Impurity:** 0.8 ppm boron (CRITICAL - ±17 pcm impact)

**M4: Control Rod Poison** (Gd₂O₃-Al₂O₃)
- **Density:** 5.873 g/cm³
- **Temperature:** 911 K
- **Composition:** 70% Gd₂O₃, 30% Al₂O₃ by weight

---

## INTEGRATION WITH LATTICE

### Universe Hierarchy

```
Universe 0 (Base - THIS FILE)
    │
    ├─ Cell 1000: Core region → FILL=10
    │       │
    │       └─ Universe 10 (Lattice Universe - YOUR LATTICE)
    │               │
    │               └─ Cell 100: LAT=1 cell → FILL array
    │                       │
    │                       ├─ Universe 1: Graphite stringer
    │                       ├─ Universe 2: Control rod (withdrawn)
    │                       ├─ Universe 3: Regulating rod (3% inserted)
    │                       └─ Universe 4: Sample basket
    │
    ├─ Cell 1010: Core can (INOR-8)
    ├─ Cell 1020: Downcomer annulus (void)
    ├─ Cell 1100: Vessel wall (INOR-8)
    ├─ Cell 1200: Lower plenum (fuel salt)
    ├─ Cell 1300: Upper plenum (fuel salt)
    └─ Cell 1999: Graveyard
```

### Integration Steps

**1. Define Universe 10 (Lattice Universe):**
```
c Universe 10: Lattice definition
100  0  -50 51 -52 53 -54 55  U=10  LAT=1  IMP:N=1  &
     FILL=-14:14 -14:14 0:0  <FILL_ARRAY>

c Lattice element boundaries (5.084 cm pitch)
50  PX  -2.542
51  PX   2.542
52  PY  -2.542
53  PY   2.542
54  PZ   0.0
55  PZ  170.311
```

**2. Define Universe 1 (Graphite Stringer):**
- 5.084 cm × 5.084 cm square cross-section
- 4 grooves on sides (fuel channels)
- See MSRE_Lattice_Structure_Plan.md for details

**3. Define Universe 2, 3 (Control Rods):**
- INOR-8 thimbles (OD = 5.08 cm)
- Universe 2: Withdrawn (fuel salt inside)
- Universe 3: Regulating rod with poison (3% inserted)

**4. Define Universe 4 (Sample Basket):**
- INOR-8 basket (OD = 5.4287 cm)
- Homogenized interior (simplified model)

**5. Cell 1000 Integration:**
- Cell 1000 in Universe 0 uses `FILL=10`
- This loads Universe 10 (your lattice)
- Universe 10 contains LAT=1 cell with FILL array
- Lattice is bounded by surface 1000 (RCC, R=70.285 cm)

### Boundary Matching

**Critical Requirement:** Lattice universe surfaces must match base geometry coordinate system.

**Lattice Surfaces (Universe 10):**
- Surface 54: `PZ 0.0` (lattice bottom) → matches z=0 in Universe 0 ✓
- Surface 55: `PZ 170.311` (lattice top) → matches core height ✓
- Surfaces 50-53: Define unit cell pitch (5.084 cm)

**Truncation:** 
- Infinite LAT=1 array is "windowed" by surface 1000 (R=70.285 cm)
- MCNP automatically truncates lattice at cylindrical boundary
- ~593 positions within circle (out of 29×29=841 total)

---

## VALIDATION PLAN

### Pre-Execution Checks

**Surface Verification:**
- [ ] All RCC surfaces have 7 values: `j RCC vx vy vz hx hy hz R`
- [ ] All PZ surfaces have 1 value: `j PZ D`
- [ ] No duplicate surface numbers
- [ ] Surface numbers in correct ranges:
  - 1000-1099: Core and vessel
  - 50-99: Reserved for lattice (Universe 10)

**Cell Verification:**
- [ ] All cells have unique numbers
- [ ] All cells have IMP:N set (0 or >0)
- [ ] Graveyard exists (cell 1999, IMP:N=0)
- [ ] Cell 1000 has FILL=10 parameter
- [ ] All surfaces referenced in cells are defined

**Material Verification:**
- [ ] M1 (fuel salt) defined with Li enrichment
- [ ] M3 (INOR-8) defined
- [ ] Densities negative (g/cm³ units)
- [ ] TMP cards for all materials at 911 K

### Geometry Plotting (mcnp6 inp=file.i ip)

**XY Plane (z=85 cm, mid-core):**
- [ ] Circular lattice region at R=70.285 cm
- [ ] Core can shell at R=71.737 cm
- [ ] Downcomer annulus (void) visible
- [ ] Vessel inner wall at R=74.299 cm
- [ ] Vessel outer wall at R=76.862 cm
- [ ] Lattice visible inside core boundary
- [ ] No dashed lines (geometry errors)

**XZ Plane (y=0, vertical cross-section):**
- [ ] Lower plenum: z = -51 to 0 cm
- [ ] Core lattice: z = 0 to 170.311 cm
- [ ] Upper plenum: z = 170.311 to 220 cm
- [ ] Vessel extends full height
- [ ] No gaps or overlaps
- [ ] No dashed lines

**YZ Plane (x=0):**
- [ ] Same as XZ (cylindrical symmetry)

### VOID Test

**Procedure:**
1. Add `VOID` card to data block
2. Run with NPS 10000
3. Check output:
   - [ ] Zero lost particles (MUST be 0)
   - [ ] No "overlap" warnings
   - [ ] No "gap" warnings
4. Remove VOID card after validation

### Volume Checks

**Core Lattice (Cell 1000):**
```
V = π × R² × H = π × 70.285² × 170.311 = 2,642,600 cm³
```

**Downcomer Annulus (Cell 1020):**
```
V = π × (R₂² - R₁²) × H
  = π × (74.299² - 71.737²) × 170.311
  = 152,400 cm³
```

**Lower Plenum (Cell 1200):**
```
V = π × R² × H = π × 74.299² × 51 = 885,700 cm³
```

---

## SIMPLIFICATIONS AND BIASES

### Simplifications Used (Phase 2 Initial Model)

| Component | Detailed Model | Simplified Model | Bias (pcm) | Status |
|-----------|----------------|------------------|------------|--------|
| **Vessel heads** | Torispherical | Flat planes (PZ) | +243 | ✓ Acceptable |
| **Plenums** | Detailed piping | Uniform fuel salt | Small | ✓ Acceptable |
| **Thermal shield** | SS304 shield | Omitted | -885 | ⚠️ Add Phase 3 |
| **Insulation** | Vermiculite | Omitted | Small | ⚠️ Add Phase 3 |
| **Core can** | Separate inner/outer | Combined with lattice | Negligible | ✓ Acceptable |

**Total Bias (Current Model):** ~-640 pcm (primarily from omitted thermal shield)

**Recommendation:** 
- Current model acceptable for initial validation
- Add thermal shield in Phase 3 for production benchmark

### Phase 3 Enhancements

**To Add:**
1. **Thermal Shield** (CRITICAL - largest bias)
   - Type 304 stainless steel
   - ID = 236.22 cm, OD ~ 317.5 cm
   - Height = 383.54 cm
   - Surface numbers: 500-599

2. **Insulation Layer**
   - Vermiculite (homogenized)
   - Thickness: 15.24 cm
   - Between vessel and thermal shield
   - Surface numbers: 600-699

3. **Torispherical Vessel Heads**
   - Replace flat PZ planes with ellipsoid/torus surfaces
   - Requires ASME head geometry calculations
   - Surface numbers: 240-259

4. **Lower Plenum Details**
   - Flow distributor (omission: -98 pcm)
   - INOR-8 piping
   - Homogenized 90.8:9.2 salt:INOR-8 ratio

---

## EXPECTED RESULTS

### Criticality Target

**Expected keff (with current simplifications):**
- **Benchmark target:** 1.02132 ± 0.00003 (Serpent/ENDF-VII.1)
- **Current model:** ~1.014 - 1.016 (estimated, with biases)
- **After Phase 3 additions:** 1.019 - 1.024 (target range)

**Acceptance Criteria:**
- Statistical uncertainty < 50 pcm
- Zero lost particles
- Shannon entropy converged (slope < 0.001)
- C-E discrepancy 1.5-2.5% (2.1% expected for graphite systems)

### Neutron Balance (Expected)

**Production:**
- ~99% from ²³⁵U fission
- ~1% from other isotopes

**Absorption:**
- ~40% in fuel (U, Li, structural)
- ~25% in graphite (C-12 capture)
- ~20% in control rods (Gd poison)
- ~15% in structural materials

**Leakage:**
- ~5-10% radial leakage
- ~2-5% axial leakage

---

## TROUBLESHOOTING

### Common Issues

**Issue 1: Lost Particles**
- **Symptom:** "X particles got lost"
- **Cause:** Geometry gap or overlap
- **Fix:** Run VOID test, plot geometry, check cell boundaries

**Issue 2: Lattice Not Appearing**
- **Symptom:** Lattice region appears void in plots
- **Cause:** Universe 10 not defined or FILL parameter incorrect
- **Fix:** Verify Universe 10 exists, check FILL=10 on cell 1000

**Issue 3: Wrong keff**
- **Symptom:** keff far from 1.02 (> 3% difference)
- **Cause:** Material error (likely Li enrichment)
- **Fix:** Verify M1 uses ⁶Li at 0.005%, NOT natural Li

**Issue 4: Geometry Overlap Warning**
- **Symptom:** "cells X and Y overlap"
- **Cause:** Cell boundaries not mutually exclusive
- **Fix:** Check Boolean operations, verify surface sense

**Issue 5: Lattice Truncation**
- **Symptom:** Edge stringers partially cut by RCC
- **Cause:** Expected behavior (square lattice in circular boundary)
- **Fix:** None needed - this is correct

---

## FILE STRUCTURE

### Complete MCNP Input File Organization

```
MSRE First Criticality Benchmark
c =================================================================
c BLOCK 1: TITLE AND CELL CARDS
c =================================================================
<Base geometry cells (Universe 0) - THIS FILE>
<Lattice universe cells (Universe 10) - YOUR FILE>
<Unit cell universes (Universe 1-4) - YOUR FILE>

c =================================================================
c BLOCK 2: SURFACE CARDS
c =================================================================
<Base geometry surfaces (1000-1999) - THIS FILE>
<Lattice surfaces (50-99, 10-49) - YOUR FILE>

<BLANK LINE>

c =================================================================
c BLOCK 3: DATA CARDS
c =================================================================
MODE N
KCODE  10000  1.0  50  200
KSRC   0 0 85  10 0 85  -10 0 85  0 10 85  0 -10 85

c --- Material Definitions ---
M1   <fuel salt composition>
M2   <graphite composition>
M3   <INOR-8 composition>
M4   <poison composition>
MT2  grph.87t
TMP  911 911 911 911

c --- Physics ---
PHYS:N  20  0  0

c --- Optional ---
PRINT
PRDMP  2J  1
```

---

## NEXT STEPS

### Immediate Actions

1. **Review this base geometry** for dimensional accuracy
2. **Define Universe 10** (lattice universe with LAT=1)
3. **Define Universe 1-4** (unit cells)
4. **Define materials M1-M4** in data block
5. **Combine all components** into single input file

### Validation Sequence

1. **Syntax check:** Run with NPS 0 (immediate termination)
2. **Geometry plot:** Interactive plotting (mcnp6 inp=file.i ip)
3. **VOID test:** Run with VOID card, NPS 10000
4. **Initial run:** KCODE 10000 1.0 20 100 (quick check)
5. **Production run:** KCODE 50000 1.0 100 500 (benchmark quality)

### Documentation

- [ ] Create geometry plots (XY, XZ, YZ views)
- [ ] Document all assumptions
- [ ] Record simplifications and biases
- [ ] Save validation output
- [ ] Prepare Phase 3 enhancement plan

---

## REFERENCES

**Design Specifications:**
- `/home/user/mcnp-skills/MSRE_Design_Specification_Complete.md`
- `/home/user/mcnp-skills/MSRE_Geometry_Plan.md`
- `/home/user/mcnp-skills/MSRE_Lattice_Structure_Plan.md`

**MCNP Manual:**
- Chapter 3: Geometry (Cells and Surfaces)
- Chapter 4: Data Cards
- Section 5.5: Repeated Structures (LAT, FILL)

**Literature:**
- Shen et al. (2021): "Reactor Physics Benchmark of the First Criticality in the MSRE"
- ORNL-TM-728: MSRE Design and Operations Report
- ORNL-4233: Zero-Power Physics Experiments

---

**END OF INTEGRATION NOTES**

**Status:** ✓ Base geometry complete, ready for lattice integration  
**Next:** Define Universe 10 and integrate lattice
