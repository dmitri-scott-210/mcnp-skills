# GT-MHR Full Reactor Model Validation - Master Plan

**Created**: 2025-10-31
**Status**: Phase 1 Ready to Execute
**Estimated Duration**: 4-5 hours
**Last Updated**: 2025-10-31

---

## Executive Summary

This master plan documents the comprehensive validation of MCNP skills through generation of a complete GT-MHR (Gas Turbine - Modular Helium Reactor) full-core model from scratch. This validates that the MCNP skills framework can handle complex, multi-level hierarchical reactor geometries comparable to production-quality nuclear engineering models.

### Primary Objective

Validate that MCNP skills can generate a complete, accurate GT-MHR reactor model from scratch based on published design parameters, comparable to the reference `gt-mhr-pbmr.i` model provided by Forest Brown in the MCNP Criticality Primer.

### Critical Success Criteria

1. ✅ **Geometry Complete**: All 7 universe levels built correctly
2. ✅ **No MCNP Errors**: Generated input passes validation
3. ✅ **Materials Accurate**: UCO enrichment, densities match literature
4. ✅ **Lattices Correct**: Both lat=1 (cubic) and lat=2 (hexagonal) implemented
5. ✅ **KCODE Functional**: Criticality calculation can initialize

### Quality Metrics

- **Structural similarity** to gt-mhr-pbmr.i: >90%
- **Design parameter accuracy**: ±5% of literature values
- **Cross-reference completeness**: 100%

---

## Background & Context

### GT-MHR Reactor Overview

**GT-MHR (Gas Turbine - Modular Helium Reactor)**:
- High-temperature gas-cooled reactor (HTGR)
- Helium coolant, graphite moderated
- TRISO coated particle fuel
- Hexagonal fuel block geometry
- Designed for inherent safety and modularity

**Key Features**:
- Core thermal power: 600 MWth
- Outlet temperature: ~850°C
- Fuel: UCO (Uranium Oxycarbide) TRISO particles
- Coolant: Helium at ~7 MPa
- Moderator: Graphite

### Reference Model: gt-mhr-pbmr.i

**File**: `gt-mhr-pbmr.i` (222 lines)
**Author**: Forest Brown (LANL, nuclear criticality professional)
**Source**: MCNP Criticality Primer
**Description**: Approximate model of NGNR full core reactor based on GT-MHR concepts

**Model Characteristics**:
- 7-level hierarchical geometry using universe/fill
- TRISO particle fuel with 5 coating layers
- Double heterogeneity (particles in compacts, compacts in blocks)
- Hexagonal fuel blocks in hexagonal core lattice
- Full core with reflector regions
- Criticality calculation with KCODE

---

## GT-MHR Design Parameters (from Literature)

### Source Documents

1. **"IAEA GT-MHR Benchmark Calculations using the HELIOS/MASTER Code Package"**
   - IAEA benchmark specifications
   - GT-MHR design parameters

2. **MCNP Criticality Primer** (Forest Brown, LANL)
   - Reference model: gt-mhr-pbmr.i
   - NGNR/GT-MHR concepts

### TRISO Particle Specifications

**5-Layer Coated Particle Structure** (from inside to out):

| Layer | Material | Dimension | Purpose |
|-------|----------|-----------|---------|
| Kernel | UO₂ or UCO | 350 μm diameter | Fissile fuel |
| Buffer | Porous carbon | 100 μm thick | Fission gas retention |
| IPyC | Inner PyC | 40 μm thick (≤50 μm) | Pressure barrier |
| SiC | Silicon carbide | 35 μm thick | Primary containment |
| OPyC | Outer PyC | 40 μm thick | Structural support |

**Calculated Radii** (for MCNP spherical surfaces):
- r1 (kernel): 0.0175 cm (175 μm radius)
- r2 (buffer outer): 0.0275 cm (275 μm radius)
- r3 (IPyC outer): 0.0315 cm (315 μm radius)
- r4 (SiC outer): 0.0350 cm (350 μm radius)
- r5 (OPyC outer): 0.0390 cm (390 μm radius)

**Fuel Composition**:
- **Enrichment**: 10.36% U-235 (in UCO)
- **Form**: Uranium oxycarbide (UCO = UO₂ + UC₂)
- **Density**: ~7.086×10⁻² atoms/b-cm (kernel)

### Fuel Compact Geometry

| Parameter | Value | Notes |
|-----------|-------|-------|
| Radius | 0.6225 cm | Cylindrical compact |
| Packing fraction | ~35% | TRISO particles in graphite matrix |
| Matrix material | Graphite | Density: 1.7 g/cm³ |
| Gap (outside compact) | 0.635 cm radius | Void region |
| Graphite wall | 8.725580×10⁻² atoms/b-cm | Structural graphite |

**Particle Lattice**:
- **Type**: Cubic lattice (lat=1 in MCNP)
- **Array size**: 15×15×1 (from gt-mhr-pbmr.i)
- **Cell size**: 0.0951 cm per side (RPP -0.04755 to 0.04755)

### Fuel Block Layout

**Channel Configuration**:
- **Fuel channels**: 210 (contain fuel compacts)
- **Large coolant holes**: 102 (radius 0.79375 cm)
- **Small coolant holes**: 6 (radius 0.635 cm)
- **Total channels**: 318

**Block Geometry**:
- **Shape**: Hexagonal prism
- **Flat-to-flat**: ~36 cm (17.9985 cm half-width in gt-mhr-pbmr.i)
- **Height**: 79.3 cm (active fuel region)
- **Lattice type**: Hexagonal (lat=2 in MCNP)
- **Array size**: 23×23

**Hexagonal Lattice Surfaces** (from gt-mhr-pbmr.i):
```
501 px 0.9398           (vertical plane)
502 px -0.9398          (vertical plane)
503 p 1 1.7320508076 0 1.8796    (60° plane)
504 p 1 1.7320508076 0 -1.8796   (60° plane)
505 p -1 1.7320508076 0 1.8796   (60° plane)
506 p -1 1.7320508076 0 -1.8796  (60° plane)
```

### Column Structure

**Fuel Column** (universe 3):
- **Fuel block height**: 79.3 cm (universe 4)
- **Top reflector**: 793 cm height (872.3 - 79.3 cm)
- **Bottom reflector**: 79.3 cm height (0 to 79.3 cm)
- **Total column height**: 951.6 cm

**Hexagonal dimensions**:
- Block hex: 17.9985 cm half-width
- Total hex: 18.05 cm half-width (includes gap)

### Core Configuration

**Core Lattice**:
- **Type**: Hexagonal (lat=2)
- **Array size**: 23×23
- **Contents**: Fuel columns (universe 3) + reflector columns (universe 2)

**Core Dimensions**:
- **Radius**: 341.63 cm (from RCC surface 900)
- **Height**: 951.6 cm
- **Shape**: Cylindrical (RCC)

**Reflector Columns** (universe 2):
- **Material**: Graphite (8.725580×10⁻² atoms/b-cm)
- **Height**: 951.6 cm (full core height)
- **Position**: Surrounding and within core lattice

### Material Specifications

**From gt-mhr-pbmr.i**:

| Material | ID | Components | Density | Notes |
|----------|----|-----------| --------|-------|
| UCO Fuel | m1 | U-235, U-238, C, O | 7.086×10⁻² | 10.36% enriched |
| Buffer C | m2 | Carbon | 5.0147×10⁻² | Porous carbon |
| IPyC | m3 | Carbon | 9.5279×10⁻² | Pyrolytic carbon |
| SiC | m4 | Si, C | 9.6136×10⁻² | Silicon carbide |
| OPyC | m5 | Carbon | 9.5279×10⁻² | Pyrolytic carbon |
| Matrix | m6 | Carbon | -1.7 g/cm³ | Graphite matrix |
| Block | m7 | C, B-10 | 8.7255×10⁻² | Graphite + boron |
| Reflector | m8 | C, B-10 | 8.7255×10⁻² | Top/bottom reflector |
| Side Refl | m9 | C, B-10 | 8.7255×10⁻² | Replaceable reflector |

**Material m1 (UCO Fuel)**:
```
m1   92235.66c  0.002475    (U-235)
     92238.66c  0.021145    (U-238)
      6000.66c  0.01181     (Carbon)
      8016.62c  0.03543     (Oxygen)
mt1 grph.60t                (Thermal scattering)
```

**Boron Impurity**: 7.22×10⁻⁷ atoms/b-cm in graphite (B-10)

### Physics Parameters

**Criticality Calculation**:
```
mode n                                      (neutron transport)
kcode 5000 1.0 50 500                      (5000 histories, k=1.0, skip 50, run 500 cycles)
ksrc 180.5 2 120 0 202.5 436.15 -202.5 0 515.45   (3 source points)
```

**Variance Reduction**:
```
prdmp 999999 999999 1 1 9999999            (print dump control)
spdtl off                                   (source point details off)
```

---

## Reference Model Analysis: gt-mhr-pbmr.i

### 7-Level Hierarchical Structure

The gt-mhr-pbmr.i model uses a sophisticated 7-level universe hierarchy:

**Level 1: TRISO Particle (universe 50)**
```
101 1 7.086e-2 -101 u=50 imp:n=1           $ uranium oxycarbide region
102 2 5.0147e-2 101 -102 u=50 imp:n=1      $ porous carbon buffer
103 3 9.5279e-2 102 -103 u=50 imp:n=1      $ inner pyrolytic carbon
104 4 9.6136e-2 103 -104 u=50 imp:n=1      $ silicon carbide region
105 5 9.5279e-2 104 -105 u=50 imp:n=1      $ outer pyrolytic carbon
106 6 -1.7 105 u=50 imp:n=1                $ graphite matrix
```
- 5 concentric spheres (surfaces 101-105)
- Graphite matrix fill outside particle

**Level 2: Particle Lattice (universe 40)**
```
200 6 -1.7 -200 lat=1 u=40 imp:n=1         $ cubic region
        fill= -7:7 -7:7 0:0
        [15×15×1 array of universe 40 (graphite) and 50 (particles)]
```
- Cubic lattice (lat=1)
- 15×15×1 array (-7 to 7, -7 to 7, 0 to 0)
- Fills with mix of graphite (u=40) and particles (u=50)
- Packing fraction ~35%

**Level 3: Flat Lattice Transition (universe 41)**
```
201 0 -201 lat=1 fill=40 imp:n=1 u=41
```
- Single-cell cubic lattice
- Contains universe 40 (particle lattice)
- Provides flat surface for cylindrical compact

**Level 4: Fuel Compact (universe 5)**
```
300 0 -300 fill=41 u=5 imp:n=1             $ fuel compact region
301 0 300 -301 u=5 imp:n=1                 $ void outside fuel pin
302 7 8.725580e-2 301 u=5 imp:n=1          $ graphite wall
```
- Cylinder r=0.6225 cm (surface 300)
- Gap r=0.635 cm (surface 301)
- Graphite wall outside

**Level 5: Coolant Hole (universe 6)**
```
400 0 -400 u=6 imp:n=1                     $ larger coolant hole
401 7 8.725580e-2 400 u=6 imp:n=1          $ graphite wall
```
- Cylinder r=0.79375 cm (surface 400)
- Graphite wall outside

**Level 6: Fuel Block (universe 4)**
```
500 7 8.725580e-2 -501 502 -503 504 -505 506 u=4 lat=2 imp:n=1
                fill=-11:11 -11:11 0:0
        [23×23 array of universes 4 (graphite), 5 (fuel), 6 (coolant)]
```
- Hexagonal lattice (lat=2)
- 23×23 array (-11 to 11, -11 to 11, 0 to 0)
- 6 planes define hexagonal boundary
- Fills with fuel compacts (u=5), coolant holes (u=6), graphite (u=4)

**Level 7: Column (universe 3)**
```
601 0 -601 *fill=4 (0 0 0 30 120 90 60 30 90 90 90 0) u=3 imp:n=1
602 8 8.725580e-2 -602 u=3 imp:n=1          $ top reflector column
603 8 8.725580e-2 -603 u=3 imp:n=1          $ bottom reflector column
604 0 601 #602 #603 u=3 imp:n=1             $ void outside column
```
- Fuel block hex (79.3 cm height)
- Top reflector (793 cm)
- Bottom reflector (79.3 cm)
- Total: 951.6 cm

**Level 8: Core (universe 1)**
```
800 0 -800 u=1 lat=2 imp:n=1 fill=-11:11 -11:11 0:0
        [23×23 array of universes 2 (reflector) and 3 (fuel column)]
```
- Hexagonal lattice (lat=2)
- 23×23 array
- Fuel columns (u=3) in center
- Reflector columns (u=2) on periphery

**Level 9: Reactor**
```
900 0 -900 fill=1 imp:n=1                  $ reactor core
901 0 900 imp:n=0                           $ outside the core
```
- RCC cylinder: r=341.63 cm, h=951.6 cm (surface 900)
- Filled with core universe (u=1)
- Outside has imp:n=0 (neutron importance 0)

### Key MCNP Techniques Demonstrated

1. **Nested Universes**: 7-level deep hierarchy
2. **Mixed Lattices**: Both lat=1 (cubic) and lat=2 (hexagonal)
3. **Fill Transformations**: Rotation of fuel block (0 0 0 30 120 90 60 30 90 90 90 0)
4. **Double Heterogeneity**: Particles in compacts, compacts in blocks
5. **Material Variation**: 9 different materials with thermal scattering (mt cards)
6. **Criticality**: KCODE eigenvalue calculation with multiple source points

---

## Five-Phase Validation Plan

### Phase 1: Design Parameter Documentation (30 min)

**Objective**: Create comprehensive design specification document

**Tasks**:
1. Document TRISO particle dimensions with calculated radii
2. Document fuel compact geometry and packing fraction
3. Document fuel block layout with channel counts
4. Document core configuration with lattice details
5. Document all material specifications with compositions
6. Document physics parameters (KCODE, source)

**Deliverable**: `tests/validation/gt_mhr_design_spec.md`

**Success Criteria**:
- All design parameters from literature documented
- Parameters match gt-mhr-pbmr.i within ±5%
- Material compositions fully specified
- Geometry dimensions complete

**Status**: ⏸️ Ready to execute

---

### Phase 2: Model Generation Using Skills (2-3 hours)

**Objective**: Build GT-MHR model step-by-step using MCNP skills

#### 2.1 TRISO Particle (mcnp-geometry-builder)

**Tasks**:
- Create 5 concentric spheres (SO surfaces)
  - s101: 0.0175 cm (kernel)
  - s102: 0.0275 cm (buffer)
  - s103: 0.0315 cm (IPyC)
  - s104: 0.0350 cm (SiC)
  - s105: 0.0390 cm (OPyC)
- Define cells for each layer (c101-c105)
- Define graphite matrix cell (c106)
- Assign to universe 50

**Test**: Verify sphere radii match specifications (±0.0001 cm)

#### 2.2 Particle Lattice (mcnp-lattice-builder)

**Tasks**:
- Create cubic lattice (lat=1) in universe 40
- Define RPP cell: -0.04755 to 0.04755 (0.0951 cm cube)
- Create 15×15×1 fill array (-7:7, -7:7, 0:0)
- Fill pattern: ~35% universe 50 (particles), rest universe 40 (graphite)
- Pattern should approximate circular distribution

**Test**: Verify lattice dimensions (0.0951 cm cell) and fill pattern

#### 2.3 Flat Lattice Transition (mcnp-lattice-builder)

**Tasks**:
- Create universe 41 with lat=1
- Define RPP cell: -0.71325 to 0.71325
- Fill with universe 40 (single cell)

**Test**: Verify proper transition to cylindrical geometry

#### 2.4 Fuel Compact (mcnp-geometry-builder)

**Tasks**:
- Create CZ surface 300: r=0.6225 cm
- Create CZ surface 301: r=0.635 cm (gap)
- Define cells:
  - c300: fill=41 (contains particle lattice)
  - c301: void (gap)
  - c302: graphite wall
- Assign to universe 5

**Test**: Verify compact radius and structure

#### 2.5 Coolant Hole (mcnp-geometry-builder)

**Tasks**:
- Create CZ surface 400: r=0.79375 cm
- Define cells:
  - c400: void (coolant channel)
  - c401: graphite wall
- Assign to universe 6

**Test**: Verify coolant hole radius

#### 2.6 Fuel Block (mcnp-lattice-builder + mcnp-geometry-builder)

**Tasks**:
- Create hexagonal boundary (6 P surfaces):
  - s501: px 0.9398
  - s502: px -0.9398
  - s503-s506: p planes at 60° angles
- Create hexagonal lattice (lat=2) in universe 4
- Define 23×23 fill array (-11:11, -11:11, 0:0)
- Fill pattern:
  - Universe 5: fuel compacts (210 channels)
  - Universe 6: coolant holes (102 large)
  - Universe 4: graphite fill

**Test**: Verify hexagonal geometry and channel positions (match gt-mhr-pbmr.i pattern)

#### 2.7 Column Structure (mcnp-geometry-builder)

**Tasks**:
- Create HEX surfaces:
  - s601: fuel block (79.3 cm height)
  - s602: top reflector (872.3 cm total)
  - s603: bottom reflector (79.3 cm)
- Define cells in universe 3:
  - c601: fill=4 with rotation (0 0 0 30 120 90 60 30 90 90 90 0)
  - c602: top reflector (material 8)
  - c603: bottom reflector (material 8)
  - c604: void outside
- Create universe 2 (reflector column):
  - s700: hex 951.6 cm height
  - c700: material 9

**Test**: Verify column heights and reflector placement

#### 2.8 Core Lattice (mcnp-lattice-builder)

**Tasks**:
- Create HEX surface 800 in universe 1
- Create hexagonal lattice (lat=2)
- Define 23×23 fill array (-11:11, -11:11, 0:0)
- Fill pattern (match gt-mhr-pbmr.i):
  - Universe 3: fuel columns (center region)
  - Universe 2: reflector columns (periphery)

**Test**: Verify core lattice pattern matches reference

#### 2.9 Reactor Vessel (mcnp-geometry-builder)

**Tasks**:
- Create RCC surface 900: origin (0,0,0), axis (0,0,951.6), radius 341.63 cm
- Define cells:
  - c900: fill=1 (core), imp:n=1
  - c901: outside core, imp:n=0

**Test**: Verify reactor dimensions

#### 2.10 Materials (mcnp-material-builder)

**Tasks**:
- Define m1: UCO fuel (U-235, U-238, C, O) with mt1 grph.60t
- Define m2: Buffer carbon
- Define m3: IPyC
- Define m4: SiC (Si + C)
- Define m5: OPyC
- Define m6: Graphite matrix
- Define m7: Fuel block graphite + B-10
- Define m8: Reflector graphite + B-10
- Define m9: Side reflector graphite + B-10

**Test**: Verify isotopic compositions match gt-mhr-pbmr.i

#### 2.11 Source & Physics (mcnp-source-builder + mcnp-physics-builder)

**Tasks**:
- Add title card
- Define MODE N
- Define KCODE: 5000 1.0 50 500
- Define KSRC: 180.5 2 120   0 202.5 436.15   -202.5 0 515.45
- Add PRDMP: 999999 999999 1 1 9999999
- Add SPDTL: off

**Test**: Verify criticality setup

**Deliverable**: `tests/validation/generated_gt_mhr.inp`

**Success Criteria**:
- Complete MCNP input file generated
- All 7 universe levels present
- All materials defined
- KCODE setup complete
- File compiles without syntax errors

**Status**: ⏸️ Pending Phase 1 completion

---

### Phase 3: Structural Validation (1 hour)

**Objective**: Validate generated model structure and syntax

#### 3.1 Geometry Validation (mcnp-geometry-checker)

**Skill**: mcnp-geometry-checker

**Tasks**:
- Check for overlapping cells
- Verify surface definitions
- Check universe hierarchy (7+ levels deep)
- Verify lattice definitions (lat=1 and lat=2)

**Pass Criteria**:
- Zero geometry errors
- All universes defined
- All surfaces referenced

#### 3.2 Cross-Reference Validation (mcnp-cross-reference-checker)

**Skill**: mcnp-cross-reference-checker

**Tasks**:
- Verify all cell→surface references valid
- Verify all cell→material references valid
- Check universe→fill references complete
- Verify lattice fill arrays correct

**Pass Criteria**:
- 100% cross-reference completeness
- No broken references
- All universes filled correctly

#### 3.3 Input Validation (mcnp-input-validator)

**Skill**: mcnp-input-validator

**Tasks**:
- Check block structure (title, cells, surfaces, data)
- Verify card syntax (cell, surface, data cards)
- Check material definitions (9 materials)
- Verify importance (imp) cards

**Pass Criteria**:
- Zero syntax errors
- All required blocks present
- Proper blank line separation

**Deliverable**: `tests/validation/gt_mhr_validation_report.md`

**Success Criteria**:
- All validation checks pass
- Detailed comparison to gt-mhr-pbmr.i documented
- Differences explained and justified

**Status**: ⏸️ Pending Phase 2 completion

---

### Phase 4: Physics Validation (30 min)

**Objective**: Verify physics setup correctness

**Tasks**:

#### 4.1 Material Composition Comparison
- Compare m1 (UCO) composition to reference
- Verify enrichment: 10.36% U-235
- Check all material densities

#### 4.2 KCODE Parameters
- Verify: 5000 histories per cycle
- Verify: k-guess = 1.0
- Verify: 50 skip cycles
- Verify: 500 active cycles

#### 4.3 Source Distribution
- Verify KSRC positions (3 points)
- Check source points are within core geometry

**Pass Criteria**:
- Material compositions match reference (±1%)
- KCODE parameters match exactly
- Source points valid

**Status**: ⏸️ Pending Phase 3 completion

---

### Phase 5: Completeness Check (30 min)

**Objective**: Document model completeness and compare to reference

**Checklist**:

#### 5.1 Geometry Hierarchy
- [ ] Level 1: TRISO particle (u=50) ✓
- [ ] Level 2: Particle lattice (u=40) ✓
- [ ] Level 3: Flat transition (u=41) ✓
- [ ] Level 4: Fuel compact (u=5) ✓
- [ ] Level 5: Coolant hole (u=6) ✓
- [ ] Level 6: Fuel block (u=4) ✓
- [ ] Level 7: Column (u=3) ✓
- [ ] Level 8: Core (u=1) ✓
- [ ] Level 9: Reactor vessel ✓

#### 5.2 Materials
- [ ] m1: UCO fuel ✓
- [ ] m2: Buffer carbon ✓
- [ ] m3: IPyC ✓
- [ ] m4: SiC ✓
- [ ] m5: OPyC ✓
- [ ] m6: Matrix graphite ✓
- [ ] m7: Fuel block graphite ✓
- [ ] m8: Reflector graphite ✓
- [ ] m9: Side reflector ✓
- [ ] All mt (thermal scattering) cards ✓

#### 5.3 Lattices
- [ ] Cubic lattice (lat=1) for particles ✓
- [ ] Cubic lattice (lat=1) for transition ✓
- [ ] Hexagonal lattice (lat=2) for fuel block ✓
- [ ] Hexagonal lattice (lat=2) for core ✓

#### 5.4 Physics
- [ ] MODE N ✓
- [ ] KCODE ✓
- [ ] KSRC ✓
- [ ] PRDMP ✓
- [ ] SPDTL ✓

#### 5.5 Model Size
- [ ] Total line count: ~200-250 lines (target ~220 like reference)
- [ ] Cell cards: ~30-40
- [ ] Surface cards: ~30-40
- [ ] Data cards: ~50-70

**Deliverable**: Final section in `gt_mhr_validation_report.md`

**Success Criteria**:
- All checklist items complete
- Model comparable to gt-mhr-pbmr.i in complexity
- All critical components present

**Status**: ⏸️ Pending Phase 4 completion

---

## Skills Required

### Geometry & Lattice Skills
- **mcnp-geometry-builder**: TRISO particles, fuel compacts, coolant holes, reactor vessel
- **mcnp-lattice-builder**: Cubic lattices (lat=1), hexagonal lattices (lat=2), fill arrays

### Material & Physics Skills
- **mcnp-material-builder**: UCO fuel, graphite grades, SiC, carbon layers
- **mcnp-source-builder**: KCODE setup, KSRC initial sources
- **mcnp-physics-builder**: MODE card, physics parameters

### Validation Skills
- **mcnp-input-validator**: Syntax validation, block structure
- **mcnp-geometry-checker**: Overlap detection, surface checks
- **mcnp-cross-reference-checker**: Cell/surface/material/universe references

---

## Test File Structure

```
tests/validation/
├── GT_MHR_VALIDATION_MASTER_PLAN.md       (This document)
├── gt_mhr_design_spec.md                  (Phase 1 - Design parameters)
├── generated_gt_mhr.inp                   (Phase 2 - Generated model)
├── gt_mhr_validation_report.md            (Phases 3-5 - Validation results)
└── test_gt_mhr_generation.py              (Optional - Automated tests)
```

---

## Timeline & Milestones

| Phase | Duration | Status | Deliverable |
|-------|----------|--------|-------------|
| Phase 1 | 30 min | ⏸️ Ready | gt_mhr_design_spec.md |
| Phase 2 | 2-3 hours | ⏸️ Pending | generated_gt_mhr.inp |
| Phase 3 | 1 hour | ⏸️ Pending | gt_mhr_validation_report.md |
| Phase 4 | 30 min | ⏸️ Pending | Physics validation section |
| Phase 5 | 30 min | ⏸️ Pending | Completeness checklist |
| **Total** | **4-5 hours** | **0% Complete** | **3 documents + model** |

---

## Success Criteria Summary

### Critical Requirements (Must Pass)

1. ✅ **Geometry Complete**: All 7+ universe levels built correctly
2. ✅ **No MCNP Errors**: Generated input passes mcnp-input-validator
3. ✅ **Materials Accurate**: UCO enrichment and densities match literature
4. ✅ **Lattices Correct**: Both lat=1 (cubic) and lat=2 (hex) implemented
5. ✅ **KCODE Functional**: Criticality calculation properly set up

### Quality Metrics

- **Structural similarity** to gt-mhr-pbmr.i: >90%
- **Design parameter accuracy**: ±5% of literature values
- **Cross-reference completeness**: 100%
- **Material composition accuracy**: ±1%
- **Geometry dimensions**: ±5%

### Pass/Fail Determination

**PASS** requires:
- All 5 critical requirements met
- All quality metrics within tolerance
- All validation checks (Phase 3) passing
- Complete documentation (Phases 1, 3-5)

**FAIL** triggers:
- Any critical requirement not met
- MCNP syntax errors in generated input
- Geometry errors (overlaps, lost particles)
- Missing universe levels or materials
- Cross-reference errors >0

---

## Notes for Future Claudes

### Context Continuation

If you are a future Claude continuing this work:

1. **Read this document first** - It contains all design parameters and the complete plan
2. **Check timeline table** - See which phases are complete
3. **Review deliverables** - Check if files exist in tests/validation/
4. **Start where left off** - Continue with the next pending phase
5. **Update status** - Mark phases complete and update this document

### Key Files to Reference

- **gt-mhr-pbmr.i**: Reference model (project root)
- **This document**: Complete plan and design parameters
- **TESTING_STATUS.md**: Overall project testing status
- **Generated deliverables**: In tests/validation/ directory

### Common Pitfalls to Avoid

1. **Don't skip Phase 1** - Design spec is critical for accurate model generation
2. **Universe numbering** - Must match gt-mhr-pbmr.i (u=50, 40, 41, 5, 6, 4, 3, 2, 1)
3. **Lattice indexing** - Arrays use -11:11 notation (23 cells total)
4. **Hexagonal surfaces** - Require 6 plane surfaces for proper definition
5. **Fill transformations** - Fuel block rotation: (0 0 0 30 120 90 60 30 90 90 90 0)
6. **Material thermal scattering** - Don't forget mt cards for graphite (grph.60t)

### Debugging Tips

If validation fails:

1. **Geometry errors** → Check universe hierarchy and surface definitions
2. **Cross-reference errors** → Verify all universe/fill/material references
3. **Syntax errors** → Check blank line separation between blocks
4. **Lost particles** → Check for gaps in geometry, verify lattice fill patterns
5. **Material errors** → Verify ZAIDs and thermal scattering libraries

### Progress Tracking

Update this section as work progresses:

**Phase 1**: ⏸️ Not started
**Phase 2**: ⏸️ Not started
**Phase 3**: ⏸️ Not started
**Phase 4**: ⏸️ Not started
**Phase 5**: ⏸️ Not started

**Overall Progress**: 0/5 phases complete (0%)

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-31 | 1.0 | Initial master plan created | Claude (Sonnet 4.5) |

---

## References

1. **IAEA GT-MHR Benchmark Calculations using the HELIOS/MASTER Code Package**
   - IAEA benchmark specifications
   - GT-MHR design parameters
   - TRISO particle specifications

2. **MCNP Criticality Primer** (Forest Brown, LANL)
   - gt-mhr-pbmr.i reference model
   - NGNR/GT-MHR concepts
   - HTGR modeling techniques

3. **MCNP6 User's Manual** (LA-CP-13-00634)
   - Universe/fill syntax
   - Lattice definitions (lat=1, lat=2)
   - Material specifications

4. **GT-MHR Technical Literature**
   - Fuel specifications
   - Core design parameters
   - Safety analysis

---

**END OF MASTER PLAN**

*This document serves as the definitive reference for GT-MHR full reactor model validation. All future work should reference and update this document.*
