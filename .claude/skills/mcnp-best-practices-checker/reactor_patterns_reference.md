# Reactor Modeling Patterns Reference

**Purpose:** Common reactor geometry patterns and hierarchies for professional MCNP modeling

**Based on:** Production HTGR, PWR, and fast reactor models

---

## Multi-Level Lattice Hierarchies

### PWR Core Pattern (4 levels)

**Hierarchy:**
```
Level 1: Fuel Pin (u=100 series)
├── Fuel pellet (UO2)
├── Gap (helium)
├── Cladding (Zircaloy)
└── Coolant (water)

Level 2: Assembly (u=200, LAT=1)
├── 17×17 pin array
├── Guide tubes (positions without fuel)
└── Instrument tube (center position)

Level 3: Core Quarter (u=300, LAT=1)
├── Assembly array (typically 8×8 or larger)
├── Reflector assemblies (outer positions)
└── Control rod assemblies

Level 4: Full Core
├── Reflective/rotational symmetry
├── Barrel and vessel
└── Ex-core components
```

**Typical dimensions:**
- Pin pitch: ~1.26 cm
- Assembly pitch: ~21.5 cm
- Fuel pellet radius: ~0.41 cm
- Cladding thickness: ~0.057 cm

**Universe numbering:**
- 100-199: Pin-level universes
- 200-299: Assembly-level universes
- 300-399: Core-level universes

---

### HTGR Core Pattern (6 levels)

**Hierarchy:**
```
Level 1: TRISO Particle (u=XXX4)
├── Kernel (UCO, 350 μm diameter)
├── Buffer (porous PyC, 100 μm)
├── IPyC (inner PyC, 40 μm)
├── SiC (silicon carbide, 35 μm)
└── OPyC (outer PyC, 40 μm)

Level 2: Particle Lattice (u=XXX6, LAT=1)
├── 15×15 or 23×23 rectangular array
├── TRISO particles in lattice positions
└── Matrix material (SiC or graphite) filling

Level 3: Compact Stack (u=XXX0, LAT=1)
├── Vertical 1×1×31 array
├── Fuel compacts (active region)
└── Graphite plugs (top/bottom)

Level 4: Fuel Channel (u=XXX1)
├── Cylindrical channel in graphite block
├── Filled with compact stack
└── Graphite surrounding

Level 5: Hexagonal Assembly (u=XXX0, LAT=2)
├── Fuel channels in hex pattern
├── Coolant channels
└── Graphite block structure

Level 6: Core
├── Multiple hex assemblies
├── Reflector blocks
├── Control rod channels
└── Barrel/vessel
```

**Typical dimensions:**
- TRISO kernel: 350 μm diameter
- TRISO total: 865 μm diameter
- Compact diameter: ~1.27 cm
- Compact length: ~5.08 cm
- Fuel channel diameter: ~1.27 cm
- Hex block flat-to-flat: ~36 cm

**Universe numbering (AGR-1 pattern):**
- XXX4: TRISO particle (last digit 4)
- XXX5: Matrix cell (last digit 5)
- XXX6: Particle lattice (last digit 6)
- XXX0: Compact stack (last digit 0)
- XXX1: Fuel channel (last digit 1)
- XXX0: Assembly (last digit 0, different range)

---

### Fast Reactor Pattern (5 levels)

**Hierarchy:**
```
Level 1: Fuel Pin (u=100 series)
├── Fuel (MOX or metal)
├── Bond (sodium or gas)
├── Cladding (steel)
└── Coolant (sodium)

Level 2: Pin Bundle (u=200, LAT=2)
├── Hexagonal pin array (91, 127, 169, 217, or 271 pins)
├── Wire wrap or grid spacers
└── Coolant flowing between pins

Level 3: Assembly Duct (u=300)
├── Hexagonal duct containing pin bundle
├── Inter-assembly gap (sodium)
└── Load pads (corners)

Level 4: Core (u=400, LAT=2)
├── Hexagonal assembly array
├── Driver fuel assemblies
├── Control assemblies
├── Reflector assemblies
└── Shield assemblies

Level 5: Vessel
├── Core barrel
├── Radial shield
├── Reactor vessel
└── Guard vessel
```

**Typical dimensions:**
- Pin diameter: ~0.6-0.8 cm
- Pin pitch: ~0.8-1.0 cm
- Assembly flat-to-flat: ~11-16 cm
- Core height: ~100-150 cm

**Universe numbering:**
- 100-199: Pin-level
- 200-299: Bundle-level
- 300-399: Assembly-level
- 400-499: Core-level

---

## Systematic Numbering Schemes

### Hierarchical Encoding (HTGR AGR-1)

**Cell numbering formula:**
```python
# 9[capsule][stack][2×compact][sequence]
cell_id = 90000 + capsule*1000 + stack*100 + 2*(compact-1)*10 + sequence

# Example: Cell 91234
#   9 = experiment prefix
#   1 = capsule 1
#   2 = stack 2
#   3 = compact 2 (2*(2-1)=2, position 3)
#   4 = sequence/component 4
```

**Surface numbering:**
```python
# 9[capsule][stack][compact][layer]
surf_id = 9000 + capsule*100 + stack*10 + compact

# Example: Surface 9122 = Capsule 1, Stack 2, Compact 2
```

**Material numbering:**
```python
# 9[capsule][stack][compact]
mat_id = 9000 + capsule*100 + stack*10 + compact

# Example: m9122 = Fuel in Capsule 1, Stack 2, Compact 2
```

**Universe numbering:**
```python
# [capsule][stack][compact][level]
univ_id = capsule*100 + stack*10 + compact + level_digit

# Example: u=1224 = Capsule 1, Stack 2, Compact 2, Level 4 (TRISO)
```

**Benefits:**
- Zero numbering conflicts across 1500+ entities
- Instant location identification (see 91234, know it's capsule 1)
- Enables automated generation
- Simplifies debugging

---

### Layer-Assembly Pattern (Microreactor)

**Encoding:**
```python
# [layer][assembly][component]
def numbering(layer, assembly_number, component):
    base = (layer+1) * 1000 + assembly_number * 10
    cell_id = base + component
    surf_id = base + component
    mat_id = base * 10 + component  # Extra digit for materials
    return cell_id, surf_id, mat_id

# Example: Layer 2, Assembly 01, Component 3
# Cell: 2013, Surface: 2013, Material: 20103
```

**Range allocation:**
- 1000-1999: Layer 0 (bottom)
- 2000-2999: Layer 1
- 3000-3999: Layer 2
- 4000-4999: Layer 3 (top)
- 8000-8999: Shield/shutdown components
- 9000-9999: Reflector/boundaries

---

### Subsystem Ranges (General Pattern)

**Allocate by function:**
```
10000-19999: Core region
  10000-10999: Fuel assemblies (driver)
  11000-11999: Control assemblies
  12000-12999: Reflector assemblies

20000-29999: Ex-core components
  20000-20999: Core barrel
  21000-21999: Thermal shield
  22000-22999: Biological shield

30000-39999: Vessel and supports
  30000-30999: Reactor vessel
  31000-31999: Guard vessel
  32000-32999: Support structures

80000-89999: Data cards
  80000: Source definition
  81000-81999: Tallies
  82000-82999: Transformations

90000-99999: Graveyard and boundaries
```

**Document in header:**
```mcnp
c NUMBERING SCHEME:
c   10000-19999: Core region (fuel, control, reflector)
c   20000-29999: Ex-core components (barrel, shields)
c   30000-39999: Vessel and supports
c   80000-89999: Data cards (source, tallies, transforms)
c   90000-99999: Graveyard and outer boundaries
```

---

## Lattice Type Selection

### LAT=1 (Rectangular) - Use For:

**Geometry types:**
- PWR/BWR fuel assemblies (square grid)
- Vertical stacks (1×1×N compact stacks)
- Rectangular TRISO particle arrays (15×15, 23×23)
- Regular cartesian grids
- Box-type assemblies

**Surface requirement:**
- RPP (rectangular parallelepiped)
- Extent = N × pitch

**Example:**
```mcnp
c Particle lattice: 15×15×1 array
1116  10  -1.0  -1116  u=1116  lat=1  fill=-7:7 -7:7 0:0
      1114 1114 1114 ... (225 entries total)
      1115 1115 1115 ...

1116  rpp  -0.75 0.75  -0.75 0.75  -0.025 0.025  $ 15×0.1cm = 1.5cm extent
```

---

### LAT=2 (Hexagonal) - Use For:

**Geometry types:**
- HTGR cores (hexagonal fuel blocks)
- Fast reactor cores (hexagonal assemblies)
- Hexagonal fuel pin bundles
- Any honeycomb pattern
- Hex-duct assemblies

**Surface requirement:**
- RHP (right hexagonal prism)
- Pitch = R × √3 (where R is RHP apothem)

**Example:**
```mcnp
c Hexagonal core: 13×13 assembly array
400  0  -400  u=400  lat=2  fill=-6:6 -6:6 0:0
     300 300 300 300 300 300 100 100 100 300 300 300 300  $ Row j=-6
     300 300 300 100 100 100 100 100 100 100 300 300 300  $ Row j=-5
     ...

400  rhp  0 0 0  0 0 150  0 20 0  $ Height 150cm, R=20cm apothem
c Pitch = 20 × √3 = 34.64 cm
```

**CRITICAL:** Cannot use RPP with LAT=2!

---

### Mixed Lattice Types (Allowed)

**Example: HTGR with rectangular particles in hexagonal core:**
```
Level 2: Particle lattice (LAT=1) - rectangular packing in compact
Level 5: Core lattice (LAT=2) - hexagonal assembly arrangement
```

**Each level chooses appropriate type for its geometry.**

---

## Validation Checklists

### Lattice Hierarchy Validation

**Before implementation:**
- [ ] Drew containment tree diagram
- [ ] Identified all nesting levels (counted from innermost to outermost)
- [ ] Allocated universe number ranges for each level
- [ ] Verified no universe appears in its own fill chain
- [ ] Checked all parent universes defined before children use them

**During implementation:**
- [ ] Small test first (2×2 lattice before 17×17)
- [ ] Plotted each level separately
- [ ] Verified fill array element count matches bounds
- [ ] Checked surface extents match lattice dimensions

**After implementation:**
- [ ] Plotted geometry from 3+ angles
- [ ] VOID test passed (0 lost particles)
- [ ] No dashed lines in plots (no overlaps)
- [ ] Visual inspection confirms expected structure

---

### Numbering Scheme Validation

**Before starting:**
- [ ] Numbering scheme designed and documented
- [ ] Range allocations prevent conflicts
- [ ] Scheme encoded in numbers (hierarchical or functional)
- [ ] Documented in input file header

**During generation:**
- [ ] Script checks for duplicate IDs before writing
- [ ] Cross-references validated (all referenced entities defined)
- [ ] Number ranges respected (no spillover)

**After generation:**
- [ ] Automated check for duplicate cell IDs
- [ ] Automated check for duplicate surface IDs
- [ ] Automated check for duplicate material IDs
- [ ] Automated check for duplicate universe IDs

---

### Surface Type Validation

**For each lattice:**
- [ ] LAT=1 uses RPP (or RPP-equivalent macrobody)
- [ ] LAT=2 uses RHP (right hexagonal prism)
- [ ] Surface extent matches lattice dimensions
  - LAT=1: extent = N × pitch
  - LAT=2: R × √3 = pitch
- [ ] Surface center aligns with lattice origin

---

## Common Patterns Summary

| Reactor Type | Levels | LAT Types | Typical Cells | Numbering Pattern |
|--------------|--------|-----------|---------------|-------------------|
| PWR | 4 | LAT=1 throughout | 1,000-5,000 | Subsystem ranges |
| HTGR | 6 | LAT=1 (pins) + LAT=2 (core) | 5,000-20,000 | Hierarchical encoding |
| Fast Reactor | 5 | LAT=2 throughout | 2,000-10,000 | Subsystem ranges |
| Microreactor | 4-5 | Mixed | 1,000-5,000 | Layer-assembly encoding |

---

**END OF REACTOR PATTERNS REFERENCE**

Use these patterns as starting points, adapt to your specific reactor design.

For detailed automation see: automation_guide.md
For thermal scattering see: thermal_scattering_reference.md
