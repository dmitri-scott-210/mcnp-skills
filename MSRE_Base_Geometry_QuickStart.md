# MSRE Base Geometry - Quick Start Guide

**Status:** ✓ Ready for lattice integration  
**Files created:** 2025-11-07

---

## FILES CREATED

### 1. Cell and Surface Cards (Ready to Use)
**File:** `/home/user/mcnp-skills/MSRE_Base_Geometry_Universe0.txt`
- Complete MCNP geometry cards
- 11 cells (Universe 0)
- 9 surfaces (RCC macrobodies + PZ planes)
- Copy-paste ready for MCNP input file

### 2. Integration Instructions
**File:** `/home/user/mcnp-skills/MSRE_Base_Geometry_Integration_Notes.md`
- Detailed integration with lattice (Universe 10)
- Material specifications (M1, M3)
- Validation procedures
- Troubleshooting guide

### 3. Visual Reference
**File:** `/home/user/mcnp-skills/MSRE_Base_Geometry_Visual_Reference.txt`
- ASCII diagrams (radial, axial cross-sections)
- Universe hierarchy visualization
- Dimension summary tables
- Coordinate system reference

### 4. Comprehensive Report
**File:** `/home/user/mcnp-skills/MSRE_Base_Geometry_Report.md`
- Complete geometry documentation
- Validation targets
- Phase 3 enhancement plan
- All integration points

### 5. This Quick Start
**File:** `/home/user/mcnp-skills/MSRE_Base_Geometry_QuickStart.md`

---

## GEOMETRY OVERVIEW

### Radial Structure (Concentric Cylinders)

```
  R (cm)      Component              Material
  ------      -------------------    ----------
  0.0         Core center            (lattice)
  70.285      Lattice boundary       FILL=10
  71.737      Core can outer         INOR-8
  74.299      Vessel inner           (void annulus)
  76.862      Vessel outer           INOR-8
  150.0       Graveyard boundary     Void (IMP=0)
```

### Axial Structure (Vertical Layers)

```
  z (cm)      Component              Material
  ------      -------------------    ----------
  -51         Vessel bottom          INOR-8
  0           Lattice bottom         FILL=10
  170.311     Lattice top            FILL=10
  220         Vessel top             INOR-8
```

---

## INTEGRATION CHECKLIST

### Step 1: Copy Base Geometry
```bash
# Cell cards (Block 1)
cat /home/user/mcnp-skills/MSRE_Base_Geometry_Universe0.txt
# (Copy cells 1000-1999 to your input file)

# Surface cards (Block 2)
# (Copy surfaces 1000-1999 to your input file)
```

### Step 2: Add Lattice (Universe 10)
```mcnp
c Universe 10: Lattice definition
100  0  -50 51 -52 53 -54 55  U=10  LAT=1  IMP:N=1  &
     FILL=-14:14 -14:14 0:0  <YOUR_FILL_ARRAY>

c Lattice element boundaries (5.084 cm pitch)
50  PX  -2.542
51  PX   2.542
52  PY  -2.542
53  PY   2.542
54  PZ   0.0
55  PZ  170.311
```

### Step 3: Add Unit Cell Universes (1-4)
- Universe 1: Graphite stringer with fuel grooves
- Universe 2: Control rod (withdrawn)
- Universe 3: Regulating rod (3% inserted)
- Universe 4: Sample basket (homogenized)

### Step 4: Define Materials (Data Block)
```mcnp
MODE N
KCODE  10000  1.0  50  200
KSRC   0 0 85

c Fuel salt (CRITICAL: Li enrichment, NOT natural)
M1  3006.80c -0.0000055  3007.80c -0.1095445  ...
TMP1 911

c Graphite (CRITICAL: include B impurity and thermal scattering)
M2  6000.80c 1.0  5010.80c 8.0E-7  5011.80c 3.2E-6
MT2 grph.87t
TMP2 911

c INOR-8 (Hastelloy-N)
M3  28000.80c -0.70  42000.80c -0.17  ...
TMP3 911

c Control rod poison
M4  64000.80c -0.6113  13027.80c -0.1588  8016.80c -0.2299
TMP4 911
```

### Step 5: Validate Geometry
```bash
# Plot mode
mcnp6 inp=MSRE_input.i ip

# VOID test (add VOID to data block)
mcnp6 inp=MSRE_input.i

# Check output for:
# - Zero lost particles
# - No overlap warnings
# - No gap warnings
```

---

## KEY DIMENSIONS (Hot, 911 K)

| Parameter | Value (cm) | Surface | Cell |
|-----------|------------|---------|------|
| **Radial** |
| Lattice radius | 70.285 | 1000 | 1000 |
| Core can outer | 71.737 | 1001 | 1010 |
| Vessel inner | 74.299 | 1002 | 1020,1100 |
| Vessel outer | 76.862 | 1003 | 1100 |
| **Axial** |
| Lower plenum bottom | -51 | 1050 | 1200,1201 |
| Lattice bottom | 0 | 1010,54 | 1000 |
| Lattice top | 170.311 | 1011,55 | 1000 |
| Vessel top | 220 | 1012,1051 | 1300,1301 |
| **Thicknesses** |
| Core can | 1.452 | - | - |
| Downcomer width | 2.562 | - | - |
| Vessel wall | 2.563 | - | - |

---

## CRITICAL REQUIREMENTS

### Materials

1. **Fuel Salt (M1):**
   - ⚠️ **Li must be enriched: 0.005% ⁶Li (NOT natural 7.5%)**
   - Natural Li causes ~172 pcm error (2nd largest uncertainty)
   - Use 3006.80c and 3007.80c explicitly

2. **Graphite (M2):**
   - ⚠️ **Include boron impurity: 0.8 ppm (±17 pcm impact)**
   - ⚠️ **Use thermal scattering: MT2 grph.87t**
   - ⚠️ **Temperature: TMP2 911**

3. **All Materials:**
   - Temperature: 911 K (TMP cards)
   - Density: Negative for g/cm³ units
   - ENDF/B-VII.1 library (.80c suffix)

### Geometry

1. **Coordinate System:**
   - Origin: (0,0,0) at bottom center of lattice
   - z=0 at lattice bottom
   - All hot dimensions (911 K)

2. **Integration:**
   - Cell 1000: Must have FILL=10
   - Universe 10: Must contain LAT=1 cell
   - Surface 54 (Universe 10) matches z=0 (Universe 0)
   - Surface 55 (Universe 10) matches z=170.311

3. **Validation:**
   - Zero lost particles (MANDATORY)
   - VOID test passes
   - Geometry plots show no dashed lines

---

## EXPECTED RESULTS

### Phase 2 (Current Model)

**keff:** ~1.014-1.016
- Simplified vessel heads: +243 pcm
- Omitted thermal shield: -885 pcm
- Net bias: ~-640 pcm

**Acceptance:** Model runs without errors, zero lost particles

### Phase 3 (Production Model)

**keff:** 1.019-1.024 (target range)
- Add thermal shield (+885 pcm correction)
- Within ±200 pcm of Serpent benchmark (1.02132)

**C-E discrepancy:** 2.1-2.2% (expected for graphite systems)

---

## TROUBLESHOOTING

### "Lost particles" Error
- **Cause:** Geometry gap or overlap
- **Fix:** Run VOID test, plot geometry, check cell boundaries
- **Tool:** `python scripts/geometry_validator.py input.inp`

### "Lattice not visible" in Plots
- **Cause:** Universe 10 not defined or FILL parameter missing
- **Fix:** Verify Universe 10 exists, check `FILL=10` on cell 1000

### keff Too Low (< 1.01)
- **Cause:** Likely natural Li (NOT enriched)
- **Fix:** Use 3006.80c (0.005%) + 3007.80c (99.995%), NOT 3000.80c

### keff Too High (> 1.03)
- **Cause:** Control rods missing or positioned incorrectly
- **Fix:** Verify Universe 3 (regulating rod) in FILL array at correct position

---

## NEXT STEPS

### Immediate (Build Lattice)

1. Define Universe 10 (LAT=1 lattice container)
2. Define Universe 1 (graphite stringer unit cell)
3. Define Universe 2, 3 (control rod thimbles)
4. Define Universe 4 (sample basket)
5. Generate FILL array (29×29, ~593 positions in circle)

### Near-Term (Validation)

1. Combine all geometry into single input file
2. Define materials M1-M4 in data block
3. Plot geometry (XY, XZ, YZ views)
4. Run VOID test
5. Initial MCNP run (KCODE 10000 1.0 20 100)

### Long-Term (Production)

1. Increase statistics (KCODE 50000 1.0 100 500)
2. Add thermal shield (Phase 3 enhancement)
3. Refine vessel heads if needed
4. Compare to benchmark (target keff = 1.02132)
5. Document results

---

## CONTACT AND SUPPORT

**Documentation:**
- Design spec: `MSRE_Design_Specification_Complete.md`
- Geometry plan: `MSRE_Geometry_Plan.md`
- Lattice plan: `MSRE_Lattice_Structure_Plan.md`
- Integration notes: `MSRE_Base_Geometry_Integration_Notes.md`
- Full report: `MSRE_Base_Geometry_Report.md`

**Automation Tools:**
- Geometry validator: `scripts/geometry_validator.py`
- Plot helper: `scripts/geometry_plotter_helper.py`

**Skills:**
- Geometry: `mcnp-geometry-builder`
- Materials: `mcnp-material-builder`
- Lattice: `mcnp-lattice-builder`
- Validation: `mcnp-geometry-checker`

---

**END OF QUICK START**

**Status:** ✓ Base geometry ready  
**Action:** Build lattice (Universe 10) and integrate
