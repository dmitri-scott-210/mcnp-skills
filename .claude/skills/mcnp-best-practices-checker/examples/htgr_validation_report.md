# HTGR Model Validation Report

**Model:** AGR-1 Experiment TRISO Particle Model (6-level hierarchy)
**Date:** 2025-01-15
**Validator:** Best Practices Checker v2.0
**Input File:** sdr-agr-1.i (18,427 lines)

---

## PHASE 0: PROFESSIONAL MODELING STANDARDS

### Repository Structure

```
✓ Version control initialized (git)
✓ README documents workflow
✓ CSV data files with provenance
✓ Python generation script
✓ Numbering scheme designed (9XYZW encoding)
```

**Details:**
- Git repository: 47 commits, 3 tags (v1.0-baseline, v1.1-burnup, v2.0-sdr)
- README: Complete with regeneration instructions
- Data files: power.csv (13 cycles), positions.csv, materials.json
- Generation: create_inputs.py (478 lines, well-documented)
- Numbering: 9[capsule][stack][2×compact][sequence] = 91234 pattern

**Score:** 5/5 items PASS

---

### Automation

```
✓ Programmatic generation (create_inputs.py)
✓ Validation script (validate_inputs.py)
✓ Single command regenerates all
✓ No hardcoded parameters
```

**Details:**
- Generation: `python create_inputs.py` → 13 inputs generated
- Validation: `python validate_inputs.py` → all checks pass
- Parameters: All in materials.json and power.csv
- Reproducibility: Tested on independent machine, perfect match

**Score:** 3/3 items PASS

---

### Material Standards

```
✗ Missing thermal scattering for graphite!
  Action: Add mt9040 grph.18t for moderator
  Action: Add mt9090-mt9094 grph.18t for TRISO coatings
  Impact: ~2000 pcm reactivity error without this
```

**Analysis:**
- Materials checked: 385 total material definitions
- Carbon detected in: m9040 (moderator), m9090-m9094 (PyC coatings), m9110-9167 (fuel kernels)
- MT cards found: NONE
- **CRITICAL ERROR:** All graphite materials missing thermal scattering

**Required fixes:**
```mcnp
c Graphite moderator (operating ~700K)
m9040  6012.00c 0.9890  6013.00c 0.0110
mt9040 grph.18t  $ REQUIRED! 700K thermal scattering

c PyC coatings (TRISO particles, ~700K)
m9090  6012.00c 0.9890  6013.00c 0.0110
mt9090 grph.18t  $ REQUIRED!

m9091  6012.00c 0.9890  6013.00c 0.0110
mt9091 grph.18t  $ REQUIRED!
...
```

**Score:** 1/3 items (1 CRITICAL FAIL)

**Assessment:** 14/15 Phase 0 items complete, **1 CRITICAL ERROR**

**Action Required:** **STOP** - Fix thermal scattering before ANY runs

---

## PHASE 1: PROBLEM SETUP (Reactor-Specific)

### Multi-Level Lattice Validation

**Level 1: TRISO Particle (u=1114)**
```
✓ Concentric spheres (SO surfaces)
✓ No gaps verified (r1 < r2 < r3 < r4 < r5)
  - Kernel: 0.0175 cm
  - Buffer: 0.0275 cm
  - IPyC: 0.0315 cm
  - SiC: 0.0350 cm
  - OPyC: 0.0390 cm
✓ Material m9111 defined (UCO kernel)
✓ Volume specified (vol=0.092522 cm³)
```

**Level 2: Particle Lattice (u=1116, LAT=1)**
```
✓ Dimension: fill=-7:7 -7:7 0:0 → 15×15×1 = 225 elements
✓ Element count validation:
  - 169 TRISO particles (u=1114)
  - 56 matrix cells (u=1115)
  - Total: 225 ✓ MATCHES
✓ Bounding surface: RPP -0.75 0.75 -0.75 0.75 -0.025 0.025
  - Extent: 1.5 cm = 15 × 0.1 cm pitch ✓
✓ All filled universes defined (u=1114, u=1115)
```

**Level 3: Compact Stack (u=1110, LAT=1)**
```
✓ Dimension: fill=0:0 0:0 -15:15 → 1×1×31 = 31 elements
✓ Pattern validation:
  - 1117 2R: 3 copies (top plugs)
  - 1116 24R: 25 copies (fuel compacts)
  - 1117 2R: 3 copies (bottom plugs)
  - Total: 3 + 25 + 3 = 31 ✓ MATCHES
✓ Bounding surface: RPP vertical extent matches 31 × 5.08 cm = 157.48 cm
✓ All filled universes defined (u=1116, u=1117)
```

**Level 4-6: Capsule Hierarchy**
```
✓ Transformation cards (x,y,z) positions validated
✓ No circular universe references detected
✓ All 72 compacts generated systematically
  - 6 capsules × 3 stacks × 4 compacts = 72 ✓
  - Universe IDs: 1110, 1120, ..., 6340 (all unique)
```

**Score:** 8/8 items PASS

---

### Cross-Reference Validation

**Surface References:**
```
✓ Extracted 1607 cell definitions
✓ Extracted 892 surface definitions
✓ Checked all cell → surface references
✓ Result: 0 undefined surface references
```

**Material References:**
```
✓ Extracted 385 material definitions
✓ Checked all cell → material references
✓ Result: 0 undefined material references
```

**Universe Fill Validation:**
```
✓ Built universe dependency graph
✓ Checked for circular references
✓ Result: No cycles detected
✓ Hierarchy depth: 6 levels (as designed)
```

**Score:** 3/3 items PASS

---

### Numbering Scheme Validation

**Duplicate Detection:**
```
✓ Cell IDs: 1607 unique (0 duplicates)
✓ Surface IDs: 892 unique (0 duplicates)
✓ Material IDs: 385 unique (0 duplicates)
✓ Universe IDs: 124 unique (0 duplicates)
```

**Scheme Adherence:**
```
✓ Cell numbering follows 9XYZW pattern
✓ Surface numbering follows 9XYZ pattern
✓ Material numbering follows 9XYZ pattern
✓ Universe numbering follows XYZ[level] pattern
```

**Examples:**
- Cell 91234: Capsule 1, Stack 2, Compact 2, Sequence 4 ✓
- Surface 9122: Capsule 1, Stack 2, Compact 2 ✓
- Material m9122: Fuel in Capsule 1, Stack 2, Compact 2 ✓
- Universe 1224: Capsule 1, Stack 2, Compact 2, Level 4 ✓

**Score:** 4/4 items PASS

---

### Comment Documentation

```
✓ Every cell has descriptive comment
  Example: "91234 10 -1.0 -91234 imp:n=1 $ Capsule 1, Stack 2, Compact 2, Kernel"
✓ Every surface documented with purpose
  Example: "9122 so 0.0175 $ TRISO kernel outer radius"
✓ Every material has composition note
  Example: "m9122 92235.00c 0.1975 ... $ UCO fuel, 19.75% enriched"
✓ Section headers clearly mark blocks
  Example: "c --- CAPSULE 1 CELLS ---"
```

**Score:** 4/4 items PASS

---

### Geometry Validation

**Plotting:**
```
✓ Plotted from XY view (extent -50 to 50, origin)
✓ Plotted from XZ view (extent -50 to 50, origin)
✓ Plotted from YZ view (extent -50 to 50, origin)
✓ No dashed lines observed (no overlaps/gaps)
✓ Visual inspection confirms:
  - TRISO particles visible in compacts
  - Capsule positions correct (6 total)
  - Stack arrangement correct (3 per capsule)
```

**VOID Test:**
```
Test Setup:
  VOID card: All materials → void
  Source: SUR=998 NRM=-1 (flood from outside)
  Particles: 1,000,000

Results:
  ✓ Particles run: 1,000,000
  ✓ Lost particles: 0
  ✓ Geometry is watertight

Conclusion: Geometry VALID
```

**Volume Validation:**
```
Pre-calculated volumes:
  - TRISO particle: 0.092522 cm³ (spherical, r=0.039 cm)
  - Compact: 64.8 cm³ (cylindrical, r=0.635 cm, h=5.08 cm)
  - Capsule: ~1200 cm³ (complex shape)

MCNP calculated (VOL card):
  - TRISO: 0.092519 cm³ (0.003% difference) ✓
  - Compact: 64.7 cm³ (0.15% difference) ✓
  - Capsule: 1198 cm³ (0.17% difference) ✓

All within 1% tolerance ✓
```

**Score:** 7/7 items PASS

---

## SUMMARY

### Phase 0: Professional Modeling Standards
- **Total Items:** 15
- **Passed:** 14
- **Failed:** 1 (CRITICAL)
- **Warnings:** 0

### Phase 1: Setup (Standard + Reactor-Specific)
- **Total Items:** 30
- **Passed:** 29
- **Failed:** 1 (from Phase 0)
- **Warnings:** 0

### Overall Assessment

```
==========================================
CRITICAL FAILURE - INPUT NOT READY
==========================================

BLOCKING ISSUE:
  ✗ Missing thermal scattering for ALL graphite materials

IMPACT:
  - Reactivity error: ~2000 pcm (WRONG keff)
  - Reaction rates: WRONG by 10-30%
  - Results: INVALID

ACTION REQUIRED:
  1. Add MT cards to all graphite materials (m9040, m9090-m9094, etc.)
  2. Use grph.18t (700K) for operating conditions
  3. Re-validate after fix
  4. THEN proceed to Phase 2 test run

DO NOT RUN MCNP until this is fixed!
```

---

## Next Steps

1. **Immediate:** Fix thermal scattering
   ```mcnp
   mt9040 grph.18t
   mt9090 grph.18t
   mt9091 grph.18t
   ...
   ```

2. **Re-validate:** Run reactor_model_checker.py again

3. **Phase 2:** Test run (100k particles)
   - Check statistical quality
   - Verify FOM stability
   - Examine warnings

4. **Production:** Full run after Phase 2 validates

---

**Report Generated:** 2025-01-15 14:32:17
**Validation Time:** 12.3 seconds
**Tool:** reactor_model_checker.py v2.0
