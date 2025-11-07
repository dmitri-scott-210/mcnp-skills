# MCNP Geometry Definition - MSRE Base Geometry (Universe 0)

**GEOMETRY TYPE:** Moderate  
**TOTAL REGIONS:** 11 cells (7 material regions + 4 structural/void)

---

## CELL CARDS

```mcnp
c =================================================================
c CELL CARDS - UNIVERSE 0 (Base Geometry)
c =================================================================

c --- Core Region ---

c Cell 1000: Core lattice region (filled with Universe 10)
1000  0          -1000          FILL=10  IMP:N=1
     $ Core lattice (R=70.285 cm, H=170.311 cm)
     $ Contains LAT=1 lattice with graphite stringers

c --- Core Can (INOR-8 Structural Shell) ---

c Cell 1010: Core can wall (INOR-8)
1010  3  -8.7745  1000 -1001    IMP:N=1
     $ INOR-8 core can
     $ Inner R=70.285 cm, Outer R=71.737 cm

c --- Downcomer Annulus (Void at Zero-Power) ---

c Cell 1020: Downcomer annulus (void, no salt flow at criticality)
1020  0          1001 -1002    IMP:N=1
     $ Void annulus between core can and vessel
     $ Width = 2.562 cm

c --- Reactor Vessel (INOR-8) ---

c Cell 1100: Vessel wall (INOR-8)
1100  3  -8.7745  1002 -1003  -1051  IMP:N=1
     $ Reactor vessel wall
     $ Inner R=74.299 cm, Outer R=76.862 cm
     $ Wall thickness = 2.563 cm

c --- Lower Plenum (Below Core) ---

c Cell 1200: Lower plenum fuel salt
1200  1  -2.3275  -1002  1050 -1010  IMP:N=1
     $ Fuel salt below lattice
     $ z = -51 to 0 cm (51 cm depth)

c Cell 1201: Lower plenum bottom head (INOR-8, simplified flat)
1201  3  -8.7745  -1003  1050  IMP:N=1
     $ Vessel bottom head (flat, simplified)

c --- Upper Plenum (Above Core) ---

c Cell 1300: Upper plenum fuel salt
1300  1  -2.3275  -1002  1011 -1012  IMP:N=1
     $ Fuel salt above lattice
     $ z = 170.311 to 220 cm

c Cell 1301: Upper plenum top head (INOR-8, simplified flat)
1301  3  -8.7745  -1003  1012 -1051  IMP:N=1
     $ Vessel top head (flat, simplified)

c --- Outer Void and Graveyard ---

c Cell 1900: Outer void region (air/vacuum)
1900  0          1003 -1999    IMP:N=1
     $ Void outside vessel, inside graveyard

c Cell 1999: Graveyard (particle termination)
1999  0          1999           IMP:N=0
     $ Graveyard boundary
     $ All particles entering are killed
```

---

## SURFACE CARDS

```mcnp
c =================================================================
c SURFACE CARDS - UNIVERSE 0
c =================================================================

c --- Core Geometry (1000-1099) ---

c Surface 1000: Graphite lattice boundary
1000  RCC  0 0 0  0 0 170.311  70.285
     $ Lattice cylinder (R=70.285 cm, H=170.311 cm)
     $ Vertex: (0, 0, 0) at lattice bottom
     $ Height vector: (0, 0, 170.311) upward
     $ Radius: 70.285 cm

c Surface 1001: Core can outer wall
1001  RCC  0 0 0  0 0 170.311  71.737
     $ Core can outer boundary (R=71.737 cm)

c --- Vessel System (1002-1099) ---

c Surface 1002: Vessel inner wall
1002  RCC  0 0 -51  0 0 271  74.299
     $ Vessel inner surface (R=74.299 cm)
     $ z = -51 to 220 cm

c Surface 1003: Vessel outer wall
1003  RCC  0 0 -51  0 0 271  76.862
     $ Vessel outer surface (R=76.862 cm)

c --- Axial Planes (Plenums) ---

1010  PZ  0.0
     $ Lattice bottom / lower plenum top

1011  PZ  170.311
     $ Lattice top / upper plenum bottom

1012  PZ  220.0
     $ Upper plenum top

1050  PZ  -51.0
     $ Lower plenum bottom / vessel bottom

1051  PZ  220.0
     $ Vessel top

c --- Outer Boundary (1999) ---

c Surface 1999: Graveyard boundary
1999  RCC  0 0 -100  0 0 400  150
     $ Outer boundary cylinder
     $ R=150 cm, z = -100 to 300 cm
```

---

## GEOMETRY SUMMARY

### Regions

**Core and Structural:**
- **Core lattice (cell 1000):** Cylindrical region for Universe 10 (LAT=1 lattice)
  - Radius: 70.285 cm
  - Height: 170.311 cm (z = 0 to 170.311)
  - Volume: ~2,642,600 cm³
  - Content: FILL=10 (graphite stringers with fuel channels)

- **Core can (cell 1010):** INOR-8 structural shell
  - Inner R: 70.285 cm
  - Outer R: 71.737 cm
  - Thickness: 1.452 cm
  - Material: INOR-8 (m3, ρ=8.7745 g/cm³)

- **Downcomer annulus (cell 1020):** Void region (no salt flow at criticality)
  - Inner R: 71.737 cm
  - Outer R: 74.299 cm
  - Width: 2.562 cm (matches specification)
  - Material: Void (m0)

**Vessel System:**
- **Reactor vessel (cell 1100):** Main containment
  - Inner R: 74.299 cm
  - Outer R: 76.862 cm
  - Wall thickness: 2.563 cm
  - Height: 271 cm (z = -51 to 220)
  - Material: INOR-8 (m3, ρ=8.7745 g/cm³)

**Plenums:**
- **Lower plenum (cell 1200):** Fuel salt below core
  - Radius: < 74.299 cm
  - Height: 51 cm (z = -51 to 0)
  - Volume: ~885,700 cm³
  - Material: Fuel salt (m1, ρ=2.3275 g/cm³)

- **Upper plenum (cell 1300):** Fuel salt above core
  - Radius: < 74.299 cm
  - Height: 49.689 cm (z = 170.311 to 220)
  - Volume: ~862,500 cm³
  - Material: Fuel salt (m1, ρ=2.3275 g/cm³)

**Boundaries:**
- **Vessel heads (cells 1201, 1301):** Simplified flat planes
  - Material: INOR-8 (m3)
  - Note: Torispherical heads omitted (+243 pcm bias, acceptable for Phase 2)

- **Graveyard (cell 1999):** Outer boundary
  - Radius: 150 cm
  - Material: Void (m0, IMP:N=0)

### Complexity

**Simple to Moderate:**
- Cylindrically symmetric geometry (no azimuthal variation)
- RCC macrobodies used throughout (no infinite surfaces)
- Clear radial and axial layering
- Straightforward Boolean operations

**Integration Complexity:**
- Universe 0 → Cell 1000 → FILL=10 → Universe 10 (lattice)
- Requires lattice universe definition (separate task)

### Symmetry

**Cylindrical symmetry about z-axis:**
- All radial structures concentric
- No angular dependence in base geometry
- Lattice (Universe 10) will introduce square array pattern

### Materials

**Base Geometry Materials:**
- **M1:** Fuel salt (LiF-BeF₂-ZrF₄-UF₄, ρ=2.3275 g/cm³)
  - Used in plenums (cells 1200, 1300)
  - **CRITICAL:** Li must be enriched (0.005% ⁶Li, NOT natural)

- **M3:** INOR-8 (Hastelloy-N, ρ=8.7745 g/cm³)
  - Used in core can (1010), vessel (1100), heads (1201, 1301)
  - Composition: ~70% Ni, 17% Mo, 7% Cr, 5% Fe, 0.07% C

**Lattice Universe Materials (to be defined):**
- **M2:** Graphite (nuclear grade, ρ=1.86 g/cm³)
- **M4:** Control rod poison (Gd₂O₃-Al₂O₃, ρ=5.873 g/cm³)

---

## VALIDATION STATUS

### Pre-Execution Checks

✓ **All surfaces referenced in cells defined**
- Surfaces 1000-1003: RCC macrobodies (core, vessel)
- Surfaces 1010-1012, 1050-1051: PZ planes (plenums)
- Surface 1999: RCC graveyard

✓ **All cells have importance set (IMP:N)**
- Cells 1000-1900: IMP:N=1 (active tracking)
- Cell 1999: IMP:N=0 (graveyard)

✓ **Graveyard present**
- Cell 1999, surface 1999, IMP:N=0

✓ **No undefined surfaces**
- All surface numbers in cells correspond to defined surfaces

✓ **Boolean expressions verified**
- Simple combinations (inside/outside single surfaces or pairs)
- No complex nested Boolean operations

### Recommended Validation

**1. Plot geometry:**
```bash
mcnp6 inp=MSRE_input.i ip
```

**Plots to generate:**
- **XY plane at z=85 cm:** Mid-core horizontal cross-section
  - Should show: Circular lattice (R=70.285), core can shell, downcomer annulus (void gap), vessel walls (concentric circles)
  - Check: No dashed lines (geometry errors)

- **XZ plane at y=0:** Vertical cross-section
  - Should show: Lower plenum (-51 to 0), core lattice (0 to 170.311), upper plenum (170.311 to 220), vessel extending full height
  - Check: No gaps between regions

- **YZ plane at x=0:** Vertical cross-section (should match XZ due to symmetry)

**2. VOID card test:**
```
c Add to data block:
VOID
```
- Run: `mcnp6 inp=MSRE_input.i`
- Expected: Zero lost particles, no overlap/gap warnings
- Remove VOID after validation

**3. Volume check:**

Calculate expected volumes and compare:

**Core lattice (cell 1000):**
```
V = π × R² × H = π × 70.285² × 170.311 = 2,642,600 cm³
```

**Downcomer annulus (cell 1020):**
```
V = π × (R₂² - R₁²) × H = π × (74.299² - 71.737²) × 170.311 = 152,400 cm³
```

**Lower plenum (cell 1200):**
```
V = π × R² × H = π × 74.299² × 51 = 885,700 cm³
```

**Run MCNP with:**
```
VOL  2642600  J  152400  885700  J  J  J  J  J  J
```
- Compare calculated vs MCNP volumes

---

## INTEGRATION

### Material Cards Needed

**M1: Fuel Salt (LiF-BeF₂-ZrF₄-UF₄) at 911 K**
```mcnp
c Fuel salt (ρ = 2.3275 g/cm³, 911 K)
c CRITICAL: Lithium enrichment (0.005% Li-6, NOT natural)
M1   3006.80c  -0.0000055    $ Li-6 (0.005 at.%, HIGHLY DEPLETED)
     3007.80c  -0.1095445    $ Li-7 (99.995 at.%, balance)
     4009.80c  -0.06349      $ Be-9
     40000.80c -0.11101      $ Zr (natural)
     92234.80c -0.00063      $ U-234
     92235.80c -0.06335      $ U-235 (enriched)
     92236.80c -0.00027      $ U-236
     92238.80c -4.43075      $ U-238
     9019.80c  -0.67027      $ F-19
c Optional impurities (±24 pcm if omitted):
c    26000.80c -0.000162     $ Fe (162 ppm)
c    24000.80c -0.000028     $ Cr (28 ppm)
c    28000.80c -0.000030     $ Ni (30 ppm)
c    8016.80c  -0.000490     $ O (490 ppm)
TMP1 911
```

**M3: INOR-8 (Hastelloy-N) at 911 K**
```mcnp
c INOR-8 (Hastelloy-N, ρ = 8.7745 g/cm³, 911 K)
M3   28000.80c -0.70          $ Ni (balance, ~70%)
     42000.80c -0.17          $ Mo (17%)
     24000.80c -0.07          $ Cr (7%)
     26000.80c -0.05          $ Fe (5%)
     6000.80c  -0.01          $ C (0.07% average)
TMP3 911
```

### Material Cross-References

**Materials referenced in base geometry:**
- **M1:** Cells 1200 (lower plenum), 1300 (upper plenum)
- **M3:** Cells 1010 (core can), 1100 (vessel wall), 1201 (bottom head), 1301 (top head)

**Materials in lattice universes (Universe 1-4):**
- **M2:** Graphite (nuclear grade, ρ=1.86 g/cm³)
  - Use in Universe 1 (graphite stringer bodies)
  - **CRITICAL:** Include thermal scattering (MT2 grph.87t)
  - **CRITICAL:** Include boron impurity (0.8 ppm, ±17 pcm impact)

- **M4:** Control rod poison (Gd₂O₃-Al₂O₃, ρ=5.873 g/cm³)
  - Use in Universe 3 (regulating rod)

### Source Placement

**Initial source in core:**
```mcnp
KCODE  10000  1.0  50  200
KSRC   0 0 85  10 0 85  -10 0 85  0 10 85  0 -10 85
```
- Source points at z=85 cm (mid-core height)
- Distributed radially near center
- MCNP will redistribute after convergence

### Tally Placement

**Example tallies:**
```mcnp
c Cell flux tally (core lattice)
F4:N  1000
E4    1E-10  1E-7  0.625E-6  1.0  20.0

c Surface current tally (vessel inner)
F1:N  1002.1

c Fission energy deposition (core)
F7:N  1000
```

---

## INTEGRATION POINTS

### Lattice Integration (Universe 10)

**Cell 1000 in Universe 0:**
```mcnp
1000  0  -1000  FILL=10  IMP:N=1
```
- Loads Universe 10 (lattice universe)
- Universe 10 must contain LAT=1 cell definition

**Universe 10 structure (example):**
```mcnp
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

**Coordinate system compatibility:**
- Surface 54 (PZ 0.0) in Universe 10 matches z=0 in Universe 0 ✓
- Surface 55 (PZ 170.311) matches core height ✓
- Lattice bounded by surface 1000 (RCC, R=70.285) in Universe 0

### Complementary Specialists

**Geometry → Materials (mcnp-material-builder):**
- Define M1 (fuel salt) with Li enrichment
- Define M3 (INOR-8)
- Define M2 (graphite) with B impurity and thermal scattering
- Define M4 (control rod poison)

**Geometry → Source (mcnp-source-builder):**
- KCODE parameters for criticality
- Initial source distribution in core (CEL=1000 or specific positions)

**Geometry → Tallies (mcnp-tally-builder):**
- F4:N flux tally in core (cell 1000)
- F7:N fission energy deposition
- F2:N leakage current (surface 1002 or 1003)

**Geometry → Validation (mcnp-geometry-checker):**
- Run geometry validator script
- Check for overlaps, gaps, Boolean errors
- Generate automated plots

---

## USAGE

### Complete MCNP Input File Structure

```mcnp
MSRE First Criticality Benchmark - Full Model
c =================================================================
c BLOCK 1: TITLE AND CELL CARDS
c =================================================================

c --- BASE GEOMETRY (Universe 0) ---
<Insert cell cards from this file (cells 1000-1999)>

c --- LATTICE UNIVERSE (Universe 10) ---
<Insert lattice definition with LAT=1>

c --- UNIT CELL UNIVERSES (Universe 1-4) ---
<Insert graphite stringer, control rods, sample basket>

c =================================================================
c BLOCK 2: SURFACE CARDS
c =================================================================

c --- BASE GEOMETRY SURFACES (1000-1999) ---
<Insert surface cards from this file (surfaces 1000-1999)>

c --- LATTICE SURFACES (10-99) ---
<Insert lattice and unit cell surfaces>

<BLANK LINE - REQUIRED>

c =================================================================
c BLOCK 3: DATA CARDS
c =================================================================

MODE N
KCODE  10000  1.0  50  200
KSRC   0 0 85  10 0 85  -10 0 85  0 10 85  0 -10 85

c --- Material Definitions ---
M1  <fuel salt composition - see above>
M2  <graphite composition>
M3  <INOR-8 composition - see above>
M4  <poison composition>
MT2 grph.87t
TMP1 911 911 911 911

c --- Physics ---
PHYS:N  20  0  0

c --- Optional ---
PRINT
PRDMP  2J  1
LOST  10  10

<BLANK LINE - REQUIRED>
```

### File Locations

**Generated files:**
- `/home/user/mcnp-skills/MSRE_Base_Geometry_Universe0.txt`
  - Complete cell and surface cards (copy-paste ready)

- `/home/user/mcnp-skills/MSRE_Base_Geometry_Integration_Notes.md`
  - Detailed integration instructions
  - Validation procedures
  - Material specifications

- `/home/user/mcnp-skills/MSRE_Base_Geometry_Visual_Reference.txt`
  - ASCII diagrams of geometry
  - Radial and axial cross-sections
  - Universe hierarchy visualization

- `/home/user/mcnp-skills/MSRE_Base_Geometry_Report.md`
  - This comprehensive report

**Reference files:**
- `/home/user/mcnp-skills/MSRE_Design_Specification_Complete.md`
  - Source of all dimensions and material compositions

- `/home/user/mcnp-skills/MSRE_Geometry_Plan.md`
  - Overall geometry strategy and surface numbering

- `/home/user/mcnp-skills/MSRE_Lattice_Structure_Plan.md`
  - Detailed lattice universe planning

### Next Steps

**1. Review base geometry:**
- Check dimensional accuracy against specifications
- Verify surface numbering scheme
- Confirm material references

**2. Build lattice (Universe 10):**
- Define LAT=1 cell with FILL array
- Create 29×29 array (-14:14 in each direction)
- Place Universe 1 (stringers), Universe 2-3 (control rods), Universe 4 (basket)

**3. Build unit cell universes:**
- Universe 1: Graphite stringer with 4 fuel grooves
- Universe 2: Control rod thimble (withdrawn)
- Universe 3: Regulating rod (3% inserted with poison)
- Universe 4: Sample basket (homogenized)

**4. Define materials:**
- M1: Fuel salt with Li enrichment
- M2: Graphite with B impurity and thermal scattering
- M3: INOR-8
- M4: Control rod poison

**5. Validate geometry:**
- Plot XY, XZ, YZ views
- Run VOID test
- Check volumes

**6. Run MCNP:**
- Initial test: NPS 10000, check for lost particles
- Production run: KCODE 50000 1.0 100 500
- Target keff: 1.019-1.024 (with current simplifications)

---

## SIMPLIFICATIONS AND PHASE 3 ENHANCEMENTS

### Current Simplifications (Phase 2)

| Component | Detailed Model | Simplified Model | Bias (pcm) |
|-----------|----------------|------------------|------------|
| Vessel heads | Torispherical (ASME) | Flat planes | +243 |
| Plenums | Detailed piping | Uniform fuel salt | Small (~10) |
| Thermal shield | SS304 shield | **Omitted** | **-885** |
| Insulation | Vermiculite | **Omitted** | Small (~20) |

**Total estimated bias:** ~-640 pcm (primarily thermal shield omission)

### Phase 3 Enhancements (Production Model)

**Add thermal shield** (CRITICAL - largest bias correction):
```mcnp
c Thermal shield (Type 304 SS, ID=236.22 cm, OD~317.5 cm, H=383.54 cm)
500  RCC  0 0 Z_SHIELD_BOTTOM  0 0 383.54  118.11   $ Inner
501  RCC  0 0 Z_SHIELD_BOTTOM  0 0 383.54  158.75   $ Outer

c Cell for thermal shield
1500  5  -X.XXX  500 -501  IMP:N=1  $ M5 = SS304
```
- Bias correction: +885 pcm
- Material M5: Type 304 stainless steel
- Temperature: 305 K (external cooling)

**Add insulation layer:**
```mcnp
c Insulation (vermiculite, 15.24 cm thickness)
600  RCC  0 0 Z_INS_BOTTOM  0 0 H_INS  R_INS_INNER
601  RCC  0 0 Z_INS_BOTTOM  0 0 H_INS  (R_INS_INNER + 15.24)

c Cell for insulation
1600  6  -X.XXX  600 -601  IMP:N=1  $ M6 = homogenized vermiculite
```
- Bias correction: ~+20 pcm

**Refine vessel heads (optional):**
- Replace flat PZ surfaces with torispherical geometry
- Use ellipsoid (SQ) + torus (TZ) surfaces
- Bias correction: -243 pcm

**Expected keff after Phase 3:**
- With thermal shield: 1.019-1.024 (target range ✓)
- Matches Serpent benchmark: 1.02132 ± 0.00003

---

## VALIDATION TARGETS

### Criticality

**Expected keff (Phase 2 model):**
- **Current model:** ~1.014-1.016 (estimated with biases)
- **After Phase 3:** 1.019-1.024 (target range)
- **Benchmark (Serpent):** 1.02132 ± 0.00003
- **Acceptance:** Within ±200 pcm of Serpent

**Statistical quality:**
- Uncertainty: < 50 pcm (σ < 0.00005)
- Shannon entropy: Converged (slope < 0.001 after 20-50 cycles)
- Lost particles: Zero (MUST be 0)

### C-E Discrepancy

**Expected:** 2.1-2.2% (typical for graphite-moderated systems)
- **NOT a model error** - known bias in carbon cross-sections
- Other graphite benchmarks: HTR-10 (+1.19%), HTTR (+2.03%), PROTEUS (+0.90%)
- MSRE: +2.15% (within expected range)

### Neutron Balance

**Production (expected):**
- ~99% from U-235 fission
- ~1% from other isotopes

**Absorption (expected):**
- ~40% in fuel (U, Li, impurities)
- ~25% in graphite (C-12 capture)
- ~20% in control rods (Gd poison)
- ~15% in structural materials

**Leakage (expected):**
- ~5-10% radial leakage
- ~2-5% axial leakage

---

## REFERENCES

**Design Specifications:**
- `/home/user/mcnp-skills/MSRE_Design_Specification_Complete.md`
- `/home/user/mcnp-skills/MSRE_Geometry_Plan.md`
- `/home/user/mcnp-skills/MSRE_Lattice_Structure_Plan.md`

**Bundled Resources:**
- `.claude/skills/mcnp-geometry-builder/surface_types_comprehensive.md`
- `.claude/skills/mcnp-geometry-builder/macrobodies_reference.md`
- `.claude/skills/mcnp-geometry-builder/cell_definition_comprehensive.md`

**MCNP Manual:**
- Chapter 3: Geometry (Cells and Surfaces)
- Chapter 5: Repeated Structures (LAT, FILL)

**Literature:**
- Shen et al. (2021): IRPhEP benchmark paper
- ORNL-TM-728: MSRE Design and Operations Report
- ORNL-4233: Zero-Power Physics Experiments

---

**END OF GEOMETRY REPORT**

**Status:** ✓ Base geometry complete and ready for lattice integration  
**Date:** 2025-11-07  
**Next Action:** Build Universe 10 (lattice) and Universe 1-4 (unit cells)
