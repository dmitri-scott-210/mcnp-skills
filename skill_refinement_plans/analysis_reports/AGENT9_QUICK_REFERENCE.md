# CROSS-REFERENCING QUICK REFERENCE GUIDE

## Cell → Surface References

**Basic Syntax:**
```
CELL_ID  MATERIAL  DENSITY  SURFACE_LIST  [OPTIONS]
60106 2106 7.969921E-02  1111 -1118 74 -29 53 100 -110 $ Comment
```

**Boolean Operations:**
- Space = AND: `10 -20 30` → inside 10 AND outside 20 AND inside 30
- Colon = OR: `10:20:30` → inside 10 OR 20 OR 30
- Complement: `#100` → everything NOT in cell 100

**Surface Sense:**
- `+N` or `N` → positive side (inside for spheres/cylinders)
- `-N` → negative side (outside for spheres/cylinders)

---

## Cell → Material References

**Material Assignment:**
```
CELL_ID  MAT_ID  DENSITY  SURFACES
```

**Density Conventions:**
- Positive: atom density (atoms/barn-cm)
  - Example: `2106 7.969921E-02` → 7.97×10⁻² atoms/barn-cm
- Negative: mass density (g/cm³)
  - Example: `9111 -10.924` → 10.924 g/cm³

**Void Cells (Material 0):**
- `0 ... lat=1 fill=...` → Lattice container
- `0 ... fill=U` → Fills with universe U
- `0 ...` → True void (kills particles)

---

## Cell → Universe References

**Universe Declaration:**
```
CELL_ID  MAT  DENSITY  SURFACES  u=UNIVERSE_ID
91101 9111 -10.924 -91111  u=1114 vol=0.092522  $ Cell in universe 1114
```

**Universe Fill:**
```
CELL_ID  0  SURFACES  fill=UNIVERSE_ID  [(X Y Z)]
91111 0 -97011 98005 -98051 fill=1110 (25.547 -24.553 19.108)
```

**Lattice Declaration:**
```
CELL_ID  0  SURFACES  u=U lat=1  fill=X_RANGE Y_RANGE Z_RANGE
91110 0 -91118 u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
```

**Fill Array Shortcuts:**
- `2R` → repeat previous entry 2 times
- `5*1234` → universe 1234 five times
- `1 2 3 4 5` → explicit universe list

---

## AGR-1 Numbering Scheme

### Cell Numbers: 9XYZW
```python
c = 90000 + cap*1000 + stack*100 + 2*(comp-1)*10 + sequence
```
- `9`: AGR identifier
- `X`: Capsule (1-6)
- `Y`: Stack (1-3)
- `Z`: Compact (0,2,4,6 for compacts 1-4)
- `W`: Sequence (0-9)

**Examples:**
- `91101`: Capsule 1, Stack 1, Compact 1, Cell 1
- `93241`: Capsule 3, Stack 2, Compact 4, Cell 1

### Surface Numbers: 9XYZn
```python
s = 9000 + cap*100 + stack*10 + comp
```
- Last digit `n` indicates layer:
  - 1: Kernel surface
  - 2: Buffer surface
  - 3: IPyC surface
  - 4: SiC surface
  - 5: OPyC surface
  - 6: Matrix sphere
  - 7: Lattice box
  - 8: Compact box
  - 9: Compact cylinder

**Examples:**
- `91111`: Capsule 1, Stack 1, Compact 1, Kernel surface
- `91115`: Capsule 1, Stack 1, Compact 1, OPyC surface

### Material Numbers: 9XYZ
```python
m = 9000 + cap*100 + stack*10 + comp
```
- Matches compact location

**Examples:**
- `m9111`: Fuel kernel for Capsule 1, Stack 1, Compact 1
- `m9234`: Fuel kernel for Capsule 2, Stack 3, Compact 4

### Universe Numbers: XYZn
```python
u = cap*100 + stack*10 + comp
```
- Last digit `n` indicates structure level:
  - 0: Full compact assembly
  - 4: TRISO particle
  - 5: Matrix-only cell
  - 6: Particle lattice
  - 7: Matrix block

**Examples:**
- `u=1114`: TRISO particle in Capsule 1, Stack 1, Compact 1
- `u=1110`: Compact assembly in Capsule 1, Stack 1, Compact 1

### Global Surfaces
- **970XX**: Capsule cylinders
  - `97011-97012`: Stack 1
  - `97021-97022`: Stack 2
  - `97031-97032`: Stack 3
  - `97060-97066`: Common capsule walls

- **980XX**: Axial planes
  - Sequential numbering with height

---

## Universe Hierarchy Example (AGR-1)

```
Base Universe (0)
│
├─ Capsule Fill Cell: fill=1110 at (x,y,z)
│  │
│  └─ Universe 1110 (Compact stack, lat=1, vertical)
│     ├─ Universe 1117 (Matrix end caps)
│     └─ Universe 1116 (Particle layer, lat=1, 15×15)
│        ├─ Universe 1114 (TRISO particle)
│        │  ├─ Kernel (cell 91101, material 9111)
│        │  ├─ Buffer (cell 91102, material 9090)
│        │  ├─ IPyC (cell 91103, material 9091)
│        │  ├─ SiC (cell 91104, material 9092)
│        │  ├─ OPyC (cell 91105, material 9093)
│        │  └─ Matrix (cell 91106, material 9094)
│        └─ Universe 1115 (Matrix-only)
```

**Validation Rules:**
1. Define child universes before parent
2. No circular references
3. All filled universes must be defined
4. Lattice array size must match fill entries

---

## Common Surface Types

```
so   R           $ Sphere at origin, radius R
s    X Y Z R     $ Sphere at (X,Y,Z), radius R
cz   R           $ Cylinder along z-axis, radius R
c/z  X Y R       $ Cylinder parallel to z-axis, center (X,Y)
pz   Z           $ Plane perpendicular to z-axis at Z
px   X           $ Plane perpendicular to x-axis at X
py   Y           $ Plane perpendicular to y-axis at Y
p    A B C D     $ General plane: Ax + By + Cz - D = 0
rpp  xmin xmax ymin ymax zmin zmax  $ Rectangular parallelepiped
```

---

## Lattice Dimension Validation

**Formula:**
```
Total elements = (x_max - x_min + 1) × (y_max - y_min + 1) × (z_max - z_min + 1)
```

**Example:**
```
fill=-7:7 -7:7 0:0
Elements = (7-(-7)+1) × (7-(-7)+1) × (0-0+1) = 15 × 15 × 1 = 225
```

**Fill array must have exactly 225 entries!**

---

## Validation Checklist

### Pre-Run Checks
- [ ] All surfaces referenced by cells are defined
- [ ] All materials referenced by cells are defined
- [ ] All universes filled are defined
- [ ] No circular universe references
- [ ] Lattice fill arrays match declared dimensions
- [ ] Comments document all entities
- [ ] Geometry visualized with plotter

### Common Errors
- **Undefined surface:** Cell references surface not in surfaces block
- **Undefined material:** Cell references material not in materials block
- **Undefined universe:** Fill references non-existent universe
- **Lattice mismatch:** Fill array count ≠ (x_range × y_range × z_range)
- **Lost particles:** Gaps in geometry (run test with 100 particles)
- **Overlapping cells:** Multiple cells claim same region
- **Circular reference:** Universe A fills with B, B fills with A

### MCNP Fatal Errors
```
"surface XXX not found" → Undefined surface
"material XXX not found" → Undefined material
"universe recursion detected" → Circular reference
"wrong number of lattice fill entries" → Array size mismatch
"N particles got lost" → Geometry gaps/errors
```

---

## Python Generation Template

```python
# Systematic numbering
for cap in range(1, 7):          # Capsules 1-6
    for stack in range(1, 4):    # Stacks 1-3
        for comp in range(1, 5): # Compacts 1-4

            # Calculate IDs
            cell_base = 90000 + cap*1000 + stack*100 + 2*(comp-1)*10
            surf_base = 9000 + cap*100 + stack*10 + comp
            mat_id = 9000 + cap*100 + stack*10 + comp
            univ_base = cap*100 + stack*10 + comp

            # Generate cells
            cells += f"""
{cell_base+1} {mat_id} -10.924 -{surf_base}1  u={univ_base}4
{cell_base+2} 9090 -1.100 {surf_base}1 -{surf_base}2  u={univ_base}4
"""

            # Generate surfaces
            surfaces += f"""
{surf_base}1 so 0.01748  $ Kernel
{surf_base}2 so 0.02763  $ Buffer
"""

            # Generate materials
            materials += f"""
m{mat_id}
     92235.00c  0.199636
     92238.00c  0.796829
"""
```

---

## Best Practices

### Numbering
1. Allocate digit ranges by entity type
2. Embed hierarchy in number structure
3. Correlate related entities (cell 1234 → material 1234 → surface 1234)
4. Reserve gaps for future expansion
5. Document scheme in header

### Cross-Referencing
1. Define before use (surfaces before cells)
2. Use comments on every definition
3. Group related entities together
4. Validate completeness before running

### Universe Design
1. Plan hierarchy before implementation
2. Draw tree diagram of containment
3. Higher numbers for deeper nesting
4. Test small lattice before scaling up

### Automation
1. Use scripts for repetitive structures
2. Validate generated output
3. Version control generation code
4. Comment script logic clearly

---

## Quick Debugging Guide

**Problem:** "surface XXX not found"
- **Solution:** Add surface XXX to surfaces block or fix typo in cell

**Problem:** "N particles got lost"
- **Solution:** Visualize geometry, look for gaps, add cells to fill voids

**Problem:** "wrong number of lattice fill entries"
- **Solution:** Count array elements, verify matches (x_max-x_min+1)×(y_max-y_min+1)×(z_max-z_min+1)

**Problem:** Universe recursion
- **Solution:** Map fill chain, find cycle, restructure hierarchy

**Problem:** Results don't make physical sense
- **Solution:** Check density signs (+ for atoms/barn-cm, - for g/cm³)

---

## File Locations

**Full Analysis:**
```
/home/user/mcnp-skills/analysis_reports/AGENT9_CROSS_REFERENCING_PATTERNS.md
```

**Example Files:**
```
/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/agr-1/
├── bench.template
├── create_inputs.py
└── mcnp/bench_138B.i
```
