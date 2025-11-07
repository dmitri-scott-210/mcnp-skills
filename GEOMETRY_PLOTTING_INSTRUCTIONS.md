# MSRE Phase 2 Model - Geometry Plotting Instructions

## Status: Phase 2 Steps 2.2-2.4 COMPLETE ✓

All materials defined, lattice constructed, base geometry built, and integrated into a complete MCNP input file.

---

## Complete MCNP Input File

**Location:** `/home/user/mcnp-skills/MSRE_Complete_Phase2_Model.inp`

**Contents:**
- Universe 0: Base geometry (vessel, reflector, plenums)
- Universe 10: LAT=1 lattice container (29×29 array)
- Universe 1: Graphite stringer (589 positions)
- Universe 2: Control rods withdrawn (2 positions at (-1,+1) and (+1,+1))
- Universe 3: Regulating rod 3% inserted (1 position at (-1,-1))
- Universe 4: Sample basket (1 position at (+1,-1)) ✓ USER CONFIRMED
- Materials m1-m5 (all defined with correct densities)
- KCODE source definition (10000 particles/cycle, 50 skip, 200 active)

---

## Critical Corrections Applied

### Cell 5 Boolean Error Fixed

**Original (INVALID):**
```mcnp
5   2  -1.86    50 -51 52 -53 -54 55      &
               10 -11 -12 13               &  $ Would fail
               16 -17 -18 19               &
```

**Corrected (VALID):**
```mcnp
5   2  -1.86    50 -51 52 -53 -54 55  #1 #2 #3 #4  U=1
```

Using complement operator `#` to exclude fuel grooves.

### Material m5 Homogenized Density Calculated

**Placeholder:** -3.500 g/cm³
**Calculated:** -2.6206 g/cm³ (17.4% graphite + 5.8% INOR-8 + 76.8% fuel salt)

---

## Geometry Plotting Commands

### Method 1: Interactive Plotter (Recommended for Verification)

```bash
mcnp6 inp=MSRE_Complete_Phase2_Model.inp ip tasks 1
```

Or if MCNP is at a specific location:
```bash
/path/to/mcnp6 inp=MSRE_Complete_Phase2_Model.inp ip tasks 1
```

For Windows:
```cmd
"C:\path\to\mcnp6.exe" inp=MSRE_Complete_Phase2_Model.inp ip tasks 1
```

### Method 2: Batch Plot Generation

```bash
mcnp6 inp=MSRE_Complete_Phase2_Model.inp tasks 1 <<EOF
plot
XY 85
LABEL 1 1 1
EXTENT 150
COLOR 1 RED
COLOR 2 GREEN
COLOR 3 BLUE
END
plot
XZ 0
LABEL 1 1 1
EXTENT 150 250
END
plot
YZ 0
LABEL 1 1 1
EXTENT 150 250
END
END
EOF
```

---

## Critical Plots to Generate

### 1. XY Plane at z=85 cm (Mid-Height)

**Command in plotter:**
```
plot
BASIS XY
ORIGIN 0 0 85
EXTENT 150
LABEL 1 1 1
```

**What to verify:**
- [ ] Circular core lattice (R=70.285 cm) visible
- [ ] ~593 lattice positions within core boundary
- [ ] Central pattern correct:
  - (0,0): Universe 1 (graphite, green)
  - (-1,+1): Universe 2 (control rod, blue)
  - (+1,+1): Universe 2 (control rod, blue)
  - (-1,-1): Universe 3 (regulating rod, yellow)
  - (+1,-1): Universe 4 (sample basket, orange) ✓
- [ ] Core can (INOR-8) at R=70.285-71.737 cm
- [ ] Void downcomer at R=71.737-74.299 cm
- [ ] Vessel wall (INOR-8) at R=74.299-76.862 cm
- [ ] No overlaps (no red error markers)
- [ ] No gaps (no missing regions)

### 2. XZ Plane at y=0 (Vertical Cross-Section)

**Command in plotter:**
```
plot
BASIS XZ
ORIGIN 0 0 85
EXTENT 150 250
```

**What to verify:**
- [ ] Lower plenum (fuel salt) z=-51 to 0 cm
- [ ] Core lattice (graphite + fuel) z=0 to 170.311 cm
- [ ] Upper plenum (fuel salt) z=170.311 to 220 cm
- [ ] Vessel extends full height
- [ ] No axial gaps or overlaps

### 3. YZ Plane at x=0 (Another Vertical Cross-Section)

Same as XZ, verifies symmetry.

---

## Interactive Plotter Navigation

### Basic Commands

| Command | Action |
|---------|--------|
| `plot` | Start plot |
| `basis XY` | Set view plane (XY, XZ, YZ) |
| `origin X Y Z` | Set plot center |
| `extent W` or `extent W H` | Set plot dimensions (cm) |
| `label 1 1 1` | Show cell/surface/universe numbers |
| `color N colorname` | Set material N color |
| `zoom 2` | Zoom in by factor |
| `zoom 0.5` | Zoom out |
| `PX +10` | Move right 10 cm |
| `PX -10` | Move left 10 cm |
| `PY +10` | Move up 10 cm |
| `PZ +10` | Move into page 10 cm |
| `end` | Finish current plot |
| `END` (uppercase) | Exit plotter |

### Recommended Sequence

1. Start with XY at z=85 (mid-height)
2. Verify central pattern matches user confirmation
3. Check for lattice symmetry
4. Switch to XZ at y=0 (vertical slice)
5. Verify axial structure (plenums, core)
6. Generate postscript files for documentation

---

## Expected Visual Results

### Color Coding (default)

| Material | Number | Component | Expected Color |
|----------|--------|-----------|----------------|
| Fuel salt | m1 | Plenums, grooves | Yellow/Orange |
| Graphite | m2 | Stringers, reflector | Green |
| INOR-8 | m3 | Vessel, core can | Blue |
| Poison | m4 | Regulating rod | Red |
| Homogenized | m5 | Sample basket | Purple |
| Void | m0 | Downcomer | White |

### XY at z=85 cm (Expected Pattern)

```
             Outer boundary (R=150 cm)
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      │   Void       │   Void       │
      │              │              │
      │     ┌────────┼────────┐     │
      │     │ Vessel │ Vessel │     │
      │     │   ┌────┼────┐   │     │
      │     │   │Core│Core│   │     │
      │     │   │ ┌──┼──┐ │   │     │
      │     │   │ │Lat│  │ │   │     │
      │     │   │ │tice  │ │   │     │
      │     │   │ │  ★  │ │   │     │  ← Central pattern
      │     │   │ └──┼──┘ │   │     │
      │     │   └────┼────┘   │     │
      │     └────────┼────────┘     │
      └──────────────┼──────────────┘
                     │
         593 lattice positions visible
         in circular core (R=70.285 cm)

Central ★ pattern (i,j indices at z=85):
  (-1,+1): U2 (control rod)    (+1,+1): U2 (control rod)
              (0,0): U1 (graphite - center)
  (-1,-1): U3 (regulating)     (+1,-1): U4 (basket) ✓
```

---

## Validation Checklist

### Pre-MCNP Run

- [ ] **Geometry plots generated** (XY, XZ, YZ)
- [ ] **Central pattern verified** against user confirmation
- [ ] **No overlaps** (no red error markers in plots)
- [ ] **No gaps** (all space defined)
- [ ] **589 graphite stringers** visible in lattice
- [ ] **4 special positions** at diagonal square
- [ ] **Circular boundary** R=70.285 cm clean

### Syntax Validation (Optional - already checked by agents)

```bash
mcnp6 inp=MSRE_Complete_Phase2_Model.inp tasks 1
```

Check output for:
- "run terminated when it had used 0 minutes" (syntax OK)
- No "bad trouble" messages
- No "fatal error" messages

### VOID Test (Mandatory Before Production Run)

Add to data block:
```
VOID
```

Run:
```bash
mcnp6 inp=MSRE_Complete_Phase2_Model.inp tasks 1
```

**Expected:** Zero lost particles, no geometry errors

---

## Next Steps After Plotting

### If Geometry Looks Correct:

1. **Remove VOID card** (if added)
2. **Run initial MCNP calculation:**
   ```bash
   mcnp6 inp=MSRE_Complete_Phase2_Model.inp outp=msre_phase2.out
   ```
3. **Monitor output:**
   - keff convergence
   - Shannon entropy slope
   - Lost particles (MUST be zero)
4. **Expected keff:** 1.014-1.016 (Phase 2, before thermal shield)

### If Geometry Has Issues:

1. **Document errors** (screenshot plots, note cell numbers)
2. **Launch appropriate validator:**
   - Overlaps: `mcnp-geometry-checker`
   - Cell references: `mcnp-cell-checker`
   - Fatal errors: `mcnp-fatal-error-debugger`
3. **Iterate until clean**

---

## Deliverables Summary

### Primary File
- **`MSRE_Complete_Phase2_Model.inp`** - Complete MCNP input (ready to run)

### Supporting Documentation
- **`MSRE_Lattice_Construction_CORRECTED.txt`** - Corrected lattice with Cell 5 fix
- **`MSRE_Lattice_Validation_Report.txt`** - 30+ page validation analysis
- **`MSRE_Base_Geometry_Universe0.txt`** - Base geometry cells/surfaces
- **`MSRE_Base_Geometry_Integration_Notes.md`** - Integration instructions
- **`MSRE_m4_control_rod_poison.txt`** - Material m4 definition

### Planning Documents (from earlier phases)
- **`MSRE_Design_Specification_Complete.md`** - Parameter specifications
- **`MSRE_Geometry_Plan.md`** - Surface numbering scheme
- **`MSRE_Lattice_Structure_Plan.md`** - LAT=1 configuration
- **`MSRE_Lattice_Position_CORRECTION.md`** - User-confirmed positions

---

## Critical Requirements Implemented

✅ **Li-6 enrichment:** 0.005% (depleted 1500× from natural)
✅ **Graphite boron impurity:** 0.8 ppm (both B-10 and B-11)
✅ **Thermal scattering:** MT2 grph.87t at 923 K
✅ **Temperature:** 911 K on all core materials
✅ **Central pattern:** User-confirmed positions
✅ **LAT=1 lattice:** 29×29 array, 589 stringers
✅ **Cell 5 correction:** Boolean error fixed with # operator
✅ **Material m5:** Homogenized density calculated

---

## Workflow Status

**Phase 1:** ✓ COMPLETE (Literature analysis, design specification)
**Phase 2 Step 2.1:** ✓ COMPLETE (Geometry/lattice strategy)
**Phase 2 Step 2.2:** ✓ COMPLETE (Core lattice construction + validation)
**Phase 2 Step 2.3:** ✓ COMPLETE (Reflector/vessel construction)
**Phase 2 Step 2.4:** ✓ COMPLETE (Material definitions m1-m5)
**Phase 2 Integration:** ✓ COMPLETE (All components integrated)

**CURRENT:** Geometry plotting and verification
**NEXT:** Step 2.6 (Validation cascade with 5 validators)
**NEXT:** Step 2.7 (Initial MCNP run)
**NEXT:** Step 2.8 (Results analysis)

---

## Questions or Issues?

If you encounter any problems:

1. **Geometry errors:** Check plot for overlaps/gaps, use `mcnp-geometry-checker`
2. **Lost particles:** Run VOID test, check cell definitions
3. **Material warnings:** Verify cross-section library availability (.80c)
4. **Performance issues:** Reduce KCODE particles (try 5000 per cycle initially)

---

**Ready for geometry plotting!** Execute the plotting commands above to visually verify the MSRE model before running the full criticality calculation.

---

**Date:** 2025-11-07
**Model:** MSRE_Complete_Phase2_Model.inp
**Status:** READY FOR VALIDATION
